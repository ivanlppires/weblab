# Capítulo 10 — Qualidade, performance e observabilidade

> **Deploy & Ferramentas** · Unidade 3: Infraestrutura, automação e qualidade
> WebLab · curso aberto de desenvolvimento web
> **Tempo estimado:** 2 a 3 h · estudo autônomo, em paralelo à sua trilha

## 🎯 Objetivos de aprendizagem

Ao final deste capítulo você será capaz de:

- Configurar o ESLint 9 em *flat config* (`eslint.config.js`) para uma API Node e para um projeto Vue, e combiná-lo com o Prettier sem que um desfaça o trabalho do outro.
- Escrever e executar testes automatizados da API com **Vitest e supertest** — a mesma pilha da Aula 13 do Nível 3 —, incluindo um teste de integração que sobe o Express de verdade, e medir a cobertura.
- Escrever testes de componente e de store com o Vitest e o Vue Test Utils.
- Explicar as três métricas do Core Web Vitals (LCP, INP e CLS) e medir uma página publicada com o Lighthouse no DevTools, na linha de comando e no CI.
- Aplicar melhorias concretas de performance — imagens, fontes, divisão de código, cache e compressão no nginx — e comprovar o ganho com uma medição antes e depois.
- Instrumentar erros de produção com o SDK do Sentry (Node e navegador) e produzir logs estruturados com o pino, com rotação no servidor.
- Configurar monitoramento de disponibilidade e publicar `robots.txt` e `sitemap.xml` corretos.

## 📋 Pré-requisitos

- [ ] `unieventos-api` (Express 5) e `unieventos-web` (Vue 3 + Vite) rodando localmente, com `GET /health` respondendo `{ "status": "ok" }`.
- [ ] Os dois projetos publicados: o site em um endereço HTTPS e a API no Render ou no VPS com nginx (Capítulos 03, 05 e 06).
- [ ] Workflows do GitHub Actions funcionando no repositório (Capítulo 09).
- [ ] Node 22 LTS na máquina (`node -v`) e a API já com `vitest` e `supertest` instalados (Aula 13 do Nível 3); se ainda não estiverem, a §3.1 mostra o `npm install`.
- [ ] Uma conta de e-mail para criar contas gratuitas no Sentry e em um serviço de uptime.

> No Capítulo 09 o GitHub Actions passou a testar e publicar o projeto sozinho a cada push, e ficou uma pergunta em aberto — grande: **testar o quê?** Um pipeline que roda `npm test` sem nenhum teste escrito é um carimbo verde que não significa nada. Hoje você preenche esse vazio com quatro instrumentos — linter, testes, Lighthouse e observabilidade — e transforma "o código está bom", "o site parece rápido" e "acho que está no ar" em números que você consegue mostrar para outra pessoa: medição de performance com valor antes e depois, e um painel que avisa quando a produção quebra. Este é o último capítulo técnico da trilha; o próximo trata de usar assistentes de IA sem terceirizar o seu aprendizado.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Por que medir; ESLint 9 flat config e Prettier nos dois projetos; scripts npm de qualidade |
| 2 | 50 min | Testes de API e de componente com Vitest; Core Web Vitals; Lighthouse no DevTools, na CLI e no CI |
| 3 | 50 min | Melhorias de performance com medição antes/depois; Sentry, pino, uptime, `robots.txt` e `sitemap.xml` |

## 1. Qualidade não é opinião

"O código está bom" e "o site está rápido" são frases sem valor até virarem número. Quatro instrumentos cobrem quatro perguntas diferentes, e é comum confundi-los:

| Instrumento | Pergunta que responde | Quando roda |
|---|---|---|
| Linter (ESLint) | O código tem erro ou mau hábito **sem precisar executá-lo**? | Ao digitar, ao salvar, no CI |
| Testes (Vitest, supertest) | O código faz o que eu disse que faz? | Antes de cada commit e no CI |
| Lighthouse / Core Web Vitals | A página é rápida e utilizável para quem acessa? | Em cada publicação |
| Observabilidade (Sentry, pino, uptime) | O que está acontecendo **agora**, na produção? | O tempo todo, sem você pedir |

Repare no que cada um **não** faz. O linter não sabe se a sua conta está errada; sabe que você declarou uma variável e não usou. O teste não sabe se o site é lento. O Lighthouse mede a página no seu laboratório, com rede simulada — não mede o usuário real no 4G de Sinop. E a observabilidade não previne erro nenhum: conta que o erro aconteceu, para quem e com qual entrada.

Um detalhe que separa quem programa há um mês de quem programa há um ano: **os quatro são baratos de instalar e caros de instalar tarde**. Configurar ESLint em um projeto de 40 arquivos leva dez minutos e gera três avisos; em um de 400 arquivos, gera oitocentos avisos e vira um dia de trabalho que ninguém quer fazer.

> **🧠 Você sabia?**
> O Node passou a ter **executor de testes embutido**: o módulo `node:test`, estável desde a linha 20. Antes disso, todo projeto Node precisava de uma biblioteca externa (Mocha, Jest, AVA, Tape) e arrastava dezenas de dependências só para escrever um `assert`. Hoje `node --test` roda um arquivo de teste sem nenhum `npm install`. A trilha continua usando o Vitest na API — porque é ele que o Nível 3 instalou e é o mesmo executor do front —, mas saber que o runner nativo existe muda a resposta para "vale a pena testar este script de 40 linhas?".

## 2. ESLint 9 e Prettier

### 2.1 O que o linter faz

O ESLint lê o seu JavaScript, monta a árvore sintática do arquivo e aplica **regras**. Cada regra tem um nível: `off`, `warn` (aparece, não quebra o build) ou `error` (quebra). Ele pega três famílias de problema: erros que só apareceriam em produção (`no-undef`, `no-unreachable`, `no-dupe-keys`), maus hábitos (`no-var`, `eqeqeq`, `prefer-const`) e convenções de biblioteca (o plugin do Vue avisa quando falta `:key` em um `v-for`). O que ele **não** pega: lógica errada, senha no código, consulta SQL lenta. Linter é o primeiro filtro, não o único.

A versão 9 abandonou o `.eslintrc` com `extends` em cascata e adotou o **flat config**: um único `eslint.config.js` que exporta um **array de objetos de configuração**, aplicados de cima para baixo — o último que fala sobre uma regra vence. Não há mais herança mágica de pastas superiores, e cada objeto pode se limitar a certos arquivos com `files`.

### 2.2 Na API

```bash
cd ~/weblab/unieventos-api
npm install --save-dev eslint @eslint/js globals prettier eslint-config-prettier
```

`unieventos-api/eslint.config.js`

```js
import js from '@eslint/js'
import globals from 'globals'
import prettier from 'eslint-config-prettier'

export default [
  // Um objeto só com "ignores" vale para o projeto inteiro.
  { ignores: ['node_modules/', 'coverage/', 'dist/'] },

  js.configs.recommended,

  {
    files: ['**/*.js'],
    languageOptions: {
      ecmaVersion: 2024,
      sourceType: 'module',
      globals: { ...globals.node },
    },
    rules: {
      'no-var': 'error',
      'prefer-const': 'error',
      eqeqeq: ['error', 'always'],
      'no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      'no-console': ['warn', { allow: ['error'] }],
    },
  },

  { files: ['tests/**/*.js'], rules: { 'no-console': 'off' } },

  // Desliga toda regra que brigaria com o Prettier. PRECISA ser o último item.
  prettier,
]
```

Três decisões merecem explicação. `globals.node` informa que `process`, `console` e `URL` existem — sem isso, `no-undef` reclama de tudo (no front o equivalente é `globals.browser`). `argsIgnorePattern: '^_'` permite escrever `(erro, req, res, _next)` no middleware de erro do Express 5 sem que o `_next`, obrigatório na assinatura e inútil no corpo, vire erro. E `'no-console': 'warn'` é um lembrete: na §7 os `console.log` da API viram chamadas ao pino.

### 2.3 No front Vue

```bash
cd ~/weblab/unieventos-web
npm install --save-dev eslint @eslint/js globals eslint-plugin-vue prettier eslint-config-prettier
```

`unieventos-web/eslint.config.js`

```js
import js from '@eslint/js'
import pluginVue from 'eslint-plugin-vue'
import globals from 'globals'
import prettier from 'eslint-config-prettier'

export default [
  { ignores: ['node_modules/', 'dist/', 'coverage/'] },
  js.configs.recommended,

  // O preset do Vue já configura o parser de arquivos .vue (vue-eslint-parser).
  ...pluginVue.configs['flat/recommended'],

  {
    files: ['**/*.{js,vue}'],
    languageOptions: { ecmaVersion: 2024, sourceType: 'module', globals: { ...globals.browser } },
    rules: {
      // As telas do UniEventos se chamam Eventos.vue, Login.vue…
      'vue/multi-word-component-names': 'off',
      'no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    },
  },

  prettier,
]
```

Repare nos três pontos de `...pluginVue.configs['flat/recommended']`: o preset é um **array** de configurações, e o espalhamento coloca cada uma como item do array externo. Sem eles, o ESLint recebe um array dentro do array e falha ao carregar.

### 2.4 Prettier: quem decide a forma

O ESLint sabe formatar, mas formatar não é trabalho dele. A divisão que o mercado adotou é: **Prettier decide a forma, ESLint decide o conteúdo**. Repita o `.prettierrc` do Capítulo 01 na raiz de cada projeto e acrescente um `.prettierignore` com `node_modules`, `coverage`, `dist` e `package-lock.json`. O pacote `eslint-config-prettier`, importado como último item do array, **desliga** as regras de estilo do ESLint (indentação, aspas, vírgula final) que apontariam erro exatamente no formato que o Prettier acabou de aplicar — você já viu esse conflito se algum dia salvou um arquivo e o viu ser formatado e sublinhado de vermelho ao mesmo tempo.

Com tudo no lugar, o `package.json` da API ganha os scripts de qualidade:

`unieventos-api/package.json` (seção `scripts`)

```json
{
  "scripts": {
    "dev": "node --watch --env-file=.env src/server.js",
    "start": "node src/server.js",
    "lint": "eslint . --max-warnings=0",
    "lint:corrigir": "eslint . --fix",
    "formatar": "prettier --write .",
    "formatar:conferir": "prettier --check .",
    "test": "vitest run",
    "test:observar": "vitest",
    "test:cobertura": "vitest run --coverage",
    "qualidade": "npm run lint && npm run formatar:conferir && npm test"
  }
}
```

`npm run qualidade` é o comando que você roda antes de abrir um pull request — e é exatamente o que o CI vai rodar. Quando os dois são o mesmo comando, ninguém é surpreendido pelo robô. O `--fix` resolve o mecânico (aspas, `let` que podia ser `const`) e deixa para você o que exige decisão: uma variável não usada pode ser lixo ou pode ser um bug.

> **🔎 Por baixo do capô**
> O `&&` entre os scripts não é decoração: ele encadeia processos e para no primeiro que devolver código de saída diferente de zero. Todo comando de terminal devolve esse código, e é assim que o GitHub Actions decide se um step passou. Teste: rode `npm run lint` em um projeto com erro e depois `echo $?` — vai imprimir `1`. Depois de um comando bem-sucedido, `0`.

> **⚠️ Atenção**
> A extensão ESLint do VS Code usa o `eslint.config.js` da **pasta aberta no editor**. Se você abrir uma pasta que contém `unieventos-web` e `unieventos-api` lado a lado, ela procura um único arquivo na raiz e não acha nenhum dos dois. Abra um projeto por janela.

## 3. Testes da API com Vitest e supertest

### 3.1 O que testar quando o tempo é curto

A pilha de testes da API é a mesma desde a Aula 13 do Nível 3 — **Vitest** como executor e **supertest** para bater nas rotas —, e é a mesma do front (§4): um executor só para o projeto inteiro, uma configuração só, um `npm test` só. Se a sua API ainda não tem os dois:

```bash
cd ~/weblab/unieventos-api
npm install --save-dev vitest supertest @vitest/coverage-v8
```

> **💡 Dica**
> Para projetos sem dependência nenhuma — um script de manutenção, um utilitário de linha de comando —, o Node 22 traz um runner embutido: `import { describe, it } from 'node:test'`, `import assert from 'node:assert/strict'` e `node --test` para executar, sem `npm install`. A API da trilha fica no Vitest (é o que o Nível 3 instalou e o que o front usa), mas o `node:test` é a alternativa certa quando adicionar uma devDependency não compensa.

Você não vai testar tudo, e não precisa. A ordem que rende mais por hora investida: primeiro as **funções puras com regra de negócio** (paginação, cálculo de vagas, validação, normalização de texto) — baratas de testar e onde moram os bugs sutis; depois as **rotas da API pelo contrato** (o `GET` devolve 200 e um array? o `POST` sem título devolve 400 com mensagem?), que pegam quase todo erro de integração; e sempre a regra de ouro: **todo bug corrigido vira um teste** — antes de arrumar, escreva o teste que falha por causa dele.

O que não vale a pena no nosso tamanho: testar `getters` triviais, testar bibliotecas de terceiros e testar telas ponta a ponta (isso exige Playwright ou Cypress).

### 3.2 Teste de unidade

`unieventos-api/src/util/paginacao.js`

```js
/** Recorta uma lista em páginas. Sempre devolve uma página válida, mesmo com entrada absurda. */
export function paginar(lista, pagina = 1, porPagina = 10) {
  const total = lista.length
  const paginas = Math.max(1, Math.ceil(total / porPagina))
  const atual = Math.min(Math.max(1, Number(pagina) || 1), paginas)
  const inicio = (atual - 1) * porPagina
  return { itens: lista.slice(inicio, inicio + porPagina), total, pagina: atual, paginas }
}
```

O teste vive em `tests/`, com a terminação `.test.js` — um dos padrões que o Vitest encontra sozinho:

`unieventos-api/tests/paginacao.test.js`

```js
import { describe, it, expect } from 'vitest'
import { paginar } from '../src/util/paginacao.js'

const trinta = Array.from({ length: 30 }, (_, i) => ({ id: i + 1 }))

describe('paginar', () => {
  it('devolve os 10 primeiros itens na página 1', () => {
    const r = paginar(trinta, 1, 10)
    expect(r.itens).toHaveLength(10)
    expect(r.itens[0].id).toBe(1)
    expect(r.paginas).toBe(3)
    expect(r.total).toBe(30)
  })

  it('trata lista vazia sem quebrar', () => {
    const r = paginar([], 5, 10)
    expect(r.itens).toEqual([])
    expect(r.pagina).toBe(1)
    expect(r.paginas).toBe(1)
  })

  it('grampeia páginas fora do intervalo e entradas inválidas', () => {
    expect(paginar(trinta, 99, 10).pagina).toBe(3)
    expect(paginar(trinta, 'abacaxi', 10).pagina).toBe(1)
  })
})
```

`toBe` compara com `Object.is` (na prática, `===`) e `toEqual` compara estruturas campo a campo. Prefira sempre a comparação estrita: em um `expect('1').toEqual(1)` o teste falha, e é isso que você quer — um teste que passa por engano é pior do que nenhum teste.

### 3.3 Teste de integração da rota

Este vale por dez: o supertest sobe o Express de verdade em uma porta livre, faz uma requisição HTTP real e derruba tudo no fim, sem você administrar servidor nem porta. Ele exige que `src/app.js` **exporte o app** sem chamar `listen` — a separação que a `unieventos-api` já tem desde o Nível 3 (`export const app`), e que existe justamente para isto; quem chama `listen` é o `src/server.js`.

`unieventos-api/tests/eventos.test.js`

```js
import { describe, it, expect } from 'vitest'
import request from 'supertest'
import { app } from '../src/app.js'

describe('GET /api/eventos', () => {
  it('responde 200, JSON e uma lista', async () => {
    const resposta = await request(app).get('/api/eventos')

    expect(resposta.status).toBe(200)
    expect(resposta.headers['content-type']).toMatch(/application\/json/)
    expect(Array.isArray(resposta.body.itens)).toBe(true)
  })
})

describe('POST /api/eventos', () => {
  it('recusa evento sem título com 400 e mensagem', async () => {
    const resposta = await request(app)
      .post('/api/eventos')
      .send({ local: 'Anfiteatro' })

    expect(resposta.status).toBe(400)
    expect(resposta.body.erro).toMatch(/t[íi]tulo/i)
  })
})
```

O `request(app)` abre um servidor em uma porta efêmera, dispara a requisição e fecha tudo sozinho — testes nunca devem brigar por porta fixa. Quatro asserções cobrem o contrato inteiro de uma rota: código de status, tipo de conteúdo, formato do corpo e comportamento com entrada errada.

### 3.4 Executando e medindo cobertura

```bash
npx vitest run                     # roda tudo que parece teste e sai
npx vitest                         # modo interativo: reexecuta ao salvar
npx vitest run -t "paginar"        # só os testes cujo nome bate
npx vitest run --coverage          # com relatório de cobertura
```

`vitest run` executa uma vez e sai — é a forma que o CI precisa, porque o modo interativo nunca terminaria. A cobertura sai em tabela no fim, com a porcentagem de linhas, ramos e funções por arquivo e as linhas não cobertas. Use-a como **mapa**, não como meta: 100 % com asserções fracas não prova nada, e 60 % nas rotas certas já protege o essencial.

> **🔬 Investigue**
> Rode `npm run test:cobertura` na sua API e olhe a coluna de linhas não cobertas do arquivo de rotas. Escolha **uma** linha não coberta que trate erro (um `if` de validação, um `catch`) e escreva o teste que a executa. Rode de novo e veja a porcentagem subir. Cronometre: quase sempre são menos de cinco minutos por teste — e essa é a resposta para "não tenho tempo de testar".

## 4. Testes de componente com Vitest

No front o executor é o mesmo — **Vitest** —, mas a configuração muda: ele reaproveita a do Vite (aliases, plugins, variáveis de ambiente) e precisa de um DOM de mentira para montar componentes Vue.

```bash
cd ~/weblab/unieventos-web
npm install --save-dev vitest @vue/test-utils jsdom @vitest/coverage-v8
```

`unieventos-web/vitest.config.js`

```js
import { fileURLToPath } from 'node:url'
import { mergeConfig, defineConfig, configDefaults } from 'vitest/config'
import viteConfig from './vite.config.js'

export default mergeConfig(
  viteConfig,
  defineConfig({
    test: {
      // jsdom simula document/window dentro do Node: é o "navegador de mentira".
      environment: 'jsdom',
      globals: true,
      setupFiles: ['./vitest.setup.js'],
      exclude: [...configDefaults.exclude, 'e2e/**'],
      root: fileURLToPath(new URL('./', import.meta.url)),
    },
  }),
)
```

`unieventos-web/vitest.setup.js`

```js
// O Vuetify observa o tamanho dos elementos; o jsdom não implementa ResizeObserver.
// Sem este substituto, montar qualquer componente Vuetify quebra com ReferenceError.
global.ResizeObserver = class {
  observe() {}
  unobserve() {}
  disconnect() {}
}
```

`unieventos-web/src/components/__tests__/EventoCard.spec.js`

```js
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import EventoCard from '../EventoCard.vue'

const vuetify = createVuetify({ components, directives })

function montar(evento) {
  return mount(EventoCard, { global: { plugins: [vuetify] }, props: { evento } })
}

describe('EventoCard', () => {
  it('mostra o título e o local do evento', () => {
    const wrapper = montar({ id: 1, titulo: 'Semana Acadêmica', local: 'Anfiteatro', vagas: 30 })
    expect(wrapper.text()).toContain('Semana Acadêmica')
    expect(wrapper.text()).toContain('Anfiteatro')
  })

  it('desabilita a inscrição quando não há vagas', () => {
    const wrapper = montar({ id: 2, titulo: 'Oficina de Cafés', local: 'Lab 3', vagas: 0 })
    expect(wrapper.get('button').attributes('disabled')).toBeDefined()
  })

  it('emite "inscrever" com o id ao clicar', async () => {
    const wrapper = montar({ id: 7, titulo: 'Palestra', local: 'Auditório', vagas: 5 })
    await wrapper.get('button').trigger('click')
    expect(wrapper.emitted('inscrever')[0]).toEqual([7])
  })
})
```

Uma store da Pinia se testa do mesmo jeito, sem rede: `setActivePinia(createPinia())` em um `beforeEach` (cada teste precisa começar com estado limpo), depois atribua `store.eventos` na mão e verifique os *getters*. É o teste mais barato do front e pega quase todo erro de filtro e de total.

Scripts do front: `"test:unit": "vitest run"`, `"test:observar": "vitest"`, `"test:cobertura": "vitest run --coverage"` e um `qualidade` encadeando lint, formatação e testes. O `vitest` sem argumento entra em modo interativo e reexecuta ao salvar; `vitest run` executa uma vez e sai — é a forma que o CI precisa, porque o modo interativo nunca terminaria.

## 5. Core Web Vitals e Lighthouse

### 5.1 As três métricas

O Google padronizou três medidas de experiência real, os **Core Web Vitals**, escolhidas porque respondem a três perguntas que o usuário faz sem perceber:

| Métrica | Pergunta do usuário | Bom / Ruim |
|---|---|---|
| **LCP** (Largest Contentful Paint) | "Já carregou?" — quando o maior elemento visível aparece | ≤ 2,5 s / > 4,0 s |
| **INP** (Interaction to Next Paint) | "Está travado?" — quanto a página demora a reagir a um clique | ≤ 200 ms / > 500 ms |
| **CLS** (Cumulative Layout Shift) | "Por que o botão fugiu?" — quanto o conteúdo pula durante a carga | ≤ 0,1 / > 0,25 |

Os limites valem para o **percentil 75** dos carregamentos: três de cada quatro visitas precisam ficar na faixa boa. O INP substituiu o antigo FID, que media só o atraso da *primeira* interação — um número fácil de acertar e que escondia páginas travadas do segundo clique em diante.

Há duas fontes de dado, bem diferentes. **Laboratório:** o Lighthouse roda a página na sua máquina, com CPU e rede simuladas — reproduzível, imediato e não representa ninguém em particular. **Campo:** medições de visitantes reais; o PageSpeed Insights mostra os dados do CrUX quando o site tem tráfego suficiente, o que provavelmente não é o caso do seu projeto de estudo (para coletar os seus, use a biblioteca `web-vitals`). O Lighthouse não consegue medir INP em laboratório — não há usuário clicando — e usa o **TBT** (*Total Blocking Time*) como aproximação; a nota de 0 a 100 é uma média ponderada em que TBT, LCP e CLS pesam mais, e por isso um site com JavaScript pesado perde pontos mesmo pintando rápido.

> **🧠 Você sabia?**
> A pontuação de performance do Lighthouse é comparativa: posiciona o seu site em uma curva construída a partir de milhões de páginas reais. Por isso ela é implacável na faixa alta — sair de 90 para 95 costuma dar mais trabalho do que sair de 40 para 70. E por isso a nota **varia entre execuções** na mesma página: rede, CPU disponível e até uma extensão do navegador mudam o resultado. Rode três vezes e use a mediana; o Lighthouse CI faz isso por você.

### 5.2 Medindo de três formas

**No DevTools:** aba **Lighthouse** → *Mobile* → **Analyze page load**. Bom para explorar, porque cada item reprovado abre com explicação e lista de arquivos.

**Na linha de comando**, que é o que permite guardar um relatório e comparar depois:

```bash
npx lighthouse@latest https://eventos.seudominio.dev \
  --only-categories=performance,accessibility,best-practices,seo \
  --output=html --output=json --output-path=./relatorios/antes \
  --chrome-flags="--headless" --quiet
```

Isso grava `relatorios/antes.report.html` (para abrir no navegador) e `antes.report.json` (para extrair números). Sem `--preset=desktop`, o Lighthouse simula um celular mediano com rede lenta — que é o cenário certo para a maioria de quem acessa pela primeira vez.

**No CI**, com o Lighthouse CI, que roda várias vezes, tira a mediana e **reprova o build** se a nota cair:

`unieventos-web/lighthouserc.json`

```json
{
  "ci": {
    "collect": {
      "startServerCommand": "npm run preview",
      "url": ["http://localhost:4173/", "http://localhost:4173/eventos"],
      "numberOfRuns": 3
    },
    "assert": {
      "preset": "lighthouse:no-pwa",
      "assertions": {
        "categories:performance": ["error", { "minScore": 0.9 }],
        "categories:accessibility": ["error", { "minScore": 0.9 }]
      }
    },
    "upload": { "target": "temporary-public-storage" }
  }
}
```

```bash
npm install --save-dev @lhci/cli
npm run build
npx lhci autorun
```

O `autorun` sobe o servidor de preview, roda o Lighthouse três vezes em cada URL, compara com as asserções e imprime um link público temporário para o relatório. No GitHub Actions vira um workflow:

`.github/workflows/qualidade.yml`

```yaml
name: qualidade

on:
  push:
    branches: [main]
  pull_request:

jobs:
  verificar:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: npm
      - run: npm ci
      - run: npm run lint
      - run: npm run formatar:conferir
      - run: npm run test:unit
      - run: npm run build
      - run: npx lhci autorun
```

## 6. Sete melhorias que mudam o número

Não adianta otimizar no escuro. A ordem abaixo é a que mais rende em projetos do nosso tamanho, e cada item diz qual métrica ele move.

**1. Dimensione e converta as imagens (LCP).** Uma foto de 3000 px exibida em uma caixa de 600 px transfere nove vezes mais bytes do que precisa. Redimensione para o dobro da largura de exibição (por causa das telas de alta densidade), converta para WebP ou AVIF e sirva com `<picture>`:

`unieventos-web/src/components/Hero.vue` (trecho do template)

```html
<picture>
  <source srcset="/img/hero-1200.avif" type="image/avif" />
  <source srcset="/img/hero-1200.webp" type="image/webp" />
  <img
    src="/img/hero-1200.jpg"
    alt="Estudantes na abertura da Semana Acadêmica"
    width="1200"
    height="600"
    fetchpriority="high"
  />
</picture>
```

**2. Declare `width` e `height` em toda imagem (CLS).** Sem elas o navegador reserva zero altura, pinta o texto e empurra tudo para baixo quando a imagem chega. Os atributos não fixam o tamanho visual (o CSS continua mandando com `width: 100%; height: auto`); informam a **proporção**, e o navegador reserva o espaço certo.

**3. `loading="lazy"` fora da dobra, nunca na imagem do LCP.** Imagens que só aparecem depois de rolar ganham `loading="lazy"`; a principal do topo recebe o oposto, `fetchpriority="high"` e nenhum `lazy`. Adiar a imagem do LCP é o erro de otimização mais comum — piora justamente a métrica que você queria melhorar.

**4. Controle as fontes (LCP e CLS).** Fonte externa bloqueia texto. No `<head>`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet" />
```

O `display=swap` manda mostrar o texto imediatamente com a fonte de sistema e trocar quando a personalizada chegar. Melhor ainda: baixe os `.woff2` para `public/fontes/`, declare `@font-face` com `font-display: swap` e um `<link rel="preload" as="font" crossorigin>` — some duas conexões externas e um risco a menos de indisponibilidade.

**5. Divida o JavaScript por rota (TBT/INP).** No Vue Router, troque a importação estática pela dinâmica: o Vite gera um arquivo por rota e o navegador só baixa a tela que o usuário abriu.

`unieventos-web/src/router/index.js`

```js
import { createRouter, createWebHistory } from 'vue-router'
import Inicio from '../views/Inicio.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // A tela inicial vem no pacote principal: é sempre a primeira a abrir.
    { path: '/', name: 'inicio', component: Inicio },
    // As demais viram arquivos separados, baixados sob demanda.
    { path: '/eventos', name: 'eventos', component: () => import('../views/Eventos.vue') },
    { path: '/eventos/:id', name: 'evento', component: () => import('../views/Evento.vue') },
    { path: '/admin', name: 'admin', component: () => import('../views/Admin.vue') },
  ],
})

export default router
```

Rode `npm run build` antes e depois: a saída do Vite lista o tamanho de cada arquivo gerado, e você vê o pacote principal encolher.

**6. Cabeçalhos de cache no nginx (visitas seguintes).** O Vite coloca um hash no nome de cada arquivo gerado (`index-B7fK2p.js`). Como o nome muda sempre que o conteúdo muda, esses arquivos podem ser guardados por um ano sem risco. O `index.html`, que aponta para eles, não pode ser guardado nunca.

`/etc/nginx/sites-available/unieventos` (trecho do `server`)

```nginx
location ~* \.(?:js|css|woff2|png|jpg|jpeg|webp|avif|svg|ico)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    access_log off;
}

location = /index.html {
    add_header Cache-Control "no-cache";
}
```

**7. Compressão (todas as métricas de rede).** Texto comprime muito: um pacote de 300 KB costuma virar 90 KB com gzip.

`/etc/nginx/nginx.conf` (dentro do bloco `http`)

```nginx
gzip on;
gzip_vary on;
gzip_comp_level 5;
gzip_min_length 256;
gzip_proxied any;
gzip_types text/plain text/css text/xml application/javascript application/json application/xml image/svg+xml;
```

`text/html` não entra na lista porque o nginx sempre o comprime. Não comprima imagens: JPEG, PNG e WebP já são formatos comprimidos, e passar gzip neles gasta CPU para economizar quase nada. O **Brotli** comprime cerca de 15 % melhor em texto, mas não vem no nginx padrão: depende do módulo `ngx_brotli`, que algumas distribuições empacotam e outras exigem compilar. Se a sua não tem, siga com gzip. Em Netlify, Vercel, Cloudflare Pages e GitHub Pages a compressão já vem ligada e negociada automaticamente.

```bash
sudo nginx -t && sudo systemctl reload nginx
curl -sI -H 'Accept-Encoding: gzip, br' https://eventos.seudominio.dev/assets/index.js | grep -i -E 'content-encoding|cache-control'
```

> **🔬 Investigue**
> Rode o `curl` acima em três sites: o seu, o do WebLab e o portal da sua universidade ou escola. Compare `content-encoding` e `cache-control`. Depois, no DevTools → Network, clique em um arquivo `.js` e compare **Size** (o que trafegou) com o tamanho descomprimido: a razão entre os dois é a taxa de compressão. Qual dos três comprime melhor?

## 7. Observabilidade: Sentry e pino

### 7.1 Erros de produção

Em produção o `console.log` da API vai para um arquivo que ninguém lê, e o `console.error` do navegador morre no computador do usuário. Você fica sabendo do erro quando alguém reclama — se reclamar. Uma ferramenta de rastreamento inverte isso: o erro chega até você com pilha de chamadas, navegador, rota e quantas pessoas foram atingidas.

O **Sentry** tem plano gratuito suficiente para projetos de estudo. Crie a conta, crie dois projetos (um `node` e um `vue`) e guarde os dois **DSN** — a URL que identifica o projeto para onde os eventos são enviados.

```bash
cd ~/weblab/unieventos-api
npm install @sentry/node
```

O SDK precisa ser inicializado **antes de qualquer outro import**, porque instrumenta os módulos na hora em que são carregados. Por isso ele mora em um arquivo separado, carregado pelo Node antes do programa:

`unieventos-api/instrument.js`

```js
import * as Sentry from '@sentry/node'

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV ?? 'development',
  release: process.env.APP_VERSION ?? 'dev',
  // Fração das requisições que vira "trace" de performance. 0.1 = 10 %.
  tracesSampleRate: 0.1,
  // Não envie IP, cookies nem corpo de requisição por padrão (LGPD).
  sendDefaultPii: false,
  // Sem DSN configurado, o SDK fica inerte — ótimo para rodar testes localmente.
  enabled: Boolean(process.env.SENTRY_DSN),
})
```

No `package.json`, o script `start` passa a carregá-lo: `"start": "node --import ./instrument.js src/server.js"`. O `--import` executa o módulo antes do arquivo principal e é a forma recomendada com módulos ES. Depois de registrar todas as rotas, e **antes** do seu middleware de erro:

`unieventos-api/src/app.js` (trecho final)

```js
// Captura as exceções que escaparem das rotas; vem ANTES do seu middleware de erro.
Sentry.setupExpressErrorHandler(app)

app.use((erro, req, res, _next) => {
  const status = erro.status ?? 500
  // Por enquanto, console.error; na §7.2 o pino-http cria req.log e esta
  // linha vira req.log.error({ err: erro }, 'erro não tratado').
  console.error('erro não tratado', erro)
  res.status(status).json({ erro: status === 500 ? 'Erro interno' : erro.message })
})
```

Lembre do Express 5: erros lançados dentro de handlers `async` vão automaticamente para o middleware de erro, sem `.catch(next)` — o que significa que o Sentry vê **todos** eles. Para algo que você tratou mas quer acompanhar, use `Sentry.captureException(erro, { tags: { etapa: 'email-confirmacao' } })`.

No front:

`unieventos-web/src/main.js` (trecho)

```js
import * as Sentry from '@sentry/vue'

const app = createApp(App)

Sentry.init({
  app,
  dsn: import.meta.env.VITE_SENTRY_DSN,
  environment: import.meta.env.MODE,
  integrations: [Sentry.browserTracingIntegration({ router })],
  tracesSampleRate: 0.2,
  enabled: Boolean(import.meta.env.VITE_SENTRY_DSN),
})
```

O DSN do navegador é público por natureza: vai no JavaScript que qualquer pessoa baixa, e só permite *enviar* eventos. O que nunca pode aparecer no front é o token de autenticação da API do Sentry. E sem *source map* a pilha chega ilegível (`t.e is not a function`, linha 1): gere os mapas no build e envie-os com o plugin oficial do Sentry para Vite, e o painel passa a mostrar o seu código original.

> **⚠️ Atenção**
> Não mande dado pessoal para o Sentry. `sendDefaultPii: false` é o padrão e deve continuar assim. Se usar `Sentry.setUser`, passe um identificador interno (`{ id: usuario.id }`), não o e-mail. E revise as mensagens da sua própria API: `Usuário maria@exemplo.com não encontrado` vira vazamento no momento em que essa string sobe para um serviço de terceiros.

### 7.2 Logs estruturados com pino

`Usuário logou às 3 da tarde` é ótimo para ler uma linha e péssimo para responder "quantos logins falharam na última hora?". Log **estruturado** resolve: cada linha é um JSON com campos fixos, e a busca vira filtro.

```bash
npm install pino pino-http && npm install --save-dev pino-pretty
```

`unieventos-api/src/log.js`

```js
import pino from 'pino'

export const log = pino({
  level: process.env.LOG_LEVEL ?? 'info',
  // Campos que nunca podem sair no log, por mais fundo que estejam no objeto.
  redact: {
    paths: ['req.headers.authorization', 'req.headers.cookie', '*.senha', '*.token'],
    censor: '[oculto]',
  },
  // Nome do serviço em toda linha: essencial quando dois processos escrevem no mesmo lugar.
  base: { servico: 'unieventos-api' },
})
```

Com o middleware registrado, o `console.error` do tratador de erro da §7.1 vira `req.log.error({ err: erro }, 'erro não tratado')` — a mesma linha, agora amarrada ao identificador da requisição. No `src/app.js`, `app.use(pinoHttp({ logger: log }))` antes de tudo gera uma linha por requisição, com método, rota, status e duração. Dentro de qualquer rota, `req.log` é um logger já preenchido com o identificador daquela requisição: `req.log.info({ inscricaoId: inscricao.id }, 'inscrição criada')` produz uma linha JSON com `level`, `time`, `servico`, `reqId`, `inscricaoId` e `msg`. Os níveis são numéricos: `trace` 10, `debug` 20, `info` 30, `warn` 40, `error` 50, `fatal` 60. Definir `LOG_LEVEL=warn` faz o pino descartar tudo abaixo de 40 **sem nem formatar a mensagem** — por isso ele é rápido o bastante para ficar ligado em produção.

```bash
node src/server.js | npx pino-pretty                              # legível no desenvolvimento
grep '"level":50' ~/.pm2/logs/unieventos-api-out.log | tail -20   # erros no servidor
tail -500 ~/.pm2/logs/unieventos-api-out.log | jq -c 'select(.level >= 40) | {msg, url: .req.url}'
```

### 7.3 Rotação: o log que enche o disco

Um arquivo de log cresce para sempre, e servidor de projeto pequeno para por disco cheio de log — o sintoma é bonito: tudo funciona, até que nada funciona. Com pm2 (Capítulo 06), o módulo oficial resolve; com o `logrotate` do sistema, que já roda diariamente no Ubuntu, é um arquivo de configuração:

```bash
pm2 install pm2-logrotate
pm2 set pm2-logrotate:max_size 10M
pm2 set pm2-logrotate:retain 14
pm2 set pm2-logrotate:compress true
```

`/etc/logrotate.d/unieventos`

```text
/home/deploy/.pm2/logs/*.log {
    daily
    rotate 14
    maxsize 20M
    compress
    delaycompress
    missingok
    notifempty
    copytruncate
}
```

`copytruncate` é a chave quando o processo mantém o arquivo aberto (o caso do pm2): o logrotate copia o conteúdo e zera o original, em vez de renomeá-lo e deixar o processo escrevendo em um arquivo invisível. Teste sem esperar um dia com `sudo logrotate -d /etc/logrotate.d/unieventos` (simula) e `-f` (força). Se a sua API roda como serviço `systemd` e escreve na saída padrão — o laboratório `dsw-gN` do Capítulo 06 —, o `journald` já faz a rotação (`journalctl -u dsw-g3 -n 100 --no-pager`).

## 8. Uptime, `robots.txt` e `sitemap.xml`

Um monitor de disponibilidade chama uma URL em intervalos fixos e avisa quando a resposta muda. Configuração mínima: **alvo** `https://api.seudominio.dev/health` (não a home do site — uma home estática continua respondendo 200 com a API caída); **intervalo** de 5 minutos, que é o do plano gratuito do UptimeRobot; **condição de alerta** status diferente de 200 **ou** corpo sem a palavra `ok`, o que pega o caso em que o processo responde mas o banco caiu; e pelo menos um canal que apite no celular. O UptimeRobot dá 50 monitores no plano gratuito; o Better Stack dá menos monitores, intervalo menor e uma página de status pública — detalhe profissional barato, que deixa qualquer pessoa descobrir se o problema é o sistema ou a internet dela.

Vale melhorar o `/health` para que ele signifique alguma coisa:

`unieventos-api/src/rotas/saude.js`

```js
import { Router } from 'express'
import { pool } from '../db/pool.js'

const rotas = Router()

rotas.get('/health', async (req, res) => {
  try {
    // Uma consulta trivial prova que a conexão com o banco está viva.
    await pool.query('SELECT 1')
    res.json({ status: 'ok', versao: process.env.APP_VERSION ?? 'dev' })
  } catch (erro) {
    req.log.error({ err: erro }, 'health check falhou')
    res.status(503).json({ status: 'degradado', detalhe: 'banco indisponível' })
  }
})

export default rotas
```

O `robots.txt` fica na raiz do domínio e diz aos rastreadores o que podem visitar. Ele **não** protege nada — é um pedido, não uma tranca.

`unieventos-web/public/robots.txt`

```text
User-agent: *
Allow: /
Disallow: /admin

Sitemap: https://eventos.seudominio.dev/sitemap.xml
```

Em um ambiente de teste ou homologação o arquivo é outro (`User-agent: *` seguido de `Disallow: /`) — esquecer disso é como um endereço de rascunho aparece no Google. O sitemap lista as URLs que você quer indexadas; em um site pequeno pode ser escrito à mão:

`unieventos-web/public/sitemap.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://eventos.seudominio.dev/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
```

Se o seu site tem páginas geradas a partir do banco (uma por evento), escreva um script que gere o arquivo no build e inclua a tag `<lastmod>` com a data da última alteração de cada registro — assim o buscador sabe o que revisitar. Arquivo gerado por script não erra e não envelhece.

> **📌 Vale gravar**
> Saber diferenciar as três métricas do Core Web Vitals pela pergunta que cada uma responde; saber que dado de laboratório (Lighthouse) e dado de campo (usuários reais) medem coisas diferentes; e explicar por que `robots.txt` não é mecanismo de segurança.

## 🚀 Passo a passo — UniEventos medido, testado e vigiado

Ao fim destes passos você tem: linter e formatador nos dois projetos, testes rodando local e no CI, um relatório Lighthouse **antes** e outro **depois** com a diferença explicada, erros de produção chegando ao seu e-mail e um monitor apitando se a API cair.

Está no **Nível 2**? Aplique o mesmo passo na `cafe-cerrado-api` e no front do Café Cerrado: o linter, os testes com Vitest e supertest, o Lighthouse e o Sentry não dependem do domínio do projeto — só das rotas que você tem.

### Passo 1 — Linha de base (faça antes de mexer em qualquer coisa)

```bash
cd ~/weblab/unieventos-web
mkdir -p relatorios
npx lighthouse@latest https://eventos.seudominio.dev \
  --output=html --output=json --output-path=./relatorios/antes \
  --chrome-flags="--headless" --quiet
```

Anote em `relatorios/comparativo.md`: nota de Performance, LCP, CLS, TBT e total transferido. **Sem esta medição, o resto do capítulo vira opinião.**

### Passo 2 — ESLint e Prettier nos dois projetos

Instale as dependências das §2.2 e §2.3, crie os dois `eslint.config.js`, o `.prettierrc` (Capítulo 01) e o `.prettierignore`. Em cada projeto:

```bash
npx eslint .
npx prettier --write .
npx eslint . --fix
npx eslint .
```

Esperado: a primeira execução lista problemas; a última não lista nenhum. Leia cada erro que o `--fix` não resolveu — quase sempre há uma variável não usada revelando código morto. Acrescente os scripts de qualidade aos dois `package.json`.

### Passo 3 — Testes dos dois projetos

Na API, garanta `vitest`, `supertest` e `@vitest/coverage-v8` instalados e crie `tests/paginacao.test.js` e `tests/eventos.test.js` (§3), adaptando os nomes de rota. No front, instale `vitest`, `@vue/test-utils`, `jsdom` e `@vitest/coverage-v8` e crie `vitest.config.js`, `vitest.setup.js` e o teste de componente da §4.

```bash
cd ~/weblab/unieventos-api && npm test && npm run test:cobertura
cd ~/weblab/unieventos-web && npm run test:unit
```

Esperado: todos passam e a tabela de cobertura aparece. Se o processo da API travar sem terminar, o `after` não está fechando o servidor.

### Passo 4 — As correções de performance

Aplique nesta ordem, rodando `npm run build` antes e depois do item 4:

1. Converta a imagem do topo para WebP, redimensione-a e adicione `width`, `height` e `fetchpriority="high"`.
2. Ponha `loading="lazy"` nas imagens dos cards de evento.
3. Ajuste a fonte com `preconnect` e `display=swap` (ou baixe os `.woff2`).
4. Troque as rotas do Vue Router por importação dinâmica.
5. No servidor, aplique os blocos de cache e de gzip da §6 e recarregue o nginx.

```bash
sudo nginx -t && sudo systemctl reload nginx
curl -sI -H 'Accept-Encoding: gzip' https://eventos.seudominio.dev/ | grep -i -E 'content-encoding|cache-control'
```

### Passo 5 — Publique e meça de novo

```bash
cd ~/weblab/unieventos-web
npm run build
rsync -avz --delete dist/ meuvps:/var/www/unieventos-web/
npx lighthouse@latest https://eventos.seudominio.dev \
  --output=html --output=json --output-path=./relatorios/depois \
  --chrome-flags="--headless" --quiet
```

Complete o `comparativo.md` com uma tabela antes/depois e **uma frase por linha** dizendo qual correção causou aquela mudança. É esse documento, não a nota, que prova que você entendeu.

### Passo 6 — Sentry nos dois lados

Crie os dois projetos no Sentry. Na API: `instrument.js`, `SENTRY_DSN` no `.env` (e nas variáveis do Render ou do serviço systemd), `start` com `--import` e `Sentry.setupExpressErrorHandler(app)`. No front: `VITE_SENTRY_DSN` e o `Sentry.init` da §7.1. Para conferir, crie uma rota `/api/erro-de-teste` que lança `throw new Error('teste de instrumentação')`, chame-a com `curl`, confirme que o evento aparece no painel em segundos e **apague a rota em seguida**.

### Passo 7 — pino, rotação, CI e uptime

Instale `pino` e `pino-http`, crie `src/log.js`, registre o middleware e troque os `console.log` restantes por `req.log` ou `log`. No servidor, configure `pm2-logrotate` ou `/etc/logrotate.d/unieventos`. Crie o `.github/workflows/qualidade.yml` e o `lighthouserc.json` (§5.2), faça o push e confira a marca verde no pull request. Por fim, cadastre o monitor de `/health` no UptimeRobot com alerta por e-mail.

### Como conferir

| Comando ou ação | Resultado esperado |
|---|---|
| `npm run qualidade` (API e front) | Termina sem erro nos dois projetos |
| `npm run test:cobertura` | Todos os testes passam; a tabela de cobertura aparece |
| `npx lhci autorun` | Três execuções, asserções aprovadas, link do relatório |
| `curl -sI` no site publicado | `content-encoding: gzip` e `cache-control` nos arquivos com hash |
| `relatorios/comparativo.md` | Tabela antes/depois com LCP, CLS, TBT e nota |
| Rota de erro proposital | Evento no painel do Sentry, com pilha legível |
| `tail -1` no log da API | Uma linha JSON com `servico`, `level` e `msg` |
| Parar a API por 6 minutos | E-mail do monitor de uptime avisando que caiu |

## 🧪 Laboratório

### Nível A — Fixação

**A1.** No `eslint.config.js` da API, o objeto `prettier` está no fim do array. O que acontece se você movê-lo para antes de `js.configs.recommended`? Justifique com a regra de precedência do flat config.

**A2.** Classifique cada problema como "o linter pega", "o teste pega", "o Lighthouse pega" ou "só a observabilidade pega": (a) `if (idade = 18)` com um só sinal de igual; (b) a paginação devolve a página 0 com lista vazia; (c) a imagem do topo tem 2,4 MB; (d) a API devolve 500 apenas quando o usuário tem acento no nome.

**A3.** `expect('3').toBe(3)` passa ou falha no Vitest? E `assert.equal('3', 3)` com `node:assert/strict` e com o `node:assert` comum? Explique por que um comparador que coage tipos torna um teste perigoso.

**A4.** Uma página tem LCP de 1,8 s, INP de 90 ms e CLS de 0,32. Quais métricas estão na faixa boa e qual é o provável culpado do valor ruim?

**A5.** Explique em uma frase por que `loading="lazy"` na imagem do topo **piora** o LCP, enquanto a mesma propriedade nas imagens do rodapé melhora o carregamento.

**A6.** Os arquivos gerados pelo Vite têm hash no nome (`index-B7fK2p.js`). Como isso permite `Cache-Control: public, immutable` por um ano sem prender o usuário a uma versão antiga? E por que o `index.html` não pode receber o mesmo cabeçalho?

### Nível B — Aplicação

**B1.** Cobertura dirigida. Rode `npm run test:cobertura` na sua API, escolha o arquivo com a menor cobertura de linhas e escreva **três** testes que subam esse número em pelo menos 20 pontos percentuais. Pelo menos um deve exercitar um caminho de erro (entrada inválida, recurso inexistente).

Resultado esperado: a tabela de cobertura antes e depois, colada no `README.md`, com a diferença destacada.

<details><summary>Dica</summary>

A saída da cobertura lista, na última coluna, os intervalos de linhas não executadas. Abra o arquivo nessas linhas: quase sempre são `if` de validação e blocos `catch`. Para exercitar um `catch` de banco, extraia a regra para uma função pura e teste-a diretamente, ou aponte a conexão para um host inválido em um teste isolado.
</details>

**B2.** Um linter que reprova de propósito. Introduza três problemas no seu código — uma variável declarada e não usada, um `==` em vez de `===` e um `var` — e comprove que `npm run lint` falha com código de saída diferente de zero (`echo $?`). Depois corrija dois com `--fix` e explique por que o terceiro exigiu decisão sua.

Resultado esperado: o log dos dois `npm run lint` (antes e depois) e um parágrafo dizendo qual problema o `--fix` não resolveu e por quê.

<details><summary>Dica</summary>

O `--fix` só aplica correções que a regra declara como seguras e sem ambiguidade. Trocar `var` por `let` e `==` por `===` muda comportamento em casos-limite, então nem toda regra oferece correção automática. A documentação de cada regra tem um selo indicando se ela é corrigível.
</details>

**B3.** Orçamento de performance. Adicione ao seu `lighthouserc.json` asserções que reprovem o build se a nota de performance cair abaixo de 0,9, a de acessibilidade abaixo de 0,95 ou o LCP passar de 2500 ms. Faça um commit que quebre uma delas de propósito (trocando a imagem do topo por uma versão gigante, por exemplo) e mostre o CI vermelho.

Resultado esperado: dois links de execução do workflow — um verde e um vermelho — e a mensagem exata da asserção que falhou.

<details><summary>Dica</summary>

Em `ci.assert.assertions` você pode citar auditorias individuais pelo id, como `largest-contentful-paint`, no formato `["error", { "maxNumericValue": 2500 }]`. Os ids aparecem na chave `audits` do relatório JSON.
</details>

### Nível C — Desafio

**C1.** Bug plantado, teste primeiro. Peça a um colega que introduza **um** bug em uma função de regra de negócio da sua API, sem dizer qual. Sua missão, em ordem obrigatória: (1) descubra o bug pelo comportamento, não lendo o diff; (2) escreva um teste que **falha** por causa dele; (3) só então corrija; (4) confirme que o teste passa. Troque de papel e repita. No fim, os dois repositórios têm um teste novo cada, com uma mensagem de commit explicando o bug capturado.

<details><summary>Dica</summary>

Este é o ciclo de correção guiada por teste, e a ordem importa: se você corrigir antes de escrever o teste, nunca vai saber se ele realmente detectaria o problema. Um teste que nunca foi visto falhando é um teste em que não se pode confiar. Para achar o bug sem ler o diff, rode os testes que já existem — se todos passam, o bug está em um caminho que ninguém cobriu, e isso já é uma pista.
</details>

## 🏆 Desafios

### ⭐ O relatório antes e depois
Tags: performance, deploy, investigacao

Todo mundo diz que "otimizou o site". Quase ninguém consegue mostrar o número. Hoje você mostra. Pegue o seu projeto autoral publicado, meça, aplique **exatamente três** correções de performance e meça de novo — provando qual das três rendeu mais.

**Critérios de pronto**

- Dois relatórios do Lighthouse guardados no repositório (`relatorios/antes.report.html` e `depois.report.html`), gerados pela CLI com o mesmo comando.
- Um `comparativo.md` com uma tabela de no máximo quatro colunas: métrica, antes, depois, correção responsável.
- As três correções são de categorias diferentes (uma de imagem, uma de rede/cabeçalho, uma de JavaScript ou fonte).
- Uma seção "o que não funcionou" com pelo menos uma tentativa que não mudou o número, e a hipótese de por quê.
- A nota foi medida **três vezes** em cada momento e a tabela usa a mediana.

<details><summary>Pistas</summary>

1. Comece pela aba Network com **Slow 4G**: ordene por **Size** e olhe os três maiores arquivos. É quase sempre lá que está o ganho fácil.
2. O relatório do Lighthouse estima a economia em segundos de cada oportunidade ("Properly size images", "Eliminate render-blocking resources"). Use a estimativa para escolher as três correções.
3. Para converter imagens sem instalar nada, use <https://squoosh.app>; compare WebP com qualidade 75 e AVIF com qualidade 50.
</details>

### ⭐⭐ A rede de segurança do projeto autoral
Tags: testes, ci-cd, node

O seu projeto autoral não termina no primeiro deploy: se der certo, você (ou outra pessoa) vai voltar a mexer nele daqui a alguns meses. Sem testes, cada mudança futura é uma aposta. Construa a rede de segurança: uma suíte que roda em segundos, cobre o que importa e trava o pull request quando alguém quebra alguma coisa.

**Critérios de pronto**

- Pelo menos 10 testes: no mínimo 4 de unidade sobre regra de negócio e 4 de integração cobrindo os quatro verbos do CRUD principal.
- Pelo menos dois testes verificam **falha**: entrada inválida devolvendo 400 com mensagem, e acesso sem autenticação devolvendo 401.
- `npm test` roda sem depender de banco de produção nem de rede externa (banco de teste, arquivo temporário ou dados em memória).
- A suíte inteira termina em menos de 15 segundos.
- Um workflow no GitHub Actions roda lint, formatação e testes a cada pull request; a branch `main` está protegida exigindo esse workflow verde.
- O `README.md` tem uma seção "Como rodar os testes" de no máximo 8 linhas.

<details><summary>Pistas</summary>

1. Para isolar o banco, exporte a criação do pool de uma função que aceite a URL de conexão; nos testes, passe a de um banco `_teste` recriado no `before`.
2. Um `beforeEach` com `TRUNCATE` (ou a recriação do arquivo JSON) evita que um teste dependa da ordem de execução — causa número um de suíte instável.
3. Um teste que precisa de token pode gerar um token válido com a mesma função que a API usa, sem passar pelo login.
4. Em **Settings → Branches → Add rule**, marque *Require status checks to pass before merging* e escolha o job do workflow.
</details>

### ⭐⭐⭐ Painel de saúde do seu sistema
Tags: performance, deploy, seguranca

Sistemas profissionais têm uma página que responde, em cinco segundos de olhada, "está tudo bem?". Construa a sua para o projeto autoral: uma página `/status` que reúne disponibilidade, desempenho e erros — e que você consiga defender em uma apresentação de cinco minutos.

**Critérios de pronto**

- `GET /health` verifica de verdade a dependência crítica (banco) e devolve 503 quando ela cai; comprove derrubando o banco de propósito.
- Métricas de campo coletadas do navegador real com a biblioteca `web-vitals` e enviadas para a sua própria API, que as grava.
- Uma página `/status` mostrando LCP e CLS medianos das últimas visitas, contagem de erros nas últimas 24 horas e o tempo desde o último incidente.
- Sentry configurado nos dois lados, com source maps enviados no build, de modo que a pilha de um erro do front mostre o seu código original.
- Um alerta (Sentry ou uptime) que chega no seu celular, comprovado com uma captura de tela.
- Um `OBSERVABILIDADE.md` de no máximo uma página explicando o que você faria com 10 vezes mais usuários.

<details><summary>Pistas</summary>

1. `import { onLCP, onINP, onCLS } from 'web-vitals'` e, no callback, `navigator.sendBeacon('/api/metricas', JSON.stringify(metrica))` — o `sendBeacon` sobrevive ao fechamento da aba.
2. Grave as métricas em uma tabela simples (`nome`, `valor`, `rota`, `dispositivo`) e calcule a mediana em SQL com `ORDER BY` e `LIMIT`/`OFFSET`, ou em JavaScript mesmo.
3. Para os source maps, o plugin oficial do Sentry para Vite recebe organização, projeto e um token de autenticação — que vive em um secret do GitHub Actions, nunca no repositório.
4. Este é o tipo de material que fecha bem o Marco final da sua trilha.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `ESLint couldn't find an eslint.config.js file` | ESLint 9 procura flat config na pasta em que foi executado; o projeto ainda tem `.eslintrc.json` | Crie o `eslint.config.js` na raiz e apague o `.eslintrc*`; rode o ESLint de dentro da pasta certa |
| `'process' is not defined  no-undef` no back-end | `globals.node` não foi declarado em `languageOptions.globals` | Acrescente `globals: { ...globals.node }` ao objeto que casa com aqueles arquivos |
| O editor formata ao salvar e o ESLint sublinha a mesma linha em vermelho | Regras de estilo do ESLint brigando com o Prettier | Instale `eslint-config-prettier` e deixe-o como **último** item do array |
| `No test files found` no `vitest run` | Os arquivos não seguem o padrão de nome esperado (`*.test.js`, `*.spec.js`) | Renomeie para `tests/algo.test.js` ou passe o caminho: `npx vitest run tests/` |
| Os testes passam mas o processo nunca sai | Um pool de banco, um servidor ou um `setInterval` continua aberto | Feche tudo em um `afterAll` do Vitest: `pool.end()`, `servidor.close()`, `clearInterval` |
| `ReferenceError: ResizeObserver is not defined` no Vitest | O jsdom não implementa `ResizeObserver`, que o Vuetify usa | Declare o substituto em `vitest.setup.js` e registre o arquivo em `test.setupFiles` |
| `[Vue warn]: Failed to resolve component: v-btn` no teste | Componente montado sem o plugin do Vuetify | `mount(C, { global: { plugins: [createVuetify({ components, directives })] } })` |
| A nota do Lighthouse muda 15 pontos entre duas execuções seguidas | Medição única, com CPU e rede compartilhadas | Rode três vezes e use a mediana; no CI, `numberOfRuns: 3` |
| CLS alto só no celular | Imagens sem `width`/`height`, ou fonte que troca e muda a altura das linhas | Declare as dimensões em toda imagem; use `font-display: swap` com fallback de métrica parecida |
| `content-encoding` ausente na resposta do nginx | O tipo não está em `gzip_types`, ou o arquivo tem menos de `gzip_min_length` bytes | Acrescente o tipo à lista; lembre que `text/html` é sempre comprimido e não deve ser listado |
| O usuário continua vendo a versão antiga do site depois do deploy | `index.html` servido com cache longo | `Cache-Control: no-cache` no `index.html`; só arquivos com hash recebem `immutable` |
| Nenhum evento aparece no Sentry, sem mensagem de erro | DSN vazio, `enabled: false`, ou `instrument.js` carregado depois do Express | Confira a variável no servidor; use `node --import ./instrument.js`; teste com uma rota que lança erro |
| A pilha no Sentry mostra `t.e is not a function` na linha 1 | Código minificado sem source map enviado | Ative `build.sourcemap` e envie os mapas com o plugin oficial do Sentry para Vite |
| O servidor parou e o disco está 100 % cheio de logs | Nenhuma rotação configurada | `pm2 install pm2-logrotate` ou um arquivo em `/etc/logrotate.d/` com `copytruncate` |

## 🏠 Para praticar depois da aula (1 h)

No repositório do seu **projeto autoral** (front e API):

1. Configure ESLint 9 em flat config e Prettier nos dois projetos, com os scripts `lint`, `formatar:conferir` e `qualidade`. Rode `npm run lint:corrigir`, corrija o que sobrar e comite em um commit separado chamado `chore: lint e formatação`.
2. Escreva no mínimo **quatro** testes: dois de unidade sobre uma regra de negócio sua e dois de integração sobre a rota principal da API (um caminho feliz e um de erro).
3. Meça o site publicado com a CLI do Lighthouse, aplique **duas** correções de performance e meça de novo. Guarde os dois relatórios em `relatorios/` e escreva o `comparativo.md`.
4. Configure o Sentry no front (é o mais rápido dos dois) e force um erro para confirmar que o evento chega.

**Critério de pronto:** `npm run qualidade` termina sem erro nos dois projetos; `relatorios/comparativo.md` mostra a nota antes e depois com as duas correções nomeadas; existe uma captura de tela do evento no painel do Sentry.

**Guarde no seu repositório:** commit + push, com o `comparativo.md` visível na raiz e a captura em `relatorios/`.

## ✅ Está no ar quando…

- [ ] `npm run lint` e `npm run formatar:conferir` passam nos dois projetos, sem avisos (`--max-warnings=0`).
- [ ] `npm test` na API roda pelo menos um teste de unidade e um de integração, e o processo encerra sozinho.
- [ ] O workflow de qualidade roda em cada pull request e a branch `main` exige que ele passe.
- [ ] Existem dois relatórios do Lighthouse no repositório e um `comparativo.md` explicando a diferença.
- [ ] Performance e Accessibility do site publicado estão em 90 ou mais no modo *Mobile*.
- [ ] `curl -sI` mostra `content-encoding: gzip` nos arquivos de texto e `cache-control: public, immutable` nos arquivos com hash.
- [ ] Um erro proposital na API aparece no painel do Sentry em menos de um minuto, com pilha legível.
- [ ] Uma linha de log da API é JSON válido, tem `servico` e `level`, e não contém token nem senha.
- [ ] Um monitor de uptime vigia `/health` e você recebeu ao menos um alerta de teste.
- [ ] `https://eventos.seudominio.dev/robots.txt` e `/sitemap.xml` respondem 200 com o conteúdo correto para produção.

## 📚 Para aprofundar

- [ESLint — Configuration Files](https://eslint.org/docs/latest/use/configure/configuration-files) — o flat config item a item, com a ordem de precedência.
- [eslint-plugin-vue](https://eslint.vuejs.org/) — os presets `flat/essential` e `flat/recommended` e o que cada regra verifica.
- [Prettier — Integrating with Linters](https://prettier.io/docs/integrating-with-linters) — por que o `eslint-config-prettier` existe e como configurá-lo.
- [Node.js — Test runner](https://nodejs.org/api/test.html) — a API completa de `node:test`, o executor embutido: a alternativa sem dependências citada na §3.1.
- [Vitest — Getting Started](https://vitest.dev/guide/) — configuração, modo de observação e cobertura.
- [Vue Test Utils](https://test-utils.vuejs.org/) — `mount`, `props`, `emitted`, `trigger` e testes assíncronos de componente.
- [web.dev — Core Web Vitals](https://web.dev/articles/vitals?hl=pt-br) — definição, limites e a diferença entre dado de campo e de laboratório.
- [Lighthouse — documentação](https://developer.chrome.com/docs/lighthouse/overview?hl=pt-br) — categorias, cálculo da nota e uso da CLI.
- [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/getting-started.md) — `lhci autorun`, asserções e orçamento de performance.
- [Sentry — Node.js](https://docs.sentry.io/platforms/javascript/guides/node/) e [Sentry — Vue](https://docs.sentry.io/platforms/javascript/guides/vue/) — instalação, `instrument.js`, integrações e source maps.
- [pino — documentação](https://getpino.io/) — níveis, `redact`, transportes e o `pino-http` para Express.
- [nginx — módulo gzip](https://nginx.org/en/docs/http/ngx_http_gzip_module.html) e [módulo headers](https://nginx.org/en/docs/http/ngx_http_headers_module.html) — diretivas `gzip*`, `expires` e `add_header`.
- [MDN — atributo `loading`](https://developer.mozilla.org/pt-BR/docs/Web/HTML/Element/img) — quando o carregamento adiado ajuda e quando atrapalha.
- [sitemaps.org](https://www.sitemaps.org/pt_BR/protocol.html) e [Google Search Central — robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/intro?hl=pt-br) — o formato dos dois arquivos, direto da fonte.

No próximo capítulo a trilha fecha com a ferramenta mais nova e mais mal usada da caixa: assistentes de inteligência artificial. Você vai aprender a dar contexto em um prompt, a desconfiar de API inventada, a usar a IA para revisar o seu projeto autoral — e a regra que vale nos três Níveis do WebLab sobre o que é apoio e o que é cola.
