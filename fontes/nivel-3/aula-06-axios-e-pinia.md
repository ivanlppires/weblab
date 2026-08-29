# Aula 06 — Axios e Pinia

> **Nível 3 — Frameworks Modernos** · Unidade 2: Vue.js avançado: Vuetify, Axios, Router e Pinia
> WebLab · UNEMAT Sinop · Prof. Ivan Luiz Pedroso Pires

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Explicar o protocolo HTTP na prática: métodos, os status codes que realmente importam no dia a dia e por que o CORS existe.
- Configurar uma instância dedicada do Axios (`axios.create`) com interceptors de request e response, e tratar erros distinguindo `error.response` de `error.request`.
- Cancelar requisições com `AbortController` e enviar arquivos com `FormData`.
- Organizar chamadas HTTP em uma camada de serviços, mantendo os componentes livres de detalhes de rede.
- Subir uma API falsa com `json-server` para desenvolvimento e testes.
- Criar stores Pinia no estilo **setup store**, com `storeToRefs`, ações assíncronas, `$reset`, `$patch`, `$subscribe` e persistência em `localStorage`.
- Conectar o UniEventos a uma API real via camada de serviços e stores, com feedback visual de carregamento, erro e sucesso.

## 📋 Pré-requisitos desta aula

- [ ] UniEventos da Aula 05 com componentes extraídos, composable `useEventos`, rotas aninhadas e formulário validado funcionando.
- [ ] Node.js 22.22.2 e npm 10.9.7 instalados (`node -v`, `npm -v`).
- [ ] Terminal disponível para rodar dois processos simultâneos (API falsa + app Vue).

> Na Aula 05 você quebrou o UniEventos em componentes e extraiu a lógica de dados para o composable `useEventos`. Esse composable ainda trabalha com um array estático importado de `src/data/eventos.js`. Hoje esse array vira uma **API de verdade**, e o estado que hoje vive em `ref`s locais migra para **stores Pinia** — compartilhadas por toda a aplicação.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | HTTP na prática, CORS, Axios: instância dedicada, interceptors, tratamento de erro |
| 2 | 50 min | Camada de serviços, `json-server`, Pinia: setup store, `storeToRefs`, ações assíncronas, persistência |
| 3 | 50 min | Mão na massa: UniEventos consumindo API real via serviços + stores |

## 1. HTTP na prática

Você já usou `fetch` na Aula 03. Antes de trocar por Axios, vale consolidar o que realmente importa saber sobre HTTP para trabalhar com APIs no dia a dia.

### Métodos

| Método | Uso típico |
|---|---|
| `GET` | ler um recurso (lista de eventos, um evento específico) |
| `POST` | criar um recurso novo |
| `PUT` | substituir um recurso inteiro |
| `PATCH` | atualizar parcialmente um recurso |
| `DELETE` | remover um recurso |

### Status codes que importam

Não é preciso decorar os ~60 códigos HTTP — só os que aparecem o tempo todo:

| Código | Significado | Quando aparece |
|---|---|---|
| `200 OK` | sucesso, resposta com corpo | `GET`, `PUT`, `PATCH` bem-sucedidos |
| `201 Created` | recurso criado | `POST` bem-sucedido |
| `204 No Content` | sucesso, sem corpo de resposta | `DELETE` bem-sucedido |
| `400 Bad Request` | requisição malformada | corpo JSON inválido, campo faltando |
| `401 Unauthorized` | não autenticado | token ausente ou inválido |
| `403 Forbidden` | autenticado, mas sem permissão | usuário comum tentando ação de admin |
| `404 Not Found` | recurso não existe | ID inexistente na URL |
| `409 Conflict` | conflito de estado | tentar criar um recurso duplicado |
| `422 Unprocessable Entity` | validação de negócio falhou | e-mail em formato inválido, vagas negativas |
| `500 Internal Server Error` | erro não tratado no servidor | bug no back-end |

> **📌 Na prova:** a diferença entre `400` e `422` é sutil, mas cai em prova: `400` é sobre a **forma** da requisição (JSON quebrado, tipo errado); `422` é sobre o **conteúdo semanticamente inválido** de uma requisição bem formada (ex.: `vagas: -5`).

### Headers e JSON

Toda requisição e resposta HTTP carrega **headers** — metadados como `Content-Type: application/json` (informa que o corpo é JSON) e `Authorization: Bearer <token>` (credencial de autenticação). O corpo em si, na grande maioria das APIs modernas, é um texto no formato JSON — o mesmo `JSON.stringify`/`JSON.parse` que você já usa em JavaScript puro.

### CORS explicado de verdade

**CORS** (Cross-Origin Resource Sharing) é uma política de segurança **do navegador**, não do servidor. Quando sua aplicação Vue, servida em `http://localhost:5173`, faz uma requisição para uma API em `http://localhost:3000`, o navegador considera isso uma requisição **cross-origin** (origens diferentes: porta diferente já conta como origem diferente, mesmo com o mesmo domínio `localhost`).

Por padrão, o navegador **bloqueia** a leitura da resposta de uma requisição cross-origin, a menos que o servidor responda explicitamente autorizando aquela origem, através do header `Access-Control-Allow-Origin`. Isso existe para impedir que um site malicioso, rodando no seu navegador enquanto você está autenticado em outro site (ex.: seu banco), faça requisições silenciosas para esse outro site usando suas credenciais de sessão sem seu conhecimento.

Para requisições "simples" (GET/POST com `Content-Type` comum), o navegador já bloqueia a leitura da resposta se o header de autorização não vier certo. Para requisições consideradas "não simples" — como `PUT`, `DELETE`, ou `POST` com `Content-Type: application/json` combinado com headers customizados — o navegador primeiro envia uma requisição `OPTIONS` chamada **preflight**, perguntando ao servidor "você aceita esse tipo de requisição desta origem, com estes headers?". Só se o servidor responder afirmativamente ao preflight é que o navegador envia a requisição real.

> **⚠️ Atenção:** CORS é responsabilidade do **servidor** resolver (autorizando origens), não do front-end. Se você está desenvolvendo e vê um erro de CORS no console, a correção não é "tentar outra sintaxe no Axios" — é configurar o servidor para responder com os headers corretos. Vamos configurar isso na prática quando construirmos a API Express, na Unidade 3 (Aula 07 em diante). Por hoje, o `json-server` que vamos usar já vem com CORS liberado por padrão.

## 2. Axios: por que uma biblioteca além do `fetch`

`fetch` é nativo do navegador e funciona bem para casos simples — foi o suficiente até a Aula 03. Mas em uma aplicação real, algumas limitações do `fetch` pesam:

| Recurso | `fetch` | Axios |
|---|---|---|
| Corpo da resposta já convertido em JSON | precisa de `.json()` manual | `response.data` já vem pronto |
| Erros HTTP (4xx/5xx) | **não** rejeitam a Promise automaticamente | rejeitam a Promise automaticamente |
| Timeout de requisição | precisa implementar manualmente com `AbortController` | prop `timeout` pronta |
| Interceptors (request/response) | não existe nativamente | suportado nativamente |
| Instância com configuração padrão (`baseURL`, headers) | precisa reimplementar um wrapper | `axios.create({...})` pronto |
| Cancelamento | `AbortController` | `AbortController` (compatível) |

O ponto mais importante da tabela é o segundo: com `fetch`, uma resposta `404` ou `500` **não** faz a Promise falhar — você precisa checar `response.ok` manualmente. Isso é uma fonte comum de bugs silenciosos. Com Axios, qualquer status fora da faixa 2xx já cai automaticamente no `catch`.

### Instalação

```bash
npm install axios
```

Versão usada nesta disciplina: **axios 1.19.0**.

### Instância dedicada

> **⚠️ Atenção:** nunca use o `axios` importado diretamente (`import axios from 'axios'`) espalhado pelos componentes. Sempre crie uma **instância dedicada**, configurada uma única vez, e reutilize-a em toda a aplicação.

```js
// src/services/http.js
import axios from 'axios'

const http = axios.create({
  baseURL: 'http://localhost:3000',
  timeout: 8000,
  headers: {
    'Content-Type': 'application/json',
  },
})

export default http
```

Isso centraliza `baseURL` (endereço da API), `timeout` (tempo máximo de espera antes de desistir da requisição) e headers padrão em um único lugar — trocar de ambiente (desenvolvimento → produção) vira uma alteração em um arquivo só.

### Interceptor de request — injetar token

Um **interceptor** é uma função que roda automaticamente antes de cada requisição sair (interceptor de request) ou antes de cada resposta chegar ao código que a chamou (interceptor de response):

```js
// src/services/http.js (trecho — adicionar após criar a instância)
http.interceptors.request.use((config) => {
  const token = localStorage.getItem('uniEventosToken')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

Com isso, **nenhum componente ou serviço precisa se lembrar de anexar o token manualmente** — toda requisição feita através de `http` já sai com o header `Authorization` quando há um token salvo. Vamos usar esse mecanismo de verdade na Unidade 3, quando implementarmos login com Firebase.

### Interceptor de response — tratar 401 e normalizar erros

```js
// src/services/http.js (trecho — adicionar após o interceptor de request)
http.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('uniEventosToken')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)
```

Esse interceptor de response roda para **toda** resposta com erro, em qualquer lugar da aplicação: se o servidor responder `401` (token expirado ou inválido), o interceptor limpa o token salvo e redireciona para o login — sem que cada chamada de API precise repetir essa lógica.

### Tratamento de erro: `error.response` vs. `error.request`

Ao capturar um erro do Axios, existem três cenários possíveis, e cada um exige um tratamento diferente:

```js
try {
  const resposta = await http.get('/eventos')
  console.log(resposta.data)
} catch (erro) {
  if (erro.response) {
    // o servidor respondeu, mas com status de erro (4xx, 5xx)
    console.error('Erro do servidor:', erro.response.status, erro.response.data)
  } else if (erro.request) {
    // a requisição foi enviada, mas nenhuma resposta chegou
    // (servidor fora do ar, sem rede, CORS bloqueando)
    console.error('Sem resposta do servidor:', erro.request)
  } else {
    // erro ao montar a própria requisição (configuração inválida, etc.)
    console.error('Erro ao configurar a requisição:', erro.message)
  }
}
```

Essa distinção importa na prática: um `erro.response` com `404` deve mostrar "evento não encontrado"; um `erro.request` (sem resposta nenhuma) deve mostrar "não foi possível conectar ao servidor — verifique sua internet".

### Cancelamento com `AbortController`

Em telas com busca "ao digitar" (busca incremental), cada tecla pode disparar uma nova requisição antes da anterior terminar — sem cancelamento, respostas antigas podem chegar depois das novas e sobrescrever dados mais recentes na tela.

```js
let controlador = null

async function buscar(termo) {
  if (controlador) controlador.abort() // cancela a busca anterior, se existir
  controlador = new AbortController()

  try {
    const resposta = await http.get('/eventos', {
      params: { titulo_like: termo },
      signal: controlador.signal,
    })
    return resposta.data
  } catch (erro) {
    if (axios.isCancel(erro) || erro.code === 'ERR_CANCELED') {
      return [] // busca cancelada, não é um erro de verdade
    }
    throw erro
  }
}
```

### Upload com `FormData`

Quando o UniEventos precisar permitir upload de uma imagem de evento (em vez de só uma URL), o corpo da requisição deixa de ser JSON e passa a ser `multipart/form-data`, construído com `FormData`:

```js
async function enviarImagem(arquivo) {
  const dados = new FormData()
  dados.append('imagem', arquivo)

  const resposta = await http.post('/upload', dados, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return resposta.data.url
}
```

`FormData` é uma API nativa do navegador (não específica do Axios) para montar corpos de requisição no formato usado tradicionalmente por formulários HTML com arquivos.

## 3. Camada de serviços

Um erro comum é chamar `http.get(...)` diretamente dentro de um componente `.vue`. Isso mistura duas responsabilidades que deveriam ser independentes: **como a tela se comporta** e **como os dados são buscados**. Se a API mudar (endpoint renomeado, formato de resposta diferente), você teria que caçar cada componente que faz chamadas HTTP.

A solução é uma **camada de serviços**: um módulo por recurso, que expõe funções com nomes de negócio (`listar`, `criar`, `remover`) e esconde os detalhes de URL, método HTTP e formato de payload.

```js
// src/services/eventosService.js
import http from './http'

export default {
  async listar(filtros = {}) {
    const resposta = await http.get('/eventos', { params: filtros })
    return resposta.data
  },

  async buscarPorId(id) {
    const resposta = await http.get(`/eventos/${id}`)
    return resposta.data
  },

  async criar(evento) {
    const resposta = await http.post('/eventos', evento)
    return resposta.data
  },

  async atualizar(id, evento) {
    const resposta = await http.put(`/eventos/${id}`, evento)
    return resposta.data
  },

  async remover(id) {
    await http.delete(`/eventos/${id}`)
  },
}
```

Um componente (ou, como veremos, uma store) usa isso assim:

```js
import eventosService from '../services/eventosService'

const eventos = await eventosService.listar({ categoria: 'palestra' })
```

**Por que os componentes não devem chamar Axios diretamente:**

1. **Testabilidade** — testar um serviço isolado (mockando `http`) é muito mais simples do que testar um componente inteiro só para validar uma chamada de API.
2. **Reuso** — a mesma função `eventosService.listar()` é chamada pela `HomeView`, pela busca administrativa e por um composable, sem repetir a URL em três lugares.
3. **Um ponto único de mudança** — se o endpoint `/eventos` virar `/api/v1/eventos`, você edita um arquivo, não uma dúzia de componentes.
4. **Separação de camadas** — é o mesmo princípio de "não misturar HTML com lógica de banco de dados" que você vai aplicar no back-end, na Unidade 3.

## 4. API falsa para a aula: `json-server`

Antes de existir um back-end real (isso vem na Unidade 3, com Express), usamos o **json-server**: uma ferramenta que transforma um arquivo JSON em uma API REST completa, com poucos minutos de configuração.

### Criando o `db.json` do UniEventos

```json
// db.json
{
  "eventos": [
    { "id": 1, "titulo": "Semana Acadêmica de Computação", "descricao": "Palestras e minicursos sobre tendências em tecnologia.", "categoria": "palestra", "dataHora": "2026-09-29T19:00:00", "local": "Auditório Central", "vagas": 40, "imagemUrl": "https://picsum.photos/seed/evento1/600/300" },
    { "id": 2, "titulo": "Minicurso de Vue.js Avançado", "descricao": "Componentização, roteamento e gerenciamento de estado.", "categoria": "minicurso", "dataHora": "2026-09-15T18:30:00", "local": "Laboratório 3", "vagas": 25, "imagemUrl": "https://picsum.photos/seed/evento2/600/300" },
    { "id": 3, "titulo": "Workshop de Prototipação em Figma", "descricao": "Fundamentos de design de interfaces para desenvolvedores.", "categoria": "workshop", "dataHora": "2026-09-20T14:00:00", "local": "Sala 12", "vagas": 30, "imagemUrl": "https://picsum.photos/seed/evento3/600/300" },
    { "id": 4, "titulo": "Palestra: Carreira em Dados", "descricao": "Trilhas profissionais em ciência e engenharia de dados.", "categoria": "palestra", "dataHora": "2026-10-02T19:30:00", "local": "Auditório Central", "vagas": 50, "imagemUrl": "https://picsum.photos/seed/evento4/600/300" },
    { "id": 5, "titulo": "Minicurso de Banco de Dados NoSQL", "descricao": "Modelagem de dados com MongoDB na prática.", "categoria": "minicurso", "dataHora": "2026-09-22T18:30:00", "local": "Laboratório 2", "vagas": 20, "imagemUrl": "https://picsum.photos/seed/evento5/600/300" },
    { "id": 6, "titulo": "Workshop de Testes Automatizados", "descricao": "Testes unitários e de integração em aplicações web.", "categoria": "workshop", "dataHora": "2026-10-05T14:00:00", "local": "Sala 12", "vagas": 25, "imagemUrl": "https://picsum.photos/seed/evento6/600/300" },
    { "id": 7, "titulo": "Palestra: Ética em Inteligência Artificial", "descricao": "Discussão sobre vieses e responsabilidade em sistemas de IA.", "categoria": "palestra", "dataHora": "2026-10-10T19:00:00", "local": "Auditório Central", "vagas": 60, "imagemUrl": "https://picsum.photos/seed/evento7/600/300" },
    { "id": 8, "titulo": "Minicurso de Node.js e Express", "descricao": "Construindo APIs REST do zero.", "categoria": "minicurso", "dataHora": "2026-09-25T18:30:00", "local": "Laboratório 1", "vagas": 25, "imagemUrl": "https://picsum.photos/seed/evento8/600/300" }
  ],
  "inscricoes": []
}
```

### Rodando o servidor

```bash
npx json-server --watch db.json --port 3000
```

Isso sobe uma API completa em `http://localhost:3000`, com:

- `GET /eventos` — lista todos os eventos.
- `GET /eventos/3` — retorna o evento com `id: 3`, ou `404` se não existir.
- `GET /eventos?categoria=palestra` — filtro por campo exato.
- `GET /eventos?titulo_like=vue` — busca parcial, sem diferenciar maiúsculas/minúsculas.
- `POST /eventos` — cria um evento novo (retorna `201`).
- `PUT /eventos/3` — substitui o evento `3` inteiro.
- `PATCH /eventos/3` — atualiza campos específicos do evento `3`.
- `DELETE /eventos/3` — remove o evento `3` (retorna `200` com corpo vazio no json-server).

O `--watch` faz o json-server recarregar automaticamente sempre que `db.json` é editado manualmente — útil para resetar o estado de teste durante a aula.

> **💡 Dica:** rode o `json-server` e o `npm run dev` do Vite em dois terminais separados. Nenhum dos dois substitui o outro — um serve a API, o outro serve a aplicação Vue.

> **🔎 Por baixo do capô:** o `json-server` não é o que você vai construir de verdade. Ele existe para permitir treinar consumo de API **antes** de saber construir uma. Na Unidade 3 (Aulas 07–08), você vai construir a API real do UniEventos com Express, replicando esses mesmos endpoints — e aí vai entender por dentro o que o json-server faz por baixo dos panos.

## 5. Pinia: estado compartilhado de verdade

### O problema do prop drilling e do estado espalhado

Na Aula 05, você usou `provide`/`inject` para dados amplamente compartilhados, e o composable `useEventos` para lógica reutilizável. Mas o composable tem uma limitação: **cada componente que o chama recebe seu próprio estado isolado**. Se a `HomeView` e o `CabecalhoApp` chamarem `useEventos()` separadamente, cada um tem sua própria cópia da lista de eventos — atualizar uma não atualiza a outra.

Para estado que precisa ser **verdadeiramente compartilhado** — a lista de eventos carregada uma vez e usada em várias telas, as inscrições do usuário, o carrinho de um e-commerce —, a resposta é uma **store**: um único objeto reativo, acessível de qualquer componente, sem precisar passar por props em cada nível da árvore.

### Pinia: `createPinia`

O Pinia já vem instalado e registrado se você criou o projeto com a flag `--pinia` (como recomenda a §4 da especificação):

```js
// src/main.js (trecho, já presente no scaffold)
import { createPinia } from 'pinia'
// ...
app.use(createPinia())
```

### `defineStore`: dois estilos

Pinia suporta dois estilos de declaração de store. **Esta disciplina usa o setup store** — mas você precisa reconhecer os dois, porque o estilo options ainda aparece bastante em projetos e tutoriais existentes.

**Options store** (parecido com a Options API do Vue 2):

```js
// exemplo — NÃO é o estilo usado nesta disciplina, mas você deve reconhecê-lo
import { defineStore } from 'pinia'

export const useContadorStore = defineStore('contador', {
  state: () => ({ valor: 0 }),
  getters: {
    dobro: (state) => state.valor * 2,
  },
  actions: {
    incrementar() {
      this.valor++
    },
  },
})
```

**Setup store** (usa a Composition API — `ref`, `computed`, funções comuns):

```js
// src/stores/contadorStore.js — estilo usado nesta disciplina
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useContadorStore = defineStore('contador', () => {
  const valor = ref(0)
  const dobro = computed(() => valor.value * 2)

  function incrementar() {
    valor.value++
  }

  return { valor, dobro, incrementar }
})
```

No setup store: `ref` vira **state**, `computed` vira **getter**, função comum vira **action** — e você retorna explicitamente tudo que deve ficar público. É o mesmo modelo mental que você já usa em `<script setup>` e em composables, o que reduz a curva de aprendizado: uma store é, na prática, um composable que vive fora de qualquer componente e é compartilhado por todos eles.

> **📌 Na prova:** se te perguntarem a diferença entre uma store setup e um composable comum, a resposta central é: **uma store é um singleton** (uma instância única compartilhada por toda a aplicação, gerenciada pelo Pinia); **um composable comum cria estado novo a cada chamada**. Veja o box de padrões de projeto logo abaixo.

### `storeToRefs` — por que desestruturar direto quebra a reatividade

```js
import { useEventosStore } from '../stores/eventosStore'

const store = useEventosStore()

// ERRADO — quebra a reatividade
const { eventos, carregando } = store
```

Desestruturar propriedades reativas diretamente de `store` **quebra a reatividade**: `eventos` e `carregando` viram cópias estáticas do valor no momento da desestruturação, desconectadas da store. Se a store atualizar depois, essas variáveis locais não acompanham.

```js
import { storeToRefs } from 'pinia'
import { useEventosStore } from '../stores/eventosStore'

const store = useEventosStore()
const { eventos, carregando } = storeToRefs(store) // CORRETO — mantém reatividade

// ações continuam sendo chamadas direto da store, sem storeToRefs
store.carregarEventos()
```

`storeToRefs` converte cada propriedade de state/getter em um `ref` reativo de verdade, ligado à store original. **Ações** (funções) não precisam desse tratamento — elas não são reativas, só são chamadas — então continuam sendo acessadas direto de `store.nomeDaAcao()`.

> **🔎 Por baixo do capô:** isso acontece pela mesma razão pela qual desestruturar um `reactive()` comum quebra a reatividade (você viu isso na Aula 03, ao estudar `reactive` vs. `ref`): a store internamente é um objeto `reactive`, e desestruturar um `reactive` extrai o **valor primitivo** naquele instante, perdendo o Proxy que rastreia mudanças. `storeToRefs` contorna isso criando um `ref` para cada propriedade, que continua "ligado" ao Proxy original.

### Store completa: `eventosStore.js`

```js
// src/stores/eventosStore.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import eventosService from '../services/eventosService'

export const useEventosStore = defineStore('eventos', () => {
  const eventos = ref([])
  const carregando = ref(false)
  const erro = ref(null)
  const categoriaFiltro = ref('Todas')
  const busca = ref('')

  const eventosFiltrados = computed(() => {
    return eventos.value.filter((evento) => {
      const bateCategoria =
        categoriaFiltro.value === 'Todas' ||
        evento.categoria === categoriaFiltro.value.toLowerCase()
      const bateBusca = evento.titulo
        .toLowerCase()
        .includes(busca.value.toLowerCase())
      return bateCategoria && bateBusca
    })
  })

  async function carregarEventos() {
    carregando.value = true
    erro.value = null
    try {
      eventos.value = await eventosService.listar()
    } catch (e) {
      erro.value = 'Não foi possível carregar os eventos. Tente novamente.'
    } finally {
      carregando.value = false
    }
  }

  async function removerEvento(id) {
    await eventosService.remover(id)
    eventos.value = eventos.value.filter((e) => e.id !== id)
  }

  async function salvarEvento(dadosEvento) {
    if (dadosEvento.id) {
      const atualizado = await eventosService.atualizar(dadosEvento.id, dadosEvento)
      const indice = eventos.value.findIndex((e) => e.id === dadosEvento.id)
      if (indice !== -1) eventos.value[indice] = atualizado
    } else {
      const criado = await eventosService.criar(dadosEvento)
      eventos.value.push(criado)
    }
  }

  function $reset() {
    eventos.value = []
    carregando.value = false
    erro.value = null
    categoriaFiltro.value = 'Todas'
    busca.value = ''
  }

  return {
    eventos,
    carregando,
    erro,
    categoriaFiltro,
    busca,
    eventosFiltrados,
    carregarEventos,
    removerEvento,
    salvarEvento,
    $reset,
  }
})
```

### Ações assíncronas

Repare que `carregarEventos`, `removerEvento` e `salvarEvento` são funções `async` comuns — Pinia não exige nenhuma sintaxe especial para ações assíncronas. O padrão `carregando`/`erro` como state da própria store (em vez de `ref`s locais em cada componente) é o que permite que **qualquer tela** mostre o estado de carregamento correto, sem duplicar essa lógica.

### `$reset`, `$patch`, `$subscribe`

```js
const store = useEventosStore()

// $reset — no setup store, você define sua própria função $reset (como acima),
// pois o Pinia só gera $reset automaticamente para options stores
store.$reset()

// $patch — atualiza várias propriedades de uma vez, útil para mudanças em lote
store.$patch({ categoriaFiltro: 'Palestra', busca: '' })

// $patch também aceita uma função, útil quando a mudança depende do estado atual
store.$patch((state) => {
  state.eventos.push({ id: 99, titulo: 'Evento de teste' })
})

// $subscribe — reage a qualquer mudança de state da store (ótimo para persistência/log)
store.$subscribe((mutation, state) => {
  console.log('Store eventos mudou:', mutation.type, state)
})
```

> **⚠️ Atenção:** em uma **setup store**, `$reset()` não é gerado automaticamente pelo Pinia (isso só acontece no estilo options store) — por isso a store acima define sua própria função `$reset` manualmente e a expõe no `return`. É um detalhe pequeno, mas comum de esquecer.

### Composição de stores

Uma store pode usar outra dentro de si, exatamente como um composable usa outro:

```js
// src/stores/inscricoesStore.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useEventosStore } from './eventosStore'

export const useInscricoesStore = defineStore('inscricoes', () => {
  const eventosStore = useEventosStore()

  const idsInscritos = ref(
    JSON.parse(localStorage.getItem('uniEventosInscricoes') || '[]')
  )

  const eventosInscritos = computed(() =>
    eventosStore.eventos.filter((evento) => idsInscritos.value.includes(evento.id))
  )

  function inscrever(idEvento) {
    if (!idsInscritos.value.includes(idEvento)) {
      idsInscritos.value.push(idEvento)
      persistir()
    }
  }

  function cancelarInscricao(idEvento) {
    idsInscritos.value = idsInscritos.value.filter((id) => id !== idEvento)
    persistir()
  }

  function estaInscrito(idEvento) {
    return idsInscritos.value.includes(idEvento)
  }

  function persistir() {
    localStorage.setItem('uniEventosInscricoes', JSON.stringify(idsInscritos.value))
  }

  return {
    idsInscritos,
    eventosInscritos,
    inscrever,
    cancelarInscricao,
    estaInscrito,
  }
})
```

`useInscricoesStore` depende de `useEventosStore` para calcular `eventosInscritos` — uma composição direta, sem nenhuma cerimônia especial: dentro do setup store, você simplesmente chama `useEventosStore()` como chamaria em qualquer componente.

### Persistência em `localStorage`

A `inscricoesStore` acima já persiste manualmente, chamando `persistir()` a cada mudança. Uma alternativa mais genérica é usar `$subscribe` para persistir qualquer mudança de state automaticamente, sem espalhar chamadas de `localStorage.setItem` pelas ações:

```js
// src/stores/inscricoesStore.js (trecho — alternativa com $subscribe)
export const useInscricoesStore = defineStore('inscricoes', () => {
  const idsInscritos = ref(
    JSON.parse(localStorage.getItem('uniEventosInscricoes') || '[]')
  )

  function inscrever(idEvento) {
    if (!idsInscritos.value.includes(idEvento)) {
      idsInscritos.value.push(idEvento)
    }
  }

  function cancelarInscricao(idEvento) {
    idsInscritos.value = idsInscritos.value.filter((id) => id !== idEvento)
  }

  return { idsInscritos, inscrever, cancelarInscricao }
})
```

```js
// src/main.js (trecho — assinatura global, fora da store)
import { useInscricoesStore } from './stores/inscricoesStore'

const inscricoesStore = useInscricoesStore()
inscricoesStore.$subscribe((mutation, state) => {
  localStorage.setItem('uniEventosInscricoes', JSON.stringify(state.idsInscritos))
})
```

Ambas as abordagens são válidas; a primeira (persistir dentro da própria ação) é mais explícita e fácil de acompanhar em uma disciplina introdutória — é a que vamos usar no Mão na massa.

### Vue DevTools inspecionando a store

Instale a extensão **Vue DevTools** no navegador (ou use `vite-plugin-vue-devtools`, incluído por padrão em muitos scaffolds do `create-vue`). Na aba **Pinia**, você vê, em tempo real: todas as stores ativas, o state atual de cada uma, e um histórico de mutações — útil para depurar por que `eventosFiltrados` não está retornando o que você espera, sem precisar espalhar `console.log` pelo código.

## 🧩 Padrão de projeto em uso

> ### 🧩 Padrão de projeto em uso — Singleton e Decorator
>
> **Singleton (criacional):** uma store Pinia é, por construção, uma instância única compartilhada. Não importa quantas vezes `useEventosStore()` seja chamado, em quantos componentes diferentes — todos recebem **a mesma instância** de store, gerenciada internamente pelo Pinia (identificada pelo primeiro argumento de `defineStore`, `'eventos'`). Isso é exatamente o padrão Singleton: garantir que existe no máximo uma instância de um objeto, e fornecer um ponto de acesso global a ela. É a diferença estrutural entre uma store e um composable comum — o composable cria estado novo a cada chamada; a store sempre devolve a mesma instância.
>
> **Decorator (estrutural):** os interceptors do Axios são um exemplo direto de Decorator. Cada interceptor "envolve" a requisição (ou resposta) original, adicionando comportamento sem alterar o código que originou a chamada — o interceptor de request adiciona o header `Authorization`; o interceptor de response adiciona tratamento de `401`. O componente que chama `http.get('/eventos')` não sabe (nem precisa saber) que essas camadas extras existem — elas são "decoradas" por fora, de forma transparente.

## 💻 Mão na massa — UniEventos consumindo API real

### Passo 1 — instalar Axios e criar `db.json`

```bash
npm install axios
```

Crie `db.json` na raiz do projeto (conteúdo completo na §4 acima), e rode em um terminal separado:

```bash
npx json-server --watch db.json --port 3000
```

Deixe esse terminal aberto durante toda a aula — é a "API" que o front vai consumir.

### Passo 2 — criar a instância HTTP

```js
// src/services/http.js
import axios from 'axios'

const http = axios.create({
  baseURL: 'http://localhost:3000',
  timeout: 8000,
  headers: {
    'Content-Type': 'application/json',
  },
})

http.interceptors.request.use((config) => {
  const token = localStorage.getItem('uniEventosToken')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

http.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('uniEventosToken')
    }
    return Promise.reject(error)
  }
)

export default http
```

### Passo 3 — criar `eventosService.js`

```js
// src/services/eventosService.js
import http from './http'

export default {
  async listar(filtros = {}) {
    const resposta = await http.get('/eventos', { params: filtros })
    return resposta.data
  },

  async buscarPorId(id) {
    const resposta = await http.get(`/eventos/${id}`)
    return resposta.data
  },

  async criar(evento) {
    const resposta = await http.post('/eventos', evento)
    return resposta.data
  },

  async atualizar(id, evento) {
    const resposta = await http.put(`/eventos/${id}`, evento)
    return resposta.data
  },

  async remover(id) {
    await http.delete(`/eventos/${id}`)
  },
}
```

### Passo 4 — criar `eventosStore.js`

```js
// src/stores/eventosStore.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import eventosService from '../services/eventosService'

export const useEventosStore = defineStore('eventos', () => {
  const eventos = ref([])
  const carregando = ref(false)
  const erro = ref(null)
  const categoriaFiltro = ref('Todas')
  const busca = ref('')

  const eventosFiltrados = computed(() => {
    return eventos.value.filter((evento) => {
      const bateCategoria =
        categoriaFiltro.value === 'Todas' ||
        evento.categoria === categoriaFiltro.value.toLowerCase()
      const bateBusca = evento.titulo
        .toLowerCase()
        .includes(busca.value.toLowerCase())
      return bateCategoria && bateBusca
    })
  })

  async function carregarEventos() {
    carregando.value = true
    erro.value = null
    try {
      eventos.value = await eventosService.listar()
    } catch (e) {
      erro.value = 'Não foi possível carregar os eventos. Verifique se o json-server está rodando.'
    } finally {
      carregando.value = false
    }
  }

  async function removerEvento(id) {
    await eventosService.remover(id)
    eventos.value = eventos.value.filter((e) => e.id !== id)
  }

  async function salvarEvento(dadosEvento) {
    if (dadosEvento.id) {
      const atualizado = await eventosService.atualizar(dadosEvento.id, dadosEvento)
      const indice = eventos.value.findIndex((e) => e.id === dadosEvento.id)
      if (indice !== -1) eventos.value[indice] = atualizado
    } else {
      const criado = await eventosService.criar(dadosEvento)
      eventos.value.push(criado)
    }
  }

  function $reset() {
    eventos.value = []
    carregando.value = false
    erro.value = null
    categoriaFiltro.value = 'Todas'
    busca.value = ''
  }

  return {
    eventos,
    carregando,
    erro,
    categoriaFiltro,
    busca,
    eventosFiltrados,
    carregarEventos,
    removerEvento,
    salvarEvento,
    $reset,
  }
})
```

### Passo 5 — criar `inscricoesStore.js`

```js
// src/stores/inscricoesStore.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useEventosStore } from './eventosStore'

const CHAVE_LOCALSTORAGE = 'uniEventosInscricoes'

export const useInscricoesStore = defineStore('inscricoes', () => {
  const eventosStore = useEventosStore()

  const idsInscritos = ref(
    JSON.parse(localStorage.getItem(CHAVE_LOCALSTORAGE) || '[]')
  )

  const eventosInscritos = computed(() =>
    eventosStore.eventos.filter((evento) => idsInscritos.value.includes(evento.id))
  )

  function persistir() {
    localStorage.setItem(CHAVE_LOCALSTORAGE, JSON.stringify(idsInscritos.value))
  }

  function inscrever(idEvento) {
    if (!idsInscritos.value.includes(idEvento)) {
      idsInscritos.value.push(idEvento)
      persistir()
    }
  }

  function cancelarInscricao(idEvento) {
    idsInscritos.value = idsInscritos.value.filter((id) => id !== idEvento)
    persistir()
  }

  function estaInscrito(idEvento) {
    return idsInscritos.value.includes(idEvento)
  }

  return {
    idsInscritos,
    eventosInscritos,
    inscrever,
    cancelarInscricao,
    estaInscrito,
  }
})
```

### Passo 6 — atualizar `HomeView.vue` para usar a store

```vue
<!-- src/views/HomeView.vue -->
<script setup>
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useEventosStore } from '../stores/eventosStore'
import FiltroEventos from '../components/FiltroEventos.vue'
import EventoLista from '../components/EventoLista.vue'

const store = useEventosStore()
const { carregando, erro, categoriaFiltro, busca, eventosFiltrados } = storeToRefs(store)

onMounted(() => {
  store.carregarEventos()
})
</script>

<template>
  <v-container>
    <h1 class="text-h4 mb-4">Eventos disponíveis</h1>

    <FiltroEventos v-model:busca="busca" v-model:categoria="categoriaFiltro" />

    <div v-if="carregando" class="d-flex justify-center pa-8">
      <v-skeleton-loader type="card" v-for="n in 3" :key="n" class="mb-4" />
    </div>

    <v-alert v-else-if="erro" type="error" variant="tonal" title="Erro ao carregar eventos">
      {{ erro }}
    </v-alert>

    <v-alert
      v-else-if="eventosFiltrados.length === 0"
      type="info"
      variant="tonal"
      title="Nenhum evento encontrado"
    >
      Tente ajustar os filtros de categoria ou o termo de busca.
    </v-alert>

    <EventoLista v-else :eventos="eventosFiltrados" />
  </v-container>
</template>
```

Note os três estados de tela que você já pratica desde a Aula 03 (carregando / erro / vazio), agora alimentados pela store em vez de lógica local — e uma quarta condição implícita (dados carregados com sucesso), coberta pelo `v-else` final.

### Passo 7 — feedback com `v-snackbar` na inscrição

```vue
<!-- src/views/EventoDetalheView.vue -->
<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useEventosStore } from '../stores/eventosStore'
import { useInscricoesStore } from '../stores/inscricoesStore'

const rota = useRoute()
const router = useRouter()

const eventosStore = useEventosStore()
const { eventos } = storeToRefs(eventosStore)

const inscricoesStore = useInscricoesStore()

const snackbarAberto = ref(false)
const snackbarMensagem = ref('')
const snackbarCor = ref('success')

onMounted(() => {
  if (eventos.value.length === 0) {
    eventosStore.carregarEventos()
  }
})

const evento = computed(() =>
  eventos.value.find((e) => e.id === Number(rota.params.id))
)

const jaInscrito = computed(() =>
  evento.value ? inscricoesStore.estaInscrito(evento.value.id) : false
)

function formatarDataHora(dataIso) {
  return new Date(dataIso).toLocaleString('pt-BR', {
    dateStyle: 'long',
    timeStyle: 'short',
  })
}

function inscrever() {
  inscricoesStore.inscrever(evento.value.id)
  snackbarMensagem.value = 'Inscrição realizada com sucesso!'
  snackbarCor.value = 'success'
  snackbarAberto.value = true
}

function cancelarInscricao() {
  inscricoesStore.cancelarInscricao(evento.value.id)
  snackbarMensagem.value = 'Inscrição cancelada.'
  snackbarCor.value = 'warning'
  snackbarAberto.value = true
}

function voltar() {
  router.push({ name: 'home' })
}
</script>

<template>
  <v-container>
    <v-btn variant="text" prepend-icon="mdi-arrow-left" class="mb-4" @click="voltar">
      Voltar para eventos
    </v-btn>

    <v-alert v-if="!evento" type="error" variant="tonal" title="Evento não encontrado">
      Não existe evento com este identificador. Confira o link acessado.
    </v-alert>

    <v-card v-else>
      <v-img :src="evento.imagemUrl" height="280" cover />
      <v-card-title class="text-h5">{{ evento.titulo }}</v-card-title>
      <v-card-subtitle>
        <v-icon icon="mdi-calendar" size="small" class="mr-1" />
        {{ formatarDataHora(evento.dataHora) }}
      </v-card-subtitle>
      <v-card-text>
        <p class="mb-4">{{ evento.descricao }}</p>
        <div class="d-flex align-center mb-2">
          <v-icon icon="mdi-map-marker" class="mr-2" />
          <span>{{ evento.local }}</span>
        </div>
        <div class="d-flex align-center">
          <v-icon icon="mdi-account-group" class="mr-2" />
          <span>{{ evento.vagas }} vagas disponíveis</span>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-chip color="secondary">{{ evento.categoria }}</v-chip>
        <v-spacer />
        <v-btn v-if="!jaInscrito" color="primary" variant="flat" @click="inscrever">
          Inscrever-se
        </v-btn>
        <v-btn v-else color="error" variant="outlined" @click="cancelarInscricao">
          Cancelar inscrição
        </v-btn>
      </v-card-actions>
    </v-card>

    <v-snackbar v-model="snackbarAberto" :color="snackbarCor" timeout="3000">
      {{ snackbarMensagem }}
    </v-snackbar>
  </v-container>
</template>
```

### Passo 8 — atualizar `AdminEventosView.vue` e o formulário para usar a store

```vue
<!-- src/views/admin/AdminEventosView.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useEventosStore } from '../../stores/eventosStore'
import DialogoConfirmacao from '../../components/DialogoConfirmacao.vue'

const store = useEventosStore()
const { eventos, carregando, erro } = storeToRefs(store)

const dialogoAberto = ref(false)
const eventoParaExcluir = ref(null)
const busca = ref('')
const snackbarAberto = ref(false)

const cabecalhos = [
  { title: 'Título', key: 'titulo' },
  { title: 'Categoria', key: 'categoria' },
  { title: 'Vagas', key: 'vagas' },
  { title: 'Ações', key: 'acoes', sortable: false },
]

onMounted(() => {
  if (eventos.value.length === 0) store.carregarEventos()
})

function pedirExclusao(evento) {
  eventoParaExcluir.value = evento
  dialogoAberto.value = true
}

async function confirmarExclusao() {
  await store.removerEvento(eventoParaExcluir.value.id)
  eventoParaExcluir.value = null
  snackbarAberto.value = true
}
</script>

<template>
  <div>
    <div class="d-flex justify-space-between align-center mb-4">
      <v-text-field
        v-model="busca"
        label="Buscar"
        prepend-inner-icon="mdi-magnify"
        density="compact"
        style="max-width: 300px"
      />
      <v-btn color="primary" prepend-icon="mdi-plus" :to="{ name: 'admin-evento-novo' }">
        Novo evento
      </v-btn>
    </div>

    <v-alert v-if="erro" type="error" variant="tonal" class="mb-4">{{ erro }}</v-alert>

    <v-data-table
      :headers="cabecalhos"
      :items="eventos"
      :search="busca"
      :loading="carregando"
      items-per-page="5"
    >
      <template #item.acoes="{ item }">
        <v-btn
          icon="mdi-pencil"
          size="small"
          variant="text"
          :to="{ name: 'admin-evento-editar', params: { id: item.id } }"
        />
        <v-btn
          icon="mdi-delete"
          size="small"
          variant="text"
          color="error"
          @click="pedirExclusao(item)"
        />
      </template>
    </v-data-table>

    <DialogoConfirmacao
      v-model="dialogoAberto"
      titulo="Excluir evento"
      :mensagem="`Excluir '${eventoParaExcluir?.titulo}'? Esta ação não pode ser desfeita.`"
      @confirmar="confirmarExclusao"
    />

    <v-snackbar v-model="snackbarAberto" color="success" timeout="3000">
      Evento excluído com sucesso.
    </v-snackbar>
  </div>
</template>
```

```vue
<!-- src/views/admin/AdminEventoFormView.vue -->
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter, onBeforeRouteLeave } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useEventosStore } from '../../stores/eventosStore'

const rota = useRoute()
const router = useRouter()
const store = useEventosStore()
const { eventos } = storeToRefs(store)

const modoEdicao = computed(() => rota.name === 'admin-evento-editar')
const formRef = ref(null)
const formularioAlterado = ref(false)
const salvando = ref(false)
const erroSalvar = ref(null)

const titulo = ref('')
const descricao = ref('')
const categoria = ref('palestra')
const local = ref('')
const vagas = ref(null)

const categorias = ['palestra', 'minicurso', 'workshop']

const regrasTitulo = [
  (v) => !!v || 'O título é obrigatório',
  (v) => (v && v.length >= 5) || 'Mínimo de 5 caracteres',
]
const regrasLocal = [(v) => !!v || 'O local é obrigatório']
const regrasVagas = [
  (v) => !!v || 'Informe o número de vagas',
  (v) => v > 0 || 'Deve ser maior que zero',
]

onMounted(() => {
  if (modoEdicao.value) {
    const evento = eventos.value.find((e) => e.id === Number(rota.params.id))
    if (evento) {
      titulo.value = evento.titulo
      descricao.value = evento.descricao
      categoria.value = evento.categoria
      local.value = evento.local
      vagas.value = evento.vagas
    }
  }
})

onBeforeRouteLeave(() => {
  if (formularioAlterado.value) {
    const confirmar = window.confirm('Existem alterações não salvas. Sair mesmo assim?')
    if (!confirmar) return false
  }
})

async function salvar() {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  salvando.value = true
  erroSalvar.value = null
  try {
    await store.salvarEvento({
      id: modoEdicao.value ? Number(rota.params.id) : undefined,
      titulo: titulo.value,
      descricao: descricao.value,
      categoria: categoria.value,
      local: local.value,
      vagas: vagas.value,
      dataHora: new Date().toISOString(),
      imagemUrl: `https://picsum.photos/seed/evento${Date.now()}/600/300`,
    })
    formularioAlterado.value = false
    router.push({ name: 'admin-eventos' })
  } catch (e) {
    erroSalvar.value = 'Não foi possível salvar o evento. Tente novamente.'
  } finally {
    salvando.value = false
  }
}
</script>

<template>
  <v-card class="pa-4">
    <v-card-title>{{ modoEdicao ? 'Editar evento' : 'Novo evento' }}</v-card-title>
    <v-card-text>
      <v-alert v-if="erroSalvar" type="error" variant="tonal" class="mb-4">{{ erroSalvar }}</v-alert>
      <v-form ref="formRef" @submit.prevent="salvar" @update:model-value="formularioAlterado = true">
        <v-text-field v-model="titulo" label="Título" :rules="regrasTitulo" class="mb-2" />
        <v-textarea v-model="descricao" label="Descrição" rows="3" class="mb-2" />
        <v-select v-model="categoria" :items="categorias" label="Categoria" class="mb-2" />
        <v-text-field v-model="local" label="Local" :rules="regrasLocal" class="mb-2" />
        <v-text-field v-model.number="vagas" label="Vagas" type="number" :rules="regrasVagas" class="mb-4" />
        <v-btn type="submit" color="primary" variant="flat" :loading="salvando">Salvar</v-btn>
        <v-btn variant="text" class="ml-2" :to="{ name: 'admin-eventos' }">Cancelar</v-btn>
      </v-form>
    </v-card-text>
  </v-card>
</template>
```

### Passo 9 — testar de ponta a ponta

Com o `json-server` rodando em um terminal e `npm run dev` em outro: a home carrega eventos da API (confira na aba Rede do navegador que a requisição `GET http://localhost:3000/eventos` acontece); inscrever-se em um evento persiste em `localStorage` (recarregue a página — a inscrição continua marcada); editar um evento na área administrativa reflete na home; derrubar o `json-server` (Ctrl+C) e recarregar a home deve mostrar o alerta de erro, não uma tela quebrada.

## 🧪 Laboratório

**1. Cancelamento de requisição na busca**
Aplique a técnica de `AbortController` da §2 no `eventosService.listar`, cancelando a busca anterior sempre que o usuário digitar um novo termo antes da resposta anterior chegar.

<details markdown="1">
<summary>Dica</summary>

Guarde a instância de `AbortController` em uma variável de módulo dentro do próprio serviço, como no exemplo da §2.
</details>

**2. Getter `totalPorCategoria` na store**
Adicione um `computed` em `eventosStore.js` chamado `totalPorCategoria`, que retorna um objeto `{ palestra: n, minicurso: n, workshop: n }` contando eventos de cada categoria. Exiba isso em três `v-chip` no `AdminHomeView.vue`.

<details markdown="1">
<summary>Dica</summary>

`eventos.value.reduce((acc, e) => { acc[e.categoria] = (acc[e.categoria] || 0) + 1; return acc }, {})`.
</details>

**3. `$subscribe` para log de auditoria**
No `main.js`, use `eventosStore.$subscribe` para imprimir no console, a cada mudança, quantos eventos existem na store — útil para depurar sincronizações inesperadas.

<details markdown="1">
<summary>Dica</summary>

`store.$subscribe((mutation, state) => console.log('eventos:', state.eventos.length))`, chamado após `app.mount('#app')`.
</details>

**4. Tratamento de erro de rede real**
Derrube o `json-server` propositalmente e force um `erro.request` (não `erro.response`). Ajuste `eventosStore.carregarEventos` para mostrar uma mensagem diferente quando o erro for de conexão (sem resposta) versus quando for um erro HTTP com resposta.

<details markdown="1">
<summary>Dica</summary>

Dentro do `catch`, verifique `if (e.response) { ... } else if (e.request) { ... }`, como na §2.
</details>

**5. Persistência de tema com Pinia**
Crie `src/stores/preferenciasStore.js` com uma setup store que guarda o tema atual (`'light'`/`'dark'`), persiste em `localStorage` e é usada pelo `CabecalhoApp.vue` no lugar da lógica local de `useTheme()` isolada.

<details markdown="1">
<summary>Dica</summary>

A store guarda o nome do tema em um `ref`; um `watch` sobre esse `ref` chama `tema.global.name.value = novoValor` e `localStorage.setItem`.
</details>

## 🐛 Erros comuns e como resolver

| Sintoma | Causa | Solução |
|---|---|---|
| Erro de CORS no console, requisição bloqueada | Servidor não autoriza a origem do front-end | Confirme que o `json-server` está rodando (ele libera CORS por padrão); em uma API própria, configure o header `Access-Control-Allow-Origin` |
| `eventos.value` nunca atualiza na tela, mesmo a store mudando | Desestruturação direta da store (`const { eventos } = store`) em vez de `storeToRefs` | Use `storeToRefs(store)` para state/getters; ações continuam vindo direto de `store.acao()` |
| `store.$reset is not a function` | Setup store não define `$reset` manualmente — Pinia só gera isso automaticamente em options stores | Declare uma função `$reset` na própria store e inclua-a no `return` |
| `Cannot read properties of undefined (reading 'status')` no `catch` de um erro Axios | Tentando ler `erro.response.status` quando o erro é `erro.request` (sem resposta) | Sempre cheque `erro.response` antes de acessar `erro.response.status` |
| `json-server` responde, mas com `404` em toda requisição | Nome da propriedade no `db.json` não bate com a rota chamada (ex.: `db.json` tem `"evento"` no singular, mas o serviço chama `/eventos`) | O nome da chave raiz do `db.json` define o endpoint — confira a grafia exata |
| Inscrição some ao recarregar a página | `localStorage.setItem` não está sendo chamado após a mutação, ou a chave usada na leitura é diferente da usada na escrita | Confirme que `persistir()` roda em toda ação que muda `idsInscritos`, e que a chave é idêntica nos dois lugares |
| Interceptor de request não injeta o token | Token não existe ainda em `localStorage` (usuário nunca logou) ou a chave usada é diferente da chave de login | Confirme a chave (`uniEventosToken`) e teste manualmente com `localStorage.setItem('uniEventosToken', 'teste')` |

## 🏠 Atividade assíncrona (1 h)

No seu **projeto autoral**:

1. Crie um `db.json` com os mesmos dados do seu domínio (mínimo 8 registros) e suba com `json-server`.
2. Crie `src/services/http.js` com instância dedicada, interceptor de request e de response.
3. Crie um serviço (`*Service.js`) com pelo menos `listar`, `buscarPorId`, `criar`, `remover`.
4. Crie uma store Pinia (setup store) para o recurso principal do seu domínio, com `carregando`, `erro` e ao menos uma ação assíncrona.
5. Conecte pelo menos uma tela à store usando `storeToRefs`, com feedback de `v-snackbar` em pelo menos uma ação (criar, excluir ou favoritar).

**Critério de pronto:** a tela principal carrega dados reais do `json-server` (não mais do array estático); desligar o `json-server` e recarregar mostra uma mensagem de erro, não uma tela em branco ou quebrada. Suba o commit.

## ✅ Checkpoint do projeto autoral

- [ ] `db.json` criado com pelo menos 8 registros do domínio autoral.
- [ ] `src/services/http.js` com instância Axios dedicada e ao menos um interceptor.
- [ ] Camada de serviço (`*Service.js`) usada por pelo menos uma store — nenhum componente chama Axios direto.
- [ ] Pelo menos uma setup store Pinia com state, getter e ação assíncrona.
- [ ] `storeToRefs` usado corretamente em pelo menos uma tela.
- [ ] Estado de carregando/erro refletido visualmente na interface (skeleton ou spinner + alert).
- [ ] Alguma forma de persistência em `localStorage` (favoritos, inscrições, tema — a seu critério).

## 📚 Para aprofundar

- Documentação oficial do Axios: <https://axios-http.com/docs/intro>
- MDN — CORS: <https://developer.mozilla.org/pt-BR/docs/Web/HTTP/CORS>
- MDN — Status HTTP: <https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Status>
- `json-server` (repositório oficial): <https://github.com/typicode/json-server>
- Documentação oficial do Pinia: <https://pinia.vuejs.org/>
- Pinia — setup stores: <https://pinia.vuejs.org/core-concepts/#setup-stores>
- Pinia — `storeToRefs`: <https://pinia.vuejs.org/core-concepts/state.html#accessing-the-state>
- Referências básicas do plano de curso: capítulos sobre consumo de API e gerenciamento de estado.

Isso encerra a Unidade 2. A **Avaliação 2** vence em **07/10/2026**, com as instruções completas de entrega na Aula 08 — mas o escopo, resumido em 5 linhas: seu projeto autoral deve consumir dados de uma API (própria ou `json-server`) através de uma camada de serviços com Axios; ter estado gerenciado por pelo menos uma store Pinia com `carregando`/`erro`; refletir esses estados visualmente na interface; persistir algum dado em `localStorage`; e manter tudo isso rodando em cima da estrutura de rotas e componentes que você já construiu nas Aulas 04 e 05. Comece a organizar seu `db.json` e sua camada de serviços desde já — não deixe para a última semana.
