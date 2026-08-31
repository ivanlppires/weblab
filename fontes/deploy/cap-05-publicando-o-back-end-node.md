# Capítulo 05 — Publicando o back-end Node

> **Deploy & Ferramentas** · Unidade 2: Publicação: estático, back-end, domínio e servidor
> WebLab · UNEMAT Sinop · Prof. Ivan Luiz Pedroso Pires
> **Carga:** capítulo de estudo autônomo · use em paralelo à sua trilha

## 🎯 Objetivos de aprendizagem

Ao final deste capítulo você será capaz de:

- Explicar a diferença entre hospedagem estática e servidor de aplicação, e por que um processo Node precisa de outra categoria de hospedagem.
- Comparar PaaS, VPS, contêiner gerenciado e funções serverless, escolhendo com critério onde publicar uma API.
- Preparar uma API Express 5 para produção: porta vinda do ambiente, escuta em `0.0.0.0`, `npm ci`, campo `engines`, script `start` e encerramento gracioso no `SIGTERM`.
- Separar configuração de código com variáveis de ambiente, manter o `.env` fora do Git, publicar um `.env.example` e falhar na subida quando faltar um segredo.
- Publicar a `cafe-cerrado-api` no Render a partir do GitHub, com deploy automático a cada `push`, health check e logs.
- Escrever uma rota de health check honesta e ler os logs de um serviço para diagnosticar uma queda.
- Configurar CORS liberando exatamente a origem do front publicado — e explicar por que `origin: '*'` não é a resposta.
- Reconhecer os limites do plano gratuito: *cold start*, disco efêmero, região distante e cota de horas.

## 📋 Pré-requisitos

- [ ] `cafe-cerrado-api` (Nível 2, Unidade 3) rodando na sua máquina: `npm start` sobe o Express 5 e `curl http://localhost:3000/api/produtos` devolve a lista do cardápio.
- [ ] Repositório da API no GitHub (Capítulo 02), com o `package-lock.json` versionado e o `node_modules/` no `.gitignore`.
- [ ] Café Cerrado estático publicado no Capítulo 03 (Netlify, Vercel ou GitHub Pages) — é ele que vai consumir a API.
- [ ] Node 22 LTS (`node -v`) e `curl` (`curl --version`) na sua máquina.
- [ ] Uma conta no Render (<https://render.com>), criada com o login do GitHub.
- [ ] Opcional: o domínio do Capítulo 04, para dar um nome decente à API.

> Nos Capítulos 03 e 04 você publicou **arquivos**: HTML, CSS, JS e imagens que uma CDN entrega sem executar nada, com domínio próprio e HTTPS. Hoje o que vai ao ar é diferente — um **processo** que precisa estar vivo, ouvindo uma porta, com memória, segredos e um banco (ou um JSON) por baixo. Você vai colocar a `cafe-cerrado-api` no Render, ligar o front publicado a ela e descobrir, na prática, o que o plano gratuito cobra em troca.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 45 min | Estático × servidor; onde um processo Node pode morar; como uma PaaS constrói e roda o código (§1 a §3) |
| 2 | 50 min | Preparar a API: porta, host, scripts, variáveis de ambiente, health check, logs e CORS (§4 a §8) |
| 3 | 55 min | Passo a passo: `cafe-cerrado-api` no Render com o front consumindo a URL pública + Laboratório |

## 1. Estático × servidor: o que realmente muda

### 1.1 O que uma hospedagem estática faz

No Capítulo 03 você entregou uma pasta. O GitHub Pages e a Netlify copiaram esses arquivos para servidores espalhados pelo mundo e, quando alguém pede `/cardapio.html`, devolvem o arquivo. Não há código seu rodando do lado do servidor. Isso explica tudo o que era fácil ali: escala infinita (é só cache), custo zero, nada para reiniciar, nada para monitorar.

### 1.2 O que um servidor de aplicação faz

A `cafe-cerrado-api` é outra coisa. Ela é um **processo do sistema operacional** que:

1. sobe, lê a configuração e abre uma porta TCP;
2. fica parado esperando conexões, para sempre;
3. a cada requisição, executa o seu código: lê o `dados/produtos.json`, valida um ID token do Google, grava uma alteração, monta uma resposta JSON;
4. guarda coisas em memória enquanto está vivo;
5. morre se você derrubar, se a máquina reiniciar, se uma exceção não tratada escapar — e alguém precisa trazê-lo de volta.

O resumo em uma tabela:

| Aspecto | Site estático | API Node |
|---|---|---|
| O que é publicado | arquivos | um processo em execução |
| Quem executa código | só o navegador | o servidor **e** o navegador |
| Se cair | não cai (é só arquivo em cache) | precisa de alguém que reinicie |
| Segredos | não pode ter nenhum | vivem no ambiente do processo |

### 1.3 As quatro consequências práticas

**O processo precisa de um supervisor.** Alguém tem que reiniciá-lo quando ele morre e quando a máquina liga. Numa PaaS isso é automático; num VPS é o pm2 ou o systemd (Capítulo 06).

**A porta não é sua escolha.** Na sua máquina você fixa `3000`. Em produção, quem manda é a plataforma: ela reserva uma porta, escreve o número na variável de ambiente `PORT` e espera que o seu processo escute exatamente ali. Ignorar isso é o erro nº 1 do primeiro deploy.

**O disco é descartável.** Em quase toda PaaS, o sistema de arquivos do serviço é **efêmero**: some a cada novo deploy e a cada reinício. Se a `cafe-cerrado-api` grava produtos no `dados/produtos.json`, tudo o que os visitantes criarem desaparece no próximo `git push`. Isso não é bug, é o modelo — e é exatamente por isso que existe o Capítulo 08, quando o estado sai para um banco de verdade.

**Configuração não é código.** URL do banco, client ID do Google, origem liberada no CORS: nada disso pode estar dentro do repositório, porque muda de ambiente para ambiente e porque parte é segredo (§5).

> **🧠 Você sabia?**
> A ideia de "configuração no ambiente" foi popularizada em 2011 pelo manifesto **The Twelve-Factor App**, escrito por engenheiros da Heroku — a primeira PaaS a fazer `git push heroku main` virar um deploy. Doze regras curtas sobre como escrever software que sobe em qualquer lugar; o fator III, *Config*, é literalmente "guarde configuração no ambiente". Praticamente toda plataforma moderna (Render, Railway, Fly.io, Vercel, Cloud Run) implementa aquele contrato: você entrega um repositório, a plataforma injeta variáveis de ambiente e uma `PORT`, e espera um processo que escute nela.

## 2. Onde um processo Node pode morar

Quatro modelos, do mais gerenciado ao mais manual:

| Modelo | Você entrega | Você administra |
|---|---|---|
| **PaaS** (Render, Railway, Fly.io) | um repositório Git | só o código e as variáveis |
| **Contêiner gerenciado** (Cloud Run, ECS) | uma imagem Docker | a imagem (Capítulo 07) |
| **VPS** (Contabo, Hetzner, DigitalOcean) | acesso SSH | tudo: SO, Node, nginx, TLS (Capítulo 06) |
| **Serverless / funções** (Vercel, Netlify, Workers) | funções isoladas | nada — mas o modelo muda |

Neste capítulo você usa o primeiro modelo, porque ele é o caminho mais curto entre "funciona na minha máquina" e "está na internet". Os outros vêm nos capítulos seguintes, e no fim do semestre você terá visto os quatro para poder escolher com critério.

### 2.1 Render — o principal deste capítulo

O **Render** (<https://render.com>) conecta ao seu repositório do GitHub, roda um comando de build, roda um comando de start e coloca o processo atrás de um domínio `https://<nome>.onrender.com` com certificado automático. A cada `push` na branch escolhida, ele repete tudo.

O que o plano gratuito dá — e o que cobra em troca:

- Domínio `.onrender.com` com HTTPS, e também **domínio próprio** com certificado emitido pela plataforma.
- Deploy automático a cada `push`, com histórico e botão de *rollback* para a versão anterior.
- Logs em tempo real no painel.
- **Cold start:** um serviço gratuito é desligado depois de cerca de 15 minutos sem receber requisição. A próxima requisição acorda o processo — e espera. Podem ser 30, 50 segundos ou mais. O visitante vê a página girando.
- **Disco efêmero:** sem disco persistente no plano gratuito. Tudo o que o processo grava some no próximo deploy ou reinício.
- **Cota de horas** de execução por mês na conta inteira, e um limite de banda. Confira os números atuais na página de preços antes de publicar cinco serviços.
- **Região:** as regiões ficam nos EUA, Europa e Ásia. De Sinop, cada requisição atravessa o continente. Para um trabalho de faculdade, tudo bem; para um cliente, isso pesa.

### 2.2 Railway — resumo

O **Railway** (<https://railway.com>) tem a melhor experiência de uso do trio: detecta o projeto, sobe banco de dados com dois cliques e mostra tudo num diagrama. Ele **não** tem plano gratuito permanente — dá um crédito de teste e depois cobra por uso (CPU, memória e banda medidos por segundo). O fluxo pela linha de comando:

```bash
npm install -g @railway/cli
railway login
railway init
railway up
railway variables
railway logs
```

Use-o quando quiser um banco gerenciado junto da aplicação sem configurar nada — e quando o cartão puder entrar na história.

### 2.3 Fly.io — resumo

O **Fly.io** (<https://fly.io>) roda a sua aplicação como microVM perto do usuário, e tem região em **São Paulo** (`gru`) — a menor latência para o Brasil entre as três. Ele empacota o projeto em uma imagem (o `fly launch` gera um `Dockerfile` se você não tiver um), então casa naturalmente com o Capítulo 07. Também é pago por uso, com valores baixos para um projeto pequeno.

```bash
curl -L https://fly.io/install.sh | sh
fly auth login
fly launch --region gru
fly secrets set GOOGLE_CLIENT_ID=seu-client-id CORS_ORIGENS=https://cafe.seudominio.dev
fly deploy
fly logs
fly status
```

A configuração fica em `fly.toml`, versionado no repositório. Com `auto_stop_machines`, a máquina dorme quando não há tráfego — o mesmo *cold start* do Render, mas medido em milissegundos porque a microVM sobe muito mais rápido que um contêiner clássico.

> **💡 Dica**
> Escolha uma plataforma e vá fundo nela neste semestre. Testar as três ao mesmo tempo dá a sensação de produtividade e o conhecimento de nenhuma. O que você aprende aqui — porta pelo ambiente, segredos fora do Git, health check, logs, CORS — vale igual nas três e no VPS.

## 3. Como uma PaaS constrói e roda o seu código

Todo deploy numa PaaS tem as mesmas cinco etapas. Entender cada uma é o que separa "não sei por que não subiu" de "sei exatamente qual etapa falhou":

1. **Clone.** A plataforma baixa a branch configurada do seu repositório. Só o que está commitado existe — se funciona na sua máquina por causa de um arquivo não versionado, vai falhar aqui.
2. **Build.** Roda o *build command*. Para uma API Node, quase sempre `npm ci`. Para um front com Vite, `npm ci && npm run build`.
3. **Start.** Roda o *start command* (`npm start`) e injeta as variáveis de ambiente, incluindo a `PORT`.
4. **Health check.** A plataforma faz requisições ao caminho que você indicou. Enquanto não receber `200`, considera que a versão nova não subiu — e mantém a antiga no ar.
5. **Troca de tráfego.** Deu certo, o roteador passa a mandar as requisições para a instância nova e derruba a velha. Deu errado, a versão anterior continua servindo e o deploy é marcado como falho.

Um detalhe que economiza horas: a etapa 2 roda com as `devDependencies` disponíveis, mas a etapa 3 roda **só o que está no repositório mais o que o build instalou**. Se você importa um pacote que só está em `devDependencies`, o build passa e o start quebra com `Cannot find module`.

> **🔎 Por baixo do capô**
> Como a plataforma sabe que o seu processo subiu? Ela não lê o seu `console.log`. Ela abre uma conexão TCP na porta que reservou. Se o processo escutar em `127.0.0.1`, ele aceita conexões **apenas de dentro do próprio contêiner** — e a plataforma, que está fora, recebe "conexão recusada". O sintoma no painel é uma mensagem de *port scan timeout*: "no open ports detected". A correção é escutar em `0.0.0.0`, o endereço curinga que significa "todas as interfaces de rede desta máquina" (§4.2).

## 4. Preparando a API para produção

Cinco mudanças pequenas no código, todas no repositório da `cafe-cerrado-api`.

### 4.1 A porta vem do ambiente

Nunca escreva `3000` no `listen`. Leia da variável `PORT` e use `3000` só como valor de reserva para a sua máquina:

`src/config.js`

```js
// src/config.js — lê e valida tudo o que vem do ambiente.
// Se faltar algo obrigatório, o processo morre AQUI, com mensagem clara,
// em vez de quebrar três dias depois numa requisição qualquer.

const ambiente = process.env.NODE_ENV ?? 'development';
const producao = ambiente === 'production';

function texto(nome, padrao) {
  const valor = process.env[nome] ?? padrao;
  if (valor === undefined || valor === '') {
    throw new Error(`Configuração ausente: defina ${nome} no ambiente (ou no .env).`);
  }
  return valor;
}

function numero(nome, padrao) {
  const valor = Number(texto(nome, padrao));
  if (!Number.isInteger(valor) || valor <= 0) {
    throw new Error(`Configuração inválida: ${nome} precisa ser um inteiro positivo.`);
  }
  return valor;
}

function lista(nome, padrao) {
  return texto(nome, padrao)
    .split(',')
    .map((item) => item.trim())
    .filter((item) => item.length > 0);
}

export const config = {
  ambiente,
  producao,
  porta: numero('PORT', '3000'),
  host: texto('HOST', '0.0.0.0'),
  origensPermitidas: lista('CORS_ORIGENS', 'http://localhost:5500,http://127.0.0.1:5500'),
  // Em produção não há padrão: sem client ID, o processo nem sobe.
  googleClientId: texto('GOOGLE_CLIENT_ID', producao ? undefined : 'client-id-de-desenvolvimento'),
};
```

### 4.2 Escutar em `0.0.0.0` e encerrar com educação

`src/server.js`

```js
// src/server.js — o único arquivo que sobe o servidor.
// Separar 'app' de 'server' permite importar o app nos testes sem abrir porta.
import { app } from './app.js';
import { config } from './config.js';

const servidor = app.listen(config.porta, config.host, () => {
  console.log(`[cafe-cerrado-api] no ar em ${config.host}:${config.porta} (${config.ambiente})`);
});

function encerrar(sinal) {
  console.log(`[cafe-cerrado-api] recebi ${sinal}: parando de aceitar conexões novas.`);
  servidor.close(() => {
    console.log('[cafe-cerrado-api] tudo fechado. Até logo.');
    process.exit(0);
  });
  // Se alguma conexão travar, saia à força depois de 10 s em vez de ficar pendurado.
  setTimeout(() => {
    console.error('[cafe-cerrado-api] demorou demais para encerrar; saindo à força.');
    process.exit(1);
  }, 10_000).unref();
}

process.on('SIGTERM', () => encerrar('SIGTERM'));
process.on('SIGINT', () => encerrar('SIGINT'));
```

Por que tratar `SIGTERM`? Porque é assim que toda plataforma pede que o processo saia: manda `SIGTERM`, espera alguns segundos e, se ele insistir em viver, manda `SIGKILL`. Tratando o sinal, você termina as requisições em andamento antes de sair. Sem tratar, quem estava recebendo uma resposta leva um erro de conexão a cada deploy.

### 4.3 `package.json`: o contrato com a plataforma

`package.json`

```json
{
  "name": "cafe-cerrado-api",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "engines": {
    "node": ">=22.0.0"
  },
  "scripts": {
    "start": "node src/server.js",
    "dev": "node --watch --env-file=.env src/server.js",
    "teste": "node --test"
  },
  "dependencies": {
    "cors": "^2.8.5",
    "express": "^5.1.0",
    "google-auth-library": "^9.15.0"
  }
}
```

Quatro campos que a plataforma lê:

- `"type": "module"` — habilita `import`/`export` sem extensão `.mjs`. Se o seu projeto ainda usa `require`, mantenha o `type` fora e nada muda.
- `"engines"` — declara a versão do Node. O Render, o Railway e o Fly.io respeitam esse campo. Sem ele, você pode receber uma versão diferente da sua e descobrir a diferença do jeito ruim.
- `"scripts.start"` — o comando que a plataforma executa. Nunca coloque `nodemon` ou `--watch` aqui: em produção, o processo tem que ser um só.
- `"dependencies"` × `"devDependencies"` — o que a aplicação precisa **em produção** fica em `dependencies`. `nodemon`, `eslint` e o que roda só na sua máquina ficam em `devDependencies`.

### 4.4 `npm ci`, não `npm install`

Os dois instalam dependências, mas fazem coisas diferentes:

| Comando | Usa o `package-lock.json` | Quando usar |
|---|---|---|
| `npm install` | atualiza o lock se achar necessário | na sua máquina, ao adicionar pacote |
| `npm ci` | exige o lock e instala **exatamente** ele | build, CI e produção |

O `npm ci` apaga o `node_modules/` e reinstala do zero, na versão exata registrada no lock. É reproduzível e mais rápido. Ele **falha** se o `package.json` e o `package-lock.json` estiverem inconsistentes — o que é bom: significa que alguém commitou um sem o outro.

> **⚠️ Atenção**
> O `package-lock.json` **precisa estar no repositório**. É comum ver `.gitignore` de tutorial antigo com `package-lock.json` dentro. Sem ele, `npm ci` falha com `The npm ci command can only install with an existing package-lock.json` e você perde meia hora achando que o problema é a plataforma.

### 4.5 Confiar no proxy

Em produção a sua API nunca fala direto com o navegador: existe um balanceador ou um nginx na frente. Do ponto de vista do Express, **todas** as requisições vêm do mesmo IP interno e chegam por HTTP simples. O IP real e o protocolo original vêm nos cabeçalhos `X-Forwarded-For` e `X-Forwarded-Proto`. Uma linha resolve:

```js
app.set('trust proxy', 1);
```

Com isso, `req.ip` passa a devolver o IP do visitante e `req.protocol` devolve `https`. Isso importa para logs, para limitar requisições por IP e para qualquer redirecionamento que dependa do protocolo.

## 5. Configuração e segredos

### 5.1 A regra

**Nada que muda entre a sua máquina e o servidor pode estar em código versionado.** Client ID do Google, senha do banco, chave de API, origem liberada no CORS: tudo vem do ambiente. O código lê `process.env`; quem preenche é a plataforma.

### 5.2 `.env` na sua máquina, painel no servidor

Na sua máquina, um arquivo `.env` na raiz do projeto guarda os valores. Ele **nunca** vai para o Git:

`.gitignore`

```gitignore
node_modules/
.env
.env.local
*.log
.DS_Store
```

O Node 22 lê esse arquivo sozinho, sem biblioteca nenhuma:

```bash
node --env-file=.env src/server.js
npm run dev
```

E, para documentar quais variáveis existem sem vazar valor nenhum, versiona-se um **exemplo**:

`.env.example`

```env
# Copie este arquivo para .env e preencha. O .env NUNCA vai para o Git.

# Porta local. Em produção a plataforma define esta variável sozinha.
PORT=3000

# 0.0.0.0 = todas as interfaces. Obrigatório em contêiner/PaaS.
HOST=0.0.0.0

# development | production
NODE_ENV=development

# Origens autorizadas a chamar a API pelo navegador, separadas por vírgula.
CORS_ORIGENS=http://localhost:5500,http://127.0.0.1:5500

# Client ID do Google Identity Services (Nível 2, Unidade 3).
GOOGLE_CLIENT_ID=coloque-aqui-o-client-id-do-console-do-google
```

O `.env.example` é a documentação executável do seu projeto: quem clonar o repositório copia, preenche e roda.

### 5.3 No Render

As mesmas variáveis vão em **Environment → Environment Variables**, uma a uma. Duas particularidades:

- A plataforma injeta `PORT` sozinha — **não crie** essa variável manualmente.
- Para arquivos inteiros (a chave JSON de uma conta de serviço do Firebase, por exemplo) existe **Secret Files**: você cola o conteúdo e ele aparece como arquivo no disco do serviço, sem passar pelo Git.

Mudar uma variável dispara um novo deploy. É o comportamento certo: o processo só lê o ambiente quando sobe.

### 5.4 Vazou um segredo. E agora?

Se um `.env` foi commitado, **remover no commit seguinte não resolve** — o valor continua no histórico e qualquer pessoa com o repositório o encontra com `git log -p`. A ordem é sempre esta:

1. **Revogue e gere outro** no serviço de origem (Google Cloud Console, painel do banco). O segredo antigo passa a não valer nada, e é isso que interessa.
2. Coloque o novo valor no painel da plataforma e no seu `.env` local.
3. Só então limpe o histórico, se valer a pena.
4. Adicione `.env` ao `.gitignore` e confira com `git ls-files | grep env` que nada suspeito está versionado.

> **⚠️ Atenção**
> Robôs varrem o GitHub procurando chaves em commits públicos, e o intervalo entre o `push` e o primeiro uso indevido costuma ser de **minutos**. Nunca conte com "o repositório é pequeno, ninguém vai ver".

## 6. Health check e logs

### 6.1 A rota de saúde

Um *health check* é uma rota barata que responde "estou de pé". A plataforma a chama a cada poucos segundos; monitores externos (Capítulo 10) também. Ela precisa ser rápida, não precisa de autenticação e **não** pode devolver dado sensível.

`src/app.js`

```js
// src/app.js — monta o Express; não abre porta (isso é do server.js).
import express from 'express';
import cors from 'cors';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { config } from './config.js';
import rotasProdutos from './rotas/produtos.js';

const aqui = path.dirname(fileURLToPath(import.meta.url));

export const app = express();

// Atrás do balanceador da plataforma: req.ip e req.protocol passam a ser os reais.
app.set('trust proxy', 1);

app.use(express.json());
app.use(cors({ origin: config.origensPermitidas }));
app.use(express.static(path.join(aqui, '..', 'public')));

// Health check. Dois caminhos: o nosso e o nome que as ferramentas esperam.
app.get(['/api/saude', '/health'], (requisicao, resposta) => {
  resposta.json({
    status: 'ok',
    ambiente: config.ambiente,
    versao: process.env.npm_package_version ?? 'desconhecida',
    segundosNoAr: Math.round(process.uptime()),
  });
});

app.use('/api/produtos', rotasProdutos);

// 404 em JSON: quem chama uma API espera JSON, não uma página de erro em HTML.
app.use((requisicao, resposta) => {
  resposta.status(404).json({ erro: 'Rota não encontrada', caminho: requisicao.originalUrl });
});

// Tratador de erros do Express 5: quatro parâmetros, sempre por último.
// Em produção, a mensagem interna vai só para o log — nunca para o cliente.
app.use((erro, requisicao, resposta, proximo) => {
  console.error(`[erro] ${requisicao.method} ${requisicao.originalUrl} — ${erro.message}`);
  resposta.status(erro.status ?? 500).json({
    erro: config.producao ? 'Erro interno do servidor' : erro.message,
  });
});
```

Repare em três decisões:

- O health check aceita `/api/saude` **e** `/health`. Passar um array de caminhos é a forma correta no Express 5, que não aceita mais alternância por expressão regular na rota.
- O tratador de erros tem **quatro** parâmetros. É a assinatura que faz o Express reconhecê-lo como tratador de erros; com três, ele vira um middleware comum e nunca é chamado. No Express 5 você não precisa mais de `.catch(next)` em handlers `async`: erros de promessa rejeitada chegam aqui sozinhos.
- A mensagem real do erro só aparece no log. Devolver `erro.message` em produção entrega ao atacante nomes de tabelas, caminhos de arquivo e versões.

### 6.2 O que o health check **não** deve fazer

Uma rota de saúde que consulta o banco a cada 5 segundos multiplica a carga do banco por nada. Duas variantes bem estabelecidas:

| Rota | Responde | Quem usa |
|---|---|---|
| *liveness* (`/api/saude`) | "o processo está vivo" — sem tocar em dependências | a plataforma, o supervisor |
| *readiness* | "consigo atender" — testa banco e serviços | um orquestrador, antes de mandar tráfego |

No Café Cerrado, uma rota de *liveness* basta. E jamais devolva variáveis de ambiente, caminhos absolutos ou a string de conexão do banco: essa rota é pública.

### 6.3 Logs: `stdout` é o log

Numa PaaS não existe arquivo de log para você abrir. **O que o processo escreve na saída padrão é o log** — a plataforma captura, carimba a data e mostra no painel. Ou seja: `console.log` e `console.error` são a sua ferramenta.

Três regras que evitam sofrimento:

1. **Uma linha por evento**, com um prefixo que identifique de onde veio (`[cafe-cerrado-api]`, `[erro]`). Painel de logs é lido com busca textual.
2. **Nunca logue segredo.** `console.log(config)` parece inofensivo até imprimir o client ID e a senha do banco em texto puro num painel compartilhado.
3. **Logue o suficiente para reconstruir uma falha**: método, caminho, status e tempo. Um middleware de 6 linhas resolve; no Capítulo 10 isso vira log estruturado com o `pino`.

`src/registro.js`

```js
// src/registro.js — middleware de log de acesso, em uma linha por requisição.
export function registrarAcesso(requisicao, resposta, proximo) {
  const inicio = process.hrtime.bigint();
  resposta.on('finish', () => {
    const ms = Number(process.hrtime.bigint() - inicio) / 1_000_000;
    console.log(
      `[acesso] ${requisicao.method} ${requisicao.originalUrl} ${resposta.statusCode} ${ms.toFixed(1)}ms`,
    );
  });
  proximo();
}
```

Use `app.use(registrarAcesso);` logo depois do `trust proxy`. O evento `finish` do objeto de resposta dispara quando a resposta terminou de ser enviada, então o tempo medido é o tempo real da requisição.

> **🔬 Investigue**
> Suba a API localmente com `npm run dev` e, em outro terminal, rode os três comandos abaixo. Compare o corpo, o status e o tempo de cada um; depois olhe o terminal do servidor e confira que cada requisição gerou exatamente uma linha `[acesso]`.
>
> ```bash
> curl -i http://localhost:3000/api/saude
> curl -i http://localhost:3000/api/produtos
> curl -i http://localhost:3000/api/nao-existe
> ```
>
> Agora derrube o servidor com <kbd>Ctrl</kbd>+<kbd>C</kbd> e observe as mensagens de encerramento da §4.2. Quantos milissegundos o processo levou entre receber o sinal e sair?

## 7. CORS: liberando o front publicado

### 7.1 O que o navegador faz

Enquanto front e back rodavam na mesma máquina, tudo era `localhost` e nada reclamava. Publicados, eles ficam em **origens diferentes**: `https://cafe-cerrado.netlify.app` e `https://cafe-cerrado-api.onrender.com`. Uma origem é a trinca **protocolo + host + porta** — mudou qualquer um dos três, é outra origem.

Por padrão, o navegador **bloqueia** a leitura da resposta de uma requisição para outra origem feita por JavaScript. Repare no verbo: a requisição costuma chegar ao servidor e ser executada; o que o navegador impede é o seu código **ler** o resultado. A permissão vem de um cabeçalho enviado pelo servidor:

```http
Access-Control-Allow-Origin: https://cafe-cerrado.netlify.app
```

Sem esse cabeçalho, o console mostra a mensagem que você vai ver muito nesta semana:

```text
Access to fetch at 'https://cafe-cerrado-api.onrender.com/api/produtos'
from origin 'https://cafe-cerrado.netlify.app' has been blocked by CORS policy:
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

### 7.2 A requisição de verificação prévia

Requisições "simples" (`GET`, ou `POST` com formulário) saem direto. Mas um `POST` com `Content-Type: application/json`, ou qualquer requisição com cabeçalho `Authorization`, dispara antes uma **verificação prévia** (*preflight*): o navegador manda um `OPTIONS` perguntando se aquele método e aqueles cabeçalhos são permitidos.

```http
OPTIONS /api/produtos HTTP/1.1
Origin: https://cafe-cerrado.netlify.app
Access-Control-Request-Method: POST
Access-Control-Request-Headers: content-type, authorization
```

Se a resposta ao `OPTIONS` não trouxer as permissões, a requisição real **nem sai**. Sintoma clássico: o `GET` funciona, o `POST` falha, e não há nenhum registro do `POST` no log do servidor.

### 7.3 Configurando de verdade

O pacote `cors` cuida do `OPTIONS` e dos cabeçalhos. O que muda em relação ao tutorial genérico é a **origem**: ela vem da configuração, não fica escrita no código.

```js
app.use(
  cors({
    origin: config.origensPermitidas,
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    maxAge: 86400,
  }),
);
```

E, no painel do Render:

```env
CORS_ORIGENS=https://cafe-cerrado.netlify.app,https://cafe.seudominio.dev
```

Sem barra no final, com o protocolo, exatamente como aparece na barra de endereço. `https://cafe-cerrado.netlify.app/` (com barra) não casa.

> **⚠️ Atenção**
> `origin: '*'` libera qualquer site do mundo a chamar a sua API pelo navegador do visitante. Para uma API pública e somente leitura, pode ser aceitável. Para qualquer coisa que aceite `POST`, `PUT` ou `DELETE`, não é. E existe uma incompatibilidade dura: `*` é **incompatível com credenciais** — com `credentials: true`, o navegador exige uma origem específica e recusa o curinga, com a mensagem `The value of the 'Access-Control-Allow-Origin' header in the response must not be the wildcard '*' when the request's credentials mode is 'include'`.

### 7.4 CORS não é segurança do servidor

Isto derruba muita gente: CORS protege o **usuário**, não o seu servidor. Ele é uma regra que o **navegador** aplica. Um `curl`, um script Node ou o Postman ignoram CORS completamente — sua API responde normalmente a eles. Portanto:

- CORS **não** substitui autenticação. Rota que precisa de login continua precisando verificar o token (Nível 2, Unidade 3).
- Se um `fetch` falha no navegador mas o `curl` funciona, o problema é CORS. Se falha nos dois, o problema é outro.

## 8. As três plataformas lado a lado

| Critério | Render | Railway / Fly.io |
|---|---|---|
| Plano gratuito | sim, com *cold start* e disco efêmero | crédito de teste; depois, por uso |
| Região mais próxima | EUA / Europa / Ásia | Fly.io tem São Paulo (`gru`) |
| Como se publica | conectar o repositório no painel | linha de comando (`railway up`, `fly deploy`) |
| Melhor para | primeiro deploy e trabalhos da disciplina | projeto com banco junto ou que precise de baixa latência |

Para este capítulo: **Render**. Ele é o que exige menos ferramentas instaladas, tem plano gratuito de verdade e ensina o contrato (build, start, `PORT`, variáveis, health check) que vale em qualquer lugar.

## 🚀 Passo a passo — a `cafe-cerrado-api` no Render

O que vai ao ar: a API do Café Cerrado, em `https://cafe-cerrado-api.onrender.com`, com deploy automático a cada `push`, health check configurado e o site estático publicado no Capítulo 03 consumindo essa URL.

### Passo 1 — deixe o repositório pronto

Na sua máquina, na raiz da `cafe-cerrado-api`:

```bash
node -v                       # precisa ser 22.x
npm ci                        # falha aqui? o package-lock.json está inconsistente
npm start                     # sobe em 0.0.0.0:3000
curl -s http://localhost:3000/api/saude
```

Resultado esperado do `curl`: `{"status":"ok","ambiente":"development","versao":"1.0.0","segundosNoAr":3}`.

Confira também o que está versionado:

```bash
git ls-files | grep -E "package-lock|\.env"
```

Deve aparecer `package-lock.json` e `.env.example` — e **não** deve aparecer `.env`.

### Passo 2 — aplique as mudanças das §4 a §7

Se ainda não fez: `src/config.js`, `src/server.js` com `SIGTERM`, `app.set('trust proxy', 1)`, o health check, o CORS por variável, o `engines` e o script `start` no `package.json`, o `.env.example` e o `.gitignore`.

```bash
git add .
git commit -m "prepara a API para produção: PORT, config, health check e CORS"
git push
```

### Passo 3 — crie o serviço no Render

No painel: **New → Web Service → Build and deploy from a Git repository**, autorize o GitHub e escolha o repositório `cafe-cerrado-api`. Preencha:

```text
Name:              cafe-cerrado-api
Language:          Node
Branch:            main
Region:            Oregon (US West)
Root Directory:    (vazio — o package.json está na raiz)
Build Command:     npm ci
Start Command:     npm start
Instance Type:     Free
```

### Passo 4 — cadastre as variáveis de ambiente

Ainda na tela de criação, em **Environment Variables**:

```env
NODE_ENV=production
NODE_VERSION=22
CORS_ORIGENS=https://cafe-cerrado.netlify.app
GOOGLE_CLIENT_ID=o-client-id-que-esta-no-seu-.env
```

Não crie `PORT`: o Render injeta essa variável e sobrescrever pode quebrar o serviço. Clique em **Deploy Web Service**.

### Passo 5 — acompanhe o primeiro deploy pelos logs

A aba **Logs** mostra, em ordem: o clone, o `npm ci`, o `npm start` e — se tudo deu certo — a sua própria linha:

```text
==> Cloning from https://github.com/seu-usuario/cafe-cerrado-api
==> Running build command 'npm ci'...
added 78 packages in 4s
==> Running 'npm start'
[cafe-cerrado-api] no ar em 0.0.0.0:10000 (production)
==> Your service is live 🎉
```

Repare na porta: `10000`, não `3000`. Foi o Render quem escolheu, e o seu código obedeceu porque lê `process.env.PORT`. Se em vez disso aparecer `==> No open ports detected`, volte à §4.2.

### Passo 6 — configure o health check

**Settings → Health & Alerts → Health Check Path**: `/api/saude`. Salve. A partir de agora, um deploy só entra no ar depois que essa rota responder `200` — e um deploy quebrado deixa a versão anterior servindo em vez de derrubar o site.

### Passo 7 — teste a API pública

```bash
curl -i https://cafe-cerrado-api.onrender.com/api/saude
curl -s https://cafe-cerrado-api.onrender.com/api/produtos | head -c 300
curl -i -X POST https://cafe-cerrado-api.onrender.com/api/produtos \
  -H "Content-Type: application/json" \
  -d '{"nome":"Café coado","preco":7.5}'
```

O `GET` de saúde responde `200` com o JSON. Se for a primeira requisição depois de um tempo parado, ela vai demorar — é o *cold start* da §2.1. O `POST` responde `401` se a sua API exige autenticação; isso é sucesso, não erro: significa que a rota existe e a regra funciona.

### Passo 8 — ligue o front publicado à API

No repositório do Café Cerrado estático, centralize a URL em um só arquivo:

`js/api.js`

```js
// js/api.js — único lugar do front que sabe onde a API mora.
const local = ['localhost', '127.0.0.1'].includes(window.location.hostname);

export const API_URL = local
  ? 'http://localhost:3000'
  : 'https://cafe-cerrado-api.onrender.com';

export async function buscarProdutos() {
  const resposta = await fetch(`${API_URL}/api/produtos`);
  if (!resposta.ok) {
    throw new Error(`A API respondeu ${resposta.status} ${resposta.statusText}`);
  }
  return resposta.json();
}

export async function acordarApi() {
  // Plano gratuito dorme depois de ~15 min. Chamar o health check no carregamento
  // da página faz o servidor acordar enquanto o usuário ainda lê o cabeçalho.
  try {
    await fetch(`${API_URL}/api/saude`, { cache: 'no-store' });
  } catch {
    console.warn('[api] não consegui acordar a API; ela pode estar iniciando.');
  }
}
```

Chame `acordarApi()` no início do script da página e mostre um estado de carregamento honesto enquanto `buscarProdutos()` não volta. Faça `commit` e `push`; a Netlify republica sozinha.

### Passo 9 — confirme o CORS com a origem real

Abra o site publicado, vá ao DevTools → Console. Se aparecer `blocked by CORS policy`, copie a origem exata que a mensagem cita, coloque-a em `CORS_ORIGENS` no Render (separando por vírgula, sem barra final) e salve — o serviço reinicia com o valor novo.

### Passo 10 — deploy automático e rollback

Faça uma mudança qualquer visível (o texto de uma mensagem de erro, por exemplo), `commit` e `push`. Em **Events**, o Render mostra o deploy começando sozinho. Se algo quebrar, o mesmo painel tem o botão de voltar para a versão anterior — e é por isso que commits pequenos valem tanto.

### Como conferir

```bash
curl -s -o /dev/null -w "%{http_code} %{time_total}s\n" https://cafe-cerrado-api.onrender.com/api/saude
curl -s -H "Origin: https://cafe-cerrado.netlify.app" -i \
  https://cafe-cerrado-api.onrender.com/api/produtos | grep -i access-control
curl -s -H "Origin: https://site-aleatorio.example" -i \
  https://cafe-cerrado-api.onrender.com/api/produtos | grep -i access-control
```

Resultado esperado:

- o primeiro comando devolve `200` e um tempo total abaixo de 1 s (a não ser que o serviço estivesse dormindo — repita e compare os dois tempos);
- o segundo mostra `access-control-allow-origin: https://cafe-cerrado.netlify.app`;
- o terceiro **não** mostra nenhum cabeçalho `access-control-allow-origin` — a origem desconhecida não foi liberada;
- no site publicado, o cardápio carrega os produtos vindos do Render e o console não tem erros;
- no painel do Render, a aba **Logs** mostra as linhas `[acesso] GET /api/produtos 200` correspondentes às suas visitas.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Explique em duas frases por que o GitHub Pages não consegue hospedar a `cafe-cerrado-api`, mesmo o repositório tendo `index.html` dentro de `public/`.

**A2.** Preveja a saída. O código tem `app.listen(3000)` e a plataforma definiu `PORT=10000`. O processo sobe? A plataforma consegue falar com ele? Qual mensagem aparece no painel? E se o código tivesse `app.listen(process.env.PORT, '127.0.0.1')`?

**A3.** Classifique cada item em `dependencies` ou `devDependencies` e justifique: `express`, `nodemon`, `cors`, `eslint`, `google-auth-library`, `vitest`.

**A4.** Um colega diz: "coloquei `origin: '*'` e resolvi meu problema de CORS". Cite duas situações em que essa solução falha e uma em que ela é aceitável.

**A5.** Complete: para que a plataforma consiga abrir uma conexão com o seu processo, ele precisa escutar no host `______` e na porta lida de `______`. Se ele escutar em `127.0.0.1`, o erro no painel é `______`.

**A6.** A API grava um produto novo em `dados/produtos.json` e responde `201`. Você faz um `git push` de outro assunto qualquer. O produto continua lá? Explique com a palavra "efêmero" e diga qual capítulo resolve isso.

### Nível B — Aplicação

**B1.** Faça a API **recusar-se a subir** quando faltar uma variável obrigatória. Remova `GOOGLE_CLIENT_ID` do painel do Render (ou do seu `.env` com `NODE_ENV=production`) e observe o comportamento; depois melhore a mensagem de erro para que ela liste **todas** as variáveis faltantes de uma vez, não só a primeira.

Resultado esperado: com duas variáveis ausentes, o processo morre na subida com uma única mensagem do tipo `Configuração ausente: GOOGLE_CLIENT_ID, CORS_ORIGENS`, e o deploy é marcado como falho sem derrubar a versão que estava no ar.

<details><summary>Dica</summary>

Em vez de lançar a exceção dentro de `texto()`, acumule os nomes que faltaram em um array e lance uma única vez no fim do módulo. Lembre-se de que `import` executa o módulo inteiro antes de qualquer coisa — é por isso que o erro aparece antes de o servidor abrir a porta.
</details>

**B2.** Meça o *cold start*. Deixe o serviço parado por 20 minutos, depois cronometre a primeira requisição e mais cinco seguidas.

Resultado esperado: uma tabela com seis tempos, a primeira linha muito maior que as outras, e uma frase explicando a diferença. Comando sugerido: `curl -s -o /dev/null -w "%{time_total}\n" https://sua-api.onrender.com/api/saude`.

<details><summary>Dica</summary>

Use `for i in 1 2 3 4 5; do curl -s -o /dev/null -w "%{time_total}\n" URL; done` para as cinco seguidas. A diferença entre a primeira e a segunda é o tempo de subir o contêiner, instalar nada (a imagem já está pronta) e rodar `npm start`.
</details>

**B3.** Prove que CORS é regra de navegador. Faça a mesma requisição de três formas: pelo `fetch` no console de um site de origem não autorizada (abra qualquer site e use o console), por `curl` e pelo `fetch` do site autorizado.

Resultado esperado: a primeira falha com a mensagem de CORS, a segunda devolve o JSON normalmente, a terceira funciona. Um parágrafo explica por que a segunda funciona e o que isso significa para a segurança da sua API.

<details><summary>Dica</summary>

No console de um site qualquer, `await (await fetch('https://sua-api.onrender.com/api/produtos')).json()`. Olhe também a aba Rede: a requisição **saiu** e voltou com `200`; foi o navegador que impediu o JavaScript de ler.
</details>

**B4.** Adicione o middleware `registrarAcesso` da §6.3 e faça três requisições ruins de propósito: uma rota inexistente, um `POST` com JSON inválido e um `GET` numa rota que lança exceção. Leia as três linhas no log do Render.

Resultado esperado: as três linhas `[acesso]` copiadas do painel, com os status `404`, `400` e `500`, e a linha `[erro]` correspondente à terceira. Uma frase explica por que o cliente recebeu "Erro interno do servidor" e não a mensagem real.

<details><summary>Dica</summary>

Para forçar o `400`: `curl -X POST URL/api/produtos -H "Content-Type: application/json" -d '{isso não é json}'`. O `express.json()` rejeita e o erro cai no seu tratador. Para forçar o `500`, crie temporariamente uma rota que faça `throw new Error('erro de teste')`.
</details>

### Nível C — Desafio em sala

**C1.** Publique a **mesma** API em duas plataformas (Render e Fly.io, ou Render e Railway), a partir do mesmo repositório e do mesmo commit, e compare-as com dados. Meça, de Sinop: latência mediana de 20 requisições ao health check em cada uma, tempo do *cold start* (se houver), tempo total do deploy e o que cada painel mostra de log. Termine com uma recomendação de uma linha para o Café Cerrado, justificada pelos números.

<details><summary>Dica</summary>

O Fly.io precisa de um `Dockerfile` — o `fly launch` gera um para projetos Node, e o Capítulo 07 explica cada linha dele. Para a latência, `for i in $(seq 20); do curl -s -o /dev/null -w "%{time_total}\n" URL; done | sort -n` e pegue o valor do meio. A região `gru` deve fazer diferença visível; se não fizer, verifique onde a máquina realmente foi criada com `fly status`.
</details>

## 🏆 Desafios

### ⭐ Health check que diz a verdade
Tags: node, express, api, investigacao

O `/api/saude` do Passo a passo responde `ok` mesmo que o arquivo de dados tenha sumido, que o disco esteja cheio ou que a API não consiga mais ler o cardápio. Ele diz apenas "o processo está vivo" — o que é útil, mas é pouco quando alguém pergunta "o site está funcionando?". Crie uma segunda rota, de prontidão, que verifique de fato as dependências da API e responda com o status HTTP correto.

**Critérios de pronto**

- `GET /api/pronto` verifica se o arquivo de dados existe e é legível e responde `200` com `{"status":"pronto"}` quando tudo está bem.
- Quando a dependência falha, a rota responde `503` (não `200`, não `500`) com uma lista das verificações que falharam — sem revelar caminhos absolutos do servidor.
- `/api/saude` continua sem tocar em nada, respondendo em menos de 5 ms.
- Um teste manual documentado no `README.md`: como quebrar a dependência de propósito e o que se espera ver.
- O health check do Render continua apontando para `/api/saude`, e você explica em duas linhas por que **não** deve apontar para `/api/pronto`.

<details><summary>Pistas</summary>

1. `fs.promises.access(caminho, fs.constants.R_OK)` resolve ou rejeita — é a verificação mais barata de "existe e consigo ler".
2. O código `503 Service Unavailable` significa "estou de pé, mas não consigo atender agora". É o status que monitores entendem como indisponibilidade temporária.
3. Para quebrar de propósito sem apagar nada: renomeie o arquivo, ou mude a permissão com `chmod 000`.
4. Se o *readiness* fosse o health check da plataforma, uma falha momentânea do banco derrubaria o serviço inteiro e reiniciaria o processo em looping — pense no que isso causaria durante um pico de acesso.
</details>

### ⭐⭐ Uma API, três ambientes
Tags: deploy, node, seguranca, projeto

Todo time profissional trabalha com três ambientes: **local** (a sua máquina), **homologação** (onde se testa sem medo) e **produção** (onde os usuários estão). Hoje a sua API tem local e produção, e cada `push` na `main` vai direto para os visitantes. Monte o do meio: um serviço de homologação ligado à branch `desenvolvimento` e o de produção ligado à `main`, com variáveis, dados e URLs diferentes — e o front escolhendo a URL certa sem você editar código na hora do deploy.

**Critérios de pronto**

- Dois serviços no Render a partir do **mesmo** repositório, em branches diferentes, com nomes distinguíveis (`cafe-cerrado-api` e `cafe-cerrado-api-homolog`).
- `CORS_ORIGENS` de cada um libera apenas o front correspondente (produção não aceita a origem de homologação e vice-versa) — provado com dois `curl -H "Origin: …"`.
- `GET /api/saude` de cada serviço devolve `ambiente` diferente, e a resposta permite identificar em qual você está sem olhar a URL.
- Um `pull request` da `desenvolvimento` para a `main` sobe para produção só depois de mesclado; um `push` direto na `desenvolvimento` **não** afeta produção. Demonstre com o histórico da aba Events.
- `README.md` com uma tabela de três colunas (ambiente · branch · URL) e o procedimento de promoção em até cinco passos.

<details><summary>Pistas</summary>

1. Ao criar o segundo serviço, mude apenas **Branch** e **Name**; todo o resto é igual. As variáveis são independentes por serviço.
2. Para o front escolher a URL, você já tem `js/api.js`: acrescente uma terceira possibilidade baseada em `window.location.hostname`, ou publique dois sites (um por branch) na Netlify, que sabe fazer *deploy* por branch.
3. Dois serviços gratuitos consomem a mesma cota mensal de horas da conta. Suspenda o de homologação quando não estiver usando.
4. Se o `pull request` mesclado não disparar deploy, confira em Settings se o *Auto-Deploy* está ligado e se a branch está certa.
</details>

### ⭐⭐⭐ Sobreviva ao disco efêmero
Tags: deploy, node, api, banco-de-dados

Faça o teste que ninguém faz antes de entregar: crie três produtos pela API publicada, force um novo deploy e recarregue o cardápio. Eles sumiram. O `dados/produtos.json` voltou ao estado do repositório, porque o disco do serviço é efêmero — e isso vale para uploads, sessões em arquivo e qualquer coisa que o seu código grave. Documente a perda com evidências e implemente uma solução que sobreviva a três reinícios seguidos, **sem** ainda usar um banco gerenciado (isso é o Capítulo 08).

**Critérios de pronto**

- Um registro do problema no `README.md`: as três requisições de criação, a saída do `GET` antes e depois do deploy, e o horário de cada uma.
- Uma solução implementada e funcionando após três deploys consecutivos: pode ser um armazenamento externo por HTTP (um Gist, um bucket, uma planilha via API) ou um disco persistente pago — a escolha é sua, mas precisa estar justificada.
- A API continua respondendo em menos de 1 s no caminho feliz: nada de ler o armazenamento externo a cada requisição sem cache em memória.
- Tratamento de falha: se o armazenamento externo estiver fora do ar, a API responde `503` na escrita e continua servindo leitura do cache — não devolve `500` genérico nem trava.
- Uma seção de 10 linhas no `README.md` comparando a sua solução com "usar um banco gerenciado" em três eixos: complexidade, custo e risco de perda de dados.

<details><summary>Pistas</summary>

1. Comece medindo: `curl` de criação, `git commit --allow-empty -m "forca deploy"` e `git push` para disparar um deploy sem mudar código, e `curl` de leitura depois.
2. O padrão é sempre o mesmo: **cache em memória + persistência externa**. Leia uma vez na subida, mantenha o array em memória, e grave fora a cada alteração.
3. Escrever a cada requisição num serviço externo é lento e frágil. Pesquise "write-behind" e considere agrupar as gravações em um intervalo — e o que acontece com as alterações pendentes quando chega o `SIGTERM` (§4.2).
4. Se optar por disco persistente, veja que ele fixa o serviço em uma única instância; entenda por que isso impede escalar horizontalmente antes de defender a escolha.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| Painel: `==> No open ports detected, continuing to scan...` e o deploy expira | processo escutando em `127.0.0.1` ou em porta fixa, ignorando `process.env.PORT` | `app.listen(process.env.PORT ?? 3000, '0.0.0.0')` |
| Build falha com `The npm ci command can only install with an existing package-lock.json` | lock ausente ou dessincronizado do `package.json` | rode `npm install` local, commite o `package-lock.json`; nunca o coloque no `.gitignore` |
| Start falha com `Error: Cannot find module 'express'` | dependência declarada em `devDependencies`, ou build command errado | mova para `dependencies`; confirme `npm ci` como build command |
| Start falha com `SyntaxError: Cannot use import statement outside a module` | `import`/`export` sem `"type": "module"` no `package.json` | adicione o campo, ou converta o arquivo para `require` |
| Console do site: `blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present` | a origem publicada não está em `CORS_ORIGENS`, ou entrou com barra final | copie a origem exata da mensagem, sem barra, e salve a variável no painel |
| O `GET` funciona, o `POST` falha e **não** aparece no log do servidor | a verificação prévia (`OPTIONS`) foi bloqueada antes da requisição real | libere `methods` e `allowedHeaders` no `cors`; não intercepte `OPTIONS` antes dele |
| `The value of the 'Access-Control-Allow-Origin' header in the response must not be the wildcard '*'` | `origin: '*'` combinado com `credentials: true` | liste as origens explicitamente |
| Primeira requisição do dia leva quase um minuto; as seguintes, milissegundos | *cold start*: o plano gratuito desligou o serviço após ~15 min sem tráfego | acorde no carregamento da página (Passo 8), avise o usuário, ou pague um plano que não dorme |
| Produtos criados somem depois de um `git push` | disco efêmero: o sistema de arquivos volta ao estado do repositório a cada deploy | banco de dados (Capítulo 08) ou armazenamento externo |
| Processo morre no start com `Configuração ausente: GOOGLE_CLIENT_ID` | variável não cadastrada no painel | cadastre em Environment; compare com o `.env.example` |
| `Error: listen EADDRINUSE: address already in use :::3000` na sua máquina | outro processo (ou uma instância antiga da API) segurando a porta | `lsof -i :3000` e encerre o processo, ou rode com outra `PORT` |
| Deploy "bem-sucedido" mas o site responde `502` | o processo caiu logo depois de subir; o health check não estava configurado | veja os logs no minuto do deploy; defina o Health Check Path (Passo 6) |
| Segredo apareceu no log do painel | algum `console.log` imprimindo o objeto de configuração inteiro | remova o log, **revogue e gere outro segredo** (§5.4) |

## 🏠 Atividade assíncrona (1 h)

Na API do seu **projeto autoral** (ou na `cafe-cerrado-api`, se o seu projeto ainda não tem back-end):

1. Aplique as cinco preparações da §4: `PORT` do ambiente, `0.0.0.0`, `engines`, script `start` e tratamento de `SIGTERM`.
2. Crie `src/config.js` lendo todas as configurações do ambiente, com mensagem de erro clara quando faltar alguma, e um `.env.example` completo e comentado. Confirme que o `.env` **não** está versionado.
3. Publique no Render (ou Railway/Fly.io) com health check configurado e deploy automático a partir da `main`.
4. Ligue o front publicado à URL da API, com `CORS_ORIGENS` liberando exatamente aquela origem.
5. Acrescente ao `README.md` uma seção **"Como publicar"** de no máximo 15 linhas: variáveis necessárias, build command, start command, health check path e como ver os logs.

**Critério de pronto:** um colega consegue, lendo só o seu `README.md`, dizer quais variáveis precisa cadastrar; `curl https://sua-api/api/saude` responde `200` com JSON; o site publicado carrega dados da API sem erro no console; e `git ls-files` não lista nenhum `.env`.

**Entrega:** commit + push e link do repositório no SIGAA, com a URL pública da API e a do site na descrição do repositório.

## ✅ Está no ar quando…

- [ ] `curl -i https://sua-api/api/saude` devolve `200` com `{"status":"ok"}` e o `ambiente` correto.
- [ ] Nos logs do primeiro deploy aparece a porta escolhida pela plataforma (não `3000`), lida de `process.env.PORT`.
- [ ] O site publicado no Capítulo 03 lista os produtos vindos da API, sem nenhum erro no console.
- [ ] `curl -H "Origin: <origem-do-front>"` traz o cabeçalho `access-control-allow-origin`; com uma origem qualquer, não traz.
- [ ] Nenhum segredo está no repositório: `git ls-files` não mostra `.env`, e o `.env.example` documenta todas as variáveis.
- [ ] Um `push` na branch configurada dispara um deploy sozinho, visível na aba Events.
- [ ] O Health Check Path aponta para a rota de saúde e um deploy quebrado **não** derruba a versão anterior.
- [ ] Você sabe dizer, sem consultar, quanto tempo leva o *cold start* da sua API e o que acontece com um arquivo gravado pelo processo depois de um novo deploy.
- [ ] O `README.md` tem a seção "Como publicar" e o `package.json` tem `engines` e `start`.

## 📚 Para aprofundar

- Render — "Deploy a Node.js app": <https://render.com/docs/deploy-node-express-app> — o guia oficial do fluxo que você fez, com as telas atualizadas.
- Render — "Environment variables and secret files": <https://render.com/docs/configure-environment-variables> — variáveis, grupos e arquivos de segredo.
- Render — "Health checks" e "Free instance types": <https://render.com/docs/health-checks> — o que a plataforma faz com a rota de saúde e os limites do plano gratuito.
- Render — Blueprint (`render.yaml`): <https://render.com/docs/blueprint-spec> — descrever o serviço em arquivo versionado em vez de clicar no painel.
- Railway — documentação: <https://docs.railway.com> — e Fly.io — "Speedrun": <https://fly.io/docs/languages-and-frameworks/node/> — para comparar os modelos.
- The Twelve-Factor App (em português): <https://12factor.net/pt_br/> — leia os fatores III (Config), VI (Processos) e IX (Descartabilidade); são exatamente as §§4 e 5 deste capítulo.
- Node.js — variáveis de ambiente e `--env-file`: <https://nodejs.org/api/cli.html#--env-fileconfig> — o suporte nativo que dispensa bibliotecas.
- Node.js — sinais de processo: <https://nodejs.org/api/process.html#signal-events> — `SIGTERM`, `SIGINT` e o que cada um significa.
- Express — guia de produção, "Best Practices": <https://expressjs.com/pt-br/advanced/best-practice-performance.html> — em português, com `NODE_ENV`, tratamento de erros e proxy reverso.
- MDN — CORS: <https://developer.mozilla.org/pt-BR/docs/Web/HTTP/CORS> — a referência definitiva, com a lista do que dispara verificação prévia.
- MDN — "Same-origin policy": <https://developer.mozilla.org/pt-BR/docs/Web/Security/Same-origin_policy> — por que a regra existe, do ponto de vista do usuário.
- npm — `npm ci`: <https://docs.npmjs.com/cli/v10/commands/npm-ci> — as diferenças exatas para o `npm install`.

No próximo capítulo você sai da PaaS e aluga um servidor inteiro: um VPS com Ubuntu, acesso por SSH com chave, firewall, Node e MySQL instalados na mão, nginx fazendo proxy reverso, pm2 mantendo o processo vivo e o `certbot` emitindo o certificado — inclusive no laboratório real da disciplina, em `ivanpires.dev/dsw/gN/`.
