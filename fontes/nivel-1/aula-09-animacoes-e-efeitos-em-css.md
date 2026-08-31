# Aula 09 — Animações e efeitos em CSS

> **Nível 1 — Introdução ao Desenvolvimento Web** · Unidade 2: CSS: estilo, layout e responsividade
> WebLab · UNEMAT — Campus Sinop
> **Tempo estimado:** 3 blocos de 50 min + 1 h de prática

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Aplicar transições para suavizar mudanças de estado em botões, links, cartões e menus, escolhendo duração e curva adequadas.
- Usar transformações 2D e 3D (`translate`, `scale`, `rotate`, `skew`, `perspective`) para mover, girar e escalar elementos sem afetar o layout dos vizinhos.
- Criar animações com `@keyframes` e controlá-las com as propriedades de `animation`, incluindo animações escalonadas e múltiplas.
- Explicar o pipeline de renderização (layout → paint → composite) e escolher propriedades baratas (`transform` e `opacity`) para animar sem travar a interface.
- Respeitar `prefers-reduced-motion` e os critérios de acessibilidade da WCAG sobre movimento, piscadas e pausa.
- Construir efeitos visuais comuns — sombras, gradientes, filtros, `backdrop-filter`, efeitos de hover e revelação ao rolar — com feedback também para quem navega por teclado.
- Medir o desempenho de uma animação no painel Performance do DevTools e provar, com números, que `transform` é mais barato que `left`.

## 📋 Pré-requisitos

- [ ] Site do evento (`site-evento/`) com as cinco páginas estilizadas pelo `css/estilo.css` da Aula 06, layout Grid + Flexbox e menu acessível da Aula 07, e responsivo com menu hambúrguer, tema escuro e `js/menu.js` da Aula 08.
- [ ] Seu projeto autoral no mesmo estágio (responsivo em três larguras).
- [ ] VS Code com Live Server; Chrome ou Firefox com DevTools — hoje você vai usar o painel **Performance** e a aba **Rendering**.
- [ ] Um celular na mesma rede Wi-Fi do computador (para sentir a diferença de desempenho de verdade).

> Na aula passada você fez o site do evento se adaptar a qualquer tela: mobile first, três breakpoints, menu hambúrguer com `aria-expanded`, imagens fluidas e tema escuro com `prefers-color-scheme`. O site funciona em qualquer lugar — mas tudo nele acontece de repente: o menu aparece num estalo, o botão muda de cor sem aviso, os cartões surgem prontos. Hoje você dá **movimento** ao site, com transições, transformações e animações que comunicam algo, custam pouco para o navegador e respeitam quem prefere menos movimento. Esta aula fecha a Unidade 2.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Por que animar; transições (as quatro propriedades, curvas, durações, o que pode ser animado); transformações 2D e 3D |
| 2 | 50 min | `@keyframes` e `animation`; animações de referência; performance (layout → paint → composite, `will-change`); `prefers-reduced-motion` e WCAG |
| 3 | 50 min | Efeitos visuais (sombras, gradientes, filtros, hover, revelação ao rolar); Mão na massa: polindo o site do evento; Laboratório |

## 1. Por que animar

Animação em interface não é enfeite. Ela serve a três funções concretas:

| Função | Exemplo |
|---|---|
| **Feedback** | O botão escurece e afunda ao ser pressionado — o clique foi registrado |
| **Continuidade** | Um painel desliza para dentro — o usuário entende de onde ele veio e para onde vai voltar |
| **Atenção** | Uma mensagem de erro treme levemente — o olho é direcionado ao campo com problema |

Pense no menu hambúrguer da Aula 08. Quando ele aparece de repente, o cérebro precisa de um instante para entender "de onde veio isso?". Quando ele desliza de cima para baixo em 250 ms, a origem é óbvia: saiu do botão. É a mesma quantidade de informação, entregue com menos esforço.

> **⚠️ Atenção**
> Regra de ouro: **se a animação não comunica nada, remova-a.** Movimento gratuito cansa, atrasa a interação (o usuário espera a animação acabar para clicar) e prejudica pessoas com sensibilidade vestibular. Toda animação desta aula precisa responder à pergunta "o que isso está dizendo ao usuário?".

> **🧠 Você sabia?**
> Os "12 princípios da animação" foram formulados por dois animadores da Disney, Frank Thomas e Ollie Johnston, no livro *The Illusion of Life* — décadas antes de existir CSS. Vários deles migraram direto para as interfaces: *ease in / ease out* (nada no mundo físico começa nem para de repente), *anticipation* (um botão que "afunda" antes de abrir um painel) e *follow through* (o painel que passa um pouquinho do ponto e volta — o efeito de ricochete do `cubic-bezier`). As diretrizes de movimento do Material Design, da Apple e da Microsoft citam esses princípios explicitamente.

## 2. Transições

Uma **transição** interpola automaticamente a mudança de um valor entre dois estados. Você declara os dois estados (normal e `:hover`, por exemplo) e diz ao navegador "em vez de trocar de repente, leve 200 ms para ir de um ao outro". O navegador calcula todos os valores intermediários, quadro a quadro.

**`css/estilo.css`** (trecho de exemplo)

```css
.botao {
  background-color: var(--cor-primaria);
  transform: translateY(0);
  transition: background-color 200ms ease, transform 200ms ease;
}

.botao:hover {
  background-color: var(--cor-secundaria);
  transform: translateY(-2px);
}
```

Passe o mouse sobre o botão: a cor muda suavemente e ele sobe 2 px. Tire o mouse: ele desce e volta à cor original, também suavemente — porque a `transition` está declarada no estado **normal**, e vale para os dois sentidos.

### As quatro propriedades

```css
.botao {
  transition-property: background-color, transform;   /* o que anima */
  transition-duration: 200ms;                         /* quanto tempo */
  transition-timing-function: ease;                   /* a curva de velocidade */
  transition-delay: 0s;                               /* espera antes de começar */
}

/* Atalho: propriedade  duração  curva  atraso */
.painel {
  transition: transform 300ms ease-out 100ms;
}
```

O atalho `transition` aceita várias transições separadas por vírgula, cada uma com sua duração e curva. Na prática você quase sempre usa o atalho.

> **📌 Vale gravar**
> A `transition` deve ser declarada no **estado base** do elemento (`.botao`), não no estado de interação (`.botao:hover`). Se ficar no `:hover`, a entrada é suave e a saída é abrupta — porque ao tirar o mouse a regra `:hover` deixa de valer, e com ela a `transition`.

### Funções de tempo

A **curva** define como a velocidade varia ao longo da transição. É o que separa um movimento "mecânico" de um movimento natural.

| Valor | Comportamento | Uso típico |
|---|---|---|
| `linear` | Velocidade constante | Rotação contínua, barras de progresso |
| `ease` | Acelera e desacelera (padrão) | Uso geral |
| `ease-in` | Começa devagar | Elemento **saindo** da tela |
| `ease-out` | Termina devagar | Elemento **entrando** na tela |
| `ease-in-out` | Devagar nas duas pontas | Movimentos longos |
| `cubic-bezier(.34, 1.56, .64, 1)` | Curva personalizada | Efeito de "ricochete" (passa do ponto e volta) |
| `steps(5, end)` | Saltos discretos | Sprites, efeito de digitação |

A regra de bolso: **o que entra usa `ease-out`** (chega rápido e assenta devagar, como um carro estacionando); **o que sai usa `ease-in`** (parte devagar e some rápido). Use o site [cubic-bezier.com](https://cubic-bezier.com) para desenhar curvas visualmente e comparar duas lado a lado.

### Duração adequada

| Faixa | Percepção |
|---|---|
| 100–150 ms | Micro-interações: `:hover`, foco, mudança de cor |
| 200–300 ms | Padrão para a maioria dos casos |
| 300–500 ms | Painéis, modais, elementos grandes que percorrem distância |
| acima de 500 ms | Percebido como lento e irritante |

Elementos pequenos que se movem pouco precisam de menos tempo; elementos grandes que atravessam a tela precisam de mais. Na dúvida, comece em 200 ms e ajuste olhando.

> **⚠️ Atenção**
> `transition: all` é uma armadilha. Ele anima **todas** as propriedades que mudarem, inclusive as que você não pretendia — e as caras (`width`, `height`, `margin`). Pior: quando você acrescentar CSS meses depois, coisas passam a animar sem você entender por quê. Liste as propriedades explicitamente, sempre.

### O que pode e o que não pode ser animado

Só propriedades com valores **numericamente interpoláveis** transicionam. O navegador precisa conseguir calcular "o valor no meio do caminho" entre o estado inicial e o final.

- **Funcionam:** `color`, `background-color`, `opacity`, `width`, `height`, `transform`, `box-shadow`, `border-radius`, `padding`, `margin`, `font-size`.
- **Não funcionam:** `display`, `font-family`, `position`, `flex-direction`, `grid-template-columns` (em alguns navegadores), `visibility` (tem regra especial, veja abaixo).

Não existe "meio caminho" entre `display: none` e `display: block`. Por isso o exemplo abaixo simplesmente não anima:

```css
/* Errado: display não interpola — o painel aparece de repente */
.painel {
  display: none;
  transition: display 300ms;
}
```

A solução clássica combina `opacity` (que interpola) com `visibility` (que tira o elemento da navegação por teclado e do leitor de tela):

```css
/* Certo: opacity anima; visibility esconde do teclado e do leitor de tela */
.painel {
  opacity: 0;
  visibility: hidden;
  transition: opacity 300ms ease, visibility 0s 300ms;
}

.painel.ativo {
  opacity: 1;
  visibility: visible;
  transition: opacity 300ms ease, visibility 0s;
}
```

Repare no truque do `visibility`. Ao **esconder**, `visibility 0s 300ms` espera os 300 ms do fade terminar e só então vira `hidden` — senão o painel sumiria instantaneamente antes de desvanecer. Ao **mostrar**, `visibility 0s` (sem atraso) torna o elemento visível na hora, e o `opacity` faz o fade de entrada.

> **🔎 Por baixo do capô**
> Por que `opacity: 0` sozinho não basta? Porque um elemento transparente **continua no fluxo e continua focável**: quem navega por <kbd>Tab</kbd> cai em links invisíveis, e o leitor de tela lê o conteúdo de um painel que "não está lá". `visibility: hidden` resolve os dois problemas. Navegadores recentes começam a aceitar `transition-behavior: allow-discrete` junto com `@starting-style` para animar até `display`, mas a dupla `opacity` + `visibility` funciona em todos e é o que você vai usar nesta disciplina.

## 3. Transformações

`transform` altera a **renderização** do elemento sem afetar o layout dos vizinhos. Um elemento com `transform: translateX(50px)` é desenhado 50 px à direita, mas para o resto da página ele continua exatamente onde estava — ninguém é empurrado, nada é recalculado. É por isso que `transform` é barato (a §6 mostra o quanto).

```css
/* Translação: move sem tirar do fluxo */
.a { transform: translateX(20px); }
.b { transform: translateY(-10px); }
.c { transform: translate(20px, -10px); }

/* Escala: 1 = tamanho original */
.d { transform: scale(1.05); }          /* 5% maior nos dois eixos */
.e { transform: scaleX(2) scaleY(0.5); } /* estica na horizontal, achata na vertical */

/* Rotação: graus ou voltas */
.f { transform: rotate(45deg); }
.g { transform: rotate(-0.25turn); }    /* um quarto de volta no sentido anti-horário */

/* Inclinação */
.h { transform: skewX(15deg); }

/* Combinadas — a ORDEM importa */
.i { transform: translateX(50px) rotate(45deg); }  /* move, depois gira no lugar */
.j { transform: rotate(45deg) translateX(50px); }  /* gira o eixo, depois move ao longo do eixo girado */
```

Sobre a ordem: as funções são aplicadas **da esquerda para a direita, sobre o sistema de coordenadas do elemento**. Em `.i`, o elemento desliza 50 px para a direita e então gira em torno do próprio centro. Em `.j`, o elemento primeiro gira — e com ele giram os eixos X e Y — e só então anda 50 px "para a direita", que agora aponta para a diagonal. Os dois terminam em lugares diferentes. Teste no DevTools trocando a ordem e veja.

### Ponto de origem

Toda transformação acontece em torno de um ponto. O padrão é o centro do elemento; `transform-origin` muda isso.

```css
.padrao   { transform-origin: center; }     /* padrão: gira/escala em torno do centro */
.canto    { transform-origin: top left; }   /* gira em torno do canto superior esquerdo */
.base     { transform-origin: 50% 100%; }   /* meio da borda inferior — um pêndulo */
```

Um ponteiro de relógio gira em torno da base, não do centro; um menu suspenso "cresce" a partir do topo; o sublinhado do menu do site do evento cresce a partir da esquerda. Sempre que a origem padrão parecer estranha, é `transform-origin` que resolve.

### Transformações 3D

Com `perspective` no contêiner pai, o navegador passa a projetar as transformações 3D dos filhos com profundidade. O exemplo clássico é o cartão que vira para mostrar o verso — a estrutura tem três camadas: o palco (com a perspectiva), o virador (que gira) e as duas faces.

**`exemplos/cartao-3d.html`**

```html
<div class="virador">
  <div class="virador__faces">
    <div class="virador__face virador__frente">
      <img src="img/palestrante-ana.jpg" alt="">
      <h3>Ana Souza</h3>
    </div>
    <div class="virador__face virador__verso">
      <p>Engenheira de software, trabalha com sistemas distribuídos e ensina Go.</p>
      <a href="palestrantes.html#ana">Ver palestra</a>
    </div>
  </div>
</div>
```

**`exemplos/cartao-3d.css`**

```css
.virador {
  perspective: 1000px;            /* no CONTÊINER pai — nunca no elemento que gira */
  width: 280px;
  height: 360px;
}

.virador__faces {
  position: relative;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;   /* os filhos continuam em 3D, e não achatados */
  transition: transform 600ms ease;
}

.virador__face {
  position: absolute;
  inset: 0;
  backface-visibility: hidden;    /* esconde a face que está de costas para você */
  border-radius: var(--raio-borda);
  background: var(--cor-superficie);
  box-shadow: var(--sombra-cartao);
}

.virador__verso {
  transform: rotateY(180deg);     /* começa virado para trás */
}

.virador:hover .virador__faces,
.virador:focus-within .virador__faces {
  transform: rotateY(180deg);
}
```

Quanto menor o valor de `perspective`, mais "perto" está o observador e mais exagerada fica a distorção. Valores entre 800 px e 1200 px parecem naturais. O `:focus-within` faz o cartão virar também quando o link do verso recebe foco por teclado — sem isso, quem não usa mouse jamais veria o verso.

## 4. Animações com `@keyframes`

Transições precisam de uma **mudança de estado** (hover, classe adicionada, foco). Animações rodam **sozinhas**, podem ter vários passos intermediários e podem se repetir.

Uma animação tem duas partes: a **definição** dos quadros-chave (`@keyframes`) e a **aplicação** a um elemento (`animation`).

```css
@keyframes pulsar {
  0%   { transform: scale(1);    opacity: 1; }
  50%  { transform: scale(1.08); opacity: 0.85; }
  100% { transform: scale(1);    opacity: 1; }
}

.alerta {
  animation: pulsar 1.5s ease-in-out infinite;
}
```

O navegador interpola entre cada par de quadros consecutivos: de 0 % a 50 % o elemento cresce e clareia; de 50 % a 100 % volta. Com `infinite`, recomeça para sempre.

Quando há só dois passos, `from` e `to` são mais legíveis:

```css
@keyframes surgir {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

### As propriedades de `animation`

```css
.cartao {
  animation-name: surgir;
  animation-duration: 400ms;
  animation-timing-function: ease-out;
  animation-delay: 100ms;
  animation-iteration-count: 1;        /* ou infinite, ou um número */
  animation-direction: normal;         /* reverse | alternate | alternate-reverse */
  animation-fill-mode: forwards;       /* none | forwards | backwards | both */
  animation-play-state: running;       /* paused */
}

/* Atalho: nome duração curva atraso repetições direção preenchimento */
.cartao {
  animation: surgir 400ms ease-out 100ms 1 normal forwards;
}
```

Um detalhe do atalho: quando há dois valores de tempo, o **primeiro** é a duração e o **segundo** é o atraso. `animation: surgir 400ms 100ms` significa "dura 400 ms, começa depois de 100 ms".

> **⚠️ Atenção**
> `animation-fill-mode` é o que quase todo mundo esquece. Sem ele, quando a animação termina o elemento **volta ao estado original** — o cartão que surgiu do nada desaparece de novo. Com `forwards`, o último quadro permanece aplicado. Com `backwards`, o **primeiro** quadro é aplicado durante o `animation-delay` (útil em animações escalonadas: o elemento fica invisível enquanto espera a sua vez). `both` faz as duas coisas.

`animation-direction: alternate` inverte o sentido a cada repetição (vai e volta, como um pêndulo), o que evita o "salto" no fim de cada ciclo de uma animação `infinite`. `reverse` roda a animação de trás para frente, sempre.

### Animações escalonadas

Cartões que surgem um após o outro, em cascata, parecem mais vivos que todos surgindo ao mesmo tempo. A forma ingênua é um atraso por posição:

```css
.cartao { animation: surgir 400ms ease-out backwards; }
.cartao:nth-child(1) { animation-delay: 0ms; }
.cartao:nth-child(2) { animation-delay: 80ms; }
.cartao:nth-child(3) { animation-delay: 160ms; }
.cartao:nth-child(4) { animation-delay: 240ms; }
```

Funciona, mas não escala: com 12 cartões são 12 regras. Com uma **variável CSS** por elemento, o mesmo efeito fica genérico:

```css
.cartao {
  animation: surgir 400ms ease-out backwards;
  animation-delay: calc(var(--i, 0) * 80ms);
}
```

```html
<li class="cartao" style="--i: 0">Primeiro cartão</li>
<li class="cartao" style="--i: 1">Segundo cartão</li>
<li class="cartao" style="--i: 2">Terceiro cartão</li>
```

O `var(--i, 0)` tem um valor de reserva: se algum cartão vier sem `--i`, ele anima sem atraso, em vez de quebrar. Repare no `backwards`: sem ele, os cartões que ainda estão esperando o atraso ficariam **visíveis** no estado final e só "piscariam" quando a animação começasse.

### Múltiplas animações

Um elemento pode rodar várias animações ao mesmo tempo, separadas por vírgula. Cada uma tem sua duração, curva, atraso e repetição:

```css
.balao {
  animation:
    surgir 400ms ease-out,
    flutuar 3s ease-in-out 400ms infinite;
}
```

O balão surge em 400 ms e, quando termina de surgir, passa a flutuar para sempre. Cuidado: se duas animações mexem na **mesma propriedade** (aqui, as duas usam `transform`), a última declarada vence enquanto estiver rodando.

> **🔎 Por baixo do capô**
> Quando você aplica `animation` a um elemento, o navegador cria uma linha do tempo interna para ele e, a cada quadro (idealmente 60 por segundo), calcula em que ponto da linha ele está, interpola os valores dos dois quadros-chave vizinhos e reaplica o estilo. Tudo isso acontece **fora** do fluxo de JavaScript da página — se a animação usa só `transform` e `opacity`, ela roda até com a thread principal ocupada. É a diferença entre "o botão continua girando enquanto a página carrega" e "o botão trava".

## 5. Animações úteis de referência

Cinco animações que aparecem em quase todo projeto. Copie para o seu `css/estilo.css` conforme precisar — todas usam só `transform`, `opacity` ou `background-position`.

**`css/estilo.css`** (seção 5 — componentes)

```css
/* Carregando — giro contínuo */
@keyframes girar {
  to { transform: rotate(360deg); }
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--cor-borda);
  border-top-color: var(--cor-secundaria);
  border-radius: 50%;
  animation: girar 700ms linear infinite;
}

/* Esqueleto de carregamento — brilho que percorre a caixa */
@keyframes brilho {
  to { background-position-x: -200%; }
}

.esqueleto {
  background: linear-gradient(90deg,
    var(--cor-esqueleto) 40%,
    var(--cor-esqueleto-brilho) 50%,
    var(--cor-esqueleto) 60%);
  background-size: 200% 100%;
  border-radius: var(--raio-borda);
  animation: brilho 1.4s linear infinite;
}

/* Balançar — campo inválido */
@keyframes tremer {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-6px); }
  40%, 80% { transform: translateX(6px); }
}

.campo.invalido {
  animation: tremer 400ms ease;
}

/* Entrada lateral */
@keyframes entrarEsquerda {
  from { opacity: 0; transform: translateX(-24px); }
  to   { opacity: 1; transform: translateX(0); }
}

/* Flutuação sutil — para um ícone ou ilustração de destaque */
@keyframes flutuar {
  0%, 100% { transform: translateY(0); }
  50%      { transform: translateY(-8px); }
}
```

O `@keyframes girar` só tem `to`: quando falta o `from`, o navegador usa o estado atual do elemento como ponto de partida (`rotate(0deg)`). O esqueleto usa um gradiente com o dobro da largura da caixa e desloca a posição do fundo — o "brilho" do meio parece passar de um lado ao outro.

> **💡 Dica**
> Dê nomes de `@keyframes` que descrevam o **movimento** (`surgir`, `tremer`, `girar`), não o uso (`animacaoDoCartao`). Assim a mesma animação serve para cartões, alertas e imagens, e você constrói aos poucos uma biblioteca reutilizável — o desafio ⭐⭐⭐ desta aula é exatamente isso.

## 6. Performance: as duas propriedades baratas

O navegador desenha uma página em etapas. Entender essas etapas é o que separa uma animação que roda lisa no celular de uma que trava.

1. **Layout** (também chamado de *reflow*): o navegador calcula a posição e o tamanho de cada elemento. Se um elemento muda de largura, todos os vizinhos, os filhos e às vezes a página inteira precisam ser recalculados.
2. **Paint**: o navegador pinta os pixels de cada elemento — cores, bordas, sombras, texto.
3. **Composite**: o navegador junta as camadas já pintadas na tela, com posição, escala e opacidade. Essa etapa roda na GPU e é muito barata.

Cada propriedade CSS, quando animada, dispara a partir de uma dessas etapas — e tudo que vem depois:

| Propriedade animada | Etapas disparadas | Custo |
|---|---|---|
| `width`, `height`, `margin`, `padding`, `top`, `left` | Layout + Paint + Composite | Alto |
| `background-color`, `box-shadow`, `color`, `border-radius` | Paint + Composite | Médio |
| `transform`, `opacity` | Só Composite | Baixo |

A conclusão prática cabe numa frase: **sempre que possível, anime apenas `transform` e `opacity`.** Um painel que desliza com `left` obriga o navegador a refazer o layout da página a cada quadro; o mesmo painel com `translateX` só muda a posição de uma camada já pintada.

```css
/* Errado: recalcula o layout a cada quadro — trava em celular */
.menu-lateral {
  left: -300px;
  transition: left 300ms;
}
.menu-lateral.aberto {
  left: 0;
}

/* Certo: só composição — 60 fps mesmo em aparelhos modestos */
.menu-lateral {
  transform: translateX(-300px);
  transition: transform 300ms;
}
.menu-lateral.aberto {
  transform: translateX(0);
}
```

O resultado visual é idêntico. O custo, não.

> **🧠 Você sabia?**
> A maioria das telas atualiza 60 vezes por segundo. Isso dá ao navegador **16,7 ms** para produzir cada quadro — calcular layout, pintar e compor. Se um quadro demora mais que isso, ele é pulado, e o olho percebe o "engasgo": é o que os desenvolvedores chamam de *jank*. Animar `left` numa página grande pode custar 30 ms por quadro só de layout; animar `transform` custa uma fração de milissegundo, porque a GPU só desloca uma textura já pronta. Telas de 120 Hz (comuns em celulares atuais) dão apenas 8,3 ms por quadro — a margem só diminui.

### `will-change` — com moderação

```css
.painel {
  will-change: transform;
}
```

`will-change` avisa o navegador com antecedência: "este elemento vai animar `transform`, prepare uma camada dedicada para ele". Isso evita o pequeno atraso da criação da camada no início da animação. Mas cada camada consome memória da GPU. Aplique **apenas** em elementos que realmente vão animar e que mostraram problema na medição; nunca em `*` ou em dezenas de elementos. Deixar `will-change` espalhado piora o desempenho — exatamente o oposto do pretendido.

> **🔬 Investigue**
> Abra o site do evento, pressione <kbd>F12</kbd> e vá ao painel **Performance**. No ícone de engrenagem, marque **CPU: 4× slowdown** (simula um celular barato). Clique em gravar, passe o mouse sobre alguns cartões e abra o menu hambúrguer, pare a gravação. Na linha do tempo, procure as barras roxas (**Layout**) e verdes (**Paint**) e o gráfico de **FPS** no topo. Agora troque temporariamente uma transição de `transform` por `left` (ou `margin-left`) e repita. Compare: quantos quadros caíram abaixo de 60 fps? Quanto tempo total foi gasto em Layout? Guarde as duas capturas — o desafio ⭐⭐ pede exatamente esse relatório. Bônus: na aba **Rendering** (menu ⋮ → More tools), ative **Paint flashing**: tudo que é repintado pisca em verde. Uma animação boa quase não pisca.

## 7. Acessibilidade — não é opcional

Movimento excessivo causa náusea, tontura e desorientação em pessoas com distúrbios vestibulares — e o problema não é raro. Todo sistema operacional moderno tem uma opção "reduzir movimento" (no Android, em Acessibilidade; no iOS, em Acessibilidade → Movimento; no Windows, em Configurações de exibição). O CSS consegue ler essa preferência:

**`css/estilo.css`** (última seção do arquivo, depois de todas as media queries)

```css
/* Respeita a preferência do sistema por menos movimento.
   Precisa ficar no FIM da folha para vencer qualquer regra anterior. */
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

Este bloco é uma das poucas situações em que `!important` é justificado: ele precisa vencer **qualquer** regra do projeto, inclusive as mais específicas, e ninguém deve conseguir sobrescrevê-lo por acidente. Cole-o no fim de toda folha de estilo desta disciplina.

Dois detalhes que costumam gerar dúvida:

- **Por que `0.01ms` e não `0`?** Na Unidade 3 você vai escrever JavaScript que espera o evento `transitionend` ou `animationend` para fazer algo (fechar um painel, por exemplo). Com duração zero, alguns navegadores não disparam o evento e o código trava. Com 0,01 ms, a animação "acontece" instantaneamente e o evento dispara.
- **Por que a Aula 08 já tinha uma versão curta disso?** Lá o bloco só existia para você conhecer a media query. Esta versão cobre pseudo-elementos, repetições infinitas e rolagem suave — é a definitiva.

Reduzir movimento **não** significa remover feedback. A melhor prática é trocar o movimento por um fade: onde o cartão deslizava 24 px para cima, ele apenas aparece. O desafio ⭐ desta aula trabalha isso.

Outras regras, todas com base na WCAG 2.1:

- Nada que pisque mais de **3 vezes por segundo** (critério 2.3.1 — risco de convulsão fotossensível).
- Animações infinitas que chamam atenção devem poder ser **pausadas** (critério 2.2.2 — pausar, parar, ocultar). Carrosséis automáticos precisam de botão de pausa visível.
- Nunca use animação como **única** forma de comunicar informação: o campo inválido treme **e** fica com borda vermelha **e** mostra uma mensagem de texto.
- Todo efeito de `:hover` precisa de um equivalente em `:focus-visible` — quem navega por teclado também merece feedback.

> **🔬 Investigue**
> No DevTools, aba **Rendering**, procure **Emulate CSS media feature prefers-reduced-motion** e escolha `reduce`. Recarregue o site do evento. Tudo que ainda se mexe é uma regra que escapou do bloco acima — geralmente uma animação declarada em um arquivo carregado depois de `estilo.css`, ou uma `transition` inline. Faça o mesmo com `prefers-color-scheme: dark` para conferir o tema escuro da Aula 08.

## 8. Efeitos visuais

Nem todo efeito envolve movimento. Sombras, gradientes e filtros dão profundidade e hierarquia à página — e, combinados com transições, produzem os efeitos de hover que você vê nos sites profissionais.

### Sombras

```css
/* Elevação sutil — cartões em repouso */
.cartao { box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12); }

/* Elevação média — cartão em hover, menu suspenso */
.cartao:hover { box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); }

/* Sombra interna — campo de formulário "afundado" */
.campo { box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1); }

/* Anel de foco — alternativa ao outline que respeita o border-radius */
.botao:focus-visible { box-shadow: 0 0 0 3px rgba(26, 127, 181, 0.4); }

/* Múltiplas sombras — uma curta e densa, outra longa e difusa */
.modal { box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1), 0 8px 24px rgba(0, 0, 0, 0.12); }

/* Sombra que acompanha o formato (útil em PNG com transparência e SVG) */
.logo { filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.2)); }
```

Os quatro valores de `box-shadow` são: deslocamento horizontal, deslocamento vertical, desfoque e cor. Sombras realistas têm deslocamento vertical maior que o horizontal (a luz vem de cima) e cor preta com pouca opacidade, nunca cinza sólido. `box-shadow` desenha um retângulo (ou o `border-radius` da caixa); `filter: drop-shadow()` segue o contorno real dos pixels — é o que você quer numa logo com fundo transparente.

### Gradientes

```css
/* Linear: direção por palavra-chave ou ângulo */
.faixa   { background: linear-gradient(to right, #0b3d5c, #1a7fb5); }
.faixa-2 { background: linear-gradient(135deg, #0b3d5c 0%, #1a7fb5 60%, #7ec8e3 100%); }

/* Radial: a partir de um ponto */
.bolha { background: radial-gradient(circle at 30% 30%, #1a7fb5, #0b3d5c); }

/* Cônico: gira em torno do centro — gráficos de pizza sem JavaScript */
.pizza { background: conic-gradient(#0b3d5c 0% 25%, #1a7fb5 25% 100%); }

/* Texto com gradiente */
.titulo-gradiente {
  background: linear-gradient(90deg, #0b3d5c, #1a7fb5);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

/* Sobreposição escura em imagem, para garantir contraste do texto */
.hero {
  background:
    linear-gradient(rgba(0, 0, 0, 0.55), rgba(0, 0, 0, 0.55)),
    url("../img/banner.jpg") center / cover no-repeat;
  color: #ffffff;
}
```

O último exemplo é o mais importante para o projeto: texto branco sobre uma foto **nunca** tem contraste garantido — em alguma parte da imagem haverá um trecho claro. Um gradiente de duas cores iguais funciona como um "vidro escuro" sobre a foto e garante o contraste AA em toda a área. Repare no caminho `../img/banner.jpg`: dentro de `css/estilo.css`, os caminhos são relativos ao **arquivo CSS**, não à página HTML.

### Filtros

```css
.a { filter: blur(4px); }
.b { filter: brightness(1.2); }
.c { filter: contrast(1.1); }
.d { filter: grayscale(100%); }
.e { filter: saturate(1.4); }
.f { filter: sepia(60%); }
.g { filter: hue-rotate(90deg); }
.h { filter: invert(100%); }
.i { filter: grayscale(100%) brightness(1.1); }   /* combináveis, aplicados em ordem */

/* Desfoque do que está ATRÁS do elemento — o "vidro fosco" */
.modal-fundo {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(8px);
}
```

`filter` altera o próprio elemento; `backdrop-filter` altera o que está **atrás** dele — é o efeito de vidro fosco dos menus e modais modernos. Como a foto de um palestrante em preto e branco que ganha cor no hover: `filter: grayscale(100%)` no estado normal, `grayscale(0)` no `:hover`, com `transition: filter 300ms`.

### Efeitos de hover comuns

```css
/* 1. Sublinhado que cresce da esquerda e recolhe pela direita */
.link {
  position: relative;
  text-decoration: none;
}

.link::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: -2px;
  width: 100%;
  height: 2px;
  background: currentColor;
  transform: scaleX(0);
  transform-origin: right;
  transition: transform 250ms ease;
}

.link:hover::after,
.link:focus-visible::after {
  transform: scaleX(1);
  transform-origin: left;
}

/* 2. Cartão que se eleva */
.cartao {
  transition: transform 200ms ease, box-shadow 200ms ease;
}

.cartao:hover,
.cartao:focus-within {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

/* 3. Zoom da imagem dentro da moldura */
.moldura {
  overflow: hidden;
  border-radius: var(--raio-borda);
}

.moldura img {
  display: block;
  transition: transform 400ms ease;
}

.moldura:hover img,
.moldura:focus-within img {
  transform: scale(1.06);
}
```

O sublinhado (efeito 1) é o mesmo que você usou "de bônus" no menu da Aula 07 — agora com um refinamento: a troca de `transform-origin` faz a linha **crescer da esquerda** ao entrar e **recolher pela direita** ao sair, como se deslizasse por baixo do texto. No zoom (efeito 3), o `overflow: hidden` da moldura corta o excesso da imagem ampliada; sem ele, a imagem invadiria os vizinhos.

> **⚠️ Atenção**
> Sempre replique o efeito de `:hover` também em `:focus-visible` (ou `:focus-within`, quando o elemento interativo está dentro do cartão). Caso contrário, quem navega por teclado não recebe **nenhum** retorno visual — e não tem como saber onde está.

### Revelação ao rolar a página

O efeito de seções que "surgem" conforme você rola é a combinação de uma transição CSS com um pedacinho de JavaScript que observa quando o elemento entra na tela. O JavaScript é a Unidade 3; aqui você só precisa saber que ele **adiciona uma classe** — toda a animação continua no CSS.

**`css/estilo.css`** (seção 6 — utilitários)

```css
/* Só esconde quando o JavaScript está ativo; sem JS, o conteúdo aparece normalmente */
.js .revelar {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 500ms ease, transform 500ms ease;
}

.js .revelar.visivel {
  opacity: 1;
  transform: translateY(0);
}
```

**`js/efeitos.js`**

```js
// Marca que o JavaScript está ativo: o CSS só esconde os .revelar com essa classe.
document.documentElement.classList.add("js");

// Observa cada elemento .revelar e adiciona "visivel" quando 15% dele entra na tela.
const observador = new IntersectionObserver((entradas) => {
  entradas.forEach((entrada) => {
    if (entrada.isIntersecting) {
      entrada.target.classList.add("visivel");
      observador.unobserve(entrada.target); // já revelou: para de observar
    }
  });
}, { threshold: 0.15 });

document.querySelectorAll(".revelar").forEach((elemento) => observador.observe(elemento));
```

**`index.html`** (antes de `</body>`)

```html
<script src="js/efeitos.js" defer></script>
```

> **💡 Dica**
> Repare na classe `.js` no `<html>`. Se o CSS escondesse `.revelar` incondicionalmente e o JavaScript falhasse (bloqueado, com erro, ou ainda carregando numa conexão lenta), o conteúdo ficaria **invisível para sempre**. Com o `.js` adicionado pelo próprio script, sem JavaScript a página é só uma página normal. Conteúdo nunca deve depender de animação para existir — esse é o padrão correto, sem exceção.

## 💻 Mão na massa — Polindo o site do evento

Você vai aplicar os dez itens da prática guiada ao site da **Semana Acadêmica de Sistemas de Informação**. Todos os trechos vão em `css/estilo.css`, respeitando a ordem da folha da Aula 06 (1 reset · 2 variáveis · 3 base · 4 layout · 5 componentes · 6 utilitários · 7 media queries), mais um arquivo novo, `js/efeitos.js`. Abra o site com o Live Server e mantenha o DevTools aberto: cada passo tem um resultado visível.

### Passo 1 — variáveis de movimento e transições nos elementos interativos

Assim como as cores e os espaçamentos, as durações e curvas do projeto viram variáveis. Se um dia o evento quiser um site "mais calmo", você muda três linhas.

**`css/estilo.css`** (seção 2 — variáveis; acrescente ao `:root` existente)

```css
:root {
  --duracao-curta: 150ms;
  --duracao-media: 250ms;
  --duracao-longa: 400ms;
  --curva-padrao: ease-out;
  --cor-esqueleto: #e4e9ee;         /* fundo do cartão-esqueleto */
  --cor-esqueleto-brilho: #f2f5f8;  /* faixa clara que percorre o esqueleto */
}
```

E, no bloco `@media (prefers-color-scheme: dark)` que você escreveu na Aula 08, os dois valores escuros correspondentes — sem eles, o esqueleto vira uma mancha branca no tema escuro:

```css
@media (prefers-color-scheme: dark) {
  :root {
    --cor-esqueleto: #1e2a3a;
    --cor-esqueleto-brilho: #2a3948;
  }
}
```

As duas cores do esqueleto entram como variáveis pelo mesmo motivo de todas as outras: o Boss desta aula exige "nenhuma cor solta na folha", e um valor fixo aqui quebraria o tema escuro exatamente no componente que mais aparece durante o carregamento.

**`css/estilo.css`** (seção 5 — componentes; substitua as regras de `.botao`, links e campos da Aula 06)

```css
/* Botões: cor, elevação e "afundar" ao pressionar */
.botao {
  display: inline-block;
  padding: var(--espaco-pequeno) var(--espaco-grande);
  background-color: var(--cor-primaria);
  color: #ffffff;
  border: 0;
  border-radius: 999px;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  transition:
    background-color var(--duracao-curta) var(--curva-padrao),
    transform var(--duracao-curta) var(--curva-padrao),
    box-shadow var(--duracao-curta) var(--curva-padrao);
}

.botao:hover,
.botao:focus-visible {
  background-color: var(--cor-secundaria);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.botao:active {
  transform: translateY(0);
  box-shadow: none;
}

.botao:focus-visible {
  outline: 3px solid var(--cor-secundaria);
  outline-offset: 3px;
}

/* Links de conteúdo */
main a {
  color: var(--cor-secundaria);
  transition: color var(--duracao-curta) var(--curva-padrao);
}

main a:hover,
main a:focus-visible {
  color: var(--cor-primaria);
}

/* Campos do formulário de inscrição (Aula 03) */
.campo input,
.campo select,
.campo textarea {
  border: 1px solid var(--cor-borda);
  border-radius: var(--raio-borda);
  padding: var(--espaco-pequeno) var(--espaco-medio);
  transition:
    border-color var(--duracao-curta) var(--curva-padrao),
    box-shadow var(--duracao-curta) var(--curva-padrao);
}

.campo input:focus-visible,
.campo select:focus-visible,
.campo textarea:focus-visible {
  outline: none;
  border-color: var(--cor-secundaria);
  box-shadow: 0 0 0 3px rgba(26, 127, 181, 0.35);
}
```

Todas as durações ficam entre 150 ms e 250 ms — micro-interações. Repare que o `:active` **não** tem transição própria: ele herda a do estado base, e o botão "afunda" em 150 ms.

### Passo 2 — menu com sublinhado animado e item ativo

Substitua o `::after` do menu da Aula 07 por esta versão, que cresce da esquerda e recolhe pela direita:

**`css/estilo.css`** (seção 4 — layout, regras do `.menu`)

```css
.menu a {
  position: relative;
  display: block;
  padding: 0.5rem 0;
  color: var(--cor-texto);
  text-decoration: none;
  font-weight: 500;
  transition: color var(--duracao-curta) var(--curva-padrao);
}

.menu a::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  height: 2px;
  background: var(--cor-secundaria);
  transform: scaleX(0);
  transform-origin: right;
  transition: transform var(--duracao-media) var(--curva-padrao);
}

.menu a:hover,
.menu a:focus-visible {
  color: var(--cor-secundaria);
}

.menu a:hover::after,
.menu a:focus-visible::after,
.menu a[aria-current="page"]::after {
  transform: scaleX(1);
  transform-origin: left;
}

.menu a[aria-current="page"] {
  color: var(--cor-primaria);
  font-weight: 600;
}

.menu__cta::after {
  display: none;
}
```

O item ativo (`aria-current="page"`, que cada página marca no seu próprio link desde a Aula 07) fica com o sublinhado permanente e não anima — ele **está** lá, não precisa chamar atenção.

### Passo 3 — cartões que se elevam

Os cartões de `programacao.html` e `palestrantes.html` (grade `.cartoes` da Aula 07) ganham elevação no hover e quando o link interno recebe foco.

**`css/estilo.css`** (seção 5 — componentes)

```css
.cartao {
  position: relative;               /* já existia: ancora o selo absolute */
  background: var(--cor-superficie);
  border-radius: var(--raio-borda);
  box-shadow: var(--sombra-cartao);
  overflow: hidden;                 /* corta o zoom da imagem */
  transition:
    transform var(--duracao-media) var(--curva-padrao),
    box-shadow var(--duracao-media) var(--curva-padrao);
}

.cartao:hover,
.cartao:focus-within {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.cartao__imagem {
  display: block;
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
  transition: transform var(--duracao-longa) var(--curva-padrao);
}

.cartao:hover .cartao__imagem,
.cartao:focus-within .cartao__imagem {
  transform: scale(1.05);
}

.cartao a:focus-visible {
  outline: 3px solid var(--cor-secundaria);
  outline-offset: 2px;
}
```

### Passo 4 — hero com gradiente sobre a imagem

A página inicial ganha uma seção de destaque com a foto do auditório ao fundo. Sem o gradiente, o título branco some nas partes claras da foto.

**`index.html`** (logo depois do `<header>`, dentro de `<main id="conteudo">`)

```html
<section class="hero" aria-labelledby="titulo-hero">
  <div class="container hero__conteudo">
    <p class="hero__chamada">Semana Acadêmica de Sistemas de Informação</p>
    <h1 id="titulo-hero">Três dias de palestras, minicursos e maratona de programação</h1>
    <p>Auditório da FACET · UNEMAT Sinop · vagas limitadas</p>
    <a href="inscricao.html" class="botao">Garanta sua vaga</a>
  </div>
</section>
```

**`css/estilo.css`** (seção 4 — layout)

```css
.hero {
  background:
    linear-gradient(rgba(11, 61, 92, 0.78), rgba(11, 61, 92, 0.78)),
    url("../img/banner.jpg") center / cover no-repeat;
  color: #ffffff;
  padding-block: clamp(3rem, 10vw, 7rem);
  text-align: center;
}

.hero__chamada {
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 0.875rem;
  opacity: 0.85;
}

.hero h1 {
  font-size: clamp(1.75rem, 4vw, 3rem);
  max-width: 20ch;
  margin-inline: auto;
}

.hero .botao {
  margin-top: var(--espaco-grande);
}
```

Usei a própria cor primária do evento (`#0b3d5c`) com 78 % de opacidade no lugar do preto: o resultado tem a identidade do site e ainda assim garante o contraste. Confira no WebAIM: branco sobre `#0b3d5c` passa com folga no nível AAA.

### Passo 5 — entrada escalonada dos cartões da programação

**`programacao.html`** (a lista de cartões existente; acrescente o `--i` em cada item)

```html
<ul class="cartoes">
  <li class="cartao" style="--i: 0">
    <img src="img/palestra-ia.jpg" alt="" class="cartao__imagem">
    <span class="cartao__selo">Palestra</span>
    <h3>Inteligência artificial no dia a dia do desenvolvedor</h3>
    <p>Como usar assistentes de código sem perder o controle do que você entrega.</p>
    <a href="#ia">Ver detalhes</a>
  </li>
  <li class="cartao" style="--i: 1">
    <img src="img/minicurso-git.jpg" alt="" class="cartao__imagem">
    <span class="cartao__selo">Minicurso</span>
    <h3>Git e GitHub do zero</h3>
    <p>Versionamento, branches e o primeiro pull request em três horas.</p>
    <a href="#git">Ver detalhes</a>
  </li>
  <li class="cartao" style="--i: 2">
    <img src="img/maratona.jpg" alt="" class="cartao__imagem">
    <span class="cartao__selo">Competição</span>
    <h3>Maratona de programação</h3>
    <p>Equipes de três, seis problemas, quatro horas. Inscrições por equipe.</p>
    <a href="#maratona">Ver detalhes</a>
  </li>
</ul>
```

**`css/estilo.css`** (seção 5 — componentes)

```css
@keyframes surgir {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

.cartoes .cartao {
  animation: surgir var(--duracao-longa) var(--curva-padrao) backwards;
  animation-delay: calc(var(--i, 0) * 80ms);
}
```

> **⚠️ Atenção**
> Enquanto a animação `surgir` está rodando, o `transform` dela vence o `transform` do `:hover` do Passo 3 — é a regra de cascata das animações. Como ela dura 400 ms e acontece só no carregamento, ninguém percebe. Mas se você fizer uma animação `infinite` com `transform` num cartão, o hover de elevação **para de funcionar**. Uma propriedade, um dono.

### Passo 6 — spinner no botão e esqueleto de palestrante a confirmar

Ainda não há JavaScript para "carregar" nada de verdade, mas o site já pode ter os dois componentes prontos. O spinner vira um estado do botão de inscrição (a Unidade 3 vai ativá-lo ao enviar o formulário); o esqueleto representa os palestrantes ainda não confirmados em `palestrantes.html`.

**`css/estilo.css`** (seção 5 — componentes; as animações `girar` e `brilho` da §5 precisam estar no arquivo)

```css
/* Botão em estado de carregamento: o texto some e um spinner ocupa o centro */
.botao--carregando {
  position: relative;
  color: transparent;
  pointer-events: none;
}

.botao--carregando::after {
  content: "";
  position: absolute;
  inset: 0;
  margin: auto;
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.4);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: girar 700ms linear infinite;
}

/* Cartão-esqueleto: mesmo tamanho de um cartão real, sem conteúdo */
.cartao--esqueleto {
  padding: var(--espaco-medio);
  display: grid;
  gap: var(--espaco-pequeno);
}

.esqueleto--foto {
  aspect-ratio: 16 / 9;
}

.esqueleto--linha {
  height: 1rem;
}

.esqueleto--curta {
  width: 60%;
}

/* Texto só para leitores de tela (se ainda não tiver este utilitário, adicione na seção 6) */
.visualmente-oculto {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
}
```

**`palestrantes.html`** (último item da grade `.cartoes`)

```html
<li class="cartao cartao--esqueleto" style="--i: 3">
  <span class="visualmente-oculto">Palestrante a confirmar</span>
  <div class="esqueleto esqueleto--foto" aria-hidden="true"></div>
  <div class="esqueleto esqueleto--linha" aria-hidden="true"></div>
  <div class="esqueleto esqueleto--linha esqueleto--curta" aria-hidden="true"></div>
</li>
```

**`inscricao.html`** (para testar o spinner, adicione a classe temporariamente ao botão de envio)

```html
<button type="submit" class="botao botao--carregando">Enviar inscrição</button>
```

O `aria-hidden="true"` nas caixas cinzas e o texto visualmente oculto fazem o leitor de tela anunciar "Palestrante a confirmar" em vez de silêncio ou de três caixas vazias. Depois de testar o spinner, remova a classe `botao--carregando` do botão.

### Passo 7 — o menu hambúrguer passa a deslizar

Na Aula 08 o menu no celular alternava entre `display: none` e `display: flex`. Esse é o caso clássico de "não anima". Você vai trocar por `opacity` + `visibility` + `transform`, mantendo o `js/menu.js` **exatamente como está** — ele só inverte o `aria-expanded`, e é o CSS que reage.

**`css/estilo.css`** (seção 4 — layout; **remova** as regras `.menu { display: none; }` e `.menu-botao[aria-expanded="true"] + .menu { display: flex; }` da Aula 08 e coloque estas no lugar)

```css
/* Celular: o menu fica ancorado logo abaixo do cabeçalho, fora de vista */
.menu {
  position: absolute;       /* em relação ao .cabecalho, que é sticky (Aula 07) */
  top: 100%;
  left: 0;
  right: 0;
  display: flex;
  flex-direction: column;
  gap: 0;
  padding: var(--espaco-medio);
  background: var(--cor-superficie);
  border-bottom: 1px solid var(--cor-borda);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  list-style: none;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-8px);
  transition:
    opacity var(--duracao-media) var(--curva-padrao),
    transform var(--duracao-media) var(--curva-padrao),
    visibility 0s var(--duracao-media);
}

.menu-botao[aria-expanded="true"] + .menu {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
  transition:
    opacity var(--duracao-media) var(--curva-padrao),
    transform var(--duracao-media) var(--curva-padrao),
    visibility 0s;
}

/* O ícone do botão gira 90° quando o menu está aberto */
.menu-botao__icone {
  display: inline-block;
  transition: transform var(--duracao-media) var(--curva-padrao);
}

.menu-botao[aria-expanded="true"] .menu-botao__icone {
  transform: rotate(90deg);
}
```

**`css/estilo.css`** (seção 7 — media queries; dentro do `@media (min-width: 768px)` já existente, substitua a regra do `.menu`)

```css
@media (min-width: 768px) {
  .menu {
    position: static;
    flex-direction: row;
    gap: 1.5rem;
    padding: 0;
    background: transparent;
    border: 0;
    box-shadow: none;
    opacity: 1;
    visibility: visible;
    transform: none;
    transition: none;
  }
}
```

Este é o "painel lateral" do item 7 da prática guiada: entra com `transform`, sai suavemente e o `visibility` garante que, fechado, os links não sejam alcançáveis por <kbd>Tab</kbd>.

### Passo 8 — revelação ao rolar em duas seções

**`index.html`** (as duas seções abaixo do hero recebem a classe `revelar`)

```html
<section class="container revelar" id="sobre" aria-labelledby="titulo-sobre">
  <h2 id="titulo-sobre">Sobre o evento</h2>
  <p>A Semana Acadêmica de Sistemas de Informação reúne estudantes, professores e profissionais do mercado em três dias de palestras, minicursos e competições no campus de Sinop.</p>
</section>

<section class="container revelar" id="numeros" aria-labelledby="titulo-numeros">
  <h2 id="titulo-numeros">A edição em números</h2>
  <ul class="numeros">
    <li><strong>12</strong> palestras</li>
    <li><strong>6</strong> minicursos</li>
    <li><strong>300</strong> vagas</li>
  </ul>
</section>
```

Crie o arquivo **`js/efeitos.js`** com o código da §8 (o `IntersectionObserver` que adiciona a classe `visivel`) e adicione as regras `.js .revelar` ao `css/estilo.css` (seção 6 — utilitários). Inclua o script no fim de `index.html`:

```html
<script src="js/menu.js" defer></script>
<script src="js/efeitos.js" defer></script>
```

### Passo 9 — bloco `prefers-reduced-motion` no fim da folha

Cole o bloco completo da §7 como **última** regra de `css/estilo.css`, depois de todas as media queries. Se ele ficar antes de alguma `transition` declarada mais abaixo, o `!important` ainda vence — mas a convenção "fica no fim" evita que alguém procure por ele no meio do arquivo.

### Passo 10 — auditoria no painel Performance

1. Abra `index.html` no Chrome, <kbd>F12</kbd> → painel **Performance**.
2. Na engrenagem, marque **CPU: 4× slowdown**.
3. Clique em **Record**, role a página do topo ao rodapé passando o mouse sobre os cartões, abra e feche o menu hambúrguer (redimensione para menos de 768 px antes), pare a gravação.
4. Observe o gráfico de **FPS** no topo: ele deve ficar verde e estável. Barras vermelhas indicam quadros perdidos.
5. Na faixa **Main**, procure blocos roxos de **Layout**. Durante as animações não deve haver nenhum — se houver, alguma transição está usando uma propriedade de layout.

### Como testar

- **Botões e links:** passe o mouse e navegue por <kbd>Tab</kbd>. Cada elemento interativo reage em até 250 ms, e o retorno do teclado é igual ao do mouse.
- **Menu:** em qualquer página, o sublinhado cresce da esquerda ao passar o mouse e recolhe pela direita ao sair; o item da página atual fica sublinhado o tempo todo.
- **Cartões:** recarregue `programacao.html` — os cartões surgem um após o outro, com 80 ms de intervalo. Depois disso, o hover eleva o cartão e amplia a imagem sem vazar da moldura.
- **Hero:** o título é legível em qualquer parte da foto; reduza a janela — o título e o espaçamento acompanham (`clamp`).
- **Esqueleto e spinner:** o último cartão de `palestrantes.html` "brilha"; o botão com `botao--carregando` mostra um círculo girando no lugar do texto.
- **Menu hambúrguer:** abaixo de 768 px, o menu desliza de cima em 250 ms ao clicar no botão e desaparece suavemente ao fechar. Com o menu fechado, <kbd>Tab</kbd> não entra nos links dele.
- **Revelação:** recarregue `index.html` e role — as seções "Sobre o evento" e "A edição em números" surgem subindo. Desative o JavaScript (DevTools → <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> → "Disable JavaScript") e recarregue: as seções aparecem normalmente, sem animação.
- **Movimento reduzido:** em Rendering, emule `prefers-reduced-motion: reduce`. Tudo passa a acontecer instantaneamente, mas nada some nem deixa de funcionar.
- **Performance:** a gravação com CPU 4× mostra FPS estável e nenhum bloco de Layout durante as animações.

**Resultado esperado:** o site do evento continua idêntico em estrutura, mas cada interação agora tem resposta visual suave, os cartões chegam em cascata, o hero é legível, o menu do celular desliza e ninguém que prefira menos movimento é prejudicado. Faça o commit com a mensagem `Aula 09: transições, animações e efeitos`.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Qual a diferença entre `transition` e `animation`? Quando usar cada uma?

**A2.** Escreva a transição de `background-color` e `transform` em 250 ms com curva `ease-out`, na forma abreviada.

**A3.** Por que `transition: all` é desaconselhado? Dê dois motivos.

**A4.** Explique cada uma das quatro propriedades da transição (`transition-property`, `transition-duration`, `transition-timing-function`, `transition-delay`).

**A5.** Diferencie `ease-in`, `ease-out` e `ease-in-out`, indicando quando usar cada uma.

**A6.** Por que `display: none` não pode ser transicionado? Qual a alternativa e como ela evita que o elemento escondido receba foco?

**A7.** Qual a diferença de resultado entre `transform: translateX(50px) rotate(45deg)` e `transform: rotate(45deg) translateX(50px)`? Desenhe.

**A8.** O que faz `transform-origin`? Dê um exemplo em que alterá-lo é necessário.

**A9.** Escreva um `@keyframes` que leve a opacidade de 0 a 1 e desloque o elemento 20 px para cima.

**A10.** O que faz `animation-fill-mode: forwards`? O que acontece sem ele?

**A11.** Qual a diferença entre `animation-direction: alternate` e `reverse`?

**A12.** Por que `transform` e `opacity` são as propriedades mais performáticas para animar? Cite as etapas do pipeline que cada grupo de propriedades dispara.

**A13.** Reescreva de forma performática: `.painel { top: -200px; transition: top 300ms; }` e o estado aberto `.painel.aberto { top: 0; }`.

**A14.** Para que serve `will-change`? Qual o risco de abusar dela?

**A15.** Escreva o bloco `prefers-reduced-motion` completo e explique por que ele usa `!important` e por que usa `0.01ms` em vez de `0`.

**A16.** Qual o limite de piscadas por segundo previsto na WCAG (critério 2.3.1) e por quê?

**A17.** Escreva um gradiente linear diagonal (135°) de `#0b3d5c` para `#1a7fb5`.

**A18.** Qual a diferença entre `box-shadow` e `filter: drop-shadow()`? Em que caso só o segundo funciona?

**A19.** Por que todo efeito de `:hover` deve ser replicado em `:focus-visible`? Qual a diferença entre `:focus` e `:focus-visible`?

**A20.** O que faz `backdrop-filter` e em que componente ele é tipicamente usado?

### Nível B — Aplicação

**B1.** Construa um botão completo com estados animados: normal, `:hover` (elevação), `:active` (pressionado), `:disabled` (opaco, sem transição) e `:focus-visible` (anel). Nenhum estado pode depender **só** de cor.

**Resultado esperado:** um botão que sobe no hover, afunda no clique, mostra um anel no foco por teclado e, desabilitado, fica opaco com cursor `not-allowed` — e cada estado é distinguível mesmo em uma captura de tela em preto e branco.

<details><summary>Dica</summary>

Declare a `transition` no estado base. Para o `:disabled`, use `transition: none` e `opacity: 0.5` — um botão desabilitado não deve "reagir" ao mouse. O anel de foco pode ser `outline` com `outline-offset` ou `box-shadow: 0 0 0 3px`.
</details>

**B2.** Faça um cartão giratório 3D para um palestrante: a frente mostra a foto e o nome; o verso mostra a mini-biografia e o link da palestra. O giro acontece no hover **e** também no foco por teclado.

**Resultado esperado:** o cartão vira em 600 ms com profundidade real; o verso não aparece espelhado; ao pressionar <kbd>Tab</kbd> até o link do verso, o cartão vira sozinho.

<details><summary>Dica</summary>

`perspective` no pai, `transform-style: preserve-3d` no elemento que gira, `backface-visibility: hidden` nas duas faces, e o verso começa com `rotateY(180deg)`. Use `:focus-within` no pai para o giro por teclado. O exemplo completo está na §3.
</details>

**B3.** Crie um spinner e um esqueleto de carregamento para uma listagem de 6 cartões. Simule o carregamento com um `setTimeout` de 2 segundos (o professor fornece o trecho de JavaScript de 4 linhas) e faça a transição do esqueleto para o conteúdo real.

**Resultado esperado:** ao abrir a página, seis cartões cinza "brilham" por 2 segundos e então desvanecem, dando lugar aos cartões reais, que surgem com `surgir`.

<details><summary>Dica</summary>

Tenha os dois conjuntos de cartões no HTML (esqueleto e real), com o real escondido por `opacity: 0; visibility: hidden`. O JavaScript apenas troca uma classe no contêiner após 2 s: `setTimeout(() => lista.classList.add("carregado"), 2000)`. O CSS faz o resto com `.carregado .esqueleto` e `.carregado .cartao`.
</details>

**B4.** Implemente um menu lateral (drawer) que entra da esquerda animando apenas `transform`, com sobreposição escura em `opacity`, fechamento pelo <kbd>Esc</kbd>, pelo clique fora e por botão, e com o foco preso dentro dele enquanto estiver aberto (o professor fornece o esqueleto do JavaScript; você faz todo o CSS).

**Resultado esperado:** o painel desliza em 300 ms; o fundo escurece junto; nenhuma barra de Layout aparece no painel Performance durante a abertura; com o painel fechado, seus links não recebem foco.

<details><summary>Dica</summary>

Painel: `position: fixed; inset: 0 auto 0 0; width: min(320px, 85vw); transform: translateX(-100%)`; aberto: `translateX(0)`. Sobreposição: `position: fixed; inset: 0; background: rgba(0,0,0,0.5); opacity: 0; visibility: hidden` com o truque do `visibility 0s 300ms`. Use a escala de z-index da Aula 07 (900 para a sobreposição, 1000 para o painel).
</details>

**B5.** Construa um acordeão animado com três itens: a altura anima suavemente, o ícone gira 180°, apenas um item fica aberto por vez, e o conteúdo fechado não é alcançável por teclado.

**Resultado esperado:** clicar em um título abre o conteúdo com deslizamento suave e fecha o que estava aberto; o "chevron" gira; <kbd>Tab</kbd> pula os conteúdos fechados.

<details><summary>Dica</summary>

Altura `auto` não transiciona. Duas saídas: usar `grid-template-rows: 0fr` → `1fr` no contêiner (com `overflow: hidden` no filho), que anima em navegadores modernos, ou `max-height` com um valor maior que o conteúdo. Para fechar os outros, use `<details name="acordeao">` com o mesmo `name` em todos, ou um pouco de JavaScript. Para o teclado, `visibility: hidden` no conteúdo fechado.
</details>

**B6.** Faça uma galeria de 6 fotos com efeito de zoom e legenda: a imagem amplia dentro da moldura, a legenda desliza de baixo para cima e um filtro de saturação é aplicado. Tudo reversível e suave.

**Resultado esperado:** ao passar o mouse (ou focar por teclado), a foto cresce 6 % sem vazar da moldura, ganha cor mais viva e a legenda sobe do rodapé da moldura; ao sair, tudo volta na mesma velocidade.

<details><summary>Dica</summary>

Moldura com `position: relative; overflow: hidden`. Legenda `position: absolute; bottom: 0; transform: translateY(100%)`, e `translateY(0)` no hover. Na imagem, `filter: saturate(1)` → `saturate(1.4)` e `transform: scale(1.06)`. Use `:focus-within` na moldura se a foto for um link.
</details>

**B7.** Implemente uma barra de progresso animada que vai de 0 % ao valor real ao entrar na viewport, com o número contando junto, usando `IntersectionObserver` (adapte o `js/efeitos.js`).

**Resultado esperado:** ao rolar até a seção "vagas preenchidas", a barra cresce de 0 a 72 % em 1,2 s e o texto passa de "0 %" a "72 %" ao mesmo tempo.

<details><summary>Dica</summary>

A barra é um `transform: scaleX(0)` com `transform-origin: left` que vai a `scaleX(var(--progresso))` quando ganha a classe `visivel` — é `transform`, portanto barato. O número contando é a única parte que precisa de JavaScript (um `setInterval` curto ou `requestAnimationFrame`); o professor fornece o trecho.
</details>

**B8.** Crie um conjunto de notificações (toasts) que entram deslizando pela direita, empilham-se, somem automaticamente após 4 segundos com animação de saída e podem ser fechadas manualmente.

**Resultado esperado:** um botão "Testar notificação" adiciona um toast no canto inferior direito; ele entra da direita, fica 4 s, e sai para a direita desvanecendo; três cliques rápidos empilham três toasts sem sobreposição.

<details><summary>Dica</summary>

Contêiner `position: fixed; bottom: 1rem; right: 1rem; display: flex; flex-direction: column; gap: 0.5rem`. Entrada com `@keyframes entrarDireita` (espelho de `entrarEsquerda`) e `animation-fill-mode: both`. A saída é outra classe (`.saindo`) com uma animação que leva a `translateX(120%)` e `opacity: 0`; remova o elemento no `animationend`.
</details>

**B9.** Anime a validação do formulário de inscrição: campo inválido treme e ganha borda vermelha; campo válido exibe um ícone de confirmação que surge com escala; a mensagem de erro desliza para baixo.

**Resultado esperado:** ao sair de um campo inválido (`:invalid` após interação, ou classe `.invalido`), ele treme 400 ms e fica vermelho com uma mensagem abaixo; um campo válido mostra um "✓" que cresce de `scale(0)` a `scale(1)` com ricochete.

<details><summary>Dica</summary>

Use a animação `tremer` da §5. Para não tremer antes de o usuário digitar, prefira `:user-invalid` (navegadores recentes) ou uma classe adicionada por JavaScript. O ícone pode ser um `::after` com `content: "✓"` e `transform: scale(0)` → `scale(1)` com `cubic-bezier(.34, 1.56, .64, 1)`. A mensagem de erro nasce com `opacity: 0; transform: translateY(-4px)`.
</details>

**B10.** Construa um carrossel de depoimentos com transição entre slides, indicadores clicáveis, avanço automático a cada 5 segundos, pausa no hover e no foco, e botão explícito de pausar.

**Resultado esperado:** três depoimentos alternam a cada 5 s com fade ou deslizamento; os três pontinhos abaixo indicam e escolhem o slide; passar o mouse ou focar qualquer coisa do carrossel interrompe o avanço; o botão "Pausar" vira "Continuar" e realmente para o relógio.

<details><summary>Dica</summary>

Faça a versão só com CSS primeiro: uma faixa `display: flex` com `transform: translateX(calc(var(--slide) * -100%))` e `transition: transform 500ms`. O avanço automático e o botão de pausa precisam de JavaScript (`setInterval` / `clearInterval` — o professor fornece). O botão de pausa é obrigatório pela WCAG 2.2.2 — sem ele, o exercício não está pronto.
</details>

### Nível C — Desafio

**C1.** **Página de apresentação animada.** Construa uma landing page de um produto (ou do próprio evento) com: hero com gradiente animado ao fundo e texto que entra escalonado; menu que muda de aparência ao rolar (fica compacto e ganha sombra); seções que se revelam por `IntersectionObserver`; contadores animados; galeria com zoom; depoimentos em carrossel; formulário com validação animada; rodapé com links de sublinhado animado. Requisitos: todas as animações usam apenas `transform` e `opacity` onde for possível, `prefers-reduced-motion` respeitado, e a página mantém 60 fps na gravação do painel Performance com CPU 4×. Comece em sala com o hero e o menu; o restante pode ser terminado em casa e reaproveita os exercícios B6, B7, B9 e B10.

<details><summary>Dica</summary>

O gradiente animado ao fundo é um `background-size: 200% 200%` com `@keyframes` deslocando `background-position` — barato o suficiente para um único elemento grande. O "menu que muda ao rolar" é uma classe `.compacto` adicionada pelo JavaScript quando `window.scrollY > 80`, e o CSS transiciona `padding` e `box-shadow` — aqui `padding` é aceitável porque muda uma vez, não a cada quadro. Faça a auditoria de performance no fim de **cada** seção, não só no fim da página.
</details>

## 🏆 Desafios

### ⭐ Caça ao bug: quatro animações que não animam

Tags: css, animacao, bug, devtools

Um colega enviou o CSS abaixo dizendo "nada anima, o CSS deve estar bugado". Não está — o navegador está fazendo exatamente o que foi pedido. Há **quatro** erros conceituais, cada um de um tipo diferente visto nesta aula. Encontre e corrija todos sem reescrever do zero: a intenção do colega deve ser preservada.

```css
.botao {
  background: #0b3d5c;
  color: #fff;
}
.botao:hover {
  background: #1a7fb5;
  transform: translateY(-2px);
  transition: all 200ms ease;
}

.cartao-3d {
  perspective: 1000px;
  transform-style: preserve-3d;
  transition: transform 600ms;
}
.cartao-3d:hover {
  transform: rotateY(180deg);
}

@keyframes aparecer {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
.destaque {
  animation: aparecer 500ms ease-out;
}

.painel {
  display: none;
  transition: opacity 300ms;
}
.painel.aberto {
  display: block;
  opacity: 1;
}
```

**Critérios de pronto**

- O botão entra **e sai** do hover suavemente, e a transição lista só as propriedades que mudam.
- O cartão 3D gira com profundidade visível (não "achatado"), com a perspectiva no elemento certo.
- O `.destaque` permanece visível depois que a animação termina.
- O `.painel` desvanece ao abrir e ao fechar, e fechado não recebe foco por teclado.
- Um comentário acima de cada correção diz, em uma linha, qual era o erro.

<details><summary>Pistas</summary>

1. Releia o callout **📌 Vale gravar** da §2: onde a `transition` deve ser declarada?
2. Na §3, `perspective` e `transform-style` ficam em elementos **diferentes** — qual vai no pai e qual no filho?
3. A §4 tem um callout inteiro sobre a propriedade que "quase todo mundo esquece".
4. A §2 mostra a dupla que substitui `display` quando você quer animar a entrada e a saída.
</details>

### ⭐ Movimento que degrada com elegância

Tags: css, animacao, acessibilidade, refatoracao

Ative `prefers-reduced-motion: reduce` no sistema (ou emule no DevTools) e abra qualquer site grande: a maioria simplesmente **remove** tudo, e junto some o feedback — o painel que deslizava agora aparece do nada, o toast que entrava pela direita simplesmente "está lá". Reduzir movimento não é remover comunicação. Pegue as animações abaixo, que são chamativas demais para quem tem sensibilidade vestibular, e reescreva o CSS para que, com movimento reduzido, cada uma seja substituída por um **fade** curto — sem depender do bloco `!important` genérico do fim da folha.

```css
@keyframes entrarGirando {
  from { opacity: 0; transform: translateX(-100vw) rotate(-360deg); }
  to   { opacity: 1; transform: translateX(0) rotate(0); }
}
.cartao-destaque { animation: entrarGirando 1.2s ease-out both; }

@keyframes saltar {
  0%, 100% { transform: translateY(0); }
  50%      { transform: translateY(-40px); }
}
.icone-atencao { animation: saltar 700ms ease-in-out infinite; }

.painel-lateral {
  transform: translateX(-100%);
  transition: transform 500ms cubic-bezier(.34, 1.56, .64, 1);
}
.painel-lateral.aberto { transform: translateX(0); }
```

**Critérios de pronto**

- Com movimento reduzido, o cartão de destaque **aparece com fade** de 200 ms, sem deslocamento nem rotação.
- O ícone de atenção não salta; em vez disso, muda de opacidade duas vezes e **para** (nada infinito).
- O painel lateral abre e fecha com fade de 200 ms, sem deslizar, e continua inalcançável por teclado quando fechado.
- Sem movimento reduzido, as três animações originais continuam funcionando.
- A solução usa a media query `prefers-reduced-motion` de forma **específica** por componente, e não `!important` em `*`.

<details><summary>Pistas</summary>

1. A media query pode redefinir o `@keyframes`? Não — mas pode trocar o `animation-name` do elemento por outro `@keyframes` só de opacidade.
2. Para o ícone, `animation-iteration-count: 2` dentro da media query resolve o "infinito"; a §7 explica por quê.
3. Para o painel, dentro da media query troque a `transition` por `opacity` + `visibility` (§2) e faça `transform: none` nos dois estados.
4. Teste com a emulação do DevTools ligada **e** desligada — as duas versões precisam funcionar.
</details>

**Para ir além:** transforme a técnica em uma convenção do seu projeto autoral: toda animação nova nasce com sua versão reduzida ao lado.

### ⭐⭐ `left` contra `transform`: meça, não acredite

Tags: css, performance, devtools, investigacao

Esta aula afirma que animar `transform` é mais barato que animar `left`. Você vai **provar** isso com números, do jeito que um engenheiro de front-end faz antes de discutir com o colega. Implemente o mesmo painel deslizante de duas formas: uma animando `left` (ou `width`), outra animando `transform`. Meça as duas com o painel Performance do DevTools, capture o número de quadros por segundo e o tempo gasto em Layout, e escreva um relatório de uma página comparando os resultados, com as capturas de tela como evidência. Repita o teste com a CPU limitada em 4× — é aí que a diferença aparece de verdade.

**Critérios de pronto**

- Duas páginas (`painel-left.html` e `painel-transform.html`) com o **mesmo** painel, o mesmo conteúdo (coloque pelo menos 200 elementos na página para o layout ter custo) e o mesmo botão de abrir/fechar.
- Quatro gravações do painel Performance: cada versão com CPU normal e com CPU 4×.
- O relatório (`relatorio.md` ou PDF de uma página) traz uma tabela com FPS mínimo e tempo total de Layout para as quatro gravações, as capturas, e uma conclusão de três linhas.
- O relatório explica, com suas palavras, **por que** a diferença existe (pipeline da §6).
- Bônus: repita no celular real usando a depuração remota do Chrome (`chrome://inspect`).

<details><summary>Pistas</summary>

1. No painel Performance, o resumo (aba **Summary**) mostra o tempo total de Rendering; a aba **Bottom-Up** mostra quanto foi Layout.
2. O gráfico de FPS fica no topo da gravação; passe o mouse sobre as barras vermelhas para ver a duração de cada quadro perdido.
3. Se a diferença não aparecer com CPU normal, não conclua que "é igual": aumente o número de elementos e ligue o 4×.
4. Grave só o trecho da animação (clique em Record, abra o painel, feche, pare) — gravações longas escondem o pico.
</details>

### ⭐⭐⭐ Sua biblioteca de animações

Tags: css, animacao, refatoracao, projeto

Bibliotecas como a Animate.css têm milhões de downloads por semana — e cabem em um arquivo CSS que você já sabe ler. Crie o seu `animacoes.css` com no mínimo 20 animações reutilizáveis, organizadas em quatro categorias (**entrada**, **saída**, **atenção** e **carregamento**), controladas por variáveis CSS (`--duracao`, `--atraso`, `--curva`) e aplicáveis por classe (`.anim-surgir`, `.anim-tremer`). Documente cada uma em uma página de demonstração com o código ao lado do exemplo funcionando e um controle deslizante (`<input type="range">`) que ajusta a duração ao vivo.

**Critérios de pronto**

- `animacoes.css` com ≥ 20 animações, cada uma em um `@keyframes` com nome em português descrevendo o movimento, e uma classe `.anim-*` que a aplica lendo `var(--duracao, 400ms)`, `var(--atraso, 0ms)` e `var(--curva, ease-out)`.
- Pelo menos 5 animações por categoria, e as de **atenção** têm `animation-iteration-count` finito por padrão.
- Todas usam apenas `transform`, `opacity` ou `background-position` — nenhuma anima propriedade de layout.
- O arquivo termina com o bloco `prefers-reduced-motion` que troca **todas** as entradas/saídas por fade (não por remoção).
- `demo.html` mostra cada animação com um botão "Reproduzir", o código-fonte ao lado (em `<pre><code>`) e um `<input type="range">` que altera `--duracao` no `:root` ao vivo (o professor fornece as 3 linhas de JavaScript).
- Um `README.md` explica como usar a biblioteca em qualquer projeto em 5 linhas.

<details><summary>Pistas</summary>

1. Para "reproduzir" uma animação de novo por clique, remova a classe, force um reflow (`void elemento.offsetWidth`) e adicione a classe de volta — esse é o truque clássico.
2. Variáveis CSS entram em `animation-duration: var(--duracao, 400ms)` normalmente; o valor de reserva garante que a classe funcione sem configuração.
3. Para a saída, `animation-fill-mode: forwards` é obrigatório — senão o elemento "volta" ao terminar.
4. Olhe a lista de nomes da Animate.css para não esquecer categorias inteiras (flip, zoom, slide, fade, bounce), mas escreva cada `@keyframes` você mesmo.
</details>

**Para ir além:** publique a biblioteca no GitHub Pages (Aula 15) e use-a no seu projeto autoral no lugar das animações soltas.

### 🔥 Boss — Projeto pronto para o Marco 2

Tags: css, layout, responsivo, animacao, projeto

Quatro aulas atrás o seu projeto autoral era HTML puro. Hoje ele tem um sistema de design, um layout de verdade, responde a qualquer tela e se move com propósito. O Boss desta unidade é fechar tudo isso em um site que você mostraria numa entrevista — e que é a base direta do Marco 2. Não há nada novo aqui: há tudo da Unidade 2, junto, funcionando ao mesmo tempo, no seu tema.

**Critérios de pronto**

- **Aula 06 — sistema de design:** `css/estilo.css` único, organizado nas 7 seções, com `:root` de pelo menos 12 variáveis (cores, espaçamentos, fonte, raio, sombra, durações, curva); nenhuma cor ou duração "solta" no meio do arquivo; contraste AA em todos os textos, incluindo o hero.
- **Aula 07 — layout:** estrutura da página em Grid com áreas nomeadas, componentes internos em Flexbox, cabeçalho sticky com `<nav aria-label>` em lista, `aria-current="page"` em cada página, link de salto funcionando, rodapé sempre no fim da janela; zero `float` e zero `position: absolute` para layout.
- **Aula 08 — responsividade:** mobile first com três breakpoints escolhidos pelo conteúdo (documentados em comentário), grade de cartões sem media query (`auto-fit`/`minmax`), imagens fluidas com `object-fit`, tipografia com `clamp()`, menu hambúrguer com `<button aria-expanded aria-controls>`, tema escuro via `prefers-color-scheme`.
- **Aula 09 — movimento:** transições em todos os elementos interativos (150–250 ms) com `:focus-visible` equivalente ao `:hover`; menu hambúrguer que desliza (`transform` + `opacity` + `visibility`); cartões com entrada escalonada e elevação; hero com gradiente; pelo menos duas seções com revelação ao rolar que **aparecem normalmente sem JavaScript**; bloco `prefers-reduced-motion` no fim da folha; nenhuma animação de propriedade de layout.
- **Qualidade:** Lighthouse (modo mobile) com Acessibilidade ≥ 90 e Boas práticas ≥ 90 em todas as páginas; gravação do painel Performance com CPU 4× sem quadros perdidos durante a rolagem e a abertura do menu; validador W3C sem erros (Aula 02).
- **Entrega:** capturas de cada página em 360 px, 768 px e 1440 px, a captura do Lighthouse e a do painel Performance, tudo numa pasta `evidencias/` no repositório.

<details><summary>Pistas</summary>

1. Use os checkpoints das Aulas 06, 07, 08 e 09 como lista de verificação, na ordem — a maioria dos itens você já fez; o Boss é o que falta e a integração.
2. Rode o Lighthouse **antes** de mexer em qualquer coisa e anote a nota: os itens de acessibilidade que ele aponta (contraste, nomes de botão, `alt`, ordem de títulos) são os mais rápidos de resolver.
3. A gravação de Performance sem quadros perdidos é o critério que mais reprova: procure `transition: all`, `box-shadow` animado em muitos elementos ao mesmo tempo e `will-change` espalhado.
4. Deixe o tema escuro por último e teste-o com o menu aberto, no hero e nos cartões — é onde as cores "fixas" que escaparam das variáveis aparecem.
</details>

**Para ir além:** peça a um colega que use o seu site **só pelo teclado** por dois minutos e anote onde ele se perdeu. Cada ponto anotado é um item do checklist de qualidade do Marco 2 que você acabou de garantir.

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| O hover entra suave, mas ao tirar o mouse o elemento "pula" de volta | `transition` declarada dentro de `:hover` — ao sair, a regra deixa de valer | Declare a `transition` no estado base do elemento (`.botao`), não no `:hover` |
| Ao acrescentar uma regra nova, coisas que não deviam animar passaram a animar (largura, margem) | `transition: all` anima qualquer propriedade que mude | Liste as propriedades explicitamente: `transition: transform 200ms, opacity 200ms` |
| A animação roda lisa no computador e engasga no celular; Performance mostra barras roxas de Layout a cada quadro | Animação de `width`, `left`, `top`, `margin` ou `height` | Reescreva com `transform` (`translate`/`scale`); confirme no painel Performance com CPU 4× |
| O elemento aparece com a animação e, quando ela termina, **some** ou volta ao estado inicial | Falta `animation-fill-mode` — o padrão `none` descarta o último quadro | `animation-fill-mode: forwards` (ou `both` em animações com atraso) |
| Cartões escalonados aparecem todos de uma vez e "piscam" quando chega a vez de cada um | `animation-delay` sem `backwards`: durante a espera o elemento fica no estado normal | `animation-fill-mode: backwards` (ou `both`) para aplicar o primeiro quadro durante o atraso |
| Micro-interação parece "lenta e arrastada" | Duração acima de 500 ms em hover, foco ou troca de cor | Reduza para 150–250 ms; reserve 300–500 ms para painéis e modais |
| Quem navega por <kbd>Tab</kbd> não vê nenhum retorno visual | Efeito só em `:hover`, sem `:focus-visible` (ou `:focus-within` no cartão) | Replique cada regra de `:hover` em `:focus-visible`; teste sem o mouse |
| Usuário relata tontura; o site ignora a opção "reduzir movimento" do sistema | Bloco `prefers-reduced-motion` ausente, ou declarado antes de outras regras sem `!important` | Cole o bloco completo da §7 no **fim** de `estilo.css` |
| A página ficou mais lenta depois de "otimizar" com `will-change` | `will-change` aplicado a dezenas de elementos cria dezenas de camadas na GPU | Use apenas no elemento que comprovadamente precisa; remova do restante |
| Animação infinita (spinner, pulsar) distrai e não pode ser parada | Sem controle de pausa, viola a WCAG 2.2.2 | Ofereça botão de pausa, ou limite as repetições; carrossel automático precisa de "Pausar" |
| O cartão 3D vira, mas parece achatado, sem profundidade; o verso aparece espelhado | `perspective` no próprio elemento que gira em vez do pai; falta `backface-visibility: hidden` | `perspective` no contêiner pai, `transform-style: preserve-3d` no que gira, `backface-visibility: hidden` nas faces |
| `transition: display 300ms` não faz nada; o painel aparece de repente | `display` não é interpolável | `opacity` + `visibility` com o atraso de `visibility 0s 300ms` na saída (§2) |
| A imagem de fundo do hero não aparece (`404` na aba Network) | Caminho relativo ao HTML usado dentro do CSS | Dentro de `css/estilo.css`, o caminho é relativo ao CSS: `url("../img/banner.jpg")` |
| Seções com `.revelar` ficam invisíveis quando o JavaScript está desativado ou com erro | CSS esconde `.revelar` incondicionalmente | Esconda apenas `.js .revelar`, com a classe `js` adicionada pelo próprio script |
| O hover de elevação do cartão parou de funcionar depois de adicionar uma animação | Duas regras disputam a mesma propriedade `transform`; a animação em execução vence | Não anime `transform` de forma infinita no mesmo elemento que usa `transform` no hover; ou anime um filho |

## 🏠 Para praticar depois da aula (1 h)

**Parte 1 — Leitura (15 min).** SILVA, Maurício Samy. *Criando sites com HTML*, capítulo sobre efeitos e transformações. MDN: *Using CSS transitions* e *Using CSS animations* (links em "Para aprofundar"). Anote uma coisa que a MDN explica e esta aula não.

**Parte 2 — Entrega (40 min).** Aplique ao **seu projeto autoral** a Mão na massa completa, com os dez requisitos:

1. Variáveis de movimento e transições em todos os elementos interativos (150–250 ms).
2. Menu com sublinhado animado e item ativo.
3. Cartões com elevação no hover, replicada em `:focus-within`.
4. Hero com gradiente sobre a imagem garantindo contraste AA.
5. Entrada escalonada dos cartões com `--i`.
6. Spinner e esqueleto de carregamento.
7. Menu hambúrguer (ou painel lateral) que abre com `transform` e sai suavemente.
8. Revelação ao rolar em duas seções, com `js/efeitos.js`.
9. Bloco `prefers-reduced-motion` no fim da folha.
10. Captura de tela do painel Performance (CPU 4×) mostrando a rolagem sem quedas de quadro, salva em `evidencias/performance.png`.

**Critério de pronto:** todos os dez itens presentes; emular `prefers-reduced-motion: reduce` no DevTools não esconde nem quebra nada; desativar o JavaScript não esconde nenhuma seção; a captura do painel Performance está no repositório.

**Parte 3 — Discussão (5 min).** Em texto próprio (ou no fórum da turma, se você cursa a disciplina): traga um site com movimento bem empregado e outro com movimento excessivo, explicando tecnicamente a diferença (o que cada animação comunica, duração, propriedade animada).

**Guarde no seu repositório:** commit + push (ou a pasta do projeto).

## ✅ Checkpoint do projeto

Ao fim desta aula — e da Unidade 2 — o repositório do seu projeto autoral precisa ter:

- [ ] `css/estilo.css` único, organizado nas 7 seções, com `:root` incluindo as variáveis de movimento (`--duracao-*`, `--curva-padrao`).
- [ ] Todos os botões, links, campos e cartões com transição entre 150 ms e 250 ms, e cada `:hover` com seu `:focus-visible`.
- [ ] Menu com sublinhado animado (`transform: scaleX` + `transform-origin`) e item ativo via `aria-current`.
- [ ] Hero com gradiente sobre imagem, título legível em qualquer ponto da foto, tamanhos com `clamp()`.
- [ ] Cartões com entrada escalonada (`--i` + `animation-delay` + `backwards`) e elevação no hover.
- [ ] Spinner (`@keyframes girar`) e esqueleto (`@keyframes brilho`) prontos no CSS, com texto para leitor de tela.
- [ ] Menu hambúrguer da Aula 08 animado com `opacity` + `visibility` + `transform`, sem `display: none`, e `js/menu.js` inalterado.
- [ ] `js/efeitos.js` com `IntersectionObserver` e pelo menos duas seções `.revelar` que aparecem mesmo sem JavaScript.
- [ ] Bloco `prefers-reduced-motion` completo como última regra do CSS.
- [ ] Nenhuma animação de `width`, `height`, `top`, `left` ou `margin`; nenhum `transition: all`; nenhum `will-change` sem justificativa.
- [ ] `evidencias/performance.png` com a gravação sem quedas de quadro.
- [ ] Tudo o que os checkpoints das Aulas 06, 07 e 08 pediam continua funcionando (design system, layout Grid/Flexbox, responsividade em três larguras, tema escuro).

## 📚 Para aprofundar

- MDN — Animações CSS: <https://developer.mozilla.org/pt-BR/docs/Web/CSS/CSS_animations> — o guia "Usando animações CSS" cobre `@keyframes`, o atalho `animation` e os eventos que a Unidade 3 vai usar.
- MDN — Transições CSS: <https://developer.mozilla.org/pt-BR/docs/Web/CSS/CSS_transitions> — leia a lista de propriedades animáveis e a seção sobre `transitionend`.
- MDN — Transformações CSS: <https://developer.mozilla.org/pt-BR/docs/Web/CSS/CSS_transforms> — a explicação da ordem das funções e de `perspective` com figuras.
- MDN — Media queries: <https://developer.mozilla.org/pt-BR/docs/Web/CSS/CSS_media_queries> — procure `prefers-reduced-motion` e `prefers-color-scheme`.
- web.dev — Learn CSS: <https://web.dev/learn/css> — os módulos *Transitions*, *Animations* e *Shadows* têm demonstrações interativas de cada curva.
- cubic-bezier.com: <https://cubic-bezier.com> — desenhe curvas e compare duas ao vivo antes de colar no projeto.
- W3C — WCAG 2.1, critérios 2.2.2 (Pausar, parar, ocultar) e 2.3.1 (Três flashes ou abaixo do limite): <https://www.w3.org/WAI/WCAG21/quickref/> — filtre por "2.2.2" e "2.3.1".
- Especificações do CSS Working Group: *CSS Transitions* e *CSS Animations* — para quando a MDN não responder um detalhe de comportamento.
- SILVA, Maurício Samy. *Criando sites com HTML: sites de alta qualidade com HTML e CSS*. Novatec, 2008 — capítulo de efeitos e transformações.
- TERUEL, Evandro C. *HTML 5 — Guia Prático*. Saraiva, 2014 — capítulo sobre CSS3 e efeitos visuais.

Isso encerra a Unidade 2. Em quatro aulas o seu site saiu de HTML puro para um sistema de design em variáveis, um layout de verdade com Grid e Flexbox, responsividade em qualquer tela e movimento que comunica sem atrapalhar. O **Marco 2** é exatamente esse site — o Boss desta aula é o roteiro para fechá-lo, e ele fecha na próxima aula. Na próxima aula você abre a Unidade 3 com a **Introdução ao JavaScript**: um `js/app.js` novo entra na pasta `js/` ao lado do `menu.js` (Aula 08) e do `efeitos.js` (hoje), e você começa a ler linha a linha o código que até agora colou "sem entender" — a leitura completa dos dois arquivos se fecha na Aula 13, com funções e eventos. O site deixa de ser só apresentação e começa a reagir ao usuário.
