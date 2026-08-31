# Aula 02 — Introdução ao HTML: estrutura, textos, links e tabelas

> **Nível 1 — Introdução ao Desenvolvimento Web** · Unidade 1: Arquitetura da Web e HTML
> WebLab · UNEMAT Sinop · Prof. Ivan Luiz Pedroso Pires
> **Carga:** 3 aulas de 50 min (presencial) + 1 h (assíncrona)

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Escrever a estrutura mínima de um documento HTML5 válido e explicar a função de cada linha do `<head>`.
- Aplicar os elementos de texto (títulos, parágrafos, ênfase, citações, quebras) respeitando a hierarquia e o significado de cada um.
- Construir listas ordenadas, não ordenadas, de definição e aninhadas.
- Criar links externos, internos, de âncora, de e-mail, de telefone e de download, com caminhos relativos corretos e atributos de segurança.
- Marcar tabelas de dados com `caption`, `thead`/`tbody`/`tfoot`, `th scope` e mesclagem de células.
- Usar HTML semântico (`header`, `nav`, `main`, `section`, `article`, `aside`, `footer`) em vez de `div` genérica.
- Validar páginas no validador do W3C e corrigir os erros apontados.

## 📋 Pré-requisitos

- [ ] Pasta `introducao-web/` da Aula 01 com `site-evento/index.html` abrindo no Live Server.
- [ ] VS Code com Live Server e Prettier instalados e *format on save* ativado.
- [ ] Navegador com DevTools — você vai usar a aba **Elements** o tempo todo hoje.
- [ ] Tema do projeto autoral definido (entregue na atividade assíncrona da Aula 01).

Na aula passada você viu como a Web funciona por fora: cliente e servidor, URL, HTTP, o caminho de uma requisição até a renderização — e criou um `index.html` mínimo sem entender cada linha. Hoje você entende cada linha, aprende os elementos de texto, listas, links e tabelas, e constrói três das cinco páginas do site do evento com HTML semântico e validado.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Anatomia do elemento, aninhamento, estrutura do documento, elementos de texto |
| 2 | 50 min | Listas, links (caminhos, âncoras, segurança), tabelas |
| 3 | 50 min | HTML semântico, entidades, validação no W3C; Mão na massa: início, programação e palestrantes do site do evento |

## 1. O que é HTML

HTML é uma linguagem de **marcação**, não de programação: ela não tem variáveis, condicionais ou laços. Sua função é descrever a **estrutura e o significado** do conteúdo por meio de marcas (*tags*). Você não diz ao navegador "desenhe um retângulo azul aqui"; você diz "isto é um título", "isto é um parágrafo", "isto é uma lista de três itens" — e o navegador (ou o leitor de tela, ou o buscador) decide o que fazer com essa informação.

Essa é a diferença entre HTML e um editor de texto: no Word você formata a aparência; no HTML você declara o que cada coisa **é**. A aparência é assunto do CSS, a partir da Aula 05.

### Anatomia de um elemento

```text
<a href="https://unemat.br" title="Site oficial">UNEMAT</a>
└┬┘└──────────┬───────────┘ └───────┬───────┘└──┬──┘└─┬─┘
 │            │                     │           │     │
nome      atributo 1            atributo 2   conteúdo tag
da tag                                                de fechamento
└───────────────── tag de abertura ─────────────┘
```

- **Elemento** = tag de abertura + conteúdo + tag de fechamento.
- **Atributo** = informação adicional, sempre na tag de abertura, no formato `nome="valor"`. Use sempre aspas duplas.
- **Elementos vazios** não têm conteúdo nem fechamento: `<br>`, `<hr>`, `<img>`, `<input>`, `<meta>`, `<link>`.

Os nomes de tags e atributos não diferenciam maiúsculas de minúsculas, mas a convenção universal é **tudo em minúsculas**. Siga-a.

### Aninhamento

Elementos podem conter outros, mas precisam ser fechados na **ordem inversa** da abertura — como parênteses em matemática:

```html
<!-- CORRETO -->
<p>Texto com <strong>destaque <em>duplo</em></strong> aqui.</p>

<!-- ERRADO: fechamento cruzado -->
<p>Texto com <strong>destaque <em>duplo</strong></em> aqui.</p>
```

O aninhamento é o que transforma o HTML em uma **árvore** — a mesma árvore que você viu na Aula 01 com o nome de DOM. `<p>` é pai de `<strong>`, que é pai de `<em>`. Todo elemento tem exatamente um pai (exceto `<html>`, a raiz) e pode ter vários filhos.

> **🧠 Você sabia?**
> O navegador nunca se recusa a exibir um HTML "errado". A especificação da WHATWG descreve, passo a passo, como o parser deve **se recuperar** de cada tipo de erro: uma tag cruzada é reorganizada, um `</li>` esquecido é inserido, um `<p>` aberto dentro de outro `<p>` fecha o anterior. É por isso que páginas quebradas "funcionam" — e por isso que o resultado às vezes não é o que você escreveu. Aliás, pela especificação, fechar `<li>`, `<p>`, `<td>` e `<tr>` é **opcional**; nesta disciplina você fecha tudo, sempre, porque código previsível é mais fácil de ler, depurar e manter.

## 2. Estrutura mínima de um documento

`exercicios/aula02/modelo.html`

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Descrição da página em até 160 caracteres.">
  <meta name="author" content="Seu Nome">
  <title>Título que aparece na aba do navegador</title>
  <link rel="stylesheet" href="css/estilo.css">
</head>
<body>
  <!-- Todo conteúdo visível fica aqui -->
  <script src="js/script.js"></script>
</body>
</html>
```

| Linha | Função |
|---|---|
| `<!DOCTYPE html>` | Declara HTML5. Sem ela, o navegador entra em *quirks mode* e emula bugs de navegadores antigos |
| `lang="pt-BR"` | Idioma do conteúdo. Essencial para leitores de tela (pronúncia), tradução automática e buscadores |
| `<meta charset="UTF-8">` | Codificação de caracteres. Sempre a primeira linha do `<head>` — você viu na Aula 01 o que acontece sem ela |
| `viewport` | Faz a página se adaptar a telas de celular. Sem ela, não há responsividade (Aula 08) |
| `description` | Texto que aparece nos resultados de busca, abaixo do título |
| `<title>` | Título da aba, dos favoritos e do resultado de busca. Obrigatório |
| `<link rel="stylesheet">` | Liga uma folha de estilo externa (Aula 05). Pode omitir enquanto não houver CSS |
| `<script src>` | Liga um arquivo JavaScript (Aula 10). Fica no fim do `<body>` para não bloquear a renderização |

O `<head>` é **invisível**: nada dele aparece na tela. Ele carrega metadados — informações *sobre* a página para o navegador, os buscadores e as redes sociais. Tudo que o usuário vê fica dentro de `<body>`.

> **🔎 Por baixo do capô**
> O *quirks mode* existe por causa da história: nos anos 1990, cada navegador interpretava CSS de um jeito, e milhões de páginas foram escritas em cima desses bugs. Quando os padrões foram corrigidos, os navegadores precisaram de um jeito de saber se a página era "antiga" (renderiza com os bugs) ou "moderna" (renderiza pelo padrão). O sinal é o `<!DOCTYPE>`. Sem ele, o navegador assume o pior — e o seu CSS da Unidade 2 vai se comportar de forma estranha sem motivo aparente.

## 3. Elementos de texto

### Títulos

```html
<h1>Título principal — apenas um por página</h1>
  <h2>Seção</h2>
    <h3>Subseção</h3>
      <h4>Sub-subseção</h4>
```

> **⚠️ Atenção**
> Hierarquia de títulos **não é escolha de tamanho de fonte** — é estrutura de documento. Leitores de tela permitem navegar pulando de título em título, e o Google usa essa hierarquia para entender a página. Nunca pule níveis (`h1` direto para `h4`) e nunca escolha `<h3>` só porque "ficou menor". Tamanho é assunto do CSS.

Pense nos títulos como o sumário de um livro: `<h1>` é o título do livro (um só), `<h2>` são os capítulos, `<h3>` as seções dentro de cada capítulo. Se você conseguir extrair só os títulos da página e eles formarem um sumário coerente, a hierarquia está certa.

### Parágrafos e semântica inline

```html
<p>Um parágrafo comum de texto.</p>

<p>
  Este é <strong>importante</strong> e este tem <em>ênfase</em>.
  Este é apenas <b>negrito visual</b> e este é <i>itálico visual</i>.
  <mark>Texto realçado</mark>, <small>letra miúda</small>,
  <del>removido</del> e <ins>inserido</ins>.
  Fórmula: H<sub>2</sub>O e potência: x<sup>2</sup>.
  Código: <code>let x = 10;</code>.
  Atalho: <kbd>Ctrl</kbd> + <kbd>S</kbd>.
</p>
```

| Par de tags | Diferença |
|---|---|
| `<strong>` × `<b>` | `strong` = importância semântica (o leitor de tela pode enfatizar). `b` = negrito puramente visual (palavras-chave, nome de produto) |
| `<em>` × `<i>` | `em` = ênfase semântica (muda o sentido da frase). `i` = itálico visual (termo estrangeiro, nome científico, pensamento) |

Na prática: use `strong` e `em`; deixe `b` e `i` para casos específicos. Uma regra simples: se você leria a palavra em voz alta com outro tom, é `em`; se a informação é importante mesmo lida em tom neutro, é `strong`.

> **📌 Na prova**
> A diferença entre `<strong>`/`<b>` e `<em>`/`<i>` é pergunta clássica. Resposta curta: os dois pares têm a mesma aparência padrão, mas só `strong` e `em` carregam **significado** — e significado é o que leitores de tela e buscadores usam.

### Citações e quebras

```html
<blockquote cite="https://www.w3.org/">
  <p>A força da Web está em sua universalidade.</p>
  <footer>— <cite>Tim Berners-Lee</cite></footer>
</blockquote>

<p>Endereço:<br>Av. dos Ingás, 3001<br>Sinop — MT</p>

<hr>

<pre>
Texto pré-formatado:
    preserva     espaços
    e quebras de linha.
</pre>
```

- `<blockquote>` é uma citação em bloco; o atributo `cite` guarda a URL da fonte (não aparece na tela). `<cite>` marca o **título da obra ou autor** citado.
- `<q>` é a versão inline: `<p>Ele disse <q>volto já</q> e sumiu.</p>` — o navegador coloca as aspas.
- `<br>` quebra a linha dentro de um bloco; `<hr>` é uma quebra temática (mudança de assunto), não uma "linha decorativa".
- `<pre>` preserva espaços e quebras exatamente como digitados — útil para código e diagramas.

> **⚠️ Atenção**
> `<br>` serve para quebras **dentro** de um bloco de conteúdo (endereços, poemas, letras de música). Usar `<br><br>` para separar parágrafos é erro — use `<p>`. O espaçamento entre parágrafos é assunto do CSS.

## 4. Listas

Três tipos, cada um com um significado:

```html
<!-- Lista não ordenada: a ordem dos itens não importa -->
<ul>
  <li>HTML</li>
  <li>CSS</li>
  <li>JavaScript</li>
</ul>

<!-- Lista ordenada: a ordem importa (passos, ranking) -->
<ol>
  <li>Analisar a URL</li>
  <li>Resolver o DNS</li>
  <li>Abrir conexão TCP</li>
</ol>

<!-- Com atributos: numeração romana, começando em 3, decrescente -->
<ol type="I" start="3" reversed>
  <li>Terceiro item</li>
  <li>Segundo item</li>
  <li>Primeiro item</li>
</ol>

<!-- Lista de definições: pares termo → descrição -->
<dl>
  <dt>HTML</dt>
  <dd>Linguagem de marcação que estrutura o conteúdo.</dd>
  <dt>CSS</dt>
  <dd>Linguagem de estilo que define a apresentação.</dd>
</dl>

<!-- Listas aninhadas: o <ul> filho vai DENTRO do <li> pai -->
<ul>
  <li>Front-end
    <ul>
      <li>HTML</li>
      <li>CSS</li>
    </ul>
  </li>
  <li>Back-end</li>
</ul>
```

A pergunta para escolher entre `<ul>` e `<ol>` é: **se eu embaralhar os itens, a informação muda?** Passos de uma receita, sim → `<ol>`. Ingredientes, não → `<ul>`. A lista de definições (`<dl>`) serve para glossários, metadados ("Autor: Fulano", "Duração: 2 h") e perguntas frequentes.

Um `<ul>` ou `<ol>` só pode ter `<li>` como filhos diretos. Qualquer outra coisa — um `<h3>`, um `<p>`, outra lista — vai **dentro** de um `<li>`. O validador do W3C avisa quando você erra isso.

## 5. Links (âncoras)

O link é a invenção que dá o "hipertexto" ao HTML. Todos os tipos usam o mesmo elemento, `<a>`, e mudam só o `href`:

```html
<a href="https://www.unemat.br">Link externo</a>
<a href="contato.html">Link interno relativo</a>
<a href="/sobre.html">Link a partir da raiz</a>
<a href="#secao3">Âncora interna da própria página</a>
<a href="programacao.html#dia-2">Âncora em outra página</a>
<a href="documentos/edital.pdf" download>Baixar edital</a>
<a href="mailto:contato@unemat.br">Enviar e-mail</a>
<a href="tel:+556635111000">Ligar</a>
<a href="https://exemplo.com" target="_blank" rel="noopener noreferrer">
  Abrir em nova aba
</a>
```

Os caminhos relativos seguem exatamente a tabela da §5 da Aula 01: `contato.html` é "na mesma pasta", `../index.html` é "uma pasta acima", `img/logo.png` é "na subpasta `img`".

> **⚠️ Atenção**
> Segurança: ao usar `target="_blank"`, sempre inclua `rel="noopener noreferrer"`. Sem isso, a página aberta ganha acesso parcial à sua janela original (`window.opener`) e pode redirecioná-la — um vetor de phishing conhecido como *tabnabbing*. Navegadores modernos já aplicam `noopener` por padrão, mas o atributo explícito garante o comportamento em todos.

### Âncoras internas

Para a âncora funcionar, o destino precisa de um `id` — e `id` deve ser **único** na página:

```html
<a href="#metodologia">Ir para Metodologia</a>

<h2 id="metodologia">Metodologia</h2>
<p>O evento combina palestras e oficinas práticas.</p>
```

Ao clicar, o navegador rola até o elemento e acrescenta `#metodologia` à URL — lembre-se da Aula 01: o fragmento nunca é enviado ao servidor. Um link `href="#topo"` para um `id="topo"` no cabeçalho dá o clássico "voltar ao topo".

### Texto de link

Textos de link ruins: "clique aqui", "saiba mais", "link". Um usuário de leitor de tela pode navegar por uma lista só de links — "clique aqui" ali não significa nada. Buscadores também usam o texto do link para entender o destino. Use texto descritivo: "Baixe o edital em PDF", "Veja a programação completa".

## 6. Tabelas

Tabelas são para **dados tabulares** — informação que faz sentido em linhas e colunas, como notas, horários, preços. Jamais para layout: isso quebra em celular, confunde leitores de tela e é assunto do CSS (Aula 07).

```html
<table>
  <caption>Notas da turma</caption>
  <thead>
    <tr>
      <th scope="col">Aluno</th>
      <th scope="col">A1</th>
      <th scope="col">A2</th>
      <th scope="col">A3</th>
      <th scope="col">Média</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Maria Silva</th>
      <td>8,0</td><td>7,5</td><td>9,0</td><td>8,2</td>
    </tr>
    <tr>
      <th scope="row">João Souza</th>
      <td>6,0</td><td>5,5</td><td>7,0</td><td>6,2</td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <th scope="row">Média da turma</th>
      <td>7,0</td><td>6,5</td><td>8,0</td><td>7,2</td>
    </tr>
  </tfoot>
</table>
```

| Elemento | Função |
|---|---|
| `<caption>` | Título/legenda da tabela — o leitor de tela anuncia antes de entrar nela |
| `<thead>`, `<tbody>`, `<tfoot>` | Agrupamento semântico de linhas: cabeçalho, corpo, rodapé (totais) |
| `<tr>` | Linha (*table row*) |
| `<th>` | Célula de cabeçalho |
| `<td>` | Célula de dado |
| `scope="col"` / `scope="row"` | Informa a leitores de tela a qual eixo o cabeçalho pertence |

### Mesclagem de células

```html
<td colspan="3">Ocupa 3 colunas</td>
<td rowspan="2">Ocupa 2 linhas</td>
```

`colspan` estende a célula para a direita; `rowspan`, para baixo. Cuidado com a contagem: se uma linha tem `colspan="3"`, as linhas seguintes precisam continuar somando o mesmo número de colunas, senão a tabela fica torta e o validador reclama.

Sem CSS, a tabela aparece sem bordas — parece "só texto alinhado". É normal. A Aula 06 coloca as bordas; hoje o que importa é a estrutura estar certa.

## 7. HTML semântico

Antes do HTML5, tudo era `<div>`. O resultado era a chamada *div soup*: código ilegível, inacessível e ruim para buscadores. O HTML5 trouxe elementos que dizem **o que a região é**:

```html
<body>
  <header>
    <h1>Nome do site</h1>
    <nav>
      <ul>
        <li><a href="index.html">Início</a></li>
        <li><a href="sobre.html">Sobre</a></li>
        <li><a href="contato.html">Contato</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <article>
      <header>
        <h2>Título do artigo</h2>
        <p>Publicado em <time datetime="2026-08-19">19 de agosto</time></p>
      </header>
      <section>
        <h3>Primeira seção</h3>
        <p>Texto da primeira seção do artigo.</p>
      </section>
      <footer>Autor: Maria Silva</footer>
    </article>

    <aside>
      <h3>Conteúdo relacionado</h3>
      <p>Links, publicidade, biografia do autor.</p>
    </aside>
  </main>

  <footer>
    <p>&copy; UNEMAT — Todos os direitos reservados</p>
  </footer>
</body>
```

| Elemento | Quando usar |
|---|---|
| `<header>` | Cabeçalho do site ou de um artigo/seção |
| `<nav>` | Bloco de navegação principal |
| `<main>` | Conteúdo principal e único da página. **Apenas um** por página |
| `<article>` | Conteúdo autocontido que faria sentido isolado (post, notícia, produto, palestrante) |
| `<section>` | Agrupamento temático com título próprio |
| `<aside>` | Conteúdo tangencial (barra lateral, box relacionado) |
| `<footer>` | Rodapé do site ou de um artigo |
| `<figure>` / `<figcaption>` | Ilustração com legenda (detalhado na Aula 04) |
| `<time datetime="">` | Data/hora legível por máquina |
| `<div>` | Só quando não existe elemento semântico adequado — agrupamento puramente visual |

Repare que `<header>` e `<footer>` podem aparecer mais de uma vez: um para o site, outro dentro de cada `<article>`. Só `<main>` é único.

> **💡 Dica**
> Teste da semântica: se você trocar todo o seu CSS por um arquivo vazio, a página ainda faz sentido lida de cima a baixo? Se sim, sua semântica está boa. É exatamente o que um leitor de tela e um buscador "veem".

Para decidir entre `<section>` e `<article>`: pergunte se o trecho faria sentido publicado sozinho, em outro site. Um palestrante com nome, bio e foto, sim → `<article>`. A seção "Sobre o evento" da página inicial só faz sentido dentro dela → `<section>`.

> **🔬 Investigue**
> Crie `exercicios/aula02/minimo.html` contendo **só** a linha `<p>Oi` — sem doctype, sem `<html>`, sem `<body>`, sem fechar o `<p>`. Abra no Live Server e vá à aba **Elements** do DevTools. O navegador construiu `<html>`, `<head>`, `<body>` e fechou o `<p>` sozinho: você está vendo o DOM, não o arquivo. Agora acrescente uma `<table>` com um `<tr>` direto dentro (sem `<tbody>`) e olhe de novo: o `<tbody>` aparece no DOM sem você ter escrito. Quando o JavaScript da Unidade 3 percorrer a árvore, é **essa** árvore que ele vai encontrar.

### Entidades HTML

Alguns caracteres têm significado especial no HTML e precisam ser escapados:

| Caractere | Entidade |
|---|---|
| `<` | `&lt;` |
| `>` | `&gt;` |
| `&` | `&amp;` |
| `"` | `&quot;` |
| espaço fixo (não separável) | `&nbsp;` |
| `©` | `&copy;` |
| `®` | `&reg;` |
| `—` (travessão) | `&mdash;` |

Com `<meta charset="UTF-8">`, acentos, `©` e `—` podem ser digitados diretamente. As entidades que você **precisa** usar são as três primeiras — sem elas, o navegador acha que `<` abre uma tag e `&` inicia uma entidade.

## 8. Validação no W3C

O validador (<https://validator.w3.org/>) é o corretor ortográfico do HTML. Ele compara o seu código com a especificação e lista cada erro com a linha exata. Três formas de usar:

1. **Validate by URI** — para sites já publicados.
2. **Validate by File Upload** — envie o arquivo `.html`.
3. **Validate by Direct Input** — cole o código. É a forma mais rápida durante a aula.

A meta é sempre a mesma mensagem: **"Document checking completed. No errors or warnings to show."**

| Mensagem do validador | O que significa |
|---|---|
| `Stray end tag “p”.` | Um `</p>` sem `<p>` correspondente — geralmente um fechamento duplicado ou cruzado |
| `Unclosed element “ul”.` | Faltou `</ul>` |
| `End tag “strong” violates nesting rules.` | Fechamento cruzado (§1) |
| `Element “ul” not allowed as child of element “ol” in this context.` | Lista aninhada fora do `<li>` (§4) |
| `Element “h2” not allowed as child of element “ul”.` | Só `<li>` pode ser filho direto de lista |
| `Duplicate ID “topo”.` | Dois elementos com o mesmo `id` — âncoras vão quebrar |
| `Consider adding a “lang” attribute to the “html” start tag` | Faltou `lang="pt-BR"` (aviso, mas corrija) |
| `A table row was N columns wide and exceeded the column count` | `colspan`/`rowspan` desbalanceado (§6) |

Erros são listados na ordem em que ocorrem, e **um erro costuma causar vários**: uma tag não fechada no início gera dezenas de mensagens depois. Corrija o primeiro, revalide, repita.

## 💻 Mão na massa — Início, programação e palestrantes do site do evento

Hoje o `index.html` da Aula 01 vira uma página de verdade, e nascem `programacao.html` e `palestrantes.html`. As páginas `inscricao.html` e `contato.html` ganham só o esqueleto — elas são o assunto da Aula 03.

### Passo 1 — O `<head>` completo da página inicial

Abra `site-evento/index.html` e substitua o `<head>`:

`site-evento/index.html` (trecho: `<head>`)

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Semana Acadêmica de Sistemas de Informação da UNEMAT Sinop: três dias de palestras, minicursos e oficinas para estudantes e profissionais de tecnologia.">
  <meta name="author" content="Curso de Sistemas de Informação — UNEMAT Sinop">
  <title>Início — Semana Acadêmica de Sistemas de Informação</title>
</head>
```

O `<title>` segue o padrão "Página — Nome do site": é assim que ele aparece na aba e no histórico.

### Passo 2 — Cabeçalho e navegação

O cabeçalho é **idêntico nas cinco páginas** — é o que faz o site parecer um site. Escreva uma vez, com capricho, e copie nas outras.

`site-evento/index.html` (trecho: início do `<body>`)

```html
<body>
  <header id="topo">
    <h1>Semana Acadêmica de Sistemas de Informação</h1>
    <p>UNEMAT Sinop · três noites de outubro · Auditório Central</p>
    <nav>
      <ul>
        <li><a href="index.html">Início</a></li>
        <li><a href="programacao.html">Programação</a></li>
        <li><a href="inscricao.html">Inscrição</a></li>
        <li><a href="palestrantes.html">Palestrantes</a></li>
        <li><a href="contato.html">Contato</a></li>
      </ul>
    </nav>
  </header>
```

Os cinco `href` são caminhos relativos: todos os arquivos estão na mesma pasta. O `id="topo"` vai servir para os links "voltar ao topo".

### Passo 3 — Conteúdo principal em seções

`site-evento/index.html` (trecho: `<main>`)

```html
  <main>
    <p>Nesta página:</p>
    <ul>
      <li><a href="#sobre">Sobre o evento</a></li>
      <li><a href="#como-participar">Como participar</a></li>
      <li><a href="#glossario">Glossário</a></li>
    </ul>

    <section id="sobre">
      <h2>Sobre o evento</h2>
      <p>
        A Semana Acadêmica de Sistemas de Informação reúne estudantes, professores e
        profissionais de tecnologia da região norte de Mato Grosso em três dias de
        <strong>palestras, minicursos e oficinas práticas</strong>. O evento é
        <em>gratuito</em> e aberto à comunidade.
      </p>
      <p>
        Nesta edição, o tema central é <q>Desenvolvimento web para problemas reais</q>:
        cada atividade parte de um caso concreto — do agronegócio à saúde pública —
        e mostra como HTML, CSS e JavaScript resolvem parte dele.
      </p>
      <p>Emitimos certificado de <strong>20 horas</strong> para quem participar de pelo menos 75% das atividades.</p>
      <p><a href="#topo">Voltar ao topo</a></p>
    </section>

    <section id="como-participar">
      <h2>Como participar</h2>
      <ol>
        <li>Leia a <a href="programacao.html">programação</a> e escolha as atividades.</li>
        <li>Preencha o <a href="inscricao.html">formulário de inscrição</a>.</li>
        <li>Confira o e-mail de confirmação (verifique a caixa de spam).</li>
        <li>No primeiro dia, faça o credenciamento no saguão do auditório a partir das 18h30.</li>
        <li>Participe, assine a lista de presença e receba o certificado por e-mail.</li>
      </ol>
      <p><a href="#topo">Voltar ao topo</a></p>
    </section>

    <section id="glossario">
      <h2>Glossário</h2>
      <dl>
        <dt>Palestra</dt>
        <dd>Apresentação expositiva de 50 minutos, com perguntas ao final.</dd>
        <dt>Minicurso</dt>
        <dd>Atividade prática de 3 horas, com computador, para até 30 participantes.</dd>
        <dt>Oficina</dt>
        <dd>Atividade curta (90 minutos) em que os participantes constroem algo juntos.</dd>
        <dt>Mesa-redonda</dt>
        <dd>Conversa entre três ou quatro convidados mediada por um professor do curso.</dd>
        <dt>Credenciamento</dt>
        <dd>Confirmação de presença e retirada do crachá no primeiro dia.</dd>
      </dl>
      <p><a href="#topo">Voltar ao topo</a></p>
    </section>

    <blockquote cite="https://www.w3.org/">
      <p>A força da Web está em sua universalidade. O acesso por todos, independentemente de deficiência, é um aspecto essencial.</p>
      <footer>— <cite>Tim Berners-Lee</cite>, criador da Web</footer>
    </blockquote>
  </main>
```

Cada `<section>` tem um `<h2>` — regra de ouro: seção sem título provavelmente deveria ser um `<div>`. Os `id` dos `<section>` alimentam a lista "Nesta página" e as âncoras funcionam sem uma linha de CSS ou JavaScript.

### Passo 4 — Rodapé

`site-evento/index.html` (trecho: `<footer>` e fechamento)

```html
  <footer>
    <p>Realização: Curso de Sistemas de Informação — UNEMAT, Campus Sinop.</p>
    <p>
      <a href="mailto:semana.si@unemat.br">semana.si@unemat.br</a> ·
      <a href="tel:+556635111000">(66) 3511-1000</a>
    </p>
    <p>&copy; Curso de Sistemas de Informação &mdash; UNEMAT Sinop. Todos os direitos reservados.</p>
  </footer>
</body>
</html>
```

Salve e olhe o Live Server: uma página sem estilo, mas com estrutura clara. Clique nos links "Nesta página" e "Voltar ao topo" e observe o `#` na URL.

### Passo 5 — A página de programação

Crie `site-evento/programacao.html`. Copie o `<head>` (trocando o `<title>` e a `description`) e o `<header>` inteiro do `index.html`. O `<main>` é uma tabela:

`site-evento/programacao.html`

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Programação completa da Semana Acadêmica de Sistemas de Informação da UNEMAT Sinop: horários, atividades e locais dos três dias.">
  <meta name="author" content="Curso de Sistemas de Informação — UNEMAT Sinop">
  <title>Programação — Semana Acadêmica de Sistemas de Informação</title>
</head>
<body>
  <header id="topo">
    <h1>Semana Acadêmica de Sistemas de Informação</h1>
    <p>UNEMAT Sinop · três noites de outubro · Auditório Central</p>
    <nav>
      <ul>
        <li><a href="index.html">Início</a></li>
        <li><a href="programacao.html">Programação</a></li>
        <li><a href="inscricao.html">Inscrição</a></li>
        <li><a href="palestrantes.html">Palestrantes</a></li>
        <li><a href="contato.html">Contato</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <h2>Programação</h2>
    <p>Todas as atividades acontecem no período noturno. Minicursos exigem inscrição prévia e têm vagas limitadas.</p>

    <table>
      <caption>Programação dos três dias do evento</caption>
      <thead>
        <tr>
          <th scope="col">Horário</th>
          <th scope="col">Atividade</th>
          <th scope="col">Responsável</th>
          <th scope="col">Local</th>
        </tr>
      </thead>
      <tbody id="dia-1">
        <tr>
          <th colspan="4" scope="colgroup">Dia 1</th>
        </tr>
        <tr>
          <th scope="row"><time datetime="18:30">18h30</time></th>
          <td>Credenciamento</td>
          <td>Comissão organizadora</td>
          <td>Saguão</td>
        </tr>
        <tr>
          <th scope="row"><time datetime="19:00">19h00</time></th>
          <td>Abertura e palestra magna: o futuro do desenvolvimento web</td>
          <td>Eduarda Ribeiro</td>
          <td>Auditório Central</td>
        </tr>
        <tr>
          <th scope="row"><time datetime="20:00">20h00</time></th>
          <td>Minicurso: Git e GitHub do zero</td>
          <td>Diego Nascimento</td>
          <td>Laboratório 2</td>
        </tr>
        <tr>
          <th scope="row"><time datetime="21:00">21h00</time></th>
          <td>Dashboards que os produtores realmente usam</td>
          <td>Bruno Takahashi</td>
          <td>Auditório Central</td>
        </tr>
      </tbody>
      <tbody id="dia-2">
        <tr>
          <th colspan="4" scope="colgroup">Dia 2</th>
        </tr>
        <tr>
          <th scope="row"><time datetime="19:00">19h00</time></th>
          <td>Minicurso: acessibilidade na prática</td>
          <td>Diego Nascimento</td>
          <td>Laboratório 1</td>
        </tr>
        <tr>
          <th scope="row"><time datetime="19:00">19h00</time></th>
          <td>Minicurso: primeiros passos com redes neurais</td>
          <td>Ana Lúcia Ferreira</td>
          <td>Laboratório 3</td>
        </tr>
        <tr>
          <th scope="row"><time datetime="20:30">20h30</time></th>
          <td>Segurança em aplicações web: dez erros comuns</td>
          <td>Carla Mendes</td>
          <td>Auditório Central</td>
        </tr>
        <tr>
          <th scope="row"><time datetime="21:30">21h30</time></th>
          <td colspan="3">Confraternização com coffee break — saguão</td>
        </tr>
      </tbody>
      <tbody id="dia-3">
        <tr>
          <th colspan="4" scope="colgroup">Dia 3</th>
        </tr>
        <tr>
          <th scope="row"><time datetime="18:30">18h30</time></th>
          <td>Maratona de programação</td>
          <td>Eduarda Ribeiro</td>
          <td>Laboratórios 1 e 2</td>
        </tr>
        <tr>
          <th scope="row"><time datetime="19:00">19h00</time></th>
          <td>Minicurso: phishing e engenharia social</td>
          <td>Carla Mendes</td>
          <td>Laboratório 3</td>
        </tr>
        <tr>
          <th scope="row"><time datetime="22:00">22h00</time></th>
          <td>Encerramento e premiação</td>
          <td>Eduarda Ribeiro</td>
          <td>Auditório Central</td>
        </tr>
      </tbody>
      <tfoot>
        <tr>
          <td colspan="4">Programação sujeita a alterações. Consulte esta página na véspera de cada dia.</td>
        </tr>
      </tfoot>
    </table>

    <p><a href="#topo">Voltar ao topo</a></p>
  </main>

  <footer>
    <p>Realização: Curso de Sistemas de Informação — UNEMAT, Campus Sinop.</p>
    <p>
      <a href="mailto:semana.si@unemat.br">semana.si@unemat.br</a> ·
      <a href="tel:+556635111000">(66) 3511-1000</a>
    </p>
    <p>&copy; Curso de Sistemas de Informação &mdash; UNEMAT Sinop. Todos os direitos reservados.</p>
  </footer>
</body>
</html>
```

Três detalhes importantes nessa tabela:

- Um `<tbody>` **por dia**, cada um com `id`. Isso permite links diretos como `programacao.html#dia-2` a partir de outras páginas.
- A linha de título de cada dia usa `<th colspan="4">`: uma célula ocupa as quatro colunas. Note que a linha da confraternização tem `<th>` + `<td colspan="3">` — somando 4 de novo.
- O `<tfoot>` carrega a observação final. Sem CSS ele aparece no fim, onde deve.

### Passo 6 — A página de palestrantes

`site-evento/palestrantes.html`

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Conheça os palestrantes e ministrantes da Semana Acadêmica de Sistemas de Informação da UNEMAT Sinop.">
  <meta name="author" content="Curso de Sistemas de Informação — UNEMAT Sinop">
  <title>Palestrantes — Semana Acadêmica de Sistemas de Informação</title>
</head>
<body>
  <header id="topo">
    <h1>Semana Acadêmica de Sistemas de Informação</h1>
    <p>UNEMAT Sinop · três noites de outubro · Auditório Central</p>
    <nav>
      <ul>
        <li><a href="index.html">Início</a></li>
        <li><a href="programacao.html">Programação</a></li>
        <li><a href="inscricao.html">Inscrição</a></li>
        <li><a href="palestrantes.html">Palestrantes</a></li>
        <li><a href="contato.html">Contato</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <h2>Palestrantes e ministrantes</h2>
    <p>Convidados desta edição, em ordem alfabética. Os demais entram na Aula 04, quando a página ganhar fotos.</p>

    <article id="ana-lucia-ferreira">
      <h3>Ana Lúcia Ferreira</h3>
      <p><strong>Professora e pesquisadora</strong> da UNEMAT — Sinop, na área de inteligência artificial.</p>
      <p>Pesquisa redes neurais aplicadas à previsão de safra de soja e coordena um grupo de estudos em aprendizado de máquina.</p>
      <dl>
        <dt>Atividades</dt>
        <dd><a href="programacao.html#dia-2">Minicurso: primeiros passos com redes neurais</a> (dia 2)</dd>
        <dt>Contato</dt>
        <dd><a href="https://www.linkedin.com/" target="_blank" rel="noopener noreferrer">Perfil no LinkedIn</a></dd>
      </dl>
    </article>

    <article id="bruno-takahashi">
      <h3>Bruno Takahashi</h3>
      <p><strong>Cientista de dados</strong> na startup AgroData, especialista em visualização de dados.</p>
      <p>Constrói painéis que produtores rurais realmente usam no dia a dia e escreve sobre dados abertos e cidades inteligentes.</p>
      <dl>
        <dt>Atividades</dt>
        <dd><a href="programacao.html#dia-1">Dashboards que os produtores realmente usam</a> (dia 1)</dd>
        <dd><a href="programacao.html#dia-3">Dados abertos e cidades inteligentes</a> (dia 3)</dd>
        <dt>Contato</dt>
        <dd><a href="https://github.com/" target="_blank" rel="noopener noreferrer">Perfil no GitHub</a></dd>
      </dl>
    </article>

    <article id="carla-mendes">
      <h3>Carla Mendes</h3>
      <p><strong>Pesquisadora em segurança da informação</strong> na UFMT.</p>
      <p>Estuda a relação entre experiência de uso e ataques de engenharia social, e treina equipes de desenvolvimento em segurança.</p>
      <dl>
        <dt>Atividades</dt>
        <dd><a href="programacao.html#dia-2">Segurança em aplicações web: dez erros comuns</a> (dia 2)</dd>
        <dd><a href="programacao.html#dia-3">Minicurso: phishing e engenharia social</a> (dia 3)</dd>
        <dt>Contato</dt>
        <dd><a href="mailto:carla@exemplo.com">carla@exemplo.com</a></dd>
      </dl>
    </article>

    <p><a href="#topo">Voltar ao topo</a></p>
  </main>

  <footer>
    <p>Realização: Curso de Sistemas de Informação — UNEMAT, Campus Sinop.</p>
    <p>
      <a href="mailto:semana.si@unemat.br">semana.si@unemat.br</a> ·
      <a href="tel:+556635111000">(66) 3511-1000</a>
    </p>
    <p>&copy; Curso de Sistemas de Informação &mdash; UNEMAT Sinop. Todos os direitos reservados.</p>
  </footer>
</body>
</html>
```

Cada palestrante é um `<article>`: faria sentido sozinho em outro site. Os títulos são `<h3>` porque estão abaixo do `<h2>` "Palestrantes e ministrantes" — hierarquia respeitada. Os links para `programacao.html#dia-2` combinam caminho relativo com fragmento.

### Passo 7 — Esqueleto das páginas restantes

Para o menu não levar a um `404`, crie `inscricao.html` e `contato.html` com o `<head>`, o `<header>` e o `<footer>` copiados, e um `<main>` mínimo:

`site-evento/inscricao.html` (trecho: `<main>`)

```html
  <main>
    <h2>Inscrição</h2>
    <p>O formulário de inscrição será construído na próxima aula.</p>
  </main>
```

Faça o mesmo em `contato.html`, trocando o título para "Contato". Ajuste o `<title>` e a `description` de cada uma.

### Passo 8 — Validar as cinco páginas

Abra <https://validator.w3.org/#validate_by_input>, cole o código de cada página e corrija até ver **"No errors or warnings to show"**. Faça isso nas cinco. É a última etapa de toda aula da Unidade 1.

### Como testar

- As cinco páginas abrem no Live Server e o menu leva de uma para outra sem `404`.
- Em `index.html`, os links "Nesta página" rolam até a seção e a URL ganha `#sobre`, `#como-participar`, `#glossario`.
- Em `palestrantes.html`, clicar em "Minicurso: primeiros passos com redes neurais" abre `programacao.html` já posicionada no Dia 2.
- Na aba Elements, a tabela mostra três `<tbody>` e um `<tfoot>`; cada `<tr>` soma 4 colunas.
- O validador não acusa nenhum erro em nenhuma das cinco páginas.

**Resultado esperado:** um site de cinco páginas, sem estilo, navegável, com hierarquia de títulos correta, tabela de programação estruturada e zero erros no W3C. Ele parece "feio" — e vai continuar assim até a Aula 05. O que importa agora é a estrutura.

## 🧪 Laboratório

### Nível A — Fixação

Os itens A1 a A6 revisam a arquitetura da Aula 01; os demais são sobre o HTML de hoje.

**A1.** Diferencie as camadas de apresentação, aplicação e dados, dizendo onde cada uma executa.

**A2.** Um blog cujo conteúdo vem de um banco de dados MySQL é estático ou dinâmico? Justifique.

**A3.** Explique a diferença fundamental entre MPA e SPA em uma frase para cada.

**A4.** Qual verbo HTTP você usaria para: (a) listar produtos; (b) cadastrar um cliente; (c) excluir um pedido; (d) atualizar o preço de um item?

**A5.** Classifique cada código como erro de cliente ou de servidor: `403`, `500`, `404`, `502`, `400`, `503`.

**A6.** O que acontece com uma página HTML que não declara `<!DOCTYPE html>`?

**A7.** Corrija os erros do trecho abaixo (há pelo menos quatro):

```html
<p>Texto <strong>importante <em>e enfático</strong></em>.
<a href=programacao.html>Programação</a>
<ul>
  <li>Um
  <li>Dois
</ul>
```

**A8.** Qual a diferença semântica entre `<strong>` e `<b>`? E entre `<em>` e `<i>`?

**A9.** Escreva o HTML de uma lista não ordenada com 3 itens, sendo que o segundo contém uma sublista ordenada com 2 itens.

**A10.** Escreva um link que abra `https://sigaa.unemat.br` em nova aba, com os atributos de segurança corretos.

**A11.** O que faz o atributo `scope` em um `<th>`?

**A12.** Escreva o HTML de uma célula que ocupe 3 colunas e outra que ocupe 2 linhas.

**A13.** Para cada situação, indique o elemento semântico mais adequado: (a) menu principal; (b) uma notícia completa; (c) barra lateral de links relacionados; (d) rodapé com copyright; (e) imagem com legenda; (f) conteúdo principal da página.

**A14.** Por que `<main>` deve aparecer apenas uma vez por página?

**A15.** Escreva as entidades HTML para: `<`, `>`, `&`, `©` e espaço não separável.

**A16.** O que é um elemento vazio? Cite quatro.

### Nível B — Aplicação

**B1.** Crie `exercicios/aula02/curriculo.html` — um currículo pessoal completo usando apenas HTML semântico, sem nenhum CSS. Deve conter: dados pessoais no `<header>`; seções de formação, experiência, habilidades e projetos; listas apropriadas em cada uma (ordenada onde a cronologia importa); uma tabela de idiomas com nível; links para e-mail, telefone, LinkedIn e GitHub; `<footer>`.

**Resultado esperado:** validador do W3C com zero erros; a hierarquia `h1` → `h2` sem pulos; os links `mailto:` e `tel:` funcionando.

<details><summary>Dica</summary>

Use a página de palestrantes como modelo: `<header>` com seu nome no `<h1>`, `<main>` com uma `<section>` por bloco do currículo, `<dl>` para pares como "Período / Instituição". Para a tabela de idiomas, `<th scope="row">` no nome do idioma.
</details>

**B2.** Escreva o HTML (sem CSS) de uma página de notícia com: cabeçalho do site, navegação, artigo com título, subtítulo, data em `<time>`, autor, cinco parágrafos, uma citação em destaque, uma seção de "leia também" em `<aside>` e rodapé do artigo com as tags do assunto.

**Resultado esperado:** um `<article>` com `<header>` e `<footer>` próprios, além do `<header>` e `<footer>` do site; o `<aside>` fora do `<article>`; zero erros no validador.

<details><summary>Dica</summary>

O exemplo da §7 é quase esse esqueleto. O subtítulo da notícia é um `<p>` dentro do `<header>` do artigo, não um `<h2>` — subtítulo jornalístico é descrição, não seção. As tags do assunto cabem em uma `<ul>` dentro do `<footer>` do artigo.
</details>

**B3.** Reproduza em HTML a tabela do cronograma desta disciplina (15 aulas, com data, unidade e tema — está na Aula 01), usando `<caption>`, `<thead>`, `<tbody>` e `<th scope>` corretamente. Mescle células nas linhas de avaliação para indicar "Avaliação — entrega pelo SIGAA".

**Resultado esperado:** uma tabela de 15 linhas de dados, três `<th scope="row">` de avaliação mesclados com `colspan`, e cada linha somando o mesmo número de colunas.

<details><summary>Dica</summary>

Comece pela tabela de programação do Mão na massa: um `<tbody>` por unidade deixa a estrutura mais clara. Nas linhas de avaliação, se a tabela tem 4 colunas e você quer "Data" + "Avaliação — entrega pelo SIGAA", use `<th scope="row">` + `<td colspan="3">`.
</details>

**B4.** Pegue o trecho abaixo (*div soup*) e reescreva-o inteiramente com HTML5 semântico:

```html
<div id="topo">
  <div class="titulo">Blog do Curso</div>
  <div class="menu"><div><a href="#">Home</a></div><div><a href="#">Posts</a></div></div>
</div>
<div id="conteudo">
  <div class="post">
    <div class="titulo-post">Como estudar programação</div>
    <div class="data">19/08/2026</div>
    <div class="texto">Estudar programação exige prática diária e projetos pequenos que cresçam aos poucos.</div>
  </div>
</div>
<div id="rodape">Copyright 2026</div>
```

**Resultado esperado:** zero `<div>` no resultado; `<header>`, `<nav>` com `<ul>`, `<main>`, `<article>` com `<h2>` e `<time datetime>`, `<footer>` com `&copy;`.

<details><summary>Dica</summary>

Cada `class` do original está gritando o nome do elemento semântico: `titulo` → `<h1>`, `menu` → `<nav>`, `post` → `<article>`, `data` → `<time>`. Só o `#` dos links deve virar um caminho real.
</details>

**B5.** Construa um índice navegável: uma página longa com 6 seções, cada uma com `id`, e um menu no topo com links de âncora para cada seção. Ao final de cada seção, inclua um link "voltar ao topo".

**Resultado esperado:** clicar em cada item do menu rola até a seção certa e a URL muda para `#id-da-secao`; "voltar ao topo" funciona em todas.

<details><summary>Dica</summary>

Cada seção precisa de conteúdo suficiente para a página rolar — copie três parágrafos da §1 desta aula em cada uma. Os `id` não podem ter espaços nem acentos e não podem se repetir.
</details>

**B6.** Compare arquiteturas: escolha três sistemas que você usa (por exemplo SIGAA, Instagram e um blog pessoal) e produza uma tabela HTML classificando cada um quanto a: estático/dinâmico, MPA/SPA e quantas camadas você supõe existirem. Justifique cada classificação com uma evidência observável (comportamento ao navegar, aba Network).

**Resultado esperado:** uma `<table>` com `<caption>`, `<thead>` e três linhas de dados, seguida de um parágrafo de justificativa por sistema.

<details><summary>Dica</summary>

Na aba Network, filtre por *Doc*: uma MPA carrega um novo documento HTML a cada clique; uma SPA carrega um documento no início e depois só *Fetch/XHR* com JSON.
</details>

**B7.** Use o validador do W3C em três sites reais e registre quantos erros e avisos cada um apresenta. Escolha um erro de cada site, explique o que significa e como corrigir.

**Resultado esperado:** uma lista com site, número de erros, número de avisos, o texto literal de um erro e a correção proposta.

<details><summary>Dica</summary>

Use *Validate by URI*. Sites grandes costumam ter dezenas de erros — isso não os impede de funcionar (lembre-se do "Você sabia?" da §1), mas mostra por que o validador é um padrão de qualidade e não uma obrigação técnica.
</details>

**B8.** Página institucional do curso. Construa `exercicios/aula02/curso-si.html`, uma página sobre o curso de Sistemas de Informação, contendo obrigatoriamente: estrutura completa do documento com todas as `<meta>` vistas; `<header>` com `<h1>` e `<nav>` com 4 links de âncora interna; `<main>` com três `<section>`, cada uma com `<h2>` e conteúdo; uma lista ordenada com as etapas do ciclo requisição-resposta (Aula 01); uma lista de definições com 5 termos técnicos da Aula 01; uma tabela com a grade de uma fase do curso (disciplina, carga horária, professor); um `<blockquote>` com citação e `<cite>`; `<footer>` com direitos autorais usando `&copy;`.

**Resultado esperado:** zero erros no validador; os 4 links de âncora funcionando; a tabela com `<caption>`, `<thead>` e `<th scope>`.

<details><summary>Dica</summary>

É a mesma receita do `index.html` do evento, com outro conteúdo. Se travar em algum elemento, procure-o na página do site do evento e copie a estrutura.
</details>

### Nível C — Desafio em sala

**C1.** Site institucional de 4 páginas. Construa, em `exercicios/aula02/curso/`, um site sobre o curso de Sistemas de Informação da UNEMAT com quatro páginas interligadas: `index.html` (apresentação), `grade.html` (tabela com a grade curricular completa), `corpo-docente.html` (lista de professores com formação) e `contato.html` (endereço, telefone, e-mail e mapa em link). Requisitos: navegação idêntica em todas as páginas; caminhos relativos corretos; HTML5 semântico; zero erros no validador; nomes de arquivos em minúsculas sem acentos. Sem CSS ainda — este site será estilizado nas Aulas 05 e 06.

<details><summary>Dica</summary>

Faça primeiro o `<header>` com o `<nav>` de 4 links e só depois as páginas — copie o cabeçalho pronto em cada uma. Para a grade curricular, um `<tbody>` por fase, como na programação do evento. O "mapa em link" é um `<a>` para o Google Maps com `target="_blank"` e `rel`.
</details>

## 🏆 Desafios

### ⭐ Caça ao bug: oito erros escondidos
Tags: html, bug, investigacao

O trecho abaixo "funciona" — abre no navegador e mostra tudo. Mesmo assim, ele tem **pelo menos oito problemas**: alguns o validador do W3C encontra, outros só um olho humano treinado percebe. Encontre todos, classifique-os e corrija.

```html
<html>
<head>
  <title>Semana de SI</title>
  <meta charset="UTF-8">
</head>
<body>
  <h1>Semana Acadêmica</h1>
  <h1>Programação</h1>
  <h4>Dia 1</h4>
  <p>Palestra de abertura com <strong>convidada <em>especial</strong></em>.</p>
  <p>Para se inscrever, <a href="inscricao.html" target="_blank">clique aqui</a>.<br><br>
  As vagas são limitadas.</p>
  <ul>
    <li>Minicursos</li>
    <ul>
      <li>HTML e CSS</li>
    </ul>
    <li>Oficinas</li>
  </ul>
  <table>
    <tr><td>Horário</td><td>Atividade</td></tr>
    <tr><td>19h</td><td colspan="3">Abertura</td></tr>
  </table>
</body>
</html>
```

**Critérios de pronto**

- Uma lista numerada com cada problema, a linha em que está e uma classificação: "o validador encontra" ou "só um humano encontra".
- Pelo menos oito problemas listados (há mais — quem achar dez ganha destaque em sala).
- A versão corrigida, validada com zero erros e zero avisos.
- Uma frase explicando por que os problemas que o validador **não** encontra são, ainda assim, problemas.

<details><summary>Pistas</summary>

1. Cole o código como está no validador e leia as mensagens — elas resolvem a primeira metade.
2. Releia a tabela de "Erros comuns" desta aula: cada linha dela é um candidato.
3. Pense em: quantos `<h1>`? Que nível vem depois de `<h1>`? O `<ul>` filho está dentro de um `<li>`? O `target="_blank"` está acompanhado? O texto do link diz para onde vai? A tabela tem cabeçalhos de verdade? E o que falta na primeira linha do arquivo?
4. Conte as colunas da tabela linha a linha.
</details>

### ⭐ Sem mouse, sem CSS
Tags: acessibilidade, html, investigacao

Boa parte das pessoas que usam a Web não usa mouse: quem navega por teclado, quem usa leitor de tela, quem tem lesão por esforço repetitivo. E buscadores não "veem" CSS nenhum. Hoje você vai usar o site do evento (e um site real) do jeito que eles usam — e descobrir se a estrutura que você escreveu se sustenta sozinha.

**Critérios de pronto**

- No `index.html` do site do evento, navegue **só com o teclado** (<kbd>Tab</kbd>, <kbd>Shift</kbd>+<kbd>Tab</kbd>, <kbd>Enter</kbd>): registre a ordem em que os links recebem foco e se algum ficou inalcançável.
- No Firefox, abra um site real (o da UNEMAT ou um jornal), desligue os estilos (*Exibir → Estilo da página → Sem estilo*) e responda: a página ainda faz sentido lida de cima a baixo? Onde a ordem do conteúdo surpreendeu você?
- Um parágrafo comparando as duas experiências e apontando **uma** melhoria concreta que você faria no site real, com o elemento HTML que usaria.
- No site do evento, uma melhoria implementada a partir do que você observou. Sugestão: acrescente `id="conteudo"` ao `<main>` das cinco páginas (ele ainda não tem) e, como primeiro elemento do `<body>`, um link `<a href="#conteudo">Pular para o conteúdo</a>` — sem CSS ele fica visível o tempo todo, e está tudo bem: escondê-lo até receber foco é assunto da Aula 07.

<details><summary>Pistas</summary>

1. A ordem do foco segue a ordem do HTML — não há como mudá-la sem reordenar o código (e é assim que deve ser).
2. No Chrome não há menu "sem estilo", mas a extensão *Web Developer* (Chris Pederick) tem *CSS → Disable All Styles*.
3. Leitores de tela oferecem uma lista só de títulos e outra só de links. Imagine essa lista para a sua página: os textos de link fazem sentido fora de contexto?
4. O link "pular para o conteúdo" é o primeiro elemento do `<body>` em quase todo site bem feito — procure-o com <kbd>Tab</kbd> em <https://developer.mozilla.org/pt-BR/>.
</details>

### ⭐⭐ Documentação técnica dos status HTTP
Tags: html, http, projeto

A tabela de status HTTP da Aula 01 tem cinco linhas. Um desenvolvedor consulta esses códigos toda semana — e a maioria dos sites de referência é em inglês. Produza `http-referencia.html`: uma página que documente os códigos de status HTTP com uma tabela por faixa (1xx a 5xx), com pelo menos 4 códigos por faixa, contendo código, nome em inglês, descrição em português e um exemplo de quando ocorre. Inclua um índice com âncoras internas para cada faixa.

**Critérios de pronto**

- Cinco `<section>`, uma por faixa, cada uma com `<h2>` e `id`, e um índice no topo com âncoras para as cinco.
- Cinco tabelas com `<caption>`, `<thead>`, `<th scope="col">` e pelo menos 4 linhas de dados cada (20 códigos no total).
- Pelo menos um código por faixa que **não** aparece na Aula 01 (por exemplo `418`, `429`, `451`, `307`, `206`).
- Um link "voltar ao índice" ao fim de cada seção.
- Zero erros no validador.

<details><summary>Pistas</summary>

1. A referência completa está em <https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Status> — cada código tem uma página própria com exemplos.
2. O `<th scope="row">` cabe bem no código numérico: ele é o "nome" da linha.
3. Escreva os exemplos com casos que você já viu: `404` ao renomear o `index.html` na Aula 01, `304` no desafio de cache.
4. Esta página vai ganhar CSS na Aula 06 — mantenha-a na pasta `exercicios/`.
</details>

### ⭐⭐ Análise arquitetural de um sistema real
Tags: investigacao, devtools, http

Você aprendeu camadas, MPA/SPA e APIs em teoria. Agora aplique em um sistema que você usa todo dia: escolha um (SIGAA, um e-commerce, uma rede social, um app de banco no navegador) e produza um relatório de 2 páginas com: diagrama da arquitetura provável (camadas e componentes), evidências obtidas na aba Network (formatos de resposta, chamadas de API visíveis, uso de CDN identificável pelos domínios), classificação MPA/SPA justificada, e uma proposta fundamentada de como você reorganizaria a arquitetura se precisasse suportar 10× mais usuários.

**Critérios de pronto**

- Um diagrama (papel, Draw.io ou Excalidraw) com pelo menos três camadas e os componentes que você identificou (CDN, API, servidor de aplicação, banco).
- Pelo menos cinco evidências da aba Network, cada uma com o que foi observado (URL, `Content-Type`, domínio) e o que ela indica.
- A classificação MPA ou SPA com a evidência decisiva (documento novo a cada clique, ou JSON via *Fetch/XHR*).
- A proposta para 10× mais usuários citando pelo menos duas técnicas da §8 e da §12 da Aula 01 (CDN, cache, separação de camadas, balanceamento).

<details><summary>Pistas</summary>

1. Na aba Network, o filtro *Fetch/XHR* mostra as chamadas de API; o filtro *Doc* mostra os documentos HTML. A proporção entre eles já classifica MPA/SPA.
2. Clique com o botão direito no cabeçalho das colunas e ative *Domain*: domínios como `cdn.`, `static.`, `cloudfront.net`, `akamaihd.net` denunciam CDN.
3. Respostas com `Content-Type: application/json` são a camada de aplicação falando; `text/html` é a camada de apresentação sendo entregue.
4. Para "10× mais usuários", pense no que é caro (gerar HTML dinâmico, consultar banco) e no que é barato (servir arquivo estático do cache).
</details>

### ⭐⭐⭐ Reproduza um artigo da Wikipédia só com HTML
Tags: html, acessibilidade, projeto

A Wikipédia é um dos sites mais bem estruturados da Web: sumário com âncoras, infobox em tabela, seções hierárquicas, notas de rodapé com links de ida e volta. Escolha um artigo em português (sugestão: "HTML" ou "Tim Berners-Lee") e reproduza a sua **estrutura** integralmente em HTML semântico, sem uma linha de CSS. Ao final, compare a sua versão com o artigo real de estilos desligados: se ficaram parecidos, você entendeu HTML.

**Critérios de pronto**

- Arquivo único `exercicios/aula02/wikipedia.html` com título, introdução, sumário (`<nav>` com `<ol>` de âncoras, incluindo subitens aninhados), pelo menos 6 seções (`<h2>`) e 4 subseções (`<h3>`).
- A infobox reproduzida como `<table>` com `<caption>` e `<th scope="row">` em cada linha.
- Pelo menos 5 referências: no texto, um link `<a href="#ref-1"><sup>[1]</sup></a>`; na seção "Referências", uma `<ol>` com `id="ref-1"` em cada item e um link de volta ao ponto de citação.
- Um `<blockquote>` com `cite` e pelo menos uma `<figure>` com `<figcaption>` (pode usar uma imagem de <https://commons.wikimedia.org/> com `alt` — a Aula 04 aprofunda).
- Zero erros no validador; navegação completa por teclado; o sumário funcionando.
- Uma comparação escrita (10 linhas) entre a sua página e o artigo real com estilos desligados no Firefox.

<details><summary>Pistas</summary>

1. Abra o artigo real, pressione <kbd>Ctrl</kbd>+<kbd>U</kbd> e estude o código-fonte — ele é enorme, mas procure `<h2>`, `<table class="infobox"` e `<ol class="references"`.
2. Para o link de volta na referência, o ponto de citação precisa de um `id` também: `<sup id="cite-1">` e, na referência, `<a href="#cite-1">↑</a>`.
3. Sumário aninhado: o `<ol>` das subseções vai **dentro** do `<li>` da seção — o mesmo padrão da §4.
4. Faça em etapas: estrutura de títulos → sumário → tabela → referências. Valide a cada etapa; um erro de aninhamento no início gera dezenas de mensagens depois.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| Validador: `End tag “strong” violates nesting rules.` | Fechamento cruzado (`<strong><em></strong></em>`) | Fechar na ordem inversa da abertura |
| Validador: `Element “ul” not allowed as child of element “ul”.` | Lista aninhada colocada fora do `<li>` | O `<ul>` filho vai **dentro** do `<li>` pai |
| Validador: `Duplicate ID “topo”.` e a âncora leva ao lugar errado | Dois elementos com o mesmo `id` | `id` único por página; use nomes descritivos |
| Página cheia de `<h1>` "porque ficou bonito" | Título usado como tamanho de fonte | Um `<h1>` por página; hierarquia sequencial; tamanho é CSS |
| Parágrafos "colados" ou separados com `<br><br>` | `<br>` usado como espaçamento | Um `<p>` por parágrafo; espaçamento é CSS |
| Link abre em nova aba, mas o validador ou o Lighthouse avisa sobre `noopener` | `target="_blank"` sem `rel` | Acrescentar `rel="noopener noreferrer"` |
| Leitor de tela lê "clique aqui, clique aqui, clique aqui" | Texto de link sem significado | Texto que descreve o destino |
| A tabela fica torta, com célula sobrando à direita | `colspan`/`rowspan` desbalanceado | Cada linha deve somar o mesmo número de colunas |
| Âncora `#secao` não rola até o lugar | O `id` de destino não existe, tem grafia diferente ou está com acento | Copiar o `id` exato; sem espaços nem acentos |
| Página inteira de `<div>` | Falta de elementos semânticos | `header`, `nav`, `main`, `section`, `article`, `aside`, `footer` |
| `&` sozinho no texto vira algo estranho ou gera aviso | `&` não escapado | `&amp;` |

## 🏠 Atividade assíncrona (1 h)

**Parte 1 — Leitura (20 min).** SILVA, M. S. *Criando sites com HTML*, capítulos sobre estrutura do documento e elementos de texto. TERUEL, E. C. *HTML5 — Guia Prático*, capítulo introdutório. Anote um elemento HTML que apareceu na leitura e não nesta aula, e pesquise o que ele faz na MDN.

**Parte 2 — Entrega (30 min).** Envie o exercício **B1** (currículo em HTML semântico), em arquivo `.html`, acompanhado de captura de tela do validador W3C mostrando "Document checking completed. No errors or warnings to show."

No **projeto autoral**: replique no seu `meu-projeto/` o que o site do evento ganhou hoje — `index.html` completo (cabeçalho, navegação com as cinco páginas, três seções com `<h2>`, uma lista ordenada, uma lista de definições, um `<blockquote>`, rodapé), mais uma página com uma tabela de dados do seu domínio e uma página com `<article>` por item (o equivalente aos palestrantes). Inclua o `.zip` da pasta na entrega.

**Parte 3 — Fórum (10 min).** Poste no fórum "Semântica importa": encontre um site real com problemas de semântica (uso excessivo de `div`, títulos fora de ordem, links "clique aqui") e descreva três problemas encontrados com a correção proposta para cada. Comente a postagem de um colega.

**Critério de pronto:** o currículo e as três páginas do projeto autoral passam no validador com zero erros; a navegação do projeto autoral não leva a nenhum `404`.

**Entrega:** `curriculo.html`, a captura do validador e o `.zip` de `meu-projeto/`, pelo SIGAA.

## ✅ Checkpoint do projeto

Ao fim desta aula, em `site-evento/`:

- [ ] `index.html` com `<head>` completo (charset, viewport, description, author, title) e `<header>` com `<h1>` e `<nav>` de cinco links.
- [ ] `index.html` com três `<section>` (`#sobre`, `#como-participar`, `#glossario`), uma `<ol>`, uma `<dl>`, um `<blockquote>` com `<cite>` e um `<footer>` com `mailto:`, `tel:` e `&copy;`.
- [ ] `programacao.html` com tabela completa: `<caption>`, `<thead>`, três `<tbody>` com `id`, `<tfoot>`, `th scope` e `colspan`.
- [ ] `palestrantes.html` com um `<article>` por palestrante, `<h3>` abaixo do `<h2>`, `<dl>` de atividades e links para `programacao.html#dia-N`.
- [ ] `inscricao.html` e `contato.html` com cabeçalho, navegação e rodapé idênticos e `<main>` mínimo.
- [ ] As cinco páginas com zero erros no validador do W3C.
- [ ] Em `meu-projeto/`: o mesmo avanço com o seu tema (feito na atividade assíncrona).

## 📚 Para aprofundar

- MDN — Estruturando conteúdo com HTML (curso, em português): <https://developer.mozilla.org/pt-BR/docs/Learn_web_development/Core/Structuring_content> — os módulos "Estrutura básica", "Títulos e parágrafos", "Links" e "Tabelas" cobrem exatamente esta aula.
- MDN — Referência de elementos HTML: <https://developer.mozilla.org/pt-BR/docs/Web/HTML/Element> — consulte quando tiver dúvida sobre qualquer tag.
- MDN — O elemento `<table>`: <https://developer.mozilla.org/pt-BR/docs/Web/HTML/Element/table> — leia a seção de acessibilidade.
- MDN — O elemento `<a>`: <https://developer.mozilla.org/pt-BR/docs/Web/HTML/Element/a> — todos os valores de `rel` e `target`.
- web.dev — Learn HTML (em inglês): <https://web.dev/learn/html> — os capítulos "Document structure", "Semantic HTML", "Headings and sections", "Links" e "Tables".
- Validador do W3C: <https://validator.w3.org/> — use em toda página, sempre.
- WHATWG — HTML Living Standard (em inglês, referência): <https://html.spec.whatwg.org/multipage/> — a seção "Optional tags" explica o "Você sabia?" da §1.
- SILVA, Maurício Samy. *Criando sites com HTML: sites de alta qualidade com HTML e CSS*. Novatec, 2008 — capítulos 2 a 5.
- TERUEL, Evandro C. *HTML 5 — Guia Prático*. Saraiva, 2014 — capítulos sobre estrutura e texto (Minha Biblioteca).
- MILETTO, Evandro M.; BERTAGNOLLI, Silvia C. *Desenvolvimento de software II*. Bookman, 2014 — capítulo sobre arquitetura de aplicações web (para os itens A1–A6).
- W3C — HTML 5.2 Recommendation: <https://www.w3.org/TR/html52/> — seções de elementos de seccionamento e conteúdo de texto.

Na próxima aula, a página de inscrição deixa de ser um esqueleto: você vai aprender o elemento `<form>`, os tipos de `<input>`, rótulos, agrupamento, validação nativa e a diferença entre GET e POST — e vai ver, na aba Network, os dados do formulário viajando até o servidor.
