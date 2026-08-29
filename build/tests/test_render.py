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
