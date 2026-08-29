"""Lint das fontes Markdown do WebLab.

Uso: python3 build/lint.py            (código de saída 1 se houver erros)
     from build import lint; lint.lint_texto(texto, "aula")
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from build import config  # noqa: E402

# (emoji, nome legível, alternativas aceitas para deploy)
SECOES_AULA = [
    ("🎯", "Objetivos de aprendizagem"),
    ("📋", "Pré-requisitos"),
    ("🗺", "Roteiro"),
    ("💻", "Mão na massa"),
    ("🧪", "Laboratório"),
    ("🏆", "Desafios"),
    ("🐛", "Erros comuns"),
    ("🏠", "Atividade assíncrona"),
    ("✅", "Checkpoint"),
    ("📚", "Para aprofundar"),
]
EQUIVALENTES = {"🚀": "💻"}  # deploy: "🚀 Passo a passo" vale como "💻 Mão na massa"
MIN_LINHAS = {"aula": 600, "deploy": 400, "livre": 0}
MIN_LAB = {"A": 4, "B": 3, "C": 1}
MIN_DESAFIOS = 3

_RE_PLACEHOLDER = re.compile(r"\.\.\.\s*resto|//\s*\.\.\.|\bTODO\b|\bTBD\b|Lorem ipsum|\bFIXME\b")
_RE_FENCE = re.compile(r"^\s*(`{3,}|~{3,})\s*([\w+.#-]*)\s*(.*)$")


def _emoji_secao(linha: str):
    """Emoji inicial de um '## ' (sem seletor de variação), ou None."""
    m = re.match(r"^##\s+(\S+)", linha)
    if not m:
        return None
    tok = m.group(1).replace("️", "")
    return tok[:1] if tok else None


def _fences(linhas):
    """Gera (num_linha, linguagem) para cada fence de abertura; ignora conteúdo interno."""
    aberto = None  # (marcador, tamanho)
    for n, linha in enumerate(linhas, 1):
        m = _RE_FENCE.match(linha)
        if not m:
            continue
        marcador, lang, resto = m.group(1), m.group(2), m.group(3)
        if aberto is None:
            aberto = (marcador[0], len(marcador))
            yield n, lang
        elif marcador[0] == aberto[0] and len(marcador) >= aberto[1] and not lang and not resto.strip():
            aberto = None


def _fora_de_codigo(linhas):
    """Linhas (num, texto) que não estão dentro de blocos de código."""
    aberto = None
    for n, linha in enumerate(linhas, 1):
        m = _RE_FENCE.match(linha)
        if m:
            marcador, lang, resto = m.group(1), m.group(2), m.group(3)
            if aberto is None:
                aberto = (marcador[0], len(marcador))
                continue
            if marcador[0] == aberto[0] and len(marcador) >= aberto[1] and not lang and not resto.strip():
                aberto = None
                continue
        if aberto is None:
            yield n, linha


def _secoes(linhas):
    """[(num_linha, emoji, texto)] dos '## ' fora de código."""
    out = []
    for n, linha in _fora_de_codigo(linhas):
        if linha.startswith("## "):
            out.append((n, _emoji_secao(linha), linha[3:].strip()))
    return out


def _corpo_secao(linhas, emoji):
    """Linhas da seção cujo '## ' começa com o emoji (até o próximo '## ')."""
    dentro, out = False, []
    for _, linha in _fora_de_codigo_com_codigo(linhas):
        if linha.startswith("## "):
            dentro = _emoji_secao(linha) == emoji
            continue
        if dentro:
            out.append(linha)
    return out


def _fora_de_codigo_com_codigo(linhas):
    """Como _fora_de_codigo, mas mantém as linhas de código (marcando '## ' só fora dele)."""
    aberto = None
    for n, linha in enumerate(linhas, 1):
        m = _RE_FENCE.match(linha)
        if m:
            marcador, lang, resto = m.group(1), m.group(2), m.group(3)
            if aberto is None:
                aberto = (marcador[0], len(marcador))
            elif marcador[0] == aberto[0] and len(marcador) >= aberto[1] and not lang and not resto.strip():
                aberto = None
            yield n, linha
            continue
        if aberto is not None and linha.startswith("## "):
            yield n, " " + linha  # neutraliza '## ' dentro de código
        else:
            yield n, linha


def lint_texto(texto: str, tipo: str = "aula", titulo_esperado: str | None = None):
    """Retorna a lista de erros (strings) de um arquivo-fonte."""
    erros = []
    linhas = texto.splitlines()

    # tamanho
    if len(linhas) < MIN_LINHAS.get(tipo, 0):
        erros.append(f"tem {len(linhas)} linhas; mínimo para '{tipo}' é {MIN_LINHAS[tipo]} linhas")

    # fences com linguagem
    for n, lang in _fences(linhas):
        if not lang:
            erros.append(f"linha {n}: bloco de código sem linguagem (use ```html, ```js, ```bash…)")

    # placeholders (fora e dentro de código)
    for n, linha in enumerate(linhas, 1):
        if _RE_PLACEHOLDER.search(linha):
            erros.append(f"linha {n}: placeholder proibido ({linha.strip()[:60]})")

    # título
    if titulo_esperado is not None:
        m = re.search(r"^#\s+(.+?)\s*$", texto, re.M)
        atual = m.group(1).strip() if m else ""
        if atual != titulo_esperado:
            erros.append(f"título H1 '{atual}' difere do esperado em config.py: '{titulo_esperado}'")

    if tipo == "livre":
        return erros

    # seções obrigatórias e ordem
    secoes = _secoes(linhas)
    emojis = [EQUIVALENTES.get(e, e) for _, e, _ in secoes]
    posicoes = []
    for emoji, nome in SECOES_AULA:
        if emoji not in emojis:
            erros.append(f"falta a seção '## {emoji} {nome}'")
        else:
            posicoes.append(emojis.index(emoji))
    if posicoes != sorted(posicoes):
        erros.append("seções obrigatórias fora de ordem (ver ESPECIFICACAO.md §3)")

    # tabelas largas (fora de código)
    for n, linha in _fora_de_codigo(linhas):
        if re.match(r"^\s*\|\s*:?-+", linha):
            colunas = [c for c in linha.strip().strip("|").split("|")]
            if len(colunas) > 4:
                erros.append(f"linha {n}: tabela com {len(colunas)} colunas (máximo 4)")

    # laboratório
    lab = "\n".join(_corpo_secao(linhas, "🧪"))
    for nivel, minimo in MIN_LAB.items():
        qtd = len(re.findall(r"^\**" + nivel + r"\d+[.)]", lab, re.M))
        if qtd < minimo:
            erros.append(f"Laboratório: Nível {nivel} tem {qtd} itens (mínimo {minimo}; formato '**{nivel}1.** …')")

    # desafios
    des = "\n".join(_corpo_secao(linhas, "🏆"))
    blocos = re.split(r"^###\s+", des, flags=re.M)[1:]
    validos = [b for b in blocos if re.match(r"^(⭐{1,3}\s|🔥\s*Boss)", b)]
    if len(validos) < MIN_DESAFIOS:
        erros.append(
            f"Desafios: {len(validos)} desafios válidos (mínimo {MIN_DESAFIOS}; títulos '### ⭐ …', '### ⭐⭐ …', '### ⭐⭐⭐ …' ou '### 🔥 Boss — …')"
        )
    for b in validos:
        titulo = b.splitlines()[0][:50]
        if not re.search(r"^\s*Tags:\s*\S", b, re.M):
            erros.append(f"Desafio '{titulo}': falta a linha 'Tags: …'")
        if "**Critérios de pronto**" not in b:
            erros.append(f"Desafio '{titulo}': falta '**Critérios de pronto**'")
        if "<details" not in b:
            erros.append(f"Desafio '{titulo}': falta '<details><summary>Pistas</summary>'")

    return erros


def lint_arquivo(caminho: Path, tipo: str, titulo_esperado: str | None = None):
    if not caminho.exists():
        return [f"{caminho}: arquivo ausente"]
    erros = lint_texto(caminho.read_text(encoding="utf-8"), tipo, titulo_esperado)
    return [f"{caminho.relative_to(config.RAIZ)}: {e}" for e in erros]


def titulo_esperado(aula):
    rotulo = "Capítulo" if aula["trilha"] == "deploy" else "Aula"
    return f"{rotulo} {aula['num']} — {aula['titulo']}"


def lint_tudo(parcial: bool = False):
    """Lint de todas as fontes listadas em config. Com parcial=True, arquivos ausentes são ignorados."""
    erros = []
    for tid, t in config.TRILHAS.items():
        for a in t["aulas"]:
            caminho = config.caminho_fonte(a)
            if parcial and not caminho.exists():
                continue
            erros += lint_arquivo(caminho, t["tipo"], titulo_esperado(a))
    for rel in ("links.md", "home.md", "desafios/projetos-integradores.md"):
        caminho = config.FONTES / rel
        if caminho.exists():
            erros += lint_arquivo(caminho, "livre")
        elif not parcial:
            erros.append(f"fontes/{rel}: arquivo ausente")
    return erros


if __name__ == "__main__":
    parcial = "--parcial" in sys.argv
    erros = lint_tudo(parcial)
    for e in erros:
        print("✗", e)
    print(f"{len(erros)} erro(s)")
    sys.exit(1 if erros else 0)
