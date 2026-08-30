from build import render

MD = """# Aula 01 — Teste

> **Nível 1 — Introdução** · Unidade 1: X
> WebLab · UNEMAT Sinop
> **Carga:** 3 aulas

## 1. Seção

> **💡 Dica**
> Use `const`.

> **🧠 Você sabia?**
> Fato.

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

## 🐛 Erros comuns

texto
"""


def test_converter_e_enfeitar_callout_e_codigo():
    html = render.enfeitar(render.converter(MD))
    assert 'blockquote class="dica"' in html
    assert 'blockquote class="saiba"' in html
    assert 'class="bloco"' in html and "Copiar" in html and "JavaScript" in html
    assert '<div class="tabela-wrap"><table>' in html


def test_remover_cabecalho():
    corpo = render.remover_cabecalho(MD)
    assert not corpo.lstrip().startswith("# Aula")
    assert "**Carga:**" not in corpo and "WebLab · UNEMAT" not in corpo
    assert "## 1. Seção" in corpo


def test_sumario():
    html = render.converter(MD)
    itens = render.sumario(html)
    assert ("2", "1-secao", "1. Seção") in itens
    assert any(i[0] == "3" and i[1] == "primeiro-desafio" for i in itens)


def test_extrair_desafios():
    aula = {"num": "01", "titulo": "Teste", "pagina": "aula-01.html", "trilha": "nivel-1"}
    ds = render.extrair_desafios(MD, aula)
    assert [d["dificuldade"] for d in ds] == [1, 3, "boss"]
    assert ds[0]["tags"] == ["html", "css"]
    assert ds[0]["resumo"].startswith("Texto do desafio")
    assert ds[2]["titulo"] == "Chefão" and ds[2]["pagina"] == "aula-01.html"
    assert ds[0]["ancora"] == "primeiro-desafio"
    assert ds[0]["id"] == "nivel-1/aula-01/primeiro-desafio"
    assert ds[0]["trilha"] == "nivel-1" and ds[0]["aula_num"] == "01"


def test_slug_remove_acentos_e_emojis():
    assert render.slug("⭐⭐ Busca que ignora acentos") == "busca-que-ignora-acentos"
    assert render.slug("🔥 Boss — Chefão final!") == "boss-chefao-final"
    assert render.slug("1. Seção") == "1-secao"


def test_prefixar_ids():
    html = '<h2 id="x">X</h2><a href="#x">l</a><a href="outra.html#y">z</a>'
    out = render.prefixar_ids(html, "a01")
    assert 'id="a01-x"' in out and 'href="#a01-x"' in out and 'href="outra.html#y"' in out


def test_enfeitar_desafios_envolve_em_article():
    aula = {"num": "01", "titulo": "Teste", "pagina": "aula-01.html", "trilha": "nivel-1"}
    ds = render.extrair_desafios(MD, aula)
    html = render.enfeitar(render.converter(MD))
    out = render.enfeitar_desafios(html, ds)
    assert out.count('<article class="desafio"') == 3
    assert 'data-id="nivel-1/aula-01/primeiro-desafio"' in out
    assert 'class="estrelas"' in out
    # o conteúdo posterior (Erros comuns) não é engolido pelo último article
    assert out.index("</article>", out.rindex('<article class="desafio"')) < out.index("Erros comuns")


# --------------------------------------------------------------------------
# <details><summary>…</summary> sem markdown="1" (formato do Nível 1/2/deploy)
# --------------------------------------------------------------------------
DETALHES_SIMPLES = """<details><summary>Dica</summary>

Use `min-height: 100vh` e uma lista:

- item um
- item dois

```js
const x = 1;
```
</details>
"""


def test_details_summary_mesma_linha_processa_markdown_interno():
    html = render.converter(DETALHES_SIMPLES)
    assert "<details" in html
    assert "<summary>Dica</summary>" in html
    assert "<code>" in html  # crases viraram <code>
    assert "<ul>" in html and "<li>" in html  # lista viraram <ul>/<li>
    assert "<pre" in html and "codehilite" in html  # fence virou bloco destacado
    assert "`" not in html  # nenhuma crase literal sobrou
    assert "- item" not in html  # nenhum "- item" literal (lista crua) sobrou


def test_details_summary_seguido_de_titulo_no_gera_h3():
    md = DETALHES_SIMPLES + "\n### Título seguinte\ntexto\n"
    html = render.converter(md)
    assert '<h3 id="titulo-seguinte">' in html


def test_details_summary_mencionando_a_propria_tag_nao_engole_o_resto():
    md = (
        '<details><summary>Dica</summary>\n\n'
        'Para fechar os outros, use `<details name="acordeao">` com o mesmo `name`, '
        'ou dentro de `<details>` simples.\n'
        '</details>\n\n'
        '### Título depois\n'
        'texto do resto do arquivo\n'
    )
    html = render.converter(md)
    assert '<h3 id="titulo-depois">' in html
    assert "&lt;details" in html  # a menção à tag aparece escapada, não crua


def test_details_markdown_1_com_summary_na_linha_seguinte_continua_funcionando():
    md = (
        '<details markdown="1">\n'
        '<summary>Dica</summary>\n\n'
        'Cinco linhas — uma por endpoint.\n'
        '</details>\n\n'
        '### Título depois\n'
        'texto\n'
    )
    html = render.converter(md)
    assert "<summary>Dica</summary>" in html
    assert "<p>Cinco linhas" in html
    assert '<h3 id="titulo-depois">' in html
