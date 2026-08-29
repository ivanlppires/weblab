"""Gera o site estático do WebLab em site/.

Uso: python3 build/build.py [--parcial]
  --parcial  gera só as aulas que existem (sem exigir conteúdo completo); útil durante a escrita.
"""
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from build import config, lint, paginas, render  # noqa: E402


def _ler(caminho: Path) -> str:
    return caminho.read_text(encoding="utf-8")


def _escrever(caminho: Path, texto: str):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(texto, encoding="utf-8")


def _renderizar_aula(t, a, texto):
    """(corpo_html, itens_toc, desafios) de uma aula."""
    corpo_md = render.remover_cabecalho(texto)
    html = render.enfeitar(render.converter(corpo_md))
    desafios = render.extrair_desafios(texto, a)
    html = render.enfeitar_desafios(html, desafios)
    itens = render.sumario(html)
    return html, itens, desafios


def gerar(parcial: bool = False):
    site = config.SITE
    fontes = config.FONTES

    erros = lint.lint_tudo(parcial=parcial)
    if erros:
        for er in erros:
            print("✗", er)
        print(f"{len(erros)} erro(s) de lint — corrija antes de gerar.")
        sys.exit(1)

    if site.exists():
        shutil.rmtree(site)
    site.mkdir(parents=True)

    todos_desafios = []
    busca = []
    urls = ["/"]
    desafios_por_trilha = {}

    for tid, t in config.TRILHAS.items():
        existentes = {a["pagina"] for a in t["aulas"] if (fontes / tid / a["arquivo"]).exists()}
        secoes = []
        n_des = 0
        for i, a in enumerate(t["aulas"]):
            caminho = fontes / tid / a["arquivo"]
            if not caminho.exists():
                continue
            texto = _ler(caminho)
            html, itens, desafios = _renderizar_aula(t, a, texto)
            _escrever(site / tid / a["pagina"], paginas.pagina_aula(t, a, i, html, itens, existentes))
            urls.append(f"/{tid}/{a['pagina']}")
            todos_desafios += desafios
            n_des += len(desafios)
            rot = "Capítulo" if tid == "deploy" else "Aula"
            busca.append(
                {
                    "u": f"{tid}/{a['pagina']}",
                    "t": f"{rot} {a['num']} — {a['titulo']}",
                    "tr": t["curto"],
                    "h": [x for _, _, x in itens if not x.startswith(("🏆", "🐛", "📚", "🏠", "✅", "🎯", "📋", "🗺"))][:40],
                    "d": [d["titulo"] for d in desafios],
                }
            )
            prefixo = f"a{a['num']}"
            html_pref = render.prefixar_ids(html, prefixo)
            secoes.append({"aula": a, "i": i, "html": html_pref, "toc": [(n, f"{prefixo}-{ident}", x) for n, ident, x in itens]})
        desafios_por_trilha[tid] = n_des
        _escrever(site / tid / "index.html", paginas.pagina_indice_trilha(t, n_des, existentes))
        urls.append(f"/{tid}/")
        if secoes:
            _escrever(site / tid / "apostila.html", paginas.apostila_unica(t, secoes))
            urls.append(f"/{tid}/apostila.html")

    # projetos integradores → desafios com trilha "projetos"
    proj_md = fontes / "desafios" / "projetos-integradores.md"
    projetos_html = ""
    if proj_md.exists():
        texto = _ler(proj_md)
        aula_fake = {"trilha": "projetos", "num": "—", "titulo": "Projetos integradores", "pagina": "index.html"}
        # extrai como se fosse uma seção de desafios
        texto_sec = "## 🏆 Desafios\n\n" + texto if not re.search(r"^##\s+🏆", texto, re.M) else texto
        projetos = render.extrair_desafios(texto_sec, aula_fake)
        projetos_html = render.enfeitar_desafios(render.enfeitar(render.converter(texto)), projetos)
        todos_desafios += projetos
        busca.append({"u": "desafios/", "t": "Projetos integradores", "tr": "Desafios", "h": [], "d": [p["titulo"] for p in projetos]})

    tags_contagem = Counter(tg for d in todos_desafios for tg in d["tags"])
    _escrever(site / "desafios" / "index.html", paginas.pagina_desafios(todos_desafios, projetos_html, tags_contagem))
    urls.append("/desafios/")

    # links
    links_md = fontes / "links.md"
    n_links = 0
    links_html, itens = "", []
    if links_md.exists():
        texto = _ler(links_md)
        n_links = len(re.findall(r"^\s*[-*]\s+\[[^\]]+\]\(https?://", texto, re.M))
        links_html = render.enfeitar(render.converter(texto))
        itens = [(n, i, x) for n, i, x in render.sumario(links_html) if n == "2"]
        busca.append({"u": "links/", "t": "Links úteis", "tr": "Links", "h": [x for _, _, x in itens], "d": []})
    _escrever(site / "links" / "index.html", paginas.pagina_links(links_html, itens))
    urls.append("/links/")

    # home
    home_md = fontes / "home.md"
    home_html = render.enfeitar(render.converter(_ler(home_md))) if home_md.exists() else ""
    totais = {
        "aulas": sum(len(t["aulas"]) for t in config.TRILHAS.values()),
        "desafios": len(todos_desafios),
        "links": n_links,
        "desafios_por_trilha": desafios_por_trilha,
    }
    _escrever(site / "index.html", paginas.pagina_home(home_html, totais))

    # utilitários
    _escrever(site / "404.html", paginas.pagina_404())
    _escrever(site / "busca.json", json.dumps(busca, ensure_ascii=False, separators=(",", ":")))
    _escrever(site / "robots.txt", f"User-agent: *\nAllow: /\nSitemap: {config.URL_BASE}/sitemap.xml\n")
    sm = "".join(f"  <url><loc>{config.URL_BASE}{u}</loc></url>\n" for u in urls)
    _escrever(site / "sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}</urlset>\n')

    problemas = checar_links(site)
    for p in problemas:
        print("⚠", p)
    print(f"site/ gerado: {len(urls)} páginas, {len(todos_desafios)} desafios, {n_links} links, {len(problemas)} link(s) quebrado(s)")
    return problemas


_RE_HREF = re.compile(r'(?:href|src)="([^"]+)"')
_RE_ID = re.compile(r'\bid="([^"]+)"')


def checar_links(site: Path):
    """Confere que todo href/src relativo aponta para arquivo existente (e âncora existente)."""
    ids_cache = {}

    def ids_de(arq: Path):
        if arq not in ids_cache:
            ids_cache[arq] = set(_RE_ID.findall(_ler(arq))) if arq.exists() else set()
        return ids_cache[arq]

    problemas = []
    for arq in site.rglob("*.html"):
        texto = _ler(arq)
        proprios = set(_RE_ID.findall(texto))
        # ignora o JS/CSS inline (contém strings com href=)
        texto = re.sub(r"<script>[\s\S]*?</script>|<style>[\s\S]*?</style>", "", texto)
        for alvo in set(_RE_HREF.findall(texto)):
            if alvo.startswith(("http://", "https://", "mailto:", "data:", "javascript:", "tel:")):
                continue
            base, _, frag = alvo.partition("#")
            base = base.split("?", 1)[0]
            if not base:
                if frag and frag not in proprios and not frag.startswith("aula-"):
                    problemas.append(f"{arq.relative_to(site)}: âncora #{frag} não existe")
                continue
            if base.startswith("/"):
                destino = site / base.lstrip("/")
            else:
                destino = (arq.parent / base).resolve()
            if destino.is_dir():
                destino = destino / "index.html"
            if not destino.exists():
                problemas.append(f"{arq.relative_to(site)}: link para '{alvo}' não existe")
                continue
            if frag and destino.suffix == ".html" and frag not in ids_de(destino):
                problemas.append(f"{arq.relative_to(site)}: âncora '{alvo}' não existe")
    return sorted(problemas)


if __name__ == "__main__":
    gerar(parcial="--parcial" in sys.argv)
