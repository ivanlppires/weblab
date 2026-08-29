# WebLab — Apostila online de Desenvolvimento Web (weblab.ivanpires.dev)

**Data:** 2026-08-29 · **Autor:** Prof. Ivan Luiz Pedroso Pires (com Claude Code) · **Status:** aprovado para implementação (execução autônoma via `/goal`)

## 1. Objetivo

Publicar em **https://weblab.ivanpires.dev** uma apostila online, gratuita e autocontida, que ensine desenvolvimento web em **três níveis** mais uma trilha transversal de **Deploy & Ferramentas**, com **muitos exercícios desafiadores** que instiguem curiosidade e vontade de superação, e com **links úteis** curados. A base de conteúdo são os três Planos de Curso 2026.2 da UNEMAT/Sinop (curso TADS/SI) ministrados pelo professor:

| Nível | Disciplina de origem | Carga | Aulas |
|---|---|---|---|
| **Nível 1 — Introdução ao Desenvolvimento Web** | FACET-SNP-319 (sem pré-requisito) | 60h | 15 |
| **Nível 2 — Desenvolvimento Web (intermediário → avançado)** | FACET-SNP-307 (pré-req. 319) | 60h | 16 |
| **Nível 3 — Frameworks Modernos (front e back)** | FACET-SNP-310 (pré-req. 307) | 60h | 15 |
| **Deploy & Ferramentas — colocando tudo online** | transversal (novo) | — | 11 capítulos |

Fontes reaproveitadas (todas em `~/Documents/UNEMAT/Ensino/`):

- `2026.2/idw/Apostila_Introducao_Desenvolvimento_Web_UNEMAT_2026-2.pdf` (143 p., 15 aulas, exercícios em níveis A/B/C) → base do Nível 1.
- `2026.2/dsw/Aula_01..16_*.pdf` (handouts de 3–4 p.) + `dsw/CLAUDE.md` (fio-condutor "Café Cerrado", projeto incremental) → base do Nível 2 (precisa de expansão forte).
- `2026.2/fds/MaterialFACETSNP3102026.2/material/aulas/*.md` (15 aulas, 900–1.360 linhas cada, spec `ESPECIFICACAO.md`, pipeline `build_html.py`/`build_single.py`) → base do Nível 3 (reaproveitado quase integralmente) e do pipeline.
- `10_projetos_html_css_javascript (1).pdf` → projetos integradores do Banco de Desafios.

## 2. Decisões de design

1. **Site estático autocontido**, gerado de Markdown por um pipeline Python (evolução do `build_html.py` do FDS). Sem framework JS, sem dependências externas em runtime (CSS/JS inline; fontes do sistema). Funciona offline e imprime bem.
2. **Conteúdo atemporal + cronograma separado.** As aulas não trazem datas no corpo (exceto a Aula 01 de cada nível, que apresenta a disciplina). O índice de cada nível tem a tabela "Cronograma 2026.2" (datas e prazos literais do Plano de Curso). Assim a apostila serve a semestres futuros trocando só a tabela.
3. **Um projeto fio-condutor por nível**, construído incrementalmente pelo professor; o estudante replica a arquitetura em um **projeto autoral** de domínio próprio (regra herdada do FDS e do DSW):
   - Nível 1: **site institucional de um evento acadêmico** (5 páginas: início, programação, inscrição, palestrantes, contato) — mesmo tema da apostila IDW.
   - Nível 2: **Café Cerrado** — cafeteria fictícia: site estático → SPA client-side com `produtos` → API Express + OAuth Google + CRUD.
   - Nível 3: **UniEventos** — plataforma de eventos acadêmicos em Vue 3 + Vuetify + Pinia + Express + MySQL/Supabase + Firebase Auth.
   - Deploy & Ferramentas: publica os três projetos acima (estático, API Node, banco) e ensina as ferramentas do ofício.
4. **Exercícios são o centro.** Cada aula tem quatro camadas de prática, sempre nesta ordem: `💻 Mão na massa` (guiado) → `🧪 Laboratório` (níveis A fixação / B aplicação / C desafio, feitos em sala) → `🏆 Desafios` (extras, ⭐ a ⭐⭐⭐, com pistas mas sem solução, e um `🔥 Boss` por unidade) → `🏠 Atividade assíncrona`. Desafios são agregados automaticamente no **Banco de Desafios** (`/desafios/`).
5. **Curiosidade como recurso didático:** callouts `🧠 Você sabia?` (fato surpreendente ligado ao conteúdo) e `🔬 Investigue` (experimento de 5 minutos no DevTools/terminal) em toda aula; desafios com enunciado aberto e "critérios de pronto" no lugar de passo a passo.
6. **Progresso local:** checkbox "Concluí esta aula" e "✔ Feito" em cada desafio, persistidos em `localStorage`; barra de progresso por nível na home. Sem backend, sem login.
7. **Hospedagem no VPS existente** (`ivanpires.dev`, Contabo, nginx + certbot): vhost dedicado `weblab.ivanpires.dev` servindo `/home/webmaster/apps/weblab/site/`. Publicação por `rsync` (`deploy.sh`). Fonte versionada em Git e espelhada em GitHub público (`ivanlppires/weblab`), como já se fez com o material do FDS.

Alternativas descartadas: (a) GitHub Pages com CNAME — funcionaria, mas o DNS de `weblab.` já aponta para o VPS e o professor hospeda lá os projetos dos alunos (`/dsw/gN/`), então centralizar simplifica; (b) gerador pronto (MkDocs/Docusaurus/VitePress) — traria dependências e tema genérico; o pipeline próprio já existe, é testado e dá controle total sobre a extração de desafios e o lint de conteúdo.

## 3. Arquitetura do repositório

```
tutorialonline/                      (raiz do repo git; GitHub: ivanlppires/weblab)
├── README.md · CLAUDE.md · .gitignore
├── docs/
│   ├── planos/Plano_de_Curso_*.pdf  (3 planos de curso, fonte da verdade para datas)
│   └── superpowers/specs|plans/     (este documento e o plano de implementação)
├── fontes/                          ★ conteúdo canônico (Markdown)
│   ├── ESPECIFICACAO.md             regras editoriais para quem escreve aulas
│   ├── nivel-1/aula-01-….md … aula-15-….md
│   ├── nivel-2/aula-01-….md … aula-16-….md
│   ├── nivel-3/aula-01-….md … aula-15-….md
│   ├── deploy/cap-01-….md … cap-11-….md
│   ├── desafios/projetos-integradores.md
│   ├── links.md
│   └── home.md                      texto da página inicial (hero, como usar, trilha)
├── build/
│   ├── config.py                    trilhas, aulas, unidades, marcos de avaliação, cronograma 2026.2
│   ├── build.py                     gera site/ inteiro
│   ├── lint.py                      valida fontes (seções obrigatórias, mínimos, links)
│   ├── theme.css · app.js           design system e comportamento (inlinados no build)
│   └── tests/test_build.py          testes do pipeline (pytest)
├── site/                            saída gerada (gitignored)
└── deploy.sh                        rsync → servidor
```

## 4. Site gerado (`site/`)

| URL | Página | Gerada de |
|---|---|---|
| `/` | Home: hero, mapa das trilhas (cards), "como usar", progresso local, busca | `fontes/home.md` + config |
| `/nivel-1/` `/nivel-2/` `/nivel-3/` | Índice do nível: ementa, projeto fio-condutor, unidades, cards das aulas, cronograma 2026.2, avaliações, stack/versões | config + `aula-01` |
| `/nivel-N/aula-NN.html` | Página da aula (sidebar do nível, sumário lateral, navegação anterior/próxima) | `fontes/nivel-N/aula-NN-*.md` |
| `/nivel-N/apostila.html` | Apostila do nível em arquivo único (leitura corrida, projeção, offline, Ctrl+P) | idem |
| `/deploy/` e `/deploy/cap-NN.html` | Trilha Deploy & Ferramentas (mesmo layout de aula) | `fontes/deploy/*.md` |
| `/desafios/` | Banco de Desafios: todos os `🏆` extraídos das aulas + projetos integradores; filtros por nível, tema (tag) e dificuldade; contador de feitos | extração no build + `desafios/projetos-integradores.md` |
| `/links/` | Links úteis por categoria, cada um com uma linha de "por que usar" | `fontes/links.md` |
| `/busca.json` | Índice de busca (título, nível, cabeçalhos h2/h3, títulos de desafios) consumido pela caixa de busca global | build |
| `/404.html`, `/sitemap.xml`, `/robots.txt` | utilitários | build |

Recursos de interface (herdados do FDS e ampliados): tema claro/escuro persistido; botão **Copiar** em todo bloco de código; sumário lateral com destaque da seção visível; barra de progresso de leitura; atalhos `j`/`k`/`/`/`Esc`; impressão limpa; responsivo (sidebar vira menu em telas pequenas); links âncora nos títulos; **busca global**; **progresso local** (aulas concluídas e desafios feitos).

Identidade visual: nome **WebLab · Laboratório de Desenvolvimento Web**; cor de destaque por trilha (N1 teal, N2 indigo, N3 fúcsia, Deploy âmbar, Desafios rosa); estética de "caderno de laboratório" — fundo papel/azul-noite, tipografia de sistema com acentos monoespaçados, badges de dificuldade ⭐. Definida em `build/theme.css`; a skill `frontend-design` orienta a execução.

## 5. Modelo de conteúdo

### 5.1 Estrutura obrigatória de cada aula (`fontes/nivel-N/aula-NN-slug.md`)

```
# Aula NN — Título
## 🎯 Objetivos de aprendizagem          5–7 objetivos com verbos observáveis
## 📋 Pré-requisitos                     checklist do que precisa estar funcionando
## 🗺️ Roteiro                            tabela: 3 blocos de 50 min
## 1. … ## n.  Seções teóricas           porquê antes do como; código completo e comentado, caminho do arquivo acima do bloco
   (callouts: 💡 Dica · ⚠️ Atenção · 🔎 Por baixo do capô · 📌 Na prova · 🧠 Você sabia? · 🔬 Investigue)
## 💻 Mão na massa — <passo do projeto>  passo a passo numerado no projeto fio-condutor
## 🧪 Laboratório                        Nível A (≥4 fixação) · Nível B (≥3 aplicação) · Nível C (≥1 desafio em sala); cada item com resultado esperado; dica em <details>
## 🏆 Desafios                           ≥3 desafios extras: "### ⭐ Título", "### ⭐⭐ Título", "### ⭐⭐⭐ Título"; cada um com contexto, critérios de pronto e <details>Pistas</details>; tags na linha `Tags: html, css`; última aula de cada unidade traz "### 🔥 Boss — Título"
## 🐛 Erros comuns                       tabela sintoma → causa → solução
## 🏠 Atividade assíncrona (1 h)         tarefa objetiva com critério de pronto, ligada ao projeto autoral, entrega no SIGAA
## ✅ Checkpoint do projeto              checklist do que deve estar no repositório ao fim da aula
## 📚 Para aprofundar                    links oficiais (MDN/web.dev/docs) + bibliografia do plano
(aulas de fechamento de unidade) ## 📝 Avaliação N — rubrica de 10 pontos, formato de entrega, política de atraso e de IA
```

Capítulos de Deploy seguem a mesma estrutura, trocando "Mão na massa" por um passo a passo real de publicação e o "Checkpoint" por "✅ Está no ar quando…".

### 5.2 Regras editoriais (detalhadas em `fontes/ESPECIFICACAO.md`)

- Português do Brasil; identificadores em português; tom direto; sem "vamos agora".
- 900–1.500 linhas por aula (sustenta 150 min). Código completo e executável, com linguagem declarada em todo fence; nunca `// ...resto`.
- Versões verificadas (Node 22/24, Vue 3.5, Vite 8, Vuetify 4, Vue Router 5, Pinia 4, Express 5, mysql2, Firebase 12 modular, supabase-js 2) — a tabela e as armadilhas (Vuetify 4, Express 5) do `ESPECIFICACAO.md` do FDS são incorporadas.
- Continuidade: cada aula retoma a anterior em 3 linhas e anuncia a próxima, sem datas.
- Desafios: enunciado aberto + critérios de pronto + pistas; nunca a solução; sempre um gancho de curiosidade ("por que o navegador faz isso?"); variação de formato (investigação no DevTools, refatoração, bug plantado, performance, acessibilidade, mini-projeto).
- Tabelas com no máximo 4 colunas.

### 5.3 Extração automática de desafios

O build lê a seção `## 🏆 Desafios` de cada aula; cada `### ⭐{1,3} Título` (ou `### 🔥 Boss — Título`) vira um item com: nível/trilha, aula (link com âncora), dificuldade, título, primeiro parágrafo (resumo), tags. Falta de tags ou de critérios de pronto → erro de lint.

## 6. Pipeline (`build/`)

- `config.py`: `TRILHAS = {"nivel-1": {...}, ...}` com nome, cor, descrição, projeto fio-condutor, unidades, lista de aulas `(num, slug, título, unidade, avaliacao?)`, cronograma 2026.2 (datas literais dos planos), stack.
- `build.py`: Markdown (python-markdown: fenced_code, codehilite/pygments, tables, toc, attr_list, md_in_html) → HTML; pós-processamento `enfeitar()` (callouts por emoji, blocos de código com cabeçalho e botão copiar, tabelas roláveis, escape de tags cruas); templates de página; índices; apostila única por trilha; banco de desafios; links; home; `busca.json`; sitemap. Ids de cabeçalho prefixados por aula na apostila única.
- `lint.py`: para cada fonte, verifica seções obrigatórias e ordem, mínimos (A≥4, B≥3, C≥1, desafios≥3), fences com linguagem, ausência de placeholders (`...resto`, `TODO`, `TBD`), tamanho (≥600 linhas para aula; ≥400 para capítulo de deploy), links internos resolvíveis, tabelas ≤4 colunas. `build.py` chama o lint e falha se houver erro.
- `tests/test_build.py` (pytest): `enfeitar()` (callouts, blocos), extração de desafios, geração de ids únicos, lint (fixtures com erros conhecidos), links internos do site gerado.
- Comandos: `python3 build/build.py` (lint + build), `python3 build/lint.py` (só lint), `pytest build/tests`, `./deploy.sh`.

## 7. Deploy

1. **Servidor** (uma vez, com root via `docker run --privileged … redis:7-alpine chroot /host`): criar `/etc/nginx/sites-available/weblab.ivanpires.dev` (server_name, `root /home/webmaster/apps/weblab/site`, `index index.html`, `try_files $uri $uri/ $uri.html =404`, `error_page 404 /404.html`, gzip, cache 1h para html e 7d para json), symlink em `sites-enabled`, `nginx -t && systemctl reload nginx`, `certbot --nginx -d weblab.ivanpires.dev --non-interactive --agree-tos -m ivanpires@gmail.com --redirect`. Renovação automática já existe (certbot timer) — confirmar com `certbot renew --dry-run`.
2. **Publicação** (sempre): `deploy.sh` = `python3 build/build.py && rsync -az --delete site/ webmaster@ivanpires.dev:/home/webmaster/apps/weblab/site/`.
3. **Verificação**: `curl -sI https://weblab.ivanpires.dev/` → 200 + certificado válido para `weblab.ivanpires.dev`; abrir home, um índice, uma aula, a apostila única, desafios e links em Chrome headless e conferir capturas (desktop 1280 e mobile 390); checar `busca.json` e 404.

## 8. Produção do conteúdo

Volume: N1 15 aulas (converter/enriquecer a partir da apostila IDW), N2 16 aulas (expandir handouts DSW para o formato completo), N3 15 aulas (reaproveitar FDS; remover linha de data do cabeçalho; **adicionar** `🏆 Desafios` e callouts de curiosidade), Deploy 11 capítulos (novos), projetos integradores (10, do PDF, adaptados com critérios e extensões), links (~60). Escrita por subagentes em paralelo, cada um com o `ESPECIFICACAO.md`, o texto-fonte extraído dos PDFs (`scratchpad/fontes-pdf/`) e uma aula-modelo; o lint valida cada entrega; revisão de amostra pelo orquestrador.

Capítulos de Deploy & Ferramentas (ordem):

1. Caixa de ferramentas do dev web — terminal, VS Code e extensões, DevTools, Live Server, Node/npm/nvm, gerenciando versões.
2. Git e GitHub do zero ao pull request — fluxo, branches, `.gitignore`, mensagens, `gh` CLI, resolvendo conflitos.
3. Publicando sites estáticos — GitHub Pages, Netlify, Vercel, Cloudflare Pages; `.nojekyll`, SPA fallback, cache.
4. Domínios, DNS e HTTPS — registros A/CNAME/TXT, propagação, Let's Encrypt, Cloudflare, subdomínios para projetos.
5. Publicando o back-end Node — Render, Railway, Fly.io; variáveis de ambiente; `PORT`; healthcheck; logs; cold start.
6. Servidor próprio (VPS) — Ubuntu, SSH com chaves, nginx como reverse proxy, pm2/systemd, certbot; o laboratório `ivanpires.dev/dsw/gN` como exemplo real.
7. Docker para desenvolvedores web — imagens, Dockerfile de app Node e de site estático, `docker compose` com app + banco, volumes, `.dockerignore`.
8. Bancos de dados na nuvem — Supabase, Neon, MySQL gerenciado, connection strings, migrações, backups, seeds.
9. CI/CD com GitHub Actions — lint/test/build em cada push, deploy automático, preview deploys, segredos.
10. Qualidade, performance e observabilidade — Lighthouse, Web Vitals, UptimeRobot, Sentry, analytics com privacidade; segurança básica (HTTPS, headers, CORS, rate limit, segredos fora do repo).
11. IA como ferramenta de desenvolvimento — assistentes no editor, prompts úteis, revisão crítica do que a IA gera, política de uso nas avaliações.

## 9. Fora de escopo (YAGNI)

Login, backend, comentários, fórum, autoavaliação corrigida automaticamente, PDF gerado no build (o navegador imprime), i18n, tema por usuário além de claro/escuro, analytics.

## 10. Critérios de aceite

- `https://weblab.ivanpires.dev/` responde 200 com HTTPS válido e mostra a home com as 3 trilhas + Deploy + Desafios + Links.
- 57 páginas de aula/capítulo (15+16+15+11) publicadas, todas passando no lint (estrutura completa, ≥4 A / ≥3 B / ≥1 C, ≥3 desafios, código com linguagem, sem placeholders).
- Banco de Desafios com ≥170 desafios extraídos + 10 projetos integradores, filtráveis.
- Links úteis com ≥50 links em ≥8 categorias, todos com justificativa.
- Cronograma 2026.2 de cada nível idêntico ao Plano de Curso (datas e prazos literais).
- Busca global, tema claro/escuro, progresso local e apostila única por nível funcionando; layout ok em 1280px e 390px.
- Repositório com README e CLAUDE.md descrevendo como editar e republicar (`build` → `deploy.sh`).
