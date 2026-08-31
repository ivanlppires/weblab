# Aula 16 — CRUD completo com autenticação e entrega final

> **Nível 2 — Desenvolvimento Web** · Unidade 3: Web dinâmica server-side
> WebLab · curso aberto de desenvolvimento web
> **Tempo estimado:** 3 blocos de 50 min + 1 h de prática

Última aula desta trilha. As duas metades do sistema já existem: o CRUD com persistência e o login do Google. Hoje elas se encontram no detalhe que separa um projeto de aula de um sistema de verdade — **saber de quem é cada registro**. Ao fim destes 150 minutos, a sua aplicação vai recusar com `401` quem não está logado, recusar com `403` quem está logado mas mexe no que não é seu, e rodar do zero numa pasta limpa com dois comandos. É também o dia do Marco 3, o fechamento do semestre e a hora de olhar para o que vem depois.

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Diferenciar autenticação de autorização e escolher corretamente entre `401`, `403` e `404` em cada situação.
- Gravar a identidade do criador de um registro a partir do token verificado, e explicar por que jamais a partir do corpo da requisição.
- Implementar regras de autorização por dono nas rotas de escrita, concentradas num único ponto do código.
- Fazer a interface refletir as permissões do usuário sem confundir conforto visual com segurança.
- Executar um roteiro completo de auto-teste que simula uma revisão rigorosa do projeto, incluindo o teste com duas contas diferentes.
- Escrever um `README.md` que permita a outra pessoa rodar o seu projeto do zero, e provar isso num clone limpo.
- Reconhecer o que foi construído em todo o semestre como a arquitetura padrão de uma aplicação web e identificar os próximos passos de estudo.

## 📋 Pré-requisitos

- [ ] `cafe-cerrado-api` com CRUD completo, persistência em arquivo e a camada `data/repositorio.js` (Aula 15).
- [ ] Front consumindo a própria API por `public/js/api.js`, com formulário de criar/editar e exclusão funcionando (Aula 15).
- [ ] Login Google operante, `.env` com `GOOGLE_CLIENT_ID` fora do Git e o middleware `exigirLogin` nas rotas de escrita (Aula 14).
- [ ] `testes.http` versionado, com pelo menos um cenário de cada status (`200`, `201`, `204`, `400`, `401`, `404`).
- [ ] Uma segunda conta Google disponível (uma pessoal e outra de trabalho/estudo, por exemplo) ou peça a outra pessoa para logar com a conta dela por um minuto — hoje vamos precisar de duas identidades diferentes.

> Na aula passada a interface ganhou o CRUD inteiro: formulário único para criar e editar, exclusão com confirmação, feedback anunciado por `aria-live` e dados sobrevivendo ao reinício do servidor. Ficou uma brecha, e ela é grave: qualquer pessoa logada — com qualquer conta Google do planeta — pode editar e excluir os produtos cadastrados por qualquer outra. Hoje fechamos essa brecha, rodamos o roteiro de auto-teste da entrega e encerramos esta trilha.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | `401` × `403`; campo `dono` vindo do token; regras de autorização no servidor; migração dos registros antigos |
| 2 | 50 min | Interface reagindo ao dono; roteiro de auto-teste com duas contas; README e teste da pasta limpa |
| 3 | 50 min | Laboratório, tira-dúvidas do Marco 3 e encerramento desta trilha |

## 1. Autenticação e autorização: duas perguntas diferentes

### 1.1 Quem é você × o que você pode

A Aula 14 respondeu à primeira pergunta. Lá, o `authController` usou o `google-auth-library` **uma única vez**, no login, para conferir o ID token do Google e emitir uma sessão própria — um token assinado com HMAC pelo seu servidor, válido por 8 horas. O middleware `exigirLogin` confere a assinatura **dessa sessão** a cada requisição e preenche `req.usuario` com dados em que dá para confiar: nome, e-mail e foto, que vieram do Google no momento do login. Isso é **autenticação**.

Falta a segunda pergunta. Hoje, com um token válido de qualquer conta Google, dá para apagar o cardápio inteiro do Café Cerrado. O sistema sabe quem você é e não faz absolutamente nada com essa informação. Decidir **o que cada identidade pode fazer** é **autorização** — e é a parte que quase todo projeto de aula esquece.

```text
autenticação → "quem é você?"        → 401 quando não sei
autorização  → "você pode fazer isso?" → 403 quando sei quem é, mas não pode
```

### 1.2 Escolhendo o status certo

| Status | Significado | Situação típica no projeto |
|---|---|---|
| `401 Unauthorized` | Não autenticado (o nome do status é histórico e enganoso) | Nenhum token, token expirado ou assinatura inválida |
| `403 Forbidden` | Autenticado, mas sem permissão | Editar ou excluir um produto de outra pessoa |
| `404 Not Found` | O recurso não existe | `PUT /api/produtos/9999` |

O `401` costuma vir acompanhado de uma instrução: "faça login". O `403` é diferente — repetir o login não muda nada, porque o problema não é a identidade, é a permissão. Por isso a interface reage de formas distintas: no `401`, abre o botão de login; no `403`, explica que aquele item é de outra pessoa.

> **💡 Dica**
> Existe uma escola que responde `404` em vez de `403` para recursos que existem mas não são seus. O argumento é bom: um `403` confirma que o recurso existe, o que já é informação para quem está sondando o sistema (dá para descobrir quantos registros existem só variando o id). Para o Café Cerrado, cujo cardápio é público, o `403` é mais honesto e mais didático. Num sistema de prontuários médicos, o `404` seria a escolha certa. Saber justificar a decisão vale mais do que decorar a regra.

### 1.3 Onde a autorização mora

Regra de ouro: **autorização é regra de negócio, e regra de negócio mora no servidor**. Esconder um botão no HTML não protege nada — a página é do usuário, ele pode reescrevê-la no DevTools em cinco segundos, ou simplesmente ignorá-la e mandar a requisição pelo `curl`. A interface **orienta**; o servidor **garante**.

> **🔬 Investigue**
> Abra o site logado, clique com o botão direito num card e escolha "Inspecionar". No painel Elements, encontre um `<div class="acoes-card">` escondido (ou apague um `hidden` de qualquer elemento) e veja o botão aparecer. Agora clique nele. O que acontece? Depois desta aula, a resposta será `403` e nada mudará no banco de dados. Antes dela, a exclusão acontece. É essa a diferença entre uma interface bonita e um sistema seguro — e é literalmente o mesmo experimento que um invasor faria primeiro.

> **🧠 Você sabia?**
> A falha que estamos corrigindo hoje tem nome: **IDOR** (*Insecure Direct Object Reference*, referência direta a objeto insegura). É quando o sistema aceita um identificador vindo do cliente (`/api/produtos/7`) e age sobre ele sem checar se aquele cliente tem direito àquele objeto. Na lista OWASP Top 10 de 2021 — o ranking das falhas de segurança web mais críticas, mantido por uma fundação sem fins lucrativos —, a categoria que abriga o IDOR (*Broken Access Control*) subiu para o **primeiro lugar**, presente em 94% das aplicações testadas. Ou seja: a linha de código que você vai escrever hoje é, estatisticamente, a correção de segurança mais necessária da web.

## 2. Todo registro tem dono

### 2.1 O dono vem do token, nunca do corpo

O middleware `exigirLogin` já deixa `req.usuario` preenchido com os dados da sessão verificada — o e-mail veio do Google no login e viajou dentro de um token que só o seu servidor sabe assinar. Basta usá-lo no momento da criação:

```js
const novo = {
  id: repo.proximoId(produtos),
  nome: req.body.nome.trim(),
  categoria: req.body.categoria?.trim() || "geral",
  preco: req.body.preco,
  descricao: req.body.descricao?.trim() || "",
  dono: req.usuario.email, // vem do TOKEN verificado — jamais de req.body
  criadoEm: new Date().toISOString(),
};
```

> **⚠️ Atenção**
> A linha `dono: req.usuario.email` é a linha mais importante desta aula. Se ela fosse `dono: req.body.dono`, qualquer pessoa poderia mandar `{ "dono": "professor@exemplo.br" }` e criar registros em nome de outra — e depois nem editá-los conseguiria. Vale como princípio geral: **tudo que identifica o autor de uma ação vem do token verificado; tudo que o cliente manda no corpo é palpite até ser validado.**

`criadoEm` guarda o instante em ISO 8601 (`"2030-03-14T18:32:05.123Z"`), o formato que `new Date()` entende de volta sem ambiguidade e que ordena corretamente como texto. Nunca grave data como `"14/03 às 18h32"`: formatar é trabalho da interface, com `Intl.DateTimeFormat`.

### 2.2 Os registros que já existem

Os produtos cadastrados antes de hoje não têm o campo `dono`. Sem tratamento, eles ficariam impossíveis de editar: `undefined !== "voce@gmail.com"` é sempre verdade, então toda tentativa responderia `403`. Um script resolve isso de uma vez:

`cafe-cerrado-api/scripts/definir-dono.js`

```js
// Uso: node scripts/definir-dono.js seu-email@gmail.com
// Atribui um dono aos produtos criados antes da regra de autorização existir.
const repo = require("../data/repositorio");

async function principal() {
  const email = process.argv[2];
  if (!email) {
    console.error("Informe o e-mail: node scripts/definir-dono.js voce@gmail.com");
    process.exit(1);
  }

  const produtos = await repo.lerTodos();
  let ajustados = 0;

  for (const produto of produtos) {
    if (!produto.dono) {
      produto.dono = email;
      produto.criadoEm = produto.criadoEm ?? new Date().toISOString();
      ajustados += 1;
    }
  }

  await repo.salvarTodos(produtos);
  console.log(`${ajustados} produto(s) passaram a pertencer a ${email}.`);
}

principal().catch((erro) => {
  console.error("Falha na migração:", erro);
  process.exit(1);
});
```

```bash
node scripts/definir-dono.js seu-email@gmail.com
# esperado: 6 produto(s) passaram a pertencer a seu-email@gmail.com.
```

Guarde esse script no repositório. Ele é a versão artesanal do que, num projeto com banco de dados, se chama **migração**: um passo versionado que leva os dados de um formato ao seguinte. Você vai reencontrar o conceito no Nível 3, com nome e ferramenta próprios.

## 3. A regra de autorização, num lugar só

### 3.1 O controlador completo

Duas linhas de checagem entram em `atualizar` e `remover`. Como a regra é idêntica nas duas, ela vira uma função — assim, no dia em que administradores puderem editar tudo, você muda um lugar só.

`cafe-cerrado-api/controllers/produtosController.js`

```js
const repositorio = require("../data/repositorio");

// A lista branca de categorias do cardápio (Aula 13).
const CATEGORIAS = ["cafes", "geladas", "salgados", "doces"];

// Deixa o texto comparável: sem acento, sem maiúscula, sem espaço nas pontas.
function normalizar(texto) {
  return String(texto ?? "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim();
}

// Converte o :id da rota. Se não for inteiro positivo, já responde 400.
function idDaRota(req, res) {
  const id = Number(req.params.id);

  if (!Number.isInteger(id) || id <= 0) {
    res.status(400).json({ erro: "O id precisa ser um número inteiro positivo." });
    return null;
  }

  return id;
}

// Valida e normaliza o corpo (Aula 13). Com { parcial: true }, ignora ausentes.
function validarProduto(corpo = {}, { parcial = false } = {}) {
  const erros = [];
  const dados = {};

  if (corpo.nome !== undefined || !parcial) {
    const nome = typeof corpo.nome === "string" ? corpo.nome.trim() : "";
    if (nome.length < 3) {
      erros.push({ campo: "nome", mensagem: "O nome precisa ter ao menos 3 caracteres." });
    } else {
      dados.nome = nome;
    }
  }

  if (corpo.preco !== undefined || !parcial) {
    const preco = Number(corpo.preco);
    if (!Number.isFinite(preco) || preco <= 0) {
      erros.push({ campo: "preco", mensagem: "O preço precisa ser um número maior que zero." });
    } else {
      dados.preco = Math.round(preco * 100) / 100;
    }
  }

  if (corpo.categoria !== undefined || !parcial) {
    const categoria = typeof corpo.categoria === "string" ? normalizar(corpo.categoria) : "";
    if (!CATEGORIAS.includes(categoria)) {
      erros.push({
        campo: "categoria",
        mensagem: `A categoria precisa ser uma destas: ${CATEGORIAS.join(", ")}.`,
      });
    } else {
      dados.categoria = categoria;
    }
  }

  if (corpo.descricao !== undefined) {
    dados.descricao = String(corpo.descricao).trim();
  } else if (!parcial) {
    dados.descricao = "";
  }

  if (corpo.imagem !== undefined) {
    dados.imagem = String(corpo.imagem).trim();
  } else if (!parcial) {
    dados.imagem = "";
  }

  return { erros, dados };
}

// Única definição da regra de autorização do projeto.
function podeAlterar(produto, usuario) {
  return produto.dono === usuario.email;
}

// GET /api/produtos?q=cafe&categoria=cafes&ordenar=preco
exports.listar = async (req, res) => {
  const { q, categoria, ordenar } = req.query;
  let lista = await repositorio.lerTodos();

  if (typeof categoria === "string" && categoria !== "") {
    const alvo = normalizar(categoria);
    lista = lista.filter((produto) => normalizar(produto.categoria) === alvo);
  }

  if (typeof q === "string" && q !== "") {
    const termo = normalizar(q);
    lista = lista.filter(
      (produto) =>
        normalizar(produto.nome).includes(termo) ||
        normalizar(produto.descricao).includes(termo),
    );
  }

  if (ordenar === "preco") {
    lista = [...lista].sort((a, b) => a.preco - b.preco);
  } else if (ordenar === "-preco") {
    lista = [...lista].sort((a, b) => b.preco - a.preco);
  } else if (ordenar === "nome") {
    lista = [...lista].sort((a, b) => a.nome.localeCompare(b.nome, "pt-BR"));
  }

  res.json(lista);
};

exports.obter = async (req, res) => {
  const id = idDaRota(req, res);
  if (id === null) return;

  const lista = await repositorio.lerTodos();
  const produto = lista.find((item) => item.id === id);
  if (!produto) return res.status(404).json({ erro: `Produto ${id} não encontrado.` });

  res.json(produto);
};

exports.criar = async (req, res) => {
  const { erros, dados } = validarProduto(req.body);
  if (erros.length > 0) {
    return res.status(400).json({ erro: "Dados inválidos.", detalhes: erros });
  }

  const lista = await repositorio.lerTodos();
  const novo = {
    id: repositorio.proximoId(lista),
    ...dados,
    dono: req.usuario.email, // do token verificado, NUNCA do corpo
    criadoEm: new Date().toISOString(),
  };

  lista.push(novo);
  await repositorio.salvarTodos(lista);

  res.status(201).location(`/api/produtos/${novo.id}`).json(novo);
};

exports.atualizar = async (req, res) => {
  const id = idDaRota(req, res);
  if (id === null) return;

  const lista = await repositorio.lerTodos();
  const indice = lista.findIndex((item) => item.id === id);
  if (indice === -1) return res.status(404).json({ erro: `Produto ${id} não encontrado.` });

  if (!podeAlterar(lista[indice], req.usuario)) {
    return res.status(403).json({ erro: "Este produto foi cadastrado por outra pessoa." });
  }

  const { erros, dados } = validarProduto(req.body, { parcial: true });
  if (erros.length > 0) {
    return res.status(400).json({ erro: "Dados inválidos.", detalhes: erros });
  }
  if (Object.keys(dados).length === 0) {
    return res.status(400).json({ erro: "Envie ao menos um campo para atualizar." });
  }

  // O id, o dono e a data de criação são preservados de propósito: nenhum
  // deles pode ser trocado por um campo vindo do corpo da requisição.
  const atualizado = {
    ...lista[indice],
    ...dados,
    id,
    dono: lista[indice].dono,
    criadoEm: lista[indice].criadoEm,
    atualizadoEm: new Date().toISOString(),
  };

  lista[indice] = atualizado;
  await repositorio.salvarTodos(lista);

  res.json(atualizado);
};

exports.remover = async (req, res) => {
  const id = idDaRota(req, res);
  if (id === null) return;

  const lista = await repositorio.lerTodos();
  const indice = lista.findIndex((item) => item.id === id);
  if (indice === -1) return res.status(404).json({ erro: `Produto ${id} não encontrado.` });

  if (!podeAlterar(lista[indice], req.usuario)) {
    return res.status(403).json({ erro: "Este produto foi cadastrado por outra pessoa." });
  }

  lista.splice(indice, 1);
  await repositorio.salvarTodos(lista);

  res.status(204).end();
};
```

Este é o controlador da Aula 13 — filtros, ordenação, lista branca de categorias, `400` para id malformado e `detalhes: [{ campo, mensagem }]` intactos — com **três** acréscimos de hoje: a função `podeAlterar`, os campos `dono` e `criadoEm` no `criar`, e a checagem de `403` no `atualizar` e no `remover`. Nada foi removido; autorização se **soma** ao que existe.

Repare também no objeto montado dentro de `atualizar`: `dono` e `criadoEm` são reafirmados a partir do registro que já estava no disco. Sem isso, bastaria mandar `{"dono": "eu@gmail.com"}` no corpo de um `PUT` para tomar posse de um produto alheio — a mesma armadilha do `id` que a Aula 13 fechou, agora com consequência de segurança.


### 3.2 A versão em middleware (e a armadilha da referência)

Dá para tirar a checagem dos controladores e transformá-la num middleware, no espírito da Aula 12. Fica mais elegante e coloca a regra literalmente na rota:

`cafe-cerrado-api/middlewares/exigirDono.js`

```js
const repo = require("../data/repositorio");

// Roda DEPOIS de exigirLogin: conta com req.usuario já preenchido.
// Deixa a lista inteira e o produto encontrado disponíveis para o controlador,
// para não ler o arquivo duas vezes na mesma requisição.
module.exports = async function exigirDono(req, res, next) {
  const produtos = await repo.lerTodos();
  const produto = produtos.find((p) => p.id === Number(req.params.id));

  if (!produto) return res.status(404).json({ erro: "Produto não encontrado" });
  if (produto.dono !== req.usuario.email) {
    return res.status(403).json({ erro: "Este produto foi cadastrado por outra pessoa" });
  }

  req.produtos = produtos; // a lista que será salva
  req.produto = produto; // referência para um item DENTRO dessa lista
  next();
};
```

`cafe-cerrado-api/routes/produtos.js`

```js
const express = require("express");
const controlador = require("../controllers/produtosController");
const exigirLogin = require("../middlewares/exigirLogin");
const exigirDono = require("../middlewares/exigirDono");

const router = express.Router();

router.get("/", controlador.listar);
router.get("/:id", controlador.obter);
router.post("/", exigirLogin, controlador.criar);
router.put("/:id", exigirLogin, exigirDono, controlador.atualizar);
router.delete("/:id", exigirLogin, exigirDono, controlador.remover);

module.exports = router;
```

> **🔎 Por baixo do capô**
> Por que o middleware precisa passar `req.produtos` **e** `req.produto`? Porque `repo.lerTodos()` faz `JSON.parse` a cada chamada, e `JSON.parse` cria objetos novos. Se o controlador chamasse `lerTodos()` de novo, ele receberia uma lista **diferente**, com objetos diferentes: alterar `req.produto` não teria efeito nenhum sobre a lista que seria salva, e o `PUT` responderia `200` sem mudar nada no disco. Passando as duas coisas, o `req.produto` é uma referência a um item de dentro de `req.produtos` — mudar um muda o outro, porque são o mesmo objeto na memória. Esse é um dos efeitos de referência mais traiçoeiros do JavaScript, e ele custa horas de depuração a quem nunca tropeçou nele.

Se você adotar o middleware, os controladores `atualizar` e `remover` passam a usar `req.produtos` e `req.produto` em vez de reler o arquivo. **Escolha um dos dois caminhos** — a checagem no controlador (seção 3.1) ou o middleware (seção 3.2) — e mantenha a coerência. Ter a regra nos dois lugares é pior do que tê-la em um só: um dia você corrige um e esquece o outro.

### 3.3 Provando pelo `testes.http`

Antes de tocar na interface, prove a regra com requisições cruas. Você vai precisar de dois **tokens de sessão**: um seu e um de uma segunda conta (uma alternativa sua, ou a de outra pessoa que te empreste o login por um minuto). Cada um se obtém do mesmo jeito da Aula 14: faça login com a conta, abra o console do navegador e rode `JSON.parse(sessionStorage.getItem("cafe-cerrado-sessao")).token`. Não use o ID token do Google — o `exigirLogin` confere a assinatura HMAC da sua própria API e recusaria qualquer outra coisa com `401`.

`cafe-cerrado-api/testes.http`

```http
@tokenA = cole-aqui-o-token-de-sessao-da-conta-A
@tokenB = cole-aqui-o-token-de-sessao-da-conta-B

### A conta A cria um produto — 201, id 11, com "dono" igual ao e-mail da conta A
POST http://localhost:3000/api/produtos
Content-Type: application/json
Authorization: Bearer {{tokenA}}

{ "nome": "Espresso Duplo", "categoria": "cafes", "preco": 8.5, "descricao": "Duas doses curtas na mesma xícara." }

### A conta A edita o próprio produto — 200
PUT http://localhost:3000/api/produtos/11
Content-Type: application/json
Authorization: Bearer {{tokenA}}

{ "nome": "Espresso Duplo", "categoria": "cafes", "preco": 9, "descricao": "Duas doses curtas na mesma xícara." }

### A conta B tenta editar o produto da conta A — 403
PUT http://localhost:3000/api/produtos/11
Content-Type: application/json
Authorization: Bearer {{tokenB}}

{ "nome": "Sequestrado", "categoria": "cafes", "preco": 1, "descricao": "Não deve funcionar" }

### A conta B tenta excluir o produto da conta A — 403
DELETE http://localhost:3000/api/produtos/11
Authorization: Bearer {{tokenB}}

### Ninguém tenta excluir sem token — 401
DELETE http://localhost:3000/api/produtos/11

### Excluir um produto que não existe — 404
DELETE http://localhost:3000/api/produtos/99999
Authorization: Bearer {{tokenA}}

### A conta A exclui o próprio produto — 204
DELETE http://localhost:3000/api/produtos/11
Authorization: Bearer {{tokenA}}
```

As variáveis `@tokenA` e `@tokenB` são um recurso da extensão REST Client: declaradas no topo do arquivo, são usadas com `{{tokenA}}` em qualquer requisição. Trocar de token vira uma edição só.

> **⚠️ Atenção**
> Esses tokens são credenciais reais, válidas por cerca de uma hora, que identificam pessoas de verdade. Nunca comite um `testes.http` com tokens preenchidos: deixe os marcadores `COLE_AQUI...` no arquivo versionado e preencha localmente na hora de testar. É o mesmo cuidado do `.env` — segredo no histórico do Git é segredo vazado para sempre.

## 4. A interface reage ao dono

Com o servidor garantindo a regra, a interface pode (e deve) refletir a mesma lógica — não por segurança, mas por educação: mostrar um botão que sempre falha é maltratar quem usa o sistema.

Duas mudanças no `criarCard` do `public/js/app.js`: exibir quem cadastrou e mostrar os botões só para o dono.

`cafe-cerrado-api/public/js/app.js — a função criarCard atualizada`

```js
function criarCard(produto) {
  const card = document.createElement("article");
  card.className = "card-produto";
  card.dataset.id = produto.id;

  const titulo = document.createElement("h3");
  titulo.textContent = produto.nome;

  const preco = document.createElement("p");
  preco.className = "preco";
  preco.textContent = moeda.format(produto.preco);

  const categoria = document.createElement("p");
  categoria.className = "categoria";
  categoria.textContent = produto.categoria;

  const descricao = document.createElement("p");
  descricao.className = "descricao";
  descricao.textContent = produto.descricao || "Sem descrição.";

  const autor = document.createElement("p");
  autor.className = "autor";
  autor.textContent = produto.dono ? `cadastrado por ${produto.dono}` : "cadastro antigo, sem dono";

  card.append(titulo, preco, categoria, descricao, autor);

  // Conforto de interface: só o dono vê os botões. A garantia é o 403 do servidor.
  const usuario = obterUsuario();
  const souDono = Boolean(usuario) && produto.dono === usuario.email;

  if (souDono) {
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
```

E o tratamento de erro ganha uma mensagem específica para o `403`, aproveitando o `status` que a `ErroDeApi` da Aula 15 já carrega:

`cafe-cerrado-api/public/js/app.js — a função de mensagem de erro`

```js
function mensagemDeErro(erro) {
  if (erro.status === 401) return "Sua sessão expirou. Entre com o Google de novo.";
  if (erro.status === 403) return "Este item foi cadastrado por outra pessoa — você não pode alterá-lo.";
  if (erro.status === 404) return "Este item não existe mais. A lista será atualizada.";
  const extra = erro.detalhes?.length ? ` (${erro.detalhes.join("; ")})` : "";
  return `${erro.message}${extra}`;
}
```

Use-a nos dois `catch` que mostram erro ao usuário (o do `submit` e o do `excluirProduto`), trocando `avisar(erro.message, "erro")` por `avisar(mensagemDeErro(erro), "erro")`. No caso do `404`, vale ainda chamar `carregarProdutos()` em seguida: se o item sumiu, a tela está desatualizada.

`cafe-cerrado-api/public/css/estilo.css — acréscimo`

```css
.card-produto .autor {
  margin-top: 0.5rem;
  font-size: 0.8rem;
  color: #57534e;
}
```

## 5. Roteiro de auto-teste: simule a correção

Antes de considerar o projeto pronto, faça o que uma revisão rigorosa faria. Com o servidor rodando e o navegador em uma janela anônima (para não reaproveitar a sua sessão), percorra os dez passos abaixo. Anote o que falhar; corrija; repita do começo.

1. **Visitante.** Abra o site sem login: a lista carrega, nenhum botão de escrita aparece, a área de gestão está oculta.
2. **Escrita bloqueada.** Pelo `testes.http`, faça um `POST /api/produtos` sem cabeçalho `Authorization`. Esperado: `401` com JSON explicando.
3. **Login.** Clique no botão do Google: nome e foto aparecem, o formulário de cadastro fica visível, os cards seus ganham botões.
4. **Create.** Cadastre um item: feedback de sucesso, item na lista sem recarregar, `201` na aba Network, campo `dono` com o seu e-mail no `data/produtos.json`.
5. **Read.** Busque por um termo com e sem acento (`cafe` e `café`): a busca encontra nos dois casos. Peça `GET /api/produtos/99999`: `404`.
6. **Update.** Edite o item criado: a mudança aparece na tela sem recarregar, `200` na Network, `atualizadoEm` preenchido no arquivo.
7. **Delete.** Exclua com confirmação: o card some, `204` na Network. Repita o mesmo `DELETE` no `testes.http`: `404`.
8. **Autorização.** Com o token da segunda conta, tente editar e excluir um item da primeira: `403` nos dois casos, e o arquivo no disco intacto.
9. **Persistência.** Derrube o servidor (<kbd>Ctrl</kbd>+<kbd>C</kbd>), suba de novo e recarregue a página: tudo continua lá.
10. **Higiene.** `git status` limpo, `node_modules/` e `.env` fora do Git, e o teste da pasta limpa da seção 6 passando.

> **📌 Vale gravar**
> Este roteiro é um bom resumo de como o back-end da Unidade 3 funciona: qual status cada situação produz, quem valida o quê, em que ordem os middlewares rodam e por que a proteção do cliente não substitui a do servidor. Se você consegue explicar cada um dos dez passos para outra pessoa, você domina a parte de back-end desta unidade.

## 6. Higiene do repositório e o teste da pasta limpa

### 6.1 O que nunca sobe

`cafe-cerrado-api/.gitignore`

```text
node_modules/
.env
*.log
.DS_Store
data/produtos.json.tmp
```

Se você descobriu tarde demais que `node_modules/` ou `.env` já estão no histórico, o comando abaixo remove os arquivos do controle de versão sem apagá-los do seu disco:

```bash
git rm -r --cached node_modules .env
git commit -m "remove arquivos que não deveriam estar versionados"
```

Isso resolve para o futuro. Se um segredo real chegou a subir para o GitHub, considere-o vazado: gere um Client ID novo no Google Cloud Console e apague o antigo. Reescrever o histórico é possível, mas cópias já podem ter sido feitas.

Para que outra pessoa saiba **quais** variáveis existem, versione um exemplo sem valores:

`cafe-cerrado-api/.env.exemplo`

```text
GOOGLE_CLIENT_ID=cole-aqui-o-client-id-do-google-cloud-console
SESSAO_SEGREDO=gere-com-node-e-crypto-randomBytes-32-hex
PORT=3000
```

As três variáveis são obrigatórias, e o `SESSAO_SEGREDO` é a mais fácil de esquecer: sem ele o `server.js` da Aula 14 encerra com `process.exit(1)` e a mensagem "Variável SESSAO_SEGREDO ausente" — o que reprova na hora o teste da pasta limpa da próxima seção. Gere um valor com:

```bash
node -e "console.log(require('node:crypto').randomBytes(32).toString('hex'))"
```

### 6.2 O teste da pasta limpa

O erro mais comum na entrega não é código errado — é código que só roda na máquina de quem escreveu. Prove que não é o seu caso clonando o próprio repositório em outra pasta:

```bash
cd /tmp
git clone https://github.com/seu-usuario/cafe-cerrado-api.git teste-entrega
cd teste-entrega
cp /caminho/do/seu/projeto/.env .env   # o .env não vem do Git, e está certo assim
npm install
npm run dev
# abra http://localhost:3000 e repita os passos 1 a 7 do roteiro de auto-teste
```

Três coisas costumam falhar aqui, e todas fazem o projeto parecer quebrado para quem só tem o repositório, sem acesso à sua máquina:

- **`Cannot find module 'express'`** — alguma dependência foi instalada sem entrar no `package.json`. Rode `npm install express google-auth-library dotenv` na pasta original e comite o `package.json` e o `package-lock.json`.
- **`data/produtos.json` não existe** — o arquivo de dados está no `.gitignore` ou nunca foi comitado. Versione uma versão pequena com dois ou três itens de exemplo: quem for testar precisa ver a tela cheia, não vazia.
- **A aplicação sobe, mas o login não funciona** — o `README.md` não explica que é preciso criar um Client ID próprio e adicionar `http://localhost:3000` às origens autorizadas. Explique.

### 6.3 O README que faz o projeto existir para os outros

Um repositório sem README é um projeto que só funciona para quem o escreveu. Este é o esqueleto mínimo — copie a estrutura e escreva o conteúdo do **seu** projeto:

`cafe-cerrado-api/README.md`

```markdown
# Café Cerrado — API e site

Aplicação full-stack da cafeteria fictícia Café Cerrado, desenvolvida na
no Nível 2 do WebLab (Desenvolvimento Web).
Site estático servido pelo Express, API REST com CRUD de produtos,
login com Google e persistência em arquivo JSON.

## Tecnologias

- Node.js 22 LTS e Express 5
- Google Identity Services (login) e google-auth-library (verificação do token)
- HTML5, CSS3 e Bootstrap 5.3 no front; JavaScript com módulos ES e fetch
- Persistência em arquivo JSON com fs/promises

## Como rodar

Pré-requisitos: Node.js 22 ou superior e uma conta Google.

1. Clone o repositório e instale as dependências:

        git clone https://github.com/seu-usuario/cafe-cerrado-api.git
        cd cafe-cerrado-api
        npm install

2. Crie um projeto no Google Cloud Console, gere um ID do cliente OAuth do
   tipo "Aplicativo da Web" e adicione `http://localhost:3000` às origens
   JavaScript autorizadas.

3. Copie `.env.exemplo` para `.env` e preencha o `GOOGLE_CLIENT_ID` e o
   `SESSAO_SEGREDO` (o Client ID chega ao navegador por `GET /api/config`;
   não há nada para colar no HTML):

        cp .env.exemplo .env
        node -e "console.log(require('node:crypto').randomBytes(32).toString('hex'))"

4. Suba o servidor:

        npm run dev

5. Acesse <http://localhost:3000>.

## Endpoints da API

| Método | Caminho | Descrição |
|---|---|---|
| GET | /api/produtos | Lista produtos; aceita `?q=`, `?categoria=` e `?ordenar=` |
| GET | /api/produtos/:id | Um produto |
| POST | /api/produtos | Cria (exige login) |
| PUT | /api/produtos/:id | Atualiza (exige login e ser o dono) |
| DELETE | /api/produtos/:id | Remove (exige login e ser o dono) |
| GET | /api/categorias | Lista as categorias do cardápio, como `{ id, nome }` |
| GET | /api/config | Configuração pública do front (Client ID do Google) |
| POST | /api/auth/google | Recebe `{ credential }`, verifica o ID token e devolve `{ usuario, token }` |
| GET | /api/auth/eu | Dados do usuário da sessão atual (exige login) |

Status possíveis: 200, 201, 204, 400, 401, 403, 404 e 500.

## Estrutura de pastas

- `server.js` — configuração do Express e dos middlewares
- `routes/` — definição das rotas
- `controllers/` — regras de cada operação
- `middlewares/` — log, autenticação, autorização, 404 e erros
- `data/` — repositório de persistência e o arquivo de dados
- `public/` — site (HTML, CSS, JavaScript, imagens)
- `scripts/` — utilitários de manutenção
- `testes.http` — requisições de teste (extensão REST Client)

## Decisões técnicas

- Bootstrap 5.3 como framework CSS, pela documentação em português e pelo
  sistema de grid pronto (justificativa completa na Unidade 1).
- Persistência em arquivo JSON, isolada em `data/repositorio.js`, para que a
  troca por um banco de dados afete um arquivo só.
- Login delegado ao Google: o projeto não guarda senhas.

## Autor

Seu Nome — Nível 2 do WebLab.
```

Os blocos de comando dentro do README acima estão recuados em oito espaços: dentro de um bloco de código Markdown, essa é a forma de mostrar código sem abrir outra cerca. No seu README de verdade, use cercas normais com três crases.

## 7. O que você construiu nesta trilha

Em dezesseis encontros, o mesmo projeto atravessou a pilha inteira de uma aplicação web profissional:

| Unidade | O que entrou | Onde vive no projeto |
|---|---|---|
| 1 — Web estática | HTML semântico, Bootstrap, SVG, animação, ARIA | `public/index.html`, `public/css/` |
| 2 — Client-side | DOM, eventos, vetores, Promises, `fetch`, SPA | `public/js/app.js` |
| 3 — Server-side | Express, middlewares, rotas, controladores, OAuth, CRUD | `server.js`, `routes/`, `controllers/`, `data/` |

Nada disso é específico do Café Cerrado. Troque "produto" por "consulta", "vaga", "chamado" ou "pedido" e você tem, respectivamente, um sistema de clínica, um portal de estágios, um help desk e um delivery. **A arquitetura é a mesma.** Foi por isso que passamos o semestre insistindo em separar camadas: é ela que você leva daqui, não o cardápio.

## 💻 Mão na massa — fechando o Café Cerrado

**Passo 1 — acrescente o dono ao `criar`.** Abra `controllers/produtosController.js` e aplique as mudanças da seção 3.1: a função `podeAlterar`, os campos `dono` e `criadoEm` no `criar`, e o `atualizadoEm` no `atualizar`.

**Passo 2 — proteja `atualizar` e `remover`** com a checagem de `403`, na ordem correta (existe → é seu → é válido).

**Passo 3 — migre os produtos antigos:**

```bash
mkdir -p scripts
# crie scripts/definir-dono.js com o conteúdo da seção 2.2
node scripts/definir-dono.js seu-email@gmail.com
cat data/produtos.json | head -20
# confirme que os produtos agora têm "dono" e "criadoEm"
```

**Passo 4 — prove a regra pelo `testes.http`** com dois tokens, como na seção 3.3. Não avance enquanto os `403` não aparecerem: se a interface ficar pronta antes da regra, você vai depurar dois problemas ao mesmo tempo.

**Passo 5 — atualize o `criarCard`** com a versão da seção 4, e acrescente a função `mensagemDeErro` ao `app.js`, usando-a nos dois `catch`.

**Passo 6 — acrescente o estilo do autor** ao `public/css/estilo.css`.

**Passo 7 — rode o roteiro de auto-teste completo** da seção 5, os dez passos, em janela anônima.

**Passo 8 — arrume a casa:**

```bash
# confira o que está versionado
git ls-files | grep -E "node_modules|\.env$" && echo "PROBLEMA: remova estes arquivos"
# crie o .env.exemplo e o .gitignore da seção 6.1, se ainda não existirem
git add .
git commit -m "autorização por dono, README e roteiro de entrega"
git push
```

**Passo 9 — faça o teste da pasta limpa** da seção 6.2, do `git clone` até o login funcionando.

**Como testar — o resultado esperado:**

1. Um produto criado por você mostra "cadastrado por seu-email@gmail.com" e tem os botões Editar/Excluir.
2. Um produto criado por outra conta aparece na lista, mostra o e-mail do dono e **não** tem botões.
3. Forçar a exclusão de um produto alheio pelo `testes.http` responde `403` e o arquivo não muda.
4. Sem token, qualquer escrita responde `401`.
5. `npm install && npm run dev` funciona numa pasta recém-clonada, seguindo só o que está escrito no README.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Explique, em duas frases, a diferença entre `401` e `403`. Dê um exemplo de cada, tirado do seu projeto autoral.

**A2.** Por que `dono: req.usuario.email` é seguro e `dono: req.body.dono` não é? Descreva o ataque exato que a segunda forma permite.

**A3.** Na função `atualizar`, qual é a ordem correta das verificações (`400`, `403`, `404`)? O que aconteceria de estranho se a validação de dados viesse antes da busca do produto?

**A4.** O que é IDOR? Escreva uma requisição `curl` ou um bloco do `testes.http` que explore essa falha numa API que não checa o dono.

**A5.** Um produto cadastrado antes da regra de hoje não tem o campo `dono`. O que acontece ao tentar editá-lo? Qual comparação, exatamente, produz esse resultado?

**A6.** Por que esconder o botão "Excluir" no HTML não é uma medida de segurança? Cite duas formas de burlar essa "proteção" sem sair do navegador.

**A7.** O que faz `git rm -r --cached node_modules`? Qual é a diferença em relação a `rm -rf node_modules`?

**A8.** Por que `.env.exemplo` é versionado e `.env` não? O que deve haver dentro de cada um?

**A9.** Cite três motivos pelos quais um projeto que roda na sua máquina pode falhar num `git clone` limpo, e como o README evita cada um deles.

**A10.** Explique por que o middleware `exigirDono` precisa entregar ao controlador tanto `req.produtos` quanto `req.produto`, em vez de só o segundo.

### Nível B — Aplicação

**B1.** Mostre quando cada produto foi cadastrado, em linguagem natural ("há 3 dias", "há 2 horas"), a partir do campo `criadoEm`, usando `Intl.RelativeTimeFormat` com o locale `pt-BR`. Inclua o valor exato em um `title` no elemento, formatado com `Intl.DateTimeFormat`.

**Resultado esperado:** cada card exibe "cadastrado por fulano · há 2 horas"; passar o mouse mostra a data e a hora completas; produtos migrados pelo script mostram o instante da migração.

<details markdown="1">
<summary>Dica</summary>

Calcule a diferença em milissegundos (`Date.now() - new Date(produto.criadoEm)`), escolha a maior unidade que couber (dia, hora, minuto) e chame `new Intl.RelativeTimeFormat("pt-BR", { numeric: "auto" }).format(-valor, unidade)` — o valor negativo é o que produz "há". Uma função `formatarRelativo(iso)` isolada facilita testar no console.
</details>

**B2.** Acrescente um filtro "somente os meus" à listagem: uma caixa de seleção que, marcada, mostra apenas os produtos do usuário logado. Implemente o filtro **no servidor**, com `?meus=1` e o e-mail vindo do token — não no cliente.

**Resultado esperado:** marcada a caixa, a requisição vai para `/api/produtos?meus=1` com o cabeçalho `Authorization`, e a resposta traz só os seus itens. Sem login, a caixa fica desabilitada.

<details markdown="1">
<summary>Dica</summary>

A rota `GET /api/produtos` é pública, então ela não pode exigir login — mas pode **aceitar** um token quando ele vier. Crie um middleware `identificarOpcional` que tenta verificar o token e, se falhar, apenas segue sem `req.usuario`. No controlador, `if (req.query.meus === "1" && req.usuario)` filtra por `dono`.
</details>

**B3.** Escreva o `README.md` completo do seu projeto autoral, seguindo a estrutura da seção 6.3, e valide-o com o teste da pasta limpa. Peça a outra pessoa — colega de estudos, amigo, alguém de uma comunidade online — para seguir só o README, sem falar com você, e anote onde ela travou. Sem ninguém disponível? Feche o projeto, espere um dia, e siga seu próprio README do zero como se fosse a primeira vez.

**Resultado esperado:** outra pessoa (ou você mesmo, em outro dia, seguindo só o texto) consegue clonar, instalar, configurar o Client ID e ver a aplicação funcionando sem fazer nenhuma pergunta. Cada pergunta que precisou ser feita vira uma linha nova no README.

<details markdown="1">
<summary>Dica</summary>

O ponto onde as pessoas mais travam é o Client ID do Google: escreva o passo a passo do Cloud Console com os nomes exatos dos menus, incluindo a origem `http://localhost:3000`. Se o seu projeto precisa de dados de exemplo para não abrir vazio, versione um `data/` com dois ou três registros.
</details>

**B4.** A sessão já sobrevive ao <kbd>F5</kbd> (o `auth.js` da Aula 15 lê o `sessionStorage`), mas hoje a interface acredita cegamente no que está guardado: um token expirado ou adulterado à mão pelo DevTools continua desenhando os botões de escrita, que só falham quando alguém clica. Conserte isso: ao carregar a página, confirme a sessão no servidor com `GET /api/auth/eu` antes de considerar o usuário logado. Se a resposta for `401`, limpe o `sessionStorage` e volte ao estado de visitante.

**Resultado esperado:** logar, recarregar a página e continuar logado, com os botões de escrita visíveis; abrir uma aba anônima e continuar deslogado; esperar o token expirar e ver a aplicação voltar sozinha ao estado de visitante.

<details markdown="1">
<summary>Dica</summary>

`GET /api/auth/eu` já existe desde a Aula 14 e passa pelo `exigirLogin`: ele responde `200` com o usuário quando o token é válido e `401` quando não é — exatamente a pergunta que você precisa fazer. Chame-o dentro da função `async iniciar()` do `auth.js`, antes de `pintarAreaDoUsuario()`, e trate o `401` como logout. Para testar, edite o token no DevTools (Application → Session Storage), troque um caractere e recarregue: a página tem de voltar ao estado de visitante sozinha.
</details>

### Nível C — Desafio

**C1.** Em dupla, cada um usando a própria conta Google: cadastrem produtos, tentem editar e excluir os itens um do outro pela interface e pelo `testes.http`, e produzam um pequeno relatório `docs/teste-autorizacao.md` com as requisições feitas, os status obtidos e os status esperados. Encontrem pelo menos uma diferença entre o que a interface permite e o que o servidor permite.

<details markdown="1">
<summary>Dica</summary>

A diferença mais provável é a rota `GET /api/produtos/:id`: ela é pública, então qualquer pessoa lê qualquer produto — inclusive os campos `dono` e `criadoEm`. Isso é um problema? Depende do domínio: num cardápio, não; numa lista de candidaturas a vagas, sim. Registrem a conclusão no relatório.
</details>

**C2.** Implemente detecção de edição concorrente: se duas pessoas (ou duas abas) abrirem o mesmo produto para editar e a segunda salvar depois da primeira, a segunda deve receber `409 Conflict` em vez de sobrescrever silenciosamente as mudanças da primeira.

<details markdown="1">
<summary>Dica</summary>

O cliente envia, junto com os dados, o `atualizadoEm` que ele recebeu ao carregar o produto. O servidor compara com o `atualizadoEm` atual: se forem diferentes, alguém editou nesse meio-tempo e a resposta é `409` com uma mensagem clara. É a versão simples do que o HTTP chama de requisição condicional (cabeçalhos `ETag` e `If-Match`) — vale procurar na MDN depois de fazer funcionar.
</details>

## 🏆 Desafios

### ⭐ A prova dos três status
Tags: seguranca, autenticacao, http, investigacao

Dizer "minha API está protegida" é fácil; provar é outra coisa. Monte a evidência: um único arquivo com as requisições que demonstram, sem margem de dúvida, que a sua API distingue os três casos — visitante (`401`), pessoa logada mexendo no que não é dela (`403`) e pessoa logada mexendo no que é dela (`200`/`204`). Ao terminar, você vai ter o anexo mais convincente da sua entrega.

**Critérios de pronto**

- Um arquivo `docs/evidencias.md` com, para cada um dos três casos: o método e a URL, os cabeçalhos relevantes (com o token abreviado), o status recebido e o corpo da resposta.
- As requisições foram feitas com **duas contas Google diferentes**, e o relatório deixa claro qual conta fez o quê.
- Uma seção final aponta, em duas linhas, qual arquivo e qual linha do servidor produzem cada status.
- Nenhum token completo aparece no arquivo (mostre só os 12 primeiros caracteres seguidos de reticências).

<details markdown="1">
<summary>Pistas</summary>

1. A aba Network do DevTools tem "Copiar como cURL" no menu de contexto de cada requisição — é a forma mais rápida de registrar cabeçalhos reais.
2. Para conseguir o segundo token sem uma segunda conta, use uma janela anônima e uma conta institucional da sua universidade ou escola (se ela for uma conta Google) ou qualquer outra conta Google que você tenha.
3. Os status ficam visíveis também no log de requisições que o seu middleware da Aula 12 imprime no terminal — vale colar esse trecho no relatório.
4. Se algum caso não produzir o status esperado, você acabou de encontrar um bug antes do avaliador. Essa é a graça do desafio.
</details>

### ⭐⭐ O crachá de administrador
Tags: autenticacao, express, middleware, seguranca

O Café Cerrado cresceu e agora tem um gerente, que precisa corrigir o preço de qualquer produto — inclusive os cadastrados por outras pessoas. Sem inventar um sistema de cadastro de usuários: uma lista de e-mails administradores no `.env` resolve. O desafio é fazer isso sem espalhar `if` de permissão pelo código todo.

**Critérios de pronto**

- Uma variável `ADMINS` no `.env` (e no `.env.exemplo`), com e-mails separados por vírgula, alimenta a regra.
- `podeAlterar` (ou o middleware equivalente) passa a aceitar dono **ou** administrador, e continua sendo o único lugar do projeto que decide isso.
- Um administrador vê os botões de editar/excluir em todos os cards; um usuário comum, só nos seus.
- A resposta da API inclui, de forma explícita, se o usuário atual é administrador — a interface não adivinha lendo o `.env` (ela não tem acesso a ele).
- O `testes.http` prova os quatro cenários: dono, administrador, terceiro logado e visitante.

<details markdown="1">
<summary>Pistas</summary>

1. `process.env.ADMINS?.split(",").map((e) => e.trim().toLowerCase()) ?? []` no carregamento do módulo evita refazer a conversão a cada requisição.
2. Compare sempre em minúsculas: e-mails não diferenciam maiúsculas na prática, e um `Fulano@gmail.com` no `.env` não pode quebrar a regra.
3. Para a interface saber, o endpoint `POST /api/auth/google` da Aula 14 pode devolver um campo `admin: true/false` junto com nome, e-mail e foto.
4. Cuidado com a tentação de mandar a lista de administradores para o cliente. O front precisa saber se **este** usuário é admin, não quem são todos eles.
</details>

### ⭐⭐⭐ Quem mexeu no cardápio?
Tags: express, seguranca, node, crud

Todo sistema sério registra quem fez o quê. Sem isso, quando um preço aparecer errado, ninguém consegue dizer se foi engano, sabotagem ou bug. Construa uma trilha de auditoria para o Café Cerrado: cada criação, alteração e exclusão vira uma linha imutável em um arquivo próprio, consultável por uma rota protegida.

**Critérios de pronto**

- Toda escrita bem-sucedida acrescenta uma entrada em `data/auditoria.jsonl` (um JSON por linha) com quem, quando, qual ação, qual id e o que mudou.
- O arquivo é **somente acrescido**: nenhuma parte do código reescreve linhas anteriores, e uma linha nova nunca sobrescreve outra mesmo com requisições simultâneas.
- `GET /api/auditoria` devolve as últimas 50 entradas, exige login e responde `403` para quem não for administrador (ou para quem não for dono de nenhum registro, se você não fez o desafio anterior).
- O registro é feito por um único ponto do código, não repetido em cada controlador.
- Um teste de carga simples (20 requisições disparadas em paralelo com `Promise.all` num script) prova que nenhuma linha se perdeu nem saiu corrompida.

<details markdown="1">
<summary>Pistas</summary>

1. `fs.appendFile` é a operação certa: ela abre no modo `a`, que grava no fim do arquivo — diferente do `writeFile`, que trunca.
2. O formato JSONL (um objeto JSON por linha, sem vírgulas nem colchetes) existe exatamente para arquivos que só crescem: dá para acrescentar sem reler o que já está lá.
3. Para não repetir código, pense em onde uma função pode observar todas as respostas: um middleware colocado **antes** das rotas pode registrar-se no evento `finish` da resposta (`res.on("finish", ...)`) e ler `res.statusCode` depois de tudo pronto.
4. Para saber o que mudou, compare o objeto antes e depois: `Object.keys(depois).filter((k) => antes[k] !== depois[k])` já dá uma lista de campos alterados.
5. Para as últimas 50 linhas sem ler o arquivo inteiro na memória, `readFile` seguido de `split("\n").slice(-50)` resolve enquanto o arquivo for pequeno — e vale um comentário no código dizendo o que fazer quando não for mais.
</details>

### 🔥 Boss — O Café Cerrado recebe pedidos
Tags: projeto, crud, autenticacao, express

Este é o mini-projeto que fecha a Unidade 3 e usa tudo: rotas, controladores, middlewares, autenticação, autorização, persistência e front assíncrono. O cardápio está no ar e as pessoas querem **pedir**. Crie um segundo recurso completo — `pedidos` — que se relaciona com os produtos existentes, com regras de acesso próprias: cada cliente vê e cancela apenas os seus pedidos; o dono do produto vê os pedidos que envolvem os seus itens.

Um pedido tem, no mínimo: `id`, `produtoId`, `quantidade`, `observacao`, `cliente` (e-mail vindo do token), `situacao` (`recebido`, `preparando`, `entregue` ou `cancelado`) e `criadoEm`.

**Critérios de pronto**

- Um recurso `pedidos` completo, com `data/pedidosRepositorio.js`, `controllers/pedidosController.js` e `routes/pedidos.js`, seguindo exatamente a arquitetura em camadas do recurso de produtos.
- `POST /api/pedidos` exige login, valida que o `produtoId` existe (`400` se não existir), rejeita quantidade menor que 1 e grava o `cliente` a partir do token.
- `GET /api/pedidos` exige login e devolve **apenas** os pedidos do usuário — nunca os dos outros. Um segundo usuário logado não consegue ver os seus pedidos de forma alguma, nem variando ids na URL.
- `PATCH /api/pedidos/:id/situacao` muda a situação e só é permitido ao dono do **produto** pedido; transições inválidas (de `entregue` para `recebido`, por exemplo) respondem `400`.
- `DELETE /api/pedidos/:id` cancela o pedido, permitido só ao cliente e só enquanto a situação for `recebido`; caso contrário, `403` com mensagem explicando.
- Uma tela nova no front, consumindo a API pela mesma fachada `api.js`, com os quatro estados (carregando, erro, vazio, conteúdo) e feedback acessível.
- `testes.http` com um cenário para cada status possível (`200`, `201`, `204`, `400`, `401`, `403`, `404`) e o README atualizado com os endpoints novos.
- Tudo funcionando num `git clone` limpo, com `npm install && npm run dev`.

<details markdown="1">
<summary>Pistas</summary>

1. Comece pelo contrato, como na Aula 15: escreva a tabela de endpoints do recurso `pedidos` antes de programar. Metade dos problemas de integração morre aí.
2. O repositório de pedidos é quase idêntico ao de produtos. Resista à tentação de copiar e colar: escreva um `criarRepositorio(nomeDoArquivo)` que devolve `{ lerTodos, salvarTodos, proximoId }` e use-o duas vezes.
3. Para descobrir se o usuário é dono do produto de um pedido, o controlador de pedidos precisa consultar o repositório de produtos — isso é normal e não quebra as camadas; o que não pode é um repositório chamar o outro.
4. As transições válidas de situação cabem num objeto: `{ recebido: ["preparando", "cancelado"], preparando: ["entregue"], entregue: [], cancelado: [] }`. A validação vira uma linha, e a regra fica visível.
5. `PATCH` é o verbo certo aqui porque só um campo muda (veja a curiosidade da Aula 15 sobre `PUT` e `PATCH`). No Express 5, `app.patch` e `router.patch` existem e funcionam como os outros.
6. Para a tela, reaproveite a estrutura do `app.js`: estado, `renderizar()`, quatro estados. Um segundo módulo `public/js/pedidos.js` mantém os dois assuntos separados.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `403` ao editar um produto que é seu | O produto foi criado antes da regra e não tem o campo `dono` | Rode `node scripts/definir-dono.js seu-email@gmail.com` (seção 2.2) |
| `TypeError: Cannot read properties of undefined (reading 'email')` no controlador | A rota não passa por `exigirLogin`, então `req.usuario` não existe | Confira a ordem em `routes/produtos.js`: `exigirLogin` vem antes do controlador |
| Qualquer usuário logado consegue editar tudo | A comparação usa `req.body.dono` ou o campo nem é comparado | Use `produto.dono === req.usuario.email`, com o e-mail vindo do token |
| `PUT` responde `200` mas nada muda no arquivo | O objeto alterado veio de uma leitura diferente da lista que foi salva | Altere um item **de dentro** da lista que será passada a `salvarTodos` (seção 3.2) |
| `Error: Wrong recipient, payload audience != requiredAudience` | O `GOOGLE_CLIENT_ID` do `.env` não é o do projeto que emitiu o token (dois projetos no Google Cloud, ou o `.env` de outra máquina) | Corrija o `.env` e reinicie o servidor; o front lê o mesmo valor por `GET /api/config`, então não há um segundo lugar para ajustar |
| Tudo funciona por um tempo e depois só dá `401` | O token de sessão emitido em `POST /api/auth/google` expirou (8 horas, Aula 14) | Faça login de novo e atualize o `@tokenA`/`@tokenB` do `testes.http` |
| `Cannot find module 'google-auth-library'` num clone limpo | A dependência não está no `package.json` | `npm install google-auth-library` na pasta original e comite `package.json` e `package-lock.json` |
| A aplicação sobe vazia num clone limpo | `data/produtos.json` está no `.gitignore` ou nunca foi comitado | Versione um arquivo de dados com dois ou três itens de exemplo |
| `git push` recusado com aviso de segredo detectado | O `.env` (ou um token) entrou no commit | `git rm -r --cached .env`, comite, e gere um Client ID novo no Google Cloud Console |
| O botão de excluir some, mas o `curl` ainda apaga | A regra está só na interface, não no servidor | A checagem de `403` precisa estar no controlador ou no middleware (seção 3) |
| `EADDRINUSE: address already in use :::3000` | Ficou um servidor antigo rodando em outro terminal | Feche o outro terminal, ou `kill $(lsof -t -i:3000)` no Linux e no macOS |

## 🏠 Para praticar depois da aula (1 h)

Esta é a última atividade do semestre, e ela é a própria preparação da entrega:

1. Aplique a autorização por dono ao **projeto autoral**: campo de dono vindo do token, `403` em `PUT` e `DELETE` de registros alheios, e a regra num único ponto do código.
2. Rode o script de migração nos seus dados antigos, para que nenhum registro fique órfão.
3. Atualize a interface: exiba o autor de cada registro e mostre os controles de escrita apenas para quem pode usá-los.
4. Atualize o `testes.http` com os cenários de `401`, `403` e `404`, usando duas contas.
5. Escreva o `README.md` completo, seguindo a estrutura da seção 6.3.
6. Execute o roteiro de auto-teste da seção 5, os dez passos, e o teste da pasta limpa da seção 6.2.
7. Faça o commit final e confirme que `.env` e `node_modules/` não subiram.

**Critério de pronto:** o repositório clonado numa pasta vazia roda com `npm install && npm run dev`; um usuário logado só altera o que é dele; a documentação permite que outra pessoa reproduza tudo sem perguntar nada.

**Guarde no seu repositório:** commit + push, com o link público atualizado.

## ✅ Checkpoint do projeto

Ao final desta aula, o seu repositório precisa ter:

- [ ] Campo de dono gravado a partir do token verificado em toda criação.
- [ ] `403` em `PUT` e `DELETE` de registros de outra pessoa, com a regra em um único ponto do código.
- [ ] `401` em todas as rotas de escrita sem token; leitura pública funcionando sem login.
- [ ] Interface mostrando o autor de cada registro e escondendo controles de escrita de quem não pode usá-los.
- [ ] Script de migração versionado, para os registros criados antes da regra.
- [ ] `testes.http` cobrindo `200`, `201`, `204`, `400`, `401`, `403` e `404`, sem tokens reais comitados.
- [ ] `.gitignore` com `node_modules/` e `.env`; `.env.exemplo` versionado.
- [ ] `README.md` completo: descrição, tecnologias, como rodar, endpoints, estrutura de pastas e decisões técnicas.
- [ ] `npm install && npm run dev` funcionando num clone limpo.
- [ ] Roteiro de auto-teste da seção 5 executado, com os dez passos passando.

## 🎓 Marco do projeto — Unidade 3

**Escopo.** Aplicação full-stack do **projeto autoral**, construída sobre o Marco 2: API em Node.js com Express 5, autenticação com Google, CRUD completo com persistência e front-end assíncrono consumindo a própria API. Este é o marco final desta trilha — reúne tudo o que o projeto acumulou desde a Aula 01.

**Requisitos.**

| # | Requisito | Onde foi estudado |
|---|---|---|
| 1 | Servidor Express 5 servindo o front de `public/` e a API em `/api` | Aula 11 |
| 2 | Estrutura em camadas: `routes/`, `controllers/`, `data/`, `middlewares/`, `server.js` enxuto | Aulas 12 e 13 |
| 3 | Middlewares de `express.json()`, log de requisições, 404 da API e tratador de erros | Aula 12 |
| 4 | CRUD completo do recurso principal, com busca por query string | Aula 13 |
| 5 | Validação no servidor, com `400` e mensagem útil; status corretos em todas as rotas | Aulas 13 e 15 |
| 6 | Persistência em arquivo, isolada numa camada de repositório; dados sobrevivem ao reinício | Aula 15 |
| 7 | Login com Google Identity Services e verificação do ID token no servidor | Aula 14 |
| 8 | Segredos em `.env` fora do Git, com `.env.exemplo` versionado | Aula 14 |
| 9 | `401` nas rotas de escrita sem token; leitura pública funcionando | Aula 14 |
| 10 | Registros com dono e `403` ao alterar registro alheio | Aula 16 |
| 11 | Front consumindo a API com `fetch` e `async/await`, sem recarregar a página | Aula 15 |
| 12 | Quatro estados de tela (carregando, erro, vazio, conteúdo) e feedback com `aria-live` | Aula 15 |
| 13 | `testes.http` versionado, cobrindo sucesso e todos os erros previstos | Aulas 12 a 16 |
| 14 | `README.md` completo e projeto rodando num clone limpo com `npm install && npm run dev` | Aula 16 |

O repositório precisa ser **público no GitHub**, com histórico de commits mostrando evolução ao longo do semestre (não um único commit final), `.gitignore` funcionando e nenhum segredo versionado. Ele precisa conter o front em `public/`, o `testes.http` e o `README.md`.

### Checklist de qualidade

- **Rotas, controladores e middlewares:** arquitetura em camadas de verdade, com os status HTTP corretos em cada rota.
- **Autenticação Google:** botão funcionando, verificação do token no servidor (nunca só no cliente), segredos fora do Git.
- **CRUD com persistência:** as quatro operações completas, com validação e dados sobrevivendo ao reinício do servidor.
- **Autorização:** `401` em toda escrita sem token, `403` em registro alheio, dono sempre vindo do token — nunca do corpo da requisição.
- **Integração com front-end assíncrono:** `fetch`/`async-await`, os quatro estados de tela, nada recarregando a página.
- **README, `testes.http` e higiene do repositório:** roda de fato num clone limpo, sem depender da sua máquina.

Um critério "pela metade" costuma significar que ele funciona no caminho feliz mas falha num caso de borda (token expirado, registro alheio, lista vazia) — teste esses casos antes de considerar o marco pronto.

**Sobre IA:** use como apoio para tirar dúvidas, sugerir abordagens e revisar código — não para gerar o projeto inteiro sem entender. O teste real: você precisa conseguir explicar qualquer trecho do que construiu.

### Como saber que está pronto

- Execute o roteiro de auto-teste completo da seção 5 (os dez passos) numa janela anônima, com duas contas Google diferentes.
- Rode o teste da pasta limpa da seção 6.2: clone o próprio repositório numa pasta nova e confirme que `npm install && npm run dev` funciona sem ajustes manuais.
- Confira, pelo `testes.http`, que cada rota de escrita devolve `401` sem token e `403` para quem não é dono do registro.
- Abra o `README.md` como se fosse a primeira vez vendo o projeto: ele explica tecnologias, como rodar, endpoints e estrutura de pastas?
- Revise o histórico de commits: ele mostra o projeto evoluindo aula a aula, não aparecendo pronto de uma vez.

## 8. Depois daqui: para onde ir agora

Você entra nesta trilha sabendo HTML e CSS e sai com uma aplicação full-stack autenticada. O próximo passo depende do que despertou mais curiosidade ao longo do caminho — e há dois caminhos naturais dentro do próprio WebLab.

### 8.1 Nível 3 — Frameworks Modernos

O [Nível 3 — Frameworks Modernos](../nivel-3/) é a continuação direta desta trilha. Lá, o ciclo estado → render que você implementou à mão na Aula 15 vira **reatividade automática** com o Vue 3; o `criarCard` com `document.createElement` vira um componente declarativo; a fachada `api.js` vira uma instância do Axios com interceptadores; o estado que você guardou em variáveis de módulo vira uma store do Pinia. No back, o Express que você já conhece ganha um banco de dados de verdade (MySQL e Supabase), autenticação com Firebase e documentação com Swagger.

O mais importante: você vai reconhecer cada ferramenta como a automação de algo que **já entendeu**. Quem chega ao Vue sem ter escrito um render à mão aprende a sintaxe; quem chega depois desta trilha entende o mecanismo. É uma diferença que aparece na primeira vez que algo dá errado.

### 8.2 Trilha Deploy — tirar o projeto do `localhost`

O seu Café Cerrado roda em `http://localhost:3000`, o que significa que ele existe para exatamente uma pessoa. A trilha [Deploy & Ferramentas](../deploy/) é transversal e resolve isso; o capítulo mais direto para o que você acabou de construir é o [Capítulo 05 — Publicando o back-end Node](../deploy/cap-05.html), que pega uma API Express como a sua e a coloca no ar com URL pública, variáveis de ambiente configuradas no painel do serviço e HTTPS.

Um projeto publicado muda de natureza: vira link em currículo, vira coisa que dá para mostrar num processo seletivo, vira portfólio. Um repositório que só roda na sua máquina, não.

### 8.3 Caminhos por conta própria

- **Banco de dados de verdade.** Trocar `data/repositorio.js` por PostgreSQL ou MySQL é o próximo salto técnico — e, graças à arquitetura em camadas, mexe em um arquivo só. É um ótimo projeto de férias.
- **TypeScript.** Tipos sobre o JavaScript que você já domina. Em projetos que crescem, o ganho (erros detectados enquanto você escreve, autocomplete que funciona de verdade) é grande.
- **Testes automatizados.** O `testes.http` é o embrião. O passo seguinte é escrever testes que rodam sozinhos a cada commit, com o `node --test` que já vem no Node 22.
- **Portfólio.** Este repositório, com README caprichado e deploy no ar, já é peça de portfólio para estágio. Trate-o como cartão de visita: continue commitando, mesmo depois da nota.

## 📚 Para aprofundar

- MDN — Status HTTP `401 Unauthorized`: <https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Status/401> — leia por que o nome do status é enganoso.
- MDN — Status HTTP `403 Forbidden`: <https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Status/403> — a diferença prática em relação ao `401` e ao `404`.
- MDN — `Intl.RelativeTimeFormat`: <https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Global_Objects/Intl/RelativeTimeFormat> — base do exercício B1.
- MDN — `Window.sessionStorage`: <https://developer.mozilla.org/pt-BR/docs/Web/API/Window/sessionStorage> — para o exercício B4, com as ressalvas de segurança.
- OWASP Top 10 — Broken Access Control: <https://owasp.org/Top10/A01_2021-Broken_Access_Control/> — a categoria da falha corrigida hoje, com exemplos reais.
- Google Identity — verificação do ID token no servidor: <https://developers.google.com/identity/gsi/web/guides/verify-google-id-token> — a referência oficial do que o `google-auth-library` faz.
- Express 5 — roteamento: <https://expressjs.com/en/5x/api.html#router> — `router.patch`, encadeamento de middlewares e parâmetros de rota.
- Node.js — `fs.appendFile`: <https://nodejs.org/docs/latest-v22.x/api/fs.html#fspromisesappendfilepath-data-options> — base do desafio ⭐⭐⭐.
- Git — removendo arquivos do controle de versão: <https://git-scm.com/docs/git-rm> — a opção `--cached` em detalhe.
- GitHub Docs — sobre READMEs: <https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes> — o que a plataforma espera do arquivo.
- QUEIRÓS, Ricardo; PORTELA, Filipe. *Introdução ao Desenvolvimento Moderno para a Web*. FCA, 2018 — releitura recomendada ao fim do curso, com a visão global agora fazendo sentido.
- LOUDON, Kyle. *Desenvolvimento de Grandes Aplicações Web*. Novatec, 2019 — segurança e evolução de aplicações que crescem.
- ALVES, William P. *Projetos de Sistemas Web*. Érica, 2015 — organização de projetos web do início ao fim.
- PUREWAL, Semmy. *Aprendendo a Desenvolver Aplicações Web*. Novatec, 2014 — aplicação completa com Node.js, do zero ao deploy.

---

**Fim do semestre.** Em dezesseis aulas, o mesmo projeto saiu de um `index.html` vazio e chegou a uma aplicação full-stack com API REST, login federado, autorização por dono e persistência — e você entende cada linha dela, porque escreveu cada uma. Guarde o repositório: ele é a prova de que você sabe construir um sistema web inteiro, e não apenas usar um framework. Na próxima aula da sua trajetória — a Aula 01 do [Nível 3](../nivel-3/) — esse mesmo conhecimento vira a base para Vue, Vuetify, Pinia e bancos de dados na nuvem. Bom exame a quem precisar, e bons deploys a todos.
