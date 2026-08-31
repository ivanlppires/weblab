# Aula 03 — Revisão de HTML: layout, links e formulários

> **Nível 2 — Desenvolvimento Web** · Unidade 1: Web estática
> WebLab · UNEMAT — Campus Sinop
> **Tempo estimado:** 3 blocos de 50 min + 1 h de prática

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Escolher a tag correta para cada trecho de conteúdo e justificar a escolha pelos três benefícios da semântica: acessibilidade, indexação e manutenção.
- Montar o esqueleto de uma página com os **landmarks** `header`, `nav`, `main`, `section`, `article`, `aside` e `footer`, e explicar o que cada um significa para um leitor de tela.
- Estruturar conteúdo com listas (`ul`, `ol`, `dl`), imagens com `alt` descritivo, `figure`/`figcaption` e tabelas de dados com `caption`, `thead`, `tbody` e `th scope`.
- Usar links em todas as suas formas — página interna, âncora, URL absoluta, `mailto:`, `tel:`, `download` — e escrever textos de link que fazem sentido fora do contexto.
- Construir um formulário completo com os tipos de campo do HTML5, `label` para cada controle, agrupamento com `fieldset`/`legend` e validação nativa (`required`, `pattern`, `minlength`, `min`/`max`).
- Explicar por que a validação do navegador **nunca** substitui a validação no servidor, e onde cada camada entra no Café Cerrado.
- Validar o HTML no W3C e corrigir os erros mais comuns lendo a mensagem do validador.

## 📋 Pré-requisitos

- [ ] Repositório `cafe-cerrado` clonado na máquina, com `index.html`, `README.md`, e as pastas `css/`, `js/` e `img/` criadas na Aula 02.
- [ ] `css/estilo.css` já ligado ao `index.html` por `<link rel="stylesheet" href="css/estilo.css">`.
- [ ] GitHub Pages ativo no repositório (Aula 01) e o endereço público anotado no `README.md`.
- [ ] VS Code com a extensão **Live Server** e um navegador com DevTools (Chrome ou Firefox).
- [ ] Git configurado com o seu nome e e-mail (`git config --global user.name`, `git config --global user.email`).

> Na aula passada você viu o caminho completo de uma requisição — do `Enter` na barra de endereços até o *paint* na tela — escreveu a anatomia mínima de um documento HTML5 válido e organizou o repositório do Café Cerrado em `css/`, `js/` e `img/`. O `index.html` funciona, mas ainda é um esqueleto de uma página só. Hoje ele vira um site: três páginas ligadas entre si, com estrutura semântica de verdade, um cardápio com listas e tabela e um formulário de contato que o navegador valida sozinho.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Semântica e landmarks; hierarquia de títulos; listas, imagens, `figure` e tabelas de dados; inspeção da árvore de acessibilidade no DevTools |
| 2 | 50 min | Links em todas as formas; caminhos relativos; formulários: anatomia, `label`, tipos de campo, `fieldset` |
| 3 | 50 min | Validação nativa e as três camadas; Mão na massa: `index.html`, `cardapio.html` e `contato.html` do Café Cerrado; validação no W3C; laboratório |

## 1. Semântica: a tag certa não é detalhe

### 1.1 O problema que a `div` não resolve

Considere dois trechos que produzem **exatamente** a mesma imagem na tela:

```html
<div class="topo">
  <div class="titulo">Café Cerrado</div>
  <div class="menu">
    <div><a href="index.html">Início</a></div>
    <div><a href="cardapio.html">Cardápio</a></div>
  </div>
</div>
```

```html
<header>
  <h1>Café Cerrado</h1>
  <nav>
    <ul>
      <li><a href="index.html">Início</a></li>
      <li><a href="cardapio.html">Cardápio</a></li>
    </ul>
  </nav>
</header>
```

Para quem enxerga a página com CSS aplicado, os dois são idênticos. Para todo o resto do mundo, não: o primeiro é uma pilha de caixas anônimas; o segundo declara "isto é o cabeçalho", "isto é o título principal", "isto é a navegação", "isto é uma lista de dois itens".

**Semântica é significado.** Uma `<div>` não diz nada sobre o seu conteúdo — o nome vem de *division*, divisão. Um `<nav>` diz: este bloco é a navegação do site. Essa diferença rende três benefícios concretos:

1. **Acessibilidade.** Leitores de tela constroem, a partir do HTML, uma lista de regiões da página. Quem usa NVDA, VoiceOver ou TalkBack pressiona uma tecla e pula direto para a navegação, ou direto para o conteúdo principal. Com `div`, essa lista sai vazia e a pessoa precisa percorrer a página inteira, elemento por elemento.
2. **Indexação.** Buscadores usam a estrutura para decidir o que é conteúdo e o que é enfeite. Um `<h1>` dentro de `<main>` pesa mais do que um texto grande dentro de um `<div>` do rodapé.
3. **Manutenção.** O código se autodocumenta. Você abre um arquivo de 400 linhas escrito há seis meses e encontra o rodapé procurando por `<footer>` — não por `class="bottom-area-2"`.

> **🧠 Você sabia?**
> As tags semânticas do HTML5 não foram inventadas no vácuo. Em 2005 o Google analisou mais de um bilhão de páginas para descobrir quais nomes de classe as pessoas mais usavam em `<div>`. O ranking foi dominado por `footer`, `menu`, `nav`, `header`, `content`, `main` e `sidebar` — exatamente os nomes que viraram tags no HTML5. Em outras palavras: a especificação não impôs uma estrutura, ela **oficializou a estrutura que a comunidade já usava na mão**. Quando você escreve `<footer>` hoje, está usando um padrão que nasceu de um levantamento estatístico do que os desenvolvedores já faziam.

### 1.2 O inventário de tags estruturais

| Tag | Papel na página |
|---|---|
| `<header>` | Cabeçalho da página **ou de uma seção**: logo, título, navegação. Pode haver vários. |
| `<nav>` | Bloco de links de navegação (menu principal, rodapé, trilha de navegação). |
| `<main>` | Conteúdo principal — **único e não repetido** entre páginas. Um por documento. |
| `<section>` | Seção temática do conteúdo, com título próprio (`h2`/`h3`). |
| `<article>` | Conteúdo independente e autocontido: um post, uma notícia, um card de produto. |
| `<aside>` | Conteúdo complementar: barra lateral, box de curiosidade, links relacionados. |
| `<footer>` | Rodapé da página ou de uma seção: créditos, contato, links institucionais. |
| `<div>` / `<span>` | Contêineres **sem significado**. Só quando nenhuma tag semântica couber. |

Três dúvidas aparecem sempre:

**`section` ou `article`?** O teste: o conteúdo faria sentido sozinho, publicado fora desta página (num feed RSS, num resultado de busca, num aplicativo agregador)? Se sim, é `article`. Um card de produto do cardápio é um `article`; a seção "Nossa história" da página inicial é uma `section`. Na dúvida entre os dois, prefira `section` — ela é o contêiner temático genérico.

**`section` ou `div`?** Toda `section` deveria ter um título (`h2`, `h3`) que a nomeia. Se você não consegue escrever um título para o bloco, provavelmente ele não é uma seção temática: é um agrupamento visual, e aí `div` é a tag honesta.

**`header` só um por página?** Não. `<header>` é o cabeçalho de qualquer coisa: da página, de um `<article>`, de uma `<section>`. O que é único por página é o `<main>`.

### 1.3 Landmarks: o mapa que o leitor de tela enxerga

Cinco tags viram automaticamente **landmarks** (marcos) na árvore de acessibilidade:

| Tag HTML | Landmark anunciado |
|---|---|
| `<header>` (filho direto do `body`) | `banner` |
| `<nav>` | `navigation` |
| `<main>` | `main` |
| `<aside>` | `complementary` |
| `<footer>` (filho direto do `body`) | `contentinfo` |

Repare no detalhe entre parênteses: `<header>` e `<footer>` só viram landmarks quando são filhos diretos do `<body>`. Um `<header>` dentro de um `<article>` é apenas o cabeçalho daquele artigo — o que é correto e desejado.

Quando a página tem **mais de uma** navegação, cada `<nav>` precisa de um rótulo, senão o usuário ouve "navegação", "navegação", "navegação" e não sabe qual é qual:

```html
<nav aria-label="Principal">
  <ul>
    <li><a href="index.html">Início</a></li>
    <li><a href="cardapio.html">Cardápio</a></li>
  </ul>
</nav>

<nav aria-label="Rodapé">
  <ul>
    <li><a href="#politica">Política de privacidade</a></li>
  </ul>
</nav>
```

O `aria-label` é um dos poucos atributos ARIA que você vai usar hoje. A aula de **Acessibilidade e ARIA** aprofunda o assunto; por enquanto, guarde a regra: **rotule toda navegação quando houver mais de uma**.

> **🔬 Investigue**
> Abra qualquer site grande (um portal de notícias, o site da UNEMAT) e pressione <kbd>F12</kbd>. No Chrome, vá em **Elements** e, no painel da direita, abra a aba **Accessibility**; no Firefox, use a aba **Acessibilidade** e ative "Mostrar tabulações". Procure a árvore de acessibilidade e conte quantos landmarks a página tem. Depois abra o seu `index.html` do Café Cerrado e faça a mesma contagem. Anote a diferença — no fim desta aula, refaça o teste na sua página e compare com o número de agora.

### 1.4 Hierarquia de títulos: estrutura, não tamanho

`<h1>` a `<h6>` formam o **sumário** da página, como os capítulos e seções de um livro. Regras:

- Um único `<h1>` por página, dizendo do que a página trata.
- `<h2>` para as seções principais, `<h3>` para subseções — **sem pular níveis** (nunca `h2` direto para `h4`).
- Tamanho de fonte é problema do CSS. Se um `<h2>` está grande demais, mude o CSS; não troque para `<h4>`.

Um `<h1>` mal escolhido custa caro: leitores de tela oferecem "listar todos os títulos" como forma rápida de entender a página. Se a lista sai como `h1: Café Cerrado`, `h3: Cafés`, `h5: Espresso`, o usuário conclui que faltam níveis — e não faltam, é só desleixo.

**Sumário correto de `cardapio.html`:**

```text
h1  Cardápio
├── h2  Cafés
│   ├── h3  Espresso do Cerrado
│   ├── h3  Coado da Casa
│   └── h3  Cappuccino Sinop
├── h2  Bebidas geladas
│   ├── h3  Cold Brew da Chapada
│   └── h3  Frappê de Café
├── h2  Salgados
└── h2  Doces
```

> **📌 Vale gravar**
> Duas confusões comuns: (a) "pode haver mais de um `<h1>` por página" — na prática deste material, **não**: um por página; (b) "`<h1>` é o texto maior da página" — falso, `h1` é o título mais importante, e o tamanho é decisão do CSS.

### 1.5 Quando `div` e `span` ainda são a resposta certa

Semântica não é uma corrida para eliminar `div`. Ela continua sendo a ferramenta correta quando o agrupamento existe **só para o layout**: um contêiner que centraliza o conteúdo, uma linha do grid, um invólucro para aplicar um fundo. O mesmo vale para `<span>`, o contêiner genérico em linha.

```html
<footer>
  <div class="container">
    <p>Café Cerrado — Avenida dos Jacarandás, 1200, Sinop, MT</p>
    <p>Preço a partir de <span class="destaque">R$ 6,00</span></p>
  </div>
</footer>
```

Aqui `div.container` existe para o CSS limitar a largura e centralizar; `span.destaque` existe para colorir um pedaço de texto. Nenhum dos dois carrega significado — e está certo assim. O erro é o inverso: usar `div` onde existe uma tag com significado.

## 2. Conteúdo: listas, imagens e tabelas

### 2.1 Listas: três tipos, três significados

```html
<!-- Lista não ordenada: a ordem não importa -->
<ul>
  <li>Wi-Fi liberado</li>
  <li>Tomadas em todas as mesas</li>
  <li>Espaço para estudo</li>
</ul>

<!-- Lista ordenada: a ordem importa -->
<ol>
  <li>Escolha os grãos no balcão</li>
  <li>Peça a moagem na hora</li>
  <li>Retire o café no guichê</li>
</ol>

<!-- Lista de definições: pares termo/descrição -->
<dl>
  <dt>Torra clara</dt>
  <dd>Realça a acidez e as notas frutadas do grão.</dd>
  <dt>Torra média</dt>
  <dd>Equilibra doçura, corpo e acidez. É a nossa torra padrão.</dd>
  <dt>Torra escura</dt>
  <dd>Mais amarga e encorpada, com notas de chocolate amargo.</dd>
</dl>
```

A `<dl>` (*description list*) é subutilizada e resolve muito bem glossários, especificações e — no nosso caso — a descrição das torras. Cada `<dt>` é um termo; cada `<dd>`, a descrição correspondente. Um `<dt>` pode ter vários `<dd>` e vice-versa.

Listas também são a base semântica de menus: um menu é uma lista de links. O leitor de tela anuncia "lista com 4 itens" ao entrar no `<nav>` — o usuário sabe o tamanho da navegação antes de percorrê-la.

### 2.2 Imagens: `alt` é obrigatório, e não é opcional

```html
<img src="img/fachada.jpg"
     alt="Fachada do Café Cerrado com toldo verde e mesas na calçada"
     width="1200" height="800">
```

Quatro atributos que valem nota:

- **`src`** — o caminho do arquivo, relativo à página (seção 3.1).
- **`alt`** — o texto alternativo. Descreve a imagem para quem não a vê: leitores de tela, buscadores e o próprio navegador quando o arquivo falha. É **obrigatório**.
- **`width`/`height`** — as dimensões reais do arquivo, em pixels e **sem unidade**. Não servem para redimensionar (isso é papel do CSS): servem para o navegador reservar o espaço antes de a imagem carregar, evitando que o texto "pule" na tela.
- **`loading="lazy"`** — opcional; adia o download de imagens que estão fora da tela. Use em galerias longas, nunca na imagem principal do topo.

**Como escrever um bom `alt`:** descreva o que a imagem comunica naquele contexto, em uma frase, sem começar com "imagem de" (o leitor de tela já anuncia que é uma imagem).

| Situação | `alt` correto |
|---|---|
| Foto de produto no cardápio | `alt="Xícara de espresso com creme dourado sobre pires branco"` |
| Logo dentro de um link para a home | `alt="Café Cerrado — página inicial"` |
| Gráfico com dados | `alt="Gráfico de barras: vendas de café coado sobem de 120 para 310 xícaras por semana"` |
| Imagem puramente decorativa | `alt=""` — vazio, **mas presente** |

O `alt=""` merece explicação: um `alt` vazio diz ao leitor de tela "ignore esta imagem, ela não acrescenta informação". Já **omitir** o atributo faz o leitor anunciar o nome do arquivo — e ouvir "i-m-g-underline-2-0-2-4-underline-final-ponto-jpg" é pior do que ouvir nada.

> **⚠️ Atenção**
> Se a imagem está dentro de um link e é o **único** conteúdo dele, o `alt` deixa de descrever a imagem e passa a descrever **o destino do link**. Um logo clicável tem `alt="Café Cerrado — página inicial"`, não `alt="Logo"`. Quem navega por leitor de tela ouve o `alt` como se fosse o texto do link.

### 2.3 `figure` e `figcaption`: imagem com legenda

```html
<figure>
  <img src="img/grao-cerrado.jpg"
       alt="Grãos de café verdes sendo peneirados em uma bandeja de metal"
       width="1000" height="667">
  <figcaption>
    Grãos do Cerrado mato-grossense recém-beneficiados, antes da torra.
  </figcaption>
</figure>
```

`<figure>` agrupa um conteúdo autocontido (imagem, trecho de código, tabela, vídeo) com sua legenda, e o `<figcaption>` é a legenda — que deve ser o **primeiro ou o último** filho da `<figure>`.

A diferença entre `alt` e `figcaption` confunde: o `alt` **descreve** a imagem para quem não a vê; o `figcaption` **comenta** a imagem para todo mundo. Eles não devem repetir um ao outro. No exemplo acima, o `alt` diz o que aparece na foto; a legenda diz de onde vieram os grãos.

### 2.4 Tabelas de dados — nunca para layout

Tabela serve para **dados tabulares**: informação que faz sentido em linhas e colunas. Layout é problema de CSS (Flexbox e Grid, que você estudou no Nível 1). Uma tabela usada para layout destrói a leitura em leitor de tela, que anuncia "linha 3, coluna 2" para cada pedaço da página.

```html
<table>
  <caption>Horário de atendimento do Café Cerrado</caption>
  <thead>
    <tr>
      <th scope="col">Dia</th>
      <th scope="col">Abertura</th>
      <th scope="col">Fechamento</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Segunda a sexta</th>
      <td>07h00</td>
      <td>20h00</td>
    </tr>
    <tr>
      <th scope="row">Sábado</th>
      <td>08h00</td>
      <td>18h00</td>
    </tr>
    <tr>
      <th scope="row">Domingo</th>
      <td colspan="2">Fechado</td>
    </tr>
  </tbody>
</table>
```

Os elementos que fazem a tabela ser acessível:

- **`<caption>`** — o título da tabela, primeiro filho de `<table>`. Anunciado pelo leitor de tela ao entrar na tabela.
- **`<thead>` / `<tbody>` / `<tfoot>`** — separam cabeçalho, corpo e rodapé. Permitem que o navegador repita o cabeçalho ao imprimir e que o CSS fixe o cabeçalho ao rolar.
- **`<th>` com `scope`** — `scope="col"` diz "sou o cabeçalho desta coluna"; `scope="row"`, "sou o cabeçalho desta linha". É isso que faz o leitor de tela anunciar "Sábado, Abertura: 08h00" em vez de só "08h00".
- **`colspan` / `rowspan`** — mesclagem de células. Use com parcimônia: tabelas muito mescladas ficam impossíveis de navegar.

> **💡 Dica**
> Tabelas largas estouram a tela do celular. A solução de uma linha: envolva a `<table>` em uma `<div class="tabela-rolavel">` com `overflow-x: auto` no CSS. A tabela rola sozinha no eixo horizontal em vez de esticar a página inteira. Você vai usar exatamente isso no `cardapio.html`.

## 3. Links: a essência do hipertexto

### 3.1 Caminhos relativos e absolutos

Antes das formas de link, o assunto que mais gera erro 404 em trabalho de aluno: **como escrever o caminho**.

| Escrita | Significa |
|---|---|
| `cardapio.html` | Arquivo na **mesma pasta** da página atual |
| `img/fachada.jpg` | Arquivo na subpasta `img/`, a partir da pasta atual |
| `../index.html` | Sobe **uma** pasta e procura ali |
| `/cafe-cerrado/index.html` | A partir da **raiz do domínio** (cuidado no GitHub Pages) |

A armadilha clássica: caminhos que começam com `/` são absolutos **em relação ao domínio**, não ao seu projeto. Se você escreve `/img/logo.svg` e publica em `https://seuusuario.github.io/cafe-cerrado/`, o navegador procura em `https://seuusuario.github.io/img/logo.svg` — que não existe. Funciona no Live Server (onde o projeto é a raiz) e quebra no GitHub Pages. **Regra do curso: use sempre caminhos relativos** (`img/logo.svg`, `css/estilo.css`), sem a barra inicial.

Outra armadilha: **Linux e macOS diferenciam maiúsculas de minúsculas; Windows não.** `img/Fachada.JPG` funciona na sua máquina e quebra no GitHub Pages, que roda em Linux. Padronize: nomes de arquivo em minúsculas, sem espaços e sem acentos, com hífen no lugar do espaço (`pao-de-queijo.jpg`).

### 3.2 As sete formas de link

```html
<!-- 1. Outra página do site (caminho relativo) -->
<a href="cardapio.html">Ver o cardápio completo</a>

<!-- 2. Âncora interna: rola até o elemento com esse id -->
<a href="#horarios">Horários de atendimento</a>

<!-- 3. Âncora em outra página -->
<a href="cardapio.html#doces">Doces do dia</a>

<!-- 4. Site externo (URL absoluta) -->
<a href="https://www.unemat.br">UNEMAT</a>

<!-- 5. Abrir em nova aba -->
<a href="https://www.unemat.br" target="_blank" rel="noopener">
  UNEMAT (abre em nova aba)
</a>

<!-- 6. E-mail e telefone -->
<a href="mailto:contato@cafecerrado.exemplo.br">contato@cafecerrado.exemplo.br</a>
<a href="tel:+556699999000">(66) 9 9999-9000</a>

<!-- 7. Download de arquivo -->
<a href="docs/cardapio.pdf" download>Baixar o cardápio em PDF</a>
```

Detalhes que importam:

- **`mailto:`** aceita assunto e corpo pré-preenchidos: `mailto:contato@cafecerrado.exemplo.br?subject=Reserva%20de%20mesa`. O `%20` é o espaço codificado para URL.
- **`tel:`** deve trazer o número em formato internacional, sem espaços nem parênteses: `tel:+556699999000`. No celular, o link abre o discador; no desktop, costuma abrir o aplicativo de chamadas configurado.
- **`download`** sugere ao navegador baixar em vez de abrir. Com valor (`download="cardapio-cafe-cerrado.pdf"`), define o nome do arquivo salvo. Só funciona para arquivos do **mesmo domínio**.

### 3.3 `target="_blank"` e por que o `rel` é obrigatório

Abrir link em nova aba parece inofensivo, mas tem duas consequências:

**Segurança.** A página aberta recebe uma referência à página que a abriu (`window.opener`) e pode reescrever o endereço da aba original — técnica conhecida como *tabnabbing*. O `rel="noopener"` corta essa referência. Navegadores modernos já aplicam `noopener` por padrão em `target="_blank"`, mas escrever explicitamente é a prática correta: o seu HTML não deveria depender do comportamento padrão de uma versão específica de navegador.

**Acessibilidade.** Abrir uma aba nova sem avisar quebra o botão "voltar", que é a forma como muita gente navega. Sinalize no texto do link, no `title` ou com um ícone que tenha texto alternativo.

```html
<a href="https://developer.mozilla.org/pt-BR/" target="_blank" rel="noopener">
  MDN Web Docs (abre em nova aba)
</a>
```

> **🔎 Por baixo do capô**
> `rel="noreferrer"` faz mais do que `noopener`: além de cortar o `window.opener`, ele impede que o navegador envie o cabeçalho HTTP `Referer` — o campo que informa ao site de destino de onde o visitante veio. Isso protege a privacidade, mas apaga a sua origem das estatísticas do site linkado. Para links externos comuns, `noopener` basta. Se a página tiver informação sensível na URL (um identificador de sessão, por exemplo), use `noopener noreferrer`.

### 3.4 Âncoras internas e o `id`

Uma âncora é um link para um `id` da própria página:

```html
<nav aria-label="Nesta página">
  <ul>
    <li><a href="#cafes">Cafés</a></li>
    <li><a href="#geladas">Bebidas geladas</a></li>
    <li><a href="#salgados">Salgados</a></li>
  </ul>
</nav>

<section id="cafes">
  <h2>Cafés</h2>
</section>
```

Regras do `id`: **único no documento inteiro**, sem espaços, começando por letra. Um `id` duplicado é erro no validador do W3C e faz o navegador rolar sempre para a primeira ocorrência.

Duas melhorias de uma linha cada:

```css
html {
  scroll-behavior: smooth;   /* rolagem suave até a âncora */
  scroll-padding-top: 5rem;  /* compensa a altura do cabeçalho fixo */
}
```

Sem `scroll-padding-top`, a âncora leva o título exatamente para o topo da janela — e o cabeçalho fixo cobre o título. Esse é um dos bugs mais frequentes e mais fáceis de corrigir.

### 3.5 O texto do link, `aria-current` e o estado da página atual

Leitores de tela oferecem "listar todos os links da página". Nessa lista, cada link aparece **sozinho**, fora do contexto do parágrafo. Uma página com dez "clique aqui" produz uma lista inútil.

| Ruim | Bom |
|---|---|
| `Para ver o cardápio, <a href="cardapio.html">clique aqui</a>.` | `Veja o <a href="cardapio.html">cardápio completo</a>.` |
| `<a href="docs/menu.pdf">Leia mais</a>` | `<a href="docs/menu.pdf" download>Baixar o cardápio em PDF</a>` |
| `<a href="https://unemat.br">https://unemat.br</a>` | `<a href="https://unemat.br">Portal da UNEMAT</a>` |

E, no menu, marque a página atual **semanticamente**:

```html
<nav aria-label="Principal">
  <ul>
    <li><a href="index.html">Início</a></li>
    <li><a href="cardapio.html" aria-current="page">Cardápio</a></li>
    <li><a href="contato.html">Contato</a></li>
  </ul>
</nav>
```

O atributo `aria-current="page"` faz o leitor de tela anunciar "Cardápio, página atual". Quem enxerga recebe a mesma informação por cor — e a cor sozinha nunca basta, porque cerca de 8% dos homens têm alguma forma de daltonismo. Bônus: o CSS pode usar o próprio atributo como seletor (`nav a[aria-current="page"]`), então o destaque visual sai de graça, sem classe extra.

## 4. Formulários: a porta de entrada de dados

Formulário é onde o site deixa de ser um panfleto. Toda a Unidade 3 desta disciplina vive de dados que chegam por formulários: na Unidade 2 você vai validá-los com JavaScript e, na Unidade 3, recebê-los no Express. Estruturar o formulário direito agora é investimento nos três marcos do projeto.

### 4.1 Anatomia do `<form>`

```html
<form action="contato.html" method="post">
  <label for="nome">Nome completo</label>
  <input type="text" id="nome" name="nome" required>

  <button type="submit">Enviar</button>
</form>
```

- **`action`** — para onde os dados vão. Em um site estático ainda não há servidor para recebê-los; na Unidade 3, isso vira `/api/contatos`.
- **`method`** — `get` coloca os dados na URL (`?nome=Ana&assunto=reserva`), o que serve para buscas e páginas compartilháveis; `post` envia no corpo da requisição, o que serve para cadastros, senhas e qualquer coisa que não deva ficar no histórico do navegador.
- **`name`** — o nome do dado enviado. **Sem `name`, o campo simplesmente não é enviado.** É o erro silencioso número um de formulário: tudo parece certo, e o servidor recebe menos campos do que a tela mostra.
- **`id`** — identifica o elemento no documento, para o `<label>` e para o JavaScript. `id` e `name` costumam ter o mesmo valor, mas são coisas diferentes: `id` é para o navegador, `name` é para o servidor.

> **📌 Vale gravar**
> A diferença entre `id` e `name` em campos de formulário é pergunta recorrente. Resposta curta: `id` é único no documento e serve para `label for`, CSS e JavaScript; `name` é a chave com que o dado viaja para o servidor, pode se repetir (é assim que um grupo de `radio` funciona) e, se faltar, o campo não é enviado.

### 4.2 `<label>`: um para cada campo, sem exceção

```html
<!-- Forma 1: label com for apontando para o id do campo -->
<label for="email">E-mail</label>
<input type="email" id="email" name="email">

<!-- Forma 2: label envolvendo o campo (dispensa for/id) -->
<label>
  E-mail
  <input type="email" name="email">
</label>
```

O `<label>` faz três coisas ao mesmo tempo:

1. O leitor de tela anuncia o rótulo quando o campo recebe foco. Sem ele, a pessoa ouve apenas "caixa de edição" e não sabe o que digitar.
2. Clicar no rótulo foca o campo — e, em `checkbox`/`radio`, marca a opção. Isso multiplica a área clicável, o que é decisivo no celular.
3. O rótulo permanece visível enquanto a pessoa digita, ao contrário do `placeholder`.

> **⚠️ Atenção**
> `placeholder` **não é rótulo**. Ele desaparece assim que a pessoa digita a primeira letra, tem contraste baixo por padrão (falhando nos critérios de acessibilidade) e alguns leitores de tela o ignoram. Use `placeholder` só para mostrar o **formato** esperado — `placeholder="78550-000"` ao lado do rótulo "CEP" — nunca no lugar do `<label>`.

### 4.3 Os tipos de campo do HTML5

| `type` | Comportamento |
|---|---|
| `text` | Texto livre de uma linha. O padrão. |
| `password` | Oculta os caracteres digitados. |
| `email` | Valida o formato e abre teclado com `@` no celular. |
| `tel` | Abre teclado numérico. **Não valida sozinho** — use `pattern`. |
| `url` | Exige um endereço completo, com `https://`. |
| `number` | Numérico com `min`, `max` e `step`; setas de incremento. |
| `range` | Controle deslizante entre `min` e `max`. |
| `date` / `time` | Seletores nativos de data e de hora. |
| `checkbox` | Escolha múltipla, independente. |
| `radio` | Escolha única dentro do grupo definido pelo mesmo `name`. |
| `file` | Envio de arquivo; `accept` filtra os tipos. |
| `search` | Campo de busca; alguns navegadores mostram um "x" para limpar. |
| `color` | Seletor de cor; devolve o valor no formato `#rrggbb`. |
| `hidden` | Valor enviado sem aparecer na tela. |

Exemplos completos dos que você vai usar hoje:

```html
<label for="pessoas">Quantas pessoas</label>
<input type="number" id="pessoas" name="pessoas" min="1" max="40" step="1" value="2">

<label for="data">Data desejada</label>
<input type="date" id="data" name="data">

<label for="horario">Horário</label>
<input type="time" id="horario" name="horario" min="07:00" max="20:00" step="900">

<label for="foto">Foto do evento (opcional)</label>
<input type="file" id="foto" name="foto" accept="image/png, image/jpeg">
```

O `step="900"` no campo de hora significa 900 segundos, ou seja, intervalos de 15 minutos.

> **🧠 Você sabia?**
> `type="tel"` **não valida nada**. Ele existe apenas para dizer ao celular "abra o teclado numérico". A razão é cultural: formatos de telefone variam demais entre países (o Brasil tem números de 10 e de 11 dígitos, com e sem o nono dígito), e a especificação decidiu que qualquer regra embutida excluiria alguém. `type="email"`, por outro lado, valida — e valida de forma bem mais permissiva do que a maioria imagina: `a@b` passa, porque endereços de intranet sem ponto no domínio são válidos segundo a especificação. Se você precisa de uma regra mais estrita, ela é sua, via `pattern` — e depois no servidor.

### 4.4 Agrupando: `fieldset`, `legend`, `select`, `textarea`

```html
<fieldset>
  <legend>Como prefere ser respondido?</legend>

  <label>
    <input type="radio" name="canal" value="email" checked>
    E-mail
  </label>

  <label>
    <input type="radio" name="canal" value="telefone">
    Telefone
  </label>

  <label>
    <input type="radio" name="canal" value="whatsapp">
    WhatsApp
  </label>
</fieldset>
```

`<fieldset>` agrupa campos relacionados e `<legend>` dá o título do grupo — que o leitor de tela anuncia junto com cada opção ("Como prefere ser respondido? E-mail, botão de opção 1 de 3"). Para grupos de `radio` e `checkbox`, o par `fieldset`/`legend` **não é decoração: é o que dá sentido às opções**.

Os três `radio` compartilham o mesmo `name="canal"` — é isso que os torna mutuamente exclusivos — e cada um tem um `value` diferente, que é o dado que chega ao servidor.

```html
<label for="assunto">Assunto</label>
<select id="assunto" name="assunto" required>
  <option value="">Selecione um assunto</option>
  <optgroup label="Atendimento">
    <option value="reserva">Reserva de mesa</option>
    <option value="encomenda">Encomenda de bolos e tortas</option>
  </optgroup>
  <optgroup label="Institucional">
    <option value="evento">Evento ou parceria</option>
    <option value="trabalhe">Trabalhe conosco</option>
  </optgroup>
</select>

<label for="mensagem">Mensagem</label>
<textarea id="mensagem" name="mensagem" rows="5" maxlength="500"
          placeholder="Conte o que você precisa"></textarea>
```

Dois detalhes do `<select>`:

- A primeira `<option>` tem `value=""`. Isso é o que faz o `required` funcionar: sem uma opção de valor vazio, o primeiro item já vem selecionado e a validação nunca reclama.
- `<optgroup>` agrupa opções sob um rótulo não selecionável. Em listas longas (estados, categorias), organiza muito.

O `<textarea>` não tem atributo `value`: o conteúdo inicial vai **entre** as tags. E cuidado — qualquer espaço ou quebra de linha entre `<textarea>` e `</textarea>` vira conteúdo do campo. Por isso escrevemos as duas tags coladas.

### 4.5 Validação nativa: o navegador trabalhando por você

O navegador valida antes de enviar, sem uma linha de JavaScript:

| Atributo | O que exige |
|---|---|
| `required` | Campo preenchido (ou, em `checkbox`, marcado) |
| `minlength` / `maxlength` | Número mínimo/máximo de caracteres |
| `min` / `max` | Valor mínimo/máximo em `number`, `date`, `time`, `range` |
| `step` | Incremento válido em `number`, `date`, `time` |
| `pattern` | Expressão regular que o valor precisa casar |
| `type` | `email` e `url` já trazem regra de formato embutida |

```html
<label for="cep">CEP</label>
<input type="text" id="cep" name="cep"
       required
       pattern="[0-9]{5}-?[0-9]{3}"
       placeholder="78550-000"
       title="Digite um CEP no formato 78550-000"
       inputmode="numeric"
       autocomplete="postal-code">
```

Quatro observações sobre esse bloco:

- O `pattern` casa o valor **inteiro** — não precisa de `^` nem `$`, eles são implícitos. `[0-9]{5}-?[0-9]{3}` aceita `78550000` e `78550-000`.
- O `title` vira a mensagem de erro exibida pelo navegador quando o `pattern` falha. Sem `title`, a pessoa lê apenas "Corresponda ao formato solicitado", que não ajuda ninguém.
- `inputmode="numeric"` abre o teclado numérico no celular **sem** mudar o `type` — o que seria errado aqui, porque `type="number"` remove zeros à esquerda e mostra setas de incremento.
- `autocomplete="postal-code"` deixa o navegador preencher o campo com o CEP já salvo pelo usuário.

O CSS reage aos estados de validação com pseudoclasses:

```css
input:invalid,
select:invalid {
  border-color: #b42318;
}

input:user-invalid {
  outline: 2px solid #b42318;   /* só depois que a pessoa interagiu com o campo */
}

input:valid {
  border-color: #1a7f37;
}

input:required + .marca-obrigatorio::after {
  content: " *";
  color: #b42318;
}
```

`:invalid` casa desde o carregamento da página — todo campo `required` vazio já nasce inválido, e pintar tudo de vermelho antes de a pessoa digitar é hostil. `:user-invalid` resolve isso: só casa depois que a pessoa interagiu com o campo e saiu dele. Prefira `:user-invalid` sempre que puder.

> **🔬 Investigue**
> Crie um arquivo `teste-validacao.html` com um único campo: `<form><input type="email" required><button>Enviar</button></form>`. Abra no navegador e clique em Enviar com o campo vazio — anote a mensagem exata que aparece. Agora digite `ana@` e envie: outra mensagem. Digite `a@b`: passa, e é isso mesmo (seção 4.3). Por fim, abra o console (<kbd>F12</kbd> → Console) e execute `document.querySelector('input').validity` — o navegador devolve um objeto `ValidityState` com um campo booleano para cada tipo de erro (`valueMissing`, `typeMismatch`, `patternMismatch`, `tooShort`). Esse objeto é exatamente o que você vai usar para escrever mensagens de erro personalizadas na Unidade 2.

Para **testar** o formulário sem que o navegador atrapalhe, existe o `novalidate`:

```html
<form action="contato.html" method="post" novalidate>
</form>
```

Ele desliga a validação nativa do formulário inteiro. Use durante o desenvolvimento e para assumir o controle das mensagens com JavaScript — jamais como forma de "resolver" um campo que insiste em não validar.

### 4.6 As três camadas de validação

Este é o conceito mais importante da seção, e o que separa quem entende de segurança de quem não entende:

| Camada | Onde roda | Serve para |
|---|---|---|
| Validação nativa (HTML) | Navegador | Feedback imediato, teclado certo no celular |
| Validação com JavaScript | Navegador | Mensagens personalizadas, regras de negócio, máscaras |
| Validação no servidor | Servidor | **A única em que se pode confiar** |

As duas primeiras rodam **na máquina do usuário**, e tudo que roda na máquina do usuário pode ser burlado: basta abrir o DevTools e remover o atributo `required`, ou enviar a requisição direto por `curl` sem passar pela página. A validação do cliente existe para melhorar a experiência de quem está agindo de boa-fé; a validação do servidor existe para proteger o sistema de quem não está.

Você vai ver isso literalmente acontecer: na Unidade 3, ao construir a API do Café Cerrado, o primeiro teste será enviar um `POST /api/produtos` com o corpo vazio, sem passar por formulário nenhum.

> **⚠️ Atenção**
> Nunca confie em dados vindos do cliente. Nem no `hidden`, nem no `select` (o usuário pode trocar o `value` de uma `<option>` no DevTools), nem no `maxlength`. A regra vale para o resto da sua vida profissional.

## 5. Validando o HTML: o W3C como corretor automático

O validador oficial (<https://validator.w3.org/nu/>) lê o seu HTML e aponta erros de sintaxe, aninhamento inválido, atributos inexistentes e `id` duplicado. É gratuito, roda no navegador e aceita três entradas: URL pública, upload de arquivo ou texto colado.

Fluxo recomendado no Café Cerrado:

1. Escreva a página.
2. Cole o conteúdo em "Validate by direct input" (o site ainda não está publicado com as mudanças).
3. Corrija do primeiro erro para o último — erros de aninhamento costumam gerar cascatas, e resolver o primeiro apaga vários.
4. Só depois faça `commit` e `push`.

Aprenda a **ler** a mensagem. Ela sempre tem três partes: a linha, o que o validador esperava e o que encontrou.

```text
Error: Element "figcaption" not allowed as child of element "div" in this context.
From line 42, column 5; to line 42, column 17
```

Tradução: `figcaption` só pode ser filho de `figure`. Você trocou a `figure` por uma `div` em algum momento.

```text
Error: Duplicate ID "nome".
```

Tradução: dois elementos têm `id="nome"`. Provavelmente você copiou um bloco de campo e esqueceu de trocar o `id` — e, de quebra, o `label for="nome"` agora aponta para o campo errado.

Vale também rodar o **Lighthouse** (DevTools → aba Lighthouse → Accessibility). Ele não substitui o validador, mas encontra outra categoria de problemas: contraste, campos sem rótulo, links sem texto discernível. A aula de Acessibilidade e ARIA vai exigir nota ≥ 90 nesse relatório — começar a olhar para ele agora facilita a vida depois.

## 💻 Mão na massa — Três páginas do Café Cerrado

O Café Cerrado — o projeto-fio apresentado na Aula 01 e iniciado na Aula 02 — sai hoje de uma página só para três páginas ligadas entre si, com estrutura semântica completa.

Ao final você terá:

- `index.html` — hero, sobre, destaques e horários.
- `cardapio.html` — produtos em listas por categoria, tabela de torras e uma `figure`.
- `contato.html` — formulário completo com validação nativa.
- Um menu igual nas três páginas, com `aria-current="page"` no item certo.

> **⚠️ Cuidado**
> O `index.html` de hoje **substitui** o da Aula 02, com nomes de classe novos. Antes de colar o código do Passo 1, abra `css/estilo.css` e **apague as cinco regras da Aula 02 que ficaram sem dono**: `.cabecalho`, `.marca` (a versão antiga, de uma linha só), `.navegacao ul`, `.navegacao a` (e o `:hover`/`:focus` dela), `.destaque`, `.destaque h1`, `.destaque p`, `.sobre`, `.sobre h2`, `.botao` (todas as declarações antigas dela) e `.rodape`/`.rodape p`. Ficam de pé, sem alteração: o bloco `:root`, o reset da §7.2, `body`, `img`, `a` e a regra de `main`. As classes novas — `.topo`, `.topo__interno`, `.hero`, `.cartoes`, `.rodape__grade` — entram no Passo 4. Duas regras com o mesmo nome no mesmo arquivo não dão erro: a última vence em silêncio, e você passa a tarde caçando um estilo que "não aplica".
>
> Se você fez o laboratório B1 da Aula 02 e criou `sobre.html`, mantenha o item **Sobre** no menu das três páginas (um `<li>` a mais, sem `aria-current`) e repita nele o mesmo `<header>`/`<footer>`. O menu de três itens abaixo é o mínimo, não o teto.

### Passo 1 — `index.html` completo

Escreva a página inicial inteira. O `<header>` e o `<footer>` deste arquivo são **idênticos** nas outras duas páginas — só muda em qual item do menu fica o `aria-current="page"`.

**`cafe-cerrado/index.html`**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Café Cerrado: torrefação artesanal de grãos do Cerrado mato-grossense em Sinop, MT. Cafés, bebidas geladas, salgados e doces.">
  <title>Café Cerrado — Torrefação artesanal em Sinop, MT</title>
  <link rel="stylesheet" href="css/estilo.css">
</head>
<body>
  <header class="topo">
    <div class="container topo__interno">
      <a class="marca" href="index.html">
        <span class="marca__nome">Café Cerrado</span>
        <span class="marca__slogan">Torrefação artesanal · Sinop, MT</span>
      </a>

      <nav aria-label="Principal">
        <ul class="menu">
          <li><a href="index.html" aria-current="page">Início</a></li>
          <li><a href="cardapio.html">Cardápio</a></li>
          <li><a href="contato.html">Contato</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <main class="container">
    <section class="hero">
      <div class="hero__texto">
        <h1>Café do Cerrado, torrado em Sinop</h1>
        <p class="hero__chamada">
          Compramos grãos de produtores da região, torramos em pequenos lotes e
          moemos na hora do seu pedido. Sem pressa e sem atalho.
        </p>
        <p>
          <a class="botao" href="cardapio.html">Ver o cardápio completo</a>
          <a class="botao botao--vazado" href="contato.html">Reservar uma mesa</a>
        </p>
      </div>

      <img src="img/fachada.jpg"
           alt="Fachada do Café Cerrado com toldo verde e mesas na calçada"
           width="1200" height="800">
    </section>

    <section id="sobre">
      <h2>Nossa história</h2>
      <p>
        O Café Cerrado nasceu em uma garagem no Setor Comercial de Sinop, com um
        torrador de dois quilos e a teimosia de provar que o café produzido no
        Mato Grosso pode brigar com os grãos mais famosos do país.
      </p>
      <p>
        Hoje trabalhamos com quatro sítios parceiros no cerrado mato-grossense e
        torramos, em média, sessenta quilos por semana — tudo consumido aqui
        mesmo, no balcão ou nas mesas da calçada.
      </p>

      <h3>O que você encontra aqui</h3>
      <ul>
        <li>Wi-Fi liberado e tomada em todas as mesas</li>
        <li>Moagem na hora, com escolha da torra</li>
        <li>Grãos embalados para levar para casa</li>
        <li>Opções sem lactose e sem glúten identificadas no cardápio</li>
      </ul>
    </section>

    <section id="destaques">
      <h2>Destaques da semana</h2>

      <ul class="cartoes">
        <li>
          <article class="cartao">
            <h3>Cold Brew da Chapada</h3>
            <p class="cartao__preco">R$ 15,00</p>
            <p>Extração a frio por dezoito horas, servido com gelo e rodela de laranja.</p>
            <p><a href="cardapio.html#geladas">Ver nas bebidas geladas</a></p>
          </article>
        </li>

        <li>
          <article class="cartao">
            <h3>Pão de Queijo Mineiro</h3>
            <p class="cartao__preco">R$ 7,00</p>
            <p>Massa de polvilho azedo com queijo canastra, assado de hora em hora.</p>
            <p><a href="cardapio.html#salgados">Ver nos salgados</a></p>
          </article>
        </li>

        <li>
          <article class="cartao">
            <h3>Bolo de Milho Verde</h3>
            <p class="cartao__preco">R$ 9,50</p>
            <p>Receita da avó da Dona Marli, com milho comprado na feira do produtor.</p>
            <p><a href="cardapio.html#doces">Ver nos doces</a></p>
          </article>
        </li>
      </ul>
    </section>

    <section id="horarios">
      <h2>Horário de atendimento</h2>

      <div class="tabela-rolavel">
        <table>
          <caption>Horário de atendimento do Café Cerrado</caption>
          <thead>
            <tr>
              <th scope="col">Dia</th>
              <th scope="col">Abertura</th>
              <th scope="col">Fechamento</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <th scope="row">Segunda a sexta</th>
              <td>07h00</td>
              <td>20h00</td>
            </tr>
            <tr>
              <th scope="row">Sábado</th>
              <td>08h00</td>
              <td>18h00</td>
            </tr>
            <tr>
              <th scope="row">Domingo</th>
              <td colspan="2">Fechado</td>
            </tr>
          </tbody>
        </table>
      </div>

      <p>
        Precisa de um horário fora do expediente para um evento?
        <a href="contato.html">Fale com a gente pelo formulário de contato</a>.
      </p>
    </section>
  </main>

  <footer class="rodape">
    <div class="container rodape__grade">
      <section>
        <h2>Café Cerrado</h2>
        <p>Torrefação artesanal de grãos do Cerrado mato-grossense. Projeto fictício
           usado como estudo de caso da disciplina de Desenvolvimento Web.</p>
      </section>

      <section>
        <h2>Onde estamos</h2>
        <address>
          Avenida dos Jacarandás, 1200 — Setor Comercial<br>
          Sinop — MT<br>
          <a href="tel:+556699999000">(66) 9 9999-9000</a><br>
          <a href="mailto:contato@cafecerrado.exemplo.br">contato@cafecerrado.exemplo.br</a>
        </address>
      </section>

      <nav aria-label="Rodapé">
        <h2>Navegação</h2>
        <ul>
          <li><a href="index.html">Início</a></li>
          <li><a href="cardapio.html">Cardápio</a></li>
          <li><a href="contato.html">Contato</a></li>
          <li><a href="index.html#horarios">Horários</a></li>
        </ul>
      </nav>
    </div>

    <p class="rodape__creditos">Café Cerrado · UNEMAT Sinop · Projeto acadêmico</p>
  </footer>
</body>
</html>
```

Repare em duas escolhas:

- Os cartões de destaque são `<article>` dentro de `<li>`: cada cartão é autocontido (faria sentido sozinho num feed), e a lista informa quantos são.
- A `<meta name="description">` não aparece na tela, mas é o texto que o buscador exibe abaixo do título nos resultados. Uma frase de até 160 caracteres.

### Passo 2 — `cardapio.html`: listas, tabela e `figure`

Duplique `index.html` como `cardapio.html` e faça quatro trocas: o `<title>` vira `Cardápio — Café Cerrado`; a `<meta name="description">` descreve o cardápio; o `aria-current="page"` sai do item **Início** e vai para o item **Cardápio**; e o `<main>` inteiro é substituído pelo bloco abaixo. O `<footer>` fica exatamente igual.

**`cafe-cerrado/cardapio.html` — conteúdo do `<main>`**

```html
  <main class="container">
    <h1>Cardápio</h1>
    <p>
      Preços válidos para consumo no local. Todos os cafés podem ser preparados
      com leite vegetal por R$ 2,00 adicionais.
    </p>

    <nav aria-label="Seções do cardápio">
      <ul class="atalhos">
        <li><a href="#cafes">Cafés</a></li>
        <li><a href="#geladas">Bebidas geladas</a></li>
        <li><a href="#salgados">Salgados</a></li>
        <li><a href="#doces">Doces</a></li>
        <li><a href="#torras">Guia de torras</a></li>
      </ul>
    </nav>

    <section id="cafes">
      <h2>Cafés</h2>

      <ul class="produtos">
        <li>
          <article class="produto">
            <h3>Espresso do Cerrado</h3>
            <p class="produto__preco">R$ 6,00</p>
            <p>Cinquenta mililitros de grãos de altitude, torra média, extraídos em
               vinte e cinco segundos.</p>
          </article>
        </li>

        <li>
          <article class="produto">
            <h3>Coado da Casa</h3>
            <p class="produto__preco">R$ 8,50</p>
            <p>Duzentos mililitros em coador de papel, moagem média feita na hora
               do pedido.</p>
          </article>
        </li>

        <li>
          <article class="produto">
            <h3>Cappuccino Sinop</h3>
            <p class="produto__preco">R$ 12,00</p>
            <p>Espresso duplo, leite vaporizado e canela do Cerrado por cima.</p>
          </article>
        </li>

        <li>
          <article class="produto">
            <h3>Latte de Baunilha</h3>
            <p class="produto__preco">R$ 14,00</p>
            <p>Espresso, leite vaporizado e calda de baunilha feita na casa.</p>
          </article>
        </li>
      </ul>
    </section>

    <section id="geladas">
      <h2>Bebidas geladas</h2>

      <ul class="produtos">
        <li>
          <article class="produto">
            <h3>Cold Brew da Chapada</h3>
            <p class="produto__preco">R$ 15,00</p>
            <p>Extração a frio por dezoito horas, servida com gelo e rodela de laranja.</p>
          </article>
        </li>

        <li>
          <article class="produto">
            <h3>Frappê de Café</h3>
            <p class="produto__preco">R$ 16,00</p>
            <p>Espresso batido com gelo, leite e chantili. Também sai sem lactose.</p>
          </article>
        </li>
      </ul>
    </section>

    <section id="salgados">
      <h2>Salgados</h2>

      <ul class="produtos">
        <li>
          <article class="produto">
            <h3>Pão de Queijo Mineiro</h3>
            <p class="produto__preco">R$ 7,00</p>
            <p>Porção com quatro unidades de polvilho azedo com queijo canastra.</p>
          </article>
        </li>

        <li>
          <article class="produto">
            <h3>Torta de Frango</h3>
            <p class="produto__preco">R$ 13,00</p>
            <p>Fatia generosa com massa amanteigada e recheio de frango desfiado.</p>
          </article>
        </li>
      </ul>
    </section>

    <section id="doces">
      <h2>Doces</h2>

      <ul class="produtos">
        <li>
          <article class="produto">
            <h3>Bolo de Milho Verde</h3>
            <p class="produto__preco">R$ 9,50</p>
            <p>Fatia de bolo cremoso feito com milho da feira do produtor.</p>
          </article>
        </li>

        <li>
          <article class="produto">
            <h3>Brownie de Castanha</h3>
            <p class="produto__preco">R$ 11,00</p>
            <p>Chocolate meio amargo com castanha-do-pará. Sem glúten.</p>
          </article>
        </li>
      </ul>
    </section>

    <section id="torras">
      <h2>Guia de torras</h2>

      <figure>
        <img src="img/grao-cerrado.jpg"
             alt="Grãos de café verdes sendo peneirados em uma bandeja de metal"
             width="1000" height="667"
             loading="lazy">
        <figcaption>
          Grãos do Cerrado mato-grossense recém-beneficiados, antes da torra.
        </figcaption>
      </figure>

      <dl>
        <dt>Torra clara</dt>
        <dd>Realça a acidez e as notas frutadas do grão. Boa para métodos coados.</dd>

        <dt>Torra média</dt>
        <dd>Equilibra doçura, corpo e acidez. É a nossa torra padrão.</dd>

        <dt>Torra escura</dt>
        <dd>Mais amarga e encorpada, com notas de chocolate amargo. Boa para espresso com leite.</dd>
      </dl>

      <div class="tabela-rolavel">
        <table>
          <caption>Grãos disponíveis para moagem e venda em pacote de 250 g</caption>
          <thead>
            <tr>
              <th scope="col">Sítio parceiro</th>
              <th scope="col">Torra</th>
              <th scope="col">Preço do pacote</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <th scope="row">Sítio Santa Rita</th>
              <td>Clara</td>
              <td>R$ 38,00</td>
            </tr>
            <tr>
              <th scope="row">Fazenda Vale Verde</th>
              <td>Média</td>
              <td>R$ 35,00</td>
            </tr>
            <tr>
              <th scope="row">Sítio Boa Esperança</th>
              <td>Escura</td>
              <td>R$ 33,00</td>
            </tr>
          </tbody>
        </table>
      </div>

      <p>
        Quer levar grãos para casa em outra moagem?
        <a href="contato.html">Peça pelo formulário de contato</a>.
      </p>
    </section>
  </main>
```

> **💡 Dica**
> Guarde esses dez produtos com carinho: nome, categoria, preço e descrição. Na Aula 07 eles voltam como um **array de objetos** em `js/app.js`, renderizados como cartões pelo próprio JavaScript; na Unidade 3, viram o `data/produtos.json` servido pela sua API Express. Quanto mais consistente o cardápio ficar hoje, menos retrabalho depois.

### Passo 3 — `contato.html`: o formulário completo

Mesma receita: duplique `index.html` como `contato.html`, ajuste `<title>` e `<meta name="description">`, mova o `aria-current="page"` para o item **Contato** e troque o `<main>` pelo bloco abaixo.

**`cafe-cerrado/contato.html` — conteúdo do `<main>`**

```html
  <main class="container">
    <h1>Fale com a gente</h1>
    <p>
      Reservas para grupos, encomendas de bolos e tortas, eventos e parcerias.
      Respondemos em até um dia útil. Campos marcados com asterisco são obrigatórios.
    </p>

    <form class="formulario" action="contato.html" method="post">
      <fieldset>
        <legend>Seus dados</legend>

        <p class="campo">
          <label for="nome">Nome completo *</label>
          <input type="text" id="nome" name="nome"
                 required minlength="3" maxlength="80"
                 autocomplete="name"
                 placeholder="Ana Beatriz Souza">
        </p>

        <p class="campo">
          <label for="email">E-mail *</label>
          <input type="email" id="email" name="email"
                 required
                 autocomplete="email"
                 placeholder="voce@exemplo.com">
        </p>

        <p class="campo">
          <label for="telefone">Telefone com DDD</label>
          <input type="tel" id="telefone" name="telefone"
                 pattern="\(?[0-9]{2}\)?\s?9?[0-9]{4}-?[0-9]{4}"
                 title="Digite o telefone com DDD, no formato (66) 99999-0000"
                 inputmode="tel"
                 autocomplete="tel"
                 placeholder="(66) 99999-0000">
        </p>

        <p class="campo">
          <label for="cep">CEP</label>
          <input type="text" id="cep" name="cep"
                 pattern="[0-9]{5}-?[0-9]{3}"
                 title="Digite um CEP no formato 78550-000"
                 inputmode="numeric"
                 autocomplete="postal-code"
                 placeholder="78550-000">
        </p>
      </fieldset>

      <fieldset>
        <legend>Sobre o seu pedido</legend>

        <p class="campo">
          <label for="assunto">Assunto *</label>
          <select id="assunto" name="assunto" required>
            <option value="">Selecione um assunto</option>
            <optgroup label="Atendimento">
              <option value="reserva">Reserva de mesa</option>
              <option value="encomenda">Encomenda de bolos e tortas</option>
              <option value="graos">Compra de grãos em pacote</option>
            </optgroup>
            <optgroup label="Institucional">
              <option value="evento">Evento ou parceria</option>
              <option value="trabalhe">Trabalhe conosco</option>
            </optgroup>
          </select>
        </p>

        <p class="campo">
          <label for="pessoas">Quantas pessoas</label>
          <input type="number" id="pessoas" name="pessoas"
                 min="1" max="40" step="1" value="2">
        </p>

        <p class="campo">
          <label for="data">Data desejada</label>
          <input type="date" id="data" name="data">
        </p>

        <p class="campo">
          <label for="horario">Horário</label>
          <input type="time" id="horario" name="horario"
                 min="07:00" max="20:00" step="900">
        </p>

        <p class="campo">
          <label for="mensagem">Mensagem *</label>
          <textarea id="mensagem" name="mensagem"
                    rows="5" maxlength="500"
                    required minlength="10"
                    placeholder="Conte o que você precisa"></textarea>
        </p>
      </fieldset>

      <fieldset>
        <legend>Como prefere ser respondido?</legend>

        <p class="campo campo--linha">
          <label>
            <input type="radio" name="canal" value="email" checked>
            E-mail
          </label>

          <label>
            <input type="radio" name="canal" value="telefone">
            Telefone
          </label>

          <label>
            <input type="radio" name="canal" value="whatsapp">
            WhatsApp
          </label>
        </p>
      </fieldset>

      <p class="campo">
        <label>
          <input type="checkbox" name="novidades" value="sim">
          Quero receber avisos de novos lotes de café por e-mail
        </label>
      </p>

      <p class="campo">
        <label>
          <input type="checkbox" name="consentimento" value="sim" required>
          Autorizo o Café Cerrado a usar meus dados para responder a este contato *
        </label>
      </p>

      <input type="hidden" name="origem" value="site-contato">

      <p class="campo">
        <button type="submit" class="botao">Enviar mensagem</button>
        <button type="reset" class="botao botao--vazado">Limpar formulário</button>
      </p>
    </form>

    <section id="outros-canais">
      <h2>Outros canais</h2>
      <ul>
        <li><a href="tel:+556699999000">Ligar para (66) 9 9999-9000</a></li>
        <li>
          <a href="mailto:contato@cafecerrado.exemplo.br?subject=Reserva%20de%20mesa">
            Enviar e-mail já com o assunto "Reserva de mesa"
          </a>
        </li>
        <li><a href="index.html#horarios">Conferir o horário de atendimento</a></li>
      </ul>
    </section>
  </main>
```

O `action="contato.html"` é um placeholder honesto: o site ainda é estático, não há servidor para receber os dados. Ao enviar, o navegador recarrega a própria página — e é exatamente isso que você deve observar no teste. Na Aula 07, o JavaScript vai interceptar o envio; na Unidade 3, o `action` aponta para a sua API Express.

### Passo 4 — Um mínimo de CSS para enxergar a estrutura

Na próxima aula o Café Cerrado adota o Bootstrap, e boa parte deste CSS será substituída. Por enquanto, o suficiente para que a estrutura fique legível — escrito com as **variáveis da Aula 02**, porque o checkpoint daquela aula ("nenhuma cor literal fora do `:root`") continua valendo.

Primeiro, acrescente três variáveis ao `:root` que já existe no alto do arquivo. Não crie um segundo `:root`: edite o que está lá.

**`cafe-cerrado/css/estilo.css`** — dentro do `:root` da Aula 02

```css
:root {
  /* … as variáveis da Aula 02 continuam aqui … */

  /* Novas nesta aula */
  --cor-borda-campo: #8a7a68;   /* 4,1:1 sobre o branco: a WCAG exige 3:1 na borda de um campo */
  --cor-erro: #b42318;
  --realce-invalido: rgba(180, 35, 24, 0.25);
}
```

Agora acrescente as regras abaixo **ao final** do arquivo, depois de ter apagado as regras órfãs da Aula 02 (o aviso do início do Mão na massa).

**`cafe-cerrado/css/estilo.css` — acrescente ao final**

```css
/* Ancoragem suave, compensando a altura do cabeçalho */
html {
  scroll-behavior: smooth;
  scroll-padding-top: 5rem;
}

.container {
  width: 100%;
  max-width: var(--largura-maxima);
  margin-inline: auto;
  padding-inline: var(--espaco-2);
}

/* Cabeçalho e menu */
.topo {
  background: var(--cor-superficie);
  border-bottom: 1px solid var(--borda-suave);
}

.topo__interno {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: var(--espaco-2);
  padding-block: var(--espaco-2);
}

.marca { color: var(--cor-marca-escura); text-decoration: none; }
.marca__nome { display: block; font-size: 1.4rem; font-weight: 700; }
.marca__slogan { display: block; font-size: .8rem; color: var(--cor-texto-suave); }

.menu {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  list-style: none;
  margin: 0;
  padding: 0;
}

.menu a {
  display: block;
  padding: .25rem 0;
  color: var(--cor-marca-escura);
  font-weight: 500;
  text-decoration: none;
}

.menu a:hover,
.menu a:focus-visible { text-decoration: underline; }

/* O destaque da página atual sai do atributo, sem classe extra */
.menu a[aria-current="page"] {
  color: var(--cor-destaque);
  border-bottom: 2px solid var(--cor-destaque);
}

/* Listas de cartões e de produtos */
.cartoes, .produtos, .atalhos { list-style: none; margin: 0; padding: 0; }

.cartoes, .produtos {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: var(--espaco-2);
  margin-block: var(--espaco-2) var(--espaco-3);
}

.atalhos {
  display: flex;
  flex-wrap: wrap;
  gap: var(--espaco-2);
  margin-block: var(--espaco-2);
}

.cartao, .produto {
  height: 100%;
  padding: var(--espaco-2);
  background: var(--cor-superficie);
  border: 1px solid var(--borda-suave);
  border-radius: var(--raio);
}

.cartao__preco, .produto__preco { font-weight: 700; color: var(--cor-destaque); }

/* Tabelas: rolam sozinhas em vez de estourar a tela */
.tabela-rolavel { overflow-x: auto; margin-block: var(--espaco-2); }

table { border-collapse: collapse; width: 100%; min-width: 22rem; }
caption { text-align: left; font-weight: 600; padding-bottom: var(--espaco-1); }

th, td {
  border: 1px solid var(--borda-suave);
  padding: .5rem .75rem;
  text-align: left;
}

thead th { background: var(--cor-fundo); }

/* Figuras */
figure { margin: 1.5rem 0; }
figure img { max-width: 100%; height: auto; border-radius: var(--raio); }
figcaption { font-size: .9rem; color: var(--cor-texto-suave); padding-top: var(--espaco-1); }

/* Formulário */
.formulario fieldset {
  padding: var(--espaco-2);
  margin-block: 1.5rem;
  border: 1px solid var(--borda-suave);
  border-radius: var(--raio);
}

.formulario legend { font-weight: 600; padding-inline: var(--espaco-1); }

.campo {
  display: flex;
  flex-direction: column;
  gap: .35rem;
  margin-block: var(--espaco-2);
}

.campo--linha { flex-direction: row; flex-wrap: wrap; gap: 1.5rem; }
.campo label { font-weight: 500; }

.campo input, .campo select, .campo textarea {
  font: inherit;
  max-width: 32rem;
  padding: var(--espaco-1);
  border: 1px solid var(--cor-borda-campo);
  border-radius: 6px;
}

/* :user-invalid só marca o campo DEPOIS da interação (seção 4.5) */
.campo input:user-invalid,
.campo select:user-invalid,
.campo textarea:user-invalid {
  border-color: var(--cor-erro);
  outline: 2px solid var(--realce-invalido);
}

/* Botões */
.botao {
  display: inline-block;
  padding: .6rem 1.2rem;
  background: var(--cor-marca);
  color: var(--cor-superficie);
  border: 2px solid var(--cor-marca);
  border-radius: 999px;
  font: inherit;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
}

.botao--vazado { background: transparent; color: var(--cor-marca); }

.botao:hover,
.botao:focus-visible {
  background: var(--cor-marca-escura);
  border-color: var(--cor-marca-escura);
  color: var(--cor-superficie);
}

/* Rodapé */
.rodape {
  margin-top: var(--espaco-4);
  padding-block: var(--espaco-3);
  background: var(--cor-marca-escura);
  color: var(--cor-superficie);
}

.rodape__grade {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--espaco-3);
}

.rodape h2 { font-size: 1rem; }
.rodape ul { list-style: none; padding: 0; }
.rodape a { color: var(--cor-fundo); }
.rodape address { font-style: normal; line-height: 1.7; }

.rodape__creditos {
  text-align: center;
  font-size: .85rem;
  opacity: .8;
  padding-top: 1.5rem;
}
```

> **🧠 Você sabia?**
> As duas regras `.rodape` — a da Aula 02 e esta — não podem coexistir. Se você não apagou a antiga, o navegador aplica **as duas**, na ordem do arquivo, e o resultado é uma mistura: `text-align: center` da primeira sobrevive porque a segunda não o redefine. Esse é o tipo de bug que não aparece no validador, não aparece no console e só some quando alguém lê o CSS inteiro. Na Aula 04 o problema desaparece pela raiz: o `estilo.css` é reescrito do zero.

### Passo 5 — Validar no W3C

Abra <https://validator.w3.org/nu/>, escolha **Validate by direct input** e cole o conteúdo de cada uma das três páginas, uma por vez. Corrija tudo o que aparecer como `Error`. Os `Warning` merecem leitura, mas nem todos exigem ação — o aviso sobre `<section>` sem título, por exemplo, é legítimo e você deve resolver; o aviso sobre codificação de caracteres desaparece quando a página é servida por HTTP de verdade.

### Passo 6 — Publicar

**Terminal, na pasta do repositório**

```bash
git add index.html cardapio.html contato.html css/estilo.css
git commit -m "Estrutura semantica das tres paginas com formulario de contato"
git push
```

O GitHub Pages republica sozinho em cerca de um minuto. Abra o endereço público e confira as três páginas.

### Como testar

1. Abra `index.html` com o Live Server. Os três links do menu funcionam e "Início" está destacado. Em `cardapio.html`, o destaque muda para "Cardápio"; em `contato.html`, para "Contato".
2. Clique em "Ver nas bebidas geladas" no cartão do Cold Brew: você vai para `cardapio.html` e a página rola até a seção **Bebidas geladas**, com o título visível abaixo do cabeçalho (é o `scroll-padding-top` funcionando).
3. No `cardapio.html`, os cinco atalhos rolam para as seções corretas. Reduza a janela para 380 px de largura: a tabela de grãos ganha uma barra de rolagem própria e a página não rola na horizontal.
4. Em `contato.html`, clique em **Enviar mensagem** com tudo em branco. O navegador deve bloquear o envio e mostrar a mensagem "Preencha este campo" (ou equivalente) no campo **Nome completo**.
5. Preencha o nome com duas letras e envie: a mensagem muda para algo como "Use pelo menos 3 caracteres". Digite `ana` no e-mail: "Inclua um '@' no endereço de e-mail".
6. Digite `123` no telefone e envie: aparece o texto do `title` — "Digite o telefone com DDD, no formato (66) 99999-0000".
7. Preencha tudo corretamente, **sem** marcar o consentimento, e envie: o navegador bloqueia no checkbox. Marque e envie: a página recarrega (comportamento esperado por enquanto).
8. Clique no texto do rótulo "Quero receber avisos de novos lotes": o checkbox marca. Se não marcar, o `label` não está associado ao campo.
9. Navegue a página inteira apenas com <kbd>Tab</kbd>. Todo campo deve mostrar foco visível, e a ordem deve ser de cima para baixo.
10. Cole as três páginas no validador do W3C: zero erros.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Escreva o esqueleto semântico de uma página de notícia: cabeçalho com o nome do jornal e o menu, conteúdo principal com o artigo (título, autor, corpo), uma barra lateral com "leia também" e o rodapé. Use apenas tags semânticas — zero `div`.

**A2.** Qual a diferença entre `<section>` e `<article>`? Dê um exemplo de cada tirado do `cardapio.html` que você escreveu e justifique.

**A3.** Explique por que `<header>` pode aparecer várias vezes em uma página, mas `<main>` não. O que muda na árvore de acessibilidade quando o `<header>` **não** é filho direto do `<body>`?

**A4.** Corrija a hierarquia de títulos abaixo e explique cada mudança:

```html
<h1>Café Cerrado</h1>
<h3>Cardápio</h3>
<h2>Espresso do Cerrado</h2>
<h5>Ingredientes</h5>
<h1>Contato</h1>
```

**A5.** Para cada situação, escreva o `alt` adequado (ou justifique o `alt=""`): (a) foto do cappuccino no cardápio; (b) ícone de xícara ao lado do texto "Cafés", que já está escrito na tela; (c) logo do Café Cerrado dentro de um link para `index.html`; (d) gráfico com o consumo semanal por tipo de bebida.

**A6.** Escreva a marcação completa de uma tabela com o consumo semanal de três produtos, incluindo `caption`, `thead`, `tbody` e `th` com `scope` correto nas duas direções. Depois explique, em uma frase, o que muda para o leitor de tela por causa do `scope`.

**A7.** Dê o código de cinco links diferentes a partir de `cardapio.html`: (a) para o `index.html`; (b) para a seção `#doces` da própria página; (c) para a seção `#horarios` da página inicial; (d) para o site da UNEMAT em nova aba, com segurança; (e) para o e-mail do café já com o assunto "Encomenda".

**A8.** Qual a diferença entre `id` e `name` em um campo de formulário? O que acontece se faltar cada um deles?

**A9.** Escreva um campo de CPF com validação nativa: obrigatório, teclado numérico no celular, aceitando `000.000.000-00` ou `00000000000`, com mensagem de erro clara. Explique cada atributo que você usou.

**A10.** Prevê a saída: o formulário abaixo é enviado com o campo preenchido. Quais pares chave/valor chegam ao servidor? Por quê?

```html
<form method="get" action="/busca">
  <input type="text" id="termo" value="cold brew">
  <input type="hidden" name="pagina" value="1">
  <button type="submit">Buscar</button>
</form>
```

**A11.** Explique, em três frases, por que a validação no navegador não substitui a validação no servidor. Descreva um passo a passo concreto de como alguém burlaria a validação nativa do `contato.html`.

### Nível B — Aplicação

**B1.** Construa a página `sobre.html` do Café Cerrado com estrutura semântica completa: cabeçalho e rodapé iguais aos das outras três páginas (com `aria-current` no lugar certo), um `<main>` com a história em duas `<section>`, uma `<aside>` com a caixa "Nossos parceiros" (lista de três sítios), uma `<figure>` com foto e legenda, e a página adicionada ao menu de todas as outras.

Resultado esperado: quatro páginas navegáveis entre si, `aria-current="page"` correto em cada uma, zero erros no validador do W3C, e a árvore de acessibilidade do DevTools mostrando os landmarks `banner`, `navigation`, `main`, `complementary` e `contentinfo`.

<details markdown="1"><summary>Dica</summary>

Copie o cabeçalho de `index.html` e troque **duas** coisas: o `aria-current` sai do "Início" e vai para o novo item, e o novo item entra em todos os quatro menus. Se esquecer de um, o teste falha — faça uma passada final abrindo as quatro páginas em sequência.
</details>

**B2.** Crie `encomendas.html` com um formulário de encomenda de bolos, contendo ao menos oito campos de **tipos diferentes**: texto, e-mail, telefone com `pattern`, data, número com `min`/`max`, `select` com `optgroup`, grupo de `radio` dentro de `fieldset`, `checkbox` obrigatório de consentimento e `textarea` com `maxlength`. Todos com `label` e `autocomplete` quando fizer sentido.

Resultado esperado: o navegador bloqueia o envio em cada campo obrigatório vazio, com mensagem específica; o campo de telefone recusa `123` e aceita `(66) 99999-0000`; clicar em qualquer rótulo foca ou marca o campo; a página passa no validador do W3C.

<details markdown="1"><summary>Dica</summary>

Comece pela lista dos oito campos em papel, escrevendo ao lado de cada um o `type`, o `name` e a regra de validação. Só depois escreva o HTML. Para o `select` com `required`, lembre-se da primeira `<option value="">`.
</details>

**B3.** Refatore o HTML abaixo, que é o cardápio de um concorrente. Ele produz o visual certo e a semântica errada. Reescreva usando as tags corretas, sem mudar o texto exibido, e escreva um comentário HTML de uma linha acima de cada bloco explicando a troca.

```html
<div class="topo">
  <div class="titulo-grande">Padaria do Bairro</div>
  <div class="links">
    <a href="index.html">Home</a> | <a href="menu.html">Menu</a>
  </div>
</div>
<div class="miolo">
  <div class="titulo-medio">Pães</div>
  <div class="item">
    <div class="titulo-pequeno">Pão francês</div>
    <div>R$ 0,90 a unidade</div>
    <img src="pao.jpg">
  </div>
  <div class="tabela">
    <div class="linha"><div>Dia</div><div>Abre</div></div>
    <div class="linha"><div>Segunda</div><div>06h</div></div>
  </div>
</div>
<div class="rodape">Copyright Padaria do Bairro</div>
```

Resultado esperado: a nova versão usa `header`, `nav`, `ul`, `main`, `section`, `article`, `h1`–`h3`, `img` com `alt`, `table` com `caption`/`thead`/`tbody`/`th scope` e `footer`; passa no validador do W3C; e a árvore de acessibilidade mostra pelo menos quatro landmarks.

<details markdown="1"><summary>Dica</summary>

Faça de trás para frente: primeiro identifique o papel de cada `div` pelo nome da classe, depois escolha a tag. `titulo-grande` no topo é o `h1`; `linha` dentro de `tabela` é `tr`. A `img` sem `alt` é erro de validação, não apenas má prática.
</details>

**B4.** Escreva um "guia de estilo do projeto" no arquivo `docs/html.md` do seu repositório, com as decisões de marcação que você vai seguir o semestre inteiro: quando usar `section` × `article` × `div`, como nomear arquivos de imagem, o padrão de `alt`, quando usar tabela, o padrão do menu (lista + `aria-label` + `aria-current`) e o checklist de validação antes de cada `commit`. Mínimo de uma página, com um exemplo de código para cada regra.

Resultado esperado: o arquivo existe no repositório, tem pelo menos seis regras, cada uma com um exemplo curto de código, e você consegue apontar no `index.html` do Café Cerrado uma linha que segue cada regra.

<details markdown="1"><summary>Dica</summary>

Escreva as regras como frases imperativas curtas ("Toda imagem informativa tem `alt` descritivo em uma frase") e não como teoria. Um guia de estilo que ninguém consegue conferir em dez segundos não é usado por ninguém — nem por você.
</details>

### Nível C — Desafio

**C1.** Estrutura completa do projeto autoral. Defina o domínio do seu projeto (o seu "Café Cerrado": um brechó, um viveiro de mudas, uma escolinha de futebol, um estúdio de tatuagem, uma banda) e construa as **três páginas** equivalentes: inicial, catálogo e contato. Exigências: HTML semântico com todos os landmarks; um `<h1>` por página e hierarquia de títulos sem saltos; pelo menos uma `<figure>`, uma tabela de dados com `caption` e `th scope`, uma `<dl>` e três tipos de lista; menu idêntico nas três páginas com `aria-label` e `aria-current`; formulário de contato com no mínimo oito campos de tipos diferentes, todos com `label`, `required` onde faz sentido e ao menos dois `pattern`; e as três páginas com zero erros no validador do W3C. Este é o esqueleto que será estilizado na Aula 04 e chega pronto no Marco 1.

<details markdown="1"><summary>Dica</summary>

Não comece pelo código: liste em papel o conteúdo real das três páginas (títulos, seções, itens do catálogo com preço e descrição) e só então escolha as tags. Os itens do seu catálogo vão virar objetos JavaScript na Aula 07 — se você escrever nomes, categorias, preços e descrições consistentes agora, ganha tempo depois. Copie a estrutura do Café Cerrado e troque o conteúdo; o que se aprende aqui é a arquitetura, não o texto.
</details>

## 🏆 Desafios

### ⭐ Caça aos landmarks
Tags: html, acessibilidade, devtools, investigacao

Quantas regiões um leitor de tela consegue enxergar no seu site? E no site da sua faculdade? Sem instalar nada, o DevTools mostra a mesma árvore que o leitor de tela usa — e a diferença entre um site bem marcado e um mar de `div` fica escandalosa em trinta segundos. Faça essa comparação e, no caminho, descubra se o **seu** projeto está mais para um lado ou para o outro.

**Critérios de pronto**

- Uma tabela em `docs/landmarks.md` comparando **três** sites (o seu projeto autoral, o portal da UNEMAT e um site de sua escolha) com as colunas: site, quantidade de landmarks, landmarks encontrados.
- Para cada site, a captura de tela da árvore de acessibilidade do DevTools.
- Um parágrafo apontando o site com melhor estrutura e explicando **por quê**, citando tags específicas.
- No mínimo duas correções aplicadas ao seu próprio projeto a partir do que você observou, listadas no arquivo com o antes e o depois.

<details markdown="1"><summary>Pistas</summary>

1. No Chrome: <kbd>F12</kbd> → **Elements** → painel direito → aba **Accessibility** → marque "Enable full-page accessibility tree" e clique no ícone no topo do painel Elements.
2. No Firefox, a aba **Acessibilidade** tem um filtro por tipo de item — escolha "Landmarks" para ver só as regiões.
3. Sites com muitos `<div role="navigation">` estão simulando com ARIA o que a tag nativa faria de graça. Anote quando encontrar: isso vira assunto na aula de Acessibilidade e ARIA.
</details>

### ⭐⭐ O formulário que não deixa você errar
Tags: html, formularios, acessibilidade, refatoracao

Existe um formulário famoso por ser insuportável: o de cadastro que rejeita o seu telefone porque você digitou parênteses, recusa a senha porque tem um caractere "inválido" que ele não diz qual é, e apaga tudo quando você erra um campo. O oposto disso — um formulário que **ajuda** — é feito de escolhas pequenas: `inputmode` certo, `autocomplete` certo, `pattern` permissivo com `title` explicativo, e nenhum campo obrigatório sem necessidade. Reprojete o `contato.html` do Café Cerrado com essa obsessão.

**Critérios de pronto**

- Todos os campos têm `autocomplete` com o valor correto da especificação HTML (pesquise a lista de tokens; `nome`, `email`, `tel`, `cep` e `data` têm token próprio).
- Todo campo de texto com formato definido tem `inputmode` adequado e um `title` que descreve o formato em linguagem natural, não em expressão regular.
- Os `pattern` aceitam as variações que uma pessoa real digita: telefone com e sem parênteses, com e sem espaço, com e sem hífen; CEP com e sem hífen.
- Um arquivo `docs/formulario.md` com uma tabela de três colunas: campo, o que era exigido antes, o que passou a ser aceito.
- Teste no celular (ou no modo dispositivo do DevTools) documentado com capturas: cada campo abre o teclado correto.

<details markdown="1"><summary>Pistas</summary>

1. A lista completa de valores de `autocomplete` está na especificação do WHATWG e na página "atributo autocomplete" da MDN — são mais de cinquenta tokens.
2. `inputmode` aceita `numeric`, `tel`, `email`, `decimal`, `search` e `url`. Ele muda o teclado sem mudar a semântica do campo, o que é diferente de trocar o `type`.
3. Para o telefone, pense na expressão regular em partes: DDD opcionalmente entre parênteses, espaço opcional, nono dígito opcional, quatro dígitos, hífen opcional, quatro dígitos.
4. Teste cada `pattern` isoladamente em um arquivo separado antes de colocar no formulário. Um `pattern` errado bloqueia o envio de valores corretos e é difícil de perceber.
</details>

### ⭐⭐ Caça ao bug de marcação
Tags: html, formularios, bug, investigacao

O arquivo abaixo abre no navegador sem nenhum erro visível no console e parece funcionar. Mas ele tem **sete** problemas: alguns o validador do W3C aponta, outros só aparecem quando você navega por teclado ou clica nos rótulos. Encontre todos os sete, corrija e documente cada um. Regra: você só pode usar o validador do W3C, o DevTools e a tecla <kbd>Tab</kbd> — nada de pedir a resposta pronta.

**`caca-ao-bug.html`**

```html
<!DOCTYPE html>
<html>
<head>
  <title>Reserva</title>
</head>
<body>
  <div class="topo">
    <h2>Café Cerrado</h2>
    <a href="index.html">Início</a>
    <a href="Cardapio.html">Cardápio</a>
  </div>

  <h1>Reserva de mesa</h1>

  <form method="post">
    <label for="nome">Nome</label>
    <input type="text" id="nome" required>

    <label for="email">E-mail</label>
    <input type="text" id="nome" name="email" required>

    <label>Telefone</label>
    <input type="number" name="telefone" pattern="[0-9]{11}">

    <select name="mesa">
      <option>Mesa interna</option>
      <option>Mesa na calçada</option>
    </select>

    <img src="/img/mesa.jpg">

    <button>Reservar</button>
  </form>
</body>
</html>
```

**Critérios de pronto**

- Uma versão corrigida do arquivo, com um comentário HTML de uma linha acima de cada correção, explicando o problema.
- O arquivo corrigido passa no validador do W3C com zero erros e zero avisos evitáveis.
- Um documento `docs/bugs-marcacao.md` com os sete problemas, cada um classificado como "erro de validação", "erro de acessibilidade" ou "erro que só aparece em produção".
- O formulário corrigido envia **todos** os campos: prove com a aba Network do DevTools, mostrando o corpo da requisição.

<details markdown="1"><summary>Pistas</summary>

1. Comece pelo validador. Ele acha três de uma vez, e um deles envolve dois elementos com o mesmo identificador.
2. Depois pressione <kbd>Tab</kbd> e clique em cada rótulo. Um dos rótulos não faz nada quando clicado — por quê?
3. Um dos campos nunca chega ao servidor, mesmo preenchido. Compare os atributos dele com os dos outros (revise a seção 4.1).
4. Um dos problemas só aparece depois do `git push`: o link funciona na sua máquina e dá 404 no GitHub Pages. Há **dois** motivos possíveis nesse arquivo — o caminho da imagem e o nome de um arquivo.
5. `pattern` não funciona em qualquer `type`. O validador avisa; leia a mensagem inteira.
</details>

### ⭐⭐⭐ Reprodução estrutural de uma página real
Tags: html, acessibilidade, layout, investigacao, projeto

Escolha uma página de um site que você usa toda semana — um portal de notícias, uma loja, o sistema acadêmico, um blog técnico — e reproduza a **estrutura semântica** dela: só HTML, sem uma linha de CSS, com conteúdo escrito por você (nada de copiar textos ou imagens). O objetivo não é ficar parecido: é descobrir que a maior parte do que você vê na tela é decoração por cima de uma árvore de umas quarenta tags. Ao terminar, você vai olhar para qualquer site com raio-X.

**Critérios de pronto**

- O arquivo `reproducao.html` renderiza sem CSS e continua **compreensível**: dá para ler a página inteira de cima a baixo e entender a hierarquia só pelos títulos.
- Um documento com o sumário de títulos (`h1` a `h4`) da página original e o da sua reprodução, lado a lado, apontando as diferenças.
- Pelo menos oito tags semânticas diferentes usadas corretamente, listadas com uma justificativa de uma linha cada.
- Uma tabela comparando a quantidade de landmarks da página original com a da sua reprodução, com um parágrafo dizendo qual das duas um leitor de tela navegaria melhor e por quê.
- Zero erros no validador do W3C e nenhuma `<div>` que pudesse ser substituída por uma tag semântica.

**Para ir além:** aplique a mesma reprodução à página inicial do seu projeto autoral e compare — o que o site profissional faz que o seu ainda não faz?

<details markdown="1"><summary>Pistas</summary>

1. Comece pelo DevTools na página original: colapse todos os nós do painel Elements (<kbd>Ctrl</kbd> + clique na seta) e vá abrindo nível por nível. A estrutura macro aparece em menos de um minuto.
2. Desligue o CSS da página original para ver o esqueleto: no Firefox, menu **Exibir → Estilo da página → Sem estilo**; no Chrome, desmarque a folha de estilo na aba **Network** e recarregue, ou use o modo leitor.
3. Extraia o sumário de títulos com a árvore de acessibilidade do DevTools, filtrando por "headings" — é mais rápido que ler o HTML.
4. Se a página usa muito `<div role="...">`, anote: é um site simulando com ARIA o que a tag nativa faria sozinha. Na sua reprodução, use a tag nativa e mostre a diferença na contagem de landmarks.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `Error: Duplicate ID "nome".` no validador | Dois elementos com o mesmo `id`, normalmente por copiar e colar um campo | Deixe cada `id` único; confira também se o `label for` aponta para o campo certo |
| O campo é preenchido, mas não chega ao servidor | Falta o atributo `name` — `id` sozinho não envia nada | Todo campo que deve ser enviado precisa de `name` |
| `Error: Attribute pattern is only allowed when the input type is email, password, search, tel, text, or url.` | `pattern` usado em `type="number"` ou `type="date"` | Use `type="text"` com `pattern` e `inputmode="numeric"`, ou troque para `min`/`max`/`step` |
| Clicar no rótulo não foca o campo | O `for` do `label` não bate com o `id` do campo (ou o campo não tem `id`) | Confira o par `for`/`id`, ou envolva o campo com o próprio `<label>` |
| `select` obrigatório nunca acusa erro | A primeira `<option>` tem um valor válido e já vem selecionada | Coloque `<option value="">Selecione</option>` como primeira opção |
| A imagem aparece no Live Server e some no GitHub Pages | Caminho absoluto (`/img/foto.jpg`) ou nome com maiúscula/acento/espaço | Use caminho relativo (`img/foto.jpg`) e nomes em minúsculas, sem acento, com hífen |
| A âncora rola até a seção, mas o título fica escondido atrás do cabeçalho | Cabeçalho fixo cobrindo o alvo da âncora | `html { scroll-padding-top: 5rem; }` com a altura do cabeçalho |
| `Error: An img element must have an alt attribute, except under certain conditions.` | `<img>` sem `alt` | Adicione `alt` descritivo; se a imagem for decorativa, use `alt=""` |
| O `textarea` já vem com espaços dentro | Quebra de linha ou indentação entre `<textarea>` e `</textarea>` | Escreva as duas tags coladas, sem nada entre elas |
| `Error: Element "li" not allowed as child of element "div" in this context.` | `<li>` fora de `<ul>`, `<ol>` ou `<menu>` | Envolva os itens na lista correta |
| Todos os campos ficam vermelhos assim que a página abre | O CSS usa `:invalid`, que casa com campos `required` vazios desde o carregamento | Use `:user-invalid`, que só casa depois da interação |
| O leitor de tela anuncia "navegação" três vezes sem distinguir | Vários `<nav>` sem `aria-label` | Rotule cada um: `<nav aria-label="Principal">`, `<nav aria-label="Rodapé">` |
| O formulário recarrega a página e perde os dados ao enviar | Comportamento padrão de `<form>` sem servidor que responda | Esperado nesta aula; na Aula 07 o JavaScript intercepta com `preventDefault()` |

## 🏠 Para praticar depois da aula (1 h)

**Parte 1 — Leitura (20 min).** QUEIRÓS e PORTELA, *Introdução ao Desenvolvimento Moderno para a Web*, seções sobre a camada de estrutura (HTML) e a camada de apresentação (CSS) — esta segunda serve de preparação para a próxima aula. Na MDN em pt-BR, leia "Estrutura de um documento e sites" e "Seu primeiro formulário". Anote **duas** tags ou atributos que aparecem nas leituras e não apareceram nesta aula.

**Parte 2 — Entrega (30 min).** No repositório do seu **projeto autoral**:

1. As três páginas do exercício **C1** completas e navegáveis entre si.
2. O guia de marcação do exercício **B4** em `docs/html.md`.
3. As três páginas validadas no W3C — cole no `README.md` o print ou o texto "Document checking completed. No errors or warnings to show." para cada uma.
4. `README.md` atualizado com: nome do projeto, uma frase sobre o domínio escolhido, a lista de páginas e o link do GitHub Pages.

**Parte 3 — Explicar a decisão (10 min).** Em `docs/decisao.md`, escreva um trecho de dez a vinte linhas do HTML do seu projeto e explique **uma** decisão de marcação que você tomou e por quê (por exemplo: por que aquele bloco é `article` e não `section`). Se puder, compare com um colega (ou releia depois de um dia) e anote uma melhoria concreta que encontrar.

**Critério de pronto:** as três páginas do projeto autoral abrem pelo endereço do GitHub Pages; o menu leva de qualquer página para qualquer outra e marca a atual com `aria-current`; o formulário bloqueia o envio quando algum campo obrigatório está vazio, com mensagem específica; e o validador do W3C não aponta nenhum erro em nenhuma das três.

**Guarde no seu repositório:** commit + push.

## ✅ Checkpoint do projeto

Ao fim desta aula, o repositório do seu projeto autoral deve ter:

- [ ] Três páginas HTML ligadas entre si, todas com `<!DOCTYPE html>`, `lang="pt-BR"`, `<meta charset>`, `<meta name="viewport">`, `<title>` distinto e `<meta name="description">`.
- [ ] Landmarks completos em todas as páginas: `header`, `nav`, `main`, `footer` (e `aside` em pelo menos uma).
- [ ] Um único `<h1>` por página e hierarquia de títulos sem saltos de nível.
- [ ] Menu idêntico nas três páginas, como `<ul>` dentro de `<nav aria-label="Principal">`, com `aria-current="page"` no item correto de cada uma.
- [ ] Toda imagem com `alt` adequado (descritivo ou `alt=""` para decorativas) e `width`/`height` declarados.
- [ ] Pelo menos uma `<figure>` com `<figcaption>` e uma `<dl>` com três pares.
- [ ] Uma tabela de dados com `caption`, `thead`, `tbody` e `th scope`, dentro de um contêiner com `overflow-x: auto`.
- [ ] Pelo menos cinco formas diferentes de link em uso: página interna, âncora, âncora em outra página, URL externa com `rel="noopener"`, `mailto:` e/ou `tel:`.
- [ ] Formulário de contato com no mínimo oito campos de tipos diferentes, cada um com `<label>`, agrupados em `<fieldset>`/`<legend>`, com `required`, ao menos dois `pattern` com `title` e um `checkbox` de consentimento obrigatório.
- [ ] Caminhos de arquivo relativos, em minúsculas, sem espaços e sem acentos.
- [ ] Zero erros no validador do W3C nas três páginas.
- [ ] `commit` e `push` feitos; site atualizado no GitHub Pages.

## 📚 Para aprofundar

- MDN — **Estrutura de um documento e sites** (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Learn/HTML/Introduction_to_HTML/Document_and_website_structure> — a página que resume, com exemplos, tudo o que a seção 1 discutiu.
- MDN — **Seu primeiro formulário HTML** (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Learn/Forms/Your_first_form> — leia até o fim e faça o exemplo; é a base do que você vai automatizar na Unidade 2.
- MDN — **Validação de dados de formulário** (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Learn/Forms/Form_validation> — cobre `pattern`, `ValidityState` e mensagens personalizadas.
- MDN — **`<input>`: o elemento de entrada**: <https://developer.mozilla.org/pt-BR/docs/Web/HTML/Element/input> — a lista completa dos tipos, com exemplo interativo de cada um. Guarde nos favoritos.
- MDN — **Atributo `autocomplete`**: <https://developer.mozilla.org/pt-BR/docs/Web/HTML/Attributes/autocomplete> — a tabela de tokens que o desafio ⭐⭐ pede.
- WHATWG — **HTML Living Standard, seção Forms**: <https://html.spec.whatwg.org/multipage/forms.html> — a especificação oficial, para quando a MDN não bastar.
- **Validador do W3C**: <https://validator.w3.org/nu/> — use antes de cada `commit`; o hábito vale mais que a ferramenta.
- **WAI-ARIA Authoring Practices — Landmarks**: <https://www.w3.org/WAI/ARIA/apg/patterns/landmarks/> — quando e como rotular cada região da página.
- QUEIRÓS, Ricardo; PORTELA, Filipe. *Introdução ao Desenvolvimento Moderno para a Web*. FCA, 2018 — camada de estrutura (HTML) e camada de apresentação (CSS).
- PUREWAL, Semmy. *Aprendendo a Desenvolver Aplicações Web*. Novatec, 2014 — capítulos de estruturação de páginas e formulários.
- ALVES, William P. *Projetos de Sistemas Web*. Érica, 2015 — elementos de interface e formulários em sistemas.

Na próxima aula o Café Cerrado ganha aparência profissional sem você escrever centenas de linhas de CSS: vamos comparar as duas filosofias dominantes dos frameworks CSS — componentes prontos e classes utilitárias —, experimentar Bootstrap, Tailwind e Material Web lado a lado, e adotar um deles no projeto, com a escolha justificada no `README.md`. A estrutura semântica que você escreveu hoje permanece exatamente como está: o framework entra nas classes, não no lugar das tags.
