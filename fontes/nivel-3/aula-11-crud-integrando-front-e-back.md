# Aula 11 — Integrando front-end com back-end: CRUD

> **Nível 3 — Frameworks Modernos** · Unidade 3: Integração front-end/back-end
> WebLab · UNEMAT Sinop · Prof. Ivan Luiz Pedroso Pires
> **Carga:** 3 aulas de 50 min (presencial) + 1 h (assíncrona)

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Documentar um contrato de API em tabela, cobrindo os 5 endpoints de um recurso CRUD.
- Completar a camada controller → service → repository com regras de negócio, paginação e busca.
- Construir uma camada `services/` no front alinhada exatamente ao contrato da API.
- Implementar uma store Pinia de domínio com estados de lista, item atual, carregamento e erro.
- Diferenciar atualização otimista de pessimista e justificar a escolha da pessimista para o projeto.
- Construir telas de listagem, formulário (criar/editar na mesma tela) e confirmação de exclusão em Vuetify.
- Depurar uma integração front-back usando a aba Network do DevTools e reproduzir requisições em `curl`.

## 📋 Pré-requisitos desta aula

Na Aula 10 o UniEventos passou a exigir token do Firebase para escrever dados, e a API passou a validar esse token com `firebase-admin`. Todas as peças já existem separadas: Vue no front, Express no back, MySQL persistindo, Firebase autenticando. Hoje é a aula de **fechar o ciclo** — o CRUD completo de eventos, ponta a ponta, com as duas pontas conversando por um contrato bem definido.

Checklist antes de começar:

- [ ] `unieventos-api` com autenticação Firebase funcionando (Aula 10) e CRUD básico de eventos no MySQL (Aula 09).
- [ ] `unieventos-web` com Pinia, Vue Router, Vuetify e `authStore` funcionando (Aulas 05–10).
- [ ] MySQL rodando localmente com a tabela `eventos` criada.
- [ ] `unieventos-api` e `unieventos-web` rodando em portas diferentes (ex.: `3000` e `5173`) — vamos revisitar CORS.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Contrato de API; completar back-end (validação, regras de negócio, paginação, busca) |
| 2 | 50 min | `eventosService.js`, `eventosStore.js`, atualização otimista × pessimista, telas de listagem e formulário |
| 3 | 50 min | Upload de imagem; depuração ponta a ponta (Network, `curl`, CORS); laboratório |

## 1. Contrato de API: o acordo entre as duas pontas

Antes de escrever uma linha de código de integração, front e back precisam concordar sobre um **contrato**: para cada endpoint, qual método HTTP, qual caminho, o que vai no corpo da requisição, o que volta na resposta, quais status e se exige autenticação. É esse contrato — não o código de um lado ou de outro — que permite que duas pessoas (ou você, em momentos diferentes) trabalhem em front e back sem precisar ler o código um do outro toda hora.

**Contrato do recurso `evento`:**

| Método | Caminho | Autenticação |
|---|---|---|
| GET | `/api/eventos` | Pública |
| GET | `/api/eventos/:id` | Pública |
| POST | `/api/eventos` | Autenticado |
| PUT | `/api/eventos/:id` | Autenticado |
| PATCH | `/api/eventos/:id` | Autenticado |
| DELETE | `/api/eventos/:id` | Admin |

Detalhando corpo e resposta de cada um:

**`GET /api/eventos`** — lista paginada, com filtros por query string.

Query string: `?pagina=1&porPagina=10&busca=semana&categoria=palestra`

```json
{
  "dados": [
    {
      "id": 1,
      "titulo": "Semana da Computação",
      "descricao": "Palestras e minicursos de tecnologia",
      "categoria": "palestra",
      "dataHora": "2030-12-01T19:00:00.000Z",
      "local": "Auditório Central",
      "vagas": 80,
      "vagasDisponiveis": 62,
      "imagemUrl": "https://storage.unieventos.dev/eventos/semana-computacao.jpg"
    }
  ],
  "paginacao": { "pagina": 1, "porPagina": 10, "total": 34, "totalPaginas": 4 }
}
```

Status: `200 OK`.

> **⚠️ Atenção — camelCase no JSON, snake_case no banco**
> As colunas do MySQL são `data_hora` e `imagem_url` (Aula 09), mas o JSON que a API troca com o front é `dataHora` e `imagemUrl`, **camelCase, desde a Aula 06**. Quem traduz é o repositório, com uma função `linhaParaEvento` — e só ele. Se você deixar o `SELECT *` vazar os nomes de coluna para a resposta, o formulário do Passo 3 grava campo errado e a tela mostra "Invalid Date" sem erro nenhum no console.

**`GET /api/eventos/:id`** — um evento. Status `200 OK` ou `404 Not Found` com `{ "erro": { "mensagem": "Evento não encontrado.", "codigo": "NAO_ENCONTRADO" } }`.

**`POST /api/eventos`** — corpo:

```json
{
  "titulo": "Semana da Computação",
  "descricao": "Palestras e minicursos de tecnologia",
  "categoria": "palestra",
  "dataHora": "2030-12-01T19:00:00",
  "local": "Auditório Central",
  "vagas": 80,
  "imagemUrl": "https://storage.unieventos.dev/eventos/semana-computacao.jpg"
}
```

Resposta: o evento criado, com `id`, status `201 Created`. Erros de validação: `422 Unprocessable Entity` com `{ "erro": { "mensagem": "...", "codigo": "VALIDACAO", "detalhes": [...] } }` — o mesmo envelope de erro da Aula 08. Sem token: `401`.

**`PUT /api/eventos/:id`** — **o corpo completo**, exatamente o mesmo esquema do `POST` (é o que "substituir o recurso inteiro" significa; para atualização parcial existe o `PATCH`, da Aula 09). Resposta: o evento atualizado, `200 OK`. Sem token: `401`. Não é dono nem admin: decisão de negócio do projeto (aqui, qualquer autenticado pode editar — o desafio ⭐⭐ desta aula fecha essa brecha). Evento inexistente: `404`.

**`PATCH /api/eventos/:id`** — herdado da Aula 09: corpo com **apenas os campos que mudam**, validado pelo `esquemaEventoParcial`. Resposta: o evento atualizado, `200 OK`. Mesmos códigos de erro do `PUT`.

**`DELETE /api/eventos/:id`** — sem corpo. Resposta: `204 No Content`. Sem token: `401`. Sem ser admin: `403`. Evento com inscritos: `409 Conflict` com `{ "erro": { "mensagem": "Não é possível excluir evento com inscritos.", "codigo": "CONFLITO" } }`.

Todo erro, em qualquer endpoint, sai no envelope único `{ "erro": { "mensagem", "codigo" } }` fixado na Aula 08 — com um `detalhes` extra quando a falha é de validação. O front nunca precisa adivinhar a forma de uma resposta de erro.

> **💡 Dica**
> Escreva esse contrato **antes** de codificar, mesmo sozinho. Ele vira a fonte da verdade quando front e back divergem — e em equipes reais costuma virar um arquivo OpenAPI/Swagger, que veremos na Aula 14. Por ora, uma tabela em Markdown já resolve.

> **🧠 Você sabia?**
> A sigla CRUD não nasceu na web. Ela foi popularizada por James Martin em 1983, no livro *Managing the Data-base Environment*, para descrever as quatro operações básicas sobre um registro. Quarenta anos depois, virou o mapa dos verbos HTTP — `POST`, `GET`, `PUT`/`PATCH`, `DELETE` — e o esqueleto de praticamente toda API REST, inclusive a que você está fechando hoje.

## 2. Back-end: completando controller → service → repository

Revisamos a estrutura da Aula 09 e adicionamos: validação com zod, regras de negócio, paginação e busca.

### 2.1 Repository — só acesso a dados, sem regra de negócio

Duas mudanças em relação à Aula 09, ambas declaradas de propósito antes do código.

**1. Os nomes das funções encurtam.** Como o arquivo já se chama `eventosRepository.js`, repetir "Evento" em cada função é redundante: `listarEventos` vira `listar`, `buscarEventoPorId` vira `buscarPorId`, `inserirEvento` vira `criar`, `substituirEvento` vira `atualizar`, `excluirEvento` vira `remover`. É uma renomeação mecânica — troque os nomes no repositório e no service, e o resto da aplicação nem percebe. O caminho do pool **não** muda: continua `src/bancoDeDados.js`, como na Aula 09.

**2. `vagas` passa a ser capacidade total, não vagas restantes.** Na Aula 09, inscrever alguém fazia `UPDATE eventos SET vagas = vagas - 1`: o contador era mantido à mão, e qualquer inscrição perdida ou revertida deixava o número errado para sempre. A partir de agora, `eventos.vagas` guarda a **capacidade** do evento (um número que só muda quando o organizador edita), e a disponibilidade é **derivada** por consulta: `vagas - COUNT(inscricoes)`. Dado derivado nunca "desincroniza" — é sempre calculado a partir da fonte da verdade, que são as linhas de `inscricoes`.

A migração do banco da Aula 09 para esse modelo, para rodar uma única vez:

```sql
-- 1) devolve a `vagas` o valor de capacidade (vagas restantes + inscritos já feitos)
UPDATE eventos e
SET e.vagas = e.vagas + (SELECT COUNT(*) FROM inscricoes i WHERE i.evento_id = e.id);

-- 2) a inscrição passa a ser identificada pelo uid do Firebase (Aula 10),
--    não mais por um id inteiro da tabela `usuarios`
ALTER TABLE inscricoes DROP FOREIGN KEY fk_inscricoes_usuario;
ALTER TABLE inscricoes CHANGE COLUMN usuario_id usuario_uid VARCHAR(128) NOT NULL;
ALTER TABLE inscricoes ADD CONSTRAINT uq_inscricao UNIQUE (evento_id, usuario_uid);
```

> **⚠️ Atenção**
> Rode o passo 1 **antes** de qualquer coisa e só uma vez: rodar duas vezes soma os inscritos de novo e infla a capacidade. Se o seu banco de desenvolvimento estiver vazio de inscrições, os dois números coincidem e nada muda — o que é o caso mais provável em sala.

```js
// unieventos-api/src/repositories/eventosRepository.js
import { pool } from '../bancoDeDados.js'
import { ErroHttp, erroNaoEncontrado } from '../erros/ErroHttp.js'

// tradução única entre o vocabulário do banco (snake_case) e o da API (camelCase)
function linhaParaEvento(linha) {
  return {
    id: linha.id,
    titulo: linha.titulo,
    descricao: linha.descricao,
    categoria: linha.categoria,
    dataHora: linha.data_hora,
    local: linha.local,
    vagas: linha.vagas,
    vagasDisponiveis: linha.vagas_disponiveis,
    imagemUrl: linha.imagem_url,
  }
}

export async function listar({ pagina, porPagina, busca, categoria }) {
  const offset = (pagina - 1) * porPagina
  const condicoes = []
  const parametros = []

  if (busca) {
    condicoes.push('(titulo LIKE ? OR descricao LIKE ?)')
    parametros.push(`%${busca}%`, `%${busca}%`)
  }
  if (categoria) {
    condicoes.push('categoria = ?')
    parametros.push(categoria)
  }

  const clausulaWhere = condicoes.length > 0 ? `WHERE ${condicoes.join(' AND ')}` : ''

  const [linhas] = await pool.query(
    `SELECT e.*, (e.vagas - COALESCE(COUNT(i.id), 0)) AS vagas_disponiveis
     FROM eventos e
     LEFT JOIN inscricoes i ON i.evento_id = e.id
     ${clausulaWhere}
     GROUP BY e.id
     ORDER BY e.data_hora ASC
     LIMIT ? OFFSET ?`,
    [...parametros, porPagina, offset],
  )

  const [[{ total }]] = await pool.query(
    `SELECT COUNT(*) AS total FROM eventos e ${clausulaWhere}`,
    parametros,
  )

  return { linhas: linhas.map(linhaParaEvento), total }
}

export async function buscarPorId(id) {
  const [linhas] = await pool.query(
    `SELECT e.*, (e.vagas - COALESCE(COUNT(i.id), 0)) AS vagas_disponiveis
     FROM eventos e
     LEFT JOIN inscricoes i ON i.evento_id = e.id
     WHERE e.id = ?
     GROUP BY e.id`,
    [id],
  )
  return linhas[0] ? linhaParaEvento(linhas[0]) : null
}

export async function contarInscritos(id, conexao = pool) {
  const [[{ total }]] = await conexao.query(
    'SELECT COUNT(*) AS total FROM inscricoes WHERE evento_id = ?',
    [id],
  )
  return total
}

export async function criar(evento) {
  const [resultado] = await pool.query(
    `INSERT INTO eventos (titulo, descricao, categoria, data_hora, local, vagas, imagem_url)
     VALUES (?, ?, ?, ?, ?, ?, ?)`,
    [
      evento.titulo,
      evento.descricao,
      evento.categoria,
      evento.dataHora,
      evento.local,
      evento.vagas,
      evento.imagemUrl ?? null,
    ],
  )
  return buscarPorId(resultado.insertId)
}

export async function atualizar(id, evento) {
  await pool.query(
    `UPDATE eventos
     SET titulo = ?, descricao = ?, categoria = ?, data_hora = ?, local = ?, vagas = ?, imagem_url = ?
     WHERE id = ?`,
    [
      evento.titulo,
      evento.descricao,
      evento.categoria,
      evento.dataHora,
      evento.local,
      evento.vagas,
      evento.imagemUrl ?? null,
      id,
    ],
  )
  return buscarPorId(id)
}

export async function remover(id) {
  await pool.query('DELETE FROM eventos WHERE id = ?', [id])
}

// ATENÇÃO: esta função está DELIBERADAMENTE incompleta — ela abre a transação,
// trava a linha e confere as vagas, mas ainda não insere a inscrição. Completá-la
// (e expor o endpoint) é o Laboratório C1 desta aula.
export async function verificarVagaEInscrever(id, usuarioUid) {
  // Transação: ler vagas disponíveis e inserir a inscrição são duas
  // operações que precisam ser atômicas — senão dois usuários podem
  // "ganhar" a última vaga ao mesmo tempo (condição de corrida).
  const conexao = await pool.getConnection()
  try {
    await conexao.beginTransaction()

    const [linhas] = await conexao.query(
      'SELECT vagas, (SELECT COUNT(*) FROM inscricoes WHERE evento_id = ?) AS inscritos FROM eventos WHERE id = ? FOR UPDATE',
      [id, id],
    )

    const evento = linhas[0]
    if (!evento) throw erroNaoEncontrado('Evento não encontrado.')
    if (evento.inscritos >= evento.vagas) {
      throw new ErroHttp(409, 'Não há vagas disponíveis para este evento.', 'SEM_VAGAS')
    }

    // (o Laboratório C1 insere aqui a linha em `inscricoes`, usando esta mesma conexão)

    await conexao.commit()
    return true
  } catch (erro) {
    // um único rollback, no caminho de erro — os `throw` acima caem todos aqui
    await conexao.rollback()
    throw erro
  } finally {
    conexao.release()
  }
}
```

> **🔎 Por baixo do capô**
> `FOR UPDATE` trava a linha lida até o fim da transação, impedindo que outra requisição simultânea leia o mesmo número de vagas antes do commit. Sem isso, duas requisições concorrentes poderiam ambas ler "1 vaga disponível" e ambas inserirem a inscrição, estourando a capacidade do evento.

### 2.2 Service — regras de negócio e validação

```js
// unieventos-api/src/services/eventosService.js
import { z } from 'zod'
import * as eventosRepository from '../repositories/eventosRepository.js'
import { ErroHttp, erroNaoEncontrado } from '../erros/ErroHttp.js'

export const esquemaEvento = z.object({
  titulo: z.string().trim().min(3, 'Título precisa ter ao menos 3 caracteres'),
  descricao: z.string().trim().min(10, 'Descrição precisa ter ao menos 10 caracteres'),
  categoria: z.enum(['palestra', 'minicurso', 'workshop'], {
    message: 'Categoria precisa ser palestra, minicurso ou workshop',
  }),
  dataHora: z
    .string()
    .datetime({ offset: true, message: 'Data e hora em formato ISO inválido' })
    .or(z.string().min(1)) // aceita também "2030-12-01T19:00:00" sem offset
    .refine((valor) => !Number.isNaN(Date.parse(valor)), 'Data e hora inválidas')
    .refine((valor) => new Date(valor).getTime() > Date.now(), 'A data do evento não pode estar no passado'),
  local: z.string().trim().min(3, 'Local precisa ter ao menos 3 caracteres'),
  vagas: z.number().int().positive('Vagas precisa ser um número positivo'),
  imagemUrl: z.url('URL de imagem inválida').optional().or(z.literal('')),
})

export const esquemaEventoParcial = esquemaEvento.partial()

export async function listar({ pagina = 1, porPagina = 10, busca, categoria }) {
  const paginaSegura = Math.max(1, Number(pagina))
  const porPaginaSegura = Math.min(50, Math.max(1, Number(porPagina)))

  const { linhas, total } = await eventosRepository.listar({
    pagina: paginaSegura,
    porPagina: porPaginaSegura,
    busca,
    categoria,
  })

  return {
    dados: linhas,
    paginacao: {
      pagina: paginaSegura,
      porPagina: porPaginaSegura,
      total,
      totalPaginas: Math.ceil(total / porPaginaSegura),
    },
  }
}

export async function buscarPorId(id) {
  const evento = await eventosRepository.buscarPorId(id)
  if (!evento) throw erroNaoEncontrado('Evento não encontrado.')
  return evento
}

export async function criar(dadosBrutos) {
  const dados = esquemaEvento.parse(dadosBrutos)
  return eventosRepository.criar(dados)
}

export async function atualizar(id, dadosBrutos) {
  await buscarPorId(id) // garante 404 antes de tentar validar/atualizar
  // MESMO esquema do POST: PUT substitui o recurso inteiro (ver contrato da §1)
  const dados = esquemaEvento.parse(dadosBrutos)
  return eventosRepository.atualizar(id, dados)
}

export async function atualizarParcial(id, dadosBrutos) {
  const atual = await buscarPorId(id)
  const dados = esquemaEventoParcial.parse(dadosBrutos)
  return eventosRepository.atualizar(id, { ...atual, ...dados })
}

export async function remover(id) {
  await buscarPorId(id)

  const inscritos = await eventosRepository.contarInscritos(id)
  if (inscritos > 0) {
    throw new ErroHttp(409, 'Não é possível excluir evento com inscritos.', 'CONFLITO')
  }

  await eventosRepository.remover(id)
}
```

### 2.3 Controller — só orquestra requisição/resposta

```js
// unieventos-api/src/controllers/eventosController.js
import * as eventosService from '../services/eventosService.js'

export async function listar(req, res) {
  const { pagina, porPagina, busca, categoria } = req.query
  const resultado = await eventosService.listar({ pagina, porPagina, busca, categoria })
  res.json(resultado)
}

export async function buscarPorId(req, res) {
  const evento = await eventosService.buscarPorId(req.params.id)
  res.json(evento)
}

export async function criar(req, res) {
  const evento = await eventosService.criar(req.body)
  res.status(201).json(evento)
}

export async function atualizar(req, res) {
  const evento = await eventosService.atualizar(req.params.id, req.body)
  res.json(evento)
}

export async function atualizarParcial(req, res) {
  const evento = await eventosService.atualizarParcial(req.params.id, req.body)
  res.json(evento)
}

export async function remover(req, res) {
  await eventosService.remover(req.params.id)
  res.status(204).send()
}
```

Sem `try/catch` nos controllers: Express 5 encaminha automaticamente qualquer rejeição de handler `async` para o middleware de erro central, criado na Aula 08. Ele **não muda de envelope** aqui — continua sendo `{ erro: { mensagem, codigo } }`, com `422` para validação. A única adição é reconhecer o `ZodError` que escapa do `esquemaEvento.parse()` dentro do service:

```js
// unieventos-api/src/middlewares/tratadorDeErros.js — o da Aula 08, com um caso a mais
import { ZodError } from 'zod'
import { ErroHttp } from '../erros/ErroHttp.js'

export function tratadorDeErros(err, req, res, next) {
  if (err instanceof ZodError) {
    return res.status(422).json({
      erro: {
        mensagem: 'Dados inválidos.',
        codigo: 'VALIDACAO',
        detalhes: err.issues.map((i) => ({ campo: i.path.join('.'), mensagem: i.message })),
      },
    })
  }

  const status = err instanceof ErroHttp ? err.status : 500
  const codigo = err instanceof ErroHttp ? err.codigo : 'ERRO_INTERNO'
  const mensagem = err instanceof ErroHttp ? err.message : 'Erro interno do servidor'

  if (status === 500) console.error(err)
  res.status(status).json({ erro: { mensagem, codigo } })
}
```

> **⚠️ Atenção**
> Nada de inventar um terceiro formato de erro. `ErroHttp` e o envelope `{ erro: { mensagem, codigo } }` vêm da Aula 08 e valem até o fim da trilha — inclusive na documentação Swagger da Aula 14. Um front que aprendeu a ler `erro.mensagem` uma vez lê para sempre.

### 2.4 Rotas com validação por middleware Zod

Reaproveitando o padrão de validação da Aula 08, com o mesmo esquema completo nos dois pontos em que o `PUT` passa (middleware e service):

```js
// unieventos-api/src/middlewares/validar.js
export function validar(esquema) {
  return (req, res, next) => {
    req.body = esquema.parse(req.body) // lança ZodError, capturado pelo tratadorErros
    next()
  }
}
```

```js
// unieventos-api/src/routes/eventos.routes.js
import { Router } from 'express'
import { autenticar } from '../middlewares/autenticar.js'
import { autorizar } from '../middlewares/autorizar.js'
import { validar } from '../middlewares/validar.js'
import { esquemaEvento, esquemaEventoParcial } from '../services/eventosService.js'
import * as eventosController from '../controllers/eventosController.js'

const router = Router()

router.get('/', eventosController.listar)
router.get('/:id', eventosController.buscarPorId)
router.post('/', autenticar, validar(esquemaEvento), eventosController.criar)
// PUT usa o esquema COMPLETO, o mesmo do POST — é o que o service revalida adiante.
// O esquema parcial é do PATCH (Aula 09), não do PUT.
router.put('/:id', autenticar, validar(esquemaEvento), eventosController.atualizar)
router.patch('/:id', autenticar, validar(esquemaEventoParcial), eventosController.atualizarParcial)
router.delete('/:id', autenticar, autorizar(['admin']), eventosController.remover)

export default router
```

## 3. Front-end: `services/` alinhado ao contrato

```js
// src/services/eventosService.js
import http from './http'

export function listarEventos({ pagina = 1, porPagina = 10, busca = '', categoria = '' } = {}) {
  return http
    .get('/eventos', { params: { pagina, porPagina, busca, categoria } })
    .then((resposta) => resposta.data)
}

export function buscarEvento(id) {
  return http.get(`/eventos/${id}`).then((resposta) => resposta.data)
}

export function criarEvento(evento) {
  return http.post('/eventos', evento).then((resposta) => resposta.data)
}

export function atualizarEvento(id, evento) {
  return http.put(`/eventos/${id}`, evento).then((resposta) => resposta.data)
}

export function removerEvento(id) {
  return http.delete(`/eventos/${id}`)
}
```

> **💡 Dica**
> Repare que cada função do service tem exatamente uma responsabilidade e um nome que espelha o contrato da seção 1. Ninguém que ler esse arquivo precisa saber que por trás existe Axios, interceptors ou token — e é exatamente esse esconderijo que a store vai explorar.

## 4. Store Pinia: estado da lista, item atual e paginação

```js
// src/stores/eventosStore.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as eventosService from '@/services/eventosService'

export const useEventosStore = defineStore('eventos', () => {
  const lista = ref([])
  const itemAtual = ref(null)
  const carregando = ref(false)
  const erro = ref(null)
  const paginacao = ref({ pagina: 1, porPagina: 10, total: 0, totalPaginas: 0 })

  async function carregar({ pagina = 1, porPagina = 10 } = {}) {
    carregando.value = true
    erro.value = null
    try {
      const resultado = await eventosService.listarEventos({ pagina, porPagina })
      lista.value = resultado.dados
      paginacao.value = resultado.paginacao
    } catch (e) {
      erro.value = e.response?.data?.erro?.mensagem ?? 'Não foi possível carregar os eventos.'
    } finally {
      carregando.value = false
    }
  }

  async function buscar({ termo = '', categoria = '', pagina = 1 } = {}) {
    carregando.value = true
    erro.value = null
    try {
      const resultado = await eventosService.listarEventos({
        pagina,
        porPagina: paginacao.value.porPagina,
        busca: termo,
        categoria,
      })
      lista.value = resultado.dados
      paginacao.value = resultado.paginacao
    } catch (e) {
      erro.value = e.response?.data?.erro?.mensagem ?? 'Não foi possível buscar os eventos.'
    } finally {
      carregando.value = false
    }
  }

  async function carregarUm(id) {
    carregando.value = true
    erro.value = null
    try {
      itemAtual.value = await eventosService.buscarEvento(id)
    } catch (e) {
      erro.value = e.response?.data?.erro?.mensagem ?? 'Evento não encontrado.'
    } finally {
      carregando.value = false
    }
  }

  // Atualização PESSIMISTA: só mexemos no estado local depois que o
  // servidor confirmar. Mais lento na percepção do usuário, mas nunca
  // mostra dado que pode não ter sido salvo de fato — ver seção 5.
  async function criar(evento) {
    carregando.value = true
    erro.value = null
    try {
      const novoEvento = await eventosService.criarEvento(evento)
      lista.value = [novoEvento, ...lista.value]
      return novoEvento
    } catch (e) {
      erro.value = e.response?.data?.erro?.mensagem ?? 'Não foi possível criar o evento.'
      throw e
    } finally {
      carregando.value = false
    }
  }

  async function atualizar(id, evento) {
    carregando.value = true
    erro.value = null
    try {
      const eventoAtualizado = await eventosService.atualizarEvento(id, evento)
      const indice = lista.value.findIndex((e) => e.id === Number(id))
      if (indice !== -1) lista.value[indice] = eventoAtualizado
      return eventoAtualizado
    } catch (e) {
      erro.value = e.response?.data?.erro?.mensagem ?? 'Não foi possível atualizar o evento.'
      throw e
    } finally {
      carregando.value = false
    }
  }

  async function remover(id) {
    carregando.value = true
    erro.value = null
    try {
      await eventosService.removerEvento(id)
      lista.value = lista.value.filter((e) => e.id !== Number(id))
    } catch (e) {
      erro.value = e.response?.data?.erro?.mensagem ?? 'Não foi possível excluir o evento.'
      throw e
    } finally {
      carregando.value = false
    }
  }

  return { lista, itemAtual, carregando, erro, paginacao, carregar, buscar, carregarUm, criar, atualizar, remover }
})
```

## 5. Atualização otimista × pessimista

Duas estratégias para refletir uma mudança na interface depois de uma ação do usuário (criar, editar, excluir):

- **Otimista:** a interface muda **imediatamente**, antes da resposta do servidor chegar — assumindo que vai dar certo. Se der errado, é preciso desfazer a mudança local e mostrar um erro. Percepção de velocidade excelente; complexidade de "desfazer" real.
- **Pessimista:** a interface só muda **depois** que o servidor confirmar o sucesso. Mais lenta na percepção (o usuário espera o `carregando`), mas nunca mente sobre o estado — o que a tela mostra é sempre o que o servidor de fato tem salvo.

A store acima implementa a **pessimista** de propósito: cada ação (`criar`, `atualizar`, `remover`) só atualiza `lista.value` depois do `await` na chamada de serviço resolver com sucesso. Para um CRUD acadêmico, essa é a escolha mais segura — evita o cenário em que o aluno vê "Evento criado!" na tela, mas na verdade a validação do back-end rejeitou e nada foi salvo.

> **📌 Na prova**
> Otimista = muda a tela antes de saber o resultado (rápido, mas exige lógica de desfazer). Pessimista = muda a tela só após confirmação do servidor (mais lento, mais seguro). Nesta disciplina, sempre pessimista.

## 6. Upload de imagem do evento com Firebase Storage

Escolhemos Firebase Storage (o front já tem o SDK do Firebase configurado desde a Aula 07/10) para o upload da imagem do evento.

```js
// src/services/storageService.js
import { getStorage, ref as storageRef, uploadBytes, getDownloadURL } from 'firebase/storage'
import { auth } from './firebase'

const storage = getStorage()

export async function enviarImagemEvento(arquivo) {
  if (!auth.currentUser) {
    throw new Error('É preciso estar autenticado para enviar imagens.')
  }

  const nomeUnico = `${Date.now()}-${arquivo.name}`
  const caminho = `eventos/${nomeUnico}`
  const referencia = storageRef(storage, caminho)

  await uploadBytes(referencia, arquivo)
  return getDownloadURL(referencia)
}
```

O trecho abaixo entra no `EventoFormView.vue` que você constrói no Passo 3 do Mão na massa — guarde-o para lá:

```vue
<!-- trecho a adicionar em EventoFormView.vue: campo de upload -->
<script setup>
// os mesmos imports do Passo 3, mais o serviço de storage
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useEventosStore } from '@/stores/eventosStore'
import { enviarImagemEvento } from '@/services/storageService'

const enviandoImagem = ref(false)

async function aoSelecionarImagem(arquivos) {
  // sem `multiple`, o v-file-input emite um File solto; com `multiple`, um array.
  // Normalizar aqui evita o clássico "arquivo é undefined" em um dos dois casos.
  const arquivo = Array.isArray(arquivos) ? arquivos[0] : arquivos
  if (!arquivo) return

  enviandoImagem.value = true
  try {
    form.value.imagemUrl = await enviarImagemEvento(arquivo)
  } catch (e) {
    erroSubmissao.value = 'Falha ao enviar imagem: ' + e.message
  } finally {
    enviandoImagem.value = false
  }
}
</script>

<template>
  <!-- dentro do v-form, antes do botão de submit -->
  <v-file-input
    label="Imagem do evento"
    accept="image/*"
    prepend-icon="mdi-camera"
    :loading="enviandoImagem"
    @update:model-value="aoSelecionarImagem"
  />
  <v-img v-if="form.imagemUrl" :src="form.imagemUrl" max-height="200" class="mb-4" cover />
</template>
```

> **💡 Dica**
> A alternativa é usar `multer` no Express, recebendo o arquivo direto no back-end (`multipart/form-data`) e salvando em disco ou repassando para um storage. É uma escolha igualmente válida — inclusive mais simples de proteger, já que o upload passa pelos seus próprios middlewares de autenticação. A vantagem do Firebase Storage é tirar carga de rede do seu servidor: o arquivo vai direto do navegador para o Firebase, e sua API só recebe a URL final, pequena, no corpo do `POST`/`PUT`.

## 7. Depuração ponta a ponta

Quando o front manda uma requisição e algo dá errado, o fluxo de depuração é sempre o mesmo:

1. **Aba Network do DevTools.** Filtre por Fetch/XHR, clique na requisição. Aba **Headers** mostra método, URL, status. Aba **Payload** (ou **Request**) mostra o corpo enviado. Aba **Response** mostra o corpo devolvido pelo servidor — é aqui que aparece a mensagem de erro do `tratadorErros`.
2. **Reproduza em `curl`.** Copie a requisição do Network (botão direito → Copy → Copy as cURL) ou monte à mão:

```bash
curl -i http://localhost:3000/api/eventos \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "titulo": "Minicurso de Docker",
    "descricao": "Introdução prática a containers",
    "categoria": "minicurso",
    "dataHora": "2030-12-10T14:00:00",
    "local": "Laboratório 3",
    "vagas": 30
  }'
```

Isso isola o problema: se o `curl` reproduz o erro, o problema é no back-end (ou nos dados enviados). Se o `curl` funciona mas o front falha, o problema é no front (token não enviado, payload montado errado, CORS).

3. **Leia os logs do servidor.** O terminal onde `unieventos-api` está rodando mostra qualquer `console.error` do `tratadorErros` e, se usar `morgan` ou similar, cada requisição recebida — confirme que ela chegou, com o método e caminho certos.

### CORS: erros mais comuns e configuração correta

CORS (Cross-Origin Resource Sharing) é uma proteção do **navegador**, não do servidor — ele bloqueia a resposta de chegar ao JavaScript da página quando origem (protocolo + domínio + porta) da página é diferente da origem da API, a menos que o servidor autorize explicitamente via cabeçalhos.

Sintomas típicos no console do navegador:

- `has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present` → o servidor não está usando `cors()`, ou está usando com `origin` que não bate com a URL do front.
- `Request header field authorization is not allowed by Access-Control-Allow-Headers` → o servidor não liberou explicitamente o cabeçalho `Authorization`.
- Requisição aparece como `OPTIONS` seguida de falha → é o *preflight* automático do navegador para métodos como `PUT`/`DELETE` ou cabeçalhos customizados; se o servidor não responde `200`/`204` a esse `OPTIONS`, o navegador cancela a requisição real.

> **🔬 Investigue**
> Com front e API rodando, abra a aba Network, filtre por `eventos` e edite um evento. Você verá **duas** requisições para a mesma URL: um `OPTIONS` e o `PUT`. Clique no `OPTIONS`: qual foi o status e quais cabeçalhos `Access-Control-Allow-*` vieram na resposta? Agora saia da conta e recarregue a lista (um `GET` sem `Authorization`): apareceu algum `OPTIONS` antes dele? A diferença é a definição de "requisição simples" do CORS — `GET` sem cabeçalhos fora da lista segura dispensa o preflight; `PUT` com `Authorization` e `Content-Type: application/json` não.

Configuração correta para o UniEventos:

```js
// unieventos-api/src/servidor.js (trecho)
import express from 'express'
import cors from 'cors'

const app = express()

app.use(
  cors({
    origin: process.env.FRONT_URL ?? 'http://localhost:5173',
    credentials: true,
    allowedHeaders: ['Content-Type', 'Authorization'],
  }),
)

app.use(express.json())
```

> **⚠️ Atenção**
> `origin: '*'` (liberar qualquer origem) parece resolver tudo rápido, mas **não funciona junto com `credentials: true`** — o navegador rejeita essa combinação por especificação. Como o UniEventos usa `Authorization` (não cookies), `credentials: true` nem é estritamente necessário aqui, mas vale registrar: se um dia usar cookies de sessão, `origin` precisa ser um domínio explícito, nunca `*`.

## 🧩 Padrão de projeto em uso — Facade

A camada `services/` do front é um **Facade** (padrão estrutural): oferece uma interface simples (`listarEventos()`, `criarEvento()`) escondendo a complexidade de configurar o Axios, montar query string, tratar cabeçalhos de autenticação e formatar a resposta. A store, os componentes e as views nunca chamam `http.get(...)` diretamente — eles conversam só com o Facade. Se amanhã trocarmos Axios por `fetch` nativo, ou a URL base da API mudar de estrutura, só o `services/` muda; store e telas continuam iguais. Voltaremos a esse mesmo princípio na Aula 12, quando o Adapter permitir trocar Express+MySQL por Supabase sem tocar no front.

## 💻 Mão na massa — telas de CRUD completas

### Passo 1 — Listagem com `v-data-table`, busca e paginação no servidor

```vue
<!-- src/views/EventosListaView.vue -->
<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useEventosStore } from '@/stores/eventosStore'
import { useAuthStore } from '@/stores/authStore'
import DialogoConfirmacao from '@/components/DialogoConfirmacao.vue'

const router = useRouter()
const eventosStore = useEventosStore()
const authStore = useAuthStore()

const termoBusca = ref('')
const opcoesTabela = ref({ page: 1, itemsPerPage: 10 })
const dialogoExclusaoAberto = ref(false)
const eventoParaExcluir = ref(null)
const snackbar = ref({ aberto: false, texto: '', cor: 'success' })

const cabecalhos = [
  { title: 'Título', key: 'titulo' },
  { title: 'Categoria', key: 'categoria' },
  { title: 'Data', key: 'dataHora' },
  { title: 'Vagas', key: 'vagasDisponiveis' },
  { title: 'Ações', key: 'acoes', sortable: false },
]

async function carregarPagina() {
  await eventosStore.buscar({
    termo: termoBusca.value,
    pagina: opcoesTabela.value.page,
  })
}

onMounted(carregarPagina)
watch(() => opcoesTabela.value.page, carregarPagina)

let temporizadorBusca = null
watch(termoBusca, () => {
  clearTimeout(temporizadorBusca)
  // debounce simples: espera 400ms sem digitar antes de buscar de novo
  temporizadorBusca = setTimeout(() => {
    opcoesTabela.value.page = 1
    carregarPagina()
  }, 400)
})

function formatarData(isoString) {
  return new Intl.DateTimeFormat('pt-BR', { dateStyle: 'short', timeStyle: 'short' }).format(new Date(isoString))
}

function abrirNovo() {
  router.push({ name: 'evento-form' })
}

function abrirEdicao(evento) {
  // rota DIFERENTE da de criação: 'evento-form' é /eventos/novo, sem :id
  router.push({ name: 'evento-form-editar', params: { id: evento.id } })
}

function pedirConfirmacaoExclusao(evento) {
  eventoParaExcluir.value = evento
  dialogoExclusaoAberto.value = true
}

async function confirmarExclusao() {
  try {
    await eventosStore.remover(eventoParaExcluir.value.id)
    snackbar.value = { aberto: true, texto: 'Evento excluído com sucesso.', cor: 'success' }
  } catch (e) {
    snackbar.value = { aberto: true, texto: eventosStore.erro ?? 'Erro ao excluir.', cor: 'error' }
  } finally {
    dialogoExclusaoAberto.value = false
  }
}
</script>

<template>
  <v-container>
    <div class="d-flex align-center justify-space-between mb-4">
      <h1 class="text-h4">Eventos</h1>
      <v-btn v-if="authStore.estaLogado" color="primary" prepend-icon="mdi-plus" @click="abrirNovo">
        Novo evento
      </v-btn>
    </div>

    <v-text-field
      v-model="termoBusca"
      label="Buscar por título ou descrição"
      prepend-inner-icon="mdi-magnify"
      clearable
      class="mb-4"
    />

    <v-progress-linear v-if="eventosStore.carregando" indeterminate color="primary" class="mb-2" />

    <v-alert v-if="eventosStore.erro" type="error" class="mb-4">
      {{ eventosStore.erro }}
    </v-alert>

    <v-data-table-server
      v-model:page="opcoesTabela.page"
      v-model:items-per-page="opcoesTabela.itemsPerPage"
      :headers="cabecalhos"
      :items="eventosStore.lista"
      :items-length="eventosStore.paginacao.total"
      :loading="eventosStore.carregando"
      item-value="id"
    >
      <template #item.dataHora="{ item }">
        {{ formatarData(item.dataHora) }}
      </template>

      <template #item.acoes="{ item }">
        <v-btn
          v-if="authStore.estaLogado"
          icon="mdi-pencil"
          size="small"
          variant="text"
          @click="abrirEdicao(item)"
        />
        <v-btn
          v-if="authStore.ehAdmin"
          icon="mdi-delete"
          size="small"
          variant="text"
          color="error"
          @click="pedirConfirmacaoExclusao(item)"
        />
      </template>

      <template #no-data>
        <p class="pa-4">Nenhum evento encontrado.</p>
      </template>
    </v-data-table-server>

    <DialogoConfirmacao
      v-model="dialogoExclusaoAberto"
      titulo="Excluir evento"
      :mensagem="`Tem certeza que deseja excluir '${eventoParaExcluir?.titulo}'? Esta ação não pode ser desfeita.`"
      @confirmar="confirmarExclusao"
    />

    <v-snackbar v-model="snackbar.aberto" :color="snackbar.cor" timeout="4000">
      {{ snackbar.texto }}
    </v-snackbar>
  </v-container>
</template>
```

### Passo 2 — Componente de confirmação reutilizável

```vue
<!-- src/components/DialogoConfirmacao.vue -->
<script setup>
defineProps({
  modelValue: { type: Boolean, required: true },
  titulo: { type: String, default: 'Confirmar ação' },
  mensagem: { type: String, required: true },
})

const emit = defineEmits(['update:modelValue', 'confirmar'])

function cancelar() {
  emit('update:modelValue', false)
}

function confirmar() {
  emit('confirmar')
}
</script>

<template>
  <v-dialog :model-value="modelValue" max-width="420" @update:model-value="$emit('update:modelValue', $event)">
    <v-card>
      <v-card-title>{{ titulo }}</v-card-title>
      <v-card-text>{{ mensagem }}</v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn variant="text" @click="cancelar">Cancelar</v-btn>
        <v-btn color="error" variant="flat" @click="confirmar">Excluir</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
```

### Passo 3 — Formulário único para criar e editar

A mesma tela serve para os dois casos: a rota `/eventos/novo` não tem `:id`, e `/eventos/:id/editar` tem. O componente decide o modo olhando `route.params.id`.

```js
// src/router/index.js — trecho das rotas de evento (adicionar ao array de routes)
{
  path: '/eventos',
  name: 'eventos-lista',
  component: () => import('@/views/EventosListaView.vue'),
},
{
  path: '/eventos/novo',
  name: 'evento-form',
  component: () => import('@/views/EventoFormView.vue'),
  meta: { requerAuth: true },
},
{
  path: '/eventos/:id/editar',
  name: 'evento-form-editar',
  component: () => import('@/views/EventoFormView.vue'),
  meta: { requerAuth: true },
  props: true,
},
```

```vue
<!-- src/views/EventoFormView.vue -->
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useEventosStore } from '@/stores/eventosStore'

const props = defineProps({
  id: { type: [String, Number], default: null },
})

const route = useRoute()
const router = useRouter()
const eventosStore = useEventosStore()

const idEvento = computed(() => props.id ?? route.params.id ?? null)
const ehEdicao = computed(() => idEvento.value !== null)

const form = ref({
  titulo: '',
  descricao: '',
  categoria: 'palestra',
  dataHora: '',
  local: '',
  vagas: 1,
  imagemUrl: '',
})

const categorias = [
  { title: 'Palestra', value: 'palestra' },
  { title: 'Minicurso', value: 'minicurso' },
  { title: 'Workshop', value: 'workshop' },
]

const salvando = ref(false)
const erroSubmissao = ref('')

const regraObrigatorio = (v) => !!v || 'Campo obrigatório'
const regraVagasPositiva = (v) => Number(v) > 0 || 'Vagas precisa ser maior que zero'

onMounted(async () => {
  if (ehEdicao.value) {
    await eventosStore.carregarUm(idEvento.value)
    if (eventosStore.itemAtual) {
      const evento = eventosStore.itemAtual
      form.value = {
        titulo: evento.titulo,
        descricao: evento.descricao,
        categoria: evento.categoria,
        dataHora: evento.dataHora?.slice(0, 16), // ISO -> formato do input datetime-local
        local: evento.local,
        vagas: evento.vagas,
        imagemUrl: evento.imagemUrl ?? '',
      }
    }
  }
})

async function aoSubmeter() {
  erroSubmissao.value = ''
  salvando.value = true
  try {
    const payload = { ...form.value, vagas: Number(form.value.vagas) }
    if (ehEdicao.value) {
      await eventosStore.atualizar(idEvento.value, payload)
    } else {
      await eventosStore.criar(payload)
    }
    router.push({ name: 'eventos-lista' })
  } catch (e) {
    erroSubmissao.value = eventosStore.erro ?? 'Não foi possível salvar o evento.'
  } finally {
    salvando.value = false
  }
}
</script>

<template>
  <v-container>
    <h1 class="text-h4 mb-4">{{ ehEdicao ? 'Editar evento' : 'Novo evento' }}</h1>

    <v-skeleton-loader v-if="eventosStore.carregando && ehEdicao" type="article" />

    <v-form v-else @submit.prevent="aoSubmeter">
      <v-alert v-if="erroSubmissao" type="error" class="mb-4" density="compact">
        {{ erroSubmissao }}
      </v-alert>

      <v-text-field v-model="form.titulo" label="Título" :rules="[regraObrigatorio]" />
      <v-textarea v-model="form.descricao" label="Descrição" :rules="[regraObrigatorio]" />
      <v-select v-model="form.categoria" :items="categorias" label="Categoria" />
      <v-text-field v-model="form.dataHora" type="datetime-local" label="Data e hora" :rules="[regraObrigatorio]" />
      <v-text-field v-model="form.local" label="Local" :rules="[regraObrigatorio]" />
      <v-text-field v-model.number="form.vagas" type="number" label="Vagas" :rules="[regraObrigatorio, regraVagasPositiva]" />
      <v-text-field v-model="form.imagemUrl" label="URL da imagem (opcional)" />

      <v-btn type="submit" color="primary" :loading="salvando">
        {{ ehEdicao ? 'Salvar alterações' : 'Criar evento' }}
      </v-btn>
      <v-btn variant="text" class="ml-2" :to="{ name: 'eventos-lista' }">Cancelar</v-btn>
    </v-form>
  </v-container>
</template>
```

> **⚠️ Atenção**
> `dataHora?.slice(0, 16)` funciona porque o back-end devolve um ISO 8601 completo (`2030-12-01T19:00:00.000Z`) e o input `datetime-local` espera `AAAA-MM-DDTHH:mm`. É um detalhe de formato pequeno, mas quebra silenciosamente se esquecido — o campo simplesmente aparece vazio.

### Como testar

Com o MySQL, a `unieventos-api` e o `unieventos-web` rodando, feche o ciclo nas duas pontas.

Primeiro só a API:

```bash
curl -s "http://localhost:3000/api/eventos?pagina=1&porPagina=2" | jq
```

Resultado esperado:

```json
{
  "dados": [
    { "id": 1, "titulo": "Semana da Computação", "categoria": "palestra", "dataHora": "2030-12-01T19:00:00.000Z", "local": "Auditório Central", "vagas": 80, "vagasDisponiveis": 62, "imagemUrl": null }
  ],
  "paginacao": { "pagina": 1, "porPagina": 2, "total": 8, "totalPaginas": 4 }
}
```

Repare em três coisas: as chaves em **camelCase**, o `vagasDisponiveis` **derivado** pelo `LEFT JOIN` (não guardado em coluna) e o envelope `{ dados, paginacao }`.

Depois o CRUD pela tela, na ordem:

1. **Listar** — `/eventos` mostra a tabela paginada; digitar na busca espera 400 ms e recarrega; ir para a página 2 dispara nova requisição (confira na aba Network que `?pagina=2` sai de verdade — paginação é no servidor).
2. **Criar** — "Novo evento" abre `/eventos/novo` em modo criação; salvar um evento válido volta para a lista **com o evento novo no topo**.
3. **Editar** — o lápis abre `/eventos/:id/editar` **já preenchido** (se abrir vazio, o nome da rota está errado: `evento-form-editar`, não `evento-form`); alterar o título e salvar reflete na tabela.
4. **Excluir** — a lixeira (visível só para admin) pede confirmação e remove a linha; em um evento com inscritos, o snackbar mostra a mensagem de `409` vinda de `erro.mensagem`.
5. **Erro de validação** — envie um evento com `vagas: 0`: a resposta é `422`, e a mensagem que aparece na tela é a do campo, não um "Erro interno".
6. **Sem token** — deslogue e tente criar pelo `curl`: `401`, e o front redireciona para `/login`.

Se os seis passam, front e back estão falando exatamente o contrato da seção 1.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Preveja o status e o corpo de cada chamada abaixo **sem rodar**, usando só o contrato da seção 1 e as rotas da seção 2.4. Depois rode as três e confira.

```bash
# (a) sem cabeçalho Authorization
curl -i -X DELETE http://localhost:3000/api/eventos/7

# (b) com token válido de um usuário comum (não admin)
curl -i -X DELETE http://localhost:3000/api/eventos/7 -H "Authorization: Bearer $TOKEN"

# (c) com token de admin, mas o evento 7 tem 3 inscritos
curl -i -X DELETE http://localhost:3000/api/eventos/7 -H "Authorization: Bearer $TOKEN_ADMIN"
```

Resultado esperado: (a) `401`, barrado pelo `autenticar` antes de qualquer regra; (b) `403`, barrado pelo `autorizar(['admin'])`; (c) `409` com `{ "erro": { "mensagem": "Não é possível excluir evento com inscritos.", "codigo": "CONFLITO" } }`, vindo do service.

**A2.** O front chama `GET /api/eventos?pagina=0&porPagina=500`. Que valores de `paginacao.pagina` e `paginacao.porPagina` voltam na resposta? Aponte a linha de `eventosService.listar` (back-end) que decide cada um.

Resultado esperado: `pagina: 1` (o `Math.max(1, …)` corrige o zero) e `porPagina: 50` (o `Math.min(50, …)` corta o excesso) — nenhum erro é devolvido, os valores são apenas normalizados.

**A3.** Verdadeiro ou falso, com justificativa de uma linha: "No Express 5, o controller `criar` precisa de `try/catch` para que um `ZodError` lançado dentro de `eventosService.criar` chegue ao `tratadorDeErros`."

Resultado esperado: falso — o Express 5 encaminha automaticamente a rejeição de um handler `async` para o middleware de erro; o `try/catch` seria redundante (e, se engolisse o erro sem `next(err)`, faria a requisição travar sem resposta).

**A4.** Em duas linhas: por que `EventoFormView.vue` faz `evento.dataHora?.slice(0, 16)` antes de preencher o formulário? O que aparece no campo se você remover o `.slice`?

Resultado esperado: o back-end devolve ISO completo (`2030-12-01T19:00:00.000Z`) e o `datetime-local` só aceita `AAAA-MM-DDTHH:mm`; sem o `.slice`, o navegador descarta o valor inteiro e o campo aparece **vazio**, sem aviso no console.

**A5.** Na store, `remover(id)` termina com `lista.value.filter((e) => e.id !== Number(id))`. Se alguém trocar por `e.id !== id` e o `id` chegar como a string `'3'` vinda de `route.params`, o que o usuário vê na tela logo depois de excluir? E depois de apertar F5? Explique a diferença.

Resultado esperado: com `!==` estrito entre número e string a comparação nunca é falsa, então a linha **continua na tabela** mesmo depois do `204` do servidor; após o F5 ela some, porque a lista é recarregada do banco — o clássico "some quando recarrego", sinal de estado local dessincronizado do servidor.

### Nível B — Aplicação

**B1.** Contrato documentado. Escreva a tabela de contrato (seção 1) para uma entidade do seu projeto autoral.

Resultado esperado: cinco linhas (método, caminho, autenticação) e, abaixo da tabela, um bloco JSON de corpo e um de resposta para o `POST` e para o `GET` de lista.

<details markdown="1">
<summary>Dica</summary>

Cinco linhas — uma por endpoint — método, caminho, autenticação. Corpo e resposta podem ir em blocos JSON abaixo da tabela.
</details>

**B2.** Back-end completo. Implemente `controller → service → repository` da sua entidade principal com validação zod, paginação e ao menos uma regra de negócio (ex.: não aceitar valor negativo, não excluir se houver dependência).

Resultado esperado: os 5 endpoints respondem no `curl` com os status do contrato; um `POST` com campo inválido devolve `422` com `detalhes` apontando o campo; `?pagina=2&porPagina=5` muda a fatia devolvida.

<details markdown="1">
<summary>Dica</summary>

Reaproveite a estrutura de `eventosService.js` — troque só os campos do `z.object`.
</details>

**B3.** Store pessimista. Implemente a store Pinia da entidade com `lista`, `carregando`, `erro` e as ações CRUD, todas aguardando confirmação do servidor antes de mudar o estado local.

Resultado esperado: cada ação só altera `lista` depois do `await`; provocar um `422` deixa `erro` preenchido e `carregando` de volta em `false`.

<details markdown="1">
<summary>Dica</summary>

Todo `try` termina em `finally { carregando.value = false }` — não esqueça, senão a tela trava em loading para sempre em caso de erro.
</details>

**B4.** Telas de listagem e formulário. Construa `ListaView` com `v-data-table-server` (busca + paginação) e `FormView` servindo criar e editar pela mesma rota parametrizada.

Resultado esperado: buscar, paginar, criar, editar e excluir funcionam sem F5; o formulário de edição abre preenchido, inclusive o campo de data.

<details markdown="1">
<summary>Dica</summary>

Confira o formato do campo de data — é a causa mais comum de formulário de edição aparecer "vazio" mesmo com dado no banco.
</details>

**B5.** Depuração guiada. Provoque de propósito um erro 422 (mande um campo inválido) e um erro de CORS (mude temporariamente o `origin` do `cors()` para uma URL errada). Documente, com print da aba Network, o que cada um parece no navegador.

Resultado esperado: dois prints (um `422` com o `detalhes` visível na aba Response; um bloqueio de CORS com a mensagem do console) e duas linhas dizendo qual lado — front ou back — causou cada um.

<details markdown="1">
<summary>Dica</summary>

Depois do teste de CORS, não esqueça de voltar o `origin` correto — é fácil esquecer e passar a aula seguinte "quebrada".
</details>

### Nível C — Desafio em sala

**C1.** Inscrição atômica, ponta a ponta. A função `verificarVagaEInscrever` do repositório (seção 2.1) abre a transação, trava a linha com `FOR UPDATE` e confere as vagas — mas ainda não insere a inscrição. Complete-a e exponha o recurso: `POST /api/eventos/:id/inscricoes` (autenticado) responde `201` com a inscrição, `404` se o evento não existe e `409` se não há vagas; no front, um botão "Inscrever-se" que some quando `vagasDisponiveis` chega a zero. Para fechar, prove a atomicidade: com um evento de 5 vagas, dispare 20 requisições simultâneas e confira no banco quantas inscrições existem.

Resultado esperado: `SELECT COUNT(*) FROM inscricoes WHERE evento_id = ?` devolve exatamente 5, e as outras 15 respostas foram `409`.

<details markdown="1">
<summary>Dica</summary>

O `INSERT INTO inscricoes (evento_id, usuario_uid)` precisa acontecer **entre** o `SELECT ... FOR UPDATE` e o `commit()`, usando a mesma `conexao`. Os erros já saem no formato certo: `erroNaoEncontrado()` vira `404` e o `ErroHttp(409, …, 'SEM_VAGAS')` vira `409` no `tratadorDeErros`. Para as 20 requisições simultâneas, um script Node com `Promise.all(Array.from({ length: 20 }, () => fetch(url, opcoes)))` basta — use tokens de usuários diferentes, ou a `UNIQUE (evento_id, usuario_uid)` vai barrar antes da regra de vagas.
</details>

## 🏆 Desafios

### ⭐ A busca que some na página 3
Tags: vue, devtools, bug, investigacao

Um colega "melhorou" a `EventosListaView.vue` e agora acontece algo estranho: navegue até a página 3 da tabela e digite "docker" na busca — a tabela mostra "Nenhum evento encontrado", mas o rodapé insiste que existem 2 resultados. O "Minicurso de Docker" está lá no banco. Este é o trecho alterado:

```js
// src/views/EventosListaView.vue — trecho com o bug plantado
watch(termoBusca, () => {
  clearTimeout(temporizadorBusca)
  temporizadorBusca = setTimeout(() => {
    carregarPagina()
  }, 400)
})
```

Antes de olhar o código, abra a aba Network: qual query string está indo para a API, e o que a resposta traz em `dados` e em `paginacao`? A resposta do servidor está errada — ou está certa demais?

**Critérios de pronto**

- Um comentário no topo do arquivo registra a URL exata da requisição que reproduz o bug e o JSON de `paginacao` devolvido.
- Buscar a partir de qualquer página mostra os resultados corretos, e o rodapé da tabela bate com o que está na tela.
- Limpar a busca (botão `clearable`) também volta a um estado coerente, sem requisição duplicada na aba Network.
- Uma frase no comentário explica por que o back-end não tem culpa nenhuma.

<details markdown="1">
<summary>Pistas</summary>

1. Na aba Network, clique na requisição de `eventos` e compare os parâmetros `pagina` e `busca` com `paginacao.totalPaginas` da resposta.
2. Compare o `watch` acima com a versão do Passo 1 do "Mão na massa" — uma linha sumiu.
3. Se, ao restaurar a linha, a busca disparar duas requisições, investigue o `watch(() => opcoesTabela.value.page, ...)`: mudar a página também chama `carregarPagina`.
</details>

### ⭐⭐ Otimista, mas honesto
Tags: pinia, vue, performance, refatoracao

A store desta aula é pessimista de propósito (seção 5). Mas abra o DevTools, ative o throttling "Slow 3G" na aba Network e exclua um evento: o botão gira por três segundos antes de a linha sumir. Gmail e Trello removem o item na hora — e o devolvem à lista se o servidor recusar. Implemente a exclusão **otimista** em `eventosStore.remover` e responda, com medições, se ela vale a complexidade extra neste projeto.

**Critérios de pronto**

- A linha some da tabela imediatamente ao confirmar a exclusão, antes de a API responder.
- Se a API responder `409` (evento com inscritos), a linha volta **na mesma posição** em que estava, sem duplicar, e um snackbar explica o motivo.
- `carregando`, `erro` e `paginacao.total` continuam coerentes nos dois caminhos (sucesso e falha).
- Um comentário no topo da função registra o tempo entre o clique e o sumiço da linha, com e sem otimismo, medido com throttling "Slow 3G".
- Um parágrafo no README do projeto autoral diz para quais operações você adotaria a estratégia otimista e por quê.

<details markdown="1">
<summary>Pistas</summary>

1. Guarde o índice e uma cópia do item antes de removê-lo da lista: `const indice = lista.value.findIndex(...)` e `const copia = lista.value[indice]`.
2. No `catch`, `lista.value.splice(indice, 0, copia)` devolve o item ao lugar original.
3. Para forçar o `409` sem ter o endpoint de inscrições, insira uma linha direto no MySQL: `INSERT INTO inscricoes (evento_id, usuario_uid) VALUES (7, 'teste')`.
4. Meça com `performance.now()` antes do `filter` e dentro do `finally`; o throttling fica no menu de velocidade da aba Network.
</details>

### ⭐⭐ O que o curl faz que a tela não deixa
Tags: seguranca, express, crud, autenticacao

O botão de editar só aparece para quem está logado, e o de excluir só para admin. Mas botão escondido não é permissão: qualquer pessoa com um token válido consegue montar um `PUT /api/eventos/3` no `curl` e editar o evento que outra pessoa criou, porque a seção 1 deixou essa decisão em aberto ("qualquer autenticado pode editar"). Feche a brecha: um evento passa a ter dono, e só o dono ou um admin pode editá-lo ou excluí-lo.

**Critérios de pronto**

- A tabela `eventos` ganha a coluna `criado_por` (uid do Firebase), preenchida no `POST` a partir do token — nunca a partir do corpo da requisição.
- `PUT` e `DELETE` feitos por quem não é dono nem admin respondem `403` com `{ "erro": { "mensagem": "...", "codigo": "..." } }`; a regra mora no service, não na rota.
- O contrato da seção 1 e a store são atualizados: a resposta de `GET` inclui `criadoPor` (o `linhaParaEvento` ganha mais uma linha), e a tela só mostra os botões para o dono ou para admin.
- Um script `docs/teste-permissoes.sh` com quatro chamadas `curl` (dono edita, outro usuário tenta editar, admin exclui, anônimo tenta excluir) e o status esperado em comentário ao lado de cada uma.

<details markdown="1">
<summary>Pistas</summary>

1. O middleware `autenticar` da Aula 10 já deixa `req.usuario.uid` disponível; passe esse uid do controller para o service junto com `req.body`.
2. `ALTER TABLE eventos ADD COLUMN criado_por VARCHAR(128) NULL` e um `UPDATE` para preencher os eventos antigos com o uid do admin.
3. No service, `atualizar(id, dados, solicitante)`: busque o evento, compare `evento.criado_por` com `solicitante.uid` e verifique se o solicitante é admin (a mesma informação que o middleware `autorizar` usa) antes de tocar no repositório.
4. Para obter dois tokens diferentes: faça login com contas diferentes em duas janelas anônimas e rode `await getAuth().currentUser.getIdToken()` no console de cada uma.
</details>

### ⭐⭐⭐ Paginação que aguenta 100 mil eventos
Tags: mysql, performance, api, banco-de-dados

`LIMIT 10 OFFSET 99990` obriga o MySQL a ler e descartar 99.990 linhas antes de devolver 10 — a última página é sempre a mais lenta. Gere 100 mil eventos falsos, meça o tempo das primeiras e das últimas páginas e depois implemente a alternativa que Twitter e Slack usam: **paginação por cursor**, em que o cliente pede "os 10 próximos depois deste ponto" em vez de "a página N".

**Critérios de pronto**

- Um script `scripts/semear.js` insere 100.000 eventos em lotes (`INSERT ... VALUES (...), (...)`) em menos de um minuto.
- Uma tabela no README compara o tempo de resposta (aba Network ou `curl -w '%{time_total}'`) de `?pagina=1`, `?pagina=5000` e `?pagina=10000`, antes e depois.
- `GET /api/eventos?depois=<cursor>&porPagina=10` devolve os próximos 10 eventos em ordem de `dataHora, id` e um campo `proximoCursor` (`null` na última página).
- O `EXPLAIN` das duas consultas está colado no README, com uma frase apontando a diferença nas colunas `rows` e `type`.
- A tela de listagem continua funcionando no modo antigo (`pagina`) — o novo modo é adicional, e a store escolhe um deles.

<details markdown="1">
<summary>Pistas</summary>

1. Procure por "keyset pagination": a condição é `WHERE (data_hora, id) > (?, ?) ORDER BY data_hora, id LIMIT ?`, e um índice composto `(data_hora, id)` é o que faz a diferença.
2. O cursor pode ser simplesmente `data_hora` e `id` do último item, codificados em base64 para o cliente não precisar entender o formato: `Buffer.from(JSON.stringify([data, id])).toString('base64')`.
3. Para gerar dados, `Array.from({ length: 1000 })` por lote e datas espalhadas com `new Date(Date.now() + i * 60000)` evitam empates no cursor.
4. `v-data-table-server` não sabe o que é cursor; para o modo novo, um botão "Carregar mais" que concatena em `lista.value` é mais honesto do que forçar a tabela.
</details>

## 🐛 Erros comuns e como resolver

| Sintoma | Causa | Solução |
|---|---|---|
| Formulário de edição abre vazio | Formato de `dataHora` incompatível com `datetime-local` | Usar `.slice(0, 16)` no ISO recebido antes de atribuir ao `v-model` |
| Lista não atualiza após criar/editar | Store otimista incompleta, ou índice errado ao substituir item | Conferir `findIndex` comparando tipos (`Number(id)` × `item.id`) |
| Erro 422 sem detalhe visível na tela | Front não está lendo `e.response.data.erro` | Padronizar leitura do erro em todo `catch` da store |
| CORS bloqueia só `PUT`/`DELETE`, `GET` funciona | Preflight `OPTIONS` não tratado — normalmente falta de `cors()` global antes das rotas | Garantir `app.use(cors(...))` antes de `app.use('/api/eventos', ...)` |
| Upload de imagem falha com "permission denied" | Regra do Firebase Storage exige autenticação e o usuário não está logado | Checar `auth.currentUser` antes de chamar `uploadBytes` |
| `curl` funciona mas o front não | Token não está sendo enviado pelo interceptor, ou front aponta para porta errada | Conferir `VITE_API_URL` e o cabeçalho `Authorization` na aba Network |
| Paginação trava na página 2+ | `v-data-table-server` não está usando `items-length` vindo do back, ou store não repassa `paginacao.total` | Confirmar que `paginacao.total` reflete o total real, não o tamanho da página atual |

## 🏠 Atividade assíncrona (1 h)

No seu projeto autoral: implemente o CRUD completo (os 5 endpoints do contrato) de uma **segunda entidade**, diferente da que você já trabalhou no laboratório de hoje. Ela deve ter, no mínimo, uma regra de negócio própria (ex.: não permitir dois registros com o mesmo nome, não excluir se estiver em uso por outra entidade). Documente o contrato dela em uma tabela, igual à da seção 1, e inclua no README do repositório.

**Critério de pronto:** os 5 endpoints respondem corretamente (teste com `curl`), a store e as telas de listagem/formulário funcionam no front, e o contrato está documentado no README.

## ✅ Checkpoint do projeto autoral

- [ ] Contrato de API documentado em tabela para pelo menos duas entidades.
- [ ] Back-end com `controller → service → repository`, validação zod e ao menos uma regra de negócio por entidade.
- [ ] Paginação e busca por query string funcionando no endpoint de listagem.
- [ ] `services/` do front alinhado ao contrato, sem chamadas diretas a `http.get/post/...` fora dessa camada.
- [ ] Store Pinia com `lista`, `itemAtual`, `carregando`, `erro`, `paginacao` e atualização pessimista.
- [ ] Telas de listagem (busca + paginação), formulário único (criar/editar) e diálogo de confirmação de exclusão.
- [ ] Upload de imagem funcionando (Firebase Storage ou `multer`) em pelo menos uma entidade.
- [ ] CORS configurado corretamente entre front e back, sem `origin: '*'` combinado com `credentials: true`.

## 📚 Para aprofundar

- [MDN — CORS](https://developer.mozilla.org/pt-BR/docs/Web/HTTP/CORS)
- [Vuetify — `v-data-table-server`](https://vuetifyjs.com/en/components/data-tables/server-side-tables/)
- [Firebase Storage — Web (modular)](https://firebase.google.com/docs/storage/web/upload-files)
- [zod — documentação oficial](https://zod.dev)
- [MySQL — transações com `mysql2/promise`](https://sidorares.github.io/node-mysql2/docs)
- Plano de curso, Unidade 3: integração front-end/back-end.

Na Aula 12 trocamos de fornecedor: o mesmo CRUD de eventos, agora falando com Supabase — Postgres gerenciado, autenticação própria e Row Level Security no lugar da validação manual de dono/admin que fizemos hoje na API Express.
