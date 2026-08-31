# Aula 03 — Vue: listas, computed e ciclo de vida

> **Nível 3 — Frameworks Modernos** · Unidade 1: Fundamentos de front-end com Vue.js
> WebLab · UNEMAT Sinop · Prof. Ivan Luiz Pedroso Pires
> **Carga:** 3 aulas de 50 min (presencial) + 1 h (assíncrona)

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Usar `v-for` sobre arrays, objetos e ranges, inclusive em `<template>` e listas aninhadas.
- Explicar por que combinar `v-for` com `v-if` no mesmo elemento é um antipadrão e resolvê-lo com `computed`.
- Criar propriedades `computed()`, entender seu cache e diferenciar computed de método e de watch.
- Usar `watch()` e `watchEffect()` com as opções `immediate` e `deep`, e parar um watcher.
- Carregar dados assincronamente dentro de `onMounted()`, implementando os três estados de tela: carregando, erro e vazio.
- Formatar datas e números em pt-BR com `Intl`, e aplicar classes/estilos condicionais com `:class` e `:style`.
- Entregar uma versão do UniEventos com filtros combinados resolvidos por computed, carregamento assíncrono e destaque visual condicional.

## 📋 Pré-requisitos desta aula

Na Aula 02 criamos a primeira versão do UniEventos: lista, busca, filtro e inscrição, tudo com diretivas básicas e uma função de filtro chamada manualmente três vezes no template. Hoje resolvemos exatamente esse desperdício com `computed()`, aprofundamos `v-for` e passamos a carregar os eventos de forma assíncrona dentro de `onMounted()`.

- Projeto `unieventos-web` funcionando, com a listagem, busca e filtro da Aula 02.
- Domínio de `ref()`, `v-model`, `v-for`+`:key`, `v-if`/`v-show` e dos hooks `onMounted`/`onUnmounted` (Aula 02).

> **⚠️ Atenção**
> Se seu `App.vue` da Aula 02 ainda não estiver rodando com `npm run dev` sem erros, resolva isso antes de continuar — hoje vamos editar esse mesmo arquivo.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | `v-for` avançado, o antipadrão `v-for`+`v-if`, introdução a `computed()` |
| 2 | 50 min | `computed` com getter/setter, `watch`/`watchEffect`, `onMounted` com os três estados |
| 3 | 50 min | Formatação `Intl`, `:class`/`:style`, mão na massa: UniEventos com filtros combinados |

## 1. `v-for` avançado

Na Aula 02 vimos `v-for` sobre um array simples. O Vue também itera sobre objetos, ranges numéricos, e permite estruturas mais ricas.

### 1.1 `v-for` sobre objetos

```vue
<script setup>
import { ref } from 'vue'

const evento = ref({
  titulo: 'Semana da Computação',
  categoria: 'palestra',
  local: 'Auditório Central',
  vagas: 40,
})
</script>

<template>
  <!-- (valor, chave) — nessa ordem -->
  <ul>
    <li v-for="(valor, chave) in evento" :key="chave">
      <strong>{{ chave }}:</strong> {{ valor }}
    </li>
  </ul>

  <!-- também existe (valor, chave, indice) com o terceiro parâmetro opcional -->
  <ul>
    <li v-for="(valor, chave, indice) in evento" :key="chave">
      {{ indice }}. {{ chave }} = {{ valor }}
    </li>
  </ul>
</template>
```

### 1.2 `v-for` sobre um range numérico

```vue
<template>
  <!-- v-for="n in 5" gera n = 1, 2, 3, 4, 5 (começa em 1, não em 0) -->
  <span v-for="n in 5" :key="n" class="estrela">⭐</span>

  <!-- útil para paginação simples -->
  <button v-for="pagina in 4" :key="pagina">{{ pagina }}</button>
</template>
```

### 1.3 `v-for` em `<template>` — repetir um grupo sem elemento extra

```vue
<script setup>
import { ref } from 'vue'

const eventos = ref([
  { id: 1, titulo: 'Semana da Computação', categoria: 'palestra' },
  { id: 2, titulo: 'Oficina de Vue.js', categoria: 'minicurso' },
])
</script>

<template>
  <dl>
    <!-- <template> com v-for não gera elemento HTML próprio no DOM final —
         só repete o que está dentro dele. Útil quando você precisa de
         MAIS de um elemento irmão por item, sem um <div> desnecessário. -->
    <template v-for="evento in eventos" :key="evento.id">
      <dt>{{ evento.titulo }}</dt>
      <dd>{{ evento.categoria }}</dd>
    </template>
  </dl>
</template>
```

### 1.4 Listas aninhadas

```vue
<script setup>
import { ref } from 'vue'

const programacao = ref([
  {
    dia: 'Dia 1',
    sessoes: [
      { horario: '19h', titulo: 'Abertura' },
      { horario: '20h', titulo: 'Palestra magna' },
    ],
  },
  {
    dia: 'Dia 2',
    sessoes: [
      { horario: '14h', titulo: 'Oficina de Vue.js' },
      { horario: '16h', titulo: 'Mesa redonda' },
    ],
  },
])
</script>

<template>
  <div v-for="dia in programacao" :key="dia.dia" class="dia-programacao">
    <h3>{{ dia.dia }}</h3>
    <!-- v-for aninhado: a key interna só precisa ser única DENTRO do
         v-for externo, mas usar algo que combine as duas chaves evita
         qualquer ambiguidade em listas grandes -->
    <ul>
      <li v-for="sessao in dia.sessoes" :key="`${dia.dia}-${sessao.horario}`">
        {{ sessao.horario }} — {{ sessao.titulo }}
      </li>
    </ul>
  </div>
</template>
```

## 2. O antipadrão `v-for` + `v-if` juntos

```vue
<script setup>
import { ref } from 'vue'

const eventos = ref([
  { id: 1, titulo: 'Semana da Computação', categoria: 'palestra', vagas: 40, inscritos: 40 },
  { id: 2, titulo: 'Oficina de Vue.js', categoria: 'minicurso', vagas: 25, inscritos: 10 },
])
</script>

<template>
  <!-- ⚠️ EVITE: v-for e v-if no MESMO elemento -->
  <li
    v-for="evento in eventos"
    v-if="evento.inscritos < evento.vagas"
    :key="evento.id"
  >
    {{ evento.titulo }}
  </li>
</template>
```

Por que isso é um problema:

1. **Precedência confusa.** No Vue 3, quando `v-if` e `v-for` estão no mesmo elemento, `v-if` tem prioridade mais alta na avaliação, mas isso significa que ele tenta avaliar a condição **antes** da variável do `v-for` (`evento`) estar disponível no escopo — um erro fácil de disparar sem perceber.
2. **Desempenho.** O Vue recria a checagem `v-if` a cada item, em **todo** re-render da lista, mesmo quando o critério do filtro não teve nenhuma relação com a mudança que disparou a atualização.
3. **Legibilidade.** Misturar "o que iterar" com "o que exibir" no mesmo atributo deixa o template difícil de ler.

**A solução: filtre antes, com `computed`, e itere sobre o resultado já filtrado.**

```vue
<script setup>
import { ref, computed } from 'vue'

const eventos = ref([
  { id: 1, titulo: 'Semana da Computação', categoria: 'palestra', vagas: 40, inscritos: 40 },
  { id: 2, titulo: 'Oficina de Vue.js', categoria: 'minicurso', vagas: 25, inscritos: 10 },
])

// computed: calcula UMA VEZ, o template só itera sobre o resultado
const eventosComVaga = computed(() =>
  eventos.value.filter((evento) => evento.inscritos < evento.vagas),
)
</script>

<template>
  <!-- correto: v-for sozinho, sobre uma lista já pronta -->
  <li v-for="evento in eventosComVaga" :key="evento.id">
    {{ evento.titulo }}
  </li>
</template>
```

Isso nos leva ao assunto central da aula de hoje: `computed()`.

## 3. `computed()`: cache de verdade

### 3.1 O problema que `computed` resolve

Na Aula 02, `obterEventosFiltrados()` era uma **função comum**, chamada manualmente no template. Toda chamada refaz o cálculo do zero — não importa se os dados mudaram ou não.

```vue
<script setup>
import { ref } from 'vue'

const eventos = ref([
  { id: 1, titulo: 'Semana da Computação', vagas: 40, inscritos: 12 },
  { id: 2, titulo: 'Oficina de Vue.js', vagas: 25, inscritos: 25 },
])

// MÉTODO: recalcula toda vez que é chamado, mesmo sem nada ter mudado
function totalDeVagasComMetodo() {
  console.log('calculando total de vagas (método)...')
  return eventos.value.reduce((total, evento) => total + evento.vagas, 0)
}
</script>

<template>
  <!-- se este valor aparecer 3 vezes no template, o log acima roda 3 vezes -->
  <p>{{ totalDeVagasComMetodo() }}</p>
  <p>{{ totalDeVagasComMetodo() }}</p>
</template>
```

```vue
<script setup>
import { ref, computed } from 'vue'

const eventos = ref([
  { id: 1, titulo: 'Semana da Computação', vagas: 40, inscritos: 12 },
  { id: 2, titulo: 'Oficina de Vue.js', vagas: 25, inscritos: 25 },
])

// COMPUTED: calcula uma vez e GUARDA o resultado em cache.
// Só recalcula quando uma dependência reativa (eventos, neste caso) muda.
const totalDeVagas = computed(() => {
  console.log('calculando total de vagas (computed)...')
  return eventos.value.reduce((total, evento) => total + evento.vagas, 0)
})
</script>

<template>
  <!-- mesmo aparecendo 2 vezes, o log acima roda 1 vez só,
       porque o segundo acesso lê o valor já em cache -->
  <p>{{ totalDeVagas }}</p>
  <p>{{ totalDeVagas }}</p>
</template>
```

> **🔎 Por baixo do capô**
> Um `computed` sabe exatamente quais variáveis reativas ele lê durante sua execução (aqui, `eventos`) — o mesmo mecanismo de rastreamento de dependências do padrão Observer que vimos na Aula 02. Enquanto nenhuma dessas dependências mudar, o Vue devolve o valor guardado em cache, sem executar a função de novo. Isso é diferente de um método, que roda de novo a cada chamada, sempre, sem cache algum.

> **🔬 Investigue**
> Rode o segundo exemplo (com `computed`) no navegador e abra o Console. Some mais um `<p>{{ totalDeVagas }}</p>` ao template, salve, e conte quantas vezes a mensagem "calculando total de vagas (computed)..." aparece no Console ao carregar a página — deveria continuar sendo **uma vez só**, mesmo com três usos no template. Agora clique em algo que altere `eventos` (ou rode `eventos.value.push({ id: 3, titulo: 'Teste', vagas: 10, inscritos: 0 })` direto no Console) e veja o log aparecer de novo — só quando a dependência realmente muda.

### 3.2 `computed` com getter e setter

Por padrão, um `computed` é somente leitura. Mas é possível criar um que também aceita escrita, definindo `get` e `set`:

```vue
<script setup>
import { ref, computed } from 'vue'

const nome = ref('Ivan')
const sobrenome = ref('Pires')

// forma somente leitura (a mais comum)
const nomeCompleto = computed(() => `${nome.value} ${sobrenome.value}`)

// forma com getter E setter
const nomeCompletoEditavel = computed({
  get() {
    return `${nome.value} ${sobrenome.value}`
  },
  set(novoValor) {
    const partes = novoValor.split(' ')
    nome.value = partes[0]
    sobrenome.value = partes.slice(1).join(' ')
  },
})

function renomear() {
  // escrever em um computed com setter dispara o "set" acima,
  // que por sua vez atualiza nome e sobrenome
  nomeCompletoEditavel.value = 'Maria Silva'
}
</script>

<template>
  <p>{{ nomeCompleto }}</p>
  <button @click="renomear">Renomear</button>
</template>
```

### 3.3 Computed encadeadas

```vue
<script setup>
import { ref, computed } from 'vue'

const eventos = ref([
  { id: 1, titulo: 'Semana da Computação', categoria: 'palestra', vagas: 40, inscritos: 40 },
  { id: 2, titulo: 'Oficina de Vue.js', categoria: 'minicurso', vagas: 25, inscritos: 10 },
  { id: 3, titulo: 'Hackathon FACET', categoria: 'workshop', vagas: 60, inscritos: 18 },
])

// primeira computed: filtra por vaga disponível
const eventosComVaga = computed(() =>
  eventos.value.filter((evento) => evento.inscritos < evento.vagas),
)

// segunda computed: DEPENDE da primeira — encadeamento
const totalDeVagasLivres = computed(() =>
  eventosComVaga.value.reduce((total, evento) => total + (evento.vagas - evento.inscritos), 0),
)
</script>

<template>
  <p>Eventos com vaga: {{ eventosComVaga.length }}</p>
  <p>Total de vagas livres: {{ totalDeVagasLivres }}</p>
</template>
```

### 3.4 Computed × método × watch

| | `computed` | método | `watch` |
|---|---|---|---|
| Tem cache? | Sim | Não | Não se aplica (não retorna valor) |
| Quando roda | Só quando uma dependência muda | Toda vez que é chamado | Quando a fonte observada muda |
| Uso típico | Derivar um valor a partir de outro estado | Reagir a um evento de UI (clique) | Executar um efeito colateral (chamar API, logar, sincronizar `localStorage`) |
| Retorna valor usável no template? | Sim | Sim (se chamado) | Não diretamente |

## 4. `watch()` e `watchEffect()`

`computed` deriva um **valor**. `watch`/`watchEffect` executam um **efeito colateral** (algo que não é "calcular e devolver", como fazer uma requisição, gravar em `localStorage`, exibir um alerta) em reação a uma mudança.

### 4.1 `watch()` — observa uma fonte específica

```vue
<script setup>
import { ref, watch } from 'vue'

const busca = ref('')
const totalDeBuscas = ref(0)

// watch(fonte, callback) — só roda quando "busca" muda
watch(busca, (valorNovo, valorAntigo) => {
  console.log(`busca mudou de "${valorAntigo}" para "${valorNovo}"`)
  totalDeBuscas.value++
})

// watch com { immediate: true } — roda também na primeira vez,
// mesmo sem a fonte ainda ter mudado
const categoriaFiltro = ref('')
watch(
  categoriaFiltro,
  (valor) => {
    console.log('categoria selecionada:', valor || '(nenhuma)')
  },
  { immediate: true },
)
</script>
```

### 4.2 `watch` com `{ deep: true }` — observar objetos/arrays por dentro

```vue
<script setup>
import { reactive, watch } from 'vue'

const filtros = reactive({
  busca: '',
  categoria: '',
  apenasComVaga: false,
})

// por padrão, watch em um objeto reactive só dispara se a REFERÊNCIA mudar.
// como alterações em filtros.busca são mudanças INTERNAS ao objeto,
// precisamos de { deep: true } para o watch perceber.
watch(
  filtros,
  (valorNovo) => {
    console.log('algum filtro mudou:', valorNovo)
  },
  { deep: true },
)
</script>
```

### 4.3 `watchEffect()` — roda de novo automaticamente, sem declarar a fonte

```vue
<script setup>
import { ref, watchEffect } from 'vue'

const busca = ref('')
const categoriaFiltro = ref('')

// watchEffect executa a função IMEDIATAMENTE (não precisa de immediate: true)
// e registra sozinho, ao rodar, quais variáveis reativas ela leu —
// depois reexecuta sempre que qualquer uma delas mudar.
watchEffect(() => {
  console.log(`filtro atual → busca: "${busca.value}", categoria: "${categoriaFiltro.value}"`)
})
</script>
```

### 4.4 Parando um watcher

```vue
<script setup>
import { ref, watch } from 'vue'

const contador = ref(0)

// watch() e watchEffect() retornam uma função para PARAR de observar
const pararDeObservar = watch(contador, (valor) => {
  console.log('contador:', valor)
})

function pararObservacao() {
  pararDeObservar() // a partir daqui, mudanças em `contador` não disparam mais o log
}
</script>
```

| | `watch` | `watchEffect` |
|---|---|---|
| Declara a fonte explicitamente? | Sim — `watch(fonte, callback)` | Não — descobre sozinho lendo o corpo da função |
| Roda na criação, por padrão? | Não (a menos que `immediate: true`) | Sim, sempre |
| Acesso ao valor antigo? | Sim (`(novo, antigo) => ...`) | Não |
| Quando usar | Precisa saber o valor anterior, ou observar só uma fonte específica | Quer reagir a "qualquer coisa que a função usa", de forma mais enxuta |

> **📌 Na prova**
> Regra prática: se você precisa **de um valor derivado** para usar no template, use `computed`. Se precisa **fazer algo** (chamar API, gravar em disco, mostrar um alerta) quando um dado muda, use `watch` ou `watchEffect`.

## 5. `onMounted()` e carregamento de dados

Até agora, `eventos` nasce pronto, direto de um array local. Na prática, dados vêm de uma API ou arquivo remoto — e isso é assíncrono. O lugar certo para disparar essa busca é o hook `onMounted` (Aula 02), porque é aí que temos garantia de que o componente já existe.

### 5.1 O padrão dos três estados de tela

Toda tela que depende de dados assíncronos deveria tratar três situações:

1. **Carregando** — a requisição está em andamento.
2. **Erro** — a requisição falhou (rede caiu, servidor retornou erro).
3. **Vazio** — a requisição funcionou, mas não há dados para mostrar.

```vue
<!-- src/components/ListaEventosAssincrona.vue -->
<script setup>
import { ref, onMounted } from 'vue'

const eventos = ref([])
const carregando = ref(true)
const erro = ref(null)

async function carregarEventos() {
  carregando.value = true
  erro.value = null

  try {
    const resposta = await fetch('/eventos.json')

    if (!resposta.ok) {
      throw new Error(`Erro HTTP: ${resposta.status}`)
    }

    const dados = await resposta.json()
    eventos.value = dados
  } catch (erroCapturado) {
    erro.value = 'Não foi possível carregar os eventos. Tente novamente mais tarde.'
    console.error(erroCapturado)
  } finally {
    carregando.value = false
  }
}

onMounted(() => {
  carregarEventos()
})
</script>

<template>
  <div class="lista-eventos">
    <!-- estado 1: carregando -->
    <p v-if="carregando">Carregando eventos...</p>

    <!-- estado 2: erro -->
    <div v-else-if="erro" class="erro">
      <p>{{ erro }}</p>
      <button @click="carregarEventos">Tentar novamente</button>
    </div>

    <!-- estado 3: vazio (sem erro, sem carregar, mas sem itens) -->
    <p v-else-if="eventos.length === 0">Nenhum evento cadastrado no momento.</p>

    <!-- estado 4 (implícito): sucesso com dados -->
    <ul v-else>
      <li v-for="evento in eventos" :key="evento.id">{{ evento.titulo }}</li>
    </ul>
  </div>
</template>
```

Crie o arquivo de dados simulando uma API, em `public/eventos.json` (a pasta `public/` do Vite é servida como está, sem processamento):

```json
[
  {
    "id": 1,
    "titulo": "Semana da Computação",
    "categoria": "palestra",
    "dataHora": "2030-09-10T19:00:00",
    "local": "Auditório Central",
    "vagas": 40,
    "inscritos": 12
  },
  {
    "id": 2,
    "titulo": "Oficina de Vue.js",
    "categoria": "minicurso",
    "dataHora": "2030-08-20T14:00:00",
    "local": "Laboratório 3",
    "vagas": 25,
    "inscritos": 25
  },
  {
    "id": 3,
    "titulo": "Hackathon FACET",
    "categoria": "workshop",
    "dataHora": "2030-10-05T08:00:00",
    "local": "Bloco B",
    "vagas": 60,
    "inscritos": 18
  },
  {
    "id": 4,
    "titulo": "Introdução a IA",
    "categoria": "palestra",
    "dataHora": "2030-08-18T19:30:00",
    "local": "Auditório Central",
    "vagas": 80,
    "inscritos": 55
  }
]
```

> **💡 Dica**
> Para testar o estado de erro de propósito, troque a URL do `fetch` para algo que não existe (`/eventos-inexistente.json`) e veja a tela de erro com o botão "Tentar novamente" funcionando.

## 6. Formatação com `Intl` e ligação de classes/estilos

### 6.1 `Intl.DateTimeFormat` e `Intl.NumberFormat`

```vue
<script setup>
const dataEvento = new Date('2030-09-10T19:00:00')
const valorInscricao = 45.9

const dataFormatada = new Intl.DateTimeFormat('pt-BR', {
  day: '2-digit',
  month: 'long',
  year: 'numeric',
  hour: '2-digit',
  minute: '2-digit',
}).format(dataEvento)

const valorFormatado = new Intl.NumberFormat('pt-BR', {
  style: 'currency',
  currency: 'BRL',
}).format(valorInscricao)
</script>

<template>
  <p>Data: {{ dataFormatada }}</p>
  <!-- 10 de setembro de 2030 19:00 -->

  <p>Valor: {{ valorFormatado }}</p>
  <!-- R$ 45,90 -->
</template>
```

> **💡 Dica**
> Em vez de instanciar `Intl.DateTimeFormat`/`Intl.NumberFormat` de novo a cada uso, crie uma função utilitária reaproveitável (`src/utils/formatadores.js`) — é o que faremos na seção de "Mão na massa" a seguir.

> **🧠 Você sabia?**
> Antes do `Intl` ser amplamente suportado pelos navegadores (ele existe desde 2012, mas só ganhou adoção maciça depois), praticamente todo projeto JavaScript trazia uma biblioteca externa — a mais famosa era o **Moment.js** — só para formatar datas e números. O `Moment.js` foi oficialmente descontinuado em 2020, e a própria documentação recomenda migrar para as APIs nativas (`Intl`, `Temporal` no futuro) exatamente pelo que você acabou de fazer: nenhuma dependência, nenhum KB extra no bundle, formatação em português correta por padrão.

### 6.2 `:class` — objeto e array

```vue
<script setup>
import { ref, computed } from 'vue'

const evento = ref({ titulo: 'Oficina de Vue.js', vagas: 25, inscritos: 25 })

const estaLotado = computed(() => evento.value.inscritos >= evento.value.vagas)
</script>

<template>
  <!-- :class com OBJETO: cada chave é uma classe, o valor decide se ela é aplicada -->
  <div :class="{ 'card-lotado': estaLotado, 'card-disponivel': !estaLotado }">
    {{ evento.titulo }}
  </div>

  <!-- :class com ARRAY: combina classes fixas e condicionais -->
  <div :class="['card', estaLotado ? 'card-lotado' : 'card-disponivel']">
    {{ evento.titulo }}
  </div>

  <!-- misturando classe estática (sem :) com classe dinâmica (com :) -->
  <div class="card" :class="{ 'card-lotado': estaLotado }">
    {{ evento.titulo }}
  </div>
</template>

<style scoped>
.card {
  border: 1px solid #ccc;
  padding: 1rem;
}
.card-lotado {
  border-color: #c0392b;
  background-color: #fdecea;
}
.card-disponivel {
  border-color: #27ae60;
}
</style>
```

### 6.3 `:style`

```vue
<script setup>
import { ref, computed } from 'vue'

const vagas = ref(40)
const inscritos = ref(30)

const percentualOcupado = computed(() => Math.round((inscritos.value / vagas.value) * 100))
</script>

<template>
  <!-- :style com objeto -->
  <div
    class="barra-progresso"
    :style="{ width: percentualOcupado + '%', backgroundColor: percentualOcupado > 80 ? '#c0392b' : '#27ae60' }"
  ></div>

  <!-- :style com array de objetos: combina múltiplos conjuntos de estilo -->
  <p :style="[{ fontWeight: 'bold' }, { color: percentualOcupado > 80 ? 'red' : 'black' }]">
    {{ percentualOcupado }}% ocupado
  </p>
</template>

<style scoped>
.barra-progresso {
  height: 8px;
  border-radius: 4px;
  transition: width 0.3s ease;
}
</style>
```

## 🧩 Padrão de projeto em uso — Proxy (estrutural)

O padrão **Proxy** cria um objeto substituto que controla o acesso a outro objeto — interceptando leituras, escritas ou chamadas, e adicionando comportamento extra sem que quem usa o objeto perceba a diferença.

Um Proxy simplificado, em JavaScript puro, para logar todo acesso a um objeto:

```js
const evento = { titulo: 'Semana da Computação', vagas: 40 }

const eventoComLog = new Proxy(evento, {
  get(alvo, propriedade) {
    console.log(`[leitura] alguém acessou "${propriedade}"`)
    return alvo[propriedade]
  },
  set(alvo, propriedade, novoValor) {
    console.log(`[escrita] "${propriedade}" mudou de "${alvo[propriedade]}" para "${novoValor}"`)
    alvo[propriedade] = novoValor
    return true
  },
})

console.log(eventoComLog.titulo) // dispara o "get" -> loga e retorna o valor
eventoComLog.vagas = 39          // dispara o "set" -> loga e altera o valor real
```

**É exatamente este mecanismo que `reactive()` usa por dentro.** Quando você chama `reactive(objeto)`, o Vue devolve um `Proxy` que envolve o objeto original. Toda leitura de propriedade (`evento.titulo`) passa pelo `get` do Proxy, que registra "este trecho de template/computed depende de `titulo`" (o rastreamento de dependências que sustenta o padrão Observer da Aula 02). Toda escrita (`evento.vagas = 39`) passa pelo `set`, que dispara a notificação para quem depende daquele valor, disparando a re-renderização. `ref()` usa uma técnica um pouco diferente por baixo (um objeto com getter/setter na propriedade `.value`, sem precisar de um `Proxy` completo, já que só precisa interceptar uma única propriedade), mas o princípio — interceptar acesso para adicionar comportamento reativo — é o mesmo padrão **Proxy**.

## 💻 Mão na massa — UniEventos com filtros combinados

Vamos consolidar tudo em uma versão mais completa: busca por texto + categoria + "apenas com vagas", ordenação, contadores derivados, carregamento assíncrono no `onMounted` e destaque visual para eventos lotados ou que acontecem nos próximos 7 dias.

**Passo 1 — utilitário de formatação, reaproveitável em todo o projeto.**

```js
// src/utils/formatadores.js
export function formatarDataHora(dataIso) {
  return new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(dataIso))
}

export function formatarPercentual(valor) {
  return new Intl.NumberFormat('pt-BR', {
    style: 'percent',
    maximumFractionDigits: 0,
  }).format(valor / 100)
}

export function ocorreNosProximosDias(dataIso, dias) {
  const agora = new Date()
  const dataDoEvento = new Date(dataIso)
  const diferencaEmMs = dataDoEvento.getTime() - agora.getTime()
  const diferencaEmDias = diferencaEmMs / (1000 * 60 * 60 * 24)
  return diferencaEmDias >= 0 && diferencaEmDias <= dias
}
```

**Passo 2 — mantenha `public/eventos.json` da Seção 5.1** (ou ajuste as datas para ficarem próximas da data atual, se quiser testar o destaque de "próximos 7 dias").

**Passo 3 — o componente completo.**

```vue
<!-- src/App.vue -->
<script setup>
import { ref, computed, onMounted } from 'vue'
import { formatarDataHora, formatarPercentual, ocorreNosProximosDias } from './utils/formatadores.js'

const eventos = ref([])
const carregando = ref(true)
const erro = ref(null)

const busca = ref('')
const categoriaFiltro = ref('')
const apenasComVaga = ref(false)
const criterioOrdenacao = ref('data') // 'data' | 'vagas'

async function carregarEventos() {
  carregando.value = true
  erro.value = null

  try {
    const resposta = await fetch('/eventos.json')
    if (!resposta.ok) {
      throw new Error(`Erro HTTP: ${resposta.status}`)
    }
    eventos.value = await resposta.json()
  } catch (erroCapturado) {
    erro.value = 'Não foi possível carregar os eventos. Tente novamente mais tarde.'
    console.error(erroCapturado)
  } finally {
    carregando.value = false
  }
}

onMounted(() => {
  carregarEventos()
})

// computed principal: aplica os TRÊS filtros de uma vez, em cadeia
const eventosFiltrados = computed(() => {
  return eventos.value
    .filter((evento) => evento.titulo.toLowerCase().includes(busca.value.trim().toLowerCase()))
    .filter((evento) => categoriaFiltro.value === '' || evento.categoria === categoriaFiltro.value)
    .filter((evento) => !apenasComVaga.value || evento.inscritos < evento.vagas)
})

// computed encadeada: ordena o resultado já filtrado
const eventosOrdenados = computed(() => {
  const copia = [...eventosFiltrados.value]

  if (criterioOrdenacao.value === 'data') {
    return copia.sort((a, b) => new Date(a.dataHora) - new Date(b.dataHora))
  }

  // ordenar por vagas restantes, da maior para a menor
  return copia.sort((a, b) => (b.vagas - b.inscritos) - (a.vagas - a.inscritos))
})

// contadores derivados — cada um é barato de calcular porque
// eventosFiltrados já está em cache
const totalFiltrado = computed(() => eventosFiltrados.value.length)
const totalVagasLivres = computed(() =>
  eventosFiltrados.value.reduce((total, evento) => total + (evento.vagas - evento.inscritos), 0),
)

function vagasRestantes(evento) {
  return evento.vagas - evento.inscritos
}

function percentualOcupacao(evento) {
  return Math.round((evento.inscritos / evento.vagas) * 100)
}

function inscrever(eventoId) {
  const evento = eventos.value.find((item) => item.id === eventoId)
  if (!evento || evento.inscritos >= evento.vagas) return
  evento.inscritos++
}

function limparFiltros() {
  busca.value = ''
  categoriaFiltro.value = ''
  apenasComVaga.value = false
}
</script>

<template>
  <main class="pagina">
    <h1>UniEventos</h1>
    <p>Encontre e inscreva-se em eventos acadêmicos.</p>

    <!-- estado: carregando -->
    <p v-if="carregando">Carregando eventos...</p>

    <!-- estado: erro -->
    <div v-else-if="erro" class="erro">
      <p>{{ erro }}</p>
      <button @click="carregarEventos">Tentar novamente</button>
    </div>

    <!-- estado: sucesso -->
    <template v-else>
      <div class="filtros">
        <input v-model.trim="busca" type="text" placeholder="Buscar por título..." />

        <select v-model="categoriaFiltro">
          <option value="">Todas as categorias</option>
          <option value="palestra">Palestra</option>
          <option value="minicurso">Minicurso</option>
          <option value="workshop">Workshop</option>
        </select>

        <label>
          <input v-model="apenasComVaga" type="checkbox" />
          Apenas com vagas
        </label>

        <select v-model="criterioOrdenacao">
          <option value="data">Ordenar por data</option>
          <option value="vagas">Ordenar por vagas livres</option>
        </select>

        <button @click="limparFiltros">Limpar filtros</button>
      </div>

      <p class="resumo">
        {{ totalFiltrado }} evento(s) encontrado(s) — {{ totalVagasLivres }} vaga(s) livre(s) no total
      </p>

      <!-- estado: vazio (sucesso, mas sem itens após o filtro) -->
      <p v-if="eventosOrdenados.length === 0" class="vazio">
        Nenhum evento encontrado com estes filtros.
      </p>

      <ul v-else class="lista-eventos">
        <li
          v-for="evento in eventosOrdenados"
          :key="evento.id"
          class="card-evento"
          :class="{
            'card-lotado': vagasRestantes(evento) === 0,
            'card-em-breve': ocorreNosProximosDias(evento.dataHora, 7),
          }"
        >
          <h2>{{ evento.titulo }}</h2>
          <p>{{ formatarDataHora(evento.dataHora) }} — {{ evento.local }}</p>
          <p>Categoria: {{ evento.categoria }}</p>

          <p v-if="ocorreNosProximosDias(evento.dataHora, 7)" class="selo-em-breve">
            Acontece em breve!
          </p>

          <div class="barra-progresso-fundo">
            <div
              class="barra-progresso"
              :style="{
                width: percentualOcupacao(evento) + '%',
                backgroundColor: vagasRestantes(evento) === 0 ? '#c0392b' : '#27ae60',
              }"
            ></div>
          </div>
          <p class="texto-ocupacao">{{ formatarPercentual(percentualOcupacao(evento)) }} ocupado</p>

          <p v-if="vagasRestantes(evento) > 0">{{ vagasRestantes(evento) }} vaga(s) restante(s)</p>
          <p v-else class="lotado">Evento lotado</p>

          <button :disabled="vagasRestantes(evento) === 0" @click="inscrever(evento.id)">
            Inscrever-se
          </button>
        </li>
      </ul>
    </template>
  </main>
</template>

<style scoped>
.pagina {
  max-width: 780px;
  margin: 0 auto;
  padding: 2rem;
  font-family: sans-serif;
}

.filtros {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
  margin-bottom: 1rem;
}

.resumo {
  color: #555;
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

.card-lotado {
  border-color: #c0392b;
  background-color: #fdecea;
}

.card-em-breve {
  border-left: 4px solid #f39c12;
}

.selo-em-breve {
  color: #d68910;
  font-weight: bold;
}

.barra-progresso-fundo {
  background-color: #eee;
  border-radius: 4px;
  height: 8px;
  overflow: hidden;
  margin-top: 0.5rem;
}

.barra-progresso {
  height: 100%;
  transition: width 0.3s ease;
}

.texto-ocupacao {
  font-size: 0.85rem;
  color: #666;
}

.lotado {
  color: #c0392b;
  font-weight: bold;
}

.erro,
.vazio {
  text-align: center;
  color: #666;
}
</style>
```

> **📌 Na prova**
> Observe que `eventosFiltrados` e `eventosOrdenados` são duas computed **encadeadas**, e `totalFiltrado`/`totalVagasLivres` dependem de `eventosFiltrados`. Se você mudar `busca`, o Vue recalcula `eventosFiltrados` (porque ela lê `busca`), o que por sua vez invalida o cache de `eventosOrdenados`, `totalFiltrado` e `totalVagasLivres` — tudo automático, seguindo a cadeia de dependências. Você não escreve nenhuma chamada manual de "atualizar".

### Como testar

```bash
npm run dev
```

1. **Carregamento** — ao abrir a página, a mensagem de "carregando" aparece por um instante antes da lista: é o `onMounted` com o carregamento assíncrono simulado.
2. **Filtro e ordenação** — digitar na busca e trocar o critério de ordenação mudam a lista imediatamente, e os contadores (`totalFiltrado`, `totalVagasLivres`) acompanham.
3. **Cache da computed** — acrescente temporariamente um `console.log('recalculou')` na primeira linha de `eventosFiltrados` e recarregue: a mensagem aparece **uma vez por mudança de dependência**, não uma vez por leitura no template. Comparar com a Aula 02, em que a função era chamada três vezes por render, é o ponto da aula. Apague o `console.log` depois.
4. **Selo "em breve"** — só os eventos dentro dos próximos 7 dias mostram o selo, e a barra de ocupação fica vermelha quando não há mais vagas.
5. **Lista vazia** — uma busca sem resultado mostra a mensagem de vazio, não uma área em branco.

Resultado esperado: os cinco passam. Se a lista não reagir a uma mudança de `busca`, o suspeito é uma `computed` que esqueceu de **ler** a ref reativa dentro do corpo (uma dependência não lida nunca é rastreada).

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Preveja o que aparece no Console assim que a página carrega — **antes** de qualquer interação — usando o trecho abaixo da Seção 4.1:

```js
const categoriaFiltro = ref('')
watch(
  categoriaFiltro,
  (valor) => {
    console.log('categoria selecionada:', valor || '(nenhuma)')
  },
  { immediate: true },
)
```

Resultado esperado: `categoria selecionada: (nenhuma)` — porque `{ immediate: true }` executa o callback uma vez assim que o `watch` é criado, mesmo sem `categoriaFiltro` ainda ter mudado.

**A2.** Complete a linha que falta para resolver o antipadrão da Seção 2 — o `<template>` abaixo já foi corrigido para iterar sobre `eventosComVaga`, mas falta declarar essa `computed`:

```vue
<script setup>
import { ref, computed } from 'vue'

const eventos = ref([
  { id: 1, titulo: 'Semana da Computação', vagas: 40, inscritos: 40 },
  { id: 2, titulo: 'Oficina de Vue.js', vagas: 25, inscritos: 10 },
])

// complete aqui: computed que filtra os eventos com vaga disponível
</script>

<template>
  <li v-for="evento in eventosComVaga" :key="evento.id">{{ evento.titulo }}</li>
</template>
```

Resultado esperado: `const eventosComVaga = computed(() => eventos.value.filter((evento) => evento.inscritos < evento.vagas))`.

**A3.** Em uma frase: por que `watchEffect(() => { console.log(busca.value) })` não precisa declarar explicitamente qual variável está observando, enquanto `watch(busca, callback)` precisa apontar `busca`?

Resultado esperado: porque `watchEffect` executa a função imediatamente e registra sozinho, durante essa execução, quais variáveis reativas foram lidas — descobrindo as dependências automaticamente; `watch` exige a fonte explícita porque só reage a mudanças naquilo que você apontou.

**A4.** Ache o erro nas linhas abaixo — o valor mostrado na tela nunca muda, mesmo depois de chamar `inscrever()` várias vezes:

```js
let totalInscritos = 0

const resumo = computed(() => `Total de inscritos: ${totalInscritos}`)

function inscrever() {
  totalInscritos++
}
```

Resultado esperado: `totalInscritos` é uma variável comum (`let`), não reativa — o `computed` não tem como perceber que ela mudou, porque não é um `ref`/`reactive`. A correção troca `let totalInscritos = 0` por `const totalInscritos = ref(0)` e usa `totalInscritos.value++` dentro de `inscrever`.

**A5.** Preveja o valor de `percentualOcupado` e a cor do texto no trecho abaixo, para `vagas = 40` e `inscritos = 34`:

```js
const vagas = ref(40)
const inscritos = ref(34)
const percentualOcupado = computed(() => Math.round((inscritos.value / vagas.value) * 100))
```

```vue
<p :style="[{ fontWeight: 'bold' }, { color: percentualOcupado > 80 ? 'red' : 'black' }]">
  {{ percentualOcupado }}% ocupado
</p>
```

Resultado esperado: `85% ocupado`, com o texto em vermelho (`85 > 80`).

### Nível B — Aplicação

**B1.** Refatorar método em computed. Pegue esta função e transforme-a em `computed`:

```js
function eventosPalestrasComVaga() {
  return eventos.value.filter((e) => e.categoria === 'palestra' && e.inscritos < e.vagas)
}
```

Resultado esperado: uma constante `eventosPalestrasComVaga` criada com `computed(() => ...)`, usada no template sem parênteses (`v-for="evento in eventosPalestrasComVaga"`, não `eventosPalestrasComVaga()`).

<details markdown="1">
<summary>Dica</summary>

`const eventosPalestrasComVaga = computed(() => eventos.value.filter((e) => e.categoria === 'palestra' && e.inscritos < e.vagas))`
</details>

**B2.** Corrigir uma lista sem `:key`. Dado este trecho com um bug proposital, corrija-o:

```vue
<li v-for="evento in eventosOrdenados">{{ evento.titulo }}</li>
```

Resultado esperado: `:key="evento.id"` adicionado, e o console do navegador sem o aviso `Elements in iteration expect to have 'v-bind:key'`.

<details markdown="1">
<summary>Dica</summary>

Abra o DevTools (Console) — o Vue avisa explicitamente quando falta `:key` em um `v-for`.
</details>

**B3.** `watch` para persistir o filtro. Use `watch` sobre `categoriaFiltro` para gravar a categoria escolhida em `localStorage.setItem('ultimaCategoria', valor)`, e leia esse valor com `localStorage.getItem` para definir o valor inicial de `categoriaFiltro`.

Resultado esperado: recarregar a página mantém a última categoria filtrada.

<details markdown="1">
<summary>Dica</summary>

```js
const categoriaFiltro = ref(localStorage.getItem('ultimaCategoria') || '')
watch(categoriaFiltro, (valor) => localStorage.setItem('ultimaCategoria', valor))
```
</details>

**B4.** Estado de erro proposital. Troque a URL do `fetch` em `carregarEventos` para `/eventos-inexistente.json`, confirme que a tela de erro aparece com o botão "Tentar novamente", depois desfaça a mudança.

Resultado esperado: você reproduz e depois corrige o estado de erro descrito na Seção 5.

<details markdown="1">
<summary>Dica</summary>

O `catch` do `try/catch` precisa capturar tanto falha de rede quanto `resposta.ok === false`.
</details>

### Nível C — Desafio em sala

**C1.** Computed com getter e setter. Crie uma computed `buscaEmMaiusculas` que exiba `busca` sempre em maiúsculas ao ler, mas ao escrever converta para minúsculas antes de gravar em `busca`. Ligue essa computed a um segundo `<input>` (além do campo de busca normal) e prove que os dois campos ficam sincronizados nos dois sentidos.

Resultado esperado: digitar "VUE" no campo ligado a `buscaEmMaiusculas` faz `busca.value` valer `"vue"`; e alterar o campo de busca original (em minúsculas) atualiza o outro campo para a versão em maiúsculas, sem nenhum `watch` envolvido.

<details markdown="1">
<summary>Dica</summary>

```js
const buscaEmMaiusculas = computed({
  get: () => busca.value.toUpperCase(),
  set: (valor) => { busca.value = valor.toLowerCase() },
})
```

Ligue os dois campos com `v-model="busca"` e `v-model="buscaEmMaiusculas"` — a sincronia acontece porque os dois computeds/refs leem e escrevem a mesma fonte de verdade (`busca`).
</details>

## 🏆 Desafios

### ⭐ O `watch` que finge que está funcionando

Tags: vue, bug, investigacao

A store de filtros do seu colega usa um objeto `reactive` com `busca`, `categoria` e `apenasComVaga`, observado por um único `watch(filtros, callback)` (sem a opção da Seção 4.2). Ele jura que testou e "funcionava" — mas agora, ao mudar só a categoria no `<select>`, o callback simplesmente não dispara, e a preferência do usuário nunca é salva. Ache a causa e corrija.

**Critérios de pronto**

- Reproduzido: alterar `filtros.categoria` (uma propriedade interna do objeto) sem que o callback do `watch` rode — comprovado com um `console.log` que nunca aparece.
- Corrigido: alterar qualquer propriedade de `filtros` agora dispara o callback.
- Um comentário de 2 linhas no código explica por que um `watch` sobre um `reactive` não pega mudanças internas por padrão.
- Testado um caso extra: substituir o objeto inteiro (`Object.assign(filtros, { busca: 'x' })` vs. recriar a referência) e uma frase documentando se o comportamento muda.

<details markdown="1">
<summary>Pistas</summary>

1. Releia a Seção 4.2 — por padrão, `watch` em um objeto `reactive` só reage a uma troca de **referência**, não a uma mudança de propriedade interna.
2. A opção que falta é uma só, e o nome já sugere o que ela faz: "olhar fundo" no objeto.
3. Existe um custo em observar objetos grandes dessa forma — o Vue precisa varrer recursivamente todas as propriedades a cada checagem. Documente esse trade-off em uma frase.
</details>

### ⭐⭐ Quanto o `computed` realmente economiza?

Tags: performance, vue, refatoracao

A Seção 3 provou, com um `console.log`, que um `computed` roda uma vez só, mesmo usado três vezes no template. Mas quanto tempo isso realmente economiza quando a lista é grande? Meça com 5.000 eventos e descubra a partir de que escala a diferença passa a importar de verdade.

**Critérios de pronto**

- Um array `eventosGrandes` com 5.000 itens gerados por código (reaproveite o padrão de geração da Aula 01).
- Duas versões lado a lado do mesmo filtro combinado (texto + categoria + vaga): uma como **método comum**, chamado três vezes no template (resumo, contador, lista); outra como **computed**, usada nos mesmos três lugares.
- Tempo medido com `performance.now()` (ou a aba **Performance** do DevTools) de um ciclo de re-renderização completo em cada versão, com os números documentados em um comentário ou no README.
- Uma frase concluindo, com os números medidos, se a diferença é perceptível ao usuário nesta escala — e uma estimativa de a partir de quantos itens ela passaria a importar.

<details markdown="1">
<summary>Pistas</summary>

1. Para forçar uma re-renderização sem recarregar a página, altere qualquer `ref` usada no template (ex.: `busca.value += ' '` e depois volte) e meça o tempo entre a mudança e o próximo `console.log` dentro da função/computed.
2. `console.count('recalculando')` dentro da função ajuda a confirmar quantas vezes cada versão realmente roda por interação.
3. A aba **Performance** do DevTools grava um perfil de execução real — grave uma interação (digitar no campo de busca) nas duas versões e compare o tempo total de "Scripting".
</details>

### ⭐⭐⭐ Estados de carregamento no seu projeto autoral

Tags: vue, projeto, async

Leve todo o padrão desta aula — computed encadeadas, `watch` persistindo uma preferência, e os três estados de tela (carregando/erro/vazio) — para o domínio do seu projeto autoral.

**Critérios de pronto**

- O `App.vue` do seu projeto carrega dados via `fetch` dentro de `onMounted`, a partir de um JSON simulado em `public/`, implementando os três estados: carregando, erro (com botão de repetir) e vazio.
- Pelo menos duas `computed` encadeadas: uma filtra a lista, a outra deriva um total/resumo a partir da primeira (como `eventosFiltrados` → `totalVagasLivres` na Seção "Mão na massa").
- Um `watch` que persiste alguma preferência do usuário (o último filtro escolhido, o critério de ordenação) em `localStorage`, recuperada ao recarregar a página.
- Um destaque visual condicional (`:class` ou `:style`) usando `Intl` para formatar pelo menos um valor exibido.
- Prints em sequência (ou vídeo curto) demonstrando: carregamento normal, o erro forçado (URL errada) com o botão de repetir funcionando, e a preferência sobrevivendo a um `F5`.

<details markdown="1">
<summary>Pistas</summary>

1. Reaproveite a estrutura do Passo 3 da Seção "Mão na massa" — troque `eventos` pela entidade do seu domínio, campo por campo.
2. Para forçar o erro de propósito, troque a URL do `fetch` por um caminho inexistente, teste a tela de erro, depois desfaça.
3. `localStorage.getItem` retorna a string salva ou `null` — trate o caso "nunca salvo antes" com um valor padrão ao inicializar o `ref`.
</details>

## 🐛 Erros comuns e como resolver

| Sintoma | Causa | Solução |
|---|---|---|
| `computed` não atualiza quando eu esperava | A função do computed não lê nenhuma variável reativa (ex.: lê uma variável comum, não um `ref`/`reactive`) | Garanta que tudo que o computed depende é reativo |
| `v-for` com `v-if` no mesmo elemento gera erro ou resultado estranho | Antipadrão descrito na Seção 2 | Mova o filtro para um `computed` e itere sobre o resultado |
| `watch` não dispara ao mudar uma propriedade interna de um objeto | Faltou `{ deep: true }` ao observar um `reactive`/objeto | Adicione a opção `deep: true` |
| Tela fica presa em "Carregando eventos..." para sempre | Esqueceu de setar `carregando.value = false` no `finally`, ou uma exceção interrompeu antes de chegar lá | Sempre use `try/catch/finally`, com `carregando.value = false` no `finally` |
| Data aparece como `Invalid Date` | `dataIso` no formato errado, ou `new Date()` recebendo `undefined` | Confira o formato ISO (`YYYY-MM-DDTHH:mm:ss`) vindo do JSON |

## 🏠 Atividade assíncrona (1 h)

No repositório do seu projeto autoral:

1. Substitua a listagem estática do seu domínio por dados carregados via `fetch` dentro de `onMounted`, a partir de um arquivo em `public/<entidade>.json` (siga o modelo da Seção 5.1).
2. Implemente os três estados de tela: carregando, erro (com botão de tentar novamente) e vazio.
3. Transforme pelo menos uma função de filtro em `computed`, e combine dois ou mais critérios de filtro na mesma computed (texto + categoria/tipo, como fizemos hoje).
4. Adicione formatação de datas e/ou valores com `Intl` para os campos do seu domínio.
5. Adicione um destaque visual condicional (`:class`) para algum estado relevante do seu domínio (ex.: "esgotado", "últimas unidades", "encerra em breve").
6. Faça commit e push.

**Critério de pronto:** os três estados de tela funcionam (teste forçando um erro), os filtros combinados funcionam via `computed`, e existe pelo menos um destaque visual condicional.

## ✅ Checkpoint do projeto autoral

- [ ] Dados carregados via `fetch` dentro de `onMounted`, a partir de um JSON em `public/`.
- [ ] Estados de carregando, erro e vazio implementados e testados.
- [ ] Pelo menos um `computed` combinando dois ou mais critérios de filtro.
- [ ] Formatação de data e/ou valor com `Intl` aplicada em pelo menos um campo.
- [ ] Destaque visual condicional com `:class` em pelo menos um cenário do domínio.
- [ ] Todo `v-for` do projeto usa `:key` com um identificador estável (nunca o índice).
- [ ] Commit enviado ao GitHub.

Na próxima aula você vai reestruturar seu projeto com **Vuetify** e **Vue Router** — os filtros e listas que você já tem hoje continuam valendo, só ganham um visual pronto e navegação entre telas.

> **⚠️ Atenção**
> O prazo da **Avaliação 1** é publicado no SIGAA (veja também o quadro de avaliações em [`../nivel-3/#avaliacao`](../nivel-3/#avaliacao)), e as instruções completas — escopo, rubrica e formato de entrega — estão na **Aula 04**.

## 📚 Para aprofundar

- [Vue 3 — Computed Properties](https://vuejs.org/guide/essentials/computed.html)
- [Vue 3 — Watchers](https://vuejs.org/guide/essentials/watchers.html)
- [Vue 3 — List Rendering, seção "v-for with v-if"](https://vuejs.org/guide/essentials/list.html#v-for-with-v-if)
- [Vue 3 — Class and Style Bindings](https://vuejs.org/guide/essentials/class-and-style.html)
- [MDN — `Intl.DateTimeFormat`](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat)
- [MDN — `Intl.NumberFormat`](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat)
- [MDN — `Proxy`](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Global_Objects/Proxy)

---

**Próxima aula (04):** introdução a **Vuetify** e **Vue Router**, transformando o UniEventos em uma SPA navegável com componentes visuais prontos — e publicação das instruções completas da **Avaliação 1**.
