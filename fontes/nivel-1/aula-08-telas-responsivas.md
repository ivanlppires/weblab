# Aula 08 — Criando telas responsivas

> **Nível 1 — Introdução ao Desenvolvimento Web** · Unidade 2: CSS: estilo, layout e responsividade
> WebLab · UNEMAT Sinop · Prof. Ivan Luiz Pedroso Pires
> **Carga:** 3 aulas de 50 min (presencial) + 1 h (assíncrona)

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Explicar o que a meta `viewport` faz e por que, sem ela, nenhuma técnica responsiva funciona.
- Escrever CSS **mobile first**: a regra base serve ao celular e as media queries de `min-width` só acrescentam o que muda em telas maiores.
- Definir breakpoints a partir do ponto em que o layout quebra, e não de uma lista de aparelhos.
- Construir grades fluidas que se adaptam sem nenhuma media query, com `auto-fit` e `minmax()`.
- Tornar imagens e tipografia fluidas com `object-fit`, `aspect-ratio`, `srcset` e `clamp()`.
- Implementar um menu hambúrguer acessível, com `<button>`, `aria-expanded` e `aria-controls`.
- Respeitar preferências do sistema do usuário: tema escuro, redução de movimento e impressão.

## 📋 Pré-requisitos

- [ ] Pasta `site-evento/` com as cinco páginas e o `css/estilo.css` como ficaram ao fim da Aula 07: cabeçalho fixo com menu horizontal, link de salto, grade de cartões com `auto-fit`, página de programação com áreas nomeadas e rodapé em três colunas.
- [ ] VS Code com a extensão Live Server e um navegador com DevTools (Chrome ou Firefox).
- [ ] Um celular conectado à mesma rede Wi-Fi do computador (opcional, mas vai valer a pena no bloco 3).
- [ ] Revisar da Aula 07: `repeat(auto-fit, minmax())`, `grid-template-areas` e a diferença entre `justify-content` e `align-items`.

> Na aula passada você estruturou o site da Semana Acadêmica de Sistemas de Informação com Grid e Flexbox e construiu o menu horizontal — mas só olhou o resultado no monitor do laboratório. Abra a mesma página no celular: o menu estoura para fora da tela, os cartões ficam estreitos demais e a lateral de filtros esmaga o conteúdo. Hoje você reescreve a folha de estilo de trás para a frente — primeiro o celular, depois as telas maiores — e cumpre a promessa da Aula 07: o menu hambúrguer.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Viewport, os três pilares do design responsivo, media queries, mobile first e breakpoints |
| 2 | 50 min | Grades fluidas sem media query, imagens responsivas (`object-fit`, `srcset`), tipografia com `clamp()` |
| 3 | 50 min | Menu hambúrguer acessível, preferências do usuário, testes no celular real e Mão na massa |

## 1. Por que "responsivo" — e o que a meta viewport tem a ver com isso

O mesmo `index.html` que você escreveu na Aula 02 vai ser aberto em um celular de 360 px de largura, em um tablet de 768 px, em um notebook de 1366 px e em um monitor de 2560 px. Não existe "a tela": existe um intervalo contínuo de larguras, e o site precisa funcionar em qualquer ponto dele.

Até o começo dos anos 2010 a solução era manter dois sites: `www.site.com` para o computador e `m.site.com` para o celular, com HTML duplicado e conteúdo sempre desatualizado em um dos dois. **Design responsivo** é a ideia de que um único HTML se adapta à largura disponível, e ele se apoia em três pilares:

1. A **meta viewport**, que diz ao celular para não fingir que é um monitor.
2. **Layouts fluidos**, feitos com larguras relativas (`%`, `fr`, `minmax()`, `max-width`) em vez de pixels fixos.
3. **Media queries**, para os ajustes pontuais que a fluidez sozinha não resolve.

Repare na ordem: as media queries vêm por último. Um layout bem feito com Grid e Flexbox, como o da Aula 07, já se adapta a boa parte das larguras sem nenhuma query. Elas entram para os pontos em que a fluidez não basta — e a Mão na massa de hoje vai mostrar que são bem poucos.

> **🧠 Você sabia?**
> O termo *Responsive Web Design* foi cunhado por Ethan Marcotte em um artigo de 2010 na revista *A List Apart*. Ele emprestou a ideia da arquitetura responsiva — prédios cujas paredes e iluminação reagem à presença das pessoas — e propôs que páginas fizessem o mesmo com a largura da janela. Antes disso, "site para celular" significava um segundo site.

### A meta viewport

Ela está no `<head>` de todas as suas páginas desde a Aula 02. Hoje você entende o que ela faz.

**`site-evento/index.html`** (dentro do `<head>`, igual nas cinco páginas)

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

| Parte | O que significa |
|---|---|
| `width=device-width` | A largura de layout da página passa a ser a largura real do aparelho em pixels CSS (360 px em um celular comum), e não os 980 px que ele finge ter por padrão. |
| `initial-scale=1.0` | O zoom inicial é 1:1 — um pixel CSS corresponde a um pixel "lógico" do aparelho. Sem isso, alguns navegadores abrem a página afastada. |

Sem essa linha, o celular renderiza a página como se a janela tivesse 980 px de largura e depois encolhe tudo para caber na tela. O resultado é aquele site minúsculo em que você precisa dar zoom para ler qualquer coisa — e nenhuma media query dispara, porque para o navegador a largura "é" 980 px.

> **⚠️ Atenção**
> Nunca acrescente `user-scalable=no` nem `maximum-scale=1` à meta viewport. Isso bloqueia o zoom, que é a única forma de muita gente conseguir ler o seu site. Os navegadores atuais ignoram essa proibição por questão de acessibilidade, e o Lighthouse penaliza a página que tenta usá-la.

> **🔎 Por baixo do capô**
> O navegador do celular trabalha com duas "janelas". A **viewport de layout** é a largura que o CSS enxerga — é nela que `width: 100%` e as media queries são calculadas. A **viewport visual** é o pedaço que aparece na tela depois do zoom. A meta viewport iguala as duas na abertura da página. E "pixel CSS" não é o mesmo que pixel físico: um celular com tela de 1080 px físicos e `devicePixelRatio` igual a 3 reporta 360 px CSS. É por isso que o seu layout de 360 px fica nítido: cada pixel CSS é desenhado com 3 × 3 pixels de verdade.
>
> Toda vez que a largura da viewport muda — você gira o celular, redimensiona a janela, abre o DevTools — o navegador recalcula a posição e o tamanho de **todas** as caixas da página. Esse recálculo se chama **reflow** (ou *layout*). Ele é caro, e vai voltar a aparecer na Aula 09 quando falarmos de animações que travam.

> **🔬 Investigue**
> Abra `site-evento/index.html` no Live Server e o console do DevTools (<kbd>F12</kbd>). Digite `window.innerWidth` e anote o valor. Ative o modo dispositivo (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>M</kbd>), escolha "Pixel 7" ou outro celular e repita: o valor cai para algo como 412, mesmo com `screen.width` informando outra coisa. Agora digite `window.devicePixelRatio`. Por fim, comente a linha da meta viewport no HTML, salve e observe `window.innerWidth` de novo no modo dispositivo: 980. Descomente antes de seguir.

### Os outros dois pilares

Os layouts fluidos são o assunto da seção 2; as media queries, da seção 3. Vale antecipar a regra de ouro que conecta os dois: **primeiro tente resolver com fluidez; só escreva uma media query quando o layout quebrar.**

## 2. Layouts fluidos: o que se adapta sozinho

### O contêiner que respira

Você já tem esta regra desde a Aula 07. Releia com outros olhos:

**`site-evento/css/estilo.css`** (seção 4 — layout)

```css
.container {
  width: 100%;
  max-width: var(--largura-max);
  margin-inline: auto;
  padding-inline: var(--espaco-medio);
}
```

Compare com a versão que muita gente escreve e que quebra no celular:

```css
/* ❌ Quebra em qualquer tela com menos de 1100 px */
.container {
  width: 1100px;
  margin: 0 auto;
}
```

A diferença é o par `width: 100%` + `max-width`. Em uma tela de 360 px o contêiner ocupa 360 px; em uma de 1920 px ele para em 1100 px e centraliza. Uma regra só, sem media query. O `padding-inline` garante que o texto não encoste na borda do celular.

> **⚠️ Atenção**
> `width` fixa em pixels é a causa número um de rolagem horizontal no celular. Se você precisa de um limite, o limite é `max-width`. Se precisa de um mínimo, é `min-width` — e mesmo assim pense duas vezes.

### Mídia nunca estoura

**`site-evento/css/estilo.css`** (seção 3 — base)

```css
img,
video {
  max-width: 100%;
  height: auto;
}
```

Uma foto de 1600 px de largura, sem essa regra, empurra o contêiner de 360 px para 1600 px e cria uma barra de rolagem horizontal na página inteira. Com `max-width: 100%` ela encolhe até caber; o `height: auto` mantém a proporção mesmo quando o HTML declara `width` e `height` no `<img>` — e você vai declarar, como mostra a seção 4.

### Unidades que se adaptam

| Unidade | Relativa a | Use para |
|---|---|---|
| `%` | largura do elemento pai | larguras de colunas e de contêineres |
| `fr` | espaço livre da grade | colunas e linhas do Grid |
| `vw` / `vh` | 1 % da largura / altura da viewport | seções de altura de tela, tipografia fluida |
| `rem` | tamanho da fonte da raiz | espaçamentos, fontes, breakpoints |
| `ch` | largura do caractere "0" | largura máxima de texto corrido (`max-width: 65ch`) |

> **💡 Dica**
> `min-height: 100vh` em um celular pode ficar mais alto do que a tela visível, porque a barra de endereço do navegador entra na conta. A unidade `dvh` (*dynamic viewport height*) resolve: `min-height: 100dvh` acompanha a barra aparecendo e sumindo. Funciona em todos os navegadores atuais.

### A grade que dispensa media query

Na Aula 07 você escreveu esta linha para os cartões de programação e de palestrantes:

**`site-evento/css/estilo.css`** (seção 4 — layout)

```css
.cartoes {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--espaco-medio);
}
```

Hoje vale fazer a conta do que ela faz em cada largura. O contêiner tem `padding-inline` de 16 px de cada lado; a largura útil é a largura da tela menos 32 px.

| Largura da tela | Largura útil | Colunas de no mínimo 280 px que cabem |
|---|---|---|
| 360 px | 328 px | 1 (com 328 px) |
| 768 px | 736 px | 2 (com 360 px cada, descontado o `gap`) |
| 1024 px | 992 px | 3 (com 320 px cada) |
| 1440 px | 1100 px (limite do `.container`) | 3 (com 356 px cada) |

O navegador cria quantas colunas de 280 px couberem, distribui o que sobrar entre elas e reorganiza tudo a cada mudança de largura. Nenhuma media query, nenhum breakpoint escolhido por você — o breakpoint nasce do conteúdo, que é exatamente onde ele deve nascer.

> **📌 Na prova**
> `auto-fit` e `auto-fill` fazem a mesma conta de quantas colunas cabem. A diferença aparece quando há **menos itens do que colunas**: `auto-fill` mantém as colunas vazias (os itens ficam estreitos, com espaço sobrando à direita); `auto-fit` colapsa as vazias e deixa os itens existentes crescerem. Para grades de cartões, você quase sempre quer `auto-fit`.

> **⚠️ Atenção**
> `minmax(280px, 1fr)` tem um ponto cego: em um contêiner com menos de 280 px de largura (um celular pequeno com `padding` generoso, ou a lateral estreita da programação), a coluna mínima é maior que o espaço e a grade estoura. A correção é `minmax(min(280px, 100%), 1fr)`: o mínimo passa a ser "280 px ou a largura toda, o que for menor". Você vai aplicar isso na Mão na massa.

## 3. Media queries e mobile first

### Anatomia de uma media query

**`site-evento/css/estilo.css`** (seção 7 — media queries)

```css
@media (min-width: 768px) {
  .grade {
    grid-template-columns: repeat(2, 1fr);
  }
}
```

Leia como uma pergunta: "a viewport tem pelo menos 768 px de largura?". Se a resposta for sim, as regras dentro das chaves valem; se for não, é como se não existissem. Dentro do bloco você escreve CSS comum — seletores, propriedades, valores — nada muda.

> **🔎 Por baixo do capô**
> Uma media query **não** aumenta a especificidade de nada. `.grade` dentro de `@media` tem exatamente o mesmo peso de `.grade` fora. O que decide quem vence, quando a query está ativa, é a regra da cascata que você aprendeu na Aula 06: entre seletores de mesmo peso, **a última declarada ganha**. Por isso as media queries ficam depois das regras base no arquivo — se você escrever a query antes, a regra base a sobrescreve e parece que "a media query não funciona". O navegador reavalia todas as queries a cada mudança de largura, e cada mudança de resultado dispara um reflow.

### Mobile first na prática

Mobile first é uma ordem de escrita: o CSS sem nenhuma media query é o CSS do celular; cada media query de `min-width` acrescenta o que muda quando a tela cresce.

**`site-evento/css/estilo.css`** (exemplo completo)

```css
/* Base — celular: uma coluna, sem query nenhuma */
.grade {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

/* Tablet — a partir de 768px: duas colunas */
@media (min-width: 768px) {
  .grade {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Notebook — a partir de 1024px: três colunas */
@media (min-width: 1024px) {
  .grade {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* Monitor grande — a partir de 1440px: quatro colunas */
@media (min-width: 1440px) {
  .grade {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

Em um monitor de 1600 px as **quatro** queries estão ativas ao mesmo tempo. As três primeiras definem `grid-template-columns`, e a última vence porque é a última. É o efeito cascata a seu favor: cada query só precisa declarar o que muda naquele tamanho.

### Por que mobile first

1. **É onde está o público.** Mais da metade dos acessos a sites no Brasil vem de celulares. Um site que começa pelo monitor e "adapta" para o celular está otimizando para a minoria.
2. **Obriga a priorizar.** Em 360 px não cabe tudo. Escrever primeiro para a tela pequena força a decidir o que é essencial — e o que é essencial no celular continua essencial no monitor.
3. **Gera CSS aditivo.** Queries de `min-width` acrescentam; queries de `max-width` precisam **desfazer** regras já aplicadas. Compare o exemplo acima com a versão *desktop first* a seguir.
4. **O celular baixa menos CSS aplicável.** O aparelho mais fraco, na rede mais lenta, processa só a base. As queries de telas grandes ficam ali, mas não alteram nada.

**Desktop first — a mesma grade, escrita ao contrário**

```css
/* Base — monitor grande: quatro colunas */
.grade {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

/* Até 1439px: desfaz para três */
@media (max-width: 1439px) {
  .grade {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* Até 1023px: desfaz para duas */
@media (max-width: 1023px) {
  .grade {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Até 767px: desfaz para uma */
@media (max-width: 767px) {
  .grade {
    grid-template-columns: 1fr;
  }
}
```

Funciona, mas repare nos limites "menos um" (`1439px`, `1023px`, `767px`) — um convite a erro de conta — e na lógica invertida: a base é a tela que menos gente usa, e o celular é o último caso tratado. Nesta disciplina você escreve **sempre** mobile first.

> **📌 Na prova**
> Uma pergunta clássica: "no CSS mobile first, o que acontece se o navegador não suportar media queries?". Resposta: ele mostra a versão de celular, que é a base e funciona em qualquer largura. No desktop first, o mesmo navegador mostraria as quatro colunas espremidas em 360 px.

### Breakpoints: onde o layout quebra

Um **breakpoint** é a largura em que uma media query entra em ação. A pergunta que todo iniciante faz é "quais são os breakpoints certos?", e a resposta honesta é: **os que o seu layout pedir**.

A tabela abaixo dá as faixas típicas, para você ter uma referência de vocabulário:

| Faixa | Dispositivo típico |
|---|---|
| até 480 px | Celular pequeno |
| 481–767 px | Celular grande |
| 768–1023 px | Tablet |
| 1024–1439 px | Notebook / desktop |
| 1440 px ou mais | Monitor grande |

> **💡 Dica**
> Não decore breakpoints de aparelhos. O método é: abra o site em uma janela larga, arraste a borda **devagar** e observe. No instante em que algo quebra — um título vira três linhas feias, os cartões ficam com 200 px, o menu estoura —, olhe o número que o DevTools mostra no canto superior direito. Esse é o seu breakpoint. O design manda no breakpoint, não o iPhone.

Para o site do evento, três pontos bastam e são os que você vai usar hoje: **768 px** (o menu cabe em linha e a grade aguenta duas colunas), **1024 px** (a lateral de filtros cabe ao lado do conteúdo) e, opcionalmente, **1440 px** (mais respiro entre as seções).

### Outras condições úteis

Media queries não são só sobre largura. Estas são as que você vai usar com frequência:

```css
/* Só até 767px (raro em mobile first, mas útil para esconder algo só no celular) */
@media (max-width: 767px) {
  .so-desktop {
    display: none;
  }
}

/* Faixa fechada: só entre 768px e 1023px */
@media (min-width: 768px) and (max-width: 1023px) {
  .lateral {
    display: none;
  }
}

/* Orientação: celular deitado */
@media (orientation: landscape) {
  .hero {
    padding-block: 2rem;
  }
}

/* Impressão: tira o que não faz sentido no papel */
@media print {
  nav,
  footer,
  .sem-impressao {
    display: none;
  }
}

/* Tema escuro escolhido no sistema operacional */
@media (prefers-color-scheme: dark) {
  :root {
    --cor-fundo: #0f1720;
    --cor-texto: #e6edf3;
  }
}

/* Usuário pediu menos movimento */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation: none !important;
    transition: none !important;
  }
}
```

As três últimas — impressão, tema escuro e redução de movimento — são **preferências do usuário**, e a seção 6 volta a elas com calma.

> **💡 Dica**
> Existe uma sintaxe mais nova, de intervalo: `@media (width >= 768px)` e `@media (768px <= width < 1024px)`. Ela já funciona em todos os navegadores atuais e evita os limites "menos um". Nesta disciplina usamos `min-width` porque é a forma que você vai encontrar em 99 % do código existente — mas reconheça as duas.

### Onde as media queries ficam no arquivo

Na Aula 06 você reservou a seção 7 de `estilo.css` para elas. Duas escolas convivem no mercado: agrupar todas as queries no fim do arquivo, em ordem crescente de largura, ou manter cada query logo abaixo do componente que ela ajusta. As duas funcionam; o que não pode é misturar. Nesta disciplina, para facilitar a leitura e a correção, **as queries ficam agrupadas no fim, em ordem crescente**: primeiro o bloco de `768px`, depois o de `1024px`, depois o de `1440px`.

## 4. Imagens e tipografia responsivas

### `object-fit` e `aspect-ratio`: fotos que não deformam

Os cartões de palestrantes recebem fotos de tamanhos diferentes: uma em 800 × 600, outra em 1200 × 1200, outra em 640 × 960. Com `width: 100%` cada uma fica com uma altura, e a grade vira um zigue-zague.

**`site-evento/css/estilo.css`** (seção 5 — componentes)

```css
.cartao img {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
  object-position: center;
  border-radius: var(--raio-borda) var(--raio-borda) 0 0;
}
```

- `aspect-ratio: 16 / 9` reserva a mesma proporção para todas as imagens, qualquer que seja a largura do cartão.
- `object-fit: cover` faz a foto **preencher** a caixa cortando o que sobra, em vez de esticar (`fill`, o padrão) ou deixar faixas vazias (`contain`).
- `object-position` escolhe que parte da foto sobrevive ao corte — `center` para paisagens, `top` para retratos, onde o rosto fica na parte de cima.

### `srcset` e `<picture>`: a imagem certa para cada tela

Servir uma foto de 1600 px para um celular de 360 px desperdiça dados e tempo de carregamento. O atributo `srcset` oferece várias versões e deixa o navegador escolher.

**`site-evento/index.html`** (banner da página inicial)

```html
<img
  src="img/banner-800.jpg"
  srcset="img/banner-400.jpg 400w,
          img/banner-800.jpg 800w,
          img/banner-1600.jpg 1600w"
  sizes="(min-width: 1024px) 1100px, 100vw"
  width="1600"
  height="900"
  alt="Auditório lotado na abertura da Semana Acadêmica de Sistemas de Informação">
```

- `srcset` lista os arquivos e a largura real de cada um (`480w` = 480 px de largura).
- `sizes` diz quanto da tela a imagem vai ocupar: 1100 px em telas a partir de 1024 px, a tela inteira (`100vw`) abaixo disso. Com essa informação e o `devicePixelRatio`, o navegador baixa **só** o arquivo adequado.
- `width` e `height` no HTML informam a proporção antes de a imagem carregar. O navegador reserva o espaço e a página não "pula" quando a foto chega — o Lighthouse mede isso como *Cumulative Layout Shift*, e vai cobrar na seção 7.

Quando a versão de celular precisa ser **outra foto** (um recorte mais fechado, por exemplo), use `<picture>`:

```html
<picture>
  <source media="(min-width: 768px)" srcset="img/banner-largo.jpg">
  <img src="img/banner-quadrado.jpg" width="800" height="800"
       alt="Auditório lotado na abertura da Semana Acadêmica de Sistemas de Informação">
</picture>
```

O `<source>` com `media` funciona como uma media query dentro do HTML; o `<img>` no fim é obrigatório e serve de reserva.

### Tipografia fluida com `clamp()`

Um `<h1>` de 3 rem fica ótimo no monitor e ocupa três linhas no celular. Antes de `clamp()`, a solução era uma media query por tamanho de fonte. Hoje é uma linha:

**`site-evento/css/estilo.css`** (seção 3 — base)

```css
h1 {
  font-size: clamp(1.75rem, 1.2rem + 2.5vw, 3rem);
}

h2 {
  font-size: clamp(1.375rem, 1.1rem + 1.25vw, 2rem);
}

body {
  font-size: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
  line-height: 1.6;
}

p,
li {
  max-width: 65ch;
}
```

`clamp(mínimo, preferido, máximo)` devolve o valor preferido, mas nunca abaixo do mínimo nem acima do máximo. No `<h1>`:

- em 360 px, `1.2rem + 2.5vw` dá 1.2 × 16 + 9 = 28,2 px — abaixo do mínimo de 28 px? Não: 28,2 px é ligeiramente acima, então esse é o valor usado;
- em 1024 px, dá 19,2 + 25,6 = 44,8 px, entre os limites;
- em 1920 px, daria 67,2 px, mas o máximo de 3 rem (48 px) segura.

> **⚠️ Atenção**
> O termo preferido mistura `rem` com `vw` de propósito. Se fosse só `2.5vw`, a fonte deixaria de responder ao zoom do navegador (<kbd>Ctrl</kbd>+<kbd>+</kbd>), porque `vw` depende da largura da janela e não do tamanho da fonte — e isso viola o critério 1.4.4 da WCAG, que exige que o texto possa crescer até 200 %. O `rem` no cálculo devolve o controle ao usuário.

> **💡 Dica**
> No celular, nunca deixe texto corrido nem campos de formulário abaixo de 16 px. Além de ficar difícil de ler, o Safari do iPhone dá zoom automático em qualquer `<input>` com fonte menor que 16 px quando ele recebe foco, e o layout inteiro "salta".

## 5. O menu hambúrguer — acessível de verdade

Na Aula 07 o menu era uma lista horizontal com cinco links, e em 360 px ela não cabe. A solução clássica é esconder a lista atrás de um botão com três barrinhas — o "hambúrguer" — que só aparece em telas pequenas.

### Por que `<button>`, e não `<div>` ou `<a>`

Você vai ver por aí menus abertos por `<div class="hamburguer">` ou por `<a href="#">`. Os dois estão errados, e a razão é acessibilidade:

- Um `<div>` não recebe foco por <kbd>Tab</kbd>, não reage a <kbd>Enter</kbd> nem a <kbd>Espaço</kbd> e é anunciado pelo leitor de tela como "texto", não como algo clicável.
- Um `<a href="#">` é focável, mas semanticamente é um **link**: o leitor de tela anuncia "link", o usuário espera navegar para outro lugar, e o `#` faz a página rolar para o topo.
- Um `<button>` é focável, reage às duas teclas, é anunciado como "botão" e aceita dois atributos que contam o resto da história: `aria-expanded` (está aberto ou fechado?) e `aria-controls` (controla qual elemento?).

### A marcação

Este é o bloco final do cabeçalho. Ele substitui o `<nav>` da Aula 07 nas cinco páginas:

**`site-evento/index.html`** (dentro de `.cabecalho__interno`, depois do logo)

```html
<nav aria-label="Principal">
  <button class="menu-botao" aria-expanded="false" aria-controls="menu-principal">
    <span class="menu-botao__icone" aria-hidden="true"></span>
    Menu
  </button>
  <ul id="menu-principal" class="menu">
    <li><a href="index.html" aria-current="page">Início</a></li>
    <li><a href="programacao.html">Programação</a></li>
    <li><a href="palestrantes.html">Palestrantes</a></li>
    <li><a href="contato.html">Contato</a></li>
    <li><a href="inscricao.html" class="menu__cta">Inscreva-se</a></li>
  </ul>
</nav>
```

Três detalhes:

1. O `<span>` do ícone tem `aria-hidden="true"` porque é decorativo — o leitor de tela lê a palavra "Menu", que está ali como texto de verdade.
2. `aria-controls="menu-principal"` aponta para o `id` da lista. Alguns leitores de tela oferecem um atalho para "pular para o elemento controlado".
3. `aria-expanded="false"` é o **estado**. É esse atributo que o CSS vai observar para mostrar ou esconder a lista — e é o único que o JavaScript vai trocar.

### O CSS: base para o celular, a query acrescenta o desktop

**`site-evento/css/estilo.css`** (seção 5 — componentes; substitui o `.menu` da Aula 07)

```css
/* Cabeçalho: logo à esquerda, botão à direita (celular) */
.cabecalho__interno {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--espaco-medio);
  padding-block: var(--espaco-medio);
}

/* Botão hambúrguer */
.menu-botao {
  display: inline-flex;
  align-items: center;
  gap: var(--espaco-pequeno);
  padding: var(--espaco-pequeno) var(--espaco-medio);
  background: transparent;
  border: 1px solid var(--cor-borda);
  border-radius: var(--raio-borda);
  color: var(--cor-texto);
  font: inherit;
  cursor: pointer;
}

.menu-botao:focus-visible {
  outline: 3px solid var(--cor-secundaria);
  outline-offset: 2px;
}

/* As três barrinhas: uma no span, duas nos pseudoelementos */
.menu-botao__icone {
  position: relative;
  display: block;
  width: 20px;
  height: 2px;
  background: currentColor;
}

.menu-botao__icone::before,
.menu-botao__icone::after {
  content: "";
  position: absolute;
  left: 0;
  width: 100%;
  height: 2px;
  background: currentColor;
}

.menu-botao__icone::before {
  top: -6px;
}

.menu-botao__icone::after {
  top: 6px;
}

/* Lista: fechada por padrão, cai abaixo do cabeçalho quando aberta */
.menu {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  flex-direction: column;
  gap: 0;
  margin: 0;
  padding: var(--espaco-pequeno) var(--espaco-medio);
  list-style: none;
  background: var(--cor-superficie);
  border-bottom: 1px solid var(--cor-borda);
  box-shadow: var(--sombra-cartao);
}

/* O atributo que o JavaScript troca é o que abre a lista */
.menu-botao[aria-expanded="true"] + .menu {
  display: flex;
}

.menu a {
  display: block;
  padding: var(--espaco-medio) 0;
  border-bottom: 1px solid var(--cor-borda);
}

.menu li:last-child a {
  border-bottom: 0;
}
```

E, na seção 7, a query que transforma o mesmo HTML no menu horizontal da Aula 07:

**`site-evento/css/estilo.css`** (seção 7 — media queries)

```css
@media (min-width: 768px) {
  .menu-botao {
    display: none;
  }

  .menu {
    display: flex;
    position: static;
    flex-direction: row;
    align-items: center;
    gap: var(--espaco-grande);
    padding: 0;
    background: transparent;
    border-bottom: 0;
    box-shadow: none;
  }

  .menu a {
    padding: var(--espaco-pequeno) 0;
    border-bottom: 0;
  }
}
```

Alguns pontos para entender, não só copiar:

- A lista aberta usa `position: absolute` com `top: 100%`. O ancestral posicionado mais próximo é o `.cabecalho`, que é `sticky` — e `sticky` conta como posicionado, como você viu na Aula 07. A lista cai exatamente abaixo do cabeçalho, por cima do conteúdo.
- O seletor `.menu-botao[aria-expanded="true"] + .menu` combina um seletor de atributo com o combinador de irmão adjacente (`+`), ambos da Aula 06. Ele só casa quando o botão está com `aria-expanded="true"` **e** a lista vem logo depois dele — que é o caso do HTML acima.
- A query de 768 px desfaz mais coisas do que o normal (`position`, `background`, `box-shadow`). É a exceção que confirma a regra do mobile first: o menu de celular e o de desktop são componentes genuinamente diferentes, então não há como um ser só "a base mais um pouco" do outro.
- O sublinhado animado de `.menu a::after` da Aula 07 continua valendo nas duas versões.

> **⚠️ Atenção**
> `display: none` remove a lista da árvore de acessibilidade — o leitor de tela não a encontra. Aqui isso é **correto**: o menu está fechado e o usuário não deveria alcançar links invisíveis com <kbd>Tab</kbd>. Na Aula 09 você vai animar a abertura, e vai aprender que `display` não anima; a técnica passa a ser `opacity` + `visibility` + `transform`, que preserva o mesmo comportamento acessível.

### Oito linhas de JavaScript — antecipação da Unidade 3

O CSS já sabe abrir e fechar. Falta alguém trocar o atributo quando o botão for clicado. Isso é JavaScript, assunto da Unidade 3 — mas são poucas linhas, e vale entendê-las agora:

**`site-evento/js/menu.js`**

```js
// Seleciona o botão e a lista pelo seletor CSS
const botao = document.querySelector('.menu-botao');
const menu = document.querySelector('#menu-principal');

// A cada clique, inverte o valor de aria-expanded
botao.addEventListener('click', () => {
  const aberto = botao.getAttribute('aria-expanded') === 'true';
  botao.setAttribute('aria-expanded', String(!aberto));
});
```

E a chamada, no `<head>` das cinco páginas:

**`site-evento/index.html`**

```html
<script src="js/menu.js" defer></script>
```

O atributo `defer` faz o navegador baixar o script em paralelo e só executá-lo depois de terminar de ler o HTML — sem ele, `document.querySelector('.menu-botao')` rodaria antes de o botão existir e devolveria `null`.

O que importa aqui é a **divisão de trabalho**: o JavaScript só troca um atributo; o CSS decide o que aparece. Nada de `menu.style.display = 'flex'` — quem manda na apresentação é a folha de estilo, e o dia em que você quiser animar a abertura vai mexer só nela.

> **🔎 Por baixo do capô**
> Com o menu fechado, o leitor de tela anuncia algo como "Menu, botão, recolhido". Depois do clique, "Menu, botão, expandido" — e a pessoa sabe que apareceu algo, mesmo sem enxergar a tela. É o `aria-expanded` que produz essa frase. Um `<div>` com uma classe `.aberto` não produz nada.

> **💡 Dica**
> O menu ainda não fecha com <kbd>Esc</kbd>, nem com um toque fora dele, nem devolve o foco ao botão. Essas três coisas são o exercício **B3** de hoje — com dicas — e vão ficar naturais na Unidade 3. Faça o básico funcionar primeiro.

## 6. Preferências do usuário

O sistema operacional guarda escolhas que a pessoa fez uma vez e espera ver respeitadas em todo lugar: tema escuro, menos animações, tamanho de fonte. O CSS lê essas escolhas por media queries — sem JavaScript e sem botão no seu site.

### Tema escuro: `prefers-color-scheme`

Como todas as cores do site vivem em variáveis desde a Aula 06, um tema escuro é **redefinir as variáveis** dentro de uma media query. Nenhum seletor de componente precisa mudar.

**`site-evento/css/estilo.css`** (seção 2 — variáveis; acrescente a variável nova e o bloco)

```css
:root {
  --cor-primaria: #0b3d5c;
  --cor-secundaria: #1a7fb5;
  --cor-sobre-primaria: #ffffff;
  --cor-texto: #333333;
  --cor-fundo: #f7f9fb;
  --cor-superficie: #ffffff;
  --cor-borda: #dfe6ec;
  --fonte-base: "Inter", Arial, sans-serif;
  --espaco-pequeno: 8px;
  --espaco-medio: 16px;
  --espaco-grande: 32px;
  --raio-borda: 8px;
  --sombra-cartao: 0 2px 8px rgba(0, 0, 0, 0.1);
  --largura-max: 1100px;
  color-scheme: light dark;
}

@media (prefers-color-scheme: dark) {
  :root {
    --cor-primaria: #7ec8e3;
    --cor-secundaria: #a9dcef;
    --cor-sobre-primaria: #0f1720;
    --cor-texto: #e6edf3;
    --cor-fundo: #0f1720;
    --cor-superficie: #172231;
    --cor-borda: #2a3948;
    --sombra-cartao: 0 2px 8px rgba(0, 0, 0, 0.5);
  }
}
```

- `color-scheme: light dark` avisa o navegador que a página suporta os dois temas. Ele passa a desenhar barras de rolagem, campos de formulário e a cor de fundo padrão de acordo com o tema — de graça.
- A variável nova, `--cor-sobre-primaria`, existe porque no tema claro a primária é escura e o texto sobre ela é branco; no escuro a primária vira azul-claro e o texto sobre ela precisa ser escuro. Toda cor que "fica em cima" de outra cor precisa de variável própria. Na Mão na massa você troca o `color: #fff` do `.menu__cta` da Aula 07 por `var(--cor-sobre-primaria)`.

> **⚠️ Atenção**
> Tema escuro não é "inverter as cores". Verifique o contraste de novo no WebAIM para cada par texto/fundo do tema escuro — o mínimo continua sendo 4.5:1. Fundos escuros costumam pedir texto um pouco menos branco (`#e6edf3` em vez de `#ffffff`) para não "vibrar", e sombras mais fortes para continuarem visíveis.

### Redução de movimento: `prefers-reduced-motion`

Pessoas com distúrbios vestibulares configuram o sistema para reduzir animações, e o site precisa obedecer. O bloco abaixo desliga transições e animações quando essa preferência está ativa. Ele vai para o **fim** da folha de estilo, porque precisa vencer tudo:

**`site-evento/css/estilo.css`** (última regra do arquivo)

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

Hoje o único movimento do site é o sublinhado do menu; a Aula 09 acrescenta transições, transformações e animações, e volta a este bloco com calma — inclusive para explicar por que é uma das poucas situações em que `!important` se justifica.

### Impressão: `@media print`

A página de programação vai ser impressa por gente que quer levar a grade de horários no bolso. No papel, cabeçalho fixo, menu, rodapé e link de salto não fazem sentido:

**`site-evento/css/estilo.css`** (seção 7 — media queries)

```css
@media print {
  .cabecalho,
  .rodape,
  .salto,
  .menu-botao {
    display: none;
  }

  body {
    background: #fff;
    color: #000;
    font-size: 12pt;
  }

  .pagina {
    display: block;
  }

  a[href^="http"]::after {
    content: " (" attr(href) ")";
    font-size: 0.85em;
  }
}
```

A última regra imprime a URL ao lado de cada link externo — no papel ninguém clica. O `attr(href)` lê o atributo do próprio elemento, uma função que você já viu na Aula 06 com `::after`.

> **🔬 Investigue**
> No DevTools, abra o menu de três pontos → *More tools* → *Rendering*. Role até *Emulate CSS media feature prefers-color-scheme* e alterne entre `light` e `dark`: o site troca de tema sem você tocar no sistema operacional. Logo abaixo, *Emulate CSS media feature prefers-reduced-motion* e, mais acima, *Emulate CSS media type* → `print` mostra a página como ela sairia na impressora. Deixe esse painel aberto durante a Mão na massa.

## 7. Testando de verdade

Um site "responsivo" que só foi testado arrastando a janela do Chrome não foi testado. Três ferramentas, em ordem crescente de confiança:

### 1. Modo dispositivo do DevTools

<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>M</kbd> (ou o ícone de celular no canto do DevTools). Escolha um aparelho na lista ou digite a largura à mão. Use o modo *Responsive* e arraste a borda devagar para achar os breakpoints. Ative *Throttling* → *Slow 4G* para sentir o carregamento em rede ruim. É rápido e ótimo para layout — mas simula: o toque vira clique de mouse, a barra de endereço não existe e as fontes do sistema são as do seu computador.

### 2. Celular real, na mesma rede

O Live Server serve a pasta do projeto na porta 5500. Do celular, na mesma rede Wi-Fi, acesse o endereço IP do computador nessa porta:

1. Descubra o IP do computador: `ip addr` (Linux), `ipconfig` (Windows) ou `ifconfig` (macOS). Procure algo como `192.168.0.15`.
2. No navegador do celular, abra `http://192.168.0.15:5500/site-evento/` (troque pelo seu IP).
3. Se não abrir, o Live Server pode estar ouvindo só em `127.0.0.1`. Nas configurações do VS Code, defina `liveServer.settings.host` como `0.0.0.0`, reinicie o Live Server e tente de novo. Se ainda não abrir, o firewall do computador está bloqueando a porta 5500.

No aparelho de verdade aparecem os problemas que o simulador esconde: o menu que não abre porque o botão tem 24 px e o dedo tem 40, a fonte que fica pequena demais, o campo de formulário que dá zoom sozinho, a altura de `100vh` que fica escondida atrás da barra de endereço. É sobre isso o fórum da atividade assíncrona.

### 3. Lighthouse

No DevTools, aba *Lighthouse* → marque *Mobile* → *Analyze page load*. Ele simula um celular de entrada em rede lenta e devolve notas de 0 a 100 em Performance, Acessibilidade, Boas práticas e SEO, com a lista do que corrigir. Problemas que ele pega e que você já sabe resolver: meta viewport ausente, texto menor que 12 px, imagens sem `width`/`height`, contraste abaixo de 4.5:1, alvos de toque menores que 48 × 48 px, `user-scalable=no`.

> **💡 Dica**
> Rode o Lighthouse em uma janela anônima. Extensões do navegador (bloqueadores de anúncio, tradutores) injetam scripts na página e derrubam a nota sem culpa sua.

### Lista de verificação responsiva

Passe cada página do site por estes itens antes de considerar pronta:

- [ ] Nenhuma rolagem horizontal em 320 px, 360 px e 768 px.
- [ ] Todo texto legível sem zoom; nada abaixo de 16 px no corpo.
- [ ] Imagens não deformam nem estouram o contêiner.
- [ ] Menu abre e fecha com o dedo, com o mouse e com <kbd>Enter</kbd>/<kbd>Espaço</kbd> no teclado.
- [ ] Alvos de toque (links do menu, botões) com pelo menos 44 × 44 px.
- [ ] Layout continua fazendo sentido com o celular deitado.
- [ ] Tema escuro do sistema é respeitado e o contraste continua ≥ 4.5:1.
- [ ] Lighthouse Mobile sem alertas de viewport, fonte pequena ou alvos de toque.

## 💻 Mão na massa — Site do evento em qualquer tela

Você vai transformar o `site-evento/` da Aula 07 em um site mobile first completo. Trabalhe com o Live Server aberto, o DevTools no modo dispositivo em 360 px e uma segunda janela em 1440 px.

### Passo 1 — Inventário do que quebra

Antes de corrigir, meça. Abra `index.html` e `programacao.html` em 360 px e anote o que você vê. A lista deve parecer com esta:

| Sintoma em 360 px | Causa provável |
|---|---|
| Menu com cinco links estoura para a direita | `.menu` é uma linha flex sem quebra |
| Lateral de filtros ocupa 240 px e esmaga o conteúdo | `.pagina` tem duas colunas fixas |
| Título do banner em quatro linhas | `font-size` fixo em `rem` |
| Rodapé com três colunas de 100 px cada | `.rodape__grade` tem três colunas fixas |
| Foto de palestrante achatada | `<img>` sem `object-fit` |

Cada linha vira um passo abaixo.

### Passo 2 — Reorganizar `estilo.css` para mobile first

Percorra a seção 4 (layout) do seu `estilo.css` e separe o que é **base** do que é **só para telas grandes**. A regra é simples: se uma declaração só faz sentido com espaço sobrando (duas ou mais colunas, `gap` grande, `padding` generoso), ela vai para uma media query na seção 7. O restante fica como base.

Ao fim da reorganização, a seção 7 do arquivo tem esta estrutura, ainda quase vazia:

**`site-evento/css/estilo.css`** (seção 7 — media queries)

```css
/* 7. Media queries — mobile first, em ordem crescente de largura */

@media (min-width: 768px) {
  /* tablet: menu em linha, rodapé em duas colunas */
}

@media (min-width: 1024px) {
  /* notebook: lateral ao lado do conteúdo, rodapé em três colunas */
}

@media (min-width: 1440px) {
  /* monitor grande: mais respiro */
}

@media print {
  /* impressão */
}
```

Os comentários vão sendo substituídos por regras nos passos seguintes. O bloco `prefers-reduced-motion` entra no passo 9, **depois** de tudo isso.

### Passo 3 — Contêiner, mídia e cartões

Confirme que a seção 3 (base) tem a regra de mídia e que a seção 4 tem o contêiner fluido; se não tiver, acrescente:

**`site-evento/css/estilo.css`** (seções 3 e 4)

```css
/* 3. Base */
img,
video {
  max-width: 100%;
  height: auto;
}

/* 4. Layout */
.container {
  width: 100%;
  max-width: var(--largura-max);
  margin-inline: auto;
  padding-inline: var(--espaco-medio);
}

.cartoes {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(280px, 100%), 1fr));
  gap: var(--espaco-medio);
}
```

E, na seção 5 (componentes), a foto do cartão com proporção fixa. Antes de colar, **apague a regra `.cartao__foto` da Aula 07** (a que fixava `width: 120px`, `height: 120px`, `border-radius: 50%` e `object-fit: cover`): `.cartao img` tem especificidade 0-1-1 e venceria `.cartao__foto` (0-1-0) de qualquer jeito, e duas regras disputando a mesma foto é exatamente o tipo de lixo que faz uma folha de estilo parar de ser previsível. Você pode manter a classe `cartao__foto` no HTML ou removê-la; o que não pode é deixar a regra órfã no CSS.

**`site-evento/css/estilo.css`** (seção 5)

```css
.cartao img {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
  object-position: center;
  border-radius: var(--raio-borda) var(--raio-borda) 0 0;
}

/* A foto do palestrante: quadrada, redonda e com o rosto preservado */
.cartao--palestrante img {
  width: 120px;
  aspect-ratio: 1 / 1;
  border-radius: 50%;
  object-position: top;
  align-self: center;
}
```

Os cartões de `palestrantes.html` já têm a classe `cartao--palestrante` ao lado de `cartao` desde a Aula 07 — confira que ela está lá nos seis, porque é ela que devolve a foto redonda de 120 px que a regra genérica acabou de sobrescrever.

**Como verificar:** em 360 px a grade de programação mostra um cartão por linha; em 768 px, dois; em 1100 px ou mais, três. Nenhuma media query foi escrita para isso.

### Passo 4 — Página de programação: uma coluna, depois duas

A `.pagina` da Aula 07 tinha `grid-template-columns: 240px 1fr` como base. Inverta: a base é uma coluna, e a lateral só vai para o lado a partir de 1024 px.

**`site-evento/css/estilo.css`** (seção 4)

```css
.pagina {
  display: grid;
  grid-template-columns: 1fr;
  grid-template-areas:
    "lateral"
    "conteudo";
  gap: var(--espaco-grande);
  padding-block: var(--espaco-grande);
}

.lateral {
  grid-area: lateral;
}

.conteudo {
  grid-area: conteudo;
}
```

**`site-evento/css/estilo.css`** (seção 7 — dentro do bloco de 1024px)

```css
@media (min-width: 1024px) {
  .pagina {
    grid-template-columns: 240px 1fr;
    grid-template-areas: "lateral conteudo";
  }
}
```

No celular a lateral de filtros vem **antes** da lista — ela é curta e é útil filtrar antes de rolar. Se a lateral fosse longa (patrocinadores, links, avisos), bastaria trocar a ordem em `grid-template-areas` da base para `"conteudo" "lateral"` — sem tocar no HTML, que continua com `<aside>` antes de `<section>`.

**Como verificar:** em 360 px os filtros aparecem em cima e os cartões embaixo, ambos com a largura toda; a partir de 1024 px a lateral gruda à esquerda com 240 px.

### Passo 5 — Menu hambúrguer

Substitua o `<nav>` das **cinco** páginas pela marcação da seção 5, mantendo `aria-current="page"` no link da página correta em cada arquivo. Depois:

1. Na seção 5 de `estilo.css`, substitua o `.menu` da Aula 07 pelo CSS de celular da seção 5 desta aula (`.menu-botao`, `.menu-botao__icone`, `.menu` com `display: none`, o seletor `.menu-botao[aria-expanded="true"] + .menu`).
2. Na seção 7, dentro do bloco de 768 px, cole a query que esconde o botão e coloca o menu em linha.
3. Crie a pasta `js/` e o arquivo `js/menu.js` com as oito linhas da seção 5.
4. Inclua `<script src="js/menu.js" defer></script>` no `<head>` das cinco páginas, logo depois do `<link>` do CSS.
5. Troque, no `.menu__cta`, `color: #fff` por `color: var(--cor-sobre-primaria)` — a variável entra no passo 8.

**`site-evento/index.html`** (`<head>` completo, como fica)

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Semana Acadêmica de Sistemas de Informação da UNEMAT Sinop: palestras, minicursos e maratona de programação.">
  <meta name="author" content="Curso de Sistemas de Informação — UNEMAT Sinop">
  <title>Início — Semana Acadêmica de Sistemas de Informação</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap"
        rel="stylesheet">
  <link rel="stylesheet" href="css/estilo.css">
  <script src="js/menu.js" defer></script>
</head>
```

Os três `<link>` da fonte Inter e o `<meta name="author">` vêm das Aulas 02 e 06 — eles continuam aqui. Quem copiar este bloco por cima do `<head>` antigo sem eles perde a tipografia do projeto inteiro.

**Como verificar:** em 360 px aparece o botão "Menu"; um clique abre a lista abaixo do cabeçalho, outro fecha. No DevTools, aba *Elements*, observe o atributo `aria-expanded` mudando a cada clique. Com <kbd>Tab</kbd> o botão recebe o anel de foco e <kbd>Enter</kbd> abre o menu. A partir de 768 px o botão some e os cinco links ficam em linha, como na Aula 07.

### Passo 6 — Tipografia fluida

Na seção 3 (base), substitua os `font-size` fixos de `h1`, `h2` e `body` pelos `clamp()` da seção 4 desta aula, e limite a largura do texto corrido:

**`site-evento/css/estilo.css`** (seção 3)

```css
body {
  font-family: var(--fonte-base);
  font-size: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
  line-height: 1.6;
  color: var(--cor-texto);
  background-color: var(--cor-fundo);
}

h1 {
  font-size: clamp(1.75rem, 1.2rem + 2.5vw, 3rem);
  line-height: 1.15;
}

h2 {
  font-size: clamp(1.375rem, 1.1rem + 1.25vw, 2rem);
  line-height: 1.25;
}

p,
li,
dd {
  max-width: 65ch;
}
```

**Como verificar:** arraste a janela de 360 px a 1440 px e veja o título crescer de forma contínua, sem saltos. Dê zoom com <kbd>Ctrl</kbd>+<kbd>+</kbd> até 200 %: o texto cresce junto.

### Passo 7 — Banner da página inicial

Na `index.html`, a seção de abertura ganha uma classe e uma altura que acompanha a tela:

**`site-evento/index.html`** (primeiro bloco dentro de `<main>`)

```html
<section class="hero">
  <div class="container">
    <h1>Semana Acadêmica de Sistemas de Informação</h1>
    <p>Três dias de palestras, minicursos e maratona de programação na UNEMAT Sinop.</p>
    <a href="inscricao.html" class="botao">Inscreva-se</a>
  </div>
</section>
```

**`site-evento/css/estilo.css`** (seção 5) — **substitua o bloco `.hero` da Aula 07**

> **⚠️ Atenção**
> O herói muda de forma: sai o Grid de duas colunas com texto de um lado e `<img>` do outro (Aula 07, Passo 5) e entra um banner de largura total com a foto como imagem de fundo. Apague as três regras antigas — `.hero`, `.hero img` e `.hero__acoes` — antes de colar as de baixo, e apague também o `<div class="hero__texto">`, a `<img>` e o segundo botão da marcação. Se as duas versões coexistirem, o `display: grid` da antiga briga com o `text-align: center` da nova e o resultado não é nem um nem outro.

```css
.hero {
  background: var(--cor-primaria) url("../img/banner.jpg") center / cover no-repeat;
  color: var(--cor-sobre-primaria);
  padding-block: clamp(3rem, 10vw, 8rem);
  text-align: center;
}

.hero h1 {
  color: inherit;
}

.hero p {
  margin-inline: auto;
}
```

O `padding-block` com `clamp()` faz o banner ter 48 px de respiro no celular e até 128 px no monitor. O `center / cover` posiciona e recorta a foto de fundo do mesmo jeito que `object-fit: cover` faz em um `<img>`. Na Aula 09 esse banner ganha um gradiente por cima da foto para garantir o contraste do texto.

### Passo 8 — Tema escuro

Na seção 2 (variáveis), acrescente `--cor-sobre-primaria: #ffffff;` e `color-scheme: light dark;` ao `:root`, e logo abaixo o bloco `@media (prefers-color-scheme: dark)` da seção 6 desta aula, com os valores escuros de todas as variáveis de cor.

Depois, procure no arquivo inteiro por cores escritas "na mão" (`#fff`, `#333`, `white`) e troque cada uma pela variável correspondente. Duas que certamente existem desde a Aula 07: o `color: #fff` do `.menu__cta` (vira `var(--cor-sobre-primaria)`) e a cor de fundo do `.cabecalho` (deve ser `var(--cor-superficie)`).

**Como verificar:** com o painel *Rendering* do DevTools em `prefers-color-scheme: dark`, o site inteiro troca de tema; nenhum texto some, nenhum botão fica branco sobre branco. Confira o contraste de `--cor-texto` sobre `--cor-fundo` e de `--cor-sobre-primaria` sobre `--cor-primaria` no WebAIM.

### Passo 9 — Redução de movimento

Cole o bloco `@media (prefers-reduced-motion: reduce)` da seção 6 como **última regra** do arquivo, depois de todas as outras media queries.

**Como verificar:** no painel *Rendering*, ative `prefers-reduced-motion: reduce`. Passe o mouse sobre um link do menu: o sublinhado aparece de imediato, sem deslizar.

### Passo 10 — Rodapé: uma, duas, três colunas

**`site-evento/css/estilo.css`** (seção 4 — base)

```css
.rodape {
  background: var(--cor-primaria);
  color: var(--cor-sobre-primaria);
  padding-block: var(--espaco-grande);
}

.rodape__grade {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--espaco-grande);
}

.rodape a {
  color: inherit;
}
```

**`site-evento/css/estilo.css`** (seção 7 — blocos de 768px e 1024px)

```css
@media (min-width: 768px) {
  .rodape__grade {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .rodape__grade {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

**Como verificar:** as três colunas do rodapé (sobre, links, contato) empilham em 360 px, ficam duas em 768 px (a terceira desce) e três a partir de 1024 px.

### Passo 11 — Impressão da programação

Cole a query `@media print` da seção 6 no fim da seção 7 (antes do bloco de `prefers-reduced-motion`). Abra `programacao.html`, pressione <kbd>Ctrl</kbd>+<kbd>P</kbd> e olhe a pré-visualização: só a grade de horários, em preto sobre branco, com as URLs dos links externos entre parênteses.

### Como testar

Abra cada uma das cinco páginas em três larguras e confira:

| Largura | O que você deve ver |
|---|---|
| 360 px | Botão "Menu" no cabeçalho; uma coluna em tudo (cartões, filtros, rodapé); título do banner em no máximo duas linhas; sem rolagem horizontal |
| 768 px | Menu horizontal com cinco links; cartões em duas colunas; rodapé em duas colunas; filtros ainda acima do conteúdo |
| 1440 px | Layout completo: lateral à esquerda com 240 px, cartões em três colunas, rodapé em três colunas, contêiner parado em 1100 px |

Depois, os três testes da seção 7: modo dispositivo em "Pixel 7" e "iPad", o celular real pelo IP do computador, e o Lighthouse Mobile em `index.html` — a meta é nenhum alerta de viewport, fonte ou alvo de toque. Guarde a captura do relatório: ela entra no checkpoint.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Por que a meta `viewport` é indispensável para responsividade? Descreva, em duas frases, o que o celular faz com uma página que não a declara.

**A2.** Qual a diferença entre a abordagem *mobile first* e *desktop first* na escrita das media queries? Qual delas usa `min-width` e qual usa `max-width`, e por que a primeira gera CSS "aditivo"?

**A3.** Escreva uma media query que aplique regras apenas entre 768 px e 1023 px de largura.

**A4.** O que faz `img { max-width: 100%; height: auto; }` e por que é uma regra praticamente obrigatória? O que aconteceria com a proporção de uma imagem que tem `width="800" height="600"` no HTML se faltasse o `height: auto`?

**A5.** Escreva a meta viewport correta e explique cada um de seus dois valores.

**A6.** Por que os breakpoints devem ser definidos pelo conteúdo e não por modelos de aparelho? Descreva o método prático para encontrá-los.

**A7.** O que faz `clamp(1rem, 2.5vw, 1.5rem)` aplicado a `font-size`? Calcule o valor resultante em uma tela de 320 px, de 800 px e de 1200 px.

**A8.** Explique o que `prefers-color-scheme` permite fazer e escreva um exemplo que troque as cores de fundo e de texto de um site para o tema escuro.

**A9.** Por que um menu hambúrguer deve ser um `<button>` com `aria-expanded`, e não um `<div>` ou um `<a href="#">`? Liste três diferenças práticas.

**A10.** Dada a grade `grid-template-columns: repeat(auto-fit, minmax(300px, 1fr))` dentro de um contêiner de 1000 px com `gap: 20px`, quantas colunas o navegador cria e qual a largura de cada uma? E se houver só dois itens na grade — o que muda entre `auto-fit` e `auto-fill`?

**A11.** O CSS abaixo foi escrito mobile first, mas o estudante reclama que "a media query não funciona". Encontre o erro sem rodar o código:

```css
@media (min-width: 768px) {
  .cartoes {
    grid-template-columns: repeat(2, 1fr);
  }
}

.cartoes {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}
```

### Nível B — Aplicação

**B1.** Crie uma galeria de 12 imagens com CSS Grid usando `auto-fit` / `minmax`, `gap` de 16 px, imagens com `aspect-ratio: 4 / 3` e `object-fit: cover`, e efeito de `scale` no `:hover` com transição. Use fotos livres (Unsplash, Pexels) ou o serviço `https://picsum.photos/600/450?random=1` mudando o número final.

**Resultado esperado:** em 360 px uma coluna; em 768 px duas; em 1200 px três ou quatro, sem nenhuma media query. Todas as imagens têm a mesma proporção, nenhuma deforma, e passar o mouse amplia a foto dentro da moldura sem estourar o cartão.

<details><summary>Dica</summary>

Para o zoom não vazar da moldura, o elemento que envolve a imagem precisa de `overflow: hidden`. A transição vai no `img` (estado normal), não no `:hover`, senão a volta é abrupta — a Aula 09 explica por quê. Replique o efeito em `:focus-within` se cada imagem for um link.
</details>

**B2.** Pegue o site institucional que você criou no exercício C1 da Aula 02 (`exercicios/aula02/curso/`) e torne-o totalmente responsivo, com pelo menos 3 breakpoints. Documente em comentários no CSS por que escolheu cada breakpoint — qual elemento quebrou e em que largura.

**Resultado esperado:** nenhuma rolagem horizontal entre 320 px e 1920 px; menu, tabela, formulário e imagens legíveis e usáveis no celular; três blocos `@media (min-width)` em ordem crescente, cada um com um comentário de uma linha justificando a largura.

<details><summary>Dica</summary>

Comece pela meta viewport e pela regra de mídia; só então redimensione. A tabela é o elemento que mais resiste: se ela não couber, envolva-a em um `<div>` com `overflow-x: auto` como solução mínima — o B4 mostra a solução completa.
</details>

**B3.** Implemente um menu responsivo completo: horizontal acima de 768 px, hambúrguer abaixo. Requisitos: `<button>` com `aria-expanded` e `aria-controls`, abertura animada por `transform`, fechamento pelo <kbd>Esc</kbd> e pelo clique fora, foco preso dentro do menu enquanto aberto e devolvido ao botão ao fechar.

**Resultado esperado:** o menu abre e fecha pelo botão, por <kbd>Esc</kbd> e por um toque fora dele; com o menu aberto, <kbd>Tab</kbd> circula só entre o botão e os links do menu; ao fechar, o foco volta ao botão; a abertura desliza em vez de aparecer de repente.

<details><summary>Dica</summary>

Este é um exercício-ponte para a Unidade 3; faça uma exigência de cada vez, sobre o `menu.js` da aula. Fechar com <kbd>Esc</kbd>: `document.addEventListener('keydown', (evento) => { if (evento.key === 'Escape') fechar(); })`. Clique fora: um `click` no `document` que só fecha se `!nav.contains(evento.target)`. Foco preso: pegue todos os links do menu com `menu.querySelectorAll('a')`, e em um `keydown` de <kbd>Tab</kbd> no último link (ou <kbd>Shift</kbd>+<kbd>Tab</kbd> no primeiro) chame `evento.preventDefault()` e `.focus()` no outro extremo. Devolver o foco: `botao.focus()` dentro de `fechar()`. Para animar, troque `display: none` por `opacity: 0; visibility: hidden; transform: translateY(-8px)` e a Aula 09 explica o resto.
</details>

**B4.** Construa uma tabela responsiva: em telas largas, tabela normal; abaixo de 640 px, cada linha vira um cartão com os rótulos das colunas via `data-*` e `::before`. Mantenha a marcação semântica de tabela. Use a grade de horários da programação do evento (dia, horário, atividade, local).

**Resultado esperado:** acima de 640 px, uma `<table>` comum com `<thead>`; abaixo, cada `<tr>` aparece como um bloco com borda, e cada célula mostra "Horário: 19h00", "Local: Auditório", com o rótulo em negrito à esquerda do valor.

<details><summary>Dica</summary>

Cada `<td>` recebe `data-rotulo="Horário"` no HTML. Na media query de `max-width: 639px`: `thead { position: absolute; left: -9999px; }` (esconde sem tirar do leitor de tela), `tr { display: block; margin-bottom: 1rem; border: 1px solid var(--cor-borda); }`, `td { display: flex; gap: 1rem; }` e `td::before { content: attr(data-rotulo); font-weight: 600; min-width: 6rem; }`. Não use `display: none` no `<thead>` — o leitor de tela perderia os cabeçalhos.
</details>

**B5.** Torne o site do seu **projeto autoral** totalmente responsivo em três breakpoints e registre capturas de tela em 360 px, 768 px e 1440 px de cada página.

**Resultado esperado:** para cada uma das cinco páginas, três capturas nomeadas `pagina-360.png`, `pagina-768.png` e `pagina-1440.png` em uma pasta `capturas/`; nenhuma mostra rolagem horizontal; o menu está aberto em pelo menos uma captura de 360 px.

<details><summary>Dica</summary>

No modo dispositivo do DevTools, o menu de três pontos ao lado da largura tem *Capture full size screenshot*, que salva a página inteira de uma vez na largura escolhida. Faça primeiro o `index.html`, valide os três tamanhos, e só então replique o padrão nas outras páginas — o CSS é o mesmo.
</details>

### Nível C — Desafio em sala

**C1.** Construa `portal/index.html` + `portal/css/portal.css`, um portal de notícias acadêmicas responsivo, com:

- **Estrutura** (Grid, com áreas nomeadas): cabeçalho, barra lateral, conteúdo principal e rodapé.
- **Cabeçalho** (Flexbox): logo à esquerda, menu horizontal à direita, `position: sticky; top: 0` com sombra.
- **Conteúdo principal** (Grid): um destaque ocupando 2 colunas, seguido de 6 cartões em `repeat(auto-fit, minmax(280px, 1fr))`. Cada cartão: imagem com `object-fit: cover`, categoria, título, resumo, data e link.
- **Barra lateral** (Flexbox em coluna): caixa de busca, lista de mais lidos, lista de tags.
- **Rodapé** (Grid de 4 colunas): sobre, links úteis, contato, redes sociais.
- **Responsividade:** até 767 px, uma coluna, lateral **depois** do conteúdo, menu vira lista vertical; de 768 px a 1023 px, cartões em 2 colunas, lateral ainda abaixo; a partir de 1024 px, layout completo com lateral à esquerda.
- **Requisitos obrigatórios:** mobile first; variáveis CSS; `gap` no lugar de margens entre itens; `:focus` visível; contraste AA; **nenhuma** media query para a grade de cartões (use `auto-fit` / `minmax`).

<details><summary>Dica</summary>

Comece pelo esqueleto de áreas na base: `grid-template-areas: "cabecalho" "conteudo" "lateral" "rodape"` — a lateral já fica depois do conteúdo no celular sem mexer no HTML. Em 1024 px redesenhe: `"cabecalho cabecalho" "lateral conteudo" "rodape rodape"` com `grid-template-columns: 260px 1fr`. O destaque de 2 colunas é `grid-column: span 2` dentro da grade de cartões — em 360 px só há uma coluna, e o `span 2` estoura; proteja com `grid-column: 1 / -1` (da primeira à última linha-guia, quantas houver). O rodapé de 4 colunas segue o mesmo `repeat(auto-fit, minmax(200px, 1fr))`.
</details>

## 🏆 Desafios

### ⭐ Grid Garden completo
Tags: grid, layout, responsivo

Você escreveu `repeat(auto-fit, minmax())` hoje e talvez ainda não tenha certeza de por que funciona — porque decorar a linha não é o mesmo que enxergar as linhas-guia da grade. O Grid Garden é um jogo de 28 fases em que cada regra CSS rega uma horta; ele obriga a pensar em linhas-guia, `span`, valores negativos e `grid-template-areas` sem nenhum atalho.

**Critérios de pronto**

- Captura de tela da fase 28 concluída, com o seu nome visível na página (escreva-o em um comentário no editor do jogo antes do print).
- Um arquivo `grid-garden.md` com três propriedades ou valores que você **não** conhecia antes do jogo, cada um com uma linha explicando o que faz.
- Um exemplo real: aplique `grid-column: 1 / -1` em algum elemento do seu projeto autoral (o destaque da página inicial, por exemplo) e explique em um comentário por que `-1` é melhor que `span 3`.

<details><summary>Pistas</summary>

1. O jogo está em `https://cssgridgarden.com/#pt-br`, em português.
2. As fases 14 a 18 usam números de linha negativos: `-1` é sempre a última linha-guia, não importa quantas colunas a grade tenha.
3. As fases 22 em diante mostram `grid-template` e `grid-area` juntos — releia a seção "Áreas nomeadas" da Aula 07 antes de tentar.
</details>

### ⭐ Caça ao bug: o site que só funciona no monitor do professor
Tags: bug, responsivo, css, devtools

Um colega jura que "o site está responsivo, testei no meu monitor". No celular ele aparece minúsculo, com rolagem horizontal, imagem estourando e um menu que nunca vira hambúrguer. Há **seis** erros entre o HTML e o CSS abaixo. Encontre todos sem "reescrever do zero" — o desafio é diagnosticar, não refazer.

**`quebrado/index.html`** (trecho do `<head>`)

```html
<head>
  <meta charset="UTF-8">
  <title>Semana Acadêmica</title>
  <link rel="stylesheet" href="css/quebrado.css">
</head>
```

**`quebrado/css/quebrado.css`**

```css
.container {
  width: 1200px;
  margin: 0 auto;
}

.menu {
  display: flex;
  gap: 2rem;
}

@media (max-width: 768px) {
  .menu {
    flex-direction: column;
  }
}

.cartoes {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
}

.cartoes img {
  width: 800px;
}

h1 {
  font-size: 64px;
}
```

**Critérios de pronto**

- Um arquivo `diagnostico.md` com uma tabela `Erro | Sintoma que ele causa | Correção`, com as seis linhas.
- O CSS corrigido, mobile first, sem rolagem horizontal em 320 px e com o menu virando coluna no celular.
- Uma captura do DevTools em 360 px antes e outra depois da correção.

<details><summary>Pistas</summary>

1. Um dos erros não está no CSS. Sem ele, o celular finge ter 980 px e nenhuma query de `max-width: 768px` dispara.
2. Duas larguras fixas em pixels empurram o contêiner para além da tela: uma em um bloco, outra em uma imagem.
3. A media query do menu está escrita desktop first e "funcionaria" — mas pense no que acontece se, em vez de `max-width`, o projeto inteiro for migrado para `min-width`: o que precisa virar base e o que precisa ir para a query?
4. `auto-fill` com apenas três cartões deixa colunas vazias à direita em telas largas; e `64px` num `<h1>` de 360 px ocupa quatro linhas. `clamp()` resolve o segundo.
</details>

### ⭐⭐ Menu hambúrguer sem uma linha de JavaScript
Tags: css, responsivo, acessibilidade, layout

O `menu.js` de hoje tem oito linhas — mas dá para ter zero. Um `<input type="checkbox">` escondido, um `<label>` que faz papel de botão e a pseudoclasse `:checked` da Aula 06 conseguem abrir e fechar o menu só com CSS. Construa essa versão, faça funcionar, e então responda à pergunta que importa: **o que ela perde** em relação à versão com `<button>` e `aria-expanded`? Descubra testando com o teclado e com um leitor de tela (NVDA no Windows, VoiceOver no macOS, TalkBack no Android).

**Critérios de pronto**

- Menu que abre e fecha em 360 px sem nenhum `<script>`, e vira horizontal a partir de 768 px.
- O `<label>` é alcançável por <kbd>Tab</kbd> e o menu abre com <kbd>Espaço</kbd> (dica: isso exige que o checkbox continue focável — não use `display: none` nele).
- Um arquivo `comparacao.md` com uma tabela `Critério | Versão com button | Versão com checkbox` cobrindo: o que o leitor de tela anuncia ao focar o controle, se o estado aberto/fechado é anunciado, se <kbd>Enter</kbd> abre o menu, e quanto código cada versão tem.
- Uma conclusão de três linhas: qual versão você usaria no projeto autoral, e por quê.

<details><summary>Pistas</summary>

1. O seletor é o mesmo raciocínio de hoje, trocando o atributo pela pseudoclasse: `#abrir-menu:checked ~ .menu { display: flex; }` — o combinador `~` (irmão geral) alcança a lista mesmo com o `<label>` no meio.
2. Para esconder o checkbox sem tirá-lo do teclado, use a mesma técnica do link de salto da Aula 07: `position: absolute; left: -9999px`, ou a classe utilitária "visualmente oculto" (`clip`, `width: 1px`, `height: 1px`, `overflow: hidden`).
3. O anel de foco precisa aparecer no `<label>`, não no checkbox invisível: `#abrir-menu:focus-visible + label { outline: 3px solid var(--cor-secundaria); }`.
4. No leitor de tela, um checkbox é anunciado como "caixa de seleção, não marcada" — compare com "botão, recolhido" e pense em qual frase ajuda mais quem não vê a tela.
</details>

**Para ir além:** procure o elemento `<details>`/`<summary>` do HTML e tente uma terceira versão do menu com ele — sem JavaScript e com semântica de "expansível" de graça.

### ⭐⭐⭐ Nota 90 no Lighthouse Mobile
Tags: responsivo, performance, acessibilidade, devtools, projeto

Rode o Lighthouse Mobile no `index.html` do seu projeto autoral agora, antes de mexer em qualquer coisa, e guarde o relatório. É comum a primeira nota de Performance ficar abaixo de 60 em um site com fotos grandes, e a de Acessibilidade tropeçar em contraste e alvos de toque. O desafio é chegar a **90 ou mais** nas duas — e cada ponto ganho vai ter um motivo técnico que você consegue explicar.

**Critérios de pronto**

- Relatório do Lighthouse Mobile "antes" e "depois" salvos como `lighthouse-antes.html` e `lighthouse-depois.html` (o botão de três pontos do relatório exporta), com Performance ≥ 90 e Acessibilidade ≥ 90 no "depois", em todas as cinco páginas.
- Imagens servidas com `srcset` em pelo menos três larguras, com `width` e `height` declarados, e a maior versão com no máximo 200 KB.
- Tabela de dados responsiva (a técnica do B4) em pelo menos uma página.
- Tema escuro via `prefers-color-scheme` com todos os pares de contraste ≥ 4.5:1, verificados no WebAIM e listados em `contraste.md`.
- Um `melhorias.md` com, para cada alerta do "antes", a correção aplicada e a seção da aula que a explica.
- Vale como item extra da rubrica da Avaliação 2.

<details><summary>Pistas</summary>

1. Abra o relatório "antes" e clique em cada alerta: o Lighthouse mostra o elemento exato e um link "Learn more" para a explicação oficial — comece pelos itens marcados em vermelho.
2. Para gerar as três larguras de cada foto sem software pago, o Squoosh (`https://squoosh.app`) redimensiona e converte para WebP no navegador; guarde a versão JPG como reserva no `src`.
3. Fontes do Google carregadas com `<link>` custam requisições e podem derrubar Performance. **Meça** antes de decidir: rode o Lighthouse com a Inter do projeto (que já vem com `display=swap` e `preconnect` desde a Aula 06) e depois com a `font-family` trocada por `Arial, sans-serif`, e registre a diferença em pontos e em milissegundos de LCP. Se a perda for pequena, a identidade visual vale o preço — a decisão é sua, mas com número.
4. Alvos de toque menores que 48 × 48 px aparecem em "Tap targets": aumente o `padding` dos links do menu e do rodapé em vez de aumentar a fonte.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| Site aparece minúsculo no celular, com tudo em 980 px, e nenhuma media query dispara | Meta `viewport` ausente ou digitada errado (`name="viewpoint"`, `content` sem `width=device-width`) | Copie exatamente `<meta name="viewport" content="width=device-width, initial-scale=1.0">` para o `<head>` de todas as páginas |
| Rolagem horizontal no celular, mesmo com layout "responsivo" | Alguma largura fixa em pixels: `width: 1200px` em um contêiner, `width: 800px` em uma imagem, um `gap` ou `padding` grande demais para 320 px | `max-width` + `width: 100%` nos contêineres; `img { max-width: 100%; height: auto; }`; no DevTools, use `* { outline: 1px solid red; }` para achar quem estoura |
| "A media query não funciona" — a regra dentro dela é ignorada | A query está **antes** da regra base com a mesma especificidade, e a base a sobrescreve na cascata | Mova as media queries para depois das regras base (seção 7 do arquivo) |
| Cartões com colunas vazias à direita quando há poucos itens | `auto-fill` em vez de `auto-fit` | `auto-fit` colapsa as faixas vazias; use `auto-fill` só quando quiser reservar o espaço |
| Grade estoura para fora do contêiner em celulares pequenos | `minmax(280px, 1fr)` com contêiner mais estreito que 280 px | `minmax(min(280px, 100%), 1fr)` |
| Menu hambúrguer não abre ao tocar no celular, mas abre no DevTools | O `<script>` está antes do botão no HTML e sem `defer`: `querySelector` devolve `null` e o `addEventListener` falha com `Cannot read properties of null` | `<script src="js/menu.js" defer></script>` no `<head>`, ou o script no fim do `<body>` |
| Menu abre no DevTools, mas o botão não reage a <kbd>Enter</kbd> nem aparece no <kbd>Tab</kbd> | O controle é um `<div>` ou um `<span>`, não um `<button>` | Troque por `<button>` com `aria-expanded` e `aria-controls` |
| Texto ilegível no celular e o Safari dá zoom sozinho ao tocar em um campo | `font-size` abaixo de 16 px no corpo ou nos `<input>` | Corpo em `clamp(1rem, 0.95rem + 0.25vw, 1.125rem)`; campos com `font-size: 1rem` |
| Breakpoints "funcionam" no simulador e quebram no aparelho real | Larguras escolhidas de uma lista de dispositivos; o aparelho real tem outra largura ou está deitado | Defina breakpoints onde o layout quebra, e teste no modo *Responsive* arrastando a borda |
| Imagens deformadas nos cartões | `width` e `height` forçados sem `object-fit` | `aspect-ratio` + `object-fit: cover` |
| Tema escuro deixa botões brancos com texto branco | Cores escritas "na mão" (`#fff`) em vez de variáveis; variável de texto-sobre-primária inexistente | Toda cor via variável; crie `--cor-sobre-primaria` e redefina no bloco `dark` |
| Página imprime o menu, o rodapé e um fundo escuro | Sem `@media print` | Esconda navegação e rodapé, force fundo branco e texto preto na query de impressão |

## 🏠 Atividade assíncrona (1 h)

**Parte 1 — Leitura (15 min).** SILVA, Maurício Samy. *Criando sites com HTML*, capítulo de design responsivo. MDN: *Media queries* (`https://developer.mozilla.org/pt-BR/docs/Web/CSS/CSS_media_queries`) — leia a página de introdução e a de "Usando media queries"; anote a sintaxe de intervalo e as três preferências do usuário que você viu hoje.

**Parte 2 — Entrega (40 min).** No seu **projeto autoral**:

1. O exercício **B5** completo: o site responsivo em três breakpoints (mobile first, queries agrupadas no fim do `estilo.css` em ordem crescente), com as capturas de tela de cada página em 360 px, 768 px e 1440 px na pasta `capturas/`.
2. O menu responsivo do exercício **B3** funcionando em todas as páginas — no mínimo o básico da aula (`<button>`, `aria-expanded`, CSS mobile first, `menu.js` com `defer`); os fechamentos por <kbd>Esc</kbd> e por clique fora valem como extra.
3. Tema escuro via `prefers-color-scheme` e o bloco `prefers-reduced-motion` no fim do arquivo.

**Parte 3 — Fórum "Testei no celular" (5 min).** Abra o seu site em um celular real pelo IP do computador (ou peça o de um colega). Relate no fórum um problema que **só** apareceu no aparelho de verdade e não no simulador do DevTools — botão pequeno demais para o dedo, fonte ilegível, `100vh` escondido pela barra de endereço, campo que dá zoom sozinho — e como você o resolveu. Responda a um colega comparando com o que aconteceu no seu aparelho.

**Critério de pronto:** nenhuma rolagem horizontal em 320 px em nenhuma página; menu hambúrguer abre e fecha por toque, por clique e por <kbd>Enter</kbd> no teclado, com `aria-expanded` mudando no DevTools; capturas das cinco páginas nas três larguras; tema escuro sem nenhum par de contraste abaixo de 4.5:1; Lighthouse Mobile sem alerta de viewport, fonte pequena ou alvo de toque.

**Entrega:** pasta `.zip` do projeto ou link do repositório no SIGAA, mais a URL da sua mensagem no fórum.

## ✅ Checkpoint do projeto

Ao fim desta aula, o repositório do seu projeto autoral deve ter:

- [ ] Meta `viewport` correta no `<head>` das cinco páginas.
- [ ] `css/estilo.css` escrito mobile first: regras base para o celular, blocos `@media (min-width: 768px)`, `(min-width: 1024px)` e, se necessário, `(min-width: 1440px)` agrupados na seção 7, em ordem crescente.
- [ ] `img, video { max-width: 100%; height: auto; }` na seção base e nenhuma largura fixa em pixels em contêineres.
- [ ] Grade de cartões com `repeat(auto-fit, minmax(min(280px, 100%), 1fr))` e sem media query própria.
- [ ] Fotos dos cartões com `aspect-ratio` e `object-fit: cover`; imagem principal com `srcset`, `sizes`, `width` e `height`.
- [ ] Tipografia fluida com `clamp()` em `body`, `h1` e `h2`; texto corrido limitado a `65ch`.
- [ ] Menu hambúrguer com `<button aria-expanded aria-controls>`, `js/menu.js` carregado com `defer`, e menu horizontal a partir de 768 px.
- [ ] Layout de duas colunas (lateral + conteúdo) só a partir de 1024 px, via `grid-template-areas`.
- [ ] Tema escuro com `prefers-color-scheme`, variável `--cor-sobre-primaria` e `color-scheme: light dark`.
- [ ] Bloco `prefers-reduced-motion` como última regra do arquivo.
- [ ] `@media print` escondendo cabeçalho, menu e rodapé.
- [ ] Pasta `capturas/` com as quinze imagens (cinco páginas × três larguras).

## 📚 Para aprofundar

- MDN — **Media queries** (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Web/CSS/CSS_media_queries> — leia "Usando media queries" para a lista completa de condições, incluindo `hover`, `pointer` e a sintaxe de intervalo.
- MDN — **CSS Grid Layout** (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Web/CSS/CSS_grid_layout> — o guia "Grid e layouts responsivos" mostra `auto-fit`, `auto-fill` e `minmax()` com exemplos ao vivo.
- MDN — **Flexbox** (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Web/CSS/CSS_flexible_box_layout> — revise "Controlando a proporção de itens flexíveis" antes de mexer no cabeçalho.
- web.dev — **Learn CSS**: <https://web.dev/learn/css> — os módulos *Sizing units*, *Layout* e *Logical properties* explicam `clamp()`, `dvh` e `margin-inline` em profundidade.
- web.dev — **Learn Responsive Design**: <https://web.dev/learn/design> — um curso inteiro sobre o assunto de hoje, incluindo imagens responsivas, tipografia e *container queries*, o próximo passo depois das media queries.
- **Grid Garden**: <https://cssgridgarden.com/#pt-br> — as 28 fases do desafio ⭐.
- **Flexbox Froggy**: <https://flexboxfroggy.com/#pt-br> — se o cabeçalho ainda confunde, 24 fases resolvem.
- WebAIM — **Contrast Checker**: <https://webaim.org/resources/contrastchecker/> — verifique cada par do tema escuro.
- SILVA, Maurício Samy. *Criando sites com HTML: sites de alta qualidade com HTML e CSS*. Novatec, 2008 — capítulo de design responsivo.
- TERUEL, Evandro C. *HTML 5 — Guia Prático*. Saraiva, 2014 — seções sobre viewport e mídias.

Na próxima aula o site ganha movimento: transições que suavizam o `:hover` dos cartões e do menu, transformações 2D e 3D, animações com `@keyframes` — e, principalmente, como medir no painel *Performance* do DevTools por que animar `transform` é barato e animar `left` trava o celular. O bloco `prefers-reduced-motion` que você colou hoje no fim do arquivo vai fazer todo o sentido.
