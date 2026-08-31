# Aula 05 — Animação e SVG

> **Nível 2 — Desenvolvimento Web** · Unidade 1: Web estática
> WebLab · UNEMAT — Campus Sinop
> **Tempo estimado:** 3 blocos de 50 min + 1 h de prática

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Explicar o que uma animação de interface comunica ao usuário e decidir, com critério, quando **não** animar.
- Escrever transições CSS completas (propriedade, duração, curva e atraso) para os estados `:hover`, `:focus-visible`, `:active` e `:disabled`, sem quebrar o retorno visual de quem navega por teclado.
- Usar `transform` (`translate`, `scale`, `rotate`) e `transform-origin` para mover, ampliar e girar elementos sem afetar o layout dos vizinhos.
- Construir animações de múltiplas etapas com `@keyframes` e controlá-las com `animation-delay`, `animation-iteration-count` e `animation-fill-mode`.
- Justificar, pelo pipeline de renderização do navegador, por que `transform` e `opacity` são as propriedades baratas — e comprovar isso no painel Performance do DevTools.
- Descrever a estrutura de um arquivo SVG (`viewBox`, formas básicas, `path`), escolher entre `<img src="…svg">` e SVG inline, e estilizar/animar um SVG inline com `fill`, `stroke` e `@keyframes`.
- Aplicar `prefers-reduced-motion` e as regras da WCAG sobre movimento, cobrindo o critério "animação/SVG" do Marco 1.

## 📋 Pré-requisitos

- [ ] Repositório `cafe-cerrado` publicado no GitHub Pages, com `index.html`, `cardapio.html` e `contato.html`.
- [ ] Bootstrap 5.3 carregado via CDN e `css/estilo.css` **depois** dele no `<head>` (Aula 04), com as variáveis de cor no `:root` (Aula 02).
- [ ] Navbar responsiva, grid de cards no cardápio e formulário de contato estilizados pelo Bootstrap (Aula 04).
- [ ] Seu projeto autoral no mesmo estágio, com a escolha do framework justificada no `README.md`.
- [ ] VS Code com Live Server e Chrome ou Firefox com DevTools — hoje você vai usar as abas **Elements**, **Rendering** e **Performance**.
- [ ] Um celular na mesma rede Wi-Fi do computador (para sentir a diferença de desempenho de verdade).

> Na aula passada o Café Cerrado ganhou aparência profissional: o Bootstrap trouxe navbar responsiva, grid de 12 colunas, cards no cardápio e um formulário consistente, e o `README.md` passou a justificar essa escolha. O site está bonito e responsivo — mas tudo nele acontece de repente: o botão troca de cor num estalo, o card não reage ao mouse, o logotipo ainda é um texto e os ícones são caracteres soltos. Hoje o site ganha **movimento** e **desenho vetorial**: microinterações que comunicam, um logotipo em SVG nítido em qualquer tela e um bloco `prefers-reduced-motion` que respeita quem prefere menos animação.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Por que animar; transições (as quatro propriedades, curvas, durações, o que anima); transformações e `transform-origin` |
| 2 | 50 min | `@keyframes` e `animation`; catálogo de animações úteis; performance (layout → paint → composite); `prefers-reduced-motion` e WCAG |
| 3 | 50 min | SVG: `viewBox`, formas, `path`, inline × `<img>`, estilo e animação, acessibilidade; Mão na massa no Café Cerrado; Laboratório |

## 1. Movimento com propósito

Animação em interface não é enfeite. Ela existe para responder a três perguntas do usuário:

| Pergunta do usuário | O que a animação responde |
|---|---|
| "O sistema recebeu meu clique?" | **Feedback** — o botão afunda e escurece no instante do toque |
| "De onde saiu isso?" | **Continuidade** — o menu desliza para fora do botão que o abriu |
| "Para onde devo olhar?" | **Atenção** — o campo com erro treme de leve e o olho vai até ele |

Se uma animação não responde a nenhuma dessas perguntas, ela é ruído. Movimento gratuito cansa, atrasa a interação (o usuário espera a animação terminar para clicar) e prejudica pessoas com sensibilidade vestibular, que sentem tontura real diante de deslocamentos grandes na tela.

A regra de ouro desta aula: **toda animação precisa responder "o que isso está dizendo ao usuário?"**. Se você não consegue responder em uma frase, apague.

> **⚠️ Atenção**
> O critério "animação/SVG" do Marco 1 é sobre **coerência**, não sobre quantidade. Três microinterações bem escolhidas valem mais que dez efeitos disputando atenção. Um site que pisca inteiro perde qualidade.

> **🧠 Você sabia?**
> Transições e animações em CSS não nasceram em um comitê: foram propostas pela Apple em 2007, dentro do WebKit, para que o Safari do primeiro iPhone conseguisse fazer interfaces fluidas sem JavaScript — o hardware da época não aguentava animar via script a 60 quadros por segundo. As propriedades saíram com prefixo `-webkit-`, os outros navegadores copiaram, e só anos depois viraram recomendação do W3C. É por isso que `transition` e `animation` parecem "feitas para telas de toque": elas foram, literalmente.

## 2. Transições

Uma **transição** interpola automaticamente a mudança de um valor entre dois estados. Você declara os dois estados (normal e `:hover`, por exemplo) e diz ao navegador: "em vez de trocar de repente, leve 200 ms para ir de um ao outro". O navegador calcula todos os valores intermediários, quadro a quadro.

**`css/estilo.css`** (exemplo isolado)

```css
.botao-exemplo {
  background-color: #3e2723;
  color: #f5efe6;
  transform: translateY(0);
  transition: background-color 200ms ease, transform 200ms ease;
}

.botao-exemplo:hover {
  background-color: #6d4c41;
  transform: translateY(-2px);
}
```

Passe o mouse: a cor muda suavemente e o botão sobe 2 px. Tire o mouse: ele desce e volta à cor original, também suavemente — porque a `transition` está declarada no estado **normal**, e vale nos dois sentidos.

### 2.1 As quatro propriedades

```css
.painel-exemplo {
  transition-property: transform, opacity;   /* o que anima */
  transition-duration: 300ms;                /* quanto tempo dura */
  transition-timing-function: ease-out;      /* a curva de velocidade */
  transition-delay: 100ms;                   /* espera antes de começar */
}

/* Atalho equivalente: propriedade duração curva atraso */
.painel-atalho {
  transition: transform 300ms ease-out 100ms, opacity 300ms ease-out 100ms;
}
```

O atalho aceita várias transições separadas por vírgula, cada uma com sua duração e curva. Na prática você usa quase sempre o atalho.

> **📌 Vale gravar**
> A `transition` deve ser declarada no **estado base** do seletor (`.botao`), nunca dentro do estado de interação (`.botao:hover`). Se ficar no `:hover`, a entrada é suave e a saída é abrupta: ao tirar o mouse a regra `:hover` deixa de valer e leva a `transition` junto.

### 2.2 Funções de tempo

A **curva** define como a velocidade varia ao longo da transição. É o que separa um movimento mecânico de um movimento natural.

| Valor | Comportamento | Uso típico |
|---|---|---|
| `linear` | Velocidade constante | Rotação contínua, barra de progresso |
| `ease` | Acelera e desacelera (padrão) | Uso geral |
| `ease-in` | Começa devagar, termina rápido | Elemento **saindo** da tela |
| `ease-out` | Começa rápido, termina devagar | Elemento **entrando** na tela |
| `cubic-bezier(0.16, 1, 0.3, 1)` | Curva personalizada, chegada macia | Painéis, cards, cartazes |
| `steps(4, end)` | Saltos discretos | Sprites, efeito de digitação |

Regra de bolso: **o que entra usa `ease-out`** (chega rápido e assenta devagar, como um carro estacionando); **o que sai usa `ease-in`** (parte devagar e some rápido). Uma transição de cor pode usar `ease` e ninguém percebe diferença.

> **🔬 Investigue**
> Abra o site do Café Cerrado, inspecione um botão (<kbd>F12</kbd> → Elements) e acrescente `transition: transform 1s ease` no painel Styles. Repare no pequeno ícone de curva que aparece ao lado do valor `ease`: clique nele. O DevTools abre um editor de `cubic-bezier` com a curva desenhada e uma bolinha que percorre a animação. Arraste os pontos de controle até criar um ricochete (o segundo ponto acima de 1) e observe o botão se mover ao vivo. Anote os quatro números da curva que você gostou — você vai usá-los no Passo 1 da Mão na massa.

### 2.3 Duração adequada

| Faixa | Percepção |
|---|---|
| 100–150 ms | Micro-interações: `:hover`, foco, troca de cor |
| 200–300 ms | Padrão para a maioria dos casos |
| 300–500 ms | Painéis, modais, elementos grandes que percorrem distância |
| acima de 500 ms | Percebido como lento e irritante |

Elementos pequenos que se movem pouco precisam de menos tempo; elementos grandes que atravessam a tela precisam de mais. Na dúvida, comece em 250 ms e ajuste olhando.

> **⚠️ Atenção**
> `transition: all` é uma armadilha. Ele anima **todas** as propriedades que mudarem, inclusive as caras (`width`, `height`, `margin`) e as que você nem sabia que mudaram. Pior: quando você acrescentar CSS meses depois, coisas passarão a animar sem explicação. Liste as propriedades sempre.

### 2.4 O que anima e o que não anima

Só propriedades com valores **numericamente interpoláveis** transicionam — o navegador precisa conseguir calcular "o valor no meio do caminho".

- **Animam:** `color`, `background-color`, `opacity`, `transform`, `box-shadow`, `border-radius`, `width`, `height`, `padding`, `margin`, `fill`, `stroke`, `stroke-dashoffset`.
- **Não animam:** `display`, `position`, `font-family`, `flex-direction`, `visibility` (tem regra especial).

Não existe meio caminho entre `display: none` e `display: block`. Por isso o bloco abaixo simplesmente não faz nada:

```css
/* Errado: display não interpola — o painel aparece de repente */
.painel-errado {
  display: none;
  transition: display 300ms;
}
```

A solução clássica combina `opacity` (que interpola) com `visibility` (que retira o elemento da navegação por teclado e do leitor de tela):

```css
/* Certo: opacity anima; visibility esconde do teclado e do leitor de tela */
.painel-certo {
  opacity: 0;
  visibility: hidden;
  transition: opacity 300ms ease, visibility 0s 300ms;
}

.painel-certo.aberto {
  opacity: 1;
  visibility: visible;
  transition: opacity 300ms ease, visibility 0s;
}
```

Repare no truque do `visibility`. Ao **esconder**, `visibility 0s 300ms` espera o fade terminar e só então vira `hidden`; sem o atraso, o painel sumiria antes de desvanecer. Ao **mostrar**, `visibility 0s` (sem atraso) torna o elemento visível na hora e o `opacity` faz a entrada.

> **🔎 Por baixo do capô**
> Por que `opacity: 0` sozinho não basta? Porque um elemento transparente **continua no fluxo e continua focável**: quem navega por <kbd>Tab</kbd> cai em links invisíveis e o leitor de tela lê o conteúdo de um painel que "não está lá". `visibility: hidden` resolve os dois problemas de uma vez. Guarde essa dupla: na Aula 06 ela vira critério de acessibilidade, e na Unidade 2 o JavaScript vai apenas alternar a classe `.aberto`.

## 3. Transformações

`transform` altera a **renderização** do elemento sem afetar o layout dos vizinhos. Um elemento com `transform: translateX(50px)` é desenhado 50 px à direita, mas para o resto da página ele continua exatamente onde estava — ninguém é empurrado, nada é recalculado. É por isso que `transform` é barato (a §5 mede isso).

```css
/* Translação: move sem tirar do fluxo */
.t1 { transform: translateX(20px); }
.t2 { transform: translateY(-10px); }
.t3 { transform: translate(20px, -10px); }

/* Escala: 1 é o tamanho original */
.t4 { transform: scale(1.05); }             /* 5% maior nos dois eixos */
.t5 { transform: scaleX(2) scaleY(0.5); }   /* estica na horizontal, achata na vertical */

/* Rotação: graus ou voltas */
.t6 { transform: rotate(45deg); }
.t7 { transform: rotate(-0.25turn); }       /* um quarto de volta, anti-horário */

/* Inclinação */
.t8 { transform: skewX(12deg); }

/* Combinadas: a ORDEM importa */
.t9  { transform: translateX(50px) rotate(45deg); }  /* move, depois gira no lugar */
.t10 { transform: rotate(45deg) translateX(50px); }  /* gira o eixo, depois anda pelo eixo girado */
```

As funções são aplicadas **da esquerda para a direita, sobre o sistema de coordenadas do elemento**. Em `.t9` o elemento desliza 50 px para a direita e então gira em torno do próprio centro. Em `.t10` ele gira primeiro — e com ele giram os eixos X e Y — e só então anda 50 px "para a direita", que agora aponta para a diagonal. Os dois terminam em lugares diferentes.

### 3.1 Ponto de origem

Toda transformação acontece em torno de um ponto. O padrão é o centro do elemento; `transform-origin` muda isso.

```css
.origem-padrao { transform-origin: center; }      /* gira/escala em torno do centro */
.origem-canto  { transform-origin: top left; }    /* gira em torno do canto superior esquerdo */
.origem-base   { transform-origin: 50% 100%; }    /* meio da borda inferior: um pêndulo */
.origem-esq    { transform-origin: left; }        /* cresce da esquerda para a direita */
```

`transform-origin: left` combinado com `scaleX` é a base do sublinhado animado do menu que você vai construir na Mão na massa: o traço nasce na esquerda ao entrar e recolhe pela direita ao sair, bastando trocar a origem nos dois estados.

### 3.2 O padrão clássico: o card que se eleva

```css
.card-exemplo {
  transition: transform 250ms ease, box-shadow 250ms ease;
}

.card-exemplo:hover,
.card-exemplo:focus-within {
  transform: translateY(-6px);
  box-shadow: 0 0.75rem 1.5rem rgba(62, 39, 35, 0.18);
}
```

`:focus-within` é o irmão de teclado do `:hover`: ele casa com o card quando **qualquer elemento dentro dele** recebe foco. Sem essa linha, quem navega por <kbd>Tab</kbd> vê o link do card ganhar foco enquanto o card em volta permanece inerte — o retorno visual some justamente para quem mais precisa dele.

## 4. Animações com `@keyframes`

Transição precisa de um gatilho (um `:hover`, uma classe trocada). Para animar **sem gatilho**, ou com mais de dois estados, use `@keyframes` + `animation`.

```css
/* 1. Definir os quadros-chave */
@keyframes surgir {
  from { opacity: 0; transform: translateY(1.5rem); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes pulsar {
  0%   { transform: scale(1); }
  50%  { transform: scale(1.06); }
  100% { transform: scale(1); }
}

/* 2. Aplicar aos elementos */
.titulo-hero { animation: surgir 400ms ease-out; }
.botao-cta   { animation: pulsar 2.4s ease-in-out 3; }   /* repete 3 vezes e para */
```

`from`/`to` são apelidos de `0%`/`100%`. Percentuais permitem quantas etapas você quiser.

### 4.1 As propriedades de `animation`

| Propriedade | O que faz |
|---|---|
| `animation-name` | Nome do `@keyframes` a executar |
| `animation-duration` | Duração de **um** ciclo |
| `animation-timing-function` | Curva de velocidade dentro do ciclo |
| `animation-delay` | Espera antes do primeiro ciclo |
| `animation-iteration-count` | Número de repetições (ou `infinite`) |
| `animation-direction` | `normal`, `reverse`, `alternate`, `alternate-reverse` |
| `animation-fill-mode` | Que quadro aplicar antes/depois da animação |

O atalho segue esta ordem: `animation: nome duração curva atraso repetições direção modo-de-preenchimento;`.

```css
.exemplo-completo {
  animation: surgir 400ms cubic-bezier(0.16, 1, 0.3, 1) 200ms 1 normal backwards;
}
```

O `animation-fill-mode` é a fonte de metade dos bugs de animação que você vai encontrar por aí:

- `none` (padrão): antes e depois da animação vale o CSS normal. O elemento **volta ao estado inicial** quando a animação acaba.
- `forwards`: o último quadro **fica**. É o que você quer em animações de entrada.
- `backwards`: o primeiro quadro vale já durante o `animation-delay`. Sem isso, um elemento com atraso fica visível, some no primeiro quadro e "pisca".
- `both`: os dois comportamentos ao mesmo tempo. É o valor seguro quando há atraso.

### 4.2 Catálogo de animações úteis

Estas cinco resolvem quase tudo o que a Unidade 1 precisa. Guarde-as no fim do `css/estilo.css`.

**`css/estilo.css`** (seção "Animações")

```css
/* Entrada: sobe e aparece */
@keyframes surgir {
  from { opacity: 0; transform: translateY(1.5rem); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Aparecer sem deslocamento (para elementos que já estão no lugar certo) */
@keyframes aparecer {
  from { opacity: 0; }
  to   { opacity: 1; }
}

/* Rotação contínua: spinners */
@keyframes girar {
  to { transform: rotate(1turn); }
}

/* Brilho passando: esqueleto de carregamento */
@keyframes brilho {
  from { background-position: -150% 0; }
  to   { background-position: 250% 0; }
}

/* Tremida curta: campo inválido */
@keyframes tremer {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-4px); }
  40%, 80% { transform: translateX(4px); }
}
```

### 4.3 Entrada escalonada

Fazer seis cards aparecerem juntos é banal; fazê-los aparecer em cascata custa três linhas. A ideia é dar a cada card um índice via variável CSS e calcular o atraso a partir dele.

**`cardapio.html`** (trecho)

```html
<div class="col-12 col-md-6 col-lg-4">
  <article class="card card-produto" style="--i: 1">
    <h3 class="h5">Espresso do Cerrado</h3>
  </article>
</div>
<div class="col-12 col-md-6 col-lg-4">
  <article class="card card-produto" style="--i: 2">
    <h3 class="h5">Coado da Casa</h3>
  </article>
</div>
```

**`css/estilo.css`**

```css
.card-produto {
  animation: surgir 400ms ease-out backwards;
  animation-delay: calc(var(--i, 0) * 80ms);
}
```

O `backwards` é obrigatório aqui: durante os 80, 160, 240 ms de espera, o card precisa já estar no primeiro quadro (invisível). Sem ele, os seis cards aparecem prontos e depois piscam um a um.

> **⚠️ Atenção**
> `var(--i, 0)` usa o **valor de reserva** `0`: se algum card esquecer o `style="--i: …"`, ele entra sem atraso em vez de quebrar o `calc()`. Sempre que ler uma variável que pode não existir, dê um valor de reserva.

## 5. Performance: as duas propriedades baratas

Para desenhar um quadro, o navegador percorre um pipeline:

| Etapa | O que faz | Custo |
|---|---|---|
| **Layout** (reflow) | Recalcula posição e tamanho de todos os elementos afetados | Alto |
| **Paint** | Pinta pixels: cores, sombras, textos, bordas | Médio |
| **Composite** | Junta as camadas já pintadas, aplicando deslocamento e opacidade | Baixo |

- Animar `width`, `height`, `top`, `left`, `margin` ou `padding` dispara **Layout → Paint → Composite** a cada quadro. Em 60 fps são 60 recálculos por segundo de toda a árvore afetada.
- Animar `background-color`, `box-shadow`, `border-radius` ou `fill` dispara **Paint → Composite**.
- Animar `transform` e `opacity` dispara **só Composite** — e o compositor roda em outra thread, muitas vezes na GPU.

Daí a regra prática: **anime `transform` e `opacity`; tudo o mais, com parcimônia**. Um `box-shadow` que muda em um botão é irrelevante; o mesmo `box-shadow` mudando em 40 cards ao mesmo tempo trava o celular de quem está vendo.

> **🔬 Investigue**
> Abra o DevTools, pressione <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>, digite "Show Rendering" e ative **Paint flashing**. Volte ao Café Cerrado e passe o mouse sobre os cards: as áreas repintadas piscam em verde. Agora troque, no painel Styles, o `transform: translateY(-6px)` do `:hover` por `margin-top: -6px` e repita. Compare quanta área verde cada versão produz. Depois ative **Frame Rendering Stats** (na mesma aba) e observe o contador de FPS enquanto rola a página com as duas versões. Anote os dois números — eles são metade da resposta do exercício B7 do Laboratório.

### 5.1 `will-change`, com moderação

`will-change: transform` avisa o navegador para promover o elemento a uma camada própria antes de a animação começar, evitando o engasgo do primeiro quadro. É uma ferramenta de último recurso: cada camada consome memória de vídeo, e dezenas de camadas deixam a página **mais** lenta.

```css
/* Use apenas no elemento que comprovadamente engasga */
.painel-lateral {
  will-change: transform;
}
```

Regra: meça primeiro no painel Performance, aplique depois, e remova se o ganho não aparecer no gráfico.

## 6. Movimento responsável

Movimento na tela não é neutro. Pessoas com distúrbios vestibulares, enxaqueca com aura ou transtornos de atenção podem sentir tontura, náusea ou perda de foco diante de deslocamentos amplos, paralaxe e animações infinitas. Os sistemas operacionais oferecem a opção "reduzir movimento", e o CSS a expõe:

**`css/estilo.css`** (última regra do arquivo)

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

Três detalhes que caem em prova:

1. **`0.01ms` e não `0`.** Uma animação com duração zero pode nunca disparar o evento `animationend`, que a Unidade 2 usa para remover elementos. Um valor mínimo mantém o evento e é imperceptível.
2. **`!important`.** O bloco precisa vencer qualquer regra escrita depois, inclusive as do Bootstrap. É a **única** exceção à regra "zero `!important`" do checkpoint da Aula 04, e ela é deliberada: aqui o objetivo é justamente atropelar tudo o que tenha ligado movimento.
3. **Reduzir não é remover.** Nada pode sumir nem parar de funcionar com o movimento desligado: o menu abre, o card muda de sombra, o formulário envia. Só o deslocamento desaparece.

O que a WCAG 2.2 exige a respeito:

| Critério | Exigência |
|---|---|
| 2.2.2 Pausar, parar, ocultar | Movimento automático com mais de 5 s precisa de controle para pausar |
| 2.3.1 Três flashes | Nada pode piscar mais de 3 vezes por segundo |
| 2.3.3 Animação a partir de interações | Animação disparada por interação deve poder ser desligada |

É por isso que o botão de destaque da Mão na massa pulsa **três vezes e para**, em vez de pulsar `infinite`: sem repetição infinita, não há o que pausar.

> **💡 Dica**
> O Bootstrap 5.3 já traz um bloco `prefers-reduced-motion` interno para as próprias animações (colapso da navbar, modais, carrossel). O bloco acima cuida do **seu** CSS. Os dois convivem sem conflito.

## 7. SVG: gráficos vetoriais na Web

SVG (*Scalable Vector Graphics*) é um formato de imagem descrito em XML — ou seja, é **código**, como o HTML. Em vez de guardar pixels, guarda instruções de desenho: "um círculo de raio 40 na posição tal, preenchido com esta cor".

| Aspecto | PNG / JPG (bitmap) | SVG (vetorial) |
|---|---|---|
| Escala | Serrilha ao ampliar | Nítido em qualquer tamanho e densidade de tela |
| Tamanho do arquivo | Cresce com a resolução | Minúsculo para ícones e logos |
| Estilizável com CSS | Não | Sim (cores, hover, animação) |
| Ideal para | Fotos | Ícones, logos, ilustrações, gráficos |

Um logotipo em PNG precisa de três arquivos (1×, 2×, 3×) para ficar nítido em telas de alta densidade. Em SVG, é um arquivo só, de poucos KB, perfeito em qualquer tela — inclusive na de 4K do laboratório e na do celular.

> **🧠 Você sabia?**
> O SVG nasceu de um empate. Em 1998 dois formatos vetoriais concorrentes foram submetidos ao W3C: o **PGML**, defendido por Adobe, IBM, Netscape e Sun, e o **VML**, defendido por Microsoft, Macromedia e Autodesk. Em vez de escolher um lado, o W3C montou um grupo de trabalho que fundiu os dois numa especificação nova — o SVG, recomendação em 2001. Só que o Internet Explorer levou uma década para suportá-lo (chegou no IE9, em 2011), e nesse intervalo o Flash dominou a web vetorial. Quando o Flash morreu, o SVG estava lá, aberto e padronizado, esperando.

### 7.1 Anatomia: o `viewBox`

```html
<svg viewBox="0 0 200 100" width="200" height="100" role="img" aria-label="Formas de exemplo">
  <rect x="10" y="10" width="80" height="80" rx="12" fill="#3e2723" />
  <circle cx="150" cy="50" r="40" fill="#d99e33" />
  <line x1="94" y1="50" x2="106" y2="50" stroke="#4e7c59" stroke-width="4" />
  <text x="50" y="55" font-size="14" text-anchor="middle" fill="#f5efe6">Café</text>
</svg>
```

`viewBox="0 0 200 100"` define o sistema de coordenadas **interno**: a origem em (0, 0), 200 unidades de largura e 100 de altura. Todas as coordenadas dos desenhos (`x`, `cy`, `r`) usam essas unidades. O navegador então estica esse retângulo até o tamanho externo (`width`/`height`, ou o tamanho que o CSS mandar), mantendo as proporções. É o segredo da nitidez infinita: as unidades internas não são pixels, são uma régua abstrata.

Na prática: **defina o `viewBox` no HTML e o tamanho no CSS**. Assim o mesmo ícone serve para 16 px e para 64 px sem editar o arquivo.

### 7.2 Formas básicas

| Elemento | Atributos principais |
|---|---|
| `<rect>` | `x`, `y`, `width`, `height`, `rx` (canto arredondado) |
| `<circle>` | `cx`, `cy`, `r` |
| `<ellipse>` | `cx`, `cy`, `rx`, `ry` |
| `<line>` | `x1`, `y1`, `x2`, `y2` |
| `<polygon>` | `points="x1,y1 x2,y2 x3,y3"` (fechado) |
| `<polyline>` | `points="…"` (aberto) |
| `<path>` | `d="…"` (qualquer forma) |
| `<g>` | agrupa e aplica atributos herdados a vários filhos |

### 7.3 O `path` e o atributo `d`

`<path>` desenha qualquer coisa. O atributo `d` é uma sequência de comandos, cada um uma letra seguida de números. Maiúscula significa coordenada **absoluta**; minúscula, **relativa** ao ponto atual.

| Comando | Significado |
|---|---|
| `M x y` | *move to* — levanta a caneta e vai até o ponto |
| `L x y` / `H x` / `V y` | *line to* — linha reta, ou só horizontal, ou só vertical |
| `C x1 y1 x2 y2 x y` | curva de Bézier cúbica com dois pontos de controle |
| `A rx ry giro arco sentido x y` | arco de elipse |
| `Z` | fecha o caminho, ligando ao ponto inicial |

Leia este `d` em voz alta e você entende a xícara do logotipo do Café Cerrado:

```html
<path d="M12 26h34v10a17 17 0 0 1-34 0z" fill="currentColor" />
```

"Vá até (12, 26); ande 34 para a direita; desça 10; faça um arco de raio 17 até 34 unidades à esquerda; feche." O resultado é um copo de fundo arredondado.

> **💡 Dica**
> Ninguém escreve `path` complexo na mão. Desenhe no Figma, Inkscape ou Illustrator e exporte como SVG; ou copie de bibliotecas de ícones. O que você **precisa** saber é ler o resultado, para trocar cores, remover atributos inúteis e entender por que um ícone não aparece.

### 7.4 Três formas de colocar SVG na página

```html
<!-- 1. Como imagem: simples, cacheável, mas o CSS da página não entra no desenho -->
<img src="img/logo.svg" alt="Café Cerrado" width="120" height="40">

<!-- 2. Inline: cada forma vira um nó do DOM, estilizável e animável com CSS -->
<svg class="logo" viewBox="0 0 64 64" aria-hidden="true" focusable="false">
  <circle cx="32" cy="32" r="28" fill="currentColor" />
</svg>

<!-- 3. Sprite: define uma vez com <symbol>, reutiliza com <use> -->
<svg class="sprite-icones" aria-hidden="true" focusable="false">
  <symbol id="icone-relogio" viewBox="0 0 24 24">
    <path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm0 2a8 8 0 1 1 0 16 8 8 0 0 1 0-16z" />
    <path d="M11 6h2v6.4l4.2 2.5-1 1.7L11 13.6z" />
  </symbol>
</svg>

<svg class="icone" aria-hidden="true" focusable="false"><use href="#icone-relogio" /></svg>
```

Quando usar cada uma:

- **`<img>`** para ilustrações grandes que não mudam de cor: o navegador guarda em cache e o HTML fica limpo.
- **Inline** para logotipos e ícones que precisam responder ao tema, ao `:hover` ou a uma animação.
- **Sprite com `<symbol>` + `<use>`** quando o mesmo ícone aparece muitas vezes na página: você paga o desenho uma vez e referencia com uma linha.

> **⚠️ Atenção**
> Em `<use href="#id">` a forma moderna é `href`; a antiga, `xlink:href`, ainda aparece em tutoriais e continua funcionando por compatibilidade, mas está obsoleta. Use `href`. E não esconda o sprite com `display: none`: alguns navegadores deixam de resolver a referência. Use `position: absolute; width: 0; height: 0; overflow: hidden`.

### 7.5 Estilizando e animando SVG inline

Dentro de um SVG inline valem seletores CSS normais, mais três propriedades específicas:

| Propriedade | Equivalente mental |
|---|---|
| `fill` | a cor do "miolo" da forma |
| `stroke` | a cor do contorno |
| `stroke-width` | a espessura do contorno |

E há uma palavra mágica: `currentColor`. Um `fill="currentColor"` faz a forma herdar a cor do texto do elemento pai — então mudar `color` no CSS muda o ícone junto, inclusive no `:hover` e no tema escuro.

```css
.icone-engrenagem {
  width: 3rem;
  color: #3e2723;
}

.icone-engrenagem path {
  fill: currentColor;
  transition: fill 300ms ease;
}

.icone-engrenagem:hover {
  color: #d99e33;
  animation: girar 2s linear infinite;
}
```

**O efeito de "desenhar o traço"** usa duas propriedades do contorno. `stroke-dasharray` transforma a linha em tracejado; se o traço tiver exatamente o comprimento total do caminho, ele vira uma linha contínua. `stroke-dashoffset` desloca esse tracejado — e um deslocamento igual ao comprimento total esconde a linha inteira. Animar o offset de "tudo" para "zero" desenha o traço.

```css
.divisor__linha {
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-dasharray: 84;     /* comprimento do caminho */
  stroke-dashoffset: 84;    /* começa totalmente escondido */
  animation: desenhar 900ms ease-out forwards;
}

@keyframes desenhar {
  to { stroke-dashoffset: 0; }
}
```

> **🔬 Investigue**
> Como descobrir o comprimento exato de um caminho? Abra o Console (<kbd>F12</kbd> → Console) na página que tem o SVG e rode `document.querySelector(".divisor__linha").getTotalLength()`. O número que aparece é o valor que você deve colocar em `stroke-dasharray` e `stroke-dashoffset`. Teste com um valor 20 % menor e observe o traço ficar incompleto; com um valor maior, o desenho começa com um atraso invisível. É a única medição desta aula que precisa do Console — na Unidade 2 você entenderá cada pedaço dessa linha.

### 7.6 Acessibilidade do SVG

Esta é a parte que mais reprova em auditoria, e é a ponte direta para a próxima aula. A pergunta é sempre a mesma: **este desenho carrega informação que não está em nenhum outro lugar?**

```html
<!-- Informativo: é a única fonte da informação -->
<svg role="img" aria-labelledby="titulo-grafico" viewBox="0 0 100 100">
  <title id="titulo-grafico">Gráfico: 70% das vendas são de café coado</title>
  <circle cx="50" cy="50" r="40" fill="#4e7c59" />
</svg>

<!-- Decorativo: o texto ao lado já diz tudo -->
<a class="navbar-brand" href="index.html">
  <svg aria-hidden="true" focusable="false" viewBox="0 0 64 64">
    <circle cx="32" cy="32" r="28" fill="currentColor" />
  </svg>
  Café Cerrado
</a>
```

Três regras:

1. **SVG informativo** recebe `role="img"` mais um nome acessível: `aria-label="…"` ou `<title>` referenciado por `aria-labelledby`. O `role="img"` é necessário porque leitores de tela antigos não tratam `<svg>` como imagem por padrão.
2. **SVG decorativo** recebe `aria-hidden="true"`. Se o texto ao lado já diz "Café Cerrado", o logotipo repetir isso só faz o leitor de tela dizer tudo duas vezes.
3. **`focusable="false"` sempre.** Sem ele, o Internet Explorer e alguns motores antigos colocam o `<svg>` na ordem de tabulação, criando paradas invisíveis no <kbd>Tab</kbd>. Custa nada e evita um erro clássico.

### 7.7 De onde tirar ícones

| Biblioteca | Combina com | Licença |
|---|---|---|
| Bootstrap Icons (`icons.getbootstrap.com`) | Bootstrap | MIT |
| Material Symbols (`fonts.google.com/icons`) | Material Design | Apache 2.0 |
| Heroicons (`heroicons.com`) | Tailwind | MIT |

Todas permitem copiar o código SVG e colar inline. **Sempre confira a licença** antes de usar em um trabalho publicado, e cite a origem no `README.md`. Ícones baixados de bancos de imagens genéricos costumam vir com termos restritivos — e um trabalho desta trilha fica público no GitHub Pages.

Antes de colar, faça uma limpeza: remova `width`/`height` fixos (o CSS cuida disso), remova `<title>` duplicados, troque `fill="#000000"` por `fill="currentColor"` e apague metadados de editor (`<metadata>`, atributos `sodipodi:*` ou `inkscape:*`). O site `svgomg.net` faz isso automaticamente e costuma cortar mais da metade do peso.

## 💻 Mão na massa — O Café Cerrado ganha vida

Ao fim destes onze passos o site terá logotipo vetorial, ícones vetoriais, microinterações em todos os elementos clicáveis, três animações com propósito e respeito à preferência de movimento reduzido. Trabalhe com o Live Server aberto e o DevTools ao lado.

### Passo 1 — variáveis de movimento

Abra o `css/estilo.css` e **acrescente** ao `:root` que já existe (Aulas 02 e 04) o bloco de movimento. As cores não mudam: `--cor-marca`, `--cor-marca-escura`, `--cor-destaque`, `--cor-fundo`, `--cor-superficie`, `--cor-texto` e `--cor-texto-suave` continuam sendo as mesmas do primeiro dia. Não crie um segundo `:root` nem renomeie cor nenhuma — a Aula 06 vai **medir** essa paleta com o Lighthouse, e ela precisa ser a que está no seu arquivo.

**`css/estilo.css`**

```css
:root {
  /* … as cores das Aulas 02 e 04 continuam aqui, intactas … */

  /* Movimento — Aula 05 */
  --duracao-rapida: 150ms;
  --duracao-media: 250ms;
  --duracao-longa: 400ms;
  --curva-entrada: cubic-bezier(0.16, 1, 0.3, 1);
  --curva-saida: cubic-bezier(0.4, 0, 1, 1);
  --elevacao: 0 0.75rem 1.5rem rgba(74, 51, 37, 0.18);   /* 74, 51, 37 = #4a3325 */
}
```

A partir daqui **nenhuma duração solta** aparece no arquivo: toda transição usa uma dessas variáveis. Quando pedirem "deixe tudo 30 % mais rápido", você muda três linhas. E, como na Aula 02, **nenhuma cor literal fora do `:root`**: todo o CSS de hoje usa `var(--cor-*)`.

### Passo 2 — microinterações nos elementos clicáveis

O Bootstrap já transiciona cor de fundo e borda nos botões; o que falta é o movimento e um foco de teclado que se veja.

**`css/estilo.css`**

```css
/* Uma transição para todos os elementos clicáveis, no estado base */
.btn,
.nav-link,
.card-produto,
.rodape a {
  transition:
    background-color var(--duracao-rapida) ease,
    color var(--duracao-rapida) ease,
    transform var(--duracao-media) var(--curva-entrada),
    box-shadow var(--duracao-media) var(--curva-entrada);
}

/* As cores do .btn-cafe já estão definidas na Aula 04, pelas variáveis
   --bs-btn-*. Aqui só acrescentamos movimento — nenhuma propriedade de cor,
   nenhuma regra concorrente. */
.btn-cafe:hover {
  transform: translateY(-2px);
  box-shadow: var(--elevacao);
}

.btn-cafe:active {
  transform: translateY(0);
  box-shadow: none;
}

.btn-cafe:disabled,
.btn-cafe.disabled {
  opacity: 0.55;
  transform: none;
  box-shadow: none;
  cursor: not-allowed;
}

/* O mesmo retorno para quem chega pelo teclado */
.btn:focus-visible,
.nav-link:focus-visible,
.rodape a:focus-visible {
  outline: 3px solid var(--cor-destaque);
  outline-offset: 3px;
}
```

Repare no `:disabled`: ele **desliga** o movimento. Um botão desabilitado que ainda sobe no hover mente ao usuário.

Repare também no que **não** está aqui: nenhuma cor de fundo, de borda ou de texto do `.btn-cafe`. Elas moram nas variáveis `--bs-btn-*` que você definiu na Aula 04, e é lá que continuam. Se você redeclarasse `background-color` aqui, teria duas regras `.btn-cafe` no mesmo arquivo brigando pelo mesmo botão — exatamente o "brigar com o framework" que a Aula 04 ensinou a evitar. Movimento é responsabilidade desta aula; cor é responsabilidade da anterior.

### Passo 3 — sublinhado animado no menu

**`css/estilo.css`**

```css
.navbar .nav-link {
  position: relative;
}

.navbar .nav-link::after {
  content: "";
  position: absolute;
  left: 0.5rem;
  right: 0.5rem;
  bottom: 0.15rem;
  height: 2px;
  background-color: var(--cor-superficie);
  transform: scaleX(0);
  transform-origin: right;
  transition: transform var(--duracao-media) var(--curva-saida);
}

.navbar .nav-link:hover::after,
.navbar .nav-link:focus-visible::after,
.navbar .nav-link[aria-current="page"]::after {
  transform: scaleX(1);
  transform-origin: left;
  transition: transform var(--duracao-media) var(--curva-entrada);
}
```

Aqui está a `transform-origin` da §3.1 em ação: no estado base a origem é `right`, então o traço **recolhe pela direita** ao sair; nos estados ativos ela é `left`, então o traço **cresce da esquerda** ao entrar. O seletor `[aria-current="page"]` reaproveita o atributo que você colocou na Aula 03 — o item da página atual fica sublinhado o tempo todo, sem classe extra.

Repare também que a `transition` aparece **duas vezes**, com curvas diferentes. Isso não contradiz a regra do callout **📌 Vale gravar**: a `transition` continua declarada no estado base (é ela que faz a saída acontecer); a segunda apenas **sobrescreve a curva** enquanto o estado ativo vale, dando `--curva-entrada` na ida e `--curva-saida` na volta. É a forma correta de ter velocidades diferentes nos dois sentidos — e é exatamente por isso que apagar a declaração do estado base quebraria a saída.

### Passo 4 — cards do cardápio que se elevam

**`css/estilo.css`**

```css
.card-produto {
  border: 0;
  border-radius: 0.75rem;
  overflow: hidden;
  background-color: var(--cor-superficie);
}

.card-produto:hover,
.card-produto:focus-within {
  transform: translateY(-6px);
  box-shadow: var(--elevacao);
}

.card-produto img {
  transition: transform var(--duracao-longa) var(--curva-entrada);
}

.card-produto:hover img,
.card-produto:focus-within img {
  transform: scale(1.06);
}
```

O `overflow: hidden` no card é o que impede a imagem ampliada de vazar pela borda arredondada. E o `:focus-within` garante que, ao chegar de <kbd>Tab</kbd> no link "Ver detalhes" dentro do card, o card inteiro reaja igual ao hover.

### Passo 5 — o logotipo em SVG inline

Substitua o texto solto da `navbar-brand` pelo logotipo desenhado: uma xícara com três fios de vapor.

**`index.html`** (e o mesmo bloco em `cardapio.html` e `contato.html`)

```html
<a class="navbar-brand d-flex align-items-center gap-2" href="index.html">
  <svg class="logo" viewBox="0 0 64 64" aria-hidden="true" focusable="false">
    <g class="logo__vapor" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round">
      <path d="M22 20c-4-4 4-8 0-12" />
      <path d="M32 18c-4-5 4-9 0-13" />
      <path d="M42 20c-4-4 4-8 0-12" />
    </g>
    <path d="M12 26h34v10a17 17 0 0 1-34 0z" fill="currentColor" />
    <path d="M46 28h4a7 7 0 0 1 0 14h-2" fill="none" stroke="currentColor" stroke-width="4" />
    <rect x="8" y="50" width="42" height="4" rx="2" fill="currentColor" />
  </svg>
  <span>Café Cerrado</span>
</a>
```

O SVG é `aria-hidden="true"` porque o `<span>` ao lado já dá o nome acessível do link. Se você optar por remover o texto e deixar só o desenho, troque para `role="img" aria-label="Café Cerrado"` — sem isso o link vira um botão sem nome, erro que o Lighthouse aponta na próxima aula.

**`css/estilo.css`**

```css
.logo {
  width: 2.25rem;
  height: 2.25rem;
  color: var(--cor-superficie);
  flex-shrink: 0;
}

.logo__vapor path {
  opacity: 0.85;
  transform-origin: bottom;
}

.navbar-brand:hover .logo__vapor path,
.navbar-brand:focus-visible .logo__vapor path {
  animation: subir-vapor 1.6s ease-in-out infinite;
}

.navbar-brand:hover .logo__vapor path:nth-child(2) { animation-delay: 200ms; }
.navbar-brand:hover .logo__vapor path:nth-child(3) { animation-delay: 400ms; }

@keyframes subir-vapor {
  0%   { opacity: 0.2; transform: translateY(4px); }
  50%  { opacity: 1;   transform: translateY(0); }
  100% { opacity: 0.2; transform: translateY(4px); }
}
```

Como o `fill` e o `stroke` são `currentColor`, basta mudar `color` no `.logo` para o logotipo inteiro trocar de cor. Guarde isso: na Aula 06 você vai precisar ajustar essa cor para passar no contraste.

### Passo 6 — sprite de ícones no cardápio

Cole o sprite logo depois da abertura do `<body>` de `cardapio.html`. Ele não desenha nada sozinho: é uma biblioteca.

**`cardapio.html`**

```html
<svg class="sprite-icones" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg">
  <symbol id="icone-grao" viewBox="0 0 24 24">
    <path d="M12 2.5c4 0 7.5 4.3 7.5 9.5s-3.5 9.5-7.5 9.5-7.5-4.3-7.5-9.5 3.5-9.5 7.5-9.5z" />
    <path d="M12 2.5c-2.6 3.6-2.6 15.4 0 19" fill="none" stroke="#ffffff" stroke-width="1.6" stroke-opacity="0.5" />
  </symbol>
  <symbol id="icone-folha" viewBox="0 0 24 24">
    <path d="M20 4C10 4 4 9 4 16c0 1.6.4 3 1.1 4.3l1.6-1.6C6.2 17.8 6 16.9 6 16c0-5.5 5-9.4 12.5-9.9C18 13 13.4 18 7.4 18.6l-2 2C15.6 21.6 21 15 20 4z" />
  </symbol>
  <symbol id="icone-relogio" viewBox="0 0 24 24">
    <path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm0 2a8 8 0 1 1 0 16 8 8 0 0 1 0-16z" />
    <path d="M11 6h2v6.4l4.2 2.5-1 1.7L11 13.6z" />
  </symbol>
  <symbol id="icone-chama" viewBox="0 0 24 24">
    <path d="M12 2c.5 3.5-1.5 5-3.2 6.7C7 10.5 6 12.2 6 14.3 6 18 8.7 21 12 21s6-3 6-6.7c0-2.6-1.4-4.3-2.8-6-1-1.2-1.8-2.4-1.9-3.9-.6.9-1.4 1.7-2.3 2.5.4-1.6.5-3.3 1-4.9z" />
  </symbol>
</svg>
```

Agora use os ícones dentro de cada card:

**`cardapio.html`** (trecho de um card)

```html
<article class="card card-produto h-100" style="--i: 1">
  <img src="img/espresso.jpg" class="card-img-top" alt="Xícara de espresso sobre a mesa de madeira">
  <div class="card-body">
    <h3 class="h5 card-title">Espresso do Cerrado</h3>
    <p class="card-text">Grãos de Alto Paraíso, torra média, corpo encorpado e final achocolatado.</p>
    <ul class="list-unstyled small mb-0">
      <li>
        <svg class="icone" aria-hidden="true" focusable="false"><use href="#icone-grao" /></svg>
        Torra média
      </li>
      <li>
        <svg class="icone" aria-hidden="true" focusable="false"><use href="#icone-relogio" /></svg>
        Pronto em 2 min
      </li>
      <li>
        <svg class="icone" aria-hidden="true" focusable="false"><use href="#icone-chama" /></svg>
        Servido quente
      </li>
    </ul>
  </div>
</article>
```

**`css/estilo.css`**

```css
/* O sprite existe para ser referenciado, nunca para ser visto */
.sprite-icones {
  position: absolute;
  width: 0;
  height: 0;
  overflow: hidden;
}

.icone {
  width: 1.1rem;
  height: 1.1rem;
  fill: currentColor;
  vertical-align: -0.15em;
  margin-right: 0.35rem;
  color: var(--cor-destaque);
  transition: transform var(--duracao-rapida) ease, color var(--duracao-rapida) ease;
}

.card-produto:hover .icone {
  color: var(--cor-marca);
  transform: scale(1.15);
}
```

Os ícones são decorativos: o texto ao lado ("Torra média") já carrega a informação. Por isso `aria-hidden="true"` em todos.

### Passo 7 — entrada escalonada dos cards

**`css/estilo.css`**

```css
.card-produto {
  animation: surgir var(--duracao-longa) var(--curva-entrada) backwards;
  animation-delay: calc(var(--i, 0) * 80ms);
}

@keyframes surgir {
  from { opacity: 0; transform: translateY(1.5rem); }
  to   { opacity: 1; transform: translateY(0); }
}
```

Numere os cards no HTML com `style="--i: 1"`, `style="--i: 2"` e assim por diante. Com seis produtos, o último entra 400 ms depois do primeiro — perceptível, mas não irritante. Acima de dez cards, reduza para 40 ms ou o usuário espera demais.

> **🔎 Por baixo do capô**
> A animação de entrada e o `:hover` do Passo 4 disputam a mesma propriedade `transform`. Enquanto a animação está em execução ela vence — passar o mouse sobre um card nos primeiros 400 ms não eleva nada. Depois que ela termina, o `animation-fill-mode: backwards` deixa de valer para o estado final e o CSS normal volta a mandar, então o hover funciona. Foi por isso que este passo usou `backwards` e não `forwards`: com `forwards`, o último quadro da animação ficaria "grudado" no elemento e o `:hover` nunca mais moveria o card. Quando você precisar de entrada **e** hover no mesmo elemento, ou usa `backwards`, ou anima um filho em vez do próprio card.

### Passo 8 — hero com entrada e botão que chama atenção

**`index.html`** (trecho do hero)

```html
<section class="hero text-center py-5">
  <div class="container">
    <h1 class="hero__titulo display-4">Café do Cerrado, torrado em Sinop</h1>
    <p class="hero__texto lead">
      Grãos de produtores de Mato Grosso, torra artesanal e um lugar para ficar.
    </p>
    <div class="hero__acoes">
      <a class="btn btn-cafe btn-lg btn-destaque" href="cardapio.html">Ver o cardápio</a>
    </div>
  </div>
</section>
```

O `<div class="container">` é o mesmo da Aula 04 — ele fica: só a classe `btn-destaque` é novidade. Animar os filhos do container, e não o container, evita que a entrada disputa espaço com o alinhamento.

**`css/estilo.css`**

```css
.hero__titulo,
.hero__texto,
.hero__acoes {
  animation: surgir var(--duracao-longa) var(--curva-entrada) backwards;
}

.hero__titulo { animation-delay: 80ms; }
.hero__texto  { animation-delay: 200ms; }
.hero__acoes  { animation-delay: 320ms; }

/* Pulsa três vezes depois de 1,5 s e para: sem movimento infinito, sem botão de pausa */
.btn-destaque {
  animation: pulsar 2.4s ease-in-out 1.5s 3 both;
}

@keyframes pulsar {
  0%, 100% { transform: scale(1);    box-shadow: 0 0 0 0 rgba(217, 158, 51, 0.55); }
  50%      { transform: scale(1.04); box-shadow: 0 0 0 0.9rem rgba(217, 158, 51, 0); }
}
```

O `both` combina `backwards` e `forwards`: durante 1,5 s de espera o botão fica no primeiro quadro (tamanho normal), e ao fim ele permanece no último. Sem isso, o botão dá um salto no início e outro no fim.

### Passo 9 — spinner no botão do formulário

Ainda não há JavaScript no projeto, mas o CSS do estado de envio pode ficar pronto agora — e você testa trocando o atributo à mão no DevTools.

**`contato.html`** (botão do formulário)

```html
<button class="btn btn-cafe btn-enviar" type="submit" data-estado="pronto">Enviar mensagem</button>
```

**`css/estilo.css`**

```css
.btn-enviar[data-estado="enviando"] {
  position: relative;
  color: transparent;
  pointer-events: none;
}

.btn-enviar[data-estado="enviando"]::after {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 1.25rem;
  height: 1.25rem;
  margin: -0.625rem 0 0 -0.625rem;
  border: 2px solid var(--cor-superficie);
  border-top-color: transparent;
  border-radius: 50%;
  animation: girar 700ms linear infinite;
}

@keyframes girar {
  to { transform: rotate(1turn); }
}
```

Para ver funcionando: inspecione o botão, troque `data-estado="pronto"` por `data-estado="enviando"` no painel Elements e observe. Na Unidade 2 esse atributo passa a ser trocado por JavaScript no envio do formulário, e o `aria-live` da Aula 06 anunciará o resultado.

### Passo 10 — divisor SVG que se desenha

Um separador entre as seções da página inicial, com o traço nascendo do centro.

**`index.html`** (entre duas seções)

```html
<svg class="divisor" viewBox="0 0 240 24" aria-hidden="true" focusable="false">
  <path class="divisor__linha" d="M88 12H4" />
  <path class="divisor__grao" d="M120 3c3.4 0 6.2 4 6.2 9s-2.8 9-6.2 9-6.2-4-6.2-9 2.8-9 6.2-9z" />
  <path class="divisor__linha" d="M152 12h84" />
</svg>
```

Os dois traços têm o mesmo comprimento, mas direções opostas: o da esquerda começa em (88, 12) e anda **para trás** até (4, 12); o da direita começa em (152, 12) e anda para a frente. Como o desenho do traço sempre segue o sentido do caminho, os dois nascem no centro e crescem para fora — simetria de graça, sem uma linha de CSS a mais.

**`css/estilo.css`**

```css
.divisor {
  display: block;
  width: min(15rem, 60%);
  height: auto;
  margin: 2.5rem auto;
  color: var(--cor-marca);
}

.divisor__linha {
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-dasharray: 84;
  stroke-dashoffset: 84;
  animation: desenhar 900ms var(--curva-entrada) forwards;
}

.divisor__grao {
  fill: currentColor;
  opacity: 0;
  animation: aparecer var(--duracao-media) ease-out 700ms forwards;
}

@keyframes desenhar {
  to { stroke-dashoffset: 0; }
}

@keyframes aparecer {
  from { opacity: 0; }
  to   { opacity: 1; }
}
```

Os dois caminhos horizontais medem 84 unidades cada — por isso `stroke-dasharray: 84`. Confirme com `getTotalLength()` no Console, como no 🔬 Investigue da §7.5, antes de reaproveitar isso com outro desenho.

### Passo 11 — respeitar a preferência de movimento

Cole este bloco como **última regra** do `css/estilo.css`.

**`css/estilo.css`** (fim do arquivo)

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

Para testar sem mexer no sistema operacional: DevTools → <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> → "Show Rendering" → em *Emulate CSS media feature prefers-reduced-motion*, escolha `reduce`. Recarregue. Tudo deve continuar visível, legível e funcional — só sem movimento.

### Como testar

- **Botões:** passe o mouse e depois navegue só por <kbd>Tab</kbd>. Todo botão sobe no hover, afunda no clique e mostra o anel de foco na cor de destaque ao chegar por teclado. Um botão `disabled` não reage.
- **Menu:** o sublinhado cresce da esquerda ao entrar e recolhe pela direita ao sair; o item da página atual fica sublinhado permanentemente, sem mouse nenhum.
- **Cards:** recarregue `cardapio.html` — os cards entram em cascata, de 80 em 80 ms. No hover, o card sobe, a foto amplia sem vazar da borda e os ícones mudam de cor. Chegando por <kbd>Tab</kbd> ao link interno, o card reage igual.
- **Logotipo:** passe o mouse na marca da navbar — os três fios de vapor sobem em sequência. O leitor de tela não anuncia "Café Cerrado" duas vezes (confira na aba Elements que o `<svg>` tem `aria-hidden="true"`).
- **Ícones:** no painel Elements, confirme que cada `<use href="#icone-…">` resolve; um ícone invisível quase sempre é `id` digitado errado ou sprite depois do uso.
- **Hero:** ao carregar a página inicial, título, texto e botão entram em sequência; 1,5 s depois o botão pulsa três vezes e para de vez.
- **Spinner:** troque `data-estado` para `enviando` no DevTools e veja o círculo girar no lugar do texto.
- **Divisor:** recarregue e observe as duas linhas se desenhando do centro para fora, com o grão surgindo no meio ao final.
- **Movimento reduzido:** com `prefers-reduced-motion: reduce` emulado, nada some, nada trava, nada se move.
- **Desempenho:** com Paint flashing ligado, o hover dos cards deve pintar pouca área. No painel Performance com CPU 4×, a rolagem mantém a taxa de quadros estável.

**Resultado esperado:** o Café Cerrado continua com a mesma estrutura e o mesmo layout Bootstrap, mas agora responde ao usuário: cada elemento clicável tem retorno visual (mouse e teclado), o cardápio chega em cascata, a marca é vetorial e nítida em qualquer tela, os ícones acompanham a cor do tema e ninguém que prefira menos movimento é prejudicado. Faça o commit com a mensagem `Aula 05: animacoes, microinteracoes e SVG` e o push para o GitHub Pages.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Qual a diferença entre `transition` e `animation`? Dê um exemplo em que só a segunda serve.

**A2.** Escreva, na forma abreviada, uma transição de `transform` e `box-shadow` com 250 ms e curva `ease-out`.

**A3.** Cite dois motivos concretos para nunca usar `transition: all`.

**A4.** Em qual seletor a `transition` deve ser declarada: `.btn` ou `.btn:hover`? Explique o que acontece se você errar.

**A5.** Diferencie `ease-in` de `ease-out` e diga qual usar para um painel que **entra** na tela.

**A6.** Qual a diferença de resultado entre `transform: translateX(40px) rotate(90deg)` e `transform: rotate(90deg) translateX(40px)`? Desenhe as duas no papel.

**A7.** O que faz `transform-origin: left` combinado com `scaleX(0)` → `scaleX(1)`? Em que passo da Mão na massa isso apareceu?

**A8.** Escreva um `@keyframes` chamado `deslizar-direita` que leve o elemento de `translateX(-100%)` e opacidade 0 até `translateX(0)` e opacidade 1.

**A9.** Explique `animation-fill-mode` nos quatro valores. Qual usar em uma entrada com `animation-delay`?

**A10.** Por que `transform` e `opacity` são as propriedades mais baratas de animar? Cite as etapas do pipeline que cada grupo dispara.

**A11.** Reescreva de forma performática: `.painel { left: -300px; transition: left 300ms; }` e `.painel.aberto { left: 0; }`.

**A12.** Escreva o bloco `prefers-reduced-motion` completo e explique por que ele usa `0.01ms` em vez de `0` e por que usa `!important`.

**A13.** O que significa `viewBox="0 0 200 100"`? O que muda se você trocar por `viewBox="0 0 100 50"` mantendo os desenhos?

**A14.** Quando usar `<img src="logo.svg">` e quando usar SVG inline? Dê um caso de cada.

**A15.** Qual a diferença entre `fill` e `stroke`? O que `currentColor` resolve?

**A16.** Um `<svg>` mostra um gráfico com dados que não aparecem em nenhum texto da página. Quais atributos ele precisa? E se fosse um ícone ao lado da palavra "Telefone"?

**A17.** Por que todo `<svg>` desta aula tem `focusable="false"`?

**A18.** O que fazem `stroke-dasharray` e `stroke-dashoffset` juntos? Como descobrir o valor correto para um caminho qualquer?

### Nível B — Aplicação

**B1.** Construa um botão com os cinco estados animados: normal, `:hover` (elevação), `:active` (pressionado), `:disabled` (opaco e sem movimento) e `:focus-visible` (anel de foco). Nenhum estado pode ser distinguível **apenas** pela cor.

**Resultado esperado:** o botão sobe no hover, afunda no clique, mostra o anel de foco na cor de destaque ao chegar por <kbd>Tab</kbd> e, desabilitado, fica opaco com cursor `not-allowed` — e os cinco estados continuam distinguíveis numa captura de tela em preto e branco.

<details><summary>Dica</summary>

Declare a `transition` no estado base. No `:disabled`, zere `transform` e `box-shadow` e use `cursor: not-allowed`. Para o anel, `outline: 3px solid` com `outline-offset` é mais simples que `box-shadow` e não some em modo de alto contraste.
</details>

**B2.** Faça os cards do cardápio reagirem em três camadas ao mesmo tempo: o card sobe, a imagem amplia dentro da moldura e um selo ("Novidade") desliza de cima para baixo. Tudo reversível e replicado em `:focus-within`.

**Resultado esperado:** ao passar o mouse ou focar o link interno, o card sobe 6 px, a foto cresce 6 % sem vazar da borda arredondada e o selo entra pelo topo em 250 ms; ao sair, tudo volta na mesma velocidade.

<details><summary>Dica</summary>

Moldura com `position: relative; overflow: hidden`. O selo é `position: absolute; top: 0; transform: translateY(-100%)` no estado base e `translateY(0)` no hover. Anime só `transform` nos três elementos.
</details>

**B3.** Refaça o menu do seu projeto autoral com o sublinhado animado do Passo 3, incluindo o estado permanente do item atual via `[aria-current="page"]` e o retorno por teclado via `:focus-visible`.

**Resultado esperado:** em cada uma das três páginas, o item correspondente já aparece sublinhado ao carregar; os demais sublinham ao passar o mouse ou ao receber foco; a saída recolhe pelo lado oposto da entrada.

<details><summary>Dica</summary>

O `::after` precisa de `content: ""` e `position: absolute` dentro de um `.nav-link` com `position: relative`. Troque `transform-origin` entre `right` (base) e `left` (ativo) para o efeito de "vem da esquerda, some pela direita".
</details>

**B4.** Desenhe do zero, à mão, um ícone SVG 24×24 relacionado ao **seu** projeto autoral, usando pelo menos três formas diferentes (`rect`, `circle`, `path`, `polygon` ou `line`). Publique-o como `<symbol>` no sprite e use-o em dois lugares da página.

**Resultado esperado:** o ícone é reconhecível em 20 px e em 100 px, herda a cor do texto via `currentColor` e aparece duas vezes na página a partir de uma única definição.

<details><summary>Dica</summary>

Comece pelo `viewBox="0 0 24 24"` e desenhe em papel quadriculado numerando de 0 a 24 — as coordenadas saem prontas. Use `fill="currentColor"` e nada de `width`/`height` dentro do `<symbol>`: quem define tamanho é o CSS da classe `.icone`.
</details>

**B5.** Crie um esqueleto de carregamento (*skeleton*) para três cards do cardápio: retângulos cinza com um brilho passando, que dão lugar ao conteúdo real quando a classe `.carregado` é adicionada ao contêiner (adicione-a à mão no DevTools).

**Resultado esperado:** três blocos cinza "brilham" continuamente; ao acrescentar `.carregado` no contêiner pelo painel Elements, os esqueletos desvanecem e os cards reais surgem com a animação `surgir`.

<details><summary>Dica</summary>

O brilho é um `background: linear-gradient(90deg, #e9e2d9 25%, #f7f3ee 50%, #e9e2d9 75%)` com `background-size: 200% 100%` animado pela keyframe `brilho` da §4.2. A troca usa a dupla `opacity` + `visibility` da §2.4 — não use `display: none`.
</details>

**B6.** Implemente o efeito de "desenhar o traço" na assinatura do rodapé: escreva o nome do café em `<path>` (ou use um traço decorativo) e faça-o se desenhar em 1,2 s ao carregar a página, permanecendo depois.

**Resultado esperado:** o traço aparece progressivamente da esquerda para a direita e fica visível ao final; com `prefers-reduced-motion: reduce`, ele já aparece completo, sem animação.

<details><summary>Dica</summary>

Meça o caminho com `getTotalLength()` no Console e use o número em `stroke-dasharray` e `stroke-dashoffset`. `animation-fill-mode: forwards` mantém o traço desenhado. O bloco `prefers-reduced-motion` do Passo 11 já cuida do resto, porque com duração de 0,01 ms o traço chega instantaneamente ao offset zero.
</details>

**B7.** Compare medindo: crie duas versões de um mesmo painel lateral, uma animando `left` e outra animando `transform: translateX`. Grave as duas no painel Performance com CPU 4× e registre a diferença.

**Resultado esperado:** uma tabela de duas linhas no `README.md` com o tempo total gasto em Layout, Paint e Composite em cada versão, e uma frase explicando por que os números são o que são.

<details><summary>Dica</summary>

No painel Performance, use o botão de gravar, dispare a animação, pare e olhe o resumo por cores (roxo é Layout, verde é Paint, cinza-claro é Composite). Grave cada versão separadamente e com a mesma duração de gravação, senão os números não são comparáveis.
</details>

### Nível C — Desafio

**C1.** **Cartaz animado do Café Cerrado.** Construa, em um arquivo novo `promocao.html`, um cartaz de página inteira para a promoção "Hora do café — 15 h às 17 h", com: fundo em gradiente que se desloca lentamente; título entrando escalonado letra a letra ou palavra a palavra; um relógio em SVG desenhado por você, com o ponteiro girando uma volta completa em 6 s; três cards de produto entrando em cascata; e um botão de chamada que pulsa três vezes e para. Requisitos técnicos: nenhuma animação de propriedade de layout; toda animação com propósito declarado em comentário; `prefers-reduced-motion` respeitado; o cartaz continua legível e navegável por teclado com o movimento desligado. Comece pelo relógio e pelo título; o resto pode ser terminado depois.

<details><summary>Dica</summary>

O gradiente animado é `background: linear-gradient(135deg, …)` com `background-size: 200% 200%` e uma keyframe deslocando `background-position` — é um único elemento grande, o custo de Paint é aceitável. O ponteiro do relógio é um `<line>` com `transform-origin` no centro do mostrador (cuidado: em SVG a origem padrão é o canto do `viewBox`, então declare `transform-origin: 50% 50%` no CSS). Para as palavras do título, envolva cada uma em um `<span>` com `style="--i: 1"` e reaproveite o `calc()` do Passo 7.
</details>

**C2.** **Auditoria de movimento em um site real.** Escolha um site comercial brasileiro que você usa (banco, loja, prefeitura). Liste cinco animações que ele faz, dizendo para cada uma: o que ela comunica, qual propriedade provavelmente está sendo animada (verifique no DevTools) e se ela sobrevive a `prefers-reduced-motion: reduce` emulado. Conclua com uma recomendação técnica de melhoria.

<details><summary>Dica</summary>

Na aba Elements, selecione o elemento animado e olhe o painel Computed com o filtro "transition" ou "animation". A aba Rendering emula a preferência de movimento reduzido; recarregue depois de emular, porque muitos sites só leem a preferência no carregamento.
</details>

## 🏆 Desafios

### ⭐ Caça ao bug: cinco animações que não animam

Tags: css, animacao, bug, devtools

Um colega mandou o CSS abaixo dizendo "não anima nada, o navegador deve estar bugado". Não está: o navegador está fazendo exatamente o que foi pedido. Há **cinco** erros conceituais, cada um de um tipo diferente visto hoje. Encontre e corrija todos sem reescrever do zero — a intenção do colega tem que sobreviver.

```css
.botao {
  background: #3e2723;
  color: #f5efe6;
}
.botao:hover {
  background: #6d4c41;
  transform: translateY(-3px);
  transition: all 200ms ease;
}

.painel {
  display: none;
  transition: opacity 300ms ease;
}
.painel.aberto {
  display: block;
  opacity: 1;
}

@keyframes entrar {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
.card {
  animation: entrar 400ms ease-out 300ms;
}

.icone {
  fill: #3e2723;
  transition: fill 3s linear;
}
.icone:hover {
  fill: #d99e33;
}

.alerta {
  animation: piscar 200ms linear infinite;
}
@keyframes piscar {
  50% { opacity: 0; }
}
```

**Critérios de pronto**

- O botão entra **e sai** do hover suavemente, e a transição lista só as propriedades que realmente mudam.
- O `.painel` desvanece ao abrir e ao fechar, e enquanto fechado não recebe foco por <kbd>Tab</kbd>.
- O `.card` permanece invisível durante os 300 ms de atraso e visível depois que a animação termina.
- O `.icone` troca de cor numa duração compatível com uma micro-interação, justificada pela tabela da §2.3.
- O `.alerta` deixa de violar o critério 2.3.1 da WCAG, sem perder a função de chamar atenção.
- Um comentário de uma linha acima de cada correção diz qual era o erro.

<details><summary>Pistas</summary>

1. Releia o callout **📌 Vale gravar** da §2: em qual seletor a `transition` precisa estar declarada?
2. A §2.4 explica por que uma propriedade específica nunca interpola e qual é a dupla que resolve.
3. A §4.1 lista quatro valores de `animation-fill-mode`; dois deles resolvem o problema do card, e só um resolve os dois lados.
4. Compare a duração da transição do `.icone` com a faixa recomendada para micro-interações na §2.3.
5. Conte quantas vezes por segundo o `.alerta` pisca e compare com a tabela de critérios da §6.
</details>

**Para ir além:** depois de corrigir, ligue o Paint flashing e confirme que nenhuma das cinco correções aumentou a área repintada.

### ⭐ O logotipo do seu projeto em menos de 2 KB

Tags: svg, css, projeto, acessibilidade

Todo projeto autoral desta trilha precisa de uma marca. É tentador baixar um PNG genérico de 80 KB que fica borrado na tela do celular. Você vai desenhar a sua — no código, com formas geométricas — e ela vai pesar menos que uma linha de texto desta apostila.

**Critérios de pronto**

- O logotipo é um `<svg>` inline com `viewBox`, composto de pelo menos quatro formas (`rect`, `circle`, `ellipse`, `polygon`, `line` ou `path`), sem nenhuma imagem bitmap.
- O arquivo `.svg` correspondente (salvo em `img/`) tem menos de 2 KB.
- Todas as cores usam `currentColor` ou variáveis do `:root`, e trocar `color` no CSS muda a marca inteira.
- A marca aparece nítida em 24 px (favicon do navegador) e em 200 px (rodapé), sem editar o código.
- Está no cabeçalho das três páginas, com a decisão de acessibilidade explicada em comentário: `aria-hidden="true"` se houver texto ao lado, `role="img"` com nome acessível se estiver sozinha.
- Uma microinteração no `:hover` ou `:focus-visible` (troca de `fill`, rotação de uma parte, traço que se desenha).

<details><summary>Pistas</summary>

1. Comece pelo `viewBox="0 0 64 64"` e esboce no papel quadriculado: cada quadradinho é uma unidade, e as coordenadas saem prontas.
2. Formas simples combinadas superam desenhos elaborados: dois círculos e um retângulo já formam uma xícara, uma folha ou um pino de mapa.
3. Para o favicon, `<link rel="icon" href="img/logo.svg">` funciona em todos os navegadores modernos e dispensa gerar `.ico`.
4. Antes de commitar, passe o arquivo pelo `svgomg.net` e compare os bytes antes e depois — anote os dois números no `README.md`.
</details>

### ⭐⭐ Do bitmap ao vetor: meça, não acredite

Tags: svg, performance, devtools, investigacao

"SVG é mais leve" é uma frase que todo mundo repete e quase ninguém mediu. Você vai medir — e vai descobrir que a frase tem exceções importantes. O objetivo não é provar que SVG ganha: é aprender a decidir com números.

**Critérios de pronto**

- Uma tabela no `README.md` compara, para **três** conteúdos diferentes (um ícone simples, um logotipo com texto e uma fotografia), quatro colunas no máximo: conteúdo, peso em PNG, peso em SVG e vencedor.
- Cada peso foi medido na aba **Network** do DevTools (coluna *Size*, com cache desativado), não estimado.
- Um parágrafo explica por que a fotografia inverte o resultado, citando o que cada formato armazena.
- Um segundo parágrafo mede o efeito da compressão do servidor: compare o `Size` (transferido) com o `Content` (descompactado) do SVG na aba Network e explique a diferença.
- O ícone testado foi otimizado com `svgomg.net`, e o `README.md` registra o peso antes e depois da otimização.

<details><summary>Pistas</summary>

1. Na aba Network, marque *Disable cache* e recarregue com <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>R</kbd>, senão você mede zero byte.
2. Para gerar o PNG do mesmo ícone em três densidades (1×, 2×, 3×), qualquer editor serve; some os três pesos, porque é isso que um site responsivo precisaria entregar.
3. SVG é texto: servidores comprimem texto com gzip ou brotli antes de enviar. O GitHub Pages faz isso automaticamente — daí a diferença entre as colunas `Size` e `Content`.
4. Uma fotografia em SVG só cabe se o pixel virar uma forma; pense em quantas formas tem uma foto de 12 megapixels.

</details>

**Para ir além:** repita a medição com o *throttling* de rede em "Slow 4G" e registre o tempo até a imagem aparecer, não só o peso.

### ⭐⭐⭐ Um gráfico SVG do Café Cerrado, desenhado à mão

Tags: svg, animacao, acessibilidade, css

A página inicial do Café Cerrado vai ganhar uma seção "O café em números" com três indicadores. A tentação é usar uma biblioteca de gráficos com 90 KB de JavaScript. Você não pode: a Unidade 1 é sem JavaScript. Vai desenhar o gráfico em SVG puro, animá-lo com CSS e — a parte difícil — torná-lo compreensível para quem não vê a tela.

**Critérios de pronto**

- Um gráfico de barras **ou** um anel de progresso (donut) desenhado em SVG, com pelo menos três séries de dados reais do projeto.
- As barras (ou o anel) crescem do zero ao valor final ao carregar a página, usando `transform: scaleY` com `transform-origin` correto, ou `stroke-dasharray`/`stroke-dashoffset`.
- Cada valor aparece também como texto legível dentro ou ao lado do gráfico — nada de informação existir só na forma.
- O `<svg>` tem `role="img"` e um nome acessível que resume o gráfico em uma frase com os números ("Vendas por categoria: café coado 52%, espresso 31%, doces 17%").
- Uma tabela HTML equivalente existe na página, visualmente discreta mas presente no DOM (não escondida com `display: none`), com os mesmos números.
- Nenhuma cor é a única portadora de significado: cada série tem também rótulo textual.
- Com `prefers-reduced-motion: reduce`, o gráfico aparece completo e correto, sem crescer.
- Uma seção no `README.md` explica a escolha de escala: qual valor corresponde a 100 % da altura e por quê.

<details><summary>Pistas</summary>

1. Barras são `<rect>` com `height` fixo no `viewBox` e `transform: scaleY(var(--valor))` com `transform-origin: bottom` — anime a escala, nunca a altura.
2. Para o donut, um `<circle>` com `fill: none`, `stroke-width` grosso e `stroke-dasharray` igual à circunferência (2 × π × raio) transforma o offset em porcentagem direta.
3. A tabela equivalente pode ficar dentro de um `<details>` com `<summary>Ver os dados em tabela</summary>` — visível para quem quiser, presente para o leitor de tela, e sem `display: none`.
4. Escolha a escala pelo maior valor, não pela soma: um gráfico em que a maior barra ocupa 40 % da altura desperdiça o espaço e engana o olho.
5. Teste o nome acessível na aba Elements → painel **Accessibility** → campo *Computed name*, antes de considerar pronto.

</details>

**Para ir além:** meça o contraste entre cada cor de série e o fundo (WebAIM Contrast Checker) e ajuste a paleta até todas passarem em 3:1 — é exatamente o que a próxima aula vai cobrar do site inteiro.

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| O hover entra suave, mas ao tirar o mouse o elemento "pula" de volta | `transition` declarada dentro de `:hover`; ao sair, a regra deixa de valer | Declare a `transition` no estado base (`.btn`), nunca no `:hover` |
| Depois de acrescentar uma regra nova, coisas que não deviam animar passaram a animar | `transition: all` anima qualquer propriedade que mude | Liste as propriedades: `transition: transform 250ms, box-shadow 250ms` |
| A animação roda lisa no notebook e engasga no celular; o Performance mostra barras roxas a cada quadro | Animação de `width`, `height`, `left`, `top` ou `margin` dispara Layout | Reescreva com `transform`; confirme no painel Performance com CPU 4× |
| O elemento aparece com a animação e, ao terminar, **some** ou volta ao estado inicial | `animation-fill-mode: none` (padrão) descarta o último quadro | Use `forwards` (ou `both` quando houver `animation-delay`) |
| Os cards escalonados aparecem todos prontos e depois piscam um a um | `animation-delay` sem `backwards`: durante a espera vale o CSS normal | Acrescente `backwards` (ou `both`) ao atalho `animation` |
| `transition: display 300ms` não faz nada; o painel aparece de repente | `display` não é interpolável | Use `opacity` + `visibility` com `visibility 0s 300ms` na saída (§2.4) |
| Quem navega por <kbd>Tab</kbd> não vê nenhum retorno visual nos cards | Efeito declarado só em `:hover`, sem `:focus-within` | Replique cada `:hover` de container em `:focus-within` e cada `:hover` de controle em `:focus-visible` |
| O ícone do sprite não aparece; o `<use>` está no DOM mas não desenha nada | `id` do `<symbol>` diferente do `href`, sprite colado **depois** do uso, ou sprite com `display: none` | Confira o `id`, mova o sprite para logo após `<body>` e esconda-o com `position: absolute; width: 0; height: 0; overflow: hidden` |
| O SVG inline aparece gigante, ocupando a tela inteira | `<svg>` sem `width`/`height` no CSS e sem `viewBox` para calcular a proporção | Declare o `viewBox` no HTML e o tamanho no CSS (`.icone { width: 1.1rem; height: 1.1rem; }`) |
| O SVG some quando você troca a cor do fundo | `fill` fixo igual à cor de fundo, ou `fill` herdado como `none` | Use `fill="currentColor"` e controle pela propriedade `color` do elemento pai |
| O leitor de tela anuncia "Café Cerrado Café Cerrado" na navbar | Logotipo com `role="img" aria-label` ao lado de um texto que diz a mesma coisa | Se há texto visível, o desenho é decorativo: `aria-hidden="true"` |
| O <kbd>Tab</kbd> para em um lugar invisível antes do primeiro link | `<svg>` sem `focusable="false"` entrando na ordem de tabulação | Acrescente `focusable="false"` a todos os `<svg>` do projeto |
| O traço do `stroke-dasharray` aparece cortado ou já começa desenhado | Valor do `dasharray` diferente do comprimento real do caminho | Meça com `getTotalLength()` no Console e use o número exato nas duas propriedades |
| O botão pulsa para sempre e o revisor aponta violação da WCAG | `animation-iteration-count: infinite` em movimento com mais de 5 s e sem controle de pausa | Limite as repetições (`3`) ou ofereça um controle explícito de pausa |
| Emular `prefers-reduced-motion: reduce` faz elementos sumirem da página | Animação de entrada com `opacity: 0` no estado base e sem `forwards` garantido | O bloco de movimento reduzido só encurta a duração; garanta que o estado final seja o visível (`forwards`/`both`) |
| O CSS do Bootstrap vence o seu e o botão não muda | `css/estilo.css` carregado **antes** do CDN do Bootstrap no `<head>` | Inverta a ordem: framework primeiro, seu arquivo depois (Aula 04) |

## 🏠 Para praticar depois da aula (1 h)

**Parte 1 — Leitura (15 min).** QUEIRÓS e PORTELA, seções sobre a camada de apresentação avançada. MDN: *Usando transições CSS*, *Usando animações CSS* e a página inicial de *SVG: Scalable Vector Graphics* (links em "Para aprofundar"). Anote uma coisa que a MDN explica e esta aula não.

**Parte 2 — Entrega (40 min).** Aplique ao **seu projeto autoral** a Mão na massa completa, com estes seis requisitos:

1. Três microinterações com transição: links do menu, botões e elevação dos cards — cada `:hover` com seu `:focus-visible` ou `:focus-within`.
2. Uma animação com `@keyframes` e propósito declarado em comentário (entrada do título, cascata dos cards ou botão de chamada limitado a três repetições).
3. SVG inline em pelo menos dois pontos: o logotipo desenhado por você com formas básicas e ao menos três ícones em um sprite `<symbol>`/`<use>`.
4. Ao menos um SVG reagindo ao `:hover` **e** ao `:focus-visible` (troca de `fill`, rotação ou traço que se desenha).
5. O bloco `prefers-reduced-motion` como última regra do `css/estilo.css`.
6. No `README.md`, uma seção "Movimento" com três linhas: o que cada animação do projeto comunica ao usuário.

**Critério de pronto:** os seis itens presentes; emular `prefers-reduced-motion: reduce` no DevTools não esconde nem quebra nada; nenhuma animação de `width`, `height`, `top`, `left` ou `margin`; nenhum `transition: all`; o site continua funcionando publicado no GitHub Pages.

**Parte 3 — Animação que ajuda e animação que atrapalha (5 min).** Em `docs/animacao.md`, anote o endereço de um site com movimento bem empregado e de outro com movimento excessivo, explicando tecnicamente a diferença: o que cada animação comunica, a duração aproximada e a propriedade animada (verifique no DevTools). Se puder, compare com outra pessoa que esteja estudando.

**Guarde no seu repositório:** commit + push.

## ✅ Checkpoint do projeto

Ao fim desta aula o repositório do seu projeto autoral precisa ter:

- [ ] `:root` do `css/estilo.css` com variáveis de movimento (`--duracao-*`, `--curva-*`, `--elevacao`) e nenhuma duração solta no restante do arquivo.
- [ ] Transição declarada no estado base de todos os elementos clicáveis, com duração entre 150 ms e 400 ms.
- [ ] `:focus-visible` visível (anel de 3 px com `outline-offset`) em botões, links e campos; `:focus-within` nos cards.
- [ ] Menu com sublinhado animado por `scaleX` + `transform-origin`, e o item da página atual marcado por `[aria-current="page"]`.
- [ ] Cards com elevação no hover, imagem que amplia sem vazar (`overflow: hidden`) e entrada escalonada com `--i`.
- [ ] Pelo menos duas animações `@keyframes` no projeto, nenhuma delas `infinite` sem controle de pausa.
- [ ] Logotipo em SVG inline no cabeçalho das três páginas, com decisão de acessibilidade correta (`aria-hidden` ou `role="img"` com nome).
- [ ] Sprite `<symbol>`/`<use>` com ao menos três ícones, escondido por `position: absolute; width: 0; height: 0; overflow: hidden`.
- [ ] Todo `<svg>` com `focusable="false"`; ícones decorativos com `aria-hidden="true"`.
- [ ] Bloco `prefers-reduced-motion` como última regra do CSS, testado com a emulação do DevTools.
- [ ] Nenhuma animação de propriedade de layout; nenhum `transition: all`; nenhum `will-change` sem medição que o justifique.
- [ ] Seção "Movimento" no `README.md` explicando o que cada animação comunica.
- [ ] Tudo o que os checkpoints das Aulas 02, 03 e 04 pediam continua funcionando (landmarks, formulário válido, grid do Bootstrap, responsividade).

## 📚 Para aprofundar

- MDN — Usando transições CSS: <https://developer.mozilla.org/pt-BR/docs/Web/CSS/CSS_transitions/Using_CSS_transitions> — leia a lista completa de propriedades animáveis e o evento `transitionend`, que a Unidade 2 vai usar.
- MDN — Usando animações CSS: <https://developer.mozilla.org/pt-BR/docs/Web/CSS/CSS_animations/Using_CSS_animations> — a seção sobre `animation-fill-mode` resolve metade dos bugs de animação.
- MDN — Transformações CSS: <https://developer.mozilla.org/pt-BR/docs/Web/CSS/CSS_transforms> — a explicação da ordem das funções com figuras.
- MDN — SVG: <https://developer.mozilla.org/pt-BR/docs/Web/SVG> — comece pelo tutorial de *Posições* e *Formas básicas*; depois leia a referência do atributo `d`.
- MDN — `prefers-reduced-motion`: <https://developer.mozilla.org/pt-BR/docs/Web/CSS/@media/prefers-reduced-motion> — inclui como a preferência é configurada em cada sistema operacional.
- web.dev — Learn CSS, módulos *Transitions* e *Animations*: <https://web.dev/learn/css> — demonstrações interativas de cada curva de tempo.
- W3C — Scalable Vector Graphics (SVG) 2: <https://www.w3.org/TR/SVG2/> — a especificação; use como referência pontual, não como leitura linear.
- W3C — WCAG 2.2, critérios 2.2.2 e 2.3.1: <https://www.w3.org/WAI/WCAG22/quickref/> — filtre pelos números para ler o texto normativo sobre movimento e flashes.
- Bootstrap Icons: <https://icons.getbootstrap.com/> — biblioteca MIT que combina com o framework escolhido pelo Café Cerrado; copie o SVG e cole no seu sprite.
- SVGOMG: <https://svgomg.net/> — otimizador de SVG no navegador; use antes de commitar qualquer ícone baixado.
- QUEIRÓS, Ricardo; PORTELA, Filipe. *Introdução ao Desenvolvimento Moderno para a Web*. FCA, 2018 — camada de apresentação avançada (Biblioteca Virtual da UNEMAT).
- ALVES, William P. *Projetos de Sistemas Web*. Érica, 2015 — capítulo sobre elementos gráficos em interfaces.
- PUREWAL, Semmy. *Aprendendo a Desenvolver Aplicações Web*. Novatec, 2014 — front-end e organização de assets.

Seu site agora responde ao usuário e tem identidade visual própria, desenhada em código. Falta a camada que decide se ele serve para **todo mundo**. Na próxima aula você fecha a Unidade 1 com acessibilidade e ARIA: skip link, foco visível, contraste medido com números, `aria-expanded` no menu, `aria-live` no formulário e uma auditoria ao vivo com o Lighthouse. É também quando aparece o Marco 1 completo — e várias decisões que você tomou hoje (`aria-hidden` nos ícones, `focusable="false"`, `:focus-visible`, movimento reduzido) já entram nele.
