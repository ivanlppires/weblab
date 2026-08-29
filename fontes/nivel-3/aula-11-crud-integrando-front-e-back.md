# Aula 11 — Integrando front-end com back-end: CRUD

> **Nível 3 — Frameworks Modernos** · Unidade 3: Integração front-end/back-end
> WebLab · UNEMAT Sinop · Prof. Ivan Luiz Pedroso Pires

Na Aula 10 o UniEventos passou a exigir token do Firebase para escrever dados, e a API passou a validar esse token com `firebase-admin`. Todas as peças já existem separadas: Vue no front, Express no back, MySQL persistindo, Firebase autenticando. Hoje é a aula de **fechar o ciclo** — o CRUD completo de eventos, ponta a ponta, com as duas pontas conversando por um contrato bem definido.

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
| DELETE | `/api/eventos/:id` | Admin |

Detalhando corpo e resposta de cada um:

**`GET /api/eventos`** — lista paginada, com filtros por query string.

Query string: `?pagina=1&limite=10&busca=semana&categoria=palestra`

```json
{
  "dados": [
    {
      "id": 1,
      "titulo": "Semana da Computação",
      "descricao": "Palestras e minicursos de tecnologia",
      "categoria": "palestra",
      "data_hora": "2026-12-01T19:00:00.000Z",
      "local": "Auditório Central",
      "vagas": 80,
      "vagas_disponiveis": 62,
      "imagem_url": "https://.../semana-computacao.jpg"
    }
  ],
  "paginacao": { "pagina": 1, "limite": 10, "total": 34, "totalPaginas": 4 }
}
```

Status: `200 OK`.

**`GET /api/eventos/:id`** — um evento. Status `200 OK` ou `404 Not Found` com `{ "erro": "Evento não encontrado." }`.

**`POST /api/eventos`** — corpo:

```json
{
  "titulo": "Semana da Computação",
  "descricao": "Palestras e minicursos de tecnologia",
  "categoria": "palestra",
  "data_hora": "2026-12-01T19:00:00",
  "local": "Auditório Central",
  "vagas": 80,
  "imagem_url": "https://.../semana-computacao.jpg"
}
```

Resposta: o evento criado, com `id`, status `201 Created`. Erros de validação: `400 Bad Request` com `{ "erro": "...", "detalhes": [...] }`. Sem token: `401`.

**`PUT /api/eventos/:id`** — mesmo corpo do `POST` (campos parciais também aceitos). Resposta: o evento atualizado, `200 OK`. Sem token: `401`. Não é dono nem admin: decisão de negócio do projeto (aqui, qualquer autenticado pode editar — ver seção 3). Evento inexistente: `404`.

**`DELETE /api/eventos/:id`** — sem corpo. Resposta: `204 No Content`. Sem token: `401`. Sem ser admin: `403`. Evento com inscritos: `409 Conflict` com `{ "erro": "Não é possível excluir evento com inscritos." }`.

> **💡 Dica**
> Escreva esse contrato **antes** de codificar, mesmo sozinho. Ele vira a fonte da verdade quando front e back divergem — e em equipes reais costuma virar um arquivo OpenAPI/Swagger, que veremos na Aula 14. Por ora, uma tabela em Markdown já resolve.

## 2. Back-end: completando controller → service → repository

Revisamos a estrutura da Aula 09 e adicionamos: validação com zod, regras de negócio, paginação e busca.

### 2.1 Repository — só acesso a dados, sem regra de negócio

```js
// unieventos-api/src/repositories/eventosRepository.js
import { pool } from '../config/database.js'

export async function listar({ pagina, limite, busca, categoria }) {
  const offset = (pagina - 1) * limite
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
    [...parametros, limite, offset],
  )

  const [[{ total }]] = await pool.query(
    `SELECT COUNT(*) AS total FROM eventos e ${clausulaWhere}`,
    parametros,
  )

  return { linhas, total }
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
  return linhas[0] ?? null
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
      evento.data_hora,
      evento.local,
      evento.vagas,
      evento.imagem_url ?? null,
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
      evento.data_hora,
      evento.local,
      evento.vagas,
      evento.imagem_url ?? null,
      id,
    ],
  )
  return buscarPorId(id)
}

export async function remover(id) {
  await pool.query('DELETE FROM eventos WHERE id = ?', [id])
}

export async function decrementarVagaEmTransacao(id) {
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
    if (!evento) {
      await conexao.rollback()
      throw new Error('EVENTO_NAO_ENCONTRADO')
    }
    if (evento.inscritos >= evento.vagas) {
      await conexao.rollback()
      throw new Error('SEM_VAGAS')
    }

    await conexao.commit()
    return true
  } catch (erro) {
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

export const esquemaEvento = z.object({
  titulo: z.string().trim().min(3, 'Título precisa ter ao menos 3 caracteres'),
  descricao: z.string().trim().min(10, 'Descrição precisa ter ao menos 10 caracteres'),
  categoria: z.enum(['palestra', 'minicurso', 'workshop'], {
    message: 'Categoria precisa ser palestra, minicurso ou workshop',
  }),
  data_hora: z
    .string()
    .datetime({ offset: true, message: 'Data e hora em formato ISO inválido' })
    .or(z.string().min(1)) // aceita também "2026-12-01T19:00:00" sem offset
    .refine((valor) => !Number.isNaN(Date.parse(valor)), 'Data e hora inválidas')
    .refine((valor) => new Date(valor).getTime() > Date.now(), 'A data do evento não pode estar no passado'),
  local: z.string().trim().min(3, 'Local precisa ter ao menos 3 caracteres'),
  vagas: z.number().int().positive('Vagas precisa ser um número positivo'),
  imagem_url: z.url('URL de imagem inválida').optional().or(z.literal('')),
})

export const esquemaEventoParcial = esquemaEvento.partial()

export async function listar({ pagina = 1, limite = 10, busca, categoria }) {
  const paginaSegura = Math.max(1, Number(pagina))
  const limiteSeguro = Math.min(50, Math.max(1, Number(limite)))

  const { linhas, total } = await eventosRepository.listar({
    pagina: paginaSegura,
    limite: limiteSeguro,
    busca,
    categoria,
  })

  return {
    dados: linhas,
    paginacao: {
      pagina: paginaSegura,
      limite: limiteSeguro,
      total,
      totalPaginas: Math.ceil(total / limiteSeguro),
    },
  }
}

export async function buscarPorId(id) {
  const evento = await eventosRepository.buscarPorId(id)
  if (!evento) {
    const erro = new Error('Evento não encontrado.')
    erro.status = 404
    throw erro
  }
  return evento
}

export async function criar(dadosBrutos) {
  const dados = esquemaEvento.parse(dadosBrutos)
  return eventosRepository.criar(dados)
}

export async function atualizar(id, dadosBrutos) {
  await buscarPorId(id) // garante 404 antes de tentar validar/atualizar
  const dados = esquemaEvento.parse(dadosBrutos)
  return eventosRepository.atualizar(id, dados)
}

export async function remover(id) {
  await buscarPorId(id)

  const inscritos = await eventosRepository.contarInscritos(id)
  if (inscritos > 0) {
    const erro = new Error('Não é possível excluir evento com inscritos.')
    erro.status = 409
    throw erro
  }

  await eventosRepository.remover(id)
}
```

### 2.3 Controller — só orquestra requisição/resposta

```js
// unieventos-api/src/controllers/eventosController.js
import * as eventosService from '../services/eventosService.js'

export async function listar(req, res) {
  const { pagina, limite, busca, categoria } = req.query
  const resultado = await eventosService.listar({ pagina, limite, busca, categoria })
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

export async function remover(req, res) {
  await eventosService.remover(req.params.id)
  res.status(204).send()
}
```

Sem `try/catch` nos controllers: Express 5 encaminha automaticamente qualquer rejeição de handler `async` para o middleware de erro central, criado na Aula 08. Só precisamos garantir que esse middleware trate `ZodError` (400), erros com `.status` customizado (404, 409) e, por padrão, 500:

```js
// unieventos-api/src/middlewares/tratadorErros.js
import { ZodError } from 'zod'

export function tratadorErros(erro, req, res, next) {
  if (erro instanceof ZodError) {
    return res.status(400).json({
      erro: 'Dados inválidos.',
      detalhes: erro.issues.map((i) => ({ campo: i.path.join('.'), mensagem: i.message })),
    })
  }

  if (erro.status) {
    return res.status(erro.status).json({ erro: erro.message })
  }

  console.error(erro)
  res.status(500).json({ erro: 'Erro interno do servidor.' })
}
```

### 2.4 Rotas com validação por middleware Zod

Reaproveitando o padrão de validação da Aula 08, mas agora com o esquema parcial para `PUT`:

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
// unieventos-api/src/routes/eventosRoutes.js
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
router.put('/:id', autenticar, validar(esquemaEventoParcial), eventosController.atualizar)
router.delete('/:id', autenticar, autorizar(['admin']), eventosController.remover)

export default router
```

## 3. Front-end: `services/` alinhado ao contrato

```js
// src/services/eventosService.js
import api from './api'

export function listarEventos({ pagina = 1, limite = 10, busca = '', categoria = '' } = {}) {
  return api
    .get('/eventos', { params: { pagina, limite, busca, categoria } })
    .then((resposta) => resposta.data)
}

export function buscarEvento(id) {
  return api.get(`/eventos/${id}`).then((resposta) => resposta.data)
}

export function criarEvento(evento) {
  return api.post('/eventos', evento).then((resposta) => resposta.data)
}

export function atualizarEvento(id, evento) {
  return api.put(`/eventos/${id}`, evento).then((resposta) => resposta.data)
}

export function removerEvento(id) {
  return api.delete(`/eventos/${id}`)
}
```

> **💡 Dica**
> Repare que cada função do service tem exatamente uma responsabilidade e um nome que espelha o contrato da seção 1. Ninguém que ler esse arquivo precisa saber que por trás existe Axios, interceptors ou token — e é exatamente esse esconderijo que a store vai explorar.

## 🧩 Padrão de projeto em uso: Facade

A camada `services/` do front é um **Facade** (padrão estrutural): oferece uma interface simples (`listarEventos()`, `criarEvento()`) escondendo a complexidade de configurar o Axios, montar query string, tratar cabeçalhos de autenticação e formatar a resposta. A store, os componentes e as views nunca chamam `api.get(...)` diretamente — eles conversam só com o Facade. Se amanhã trocarmos Axios por `fetch` nativo, ou a URL base da API mudar de estrutura, só o `services/` muda; store e telas continuam iguais. Voltaremos a esse mesmo princípio na Aula 12, quando o Adapter permitir trocar Express+MySQL por Supabase sem tocar no front.

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
  const paginacao = ref({ pagina: 1, limite: 10, total: 0, totalPaginas: 0 })

  async function carregar({ pagina = 1, limite = 10 } = {}) {
    carregando.value = true
    erro.value = null
    try {
      const resultado = await eventosService.listarEventos({ pagina, limite })
      lista.value = resultado.dados
      paginacao.value = resultado.paginacao
    } catch (e) {
      erro.value = e.response?.data?.erro ?? 'Não foi possível carregar os eventos.'
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
        limite: paginacao.value.limite,
        busca: termo,
        categoria,
      })
      lista.value = resultado.dados
      paginacao.value = resultado.paginacao
    } catch (e) {
      erro.value = e.response?.data?.erro ?? 'Não foi possível buscar os eventos.'
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
      erro.value = e.response?.data?.erro ?? 'Evento não encontrado.'
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
      erro.value = e.response?.data?.erro ?? 'Não foi possível criar o evento.'
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
      erro.value = e.response?.data?.erro ?? 'Não foi possível atualizar o evento.'
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
      erro.value = e.response?.data?.erro ?? 'Não foi possível excluir o evento.'
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
  { title: 'Data', key: 'data_hora' },
  { title: 'Vagas', key: 'vagas_disponiveis' },
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
  router.push({ name: 'evento-form', params: { id: evento.id } })
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
      <template #item.data_hora="{ item }">
        {{ formatarData(item.data_hora) }}
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
  data_hora: '',
  local: '',
  vagas: 1,
  imagem_url: '',
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
        data_hora: evento.data_hora?.slice(0, 16), // ISO -> formato do input datetime-local
        local: evento.local,
        vagas: evento.vagas,
        imagem_url: evento.imagem_url ?? '',
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
      <v-text-field v-model="form.data_hora" type="datetime-local" label="Data e hora" :rules="[regraObrigatorio]" />
      <v-text-field v-model="form.local" label="Local" :rules="[regraObrigatorio]" />
      <v-text-field v-model.number="form.vagas" type="number" label="Vagas" :rules="[regraObrigatorio, regraVagasPositiva]" />
      <v-text-field v-model="form.imagem_url" label="URL da imagem (opcional)" />

      <v-btn type="submit" color="primary" :loading="salvando">
        {{ ehEdicao ? 'Salvar alterações' : 'Criar evento' }}
      </v-btn>
      <v-btn variant="text" class="ml-2" :to="{ name: 'eventos-lista' }">Cancelar</v-btn>
    </v-form>
  </v-container>
</template>
```

> **⚠️ Atenção**
> `data_hora?.slice(0, 16)` funciona porque o back-end devolve um ISO 8601 completo (`2026-12-01T19:00:00.000Z`) e o input `datetime-local` espera `AAAA-MM-DDTHH:mm`. É um detalhe de formato pequeno, mas quebra silenciosamente se esquecido — o campo simplesmente aparece vazio.

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

```vue
<!-- trecho a adicionar em EventoFormView.vue: campo de upload -->
<script setup>
// ...imports existentes
import { enviarImagemEvento } from '@/services/storageService'

const enviandoImagem = ref(false)

async function aoSelecionarImagem(arquivos) {
  const arquivo = arquivos?.[0]
  if (!arquivo) return

  enviandoImagem.value = true
  try {
    form.value.imagem_url = await enviarImagemEvento(arquivo)
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
  <v-img v-if="form.imagem_url" :src="form.imagem_url" max-height="200" class="mb-4" cover />
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
    "data_hora": "2026-12-10T14:00:00",
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

## 🧪 Laboratório

**1. Contrato documentado.** Escreva a tabela de contrato (seção 1) para uma entidade do seu projeto autoral.
<details><summary>Dica</summary>Cinco linhas — uma por endpoint — método, caminho, autenticação. Corpo e resposta podem ir em blocos JSON abaixo da tabela.</details>

**2. Back-end completo.** Implemente `controller → service → repository` da sua entidade principal com validação zod, paginação e ao menos uma regra de negócio (ex.: não aceitar valor negativo, não excluir se houver dependência).
<details><summary>Dica</summary>Reaproveite a estrutura de `eventosService.js` — troque só os campos do `z.object`.</details>

**3. Store pessimista.** Implemente a store Pinia da entidade com `lista`, `carregando`, `erro` e as ações CRUD, todas aguardando confirmação do servidor antes de mudar o estado local.
<details><summary>Dica</summary>Todo `try` termina em `finally { carregando.value = false }` — não esqueça, senão a tela trava em loading para sempre em caso de erro.</details>

**4. Telas de listagem e formulário.** Construa `ListaView` com `v-data-table-server` (busca + paginação) e `FormView` servindo criar e editar pela mesma rota parametrizada.
<details><summary>Dica</summary>Confira o formato do campo de data — é a causa mais comum de formulário de edição aparecer "vazio" mesmo com dado no banco.</details>

**5. Depuração guiada.** Provoque de propósito um erro 400 (mande um campo inválido) e um erro de CORS (mude temporariamente o `origin` do `cors()` para uma URL errada). Documente, com print da aba Network, o que cada um parece no navegador.
<details><summary>Dica</summary>Depois do teste de CORS, não esqueça de voltar o `origin` correto — é fácil esquecer e passar a aula seguinte "quebrada".</details>

## 🐛 Erros comuns e como resolver

| Sintoma | Causa | Solução |
|---|---|---|
| Formulário de edição abre vazio | Formato de `data_hora` incompatível com `datetime-local` | Usar `.slice(0, 16)` no ISO recebido antes de atribuir ao `v-model` |
| Lista não atualiza após criar/editar | Store otimista incompleta, ou índice errado ao substituir item | Conferir `findIndex` comparando tipos (`Number(id)` × `item.id`) |
| Erro 400 sem detalhe visível na tela | Front não está lendo `e.response.data.erro` | Padronizar leitura do erro em todo `catch` da store |
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
- [ ] `services/` do front alinhado ao contrato, sem chamadas diretas a `api.get/post/...` fora dessa camada.
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
