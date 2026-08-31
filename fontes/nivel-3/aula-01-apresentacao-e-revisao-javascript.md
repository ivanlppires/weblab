# Aula 01 — Apresentação da trilha e revisão de JavaScript

> **Nível 3 — Frameworks Modernos** · Unidade 1: Fundamentos de front-end com Vue.js
> WebLab · UNEMAT — Campus Sinop
> **Tempo estimado:** 3 blocos de 50 min + 1 h de prática

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Descrever a estrutura da trilha: unidades e os marcos do projeto autoral.
- Configurar o ambiente de desenvolvimento (Node.js 22 LTS, VS Code, Git) e validar a instalação.
- Explicar por que frameworks front-end existem, comparando manipulação manual do DOM com um paradigma declarativo.
- Escrever e ler código JavaScript moderno (ES2015+): `let`/`const`, arrow functions, desestruturação, spread/rest, template literals, optional chaining e nullish coalescing.
- Transformar coleções de dados com `map`, `filter`, `reduce`, `find`, `some`, `every` e `sort` sem mutar o array original.
- Organizar código em módulos ES (`import`/`export`) e em classes.
- Consumir uma API pública com `fetch` usando `async/await` e tratamento de erro com `try/catch`.
- Definir o tema do seu projeto autoral e modelar as entidades iniciais em um `README.md`.

## 📋 Pré-requisitos desta aula

Esta é a primeira aula — não há pré-requisito de conteúdo desta trilha. Você precisa apenas de:

- Um notebook capaz de rodar Node.js 22 e o VS Code (Windows, Linux ou macOS).
- Conta no [GitHub](https://github.com) criada antes da aula.
- Conhecimento prévio de lógica de programação e alguma exposição a HTML/CSS/JS (pré-requisito formal: FACET-SNP-307).

> **⚠️ Atenção**
> Se você nunca escreveu uma linha de JavaScript, não entre em pânico — a Seção 3 desta aula é uma revisão completa. Mas reserve um tempo extra para os laboratórios em casa.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Apresentação da trilha, unidades, marcos do projeto autoral, instalação do ambiente |
| 2 | 50 min | Por que frameworks existem: DOM manual vs. paradigma declarativo |
| 3 | 50 min | Revisão de JavaScript moderno (ES2015+) com foco no domínio de dados da trilha |

## 1. Apresentação da trilha

### 1.1 O que é esta trilha

Esta trilha nasceu da disciplina **FACET-SNP-310 — Frameworks Modernos para Desenvolvimento de Sistemas** (FACET/UNEMAT — Campus Sinop) e é publicada aberta: são 15 aulas de cerca de 150 minutos cada, mais uma hora de prática por aula. Quem cursa a disciplina acompanha o calendário da turma; quem estuda por conta própria avança no ritmo que conseguir sustentar — a ordem das aulas é a mesma nos dois casos, porque cada uma depende da anterior. Quem escreveu e revisou cada parte está na página [Autoria e créditos](../autores/).

O que esta trilha cobre:

> "Desenvolvimento com uso de frameworks; padrões: criacionais, estruturais e comportamentais; aplicação conjunta das abordagens de frameworks e componentes no desenvolvimento de software."

Isso significa duas coisas na prática: (1) você vai aprender a construir aplicações reais com um framework front-end moderno e depois integrá-las a um back-end; (2) ao longo do caminho, vamos identificar **padrões de projeto clássicos (GoF)** escondidos dentro das ferramentas que usamos — Vue, Vuetify, Pinia, Express — porque isso é um compromisso central desta trilha, e porque entender o padrão por trás da ferramenta é o que separa quem usa framework de quem entende framework.

### 1.2 As três unidades

| Unidade | Conteúdo | Aulas |
|---|---|---|
| U1 | Fundamentos de front-end com Vue.js | 01–04 |
| U2 | Vue.js avançado: Vuetify, Axios, Vue Router, Pinia | 05–06 |
| U3 | Integração front-end/back-end: Firebase, Supabase, Express, autenticação, banco de dados, deploy | 07–15 |

### 1.3 A sequência das aulas

| # | Unidade | Tema |
|---|---|---|
| 01 | U1 | Apresentação da trilha e revisão de JavaScript |
| 02 | U1 | Introdução ao Vue: lifecycle, instância, data e methods, diretivas básicas |
| 03 | U1 | Vue: v-if, v-else, v-for, computed e onMounted |
| 04 | U1 | Introdução a Vuetify e Vue Router — **Marco 1 do projeto** |
| 05 | U2 | Componentes, Vue Router e Vuetify |
| 06 | U2 | Axios e Pinia |
| 07 | U3 | Firebase, Node.js e Express |
| 08 | U3 | Endpoints e middlewares — **Marco 2 do projeto** |
| 09 | U3 | Integração com MySQL |
| 10 | U3 | Requisições autenticadas com Firebase |
| 11 | U3 | CRUD front-end + back-end |
| 12 | U3 | CRUD com banco de dados em nuvem (Supabase) |
| 13 | U3 | Desenvolvimento do back-end em camadas |
| 14 | U3 | Documentação com Swagger |
| 15 | U3 | Apresentação dos resultados — **Marco 3 do projeto** |

O conteúdo abaixo é o mesmo, esteja você seguindo o calendário de uma turma ou estudando por conta própria, em qualquer época — as datas de uma oferta específica, quando existem, ficam de fora deste texto.

Todas as aulas 01 a 15 constroem, passo a passo, uma aplicação de referência chamada **UniEventos** — uma plataforma de divulgação e inscrição em eventos acadêmicos. Você vai acompanhar essa construção junto com o material, mas seu **projeto autoral** (o que evolui até cada marco) terá a mesma arquitetura aplicada a um domínio diferente, escolhido por você. Falamos disso na Seção 1.6.

### 1.4 Marcos do projeto

Esta trilha está dividida em três marcos, um ao final de cada unidade. Cada marco é um estado que o seu projeto autoral precisa alcançar — não uma prova separada — e mostra que você domina o conteúdo daquela unidade.

| Marco | Escopo |
|---|---|
| Marco 1 | Vue 3 com CLI: estrutura de projeto, componentes, diretivas |
| Marco 2 | Vue avançado: Vuetify + Axios + Vue Router + Pinia |
| Marco 3 | Back-end: Firebase/Express/Supabase, banco de dados, autenticação |

Os requisitos completos de cada marco — o que precisa estar pronto e como conferir — são detalhados na aula que fecha a unidade correspondente: o Marco 1 na Aula 04, o Marco 2 na Aula 08, o Marco 3 na Aula 15. Se você está seguindo esta trilha em uma disciplina com professor, é dele que vêm os prazos e a forma de acompanhamento de cada marco; se está estudando por conta própria, use os marcos como metas de progresso no seu próprio ritmo.

### 1.5 Comunicação

Canais de acompanhamento:

- **E-mail** — dúvidas pontuais sobre o conteúdo.
- **GitHub** — mantenha um repositório público do projeto autoral; é ali que o progresso fica visível ao longo do tempo, para você mesmo, para outra pessoa que revise seu código, ou para quem eventualmente lhe orienta (um professor, um mentor, um colega mais experiente).

Se você está cursando esta trilha como disciplina em uma instituição, ela também é quem fornece os avisos, prazos e canais complementares próprios daquela oferta.

> **💡 Dica**
> Comite no seu repositório do projeto autoral **toda semana**, mesmo que pouco. Um histórico de commits ao longo do tempo mostra evolução de verdade — vale muito mais do que um único commit gigante na véspera de um marco.

### 1.6 O projeto autoral

Escolha, logo no início desta trilha, um **domínio de aplicação diferente** do UniEventos (o projeto que construiremos ao longo do material), mas siga exatamente a mesma arquitetura técnica: Vue 3 → Vuetify + Vue Router → Axios + Pinia → back-end Express → banco de dados → autenticação → deploy.

Exemplos de temas válidos:

- Catálogo de plantas do Pantanal, com filtro por bioma e época de floração.
- Agenda de quadras esportivas do bairro, com reserva de horário.
- Mural de estágios e vagas para estudantes da FACET.
- Brechó colaborativo, com peças, categorias e reserva.
- Controle de pescarias, com espécies, rio e datas.
- Cardápio digital de um restaurante, com categorias de prato e pedidos.

Regras para o tema:

1. **Precisa ter pelo menos duas entidades relacionadas** (ex.: "Evento" e "Inscrição", "Quadra" e "Reserva") — um cadastro único sem relacionamento não sustenta as três unidades.
2. **Precisa ter uma tela de listagem com filtro**, uma tela de detalhe e uma área que exija autenticação — isso espelha as telas do UniEventos (Home, Detalhe, Minhas inscrições, Login, Área administrativa).
3. **Não pode ser o próprio UniEventos** copiado — o domínio precisa ser outro.

### 1.7 Ambiente de desenvolvimento

Vamos instalar, nesta aula, tudo que será usado até o fim da trilha. As versões abaixo foram testadas no ambiente real desta trilha — use exatamente estas.

| Ferramenta | Versão usada nesta trilha |
|---|---|
| Node.js | 22.22.2 LTS |
| npm | 10.9.7 (vem com o Node) |
| VS Code | versão estável mais recente |
| Git | versão estável mais recente |

**Passo a passo:**

1. **Node.js 22 LTS.** Baixe em [nodejs.org](https://nodejs.org) a versão "LTS" (não a "Current"). No Linux, você também pode usar o gerenciador de versões `nvm`:

```bash
# instalar nvm (se ainda não tiver)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash

# instalar e usar o Node 22 LTS
nvm install 22
nvm use 22
```

2. **Verifique a instalação:**

```bash
node -v
# esperado: v22.22.2 (ou outra 22.x LTS)

npm -v
# esperado: 10.9.7 (ou próxima)
```

> **⚠️ Atenção**
> Se `node -v` mostrar uma versão 16, 18 ou 20, desinstale-a ou troque com o `nvm` antes de continuar. Ferramentas que usaremos mais à frente, como o `create-vue`, exigem Node `^22.18.0` ou `>=24.12.0` — versões antigas simplesmente falham na instalação.

3. **VS Code.** Baixe em [code.visualstudio.com](https://code.visualstudio.com). Instale estas extensões (aba Extensions, `Ctrl+Shift+X`):

   - **Vue - Official** (antigo Volar) — suporte a arquivos `.vue`, autocomplete, checagem de tipos no template.
   - **ESLint** — aponta erros e más práticas enquanto você digita.
   - **Prettier - Code formatter** — formatação automática e consistente.

4. **Navegador com DevTools.** Use Chrome, Edge ou Firefox — qualquer um com um bom painel de DevTools (`F12`). Vamos usar a aba **Elements** (inspecionar DOM), **Console** e **Network** (ver requisições) do início ao fim da trilha.

5. **Git e GitHub.**

```bash
git --version
# se não tiver, instale: sudo apt install git (Linux) ou baixe em git-scm.com

git config --global user.name "Seu Nome"
git config --global user.email "seu-email@exemplo.com"
```

Crie uma conta em [github.com](https://github.com) se ainda não tiver. Vamos usar o GitHub para hospedar o código do projeto autoral e, mais adiante nesta trilha, para o deploy.

> **💡 Dica**
> Depois de instalar tudo, rode `node -v`, `npm -v` e `git --version` e tire um print. Cole no seu README como evidência de ambiente pronto — é o primeiro item do checkpoint desta aula.

## 2. Por que frameworks existem

### 2.1 Um problema concreto: lista de eventos com filtro

Imagine que você precisa mostrar uma lista de eventos acadêmicos na tela, com um campo de busca por texto e um filtro por categoria. Sem framework nenhum, em JavaScript puro manipulando o DOM diretamente, o código fica assim:

```html
<!-- index.html -->
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <title>Eventos — DOM manual</title>
</head>
<body>
  <input id="busca" type="text" placeholder="Buscar evento..." />
  <select id="categoria">
    <option value="">Todas as categorias</option>
    <option value="palestra">Palestra</option>
    <option value="minicurso">Minicurso</option>
    <option value="workshop">Workshop</option>
  </select>

  <ul id="lista-eventos"></ul>

  <script src="app-dom-manual.js"></script>
</body>
</html>
```

```js
// app-dom-manual.js
const eventos = [
  { id: 1, titulo: 'Semana da Computação', categoria: 'palestra', vagas: 40 },
  { id: 2, titulo: 'Oficina de Vue.js', categoria: 'minicurso', vagas: 25 },
  { id: 3, titulo: 'Hackathon FACET', categoria: 'workshop', vagas: 60 },
  { id: 4, titulo: 'Introdução a IA', categoria: 'palestra', vagas: 80 },
]

const inputBusca = document.getElementById('busca')
const selectCategoria = document.getElementById('categoria')
const listaEl = document.getElementById('lista-eventos')

// Função que decide QUAIS eventos mostrar e depois
// PRECISA, na mão, apagar o DOM antigo e reconstruir tudo.
function renderizar() {
  const termo = inputBusca.value.toLowerCase()
  const categoria = selectCategoria.value

  const filtrados = eventos.filter((evento) => {
    const bateTexto = evento.titulo.toLowerCase().includes(termo)
    const bateCategoria = categoria === '' || evento.categoria === categoria
    return bateTexto && bateCategoria
  })

  // Passo manual 1: limpar o que já estava na tela.
  listaEl.innerHTML = ''

  // Passo manual 2: recriar cada item, um por um.
  if (filtrados.length === 0) {
    const li = document.createElement('li')
    li.textContent = 'Nenhum evento encontrado.'
    listaEl.appendChild(li)
    return
  }

  filtrados.forEach((evento) => {
    const li = document.createElement('li')
    li.textContent = `${evento.titulo} (${evento.categoria}) — ${evento.vagas} vagas`
    listaEl.appendChild(li)
  })
}

// Passo manual 3: escutar cada evento de interação e chamar renderizar() de novo.
inputBusca.addEventListener('input', renderizar)
selectCategoria.addEventListener('change', renderizar)

renderizar()
```

Funciona. Mas repare no que **você**, programador, teve que fazer manualmente:

1. Escutar cada evento de UI (`input`, `change`) e lembrar de chamar `renderizar()`.
2. Dentro de `renderizar()`, apagar o HTML antigo (`innerHTML = ''`) e reconstruir do zero.
3. Manter sincronizado, na sua cabeça, o **estado** (`eventos`, o termo de busca, a categoria) com o que está na tela.

Em uma lista de 4 eventos isso é trivial. Em uma aplicação real — com dezenas de componentes, cada um reagindo a mudanças de estado de outros — esse sincronismo manual vira a maior fonte de bugs: tela desatualizada, elementos duplicados, listeners que vazam memória.

### 2.2 A mesma ideia, em paradigma declarativo

Compare com o que faremos a partir da Aula 02, em Vue:

```vue
<!-- Antecipação — ainda NÃO é o que vamos escrever hoje, é só para criar contraste -->
<template>
  <input v-model="busca" type="text" placeholder="Buscar evento..." />
  <select v-model="categoria">
    <option value="">Todas as categorias</option>
    <option value="palestra">Palestra</option>
    <option value="minicurso">Minicurso</option>
    <option value="workshop">Workshop</option>
  </select>

  <ul>
    <li v-for="evento in eventosFiltrados" :key="evento.id">
      {{ evento.titulo }} ({{ evento.categoria }}) — {{ evento.vagas }} vagas
    </li>
    <li v-if="eventosFiltrados.length === 0">Nenhum evento encontrado.</li>
  </ul>
</template>
```

Note a diferença de raciocínio: no código Vue você **descreve o resultado desejado** ("a lista deve mostrar `eventosFiltrados`") e o framework decide, sozinho, quando e como atualizar o DOM. Você não escreve `innerHTML = ''`, não escreve `addEventListener`, não gerencia manualmente qual elemento criar ou remover. Isso é **programação declarativa**: você declara o "o quê", o framework resolve o "como".

Essa é a promessa central de um framework front-end reativo como o Vue — e é o fio condutor de toda esta trilha. Ainda não vamos escrever Vue hoje (isso começa na Aula 02); hoje construímos a base de JavaScript que sustenta tudo isso.

### 2.3 Conceitos que você vai ouvir o tempo todo

- **SPA (Single Page Application) vs. MPA (Multi Page Application).** Uma MPA tradicional recarrega o HTML inteiro do servidor a cada navegação. Uma SPA carrega um único HTML inicial e, depois, troca apenas os pedaços de tela necessários via JavaScript — é o modelo que o Vue Router (Aula 04) implementa.
- **Client-side rendering (CSR).** O HTML final da página é montado no navegador do usuário, em JavaScript, a partir de dados — em vez de vir pronto do servidor. É o padrão que usaremos com Vue + Vite.
- **Bundler.** Ferramenta que pega seus arquivos-fonte (`.vue`, `.js`, `.css`, módulos separados) e os empacota em arquivos otimizados para o navegador. Usaremos o **Vite** a partir da Aula 02.
- **Transpilação.** Processo de converter uma sintaxe moderna (ES2022+, ou até TypeScript) em um JavaScript que rode em navegadores mais antigos ou que corresponda ao que o navegador entende nativamente. O Vite faz isso por baixo dos panos.
- **npm e `package.json`.** O `npm` (Node Package Manager) instala bibliotecas de terceiros. O `package.json` é o arquivo que lista essas dependências e os scripts do projeto (`npm run dev`, por exemplo).
- **SemVer (versionamento semântico).** Versões no formato `MAIOR.MENOR.PATCH` (ex.: `3.5.41`). Mudanças de `MAIOR` podem quebrar compatibilidade; `MENOR` adiciona funcionalidade sem quebrar; `PATCH` corrige bugs. É por isso que, nesta trilha, **fixamos versões exatas** — evita que seu projeto quebre por uma atualização automática inesperada.

## 3. Revisão de JavaScript moderno (ES2015+)

Esta é a espinha dorsal da aula de hoje. O Vue é, por baixo, "só" JavaScript — cada recurso que revisamos aqui reaparece dentro de um `<script setup>` já na próxima aula.

> **🧠 Você sabia?**
> O JavaScript foi criado por Brendan Eich em **10 dias**, em maio de 1995, para a Netscape — daí virem tantas decisões de design "estranhas" que a linguagem carrega até hoje, como o `==` fazer coerção de tipo. O nome "JavaScript" foi uma decisão de marketing da Netscape para surfar na popularidade do Java, sem relação técnica real entre as duas linguagens; a especificação oficial se chama **ECMAScript**, e é por isso que falamos em "ES2015", "ES2020" — cada ano, uma revisão da especificação.

### 3.1 `let`, `const` e escopo de bloco

```js
// Antes do ES2015 só existia `var`, com escopo de função (confuso).
// Hoje: use `const` por padrão, `let` só quando o valor precisa mudar.

const nomeEvento = 'Semana da Computação' // não pode ser reatribuída
let vagasDisponiveis = 40                 // pode ser reatribuída

vagasDisponiveis = vagasDisponiveis - 1
console.log(vagasDisponiveis) // 39

// `let` e `const` respeitam escopo de bloco { }
if (vagasDisponiveis > 0) {
  const mensagem = 'ainda há vagas'
  console.log(mensagem)
}
// console.log(mensagem) aqui daria ReferenceError: mensagem não existe fora do bloco
```

> **⚠️ Atenção**
> Nunca use `var` em código novo. `var` "vaza" para fora de blocos `if`/`for`, o que gera bugs difíceis de rastrear. Esta trilha inteira usa apenas `let` e `const`.

### 3.2 Template literals

```js
const evento = { titulo: 'Oficina de Vue.js', vagas: 25 }

// Antes: concatenação com +
const antigo = 'Evento: ' + evento.titulo + ' (' + evento.vagas + ' vagas)'

// Agora: template literal, com crase e ${}
const moderno = `Evento: ${evento.titulo} (${evento.vagas} vagas)`

// Suporta múltiplas linhas sem precisar de \n
const bloco = `
  Título: ${evento.titulo}
  Vagas: ${evento.vagas}
`
console.log(moderno)
```

### 3.3 Arrow functions e `this`

```js
// Função tradicional
function dobrar(numero) {
  return numero * 2
}

// Arrow function equivalente
const dobrarArrow = (numero) => numero * 2

// Com múltiplos parâmetros e corpo de bloco
const somarVagas = (a, b) => {
  const total = a + b
  return total
}

// Sem parâmetros, precisa dos parênteses vazios
const gerarId = () => Math.floor(Math.random() * 1000)
```

A diferença mais importante não é a sintaxe curta — é o comportamento do `this`.

```js
const contador = {
  vagas: 10,
  // `function` tradicional: `this` é o objeto que CHAMA o método (contador).
  reduzirComFunction: function () {
    setTimeout(function () {
      // aqui `this` NÃO é mais `contador` — em modo estrito, é `undefined`.
      console.log(this?.vagas) // undefined
    }, 100)
  },
  // arrow function: `this` é herdado do escopo onde a arrow foi DEFINIDA.
  reduzirComArrow: function () {
    setTimeout(() => {
      // aqui `this` continua sendo `contador`, porque a arrow "pega emprestado"
      // o `this` do método externo.
      console.log(this.vagas) // 10
    }, 100)
  },
}

contador.reduzirComFunction()
contador.reduzirComArrow()
```

> **🔎 Por baixo do capô**
> Arrow functions não têm seu próprio `this` — em vez de criar um novo, elas capturam o `this` do escopo léxico onde foram escritas. É exatamente por isso que, dentro de um `<script setup>` do Vue (Aula 02), quase sempre usamos arrow functions ou funções normais no nível do módulo: o comportamento de `this` deixa de ser um problema porque a Composition API não depende dele.

### 3.4 Desestruturação de objetos e arrays

```js
const evento = {
  id: 2,
  titulo: 'Oficina de Vue.js',
  categoria: 'minicurso',
  vagas: 25,
  local: 'Bloco B, sala 12',
}

// Desestruturação de objeto: extrai propriedades para variáveis
const { titulo, vagas } = evento
console.log(titulo, vagas) // Oficina de Vue.js 25

// Renomear ao desestruturar
const { titulo: nomeDoEvento } = evento
console.log(nomeDoEvento) // Oficina de Vue.js

// Valor default se a propriedade não existir
const { imagemUrl = '/img/padrao.png' } = evento
console.log(imagemUrl) // /img/padrao.png

// Desestruturação de array: extrai por posição
const coordenadas = [-16.0736, -57.6789]
const [latitude, longitude] = coordenadas
console.log(latitude, longitude) // -16.0736 -57.6789

// Desestruturação em parâmetros de função — muito comum no Vue com props
function exibirEvento({ titulo, vagas }) {
  return `${titulo}: ${vagas} vagas`
}
console.log(exibirEvento(evento)) // Oficina de Vue.js: 25 vagas
```

### 3.5 Spread e rest

```js
// Spread (...) em array: "espalha" os elementos
const categoriasBase = ['palestra', 'minicurso']
const todasCategorias = [...categoriasBase, 'workshop']
console.log(todasCategorias) // ['palestra', 'minicurso', 'workshop']

// Spread em objeto: cria uma CÓPIA com propriedades sobrescritas
// (importante: nunca mutar o objeto original em Vue)
const eventoOriginal = { id: 1, titulo: 'Semana da Computação', vagas: 40 }
const eventoAtualizado = { ...eventoOriginal, vagas: 39 }
console.log(eventoOriginal.vagas)   // 40 — original intocado
console.log(eventoAtualizado.vagas) // 39 — cópia com a mudança

// Rest (...) em parâmetros: agrupa "o resto" dos argumentos em array
function somarTodasAsVagas(...quantidades) {
  return quantidades.reduce((total, atual) => total + atual, 0)
}
console.log(somarTodasAsVagas(10, 20, 30)) // 60

// Rest em desestruturação: agrupa "o resto" das propriedades
const { id, ...detalhesDoEvento } = eventoOriginal
console.log(id)              // 1
console.log(detalhesDoEvento) // { titulo: 'Semana da Computação', vagas: 40 }
```

### 3.6 Parâmetros default

```js
function criarEvento(titulo, categoria = 'palestra', vagas = 30) {
  return { titulo, categoria, vagas }
}

console.log(criarEvento('Minicurso de Git'))
// { titulo: 'Minicurso de Git', categoria: 'palestra', vagas: 30 }

console.log(criarEvento('Workshop de Testes', 'workshop', 15))
// { titulo: 'Workshop de Testes', categoria: 'workshop', vagas: 15 }
```

### 3.7 Optional chaining (`?.`) e nullish coalescing (`??`)

```js
const evento = {
  titulo: 'Semana da Computação',
  local: {
    predio: 'Bloco A',
    // sala não foi informada
  },
}

// Sem optional chaining, acessar uma propriedade aninhada ausente quebra:
// console.log(evento.organizador.nome) // TypeError: Cannot read properties of undefined

// Com optional chaining: retorna `undefined` em vez de lançar erro
console.log(evento.organizador?.nome) // undefined
console.log(evento.local?.sala)       // undefined
console.log(evento.local?.predio)     // Bloco A

// Funciona também para chamar métodos que podem não existir
const relatorio = null
console.log(relatorio?.gerar?.()) // undefined, sem quebrar

// Nullish coalescing (??): fornece um valor padrão SOMENTE quando o
// valor à esquerda é null ou undefined (diferente do || , que também
// cai no padrão para 0, '' ou false — o que costuma ser um bug).
const vagasInformadas = 0
console.log(vagasInformadas || 10) // 10 — ERRADO: 0 é um valor válido de vagas!
console.log(vagasInformadas ?? 10) // 0  — CORRETO: só usa o padrão se for null/undefined

const sala = evento.local?.sala ?? 'a definir'
console.log(sala) // a definir
```

> **⚠️ Atenção**
> `||` e `??` parecem intercambiáveis, mas não são. Use `??` sempre que `0`, `''` ou `false` forem valores legítimos que você não quer substituir pelo padrão. É um erro comum em formulários (campo numérico zerado sendo tratado como "vazio").

### 3.8 Métodos de array: `map`, `filter`, `reduce`, `find`, `some`, `every`, `sort`

Vamos usar o mesmo array de eventos em todos os exemplos — é o dado que sustentará o UniEventos a partir da Aula 02.

```js
const eventos = [
  { id: 1, titulo: 'Semana da Computação', categoria: 'palestra', dataHora: '2030-09-10T19:00:00', vagas: 40, inscritos: 12 },
  { id: 2, titulo: 'Oficina de Vue.js', categoria: 'minicurso', dataHora: '2030-08-20T14:00:00', vagas: 25, inscritos: 25 },
  { id: 3, titulo: 'Hackathon FACET', categoria: 'workshop', dataHora: '2030-10-05T08:00:00', vagas: 60, inscritos: 18 },
  { id: 4, titulo: 'Introdução a IA', categoria: 'palestra', dataHora: '2030-08-18T19:30:00', vagas: 80, inscritos: 55 },
]
```

**`map` — transforma cada item em outra coisa, sem mudar o tamanho do array:**

```js
const titulos = eventos.map((evento) => evento.titulo)
console.log(titulos)
// ['Semana da Computação', 'Oficina de Vue.js', 'Hackathon FACET', 'Introdução a IA']

// map devolvendo objetos NOVOS (sem mutar os originais) — padrão que
// vamos repetir sempre que precisarmos "decorar" dados para a tela
const eventosComVagasRestantes = eventos.map((evento) => ({
  ...evento,
  vagasRestantes: evento.vagas - evento.inscritos,
}))
console.log(eventosComVagasRestantes[0].vagasRestantes) // 28
```

**`filter` — seleciona um subconjunto:**

```js
const palestras = eventos.filter((evento) => evento.categoria === 'palestra')
console.log(palestras.length) // 2

const comVagas = eventos.filter((evento) => evento.inscritos < evento.vagas)
console.log(comVagas.map((e) => e.titulo)) // exclui a "Oficina de Vue.js" (lotada)
```

**`reduce` — acumula os itens em um único valor:**

```js
const totalDeVagas = eventos.reduce((acumulado, evento) => acumulado + evento.vagas, 0)
console.log(totalDeVagas) // 205

// reduce também serve para agrupar por categoria
const porCategoria = eventos.reduce((grupos, evento) => {
  const chave = evento.categoria
  if (!grupos[chave]) {
    grupos[chave] = []
  }
  grupos[chave].push(evento)
  return grupos
}, {})
console.log(Object.keys(porCategoria)) // ['palestra', 'minicurso', 'workshop']
```

**`find` — retorna o primeiro item que bate na condição (ou `undefined`):**

```js
const eventoBuscado = eventos.find((evento) => evento.id === 3)
console.log(eventoBuscado.titulo) // Hackathon FACET

const inexistente = eventos.find((evento) => evento.id === 999)
console.log(inexistente) // undefined
```

**`some` e `every` — testam a coleção e retornam `boolean`:**

```js
const existeEventoLotado = eventos.some((evento) => evento.inscritos >= evento.vagas)
console.log(existeEventoLotado) // true (a Oficina de Vue.js está lotada)

const todosTemVagas = eventos.every((evento) => evento.inscritos < evento.vagas)
console.log(todosTemVagas) // false
```

**`sort` — ordena o array (⚠️ muta o array original):**

```js
// sort() muda o array ORIGINAL. Para não afetar `eventos`, copie antes com spread.
const eventosPorData = [...eventos].sort(
  (a, b) => new Date(a.dataHora) - new Date(b.dataHora),
)
console.log(eventosPorData.map((e) => e.titulo))
// ['Introdução a IA', 'Oficina de Vue.js', 'Semana da Computação', 'Hackathon FACET']

console.log(eventos.map((e) => e.titulo))
// ainda na ordem original — porque ordenamos a CÓPIA, não `eventos`
```

> **🔬 Investigue**
> Abra o Console do navegador (`F12`) e cole o array `eventos` da Seção 3.8 acima. Rode `console.table(eventos)` para ver a ordem atual, depois rode `eventos.sort((a, b) => a.vagas - b.vagas)` e `console.table(eventos)` de novo — a ordem mudou. Agora rode só `eventos` mais uma vez: ele continua alterado, porque `.sort()` muta o array original em vez de devolver uma cópia. É exatamente o bug que o item **A4** do Laboratório desta aula pede para você achar.

**Encadeando métodos** — o padrão mais comum no dia a dia:

```js
const resumoDePalestrasComVaga = eventos
  .filter((evento) => evento.categoria === 'palestra')
  .filter((evento) => evento.inscritos < evento.vagas)
  .map((evento) => `${evento.titulo} (${evento.vagas - evento.inscritos} vagas livres)`)

console.log(resumoDePalestrasComVaga)
// ['Semana da Computação (28 vagas livres)', 'Introdução a IA (25 vagas livres)']
```

### 3.9 Objetos e shorthand

```js
const titulo = 'Semana da Computação'
const vagas = 40

// Antes: repetir a chave e o valor
const eventoAntigo = { titulo: titulo, vagas: vagas }

// Shorthand: quando o nome da variável é igual ao nome da propriedade
const eventoModerno = { titulo, vagas }
console.log(eventoModerno) // { titulo: 'Semana da Computação', vagas: 40 }

// Shorthand também funciona para métodos
const gerenciadorDeEventos = {
  eventos: [],
  adicionar(evento) {          // em vez de: adicionar: function (evento) { ... }
    this.eventos.push(evento)
  },
  contar() {
    return this.eventos.length
  },
}
gerenciadorDeEventos.adicionar({ titulo: 'Novo evento' })
console.log(gerenciadorDeEventos.contar()) // 1

// Nomes de propriedade computados
const chave = 'categoria'
const filtro = { [chave]: 'palestra' }
console.log(filtro) // { categoria: 'palestra' }
```

### 3.10 Módulos ES: `import` e `export`

Organizar código em módulos é essencial — é assim que um projeto Vue inteiro é estruturado, um arquivo por responsabilidade.

```js
// arquivo: eventos.js
// export nomeado: pode haver vários por arquivo
export const CATEGORIAS = ['palestra', 'minicurso', 'workshop']

export function filtrarPorCategoria(eventos, categoria) {
  if (!categoria) return eventos
  return eventos.filter((evento) => evento.categoria === categoria)
}

export function calcularVagasRestantes(evento) {
  return evento.vagas - evento.inscritos
}

// export default: no máximo um por arquivo — geralmente a "coisa principal"
export default class GerenciadorDeEventos {
  constructor(eventosIniciais = []) {
    this.eventos = eventosIniciais
  }

  adicionar(evento) {
    this.eventos.push(evento)
  }
}
```

```js
// arquivo: main.js
// import nomeado: usa chaves { } e o mesmo nome do export
import { CATEGORIAS, filtrarPorCategoria } from './eventos.js'

// import default: sem chaves, você escolhe o nome
import GerenciadorDeEventos from './eventos.js'

// import combinando os dois na MESMA linha (é assim que se escreve na prática —
// não repita o import default do mesmo módulo, como fizemos acima só para separar os casos)
// import GerenciadorDeEventos, { calcularVagasRestantes } from './eventos.js'
import { calcularVagasRestantes } from './eventos.js'

console.log(CATEGORIAS) // ['palestra', 'minicurso', 'workshop']

const gerenciador = new GerenciadorDeEventos()
gerenciador.adicionar({ titulo: 'Minicurso de Git', categoria: 'minicurso', vagas: 20, inscritos: 5 })
console.log(calcularVagasRestantes(gerenciador.eventos[0])) // 15
```

Para rodar módulos ES direto no navegador (sem bundler ainda), o HTML precisa declarar `type="module"`:

```html
<script type="module" src="main.js"></script>
```

> **📌 Vale gravar**
> A partir da Aula 02, todo componente `.vue` é, por baixo, um módulo ES: ele importa outros componentes com `import` e é importado por quem o usa. Entender `import`/`export` agora evita confusão depois.

### 3.11 Classes

```js
class Evento {
  // Campos de instância (sintaxe moderna, sem precisar declarar no constructor)
  inscritos = 0

  constructor(titulo, categoria, vagas) {
    this.titulo = titulo
    this.categoria = categoria
    this.vagas = vagas
  }

  // Método de instância
  inscrever() {
    if (this.inscritos >= this.vagas) {
      throw new Error('Evento lotado')
    }
    this.inscritos += 1
  }

  // Getter: parece uma propriedade, mas é calculado
  get vagasRestantes() {
    return this.vagas - this.inscritos
  }
}

// Herança com extends
class Minicurso extends Evento {
  constructor(titulo, vagas, cargaHoraria) {
    super(titulo, 'minicurso', vagas) // chama o constructor da classe-mãe
    this.cargaHoraria = cargaHoraria
  }
}

const oficina = new Minicurso('Oficina de Vue.js', 25, 4)
oficina.inscrever()
oficina.inscrever()
console.log(oficina.vagasRestantes) // 23
console.log(oficina.cargaHoraria)   // 4
console.log(oficina instanceof Evento) // true
```

### 3.12 JSON: `parse` e `stringify`

```js
const evento = { id: 1, titulo: 'Semana da Computação', vagas: 40 }

// Objeto JavaScript → texto JSON (para enviar em uma requisição, por exemplo)
const textoJson = JSON.stringify(evento)
console.log(textoJson) // '{"id":1,"titulo":"Semana da Computação","vagas":40}'

// Com indentação, útil para debug/log
console.log(JSON.stringify(evento, null, 2))

// Texto JSON → objeto JavaScript (o inverso — comum ao ler resposta de API)
const textoRecebido = '{"id":2,"titulo":"Oficina de Vue.js","vagas":25}'
const objetoRecebido = JSON.parse(textoRecebido)
console.log(objetoRecebido.titulo) // Oficina de Vue.js
```

### 3.13 Assíncrono: de callback a `async/await`

O JavaScript é de thread única, então operações demoradas (rede, temporizadores) precisam de um jeito de "avisar quando terminar" sem travar tudo. A linguagem evoluiu em três estágios.

**Estágio 1 — callback (o jeito antigo, difícil de encadear):**

```js
function buscarEventoComCallback(id, aoTerminar) {
  setTimeout(() => {
    aoTerminar({ id, titulo: 'Semana da Computação' })
  }, 500)
}

buscarEventoComCallback(1, (evento) => {
  console.log('recebido:', evento.titulo)
  // se precisasse buscar outra coisa depois, teria que aninhar
  // outro callback aqui dentro — o famoso "callback hell"
})
```

**Estágio 2 — Promise (representa um valor que existirá no futuro):**

```js
function buscarEventoComPromise(id) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (id > 0) {
        resolve({ id, titulo: 'Semana da Computação' })
      } else {
        reject(new Error('id inválido'))
      }
    }, 500)
  })
}

buscarEventoComPromise(1)
  .then((evento) => console.log('recebido:', evento.titulo))
  .catch((erro) => console.error('deu erro:', erro.message))
```

**Estágio 3 — `async/await` (mesma Promise por baixo, sintaxe que lê como código síncrono):**

```js
async function carregarEvento() {
  try {
    const evento = await buscarEventoComPromise(1)
    console.log('recebido:', evento.titulo)
  } catch (erro) {
    console.error('deu erro:', erro.message)
  }
}

carregarEvento()
```

> **🔎 Por baixo do capô**
> `async/await` não é uma tecnologia nova e diferente de Promise — é **açúcar sintático** sobre Promise. `await` pausa a execução da função `async` até a Promise resolver ou rejeitar, sem bloquear o restante do programa. Todo `await` precisa estar dentro de uma função marcada `async`.

**`fetch` com `async/await` e `try/catch` — o padrão que vamos usar do início ao fim da trilha:**

```js
async function buscarEventosDaApi() {
  try {
    const resposta = await fetch('https://jsonplaceholder.typicode.com/posts?_limit=5')

    if (!resposta.ok) {
      throw new Error(`Erro HTTP: ${resposta.status}`)
    }

    const dados = await resposta.json()
    console.log('eventos recebidos:', dados.length)
    return dados
  } catch (erro) {
    console.error('falha ao buscar eventos:', erro.message)
    return []
  }
}

buscarEventosDaApi()
```

**`Promise.all` — disparar várias requisições em paralelo e esperar todas:**

```js
async function carregarDadosDaHome() {
  try {
    const [respostaEventos, respostaCategorias] = await Promise.all([
      fetch('https://jsonplaceholder.typicode.com/posts?_limit=5'),
      fetch('https://jsonplaceholder.typicode.com/users?_limit=3'),
    ])

    const eventos = await respostaEventos.json()
    const categorias = await respostaCategorias.json()

    console.log('eventos:', eventos.length, 'categorias:', categorias.length)
  } catch (erro) {
    // Promise.all rejeita assim que QUALQUER uma das promises falhar
    console.error('alguma requisição falhou:', erro.message)
  }
}

carregarDadosDaHome()
```

> **⚠️ Atenção**
> `Promise.all` falha rápido: se uma das promises rejeitar, todas as outras são "abandonadas" do ponto de vista do `.catch`/`try-catch`, mesmo que já estivessem resolvidas. Quando precisar do resultado de todas independentemente de falha, use `Promise.allSettled` (não obrigatório nesta trilha, mas bom saber que existe).

## 🧩 Padrão de projeto em uso — Module / Revealing Module

O padrão **Module** organiza código relacionado (estado + comportamento) dentro de um único bloco, escondendo detalhes internos e expondo apenas uma interface pública. Antes dos módulos ES nativos, isso era feito com uma IIFE (função invocada imediatamente) que retornava um objeto com as partes públicas — o **Revealing Module Pattern**:

```js
// Revealing Module Pattern — jeito pré-ES2015 de encapsular
const GerenciadorDeEventos = (function () {
  // "privado": só existe dentro deste escopo de função
  let eventos = []

  function adicionar(evento) {
    eventos.push(evento)
  }

  function contarVagas() {
    return eventos.reduce((total, e) => total + e.vagas, 0)
  }

  // "revela" (expõe) só o que deve ser público
  return {
    adicionar,
    contarVagas,
  }
})()

GerenciadorDeEventos.adicionar({ titulo: 'Semana da Computação', vagas: 40 })
console.log(GerenciadorDeEventos.contarVagas()) // 40
// GerenciadorDeEventos.eventos não existe aqui fora — está encapsulado
```

Os **módulos ES** (`import`/`export`, Seção 3.10) resolvem o mesmo problema de forma nativa e sem a necessidade da IIFE: tudo que não é exportado com `export` é automaticamente privado ao arquivo. É o mesmo padrão de projeto, com sintaxe de linguagem em vez de truque de engenharia. Todo componente `.vue` que você vai escrever a partir da Aula 02 é, conceitualmente, um Module: estado interno + funções, expondo ao `<template>` só o que for necessário.

## 💻 Mão na massa — configurando o primeiro arquivo de revisão

Vamos consolidar tudo em um único exercício guiado, rodado no navegador.

**Passo 1 — crie a pasta e os arquivos.**

```bash
mkdir -p ~/unieventos-aula01 && cd ~/unieventos-aula01
touch index.html eventos.js main.js
```

**Passo 2 — o HTML que carrega o módulo:**

```html
<!-- index.html -->
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <title>Aula 01 — Revisão de JavaScript</title>
</head>
<body>
  <h1>Abra o Console do navegador (F12) para ver os resultados</h1>
  <ul id="saida"></ul>

  <script type="module" src="main.js"></script>
</body>
</html>
```

**Passo 3 — o módulo com os dados e as funções:**

```js
// eventos.js
export const eventos = [
  { id: 1, titulo: 'Semana da Computação', categoria: 'palestra', dataHora: '2030-09-10T19:00:00', vagas: 40, inscritos: 12 },
  { id: 2, titulo: 'Oficina de Vue.js', categoria: 'minicurso', dataHora: '2030-08-20T14:00:00', vagas: 25, inscritos: 25 },
  { id: 3, titulo: 'Hackathon FACET', categoria: 'workshop', dataHora: '2030-10-05T08:00:00', vagas: 60, inscritos: 18 },
  { id: 4, titulo: 'Introdução a IA', categoria: 'palestra', dataHora: '2030-08-18T19:30:00', vagas: 80, inscritos: 55 },
]

export function filtrarPorCategoria(lista, categoria) {
  if (!categoria) return lista
  return lista.filter((evento) => evento.categoria === categoria)
}

export function ordenarPorData(lista) {
  return [...lista].sort((a, b) => new Date(a.dataHora) - new Date(b.dataHora))
}

export function totalDeVagas(lista) {
  return lista.reduce((total, evento) => total + evento.vagas, 0)
}

export function formatarData(dataIso) {
  const data = new Date(dataIso)
  return new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: 'long',
    hour: '2-digit',
    minute: '2-digit',
  }).format(data)
}
```

**Passo 4 — consumir o módulo, renderizar no DOM e buscar dados de uma API:**

```js
// main.js
import { eventos, filtrarPorCategoria, ordenarPorData, totalDeVagas, formatarData } from './eventos.js'

const listaEl = document.getElementById('saida')

function renderizarLista(lista) {
  listaEl.innerHTML = ''
  lista.forEach((evento) => {
    const item = document.createElement('li')
    item.textContent = `${evento.titulo} — ${formatarData(evento.dataHora)} (${evento.vagas} vagas)`
    listaEl.appendChild(item)
  })
}

const palestras = filtrarPorCategoria(eventos, 'palestra')
const ordenados = ordenarPorData(eventos)

console.log('total de palestras:', palestras.length)
console.log('total de vagas em todos os eventos:', totalDeVagas(eventos))
renderizarLista(ordenados)

// buscando dados externos de verdade
async function buscarPostsDeExemplo() {
  try {
    const resposta = await fetch('https://jsonplaceholder.typicode.com/posts?_limit=3')
    if (!resposta.ok) throw new Error(`HTTP ${resposta.status}`)
    const posts = await resposta.json()
    console.log('posts de exemplo recebidos da API:', posts)
  } catch (erro) {
    console.error('não foi possível buscar os posts:', erro.message)
  }
}

buscarPostsDeExemplo()
```

**Passo 5 — abra `index.html`** com a extensão **Live Server** do VS Code (ou qualquer servidor local — módulos ES não funcionam abrindo o arquivo direto com `file://` por causa de CORS).

### Como testar

Com a página aberta pelo Live Server, abra o DevTools (`F12`) e vá ao **Console**.

Resultado esperado, nesta ordem:

```text
total de palestras: 2
total de vagas em todos os eventos: 205
posts de exemplo recebidos da API: (3) [{…}, {…}, {…}]
```

E, na página, a lista de eventos renderizada em ordem de data, do mais próximo ao mais distante. Confira também os dois sinais de que os módulos ES estão funcionando: (1) o `<script type="module">` não reclama de `import`; (2) abrir o mesmo arquivo com duplo clique (`file://`) **quebra** com erro de CORS — é exatamente o motivo de usar um servidor local. A linha dos posts chegar **por último**, depois das duas primeiras, é a prova visual de que `fetch` é assíncrono: o `console.log` de baixo do `buscarPostsDeExemplo()` não espera a resposta da rede.

## 🧪 Laboratório

Use o array `eventos` do Passo 3 acima para os exercícios. Crie um arquivo `lab.js`, importe o que precisar de `eventos.js` e teste cada exercício no console.

### Nível A — Fixação

**A1.** Preveja a saída do trecho abaixo **sem rodar**, usando o que a Seção 3.3 explica sobre arrow functions e `this`:

```js
const contador = {
  vagas: 5,
  reduzir: function () {
    setTimeout(function () {
      console.log('a', this?.vagas)
    }, 0)
    setTimeout(() => {
      console.log('b', this.vagas)
    }, 0)
  },
}
contador.reduzir()
```

Resultado esperado: a linha `a` imprime `undefined` (a `function` tradicional perde o `this` de `contador` dentro do `setTimeout`); a linha `b` imprime `5` (a arrow function herda o `this` de `reduzir`).

**A2.** Complete a linha que falta para que `resumo` traga só os **títulos** dos eventos de categoria `'palestra'` que ainda têm vaga (`inscritos < vagas`), na mesma ordem em que aparecem no array `eventos`:

```js
const resumo = eventos
  .filter((evento) => evento.categoria === 'palestra')
  // complete aqui
  .map((evento) => evento.titulo)
```

Resultado esperado: a linha que falta é `.filter((evento) => evento.inscritos < evento.vagas)`, resultando em `['Semana da Computação', 'Introdução a IA']`.

**A3.** Em uma frase: por que `vagasInformadas || 10` é um bug quando `vagasInformadas` vale `0`, mas `vagasInformadas ?? 10` não é?

Resultado esperado: porque `||` cai no valor padrão para qualquer valor "falsy" — incluindo `0`, que é um número de vagas válido — enquanto `??` só usa o padrão quando o valor é `null` ou `undefined`.

**A4.** Ache o erro nas linhas abaixo. A função deveria devolver os eventos ordenados por vagas restantes **sem alterar** o array `eventos` original, mas, depois de chamá-la, um `console.log(eventos[0].titulo)` seguinte mostra uma ordem diferente da original:

```js
function ordenarPorVagasRestantes(lista) {
  return lista.sort(
    (a, b) => (b.vagas - b.inscritos) - (a.vagas - a.inscritos),
  )
}
```

Resultado esperado: falta copiar o array antes de ordenar — `lista.sort(...)` muta `lista`, que é a mesma referência de `eventos`. A correção é `return [...lista].sort(...)`.

**A5.** Preveja a saída do trecho abaixo usando o que a Seção 3.7 explica sobre optional chaining e nullish coalescing:

```js
const evento = { titulo: 'Hackathon FACET', local: { predio: 'Bloco B' } }
console.log(evento.local?.sala ?? 'a definir')
console.log(evento.organizador?.contato?.email ?? 'sem contato')
```

Resultado esperado: `a definir` (a propriedade `sala` não existe dentro de `local`, mas `?.` evita o erro) e `sem contato` (nem `organizador` existe, e a cadeia inteira encurta sem quebrar).

### Nível B — Aplicação

**B1.** Filtrar por categoria. Escreva uma função `apenasWorkshops(lista)` que retorne só os eventos de categoria `'workshop'`, usando `filter`.

Resultado esperado: array com 1 item (`Hackathon FACET`).

<details markdown="1">
<summary>Dica</summary>

`lista.filter((evento) => evento.categoria === 'workshop')`
</details>

**B2.** Ordenar por vagas restantes. Escreva `ordenarPorVagasRestantes(lista)` que devolva uma cópia do array ordenada da maior para a menor quantidade de vagas restantes (`vagas - inscritos`), sem mutar o array original.

Resultado esperado: o array original (`eventos`) mantém a mesma ordem depois de chamar a função.

<details markdown="1">
<summary>Dica</summary>

Copie primeiro com `[...lista]`, depois use `.sort((a, b) => (b.vagas - b.inscritos) - (a.vagas - a.inscritos))`.
</details>

**B3.** Calcular vagas totais com `reduce`. Escreva `vagasRestantesTotais(lista)` que retorne a soma de `vagas - inscritos` de todos os eventos.

Resultado esperado: `95` (para o array de exemplo: 28 + 0 + 42 + 25).

<details markdown="1">
<summary>Dica</summary>

`lista.reduce((total, evento) => total + (evento.vagas - evento.inscritos), 0)`
</details>

**B4.** Formatar datas em pt-BR. Usando `Intl.DateTimeFormat('pt-BR', { dateStyle: 'long' })`, formate a `dataHora` de cada evento e monte um array de strings como `"10 de setembro de 2030"`.

Resultado esperado: 4 strings de data em português.

<details markdown="1">
<summary>Dica</summary>

```js
const formatador = new Intl.DateTimeFormat('pt-BR', { dateStyle: 'long' })
eventos.map((evento) => formatador.format(new Date(evento.dataHora)))
```
</details>

### Nível C — Desafio

**C1.** Buscar dados de uma API pública e renderizar. Usando `fetch` e `async/await`, busque `https://jsonplaceholder.typicode.com/users` (sem parâmetro de limite), pegue apenas os 3 primeiros com `.slice(0, 3)`, e renderize o `name` de cada um em uma lista `<ul>` no HTML. Se a rede falhar (desligue o Wi-Fi um instante e tente de novo), a página não pode travar nem ficar em branco — mostre uma mensagem de erro no lugar da lista.

Resultado esperado: 3 nomes de usuários aparecendo na página; com a rede desligada, uma mensagem de erro visível em vez de tela em branco, e nenhum erro não tratado no Console.

<details markdown="1">
<summary>Dica</summary>

`const usuarios = await (await fetch(url)).json()`, depois `usuarios.slice(0, 3).forEach(...)` criando `<li>` como no Passo 4. Para o tratamento de erro, envolva a busca e a renderização em `try/catch` e, no `catch`, escreva a mensagem de erro no mesmo elemento `<ul>` com `innerHTML`.
</details>

## 🏆 Desafios

### ⭐ O evento com zero vagas que "ganha" 10

Tags: javascript, bug, investigacao

Um colega escreveu `vagasParaExibir(evento)` para mostrar o número de vagas no card do evento, usando o padrão que a Seção 3.7 alertou ser perigoso: `evento.vagasDisponiveis || 10`. Um evento com exatamente **zero** vagas está aparecendo na tela como "10 vagas disponíveis" — e alunos estão tentando se inscrever em um evento lotado. Ache a causa raiz e corrija sem quebrar o caso em que o campo realmente não foi informado.

**Critérios de pronto**

- `vagasParaExibir({ vagasDisponiveis: 0 })` retorna `0` (evento esgotado, sem valor padrão).
- `vagasParaExibir({})` (campo ausente) retorna `10` (o valor padrão continua funcionando quando faz sentido).
- `vagasParaExibir({ vagasDisponiveis: 25 })` retorna `25`.
- Um comentário de 2 linhas acima da função explica, em português, por que `||` escondia esse bug e por que `??` resolve.

<details markdown="1">
<summary>Pistas</summary>

1. Releia a Seção 3.7 — a diferença entre `||` e `??` está exatamente nos valores "falsy" que não são `null`/`undefined`.
2. Teste os três casos no Console antes de mexer no código: `0 || 10`, `undefined || 10`, `0 ?? 10`, `undefined ?? 10`.
3. A troca é de um único operador — mas escreva o teste dos três casos antes de trocar, para provar que a correção não quebrou o caso do valor ausente.
</details>

### ⭐⭐ Quanto custa recriar a lista inteira a cada tecla?

Tags: performance, dom, javascript, devtools

O código da Seção 2.1 (DOM manual) apaga `listaEl.innerHTML` e reconstrói tudo a cada tecla digitada na busca — funciona bem com 4 eventos, mas e com mil? Gere uma lista grande, meça o custo real de `renderizar()` a cada tecla e decida, com números, se vale a pena adicionar um `debounce` (atraso antes de reagir) antes de otimizar de verdade.

**Critérios de pronto**

- Um array `eventosGrandes` com 1.000 itens gerados por código (`Array.from({ length: 1000 }, (_, i) => ({ ... }))`), reaproveitando os campos de `eventos.js`.
- `renderizar()` adaptada para `eventosGrandes`, com `performance.now()` antes e depois da reconstrução do DOM, logando o tempo de cada chamada no Console.
- Uma tabela (fora do código, no comentário ou no README) com o tempo de 5 renderizações digitando rápido, sem debounce.
- A mesma medição depois de adicionar um `debounce` de 300 ms no `input` (só chama `renderizar()` 300 ms depois da última tecla), com uma frase concluindo se, neste caso, o ganho compensou a complexidade extra.

<details markdown="1">
<summary>Pistas</summary>

1. `performance.now()` retorna milissegundos; chame uma vez antes e uma vez depois de `renderizar()` e subtraia.
2. Para gerar 1.000 eventos variados, alterne `categoria` entre `'palestra'`, `'minicurso'` e `'workshop'` usando o resto da divisão (`i % 3`).
3. O padrão de debounce é o mesmo `setTimeout` + `clearTimeout` que reaparece na aula sobre CRUD (Aula 11) — pesquise "debounce javascript" se quiser ver outras implementações antes de escrever a sua.
4. Ligue a aba **Performance** do DevTools durante uma digitação rápida sem debounce — o gráfico de "Scripting" mostra visualmente o custo que você já mediu com números.
</details>

### ⭐⭐⭐ O módulo de dados do seu projeto autoral

Tags: javascript, projeto, api, async

Toda a Seção 3 revisou ferramentas de JavaScript moderno usando eventos como exemplo — mas o seu projeto autoral (Seção 1.6) tem outro domínio. Construa o `dominio.js` real do seu projeto, aplicando classes, módulos, os métodos de array e uma busca assíncrona a dados reais (ou simulados) do seu tema.

**Critérios de pronto**

- Um arquivo `dominio.js` define ao menos **duas classes relacionadas** por composição ou herança (ex.: `Quadra` e `Reserva`, `Planta` e `Floracao`), cada uma com pelo menos um `get` calculado (equivalente a `vagasRestantes` da Seção 3.11).
- Três funções exportadas (`export function`) que usam `filter`, `map`, `reduce` ou `sort` sobre uma lista de pelo menos 8 itens de exemplo do seu domínio, **sem mutar** o array recebido.
- Uma função `async` que busca dados de uma API pública (do seu tema, ou `jsonplaceholder.typicode.com` como placeholder) com `try/catch`, sem deixar a página quebrada se a busca falhar.
- Um `main.js` que importa tudo de `dominio.js` e renderiza pelo menos 5 itens na tela, em HTML puro (sem framework — isso só começa na Aula 02).
- Um `README.md` de 5 a 10 linhas explicando as entidades escolhidas e o que cada função exportada faz.

<details markdown="1">
<summary>Pistas</summary>

1. Reveja a Seção 3.10 (módulos) e 3.11 (classes) — a estrutura é a mesma do `eventos.js`/`GerenciadorDeEventos` do Passo 3 do "Mão na massa", só que com as entidades do seu tema.
2. Comece pelas classes e pelos dados de exemplo (um array com 8 objetos criados na mão) antes de pensar na API — é mais fácil testar `filter`/`map`/`reduce` sobre dados que você já conhece.
3. Se seu tema não tiver uma API pública específica, use o JSONPlaceholder mesmo (`/posts`, `/users`, `/comments`) só para provar que o `fetch` com `try/catch` funciona — a ligação semântica com o tema pode vir depois, na Unidade 3.
4. Teste o `catch` de propósito: chame a função com uma URL errada (ex.: troque `.com` por `.com.br/inexistente`) e confira que a página continua funcionando, só sem os dados da API.
</details>

## 🐛 Erros comuns e como resolver

| Sintoma | Causa | Solução |
|---|---|---|
| `this` é `undefined` dentro de um callback | Usou `function` tradicional dentro de um método, perdendo o `this` do objeto | Troque por arrow function, que herda o `this` do escopo externo |
| Array original mudou de ordem sem eu querer | `.sort()` muta o array original | Copie antes: `[...array].sort(...)` |
| `if (vagas == '40')` deu `true` mas os tipos são diferentes | Uso de `==` faz coerção de tipo | Use sempre `===` e `!==` |
| `TypeError: Cannot read properties of undefined` | Esqueceu de colocar `await` antes de uma Promise | Confira se toda chamada assíncrona tem `await` dentro de uma função `async` |
| `fetch` falha com erro de CORS no console | A API não libera requisições vindas do seu domínio local | Use uma API que libere CORS publicamente (como JSONPlaceholder) ou rode via proxy/back-end nas aulas futuras |

## 🏠 Para praticar depois da aula (1 h)

1. Escolha o **tema do seu projeto autoral** seguindo as regras da Seção 1.6.
2. Crie um repositório público no GitHub chamado `<seu-tema>-web` (ex.: `pantanal-plantas-web`).
3. Escreva um `README.md` na raiz do repositório contendo:
   - Uma descrição de 3 a 5 linhas do problema que o projeto resolve.
   - As **entidades** do domínio (no mínimo duas relacionadas) com seus **campos**, no mesmo estilo da Seção 3 do plano de curso (compare com `Evento`/`Inscricao`/`Usuario` do UniEventos).
   - As **telas previstas**: pelo menos listagem com filtro, detalhe, e uma área autenticada.
4. Guarde no seu repositório: commit + push.

**Critério de pronto:** repositório público criado, `README.md` com descrição, modelo de dados (entidades + campos) e lista de telas.

## ✅ Checkpoint do projeto autoral

Ao final desta aula, seu repositório deve ter:

- [ ] Repositório criado no GitHub, nomeado `<tema>-web`, com visibilidade pública.
- [ ] `README.md` com descrição do projeto, entidades e campos, e telas previstas.
- [ ] Ambiente instalado e verificado: `node -v` mostrando Node 22 LTS, VS Code com as extensões Vue - Official, ESLint e Prettier.
- [ ] Git configurado localmente (`git config --global user.name/user.email`).

## 📚 Para aprofundar

- [MDN Web Docs — JavaScript](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript) — referência oficial e gratuita, em português.
- [MDN — Guia de gramática e tipos](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Guide)
- [MDN — `Array.prototype`](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Global_Objects/Array) — todos os métodos de array com exemplos.
- [MDN — `Intl.DateTimeFormat`](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat)
- [javascript.info](https://javascript.info/) — curso completo e gratuito de JS moderno.
- [Node.js — site oficial](https://nodejs.org)

---

**Na próxima aula** começamos o Vue de verdade — `createApp`, instância, `data`/`methods` (Options API) e Composition API com `<script setup>`, além das diretivas básicas (`v-bind`, `v-on`, `v-model`, `v-if`, `v-for`). Traga o ambiente instalado e o repositório do projeto autoral criado.
