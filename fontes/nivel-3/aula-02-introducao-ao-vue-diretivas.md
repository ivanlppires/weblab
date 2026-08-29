# Aula 02 — Introdução ao Vue: instância, ciclo de vida e diretivas

> **Nível 3 — Frameworks Modernos** · Unidade 1: Fundamentos de front-end com Vue.js
> WebLab · UNEMAT Sinop · Prof. Ivan Luiz Pedroso Pires

Na Aula 01 revisamos JavaScript moderno e comparamos DOM manual com o estilo declarativo. Hoje esse estilo declarativo ganha nome: **Vue 3**.

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Explicar o que é o Vue 3, o que significa "framework progressivo" e a diferença entre Options API e Composition API.
- Criar uma instância Vue via CDN com `createApp` e entender o ciclo montar/renderizar.
- Criar um projeto Vue com Vite usando `npm create vue@latest` e explicar cada arquivo gerado.
- Distinguir `ref()` de `reactive()` e explicar por que `.value` existe.
- Usar as diretivas `v-bind`, `v-on`, `v-model`, `v-if`/`v-else-if`/`v-else`, `v-show`, `v-for` (com `:key`) e `v-text`/`v-html` corretamente, cada uma com seus casos de uso e armadilhas.
- Descrever as fases do ciclo de vida de um componente e usar os hooks `onMounted` e `onUnmounted`.
- Construir a primeira versão navegável do UniEventos: lista, busca, filtro e inscrição.

## 📋 Pré-requisitos desta aula

- Ambiente instalado na Aula 01: Node 22 LTS, VS Code com Vue - Official/ESLint/Prettier, Git.
- Conforto com `let`/`const`, arrow functions, desestruturação, `map`/`filter`, `import`/`export` (Aula 01, Seção 3).
- Repositório do projeto autoral criado com `README.md`.

> **⚠️ Atenção**
> Verifique agora, antes de começar: `node -v` precisa mostrar uma versão `22.18.0` ou superior (ou `24.12.0`+). O `create-vue` desta aula exige isso.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | O que é Vue, Options API vs Composition API, primeiro contato via CDN |
| 2 | 50 min | Projeto Vite real, reatividade (`ref`/`reactive`), diretivas de vinculação e eventos |
| 3 | 50 min | Diretivas condicionais/lista, ciclo de vida, mão na massa no UniEventos |

## 1. O que é o Vue 3

Vue é um **framework progressivo** para construir interfaces de usuário. "Progressivo" significa que você pode adotá-lo aos poucos: usar só para uma parte reativa de uma página HTML existente (como faremos daqui a pouco, via CDN) ou para uma aplicação inteira, com build, roteamento e gerenciamento de estado (como faremos a partir de hoje mesmo, com Vite).

O ecossistema Vue que usaremos no semestre:

| Peça | Papel | Quando entra |
|---|---|---|
| **Vue 3** (core) | Reatividade + renderização de componentes | Hoje |
| **Vite** | Servidor de desenvolvimento e bundler | Hoje |
| **Vue Router** | Navegação entre "páginas" da SPA | Aula 04 |
| **Pinia** | Estado compartilhado entre componentes | Aula 06 |
| **Vuetify** | Biblioteca de componentes visuais prontos (Material Design) | Aula 04 |
| **Axios** | Cliente HTTP para consumir APIs | Aula 06 |

Vamos usar a versão **3.5.41** do Vue, instalada via **Vite 8.2.1** com o plugin **@vitejs/plugin-vue 6.0.8** — as mesmas versões testadas e listadas no início do curso.

### 1.1 Options API vs. Composition API

O Vue 3 oferece duas formas de escrever a lógica de um componente. Elas produzem o mesmo resultado; mudam a organização do código.

**Options API** — organiza o componente em "opções" fixas: `data()` (estado), `methods` (funções), `computed` (Aula 03), `mounted()` (ciclo de vida) etc. É o estilo herdado do Vue 2, ainda muito usado e citado no plano de curso.

```js
// Options API — cada preocupação vai em uma "caixa" pré-definida
export default {
  data() {
    return {
      contador: 0,
    }
  },
  methods: {
    incrementar() {
      this.contador++
    },
  },
  mounted() {
    console.log('componente montado, contador =', this.contador)
  },
}
```

**Composition API** — organiza o componente por funções que você importa e compõe livremente (`ref`, `reactive`, `onMounted`...), agrupando por *funcionalidade* em vez de por *tipo de opção*. É o padrão do Vue 3 moderno e o que o `create-vue` gera por padrão, dentro da sintaxe açucarada `<script setup>`.

```vue
<script setup>
// Composition API com <script setup> — tudo neste bloco já é
// automaticamente exposto ao <template>, sem "return" manual
import { ref, onMounted } from 'vue'

const contador = ref(0)

function incrementar() {
  contador.value++
}

onMounted(() => {
  console.log('componente montado, contador =', contador.value)
})
</script>
```

> **📌 Na prova**
> **Esta disciplina usa Composition API com `<script setup>`** do início ao fim, porque é o padrão gerado pelo `create-vue` e o que você vai encontrar em qualquer projeto Vue 3 novo. Nos primeiros exemplos de hoje mostramos o equivalente em Options API lado a lado — o plano de curso cita explicitamente "instância vue, data e methods" — mas a partir da Aula 03 falamos só Composition API.

## 2. Primeiro contato: Vue via CDN

Antes de qualquer ferramenta de build, vamos ver o Vue rodando com o mínimo possível: um único arquivo HTML.

```html
<!-- cdn/index.html -->
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <title>Primeiro contato com Vue</title>
</head>
<body>
  <div id="app">
    <h1>{{ titulo }}</h1>
    <p>Você clicou {{ contador }} vez(es).</p>
    <button v-on:click="incrementar">Clicar</button>
  </div>

  <script src="https://unpkg.com/vue@3.5.41/dist/vue.global.js"></script>
  <script>
    const { createApp } = Vue

    createApp({
      data() {
        return {
          titulo: 'Olá, Vue!',
          contador: 0,
        }
      },
      methods: {
        incrementar() {
          this.contador++
        },
      },
    }).mount('#app')
  </script>
</body>
</html>
```

Abra este arquivo direto no navegador (funciona com `file://`, sem precisar de servidor, porque não há módulos ES aqui). Três ideias novas:

1. **`createApp({...})`** recebe um objeto de configuração — no estilo Options API — e devolve uma instância da aplicação Vue.
2. **`.mount('#app')`** diz ao Vue: "assuma o controle deste elemento do DOM e tudo dentro dele". A partir daqui, o Vue passa a gerenciar esse pedaço de página.
3. **`{{ titulo }}`** é **interpolação de texto**: insere o valor da variável reativa `titulo` no HTML. Sempre que `titulo` muda, o texto na tela muda sozinho — sem `innerHTML`, sem `addEventListener` manual.

> **🔎 Por baixo do capô**
> `{{ }}` só funciona dentro do elemento montado (`#app` e seus descendentes). Fora dele, o Vue nem olha para o HTML — por isso o `<h1>` do exemplo fica dentro de `<div id="app">`.

O mesmo exemplo, agora em `<script setup>` (o estilo que usaremos a partir de agora), ainda via CDN mas em módulo ES:

```html
<!-- cdn/index-composition.html -->
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <title>Primeiro contato — Composition API</title>
</head>
<body>
  <div id="app"></div>

  <script type="module">
    import { createApp, ref } from 'https://unpkg.com/vue@3.5.41/dist/vue.esm-browser.js'

    createApp({
      setup() {
        const titulo = ref('Olá, Vue!')
        const contador = ref(0)

        function incrementar() {
          contador.value++
        }

        return { titulo, contador, incrementar }
      },
      template: `
        <h1>{{ titulo }}</h1>
        <p>Você clicou {{ contador }} vez(es).</p>
        <button v-on:click="incrementar">Clicar</button>
      `,
    }).mount('#app')
  </script>
</body>
</html>
```

Note que aqui, sem `<script setup>` (que só existe dentro de arquivos `.vue` compilados pelo Vite), precisamos declarar `setup()` manualmente e **retornar** o que o template usa. É exatamente esse `return` que o `<script setup>` elimina automaticamente — daí o nome "açúcar sintático".

## 3. Migrando para um projeto Vite de verdade

CDN é ótimo para aprender o conceito, mas nenhuma aplicação real do semestre vai ser um único HTML. A partir de agora usamos **Vite** com **Single File Components** (`.vue`).

### 3.1 Criando o projeto

```bash
npm create vue@latest
```

O `create-vue` (versão 3.23.0) pergunta interativamente o nome do projeto e quais recursos incluir. Para o UniEventos que construiremos em sala, as respostas são:

```text
✔ Project name: … unieventos-web
✔ Add TypeScript? … No
✔ Add JSX Support? … No
✔ Add Vue Router for Single Page Application development? … Yes
✔ Add Pinia for state management? … Yes
✔ Add Vitest for Unit testing? … No
✔ Add an End-to-End Testing Solution? › No
✔ Add ESLint for code quality? … Yes
✔ Add Prettier for code formatting? … Yes
```

Ou, sem o modo interativo, direto com flags:

```bash
npx create-vue@latest unieventos-web --router --pinia --eslint --prettier
cd unieventos-web
npm install
npm run dev
```

> **💡 Dica**
> Já habilitamos `--router` e `--pinia` mesmo sem usá-los ainda — eles só entram em cena nas Aulas 04 e 06, mas evita reconfigurar o projeto depois. Os arquivos que eles geram (`src/router/index.js`, `src/stores/counter.js`) ficam parados até lá.

### 3.2 Estrutura gerada

```text
unieventos-web/
├─ .vscode/
├─ public/favicon.ico
├─ src/
│  ├─ App.vue
│  ├─ main.js
│  ├─ router/index.js
│  └─ stores/counter.js
├─ index.html
├─ jsconfig.json
├─ package.json
└─ vite.config.js
```

| Arquivo | Papel |
|---|---|
| `index.html` | HTML raiz — único ponto de entrada real da SPA, contém `<div id="app">` |
| `src/main.js` | Ponto de entrada JS: cria a aplicação, registra plugins, monta no DOM |
| `src/App.vue` | Componente raiz — tudo que renderizamos começa aqui |
| `src/router/index.js` | Configuração de rotas (usada a partir da Aula 04) |
| `src/stores/counter.js` | Exemplo de store Pinia gerado pelo scaffold (usado a partir da Aula 06) |
| `vite.config.js` | Configuração do Vite: plugins, aliases de importação |
| `package.json` | Dependências e scripts (`npm run dev`, `npm run build`) |
| `jsconfig.json` | Ajuda o VS Code a resolver imports como `@/components/...` |

`src/main.js` gerado:

```js
// src/main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
```

Compare com o `createApp(...).mount('#app')` do exemplo CDN: é a mesma API. A diferença é que aqui `App` vem de um **componente `.vue` importado**, e `app.use(...)` registra **plugins** (Pinia, Router) que ainda não vamos usar hoje.

Rode o projeto:

```bash
npm run dev
```

O Vite sobe um servidor local (normalmente `http://localhost:5173`) com **hot module replacement**: você edita um arquivo `.vue` e a tela atualiza sozinha, sem recarregar a página inteira.

### 3.3 Anatomia de um Single File Component (SFC)

Abra `src/App.vue` gerado pelo scaffold — ele vem com bastante conteúdo de boas-vindas. Vamos substituí-lo por algo mínimo para entender a estrutura:

```vue
<!-- src/App.vue -->
<script setup>
import { ref } from 'vue'

const titulo = ref('UniEventos')
const contador = ref(0)

function incrementar() {
  contador.value++
}
</script>

<template>
  <main>
    <h1>{{ titulo }}</h1>
    <p>Cliques: {{ contador }}</p>
    <button @click="incrementar">Clicar</button>
  </main>
</template>

<style scoped>
main {
  font-family: sans-serif;
  padding: 2rem;
}

h1 {
  color: #2c3e50;
}
</style>
```

Um `.vue` tem até três blocos:

- **`<script setup>`** — lógica do componente em Composition API. Tudo declarado aqui (variáveis, funções) fica automaticamente disponível no `<template>`, sem `return` explícito — é isso que o `setup: '<script setup>'` do compilador do Vite faz por você.
- **`<template>`** — o HTML do componente, com as diretivas do Vue.
- **`<style scoped>`** — CSS que se aplica **somente** a este componente (o Vue adiciona um atributo único a cada elemento na hora do build, isolando o CSS). Sem `scoped`, o estilo vaza para a aplicação inteira.

> **⚠️ Atenção**
> `<script setup>` só existe dentro de arquivos `.vue` processados pelo Vite — não existe fora desse contexto. Por isso o exemplo CDN da Seção 2 usou `setup() { return {...} }` explícito.

## 4. Reatividade: `ref()` e `reactive()`

### 4.1 Por que `.value`

```vue
<script setup>
import { ref } from 'vue'

// ref() envolve um valor primitivo (ou qualquer valor) em um objeto reativo
const contadorVagas = ref(40)

function reduzirVaga() {
  // DENTRO do <script>, é preciso acessar/alterar via .value
  contadorVagas.value--
  console.log(contadorVagas.value)
}
</script>

<template>
  <!-- NO <template>, o Vue "desembrulha" automaticamente — sem .value -->
  <p>Vagas: {{ contadorVagas }}</p>
  <button @click="reduzirVaga">Inscrever</button>
</template>
```

> **🔎 Por baixo do capô**
> Um valor primitivo em JavaScript (`number`, `string`, `boolean`) não tem como "avisar" ninguém quando muda — não há como interceptar `contador = contador + 1` para uma variável solta. `ref()` resolve isso guardando o valor dentro de um objeto (`{ value: 40 }`) e tornando esse objeto reativo. É por isso que, no script, você sempre acessa `.value`. No `<template>`, o compilador do Vue já sabe que uma variável vinda de `ref()` precisa ser desembrulhada e faz isso por você automaticamente.

### 4.2 `reactive()` — para objetos e arrays

```vue
<script setup>
import { reactive } from 'vue'

// reactive() torna um OBJETO inteiro reativo, sem precisar de .value
const evento = reactive({
  titulo: 'Semana da Computação',
  vagas: 40,
  inscritos: 12,
})

function inscrever() {
  // acesso direto às propriedades, sem .value
  evento.inscritos++
}
</script>

<template>
  <p>{{ evento.titulo }}: {{ evento.inscritos }}/{{ evento.vagas }}</p>
  <button @click="inscrever">Inscrever</button>
</template>
```

> **🔎 Por baixo do capô**
> `reactive()` usa um **`Proxy`** do JavaScript (recurso nativo do ES2015) para interceptar leituras e escritas nas propriedades do objeto. Toda vez que você lê `evento.titulo`, o Proxy registra "alguém depende disso"; toda vez que você escreve `evento.inscritos = ...`, o Proxy avisa "isso mudou, quem depende precisa atualizar". Vamos detalhar esse mecanismo na Aula 03, no box de padrão de projeto **Proxy**.

### 4.3 Quando usar cada um

| Situação | Use |
|---|---|
| Valor único (número, string, boolean) | `ref()` |
| Objeto ou array com várias propriedades relacionadas | `reactive()` (ou `ref()` também funciona para objetos — é uma escolha de estilo) |
| Precisa **substituir o valor inteiro** depois (ex.: `eventos = novaLista`) | `ref()` — `reactive()` não permite reatribuir a variável inteira sem perder a reatividade |

```vue
<script setup>
import { ref } from 'vue'

// Para uma LISTA que será recarregada inteira (ex.: vinda de uma API),
// ref() é mais seguro: dá para trocar o array inteiro sem perder reatividade.
const eventos = ref([])

async function carregarEventos() {
  eventos.value = [
    { id: 1, titulo: 'Semana da Computação' },
    { id: 2, titulo: 'Oficina de Vue.js' },
  ]
}
</script>
```

> **⚠️ Atenção**
> Se você usasse `reactive([])` e depois tentasse `eventos = [...]` (reatribuir a variável), perderia a conexão reativa — o `template` continuaria olhando para o array antigo. Com `reactive`, mude o conteúdo (`eventos.push(...)`, `eventos.splice(...)`), nunca a referência.

**Equivalência com Options API** — o `data()` que você viu na Seção 1.1 usa reatividade automática em tudo que ele retorna, sem você escolher entre `ref` e `reactive`:

```js
// Options API — Vue decide a reatividade por trás das cortinas
export default {
  data() {
    return {
      contadorVagas: 40, // equivale a um ref
      evento: { titulo: 'Semana da Computação', inscritos: 12 }, // equivale a um reactive
    }
  },
  methods: {
    inscrever() {
      this.evento.inscritos++ // this.<propriedade>, sem .value
    },
  },
}
```

## 5. Diretivas

Diretivas são atributos especiais do Vue, prefixados com `v-`, que ligam o `template` ao estado reativo. Vamos ver cada uma com exemplo próprio.

### 5.1 `v-bind` — vincular atributos HTML

```vue
<script setup>
import { ref } from 'vue'

const evento = ref({
  titulo: 'Oficina de Vue.js',
  imagemUrl: '/img/oficina-vue.jpg',
  linkInativo: true,
})
</script>

<template>
  <!-- forma completa -->
  <img v-bind:src="evento.imagemUrl" v-bind:alt="evento.titulo" />

  <!-- atalho ":" — é o que se usa no dia a dia -->
  <img :src="evento.imagemUrl" :alt="evento.titulo" />

  <!-- vinculando um atributo booleano -->
  <button :disabled="evento.linkInativo">Ver detalhes</button>
</template>
```

`v-bind` conecta um **atributo do HTML** a uma **expressão JavaScript reativa**. Sem ele, `src="evento.imagemUrl"` seria só o texto literal `"evento.imagemUrl"` — não avaliaria a expressão.

### 5.2 `v-on` — escutar eventos

```vue
<script setup>
import { ref } from 'vue'

const contador = ref(0)

function incrementar() {
  contador.value++
}

function tratarEnvio() {
  console.log('formulário enviado, sem recarregar a página')
}
</script>

<template>
  <!-- forma completa -->
  <button v-on:click="incrementar">+1</button>

  <!-- atalho "@" — o que se usa no dia a dia -->
  <button @click="incrementar">+1</button>

  <!-- modificador .prevent: chama event.preventDefault() automaticamente -->
  <form @submit.prevent="tratarEnvio">
    <button type="submit">Enviar</button>
  </form>

  <!-- modificador .stop: chama event.stopPropagation() -->
  <div @click="console.log('clique no pai')">
    <button @click.stop="console.log('clique só no botão')">Não propaga</button>
  </div>

  <!-- modificador .once: o handler roda só na primeira vez -->
  <button @click.once="console.log('só uma vez')">Clique único</button>

  <!-- modificador de tecla: só dispara com Enter -->
  <input @keyup.enter="incrementar" placeholder="Pressione Enter" />
</template>
```

### 5.3 `v-model` — vinculação bidirecional em formulários

`v-model` é açúcar sintático que combina `v-bind` (mostra o valor) com `v-on` (atualiza o valor a cada mudança), poupando você de escrever os dois manualmente.

```vue
<script setup>
import { ref } from 'vue'

const busca = ref('')
const observacoes = ref('')
const aceitaTermos = ref(false)
const categoriasEscolhidas = ref([])
const categoriaSelecionada = ref('palestra')
const email = ref('')
</script>

<template>
  <!-- input de texto -->
  <input v-model="busca" type="text" placeholder="Buscar evento..." />
  <p>Buscando por: {{ busca }}</p>

  <!-- textarea -->
  <textarea v-model="observacoes" placeholder="Observações"></textarea>

  <!-- checkbox único: liga a uma variável boolean -->
  <label>
    <input v-model="aceitaTermos" type="checkbox" />
    Aceito os termos
  </label>

  <!-- vários checkboxes: liga a um array — cada "value" marcado entra no array -->
  <label><input v-model="categoriasEscolhidas" type="checkbox" value="palestra" /> Palestra</label>
  <label><input v-model="categoriasEscolhidas" type="checkbox" value="minicurso" /> Minicurso</label>
  <p>Selecionadas: {{ categoriasEscolhidas }}</p>

  <!-- radio: só um valor por grupo de "name" implícito pelo v-model -->
  <label><input v-model="categoriaSelecionada" type="radio" value="palestra" /> Palestra</label>
  <label><input v-model="categoriaSelecionada" type="radio" value="workshop" /> Workshop</label>

  <!-- select -->
  <select v-model="categoriaSelecionada">
    <option value="palestra">Palestra</option>
    <option value="minicurso">Minicurso</option>
    <option value="workshop">Workshop</option>
  </select>

  <!-- modificadores -->
  <!-- .trim: remove espaços das pontas automaticamente -->
  <input v-model.trim="email" type="email" placeholder="seu@email.com" />

  <!-- .number: converte o valor digitado para Number -->
  <input v-model.number="categoriaSelecionada" type="number" />

  <!-- .lazy: sincroniza no evento "change" (ao sair do campo), não a cada tecla -->
  <input v-model.lazy="busca" type="text" />
</template>
```

> **💡 Dica**
> `v-model` é o par perfeito para o formulário de inscrição do UniEventos que vamos montar hoje: o valor do campo de busca já fica disponível como variável reativa, sem escrever um único `addEventListener`.

### 5.4 `v-if`, `v-else-if`, `v-else`

```vue
<script setup>
import { ref } from 'vue'

const vagasRestantes = ref(0)
</script>

<template>
  <p v-if="vagasRestantes > 10">Vagas disponíveis</p>
  <p v-else-if="vagasRestantes > 0">Últimas vagas!</p>
  <p v-else>Evento lotado</p>
</template>
```

`v-if` (e seus complementos) **adiciona ou remove o elemento do DOM** conforme a condição — quando falso, o elemento simplesmente não existe na página.

### 5.5 `v-show` — a alternativa que só esconde

```vue
<script setup>
import { ref } from 'vue'

const mostrarDetalhes = ref(false)
</script>

<template>
  <button @click="mostrarDetalhes = !mostrarDetalhes">Alternar detalhes</button>

  <!-- o elemento SEMPRE existe no DOM; v-show só alterna display: none -->
  <div v-show="mostrarDetalhes">
    <p>Estes são os detalhes completos do evento.</p>
  </div>
</template>
```

| | `v-if` | `v-show` |
|---|---|---|
| Como funciona | Remove/insere o elemento no DOM | Alterna `display: none` via CSS |
| Custo de alternar | Mais caro (recria o elemento) | Mais barato (só troca CSS) |
| Custo inicial se falso | Mais barato (nem renderiza) | Mais caro (sempre renderiza) |
| Quando usar | Condição muda raramente | Condição alterna com frequência (ex.: abrir/fechar painel) |

### 5.6 `v-for` e a importância da `:key`

```vue
<script setup>
import { ref } from 'vue'

const eventos = ref([
  { id: 1, titulo: 'Semana da Computação', categoria: 'palestra' },
  { id: 2, titulo: 'Oficina de Vue.js', categoria: 'minicurso' },
  { id: 3, titulo: 'Hackathon FACET', categoria: 'workshop' },
])
</script>

<template>
  <ul>
    <!-- CORRETO: key única e estável (o id do dado, nunca o índice) -->
    <li v-for="evento in eventos" :key="evento.id">
      {{ evento.titulo }} — {{ evento.categoria }}
    </li>
  </ul>

  <!-- v-for também expõe o índice, como segundo parâmetro -->
  <ol>
    <li v-for="(evento, indice) in eventos" :key="evento.id">
      {{ indice + 1 }}. {{ evento.titulo }}
    </li>
  </ol>
</template>
```

**O bug do índice como `:key`:**

```vue
<script setup>
import { ref } from 'vue'

const eventos = ref([
  { id: 1, titulo: 'Semana da Computação' },
  { id: 2, titulo: 'Oficina de Vue.js' },
  { id: 3, titulo: 'Hackathon FACET' },
])

function removerPrimeiro() {
  eventos.value.shift() // remove o item do início
}
</script>

<template>
  <!-- ERRADO: usar o índice como key -->
  <div v-for="(evento, indice) in eventos" :key="indice">
    <input type="checkbox" /> {{ evento.titulo }}
  </div>

  <button @click="removerPrimeiro">Remover o primeiro</button>
</template>
```

Se cada `<input type="checkbox">` tiver estado próprio (marcado por quem interage) e você remover o primeiro item da lista, o Vue reaproveitará os elementos DOM **pelo índice**: o segundo item (índice `0` agora) herda o checkbox que estava marcado no antigo primeiro item, mesmo sendo um dado diferente. O texto atualiza corretamente, mas o **estado interno do elemento (checkbox marcado, valor de input, foco) fica errado**, porque o Vue pensa que é "o mesmo elemento" da posição `0`.

> **⚠️ Atenção**
> Use sempre um identificador **estável e único do dado** (`evento.id`) como `:key`, nunca o índice do `v-for`. O índice muda quando a lista é reordenada, filtrada ou tem itens removidos — e o Vue usa a `key` exatamente para saber "isso é o mesmo item de antes ou é outro?".

### 5.7 `v-text` e `v-html`

```vue
<script setup>
import { ref } from 'vue'

const descricaoSimples = ref('Evento sobre Vue.js')
const descricaoComHtml = ref('<strong>Evento</strong> sobre Vue.js')
</script>

<template>
  <!-- v-text é equivalente a {{ }}, mas substitui TODO o conteúdo do elemento -->
  <p v-text="descricaoSimples"></p>

  <!-- interpolação normal: sempre trata o conteúdo como TEXTO puro (escapa HTML) -->
  <p>{{ descricaoComHtml }}</p>
  <!-- renderiza literalmente: <strong>Evento</strong> sobre Vue.js -->

  <!-- v-html: injeta HTML de verdade, interpretado pelo navegador -->
  <p v-html="descricaoComHtml"></p>
  <!-- renderiza: Evento (em negrito) sobre Vue.js -->
</template>
```

> **⚠️ Atenção — risco de XSS**
> `v-html` injeta HTML bruto na página, sem escapar. Se o conteúdo vier de um usuário (comentário, campo de formulário, dado de API não confiável) e contiver `<script>` ou atributos como `onerror=`, isso **executa no navegador de quem visualiza a página** — um ataque de Cross-Site Scripting (XSS). Use `v-html` só com conteúdo que você controla (texto formatado vindo do seu próprio backend, sanitizado). Para exibir texto de usuário, use interpolação `{{ }}` normal, que sempre escapa.

## 6. Ciclo de vida do componente

Todo componente Vue passa por fases previsíveis, do momento em que é criado até ser destruído.

```text
criação do componente
        │
        ▼
  onBeforeMount()   ← ainda não existe no DOM real
        │
        ▼
   [Vue monta o componente no DOM]
        │
        ▼
    onMounted()      ← já existe no DOM, pode acessar elementos, disparar fetch
        │
        ▼
  (o componente vive aqui — reage a mudanças de estado)
        │
        ├──► dado reativo muda
        │         │
        │         ▼
        │   onBeforeUpdate()  ← estado já mudou, DOM ainda não
        │         │
        │         ▼
        │   [Vue re-renderiza o DOM]
        │         │
        │         ▼
        │      onUpdated()    ← DOM já reflete o novo estado
        │         │
        │         └──► volta a "viver" aqui
        │
        ▼
  onBeforeUnmount()  ← componente prestes a ser removido
        │
        ▼
   [Vue remove o componente do DOM]
        │
        ▼
    onUnmounted()     ← já foi removido; hora de limpar recursos
```

```vue
<!-- src/components/DemoCicloDeVida.vue -->
<script setup>
import { ref, onBeforeMount, onMounted, onBeforeUpdate, onUpdated, onBeforeUnmount, onUnmounted } from 'vue'

const segundos = ref(0)
let intervaloId = null

onBeforeMount(() => {
  console.log('[ciclo] onBeforeMount — ainda não está no DOM')
})

onMounted(() => {
  console.log('[ciclo] onMounted — já está no DOM, iniciando o relógio')

  // setInterval é um recurso "externo" ao Vue — precisa ser limpo manualmente
  intervaloId = setInterval(() => {
    segundos.value++
  }, 1000)
})

onBeforeUpdate(() => {
  console.log('[ciclo] onBeforeUpdate — segundos mudou para', segundos.value, 'mas o DOM ainda não')
})

onUpdated(() => {
  console.log('[ciclo] onUpdated — DOM já mostra', segundos.value)
})

onBeforeUnmount(() => {
  console.log('[ciclo] onBeforeUnmount — componente prestes a sumir')
})

onUnmounted(() => {
  console.log('[ciclo] onUnmounted — limpando o setInterval')
  // ESSENCIAL: sem isso, o timer continua rodando mesmo após o
  // componente sumir da tela — um vazamento de memória clássico.
  clearInterval(intervaloId)
})
</script>

<template>
  <p>Segundos desde a montagem: {{ segundos }}</p>
</template>
```

**Equivalência com Options API:**

| Composition API | Options API |
|---|---|
| `onBeforeMount` | `beforeMount()` |
| `onMounted` | `mounted()` |
| `onBeforeUpdate` | `beforeUpdate()` |
| `onUpdated` | `updated()` |
| `onBeforeUnmount` | `beforeUnmount()` |
| `onUnmounted` | `unmounted()` |

```js
// Options API — os mesmos hooks, como métodos especiais do objeto
export default {
  data() {
    return { segundos: 0, intervaloId: null }
  },
  mounted() {
    console.log('mounted')
    this.intervaloId = setInterval(() => { this.segundos++ }, 1000)
  },
  unmounted() {
    clearInterval(this.intervaloId)
  },
}
```

> **📌 Na prova**
> `onMounted` é, de longe, o hook mais usado na prática — é onde disparamos requisições `fetch` (Aula 03) porque é o primeiro momento em que temos garantia de que o DOM existe. `onUnmounted` é onde limpamos qualquer recurso externo (`setInterval`, `addEventListener` em `window`, conexões abertas) para não vazar memória quando o componente sai de cena.

## 🧩 Padrão de projeto em uso

> ### 🧩 Padrão de projeto em uso — Observer (comportamental)
>
> O padrão **Observer** define uma relação um-para-muitos entre um objeto (o *subject*, que muda de estado) e vários *observers*, que são notificados automaticamente sempre que o subject muda — sem que o subject precise conhecer os observers individualmente.
>
> Um Observer "na mão", em JavaScript puro:
>
> ```js
> // Um EventTarget simplificado — a base do Observer em JS puro
> class ContadorObservavel {
>   constructor() {
>     this.valor = 0
>     this.observadores = []
>   }
>
>   observar(funcaoCallback) {
>     this.observadores.push(funcaoCallback)
>   }
>
>   incrementar() {
>     this.valor++
>     // notifica TODOS os observadores registrados
>     this.observadores.forEach((callback) => callback(this.valor))
>   }
> }
>
> const contador = new ContadorObservavel()
> contador.observar((valor) => console.log('UI A atualizada:', valor))
> contador.observar((valor) => console.log('UI B atualizada:', valor))
> contador.incrementar() // dispara os dois observadores
> ```
>
> **É exatamente isso que o sistema de reatividade do Vue faz por baixo dos panos.** Quando você escreve `{{ contador }}` no template, o Vue registra esse trecho do DOM como um "observador" da variável `contador`. Quando você escreve `contador.value++`, o Vue percorre a lista de observadores daquela variável (os pedaços de template que a usam) e re-renderiza só eles — sem você escrever `observar()` ou `notificar()` manualmente. `ref` e `reactive` são, na essência, subjects observáveis; cada trecho do template que os lê vira, automaticamente, um observer. Vamos abrir esse mecanismo com mais detalhe na Aula 03, quando falarmos do padrão **Proxy**.

## 💻 Mão na massa — primeira versão do UniEventos

Vamos construir, dentro do projeto `unieventos-web` criado na Seção 3, a primeira tela funcional: lista de eventos com busca, filtro por categoria e inscrição.

**Passo 1 — dados de exemplo.** Crie um arquivo separado só com os dados, para manter o componente organizado (o mesmo raciocínio do módulo `eventos.js` da Aula 01).

```js
// src/data/eventos.js
export const eventosIniciais = [
  {
    id: 1,
    titulo: 'Semana da Computação',
    categoria: 'palestra',
    dataHora: '2026-09-10T19:00:00',
    local: 'Auditório Central',
    vagas: 40,
    inscritos: 12,
  },
  {
    id: 2,
    titulo: 'Oficina de Vue.js',
    categoria: 'minicurso',
    dataHora: '2026-08-20T14:00:00',
    local: 'Laboratório 3',
    vagas: 25,
    inscritos: 25,
  },
  {
    id: 3,
    titulo: 'Hackathon FACET',
    categoria: 'workshop',
    dataHora: '2026-10-05T08:00:00',
    local: 'Bloco B',
    vagas: 60,
    inscritos: 18,
  },
  {
    id: 4,
    titulo: 'Introdução a IA',
    categoria: 'palestra',
    dataHora: '2026-08-18T19:30:00',
    local: 'Auditório Central',
    vagas: 80,
    inscritos: 55,
  },
]
```

**Passo 2 — o componente principal.** Ainda usamos `filter` "na mão" dentro de uma função (vamos trocar por `computed`, que faz cache, na Aula 03 — por hoje o objetivo é praticar diretivas).

```vue
<!-- src/App.vue -->
<script setup>
import { ref } from 'vue'
import { eventosIniciais } from './data/eventos.js'

const eventos = ref(eventosIniciais)
const busca = ref('')
const categoriaFiltro = ref('')

// Função comum (não computed ainda) — recalculada manualmente a cada uso.
// Repare que ela SEMPRE cria um array novo com filter, sem mutar `eventos`.
function obterEventosFiltrados() {
  return eventos.value
    .filter((evento) => evento.titulo.toLowerCase().includes(busca.value.toLowerCase()))
    .filter((evento) => categoriaFiltro.value === '' || evento.categoria === categoriaFiltro.value)
}

function inscrever(eventoId) {
  const evento = eventos.value.find((item) => item.id === eventoId)
  if (!evento) return

  if (evento.inscritos >= evento.vagas) {
    alert('Este evento está lotado.')
    return
  }

  evento.inscritos++
}

function vagasRestantes(evento) {
  return evento.vagas - evento.inscritos
}
</script>

<template>
  <main class="pagina">
    <h1>UniEventos</h1>
    <p>Encontre e inscreva-se em eventos acadêmicos.</p>

    <div class="filtros">
      <input
        v-model.trim="busca"
        type="text"
        placeholder="Buscar por título..."
      />

      <select v-model="categoriaFiltro">
        <option value="">Todas as categorias</option>
        <option value="palestra">Palestra</option>
        <option value="minicurso">Minicurso</option>
        <option value="workshop">Workshop</option>
      </select>
    </div>

    <ul class="lista-eventos">
      <li
        v-for="evento in obterEventosFiltrados()"
        :key="evento.id"
        class="card-evento"
      >
        <h2>{{ evento.titulo }}</h2>
        <p>Categoria: {{ evento.categoria }}</p>
        <p>Local: {{ evento.local }}</p>
        <p v-if="vagasRestantes(evento) > 0">
          {{ vagasRestantes(evento) }} vaga(s) restante(s)
        </p>
        <p v-else class="lotado">Evento lotado</p>

        <button
          :disabled="vagasRestantes(evento) === 0"
          @click="inscrever(evento.id)"
        >
          Inscrever-se
        </button>
      </li>
    </ul>

    <p v-if="obterEventosFiltrados().length === 0" class="vazio">
      Nenhum evento encontrado com estes filtros.
    </p>
  </main>
</template>

<style scoped>
.pagina {
  max-width: 720px;
  margin: 0 auto;
  padding: 2rem;
  font-family: sans-serif;
}

.filtros {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.lista-eventos {
  list-style: none;
  padding: 0;
  display: grid;
  gap: 1rem;
}

.card-evento {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
}

.lotado {
  color: #c0392b;
  font-weight: bold;
}

.vazio {
  text-align: center;
  color: #666;
}
</style>
```

> **⚠️ Atenção**
> Repare que `obterEventosFiltrados()` é chamada **três vezes** no template (na `v-for`, e de novo para checar se está vazio). Cada chamada refaz o `filter` duas vezes do zero — funciona, mas é desperdício de processamento e, pior, dificulta manter os resultados sincronizados. Vamos resolver isso com `computed()` já na próxima aula.

## 🧪 Laboratório

**1. Contador de inscritos totais** — adicione, logo abaixo do `<h1>`, um parágrafo mostrando quantas pessoas estão inscritas somando todos os eventos, usando `reduce` (Aula 01).

Resultado esperado: um número que aumenta a cada clique em "Inscrever-se".

<details markdown="1">
<summary>Dica</summary>

`eventos.value.reduce((total, evento) => total + evento.inscritos, 0)` dentro de uma função chamada no template, ou direto em uma expressão de interpolação.
</details>

**2. Botão de limpar filtros** — adicione um botão que zera `busca` e `categoriaFiltro` de uma vez.

Resultado esperado: clicar no botão limpa o campo de texto e volta o select para "Todas as categorias".

<details markdown="1">
<summary>Dica</summary>

```js
function limparFiltros() {
  busca.value = ''
  categoriaFiltro.value = ''
}
```
</details>

**3. Destacar evento quase lotado com `v-show`** — mostre um aviso `"Últimas vagas!"` com `v-show` (não `v-if`) quando `vagasRestantes(evento) <= 5 && vagasRestantes(evento) > 0`.

Resultado esperado: o aviso aparece/some conforme inscrições, sem recriar o elemento no DOM (confira no DevTools, aba Elements).

<details markdown="1">
<summary>Dica</summary>

`<span v-show="vagasRestantes(evento) <= 5 && vagasRestantes(evento) > 0">Últimas vagas!</span>`
</details>

**4. Modificador `.once` em uma mensagem de boas-vindas** — adicione um botão "Ver dica" que mostra um alerta apenas na primeira vez que for clicado, usando `@click.once`.

Resultado esperado: cliques seguintes não fazem nada.

<details markdown="1">
<summary>Dica</summary>

`<button @click.once="alert('Dica: use os filtros para encontrar eventos mais rápido!')">Ver dica</button>`
</details>

**5. Corrigir uma `:key` proposital** — troque temporariamente `:key="evento.id"` por `:key="indiceDoLoop"` (usando a forma `v-for="(evento, indiceDoLoop) in ..."`), adicione um `<input type="checkbox">` dentro de cada card, marque alguns, filtre por categoria e observe o comportamento estranho dos checkboxes. Depois desfaça a mudança.

Resultado esperado: você reproduz em sala o bug descrito na Seção 5.6 antes de corrigi-lo.

<details markdown="1">
<summary>Dica</summary>

O bug aparece quando a lista filtrada muda de tamanho/ordem — os checkboxes "grudam" na posição, não no evento.
</details>

## 🐛 Erros comuns e como resolver

| Sintoma | Causa | Solução |
|---|---|---|
| Tela em branco, console mostra erro sobre `.vue` | Arquivo `.vue` com erro de sintaxe, ou `<script setup>` mal fechado | Confira se os três blocos (`script`, `template`, `style`) estão bem formados e balanceados |
| Alterei `contador` no script mas a tela não atualiza | Esqueceu o `.value` ao alterar um `ref` | Sempre `variavel.value = novoValor` dentro do `<script setup>` |
| `v-model` não atualiza nada | Esqueceu de declarar a variável com `ref()`, ou digitou o nome errado no template | Confira se a variável usada no `v-model` existe e foi criada com `ref()` |
| Checkbox/input "gruda" em posição errada após filtrar/remover | `:key` usando o índice do `v-for` | Use um identificador estável do dado, como `evento.id` |
| `v-html` mostra texto cru com as tags `<...>` aparecendo | Trocou `v-html` por interpolação `{{ }}` sem querer | `{{ }}` sempre escapa HTML; use `v-html` só quando o objetivo é renderizar HTML de verdade |

## 🏠 Atividade assíncrona (1 h)

No repositório do seu projeto autoral:

1. Rode `npm create vue@latest` (ou `npx create-vue@latest <seu-tema>-web --router --pinia --eslint --prettier`) dentro da pasta do seu projeto.
2. Crie um arquivo `src/data/<entidade principal>.js` com um array de pelo menos 4 itens de exemplo do seu domínio (equivalente ao `eventos.js` de hoje).
3. Em `src/App.vue`, monte uma primeira listagem usando `v-for` com `:key` correto, um campo de busca com `v-model` e pelo menos um filtro (`v-model` em `<select>`).
4. Adicione uma ação (ex.: "reservar", "favoritar", "adicionar ao carrinho" — o verbo do seu domínio) usando `v-on`/`@click`.
5. Faça commit e push.

**Critério de pronto:** `npm run dev` abre a aplicação, a lista aparece, busca e filtro funcionam, `:key` usa um identificador estável.

## ✅ Checkpoint do projeto autoral

- [ ] Projeto Vite criado com `create-vue` (flags `--router --pinia`) no repositório do tema autoral.
- [ ] `src/data/*.js` com dados de exemplo do domínio escolhido.
- [ ] Listagem funcionando com `v-for` e `:key` estável (nunca o índice).
- [ ] Busca com `v-model` e pelo menos um filtro funcionando.
- [ ] Uma ação de interação implementada com `v-on`/`@click`.
- [ ] Commit enviado ao GitHub.

## 📚 Para aprofundar

- [Documentação oficial do Vue 3 — Introdução](https://vuejs.org/guide/introduction.html)
- [Vue 3 — Reactivity Fundamentals](https://vuejs.org/guide/essentials/reactivity-fundamentals.html)
- [Vue 3 — Template Syntax (diretivas)](https://vuejs.org/guide/essentials/template-syntax.html)
- [Vue 3 — Lifecycle Hooks](https://vuejs.org/guide/essentials/lifecycle.html)
- [Vue 3 — List Rendering (`v-for` e `:key`)](https://vuejs.org/guide/essentials/list.html)
- [Documentação do Vite](https://vitejs.dev/)

---

**Próxima aula (03, 26/08/2026):** aprofundamos `v-for`, resolvemos o antipadrão `v-for` + `v-if` juntos, introduzimos `computed()` (com cache de verdade) e usamos `onMounted()` para carregar dados de uma fonte assíncrona, com estados de carregando/erro/vazio.
