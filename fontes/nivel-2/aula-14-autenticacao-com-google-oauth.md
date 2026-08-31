# Aula 14 — Autenticação com Google (OAuth 2.0)

> **Nível 2 — Desenvolvimento Web** · Unidade 3: Web dinâmica server-side
> WebLab · UNEMAT Sinop · Prof. Ivan Luiz Pedroso Pires
> **Carga:** 3 aulas de 50 min (presencial) + 1 h (assíncrona)

Sua API está completa e tem um problema grave: qualquer pessoa com um terminal pode apagar o cardápio inteiro do Café Cerrado. `curl -X DELETE http://localhost:3000/api/produtos/1` e pronto. Hoje a aplicação aprende a responder a pergunta que separa um exercício de um sistema de verdade — **quem está fazendo esta requisição?** — sem que você precise guardar a senha de ninguém.

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Distinguir autenticação de autorização e escolher entre `401` e `403` em cada situação.
- Explicar o papel do OAuth 2.0 e do OpenID Connect no login com contas de terceiros.
- Ler a estrutura de um JWT e explicar por que decodificar um token não é o mesmo que verificá-lo.
- Configurar um projeto no Google Cloud Console e obter um Client ID para aplicação web.
- Renderizar o botão do Google no front com a biblioteca Google Identity Services.
- Verificar o ID token no servidor com `google-auth-library` e emitir um token de sessão próprio, assinado.
- Proteger as rotas de escrita da API com um middleware que devolve `401` sem token válido.
- Guardar segredos em `.env`, mantê-los fora do Git e justificar por que isso é inegociável.

## 📋 Pré-requisitos desta aula

Na Aula 13 a API do Café Cerrado ganhou controladores, CRUD completo e persistência em arquivo JSON — está funcional, organizada e escancarada. Hoje colocamos uma porta na frente das operações de escrita: o front delega o login ao Google, o servidor verifica quem chegou e só então deixa criar, editar ou excluir.

Checklist antes de começar:

- [ ] `cafe-cerrado-api` com os cinco endpoints de `/api/produtos` respondendo (Aula 13).
- [ ] O site do Café Cerrado sendo servido por `express.static('public')` em `http://localhost:3000`.
- [ ] `testes.http` funcionando com a extensão REST Client.
- [ ] Uma conta Google (Gmail) para usar no Google Cloud Console — se possível, já com o console aberto.
- [ ] Git configurado no repositório, com `node_modules/` já ignorado no `.gitignore`.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Autenticação × autorização; OAuth 2.0 e OpenID Connect; anatomia do JWT |
| 2 | 50 min | Google Cloud Console, `.env`, verificação do ID token e sessão assinada |
| 3 | 50 min | Botão do Google no front, middleware `exigirLogin`, testes de `401`; laboratório |

## 1. Autenticação não é autorização

Duas perguntas diferentes, feitas em momentos diferentes, com respostas diferentes:

- **Autenticação** responde "quem é você?". O resultado é uma identidade: `maria@gmail.com`.
- **Autorização** responde "o que você pode fazer?". O resultado é uma permissão: "pode criar produtos, não pode excluir os dos outros".

Confundir as duas gera bugs difíceis de enxergar. O HTTP tem um status para cada caso, e os nomes atrapalham:

| Status | Nome oficial | Significa de verdade |
|---|---|---|
| `401` | Unauthorized | Não sei quem você é. Faça login. |
| `403` | Forbidden | Sei quem você é, e você não pode fazer isso. |

Sim, o `401` se chama "Unauthorized" e quer dizer "não autenticado" — um erro de nomenclatura que ficou na especificação do HTTP para sempre. Guarde pelo comportamento, não pelo nome: `401` é convite para o front mostrar a tela de login; `403` é para mostrar "você não tem permissão", porque fazer login de novo não vai resolver.

Hoje implementamos a autenticação e o `401`. Na Aula 16, cada produto ganha um dono e aparece o primeiro `403`.

> **⚠️ Atenção**
> Esconder o botão "Excluir" para quem não está logado **não é** autorização. É cortesia com o usuário. Qualquer pessoa abre o DevTools, remove o atributo `hidden` e clica; ou pula o seu site inteiro e manda a requisição pelo `curl`. A proteção real acontece no servidor, em toda requisição sensível, sem exceção. Interface é conveniência; servidor é segurança.

## 2. Delegar o login: OAuth 2.0 e OpenID Connect

A alternativa óbvia seria criar uma tabela de usuários com e-mail e senha. Pense no que isso obriga você a fazer direito, sem errar nenhuma vez:

- Nunca guardar a senha em texto puro — usar uma função de hash lenta e com sal (bcrypt, scrypt, argon2).
- Implementar "esqueci minha senha" com token de uso único e expiração.
- Limitar tentativas de login para dificultar ataque de força bruta.
- Detectar vazamentos, avisar usuários, forçar troca de senha.
- Lidar com o fato de que as pessoas reutilizam a mesma senha em dez sites — o vazamento do seu projeto de faculdade vira o problema do banco delas.

É muita responsabilidade para um cardápio de cafeteria. A indústria resolveu isso delegando a autenticação a um **provedor de identidade** que já faz tudo isso em escala: Google, Microsoft, Apple, GitHub. É o "Entrar com Google" que você usa todo dia sem pensar.

Dois protocolos sustentam isso:

- **OAuth 2.0** (RFC 6749) é um protocolo de **autorização delegada**: permite que um aplicativo acesse recursos em nome do usuário — ler a agenda, enviar um e-mail — sem nunca conhecer a senha dele. Ele não foi criado para dizer quem o usuário é.
- **OpenID Connect (OIDC)** é uma camada de **identidade** construída em cima do OAuth 2.0. Ela acrescenta um artefato que o OAuth sozinho não tem: o **ID token**, um documento assinado pelo provedor dizendo "esta pessoa é `maria@gmail.com`, e eu, Google, garanto".

O que vamos usar hoje é OIDC, no fluxo mais simples que existe para aplicação web: o Google devolve o ID token direto ao navegador, e o navegador o entrega ao nosso servidor, que verifica a assinatura.

### 2.1 Os três papéis

| Papel | Quem é aqui | O que faz |
|---|---|---|
| Usuário | A pessoa no navegador | Escolhe entrar com a conta Google |
| Cliente | O Café Cerrado (front + API) | Recebe o token e decide o que liberar |
| Provedor de identidade | O Google | Autentica a pessoa e assina o ID token |

Repare no que **não** acontece: a senha do usuário nunca passa pelo seu servidor, nunca aparece no seu código e nunca vira sua responsabilidade. O login acontece inteiramente no domínio do Google. Você recebe só o resultado, assinado.

> **🧠 Você sabia?**
> A biblioteca JavaScript que a maior parte dos tutoriais na internet ainda ensina — `gapi.auth2`, do "Google Sign-In for Websites" — foi descontinuada e **desligada em 2023**. Código escrito com ela simplesmente não funciona mais: o botão não aparece e o console reclama de `idpiframe_initialization_failed`. A substituta é a **Google Identity Services (GSI)**, que usamos hoje. Isso é um bom lembrete de um fato da profissão: a idade do tutorial importa mais que o número de estrelas dele. Antes de copiar uma solução de autenticação da internet, procure a data e confira na documentação oficial se a API ainda existe.

## 3. O ID token por dentro: anatomia de um JWT

O ID token é um **JWT** (JSON Web Token, RFC 7519). Ele parece uma sopa de letras, mas tem estrutura rígida: três blocos separados por ponto.

```text
eyJhbGciOiJSUzI1NiIsImtpZCI6IjEyMyJ9.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20ifQ.QWJjRGVmR2hpSmts
└──────── cabeçalho ────────┘ └──────────── dados (payload) ────────────┘ └──── assinatura ────┘
```

- **Cabeçalho**: qual algoritmo assinou (`RS256`) e qual chave foi usada (`kid`).
- **Dados**: as informações do usuário e do próprio token, chamadas *claims*.
- **Assinatura**: o resultado de assinar cabeçalho + dados com a chave **privada** do Google.

Os dois primeiros blocos são apenas **base64url** — uma codificação, não uma criptografia. Qualquer pessoa lê o conteúdo. Isso não é falha: o JWT não foi feito para esconder, foi feito para **provar autoria**.

As claims que interessam em um ID token do Google:

| Claim | Exemplo | Para que serve |
|---|---|---|
| `iss` | `https://accounts.google.com` | Quem emitiu o token |
| `aud` | `1234....apps.googleusercontent.com` | Para **qual aplicação** o token foi emitido |
| `sub` | `114857...` | Identificador único e permanente do usuário |
| `exp` | `1731628800` | Instante em que o token expira (cerca de 1 h) |
| `email` | `maria@gmail.com` | E-mail da conta |
| `email_verified` | `true` | Se o Google confirmou o e-mail |
| `name` / `picture` | `Maria Silva` / URL | Nome e foto do perfil |

### 3.1 Decodificar não é verificar

Esta é a ideia mais importante da aula inteira.

**Decodificar** é desfazer o base64url e ler o JSON. Faz-se no navegador, em uma linha, e não prova absolutamente nada — eu posso escrever um JSON dizendo que sou `reitoria@unemat.br`, codificar em base64url e mandar para a sua API.

**Verificar** é conferir a assinatura com a **chave pública** do Google e checar três coisas: que `iss` é o Google, que `exp` ainda não passou e que `aud` é exatamente o **seu** Client ID. Só a chave privada do Google produz uma assinatura que bate com a chave pública dele — e essa chave privada nunca sai dos servidores do Google.

A checagem de `aud` é a que mais gente esquece, e é a mais perigosa. Sem ela, um token legítimo emitido para **outro** aplicativo qualquer é aceito pela sua API. Como qualquer pessoa pode criar um aplicativo no Google e obter tokens válidos dos próprios usuários, esquecer o `aud` transforma sua verificação em teatro.

A biblioteca `google-auth-library` faz as quatro checagens em uma chamada, desde que você passe o `audience`. É por isso que a usamos em vez de escrever a verificação à mão.

> **🔬 Investigue**
> Abra <https://myaccount.google.com> em uma aba para garantir que está logado. Depois, no console do navegador, cole `atob('eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJlbWFpbCI6ImV4ZW1wbG9AZ21haWwuY29tIn0')` e veja um JSON aparecer. Você acabou de "abrir" um pedaço de token sem nenhuma chave. Agora responda por escrito, em duas linhas: se ler é tão fácil assim, o que exatamente impede alguém de **inventar** um token dizendo que é você? No fim da aula, quando tiver um ID token de verdade, repita a experiência com ele: `atob(token.split('.')[1])` mostra as suas próprias claims.

> **🔎 Por baixo do capô**
> Como o `verifyIdToken` conhece a chave pública do Google? Ele busca em `https://www.googleapis.com/oauth2/v3/certs`, um endereço público que devolve o conjunto de chaves em uso, cada uma com o seu `kid`. O cabeçalho do token diz qual `kid` usar; a biblioteca escolhe a chave certa e confere a assinatura. As chaves são trocadas de tempos em tempos, e a biblioteca respeita o `Cache-Control` da resposta para não buscar a lista a cada requisição. É por isso que a verificação funciona sem você configurar chave nenhuma — e também por isso que ela precisa de internet.

## 4. O fluxo, passo a passo

O que acontece entre o clique no botão e o produto criado:

1. O front pede ao Google que desenhe o botão "Entrar com o Google", informando o Client ID da aplicação.
2. O usuário clica; o Google abre a própria tela de login (ou reconhece uma sessão já ativa). **A senha é digitada no domínio do Google, nunca no seu.**
3. O Google devolve ao seu front um **ID token** assinado, entregue a uma função de callback que você registrou.
4. O front envia esse token ao seu back-end, em `POST /api/auth/google`.
5. O back-end verifica a assinatura, o emissor, a validade e o `aud` com `google-auth-library`. Deu certo: o Google garante a identidade.
6. O back-end cria a **sua própria sessão** — um token curto, assinado por você — e devolve ao front junto com nome, e-mail e foto.
7. Dali em diante, toda requisição de escrita leva o cabeçalho `Authorization: Bearer <token da sessão>`, e o middleware `exigirLogin` confere antes de deixar o controlador rodar.

| Etapa | Onde acontece | O que trafega |
|---|---|---|
| 1 a 3 | Navegador ↔ Google | Credenciais do usuário e o ID token |
| 4 e 5 | Navegador → sua API | ID token, verificado no servidor |
| 6 e 7 | Sua API ↔ navegador | Token de sessão da sua aplicação |

## 5. Segredos, `.env` e o que nunca vai para o Git

Sua aplicação vai precisar de dois valores de configuração:

- `GOOGLE_CLIENT_ID` — identifica a sua aplicação para o Google.
- `SESSAO_SEGREDO` — a chave com que **você** assina os seus tokens de sessão.

O primeiro **não é segredo**: ele aparece no HTML de qualquer site que use login do Google, e tem que aparecer mesmo, porque o navegador precisa dele. O segundo é segredo de verdade: quem o tiver consegue forjar sessões válidas da sua aplicação e entrar como qualquer usuário.

Mesmo assim, os dois vão para o mesmo lugar — um arquivo `.env` fora do Git — por um motivo prático: **configuração que muda entre máquinas não pertence ao código**. O Client ID do seu computador é diferente do Client ID do servidor de produção; o segredo de sessão também. Deixá-los fora do código é o que permite publicar o mesmo repositório em qualquer lugar.

```text
GOOGLE_CLIENT_ID=000000000000-abcdefghijklmnopqrstuvwxyz012345.apps.googleusercontent.com
SESSAO_SEGREDO=troque-por-uma-frase-longa-gerada-aleatoriamente
PORTA=3000
```

> **⚠️ Atenção**
> Um segredo commitado no GitHub é considerado **vazado para sempre**, mesmo que você apague no commit seguinte: o histórico do Git guarda tudo, e existem robôs varrendo repositórios públicos em busca de chaves — em minutos, não em dias. Se acontecer com você, a resposta correta não é apagar o arquivo: é **revogar a credencial** no console do provedor e gerar outra. Coloque `.env` no `.gitignore` **antes** do primeiro `git add`.

> **💡 Dica**
> Commite um `.env.exemplo` com as chaves e valores fictícios. Ele documenta o que a aplicação precisa para rodar e evita a mensagem "clonei o projeto e não funciona". O `README.md` só precisa dizer: copie `.env.exemplo` para `.env` e preencha.

## 6. Sessão própria: por que não usar o token do Google em tudo

Uma dúvida honesta aparece aqui: já que o front tem um ID token do Google, por que não mandar esse token em toda requisição e verificar de novo no servidor a cada vez?

Funciona, e muitos tutoriais fazem exatamente isso. Mas tem três problemas:

1. **Custo.** Cada verificação consulta as chaves públicas do Google. Há cache, mas ainda assim você amarra o funcionamento da sua API à disponibilidade de um serviço externo — em toda requisição.
2. **Validade curta.** O ID token do Google expira em cerca de uma hora e **não** pode ser renovado sem interação do usuário nesse fluxo. Sua sessão passa a durar o que o Google decidir.
3. **Informação sua.** Quando o projeto crescer, a sessão precisa carregar dados que só a sua aplicação conhece: papel de administrador, preferências, plano contratado. Nada disso cabe em um token emitido pelo Google.

Por isso o padrão é: **verifique o token do provedor uma vez, no login, e emita a sua própria sessão**. É o que faremos, com um token bem simples de dois blocos:

```text
<dados em base64url>.<assinatura HMAC-SHA256>
```

Assinar com HMAC significa calcular um resumo criptográfico dos dados **misturado com o seu segredo**. Sem o segredo, ninguém consegue produzir a assinatura correta — então ninguém consegue alterar os dados sem invalidar o token. É o mesmo princípio do JWT do Google, com um algoritmo simétrico (a mesma chave assina e confere), que é o suficiente quando quem assina e quem confere são o mesmo servidor.

Você vai escrever isso com o módulo `node:crypto`, que já vem no Node — sem instalar nada.

> **📌 Na prova**
> Saiba explicar por que a assinatura de um token não pode ser comparada com `===`. Comparar strings byte a byte com parada no primeiro byte diferente vaza informação pelo **tempo** de resposta: um atacante que meça milhares de tentativas consegue descobrir a assinatura correta byte a byte. A defesa é comparar em tempo constante — em Node, `crypto.timingSafeEqual`.

## 🧩 Padrão de projeto em uso: Chain of Responsibility

O middleware do Express, que você usa desde a Aula 12, é uma implementação do padrão **Chain of Responsibility** (GoF): uma requisição percorre uma corrente de manipuladores, e cada um decide se trata, se repassa (`next()`) ou se interrompe respondendo.

A cadeia que a rota `POST /api/produtos` terá ao fim desta aula:

| Ordem | Elo | Decisão |
|---|---|---|
| 1 | `express.json()` | Transforma o corpo em objeto e repassa |
| 2 | Log | Registra e repassa |
| 3 | `exigirLogin` | Repassa com `req.usuario`, ou responde `401` e interrompe |
| 4 | `controlador.criar` | Valida, grava e responde |

O ganho do padrão é que cada elo ignora completamente os outros. O `exigirLogin` não sabe que existe um controlador de produtos; o controlador não sabe como a identidade chegou em `req.usuario` — se veio do Google, de um login com senha ou de um teste automatizado. Trocar o provedor de identidade um dia significará reescrever um arquivo, e nenhum controlador.

Esse desacoplamento tem um preço conhecido: como qualquer elo pode interromper a corrente, esquecer um `next()` faz a requisição travar sem erro nenhum. É o bug mais silencioso do Express.

## 💻 Mão na massa — login com Google no Café Cerrado

Ao fim desta prática, o site do Café Cerrado terá um botão de login do Google, e as rotas de escrita da API só funcionarão para quem estiver autenticado.

### Passo 1 — Criar o projeto no Google Cloud Console

1. Acesse <https://console.cloud.google.com> com a sua conta Google.
2. No seletor de projetos, no topo da página, escolha **Novo projeto**. Dê o nome `cafe-cerrado` e crie.
3. Confirme, no seletor, que o projeto novo é o **projeto ativo**. Configurar credenciais no projeto errado é o tropeço mais comum deste passo.
4. No menu, vá em **APIs e serviços → Tela de permissão OAuth**. Escolha o tipo **Externo** e preencha: nome do app (`Café Cerrado`), e-mail de suporte e e-mail do desenvolvedor. Salve.
5. Ainda na tela de permissão, adicione o seu próprio e-mail em **Usuários de teste**. Enquanto o app estiver como "em teste", só usuários dessa lista conseguem entrar — e isso é ótimo para um trabalho de faculdade.
6. Vá em **Credenciais → Criar credenciais → ID do cliente OAuth**. Tipo de aplicativo: **Aplicativo da Web**. Nome: `cafe-cerrado-local`.
7. Em **Origens JavaScript autorizadas**, adicione exatamente `http://localhost:3000`. Sem barra no final.
8. Crie e copie o **Client ID**, no formato `000000000000-letras.apps.googleusercontent.com`.

> **⚠️ Atenção**
> "Origem" é o trio protocolo + host + porta. `http://localhost:3000` e `http://127.0.0.1:3000` são origens **diferentes** para o Google, e `http://localhost:5500` (a porta do Live Server) é outra ainda. Se você abrir o site pelo Live Server em vez de pelo seu servidor Express, o botão do Google não vai aparecer e o console vai dizer `The given origin is not allowed for the given client ID`. Nesta aula, o site é sempre servido pelo Express — é o `express.static('public')` da Aula 11 que faz isso.

### Passo 2 — Instalar as dependências e guardar os segredos

```bash
cd cafe-cerrado-api
npm install google-auth-library dotenv
```

Gere um segredo de sessão de verdade, aleatório, em vez de inventar um:

```bash
node -e "console.log(require('node:crypto').randomBytes(32).toString('hex'))"
```

Crie o `.env` na raiz do projeto com o Client ID do passo 1 e o segredo gerado:

`cafe-cerrado-api/.env`

```text
GOOGLE_CLIENT_ID=000000000000-abcdefghijklmnopqrstuvwxyz012345.apps.googleusercontent.com
SESSAO_SEGREDO=8f2b1c9d4e7a0b3f6c5d8e1a4b7c0d3e6f9a2b5c8d1e4f7a0b3c6d9e2f5a8b1c
PORTA=3000
```

Crie também o exemplo, que **vai** para o Git:

`cafe-cerrado-api/.env.exemplo`

```text
GOOGLE_CLIENT_ID=cole-aqui-o-client-id-do-google-cloud-console
SESSAO_SEGREDO=gere-com-node-e-crypto-randomBytes-32-hex
PORTA=3000
```

E ignore o `.env` **antes** de qualquer commit:

`cafe-cerrado-api/.gitignore`

```text
node_modules/
.env
*.tmp
```

Confirme que deu certo antes de seguir. O comando abaixo não pode listar o `.env`:

```bash
git status --short
git check-ignore -v .env
```

O primeiro mostra o que entraria no commit; o segundo confirma qual regra do `.gitignore` está barrando o arquivo. Se `git status` mostrar `.env`, pare tudo e resolva agora.

### Passo 3 — O token de sessão assinado

Crie a pasta `auth/` e o módulo que assina e confere as sessões. Ele não sabe nada sobre HTTP nem sobre Google: só transforma um usuário em texto assinado e de volta.

`cafe-cerrado-api/auth/sessao.js`

```js
// Token de sessão da própria aplicação: dados em base64url + assinatura HMAC.
// Quem não tem o SESSAO_SEGREDO não consegue produzir uma assinatura válida.
const crypto = require('node:crypto');

const DURACAO_MS = 8 * 60 * 60 * 1000; // 8 horas

function segredo() {
  const valor = process.env.SESSAO_SEGREDO;
  if (!valor) {
    throw new Error('SESSAO_SEGREDO não definido. Confira o arquivo .env.');
  }
  return valor;
}

function assinar(conteudo) {
  return crypto.createHmac('sha256', segredo()).update(conteudo).digest('base64url');
}

function criarToken(usuario) {
  const dados = {
    email: usuario.email,
    nome: usuario.nome,
    foto: usuario.foto,
    expiraEm: Date.now() + DURACAO_MS,
  };
  const corpo = Buffer.from(JSON.stringify(dados), 'utf-8').toString('base64url');
  return `${corpo}.${assinar(corpo)}`;
}

// Devolve os dados do usuário se o token for válido; null em qualquer outro caso.
function lerToken(token) {
  if (typeof token !== 'string') {
    return null;
  }

  const partes = token.split('.');
  if (partes.length !== 2) {
    return null;
  }

  const [corpo, assinaturaRecebida] = partes;
  const assinaturaEsperada = assinar(corpo);

  const recebida = Buffer.from(assinaturaRecebida);
  const esperada = Buffer.from(assinaturaEsperada);
  if (recebida.length !== esperada.length || !crypto.timingSafeEqual(recebida, esperada)) {
    return null;
  }

  try {
    const dados = JSON.parse(Buffer.from(corpo, 'base64url').toString('utf-8'));
    if (typeof dados.expiraEm !== 'number' || Date.now() > dados.expiraEm) {
      return null;
    }
    return { email: dados.email, nome: dados.nome, foto: dados.foto };
  } catch (erro) {
    return null;
  }
}

module.exports = { criarToken, lerToken };
```

Três detalhes que valem a leitura atenta:

- A assinatura é conferida **antes** de o JSON ser interpretado. Nunca confie no conteúdo de um token cuja assinatura você ainda não validou.
- `timingSafeEqual` exige buffers do mesmo tamanho — por isso a comparação de comprimento vem antes, com `||` (que não avalia o lado direito quando o esquerdo já é verdadeiro).
- `lerToken` devolve `null` para todo problema: token torto, assinatura errada, JSON quebrado, prazo vencido. Quem chama não precisa distinguir os casos, e o atacante também não descobre qual foi o erro.

### Passo 4 — Verificando o ID token do Google

`cafe-cerrado-api/controllers/authController.js`

```js
const { OAuth2Client } = require('google-auth-library');
const sessao = require('../auth/sessao');

const cliente = new OAuth2Client(process.env.GOOGLE_CLIENT_ID);

// POST /api/auth/google  { "credential": "<ID token do Google>" }
exports.entrarComGoogle = async (req, res) => {
  const { credential } = req.body ?? {};
  if (!credential) {
    return res.status(400).json({ erro: 'Envie o campo credential com o ID token do Google.' });
  }

  let bilhete;
  try {
    bilhete = await cliente.verifyIdToken({
      idToken: credential,
      audience: process.env.GOOGLE_CLIENT_ID, // o token foi emitido para NÓS?
    });
  } catch (erro) {
    console.error('Falha ao verificar o ID token:', erro.message);
    return res.status(401).json({ erro: 'Token do Google inválido ou expirado.' });
  }

  const dados = bilhete.getPayload();
  if (!dados.email_verified) {
    return res.status(401).json({ erro: 'A conta Google precisa ter e-mail verificado.' });
  }

  const usuario = { email: dados.email, nome: dados.name, foto: dados.picture };
  res.json({ usuario, token: sessao.criarToken(usuario) });
};

// GET /api/auth/eu — quem sou eu, segundo o servidor
exports.eu = (req, res) => {
  res.json({ usuario: req.usuario });
};
```

Aqui o `try/catch` é obrigatório, apesar do Express 5 capturar erros de funções `async` sozinho. O motivo: um token inválido não é um erro **inesperado** do servidor — é uma resposta esperada da aplicação. Sem o `catch`, a falha viraria `500 Erro interno do servidor`, e o front concluiria que a sua API está quebrada em vez de pedir um novo login. Use o tratador global para o que você não previu; trate explicitamente o que você previu.

> **💡 Dica**
> Note que a aplicação nunca usa *client secret*. No fluxo do Google Identity Services para aplicações web, o token chega ao navegador e é verificado por assinatura — não há troca de código por token no servidor, então não há segredo do cliente envolvido. Se algum tutorial mandar você colar um `client_secret` no front-end, feche a página.

### Passo 5 — O middleware `exigirLogin` e as rotas protegidas

`cafe-cerrado-api/middlewares/exigirLogin.js`

```js
const sessao = require('../auth/sessao');

// Barra a requisição que não trouxer um token de sessão válido.
// Quando passa, deixa req.usuario disponível para os controladores.
module.exports = function exigirLogin(req, res, next) {
  const cabecalho = req.headers.authorization ?? '';

  if (!cabecalho.startsWith('Bearer ')) {
    return res.status(401).json({ erro: 'Faça login para continuar.' });
  }

  const usuario = sessao.lerToken(cabecalho.slice(7));
  if (!usuario) {
    return res.status(401).json({ erro: 'Sessão inválida ou expirada. Entre novamente.' });
  }

  req.usuario = usuario;
  next();
};
```

`cabecalho.slice(7)` corta exatamente os 7 caracteres de `'Bearer '`. Esse formato — o esquema, um espaço e a credencial — está na especificação do HTTP; `Bearer` significa "portador": quem apresentar o token é tratado como dono dele. É por isso que um token vazado é tão sério quanto uma senha vazada, e por isso que ele expira.

Agora o arquivo de rotas de produtos: leitura aberta, escrita protegida. Duas palavras a mais por linha.

`cafe-cerrado-api/routes/produtos.js`

```js
const express = require('express');
const controlador = require('../controllers/produtosController');
const exigirLogin = require('../middlewares/exigirLogin');

const router = express.Router();

router.get('/', controlador.listar);
router.get('/:id', controlador.obter);
router.post('/', exigirLogin, controlador.criar);
router.put('/:id', exigirLogin, controlador.atualizar);
router.delete('/:id', exigirLogin, controlador.remover);

module.exports = router;
```

Leia essas cinco linhas como um documento de política de acesso: qualquer visitante lê o cardápio; só quem está logado altera. Essa clareza é consequência direta da separação que você fez na Aula 13 — com a lógica dentro das rotas, essa política estaria diluída em cem linhas.

`cafe-cerrado-api/routes/auth.js`

```js
const express = require('express');
const controlador = require('../controllers/authController');
const exigirLogin = require('../middlewares/exigirLogin');

const router = express.Router();

router.post('/google', controlador.entrarComGoogle);
router.get('/eu', exigirLogin, controlador.eu);

module.exports = router;
```

### Passo 6 — Montando tudo no `server.js`

`cafe-cerrado-api/server.js`

```js
// A PRIMEIRA linha do projeto: carrega o .env em process.env.
// Precisa vir antes de qualquer require que leia process.env.
require('dotenv').config();

const express = require('express');
const produtosRouter = require('./routes/produtos');
const authRouter = require('./routes/auth');

const app = express();
const PORTA = Number(process.env.PORTA) || 3000;

// Falha cedo e com mensagem clara se a configuração estiver incompleta.
for (const chave of ['GOOGLE_CLIENT_ID', 'SESSAO_SEGREDO']) {
  if (!process.env[chave]) {
    console.error(`Variável ${chave} ausente. Copie .env.exemplo para .env e preencha.`);
    process.exit(1);
  }
}

app.use(express.json());

app.use((req, res, next) => {
  const inicio = Date.now();
  res.on('finish', () => {
    const duracao = Date.now() - inicio;
    console.log(`${req.method} ${req.originalUrl} -> ${res.statusCode} (${duracao} ms)`);
  });
  next();
});

app.use(express.static('public'));

// Configuração pública que o front precisa conhecer.
// O Client ID não é segredo; o segredo de sessão nunca sai daqui.
app.get('/api/config', (req, res) => {
  res.json({ googleClientId: process.env.GOOGLE_CLIENT_ID });
});

app.use('/api/auth', authRouter);
app.use('/api/produtos', produtosRouter);

app.all('/api/{*splat}', (req, res) => {
  res.status(404).json({ erro: `Rota ${req.method} ${req.originalUrl} não existe.` });
});

app.use((erro, req, res, next) => {
  console.error(erro);
  res.status(500).json({ erro: 'Erro interno do servidor.' });
});

app.listen(PORTA, () => {
  console.log(`Café Cerrado API em http://localhost:${PORTA}`);
});
```

A ordem do `require('dotenv').config()` não é estética. O `authController.js` executa `new OAuth2Client(process.env.GOOGLE_CLIENT_ID)` no momento em que é importado — se o `.env` ainda não tiver sido carregado, o cliente nasce com `undefined` e toda verificação falha com uma mensagem confusa. Carregue a configuração antes de tudo.

> **💡 Dica**
> O Node 22 lê variáveis de ambiente sem biblioteca nenhuma: `node --env-file=.env server.js`. É uma opção legítima e um argumento a menos no `package.json` de dependências. Usamos o `dotenv` porque ele funciona igual em qualquer versão e em qualquer serviço de hospedagem, inclusive nos que você vai encontrar na trilha de Deploy. Saber que a alternativa nativa existe é o que importa.

### Passo 7 — O botão do Google no front

Primeiro o HTML. Coloque o bloco dentro do `header` do site, ao lado do menu:

`cafe-cerrado-api/public/index.html` (dentro do `header`, depois do `nav`)

```html
<div class="autenticacao">
  <div id="area-login">
    <div id="botao-google"></div>
  </div>

  <div id="area-usuario" hidden>
    <img id="foto-usuario" src="" alt="" width="32" height="32" class="avatar">
    <span id="nome-usuario"></span>
    <button type="button" id="btn-sair">Sair</button>
  </div>

  <p id="aviso-login" role="status" aria-live="polite"></p>
</div>

<script src="https://accounts.google.com/gsi/client" async defer></script>
<script type="module" src="js/auth.js"></script>
```

O `alt=""` da foto é proposital: o nome do usuário está escrito ao lado, em texto. Uma imagem puramente decorativa com `alt` vazio é ignorada pelo leitor de tela, e é exatamente isso que se quer — repetir "foto de Maria Silva" logo antes de ler "Maria Silva" só atrapalha. O `role="status"` com `aria-live="polite"` faz o leitor de tela anunciar as mensagens de login sem interromper o que o usuário estiver fazendo.

Agora o módulo de autenticação:

`cafe-cerrado-api/public/js/auth.js`

```js
// Autenticação do Café Cerrado com Google Identity Services.
const CHAVE_SESSAO = 'cafe-cerrado-sessao';

const areaLogin = document.querySelector('#area-login');
const areaUsuario = document.querySelector('#area-usuario');
const nomeUsuario = document.querySelector('#nome-usuario');
const fotoUsuario = document.querySelector('#foto-usuario');
const botaoSair = document.querySelector('#btn-sair');
const aviso = document.querySelector('#aviso-login');

export function obterSessao() {
  const bruto = sessionStorage.getItem(CHAVE_SESSAO);
  if (!bruto) {
    return null;
  }
  try {
    return JSON.parse(bruto);
  } catch (erro) {
    sessionStorage.removeItem(CHAVE_SESSAO);
    return null;
  }
}

export function obterToken() {
  return obterSessao()?.token ?? null;
}

function mostrarUsuario(usuario) {
  nomeUsuario.textContent = usuario.nome;
  fotoUsuario.src = usuario.foto;
  areaUsuario.hidden = false;
  areaLogin.hidden = true;
  document.dispatchEvent(new CustomEvent('sessao-alterada'));
}

export function sair() {
  sessionStorage.removeItem(CHAVE_SESSAO);
  google.accounts.id.disableAutoSelect();
  areaUsuario.hidden = true;
  areaLogin.hidden = false;
  aviso.textContent = 'Você saiu da sua conta.';
  document.dispatchEvent(new CustomEvent('sessao-alterada'));
}

// Chamado pelo Google quando o login termina com sucesso.
async function aoReceberCredencial(resposta) {
  aviso.textContent = 'Entrando…';

  const requisicao = await fetch('/api/auth/google', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ credential: resposta.credential }),
  });

  if (!requisicao.ok) {
    const corpo = await requisicao.json().catch(() => ({}));
    aviso.textContent = corpo.erro ?? 'Não foi possível entrar. Tente de novo.';
    return;
  }

  const sessao = await requisicao.json();
  sessionStorage.setItem(CHAVE_SESSAO, JSON.stringify(sessao));
  aviso.textContent = '';
  mostrarUsuario(sessao.usuario);
}

async function iniciar() {
  const configuracao = await fetch('/api/config').then((r) => r.json());

  google.accounts.id.initialize({
    client_id: configuracao.googleClientId,
    callback: aoReceberCredencial,
  });

  google.accounts.id.renderButton(document.querySelector('#botao-google'), {
    type: 'standard',
    theme: 'outline',
    size: 'large',
    text: 'signin_with',
    locale: 'pt-BR',
  });

  const sessao = obterSessao();
  if (sessao) {
    mostrarUsuario(sessao.usuario);
  }
}

botaoSair.addEventListener('click', sair);

// O script do Google carrega com "async": pode chegar antes ou depois deste módulo.
if (window.google?.accounts?.id) {
  iniciar();
} else {
  window.onGoogleLibraryLoad = iniciar;
}
```

Duas decisões merecem discussão:

- **A corrida do carregamento.** O script do Google tem `async`, então não há garantia de ordem entre ele e o seu módulo. Chamar `google.accounts.id.initialize` direto dá `TypeError: Cannot read properties of undefined (reading 'accounts')` em metade das vezes — o pior tipo de bug, o que só aparece às vezes. O bloco final cobre os dois cenários: se a biblioteca já está lá, inicia; se não, registra `window.onGoogleLibraryLoad`, o gancho que a própria GSI chama ao terminar de carregar.
- **O `CustomEvent`.** O módulo avisa o resto da aplicação toda vez que a sessão muda. Na Aula 15, o `app.js` vai ouvir esse evento para mostrar ou esconder os botões de editar e excluir, sem que os dois arquivos precisem se conhecer.

> **⚠️ Atenção**
> Guardamos o token no `sessionStorage` porque é simples e some ao fechar a aba. Saiba o que isso custa: qualquer JavaScript que rode na sua página — inclusive um script de terceiro comprometido — consegue ler `sessionStorage` e roubar a sessão. Isso se chama XSS. A defesa profissional é entregar a sessão em um **cookie `httpOnly`**, que o JavaScript não enxerga e o navegador envia sozinho. Não é mais difícil, é só mais assunto do que cabe hoje — e é o desafio ⭐⭐⭐ desta aula.

### Passo 8 — Provando que a proteção funciona

Acrescente ao `testes.http` os blocos de autenticação. O `@token` você preenche daqui a pouco:

`cafe-cerrado-api/testes.http` (acrescente ao final)

```http
@token = cole-aqui-o-token-copiado-do-navegador

### 14. Configuração pública (200, com o Client ID)
GET {{base}}/config

### 15. Quem sou eu, sem token (401)
GET {{base}}/auth/eu

### 16. Login com token falso (401, e não 500)
POST {{base}}/auth/google
Content-Type: application/json

{
  "credential": "isto.nao.e-um-token"
}

### 17. Criar produto SEM token (401) — a proteção do dia
POST {{base}}/produtos
Content-Type: application/json

{
  "nome": "Café gelado da casa",
  "categoria": "bebidas-geladas",
  "preco": 14.0
}

### 18. Listar SEM token (200) — leitura continua pública
GET {{base}}/produtos

### 19. Quem sou eu, com token (200, com e-mail e nome)
GET {{base}}/auth/eu
Authorization: Bearer {{token}}

### 20. Criar produto COM token (201)
POST {{base}}/produtos
Content-Type: application/json
Authorization: Bearer {{token}}

{
  "nome": "Café gelado da casa",
  "categoria": "bebidas-geladas",
  "preco": 14.0
}

### 21. Excluir COM token (204)
DELETE {{base}}/produtos/6
Authorization: Bearer {{token}}
```

### Como testar

Suba o servidor com `npm run dev` e siga o roteiro:

1. Abra `http://localhost:3000`. O botão "Fazer login com o Google" aparece no cabeçalho. Se não aparecer, abra o console: a mensagem de erro do GSI diz exatamente o que falta.
2. Clique, escolha a sua conta. Nome e foto substituem o botão. No terminal do servidor, o log mostra `POST /api/auth/google -> 200`.
3. No console do navegador, execute `JSON.parse(sessionStorage.getItem('cafe-cerrado-sessao')).token` e copie o valor (sem as aspas). Cole na variável `@token` do `testes.http`.
4. Rode os blocos 14 a 21 na ordem. Os status esperados:

| Blocos | Status | O que prova |
|---|---|---|
| 14 e 18 | `200` | Configuração e leitura continuam públicas |
| 15, 16 e 17 | `401` | Sem identidade não se lê `/auth/eu` nem se escreve |
| 19, 20 e 21 | `200`, `201`, `204` | Com a sessão válida, tudo funciona |

5. Prova final da assinatura: no bloco 19, **troque um caractere** do token colado e envie de novo. A resposta tem que ser `401`. Um único byte diferente destrói a assinatura — é isso que impede alguém de editar os próprios dados de sessão.
6. Clique em "Sair" no site e recarregue a página: o botão do Google volta, porque o `sessionStorage` foi limpo.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Classifique cada situação como `401` ou `403`, com uma linha de justificativa:

- (a) Requisição sem cabeçalho `Authorization`.
- (b) Token de sessão expirado há dois minutos.
- (c) Usuário logado tentando excluir um produto cadastrado por outra pessoa.
- (d) Token com a assinatura adulterada.

**A2.** Um colega diz: "decodifiquei o JWT com `atob` e vi que o e-mail é `professor@unemat.br`, então o usuário é o professor". Explique em três linhas por que a conclusão está errada e o que faltou fazer.

**A3.** Preveja a resposta de cada requisição **sem rodar**, e depois confira:

```bash
curl -i http://localhost:3000/api/produtos
curl -i -X DELETE http://localhost:3000/api/produtos/1
curl -i -H "Authorization: Bearer qualquer-coisa" http://localhost:3000/api/auth/eu
curl -i -H "Authorization: Basic YWJjOjEyMw==" http://localhost:3000/api/auth/eu
```

**A4.** No `authController.js`, remova mentalmente a linha `audience: process.env.GOOGLE_CLIENT_ID`. A verificação da assinatura continua funcionando? Que ataque passa a ser possível? Responda em três linhas.

**A5.** O que acontece se `require('dotenv').config()` for movido para **depois** de `const authRouter = require('./routes/auth')` no `server.js`? Descreva a mensagem de erro que o usuário veria ao tentar entrar e explique a causa.

**A6.** Em `exigirLogin`, alguém trocou `return res.status(401).json(...)` por `res.status(401).json(...)`, sem o `return`. Descreva o que acontece com uma requisição sem token — e por que o erro que aparece no terminal fala em cabeçalhos.

### Nível B — Aplicação

**B1.** Login no seu projeto autoral. Configure o Google Cloud Console para o seu projeto e implemente o fluxo completo: botão, `POST /api/auth/google`, sessão assinada e exibição do nome e da foto no cabeçalho.

Resultado esperado: entrar mostra nome e foto; recarregar a página mantém a sessão; "Sair" limpa tudo e traz o botão de volta.

<details markdown="1">
<summary>Dica</summary>

Crie um Client ID **novo** para o seu projeto, com o nome dele — não reaproveite o do Café Cerrado. Se a porta do seu servidor não for 3000, é essa porta que precisa estar em "Origens JavaScript autorizadas".
</details>

**B2.** Proteja as escritas. Aplique o `exigirLogin` nas rotas `POST`, `PUT` e `DELETE` do seu recurso principal, mantendo os `GET` públicos, e prove a proteção com quatro blocos no `testes.http`.

Resultado esperado: escrita sem token devolve `401` com mensagem em JSON; leitura sem token devolve `200`; escrita com token funciona normalmente.

<details markdown="1">
<summary>Dica</summary>

O middleware entra entre o caminho e o controlador: `router.post('/', exigirLogin, controlador.criar)`. Se todas as rotas do arquivo precisassem de login, uma linha `router.use(exigirLogin)` no topo resolveria de uma vez.
</details>

**B3.** Registre quem fez o quê. Faça o middleware de log incluir o e-mail do usuário quando houver sessão, produzindo linhas como `POST /api/produtos -> 201 (12 ms) por maria@gmail.com`.

Resultado esperado: requisições anônimas continuam sendo registradas normalmente, sem quebrar; requisições autenticadas mostram o e-mail.

<details markdown="1">
<summary>Dica</summary>

O log roda **antes** do `exigirLogin`, então `req.usuario` ainda não existe quando a linha é montada — mas o callback de `res.on('finish', ...)` executa **depois** de tudo. Leia `req.usuario` lá dentro, com `?.` para o caso anônimo.
</details>

**B4.** Diagnóstico honesto. Escreva no `README.md` uma seção "Segurança" com três parágrafos: onde o token de sessão é guardado no navegador, qual o risco dessa escolha, e o que você faria diferente em um sistema com dados sensíveis.

Resultado esperado: o texto cita XSS pelo nome, explica o que um cookie `httpOnly` mudaria e não promete segurança que o projeto não tem.

<details markdown="1">
<summary>Dica</summary>

Um bom parágrafo de risco responde três perguntas: o que um atacante precisaria conseguir, o que ele obteria, e por quanto tempo o estrago dura. A duração está no `DURACAO_MS` do `sessao.js`.
</details>

### Nível C — Desafio em sala

**C1.** Sessão que expira na cara do usuário. Reduza `DURACAO_MS` para 60 segundos e observe o desastre: passado um minuto, cada tentativa de escrita devolve `401` e o site continua exibindo alegremente o nome e a foto do usuário, como se nada tivesse acontecido. Conserte o comportamento nas duas pontas.

O servidor precisa dizer **por que** negou, de forma que o front distinga "nunca entrou" de "a sessão venceu"; e o front precisa reagir a um `401` limpando a sessão, voltando o botão de login e avisando a pessoa — sem que cada chamada `fetch` do projeto precise repetir esse tratamento.

Resultado esperado: com a duração em 60 segundos, esperar um minuto e tentar criar um produto faz o site voltar sozinho ao estado deslogado, com a mensagem "Sua sessão expirou. Entre novamente."; o console não mostra nenhum erro não tratado; e no fim você devolve `DURACAO_MS` para 8 horas.

<details markdown="1">
<summary>Dica</summary>

No servidor, devolva um campo a mais junto do erro (por exemplo `codigo: 'sessao_expirada'` × `codigo: 'sem_token'`) — isso exige separar os dois casos no `lerToken`, hoje unificados em `null`. No front, escreva uma função `requisitar(url, opcoes)` que envolve o `fetch`, adiciona o `Authorization` quando há token e trata o `401` em um lugar só; é a mesma camada que a Aula 15 vai usar para todo o CRUD. A função `sair()` já faz tudo que o tratamento precisa.
</details>

## 🏆 Desafios

### ⭐ O botão que não quer aparecer
Tags: oauth, autenticacao, devtools, bug

Abra o site do Café Cerrado pelo Live Server do VS Code, em `http://127.0.0.1:5500`, em vez de pelo seu servidor Express. O botão do Google some, e o console solta uma mensagem que menciona `origin`. Antes de consertar, entenda: o erro não veio do seu código nem do seu servidor — veio do Google, sobre uma decisão que **você** configurou. Reproduza três variações do problema, explique o que cada uma revela sobre o conceito de origem e deixe o projeto documentado para que ninguém da sua equipe caia nisso.

**Critérios de pronto**

- Um arquivo `docs/origens.md` registra, para cada uma das três variações (porta diferente, `127.0.0.1` no lugar de `localhost`, e `https` no lugar de `http`), a mensagem exata do console e uma linha explicando por que o Google recusou.
- Uma frase define "origem" em termos de protocolo, host e porta, com um exemplo de duas URLs que parecem iguais e são origens diferentes.
- O `README.md` ganha um aviso de uma linha dizendo por qual endereço o site deve ser aberto e por quê.
- O botão volta a funcionar no endereço correto, sem que você tenha cadastrado todas as origens possíveis no console do Google.

<details markdown="1">
<summary>Pistas</summary>

1. Copie a mensagem inteira do console, incluindo o prefixo `[GSI_LOGGER]`, e procure por ela na documentação do Google Identity Services.
2. A configuração relevante está em "Origens JavaScript autorizadas", na credencial que você criou. Ela aceita várias entradas — mas cadastrar tudo não é a resposta, é a preguiça.
3. Para a variação com `https`, lembre-se de que `localhost` é tratado como origem segura mesmo sem certificado; teste e explique o que acontece.
4. Vale investigar também o que muda se você abrir o arquivo com duplo clique (`file://`). O que o console diz sobre a origem nesse caso?
</details>

### ⭐⭐ Só quem é da casa entra
Tags: autenticacao, seguranca, express, middleware

Hoje qualquer pessoa com uma conta Google — o planeta inteiro — vira um usuário capaz de mexer no cardápio do Café Cerrado. Isso está certo para um blog e errado para um sistema interno. Implemente autorização de verdade: a API passa a ter uma lista de e-mails autorizados a escrever, e quem está autenticado mas fora da lista recebe `403`, com uma mensagem que explique a diferença.

**Critérios de pronto**

- Um middleware `exigirPermissao` roda **depois** de `exigirLogin` e devolve `403` com `{ "erro": "..." }` para e-mails fora da lista.
- A lista vem do `.env` (por exemplo `EMAILS_AUTORIZADOS=a@x.com,b@y.com`), nunca do código, e o `.env.exemplo` documenta o formato.
- `GET` continua público, escrita sem token continua `401` e escrita com token não autorizado devolve `403` — os três casos provados no `testes.http`.
- `GET /api/auth/eu` passa a devolver um campo booleano dizendo se aquele usuário pode escrever, para o front decidir o que mostrar.
- Um parágrafo no `README.md` explica, com as suas palavras, por que `401` e `403` não são intercambiáveis.

<details markdown="1">
<summary>Pistas</summary>

1. `process.env.EMAILS_AUTORIZADOS.split(',').map((e) => e.trim().toLowerCase())` transforma a variável em lista utilizável.
2. Compare sempre em minúsculas: o Google devolve o e-mail como cadastrado, e a sua lista foi digitada à mão.
3. A ordem na rota importa: `router.post('/', exigirLogin, exigirPermissao, controlador.criar)`. Inverter os dois faz o `exigirPermissao` ler um `req.usuario` que ainda não existe.
4. Pense no caso da lista vazia ou ausente: liberar todo mundo ou bloquear todo mundo? Escolha, justifique no README e implemente a escolha explicitamente — comportamento de segurança nunca deve ser acidente.
</details>

### ⭐⭐ Quanto tempo dura a sua identidade
Tags: autenticacao, oauth, investigacao, http

O ID token do Google e o token de sessão que você emitiu têm prazos de validade diferentes, definidos por gente diferente, por motivos diferentes. Poucos desenvolvedores sabem dizer quais são. Descubra os dois experimentalmente, documente e depois tome uma decisão de projeto informada sobre a duração da **sua** sessão.

**Critérios de pronto**

- Um arquivo `docs/validade-dos-tokens.md` mostra as claims `iat` e `exp` de um ID token real (obtidas decodificando o token no console) convertidas para horário legível, com a duração calculada em minutos.
- O mesmo documento registra a duração da sessão emitida pela sua API e como você a mediu, sem confiar apenas no valor da constante.
- Uma tabela de três linhas compara os dois tokens: quem emite, quanto dura, o que acontece quando vence.
- Um parágrafo justifica a duração escolhida para a sessão do seu projeto, considerando que ela é usada em um laboratório da universidade com computadores compartilhados.
- A constante `DURACAO_MS` passa a ser lida do `.env`, com um padrão sensato quando a variável não existir.

<details markdown="1">
<summary>Pistas</summary>

1. `JSON.parse(atob(token.split('.')[1]))` no console devolve as claims do ID token. `iat` e `exp` estão em **segundos** desde 1970 — multiplique por 1000 antes de passar para `new Date()`.
2. Para medir a sessão sem confiar na constante, decodifique o corpo do seu próprio token com `Buffer.from(corpo, 'base64url')` em um script Node e olhe o `expiraEm`.
3. Um valor vindo do `.env` chega como string: `Number(process.env.SESSAO_HORAS) || 8` resolve conversão e padrão de uma vez.
4. Para o parágrafo final, pense no cenário concreto: alguém entra no seu sistema no laboratório, esquece de sair e vai embora. Quanto tempo a sessão continua aberta?
</details>

### ⭐⭐⭐ Tirando o token das mãos do JavaScript
Tags: seguranca, autenticacao, express, http

Se um único script malicioso rodar na sua página, ele lê o `sessionStorage` e leva a sessão embora. É assim que contas são roubadas de verdade. A defesa padrão da indústria é entregar a sessão em um cookie `httpOnly`: o navegador guarda, envia sozinho em cada requisição e **não** deixa o JavaScript ler. Migre o Café Cerrado para esse modelo e prove, com o DevTools, que o token sumiu do alcance do JavaScript.

**Critérios de pronto**

- `POST /api/auth/google` passa a responder com `Set-Cookie` contendo o token de sessão, com os atributos `HttpOnly`, `SameSite=Lax`, `Path=/` e `Max-Age` coerente com a duração da sessão. O corpo da resposta traz só os dados do usuário.
- `exigirLogin` aceita a sessão vinda do cookie; o front não guarda mais token nenhum no `sessionStorage`.
- Existe `POST /api/auth/sair`, que apaga o cookie, e o botão "Sair" passa a chamá-lo.
- No console do navegador, `document.cookie` **não** mostra o token, enquanto a aba Application do DevTools mostra o cookie presente — com prova em duas capturas de tela no `docs/`.
- O `README.md` explica em um parágrafo o que `SameSite` faz e por que ele importa aqui, citando o ataque que esse atributo previne.

<details markdown="1">
<summary>Pistas</summary>

1. Enviar é fácil: `res.cookie('sessao', token, { httpOnly: true, sameSite: 'lax', maxAge: DURACAO_MS, path: '/' })` já vem no Express. Ler exige interpretar `req.headers.cookie`, que é uma string única com pares separados por `;` — escreva uma função de dez linhas ou instale `cookie-parser`.
2. Faça o `exigirLogin` aceitar as duas origens durante a migração (cabeçalho `Authorization` **ou** cookie) e só depois remova a antiga. Migração em dois passos evita ficar sem login no meio do caminho.
3. Para apagar um cookie, envie-o de novo com validade no passado: `res.clearCookie('sessao', { path: '/' })`. O `path` precisa bater com o do cookie original, ou o navegador ignora.
4. Cookies criam uma porta nova para um ataque chamado CSRF, porque o navegador passa a enviar a credencial sozinho — inclusive em requisições disparadas por outro site. Leia sobre `SameSite` na MDN antes de escrever o parágrafo do README; é ele que fecha essa porta no nosso caso.
</details>

## 🐛 Erros comuns e como resolver

| Sintoma | Causa | Solução |
|---|---|---|
| `[GSI_LOGGER]: The given origin is not allowed for the given client ID` | A página foi aberta em uma origem não cadastrada (Live Server, `127.0.0.1`, outra porta) | Abrir o site pelo Express em `http://localhost:3000`, a origem cadastrada no console |
| `TypeError: Cannot read properties of undefined (reading 'accounts')` | O `auth.js` rodou antes do script `gsi/client` terminar de carregar | Iniciar por `window.onGoogleLibraryLoad`, com a checagem prévia de `window.google` |
| `Error: Wrong recipient, payload audience != requiredAudience` | O Client ID do front é diferente do `GOOGLE_CLIENT_ID` do `.env` | Servir o Client ID ao front por `GET /api/config` para existir um valor só |
| `Token used too late` na verificação | ID token expirado (mais de 1 h) ou relógio do computador fora de hora | Fazer login de novo; conferir o horário automático do sistema operacional |
| `SESSAO_SEGREDO não definido` ao subir o servidor | `.env` ausente, ou `require('dotenv').config()` fora da primeira linha | Copiar `.env.exemplo` para `.env` e carregar o dotenv antes de qualquer outro require |
| `POST /api/produtos` devolve `401` mesmo logado | O `fetch` não enviou o cabeçalho `Authorization` | Conferir na aba Network se o cabeçalho está na requisição, e o `Bearer ` com espaço |
| `Cannot set headers after they are sent to the client` | Faltou `return` antes de um `res.status(401).json(...)` no middleware | Todo caminho que responde no middleware termina com `return` ou com `next()` |
| Login funciona, mas `GET /api/auth/eu` devolve `401` | Token colado no `testes.http` com aspas, espaços ou quebra de linha | Copiar apenas o conteúdo do token, sem aspas, em uma única linha |
| `SyntaxError: Unexpected token '<'` ao ler `/api/config` | A rota não existe e o Express devolveu HTML, que o `fetch` tentou ler como JSON | Registrar `app.get('/api/config', ...)` antes do 404 de API e conferir o caminho |
| O `.env` aparece no `git status` | O `.gitignore` foi criado depois do primeiro `git add` do arquivo | `git rm --cached .env`, ajustar o `.gitignore` e **trocar** o segredo, que já foi exposto |

## 🏠 Atividade assíncrona (1 h)

No **seu projeto autoral**:

1. Crie o projeto no Google Cloud Console, obtenha o Client ID e configure `.env` (no `.gitignore`) e `.env.exemplo` (versionado).
2. Implemente `POST /api/auth/google` verificando o ID token com `google-auth-library`, com `audience` preenchido.
3. Emita um token de sessão assinado pela sua aplicação e devolva-o junto com nome, e-mail e foto.
4. Adicione o botão do Google no cabeçalho do site, com a área de usuário (nome, foto, botão Sair) e a mensagem de status acessível.
5. Proteja `POST`, `PUT` e `DELETE` com o `exigirLogin`, mantendo os `GET` públicos.
6. Registre no `testes.http` os quatro cenários: leitura sem token (`200`), escrita sem token (`401`), login com token falso (`401`) e escrita com token válido (`201`).

**Critério de pronto:** o `git status` não mostra o `.env` em momento algum; um visitante anônimo consegue ler o conteúdo; e nenhuma operação de escrita funciona sem um token de sessão válido — verificado pelo `curl`, não pela interface.

**Entrega:** commit + push e link do repositório no SIGAA.

## ✅ Checkpoint do projeto

- [ ] Client ID criado no Google Cloud Console, com `http://localhost:3000` nas origens autorizadas.
- [ ] `.env` no `.gitignore` e `.env.exemplo` versionado com as chaves necessárias.
- [ ] `require('dotenv').config()` na primeira linha do `server.js`, com checagem das variáveis obrigatórias.
- [ ] `POST /api/auth/google` verificando assinatura, emissor, validade e `audience` do ID token.
- [ ] Token de sessão próprio, assinado com HMAC e com prazo de validade.
- [ ] Middleware `exigirLogin` devolvendo `401` em JSON e preenchendo `req.usuario`.
- [ ] `POST`, `PUT` e `DELETE` protegidos; `GET` públicos.
- [ ] Botão do Google renderizado por `google.accounts.id.renderButton`, com nome e foto após o login e botão "Sair" funcionando.
- [ ] `testes.http` com os cenários de `401` e de sucesso.

## 📚 Para aprofundar

- [Google Identity — Sign In With Google (JavaScript API)](https://developers.google.com/identity/gsi/web/reference/js-reference) — a referência de `initialize`, `renderButton` e `disableAutoSelect`.
- [Google Identity — Verificar o ID token no servidor](https://developers.google.com/identity/gsi/web/guides/verify-google-id-token) — por que verificar `aud` e `iss`, com exemplos oficiais.
- [MDN — Autenticação HTTP](https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Authentication) — o esquema `Bearer` e os status `401` e `403`.
- [MDN — `Set-Cookie` e o atributo `SameSite`](https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Headers/Set-Cookie) — leitura obrigatória antes do desafio ⭐⭐⭐.
- [RFC 7519 — JSON Web Token](https://datatracker.ietf.org/doc/html/rfc7519) — leia só as seções 3 e 4, sobre a estrutura e as claims registradas.
- [RFC 6749 — OAuth 2.0](https://datatracker.ietf.org/doc/html/rfc6749) — a seção 1 explica os papéis do protocolo em duas páginas.
- [Node.js — `crypto.createHmac` e `crypto.timingSafeEqual`](https://nodejs.org/api/crypto.html) — as duas funções que sustentam a sessão desta aula.
- QUEIRÓS, Ricardo; PORTELA, Filipe. *Introdução ao Desenvolvimento Moderno para a Web*. FCA, 2018 — segurança e autenticação em aplicações web.
- LOUDON, Kyle. *Desenvolvimento de Grandes Aplicações Web*. Novatec, 2019 — segurança em aplicações de grande porte.

A API sabe quem você é e o site sabe mostrar o seu nome — mas ainda não existe uma tela para cadastrar um produto. Na próxima aula, o front-end assíncrono da Unidade 2 finalmente encontra a API da Unidade 3: formulário que serve para criar e editar, exclusão com confirmação, feedback acessível e lista que se atualiza sem recarregar a página, tudo enviando o token que você emitiu hoje.
