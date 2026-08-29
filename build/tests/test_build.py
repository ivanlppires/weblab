import json

import pytest

from build import build, config
from build.tests.test_lint import aula_ok


@pytest.fixture
def fontes_minimas(tmp_path, monkeypatch):
    fontes = tmp_path / "fontes"
    site = tmp_path / "site"
    for t in config.TRILHAS:
        (fontes / t).mkdir(parents=True)
        tipo = config.TRILHAS[t]["tipo"]
        for a in config.aulas(t)[:2]:
            texto = aula_ok(tipo).replace("# Aula 01 — X", f"# Aula {a['num']} — {a['titulo']}", 1)
            texto = texto.replace("# Capítulo 01 — X", f"# Capítulo {a['num']} — {a['titulo']}", 1)
            (fontes / t / a["arquivo"]).write_text(texto, encoding="utf-8")
    (fontes / "links.md").write_text(
        "## Documentação oficial\n\n- [MDN](https://developer.mozilla.org/pt-BR/) — referência.\n", encoding="utf-8"
    )
    (fontes / "home.md").write_text("## Como usar\n\nTexto da home.\n", encoding="utf-8")
    (fontes / "desafios").mkdir()
    (fontes / "desafios" / "projetos-integradores.md").write_text(
        "### ⭐⭐ Projeto teste\nTags: projeto, html\n\nresumo\n\n**Critérios de pronto**\n\n- a\n\n"
        "<details><summary>Pistas</summary>\n\n1. p\n</details>\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(config, "FONTES", fontes)
    monkeypatch.setattr(config, "SITE", site)
    return fontes, site


def test_build_parcial_gera_estrutura(fontes_minimas):
    fontes, site = fontes_minimas
    build.gerar(parcial=True)
    assert (site / "index.html").exists()
    for t in config.TRILHAS:
        assert (site / t / "index.html").exists()
        assert (site / t / "apostila.html").exists()
        assert (site / t / config.aulas(t)[0]["pagina"]).exists()
        assert (site / t / config.aulas(t)[1]["pagina"]).exists()
    assert (site / "desafios" / "index.html").exists()
    assert (site / "links" / "index.html").exists()
    assert (site / "busca.json").exists()
    assert (site / "404.html").exists()
    assert (site / "sitemap.xml").exists()
    assert (site / "robots.txt").exists()


def test_paginas_autocontidas_e_links_ok(fontes_minimas):
    fontes, site = fontes_minimas
    build.gerar(parcial=True)
    html = (site / "nivel-1" / "aula-01.html").read_text(encoding="utf-8")
    assert "<script src" not in html
    assert 'rel="stylesheet" href=' not in html
    assert 'data-trilha="nivel-1"' in html
    assert 'id="concluir"' in html
    assert 'class="desafio"' in html
    assert build.checar_links(site) == []


def test_busca_e_desafios(fontes_minimas):
    fontes, site = fontes_minimas
    build.gerar(parcial=True)
    busca = json.loads((site / "busca.json").read_text(encoding="utf-8"))
    urls = [b["u"] for b in busca]
    assert "nivel-1/aula-01.html" in urls and "deploy/cap-01.html" in urls
    item = next(b for b in busca if b["u"] == "nivel-1/aula-01.html")
    assert item["t"].startswith("Aula 01") and "1. Teoria" in item["h"]
    des = (site / "desafios" / "index.html").read_text(encoding="utf-8")
    # 8 aulas × 3 desafios + 1 projeto
    assert des.count('<article class="ficha ') == 8 * 3 + 1
    assert 'href="../nivel-1/aula-01.html#t1"' in des
    assert 'class="desafio"' in des  # projeto integrador embutido na própria página


def test_apostila_unica_prefixa_ids(fontes_minimas):
    fontes, site = fontes_minimas
    build.gerar(parcial=True)
    ap = (site / "nivel-2" / "apostila.html").read_text(encoding="utf-8")
    assert 'id="aula-01"' in ap and 'id="aula-02"' in ap
    assert 'id="a01-1-teoria"' in ap and 'id="a02-1-teoria"' in ap


def test_build_completo_falha_sem_conteudo(fontes_minimas):
    with pytest.raises(SystemExit):
        build.gerar(parcial=False)
