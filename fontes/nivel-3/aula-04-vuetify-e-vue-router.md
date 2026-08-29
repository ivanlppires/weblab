# Aula 04 — Introdução a Vuetify e Vue Router

> **Nível 3 — Frameworks Modernos** · Unidade 1: Fundamentos de front-end com Vue.js
> WebLab · UNEMAT Sinop · Prof. Ivan Luiz Pedroso Pires

Nas Aulas 02 e 03 você construiu o UniEventos em Vue puro: listagem com `v-for`, filtros com `computed()`, carregamento assíncrono em `onMounted()` e HTML/CSS escritos à mão. Hoje ele ganha interface profissional com **Vuetify** e navegação real com **Vue Router**, virando uma SPA de verdade — e você recebe as instruções completas da Avaliação 1.

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Explicar o que é um design system e por que um framework de UI acelera (e padroniza) o desenvolvimento de interfaces.
- Instalar e configurar o Vuetify 4 em um projeto Vite/Vue 3 seguindo exatamente os passos testados nesta disciplina.
- Estruturar uma aplicação com `v-app`, `v-app-bar`, `v-navigation-drawer`, `v-main` e o sistema de grid `v-container`/`v-row`/`v-col`.
- Usar os componentes essenciais do Vuetify (`v-card`, `v-btn`, `v-chip`, `v-icon`, `v-list`, `v-alert`, `v-dialog`, `v-snackbar`, `v-text-field`, `v-select`, `v-img`, `v-progress-circular`) para montar telas reais.
- Configurar um tema institucional customizado e implementar um alternador de tema claro/escuro.
- Criar rotas com Vue Router 5 (`createRouter`, `createWebHistory`), navegar com `<RouterLink>`/`<RouterView>`, ler parâmetros de rota e tratar rota 404.
- Transformar o UniEventos de página única em uma SPA navegável com múltiplas views.

## 📋 Pré-requisitos desta aula

Antes de começar, confirme que você tem:

- [ ] O projeto UniEventos das aulas 02–03 rodando localmente com `npm run dev` (lista de eventos com filtro, `v-for`, `v-if`, `computed`, `onMounted`, carregamento assíncrono com `fetch`).
- [ ] Node.js 22.22.2 LTS instalado (`node -v`). O `create-vue` exige `^22.18.0 || >=24.12.0`.
- [ ] Git configurado e uma conta no GitHub — hoje você vai precisar de um repositório público para a Avaliação 1.
- [ ] Revisão rápida: `<script setup>`, `ref`, `computed`, `v-bind`, `v-on`, `v-model`, `v-if`/`v-for` com `:key`, `onMounted`.

> **📌 Na prova:** hoje marca o fim da Unidade 1. Tudo que vier depois — Vuetify avançado, Axios, Pinia — pressupõe que você sabe montar uma SPA com rotas. Não pule esta aula.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Design system, Material Design 3, instalação do Vuetify 4, estrutura de aplicação e grid |
| 2 | 50 min | Componentes essenciais do Vuetify, tema customizado, Vue Router 5 (rotas, parâmetros, navegação) |
| 3 | 50 min | Mão na massa: migração do UniEventos para SPA com layout, views e tema institucional + instruções da Avaliação 1 |

## 1. Por que usar um framework de UI

Nas aulas 02 e 03 você escreveu HTML e CSS à mão para estilizar os cards de evento. Funciona, mas em um projeto real isso significa reinventar, para cada tela nova, decisões que já foram tomadas mil vezes por outras equipes: como um botão deve reagir ao toque, quanto de espaçamento um card precisa, que cor de texto garante contraste suficiente sobre um fundo azul.

Um **framework de UI** (ou biblioteca de componentes) resolve isso entregando componentes prontos — botões, cartões, campos de formulário, tabelas, diálogos — que já implementam essas decisões de forma consistente. Isso é diferente de um framework como o Vue, que resolve *como a interface reage a dados*; um framework de UI resolve *como a interface se parece e se comporta visualmente*.

A vantagem central é o **design system**: um conjunto de regras (cores, tipografia, espaçamento, elevação, animação) aplicado uniformemente em toda a aplicação. Sem um design system, cada componente vira uma ilha visual, e a interface fica com "cara de colcha de retalhos". Com um, o card de evento, o formulário de inscrição e o painel administrativo compartilham a mesma linguagem visual — mesmo que tenham sido escritos em dias diferentes por pessoas diferentes.

### Material Design 3 em uma página

O Vuetify 4 implementa o **Material Design 3 (MD3)**, o design system do Google usado no Android e em produtos como Gmail e YouTube. Os pilares que importam para o dia a dia:

- **Color roles** — em vez de "azul" e "cinza", você pensa em papéis: `primary` (ação principal), `secondary` (ação de apoio), `error`, `success`, `warning`, `info`, `surface` (fundo de cartões) e `background`. Trocar o tema não exige trocar cada componente — só redefinir os papéis.
- **Elevação** — sombras indicam hierarquia (o que está "mais perto" do usuário). O MD3 no Vuetify 4 trabalha com uma escala reduzida de 6 níveis (0 a 5), mais sutil que a escala antiga de 0 a 24 do Material Design 2.
- **Tipografia em escala** — títulos, corpo e rótulos seguem uma escala tipográfica nomeada (`display`, `headline`, `title`, `body`, `label`), cada uma em tamanhos `large`/`medium`/`small`.
- **Forma e espaçamento** — cantos arredondados e um sistema de espaçamento em múltiplos de 4px, aplicado por classes utilitárias.

> **⚠️ Atenção:** o Vuetify 4 migrou a tipografia de MD2 para MD3. As classes antigas `text-h1` … `text-h6` continuam existindo, mas mudaram de tamanho e semântica. Os equivalentes MD3 são nomes como `text-display-large`, `text-headline-medium`, `text-title-large`, `text-body-medium`, `text-label-large`. Nesta disciplina, prefira citar explicitamente a classe MD3 ou definir sua própria tipografia — não assuma que `text-h4` de um tutorial antigo vai parecer do jeito que você viu em vídeo.

## 2. Instalando o Vuetify 4

Vamos instalar o Vuetify no projeto UniEventos que você já tem. Os comandos abaixo são os mesmos testados no ambiente da disciplina — siga exatamente esta ordem.

```bash
npm install vuetify @mdi/font
npm install -D vite-plugin-vuetify
```

O primeiro comando instala o Vuetify em si e a fonte de ícones **Material Design Icons** (MDI), que usaremos em botões, listas e menus. O segundo instala o plugin do Vite que faz o **autoimport** dos componentes — sem ele, você teria que importar manualmente cada `v-card`, `v-btn` etc. em cada arquivo `.vue`, o que é inviável em um projeto com dezenas de telas.

Configure o `vite.config.js`:

```js
// vite.config.js
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'

export default defineConfig({
  plugins: [
    vue({ template: { transformAssetUrls } }),
    vuetify({ autoImport: true }),
  ],
  resolve: {
    alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) },
  },
})
```

Repare em dois detalhes:

- `transformAssetUrls` é passado ao plugin do Vue para que caminhos de imagem usados dentro de props do Vuetify (como `src` de `v-img`) sejam resolvidos corretamente pelo Vite.
- `vuetify({ autoImport: true })` é o que permite usar `<v-card>`, `<v-btn>` e qualquer outro componente do Vuetify **sem importar nada** no `<script setup>`. O plugin varre seus templates em tempo de build, detecta quais componentes e diretivas você usou, e injeta o registro automaticamente. Isso substitui o padrão antigo de fazer `import * as components from 'vuetify/components'` e registrar tudo manualmente (ou, pior, registrar tudo globalmente e inflar o bundle).

Agora o `src/main.js`:

```js
// src/main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'

const vuetify = createVuetify({
  theme: { defaultTheme: 'light' },   // v4: o padrão virou 'system'
})

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(vuetify)
app.mount('#app')
```

Três importações merecem atenção:

1. `'@mdi/font/css/materialdesignicons.css'` — carrega a fonte de ícones. Sem isso, `<v-icon>mdi-account</v-icon>` aparece como um quadrado vazio.
2. `'vuetify/styles'` — o CSS base do Vuetify (grid, tipografia, reset parcial).
3. `createVuetify(...)` — cria a instância do Vuetify, análoga ao `createPinia()` ou `createRouter()`: você a registra na aplicação com `app.use(vuetify)`.

> **⚠️ Atenção:** no Vuetify 4, o tema padrão passou a ser `'system'` — ou seja, se você não configurar nada, a aplicação vai seguir a preferência de tema (claro/escuro) do sistema operacional do usuário. Isso é ótimo em produção, mas péssimo para dar aula: metade da turma veria uma tela clara e a outra metade, escura, sem que ninguém tivesse mudado nada. Por isso declaramos `defaultTheme: 'light'` explicitamente — mais adiante, na seção de tema, vamos configurar isso de verdade com cores institucionais.

> **🔎 Por baixo do capô:** `app.use(vuetify)` funciona exatamente como `app.use(router)` ou `app.use(pinia)` — é o mecanismo de **plugin** do Vue. Um plugin é um objeto com um método `install(app, options)` que o Vue chama internamente. Isso é o mesmo padrão que você vai usar para instalar qualquer biblioteca de terceiros no ecossistema Vue.

Depois de configurar os dois arquivos, rode:

```bash
npm run dev
```

Se a tela carregar sem erros no console, o Vuetify está funcionando. Um teste rápido: coloque `<v-btn color="primary">Teste</v-btn>` em qualquer template e veja se aparece um botão estilizado (não um `<button>` cru do navegador).

## 3. Estrutura de aplicação Vuetify

Toda aplicação Vuetify é envolvida por um componente raiz obrigatório: `<v-app>`. Ele injeta o contexto de tema, o sistema de layout responsivo e o container onde diálogos e menus são renderizados (via teleport). **Sem `v-app`, nada no Vuetify funciona direito** — nem cores de tema, nem posicionamento de `v-dialog`.

Dentro de `v-app`, os blocos estruturais mais comuns são:

| Componente | Papel |
|---|---|
| `v-app-bar` | barra superior fixa — logotipo, título, ações, botão de menu |
| `v-navigation-drawer` | menu lateral (fixo ou retrátil) |
| `v-main` | área de conteúdo principal — se ajusta automaticamente ao espaço ocupado por app-bar e drawer |
| `v-footer` | rodapé |

```vue
<!-- src/App.vue (esqueleto conceitual — vamos completar na seção Mão na massa) -->
<template>
  <v-app>
    <v-app-bar color="primary">
      <v-app-bar-title>UniEventos</v-app-bar-title>
    </v-app-bar>

    <v-navigation-drawer>
      <!-- itens de menu aqui -->
    </v-navigation-drawer>

    <v-main>
      <v-container>
        <!-- conteúdo da página aqui -->
      </v-container>
    </v-main>

    <v-footer app color="primary">
      <span>UNEMAT · FACET · 2026</span>
    </v-footer>
  </v-app>
</template>
```

Note que `v-main` já "sabe" que existe um `v-app-bar` acima dele e um `v-navigation-drawer` ao lado — o Vuetify calcula o espaçamento automaticamente. Você não precisa (e não deve) definir `margin-top` manualmente para compensar a barra fixa.

### Grid: `v-container` / `v-row` / `v-col`

O Vuetify usa um grid de 12 colunas, parecido com o Bootstrap, mas com props reativas a breakpoints:

```vue
<v-container>
  <v-row>
    <v-col cols="12" sm="6" md="4">
      <!-- ocupa 12/12 no celular, 6/12 em tablet, 4/12 em desktop -->
    </v-col>
  </v-row>
</v-container>
```

Os breakpoints do Vuetify 4 mudaram de valor em relação a versões anteriores — use os números abaixo, não os de tutoriais antigos:

| Breakpoint | Largura mínima |
|---|---|
| `sm` | 600px |
| `md` | 840px |
| `lg` | 1145px |
| `xl` | 1545px |
| `xxl` | 2138px |

Um grid de cards de evento responsivo típico:

```vue
<v-row>
  <v-col v-for="evento in eventos" :key="evento.id" cols="12" sm="6" md="4">
    <!-- v-card do evento -->
  </v-col>
</v-row>
```

Em telas pequenas (`cols="12"`), um card por linha. A partir de 600px, dois por linha (`sm="6"`). A partir de 840px, três por linha (`md="4"`). Essa é a técnica que você vai usar no Mão na massa desta aula.

> **⚠️ Atenção — duas armadilhas comuns do grid no Vuetify 4:**
> 1. `<v-container fill-height>` **não centraliza mais verticalmente** como fazia antes. Se você precisa centralizar conteúdo na tela (por exemplo, uma tela de erro 404), use classes utilitárias: `<v-container class="d-flex align-center justify-center" style="min-height: 100vh">`.
> 2. As props `align`, `justify` e `dense` do `<v-row>` **foram removidas**. No lugar delas, use classes utilitárias de flexbox (`class="justify-space-between"`, `class="align-center"`) ou a prop `density="compact"` para reduzir o espaçamento entre colunas. Código copiado de tutoriais do Vuetify 3 que usa `<v-row align="center">` **vai quebrar silenciosamente** — a prop simplesmente é ignorada.

## 4. Componentes essenciais

Vamos conhecer os componentes que você vai usar em praticamente toda tela do UniEventos.

### `v-card`

O cartão é a unidade básica de conteúdo agrupado — um evento, um resultado de busca, um formulário curto. Ele é composto por subcomponentes:

```vue
<v-card>
  <v-img src="/img/evento.jpg" height="180" cover />
  <v-card-title>Semana Acadêmica de Computação</v-card-title>
  <v-card-subtitle>29/09/2026 · Auditório Central</v-card-subtitle>
  <v-card-text>
    Palestras, minicursos e apresentação de projetos dos estudantes.
  </v-card-text>
  <v-card-actions>
    <v-btn color="primary" variant="text">Ver detalhes</v-btn>
    <v-spacer />
    <v-chip color="success" size="small">32 vagas</v-chip>
  </v-card-actions>
</v-card>
```

`v-card-title`, `v-card-subtitle`, `v-card-text` e `v-card-actions` existem para dar estrutura semântica e espaçamento correto — evite substituí-los por `<div>` com classes manuais.

### `v-btn` e suas variantes

O `v-btn` tem seis variantes visuais (prop `variant`), cada uma com um uso recomendado:

| Variant | Quando usar |
|---|---|
| `elevated` | ação de destaque, com sombra (padrão visual antigo do Material) |
| `flat` | ação primária sem sombra — a mais comum em toolbars |
| `tonal` | ação secundária, fundo suave na cor do tema |
| `outlined` | ação secundária, apenas borda |
| `text` | ação terciária, sem fundo — links de ação dentro de cards |
| `plain` | mínimo destaque visual, quase texto puro |

```vue
<v-btn color="primary" variant="elevated">Inscrever-se</v-btn>
<v-btn color="primary" variant="tonal">Ver mais</v-btn>
<v-btn color="error" variant="outlined">Cancelar inscrição</v-btn>
<v-btn variant="text">Voltar</v-btn>
```

> **⚠️ Atenção:** no Vuetify 4, `v-btn` **não** transforma mais o texto em UPPERCASE automaticamente (era o comportamento padrão em versões antigas do Material Design). Se você escrever `Inscrever-se`, o texto aparece exatamente assim — não `INSCREVER-SE`. Isso é intencional: o MD3 abandonou a caixa alta como padrão de botão.

### `v-chip`, `v-icon`, `v-list`

`v-chip` é uma etiqueta compacta — categoria do evento, status, tag:

```vue
<v-chip color="primary" size="small" prepend-icon="mdi-tag">Minicurso</v-chip>
```

`v-icon` renderiza um ícone MDI (Material Design Icons) — o nome sempre começa com o prefixo `mdi-`:

```vue
<v-icon icon="mdi-calendar" color="primary" />
<v-icon>mdi-map-marker</v-icon>
```

`v-list` organiza itens verticais — menu de navegação, lista de eventos inscritos:

```vue
<v-list>
  <v-list-item
    v-for="evento in eventos"
    :key="evento.id"
    :title="evento.titulo"
    :subtitle="evento.local"
    prepend-icon="mdi-calendar-star"
  />
</v-list>
```

### `v-alert`, `v-dialog`, `v-snackbar`

Três componentes de feedback com propósitos distintos:

- **`v-alert`** — mensagem persistente embutida no fluxo da página (ex.: "nenhum evento encontrado com esse filtro").
- **`v-dialog`** — janela modal que bloqueia a interação até ser fechada (ex.: confirmar exclusão de um evento).
- **`v-snackbar`** — notificação temporária no rodapé da tela, some sozinha (ex.: "inscrição realizada com sucesso").

```vue
<v-alert type="info" variant="tonal" title="Nenhum evento encontrado">
  Tente ajustar os filtros de categoria ou data.
</v-alert>
```

```vue
<script setup>
import { ref } from 'vue'
const mostrarDialogo = ref(false)
</script>

<template>
  <v-btn color="error" @click="mostrarDialogo = true">Excluir</v-btn>

  <v-dialog v-model="mostrarDialogo" max-width="400">
    <v-card title="Confirmar exclusão">
      <v-card-text>Esta ação não pode ser desfeita.</v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn variant="text" @click="mostrarDialogo = false">Cancelar</v-btn>
        <v-btn color="error" variant="flat" @click="mostrarDialogo = false">Excluir</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
```

Repare que `v-dialog` usa `v-model` para controlar se está aberto ou fechado — o mesmo padrão de two-way binding que você já usa em `v-text-field`. Vamos usar `v-snackbar` de verdade na Aula 06, quando tivermos ações assíncronas (salvar, excluir) que precisam de feedback.

### `v-text-field`, `v-select`, `v-img`, `v-progress-circular`

```vue
<v-text-field
  v-model="busca"
  label="Buscar evento"
  prepend-inner-icon="mdi-magnify"
  variant="outlined"
  clearable
/>

<v-select
  v-model="categoriaFiltro"
  :items="['Todas', 'Palestra', 'Minicurso', 'Workshop']"
  label="Categoria"
  variant="outlined"
/>

<v-img src="/img/banner.jpg" height="200" cover />

<v-progress-circular indeterminate color="primary" />
```

`v-progress-circular` com `indeterminate` é o spinner de carregamento — você já usou um estado de "carregando" na Aula 03 com uma condição simples; agora vamos trocar o texto "Carregando..." por esse componente visual.

## 5. Tema: cores institucionais e alternador claro/escuro

Um tema no Vuetify é declarado em `createVuetify`, com um conjunto de cores nomeadas por papel:

```js
// src/main.js (trecho — configuração de tema)
const vuetify = createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        dark: false,
        colors: {
          primary: '#1B5E20',    // verde institucional
          secondary: '#F9A825',  // amarelo de destaque
          error: '#B00020',
          success: '#2E7D32',
          warning: '#F57F17',
          info: '#0277BD',
          background: '#F5F5F5',
          surface: '#FFFFFF',
        },
      },
      dark: {
        dark: true,
        colors: {
          primary: '#66BB6A',
          secondary: '#FFCA28',
          error: '#CF6679',
          success: '#66BB6A',
          warning: '#FFB300',
          info: '#4FC3F7',
          background: '#121212',
          surface: '#1E1E1E',
        },
      },
    },
  },
})
```

Depois de declarado, qualquer componente usa `color="primary"` e recebe automaticamente a cor certa, seja no tema claro ou escuro — você nunca escreve um valor hexadecimal direto no template.

Para alternar entre os temas em tempo de execução, o Vuetify expõe o composable `useTheme()`:

```vue
<!-- src/components/AlternadorTema.vue -->
<script setup>
import { computed } from 'vue'
import { useTheme } from 'vuetify'

const tema = useTheme()

const ehEscuro = computed(() => tema.global.name.value === 'dark')

function alternarTema() {
  tema.global.name.value = ehEscuro.value ? 'light' : 'dark'
}
</script>

<template>
  <v-btn
    :icon="ehEscuro ? 'mdi-weather-sunny' : 'mdi-weather-night'"
    variant="text"
    @click="alternarTema"
  />
</template>
```

`useTheme()` é um composable — mesma ideia dos composables `useRoute()`/`useRouter()` que veremos já já, e dos que você vai escrever na Aula 05. Ele te dá acesso reativo ao estado global de tema: ler `tema.global.name.value` e escrever nele muda o tema da aplicação inteira instantaneamente.

> **💡 Dica:** guarde a preferência de tema do usuário em `localStorage` para que ela persista entre visitas. Vamos formalizar esse padrão de persistência com Pinia na Aula 06 — por hoje, é suficiente saber alternar o tema em memória.

## 6. Classes utilitárias de espaçamento e layout

O Vuetify gera classes utilitárias para espaçamento e flexbox, seguindo a convenção `{propriedade}{direção}-{tamanho}`:

- `pa-4` — padding em todos os lados, tamanho 4 (múltiplo de 4px → 16px)
- `ma-2` — margin em todos os lados, tamanho 2 (8px)
- `mt-4`, `mb-2`, `mx-auto`, `py-6` — direções específicas (t=top, b=bottom, x=horizontal, y=vertical)
- `d-flex` — `display: flex`
- `align-center` — `align-items: center` (funciona em contêiner flex)
- `justify-space-between` — `justify-content: space-between`

```vue
<div class="d-flex align-center justify-space-between pa-4">
  <span class="text-h6">Eventos disponíveis</span>
  <v-btn color="primary" variant="tonal">Novo evento</v-btn>
</div>
```

Essas classes evitam CSS customizado para casos simples de espaçamento e alinhamento — e, por serem previsíveis, tornam o código mais fácil de ler entre desenvolvedores diferentes.

## 7. Vue Router 5: transformando páginas em rotas

Até agora o UniEventos era uma única página com tudo dentro de `App.vue`. Uma aplicação real precisa de **navegação**: uma URL para a lista de eventos, outra para o detalhe de um evento específico, outra para "sobre". Isso é o papel do **Vue Router**.

O UniEventos, se você criou o projeto com `--router` (como recomenda a §4 da especificação), já vem com Vue Router 5.2.0 instalado e configurado. Vamos entender e expandir essa configuração.

### Estrutura básica

```js
// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
  ],
})

export default router
```

- `createRouter` monta a instância do roteador — assim como `createVuetify` e `createPinia`, ela é registrada com `app.use(router)` no `main.js` (isso já vem pronto no scaffold).
- `createWebHistory` usa a API de histórico do navegador (`pushState`) para gerar URLs "limpas" (`/eventos/12`) em vez de usar `#` (hash). Isso exige que o servidor de produção redirecione todas as rotas para `index.html` — trataremos disso na Unidade 3, ao falar de deploy.
- `routes` é um array de objetos `{ path, name, component }`. `name` permite navegar por nome em vez de string de URL, o que evita erros de digitação espalhados pelo código.

### `<RouterLink>` e `<RouterView>`

Dois componentes globais, já registrados automaticamente pelo `app.use(router)`:

```vue
<template>
  <nav>
    <RouterLink to="/">Home</RouterLink>
    <RouterLink :to="{ name: 'sobre' }">Sobre</RouterLink>
  </nav>

  <RouterView />
</template>
```

- `<RouterLink>` renderiza um `<a>` de verdade (importante para acessibilidade e SEO), mas intercepta o clique para trocar de rota sem recarregar a página inteira.
- `<RouterView>` é o "buraco" onde o componente da rota ativa é renderizado. Em `App.vue`, ele normalmente fica dentro de `v-main`.

### Rotas com parâmetros

A tela de detalhe de um evento precisa saber *qual* evento mostrar. Isso é feito com um segmento dinâmico na URL:

```js
// src/router/index.js (trecho)
{
  path: '/eventos/:id',
  name: 'evento-detalhe',
  component: () => import('../views/EventoDetalheView.vue'),
}
```

Dentro do componente, o parâmetro é lido com o composable `useRoute()`:

```vue
<!-- src/views/EventoDetalheView.vue (trecho) -->
<script setup>
import { useRoute } from 'vue-router'

const rota = useRoute()
console.log(rota.params.id) // string com o valor de :id na URL atual
</script>
```

> **⚠️ Atenção:** `rota.params.id` sempre vem como **string**, mesmo que o ID no seu array de dados seja um número. Se você comparar com `===`, compare string com string ou converta com `Number(rota.params.id)`.

### Rota 404 (catch-all)

Toda SPA precisa de uma rota que capture qualquer caminho não mapeado:

```js
// src/router/index.js (trecho — sempre por último no array de routes)
{
  path: '/:pathMatch(.*)*',
  name: 'nao-encontrado',
  component: () => import('../views/NaoEncontradoView.vue'),
}
```

O padrão `/:pathMatch(.*)*` é a sintaxe do Vue Router para "qualquer caminho, com qualquer profundidade de segmentos". Ele precisa ficar **por último** na lista de rotas — o roteador testa as rotas na ordem declarada, e uma rota catch-all no início bloquearia todas as outras.

### Navegação programática

Além de `<RouterLink>`, você pode navegar via código — por exemplo, depois de confirmar uma inscrição:

```js
import { useRouter } from 'vue-router'

const router = useRouter()

function confirmarInscricao() {
  // ... lógica de inscrição
  router.push({ name: 'home' })
}
```

`useRouter()` (com R maiúsculo de Router) dá acesso ao roteador inteiro — inclusive ao método `push`, que navega para uma nova rota, empilhando-a no histórico do navegador (o botão "voltar" funciona). Note a diferença: `useRoute()` (singular, sem "r" no fim de Route) dá acesso somente à **rota atual**; `useRouter()` dá acesso ao **roteador**, que permite navegar.

### Lazy loading de rotas

Repare que, no exemplo de `/eventos/:id` acima, o componente foi importado como `() => import('../views/EventoDetalheView.vue')` em vez de um `import` estático no topo do arquivo. Essa é a técnica de **lazy loading** (carregamento tardio): o Vite gera um arquivo JavaScript separado para essa view, que só é baixado pelo navegador quando o usuário navega até ela.

Em uma aplicação pequena isso não faz diferença perceptível, mas é o padrão recomendado desde já — conforme o UniEventos cresce (área administrativa, formulários, tabelas), o bundle inicial permanece pequeno porque cada view só é carregada quando necessária.

```js
// src/router/index.js — versão completa recomendada, com lazy loading em tudo
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: () => import('../views/HomeView.vue') },
    { path: '/eventos/:id', name: 'evento-detalhe', component: () => import('../views/EventoDetalheView.vue') },
    { path: '/sobre', name: 'sobre', component: () => import('../views/SobreView.vue') },
    { path: '/:pathMatch(.*)*', name: 'nao-encontrado', component: () => import('../views/NaoEncontradoView.vue') },
  ],
})

export default router
```

## 🧩 Padrão de projeto em uso

> ### 🧩 Padrão de projeto em uso — Composite (estrutural)
>
> A árvore de componentes do Vue é um exemplo direto do padrão **Composite**: um componente pode conter outros componentes, que por sua vez podem conter outros, formando uma hierarquia onde o "todo" e a "parte" são tratados de forma uniforme. `v-app` contém `v-app-bar`, `v-main` e `v-navigation-drawer`; `v-main` contém `RouterView`; `RouterView` renderiza uma view, que contém `v-container` > `v-row` > `v-col` > `v-card`. Em cada nível, você trabalha com a mesma interface (props, slots, eventos) sem precisar saber o que está por dentro.
>
> O Vue Router aplica a mesma lógica na dimensão de **navegação**: rotas podem ter rotas-filhas (`children`), formando uma árvore de rotas que espelha uma árvore de `RouterView`s aninhados. Vamos explorar isso a fundo na Aula 05, quando construirmos a área administrativa com rotas aninhadas.

## 💻 Mão na massa — migrando o UniEventos para uma SPA de verdade

Vamos transformar o projeto de página única em uma aplicação navegável com layout persistente, tema institucional e quatro views.

### Passo 1 — instalar o Vuetify no projeto

Se você ainda não instalou (parte da §2 desta aula), rode dentro da pasta do projeto:

```bash
npm install vuetify @mdi/font
npm install -D vite-plugin-vuetify
```

### Passo 2 — configurar `vite.config.js`

```js
// vite.config.js
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'

export default defineConfig({
  plugins: [
    vue({ template: { transformAssetUrls } }),
    vuetify({ autoImport: true }),
  ],
  resolve: {
    alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) },
  },
})
```

### Passo 3 — criar o plugin do Vuetify com tema institucional

```js
// src/plugins/vuetify.js
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'

export default createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        dark: false,
        colors: {
          primary: '#1B5E20',
          secondary: '#F9A825',
          error: '#B00020',
          success: '#2E7D32',
          warning: '#F57F17',
          info: '#0277BD',
          background: '#F5F5F5',
          surface: '#FFFFFF',
        },
      },
      dark: {
        dark: true,
        colors: {
          primary: '#66BB6A',
          secondary: '#FFCA28',
          error: '#CF6679',
          success: '#66BB6A',
          warning: '#FFB300',
          info: '#4FC3F7',
          background: '#121212',
          surface: '#1E1E1E',
        },
      },
    },
  },
})
```

Separar a configuração do Vuetify em `src/plugins/vuetify.js` (em vez de deixar tudo dentro de `main.js`) mantém o ponto de entrada da aplicação enxuto — uma prática que vamos repetir com o Axios na Aula 06.

### Passo 4 — atualizar `src/main.js`

```js
// src/main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(vuetify)

app.mount('#app')
```

### Passo 5 — criar o modelo de dados de eventos

```js
// src/data/eventos.js
export const eventos = [
  { id: 1, titulo: 'Semana Acadêmica de Computação', descricao: 'Palestras e minicursos sobre tendências em tecnologia.', categoria: 'palestra', dataHora: '2026-09-29T19:00:00', local: 'Auditório Central', vagas: 40, imagemUrl: 'https://picsum.photos/seed/evento1/600/300' },
  { id: 2, titulo: 'Minicurso de Vue.js Avançado', descricao: 'Componentização, roteamento e gerenciamento de estado.', categoria: 'minicurso', dataHora: '2026-09-15T18:30:00', local: 'Laboratório 3', vagas: 25, imagemUrl: 'https://picsum.photos/seed/evento2/600/300' },
  { id: 3, titulo: 'Workshop de Prototipação em Figma', descricao: 'Fundamentos de design de interfaces para desenvolvedores.', categoria: 'workshop', dataHora: '2026-09-20T14:00:00', local: 'Sala 12', vagas: 30, imagemUrl: 'https://picsum.photos/seed/evento3/600/300' },
  { id: 4, titulo: 'Palestra: Carreira em Dados', descricao: 'Trilhas profissionais em ciência e engenharia de dados.', categoria: 'palestra', dataHora: '2026-10-02T19:30:00', local: 'Auditório Central', vagas: 50, imagemUrl: 'https://picsum.photos/seed/evento4/600/300' },
  { id: 5, titulo: 'Minicurso de Banco de Dados NoSQL', descricao: 'Modelagem de dados com MongoDB na prática.', categoria: 'minicurso', dataHora: '2026-09-22T18:30:00', local: 'Laboratório 2', vagas: 20, imagemUrl: 'https://picsum.photos/seed/evento5/600/300' },
  { id: 6, titulo: 'Workshop de Testes Automatizados', descricao: 'Testes unitários e de integração em aplicações web.', categoria: 'workshop', dataHora: '2026-10-05T14:00:00', local: 'Sala 12', vagas: 25, imagemUrl: 'https://picsum.photos/seed/evento6/600/300' },
  { id: 7, titulo: 'Palestra: Ética em Inteligência Artificial', descricao: 'Discussão sobre vieses e responsabilidade em sistemas de IA.', categoria: 'palestra', dataHora: '2026-10-10T19:00:00', local: 'Auditório Central', vagas: 60, imagemUrl: 'https://picsum.photos/seed/evento7/600/300' },
  { id: 8, titulo: 'Minicurso de Node.js e Express', descricao: 'Construindo APIs REST do zero.', categoria: 'minicurso', dataHora: '2026-09-25T18:30:00', local: 'Laboratório 1', vagas: 25, imagemUrl: 'https://picsum.photos/seed/evento8/600/300' },
]
```

Estes são os mesmos oito eventos-base que continuam evoluindo a partir de agora até a Unidade 3, quando virão de uma API de verdade.

### Passo 6 — atualizar `src/router/index.js`

```js
// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: () => import('../views/HomeView.vue') },
    { path: '/eventos/:id', name: 'evento-detalhe', component: () => import('../views/EventoDetalheView.vue') },
    { path: '/sobre', name: 'sobre', component: () => import('../views/SobreView.vue') },
    { path: '/:pathMatch(.*)*', name: 'nao-encontrado', component: () => import('../views/NaoEncontradoView.vue') },
  ],
})

export default router
```

### Passo 7 — criar o layout em `App.vue`

```vue
<!-- src/App.vue -->
<script setup>
import { ref, computed } from 'vue'
import { useTheme } from 'vuetify'
import { RouterLink, RouterView } from 'vue-router'

const drawerAberto = ref(false)
const tema = useTheme()
const ehEscuro = computed(() => tema.global.name.value === 'dark')

function alternarTema() {
  tema.global.name.value = ehEscuro.value ? 'light' : 'dark'
}

const linksMenu = [
  { titulo: 'Início', rota: 'home', icone: 'mdi-home' },
  { titulo: 'Sobre', rota: 'sobre', icone: 'mdi-information' },
]
</script>

<template>
  <v-app>
    <v-app-bar color="primary">
      <v-app-bar-nav-icon @click="drawerAberto = !drawerAberto" />
      <v-app-bar-title>
        <RouterLink to="/" class="text-white text-decoration-none">UniEventos</RouterLink>
      </v-app-bar-title>
      <v-spacer />
      <v-btn
        :icon="ehEscuro ? 'mdi-weather-sunny' : 'mdi-weather-night'"
        variant="text"
        @click="alternarTema"
      />
    </v-app-bar>

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

    <v-footer color="primary" class="d-flex justify-center pa-4">
      <span class="text-white">UNEMAT · FACET · FACET-SNP-310 · 2026.2</span>
    </v-footer>
  </v-app>
</template>
```

Repare que `v-list-item` aceita a prop `to`, exatamente como `RouterLink` — internamente, o Vuetify integra os dois. Isso evita ter que envolver cada item de menu em um `<RouterLink>` manualmente.

### Passo 8 — criar `HomeView.vue`

```vue
<!-- src/views/HomeView.vue -->
<script setup>
import { ref, computed, onMounted } from 'vue'
import { eventos } from '../data/eventos'

const carregando = ref(true)
const listaEventos = ref([])
const categoriaFiltro = ref('Todas')
const busca = ref('')

onMounted(() => {
  // simula uma chamada assíncrona, como fizemos na Aula 03 com fetch
  setTimeout(() => {
    listaEventos.value = eventos
    carregando.value = false
  }, 400)
})

const categorias = ['Todas', 'Palestra', 'Minicurso', 'Workshop']

const eventosFiltrados = computed(() => {
  return listaEventos.value.filter((evento) => {
    const bateCategoria =
      categoriaFiltro.value === 'Todas' ||
      evento.categoria === categoriaFiltro.value.toLowerCase()
    const bateBusca = evento.titulo
      .toLowerCase()
      .includes(busca.value.toLowerCase())
    return bateCategoria && bateBusca
  })
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
  <v-container>
    <h1 class="text-h4 mb-4">Eventos disponíveis</h1>

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
          v-model="categoriaFiltro"
          :items="categorias"
          label="Categoria"
          variant="outlined"
          density="compact"
        />
      </v-col>
    </v-row>

    <div v-if="carregando" class="d-flex justify-center pa-8">
      <v-progress-circular indeterminate color="primary" size="48" />
    </div>

    <v-alert
      v-else-if="eventosFiltrados.length === 0"
      type="info"
      variant="tonal"
      title="Nenhum evento encontrado"
    >
      Tente ajustar os filtros de categoria ou o termo de busca.
    </v-alert>

    <v-row v-else>
      <v-col
        v-for="evento in eventosFiltrados"
        :key="evento.id"
        cols="12"
        sm="6"
        md="4"
      >
        <v-card :to="{ name: 'evento-detalhe', params: { id: evento.id } }">
          <v-img :src="evento.imagemUrl" height="160" cover />
          <v-card-title>{{ evento.titulo }}</v-card-title>
          <v-card-subtitle>
            {{ formatarData(evento.dataHora) }} · {{ evento.local }}
          </v-card-subtitle>
          <v-card-actions>
            <v-chip color="secondary" size="small">{{ evento.categoria }}</v-chip>
            <v-spacer />
            <v-chip color="success" size="small">{{ evento.vagas }} vagas</v-chip>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
```

Assim como `v-list-item`, o `v-card` aceita a prop `to` — o card inteiro vira clicável e navega para o detalhe do evento, sem precisar de um `@click` manual com `router.push`.

### Passo 9 — criar `EventoDetalheView.vue`

```vue
<!-- src/views/EventoDetalheView.vue -->
<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { eventos } from '../data/eventos'

const rota = useRoute()
const router = useRouter()

const evento = computed(() =>
  eventos.find((e) => e.id === Number(rota.params.id))
)

function formatarDataHora(dataIso) {
  return new Date(dataIso).toLocaleString('pt-BR', {
    dateStyle: 'long',
    timeStyle: 'short',
  })
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
        <v-btn color="primary" variant="flat">Inscrever-se</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>
```

Note o uso de `Number(rota.params.id)` — como discutido na §7, o parâmetro de rota sempre chega como string, e nossos IDs no array `eventos` são números.

### Passo 10 — criar `SobreView.vue` e `NaoEncontradoView.vue`

```vue
<!-- src/views/SobreView.vue -->
<script setup>
</script>

<template>
  <v-container>
    <v-card class="pa-4">
      <v-card-title class="text-h5">Sobre o UniEventos</v-card-title>
      <v-card-text>
        <p class="mb-2">
          O UniEventos é uma plataforma para divulgação e inscrição em eventos
          acadêmicos — palestras, minicursos e workshops.
        </p>
        <p>
          Projeto desenvolvido na disciplina FACET-SNP-310 — Frameworks Modernos
          para Desenvolvimento de Sistemas, UNEMAT/Sinop, 2026.2.
        </p>
      </v-card-text>
    </v-card>
  </v-container>
</template>
```

```vue
<!-- src/views/NaoEncontradoView.vue -->
<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <v-container class="d-flex flex-column align-center justify-center" style="min-height: 60vh">
    <v-icon icon="mdi-alert-circle-outline" size="80" color="error" class="mb-4" />
    <h1 class="text-h4 mb-2">Página não encontrada</h1>
    <p class="mb-6">O endereço acessado não existe no UniEventos.</p>
    <v-btn color="primary" variant="flat" :to="{ name: 'home' }">Voltar para o início</v-btn>
  </v-container>
</template>
```

Repare que usamos `class="d-flex flex-column align-center justify-center"` em vez de `fill-height` — exatamente o alerta da §6 sobre a mudança de comportamento no Vuetify 4.

### Passo 11 — testar a navegação

```bash
npm run dev
```

Confira: a home lista os eventos com filtro funcionando; clicar em um card navega para o detalhe com a URL `/eventos/3`; o menu lateral abre com o ícone de hambúrguer; o botão de sol/lua alterna o tema; acessar uma URL inexistente (`/qualquer-coisa`) mostra a tela 404.

## 🧪 Laboratório

**1. Chip de vagas esgotadas**
No `HomeView.vue`, altere o chip de vagas para mostrar `"Esgotado"` em vermelho (`color="error"`) quando `evento.vagas === 0`. Adicione um evento de teste com `vagas: 0` no array de dados.

<details markdown="1">
<summary>Dica</summary>

Use um `v-if`/`v-else` dentro do `v-card-actions`, ou um `computed` que retorna a cor e o texto do chip com base em `evento.vagas`.
</details>

**2. Rota `/eventos` (lista) separada da rota `/eventos/:id` (detalhe)**
Hoje a home (`/`) já mostra a lista. Crie também uma rota nomeada `eventos-lista` no caminho `/eventos` que renderiza o mesmo componente que a home usa para a listagem. Use `<RouterLink :to="{ name: 'eventos-lista' }">` em algum lugar do menu.

<details markdown="1">
<summary>Dica</summary>

Você pode apontar duas entradas de `routes` para o mesmo `component`, com `path` e `name` diferentes.
</details>

**3. Contador de eventos no app-bar**
No `App.vue`, mostre no `v-app-bar` (ao lado do título) um `v-chip` com o total de eventos cadastrados. Você vai precisar importar o array `eventos` também no `App.vue`.

<details markdown="1">
<summary>Dica</summary>

`import { eventos } from './data/eventos'` e depois `{{ eventos.length }}` dentro de um `v-chip`.
</details>

**4. Tema alternativo com terceira paleta**
Adicione um terceiro tema chamado `contraste`, com cores de alto contraste (preto/amarelo), e um botão que cicla entre `light` → `dark` → `contraste` → `light`.

<details markdown="1">
<summary>Dica</summary>

`themes: { light: {...}, dark: {...}, contraste: {...} }` no `createVuetify`, e uma função que usa um array `['light', 'dark', 'contraste']` com `indexOf` para descobrir o próximo tema.
</details>

**5. Rota protegida por parâmetro inválido**
No `EventoDetalheView.vue`, se `rota.params.id` não for um número válido (ex.: `/eventos/abc`), redirecione automaticamente para a rota `nao-encontrado` usando `router.push`.

<details markdown="1">
<summary>Dica</summary>

`Number.isNaN(Number(rota.params.id))` dentro de um `onMounted` ou de um `watch` sobre `rota.params.id`.
</details>

## 🐛 Erros comuns e como resolver

| Sintoma | Causa | Solução |
|---|---|---|
| `v-card`, `v-btn` etc. aparecem como tags desconhecidas (sem estilo) | `vuetify({ autoImport: true })` não foi adicionado ao `vite.config.js`, ou o servidor não foi reiniciado após editar a config | Confira o `vite.config.js` e reinicie `npm run dev` |
| Ícones MDI aparecem como quadrado vazio | Faltou importar `@mdi/font/css/materialdesignicons.css` | Adicione o import no arquivo onde `createVuetify` é chamado |
| Tela muda de clara para escura sozinha, sem clique | `defaultTheme` não foi definido — Vuetify 4 usa `'system'` por padrão | Defina `theme: { defaultTheme: 'light' }` explicitamente |
| `v-row align="center"` não centraliza nada | Prop removida no Vuetify 4 | Troque por `class="align-center"` no `v-row`, ou `d-flex align-center` num `<div>` |
| `RouterLink`/`RouterView` não reconhecidos no template | Componente não importado (fora do padrão de autoimport do Vuetify, que não cobre o Vue Router) | Adicione `import { RouterLink, RouterView } from 'vue-router'` no `<script setup>` |
| `rota.params.id` comparado com `===` a um número nunca bate | Parâmetro de rota sempre é string | Converta com `Number(rota.params.id)` antes de comparar |
| Rota 404 nunca é acionada, mesmo em URL inválida | Rota catch-all `/:pathMatch(.*)*` não está por último no array `routes` | Mova a rota catch-all para o final da lista |

## 🏠 Atividade assíncrona (1 h)

No **seu projeto autoral** (definido na Aula 01), aplique exatamente a mesma migração feita hoje no UniEventos:

1. Instale o Vuetify seguindo os passos da §2.
2. Crie um layout com `v-app-bar`, `v-navigation-drawer` (ou menu simples) e `v-main`.
3. Configure um tema com pelo menos `primary` e `secondary` customizados, coerente com o domínio do seu projeto.
4. Crie pelo menos três rotas: uma lista, um detalhe com parâmetro (`/:id`) e uma rota 404.
5. Migre seus dados (mínimo 8 registros, já existentes desde a Aula 01/02) para os cards em grid responsivo.

**Critério de pronto:** `npm run dev` roda sem erros no console; navegar entre as três rotas funciona; o card de detalhe mostra os dados corretos ao clicar em um item da lista; acessar uma URL inexistente mostra a tela 404. Suba o commit no repositório do projeto autoral.

## ✅ Checkpoint do projeto autoral

Ao final desta aula, seu repositório deve ter:

- [ ] Vuetify 4 instalado e funcionando (`v-card`, `v-btn` renderizando estilizados).
- [ ] Tema customizado com `defaultTheme: 'light'` declarado explicitamente.
- [ ] Layout com `v-app-bar` + `v-main` (e `v-navigation-drawer` se aplicável).
- [ ] Vue Router configurado com no mínimo: rota de lista, rota de detalhe com parâmetro `:id`, rota 404.
- [ ] Navegação funcionando via `<RouterLink>` e/ou `:to` em `v-card`/`v-list-item`.
- [ ] Dados de pelo menos 8 registros do domínio autoral, exibidos em grid responsivo (`v-row`/`v-col` com breakpoints).
- [ ] README atualizado com instruções de instalação e execução (`npm install`, `npm run dev`).
- [ ] Código versionado e enviado ao repositório GitHub público.

## 📝 Avaliação 1 — instruções de entrega

### Escopo

A Avaliação 1 cobre a **Unidade 1** inteira: estrutura de um projeto Vue 3 criado com CLI, componentes, diretivas, reatividade, ciclo de vida e — a partir de hoje — Vuetify e Vue Router básico. Você vai entregar o **projeto autoral** que vem evoluindo desde a Aula 01.

O projeto deve:

- Ter sido criado com `npm create vue@latest` (ou `npx create-vue@latest`), com as flags `--router` no mínimo.
- Ser uma SPA de página única transformada em múltiplas views navegáveis (o que fizemos hoje).
- Usar **Vuetify** para toda a interface visual (não é permitido CSS puro substituindo os componentes do Vuetify nas telas principais).
- Ter um domínio de dados **diferente** do UniEventos construído em sala (ex.: catálogo de plantas do Pantanal, agenda de quadras esportivas, mural de estágios, brechó, controle de pescarias, cardápio de restaurante — ou outro tema aprovado na Aula 01).

### Requisitos obrigatórios

1. **Mínimo de 6 componentes `.vue`** próprios (views + componentes reutilizáveis), além do `App.vue`.
2. **Uso comprovado** — em código, não só em teoria — de: `v-if`/`v-else`, `v-for` com `:key`, `v-model`, `v-bind` (ou o atalho `:`), `v-on` (ou o atalho `@`), `computed` e `onMounted`.
3. **Dados de pelo menos 8 registros** do domínio escolhido, em um arquivo separado (`src/data/*.js`) ou vindos de `fetch` a uma API pública/mock.
4. **Roteamento** com Vue Router: no mínimo 3 rotas, sendo uma delas com parâmetro dinâmico e uma delas a rota 404.
5. **README.md** no repositório, com: nome do projeto, descrição de uma linha, instruções de instalação (`npm install`) e execução (`npm run dev`), e print de tela (opcional, mas recomendado).
6. **Repositório GitHub público**, com histórico de commits que mostre evolução incremental (não um único commit "projeto final").

### Formato e prazo de entrega

Entregue **o link do repositório GitHub público** via SIGAA, na atividade "Avaliação 1", até **02/09/2026, 23h59**. Cole o link diretamente no campo de texto da atividade — não anexe `.zip`.

### Rubrica (10,0 pontos)

| Critério | Peso |
|---|---|
| Estrutura e organização do projeto (pastas, nomes, componentização mínima) | 2,0 |
| Uso correto de diretivas e reatividade (`v-if`, `v-for`, `v-model`, `v-bind`, `v-on`) | 3,0 |
| Uso de `computed` e ciclo de vida (`onMounted`) de forma coerente com o domínio | 2,0 |
| Interface visual com Vuetify e navegação com Vue Router funcionando | 1,5 |
| README, versionamento e histórico de commits | 1,5 |

### Política de atraso

Entregas após 02/09/2026 23h59 perdem **1,0 ponto por dia corrido** de atraso, até o limite de 5 dias. Após esse prazo, a atividade recebe nota zero, salvo justificativa formal protocolada junto à coordenação do curso.

### Política de plágio e uso de IA

É permitido usar ferramentas de IA como apoio (explicar erros, sugerir sintaxe, revisar código) — assim como é permitido consultar documentação e tutoriais. **Não é permitido** entregar um projeto gerado quase integralmente por IA sem compreensão do próprio código: na correção, qualquer estudante pode ser chamado para explicar oralmente uma parte do seu projeto, e a nota é ajustada conforme a clareza da explicação. Cópia integral do projeto de outro colega (mesmo com o domínio "trocado") é considerada plágio e resulta em nota zero para ambos os envolvidos, com encaminhamento ao regimento acadêmico da UNEMAT.

## 📚 Para aprofundar

- Documentação oficial do Vuetify 4: <https://vuetifyjs.com/>
- Guia de instalação com Vite: <https://vuetifyjs.com/en/getting-started/installation/>
- Material Design 3 — cores e temas: <https://m3.material.io/styles/color/overview>
- Vue Router — guia oficial: <https://router.vuejs.org/>
- Vue Router — rotas dinâmicas e parâmetros: <https://router.vuejs.org/guide/essentials/dynamic-matching.html>
- Referências básicas do plano de curso: capítulos sobre componentização e roteamento client-side.

Na Aula 05 vamos aprofundar componentização — `defineProps`, `defineEmits`, slots, composables — e o Vue Router avançado: rotas aninhadas, guards de navegação e query strings sincronizadas com filtros. É também quando o Vuetify ganha formulários com validação e `v-data-table`.
