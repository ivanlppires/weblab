# Aula 07 — Formatando o layout de um website e o menu

> **Nível 1 — Introdução ao Desenvolvimento Web** · Unidade 2: CSS: estilo, layout e responsividade
> WebLab · UNEMAT Sinop · Prof. Ivan Luiz Pedroso Pires
> **Carga:** 3 aulas de 50 min (presencial) + 1 h (assíncrona)

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Explicar o **fluxo normal** do navegador e prever onde um elemento vai parar com cada valor de `position` (`static`, `relative`, `absolute`, `fixed`, `sticky`).
- Controlar sobreposição com `z-index` e transbordamento com `overflow`, e explicar por que `float` não serve mais para layout.
- Construir layouts em **uma dimensão** com Flexbox: eixos, alinhamento, distribuição de espaço, `gap`, `flex-grow`, `flex-shrink` e `flex-basis`.
- Construir layouts em **duas dimensões** com CSS Grid: unidade `fr`, `repeat()`, `minmax()`, `auto-fit` e áreas nomeadas.
- Decidir, diante de um componente ou de uma página, se o problema pede Flexbox, Grid ou os dois combinados.
- Implementar um menu de navegação horizontal, fixo no topo e **acessível** (lista semântica, `aria-label`, `aria-current`, link de salto).
- Inspecionar e depurar um layout com o overlay de Flexbox e Grid do DevTools.

## 📋 Pré-requisitos

- [ ] Pasta `site-evento/` com as cinco páginas em HTML semântico da Unidade 1 (`index.html`, `programacao.html`, `inscricao.html`, `palestrantes.html`, `contato.html`), validadas no W3C.
- [ ] `site-evento/css/estilo.css` criado na Aula 06, com o reset `box-sizing: border-box`, o bloco `:root` de variáveis e a folha organizada na ordem recomendada (reset → variáveis → base → layout → componentes → utilitários → media queries).
- [ ] VS Code com a extensão Live Server e um navegador com DevTools (Chrome ou Firefox).
- [ ] Revisar da Aula 06: especificidade de seletores, `display: block` versus `display: inline`, o modelo de caixa (`margin`, `border`, `padding`) e `var(--nome)`.

> Na aula passada você estilizou o site do evento: sistema de design em variáveis, tipografia, cores, botões e tabela. Mas as páginas ainda são uma pilha de blocos de cima para baixo — o cabeçalho não fica ao lado do logo, os cartões de palestra não formam uma grade e o rodapé sobe quando a página tem pouco conteúdo. Hoje você aprende as duas ferramentas que resolvem isso — **Flexbox** e **Grid** — e constrói o esqueleto de layout definitivo do site, com um menu de navegação que qualquer pessoa consegue usar.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Fluxo normal; `position` e seus cinco valores; `z-index`; `float` como legado; `overflow`; experimentos no DevTools |
| 2 | 50 min | Flexbox completo: eixos, propriedades do contêiner e dos itens, os quatro padrões de layout que resolvem 80% dos casos |
| 3 | 50 min | CSS Grid: `fr`, `repeat`, `minmax`, áreas nomeadas; Flexbox ou Grid?; menu acessível; Mão na massa no site do evento |

## 1. Fluxo normal e posicionamento

### 1.1 O que o navegador faz quando você não diz nada

Antes de qualquer CSS de layout, o navegador já tem um plano: o **fluxo normal**. Elementos de bloco (`div`, `p`, `section`, `h1`) são empilhados de cima para baixo, cada um ocupando toda a largura disponível. Elementos em linha (`a`, `strong`, `span`, `img`) são dispostos lado a lado, da esquerda para a direita, quebrando linha quando falta espaço — exatamente como as palavras de um parágrafo.

Pense no fluxo normal como a água escorrendo por uma calha: cada caixa cai na primeira posição livre. Tudo o que você vai aprender hoje — `position`, Flexbox, Grid — é uma forma de **desviar a água**: tirar um elemento do fluxo ou trocar as regras de como os filhos de um contêiner se organizam.

> **🧠 Você sabia?**
> Toda vez que o navegador precisa recalcular a posição e o tamanho das caixas, ele faz um **reflow** (ou *layout*). Mudar a largura de um elemento no topo da página pode obrigar o navegador a recalcular a posição de **todos** os elementos abaixo dele — em uma página grande, isso custa milissegundos que se transformam em travadas visíveis. É por isso que, na Aula 09, você vai aprender a animar só propriedades que não disparam reflow. Por enquanto, guarde a ideia: layout é a etapa cara do desenho de uma página.

### 1.2 `position`: cinco maneiras de dizer "fique aqui"

A propriedade `position` define **em relação a quê** um elemento é posicionado e **se ele ainda ocupa espaço** no fluxo. As propriedades `top`, `right`, `bottom` e `left` só têm efeito quando `position` é diferente de `static`.

**Exemplo — os cinco valores lado a lado**

```css
.a { position: static; }                          /* padrão; ignora top/right/bottom/left */
.b { position: relative; top: 10px; left: 20px; } /* desloca-se da própria posição original */
.c { position: absolute; top: 0; right: 0; }      /* canto do ancestral posicionado mais próximo */
.d { position: fixed; bottom: 20px; right: 20px; } /* preso à janela; não rola com a página */
.e { position: sticky; top: 0; }                  /* normal até encostar no topo; então gruda */
```

| Valor | Referência de posicionamento | Ocupa espaço no fluxo? |
|---|---|---|
| `static` | Nenhuma — segue o fluxo normal | Sim |
| `relative` | A própria posição original | Sim (o espaço original é mantido, mesmo deslocado) |
| `absolute` | O ancestral posicionado mais próximo (ou o `<html>`) | Não — sai do fluxo |
| `fixed` | A janela do navegador (*viewport*) | Não — sai do fluxo |
| `sticky` | Fluxo normal até atingir o limite (`top`, `bottom`); depois, o contêiner de rolagem | Sim |

**A regra de ouro do `absolute`.** Um elemento `absolute` procura, subindo na árvore, o ancestral mais próximo cujo `position` seja **diferente de `static`**. Se não encontrar nenhum, ele se posiciona em relação à página inteira — e vai parar no canto do documento, longe de onde você queria. Por isso a receita clássica é: `position: relative` no **pai** (que não se move, porque sem `top`/`left` o `relative` não desloca nada) e `position: absolute` no **filho**.

No site do evento, é assim que o selo "Esgotado" fica preso no canto do cartão de um minicurso:

**`site-evento/css/estilo.css` — trecho**

```css
.cartao {
  position: relative;   /* vira a referência do selo, sem se mover */
}

.cartao__selo {
  position: absolute;   /* sai do fluxo e ancora no cartão */
  top: 8px;
  right: 8px;
}
```

**`sticky` merece atenção especial.** Ele é o híbrido: o elemento rola normalmente com a página até que a distância definida (`top: 0`) seja atingida; a partir daí, ele "gruda" e a página continua rolando por baixo. É o comportamento perfeito para um cabeçalho: não rouba espaço no topo quando a página carrega, mas fica sempre à mão. Duas condições para funcionar: declarar `top` (ou `bottom`) e nenhum ancestral com `overflow` diferente de `visible` — você vai reencontrar essa segunda condição na tabela de erros comuns.

> **💡 Dica**
> `fixed` e `sticky` parecem iguais no cabeçalho, mas diferem no resto: `fixed` sai do fluxo (o conteúdo abaixo sobe e fica escondido atrás do cabeçalho, obrigando você a compensar com `padding-top` no `body`); `sticky` continua ocupando o espaço original. Prefira `sticky` para cabeçalhos.

### 1.3 `z-index` e a pilha de elementos

Quando dois elementos posicionados se sobrepõem, quem fica na frente? Por padrão, o que vem **depois** no HTML. `z-index` muda isso: valores maiores ficam à frente. Só funciona em elementos com `position` diferente de `static` (e em itens de Flexbox e Grid).

```css
.modal   { position: fixed; z-index: 1000; }
.overlay { position: fixed; z-index: 900; }
```

> **⚠️ Atenção**
> Evite `z-index: 9999`. Quando cada componente "grita mais alto" que o anterior, ninguém sabe mais quem está na frente de quem. Defina uma **escala do projeto** e documente-a na folha de estilo. No site do evento: `100` para o cabeçalho fixo, `900` para sobreposições escuras, `1000` para modais e para o link de salto.

> **🔎 Por baixo do capô**
> `z-index` não é uma escala global. Todo elemento posicionado com `z-index` diferente de `auto` cria um **contexto de empilhamento**: os filhos dele só competem entre si, e o grupo inteiro é comparado com os vizinhos usando o `z-index` do pai. É por isso que, às vezes, um `z-index: 9999` "não funciona": o elemento está dentro de um contexto com `z-index: 1`, e o contexto inteiro está atrás de outro com `z-index: 2`. `opacity` menor que 1, `transform` e `filter` também criam contextos de empilhamento — lembre-se disso na Aula 09.

### 1.4 `float` — o legado que você precisa reconhecer

`float` foi criado com um único propósito: fazer texto envolver uma imagem, como em uma revista. Como durante mais de dez anos não existia nada melhor, a comunidade usou `float` para construir colunas, menus e páginas inteiras — com gambiarras como `clearfix` e contêineres que colapsavam. Hoje **não use `float` para layout**: Flexbox e Grid resolvem tudo isso de forma previsível. Ainda é válido para o caso original:

```css
figure { float: left; margin: 0 16px 16px 0; }  /* texto envolve a figura */
.limpa { clear: both; }                          /* próximo elemento não envolve nada */
```

Você vai encontrar `float` em código antigo, em tutoriais desatualizados e em respostas de fórum. Saiba ler; não escreva.

### 1.5 `overflow`: o que acontece quando o conteúdo não cabe

```css
overflow: visible;  /* padrão: o conteúdo transborda e aparece fora da caixa */
overflow: hidden;   /* corta o excesso */
overflow: auto;     /* barra de rolagem só quando precisar */
overflow: scroll;   /* barra sempre visível */
overflow-x: auto;   /* controle por eixo */
overflow-y: hidden;
```

Um uso legítimo no site do evento: uma tabela de programação larga, dentro de um contêiner com `overflow-x: auto`, rola horizontalmente no celular em vez de estourar a página inteira.

> **🔬 Investigue**
> Abra `index.html` com o Live Server e o DevTools (<kbd>F12</kbd>). No painel Elements, selecione o `<header>` e, na aba Styles, adicione `position: sticky; top: 0;` clicando no bloco `element.style`. Role a página: o cabeçalho gruda. Agora troque para `position: fixed`: veja o conteúdo "pular" para cima, porque o cabeçalho saiu do fluxo e deixou de ocupar espaço. Por fim, adicione `overflow-x: hidden` ao `<body>` com o `sticky` de volta — e observe que o cabeçalho **para de grudar**. Você acabou de encontrar o bug de `sticky` mais comum da web.

## 2. Flexbox — layout em uma dimensão

### 2.1 O que muda com `display: flex`

Flexbox distribui os filhos de um contêiner ao longo de **um eixo** — uma linha ou uma coluna — e resolve, com poucas propriedades, o que antes exigia truques: alinhar verticalmente, distribuir espaço sobrando, fazer itens crescerem ou encolherem, mudar a ordem visual.

```css
.contêiner {
  display: flex;
}
```

Só essa linha já transforma todos os **filhos diretos** em *flex items* e os coloca lado a lado. Os netos não são afetados — Flexbox age em um nível só. Isso importa: se você quiser um Flexbox dentro de um item, o item precisa ser, ele mesmo, um contêiner `display: flex`.

### 2.2 Os dois eixos

Tudo em Flexbox gira em torno de dois eixos. O **eixo principal** (*main axis*) segue `flex-direction`; o **eixo transversal** (*cross axis*) é perpendicular a ele.

```text
flex-direction: row (padrão)

   eixo principal (main axis) ─────────────────────────>
   ┌─────┐ ┌─────┐ ┌─────┐                          │
   │  1  │ │  2  │ │  3  │                          │ eixo transversal
   └─────┘ └─────┘ └─────┘                          │ (cross axis)
                                                    ▼

flex-direction: column

   eixo transversal ────────────>
   ┌─────┐   │
   │  1  │   │
   └─────┘   │ eixo principal
   ┌─────┐   │
   │  2  │   │
   └─────┘   ▼
```

Com `flex-direction: column`, os eixos trocam de papel: o principal passa a ser vertical. **Todas** as propriedades a seguir são definidas em relação a esses eixos, não em relação a "horizontal" e "vertical". Essa é a fonte da confusão mais comum com Flexbox — e a razão de `justify-content` alinhar horizontalmente em uma linha, mas verticalmente em uma coluna.

### 2.3 Propriedades do contêiner

```css
.contêiner {
  display: flex;

  flex-direction: row;          /* row | row-reverse | column | column-reverse */

  flex-wrap: wrap;              /* nowrap (padrão) | wrap | wrap-reverse */

  justify-content: center;      /* distribui no EIXO PRINCIPAL */
  /* flex-start | flex-end | center | space-between | space-around | space-evenly */

  align-items: center;          /* alinha no EIXO TRANSVERSAL */
  /* stretch (padrão) | flex-start | flex-end | center | baseline */

  align-content: center;        /* alinha as LINHAS entre si (só com wrap e várias linhas) */

  gap: 16px;                    /* espaço entre itens — use isto, não margin */
  row-gap: 16px;
  column-gap: 24px;
}
```

| Valor de `justify-content` | Resultado |
|---|---|
| `flex-start` | Todos encostados no início do eixo (padrão) |
| `flex-end` | Todos encostados no fim |
| `center` | Agrupados no centro |
| `space-between` | Primeiro na ponta, último na ponta, o resto distribuído por igual |
| `space-around` | Espaço igual em volta de cada item (as bordas ficam com metade) |
| `space-evenly` | Espaços exatamente iguais, inclusive nas bordas |

Repare em `align-items: stretch`, o padrão: os itens **esticam** para ocupar toda a altura do contêiner. É por isso que, em uma linha de cartões flex, todos ficam com a mesma altura sem nenhum esforço — algo que era quase impossível com `float`.

**A centralização perfeita.** Centralizar um elemento nos dois eixos foi, por vinte anos, um dos problemas mais frustrantes do CSS. Hoje são três linhas:

```css
.centro {
  display: flex;
  justify-content: center;   /* eixo principal */
  align-items: center;       /* eixo transversal */
}
```

> **🧠 Você sabia?**
> O primeiro rascunho do Flexbox é de 2009 — mas ele só se tornou utilizável em todos os navegadores por volta de 2015. Foram três sintaxes diferentes no caminho (`display: box`, depois `display: flexbox`, por fim `display: flex`), cada uma com prefixos de fornecedor (`-webkit-`, `-ms-`), e um Internet Explorer que implementou a versão intermediária e nunca atualizou. Se você encontrar `display: -webkit-box` em código antigo, é um fóssil dessa história. A lição: uma especificação só vira ferramenta quando **todos** os navegadores concordam — e isso leva tempo.

### 2.4 Propriedades dos itens

As propriedades do contêiner organizam o conjunto; as dos itens dizem como **cada um** reage ao espaço disponível.

```css
.item {
  flex-grow: 1;       /* fator de crescimento quando sobra espaço (padrão 0: não cresce) */
  flex-shrink: 1;     /* fator de encolhimento quando falta espaço (padrão 1: encolhe) */
  flex-basis: 200px;  /* tamanho inicial antes de distribuir (padrão auto: o tamanho do conteúdo) */

  flex: 1;            /* atalho = flex: 1 1 0 — todos os itens com o mesmo tamanho */
  flex: 0 0 250px;    /* largura fixa: não cresce, não encolhe */
  flex: 1 1 280px;    /* começa com 280px, cresce e encolhe conforme o espaço */

  align-self: flex-end;   /* sobrescreve align-items só neste item */
  order: 2;               /* muda a ordem visual (padrão 0; menores vêm primeiro) */
}
```

Como ler `flex: 1 1 280px`: "comece com 280 px; se sobrar espaço, cresça na proporção 1; se faltar, encolha na proporção 1". Quando todos os irmãos têm `flex: 1`, o espaço é dividido igualmente. Quando um tem `flex: 2` e os outros `flex: 1`, ele recebe o dobro do espaço **sobrando** — não o dobro do tamanho total.

> **⚠️ Atenção**
> `order` muda apenas a ordem **visual**, não a ordem do DOM. Quem navega com <kbd>Tab</kbd> ou com um leitor de tela continua seguindo a ordem do HTML — e, se a tela mostra "Contato" antes de "Início" mas o foco vai na ordem contrária, a experiência fica confusa. Use `order` com parcimônia e nunca para inverter a sequência lógica de navegação.

### 2.5 Os quatro padrões que resolvem quase tudo

**`site-evento/css/estilo.css` — trechos de exemplo**

```css
/* 1. Barra de navegação: logo à esquerda, menu à direita, tudo alinhado no centro */
.cabecalho__interno {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 32px;
}

/* 2. Menu horizontal com espaçamento uniforme */
.menu {
  display: flex;
  gap: 24px;
  list-style: none;
}

/* 3. Linha de cartões que quebra sozinha quando falta espaço */
.cartoes-flex {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
}
.cartoes-flex .cartao {
  flex: 1 1 280px;   /* mínimo 280px; cresce para preencher; quebra linha quando não couber */
}

/* 4. Rodapé sempre no fim da tela, mesmo com pouco conteúdo */
body {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
main {
  flex: 1;           /* o main absorve todo o espaço sobrando; o rodapé é empurrado para baixo */
}
```

O padrão 4 resolve um problema clássico do site do evento: a página `contato.html` tem pouco conteúdo, e o rodapé ficava flutuando no meio da tela. Com `body` em coluna e `main { flex: 1 }`, o rodapé vai para o fim da janela — e, quando a página cresce, ele desce junto.

> **🔬 Investigue**
> No DevTools, painel Elements, todo elemento com `display: flex` ganha um selo cinza escrito **flex** ao lado da tag. Clique nele: o navegador desenha o eixo principal, o contorno de cada item e os espaços de `gap`. Agora abra a aba **Layout** (Chrome) ou o painel **Flexbox** (Firefox): você pode ligar o overlay de vários contêineres ao mesmo tempo e ver, ao vivo, o que `justify-content: space-between` está fazendo com o espaço. Troque o valor na aba Styles e observe o desenho mudar.

## 3. CSS Grid — layout em duas dimensões

### 3.1 Linhas e colunas ao mesmo tempo

Flexbox pensa em uma fila. Grid pensa em uma **tabela invisível**: você declara colunas e linhas, e os filhos ocupam as células. É a ferramenta certa para a estrutura geral de uma página — cabeçalho, lateral, conteúdo, rodapé — e para qualquer coisa que precise alinhar nos dois eixos, como uma galeria.

```css
.grade {
  display: grid;
  grid-template-columns: 200px 1fr 200px;   /* três colunas: fixa, elástica, fixa */
  grid-template-rows: auto 1fr auto;        /* três linhas: conteúdo, elástica, conteúdo */
  gap: 20px;
}
```

A unidade **`fr`** (*fraction*) representa uma fração do espaço **que sobra** depois de descontar tamanhos fixos e `gap`s. Em um contêiner de 1000 px com `200px 1fr 200px` e `gap: 20px`, sobram 1000 − 200 − 200 − 40 = 560 px para a coluna do meio. Com `1fr 2fr`, o espaço livre é dividido em três partes: uma para a primeira coluna, duas para a segunda.

### 3.2 Definindo colunas

```css
grid-template-columns: 200px 200px 200px;                     /* três fixas */
grid-template-columns: 1fr 1fr 1fr;                           /* três iguais e elásticas */
grid-template-columns: repeat(3, 1fr);                        /* idem, abreviado */
grid-template-columns: 250px 1fr;                             /* lateral fixa + conteúdo elástico */
grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));  /* responsivo sem media query */
```

> **💡 Dica**
> A linha `repeat(auto-fit, minmax(250px, 1fr))` é uma das mais poderosas do CSS moderno. Leia-a assim: "crie quantas colunas couberem (`auto-fit`), cada uma com no mínimo 250 px e no máximo uma fração igual do espaço (`minmax(250px, 1fr)`)". Em uma janela de 1100 px cabem quatro colunas; em 800 px, três; em um celular, uma. A grade se reorganiza sozinha — **sem nenhuma media query**. É assim que os cartões de programação e de palestrantes do site do evento vão se comportar.

**`auto-fit` ou `auto-fill`?** Os dois criam quantas colunas couberem. A diferença aparece quando há **poucos itens**: `auto-fill` mantém as colunas vazias (três cartões em uma grade de cinco colunas ficam encolhidos à esquerda); `auto-fit` colapsa as faixas vazias e deixa os itens existentes **esticarem** para ocupar a largura toda. Para cartões, quase sempre você quer `auto-fit`.

### 3.3 Posicionando itens na grade

Grid numera as **linhas-guia** (as divisórias), não as células. Uma grade de três colunas tem quatro linhas-guia verticais: 1, 2, 3 e 4.

```css
.item {
  grid-column: 1 / 3;          /* da linha-guia 1 até a 3 — ocupa duas colunas */
  grid-column: span 2;         /* ocupa duas colunas a partir de onde estiver */
  grid-row: 2 / 4;             /* da linha-guia 2 até a 4 — ocupa duas linhas */
  grid-area: 2 / 1 / 4 / 3;    /* linha-início / coluna-início / linha-fim / coluna-fim */
}
```

Itens sem posição explícita são colocados automaticamente na próxima célula livre, na ordem do HTML. Isso é o que faz `auto-fit` funcionar sem que você precise posicionar cartão por cartão.

### 3.4 Áreas nomeadas — o layout desenhado no código

Números de linha-guia funcionam, mas ninguém lê `grid-area: 2 / 1 / 4 / 3` e visualiza a página. Áreas nomeadas resolvem isso: você **desenha** o layout com palavras.

```css
.layout {
  display: grid;
  min-height: 100vh;
  grid-template-columns: 240px 1fr;
  grid-template-rows: auto 1fr auto;
  grid-template-areas:
    "cabecalho cabecalho"
    "lateral   conteudo"
    "rodape    rodape";
  gap: 16px;
}

.cabecalho { grid-area: cabecalho; }
.lateral   { grid-area: lateral; }
.conteudo  { grid-area: conteudo; }
.rodape    { grid-area: rodape; }
```

Cada string é uma linha da grade; cada palavra, uma célula. Repetir o nome em células vizinhas faz a área se estender (o cabeçalho ocupa as duas colunas). Um ponto (`.`) marca uma célula vazia. Para reorganizar tudo no celular, basta **redesenhar** as áreas dentro de uma media query — uma coluna só, cada área em uma linha — sem tocar no HTML. Você fará exatamente isso na Aula 08.

### 3.5 Alinhamento no Grid

As propriedades de alinhamento têm os mesmos nomes do Flexbox, mas com uma camada a mais: alinhar **os itens dentro das células** e alinhar **a grade inteira dentro do contêiner**.

```css
.grade {
  justify-items: center;    /* cada item, horizontalmente, dentro da sua célula */
  align-items: center;      /* cada item, verticalmente, dentro da sua célula */
  place-items: center;      /* atalho: align-items + justify-items */

  justify-content: center;  /* a grade inteira, horizontalmente, no contêiner */
  align-content: center;    /* a grade inteira, verticalmente, no contêiner */
}
```

> **📌 Na prova**
> Em Grid, `justify-*` sempre se refere ao eixo horizontal (colunas) e `align-*` ao vertical (linhas). Em Flexbox, `justify-content` segue o **eixo principal**, que muda com `flex-direction`. Essa diferença cai em prova — e cai no dia a dia.

> **🔬 Investigue**
> Selecione no DevTools qualquer elemento com `display: grid`; ele ganha um selo **grid**. Clique nele e vá à aba Layout: ative "Show line numbers" e "Show area names". O navegador desenha as linhas-guia numeradas e escreve o nome de cada área por cima da página. Redimensione a janela com o overlay ligado e veja `auto-fit` criando e removendo colunas. Esse overlay vai economizar horas de tentativa e erro — use-o sempre que um item cair na célula errada.

## 4. Flexbox ou Grid?

A pergunta certa não é "qual é melhor", e sim "quantas dimensões o problema tem".

| Use Flexbox quando | Use Grid quando |
|---|---|
| O layout é **uma** linha ou **uma** coluna | Você precisa controlar linhas **e** colunas |
| O tamanho dos itens (conteúdo) define a distribuição | O contêiner define a estrutura, e o conteúdo se encaixa |
| Barra de navegação, grupo de botões, cartões em linha, campo de busca com botão | Estrutura da página, galerias, dashboards, formulários em colunas |
| Alinhar coisas **dentro** de um componente | Posicionar os componentes **na página** |

Eles não competem — se combinam. A arquitetura padrão de um site hoje é: **Grid para a estrutura da página** (onde ficam cabeçalho, lateral, conteúdo, rodapé) e **Flexbox para o interior de cada componente** (o que há dentro do cabeçalho, de um cartão, de um formulário). É assim que o site do evento vai ficar ao fim desta aula.

Dois testes rápidos para decidir:

1. **Você consegue descrever o layout com uma frase que tenha "ao lado" ou "abaixo", mas não os dois?** Flexbox. ("Logo ao lado do menu"; "campos empilhados abaixo do outro".)
2. **Você precisa que a segunda linha se alinhe com a primeira?** Grid. (Uma galeria em que as colunas precisam bater; um formulário em que os rótulos alinham nas duas linhas.)

## 5. Construindo o menu de navegação

O menu é o componente que mais aparece em avaliação e o que mais concentra erros de acessibilidade. Ele também é a primeira coisa que todo visitante toca. Vale construí-lo com cuidado.

### 5.1 Marcação

**`site-evento/index.html` — trecho do cabeçalho**

```html
<header class="cabecalho">
  <div class="container cabecalho__interno">
    <a href="index.html" class="logo">
      <img src="img/logo.svg" alt="Página inicial — Semana Acadêmica de Sistemas de Informação">
    </a>

    <nav aria-label="Principal">
      <ul class="menu">
        <li><a href="index.html" aria-current="page">Início</a></li>
        <li><a href="programacao.html">Programação</a></li>
        <li><a href="palestrantes.html">Palestrantes</a></li>
        <li><a href="contato.html">Contato</a></li>
        <li><a href="inscricao.html" class="menu__cta">Inscreva-se</a></li>
      </ul>
    </nav>
  </div>
</header>
```

Três pontos que valem nota:

1. **O menu é uma lista** (`ul`/`li`). Leitores de tela anunciam "lista com 5 itens" ao entrar nela — o usuário sabe o tamanho da navegação antes de percorrê-la. Uma sequência de `<a>` soltos não dá essa informação.
2. **`<nav aria-label="Principal">`** distingue esta navegação de outras que a página pode ter (a do rodapé, uma trilha de "você está aqui", os filtros da programação). Sem o rótulo, o leitor de tela anuncia só "navegação", e o usuário não sabe qual.
3. **`aria-current="page"`** marca a página atual **semanticamente**, não só com cor. Quem não enxerga a cor (por daltonismo ou por usar leitor de tela) recebe a mesma informação. Em cada página do site, o atributo vai no link correspondente — e o CSS usa o atributo como seletor, então o destaque visual vem de graça.

O `alt` do logo diz para onde o link leva ("Página inicial") e o que a imagem é, porque um logo dentro de um link é, antes de tudo, um link.

### 5.2 Estilo

**`site-evento/css/estilo.css` — seção 4 (layout)**

```css
.cabecalho {
  background: var(--cor-superficie);
  border-bottom: 1px solid var(--cor-borda);
  position: sticky;
  top: 0;
  z-index: 100;
}

.cabecalho__interno {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--espaco-grande);
  padding-block: var(--espaco-medio);
}

.logo img {
  display: block;   /* remove o espaço fantasma abaixo da imagem em linha */
  height: 40px;
  width: auto;
}

.menu {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  list-style: none;
}

.menu a {
  position: relative;      /* referência para o sublinhado (::after) */
  display: block;
  padding: .5rem 0;
  color: var(--cor-texto);
  text-decoration: none;
  font-weight: 500;
}

/* Sublinhado que cresce — a Aula 09 explica transform e transition em detalhe */
.menu a::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  height: 2px;
  background: var(--cor-primaria);
  transform: scaleX(0);
  transition: transform 200ms ease;
}

.menu a:hover::after,
.menu a:focus-visible::after,
.menu a[aria-current="page"]::after {
  transform: scaleX(1);
}

.menu a[aria-current="page"] {
  color: var(--cor-primaria);
  font-weight: 600;
}

/* O botão-pílula de inscrição */
.menu a.menu__cta {
  padding: .5rem 1.25rem;
  background: var(--cor-primaria);
  color: #fff;
  border-radius: 999px;
}

.menu a.menu__cta::after {
  display: none;           /* o botão não recebe o sublinhado */
}

.menu a.menu__cta:hover,
.menu a.menu__cta:focus-visible {
  background: var(--cor-secundaria);
}
```

> **💡 Dica**
> Repare no seletor `.menu a.menu__cta` em vez de só `.menu__cta`. Como vimos na Aula 06, `.menu a` tem especificidade (0,1,1) e vence `.menu__cta` (0,1,0) — se você escrevesse só a classe, o `color: #fff` seria ignorado e o botão ficaria com texto escuro sobre fundo escuro. `.menu a.menu__cta` tem (0,2,1) e ganha. Quando um estilo "não pega", a especificidade é a primeira suspeita.

Duas decisões pequenas com efeito grande:

- **`:focus-visible` ao lado de `:hover`** em todos os estados. Quem navega por teclado precisa ver onde está — e o contorno padrão do navegador, que você talvez tenha removido com `outline: none` em algum momento, era exatamente isso. Nunca remova o `outline` sem oferecer uma alternativa visível.
- **`display: block` nos links** aumenta a área clicável para o padding inteiro, e não só para o texto. No celular, isso é a diferença entre acertar e errar o toque.

### 5.3 Link de salto — o detalhe profissional

Quem navega por teclado não deveria ter que percorrer o menu inteiro, em **toda** página, para chegar ao conteúdo. O link de salto é o primeiro elemento do `<body>`: invisível para quem usa mouse, é o primeiro que aparece ao pressionar <kbd>Tab</kbd>.

**`site-evento/index.html` — logo após `<body>` e o início do `<main>`**

```html
<body>
  <a href="#conteudo" class="salto">Pular para o conteúdo</a>

  <header class="cabecalho">
    <div class="container cabecalho__interno">
      <a href="index.html" class="logo">
        <img src="img/logo.svg" alt="Página inicial — Semana Acadêmica de Sistemas de Informação">
      </a>
      <nav aria-label="Principal">
        <ul class="menu">
          <li><a href="index.html" aria-current="page">Início</a></li>
          <li><a href="programacao.html">Programação</a></li>
          <li><a href="palestrantes.html">Palestrantes</a></li>
          <li><a href="contato.html">Contato</a></li>
          <li><a href="inscricao.html" class="menu__cta">Inscreva-se</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <main id="conteudo" tabindex="-1">
    <h1>Semana Acadêmica de Sistemas de Informação</h1>
  </main>
</body>
```

**`site-evento/css/estilo.css` — seção 6 (utilitários)**

```css
.salto {
  position: absolute;
  left: -9999px;            /* fora da tela, mas presente para o teclado e o leitor de tela */
  top: 1rem;
  padding: .75rem 1.25rem;
  background: var(--cor-primaria);
  color: #fff;
  border-radius: var(--raio-borda);
  z-index: 1000;
}

.salto:focus {
  left: 1rem;               /* ao receber foco, entra na tela */
}
```

O `tabindex="-1"` no `<main>` permite que ele **receba foco** ao ser alvo do link (sem entrar na sequência normal do <kbd>Tab</kbd>), o que faz o leitor de tela começar a ler dali. Sem isso, alguns navegadores rolam até o conteúdo, mas o foco continua no link de salto.

> **🔎 Por baixo do capô**
> Por que `left: -9999px` e não `display: none`? Porque `display: none` **remove** o elemento da árvore de acessibilidade: ele deixa de existir para o teclado e para o leitor de tela. Deslocar para fora da tela mantém o elemento "vivo" — invisível, mas focável. É o mesmo raciocínio que você vai reencontrar na Aula 09, quando `display` não puder ser animado.

### 5.4 O que fica para a próxima aula

Esse menu funciona perfeitamente em telas largas. No celular, cinco links não cabem lado a lado — e a solução é o menu "hambúrguer", que abre e fecha. A versão responsiva do menu fica para a Aula 08, porque depende de media queries e de um pouco de raciocínio *mobile first* que você ainda não viu. Hoje, o menu quebra linha de forma aceitável graças ao `flex-wrap` que você vai adicionar na Mão na massa.

## 💻 Mão na massa — Esqueleto do site do evento com Grid e Flexbox

Você vai aplicar tudo isso no site da **Semana Acadêmica de Sistemas de Informação**. Ao final, as cinco páginas terão o mesmo cabeçalho fixo com menu acessível, o rodapé no fim da tela, a página inicial com um herói em duas colunas, a programação com lateral de filtros e grade de cartões, e os palestrantes em uma galeria que se reorganiza sozinha.

### Passo 1 — Novas variáveis e a escala de `z-index`

Abra `site-evento/css/estilo.css`. Na seção 2 (variáveis), acrescente três variáveis ao bloco `:root` que você criou na Aula 06 e documente a escala de empilhamento em um comentário.

**`site-evento/css/estilo.css` — seção 2 (variáveis), bloco completo**

```css
/* 2. Variáveis */
:root {
  --cor-primaria: #0b3d5c;
  --cor-secundaria: #1a7fb5;
  --cor-texto: #333333;
  --cor-fundo: #f7f9fb;
  --cor-superficie: #ffffff;   /* fundo de cabeçalho e cartões */
  --cor-borda: #dfe6ec;        /* linhas divisórias */
  --fonte-base: "Inter", Arial, sans-serif;
  --espaco-pequeno: 8px;
  --espaco-medio: 16px;
  --espaco-grande: 32px;
  --raio-borda: 8px;
  --sombra-card: 0 2px 8px rgba(0, 0, 0, 0.1);
  --largura-max: 1100px;       /* largura máxima do conteúdo */
}

/* Escala de z-index do projeto:
   100  cabeçalho fixo
   900  sobreposições escuras (overlay)
   1000 modais e link de salto */
```

### Passo 2 — Rodapé no fim da tela e o contêiner central

Na seção 4 (layout), substitua o `main { max-width: 1100px; margin: 0 auto; }` da Aula 06 pelo padrão do `body` em coluna e por uma classe `.container` reutilizável.

**`site-evento/css/estilo.css` — seção 4 (layout), início**

```css
/* 4. Layout */
body {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex: 1;                     /* empurra o rodapé para o fim da janela */
}

.container {
  width: 100%;
  max-width: var(--largura-max);
  margin-inline: auto;         /* centraliza horizontalmente */
  padding-inline: var(--espaco-medio);
}
```

`margin-inline` e `padding-inline` são as versões "lógicas" de `margin-left`/`margin-right` — funcionam também em idiomas escritos da direita para a esquerda. Use-as sempre que a intenção for "dos lados".

### Passo 3 — Cabeçalho e menu em todas as páginas

Coloque o cabeçalho da seção 5.1 nas **cinco** páginas, trocando o `aria-current="page"` para o link da página correspondente. Em `programacao.html`, por exemplo:

**`site-evento/programacao.html` — cabeçalho**

```html
<a href="#conteudo" class="salto">Pular para o conteúdo</a>

<header class="cabecalho">
  <div class="container cabecalho__interno">
    <a href="index.html" class="logo">
      <img src="img/logo.svg" alt="Página inicial — Semana Acadêmica de Sistemas de Informação">
    </a>

    <nav aria-label="Principal">
      <ul class="menu">
        <li><a href="index.html">Início</a></li>
        <li><a href="programacao.html" aria-current="page">Programação</a></li>
        <li><a href="palestrantes.html">Palestrantes</a></li>
        <li><a href="contato.html">Contato</a></li>
        <li><a href="inscricao.html" class="menu__cta">Inscreva-se</a></li>
      </ul>
    </nav>
  </div>
</header>
```

Cole o CSS do cabeçalho e do menu da seção 5.2 na seção 4 da folha de estilo, e acrescente `flex-wrap: wrap` ao `.menu`, para que os links quebrem linha em vez de estourar o cabeçalho quando a janela for estreita — um paliativo até a Aula 08:

**`site-evento/css/estilo.css` — ajuste no `.menu`**

```css
.menu {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 1.5rem;
  list-style: none;
}
```

### Passo 4 — Link de salto

Adicione o `<a href="#conteudo" class="salto">` como primeiro filho do `<body>` em todas as páginas, coloque `id="conteudo" tabindex="-1"` no `<main>` de cada uma e cole o CSS de `.salto` na seção 6 (utilitários).

### Passo 5 — Herói da página inicial com Grid

A página inicial abre com um "herói": título, texto de chamada, dois botões e a imagem do evento. Em telas largas, texto e imagem ficam lado a lado; em telas estreitas, empilham — e o `auto-fit` decide sozinho.

**`site-evento/index.html` — conteúdo do `<main>`**

```html
<main id="conteudo" tabindex="-1">
  <section class="container hero">
    <div class="hero__texto">
      <h1>Semana Acadêmica de Sistemas de Informação</h1>
      <p>Três dias de palestras, minicursos e maratona de programação no campus de Sinop. Aberto a estudantes de todos os cursos.</p>
      <div class="hero__acoes">
        <a class="botao" href="inscricao.html">Inscreva-se</a>
        <a class="botao botao--secundario" href="programacao.html">Ver programação</a>
      </div>
    </div>
    <img src="img/banner.jpg" alt="Auditório lotado durante a abertura da edição anterior" width="1200" height="800">
  </section>
</main>
```

**`site-evento/css/estilo.css` — seção 4 (layout)**

```css
.hero {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  align-items: center;
  gap: var(--espaco-grande);
  padding-block: var(--espaco-grande);
}

.hero img {
  width: 100%;
  height: auto;
  border-radius: var(--raio-borda);
}

.hero__acoes {
  display: flex;
  flex-wrap: wrap;
  gap: var(--espaco-medio);
  margin-top: var(--espaco-medio);
}
```

Se o `.botao--secundario` ainda não existir, crie-o na seção 5 (componentes) como uma variação com fundo transparente e borda na cor primária:

**`site-evento/css/estilo.css` — seção 5 (componentes)**

```css
.botao--secundario {
  background-color: transparent;
  color: var(--cor-primaria);
  border: 2px solid var(--cor-primaria);
}

.botao--secundario:hover,
.botao--secundario:focus-visible {
  background-color: var(--cor-primaria);
  color: #fff;
}
```

### Passo 6 — Programação: lateral de filtros e grade de cartões

A programação é a página mais rica do site. Em telas largas, ela tem uma **lateral** com filtros por dia e uma área de **conteúdo** com os cartões de cada atividade. É Grid para a estrutura (lateral + conteúdo) e Grid de novo, com `auto-fit`, para os cartões — e Flexbox dentro de cada cartão.

**`site-evento/programacao.html` — conteúdo do `<main>`**

```html
<main id="conteudo" tabindex="-1" class="container pagina">
  <aside class="lateral">
    <h2>Filtrar por dia</h2>
    <nav aria-label="Dias do evento">
      <ul class="lista-filtros">
        <li><a href="#dia-1">Dia 1 — Segunda-feira</a></li>
        <li><a href="#dia-2">Dia 2 — Terça-feira</a></li>
        <li><a href="#dia-3">Dia 3 — Quarta-feira</a></li>
      </ul>
    </nav>
  </aside>

  <section class="conteudo">
    <h1>Programação</h1>

    <h2 id="dia-1">Dia 1 — Segunda-feira</h2>
    <ul class="cartoes">
      <li class="cartao">
        <h3>Abertura e palestra magna</h3>
        <p class="cartao__meta"><time datetime="19:00">19h</time> · Auditório Central</p>
        <p>O futuro do desenvolvimento web e o papel de quem está começando agora.</p>
        <a class="botao" href="inscricao.html">Inscrever-se</a>
      </li>
      <li class="cartao">
        <span class="cartao__selo">Esgotado</span>
        <h3>Minicurso: Git e GitHub do zero</h3>
        <p class="cartao__meta"><time datetime="20:00">20h</time> · Laboratório 2</p>
        <p>Versionamento, branches e o primeiro pull request. Traga o notebook.</p>
        <a class="botao" href="inscricao.html" aria-disabled="true">Lista de espera</a>
      </li>
      <li class="cartao">
        <h3>Mesa-redonda: mercado de trabalho em Sinop</h3>
        <p class="cartao__meta"><time datetime="20:00">20h</time> · Sala 105</p>
        <p>Egressos e empresas da região conversam sobre estágios e primeiro emprego.</p>
        <a class="botao" href="inscricao.html">Inscrever-se</a>
      </li>
    </ul>

    <h2 id="dia-2">Dia 2 — Terça-feira</h2>
    <ul class="cartoes">
      <li class="cartao">
        <h3>Minicurso: acessibilidade na prática</h3>
        <p class="cartao__meta"><time datetime="19:00">19h</time> · Laboratório 1</p>
        <p>Teste seu site com leitor de tela e só com o teclado.</p>
        <a class="botao" href="inscricao.html">Inscrever-se</a>
      </li>
      <li class="cartao">
        <h3>Palestra: segurança em aplicações web</h3>
        <p class="cartao__meta"><time datetime="20:30">20h30</time> · Auditório Central</p>
        <p>Os dez erros mais comuns e como evitá-los desde o primeiro commit.</p>
        <a class="botao" href="inscricao.html">Inscrever-se</a>
      </li>
    </ul>

    <h2 id="dia-3">Dia 3 — Quarta-feira</h2>
    <ul class="cartoes">
      <li class="cartao">
        <h3>Maratona de programação</h3>
        <p class="cartao__meta"><time datetime="18:30">18h30</time> · Laboratórios 1 e 2</p>
        <p>Equipes de três pessoas, quatro horas, dez problemas. Premiação no encerramento.</p>
        <a class="botao" href="inscricao.html">Inscrever equipe</a>
      </li>
      <li class="cartao">
        <h3>Encerramento e premiação</h3>
        <p class="cartao__meta"><time datetime="22:00">22h</time> · Auditório Central</p>
        <p>Resultados da maratona, sorteios e confraternização.</p>
        <a class="botao" href="inscricao.html">Inscrever-se</a>
      </li>
    </ul>
  </section>
</main>
```

**`site-evento/css/estilo.css` — seção 4 (layout) e seção 5 (componentes)**

```css
/* Estrutura da página de programação: lateral + conteúdo */
.pagina {
  display: grid;
  grid-template-columns: 240px 1fr;
  grid-template-areas: "lateral conteudo";
  gap: var(--espaco-grande);
  padding-block: var(--espaco-grande);
}

.lateral  { grid-area: lateral; }
.conteudo { grid-area: conteudo; }

.lateral {
  align-self: start;           /* não estica até o fim da coluna */
  position: sticky;            /* acompanha a rolagem, abaixo do cabeçalho */
  top: 88px;                   /* altura do cabeçalho + respiro */
}

.lista-filtros {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: var(--espaco-pequeno);
}

.lista-filtros a {
  display: block;
  padding: var(--espaco-pequeno) var(--espaco-medio);
  border-left: 3px solid var(--cor-borda);
  color: var(--cor-texto);
  text-decoration: none;
}

.lista-filtros a:hover,
.lista-filtros a:focus-visible {
  border-left-color: var(--cor-primaria);
  color: var(--cor-primaria);
}

/* Grade de cartões: quantas colunas couberem, mínimo 280px cada */
.cartoes {
  list-style: none;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--espaco-medio);
  margin-block: var(--espaco-medio) var(--espaco-grande);
}

/* 5. Componentes */
.cartao {
  position: relative;          /* referência para o selo */
  display: flex;               /* Flexbox DENTRO do cartão */
  flex-direction: column;
  gap: var(--espaco-pequeno);
  padding: var(--espaco-medio);
  background: var(--cor-superficie);
  border: 1px solid var(--cor-borda);
  border-radius: var(--raio-borda);
  box-shadow: var(--sombra-card);
}

.cartao .botao {
  margin-top: auto;            /* empurra o botão para o fim, alinhando todos os cartões */
  align-self: flex-start;      /* o botão não estica até a largura do cartão */
}

.cartao__meta {
  color: var(--cor-secundaria);
  font-size: .875rem;
  font-weight: 600;
}

.cartao__selo {
  position: absolute;
  top: var(--espaco-pequeno);
  right: var(--espaco-pequeno);
  padding: 2px 10px;
  font-size: .75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: .04em;
  background: #b42318;
  color: #fff;
  border-radius: 999px;
}
```

Repare no truque `margin-top: auto` dentro de um contêiner flex em coluna: a margem automática absorve todo o espaço sobrando e empurra o botão para o rodapé do cartão. Como `align-items: stretch` (o padrão do Grid) deixa todos os cartões da linha com a mesma altura, os botões ficam alinhados mesmo que os textos tenham tamanhos diferentes.

### Passo 7 — Palestrantes: galeria que se reorganiza sozinha

A página de palestrantes reaproveita `.cartoes` e `.cartao`, com uma variação para a foto.

**`site-evento/palestrantes.html` — conteúdo do `<main>`**

```html
<main id="conteudo" tabindex="-1" class="container">
  <h1>Palestrantes</h1>
  <p>Profissionais e pesquisadores que vão compartilhar experiências nesta edição.</p>

  <ul class="cartoes">
    <li class="cartao cartao--palestrante">
      <img class="cartao__foto" src="img/ana-souza.jpg" alt="Ana Souza" width="400" height="400">
      <h2>Ana Souza</h2>
      <p class="cartao__meta">Engenheira de software · Palestra magna</p>
      <p>Trabalha com plataformas web de grande escala e mantém projetos de código aberto.</p>
    </li>
    <li class="cartao cartao--palestrante">
      <img class="cartao__foto" src="img/bruno-lima.jpg" alt="Bruno Lima" width="400" height="400">
      <h2>Bruno Lima</h2>
      <p class="cartao__meta">Analista de segurança · Palestra</p>
      <p>Atua com resposta a incidentes e treina equipes de desenvolvimento em segurança.</p>
    </li>
    <li class="cartao cartao--palestrante">
      <img class="cartao__foto" src="img/carla-mendes.jpg" alt="Carla Mendes" width="400" height="400">
      <h2>Carla Mendes</h2>
      <p class="cartao__meta">Professora · Minicurso de acessibilidade</p>
      <p>Pesquisa interação humano-computador e tecnologias assistivas.</p>
    </li>
    <li class="cartao cartao--palestrante">
      <img class="cartao__foto" src="img/diego-rocha.jpg" alt="Diego Rocha" width="400" height="400">
      <h2>Diego Rocha</h2>
      <p class="cartao__meta">Egresso · Mesa-redonda</p>
      <p>Formou-se no campus e hoje lidera um time de front-end em uma empresa de Sinop.</p>
    </li>
  </ul>
</main>
```

**`site-evento/css/estilo.css` — seção 5 (componentes)**

```css
.cartao--palestrante {
  align-items: center;         /* centraliza foto, nome e texto no eixo transversal */
  text-align: center;
}

.cartao__foto {
  width: 120px;
  height: 120px;
  border-radius: 50%;          /* foto redonda */
  object-fit: cover;           /* recorta sem distorcer — a Aula 08 aprofunda */
}
```

### Passo 8 — Rodapé em três colunas

**`site-evento/index.html` — antes de `</body>`, em todas as páginas**

```html
<footer class="rodape">
  <div class="container rodape__grade">
    <section>
      <h2>Sobre o evento</h2>
      <p>Organizado pelos cursos de computação da UNEMAT, campus Sinop, com apoio do centro acadêmico.</p>
    </section>
    <section>
      <h2>Links</h2>
      <ul>
        <li><a href="programacao.html">Programação completa</a></li>
        <li><a href="inscricao.html">Inscrições</a></li>
        <li><a href="contato.html">Fale com a organização</a></li>
      </ul>
    </section>
    <section>
      <h2>Contato</h2>
      <address>
        <a href="mailto:semana@exemplo.edu.br">semana@exemplo.edu.br</a><br>
        Avenida dos Ingás, 3001 — Sinop, MT
      </address>
    </section>
  </div>
  <p class="rodape__creditos">Semana Acadêmica de Sistemas de Informação · UNEMAT Sinop</p>
</footer>
```

**`site-evento/css/estilo.css` — seção 4 (layout)**

```css
.rodape {
  margin-top: var(--espaco-grande);
  padding-block: var(--espaco-grande);
  background: var(--cor-primaria);
  color: #fff;
}

.rodape__grade {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--espaco-grande);
}

.rodape h2 {
  font-size: 1rem;
  margin-bottom: var(--espaco-pequeno);
}

.rodape ul {
  list-style: none;
}

.rodape a {
  color: #fff;
}

.rodape address {
  font-style: normal;
}

.rodape__creditos {
  margin-top: var(--espaco-grande);
  text-align: center;
  font-size: .875rem;
  opacity: .85;
}
```

### Passo 9 — Um paliativo para telas estreitas

A grade de cartões e o rodapé já se adaptam sozinhos graças ao `auto-fit`. A página de programação, não: com `240px 1fr`, em um celular a coluna de conteúdo fica com 100 px de largura. Por hoje, uma media query simples resolve — a Aula 08 vai inverter essa lógica para *mobile first* e formalizar os breakpoints.

**`site-evento/css/estilo.css` — seção 7 (media queries)**

```css
/* 7. Media queries */
@media (max-width: 1023px) {
  .pagina {
    grid-template-columns: 1fr;
    grid-template-areas:
      "conteudo"
      "lateral";               /* no celular, os filtros vão para depois do conteúdo */
  }

  .lateral {
    position: static;          /* deixa de acompanhar a rolagem */
  }
}
```

### Como testar

1. Abra `index.html` com o Live Server. O cabeçalho deve ficar grudado no topo ao rolar, com o logo à esquerda e o menu à direita, e o link "Início" destacado com o sublinhado na cor primária.
2. Pressione <kbd>Tab</kbd> uma vez: o botão "Pular para o conteúdo" deve aparecer no canto superior esquerdo. Pressione <kbd>Enter</kbd>: o foco vai para o `<main>`. Continue com <kbd>Tab</kbd>: cada link do menu mostra o sublinhado crescendo.
3. Abra `contato.html` (a página com menos conteúdo): o rodapé deve estar colado no fim da janela, não flutuando no meio.
4. Em `programacao.html`, a lateral fica à esquerda e os cartões à direita, em colunas de no mínimo 280 px; o selo "Esgotado" aparece no canto superior direito do minicurso de Git; todos os botões de uma mesma linha ficam alinhados na base. Redimensione a janela: abaixo de 1024 px, tudo vira uma coluna e a lateral vai para o fim.
5. Em `palestrantes.html`, as fotos são redondas e os cartões se reorganizam de 4 para 3, 2 e 1 coluna conforme você estreita a janela — sem nenhuma media query.
6. No DevTools, clique no selo **grid** ao lado de `<ul class="cartoes">` e no selo **flex** ao lado de `<div class="cabecalho__interno">` e confira, com o overlay, que a estrutura é a que você desenhou.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Explique a diferença entre `position: relative`, `absolute` e `fixed` quanto a dois critérios: a **referência** de posicionamento e a **ocupação de espaço** no fluxo.

**A2.** Por que um elemento com `position: absolute` costuma exigir `position: relative` no elemento pai? O que acontece se o pai não tiver essa declaração?

**A3.** Em um contêiner com `display: flex` e `flex-direction: row`, qual propriedade alinha os itens horizontalmente? E verticalmente? E se a direção for `column`?

**A4.** Diferencie `space-between`, `space-around` e `space-evenly`. Desenhe (em papel ou em texto) três itens em cada caso, marcando os espaços.

**A5.** O que significa `flex: 1`? Escreva sua forma expandida (as três propriedades) e explique o que cada valor faz.

**A6.** Escreva o CSS para centralizar perfeitamente um elemento na tela, horizontal e verticalmente, usando Flexbox. Depois reescreva usando Grid com uma linha só.

**A7.** O que a unidade `fr` representa? Em `grid-template-columns: 200px 1fr 2fr`, com um contêiner de 1100 px e `gap: 0`, qual é a largura de cada coluna? Mostre a conta.

**A8.** Explique, palavra por palavra, o que faz `repeat(auto-fit, minmax(250px, 1fr))`. Quantas colunas ela cria em uma janela de 1100 px? E em uma de 600 px?

**A9.** Escreva um `grid-template-areas` para um layout com cabeçalho no topo (largura total), lateral à esquerda, conteúdo à direita e rodapé embaixo (largura total). Inclua o `grid-template-columns` e o `grid-template-rows` correspondentes.

**A10.** Quando você usaria Flexbox e quando usaria Grid? Dê dois exemplos concretos de cada, tirados do site do evento.

**A11.** Por que `float` não deve mais ser usado para layout? Cite o único caso em que ele ainda é a ferramenta certa.

### Nível B — Aplicação

**B1.** Construa uma barra de navegação com Flexbox: logo à esquerda, cinco links à direita, item ativo destacado com `aria-current="page"`. Em telas abaixo de 768 px, os links devem virar uma coluna centralizada abaixo do logo.

Resultado esperado: em 1200 px, logo e links na mesma linha, com `space-between`; em 500 px, o logo centralizado em cima e os cinco links empilhados e centralizados abaixo; o link ativo tem cor e sublinhado diferentes; <kbd>Tab</kbd> percorre os links na ordem do HTML com foco visível.

<details><summary>Dica</summary>

Na media query, troque `flex-direction` do contêiner do cabeçalho para `column` e do `.menu` também; `align-items: center` centraliza os dois. Não use `order` — a ordem do HTML já é a que você quer.
</details>

**B2.** Implemente o layout "santo graal": cabeçalho, três colunas (lateral esquerda fixa de 200 px, conteúdo elástico, lateral direita fixa de 200 px) e rodapé, com o rodapé sempre no fim da janela mesmo com pouco conteúdo. Em telas pequenas, tudo vira uma única coluna. Faça com Grid e áreas nomeadas.

Resultado esperado: em 1200 px, cinco áreas visíveis com `grid-template-areas` de três linhas; com um parágrafo só no conteúdo, o rodapé continua colado no fim da janela; abaixo de 768 px, as áreas se empilham na ordem cabeçalho → conteúdo → lateral esquerda → lateral direita → rodapé.

<details><summary>Dica</summary>

Use `min-height: 100vh` e `grid-template-rows: auto 1fr auto` no contêiner: a linha `1fr` absorve o espaço sobrando. Na media query, redesenhe as áreas com uma palavra por linha — a ordem das strings define a ordem visual, sem tocar no HTML.
</details>

**B3.** Crie uma seção de "planos de inscrição" para o site do evento com três planos lado a lado (Flexbox): Estudante, Profissional e Apoiador. O do meio deve ser destacado (maior, com borda colorida e um selo "Mais popular" posicionado com `absolute`). Responsivo: os três empilham abaixo de 768 px.

Resultado esperado: três cartões com a mesma altura em telas largas, o do meio 8% maior (`transform: scale(1.08)` ou `padding` maior) e com borda na cor primária; o selo fica preso no canto superior direito do cartão do meio, mesmo ao redimensionar; no celular, os cartões ficam um abaixo do outro e o do meio deixa de ser maior.

<details><summary>Dica</summary>

`align-items: stretch` (o padrão) já iguala as alturas. Para o selo, `position: relative` no cartão e `absolute` no selo — a receita da seção 1.2. Lembre-se de `flex: 1 1 260px` nos cartões para que eles cresçam e quebrem linha.
</details>

**B4.** Reescreva o layout do exercício B3 duas vezes: uma versão **só com Flexbox** e outra **só com Grid**. Escreva meia página comparando a quantidade de código, a legibilidade e a facilidade de alteração de cada abordagem (ex.: o que muda para acrescentar um quarto plano?).

Resultado esperado: dois arquivos HTML funcionais e visualmente idênticos, e um texto de comparação com pelo menos três diferenças concretas, apontando qual versão você escolheria para o site do evento e por quê.

<details><summary>Dica</summary>

Conte as linhas de CSS de cada versão. Na versão Grid, experimente `grid-template-columns: repeat(auto-fit, minmax(260px, 1fr))` e veja o que acontece ao adicionar um quarto cartão. Na versão Flexbox, veja o que `flex-wrap` faz com um número ímpar de cartões na última linha.
</details>

**B5.** Construa um painel (dashboard) da organização do evento com Grid: cabeçalho, quatro cartões de indicadores na primeira linha (inscritos, vagas, palestrantes, minicursos), um cartão grande de "inscrições por dia" ocupando três colunas e um de "últimas inscrições" ocupando uma coluna na segunda linha, e uma tabela de atividades ocupando toda a largura na terceira. Responsivo em três breakpoints.

Resultado esperado: em 1200 px, uma grade de quatro colunas com os `span`s corretos; em 768 px, duas colunas (os indicadores em 2 × 2, o gráfico em largura total); no celular, tudo em uma coluna; a tabela nunca estoura a largura (use um contêiner com `overflow-x: auto`).

<details><summary>Dica</summary>

Defina `grid-template-columns: repeat(4, 1fr)` na base e use `grid-column: span 3` e `span 4` nos itens grandes. Nas media queries, troque o `repeat(4, 1fr)` por `repeat(2, 1fr)` e `1fr`, e ajuste os `span`s para que nenhum item peça mais colunas do que a grade tem — se pedir, o Grid cria colunas implícitas e o layout estoura.
</details>

### Nível C — Desafio em sala

**C1.** Base do projeto autoral. Defina o tema do seu projeto (o "site do evento" da sua versão: uma feira, um campeonato, uma semana cultural, um curso de extensão) e construa o esqueleto completo de todas as páginas: HTML semântico, estrutura de layout com Grid e áreas nomeadas, componentes internos com Flexbox, sistema de design em variáveis, navegação funcional entre as páginas, cabeçalho fixo e rodapé consistentes em todas elas, link de salto funcionando. Entregue também um wireframe (papel fotografado, Figma ou Excalidraw) de **três larguras**: celular, tablet e desktop. Este exercício é a primeira etapa do que será avaliado na Avaliação 2.

<details><summary>Dica</summary>

Comece pelo wireframe, não pelo código: desenhe as três larguras em dez minutos e só então decida quais áreas nomeadas cada página precisa. Reaproveite `.container`, `.cabecalho`, `.menu`, `.cartoes` e `.rodape` da Mão na massa — o que muda no seu projeto é o conteúdo e as cores, não a arquitetura. Valide o HTML de cada página no W3C antes de estilizar.
</details>

## 🏆 Desafios

### ⭐ Flexbox Froggy e Grid Garden até o fim
Tags: css, flexbox, grid

Você consegue levar 24 sapos para as vitórias-régias certas usando só `justify-content`, `align-items` e `flex-wrap`? E regar 28 cenouras com `grid-column`, `grid-area` e `grid-template-areas`? Os dois jogos foram criados para fixar, por repetição, exatamente as propriedades desta aula — e muita gente que "já sabia Flexbox" descobre no nível 18 que não sabia `align-content`. Jogue os dois em português (<https://flexboxfroggy.com/#pt-br> e <https://cssgridgarden.com/#pt-br>) e anote o que travou.

**Critérios de pronto**

- Captura de tela do último nível de cada jogo concluído (nível 24 do Froggy e nível 28 do Garden).
- Um arquivo `aprendizados.md` com três propriedades ou valores que você não conhecia (ou usava errado) antes dos jogos, com uma frase explicando cada um.
- Para cada uma das três, um trecho do site do evento onde ela poderia ser aplicada.

<details><summary>Pistas</summary>

1. Se travar em um nível, abra a referência de Flexbox da MDN em pt-BR e procure a propriedade que o enunciado do nível cita — o jogo sempre diz qual é.
2. No Froggy, os níveis a partir do 19 combinam `flex-direction` com `justify-content`: lembre que o eixo principal muda de lugar.
3. No Garden, `grid-column: 2 / span 3` e `grid-column: 2 / 5` fazem a mesma coisa — os níveis finais testam se você entende as duas formas.
</details>

### ⭐⭐ Caça ao bug de layout
Tags: css, layout, bug, devtools

O código abaixo era para produzir um cabeçalho fixo com menu à direita, uma página com lateral à esquerda e conteúdo à direita, e um selo "Esgotado" no canto do cartão. Nada disso acontece: o cabeçalho rola junto com a página, a lateral cai embaixo do conteúdo, o selo aparece no canto da janela e o menu tem marcadores e espaços duplos. Há **cinco** bugs. Encontre e corrija todos usando apenas o DevTools como ferramenta de investigação — sem reescrever do zero.

**`caca-ao-bug.html`**

```html
<body>
  <header class="topo">
    <div class="topo__interno">
      <a class="logo" href="index.html">Semana</a>
      <nav aria-label="Principal">
        <ul class="menu">
          <li><a href="index.html">Início</a></li>
          <li><a href="programacao.html">Programação</a></li>
          <li><a href="contato.html">Contato</a></li>
        </ul>
      </nav>
    </div>
  </header>
  <main class="grade">
    <aside class="lateral">Filtros</aside>
    <section class="conteudo">
      <div class="cartao">
        <span class="selo">Esgotado</span>
        <h2>Minicurso de Git</h2>
        <p>Versionamento do zero ao primeiro pull request.</p>
      </div>
    </section>
  </main>
</body>
```

**`caca-ao-bug.css`**

```css
body { margin: 0; overflow-x: hidden; }
.topo { position: sticky; z-index: 10; background: #fff; }
.topo__interno { display: flex; justify-content: space-between; padding: 16px; }
.menu { display: flex; gap: 24px; }
.menu li { margin-right: 24px; }
.grade { display: grid; grid-template-columns: 240px 1fr; grid-template-areas: "lateral conteudo"; gap: 24px; }
.lateral { grid-area: sidebar; }
.conteudo { grid-area: conteudo; }
.cartao { padding: 16px; border: 1px solid #ccc; }
.selo { position: absolute; top: 8px; right: 8px; background: #b42318; color: #fff; padding: 2px 8px; }
```

**Critérios de pronto**

- O cabeçalho gruda no topo ao rolar a página.
- A lateral fica à esquerda e o conteúdo à direita, na mesma linha.
- O selo "Esgotado" fica no canto superior direito do cartão, mesmo ao rolar e redimensionar.
- O menu não tem marcadores de lista e os links têm exatamente 24 px de espaço entre si.
- Um comentário acima de cada correção explica o bug em uma linha (por que o comportamento errado acontecia).

<details><summary>Pistas</summary>

1. `sticky` precisa de duas coisas para funcionar: uma delas está faltando na regra, a outra está sendo sabotada por um ancestral — releia a seção 1.2 e o Investigue da seção 1.5.
2. No DevTools, ative o overlay da grade e "Show area names": o nome que aparece na primeira coluna é o mesmo que a `.lateral` está pedindo?
3. `absolute` procura o ancestral posicionado mais próximo. Qual é o ancestral posicionado mais próximo do selo neste código?
4. `gap` e `margin` não se anulam — se somam. E `ul` tem um estilo padrão que ninguém removeu.
</details>

### ⭐⭐ Mosaico de destaques com Grid
Tags: css, grid, layout, projeto

A página inicial do site do evento precisa de um bloco de destaques em formato de revista: sete cartões de tamanhos diferentes — um grande (2 × 2), dois largos (2 × 1), um alto (1 × 2) e três pequenos (1 × 1) — encaixados sem buracos, como um mosaico. O detalhe: quando a janela estreita e a grade perde colunas, os buracos aparecem, a menos que você conheça uma propriedade que faz o Grid "preencher para trás". Descubra qual é e construa o mosaico.

**Critérios de pronto**

- Em 1100 px, os sete cartões ocupam uma grade de quatro colunas sem nenhuma célula vazia.
- Em 700 px (duas colunas) e em 400 px (uma coluna), continua não havendo buracos e nenhum cartão pede mais colunas do que existem.
- Nenhum cartão é posicionado com números de linha fixos (`grid-column: 3 / 5`) — só com `span`.
- A ordem de leitura por teclado (<kbd>Tab</kbd> nos links dos cartões) faz sentido mesmo quando o Grid reordena visualmente.

<details><summary>Pistas</summary>

1. Procure `grid-auto-flow` na MDN e leia sobre o valor `dense`.
2. `grid-auto-rows` com um valor fixo (ou `minmax`) dá altura às linhas implícitas, para que `span 2` em linhas tenha efeito visível.
3. Na media query de duas colunas, reduza todo `span` maior que 2 para `span 2`; em uma coluna, `span 1` para todos.
4. `dense` pode mover um cartão para antes de outro que vem primeiro no HTML. Teste com <kbd>Tab</kbd> e, se a ordem ficar estranha, reordene o HTML — não o CSS.
</details>

### ⭐⭐⭐ Recriação de um layout real
Tags: css, grid, flexbox, layout, responsivo

Você consegue reproduzir a página inicial de um site que usa todo dia? Escolha a home de um site conhecido (o portal da UNEMAT, um jornal, uma loja, a página inicial do GitHub) e reproduza seu **layout** — estrutura e disposição, com conteúdo próprio e sem copiar imagens — usando Grid para a página e Flexbox para os componentes, com responsividade em três larguras. Requisito inegociável: zero `float` e zero `position: absolute` para layout (o `absolute` só pode aparecer em selos e ícones). Ao terminar, você vai perceber quanto dos sites que admira é só Grid e Flexbox bem combinados. Vale como item extra na rubrica da Avaliação 2.

**Critérios de pronto**

- Três pares de capturas lado a lado (original × sua versão) em 375 px, 768 px e 1440 px.
- O arquivo CSS tem, no topo, um comentário com o desenho das áreas nomeadas de cada largura.
- O DevTools não mostra nenhum `float` e nenhum `position: absolute` em elementos estruturais (cabeçalho, colunas, seções, rodapé).
- O menu principal é uma lista dentro de `<nav aria-label>`, com `aria-current` e link de salto.
- HTML validado sem erros no W3C.

<details><summary>Pistas</summary>

1. Antes de escrever CSS, abra o site escolhido com o DevTools e clique nos selos **grid** e **flex**: muitos sites profissionais deixam a estrutura à mostra.
2. Desenhe o `grid-template-areas` das três larguras em papel primeiro; se você não consegue desenhar, não consegue codificar.
3. Comece pela largura maior (a mais complexa) e reduza — nesta aula ainda é aceitável; na Aula 08 você vai inverter.
4. Onde o original usa uma imagem de fundo com texto por cima, use uma célula do Grid com `background-image` e um `div` com Flexbox para o texto — sem `absolute`.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `justify-content: center` centralizou na vertical em vez de na horizontal | O contêiner está em `flex-direction: column`; `justify-content` segue o eixo principal, que agora é vertical | Use `align-items` para o eixo transversal; releia a seção 2.2 sobre os eixos |
| Espaço duplo (ou irregular) entre os itens do menu | `margin` nos itens somado ao `gap` do contêiner | Remova as margens e use só `gap` |
| O cabeçalho com `position: sticky` não gruda | Falta `top: 0`, ou um ancestral tem `overflow: hidden`/`auto` (inclusive `overflow-x: hidden` no `body`) | Declare `top` e remova o `overflow` do ancestral — ou aplique o `overflow` só ao elemento que realmente precisa |
| O selo `absolute` foi parar no canto da página | Nenhum ancestral tem `position` diferente de `static` | `position: relative` no cartão que deve servir de referência |
| A lateral caiu para baixo do conteúdo em uma grade de duas colunas | O nome em `grid-area` não bate com o nome em `grid-template-areas` (letra a mais, acento, maiúscula), e o item foi posicionado automaticamente | Confira os nomes com "Show area names" no DevTools; use nomes sem acento e em minúsculas |
| Cartões com `auto-fit` ficaram encolhidos à esquerda quando há poucos itens | Usou `auto-fill`, que mantém as colunas vazias | Troque por `auto-fit`, que colapsa as faixas vazias e deixa os itens esticarem |
| A grade "estourou" e criou uma coluna extra fora do contêiner | Um item pede `grid-column: span 4` em uma grade de 3 colunas; o Grid cria colunas implícitas | Nunca peça mais colunas do que a grade tem; ajuste os `span`s em cada media query |
| O layout inteiro rola horizontalmente no celular | Um contêiner com `width: 1100px` fixo, ou uma imagem maior que a tela | `max-width` + `width: 100%` no contêiner; `img { max-width: 100%; height: auto; }` |
| `z-index: 9999` e o elemento continua atrás de outro | O elemento está dentro de um contexto de empilhamento com `z-index` menor (criado pelo pai com `position` + `z-index`, `transform` ou `opacity`) | Suba o `z-index` do ancestral que cria o contexto, ou mova o elemento para fora dele; documente a escala do projeto |
| O rodapé sobe para o meio da tela em páginas curtas | O `body` não é um contêiner flex em coluna, ou o `main` não tem `flex: 1` | `body { display: flex; flex-direction: column; min-height: 100vh; } main { flex: 1; }` |
| O menu fica com marcadores (bolinhas) | `list-style` padrão da `ul` não foi removido | `.menu { list-style: none; }` — e mantenha a lista: ela é semântica |
| A ordem do <kbd>Tab</kbd> não bate com a ordem visual | `order` (Flexbox) ou `grid-auto-flow: dense` reordenou só a apresentação | Reordene o HTML, não o CSS; use `order` apenas para pequenos ajustes decorativos |

## 🏠 Atividade assíncrona (1 h)

**Parte 1 — Leitura (20 min).** SILVA, Maurício Samy. *Criando sites com HTML*, capítulos de posicionamento e layout. MDN Web Docs em pt-BR: os guias "Conceitos básicos do Flexbox" e "Conceitos básicos do Grid Layout" (links em "Para aprofundar"). Anote uma propriedade de cada guia que não apareceu nesta aula.

**Parte 2 — Entrega (30 min).** No seu **projeto autoral**:

1. Exercícios **B1** (barra de navegação) e **B5** (dashboard), em arquivos separados na pasta `exercicios/aula-07/`.
2. O layout principal do projeto construído com Grid e áreas nomeadas em pelo menos uma página (a mais complexa), com Flexbox no interior dos componentes.
3. O menu de navegação completo em **todas** as páginas: lista semântica, `nav aria-label`, `aria-current` na página atual, `:focus-visible` em todos os links e link de salto funcionando.

**Parte 3 — Fórum (10 min).** No fórum "Flexbox ou Grid" do SIGAA: traga um componente do seu projeto (um trecho de HTML + CSS), diga qual dos dois você usou e justifique tecnicamente com base na tabela da seção 4. Comente a escolha de um colega.

**Critério de pronto:** ao pressionar <kbd>Tab</kbd> na primeira página do seu projeto, o link de salto aparece; ao pressionar <kbd>Enter</kbd>, o foco vai para o conteúdo; navegando pelo menu, cada link mostra foco visível e a página atual está marcada com `aria-current`; ao abrir a página mais curta, o rodapé está no fim da janela; ao clicar nos selos **grid**/**flex** do DevTools, a estrutura desenhada é a que você planejou.

**Entrega:** pasta `.zip` do projeto ou link do repositório no SIGAA.

## ✅ Checkpoint do projeto

Ao fim desta aula, o seu projeto autoral deve ter:

- [ ] `css/estilo.css` com as variáveis `--cor-superficie`, `--cor-borda` e `--largura-max` e a escala de `z-index` documentada em comentário.
- [ ] `body` em Flexbox de coluna com `main { flex: 1 }` — rodapé no fim da tela em todas as páginas.
- [ ] Classe `.container` com `max-width` e `margin-inline: auto` em uso em todas as páginas.
- [ ] Cabeçalho `sticky` com logo e menu alinhados por Flexbox, presente e idêntico nas cinco páginas.
- [ ] Menu como `ul` dentro de `<nav aria-label="Principal">`, com `aria-current="page"` na página atual e estados `:hover` e `:focus-visible`.
- [ ] Link de salto como primeiro elemento do `<body>` e `<main id="conteudo" tabindex="-1">`.
- [ ] Pelo menos uma grade de cartões com `repeat(auto-fit, minmax(…, 1fr))`.
- [ ] Pelo menos uma página com estrutura em Grid e áreas nomeadas.
- [ ] Nenhum `float` e nenhum `position: absolute` usado para layout.
- [ ] HTML de todas as páginas sem erros no validador do W3C.

## 📚 Para aprofundar

- MDN — **CSS Flexible Box Layout** (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Web/CSS/CSS_flexible_box_layout> — leia "Conceitos básicos do Flexbox" e "Alinhando itens em um contêiner flex"; é a referência definitiva dos eixos.
- MDN — **CSS Grid Layout** (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Web/CSS/CSS_grid_layout> — "Conceitos básicos do Grid Layout" e "Grid template areas"; guarde a página de `grid-template-areas` nos favoritos.
- MDN — **`position`** (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Web/CSS/position> — os exemplos interativos de `sticky` valem a visita.
- web.dev — **Learn CSS**: <https://web.dev/learn/css> — os módulos "Flexbox", "Grid" e "Z-index and stacking contexts" explicam o contexto de empilhamento com ilustrações.
- Flexbox Froggy (pt-BR): <https://flexboxfroggy.com/#pt-br> — 24 níveis para fixar as propriedades do contêiner e dos itens.
- Grid Garden (pt-BR): <https://cssgridgarden.com/#pt-br> — 28 níveis de `grid-column`, `grid-row` e áreas nomeadas.
- SILVA, Maurício Samy. *Criando sites com HTML: sites de alta qualidade com HTML e CSS*. Novatec, 2008 — capítulos de posicionamento e layout (contexto histórico do `float`; compare com o que você aprendeu hoje).
- TERUEL, Evandro C. *HTML 5 — Guia Prático*. Saraiva, 2014 — capítulo sobre estruturação de páginas com os elementos semânticos que o Grid organiza.

Na próxima aula, o site do evento vai para o celular de verdade: você vai reescrever a folha de estilo no modo *mobile first*, definir breakpoints onde o layout quebra (e não onde o iPhone manda), transformar o menu em um hambúrguer acessível e respeitar as preferências do usuário — tema escuro e redução de movimento.
