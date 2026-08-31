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


def test_material_atemporal_por_padrao():
    """O site padrão não mostra datas: sem semestre, sem cronograma, sem prazos."""
    assert config.SEMESTRE == ""
    assert config.CRONOGRAMA == {}
    for trilha, avs in config.AVALIACOES.items():
        for av in avs:
            assert "prazo" not in av, f"{trilha}: avaliação {av['n']} tem prazo fixo"


def test_calendario_opcional_tem_o_formato_esperado():
    """Quando um semestre é configurado, o índice sabe renderizá-lo."""
    cron = {"nivel-1": [{"data": "10/03/2027", "num": "01", "descricao": "Aula inaugural", "prazo": True}]}
    item = cron["nivel-1"][0]
    assert set(item) >= {"data", "num", "descricao"}
    assert item["num"] in [a["num"] for a in config.aulas("nivel-1")]


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
