"""Conversão Markdown → HTML, pós-processamento e extração de desafios.

Funções puras (sem I/O). Usadas por build.py e pelos testes.
"""
import html as html_mod
import re
import unicodedata

import markdown
from pygments.formatters import HtmlFormatter

# --------------------------------------------------------------------------
# slug
# --------------------------------------------------------------------------
_RE_NAO_ALNUM = re.compile(r"[^a-z0-9\s-]")
_RE_ESPACOS = re.compile(r"[\s_]+")
_RE_HIFENS = re.compile(r"-{2,}")


def slug(texto: str) -> str:
    """Slug ASCII: remove acentos, emojis e pontuação; espaços viram hífens."""
    t = unicodedata.normalize("NFKD", texto)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = t.lower()
    t = _RE_NAO_ALNUM.sub(" ", t)
    t = _RE_ESPACOS.sub("-", t.strip())
    t = _RE_HIFENS.sub("-", t)
    return t.strip("-")


def _slugify_md(value, separator):  # assinatura exigida pela extensão toc
    return slug(value)


# --------------------------------------------------------------------------
# Markdown
# --------------------------------------------------------------------------
PYG_CSS = HtmlFormatter(style="stata-dark").get_style_defs(".highlight")

_MD = markdown.Markdown(
    extensions=["fenced_code", "codehilite", "tables", "toc", "attr_list", "sane_lists", "md_in_html"],
    extension_configs={
        "codehilite": {"guess_lang": False, "css_class": "codehilite", "use_pygments": True},
        "toc": {"anchorlink": False, "permalink": "¶", "permalink_class": "anchor", "slugify": _slugify_md},
    },
)


_RE_FENCE = re.compile(r"^\s*(`{3,}|~{3,})\s*([\w+.#-]*)\s*(.*)$")


def _separar_callouts(md_texto: str) -> str:
    """Insere um separador entre blockquotes adjacentes (fora de código).

    O python-markdown funde '> a\\n\\n> b' em um único <blockquote>; dois callouts
    seguidos virariam uma caixa só, com a cor do primeiro.
    """
    linhas = md_texto.splitlines()
    out = []
    aberto = None
    ultimo_bq = False  # a última linha não em branco (fora de código) era blockquote?
    pendentes = 0      # linhas em branco acumuladas desde então
    for linha in linhas:
        m = _RE_FENCE.match(linha)
        if m:
            marcador, lang, resto = m.group(1), m.group(2), m.group(3)
            if aberto is None:
                aberto = (marcador[0], len(marcador))
            elif marcador[0] == aberto[0] and len(marcador) >= aberto[1] and not lang and not resto.strip():
                aberto = None
            out.extend([""] * pendentes)
            pendentes = 0
            ultimo_bq = False
            out.append(linha)
            continue
        if aberto is not None:
            out.extend([""] * pendentes)
            pendentes = 0
            out.append(linha)
            continue
        if not linha.strip():
            pendentes += 1
            continue
        eh_bq = linha.lstrip().startswith(">")
        if eh_bq and ultimo_bq and pendentes:
            out.extend(["", "<!-- -->", ""])
        else:
            out.extend([""] * pendentes)
        pendentes = 0
        out.append(linha)
        ultimo_bq = eh_bq
    out.extend([""] * pendentes)
    return "\n".join(out)


def converter(md_texto: str) -> str:
    """Markdown → HTML bruto (com ids nos títulos e código destacado)."""
    _MD.reset()
    return _MD.convert(_separar_callouts(md_texto))


# --------------------------------------------------------------------------
# cabeçalho das fontes
# --------------------------------------------------------------------------
_RE_DATA = re.compile(r"^\s*>?\s*\*\*Data:\*\*.*$", re.M)


def remover_cabecalho(md_texto: str) -> str:
    """Remove o H1 inicial e o blockquote de cabeçalho (trilha/unidade/carga)."""
    linhas = md_texto.splitlines()
    i = 0
    # pula linhas em branco iniciais
    while i < len(linhas) and not linhas[i].strip():
        i += 1
    if i < len(linhas) and linhas[i].startswith("# "):
        i += 1
    # pula blockquote de cabeçalho e linhas em branco logo após o H1
    while i < len(linhas) and (not linhas[i].strip() or linhas[i].lstrip().startswith(">")):
        i += 1
    corpo = "\n".join(linhas[i:])
    corpo = _RE_DATA.sub("", corpo)
    return corpo


def titulo_h1(md_texto: str) -> str:
    """Texto do primeiro H1 (sem o '# ')."""
    m = re.search(r"^#\s+(.+?)\s*$", md_texto, re.M)
    return m.group(1).strip() if m else ""


# --------------------------------------------------------------------------
# pós-processamento
# --------------------------------------------------------------------------
ROTULOS = {
    "js": "JavaScript", "javascript": "JavaScript", "mjs": "JavaScript", "vue": "Vue SFC",
    "bash": "Terminal", "shell": "Terminal", "sh": "Terminal", "zsh": "Terminal", "console": "Terminal",
    "html": "HTML", "css": "CSS", "json": "JSON", "sql": "SQL", "yaml": "YAML", "yml": "YAML",
    "text": "Texto", "txt": "Texto", "http": "HTTP", "ts": "TypeScript", "typescript": "TypeScript",
    "xml": "XML", "svg": "SVG", "dockerfile": "Dockerfile", "docker": "Dockerfile", "ini": "Config",
    "toml": "TOML", "diff": "Diff", "mermaid": "Diagrama", "python": "Python", "py": "Python",
    "nginx": "nginx", "env": ".env", "dotenv": ".env", "md": "Markdown", "markdown": "Markdown",
    "jsx": "JSX", "powershell": "PowerShell", "ps1": "PowerShell", "cmd": "Prompt", "bat": "Prompt",
    "gitignore": ".gitignore", "properties": "Config", "conf": "Config", "apache": "Apache",
}

CALLOUTS = [
    ("💡", "dica"), ("⚠️", "atencao"), ("⚠", "atencao"), ("🔎", "capo"), ("📌", "prova"),
    ("🧠", "saiba"), ("🔬", "investigue"), ("🧩", "padrao"), ("🚀", "capo"),
]

_RE_BLOCO = re.compile(
    r'<div class="codehilite(?: [^"]*)?"(?: [^>]*)?>\s*(<pre[\s\S]*?</pre>)\s*</div>'
)
_RE_LANG = re.compile(r'<code class="language-([\w+.-]+)"')


def _bloco(m):
    pre = m.group(1)
    ml = _RE_LANG.search(pre)
    lang = ml.group(1).lower() if ml else ""
    rotulo = ROTULOS.get(lang, lang.upper() if lang else "Código")
    return (
        '<div class="bloco"><div class="bloco-topo"><span class="lang">' + html_mod.escape(rotulo) + "</span>"
        '<span class="espaco"></span>'
        '<button class="copiar" type="button" aria-label="Copiar código">Copiar</button></div>'
        '<div class="highlight">' + pre + "</div></div>"
    )


def _callout(m):
    interior = m.group(1)
    inicio = interior[:200]
    for emoji, cls in CALLOUTS:
        if emoji in inicio:
            return '<blockquote class="' + cls + '">' + interior + "</blockquote>"
    return "<blockquote>" + interior + "</blockquote>"


_TAGS_CRUAS = ("template", "script", "style", "iframe", "textarea", "object", "embed", "form", "input", "button")


def enfeitar(corpo: str) -> str:
    """Callouts por emoji, blocos de código com cabeçalho, tabelas roláveis, escape de tags cruas."""
    corpo = _RE_BLOCO.sub(_bloco, corpo)
    corpo = re.sub(r"<blockquote>([\s\S]*?)</blockquote>", _callout, corpo)
    corpo = corpo.replace("<table>", '<div class="tabela-wrap"><table>').replace("</table>", "</table></div>")
    # rede de segurança: tags cruas escritas fora de blocos de código quebram a página.
    # O código real já vem escapado pelo Pygments; qualquer ocorrência aqui é acidental.
    for tag in _TAGS_CRUAS:
        corpo = re.sub(
            r"<(/?)" + tag + r"(\s[^>]*)?>",
            lambda m, tag=tag: "<code>&lt;" + m.group(1) + tag + html_mod.escape(m.group(2) or "") + "&gt;</code>",
            corpo,
            flags=re.I,
        )
    return corpo


_RE_H = re.compile(r'<h([23]) id="([^"]+)">(.*?)</h[23]>', re.S)


def _limpar_titulo(txt: str) -> str:
    limpo = re.sub(r"<[^>]+>", "", txt).replace("¶", "").strip()
    return html_mod.unescape(limpo)


def sumario(corpo_html: str):
    """[(nivel, id, texto)] dos h2/h3 do HTML."""
    out = []
    for nivel, ident, txt in _RE_H.findall(corpo_html):
        limpo = _limpar_titulo(txt)
        if limpo:
            out.append((nivel, ident, limpo))
    return out


def prefixar_ids(corpo_html: str, prefixo: str) -> str:
    """Prefixa todos os id="" e os href="#…" internos (para a apostila de arquivo único)."""
    corpo_html = re.sub(r'\bid="([^"]+)"', lambda m: f'id="{prefixo}-{m.group(1)}"', corpo_html)
    corpo_html = re.sub(r'href="#([^"]+)"', lambda m: f'href="#{prefixo}-{m.group(1)}"', corpo_html)
    return corpo_html


# --------------------------------------------------------------------------
# desafios
# --------------------------------------------------------------------------
_RE_SECAO_DESAFIOS = re.compile(r"^##\s+🏆[^\n]*\n([\s\S]*?)(?=^##\s|\Z)", re.M)
_RE_H3 = re.compile(r"^###\s+(.+?)\s*$", re.M)
_RE_DIFIC = re.compile(r"^(⭐{1,3})\s*(.*)$|^🔥\s*Boss\s*[—–-]\s*(.*)$")


def _dificuldade(titulo_bruto: str):
    m = _RE_DIFIC.match(titulo_bruto.strip())
    if not m:
        return None, titulo_bruto.strip()
    if m.group(1):
        return len(m.group(1)), m.group(2).strip()
    return "boss", m.group(3).strip()


def _resumo(bloco: str) -> str:
    """Primeiro parágrafo de texto do desafio (ignorando Tags:, listas, negritos de rótulo)."""
    paras = re.split(r"\n\s*\n", bloco.strip())
    for p in paras:
        linha = " ".join(l.strip() for l in p.splitlines()).strip()
        if not linha or linha.lower().startswith("tags:") or linha.startswith(("**Crit", "<details", "-", "*", "1.", "|")):
            continue
        linha = re.sub(r"[*`_]", "", linha)
        return (linha[:217] + "…") if len(linha) > 220 else linha
    return ""


def extrair_desafios(md_texto: str, aula: dict):
    """Lista de desafios da seção '## 🏆 Desafios' de uma aula.

    Cada item: id, trilha, aula_num, aula_titulo, pagina, ancora, dificuldade (1|2|3|'boss'),
    titulo, resumo, tags.
    """
    m = _RE_SECAO_DESAFIOS.search(md_texto)
    if not m:
        return []
    secao = m.group(1)
    partes = _RE_H3.split(secao)
    # partes = [antes, titulo1, corpo1, titulo2, corpo2, ...]
    out = []
    vistos = {}
    prefixo = aula["pagina"].rsplit(".", 1)[0]
    for i in range(1, len(partes), 2):
        titulo_bruto = partes[i]
        corpo = partes[i + 1] if i + 1 < len(partes) else ""
        dific, titulo = _dificuldade(titulo_bruto)
        if dific is None:
            continue
        ancora = slug(titulo_bruto)
        # emula o unique() da extensão toc do python-markdown
        base = ancora
        n = vistos.get(base, 0)
        if n:
            ancora = f"{base}_{n}"
        vistos[base] = n + 1
        mt = re.search(r"^\s*Tags:\s*(.+)$", corpo, re.M | re.I)
        tags = [slug(t) for t in mt.group(1).split(",") if t.strip()] if mt else []
        out.append(
            {
                "id": f"{aula['trilha']}/{prefixo}/{ancora}",
                "trilha": aula["trilha"],
                "aula_num": aula["num"],
                "aula_titulo": aula["titulo"],
                "pagina": aula["pagina"],
                "ancora": ancora,
                "dificuldade": dific,
                "titulo": titulo,
                "resumo": _resumo(corpo),
                "tags": tags,
            }
        )
    return out


def estrelas(dific) -> str:
    return "🔥" if dific == "boss" else "⭐" * int(dific)


def rotulo_dificuldade(dific) -> str:
    return {1: "1–2 h", 2: "uma tarde", 3: "um fim de semana", "boss": "Boss da unidade"}.get(dific, "")


def enfeitar_desafios(corpo_html: str, desafios) -> str:
    """Envolve cada desafio (h3 + conteúdo até o próximo h2/h3) em <article class="desafio">."""
    for d in desafios:
        padrao = re.compile(
            r'(<h3 id="' + re.escape(d["ancora"]) + r'">[\s\S]*?</h3>)([\s\S]*?)(?=<h[23]\b|<div class="navpe"|\Z)'
        )

        def _wrap(m, d=d):
            cabecalho = (
                '<article class="desafio" data-id="' + html_mod.escape(d["id"]) + '" data-dificuldade="'
                + str(d["dificuldade"]) + '">'
                '<div class="desafio-topo"><span class="estrelas" title="' + rotulo_dificuldade(d["dificuldade"]) + '">'
                + estrelas(d["dificuldade"]) + "</span>"
                '<label class="feito"><input type="checkbox" data-chave="weblab:desafio:'
                + html_mod.escape(d["id"]) + '"> Feito</label></div>'
            )
            return cabecalho + m.group(1) + m.group(2) + "</article>"

        corpo_html, n = padrao.subn(_wrap, corpo_html, count=1)
    # a linha "Tags: x, y" vira chips
    corpo_html = re.sub(
        r"<p>\s*Tags:\s*(.*?)</p>",
        lambda m: '<p class="tags">' + "".join(
            f'<span class="chip">{html_mod.escape(t.strip())}</span>' for t in m.group(1).split(",") if t.strip()
        ) + "</p>",
        corpo_html,
    )
    return corpo_html
