# ESPECIFICAÇÃO DO MATERIAL — FACET-SNP-310 (2026.2)

> Documento interno. Todo agente que escrever uma aula DEVE seguir isto à risca.

## 1. Identidade da disciplina

- **Código/Turma:** FACET-SNP-310 — FRAMEWORKS MODERNOS PARA DESENVOLVIMENTO DE SISTEMAS — Turma 01 (2026.2)
- **Instituição:** UNEMAT — Universidade do Estado de Mato Grosso "Carlos Alberto Reyes Maldonado", Campus Cáceres — FACET
- **Professor:** Ivan Luiz Pedroso Pires
- **Carga horária:** 60h = 45h síncronas presenciais + 15h assíncronas (EAD)
- **Horário:** 4N234 — noturno, 3 aulas de 50 min (2ª, 3ª e 4ª aulas do turno)
- **Datas:** use SEMPRE as datas literais do cronograma da §2. Não recalcule dia da semana nem "corrija" datas.
- **Pré-requisito:** FACET-SNP-307 ou SNP56D33
- **Ementa (literal do plano):** "Desenvolvimento com uso de frameworks; padrões: criacionais, estruturais e comportamentais; aplicação conjunta das abordagens de frameworks e componentes no desenvolvimento de software."

### Divisão em unidades
- **Unidade 1** — Fundamentos de front-end com Vue.js: estrutura do framework, componentes, integração com HTML/CSS/JS.
- **Unidade 2** — Vue.js avançado: Vuetify, Axios, Vue Router, Pinia.
- **Unidade 3** — Integração front-end/back-end: Firebase, Supabase, Express, autenticação, banco de dados, deploy.

### Avaliações (média aritmética simples das 3)
- **Avaliação 1** — entrega até **31/08/2026, 23h59**. Implementação introdutória de Vue 3 com CLI: estrutura, componentes, diretivas.
- **Avaliação 2** — entrega até **05/10/2026, 23h59**. Vue avançado: Vuetify + Axios + Vue Router + Pinia.
- **Avaliação 3** — entrega até **14/12/2026, 23h59**. Back-end: Firebase/Express/Supabase, banco de dados, autenticação.
- **Exame final:** prova teórica presencial e individual sobre as 3 unidades.
- Entregas **via SIGAA**.

## 2. Cronograma das 15 aulas (literal do plano de curso)

| # | Data | Unidade | Tema (conforme plano) |
|---|------|---------|------------------------|
| 01 | 10/08/2026 | U1 | Apresentação da Disciplina e Revisão JavaScript |
| 02 | 17/08/2026 | U1 | Introdução ao Vue — lifecycle, instância vue, data e methods, v-if, v-else, v-for, v-on, v-bind, v-model |
| 03 | 24/08/2026 | U1 | Introdução ao Vue — v-if, v-else, v-for, computed e onMounted |
| 04 | 31/08/2026 | U1 | Introdução a Vuetify e Vue Router. **Data final da Avaliação 1** |
| 05 | 14/09/2026 | U2 | Componentes, Vue Router e Introdução ao Vuetify |
| 06 | 21/09/2026 | U2 | Axios e Pinia |
| 07 | 28/09/2026 | U3 | Introdução ao Firebase, Node.js e Express |
| 08 | 05/10/2026 | U3 | Definindo endpoints, criando e usando middleware. **Data final da Avaliação 2** |
| 09 | 19/10/2026 | U3 | Integrando com SGBD MySQL |
| 10 | 26/10/2026 | U3 | Requisições autenticadas com Firebase |
| 11 | 09/11/2026 | U3 | Integrando front-end com back-end: exemplo de CRUD |
| 12 | 16/11/2026 | U3 | Introdução a CRUD com banco de dados em nuvem (Supabase) |
| 13 | 23/11/2026 | U3 | Desenvolvimento do Back-end |
| 14 | 07/12/2026 | U3 | Documentação com Swagger |
| 15 | 14/12/2026 | U3 | Apresentação dos resultados e finalização. **Data final da Avaliação 3** |

## 3. Projeto fio-condutor: **UniEventos**

Todas as aulas constroem incrementalmente a mesma aplicação de referência, o **UniEventos** — plataforma de divulgação e inscrição em eventos acadêmicos (palestras, minicursos, semanas acadêmicas).

**Entidades:**
- `Evento` — `id`, `titulo`, `descricao`, `categoria` (palestra | minicurso | workshop), `data_hora`, `local`, `vagas`, `imagem_url`
- `Inscricao` — `id`, `evento_id`, `usuario_uid`, `criado_em`
- `Usuario` — autenticado via Firebase Auth (`uid`, `email`, `displayName`)

**Telas:** Home (lista de eventos + filtros) · Detalhe do evento · Minhas inscrições · Login/Cadastro · Área administrativa (CRUD de eventos).

**Regra pedagógica:** o professor constrói o UniEventos em sala; **cada estudante desenvolve um projeto autoral com a mesma arquitetura, mas domínio diferente** (ex.: catálogo de plantas do Pantanal, agenda de quadras esportivas, mural de estágios, brechó, controle de pescarias, cardápio de restaurante). As avaliações são sobre o projeto autoral do estudante.

**Evolução por aula:**
- A01: definição do tema autoral + revisão JS com o modelo de dados
- A02–A03: protótipo do UniEventos em Vue puro (CDN → Vite)
- A04–A05: Vuetify + Vue Router (SPA navegável)
- A06: Axios (consumo de API pública/mock) + Pinia (estado global)
- A07–A08: API Express `uni-eventos-api` com endpoints e middlewares
- A09: persistência em MySQL
- A10: autenticação Firebase ponta a ponta
- A11: CRUD completo front + back
- A12: variante em Supabase
- A13: refatoração do backend em camadas
- A14: documentação Swagger
- A15: deploy e apresentação

**Repositórios:** `unieventos-web` (front) e `unieventos-api` (back).

## 4. Stack e versões — VERIFICADAS EM 12/08/2026 NO AMBIENTE REAL

**Não invente versões nem comandos. Estes foram testados e funcionam:**

| Pacote | Versão | Observação |
|---|---|---|
| Node.js | 22.22.2 LTS | `create-vue` exige `^22.18.0 \|\| >=24.12.0` |
| npm | 10.9.7 | |
| create-vue | 3.23.0 | `npm create vue@latest` |
| vue | 3.5.41 | Composition API + `<script setup>` como padrão |
| vite | 8.2.1 | |
| @vitejs/plugin-vue | 6.0.8 | |
| vue-router | 5.2.0 | **sem breaking changes** vs v4 para uso clássico |
| pinia | 4.0.3 | **sem breaking changes** de API pública vs v2/v3 |
| vuetify | 4.1.8 | **v4 tem mudanças relevantes vs v3 — ver §5** |
| vite-plugin-vuetify | 2.1.3 | |
| @mdi/font | 7.4.47 | |
| axios | 1.19.0 | |
| express | 5.2.1 | Node 18+; **mudanças vs v4 — ver §5** |
| mysql2 | 3.23.3 | usar `mysql2/promise` |
| firebase | 12.17.1 | SDK modular |
| firebase-admin | 14.2.0 | |
| @supabase/supabase-js | 2.112.3 | |
| swagger-ui-express | 5.0.1 | |
| swagger-jsdoc | 6.3.0 | usar chave `definition` (não `swaggerDefinition`) |

### Scaffold oficial usado na disciplina (testado)

```bash
npm create vue@latest
# ou, direto:
npx create-vue@latest unieventos-web --router --pinia
cd unieventos-web
npm install
npm run dev
```

Flags disponíveis no `create-vue` 3.23: `--default --ts --jsx --router --pinia --vitest --cypress --playwright --eslint --prettier --oxfmt --bare --force`.

Estrutura gerada (JavaScript, com `--router --pinia --bare`) — **confirmada rodando o comando**:

```
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

`src/main.js` gerado:
```js
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
```

### Instalação do Vuetify 4 (TESTADA — `npm run build` passou com Vite 8)

```bash
npm install vuetify @mdi/font
npm install -D vite-plugin-vuetify
```

`vite.config.js`:
```js
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

`src/main.js`:
```js
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

Com `autoImport: true` **não é necessário** importar `* as components` / `* as directives`.

## 5. ARMADILHAS — nunca escreva estas sintaxes desatualizadas

### Vuetify 4 (mudou em relação ao 3)
- Tema padrão agora é `system`, não `light`. Declare `defaultTheme: 'light'` para consistência em sala.
- `v-btn` **não** aplica mais UPPERCASE automático.
- Tipografia migrou de MD2 para MD3: `text-h1`…`text-h6` mudaram de tamanho/semântica (equivalentes MD3: `text-display-large`, `text-label-large` etc.). Prefira citar a classe MD3 ou usar tipografia própria.
- Elevação: 6 níveis (0–5), não mais 0–24.
- Breakpoints mudaram: md 840px, lg 1145px, xl 1545px, xxl 2138px.
- `<v-container fill-height>` **não** centraliza mais verticalmente — use `class="d-flex align-center"`.
- Props `align`, `justify`, `dense` em `<v-row>` foram substituídas por utility classes / `density="compact"`.
- O reset CSS universal foi removido; há 5 CSS layers.
- `v-app`, `v-main`, `v-app-bar`, `v-navigation-drawer`, `v-card`, `v-btn`, `v-text-field`, `v-data-table`, `v-container/v-row/v-col` **continuam existindo** com a API estrutural compatível.

### Express 5 (mudou em relação ao 4) — TUDO ABAIXO FOI TESTADO
- Erros em handler `async` são capturados automaticamente. Não precisa de `.catch(next)`.
- `req.query` é somente leitura.
- `app.del()` foi removido → `app.delete()`.
- `res.redirect(302, '/rota')` — ordem invertida em relação ao Express 4. `res.redirect('back')` foi removido.
- `res.json(obj, 201)` não existe → `res.status(201).json(obj)`.
- `req.param('id')` foi removido → `req.params.id`.
- `res.sendfile()` → `res.sendFile()`.
- Rotas com path-to-regexp v8:
  - curinga: `app.get('/arquivos/*splat')` → `req.params.splat` é **array**. Use `/{*splat}` para incluir também a raiz.
  - segmento opcional: `app.get('/relatorio{/:ano}')` no lugar de `/relatorio/:ano?`.
  - alternância por regex não é suportada → passe um array de paths.
- `express.json()` e `express.urlencoded()` são nativos; não instale `body-parser`.
- `req.body` é `undefined` (não `{}`) quando nada foi parseado.
- `express.static` agora ignora dotfiles por padrão.

### Firebase
- Nunca use a API antiga com namespace (`firebase.auth()`). Só a **API modular**: `import { getAuth, signInWithEmailAndPassword } from 'firebase/auth'`.

### Supabase
- Se a tabela tem RLS **habilitado sem policies**, o CRUD retorna `data: []` **sem erro** — é a causa nº1 de "meu código não funciona". Sempre mostre a policy junto.
- Nunca coloque a `service_role key` no front-end.

### Swagger
- `swagger-jsdoc` 6.x usa a chave `definition`, não `swaggerDefinition`.

### Axios
- Ensine sempre instância dedicada (`axios.create({ baseURL })`) com interceptors, não `axios` global.

## 6. Padrões de projeto (obrigatório pela ementa)

A ementa exige **padrões criacionais, estruturais e comportamentais**. Cada aula, quando o conteúdo permitir, DEVE trazer um box `> ### 🧩 Padrão de projeto em uso` conectando o código do dia a um padrão do catálogo GoF. Distribuição sugerida:

| Aula | Padrão | Onde aparece |
|---|---|---|
| 01 | Module / Revealing Module | módulos ES, closures |
| 02 | Observer (comportamental) | sistema de reatividade do Vue |
| 03 | Proxy (estrutural) | `reactive()` e o Proxy do ES6 sob o `ref`/`reactive` |
| 04 | Composite (estrutural) | árvore de componentes; Vue Router aninhado |
| 05 | Composite + Template Method | slots e componentes de layout |
| 06 | Singleton (criacional) + Decorator (estrutural) | store Pinia como instância única; interceptors do Axios decorando requisições |
| 07 | Chain of Responsibility (comportamental) | pipeline de middlewares do Express |
| 08 | Chain of Responsibility + Strategy | middlewares e validadores intercambiáveis |
| 09 | Factory + Pool / Repository | `createPool` do mysql2; camada de repositório |
| 10 | Proxy de proteção + Guard | middleware de autenticação; navigation guards |
| 11 | Facade (estrutural) | camada `services/` unificando chamadas ao back |
| 12 | Adapter (estrutural) | trocar MySQL por Supabase sem mudar o front |
| 13 | Builder + Dependency Injection + camadas | arquitetura controller/service/repository |
| 14 | Decorator / documentação como contrato | anotações OpenAPI |
| 15 | Retrospectiva: mapa de todos os padrões usados no projeto |

## 7. Estrutura obrigatória de CADA arquivo de aula

O arquivo é `aula-NN-slug.md`. Deve conter, nesta ordem:

```
# Aula NN — <Título>

> **FACET-SNP-310 — Frameworks Modernos para Desenvolvimento de Sistemas** · Unidade N
> UNEMAT/Cáceres — FACET · Prof. Ivan Luiz Pedroso Pires · 2026.2
> **Data:** DD/MM/2026 · **Carga:** 3 aulas de 50 min (síncrona) + 1 h (assíncrona)

## 🎯 Objetivos de aprendizagem
(5 a 7 objetivos com verbos observáveis — "ao final desta aula você será capaz de…")

## 📋 Pré-requisitos desta aula
(o que precisa estar funcionando na máquina / o que revisar; checklist)

## 🗺️ Roteiro
| Bloco | Tempo | Atividade |
(3 blocos de 50 min, com o que acontece em cada um)

## 1. <Seção teórica> …
(seções numeradas, com explicação do PORQUÊ antes do COMO;
 analogias; comparação com o que o aluno já sabe de JS puro)

## 🧩 Padrão de projeto em uso
(box conforme §6)

## 💻 Mão na massa — <nome do passo>
(passo a passo numerado, com blocos de código COMPLETOS e comentados em português;
 sempre indicar o caminho do arquivo acima do bloco: `src/components/EventoCard.vue`)

## 🧪 Laboratório
(3 a 5 exercícios crescentes, feitos em sala; cada um com enunciado,
 resultado esperado e uma dica em <details>)

## 🐛 Erros comuns e como resolver
(tabela: sintoma → causa → solução)

## 🏠 Atividade assíncrona (1 h)
(tarefa objetiva, com critério de pronto; ligada ao projeto autoral)

## ✅ Checkpoint do projeto autoral
(checklist do que deve estar funcionando no repositório do estudante ao fim desta aula)

## 📚 Para aprofundar
(links oficiais + capítulos das referências básicas do plano)
```

Nas aulas 04, 08 e 15, acrescentar antes de "Para aprofundar":

```
## 📝 Avaliação N — instruções de entrega
(escopo, requisitos obrigatórios, rubrica em tabela com pesos somando 10,
 formato de entrega no SIGAA, prazo, política de atraso e de plágio)
```

## 8. Regras de escrita

- **Idioma:** português do Brasil. Código e identificadores em português (`eventos`, `carregarEventos`), exceto palavras-chave e APIs.
- **Tom:** direto, prático, sem enrolação. Frases curtas. Voz ativa. Sem "vamos agora" repetitivo.
- **Tamanho:** 900 a 1.600 linhas de markdown por aula — precisa sustentar 150 min de aula. Não resuma.
- **Código:** completo e executável. Nada de `// ...resto do código`. Sempre com o caminho do arquivo antes do bloco.
- **Cada bloco de código** deve ter a linguagem declarada: ```vue, ```js, ```bash, ```sql, ```html, ```json.
- **Callouts:** use `> **💡 Dica**`, `> **⚠️ Atenção**`, `> **🔎 Por baixo do capô**`, `> **📌 Na prova**`.
- **Acessibilidade/qualidade:** mencionar boas práticas (semântica, `key` em `v-for`, tratamento de erro, loading states).
- **Continuidade:** cada aula começa retomando em 3 linhas onde a anterior parou e termina anunciando a próxima. Não reintroduza o que já foi ensinado — referencie ("como vimos na Aula 03").
- **Sem invenção:** se não tiver certeza de uma API, use as versões e trechos deste documento. Não cite números de versão diferentes dos da tabela §4.
- Não use tabelas com mais de 4 colunas (quebram na projeção).
- Sempre deixar uma linha em branco antes de listas e depois de títulos.
