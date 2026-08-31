# Aula 08 — Definindo endpoints e middlewares

> **Nível 3 — Frameworks Modernos** · Unidade 3: Integração front-end/back-end
> WebLab · UNEMAT Sinop · Prof. Ivan Luiz Pedroso Pires
> **Carga:** 3 aulas de 50 min (presencial) + 1 h (assíncrona)

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

Na Aula 07 você criou a `unieventos-api` com Express 5, duas rotas `GET` em memória, CORS habilitado, e conectou o front-end real a ela. Hoje essa API vira um CRUD completo, ganha middlewares próprios e validação de entrada — e você recebe as instruções da **Avaliação 2**, com entrega até hoje às 23h59.

- [ ] `unieventos-api` da Aula 07 rodando, com `GET /api/eventos` e `GET /api/eventos/:id` funcionando em memória.
- [ ] Front-end `unieventos-web` apontando para essa API via `baseURL` do Axios.
- [ ] Entendimento de `async`/`await` e por que erros em handlers `async` do Express 5 são capturados automaticamente (Aula 07).
- [ ] Projeto autoral com API própria (`<seu-projeto>-api`) criada na atividade assíncrona da Aula 07.

> **⚠️ Atenção**
> Esta é a aula da **Avaliação 2**. Leia a seção "📝 Avaliação 2 — instruções de entrega" logo no início do período de aula, para planejar seu tempo — o prazo de entrega é hoje, às 23h59.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | REST na prática: recursos, verbos, status codes, formato de resposta, paginação e filtros |
| 2 | 50 min | CRUD completo com `express.Router()`; middlewares próprios e de terceiros; tratador de erros central |
| 3 | 50 min | Validação com `zod`; `requests.http` completo; instruções da Avaliação 2 |

## 1. REST na prática

Você já usa APIs "estilo REST" desde a Aula 06, mas hoje é você quem projeta os endpoints. REST não é um protocolo com regras fixadas em pedra — é um conjunto de convenções que, seguidas com consistência, tornam uma API previsível para quem consome.

O nome vem de *Representational State Transfer* — a ideia central é que cada recurso do seu domínio (um evento, um usuário, uma inscrição) tem uma **representação** (o JSON que a API devolve) e um **endereço próprio** (a URL). O cliente manipula o estado do sistema transferindo representações desse recurso para lá e para cá, usando os verbos HTTP para expressar a intenção. Você não precisa decorar a definição formal — o que importa na prática são as convenções que seguem daqui.

Por que seguir convenção importa: quando toda API do mercado usa `GET` para ler e `POST` para criar, qualquer desenvolvedor que chega no seu projeto já sabe, sem ler documentação nenhuma, que `POST /api/eventos` cria um evento. Quebrar essa expectativa (por exemplo, usando `GET /api/deletarEvento?id=3` para apagar algo) obriga quem consome sua API a ler cada linha de código para entender o que uma rota faz — e, pior, faz com que caches e proxies HTTP, que assumem que `GET` nunca tem efeito colateral, possam repetir a chamada e apagar coisas sem querer.

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

> **🧠 Você sabia?**
> O termo REST foi cunhado em 2000, na tese de doutorado de Roy Fielding — um dos autores da própria especificação do protocolo HTTP. Ele não descrevia uma tecnologia nova, mas um estilo arquitetural que já explicava por que a web funcionava tão bem em escala: cada recurso com endereço próprio, operações padronizadas (os verbos HTTP) e respostas que já dizem por si mesmas o que aconteceu (os status codes). Praticamente toda API que você consome hoje — de rede social, de banco, de pagamento — segue essas convenções, ainda que quase nenhuma implemente a especificação de Fielding à risca.

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

APIs públicas costumam prefixar as rotas com um número de versão — `/api/v1/eventos` — para poder evoluir sem quebrar quem já consome a versão antiga: quando uma mudança incompatível é necessária, ela nasce em `/api/v2` e o `/v1` continua no ar até que todos os clientes migrem.

```js
// exemplo de API versionada — NÃO é o que usamos aqui
app.use('/api/v1/eventos', eventosRoutesV1)
app.use('/api/v2/eventos', eventosRoutesV2)
```

> **🧠 Você sabia?**
> Versionar por caminho (`/api/v1`) é a forma mais comum, mas não a única: há APIs que versionam por cabeçalho (`Accept: application/vnd.unieventos.v2+json`) ou por parâmetro de query (`?versao=2`). O trade-off é sempre o mesmo — caminho é explícito e fácil de testar no navegador; cabeçalho mantém a URL do recurso estável, que é o argumento "REST puro". **Nesta disciplina usamos `/api` sem versão**, porque o `unieventos-api` tem um único cliente (o nosso front) e nenhuma versão antiga para preservar; carregar um `v1` que nunca vira `v2` só adiciona ruído. Quando você publicar uma API com clientes de terceiros, aí sim escolha e documente uma estratégia de versionamento.

O prefixo da `unieventos-api`, portanto, continua sendo o mesmo da Aula 07:

```js
app.use('/api/eventos', eventosRoutes)
```

### Formato de resposta consistente

Uma API previsível responde sempre no mesmo formato — envelope de sucesso e envelope de erro —, para que o front-end trate qualquer resposta da mesma forma, sem checar caso a caso.

```json
{
  "dados": { "id": 1, "titulo": "Semana Acadêmica de Computação" },
  "paginacao": { "pagina": 1, "porPagina": 10, "total": 42 }
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

`dados` carrega o conteúdo (objeto único ou array); `paginacao` carrega os metadados de paginação quando aplicável; `erro` só aparece em respostas de falha, nunca junto com `dados`. Vamos implementar exatamente esse envelope no CRUD desta aula.

O ganho prático aparece no front-end: um interceptor de resposta do Axios (Aula 06) pode, por exemplo, sempre extrair `response.data.dados` automaticamente, ou sempre reconhecer `response.data.erro` para disparar uma notificação padronizada — porque a forma nunca muda, só o conteúdo. Sem esse envelope, cada endpoint devolveria uma "forma" diferente (às vezes um array solto, às vezes um objeto solto, às vezes um objeto com `results`), obrigando o front a tratar cada chamada como um caso especial.

### Paginação, filtros e ordenação por query string

```text
GET /api/eventos?pagina=2&porPagina=10
GET /api/eventos?categoria=palestra
GET /api/eventos?ordenarPor=dataHora&direcao=asc
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
    dataHora: '2030-10-15T19:00:00',
    local: 'Auditório FACET',
    vagas: 80,
    imagemUrl: 'https://picsum.photos/seed/semana-computacao/400/240',
  },
  {
    id: 2,
    titulo: 'Minicurso de Vue 3',
    descricao: 'Introdução prática ao framework Vue com Composition API.',
    categoria: 'minicurso',
    dataHora: '2030-10-20T14:00:00',
    local: 'Laboratório 3',
    vagas: 30,
    imagemUrl: 'https://picsum.photos/seed/minicurso-vue/400/240',
  },
  {
    id: 3,
    titulo: 'Workshop de Firebase e Express',
    descricao: 'Construindo uma API real do zero.',
    categoria: 'workshop',
    dataHora: '2030-10-28T19:30:00',
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

Repare que dentro do arquivo de rotas os caminhos são **relativos**: `router.get('/')` e `router.get('/:id')`, sem repetir `/api/eventos`. É só na hora de montar, em `servidor.js`, que o prefixo é definido:

```js
app.use('/api/eventos', eventosRoutes)
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

// GET /api/eventos — lista com filtro, ordenação e paginação
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
  const porPagina = Number(req.query.porPagina) || 10
  const inicio = (pagina - 1) * porPagina
  const paginaDeResultados = resultado.slice(inicio, inicio + porPagina)

  res.json({
    dados: paginaDeResultados,
    paginacao: { pagina, porPagina, total: resultado.length },
  })
})

// GET /api/eventos/:id — busca um evento específico
router.get('/:id', (req, res) => {
  const id = Number(req.params.id)
  const evento = eventos.find((e) => e.id === id)

  if (!evento) {
    throw erroNaoEncontrado('Evento não encontrado')
  }

  res.json({ dados: evento })
})

// POST /api/eventos — cria um evento novo
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
    .location(`/api/eventos/${novoEvento.id}`)
    .json({ dados: novoEvento })
})

// PUT /api/eventos/:id — substitui o evento inteiro
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

// PATCH /api/eventos/:id — atualiza campos específicos
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

// DELETE /api/eventos/:id — remove o evento
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

// monta o router em /api/eventos — dentro do router, as rotas usam caminhos relativos
app.use('/api/eventos', eventosRoutes)

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
app.use('/api/eventos', eventosRoutes)  // 5º: tenta casar com alguma rota de evento
app.use(middlewareNaoEncontrado)  // 6º: só roda se nada casou acima
app.use(tratadorDeErros)          // 7º: só roda se algo lançou erro em qualquer ponto anterior
```

### Middleware de aplicação × de rota × de erro

**Middleware de aplicação** roda para toda requisição, registrado direto em `app.use(fn)`, sem caminho — é o caso de `cors()`, `express.json()`, `logger`.

**Middleware de rota** roda só para requisições que casam com um caminho e método específicos, registrado como argumento extra antes do handler final:

```js
// middleware de rota: só roda para POST /api/eventos
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

> **🔬 Investigue**
> Adicione um `console.log('middleware X rodou')` no início de cada middleware registrado em `servidor.js` (`cors`, `express.json`, `logger`, `medidorDeTempo`) e reinicie o servidor. Faça uma única requisição `GET /api/eventos` pelo navegador e observe, no terminal, a ordem exata em que as mensagens aparecem. Depois, mova `app.use(logger)` para depois de `app.use('/api/eventos', eventosRoutes)` e repita a requisição — o que muda na ordem impressa, e por quê?

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
  limit: 100,                 // no máximo 100 requisições por IP nessa janela (era `max` até a v6)
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

## 🧩 Padrão de projeto em uso — Chain of Responsibility e Strategy

A cadeia `cors → express.json → logger → medidorDeTempo → eventosRoutes → middlewareNaoEncontrado → tratadorDeErros` é o **Chain of Responsibility** completo: cada middleware decide se processa a requisição e a passa adiante com `next()`, ou se responde e encerra a cadeia ali. A ordem importa — é o próprio desenho do padrão: cada elo só recebe a requisição se o anterior decidiu repassá-la.

Já os validadores de corpo que vamos construir com `zod` ilustram o **Strategy** (comportamental): a função `validar(schema)` é genérica — ela não sabe nada sobre "evento" —, e recebe de fora, como parâmetro, a estratégia de validação específica (o schema Zod do evento, do usuário, do que for). Trocar a validação de uma rota é só trocar o schema passado, sem tocar no middleware `validar`. Isso é Strategy: o algoritmo (validação) é injetado, intercambiável, sem alterar quem o usa.

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

// GET /api/eventos — lista com filtro, ordenação e paginação (sem alteração desde a seção 2)
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
  const porPagina = Number(req.query.porPagina) || 10
  const inicio = (pagina - 1) * porPagina
  const paginaDeResultados = resultado.slice(inicio, inicio + porPagina)

  res.json({
    dados: paginaDeResultados,
    paginacao: { pagina, porPagina, total: resultado.length },
  })
})

// GET /api/eventos/:id — busca um evento específico (sem alteração desde a seção 2)
router.get('/:id', (req, res) => {
  const id = Number(req.params.id)
  const evento = eventos.find((e) => e.id === id)

  if (!evento) {
    throw erroNaoEncontrado('Evento não encontrado')
  }

  res.json({ dados: evento })
})

router.post('/', validar(schemaEvento), (req, res) => {
  // req.body já chega validado e com os tipos corretos (vagas já é number, por exemplo)
  const novoEvento = { id: proximoId(), ...req.body }
  eventos.push(novoEvento)
  res.status(201).location(`/api/eventos/${novoEvento.id}`).json({ dados: novoEvento })
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

@baseUrl = http://localhost:3000/api

### listar eventos (com paginação, filtro e ordenação)
GET {{baseUrl}}/eventos?pagina=1&porPagina=10&categoria=palestra&ordenarPor=dataHora&direcao=asc

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
  "dataHora": "2030-11-05T19:00:00",
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
  "dataHora": "2030-10-16T19:00:00",
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
> A variável `@baseUrl` no topo do arquivo evita repetir `http://localhost:3000/api` em toda linha — troque só ali quando mudar de ambiente (local, homologação, produção).

### Passo 4 — adaptar o front ao envelope de resposta

A API mudou de contrato: onde antes ela devolvia um array solto (`[{...}, {...}]`), agora devolve `{ dados, paginacao }`. O `unieventos-web` da Aula 06 não sabe disso — o `eventosService.listar()` faz `return resposta.data`, e a `HomeView` chama `.filter()` no resultado. Se você subir os dois lado a lado agora, o console mostra `eventos.value.filter is not a function`. **Toda mudança de contrato na API cobra um passo do lado do cliente** — e este é o passo.

Há dois lugares possíveis para desembrulhar o envelope. O primeiro é o próprio `eventosService`, explícito, endpoint a endpoint:

```js
// src/services/eventosService.js (unieventos-web) — versão adaptada ao envelope
import http from './http'

export default {
  async listar(filtros = {}) {
    const resposta = await http.get('/eventos', { params: filtros })
    // a API devolve { dados, paginacao }; quem chama continua recebendo só o array
    return resposta.data.dados
  },

  // a mesma ideia vale para listagens paginadas, quando a tela precisa do total
  async listarComPaginacao(filtros = {}) {
    const resposta = await http.get('/eventos', { params: filtros })
    return { eventos: resposta.data.dados, paginacao: resposta.data.paginacao }
  },

  async buscarPorId(id) {
    const resposta = await http.get(`/eventos/${id}`)
    return resposta.data.dados
  },

  async criar(evento) {
    const resposta = await http.post('/eventos', evento)
    return resposta.data.dados
  },

  async atualizar(id, evento) {
    const resposta = await http.put(`/eventos/${id}`, evento)
    return resposta.data.dados
  },

  async remover(id) {
    await http.delete(`/eventos/${id}`)
  },
}
```

O segundo é o interceptor de resposta do `http.js` (Aula 06), que resolve de uma vez para **todos** os services — inclusive os que você ainda vai escrever:

```js
// src/services/http.js (trecho — dentro do interceptor de response já existente)
http.interceptors.response.use(
  (response) => {
    // desembrulha o envelope: quem chamou recebe direto o conteúdo de `dados`
    if (response.data && typeof response.data === 'object' && 'dados' in response.data) {
      response.paginacao = response.data.paginacao   // preserva a paginação para quem precisar
      response.data = response.data.dados
    }
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('uniEventosToken')
    }
    // o envelope de erro também é único: { erro: { mensagem, codigo } }
    error.mensagemAmigavel = error.response?.data?.erro?.mensagem ?? 'Falha de comunicação com o servidor'
    return Promise.reject(error)
  }
)
```

> **⚠️ Atenção**
> Escolha **um** dos dois — se você desembrulhar no interceptor *e* no service, `resposta.data.dados` vira `undefined` e a lista some sem erro nenhum no console. Neste material seguimos com a versão do interceptor, porque o envelope é uma decisão da API inteira, não de um endpoint. Registre a escolha em uma linha no `README` do front.

### Como testar

Suba os dois projetos ao mesmo tempo — `unieventos-api` em `http://localhost:3000` e `unieventos-web` com `npm run dev` — e percorra este roteiro de ponta a ponta:

```bash
# 1) a API sozinha, pelo terminal
curl -s "http://localhost:3000/api/eventos?pagina=1&porPagina=2" | jq
```

Resultado esperado:

```json
{
  "dados": [
    { "id": 1, "titulo": "Semana Acadêmica de Computação", "categoria": "palestra", "dataHora": "2030-09-10T19:00:00.000Z", "local": "Auditório Central", "vagas": 120 }
  ],
  "paginacao": { "pagina": 1, "porPagina": 2, "total": 3 }
}
```

```bash
# 2) o envelope de erro, com um POST inválido
curl -s -X POST http://localhost:3000/api/eventos \
  -H "Content-Type: application/json" -d '{"titulo":"AB"}' | jq
```

Resultado esperado: status `422` e corpo `{ "erro": { "mensagem": "...", "codigo": "VALIDACAO", "detalhes": [...] } }`.

3. No navegador, abra o `unieventos-web`: a lista da `HomeView` carrega normalmente, o formulário administrativo cria um evento e a exclusão remove da tabela. Na aba **Network**, a resposta de `GET /api/eventos` mostra o objeto `{ dados, paginacao }`; no **Console**, nenhum `filter is not a function`.
4. Pare a API (`Ctrl+C`) e recarregue o front: a mensagem de erro que aparece na tela vem de `error.mensagemAmigavel`, não de um `undefined`.

Se os quatro passos passam, o contrato novo está fechado dos dois lados — e é exatamente esse o critério da Avaliação 2.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Preveja, sem rodar, usando só a tabela de status codes da seção 1 e o CRUD com Zod desta aula, qual status cada chamada abaixo devolve:

```bash
curl -i -X DELETE http://localhost:3000/api/eventos/999
curl -i -X POST http://localhost:3000/api/eventos -H "Content-Type: application/json" -d '{"titulo":"AB","categoria":"show"}'
curl -i -X PATCH http://localhost:3000/api/eventos/1 -H "Content-Type: application/json" -d '{"vagas": 40}'
```

Resultado esperado: (a) `404` — o evento `999` não existe; (b) `422` — `"titulo":"AB"` tem menos de 3 caracteres e `"categoria":"show"` não está no `enum`, ambos rejeitados pelo Zod; (c) `200` com o evento atualizado — `vagas: 40` é um inteiro positivo válido no schema parcial.

**A2.** Complete a linha que falta para a rota de estatísticas (Laboratório B1, a seguir) não ser capturada pelo handler de `:id`:

```js
const router = Router()

// linha que falta aqui
router.get('/:id', (req, res) => { /* busca o evento pelo id */ })
```

Resultado esperado: `router.get('/estatisticas/por-categoria', (req, res) => { ... })` — registrada **antes** de `router.get('/:id', ...)`, senão o Express interpreta `estatisticas` como o valor do parâmetro `:id`.

**A3.** Em uma frase: por que um middleware de erro precisa ter exatamente quatro parâmetros — `(err, req, res, next)` — mesmo quando `next` não é usado dentro dele?

Resultado esperado: porque o Express identifica um middleware de erro pela contagem de parâmetros da função (a aridade); com menos de quatro, ele é tratado como middleware normal e nunca é chamado no caminho de erro.

**A4.** Ache o erro nas linhas abaixo (a ordem de registro quebra o tratamento de erros) e diga a correção:

```js
app.use(tratadorDeErros)
app.use(cors())
app.use(express.json())
app.use('/api/eventos', eventosRoutes)
app.use(middlewareNaoEncontrado)
```

Resultado esperado: `tratadorDeErros` está registrado **antes** das rotas — ele nunca vai capturar erro nenhum. A ordem correta é `cors()`, `express.json()`, as rotas, `middlewareNaoEncontrado` e, só por último, `tratadorDeErros`.

**A5.** Verdadeiro ou falso, com justificativa de uma linha: "`PATCH` é sempre idempotente, assim como `PUT` e `DELETE`."

Resultado esperado: falso — `PATCH` costuma **não** ser idempotente (ex.: um corpo que decrementa `vagas` em 1 produz um resultado diferente a cada chamada); `PUT` é idempotente porque substitui o recurso inteiro pelo mesmo valor em todas as chamadas.

### Nível B — Aplicação

**B1.** Endpoint de contagem por categoria. Crie `GET /api/eventos/estatisticas/por-categoria` que devolve `{ "dados": { "palestra": 1, "minicurso": 1, "workshop": 1 } }`, contando quantos eventos existem em cada categoria.

Resultado esperado: a contagem bate exatamente com os três eventos de exemplo desta aula, e a rota responde corretamente mesmo com `estatisticas` no caminho, sem cair no handler de `:id`.

<details markdown="1">
<summary>Dica</summary>

Cuidado com a ordem: registre essa rota **antes** de `router.get('/:id', ...)`, senão o Express interpreta `estatisticas` como um valor de `:id`.
</details>

**B2.** Middleware de log condicional. Modifique o `logger` para só imprimir requisições cujo método seja `POST`, `PUT`, `PATCH` ou `DELETE` (as que alteram dados) — omita `GET`.

Resultado esperado: no terminal, uma requisição `GET /api/eventos` não gera nenhuma linha de log; uma `POST /api/eventos` gera uma linha, no mesmo formato de antes.

<details markdown="1">
<summary>Dica</summary>

Um `if (req.method !== 'GET') { ... }` dentro do middleware, antes de chamar `next()`.
</details>

**B3.** Erro de validação com múltiplos campos. Envie, pelo `requests.http`, um `POST /api/eventos` com `titulo` vazio **e** `categoria` inválida ao mesmo tempo. Confirme que a resposta `422` lista as duas mensagens de erro no array `detalhes`.

Resultado esperado: a resposta `422` traz `detalhes` com pelo menos duas mensagens, uma sobre o `titulo` e outra sobre a `categoria`, na mesma requisição.

<details markdown="1">
<summary>Dica</summary>

O Zod, por padrão, coleta **todos** os problemas antes de falhar — não para no primeiro. `resultado.error.issues` é um array com um item por campo problemático.
</details>

**B4.** Rate limit em ação. Reduza temporariamente o `limit` do `express-rate-limit` para `5` e a `windowMs` para `60000` (1 minuto). Dispare mais de 5 requisições seguidas com `curl` num loop e observe a resposta `429 Too Many Requests`. Depois volte os valores originais.

Resultado esperado: as primeiras 5 chamadas respondem `200`; a partir da sexta, a resposta muda para `429`, até a janela de 1 minuto expirar.

<details markdown="1">
<summary>Dica</summary>

```bash
for i in 1 2 3 4 5 6 7; do curl -s -o /dev/null -w "%{http_code}\n" http://localhost:3000/api/eventos; done
```
</details>

**B5.** PATCH que tenta mudar o id. Envie `PATCH /api/eventos/1` com corpo `{ "id": 999 }`. Verifique o que acontece com o registro em memória. Corrija o handler para ignorar qualquer `id` enviado no corpo (o id da URL é sempre a fonte da verdade).

Resultado esperado: antes da correção, o registro em memória passa a ter `id: 999` (inconsistente com a URL usada para acessá-lo); depois da correção, o id da URL sempre prevalece, mesmo enviando outro id no corpo.

<details markdown="1">
<summary>Dica</summary>

Depois do merge (`{ ...eventos[indice], ...req.body }`), force `eventos[indice].id = id` (o id da URL, já convertido para número) por cima, sobrescrevendo qualquer valor vindo do corpo.
</details>

### Nível C — Desafio em sala

**C1.** Middleware de erro específico para JSON malformado. Envie, via `curl`, um `POST /api/eventos` com corpo JSON propositalmente quebrado (ex.: `{"titulo": "teste",}` com vírgula sobrando). Observe qual status volta. `express.json()` lança um erro de parsing antes mesmo de sua rota rodar — confirme que esse erro também é capturado pelo seu `tratadorDeErros`, e ajuste a mensagem para ficar amigável ("corpo da requisição não é um JSON válido") quando o erro vier do parser.

Resultado esperado: sem a correção, o erro de parsing cai no `tratadorDeErros` genérico e devolve `500` com "Erro interno do servidor"; depois de adicionar a verificação de `err.type === 'entity.parse.failed'`, a mesma requisição passa a devolver `400` com `{ "erro": { "mensagem": "JSON inválido no corpo da requisição", "codigo": "JSON_INVALIDO" } }`.

<details markdown="1">
<summary>Dica</summary>

O erro lançado pelo `express.json()` tem `err.type === 'entity.parse.failed'`. No `tratadorDeErros`, adicione uma verificação extra antes da checagem de `ErroHttp`: `if (err.type === 'entity.parse.failed') { return res.status(400).json({ erro: { mensagem: 'JSON inválido no corpo da requisição', codigo: 'JSON_INVALIDO' } }) }`.
</details>

## 🏆 Desafios

### ⭐ O 404 que na verdade é um 200

Tags: express, http, bug, investigacao

Teste no seu `unieventos-api`: `GET /api/eventos/abc` (um id que não é número). O que a rota devolve? Compare com o que a tabela de status codes desta aula promete para "recurso inexistente". Investigue por que `Number('abc')` não gera o erro que você esperava, e corrija a rota para tratar esse caso de forma explícita.

**Critérios de pronto**

- `GET /api/eventos/abc` responde `400` (requisição malformada) em vez de tratar `"abc"` como um id válido.
- Um comentário no código explica o que `Number('abc')` retorna e por que isso passava despercebido antes.
- O mesmo tratamento é aplicado a toda rota que recebe `:id` como parâmetro numérico.

<details markdown="1">
<summary>Pistas</summary>

1. `Number('abc')` não lança erro — ele devolve `NaN`, um valor "não é um número" que ainda passa por comparações sem quebrar o programa.
2. `Number.isNaN(id)` detecta o caso; combine com um `throw` de erro `400` antes de continuar a lógica normal do handler.
3. Considere um pequeno middleware de validação de parâmetro reutilizável, para não repetir a checagem em cada rota com `:id`.
</details>

### ⭐⭐ Um middleware, duas versões

Tags: middleware, performance, refatoracao, node

O `medidorDeTempo` desta aula usa `process.hrtime.bigint()` e o evento `'finish'` do objeto `res`. Implemente uma segunda versão que, além de logar o tempo no console, guarda em um array em memória as últimas 100 durações de resposta e exponha isso em `GET /api/metricas` (tempo médio, mínimo e máximo). Meça se registrar essas métricas atrasa perceptivelmente as respostas.

**Critérios de pronto**

- `GET /api/metricas` devolve `{ "dados": { "media": N, "minimo": N, "maximo": N, "amostras": N } }`, calculado a partir das últimas 100 requisições reais.
- O array de amostras nunca cresce além de 100 itens (as mais antigas são descartadas).
- Uma medição no README compara o tempo de resposta de `GET /api/eventos` com e sem o middleware de métricas ativado (usando `curl -w '%{time_total}'`).
- Uma frase conclui se a diferença medida é ou não perceptível para este projeto.

<details markdown="1">
<summary>Pistas</summary>

1. Um array declarado fora de qualquer função guarda o estado entre requisições — cuidado, isso não escalaria para múltiplas instâncias do servidor (mesma limitação do array em memória das Aulas 07 e 08).
2. `array.push(duracao); if (array.length > 100) array.shift()` mantém o tamanho fixo.
3. Para média, mínimo e máximo, um `reduce` simples resolve; não precisa de biblioteca externa.
</details>

### ⭐⭐⭐ Envelope de erro, ponta a ponta

Tags: api, express, refatoracao, projeto

O envelope `{ "erro": { "mensagem", "codigo" } }` desta aula não chega pronto ao usuário final — alguém no front precisa transformá-lo em algo visível. Implemente, no front-end do seu projeto autoral, um interceptor de resposta do Axios que trate todos os códigos de erro conhecidos (`VALIDACAO`, `NAO_ENCONTRADO`, `ROTA_NAO_ENCONTRADA`, `RATE_LIMIT`, `ERRO_INTERNO`, `JSON_INVALIDO`) com uma mensagem amigável específica, e prove com prints que cada código produz uma notificação diferente na tela.

**Critérios de pronto**

- Uma função `traduzirErro(codigo)` no front-end mapeia cada código conhecido para uma frase em português voltada ao usuário final (não a mensagem técnica crua).
- Um snackbar ou notificação visível aparece para pelo menos 4 códigos de erro diferentes, provocados de propósito (evento inexistente, campo inválido, rota errada, limite de requisições).
- Um código não mapeado (ex.: um código que você inventa de propósito, só para o teste) cai num texto padrão ("Algo deu errado, tente novamente"), sem quebrar a interface.
- Prints (ou um vídeo curto) mostrando as quatro notificações diferentes na tela.

<details markdown="1">
<summary>Pistas</summary>

1. O interceptor de resposta do Axios (Aula 06) recebe o erro em `error.response.data.erro.codigo` — é esse valor que entra no mapeamento de tradução.
2. Um objeto `{ VALIDACAO: '...', NAO_ENCONTRADO: '...' }` com um valor padrão (`objeto[codigo] ?? 'Algo deu errado...'`) cobre o caso "código desconhecido" sem precisar de uma cadeia longa de `if/else`.
3. Para provocar o `RATE_LIMIT` de propósito, reduza temporariamente o `limit` do rate limiter (Laboratório B4) e dispare várias requisições seguidas pelo front.
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

## 🏠 Atividade assíncrona (1 h)

Além de finalizar e entregar a Avaliação 2, use esta hora para:

1. Adicionar ao seu `requests.http` autoral os casos de erro esperados (`404`, `422`) — não só o caminho feliz.
2. Rodar o laboratório de rate limit (exercício 4) no seu próprio projeto, confirmando que o `429` aparece.
3. Revisar seu tratador de erros: force um erro inesperado (ex.: acesse uma propriedade de `undefined` de propósito dentro de uma rota) e confirme que a resposta chega como `500` com o envelope `{ "erro": { ... } }`, sem vazar o stack trace para o cliente.

**Critério de pronto:** sua API autoral tem CRUD completo, middlewares próprios funcionando na ordem correta, validação com Zod retornando `422` com mensagens claras, e a Avaliação 2 já submetida no SIGAA.

## ✅ Checkpoint do projeto autoral

- [ ] CRUD completo (`GET` lista, `GET` por id, `POST`, `PUT`, `PATCH`, `DELETE`) funcionando na sua API autoral.
- [ ] Rotas modularizadas com `express.Router()`, montadas com prefixo `/api/<recurso>`.
- [ ] Middlewares próprios (`logger`, `medidorDeTempo`, `middlewareNaoEncontrado`, `tratadorDeErros`) escritos e na ordem correta.
- [ ] Validação de entrada com `zod`, retornando `422` com mensagens em português.
- [ ] `requests.http` cobrindo todos os endpoints, inclusive casos de erro.
- [ ] Front-end autoral consumindo o CRUD completo, com tratamento de carregando/erro/vazio.
- [ ] Avaliação 2 entregue via SIGAA.

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

**Prazo.** Até 23h59 do prazo publicado no SIGAA (veja também o quadro de avaliações em [`../nivel-3/#avaliacao`](../nivel-3/#avaliacao)), horário de Brasília. O SIGAA registra o horário da submissão — entregas após o prazo entram na política de atraso abaixo.

**Política de atraso.** Cada 24h de atraso desconta 1,0 ponto da nota final da avaliação, até o limite de 5 dias corridos; após esse prazo, a atividade recebe nota zero, salvo justificativa formal (atestado médico ou similar) protocolada junto à coordenação.

**Política de plágio e uso de IA.** É permitido usar ferramentas de IA como apoio (explicar um erro, sugerir uma correção pontual, revisar um trecho) — é o mesmo tipo de apoio que se espera de qualquer ferramenta de desenvolvimento moderna. **Não é permitido** entregar um projeto majoritariamente gerado por IA sem compreensão do próprio código: na correção, o professor pode fazer perguntas orais sobre qualquer trecho entregue, e a incapacidade de explicar decisões básicas do próprio código (por que essa rota, por que essa store, o que faz esse `computed`) resulta em revisão da nota. Cópia entre colegas — código idêntico ou com alterações cosméticas — resulta em nota zero para todos os envolvidos, sem exceção.

## 📚 Para aprofundar

- Guia oficial de roteamento do Express — [expressjs.com/en/guide/routing.html](https://expressjs.com/en/guide/routing.html).
- Guia oficial de middleware — [expressjs.com/en/guide/using-middleware.html](https://expressjs.com/en/guide/using-middleware.html) e *error handling* — [expressjs.com/en/guide/error-handling.html](https://expressjs.com/en/guide/error-handling.html).
- Documentação do Zod — [zod.dev](https://zod.dev/).
- Documentação do `helmet` — [helmetjs.github.io](https://helmetjs.github.io/) — o que cada cabeçalho de segurança faz.
- Documentação do `express-rate-limit` — [express-rate-limit.mintlify.app](https://express-rate-limit.mintlify.app/) — estratégias de limitação além do padrão por IP.
- RFC 9110 (semântica HTTP) — referência formal de métodos e status codes, para quem quiser a fonte primária.
- Plano de curso FACET-SNP-310 — bibliografia básica, capítulos sobre APIs REST e middleware.

Na Aula 09 os dados em memória desta API saem de cena: você migra tudo para **MySQL**, com pool de conexões, consultas parametrizadas e camada de repositório — mantendo os mesmos contratos de endpoint, para o front-end não perceber a diferença.
