# Aula 13 — Rotas e controladores

> **Nível 2 — Desenvolvimento Web** · Unidade 3: Web dinâmica server-side
> WebLab · UNEMAT Sinop · Prof. Ivan Luiz Pedroso Pires
> **Carga:** 3 aulas de 50 min (presencial) + 1 h (assíncrona)

Na Aula 12 as rotas do Café Cerrado saíram do `server.js` e ganharam arquivo próprio com `express.Router`. Mas a lógica continua morando dentro delas: a rota sabe o endereço **e** faz o serviço. Hoje damos o último passo da arquitetura do back-end — a rota vira um índice de duas palavras por linha, o controlador executa, e uma terceira camada guarda os dados em disco. No fim da aula a API do Café Cerrado tem CRUD completo, busca por query string, validação de verdade e produtos que sobrevivem ao reinício do servidor.

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Explicar o papel de cada camada do padrão rota → controlador → repositório e justificar por que separá-las.
- Implementar os cinco endpoints REST de um recurso (`GET` lista, `GET` item, `POST`, `PUT`, `DELETE`) com os status HTTP corretos.
- Aplicar as convenções REST de nomenclatura de recursos e distinguir parâmetro de rota de query string.
- Filtrar, buscar e ordenar uma coleção no servidor a partir de `req.query`, sem depender do front-end.
- Escrever uma função de validação que devolve `400` com a lista de campos inválidos, em vez de derrubar o servidor.
- Persistir os dados em um arquivo JSON com `fs/promises`, tratando o caso de arquivo inexistente.
- Testar o ciclo completo criar → listar → atualizar → detalhar → excluir → detalhar com o REST Client e com `curl`.

## 📋 Pré-requisitos desta aula

Na Aula 11 você criou o repositório `cafe-cerrado-api`, instalou o Express 5 e serviu o site da Unidade 2 pela pasta `public/`. Na Aula 12 o `server.js` virou uma montagem de peças: `express.json()`, middleware de log, `express.static`, o router de `/api/produtos`, o 404 da API e o tratador de erros. Hoje esvaziamos as rotas e distribuímos a lógica entre um controlador e um repositório.

Checklist antes de começar:

- [ ] `cafe-cerrado-api` rodando com `npm run dev` e respondendo em `http://localhost:3000`.
- [ ] `GET http://localhost:3000/api/produtos` devolvendo a lista de produtos em JSON.
- [ ] `POST /api/produtos` com corpo JSON funcionando (mesmo que sem validação caprichada) — sinal de que `express.json()` está no lugar certo.
- [ ] Extensão **REST Client** instalada no VS Code e o arquivo `testes.http` versionado no repositório.
- [ ] `node -v` mostrando 22 ou superior.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Camadas rota/controlador/repositório; convenções REST; status HTTP do CRUD |
| 2 | 50 min | Mão na massa: repositório em JSON, controlador completo, busca por query string, validação |
| 3 | 50 min | Roteiro de testes ponta a ponta no `testes.http`; laboratório |

## 1. Uma rota não deveria saber cozinhar

Olhe o arquivo de rotas que você terminou na Aula 12. Ele provavelmente parece com isto:

```js
// cafe-cerrado-api/routes/produtos.js — versão da Aula 12
const express = require('express');
const produtos = require('../data/produtos');

const router = express.Router();

router.get('/', (req, res) => {
  res.json(produtos);
});

router.get('/:id', (req, res) => {
  const produto = produtos.find((p) => p.id === Number(req.params.id));
  if (!produto) {
    return res.status(404).json({ erro: 'Produto não encontrado.' });
  }
  res.json(produto);
});

module.exports = router;
```

Funciona. Com dois endpoints, funciona muito bem. O problema aparece quando o recurso cresce: some `POST`, `PUT`, `DELETE`, validação de cada campo, filtro por categoria, busca por nome, ordenação, e daqui a duas aulas a checagem de quem está logado. O arquivo de rotas passa de 20 para 200 linhas e você perde a resposta para uma pergunta simples: **o que esta API oferece?**

A separação que vamos fazer hoje responde a essa pergunta em cinco linhas. Ela tem nome — é o **MVC aplicado ao servidor** — e três camadas:

| Camada | Arquivo | Responsabilidade |
|---|---|---|
| Rota | `routes/produtos.js` | Casar método + caminho com uma função. Nada além disso. |
| Controlador | `controllers/produtosController.js` | Ler a requisição, validar, decidir status e montar a resposta. |
| Repositório (dados) | `data/repositorio.js` | Ler e gravar os produtos. Não sabe que existe HTTP. |

A estrutura final do projeto de hoje:

```text
cafe-cerrado-api/
├── controllers/
│   └── produtosController.js
├── data/
│   ├── produtos.json
│   └── repositorio.js
├── public/
│   ├── index.html
│   ├── cardapio.html
│   ├── css/
│   └── js/
├── routes/
│   └── produtos.js
├── package.json
├── server.js
└── testes.http
```

### 1.1 Por que isso não é burocracia

Três motivos práticos, em ordem de importância para você agora:

1. **Navegabilidade.** Abrir `routes/produtos.js` e ver cinco linhas é abrir o índice da API. Quem entra no projeto — inclusive você daqui a três semanas — descobre em dez segundos o que existe.
2. **Testabilidade.** Um controlador é uma função comum que recebe `req` e `res`. Dá para chamá-la sem subir servidor. Um repositório é uma função que devolve dados; dá para trocá-lo por outro sem tocar em nada acima.
3. **Divisão de trabalho.** Duas pessoas mexendo no mesmo arquivo de 200 linhas geram conflito de merge toda hora. Em arquivos separados por responsabilidade, cada uma trabalha no seu.

Há um quarto motivo, que só aparece mais tarde: quando você trocar o arquivo JSON por um banco de dados de verdade, **só o repositório muda**. Rotas, controladores e front-end continuam iguais. Essa é a promessa das camadas, e você vai comprová-la no Nível 3.

> **🔎 Por baixo do capô**
> O "M" do MVC (Model) é frequentemente confundido com "a tabela do banco". No desenho original, de Trygve Reenskaug nos anos 1970 para a linguagem Smalltalk, o Model é o **domínio** — os dados e as regras que valem sobre eles, independentemente de tela ou de protocolo. É por isso que o nosso `repositorio.js` não pode conter `res.status(404)`: status HTTP é assunto do controlador, não do domínio. Se o repositório souber o que é HTTP, você não consegue reaproveitá-lo em um script de linha de comando, em um job agendado ou em um teste.

### 1.2 O controlador em três movimentos

Todo controlador de API faz sempre as mesmas três coisas, nesta ordem:

1. **Extrair** o que veio na requisição: `req.params`, `req.query`, `req.body`, `req.headers`.
2. **Decidir**: os dados são válidos? O recurso existe? Quem pediu tem permissão (a partir da Aula 14)?
3. **Responder**: escolher o status, montar o corpo, devolver.

Quando um controlador seu passar de umas 25 linhas, quase sempre é porque o passo 2 cresceu — e o passo 2 é regra de negócio, que merece uma função à parte. Você vai fazer exatamente isso com a validação, na seção 5.

## 2. REST: as convenções que todo mundo já espera

REST é o estilo arquitetural descrito por Roy Fielding em 2000 para explicar por que a web funciona em escala planetária. Na prática do dia a dia, ele virou um punhado de convenções sobre como URLs e métodos HTTP expressam operações. Segui-las não é frescura: é o que faz um desenvolvedor abrir sua API pela primeira vez e adivinhar corretamente como usá-la.

| Operação | Método e caminho | Sucesso |
|---|---|---|
| Listar | `GET /api/produtos` | `200` + array |
| Detalhar | `GET /api/produtos/7` | `200` + objeto |
| Criar | `POST /api/produtos` | `201` + objeto criado |
| Atualizar | `PUT /api/produtos/7` | `200` + objeto atualizado |
| Excluir | `DELETE /api/produtos/7` | `204` sem corpo |

As regras que sustentam essa tabela:

- **Recursos são substantivos no plural**: `/produtos`, `/categorias`, `/pedidos`. Nunca `/criarProduto` ou `/listarProdutos` — o verbo já está no método HTTP. Uma URL com verbo é o sintoma mais fácil de detectar de uma API que não é REST.
- **Parâmetro de rota identifica**: `/api/produtos/7` diz *qual* produto. É parte da identidade do recurso.
- **Query string refina**: `/api/produtos?categoria=doces&ordenar=preco` diz *como* listar. Ela nunca muda qual recurso está sendo acessado, só a fatia devolvida.
- **Aninhamento expressa relação**: `GET /api/produtos/7/avaliacoes` são as avaliações do produto 7. Use no máximo dois níveis; três já viram um labirinto.
- **O mesmo caminho serve a métodos diferentes**: `/api/produtos/7` responde a `GET`, `PUT` e `DELETE`. Isso é proposital — o recurso é um só; o que muda é a intenção.

### 2.1 Idempotência: a propriedade que quase ninguém explica

Um método é **idempotente** quando repeti-lo produz o mesmo estado final que executá-lo uma vez.

- `GET` é idempotente e **seguro** (não muda nada). Peça mil vezes, o servidor continua igual.
- `PUT` é idempotente: mandar o mesmo produto atualizado dez vezes deixa o produto no mesmo estado.
- `DELETE` é idempotente quanto ao **estado**: depois da primeira exclusão o recurso não existe mais, e continuar excluindo não muda isso (a resposta, sim, muda para `404` — o estado, não).
- `POST` **não** é idempotente: dez requisições criam dez produtos.

Isso não é trivia de prova. É a razão pela qual navegadores e proxies podem repetir automaticamente um `GET` que falhou por timeout, mas nunca repetem um `POST` — e é por isso que aquele aviso "não atualize a página, seu pedido está sendo processado" existe em site de compra.

> **📌 Na prova**
> Saiba dizer, com exemplo, a diferença entre método **seguro** (não altera estado: `GET`, `HEAD`, `OPTIONS`) e método **idempotente** (repetir não muda o resultado: os seguros mais `PUT` e `DELETE`). Todo método seguro é idempotente; o contrário não vale — `DELETE` é idempotente e não é seguro.

### 2.2 `PUT` ou `PATCH`?

Pelo livro, `PUT` **substitui** o recurso inteiro: o que não vier no corpo deveria ser apagado. `PATCH` aplica uma alteração parcial: só os campos enviados mudam.

Na prática, uma quantidade enorme de APIs implementa `PUT` com semântica de `PATCH`, porque é mais cômodo para o front. Nós vamos fazer o mesmo — mas conscientemente, e o documento de contrato da API vai dizer isso com todas as letras. O desafio ⭐⭐ desta aula pede que você implemente os dois com a semântica correta e sinta a diferença.

> **🧠 Você sabia?**
> A tese de doutorado que definiu REST não descreve nenhuma API. Roy Fielding, um dos autores da especificação do HTTP/1.1, escreveu em 2000 um trabalho sobre *estilos arquiteturais de software em rede*, e o capítulo 5 — chamado "Representational State Transfer" — explica por que a própria web escala: recursos com identificadores únicos, comunicação sem estado, respostas cacheáveis, interface uniforme. O termo "API REST", que hoje aparece em toda vaga de emprego, é uma leitura bem mais estreita do que ele propôs. Fielding chegou a escrever, anos depois, um texto irritado dizendo que a maioria das "APIs REST" não é REST.

### 2.3 O contrato da API, por escrito

Uma API só é útil quando alguém consegue usá-la sem ler o seu código. Esse "alguém" pode ser um colega de equipe, um aplicativo móvel, ou você mesmo na Aula 15, escrevendo o front. O documento que torna isso possível chama-se **contrato**: para cada endpoint, qual método, qual caminho, o que vai no corpo, o que volta e com qual status.

Este é o contrato do recurso `produto` do Café Cerrado, que você vai implementar hoje e colar no `README.md`:

| Método e caminho | Corpo da requisição | Resposta |
|---|---|---|
| `GET /api/produtos` | — | `200` + array de produtos |
| `GET /api/produtos/:id` | — | `200` + produto, ou `404` |
| `POST /api/produtos` | produto sem `id` | `201` + produto criado, ou `400` |
| `PUT /api/produtos/:id` | campos a alterar | `200` + produto atualizado, `400` ou `404` |
| `DELETE /api/produtos/:id` | — | `204` sem corpo, ou `404` |

Parâmetros de query string aceitos por `GET /api/produtos`:

| Parâmetro | Exemplo | Efeito |
|---|---|---|
| `q` | `?q=cafe` | Busca no nome e na descrição, ignorando acento e caixa |
| `categoria` | `?categoria=doces` | Filtra por categoria exata |
| `ordenar` | `?ordenar=preco` | Ordena por `preco`, `-preco` (decrescente) ou `nome` |

E o formato de um produto, que é o mesmo na entrada e na saída (menos o `id`, que o servidor gera):

```json
{
  "id": 3,
  "nome": "Bolo de castanha-de-baru",
  "categoria": "doces",
  "preco": 9.5,
  "descricao": "Fatia generosa com castanha nativa do cerrado.",
  "imagem": "img/bolo-baru.jpg"
}
```

Escreva o contrato **antes** de programar, mesmo trabalhando sozinho. Ele obriga você a decidir os nomes e os status antes de estar com as mãos no código, e vira a fonte da verdade quando front e back discordam. Em projetos maiores, esse documento é gerado em um formato padronizado chamado OpenAPI — no Nível 3 você vai vê-lo funcionando com o Swagger.

## 3. Os status HTTP que sua API vai usar hoje

Escolher o status certo é comunicação, não decoração. O front-end da Aula 15 vai tomar decisões olhando exclusivamente para o número: `201` limpa o formulário, `400` mostra os erros nos campos, `404` mostra "produto não encontrado", `401` manda fazer login.

| Código | Nome | Quando devolver |
|---|---|---|
| `200` | OK | Consulta ou atualização bem-sucedida, com corpo. |
| `201` | Created | Recurso criado. Devolva o objeto criado e o cabeçalho `Location`. |
| `204` | No Content | Sucesso sem nada a dizer. O caso clássico é `DELETE`. |
| `400` | Bad Request | O cliente mandou dados inválidos ou incompletos. |
| `404` | Not Found | O recurso pedido não existe (ou a rota não existe). |
| `409` | Conflict | O pedido conflita com o estado atual (nome duplicado, por exemplo). |
| `500` | Internal Server Error | Deu errado do lado do servidor. Culpa sua, não do cliente. |

A regra mnemônica das faixas: **2xx** deu certo; **3xx** procure em outro lugar; **4xx** o cliente errou; **5xx** o servidor errou. Um `500` em log de produção é sempre um bug esperando para ser corrigido — nunca use `500` para dizer "você digitou errado".

> **⚠️ Atenção**
> Devolver `200` com `{ "erro": "produto não encontrado" }` no corpo é um erro de projeto comum e caro. O `fetch` do front só rejeita a Promise em falha de rede; para tudo mais é preciso olhar `resposta.ok`, que é calculado a partir do status. Se você mente no status, o front precisa abrir o corpo e adivinhar — e quando alguém consumir sua API com outra ferramenta, vai contar como sucesso o que foi falha.

> **🔬 Investigue**
> Com o servidor da Aula 12 rodando, execute no terminal: `curl -i http://localhost:3000/api/produtos` e depois `curl -i http://localhost:3000/api/produtos/9999`. A opção `-i` mostra a linha de status e os cabeçalhos antes do corpo. Anote três coisas: o status de cada resposta, o valor de `Content-Type` e o valor de `Content-Length`. Agora rode `curl -I http://localhost:3000/api/produtos` (`-I` faz um `HEAD`): o corpo some, mas o `Content-Length` continua lá. Por que o servidor calcularia o tamanho de um corpo que não vai enviar?

## 4. Query string: filtrar no servidor

Na Unidade 2, a busca do cardápio do Café Cerrado filtrava um array já carregado no navegador com `filter`. Aquilo era correto para 12 produtos. Com 12 mil, baixar tudo para descartar 11.990 no cliente é desperdício de banda, de bateria e de tempo — e no celular do estudante que está no ônibus, isso se sente.

A partir de hoje o filtro mora no servidor, e o front só pede o que precisa:

```js
// no front, na Aula 15
const resposta = await fetch(`/api/produtos?q=${encodeURIComponent(termo)}`);
```

No Express, tudo que vem depois do `?` chega pronto em `req.query`, já decodificado e transformado em objeto:

```js
// GET /api/produtos?q=cafe&categoria=cafes&ordenar=preco
// req.query === { q: 'cafe', categoria: 'cafes', ordenar: 'preco' }
```

Três cuidados que separam uma listagem robusta de uma quebradiça:

1. **Todo valor de query string é string.** `?limite=10` chega como `'10'`, não como `10`. Converta com `Number()` e valide antes de usar.
2. **O parâmetro pode não vir.** `req.query.q` é `undefined` quando ninguém buscou nada. Trate a ausência como "não filtre", nunca como "filtre por vazio".
3. **O mesmo parâmetro pode vir repetido.** `?categoria=doces&categoria=cafes` faz `req.query.categoria` virar um **array**. Se o seu código chama `.toLowerCase()` direto, ele quebra com `TypeError: categoria.toLowerCase is not a function`. Quem manda essa URL nem sempre é um usuário distraído; às vezes é alguém testando sua API.

> **⚠️ Atenção — mudou no Express 5**
> No Express 4 era possível escrever `req.query.categoria = 'doces'` dentro de um middleware para "normalizar" a entrada. No Express 5, `req.query` virou um *getter*: a propriedade é calculada na primeira leitura e **não aceita atribuição**. Se você tentar, o valor simplesmente não muda (ou estoura em modo estrito). Precisa de um valor tratado? Guarde em outra variável, ou pendure em `req` com outro nome: `req.filtros = { categoria }`.

### 4.1 Busca que não depende de acento nem de caixa

O cliente digita `cafe` no celular, sem acento e sem maiúscula. O produto se chama `Café coado da casa`. Comparação literal não acha nada, e o usuário conclui que a cafeteria não vende café.

A solução é normalizar os dois lados da comparação com a mesma função:

```js
function normalizar(texto) {
  return String(texto)
    .normalize('NFD')                  // separa a letra do acento
    .replace(/[\u0300-\u036f]/g, '') // remove os acentos combinantes
    .toLowerCase()
    .trim();
}
```

`normalize('NFD')` decompõe `é` em `e` seguido de um acento combinante (um caractere invisível na faixa Unicode `U+0300`–`U+036F`). A expressão regular varre esses combinantes e os apaga, sobrando `e`. Mesma coisa para `ç`, `ã`, `ü`. É a mesma técnica que você usa para gerar *slug* de URL a partir de um título.

## 5. Validar no servidor: a única validação que conta

O `required` do HTML ajuda o usuário. O JavaScript do formulário ajuda mais ainda. Nenhum dos dois protege nada: qualquer pessoa abre o terminal e manda

```bash
curl -X POST http://localhost:3000/api/produtos \
  -H "Content-Type: application/json" \
  -d '{"nome":"","preco":-99,"categoria":"<script>"}'
```

sem nunca ter visto o seu formulário. Se a API aceitar, o produto entra no arquivo com preço negativo e o cardápio quebra para todo mundo.

Uma boa validação de API tem quatro propriedades:

1. **Devolve `400`**, não `500`. Dado ruim é culpa do cliente.
2. **Diz qual campo está errado**, para o front destacar o campo certo. Um `{"erro": "dados inválidos"}` genérico obriga o usuário a adivinhar.
3. **Devolve todos os erros de uma vez**, não um por requisição. Ninguém merece enviar o formulário cinco vezes.
4. **Normaliza enquanto valida**: corta espaços com `trim()`, converte `"6.5"` em `6.5`, arredonda o preço para dois decimais. O que entra no arquivo já entra limpo.

O formato de resposta que vamos adotar em todo o projeto:

```json
{
  "erro": "Dados inválidos.",
  "detalhes": [
    { "campo": "nome", "mensagem": "O nome precisa ter ao menos 3 caracteres." },
    { "campo": "preco", "mensagem": "O preço precisa ser um número maior que zero." }
  ]
}
```

Em projetos maiores você usaria uma biblioteca de validação por esquema (Zod, Joi, express-validator). Escrever a validação à mão uma vez, como faremos hoje, é o que faz você entender o que essas bibliotecas automatizam.

> **💡 Dica**
> Valide **e** normalize no mesmo lugar, devolvendo um objeto novo com só os campos aceitos. Nunca faça `produtos.push(req.body)`: isso deixa o cliente injetar qualquer campo no seu registro — inclusive um `dono` falso, que na Aula 16 vai virar problema de segurança de verdade.

## 6. Persistência: os dados precisam sobreviver ao <kbd>Ctrl</kbd> + <kbd>C</kbd>

Até a Aula 12, os produtos moravam em um array dentro de `data/produtos.js`. Isso significa que reiniciar o servidor apaga tudo que foi criado — e o `node --watch` reinicia sozinho a cada arquivo salvo. Você cria três produtos, corrige uma vírgula, e eles somem.

A solução definitiva é um banco de dados; ela chega no Nível 3. Para o Café Cerrado, um arquivo JSON entrega o conceito de persistência com o que você já sabe: ler arquivo, converter texto em objeto, converter objeto em texto, gravar.

O módulo do Node para isso é o `fs`, e a versão que interessa é a de Promises:

```js
const fs = require('node:fs/promises');
```

O prefixo `node:` explicita que o módulo é interno do Node, não um pacote do `node_modules`. É a forma recomendada desde o Node 18 e evita um ataque real chamado *dependency confusion*, em que alguém publica no npm um pacote com o nome de um módulo interno.

Duas armadilhas para tratar desde já:

- **O arquivo pode não existir** na primeira execução. `fs.readFile` lança um erro com `erro.code === 'ENOENT'` (*Error NO ENTry*). Nesse caso, o certo é devolver uma lista vazia, não derrubar o servidor.
- **Gravar direto por cima é arriscado.** Se o processo morrer no meio de um `writeFile`, o arquivo fica pela metade — e um JSON pela metade não é JSON. A técnica padrão é gravar em um arquivo temporário e depois renomeá-lo por cima do original: no mesmo sistema de arquivos, `rename` é atômico, ou seja, ou vale o conteúdo antigo inteiro ou o novo inteiro, nunca uma mistura.

> **🔎 Por baixo do capô**
> Por que `rename` é atômico e `writeFile` não? Porque `writeFile` copia bytes para dentro do arquivo, e uma queda no meio deixa metade nova e metade velha. Já `rename` só troca uma entrada de diretório: o nome `produtos.json` passa a apontar para outro conjunto de blocos que já está inteiro no disco. Essa é a mesma ideia que bancos de dados usam com o write-ahead log e que o Git usa ao gravar objetos. Um detalhe importante: isso só vale se o arquivo temporário estiver no **mesmo** sistema de arquivos — por isso criamos o `.tmp` ao lado do arquivo final, e não em `/tmp`.

## 🧩 Padrão de projeto em uso: Repository

O `data/repositorio.js` que você vai escrever no Mão na massa é uma implementação do padrão **Repository**, catalogado por Martin Fowler: uma camada que se comporta como uma coleção de objetos em memória e esconde completamente de onde os dados vêm.

O contrato do nosso repositório tem três funções: `lerTodos()`, `salvarTodos(lista)` e `proximoId(lista)`. Nenhuma delas menciona arquivo, caminho, JSON ou `fs`. Isso é proposital — é o que permite, no futuro, trocar o corpo dessas funções por consultas SQL sem que o controlador perceba.

O ganho fica visível quando você faz a conta do que muda em cada cenário:

| Mudança | O que precisa ser reescrito |
|---|---|
| Trocar JSON por MySQL | Só `data/repositorio.js` |
| Adicionar campo `estoque` ao produto | Validação no controlador |
| Trocar `/api/produtos` por `/api/v2/produtos` | Uma linha no `server.js` |

O preço do padrão é um arquivo a mais e uma indireção a mais para ler. Em um projeto de duas telas isso pode ser exagero; em um projeto que vai crescer por um semestre inteiro, paga-se sozinho na terceira semana.

## 💻 Mão na massa — CRUD completo da API do Café Cerrado

Objetivo desta prática: sair de duas rotas de leitura e chegar a cinco endpoints com validação, busca e persistência em disco. Trabalhe dentro de `cafe-cerrado-api`, com `npm run dev` rodando em um terminal.

### Passo 1 — Os dados saem do código e vão para o disco

Crie o arquivo de dados. Note que ele é **só dados**: nenhum `module.exports`, nenhuma vírgula sobrando, aspas duplas em todas as chaves — é JSON, não JavaScript.

`cafe-cerrado-api/data/produtos.json`

```json
[
  {
    "id": 1,
    "nome": "Café coado da casa",
    "categoria": "cafes",
    "preco": 6.5,
    "descricao": "Grãos do cerrado mato-grossense, torra média, coado na hora.",
    "imagem": "img/cafe-coado.jpg"
  },
  {
    "id": 2,
    "nome": "Cappuccino cremoso",
    "categoria": "cafes",
    "preco": 12.9,
    "descricao": "Espresso, leite vaporizado e canela em pó.",
    "imagem": "img/cappuccino.jpg"
  },
  {
    "id": 3,
    "nome": "Bolo de castanha-de-baru",
    "categoria": "doces",
    "preco": 9.5,
    "descricao": "Fatia generosa com castanha nativa do cerrado.",
    "imagem": "img/bolo-baru.jpg"
  },
  {
    "id": 4,
    "nome": "Pão de queijo mineiro",
    "categoria": "salgados",
    "preco": 5.0,
    "descricao": "Assado a cada duas horas, servido quente.",
    "imagem": "img/pao-de-queijo.jpg"
  },
  {
    "id": 5,
    "nome": "Açaí batido na hora",
    "categoria": "bebidas-geladas",
    "preco": 18.0,
    "descricao": "Polpa pura com granola e banana.",
    "imagem": "img/acai.jpg"
  }
]
```

Agora o repositório. Ele é a única parte do sistema que sabe que existe um arquivo.

`cafe-cerrado-api/data/repositorio.js`

```js
// Camada de acesso a dados do Café Cerrado.
// Só esta camada sabe que os produtos moram em um arquivo JSON.
const fs = require('node:fs/promises');
const path = require('node:path');

const ARQUIVO = path.join(__dirname, 'produtos.json');

// Lê o arquivo inteiro e devolve um array de produtos.
// Se o arquivo ainda não existe, começa vazio em vez de estourar.
async function lerTodos() {
  try {
    const texto = await fs.readFile(ARQUIVO, 'utf-8');
    return JSON.parse(texto);
  } catch (erro) {
    if (erro.code === 'ENOENT') {
      return [];
    }
    throw erro;
  }
}

// Grava a lista inteira. Escreve primeiro em um arquivo temporário e
// depois renomeia: assim nunca sobra um JSON pela metade no disco.
async function salvarTodos(lista) {
  const temporario = `${ARQUIVO}.tmp`;
  await fs.writeFile(temporario, JSON.stringify(lista, null, 2), 'utf-8');
  await fs.rename(temporario, ARQUIVO);
}

// Próximo id disponível: o maior existente mais um.
function proximoId(lista) {
  return lista.reduce((maior, produto) => Math.max(maior, produto.id), 0) + 1;
}

module.exports = { lerTodos, salvarTodos, proximoId };
```

Repare no `path.join(__dirname, 'produtos.json')`. Se você escrevesse `'./data/produtos.json'`, o caminho seria resolvido a partir do diretório de onde você **rodou** o `node`, não de onde o arquivo está. Rodar `npm run dev` de dentro de outra pasta quebraria tudo. `__dirname` é a pasta do arquivo atual e resolve isso de vez.

Por fim, apague o antigo `data/produtos.js` — ele foi substituído.

```bash
cd cafe-cerrado-api
rm data/produtos.js
```

### Passo 2 — O controlador: leitura

Crie a pasta e o arquivo do controlador. Começamos pelas duas operações de leitura, já com busca, filtro e ordenação.

`cafe-cerrado-api/controllers/produtosController.js`

```js
const repositorio = require('../data/repositorio');

const CATEGORIAS = ['cafes', 'doces', 'salgados', 'bebidas-geladas'];

// Deixa o texto comparável: sem acento, sem maiúscula, sem espaço nas pontas.
function normalizar(texto) {
  return String(texto)
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .trim();
}

// GET /api/produtos?q=cafe&categoria=cafes&ordenar=preco
exports.listar = async (req, res) => {
  const { q, categoria, ordenar } = req.query;
  let lista = await repositorio.lerTodos();

  if (typeof categoria === 'string' && categoria !== '') {
    const alvo = normalizar(categoria);
    lista = lista.filter((produto) => normalizar(produto.categoria) === alvo);
  }

  if (typeof q === 'string' && q !== '') {
    const termo = normalizar(q);
    lista = lista.filter(
      (produto) =>
        normalizar(produto.nome).includes(termo) ||
        normalizar(produto.descricao).includes(termo),
    );
  }

  if (ordenar === 'preco') {
    lista = [...lista].sort((a, b) => a.preco - b.preco);
  } else if (ordenar === '-preco') {
    lista = [...lista].sort((a, b) => b.preco - a.preco);
  } else if (ordenar === 'nome') {
    lista = [...lista].sort((a, b) => a.nome.localeCompare(b.nome, 'pt-BR'));
  }

  res.json(lista);
};

// GET /api/produtos/7
exports.obter = async (req, res) => {
  const id = Number(req.params.id);
  if (!Number.isInteger(id) || id <= 0) {
    return res.status(400).json({ erro: 'O id precisa ser um número inteiro positivo.' });
  }

  const lista = await repositorio.lerTodos();
  const produto = lista.find((item) => item.id === id);
  if (!produto) {
    return res.status(404).json({ erro: `Produto ${id} não encontrado.` });
  }

  res.json(produto);
};
```

Três decisões que valem comentário:

- `typeof categoria === 'string'` protege contra a query string repetida (`?categoria=a&categoria=b`), que chegaria como array e quebraria o `normalizar`.
- `[...lista].sort(...)` ordena uma **cópia**. `sort` altera o array original, e o original aqui veio direto do arquivo — ordenar no lugar não faria estrago hoje, mas é o tipo de efeito colateral que assombra depois.
- `Number('abc')` é `NaN`, e `Number.isInteger(NaN)` é `false`. Por isso `/api/produtos/abc` devolve `400`, e não uma busca silenciosa por `undefined`.

### Passo 3 — Validação e escrita

Acrescente ao **mesmo arquivo** do controlador, logo abaixo de `normalizar`, a função de validação:

`cafe-cerrado-api/controllers/produtosController.js` (acrescente após `normalizar`)

```js
// Valida e normaliza o corpo da requisição.
// Com { parcial: true }, campos ausentes são ignorados (usado no PUT).
function validarProduto(corpo = {}, { parcial = false } = {}) {
  const erros = [];
  const dados = {};

  if (corpo.nome !== undefined || !parcial) {
    const nome = typeof corpo.nome === 'string' ? corpo.nome.trim() : '';
    if (nome.length < 3) {
      erros.push({ campo: 'nome', mensagem: 'O nome precisa ter ao menos 3 caracteres.' });
    } else {
      dados.nome = nome;
    }
  }

  if (corpo.preco !== undefined || !parcial) {
    const preco = Number(corpo.preco);
    if (!Number.isFinite(preco) || preco <= 0) {
      erros.push({ campo: 'preco', mensagem: 'O preço precisa ser um número maior que zero.' });
    } else {
      dados.preco = Math.round(preco * 100) / 100;
    }
  }

  if (corpo.categoria !== undefined || !parcial) {
    const categoria = typeof corpo.categoria === 'string' ? normalizar(corpo.categoria) : '';
    if (!CATEGORIAS.includes(categoria)) {
      erros.push({
        campo: 'categoria',
        mensagem: `A categoria precisa ser uma destas: ${CATEGORIAS.join(', ')}.`,
      });
    } else {
      dados.categoria = categoria;
    }
  }

  if (corpo.descricao !== undefined) {
    dados.descricao = String(corpo.descricao).trim();
  } else if (!parcial) {
    dados.descricao = '';
  }

  if (corpo.imagem !== undefined) {
    dados.imagem = String(corpo.imagem).trim();
  } else if (!parcial) {
    dados.imagem = '';
  }

  return { erros, dados };
}
```

Agora as três operações de escrita, no fim do arquivo:

`cafe-cerrado-api/controllers/produtosController.js` (acrescente ao final)

```js
// POST /api/produtos
exports.criar = async (req, res) => {
  const { erros, dados } = validarProduto(req.body);
  if (erros.length > 0) {
    return res.status(400).json({ erro: 'Dados inválidos.', detalhes: erros });
  }

  const lista = await repositorio.lerTodos();
  const novo = { id: repositorio.proximoId(lista), ...dados };

  lista.push(novo);
  await repositorio.salvarTodos(lista);

  res.status(201).location(`/api/produtos/${novo.id}`).json(novo);
};

// PUT /api/produtos/7
exports.atualizar = async (req, res) => {
  const id = Number(req.params.id);
  const lista = await repositorio.lerTodos();
  const indice = lista.findIndex((item) => item.id === id);

  if (indice === -1) {
    return res.status(404).json({ erro: `Produto ${id} não encontrado.` });
  }

  const { erros, dados } = validarProduto(req.body, { parcial: true });
  if (erros.length > 0) {
    return res.status(400).json({ erro: 'Dados inválidos.', detalhes: erros });
  }
  if (Object.keys(dados).length === 0) {
    return res.status(400).json({ erro: 'Envie ao menos um campo para atualizar.' });
  }

  const atualizado = { ...lista[indice], ...dados, id };
  lista[indice] = atualizado;
  await repositorio.salvarTodos(lista);

  res.json(atualizado);
};

// DELETE /api/produtos/7
exports.remover = async (req, res) => {
  const id = Number(req.params.id);
  const lista = await repositorio.lerTodos();
  const indice = lista.findIndex((item) => item.id === id);

  if (indice === -1) {
    return res.status(404).json({ erro: `Produto ${id} não encontrado.` });
  }

  lista.splice(indice, 1);
  await repositorio.salvarTodos(lista);

  res.status(204).end();
};
```

Detalhes que merecem sua atenção:

- Em `criar`, o objeto novo é montado como `{ id: ..., ...dados }`, e não a partir de `req.body`. Só os campos que a validação aprovou entram no arquivo.
- Em `atualizar`, o `id` aparece **de novo** no fim de `{ ...lista[indice], ...dados, id }`. Isso impede que alguém troque o id do produto mandando `{"id": 999}` no corpo — o último valor vence no espalhamento.
- `res.status(204).end()`: `204` significa "sem conteúdo". Chamar `res.json()` depois de `204` é contraditório, e alguns clientes reclamam.
- Nenhum controlador tem `try/catch`. No Express 5, um erro lançado dentro de uma função `async` é capturado e encaminhado automaticamente ao middleware de erro. Era exatamente isso que exigia `.catch(next)` no Express 4.

### Passo 4 — A rota vira índice

Agora o arquivo de rotas fica com uma linha por endpoint. É o índice da API:

`cafe-cerrado-api/routes/produtos.js`

```js
const express = require('express');
const controlador = require('../controllers/produtosController');

const router = express.Router();

router.get('/', controlador.listar);
router.get('/:id', controlador.obter);
router.post('/', controlador.criar);
router.put('/:id', controlador.atualizar);
router.delete('/:id', controlador.remover);

module.exports = router;
```

> **⚠️ Atenção**
> A ordem importa. Se você acrescentar depois uma rota fixa como `router.get('/destaques', ...)`, ela precisa vir **antes** de `router.get('/:id', ...)`. O Express testa na ordem de registro, e `/:id` casa com qualquer coisa — inclusive com a palavra `destaques`, que viraria `req.params.id = 'destaques'` e devolveria `400`. Esse é o desafio ⭐ de hoje.

E o `server.js` só muda no 404 da API, que agora usa o curinga do Express 5:

`cafe-cerrado-api/server.js`

```js
const express = require('express');
const produtosRouter = require('./routes/produtos');

const app = express();
const PORTA = 3000;

// 1. Interpreta corpos JSON e coloca o resultado em req.body.
app.use(express.json());

// 2. Log de toda requisição, com status e duração.
app.use((req, res, next) => {
  const inicio = Date.now();
  res.on('finish', () => {
    const duracao = Date.now() - inicio;
    console.log(`${req.method} ${req.originalUrl} -> ${res.statusCode} (${duracao} ms)`);
  });
  next();
});

// 3. Site estático do Café Cerrado (Unidades 1 e 2).
app.use(express.static('public'));

// 4. Recurso produtos.
app.use('/api/produtos', produtosRouter);

// 5. Qualquer outra rota sob /api que não casou: 404 em JSON.
app.all('/api/{*splat}', (req, res) => {
  res.status(404).json({ erro: `Rota ${req.method} ${req.originalUrl} não existe.` });
});

// 6. Tratador de erros: quatro parâmetros, sempre por último.
app.use((erro, req, res, next) => {
  console.error(erro);
  res.status(500).json({ erro: 'Erro interno do servidor.' });
});

app.listen(PORTA, () => {
  console.log(`Café Cerrado API em http://localhost:${PORTA}`);
});
```

O padrão `'/api/{*splat}'` é a sintaxe de curinga do Express 5. As chaves tornam o trecho opcional (então `/api` sozinho também casa) e `*splat` captura o resto do caminho em `req.params.splat`, que é um **array** de segmentos. No Express 4 isso se escrevia `'/api/*'` — se você encontrar essa forma em um tutorial antigo, saiba que ela não funciona mais.

> **💡 Dica**
> O log do passo 2 usa `res.on('finish', ...)` em vez de imprimir antes de `next()`. A diferença: `finish` dispara quando a resposta terminou de ser enviada, então você consegue registrar o **status** e a **duração** reais. Um log que só mostra o que entrou não ajuda a caçar lentidão.

### Passo 5 — O roteiro de testes

Substitua o `testes.http` da Aula 12 por este roteiro completo. Cada bloco separado por `###` vira um botão "Send Request" no VS Code.

`cafe-cerrado-api/testes.http`

```http
@base = http://localhost:3000/api

### 1. Listar tudo (200, array com 5 itens)
GET {{base}}/produtos

### 2. Buscar por nome, sem acento e em minúscula (200, acha "Café coado da casa")
GET {{base}}/produtos?q=cafe

### 3. Filtrar por categoria e ordenar do mais barato ao mais caro (200)
GET {{base}}/produtos?categoria=doces&ordenar=preco

### 4. Detalhar um produto existente (200)
GET {{base}}/produtos/3

### 5. Detalhar um id inexistente (404)
GET {{base}}/produtos/9999

### 6. Detalhar um id que nem é número (400)
GET {{base}}/produtos/abacaxi

### 7. Criar produto válido (201 + cabeçalho Location)
POST {{base}}/produtos
Content-Type: application/json

{
  "nome": "Suco de cupuaçu",
  "categoria": "bebidas-geladas",
  "preco": 11.5,
  "descricao": "Polpa batida com água gelada, sem açúcar.",
  "imagem": "img/suco-cupuacu.jpg"
}

### 8. Criar produto inválido (400 com dois itens em detalhes)
POST {{base}}/produtos
Content-Type: application/json

{
  "nome": "Ab",
  "categoria": "sobremesa",
  "preco": -3
}

### 9. Atualizar só o preço (200, os outros campos continuam iguais)
PUT {{base}}/produtos/6
Content-Type: application/json

{
  "preco": 12.9
}

### 10. Atualizar produto inexistente (404)
PUT {{base}}/produtos/9999
Content-Type: application/json

{
  "preco": 1
}

### 11. Excluir (204, sem corpo)
DELETE {{base}}/produtos/6

### 12. Excluir de novo (404 — o recurso já não existe)
DELETE {{base}}/produtos/6

### 13. Rota de API que não existe (404 em JSON, não em HTML)
GET {{base}}/pedidos
```

### Como testar

Com `npm run dev` rodando, execute os 13 blocos **na ordem**. O roteiro foi montado para contar uma história: o bloco 7 cria o produto de id 6, o 9 altera esse mesmo produto, o 11 o exclui e o 12 prova que ele sumiu.

O resultado esperado, bloco a bloco:

| Blocos | Status esperado | O que confirma |
|---|---|---|
| 1 a 4 | `200` | Leitura, busca, filtro e ordenação |
| 5 e 6 | `404` e `400` | Id inexistente × id malformado |
| 7 e 8 | `201` e `400` | Criação e validação com `detalhes` |
| 9 a 13 | `200`, `404`, `204`, `404`, `404` | Atualização parcial, exclusão e 404 de API |

Duas provas finais, e só então a prática está encerrada:

1. Abra `data/produtos.json` no editor depois do bloco 7. O produto novo está lá, com indentação de 2 espaços. **Os dados saíram da memória e foram para o disco.**
2. Pare o servidor com <kbd>Ctrl</kbd> + <kbd>C</kbd>, suba de novo e rode o bloco 1. O produto criado continua na lista. Era exatamente isso que não acontecia até a Aula 12.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Preveja o status HTTP de cada chamada abaixo **sem rodar**, usando só o código do Mão na massa. Depois rode as quatro e confira.

```bash
curl -i http://localhost:3000/api/produtos/2
curl -i http://localhost:3000/api/produtos/dois
curl -i -X DELETE http://localhost:3000/api/produtos/2
curl -i -X DELETE http://localhost:3000/api/produtos/2
```

**A2.** O cliente chama `GET /api/produtos?q=`. O que `req.query.q` vale nessa requisição, e por que a listagem devolve todos os produtos em vez de nenhum? Aponte a linha exata do controlador que decide isso.

**A3.** Verdadeiro ou falso, com uma linha de justificativa cada:

- (a) No Express 5, `exports.criar` precisa de `try/catch` para que um erro de `fs.writeFile` chegue ao tratador de erros.
- (b) `req.query.categoria = 'doces'` dentro de um middleware altera o filtro que o controlador vai ler.
- (c) `DELETE /api/produtos/2` repetido devolve o mesmo status nas duas vezes.

**A4.** Em `atualizar`, o objeto final é `{ ...lista[indice], ...dados, id }`. Descreva o que acontece com o produto 3 se um cliente mandar `PUT /api/produtos/3` com o corpo `{"id": 99, "preco": 7}` — e o que aconteceria se o `id` não estivesse repetido no fim.

**A5.** Alguém trocou `lista = [...lista].sort(...)` por `lista.sort(...)` no `listar`. O endpoint continua devolvendo a resposta certa? E o arquivo `produtos.json` no disco, muda? Justifique olhando de onde veio o array.

**A6.** Explique, em duas linhas, por que `data/repositorio.js` não pode conter `res.status(404)` — e o que quebraria se contivesse.

### Nível B — Aplicação

**B1.** Endpoint de contagem. Implemente `GET /api/produtos/contagem`, que devolve `{ "total": 5 }` respeitando os mesmos filtros de `q` e `categoria` do `listar`.

Resultado esperado: `GET /api/produtos/contagem?categoria=cafes` devolve `200` com `{"total":2}`; sem query string, devolve o total geral. A rota nova não pode ser engolida por `/:id`.

<details markdown="1">
<summary>Dica</summary>

Duas coisas: a rota fixa precisa ser registrada **antes** de `router.get('/:id', ...)`, e a lógica de filtro está duplicada — extraia-a para uma função `aplicarFiltros(lista, req.query)` usada pelos dois controladores.
</details>

**B2.** Segundo recurso completo. Crie o recurso `categorias` com rota e controlador próprios: `GET /api/categorias` devolve a lista de categorias com a quantidade de produtos de cada uma, e `GET /api/categorias/:slug/produtos` devolve os produtos daquela categoria.

Resultado esperado: `GET /api/categorias` devolve `[{"slug":"cafes","total":2}, ...]`; `GET /api/categorias/doces/produtos` devolve só os doces; `GET /api/categorias/inexistente/produtos` devolve `404`.

<details markdown="1">
<summary>Dica</summary>

Crie `routes/categorias.js` e `controllers/categoriasController.js`, e monte com `app.use('/api/categorias', categoriasRouter)` no `server.js`. Para contar por categoria, `reduce` sobre a lista de produtos acumulando em um objeto resolve em cinco linhas.
</details>

**B3.** Nome duplicado devolve `409`. Hoje é possível criar dois produtos chamados "Cappuccino cremoso". Impeça isso no `criar` e no `atualizar`, devolvendo `409 Conflict` com uma mensagem clara.

Resultado esperado: criar um produto com nome já existente (ignorando acento e caixa) devolve `409`; renomear um produto para o nome de outro também; renomear um produto para o **próprio** nome continua funcionando.

<details markdown="1">
<summary>Dica</summary>

Compare com `normalizar` dos dois lados. No `atualizar`, a checagem precisa ignorar o próprio produto: `lista.some((p) => p.id !== id && normalizar(p.nome) === normalizar(dados.nome))`.
</details>

**B4.** Contrato documentado. Escreva no `README.md` do `cafe-cerrado-api` a tabela de contrato da API: uma linha por endpoint, com método, caminho e o que devolve em caso de sucesso. Abaixo da tabela, um bloco JSON de exemplo do corpo do `POST` e um da resposta de erro `400`.

Resultado esperado: alguém que nunca viu o projeto consegue usar a API só lendo o README, sem abrir código.

<details markdown="1">
<summary>Dica</summary>

Cinco linhas na tabela (mais as que você criou nos itens B1 e B2). Não esqueça de documentar os parâmetros de query string aceitos por `GET /api/produtos` — é a parte que o front da Aula 15 mais vai usar.
</details>

### Nível C — Desafio em sala

**C1.** Paginação com metadados. Listar 12 produtos é fácil; listar 12 mil não é. Implemente paginação em `GET /api/produtos` com os parâmetros `pagina` (padrão 1) e `limite` (padrão 10, máximo 50), devolvendo um envelope com os dados e os metadados:

```json
{
  "dados": [],
  "paginacao": { "pagina": 2, "limite": 10, "total": 34, "totalPaginas": 4 }
}
```

Valores inválidos (`?pagina=0`, `?limite=999`, `?pagina=abc`) não podem quebrar nem devolver `500`: eles caem no padrão ou no teto. A paginação é aplicada **depois** do filtro e da ordenação — `total` é o total filtrado, não o total do arquivo.

Resultado esperado: `?limite=2&pagina=2` devolve os produtos 3 e 4 da lista ordenada, com `totalPaginas: 3`; `?pagina=99` devolve `dados: []` e `paginacao` coerente; `?limite=999` devolve no máximo 50 itens.

<details markdown="1">
<summary>Dica</summary>

`const pagina = Math.max(1, Number(req.query.pagina) || 1)` resolve `0`, `abc` e ausência de uma vez, porque `NaN || 1` é `1`. Para o limite, `Math.min(50, Math.max(1, Number(req.query.limite) || 10))`. A fatia é `lista.slice((pagina - 1) * limite, pagina * limite)`, e `totalPaginas` é `Math.ceil(total / limite)` — cuidado com o caso `total === 0`, em que o resultado deve ser `0` ou `1`, e não `NaN`.
</details>

## 🏆 Desafios

### ⭐ A rota que engoliu a palavra
Tags: express, rotas, bug, investigacao

O Café Cerrado quer uma vitrine de destaques na página inicial. Você acrescenta `router.get('/destaques', controlador.destaques)` no fim do arquivo de rotas, sobe o servidor, abre `http://localhost:3000/api/produtos/destaques` e recebe:

```json
{ "erro": "O id precisa ser um número inteiro positivo." }
```

O controlador `destaques` nem foi chamado — coloque um `console.log` dentro dele para se convencer. Descubra por que o Express entregou a requisição para o controlador errado e conserte, deixando o endpoint de destaques funcionando: ele devolve os três produtos mais caros.

**Critérios de pronto**

- `GET /api/produtos/destaques` devolve `200` com exatamente três produtos, do mais caro para o mais barato.
- `GET /api/produtos/3` continua devolvendo o produto 3, sem regressão.
- Um comentário de duas linhas no `routes/produtos.js` explica a regra que você descobriu sobre a ordem de registro das rotas.
- Um bloco novo no `testes.http` cobre o endpoint de destaques.

<details markdown="1">
<summary>Pistas</summary>

1. Adicione `console.log('entrou em obter', req.params.id)` na primeira linha de `exports.obter` e repita a requisição. O que aparece no terminal?
2. Leia a página "Routing" da documentação do Express prestando atenção em uma frase: as rotas são avaliadas na ordem em que foram definidas, e a primeira que casar vence.
3. `/:id` é um curinga de um segmento. Que caminhos de um segmento **não** casam com ele?
4. A correção é mover uma linha. A prevenção é uma convenção: rotas fixas antes de rotas com parâmetro, sempre.
</details>

### ⭐⭐ PUT que substitui, PATCH que remenda
Tags: api, http, rotas, refatoracao

O `PUT` que você escreveu hoje mente: pelo RFC 9110, `PUT` substitui o recurso inteiro, então mandar `{"preco": 12.9}` deveria apagar nome, categoria e descrição. O nosso preserva — comportamento de `PATCH` usando o nome errado. Muitas APIs de mercado fazem isso, mas quase nenhuma documenta, e é aí que o cliente se machuca. Implemente os dois métodos com a semântica correta e documente a diferença.

**Critérios de pronto**

- `PUT /api/produtos/3` com corpo incompleto devolve `400` listando os campos obrigatórios ausentes; com corpo completo, substitui todos os campos (o `id` é preservado).
- `PATCH /api/produtos/3` com `{"preco": 12.9}` altera só o preço e devolve `200` com o produto inteiro.
- `PATCH` com corpo `{}` devolve `400` com uma mensagem que explica o problema.
- A tabela de contrato no `README.md` ganha as duas linhas, com uma frase dizendo o que cada método faz com os campos ausentes.
- O `testes.http` prova a diferença: um `PUT` parcial que falha e um `PATCH` equivalente que funciona, lado a lado.

<details markdown="1">
<summary>Pistas</summary>

1. A função `validarProduto` já tem a chave: o `PUT` usa `{ parcial: false }` e o `PATCH` usa `{ parcial: true }`.
2. Com `parcial: false`, o objeto salvo deve ser montado do zero — `{ id, ...dados }` — e não espalhando o produto antigo por cima.
3. `router.patch('/:id', controlador.remendar)` é a linha nova no arquivo de rotas.
4. Antes de codificar, procure na especificação do HTTP (RFC 9110, seção sobre `PUT`) a frase que define substituição. Cole-a como comentário no controlador: ela justifica o `400`.
</details>

### ⭐⭐ O gerente que quer saber o que vende
Tags: api, express, json, crud

A dona do Café Cerrado pediu um resumo do cardápio: quantos produtos existem, quanto custa o mais caro e o mais barato, qual o preço médio por categoria. Ela não sabe o que é JSON, mas o seu front vai saber. Construa `GET /api/produtos/resumo` sem fazer o cálculo virar um monstro de dez `for` aninhados — e sem duplicar nada que já existe no controlador.

**Critérios de pronto**

- `GET /api/produtos/resumo` devolve `200` com `total`, `precoMinimo`, `precoMaximo`, `precoMedio` (duas casas) e um array `porCategoria` com `slug`, `total` e `precoMedio` de cada categoria.
- O resumo respeita `?categoria=` e `?q=`, reaproveitando a mesma função de filtro do `listar` (nenhuma linha de filtro copiada e colada).
- Com o cardápio vazio (renomeie `produtos.json` temporariamente), o endpoint devolve `200` com `total: 0` e nenhum `NaN` no corpo.
- Um bloco no `testes.http` e uma linha na tabela do `README.md`.

<details markdown="1">
<summary>Pistas</summary>

1. `reduce` resolve os quatro agregados numéricos em uma passada; `Math.min(...lista.map(...))` estoura com lista vazia, então trate esse caso antes.
2. Para agrupar por categoria sem bibliotecas: `Object.groupBy` existe no Node 22 e devolve um objeto com um array por chave.
3. Arredonde só na hora de responder: `Number(media.toFixed(2))` devolve número, enquanto `media.toFixed(2)` devolve string — e string em campo numérico atrapalha o front.
4. Lembre-se do desafio ⭐: `resumo` é uma rota fixa.
</details>

### ⭐⭐⭐ Dois pedidos ao mesmo tempo, um produto perdido
Tags: node, api, bug, performance

Seu `criar` faz três coisas em sequência: lê o arquivo, acrescenta um item, grava o arquivo. Entre a leitura e a gravação existe uma janela de alguns milissegundos. Se duas requisições entrarem nessa janela juntas, as duas leem a **mesma** lista de 5 itens, cada uma acrescenta o seu produto com o **mesmo** id 6, e a segunda gravação apaga a primeira. Isso se chama *lost update*, e é a razão de existirem transações em bancos de dados. Prove que o bug existe na sua API, meça o estrago e conserte.

**Critérios de pronto**

- Um script `scripts/estresse.js` dispara 50 `POST` simultâneos com `Promise.all` e imprime quantos produtos foram efetivamente gravados no arquivo. Antes da correção, o número é visivelmente menor que 50.
- Uma tabela de três linhas no `README.md` registra a medição: produtos esperados, produtos gravados antes da correção, produtos gravados depois.
- Depois da correção, as 50 requisições resultam em 50 produtos com ids únicos e sequenciais, sem nenhum id repetido.
- A correção fica **dentro** do repositório: o controlador não muda uma linha.
- Um comentário no `repositorio.js` explica em três linhas por que o Node, sendo de thread única, mesmo assim sofre desse problema.

<details markdown="1">
<summary>Pistas</summary>

1. O Node executa JavaScript em uma thread só, mas `await` devolve o controle ao event loop: entre o `await lerTodos()` e o `await salvarTodos()` outra requisição roda inteirinha. Concorrência não é paralelismo.
2. A solução mais simples é uma fila de promessas: guarde a última operação em uma variável e encadeie a próxima com `fila = fila.then(() => operacao())`. Assim, cada escrita só começa quando a anterior terminou.
3. Exponha uma função `atualizarComExclusividade(transformar)` no repositório, que recebe uma função `(lista) => novaLista`, e faça `criar`, `atualizar` e `remover` passarem por ela.
4. Para o script de estresse, `Array.from({ length: 50 }, (valor, i) => fetch(url, opcoes(i)))` dentro de `Promise.all` basta; conte o resultado com `fs.readFile` depois de todas as respostas chegarem.
5. Meça também o tempo total: a fila serializa as escritas e isso custa. Vale a pena discutir no README se o custo compensa.
</details>

## 🐛 Erros comuns e como resolver

| Sintoma | Causa | Solução |
|---|---|---|
| `Cannot find module '../data/produtos'` ao subir o servidor | Sobrou um `require('../data/produtos')` apontando para o arquivo apagado | Trocar por `require('../data/repositorio')` e usar `await repositorio.lerTodos()` |
| `TypeError: Cannot read properties of undefined (reading 'nome')` no `POST` | `express.json()` ausente ou depois do router: `req.body` é `undefined` | Manter `app.use(express.json())` antes de `app.use('/api/produtos', ...)` |
| `GET /api/produtos/destaques` devolve `400` | `router.get('/:id')` foi registrado antes da rota fixa e casou primeiro | Mover as rotas fixas para antes das rotas com parâmetro |
| `SyntaxError: Unexpected end of JSON input` ao ler o arquivo | `produtos.json` vazio ou gravado pela metade em uma queda anterior | Repor `[]` no arquivo e gravar sempre via arquivo temporário + `rename` |
| `Error: ENOENT: no such file or directory, open 'data/produtos.json'` | Caminho relativo ao diretório de execução, não ao do módulo | Usar `path.join(__dirname, 'produtos.json')` no repositório |
| Produto criado some ao reiniciar o servidor | Faltou o `await repositorio.salvarTodos(lista)` depois do `push` | Toda escrita termina gravando; conferir no `data/produtos.json` |
| `PUT` devolve `200` mas o produto não muda | O corpo veio sem `Content-Type: application/json`, então `req.body` ficou vazio | Incluir o cabeçalho no `testes.http` e no `fetch` do front |
| Resposta `404` chega como página HTML, não como JSON | A requisição caiu no `express.static` ou no 404 padrão do Express | Conferir se `app.all('/api/{*splat}', ...)` está registrado depois dos routers |
| `Route.get() requires a callback function but got a [object Undefined]` | Nome exportado no controlador diferente do usado na rota (`exports.listar` × `controlador.listarTudo`) | Conferir a grafia dos dois lados; `module.exports` do controlador é o objeto `exports` |

## 🏠 Atividade assíncrona (1 h)

No **seu projeto autoral**, refatore a API para a arquitetura de hoje e complete o CRUD:

1. Separe `routes/`, `controllers/` e `data/repositorio.js`, deixando o arquivo de rotas com uma linha por endpoint.
2. Implemente os cinco endpoints do seu recurso principal com os status corretos (`200`, `201`, `204`, `400`, `404`).
3. Persista em arquivo JSON com `fs/promises`, tratando `ENOENT` e gravando por arquivo temporário + `rename`.
4. Implemente busca e filtro por query string no `listar`, com normalização de acentos.
5. Atualize o `testes.http` com o roteiro completo (criar → listar → atualizar → detalhar → excluir → detalhar), incluindo pelo menos dois casos de erro.

**Critério de pronto:** clonando o repositório em uma pasta limpa, `npm install && npm run dev` sobe a API; os 13 blocos equivalentes do seu `testes.http` devolvem os status esperados; e um produto criado continua existindo depois de reiniciar o servidor.

**Entrega:** commit + push e link do repositório no SIGAA.

## ✅ Checkpoint do projeto

- [ ] `routes/` contém apenas o mapeamento método + caminho → função do controlador.
- [ ] `controllers/` contém a lógica de cada operação, sem nenhuma referência a `fs` ou a caminhos de arquivo.
- [ ] `data/repositorio.js` é o único lugar que sabe onde os dados moram, e não menciona HTTP.
- [ ] Os cinco endpoints REST respondem com os status corretos, inclusive nos casos de erro.
- [ ] `POST` inválido devolve `400` com a lista de campos em `detalhes`.
- [ ] `GET /api/produtos?q=&categoria=&ordenar=` filtra, busca e ordena no servidor.
- [ ] Os dados sobrevivem ao reinício do servidor (confira abrindo `data/produtos.json`).
- [ ] `testes.http` versionado, com o roteiro completo e os casos de erro.
- [ ] `README.md` com a tabela de contrato da API.

## 📚 Para aprofundar

- [Express — Routing](https://expressjs.com/pt-br/guide/routing.html) — parâmetros de rota, ordem de avaliação e a sintaxe de curinga do Express 5.
- [MDN — Métodos de requisição HTTP](https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Methods) — leia as páginas de `PUT`, `PATCH` e `DELETE` e compare com o que implementamos.
- [MDN — Códigos de status de respostas HTTP](https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Status) — a referência para consultar sempre que a dúvida for "qual número devolver".
- [MDN — Express Tutorial parte 4: rotas e controladores](https://developer.mozilla.org/pt-BR/docs/Learn/Server-side/Express_Nodejs/routes) — a mesma separação de hoje, com outro exemplo.
- [Node.js — File system (`fs/promises`)](https://nodejs.org/api/fs.html#promises-api) — procure `readFile`, `writeFile` e `rename`.
- [MDN — `String.prototype.normalize()`](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Global_Objects/String/normalize) — as formas NFC e NFD por trás da busca sem acento.
- QUEIRÓS, Ricardo; PORTELA, Filipe. *Introdução ao Desenvolvimento Moderno para a Web*. FCA, 2018 — capítulo sobre APIs REST.
- LOUDON, Kyle. *Desenvolvimento de Grandes Aplicações Web*. Novatec, 2019 — organização em camadas e lógica de negócio.
- ALVES, William P. *Projetos de Sistemas Web*. Érica, 2015 — modelagem das operações de um sistema.

Sua API já faz tudo — e é exatamente esse o problema: qualquer pessoa com um terminal pode excluir o cardápio inteiro. Na próxima aula você resolve a pergunta que toda aplicação real precisa responder antes de ir ao ar: **quem está fazendo esta requisição?** Vamos delegar o login ao Google, verificar o token no servidor e proteger as rotas de escrita. Crie antes da aula uma conta no Google Cloud Console com o seu Gmail — isso poupa quinze minutos da prática.
