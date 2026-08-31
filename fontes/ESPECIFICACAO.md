# ESPECIFICAÇÃO EDITORIAL — WebLab (weblab.aprendabit.com)

> Documento-mestre. Todo agente ou pessoa que escrever ou editar uma aula DEVE seguir isto à risca.
> O build (`python3 build/build.py`) roda um lint que **rejeita** arquivos fora do padrão.

## 1. O que é o WebLab

**WebLab — Laboratório de Desenvolvimento Web** é a apostila online, pública e gratuita de desenvolvimento web, escrita e revisada por um grupo de professores universitários (ver `fontes/autores.md`). Nasceu de disciplinas de graduação, mas **não é material institucional**: não cita a instituição no corpo das aulas, não pressupõe matrícula e serve a qualquer pessoa. Ela é organizada em quatro trilhas, abertas a qualquer pessoa que queira aprender:

| Trilha | Pré-requisito | Aulas | Projeto fio-condutor |
|---|---|---|---|
| **Nível 1 — Introdução ao Desenvolvimento Web** | Nenhum | 15 | **Site do evento acadêmico** — 5 páginas (início, programação, inscrição, palestrantes, contato) |
| **Nível 2 — Desenvolvimento Web** | Nível 1 | 16 | **Café Cerrado** — cafeteria fictícia: site estático → SPA → API Express + login Google + CRUD |
| **Nível 3 — Frameworks Modernos** | Nível 2 | 15 | **UniEventos** — Vue 3 + Vuetify + Pinia + Express + MySQL/Supabase + Firebase Auth |
| **Deploy & Ferramentas** | trilha transversal | 11 capítulos | Publicar de verdade os três projetos acima |

**Regra pedagógica central:** o professor constrói o projeto fio-condutor em sala; **cada estudante desenvolve um projeto autoral** com a mesma arquitetura e um domínio diferente (ex.: catálogo de plantas do Pantanal, agenda de quadras, mural de estágios, brechó, controle de pescarias, cardápio). As avaliações são sobre o projeto autoral.

**Público:** estudantes de graduação em computação, noturno, muitos trabalhando de dia. Alguns nunca programaram (Nível 1); outros já fazem freelas (Nível 3). O texto precisa servir aos dois: explicar o porquê antes do como, sem infantilizar.

## 2. O que muda em relação a uma apostila comum: os exercícios são o centro

O objetivo declarado do WebLab é **instigar curiosidade e vontade de superação**. Cada aula tem quatro camadas de prática, sempre nesta ordem:

1. **💻 Mão na massa** — passo a passo guiado no projeto fio-condutor. Todo mundo faz junto.
2. **🧪 Laboratório** — exercícios em sala em três níveis: **A (fixação)**, **B (aplicação)** e **C (desafio)**. Cada item tem resultado esperado; os B e C têm dica em `<details>`.
3. **🏆 Desafios** — extras, opcionais, mais difíceis, com estrelas: `⭐` (1–2 h), `⭐⭐` (uma tarde), `⭐⭐⭐` (um fim de semana). Na última aula de cada unidade há um **🔥 Boss** — um mini-projeto que combina tudo da unidade. Os desafios de todas as aulas são reunidos automaticamente no **Banco de Desafios** do site.
4. **🏠 Para praticar depois da aula (1 h)** — tarefa objetiva com critério de pronto, ligada ao projeto autoral, guardada no repositório do estudante.

### 2.1 Como escrever um bom desafio

- **Enunciado aberto, critérios fechados.** Diga o *quê* e o *porquê*; não diga o *como*. Em vez de "crie uma função `filtrar(lista, termo)` que…", diga "a busca do cardápio precisa ignorar acentos e maiúsculas — hoje 'cafe' não acha 'Café'. Resolva sem biblioteca externa." Depois liste **Critérios de pronto** verificáveis.
- **Gancho de curiosidade.** Comece com uma pergunta ou um fato que faça o estudante querer descobrir ("Por que o navegador demora 300 ms para reagir ao toque no celular? Hoje você vai medir isso.").
- **Pistas, nunca solução.** O bloco `<details><summary>Pistas</summary>` traz 2–4 pistas progressivas: a primeira aponta a documentação certa; a última quase entrega a abordagem. Nunca cole o código final.
- **Variedade de formato.** Alterne entre: investigação no DevTools/terminal, bug plantado para caçar, refatoração de código feio (dado no enunciado), otimização de performance com medição, acessibilidade (usar só o teclado / leitor de tela), mini-projeto, "explique para um colega", comparação entre duas abordagens, reprodução de um componente de um site real.
- **Conectado à aula e ao projeto autoral.** O desafio usa o que foi ensinado hoje e, de preferência, melhora o projeto do estudante.
- **Escalonável.** ⭐ deve ser possível para quem só fez o Laboratório A; ⭐⭐⭐ deve fazer o melhor da turma suar. Diga o que ganha quem faz (ex.: "vale como item extra da rubrica de Avaliação 2").

**Formato obrigatório de cada desafio** (o build extrai os campos; lint rejeita se faltar algo):

````markdown
### ⭐⭐ Busca que ignora acentos
Tags: javascript, strings, unicode

Digite "cafe" na busca do Café Cerrado: nada aparece, porque o produto se chama "Café com leite". Usuários não digitam acento no celular — e o seu site não pode depender disso. Descubra por que `"café" === "cafe"` é falso e resolva o problema na raiz, sem biblioteca externa.

**Critérios de pronto**

- `buscar("cafe")` encontra "Café com leite" e "CAFÉ EXPRESSO".
- `buscar("acai")` encontra "Açaí" (o ç também é normalizado).
- A normalização é feita em **uma** função reutilizável, usada tanto no termo digitado quanto nos nomes dos produtos.
- Um comentário de 3 linhas no código explica o que é a forma de normalização Unicode usada.

<details><summary>Pistas</summary>

1. Procure "String.prototype.normalize" na MDN e leia sobre as formas NFC e NFD.
2. Na forma NFD, o "é" vira "e" + um acento combinante separado. Acentos combinantes vivem no intervalo Unicode `̀`–`ͯ`.
3. Uma expressão regular com esse intervalo e a flag `g` remove todos os acentos de uma vez.
4. Lembre-se de aplicar a mesma normalização (mais `toLowerCase()`) nos dois lados da comparação.
</details>
````

Regras do formato: título no `### ` começando com `⭐`, `⭐⭐`, `⭐⭐⭐` ou `🔥 Boss — `; linha `Tags:` logo abaixo (2–5 tags minúsculas, separadas por vírgula, do vocabulário da §2.2); parágrafo de contexto; `**Critérios de pronto**` com lista; `<details><summary>Pistas</summary>` com lista numerada. Nada mais é obrigatório, mas um "**Para ir além**" de uma linha é bem-vindo.

### 2.2 Vocabulário de tags

`html`, `css`, `javascript`, `dom`, `eventos`, `formularios`, `acessibilidade`, `responsivo`, `layout`, `flexbox`, `grid`, `animacao`, `svg`, `performance`, `devtools`, `http`, `fetch`, `async`, `json`, `api`, `spa`, `node`, `express`, `rotas`, `middleware`, `autenticacao`, `oauth`, `crud`, `banco-de-dados`, `mysql`, `supabase`, `firebase`, `vue`, `vuetify`, `pinia`, `router`, `axios`, `padroes-de-projeto`, `git`, `github`, `deploy`, `dns`, `https`, `nginx`, `docker`, `ci-cd`, `seguranca`, `testes`, `swagger`, `ia`, `terminal`, `investigacao`, `refatoracao`, `bug`, `projeto`. Use só estas (o Banco de Desafios filtra por elas). Se precisar de outra, use no máximo uma tag nova por aula.

## 3. Estrutura obrigatória de CADA aula

Arquivo: `fontes/<trilha>/aula-NN-slug.md` (nível) ou `fontes/deploy/cap-NN-slug.md` (deploy). Os nomes exatos estão em `build/config.py` — não invente nomes. Conteúdo, nesta ordem:

```
# Aula NN — <Título exatamente como em config.py>

> **Nível N — <nome da trilha>** · Unidade N: <nome da unidade>
> WebLab · curso aberto de desenvolvimento web
> **Tempo estimado:** 3 blocos de 50 min + 1 h de prática

## 🎯 Objetivos de aprendizagem
(5 a 7 objetivos com verbos observáveis — "ao final desta aula você será capaz de…")

## 📋 Pré-requisitos
(checklist do que precisa estar funcionando na máquina / o que revisar da aula anterior;
 retome a aula anterior em 3 linhas: "Na aula passada… Hoje…")

## 🗺️ Roteiro
| Bloco | Tempo | Atividade |
(3 blocos de 50 min, com o que acontece em cada um)

## 1. <Seção teórica>
## 2. …
(seções numeradas; PORQUÊ antes do COMO; analogias; comparação com o que o estudante já sabe;
 código COMPLETO e comentado em português, com o caminho do arquivo em negrito ou `code` na linha acima do bloco;
 pelo menos um `> **🧠 Você sabia?**` e um `> **🔬 Investigue**` por aula)

## 🧩 Padrão de projeto em uso            ← obrigatório só no Nível 3 (ementa exige); opcional nos outros
(conecta o código do dia a um padrão GoF ou de arquitetura)

## 💻 Mão na massa — <nome do passo>
(passo a passo numerado no projeto fio-condutor da trilha; código completo; caminho do arquivo antes de cada bloco;
 termina com "Como testar" e o resultado esperado)

## 🧪 Laboratório
### Nível A — Fixação        (≥ 4 itens: **A1.** … perguntas curtas / trechos para prever a saída / completar código)
### Nível B — Aplicação      (≥ 3 itens: **B1.** … construir algo pequeno; cada um com "Resultado esperado" e <details>Dica</details>)
### Nível C — Desafio         (≥ 1 item: **C1.** … o mais difícil, para quem termina antes; <details>Dica</details>)

## 🏆 Desafios
(≥ 3 desafios no formato da §2.1: um ⭐, um ⭐⭐, um ⭐⭐⭐; na última aula de cada unidade, também um 🔥 Boss)

## 🐛 Erros comuns
| Sintoma | Causa | Solução |
(≥ 5 linhas; sintomas reais — mensagens de erro literais do console/terminal quando existirem)

## 🏠 Para praticar depois da aula (1 h)
(tarefa objetiva, ligada ao projeto autoral; "Critério de pronto"; termina com "commit + push no seu repositório")

## ✅ Checkpoint do projeto             ← na trilha Deploy: "## ✅ Está no ar quando…"
(checklist do que deve estar funcionando no repositório do estudante ao fim desta aula)

## 📚 Para aprofundar
(links oficiais — MDN em pt-BR quando existir, web.dev, docs do Node/Express/Vue/Vuetify/Pinia — com 1 linha dizendo o que ler;
 capítulo(s) da bibliografia da disciplina, listada em config.py)
```

Nas aulas que fecham unidade (**N1: 06, 10, 15 · N2: 06, 10, 16 · N3: 04, 08, 15**), acrescentar **antes** de "Para aprofundar":

```
## 🎓 Marco do projeto — Unidade N
(o que o projeto autoral do estudante precisa ter ao fim da unidade:
 escopo em um parágrafo; requisitos obrigatórios numerados, cada um dizendo em que aula foi estudado;
 um "checklist de qualidade" com o que separa um projeto pronto de um projeto entregue às pressas;
 e "Como saber que está pronto": o que abrir, medir ou testar para ter certeza.
 SEM nota, peso, rubrica pontuada, prazo, entrega institucional ou política de atraso —
 quem cursa a disciplina recebe essas regras do professor; quem estuda sozinho usa o marco como meta.)
```

Na trilha Deploy, `## 💻 Mão na massa` chama-se `## 🚀 Passo a passo — <o que vai ao ar>` e publica de verdade um projeto das trilhas.

## 4. Callouts

Use blockquotes que começam com o emoji + rótulo em negrito. O build os transforma em caixas coloridas.

```markdown
> **💡 Dica**
> Texto.

> **⚠️ Atenção**
> Texto.

> **🔎 Por baixo do capô**
> Como a coisa funciona internamente (event loop, especificidade, TCP…).

> **📌 Na prova**
> O que costuma cair no exame final teórico.

> **🧠 Você sabia?**
> Fato surpreendente, histórico ou de mercado, ligado ao conteúdo. Uma curiosidade por aula, no mínimo.

> **🔬 Investigue**
> Experimento de 5 minutos no DevTools/terminal/console que o estudante faz agora, com o que observar.
```

## 5. Stack e versões — NÃO invente versões nem comandos

| Pacote | Versão | Observação |
|---|---|---|
| Node.js | 22 LTS (ou 24) | `node -v`; `create-vue` exige `^22.18.0 \|\| >=24.12.0` |
| npm | 10+ | vem com o Node |
| vue | 3.5 | Composition API + `<script setup>` como padrão |
| vite | 8 | `npm create vue@latest` |
| vue-router | 5 | sem breaking changes vs v4 para uso clássico |
| pinia | 4 | API pública igual à v2/v3 |
| vuetify | 4 | **v4 tem mudanças vs v3 — ver §6** |
| axios | 1.19 | sempre instância dedicada com `axios.create` |
| express | 5 | Node 18+; **mudanças vs v4 — ver §6** |
| mysql2 | 3 | usar `mysql2/promise` e `createPool` |
| firebase | 12 | **só API modular** |
| firebase-admin | 14 | verificação de token no back |
| @supabase/supabase-js | 2 | RLS! ver §6 |
| swagger-jsdoc / swagger-ui-express | 6.3 / 5.0 | chave `definition` |
| google-auth-library | 9+ | `OAuth2Client.verifyIdToken` (Nível 2) |
| Bootstrap | 5.3 | via CDN nas aulas de framework CSS |
| Tailwind | 4 | via Play CDN (`<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4">`) só para demonstração |

Scaffold oficial do Nível 3 (testado): `npx create-vue@latest unieventos-web --router --pinia`, `npm install vuetify @mdi/font`, `npm install -D vite-plugin-vuetify`, `vite.config.js` com `vuetify({ autoImport: true })`, `createVuetify({ theme: { defaultTheme: 'light' } })`.

## 6. Armadilhas — nunca escreva estas sintaxes desatualizadas

**Vuetify 4 (mudou em relação ao 3):** tema padrão é `system` (declare `defaultTheme: 'light'`); `v-btn` não aplica mais UPPERCASE; tipografia MD3 (`text-h1…h6` mudaram); elevação 0–5; breakpoints md 840 / lg 1145 / xl 1545; `<v-container fill-height>` não centraliza (use `class="d-flex align-center"`); props `align`/`justify`/`dense` em `v-row` viraram utility classes / `density="compact"`; `v-app`, `v-main`, `v-app-bar`, `v-navigation-drawer`, `v-card`, `v-btn`, `v-text-field`, `v-data-table`, `v-container/v-row/v-col` continuam com a mesma API estrutural.

**Express 5 (mudou em relação ao 4):** erros em handlers `async` são capturados automaticamente (sem `.catch(next)`); `req.query` é somente leitura; `app.del()` → `app.delete()`; `res.redirect(302, '/rota')` (ordem invertida), `res.redirect('back')` removido; `res.json(obj, 201)` → `res.status(201).json(obj)`; `req.param('id')` → `req.params.id`; `res.sendfile()` → `res.sendFile()`; curinga `app.get('/arquivos/*splat')` (`req.params.splat` é array) e `/{*splat}` para incluir a raiz; opcional `'/relatorio{/:ano}'`; sem regex de alternância (passe array); `express.json()`/`express.urlencoded()` nativos (não instale `body-parser`); `req.body` é `undefined` quando nada foi parseado; `express.static` ignora dotfiles.

**Firebase:** nunca `firebase.auth()` (namespace); só `import { getAuth, signInWithEmailAndPassword } from 'firebase/auth'`.

**Supabase:** tabela com RLS habilitado e sem policies retorna `data: []` **sem erro** — sempre mostre a policy junto. Nunca a `service_role key` no front.

**Google Sign-In (Nível 2):** use a biblioteca **Google Identity Services** (`<script src="https://accounts.google.com/gsi/client" async></script>`, `google.accounts.id.initialize`/`renderButton`) e verifique o **ID token** no back com `google-auth-library`. Não use a antiga `gapi.auth2`.

**Swagger:** `swagger-jsdoc` 6.x usa `definition`, não `swaggerDefinition`.

**JavaScript moderno:** `const`/`let` (nunca `var` em código novo); `fetch` + `async/await` (mostre `.then` uma vez, para entender, e siga com `await`); módulos ES (`type="module"`) a partir do Nível 2 Unidade 2.

**HTML/CSS:** `<!DOCTYPE html>`, `lang="pt-BR"`, `meta viewport`; nada de `<center>`, `<font>`, tabelas para layout; unidades relativas; `prefers-reduced-motion` em toda animação; contraste mínimo 4.5:1.

**CDNs:** sempre fixe a versão na URL e, quando o provedor fornecer (Bootstrap, jsDelivr), inclua `integrity="sha384-…" crossorigin="anonymous"` — explique que isso protege contra um CDN comprometido. Scripts de demonstração (Tailwind Play CDN) são só para aula; em produção o estudante instala via npm.

## 7. Regras de escrita

- **Idioma:** português do Brasil. Código e identificadores em português (`produtos`, `carregarProdutos`, `EventoCard`), exceto palavras-chave, APIs e convenções universais (`index.html`, `README.md`, `main.js`).
- **Tom:** direto, prático, sem enrolação. Frases curtas. Voz ativa. Sem "vamos agora" repetido. Fale com o estudante na segunda pessoa ("você").
- **Tamanho:** aulas de nível: 900 a 1.500 linhas de Markdown (o lint exige ≥ 600); capítulos de deploy: 600 a 1.000 (lint ≥ 400). Precisa sustentar 150 min de aula. Não resuma.
- **Código:** completo e executável. Nada de `// ...resto do código`, `TODO`, `TBD`. Todo bloco com linguagem declarada: ```` ```html ````, ```` ```css ````, ```` ```js ````, ```` ```vue ````, ```` ```bash ````, ```` ```sql ````, ```` ```json ````, ```` ```http ````, ```` ```yaml ````, ```` ```dockerfile ````, ```` ```nginx ````, ```` ```text ````. Caminho do arquivo antes do bloco.
- **Material aberto:** sem nota, peso, rubrica pontuada, prazo, entrega institucional (SIGAA), frequência ou exame — o WebLab serve tanto a quem cursa a disciplina quanto a quem estuda por conta própria, em qualquer lugar. Onde havia avaliação, há **marco do projeto**; onde havia entrega, há "commit + push no seu repositório".
- **Sem datas, sem semestre, sem turma — em nenhuma aula, nem na 01.** O material serve a qualquer oferta: a Aula 01 apresenta a sequência das aulas e o escopo das avaliações **sem** datas, dizendo que o calendário e os prazos saem no SIGAA. Nada de `2026.2`, `Turma 01`, `dd/mm/aaaa` ou dia da semana fixo. O calendário de um semestre é opcional e vive só em `build/config.py` (`SEMESTRE`, `CRONOGRAMA`, `prazo` das avaliações) — ver `docs/calendario-2026-2.md`. Em dados de exemplo (eventos fictícios, `<time>`, seeds), use o ano **2030**; datas históricas e didáticas (1995, `31/02/2000`) permanecem.
- **Continuidade:** cada aula retoma em 3 linhas onde a anterior parou e termina anunciando a próxima ("Na próxima aula…" sem data). Não reintroduza o que já foi ensinado — referencie ("como vimos na Aula 03").
- **Sem invenção:** se não tiver certeza de uma API, use as versões e trechos deste documento. Prefira links para documentação oficial (MDN pt-BR: `https://developer.mozilla.org/pt-BR/docs/...`).
- **Tabelas com no máximo 4 colunas** (quebram na projeção e no celular).
- Linha em branco antes de listas e depois de títulos. Sem HTML cru além de `<details>`, `<summary>`, `<kbd>`, `<br>`.
- Acessibilidade e qualidade: mencione boas práticas (semântica, `alt`, `label`, `key` em `v-for`, tratamento de erro, estados de carregamento).
- **Não copie texto de livros ou sites.** Escreva com as próprias palavras; cite a fonte em "Para aprofundar".

## 8. O que o lint verifica (resumo)

Seções obrigatórias na ordem da §3 · Laboratório com ≥4 A, ≥3 B, ≥1 C · ≥3 desafios com `Tags:`, `**Critérios de pronto**` e `<details>` · todo fence com linguagem · sem placeholders (`...resto`, `// ...`, `TODO`, `TBD`, `Lorem`) · ≥600 linhas (aula) / ≥400 (deploy) · tabelas ≤4 colunas · título H1 igual ao de `config.py`. Rode `python3 build/lint.py` antes de entregar; entregue só com **zero erros**.

## 9. Aula-modelo

Use como referência de formato e profundidade: `fontes/nivel-3/aula-06-axios-e-pinia.md` (Nível 3) e, quando existirem, `fontes/nivel-1/aula-07-layout-de-um-website-e-menu.md` (Nível 1) e `fontes/nivel-2/aula-09-promises-e-async-await.md` (Nível 2).
