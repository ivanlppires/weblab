# Aula 06 — CSS: sintaxe, seletores, classes, atributos e valores

> **Nível 1 — Introdução ao Desenvolvimento Web** · Unidade 2: CSS: estilo, layout e responsividade
> WebLab · UNEMAT — Campus Sinop
> **Tempo estimado:** 3 blocos de 50 min + 1 h de prática

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Escrever seletores precisos usando tipo, classe, `id`, atributo, combinadores, pseudoclasses e pseudoelementos — e explicar o que cada um alcança.
- Prever qual regra vence um conflito, calculando a **especificidade** e aplicando as três etapas da cascata.
- Distinguir propriedades herdadas de não herdadas e usar a herança para escrever menos CSS.
- Escolher e escrever cores nas notações hexadecimal, `rgb()` e `hsl()`, e verificar o contraste segundo a WCAG.
- Justificar o uso de unidades relativas (`rem`, `em`, `%`, `vw`, `ch`) em vez de `px` e evitar a armadilha do `em` acumulado.
- Definir uma escala tipográfica legível: pilha de fontes, tamanhos, `line-height` e largura de linha.
- Montar um **sistema de design** em variáveis CSS e organizar a folha de estilo em seções previsíveis.

## 📋 Pré-requisitos

- [ ] Pasta `site-evento/` com as cinco páginas em HTML semântico validadas no W3C e `css/estilo.css` ligado em todas elas (Aula 05).
- [ ] VS Code com Live Server e um navegador com DevTools. Hoje o painel **Styles** e a aba **Computed** são as ferramentas principais.
- [ ] Revisar da Aula 05: sintaxe de uma regra CSS (seletor, declaração, bloco), o modelo de caixa, `box-sizing: border-box`, os valores de `display` e o gostinho de herança, `:hover` e variáveis da seção 6.
- [ ] **Marco 1 pronto** — o site em HTML puro. As instruções completas estão no fim desta aula.

Na aula passada você deu ao site do evento um esqueleto semântico correto e escreveu a primeira folha de estilo: um reset com `box-sizing: border-box`, três variáveis, uma tipografia base e alguns componentes. Aquela folha funciona, mas não escala: as cores estão espalhadas, os seletores são genéricos demais e, quando duas regras brigam, você ainda não sabe explicar quem ganha. Hoje isso muda — e o site ganha um sistema de design de verdade. Esta aula abre a **Unidade 2** e é também o dia do **Marco 1**.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Seletores completos: tipo, classe, `id`, atributo, combinadores, pseudoclasses e pseudoelementos |
| 2 | 50 min | Cascata, especificidade e herança; cores e contraste; unidades relativas; tipografia |
| 3 | 50 min | Variáveis CSS e organização da folha; Mão na massa: o sistema de design do site; Marco 1 do projeto |

## 1. Seletores

Um seletor responde a uma pergunta: **quais elementos desta página recebem este estilo?** Quanto mais preciso o seletor, menos você luta contra o próprio CSS depois.

### 1.1 Os quatro seletores básicos

```css
*           { }   /* universal: todos os elementos */
p           { }   /* tipo (ou elemento): todos os <p> */
.destaque   { }   /* classe: todos os elementos com class="destaque" */
#cabecalho  { }   /* id: o único elemento com id="cabecalho" */
```

- **Universal (`*`)** existe para o reset. Fora dele, quase nunca é a ferramenta certa.
- **Tipo** serve para estilos base: como deve ser *todo* parágrafo, *todo* link, *toda* tabela deste site.
- **Classe** é o seletor do dia a dia. Reutilizável, aplicável a qualquer elemento, fácil de sobrescrever.
- **`id`** identifica um elemento único na página. Para estilo, evite: ele tem especificidade altíssima e não é reutilizável.

> **💡 Dica**
> A regra da disciplina, que você já conhece desde a Aula 05: **estilize com classes**; reserve `id` para âncoras (`#topo`), para o atributo `for` dos rótulos e para o JavaScript da Unidade 3. Se um estilo aparece uma vez hoje, quase certamente vai aparecer duas amanhã — e uma classe já estará pronta.

### 1.2 Agrupamento

Uma vírgula aplica a mesma regra a vários seletores:

```css
h1, h2, h3 {
  font-family: var(--fonte-base);
  line-height: 1.2;
}
```

Cuidado com o efeito colateral: se um dos seletores da lista estiver errado, alguns navegadores antigos descartavam a regra inteira. Hoje isso não acontece mais com seletores válidos, mas continua valendo a disciplina de agrupar apenas o que é realmente comum.

### 1.3 Combinadores: seletores que descrevem relações

```css
article p   { }   /* descendente: todo <p> dentro de <article>, em qualquer nível */
article > p { }   /* filho direto: só os <p> filhos imediatos de <article> */
h2 + p      { }   /* irmão adjacente: o <p> imediatamente depois de um <h2> */
h2 ~ p      { }   /* irmãos gerais: todos os <p> depois de um <h2>, no mesmo pai */
```

```text
<article>            article p   pega os 3 parágrafos
  <p>A</p>           article > p pega só A e C
  <div>              h2 + p      pega só o parágrafo logo após o h2
    <p>B</p>         h2 ~ p      pega todos os parágrafos irmãos depois do h2
  </div>
  <h2>Título</h2>
  <p>C</p>
</article>
```

O combinador de irmão adjacente resolve um problema clássico de tipografia: dar uma margem maior ao parágrafo que abre uma seção, sem tocar nos outros.

```css
h2 + p {
  font-size: 1.125rem;   /* o parágrafo de abertura é um pouco maior */
}
```

### 1.4 Um espaço muda tudo

```css
p.destaque   { }   /* um <p> QUE TEM a classe destaque */
p .destaque  { }   /* qualquer elemento com classe destaque DENTRO de um <p> */
.cartao.ativo  { }   /* um elemento que tem AMBAS as classes */
.cartao .ativo { }   /* um elemento com classe ativo dentro de um .cartao */
```

Esse espaço é o erro de digitação mais caro do CSS iniciante: o estilo "simplesmente não pega" e não há mensagem de erro nenhuma. Quando isso acontecer, o primeiro passo é ler o seletor em voz alta, palavra por palavra: "pê ponto destaque" (o mesmo elemento) ou "pê espaço ponto destaque" (um dentro do outro)?

> **🔬 Investigue**
> Abra `index.html` no Live Server e o DevTools. No painel **Elements**, selecione um `<h2>` e olhe a aba **Styles**: à direita de cada regra aparece o arquivo e a linha de origem; regras riscadas foram vencidas por outras. Agora, na aba **Console**, digite `document.querySelectorAll("main p").length` e depois `document.querySelectorAll("main > p").length`. Os números são diferentes — e a diferença é exatamente o que o combinador `>` exclui. Repita com `.cartao p`, `.cartao > p` e `h2 + p`. O `querySelectorAll` aceita **os mesmos seletores do CSS**, e é a maneira mais rápida de conferir se um seletor pega o que você acha que pega.

### 1.5 Seletores de atributo

```css
a[target]              { }   /* tem o atributo, qualquer que seja o valor */
a[target="_blank"]     { }   /* valor exato */
a[href^="https"]       { }   /* COMEÇA com (^ = começo) */
a[href$=".pdf"]        { }   /* TERMINA com ($ = fim) */
a[href*="unemat"]      { }   /* CONTÉM em qualquer posição */
input[type="checkbox"] { }   /* muito usado em formulários */
```

Eles são poderosos justamente porque estilizam **pelo significado do HTML**, sem exigir uma classe extra. Dois usos que você vai aplicar hoje:

```css
/* Avisa visualmente que o link sai do site */
a[href^="http"]::after {
  content: " ↗";
}

/* Avisa que o link baixa um arquivo pesado */
a[href$=".pdf"]::after {
  content: " (PDF)";
  font-size: .875rem;
}
```

No site do evento, o menu vai usar `a[aria-current="page"]` para destacar a página atual — o mesmo atributo que você aprendeu na Aula 04 por acessibilidade vira, de graça, um seletor de estilo. Essa é a recompensa de escrever HTML semântico: o CSS fica mais curto.

### 1.6 Pseudoclasses: o estado do elemento

Uma pseudoclasse (um `:` simples) mira um elemento **em determinado estado**.

```css
a:link           { }   /* link ainda não visitado */
a:visited        { }   /* já visitado */
a:hover          { }   /* mouse por cima */
a:active         { }   /* no instante do clique */
a:focus          { }   /* com foco (teclado ou clique) */
a:focus-visible  { }   /* com foco E o navegador julga útil mostrar o anel */

input:required   { }
input:checked    { }
input:disabled   { }
input:valid      { }
input:invalid    { }
input:placeholder-shown { }
```

> **⚠️ Atenção**
> **Ordem obrigatória das pseudoclasses de link: LVHA** — `:link`, `:visited`, `:hover`, `:active`. Como todas têm a mesma especificidade, quem vem depois vence; escrever `:hover` antes de `:visited` faz o `:hover` "não funcionar" em links já visitados. O mnemônico clássico é *LoVe HAte*.

**`:focus` ou `:focus-visible`?** Use `:focus-visible`. Ele mostra o anel de foco quando a navegação é por teclado e o esconde quando o foco veio de um clique de mouse — exatamente o comportamento que as pessoas esperam. E nunca escreva `outline: none` sem colocar outro indicador visível no lugar: um site sem foco visível é inutilizável por teclado, ponto.

### 1.7 Pseudoclasses estruturais

```css
li:first-child      { }   /* o primeiro filho */
li:last-child       { }   /* o último filho */
li:only-child       { }   /* quando é o único */
tr:nth-child(3)     { }   /* o terceiro */
tr:nth-child(odd)   { }   /* ímpares: 1, 3, 5… */
tr:nth-child(even)  { }   /* pares: 2, 4, 6… */
li:nth-child(3n)    { }   /* de 3 em 3: 3, 6, 9… */
li:nth-child(3n+1)  { }   /* 1, 4, 7… */
p:not(.destaque)    { }   /* todos os <p> que NÃO têm a classe destaque */
```

`:nth-child(even)` é o que dá as **linhas alternadas** de uma tabela — o famoso "zebrado" que você vai aplicar na programação do evento. Já `:not()` evita regras duplicadas: em vez de escrever um estilo para todos os parágrafos e depois desfazê-lo em alguns, você exclui de uma vez.

> **📌 Vale gravar**
> `:nth-child(n)` conta **todos os irmãos**, não só os do mesmo tipo. Em `<div><h2></h2><p>A</p><p>B</p></div>`, o parágrafo A é o **segundo** filho — `p:nth-child(1)` não pega nada. Quando você quer contar só os do mesmo tipo, existe `:nth-of-type(n)`. Essa diferença é pergunta certa de prova e bug certo na vida real.

### 1.8 Pseudoelementos: partes que não existem no HTML

Um pseudoelemento (dois-pontos duplos, `::`) cria ou alcança uma **parte virtual** do elemento.

```css
p::first-line   { font-weight: 600; }
p::first-letter { font-size: 3rem; line-height: 1; }

.aviso::before  { content: "⚠ "; }
.externo::after { content: " ↗"; }

li::marker      { color: var(--cor-secundaria); }   /* o marcador da lista */
::selection     { background: #0b3d5c; color: #fff; }   /* texto selecionado */
```

A propriedade `content` é **obrigatória** em `::before` e `::after`: sem ela, o pseudoelemento não é criado — nem mesmo com `content: ""` esquecido. Esse é o motivo número um de "meu `::after` não aparece".

> **⚠️ Atenção**
> Conteúdo criado por `content` é decoração, não informação. Ele pode não ser lido por leitores de tela, não é copiado de forma confiável e some se o CSS não carregar. Use `::before`/`::after` para ícones, setas e aspas decorativas — **nunca** para texto que a pessoa precisa ler para entender a página. A seta de link externo é aceitável porque a informação essencial ("este link sai do site") também deve estar no texto ou no `title` do link.

> **🧠 Você sabia?**
> A sintaxe de dois-pontos duplos (`::before`) só apareceu no CSS3, justamente para distinguir **pseudoelementos** (partes virtuais) de **pseudoclasses** (estados). Antes disso, tudo usava um dois-pontos só, e os navegadores aceitam `:before` até hoje por compatibilidade retroativa. Nunca deixaram de aceitar — porque remover algo da Web quebra páginas que ninguém pode mais consertar. É a mesma lógica que mantém `<form>` funcionando desde 1993, e o motivo pelo qual o CSS tem tantos "dois jeitos de fazer a mesma coisa". Escreva sempre com `::`; leia `:` sem estranhar.

## 2. A cascata: como o navegador decide

Duas regras diferentes atingem o mesmo `<h2>` e dizem cores diferentes. Quem ganha? O navegador decide em **três etapas, nesta ordem**.

### 2.1 Etapa 1 — origem e importância

Da menor para a maior prioridade:

1. Estilos padrão do **navegador** (é por isso que um `<h1>` já nasce grande e em negrito).
2. Estilos do **usuário** (folha de estilo pessoal, configurações de acessibilidade).
3. Estilos do **autor** — você, no `estilo.css`.
4. Declarações `!important` do **autor**.
5. Declarações `!important` do **usuário** — a última palavra é sempre de quem lê a página.

Repare na inversão do topo: o `!important` do usuário vence o do autor. Isso é proposital. Alguém que precisa de fonte gigante ou de altíssimo contraste para conseguir ler tem prioridade sobre o seu design.

> **⚠️ Atenção**
> `!important` resolve o conflito de agora e cria um problema permanente: para sobrescrevê-lo, só com outro `!important` mais específico — e a folha vira uma escada de gritos. **Regra da disciplina: `!important` é proibido nos trabalhos**, salvo justificativa escrita (a única exceção que você vai encontrar é dentro do bloco `prefers-reduced-motion` da Aula 09). Se precisou dele, o problema é de arquitetura, e o remédio é reorganizar os seletores.

### 2.2 Etapa 2 — especificidade

Se duas regras têm a mesma origem, vence a **mais específica**. Conte cada seletor como um trio **(A, B, C)**:

| Peso | O que conta | Exemplos |
|---|---|---|
| **A** | `id` | `#menu` |
| **B** | Classes, atributos e pseudoclasses | `.cartao`, `[type="text"]`, `:hover` |
| **C** | Elementos e pseudoelementos | `p`, `div`, `::before` |

O universal (`*`) e os combinadores (`>`, `+`, `~`) valem **zero**. `:not()` não conta em si, mas o que está **dentro** dele conta.

| Seletor | A, B, C | Leitura |
|---|---|---|
| `p` | 0, 0, 1 | 0-0-1 |
| `.destaque` | 0, 1, 0 | 0-1-0 |
| `p.destaque` | 0, 1, 1 | 0-1-1 |
| `nav ul li a` | 0, 0, 4 | 0-0-4 |
| `.menu a` | 0, 1, 1 | 0-1-1 |
| `#menu` | 1, 0, 0 | 1-0-0 |
| `#menu li a:hover` | 1, 1, 2 | 1-1-2 |
| `style="…"` (inline) | — | Vence tudo, exceto `!important` |

Compara-se **A** primeiro; só em caso de empate compara-se **B**; e, empatando de novo, **C**. Um `id` vence qualquer quantidade de classes: `#menu` (1-0-0) ganha de `.nav .lista .item .link` (0-4-0). É exatamente por isso que estilizar com `id` é uma armadilha — você constrói uma parede que só um `id` maior derruba.

**Um caso real que você vai encontrar na Aula 07.** Um menu com um link em formato de botão:

```css
.menu a      { color: var(--cor-texto); }   /* 0-1-1 */
.menu__cta   { color: #ffffff; }            /* 0-1-0 — PERDE */
.menu a.menu__cta { color: #ffffff; }       /* 0-2-1 — ganha */
```

O botão ficaria com texto escuro sobre fundo escuro, e nada no console avisaria. Quando um estilo "não pega", **a especificidade é a primeira suspeita** — e o DevTools mostra a regra vencida riscada.

### 2.3 Etapa 3 — ordem no arquivo

Empatou em especificidade? **Vence a última regra escrita.**

```css
.botao { background-color: #0b3d5c; }
.botao { background-color: #1a7fb5; }   /* esta vence: veio depois */
```

Isso vale também entre arquivos: se a página tem dois `<link rel="stylesheet">`, o segundo sobrescreve o primeiro em caso de empate. E é por isso que a **ordem das seções** dentro da folha (seção 7 desta aula) importa: base primeiro, componentes depois, utilitários por último.

### 2.4 Herança

Algumas propriedades passam automaticamente de pai para filho. Você já viu isso na Aula 05; agora vale a tabela completa e a lógica por trás.

| Herdadas (passam para os filhos) | Não herdadas (cada elemento define a sua) |
|---|---|
| `color`, `font-family`, `font-size`, `font-weight` | `margin`, `padding`, `border` |
| `line-height`, `text-align`, `letter-spacing` | `width`, `height`, `background` |
| `visibility`, `cursor`, `list-style` | `display`, `position`, `overflow` |

A lógica: propriedades de **texto** são herdadas (faz sentido que o parágrafo use a fonte do `body`); propriedades de **caixa** não são (não faz sentido que todo filho de uma caixa com borda ganhe borda também).

A herança é o que permite escrever pouco CSS:

```css
body {
  font-family: var(--fonte-base);
  font-size: 1rem;
  line-height: 1.6;
  color: var(--cor-texto);
}
/* O site inteiro herda estas quatro declarações. */
```

Quatro palavras-chave funcionam em **qualquer** propriedade e controlam a herança na mão:

```css
.filho {
  border: inherit;   /* força a herança de uma propriedade que não é herdada */
  color: initial;    /* volta ao valor padrão da especificação (preto, no caso) */
  padding: unset;    /* herda se for herdável; volta ao inicial se não for */
  margin: revert;    /* volta ao valor que o NAVEGADOR daria */
}
```

`revert` é a mais útil das quatro: ela desfaz o seu CSS sem desfazer o do navegador. Útil quando um reset agressivo tirou algo que você quer de volta em um caso específico.

## 3. Cores

### 3.1 As notações

```css
color: red;                       /* 1. nome — 147 nomes padronizados */
color: #0b3d5c;                   /* 2. hexadecimal: #RRGGBB */
color: #f0a;                      /* 3. hex abreviado = #ff00aa */
color: #0b3d5c80;                 /* 4. hex com alfa (últimos dois dígitos) */
color: rgb(11, 61, 92);           /* 5. RGB decimal, 0 a 255 */
color: rgba(11, 61, 92, 0.5);     /* 6. RGB com transparência, 0 a 1 */
color: hsl(203, 79%, 20%);        /* 7. matiz, saturação, luminosidade */
color: hsla(203, 79%, 20%, 0.5);  /* 8. HSL com transparência */
```

O hexadecimal é a notação mais comum porque é a que as ferramentas de design cospem. Mas ele é ilegível para humanos: olhando `#0b3d5c` você não sabe se é claro ou escuro, nem qual é o "primo mais claro" dessa cor.

### 3.2 HSL: a notação que serve para pensar

`hsl()` descreve a cor como uma pessoa descreveria:

- **H** (*hue*, matiz): a cor em si, em graus de 0 a 360 no círculo cromático (0 vermelho, 120 verde, 240 azul).
- **S** (*saturation*, saturação): quanto de cor, de 0% (cinza) a 100% (vibrante).
- **L** (*lightness*, luminosidade): de 0% (preto) a 100% (branco); 50% é a cor "pura".

Isso torna trivial construir uma paleta coerente: **mantenha o H, varie o L**.

```css
:root {
  --azul-900: hsl(203, 79%, 20%);   /* mais escuro  — texto sobre claro */
  --azul-700: hsl(203, 79%, 32%);
  --azul-500: hsl(203, 75%, 40%);   /* a cor "da marca" */
  --azul-300: hsl(203, 60%, 70%);
  --azul-100: hsl(203, 60%, 94%);   /* mais claro — fundos suaves */
}
```

Cinco tons que combinam entre si, escritos em cinco linhas, sem nenhuma ferramenta. Tente fazer isso adivinhando hexadecimais.

> **💡 Dica**
> No DevTools, clique no quadradinho de cor ao lado de qualquer declaração de `color` ou `background`: abre o seletor de cores. Clique no rótulo do formato (embaixo, à direita do valor) e ele **converte** entre hex, `rgb` e `hsl` na hora. É a maneira mais rápida de descobrir o `hsl()` equivalente a um hexadecimal que veio de um layout.

**E o `oklch()`?** Existe uma notação mais nova, `oklch(luminosidade croma matiz)` — por exemplo, `oklch(45% 0.09 240)`. Ela resolve um defeito do HSL: dois tons com o mesmo `L` em HSL podem parecer bem diferentes em brilho para o olho humano (compare um amarelo e um azul com `L: 50%`). O `oklch` é perceptualmente uniforme, ou seja, mesma luminosidade significa mesmo brilho aparente. Já funciona em todos os navegadores atuais e vale conhecer; nesta disciplina continuamos com `hsl()` e hexadecimal, que é o que você vai encontrar em 99% do código existente.

### 3.3 Fundos

```css
background-color: #f5f5f5;
background-image: url("../img/textura.png");
background-repeat: no-repeat;
background-position: center;
background-size: cover;      /* cobre todo o espaço, cortando o excesso */
background-size: contain;    /* cabe inteira, podendo sobrar espaço */

/* Forma abreviada: cor, imagem, repetição, posição / tamanho */
background: #f5f5f5 url("../img/fundo.jpg") no-repeat center / cover;

/* Gradientes são imagens, não cores */
background-image: linear-gradient(to right, #0b3d5c, #1a7fb5);
background-image: linear-gradient(160deg, #0b3d5c 0%, #1a7fb5 100%);
background-image: radial-gradient(circle, #ffffff, #cccccc);
```

Repare no caminho `url("../img/textura.png")`: dentro de `css/estilo.css`, o `../` sobe para a raiz do site antes de entrar em `img/`. **Caminhos em CSS são relativos ao arquivo CSS**, não ao HTML — é a causa mais comum de imagem de fundo que não aparece.

### 3.4 Contraste é requisito, não gosto

A WCAG exige **4,5:1** de contraste entre texto e fundo (3:1 para texto grande — 24 px, ou 18,5 px em negrito). Texto cinza-claro sobre branco reprova; texto branco sobre amarelo reprova com folga.

Verifique em <https://webaim.org/resources/contrastchecker/> — dois campos, um resultado, dez segundos. As cores do site do evento:

| Par (texto sobre fundo) | Razão | Serve para |
|---|---|---|
| `#0b3d5c` sobre `#ffffff` | 11,4:1 | Texto, títulos, links — passa AAA |
| `#ffffff` sobre `#0b3d5c` | 11,4:1 | Cabeçalho, rodapé e botão primário |
| `#333333` sobre `#f7f9fb` | 12,0:1 | Corpo de texto do site inteiro |
| `#ffffff` sobre `#1a7fb5` | 4,4:1 | **Só texto grande e bordas** — reprova em texto normal |

Essa última linha é o tipo de descoberta que o verificador entrega e o olho não: `#1a7fb5` parece perfeitamente legível, e falha por pouco. Por isso `--cor-secundaria` é usada, no site do evento, em **bordas, ícones e estado `:hover`** — nunca como fundo de texto pequeno.

> **⚠️ Atenção**
> Nunca comunique uma informação **só** por cor. Campo inválido com borda vermelha e mais nada exclui quem tem daltonismo (cerca de 8% dos homens). Acrescente sempre um segundo sinal: um ícone, um texto, uma mudança de espessura de borda. Isso entra no checklist de qualidade dos Marcos 2 e 3.

## 4. Unidades

### 4.1 Absolutas

| Unidade | Uso recomendado |
|---|---|
| `px` | Pixel de referência. Previsível — bom para bordas, sombras e raios |
| `pt`, `cm`, `mm`, `in` | Impressão. Não use para tela |

### 4.2 Relativas — prefira sempre

| Unidade | Relativa a | Observação |
|---|---|---|
| `%` | Uma medida do elemento pai | Ótima para largura |
| `em` | `font-size` do **próprio elemento** (ou do pai, quando aplicada ao próprio `font-size`) | Acumula em aninhamentos |
| `rem` | `font-size` da **raiz** (`<html>`) | Previsível; padrão para tipografia |
| `vw` / `vh` | 1% da largura / altura da janela | `100vh` é a altura total da tela |
| `vmin` / `vmax` | Menor / maior dimensão da janela | Útil em elementos quadrados |
| `ch` | Largura do caractere "0" da fonte atual | Ideal para limitar a linha de texto |

```css
html  { font-size: 100%; }        /* respeita o padrão do navegador: 16px */
h1    { font-size: 2rem; }        /* 32px */
p     { font-size: 1rem; }        /* 16px */
small { font-size: 0.875rem; }    /* 14px */
```

> **⚠️ Atenção**
> **A armadilha do `em`.** Se `.pai { font-size: 1.5em }` e, dentro dele, `.filho { font-size: 1.5em }`, o filho fica com 2,25× o tamanho base. Em três níveis, 3,4×. Com `rem` isso não acontece, porque a referência é sempre a raiz — a fonte de um item de menu não muda porque alguém aninhou mais uma `<div>`. Use `rem` para tipografia e `em` só quando **quiser** essa proporcionalidade local (o padding de um botão que cresce junto com o texto dele, por exemplo).

> **🧠 Você sabia?**
> Nunca escreva `html { font-size: 14px }` para "deixar tudo menor". Essa linha é uma das piores coisas que se pode fazer com acessibilidade: uma pessoa com baixa visão que configurou o navegador para fonte 20 px acabou de ter a escolha dela anulada — e não faz ideia do porquê. Todo o valor do `rem` está em ele ser relativo a uma raiz que o **usuário** controla. Se você precisa de tudo menor, reduza os valores em `rem` das suas regras, não a raiz. `html { font-size: 100% }` é a única declaração de tamanho de raiz aceitável nesta disciplina.

### 4.3 Fazendo contas: `calc()`, `min()`, `max()` e `clamp()`

```css
width:  calc(100% - 40px);        /* largura total menos um espaço fixo */
height: calc(100vh - 80px);       /* tela inteira menos o cabeçalho */

width: min(1100px, 100% - 2rem);  /* o MENOR dos dois: nunca estoura a tela */
width: max(300px, 30%);           /* o MAIOR dos dois: nunca fica estreito demais */

font-size: clamp(1rem, 2.5vw, 1.5rem);  /* mínimo, ideal fluido, máximo */
```

Os **espaços em volta dos operadores** de `calc()` são obrigatórios: `calc(100%-40px)` não funciona, e o navegador não avisa. Motivo histórico: sem espaço, `-40px` seria interpretado como um número negativo, não como uma subtração.

`clamp()` é a peça central da tipografia fluida da Aula 08 — por ora, guarde a leitura: "no mínimo 1rem, idealmente 2,5% da largura da janela, no máximo 1.5rem".

## 5. Tipografia

Tipografia é 90% da aparência de um site. Antes de escolher cor, escolha bem a fonte, o tamanho e o espaçamento.

### 5.1 A pilha de fontes

```css
body {
  font-family: "Inter", Arial, sans-serif;
}
```

A pilha é lida da esquerda para a direita: o navegador usa **a primeira que existir** no sistema do usuário. Sempre termine com uma família genérica (`sans-serif`, `serif`, `monospace`) — é a garantia de que existe um fim de linha.

Nomes com espaço vão entre aspas (`"Segoe UI"`). Uma pilha "de sistema" — que usa a fonte nativa de cada sistema operacional e não baixa nada — é uma escolha profissional e rápida:

```css
font-family: system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
```

### 5.2 As propriedades

```css
body {
  font-family: var(--fonte-base);
  font-size: 1rem;
  font-weight: 400;         /* 100 a 900; 400 = normal, 700 = negrito */
  font-style: normal;       /* normal | italic | oblique */
  line-height: 1.6;         /* SEM unidade = múltiplo do font-size. Recomendado */
  letter-spacing: 0.01em;
  color: var(--cor-texto);
}

h1 {
  font-size: 2rem;
  line-height: 1.2;         /* títulos pedem entrelinha menor */
  text-transform: none;     /* uppercase | lowercase | capitalize */
  text-align: left;         /* center | right | justify */
}

a {
  text-decoration: underline;
  text-underline-offset: 2px;   /* afasta o sublinhado da base das letras */
}
```

> **💡 Dica**
> `line-height` **sem unidade** (`1.6`) é sempre a escolha certa. Com unidade (`line-height: 24px` ou `1.6em`), o valor **calculado** é herdado pelos filhos — então um título de 2rem dentro de um `body` com `line-height: 24px` herda 24 px de entrelinha e as letras se sobrepõem. Sem unidade, o que se herda é o **fator**, e cada elemento calcula a própria entrelinha a partir do próprio tamanho.

### 5.3 Uma escala tipográfica

Não escolha tamanhos no chute. Parta de 1rem e multiplique por uma razão constante (1,25 é uma boa escolha para telas):

| Nome | Valor | Uso |
|---|---|---|
| `2.5rem` | 40 px | Título da página inicial |
| `2rem` | 32 px | `h1` |
| `1.5rem` | 24 px | `h2` |
| `1.25rem` | 20 px | `h3` |
| `1rem` | 16 px | Corpo de texto |
| `0.875rem` | 14 px | Legendas, metadados, rodapé |

Seis tamanhos bastam para um site inteiro. Se você precisou de um sétimo, provavelmente precisava era de outro peso (`font-weight`) ou de outra cor.

### 5.4 Fontes externas (Google Fonts)

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap"
      rel="stylesheet">
```

```css
body { font-family: "Inter", Arial, sans-serif; }
```

- `preconnect` abre a conexão com o servidor de fontes antes de ela ser necessária — economiza cerca de 100 ms.
- `wght@400;600;700` importa **três** pesos. Cada peso é um arquivo baixado: importar oito "por precaução" pode custar centenas de kilobytes e atrasar a primeira pintura da página.
- `display=swap` mostra o texto imediatamente com a fonte de reserva e troca quando a externa chegar. Sem ele, alguns navegadores escondem o texto por até três segundos.

> **🔎 Por baixo do capô**
> A troca de fonte tem dois nomes que aparecem em toda auditoria de performance: **FOUT** (*flash of unstyled text*, o texto aparece com a fonte de reserva e "pula" quando a definitiva carrega) e **FOIT** (*flash of invisible text*, o texto simplesmente não aparece até a fonte chegar). `display=swap` escolhe deliberadamente o FOUT — porque texto visível com a fonte errada é melhor do que página em branco. Para reduzir o "pulo", escolha uma fonte de reserva com largura parecida (Arial para Inter, Georgia para uma serifada) — é o motivo real de a pilha de fontes ter mais de um nome.

### 5.5 Legibilidade: quatro números que resolvem

- Corpo de texto entre **1rem e 1.125rem**. Menor que isso, cansa.
- `line-height` entre **1.5 e 1.7** para texto corrido.
- Largura de linha entre **45 e 75 caracteres** — em CSS, `max-width: 65ch`. Linha muito longa faz o olho perder o começo da seguinte.
- Evite `text-align: justify` na web: sem hifenização, ele abre "rios" de espaço em branco no meio do parágrafo.

## 6. Variáveis CSS (custom properties)

### 6.1 Declarar e usar

```css
:root {
  --cor-primaria: #0b3d5c;
  --cor-secundaria: #1a7fb5;
  --espaco-medio: 16px;
  --raio-borda: 8px;
}

.botao {
  background-color: var(--cor-primaria);
  padding: var(--espaco-medio);
  border-radius: var(--raio-borda);
}

.botao:hover {
  background-color: var(--cor-secundaria);
}
```

O nome **precisa** começar com dois hífens (`--`) e diferencia maiúsculas de minúsculas (`--Cor` e `--cor` são variáveis diferentes). `:root` é o seletor do elemento `<html>`: declarar ali torna a variável visível na página inteira.

### 6.2 Escopo e herança

Variáveis são **herdadas**, e é isso que as torna poderosas: você pode redefinir uma variável em qualquer escopo e tudo abaixo dela muda.

```css
:root       { --cor-fundo-cartao: #ffffff; }
.destaque   { --cor-fundo-cartao: #fff8e1; }   /* só dentro de .destaque */

.cartao { background-color: var(--cor-fundo-cartao); }
```

Um `.cartao` dentro de `.destaque` fica amarelado; os outros continuam brancos — e a regra do `.cartao` não foi tocada. É esse mecanismo que permite temas claro e escuro trocando poucas linhas (assunto da Aula 09 e requisito do projeto final).

### 6.3 Valor de reserva

```css
.cartao { box-shadow: var(--sombra-cartao, 0 1px 4px rgba(0, 0, 0, 0.15)); }
```

O segundo argumento de `var()` é usado quando a variável não existe. Útil em componentes que podem ser copiados para outro projeto.

### 6.4 O que vira variável e o que não vira

Vire variável tudo que **se repete e pode mudar junto**: cores da marca, espaçamentos da escala, raios de borda, sombras, a pilha de fontes. Não vire variável valores que aparecem uma vez só, nem valores que por acaso são iguais mas não têm relação (o `padding` de um botão e a `margin` de um parágrafo podem ser 16 px hoje e nada obriga que continuem iguais).

E cuidado com o nome: `--azul-escuro` é um nome ruim, porque no dia em que a identidade virar verde, a variável passa a mentir. `--cor-primaria` continua verdadeira.

## 7. Organizando a folha de estilo

### 7.1 As sete seções

Uma folha de estilo cresce todo dia. Sem uma ordem combinada, em duas semanas ninguém acha nada — e regras duplicadas começam a brigar. A ordem que você vai usar da Aula 06 até a Aula 09:

```css
/* 1. Reset e box-sizing        */
/* 2. Variáveis em :root        */
/* 3. Base (body, tipografia, links, imagens) */
/* 4. Layout (header, main, footer, contêineres) */
/* 5. Componentes (botões, cartões, tabelas, formulários) */
/* 6. Utilitários (.texto-centro, .oculto) */
/* 7. Media queries (Aula 08)   */
```

A ordem não é arbitrária: ela vai **do mais genérico ao mais específico**, e a etapa 3 da cascata (ordem no arquivo) faz o resto. Um utilitário escrito na seção 6 sobrescreve um componente da seção 5 sem precisar de especificidade extra — que é exatamente o que se espera de um utilitário.

### 7.2 Nomes de classe que não mentem

O nome da classe deve descrever a **função**, não a aparência:

| Ruim | Bom | Por quê |
|---|---|---|
| `.texto-vermelho` | `.mensagem-erro` | Se mudar para laranja, o nome não mente |
| `.caixa-esquerda` | `.barra-lateral` | Se mudar de lado, o nome continua válido |
| `.f18b` | `.titulo-secao` | Legibilidade para quem lê depois (inclusive você) |
| `.azul-grande` | `.botao--primario` | Descreve o papel, não os pixels |

O padrão `bloco__elemento--modificador` (`.cartao`, `.cartao__titulo`, `.cartao--destaque`) tem nome: **BEM**. Você não é obrigado a segui-lo à risca nesta disciplina, mas vai encontrá-lo na Aula 07 e em quase todo projeto profissional — e ele resolve um problema real: um nome de classe longo e específico nunca colide com o de outro componente.

## 💻 Mão na massa — O sistema de design do site do evento

Hoje você reescreve `css/estilo.css` inteiro. A folha da Aula 05 tinha 5 seções e 3 variáveis; a nova terá 7 seções, um sistema de design em 10 variáveis, uma escala tipográfica, botões com todos os estados e a tabela de programação estilizada.

### Passo 1 — Importar a fonte nas cinco páginas

Antes do `<link rel="stylesheet" href="css/estilo.css">` de **cada** página, acrescente os três links da fonte:

**`site-evento/index.html` (no `<head>`, antes do link do CSS)**

```html
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap"
        rel="stylesheet">
  <link rel="stylesheet" href="css/estilo.css">
```

Repita nas cinco páginas. A ordem importa: a fonte precisa estar disponível quando o seu CSS pedir por ela.

### Passo 2 — Simplificar o `<main>` das cinco páginas

Na Aula 05, todas as regiões receberam um `<div class="container">`. O `<main>` não precisa dele: como o conteúdo principal não tem fundo colorido sangrando até as bordas da tela, o próprio `<main>` pode assumir a largura máxima do projeto. Em cada página, **remova o `<div class="container">` de dentro do `<main>`** (e o `</div>` correspondente), promovendo as seções um nível:

**`site-evento/index.html` (trecho do `<main>`, depois da mudança)**

```html
  <main>
    <section class="hero">
      <h2>Três noites de palestras, minicursos e maratona de programação</h2>
      <p>Participação gratuita, com certificado de 20 horas para quem comparecer a pelo menos 75% das atividades.</p>
      <a href="inscricao.html" class="botao">Inscreva-se</a>
    </section>
  </main>
```

O `<div class="container">` continua no `<header>` e no `<footer>`, onde ele é necessário: essas duas regiões têm fundo azul de ponta a ponta da tela, e só o **conteúdo** delas fica limitado a 1100 px — o mesmo 1100 px que a Aula 05 fixou.

> **💡 Dica**
> Guarde esse número. Na Aula 07 ele vira a variável `--largura-max`, e a classe `.container` volta ao `<main>` — não mais como uma `<div>` interna, mas aplicada ao próprio `<main>` ou à `<section>` de topo. A largura nunca muda; o que muda é **quem** carrega a classe.

### Passo 3 — Reset e variáveis

Abra `css/estilo.css` e substitua o arquivo inteiro. Comece pelas duas primeiras seções:

**`site-evento/css/estilo.css` — seções 1 e 2**

```css
/* ==========================================================
   Semana Acadêmica de Sistemas de Informação — folha de estilo
   1. Reset · 2. Variáveis · 3. Base · 4. Layout
   5. Componentes · 6. Utilitários · 7. Media queries
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
  --fonte-base: "Inter", Arial, sans-serif;
  --espaco-pequeno: 8px;
  --espaco-medio: 16px;
  --espaco-grande: 32px;
  --raio-borda: 8px;
  --sombra-cartao: 0 2px 8px rgba(0, 0, 0, 0.1);
}
```

Dez variáveis: quatro cores, uma fonte, três espaçamentos, um raio e uma sombra. É o **sistema de design** do projeto — a partir de agora, nenhum valor de cor ou de espaçamento é escrito solto no meio da folha. Na Aula 07 você vai acrescentar mais três.

> **💡 Dica**
> Três espaçamentos parecem pouco, e são suficientes. Uma escala curta (8 / 16 / 32) força consistência: o olho percebe imediatamente quando um espaço "não é nenhum dos três". Quando você precisar de um valor intermediário, quase sempre o certo é usar um dos três, não inventar o quarto.

### Passo 4 — Estilos base: tipografia, links e imagens

**`site-evento/css/estilo.css` — seção 3**

```css
/* 3. Base */
html {
  font-size: 100%;              /* respeita o tamanho escolhido pelo usuário */
  scroll-behavior: smooth;      /* rolagem suave nas âncoras "Voltar ao topo" */
}

body {
  font-family: var(--fonte-base);
  font-size: 1rem;
  line-height: 1.6;
  color: var(--cor-texto);
  background-color: var(--cor-fundo);
}

h1,
h2,
h3 {
  line-height: 1.2;
  color: var(--cor-primaria);
  margin-bottom: var(--espaco-medio);
}

h1 { font-size: 2rem; }
h2 { font-size: 1.5rem; }
h3 { font-size: 1.25rem; }

p,
ul,
ol,
dl,
table {
  margin-bottom: var(--espaco-medio);
}

p {
  max-width: 65ch;              /* linha de leitura confortável */
}

ul,
ol {
  padding-left: var(--espaco-grande);   /* devolve o recuo que o reset tirou */
}

a {
  color: var(--cor-primaria);
  text-decoration: underline;
  text-underline-offset: 2px;
}

a:hover {
  color: var(--cor-secundaria);
}

/* Sinaliza links que saem do site */
a[href^="http"]::after {
  content: " ↗";
  font-size: .875rem;
}

/* Foco visível em TUDO que é focável */
:focus-visible {
  outline: 3px solid var(--cor-secundaria);
  outline-offset: 2px;
}

img,
video {
  max-width: 100%;
  height: auto;
  display: block;
}
```

Quatro decisões que merecem explicação:

- **`ul, ol { padding-left: var(--espaco-grande) }`** devolve o recuo que o reset universal apagou. Sem essa linha, os marcadores das listas ficam para fora da caixa e somem no corte.
- **`p { max-width: 65ch }`** limita a linha de leitura mesmo antes de existir qualquer layout. É o ajuste de legibilidade mais barato que existe.
- **`:focus-visible` sem seletor de elemento** aplica-se a tudo que recebe foco: links, botões, campos. Uma regra, o site inteiro acessível pelo teclado.
- **`a[href^="http"]::after`** usa um seletor de atributo para marcar links externos. Como todos os links internos do site são relativos (`programacao.html`), só os externos começam com `http`.

### Passo 5 — Layout: cabeçalho, conteúdo e rodapé

**`site-evento/css/estilo.css` — seção 4**

```css
/* 4. Layout */
.container {
  max-width: 1100px;
  margin: 0 auto;
  padding-inline: var(--espaco-medio);
}

header {
  background-color: var(--cor-primaria);
  color: #ffffff;
  padding-block: var(--espaco-grande);
}

header h1,
header h2 {
  color: #ffffff;
}

header a {
  color: #ffffff;
}

header nav ul {
  padding-left: 0;
  list-style: none;
}

header nav li {
  display: inline-block;              /* menu na horizontal, sem Flexbox ainda */
  margin-right: var(--espaco-medio);
}

main {
  max-width: var(--largura-max, 1100px);
  margin: 0 auto;
  padding: var(--espaco-grande) var(--espaco-medio);
}

main section {
  margin-bottom: var(--espaco-grande);
}

main section > h2 {
  border-bottom: 3px solid var(--cor-secundaria);
  padding-bottom: var(--espaco-pequeno);
}

footer {
  background-color: var(--cor-primaria);
  color: #ffffff;
  text-align: center;
  padding-block: var(--espaco-grande);
}

footer a {
  color: #ffffff;
}

footer p {
  max-width: none;                    /* o rodapé é centralizado, não é leitura corrida */
  margin-inline: auto;
}
```

O menu horizontal com `display: inline-block` é um paliativo consciente: na Aula 07 ele será refeito com Flexbox, que resolve alinhamento e espaçamento de forma muito mais limpa. Por hoje, funciona e não atrapalha.

> **⚠️ Atenção**
> As regras `header a { color: #ffffff }` e `footer a { color: #ffffff }` têm especificidade 0-0-2 e vencem `a { color: var(--cor-primaria) }` (0-0-1) — que é o que queremos, porque azul-escuro sobre azul-escuro seria ilegível. Se você tivesse escrito `.container a`, a especificidade seria 0-1-1 e o resultado seria o mesmo; mas aí o `main` também seria afetado, porque ele *também* estava dentro de um `.container` até o Passo 2. É por isso que seletores mais precisos são mais fáceis de manter.

### Passo 6 — Componentes: botão, cartão e tabela

**`site-evento/css/estilo.css` — seção 5, botões**

```css
/* 5. Componentes */
.botao {
  display: inline-block;
  padding: 12px 24px;
  background-color: var(--cor-primaria);
  color: #ffffff;
  font-weight: 600;
  text-decoration: none;
  border: 2px solid var(--cor-primaria);
  border-radius: var(--raio-borda);
  cursor: pointer;
}

.botao:hover,
.botao:focus-visible {
  background-color: var(--cor-secundaria);
  border-color: var(--cor-secundaria);
}

.botao:active {
  background-color: #072a40;          /* um tom mais escuro no instante do clique */
}

.botao--contorno {
  background-color: transparent;
  color: var(--cor-primaria);
}

.botao--contorno:hover,
.botao--contorno:focus-visible {
  background-color: var(--cor-primaria);
  color: #ffffff;
}

.botao:disabled,
.botao[aria-disabled="true"] {
  background-color: #9aa8b2;
  border-color: #9aa8b2;
  cursor: not-allowed;
}
```

Quatro estados em um componente só: repouso, `:hover`/`:focus-visible`, `:active` e desabilitado. Um botão que não muda de aparência ao receber foco é um botão quebrado para quem usa teclado.

**`site-evento/css/estilo.css` — seção 5, cartão**

```css
.cartao {
  background-color: #ffffff;
  border: 1px solid #dfe6ec;
  border-radius: var(--raio-borda);
  padding: var(--espaco-medio);
  margin-bottom: var(--espaco-medio);
  box-shadow: var(--sombra-cartao);
}

.cartao h3 {
  margin-bottom: var(--espaco-pequeno);
}

.cartao p:last-child {
  margin-bottom: 0;                   /* sem espaço sobrando no fim do cartão */
}
```

**`site-evento/css/estilo.css` — seção 5, tabela da programação**

```css
table {
  width: 100%;
  border-collapse: collapse;          /* junta as bordas duplas em uma só */
}

caption {
  text-align: left;
  font-weight: 600;
  color: var(--cor-primaria);
  padding-bottom: var(--espaco-pequeno);
}

th,
td {
  padding: var(--espaco-pequeno) var(--espaco-medio);
  border-bottom: 1px solid #dfe6ec;
  text-align: left;
  vertical-align: top;
}

thead th {
  background-color: var(--cor-primaria);
  color: #ffffff;
}

tbody th[scope="colgroup"] {
  background-color: #e8eef3;
  color: var(--cor-primaria);
}

tbody tr:nth-child(even) {
  background-color: #ffffff;          /* zebrado: linhas pares em branco */
}

tbody tr:hover {
  background-color: #eef4f8;
}

tfoot td {
  font-size: .875rem;
  font-style: italic;
}
```

Três seletores desta tabela vieram direto da teoria de hoje: `tbody tr:nth-child(even)` (pseudoclasse estrutural), `tbody th[scope="colgroup"]` (seletor de atributo, aproveitando a semântica que você escreveu na Aula 02) e `tbody tr:hover` (pseudoclasse de estado). Nenhuma classe nova foi necessária — o HTML bem marcado já dizia tudo.

Duas tabelas do site usam essas regras: a da programação, escrita na Aula 02, e a de horário de atendimento em `contato.html`, escrita na Aula 05. Na Aula 07 a programação será redesenhada em cartões; a folha de estilo da tabela **continua valendo** para a de `contato.html`, então nada aqui é desperdício.

> **⚠️ Atenção**
> `border-collapse: collapse` é o que transforma a tabela padrão (com bordas duplas e um espaço entre as células) em uma tabela de aparência profissional. Ela precisa ir no elemento `table`, não nas células — e, com `collapse` ativo, `border-radius` na tabela deixa de ter efeito visível nas células das pontas.

### Passo 7 — Utilitários e o espaço das media queries

**`site-evento/css/estilo.css` — seções 6 e 7**

```css
/* 6. Utilitários */
.texto-centro {
  text-align: center;
}

.sem-margem {
  margin: 0;
}

/* Some da tela, continua existindo para leitores de tela */
.oculto-visualmente {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
}

/* 7. Media queries */
/* Reservado para a Aula 08: mobile first e breakpoints. */
```

`.oculto-visualmente` é o utilitário mais importante da lista. Ele resolve um caso frequente: um rótulo que precisa existir para o leitor de tela mas ficaria redundante na tela (um campo de busca com ícone de lupa, por exemplo). Note que **não** é `display: none`: isso removeria o elemento da árvore de acessibilidade, e ele deixaria de ser lido — o oposto da intenção.

### Passo 8 — Verificar contraste e revisar

1. Abra <https://webaim.org/resources/contrastchecker/> e teste os quatro pares da tabela da seção 3.4.
2. Crie, na raiz do projeto, um arquivo `contraste.md` anotando cada par (texto × fundo), a razão obtida e onde ele é usado. Esse arquivo faz parte do Marco 2 (Aula 10).
3. No DevTools, selecione qualquer texto e abra a aba **Computed**: confira `font-size` (16 px no corpo), `line-height` (25,6 px = 1,6 × 16) e `color`.

### Como testar

1. As cinco páginas abrem no Live Server com a fonte Inter, cabeçalho e rodapé azul-escuros e conteúdo centralizado com no máximo 1100 px.
2. Cada `<h2>` de seção tem a linha azul-clara embaixo; nenhum parágrafo passa de cerca de 65 caracteres por linha.
3. Os links externos (LinkedIn e GitHub, na página de palestrantes) mostram a seta `↗`; os internos, não.
4. Pressionando <kbd>Tab</kbd>, cada link e cada botão ganha um contorno azul de 3 px visível — inclusive dentro do cabeçalho azul.
5. Em `programacao.html`, a tabela ocupa a largura toda, o cabeçalho é branco sobre azul-escuro, as linhas alternam de cor e a linha sob o cursor muda de fundo.
6. Passando o mouse sobre o botão "Inscreva-se", ele fica azul-claro; segurando o clique, escurece.
7. No DevTools, mudar `--cor-primaria` no bloco `:root` muda **cabeçalho, rodapé, títulos, links, botões e cabeçalho da tabela ao mesmo tempo**. Esse é o teste definitivo de que o sistema de design está funcionando: faça, é impressionante.

**Resultado esperado:** o mesmo site da Aula 05, agora com identidade visual coerente, tipografia legível, botões com quatro estados, tabela zebrada e uma folha de estilo em que qualquer alteração de marca custa uma linha. O layout ainda é uma pilha de blocos — isso é a Aula 07.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Escreva o seletor CSS para: (a) todos os parágrafos; (b) elementos com a classe `aviso`; (c) o elemento com `id="topo"`; (d) parágrafos dentro de `article`; (e) apenas os `li` filhos diretos de uma `ul`; (f) links que abrem em nova aba.

**A2.** Qual é a diferença entre `p.destaque` e `p .destaque`? Escreva um trecho de HTML em que o primeiro pega um elemento e o segundo não pega nenhum.

**A3.** Calcule a especificidade (A, B, C) de: (a) `p`; (b) `.cartao`; (c) `#menu a`; (d) `nav ul li a:hover`; (e) `.cartao .titulo span`; (f) `article > p.intro`.

**A4.** Dado o CSS e o HTML abaixo, de que cor fica o parágrafo? Justifique com o cálculo das quatro especificidades.

```css
p           { color: blue; }
.texto      { color: green; }
#principal p { color: red; }
p.texto     { color: orange; }
```

```html
<div id="principal"><p class="texto">Qual cor?</p></div>
```

**A5.** Converta `#1a7fb5` para `rgb()`. Depois escreva a mesma cor com 40% de transparência, nas duas notações que você conhece.

**A6.** Se `html { font-size: 100% }` e o navegador está no padrão, quantos pixels equivalem a `1.5rem`, `0.75rem` e `2.5rem`?

**A7.** Explique a diferença entre `em` e `rem` e descreva, com um exemplo de três níveis aninhados, por que `rem` é preferível para tipografia.

**A8.** Escreva a ordem correta das pseudoclasses de link e explique o que acontece com o `:hover` se ela for invertida.

**A9.** Declare uma variável CSS `--cor-destaque` em `:root` e use-a em duas regras diferentes, uma delas com valor de reserva.

**A10.** Explique o que faz cada um destes seletores de atributo: `a[href^="mailto:"]`, `a[href$=".zip"]`, `input[type="radio"]`, `li[data-dia]`.

**A11.** Por que `line-height: 1.6` é melhor que `line-height: 24px`? Dê um exemplo em que a segunda forma quebra o layout.

**A12.** Diferencie `:nth-child(2)` de `:nth-of-type(2)` usando o HTML `<div><h2>T</h2><p>A</p><p>B</p></div>`. Qual elemento cada um pega?

### Nível B — Aplicação

**B1.** Estilize uma tabela de notas em `exercicios/aula06/notas.html`: `border-collapse: collapse`, cabeçalho com fundo escuro e texto claro, linhas pares com fundo cinza-claro (`:nth-child(even)`), destaque no `:hover` da linha, colunas numéricas alinhadas à direita e `caption` estilizado acima da tabela.

Resultado esperado: a tabela ocupa 100% da largura do contêiner; as bordas não são duplas; as linhas alternam visivelmente; passar o mouse muda o fundo da linha inteira; as notas ficam alinhadas à direita e os nomes à esquerda.

<details markdown="1"><summary>Dica</summary>

Para alinhar só a coluna de notas, use um seletor de posição (`td:nth-child(3)`) ou uma classe nas células numéricas. A segunda opção é mais robusta: se você acrescentar uma coluna, o número muda e o `nth-child` mira a coluna errada.
</details>

**B2.** Construa uma paleta documentada em `exercicios/aula06/paleta.html`: dez quadrados coloridos, cada um exibindo o nome da cor, o hexadecimal e o `hsl()`. Todas as cores declaradas como variáveis em `:root`. A paleta deve ser coerente: uma primária, uma secundária, uma de destaque, três neutros e as quatro cores semânticas (sucesso, alerta, erro, informação).

Resultado esperado: dez blocos, cada um com o nome do papel da cor (não o nome da cor), os dois valores e a razão de contraste com preto e com branco; as cores da mesma família compartilham o matiz (H) e variam a luminosidade (L).

<details markdown="1"><summary>Dica</summary>

Escolha o matiz primeiro (um número de 0 a 360) e construa a família variando só o `L`. Para as semânticas, os matizes convencionais são: sucesso perto de 140, alerta perto de 40, erro perto de 0 e informação perto de 210.
</details>

**B3.** Estilize completamente o formulário de inscrição da Aula 03. Em `css/estilo.css`, na seção 5, acrescente um bloco de formulário: campos com `padding`, borda e `border-radius`; `:focus-visible` com borda colorida; `:invalid` com borda vermelha **e** um segundo sinal que não seja cor; `:valid` discreto; `fieldset` com borda suave e `legend` destacada; rótulos em bloco acima dos campos.

Resultado esperado: a `inscricao.html` fica legível e agradável sem uma linha de JavaScript; navegando por <kbd>Tab</kbd>, cada campo mostra claramente que está focado; um campo obrigatório vazio, depois de tocado, indica o problema por borda **e** por outro sinal visual.

<details markdown="1"><summary>Dica</summary>

`input:invalid` marca o campo como inválido desde o carregamento da página, o que assusta o usuário antes de ele digitar qualquer coisa. Combine com `:not(:placeholder-shown)` para só sinalizar depois que a pessoa começou a preencher. Para o segundo sinal, `::after` no rótulo ou um `border-left` mais grosso funcionam bem.
</details>

**B4.** Experimento de especificidade em `exercicios/aula06/especificidade.html`: uma página com um único parágrafo e **seis** regras diferentes que o atingem, cada uma com uma cor distinta. Preveja no papel qual cor vencerá, teste no navegador e escreva um relatório explicando o resultado com a tabela (A, B, C) de cada seletor.

Resultado esperado: as seis regras, a previsão escrita antes do teste, uma captura de tela do painel Styles mostrando as cinco regras riscadas, e a explicação de por que a vencedora venceu (etapa 2 ou etapa 3 da cascata).

<details markdown="1"><summary>Dica</summary>

Inclua pelo menos um empate proposital — duas regras com a mesma especificidade — para que a etapa 3 (ordem no arquivo) apareça no relatório. E inclua um seletor com `:not()` para testar se você entendeu que o conteúdo dele conta.
</details>

**B5.** Refatoração. Reescreva o CSS abaixo eliminando toda a repetição por meio de variáveis, agrupamento de seletores e herança. Comente cada mudança e conte as linhas antes e depois.

```css
.header  { background-color: #2c3e50; padding: 20px; font-family: Arial; }
.footer  { background-color: #2c3e50; padding: 20px; font-family: Arial; }
.sidebar { background-color: #34495e; padding: 20px; font-family: Arial; }
.header h1  { color: #ecf0f1; font-family: Arial; }
.footer p   { color: #ecf0f1; font-family: Arial; }
.sidebar h2 { color: #ecf0f1; font-family: Arial; }
```

Resultado esperado: a versão refatorada tem menos da metade das linhas, nenhuma cor repetida em literal, `font-family` declarada uma única vez (no `body`, aproveitando a herança) e um comentário por decisão tomada.

<details markdown="1"><summary>Dica</summary>

`font-family` é herdada: declarar no `body` elimina as seis repetições de uma vez. As três cores viram duas variáveis (`--cor-superficie-escura` e `--cor-texto-claro`) mais uma variação. E `.header, .footer` agrupados resolvem as duas primeiras regras em uma.
</details>

### Nível C — Desafio

**C1.** Sistema de design documentado. Crie `design-system.css` e `design-system.html` no seu **projeto autoral**, documentando visualmente o seu sistema: paleta completa em variáveis (com o papel de cada cor), escala tipográfica (seis tamanhos, cada um com nome e valor em `rem`), escala de espaçamentos (três a cinco níveis), botões em quatro variações (primário, secundário, contorno, desabilitado) com os quatro estados cada, campos de formulário em todos os estados, um cartão e um alerta em quatro cores semânticas. Todos os contrastes precisam passar no WCAG AA — apresente a tabela de verificação.

<details markdown="1"><summary>Dica</summary>

Construa a página como um catálogo: uma seção por família de componente, com o exemplo visual à esquerda e o código que o produz à direita (dentro de `<pre><code>`). Essa página é o seu material de consulta pelo resto da disciplina e entra bem no Marco 2 — e é exatamente assim que sistemas de design profissionais são documentados.
</details>

## 🏆 Desafios

### ⭐ Detetive de especificidade
Tags: css, investigacao, devtools

Existe um estilo que "não pega" em praticamente todo projeto de CSS — e quase sempre a culpa é da especificidade. Neste desafio você vai treinar o olho: dada uma lista de conflitos reais, prever quem vence **antes** de abrir o navegador e depois conferir. Quem acerta dez de dez raramente volta a perder tempo caçando esse tipo de bug.

**Critérios de pronto**

- Um arquivo `detetive.html` com dez pares de regras conflitantes, cada par atingindo um elemento diferente da página.
- Uma tabela em `previsoes.md` com, para cada par: os dois seletores, a especificidade calculada de cada um, a sua previsão e o resultado observado.
- Pelo menos dois pares em que a decisão é tomada pela **etapa 3** (ordem no arquivo), não pela especificidade.
- Pelo menos um par envolvendo `:not()` e um envolvendo um seletor de atributo.
- Uma captura de tela do painel **Styles** de um dos casos, com a regra vencida riscada, e uma frase explicando o que o DevTools está mostrando.

<details markdown="1"><summary>Pistas</summary>

1. Comece pelos casos fáceis (`p` × `.classe`) e vá subindo até `#id` × muitas classes — a surpresa está sempre nos empates.
2. `:not(.a)` não conta como pseudoclasse, mas o `.a` de dentro conta. Teste e confirme.
3. Um `style=""` inline vence qualquer seletor: inclua um par com ele e explique por que isso torna o atributo `style` uma má ideia em código de produção.
4. No painel Styles, as regras aparecem da mais específica para a menos específica, de cima para baixo. Use isso para conferir sua tabela em segundos.
</details>

### ⭐⭐ A paleta que ninguém consegue ler
Tags: css, acessibilidade, investigacao

Escolha três sites reais que você usa toda semana — um portal público, uma loja e uma rede social — e audite o contraste deles. Você vai encontrar texto cinza-claro sobre branco, botão desabilitado ilegível e link que só se distingue do texto pela cor (o que também reprova, por outro critério da WCAG). Depois, conserte: reescreva a paleta de um deles mantendo a identidade visual e passando em AA.

**Critérios de pronto**

- Uma tabela com pelo menos doze pares de cor auditados (texto × fundo), a razão de contraste medida e o veredito (AA, AAA, reprova).
- Pelo menos três reprovações encontradas, com captura de tela da tela original.
- Uma paleta corrigida de um dos sites, em variáveis CSS, com cada cor ajustada apenas na luminosidade (o matiz da marca precisa ser preservado).
- Uma página `antes-depois.html` mostrando os dois estados lado a lado, com conteúdo próprio.
- Uma frase por correção explicando o que mudou e por quanto passou a razão de contraste.

<details markdown="1"><summary>Pistas</summary>

1. O verificador do WebAIM aceita colar os dois hexadecimais; para pegar os hexadecimais do site, use o conta-gotas do seletor de cores do DevTools.
2. O Lighthouse (aba do DevTools) tem uma auditoria de contraste que lista os elementos reprovados de uma vez — use como ponto de partida, não como conclusão.
3. Para corrigir mantendo a marca: converta a cor para `hsl()`, deixe H e S intactos e baixe (ou suba) o L de 5 em 5 pontos até passar.
4. Texto grande tem exigência menor (3:1). Antes de escurecer um título gigante, confira se ele já não passa.
</details>

### ⭐⭐ Reconstruindo um componente só com seletores
Tags: css, html, refatoracao, acessibilidade

Pegue este HTML sujo, cheio de classes que descrevem aparência, e reconstrua o mesmo visual **sem tocar no HTML** — usando apenas seletores de tipo, de atributo, combinadores e pseudoclasses. Depois reescreva o HTML como ele deveria ser e compare as duas folhas de estilo. O objetivo é sentir na prática o que um HTML semântico economiza de CSS.

**`componente-sujo.html`**

```html
<div class="caixa-branca-borda-cinza">
  <div class="texto-azul-grande-negrito">Minicurso de Git e GitHub</div>
  <div class="texto-cinza-pequeno">Dia 2 · 19h · Laboratório 2</div>
  <div class="texto-normal">Do primeiro commit ao primeiro pull request, em duas horas.</div>
  <div class="linha-botoes">
    <span class="botao-azul" onclick="inscrever()">Inscrever-se</span>
    <span class="botao-branco" onclick="detalhes()">Ver detalhes</span>
  </div>
</div>
```

**Critérios de pronto**

- Uma folha `versao-a.css` que reproduz o visual do componente sem alterar uma vírgula do HTML acima.
- Um arquivo `componente-limpo.html` com a mesma informação em HTML semântico (`article`, `h3`, `time`, `p`, `a` ou `button`) e sem nenhuma classe que descreva aparência.
- Uma folha `versao-b.css` para a versão limpa, com o mesmo resultado visual.
- Uma comparação: número de linhas de cada folha, número de classes de cada HTML e três problemas de acessibilidade que a versão suja tinha e a limpa não tem.
- Os dois componentes precisam ser utilizáveis por teclado — o que, na versão suja, exige explicar por que `<span onclick>` não é um botão.

<details markdown="1"><summary>Pistas</summary>

1. Na versão A, `div:first-child`, `div:nth-child(2)` e `.linha-botoes span:first-child` fazem quase todo o trabalho — e você vai perceber como isso é frágil.
2. Na versão B, `article h3`, `article time` e `article .botao` bastam, e o CSS sobrevive a uma reordenação do conteúdo.
3. Um `<span>` não é focável nem anunciado como botão. Liste isso, junto com a ausência de rótulo e a dependência de JavaScript inline.
4. Meça o tempo: quanto você demorou para escrever cada folha? Esse número também é um resultado.
</details>

### ⭐⭐⭐ Clone visual de uma identidade real
Tags: css, investigacao, projeto, acessibilidade

Escolha a página inicial de um site cuja identidade visual você admira e reproduza **a identidade** — paleta, tipografia, escala de espaçamentos, estilo de botões, tratamento de links — em uma página com conteúdo totalmente diferente e seu. Não é copiar o layout (isso é a Aula 07): é extrair o **sistema** por trás da aparência e escrevê-lo em variáveis. Ao terminar, você vai olhar para qualquer site e enxergar as decisões, não os pixels.

**Critérios de pronto**

- Um arquivo `identidade.css` com todo o sistema em variáveis: paleta com o papel de cada cor, escala tipográfica completa, escala de espaçamentos, raios e sombras.
- Uma página `clone.html` com conteúdo próprio (pode ser sobre o seu projeto autoral) que usa **apenas** as variáveis — nenhum valor de cor ou espaçamento escrito solto.
- Um documento de meia página analisando as decisões do site original: por que essas cores, por que essa escala, qual é a razão entre os tamanhos de fonte, quantos espaçamentos diferentes ele usa de verdade.
- Uma tabela de contraste provando que a sua versão passa em AA em todos os pares de texto — inclusive se o original não passar (e diga se não passa).
- A troca de tema: mudando **apenas** os valores dentro do `:root`, a página inteira assume outra identidade coerente. Entregue as duas capturas de tela.

<details markdown="1"><summary>Pistas</summary>

1. No DevTools, a aba **Computed** de um elemento mostra os valores finais; anote `font-size`, `line-height`, `padding` e `color` de uns dez elementos e procure os padrões. Você vai descobrir que quase todo site usa cinco ou seis valores, repetidos.
2. Muitos sites profissionais já expõem o sistema deles: procure por `--` no painel Styles do elemento `<html>` e veja as variáveis do próprio site.
3. Para a escala tipográfica, divida cada tamanho pelo anterior: se der sempre perto de 1,25 ou de 1,333, você encontrou a razão.
4. O teste final do sistema é o item 5 dos critérios: se trocar o `:root` não muda tudo, é porque ainda há valores soltos. Procure-os com <kbd>Ctrl</kbd>+<kbd>F</kbd> por `#` no seu CSS.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| A regra seguinte é ignorada em silêncio | Falta o `;` no fim da declaração anterior, ou foi usado `//` como comentário | Toda declaração termina com `;`; em CSS o comentário é `/* assim */` |
| O estilo "não pega" e não há erro nenhum | Espaço acidental no seletor: `p .classe` em vez de `p.classe` | Leia o seletor em voz alta e confira no console com `document.querySelectorAll("…")` |
| Uma regra com `#id` não consegue ser sobrescrita por classes | `id` foi usado para estilizar; 1-0-0 vence qualquer 0-n-0 | Troque o `id` por uma classe; reserve `id` para âncoras, `for` e JavaScript |
| O `:hover` do link não funciona em links já visitados | Ordem LVHA quebrada: `:hover` escrito antes de `:visited` | Escreva sempre `:link`, `:visited`, `:hover`, `:active` nessa ordem |
| O `::after` simplesmente não aparece | Falta a propriedade `content` | `content` é obrigatória em `::before`/`::after`; use `content: ""` se for só decoração |
| Layouts em porcentagem estouram a caixa | `box-sizing: border-box` não foi aplicado; `padding` e `border` somam à largura | Mantenha o reset `*, *::before, *::after { box-sizing: border-box; }` |
| A fonte fica gigante em elementos aninhados | Uso de `em` para `font-size` em vários níveis, acumulando | Use `rem` para tipografia; deixe `em` para espaçamentos internos de um componente |
| A imagem de fundo não aparece, e a aba Network mostra `404` | Caminho relativo ao HTML em vez de relativo ao arquivo CSS | Dentro de `css/estilo.css`, use `url("../img/arquivo.png")` |
| `calc(100%-40px)` não tem efeito nenhum | Faltam os espaços em volta do operador | Escreva `calc(100% - 40px)`; os espaços são obrigatórios |
| Texto cinza-claro sobre branco reprova na auditoria | Contraste abaixo de 4,5:1 | Verifique no WebAIM e escureça baixando o `L` do `hsl()` até passar |
| Todo o site perdeu o contorno de foco | Alguém escreveu `outline: none` para "ficar mais limpo" | Nunca remova sem substituir; use `:focus-visible` com `outline` e `outline-offset` |
| As bordas da tabela ficam duplas e com espaço entre células | `border-collapse` continua no valor padrão `separate` | `table { border-collapse: collapse; }` |
| Um `!important` novo foi preciso para vencer outro `!important` | Escalada de importância causada por má arquitetura de seletores | Remova os dois e resolva por especificidade ou por ordem na folha |

## 🏠 Para praticar depois da aula (1 h)

**Parte 1 — Leitura (20 min).** SILVA, Maurício Samy. *Criando sites com HTML*, capítulos de seletores e cascata. Na MDN em pt-BR: "Seletores CSS" e "Cascata, especificidade e herança" (links em Para aprofundar). Anote um seletor que apareceu na leitura e não nesta aula.

**Parte 2 — Produção (30 min).** Hoje fecha o **Marco 1** (instruções completas logo abaixo). Além dele, produza o exercício **B5** (refatoração com variáveis) aplicado ao **seu projeto autoral**: o bloco `:root` completo do seu sistema de design, com no mínimo dez variáveis, e a folha de estilo reorganizada nas sete seções.

**Parte 3 — Discussão (10 min).** Em texto próprio (ou no fórum da turma, se você cursa a disciplina): traga um conflito de estilo real que você enfrentou (no site do evento ou no seu projeto), o cálculo de especificidade dos seletores envolvidos e como resolveu **sem** `!important`. Se puder, compare a solução com a de um colega.

**Critério de pronto:** o `css/estilo.css` do seu projeto abre com o comentário das sete seções, tem um `:root` com dez ou mais variáveis, nenhum valor de cor escrito solto fora do `:root`, nenhum `!important` e nenhum `id` usado como seletor de estilo.

**Guarde no seu repositório:** commit + push (ou a pasta do projeto, se ainda não usa Git).

## ✅ Checkpoint do projeto

Ao fim desta aula, o seu projeto autoral deve ter:

- [ ] `css/estilo.css` organizado nas sete seções, com o comentário-cabeçalho listando-as.
- [ ] Bloco `:root` com no mínimo dez variáveis: cores, fonte, três espaçamentos, raio e sombra.
- [ ] Nenhum valor de cor escrito diretamente nas regras — tudo por `var(--…)`, salvo `#ffffff` e o preto de sombras.
- [ ] Tipografia base no `body` (fonte, `font-size: 1rem`, `line-height: 1.6`, cor) e escala de títulos em `rem`.
- [ ] `html { font-size: 100% }` — nunca um valor fixo em pixels.
- [ ] Parágrafos com largura de leitura limitada (`max-width: 65ch` ou equivalente).
- [ ] Regra `:focus-visible` global com `outline` visível, e nenhum `outline: none` sem substituto.
- [ ] Pelo menos um seletor de atributo em uso (por exemplo, `a[href^="http"]::after`).
- [ ] Pelo menos uma pseudoclasse estrutural em uso (`:nth-child(even)` na tabela, por exemplo).
- [ ] Um `.botao` com os quatro estados: repouso, `:hover`, `:focus-visible` e `:active`.
- [ ] Uma tabela com `border-collapse: collapse`, `caption` estilizado e linhas alternadas.
- [ ] Utilitário `.oculto-visualmente` disponível na seção 6.
- [ ] Arquivo `contraste.md` na raiz, com os pares de cor verificados no WebAIM.
- [ ] Nenhum `!important` e nenhum `id` usado como seletor de estilo.

## 🎓 Marco do projeto — Unidade 1

**Escopo.** Ao fim da Unidade 1, o seu projeto autoral precisa ser um site em HTML puro, **sem CSS**, sobre o tema que você definiu na Aula 01. O escopo são os itens **não-CSS** do Checkpoint da Aula 05: as cinco páginas, o seccionamento semântico, a hierarquia de títulos, os `<article>`, a página de contato e a validação no W3C. Os itens de CSS daquele Checkpoint — `css/estilo.css` ligado nas páginas, o bloco `:root`, a regra base de imagens e o `.botao` com `:hover`/`:focus-visible` — **não entram neste marco; eles fecham o Marco 2**, sobre este mesmo site. A página vai parecer crua, e isso é intencional: o que este marco mede é a **estrutura**. A estilização é o Marco 2, e a interatividade é o Marco 3 — mesmo site, três camadas.

**Requisitos.**

| # | Requisito | Onde foi estudado |
|---|---|---|
| 1 | Mínimo de 5 páginas interligadas por caminhos relativos, sem link quebrado | Aula 02 |
| 2 | Estrutura HTML5 válida em todas as páginas: `<!DOCTYPE>`, `lang="pt-BR"`, `charset`, `viewport`, `description` e `title` próprios | Aula 02 |
| 3 | Seccionamento semântico: `header`, `nav`, `main` (um por página), `section`, `article`, `aside`, `footer` | Aulas 02 e 05 |
| 4 | Hierarquia de títulos correta, com um único `<h1>` por página e sem pular níveis | Aula 02 |
| 5 | Elementos de texto aplicados com significado: `strong`, `em`, `blockquote` com `cite`, `time` e `q` (o `<abbr>` é opcional e conta como item extra) | Aula 02 |
| 6 | Os três tipos de lista em uso: `ul`, `ol` e `dl` | Aulas 02 e 04 |
| 7 | Menu de navegação como `<ul>` dentro de `<nav aria-label>`, com `aria-current="page"` na página atual | Aula 04 |
| 8 | Uma tabela de dados com `caption`, `thead`, `tbody`, `tfoot` e `th scope` | Aula 02 |
| 9 | Um formulário completo: mínimo de 10 campos de tipos diferentes, `<label>` associado a cada um, `fieldset`/`legend`, `<select>`, `<textarea>` e validação nativa | Aulas 03 e 04 |
| 10 | Imagens com `alt` adequado a cada situação, ao menos uma em `figure`/`figcaption`, com `width`/`height` e `loading="lazy"` abaixo da dobra | Aula 04 |
| 11 | Um vídeo ou áudio incorporado com `controls` e fallback; se vídeo, com `<track kind="captions">` | Aula 04 |
| 12 | Ao menos um link externo com `target="_blank"` e `rel="noopener noreferrer"` | Aula 02 |
| 13 | Zero erros no validador do W3C, em todas as páginas | Aula 02 |

**Checklist de qualidade.** O que separa um projeto pronto de um feito às pressas na última hora:

- Validação W3C sem erros em nenhuma das cinco páginas.
- Seccionamento semântico coerente e hierarquia de títulos sem saltos.
- Formulário completo e acessível: todo campo com rótulo associado, agrupamento em `fieldset`, validação nativa funcionando.
- Tabela, listas e elementos de texto usados pelo que significam, não só pela aparência.
- Mídias com `alt` que descreve o que a imagem comunica (não o nome do arquivo), legendas de vídeo funcionando, `width`/`height` e `loading="lazy"` presentes.
- Navegação funcional e idêntica entre todas as páginas, sem link quebrado.
- Arquivos e pastas em minúsculas, sem espaço nem acento; nomes que dizem o que cada arquivo é.
- Nenhum `<link rel="stylesheet">`, `<style>` ou atributo `style` — este marco é só estrutura.

**Como saber que está pronto.**

- Rode cada página no validador do W3C (upload de arquivo ou por URL, se já estiver publicada) e confira "Document checking completed. No errors or warnings to show."
- No Console do DevTools, `document.querySelectorAll("main").length` deve retornar `1` em cada página.
- Navegue pelo site inteiro só com <kbd>Tab</kbd> e <kbd>Enter</kbd>: todo link e todo campo do formulário precisa ser alcançável e visível em foco.
- Peça para alguém (colega, familiar, ou você mesmo depois de um dia) abrir as cinco páginas sem explicação prévia e apontar qual link parece quebrado ou qual página parece fora do lugar.
- Use IA para entender um erro do validador ou revisar uma dúvida de sintaxe — não para gerar o site inteiro no seu lugar. Se você não conseguir explicar uma linha do seu próprio HTML, ela ainda não é sua.

## 📚 Para aprofundar

- MDN — Seletores CSS (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Web/CSS/CSS_selectors> — a referência completa; leia a página de combinadores e a de pseudoclasses.
- MDN — Cascata, especificidade e herança: <https://developer.mozilla.org/pt-BR/docs/Learn_web_development/Core/Styling_basics/Handling_conflicts> — o artigo que explica as três etapas com exemplos interativos.
- MDN — Valores e unidades CSS: <https://developer.mozilla.org/pt-BR/docs/Learn_web_development/Core/Styling_basics/Values_and_units> — cores, números, unidades e funções.
- MDN — Propriedades personalizadas (variáveis CSS): <https://developer.mozilla.org/pt-BR/docs/Web/CSS/Using_CSS_custom_properties> — escopo, herança e valores de reserva.
- MDN — `font-family` e a pilha de fontes: <https://developer.mozilla.org/pt-BR/docs/Web/CSS/font-family> — as famílias genéricas e os nomes reservados.
- web.dev — Learn CSS: <https://web.dev/learn/css> — os módulos "Selectors", "The cascade", "Specificity", "Inheritance", "Color" e "Sizing units".
- WebAIM — Contrast Checker: <https://webaim.org/resources/contrastchecker/> — use em todo par de cores antes de considerar pronto.
- W3C — WCAG 2.1 em português, critérios 1.4.3 (contraste mínimo) e 1.4.1 (uso da cor): <https://www.w3.org/Translations/WCAG21-ptbr/> — a origem das exigências desta aula.
- Google Fonts: <https://fonts.google.com/> — escolha a fonte e copie os `<link>` já prontos, com os pesos que você realmente vai usar.
- CSS Specificity Calculator: <https://specificity.keegan.st/> — cole um seletor e veja o trio (A, B, C); ótimo para conferir o Laboratório A3.
- SILVA, Maurício Samy. *Criando sites com HTML: sites de alta qualidade com HTML e CSS*. Novatec, 2008 — a parte de CSS, capítulos de seletores e cascata.
- TERUEL, Evandro C. *HTML 5 — Guia Prático*. Saraiva, 2014 — capítulo de folhas de estilo (Minha Biblioteca).
- MILETTO, Evandro M.; BERTAGNOLLI, Silvia C. *Desenvolvimento de software II*. Bookman, 2014 — capítulo sobre camada de apresentação em aplicações web.

Na próxima aula o site deixa de ser uma pilha de blocos: você vai aprender posicionamento, **Flexbox** e **CSS Grid**, decidir qual dos dois cada problema pede e construir o esqueleto de layout definitivo do site do evento, com um menu de navegação fixo, acessível e com link de salto.
