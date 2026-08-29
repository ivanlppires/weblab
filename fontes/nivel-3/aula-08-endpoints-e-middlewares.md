# Aula 08 — Definindo endpoints e middlewares

> **Nível 3 — Frameworks Modernos** · Unidade 3: Integração front-end/back-end
> WebLab · UNEMAT Sinop · Prof. Ivan Luiz Pedroso Pires

Na Aula 07 você criou a `unieventos-api` com Express 5, duas rotas `GET` em memória, CORS habilitado, e conectou o front-end real a ela. Hoje essa API vira um CRUD completo, ganha middlewares próprios e validação de entrada — e você recebe as instruções da **Avaliação 2**, com entrega até hoje às 23h59.

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- projetar endpoints REST coerentes: recursos no plural, verbos HTTP corretos, status codes apropriados por operação;
- implementar um CRUD completo (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`) com Express 5, modularizado em `express.Router()`;
- escrever middlewares próprios — logger, medidor de tempo, validador, tratador de 404 e tratador de erros centralizado — entendendo a ordem de execução da cadeia;
- explicar a diferença entre middleware de aplicação, de rota e de erro, e por que este último precisa vir por último;
- validar corpos de requisição com `zod`, devolvendo `422` com mensagens em português;
- entender por que `throw` dentro de um handler `async` do Express 5 cai automaticamente no tratador de erros;
- organizar testes manuais num arquivo `requests.http` cobrindo todos os endpoints.

## 📋 Pré-requisitos desta aula

- [ ] `unieventos-api` da Aula 07 rodando, com `GET /api/eventos` e `GET /api/eventos/:id` funcionando em memória.
- [ ] Front-end `unieventos-web` apontando para essa API via `baseURL` do Axios.
- [ ] Entendimento de `async`/`await` e por que erros em handlers `async` do Express 5 são capturados automaticamente (Aula 07).
- [ ] Projeto autoral com API própria (`<seu-projeto>-api`) criada na atividade assíncrona da Aula 07.

> **⚠️ Atenção**
> Esta é a aula da **Avaliação 2**. Leia a seção "📝 Avaliação 2 — instruções de entrega" logo no início do período de aula, para planejar seu tempo — o prazo de entrega é hoje, 07/10/2026, às 23h59.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | REST na prática: recursos, verbos, status codes, formato de resposta, paginação e filtros |
| 2 | 50 min | CRUD completo com `express.Router()`; middlewares próprios e de terceiros; tratador de erros central |
| 3 | 50 min | Validação com `zod`; `requests.http` completo; instruções da Avaliação 2 |

## 1. REST na prática

Você já usa APIs "estilo REST" desde a Aula 06, mas hoje é você quem projeta os endpoints. REST não é um protocolo com regras fixadas em pedra — é um conjunto de convenções que, seguidas com consistência, tornam uma API previsível para quem consome.

O nome vem de *Representational State Transfer* — a ideia central é que cada recurso do seu domínio (um evento, um usuário, uma inscrição) tem uma **representação** (o JSON que a API devolve) e um **endereço próprio** (a URL). O cliente manipula o estado do sistema transferindo representações desse recurso para lá e para cá, usando os verbos HTTP para expressar a intenção. Você não precisa decorar a definição formal — o que importa na prática são as convenções que seguem daqui.

Por que seguir convenção importa: quando toda API do mercado usa `GET` para ler e `POST` para criar, qualquer desenvolvedor que chega no seu projeto já sabe, sem ler documentação nenhuma, que `POST /api/v1/eventos` cria um evento. Quebrar essa expectativa (por exemplo, usando `GET /api/deletarEvento?id=3` para apagar algo) obriga quem consome sua API a ler cada linha de código para entender o que uma rota faz — e, pior, faz com que caches e proxies HTTP, que assumem que `GET` nunca tem efeito colateral, possam repetir a chamada e apagar coisas sem querer.

### Recursos: substantivos no plural, sempre

Um endpoint representa um **recurso** — uma entidade do seu domínio — nunca uma ação. O verbo da ação já está no método HTTP, não precisa (e não deve) repetir no caminho.

```text
✅ GET    /api/eventos            (correto: recurso no plural, sem verbo)
❌ GET    /api/buscarEventos       (errado: verbo no caminho)
❌ GET    /api/evento               (errado: singular)

✅ POST   /api/eventos            (criar um evento)
❌ POST   /api/criarEvento          (errado: verbo redundante)

✅ DELETE /api/eventos/3          (remover o evento de id 3)
❌ GET    /api/deletarEvento?id=3  (errado: usa GET para uma ação destrutiva)
```

Sub-recursos seguem o mesmo padrão, aninhando o caminho:

```text
GET /api/eventos/3/inscricoes     (inscrições do evento 3)
POST /api/eventos/3/inscricoes    (inscrever alguém no evento 3)
```

### Verbos HTTP e o que cada um significa neste domínio

| Verbo | Uso no UniEventos | Idempotente? |
|---|---|---|
| `GET` | ler evento(s), sem efeito colateral | sim |
| `POST` | criar um evento novo | não |
| `PUT` | substituir um evento inteiro | sim |
| `PATCH` | atualizar campos específicos de um evento | não, em geral |
| `DELETE` | remover um evento | sim |

**Idempotência** significa: repetir a mesma requisição várias vezes produz o mesmo resultado final que executá-la uma vez. `GET /api/eventos/3` sempre devolve o mesmo evento (até que ele mude por outro motivo) — chamar dez vezes não altera nada. `DELETE /api/eventos/3` é idempotente porque, depois da primeira chamada, o evento já não existe; chamar de novo continua resultando em "evento 3 não existe" (ainda que a segunda chamada responda `404` em vez de `204` — o estado final do sistema é o mesmo). Já `POST /api/eventos` **não** é idempotente: cada chamada cria um evento novo, mesmo enviando o corpo idêntico.

> **📌 Na prova**
> Se a pergunta pedir para classificar um verbo HTTP como idempotente ou não, lembre: `GET`, `PUT`, `DELETE` são idempotentes; `POST` não é. `PATCH` depende de como é implementado, mas normalmente também não é.

### Status codes por operação

| Operação | Status de sucesso | Quando falha |
|---|---|---|
| `GET` (lista ou item existente) | `200 OK` | `404` se o item não existe |
| `POST` (criação) | `201 Created` + cabeçalho `Location` | `422` se a validação falha |
| `PUT`/`PATCH` (atualização) | `200 OK` com o recurso atualizado | `404` se não existe, `422` se inválido |
| `DELETE` (remoção) | `204 No Content`, sem corpo | `404` se já não existe |

O cabeçalho `Location` em uma criação bem-sucedida informa ao cliente onde o novo recurso pode ser lido depois — é uma convenção REST, não uma obrigação técnica, mas boas APIs seguem.

```js
// dentro do handler de criação, depois de gerar o novo evento com id 7
res.status(201).location(`/api/eventos/${novoEvento.id}`).json(novoEvento)
```

> **⚠️ Atenção**
> Lembre da armadilha do Express 5 vista na Aula 07: `res.json(objeto, 201)` **não existe**. A sintaxe correta é sempre `res.status(201).json(objeto)`, com o status vindo antes, encadeado.

### Versionamento

Prefixar rotas com `/api/v1` sinaliza desde o início que a API pode evoluir sem quebrar clientes existentes — quando uma mudança incompatível for necessária, ela nasce em `/api/v2`, e `/v1` continua funcionando para quem ainda depende dele.

```js
app.use('/api/v1/eventos', eventosRoutes)
```

Esta disciplina usa `/api` sem versão explícita nos exemplos anteriores para simplificar, mas a partir de hoje adotamos `/api/v1` na `unieventos-api` — é o padrão que se espera num projeto profissional, e é exigido na Avaliação 2.

### Formato de resposta consistente

Uma API previsível responde sempre no mesmo formato — envelope de sucesso e envelope de erro —, para que o front-end trate qualquer resposta da mesma forma, sem checar caso a caso.

```json
{
  "dados": { "id": 1, "titulo": "Semana Acadêmica de Computação" },
  "meta": { "pagina": 1, "limite": 10, "total": 42 }
}
```

```json
{
  "erro": {
    "mensagem": "Evento não encontrado",
    "codigo": "EVENTO_NAO_ENCONTRADO"
  }
}
```

`dados` carrega o conteúdo (objeto único ou array); `meta` carrega metadados de paginação quando aplicável; `erro` só aparece em respostas de falha, nunca junto com `dados`. Vamos implementar exatamente esse envelope no CRUD desta aula.

O ganho prático aparece no front-end: um interceptor de resposta do Axios (Aula 06) pode, por exemplo, sempre extrair `response.data.dados` automaticamente, ou sempre reconhecer `response.data.erro` para disparar uma notificação padronizada — porque a forma nunca muda, só o conteúdo. Sem esse envelope, cada endpoint devolveria uma "forma" diferente (às vezes um array solto, às vezes um objeto solto, às vezes um objeto com `results`), obrigando o front a tratar cada chamada como um caso especial.

### Paginação, filtros e ordenação por query string

```text
GET /api/v1/eventos?pagina=2&limite=10
GET /api/v1/eventos?categoria=palestra
GET /api/v1/eventos?ordenarPor=dataHora&direcao=asc
```

Paginação evita devolver milhares de registros de uma vez — o cliente pede uma "página" por vez. Filtros restringem o conjunto por algum critério. Ordenação decide a sequência dos resultados. As três são independentes e combináveis na mesma URL. Vamos implementar isso no CRUD abaixo.

## 2. CRUD completo em memória

Vamos reescrever a `unieventos-api` da Aula 07, agora com o CRUD inteiro e o formato de resposta padronizado.

### Dados em memória, com função de próximo id

```js
// src/dados/eventos.js
export const eventos = [
  {
    id: 1,
    titulo: 'Semana Acadêmica de Computação',
    descricao: 'Palestras e minicursos sobre o mercado de tecnologia.',
    categoria: 'palestra',
    dataHora: '2026-10-15T19:00:00',
    local: 'Auditório FACET',
    vagas: 80,
    imagemUrl: 'https://picsum.photos/seed/semana-computacao/400/240',
  },
  {
    id: 2,
    titulo: 'Minicurso de Vue 3',
    descricao: 'Introdução prática ao framework Vue com Composition API.',
    categoria: 'minicurso',
    dataHora: '2026-10-20T14:00:00',
    local: 'Laboratório 3',
    vagas: 30,
    imagemUrl: 'https://picsum.photos/seed/minicurso-vue/400/240',
  },
  {
    id: 3,
    titulo: 'Workshop de Firebase e Express',
    descricao: 'Construindo uma API real do zero.',
    categoria: 'workshop',
    dataHora: '2026-10-28T19:30:00',
    local: 'Laboratório 1',
    vagas: 25,
    imagemUrl: 'https://picsum.photos/seed/workshop-firebase/400/240',
  },
]

// gera o próximo id disponível — em memória; na Aula 09 o próprio banco faz isso
export function proximoId() {
  const maiorId = eventos.reduce((max, e) => Math.max(max, e.id), 0)
  return maiorId + 1
}
```

### Classe de erro HTTP customizada

Antes de escrever as rotas, criamos uma classe de erro que carrega o status HTTP junto da mensagem — assim qualquer parte do código pode `throw` um erro que já sabe se traduzir em resposta.

```js
// src/erros/ErroHttp.js
export class ErroHttp extends Error {
  constructor(status, mensagem, codigo = 'ERRO') {
    super(mensagem)
    this.name = 'ErroHttp'
    this.status = status
    this.codigo = codigo
  }
}

// atalhos comuns, para não repetir "new ErroHttp(404, ...)" em todo lugar
export function erroNaoEncontrado(mensagem = 'Recurso não encontrado') {
  return new ErroHttp(404, mensagem, 'NAO_ENCONTRADO')
}

export function erroValidacao(mensagem = 'Dados inválidos') {
  return new ErroHttp(422, mensagem, 'VALIDACAO')
}
```

### Rotas modularizadas com `express.Router()`

Até a Aula 07, as rotas viviam direto em `src/servidor.js`, registradas com `app.get(...)`. Isso funciona para duas rotas; não escala para uma API com vários recursos, cada um com seu CRUD completo. `express.Router()` cria um "mini aplicativo Express" — um objeto que aceita `.get()`, `.post()`, `.put()`, `.patch()`, `.delete()` exatamente como `app`, mas que fica isolado num arquivo próprio, sem saber em qual prefixo vai ser montado.

Repare que dentro do arquivo de rotas os caminhos são **relativos**: `router.get('/')` e `router.get('/:id')`, sem repetir `/api/v1/eventos`. É só na hora de montar, em `servidor.js`, que o prefixo é definido:

```js
app.use('/api/v1/eventos', eventosRoutes)
```

Isso significa que, se amanhã você decidir que a API deve responder em `/api/v2/eventos` também, basta montar o mesmo `eventosRoutes` num segundo prefixo — nenhuma rota interna precisa mudar.

```js
// src/routes/eventos.routes.js
import { Router } from 'express'
import { eventos, proximoId } from '../dados/eventos.js'
import { erroNaoEncontrado, erroValidacao } from '../erros/ErroHttp.js'

const router = Router()

// função auxiliar: encontra o índice do evento pelo id, ou -1
function indiceDoEvento(id) {
  return eventos.findIndex((e) => e.id === id)
}

// GET /api/v1/eventos — lista com filtro, ordenação e paginação
router.get('/', (req, res) => {
  let resultado = [...eventos]

  // filtro por categoria
  if (req.query.categoria) {
    resultado = resultado.filter((e) => e.categoria === req.query.categoria)
  }

  // ordenação
  const ordenarPor = req.query.ordenarPor || 'id'
  const direcao = req.query.direcao === 'desc' ? -1 : 1
  resultado.sort((a, b) => {
    if (a[ordenarPor] < b[ordenarPor]) return -1 * direcao
    if (a[ordenarPor] > b[ordenarPor]) return 1 * direcao
    return 0
  })

  // paginação
  const pagina = Number(req.query.pagina) || 1
  const limite = Number(req.query.limite) || 10
  const inicio = (pagina - 1) * limite
  const pagina_de_resultados = resultado.slice(inicio, inicio + limite)

  res.json({
    dados: pagina_de_resultados,
    meta: { pagina, limite, total: resultado.length },
  })
})

// GET /api/v1/eventos/:id — busca um evento específico
router.get('/:id', (req, res) => {
  const id = Number(req.params.id)
  const evento = eventos.find((e) => e.id === id)

  if (!evento) {
    throw erroNaoEncontrado('Evento não encontrado')
  }

  res.json({ dados: evento })
})

// POST /api/v1/eventos — cria um evento novo
router.post('/', (req, res) => {
  const corpo = req.body

  if (!corpo || !corpo.titulo || !corpo.categoria) {
    throw erroValidacao('Campos "titulo" e "categoria" são obrigatórios')
  }

  const novoEvento = {
    id: proximoId(),
    titulo: corpo.titulo,
    descricao: corpo.descricao || '',
    categoria: corpo.categoria,
    dataHora: corpo.dataHora || null,
    local: corpo.local || '',
    vagas: Number(corpo.vagas) || 0,
    imagemUrl: corpo.imagemUrl || '',
  }

  eventos.push(novoEvento)

  res
    .status(201)
    .location(`/api/v1/eventos/${novoEvento.id}`)
    .json({ dados: novoEvento })
})

// PUT /api/v1/eventos/:id — substitui o evento inteiro
router.put('/:id', (req, res) => {
  const id = Number(req.params.id)
  const indice = indiceDoEvento(id)

  if (indice === -1) {
    throw erroNaoEncontrado('Evento não encontrado')
  }

  const corpo = req.body
  if (!corpo || !corpo.titulo || !corpo.categoria) {
    throw erroValidacao('Campos "titulo" e "categoria" são obrigatórios')
  }

  eventos[indice] = {
    id,
    titulo: corpo.titulo,
    descricao: corpo.descricao || '',
    categoria: corpo.categoria,
    dataHora: corpo.dataHora || null,
    local: corpo.local || '',
    vagas: Number(corpo.vagas) || 0,
    imagemUrl: corpo.imagemUrl || '',
  }

  res.json({ dados: eventos[indice] })
})

// PATCH /api/v1/eventos/:id — atualiza campos específicos
router.patch('/:id', (req, res) => {
  const id = Number(req.params.id)
  const indice = indiceDoEvento(id)

  if (indice === -1) {
    throw erroNaoEncontrado('Evento não encontrado')
  }

  // mescla só os campos enviados — PATCH é parcial, diferente de PUT
  eventos[indice] = { ...eventos[indice], ...req.body }

  res.json({ dados: eventos[indice] })
})

// DELETE /api/v1/eventos/:id — remove o evento
router.delete('/:id', (req, res) => {
  const id = Number(req.params.id)
  const indice = indiceDoEvento(id)

  if (indice === -1) {
    throw erroNaoEncontrado('Evento não encontrado')
  }

  eventos.splice(indice, 1)

  res.status(204).send()
})

export default router
```

> **⚠️ Atenção**
> Note `router.delete(...)`, não `router.del(...)`. `app.del`/`router.del` foram removidos no Express 5 (Aula 07, §5).

### Montando o Router no servidor

```js
// src/servidor.js
import express from 'express'
import cors from 'cors'
import eventosRoutes from './routes/eventos.routes.js'
import { middlewareNaoEncontrado, tratadorDeErros } from './middlewares/erros.js'
import { logger } from './middlewares/logger.js'
import { medidorDeTempo } from './middlewares/medidorDeTempo.js'

const app = express()

app.use(cors())
app.use(express.json())
app.use(logger)
app.use(medidorDeTempo)

// monta o router em /api/v1/eventos — dentro do router, as rotas usam caminhos relativos
app.use('/api/v1/eventos', eventosRoutes)

// a partir daqui, nenhuma rota casou: 404
app.use(middlewareNaoEncontrado)

// tratador de erros SEMPRE por último
app.use(tratadorDeErros)

const porta = process.env.PORTA || 3000

app.listen(porta, () => {
  console.log(`unieventos-api rodando em http://localhost:${porta}`)
})
```

Modularizar com `express.Router()` separa a definição das rotas de eventos do arquivo principal do servidor. Isso escala: cada recurso (`eventos`, e futuramente `inscricoes`, `usuarios`) ganha seu próprio arquivo de rotas, e `servidor.js` só monta cada um em seu prefixo.

## 🧩 Padrão de projeto em uso

> ### 🧩 Padrão de projeto em uso — Chain of Responsibility e Strategy
>
> A cadeia `cors → express.json → logger → medidorDeTempo → eventosRoutes → middlewareNaoEncontrado → tratadorDeErros` é o **Chain of Responsibility** completo: cada middleware decide se processa a requisição e a passa adiante com `next()`, ou se responde e encerra a cadeia ali. A ordem importa — é o próprio desenho do padrão: cada elo só recebe a requisição se o anterior decidiu repassá-la.
>
> Já os validadores de corpo que vamos construir com `zod` ilustram o **Strategy** (comportamental): a função `validar(schema)` é genérica — ela não sabe nada sobre "evento" —, e recebe de fora, como parâmetro, a estratégia de validação específica (o schema Zod do evento, do usuário, do que for). Trocar a validação de uma rota é só trocar o schema passado, sem tocar no middleware `validar`. Isso é Strategy: o algoritmo (validação) é injetado, intercambiável, sem alterar quem o usa.

## 3. Middlewares a fundo

Um middleware é uma função com a assinatura `(req, res, next)` — ou `(err, req, res, next)` no caso especial de tratador de erros, com **quatro** argumentos. Ele roda entre a chegada da requisição e a resposta final, podendo:

- ler ou modificar `req`/`res`;
- encerrar o ciclo respondendo diretamente (`res.send()`, `res.json()`, etc.);
- passar a bola adiante chamando `next()`;
- passar um erro adiante chamando `next(erro)` (embora no Express 5, como vimos, um `throw` dentro de um handler `async` já faz isso sozinho).

Pense em cada middleware como uma estação de inspeção numa linha de produção. A requisição entra por um lado, passa estação por estação, e cada uma pode carimbá-la (adicionar algo a `req`), rejeitá-la ali mesmo (responder e nunca chamar `next()`) ou deixá-la seguir para a próxima estação. Uma rota (`router.get`, `router.post`, etc.) é só a última estação da linha — a que finalmente produz uma resposta para o cliente, na maioria das requisições.

### Ordem de execução

Middlewares rodam **na ordem em que são registrados** com `app.use()` ou dentro de uma rota. Se um middleware não chamar `next()` nem responder, a requisição fica pendurada para sempre — esse é o erro mais comum ao escrever middleware pela primeira vez.

```js
app.use(cors())           // 1º: libera CORS
app.use(express.json())   // 2º: faz o parse do corpo
app.use(logger)           // 3º: registra a requisição no console
app.use(medidorDeTempo)   // 4º: começa a medir o tempo de resposta
app.use('/api/v1/eventos', eventosRoutes)  // 5º: tenta casar com alguma rota de evento
app.use(middlewareNaoEncontrado)  // 6º: só roda se nada casou acima
app.use(tratadorDeErros)          // 7º: só roda se algo lançou erro em qualquer ponto anterior
```

### Middleware de aplicação × de rota × de erro

**Middleware de aplicação** roda para toda requisição, registrado direto em `app.use(fn)`, sem caminho — é o caso de `cors()`, `express.json()`, `logger`.

**Middleware de rota** roda só para requisições que casam com um caminho e método específicos, registrado como argumento extra antes do handler final:

```js
// middleware de rota: só roda para POST /api/v1/eventos
router.post('/', validar(schemaEvento), (req, res) => {
  // aqui req.body já passou pela validação
})
```

**Middleware de erro** tem **quatro** parâmetros — `(err, req, res, next)` — e o Express o reconhece pela aridade da função (contagem de parâmetros), não por onde está registrado. Ele só é chamado quando algum middleware ou handler anterior invoca `next(erro)` ou lança uma exceção (capturada automaticamente em handlers `async`, como vimos).

### Por que o tratador de erros vem por último

O Express testa os middlewares registrados na ordem em que aparecem. Um middleware de erro só é alcançado quando a cadeia "pula" para ele — o que acontece quando algo dá errado em qualquer ponto anterior. Se você registrar o tratador de erros **antes** de uma rota, ele nunca vai capturar os erros dela, porque a execução normal (sem erro) nem chega a considerá-lo — e mesmo em caso de erro, o Express busca o próximo middleware de erro **à frente** na cadeia, nunca voltando para trás. Por isso a regra é fixa: middlewares normais primeiro, depois o 404 (que captura tudo que não casou com nenhuma rota), depois o tratador de erros por último de todos.

```text
requisição
    │
    ▼
  cors() ──────────────► ok, next()
    │
    ▼
  express.json() ──────► ok, next()
    │
    ▼
  eventosRoutes ───────► lançou erro (throw)
    │                         │
    │            Express pula direto para o
    │            próximo middleware DE ERRO
    │                         │
    ▼                         ▼
  middlewareNaoEncontrado   tratadorDeErros
  (não roda: já tinha        (roda: recebe o erro,
   uma rota que casou)        responde ao cliente)
```

Se `middlewareNaoEncontrado` estivesse depois de `tratadorDeErros`, ele nunca seria alcançado no caminho de erro — e se estivesse antes das rotas, capturaria toda requisição como "não encontrada", mesmo as que tinham rota válida. A ordem — rotas, depois 404, depois tratador de erros — não é estilo, é a única ordem que faz os três cumprirem seu papel corretamente.

### Escrevendo os middlewares do zero

```js
// src/middlewares/logger.js
// registra método, caminho e horário de cada requisição recebida
export function logger(req, res, next) {
  const agora = new Date().toISOString()
  console.log(`[${agora}] ${req.method} ${req.originalUrl}`)
  next()
}
```

```js
// src/middlewares/medidorDeTempo.js
// mede quanto tempo o servidor levou para responder, em milissegundos
export function medidorDeTempo(req, res, next) {
  const inicio = process.hrtime.bigint()

  // 'finish' dispara quando a resposta terminou de ser enviada
  res.on('finish', () => {
    const fim = process.hrtime.bigint()
    const duracaoMs = Number(fim - inicio) / 1_000_000
    console.log(`  ↳ ${res.statusCode} em ${duracaoMs.toFixed(1)}ms`)
  })

  next()
}
```

```js
// src/middlewares/erros.js
import { ErroHttp } from '../erros/ErroHttp.js'

// roda quando nenhuma rota casou com a requisição — precisa vir depois de todas as rotas
export function middlewareNaoEncontrado(req, res, next) {
  next(new ErroHttp(404, `Rota ${req.method} ${req.originalUrl} não existe`, 'ROTA_NAO_ENCONTRADA'))
}

// tratador de erros central — repare nos QUATRO parâmetros, é assim que o Express o reconhece
export function tratadorDeErros(err, req, res, next) {
  // erros conhecidos (ErroHttp) já sabem seu status; erros inesperados viram 500
  const status = err instanceof ErroHttp ? err.status : 500
  const codigo = err instanceof ErroHttp ? err.codigo : 'ERRO_INTERNO'
  const mensagem = err instanceof ErroHttp ? err.message : 'Erro interno do servidor'

  if (status === 500) {
    // erro inesperado: registre o stack completo no servidor, mas não exponha ao cliente
    console.error(err)
  }

  res.status(status).json({ erro: { mensagem, codigo } })
}
```

```js
// src/middlewares/validador.js
export function validar(schema) {
  // retorna um middleware de rota configurado para o schema recebido — isto é Strategy
  return (req, res, next) => {
    const resultado = schema.safeParse(req.body)

    if (!resultado.success) {
      const mensagens = resultado.error.issues.map((problema) => problema.message)
      return res.status(422).json({
        erro: { mensagem: 'Dados inválidos', codigo: 'VALIDACAO', detalhes: mensagens },
      })
    }

    // substitui req.body pelos dados já validados e tipados pelo Zod
    req.body = resultado.data
    next()
  }
}
```

### Middlewares de terceiros

```bash
npm install morgan helmet express-rate-limit compression
```

```js
// src/servidor.js (trecho adicional)
import morgan from 'morgan'
import helmet from 'helmet'
import rateLimit from 'express-rate-limit'
import compression from 'compression'

app.use(helmet())            // cabeçalhos de segurança padrão (evita alguns ataques comuns)
app.use(compression())       // comprime respostas grandes (gzip) — mais rápido para o cliente
app.use(morgan('dev'))       // log de requisições formatado — mais completo que nosso logger

const limitador = rateLimit({
  windowMs: 15 * 60 * 1000,  // janela de 15 minutos
  max: 100,                   // no máximo 100 requisições por IP nessa janela
  message: { erro: { mensagem: 'Muitas requisições, tente novamente mais tarde', codigo: 'RATE_LIMIT' } },
})
app.use('/api/', limitador)  // aplica o limite só nas rotas de API
```

| Pacote | Para que serve |
|---|---|
| `cors` | libera requisições de outras origens (front em outra porta/domínio) |
| `morgan` | log de requisições HTTP formatado (substitui nosso `logger` em produção) |
| `helmet` | adiciona cabeçalhos HTTP de segurança (proteção básica contra alguns ataques) |
| `express-rate-limit` | limita quantas requisições um IP pode fazer numa janela de tempo |
| `compression` | comprime o corpo das respostas (gzip), reduzindo tráfego |

> **💡 Dica**
> `morgan('dev')` e nosso `logger`/`medidorDeTempo` fazem trabalho parecido. Escrever o seu próprio primeiro é pedagógico — mostra o que acontece por baixo —, mas em projetos reais é comum usar só `morgan`, já testado e configurável.

## 4. Async no Express 5, revisitado

Na Aula 07 você viu que `throw` dentro de um handler `async` cai automaticamente no tratador de erros — e testou isso no laboratório com a rota `/api/quebra`. Agora, com um tratador de erros de verdade escrito, o comportamento fica completo:

```js
// Express 5: qualquer throw, síncrono ou dentro de um await, é capturado
router.get('/:id', async (req, res) => {
  const evento = await buscarEventoPorIdNoBanco(req.params.id)  // função hipotética assíncrona
  if (!evento) {
    throw erroNaoEncontrado('Evento não encontrado')
  }
  res.json({ dados: evento })
})
```

Se `buscarEventoPorIdNoBanco` rejeitasse a Promise (por exemplo, uma falha de conexão), o Express 5 também capturaria automaticamente e encaminharia para `tratadorDeErros`. Nenhum `try/catch` manual é necessário para isso — o framework embrulha cada handler `async` internamente.

**Por que tanto código por aí usa `express-async-handler` então?** Porque esse pacote foi criado para o Express 4, que **não** tinha essa captura automática — era preciso embrulhar manualmente cada handler assíncrono:

```js
// Express 4 (não use): precisava embrulhar manualmente
// const asyncHandler = require('express-async-handler')
// router.get('/:id', asyncHandler(async (req, res) => { ... }))
```

No Express 5, esse pacote é desnecessário. Se você encontrar em um projeto ou tutorial, é sinal de código escrito para Express 4 (ou copiado de um).

> **📌 Na prova**
> Se perguntarem por que `express-async-handler` não é mais necessário no Express 5, a resposta é: o próprio framework agora captura automaticamente qualquer exceção lançada (ou Promise rejeitada) dentro de um handler `async`, encaminhando para o middleware de erro — antes isso exigia embrulhar manualmente.

## 💻 Mão na massa — validação com Zod e testes organizados

### Passo 1 — instalar e escrever o schema

```bash
npm install zod
```

```js
// src/schemas/evento.schema.js
import { z } from 'zod'

export const schemaEvento = z.object({
  titulo: z.string().min(3, 'O título precisa ter ao menos 3 caracteres'),
  descricao: z.string().optional(),
  categoria: z.enum(['palestra', 'minicurso', 'workshop'], {
    message: 'Categoria deve ser palestra, minicurso ou workshop',
  }),
  dataHora: z.string().min(1, 'Informe a data e hora do evento'),
  local: z.string().min(1, 'Informe o local do evento'),
  vagas: z.number({ message: 'Vagas deve ser um número' }).int().positive('Vagas deve ser maior que zero'),
  imagemUrl: z.string().url('URL de imagem inválida').optional().or(z.literal('')),
})

// schema para PATCH: os mesmos campos, mas todos opcionais
export const schemaEventoParcial = schemaEvento.partial()
```

### Passo 2 — aplicar o middleware `validar` nas rotas

```js
// src/routes/eventos.routes.js (trechos alterados)
import { Router } from 'express'
import { eventos, proximoId } from '../dados/eventos.js'
import { erroNaoEncontrado } from '../erros/ErroHttp.js'
import { validar } from '../middlewares/validador.js'
import { schemaEvento, schemaEventoParcial } from '../schemas/evento.schema.js'

const router = Router()

// ...rotas GET permanecem como antes...

router.post('/', validar(schemaEvento), (req, res) => {
  // req.body já chega validado e com os tipos corretos (vagas já é number, por exemplo)
  const novoEvento = { id: proximoId(), ...req.body }
  eventos.push(novoEvento)
  res.status(201).location(`/api/v1/eventos/${novoEvento.id}`).json({ dados: novoEvento })
})

router.put('/:id', validar(schemaEvento), (req, res) => {
  const id = Number(req.params.id)
  const indice = eventos.findIndex((e) => e.id === id)
  if (indice === -1) throw erroNaoEncontrado('Evento não encontrado')

  eventos[indice] = { id, ...req.body }
  res.json({ dados: eventos[indice] })
})

router.patch('/:id', validar(schemaEventoParcial), (req, res) => {
  const id = Number(req.params.id)
  const indice = eventos.findIndex((e) => e.id === id)
  if (indice === -1) throw erroNaoEncontrado('Evento não encontrado')

  eventos[indice] = { ...eventos[indice], ...req.body }
  res.json({ dados: eventos[indice] })
})

export default router
```

Com `validar(schemaEvento)` na frente do handler, o corpo malformado nunca chega a ser processado pela lógica de negócio — a validação já respondeu `422` e encerrou a cadeia antes disso.

### Passo 3 — `requests.http` completo

```http
### requests.http — todos os endpoints da unieventos-api

@baseUrl = http://localhost:3000/api/v1

### listar eventos (com paginação, filtro e ordenação)
GET {{baseUrl}}/eventos?pagina=1&limite=10&categoria=palestra&ordenarPor=dataHora&direcao=asc

### buscar evento por id
GET {{baseUrl}}/eventos/1

### buscar evento inexistente (espera 404)
GET {{baseUrl}}/eventos/999

### criar evento válido (espera 201 + Location)
POST {{baseUrl}}/eventos
Content-Type: application/json

{
  "titulo": "Palestra de Segurança da Informação",
  "categoria": "palestra",
  "dataHora": "2026-11-05T19:00:00",
  "local": "Auditório FACET",
  "vagas": 60
}

### criar evento inválido (espera 422)
POST {{baseUrl}}/eventos
Content-Type: application/json

{
  "titulo": "AB",
  "categoria": "show"
}

### substituir evento inteiro (espera 200)
PUT {{baseUrl}}/eventos/1
Content-Type: application/json

{
  "titulo": "Semana Acadêmica de Computação — atualizada",
  "categoria": "palestra",
  "dataHora": "2026-10-16T19:00:00",
  "local": "Auditório FACET",
  "vagas": 100
}

### atualizar parcialmente (espera 200)
PATCH {{baseUrl}}/eventos/2
Content-Type: application/json

{
  "vagas": 25
}

### remover evento (espera 204)
DELETE {{baseUrl}}/eventos/3

### remover evento já removido (espera 404)
DELETE {{baseUrl}}/eventos/3

### rota inexistente (espera 404 do middlewareNaoEncontrado)
GET {{baseUrl}}/qualquer-coisa
```

> **💡 Dica**
> A variável `@baseUrl` no topo do arquivo evita repetir `http://localhost:3000/api/v1` em toda linha — troque só ali quando mudar de ambiente (local, homologação, produção).

## 🧪 Laboratório

**1. Endpoint de contagem por categoria.** Crie `GET /api/v1/eventos/estatisticas/por-categoria` que devolve `{ "dados": { "palestra": 2, "minicurso": 1, "workshop": 1 } }`, contando quantos eventos existem em cada categoria.

<details markdown="1">
<summary>Dica</summary>

Cuidado com a ordem: registre essa rota **antes** de `router.get('/:id', ...)`, senão o Express interpreta `estatisticas` como um valor de `:id`.
</details>

**2. Middleware de log condicional.** Modifique o `logger` para só imprimir requisições cujo método seja `POST`, `PUT`, `PATCH` ou `DELETE` (as que alteram dados) — omita `GET`.

<details markdown="1">
<summary>Dica</summary>

Um `if (req.method !== 'GET') { ... }` dentro do middleware, antes de chamar `next()`.
</details>

**3. Erro de validação com múltiplos campos.** Envie, pelo `requests.http`, um `POST /api/v1/eventos` com `titulo` vazio **e** `categoria` inválida ao mesmo tempo. Confirme que a resposta `422` lista as duas mensagens de erro no array `detalhes`.

<details markdown="1">
<summary>Dica</summary>

O Zod, por padrão, coleta **todos** os problemas antes de falhar — não para no primeiro. `resultado.error.issues` é um array com um item por campo problemático.
</details>

**4. Rate limit em ação.** Reduza temporariamente o `max` do `express-rate-limit` para `5` e a `windowMs` para `60000` (1 minuto). Dispare mais de 5 requisições seguidas com `curl` num loop e observe a resposta `429 Too Many Requests`. Depois volte os valores originais.

<details markdown="1">
<summary>Dica</summary>

```bash
for i in 1 2 3 4 5 6 7; do curl -s -o /dev/null -w "%{http_code}\n" http://localhost:3000/api/v1/eventos; done
```
</details>

**5. PATCH que tenta mudar o id.** Envie `PATCH /api/v1/eventos/1` com corpo `{ "id": 999 }`. Verifique o que acontece com o registro em memória. Corrija o handler para ignorar qualquer `id` enviado no corpo (o id da URL é sempre a fonte da verdade).

<details markdown="1">
<summary>Dica</summary>

Depois do merge (`{ ...eventos[indice], ...req.body }`), force `eventos[indice].id = id` (o id da URL, já convertido para número) por cima, sobrescrevendo qualquer valor vindo do corpo.
</details>

**6. Middleware de erro específico para JSON malformado.** Envie, via `curl`, um `POST /api/v1/eventos` com corpo JSON propositalmente quebrado (ex.: `{"titulo": "teste",}` com vírgula sobrando). Observe qual status volta. `express.json()` lança um erro de parsing antes mesmo de sua rota rodar — confirme que esse erro também é capturado pelo seu `tratadorDeErros`, e ajuste a mensagem para ficar amigável ("corpo da requisição não é um JSON válido") quando o erro vier do parser.

<details markdown="1">
<summary>Dica</summary>

O erro lançado pelo `express.json()` tem `err.type === 'entity.parse.failed'`. No `tratadorDeErros`, adicione uma verificação extra antes da checagem de `ErroHttp`: `if (err.type === 'entity.parse.failed') { return res.status(400).json({ erro: { mensagem: 'JSON inválido no corpo da requisição', codigo: 'JSON_INVALIDO' } }) }`.
</details>

## 🐛 Erros comuns e como resolver

| Sintoma | Causa | Solução |
|---|---|---|
| `GET /eventos/estatisticas` cai no handler de `/:id` | rota com parâmetro dinâmico registrada antes da rota fixa | registre rotas fixas (`/estatisticas/...`) antes de rotas com `:id` |
| Middleware "trava" a requisição, sem resposta nem erro | esqueceu de chamar `next()` dentro do middleware | toda função de middleware precisa terminar chamando `next()` **ou** respondendo diretamente |
| Tratador de erros nunca é chamado | ele foi registrado antes das rotas, ou tem menos de 4 parâmetros | mova `app.use(tratadorDeErros)` para o fim; confira a assinatura `(err, req, res, next)` |
| `422` não aparece, servidor retorna `500` | schema Zod não corresponde ao formato de `req.body`, gerando erro diferente do esperado | confira o schema campo a campo; teste isoladamente com `schema.safeParse(objetoDeTeste)` |
| `POST` retorna `201` mas sem `Location` no cabeçalho | esqueceu `.location(...)` antes de `.json(...)` | encadeie `res.status(201).location(url).json(dados)` |
| `express-rate-limit` bloqueia até requisições legítimas em sala | `max` configurado baixo demais para uma turma toda testando do mesmo IP/rede | aumente `max` durante a aula, ou aplique o limitador só em rotas de escrita |
| `zod`: erro `Cannot read properties of undefined (reading 'issues')` | `schema.safeParse` não foi usado (usou `schema.parse`, que lança exceção em vez de devolver objeto) | use sempre `safeParse` no middleware `validar`, para tratar o erro manualmente |
| `DELETE` retorna `204` mas o corpo aparece vazio "errado" no REST Client | comportamento esperado — `204 No Content` nunca deve ter corpo | confirme com `res.status(204).send()` sem argumento; não chame `.json()` depois de `204` |
| Duas rotas parecem casar com a mesma URL, só a primeira responde | ordem de registro determina qual middleware/rota atende primeiro | reordene: rotas mais específicas antes das mais genéricas |
| Front-end para de funcionar depois de adicionar `helmet()` | `helmet` por padrão bloqueia carregamento de alguns recursos cross-origin | ajuste as políticas de `helmet` conforme a necessidade, ou mantenha o padrão em desenvolvimento e ajuste caso a caso |

## 📝 Avaliação 2 — instruções de entrega

**Escopo.** Uma aplicação **Vue 3** completa, consumindo uma API (a sua, em memória ou já com Firestore — MySQL só é exigido a partir da Aula 09), sobre o **projeto autoral** de cada estudante (não o UniEventos, que é o exemplo do professor).

**Requisitos obrigatórios:**

- **Vuetify** para toda a interface (nenhum CSS puro estrutural fora do Vuetify, exceto ajustes pontuais).
- **Vue Router**, com no mínimo **4 rotas** (ex.: Home, Detalhe, Formulário de criação/edição, uma quarta rota própria do domínio — listagem filtrada, painel, etc.).
- No mínimo **6 componentes próprios** (`.vue` autorais, além dos componentes do Vuetify) — componentes de card, formulário, lista, filtro, layout, etc.
- **Uma store Pinia** com estado assíncrono: ações que chamam a API, estados de `carregando` e `erro`, getters quando fizer sentido.
- **Axios** com instância dedicada (`axios.create`) e ao menos um interceptor.
- Consumo de API com tratamento visível de **carregando / erro / vazio** (três estados, não só o caminho feliz) em pelo menos uma tela de listagem.
- **Formulário com validação** (Vuetify `rules` ou biblioteca de validação) para criar ou editar um registro do domínio.
- **Layout responsivo** — funcional em tela de celular e de desktop, usando o sistema de grid do Vuetify.

**Rubrica:**

| Critério | Peso |
|---|---|
| Vue Router — 4+ rotas, navegação coerente, guards se aplicável | 1,5 |
| Componentização — 6+ componentes próprios, props/emits corretos | 2,0 |
| Pinia — store com estado assíncrono, carregando/erro tratados | 2,0 |
| Axios — instância dedicada, interceptor, integração com a store | 1,5 |
| Vuetify — uso consistente, responsividade | 1,5 |
| Formulário com validação funcionando | 1,0 |
| Organização do código e commits (histórico git coerente) | 0,5 |

Total: **10,0 pontos**.

**Formato de entrega.** Link do repositório Git (GitHub, GitLab ou similar), **público ou com acesso liberado para o professor**, enviado via **SIGAA**, no campo de entrega da Avaliação 2. O `README.md` do repositório deve conter: nome do projeto autoral, instruções de instalação (`npm install`, `npm run dev`) e uma breve descrição do domínio escolhido.

**Prazo.** Até **07/10/2026, 23h59**, horário de Brasília. O SIGAA registra o horário da submissão — entregas após o prazo entram na política de atraso abaixo.

**Política de atraso.** Cada 24h de atraso desconta 1,0 ponto da nota final da avaliação, até o limite de 5 dias corridos; após esse prazo, a atividade recebe nota zero, salvo justificativa formal (atestado médico ou similar) protocolada junto à coordenação.

**Política de plágio e uso de IA.** É permitido usar ferramentas de IA como apoio (explicar um erro, sugerir uma correção pontual, revisar um trecho) — é o mesmo tipo de apoio que se espera de qualquer ferramenta de desenvolvimento moderna. **Não é permitido** entregar um projeto majoritariamente gerado por IA sem compreensão do próprio código: na correção, o professor pode fazer perguntas orais sobre qualquer trecho entregue, e a incapacidade de explicar decisões básicas do próprio código (por que essa rota, por que essa store, o que faz esse `computed`) resulta em revisão da nota. Cópia entre colegas — código idêntico ou com alterações cosméticas — resulta em nota zero para todos os envolvidos, sem exceção.

## 🏠 Atividade assíncrona (1 h)

Além de finalizar e entregar a Avaliação 2, use esta hora para:

1. Adicionar ao seu `requests.http` autoral os casos de erro esperados (`404`, `422`) — não só o caminho feliz.
2. Rodar o laboratório de rate limit (exercício 4) no seu próprio projeto, confirmando que o `429` aparece.
3. Revisar seu tratador de erros: force um erro inesperado (ex.: acesse uma propriedade de `undefined` de propósito dentro de uma rota) e confirme que a resposta chega como `500` com o envelope `{ "erro": { ... } }`, sem vazar o stack trace para o cliente.

**Critério de pronto:** sua API autoral tem CRUD completo, middlewares próprios funcionando na ordem correta, validação com Zod retornando `422` com mensagens claras, e a Avaliação 2 já submetida no SIGAA.

## ✅ Checkpoint do projeto autoral

- [ ] CRUD completo (`GET` lista, `GET` por id, `POST`, `PUT`, `PATCH`, `DELETE`) funcionando na sua API autoral.
- [ ] Rotas modularizadas com `express.Router()`, montadas com prefixo `/api/v1/<recurso>`.
- [ ] Middlewares próprios (`logger`, `medidorDeTempo`, `middlewareNaoEncontrado`, `tratadorDeErros`) escritos e na ordem correta.
- [ ] Validação de entrada com `zod`, retornando `422` com mensagens em português.
- [ ] `requests.http` cobrindo todos os endpoints, inclusive casos de erro.
- [ ] Front-end autoral consumindo o CRUD completo, com tratamento de carregando/erro/vazio.
- [ ] Avaliação 2 entregue via SIGAA.

## 📚 Para aprofundar

- Guia oficial de roteamento do Express — [expressjs.com/en/guide/routing.html](https://expressjs.com/en/guide/routing.html).
- Guia oficial de middleware — [expressjs.com/en/guide/using-middleware.html](https://expressjs.com/en/guide/using-middleware.html) e *error handling* — [expressjs.com/en/guide/error-handling.html](https://expressjs.com/en/guide/error-handling.html).
- Documentação do Zod — [zod.dev](https://zod.dev/).
- Documentação do `helmet` — [helmetjs.github.io](https://helmetjs.github.io/) — o que cada cabeçalho de segurança faz.
- Documentação do `express-rate-limit` — [express-rate-limit.mintlify.app](https://express-rate-limit.mintlify.app/) — estratégias de limitação além do padrão por IP.
- RFC 9110 (semântica HTTP) — referência formal de métodos e status codes, para quem quiser a fonte primária.
- Plano de curso FACET-SNP-310 — bibliografia básica, capítulos sobre APIs REST e middleware.

Na Aula 09 os dados em memória desta API saem de cena: você migra tudo para **MySQL**, com pool de conexões, consultas parametrizadas e camada de repositório — mantendo os mesmos contratos de endpoint, para o front-end não perceber a diferença.
