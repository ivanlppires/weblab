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
    assert a["arquivo"].startswith("aula-01-") and a["arquivo"].endswith(".md")
    assert a["trilha"] == "nivel-1"
    d = config.aulas("deploy")[0]
    assert d["pagina"] == "cap-01.html" and d["arquivo"].startswith("cap-01-")


def test_unidades_cobrem_todas_as_aulas():
    for t in config.TRILHAS:
        for a in config.aulas(t):
            assert a["unidade"] in config.trilha(t)["unidades"]


def test_cronograma_literal_do_plano():
    n1 = config.CRONOGRAMA["nivel-1"]
    assert n1[0]["data"] == "11/08/2026" and n1[-1]["data"] == "17/11/2026"
    assert len(n1) == 15
    n2 = config.CRONOGRAMA["nivel-2"]
    assert n2[0]["data"] == "11/08/2026" and n2[-1]["data"] == "24/11/2026"
    assert len(n2) == 16
    n3 = config.CRONOGRAMA["nivel-3"]
    assert len(n3) == 15
    assert "deploy" not in config.CRONOGRAMA


def test_avaliacoes_marcadas_nas_aulas():
    marcadas = [a["num"] for a in config.aulas("nivel-2") if a["avaliacao"]]
    assert marcadas == ["06", "10", "16"]
    marcadas = [a["num"] for a in config.aulas("nivel-1") if a["avaliacao"]]
    assert marcadas == ["06", "10", "15"]
    marcadas = [a["num"] for a in config.aulas("nivel-3") if a["avaliacao"]]
    assert marcadas == ["04", "08", "15"]
    assert len(config.AVALIACOES["nivel-1"]) == 3


def test_arquivos_unicos():
    for t in config.TRILHAS:
        arquivos = [a["arquivo"] for a in config.aulas(t)]
        assert len(arquivos) == len(set(arquivos))
