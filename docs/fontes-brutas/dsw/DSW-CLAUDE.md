# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this directory is

Course-materials folder — not a code project and not a git repo — for **FACET-SNP-307 · Desenvolvimento Web** (60h), UNEMAT Campus Sinop, curso TADS, Turma 01, semester 2026/2, taught by Prof. Ivan Luiz Pedroso Pires (ivanpires@unemat.br). Everything here is a PDF except the example folders. All student-facing content is Brazilian Portuguese (pt-BR) and must stay that way.

- `Plano_de_Curso_FACET-SNP-307_2026.2_01_.pdf` — official SIGAA course plan (ementa, methodology, grading, weekly schedule, bibliography). Source of truth for dates and evaluation rules.
- `Aula_NN_<Titulo>.pdf` (01–16) — one 3–4 page A4 handout ("apostila") per class, rendered with wkhtmltopdf from HTML. The HTML sources are **not** kept here.
- `Aula_01_Slides.pdf`, `Aula_02_Slides.pdf` — 16:9 slide decks; only these two exist (01 exported from Google Slides, 02 built with pdf-lib).
- `files/` + `files.zip` — byte-identical copies of Aulas 09–15, a distribution bundle. The root PDFs are canonical; if one changes, refresh the copy and re-zip.
- `aula03-exemplos/` — ready-to-use HTML/CSS examples for Aula 3 (one subfolder per handout section: `01-semantica`, `02-conteudo`, `03-links`, `04-formularios`, plus `05-projeto-modelo`, a complete answer to the Aula 3 extraclass activity themed "Café Cerrado", a fictional cafeteria). Its `README.md` maps handout sections to files. Pages are self-contained, pt-BR, deliberately JavaScript-free (Unit 1), and carry their explanations as HTML comments — keep that style if adding examples for other aulas (e.g. `aula04-exemplos/`).

Sibling folders `../idw` (FACET-SNP-319, the prerequisite course) and `../fds` (FACET-SNP-310) are other courses with their own formats and pipelines; nothing is shared with them.

## Working with the files

There is nothing to build, lint or test. Example folders are opened with VS Code Live Server or directly in the browser. Useful commands:

```bash
pdftotext -layout Aula_09_Promises_Async_Await.pdf - | less   # read a handout (grep-friendly; faster than the Read tool)
pdftotext Aula_09_*.pdf - | grep -nE '^[0-9]+\. '             # list a handout's numbered sections
pdfinfo Aula_09_*.pdf                                           # page count / generator
cmp files/Aula_09_*.pdf Aula_09_*.pdf && echo same              # check that the bundle copy is current
```

`wkhtmltopdf` is not installed on this machine. Available for HTML→PDF: `google-chrome --headless --print-to-pdf=out.pdf in.html`, `weasyprint`, `pandoc`, `libreoffice`. Node v24 (nvm) and git are available for writing and checking the code examples that go into handouts.

## Course structure

Project-based learning: each student builds **one** incremental web app across the semester (free theme, chosen in Aula 1). Three units, each adding a layer to the same project and closing with an individual practical evaluation (10,0 pts, delivered as a SIGAA task):

| Unit | Aulas | Layer | Deadline |
|---|---|---|---|
| 1 — Web Estática | 01–06 | HTML semântico, frameworks CSS, animação/SVG, acessibilidade/ARIA | 29/09/2026 23h59 |
| 2 — Web Dinâmica Client-Side | 07–10 | JS/DOM/eventos, arrow functions/callbacks/vetores, Promises/async-await, AJAX/JSON/SPA | 27/10/2026 23h59 |
| 3 — Web Dinâmica Server-Side | 11–16 | Node/Express, middlewares/Router, rotas+controladores, Google OAuth 2.0, CRUD com persistência | 24/11/2026 23h59 |

MF = (A1 + A2 + A3) ÷ 3; aprovação MF ≥ 6,0; exame final if 4,0 ≤ MF < 6,0. Weekly classes 11/08 → 24/11/2026 (dates in the Plano). Atendimento: Mondays 18–19h, by e-mail appointment.

### The running example threaded through the handouts

Extraclass activities chain from one Aula to the next, so names introduced early are reused later. Keep them consistent when writing or editing material:

- **Unit 1** — static site on GitHub Pages: `index.html`, `contato.html`, `header/nav/main/footer` landmarks, CSS framework choice justified in `README.md`, `prefers-reduced-motion`, skip link, `aria-current="page"`, Lighthouse ≥ 90.
- **Unit 2** — `js/app.js` (loaded with `defer`); an array of objects for the project's items (the canonical resource is **produtos**) rendered as cards; search/filter via `filter`/`sort`/`reduce`; `buscarProdutos()` / `buscarCategorias()` returning Promises, then real `fetch` to JSONPlaceholder; hash-based SPA navigation (≥ 3 screens); ViaCEP as bonus.
- **Unit 3** — a new Node repo; site moved to `public/` and served by `express.static`; API `GET/POST/PUT/DELETE /api/produtos[/:id]` with query-string search; layout `routes/`, `controllers/`, `data/` (JSON-file persistence), lean `server.js`; `testes.http` (REST Client) versioned; middlewares `express.json()` → log → `exigirLogin`, plus API 404 and error handler; `POST /api/auth/google` verifying the Google ID token; Client ID in `.env` (gitignored); 401 for writes without token, 403 when editing another user's item; `npm install && npm run dev` must work in a clean folder.

## Handout template (Aulas 02–16)

Every handout follows the same skeleton — reproduce it when creating a new one:

1. Header block: "UNIVERSIDADE DO ESTADO DE MATO GROSSO — UNEMAT • CAMPUS SINOP / TECNOLOGIA EM ANÁLISE E DESENVOLVIMENTO DE SISTEMAS", "Desenvolvimento Web", "FACET-SNP-307 • 60h • Turma 01 • 2026/2", "Aula N — Título", professor line ending with "Unidade n: <nome>".
2. `1. Objetivos da aula`, then a callout box: normally `CONEXÃO COM A AULA ANTERIOR`; `INÍCIO DA UNIDADE n — …` on a unit's first class; `PRAZO HOJE` on evaluation-deadline days (Aulas 08, 12, 16).
3. Numbered content sections with occasional ALL-CAPS callout boxes (`ATENÇÃO`, `REGRA DE OURO`, `ARMADILHA CLÁSSICA`, …).
4. `N. Atividade extraclasse (assíncrona — SIGAA)` — numbered list ending with "Commit + push e entregar o link no SIGAA" and a "Leitura dirigida (Biblioteca Virtual da UNEMAT)" item.
5. `PRÓXIMA AULA (dd/mm)` callout, then `N. Referências`.

Dates inside handouts (`PRÓXIMA AULA`, deadlines) must match the Plano de Curso. Aulas 06, 10 and 16 additionally carry the checklist/criteria for evaluations 1, 2 and 3.

Bibliography used in "Leitura dirigida": Queirós & Portela, *Introdução ao Desenvolvimento Moderno para a Web* (FCA, 2018) — primary; Alves, *Projetos de Sistemas Web* (Érica, 2015); Loudon, *Desenvolvimento de Grandes Aplicações Web* (Novatec, 2019); Purewal, *Aprendendo a Desenvolver Aplicações Web* (Novatec, 2014); plus MDN, Node.js, Express and Google Identity docs.
