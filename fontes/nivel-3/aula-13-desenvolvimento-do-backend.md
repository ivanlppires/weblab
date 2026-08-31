# Aula 13 — Desenvolvimento do back-end em camadas

> **Nível 3 — Frameworks Modernos** · Unidade 3: Integração front-end/back-end
> WebLab · UNEMAT — Campus Sinop
> **Tempo estimado:** 3 blocos de 50 min + 1 h de prática

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Organizar uma API Express em camadas (`routes → controllers → services → repositories → db`), aplicando a regra de dependência entre elas.
- Aplicar injeção de dependência sem framework, passando repositórios para services por parâmetro/factory, e explicar por que isso torna o código testável.
- Centralizar e validar a configuração da aplicação com `zod` em `src/config/index.js`, falhando rápido quando falta uma variável de ambiente.
- Construir uma hierarquia de erros de domínio e um tratador de erros central que mapeia cada erro para o status HTTP correto, com logs estruturados via `pino`.
- Aplicar proteções básicas de segurança (`helmet`, `express-rate-limit`, CORS restritivo, limite de payload) e relacioná-las ao OWASP Top 10.
- Escrever testes automatizados de integração (rota, com `supertest`) e unitários (service, com repositório falso) usando `vitest`.
- Criar e executar migrations de banco de dados com scripts numerados e uma tabela de controle, sem depender de `schema.sql` manual.

## 📋 Pré-requisitos desta aula

Na Aula 12 trocamos o MySQL por Supabase sem alterar uma linha do front-end, porque a camada `services/` já escondia a origem dos dados atrás de uma interface única — o padrão **Adapter** em ação. Isso só foi possível porque o back-end já tinha, mesmo que informalmente, uma separação entre "o que a rota expõe" e "de onde o dado vem". Hoje formalizamos essa separação: paramos de escrever back-end que "funciona" e passamos a escrever back-end que **se sustenta** — testável, seguro, com erros previsíveis e configuração validada.

- API `unieventos-api` funcionando com Express 5, persistência em MySQL (Aula 09) e autenticação Firebase (Aula 10), com CRUD completo (Aula 11).
- Estrutura de pastas `src/routes`, `src/controllers`, `src/services`, `src/repositories` já existente desde a Aula 09 — hoje ela é formalizada e completada, não criada do zero.
- Node.js 22 LTS e MySQL rodando localmente (ou acessível via `DATABASE_URL`).

Checklist antes de começar:

- [ ] `npm run dev` sobe a API sem erro.
- [ ] Existe pelo menos um endpoint de eventos funcionando (`GET /api/eventos`).
- [ ] Você sabe onde estão as credenciais do banco no seu `.env`.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Arquitetura em camadas, injeção de dependência, configuração centralizada com zod |
| 2 | 50 min | Hierarquia de erros, segurança prática (helmet, rate limit, CORS), OWASP Top 10 |
| 3 | 50 min | Testes com vitest + supertest, migrations com scripts numerados |

## 1. Arquitetura em camadas revisitada

As Aulas 09 e 11 já entregaram o esqueleto certo: rota → controller → service → repository, com validação por middleware Zod e um tratador de erros central. O que falta não é a divisão em camadas — é **formalizar e completar** o que começamos. Hoje as dependências deixam de ser importadas e passam a ser injetadas (o que torna o service testável sem banco), a configuração passa por uma porta única e validada, os erros ganham uma hierarquia de domínio em cima do `ErroHttp` da Aula 08, e o schema do banco deixa de ser um `schema.sql` manual para virar migrations versionadas.

A solução é formalizar cinco responsabilidades separadas:

```text
routes/        → só sabe de HTTP: métodos, caminhos, parâmetros, chama o controller
controllers/    → traduz requisição/resposta HTTP para chamadas de service
services/       → regra de negócio pura, não sabe de Express nem de SQL
repositories/   → sabe conversar com a fonte de dados (MySQL, Supabase, memória...)
db/            → conexão de baixo nível (pool do mysql2, cliente do Supabase)
```

Mais três pastas de apoio, que qualquer camada pode usar:

```text
middlewares/   → funções que interceptam a requisição (auth, validação, log, segurança)
validators/    → esquemas zod que descrevem o formato esperado de cada entrada
utils/         → funções puras reaproveitáveis (logger, formatação, helpers)
config/        → leitura e validação centralizada de variáveis de ambiente
```

### 1.1 O fluxo de uma requisição, camada por camada

```text
Cliente HTTP (front-end / Postman)
        │
        │ POST /api/eventos  { titulo, categoria, vagas, ... }
        ▼
┌─────────────────────┐
│ middlewares globais  │  helmet, cors, express.json, rate-limit, log
└─────────┬────────────┘
          ▼
┌─────────────────────┐
│ routes/eventos.js    │  define o path e delega ao controller
└─────────┬────────────┘
          ▼
┌─────────────────────┐
│ middlewares de rota  │  autenticação (autenticar), validação (validar(schema))
└─────────┬────────────┘
          ▼
┌──────────────────────────┐
│ controllers/eventosController │  lê req.body/req.params, chama o service,
│                                │  monta a resposta HTTP (status + JSON)
└─────────┬──────────────────────┘
          ▼
┌──────────────────────────┐
│ services/eventosService   │  regra de negócio: "vagas não pode ser negativo",
│                            │  "só o dono pode editar", orquestra repositórios
└─────────┬──────────────────────┘
          ▼
┌──────────────────────────┐
│ repositories/eventosRepository │  monta e executa a query, mapeia linha → objeto
└─────────┬──────────────────────┘
          ▼
┌──────────────────────────┐
│ db/pool.js                │  conexão física com o MySQL (ou outro SGBD)
└────────────────────────────┘
```

A resposta sobe pelo mesmo caminho, em ordem inversa: o repository devolve dados brutos, o service aplica regra de negócio e devolve um objeto de domínio, o controller decide o status HTTP e serializa em JSON, o Express entrega ao cliente.

### 1.2 A regra de dependência

> **⚠️ Atenção**
> Camada de fora **pode** conhecer e importar a de dentro. Camada de dentro **nunca** pode importar a de fora.

Na prática:

- `routes` pode importar `controllers`. `controllers` **não pode** importar `routes`.
- `controllers` pode importar `services`. `services` **não pode** importar `controllers` nem `req`/`res` do Express.
- `services` pode importar `repositories`. `repositories` **não pode** importar `services`.
- `repositories` pode importar `db`. `db` não sabe que `repositories` existe.

O motivo: quanto mais "para dentro", mais a camada deveria ser reutilizável e testável sem HTTP nem banco real. Um `service` que importa `req`/`res` do Express está, na prática, acoplado ao protocolo HTTP — e não dá mais para chamá-lo a partir de um job agendado, de um teste unitário puro, ou de uma futura API GraphQL sem reescrever regra de negócio.

> **🔎 Por baixo do capô**
> Essa regra é uma versão simplificada da **Dependency Inversion Principle** (o "D" do SOLID) e da **Arquitetura Limpa** (Clean Architecture, Robert C. Martin): as regras de negócio no centro, os detalhes de infraestrutura (HTTP, banco, filesystem) na borda, sempre apontando para dentro.

## 2. Injeção de dependência sem framework

O problema mais comum em back-ends que "crescem sem arquitetura" é o `service` importando o `repository` diretamente no topo do arquivo. Funciona, mas prende o service a uma implementação específica — impossível testar sem banco de verdade, impossível trocar de fonte de dados sem editar o service.

**Antes — import direto, acoplado:**

```js
// src/services/eventosService.ANTES.js
// PROBLEMA: este arquivo só funciona se existir um MySQL de verdade rodando.
// Não dá para testar a regra "vagas não pode ser negativo" sem banco.
import { pool } from '../db/pool.js'

export async function listarEventos() {
  const [linhas] = await pool.query('SELECT * FROM eventos ORDER BY data_hora')
  return linhas
}

export async function criarEvento(dados) {
  if (dados.vagas < 0) {
    throw new Error('vagas não pode ser negativo')
  }
  const [resultado] = await pool.query(
    'INSERT INTO eventos (titulo, categoria, vagas) VALUES (?, ?, ?)',
    [dados.titulo, dados.categoria, dados.vagas],
  )
  return { id: resultado.insertId, ...dados }
}
```

**Depois — o repositório é injetado (passado por parâmetro):**

```js
// src/services/eventosService.js
// O service NÃO SABE se o repositório fala com MySQL, Supabase ou memória.
// Ele só conhece a INTERFACE: listar(), buscarPorId(), criar(), atualizar(), remover().
import { ErroDeValidacao, ErroNaoEncontrado } from '../erros/index.js'

export function criarServicoDeEventos({ eventosRepository }) {
  return {
    async listarEventos({ categoria, busca, pagina = 1, porPagina = 20 } = {}) {
      const paginaSegura = Math.max(1, Number(pagina) || 1)
      const porPaginaSegura = Math.min(50, Math.max(1, Number(porPagina) || 20))

      const [dados, total] = await Promise.all([
        eventosRepository.listar({ categoria, busca, pagina: paginaSegura, porPagina: porPaginaSegura }),
        eventosRepository.contar({ categoria, busca }),
      ])

      // o MESMO envelope das Aulas 08–11: { dados, paginacao }.
      // Devolver o array puro aqui quebraria o v-data-table-server do front,
      // que lê `paginacao.total` para saber quantas páginas existem.
      return {
        dados,
        paginacao: {
          pagina: paginaSegura,
          porPagina: porPaginaSegura,
          total,
          totalPaginas: Math.ceil(total / porPaginaSegura),
        },
      }
    },

    async buscarEventoPorId(id) {
      const evento = await eventosRepository.buscarPorId(id)
      if (!evento) {
        throw new ErroNaoEncontrado(`Evento ${id} não encontrado`)
      }
      return evento
    },

    async criarEvento(dados) {
      if (dados.vagas < 0) {
        throw new ErroDeValidacao('vagas não pode ser negativo')
      }
      return eventosRepository.criar(dados)
    },

    async atualizarEvento(id, dados) {
      await this.buscarEventoPorId(id) // reaproveita a validação de existência
      return eventosRepository.atualizar(id, dados)
    },

    async removerEvento(id) {
      await this.buscarEventoPorId(id)
      return eventosRepository.remover(id)
    },
  }
}
```

A função `criarServicoDeEventos` é uma **factory**: recebe as dependências como argumento (aqui, um objeto com `eventosRepository`) e devolve o objeto pronto para uso. Quem monta a aplicação decide **qual** repositório injetar — em produção, o do MySQL; em teste, um repositório falso em memória, sem precisar de banco nenhum.

```js
// src/app.js (montagem — quem decide as dependências concretas)
import { criarRepositorioDeEventosMySQL } from './repositories/eventosRepository.mysql.js'
import { criarServicoDeEventos } from './services/eventosService.js'

const eventosRepository = criarRepositorioDeEventosMySQL()
const eventosService = criarServicoDeEventos({ eventosRepository })
// eventosService agora pode ser passado ao controller, sem que o service
// jamais tenha importado o pool do MySQL diretamente.
```

> **💡 Dica**
> Injeção de dependência não exige framework nenhum em JavaScript — não precisamos de `@Injectable()` nem de container de DI. Uma função que recebe parâmetros já é injeção de dependência. O nome bonito não deve intimidar: é passar objetos como argumento, em vez de importar dentro do arquivo.

> **🧠 Você sabia?**
> O nome "injeção de dependência" foi cunhado por Martin Fowler em 2004, no artigo *Inversion of Control Containers and the Dependency Injection pattern*, justamente para separar a técnica (receber dependências de fora) dos containers pesados que a implementavam em Java na época. Vinte anos depois, o exemplo mais simples do artigo continua igual ao que você acabou de escrever: uma função que recebe o que precisa por parâmetro.

## 3. Configuração centralizada com zod

Espalhar `process.env.ALGUMA_COISA` pelo código inteiro é frágil: se a variável não existir, o erro só aparece no meio de uma requisição, em produção, na pior hora. A solução é validar **todo** o ambiente uma única vez, na inicialização, e falhar rápido se algo estiver faltando.

```js
// src/config/index.js
import { z } from 'zod'
import 'dotenv/config'

const esquemaDeAmbiente = z.object({
  NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),
  PORT: z.coerce.number().int().positive().default(3000),

  DB_HOST: z.string().min(1, 'DB_HOST é obrigatória'),
  DB_PORT: z.coerce.number().int().positive().default(3306),
  DB_USER: z.string().min(1, 'DB_USER é obrigatória'),
  DB_PASSWORD: z.string().min(1, 'DB_PASSWORD é obrigatória'),
  DB_NAME: z.string().min(1, 'DB_NAME é obrigatória'),

  FIREBASE_PROJECT_ID: z.string().min(1, 'FIREBASE_PROJECT_ID é obrigatória'),

  CORS_ORIGEM_PERMITIDA: z.string().min(1, 'CORS_ORIGEM_PERMITIDA é obrigatória'),
})

// safeParse NÃO lança exceção — devolve um objeto { success, data } ou { success, error }.
// Isso permite montar uma mensagem de erro clara antes de encerrar o processo.
const resultado = esquemaDeAmbiente.safeParse(process.env)

if (!resultado.success) {
  console.error('❌ Configuração de ambiente inválida:')
  for (const problema of resultado.error.issues) {
    console.error(`  - ${problema.path.join('.')}: ${problema.message}`)
  }
  // Falha rápido: melhor a aplicação nem subir do que subir quebrada.
  process.exit(1)
}

export const config = Object.freeze(resultado.data)
```

```bash
# .env.example — copie para .env e preencha com valores reais
NODE_ENV=development
PORT=3000

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=troque-esta-senha
DB_NAME=unieventos

FIREBASE_PROJECT_ID=uni-eventos-12345

CORS_ORIGEM_PERMITIDA=http://localhost:5173
```

A partir de agora, **nenhum outro arquivo** lê `process.env` diretamente — todos importam `config` de `src/config/index.js`:

```js
// src/db/pool.js — uso de config em vez de process.env espalhado
import mysql from 'mysql2/promise'
import { config } from '../config/index.js'

// a configuração vive no MESMO arquivo do pool — um arquivo só, sem
// `configuracaoDoPool.js` separado para importar de dois lugares
const configuracaoDoPool = {
  host: config.DB_HOST,
  port: config.DB_PORT,
  user: config.DB_USER,
  password: config.DB_PASSWORD,
  database: config.DB_NAME,
  waitForConnections: true,
  connectionLimit: 10,
}
```

> **⚠️ Atenção**
> Se você esquecer `DB_PASSWORD` no `.env`, o processo **não sobe** — imprime exatamente qual variável falta e sai com `process.exit(1)`. Isso é intencional: é infinitamente melhor descobrir isso agora, no `npm run dev`, do que na madrugada anterior ao deploy do Marco 3, tentando descobrir por que a aplicação não sobe em produção.

## 4. Tratamento de erros maduro

### 4.1 Hierarquia de erros de domínio

A classe base já existe desde a Aula 08: `ErroHttp`, em `src/erros/ErroHttp.js`, com `status`, `message` e `codigo`. Não vamos criar uma segunda família de erros — vamos **estender** essa, dando nome de domínio a cada caso e acrescentando a marca `operacional`, que separa "erro esperado" de "bug".

```js
// src/erros/index.js — reexporta o ErroHttp da Aula 08 e acrescenta os erros de domínio
import { ErroHttp } from './ErroHttp.js'

export { ErroHttp }

// Erro de domínio = ErroHttp + a marca `operacional`, que o tratador usa
// para decidir entre logar um aviso (esperado) ou um erro com stack (bug).
export class ErroDeAplicacao extends ErroHttp {
  constructor(mensagem, status = 500, codigo = 'ERRO_INTERNO') {
    super(status, mensagem, codigo)
    this.name = this.constructor.name
    this.operacional = true
  }
}

export class ErroDeValidacao extends ErroDeAplicacao {
  constructor(mensagem, detalhes = []) {
    // 422, o mesmo status de validação fixado na Aula 08 — não 400
    super(mensagem, 422, 'VALIDACAO')
    this.detalhes = detalhes
  }
}

export class ErroNaoEncontrado extends ErroDeAplicacao {
  constructor(mensagem = 'Recurso não encontrado') {
    super(mensagem, 404, 'NAO_ENCONTRADO')
  }
}

export class ErroDeAutorizacao extends ErroDeAplicacao {
  constructor(mensagem = 'Você não tem permissão para executar esta ação') {
    super(mensagem, 403, 'NAO_AUTORIZADO')
  }
}

export class ErroDeConflito extends ErroDeAplicacao {
  constructor(mensagem = 'Conflito com o estado atual do recurso') {
    super(mensagem, 409, 'CONFLITO')
  }
}
```

> **⚠️ Atenção**
> `erroNaoEncontrado()` e `erroValidacao()` (os atalhos da Aula 08) continuam valendo — `new ErroNaoEncontrado(...)` é a mesma coisa com nome de classe. O que **não** muda em hipótese alguma é o envelope que sai na resposta: `{ erro: { mensagem, codigo } }`, com `detalhes` quando for validação. A store da Aula 11 lê exatamente `erro.mensagem`; inventar um formato novo aqui quebraria o front sem aviso.

Usar essa hierarquia no service fica direto:

```js
// trecho de src/services/inscricoesService.js
import { ErroDeConflito, ErroDeAutorizacao } from '../erros/index.js'

async function inscrever({ eventoId, usuarioUid }) {
  const jaInscrito = await inscricoesRepository.existeInscricao(eventoId, usuarioUid)
  if (jaInscrito) {
    throw new ErroDeConflito('Você já está inscrito neste evento')
  }
  return inscricoesRepository.criar({ eventoId, usuarioUid })
}

async function cancelarInscricao({ inscricaoId, usuarioUidSolicitante }) {
  const inscricao = await inscricoesRepository.buscarPorId(inscricaoId)
  if (inscricao.usuario_uid !== usuarioUidSolicitante) {
    throw new ErroDeAutorizacao('Só é possível cancelar a própria inscrição')
  }
  return inscricoesRepository.remover(inscricaoId)
}
```

### 4.2 Logs estruturados com pino

```bash
npm install pino pino-http
```

```js
// src/utils/logger.js
import pino from 'pino'
import { config } from '../config/index.js'

// Em desenvolvimento, log legível por humano (pino-pretty precisa ser instalado à parte
// como devDependency: npm install -D pino-pretty).
// Em produção, log em JSON puro — mais rápido e pronto para ferramentas de observabilidade.
export const logger = pino({
  level: config.NODE_ENV === 'production' ? 'info' : 'debug',
  transport:
    config.NODE_ENV === 'production'
      ? undefined
      : { target: 'pino-pretty', options: { colorize: true } },
})
```

### 4.3 O tratador de erros central

```js
// src/middlewares/tratadorDeErros.js
import { logger } from '../utils/logger.js'
import { config } from '../config/index.js'

// Middleware de erro do Express: identificado pela ASSINATURA DE 4 PARÂMETROS.
// Em Express 5, erros lançados dentro de handlers async chegam aqui automaticamente,
// sem precisar de try/catch manual nem de .catch(next) em cada rota.
export function tratadorDeErros(erro, req, res, next) {
  const status = erro.status ?? 500
  const ehErroOperacional = erro.operacional === true

  // Erros operacionais (esperados: validação, não encontrado...) viram log de aviso.
  // Erros não-operacionais (bug inesperado) viram log de erro, com stack completo.
  if (ehErroOperacional) {
    logger.warn({ status, mensagem: erro.message, path: req.path }, 'erro operacional')
  } else {
    logger.error({ status, err: erro, path: req.path }, 'erro inesperado')
  }

  // Envelope ÚNICO da trilha, fixado na Aula 08 e lido pela store da Aula 11.
  const corpoDaResposta = {
    erro: {
      mensagem: ehErroOperacional ? erro.message : 'Erro interno do servidor',
      codigo: erro.codigo ?? 'ERRO_INTERNO',
    },
  }

  if (erro.detalhes) {
    corpoDaResposta.erro.detalhes = erro.detalhes
  }

  // NUNCA vazar stack trace em produção — é informação valiosa para um atacante
  // (caminhos de arquivo, versão de bibliotecas, estrutura interna).
  if (config.NODE_ENV !== 'production') {
    corpoDaResposta.erro.stack = erro.stack
  }

  res.status(status).json(corpoDaResposta)
}
```

```js
// src/server.js — captura de falhas que escapam do Express
import { app } from './app.js'
import { config } from './config/index.js'
import { logger } from './utils/logger.js'

const servidor = app.listen(config.PORT, () => {
  logger.info(`API rodando na porta ${config.PORT} (${config.NODE_ENV})`)
})

// Promises rejeitadas sem .catch em NENHUM lugar do código (fora do ciclo de
// requisição do Express) caem aqui. Sem isso, o processo Node continua rodando
// em estado inconsistente, silenciosamente.
process.on('unhandledRejection', (motivo) => {
  logger.error({ err: motivo }, 'unhandledRejection não tratada — encerrando processo')
  servidor.close(() => process.exit(1))
})

process.on('uncaughtException', (erro) => {
  logger.error({ err: erro }, 'uncaughtException — encerrando processo')
  process.exit(1)
})
```

> **📌 Vale gravar**
> `unhandledRejection` captura Promises rejeitadas que ninguém tratou; `uncaughtException` captura exceções síncronas que escaparam de qualquer `try/catch`. Nenhum dos dois substitui tratamento de erro local — são uma **rede de segurança final**, não a primeira linha de defesa.

## 5. Segurança prática

Regra de ouro: **nunca confie em nada que vem do cliente** — nem no `Content-Type` declarado, nem no tamanho do payload, nem nos campos do corpo, nem no token de autenticação sem verificá-lo. Tudo que chega de fora é hostil até prova em contrário.

```bash
npm install helmet express-rate-limit cors
```

```js
// src/middlewares/seguranca.js
import helmet from 'helmet'
import rateLimit from 'express-rate-limit'
import cors from 'cors'
import { config } from '../config/index.js'

// helmet(): define um conjunto de cabeçalhos HTTP de segurança com um só import
// (X-Content-Type-Options, X-Frame-Options, Strict-Transport-Security etc.).
export const cabecalhosDeSeguranca = helmet()

// Limita quantas requisições um mesmo IP pode fazer em uma janela de tempo —
// mitiga força bruta em login e ataques de negação de serviço simples.
export const limitadorDeTaxa = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutos
  limit: 100,                // 100 requisições por IP nessa janela
  standardHeaders: true,
  legacyHeaders: false,
  message: { erro: { mensagem: 'Muitas requisições. Tente novamente mais tarde.', codigo: 'RATE_LIMIT' } },
})

// CORS restritivo: só o domínio do front tem permissão — nunca use origin: '*'
// em uma API que aceita cookies ou token de autenticação.
export const corsConfigurado = cors({
  origin: config.CORS_ORIGEM_PERMITIDA,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
})
```

```js
// trecho de src/app.js — ordem importa: segurança primeiro, depois parsing, depois rotas
import express from 'express'
import { cabecalhosDeSeguranca, limitadorDeTaxa, corsConfigurado } from './middlewares/seguranca.js'

export function criarApp({ eventosRepository } = {}) {
  const app = express()

  app.use(cabecalhosDeSeguranca)
  app.use(corsConfigurado)
  app.use(limitadorDeTaxa)

  // Limite de tamanho do corpo: evita que alguém envie um payload de 500 MB
  // para derrubar o processo por consumo de memória.
  app.use(express.json({ limit: '10kb' }))
  app.use(express.urlencoded({ extended: true, limit: '10kb' }))

  // As rotas de negócio e o tratador de erros entram aqui — Passo 13 do "Mão na massa"

  return app
}
```

> **⚠️ Atenção**
> `express.json({ limit: '10kb' })` rejeita automaticamente corpos maiores com `413 Payload Too Large`. Ajuste o limite ao seu domínio — 10kb é generoso para um formulário de evento, mas seria pouco se você aceitasse upload de imagem em base64 no corpo (nesse caso, prefira Storage, como no Supabase da Aula 12).

> **🔬 Investigue**
> Com a API rodando, execute `curl -i http://localhost:3000/health` e conte os cabeçalhos da resposta. Comente a linha `app.use(cabecalhosDeSeguranca)`, reinicie e rode de novo: quantos sumiram? Procure `X-Powered-By: Express` (o helmet o remove — é uma pista de graça para quem ataca), `X-Content-Type-Options: nosniff` e `Content-Security-Policy`. Depois descomente e teste o limitador: `for i in $(seq 1 101); do curl -s -o /dev/null -w "%{http_code} " http://localhost:3000/health; done` — o último número deve ser `429`, e um `curl -i` na sequência mostra `RateLimit-Remaining: 0`.

### 5.1 Checklist OWASP Top 10 aplicado a esta trilha

| Categoria OWASP | O que fazemos no UniEventos |
|---|---|
| A01 — Quebra de controle de acesso | Middlewares `autenticar`/`autorizar` (Aula 10) + verificação de dono do recurso nos services (ex.: `ErroDeAutorizacao` ao cancelar inscrição alheia) |
| A02 — Falhas criptográficas | Senha nunca é gerenciada por nós — delegada ao Firebase Auth; `.env` fora do controle de versão; HTTPS obrigatório em produção (Aula 15) |
| A03 — Injeção | Queries sempre parametrizadas com `?` no `mysql2` (nunca concatenação de string); validação de entrada com `zod` antes de tocar no banco |
| A04 — Design inseguro | Arquitetura em camadas desta aula; regra de negócio centralizada no service, não espalhada em cada rota |
| A05 — Configuração incorreta | `helmet`, CORS restritivo, `.env` validado por `zod`, stack trace escondida em produção |
| A07 — Falhas de identificação | Token do Firebase verificado no back a cada requisição (Aula 10), nunca confiar em `usuario_uid` vindo do corpo da requisição |
| A09 — Falhas de log e monitoramento | Logs estruturados com `pino`, diferenciando erro operacional de erro inesperado |

> **🔎 Por baixo do capô**
> Note que "sanitizar entrada" aqui não significa escapar HTML manualmente — significa **validar contra um schema** (zod) antes de qualquer processamento, e **nunca montar SQL por concatenação**. Essas duas práticas já eliminam a maior parte da superfície de ataque de injeção em uma API JSON.

## 6. Testes automatizados

### 6.1 A pirâmide de testes

```text
        ▲
       ╱ ╲        poucos, lentos, caros de manter
      ╱ E2E╲       (Cypress/Playwright rodando a UI inteira)
     ╱───────╲
    ╱   API/   ╲   médios: sobem a aplicação, testam rotas HTTP reais
   ╱ integração ╲  (supertest — Seção 6.3)
  ╱───────────────╲
 ╱   unitários      ╲  muitos, rápidos, baratos — testam uma função/service
╱  (service, utils)  ╲ isolado, sem rede nem banco (Seção 6.4)
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
```

Testar o service unitariamente é mais barato que testar pela UI por três motivos: (1) roda em milissegundos, sem subir navegador nem servidor; (2) não depende de rede nem de banco de dados real, então não quebra por instabilidade externa; (3) aponta exatamente qual regra de negócio falhou, sem precisar navegar até a tela que dispara aquele fluxo.

### 6.2 Instalando e configurando

```bash
npm install -D vitest supertest
```

```json
// package.json — trecho de "scripts"
{
  "scripts": {
    "dev": "node --watch src/server.js",
    "start": "node src/server.js",
    "test": "vitest run",
    "test:watch": "vitest"
  }
}
```

```js
// vitest.config.js
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    environment: 'node',
  },
})
```

### 6.3 Teste de integração (rota, com supertest)

```js
// test/eventos.rota.test.js
import { describe, it, expect } from 'vitest'
import request from 'supertest'
import { criarApp } from '../src/app.js'
import { criarRepositorioDeEventosEmMemoria } from '../src/repositories/eventosRepository.memoria.js'

// Sobe a aplicação Express de verdade, mas com o repositório de MEMÓRIA —
// nenhum MySQL precisa estar rodando para este teste passar.
function montarAppDeTeste() {
  const eventosRepository = criarRepositorioDeEventosEmMemoria([
    { id: 1, titulo: 'Semana da Computação', categoria: 'palestra', vagas: 40 },
  ])
  return criarApp({ eventosRepository })
}

describe('rotas de /api/eventos', () => {
  it('GET /api/eventos retorna 200 e o envelope { dados, paginacao }', async () => {
    const app = montarAppDeTeste()
    const resposta = await request(app).get('/api/eventos')

    expect(resposta.status).toBe(200)
    expect(Array.isArray(resposta.body.dados)).toBe(true)
    expect(resposta.body.dados).toHaveLength(1)
    expect(resposta.body.paginacao.total).toBe(1)
  })

  it('GET /api/eventos/:id inexistente retorna 404 no envelope de erro', async () => {
    const app = montarAppDeTeste()
    const resposta = await request(app).get('/api/eventos/999')

    expect(resposta.status).toBe(404)
    expect(resposta.body.erro.mensagem).toMatch(/não encontrado/i)
    expect(resposta.body.erro.codigo).toBe('NAO_ENCONTRADO')
  })

  it('POST /api/eventos sem título retorna 422 (validação zod)', async () => {
    const app = montarAppDeTeste()
    const resposta = await request(app)
      .post('/api/eventos')
      .send({ categoria: 'palestra', vagas: 10 })

    expect(resposta.status).toBe(422)
    expect(resposta.body.erro.detalhes).toBeDefined()
  })

  it('POST /api/eventos válido retorna 201 e o evento criado', async () => {
    const app = montarAppDeTeste()
    const resposta = await request(app)
      .post('/api/eventos')
      .send({ titulo: 'Hackathon FACET', categoria: 'workshop', vagas: 60 })

    expect(resposta.status).toBe(201)
    expect(resposta.body.titulo).toBe('Hackathon FACET')
    expect(resposta.body.id).toBeDefined()
  })
})
```

### 6.4 Teste unitário (service, com repositório falso)

```js
// test/eventos.service.test.js
import { describe, it, expect } from 'vitest'
import { criarServicoDeEventos } from '../src/services/eventosService.js'

// Repositório FALSO (test double): implementa a mesma interface do repositório
// real, mas guarda tudo em um array na memória do próprio teste — zero I/O.
function criarRepositorioFalso(eventosIniciais = []) {
  const eventos = [...eventosIniciais]
  return {
    async listar() {
      return eventos
    },
    async contar() {
      return eventos.length
    },
    async buscarPorId(id) {
      return eventos.find((evento) => evento.id === id) ?? null
    },
    async criar(dados) {
      const novoEvento = { id: eventos.length + 1, ...dados }
      eventos.push(novoEvento)
      return novoEvento
    },
  }
}

describe('eventosService (unitário)', () => {
  it('listarEventos devolve o envelope { dados, paginacao }', async () => {
    const service = criarServicoDeEventos({
      eventosRepository: criarRepositorioFalso([{ id: 1, titulo: 'Evento A' }]),
    })

    const resultado = await service.listarEventos()

    expect(resultado.dados).toHaveLength(1)
    expect(resultado.dados[0].titulo).toBe('Evento A')
    expect(resultado.paginacao).toEqual({ pagina: 1, porPagina: 20, total: 1, totalPaginas: 1 })
  })

  it('buscarEventoPorId lança ErroNaoEncontrado quando o id não existe', async () => {
    const service = criarServicoDeEventos({ eventosRepository: criarRepositorioFalso([]) })

    await expect(service.buscarEventoPorId(42)).rejects.toThrow('não encontrado')
  })

  it('criarEvento lança ErroDeValidacao quando vagas é negativo', async () => {
    const service = criarServicoDeEventos({ eventosRepository: criarRepositorioFalso([]) })

    await expect(
      service.criarEvento({ titulo: 'Evento inválido', categoria: 'palestra', vagas: -5 }),
    ).rejects.toThrow('vagas não pode ser negativo')
  })
})
```

Rodando os testes:

```bash
npm test
```

```text
 RUN  v2.1.9 unieventos-api

 ✓ test/eventos.service.test.js (3 tests) 4ms
 ✓ test/eventos.rota.test.js (4 tests) 29ms

 Test Files  2 passed (2)
      Tests  7 passed (7)
   Start at  20:14:02
   Duration  612ms
```

> **💡 Dica**
> Sete testes cobrindo as regras mais importantes (listar, 404, validação, criação) já dão confiança real para refatorar sem medo. A meta não é "100% de cobertura" — é cobrir os **caminhos de negócio que importam**.

## 7. Migrations de banco

### 7.1 Por que `schema.sql` manual não escala

Até a Aula 09, o banco foi criado rodando um `schema.sql` inteiro na mão. Isso funciona sozinho, mas quebra em equipe: cada pessoa pode ter uma versão diferente do schema local, não há histórico do que mudou e quando, e aplicar uma mudança em produção vira "abrir o MySQL Workbench e rezar". **Migration** resolve isso: cada mudança de schema vira um arquivo numerado, versionado no Git, aplicado em ordem, uma única vez, com registro em uma tabela de controle.

### 7.2 Implementação simples: scripts numerados + tabela de controle

As migrations não inventam um schema novo: elas **reconstroem exatamente o `sql/schema.sql` da Aula 09** (mesmas tabelas, mesmos tamanhos de coluna, mesmas chaves) e, a partir daí, registram como um passo versionado a mudança que a Aula 11 fez à mão no banco. É essa continuidade que permite jogar o `schema.sql` fora sem perder nada.

```sql
-- migrations/0001_criar_tabela_usuarios.sql
CREATE TABLE IF NOT EXISTS usuarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  firebase_uid VARCHAR(128) NOT NULL UNIQUE,
  nome VARCHAR(120) NOT NULL,
  email VARCHAR(160) NOT NULL UNIQUE,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

```sql
-- migrations/0002_criar_tabela_eventos.sql
CREATE TABLE IF NOT EXISTS eventos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  titulo VARCHAR(160) NOT NULL,
  descricao TEXT,
  categoria ENUM('palestra', 'minicurso', 'workshop') NOT NULL,
  data_hora DATETIME NOT NULL,
  local VARCHAR(160) NOT NULL,
  vagas INT NOT NULL DEFAULT 0,
  imagem_url VARCHAR(400),
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_eventos_categoria (categoria),
  INDEX idx_eventos_data_hora (data_hora)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

```sql
-- migrations/0003_criar_tabela_inscricoes.sql
-- versão da Aula 09: a inscrição aponta para a tabela `usuarios`
CREATE TABLE IF NOT EXISTS inscricoes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  evento_id INT NOT NULL,
  usuario_id INT NOT NULL,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_inscricoes_evento FOREIGN KEY (evento_id) REFERENCES eventos(id) ON DELETE CASCADE,
  CONSTRAINT fk_inscricoes_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
  UNIQUE KEY uk_inscricao_unica (evento_id, usuario_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

```sql
-- migrations/0004_inscricao_por_uid_do_firebase.sql
-- A MUDANÇA da Aula 11, agora versionada: com o Firebase como fonte de identidade
-- (Aula 10), a inscrição passa a guardar o uid direto, sem depender da tabela local.
ALTER TABLE inscricoes DROP FOREIGN KEY fk_inscricoes_usuario;
ALTER TABLE inscricoes DROP INDEX uk_inscricao_unica;
ALTER TABLE inscricoes CHANGE COLUMN usuario_id usuario_uid VARCHAR(128) NOT NULL;
ALTER TABLE inscricoes ADD UNIQUE KEY uk_evento_usuario (evento_id, usuario_uid);
```

> **⚠️ Atenção**
> A migration 0004 é destrutiva se rodada num banco com dados reais: os `usuario_id` inteiros viram texto e perdem a ligação com `usuarios`. Em produção, isso viraria três migrations (adicionar a coluna nova, copiar `usuarios.firebase_uid` para ela, só então remover a antiga). Aqui, com banco de desenvolvimento, a versão curta serve — mas **saiba que a versão curta é a exceção, não a regra**.

```js
// scripts/migrar.js
// Executor de migrations minimalista: lê migrations/*.sql em ordem numérica,
// aplica só as que ainda não constam na tabela de controle.
import { readdir, readFile } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'
import mysql from 'mysql2/promise'
import { config } from '../src/config/index.js'

const PASTA_DE_MIGRATIONS = new URL('../migrations', import.meta.url)

async function garantirTabelaDeControle(conexao) {
  await conexao.query(`
    CREATE TABLE IF NOT EXISTS migrations_executadas (
      nome_arquivo VARCHAR(255) PRIMARY KEY,
      executado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB
  `)
}

async function listarMigrationsJaExecutadas(conexao) {
  const [linhas] = await conexao.query('SELECT nome_arquivo FROM migrations_executadas')
  return new Set(linhas.map((linha) => linha.nome_arquivo))
}

async function executarMigracoes() {
  const conexao = await mysql.createConnection({
    host: config.DB_HOST,
    port: config.DB_PORT,
    user: config.DB_USER,
    password: config.DB_PASSWORD,
    database: config.DB_NAME,
    multipleStatements: true,
  })

  try {
    await garantirTabelaDeControle(conexao)
    const jaExecutadas = await listarMigrationsJaExecutadas(conexao)

    const arquivos = (await readdir(PASTA_DE_MIGRATIONS))
      .filter((arquivo) => arquivo.endsWith('.sql'))
      .sort() // nomes numerados (0001_..., 0002_...) garantem ordem correta

    let quantidadeAplicada = 0

    for (const arquivo of arquivos) {
      if (jaExecutadas.has(arquivo)) {
        console.log(`↷ ${arquivo} já aplicada, pulando`)
        continue
      }

      // fileURLToPath, não `.pathname`: no Windows, `new URL(...).pathname` devolve
      // "/C:/Users/..." — com a barra sobrando — e o readFile falha
      const caminhoCompleto = fileURLToPath(new URL(`../migrations/${arquivo}`, import.meta.url))
      const sql = await readFile(caminhoCompleto, 'utf-8')

      console.log(`▶ aplicando ${arquivo}...`)
      await conexao.query(sql)
      await conexao.query('INSERT INTO migrations_executadas (nome_arquivo) VALUES (?)', [arquivo])
      quantidadeAplicada += 1
      console.log(`✔ ${arquivo} aplicada`)
    }

    console.log(`\nConcluído: ${quantidadeAplicada} migration(s) nova(s) aplicada(s).`)
  } finally {
    await conexao.end()
  }
}

executarMigracoes().catch((erro) => {
  console.error('❌ falha ao rodar migrations:', erro.message)
  process.exit(1)
})
```

```json
// package.json — trecho de "scripts"
{
  "scripts": {
    "migrar": "node scripts/migrar.js"
  }
}
```

```bash
npm run migrar
# ▶ aplicando 0001_criar_tabela_eventos.sql...
# ✔ 0001_criar_tabela_eventos.sql aplicada
# ▶ aplicando 0002_criar_tabela_inscricoes.sql...
# ✔ 0002_criar_tabela_inscricoes.sql aplicada
# ▶ aplicando 0003_adicionar_indice_categoria.sql...
# ✔ 0003_adicionar_indice_categoria.sql aplicada
#
# Concluído: 3 migration(s) nova(s) aplicada(s).

npm run migrar
# ↷ 0001_criar_tabela_eventos.sql já aplicada, pulando
# ↷ 0002_criar_tabela_inscricoes.sql já aplicada, pulando
# ↷ 0003_adicionar_indice_categoria.sql já aplicada, pulando
#
# Concluído: 0 migration(s) nova(s) aplicada(s).
```

> **🔎 Por baixo do capô**
> Ferramentas prontas como `node-pg-migrate` (Postgres) ou `umzug` (multi-banco) fazem exatamente isso — tabela de controle + arquivos ordenados — só que com mais recursos (rollback automático, geração de esqueleto de arquivo, migrations em JS além de SQL). Entender o mecanismo manual antes de usar a ferramenta pronta evita tratá-la como caixa-preta.

## 🧩 Padrão de projeto em uso — Builder, Dependency Injection, Singleton, Facade, Repository, Strategy

Esta aula é a mais densa em padrões GoF do semestre, porque a arquitetura em camadas é literalmente a aplicação simultânea de vários deles.

**Dependency Injection** — Seção 2: `criarServicoDeEventos({ eventosRepository })` recebe a dependência em vez de importá-la. O service não conhece a implementação concreta, só a interface (`listar`, `buscarPorId`, `criar`...).

**Singleton** — o pool de conexões do MySQL (criado na Aula 09 com `mysql2.createPool`) é instanciado **uma única vez** por processo e reutilizado por todos os repositórios:
```js
// src/db/pool.js (o mesmo arquivo da Seção 3, visto agora pelo ângulo do padrão)
let instanciaDoPool // módulo ES: só existe uma vez por processo Node — Singleton natural

export function obterPool() {
  if (!instanciaDoPool) {
    instanciaDoPool = mysql.createPool(configuracaoDoPool)
  }
  return instanciaDoPool
}
```
Qualquer repositório que chame `obterPool()` recebe a **mesma** instância — é assim que o Singleton evita esgotar conexões do banco.

**Facade** — `services/eventosService.js` é uma fachada simples sobre o repositório: o controller não precisa saber que, por trás de `criarEvento`, existem validação de negócio e uma chamada ao banco. Ele só vê uma operação de alto nível.

**Repository** — `repositories/eventosRepository.mysql.js` encapsula toda a SQL; o resto da aplicação nunca escreve `SELECT`/`INSERT` fora dessa camada.

**Strategy** — a escolha de **qual** repositório usar em tempo de execução (ver `src/repositories/index.js` na seção "Mão na massa") é o padrão Strategy: a mesma interface (`listar`, `criar`...), implementações intercambiáveis por ambiente (MySQL em produção, memória em teste).

**Builder** — a montagem de uma query de listagem com filtros opcionais (categoria, texto, paginação) usa um builder que acumula condições passo a passo antes de gerar o SQL final — ver `QueryBuilder` no Passo 7 do Mão na massa.

## 💻 Mão na massa — refatorando o `unieventos-api` para arquitetura em camadas

**Passo 1 — instale as dependências novas:**

```bash
cd unieventos-api
npm install zod pino pino-http helmet express-rate-limit dotenv
npm install -D vitest supertest pino-pretty
```

**Passo 2 — crie a estrutura de pastas:**

```bash
mkdir -p src/config src/db src/errors src/middlewares src/repositories src/services src/controllers src/routes src/validators src/utils migrations scripts test
```

**Passo 3 — configuração (já mostrada na Seção 3):**

Copie o conteúdo de `src/config/index.js` e `.env.example` da Seção 3 para o projeto.

**Passo 4 — o pool de conexão (Singleton):**

```js
// src/db/pool.js
import mysql from 'mysql2/promise'
import { config } from '../config/index.js'

let instanciaDoPool

export function obterPool() {
  if (!instanciaDoPool) {
    instanciaDoPool = mysql.createPool({
      host: config.DB_HOST,
      port: config.DB_PORT,
      user: config.DB_USER,
      password: config.DB_PASSWORD,
      database: config.DB_NAME,
      waitForConnections: true,
      connectionLimit: 10,
    })
  }
  return instanciaDoPool
}
```

**Passo 5 — validador de entrada com zod:**

```js
// src/validators/eventoSchema.js
import { z } from 'zod'

export const eventoSchema = z.object({
  titulo: z.string().min(3, 'titulo precisa ter ao menos 3 caracteres').max(150),
  descricao: z.string().max(2000).optional(),
  categoria: z.enum(['palestra', 'minicurso', 'workshop']),
  dataHora: z.string().datetime({ message: 'dataHora precisa ser um ISO 8601 válido' }),
  local: z.string().min(3).max(150),
  vagas: z.coerce.number().int().nonnegative('vagas não pode ser negativo'),
  imagemUrl: z.url().optional(),
})

export const eventoAtualizacaoSchema = eventoSchema.partial()
```

```js
// src/middlewares/validar.js
import { ErroDeValidacao } from '../erros/index.js'

// Middleware genérico: recebe um schema zod e devolve um middleware Express
// que valida req.body antes de deixar a requisição seguir para o controller.
export function validar(schema) {
  return (req, res, next) => {
    const resultado = schema.safeParse(req.body)

    if (!resultado.success) {
      const detalhes = resultado.error.issues.map((problema) => ({
        campo: problema.path.join('.'),
        mensagem: problema.message,
      }))
      throw new ErroDeValidacao('Dados inválidos', detalhes)
    }

    req.body = resultado.data // body validado e com coerções aplicadas (ex.: vagas vira number)
    next()
  }
}
```

**Passo 6 — os erros de domínio:**

Use o conteúdo de `src/erros/index.js` da Seção 4.1.

**Passo 7 — o repositório MySQL (com Builder de query):**

```js
// src/repositories/queryBuilderDeListagem.js
// Builder: monta incrementalmente a query SQL de listagem, adicionando cláusulas
// WHERE só para os filtros que realmente vieram preenchidos.
export class QueryBuilderDeListagem {
  constructor(tabela) {
    this.tabela = tabela
    this.condicoes = []
    this.parametros = []
    this.limiteValor = 20
    this.deslocamentoValor = 0
  }

  comCategoria(categoria) {
    if (categoria) {
      this.condicoes.push('categoria = ?')
      this.parametros.push(categoria)
    }
    return this // encadeamento fluente — marca registrada do Builder
  }

  comBuscaDeTexto(termo) {
    if (termo) {
      this.condicoes.push('titulo LIKE ?')
      this.parametros.push(`%${termo}%`)
    }
    return this
  }

  comPaginacao(pagina = 1, porPagina = 20) {
    this.limiteValor = porPagina
    this.deslocamentoValor = (pagina - 1) * porPagina
    return this
  }

  construir() {
    const clausulaWhere = this.condicoes.length > 0 ? `WHERE ${this.condicoes.join(' AND ')}` : ''
    const sql = `
      SELECT * FROM ${this.tabela}
      ${clausulaWhere}
      ORDER BY data_hora ASC
      LIMIT ? OFFSET ?
    `
    return {
      sql,
      parametros: [...this.parametros, this.limiteValor, this.deslocamentoValor],
    }
  }

  // mesma cláusula WHERE, sem ORDER BY nem paginação — para o `total` do envelope
  construirContagem() {
    const clausulaWhere = this.condicoes.length > 0 ? `WHERE ${this.condicoes.join(' AND ')}` : ''
    return {
      sql: `SELECT COUNT(*) AS total FROM ${this.tabela} ${clausulaWhere}`,
      parametros: [...this.parametros],
    }
  }
}
```

```js
// src/repositories/eventosRepository.mysql.js
import { obterPool } from '../db/pool.js'
import { QueryBuilderDeListagem } from './queryBuilderDeListagem.js'

function linhaParaEvento(linha) {
  return {
    id: linha.id,
    titulo: linha.titulo,
    descricao: linha.descricao,
    categoria: linha.categoria,
    dataHora: linha.data_hora,
    local: linha.local,
    vagas: linha.vagas,
    imagemUrl: linha.imagem_url,
  }
}

export function criarRepositorioDeEventosMySQL() {
  const pool = obterPool()

  return {
    async listar({ categoria, busca, pagina, porPagina } = {}) {
      const { sql, parametros } = new QueryBuilderDeListagem('eventos')
        .comCategoria(categoria)
        .comBuscaDeTexto(busca)
        .comPaginacao(pagina, porPagina)
        .construir()

      const [linhas] = await pool.query(sql, parametros)
      return linhas.map(linhaParaEvento)
    },

    async contar({ categoria, busca } = {}) {
      const { sql, parametros } = new QueryBuilderDeListagem('eventos')
        .comCategoria(categoria)
        .comBuscaDeTexto(busca)
        .construirContagem()

      const [[{ total }]] = await pool.query(sql, parametros)
      return total
    },

    async buscarPorId(id) {
      const [linhas] = await pool.query('SELECT * FROM eventos WHERE id = ?', [id])
      return linhas[0] ? linhaParaEvento(linhas[0]) : null
    },

    async criar(dados) {
      const [resultado] = await pool.query(
        `INSERT INTO eventos (titulo, descricao, categoria, data_hora, local, vagas, imagem_url)
         VALUES (?, ?, ?, ?, ?, ?, ?)`,
        [dados.titulo, dados.descricao ?? null, dados.categoria, dados.dataHora, dados.local, dados.vagas, dados.imagemUrl ?? null],
      )
      return { id: resultado.insertId, ...dados }
    },

    async atualizar(id, dados) {
      await pool.query(
        `UPDATE eventos SET titulo = ?, descricao = ?, categoria = ?, data_hora = ?, local = ?, vagas = ?, imagem_url = ?
         WHERE id = ?`,
        [dados.titulo, dados.descricao ?? null, dados.categoria, dados.dataHora, dados.local, dados.vagas, dados.imagemUrl ?? null, id],
      )
      return this.buscarPorId(id)
    },

    async remover(id) {
      await pool.query('DELETE FROM eventos WHERE id = ?', [id])
    },
  }
}
```

**Passo 8 — o repositório em memória (para testes):**

```js
// src/repositories/eventosRepository.memoria.js
// Implementa a MESMA interface do repositório MySQL, sem tocar em banco algum.
// Usado nos testes (Seção 6.3) e como referência didática de Strategy.
export function criarRepositorioDeEventosEmMemoria(eventosIniciais = []) {
  let eventos = [...eventosIniciais]
  let proximoId = eventos.length + 1

  return {
    async listar({ categoria } = {}) {
      if (!categoria) return eventos
      return eventos.filter((evento) => evento.categoria === categoria)
    },
    async contar({ categoria } = {}) {
      return (await this.listar({ categoria })).length
    },
    async buscarPorId(id) {
      return eventos.find((evento) => evento.id === Number(id)) ?? null
    },
    async criar(dados) {
      const novoEvento = { id: proximoId++, ...dados }
      eventos.push(novoEvento)
      return novoEvento
    },
    async atualizar(id, dados) {
      eventos = eventos.map((evento) => (evento.id === Number(id) ? { ...evento, ...dados } : evento))
      return this.buscarPorId(id)
    },
    async remover(id) {
      eventos = eventos.filter((evento) => evento.id !== Number(id))
    },
  }
}
```

**Passo 9 — Strategy: escolha do repositório por ambiente:**

```js
// src/repositories/index.js
// Strategy: a interface é sempre a mesma (listar/buscarPorId/criar/atualizar/remover);
// a implementação escolhida depende do ambiente de execução.
import { config } from '../config/index.js'
import { criarRepositorioDeEventosMySQL } from './eventosRepository.mysql.js'
import { criarRepositorioDeEventosEmMemoria } from './eventosRepository.memoria.js'

export function obterRepositorioDeEventos() {
  if (config.NODE_ENV === 'test') {
    return criarRepositorioDeEventosEmMemoria()
  }
  return criarRepositorioDeEventosMySQL()
}
```

**Passo 10 — o service (mostrado completo na Seção 2):**

Use `src/services/eventosService.js` da Seção 2, já com a hierarquia de erros da Seção 4.1.

**Passo 11 — o controller:**

```js
// src/controllers/eventosController.js
export function criarControllerDeEventos({ eventosService }) {
  return {
    async listar(req, res) {
      const { categoria, busca, pagina, porPagina } = req.query
      // já vem no envelope { dados, paginacao } montado pelo service
      const resultado = await eventosService.listarEventos({ categoria, busca, pagina, porPagina })
      res.status(200).json(resultado)
    },

    async buscarPorId(req, res) {
      const evento = await eventosService.buscarEventoPorId(Number(req.params.id))
      res.status(200).json(evento)
    },

    async criar(req, res) {
      const evento = await eventosService.criarEvento(req.body)
      res.status(201).json(evento)
    },

    async atualizar(req, res) {
      const evento = await eventosService.atualizarEvento(Number(req.params.id), req.body)
      res.status(200).json(evento)
    },

    async remover(req, res) {
      await eventosService.removerEvento(Number(req.params.id))
      res.status(204).end()
    },
  }
}
```

> **⚠️ Atenção**
> Repare que nenhum método do controller usa `try/catch`. Em Express 5, um erro lançado dentro de um handler `async` é capturado automaticamente e encaminhado ao middleware de erro — não precisamos mais de `.catch(next)` como no Express 4.

**Passo 12 — as rotas:**

```js
// src/routes/eventos.routes.js
import { Router } from 'express'
import { validar } from '../middlewares/validar.js'
import { eventoSchema, eventoAtualizacaoSchema } from '../validators/eventoSchema.js'
import { autenticar } from '../middlewares/autenticar.js'
import { autorizar } from '../middlewares/autorizar.js'

export function criarRotasDeEventos({ eventosController }) {
  const router = Router()

  router.get('/', eventosController.listar)
  router.get('/:id', eventosController.buscarPorId)

  // Rotas de escrita exigem autenticação (middleware da Aula 10) e corpo validado.
  router.post('/', autenticar, validar(eventoSchema), eventosController.criar)
  router.put('/:id', autenticar, validar(eventoAtualizacaoSchema), eventosController.atualizar)
  // exclusão continua exigindo admin, como nas Aulas 10 e 11
  router.delete('/:id', autenticar, autorizar(['admin']), eventosController.remover)

  return router
}
```

**Passo 13 — montando a aplicação:**

```js
// src/app.js
import express from 'express'
import { cabecalhosDeSeguranca, limitadorDeTaxa, corsConfigurado } from './middlewares/seguranca.js'
import { tratadorDeErros } from './middlewares/tratadorDeErros.js'
import { criarRotasDeEventos } from './routes/eventos.routes.js'
import { criarControllerDeEventos } from './controllers/eventosController.js'
import { criarServicoDeEventos } from './services/eventosService.js'
import { obterRepositorioDeEventos } from './repositories/index.js'

export function criarApp({ eventosRepository = obterRepositorioDeEventos() } = {}) {
  const app = express()

  app.use(cabecalhosDeSeguranca)
  app.use(corsConfigurado)
  app.use(limitadorDeTaxa)
  app.use(express.json({ limit: '10kb' }))

  const eventosService = criarServicoDeEventos({ eventosRepository })
  const eventosController = criarControllerDeEventos({ eventosService })

  app.get('/health', (req, res) => {
    res.status(200).json({ status: 'ok' })
  })

  app.use('/api/eventos', criarRotasDeEventos({ eventosController }))

  // O tratador de erros é SEMPRE o último app.use — Express identifica middlewares
  // de erro pela assinatura de 4 parâmetros, não pela posição, mas a convenção
  // de deixá-lo por último evita que ele "capture" middlewares registrados depois.
  app.use(tratadorDeErros)

  return app
}
```

**Passo 14 — o `server.js` (mostrado completo na Seção 4.3). Rode e confira:**

```bash
npm run migrar
npm run dev
curl http://localhost:3000/health
# {"status":"ok"}
```

**Passo 15 — rode os testes:**

```bash
npm test
```

Confira que os 7 testes das Seções 6.3 e 6.4 passam.

### Como testar

A refatoração só terminou quando a API **continua respondendo exatamente o mesmo contrato de antes**. Verifique nesta ordem:

```bash
# 1) migrations aplicadas do zero, em um banco vazio
npm run migrar
```

Resultado esperado: as quatro migrations são aplicadas em ordem e a tabela `migrations_executadas` lista as quatro; rodar `npm run migrar` de novo imprime "já aplicada, pulando" e não altera nada.

```bash
# 2) o contrato de listagem, com o envelope de sempre
curl -s "http://localhost:3000/api/eventos?pagina=1&porPagina=2" | jq
```

Resultado esperado: `{ "dados": [ … ], "paginacao": { "pagina": 1, "porPagina": 2, "total": 3, "totalPaginas": 2 } }`, com os campos em camelCase (`dataHora`, `imagemUrl`).

```bash
# 3) o envelope de erro, idêntico ao da Aula 08
curl -s http://localhost:3000/api/eventos/999 | jq
curl -s -X POST http://localhost:3000/api/eventos -H "Content-Type: application/json" -d '{"titulo":"Ab"}' | jq
```

Resultado esperado: `404` com `{ "erro": { "mensagem": "Evento 999 não encontrado", "codigo": "NAO_ENCONTRADO" } }` e `422` com `codigo: "VALIDACAO"` mais o array `detalhes`.

4. **Configuração** — remova `DB_PASSWORD` do `.env` e rode `npm run dev`. Resultado esperado: o processo **não sobe**, e a mensagem diz qual variável falta.
5. **Front intacto** — suba o `unieventos-web` da Aula 11 contra esta API refatorada e repita o CRUD pela tela. Resultado esperado: tudo funciona sem uma linha alterada no front. Esse é o teste real da refatoração: por fora, nada mudou.
6. **Testes** — `npm test` passa com o MySQL **desligado**, porque a suíte usa o repositório em memória.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Preveja a resposta (status e corpo) de `POST /api/eventos` com o corpo `{ "titulo": "Ab", "categoria": "show", "vagas": "10" }`, passando pelo `validar(eventoSchema)` do Passo 5. Quais campos aparecem em `detalhes`? Por que `vagas` **não** aparece, mesmo tendo chegado como string?

**A2.** Complete a lacuna e diga o status HTTP e o nível de log (`warn` ou `error`) que o `tratadorDeErros` vai produzir:

```js
const jaInscrito = await inscricoesRepository.existeInscricao(eventoId, usuarioUid)
if (jaInscrito) {
  throw new ________('Você já está inscrito neste evento')
}
```

**A3.** Verdadeiro ou falso, com justificativa: "Em produção (`NODE_ENV=production`), o `tratadorDeErros` nunca devolve `erro.message` ao cliente."

**A4.** Em duas linhas: por que `test/eventos.rota.test.js` sobe a aplicação Express inteira e ainda assim não precisa de MySQL rodando? Aponte o parâmetro que torna isso possível.

**A5.** Classifique cada trecho na camada certa (`routes`, `controllers`, `services`, `repositories`, `middlewares`) e justifique em uma linha: (a) `if (inscritos > 0) throw new ErroDeConflito(...)`; (b) `res.status(204).end()`; (c) `LIMIT ? OFFSET ?`; (d) `req.body = resultado.data`; (e) `router.put('/:id', autenticar, ...)`.

**A6.** Você rodou `npm run migrar` e as três migrations foram aplicadas. Depois editou `0002_criar_tabela_inscricoes.sql` para acrescentar uma coluna e rodou `npm run migrar` de novo. O que o script imprime, e o que acontece com a coluna? Qual é o jeito certo de fazer essa mudança?

### Nível B — Aplicação

**B1.** Refatore seu projeto autoral para a arquitetura em camadas — crie as pastas `config/`, `db/`, `erros/`, `middlewares/`, `repositories/`, `services/`, `controllers/`, `routes/`, mova o código existente para os lugares certos.

Resultado esperado: `npm run dev` continua funcionando, e nenhuma rota importa o pool do banco diretamente.

<details markdown="1">
<summary>Dica</summary>

Comece de dentro para fora: primeiro extraia o repositório (funções que tocam o banco), depois o service (regra de negócio), depois o controller (o que sobrar do handler antigo).
</details>

**B2.** Centralize a configuração com zod — crie `src/config/index.js` validando pelo menos 4 variáveis do seu `.env`.

Resultado esperado: remover uma variável obrigatória do `.env` faz o processo falhar ao iniciar, com mensagem clara.

<details markdown="1">
<summary>Dica</summary>

Use `safeParse`, não `parse` — assim você controla a mensagem de erro antes de chamar `process.exit(1)`.
</details>

**B3.** Implemente a hierarquia de erros e o tratador central no seu projeto, substituindo `throw new Error(...)` genérico por `ErroDeValidacao`, `ErroNaoEncontrado` etc.

Resultado esperado: uma requisição a um recurso inexistente devolve `404` com `{ "erro": { "mensagem": "...", "codigo": "NAO_ENCONTRADO" } }`, sem stack trace em produção.

<details markdown="1">
<summary>Dica</summary>

Simule produção localmente com `NODE_ENV=production npm start` e confira que a resposta de erro não tem o campo `stack`.
</details>

**B4.** Escreva 3 testes automatizados — pelo menos um de rota (supertest) e um de service (unitário, repositório falso).

Resultado esperado: `npm test` mostra os 3 testes passando.

<details markdown="1">
<summary>Dica</summary>

Copie a estrutura dos testes das Seções 6.3/6.4 e troque `eventos` pela entidade do seu domínio.
</details>

**B5.** Adicione `helmet`, `express-rate-limit` e CORS restritivo ao seu `app.js`.

Resultado esperado: uma requisição de origem diferente da configurada em `CORS_ORIGEM_PERMITIDA` é bloqueada pelo navegador (verifique no console do DevTools).

<details markdown="1">
<summary>Dica</summary>

Teste abrindo o front em uma porta e fazendo uma requisição para a API configurada com outra origem em `CORS_ORIGEM_PERMITIDA` — o erro de CORS aparece no console do navegador, não no Postman (Postman ignora CORS).
</details>

### Nível C — Desafio

**C1.** Service de inscrições com injeção de dependência e testes sem banco. Escreva `criarServicoDeInscricoes({ inscricoesRepository, eventosRepository })` com quatro regras: evento inexistente (`ErroNaoEncontrado`), evento lotado (`ErroDeConflito`), já inscrito (`ErroDeConflito`) e cancelamento por quem não é dono (`ErroDeAutorizacao`). Cubra cada regra com um teste unitário usando repositórios falsos e escreva um teste de rota para `POST /api/inscricoes` — que hoje é impossível sem Firebase, porque `autenticar` é importado direto dentro de `criarRotasDeInscricoes`. Resolva isso sem tocar no Firebase.

Resultado esperado: `npm test` mostra 5 testes novos passando (4 unitários + 1 de rota) com MySQL e Firebase desligados; o teste de rota confirma `201` com token "válido" e `401` sem token.

<details markdown="1">
<summary>Dica</summary>

A mesma técnica do repositório vale para o middleware: `criarRotasDeInscricoes({ inscricoesController, autenticar = autenticarReal })`. No teste, injete `(req, res, next) => { req.usuario = { uid: 'uid-teste' }; next() }` para o caso `201`, e um que responde `res.status(401).json({ erro: { mensagem: 'Token ausente', codigo: 'NAO_AUTENTICADO' } })` para o outro. `criarApp` precisa repassar esse parâmetro até as rotas.
</details>

## 🏆 Desafios

### ⭐ A ordem que quebra tudo
Tags: express, middleware, bug, testes

Um colega reorganizou o `app.js` "para ficar mais legível" e agora os testes de rota falham de um jeito curioso: `POST /api/eventos` válido devolve `422` dizendo que **todos** os campos são obrigatórios, e `GET /api/eventos/999` devolve uma página HTML em vez de `{ "erro": { "mensagem": "..." } }`. Este é o arquivo:

```js
// src/app.js — versão com os bugs plantados
export function criarApp({ eventosRepository = obterRepositorioDeEventos() } = {}) {
  const app = express()

  app.use(cabecalhosDeSeguranca)
  app.use(corsConfigurado)
  app.use(tratadorDeErros)

  const eventosService = criarServicoDeEventos({ eventosRepository })
  const eventosController = criarControllerDeEventos({ eventosService })

  app.use('/api/eventos', criarRotasDeEventos({ eventosController }))

  app.use(limitadorDeTaxa)
  app.use(express.json({ limit: '10kb' }))

  return app
}
```

Rode `npm test` antes de mexer em qualquer coisa: os testes já contam a história inteira.

**Critérios de pronto**

- Os 7 testes da aula voltam a passar sem alterar nenhum teste.
- Um comentário acima de cada `app.use` explica **por que** ele está naquela posição (o que ele precisa que já tenha acontecido, e quem depende dele).
- Você descobre e anota o valor de `req.body` que chegava ao `validar()` na versão bugada — e por que o Express 5 se comporta assim.
- Uma frase liga o problema ao padrão Chain of Responsibility da seção "Padrão de projeto em uso".

<details markdown="1">
<summary>Pistas</summary>

1. No Express 5, `req.body` é `undefined` enquanto nenhum parser rodou — e `safeParse(undefined)` reclama de tudo.
2. Um middleware de erro só captura erros de quem foi registrado **antes** dele na cadeia.
3. O `limitadorDeTaxa` depois das rotas nunca é alcançado por uma requisição que já foi respondida — confira com `curl -i` que o cabeçalho `RateLimit-Limit` sumiu.
</details>

### ⭐⭐ Rate limit que não pune todo mundo por igual
Tags: express, middleware, seguranca, testes

Em uma rede compartilhada — um laboratório, um escritório, ou até um provedor com NAT/CGNAT — várias pessoas saem para a internet pelo mesmo IP. Com `limit: 100` por IP a cada 15 minutos, bastam quatro pessoas testando a mesma API publicada para a quinta receber `429` sem ter feito nada. Meça o problema e depois redesenhe o limitador para punir quem abusa — não quem compartilha a rede.

**Critérios de pronto**

- Um script `scripts/estressar.sh` faz 101 requisições a `GET /health` em sequência e mostra, com `curl -i`, os cabeçalhos `RateLimit-Limit`/`RateLimit-Remaining` caindo até o `429`.
- Leituras públicas (`GET`) têm um limite folgado; escritas (`POST`/`PUT`/`DELETE`) têm um limite apertado e separado.
- Em rotas autenticadas, a chave do limitador é o `uid` do usuário, não o IP — dois usuários no mesmo IP têm cotas independentes.
- Um teste com `supertest` prova que a 21ª escrita seguida do mesmo usuário recebe `429` com `{ erro: { mensagem, codigo } }` em JSON, e o limitador é injetável (o resto da suíte não pode passar a falhar por causa dele).
- O README explica o que muda quando a API está atrás de um proxy (Render, Nginx) e o que `app.set('trust proxy', ...)` tem a ver com isso.

<details markdown="1">
<summary>Pistas</summary>

1. `express-rate-limit` aceita várias instâncias com configurações diferentes; aplique cada uma com `router.use` ou por método, não só com `app.use` global.
2. A opção `keyGenerator: (req) => req.usuario?.uid ?? req.ip` resolve a chave — mas só funciona se o limitador rodar **depois** de `autenticar`.
3. Para os testes, deixe `criarApp` aceitar `{ limitadores }` e injete instâncias com `limit` baixo (e `windowMs` curto) só no teste que verifica o `429`.
4. Atrás de um proxy, `req.ip` é o IP do proxy até você configurar `trust proxy`; a documentação do `express-rate-limit` tem uma seção inteira sobre isso.
</details>

### ⭐⭐ Supabase como repositório — do lado certo da chave
Tags: supabase, padroes-de-projeto, node, refatoracao

Na Aula 12 a `service_role` era proibida porque o código rodava no navegador. Aqui é diferente: o back-end é um ambiente de servidor, e a chave pode ficar no `.env`. Implemente `criarRepositorioDeEventosSupabase()` com a **mesma interface** dos repositórios MySQL e memória, e escolha entre os três por configuração — sem que service, controller ou testes percebam a troca. Depois responda: se o RLS não se aplica à `service_role`, quem passa a garantir "só o dono edita"?

**Critérios de pronto**

- `config/index.js` valida `DB_PROVIDER` (`mysql` ou `supabase`) e, quando for `supabase`, exige `SUPABASE_URL` e `SUPABASE_SERVICE_ROLE_KEY`.
- `repositories/index.js` (Strategy) devolve a implementação certa; os 7 testes da aula continuam passando sem alteração.
- `listar` com filtros (`categoria`, `busca`, paginação) funciona nos dois provedores e devolve objetos com o **mesmo formato** (`dataHora`, `imagemUrl` — o mapeamento de nomes de coluna é responsabilidade do repositório).
- Um ADR curto registra a decisão: regra de negócio no service (Express) versus policies no banco (Supabase), e por que a chave `service_role` no servidor não repete o erro da Aula 12.
- `.env.example` atualizado, e a chave nunca aparece em log nem em resposta de erro.

<details markdown="1">
<summary>Pistas</summary>

1. `createClient(url, serviceRoleKey, { auth: { persistSession: false } })` — no servidor não há sessão de usuário para persistir.
2. A busca de texto vira `.ilike('titulo', '%' + termo + '%')`; a paginação, `.range(inicio, fim)`; o total vem com `{ count: 'exact' }`.
3. Trate `{ data, error }` dentro do repositório e lance os erros de domínio da seção 4.1 — o service não pode saber que existe Supabase por trás.
4. Os testes já injetam o repositório em memória, então não dependem de `DB_PROVIDER`; se algum passou a falhar, algo vazou de `config` para o service.
</details>

### ⭐⭐⭐ Cobertura que aponta o que falta
Tags: testes, express, seguranca, refatoracao

Sete testes dão confiança — mas confiança em quê, exatamente? Meça: instale `@vitest/coverage-v8`, rode `npx vitest run --coverage` e olhe o relatório linha a linha. Você vai descobrir que `remover`, `atualizar`, o `413` do limite de payload, o `403` e o `409` nunca foram exercitados. Leve `services/` e `controllers/` a pelo menos 90% de cobertura — e faça isso sem transformar a suíte em algo que precisa de MySQL, Firebase ou de um relógio de 15 minutos.

**Critérios de pronto**

- `npm run test:cobertura` gera o relatório e falha se `services/` ou `controllers/` ficarem abaixo de 90% de linhas.
- Testes novos cobrem: `PUT`/`DELETE` felizes e com `404`; `409` de inscrição duplicada; `403` de cancelamento alheio; `413` para corpo maior que `10kb`; `400` para JSON malformado.
- Rotas autenticadas são testadas com um `autenticar` injetado (Nível C do laboratório), nunca com token real do Firebase.
- A suíte inteira roda em menos de 5 segundos e não depende de variável de ambiente além de `NODE_ENV=test`.
- Um trecho no README explica, em três frases, por que 90% não significa "sem bugs" — com um exemplo real de linha coberta que ainda poderia estar errada.

<details markdown="1">
<summary>Pistas</summary>

1. `coverage.thresholds` no `vitest.config.js` (procure "coverage thresholds" na documentação do Vitest) faz o comando falhar abaixo da meta.
2. Para o `413`, `request(app).post('/api/eventos').set('Content-Type', 'application/json').send('x'.repeat(11 * 1024))` basta — o Express responde antes de chegar ao controller.
3. JSON malformado é `.send('{ "titulo": ')` com o mesmo `Content-Type`; observe qual status e qual `mensagem` o seu `tratadorDeErros` devolve hoje (o erro do parser não é "operacional") e decida se é o certo.
4. O `limitadorDeTaxa` em memória compartilha estado entre testes do mesmo processo — injete um limitador com `limit` alto (ou desative em `NODE_ENV=test`) para que a cobertura não passe a falhar por `429`.
</details>

## 🐛 Erros comuns e como resolver

| Sintoma | Causa | Solução |
|---|---|---|
| Processo não inicia, imprime lista de variáveis faltando | `.env` incompleto em relação ao schema de `config/index.js` | Copie `.env.example` para `.env` e preencha todos os campos |
| `TypeError: eventosRepository.listar is not a function` | Repositório injetado não implementa a interface esperada pelo service | Confira se toda implementação de repositório (MySQL, memória) expõe os mesmos métodos |
| Teste de rota falha com erro de conexão ao MySQL | Testes estão usando o repositório real em vez do de memória | Injete `eventosRepository: criarRepositorioDeEventosEmMemoria()` explicitamente no `criarApp` dos testes |
| Erro 500 aparece no navegador com stack trace completo | `NODE_ENV` não está definido como `production` no deploy | Configure `NODE_ENV=production` nas variáveis de ambiente do serviço de deploy |
| `npm run migrar` reaplica uma migration já aplicada | Tabela `migrations_executadas` não foi criada ou o nome do arquivo mudou | Confira `SELECT * FROM migrations_executadas` e não renomeie arquivos de migration já aplicados |
| CORS bloqueando o front mesmo em desenvolvimento | `CORS_ORIGEM_PERMITIDA` no `.env` não bate com a porta real do Vite (`5173` por padrão) | Ajuste a variável para a URL exata mostrada pelo `npm run dev` do front |

## 🏠 Para praticar depois da aula (1 h)

1. No projeto autoral, garanta que **os 5 endpoints principais** (listar, buscar por id, criar, atualizar, remover) passam pela arquitetura em camadas completa.
2. Escreva testes cobrindo **pelo menos 40% dos métodos do service principal** (liste no README quais foram testados e por quê).
3. Aplique o checklist de segurança da Seção 5: `helmet`, rate limit, CORS restritivo, limite de payload — cole no README um trecho de log ou print mostrando o `RateLimit-Limit` no cabeçalho de resposta.
4. Rode `npm test` e cole a saída completa no README, em uma seção "Testes".

**Critério de pronto:** `npm test` passa localmente, README atualizado com a seção de testes e o checklist de segurança marcado.

## ✅ Checkpoint do projeto autoral

Ao final desta aula, seu repositório `<tema>-api` deve ter:

- [ ] Estrutura `routes/ → controllers/ → services/ → repositories/ → db/` completa, com `middlewares/`, `validators/`, `utils/`, `config/`.
- [ ] `src/config/index.js` validando o `.env` com zod e falhando rápido se algo faltar.
- [ ] Hierarquia de erros de domínio e tratador central mapeando para status HTTP.
- [ ] `helmet`, `express-rate-limit` e CORS restritivo configurados.
- [ ] Pelo menos 3 testes automatizados passando (`npm test`).
- [ ] Pasta `migrations/` com scripts numerados e script `npm run migrar` funcional.

## 📚 Para aprofundar

- [Documentação oficial do Express 5](https://expressjs.com/en/guide/error-handling.html) — tratamento de erros.
- [Zod — documentação oficial](https://zod.dev)
- [Pino — documentação oficial](https://getpino.io)
- [Vitest — documentação oficial](https://vitest.dev)
- [Supertest — repositório no GitHub](https://github.com/forwardemail/supertest)
- [OWASP Top 10 (2021, referência atual)](https://owasp.org/Top10/)
- [helmet.js — documentação](https://helmetjs.github.io)
- Martin, Robert C. — *Clean Architecture* (capítulos sobre a regra de dependência), referência complementar da bibliografia do plano de curso.

**Na Aula 14** documentamos a API inteira com OpenAPI 3 e Swagger UI — cada endpoint que construímos até aqui ganha um contrato formal, testável direto do navegador. Traga o `unieventos-api` (ou seu projeto autoral) já na arquitetura em camadas desta aula.
