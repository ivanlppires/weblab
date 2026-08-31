# Aula 15 — CRUD com front-end assíncrono

> **Nível 2 — Desenvolvimento Web** · Unidade 3: Web dinâmica server-side
> WebLab · UNEMAT — Campus Sinop
> **Tempo estimado:** 3 blocos de 50 min + 1 h de prática

Sua API já faz CRUD completo e já sabe quem está batendo na porta. Só que, até agora, quem usou esses recursos foi você — pelo `testes.http`, com a extensão REST Client. Nenhuma outra pessoa consegue cadastrar um café no Café Cerrado sem escrever uma requisição HTTP na mão. Hoje isso muda: a interface que você construiu na Unidade 2 passa a criar, editar e excluir produtos consumindo a sua própria API, sem recarregar a página uma única vez.

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Descrever o contrato completo de um recurso REST (método, caminho, corpo, resposta, status) e usá-lo como acordo entre front e back.
- Ler o contrato de um recurso já implementado (o repositório e o controlador das Aulas 13 e 14) e construir um cliente que o respeite sem alterá-lo.
- Explicar por que uma gravação em duas etapas (arquivo temporário + `rename`) protege os dados contra um servidor que morre no meio da escrita.
- Construir uma camada de acesso à API no cliente (`public/js/api.js`) que centraliza cabeçalhos, token e tratamento de erros.
- Implementar os quatro estados de uma tela que depende de rede — carregando, erro, vazio e conteúdo — e renderizá-los a partir de uma única fonte de verdade.
- Reutilizar um mesmo formulário para criar e editar registros, com o padrão de "modo edição" e foco controlado.
- Excluir registros com confirmação e anunciar cada resultado com `aria-live`, sem recarregar a página.
- Depurar uma integração front-back pela aba Network do DevTools, identificando de qual lado está o defeito.

## 📋 Pré-requisitos

- [ ] Repositório `cafe-cerrado-api` rodando com `npm run dev`, servindo o site em `http://localhost:3000` por `express.static(path.join(__dirname, 'public'))` (Aula 11).
- [ ] `routes/produtos.js`, `controllers/produtosController.js` e os middlewares de log, 404 e erro funcionando (Aulas 12 e 13).
- [ ] CRUD da API respondendo pelo `testes.http`: `GET`, `POST`, `PUT` e `DELETE` em `/api/produtos` (Aula 13).
- [ ] Login Google funcionando, `.env` com `GOOGLE_CLIENT_ID` fora do Git e o middleware `exigirLogin` protegendo as rotas de escrita (Aula 14).
- [ ] `fetch` com `async/await` e tratamento de erro no cliente (Aulas 09 e 10) — hoje é tudo isso ao mesmo tempo.

> Na aula passada você delegou o login ao Google, verificou o ID token no servidor com `google-auth-library` e barrou com `401` toda escrita sem token. As duas metades do sistema — API com CRUD e API com autenticação — existem, mas só respondem ao `testes.http`. Hoje elas ganham interface: a tela do cardápio passa a listar, criar, editar e excluir produtos consumindo `/api/produtos` com `fetch`, e os dados passam a sobreviver ao reinício do servidor. Na próxima aula, cada registro ganha dono e esta trilha se encerra com o Marco 3.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Contrato do recurso; revisão do repositório e do controlador das Aulas 13 e 14; gravação atômica |
| 2 | 50 min | Camada de API no cliente (`public/js/api.js`); estado e render; os quatro estados da tela |
| 3 | 50 min | Formulário criar/editar, exclusão com confirmação, feedback acessível; Mão na massa e laboratório |

## 1. O front-end encontra a própria API

### 1.1 Uma origem só, zero CORS

Na Aula 10 o seu `fetch` foi buscar dados no JSONPlaceholder — um servidor de outra pessoa, em outro domínio. Aquilo é uma requisição **cross-origin**, e só funcionou porque o JSONPlaceholder responde com o cabeçalho `Access-Control-Allow-Origin: *`, autorizando qualquer site a lê-lo.

Agora a situação é outra e muito mais simples. Desde a Aula 11 o Express serve o site estático (`express.static`) **e** a API no mesmo processo, na mesma porta. Abrir `http://localhost:3000/index.html` e pedir `fetch("/api/produtos")` é uma requisição de mesma origem: mesmo protocolo (`http`), mesmo host (`localhost`), mesma porta (`3000`). Nada de CORS, nada de cabeçalhos especiais, nada de preflight.

Isso tem uma consequência prática importante no código: **use sempre caminhos relativos**.

```js
// Certo: funciona em localhost:3000, em localhost:4000 e no dia em que o
// projeto for publicado num domínio de verdade — a URL acompanha o site.
const resposta = await fetch("/api/produtos");

// Errado: quebra assim que a porta ou o domínio mudarem.
const resposta2 = await fetch("http://localhost:3000/api/produtos");
```

> **⚠️ Atenção**
> Abrir o `index.html` com um duplo clique (`file:///home/voce/cafe-cerrado-api/public/index.html`) **não** funciona mais. O protocolo `file://` não tem servidor, e `/api/produtos` viraria um caminho no seu disco. A partir de agora o site só é aberto por `http://localhost:3000`, com o `npm run dev` rodando. Se você usava Live Server, aposente-o nesta unidade: quem serve o front agora é o seu próprio Express.

### 1.2 O contrato do recurso `produto`

Antes de escrever qualquer código de integração, front e back precisam concordar num **contrato**: para cada operação, qual método HTTP, qual caminho, o que vai no corpo, o que volta e qual status. O contrato é o que permite que você mexa num lado sem ler o código do outro — e é o que você vai consultar às duas da manhã, quando a tela mostrar "undefined".

Ele não é novidade: é exatamente o que a sua API responde desde a Aula 13, com as escritas protegidas pelo `exigirLogin` da Aula 14. O que fazemos aqui é escrevê-lo por extenso, do ponto de vista de quem consome.

| Método | Caminho | Autenticação |
|---|---|---|
| GET | `/api/produtos` | Pública |
| GET | `/api/produtos/:id` | Pública |
| POST | `/api/produtos` | Exige login |
| PUT | `/api/produtos/:id` | Exige login |
| DELETE | `/api/produtos/:id` | Exige login |

Detalhando corpo e resposta de cada operação:

**`GET /api/produtos`** — lista o cardápio. Aceita três parâmetros de query string, todos criados na Aula 13 e todos usados pela tela de hoje: `?q=termo` (busca no nome e na descrição, ignorando acento e caixa), `?categoria=cafes` (filtra pela categoria exata) e `?ordenar=preco` (também `-preco` e `nome`). Status `200`. Resposta:

```json
[
  {
    "id": 1,
    "nome": "Espresso do Cerrado",
    "categoria": "cafes",
    "preco": 6,
    "descricao": "Grãos de Alto Paraíso, torra média, corpo encorpado e final achocolatado.",
    "imagem": "img/espresso.jpg"
  }
]
```

**`GET /api/produtos/:id`** — um produto. Status `200`; `404` com `{ "erro": "Produto 99 não encontrado." }`; e `400` quando o id nem é um número inteiro positivo (`/api/produtos/abacaxi`).

**`POST /api/produtos`** — corpo com os campos editáveis. `categoria` só aceita um dos quatro ids do cardápio (`cafes`, `geladas`, `salgados`, `doces`) — é a lista branca do controlador:

```json
{
  "nome": "Suco de Cupuaçu",
  "categoria": "geladas",
  "preco": 10.5,
  "descricao": "Polpa batida com água gelada e um fio de mel.",
  "imagem": "img/suco-cupuacu.jpg"
}
```

Resposta: o produto criado, já com `id`, status `201` e cabeçalho `Location: /api/produtos/11`. Sem token: `401`. Corpo inválido: `400` com o formato de erro abaixo — guarde-o, porque o formulário da seção 5 depende dele para colorir o campo certo:

```json
{
  "erro": "Dados inválidos.",
  "detalhes": [
    { "campo": "nome", "mensagem": "O nome precisa ter ao menos 3 caracteres." },
    { "campo": "preco", "mensagem": "O preço precisa ser um número maior que zero." }
  ]
}
```

Cada item de `detalhes` traz **o campo** e **a mensagem**, e não só um texto solto. É essa dupla que permite ao front pendurar a mensagem embaixo do `<input>` correspondente em vez de despejar tudo num alerta genérico.

**`PUT /api/produtos/:id`** — mesmo corpo do `POST`, com atualização parcial permitida (envie só o que mudou). Resposta: o produto atualizado, status `200`. Inexistente: `404`. Id malformado: `400`. Sem token: `401`.

**`DELETE /api/produtos/:id`** — sem corpo. Resposta: status `204 No Content`, **sem corpo nenhum**. Inexistente: `404`. Id malformado: `400`. Sem token: `401`.

> **💡 Dica**
> `204` não pode ter corpo: `resposta.json()` sobre uma resposta `204` explode com `Unexpected end of JSON input`. A camada de API que escreveremos na seção 3 trata isso em uma linha — e é o tipo de detalhe que consome uma tarde de quem não sabe que existe.

> **📌 Vale gravar**
> Decore a semântica dos status que este contrato usa: `200 OK` (deu certo e há corpo), `201 Created` (criou um recurso novo), `204 No Content` (deu certo e não há corpo), `400 Bad Request` (o cliente mandou algo inválido), `401 Unauthorized` (não sei quem você é), `404 Not Found` (o recurso não existe). O `403` entra na próxima aula.

### 1.3 O ciclo estado → render

Toda a lógica de tela desta aula cabe numa frase: **o JavaScript nunca edita a tela por partes; ele muda o estado e manda desenhar tudo de novo.**

```text
evento do usuário  →  chamada à API  →  atualiza o estado  →  renderizar()  →  HTML na tela
```

Concretamente: quando você exclui um produto, o código **não** procura o `<article>` daquele card para removê-lo do DOM. Ele chama a API, recarrega a lista de produtos do servidor, guarda no array `produtos` e chama `renderizar()`, que apaga o container e o redesenha inteiro. Parece desperdício — e é, para listas gigantes — mas elimina de uma vez a classe de bug mais comum de front-end: a tela dizendo uma coisa e os dados dizendo outra.

Guarde esse ciclo. É exatamente o que Vue e React automatizam, e você vai reencontrá-lo no Nível 3 sob outro nome ("reatividade"). Aqui você o implementa à mão, que é a melhor forma de entender o que a ferramenta faz por você depois.

## 2. O back-end que já está pronto: repositório e controlador

### 2.1 O repositório da Aula 13, revisto em três linhas

O `data/repositorio.js` já existe desde a Aula 13 e **não muda hoje**. Relembre o essencial: ele é o único arquivo do projeto que sabe onde os produtos moram, exporta `lerTodos()`, `salvarTodos(lista)` e `proximoId(lista)`, resolve o caminho com `path.join(__dirname, 'produtos.json')` e usa `node:fs/promises`. Nenhuma das três funções menciona `res`, `req` ou status HTTP — é isso que permitirá trocar o arquivo JSON por um banco de dados no Nível 3 reescrevendo só esse arquivo.

Um detalhe daquele arquivo que vale reter, porque volta a importar hoje: `proximoId` usa o maior id existente **mais um**, e não `lista.length + 1`. Com `length + 1`, basta excluir um produto do meio para o próximo cadastro reaproveitar um id já usado — e a tela passa a ter dois cards com a mesma chave.

### 2.2 O controlador da Aula 13 é o contrato que o front vai consumir

O `controllers/produtosController.js` também **não é reescrito**. Vale a pena reler o que ele já faz, porque cada item desta lista vira uma funcionalidade da tela de hoje:

| O que o controlador da Aula 13 já entrega | O que a tela de hoje faz com isso |
|---|---|
| `?q=` com `normalizar` (sem acento, sem caixa) | O campo de busca com `debounce` |
| `?categoria=` validado pela lista branca | O `<select>` de categoria |
| `?ordenar=preco` / `-preco` / `nome` | O `<select>` de ordenação |
| Campo `imagem` no objeto salvo | A foto do card |
| `400` para id que não é inteiro positivo | Mensagem clara em vez de "não encontrado" |
| `400` com `detalhes: [{ campo, mensagem }]` | A mensagem embaixo do `<input>` certo |
| `201` com cabeçalho `Location` | A confirmação do cadastro |
| `204` sem corpo no `DELETE` | O card que some sem erro no console |

E as rotas continuam as da Aula 14 — leitura pública, escrita protegida:

`cafe-cerrado-api/routes/produtos.js`

```js
const express = require("express");
const controlador = require("../controllers/produtosController");
const exigirLogin = require("../middlewares/exigirLogin");

const router = express.Router();

router.get("/", controlador.listar); // leitura pública
router.get("/:id", controlador.obter);
router.post("/", exigirLogin, controlador.criar); // escrita exige login
router.put("/:id", exigirLogin, controlador.atualizar);
router.delete("/:id", exigirLogin, controlador.remover);

module.exports = router;
```

> **⚠️ Atenção**
> Resista à tentação de "simplificar" o controlador para escrever o front mais rápido — trocar `detalhes: [{ campo, mensagem }]` por um array de strings, deixar cair o `?categoria=` ou aceitar qualquer categoria. Cada uma dessas simplificações apaga uma funcionalidade da tela que você vai construir hoje, e o desafio ⭐⭐ desta aula cobra exatamente o formato de erro que você teria jogado fora.

Nada muda no back-end hoje. O trabalho da aula inteira acontece em `public/`.

### 2.3 Por que gravar em duas etapas

`fs.writeFile` não é instantâneo. Para um arquivo de 300 KB, o sistema operacional pode truncar o arquivo antigo, começar a escrever o novo conteúdo e — se o processo morrer nesse instante (você apertou <kbd>Ctrl</kbd>+<kbd>C</kbd>, a máquina reiniciou, o `--watch` recarregou) — deixar no disco um JSON pela metade. Na próxima leitura, `JSON.parse` lança `Unexpected end of JSON input` e o cardápio inteiro se perde.

O truque do arquivo temporário resolve isso:

1. Escreve todo o conteúdo em `produtos.json.tmp`. Se morrer aqui, o `produtos.json` original continua intacto.
2. Renomeia `produtos.json.tmp` para `produtos.json`. No mesmo sistema de arquivos, o `rename` é **atômico**: ou o nome aponta para o arquivo antigo, ou aponta para o novo. Nunca para um meio-termo.

> **🔎 Por baixo do capô**
> A atomicidade do `rename` não é gentileza do Node: é garantia do POSIX, o padrão que rege os sistemas Unix. Renomear um arquivo é trocar uma entrada no diretório, uma operação que o sistema de arquivos trata como indivisível. É o mesmo mecanismo que bancos de dados, editores de texto e o próprio `git` usam para nunca deixarem um arquivo pela metade. Bancos de dados de verdade vão além, com *journaling* e *write-ahead log*, mas o princípio é este.

> **🧠 Você sabia?**
> O JSON que você está gravando aqui nasceu como um efeito colateral do JavaScript: Douglas Crockford formalizou o formato em 2001 a partir da sintaxe de objeto literal da linguagem, sem inventar nada novo — e por isso ele pegou. A ironia é que hoje `JSON.parse` é **mais rápido** que escrever o mesmo objeto direto no código: o motor V8 sabe que um texto JSON tem gramática fechada e o lê de uma vez, enquanto um literal de objeto precisa passar pelo parser completo de JavaScript. Times de front-end grandes exploram isso para carregar dados de configuração, e é por isso que sempre tratamos dados como texto a ser interpretado, nunca como código a ser executado.

> **🔬 Investigue**
> Com o servidor rodando, abra `data/produtos.json` no VS Code e deixe-o visível ao lado do navegador. Agora cadastre um produto pela API (via `testes.http`, ainda) e observe: o arquivo muda sozinho, na sua frente. Em seguida, rode `echo '[{ "id": 1,' > data/produtos.json` para corromper o arquivo de propósito e recarregue `GET /api/produtos`. Qual mensagem exata aparece no terminal? Em que linha do `repositorio.js` ela nasce? Restaure com `echo "[]" > data/produtos.json` e siga em frente — agora você reconhece esse erro em um segundo.

## 3. Uma camada de API no cliente

### 3.1 O problema do `fetch` espalhado

Sem organização, o CRUD do front vira isto: cinco `fetch` diferentes, cada um com o seu `headers`, o seu `if (!resposta.ok)`, o seu `JSON.stringify`. No dia em que a API passar a exigir um cabeçalho novo, você precisa lembrar de todos os cinco. No dia em que o tratamento de erro melhorar, idem.

Concentre tudo numa função. É o mesmo raciocínio do repositório do back, aplicado ao cliente.

### 3.2 A função `requisitar()`

`cafe-cerrado-api/public/js/api.js`

```js
// Camada de acesso à API. Todo fetch do projeto passa por aqui: é o único
// lugar que conhece cabeçalhos, token e formato de erro do servidor.
import { obterToken } from "./auth.js";

const BASE = "/api/produtos";

// Erro com status: quem chamou consegue reagir diferente a 401, 404 e 400.
export class ErroDeApi extends Error {
  constructor(mensagem, status, detalhes = []) {
    super(mensagem);
    this.name = "ErroDeApi";
    this.status = status;
    this.detalhes = detalhes;
  }
}

async function requisitar(url, opcoes = {}) {
  const cabecalhos = { "Content-Type": "application/json" };
  const token = obterToken();
  if (token) cabecalhos.Authorization = `Bearer ${token}`;

  let resposta;
  try {
    resposta = await fetch(url, { ...opcoes, headers: cabecalhos });
  } catch (falhaDeRede) {
    // fetch só rejeita quando a requisição nem chegou a ser respondida:
    // servidor parado, DNS errado, sem rede. Erro 404 ou 500 NÃO cai aqui.
    console.error("Falha de rede:", falhaDeRede);
    throw new ErroDeApi("Sem resposta do servidor. O npm run dev está rodando?", 0);
  }

  if (resposta.status === 401) {
    throw new ErroDeApi("Faça login com o Google para continuar.", 401);
  }

  if (!resposta.ok) {
    // O servidor respondeu com erro. Tenta ler a mensagem que ele mandou;
    // se o corpo não for JSON (uma página de erro em HTML, por exemplo),
    // o catch devolve um objeto vazio e caímos na mensagem genérica.
    const corpo = await resposta.json().catch(() => ({}));
    throw new ErroDeApi(corpo.erro || `Erro HTTP ${resposta.status}`, resposta.status, corpo.detalhes ?? []);
  }

  // 204 = sem corpo. Chamar resposta.json() aqui lançaria
  // "Unexpected end of JSON input".
  if (resposta.status === 204) return null;
  return resposta.json();
}

export const api = {
  listar(filtros = {}) {
    const parametros = new URLSearchParams();
    for (const [chave, valor] of Object.entries(filtros)) {
      if (valor !== "" && valor !== null && valor !== undefined) {
        parametros.set(chave, valor);
      }
    }
    const consulta = parametros.toString();
    return requisitar(consulta ? `${BASE}?${consulta}` : BASE);
  },
  obter(id) {
    return requisitar(`${BASE}/${id}`);
  },
  criar(dados) {
    return requisitar(BASE, { method: "POST", body: JSON.stringify(dados) });
  },
  atualizar(id, dados) {
    return requisitar(`${BASE}/${id}`, { method: "PUT", body: JSON.stringify(dados) });
  },
  remover(id) {
    return requisitar(`${BASE}/${id}`, { method: "DELETE" });
  },
};
```

Três decisões desse arquivo valem uma pausa para pensar — ou discutir, se você estiver estudando em grupo:

- **`fetch` não rejeita em erro HTTP.** Um `404` ou um `500` são respostas válidas: a promessa resolve normalmente, com `resposta.ok === false`. O `try/catch` em volta do `fetch` só pega falha de rede. Quem esquece disso escreve código que "funciona" mesmo quando o servidor recusou tudo.
- **Erro com status.** Uma `Error` comum só carrega a mensagem. A `ErroDeApi` carrega também o `status` e os `detalhes` da validação, e é isso que permite à tela reagir de formas diferentes a `401` (peça login) e a `400` (mostre o que está errado no formulário).
- **O token vem do módulo de autenticação, não é passado por parâmetro.** Quem chama `api.criar(dados)` não precisa nem saber que existe token. Se amanhã a sessão mudar de mecanismo, muda só o `auth.js`.

### 3.3 O módulo de autenticação, agora com ouvintes

O `auth.js` da Aula 14 já faz o essencial: pede o Client ID a `GET /api/config`, chama `google.accounts.id.initialize`, troca a credencial do Google por uma **sessão própria** em `POST /api/auth/google` e guarda `{ usuario, token }` no `sessionStorage`. Nada disso muda — mudar seria quebrar a autenticação inteira.

O que falta é uma interface para o resto da aplicação: hoje `api.js` precisa do token e `app.js` precisa saber quando alguém entra ou sai. A Aula 14 avisava com um `CustomEvent`; vamos trocar o evento por três funções exportadas, que é mais explícito e mais fácil de testar.

A marcação do cabeçalho é a mesma da Aula 14, sem uma linha a mais:

`trecho de public/index.html — dentro de <header>`

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

> **⚠️ Atenção**
> Repare no que **não** está aqui: nenhum `data-client_id`, nenhum `data-callback`, nenhum `<div id="g_id_onload">`. O Client ID mora no `.env` do servidor e chega ao navegador por `GET /api/config`; o callback é passado por JavaScript em `google.accounts.id.initialize`. Se você encontrar um tutorial mandando colar o Client ID no HTML, saiba que ele funciona — e que você passa a ter a mesma configuração em dois lugares, que um dia vão divergir. Uma fonte só: o `.env`.

`cafe-cerrado-api/public/js/auth.js`

```js
// Sessão do usuário no cliente.
// O token guardado aqui é o token de SESSÃO emitido pela nossa API
// (HMAC, 8 horas, Aula 14) — nunca o ID token do Google, que é usado
// uma única vez, no login, e descartado em seguida.
const CHAVE_SESSAO = "cafe-cerrado-sessao";

const areaLogin = document.querySelector("#area-login");
const areaUsuario = document.querySelector("#area-usuario");
const nomeUsuario = document.querySelector("#nome-usuario");
const fotoUsuario = document.querySelector("#foto-usuario");
const botaoSair = document.querySelector("#btn-sair");
const aviso = document.querySelector("#aviso-login");

const ouvintes = [];

function lerSessao() {
  const bruto = sessionStorage.getItem(CHAVE_SESSAO);
  if (!bruto) return null;
  try {
    return JSON.parse(bruto);
  } catch (erro) {
    sessionStorage.removeItem(CHAVE_SESSAO);
    return null;
  }
}

export function obterToken() {
  return lerSessao()?.token ?? null;
}

export function obterUsuario() {
  return lerSessao()?.usuario ?? null;
}

// Quem quiser reagir a login/logout registra uma função aqui. É chamada
// imediatamente com o estado atual e de novo a cada mudança.
export function aoMudarSessao(callback) {
  ouvintes.push(callback);
  callback(obterUsuario());
}

function avisarOuvintes() {
  for (const ouvinte of ouvintes) ouvinte(obterUsuario());
}

function pintarAreaDoUsuario() {
  const usuario = obterUsuario();

  if (usuario) {
    nomeUsuario.textContent = usuario.nome;
    fotoUsuario.src = usuario.foto;
  }

  areaUsuario.hidden = !usuario;
  areaLogin.hidden = Boolean(usuario);
}

// Chamada pelo Google quando o login termina com sucesso.
async function aoReceberCredencial(resposta) {
  aviso.textContent = "Entrando…";

  const requisicao = await fetch("/api/auth/google", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    // O back-end da Aula 14 espera o campo credential com o ID token do Google.
    body: JSON.stringify({ credential: resposta.credential }),
  });

  if (!requisicao.ok) {
    const corpo = await requisicao.json().catch(() => ({}));
    aviso.textContent = corpo.erro ?? "Não foi possível entrar. Tente de novo.";
    return;
  }

  // A resposta é { usuario, token }: os dois campos vão inteiros para o
  // sessionStorage, e é o "token" daqui que vai no cabeçalho Authorization.
  const sessao = await requisicao.json();
  sessionStorage.setItem(CHAVE_SESSAO, JSON.stringify(sessao));

  aviso.textContent = "";
  pintarAreaDoUsuario();
  avisarOuvintes();
}

export function sair() {
  sessionStorage.removeItem(CHAVE_SESSAO);
  window.google?.accounts?.id?.disableAutoSelect(); // impede o login automático na volta
  aviso.textContent = "Você saiu da sua conta.";
  pintarAreaDoUsuario();
  avisarOuvintes();
}

async function iniciar() {
  const configuracao = await fetch("/api/config").then((r) => r.json());

  google.accounts.id.initialize({
    client_id: configuracao.googleClientId,
    callback: aoReceberCredencial,
  });

  google.accounts.id.renderButton(document.querySelector("#botao-google"), {
    type: "standard",
    theme: "outline",
    size: "large",
    text: "signin_with",
    locale: "pt-BR",
  });

  pintarAreaDoUsuario();   // recarregar a página mantém a sessão
  avisarOuvintes();
}

botaoSair.addEventListener("click", sair);

// O script do Google carrega com "async": pode chegar antes ou depois deste módulo.
if (window.google?.accounts?.id) {
  iniciar();
} else {
  window.onGoogleLibraryLoad = iniciar;
}
```

Três decisões que valem discussão:

- **`obterToken()` devolve o token da nossa sessão, não a credencial do Google.** O ID token do Google prova quem você é *para o Google*; ele é verificado uma vez, no `POST /api/auth/google`, e depois some. O que viaja em todo `Authorization: Bearer …` é o token HMAC que o seu servidor assinou, e é ele que o `exigirLogin` sabe conferir. Mandar o ID token no lugar dele resulta em `401` em **toda** escrita — é o erro mais caro que dá para cometer nesta unidade.
- **O estado mora no `sessionStorage`, não em variáveis do módulo.** Guardar em `let usuarioLogado` funciona até a primeira tecla <kbd>F5</kbd>, quando o módulo é recarregado do zero e a pessoa "desloga sozinha". Lendo do `sessionStorage` a cada chamada, recarregar a página mantém a sessão — que é o que a Aula 14 prometeu.
- **`window.google?.accounts?.id?.` com encadeamento opcional.** O script da GSI é `async`: se alguém clicar em "Sair" antes de ele terminar de baixar, `google` ainda não existe e um `ReferenceError` deixaria a pessoa presa na sessão.

## 4. Estado, render e os quatro estados da tela

### 4.1 Uma única fonte de verdade

A tela do cardápio tem três variáveis de estado e nada mais:

```js
let produtos = [];      // o que a API devolveu na última carga
let carregando = false; // há requisição em andamento?
let erroAtual = null;   // mensagem do último erro, ou null
```

Toda função que muda uma dessas três chama `renderizar()` no fim. Nenhuma função além de `renderizar()` toca no DOM da lista. Essa disciplina — parece exagerada em 200 linhas de código — é o que impede a tela de mentir.

### 4.2 Os quatro estados

Uma tela que depende de rede nunca tem dois estados ("tem dado" / "não tem"). Tem quatro, e ignorar qualquer um deles produz uma interface que trava sem explicação:

| Estado | Quando acontece | O que o usuário vê |
|---|---|---|
| Carregando | Requisição em andamento | "Carregando o cardápio…" |
| Erro | A API falhou ou a rede caiu | Mensagem do erro e botão "Tentar de novo" |
| Vazio | Sucesso, mas zero registros | "Nenhum produto cadastrado ainda" |
| Conteúdo | Sucesso, com registros | Os cards |

O estado **vazio** merece um cuidado especial: ele precisa distinguir "não há nada cadastrado" de "sua busca não achou nada". São situações diferentes, e a segunda pede um caminho de saída ("limpar busca").

### 4.3 `textContent`, nunca `innerHTML`, para dados do servidor

Você viu isso na Aula 07 e vale repetir agora que os dados vêm de fora: montar HTML por concatenação de strings com conteúdo que o usuário digitou é o caminho mais curto para um XSS.

```js
// Perigoso: se alguém cadastrar um produto chamado
// <img src=x onerror="alert(document.cookie)">, o navegador executa.
card.innerHTML = `<h3>${produto.nome}</h3>`;

// Seguro: textContent escreve texto, nunca marcação.
const titulo = document.createElement("h3");
titulo.textContent = produto.nome;
card.appendChild(titulo);
```

`innerHTML = ""` para limpar um container é seguro (não há dado do usuário ali) e é o que usaremos. O perigo está em **inserir** dados externos como HTML.

## 5. Um formulário para criar e editar

### 5.1 O padrão do modo edição

Manter dois formulários — um de cadastro e um de edição — significa manter dois HTML, duas validações e dois manipuladores de `submit` em sincronia. O padrão profissional é um formulário só, com um campo oculto guardando o id:

- campo `id` **vazio** → o `submit` chama `api.criar()`;
- campo `id` **preenchido** → o `submit` chama `api.atualizar(id, dados)`.

O botão muda de rótulo ("Adicionar" ↔ "Salvar alterações") e um botão "Cancelar" aparece para sair do modo edição.

`trecho de public/index.html — dentro de <main>`

```html
<section id="area-gestao" aria-labelledby="titulo-gestao" hidden>
  <h2 id="titulo-gestao">Gerenciar cardápio</h2>

  <form id="form-produto" novalidate>
    <input type="hidden" name="id">

    <div class="campo">
      <label for="nome">Nome</label>
      <input id="nome" name="nome" type="text" required minlength="3" autocomplete="off">
    </div>

    <div class="campo">
      <label for="preco">Preço (R$)</label>
      <input id="preco" name="preco" type="number" step="0.01" min="0" required>
    </div>

    <div class="campo">
      <label for="categoria">Categoria</label>
      <input id="categoria" name="categoria" type="text" list="categorias" placeholder="cafes">
      <datalist id="categorias">
        <option value="cafes"></option>
        <option value="geladas"></option>
        <option value="salgados"></option>
        <option value="doces"></option>
      </datalist>
    </div>

    <div class="campo">
      <label for="descricao">Descrição</label>
      <textarea id="descricao" name="descricao" rows="2"></textarea>
    </div>

    <div class="acoes">
      <button type="submit" id="btn-salvar">Adicionar</button>
      <button type="button" id="btn-cancelar" hidden>Cancelar</button>
    </div>
  </form>
</section>

<p id="feedback" class="feedback" role="status" aria-live="polite"></p>
```

O `novalidate` desliga as bolhas de validação nativa do navegador para que a mensagem apareça no nosso `#feedback` — mas os atributos `required` e `minlength` continuam ali, disponíveis para `form.checkValidity()`. É o meio-termo entre a validação nativa da Aula 03 e o controle total do JavaScript.

### 5.2 A armadilha do `form.id`

Um detalhe que derruba muita gente: dentro de um `<form>`, você acessa os campos pelo `name` (`form.nome`, `form.preco`). Mas `id` **não funciona assim**.

```js
const form = document.querySelector("#form-produto");

console.log(form.id);        // "form-produto"  ← o atributo id do FORMULÁRIO
console.log(form.id.value);  // undefined       ← e aqui o código quebra

console.log(form.elements.id.value); // ""      ← o campo oculto, correto
```

`id`, `name`, `action`, `method`, `children` e `length` são propriedades que o próprio `HTMLFormElement` já possui — elas vencem os campos de mesmo nome. Por isso, neste projeto, **sempre** acesse campos por `form.elements.<nome>`. É mais longo e nunca surpreende.

### 5.3 Validação nos dois lados

A validação do navegador é conveniência: ela evita uma ida ao servidor e dá resposta instantânea. A validação do servidor é segurança: é a única que um `curl` não consegue pular. As duas coexistem, e nenhuma substitui a outra.

Quando o servidor devolve `400`, ele manda também os `detalhes` — e é responsabilidade da tela mostrá-los, não engoli-los. Lembre do formato do controlador da Aula 13: cada item é um objeto `{ campo, mensagem }`, não uma string solta.

```js
try {
  await api.criar(dados);
} catch (erro) {
  // erro.detalhes vem do { erro, detalhes } do controlador (seção 2.2):
  // [{ campo: "nome", mensagem: "O nome precisa ter ao menos 3 caracteres." }, …]
  const extra = erro.detalhes?.length
    ? ` (${erro.detalhes.map((d) => `${d.campo}: ${d.mensagem}`).join("; ")})`
    : "";
  avisar(`${erro.message}${extra}`, "erro");
}
```

Isso já é melhor que engolir o erro, mas ainda é o mínimo: com o `campo` em mãos, dá para pendurar cada mensagem embaixo do `<input>` culpado. É exatamente o desafio ⭐⭐ desta aula.

## 6. Excluir sem susto: confirmação e feedback acessível

Exclusão é a única operação irreversível do CRUD. Três cuidados mínimos:

**1. Confirmar antes.** `confirm()` resolve por hoje: é uma linha, é acessível por padrão e é bloqueante — o código só continua depois da decisão.

```js
if (!confirm(`Excluir "${produto.nome}"? Esta ação não pode ser desfeita.`)) return;
```

A limitação é séria: `confirm()` congela a aba inteira, não é estilizável e está em desuso em aplicações reais. O caminho moderno é o elemento `<dialog>` com `showModal()`, que já é o desafio ⭐⭐⭐ desta aula.

**2. Anunciar o resultado.** O parágrafo `#feedback` tem `role="status"` e `aria-live="polite"`: quando o seu texto muda, o leitor de tela anuncia a mensagem sem interromper o que estava lendo. É a mesma técnica da Aula 06, agora valendo para o full-stack. Sem isso, quem navega por leitor de tela clica em "Excluir" e não recebe nenhuma confirmação de que algo aconteceu.

**3. Cuidar do foco.** Ao excluir um card, o botão que tinha o foco deixa de existir — e o foco volta para o `<body>`, jogando o usuário de teclado para o topo da página. Depois de recarregar a lista, devolva o foco a um ponto previsível (o campo de busca ou o título da seção).

> **💡 Dica**
> Quer saber se o seu feedback funciona mesmo? Desligue o monitor, ligue o leitor de tela (NVDA no Windows, Orca no Linux, VoiceOver no macOS com <kbd>Cmd</kbd>+<kbd>F5</kbd>) e tente cadastrar um produto só com o teclado. Cinco minutos desse exercício ensinam mais sobre acessibilidade do que uma aula inteira.

## 7. O caminho completo de um "Salvar"

Vale parar um minuto e olhar o que você construiu. Cada clique em "Adicionar" percorre, em ordem, tudo o que foi estudado até aqui:

1. **HTML e CSS (Unidade 1)** — o formulário semântico, com `<label for>`, estados de foco visíveis e layout responsivo.
2. **JavaScript no cliente (Unidade 2)** — `submit` interceptado com `preventDefault()`, dados lidos do formulário, `fetch` com `async/await`.
3. **HTTP (Aula 01)** — uma requisição `POST /api/produtos`, com `Content-Type: application/json`, `Authorization: Bearer …` e o corpo serializado.
4. **Express (Aulas 11–13)** — a cadeia de middlewares: `express.json()` → log → `exigirLogin` → rota → controlador.
5. **Autenticação (Aula 14)** — o `exigirLogin` confere a assinatura HMAC do token de **sessão** e preenche `req.usuario`. (O `google-auth-library` já fez o trabalho dele uma única vez, lá no login.)
6. **Validação e persistência (hoje)** — o controlador valida, o repositório grava em disco de forma atômica, o servidor responde `201`.
7. **De volta ao cliente** — `api.criar()` resolve, o estado é atualizado, `renderizar()` redesenha a lista e o `aria-live` anuncia "Produto criado".

Sete camadas, uma requisição, nenhum recarregamento de página. Isso é uma aplicação web moderna — e é exatamente o esqueleto de qualquer sistema que você vai encontrar no mercado.

## 🧩 Padrão de projeto em uso — Repository e Fachada

Dois padrões clássicos apareceram hoje, um em cada ponta:

**Repository (back-end).** O `data/repositorio.js` é um repositório: ele oferece uma coleção de objetos em memória (`lerTodos`, `salvarTodos`) e esconde completamente **onde** e **como** esses objetos são guardados. O controlador pede "todos os produtos" e não sabe se vieram de um JSON, de um MySQL ou de uma API remota. O teste do padrão é este: para migrar o Café Cerrado para um banco de dados, quantos arquivos você precisa abrir? Um.

**Fachada / Facade (front-end).** O objeto `api` do `public/js/api.js` é uma fachada: uma interface simples (`api.criar(dados)`) na frente de um subsistema chato (montar URL, serializar JSON, anexar token, interpretar status, extrair mensagem de erro). Quem usa a fachada escreve uma linha; quem a mantém concentra a complexidade num lugar só.

Repare que os dois padrões resolvem o mesmo problema com o mesmo remédio: **isolar o que muda**. É essa a ideia por trás da arquitetura em camadas que você vem construindo desde a Aula 12 — e é o assunto central do Nível 3, onde padrões de projeto viram conteúdo de ementa.

## 💻 Mão na massa — o cardápio do Café Cerrado vira administrável

Ao final destes passos, qualquer pessoa logada com uma conta Google consegue cadastrar, editar e excluir produtos do Café Cerrado pela interface, e os dados sobrevivem ao reinício do servidor.

**Passo 1 — confirme o back-end, sem escrever nada.** Nada muda no servidor hoje. Só confirme que as peças das Aulas 13 e 14 estão no lugar:

```bash
cd cafe-cerrado-api
ls data/ controllers/ middlewares/
# esperado em data/:        produtos.json  repositorio.js
# esperado em controllers/: produtosController.js  authController.js
# esperado em middlewares/: registro.js  erros.js  exigirLogin.js
```

**Passo 2 — confirme a API pelo `testes.http`,** antes de tocar no front. Este é o hábito que separa depurar de adivinhar: se a API está certa, todo problema que aparecer depois é do cliente.

`cafe-cerrado-api/testes.http`

```http
@base = http://localhost:3000/api
@token = cole-aqui-o-token-de-sessao

### listar tudo
GET {{base}}/produtos

### buscar por termo, sem acento e sem caixa (acha o "Frappê de Café")
GET {{base}}/produtos?q=cafe

### filtrar e ordenar (só os doces, do mais barato ao mais caro)
GET {{base}}/produtos?categoria=doces&ordenar=preco

### criar sem token — deve responder 401
POST {{base}}/produtos
Content-Type: application/json

{ "nome": "Teste sem token", "categoria": "cafes", "preco": 1 }

### criar com token — deve responder 201
POST {{base}}/produtos
Content-Type: application/json
Authorization: Bearer {{token}}

{ "nome": "Suco de Cupuaçu", "categoria": "geladas", "preco": 10.5, "descricao": "Polpa batida com água gelada e um fio de mel.", "imagem": "img/suco-cupuacu.jpg" }

### corpo inválido — deve responder 400 com detalhes [{ campo, mensagem }]
POST {{base}}/produtos
Content-Type: application/json
Authorization: Bearer {{token}}

{ "nome": "ab", "categoria": "sobremesa", "preco": "muito caro" }

### excluir o produto criado acima — deve responder 204 sem corpo
DELETE {{base}}/produtos/11
Authorization: Bearer {{token}}
```

Para preencher o `@token`: faça login no site, abra o console do navegador e rode

```js
JSON.parse(sessionStorage.getItem("cafe-cerrado-sessao")).token
```

Copie o valor **sem as aspas** e cole na variável. É o mesmo procedimento da Aula 14 — e é o token de **sessão**, o que o seu servidor assinou, válido por 8 horas. O ID token do Google não serve aqui: o `exigirLogin` confere a assinatura HMAC da sua própria API e responderia `401` para qualquer outra coisa.

**Passo 3 — atualize o `auth.js`** para a versão com ouvintes da seção 3.3.

**Passo 4 — crie a camada de API do cliente:** `public/js/api.js`, com o conteúdo da seção 3.2.

**Passo 5 — acrescente a área de gestão ao HTML.** Cole o trecho da seção 5.1 dentro do `<main>` de `public/index.html`, logo acima da lista do cardápio, e confirme que a busca e o container da lista existem com estes ids:

`trecho de public/index.html — dentro de <main>`

```html
<section aria-labelledby="titulo-cardapio">
  <h2 id="titulo-cardapio">Cardápio</h2>

  <div class="campo">
    <label for="busca">Buscar no cardápio</label>
    <input id="busca" name="busca" type="search" placeholder="café, bolo, pão…">
  </div>

  <div id="lista-produtos" class="grade-produtos"></div>
</section>
```

Se a sua página já tinha um campo de busca da Aula 08 com outro id, mantenha o seu e ajuste o seletor no `app.js` — o que não pode é ter dois campos de busca disputando a mesma lista.

Troque a tag do script principal para módulo:

`trecho de public/index.html — antes de </body>`

```html
<script src="https://accounts.google.com/gsi/client" async defer></script>
<script type="module" src="js/app.js"></script>
```

`type="module"` já se comporta como `defer` (o script só roda depois do HTML estar montado), então o atributo `defer` é ignorado ali e não precisa ser escrito.

**Passo 6 — escreva o `app.js` completo.**

`cafe-cerrado-api/public/js/app.js`

```js
import { api } from "./api.js";
import { aoMudarSessao, obterUsuario } from "./auth.js";

// ---------- elementos da tela ----------
const listaEl = document.querySelector("#lista-produtos");
const formEl = document.querySelector("#form-produto");
const feedbackEl = document.querySelector("#feedback");
const buscaEl = document.querySelector("#busca");
const areaGestaoEl = document.querySelector("#area-gestao");
const btnSalvarEl = document.querySelector("#btn-salvar");
const btnCancelarEl = document.querySelector("#btn-cancelar");

// ---------- estado: a única fonte de verdade da tela ----------
let produtos = [];
let carregando = false;
let erroAtual = null;

const moeda = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });

// ---------- feedback acessível ----------
function avisar(mensagem, tipo = "sucesso") {
  feedbackEl.textContent = mensagem;
  feedbackEl.className = `feedback feedback--${tipo}`;
}

// ---------- render ----------
function paragrafoDeEstado(texto) {
  const p = document.createElement("p");
  p.className = "estado-lista";
  p.textContent = texto;
  return p;
}

function criarCard(produto) {
  const card = document.createElement("article");
  card.className = "card-produto";
  card.dataset.id = produto.id;

  const titulo = document.createElement("h3");
  titulo.textContent = produto.nome;

  const preco = document.createElement("p");
  preco.className = "preco";
  preco.textContent = moeda.format(produto.preco);

  const descricao = document.createElement("p");
  descricao.className = "descricao";
  descricao.textContent = produto.descricao || "Sem descrição.";

  const categoria = document.createElement("p");
  categoria.className = "categoria";
  categoria.textContent = produto.categoria;

  card.append(titulo, preco, categoria, descricao);

  // Botões de escrita só para quem está logado. Isso é conforto de interface:
  // quem protege de verdade é o middleware exigirLogin, no servidor.
  if (obterUsuario()) {
    const acoes = document.createElement("div");
    acoes.className = "acoes-card";

    const btnEditar = document.createElement("button");
    btnEditar.type = "button";
    btnEditar.textContent = "Editar";
    btnEditar.setAttribute("aria-label", `Editar ${produto.nome}`);
    btnEditar.addEventListener("click", () => entrarEmModoEdicao(produto));

    const btnExcluir = document.createElement("button");
    btnExcluir.type = "button";
    btnExcluir.className = "perigo";
    btnExcluir.textContent = "Excluir";
    btnExcluir.setAttribute("aria-label", `Excluir ${produto.nome}`);
    btnExcluir.addEventListener("click", () => excluirProduto(produto));

    acoes.append(btnEditar, btnExcluir);
    card.appendChild(acoes);
  }

  return card;
}

function renderizar() {
  listaEl.innerHTML = "";

  if (carregando) {
    listaEl.appendChild(paragrafoDeEstado("Carregando o cardápio…"));
    return;
  }

  if (erroAtual) {
    listaEl.appendChild(paragrafoDeEstado(erroAtual));
    const botao = document.createElement("button");
    botao.type = "button";
    botao.textContent = "Tentar de novo";
    botao.addEventListener("click", carregarProdutos);
    listaEl.appendChild(botao);
    return;
  }

  if (produtos.length === 0) {
    const houveBusca = buscaEl.value.trim() !== "";
    listaEl.appendChild(
      paragrafoDeEstado(
        houveBusca
          ? `Nada encontrado para "${buscaEl.value.trim()}".`
          : "Nenhum produto cadastrado ainda."
      )
    );
    return;
  }

  // Monta tudo fora da árvore e insere de uma vez: um único reflow.
  const fragmento = document.createDocumentFragment();
  for (const produto of produtos) fragmento.appendChild(criarCard(produto));
  listaEl.appendChild(fragmento);
}

// ---------- operações ----------
async function carregarProdutos() {
  carregando = true;
  erroAtual = null;
  renderizar();

  try {
    produtos = await api.listar({ q: buscaEl.value.trim() });
  } catch (erro) {
    produtos = [];
    erroAtual = erro.message;
  } finally {
    carregando = false;
    renderizar();
  }
}

function entrarEmModoEdicao(produto) {
  formEl.elements.id.value = produto.id;
  formEl.elements.nome.value = produto.nome;
  formEl.elements.preco.value = produto.preco;
  formEl.elements.categoria.value = produto.categoria ?? "";
  formEl.elements.descricao.value = produto.descricao ?? "";
  btnSalvarEl.textContent = "Salvar alterações";
  btnCancelarEl.hidden = false;
  formEl.elements.nome.focus();
  avisar(`Editando "${produto.nome}".`, "info");
}

function sairDoModoEdicao() {
  formEl.reset();
  formEl.elements.id.value = "";
  btnSalvarEl.textContent = "Adicionar";
  btnCancelarEl.hidden = true;
}

async function excluirProduto(produto) {
  if (!confirm(`Excluir "${produto.nome}"? Esta ação não pode ser desfeita.`)) return;

  try {
    await api.remover(produto.id);
    avisar(`"${produto.nome}" foi excluído.`);
    await carregarProdutos();
    buscaEl.focus(); // o botão clicado sumiu: devolve o foco a um ponto estável
  } catch (erro) {
    avisar(erro.message, "erro");
  }
}

// ---------- eventos ----------
formEl.addEventListener("submit", async (evento) => {
  evento.preventDefault();

  if (!formEl.checkValidity()) {
    avisar("Preencha nome (3 letras ou mais) e preço.", "erro");
    formEl.elements.nome.focus();
    return;
  }

  const id = formEl.elements.id.value;
  const dados = {
    nome: formEl.elements.nome.value.trim(),
    preco: Number(formEl.elements.preco.value), // o input devolve string!
    categoria: formEl.elements.categoria.value.trim(),
    descricao: formEl.elements.descricao.value.trim(),
  };

  btnSalvarEl.disabled = true; // evita duplo clique criando dois registros
  try {
    if (id) {
      await api.atualizar(id, dados);
      avisar(`"${dados.nome}" foi atualizado.`);
    } else {
      await api.criar(dados);
      avisar(`"${dados.nome}" foi criado.`);
    }
    sairDoModoEdicao();
    await carregarProdutos();
  } catch (erro) {
    const extra = erro.detalhes?.length ? ` (${erro.detalhes.join("; ")})` : "";
    avisar(`${erro.message}${extra}`, "erro");
  } finally {
    btnSalvarEl.disabled = false;
  }
});

btnCancelarEl.addEventListener("click", () => {
  sairDoModoEdicao();
  avisar("Edição cancelada.", "info");
});

// Busca com atraso: só consulta a API 400 ms depois da última tecla.
let temporizadorBusca = null;
buscaEl.addEventListener("input", () => {
  clearTimeout(temporizadorBusca);
  temporizadorBusca = setTimeout(carregarProdutos, 400);
});

// Login e logout mudam a interface: mostra/esconde o formulário e redesenha
// os cards (com ou sem botões de ação).
aoMudarSessao((usuario) => {
  areaGestaoEl.hidden = !usuario;
  if (!usuario) sairDoModoEdicao();
  renderizar();
});

carregarProdutos();
```

**Passo 7 — estilo mínimo para os estados.** Acrescente ao seu CSS (o arquivo que você mantém desde a Aula 04):

`cafe-cerrado-api/public/css/estilo.css`

```css
.feedback {
  min-height: 1.5rem;
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  font-weight: 600;
}

.feedback--sucesso {
  background: #e7f6ec;
  color: #14532d;
}

.feedback--erro {
  background: #fdecec;
  color: #7f1d1d;
}

.feedback--info {
  background: #eef2ff;
  color: #312e81;
}

.estado-lista {
  padding: 1.5rem;
  text-align: center;
  color: #57534e;
}

.card-produto .acoes-card {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.75rem;
}

.card-produto button.perigo {
  border-color: #b91c1c;
  color: #b91c1c;
}

button:disabled {
  opacity: 0.6;
  cursor: progress;
}
```

**Passo 8 — teste o ciclo completo.**

```bash
npm run dev
# abra http://localhost:3000 (NÃO abra o arquivo pelo disco)
```

**Como testar — o resultado esperado, passo a passo:**

1. Sem login, a lista carrega e nenhum botão "Editar"/"Excluir" aparece; a área de gestão está oculta.
2. Faça login com o Google: seu nome e sua foto aparecem, o formulário aparece e os cards ganham os botões.
3. Cadastre "Torta de Limão", `9.90`, categoria `doces`. O feedback anuncia a criação e o card aparece na lista **sem recarregar a página**. Na aba Network do DevTools: `POST /api/produtos` com status `201`.
4. Clique em "Editar" nesse card: o formulário se preenche, o botão vira "Salvar alterações" e o "Cancelar" aparece. Mude o preço para `10.50` e salve — `PUT` com `200`, card atualizado.
5. Digite `torta` na busca: a requisição só sai 400 ms depois da última tecla (confirme na aba Network) e a lista filtra — e traz também a "Torta de Frango", porque a busca do servidor casa por trecho do nome.
6. Exclua o produto e confirme no `confirm()`: `DELETE` com `204`, o card some, o feedback anuncia.
7. Derrube o servidor com <kbd>Ctrl</kbd>+<kbd>C</kbd>, suba de novo com `npm run dev` e recarregue: os produtos continuam lá. Abra `data/produtos.json` e confirme.
8. Saia da conta ("Sair"): os botões de escrita somem, a área de gestão se esconde e a listagem continua funcionando.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Por que `fetch("/api/produtos")` funciona sem nenhuma configuração de CORS neste projeto, enquanto o `fetch` da Aula 10 (JSONPlaceholder) dependia de um cabeçalho do servidor? Responda citando os três componentes de uma "origem".

**A2.** O que acontece se o servidor responder `204` e o cliente chamar `resposta.json()`? Qual mensagem exata aparece no console? Qual linha do `api.js` evita isso?

**A3.** Preveja a saída. Dado `const form = document.querySelector("#form-produto")` com um campo `<input type="hidden" name="id" value="7">`, o que imprime cada linha?

```js
console.log(form.id);
console.log(form.elements.id.value);
console.log(typeof form.elements.preco.value);
```

**A4.** Um `fetch` para `/api/produtos/999` recebeu `404`. A promessa do `fetch` **rejeita**? Justifique e diga qual é, então, o papel do `if (!resposta.ok)`.

**A5.** Leia o código abaixo e responda ao que se pede depois dele:

```js
async function excluir(id) {
  try {
    await api.remover(id);
    avisar("Excluído.");
  } catch (erro) {
    avisar(erro.message, "erro");
  }
}
```

Descreva, em duas frases, o que acontece na tela em cada um dos dois caminhos (sucesso e falha). Em seguida, diga o que muda de comportamento se a palavra `await` for apagada da linha do `api.remover(id)`.

**A6.** Cite os quatro estados de uma tela que depende de rede e escreva a mensagem que você mostraria em cada um, no seu projeto autoral.

**A7.** Por que `proximoId` usa `Math.max(...lista.map((p) => p.id)) + 1` em vez de `lista.length + 1`? Dê um exemplo concreto de sequência de operações que quebra a segunda opção.

**A8.** Qual é a diferença entre a gravação `fs.writeFile(ARQUIVO, dados)` e a sequência `writeFile(tmp) + rename(tmp, ARQUIVO)`? Em que cenário exato a segunda salva os seus dados?

**A9.** O que `evento.preventDefault()` impede no `submit` do formulário? O que aconteceria na tela sem essa linha?

**A10.** Explique por que `btnSalvarEl.disabled = true` antes da requisição e `false` no `finally` é melhor do que desabilitar o botão só depois da resposta.

### Nível B — Aplicação

**B1.** Acrescente ao cardápio um filtro por categoria: um `<select id="filtro-categoria">` preenchido dinamicamente com as categorias distintas dos produtos carregados, enviado à API como `?categoria=`. Implemente o filtro também no controlador `listar`, combinando-o com o `?q=` já existente.

**Resultado esperado:** escolher "doces" mostra só os doces; escolher "Todas" volta à lista inteira; buscar "bolo" com "doces" selecionado aplica os dois filtros juntos, e a URL da requisição na aba Network mostra `?q=bolo&categoria=doces`.

<details markdown="1">
<summary>Dica</summary>

Para as categorias distintas: `[...new Set(produtos.map((p) => p.categoria))].sort()`. Cuidado com a ordem de execução — se você preencher o `<select>` a partir da lista já filtrada, as opções somem conforme o usuário filtra. Guarde as categorias de uma carga sem filtro, ou crie um endpoint `GET /api/categorias`.
</details>

**B2.** Implemente um contador de caracteres para o campo "Descrição": limite de 140 caracteres, contador atualizado a cada tecla, e bloqueio do envio (com mensagem no `#feedback`) se o limite for ultrapassado. Adicione a mesma verificação na função `validar` do servidor.

**Resultado esperado:** o contador mostra "0/140" e vai subindo; ao passar de 140, ele fica vermelho e o `submit` é recusado com mensagem clara. Um `POST` com 200 caracteres pelo `testes.http` recebe `400` com o detalhe correspondente.

<details markdown="1">
<summary>Dica</summary>

O evento certo é `input` (dispara a cada tecla), não `change` (só ao sair do campo). Associe o contador ao campo com `aria-describedby` para que o leitor de tela o anuncie. No servidor, a checagem entra na mesma lista `erros` das outras regras — assim a mensagem chega ao front pelo `detalhes` sem nenhum código novo.
</details>

**B3.** Troque as escutas individuais dos botões de card por **delegação de eventos**: um único `addEventListener("click")` no `#lista-produtos`, usando `evento.target.closest("button")` e o `data-id` do card para descobrir qual produto foi clicado.

**Resultado esperado:** editar e excluir continuam funcionando exatamente igual, mas o `criarCard` fica mais curto e a lista passa a ter 1 listener em vez de 2 por produto. Confirme no painel Elements → Event Listeners do DevTools.

<details markdown="1">
<summary>Dica</summary>

Marque cada botão com `dataset.acao = "editar"` ou `"excluir"`. No listener: `const botao = evento.target.closest("button[data-acao]"); if (!botao) return;` e depois `const id = Number(botao.closest(".card-produto").dataset.id)`. Para achar o produto, `produtos.find((p) => p.id === id)`.
</details>

**B4.** Adicione um indicador de carregamento no próprio botão: enquanto a requisição de salvar estiver em andamento, o texto do botão vira "Salvando…" e volta ao normal no `finally`. Faça o mesmo para a exclusão, desabilitando os dois botões daquele card.

**Resultado esperado:** com o throttling "Slow 3G" ligado na aba Network, dá para ver o botão mudar de texto e voltar. Nenhum duplo clique cria dois registros.

<details markdown="1">
<summary>Dica</summary>

Guarde o texto original antes de trocar (`const rotulo = botao.textContent`) e restaure no `finally`. Cuidado: se você recarregar a lista no sucesso, o botão do card excluído nem existe mais — proteja o restore com uma verificação de que o elemento ainda está no documento (`botao.isConnected`).
</details>

### Nível C — Desafio

**C1.** Implemente o **desfazer** da exclusão: ao excluir um produto, em vez de sumir para sempre, o feedback exibe "Produto excluído · Desfazer" por 6 segundos. Clicar em "Desfazer" recria o produto com os mesmos dados (id novo é aceitável) e cancela o sumiço definitivo.

<details markdown="1">
<summary>Dica</summary>

Guarde uma cópia do objeto antes de chamar `api.remover`. O botão "Desfazer" é um `<button>` inserido dentro do `#feedback` (que é `aria-live`, então será anunciado). Use `setTimeout` para limpar a oferta depois de 6 s e `clearTimeout` se o usuário clicar antes. Reflita: existe alguma forma de desfazer sem recriar, ou seja, sem gerar um id novo? O que mudaria no servidor?
</details>

**C2.** Faça a tela sobreviver à perda de conexão: se o `fetch` falhar por rede (status `0` na `ErroDeApi`), mostre um aviso fixo "Você está offline — as alterações não foram salvas" e tente recarregar a lista automaticamente a cada 5 segundos até voltar.

<details markdown="1">
<summary>Dica</summary>

`window.addEventListener("online", ...)` e `"offline"` avisam mudanças de conectividade, e `navigator.onLine` dá o estado atual — mas nenhum dos dois detecta "o servidor caiu com a rede funcionando", que é o caso mais comum em desenvolvimento. Combine os eventos com a sua própria detecção pelo status `0`. Pare o `setInterval` assim que uma carga der certo.
</details>

## 🏆 Desafios

### ⭐ O card que morre errado
Tags: javascript, dom, bug, crud

Um colega "otimizou" a exclusão para não precisar buscar a lista de novo no servidor: em vez de recarregar, ele remove o item direto do array local. Funciona lindamente — até você digitar algo na busca. Com o filtro `bolo` ativo, excluir o único resultado faz **outro** produto sumir da lista quando você limpa a busca. O trecho alterado é este:

```js
async function excluirProduto(produto, indice) {
  await api.remover(produto.id);
  produtos.splice(indice, 1);
  renderizar();
}
```

Reproduza o bug, explique-o e conserte-o sem voltar a fazer uma requisição extra a cada exclusão.

**Critérios de pronto**

- Um comentário de até 4 linhas no topo da função descreve a sequência exata de cliques que reproduz o bug e por que o índice está errado.
- Excluir funciona igual com e sem busca ativa, e nenhum produto some sem ter sido excluído.
- A correção não faz uma requisição `GET` extra por exclusão (a única requisição é o `DELETE`).
- O estado vazio aparece corretamente quando o último produto da lista filtrada é excluído.

<details markdown="1">
<summary>Pistas</summary>

1. Na aba Console, imprima `produtos` antes e depois do `splice` com a busca ativa. O array que está na tela é o mesmo que está na memória?
2. `splice` trabalha por posição; `filter` trabalha por conteúdo. Qual dos dois não depende de a lista estar na mesma ordem da tela?
3. `produtos = produtos.filter((p) => p.id !== produto.id)` remove pelo identificador, não pela posição — e funciona mesmo que a lista tenha sido filtrada ou reordenada.
4. Vale a pena passar `indice` como parâmetro? Que informação de um produto nunca muda e é suficiente para identificá-lo?
</details>

### ⭐⭐ A busca que corre atrás de si mesma
Tags: fetch, async, performance, devtools

Ligue o throttling "Slow 3G" na aba Network, digite `cafe` rápido no campo de busca e observe: a resposta de `caf` pode chegar **depois** da resposta de `cafe`, e a tela termina mostrando o resultado errado, para um termo que já não está mais no campo. É a *race condition* clássica de busca incremental — e ela existe em produção em muito site grande. Resolva de verdade: cancele a requisição obsoleta.

**Critérios de pronto**

- Digitar rápido nunca deixa a tela com um resultado que não corresponde ao texto atual do campo, mesmo com "Slow 3G".
- Requisições obsoletas aparecem como `canceled` na aba Network — você não está apenas ignorando a resposta, está abortando a requisição.
- O `AbortError` não vira mensagem de erro na tela (abortar foi decisão sua, não falha).
- Um comentário registra quantas requisições saem ao digitar "cafezinho" letra por letra, antes e depois do seu ajuste.

<details markdown="1">
<summary>Pistas</summary>

1. Procure `AbortController` na MDN: `const controlador = new AbortController()` e passe `signal: controlador.signal` nas opções do `fetch`.
2. Guarde o controlador da requisição em andamento numa variável de módulo; antes de disparar a próxima, chame `controlador.abort()` na anterior.
3. Quando um `fetch` é abortado, ele **rejeita** com um erro cujo `name` é `"AbortError"` — trate esse caso separadamente no `catch` do `api.js` ou do `carregarProdutos`.
4. O `debounce` de 400 ms reduz o problema, mas não elimina: uma rede lenta o suficiente ainda inverte a ordem. Os dois mecanismos são complementares.
</details>

### ⭐⭐ Erro 400 no campo certo
Tags: formularios, acessibilidade, api, fetch

O servidor já faz a parte dele: desde a Aula 13, o `400` devolve `detalhes` como lista de objetos `{ "campo": "preco", "mensagem": "…" }`. A tela é que desperdiça essa informação — ela junta tudo num parágrafo só: "Dados inválidos (nome: O nome precisa ter ao menos 3 caracteres.; preco: O preço precisa ser um número maior que zero.)". Formulários bons colocam cada mensagem embaixo do campo culpado. Aproveite o `campo` que já vem pronto e leve cada mensagem ao lugar certo, do jeito que um leitor de tela entende.

**Critérios de pronto**

- Nenhuma mensagem de validação sobra no parágrafo genérico: toda entrada de `detalhes` é levada ao seu campo, e o `testes.http` mostra o formato `{ campo, mensagem }` que o servidor devolve.
- Cada campo com erro recebe `aria-invalid="true"` e um `<p>` de mensagem associado por `aria-describedby`; o primeiro campo com erro recebe o foco.
- Corrigir o campo limpa a mensagem e o `aria-invalid` daquele campo, sem recarregar nada.
- Um cenário no `testes.http` prova que a resposta continua útil para um cliente que não é o seu front (a mensagem faz sentido sozinha).

<details markdown="1">
<summary>Pistas</summary>

1. Não mexa no controlador: `validarProduto` já empurra `{ campo, mensagem }` para `erros`. Todo o trabalho é do lado do cliente.
2. No cliente, o `ErroDeApi` já carrega `detalhes`; percorra a lista e use `document.querySelector(`#${detalhe.campo}`)` para achar o input.
3. `aria-describedby` aceita o id de qualquer elemento; crie os `<p>` de erro uma vez no HTML, vazios e escondidos, em vez de criá-los a cada falha.
4. Para limpar, o evento `input` de cada campo é suficiente — não espere o próximo envio.
</details>

### ⭐⭐⭐ Adeus, `confirm()`
Tags: acessibilidade, dom, refatoracao, javascript

O `confirm()` do navegador congela a aba inteira, não pode ser estilizado, não cabe na identidade visual do Café Cerrado e some sem deixar rastro em capturas de tela. Toda aplicação séria usa um diálogo próprio — e a plataforma web tem um elemento nativo para isso desde 2022: `<dialog>`. Substitua a confirmação de exclusão por um diálogo modal acessível de verdade, e prove que ele é acessível.

**Critérios de pronto**

- A exclusão usa um `<dialog>` aberto com `showModal()`, com título, nome do produto e dois botões (Cancelar / Excluir).
- Funciona 100% por teclado: <kbd>Esc</kbd> fecha, <kbd>Tab</kbd> circula apenas dentro do diálogo, e ao fechar o foco volta ao botão que abriu.
- A promessa de exclusão só resolve depois da decisão do usuário — o `excluirProduto` continua legível, sem callbacks aninhados.
- Um arquivo `docs/acessibilidade-dialogo.md` registra o teste feito com leitor de tela (qual, em que sistema) e o que foi anunciado ao abrir o diálogo.
- O diálogo é reutilizável: uma função `confirmar({ titulo, mensagem, rotuloConfirmar })` serve para qualquer confirmação futura do projeto.

<details markdown="1">
<summary>Pistas</summary>

1. `showModal()` (e não `show()`) é o que ativa o backdrop, o `::backdrop` estilizável, o fechamento por <kbd>Esc</kbd> e o confinamento do foco — tudo isso de graça, nativamente.
2. Para transformar o diálogo numa promessa: `return new Promise((resolver) => { dialogo.addEventListener("close", () => resolver(dialogo.returnValue === "confirmar"), { once: true }); dialogo.showModal(); })`.
3. `<button value="confirmar">` dentro de um `<form method="dialog">` fecha o diálogo e define `returnValue` sem uma linha de JavaScript.
4. Guarde `document.activeElement` antes de abrir e chame `.focus()` nele depois de fechar — o `<dialog>` devolve o foco sozinho na maioria dos navegadores, mas não conte com isso quando o elemento original tiver sido removido do DOM.
5. Para o teste com leitor de tela: NVDA (Windows, gratuito), Orca (Linux, já instalado no GNOME) ou VoiceOver (macOS, <kbd>Cmd</kbd>+<kbd>F5</kbd>).
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON` | O `fetch` recebeu uma página HTML, não JSON: a URL está errada e caiu no 404 do Express | Confira o caminho na aba Network; use `/api/produtos` (com a barra inicial), não `api/produtos` |
| `TypeError: Cannot read properties of undefined (reading 'value')` na linha do `form.id.value` | `form.id` é o atributo id do formulário, não o campo oculto | Acesse sempre por `form.elements.id.value` (seção 5.2) |
| `POST` responde `400 Dados inválidos (preco deve ser um número…)` com o campo preenchido | O `value` de um `<input type="number">` é **string**; `"9.9"` não passa em `typeof === "number"` | Converta no cliente: `preco: Number(formEl.elements.preco.value)` |
| `Uncaught SyntaxError: Cannot use import statement outside a module` | O `app.js` usa `import` mas a tag não declara módulo | Troque para `<script type="module" src="js/app.js"></script>` (e remova o `defer`, que é implícito) |
| Toda escrita responde `401`, mesmo com o usuário logado | O `Authorization` está levando o ID token do Google em vez do token de sessão | `obterToken()` tem de devolver o campo `token` da resposta de `POST /api/auth/google` (seção 3.3) |
| `Erro HTTP 401` em toda escrita, mesmo logado | O token não está sendo enviado, ou expirou (o ID token do Google vive cerca de 1 h) | Confira na aba Network se o cabeçalho `Authorization` foi enviado; se sim, faça login de novo |
| `SyntaxError: Unexpected end of JSON input` ao excluir | O servidor respondeu `204` (sem corpo) e o cliente chamou `resposta.json()` | A checagem `if (resposta.status === 204) return null` no `api.js` resolve |
| `ENOENT: no such file or directory, open './data/produtos.json'` | Caminho relativo depende da pasta de onde o `node` foi executado | Use `path.join(__dirname, "produtos.json")` no repositório (seção 2.1) |
| Os dados somem ao reiniciar o servidor | O controlador alterou o array em memória e esqueceu do `await repo.salvarTodos(produtos)` | Toda operação de escrita termina com `salvarTodos`; confira olhando o arquivo mudar no editor |
| Dois produtos com o mesmo `id` depois de algumas exclusões | O id foi gerado com `lista.length + 1` | Gere com `Math.max(...ids) + 1`, como em `proximoId` |
| A lista aparece como `[object Promise]` ou vazia sem erro | Faltou `await` antes de `api.listar()` | Toda chamada da fachada devolve promessa: `produtos = await api.listar()` |
| `Failed to fetch` ao abrir a página | O site foi aberto por `file://`, não pelo Express | Rode `npm run dev` e acesse `http://localhost:3000` |

## 🏠 Para praticar depois da aula (1 h)

No **projeto autoral**, replique tudo o que foi feito hoje no Café Cerrado:

1. Garanta que o seu recurso tem a camada `data/repositorio.js` com gravação atômica e que os controladores só falam com ela.
2. Crie `public/js/api.js` com a fachada de acesso à sua API (listar, obter, criar, atualizar, remover) e o tratamento centralizado de erro.
3. Implemente na interface o CRUD completo: formulário único com modo edição, exclusão com confirmação, feedback com `aria-live` e recarga da lista após cada operação.
4. Trate os quatro estados da tela (carregando, erro, vazio, conteúdo), com mensagens escritas para o **seu** domínio — nada de "carregando produtos" num projeto de quadras esportivas.
5. Oculte os controles de escrita para visitantes não logados, lembrando que a proteção real continua sendo o `exigirLogin` no servidor.
6. Atualize o `testes.http` com os cenários novos: criar com token, criar sem token (`401`), corpo inválido (`400`), excluir (`204`) e excluir de novo (`404`).
7. Faça o teste do reinício: crie três registros, derrube o servidor, suba de novo e confirme que continuam lá.

**Critério de pronto:** com o servidor rodando, é possível fazer login, criar, editar e excluir registros pela interface, sem nenhum recarregamento de página; os dados sobrevivem ao reinício; e o `testes.http` cobre os cinco cenários da etapa 6.

**Guarde no seu repositório:** commit + push. Confirme, antes do push, que `.env` e `node_modules/` **não** estão no commit.

## ✅ Checkpoint do projeto

Ao final desta aula, o seu repositório precisa ter:

- [ ] `data/repositorio.js` e o controlador das Aulas 13 e 14 intactos: filtros, ordenação, lista branca de categorias e `detalhes: [{ campo, mensagem }]` continuam de pé.
- [ ] Controladores `async`, sem `readFile`/`writeFile` espalhados, respondendo `200`, `201`, `204`, `400` e `404` corretamente.
- [ ] `public/js/api.js` com a fachada e a classe `ErroDeApi` carregando `status` e `detalhes`.
- [ ] `public/js/auth.js` como módulo ES, exportando `obterToken` (o token de **sessão**), `obterUsuario` e `aoMudarSessao`, com o Client ID vindo de `GET /api/config`.
- [ ] `public/js/app.js` com estado, `renderizar()` e os quatro estados da tela.
- [ ] Formulário único com modo edição funcionando (criar e editar no mesmo lugar).
- [ ] Exclusão com confirmação, feedback anunciado por `aria-live` e foco tratado.
- [ ] Dados sobrevivendo ao reinício do servidor.
- [ ] `testes.http` versionado, cobrindo sucesso, `400`, `401` e `404`.
- [ ] `.env` e `node_modules/` fora do Git.

## 📚 Para aprofundar

- MDN — Usando a API Fetch: <https://developer.mozilla.org/pt-BR/docs/Web/API/Fetch_API/Using_Fetch> — leia a parte sobre por que `fetch` não rejeita em erro HTTP.
- MDN — `Response`: <https://developer.mozilla.org/pt-BR/docs/Web/API/Response> — as propriedades `ok`, `status` e os métodos de leitura do corpo.
- MDN — `AbortController`: <https://developer.mozilla.org/pt-BR/docs/Web/API/AbortController> — a base do desafio ⭐⭐.
- MDN — `URLSearchParams`: <https://developer.mozilla.org/pt-BR/docs/Web/API/URLSearchParams> — monte query strings sem concatenar string na mão.
- MDN — `HTMLFormElement.elements`: <https://developer.mozilla.org/pt-BR/docs/Web/API/HTMLFormElement/elements> — a forma correta de acessar campos, incluindo a armadilha do `id`.
- MDN — Regiões `aria-live`: <https://developer.mozilla.org/pt-BR/docs/Web/Accessibility/ARIA/ARIA_Live_Regions> — quando usar `polite` e quando usar `assertive`.
- MDN — O elemento `<dialog>`: <https://developer.mozilla.org/pt-BR/docs/Web/HTML/Element/dialog> — para o desafio ⭐⭐⭐.
- Node.js — `fs/promises`: <https://nodejs.org/docs/latest-v22.x/api/fs.html#promises-api> — `readFile`, `writeFile` e `rename` com promessas.
- Express 5 — respostas (`res.json`, `res.status`, `res.location`): <https://expressjs.com/en/5x/api.html#res> — referência dos métodos usados nos controladores.
- Chrome DevTools — a aba Network: <https://developer.chrome.com/docs/devtools/network?hl=pt-br> — throttling, filtro por XHR e leitura de cabeçalhos.
- QUEIRÓS, Ricardo; PORTELA, Filipe. *Introdução ao Desenvolvimento Moderno para a Web*. FCA, 2018 — integração front-end e back-end.
- PUREWAL, Semmy. *Aprendendo a Desenvolver Aplicações Web*. Novatec, 2014 — construção de uma aplicação completa com Node.js.
- LOUDON, Kyle. *Desenvolvimento de Grandes Aplicações Web*. Novatec, 2019 — camada de dados e organização de aplicações que crescem.

---

Na próxima aula, cada produto ganha um **dono**: o e-mail extraído do token verificado passa a marcar quem criou cada registro, e a API aprende a diferença entre "não sei quem você é" (`401`) e "sei quem você é, mas isso não é seu" (`403`). É também a aula de encerramento desta trilha, com o roteiro completo de auto-teste, o Marco 3 e os caminhos para continuar depois daqui.
