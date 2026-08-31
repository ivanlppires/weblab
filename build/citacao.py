"""Gera CITATION.cff e .zenodo.json a partir de config.AUTORES.

Assim a lista de autores existe em um lugar só: quem entra em config.py
aparece na página /autores/, no arquivo de citação do GitHub e nos metadados
do DOI do Zenodo. Uso: .venv/bin/python build/citacao.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from build import config  # noqa: E402

RAIZ = config.RAIZ
RESUMO = (
    "Apostila online e aberta de desenvolvimento web em português do Brasil, organizada em "
    "quatro trilhas (introdução; desenvolvimento web; frameworks modernos; deploy e ferramentas), "
    "com 57 aulas, banco de desafios e um gerador de site estático em Python. O material é "
    "atemporal: não traz datas, notas nem prazos, e cada unidade fecha com um marco de projeto."
)
DESCRICAO_HTML = (
    "<p><strong>WebLab</strong> é um curso online aberto de desenvolvimento web em português do Brasil, "
    "publicado em <a href=\"https://weblab.aprendabit.com\">weblab.aprendabit.com</a>. "
    "Reúne <strong>57 aulas</strong> em quatro trilhas — introdução (HTML, CSS e JavaScript), desenvolvimento web "
    "(frameworks CSS, SVG, acessibilidade, SPA e back-end com Node.js/Express), frameworks modernos "
    "(Vue 3, Vuetify, Pinia, MySQL, Supabase, Firebase e Swagger) e uma trilha transversal de deploy e ferramentas "
    "(Git, publicação, DNS e HTTPS, VPS com nginx, Docker, CI/CD, observabilidade e uso de IA).</p>"
    "<p>Cada aula traz objetivos, teoria com código completo, um passo a passo guiado em um projeto contínuo, "
    "laboratório em três níveis de dificuldade, desafios com estrelas, tabela de erros comuns e checkpoint. "
    "Os <strong>221 desafios</strong> são reunidos em um banco filtrável por trilha, tema e dificuldade.</p>"
    "<p>O material é <strong>atemporal e aberto</strong>: não traz datas, notas, prazos nem entrega institucional, "
    "e cada unidade fecha com um <em>marco do projeto</em> — o estado que o projeto do estudante precisa alcançar. "
    "Serve tanto a quem cursa uma disciplina quanto a quem estuda por conta própria.</p>"
    "<p>O depósito inclui o <strong>gerador do site</strong>: um sistema em Python que valida as fontes em Markdown "
    "contra uma especificação editorial, converte o material e publica um sítio estático autocontido, com busca, "
    "progresso local e verificação de enlaces.</p>"
)

PALAVRAS = ["desenvolvimento web", "recurso educacional aberto", "ensino de programação",
            "HTML", "CSS", "JavaScript", "Node.js", "Vue.js", "material didático"]


SUFIXOS = {"filho", "neto", "sobrinho", "júnior", "junior", "jr", "jr.", "ii", "iii"}
PARTICULAS = {"da", "de", "do", "das", "dos", "e", "del", "van", "von"}


def _partes(nome):
    """Separa nome em (prenomes, sobrenome) respeitando o uso brasileiro.

    'Francisco Sanches Banhos Filho' -> ('Francisco Sanches', 'Banhos Filho')
    'Benevid Félix da Silva'         -> ('Benevid Félix', 'da Silva')
    'Ivan Luiz Pedroso Pires'        -> ('Ivan Luiz Pedroso', 'Pires')
    """
    p = nome.split()
    if len(p) == 1:
        return "", p[0]
    corte = len(p) - 1
    if p[corte].lower() in SUFIXOS and corte > 0:   # sufixo acompanha o sobrenome
        corte -= 1
    while corte > 0 and p[corte - 1].lower() in PARTICULAS:  # partícula idem
        corte -= 1
    return " ".join(p[:corte]), " ".join(p[corte:])


def cff():
    autores = []
    for a in config.AUTORES:
        dado, sobrenome = _partes(a["nome"])
        item = {"given-names": dado, "family-names": sobrenome}
        if a.get("orcid"):
            item["orcid"] = f'https://orcid.org/{a["orcid"]}'
        if a.get("instituicao"):
            item["affiliation"] = a["instituicao"]
        autores.append(item)
    linhas = ["cff-version: 1.2.0",
              'message: "Se você usar o WebLab, cite-o como abaixo."',
              "type: software",
              f'title: "{config.NOME_SITE} — {config.SUBTITULO}"',
              f'abstract: "{RESUMO}"',
              "authors:"]
    for a in autores:
        linhas.append(f'  - given-names: "{a["given-names"]}"')
        linhas.append(f'    family-names: "{a["family-names"]}"')
        if "affiliation" in a:
            linhas.append(f'    affiliation: "{a["affiliation"]}"')
        if "orcid" in a:
            linhas.append(f'    orcid: "{a["orcid"]}"')
    linhas += [f'url: "{config.URL_BASE}"',
               'repository-code: "https://github.com/ivanlppires/weblab"',
               'license: CC-BY-4.0',
               "keywords:"] + [f'  - "{k}"' for k in PALAVRAS]
    return "\n".join(linhas) + "\n"


def zenodo():
    criadores = []
    for a in config.AUTORES:
        dado, sobrenome = _partes(a["nome"])
        item = {"name": f"{sobrenome}, {dado}"}
        if a.get("instituicao"):
            item["affiliation"] = a["instituicao"]
        if a.get("orcid"):
            item["orcid"] = a["orcid"]
        criadores.append(item)
    return json.dumps({
        "title": f"{config.NOME_SITE} — {config.SUBTITULO}",
        "description": DESCRICAO_HTML,
        "creators": criadores,
        "upload_type": "software",
        "license": "cc-by-4.0",
        "keywords": PALAVRAS,
        "language": "por",
        "access_right": "open",
        "related_identifiers": [
            {"identifier": config.URL_BASE, "relation": "isIdenticalTo",
             "resource_type": "other", "scheme": "url"},
        ],
        "notes": ("Recurso educacional aberto. O conteúdo didático está sob CC BY 4.0 e o "
                  "gerador do site sob licença MIT; ver LICENSE no repositório."),
    }, ensure_ascii=False, indent=2) + "\n"


if __name__ == "__main__":
    (RAIZ / "CITATION.cff").write_text(cff(), encoding="utf-8")
    (RAIZ / ".zenodo.json").write_text(zenodo(), encoding="utf-8")
    print(f"CITATION.cff e .zenodo.json gerados a partir de {len(config.AUTORES)} autor(es).")
