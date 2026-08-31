# Aula 11 — Introdução ao Node.js e Express

> **Nível 2 — Desenvolvimento Web** · Unidade 3: Web dinâmica server-side
> WebLab · UNEMAT Sinop · Prof. Ivan Luiz Pedroso Pires
> **Carga:** 3 aulas de 50 min (presencial) + 1 h (assíncrona)

Na Aula 10 o Café Cerrado virou uma SPA: um único `index.html`, navegação por hash, `fetch` buscando `data/produtos.json` e uma API pública para treinar `POST`. Todo esse código rodou dentro do navegador de quem visita o site. Hoje começa a **Unidade 3**, e você troca de lado: em vez de consumir a API dos outros, você escreve o programa que fica esperando requisições e devolvendo respostas. É o mesmo JavaScript — `const`, arrow functions, `async/await`, objetos e arrays funcionam igualzinho — em outro endereço.

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Explicar o que é o Node.js, de onde ele veio e o que muda quando o JavaScript sai do navegador.
- Iniciar um projeto Node com o npm, entendendo `package.json`, `package-lock.json`, `node_modules/` e scripts.
- Criar um servidor HTTP com **Express 5** que responde a rotas `GET`, e explicar o papel de `req` e `res`.
- Servir o site das Unidades 1 e 2 pelo próprio Express com `express.static`, sem Live Server.
- Construir endpoints de API JSON (`GET /api/produtos` e `GET /api/produtos/:id`) devolvendo `200` e `404`.
- Ler dados de um arquivo JSON no servidor com `fs/promises` dentro de um handler `async`.
- Apontar o `fetch` do front-end para a sua própria API e justificar por que caminhos relativos dispensam configurar CORS.

## 📋 Pré-requisitos

Na aula passada você fechou o cliente: `fetch` real, `JSON.parse` implícito com `resposta.json()`, estados de carregando/erro e navegação SPA por hash. A Unidade 2 acabou ali. Hoje a máquina que **responde** àqueles `fetch` deixa de ser da JSONPlaceholder e passa a ser sua, escrita em JavaScript, rodando na sua máquina na porta 3000.

Antes de começar, confirme:

- [ ] **Node.js 22 LTS** instalado (`node --version` deve imprimir algo como `v22.11.0`). Instalação feita na Aula 01.
- [ ] **npm** disponível (`npm --version`, versão 10 ou superior — vem junto com o Node).
- [ ] **Git** configurado com seu nome e e-mail, e conta no GitHub ativa.
- [ ] O repositório `cafe-cerrado` (Unidades 1 e 2) atualizado, com `index.html`, `css/`, `js/app.js`, `img/` e `data/produtos.json`.
- [ ] **VS Code** com a extensão **REST Client** instalada (procure por `humao.rest-client`). Vamos usá-la a partir da próxima aula.
- [ ] Terminal integrado do VS Code funcionando (<kbd>Ctrl</kbd>+<kbd>'</kbd>).

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Node.js fora do navegador; npm, `package.json` e módulos; o servidor sem framework |
| 2 | 50 min | Express 5: primeira rota, `req`/`res`, `node --watch`, `express.static`, endpoints JSON |
| 3 | 50 min | Mão na massa: repositório `cafe-cerrado-api` ponta a ponta; laboratório |

## 1. Node.js: o JavaScript sai do navegador

### 1.1 O problema que o Node veio resolver

Até 2009, JavaScript era uma linguagem de navegador e ponto. O servidor era PHP, Java, Python, Ruby, C#. Nesse ano, Ryan Dahl pegou o **V8** — o motor JavaScript que o Google tinha escrito para o Chrome, absurdamente rápido — e o colocou para rodar sozinho, fora do navegador, acoplado a uma biblioteca de entrada e saída **não bloqueante**.

O detalhe importante é esse "não bloqueante". Os servidores da época costumavam dedicar uma thread do sistema operacional a cada conexão: mil usuários simultâneos, mil threads, e a memória acabava. O Node adotou o modelo que você já conhece do navegador — **uma thread, um event loop, callbacks** — e resolveu o problema por outro caminho: enquanto uma requisição espera o disco ou o banco de dados responder, a thread não fica parada, ela atende as outras.

Aquele diagrama da Aula 09, com a pilha, a fila de tarefas e o event loop, **é o mesmo aqui**. A diferença é o que fica pendurado esperando: lá era um `fetch` ou um `setTimeout`; aqui é uma leitura de arquivo, uma consulta ao banco, uma conexão de rede que chegou.

> **🧠 Você sabia?**
> A demonstração que apresentou o Node.js ao mundo, na JSConf EU de 2009, era sobre uma barra de progresso. Ryan Dahl mostrou que, para exibir corretamente o progresso do upload de um arquivo, os servidores da época precisavam de gambiarras — porque a requisição só era entregue ao seu código **depois** de completamente recebida. Ele escreveu, ao vivo, um servidor de poucas linhas que reagia a cada pedaço do arquivo conforme ele chegava. A plateia aplaudiu de pé. Quinze anos depois, Node é a base do Netflix, do PayPal, do LinkedIn e do próprio npm.

### 1.2 O que existe no Node e o que não existe

Esta é a tabela que evita a maior parte da confusão das próximas semanas:

| Existe no navegador | Existe no Node.js | Existe nos dois |
|---|---|---|
| `document`, `window`, DOM | `fs` (arquivos), `path`, `http`, `process` | `const`, `let`, arrow functions |
| `localStorage`, `alert` | `require`, `module.exports`, `__dirname` | `async/await`, Promises, `fetch` |
| Eventos de clique, `addEventListener` do DOM | Portas de rede, variáveis de ambiente | `JSON`, `Array`, `Object`, `Map` |

Ou seja: **não existe página** no servidor. Não há `document.querySelector`, não há `<div>`, não há CSS. O servidor recebe texto (uma requisição HTTP) e devolve texto (uma resposta HTTP). Quem transforma esse texto em pixels é o navegador, do outro lado.

### 1.3 Primeiro contato: o Node como executor de scripts

Abra um terminal em uma pasta qualquer e crie um arquivo:

`olamundo.js`

```js
// Isto é JavaScript comum — só que sem navegador em volta.
const cidade = "Sinop";
const cafes = ["coado", "cappuccino", "expresso"];

console.log(`JavaScript rodando no terminal, em ${cidade}!`);
console.log(`Temos ${cafes.length} tipos de café:`, cafes.join(", "));

// Aqui está a primeira coisa que o navegador nunca deixaria você fazer:
console.log("Esta pasta é:", process.cwd());
console.log("Versão do Node:", process.version);
```

Rode:

```bash
node olamundo.js
```

Saída esperada (o caminho varia na sua máquina):

```text
JavaScript rodando no terminal, em Sinop!
Temos 3 tipos de café: coado, cappuccino, expresso
Esta pasta é: /home/aluno/projetos
Versão do Node: v22.11.0
```

O objeto global `process` representa o processo do sistema operacional em que o seu código está rodando: diretório atual, versão, variáveis de ambiente, argumentos da linha de comando. Ele não existe no navegador porque lá não há processo seu — há uma aba.

Agora tente, no mesmo arquivo, acrescentar `console.log(document.title);` e rodar de novo:

```text
ReferenceError: document is not defined
```

Guarde esse erro. Ele é o sinal número 1 de que você colou código de front-end em um arquivo de back-end (ou o contrário).

> **🔬 Investigue**
> Digite só `node` no terminal, sem nome de arquivo, e aperte <kbd>Enter</kbd>. Você entrou no **REPL** (Read–Eval–Print Loop), um console idêntico ao do DevTools. Experimente: `2 + 2`, `[1,2,3].map(n => n * 10)`, `typeof window`, `Object.keys(process.env).length`. Compare a última resposta com o que você vê ao rodar `printenv | wc -l` em outro terminal. Para sair do REPL, `.exit` ou <kbd>Ctrl</kbd>+<kbd>D</kbd>. Anote: `typeof window` devolveu o quê? E no console do Chrome, o que devolveria?

## 2. npm: o gerenciador de pacotes

### 2.1 Iniciando um projeto

Um projeto Node é uma pasta com um arquivo `package.json` — a certidão de nascimento do projeto. Ele guarda nome, versão, scripts e, principalmente, a lista de bibliotecas de que o projeto depende.

```bash
mkdir cafe-cerrado-api
cd cafe-cerrado-api
npm init -y
```

O `-y` aceita todas as respostas padrão. O resultado:

`package.json`

```json
{
  "name": "cafe-cerrado-api",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC"
}
```

### 2.2 Instalando uma dependência

```bash
npm install express
```

Três coisas acontecem:

1. O npm baixa o Express e **tudo de que o Express depende** para dentro de `node_modules/`.
2. Acrescenta uma linha em `dependencies`, no `package.json`.
3. Cria (ou atualiza) o `package-lock.json`, registrando a versão **exata** de cada pacote baixado.

O `package.json` fica assim:

```json
{
  "name": "cafe-cerrado-api",
  "version": "1.0.0",
  "main": "server.js",
  "scripts": {
    "dev": "node --watch server.js",
    "start": "node server.js"
  },
  "dependencies": {
    "express": "^5.1.0"
  },
  "keywords": [],
  "author": "",
  "license": "ISC"
}
```

### 2.3 O acento circunflexo e o versionamento semântico

`"express": "^5.1.0"` não quer dizer "exatamente a versão 5.1.0". Os pacotes npm seguem o **versionamento semântico** (SemVer), em que o número tem três partes:

| Parte | Exemplo | Quando aumenta |
|---|---|---|
| MAIOR | **5**.1.0 | Mudança que quebra código existente (Express 4 → 5) |
| MENOR | 5.**1**.0 | Recurso novo, compatível com o que já existia |
| CORREÇÃO | 5.1.**0** | Correção de bug, sem recurso novo |

O `^` significa "esta versão ou qualquer atualização **compatível**": aceita 5.1.1, 5.2.0, 5.9.3 — mas nunca 6.0.0, porque a versão MAIOR pode quebrar tudo. É por isso que este curso usa Express 5 enquanto a maioria dos tutoriais da internet ainda mostra Express 4: são versões MAIORES diferentes, com diferenças reais de sintaxe (voltaremos a isso na seção 6).

O `package-lock.json`, por outro lado, guarda a versão exata que foi instalada **hoje**, na sua máquina. Ele existe para que o colega que clonar o projeto amanhã receba exatamente as mesmas versões, e não uma correção nova que apareceu no meio do caminho. Por isso: **`package-lock.json` vai para o Git**, sim.

### 2.4 A pasta que nunca vai para o Git

`node_modules/` pode ter dezenas de milhares de arquivos. Não é seu código — é código baixado, reconstruível a qualquer momento. Antes do primeiro commit, crie:

`.gitignore`

```text
# dependências instaladas pelo npm — reconstruídas com "npm install"
node_modules/

# arquivos de ambiente com segredos — usaremos a partir da Aula 14
.env

# lixo de sistema operacional e de editor
.DS_Store
Thumbs.db
```

Quem clonar o repositório roda `npm install` e o npm reconstrói `node_modules/` inteiro a partir do `package.json` e do `package-lock.json`.

> **⚠️ Atenção**
> Se você já commitou `node_modules/` por engano, o `.gitignore` sozinho não resolve — ele só ignora arquivos **ainda não rastreados**. Rode `git rm -r --cached node_modules` e commite a remoção. O histórico continuará pesado, mas o próximo commit já fica limpo.

> **🔬 Investigue**
> Com o Express instalado, rode no terminal do projeto: `find node_modules -type f | wc -l` (Linux/macOS) ou `(Get-ChildItem node_modules -Recurse -File).Count` (PowerShell). Depois, `du -sh node_modules` para o tamanho total. Quantos arquivos o npm baixou para instalar **um** pacote? Agora rode `npm ls express` e depois `npm ls --all | head -40`: quem são as dezenas de dependências que vieram junto? Escreva em uma linha por que isso justifica a existência do `.gitignore`.

### 2.5 Scripts npm

A seção `scripts` do `package.json` dá apelidos a comandos:

```json
{
  "scripts": {
    "dev": "node --watch server.js",
    "start": "node server.js"
  }
}
```

- `npm run dev` roda o servidor em modo de desenvolvimento, reiniciando sozinho a cada arquivo salvo.
- `npm start` roda em modo normal (`start` é um dos poucos nomes que dispensam o `run`).

A vantagem não é digitar menos: é que **qualquer pessoa** que clone o projeto descobre como rodá-lo lendo o `package.json`, sem precisar perguntar.

## 3. Módulos: `require` e `module.exports`

No front-end da Unidade 2 você usou módulos ES (`import` / `export` com `type="module"`). No servidor, o Node suporta os dois sistemas, e o padrão histórico — usado pelo Express, pela maior parte dos tutoriais e por este curso na Unidade 3 — é o **CommonJS**:

`exemplos/produtos-de-teste.js`

```js
// Um módulo CommonJS: um arquivo que exporta algo.
const produtos = [
  { id: 1, nome: "Espresso do Cerrado", preco: 6 },
  { id: 2, nome: "Coado da Casa", preco: 8.5 },
];

module.exports = produtos; // isto é o que quem der require() vai receber
```

`exemplos/uso.js`

```js
// Quem consome: o caminho relativo começa com ./ e a extensão é opcional.
const produtos = require("./produtos-de-teste");

console.log("Produtos carregados:", produtos.length);
console.log("Mais barato:", produtos.reduce((a, b) => (a.preco < b.preco ? a : b)).nome);
```

Comparando os dois sistemas:

| CommonJS (servidor, este curso) | Módulos ES (front-end, Unidade 2) |
|---|---|
| `const express = require("express")` | `import express from "express"` |
| `module.exports = router` | `export default router` |
| `exports.listar = fn` | `export function listar() {}` |

Para usar `import`/`export` no servidor, você acrescentaria `"type": "module"` ao `package.json`. **Não faça isso agora**: as aulas 12 a 16 usam `require`, e misturar os dois estilos no mesmo projeto é uma das fontes de erro mais irritantes do ecossistema Node.

> **⚠️ Atenção**
> Se escrever `import express from "express"` em um projeto CommonJS, o Node responde:
> `SyntaxError: Cannot use import statement outside a module`. A correção é trocar por `require` — não é adicionar `"type": "module"` no meio do semestre.

## 4. O primeiro servidor

### 4.1 Sem framework: o módulo `http`

Dá para escrever um servidor web usando só o que vem no Node, sem instalar nada. Vale ver uma vez, para você saber o que o Express está fazendo por baixo:

`exemplos/servidor-sem-express.js`

```js
const http = require("node:http");

const produtos = [
  { id: 1, nome: "Espresso do Cerrado", preco: 6 },
  { id: 2, nome: "Coado da Casa", preco: 8.5 },
];

const servidor = http.createServer((req, res) => {
  // Cada requisição cai aqui. Nós é que precisamos decidir tudo, na unha.
  if (req.method === "GET" && req.url === "/api/produtos") {
    res.writeHead(200, { "Content-Type": "application/json; charset=utf-8" });
    res.end(JSON.stringify(produtos));
    return;
  }

  if (req.method === "GET" && req.url === "/") {
    res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
    res.end("<h1>Café Cerrado</h1>");
    return;
  }

  res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
  res.end("Nao encontrado");
});

servidor.listen(3000, () => {
  console.log("Servidor sem framework em http://localhost:3000");
});
```

Funciona. Mas repare no trabalho manual: comparar `req.method` e `req.url` com `if`, escrever o cabeçalho `Content-Type` na mão, serializar o JSON na mão, tratar o 404 na mão. Com dez rotas isso vira uma escada de `if` ilegível. É exatamente esse desconforto que o Express elimina.

### 4.2 Com Express

`server.js`

```js
const express = require("express");

const app = express();
const PORTA = process.env.PORT || 3000;

app.get("/", (req, res) => {
  res.send("<h1>Meu primeiro servidor Express!</h1>");
});

app.listen(PORTA, () => {
  console.log(`Servidor rodando em http://localhost:${PORTA}`);
});
```

```bash
node server.js
```

Abra `http://localhost:3000` no navegador. Você acabou de atender uma requisição HTTP igual às que estudou na Aula 01 — só que do lado de dentro.

`process.env.PORT` lê uma **variável de ambiente**. Localmente ela não existe, então o `||` entrega 3000. Quando você publicar o projeto (trilha Deploy), o serviço de hospedagem define `PORT` e o seu código se adapta sem precisar de alteração. Duas linhas hoje, uma dor de cabeça a menos depois.

### 4.3 Anatomia de uma rota

```js
app.get("/api/produtos", (req, res) => {
  res.json(produtos);
});
```

Leia assim: **quando chegar uma requisição com o método `GET` no caminho `/api/produtos`, execute esta função.**

- `app.get`, `app.post`, `app.put`, `app.delete` — o método HTTP vira o nome da função. (No Express 5, `app.del()` foi removido: escreva `app.delete()`.)
- O primeiro argumento é o **caminho** (path), sempre começando com `/`.
- O segundo é a **função manipuladora** (handler), que recebe `req` e `res`.

Reconheça o padrão: é o mesmo modelo de callback dos eventos do DOM. Lá, `botao.addEventListener("click", (evento) => {})`; aqui, `app.get("/rota", (req, res) => {})`. O "evento" agora é *chegou uma requisição neste caminho*.

### 4.4 O que tem em `req` e em `res`

`req` (request) é o que o cliente mandou:

| Propriedade | O que traz |
|---|---|
| `req.method` | `"GET"`, `"POST"`, `"PUT"`, `"DELETE"` |
| `req.params` | Os pedaços variáveis do caminho: `/produtos/:id` → `req.params.id` |
| `req.query` | A query string: `?categoria=cafes&q=pao` → `req.query.categoria` |
| `req.headers` | Os cabeçalhos HTTP enviados pelo navegador |

`res` (response) é o que você vai devolver:

| Método | O que faz |
|---|---|
| `res.send(algo)` | Devolve texto ou HTML, adivinhando o `Content-Type` |
| `res.json(objeto)` | Serializa para JSON e define `Content-Type: application/json` |
| `res.status(404)` | Define o código de status; encadeável: `res.status(404).json({})` |
| `res.sendFile(caminho)` | Devolve um arquivo do disco (caminho absoluto) |

> **⚠️ Atenção**
> No Express 5, `req.query` é **somente leitura**. Tentar `req.query.q = "cafe"` derruba o servidor com `TypeError: Cannot set property query of #<IncomingMessage> which has only a getter`. Se precisar de uma versão modificada, copie para uma variável: `const filtros = { ...req.query }`.

> **📌 Na prova**
> Duas trocas do Express 4 para o 5 caem com frequência: `res.json(obj, 201)` virou `res.status(201).json(obj)`, e `res.redirect('/rota', 302)` virou `res.redirect(302, '/rota')`. A regra mental é "status primeiro".

### 4.5 Reinício automático: `node --watch`

Alterou o `server.js`? O processo Node continua rodando o código **antigo**, carregado na memória quando você digitou `node server.js`. É preciso parar (<kbd>Ctrl</kbd>+<kbd>C</kbd>) e rodar de novo. Fazer isso quarenta vezes por aula é insuportável — e é a causa número 1 de "mas eu já corrigi e não mudou nada".

O Node 22 resolve isso nativamente:

```bash
node --watch server.js
```

Com o script `dev` do `package.json`, fica só:

```bash
npm run dev
```

Saída esperada a cada salvamento:

```text
Servidor rodando em http://localhost:3000
Restarting 'server.js'
Servidor rodando em http://localhost:3000
```

> **💡 Dica**
> Tutoriais mais antigos mandam instalar o pacote `nodemon` para isso. Ele continua funcionando, mas desde o Node 18/22 a flag `--watch` faz o mesmo sem dependência nenhuma. Uma dependência a menos é sempre uma boa notícia.

> **🔎 Por baixo do capô**
> O que acontece entre você digitar `localhost:3000` e a página aparecer? (1) O navegador resolve `localhost` para o endereço `127.0.0.1` — a sua própria máquina — sem consultar DNS na internet. (2) Abre uma conexão TCP na porta 3000. (3) Envia um texto: `GET / HTTP/1.1`, mais os cabeçalhos. (4) O Node aceita a conexão, monta os objetos `req` e `res` e chama o handler que casou com método e caminho. (5) O seu `res.send` escreve de volta `HTTP/1.1 200 OK`, os cabeçalhos e o corpo. (6) O navegador lê o `Content-Type`, decide que é HTML e renderiza. Tudo isso em menos de um milissegundo, porque nada saiu da sua máquina.

## 5. Servindo o site pelo próprio Express

### 5.1 `express.static`

Até agora você abria o site com o Live Server, um servidorzinho que a extensão do VS Code sobe para você. A partir de hoje o servidor é o seu — e ele também sabe entregar HTML, CSS, imagens e JavaScript.

Coloque o site inteiro em uma pasta `public/` e acrescente **uma linha**:

`server.js`

```js
const path = require("node:path");
const express = require("express");

const app = express();
const PORTA = process.env.PORT || 3000;

// Entrega qualquer arquivo que exista dentro de public/
app.use(express.static(path.join(__dirname, "public")));

app.listen(PORTA, () => {
  console.log(`Servidor rodando em http://localhost:${PORTA}`);
});
```

Pronto: `http://localhost:3000` devolve `public/index.html`, `http://localhost:3000/css/estilo.css` devolve o CSS, `http://localhost:3000/img/logo.svg` devolve a imagem. Nenhuma rota precisou ser escrita.

`__dirname` é uma variável que o CommonJS injeta em todo módulo: a pasta onde **este arquivo** está. Você poderia escrever `express.static("public")` e funcionaria — mas apenas se o terminal estivesse aberto exatamente na pasta do projeto, porque um caminho relativo é resolvido a partir do diretório de trabalho, não do arquivo. `path.join(__dirname, "public")` funciona sempre.

### 5.2 A ordem importa

O `express.static` é registrado com `app.use`, e tudo que se registra com `app.use` entra em uma fila que é percorrida **na ordem de registro**. O `express.static` procura o arquivo pedido; se encontra, responde e encerra; se não encontra, passa a requisição adiante para as rotas seguintes.

```js
app.use(express.static(path.join(__dirname, "public")));

// Esta rota só é alcançada se NÃO existir um arquivo public/sobre.html
app.get("/sobre", (req, res) => {
  res.send("<h1>Sobre o Café Cerrado</h1>");
});
```

Se existir `public/sobre.html`, ele ganha — o arquivo estático é encontrado antes. Essa disputa entre arquivo e rota é fonte garantida de confusão; na próxima aula, ao estudar middlewares, a mecânica ficará explícita.

### 5.3 `public/` é público — literalmente

Tudo que está em `public/` pode ser baixado por qualquer pessoa que saiba (ou adivinhe) o nome do arquivo. Isso é ótimo para CSS e imagens e **péssimo** para dados que você quer controlar.

Hoje o `data/produtos.json` do Café Cerrado está dentro do site: qualquer visitante pode abrir `/data/produtos.json` e ver o arquivo cru. Na nossa nova arquitetura ele sai de lá e passa a ficar **fora** de `public/`, acessível só pelo servidor. O visitante continua vendo os produtos — mas através do endpoint `/api/produtos`, que é código seu, e onde amanhã você poderá filtrar, esconder campos, exigir login ou registrar quem consultou.

> **⚠️ Atenção**
> `express.static` ignora **dotfiles** por padrão: um arquivo chamado `.env` dentro de `public/` não é servido. Isso é uma rede de proteção, não uma permissão — segredo nenhum deve ficar em `public/`, ponto final.

## 6. Endpoints JSON: agora a API é sua

### 6.1 `res.json` e o primeiro endpoint

Na Aula 10 você consumiu a JSONPlaceholder. Agora você **é** a JSONPlaceholder:

`server.js` (trecho)

```js
const produtos = [
  { id: 1, nome: "Espresso do Cerrado", categoria: "cafes", preco: 6 },
  { id: 2, nome: "Pão de Queijo Mineiro", categoria: "salgados", preco: 7 },
];

// GET /api/produtos → a lista completa
app.get("/api/produtos", (req, res) => {
  res.json(produtos); // serializa para JSON e define o Content-Type
});
```

`res.json(produtos)` faz três coisas: chama `JSON.stringify` no objeto, define o cabeçalho `Content-Type: application/json; charset=utf-8` e envia. Sem ele, você teria que fazer os três passos na mão, como no exemplo com o módulo `http`.

Por que o caminho começa com `/api`? Convenção. Ela separa, na URL, o que é **página para humanos** (`/`, `/cardapio.html`) do que é **dado para programas** (`/api/produtos`). Quem lê a URL já sabe o que esperar.

### 6.2 Parâmetros de rota

```js
// GET /api/produtos/2 → só o produto de id 2
app.get("/api/produtos/:id", (req, res) => {
  const id = Number(req.params.id); // params SEMPRE chegam como string
  const produto = produtos.find((p) => p.id === id);

  if (!produto) {
    return res.status(404).json({ erro: "Produto não encontrado" });
  }

  res.json(produto);
});
```

Três detalhes que valem cada um um bug evitado:

1. **`:id` cria um parâmetro nomeado.** Qualquer valor naquela posição casa: `/api/produtos/2`, `/api/produtos/abc`, `/api/produtos/999`.
2. **`req.params.id` é string.** `"2" === 2` é falso. Sem o `Number()`, o `find` nunca acha nada e a sua API responde 404 para tudo.
3. **`return` antes do `res.status(404)`.** Sem ele, o código continua e tenta chamar `res.json(produto)` com `produto` valendo `undefined` — o Express reclama com `Error: Cannot set headers after they are sent to the client`.

### 6.3 Os status que a sua API vai usar hoje

| Código | Quando devolver |
|---|---|
| `200 OK` | Deu certo, e o corpo tem o que foi pedido |
| `404 Not Found` | O recurso pedido não existe (ou a rota não existe) |
| `500 Internal Server Error` | Algo quebrou dentro do seu servidor |

Na próxima aula entram `201`, `204`, `400` e, na Aula 14, `401` e `403`. Por hoje, três bastam — e a regra é sempre a mesma: **o status é para a máquina, a mensagem no corpo é para a pessoa.** Um `fetch` no front-end verifica `resposta.ok` (que é `true` só para status 200–299) e mostra a mensagem do corpo ao usuário.

> **⚠️ Atenção**
> `fetch` **não** rejeita a Promise quando o servidor responde 404 ou 500 — do ponto de vista da rede, a requisição foi um sucesso. Foi por isso que na Aula 09 você escreveu `if (!resposta.ok) throw new Error(...)`. Aquele `if` continua obrigatório agora que o servidor é seu.

### 6.4 Lendo os dados de um arquivo

Manter a lista dentro do `server.js` funciona para dois produtos e trava na hora de crescer. Vamos ler de um arquivo JSON, com o módulo `fs/promises` — a versão do módulo de arquivos que devolve Promises, exatamente o que você aprendeu a manipular na Aula 09.

`data/produtos.json`

```json
[
  {
    "id": 1,
    "nome": "Espresso do Cerrado",
    "categoria": "cafes",
    "preco": 6,
    "descricao": "Grãos de Alto Paraíso, torra média, corpo encorpado e final achocolatado.",
    "imagem": "img/espresso.jpg"
  },
  {
    "id": 2,
    "nome": "Coado da Casa",
    "categoria": "cafes",
    "preco": 8.5,
    "descricao": "Duzentos mililitros em coador de papel, moagem média feita na hora do pedido.",
    "imagem": "img/coado.jpg"
  }
]
```

`server.js` (trecho)

```js
const fs = require("node:fs/promises");

const CAMINHO_DADOS = path.join(__dirname, "data", "produtos.json");

// Lê o arquivo e devolve um array de objetos JavaScript.
async function lerProdutos() {
  const conteudo = await fs.readFile(CAMINHO_DADOS, "utf-8");
  return JSON.parse(conteudo);
}

app.get("/api/produtos", async (req, res) => {
  const produtos = await lerProdutos();
  res.json(produtos);
});
```

Repare no `async` antes de `(req, res)`. Ele é necessário porque temos um `await` dentro do handler — e o Express aceita handlers assíncronos sem qualquer configuração extra.

> **🔎 Por baixo do capô**
> Se `data/produtos.json` estiver corrompido, `JSON.parse` lança um erro. No **Express 4**, um `throw` dentro de um handler `async` não era capturado pelo framework: a Promise rejeitava em silêncio, a requisição ficava pendurada até o navegador desistir, e o processo Node inteiro corria risco de morrer com `UnhandledPromiseRejection`. Era por isso que todo tutorial mandava embrulhar tudo em `try/catch` ou instalar o pacote `express-async-handler`. No **Express 5**, o framework embrulha cada handler `async` internamente: qualquer exceção lançada — síncrona ou dentro de um `await` — é capturada e encaminhada ao tratador de erros. Você ganha um `500` limpo em vez de um servidor travado. Na próxima aula vamos escrever esse tratador.

### 6.5 Testando sem o navegador

O navegador só sabe fazer `GET`. Para os outros métodos (e para ver o status e os cabeçalhos), use o `curl`:

```bash
# lista completa; -i mostra os cabeçalhos junto com o corpo
curl -i http://localhost:3000/api/produtos

# um item existente
curl -i http://localhost:3000/api/produtos/1

# um item inexistente: deve responder 404
curl -i http://localhost:3000/api/produtos/999
```

Saída esperada da última chamada (o `curl` mostra ainda outros cabeçalhos; estes são os que importam):

```text
HTTP/1.1 404 Not Found
Content-Type: application/json; charset=utf-8
Content-Length: 34

{"erro":"Produto não encontrado"}
```

Na próxima aula você troca o `curl` por um arquivo `testes.http` versionado junto com o projeto — muito mais confortável.

## 💻 Mão na massa — o Café Cerrado ganha um servidor

Vamos criar o repositório da Unidade 3 inteira. Ele nasce hoje e será o mesmo até a Aula 16.

### Passo 1 — Criar o projeto

```bash
mkdir cafe-cerrado-api
cd cafe-cerrado-api
git init
npm init -y
npm install express
```

Confirme a versão instalada:

```bash
npm ls express
```

```text
cafe-cerrado-api@1.0.0 /home/aluno/projetos/cafe-cerrado-api
└── express@5.1.0
```

Se aparecer `express@4.x`, você está com um `package.json` antigo ou com cache estranho: apague `node_modules/` e `package-lock.json` e rode `npm install express@5` de novo.

### Passo 2 — O `.gitignore` antes de qualquer commit

`.gitignore`

```text
# dependências instaladas pelo npm — reconstruídas com "npm install"
node_modules/

# arquivos de ambiente com segredos — usaremos a partir da Aula 14
.env

# lixo de sistema operacional e de editor
.DS_Store
Thumbs.db
```

Confira que funcionou:

```bash
git status --short
```

`node_modules/` **não** pode aparecer na lista. Se aparecer, o `.gitignore` está no lugar errado (tem que estar na raiz do projeto) ou com o nome errado (é `.gitignore`, com ponto na frente).

### Passo 3 — Os scripts

Edite o `package.json` e deixe assim:

`package.json`

```json
{
  "name": "cafe-cerrado-api",
  "version": "1.0.0",
  "description": "API e site do Café Cerrado — UNEMAT Sinop",
  "main": "server.js",
  "scripts": {
    "dev": "node --watch server.js",
    "start": "node server.js"
  },
  "keywords": ["express", "api", "cafeteria"],
  "author": "Seu Nome",
  "license": "ISC",
  "dependencies": {
    "express": "^5.1.0"
  }
}
```

### Passo 4 — Trazer o site para dentro

Copie o conteúdo do repositório `cafe-cerrado` (Unidades 1 e 2) para uma pasta `public/`, **exceto** a pasta `data/`:

```bash
mkdir public
cp -r ../cafe-cerrado/index.html ../cafe-cerrado/css ../cafe-cerrado/js ../cafe-cerrado/img public/
mkdir data
cp ../cafe-cerrado/data/produtos.json data/
```

No Windows, use o Explorador de Arquivos: copie `index.html`, `css/`, `js/` e `img/` para dentro de `public/`, e `data/produtos.json` para uma pasta `data/` na raiz do projeto (fora de `public/`).

Vale saber o que veio em cada peça, porque nenhuma delas é descartável:

| Arquivo copiado | O que é | O que acontece com ele hoje |
|---|---|---|
| `index.html` | A página única da SPA, com as três `<section data-rota>` | Continua igual; o Express passa a servi-lo em `/` |
| `css/estilo.css` | Todo o CSS das Aulas 02 a 06 | Continua igual |
| `js/api.js` | A camada de acesso a dados da Aula 10 | **Duas linhas mudam** no Passo 7: as URLs |
| `js/roteador.js` | O roteador por hash da Aula 10 | Continua igual — é ele que mostra e esconde as telas |
| `js/app.js` | A aplicação (filtros, cards, carrinho, contato) | Continua igual, sem uma vírgula de diferença |
| `img/` | As fotos dos dez produtos | Continua igual |
| `data/produtos.json` | O cardápio | Sai de `public/` e vai para a raiz: agora é dado do servidor |
| `data/categorias.json` | A lista de categorias da Aula 10 | **Não é copiado**: a partir de hoje quem responde categorias é a API |

A estrutura final:

```text
cafe-cerrado-api/
├── data/
│   └── produtos.json        # dados: FORA de public/, só o servidor lê
├── public/                  # o site das Unidades 1 e 2
│   ├── css/
│   │   └── estilo.css
│   ├── img/
│   ├── js/
│   │   ├── api.js
│   │   ├── app.js
│   │   └── roteador.js
│   └── index.html
├── .gitignore
├── package.json
├── package-lock.json
└── server.js
```

### Passo 5 — Os dados do Café Cerrado

O arquivo que você copiou no passo anterior já é o cardápio certo — são os **mesmos dez produtos** das Aulas 03 a 10, com os mesmos ids, preços e categorias. Não reescreva nada: o `data/produtos.json` do `cafe-cerrado-api` tem de ser byte por byte igual ao do `cafe-cerrado`. Confira abaixo se o seu bate.

`data/produtos.json`

```json
[
  {
    "id": 1,
    "nome": "Espresso do Cerrado",
    "categoria": "cafes",
    "preco": 6,
    "descricao": "Grãos de Alto Paraíso, torra média, corpo encorpado e final achocolatado.",
    "imagem": "img/espresso.jpg"
  },
  {
    "id": 2,
    "nome": "Coado da Casa",
    "categoria": "cafes",
    "preco": 8.5,
    "descricao": "Duzentos mililitros em coador de papel, moagem média feita na hora do pedido.",
    "imagem": "img/coado.jpg"
  },
  {
    "id": 3,
    "nome": "Cappuccino Sinop",
    "categoria": "cafes",
    "preco": 12,
    "descricao": "Espresso duplo, leite vaporizado e canela do Cerrado por cima.",
    "imagem": "img/cappuccino.jpg"
  },
  {
    "id": 4,
    "nome": "Latte de Baunilha",
    "categoria": "cafes",
    "preco": 14,
    "descricao": "Espresso, leite vaporizado e calda de baunilha feita na casa.",
    "imagem": "img/latte.jpg"
  },
  {
    "id": 5,
    "nome": "Cold Brew da Chapada",
    "categoria": "geladas",
    "preco": 15,
    "descricao": "Extração a frio por dezoito horas, servida com gelo e rodela de laranja.",
    "imagem": "img/cold-brew.jpg"
  },
  {
    "id": 6,
    "nome": "Frappê de Café",
    "categoria": "geladas",
    "preco": 16,
    "descricao": "Espresso batido com gelo, leite e chantili. Também sai sem lactose.",
    "imagem": "img/frappe.jpg"
  },
  {
    "id": 7,
    "nome": "Pão de Queijo Mineiro",
    "categoria": "salgados",
    "preco": 7,
    "descricao": "Porção com quatro unidades de polvilho azedo com queijo canastra.",
    "imagem": "img/pao-de-queijo.jpg"
  },
  {
    "id": 8,
    "nome": "Torta de Frango",
    "categoria": "salgados",
    "preco": 13,
    "descricao": "Fatia generosa com massa amanteigada e recheio de frango desfiado.",
    "imagem": "img/torta-de-frango.jpg"
  },
  {
    "id": 9,
    "nome": "Bolo de Milho Verde",
    "categoria": "doces",
    "preco": 9.5,
    "descricao": "Fatia de bolo cremoso feito com milho da feira do produtor.",
    "imagem": "img/bolo-de-milho.jpg"
  },
  {
    "id": 10,
    "nome": "Brownie de Castanha",
    "categoria": "doces",
    "preco": 11,
    "descricao": "Chocolate meio amargo com castanha-do-pará. Sem glúten.",
    "imagem": "img/brownie.jpg"
  }
]
```

> **⚠️ Atenção**
> Este arquivo é o **contrato** entre o seu back-end e o seu front-end. O `js/app.js` que veio da Aula 10 filtra por `produto.categoria === "geladas"`, mostra `produto.imagem` e formata `produto.preco` — se você renomear uma categoria ou apagar um campo aqui, a SPA quebra sem dar erro no servidor. Da Aula 12 até a 16 esses dez objetos continuam sendo a base; o que muda é quem os serve.

### Passo 6 — O `server.js` completo

`server.js`

```js
const path = require("node:path");
const fs = require("node:fs/promises");
const express = require("express");

const app = express();
const PORTA = process.env.PORT || 3000;
const CAMINHO_DADOS = path.join(__dirname, "data", "produtos.json");

// As quatro categorias do cardápio, na ordem em que aparecem no site.
// Este array substitui o data/categorias.json da Aula 10: a partir de hoje,
// quem publica a lista de categorias é a API, não um arquivo do front-end.
const CATEGORIAS = [
  { id: "cafes", nome: "Cafés" },
  { id: "geladas", nome: "Bebidas geladas" },
  { id: "salgados", nome: "Salgados" },
  { id: "doces", nome: "Doces" },
];

// ---------------------------------------------------------------
// Arquivos estáticos: o site das Unidades 1 e 2, servido por nós.
// ---------------------------------------------------------------
app.use(express.static(path.join(__dirname, "public")));

// ---------------------------------------------------------------
// Acesso aos dados
// ---------------------------------------------------------------
async function lerProdutos() {
  const conteudo = await fs.readFile(CAMINHO_DADOS, "utf-8");
  return JSON.parse(conteudo);
}

// ---------------------------------------------------------------
// API
// ---------------------------------------------------------------

// GET /api/produtos → lista completa do cardápio
app.get("/api/produtos", async (req, res) => {
  const produtos = await lerProdutos();
  res.json(produtos);
});

// GET /api/produtos/:id → um produto, ou 404
app.get("/api/produtos/:id", async (req, res) => {
  const id = Number(req.params.id);
  const produtos = await lerProdutos();
  const produto = produtos.find((p) => p.id === id);

  if (!produto) {
    return res.status(404).json({ erro: `Produto ${req.params.id} não encontrado` });
  }

  res.json(produto);
});

// GET /api/categorias → [{ id, nome }], só as categorias que têm produto hoje.
// O formato é o MESMO do antigo data/categorias.json, porque o front-end da
// Aula 10 monta o <select> lendo categoria.id e categoria.nome.
app.get("/api/categorias", async (req, res) => {
  const produtos = await lerProdutos();
  const usadas = new Set(produtos.map((p) => p.categoria));
  res.json(CATEGORIAS.filter((categoria) => usadas.has(categoria.id)));
});

// ---------------------------------------------------------------
app.listen(PORTA, () => {
  console.log(`Café Cerrado no ar em http://localhost:${PORTA}`);
});
```

Rode:

```bash
npm run dev
```

```text
Café Cerrado no ar em http://localhost:3000
```

Repare na decisão do `/api/categorias`: ele **não** devolve `["cafes", "doces", "geladas", "salgados"]`. Devolveria, se fosse só um `[...new Set(…)]` — e o `<select>` do cardápio ficaria com quatro opções escritas `[object Object]` ou, pior, com os ids técnicos na cara do usuário. O front-end da Aula 10 espera objetos com `id` (o valor da `<option>`) e `nome` (o texto). Um endpoint só é "pronto" quando devolve o formato que o consumidor precisa; a API existe para servir o cliente, não o contrário.

### Passo 7 — O front-end passa a consumir a sua API

Aqui está a recompensa de ter concentrado todo o `fetch` em um arquivo só na Aula 10. O front-end inteiro — o roteador por hash, o `index.html` com as três `<section data-rota>`, os ids `#cards`, `#status-cardapio`, `#resumo`, `#filtro-categoria`, o formulário de contato — **fica exatamente como está**. Você vai editar **duas linhas**, as duas dentro de `public/js/api.js`:

`public/js/api.js` (trecho — o resto do arquivo não muda)

```js
export function buscarProdutos() {
  return pegarJson("/api/produtos");        // antes: "data/produtos.json"
}

export function buscarCategorias() {
  return pegarJson("/api/categorias");      // antes: "data/categorias.json"
}
```

É isso. Salve, recarregue `http://localhost:3000` e o cardápio aparece — agora vindo do seu servidor.

Três detalhes valem o comentário:

- **A barra inicial importa.** `"/api/produtos"` é um caminho **absoluto na origem**: sempre resolve para `http://localhost:3000/api/produtos`, esteja você em `/`, em `/index.html#/cardapio` ou em qualquer rota futura. Sem a barra, o navegador resolveria em relação à página atual e um dia buscaria `/alguma/pasta/api/produtos`.
- **Mesma origem, zero CORS.** O site e a API saem do mesmo `http://localhost:3000`, então nenhum cabeçalho de CORS precisa ser configurado. Aquele erro de `Access-Control-Allow-Origin` da Aula 10 simplesmente não existe aqui — e é por isso que servir o front pelo próprio Express é o caminho mais curto até uma aplicação que funciona.
- **`data/categorias.json` foi aposentado.** Ele não existe mais no `cafe-cerrado-api` (o `cp` do Passo 4 copiou só o `produtos.json`), e a lista de categorias passa a nascer no `server.js`. Se você ainda tiver o arquivo no repositório antigo, deixe-o lá como histórico — mas nada mais o lê.

> **⚠️ Atenção**
> Não apague o `js/roteador.js` nem troque o `<script type="module">` por um script clássico. A SPA da Aula 10 depende dos dois: sem o roteador, as `<section data-rota>` continuam com `hidden` e a tela do cardápio nunca aparece, mesmo com a API respondendo `200`. Se o cardápio "sumiu" depois desta aula, o primeiro lugar para olhar é o console — um erro de `import` derruba o módulo inteiro em silêncio visual.

### Como testar

1. Com `npm run dev` rodando, abra `http://localhost:3000`. O site aparece **sem Live Server**, e o link **Cardápio** do menu leva a `http://localhost:3000/#/cardapio` com os dez cards.
2. Abra o DevTools na aba **Network**, recarregue e clique na requisição `produtos`. Confira: **Status** `200`, **Request URL** `http://localhost:3000/api/produtos`, aba **Response** com o array JSON de dez objetos.
3. Confira o `<select>` de categoria: cinco opções ("Todas" mais as quatro), com os textos "Cafés", "Bebidas geladas", "Salgados" e "Doces" — não com os ids técnicos.
4. No terminal, `curl -i http://localhost:3000/api/produtos/3` deve devolver o Cappuccino Sinop com status `200`.
5. `curl -i http://localhost:3000/api/produtos/999` deve devolver `404` e `{"erro":"Produto 999 não encontrado"}`.
6. `curl http://localhost:3000/api/categorias` deve devolver `[{"id":"cafes","nome":"Cafés"},{"id":"geladas","nome":"Bebidas geladas"},{"id":"salgados","nome":"Salgados"},{"id":"doces","nome":"Doces"}]`.
7. Edite `data/produtos.json`, mude um preço, **salve** e recarregue a página do navegador. O preço novo aparece sem reiniciar nada: o arquivo é lido a cada requisição.
8. Renomeie `data/produtos.json` para `data/produtos-x.json` e recarregue o cardápio. O front-end mostra a mensagem de erro e o botão "Tentar de novo" da Aula 09 — a camada de erro que você escreveu continua valendo com a API nova. Volte o nome depois.

Commit:

```bash
git add .
git commit -m "Servidor Express servindo o site e a API de produtos"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/cafe-cerrado-api.git
git push -u origin main
```

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Sem rodar, diga o que cada comando abaixo imprime (ou que erro dá). Depois rode e confira.

```bash
node -e "console.log(typeof window)"
node -e "console.log(typeof process)"
node -e "console.log([1,2,3].map(n => n * 2))"
node -e "console.log(document.title)"
```

**A2.** O `package.json` de um projeto tem `"express": "^5.1.0"`. Quais destas versões o `npm install` aceitaria instalar: `5.1.4`, `5.3.0`, `6.0.0`, `5.0.9`? Justifique cada uma em meia linha.

**A3.** Dado o `server.js` do Passo 6, o que acontece com uma requisição para `http://localhost:3000/api/produtos/dois`? Qual o status e qual o corpo da resposta? Explique o papel do `Number()` nesse resultado.

**A4.** Existe um arquivo `public/api/produtos` (sem extensão) com o texto `oi`. Qual das duas respostas o servidor devolve para `GET /api/produtos`: o arquivo ou a rota? Aponte a linha do `server.js` que decide isso.

**A5.** Complete o código para que a rota devolva apenas os produtos da categoria pedida, ignorando maiúsculas. Se a query string não vier, devolva a lista inteira.

```js
app.get("/api/produtos", async (req, res) => {
  const produtos = await lerProdutos();
  const categoria = req.query.categoria;

  // Escreva aqui: filtre por categoria quando ela existir.

  res.json(produtos);
});
```

**A6.** Um colega jura que corrigiu o bug, salvou o arquivo, e o navegador continua mostrando a resposta antiga. Ele está rodando `node server.js`. Cite duas causas possíveis e como distinguir uma da outra em dez segundos.

### Nível B — Aplicação

**B1.** Endpoint de busca. Acrescente ao `server.js` a rota `GET /api/produtos/busca/:termo`, que devolve os produtos cujo `nome` contenha o termo, sem diferenciar maiúsculas de minúsculas.

Resultado esperado: `curl http://localhost:3000/api/produtos/busca/cafe` devolve os dois cafés; `curl http://localhost:3000/api/produtos/busca/xyz` devolve `[]` com status `200` (lista vazia não é erro).

<details markdown="1">
<summary>Dica</summary>

Registre esta rota **antes** de `/api/produtos/:id`, senão `busca` vira o valor de `:id` e o `Number("busca")` produz `NaN`. `String.prototype.includes` combinado com `toLowerCase()` nos dois lados resolve a comparação.
</details>

**B2.** Estatísticas do cardápio. Crie `GET /api/estatisticas`, que devolve um objeto com `total` (quantidade de produtos), `precoMedio` (arredondado para duas casas) e `maisCaro` (o nome do produto de maior preço).

Resultado esperado: com o cardápio de hoje, `{"total":10,"precoMedio":11.2,"maisCaro":"Frappê de Café"}`.

<details markdown="1">
<summary>Dica</summary>

`reduce` para somar os preços (Aula 08), `Number(x.toFixed(2))` para arredondar mantendo o tipo número, e outro `reduce` (ou `sort` seguido de `at(-1)`) para o mais caro.
</details>

**B3.** A página que o servidor monta. Crie a rota `GET /cardapio-texto` que devolve uma resposta em **texto puro** (não JSON) listando os produtos, um por linha, no formato `Nome — R$ 7,50`.

Resultado esperado: abrir `http://localhost:3000/cardapio-texto` no navegador mostra seis linhas de texto sem formatação, e `curl -i` confirma `Content-Type: text/html` ou `text/plain`.

<details markdown="1">
<summary>Dica</summary>

`res.type("text/plain")` antes de `res.send(...)` define o cabeçalho. Para juntar as linhas, `produtos.map(...).join("\n")`.
</details>

**B4.** Servidor sem framework. Reescreva **só** o endpoint `GET /api/produtos` em um arquivo `exemplos/servidor-sem-express.js`, usando apenas o módulo `node:http`, e rode na porta 3001.

Resultado esperado: `curl -i http://localhost:3001/api/produtos` devolve o mesmo JSON e o mesmo `Content-Type` que a versão Express. Escreva em duas linhas, no topo do arquivo, o que o Express fez por você.

<details markdown="1">
<summary>Dica</summary>

Você vai precisar escrever `res.writeHead(200, { "Content-Type": "application/json; charset=utf-8" })` e `res.end(JSON.stringify(produtos))` na mão — é justamente esse o ponto do exercício.
</details>

### Nível C — Desafio em sala

**C1.** Paginação no servidor. Faça `GET /api/produtos` aceitar `?pagina=2&limite=2` e devolver um objeto — não mais um array cru — no formato `{ "dados": [...], "pagina": 2, "limite": 2, "total": 6, "totalPaginas": 3 }`. Sem query string, o comportamento padrão deve ser `pagina=1` e `limite=10`. Depois, ajuste o `public/js/app.js` para continuar funcionando com o novo formato e acrescente dois botões, "Anterior" e "Próxima", que ficam desabilitados nos extremos.

Resultado esperado: `curl "http://localhost:3000/api/produtos?pagina=3&limite=2"` devolve os dois últimos produtos e `"totalPaginas":3`; na tela, os botões navegam e o botão "Anterior" nasce desabilitado.

<details markdown="1">
<summary>Dica</summary>

`slice((pagina - 1) * limite, pagina * limite)` faz o recorte. Valide os dois parâmetros: `Number("abc")` é `NaN`, e `NaN` em um `slice` devolve resultados estranhos — use `Number.isInteger(x) && x > 0` antes de confiar. No front, guarde a página atual em uma variável de módulo e chame `carregarCardapio()` de novo a cada clique.
</details>

## 🏆 Desafios

### ⭐ O endpoint que ainda falta
Tags: node, express, api, json

O front-end do Café Cerrado precisa montar os botões de filtro por categoria, mas hoje ele só sabe pedir a lista inteira de produtos e deduzir as categorias no navegador — o que significa baixar seis produtos completos (com descrição e imagem) só para descobrir quatro palavras. O `server.js` desta aula já tem um `GET /api/categorias` que resolve metade do problema: ele devolve `["cafes","doces","geladas","salgados"]`, mas o front precisa também de quantos itens há em cada uma, para mostrar "Cafés (2)". Faça a API entregar exatamente o que a tela precisa, e nem um byte a mais.

**Critérios de pronto**

- `GET /api/categorias` devolve um array de objetos com `nome` e `quantidade`, ordenado por `nome`.
- A soma dos `quantidade` é igual ao total de produtos do arquivo (confira com `/api/produtos`).
- Acrescentar um produto de categoria nova em `data/produtos.json` faz a nova categoria aparecer na resposta sem alterar uma linha de código.
- O front-end monta os botões de filtro a partir desse endpoint, exibindo o rótulo no formato `Cafés (2)`.
- Um comentário de duas linhas no `server.js` compara o tamanho da resposta de `/api/categorias` com o de `/api/produtos` (use `curl -s ... | wc -c`).

<details markdown="1">
<summary>Pistas</summary>

1. O `reduce` da Aula 08 monta um objeto contador: `produtos.reduce((acc, p) => { acc[p.categoria] = (acc[p.categoria] ?? 0) + 1; return acc; }, {})`.
2. `Object.entries(contagem)` devolve pares `[nome, quantidade]` — de onde sai o `map` para o formato final.
3. Para ordenar textos em português (com acento), `array.sort((a, b) => a.nome.localeCompare(b.nome, "pt-BR"))`.
4. Rótulos bonitos ("Cafés" em vez de "cafes") são um problema de apresentação: resolva no front, com um objeto de tradução, e não polua a API.
</details>

### ⭐⭐ A API que não morre com um arquivo quebrado
Tags: node, express, bug, json

Abra `data/produtos.json`, apague uma vírgula qualquer no meio e salve. Agora recarregue o site. O que você vê? Provavelmente a página em branco, um erro feio no terminal e um usuário que nunca vai saber o que aconteceu. O arquivo é a única fonte de dados da sua API — e ele pode estar corrompido, sumido ou sem permissão de leitura. Descubra exatamente o que o Express 5 faz nesse caso, prove com evidência, e transforme o desastre em uma resposta honesta.

**Critérios de pronto**

- Um arquivo `docs/investigacao-erro.md` registra: a mensagem literal do terminal, o status HTTP devolvido ao cliente e o corpo da resposta, nos três cenários (JSON inválido, arquivo apagado, arquivo com permissão negada).
- Com o JSON inválido, a API responde `500` com um corpo JSON `{ "erro": "..." }` — nunca uma página HTML de erro, nunca o caminho do arquivo no seu computador.
- Com o arquivo apagado, a resposta é `500` e o terminal mostra um log com a mensagem completa do erro (incluindo o código `ENOENT`).
- O site mostra a mensagem de falha do `catch` em vez de ficar em branco.
- Uma frase no `docs/investigacao-erro.md` explica por que expor `error.stack` ao cliente é um risco de segurança.

<details markdown="1">
<summary>Pistas</summary>

1. Rode `curl -i http://localhost:3000/api/produtos` com o JSON quebrado antes de escrever qualquer código: o Express 5 já responde algo. O quê, exatamente?
2. Para simular permissão negada no Linux/macOS: `chmod 000 data/produtos.json` (e `chmod 644` depois para desfazer).
3. `try { ... } catch (erro) { ... }` dentro de `lerProdutos` permite distinguir os casos: `erro.code === "ENOENT"` é arquivo ausente; um `SyntaxError` é JSON inválido.
4. A resposta ao cliente deve ser genérica; o detalhe vai para o `console.error`. Esse par — log detalhado no servidor, mensagem genérica ao cliente — é a regra que vamos formalizar em um middleware na próxima aula.
</details>

### ⭐⭐ Express contra o módulo `http`, com números
Tags: node, http, refatoracao, investigacao

"Por que instalar um framework se o Node já tem um servidor embutido?" É uma pergunta legítima, e a resposta "porque todo mundo usa" não vale nada em uma prova ou em uma entrevista. Reimplemente a sua API inteira — as três rotas mais os arquivos estáticos — usando **apenas** `node:http`, `node:fs/promises` e `node:path`, e depois defenda uma das duas versões com evidência, não com opinião.

**Critérios de pronto**

- `exemplos/servidor-sem-express.js` responde, na porta 3001, exatamente às mesmas quatro coisas que a versão Express: `/api/produtos`, `/api/produtos/:id`, `/api/categorias` e os arquivos de `public/`.
- Os `Content-Type` batem com os da versão Express para HTML, CSS, JavaScript, imagem e JSON.
- Uma tabela no `README.md` compara as duas versões em três colunas: linhas de código, o que foi difícil, o que o Express faz de graça.
- O `curl -i` de `/api/produtos/999` devolve `404` com o mesmo corpo nas duas versões.
- Uma nota no `README.md` explica o que aconteceu ao tentar servir os arquivos estáticos na mão (esse é o ponto onde o Express ganha por muitos comprimentos).

<details markdown="1">
<summary>Pistas</summary>

1. `new URL(req.url, "http://localhost")` separa caminho e query string de graça — o `req.url` cru traz os dois grudados.
2. Parâmetros de rota, sem framework, viram manipulação de string: `caminho.split("/")` e comparação de posições.
3. Para os estáticos: leia o arquivo com `fs.readFile`, escolha o `Content-Type` por extensão (`path.extname`) e devolva `404` quando o `readFile` lançar `ENOENT`.
4. Cuidado com a travessia de diretório: uma requisição para `/../data/produtos.json` não pode devolver nada. Compare o caminho resolvido com `path.resolve` antes de abrir o arquivo — é justamente esse tipo de detalhe que o `express.static` já trata.
</details>

### ⭐⭐⭐ O 304 que ninguém vê
Tags: performance, http, express, devtools

Abra o DevTools na aba Network, recarregue o site e olhe a coluna Size do `estilo.css`: em vez do tamanho em kB, aparece `(disk cache)` ou o status `304`. O Express fez isso sozinho para os arquivos estáticos — mas a sua rota `/api/produtos` baixa o JSON inteiro toda vez, mesmo quando nada mudou no cardápio. Em uma cafeteria com trezentos produtos e mil visitas por dia, isso é tráfego jogado fora. Descubra como o navegador e o servidor combinam "não mudou nada desde a última vez" e aplique o mesmo mecanismo à sua API.

**Critérios de pronto**

- Um documento `docs/cache.md` explica, com as requisições capturadas no DevTools, o que são `ETag`, `If-None-Match`, `Last-Modified` e `If-Modified-Since`, e qual deles o `express.static` usou no seu CSS.
- `GET /api/produtos` passa a devolver um cabeçalho `ETag` calculado a partir do conteúdo do arquivo.
- Uma segunda requisição enviando `If-None-Match` com o mesmo valor recebe `304 Not Modified` **sem corpo**.
- Alterar `data/produtos.json` muda o `ETag` e a requisição seguinte volta a receber `200` com o corpo completo.
- Uma tabela no `docs/cache.md` compara os bytes transferidos antes e depois, medidos com `curl -s -w '%{size_download}\n' -o /dev/null`.
- Uma frase justifica por que um `Cache-Control: max-age=3600` puro seria a escolha **errada** para um cardápio que o dono edita durante o dia.

<details markdown="1">
<summary>Pistas</summary>

1. Comece medindo: `curl -i http://localhost:3000/css/estilo.css` duas vezes, a segunda com `-H "If-None-Match: <valor que veio>"`.
2. Um `ETag` é só uma impressão digital do conteúdo. `require("node:crypto").createHash("sha1").update(conteudo).digest("hex")` serve muito bem.
3. O cabeçalho enviado pelo cliente chega em `req.headers["if-none-match"]` — sempre em minúsculas, sempre string.
4. `res.status(304).end()` encerra sem corpo. Enviar corpo junto com 304 é violação da especificação HTTP e alguns clientes engasgam.
5. Para o caso do cardápio editado durante o dia, investigue a diretiva `no-cache` — que, apesar do nome, não significa "não guarde", e sim "guarde, mas confirme antes de usar".
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `Error: Cannot find module 'express'` | `npm install` não foi rodado, ou o terminal está em outra pasta | `cd` até a pasta com o `package.json` e rode `npm install` |
| `Error: listen EADDRINUSE: address already in use :::3000` | Já existe um servidor ocupando a porta 3000 (provavelmente o seu, de outra aba) | Feche o outro terminal, ou rode `PORT=3001 npm run dev` |
| `ReferenceError: document is not defined` | Código de front-end colado em arquivo de back-end | `document` só existe no navegador; mova o código para `public/js/app.js` |
| `SyntaxError: Cannot use import statement outside a module` | `import` em projeto CommonJS | Troque por `const x = require("...")` |
| `Cannot GET /cardapio.html` | Nenhuma rota casou e o arquivo não existe em `public/` | Confira o caminho do arquivo e se `express.static` aponta para a pasta certa |
| Alteração no código não surte efeito | O processo Node carregou a versão antiga na memória | Use `npm run dev` (`node --watch`), não `node server.js` |
| `Error: Cannot set headers after they are sent to the client` | Duas respostas na mesma requisição | Coloque `return` antes de cada `res.status(...).json(...)` intermediário |
| A rota `/api/produtos/:id` sempre devolve 404 | `req.params.id` é string e o `find` compara com número | `Number(req.params.id)` antes de comparar |
| `SyntaxError: Expected double-quoted property name in JSON at position 217` | `data/produtos.json` com vírgula sobrando, aspas simples ou comentário | Abra o arquivo no VS Code: o erro de sintaxe fica sublinhado |
| O site abre, mas o cardápio fica vazio e o console mostra 404 | O `fetch` ainda aponta para `data/produtos.json`, que saiu de `public/` | Troque a URL para `/api/produtos` |

## 🏠 Atividade assíncrona (1 h)

No **seu projeto autoral**, crie o repositório da Unidade 3 e repita a arquitetura de hoje com os seus dados:

1. Crie o repositório `<seu-projeto>-api` no GitHub, com `npm init -y`, `npm install express` e `.gitignore` contendo `node_modules/`.
2. Mova o site das Unidades 1 e 2 para `public/` e sirva-o com `express.static`. O Live Server deve deixar de ser necessário.
3. Tire o arquivo de dados de dentro de `public/` e coloque-o em `data/<seu-recurso>.json`, com no mínimo **seis** itens e os mesmos seis campos do modelo (`id`, `nome`, `categoria`, `preco`, `descricao`, `imagem` — adapte os nomes ao seu domínio).
4. Implemente `GET /api/<seu-recurso>` e `GET /api/<seu-recurso>/:id`, com `404` correto para id inexistente.
5. Aponte o `fetch` do seu front-end para a sua própria API e confirme os cards renderizando.
6. Acrescente ao `README.md` uma seção "Como rodar" com os três comandos necessários (`npm install`, `npm run dev`, endereço).

**Critério de pronto:** clonando o repositório em uma pasta vazia e rodando `npm install && npm run dev`, o site abre em `http://localhost:3000` com os dados vindos da API, e `curl -i http://localhost:3000/api/<seu-recurso>/999` devolve `404`.

**Entrega:** commit + push e link do repositório no SIGAA.

## ✅ Checkpoint do projeto

- [ ] Repositório novo, com `package.json`, `package-lock.json` e `.gitignore` versionados — e `node_modules/` fora do Git.
- [ ] `npm run dev` sobe o servidor e reinicia sozinho ao salvar um arquivo.
- [ ] `http://localhost:3000` serve o site das Unidades 1 e 2 pelo Express, sem Live Server.
- [ ] Os dados moram em `data/`, fora de `public/`, e não são baixáveis diretamente.
- [ ] `GET /api/<recurso>` devolve a lista completa com status `200` e `Content-Type: application/json`.
- [ ] `GET /api/<recurso>/:id` devolve o item com `200` e um erro em JSON com `404` quando o id não existe.
- [ ] O `fetch` do front-end usa caminho relativo (`/api/...`) e os cards aparecem na tela.
- [ ] `README.md` com a seção "Como rodar".

## 📚 Para aprofundar

- [Node.js — Introdução ao Node.js (pt-BR)](https://nodejs.org/pt-br/learn/getting-started/introduction-to-nodejs) — leia a página inteira; são dez minutos e resolvem metade das dúvidas de vocabulário.
- [Express — Hello World (pt-BR)](https://expressjs.com/pt-br/starter/hello-world.html) — o menor servidor possível, comentado linha a linha.
- [Express — Servindo arquivos estáticos (pt-BR)](https://expressjs.com/pt-br/starter/static-files.html) — leia com atenção a parte sobre caminho absoluto e `__dirname`.
- [Express — Roteamento básico (pt-BR)](https://expressjs.com/pt-br/guide/routing.html) — foque nos parâmetros de rota; o resto é a próxima aula.
- [MDN — Códigos de status de resposta HTTP](https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Status) — não decore os 60; entenda as cinco famílias (1xx a 5xx).
- [npm — package.json](https://docs.npmjs.com/cli/v10/configuring-npm/package-json) — consulte quando precisar; é referência, não leitura corrida.
- [Versionamento Semântico 2.0.0 (pt-BR)](https://semver.org/lang/pt-BR/) — as três primeiras seções explicam o `^` de uma vez por todas.
- QUEIRÓS, Ricardo; PORTELA, Filipe. *Introdução ao Desenvolvimento Moderno para a Web*. FCA — capítulo sobre a camada de back-end com Node.js.
- PUREWAL, Semmy. *Aprendendo a Desenvolver Aplicações Web*. Novatec — introdução ao Node.js e ao ecossistema npm.

Na próxima aula o `server.js` de arquivo único chega ao seu limite: as rotas ganham arquivo próprio com `express.Router`, o servidor aprende a receber dados de um `POST` com `express.json()`, e você conhece a peça que sustenta o Express inteiro — o **middleware** — junto com o tratamento centralizado de erros e o 404 da API.
