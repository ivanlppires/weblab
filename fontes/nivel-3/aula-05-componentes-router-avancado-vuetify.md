# Aula 05 — Componentes, Vue Router e Vuetify avançado

> **Nível 3 — Frameworks Modernos** · Unidade 2: Vue.js avançado: Vuetify, Axios, Router e Pinia
> WebLab · UNEMAT Sinop · Prof. Ivan Luiz Pedroso Pires
> **Carga:** 3 aulas de 50 min (presencial) + 1 h (assíncrona)

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Decidir quando e como quebrar uma tela em componentes menores, distinguindo componentes "burros" (apresentação) de "inteligentes" (com lógica).
- Definir contratos de componente com `defineProps` (tipado, com `required`/`default`/`validator`) e `defineEmits`, incluindo `v-model` customizado com `defineModel()` e a forma clássica.
- Usar `provide`/`inject` para dados compartilhados em profundidade e controlar atributos fallthrough com `defineOptions({ inheritAttrs: false })`.
- Aplicar slots (padrão, nomeados e com escopo) para criar componentes de layout reutilizáveis.
- Extrair lógica reativa reutilizável em composables (`use*`) e explicar por que isso substitui mixins.
- Configurar rotas aninhadas, rotas nomeadas, `meta`, navigation guards e sincronizar filtros com query strings na URL.
- Construir formulários validados com `v-form`, listar dados com `v-data-table` e usar diálogos de confirmação, tabs, menus e skeleton loaders do Vuetify.

## 📋 Pré-requisitos desta aula

- [ ] UniEventos da Aula 04 rodando: Vuetify instalado, tema configurado, rotas `home`, `evento-detalhe`, `sobre`, `nao-encontrado` funcionando.
- [ ] Avaliação 1 entregue (ou em fase final de entrega).
- [ ] Domínio confortável de `<script setup>`, `defineProps`/`defineEmits` básicos (vistos rapidamente na Aula 02), `computed`, `onMounted`.

Na Aula 04 você transformou o UniEventos em uma SPA navegável: Vuetify instalado com tema institucional, `v-app-bar`/`v-navigation-drawer`/`v-main` no lugar, quatro rotas registradas e as views migradas para componentes Vuetify. O que ficou pendente é a organização interna: cada view ainda concentra marcação, dados e lógica no mesmo arquivo.

Hoje o UniEventos fica **modular**. Em vez de views monolíticas com tudo dentro, cada pedaço de interface vira um componente com contrato próprio — props de entrada, eventos de saída, slots para o que varia —, e a lógica reativa repetida sai das views para composables.

Na segunda metade da aula a área administrativa entra em cena, com rotas aninhadas, navigation guards, formulários validados com `v-form` e uma `v-data-table` de eventos. É o esqueleto que a Aula 06 vai conectar a uma API de verdade.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Componentização a sério: props, emits, `v-model` customizado, provide/inject, slots |
| 2 | 50 min | Composables, Vue Router avançado (rotas aninhadas, guards, query strings), formulários e `v-data-table` |
| 3 | 50 min | Mão na massa: refatoração do UniEventos em componentes + área administrativa |

## 1. Componentização a sério

Até aqui, cada view do UniEventos (`HomeView`, `EventoDetalheView`) concentrava template, lógica e estilo em um único arquivo. Isso funciona em uma tela pequena, mas cresce mal: a `HomeView` já mistura busca, filtro, grid de cards e lógica de carregamento — daqui a duas aulas, com formulário de cadastro e tabela administrativa, o arquivo viraria ilegível.

**Componentizar** é dividir a interface em peças menores, cada uma com uma responsabilidade única e um contrato explícito de entrada (props) e saída (emits). O benefício não é só organização de arquivo — é **reuso** (o mesmo `EventoCard` aparece na home, na busca e na área administrativa) e **testabilidade** (um componente pequeno é mais fácil de entender isoladamente).

### Granularidade: quando quebrar em componente

Não existe regra rígida, mas alguns sinais indicam que é hora de extrair um componente:

- O mesmo trecho de template se repete em duas ou mais telas (ex.: o card de evento).
- Um bloco do template tem lógica própria que não interessa ao componente pai (ex.: a lógica de validação de um campo de formulário).
- O arquivo passou de ~150–200 linhas e virou difícil de escanear visualmente.
- Você consegue nomear o pedaço com um substantivo claro (`EventoCard`, `FiltroEventos`, `CabecalhoApp`) — se não consegue nomear, talvez não seja um componente coerente ainda.

> **⚠️ Atenção:** granularidade excessiva também é problema. Um projeto com componentes de 5 linhas para cada `<span>` cria uma "sopa de componentes" difícil de navegar. Componentize quando há repetição ou responsabilidade clara — não por dogma.

### Componente burro vs. componente inteligente

Uma distinção útil (não uma regra do Vue, mas um padrão de arquitetura comum em SPAs):

- **Componente burro (presentational / dumb)** — só recebe dados via props e emite eventos. Não sabe de onde vêm os dados nem o que acontece depois do evento. Fácil de reutilizar e testar. Exemplo: `EventoCard`, que recebe um objeto `evento` e emite `@inscrever`.
- **Componente inteligente (container / smart)** — busca dados, decide o que fazer com eventos emitidos pelos filhos, conversa com store/API. Exemplo: `HomeView`, que carrega a lista de eventos e passa cada um para um `EventoCard`.

Essa separação evita que a lógica de negócio (como buscar dados, como filtrar) fique espalhada em componentes visuais pequenos — o que dificultaria trocar, por exemplo, a fonte de dados sem tocar em uma dezena de arquivos.

### `defineProps` com contrato completo

Você já usou `defineProps` de forma simples nas aulas anteriores. Um contrato robusto de props declara tipo, obrigatoriedade, valor padrão e validação:

```vue
<script setup>
const props = defineProps({
  evento: {
    type: Object,
    required: true,
  },
  destaque: {
    type: Boolean,
    default: false,
  },
  tamanhoImagem: {
    type: Number,
    default: 160,
    validator: (valor) => valor >= 100 && valor <= 400,
  },
})
</script>
```

- `type` habilita checagem em tempo de desenvolvimento — o Vue avisa no console se você passar um tipo errado.
- `required: true` faz o Vue emitir um aviso se a prop não for passada.
- `default` define um valor quando a prop não é informada (obrigatório para props opcionais que não são `required`).
- `validator` é uma função que recebe o valor e retorna `true`/`false` — útil para restringir um número a uma faixa, ou uma string a um conjunto de valores permitidos (`enum` informal).

> **💡 Dica:** props são **somente leitura** dentro do componente filho — nunca faça `props.evento = outraCoisa`. Se o filho precisa "mudar" algo que veio do pai, ele deve **emitir um evento** pedindo a mudança, e é o pai quem decide se atende.

### `defineEmits` e comunicação filho → pai

```vue
<!-- src/components/EventoCard.vue (trecho) -->
<script setup>
const props = defineProps({
  evento: { type: Object, required: true },
})

const emit = defineEmits({
  inscrever: (idEvento) => typeof idEvento === 'number',
  favoritar: null, // sem validação
})

function aoClicarInscrever() {
  emit('inscrever', props.evento.id)
}
</script>

<template>
  <v-card>
    <v-card-title>{{ evento.titulo }}</v-card-title>
    <v-card-subtitle>{{ evento.local }}</v-card-subtitle>
    <v-card-actions>
      <v-btn variant="text" @click="emit('favoritar', evento.id)">Favoritar</v-btn>
      <v-spacer />
      <v-btn color="primary" @click="aoClicarInscrever">Inscrever-se</v-btn>
    </v-card-actions>
  </v-card>
</template>
```

`defineEmits` declarado como objeto (em vez de array de strings) permite validar o payload de cada evento — assim como `defineProps` valida entradas, isso valida saídas. O componente pai escuta o evento normalmente:

```vue
<EventoCard :evento="evento" @inscrever="tratarInscricao" />
```

### `v-model` em componente customizado

Você já usa `v-model` em `v-text-field` e `v-dialog` — isso é possível porque esses componentes implementam o **contrato de `v-model`**. Você pode implementar o mesmo contrato nos seus próprios componentes, de duas formas.

**Forma moderna — `defineModel()` (Vue 3.4+):**

```vue
<!-- src/components/CampoBusca.vue -->
<script setup>
const modelo = defineModel({ type: String, default: '' })
</script>

<template>
  <v-text-field
    v-model="modelo"
    label="Buscar"
    prepend-inner-icon="mdi-magnify"
    variant="outlined"
    clearable
  />
</template>
```

```vue
<CampoBusca v-model="termoBusca" />
```

`defineModel()` cria automaticamente uma prop `modelValue` e um evento `update:modelValue` por baixo dos panos, expondo tudo como uma única variável reativa (`modelo`) que você lê e escreve como se fosse um `ref` comum. É a forma recomendada para código novo.

**Forma clássica — `modelValue` / `update:modelValue`:**

```vue
<!-- src/components/CampoBusca.vue (equivalente, forma clássica) -->
<script setup>
const props = defineProps({
  modelValue: { type: String, default: '' },
})
const emit = defineEmits(['update:modelValue'])
</script>

<template>
  <v-text-field
    :model-value="modelValue"
    label="Buscar"
    prepend-inner-icon="mdi-magnify"
    variant="outlined"
    clearable
    @update:model-value="emit('update:modelValue', $event)"
  />
</template>
```

As duas formas produzem exatamente o mesmo comportamento externo — `<CampoBusca v-model="termoBusca" />` funciona igual nos dois casos. `defineModel()` é mais curto e é o padrão desta disciplina daqui em diante, mas você vai encontrar a forma clássica em muito código existente (inclusive em bibliotecas), então precisa reconhecê-la.

> **🔎 Por baixo do capô:** `v-model="x"` em um componente é açúcar sintático para `:model-value="x" @update:model-value="x = $event"`. É exatamente o mesmo mecanismo de prop + evento que você já usa manualmente — só que com uma sintaxe mais curta, reconhecida pelo compilador do Vue.

### `provide`/`inject` para dados profundos

Passar props por 3 ou 4 níveis de componentes só para chegar a um neto profundo (**prop drilling**) é doloroso de manter. Para dados amplamente compartilhados — tema, usuário logado, configuração global —, o Vue oferece `provide`/`inject`:

```vue
<!-- src/App.vue (trecho) -->
<script setup>
import { provide, ref } from 'vue'

const usuarioLogado = ref({ nome: 'Convidado' })
provide('usuarioLogado', usuarioLogado)
</script>
```

```vue
<!-- src/components/PainelPerfil.vue (qualquer nível abaixo de App.vue) -->
<script setup>
import { inject } from 'vue'

const usuarioLogado = inject('usuarioLogado')
</script>

<template>
  <span>Olá, {{ usuarioLogado.nome }}</span>
</template>
```

`inject` encontra o valor mais próximo fornecido por um ancestral, não importa quantos níveis de componentes existam entre eles. Não é um substituto para comunicação local (props/emits continuam sendo a opção certa entre pai e filho diretos) — é uma ferramenta específica para dados "ambientais". Na Aula 06, o Pinia vai resolver a maior parte desses casos de forma mais estruturada; `provide`/`inject` ainda é útil para configuração de componentes de biblioteca (é assim, inclusive, que o próprio Vuetify propaga o tema).

### Atributos fallthrough e `inheritAttrs`

Quando você passa um atributo a um componente que não está declarado como prop, o Vue aplica automaticamente esse atributo à raiz do template do componente — isso se chama **fallthrough**:

```vue
<EventoCard :evento="evento" class="destaque" data-testid="card-evento" />
```

Se `EventoCard` não declara `class` nem `data-testid` como props, o Vue aplica os dois diretamente no elemento raiz do template de `EventoCard` (por exemplo, no `<v-card>`). Isso é conveniente na maioria dos casos — mas quando o componente tem múltiplos elementos raiz, ou quando você quer redirecionar o atributo para um elemento interno específico (não o raiz), use:

```vue
<script setup>
defineOptions({ inheritAttrs: false })
</script>

<template>
  <div class="wrapper">
    <v-card v-bind="$attrs">
      <!-- conteúdo -->
    </v-card>
  </div>
</template>
```

`defineOptions({ inheritAttrs: false })` desliga o comportamento automático; `v-bind="$attrs"` aplica manualmente todos os atributos não declarados como props no elemento que você escolher.

> **🔬 Investigue**
> Renderize `<EventoCard :evento="evento" class="destaque" data-testid="card-evento" />` sem declarar `class` nem `data-testid` como props em `EventoCard`. Abra o DevTools, aba **Elements**, e inspecione o `<v-card>` renderizado: a classe `destaque` e o atributo `data-testid` apareceram nele, mesmo sem você ter escrito nada a mais no template do componente — esse é o fallthrough automático. Agora adicione `defineOptions({ inheritAttrs: false })` ao `EventoCard`, sem adicionar `v-bind="$attrs"` em lugar nenhum, e inspecione de novo: para onde os atributos foram?

## 2. Slots: componentes de layout reutilizáveis

Props resolvem "que dados entram". Slots resolvem "que **conteúdo/template** entra" — permitem que um componente pai injete HTML/componentes dentro de um "buraco" definido pelo componente filho.

### Slot padrão

```vue
<!-- src/components/CartaoBase.vue -->
<template>
  <v-card class="pa-4">
    <slot />
  </v-card>
</template>
```

```vue
<CartaoBase>
  <h3>Qualquer conteúdo aqui</h3>
  <p>O CartaoBase não sabe nem precisa saber o que vai dentro.</p>
</CartaoBase>
```

### Slots nomeados

Um componente pode ter vários "buracos" com papéis diferentes:

```vue
<!-- src/components/CartaoBase.vue -->
<template>
  <v-card>
    <v-card-title>
      <slot name="titulo">Sem título</slot>
    </v-card-title>
    <v-card-text>
      <slot />
    </v-card-text>
    <v-card-actions>
      <slot name="acoes" />
    </v-card-actions>
  </v-card>
</template>
```

```vue
<CartaoBase>
  <template #titulo>Semana Acadêmica</template>

  Conteúdo do corpo do card, vai para o slot padrão.

  <template #acoes>
    <v-btn color="primary">Inscrever-se</v-btn>
  </template>
</CartaoBase>
```

`#titulo` é o atalho para `v-slot:titulo`. Um slot sem `name` é chamado de slot **padrão** (`default`), e recebe qualquer conteúdo que não esteja explicitamente marcado com `<template #algumNome>`.

### Slots com escopo (scoped slots)

Às vezes o componente filho tem dados que o pai precisa usar *dentro* do conteúdo injetado. Um slot com escopo passa dados do filho para o template do pai:

```vue
<!-- src/components/EventoLista.vue (trecho) -->
<template>
  <div v-for="evento in eventos" :key="evento.id">
    <slot name="item" :evento="evento" :formatarData="formatarData" />
  </div>
</template>
```

```vue
<EventoLista :eventos="listaEventos">
  <template #item="{ evento, formatarData }">
    <v-card>
      <v-card-title>{{ evento.titulo }}</v-card-title>
      <v-card-subtitle>{{ formatarData(evento.dataHora) }}</v-card-subtitle>
    </v-card>
  </template>
</EventoLista>
```

O componente `EventoLista` controla a iteração (`v-for`) e a lógica auxiliar (`formatarData`), mas delega ao componente pai **como cada item é desenhado**. Isso é poderoso: o mesmo `EventoLista` pode ser reaproveitado em uma tela que mostra cards e em outra que mostra uma tabela — só o slot `#item` muda.

## 3. Composables: extraindo lógica reutilizável

Um **composable** é uma função que usa a Composition API (`ref`, `computed`, `watch`, `onMounted` etc.) para encapsular um pedaço de lógica reativa reutilizável, seguindo a convenção de nome `use*`.

```js
// src/composables/useEventos.js
import { ref, computed, onMounted } from 'vue'
import { eventos as eventosBase } from '../data/eventos'

export function useEventos() {
  const carregando = ref(true)
  const eventos = ref([])
  const categoriaFiltro = ref('Todas')
  const busca = ref('')

  onMounted(() => {
    setTimeout(() => {
      eventos.value = eventosBase
      carregando.value = false
    }, 300)
  })

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

  return {
    carregando,
    eventos,
    categoriaFiltro,
    busca,
    eventosFiltrados,
  }
}
```

Qualquer componente que precise dessa lógica simplesmente chama a função:

```vue
<script setup>
import { useEventos } from '../composables/useEventos'

const { carregando, categoriaFiltro, busca, eventosFiltrados } = useEventos()
</script>
```

Cada chamada de `useEventos()` cria seu **próprio** estado isolado (as variáveis `ref` são criadas de novo a cada chamada) — diferente de uma store Pinia, que é compartilhada globalmente (veremos essa distinção com clareza na Aula 06).

### Por que composables substituem mixins

Antes da Composition API, o Vue 2 usava **mixins** para reutilizar lógica entre componentes: um objeto com `data`, `methods`, `computed` que era "misturado" ao componente. O problema era que, ao usar dois ou mais mixins no mesmo componente, não dava para saber de onde vinha cada propriedade — se `data.carregando` veio do mixin A ou do mixin B era invisível no template, e colisões de nome se sobrescreviam silenciosamente.

Composables resolvem isso porque tudo é **explícito**: você importa a função, chama, e desestrutura exatamente o que quer usar, sob o nome que quiser:

```js
const { eventosFiltrados: eventosDaHome } = useEventos()
```

Não há mágica de mesclagem por trás — é só uma função JavaScript comum retornando um objeto. Essa clareza de origem é a razão pela qual a comunidade Vue abandonou mixins como padrão recomendado.

> **🧠 Você sabia?**
> A Composition API do Vue 3 (2020) foi diretamente influenciada pelos React Hooks, lançados em 2018 — ambos resolvem o mesmo problema (reutilizar lógica com estado sem herança nem mixins) com uma ideia parecida: funções que encapsulam `ref`/`state`, `computed`/`useMemo`, `watch`/`useEffect`. A diferença prática que mais ajuda no dia a dia: hooks do React têm regras rígidas de ordem de chamada (não pode chamar dentro de `if`), enquanto composables do Vue são só funções JavaScript comuns — sem essa restrição, porque a reatividade do Vue não depende da ordem em que os hooks foram chamados na renderização anterior.

## 4. Vue Router avançado

### Rotas aninhadas (`children`)

Uma área administrativa tem uma URL-base (`/admin`) com sub-telas (`/admin/eventos`, `/admin/eventos/novo`). Em vez de repetir `/admin` em cada rota, use `children`:

```js
// src/router/index.js (trecho)
{
  path: '/admin',
  component: () => import('../views/admin/AdminLayoutView.vue'),
  children: [
    { path: '', name: 'admin-home', component: () => import('../views/admin/AdminHomeView.vue') },
    { path: 'eventos', name: 'admin-eventos', component: () => import('../views/admin/AdminEventosView.vue') },
    { path: 'eventos/novo', name: 'admin-evento-novo', component: () => import('../views/admin/AdminEventoFormView.vue') },
    { path: 'eventos/:id/editar', name: 'admin-evento-editar', component: () => import('../views/admin/AdminEventoFormView.vue') },
  ],
}
```

O componente pai da rota (`AdminLayoutView.vue`) precisa ter seu próprio `<RouterView />` — é onde as rotas-filhas serão renderizadas:

```vue
<!-- src/views/admin/AdminLayoutView.vue -->
<template>
  <v-container>
    <v-tabs>
      <v-tab :to="{ name: 'admin-home' }">Painel</v-tab>
      <v-tab :to="{ name: 'admin-eventos' }">Eventos</v-tab>
    </v-tabs>
    <RouterView />
  </v-container>
</template>
```

Esse aninhamento de `RouterView` dentro de `RouterView` é o mesmo padrão **Composite** que vimos na Aula 04 aplicado à navegação: cada nível de rota tem seu próprio "slot" de renderização.

### `meta` em rotas

Cada rota pode carregar metadados arbitrários, usados por guards ou pela própria interface (ex.: título da página, exigência de autenticação):

```js
{
  path: 'eventos/novo',
  name: 'admin-evento-novo',
  component: () => import('../views/admin/AdminEventoFormView.vue'),
  meta: { requerAutenticacao: true, titulo: 'Novo evento' },
}
```

### Navigation guards

Guards são funções que rodam antes (ou depois) de uma navegação, podendo permitir, bloquear ou redirecionar.

**`beforeEach` — guard global**, roda em toda navegação:

```js
// src/router/index.js (trecho, após criar o router)
router.beforeEach((to, from) => {
  document.title = to.meta.titulo
    ? `${to.meta.titulo} · UniEventos`
    : 'UniEventos'

  const autenticado = false // substituiremos por estado real com Pinia na Aula 06
  if (to.meta.requerAutenticacao && !autenticado) {
    return { name: 'home' } // redireciona
  }
  // retornar undefined/true permite a navegação
})
```

**`beforeEnter` — guard por rota**, só roda ao entrar naquela rota específica:

```js
{
  path: 'eventos/:id/editar',
  name: 'admin-evento-editar',
  component: () => import('../views/admin/AdminEventoFormView.vue'),
  beforeEnter: (to) => {
    if (Number.isNaN(Number(to.params.id))) {
      return { name: 'nao-encontrado' }
    }
  },
}
```

**`onBeforeRouteLeave` — guard dentro do componente**, útil para confirmar saída de um formulário com alterações não salvas:

```vue
<script setup>
import { ref } from 'vue'
import { onBeforeRouteLeave } from 'vue-router'

const formularioAlterado = ref(true)

onBeforeRouteLeave(() => {
  if (formularioAlterado.value) {
    const confirmar = window.confirm('Existem alterações não salvas. Sair mesmo assim?')
    if (!confirmar) return false
  }
})
</script>
```

### Query strings sincronizadas com filtros

Uma prática comum e muito útil: refletir o estado dos filtros de busca na URL, para que o usuário possa compartilhar/recarregar a página sem perder o filtro aplicado.

```vue
<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const rota = useRoute()
const router = useRouter()

// inicializa o filtro a partir da query string, se existir
const categoriaFiltro = ref(rota.query.categoria ?? 'Todas')

// sempre que o filtro mudar, atualiza a URL (sem recarregar a página)
watch(categoriaFiltro, (novoValor) => {
  router.push({ query: { ...rota.query, categoria: novoValor } })
})
</script>
```

Com isso, `/eventos?categoria=Minicurso` carrega a tela já filtrada — útil para compartilhar um link de busca específica, e para o botão "voltar" do navegador restaurar o filtro anterior.

### Scroll behavior

Por padrão, ao navegar entre rotas o Vue Router mantém a posição de rolagem atual. Para voltar ao topo em cada navegação (comportamento mais comum em SPAs de conteúdo):

```js
// src/router/index.js (trecho, dentro de createRouter)
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition // navegação por botão voltar/avançar
    return { top: 0 }
  },
  routes: [ /* ... */ ],
})
```

### Layouts diferentes por rota

Nem toda rota deve usar o mesmo `App.vue`. A área administrativa, por exemplo, pode ter um layout próprio (sem o app-bar público). Uma forma simples é usar rotas aninhadas com um componente de layout diferente para cada seção — exatamente a estrutura de `AdminLayoutView.vue` que criamos acima. Cada "família" de rotas aponta para seu próprio layout, e cada layout tem seu próprio `<RouterView />` interno.

## 5. Vuetify aprofundado

### `v-form` com validação por regras

```vue
<script setup>
import { ref } from 'vue'

const formRef = ref(null)
const titulo = ref('')
const vagas = ref(null)

const regrasTitulo = [
  (v) => !!v || 'O título é obrigatório',
  (v) => (v && v.length >= 5) || 'O título precisa ter ao menos 5 caracteres',
]

const regrasVagas = [
  (v) => !!v || 'Informe o número de vagas',
  (v) => (v > 0) || 'O número de vagas deve ser positivo',
]

async function salvar() {
  const { valid } = await formRef.value.validate()
  if (!valid) return
  console.log('Formulário válido — dados prontos para envio:', { titulo: titulo.value, vagas: vagas.value })
}
</script>

<template>
  <v-form ref="formRef" @submit.prevent="salvar">
    <v-text-field v-model="titulo" label="Título do evento" :rules="regrasTitulo" />
    <v-text-field v-model.number="vagas" label="Vagas" type="number" :rules="regrasVagas" />
    <v-btn type="submit" color="primary">Salvar</v-btn>
  </v-form>
</template>
```

Nesta seção o objetivo é validação — o envio real (para uma API ou para uma store) aparece completo no Mão na massa desta aula, e de novo, com Axios, na Aula 06.

`rules` é um array de funções que recebem o valor atual do campo e retornam `true` (válido) ou uma string (mensagem de erro exibida abaixo do campo). Chamar `formRef.value.validate()` executa todas as regras de todos os campos do formulário de uma vez e retorna `{ valid, errors }`.

> **⚠️ Atenção:** no Vuetify 4, se você usa o slot com escopo do `v-form` (`<v-form v-slot="{ isValid }">`) para acessar o estado de validação diretamente no template, essas variáveis de slot **não são mais refs** — não use `.value` nelas dentro do template. Compare:
>
> ```vue
> <!-- Vuetify 3 (antigo) — .value dentro do template -->
> <v-form v-slot="{ isValid }">
>   <v-btn :disabled="!isValid.value">Salvar</v-btn>
> </v-form>
>
> <!-- Vuetify 4 (atual) — SEM .value -->
> <v-form v-slot="{ isValid }">
>   <v-btn :disabled="!isValid">Salvar</v-btn>
> </v-form>
> ```
>
> Se você copiar um exemplo antigo com `.value` dentro do template do `v-form`, o botão nunca habilita — `isValid` deixou de ser um objeto ref e passou a ser o valor puro.

### `v-data-table`

```vue
<script setup>
import { ref } from 'vue'
import { eventos } from '../data/eventos'

const cabecalhos = [
  { title: 'Título', key: 'titulo' },
  { title: 'Categoria', key: 'categoria' },
  { title: 'Data', key: 'dataHora' },
  { title: 'Vagas', key: 'vagas' },
  { title: 'Ações', key: 'acoes', sortable: false },
]

const busca = ref('')
</script>

<template>
  <v-text-field v-model="busca" label="Buscar" prepend-inner-icon="mdi-magnify" class="mb-4" />

  <v-data-table
    :headers="cabecalhos"
    :items="eventos"
    :search="busca"
    items-per-page="5"
  >
    <template #item.acoes="{ item }">
      <v-btn icon="mdi-pencil" size="small" variant="text" />
      <v-btn icon="mdi-delete" size="small" variant="text" color="error" />
    </template>
  </v-data-table>
</template>
```

`v-data-table` já traz ordenação por coluna (clicando no cabeçalho), paginação e busca (via prop `search`, cruzada contra todos os campos dos itens) prontos, sem código adicional. O slot nomeado `#item.acoes` — repare no padrão `item.<chave-da-coluna>` — permite customizar completamente o conteúdo de uma coluna, exatamente com a técnica de slot com escopo que vimos na §2.

### `v-dialog` de confirmação, `v-tabs`, `v-menu`, `v-skeleton-loader`, `v-pagination`

```vue
<!-- diálogo de confirmação reutilizável -->
<v-dialog v-model="dialogoAberto" max-width="400" persistent>
  <v-card title="Confirmar exclusão" text="Esta ação não pode ser desfeita.">
    <v-card-actions>
      <v-spacer />
      <v-btn variant="text" @click="dialogoAberto = false">Cancelar</v-btn>
      <v-btn color="error" variant="flat" @click="confirmarExclusao">Excluir</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>
```

```vue
<!-- abas -->
<v-tabs v-model="abaAtiva">
  <v-tab value="proximos">Próximos</v-tab>
  <v-tab value="encerrados">Encerrados</v-tab>
</v-tabs>
<v-window v-model="abaAtiva">
  <v-window-item value="proximos">...</v-window-item>
  <v-window-item value="encerrados">...</v-window-item>
</v-window>
```

```vue
<!-- menu de contexto -->
<v-menu>
  <template #activator="{ props: propsAtivador }">
    <v-btn icon="mdi-dots-vertical" variant="text" v-bind="propsAtivador" />
  </template>
  <v-list>
    <v-list-item title="Editar" prepend-icon="mdi-pencil" />
    <v-list-item title="Excluir" prepend-icon="mdi-delete" />
  </v-list>
</v-menu>
```

O slot `#activator` do `v-menu` é outro exemplo de slot com escopo: ele entrega `propsAtivador`, um conjunto de listeners/atributos que você precisa espalhar (`v-bind`) no elemento que deve abrir o menu ao ser clicado.

```vue
<!-- esqueleto de carregamento -->
<v-skeleton-loader v-if="carregando" type="card" />
<EventoCard v-else :evento="evento" />
```

`v-skeleton-loader` substitui o `v-progress-circular` genérico quando você quer que o "estado de carregando" já sugira a forma do conteúdo final (cards cinza pulsando no lugar dos cards reais) — uma técnica de percepção de performance bastante usada em produção.

```vue
<!-- paginação manual (fora do v-data-table) -->
<v-pagination v-model="paginaAtual" :length="totalPaginas" />
```

## 🧩 Padrão de projeto em uso — Composite e Template Method

**Composite** aparece de novo hoje, agora na composição de componentes de layout: `CartaoBase` não sabe o que vai dentro dele — apenas define a "moldura" (`v-card` com título, corpo e ações), e quem usa o componente decide o conteúdo via slots. Isso é o mesmo princípio da árvore de componentes da Aula 04, aplicado deliberadamente ao design de um componente reutilizável.

**Template Method** é um padrão comportamental em que uma classe (ou, aqui, um componente) define o **esqueleto** de um algoritmo ou de uma estrutura, deixando etapas específicas para serem preenchidas por quem o usa. Um slot com escopo — como o `#item` de `EventoLista` — é exatamente isso: o componente controla o "algoritmo" (iterar sobre a lista, aplicar filtro), mas delega ao chamador a etapa de "como desenhar cada item". A estrutura geral é fixa; o passo variável é injetado de fora.

## 💻 Mão na massa — refatorando o UniEventos em componentes

### Passo 1 — criar `EventoCard.vue`

```vue
<!-- src/components/EventoCard.vue -->
<script setup>
const props = defineProps({
  evento: { type: Object, required: true },
})

const emit = defineEmits({
  inscrever: (idEvento) => typeof idEvento === 'number',
})

function formatarData(dataIso) {
  return new Date(dataIso).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  })
}
</script>

<template>
  <v-card :to="{ name: 'evento-detalhe', params: { id: evento.id } }">
    <v-img :src="evento.imagemUrl" height="160" cover />
    <v-card-title>{{ evento.titulo }}</v-card-title>
    <v-card-subtitle>
      {{ formatarData(evento.dataHora) }} · {{ evento.local }}
    </v-card-subtitle>
    <v-card-actions>
      <v-chip color="secondary" size="small">{{ evento.categoria }}</v-chip>
      <v-spacer />
      <v-chip :color="evento.vagas > 0 ? 'success' : 'error'" size="small">
        {{ evento.vagas > 0 ? `${evento.vagas} vagas` : 'Esgotado' }}
      </v-chip>
    </v-card-actions>
  </v-card>
</template>
```

### Passo 2 — criar `EventoLista.vue`

> **⚠️ Atenção**
> O `vite-plugin-vuetify` faz auto-import **só dos componentes do Vuetify** (`v-card`, `v-row`…). Os seus componentes, mesmo no mesmo diretório, **não** são registrados automaticamente pelo `create-vue`: usar `<EventoCard />` sem importar produz o aviso `Failed to resolve component: EventoCard` no console e um espaço em branco na tela. Todo componente autoral que você usar em um `<template>` precisa de um `import` no `<script setup>` do arquivo que o usa.

```vue
<!-- src/components/EventoLista.vue -->
<script setup>
import EventoCard from './EventoCard.vue'

defineProps({
  eventos: { type: Array, required: true },
})
</script>

<template>
  <v-row>
    <v-col
      v-for="evento in eventos"
      :key="evento.id"
      cols="12"
      sm="6"
      md="4"
    >
      <EventoCard :evento="evento" />
    </v-col>
  </v-row>
</template>
```

### Passo 3 — criar `FiltroEventos.vue` com `v-model` duplo

```vue
<!-- src/components/FiltroEventos.vue -->
<script setup>
const busca = defineModel('busca', { type: String, default: '' })
const categoria = defineModel('categoria', { type: String, default: 'Todas' })

const categorias = ['Todas', 'Palestra', 'Minicurso', 'Workshop']
</script>

<template>
  <v-row class="mb-2">
    <v-col cols="12" md="6">
      <v-text-field
        v-model="busca"
        label="Buscar evento"
        prepend-inner-icon="mdi-magnify"
        variant="outlined"
        density="compact"
        clearable
      />
    </v-col>
    <v-col cols="12" md="6">
      <v-select
        v-model="categoria"
        :items="categorias"
        label="Categoria"
        variant="outlined"
        density="compact"
      />
    </v-col>
  </v-row>
</template>
```

`defineModel('busca', ...)` e `defineModel('categoria', ...)` são a forma de `defineModel()` para **múltiplos** `v-model`s no mesmo componente — cada nome vira um par prop/evento independente:

```vue
<FiltroEventos v-model:busca="busca" v-model:categoria="categoriaFiltro" />
```

### Passo 4 — criar `CabecalhoApp.vue` e `RodapeApp.vue`

```vue
<!-- src/components/CabecalhoApp.vue -->
<script setup>
import { computed } from 'vue'
import { useTheme } from 'vuetify'
import { RouterLink } from 'vue-router'

defineProps({
  totalEventos: { type: Number, default: 0 },
})

const emit = defineEmits(['abrir-menu'])

const tema = useTheme()
const ehEscuro = computed(() => tema.global.name.value === 'dark')

function alternarTema() {
  tema.global.name.value = ehEscuro.value ? 'light' : 'dark'
}
</script>

<template>
  <v-app-bar color="primary">
    <v-app-bar-nav-icon @click="emit('abrir-menu')" />
    <v-app-bar-title>
      <RouterLink to="/" class="text-white text-decoration-none">UniEventos</RouterLink>
    </v-app-bar-title>
    <v-chip color="secondary" size="small" class="mr-2">{{ totalEventos }} eventos</v-chip>
    <v-spacer />
    <v-btn
      :icon="ehEscuro ? 'mdi-weather-sunny' : 'mdi-weather-night'"
      variant="text"
      @click="alternarTema"
    />
  </v-app-bar>
</template>
```

```vue
<!-- src/components/RodapeApp.vue -->
<script setup>
</script>

<template>
  <v-footer color="primary" class="d-flex justify-center pa-4">
    <span class="text-white">UNEMAT · FACET · FACET-SNP-310</span>
  </v-footer>
</template>
```

### Passo 5 — criar `DialogoConfirmacao.vue`

```vue
<!-- src/components/DialogoConfirmacao.vue -->
<script setup>
const aberto = defineModel({ type: Boolean, default: false })

defineProps({
  titulo: { type: String, default: 'Confirmar ação' },
  mensagem: { type: String, default: 'Esta ação não pode ser desfeita.' },
})

const emit = defineEmits(['confirmar'])

function confirmar() {
  emit('confirmar')
  aberto.value = false
}
</script>

<template>
  <v-dialog v-model="aberto" max-width="400" persistent>
    <v-card :title="titulo" :text="mensagem">
      <v-card-actions>
        <v-spacer />
        <v-btn variant="text" @click="aberto = false">Cancelar</v-btn>
        <v-btn color="error" variant="flat" @click="confirmar">Confirmar</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
```

### Passo 6 — atualizar `App.vue` para usar `CabecalhoApp` e `RodapeApp`

```vue
<!-- src/App.vue -->
<script setup>
import { ref, computed } from 'vue'
import { RouterView } from 'vue-router'
import CabecalhoApp from './components/CabecalhoApp.vue'
import RodapeApp from './components/RodapeApp.vue'
import { eventos } from './data/eventos'

const drawerAberto = ref(false)
const totalEventos = computed(() => eventos.length)

const linksMenu = [
  { titulo: 'Início', rota: 'home', icone: 'mdi-home' },
  { titulo: 'Sobre', rota: 'sobre', icone: 'mdi-information' },
  { titulo: 'Administração', rota: 'admin-home', icone: 'mdi-cog' },
]
</script>

<template>
  <v-app>
    <CabecalhoApp :total-eventos="totalEventos" @abrir-menu="drawerAberto = !drawerAberto" />

    <v-navigation-drawer v-model="drawerAberto" temporary>
      <v-list>
        <v-list-item
          v-for="link in linksMenu"
          :key="link.rota"
          :to="{ name: link.rota }"
          :title="link.titulo"
          :prepend-icon="link.icone"
        />
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <RouterView />
    </v-main>

    <RodapeApp />
  </v-app>
</template>
```

### Passo 7 — reescrever `HomeView.vue` usando os componentes e o composable

```vue
<!-- src/views/HomeView.vue -->
<script setup>
import { useEventos } from '../composables/useEventos'
import FiltroEventos from '../components/FiltroEventos.vue'
import EventoLista from '../components/EventoLista.vue'

const { carregando, categoriaFiltro, busca, eventosFiltrados } = useEventos()
</script>

<template>
  <v-container>
    <h1 class="text-h4 mb-4">Eventos disponíveis</h1>

    <FiltroEventos v-model:busca="busca" v-model:categoria="categoriaFiltro" />

    <div v-if="carregando" class="d-flex justify-center pa-8">
      <v-skeleton-loader type="card" v-for="n in 3" :key="n" class="mb-4" />
    </div>

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

Compare este arquivo com o `HomeView.vue` da Aula 04: a lógica de busca/filtro/carregamento saiu para o composable `useEventos`, o grid de cards virou `EventoLista`, e os campos de filtro viraram `FiltroEventos`. A view agora só orquestra — é um bom exemplo de componente "inteligente" fino, delegando apresentação aos filhos.

### Passo 8 — tornar `src/data/eventos.js` reativo

A área administrativa que começa aqui **altera** a lista de eventos: exclui, cria e edita. O arquivo criado na Aula 04 exporta um array JavaScript comum — e o Vue não observa arrays comuns. Se a área administrativa mexer nele como está, o dado até muda na memória, mas a `v-data-table`, o contador do `AdminHomeView` e o chip do `v-app-bar` continuam mostrando o valor antigo: o CRUD "não funciona" sem nenhum erro no console. Envolva o array em `reactive()` antes de seguir:

```js
// src/data/eventos.js — agora reativo
import { reactive } from 'vue'

export const eventos = reactive([
  { id: 1, titulo: 'Semana Acadêmica de Computação', descricao: 'Palestras e minicursos sobre tendências em tecnologia.', categoria: 'palestra', dataHora: '2030-09-29T19:00:00', local: 'Auditório Central', vagas: 40, imagemUrl: 'https://picsum.photos/seed/evento1/600/300' },
  // … os outros sete eventos, sem alteração
])
```

> **⚠️ Atenção**
> Continue mutando o array **no lugar** (`push`, `splice`, `Object.assign`), nunca reatribuindo (`eventos = [...]`) — `reactive()` protege o conteúdo, não a variável, e a reatribuição quebraria a ligação com todas as telas de uma vez (é exatamente o bug do item A4 da Aula 02). Este arquivo é uma "store caseira": funciona bem para uma maquete, e na Aula 06 ele dá lugar a uma store Pinia de verdade.

### Passo 9 — criar rotas administrativas aninhadas

```js
// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    return { top: 0 }
  },
  routes: [
    { path: '/', name: 'home', component: () => import('../views/HomeView.vue') },
    { path: '/eventos/:id', name: 'evento-detalhe', component: () => import('../views/EventoDetalheView.vue') },
    { path: '/sobre', name: 'sobre', component: () => import('../views/SobreView.vue'), meta: { titulo: 'Sobre' } },
    {
      path: '/admin',
      component: () => import('../views/admin/AdminLayoutView.vue'),
      children: [
        { path: '', name: 'admin-home', component: () => import('../views/admin/AdminHomeView.vue'), meta: { titulo: 'Painel administrativo' } },
        { path: 'eventos', name: 'admin-eventos', component: () => import('../views/admin/AdminEventosView.vue'), meta: { titulo: 'Gerenciar eventos' } },
        { path: 'eventos/novo', name: 'admin-evento-novo', component: () => import('../views/admin/AdminEventoFormView.vue'), meta: { titulo: 'Novo evento' } },
        {
          path: 'eventos/:id/editar',
          name: 'admin-evento-editar',
          component: () => import('../views/admin/AdminEventoFormView.vue'),
          meta: { titulo: 'Editar evento' },
          beforeEnter: (to) => {
            if (Number.isNaN(Number(to.params.id))) {
              return { name: 'nao-encontrado' }
            }
          },
        },
      ],
    },
    { path: '/:pathMatch(.*)*', name: 'nao-encontrado', component: () => import('../views/NaoEncontradoView.vue') },
  ],
})

router.beforeEach((to) => {
  document.title = to.meta.titulo ? `${to.meta.titulo} · UniEventos` : 'UniEventos'
})

export default router
```

### Passo 10 — criar `AdminLayoutView.vue`

```vue
<!-- src/views/admin/AdminLayoutView.vue -->
<script setup>
import { ref } from 'vue'
import { RouterView } from 'vue-router'

const abaAtiva = ref('admin-eventos')
</script>

<template>
  <v-container>
    <h1 class="text-h4 mb-4">Administração</h1>
    <v-tabs v-model="abaAtiva" class="mb-4">
      <v-tab value="admin-home" :to="{ name: 'admin-home' }">Painel</v-tab>
      <v-tab value="admin-eventos" :to="{ name: 'admin-eventos' }">Eventos</v-tab>
    </v-tabs>
    <RouterView />
  </v-container>
</template>
```

### Passo 11 — criar `AdminHomeView.vue` e `AdminEventosView.vue`

```vue
<!-- src/views/admin/AdminHomeView.vue -->
<script setup>
import { eventos } from '../../data/eventos'
</script>

<template>
  <v-row>
    <v-col cols="12" sm="4">
      <v-card class="pa-4 text-center">
        <div class="text-h3 text-primary">{{ eventos.length }}</div>
        <div>eventos cadastrados</div>
      </v-card>
    </v-col>
  </v-row>
</template>
```

```vue
<!-- src/views/admin/AdminEventosView.vue -->
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { eventos } from '../../data/eventos'
import DialogoConfirmacao from '../../components/DialogoConfirmacao.vue'

const router = useRouter()
const dialogoAberto = ref(false)
const eventoParaExcluir = ref(null)

const cabecalhos = [
  { title: 'Título', key: 'titulo' },
  { title: 'Categoria', key: 'categoria' },
  { title: 'Vagas', key: 'vagas' },
  { title: 'Ações', key: 'acoes', sortable: false },
]

const busca = ref('')

function pedirExclusao(evento) {
  eventoParaExcluir.value = evento
  dialogoAberto.value = true
}

function confirmarExclusao() {
  const indice = eventos.findIndex((e) => e.id === eventoParaExcluir.value.id)
  if (indice !== -1) eventos.splice(indice, 1)
  eventoParaExcluir.value = null
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

    <v-data-table :headers="cabecalhos" :items="eventos" :search="busca" items-per-page="5">
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
  </div>
</template>
```

### Passo 12 — criar `AdminEventoFormView.vue` com validação

```vue
<!-- src/views/admin/AdminEventoFormView.vue -->
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter, onBeforeRouteLeave } from 'vue-router'
import { eventos } from '../../data/eventos'

const rota = useRoute()
const router = useRouter()

const modoEdicao = computed(() => rota.name === 'admin-evento-editar')
const formRef = ref(null)
const formularioAlterado = ref(false)

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
    const evento = eventos.find((e) => e.id === Number(rota.params.id))
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

  if (modoEdicao.value) {
    const evento = eventos.find((e) => e.id === Number(rota.params.id))
    Object.assign(evento, {
      titulo: titulo.value,
      descricao: descricao.value,
      categoria: categoria.value,
      local: local.value,
      vagas: vagas.value,
    })
  } else {
    const novoId = Math.max(...eventos.map((e) => e.id)) + 1
    eventos.push({
      id: novoId,
      titulo: titulo.value,
      descricao: descricao.value,
      categoria: categoria.value,
      local: local.value,
      vagas: vagas.value,
      dataHora: new Date().toISOString(),
      imagemUrl: `https://picsum.photos/seed/evento${novoId}/600/300`,
    })
  }

  formularioAlterado.value = false
  router.push({ name: 'admin-eventos' })
}
</script>

<template>
  <v-card class="pa-4">
    <v-card-title>{{ modoEdicao ? 'Editar evento' : 'Novo evento' }}</v-card-title>
    <v-card-text>
      <v-form ref="formRef" @submit.prevent="salvar" @update:model-value="formularioAlterado = true">
        <v-text-field v-model="titulo" label="Título" :rules="regrasTitulo" class="mb-2" />
        <v-textarea v-model="descricao" label="Descrição" rows="3" class="mb-2" />
        <v-select v-model="categoria" :items="categorias" label="Categoria" class="mb-2" />
        <v-text-field v-model="local" label="Local" :rules="regrasLocal" class="mb-2" />
        <v-text-field v-model.number="vagas" label="Vagas" type="number" :rules="regrasVagas" class="mb-4" />
        <v-btn type="submit" color="primary" variant="flat">Salvar</v-btn>
        <v-btn variant="text" class="ml-2" :to="{ name: 'admin-eventos' }">Cancelar</v-btn>
      </v-form>
    </v-card-text>
  </v-card>
</template>
```

### Como testar

Com `npm run dev` rodando, percorra os dois lados da aplicação:

1. **Público** — a `HomeView` mostra os oito cards vindos de `EventoLista`/`EventoCard`; digitar no `FiltroEventos` reduz a lista e a query string da URL acompanha (`?busca=vue`); recarregar a página com a query string preservada devolve a mesma lista filtrada.
2. **Administrativo** — acesse `/admin`: a `v-data-table` lista os mesmos oito eventos. Clique em "Novo evento", salve um evento válido e confira que ele **aparece na tabela imediatamente**, que o contador do `AdminHomeView` sobe de 8 para 9 e que o evento novo também aparece na Home pública.
3. **Exclusão** — exclua esse evento pelo diálogo de confirmação: a linha some da tabela na hora e o contador volta a 8.
4. **Guard de saída** — comece a editar um evento, altere um campo e clique em "Cancelar": o `onBeforeRouteLeave` pergunta se você quer mesmo sair.

Resultado esperado: os quatro itens acima passam sem recarregar a página. Se a tabela e o contador **não** mudarem depois de criar ou excluir, o `reactive()` do Passo 8 não foi aplicado — é o sintoma exato descrito lá.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Preveja a saída no console: `EventoCard` declara `defineProps({ evento: { type: Object, required: true } })`, e o componente pai usa `<EventoCard />` sem passar a prop `evento`.

Resultado esperado: um aviso no console (`[Vue warn]: Missing required prop: "evento"`), e o template do componente provavelmente quebra ao tentar ler `evento.titulo` de `undefined` — props `required` não impedem a renderização, só avisam.

**A2.** Complete a linha que falta para que o evento `favoritar` só seja aceito se o payload for um número:

```js
const emit = defineEmits({
  favoritar: ____,
})
```

Resultado esperado: `(idEvento) => typeof idEvento === 'number'` — uma função validadora que recebe o payload do evento e retorna `true`/`false`, no mesmo espírito do `validator` de `defineProps`.

**A3.** Em uma frase: por que `useEventos()` chamado duas vezes, em dois componentes diferentes, resulta em dois estados de carregamento independentes — enquanto uma store Pinia, chamada duas vezes, resulta num único estado compartilhado?

Resultado esperado: porque um composable é só uma função JavaScript comum — cada chamada executa o corpo de novo e cria `ref`s novos; uma store Pinia é um singleton gerenciado pelo framework, então toda chamada de `useXStore()` devolve a mesma instância.

**A4.** Ache o erro nas linhas abaixo — a rota `admin-eventos` nunca renderiza nada quando o usuário acessa `/admin` diretamente (só a URL-base, sem sub-caminho):

```js
{
  path: '/admin',
  component: AdminLayoutView,
  children: [
    { path: 'home', name: 'admin-home', component: AdminHomeView },
    { path: 'eventos', name: 'admin-eventos', component: AdminEventosView },
  ],
}
```

Resultado esperado: falta uma rota-filha com `path: ''` (caminho vazio) para cobrir exatamente `/admin` sem sub-caminho nenhum — hoje `/admin` sozinho não bate com nenhuma rota-filha declarada, porque todas exigem um segmento extra (`/admin/home`, `/admin/eventos`).

**A5.** Preveja o comportamento: o `scrollBehavior` do router **não** foi declarado (a opção inteira foi omitida de `createRouter`). O usuário rola a página até o rodapé e clica em um `<RouterLink>` para outra rota.

Resultado esperado: a nova página aparece já rolada — o Vue Router preserva a posição de scroll atual por padrão quando `scrollBehavior` não está definido; é preciso declará-lo explicitamente (retornando `{ top: 0 }`) para voltar ao topo a cada navegação.

### Nível B — Aplicação

**B1.** `CartaoBase` com slots nomeados. Crie o componente `src/components/CartaoBase.vue` com slots `titulo`, padrão e `acoes` (como na §2), e use-o para reescrever a tela `SobreView.vue`.

Resultado esperado: `SobreView.vue` usa `<CartaoBase>` com `<template #titulo>` e `<template #acoes>`, e a tela renderiza visualmente igual (ou melhor) do que antes.

<details markdown="1">
<summary>Dica</summary>

`<template #titulo>`, conteúdo solto (sem `<template>`) cai no slot padrão, `<template #acoes>`.
</details>

**B2.** Composable `useAlternanciaTema`. Extraia a lógica de `alternarTema`/`ehEscuro` do `CabecalhoApp.vue` para um composable `src/composables/useAlternanciaTema.js`, e use-o também em uma nova tela de configurações.

Resultado esperado: `CabecalhoApp.vue` e a nova tela de configurações chamam `useAlternanciaTema()` e o clique em qualquer um dos dois lugares alterna o tema da aplicação inteira (porque `useTheme()` internamente já é global — o composable só organiza o acesso a ele).

<details markdown="1">
<summary>Dica</summary>

O composable recebe `useTheme()` internamente e retorna `{ ehEscuro, alternarTema }`.
</details>

**B3.** Guard de confirmação no formulário de novo evento. No `AdminEventoFormView.vue`, o `onBeforeRouteLeave` já existe, mas `formularioAlterado` nunca vira `true` ao digitar em campos que não passam por `@update:model-value` do form (ex.: se o navegador não disparar esse evento para todo campo). Ajuste para marcar `formularioAlterado.value = true` de forma confiável usando `watch` sobre os campos do formulário.

Resultado esperado: alterar qualquer campo do formulário e tentar sair da rota (clicar em "Cancelar" ou em um link do menu) dispara o `window.confirm`; salvar o formulário com sucesso não dispara mais o aviso ao sair em seguida.

<details markdown="1">
<summary>Dica</summary>

`watch([titulo, descricao, categoria, local, vagas], () => { formularioAlterado.value = true })`.
</details>

**B4.** `v-menu` de ações rápidas no `EventoCard`. Adicione um `v-menu` com um botão de três pontinhos no `EventoCard`, com opções "Compartilhar" e "Favoritar", que emitem eventos `compartilhar` e `favoritar` para o componente pai.

Resultado esperado: clicar no botão de três pontinhos abre um menu com as duas opções; clicar em cada uma emite o evento correspondente, capturável com `@compartilhar`/`@favoritar` em quem usa o `EventoCard`.

<details markdown="1">
<summary>Dica</summary>

Use o slot `#activator="{ props }"` do `v-menu`, como no exemplo da §5.
</details>

### Nível C — Desafio em sala

**C1.** Query string de paginação. Adicione um `v-pagination` na `AdminEventosView.vue` (fora do `v-data-table`, como exercício) e sincronize a página atual com `?pagina=N` na URL, seguindo o padrão da §4. A URL precisa ser a fonte da verdade: recarregar a página em `/admin/eventos?pagina=3` deve abrir já na página 3, e voltar/avançar no navegador entre páginas visitadas deve funcionar sem recarregar a tela.

Resultado esperado: `/admin/eventos?pagina=2` abre direto na página 2 do `v-pagination`; clicar em outra página atualiza a URL sem recarregar; o botão "voltar" do navegador retorna à página anterior corretamente.

<details markdown="1">
<summary>Dica</summary>

`ref(Number(rota.query.pagina) || 1)` inicializa o estado a partir da URL; um `watch` sobre esse `ref` chama `router.push({ query: { ...rota.query, pagina } })` para refletir de volta; e um `watch` sobre `rota.query.pagina` (o caminho inverso) é o que faz o botão "voltar" do navegador também atualizar o `v-pagination` — sem ele, só a URL muda ao clicar em "voltar", não a tela.
</details>

## 🏆 Desafios

### ⭐ O emit que ninguém escuta

Tags: vue, bug, investigacao

Um colega criou `DialogoConfirmacao.vue` reaproveitando o desta aula, mas trocou um detalhe sem perceber. Ao clicar em "Excluir" no diálogo, nada acontece — o evento aparentemente nunca chega ao componente pai. Este é o trecho relevante:

```vue
<!-- src/components/DialogoConfirmacao.vue — trecho com o bug plantado -->
<script setup>
const emit = defineEmits(['confirmar'])

function confirmar() {
  emit('confirmado')
}
</script>
```

Abra o Vue DevTools (aba **Components**), selecione o `DialogoConfirmacao` e observe a lista de eventos emitidos ao clicar em "Excluir". O nome que aparece bate com o que o componente pai está escutando?

**Critérios de pronto**

- Um comentário no topo do arquivo registra qual nome de evento o `defineEmits` declarava, qual nome estava realmente sendo emitido, e qual dos dois estava errado.
- Clicar em "Excluir" agora dispara a função `confirmarExclusao` (ou equivalente) no componente pai, de forma confirmável no Vue DevTools ou com um `console.log` temporário.
- Uma frase explica por que `defineEmits` **não** impede emitir um evento com nome diferente do declarado — e por que isso torna esse tipo de bug silencioso (sem erro, sem aviso).

<details markdown="1">
<summary>Pistas</summary>

1. `defineEmits(['confirmar'])` só documenta e valida payloads — ele não bloqueia `emit('outroNome')`, mesmo que `'outroNome'` não esteja na lista.
2. No Vue DevTools, a aba **Components** tem uma seção "Events" no painel de detalhes do componente selecionado — ela mostra o nome exato de cada evento emitido, em tempo real.
3. Compare, char por char, o nome usado em `@confirmar="..."` no componente pai com o nome usado em `emit(...)` no filho.
</details>

### ⭐⭐ Menu de contexto sem mouse

Tags: acessibilidade, vuetify, vue

O `v-menu` de ações rápidas do Laboratório B4 funciona perfeitamente no mouse. Agora teste só com teclado: `Tab` até o botão de três pontinhos, `Enter` para abrir, `Tab`/setas para navegar pelas opções, `Enter` para escolher, `Esc` para fechar sem escolher nada. Em qual desses passos a experiência quebra?

**Critérios de pronto**

- O botão de três pontinhos recebe foco visível com `Tab` e tem um `aria-label` descritivo (ex.: "Mais ações para o evento X" — o nome do evento entra dinamicamente no rótulo).
- Abrir o menu com `Enter` (não só com clique) funciona, e o foco move para dentro do menu.
- `Esc` fecha o menu e devolve o foco ao botão de três pontinhos — sem deixar o foco "perdido" em um elemento que sumiu da tela.
- Um vídeo curto (ou GIF) de 10-15 segundos, gravado sem tocar no mouse, mostra o fluxo completo funcionando, anexado ao README do projeto autoral.

<details markdown="1">
<summary>Pistas</summary>

1. `v-btn` aceita `aria-label` como qualquer atributo HTML — inclua o título do evento na string, usando template literal.
2. Verifique a documentação de acessibilidade do `v-menu` na versão do Vuetify instalada — componentes de menu geralmente já implementam boa parte da navegação por teclado, mas o `aria-label` do ativador é responsabilidade sua.
3. Para gravar sem mouse, o gravador de tela nativo do sistema operacional (ou a gravação de tela do próprio DevTools) já basta — não precisa de ferramenta especial.
</details>

### ⭐⭐⭐ Prop drilling até o neto

Tags: vue, refatoracao, padroes-de-projeto

O código abaixo passa o usuário logado por três componentes até chegar a quem realmente precisa dele — clássico **prop drilling**. `PainelAdmin` e `CabecalhoSecao` não usam `usuarioLogado` para nada além de repassar adiante:

```vue
<!-- App.vue: <PainelAdmin :usuario-logado="usuarioLogado" /> -->

<!-- PainelAdmin.vue -->
<script setup>
defineProps({ usuarioLogado: { type: Object, required: true } })
</script>
<template>
  <CabecalhoSecao :usuario-logado="usuarioLogado" />
</template>

<!-- CabecalhoSecao.vue -->
<script setup>
defineProps({ usuarioLogado: { type: Object, required: true } })
</script>
<template>
  <PainelPerfil :usuario-logado="usuarioLogado" />
</template>
```

Refatore essa cadeia usando `provide`/`inject` (§1), e depois responda: o que muda se `PainelPerfil` for renderizado em um lugar da árvore onde ninguém chamou `provide('usuarioLogado', ...)` acima dele?

**Critérios de pronto**

- `PainelAdmin` e `CabecalhoSecao` não recebem mais `usuarioLogado` como prop — o dado só é declarado uma vez, no ancestral comum, com `provide`.
- `PainelPerfil` continua funcionando exatamente igual, agora usando `inject('usuarioLogado')`.
- Um teste deliberado: renderize `PainelPerfil` em uma tela isolada, sem nenhum ancestral chamando `provide`. `inject` recebe um segundo argumento de valor padrão que evita a aplicação quebrar nesse caso — implemente e documente esse valor padrão.
- Um parágrafo no README compara as duas abordagens: em quantos arquivos você precisou tocar para adicionar um novo dado "ambiental" (ex.: idioma da interface) em cada uma, e qual delas você escolheria para o seu projeto autoral, e por quê.

<details markdown="1">
<summary>Pistas</summary>

1. `provide('usuarioLogado', usuarioLogado)` no componente ancestral mais alto que faz sentido (geralmente `App.vue`); `inject('usuarioLogado', valorPadrao)` em qualquer descendente, não importa a profundidade.
2. O segundo argumento de `inject` é o valor usado quando nenhum ancestral fez `provide` daquela chave — útil para não quebrar em testes isolados ou em Storybook.
3. Prop drilling não é "sempre errado" — em cadeias curtas (um ou dois níveis), a prop explícita ainda é mais fácil de rastrear do que `provide`/`inject`. O parágrafo do README deve refletir esse trade-off, não só repetir "provide/inject é melhor".
</details>

## 🐛 Erros comuns e como resolver

| Sintoma | Causa | Solução |
|---|---|---|
| `v-model` em componente customizado não atualiza nada | Componente não implementa `defineModel()` nem o par `modelValue`/`update:modelValue` | Adicione `defineModel()` (ou a forma clássica) no componente filho |
| Prop chega como `undefined` mesmo passando valor no pai | Nome da prop em `kebab-case` no template não bate com o nome em `camelCase` no `defineProps` | Vue converte automaticamente `total-eventos` ↔ `totalEventos` — confira grafia exata dos dois lados |
| `formRef.value.validate()` lança erro "Cannot read properties of null" | O `ref="formRef"` não está associado a um `<v-form>` ainda montado (chamado antes do `onMounted`) | Garanta que a chamada acontece após o componente montar, tipicamente dentro de um handler de clique |
| No `v-slot="{ isValid }"` do `v-form`, `isValid.value` é `undefined` | Código copiado do Vuetify 3 — variáveis de slot não são mais refs no Vuetify 4 | Use `isValid` diretamente, sem `.value` |
| `RouterView` da rota aninhada nunca renderiza | Falta um `<RouterView />` dentro do componente de layout (`AdminLayoutView.vue`) | Toda rota com `children` precisa de um `RouterView` próprio no componente pai da rota |
| `onBeforeRouteLeave` não é chamado | Guard declarado fora de um componente renderizado pela rota (ex.: em um componente filho que não é o componente-alvo da rota) | `onBeforeRouteLeave` só funciona dentro do componente que a rota renderiza diretamente |
| Slot com escopo não recebe os dados esperados | Faltou vincular os dados no `<slot>` do componente filho (`:evento="evento"`) | Toda variável que o slot precisa expor deve ser passada como atributo do `<slot>` |

## 🏠 Atividade assíncrona (1 h)

No seu **projeto autoral**:

1. Extraia pelo menos um componente reutilizável de apresentação (equivalente ao `EventoCard`), com `defineProps` tipado e ao menos um evento emitido.
2. Crie um componente com slot nomeado (equivalente ao `CartaoBase`) e use-o em pelo menos duas telas diferentes.
3. Extraia a lógica de carregamento/filtro de dados para um composable `use*`.
4. Adicione uma área com rotas aninhadas (ex.: painel administrativo do seu domínio) com pelo menos duas rotas-filhas.
5. Crie um formulário de cadastro/edição com `v-form` e `rules` para pelo menos dois campos.

**Critério de pronto:** o formulário não deixa salvar com campos inválidos; a navegação entre rotas aninhadas funciona sem recarregar a página; pelo menos um componente usa slot nomeado com sucesso. Suba o commit no repositório.

## ✅ Checkpoint do projeto autoral

- [ ] Pelo menos 3 componentes de apresentação extraídos, com `defineProps` tipado.
- [ ] Pelo menos um componente usando `v-model` customizado (`defineModel()` ou forma clássica).
- [ ] Pelo menos um componente com slot nomeado ou com escopo.
- [ ] Um composable `use*` extraindo lógica de dados/filtro.
- [ ] Rotas aninhadas funcionando em pelo menos uma seção da aplicação.
- [ ] Formulário com `v-form` e `rules` de validação.
- [ ] `v-data-table` (ou lista equivalente) listando os dados do domínio com busca.

## 📚 Para aprofundar

- Vue.js — Componentes: Props: <https://vuejs.org/guide/components/props.html>
- Vue.js — `defineModel()`: <https://vuejs.org/guide/components/v-model.html>
- Vue.js — Slots: <https://vuejs.org/guide/components/slots.html>
- Vue.js — Composables: <https://vuejs.org/guide/reusability/composables.html>
- Vue Router — Rotas aninhadas: <https://router.vuejs.org/guide/essentials/nested-routes.html>
- Vue Router — Guards de navegação: <https://router.vuejs.org/guide/advanced/navigation-guards.html>
- Vuetify — `v-form` e validação: <https://vuetifyjs.com/en/components/forms/>
- Vuetify — `v-data-table`: <https://vuetifyjs.com/en/components/data-tables/basics/>
- Referências básicas do plano de curso: capítulos sobre reuso de componentes e roteamento avançado.

Na Aula 06 o UniEventos passa a consumir dados de uma API de verdade com **Axios**, organizados em uma camada de serviços — e o estado de eventos e inscrições migra para **Pinia**, substituindo os `ref`s locais que temos usado até aqui.
