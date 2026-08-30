# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this is

**WebLab** (<https://weblab.ivanpires.dev>) — an online, self-contained textbook (pt-BR) for the web-development courses of UNEMAT/Sinop taught by Prof. Ivan Luiz Pedroso Pires: Nível 1 (FACET-SNP-319, HTML/CSS/JS), Nível 2 (FACET-SNP-307, front-end → Express + Google OAuth), Nível 3 (FACET-SNP-310, Vue 3/Vuetify/Pinia + Express/MySQL/Supabase/Firebase), plus the transversal **Deploy & Ferramentas** track, a **Banco de Desafios** and **Links úteis**. All student-facing content is Brazilian Portuguese and must stay that way.

Design spec: `docs/superpowers/specs/2026-08-29-weblab-design.md`. Implementation plan: `docs/superpowers/plans/2026-08-29-weblab-implementation.md`.

## Architecture: Markdown sources → Python build → static site → rsync

- `fontes/<trilha>/aula-NN-slug.md` (`cap-NN-slug.md` for deploy) are the canonical content. File names, titles, units and evaluation markers live in `build/config.py` — the lint checks the H1 against it.
- `build/render.py` converts Markdown (python-markdown + pygments), turns emoji blockquotes into callouts, wraps code blocks (language label + copy button), and **extracts every `### ⭐…`/`### 🔥 Boss — …` under `## 🏆 Desafios`** into the Banco de Desafios. Adjacent blockquotes are separated automatically (python-markdown would merge them).
- `build/lint.py` enforces `fontes/ESPECIFICACAO.md` (required sections in order, ≥4 A / ≥3 B / ≥1 C lab items, ≥3 desafios each with `Tags:`, `**Critérios de pronto**` and `<details>`, fences with language, no `TODO`/`...`, ≥600 lines for aulas / ≥400 for deploy chapters, tables ≤4 columns). `build.py` refuses to build with lint errors unless `--forcar`.
- `build/paginas.py` holds the HTML templates; `build/theme.css` and `build/app.js` are inlined into every page (no external requests at runtime). `build/build.py` writes `site/`: per-lesson pages, per-track index and single-file `apostila.html`, `desafios/`, `links/`, home, `busca.json`, `sitemap.xml`, `404.html`, then checks internal links.
- Dates for the semester exist **only** in `build/config.py` (`CRONOGRAMA`, `AVALIACOES`) and in each track's Aula 01. Lessons themselves are timeless.
- Deployment: `deploy.sh` = build + `rsync` to `webmaster@ivanpires.dev:/home/webmaster/apps/weblab/site/`, served by the nginx vhost `weblab.ivanpires.dev` (Let's Encrypt). See `docs/servidor.md`.

## Commands

```bash
.venv/bin/python -m pytest build/tests -q        # tests
.venv/bin/python build/lint.py [--parcial]       # lint sources (parcial: ignore missing files)
.venv/bin/python build/build.py [--parcial] [--forcar]
./deploy.sh [--parcial|--forcar]                 # build + publish
```

If `.venv` is missing: `python3 -m venv --system-site-packages .venv && .venv/bin/pip install pytest markdown pygments`.

## Content rules (summary — `fontes/ESPECIFICACAO.md` is the master)

- Section order: 🎯 Objetivos → 📋 Pré-requisitos → 🗺️ Roteiro → numbered theory (with ≥1 `🧠 Você sabia?` and ≥1 `🔬 Investigue`) → (🧩 Padrão de projeto, Nível 3) → 💻 Mão na massa (deploy: 🚀 Passo a passo) → 🧪 Laboratório (Nível A/B/C) → 🏆 Desafios → 🐛 Erros comuns → 🏠 Atividade assíncrona → ✅ Checkpoint (deploy: ✅ Está no ar quando…) → (📝 Avaliação N on unit-closing lessons) → 📚 Para aprofundar.
- Desafio format: `### ⭐⭐ Título` / `Tags: a, b` / context paragraph / `**Critérios de pronto**` list / `<details><summary>Pistas</summary>` numbered hints. Tags come from ESPECIFICACAO §2.2.
- Stack versions and pitfalls (Vuetify 4, Express 5, Firebase modular, Supabase RLS, Swagger `definition`) are in ESPECIFICACAO §5–§6 — check before writing example code.
- Running projects: site do evento acadêmico (N1), Café Cerrado (N2), UniEventos (N3). Students build an authorial project with the same architecture.

## Raw sources kept for reference

`docs/fontes-brutas/apostila-idw.txt` (text of the original Nível 1 PDF handbook), `docs/fontes-brutas/dsw/*.txt` (Nível 2 handouts) and `DSW-CLAUDE.md`, `docs/fontes-brutas/10-projetos.txt`, `docs/fontes-brutas/ESPECIFICACAO-FDS.md`; official course plans in `docs/planos/`.
