# Aula 05 — Elementos HTML para layout e introdução ao CSS

> **Nível 1 — Introdução ao Desenvolvimento Web** · Unidade 1: Arquitetura da Web e HTML
> WebLab · curso aberto de desenvolvimento web
> **Tempo estimado:** 3 blocos de 50 min + 1 h de prática

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Estruturar uma página com os elementos de seccionamento do HTML5 (`header`, `nav`, `main`, `section`, `article`, `aside`, `footer`) e decidir quando `div` é a escolha certa.
- Aplicar o padrão de contêiner centralizado que sustenta praticamente todo site profissional.
- Explicar o que é CSS, como o navegador o aplica e o que são seletor, declaração e regra.
- Usar as três formas de aplicação de estilo e justificar por que o CSS externo é a única aceita nos trabalhos desta trilha.
- Calcular o tamanho de uma caixa no modelo de caixa e explicar por que todo projeto começa com `box-sizing: border-box`.
- Diferenciar os valores de `display` (`block`, `inline`, `inline-block`, `none`) e seu efeito no fluxo do documento.
- Reconhecer o colapso de margens e prever o espaço real entre dois elementos.

## 📋 Pré-requisitos

- [ ] As cinco páginas do site do evento (`index.html`, `programacao.html`, `inscricao.html`, `palestrantes.html`, `contato.html`) validando com zero erros no W3C.
- [ ] VS Code com Live Server e DevTools abertos na aba **Elements** — hoje você usará muito o painel **Styles** e a aba **Computed**.
- [ ] Revisar da Aula 02 a estrutura mínima de um documento (`<!DOCTYPE html>`, `lang`, `charset`, `viewport`).

> Na Aula 04 você terminou o conteúdo das páginas do evento: listas, imagens otimizadas, vídeo com legenda e mapa incorporado. O site está completo em informação — e cru em aparência. Antes de estilizar, porém, a página precisa de um **esqueleto correto**: é sobre ele que o CSS vai trabalhar. Hoje você organiza esse esqueleto com os elementos de seccionamento, escreve a primeira folha de estilo e entende a regra que resolve a maior parte dos problemas de layout: o modelo de caixa. Esta aula fecha a Unidade 1.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Elementos de seccionamento, `section` × `article` × `div`, padrão de contêiner centralizado, diagnóstico no console |
| 2 | 50 min | O que é CSS, sintaxe, três formas de aplicação, como o navegador monta a página, primeiras regras |
| 3 | 50 min | Box model, `box-sizing`, shorthand, colapso de margens, `display`; Mão na massa: esqueleto das cinco páginas e `css/estilo.css` |

## 1. Elementos HTML para layout

Até a Aula 02 você usou `<header>`, `<nav>`, `<main>` e `<footer>` como "as partes da página". Hoje você entende o que cada um **significa** — e por que essa escolha muda o que o leitor de tela anuncia, o que o buscador indexa e como o CSS vai se apoiar na estrutura.

### 1.1 O esqueleto de uma página

**`index.html` (esqueleto)**

```html
<body>
  <header id="topo">
    <img src="img/logo-sasi.svg" alt="" width="160" height="48">
    <h1>Semana Acadêmica de Sistemas de Informação</h1>
    <p>Três noites de outubro · Auditório Central</p>
    <nav aria-label="Principal">
      <ul>
        <li><a href="index.html" aria-current="page">Início</a></li>
        <li><a href="programacao.html">Programação</a></li>
        <li><a href="inscricao.html">Inscrição</a></li>
        <li><a href="palestrantes.html">Palestrantes</a></li>
        <li><a href="contato.html">Contato</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <section class="hero">
      <h2>Três noites de palestras, minicursos e maratona de programação</h2>
      <p>Participação gratuita, com certificado para quem comparecer.</p>
    </section>

    <section class="destaques">
      <h2>Destaques</h2>
      <article class="cartao">
        <h3>Minicurso de Git e GitHub</h3>
        <p>Do primeiro commit ao pull request, em duas horas.</p>
      </article>
      <article class="cartao">
        <h3>Maratona de programação</h3>
        <p>Equipes de três, problemas de lógica, premiação no encerramento.</p>
      </article>
    </section>
  </main>

  <aside>
    <h2>Edições anteriores</h2>
    <p>Veja a galeria e os vídeos das edições passadas.</p>
  </aside>

  <footer>
    <p>Realização: Comissão Organizadora da Semana Acadêmica de Sistemas de Informação.</p>
    <p>
      <a href="mailto:contato@semanasi.com.br">contato@semanasi.com.br</a> ·
      <a href="tel:+556635111000">(66) 3511-1000</a>
    </p>
    <p>&copy; Semana Acadêmica de Sistemas de Informação. Todos os direitos reservados.</p>
  </footer>
</body>
```

O `<h1>` continua no `<header>`, como na Aula 02: ele nomeia **o site**, é o mesmo nas cinco páginas, e o título de cada página é o `<h2>` do topo do `<main>`. Só na Aula 07, quando o site for redesenhado, o `<h1>` desce para dentro do `<main>`.

| Elemento | Papel | Quantidade por página |
|---|---|---|
| `<header>` | Cabeçalho da página **ou** de uma seção (logo, título, menu) | Vários (um por contexto) |
| `<nav>` | Bloco de navegação principal | 1 a 3, sempre rotulados com `aria-label` |
| `<main>` | Conteúdo único e central da página — o que muda de uma página para outra | **Exatamente 1** |
| `<section>` | Agrupamento temático **com título** | Vários |
| `<article>` | Conteúdo autocontido, que faz sentido isolado (notícia, cartão, comentário, produto) | Vários |
| `<aside>` | Conteúdo tangencial (barra lateral, links relacionados, propaganda) | Vários |
| `<footer>` | Rodapé da página ou de uma seção | Vários |
| `<div>` | **Sem significado** — só agrupa para estilo | Quando nenhum outro serve |

Esses elementos são chamados de **marcos** (*landmarks*): o leitor de tela oferece um atalho para pular direto entre eles ("ir para o conteúdo principal", "ir para a navegação"). Uma página feita só de `<div>` não tem marcos — a pessoa cega precisa ouvir tudo, do topo, sempre.

### 1.2 `section` × `article` × `div`: a pergunta certa

A dúvida mais comum desta aula é "isso é uma `section` ou um `article`?". Três perguntas resolvem:

1. **Faz sentido sozinho, fora desta página?** Uma notícia, um cartão de palestrante, um comentário, um produto — se você conseguiria distribuí-lo por RSS ou compartilhar isoladamente, é `<article>`.
2. **É um agrupamento temático com título, que só faz sentido dentro desta página?** "Destaques", "Programação do primeiro dia", "Perguntas frequentes" — é `<section>`. Uma `<section>` sem título é sinal de que você queria uma `<div>`.
3. **Não tem significado nenhum — existe só para agrupar por estilo?** Um contêiner para centralizar, um invólucro para aplicar um fundo — é `<div>`.

> **💡 Dica**
> `div` não é proibida — é a **última** opção. Precisa de um contêiner só para centralizar o conteúdo com `max-width`? `div` é a escolha certa. Precisa marcar o rodapé? Use `footer`. A pergunta a fazer é sempre: "existe um elemento que descreva o que isto **é**?" Se existe, use-o. Se não existe, `div`.

Um `<article>` pode ter seu próprio `<header>` e `<footer>` — e é comum:

```html
<article class="cartao">
  <header>
    <h3>Minicurso de Git e GitHub</h3>
    <p><time datetime="19:30">19h30</time> · Laboratório 2 · 40 vagas</p>
  </header>
  <p>Do primeiro commit ao pull request, em duas horas.</p>
  <footer>
    <a href="inscricao.html">Inscrever-se</a>
  </footer>
</article>
```

O `<header>` de dentro do `<article>` não é o cabeçalho da página — é o cabeçalho **daquele** artigo. O leitor de tela entende a diferença pelo contexto.

### 1.3 Mais de um `<nav>`

Uma página pode ter navegação principal, um menu de rodapé e a "trilha de migalhas" (breadcrumb). Todos são `<nav>`; o que os diferencia é o `aria-label`:

```html
<nav aria-label="Principal">
  <ul>
    <li><a href="index.html">Início</a></li>
    <li><a href="programacao.html">Programação</a></li>
  </ul>
</nav>

<nav aria-label="Você está em">
  <ol>
    <li><a href="index.html">Início</a></li>
    <li><a href="programacao.html">Programação</a></li>
    <li aria-current="page">Primeiro dia</li>
  </ol>
</nav>

<footer>
  <nav aria-label="Rodapé">
    <ul>
      <li><a href="contato.html">Contato</a></li>
      <li><a href="privacidade.html">Política de privacidade</a></li>
    </ul>
  </nav>
</footer>
```

Sem o rótulo, o leitor de tela anuncia três vezes "navegação" e a pessoa não sabe qual é qual.

### 1.4 O padrão de contêiner centralizado

Abra qualquer site profissional: o cabeçalho tem uma cor de fundo que vai de uma borda à outra da janela, mas o **conteúdo** (logo, menu) fica limitado a uma faixa central. Esse é o padrão de contêiner centralizado, e ele combina um elemento semântico de largura total com uma `div` interna que limita e centraliza:

**`index.html` (trecho)**

```html
<header id="topo">
  <div class="container">
    <img src="img/logo-sasi.svg" alt="" width="160" height="48">
    <h1>Semana Acadêmica de Sistemas de Informação</h1>
    <nav aria-label="Principal">
      <ul>
        <li><a href="index.html" aria-current="page">Início</a></li>
        <li><a href="programacao.html">Programação</a></li>
      </ul>
    </nav>
  </div>
</header>
```

**`css/estilo.css` (trecho)**

```css
.container {
  width: 100%;
  max-width: 1100px;
  margin-inline: auto;
  padding-inline: 1rem;
}
```

Leia a regra assim: "ocupe toda a largura disponível, mas nunca passe de 1100 px; as margens laterais automáticas dividem a sobra igualmente, centralizando; e sempre reserve 1 rem de respiro de cada lado". Em um monitor largo, o conteúdo para em 1100 px; em um celular, ocupa toda a largura menos o respiro. **Esse número, 1100 px, é o do projeto e não muda mais** — nas Aulas 06 e 07 ele vira a variável `--largura-max`. O elemento semântico (`<header>`) continua ocupando 100% — útil para a cor de fundo que sangra até as bordas.

Esse é o esqueleto de praticamente todo site que você já visitou. Guarde-o: você o usará em todas as páginas hoje e em todos os projetos da trilha.

> **🔬 Investigue**
> Abra `index.html` no Live Server, pressione <kbd>F12</kbd>, vá à aba **Console** e cole o comando abaixo. Ele desenha um contorno vermelho translúcido em **todos** os elementos da página — você enxerga a caixa de cada um e percebe na hora onde há `div` demais, `section` sem título ou conteúdo fora do `<main>`.
>
> ```js
> document.querySelectorAll("*").forEach(el =>
>   el.style.outline = "1px solid rgba(255, 0, 0, 0.3)"
> );
> ```
>
> Depois, na aba **Elements**, clique com o botão direito no `<body>` e escolha **Expand recursively**: a árvore inteira se abre e você vê a hierarquia dos marcos. Recarregue a página para tirar os contornos.

> **🧠 Você sabia?**
> Antes do HTML5, todo site era feito de `<div id="header">`, `<div id="nav">`, `<div id="footer">`. Os nomes dos elementos de seccionamento não foram inventados por um comitê: o grupo de trabalho analisou **mais de um bilhão de páginas** indexadas pelo Google e descobriu quais eram os `id` e `class` mais usados pelos desenvolvedores. `header`, `footer`, `nav`, `content` e `sidebar` estavam no topo — e viraram `<header>`, `<footer>`, `<nav>`, `<main>` e `<aside>`. O HTML5 padronizou o que a comunidade já fazia por convenção.

## 2. O que é CSS

**CSS** (*Cascading Style Sheets*, folhas de estilo em cascata) é a linguagem que descreve **como** o conteúdo estruturado pelo HTML deve ser apresentado. O HTML responde "o que é isso?" (um título, uma lista, um formulário); o CSS responde "com que aparência?" (azul, 2 rem, centralizado, com sombra).

A separação é deliberada e vale ouro: o mesmo HTML pode ganhar dez aparências diferentes trocando só o CSS, e o mesmo CSS serve a cem páginas. É por isso que o Marco 1 fecha **sem CSS** e o Marco 2 estiliza **o mesmo site**: a estrutura e a apresentação são trabalhos diferentes.

### 2.1 Sintaxe

```css
seletor {
  propriedade: valor;
  outra-propriedade: outro-valor;
}
```

Um exemplo real:

```css
h1 {
  color: #0b3d5c;
  font-size: 2rem;
  margin-bottom: 16px;
}
```

| Termo | O que é | No exemplo |
|---|---|---|
| Seletor | Quem recebe o estilo | `h1` (todos os `<h1>` da página) |
| Declaração | Um par `propriedade: valor;` | `color: #0b3d5c;` |
| Bloco de declarações | Tudo entre as chaves | as três declarações |
| Regra | Seletor + bloco | o exemplo inteiro |

Regras de escrita que evitam metade dos erros da aula:

- Toda declaração termina com `;`. Sem ele, o navegador **junta** a declaração com a próxima e ignora as duas.
- Propriedades e valores são em minúsculas; nomes compostos usam hífen (`font-size`, não `fontSize`).
- Comentários são `/* assim */`. **Não existe** comentário de uma linha (`//`) em CSS — se você escrever `//`, a regra seguinte quebra em silêncio.
- Espaços e quebras de linha são livres: `h1{color:red}` e o bloco acima são idênticos para o navegador. Escreva para humanos.

### 2.2 Como o navegador aplica o CSS

> **🔎 Por baixo do capô**
> Quando a página carrega, o navegador faz três coisas em sequência: (1) lê o HTML e monta a **árvore DOM** (a estrutura de elementos que você vê na aba Elements); (2) lê o CSS e monta a **CSSOM**, a árvore de regras; (3) combina as duas na **árvore de renderização**, calculando para cada elemento quais regras se aplicam e qual é o valor final de cada propriedade — é isso que a aba **Computed** do DevTools mostra. Só então ele calcula posições e tamanhos (*layout*) e pinta os pixels (*paint*). Por isso um CSS externo referenciado no `<head>` **bloqueia** a renderização até ser baixado: o navegador se recusa a mostrar a página com a aparência errada e depois "piscar" para a certa.

Você vai ver esse fluxo na prática na Aula 09, quando medir o custo de animações. Por ora, o que importa: o CSS não "pinta por cima" do HTML — ele participa da construção da página desde o início.

### 2.3 Um pouco de história

> **🧠 Você sabia?**
> Nos primeiros anos da Web, quem decidia a aparência de uma página era o **navegador**, não o autor. Um `<h1>` era grande e em negrito porque o Mosaic decidiu assim. Quando o CSS foi proposto — por Håkon Wium Lie, que trabalhava com Tim Berners-Lee no CERN — a ideia central não era dar poder total ao autor, e sim criar uma **cascata**: o estilo final resulta da combinação entre o que o navegador sugere, o que o usuário prefere e o que o autor define. Essa ideia continua viva: se um usuário com baixa visão aumenta o tamanho da fonte no navegador, um site feito com `rem` respeita a escolha. Um site feito com `px` a ignora. O "C" de CSS existe para proteger o usuário.

## 3. As três formas de aplicar CSS

### 3.1 Inline — evite

```html
<p style="color: red; font-size: 18px;">Texto</p>
```

Problemas: mistura conteúdo com apresentação, não é reaproveitável (cada parágrafo precisa repetir o estilo), tem prioridade altíssima (difícil de sobrescrever — você verá o porquê na Aula 06) e polui o HTML. Uso legítimo: quando o valor é **gerado dinamicamente por JavaScript** — uma barra de progresso cuja largura muda a cada segundo, por exemplo.

### 3.2 Interna (`<style>` no `<head>`) — só para testes

```html
<head>
  <meta charset="UTF-8">
  <title>Protótipo</title>
  <style>
    body { font-family: sans-serif; }
    h1 { color: #0b3d5c; }
  </style>
</head>
```

Vale para protótipos rápidos, exemplos de aula e páginas únicas que nunca terão uma segunda. Não é reaproveitável entre páginas nem cacheável.

### 3.3 Externa — a forma correta

**`index.html` (no `<head>`)**

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Semana Acadêmica de Sistemas de Informação</title>
  <link rel="stylesheet" href="css/estilo.css">
</head>
```

**`css/estilo.css`**

```css
body {
  font-family: sans-serif;
}

h1 {
  color: #0b3d5c;
}
```

Vantagens:

- **Um arquivo serve o site inteiro.** Mudou a cor do título? Mudou nas cinco páginas.
- **Cache.** O navegador baixa `estilo.css` uma vez e reaproveita nas outras páginas — a segunda página abre mais rápido.
- **Separação de responsabilidades.** HTML descreve; CSS apresenta; na Unidade 3, JavaScript comporta.
- **Trabalho em equipe.** Uma pessoa mexe no conteúdo enquanto outra mexe no estilo, sem conflito.

Todos os trabalhos desta trilha usam CSS externo. O `href` segue as mesmas regras de caminho relativo dos links e imagens (Aula 02): `css/estilo.css` está na pasta `css`, ao lado do HTML.

> **⚠️ Atenção**
> Uma página pode ter vários `<link rel="stylesheet">`. Eles são aplicados **na ordem em que aparecem**: quando duas regras iguais conflitam, a do arquivo que veio por último vence. Guarde isso — é a terceira etapa da cascata, que você formaliza na Aula 06.

## 4. O modelo de caixa (box model)

Todo elemento HTML é uma **caixa retangular**. Não importa se é um título, uma imagem, um link ou um `<span>` no meio de uma frase: para o navegador, é um retângulo com quatro camadas. Entender isso resolve 80% dos problemas de layout que você vai encontrar.

```text
┌───────────────────────────────────────────────┐
│                    MARGIN                     │   espaço EXTERNO (transparente)
│   ┌───────────────────────────────────────┐   │
│   │                BORDER                 │   │   a borda
│   │   ┌───────────────────────────────┐   │   │
│   │   │            PADDING            │   │   │   espaço INTERNO (recebe o fundo)
│   │   │   ┌───────────────────────┐   │   │   │
│   │   │   │        CONTENT        │   │   │   │   width × height
│   │   │   │                       │   │   │   │
│   │   │   └───────────────────────┘   │   │   │
│   │   └───────────────────────────────┘   │   │
│   └───────────────────────────────────────┘   │
└───────────────────────────────────────────────┘
```

| Camada | O que é | Recebe a cor de fundo? |
|---|---|---|
| Content | O conteúdo em si: texto, imagem, filhos | Sim |
| Padding | Espaço entre o conteúdo e a borda | Sim |
| Border | A linha ao redor | Tem cor própria |
| Margin | Espaço entre esta caixa e as vizinhas | Não (sempre transparente) |

```css
.caixa {
  width: 300px;
  height: 150px;
  padding: 20px;
  border: 5px solid #0b3d5c;
  margin: 30px;
  background-color: #f0f3f6;   /* pinta content + padding, não a margem */
}
```

### 4.1 `box-sizing` — a configuração que muda tudo

Pergunta: quantos pixels de largura a `.caixa` acima ocupa na tela?

Com o comportamento padrão, chamado `content-box`, `width` define só o **conteúdo**. O padding e a borda são somados **por fora**:

```text
300 (width) + 20 + 20 (padding) + 5 + 5 (border) = 350 px de largura ocupada
```

Você pediu 300 px e recebeu 350. Em um layout de duas colunas de `50%` cada, basta um padding para a segunda coluna não caber e cair para a linha de baixo. Isso quebra layouts em porcentagem **constantemente**.

Com `border-box`, `width` passa a incluir padding e borda: a caixa ocupa exatamente 300 px, e o conteúdo fica com o que sobra (250 px). É como você pensa intuitivamente — "quero uma caixa de 300" — e é assim que todo projeto profissional trabalha. Por isso todo CSS desta trilha começa com este reset:

**`css/estilo.css` (topo do arquivo)**

```css
/* 1. Reset e box-sizing */
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
```

Leia: "todo elemento (`*`), inclusive os pseudoelementos `::before` e `::after` (Aula 06), usa `border-box` e começa sem margem nem padding". O zerar de margens tira os espaçamentos padrão do navegador (os `<h1>` e `<p>` vêm com margens que variam entre navegadores) para que **você** decida cada espaço.

> **🔬 Investigue**
> No DevTools, aba **Elements**, selecione qualquer elemento e olhe o painel **Styles**: role até o fim e você verá o diagrama do box model daquele elemento, com os valores de margin, border, padding e content. Passe o mouse sobre cada camada — o navegador destaca a área correspondente na página em cores diferentes (laranja para margem, verde para padding, azul para conteúdo). Agora, na aba **Computed**, procure `box-sizing`: aplique o reset acima e veja o valor mudar de `content-box` para `border-box` — e a largura ocupada cair de 350 para 300.

### 4.2 Notação abreviada (shorthand)

`margin` e `padding` aceitam de um a quatro valores, sempre no **sentido horário** a partir do topo:

```css
margin: 10px;                    /* todos os lados */
margin: 10px 20px;               /* vertical | horizontal */
margin: 10px 20px 30px;          /* topo | horizontal | base */
margin: 10px 20px 30px 40px;     /* topo | direita | base | esquerda (sentido horário) */

margin: 0 auto;                  /* centraliza horizontalmente um bloco COM width definida */

padding-top: 10px;               /* um lado só */
margin-inline: auto;             /* esquerda + direita (equivale a margin-left + margin-right) */
margin-block: 2rem;              /* topo + base */
```

`margin: 0 auto` é o truque clássico de centralização: as margens laterais automáticas dividem igualmente o espaço que sobra. Só funciona quando o elemento é de bloco **e** tem largura menor que o pai — se ocupar 100%, não sobra nada para dividir. A versão moderna, `margin-inline: auto`, foi a que você usou no `.container`.

### 4.3 Colapso de margens

Margens **verticais** adjacentes entre elementos irmãos não se somam: prevalece a **maior**.

```css
.a { margin-bottom: 30px; }
.b { margin-top: 20px; }
/* O espaço entre .a e .b é 30px, não 50px */
```

Isso é comportamento especificado, não bug — existe desde os primeiros dias do CSS para que parágrafos com `margin: 1em 0` fiquem espaçados por 1em, e não por 2em. Três regras para não se surpreender:

1. Só acontece com margens **verticais** (topo e base). Margens horizontais sempre se somam.
2. Acontece também entre pai e primeiro/último filho: a `margin-top` do primeiro `<p>` dentro de uma `<section>` sem padding nem borda "vaza" para fora da seção.
3. **Não** acontece em Flexbox nem em Grid (Aula 07) — o que é um dos motivos de esses modelos serem mais previsíveis.

### 4.4 Bordas

```css
border: 2px solid #333;          /* largura | estilo | cor */
border-bottom: 3px dashed red;   /* um lado só */
border-radius: 8px;              /* cantos arredondados */
border-radius: 50%;              /* círculo perfeito, se a caixa for quadrada */
```

Estilos disponíveis: `solid`, `dashed`, `dotted`, `double`, `none`. A borda só aparece se os **três** valores estiverem presentes (uma borda sem estilo é invisível — erro frequente).

### 4.5 Outros ajustes da caixa

```css
.foto-palestrante {
  width: 100%;          /* ocupa toda a largura do pai */
  max-width: 400px;     /* mas nunca passa de 400 px */
  height: auto;         /* mantém a proporção */
}

.resumo {
  max-width: 65ch;      /* no máximo 65 caracteres por linha: legibilidade */
  min-height: 120px;    /* nunca menor que isso, mesmo com pouco texto */
}

.cartao {
  overflow: hidden;     /* corta o que passar da caixa (auto: barra de rolagem; visible: vaza) */
}
```

`max-width` é mais útil que `width` na maior parte dos casos: define um teto e deixa o elemento encolher em telas pequenas. Você usará isso o tempo todo na Aula 08.

## 5. `display`: como a caixa se comporta no fluxo

O HTML renderiza os elementos em **fluxo normal**: de cima para baixo, da esquerda para a direita. A propriedade `display` define como cada caixa participa desse fluxo.

```css
display: block;          /* ocupa toda a largura disponível, aceita width/height. Padrão de div, p, h1, section, ul */
display: inline;         /* ocupa só o necessário, na linha do texto. IGNORA width/height e margens verticais. Padrão de span, a, strong, em */
display: inline-block;   /* fica na linha do texto, MAS aceita width/height e margens verticais */
display: none;           /* remove do fluxo — não ocupa espaço, como se não existisse */
display: flex;           /* Aula 07 */
display: grid;           /* Aula 07 */
```

| Valor | Quebra linha? | Aceita `width`/`height`? | Exemplos padrão |
|---|---|---|---|
| `block` | Sim, antes e depois | Sim | `div`, `p`, `h1`, `ul`, `section` |
| `inline` | Não | **Não** | `span`, `a`, `strong`, `em`, `code` |
| `inline-block` | Não | Sim | `img`, `button`, `input`, `select` |
| `none` | Some | — | `<template>`, elementos com `hidden` |

O caso clássico: você quer um `<a>` que pareça um botão, com 200 px de largura e padding vertical. Como `<a>` é `inline`, `width` e `margin-top` são ignorados. Solução: `display: inline-block` — o link continua na linha (pode ficar ao lado de outro) e passa a aceitar dimensões.

```css
.botao {
  display: inline-block;
  width: 200px;
  padding: 12px 0;
  text-align: center;
  background-color: #0b3d5c;
  color: #fff;
}
```

### 5.1 Três formas de "esconder", três resultados diferentes

| Propriedade | Ocupa espaço | Clicável | Lido por leitor de tela |
|---|---|---|---|
| `display: none` | Não | Não | Não |
| `visibility: hidden` | Sim | Não | Não |
| `opacity: 0` | Sim | **Sim** | **Sim** |

Escolha pela intenção: `display: none` para remover de verdade (um menu fechado); `visibility: hidden` para reservar o lugar (um placeholder que vai aparecer); `opacity: 0` **só** para animações de aparecer/desaparecer (Aula 09) — porque um botão com `opacity: 0` continua clicável e continua sendo lido, e isso é um bug de acessibilidade quando não é intencional. O atributo HTML `hidden` equivale a `display: none`.

## 6. Um gostinho do que vem: herança, estados e variáveis

Para o Laboratório de hoje você precisa de três ideias que a Aula 06 aprofunda. Aqui vai o mínimo para usá-las.

### 6.1 Algumas propriedades são herdadas

```css
body {
  font-family: "Segoe UI", Roboto, Arial, sans-serif;
  color: #333;
  line-height: 1.6;
}
/* Todo o site herda a fonte, a cor e a altura de linha — escreva uma vez, vale para tudo */
```

| Herdadas (passam de pai para filho) | Não herdadas (cada elemento define a sua) |
|---|---|
| `color`, `font-family`, `font-size`, `font-weight` | `margin`, `padding`, `border` |
| `line-height`, `text-align`, `letter-spacing` | `width`, `height`, `background` |
| `visibility`, `cursor`, `list-style` | `display`, `position`, `overflow` |

A lógica: propriedades de **texto** são herdadas (faz sentido que o parágrafo tenha a fonte do `body`); propriedades de **caixa** não são (não faz sentido que todo filho de uma caixa com borda ganhe borda).

### 6.2 Estados com `:hover` e `:focus`

Um seletor pode mirar um **estado** do elemento — mouse por cima, foco pelo teclado — com as pseudoclasses:

```css
.botao:hover {
  background-color: #1a7fb5;   /* mouse por cima */
}

.botao:focus-visible {
  outline: 3px solid #f0a500;  /* foco visível pelo teclado */
  outline-offset: 2px;
}
```

> **⚠️ Atenção**
> Nunca escreva `outline: none` sem colocar outro indicador no lugar. Quem navega pelo teclado (por deficiência motora, por preferência ou porque o mouse quebrou) depende do contorno de foco para saber onde está. Um site sem foco visível é **inutilizável** por teclado — não importa quão bonito ele pareça.

### 6.3 Variáveis CSS

Em vez de repetir `#0b3d5c` em vinte lugares, declare uma vez e reutilize:

```css
:root {
  --cor-primaria: #0b3d5c;
  --cor-secundaria: #1a7fb5;
  --espaco: 16px;
}

.botao {
  background-color: var(--cor-primaria);
  padding: var(--espaco);
}

.botao:hover {
  background-color: var(--cor-secundaria);
}
```

`:root` é o `<html>`; declarar ali torna a variável visível na página inteira. Mudou a cor da marca? Uma linha. Na Aula 06 você monta um sistema completo de variáveis; hoje basta usar duas ou três.

### 6.4 Por que `id` não é para estilo e `!important` não é solução

Você verá na Aula 06 que o navegador decide conflitos entre regras por **especificidade**: um `#id` vence qualquer quantidade de `.classes`, e `!important` vence tudo. Parece prático — até que você precisa sobrescrever e não consegue. Regra desta trilha desde hoje: estilize com **classes** (reutilizáveis e fáceis de sobrescrever), reserve `id` para âncoras e JavaScript, e não use `!important` — se precisou dele, há um problema de organização no CSS, e o remédio é reorganizar, não escalar a guerra.

## 💻 Mão na massa — Esqueleto semântico das cinco páginas e a primeira folha de estilo

Hoje as cinco páginas do site do evento — todas já existentes desde as Aulas 02 e 03 — ganham o esqueleto semântico correto, `contato.html` é **reestruturada** (o formulário do B5 da Aula 03 continua lá) e nasce o arquivo `css/estilo.css`, que crescerá a cada aula da Unidade 2.

### Passo 1 — criar `css/estilo.css` com reset, contêiner e base

Crie a pasta `css` e, dentro dela, o arquivo:

**`css/estilo.css`**

```css
/* ==========================================================
   Semana Acadêmica de Sistemas de Informação — folha de estilo
   Ordem: 1. reset · 2. variáveis · 3. base · 4. layout · 5. componentes
   ========================================================== */

/* 1. Reset e box-sizing */
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* 2. Variáveis */
:root {
  --cor-primaria: #0b3d5c;
  --cor-secundaria: #1a7fb5;
  --cor-texto: #333333;
  --cor-fundo: #f7f9fb;
  --espaco: 16px;
}

/* 3. Base */
body {
  font-family: "Segoe UI", Roboto, Arial, sans-serif;
  line-height: 1.6;
  color: var(--cor-texto);
  background-color: var(--cor-fundo);
}

img,
video {
  max-width: 100%;
  height: auto;
  display: block;
}

/* 4. Layout */
.container {
  width: 100%;
  max-width: 1100px;               /* largura do projeto, fixada de vez */
  margin-inline: auto;
  padding-inline: 1rem;
}

header {
  background-color: var(--cor-primaria);
  color: #ffffff;
  padding: var(--espaco) 0;
}

header a {
  color: #ffffff;
}

main {
  padding: calc(var(--espaco) * 2) 0;
}

main > .container > section {
  margin-bottom: calc(var(--espaco) * 2);
}

aside {
  padding: var(--espaco) 0;
  background-color: #e8eef3;
}

footer {
  background-color: var(--cor-primaria);
  color: #ffffff;
  padding: var(--espaco) 0;
  text-align: center;
}

footer a {
  color: #ffffff;
}

/* 5. Componentes */
.cartao {
  background-color: #ffffff;
  border: 1px solid #d9e0e7;
  border-radius: 8px;
  padding: var(--espaco);
  margin-bottom: var(--espaco);
}

.botao {
  display: inline-block;
  padding: 12px 24px;
  background-color: var(--cor-primaria);
  color: #ffffff;
  text-decoration: none;
  border-radius: 8px;
}

.botao:hover {
  background-color: var(--cor-secundaria);
}

.botao:focus-visible {
  outline: 3px solid #f0a500;
  outline-offset: 2px;
}
```

A regra `img, video { max-width: 100%; height: auto; display: block; }` merece atenção: sem ela, uma foto de 1600 px vaza para fora do contêiner em telas menores. `display: block` remove o pequeno espaço que aparece embaixo de imagens `inline` (elas ficam alinhadas à linha de base do texto, como se fossem letras).

### Passo 2 — ligar a folha de estilo nas cinco páginas

Em **cada** página, dentro do `<head>`, depois do `<title>`:

**`index.html`, `programacao.html`, `inscricao.html`, `palestrantes.html`, `contato.html` (no `<head>`)**

```html
<link rel="stylesheet" href="css/estilo.css">
```

Salve e olhe o Live Server: o cabeçalho fica azul-escuro, a fonte muda, as margens padrão somem. Se nada mudou, veja a aba Network: o `estilo.css` deve aparecer com status 200. Um 404 significa caminho errado.

### Passo 3 — reestruturar `index.html`

A página inicial já tem conteúdo desde a Aula 02 (as seções "Sobre o evento", "Como participar" e "Glossário") e o banner responsivo da Aula 04. **Nada disso sai.** O que muda é o esqueleto em volta: cada região ganha o seu `<div class="container">`, nasce uma seção de abertura (`.hero`), nascem os cartões de destaque, e o conteúdo tangencial vai para um `<aside>`.

**`index.html`**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Semana Acadêmica de Sistemas de Informação: três dias de palestras, minicursos e oficinas para estudantes e profissionais de tecnologia.">
  <meta name="author" content="Semana Acadêmica de Sistemas de Informação">
  <title>Início — Semana Acadêmica de Sistemas de Informação</title>
  <link rel="stylesheet" href="css/estilo.css">
</head>
<body>
  <header id="topo">
    <div class="container">
      <img src="img/logo-sasi.svg" alt="" width="160" height="48">
      <h1>Semana Acadêmica de Sistemas de Informação</h1>
      <p>Três noites de outubro · Auditório Central</p>
      <nav aria-label="Principal">
        <ul>
          <li><a href="index.html" aria-current="page">Início</a></li>
          <li><a href="programacao.html">Programação</a></li>
          <li><a href="inscricao.html">Inscrição</a></li>
          <li><a href="palestrantes.html">Palestrantes</a></li>
          <li><a href="contato.html">Contato</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <main>
    <div class="container">
      <section class="hero">
        <h2>Três noites de palestras, minicursos e maratona de programação</h2>
        <p>Participação gratuita, com certificado de 20 horas para quem comparecer a pelo menos 75% das atividades.</p>
        <a href="inscricao.html" class="botao">Inscreva-se</a>
      </section>

      <!-- O <picture> do banner (Aula 04) e as seções "Sobre o evento",
           "Como participar" e "Glossário" (Aula 02) continuam aqui,
           exatamente como estavam. -->

      <section class="destaques">
        <h2>Destaques desta edição</h2>

        <article class="cartao">
          <header>
            <h3>Minicurso: Git e GitHub do zero</h3>
            <p><time datetime="20:00">20h00</time> · Laboratório 2 · 30 vagas</p>
          </header>
          <p>Do primeiro commit ao pull request, em duas horas de prática.</p>
          <footer>
            <a href="inscricao.html">Garantir vaga</a>
          </footer>
        </article>

        <article class="cartao">
          <header>
            <h3>Maratona de programação</h3>
            <p><time datetime="18:30">18h30</time> · Laboratórios 1 e 2 · equipes de três</p>
          </header>
          <p>Problemas de lógica, ranking em tempo real e premiação no encerramento.</p>
          <footer>
            <a href="inscricao.html">Formar equipe</a>
          </footer>
        </article>

        <article class="cartao">
          <header>
            <h3>Mesa-redonda: mercado de trabalho em Sinop</h3>
            <p><time datetime="20:00">20h00</time> · Sala 105</p>
          </header>
          <p>Egressos do curso contam como conseguiram o primeiro emprego na região.</p>
          <footer>
            <a href="programacao.html">Ver programação</a>
          </footer>
        </article>
      </section>

      <section class="numeros">
        <h2>O evento em números</h2>
        <dl>
          <dt>Edições realizadas</dt>
          <dd>7</dd>
          <dt>Participantes na última edição</dt>
          <dd>180</dd>
          <dt>Horas de atividade</dt>
          <dd>21</dd>
        </dl>
      </section>
    </div>
  </main>

  <aside>
    <div class="container">
      <h2>Edições anteriores</h2>
      <p>Veja a <a href="palestrantes.html">galeria de palestrantes</a> e o <a href="programacao.html">vídeo de abertura</a> da edição passada.</p>
    </div>
  </aside>

  <footer>
    <div class="container">
      <p>Realização: Comissão Organizadora da Semana Acadêmica de Sistemas de Informação.</p>
      <p>
        <a href="mailto:contato@semanasi.com.br">contato@semanasi.com.br</a> ·
        <a href="tel:+556635111000">(66) 3511-1000</a>
      </p>
      <p>&copy; Semana Acadêmica de Sistemas de Informação. Todos os direitos reservados.</p>
      <nav aria-label="Rodapé">
        <ul>
          <li><a href="contato.html">Contato</a></li>
          <li><a href="https://www.w3.org/WAI/" target="_blank" rel="noopener noreferrer">Acessibilidade (W3C)</a></li>
        </ul>
      </nav>
    </div>
  </footer>
</body>
</html>
```

Três observações sobre o que **não** mudou: o `<h1>` continua no `<header>` (ele nomeia o site, não a página), o rodapé continua com os três parágrafos da Aula 02 — agora com um `<nav>` a mais — e as seções que a Aula 02 escreveu continuam no `<main>`, só que dentro do contêiner.

### Passo 4 — reestruturar `contato.html`

A quinta página existe desde a Aula 02 (esqueleto) e recebeu o formulário de mensagem no exercício **B5 da Aula 03** — com nome, e-mail, assunto, mensagem e a escolha da forma de resposta em rádios. **Esse formulário não é reescrito**: ele é transplantado para dentro do novo esqueleto, ganhando apenas o `<div class="container">` em volta e a classe `.botao` no botão de envio. O resto da página junta o que você aprendeu nas Aulas 02 a 04: tabela, links `tel:`/`mailto:` e mapa em `<iframe>`.

**`contato.html`**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Fale com a organização da Semana Acadêmica de Sistemas de Informação: telefone, e-mail, formulário e localização.">
  <title>Contato — Semana Acadêmica de Sistemas de Informação</title>
  <link rel="stylesheet" href="css/estilo.css">
</head>
<body>
  <header id="topo">
    <div class="container">
      <img src="img/logo-sasi.svg" alt="" width="160" height="48">
      <h1>Semana Acadêmica de Sistemas de Informação</h1>
      <p>Três noites de outubro · Auditório Central</p>
      <nav aria-label="Principal">
        <ul>
          <li><a href="index.html">Início</a></li>
          <li><a href="programacao.html">Programação</a></li>
          <li><a href="inscricao.html">Inscrição</a></li>
          <li><a href="palestrantes.html">Palestrantes</a></li>
          <li><a href="contato.html" aria-current="page">Contato</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <main>
    <div class="container">
      <h2>Contato</h2>

      <section>
        <h3>Fale com a organização</h3>
        <address>
          <p>Telefone: <a href="tel:+5566999990000">(66) 99999-0000</a></p>
          <p>E-mail: <a href="mailto:sasi@semanasi.com.br?subject=Contato%20pelo%20site">sasi@semanasi.com.br</a></p>
          <p>Sala 12 do Auditório Central, em Sinop</p>
        </address>
      </section>

      <section>
        <h3>Horário de atendimento</h3>
        <table>
          <caption>Atendimento presencial na sala da organização</caption>
          <thead>
            <tr>
              <th scope="col">Dia</th>
              <th scope="col">Manhã</th>
              <th scope="col">Noite</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <th scope="row">Segunda a quinta</th>
              <td>8h às 11h</td>
              <td>19h às 21h</td>
            </tr>
            <tr>
              <th scope="row">Sexta</th>
              <td>8h às 11h</td>
              <td>Fechado</td>
            </tr>
          </tbody>
        </table>
      </section>

      <section>
        <h3>Envie uma mensagem</h3>
        <form action="/contato" method="post">
          <p>
            <label for="nome">Nome completo</label>
            <input type="text" id="nome" name="nome" required minlength="5" autocomplete="name">
          </p>
          <p>
            <label for="email">E-mail</label>
            <input type="email" id="email" name="email" required autocomplete="email">
          </p>
          <p>
            <label for="assunto">Assunto</label>
            <select id="assunto" name="assunto" required>
              <option value="">Selecione</option>
              <option value="inscricao">Dúvida sobre inscrição</option>
              <option value="certificado">Certificado</option>
              <option value="patrocinio">Patrocínio</option>
              <option value="outro">Outro</option>
            </select>
          </p>
          <p>
            <label for="mensagem">Mensagem</label>
            <textarea id="mensagem" name="mensagem" rows="6" maxlength="600" required></textarea>
          </p>

          <fieldset>
            <legend>Como prefere receber a resposta?</legend>
            <p>
              <input type="radio" id="resposta-email" name="resposta" value="email" checked>
              <label for="resposta-email">Por e-mail</label>
            </p>
            <p>
              <input type="radio" id="resposta-telefone" name="resposta" value="telefone">
              <label for="resposta-telefone">Por telefone</label>
            </p>
          </fieldset>

          <p>
            <label for="telefone">Telefone (opcional, necessário se escolher resposta por telefone)</label>
            <input type="tel" id="telefone" name="telefone" autocomplete="tel"
                   placeholder="(66) 99999-0000">
          </p>

          <button type="submit" class="botao">Enviar mensagem</button>
        </form>
      </section>

      <section>
        <h3>Como chegar</h3>
        <iframe src="https://www.google.com/maps/embed?pb=CODIGO_GERADO_PELO_MAPS"
                title="Mapa: Auditório Central, em Sinop"
                width="600" height="450"
                loading="lazy"
                referrerpolicy="no-referrer-when-downgrade">
        </iframe>
      </section>
    </div>
  </main>

  <footer>
    <div class="container">
      <p>Semana Acadêmica de Sistemas de Informação</p>
    </div>
  </footer>
</body>
</html>
```

Repare no `<address>`: é o elemento semântico para informações de contato do autor ou da organização responsável pela página — exatamente este caso.

### Passo 5 — aplicar o contêiner nas outras três páginas

Em `programacao.html`, `inscricao.html` e `palestrantes.html`, envolva o conteúdo de `<header>`, `<main>` e `<footer>` com `<div class="container">`, como no Passo 3. O conteúdo em si não muda. Esse é um trabalho mecânico de cinco minutos — use a busca e substituição do VS Code (<kbd>Ctrl</kbd>+<kbd>H</kbd>) para o cabeçalho e o rodapé, que são idênticos em todas.

Aproveite para conferir, em cada página: há um único `<h1>` (o do `<header>`)? O título da página é o `<h2>` no topo do `<main>`? Em `palestrantes.html`, cada convidado já é um `<article>` desde a Aula 02 — acrescente a ele a classe `cartao`, que a folha de estilo do Passo 1 acabou de definir, e o `<h3>` continua sendo o nome da pessoa. Em `programacao.html`, a tabela permanece como está; ela ganha estilo na Aula 06.

### Passo 6 — diagnóstico e validação

1. Cole o comando de contorno da seção 1 no console de cada página e procure: conteúdo fora de `<main>`, `<section>` sem título, `<div>` que poderia ser um elemento semântico.
2. Na aba **Elements**, selecione o `.container` do `<main>` e confira no painel Styles que `width` resolve para no máximo 1100 px e que as margens laterais são iguais.
3. Redimensione a janela até 400 px: o conteúdo deve manter 1 rem de respiro em cada lado, sem barra de rolagem horizontal.
4. Valide as cinco páginas no W3C. Meta: zero erros.

### Como testar

- As cinco páginas abrem com o mesmo cabeçalho azul-escuro, a mesma fonte e o mesmo rodapé — sinal de que o CSS externo está ligado em todas.
- O conteúdo fica centralizado em monitores largos e ocupa a largura toda (menos o respiro) em janelas estreitas.
- O botão "Inscreva-se" da página inicial muda de cor ao passar o mouse e mostra um contorno amarelo ao ser alcançado com <kbd>Tab</kbd>.
- Em `contato.html`, o telefone e o e-mail são clicáveis, a tabela tem cabeçalhos, o formulário valida e o mapa aparece.
- Nenhuma imagem vaza para fora do contêiner em 400 px de largura.
- O DevTools mostra `box-sizing: border-box` em qualquer elemento que você selecionar.
- Zero erros no validador nas cinco páginas.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Quais são as três formas de aplicar CSS? Qual delas deve ser usada em projetos reais e por quê? Cite um caso legítimo para cada uma das outras duas.

**A2.** Cite quatro propriedades herdadas e quatro não herdadas. Explique a lógica que separa os dois grupos.

**A3.** Um elemento tem `width: 200px`, `padding: 15px` e `border: 5px`. Qual a largura total ocupada com `box-sizing: content-box`? E com `border-box`? Em qual dos dois o conteúdo fica com menos espaço?

**A4.** Explique o colapso de margens com um exemplo numérico. Diga em que situação ele **não** ocorre.

**A5.** Diferencie `display: none`, `visibility: hidden` e `opacity: 0` quanto a espaço ocupado, clicabilidade e leitura por leitor de tela. Para cada um, dê um uso adequado.

**A6.** O que faz `margin: 0 auto`? Que condição o elemento precisa satisfazer para funcionar? Qual a alternativa moderna com a mesma função?

**A7.** Por que `!important` deve ser evitado? O que geralmente indica quando alguém sente necessidade de usá-lo?

**A8.** Cite três elementos de seccionamento do HTML5 e o papel de cada um. O que são "marcos" para um leitor de tela?

**A9.** Quantos `<main>` uma página pode ter? Por quê? E quantos `<header>`?

**A10.** Qual a diferença entre `<section>` e `<article>`? Dê um exemplo de cada, retirado do site do evento.

**A11.** Quando o uso de `<div>` é a escolha correta? Dê o exemplo usado nesta aula.

**A12.** Escreva o esqueleto semântico completo de uma página institucional (sem conteúdo, só os elementos), incluindo o padrão de contêiner centralizado em cada região.

**A13.** Um `<a>` recebe `width: 200px` e `margin-top: 20px`, mas nada muda na tela. Por quê? Como corrigir sem tirar o link da linha do texto?

**A14.** Preveja o que acontece com a regra abaixo e explique o motivo:

```css
h1 {
  color: #0b3d5c
  font-size: 2rem;
}
```

### Nível B — Aplicação

**B1.** Crie três cartões (`article.cartao`) com: fundo branco, `border-radius`, `box-shadow`, padding interno, título, parágrafo e um link com classe `.botao`. No `:hover`, o cartão deve mudar de sombra e o botão de cor. Use **apenas variáveis CSS** para todas as cores e espaçamentos.

**Resultado esperado:** três cartões idênticos em estrutura, com sombra suave; ao passar o mouse, a sombra fica mais forte e o botão muda de cor; nenhum valor de cor ou espaçamento aparece fora de `:root`; o foco do botão via <kbd>Tab</kbd> é visível.

<details><summary>Dica</summary>

`box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1)` é uma sombra discreta; no `:hover`, troque por `0 6px 16px rgba(0, 0, 0, 0.2)`. Declare as duas como variáveis (`--sombra-cartao` e `--sombra-cartao-hover`). O `:hover` do cartão é `.cartao:hover`; o do botão dentro do cartão em hover é `.cartao:hover .botao`.
</details>

**B2.** Crie um menu de navegação horizontal usando `display: inline-block` nos itens (Flexbox só na Aula 07), com espaçamento entre eles, `:hover` com mudança de cor de fundo, `:focus-visible` visível e o item ativo destacado por uma classe `.ativo` (ou pelo atributo `aria-current`).

**Resultado esperado:** os cinco links ficam lado a lado na mesma linha, com espaço entre eles; passar o mouse muda o fundo do item; navegar por <kbd>Tab</kbd> mostra o contorno; o item da página atual tem aparência distinta sem depender do mouse.

<details><summary>Dica</summary>

`li { display: inline-block; }` coloca os itens na linha; o espaço entre eles vem de `margin-right` no `li` ou de `padding` no `a`. Para o item ativo sem criar classe, use o seletor de atributo `a[aria-current="page"]` — você já colocou esse atributo no HTML. Um pequeno espaço em branco entre os itens aparece por causa das quebras de linha do HTML: por enquanto, aceite; na Aula 07 o Flexbox resolve.
</details>

**B3.** Monte o esqueleto semântico das cinco páginas do **seu projeto autoral**, aplicando o padrão de contêiner centralizado em `header`, `main` e `footer`, ligando uma folha de estilo externa com o reset e as variáveis base, e valide todas no W3C.

**Resultado esperado:** cinco páginas com um único `<h1>` cada, `<main>` único, `<nav aria-label>`, conteúdo centralizado com respiro nas laterais; o mesmo `css/estilo.css` ligado em todas; zero erros no validador.

<details><summary>Dica</summary>

Comece pela página mais simples e copie o `<head>`, o `<header>` e o `<footer>` para as outras. Cole o comando de contorno no console de cada uma e procure conteúdo fora de `<main>`. Se o validador acusar "Element h1 not allowed" ou "Section lacks heading", releia a seção 1.2.
</details>

**B4.** Pegue a página abaixo, feita só com `<div>`, e reescreva-a usando os elementos de seccionamento adequados. Documente, em comentários HTML, cada troca e o motivo.

```html
<div id="topo">
  <div class="logo"><img src="logo.png"></div>
  <div class="menu">
    <a href="index.html">Início</a>
    <a href="noticias.html">Notícias</a>
  </div>
</div>
<div id="conteudo">
  <div class="titulo">Últimas notícias</div>
  <div class="noticia">
    <div class="titulo-noticia">Inscrições abertas</div>
    <div class="data">segunda-feira</div>
    <div class="texto">As inscrições começaram hoje.</div>
  </div>
  <div class="noticia">
    <div class="titulo-noticia">Palestrante confirmada</div>
    <div class="data">terça-feira</div>
    <div class="texto">Ana Souza falará sobre HTML semântico.</div>
  </div>
</div>
<div id="lateral">
  <div class="titulo">Links úteis</div>
  <a href="https://www.wikipedia.org">Wikipédia</a>
</div>
<div id="rodape">Todos os direitos reservados</div>
```

**Resultado esperado:** zero `<div>` com significado disfarçado; títulos como `<h1>`/`<h2>`/`<h3>`; cada notícia é um `<article>` com `<time>`; o menu é uma lista dentro de `<nav>`; a imagem tem `alt`; zero erros no validador; pelo menos oito comentários explicando as trocas.

<details><summary>Dica</summary>

Faça a pergunta da seção 1.2 para cada `div`: "existe um elemento que descreva o que isto é?". `topo` é um cabeçalho; `menu` é navegação; `conteudo` é o principal; `noticia` faz sentido sozinha; `lateral` é tangencial; `rodape` é rodapé. Os "títulos" são cabeçalhos de nível 1, 2 e 3. A `div` que sobra, se sobrar, é o contêiner centralizado.
</details>

### Nível C — Desafio

**C1.** Engenharia reversa de um site real. Escolha a página inicial de um site institucional de verdade (o portal da sua universidade ou escola, o site de uma prefeitura, o gov.br). Com o DevTools, mapeie a estrutura de marcos dela: quantos `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>` e `<footer>` existem, e quantas `<div>`. Depois reconstrua **o esqueleto** dessa página (sem copiar conteúdo — use textos próprios) em HTML semântico, com o contêiner centralizado, e escreva um parágrafo comparando: o site original usa os marcos corretamente? O que você faria diferente?

<details><summary>Dica</summary>

No console, `document.querySelectorAll("div").length` conta as `div`; troque por `main`, `nav`, `article` para os outros. Para ver os marcos como um leitor de tela vê, instale a extensão **Accessibility Insights** ou use a aba **Accessibility** do DevTools (painel Elements → Accessibility → Accessibility Tree). Sites com dezenas de `div` e nenhum `main` são comuns — e é exatamente isso que vale a pena registrar.
</details>

## 🏆 Desafios

### ⭐ A folha de estilo que não funciona
Tags: css, bug, devtools

Alguém passou uma hora tentando descobrir por que "o CSS não pega". O arquivo está abaixo, e o HTML o referencia com `<link rel="stylesheet" href="estilo.css">` — mas o arquivo está salvo em `css/estilo.css`. Além desse, há **seis** erros no CSS. Encontre todos os sete usando só o DevTools (painel Styles mostra declarações inválidas riscadas; a aba Network mostra o 404) antes de recorrer a qualquer validador.

```css
* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: Arial, sans-serif
  color: #333;
}

// Cabeçalho
header {
  background-color: darkblu;
  padding: 16px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

nav a {
  width: 120px;
  margin-top: 8px;
  color: white;
}

.cartao {
  border: 2px #0b3d5c;
  padding: 16px;
}

.aviso {
  display: inline;
  width: 100%;
  background-color: #fff3cd;
}
```

**Critérios de pronto**

- Lista numerada com os sete problemas: linha, sintoma observável na página ou no DevTools, causa e correção.
- O CSS corrigido, com as regras que dependiam de `display` funcionando (a largura dos links e do aviso aplicada de fato).
- Uma frase explicando o que o painel Styles mostra quando uma declaração é inválida, e o que a aba Network mostra quando o arquivo não é encontrado.

<details><summary>Pistas</summary>

1. Dois erros são de sintaxe pura: um `;` que falta e um comentário no formato errado. Releia a seção 2.1 sobre o que acontece com a declaração seguinte em cada caso.
2. Um nome de cor está escrito errado; o DevTools risca a declaração inválida e mostra um triângulo amarelo ao lado.
3. Uma borda precisa de três valores para aparecer (seção 4.4).
4. Dois blocos aplicam `width` e `margin-top` a elementos que, por padrão, ignoram essas propriedades (seção 5).
</details>

### ⭐⭐ Reproduza o cartão de repositório do GitHub
Tags: css, layout, investigacao

Abra o perfil de qualquer pessoa no GitHub e olhe os cartões de "repositórios fixados" (*pinned*): ícone, nome em azul, descrição em cinza, etiqueta da linguagem com uma bolinha colorida, contador de estrelas. Parece simples — e é o tipo de componente que você fará dezenas de vezes na carreira. Reproduza um cartão idêntico usando **só o que esta aula ensinou**: box model, `display: inline-block`, bordas, cores e variáveis. Sem Flexbox, sem Grid, sem `position`. Use o DevTools para descobrir os valores reais de padding, borda, raio e cores do cartão original.

**Critérios de pronto**

- O cartão tem borda de 1 px, cantos arredondados, padding interno e largura máxima iguais aos do original (medidos no DevTools, com tolerância de 2 px).
- O nome do repositório é um link; a bolinha da linguagem é um elemento `inline-block` de 12×12 px com `border-radius: 50%`.
- Todas as cores estão em variáveis em `:root`, com os valores extraídos do original.
- Três cartões lado a lado (`inline-block`) cabem em 1200 px sem quebrar; em 400 px, ficam um embaixo do outro.
- Um comentário no CSS lista os valores originais que você mediu e onde os encontrou no DevTools (painel Styles ou Computed).

<details><summary>Pistas</summary>

1. No DevTools, selecione o cartão original e leia a aba **Computed**: ela mostra o valor final de `padding`, `border-radius`, `border-color` e `background-color` já resolvidos.
2. Elementos `inline-block` lado a lado ganham um espaço em branco entre si por causa das quebras de linha no HTML; reduza-o escrevendo as tags coladas ou aceite-o por enquanto.
3. A bolinha e o nome da linguagem ficam na mesma linha porque ambos são `inline`/`inline-block`; `vertical-align: middle` alinha a bolinha ao texto.
4. Para os três cartões caberem em 1200 px, calcule: com `border-box`, três caixas de `32%` mais o espaço em branco entre elas passam de 100%? Ajuste até caber.
</details>

### ⭐⭐⭐ Laboratório interativo do box model
Tags: css, layout, devtools, investigacao

Explicar o box model para outra pessoa é a melhor forma de descobrir se você entendeu. Construa uma página didática, `box-model.html`, que **demonstre visualmente** cada conceito desta aula com exemplos vivos: a mesma caixa em `content-box` e `border-box` lado a lado, com as medidas escritas; três casos de colapso de margem (irmãos, pai e filho, sem colapso dentro de um elemento com padding); `block`, `inline` e `inline-block` recebendo a mesma `width` e reagindo de formas diferentes; e as três formas de esconder (`display: none`, `visibility: hidden`, `opacity: 0`) com um botão em cada uma para o leitor testar o clique. Tudo com HTML semântico e CSS externo — nada de JavaScript.

**Critérios de pronto**

- Cada demonstração é uma `<section>` com título, um parágrafo explicando o que observar e o exemplo vivo ao lado do código-fonte correspondente em `<pre><code>`.
- As medidas reais de cada caixa (largura ocupada, espaço entre elementos) aparecem escritas na página e conferem com o que o DevTools mostra.
- As caixas usam cores diferentes para content, padding e border, visíveis a olho nu.
- Alguém que nunca viu CSS consegue, lendo só a página, responder às questões A3, A4, A5 e A13 deste Laboratório — teste com uma pessoa nessas condições e registre as respostas.
- A página valida no W3C e usa o padrão de contêiner centralizado.

<details><summary>Pistas</summary>

1. Para mostrar o código-fonte na página, escreva o HTML dentro de `<pre><code>` trocando `<` por `&lt;` — senão o navegador renderiza em vez de exibir.
2. Para tornar visível o padding, use `background-clip: content-box` em um elemento e compare com o padrão `border-box`: a cor de fundo mostra onde termina o conteúdo.
3. O caso "pai e filho" do colapso fica evidente se você der um fundo à `<section>` pai: a margem do primeiro filho aparece **fora** do fundo. Adicione `padding-top: 1px` ao pai e veja a margem voltar para dentro.
4. Para os botões de "esconder", coloque três `<a href="#clicou">` com cada técnica e peça ao leitor para tentar clicar e usar <kbd>Tab</kbd>: só o de `opacity: 0` responde.
</details>

**Para ir além:** publique a página (Aula 15 ou trilha Deploy) e use-a como material de revisão sempre que precisar retomar o assunto.

### 🔥 Boss — Auditoria e reconstrução de um site real
Tags: html, acessibilidade, projeto, investigacao

Sites institucionais brasileiros — de prefeituras, secretarias, campi — costumam ter dezenas de `<div>`, imagens sem `alt`, formulários sem `<label>` e tabelas usadas para layout. Você agora sabe reconhecer tudo isso. Escolha um site institucional real (que não seja o mesmo usado no C1), audite as suas quatro páginas principais com tudo o que a Unidade 1 ensinou e **reconstrua** essas páginas em HTML semântico, acessível e válido, com conteúdo próprio inspirado no original. É o mini-projeto que fecha a unidade: arquitetura da Web, estrutura de documento, textos, links, tabelas, formulários, mídias, listas e seccionamento — tudo junto.

**Critérios de pronto**

- Relatório de auditoria (uma a duas páginas) com, para cada uma das quatro páginas originais: número de `<div>` e de marcos semânticos, erros do validador W3C, imagens sem `alt`, campos sem `<label>`, tabelas usadas para layout, peso total na aba Network e nota de Acessibilidade no Lighthouse.
- Quatro páginas reconstruídas, interligadas por menu em `<nav>`, com: `<main>` único, um `<h1>` por página, hierarquia de títulos correta, os três tipos de lista, uma tabela de dados com `caption`/`thead`/`th scope`, um formulário com no mínimo seis campos e `label` em todos, uma imagem em `<figure>` com `alt` adequado, um vídeo ou áudio com `controls` e um `<iframe>` com `title`.
- Folha de estilo externa única com reset, `box-sizing: border-box`, variáveis base e o contêiner centralizado — e nada além disso (a estilização completa é assunto da Unidade 2).
- Zero erros no validador nas quatro páginas; nota de Acessibilidade no Lighthouse igual ou superior a 90.
- Tabela comparativa final: original × reconstrução, nas mesmas métricas do relatório.
- README no repositório com o link do site original, as decisões de estrutura e o que você aprendeu.

<details><summary>Pistas</summary>

1. Para a auditoria, o console resolve as contagens: `document.querySelectorAll("div").length`, `document.querySelectorAll("img:not([alt])").length`, `document.querySelectorAll("input:not([id])").length`.
2. O Lighthouse está na aba homônima do DevTools; rode só a categoria **Accessibility** para ser rápido, e leia os itens reprovados — eles apontam o elemento exato.
3. Comece a reconstrução pelo esqueleto (Passo 3 da Mão na massa) e só depois preencha o conteúdo; um esqueleto validado evita retrabalho.
4. Conteúdo "inspirado no original" significa mesma estrutura de informação (seções, tipos de dado) com textos seus — não copie parágrafos nem imagens sem licença.
</details>

**Para ir além:** este Boss pode virar parte do seu Marco 1 — mostre-o junto com o restante do projeto.

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| O CSS "não pega" em nenhuma página; a aba Network mostra `estilo.css` com status 404 | Caminho errado no `href` do `<link>` (arquivo em `css/estilo.css`, link apontando para `estilo.css`) | Corrija o caminho relativo à página; confira maiúsculas e a extensão |
| Uma regra inteira é ignorada e a seguinte também | Faltou `;` ao fim de uma declaração — o navegador junta as duas e descarta | Todo `propriedade: valor` termina com `;`; o DevTools risca a declaração inválida |
| Tudo abaixo de um comentário para de funcionar | Comentário escrito com `//` — não existe em CSS | Use `/* comentário */` |
| `p .classe` não estiliza o parágrafo com a classe | Espaço acidental: `p .classe` seleciona descendentes com a classe **dentro** de `<p>` | Sem espaço (`p.classe`) para "parágrafo que tem a classe" |
| Duas colunas de `50%` não cabem lado a lado e a segunda cai | `box-sizing: content-box` somando padding e borda por fora | Reset com `box-sizing: border-box` no topo do CSS |
| `margin: 0 auto` não centraliza | Elemento sem `width`/`max-width` (ocupa 100%, não sobra espaço) ou elemento `inline` | Defina uma largura e garanta `display: block` |
| `width` e `margin-top` em um `<a>` ou `<span>` não fazem nada | Elemento `inline` ignora dimensões e margens verticais | `display: inline-block` (ou `block`) |
| A borda não aparece | `border: 2px #333` sem o estilo (`solid`) | `border: 2px solid #333` — os três valores |
| O espaço entre dois blocos é menor que a soma das margens | Colapso de margens verticais | Comportamento esperado; use só uma das margens ou padding no pai |
| O foco do teclado sumiu dos links | `outline: none` no `:focus` | Substitua por um indicador visível (`outline` colorido ou `box-shadow`) |
| A imagem vaza para fora do contêiner em telas estreitas | `<img>` sem `max-width: 100%` | Regra base `img { max-width: 100%; height: auto; }` |
| Tudo em `px` e o usuário que aumentou a fonte do navegador não é atendido | Unidades absolutas para tipografia | `rem` para texto (Aula 06) |

## 🏠 Para praticar depois da aula (1 h)

**Parte 1 — Leitura (20 min).** SILVA, M. S. *Criando sites com HTML*, capítulos sobre estrutura de página e introdução ao CSS. Na MDN em pt-BR: "Estrutura de documento e site" e "O modelo de caixa" (links em Para aprofundar).

**Parte 2 — Produção (30 min).** Exercício **B3**: o esqueleto semântico das cinco páginas do **seu projeto autoral**, validado no W3C, mais a primeira folha de estilo (`css/estilo.css`) com reset, `box-sizing: border-box` global, variáveis de cores base e o contêiner centralizado aplicado nas cinco páginas.

**Critério de pronto:** as cinco páginas abrem com o mesmo cabeçalho e rodapé estilizados; `document.querySelectorAll("main").length` retorna `1` em cada página; o DevTools mostra `box-sizing: border-box` em qualquer elemento; zero erros no validador.

**Guarde no seu repositório:** commit + push (ou a pasta do projeto, se ainda não usa Git).

**Parte 3 — Discussão (10 min).** Em texto próprio — ou no fórum da turma, se você está cursando esta trilha em grupo —: publique o tema do seu projeto e o wireframe das páginas nas três larguras (celular, tablet, desktop) — pode ser desenhado à mão e fotografado. **Os três marcos da trilha acompanham este mesmo projeto**, cada um acrescentando uma camada (HTML no Marco 1, CSS no Marco 2, JavaScript no Marco 3). Se puder, compare o wireframe com o de outra pessoa, apontando um problema de hierarquia visual.

## ✅ Checkpoint do projeto

Ao fim desta aula — e da Unidade 1 — o repositório do seu projeto autoral deve ter:

- [ ] Cinco páginas interligadas por um menu em `<nav aria-label>` com `aria-current` na página atual.
- [ ] Em cada página: `<header>`, `<main>` único, `<footer>`, um único `<h1>` e seções com título.
- [ ] `<article>` para cada conteúdo autocontido (cartões, palestrantes, notícias, produtos do seu domínio).
- [ ] Padrão de contêiner centralizado (`<div class="container">`) em `header`, `main` e `footer`.
- [ ] `css/estilo.css` ligado em todas as páginas, começando pelo reset com `box-sizing: border-box`.
- [ ] Bloco `:root` com pelo menos três variáveis (cor primária, cor secundária, espaçamento).
- [ ] Regra base `img, video { max-width: 100%; height: auto; display: block; }`.
- [ ] Um `.botao` com `:hover` e `:focus-visible` visíveis.
- [ ] Página de contato com `<address>`, links `tel:`/`mailto:`, tabela com `caption` e formulário com `label` em todos os campos.
- [ ] Zero erros no validador W3C nas cinco páginas.
- [ ] Tema e wireframe do projeto autoral registrados (no fórum da turma ou nas suas próprias anotações).

Isso encerra a Unidade 1.

## 📚 Para aprofundar

- MDN — Estrutura de documento e site: <https://developer.mozilla.org/pt-BR/docs/Learn_web_development/Core/Structuring_content/Structuring_documents> — os elementos de seccionamento com exemplos e os erros mais comuns.
- MDN — O modelo de caixa: <https://developer.mozilla.org/pt-BR/docs/Learn_web_development/Core/Styling_basics/Box_model> — `content-box` × `border-box`, colapso de margens e `display` com demonstrações interativas.
- MDN — Primeiros passos em CSS: <https://developer.mozilla.org/pt-BR/docs/Learn_web_development/Core/Styling_basics> — a trilha introdutória completa; leia "O que é CSS" e "Como o CSS é estruturado".
- MDN — Referência de CSS: <https://developer.mozilla.org/pt-BR/docs/Web/CSS> — para consultar qualquer propriedade citada nesta aula.
- MDN — Elemento `<main>`: <https://developer.mozilla.org/pt-BR/docs/Web/HTML/Element/main> — por que só um por página.
- web.dev — Learn CSS, módulo "Box model": <https://web.dev/learn/css/box-model> — explicação visual com o DevTools.
- web.dev — Learn HTML, módulo "Document structure": <https://web.dev/learn/html/document-structure> — o esqueleto de uma página profissional.
- W3C — CSS, site oficial de padronização: <https://www.w3.org/Style/CSS/> — onde as especificações vivem.
- SILVA, Maurício Samy. *Criando sites com HTML: sites de alta qualidade com HTML e CSS*. Novatec, 2008 — capítulos sobre estrutura de página e introdução ao CSS.
- TERUEL, Evandro C. *HTML 5 — Guia Prático*. Saraiva, 2014 — capítulo sobre os novos elementos estruturais do HTML5.

Na próxima aula você entra no CSS de verdade — seletores, cascata, especificidade, cores, unidades, tipografia e variáveis — e é também o dia do **Marco 1**: o site em HTML puro, com tudo o que a Unidade 1 ensinou. As instruções completas estão na Aula 06, e o escopo são os itens **não-CSS** do Checkpoint acima.
