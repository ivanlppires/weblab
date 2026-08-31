# Aula 15 — CRUD com front-end assíncrono

> **Nível 2 — Desenvolvimento Web** · Unidade 3: Web dinâmica server-side
> WebLab · UNEMAT Sinop · Prof. Ivan Luiz Pedroso Pires
> **Carga:** 3 aulas de 50 min (presencial) + 1 h (assíncrona)

Sua API já faz CRUD completo e já sabe quem está batendo na porta. Só que, até agora, quem usou esses recursos foi você — pelo `testes.http`, com a extensão REST Client. Nenhuma pessoa de fora da disciplina consegue cadastrar um café no Café Cerrado sem escrever uma requisição HTTP na mão. Hoje isso muda: a interface que você construiu na Unidade 2 passa a criar, editar e excluir produtos consumindo a sua própria API, sem recarregar a página uma única vez.

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Descrever o contrato completo de um recurso REST (método, caminho, corpo, resposta, status) e usá-lo como acordo entre front e back.
- Isolar leitura e escrita em disco numa camada `data/repositorio.js`, deixando os controladores livres de detalhes de arquivo.
- Explicar por que uma gravação em duas etapas (arquivo temporário + `rename`) protege os dados contra um servidor que morre no meio da escrita.
- Construir uma camada de acesso à API no cliente (`public/js/api.js`) que centraliza cabeçalhos, token e tratamento de erros.
- Implementar os quatro estados de uma tela que depende de rede — carregando, erro, vazio e conteúdo — e renderizá-los a partir de uma única fonte de verdade.
- Reutilizar um mesmo formulário para criar e editar registros, com o padrão de "modo edição" e foco controlado.
- Excluir registros com confirmação e anunciar cada resultado com `aria-live`, sem recarregar a página.
- Depurar uma integração front-back pela aba Network do DevTools, identificando de qual lado está o defeito.

## 📋 Pré-requisitos

- [ ] Repositório `cafe-cerrado-api` rodando com `npm run dev`, servindo o site em `http://localhost:3000` por `express.static('public')` (Aula 11).
- [ ] `routes/produtos.js`, `controllers/produtosController.js` e os middlewares de log, 404 e erro funcionando (Aulas 12 e 13).
- [ ] CRUD da API respondendo pelo `testes.http`: `GET`, `POST`, `PUT` e `DELETE` em `/api/produtos` (Aula 13).
- [ ] Login Google funcionando, `.env` com `GOOGLE_CLIENT_ID` fora do Git e o middleware `exigirLogin` protegendo as rotas de escrita (Aula 14).
- [ ] `fetch` com `async/await` e tratamento de erro no cliente (Aulas 09 e 10) — hoje é tudo isso ao mesmo tempo.

> Na aula passada você delegou o login ao Google, verificou o ID token no servidor com `google-auth-library` e barrou com `401` toda escrita sem token. As duas metades do sistema — API com CRUD e API com autenticação — existem, mas só respondem ao `testes.http`. Hoje elas ganham interface: a tela do cardápio passa a listar, criar, editar e excluir produtos consumindo `/api/produtos` com `fetch`, e os dados passam a sobreviver ao reinício do servidor. Na próxima aula, cada registro ganha dono e a disciplina se encerra com a entrega da Avaliação 3.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Contrato do recurso; camada de persistência (`data/repositorio.js`); controladores `async` com gravação atômica |
| 2 | 50 min | Camada de API no cliente (`public/js/api.js`); estado e render; os quatro estados da tela |
| 3 | 50 min | Formulário criar/editar, exclusão com confirmação, feedback acessível; Mão na massa e laboratório |

## 1. O front-end encontra a própria API

### 1.1 Uma origem só, zero CORS

Na Aula 10 o seu `fetch` foi buscar dados no JSONPlaceholder — um servidor de outra pessoa, em outro domínio. Aquilo é uma requisição **cross-origin**, e só funcionou porque o JSONPlaceholder responde com o cabeçalho `Access-Control-Allow-Origin: *`, autorizando qualquer site a lê-lo.

Agora a situação é outra e muito mais simples. Desde a Aula 11 o Express serve o site estático (`express.static('public')`) **e** a API no mesmo processo, na mesma porta. Abrir `http://localhost:3000/index.html` e pedir `fetch("/api/produtos")` é uma requisição de mesma origem: mesmo protocolo (`http`), mesmo host (`localhost`), mesma porta (`3000`). Nada de CORS, nada de cabeçalhos especiais, nada de preflight.

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

| Método | Caminho | Autenticação |
|---|---|---|
| GET | `/api/produtos` | Pública |
| GET | `/api/produtos/:id` | Pública |
| POST | `/api/produtos` | Exige login |
| PUT | `/api/produtos/:id` | Exige login |
| DELETE | `/api/produtos/:id` | Exige login |

Detalhando corpo e resposta de cada operação:

**`GET /api/produtos`** — lista todos os produtos. Aceita a busca por query string `?q=termo` (Aula 13). Status `200`. Resposta:

```json
[
  {
    "id": 1,
    "nome": "Café coado do cerrado",
    "categoria": "bebidas",
    "preco": 7.5,
    "descricao": "Grãos torrados em Sinop, coado na hora",
    "imagem": "img/cafe-coado.jpg"
  }
]
```

**`GET /api/produtos/:id`** — um produto. Status `200` ou `404` com `{ "erro": "Produto não encontrado" }`.

**`POST /api/produtos`** — corpo com os campos editáveis:

```json
{
  "nome": "Bolo de castanha",
  "categoria": "doces",
  "preco": 9.9,
  "descricao": "Fatia generosa, feita na cozinha da casa"
}
```

Resposta: o produto criado, já com `id`, status `201` e cabeçalho `Location: /api/produtos/7`. Corpo inválido: `400` com `{ "erro": "...", "detalhes": ["..."] }`. Sem token: `401`.

**`PUT /api/produtos/:id`** — mesmo corpo do `POST`. Resposta: o produto atualizado, status `200`. Inexistente: `404`. Sem token: `401`.

**`DELETE /api/produtos/:id`** — sem corpo. Resposta: status `204 No Content`, **sem corpo nenhum**. Inexistente: `404`. Sem token: `401`.

> **💡 Dica**
> Se na Aula 13 o seu `DELETE` devolveu `200` com o objeto excluído, você tem duas opções: mudar para `204` (é o mais comum em APIs REST, porque não há nada a devolver) ou manter `200`. A camada de API que escreveremos na seção 3 trata os dois casos. O que não pode é devolver `204` **com** corpo: `resposta.json()` explode com `Unexpected end of JSON input`.

> **📌 Na prova**
> Decore a semântica dos status que este contrato usa: `200 OK` (deu certo e há corpo), `201 Created` (criou um recurso novo), `204 No Content` (deu certo e não há corpo), `400 Bad Request` (o cliente mandou algo inválido), `401 Unauthorized` (não sei quem você é), `404 Not Found` (o recurso não existe). O `403` entra na próxima aula.

### 1.3 O ciclo estado → render

Toda a lógica de tela desta aula cabe numa frase: **o JavaScript nunca edita a tela por partes; ele muda o estado e manda desenhar tudo de novo.**

```text
evento do usuário  →  chamada à API  →  atualiza o estado  →  renderizar()  →  HTML na tela
```

Concretamente: quando você exclui um produto, o código **não** procura o `<article>` daquele card para removê-lo do DOM. Ele chama a API, recarrega a lista de produtos do servidor, guarda no array `produtos` e chama `renderizar()`, que apaga o container e o redesenha inteiro. Parece desperdício — e é, para listas gigantes — mas elimina de uma vez a classe de bug mais comum de front-end: a tela dizendo uma coisa e os dados dizendo outra.

Guarde esse ciclo. É exatamente o que Vue e React automatizam, e você vai reencontrá-lo no Nível 3 sob outro nome ("reatividade"). Aqui você o implementa à mão, que é a melhor forma de entender o que a ferramenta faz por você depois.

## 2. Persistência: os dados precisam sobreviver ao reinício

### 2.1 Extraindo a leitura e a escrita para um repositório

Na Aula 13 você já gravou em `data/produtos.json` com `fs/promises`. O problema é que o `readFile` e o `writeFile` foram parar dentro do controlador — e agora aparecem repetidos em cinco funções, cada uma com o seu `try/catch`. Quando o projeto trocar o arquivo JSON por um banco de dados, você vai ter que caçar essas chamadas uma a uma.

A solução é uma camada só para isso: o **repositório**. Ele conhece o arquivo; ninguém mais conhece.

`cafe-cerrado-api/data/repositorio.js`

```js
// Camada de persistência: o único arquivo do projeto que sabe onde e como
// os produtos são gravados. Trocar JSON por um banco de dados no futuro
// significa reescrever só este arquivo.
const fs = require("fs/promises");
const path = require("path");

// path.join(__dirname, ...) monta o caminho absoluto a partir da pasta DESTE
// arquivo. Um caminho relativo como "./data/produtos.json" dependeria da pasta
// de onde o "node" foi executado — origem clássica de ENOENT.
const ARQUIVO = path.join(__dirname, "produtos.json");

async function lerTodos() {
  try {
    const texto = await fs.readFile(ARQUIVO, "utf-8");
    return JSON.parse(texto);
  } catch (erro) {
    if (erro.code === "ENOENT") return []; // primeira execução: ainda não existe
    throw erro; // JSON corrompido ou permissão negada: quem chamou precisa saber
  }
}

async function salvarTodos(lista) {
  // Gravação em duas etapas (ver seção 2.3): escreve num arquivo temporário e
  // só então substitui o original. O rename é atômico no mesmo disco.
  const temporario = `${ARQUIVO}.tmp`;
  await fs.writeFile(temporario, JSON.stringify(lista, null, 2), "utf-8");
  await fs.rename(temporario, ARQUIVO);
}

function proximoId(lista) {
  return lista.length ? Math.max(...lista.map((p) => p.id)) + 1 : 1;
}

module.exports = { lerTodos, salvarTodos, proximoId, ARQUIVO };
```

Repare em `proximoId`: ele usa `Math.max` sobre os ids existentes, e **não** `lista.length + 1`. Com `length + 1`, basta excluir um produto do meio para o próximo cadastro reaproveitar um id já usado — e você passa a ter dois produtos com o mesmo id, um bug que só aparece semanas depois.

### 2.2 Controladores `async` usando o repositório

O controlador volta a fazer só o que é dele: interpretar a requisição, validar, decidir o status e responder.

`cafe-cerrado-api/controllers/produtosController.js`

```js
const repo = require("../data/repositorio");

// Normaliza texto para busca: remove acentos e caixa. "Café" e "cafe" viram
// a mesma coisa. A forma NFD separa a letra do seu acento; o intervalo
// Unicode \u0300-\u036f contém justamente os acentos combinantes.
function normalizar(texto) {
  return String(texto ?? "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();
}

// Validação do servidor: a única que vale (a do navegador é conforto).
function validar(dados) {
  const erros = [];
  if (typeof dados.nome !== "string" || dados.nome.trim().length < 3) {
    erros.push("nome deve ter ao menos 3 caracteres");
  }
  if (typeof dados.preco !== "number" || !Number.isFinite(dados.preco) || dados.preco < 0) {
    erros.push("preco deve ser um número maior ou igual a zero");
  }
  if (dados.categoria !== undefined && typeof dados.categoria !== "string") {
    erros.push("categoria deve ser texto");
  }
  return erros;
}

exports.listar = async (req, res) => {
  const produtos = await repo.lerTodos();
  const termo = normalizar(req.query.q);
  if (!termo) return res.json(produtos);

  const encontrados = produtos.filter(
    (p) => normalizar(p.nome).includes(termo) || normalizar(p.descricao).includes(termo)
  );
  res.json(encontrados);
};

exports.obter = async (req, res) => {
  const produtos = await repo.lerTodos();
  const produto = produtos.find((p) => p.id === Number(req.params.id));
  if (!produto) return res.status(404).json({ erro: "Produto não encontrado" });
  res.json(produto);
};

exports.criar = async (req, res) => {
  const erros = validar(req.body ?? {});
  if (erros.length) {
    return res.status(400).json({ erro: "Dados inválidos", detalhes: erros });
  }

  const produtos = await repo.lerTodos();
  const novo = {
    id: repo.proximoId(produtos),
    nome: req.body.nome.trim(),
    categoria: req.body.categoria?.trim() || "geral",
    preco: req.body.preco,
    descricao: req.body.descricao?.trim() || "",
  };

  produtos.push(novo);
  await repo.salvarTodos(produtos);
  res.status(201).location(`/api/produtos/${novo.id}`).json(novo);
};

exports.atualizar = async (req, res) => {
  const produtos = await repo.lerTodos();
  const produto = produtos.find((p) => p.id === Number(req.params.id));
  if (!produto) return res.status(404).json({ erro: "Produto não encontrado" });

  const erros = validar(req.body ?? {});
  if (erros.length) {
    return res.status(400).json({ erro: "Dados inválidos", detalhes: erros });
  }

  produto.nome = req.body.nome.trim();
  produto.categoria = req.body.categoria?.trim() || "geral";
  produto.preco = req.body.preco;
  produto.descricao = req.body.descricao?.trim() || "";

  await repo.salvarTodos(produtos);
  res.json(produto);
};

exports.remover = async (req, res) => {
  const produtos = await repo.lerTodos();
  const indice = produtos.findIndex((p) => p.id === Number(req.params.id));
  if (indice === -1) return res.status(404).json({ erro: "Produto não encontrado" });

  produtos.splice(indice, 1);
  await repo.salvarTodos(produtos);
  res.status(204).end(); // 204: deu certo e não há corpo para devolver
};
```

Duas coisas merecem atenção.

A primeira: **os controladores são `async` e não têm `try/catch`**. Se o disco encher e o `salvarTodos` rejeitar, o Express 5 captura a rejeição sozinho e encaminha para o seu tratador de erros da Aula 12. No Express 4 isso não acontecia — cada handler `async` precisava terminar com `.catch(next)`, e esquecer disso derrubava o processo. É uma das melhores mudanças da versão 5.

A segunda: `res.status(204).end()`. `204` significa "deu certo, e não há nada para dizer". Mandar `res.status(204).json({ ok: true })` é contraditório, e o navegador do outro lado vai quebrar ao tentar ler um corpo que a especificação diz não existir.

As rotas não mudam nada — continuam como na Aula 14:

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

É esse o ganho da arquitetura em camadas: você trocou o miolo da persistência e nem as rotas nem o front-end perceberam.

### 2.3 Por que gravar em duas etapas

`fs.writeFile` não é instantâneo. Para um arquivo de 300 KB, o sistema operacional pode truncar o arquivo antigo, começar a escrever o novo conteúdo e — se o processo morrer nesse instante (você apertou <kbd>Ctrl</kbd>+<kbd>C</kbd>, a máquina reiniciou, o `--watch` recarregou) — deixar no disco um JSON pela metade. Na próxima leitura, `JSON.parse` lança `Unexpected end of JSON input` e o cardápio inteiro se perde.

O truque do arquivo temporário resolve isso:

1. Escreve todo o conteúdo em `produtos.json.tmp`. Se morrer aqui, o `produtos.json` original continua intacto.
2. Renomeia `produtos.json.tmp` para `produtos.json`. No mesmo sistema de arquivos, o `rename` é **atômico**: ou o nome aponta para o arquivo antigo, ou aponta para o novo. Nunca para um meio-termo.

> **🔎 Por baixo do capô**
> A atomicidade do `rename` não é gentileza do Node: é garantia do POSIX, o padrão que rege os sistemas Unix. Renomear um arquivo é trocar uma entrada no diretório, uma operação que o sistema de arquivos trata como indivisível. É o mesmo mecanismo que bancos de dados, editores de texto e o próprio `git` usam para nunca deixarem um arquivo pela metade. Bancos de dados de verdade vão além, com *journaling* e *write-ahead log*, mas o princípio é este.

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

Três decisões desse arquivo valem discussão em sala:

- **`fetch` não rejeita em erro HTTP.** Um `404` ou um `500` são respostas válidas: a promessa resolve normalmente, com `resposta.ok === false`. O `try/catch` em volta do `fetch` só pega falha de rede. Quem esquece disso escreve código que "funciona" mesmo quando o servidor recusou tudo.
- **Erro com status.** Uma `Error` comum só carrega a mensagem. A `ErroDeApi` carrega também o `status` e os `detalhes` da validação, e é isso que permite à tela reagir de formas diferentes a `401` (peça login) e a `400` (mostre o que está errado no formulário).
- **O token vem do módulo de autenticação, não é passado por parâmetro.** Quem chama `api.criar(dados)` não precisa nem saber que existe token. Se amanhã a sessão mudar de mecanismo, muda só o `auth.js`.

### 3.3 O módulo de autenticação, agora como módulo ES

O `auth.js` da Aula 14 guardava o token numa variável global. Como agora `api.js` e `app.js` precisam dessa informação, ele vira um módulo ES de verdade, com uma interface pequena e explícita.

A marcação do cabeçalho é a mesma da Aula 14, com um id a mais (`botao-google`) para conseguirmos escondê-la depois do login:

`trecho de public/index.html — dentro de <header>`

```html
<div id="botao-google">
  <div id="g_id_onload"
       data-client_id="SEU_CLIENT_ID_AQUI"
       data-callback="aoLogar"></div>
  <div class="g_id_signin" data-type="standard" data-locale="pt-BR"></div>
</div>

<div id="area-usuario" hidden>
  <img id="foto-usuario" alt="" width="32" height="32">
  <span id="nome-usuario"></span>
  <button type="button" id="sair">Sair</button>
</div>
```

`cafe-cerrado-api/public/js/auth.js`

```js
// Sessão do usuário no cliente. O token é o ID token assinado pelo Google
// (Aula 14); quem valida a assinatura é o servidor, sempre.
let tokenGoogle = null;
let usuarioLogado = null;
const ouvintes = [];

export function obterToken() {
  return tokenGoogle;
}

export function obterUsuario() {
  return usuarioLogado;
}

// Quem quiser reagir a login/logout registra uma função aqui. É chamada
// imediatamente com o estado atual e de novo a cada mudança.
export function aoMudarSessao(callback) {
  ouvintes.push(callback);
  callback(usuarioLogado);
}

function avisarOuvintes() {
  for (const ouvinte of ouvintes) ouvinte(usuarioLogado);
}

function pintarAreaDoUsuario() {
  const area = document.querySelector("#area-usuario");
  const botaoGoogle = document.querySelector("#botao-google");
  if (usuarioLogado) {
    document.querySelector("#nome-usuario").textContent = usuarioLogado.nome;
    document.querySelector("#foto-usuario").src = usuarioLogado.foto;
    document.querySelector("#foto-usuario").alt = `Foto de ${usuarioLogado.nome}`;
  }
  area.hidden = !usuarioLogado;
  botaoGoogle.hidden = Boolean(usuarioLogado);
}

// Chamada pelo Google após o login (o nome casa com data-callback no HTML).
async function aoLogar(resposta) {
  tokenGoogle = resposta.credential;
  try {
    const r = await fetch("/api/auth/google", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token: tokenGoogle }),
    });
    if (!r.ok) throw new Error("O servidor recusou o token");
    usuarioLogado = await r.json(); // dados verificados PELO SERVIDOR
  } catch (erro) {
    tokenGoogle = null;
    usuarioLogado = null;
    console.error("Falha no login:", erro);
  }
  pintarAreaDoUsuario();
  avisarOuvintes();
}

export function sair() {
  tokenGoogle = null;
  usuarioLogado = null;
  google.accounts.id.disableAutoSelect(); // impede o login automático na volta
  pintarAreaDoUsuario();
  avisarOuvintes();
}

// O Google chama a função pelo nome, a partir do atributo data-callback do
// HTML. Módulos ES têm escopo próprio, então é preciso expor no window.
window.aoLogar = aoLogar;

document.querySelector("#sair").addEventListener("click", sair);
```

> **⚠️ Atenção**
> `window.aoLogar = aoLogar` parece gambiarra, mas é exigência do Google Identity Services: o `data-callback` do HTML é resolvido como propriedade global. Como todo módulo ES tem escopo próprio (nada vaza para `window` automaticamente), sem essa linha o login falha com `Uncaught ReferenceError: aoLogar is not defined`. Alternativa mais limpa, se quiser: chamar `google.accounts.id.initialize({ client_id, callback: aoLogar })` por JavaScript, sem os atributos `data-*`.

> **🧠 Você sabia?**
> O verbo `PUT` está no HTTP desde a especificação de 1996 — mas o `PATCH`, que atualiza só alguns campos, só virou padrão em 2010, na RFC 5789. Motivo: por definição, `PUT` **substitui** o recurso inteiro, e a comunidade passou anos discutindo se enviar apenas dois campos num `PUT` era abuso ou pragmatismo. Nesta disciplina usamos `PUT` com o objeto completo (é o que o formulário manda mesmo), o que mantém a semântica original honesta. Quando você vir uma API respondendo `PATCH /usuarios/9` com `{ "telefone": "..." }`, agora sabe de onde vem a diferença.

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
      <input id="categoria" name="categoria" type="text" list="categorias" placeholder="bebidas">
      <datalist id="categorias">
        <option value="bebidas"></option>
        <option value="doces"></option>
        <option value="salgados"></option>
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

Quando o servidor devolve `400`, ele manda também os `detalhes` — e é responsabilidade da tela mostrá-los, não engoli-los:

```js
try {
  await api.criar(dados);
} catch (erro) {
  // erro.detalhes vem do { erro, detalhes } do controlador (seção 2.2)
  const extra = erro.detalhes?.length ? ` (${erro.detalhes.join("; ")})` : "";
  avisar(`${erro.message}${extra}`, "erro");
}
```

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

Vale parar um minuto e olhar o que a turma construiu. Cada clique em "Adicionar" percorre, em ordem, tudo o que foi estudado no semestre:

1. **HTML e CSS (Unidade 1)** — o formulário semântico, com `<label for>`, estados de foco visíveis e layout responsivo.
2. **JavaScript no cliente (Unidade 2)** — `submit` interceptado com `preventDefault()`, dados lidos do formulário, `fetch` com `async/await`.
3. **HTTP (Aula 01)** — uma requisição `POST /api/produtos`, com `Content-Type: application/json`, `Authorization: Bearer …` e o corpo serializado.
4. **Express (Aulas 11–13)** — a cadeia de middlewares: `express.json()` → log → `exigirLogin` → rota → controlador.
5. **Autenticação (Aula 14)** — `google-auth-library` confere a assinatura do ID token e preenche `req.usuario`.
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

**Passo 1 — crie a camada de persistência.** Crie o arquivo `data/repositorio.js` com o conteúdo da seção 2.1. Confirme que `data/produtos.json` existe e contém um array (`[]` no mínimo).

```bash
cd cafe-cerrado-api
ls data/
# esperado: produtos.json  repositorio.js
```

**Passo 2 — reescreva o controlador.** Substitua `controllers/produtosController.js` pelo conteúdo da seção 2.2. Nenhuma linha de `routes/produtos.js` muda.

**Passo 3 — confirme a API pelo `testes.http`,** antes de tocar no front. Este é o hábito que separa depurar de adivinhar: se a API está certa, todo problema que aparecer depois é do cliente.

`cafe-cerrado-api/testes.http`

```http
### listar tudo
GET http://localhost:3000/api/produtos

### buscar por termo, sem acento e sem caixa
GET http://localhost:3000/api/produtos?q=cafe

### criar sem token — deve responder 401
POST http://localhost:3000/api/produtos
Content-Type: application/json

{ "nome": "Teste sem token", "preco": 1 }

### criar com token — cole abaixo o valor impresso no console do navegador
POST http://localhost:3000/api/produtos
Content-Type: application/json
Authorization: Bearer COLE_SEU_ID_TOKEN_AQUI

{ "nome": "Pão de queijo", "categoria": "salgados", "preco": 6.5, "descricao": "Da roça, assado na hora" }

### corpo inválido — deve responder 400 com detalhes
POST http://localhost:3000/api/produtos
Content-Type: application/json
Authorization: Bearer COLE_SEU_ID_TOKEN_AQUI

{ "nome": "ab", "preco": "muito caro" }

### excluir — deve responder 204 sem corpo
DELETE http://localhost:3000/api/produtos/2
Authorization: Bearer COLE_SEU_ID_TOKEN_AQUI
```

Para obter um token válido, acrescente temporariamente `console.log(tokenGoogle)` como primeira linha depois da atribuição em `aoLogar`, faça login no site e copie o valor impresso no console do navegador. Ele é longo (três blocos separados por ponto) e vale cerca de uma hora. Remova o `console.log` antes do commit: token no console é token no print de tela do colega.

**Passo 4 — atualize o `auth.js`** para a versão em módulo ES da seção 3.3.

**Passo 5 — crie a camada de API do cliente:** `public/js/api.js`, com o conteúdo da seção 3.2.

**Passo 6 — acrescente a área de gestão ao HTML.** Cole o trecho da seção 5.1 dentro do `<main>` de `public/index.html`, logo acima da lista do cardápio, e confirme que a busca e o container da lista existem com estes ids:

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

**Passo 7 — escreva o `app.js` completo.**

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

**Passo 8 — estilo mínimo para os estados.** Acrescente ao seu CSS (o arquivo que você mantém desde a Aula 04):

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

**Passo 9 — teste o ciclo completo.**

```bash
npm run dev
# abra http://localhost:3000 (NÃO abra o arquivo pelo disco)
```

**Como testar — o resultado esperado, passo a passo:**

1. Sem login, a lista carrega e nenhum botão "Editar"/"Excluir" aparece; a área de gestão está oculta.
2. Faça login com o Google: seu nome e sua foto aparecem, o formulário aparece e os cards ganham os botões.
3. Cadastre "Bolo de castanha", `9.90`, categoria `doces`. O feedback anuncia a criação e o card aparece na lista **sem recarregar a página**. Na aba Network do DevTools: `POST /api/produtos` com status `201`.
4. Clique em "Editar" nesse card: o formulário se preenche, o botão vira "Salvar alterações" e o "Cancelar" aparece. Mude o preço para `10.50` e salve — `PUT` com `200`, card atualizado.
5. Digite `bolo` na busca: a requisição só sai 400 ms depois da última tecla (confirme na aba Network) e a lista filtra.
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

### Nível C — Desafio em sala

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

Hoje, quando o servidor recusa o cadastro, todas as mensagens de validação caem no mesmo parágrafo de feedback: "Dados inválidos (nome deve ter ao menos 3 caracteres; preco deve ser um número maior ou igual a zero)". Formulários bons colocam cada mensagem embaixo do campo culpado. Faça o servidor dizer **qual campo** falhou, e a tela mostrar isso no lugar certo, do jeito que um leitor de tela entende.

**Critérios de pronto**

- O `400` do servidor passa a devolver `detalhes` como lista de objetos `{ "campo": "preco", "mensagem": "..." }`, e o `testes.http` mostra esse formato.
- Cada campo com erro recebe `aria-invalid="true"` e um `<p>` de mensagem associado por `aria-describedby`; o campo correto recebe o foco.
- Corrigir o campo limpa a mensagem e o `aria-invalid` daquele campo, sem recarregar nada.
- Um cenário no `testes.http` prova que a resposta continua útil para um cliente que não é o seu front (a mensagem faz sentido sozinha).

<details markdown="1">
<summary>Pistas</summary>

1. No `validar`, troque `erros.push("texto")` por `erros.push({ campo: "preco", mensagem: "..." })` — o resto do controlador não muda.
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
| `Uncaught ReferenceError: aoLogar is not defined` ao clicar no botão do Google | Módulos ES têm escopo próprio; o `data-callback` procura a função no `window` | Mantenha `window.aoLogar = aoLogar` no fim do `auth.js` (seção 3.3) |
| `Erro HTTP 401` em toda escrita, mesmo logado | O token não está sendo enviado, ou expirou (o ID token do Google vive cerca de 1 h) | Confira na aba Network se o cabeçalho `Authorization` foi enviado; se sim, faça login de novo |
| `SyntaxError: Unexpected end of JSON input` ao excluir | O servidor respondeu `204` (sem corpo) e o cliente chamou `resposta.json()` | A checagem `if (resposta.status === 204) return null` no `api.js` resolve |
| `ENOENT: no such file or directory, open './data/produtos.json'` | Caminho relativo depende da pasta de onde o `node` foi executado | Use `path.join(__dirname, "produtos.json")` no repositório (seção 2.1) |
| Os dados somem ao reiniciar o servidor | O controlador alterou o array em memória e esqueceu do `await repo.salvarTodos(produtos)` | Toda operação de escrita termina com `salvarTodos`; confira olhando o arquivo mudar no editor |
| Dois produtos com o mesmo `id` depois de algumas exclusões | O id foi gerado com `lista.length + 1` | Gere com `Math.max(...ids) + 1`, como em `proximoId` |
| A lista aparece como `[object Promise]` ou vazia sem erro | Faltou `await` antes de `api.listar()` | Toda chamada da fachada devolve promessa: `produtos = await api.listar()` |
| `Failed to fetch` ao abrir a página | O site foi aberto por `file://`, não pelo Express | Rode `npm run dev` e acesse `http://localhost:3000` |

## 🏠 Atividade assíncrona (1 h)

No **projeto autoral**, replique tudo o que foi feito hoje no Café Cerrado:

1. Crie a camada `data/repositorio.js` do seu recurso e migre os controladores para usá-la, com gravação atômica.
2. Crie `public/js/api.js` com a fachada de acesso à sua API (listar, obter, criar, atualizar, remover) e o tratamento centralizado de erro.
3. Implemente na interface o CRUD completo: formulário único com modo edição, exclusão com confirmação, feedback com `aria-live` e recarga da lista após cada operação.
4. Trate os quatro estados da tela (carregando, erro, vazio, conteúdo), com mensagens escritas para o **seu** domínio — nada de "carregando produtos" num projeto de quadras esportivas.
5. Oculte os controles de escrita para visitantes não logados, lembrando que a proteção real continua sendo o `exigirLogin` no servidor.
6. Atualize o `testes.http` com os cenários novos: criar com token, criar sem token (`401`), corpo inválido (`400`), excluir (`204`) e excluir de novo (`404`).
7. Faça o teste do reinício: crie três registros, derrube o servidor, suba de novo e confirme que continuam lá.

**Critério de pronto:** com o servidor rodando, é possível fazer login, criar, editar e excluir registros pela interface, sem nenhum recarregamento de página; os dados sobrevivem ao reinício; e o `testes.http` cobre os cinco cenários da etapa 6.

**Entrega:** commit + push no repositório do projeto autoral e link do repositório no SIGAA. Confirme, antes do push, que `.env` e `node_modules/` **não** estão no commit.

## ✅ Checkpoint do projeto

Ao final desta aula, o seu repositório precisa ter:

- [ ] `data/repositorio.js` com `lerTodos`, `salvarTodos` e gravação em duas etapas.
- [ ] Controladores `async`, sem `readFile`/`writeFile` espalhados, respondendo `200`, `201`, `204`, `400` e `404` corretamente.
- [ ] `public/js/api.js` com a fachada e a classe `ErroDeApi` carregando `status` e `detalhes`.
- [ ] `public/js/auth.js` como módulo ES, exportando `obterToken`, `obterUsuario` e `aoMudarSessao`.
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

Na próxima aula, cada produto ganha um **dono**: o e-mail extraído do token verificado passa a marcar quem criou cada registro, e a API aprende a diferença entre "não sei quem você é" (`401`) e "sei quem você é, mas isso não é seu" (`403`). É também a aula de encerramento da disciplina, com o roteiro completo de auto-teste, a entrega da Avaliação 3 e os caminhos para continuar depois daqui.
