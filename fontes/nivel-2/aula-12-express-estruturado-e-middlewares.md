# Aula 12 — Express estruturado e middlewares

> **Nível 2 — Desenvolvimento Web** · Unidade 3: Web dinâmica server-side
> WebLab · UNEMAT — Campus Sinop
> **Tempo estimado:** 3 blocos de 50 min + 1 h de prática

O `server.js` da Aula 11 funciona: serve o site, devolve o cardápio em JSON e responde `404` para um id inexistente. Mas ele é um arquivo só, e um arquivo só não escala. Imagine quarenta rotas, validações, regras de negócio e log de acesso empilhados ali dentro. Hoje aplicamos ao servidor exatamente o princípio que você já usa no front desde a Unidade 1 — **separação de responsabilidades** —, só que entre arquivos. E, para isso, você precisa conhecer a peça que sustenta o Express inteiro: o **middleware**.

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Explicar o que é um middleware, ler a assinatura `(req, res, next)` e dizer por que "no Express, quase tudo é middleware".
- Prever a ordem de execução de uma cadeia de middlewares e diagnosticar uma requisição que fica pendurada.
- Receber dados de um `POST` com `express.json()` e explicar por que `req.body` vem `undefined` sem ele.
- Validar dados **no servidor** e responder com os status corretos: `201`, `400`, `404`.
- Organizar as rotas de um recurso em um arquivo próprio com `express.Router`, deixando o `server.js` só com a montagem.
- Centralizar o 404 da API e o tratamento de erros em middlewares registrados na ordem certa.
- Testar a API sem front-end, com um arquivo `testes.http` versionado junto com o projeto.

## 📋 Pré-requisitos

Na aula passada você criou o repositório `cafe-cerrado-api`, subiu um servidor Express 5, serviu o site pela pasta `public/` e escreveu os endpoints `GET /api/produtos`, `GET /api/produtos/:id` e `GET /api/categorias`. Tudo isso mora em um único `server.js`. Hoje esse arquivo é quebrado em peças, ganha a capacidade de **receber** dados (não só devolver) e aprende a falhar de forma organizada. Os três endpoints continuam existindo do começo ao fim — eles apenas mudam de casa, cada recurso no seu `Router`.

Antes de começar, confirme:

- [ ] `cafe-cerrado-api` clonado ou aberto, com `npm install` já rodado.
- [ ] `npm run dev` sobe o servidor e `http://localhost:3000` mostra o site.
- [ ] `curl -i http://localhost:3000/api/produtos` devolve `200` e o array de produtos.
- [ ] Extensão **REST Client** instalada no VS Code (`humao.rest-client`).
- [ ] `data/produtos.json` com pelo menos seis itens, cada um com `id`, `nome`, `categoria`, `preco`, `descricao` e `imagem`.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Middleware: assinatura, cadeia, ordem; `express.json()` e o primeiro `POST` |
| 2 | 50 min | `express.Router`, o `server.js` enxuto, 404 de API e tratador de erros |
| 3 | 50 min | Mão na massa: refatoração completa + `testes.http`; laboratório |

## 1. Middleware: a linha de montagem do Express

### 1.1 A definição, em uma frase

Um **middleware** é uma função que recebe `(req, res, next)` e roda entre a chegada da requisição e a resposta final. Ela pode fazer três coisas:

1. **Examinar ou modificar** `req` e `res` (por exemplo, acrescentar `req.usuario` depois de conferir um token).
2. **Responder e encerrar** a requisição ali mesmo (`res.json(...)`), sem chamar `next()`.
3. **Passar adiante**, chamando `next()`, para que o próximo middleware da fila decida o que fazer.

A analogia: uma linha de montagem com estações de inspeção. A peça (a requisição) entra por um lado e passa estação por estação. Cada estação pode carimbar a peça, rejeitá-la ali mesmo ou deixá-la seguir. Uma rota — `app.get("/api/produtos", ...)` — é só a última estação da linha, a que costuma produzir a resposta.

```js
// Middleware de log: roda para TODA requisição que chega ao servidor.
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} ${req.method} ${req.originalUrl}`);
  next(); // sem next(), a requisição "trava" aqui e nunca chega às rotas
});
```

### 1.2 A ordem de registro é a ordem de execução

Middlewares são registrados com `app.use(...)` (ou com `app.get`, `app.post`, etc.) e executados **na ordem em que aparecem no arquivo**. Não é uma sugestão: é o mecanismo. Trocar duas linhas de lugar muda o comportamento do servidor.

```js
app.use(express.json());                    // 1º: transforma o corpo JSON em objeto
app.use(registrarRequisicao);               // 2º: escreve no console o que chegou
app.use(express.static("public"));          // 3º: tenta achar um arquivo em public/
app.use("/api/produtos", produtosRouter);   // 4º: tenta casar com uma rota de produto
app.use("/api", naoEncontradoApi);          // 5º: só chega aqui quem não casou acima
app.use(tratadorDeErros);                   // 6º: só roda quando algo lançou erro
```

Uma requisição para `GET /css/estilo.css` percorre 1, 2, 3 — e para no 3, porque o arquivo existe. Uma requisição para `GET /api/produtos` percorre 1, 2, 3 (não achou arquivo), e para no 4. Uma requisição para `GET /api/pedidos` percorre 1, 2, 3, 4 (nenhuma rota de produto casou) e para no 5.

### 1.3 Você já usou dois middlewares sem saber

- **`express.static("public")`** é um middleware: ele procura o arquivo pedido; se acha, responde e encerra; se não acha, chama `next()` e a requisição segue.
- **As próprias rotas** são middlewares — só que com uma condição extra: só rodam se o **método** e o **caminho** casarem.

Ou seja, `app.get("/api/produtos", handler)` é açúcar sintático para "registre este middleware, mas só execute quando o método for `GET` e o caminho for `/api/produtos`".

### 1.4 O erro número 1: esquecer o `next()`

```js
// BUG: este middleware nunca deixa a requisição seguir.
app.use((req, res, next) => {
  console.log("Chegou:", req.originalUrl);
  // faltou o next() aqui
});
```

O servidor não quebra. Não há erro no terminal. Simplesmente **nada acontece**: o navegador fica com a abinha girando até desistir, e na aba Network o status da requisição é `(pending)` — pendente — para sempre. É um bug silencioso e assustador na primeira vez.

A regra que resolve: **todo middleware precisa terminar chamando `next()` ou enviando uma resposta.** Nunca as duas coisas, nunca nenhuma das duas.

> **🔬 Investigue**
> No seu `server.js`, acrescente logo no começo um middleware de log e **não** chame `next()`. Rode `npm run dev`, abra `http://localhost:3000` e observe: a aba Network do DevTools mostra a requisição em `(pending)`; o terminal mostra a linha de log. Agora abra outra aba e peça o CSS: a requisição também fica pendurada, mas o log aparece — prova de que o middleware rodou e a cadeia parou nele. Meça quanto tempo o Chrome espera antes de desistir. Depois acrescente o `next()` e confirme que tudo volta ao normal. Anote a diferença entre "servidor travado" e "requisição travada": o processo Node continua atendendo outras conexões o tempo todo.

## 2. Os middlewares que já vêm no Express

### 2.1 `express.json()`: recebendo dados de um `POST`

Na Aula 10 o seu front-end enviou `JSON.stringify(dados)` no corpo de um `POST`. Do lado do servidor, esse corpo chega como uma sequência de bytes crua — o Express não a interpreta sozinho, por decisão de projeto (nem toda API recebe JSON). É preciso ligar o parser:

```js
app.use(express.json()); // SEM esta linha, req.body é undefined
```

Com ele registrado, o Express olha o cabeçalho `Content-Type` da requisição; se for `application/json`, lê o corpo, converte com `JSON.parse` e deixa o resultado em `req.body`.

```js
app.post("/api/produtos", (req, res) => {
  const { nome, preco } = req.body; // o objeto enviado pelo fetch

  if (!nome || typeof preco !== "number") {
    return res.status(400).json({ erro: "Os campos nome e preco são obrigatórios." });
  }

  const novo = { id: proximoId++, nome, preco };
  produtos.push(novo);

  res.status(201).json(novo); // 201 Created + o recurso criado
});
```

> **⚠️ Atenção**
> No Express 5, `req.body` é `undefined` quando nenhum parser rodou — e não um objeto vazio. Destruturar `undefined` derruba a requisição com `TypeError: Cannot destructure property 'nome' of 'req.body' as it is undefined.` Se a mensagem aparecer, a causa é quase sempre uma destas três: falta `app.use(express.json())`; o parser foi registrado **depois** da rota; ou o cliente esqueceu o cabeçalho `Content-Type: application/json`.

> **💡 Dica**
> Tutoriais de Express 4 mandam rodar `npm install body-parser` e usar `bodyParser.json()`. Não instale nada: desde o Express 4.16 os parsers `express.json()` e `express.urlencoded()` são nativos, e no Express 5 continuam sendo. Uma dependência a menos.

### 2.2 `express.urlencoded()`: o formulário HTML clássico

Um `<form method="post">` sem JavaScript não envia JSON — envia `application/x-www-form-urlencoded`, o formato `nome=Cafe&preco=7.5`. Para lê-lo:

```js
app.use(express.urlencoded({ extended: true }));
```

Os dois parsers podem conviver: cada um olha o `Content-Type` e só age no formato que entende. O Café Cerrado usa JSON (o front envia por `fetch`), mas registrar os dois é barato e evita surpresa quando alguém testa com um formulário puro.

### 2.3 A regra de ouro da validação

Lembre das camadas: na Aula 03 o HTML validou com `required` e `type="email"`; na Aula 07 o JavaScript validou com mensagens por campo. E, mesmo assim, o servidor valida **de novo**. Por quê?

Porque qualquer pessoa pode mandar um `POST` direto para a sua API — com `curl`, com o REST Client, com um script de dez linhas — pulando o seu front-end inteiro. As validações do navegador servem para dar **feedback rápido e gentil** a quem está de boa-fé. A única validação em que se pode confiar é a que roda no servidor, porque é a única que o cliente não controla.

E validação de servidor não é opcional nem "nível avançado": é o mínimo. Sem ela, um `POST` com `{"preco": "de graça"}` entra na sua base e quebra a página de todo mundo na próxima renderização.

### 2.4 Os status HTTP que a sua API vai usar

| Código | Quando devolver |
|---|---|
| `200 OK` | Sucesso em consulta ou alteração, com corpo na resposta |
| `201 Created` | Recurso criado com sucesso — resposta típica do `POST` |
| `204 No Content` | Sucesso sem corpo — resposta típica do `DELETE` |
| `400 Bad Request` | Os dados enviados pelo cliente são inválidos |
| `404 Not Found` | O recurso pedido, ou a própria rota, não existe |
| `500 Internal Server Error` | Algo quebrou dentro do seu servidor |

`401` (não autenticado) e `403` (autenticado, mas sem permissão) entram na Aula 14, quando o login Google chegar.

> **📌 Vale gravar**
> A diferença entre `400` e `500` é de **culpa**. `4xx` diz "o problema está no que você mandou"; `5xx` diz "o problema está aqui dentro, desculpe". Devolver `500` para um campo faltando é mentir para o cliente: ele vai ficar tentando de novo, achando que é instabilidade do servidor, quando bastava corrigir o corpo da requisição.

> **🧠 Você sabia?**
> O Express foi criado em 2010 por TJ Holowaychuk, inspirado no Sinatra, um microframework de Ruby. A versão 4.0 saiu em 2014 — e a 5.0 só chegou dez anos depois, em 2024. Uma década com uma única versão maior é raríssimo em JavaScript, e explica um efeito colateral que você vai sentir a semana inteira: praticamente todo tutorial, resposta de fórum e trecho gerado por IA que você encontrar por aí foi escrito para o Express 4. É por isso que a ESPECIFICAÇÃO deste curso tem uma seção só de armadilhas de sintaxe. Hoje o projeto é mantido pela OpenJS Foundation, a mesma fundação que abriga o Node.js.

## 3. Escrevendo os seus próprios middlewares

### 3.1 Middleware de aplicação: roda para tudo

`middlewares/registro.js`

```js
// Registra no console o método, o caminho, o status e a duração de cada requisição.
function registrarRequisicao(req, res, next) {
  const inicio = Date.now();

  // O evento "finish" dispara quando a resposta terminou de ser enviada ao cliente.
  res.on("finish", () => {
    const duracao = Date.now() - inicio;
    console.log(`${req.method} ${req.originalUrl} → ${res.statusCode} (${duracao}ms)`);
  });

  next();
}

module.exports = registrarRequisicao;
```

Repare no truque: o middleware roda **antes** da rota, quando o status ainda não existe. Para saber o resultado, ele se inscreve no evento `finish` de `res` — o mesmo padrão de `addEventListener` que você usa no DOM — e só imprime quando a resposta já foi embora.

Saída típica no terminal:

```text
GET / → 200 (4ms)
GET /css/estilo.css → 200 (1ms)
GET /api/produtos → 200 (2ms)
GET /api/produtos/999 → 404 (1ms)
POST /api/produtos → 201 (3ms)
```

### 3.2 Middleware restrito a um prefixo

Quando `app.use` recebe um caminho como primeiro argumento, o middleware só roda para requisições que **começam** com aquele caminho:

```js
// Só roda para /api/qualquer-coisa
app.use("/api", (req, res, next) => {
  res.setHeader("X-API-Versao", "1.0");
  next();
});
```

Confira com `curl -i http://localhost:3000/api/produtos`: o cabeçalho `X-API-Versao: 1.0` aparece na resposta. Peça `curl -i http://localhost:3000/` e ele não aparece.

> **⚠️ Atenção**
> Dentro de um middleware montado em um prefixo, `req.url` vem **sem** o prefixo: em `GET /api/produtos`, o `req.url` vale `/produtos`. Isso é intencional (é o que permite ao Router ter caminhos relativos), mas estraga mensagens de log e de erro. Para o caminho completo, use sempre `req.originalUrl`.

### 3.3 Middleware de rota: roda só naquela rota

Middlewares também podem ser passados como argumentos extras, antes do handler final:

```js
// Confere se o :id é um número inteiro positivo antes de qualquer coisa.
function validarId(req, res, next) {
  const id = Number(req.params.id);

  if (!Number.isInteger(id) || id <= 0) {
    return res.status(400).json({ erro: `O id "${req.params.id}" não é um número válido.` });
  }

  req.idProduto = id; // deixa pronto para o handler, já convertido
  next();
}

// O middleware roda primeiro; o handler só é chamado se ele der next().
router.get("/:id", validarId, (req, res) => {
  const produto = produtos.find((p) => p.id === req.idProduto);
  if (!produto) return res.status(404).json({ erro: "Produto não encontrado." });
  res.json(produto);
});
```

Duas coisas boas aconteceram aí. A conversão e a validação do id saíram de dentro do handler — que agora só cuida da regra dele. E `req.idProduto` mostra o padrão mais comum de comunicação entre middlewares: **pendurar informação no `req`** para quem vier depois. É exatamente assim que o middleware de autenticação da Aula 14 vai entregar `req.usuario` às rotas.

> **🔎 Por baixo do capô**
> O `next()` não é mágica: o Express guarda a lista de middlewares que casaram com a requisição e mantém um índice interno apontando para o atual. Chamar `next()` incrementa esse índice e invoca o próximo da lista. Chamar `next()` **duas vezes** no mesmo middleware avança duas casas e costuma produzir `Error: Cannot set headers after they are sent to the client`, porque dois handlers tentam responder. E chamar `next(erro)` — com um argumento — faz o Express pular todos os middlewares normais restantes e ir direto para o primeiro middleware de erro registrado à frente.

## 4. Estruturando o projeto com `express.Router`

### 4.1 O problema do arquivo único

Cinco rotas em um `server.js` são confortáveis. Quinze já obrigam a rolar a tela para achar coisa. Quarenta, com validações e regras no meio, é um arquivo que ninguém quer abrir — e em que duas pessoas nunca conseguem trabalhar ao mesmo tempo sem conflito no Git.

### 4.2 O Router é um mini-app

`express.Router()` cria um objeto que se comporta como um `app` em miniatura: aceita `.get`, `.post`, `.use`, middlewares — tudo igual. A diferença é que ele não escuta em porta nenhuma; ele é **montado** dentro do app principal, sob um prefixo.

`routes/produtos.js`

```js
const express = require("express");

const router = express.Router();
const produtos = require("../data/produtos.json");

// Os caminhos aqui são RELATIVOS ao prefixo onde o router for montado.
// Montado em "/api/produtos", este "/" atende GET /api/produtos.
router.get("/", (req, res) => {
  res.json(produtos);
});

router.get("/:id", (req, res) => {
  const produto = produtos.find((p) => p.id === Number(req.params.id));

  if (!produto) {
    return res.status(404).json({ erro: `Produto ${req.params.id} não encontrado.` });
  }

  res.json(produto);
});

module.exports = router;
```

### 4.3 O `server.js` enxuto

`server.js`

```js
const path = require("node:path");
const express = require("express");
const produtosRouter = require("./routes/produtos");

const app = express();
const PORTA = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));
app.use("/api/produtos", produtosRouter); // prefixo + router

app.listen(PORTA, () => {
  console.log(`Café Cerrado no ar em http://localhost:${PORTA}`);
});
```

Leia esse arquivo em voz alta: "use o parser de JSON, sirva a pasta public, monte as rotas de produtos em `/api/produtos`, escute na porta". Ele virou um **índice** do projeto. Recurso novo — categorias, pedidos, avaliações — é um arquivo novo em `routes/` e **uma linha** aqui.

### 4.4 Onde os dados moram por enquanto

Repare na linha `const produtos = require("../data/produtos.json");`. Ela é diferente do que fizemos na Aula 11:

| Aula 11 | Aula 12 |
|---|---|
| `await fs.readFile(...)` a cada requisição | `require(...)` uma vez, na inicialização |
| Editar o JSON reflete na próxima requisição | O array vive em memória enquanto o servidor roda |
| Não dá para escrever nada | O `POST` consegue acrescentar itens ao array |

Por que a troca? Porque hoje a API precisa **receber** um produto, e o array em memória é o lugar mais simples para colocá-lo. A consequência é honesta e precisa ser dita: **o que você criar via `POST` desaparece quando o servidor reinicia.** Na próxima aula, com `fs/promises` e persistência de verdade, isso é resolvido — e é justamente por resolver isso que aquela aula existe.

> **💡 Dica**
> O `require` de um arquivo `.json` lê e converte o arquivo de forma **síncrona**, e guarda o resultado em cache: pedir o mesmo arquivo em dois módulos diferentes devolve exatamente o mesmo array na memória, não duas cópias. Isso é ótimo aqui (todo mundo vê a mesma lista) e é uma armadilha clássica quando você espera cópias independentes.

### 4.5 A árvore do projeto

```text
cafe-cerrado-api/
├── data/
│   └── produtos.json         # os dados
├── middlewares/
│   ├── erros.js              # 404 da API + tratador de erros
│   └── registro.js           # log de requisições
├── public/                   # o site das Unidades 1 e 2
│   ├── css/
│   ├── img/
│   ├── js/
│   │   └── app.js
│   └── index.html
├── routes/
│   └── produtos.js           # todas as rotas de /api/produtos
├── .gitignore
├── package.json
├── package-lock.json
├── server.js                 # só configuração e montagem
└── testes.http               # requisições de teste, versionadas
```

Compare com a estrutura da Aula 11: as pastas não são enfeite. Cada nome responde a uma pergunta ("onde estão as rotas?", "onde está o log?") sem que ninguém precise abrir arquivo nenhum.

## 5. Tratando o que dá errado

### 5.1 O 404 da API

Hoje, se alguém pedir `GET /api/pedidos` — uma rota que não existe —, o Express responde com uma página HTML dizendo `Cannot GET /api/pedidos`. Para um navegador, tudo bem. Para um `fetch` esperando JSON, é péssimo: `resposta.json()` lança `SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON`, e o erro que aparece no console do usuário não tem nada a ver com o problema real.

A solução é um middleware registrado **depois** de todas as rotas de API:

`middlewares/erros.js` (primeira metade)

```js
// Só chega aqui quem pediu algo em /api e não casou com nenhuma rota.
function naoEncontradoApi(req, res) {
  res.status(404).json({
    erro: `A rota ${req.method} ${req.originalUrl} não existe nesta API.`,
  });
}
```

```js
// server.js — DEPOIS de app.use("/api/produtos", produtosRouter)
app.use("/api", naoEncontradoApi);
```

### 5.2 O curinga do Express 5

E os caminhos que não começam com `/api`? Como o Café Cerrado é uma SPA (Aula 10), a resposta certa é devolver o `index.html` e deixar o roteador do front decidir o que mostrar. Para casar com "qualquer caminho", o Express 5 exige um curinga **nomeado**:

```js
// server.js — depois do 404 da API
app.get("/{*splat}", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});
```

As chaves em `/{*splat}` tornam o trecho opcional, de modo que o padrão casa também com a raiz `/`. O nome `splat` é livre — poderia ser `caminho` — e o valor capturado fica em `req.params.splat`, como um array de segmentos.

> **⚠️ Atenção**
> No Express 4 escrevia-se `app.get("*", handler)`. No Express 5 isso derruba o servidor na inicialização com `TypeError: Missing parameter name at 1`. A mudança veio da biblioteca de rotas (`path-to-regexp`), que passou a exigir nome em todo curinga. Se você copiar um `app.get("*")` de um tutorial, é este o erro que vai aparecer — e ele acontece antes mesmo de o servidor subir, o que ao menos é fácil de perceber.

### 5.3 O middleware de erro: quatro parâmetros

O Express reconhece um middleware de erro pela **quantidade de parâmetros**: quatro, começando por `err`. Não é pelo nome nem pela posição — é pela aridade da função.

`middlewares/erros.js` (segunda metade)

```js
// QUATRO parâmetros = middleware de erro. O "next" precisa existir mesmo sem uso.
function tratadorDeErros(err, req, res, next) {
  // Log completo para o desenvolvedor: aparece no terminal do servidor.
  console.error(`[erro] ${req.method} ${req.originalUrl}`);
  console.error(err);

  // JSON malformado no corpo: o próprio express.json() marca o erro com status 400.
  if (err.status === 400 && err.type === "entity.parse.failed") {
    return res.status(400).json({ erro: "O corpo da requisição não é um JSON válido." });
  }

  // Resposta genérica para o cliente: nunca exponha detalhes internos.
  res.status(500).json({ erro: "Erro interno do servidor." });
}

module.exports = { naoEncontradoApi, tratadorDeErros };
```

```js
// server.js — a ÚLTIMA linha antes do app.listen
app.use(tratadorDeErros);
```

O parâmetro `next` fica ali sem ser usado, e isso incomoda todo mundo na primeira vez. Ele é obrigatório: retire-o e a função passa a ter três parâmetros, o Express deixa de reconhecê-la como tratador de erros e passa a tratá-la como middleware comum — que nunca vai rodar, porque está registrada depois de todas as rotas.

### 5.4 Por que o tratador de erros vem por último

O Express percorre a fila na ordem de registro. Quando algo lança um erro, ele **pula** todos os middlewares comuns restantes e procura o próximo middleware **de erro à frente** na fila — nunca para trás. Registrar o tratador antes das rotas o tornaria inalcançável.

```text
requisição
    │
    ▼
express.json() ─────► ok, next()
    │
    ▼
registrarRequisicao ► ok, next()
    │
    ▼
produtosRouter ─────► lançou um erro
    │                      │
    │        o Express pula os middlewares comuns
    │        e procura o próximo DE ERRO à frente
    ▼                      ▼
naoEncontradoApi       tratadorDeErros
(não roda)             (roda: responde 500)
```

A ordem — rotas, depois 404, depois tratador de erros — não é questão de estilo. É a única ordem em que os três cumprem o papel deles.

### 5.5 Erros dentro de handlers `async`

No Express 5, um `throw` dentro de um handler `async` é capturado automaticamente e encaminhado ao tratador de erros. Você viu isso na Aula 11; agora dá para provar, porque o tratador existe:

```js
// Rota de teste: derruba de propósito, para ver o tratador funcionando.
// Acrescente-a TEMPORARIAMENTE ao routes/produtos.js, rode o curl abaixo e
// apague-a em seguida — ela não entra no arquivo final do Mão na massa.
router.get("/teste/erro", async (req, res) => {
  throw new Error("Explosão proposital para testar o tratador de erros");
});
```

`curl -i http://localhost:3000/api/produtos/teste/erro` devolve:

```text
HTTP/1.1 500 Internal Server Error
Content-Type: application/json; charset=utf-8

{"erro":"Erro interno do servidor."}
```

E o terminal mostra a mensagem completa com a pilha de chamadas. Esse par — **log detalhado no servidor, mensagem genérica ao cliente** — é uma regra de segurança, não de organização. Um `stack trace` devolvido ao navegador entrega o caminho absoluto das suas pastas, os nomes dos seus arquivos e, muitas vezes, o trecho da consulta ao banco. É presente para quem estiver procurando uma brecha.

> **📌 Vale gravar**
> Três perguntas que valem a pena revisar sobre esta seção: (1) O que identifica um middleware de erro? **Ter quatro parâmetros.** (2) Por que ele precisa ser o último registrado? **Porque o Express só procura tratadores de erro à frente na fila.** (3) O que muda no Express 5 quanto a handlers `async`? **Exceções e Promises rejeitadas passam a ser capturadas automaticamente, sem `try/catch` nem pacotes auxiliares.**

## 🧩 Padrão de projeto em uso

> ### 🧩 Padrão de projeto em uso — Chain of Responsibility
>
> A fila `express.json() → registrarRequisicao → express.static → produtosRouter → naoEncontradoApi → tratadorDeErros` é uma implementação do padrão comportamental **Chain of Responsibility** ("corrente de responsabilidade"): um pedido percorre uma corrente de manipuladores, e **cada elo decide** se trata o pedido e encerra, ou se o repassa ao próximo. Quem envia a requisição não sabe — e não precisa saber — qual elo vai atendê-la.
>
> Os dois efeitos que você sente na prática vêm direto do padrão. Primeiro, **a ordem é o desenho**: cada elo só recebe o pedido se o anterior decidiu repassá-lo, e é por isso que trocar duas linhas de `app.use` muda o comportamento do servidor. Segundo, **os elos são independentes**: acrescentar autenticação na Aula 14 será encaixar mais um elo na corrente, sem tocar em nenhum dos outros.
>
> Você já viu a mesma ideia no front-end, com outro nome: a **propagação de eventos** do DOM. Um clique sobe do `<button>` para o `<div>` e daí para o `document`, e qualquer listener no caminho pode tratar o evento e interromper a subida com `stopPropagation()`. `next()` e `stopPropagation()` resolvem o mesmo problema pelos dois lados: um manda seguir, o outro manda parar.

## 💻 Mão na massa — o Café Cerrado ganha estrutura

Vamos refatorar o `cafe-cerrado-api` inteiro. Ao final, o `server.js` terá menos de vinte linhas úteis e a API aceitará cadastro de produtos.

### Passo 1 — Criar as pastas

```bash
cd cafe-cerrado-api
mkdir routes middlewares
```

### Passo 2 — O log de requisições

`middlewares/registro.js`

```js
// Registra método, caminho, status e duração de cada requisição atendida.
function registrarRequisicao(req, res, next) {
  const inicio = Date.now();

  res.on("finish", () => {
    const duracao = Date.now() - inicio;
    console.log(`${req.method} ${req.originalUrl} → ${res.statusCode} (${duracao}ms)`);
  });

  next();
}

module.exports = registrarRequisicao;
```

### Passo 3 — O 404 da API e o tratador de erros

`middlewares/erros.js`

```js
// Middleware do 404 da API: registrado DEPOIS de todas as rotas de /api.
function naoEncontradoApi(req, res) {
  res.status(404).json({
    erro: `A rota ${req.method} ${req.originalUrl} não existe nesta API.`,
  });
}

// Middleware de erro: reconhecido pelos QUATRO parâmetros. Vai por último.
function tratadorDeErros(err, req, res, next) {
  console.error(`[erro] ${req.method} ${req.originalUrl}`);
  console.error(err);

  if (err.status === 400 && err.type === "entity.parse.failed") {
    return res.status(400).json({ erro: "O corpo da requisição não é um JSON válido." });
  }

  res.status(500).json({ erro: "Erro interno do servidor." });
}

module.exports = { naoEncontradoApi, tratadorDeErros };
```

### Passo 4 — As rotas de produtos

`routes/produtos.js`

```js
const express = require("express");

const router = express.Router();

// Carregado uma vez, na inicialização. O array vive em memória enquanto o
// servidor roda — a persistência em arquivo chega na próxima aula.
const produtos = require("../data/produtos.json");

// Próximo id disponível: o maior id existente mais um.
let proximoId = produtos.reduce((maior, p) => Math.max(maior, p.id), 0) + 1;

// Middleware de rota: valida e converte o :id antes de qualquer handler.
function validarId(req, res, next) {
  const id = Number(req.params.id);

  if (!Number.isInteger(id) || id <= 0) {
    return res.status(400).json({ erro: `O id "${req.params.id}" não é um número válido.` });
  }

  req.idProduto = id;
  next();
}

// GET /api/produtos → lista completa, com filtro opcional por categoria
router.get("/", (req, res) => {
  const { categoria } = req.query;

  if (!categoria) {
    return res.json(produtos);
  }

  const filtrados = produtos.filter(
    (p) => p.categoria.toLowerCase() === categoria.toLowerCase(),
  );
  res.json(filtrados);
});

// GET /api/produtos/:id → um produto, ou 404
router.get("/:id", validarId, (req, res) => {
  const produto = produtos.find((p) => p.id === req.idProduto);

  if (!produto) {
    return res.status(404).json({ erro: `Produto ${req.idProduto} não encontrado.` });
  }

  res.json(produto);
});

// POST /api/produtos → cria um produto. Validação obrigatória no servidor.
router.post("/", (req, res) => {
  const { nome, categoria, preco, descricao, imagem } = req.body;
  const problemas = [];

  if (typeof nome !== "string" || nome.trim().length < 3) {
    problemas.push("nome deve ser um texto com pelo menos 3 caracteres");
  }
  if (typeof categoria !== "string" || categoria.trim() === "") {
    problemas.push("categoria é obrigatória");
  }
  if (typeof preco !== "number" || Number.isNaN(preco) || preco <= 0) {
    problemas.push("preco deve ser um número maior que zero");
  }

  if (problemas.length > 0) {
    return res.status(400).json({ erro: "Dados inválidos.", problemas });
  }

  const novo = {
    id: proximoId++,
    nome: nome.trim(),
    categoria: categoria.trim().toLowerCase(),
    preco,
    descricao: typeof descricao === "string" ? descricao.trim() : "",
    imagem: typeof imagem === "string" ? imagem.trim() : "img/sem-foto.jpg",
  };

  produtos.push(novo);

  res.status(201).json(novo);
});

module.exports = router;
```

### Passo 5 — As rotas de categorias

O `GET /api/categorias` da Aula 11 não pode sumir na refatoração: o `<select>` de categoria da SPA depende dele. Ele sai do `server.js` e vira o segundo Router do projeto — pequeno, mas com o mesmo formato dos demais.

`routes/categorias.js`

```js
const express = require("express");

const router = express.Router();

// O MESMO array que routes/produtos.js carregou: o require guarda o módulo em
// cache, então os dois arquivos enxergam o mesmo objeto na memória.
const produtos = require("../data/produtos.json");

// As quatro categorias do cardápio, na ordem em que aparecem no site.
// Esta lista estava no server.js da Aula 11; ela só mudou de arquivo.
const CATEGORIAS = [
  { id: "cafes", nome: "Cafés" },
  { id: "geladas", nome: "Bebidas geladas" },
  { id: "salgados", nome: "Salgados" },
  { id: "doces", nome: "Doces" },
];

// GET /api/categorias → [{ id, nome }], só as categorias que têm produto hoje
router.get("/", (req, res) => {
  const usadas = new Set(produtos.map((p) => p.categoria));
  res.json(CATEGORIAS.filter((categoria) => usadas.has(categoria.id)));
});

module.exports = router;
```

Doze linhas úteis, um recurso inteiro. É essa a promessa do `express.Router`: recurso novo é arquivo novo, e o `server.js` cresce **uma** linha.

### Passo 6 — O `server.js` enxuto

`server.js`

```js
const path = require("node:path");
const express = require("express");

const produtosRouter = require("./routes/produtos");
const categoriasRouter = require("./routes/categorias");
const registrarRequisicao = require("./middlewares/registro");
const { naoEncontradoApi, tratadorDeErros } = require("./middlewares/erros");

const app = express();
const PORTA = process.env.PORT || 3000;

// 1. Corpo JSON das requisições vira objeto em req.body
app.use(express.json());

// 2. Log de tudo que chega
app.use(registrarRequisicao);

// 3. Arquivos estáticos: o site das Unidades 1 e 2
app.use(express.static(path.join(__dirname, "public")));

// 4. Rotas da API — um app.use por recurso
app.use("/api/produtos", produtosRouter);
app.use("/api/categorias", categoriasRouter);

// 5. Qualquer /api que não casou acima vira 404 em JSON
app.use("/api", naoEncontradoApi);

// 6. Qualquer outro caminho devolve o index.html (a SPA cuida do resto)
app.get("/{*splat}", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

// 7. Tratador de erros: SEMPRE o último
app.use(tratadorDeErros);

app.listen(PORTA, () => {
  console.log(`Café Cerrado no ar em http://localhost:${PORTA}`);
});
```

Sete blocos comentados, sete responsabilidades, nenhuma regra de negócio. Esse é o formato de `server.js` que o projeto vai manter até a Aula 16 — inclusive o fallback `/{*splat}`, que é o que mantém a SPA da Aula 10 funcionando quando alguém recarrega a página em `/#/cardapio`.

### Passo 7 — O arquivo de testes

Crie na raiz do projeto:

`testes.http`

```http
@base = http://localhost:3000

### Listar todos os produtos (espera 200)
GET {{base}}/api/produtos

### Filtrar por categoria (espera 200 com só os cafés)
GET {{base}}/api/produtos?categoria=cafes

### Buscar um produto existente (espera 200)
GET {{base}}/api/produtos/1

### Buscar um produto inexistente (espera 404 em JSON)
GET {{base}}/api/produtos/999

### Id que não é número (espera 400)
GET {{base}}/api/produtos/abacaxi

### Listar as categorias (espera 200 com objetos {id, nome})
GET {{base}}/api/categorias

### Criar um produto válido (espera 201 + o recurso criado)
POST {{base}}/api/produtos
Content-Type: application/json

{
  "nome": "Suco de Cupuaçu",
  "categoria": "geladas",
  "preco": 10.5,
  "descricao": "Polpa batida na hora com água gelada e um fio de mel.",
  "imagem": "img/suco-cupuacu.jpg"
}

### Criar sem nome (espera 400 com a lista de problemas)
POST {{base}}/api/produtos
Content-Type: application/json

{
  "categoria": "doces",
  "preco": 10.5
}

### Preço como texto (espera 400)
POST {{base}}/api/produtos
Content-Type: application/json

{
  "nome": "Café gelado da casa",
  "categoria": "geladas",
  "preco": "dez reais"
}

### JSON malformado (espera 400 vindo do express.json)
POST {{base}}/api/produtos
Content-Type: application/json

{
  "nome": "Café",
}

### Rota de API que não existe (espera 404 em JSON)
GET {{base}}/api/pedidos

### Caminho fora da API (espera o index.html)
GET {{base}}/qualquer-coisa
```

No VS Code, com o REST Client instalado, aparece um link **Send Request** acima de cada bloco `###`. Clique e a resposta abre ao lado, com status, cabeçalhos e corpo.

> **💡 Dica**
> `@base = http://localhost:3000` é uma variável do REST Client. Quando o projeto for publicado (trilha Deploy), você troca **uma** linha para testar o servidor de produção. Alternativas ao REST Client: Postman e Insomnia, com interface gráfica. A vantagem de um `testes.http` é ele ser texto puro: entra no Git, aparece no `diff`, e quem clonar o repositório recebe a bateria de testes junto com o código.

### Como testar

1. `npm run dev`. O terminal mostra `Café Cerrado no ar em http://localhost:3000`.
2. Abra `http://localhost:3000` e navegue pelo site. O terminal deve imprimir uma linha de log por arquivo carregado, com status e duração.
3. No `testes.http`, dispare os blocos de cima para baixo e confira os status: `200`, `200`, `200`, `404`, `400`, `200`, `201`, `400`, `400`, `400`, `404`, `200`.
4. Depois do `POST` que devolveu `201`, dispare de novo o primeiro bloco: o "Suco de Cupuaçu" está na lista, com o id `11` — o seguinte ao do último produto do cardápio.
5. Pare o servidor (<kbd>Ctrl</kbd>+<kbd>C</kbd>), suba de novo e liste outra vez: o suco sumiu. É o comportamento esperado hoje — e o problema que a próxima aula resolve.
6. Peça `curl -i http://localhost:3000/api/pedidos`: a resposta é `404` com `Content-Type: application/json`, não uma página HTML.
7. Comente a linha `app.use(express.json());` do `server.js`, salve e dispare o `POST` válido: veja o `500` e a mensagem `TypeError: Cannot destructure property 'nome' of 'req.body' as it is undefined.` no terminal. Descomente antes de seguir.

Commit:

```bash
git add .
git commit -m "Rotas em Router, middlewares de log e erro, POST com validacao e testes.http"
git push
```

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Dada a cadeia abaixo, diga por quais middlewares passa cada uma destas três requisições: `GET /css/estilo.css`, `GET /api/produtos/1`, `GET /api/avaliacoes`.

```js
app.use(express.json());
app.use(registrarRequisicao);
app.use(express.static("public"));
app.use("/api/produtos", produtosRouter);
app.use("/api", naoEncontradoApi);
app.use(tratadorDeErros);
```

**A2.** O que acontece com uma requisição que chega neste middleware? Descreva o que o usuário vê no navegador e o que aparece no terminal.

```js
app.use((req, res, next) => {
  console.log("passei por aqui");
});
```

**A3.** Um colega registrou `app.use(express.json())` **depois** de `app.use("/api/produtos", produtosRouter)`. O `GET` continua funcionando e o `POST` quebra. Explique por quê, em duas linhas.

**A4.** Qual destas quatro funções o Express trata como middleware de erro? Justifique.

```js
const a = (req, res, next) => {};
const b = (err, req, res) => {};
const c = (err, req, res, next) => {};
const d = (erro, requisicao, resposta, proximo) => {};
```

**A5.** Dentro de um middleware montado com `app.use("/api", fn)`, uma requisição para `GET /api/produtos/3` chega com `req.url` valendo o quê? E `req.originalUrl`? Qual dos dois você usaria na mensagem do 404 e por quê?

**A6.** Complete o middleware para que ele bloqueie qualquer requisição cujo corpo seja maior que 10 campos, respondendo `400`. Ele deve deixar passar todas as outras.

```js
function limitarCampos(req, res, next) {
  const quantidade = Object.keys(req.body ?? {}).length;

  // Escreva aqui a verificação e a resposta 400.

  next();
}
```

### Nível B — Aplicação

**B1.** Produtos de uma categoria. Acrescente ao `routes/categorias.js` do Mão na massa a rota `GET /api/categorias/:id/produtos`, que devolve os produtos daquela categoria — sem tocar no `server.js` e sem duplicar o filtro que já existe em `routes/produtos.js`.

Resultado esperado: `curl http://localhost:3000/api/categorias/cafes/produtos` devolve os quatro cafés; `curl http://localhost:3000/api/categorias/geladas/produtos` devolve os dois itens gelados; uma categoria inexistente devolve `[]` com status `200`.

<details markdown="1">
<summary>Dica</summary>

O `app.use("/api/categorias", categoriasRouter)` já existe desde o Passo 5: dentro do router, o caminho novo é `"/:id/produtos"`. O filtro é o mesmo `produtos.filter((p) => p.categoria === req.params.id)`; se quiser evitar a duplicação de verdade, extraia a comparação para uma função em um arquivo compartilhado e chame-a nos dois routers.
</details>

**B2.** Middleware de autorização simulada. Escreva `middlewares/chaveApi.js`, que exige o cabeçalho `X-Chave-Api: cafe-cerrado-2` em todas as requisições `POST` de `/api`. Sem o cabeçalho, responde `401` com `{ "erro": "..." }`; com ele, chama `next()`.

Resultado esperado: o `POST` do `testes.http` passa a devolver `401`; acrescentando a linha `X-Chave-Api: cafe-cerrado-2` ao bloco, volta a devolver `201`. Os `GET` continuam funcionando sem o cabeçalho.

<details markdown="1">
<summary>Dica</summary>

Cabeçalhos chegam sempre em minúsculas: `req.headers["x-chave-api"]`. Para agir só no `POST`, teste `req.method !== "POST"` e chame `next()` de imediato. Isto é um ensaio do middleware `exigirLogin` da Aula 14 — lá a chave vira um token de verdade.
</details>

**B3.** Validação extraída para middleware. Tire o bloco de validação de dentro do `POST` e transforme-o em um middleware `validarProduto` registrado como argumento da rota. O handler deve ficar com no máximo dez linhas.

Resultado esperado: os mesmos status de antes (`201` e `400` com a lista de problemas), mas o handler do `POST` só monta o objeto e responde. O middleware fica em `middlewares/validarProduto.js`.

<details markdown="1">
<summary>Dica</summary>

`router.post("/", validarProduto, (req, res) => { ... })`. O middleware pode até normalizar os dados (`nome.trim()`) e devolvê-los prontos em `req.produtoValidado`, poupando o handler.
</details>

**B4.** O `testes.http` completo. Amplie o arquivo para cobrir, além do que já existe, os casos: filtro por categoria inexistente, `POST` com preço negativo, `POST` com nome de dois caracteres e requisição a `/api/produtos/0`. Cada bloco deve ter, no título, o status esperado.

Resultado esperado: quatro blocos novos, todos disparados com sucesso e com o status previsto batendo com o obtido. Nenhum deles derruba o servidor.

<details markdown="1">
<summary>Dica</summary>

`/api/produtos/0` é o caso que separa `Number.isInteger(id)` de `id > 0`. Se a sua validação usar só `isNaN`, o zero passa — e passar zero significa procurar um produto que jamais existirá, gastando um `404` onde cabia um `400`.
</details>

### Nível C — Desafio

**C1.** Corrente completa com prioridade. Implemente um middleware `medirLento` que registre no console, em destaque, toda requisição que demore mais de 50 ms, e um middleware `simularLatencia` que — só quando a query string trouxer `?lento=1` — atrase a resposta em 300 ms antes de chamar `next()`. Depois, prove que a corrente funciona: mostre no terminal um `GET /api/produtos` normal e um `GET /api/produtos?lento=1`, e explique por que o `simularLatencia` precisa estar registrado **antes** das rotas e o `medirLento` **antes** dele.

Resultado esperado: no terminal, `GET /api/produtos → 200 (2ms)` e `GET /api/produtos?lento=1 → 200 (301ms)  [LENTO]`; a explicação da ordem em três linhas de comentário no topo do `server.js`.

<details markdown="1">
<summary>Dica</summary>

Para atrasar sem travar o event loop, `setTimeout(next, 300)` — nunca um laço `while` contando tempo, que bloqueia o processo inteiro e faz o servidor parar de atender todo mundo. Para o `medirLento`, reaproveite o `res.on("finish", ...)` do middleware de log: a duração já está calculada ali. E lembre que `req.query.lento` chega como a string `"1"`, não como número.
</details>

## 🏆 Desafios

### ⭐ O crachá de cada requisição
Tags: express, middleware, node, investigacao

Duas pessoas abrem o cardápio ao mesmo tempo e o seu terminal cospe seis linhas de log embaralhadas: não dá para saber quais linhas pertencem a qual visita. Serviços de verdade resolvem isso dando um **identificador único** a cada requisição, que acompanha a requisição do começo ao fim e volta ao cliente em um cabeçalho — é assim que o suporte de uma empresa pede "me manda o id da requisição" e acha o problema em segundos. Dê um crachá a cada requisição do Café Cerrado.

**Critérios de pronto**

- Um middleware registrado antes de todos os outros gera um identificador único e o guarda em `req.id`.
- Todas as linhas de log daquela requisição — a de entrada e a de saída — começam com o mesmo identificador.
- A resposta traz o identificador no cabeçalho `X-Requisicao-Id`, verificável com `curl -i`.
- O tratador de erros inclui o identificador tanto no log do servidor quanto no JSON devolvido ao cliente.
- Um parágrafo no `README.md` explica em que situação real esse identificador salva tempo.

<details markdown="1">
<summary>Pistas</summary>

1. `require("node:crypto").randomUUID()` gera um identificador único sem instalar nada.
2. Um UUID inteiro polui o terminal; `.slice(0, 8)` é suficiente para distinguir requisições de uma aula.
3. `res.setHeader("X-Requisicao-Id", req.id)` precisa acontecer **antes** de qualquer `res.json` ou `res.send` — cabeçalhos não podem ser definidos depois do corpo enviado.
4. Devolver o identificador junto do erro é seguro (é um número aleatório, não revela nada) e é o que permite ao usuário reportar o problema de forma útil.
</details>

### ⭐⭐ O `next()` que ninguém chamou
Tags: express, middleware, bug, devtools

Um colega mexeu no `server.js` sem avisar e agora o site "não abre mais": a aba do navegador fica girando indefinidamente, o terminal não mostra erro nenhum e o processo Node continua vivo, sem consumir CPU. O `curl` também fica pendurado. Nenhum `console.log` que você acrescentar no handler da rota aparece. Este é o trecho alterado:

```js
app.use((req, res, next) => {
  if (req.originalUrl.startsWith("/api")) {
    res.setHeader("X-API-Versao", "1.0");
  } else {
    next();
  }
});
```

Antes de corrigir, diagnostique: por que o site abre e a API não? Ou o contrário? Prove o que está acontecendo antes de tocar no código.

**Critérios de pronto**

- Um arquivo `docs/diagnostico-pendente.md` registra: o que a aba Network mostra (status e tempo), o que o `curl -v` mostra, e o que aparece (ou não) no terminal do servidor.
- O diagnóstico explica, em três linhas, qual caminho de execução deixa a requisição pendurada e por quê.
- A correção mantém o cabeçalho `X-API-Versao` nas rotas de API e devolve o comportamento normal a todas as requisições.
- Um teste no `testes.http` prova que `/api/produtos` responde `200` **com** o cabeçalho e que `/` responde `200` sem ele.
- Uma frase no arquivo explica por que esse tipo de bug não gera nenhuma mensagem de erro.

<details markdown="1">
<summary>Pistas</summary>

1. Leia o `if` com calma: em qual dos dois ramos o `next()` é chamado?
2. `curl -v --max-time 5 http://localhost:3000/api/produtos` desiste em cinco segundos e mostra exatamente onde travou.
3. Definir um cabeçalho **não** envia a resposta. Só `res.json`, `res.send`, `res.end` e companhia encerram o ciclo.
4. A correção certa não é acrescentar um `res.end()` no ramo do `if` — pense em qual das três coisas que um middleware pode fazer está faltando ali.
</details>

### ⭐⭐ Validar sem repetir
Tags: express, middleware, refatoracao, api

Hoje a validação do `POST /api/produtos` são vinte linhas de `if` dentro do handler. Na próxima aula chega o `PUT`, que precisa das mesmas regras. Na aula seguinte, o recurso de categorias. Copiar e colar esses `if` três vezes é a receita conhecida para o dia em que a regra mudar em dois lugares e ficar esquecida no terceiro. Escreva **um** middleware genérico que receba a descrição do que validar e devolva o middleware pronto — e prove que ele serve para recursos diferentes.

**Critérios de pronto**

- `middlewares/validar.js` exporta uma função `validar(regras)` que **retorna** um middleware.
- As regras de produto ficam declaradas em um objeto, fora do middleware: campo, tipo esperado, obrigatoriedade e uma condição extra opcional.
- O `POST /api/produtos` usa `validar(regrasProduto)` e o handler fica com no máximo dez linhas.
- Um `400` traz a lista de **todos** os problemas encontrados, não só o primeiro.
- Um segundo recurso (categorias, avaliações, o que você preferir) usa o mesmo `validar` com outro objeto de regras, sem alterar uma linha do middleware.

<details markdown="1">
<summary>Pistas</summary>

1. Uma função que devolve um middleware é o padrão de fábrica que o próprio Express usa: `express.json()` também é uma chamada que **retorna** a função `(req, res, next)`.
2. Assinatura sugerida: `validar({ nome: { tipo: "string", obrigatorio: true, minimo: 3 }, preco: { tipo: "number", obrigatorio: true, minimo: 0.01 } })`.
3. `Object.entries(regras)` percorre campo por campo; acumule as mensagens em um array e responda uma vez só, no fim.
4. Isto é o padrão **Strategy** aplicado: o algoritmo (o conjunto de regras) é injetado de fora, e o middleware não sabe nada sobre produtos. É também a ideia por trás de bibliotecas como zod e Joi — depois de fazer o seu, vale ler a documentação de uma delas para comparar.
</details>

### ⭐⭐⭐ Escreva o seu próprio `express.json()`
Tags: node, express, middleware, http

`app.use(express.json())` parece uma linha mágica: o corpo cru vira objeto e ninguém pergunta como. Não é mágica — é um `stream`. O corpo de uma requisição HTTP chega em pedaços, e alguém precisa juntá-los, decidir quando acabou, verificar o `Content-Type`, converter e ainda impedir que uma requisição de 2 GB acabe com a memória do servidor. Escreva esse alguém, e depois compare o seu resultado com o original.

**Critérios de pronto**

- `middlewares/meuJson.js` exporta uma função que, registrada no lugar de `express.json()`, faz o `POST` de produtos funcionar exatamente como antes.
- O middleware só age quando o cabeçalho `Content-Type` é `application/json`; nos outros casos chama `next()` sem tocar em `req.body`.
- Corpo com JSON inválido produz `400` com uma mensagem clara, sem derrubar o servidor.
- Corpo maior que um limite configurável (por exemplo, 100 kB) é recusado com `413 Payload Too Large`, e a conexão é encerrada **antes** de o restante ser lido.
- Um documento `docs/meu-json.md` compara o seu middleware com o `express.json()` em pelo menos quatro aspectos, e explica o que o `express.json()` faz que o seu não faz.
- Uma medição: `curl` enviando um corpo de 1 MB é recusado com `413`, e o log mostra quantos bytes chegaram a ser lidos antes da recusa.

<details markdown="1">
<summary>Pistas</summary>

1. `req` é um stream legível. O padrão é `req.on("data", (pedaco) => {...})` acumulando em um array, `req.on("end", () => {...})` para finalizar e `req.on("error", next)` para não engolir falhas de rede.
2. Acumule `Buffer` (não string) e junte no fim com `Buffer.concat(pedacos).toString("utf-8")` — concatenar strings pedaço a pedaço quebra caracteres acentuados que caíram na fronteira entre dois pedaços. Esse bug é sutil e vale muito descobri-lo na prática.
3. Some `pedaco.length` a cada evento `data`; ao passar do limite, responda `413` e chame `req.destroy()` para não continuar recebendo.
4. `req.headers["content-type"]` pode vir como `application/json; charset=utf-8` — compare com `.startsWith("application/json")`, não com igualdade.
5. Para gerar 1 MB de corpo: `node -e 'process.stdout.write(JSON.stringify({t:"x".repeat(1e6)}))' > grande.json` e depois `curl -X POST --data-binary @grande.json -H "Content-Type: application/json" http://localhost:3000/api/produtos`.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `TypeError: Cannot destructure property 'nome' of 'req.body' as it is undefined.` | Falta `app.use(express.json())`, ou ele foi registrado depois da rota | Registre o parser antes de qualquer rota que use `req.body` |
| A requisição fica `(pending)` para sempre na aba Network | Um middleware não chamou `next()` nem respondeu | Percorra a cadeia e garanta que todo caminho termina em `next()` ou em uma resposta |
| `TypeError: Missing parameter name at 1` ao subir o servidor | Curinga do Express 4 (`app.get("*")`) | Use o curinga nomeado do Express 5: `app.get("/{*splat}", ...)` |
| `SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON` no front | A API devolveu a página HTML de 404 do Express em vez de JSON | Registre o middleware `naoEncontradoApi` depois das rotas de `/api` |
| `Error: Cannot set headers after they are sent to the client` | Duas respostas na mesma requisição, ou `next()` chamado depois de responder | `return` antes de cada `res.status(...).json(...)` intermediário |
| O tratador de erros nunca roda | Foi declarado com três parâmetros, ou registrado antes das rotas | Quatro parâmetros `(err, req, res, next)` e registro como último `app.use` |
| `Cannot find module './routes/produtos'` | Caminho relativo errado, ou o arquivo está em outra pasta | Do `server.js`, use `./routes/produtos`; de dentro de `routes/`, `../data/produtos.json` |
| O 404 da API mostra `/produtos` em vez de `/api/produtos` | Uso de `req.url` dentro de um middleware montado em prefixo | Troque por `req.originalUrl` |
| `POST` devolve `400` mesmo com o corpo aparentemente correto | Falta o cabeçalho `Content-Type: application/json` na requisição | Acrescente o cabeçalho no `testes.http` ou no `fetch` |
| O produto criado some depois de reiniciar o servidor | O array vive em memória; nada foi gravado em disco | Comportamento esperado hoje; a persistência chega na próxima aula |

## 🏠 Para praticar depois da aula (1 h)

No **seu projeto autoral**, aplique a mesma refatoração:

1. Crie `routes/<seu-recurso>.js` com um `express.Router` contendo todas as rotas do recurso, e deixe o `server.js` só com a montagem das peças.
2. Crie `middlewares/registro.js` com o log de método, caminho, status e duração.
3. Crie `middlewares/erros.js` com o 404 de API em JSON e o tratador de erros de quatro parâmetros, registrados na ordem certa.
4. Acrescente `express.json()` e implemente `POST /api/<seu-recurso>` com validação no servidor, devolvendo `201` no sucesso e `400` com a lista de problemas no erro.
5. Acrescente o curinga `/{*splat}` devolvendo o `index.html`, para o front continuar funcionando em qualquer caminho.
6. Crie o `testes.http` na raiz, cobrindo no mínimo: listagem, item existente, item inexistente (`404`), rota de API inexistente (`404`), `POST` válido (`201`) e `POST` inválido (`400`).

**Critério de pronto:** todos os blocos do `testes.http` disparam com o status esperado, o terminal mostra uma linha de log por requisição e o `server.js` tem menos de trinta linhas.

**Guarde no seu repositório:** commit + push.

## ✅ Checkpoint do projeto

- [ ] `server.js` só configura e monta: nenhuma regra de negócio dentro dele.
- [ ] Rotas do recurso principal em `routes/`, montadas com uma linha e caminhos relativos ao prefixo.
- [ ] `express.json()` registrado antes de todas as rotas.
- [ ] Middleware de log imprimindo método, caminho, status e duração de cada requisição.
- [ ] 404 de API respondendo em JSON, registrado depois das rotas de `/api`.
- [ ] Tratador de erros com quatro parâmetros, registrado por último, com log detalhado no servidor e mensagem genérica ao cliente.
- [ ] Curinga `/{*splat}` devolvendo o `index.html` para os caminhos fora da API.
- [ ] `POST` do recurso principal validando no servidor e devolvendo `201` ou `400`.
- [ ] `testes.http` versionado, cobrindo os casos de sucesso e de erro.

## 📚 Para aprofundar

- [Express — Usando middlewares (pt-BR)](https://expressjs.com/pt-br/guide/using-middleware.html) — leia inteiro; os cinco tipos de middleware estão todos ali.
- [Express — Escrevendo middlewares (pt-BR)](https://expressjs.com/pt-br/guide/writing-middleware.html) — o exemplo do `requestTime` é praticamente o nosso middleware de log.
- [Express — Tratamento de erros (pt-BR)](https://expressjs.com/pt-br/guide/error-handling.html) — atenção à seção sobre o tratador padrão e ao que ele expõe em produção.
- [Express 5 — Referência da API: `Router`](https://expressjs.com/en/5x/api.html#router) — consulte quando precisar de `router.route()` e `router.param()`.
- [Express — Migrando para a versão 5](https://expressjs.com/en/guide/migrating-5.html) — a lista oficial do que mudou; use como gabarito ao copiar código antigo da internet.
- [MDN — Códigos de status de resposta HTTP](https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Status) — revise a família `4xx` antes de escrever validações.
- [REST Client — extensão do VS Code](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) — a documentação de variáveis e ambientes vale dez minutos.
- QUEIRÓS, Ricardo; PORTELA, Filipe. *Introdução ao Desenvolvimento Moderno para a Web*. FCA — organização e estruturação da camada de back-end.
- LOUDON, Kyle. *Desenvolvimento de Grandes Aplicações Web*. Novatec — modularidade e código que precisa crescer sem virar espaguete.
- ALVES, William P. *Projetos de Sistemas Web*. Érica — arquitetura de sistemas web em camadas.

Na próxima aula damos o último passo da arquitetura: a rota deixa de conter a lógica e passa a apenas **apontar** para um controlador. Com `controllers/produtosController.js` no lugar, o CRUD fica completo — `PUT` e `DELETE` se juntam ao `GET` e ao `POST` —, a busca por query string ganha corpo e, principalmente, o que você criar para de sumir: os dados passam a ser gravados de verdade em `data/produtos.json` com `fs/promises`.
