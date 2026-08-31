"""Templates HTML do WebLab. Só monta strings; não faz I/O (exceto ler theme.css/app.js uma vez)."""
import html as H
import json
from pathlib import Path

from build import config, render

_AQUI = Path(__file__).resolve().parent
CSS = (_AQUI / "theme.css").read_text(encoding="utf-8")
JS = (_AQUI / "app.js").read_text(encoding="utf-8")

TRILHAS_NAV = [
    ("nivel-1", "Nível 1"), ("nivel-2", "Nível 2"), ("nivel-3", "Nível 3"),
    ("deploy", "Deploy"), ("desafios", "Desafios"), ("links", "Links"),
]


def e(s) -> str:
    return H.escape(str(s), quote=True)


# --------------------------------------------------------------------------
# base
# --------------------------------------------------------------------------
def pagina_base(titulo, descricao, corpo, lateral_html="", toc_html="", trilha_id="home", raiz_rel="./",
                body_class="", canonico=""):
    nav = "".join(
        f'<a href="{raiz_rel}{tid}/" class="{"ativo" if tid == trilha_id else ""}">{e(nome)}</a>'
        for tid, nome in TRILHAS_NAV
    )
    classes = ["wrap"]
    if not lateral_html:
        classes.append("sem-lateral")
    if not toc_html:
        classes.append("sem-toc")
    lateral = f'<nav class="lateral" id="lateral" aria-label="Aulas"><button class="btn fechar" type="button">✕ Fechar</button>{lateral_html}</nav>' if lateral_html else ""
    toc = f'<aside class="toc" id="toc" aria-label="Nesta página">{toc_html}</aside>' if toc_html else ""
    menu_btn = '<button class="btn" id="menu-btn" type="button" aria-expanded="false" aria-controls="lateral">☰ Aulas</button>' if lateral_html else ""
    can = f'<link rel="canonical" href="{e(canonico)}">' if canonico else ""
    return f"""<!DOCTYPE html>
<html lang="pt-BR" data-tema="claro" data-trilha="{e(trilha_id)}" data-raiz="{e(raiz_rel)}">
<head>
<meta charset="utf-8">
<script>try{{var t=localStorage.getItem('weblab:tema');if(!t&&window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches)t='escuro';if(t)document.documentElement.setAttribute('data-tema',t)}}catch(e){{}}</script>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(titulo)}</title>
<meta name="description" content="{e(descricao)}">
<meta name="author" content="{e(config.PROFESSOR)}">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(descricao)}">
<meta property="og:site_name" content="WebLab">
{can}
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%234f46e5'/%3E%3Cpath d='M8 8h16M8 16h16M8 24h16M8 8v16M16 8v16M24 8v16' stroke='%23fff' stroke-width='2' opacity='.9'/%3E%3C/svg%3E">
<style>
{CSS}
{render.PYG_CSS}
</style>
</head>
<body class="{e(body_class)}">
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
<div id="progresso" role="presentation"></div>
<header class="topo"><div class="topo-in">
  {menu_btn}
  <a class="logo" href="{raiz_rel}"><span class="q" aria-hidden="true"></span>WebLab<small>UNEMAT</small></a>
  <nav class="trilhas-nav" aria-label="Trilhas">{nav}</nav>
  <span class="espaco"></span>
  <div class="busca-wrap">
    <input id="busca" type="search" placeholder="Buscar aulas e desafios… ( / )" autocomplete="off" aria-label="Buscar no WebLab">
    <div id="busca-res" hidden></div>
  </div>
  <button class="btn" id="tema" type="button" aria-label="Alternar tema claro/escuro">Tema</button>
</div></header>
<div class="{' '.join(classes)}">
  {lateral}
  <main id="conteudo">{corpo}
    <div class="rodape">
      <strong>WebLab</strong> — {e(config.SUBTITULO)} · {e(config.INSTITUICAO)}<br>
      {e(config.PROFESSOR)} · Material didático de uso educacional; livre para consulta, estudo e reuso com atribuição.<br>
      <a href="{raiz_rel}">Início</a> · <a href="{raiz_rel}desafios/">Banco de Desafios</a> · <a href="{raiz_rel}links/">Links úteis</a> · <a href="https://github.com/ivanlppires/weblab">Fontes no GitHub</a>
    </div>
  </main>
  {toc}
</div>
<script>
{JS}
</script>
</body>
</html>"""


# --------------------------------------------------------------------------
# aulas
# --------------------------------------------------------------------------
def menu_lateral(trilha, atual=None, apostila=False, existentes=None):
    """Lista de aulas da trilha; com apostila=True os links usam data-ir (arquivo único).

    existentes: conjunto de páginas já geradas (build parcial); as demais ficam sem link.
    """
    partes = [f'<h4>{e(trilha["curto"])} · {e(trilha["titulo_curto"])}</h4><ol>']
    grupo = None
    for a in trilha["aulas"]:
        if a["unidade"] != grupo:
            grupo = a["unidade"]
            nome_u = trilha["unidades"].get(grupo, "")
            partes.append(f'<li class="grupo">Unidade {grupo} · {e(nome_u)}</li>')
        disponivel = existentes is None or a["pagina"] in existentes
        href = f'#aula-{a["num"]}' if apostila else (a["pagina"] if disponivel else "#")
        extra = f' data-ir="{a["num"]}"' if apostila else ""
        cls = "ativo" if a["num"] == atual else ("breve" if not disponivel else "")
        partes.append(
            f'<li><a class="{cls}" href="{href}"{extra} data-aula-id="{trilha["id"]}/{a["pagina"]}">'
            f'<span class="num">{a["num"]}</span><span>{e(a["titulo"])}</span></a></li>'
        )
    partes.append("</ol>")
    if apostila:
        partes.append('<div class="todas"><a href="index.html">← Índice da trilha</a></div>')
    else:
        partes.append('<div class="todas"><a href="index.html">← Índice da trilha</a> &nbsp;·&nbsp; <a href="apostila.html">Apostila em arquivo único</a></div>')
    return "".join(partes)


def toc_html(itens, titulo="Nesta aula"):
    if not itens:
        return ""
    out = [f"<h4>{e(titulo)}</h4>"]
    for nivel, ident, txt in itens:
        cls = "n3" if nivel == "3" else ""
        out.append(f'<a class="{cls}" href="#{e(ident)}">{e(txt)}</a>')
    return "".join(out)


def cabecalho_aula(trilha, a, apostila=False):
    rot = "Capítulo" if trilha["id"] == "deploy" else "Aula"
    nome_u = trilha["unidades"].get(a["unidade"], "")
    tags = [
        f'<span class="tag acento">{e(trilha["curto"])}</span>',
        f'<span class="tag">Unidade {a["unidade"]} · {e(nome_u)}</span>',
    ]
    if trilha["tipo"] == "aula":
        tags.append('<span class="tag">3 aulas de 50 min + 1 h EAD</span>')
    if a["avaliacao"]:
        tags.append(f'<span class="tag av">Fecha a unidade · Avaliação {a["avaliacao"]}</span>')
    h1 = f'<h1>{rot} {a["num"]} — <span class="marca-texto">{e(a["titulo"])}</span></h1>'
    return (
        '<div class="cabecalho">'
        f'<div class="tags">{"".join(tags)}</div>{h1}'
        f'<div class="sub">{e(trilha["nome"])} · {e(trilha["codigo"])} · WebLab · {e(config.PROFESSOR)}</div>'
        "</div>"
    )


def navpe(trilha, i, apostila=False, existentes=None):
    aulas = trilha["aulas"]
    ant = aulas[i - 1] if i > 0 else None
    pro = aulas[i + 1] if i < len(aulas) - 1 else None
    if existentes is not None and not apostila:
        if ant and ant["pagina"] not in existentes:
            ant = None
        if pro and pro["pagina"] not in existentes:
            pro = None
    rot = "Capítulo" if trilha["id"] == "deploy" else "Aula"
    h = ['<nav class="navpe" aria-label="Navegação entre aulas">']
    if ant:
        href = f'#aula-{ant["num"]}' if apostila else ant["pagina"]
        extra = f' data-ir="{ant["num"]}"' if apostila else ' data-nav="anterior"'
        h.append(f'<a href="{href}"{extra}><span class="rot">← {rot} {ant["num"]}</span><span class="tit">{e(ant["titulo"])}</span></a>')
    else:
        h.append(f'<a href="index.html" data-nav="anterior"><span class="rot">← Índice</span><span class="tit">{e(trilha["nome"])}</span></a>')
    if pro:
        href = f'#aula-{pro["num"]}' if apostila else pro["pagina"]
        extra = f' data-ir="{pro["num"]}"' if apostila else ' data-nav="proxima"'
        h.append(f'<a class="dir" href="{href}"{extra}><span class="rot">{rot} {pro["num"]} →</span><span class="tit">{e(pro["titulo"])}</span></a>')
    else:
        h.append('<a class="dir" href="../desafios/" data-nav="proxima"><span class="rot">Trilha concluída →</span><span class="tit">Encare o Banco de Desafios</span></a>')
    h.append("</nav>")
    return "".join(h)


def concluir(trilha, a):
    return (
        f'<label class="concluir"><input type="checkbox" id="concluir" data-chave="weblab:aula:{trilha["id"]}/{a["pagina"]}">'
        " Concluí esta aula (fica salvo só neste navegador)</label>"
    )


def pagina_aula(trilha, a, i, corpo_html, itens_toc, existentes=None):
    rot = "Capítulo" if trilha["id"] == "deploy" else "Aula"
    corpo = cabecalho_aula(trilha, a) + corpo_html + concluir(trilha, a) + navpe(trilha, i, existentes=existentes)
    return pagina_base(
        titulo=f'{rot} {a["num"]} — {a["titulo"]} · {trilha["curto"]} · WebLab',
        descricao=f'{trilha["nome"]} · Unidade {a["unidade"]} · {a["titulo"]}',
        corpo=corpo,
        lateral_html=menu_lateral(trilha, a["num"], existentes=existentes),
        toc_html=toc_html(itens_toc),
        trilha_id=trilha["id"],
        raiz_rel="../",
        canonico=f'{config.URL_BASE}/{trilha["id"]}/{a["pagina"]}',
    )


# --------------------------------------------------------------------------
# índice da trilha
# --------------------------------------------------------------------------
def _ids_aulas(trilha):
    return json.dumps([f'{trilha["id"]}/{a["pagina"]}' for a in trilha["aulas"]])


def barra_progresso(trilha):
    return (
        f'<div class="progresso-trilha" data-aulas=\'{_ids_aulas(trilha)}\'>'
        '<span class="rot">Seu progresso</span><span class="barra"><i></i></span><b>0/0</b></div>'
    )


def pagina_indice_trilha(trilha, n_desafios, aulas_existentes):
    t = trilha
    rot = "Capítulo" if t["id"] == "deploy" else "Aula"
    # cartões por unidade
    cards = []
    grupo = None
    for a in t["aulas"]:
        if a["unidade"] != grupo:
            grupo = a["unidade"]
            cards.append(
                f'<div class="unidade-titulo"><span class="eyebrow">Unidade {grupo}</span><h3>{e(t["unidades"].get(grupo, ""))}</h3></div><div class="grade">'
                if grupo == 1 else
                f'</div><div class="unidade-titulo"><span class="eyebrow">Unidade {grupo}</span><h3>{e(t["unidades"].get(grupo, ""))}</h3></div><div class="grade">'
            )
        disponivel = a["pagina"] in aulas_existentes
        href = a["pagina"] if disponivel else "#"
        av = f'<span class="av">Fecha a unidade · Avaliação {a["avaliacao"]}</span>' if a["avaliacao"] else ""
        breve = "" if disponivel else '<span class="av">Em breve</span>'
        cards.append(
            f'<a class="cartao" href="{href}" data-aula-id="{t["id"]}/{a["pagina"]}">'
            f'<div class="meta"><span>{rot} {a["num"]}</span><span>Unidade {a["unidade"]}</span></div>'
            f'<div class="t">{e(a["titulo"])}</div>{av}{breve}</a>'
        )
    cards.append("</div>")

    # cronograma
    cron = ""
    if t["id"] in config.CRONOGRAMA:
        linhas = "".join(
            f'<tr><td>{e(c["data"])}</td><td>{c["num"]}</td><td>{e(c["descricao"])}{" <strong>⏰</strong>" if c.get("prazo") else ""}</td></tr>'
            for c in config.CRONOGRAMA[t["id"]]
        )
        cron = f"""
<h2 id="cronograma">Cronograma{" " + e(config.SEMESTRE) if config.SEMESTRE else ""}</h2>
<p class="nota">Datas conforme o Plano de Curso da turma no SIGAA. ⏰ marca o dia de entrega de uma avaliação. Em caso de divergência com o calendário da turma, vale o aviso do professor.</p>
<div class="tabela-wrap"><table><thead><tr><th>Data</th><th>{rot}</th><th>Conteúdo</th></tr></thead><tbody>{linhas}</tbody></table></div>"""

    avals = ""
    if t["id"] in config.AVALIACOES:
        com_prazo = any(av.get("prazo") for av in config.AVALIACOES[t["id"]])
        col_prazo = "<th>Prazo</th>" if com_prazo else ""
        linhas = "".join(
            f'<tr><td>Avaliação {av["n"]}</td><td>{e(av["escopo"])}</td>'
            + (f'<td>{e(av.get("prazo", ""))}</td>' if com_prazo else "")
            + "</tr>"
            for av in config.AVALIACOES[t["id"]]
        )
        nota_prazo = "" if com_prazo else " Os prazos de cada avaliação são publicados no SIGAA e anunciados em aula."
        avals = f"""
<h2 id="avaliacao">Avaliação</h2>
<p>{e(config.REGRAS_APROVACAO)} Entregas via SIGAA.{nota_prazo} O exame final é uma prova teórica, presencial e individual sobre as três unidades.</p>
<div class="tabela-wrap"><table><thead><tr><th>Instrumento</th><th>Escopo</th>{col_prazo}</tr></thead><tbody>{linhas}</tbody></table></div>"""

    stack = "".join(f"<tr><td>{e(k)}</td><td>{e(v)}</td></tr>" for k, v in t["stack"])
    biblio = config.BIBLIOGRAFIA.get(t["id"], [])
    biblio_html = ("<h2 id=\"bibliografia\">Bibliografia da disciplina</h2><ul>" + "".join(f"<li>{e(b)}</li>" for b in biblio) + "</ul>") if biblio else ""

    n_aulas = len(t["aulas"])
    corpo = f"""
<div class="hero">
  <div class="eyebrow">{e(t["codigo"])} · {e(t["carga"])} · Pré-requisito: {e(t["prerequisito"])}</div>
  <h1><span class="marca-texto">{e(t["titulo_curto"])}</span></h1>
  <p class="lead">{e(t["resumo"])}</p>
  {barra_progresso(t)}
</div>
<div class="stats">
  <div class="stat"><div class="n">{n_aulas}</div><div class="l">{"Capítulos" if t["id"] == "deploy" else "Aulas"}</div></div>
  <div class="stat"><div class="n">{len(t["unidades"])}</div><div class="l">Unidades</div></div>
  <div class="stat"><div class="n">{n_desafios}</div><div class="l">Desafios</div></div>
  <div class="stat"><div class="n">1</div><div class="l">Projeto fio-condutor</div></div>
</div>
<p><a class="btn primario" href="{t["aulas"][0]["pagina"]}">Começar pela {rot.lower()} 01 →</a> &nbsp; <a class="btn" href="apostila.html">Apostila em arquivo único</a> &nbsp; <a class="btn" href="../desafios/?trilha={t["id"]}">Desafios desta trilha</a></p>

<h2 id="aulas">{"Capítulos" if t["id"] == "deploy" else "Aulas"}</h2>
{"".join(cards)}

<h2 id="projeto">Projeto fio-condutor: {e(t["projeto"])}</h2>
<p>{e(t["projeto_desc"])}</p>
<p><strong>Ementa:</strong> {e(t["ementa"])}</p>
{cron}
{avals}
<h2 id="stack">Stack e ferramentas</h2>
<div class="tabela-wrap"><table><thead><tr><th>Camada</th><th>Tecnologia</th></tr></thead><tbody>{stack}</tbody></table></div>
{biblio_html}
<h2 id="uso">Como usar este material</h2>
<ul>
<li>Cada aula tem objetivos, teoria com código completo, <strong>Mão na massa</strong> (guiado), <strong>Laboratório</strong> em três níveis (A fixação · B aplicação · C desafio), <strong>Desafios</strong> extras com estrelas, tabela de erros comuns e a atividade assíncrona da semana.</li>
<li>Marque <em>Concluí esta aula</em> ao fim de cada página e <em>Feito</em> em cada desafio: o progresso fica salvo neste navegador.</li>
<li>Todos os blocos de código têm botão <strong>Copiar</strong> — mas digite você mesmo: copiar e colar não fixa nada.</li>
<li>Atalhos: <kbd>j</kbd> próxima aula · <kbd>k</kbd> anterior · <kbd>/</kbd> busca. <kbd>Ctrl</kbd>+<kbd>P</kbd> imprime a aula limpa.</li>
</ul>
"""
    itens = [("2", "aulas", "Aulas"), ("2", "projeto", "Projeto fio-condutor")]
    if cron:
        itens.append(("2", "cronograma", "Cronograma" + (f" {config.SEMESTRE}" if config.SEMESTRE else "")))
    if avals:
        itens.append(("2", "avaliacao", "Avaliação"))
    itens += [("2", "stack", "Stack")]
    if biblio_html:
        itens.append(("2", "bibliografia", "Bibliografia"))
    itens.append(("2", "uso", "Como usar"))
    return pagina_base(
        titulo=f'{t["nome"]} · WebLab',
        descricao=t["resumo"],
        corpo=corpo,
        lateral_html=menu_lateral(t, existentes=aulas_existentes),
        toc_html=toc_html(itens, "Nesta página"),
        trilha_id=t["id"],
        raiz_rel="../",
        canonico=f'{config.URL_BASE}/{t["id"]}/',
    )


# --------------------------------------------------------------------------
# apostila única
# --------------------------------------------------------------------------
def apostila_unica(trilha, secoes):
    """secoes: [{'aula': a, 'i': i, 'html': corpo já com ids prefixados, 'toc': [(nivel,id,txt)]}]"""
    t = trilha
    partes = []
    for s in secoes:
        a = s["aula"]
        toc_dados = "".join(f'<a class="{"n3" if n == "3" else ""}" href="#{e(i)}">{e(x)}</a>' for n, i, x in s["toc"])
        partes.append(
            f'<section class="aula-secao" id="aula-{a["num"]}" data-aula="{a["num"]}">'
            + cabecalho_aula(t, a, apostila=True)
            + s["html"]
            + concluir(t, a).replace('id="concluir"', f'id="concluir-{a["num"]}"')
            + navpe(t, s["i"], apostila=True)
            + f'<div class="toc-dados">{toc_dados}</div></section>'
        )
    corpo = (
        f'<p class="nota">Apostila de arquivo único — {e(t["nome"])}. Uma aula por vez; use <kbd>j</kbd>/<kbd>k</kbd> ou o menu lateral. '
        f'<a href="index.html">Voltar ao índice</a>.</p>' + "".join(partes)
    )
    return pagina_base(
        titulo=f'Apostila — {t["nome"]} · WebLab',
        descricao=f'Todas as aulas de {t["nome"]} em um único arquivo.',
        corpo=corpo,
        lateral_html=menu_lateral(t, apostila=True),
        toc_html="<h4>Nesta aula</h4>",
        trilha_id=t["id"],
        raiz_rel="../",
        canonico=f'{config.URL_BASE}/{t["id"]}/apostila.html',
    )


# --------------------------------------------------------------------------
# home
# --------------------------------------------------------------------------
def pagina_home(home_html, totais):
    cards = []
    for tid, t in config.TRILHAS.items():
        n = len(t["aulas"])
        cards.append(
            f'<a class="trilha-card {t["cor"]}" href="{tid}/">'
            f'<span class="eyebrow">{e(t["codigo"])}</span>'
            f'<h2>{e(t["nome"])}</h2><p>{e(t["resumo"])}</p>'
            f'<span class="meta">{n} {"capítulos" if tid == "deploy" else "aulas"} · {totais["desafios_por_trilha"].get(tid, 0)} desafios · projeto: {e(t["projeto"])}</span>'
            f"{barra_progresso(t)}</a>"
        )
    for xid, x in config.EXTRAS.items():
        cards.append(
            f'<a class="trilha-card {x["cor"]}" href="{xid}/"><span class="eyebrow">{"todas as trilhas" if xid == "desafios" else "curadoria"}</span>'
            f'<h2>{e(x["nome"])}</h2><p>{e(x["resumo"])}</p>'
            f'<span class="meta">{totais["desafios"] if xid == "desafios" else totais["links"]} {"desafios" if xid == "desafios" else "links"}</span></a>'
        )
    corpo = f"""
<div class="hero">
  <div class="eyebrow">WebLab · {e(config.SUBTITULO)} · {e(config.INSTITUICAO)}</div>
  <h1>Programação não se aprende lendo.<br><span class="marca-texto">Abra o editor.</span></h1>
  <p class="lead">Uma apostila online, gratuita e feita para ser praticada: três níveis de desenvolvimento web — do primeiro HTML ao full-stack com frameworks — mais uma trilha para colocar tudo no ar. Cada aula termina em código escrito por você.</p>
  <div class="acoes"><a class="btn primario" href="nivel-1/">Começar do zero</a><a class="btn" href="desafios/">Ver os desafios</a><a class="btn" href="links/">Links úteis</a></div>
</div>
<div class="stats">
  <div class="stat"><div class="n">{totais["aulas"]}</div><div class="l">Aulas e capítulos</div></div>
  <div class="stat"><div class="n">{totais["desafios"]}</div><div class="l">Desafios</div></div>
  <div class="stat"><div class="n">3</div><div class="l">Projetos fio-condutor</div></div>
  <div class="stat"><div class="n">{totais["links"]}</div><div class="l">Links curados</div></div>
</div>
<div class="trilhas">{"".join(cards)}</div>
{home_html}
"""
    return pagina_base(
        titulo="WebLab — Laboratório de Desenvolvimento Web · UNEMAT",
        descricao="Apostila online de desenvolvimento web em três níveis (HTML/CSS/JS, front e back-end, frameworks modernos) mais deploy, banco de desafios e links úteis.",
        corpo=corpo,
        trilha_id="home",
        raiz_rel="./",
        body_class="home",
        canonico=f"{config.URL_BASE}/",
    )


# --------------------------------------------------------------------------
# banco de desafios
# --------------------------------------------------------------------------
NOME_TRILHA_CURTO = {"nivel-1": "Nível 1", "nivel-2": "Nível 2", "nivel-3": "Nível 3", "deploy": "Deploy", "projetos": "Projeto"}


def pagina_desafios(desafios, projetos_html, tags_contagem):
    fichas = []
    for d in desafios:
        if d["trilha"] == "projetos":
            href = f'#{d["ancora"]}'
            aula_rot = "Projeto integrador"
        else:
            rot = "Cap." if d["trilha"] == "deploy" else "Aula"
            href = f'../{d["trilha"]}/{d["pagina"]}#{d["ancora"]}'
            aula_rot = f'{rot} {d["aula_num"]} · {d["aula_titulo"]}'
        fichas.append(
            f'<article class="ficha {d["trilha"]}" data-trilha="{d["trilha"]}" data-dificuldade="{d["dificuldade"]}" data-tags="{e(" ".join(d["tags"]))}">'
            f'<div class="meta"><span class="tr">{e(NOME_TRILHA_CURTO.get(d["trilha"], d["trilha"]))}</span><span>{e(aula_rot)}</span></div>'
            f'<h3><a href="{e(href)}">{e(d["titulo"])}</a></h3>'
            f'<p>{e(d["resumo"])}</p>'
            f'<div class="pe"><span class="estrelas" title="{e(render.rotulo_dificuldade(d["dificuldade"]))}">{render.estrelas(d["dificuldade"])}</span>'
            f'<span class="tags-inline">{"".join(f"<span class=chip>{e(t)}</span> " for t in d["tags"][:4])}</span>'
            f'<label class="feito"><input type="checkbox" data-chave="weblab:desafio:{e(d["id"])}"> Feito</label></div>'
            "</article>"
        )
    opcoes = "".join(f'<option value="{tid}">{e(nome)}</option>' for tid, nome in NOME_TRILHA_CURTO.items())
    nuvem = "".join(
        f'<button type="button" data-tag="{e(t)}">{e(t)} <small>{n}</small></button>'
        for t, n in sorted(tags_contagem.items(), key=lambda x: (-x[1], x[0]))[:40]
    )
    corpo = f"""
<div class="hero">
  <div class="eyebrow">Banco de Desafios · todas as trilhas</div>
  <h1><span class="marca-texto">Desafios</span> para quem quer ir além</h1>
  <p class="lead">Todos os desafios das aulas em um só lugar, mais projetos integradores. ⭐ leva uma ou duas horas; ⭐⭐ uma tarde; ⭐⭐⭐ um fim de semana; 🔥 é o boss da unidade. Marque <em>Feito</em> e acompanhe: <strong id="desafios-feitos">0</strong> concluídos neste navegador.</p>
</div>
<div class="filtros" role="search">
  <select id="f-trilha" aria-label="Filtrar por trilha"><option value="">Todas as trilhas</option>{opcoes}</select>
  <span class="dific" role="group" aria-label="Dificuldade">
    <button type="button" data-d="1">⭐</button><button type="button" data-d="2">⭐⭐</button><button type="button" data-d="3">⭐⭐⭐</button><button type="button" data-d="boss">🔥 Boss</button>
  </span>
  <label><input type="checkbox" id="f-nao-feitos"> só os que faltam</label>
  <input type="search" id="f-texto" placeholder="Filtrar por texto…" aria-label="Filtrar por texto">
</div>
<div class="tags-nuvem" aria-label="Filtrar por tema">{nuvem}</div>
<div class="contagem" id="contagem"></div>
<div class="fichas">{"".join(fichas)}</div>
<div class="projetos-integradores">
<h2 id="projetos-integradores">Projetos integradores</h2>
<p>Projetos maiores, para juntar tudo o que você aprendeu em uma trilha. Cada um tem critérios de pronto e evoluções sugeridas — escolha um, publique e coloque no portfólio.</p>
{projetos_html}
</div>
"""
    return pagina_base(
        titulo="Banco de Desafios · WebLab",
        descricao="Todos os desafios do WebLab, filtráveis por trilha, tema e dificuldade, mais projetos integradores.",
        corpo=corpo,
        trilha_id="desafios",
        raiz_rel="../",
        body_class="largo",
        canonico=f"{config.URL_BASE}/desafios/",
    ).replace('<div class="wrap sem-lateral sem-toc">', '<div class="wrap largo">')


# --------------------------------------------------------------------------
# links
# --------------------------------------------------------------------------
def pagina_links(links_html, itens_toc):
    corpo = f"""
<div class="hero">
  <div class="eyebrow">Curadoria · documentação, prática, ferramentas e comunidade</div>
  <h1><span class="marca-texto">Links úteis</span> para desenvolver</h1>
  <p class="lead">Cada link tem uma linha dizendo por que ele está aqui. Comece pela documentação oficial: é a fonte que não desatualiza.</p>
</div>
{links_html}
"""
    return pagina_base(
        titulo="Links úteis · WebLab",
        descricao="Links curados para desenvolvimento web: documentação, prática, ferramentas, APIs públicas, design, acessibilidade, deploy e comunidades.",
        corpo=corpo,
        toc_html=toc_html(itens_toc, "Categorias"),
        trilha_id="links",
        raiz_rel="../",
        body_class="links-pagina",
        canonico=f"{config.URL_BASE}/links/",
    )


def pagina_404():
    corpo = """
<h1>404</h1>
<p class="lead">Essa página não existe — ou ainda não foi escrita.</p>
<p><a class="btn primario" href="/">Ir para o início</a> &nbsp; <a class="btn" href="/desafios/">Banco de Desafios</a></p>
<p class="nota">Dica de desenvolvedor: abra o DevTools (F12) → aba Network e veja o status desta resposta. É um 404 de verdade.</p>
"""
    return pagina_base(
        titulo="Página não encontrada · WebLab",
        descricao="404",
        corpo=corpo,
        trilha_id="home",
        raiz_rel="/",
        body_class="pagina-404",
    )
