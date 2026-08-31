"""Dados do WebLab: trilhas, aulas, unidades, avaliações e o calendário opcional.

O material é ATEMPORAL e ABERTO: nenhuma aula traz datas, semestre, turma, nota,
prazo ou entrega institucional — serve a qualquer pessoa que queira estudar.
No lugar das avaliações há MARCOS: o que o projeto do estudante precisa ter ao
fim de cada unidade.
O calendário de um semestre é um acréscimo opcional que aparece só no índice
de cada trilha. Para publicá-lo, preencha SEMESTRE, CRONOGRAMA e (se quiser)
o campo "prazo" de cada item de MARCOS — o passo a passo e o calendário
de 2026.2, usado na primeira oferta, estão em docs/calendario-2026-2.md.

Com SEMESTRE vazio e CRONOGRAMA vazio (o padrão), o site não mostra nenhuma
data e serve a qualquer turma.
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FONTES = RAIZ / "fontes"
SITE = RAIZ / "site"

URL_BASE = "https://weblab.ivanpires.dev"
NOME_SITE = "WebLab"
SUBTITULO = "Laboratório de Desenvolvimento Web"
INSTITUICAO = "UNEMAT — Universidade do Estado de Mato Grosso · Campus Sinop · FACET"
PROFESSOR = "Prof. Ivan Luiz Pedroso Pires"
SEMESTRE = ""  # ex.: "2027.1"; vazio deixa o site atemporal


def _aulas(trilha, prefixo, itens, unidades, marcos):
    """Monta a lista de aulas de uma trilha a partir de (num, slug, título)."""
    out = []
    for num, slug, titulo in itens:
        n = int(num)
        unidade = next((u for u, (a, b) in unidades.items() if a <= n <= b), None)
        out.append(
            {
                "trilha": trilha,
                "num": num,
                "slug": slug,
                "titulo": titulo,
                "unidade": unidade,
                "marco": marcos.get(num),
                "arquivo": f"{prefixo}-{num}-{slug}.md",
                "pagina": f"{prefixo}-{num}.html",
            }
        )
    return out


# --------------------------------------------------------------------------
# Nível 1 — Introdução ao Desenvolvimento Web (FACET-SNP-319)
# --------------------------------------------------------------------------
_N1 = [
    ("01", "apresentacao-tecnologias-e-arquitetura-web", "Apresentação, tecnologias e arquitetura da Web"),
    ("02", "introducao-ao-html", "Introdução ao HTML: estrutura, textos, links e tabelas"),
    ("03", "introducao-aos-formularios", "Introdução aos formulários"),
    ("04", "formularios-midias-e-listas", "Formulários, mídias e listas"),
    ("05", "layout-html-e-introducao-ao-css", "Elementos HTML para layout e introdução ao CSS"),
    ("06", "css-sintaxe-seletores-e-valores", "CSS: sintaxe, seletores, classes, atributos e valores"),
    ("07", "layout-de-um-website-e-menu", "Formatando o layout de um website e o menu"),
    ("08", "telas-responsivas", "Criando telas responsivas"),
    ("09", "animacoes-e-efeitos-em-css", "Animações e efeitos em CSS"),
    ("10", "introducao-ao-javascript", "Introdução ao JavaScript"),
    ("11", "variaveis-operadores-e-controle", "Variáveis, operações aritméticas e estruturas de controle"),
    ("12", "sequencia-condicao-e-repeticao", "Estruturas sequenciais, condicionais e de repetição"),
    ("13", "funcoes-e-eventos", "Funções e eventos"),
    ("14", "validacao-de-formularios-e-consultas-dinamicas", "JavaScript para validação de formulários e consultas dinâmicas"),
    ("15", "publicando-seu-website", "Publicando seu website na internet"),
]

# --------------------------------------------------------------------------
# Nível 2 — Desenvolvimento Web (FACET-SNP-307)
# --------------------------------------------------------------------------
_N2 = [
    ("01", "arquitetura-web-ambiente-e-git", "Apresentação, arquitetura web, ambiente de desenvolvimento e Git"),
    ("02", "introducao-ao-desenvolvimento-web-moderno", "Introdução ao desenvolvimento web moderno"),
    ("03", "revisao-de-html-layout-links-e-formularios", "Revisão de HTML: layout, links e formulários"),
    ("04", "frameworks-css", "Frameworks CSS: Bootstrap, Tailwind e Material"),
    ("05", "animacao-e-svg", "Animação e SVG"),
    ("06", "acessibilidade-e-aria", "Acessibilidade e ARIA"),
    ("07", "revisao-de-javascript-dom-e-eventos", "Revisão de JavaScript: objetos, funções, eventos e DOM"),
    ("08", "arrow-functions-callbacks-e-vetores", "Arrow functions, callbacks e operações em vetores"),
    ("09", "promises-e-async-await", "Promises e async/await"),
    ("10", "ajax-json-e-spa", "AJAX, JSON e Single Page Application"),
    ("11", "introducao-ao-nodejs-e-express", "Introdução ao Node.js e Express"),
    ("12", "express-estruturado-e-middlewares", "Express estruturado e middlewares"),
    ("13", "rotas-e-controladores", "Rotas e controladores"),
    ("14", "autenticacao-com-google-oauth", "Autenticação com Google (OAuth 2.0)"),
    ("15", "crud-com-front-end-assincrono", "CRUD com front-end assíncrono"),
    ("16", "crud-completo-com-autenticacao", "CRUD completo com autenticação e entrega final"),
]

# --------------------------------------------------------------------------
# Nível 3 — Frameworks Modernos (FACET-SNP-310)
# --------------------------------------------------------------------------
_N3 = [
    ("01", "apresentacao-e-revisao-javascript", "Apresentação da disciplina e revisão de JavaScript"),
    ("02", "introducao-ao-vue-diretivas", "Introdução ao Vue: instância, ciclo de vida e diretivas"),
    ("03", "vue-listas-computed-ciclo-de-vida", "Vue: listas, computed e ciclo de vida"),
    ("04", "vuetify-e-vue-router", "Introdução a Vuetify e Vue Router"),
    ("05", "componentes-router-avancado-vuetify", "Componentes, Vue Router e Vuetify avançado"),
    ("06", "axios-e-pinia", "Axios e Pinia"),
    ("07", "firebase-nodejs-express", "Introdução ao Firebase, Node.js e Express"),
    ("08", "endpoints-e-middlewares", "Definindo endpoints e middlewares"),
    ("09", "integrando-mysql", "Integrando com SGBD MySQL"),
    ("10", "autenticacao-firebase", "Requisições autenticadas com Firebase"),
    ("11", "crud-integrando-front-e-back", "Integrando front-end com back-end: CRUD"),
    ("12", "crud-supabase", "CRUD com banco em nuvem (Supabase)"),
    ("13", "desenvolvimento-do-backend", "Desenvolvimento do back-end em camadas"),
    ("14", "documentacao-com-swagger", "Documentação com Swagger"),
    ("15", "deploy-e-apresentacao", "Deploy, apresentação e finalização"),
]

# --------------------------------------------------------------------------
# Deploy & Ferramentas (trilha transversal)
# --------------------------------------------------------------------------
_DEPLOY = [
    ("01", "caixa-de-ferramentas-do-dev-web", "Caixa de ferramentas do dev web"),
    ("02", "git-e-github-do-zero-ao-pull-request", "Git e GitHub do zero ao pull request"),
    ("03", "publicando-sites-estaticos", "Publicando sites estáticos"),
    ("04", "dominios-dns-e-https", "Domínios, DNS e HTTPS"),
    ("05", "publicando-o-back-end-node", "Publicando o back-end Node"),
    ("06", "servidor-proprio-vps-com-nginx", "Servidor próprio (VPS) com nginx"),
    ("07", "docker-para-desenvolvedores-web", "Docker para desenvolvedores web"),
    ("08", "bancos-de-dados-na-nuvem", "Bancos de dados na nuvem"),
    ("09", "ci-cd-com-github-actions", "CI/CD com GitHub Actions"),
    ("10", "qualidade-performance-e-observabilidade", "Qualidade, performance e observabilidade"),
    ("11", "ia-como-ferramenta-de-desenvolvimento", "IA como ferramenta de desenvolvimento"),
]

TRILHAS = {
    "nivel-1": {
        "id": "nivel-1",
        "nome": "Nível 1 — Introdução ao Desenvolvimento Web",
        "curto": "Nível 1",
        "titulo_curto": "Introdução ao Desenvolvimento Web",
        "cor": "n1",
        "codigo": "FACET-SNP-319",
        "carga": "≈60 h de estudo · 15 h de prática guiada",
        "prerequisito": "Nenhum",
        "prefixo": "aula",
        "tipo": "aula",
        "resumo": "HTML, CSS e JavaScript do zero: como a Web funciona, páginas semânticas, "
                  "formulários, layouts responsivos, animações e os primeiros scripts interativos.",
        "ementa": "Arquiteturas computacionais para Web. Criação de páginas web com HTML, CSS e JavaScript.",
        "projeto": "Site institucional de um evento acadêmico",
        "projeto_desc": "Cinco páginas (início, programação, inscrição, palestrantes e contato) construídas "
                        "em HTML na Unidade 1, estilizadas e responsivas na Unidade 2 e interativas na Unidade 3. "
                        "Cada estudante replica a estrutura em um tema próprio.",
        "unidades": {1: "Arquitetura da Web e HTML", 2: "CSS: estilo, layout e responsividade", 3: "JavaScript e interatividade"},
        "aulas": _aulas("nivel-1", "aula", _N1, {1: (1, 5), 2: (6, 9), 3: (10, 15)}, {"06": 1, "10": 2, "15": 3}),
        "stack": [("Linguagens", "HTML5, CSS3, JavaScript (ES2015+)"), ("Editor", "VS Code + Live Server"),
                  ("Navegador", "Chrome/Firefox com DevTools"), ("Publicação", "GitHub Pages / Netlify")],
    },
    "nivel-2": {
        "id": "nivel-2",
        "nome": "Nível 2 — Desenvolvimento Web",
        "curto": "Nível 2",
        "titulo_curto": "Desenvolvimento Web: do front-end ao full-stack",
        "cor": "n2",
        "codigo": "FACET-SNP-307",
        "carga": "≈60 h de estudo · 15 h de prática guiada",
        "prerequisito": "Nível 1 concluído (ou HTML, CSS e JavaScript básicos)",
        "prefixo": "aula",
        "tipo": "aula",
        "resumo": "Do site estático profissional (frameworks CSS, SVG, acessibilidade) à SPA em JavaScript "
                  "assíncrono e ao back-end Node.js/Express com autenticação Google e CRUD.",
        "ementa": "Arquitetura de uma aplicação WEB. Tecnologias de Back-end. Tecnologias de Front-end. Bancos de dados para WEB.",
        "projeto": "Café Cerrado",
        "projeto_desc": "Uma cafeteria fictícia que começa como site estático (Unidade 1), ganha cardápio dinâmico, "
                        "busca e navegação SPA (Unidade 2) e termina como aplicação full-stack com API Express, "
                        "login Google e CRUD (Unidade 3). Cada estudante desenvolve um projeto autoral com a mesma arquitetura.",
        "unidades": {1: "Web estática", 2: "Web dinâmica client-side", 3: "Web dinâmica server-side"},
        "aulas": _aulas("nivel-2", "aula", _N2, {1: (1, 6), 2: (7, 10), 3: (11, 16)}, {"06": 1, "10": 2, "16": 3}),
        "stack": [("Front-end", "HTML5, CSS3, Bootstrap 5 / Tailwind 4, SVG, ARIA"), ("JavaScript", "ES2015+, DOM, fetch, Promises/async-await"),
                  ("Back-end", "Node.js 22 LTS, Express 5"), ("Autenticação", "Google Identity (OAuth 2.0 / ID token)"),
                  ("Persistência", "JSON em arquivo → banco de dados"), ("Ferramentas", "Git/GitHub, VS Code, REST Client")],
    },
    "nivel-3": {
        "id": "nivel-3",
        "nome": "Nível 3 — Frameworks Modernos",
        "curto": "Nível 3",
        "titulo_curto": "Frameworks Modernos: front-end e back-end",
        "cor": "n3",
        "codigo": "FACET-SNP-310",
        "carga": "≈60 h de estudo · 15 h de prática guiada",
        "prerequisito": "Nível 2 concluído (ou JavaScript assíncrono e Node/Express básicos)",
        "prefixo": "aula",
        "tipo": "aula",
        "resumo": "Vue 3, Vuetify, Vue Router, Pinia e Axios no front; Express 5, MySQL, Supabase, Firebase Auth "
                  "e Swagger no back — com os padrões de projeto que vivem dentro de cada ferramenta.",
        "ementa": "Desenvolvimento com uso de frameworks; padrões: criacionais, estruturais e comportamentais; "
                  "aplicação conjunta das abordagens de frameworks e componentes no desenvolvimento de software.",
        "projeto": "UniEventos",
        "projeto_desc": "Plataforma de divulgação e inscrição em eventos acadêmicos: SPA em Vue 3 + Vuetify + Pinia "
                        "consumindo uma API Express com MySQL/Supabase e autenticação Firebase. "
                        "Cada estudante desenvolve um projeto autoral com a mesma arquitetura e domínio diferente.",
        "unidades": {1: "Fundamentos de front-end com Vue.js", 2: "Vue.js avançado: Vuetify, Axios, Router e Pinia", 3: "Integração front-end/back-end"},
        "aulas": _aulas("nivel-3", "aula", _N3, {1: (1, 4), 2: (5, 6), 3: (7, 15)}, {"04": 1, "08": 2, "15": 3}),
        "stack": [("Runtime", "Node.js 22 LTS"), ("Front-end", "Vue 3.5 · Vite 8 · Vuetify 4 · Vue Router 5 · Pinia 4 · Axios 1.19"),
                  ("Back-end", "Express 5.2 · mysql2 · swagger-jsdoc/swagger-ui-express"),
                  ("Nuvem", "Firebase Auth 12 (modular) · Supabase (Postgres) · MySQL 8")],
    },
    "deploy": {
        "id": "deploy",
        "nome": "Deploy & Ferramentas",
        "curto": "Deploy",
        "titulo_curto": "Deploy & Ferramentas: colocando tudo online",
        "cor": "deploy",
        "codigo": "Trilha transversal",
        "carga": "11 capítulos · use em paralelo a qualquer nível",
        "prerequisito": "Nível 1 (aulas 1–5) para os capítulos 1–4; Nível 2 (Unidade 3) para os demais",
        "prefixo": "cap",
        "tipo": "deploy",
        "resumo": "Terminal, Git/GitHub, publicação de sites estáticos e de APIs Node, domínios e HTTPS, "
                  "servidor próprio com nginx, Docker, bancos na nuvem, CI/CD, qualidade e IA no fluxo de trabalho.",
        "ementa": "Ferramentas do ofício e publicação de aplicações web em produção.",
        "projeto": "Os três projetos das trilhas, no ar",
        "projeto_desc": "Cada capítulo publica de verdade algo construído nos níveis: o site do evento (N1) e o "
                        "Café Cerrado estático em GitHub Pages/Netlify; a API do Café Cerrado no Render e em um VPS "
                        "com nginx; o UniEventos com Docker, banco na nuvem e CI/CD.",
        "unidades": {1: "Ferramentas e versionamento", 2: "Publicação: estático, back-end, domínio e servidor", 3: "Infraestrutura, automação e qualidade"},
        "aulas": _aulas("deploy", "cap", _DEPLOY, {1: (1, 2), 2: (3, 6), 3: (7, 11)}, {}),
        "stack": [("Hospedagem estática", "GitHub Pages · Netlify · Vercel · Cloudflare Pages"), ("Back-end", "Render · Railway · Fly.io · VPS Ubuntu + nginx + pm2"),
                  ("Bancos", "Supabase · Neon · MySQL"), ("Automação", "Docker · GitHub Actions · certbot")],
    },
}

# Ordem e cores das trilhas extras (páginas geradas, não têm aulas)
EXTRAS = {
    "desafios": {"id": "desafios", "nome": "Banco de Desafios", "cor": "desafios",
                 "resumo": "Todos os desafios das trilhas em um só lugar, filtráveis por nível, tema e dificuldade — mais 12 projetos integradores."},
    "links": {"id": "links", "nome": "Links úteis", "cor": "links",
              "resumo": "Documentação oficial, prática guiada, ferramentas online, APIs públicas, design, acessibilidade, deploy e comunidades."},
}

# --------------------------------------------------------------------------
# Autoria — aparece na página /autores/, no CITATION.cff e nos metadados do DOI
# --------------------------------------------------------------------------
# papel: use os termos da taxonomia CRediT (credit.niso.org) em português.
#   "concepção"      — desenhou o material e a arquitetura
#   "redação"        — escreveu as aulas
#   "revisão"        — revisou tecnicamente (diga o que revisou em "escopo")
#   "software"       — escreveu o gerador do site
#   "curadoria"      — organizou desafios, links, exemplos
# ordem: quem entra depois vai para o fim da lista, salvo decisão em contrário.
AUTORES = [
    {
        "nome": "Ivan Luiz Pedroso Pires",
        "papel": ["concepção", "redação", "software", "curadoria"],
        "escopo": "Todas as trilhas e o gerador do site.",
        "instituicao": "UNEMAT — Campus Sinop, FACET",
        "orcid": "",   # ex.: "0000-0000-0000-0000"
        "lattes": "",  # ex.: "http://lattes.cnpq.br/0000000000000000"
        "principal": True,
    },
    # Exemplo de quem entra por revisão (remova o comentário e preencha):
    # {
    #     "nome": "Nome do colega",
    #     "papel": ["revisão"],
    #     "escopo": "Nível 2, aulas 11 a 16 (Node.js, Express e autenticação).",
    #     "instituicao": "Instituição",
    #     "orcid": "",
    #     "lattes": "",
    # },
]

# Crédito de revisão por aula: "trilha/num" -> ["Nome", ...]
# Ex.: REVISORES = {"nivel-2/11": ["Nome do colega"]}
REVISORES = {}

# --------------------------------------------------------------------------
# Calendário do semestre (opcional) — ver docs/calendario-2026-2.md
# --------------------------------------------------------------------------
CRONOGRAMA = {}  # {"nivel-1": [{"data": "dd/mm/aaaa", "num": "01", "descricao": "…", "prazo": True}, ...]}

MARCOS = {
    "nivel-1": [
        {"n": 1, "escopo": "Site em HTML com os elementos da Unidade 1 (estrutura, textos, links, tabelas, formulários, mídias, listas)."},
        {"n": 2, "escopo": "O mesmo site estilizado com CSS: layout, menu, responsividade e animações."},
        {"n": 3, "escopo": "O site dinâmico e interativo com JavaScript: eventos, validação de formulários e consultas dinâmicas."},
    ],
    "nivel-2": [
        {"n": 1, "escopo": "Website client-side em HTML e CSS: HTML semântico, layout responsivo, framework CSS, animação/SVG, acessibilidade."},
        {"n": 2, "escopo": "Evolução do site com JavaScript: validação de formulários, DOM e eventos, programação assíncrona, SPA com AJAX/JSON."},
        {"n": 3, "escopo": "Aplicação full-stack com Node.js e Express: rotas e controladores, autenticação Google, CRUD com persistência, front-end assíncrono."},
    ],
    "nivel-3": [
        {"n": 1, "escopo": "Vue 3 com CLI: estrutura, componentes, diretivas, Vuetify e Vue Router básico."},
        {"n": 2, "escopo": "Vue avançado: Vuetify + Axios + Vue Router + Pinia."},
        {"n": 3, "escopo": "Back-end com Express, banco de dados (MySQL/Supabase), autenticação Firebase, documentação e deploy."},
    ],
}

BIBLIOGRAFIA = {
    "nivel-1": [
        "SILVA, Maurício Samy. Criando sites com HTML: sites de alta qualidade com HTML e CSS. Novatec, 2008.",
        "TERUEL, Evandro C. HTML 5 — Guia Prático. Saraiva, 2014.",
        "MILETTO, Evandro M.; BERTAGNOLLI, Silvia C. Desenvolvimento de software II. Bookman, 2014.",
        "STEFANOV, Stoyan. Padrões JavaScript. Novatec, 2010.",
        "FLANAGAN, David. JavaScript: o guia definitivo. Bookman, 2014.",
    ],
    "nivel-2": [
        "QUEIRÓS, Ricardo; PORTELA, Filipe. Introdução ao Desenvolvimento Moderno para a Web: do front-end ao back-end, uma visão global. FCA, 2018.",
        "ALVES, William P. Projetos de Sistemas Web. Érica, 2015.",
        "LOUDON, Kyle. Desenvolvimento de Grandes Aplicações Web. Novatec, 2019.",
        "PUREWAL, Semmy. Aprendendo a Desenvolver Aplicações Web. Novatec, 2014.",
    ],
    "nivel-3": [
        "QUEIRÓS, Ricardo; PORTELA, Filipe. Introdução ao Desenvolvimento Moderno para a Web. FCA, 2018.",
        "ALVES, William P. Projetos de Sistemas Web. Érica, 2015.",
        "LOUDON, Kyle. Desenvolvimento de Grandes Aplicações Web. Novatec, 2019.",
        "ERL, Thomas et al. SOA with REST: Principles, Patterns & Constraints. Prentice Hall, 2017.",
        "PUREWAL, Semmy. Aprendendo a Desenvolver Aplicações Web. Novatec, 2014.",
    ],
    "deploy": [],
}


def autores_meta():
    """Nomes de todos os autores, para o <meta name="author">."""
    return "; ".join(a["nome"] for a in AUTORES)


def revisores(trilha_id, num):
    """Quem revisou uma aula específica (crédito no rodapé da página)."""
    return REVISORES.get(f"{trilha_id}/{num}", [])


def trilha(id_):
    return TRILHAS[id_]


def aulas(id_):
    return TRILHAS[id_]["aulas"]


def aula(id_, num):
    return next(a for a in aulas(id_) if a["num"] == num)


def caminho_fonte(a):
    """Caminho do arquivo Markdown de uma aula."""
    return FONTES / a["trilha"] / a["arquivo"]
