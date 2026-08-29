# WebLab Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publicar em https://weblab.ivanpires.dev uma apostila online de desenvolvimento web em 3 níveis + trilha Deploy & Ferramentas + Banco de Desafios + Links úteis, gerada de Markdown por um pipeline Python próprio.

**Architecture:** Fontes Markdown em `fontes/<trilha>/`, metadados em `build/config.py`, renderização em `build/render.py` (md → html + pós-processamento + extração de desafios), validação em `build/lint.py`, montagem das páginas em `build/build.py` (templates inline, CSS/JS de `build/theme.css` e `build/app.js`), saída em `site/`, publicação por `rsync` no VPS (`deploy.sh`). Conteúdo escrito por subagentes seguindo `fontes/ESPECIFICACAO.md`.

**Tech Stack:** Python 3.12, `markdown` 3.5, `pygments` 2.17, `pytest`; HTML/CSS/JS puro (sem dependências em runtime); nginx + certbot no VPS Ubuntu 22.04; rsync; git + gh.

**Spec:** `docs/superpowers/specs/2026-08-29-weblab-design.md`

## Global Constraints

- Idioma de todo conteúdo e UI: português do Brasil.
- Site autocontido: nenhum `<script src>`/`<link href>` externo; CSS e JS inlinados.
- URLs: `/`, `/nivel-1/`, `/nivel-2/`, `/nivel-3/`, `/deploy/`, `/desafios/`, `/links/`; páginas `aula-NN.html` (níveis) e `cap-NN.html` (deploy); `apostila.html` por nível.
- Aulas: 900–1.500 linhas; capítulos de deploy: 600–1.000 linhas; lint exige ≥600 / ≥400.
- Laboratório: ≥4 itens Nível A, ≥3 Nível B, ≥1 Nível C. Desafios: ≥3 por aula (`### ⭐`, `### ⭐⭐`, `### ⭐⭐⭐`), cada um com linha `Tags:` e bloco `**Critérios de pronto**` e `<details><summary>Pistas</summary>`.
- Todo fence de código com linguagem. Sem `...resto`, `TODO`, `TBD`. Tabelas ≤ 4 colunas.
- Datas 2026.2 só em `build/config.py` (cronograma) e na Aula 01 de cada nível; demais aulas sem datas.
- Versões: Node 22 LTS/24, Vue 3.5, Vite 8, Vuetify 4, Vue Router 5, Pinia 4, Express 5, mysql2 3, Firebase 12 (API modular), supabase-js 2, swagger-jsdoc 6 (`definition`).
- Servidor: `webmaster@ivanpires.dev`; site em `/home/webmaster/apps/weblab/site/`; root apenas via `docker run --rm -i --privileged --pid=host --net=host -v /:/host redis:7-alpine chroot /host /bin/bash`.
- Commits frequentes; mensagens terminam com o trailer `Co-Authored-By` da sessão.

---

## File map

| Arquivo | Responsabilidade |
|---|---|
| `build/config.py` | Dados: trilhas, aulas (num, slug, título, unidade, avaliação), unidades, cronograma 2026.2, avaliações, stack, cores. Funções `trilha(id)`, `aulas(id)`, `arquivo_fonte(trilha, num)`. |
| `build/render.py` | `converter(md_texto) -> str` (HTML bruto), `enfeitar(html) -> str`, `extrair_desafios(md_texto, trilha, num) -> list[dict]`, `sumario(html) -> list[(nivel, id, texto)]`, `remover_cabecalho(md) -> str`. |
| `build/lint.py` | `lint_aula(texto, tipo) -> list[str]` (erros), `lint_tudo() -> int` (CLI: imprime erros, retorna código de saída). |
| `build/theme.css`, `build/app.js` | Design system e comportamento do site (lidos e inlinados por `build.py`). |
| `build/paginas.py` | Templates: `pagina_base(...)`, `pagina_aula(...)`, `pagina_indice_trilha(...)`, `pagina_home(...)`, `pagina_desafios(...)`, `pagina_links(...)`, `apostila_unica(...)`. Só monta strings HTML. |
| `build/build.py` | Orquestra: lint → renderiza tudo → escreve `site/` → `busca.json`, `sitemap.xml`, `robots.txt`, `404.html` → checa links internos. |
| `build/tests/test_render.py`, `test_lint.py`, `test_build.py` | pytest. |
| `fontes/ESPECIFICACAO.md` | Regras editoriais para quem escreve aulas (subagentes). |
| `fontes/nivel-1/`, `nivel-2/`, `nivel-3/`, `deploy/`, `desafios/projetos-integradores.md`, `links.md`, `home.md` | Conteúdo. |
| `deploy.sh` | build + rsync. |
| `README.md`, `CLAUDE.md` | Como editar e republicar. |

---

### Task 1: Config das trilhas e especificação editorial

**Files:**
- Create: `build/config.py`, `build/__init__.py`, `fontes/ESPECIFICACAO.md`, `build/tests/__init__.py`, `build/tests/test_config.py`

**Interfaces:**
- Produces: `TRILHAS: dict[str, dict]`, `trilha(id) -> dict`, `aulas(id) -> list[dict]` (cada aula: `num:str`, `slug:str`, `titulo:str`, `unidade:int`, `avaliacao:int|None`, `arquivo:str`, `pagina:str`), `CRONOGRAMA: dict[str, list[dict]]` (`data`, `num`, `descricao`, `prazo:bool`), `AVALIACOES: dict[str, list[dict]]`, `FONTES = Path(repo)/"fontes"`, `SITE = Path(repo)/"site"`.

- [ ] **Step 1: Teste de config**

```python
# build/tests/test_config.py
from build import config

def test_trilhas_e_quantidades():
    assert list(config.TRILHAS) == ["nivel-1", "nivel-2", "nivel-3", "deploy"]
    assert len(config.aulas("nivel-1")) == 15
    assert len(config.aulas("nivel-2")) == 16
    assert len(config.aulas("nivel-3")) == 15
    assert len(config.aulas("deploy")) == 11

def test_aula_tem_campos_e_arquivo():
    a = config.aulas("nivel-1")[0]
    assert a["num"] == "01" and a["unidade"] == 1 and a["pagina"] == "aula-01.html"
    assert a["arquivo"].startswith("aula-01-")
    d = config.aulas("deploy")[0]
    assert d["pagina"] == "cap-01.html"

def test_cronograma_literal_do_plano():
    n1 = config.CRONOGRAMA["nivel-1"]
    assert n1[0]["data"] == "11/08/2026" and n1[-1]["data"] == "17/11/2026"
    n2 = config.CRONOGRAMA["nivel-2"]
    assert n2[0]["data"] == "11/08/2026" and n2[-1]["data"] == "24/11/2026"
    n3 = config.CRONOGRAMA["nivel-3"]
    assert n3[0]["data"] == "10/08/2026" and n3[-1]["data"] == "14/12/2026"

def test_avaliacoes_marcadas_nas_aulas():
    marcadas = [a["num"] for a in config.aulas("nivel-2") if a["avaliacao"]]
    assert marcadas == ["06", "10", "16"]
```

- [ ] **Step 2: Rodar e ver falhar** — `pytest build/tests/test_config.py -q` → `ModuleNotFoundError`.

- [ ] **Step 3: Escrever `build/config.py`** com as listas abaixo (títulos e datas literais dos Planos de Curso em `docs/planos/`):

Nível 1 (FACET-SNP-319, terças 19h–22h, 11/08→17/11/2026; avaliações nas aulas 06, 10 e 15 — envio de A1 em 15/09, A2 em 13/10, A3 em 17/11): 01 Apresentação, tecnologias e arquitetura web · 02 Introdução ao HTML: estrutura, textos, links, tabelas · 03 Introdução aos formulários · 04 Formulários, mídias e listas · 05 Elementos HTML para layout e introdução ao CSS · 06 CSS: sintaxe, seletores, classes, atributos e valores · 07 Formatando o layout de um website e o menu · 08 Criando telas responsivas · 09 Animações e efeitos em CSS · 10 Introdução ao JavaScript · 11 Variáveis, operações aritméticas e estruturas de controle · 12 Estruturas sequenciais, condicionais e de repetição · 13 Funções e eventos · 14 JavaScript para validação de formulários e consultas dinâmicas · 15 Publicando seu website na internet. Unidades: 1 = aulas 01–05, 2 = 06–09, 3 = 10–15.

Nível 2 (FACET-SNP-307, segundas, 11/08→24/11/2026; prazos A1 29/09, A2 27/10, A3 24/11; aulas de avaliação 06, 10, 16): 01 Apresentação, arquitetura web, ambiente e Git · 02 Introdução ao desenvolvimento web moderno · 03 Revisão de HTML: layout, links e formulários · 04 Frameworks CSS: Bootstrap, Tailwind e Material · 05 Animação e SVG · 06 Acessibilidade e ARIA · 07 Revisão de JavaScript: objetos, funções, eventos e DOM · 08 Arrow functions, callbacks e operações em vetores · 09 Promises e async/await · 10 AJAX, JSON e Single Page Application · 11 Introdução ao Node.js e Express · 12 Express estruturado e middlewares · 13 Rotas e controladores · 14 Autenticação com Google (OAuth 2.0) · 15 CRUD com front-end assíncrono · 16 CRUD completo com autenticação e entrega final. Unidades: 1 = 01–06, 2 = 07–10, 3 = 11–16.

Nível 3 (FACET-SNP-310, quartas, 10/08→14/12/2026 conforme plano; avaliações nas aulas 04, 08 e 15): usar a lista `AULAS` de `~/Documents/UNEMAT/Ensino/2026.2/fds/MaterialFACETSNP3102026.2/material/build_html.py`. Unidades: 1 = 01–04, 2 = 05–06, 3 = 07–15.

Deploy (11 capítulos, sem cronograma): 01 Caixa de ferramentas do dev web · 02 Git e GitHub do zero ao pull request · 03 Publicando sites estáticos · 04 Domínios, DNS e HTTPS · 05 Publicando o back-end Node · 06 Servidor próprio (VPS) com nginx · 07 Docker para desenvolvedores web · 08 Bancos de dados na nuvem · 09 CI/CD com GitHub Actions · 10 Qualidade, performance e observabilidade · 11 IA como ferramenta de desenvolvimento.

Estrutura:

```python
from pathlib import Path
RAIZ = Path(__file__).resolve().parent.parent
FONTES = RAIZ / "fontes"
SITE = RAIZ / "site"

def _aulas(trilha, prefixo, itens, unidades, avaliacoes):
    out = []
    for num, slug, titulo in itens:
        unidade = next(u for u, (a, b) in unidades.items() if a <= int(num) <= b)
        out.append({"num": num, "slug": slug, "titulo": titulo, "unidade": unidade,
                    "avaliacao": avaliacoes.get(num), "arquivo": f"{prefixo}-{num}-{slug}.md",
                    "pagina": f"{prefixo}-{num}.html", "trilha": trilha})
    return out

TRILHAS = {
  "nivel-1": {"id": "nivel-1", "nome": "Nível 1 — Introdução ao Desenvolvimento Web", "curto": "Nível 1",
              "cor": "n1", "codigo": "FACET-SNP-319", "prefixo": "aula", "resumo": "...", "projeto": "...",
              "unidades": {1: "Arquitetura web e HTML", 2: "CSS", 3: "JavaScript"},
              "aulas": _aulas(...)},
  ...
}
def trilha(id): return TRILHAS[id]
def aulas(id): return TRILHAS[id]["aulas"]
```

- [ ] **Step 4: Rodar testes** — `pytest build/tests/test_config.py -q` → 4 passed.

- [ ] **Step 5: Escrever `fontes/ESPECIFICACAO.md`** — adaptar o `ESPECIFICACAO.md` do FDS para o WebLab: identidade (WebLab, quatro trilhas, projetos fio-condutor por trilha), §Estrutura obrigatória (a do spec §5.1, com exemplo completo de um `### ⭐⭐` desafio), §Filosofia dos desafios (aberto, critérios de pronto, pistas, curiosidade, formatos variados, boss), §Callouts (`> **💡 Dica**`, `> **⚠️ Atenção**`, `> **🔎 Por baixo do capô**`, `> **📌 Na prova**`, `> **🧠 Você sabia?**`, `> **🔬 Investigue**`), §Stack e versões (tabela do FDS) + §Armadilhas (Vuetify 4, Express 5, Firebase modular, Supabase RLS, Swagger), §Regras de escrita (sem datas, tamanho, fences, tabelas ≤4 colunas, caminho do arquivo acima do bloco), §Aula-modelo (apontar `fontes/nivel-3/aula-06-axios-e-pinia.md` depois da Task 6).

- [ ] **Step 6: Commit** — `git add build fontes && git commit -m "build: config das trilhas e especificação editorial"`.

---

### Task 2: Renderização Markdown → HTML e extração de desafios

**Files:**
- Create: `build/render.py`, `build/tests/test_render.py`

**Interfaces:**
- Produces: `converter(md: str) -> str`; `enfeitar(html: str) -> str`; `remover_cabecalho(md: str) -> str` (remove o H1 e o blockquote de cabeçalho do FDS e linhas `**Data:**`); `sumario(html: str) -> list[tuple[str,str,str]]` (nível, id, texto); `extrair_desafios(md: str, trilha: str, aula: dict) -> list[dict]` com chaves `id, trilha, aula_num, aula_titulo, pagina, ancora, dificuldade (1|2|3|"boss"), titulo, resumo, tags:list[str]`; `prefixar_ids(html, prefixo) -> str`.

- [ ] **Step 1: Testes**

```python
# build/tests/test_render.py
from build import render

MD = """# Aula 01 — Teste

> **cabeçalho** · Unidade 1
> **Data:** 10/08/2026

## 1. Seção

> **💡 Dica**
> Use `const`.

```js
const x = 1;
```

| a | b |
|---|---|
| 1 | 2 |

## 🏆 Desafios

### ⭐ Primeiro desafio
Tags: html, css

Texto do desafio com um gancho.

**Critérios de pronto**

- item

<details><summary>Pistas</summary>

- pista
</details>

### ⭐⭐⭐ Terceiro
Tags: js

Resumo do terceiro.

**Critérios de pronto**

- x

<details><summary>Pistas</summary>
p
</details>

### 🔥 Boss — Chefão
Tags: js, api

Resumo boss.

**Critérios de pronto**

- y

<details><summary>Pistas</summary>
p
</details>
"""

def test_converter_e_enfeitar_callout_e_codigo():
    html = render.enfeitar(render.converter(MD))
    assert 'blockquote class="dica"' in html
    assert 'class="bloco"' in html and 'Copiar' in html and 'JavaScript' in html
    assert '<div class="tabela-wrap"><table>' in html

def test_remover_cabecalho():
    corpo = render.remover_cabecalho(MD)
    assert not corpo.lstrip().startswith("# Aula")
    assert "**Data:**" not in corpo and "## 1. Seção" in corpo

def test_sumario():
    html = render.converter(MD)
    itens = render.sumario(html)
    assert ("2", "1-secao", "1. Seção") in itens

def test_extrair_desafios():
    aula = {"num": "01", "titulo": "Teste", "pagina": "aula-01.html"}
    ds = render.extrair_desafios(MD, "nivel-1", aula)
    assert [d["dificuldade"] for d in ds] == [1, 3, "boss"]
    assert ds[0]["tags"] == ["html", "css"] and ds[0]["resumo"].startswith("Texto do desafio")
    assert ds[2]["titulo"] == "Chefão" and ds[2]["pagina"] == "aula-01.html"
    assert ds[0]["ancora"] == "primeiro-desafio"

def test_prefixar_ids():
    html = '<h2 id="x">X</h2><a href="#x">l</a>'
    out = render.prefixar_ids(html, "a01")
    assert 'id="a01-x"' in out and 'href="#a01-x"' in out
```

- [ ] **Step 2: Rodar e ver falhar** — `pytest build/tests/test_render.py -q`.

- [ ] **Step 3: Implementar `build/render.py`** — portar `enfeitar()` do `build_html.py` do FDS (callouts por emoji, incluindo 🧠→`saiba` e 🔬→`investigue`; blocos de código com rótulo de linguagem e botão Copiar; tabelas roláveis; escape de tags cruas). `converter()` usa `markdown.Markdown(extensions=["fenced_code","codehilite","tables","toc","attr_list","sane_lists","md_in_html"], extension_configs={"codehilite": {"guess_lang": False, "css_class": "codehilite"}, "toc": {"permalink": "¶", "permalink_class": "anchor", "slugify": slug_pt}})`, com `slug_pt` removendo acentos (unicodedata NFKD) e emojis. `extrair_desafios()` trabalha no Markdown: localiza `## 🏆 Desafios` até o próximo `## `, divide por `^### `, lê dificuldade pelo prefixo (`⭐`×n ou `🔥 Boss —`), título, linha `Tags:`, primeiro parágrafo sem `Tags:` como resumo (máx. 220 chars), e âncora = `slug_pt(título)` (o mesmo slugify do toc, aplicado ao título completo do H3 incluindo emojis removidos — garantir que o id gerado pelo markdown para `### ⭐ Primeiro desafio` seja `primeiro-desafio`).

- [ ] **Step 4: Rodar testes** — 5 passed.

- [ ] **Step 5: Commit** — `git commit -m "build: render (markdown→html, callouts, extração de desafios)"`.

---

### Task 3: Lint de conteúdo

**Files:**
- Create: `build/lint.py`, `build/tests/test_lint.py`

**Interfaces:**
- Produces: `lint_texto(texto: str, tipo: "aula"|"deploy"|"livre") -> list[str]`; `lint_arquivo(path, tipo) -> list[str]`; `lint_tudo() -> list[str]`; CLI `python3 build/lint.py` (exit 1 se erros).

Regras (`tipo == "aula"`): seções obrigatórias em ordem — `## 🎯 Objetivos de aprendizagem`, `## 📋 Pré-requisitos`, `## 🗺️ Roteiro`, `## 💻 Mão na massa`, `## 🧪 Laboratório`, `## 🏆 Desafios`, `## 🐛 Erros comuns`, `## 🏠 Atividade assíncrona`, `## ✅ Checkpoint`, `## 📚 Para aprofundar` (match por prefixo, ignorando variação após o emoji); Laboratório com ≥4 linhas `**A\d+.` ou `A\d+.`, ≥3 `B\d+.`, ≥1 `C\d+.`; ≥3 `### ⭐` (ou 🔥) em Desafios, cada um com `Tags:`, `**Critérios de pronto**` e `<details>`; todo ```` ``` ```` de abertura com linguagem; proibidos `...resto`, `// ...`, `TODO`, `TBD`, `Lorem`; ≥600 linhas; tabelas com >4 colunas (linha `|---|` com >4 células); `tipo == "deploy"`: mesmas seções exceto que `## 💻` pode ser `## 🚀 Passo a passo` e `## ✅ Checkpoint` pode ser `## ✅ Está no ar quando`; mínimo 400 linhas. `tipo == "livre"` (links, projetos, home): só fences e placeholders.

- [ ] **Step 1: Testes** (fixtures curtas construídas por função `aula_ok()` que gera uma aula válida sintética com 600+ linhas; variantes removendo cada requisito devem produzir a mensagem correspondente):

```python
from build import lint

def aula_ok():
    secs = ["## 🎯 Objetivos de aprendizagem", "## 📋 Pré-requisitos", "## 🗺️ Roteiro", "## 1. Teoria",
            "## 💻 Mão na massa — passo", "## 🧪 Laboratório", "## 🏆 Desafios", "## 🐛 Erros comuns",
            "## 🏠 Atividade assíncrona (1 h)", "## ✅ Checkpoint do projeto", "## 📚 Para aprofundar"]
    lab = "\n".join([f"**A{i}.** q" for i in range(1,5)] + [f"**B{i}.** q" for i in range(1,4)] + ["**C1.** q"])
    des = "\n".join(f"### {'⭐'*n} T{n}\nTags: x\n\ntexto\n\n**Critérios de pronto**\n\n- a\n\n<details><summary>Pistas</summary>\np\n</details>\n" for n in (1,2,3))
    corpo = {"## 🧪 Laboratório": lab, "## 🏆 Desafios": des}
    linhas = ["# Aula 01 — X"]
    for s in secs:
        linhas += [s, corpo.get(s, "texto"), ""]
    linhas += ["```js", "x", "```"] + ["linha"] * 600
    return "\n".join(linhas)

def test_aula_valida_sem_erros():
    assert lint.lint_texto(aula_ok(), "aula") == []

def test_falta_secao():
    erros = lint.lint_texto(aula_ok().replace("## 🐛 Erros comuns", "## Erros"), "aula")
    assert any("🐛" in e for e in erros)

def test_fence_sem_linguagem():
    erros = lint.lint_texto(aula_ok().replace("```js", "```"), "aula")
    assert any("sem linguagem" in e for e in erros)

def test_placeholder():
    erros = lint.lint_texto(aula_ok() + "\n// ...resto do código\n", "aula")
    assert any("placeholder" in e for e in erros)

def test_poucos_desafios_e_lab():
    t = aula_ok().replace("### ⭐⭐⭐ T3", "### T3").replace("**B3.** q", "")
    erros = lint.lint_texto(t, "aula")
    assert any("desafios" in e for e in erros) and any("Nível B" in e for e in erros)

def test_tabela_larga():
    t = aula_ok() + "\n| a | b | c | d | e |\n|---|---|---|---|---|\n| 1 | 2 | 3 | 4 | 5 |\n"
    assert any("colunas" in e for e in lint.lint_texto(t, "aula"))
```

- [ ] **Step 2: Rodar e ver falhar.**
- [ ] **Step 3: Implementar `build/lint.py`** (funções puras sobre texto; `lint_tudo()` itera `config.TRILHAS` e checa também existência de cada arquivo listado no config, reportando "arquivo ausente" como erro).
- [ ] **Step 4: Rodar testes** — 6 passed.
- [ ] **Step 5: Commit** — `git commit -m "build: lint de conteúdo"`.

---

### Task 4: Design system, templates e build das páginas

**Files:**
- Create: `build/theme.css`, `build/app.js`, `build/paginas.py`, `build/build.py`, `build/tests/test_build.py`
- Create (fixture mínima para o build rodar antes do conteúdo): nada — o build aceita aulas ausentes apenas com flag `--parcial` (gera o que existe e avisa); sem a flag, lint bloqueia.

**Interfaces:**
- `paginas.pagina_base(titulo, descricao, corpo, lateral_html, toc_html, trilha_id|None, raiz_rel, extra_head="", body_class="") -> str`
- `paginas.pagina_aula(trilha, aula, corpo_html, anterior, proxima, raiz_rel) -> str`
- `paginas.pagina_indice_trilha(trilha, resumo_html) -> str`
- `paginas.apostila_unica(trilha, secoes: list[dict(num, titulo, html, sumario)]) -> str`
- `paginas.pagina_home(home_html, progresso_ids) -> str`, `pagina_desafios(desafios, projetos_html)`, `pagina_links(links_html)`, `pagina_404()`
- `build.gerar(parcial: bool=False) -> None` escreve `site/`; `build.checar_links(site_dir) -> list[str]`.
- Progresso local: `app.js` usa chaves `weblab:aula:<trilha>/<pagina>` = "1" e `weblab:desafio:<id>` = "1"; a home lê `data-aulas` (JSON de ids por trilha) para calcular %.

- [ ] **Step 1: Testes do build** (usam `tmp_path` e fontes sintéticas via monkeypatch de `config.FONTES/SITE`; uma aula válida por trilha):

```python
from build import build, config

def test_build_parcial_gera_estrutura(tmp_path, monkeypatch):
    fontes = tmp_path / "fontes"; site = tmp_path / "site"
    for t in config.TRILHAS:
        (fontes / t).mkdir(parents=True)
        a = config.aulas(t)[0]
        (fontes / t / a["arquivo"]).write_text(AULA_MINIMA, encoding="utf-8")
    (fontes / "links.md").write_text("## Docs\n\n- [MDN](https://developer.mozilla.org) — referência.\n")
    (fontes / "home.md").write_text("Texto da home.\n")
    (fontes / "desafios").mkdir(); (fontes / "desafios" / "projetos-integradores.md").write_text("## Projeto\n\ntexto\n")
    monkeypatch.setattr(config, "FONTES", fontes); monkeypatch.setattr(config, "SITE", site)
    build.gerar(parcial=True)
    assert (site / "index.html").exists()
    for t in config.TRILHAS:
        assert (site / t / "index.html").exists() and (site / t / "apostila.html").exists()
        assert (site / t / config.aulas(t)[0]["pagina"]).exists()
    assert (site / "desafios" / "index.html").exists() and (site / "links" / "index.html").exists()
    assert (site / "busca.json").exists() and (site / "404.html").exists() and (site / "sitemap.xml").exists()
    html = (site / "nivel-1" / "aula-01.html").read_text()
    assert "<script src" not in html and '<link rel="stylesheet" href="http' not in html
    assert build.checar_links(site) == []
```

- [ ] **Step 2: Rodar e ver falhar.**
- [ ] **Step 3: `theme.css`** — usar a skill `frontend-design`. Tokens: `--bg`, `--bg-soft`, `--bg-code`, `--line`, `--fg`, `--fg-dim`, `--fg-faint`, `--accent` (por trilha via `html[data-trilha="nivel-1"]{--accent:...}`), cores das trilhas `--n1 #14b8a6`, `--n2 #6366f1`, `--n3 #d946ef`, `--deploy #f59e0b`, `--desafios #f43f5e`; tema claro/escuro por `html[data-tema]` com `prefers-color-scheme` como padrão. Layout de 3 colunas (`.lateral` 260px / `main` / `.toc` 240px) colapsando para 1 coluna < 900px com botão "☰ Aulas" que abre a lateral como painel. Componentes: `.topo` (marca WebLab + trilhas + busca + tema), `.cabecalho` da aula com tags, `.bloco` de código, callouts (`.dica .atencao .capo .prova .saiba .investigue`), `.desafio` (card com `.estrela` e checkbox "Feito"), `.cartao` de aula, `.hero`, `.stats`, `.progresso-trilha` (barra), `.filtros` do banco, `.navpe`, `@media print`.
- [ ] **Step 4: `app.js`** — tema; copiar código; barra de progresso; sumário ativo (IntersectionObserver); atalhos `j/k///Esc`; menu lateral mobile; busca global (carrega `raiz_rel + "busca.json"` no foco, filtra por título/cabeçalhos/desafios, lista até 20 resultados com link); progresso local (checkbox `#concluir` na aula, checkboxes `.desafio input`, cálculo de % na home e nos índices lendo `localStorage`); filtros do banco de desafios (trilha, dificuldade, tag, "só não feitos"). Tudo dentro de `try/catch` para `localStorage`.
- [ ] **Step 5: `paginas.py`** — portar templates do FDS (`pagina`, `menu_lateral`, `sumario`, `rodape_nav`, índice com hero/stats/cartões/cronograma/avaliações/stack, apostila única com seções ocultáveis) parametrizados por trilha. Cada aula recebe no fim `<label class="concluir"><input type="checkbox" id="concluir" data-chave="weblab:aula:{trilha}/{pagina}"> Concluí esta aula</label>`. Na seção Desafios, `enfeitar_desafios(html, desafios)` envolve cada `<h3 id=…>` de desafio e seu conteúdo até o próximo `<h3>` em `<article class="desafio" data-id=…>` com badge de dificuldade e checkbox "Feito".
- [ ] **Step 6: `build.py`** — `gerar()`: limpa `site/`; `lint_tudo()` (a menos que `--parcial`); para cada trilha: renderiza aulas existentes (`remover_cabecalho` → `converter` → `enfeitar` → `enfeitar_desafios`), escreve páginas, índice (`aula-01` fornece "resumo"? não — o índice usa `config` + texto fixo por trilha em `config["descricao_longa"]`), apostila única (`prefixar_ids`); coleta desafios; `desafios/index.html` (todos + `projetos-integradores.md` renderizado); `links/index.html`; `index.html` (home.md + cards das trilhas + stats); `busca.json` (lista de `{u, t, tr, h:[...]}`); `sitemap.xml` com `https://weblab.ivanpires.dev/...`; `robots.txt`; `404.html`; copia nada externo. `checar_links()` varre `href`/`src` relativos de todos os HTML e confirma existência de arquivo e de âncora (`id`) quando houver `#`. CLI: `python3 build/build.py [--parcial]`.
- [ ] **Step 7: Rodar testes** — `pytest build/tests -q` → todos passam.
- [ ] **Step 8: Build parcial real** com as 15 aulas do FDS copiadas para `fontes/nivel-3/` (ver Task 6 — pode ser feito aqui só a cópia bruta com `--parcial`), abrir `site/nivel-3/aula-06.html` e `site/index.html` no Chrome headless (`google-chrome --headless --screenshot=/tmp/…png --window-size=1280,900 file://…`) e conferir visualmente; ajustar CSS.
- [ ] **Step 9: Commit** — `git commit -m "build: design system, templates e geração do site"`.

---

### Task 5: Especificação final + aula-modelo + migração do Nível 3 (FDS)

**Files:**
- Create: `fontes/nivel-3/aula-01-….md` … `aula-15-….md` (cópia dos MD do FDS, renomeados conforme `config`), depois enriquecidos.
- Modify: `fontes/ESPECIFICACAO.md` (apontar aula-modelo).

- [ ] **Step 1: Copiar** os 15 arquivos de `~/Documents/UNEMAT/Ensino/2026.2/fds/MaterialFACETSNP3102026.2/material/aulas/` para `fontes/nivel-3/` com os nomes de `config.aulas("nivel-3")[i]["arquivo"]`; substituir "Cáceres" por "Sinop"; remover a linha `> **Data:** …`.
- [ ] **Step 2: Rodar `python3 build/lint.py`** — esperado: 15 erros "faltam desafios" (+ possíveis fences sem linguagem).
- [ ] **Step 3: Enriquecer com subagentes (3 agentes × 5 aulas):** cada agente recebe `fontes/ESPECIFICACAO.md`, a aula e a instrução: **adicionar** a seção `## 🏆 Desafios` (3–4 desafios ⭐/⭐⭐/⭐⭐⭐ ligados ao conteúdo daquela aula e ao UniEventos/projeto autoral, com Tags, Critérios de pronto, Pistas; nas aulas 04, 06 e 15 incluir `### 🔥 Boss`), inserir 1 `> **🧠 Você sabia?**` e 1 `> **🔬 Investigue**` em seções teóricas, reformatar o `## 🧪 Laboratório` existente em Nível A/B/C (A = 4 perguntas curtas de fixação novas; B = os exercícios já existentes; C = o mais difícil dos existentes ou um novo), corrigir fences sem linguagem, não alterar mais nada. Validar com `python3 build/lint.py`.
- [ ] **Step 4: Escolher `aula-06-axios-e-pinia.md` como aula-modelo** e referenciá-la em `ESPECIFICACAO.md`.
- [ ] **Step 5: Lint limpo para nivel-3** e commit — `git commit -m "conteúdo: nível 3 (frameworks) migrado do FDS com desafios"`.

---

### Task 6: Conteúdo — Nível 1 (15 aulas)

**Files:** Create `fontes/nivel-1/aula-01-….md` … `aula-15-….md`.

Fonte primária: `scratchpad/fontes-pdf/idw/apostila-idw.txt` (texto da apostila IDW, ~10.500 linhas; cada aula tem Objetivos, Roteiro, seções, Prática guiada, Exercícios A/B/C, Atividade EAD, Erros comuns, Leitura). Copiar esse arquivo para `docs/fontes-brutas/apostila-idw.txt` para os subagentes lerem (não versionar? versionar: é fonte de trabalho — 400 KB, aceitável).

- [ ] **Step 1: Dispatch de 5 subagentes × 3 aulas** (01–03, 04–06, 07–09, 10–12, 13–15). Prompt de cada um: ler `fontes/ESPECIFICACAO.md`, a aula-modelo, e o trecho da apostila IDW correspondente (indicar `grep -n "^Aula NN —"` para achar o início/fim); **converter para o formato WebLab** preservando todo o conteúdo técnico e os exercícios A/B/C existentes (os C viram Laboratório C ou Desafios ⭐⭐), reescrevendo em Markdown com código completo; **adicionar**: `## 🗺️ Roteiro` (3 blocos), `## 💻 Mão na massa` (a Prática guiada, no projeto fio-condutor "site do evento acadêmico"), `## 🏆 Desafios` (≥3 novos, com boss nas aulas 05, 09 e 15), callouts 🧠/🔬 (≥1 cada), `## ✅ Checkpoint do projeto`, `## 📚 Para aprofundar` com links MDN pt-BR/web.dev; a aula 15 ("Publicando seu website") deve remeter à trilha Deploy (`../deploy/cap-03.html`). Sem datas. Aulas 06, 10 e 15 trazem `## 📝 Avaliação N` com rubrica de 10 pontos (critérios do Plano: A1 site HTML; A2 CSS responsivo; A3 JS interativo). Rodar `python3 build/lint.py` até zero erros no arquivo.
- [ ] **Step 2: Revisão do orquestrador:** lint total; abrir 3 aulas no navegador headless; checar continuidade (a aula N+1 retoma N) por leitura dos 10 primeiros e últimos parágrafos.
- [ ] **Step 3: Commit** — `git commit -m "conteúdo: nível 1 (introdução) — 15 aulas"`.

---

### Task 7: Conteúdo — Nível 2 (16 aulas)

**Files:** Create `fontes/nivel-2/aula-01-….md` … `aula-16-….md`.

Fontes: `scratchpad/fontes-pdf/dsw/Aula_NN_*.txt` (handouts de 200–290 linhas: objetivos, teoria enxuta, atividade extraclasse, referências) e `~/Documents/UNEMAT/Ensino/2026.2/dsw/CLAUDE.md` (fio-condutor e requisitos por unidade). Copiar os `.txt` para `docs/fontes-brutas/dsw/`.

- [ ] **Step 1: Dispatch de 6 subagentes** (01–03, 04–06, 07–09, 10–12, 13–14, 15–16). Cada um: ler spec, aula-modelo, o handout da aula e `dsw/CLAUDE.md`; **expandir** o handout para o formato completo (900–1.500 linhas): a teoria do handout vira as seções numeradas ampliadas com código completo; a "Atividade extraclasse" vira `## 🏠 Atividade assíncrona`; criar `## 💻 Mão na massa` construindo o **Café Cerrado** (Unidade 1: site estático `index.html`/`cardapio.html`/`contato.html`; Unidade 2: `js/app.js` com array `produtos`, cards, filtros, `buscarProdutos()`, fetch, SPA por hash; Unidade 3: repo Node `cafe-cerrado-api` com `public/`, `routes/`, `controllers/`, `data/produtos.json`, `POST /api/auth/google`, CRUD com 401/403); Laboratório A/B/C; `## 🏆 Desafios` (≥3, boss nas aulas 06, 10 e 16); callouts 🧠/🔬; Erros comuns; Checkpoint; Para aprofundar. Aulas 06, 10 e 16 trazem `## 📝 Avaliação N` com critérios do Plano (A1 HTML semântico/responsivo/framework CSS/animação-SVG/acessibilidade; A2 validação/DOM/assíncrono/SPA; A3 rotas-controladores/Google/CRUD/integração). Stack: Node 22+, Express 5 (respeitar armadilhas), `google-auth-library` para verificar ID token, Bootstrap 5.3 / Tailwind 4 (CDN play) / Material Web para a aula 04. Lint até zero erros.
- [ ] **Step 2: Revisão do orquestrador** (lint, amostras no navegador, continuidade) e commit — `git commit -m "conteúdo: nível 2 (desenvolvimento web) — 16 aulas"`.

---

### Task 8: Conteúdo — Deploy & Ferramentas (11 capítulos)

**Files:** Create `fontes/deploy/cap-01-….md` … `cap-11-….md`.

- [ ] **Step 1: Dispatch de 4 subagentes** (01–03, 04–06, 07–09, 10–11). Cada capítulo: 600–1.000 linhas, estrutura de aula com `## 🚀 Passo a passo` (no lugar de Mão na massa) publicando um dos projetos das trilhas (cap. 03 publica o site do evento do N1 e o Café Cerrado estático; cap. 05 publica a `cafe-cerrado-api`; cap. 06 usa o laboratório real `https://ivanpires.dev/dsw/gN/` — SSH `gN@ivanpires.dev`, `~/frontend`, `~/backend`, `sudo systemctl restart dsw-gN`, porta `350N`, MySQL `db_gN`; cap. 07 dockeriza a `unieventos-api` + MySQL; cap. 08 Supabase/Neon para o UniEventos; cap. 09 Actions fazendo build+deploy do site estático e testes da API), `## 🧪 Laboratório` A/B/C, `## 🏆 Desafios` (≥3; boss no cap. 06 "publique os três projetos com HTTPS em subdomínios" e no cap. 09), `## 🐛 Erros comuns`, `## 🏠 Atividade assíncrona`, `## ✅ Está no ar quando…`, `## 📚 Para aprofundar` (docs oficiais: GitHub Pages, Netlify, Vercel, Cloudflare, Render, Railway, Fly, nginx, certbot, Docker, Supabase, Neon, GitHub Actions, Lighthouse, Sentry). Comandos reais e testados (`gh`, `git`, `npm`, `docker`, `ssh`, `rsync`, `certbot --nginx`), sem inventar flags. Lint (`tipo="deploy"`) até zero.
- [ ] **Step 2: Revisão e commit** — `git commit -m "conteúdo: trilha deploy & ferramentas — 11 capítulos"`.

---

### Task 9: Projetos integradores, links úteis e home

**Files:** Create `fontes/desafios/projetos-integradores.md`, `fontes/links.md`, `fontes/home.md`.

- [ ] **Step 1: `projetos-integradores.md`** (1 subagente): os 10 projetos de `docs/fontes-brutas/10-projetos.txt` no formato `### ⭐⭐ Nome` (dificuldade conforme "Nível" do PDF: Iniciante ⭐, Intermediário ⭐⭐, Avançado ⭐⭐⭐), cada um com contexto, funcionalidades mínimas, **Critérios de pronto**, "Evolução" (2–3 extensões), trilha sugerida (N1/N2/N3) e `Tags:`; mais 2 projetos "🔥 Boss" full-stack (sistema de reservas com API + auth; painel de dados com cache e gráficos). O build extrai esses itens para o banco com `trilha = "projetos"`.
- [ ] **Step 2: `links.md`** (1 subagente): ≥60 links em ≥10 categorias (`## Documentação oficial`, `## Aprender praticando`, `## Ferramentas online`, `## APIs públicas para praticar`, `## Design, cores, fontes e ícones`, `## Acessibilidade`, `## Performance e qualidade`, `## Deploy e infraestrutura`, `## Comunidades e canais em português`, `## Livros e referências`, `## Roadmaps`); formato `- [Nome](url) — por que usar (1 linha).`; URLs verificadas com `curl -sI` (status 200/301/302) por script no final.
- [ ] **Step 3: `home.md`**: hero (nome, frase), "Como usar o WebLab" (5 passos de estudo), "Trilha recomendada" (N1 → N2 → N3, Deploy em paralelo a partir do N1 aula 15), "Para a turma 2026.2" (links para os índices com cronogramas), créditos/licença (uso educacional, atribuição).
- [ ] **Step 4: Build completo sem `--parcial`**, lint zero, `checar_links` zero; commit — `git commit -m "conteúdo: projetos integradores, links úteis e home"`.

---

### Task 10: Servidor — vhost nginx + HTTPS + deploy.sh

**Files:** Create `deploy.sh`, `docs/servidor.md`.

- [ ] **Step 1: Criar pasta no servidor:** `ssh webmaster@ivanpires.dev 'mkdir -p /home/webmaster/apps/weblab/site'`.
- [ ] **Step 2: `deploy.sh`:**

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 build/build.py "$@"
rsync -az --delete --chmod=D755,F644 site/ webmaster@ivanpires.dev:/home/webmaster/apps/weblab/site/
echo "Publicado: https://weblab.ivanpires.dev/"
```

- [ ] **Step 3: Primeiro rsync** (`./deploy.sh`) e conferir `ssh … 'ls /home/webmaster/apps/weblab/site | head'`.
- [ ] **Step 4: Vhost com root via docker** — enviar por heredoc:

```bash
ssh webmaster@ivanpires.dev 'docker run --rm -i --privileged --pid=host --net=host -v /:/host redis:7-alpine chroot /host /bin/bash' <<'ROOT'
set -e
cat > /etc/nginx/sites-available/weblab.ivanpires.dev <<'NG'
server {
    listen 80;
    server_name weblab.ivanpires.dev;
    root /home/webmaster/apps/weblab/site;
    index index.html;
    charset utf-8;
    gzip on; gzip_types text/html text/css application/javascript application/json image/svg+xml;
    location / { try_files $uri $uri/ $uri.html =404; }
    location = /busca.json { add_header Cache-Control "public, max-age=3600"; }
    error_page 404 /404.html;
}
NG
ln -sf /etc/nginx/sites-available/weblab.ivanpires.dev /etc/nginx/sites-enabled/weblab.ivanpires.dev
nginx -t && systemctl reload nginx
certbot --nginx -d weblab.ivanpires.dev --non-interactive --agree-tos -m ivanpires@gmail.com --redirect
nginx -t && systemctl reload nginx
certbot renew --dry-run 2>&1 | tail -3
ROOT
```

- [ ] **Step 5: Verificar** — `curl -sI https://weblab.ivanpires.dev/ | head -3` (200), `echo | openssl s_client -servername weblab.ivanpires.dev -connect ivanpires.dev:443 2>/dev/null | openssl x509 -noout -subject` (CN=weblab.ivanpires.dev), `curl -sI http://weblab.ivanpires.dev/` (301 → https), `curl -s -o /dev/null -w "%{http_code}" https://weblab.ivanpires.dev/nao-existe` (404).
- [ ] **Step 6: `docs/servidor.md`** documentando vhost, caminho, certificado e o comando de republicação. Commit — `git commit -m "deploy: vhost nginx + HTTPS para weblab.ivanpires.dev e deploy.sh"`.

---

### Task 11: Verificação visual e funcional do site publicado

- [ ] **Step 1: Capturas headless** do site publicado: home, `/nivel-1/`, `/nivel-2/aula-09.html`, `/nivel-3/apostila.html#aula-06`, `/deploy/cap-06.html`, `/desafios/`, `/links/` em 1280×900 e 390×844; inspecionar as imagens (Read) e corrigir CSS se algo quebrar.
- [ ] **Step 2: Funcional via Chrome headless + `--dump-dom` ou script Node com `puppeteer`? Não — usar `google-chrome --headless --virtual-time-budget=2000 --dump-dom` para confirmar que `busca.json` é referenciado e que `app.js` não lança erro (`--enable-logging=stderr`); testar tema/progresso manualmente pela leitura do JS. 
- [ ] **Step 3: Checar `sitemap.xml`** lista 57 aulas + 7 índices; `busca.json` ≤ 400 KB.
- [ ] **Step 4: Corrigir** o que aparecer, rebuild, `./deploy.sh`, commit.

---

### Task 12: README, CLAUDE.md, GitHub e memória

**Files:** Create `README.md`, `CLAUDE.md`.

- [ ] **Step 1: `README.md`** — o que é, URL, estrutura, como editar uma aula, `python3 build/build.py`, `pytest build/tests`, `./deploy.sh`, licença educacional.
- [ ] **Step 2: `CLAUDE.md`** — resumo da arquitetura (fontes → build → site → rsync), regras do `ESPECIFICACAO.md`, comandos, aviso "datas só em config.py", como adicionar uma aula/trilha, onde estão as fontes brutas.
- [ ] **Step 3: GitHub** — `gh repo create weblab --public --description "WebLab — apostila online de desenvolvimento web (UNEMAT) · weblab.ivanpires.dev" --source=. --remote=origin --push`.
- [ ] **Step 4: Memória** — salvar em `memory/`: `weblab-site.md` (projeto: repo, URL, pipeline, deploy, onde está o vhost) com link `[[ivanpires-dev-server-admin]]`; atualizar `MEMORY.md`.
- [ ] **Step 5: Commit final e push.**

---

## Self-review (feito)

- Cobertura do spec: §3 arquivo→Tasks 1–4; §4 páginas→Task 4 (todas listadas em `gerar()`); §5 modelo→Tasks 1 (spec), 3 (lint), 2 (extração); §6 pipeline→Tasks 2–4; §7 deploy→Task 10; §8 conteúdo→Tasks 5–9; §10 aceite→Tasks 10–11 verificam.
- Placeholders: nenhum "TBD/TODO"; os prompts dos subagentes descrevem entradas, saídas e critério (lint zero).
- Consistência de nomes: `converter/enfeitar/remover_cabecalho/sumario/extrair_desafios/prefixar_ids` (render), `lint_texto/lint_arquivo/lint_tudo` (lint), `gerar/checar_links` (build), `pagina_*` (paginas), `TRILHAS/trilha/aulas/CRONOGRAMA/AVALIACOES/FONTES/SITE` (config) — usados com os mesmos nomes em todas as tasks.
