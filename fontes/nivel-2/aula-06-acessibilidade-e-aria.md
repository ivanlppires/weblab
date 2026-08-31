# Aula 06 — Acessibilidade e ARIA

> **Nível 2 — Desenvolvimento Web** · Unidade 1: Web estática
> WebLab · UNEMAT Sinop · Prof. Ivan Luiz Pedroso Pires
> **Carga:** 3 aulas de 50 min (presencial) + 1 h (assíncrona)

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Explicar o que é acessibilidade web, quem se beneficia dela e o que a legislação brasileira exige de sites comerciais e públicos.
- Relacionar os quatro princípios das WCAG (perceptível, operável, compreensível, robusto) a decisões concretas de HTML e CSS, distinguindo os níveis A, AA e AAA.
- Descrever como uma tecnologia assistiva lê a página pela árvore de acessibilidade, identificando papel, nome acessível, estado e valor de cada elemento no DevTools.
- Medir contraste de cores com números e corrigir uma paleta reprovada, incluindo o indicador de foco.
- Tornar o site inteiramente operável por teclado: ordem de foco coerente, foco visível, `tabindex` usado corretamente e link de salto para o conteúdo.
- Aplicar ARIA onde o HTML nativo não basta — `aria-label`, `aria-labelledby`, `aria-describedby`, `aria-expanded`, `aria-controls`, `aria-current`, `aria-hidden` e regiões `aria-live` — e justificar quando **não** usar ARIA.
- Auditar o projeto com Lighthouse, WAVE e teste manual de teclado, alcançando nota de acessibilidade ≥ 90 e entendendo por que essa nota não é prova de site acessível.

## 📋 Pré-requisitos

- [ ] Repositório `cafe-cerrado` publicado no GitHub Pages, com `index.html`, `cardapio.html` e `contato.html`.
- [ ] Bootstrap 5.3 via CDN e `css/estilo.css` depois dele; landmarks `header`/`nav`/`main`/`footer` (Aula 03) e grid responsivo (Aula 04).
- [ ] Microinterações, logotipo em SVG inline, sprite de ícones e bloco `prefers-reduced-motion` (Aula 05).
- [ ] Seu projeto autoral no mesmo estágio, com `README.md` justificando a escolha do framework.
- [ ] Chrome ou Firefox com DevTools; hoje você usa **Lighthouse**, o painel **Accessibility** da aba Elements e a aba **Rendering**.
- [ ] Opcional, mas recomendado: NVDA instalado (Windows, gratuito), o VoiceOver do macOS/iOS, ou o TalkBack do seu Android.

> Na aula passada o Café Cerrado ganhou movimento e desenho vetorial: transições em tudo o que é clicável, cards em cascata, logotipo em SVG e respeito à preferência de movimento reduzido. Você já tomou, sem perceber, três decisões de acessibilidade — `aria-hidden` nos ícones decorativos, `focusable="false"` nos `<svg>` e `:focus-visible` nos botões. Hoje essas decisões deixam de ser intuição e viram método: você vai medir o que o site entrega a quem não usa mouse, não enxerga a tela ou não distingue cores, corrigir o que estiver quebrado e fechar a Unidade 1 com a auditoria do Lighthouse. Esta é também a aula que abre a **Avaliação 1**.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | O que é acessibilidade, quem se beneficia, a lei brasileira, WCAG e POUR; a árvore de acessibilidade no DevTools |
| 2 | 50 min | Contraste medido; teclado, foco visível e link de salto; ARIA (papéis, nomes, estados, regiões vivas); formulários acessíveis |
| 3 | 50 min | Mão na massa: auditoria e correção do Café Cerrado com Lighthouse e WAVE; Laboratório; instruções da Avaliação 1 |

## 1. Acessibilidade não é caridade

**Acessibilidade web** (abreviada como *a11y*) é a prática de construir sites que qualquer pessoa consegue usar — inclusive quem navega com leitor de tela, apenas teclado, comandos de voz, ampliador de tela ou dispositivos de apontamento adaptados.

A pergunta que a maioria dos estudantes faz na primeira aula do tema é "quantas pessoas realmente precisam disso?". O IBGE, no Censo Demográfico, contabiliza milhões de brasileiros com alguma deficiência — mas o número não é o argumento mais forte. O argumento mais forte é este:

| Tipo de limitação | Exemplo | Quem é |
|---|---|---|
| **Permanente** | Cegueira, surdez, ausência de um braço, dislexia | Uma parcela grande e constante do público |
| **Temporária** | Braço engessado, conjuntivite, otite, olho dilatado após exame | Você, algumas vezes na vida |
| **Situacional** | Sol forte na tela, ambiente barulhento, criança no colo, internet lenta | Você, hoje, várias vezes |

Um site que funciona com uma mão só serve tanto para quem perdeu um braço quanto para quem está segurando o café. Um vídeo com legenda serve tanto para quem é surdo quanto para quem está no ônibus sem fone. Acessibilidade não é um recurso extra para um grupo pequeno: é a diferença entre um site que funciona no mundo real e um que só funciona no seu notebook.

> **🧠 Você sabia?**
> Chama-se **efeito da rampa de calçada** (*curb-cut effect*). As rampinhas nas esquinas foram exigidas por ativistas cadeirantes nos Estados Unidos nos anos 1970, contra a resistência de prefeituras que as consideravam um gasto para poucos. Hoje quem mais usa rampa de calçada é quem empurra carrinho de bebê, carrinho de compras, mala de rodinha ou entrega de aplicativo. O mesmo aconteceu na web: a legenda de vídeo foi criada para pessoas surdas e virou padrão de consumo em qualquer lugar barulhento; a navegação por teclado foi criada para quem não usa mouse e virou a ferramenta preferida de quem programa. O acrônimo *a11y*, aliás, é um **numerônimo**: "a" + as 11 letras do meio de *accessibility* + "y".

### 1.1 O que a lei brasileira exige

A **Lei Brasileira de Inclusão** (Lei nº 13.146/2015), no artigo 63, determina que é obrigatória a acessibilidade nos sites mantidos por empresas com sede ou representação comercial no país e por órgãos do governo, segundo as melhores práticas e diretrizes de acessibilidade adotadas internacionalmente. O Decreto nº 5.296/2004 já exigia o mesmo dos portais públicos, e o governo federal mantém o **eMAG** (Modelo de Acessibilidade em Governo Eletrônico), que é a leitura brasileira das WCAG.

Traduzindo para a sua vida profissional: quando você entregar um sistema para uma prefeitura, um hospital, um banco ou qualquer empresa com CNPJ, acessibilidade não é um "extra que o cliente pode cortar do orçamento". É requisito legal, e cabe a você avisá-lo disso — por escrito, de preferência.

### 1.2 O efeito colateral bom

A mesma semântica que faz o leitor de tela entender a página faz o buscador entender a página. A mesma estrutura de títulos que ajuda quem navega por atalhos ajuda quem lê no celular. O mesmo contraste que serve a quem tem baixa visão serve a quem está no sol. Sites acessíveis costumam ser mais rápidos, melhor ranqueados e mais fáceis de manter — não por mágica, mas porque exigem HTML bem escrito, e HTML bem escrito é bom para tudo.

## 2. WCAG: as diretrizes e os quatro princípios

As **WCAG** (*Web Content Accessibility Guidelines*), do W3C, são o padrão mundial. A versão vigente é a 2.2. Elas se organizam em quatro princípios, lembrados pelo acrônimo **POUR**:

| Princípio | Pergunta-chave | Exemplos práticos |
|---|---|---|
| **Perceptível** | A pessoa consegue **perceber** o conteúdo? | `alt` em imagens, contraste suficiente, legenda em vídeo |
| **Operável** | Consegue **operar** a interface? | Tudo funciona por teclado, foco visível, sem limite de tempo |
| **Compreensível** | Consegue **entender**? | Idioma declarado, rótulos claros, erros explicados |
| **Robusto** | Funciona com **tecnologias assistivas**? | HTML válido e semântico, ARIA correto |

Cada princípio se desdobra em diretrizes, e cada diretriz em **critérios de sucesso** numerados (1.1.1, 1.4.3, 2.4.7…) e classificados em três níveis:

- **A** — mínimo. Sem isso, há gente que simplesmente não usa o site.
- **AA** — o nível exigido pela maioria das leis e contratos. **É a nossa meta na disciplina.**
- **AAA** — máximo. Nem sempre alcançável para todo tipo de conteúdo; o próprio W3C não recomenda exigi-lo como política geral.

Os critérios que mais aparecem no trabalho de vocês:

| Critério | Nível | O que exige |
|---|---|---|
| 1.1.1 Conteúdo não textual | A | Toda imagem tem alternativa textual |
| 1.3.1 Informação e relações | A | Estrutura visual também existe no código (títulos, listas, tabelas) |
| 1.4.3 Contraste (mínimo) | AA | 4,5:1 para texto normal, 3:1 para texto grande |
| 1.4.11 Contraste não textual | AA | 3:1 para bordas de campo, ícones e indicador de foco |
| 2.1.1 Teclado | A | Toda função é operável por teclado |
| 2.4.1 Ignorar blocos | A | Link de salto ou landmarks para pular o menu |
| 2.4.7 Foco visível | AA | Dá para ver onde o foco está |
| 3.3.2 Rótulos ou instruções | A | Todo campo de formulário tem rótulo |
| 4.1.2 Nome, função, valor | A | Cada controle expõe o que é, como se chama e em que estado está |

> **📌 Na prova**
> Decore a diferença entre os três níveis e os quatro princípios do POUR, e saiba dizer a qual princípio pertence cada prática que você aplicou no projeto. "Contraste" é *perceptível*; "foco visível" é *operável*; "idioma declarado" é *compreensível*; "ARIA correto" é *robusto*.

## 3. Como uma tecnologia assistiva lê a sua página

O leitor de tela não lê o seu HTML. Ele lê a **árvore de acessibilidade**, uma estrutura que o navegador constrói a partir do DOM, descartando o que é puramente visual e expondo, para cada nó que resta, quatro informações:

| Informação | Pergunta que responde | Exemplo |
|---|---|---|
| **Papel** (*role*) | O que é isto? | botão, link, campo de texto, cabeçalho, navegação |
| **Nome acessível** | Como isto se chama? | "Enviar mensagem", "Cardápio", "Café Cerrado" |
| **Estado** | Em que situação está? | expandido, marcado, desabilitado, página atual |
| **Valor** | Que conteúdo carrega? | o texto digitado, a posição de um controle deslizante |

Um `<button>Enviar</button>` chega à árvore com papel "button", nome "Enviar" e estado normal — de graça, sem nenhum atributo extra. Um `<div class="botao" onclick="…">Enviar</div>` chega com papel "genérico", sem nome, sem estado e sem foco. Visualmente idênticos; funcionalmente, o segundo não existe para quem não vê a tela.

O **nome acessível** é calculado por uma ordem de precedência que vale a pena guardar:

1. `aria-labelledby` (texto de outro elemento) — vence tudo.
2. `aria-label` (texto no próprio atributo).
3. O rótulo nativo: `<label for>` para campos, o `alt` para imagens, o conteúdo de texto para botões e links.
4. `title` — último recurso, não confiável, não aparece em toque.

> **🔬 Investigue**
> Abra o Café Cerrado, pressione <kbd>F12</kbd>, vá à aba **Elements** e selecione o link da marca na navbar. No painel lateral, abra a aba **Accessibility**. Você verá *Computed Properties* com o nome acessível calculado e, mais abaixo, a árvore de acessibilidade completa. Repita com: o botão do menu hambúrguer (tem nome?), um ícone SVG dentro de um card (aparece na árvore ou está escondido?) e um campo do formulário de contato. Anote qualquer elemento cujo nome apareça vazio ou como "" — cada um deles é um erro que o Lighthouse vai apontar no Passo 1 da Mão na massa.

## 4. A base que você já construiu

Boa notícia: quem seguiu as aulas anteriores já fez metade do trabalho. Agora essas práticas ganham nome, critério e verificação.

| Prática | Onde surgiu | O que conferir agora |
|---|---|---|
| `lang="pt-BR"` no `<html>` | Aula 02 | Presente nas três páginas |
| Landmarks `header`/`nav`/`main`/`footer` | Aula 03 | Um único `<main>` por página |
| `alt` em todas as imagens | Aula 03 | Descritivo no conteúdo, `alt=""` no decorativo |
| `<label for>` em todos os campos | Aula 03 | O `for` aponta para o `id` correto |
| Texto de link significativo | Aula 03 | Nada de "clique aqui" ou "saiba mais" solto |
| `aria-current="page"` no menu | Aula 03 | Só no item da página atual |
| Layout responsivo sem rolagem horizontal | Aula 04 | Testado em 360 px |
| `prefers-reduced-motion` | Aula 05 | Bloco presente no fim do CSS |
| `aria-hidden` e `focusable="false"` nos SVG | Aula 05 | Decorativos escondidos, informativos nomeados |

O que falta — e é o que esta aula acrescenta — são cinco camadas: **contraste medido**, **operação por teclado**, **link de salto**, **estados ARIA** e **auditoria**.

## 5. Contraste: pare de decidir cor no olho

A WCAG 1.4.3 exige razão de contraste de **4,5:1** para texto normal e **3:1** para texto grande (a partir de 24 px, ou 18,5 px em negrito). A 1.4.11 exige **3:1** para elementos não textuais que carreguem significado: borda de campo de formulário, ícone que comunica estado e — este é o mais esquecido — o **indicador de foco**.

A razão de contraste é um número entre 1:1 (mesma cor) e 21:1 (preto sobre branco). Ela é calculada a partir da luminância relativa de cada cor, o que significa que **você não consegue estimar no olho**: a mesma cor de destaque sobre o marrom da navbar e sobre o creme do conteúdo parece igualmente "legível" na sua tela calibrada, e nos dois casos ela reprova por motivos diferentes.

A paleta do Café Cerrado — a mesma do `:root` desde a Aula 02, sem uma cor a mais — medida par a par:

| Uso | Texto sobre fundo | Razão | Situação |
|---|---|---|---|
| Texto do corpo | `#2b2118` sobre `#fdfaf6` | 15,1:1 | Passa AAA |
| Rodapé | `#ffffff` sobre `#4a3325` | 11,7:1 | Passa AAA |
| Texto secundário | `#5c4b3c` sobre `#fdfaf6` | 8,0:1 | Passa AAA |
| Navbar | `#ffffff` sobre `#6f4e37` | 7,4:1 | Passa AAA |
| Link no corpo | `#6f4e37` sobre `#fdfaf6` | 7,2:1 | Passa AAA |
| Botão de destaque | `#ffffff` sobre `#c2703d` | 3,7:1 | **Reprova** (texto normal exige 4,5:1) |
| Anel de foco na navbar | `#c2703d` sobre `#6f4e37` | 2,0:1 | **Reprova** (1.4.11 exige 3:1) |
| Cinza "discreto" | `#9e9e9e` sobre `#ffffff` | 2,7:1 | **Reprova** |

Leia a tabela de baixo para cima, porque é ali que está a lição. As cinco primeiras linhas passam com folga: marrom escuro sobre creme e branco sobre marrom são combinações seguras, e foi por isso que ninguém percebeu nada de errado nas Aulas 02 a 05.

As três últimas são o padrão da turma inteira. O **botão de destaque** que você escreveu na Aula 02 (`background: var(--cor-destaque)` com texto branco) reprova por pouco — 3,7:1 onde a norma pede 4,5:1 — e "por pouco" não existe em acessibilidade. O **anel de foco** que você escreveu na Aula 05 com `var(--cor-destaque)` passa sobre o fundo claro do conteúdo (3,6:1, e o critério 1.4.11 pede 3:1) e reprova em cima da navbar marrom, que é justamente onde o `Tab` começa. E o cinza-claro que os tutoriais chamam de "texto secundário" é o erro de contraste mais comum da web — no Café Cerrado ele nem existe, porque `--cor-texto-suave` foi escolhido escuro o bastante.

Nenhum desses três defeitos é visível a olho nu. Todos os três aparecem no Lighthouse e no seletor de cor do DevTools. O Passo 6 do Mão na massa corrige os dois primeiros.

Três formas de medir:

1. **DevTools.** Inspecione o texto, clique no quadradinho de cor da propriedade `color` no painel Styles: o seletor mostra a razão de contraste com dois marcadores (AA e AAA) e desenha uma linha na paleta indicando até onde você pode escurecer.
2. **WebAIM Contrast Checker** (`webaim.org/resources/contrastchecker`): cole os dois hexadecimais e leia o veredito.
3. **Lighthouse**, que aponta todos os pares reprovados de uma vez, com o seletor CSS de cada um.

> **🔬 Investigue**
> Na aba **Rendering** do DevTools (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> → "Show Rendering"), procure *Emulate vision deficiencies* e escolha, uma de cada vez: *Blurred vision*, *Protanopia* (dificuldade com vermelho) e *Achromatopsia* (sem percepção de cor). Navegue pelo seu site em cada modo e responda por escrito: existe alguma informação que some? O botão "disponível" e o botão "esgotado" continuam distinguíveis? O link dentro de um parágrafo ainda é reconhecível como link? Se a resposta a alguma dessas perguntas for "não", você depende de cor como única portadora de significado — o que viola o critério 1.4.1.

## 6. Teclado: o teste que ninguém faz

Largue o mouse. Sério: tire a mão do mouse e navegue pelo seu site só com <kbd>Tab</kbd> (avançar), <kbd>Shift</kbd>+<kbd>Tab</kbd> (voltar), <kbd>Enter</kbd> (ativar links e botões), <kbd>Espaço</kbd> (marcar caixas e acionar botões) e as setas (dentro de grupos de rádio e listas). Três perguntas:

1. Consigo **alcançar** todos os links, botões e campos?
2. **Vejo** onde o foco está, a cada momento?
3. A **ordem** do foco segue a ordem visual da página?

Se qualquer resposta for "não", há gente que não usa o seu site — e não é pouca gente: além de quem tem limitação motora, é quem usa leitor de tela, quem opera por voz e quem simplesmente prefere teclado.

### 6.1 Foco visível

```css
/* Crime capital — nunca escreva isto sem substituto */
/* *:focus { outline: none; } */

/* Correto: um anel de dois tons, visível em fundo claro e em fundo escuro */
:focus-visible {
  outline: 3px solid var(--cor-marca-escura);
  outline-offset: 3px;
  box-shadow: 0 0 0 6px var(--cor-superficie);
  border-radius: 2px;
}
```

O anel de dois tons resolve um problema real: um anel de cor única sempre reprova em algum fundo — é exatamente o que a tabela da §5 mostrou sobre o anel da Aula 05. O escuro (`--cor-marca-escura`, 11,3:1 sobre o fundo claro) aparece nas seções de conteúdo; o halo claro (`--cor-superficie`, 7,4:1 sobre o marrom) aparece sobre a navbar. Juntos, garantem os 3:1 da 1.4.11 em qualquer lugar do site.

A diferença entre `:focus` e `:focus-visible` importa: `:focus` casa **sempre** que o elemento recebe foco, inclusive por clique de mouse (é por isso que designers pedem para "tirar aquele contorno"); `:focus-visible` casa quando o navegador julga que o indicador é útil — na prática, quando o foco veio do teclado. Estilize `:focus-visible` e o problema estético desaparece sem tirar o retorno de quem precisa.

### 6.2 `tabindex`, os três valores

| Valor | Efeito | Quando usar |
|---|---|---|
| `tabindex="0"` | Entra na ordem natural de tabulação | Elemento customizado que precisa ser focável |
| `tabindex="-1"` | Focável por script, fora da ordem do <kbd>Tab</kbd> | Alvo de um link de salto, modal que recebe foco |
| `tabindex="1"` ou mais | Fura a fila e vai para o começo | **Nunca.** Quebra a ordem de toda a página |

Valores positivos criam uma ordem paralela e frágil: basta acrescentar um campo esquecido para toda a sequência ficar sem sentido. Se você precisou de `tabindex="5"`, o problema está na ordem do HTML, não no atributo.

### 6.3 Link de salto (*skip link*)

Quem navega por teclado passaria pelos oito links do menu em **cada** página antes de chegar ao conteúdo. O link de salto resolve: é o primeiro elemento do `<body>`, invisível até receber foco.

```html
<body>
  <a class="link-pular" href="#conteudo">Pular para o conteúdo</a>
  <header>
    <nav aria-label="Navegação principal">Menu do site</nav>
  </header>
  <main id="conteudo" tabindex="-1">Conteúdo da página</main>
</body>
```

```css
.link-pular {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1100;
  padding: 0.75rem 1rem;
  background-color: var(--cor-marca-escura);   /* 11,7:1 com o texto branco */
  color: var(--cor-superficie);
  font-weight: 600;
  text-decoration: none;
  transform: translateY(-120%);
  transition: transform var(--duracao-rapida) var(--curva-entrada);
}

.link-pular:focus {
  transform: translateY(0);
}
```

Três decisões deliberadas nesse CSS:

- **`transform`, não `top: -50px`.** É a lição de desempenho da Aula 05 aplicada: o link é escondido pelo compositor, sem tocar no layout.
- **`:focus`, não `:focus-visible`.** Este link só é alcançado por teclado; ele precisa aparecer sempre que receber foco.
- **`tabindex="-1"` no `<main>`.** Sem ele, alguns navegadores movem apenas o ponto de partida da tabulação, e o leitor de tela continua narrando de onde estava. Com ele, o foco vai de fato para o conteúdo.

> **⚠️ Atenção**
> Nunca esconda o link de salto com `display: none` ou `visibility: hidden`: elementos assim não são focáveis, e o link deixa de existir para quem ele foi feito. A técnica correta é tirá-lo da área visível mantendo-o no fluxo — com `transform`, com `clip-path` ou posicionando-o fora da tela.

### 6.4 Esconder do jeito certo

Existem **três** formas de esconder algo, e elas não são intercambiáveis:

```css
/* 1. Some para todo mundo: olho e leitor de tela */
.escondido { display: none; }

/* 2. Visível para o olho, ignorado pelo leitor de tela (só para decoração) */
/* <svg aria-hidden="true"> */

/* 3. Invisível para o olho, disponível para o leitor de tela */
.oculto-visualmente {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
  border: 0;
}
```

A terceira serve para dar título a uma seção que visualmente não precisa dele, ou para completar o texto de um link (`Ver detalhes <span class="oculto-visualmente">do Espresso do Cerrado</span>`). O Bootstrap 5.3 já traz essa classe com o nome `visually-hidden` — use a dele se preferir, o efeito é o mesmo.

> **🔎 Por baixo do capô**
> Por que `clip-path: inset(50%)` e não `width: 0; height: 0`? Porque um elemento de dimensão zero é tratado como inexistente por vários motores e some da árvore de acessibilidade junto com o conteúdo. A receita acima mantém 1 pixel de área real, tira o conteúdo da visão por recorte e impede que o texto quebre linha (`white-space: nowrap`) — ela existe há mais de uma década e cada linha resolve um bug específico de um navegador. Copie-a inteira; não "otimize".

## 7. ARIA: quando o HTML não basta

**ARIA** (*Accessible Rich Internet Applications*) é um conjunto de atributos que enriquece o que as tecnologias assistivas enxergam: papéis (`role`), nomes (`aria-label`, `aria-labelledby`), descrições (`aria-describedby`), estados (`aria-expanded`, `aria-current`) e regiões que anunciam mudanças (`aria-live`).

### 7.1 A primeira regra do ARIA é: não use ARIA

Se um elemento HTML nativo resolve, use o nativo. `<button>` já é focável, ativável por <kbd>Enter</kbd> e <kbd>Espaço</kbd>, anunciado como botão e desabilitável. `<div role="button">` exige que você recrie tudo isso à mão — `tabindex`, tratador de teclado, estado desabilitado — e quase sempre sai pela metade.

```html
<!-- Errado: reinventa o botão e esquece metade do comportamento -->
<div class="btn" role="button" onclick="enviar()">Enviar</div>

<!-- Certo -->
<button class="btn btn-cafe" type="submit">Enviar</button>
```

> **⚠️ Atenção**
> **ARIA ruim é pior que ARIA nenhum.** Um `role` errado não deixa de funcionar: ele **mente** para o leitor de tela. Um `<a role="button">` que na verdade navega faz a pessoa esperar uma ação e receber uma mudança de página. Um `aria-expanded="false"` que nunca vira `true` faz o menu parecer permanentemente fechado. Na dúvida entre pôr um atributo ARIA e não pôr, não ponha.

### 7.2 Os atributos que você vai realmente usar

| Atributo | Função | Exemplo de uso |
|---|---|---|
| `aria-label` | Nome acessível para elemento sem texto visível | `<button aria-label="Fechar">✕</button>` |
| `aria-labelledby` | Nome vindo do texto de outro elemento | `<section aria-labelledby="titulo-cardapio">` |
| `aria-describedby` | Descrição complementar (ajuda, erro) | `<input aria-describedby="ajuda-email">` |
| `aria-hidden="true"` | Remove da árvore de acessibilidade | `<svg aria-hidden="true">` decorativo |
| `aria-expanded` | Estado aberto/fechado de um controle | `<button aria-expanded="false">` |
| `aria-controls` | Diz qual elemento o controle governa | `<button aria-controls="menu-principal">` |
| `aria-current="page"` | Item de navegação da página atual | `<a href="index.html" aria-current="page">` |
| `aria-live` | Região que anuncia mudanças de conteúdo | `<p aria-live="polite">` |

Duas armadilhas frequentes:

- **`aria-label` em elemento que já tem texto visível** sobrescreve o texto. Um `<a aria-label="Cardápio completo">Cardápio</a>` faz quem usa comando de voz dizer "clicar em Cardápio" e nada acontecer, porque o nome real virou outro. Se há texto visível, ele deve fazer parte do nome acessível.
- **`aria-hidden="true"` em elemento focável** cria um fantasma: o <kbd>Tab</kbd> para nele, mas o leitor de tela não tem o que anunciar. Nunca coloque `aria-hidden` em um `<a>`, `<button>` ou `<input>`, nem em um contêiner que os tenha dentro.

### 7.3 Regiões vivas: `aria-live`

Quando o conteúdo muda **sem** recarregar a página — uma mensagem de "enviado com sucesso", um contador de resultados de busca, um erro de validação — quem enxerga percebe na hora e quem usa leitor de tela não percebe nada, porque o foco não se moveu. A região viva resolve: o leitor de tela vigia aquele trecho e anuncia o que aparecer nele.

```html
<p class="status-envio" id="status-envio" aria-live="polite" aria-atomic="true"></p>
```

| Valor | Comportamento | Use para |
|---|---|---|
| `aria-live="polite"` | Espera a pessoa parar de digitar/ler e então anuncia | Confirmações, contagem de resultados |
| `aria-live="assertive"` | Interrompe imediatamente o que estava sendo lido | Erros graves, perda de dados |
| `aria-atomic="true"` | Lê a região inteira, não só o pedaço alterado | Mensagens curtas e completas |

Dois atalhos que fazem a mesma coisa com um `role`: `role="status"` equivale a `aria-live="polite"`, e `role="alert"` equivale a `aria-live="assertive"`. Declarar os dois é redundante — escolha um.

Duas regras que decidem se funciona:

1. **A região precisa existir no HTML desde o carregamento**, vazia. Se você criar o elemento e o texto ao mesmo tempo, muitos leitores não anunciam nada.
2. **Use com parcimônia.** Três regiões `assertive` competindo transformam o site num pregão.

O formulário do Café Cerrado ganha essa região hoje; ela permanece vazia até a Unidade 2, quando o JavaScript passará a escrever "Mensagem enviada, obrigado" ou "Confira o e-mail informado" dentro dela. Deixar a estrutura pronta agora é o que permite que a mudança lá na frente seja de três linhas.

### 7.4 Landmarks com nome

Leitores de tela oferecem um atalho para saltar entre **landmarks** — as regiões `banner` (`<header>` de página), `navigation` (`<nav>`), `main` (`<main>`), `contentinfo` (`<footer>` de página), `search` e `complementary` (`<aside>`). Se a página tem mais de um `<nav>`, cada um precisa de nome próprio, senão a lista fica com dois itens chamados "navegação".

```html
<nav aria-label="Navegação principal">
  <ul>
    <li><a href="index.html" aria-current="page">Início</a></li>
    <li><a href="cardapio.html">Cardápio</a></li>
  </ul>
</nav>

<footer>
  <nav aria-label="Links do rodapé">
    <ul>
      <li><a href="contato.html">Fale conosco</a></li>
      <li><a href="cardapio.html">Cardápio completo</a></li>
    </ul>
  </nav>
</footer>
```

Não escreva `aria-label="Navegação principal do site"`: o leitor já anuncia o papel ("navegação"), então repetir a palavra vira "navegação navegação principal do site". O nome deve ser curto e distintivo.

## 8. Formulários acessíveis

Formulário é onde a acessibilidade mais falha e onde ela mais importa — é o ponto em que a pessoa precisa **fazer** algo, não só ler.

```html
<form class="formulario-contato" action="#" method="post">
  <fieldset>
    <legend class="h5">Seus dados</legend>

    <div class="mb-3">
      <label class="form-label" for="nome">Nome completo</label>
      <input class="form-control" type="text" id="nome" name="nome"
             autocomplete="name" required aria-describedby="ajuda-nome">
      <p class="form-text" id="ajuda-nome">Como você quer ser chamado no atendimento.</p>
    </div>

    <div class="mb-3">
      <label class="form-label" for="email">E-mail</label>
      <input class="form-control" type="email" id="email" name="email"
             autocomplete="email" required aria-describedby="ajuda-email">
      <p class="form-text" id="ajuda-email">Usamos apenas para responder a esta mensagem.</p>
    </div>
  </fieldset>

  <fieldset class="mt-4">
    <legend class="h5">Assunto</legend>
    <div class="form-check">
      <input class="form-check-input" type="radio" name="assunto" id="assunto-reserva" value="reserva" checked>
      <label class="form-check-label" for="assunto-reserva">Reserva de mesa</label>
    </div>
    <div class="form-check">
      <input class="form-check-input" type="radio" name="assunto" id="assunto-evento" value="evento">
      <label class="form-check-label" for="assunto-evento">Evento no espaço</label>
    </div>
  </fieldset>

  <div class="mb-3 mt-4">
    <label class="form-label" for="mensagem">Mensagem</label>
    <textarea class="form-control" id="mensagem" name="mensagem" rows="5" required></textarea>
  </div>

  <button class="btn btn-cafe btn-enviar" type="submit" data-estado="pronto">Enviar mensagem</button>

  <p class="status-envio" id="status-envio" aria-live="polite" aria-atomic="true"></p>
</form>
```

O que cada decisão entrega:

- **`<label for>` ligado ao `id`**: dá nome ao campo e aumenta a área de clique — tocar no rótulo foca o campo, o que ajuda quem tem tremor ou usa a tela pequena.
- **`<fieldset>` + `<legend>`**: agrupa campos relacionados e dá um nome ao grupo. Em um grupo de rádios isso é obrigatório: sem `legend`, o leitor anuncia "Reserva de mesa, botão de opção, 1 de 2" sem nunca dizer **do que** é a escolha.
- **`autocomplete`**: além de poupar digitação, é um critério WCAG (1.3.5). Para quem tem dificuldade motora ou cognitiva, o preenchimento automático é a diferença entre concluir e desistir.
- **`required`**: aciona a validação nativa do navegador (Aula 03), que já é acessível e traduzida.
- **`aria-describedby`**: liga o texto de ajuda ao campo, de modo que ele seja lido **depois** do rótulo. Na Unidade 2, o mesmo atributo passará a apontar também para a mensagem de erro.
- **Região `aria-live` no fim**: pronta para receber o resultado do envio.

Duas coisas que **não** aparecem no código acima, de propósito:

- **`placeholder` como rótulo.** O texto do `placeholder` some quando a pessoa começa a digitar, tem contraste baixo por padrão e nem todo leitor de tela o anuncia. Ele serve como exemplo de formato, nunca como nome do campo.
- **Asterisco vermelho sozinho para "obrigatório".** Cor não pode ser a única portadora de significado (critério 1.4.1). Ou escreva "(opcional)" nos campos que não são obrigatórios, ou acrescente a palavra ao rótulo.

## 9. Auditoria: quatro ferramentas e um limite

| Ferramenta | Como usar | O que pega |
|---|---|---|
| **Lighthouse** | <kbd>F12</kbd> → aba Lighthouse → categoria *Accessibility* → *Analyze* | Contraste, `alt`, rótulos, ARIA inválido, com nota 0–100 |
| **WAVE** (`wave.webaim.org`) | Cole a URL do seu GitHub Pages | Erros e alertas desenhados sobre a própria página |
| **axe DevTools** | Extensão do Chrome/Firefox → aba *axe* | Auditoria detalhada com instrução de correção item a item |
| **Teste de teclado** | Manual: <kbd>Tab</kbd>, <kbd>Shift</kbd>+<kbd>Tab</kbd>, <kbd>Enter</kbd> | Foco invisível, elemento inalcançável, ordem quebrada |

E o leitor de tela, que não é uma quinta ferramenta e sim a prova real: NVDA (gratuito, Windows), VoiceOver (macOS/iOS, já instalado) ou TalkBack (Android). Feche os olhos por dois minutos e tente encontrar o preço do espresso no seu próprio site.

> **⚠️ Atenção**
> **Ferramentas automáticas detectam de 30 % a 40 % dos problemas de acessibilidade.** Nota 100 no Lighthouse não significa "site acessível": significa "os erros que uma máquina consegue detectar foram resolvidos". Nenhuma ferramenta sabe dizer se o seu `alt="imagem1.jpg"` descreve a foto, se a ordem do foco faz sentido ou se o rótulo "Clique aqui" é útil. O teste de teclado e o leitor de tela são insubstituíveis — e são justamente os itens da Avaliação 1 que o professor verifica à mão.

> **🧠 Você sabia?**
> A WebAIM publica todo ano o relatório *The WebAIM Million*, uma varredura automática da página inicial de um milhão de sites. Em todas as edições recentes, mais de **95 %** das páginas apresentaram falhas de WCAG detectáveis por máquina — e os erros mais comuns são sempre os mesmos quatro: contraste insuficiente, `alt` ausente, link sem texto discernível e campo de formulário sem rótulo. Ou seja: os quatro erros que você vai corrigir hoje, em uma tarde, colocam o seu site à frente da esmagadora maioria da web comercial.

## 💻 Mão na massa — Auditoria e correção do Café Cerrado

Este é um roteiro de auditoria: mede antes, corrige, mede depois. Trabalhe com o site publicado no GitHub Pages aberto em uma aba e o DevTools em outra.

### Passo 1 — Medir antes

Abra `index.html` no navegador, <kbd>F12</kbd> → aba **Lighthouse** → marque apenas a categoria *Accessibility*, modo *Navigation*, dispositivo *Mobile* → **Analyze**. Anote a nota e tire uma captura de tela. Repita em `cardapio.html` e `contato.html`.

Crie a pasta `evidencias/` no repositório e salve as três capturas como `lighthouse-antes-index.png`, `lighthouse-antes-cardapio.png` e `lighthouse-antes-contato.png`.

> **💡 Dica**
> Rode o Lighthouse em uma janela anônima, sem extensões. Extensões injetam elementos na página e produzem erros que não são seus.

### Passo 2 — Fundamentos do documento

Confira, nas três páginas, o topo do arquivo.

**`index.html`** (início)

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Café Cerrado — cafeteria artesanal em Sinop</title>
  <meta name="description" content="Cafeteria em Sinop com grãos do Cerrado mato-grossense, torra artesanal e espaço para trabalhar.">
  <link rel="icon" href="img/logo.svg">
</head>
```

Três verificações:

1. **`lang="pt-BR"`** faz o leitor de tela usar a pronúncia portuguesa. Sem ele, "café" vira "kaf" em voz inglesa.
2. **`<title>` único e descritivo em cada página.** É a primeira coisa anunciada ao abrir a aba. `cardapio.html` recebe `Cardápio — Café Cerrado`; `contato.html`, `Contato — Café Cerrado`. O padrão é "assunto da página — nome do site".
3. **`meta viewport` sem restrição de zoom.** Se em algum tutorial você copiou `user-scalable=no` ou `maximum-scale=1`, apague: impedir o zoom viola o critério 1.4.4 e prejudica quem tem baixa visão.

### Passo 3 — Landmarks e hierarquia de títulos

**`index.html`** (esqueleto do corpo)

```html
<body>
  <a class="link-pular" href="#conteudo">Pular para o conteúdo</a>

  <header>
    <nav class="navbar navbar-expand-lg" aria-label="Navegação principal">Menu do site</nav>
  </header>

  <main id="conteudo" tabindex="-1">
    <h1>Café do Cerrado, torrado em Sinop</h1>

    <section aria-labelledby="titulo-sobre">
      <h2 id="titulo-sobre">Nossa história</h2>
      <p>Começamos em uma garagem no Setor Comercial, com um torrador de dois quilos.</p>
    </section>

    <section aria-labelledby="titulo-destaques">
      <h2 id="titulo-destaques">Destaques da semana</h2>
      <h3>Espresso do Cerrado</h3>
      <p>Dose curta, torra média, notas de chocolate.</p>
    </section>
  </main>

  <footer>
    <nav aria-label="Links do rodapé">Links secundários</nav>
    <p>Café Cerrado — Sinop, Mato Grosso.</p>
  </footer>
</body>
```

Regras que valem ponto na Avaliação 1:

- **Um `<h1>` por página**, e ele descreve a página, não o site inteiro.
- **Sem saltos na hierarquia**: depois de um `h2` vem `h3`, nunca `h4`. Títulos são a tabela de conteúdo pela qual quem usa leitor de tela navega; um salto é um capítulo faltando no índice.
- **Título nunca é escolhido por tamanho.** Se você quer um `h3` grande, use `class="h2"` do Bootstrap (que muda só a aparência) e mantenha a tag correta.
- **Cada `<section>` recebe nome**, via `aria-labelledby` apontando para o `id` do seu próprio título. Sem nome, a seção não aparece na lista de regiões.

> **📌 Na prova**
> `<section>` sem nome acessível **não** vira landmark: o navegador a trata como um contêiner genérico. É por isso que `aria-labelledby` aponta para o `id` do `<h2>` — o título vira o nome da região, sem repetir texto.

### Passo 4 — Link de salto nas três páginas

Cole o `<a class="link-pular">` como **primeiro** elemento do `<body>` das três páginas, e acrescente `id="conteudo" tabindex="-1"` ao `<main>` de cada uma. O CSS é o da §6.3.

**`css/estilo.css`**

```css
.link-pular {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1100;
  padding: 0.75rem 1rem;
  background-color: var(--cor-marca-escura);   /* 11,7:1 com o texto branco */
  color: var(--cor-superficie);
  font-weight: 600;
  text-decoration: none;
  transform: translateY(-120%);
  transition: transform var(--duracao-rapida) var(--curva-entrada);
}

.link-pular:focus {
  transform: translateY(0);
}

/* O alvo do salto não deve exibir anel de foco: quem chegou ali já sabe onde está */
main:focus {
  outline: none;
}
```

**Teste agora:** recarregue a página, pressione <kbd>Tab</kbd> uma vez. O link deve descer do topo. Pressione <kbd>Enter</kbd> e depois <kbd>Tab</kbd> de novo: o próximo foco tem de ser o primeiro link **dentro** do conteúdo, não o menu.

### Passo 5 — Corrigir o anel de foco da Aula 05

Na Aula 05 você escreveu `outline: 3px solid var(--cor-destaque)`. Meça os dois fundos em que esse anel aparece:

- sobre o fundo claro das seções (`#c2703d` sobre `#fdfaf6`): **3,6:1** — passa, porque o critério 1.4.11 exige 3:1 para o indicador de foco;
- sobre a navbar marrom (`#c2703d` sobre `#6f4e37`): **2,0:1** — **reprova**. E a navbar é o primeiro lugar onde o <kbd>Tab</kbd> chega.

Uma cor sozinha não resolve: não existe tom que fique a 3:1 do creme **e** a 3:1 do marrom. A saída é o anel de dois tons.

**`css/estilo.css`**

```css
/* Anel de foco global: escuro por dentro, claro por fora, visível em qualquer fundo */
:focus-visible {
  outline: 3px solid var(--cor-marca-escura);   /* 11,3:1 sobre o fundo claro */
  outline-offset: 3px;
  box-shadow: 0 0 0 6px var(--cor-superficie);
  border-radius: 2px;
}

/* Dentro da navbar escura, inverte as duas camadas */
.navbar :focus-visible {
  outline-color: var(--cor-superficie);         /* 7,4:1 sobre o marrom da marca */
  box-shadow: 0 0 0 6px var(--cor-marca-escura);
}
```

Repare que isto **substitui** a regra de foco da aula passada. Apague a antiga (`.btn:focus-visible, .nav-link:focus-visible, .rodape a:focus-visible`): duas regras de foco disputando é a origem clássica de "no meu computador aparece e no seu não".

### Passo 6 — Corrigir o contraste

Rode o Lighthouse de novo e leia os itens de contraste. Para cada par reprovado, decida entre escurecer o texto ou escurecer o fundo — nunca "aumentar a fonte para virar texto grande", que é como se burla a regra.

O par reprovado do Café Cerrado é um só, e vem lá da Aula 02: `--cor-destaque` (`#c2703d`) como fundo de botão com texto branco dá **3,7:1**, e texto normal exige 4,5:1. A correção é escurecer o fundo até passar — sem trocar a família de cor, para a identidade visual não mudar. Acrescente **uma** variável ao `:root` e use-a em tudo que leve texto sobre a cor de destaque:

**`css/estilo.css`**

```css
:root {
  /* … a paleta das Aulas 02 e 04 continua aqui, sem alteração … */
  --cor-destaque-escura: #a3521f;   /* 5,6:1 com o branco; 5,3:1 sobre o fundo claro */
}

/* Texto sobre a cor de destaque: sempre a versão escura */
.btn-destaque,
.badge-destaque {
  background-color: var(--cor-destaque-escura);
  color: var(--cor-superficie);      /* 5,6:1 — passa AA com folga */
}

/* A cor de destaque original continua válida onde não carrega texto:
   bordas, ícones decorativos e o sublinhado do menu (só precisam de 3:1). */
.produto__preco {
  color: var(--cor-destaque-escura);  /* 5,3:1 sobre o fundo claro */
}

/* Texto secundário: nada de cinza-claro */
.texto-secundario {
  color: var(--cor-texto-suave);      /* 8,0:1 sobre o fundo claro */
}
```

> **🧠 Você sabia?**
> A diferença entre `#c2703d` e `#a3521f` é quase invisível lado a lado — e é a diferença entre reprovar e passar. Foi por isso que a §5 abriu com "pare de decidir cor no olho": a percepção humana de "mais escuro" não é linear, e a fórmula da luminância relativa da WCAG eleva cada canal a 2,4 justamente para corrigir isso.

Confirme cada número no seletor de cor do DevTools antes de commitar. A frase "está bom assim" não é evidência.

### Passo 7 — Navbar acessível

**`index.html`** (a navbar completa, repetida nas três páginas com o `aria-current` no item certo)

```html
<nav class="navbar navbar-expand-lg" aria-label="Navegação principal">
  <div class="container">
    <a class="navbar-brand d-flex align-items-center gap-2" href="index.html">
      <svg class="logo" viewBox="0 0 64 64" aria-hidden="true" focusable="false">
        <path d="M12 26h34v10a17 17 0 0 1-34 0z" fill="currentColor" />
        <path d="M46 28h4a7 7 0 0 1 0 14h-2" fill="none" stroke="currentColor" stroke-width="4" />
        <rect x="8" y="50" width="42" height="4" rx="2" fill="currentColor" />
      </svg>
      <span>Café Cerrado</span>
    </a>

    <button class="navbar-toggler" type="button"
            data-bs-toggle="collapse" data-bs-target="#menu-principal"
            aria-controls="menu-principal" aria-expanded="false"
            aria-label="Abrir e fechar o menu de navegação">
      <span class="navbar-toggler-icon" aria-hidden="true"></span>
    </button>

    <div class="collapse navbar-collapse" id="menu-principal">
      <ul class="navbar-nav ms-auto">
        <li class="nav-item">
          <a class="nav-link" href="index.html" aria-current="page">Início</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="cardapio.html">Cardápio</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="contato.html">Contato</a>
        </li>
      </ul>
    </div>
  </div>
</nav>
```

Cinco detalhes, um a um:

1. **`aria-label` no `<nav>`** nomeia o landmark. O rodapé tem outro `<nav>`, com nome diferente.
2. **`aria-label` no botão** é obrigatório porque o `navbar-toggler-icon` do Bootstrap é uma imagem de fundo em CSS: sem o rótulo, o botão chega à árvore com nome vazio, e o Lighthouse reporta *"Buttons do not have an accessible name"*.
3. **`aria-expanded="false"`** declara o estado inicial. O JavaScript do Bootstrap alterna esse atributo sozinho ao abrir e fechar — inspecione o botão no DevTools e clique nele para ver o valor mudar ao vivo. É o primeiro estado ARIA dinâmico que o seu projeto tem, e você não escreveu uma linha de JavaScript para isso.
4. **`aria-controls="menu-principal"`** aponta para o `id` do bloco que o botão governa. O `id` precisa existir e ser único na página.
5. **`aria-current="page"`** vai apenas no link da página atual — e é o mesmo atributo que o CSS da Aula 05 usa para manter o sublinhado aceso. Um atributo, dois usos.

> **🔬 Investigue**
> Reduza a janela até o menu virar hambúrguer. Selecione o botão no painel Elements e clique nele na página: veja `aria-expanded` alternando entre `"false"` e `"true"` no HTML ao vivo. Agora abra o painel **Accessibility** com o botão selecionado e leia o campo *Name* e a lista de estados. Por fim, feche o menu e pressione <kbd>Tab</kbd> a partir do botão: os links do menu fechado ainda recebem foco? Se sim, você encontrou um problema real — e a solução dele é justamente o que o componente `collapse` do Bootstrap faz com `display: none` no bloco fechado. Confirme no painel Computed.

### Passo 8 — Imagens, ícones e links

Passe por todas as imagens e ícones das três páginas com esta régua:

```html
<!-- Imagem que carrega informação: alt descreve o conteúdo, não o arquivo -->
<img src="img/espresso.jpg" alt="Xícara de espresso com creme dourado sobre mesa de madeira" class="card-img-top">

<!-- Imagem puramente decorativa: alt vazio, para o leitor pular -->
<img src="img/textura-grao.png" alt="" class="fundo-secao">

<!-- Ícone decorativo ao lado de texto que já informa -->
<svg class="icone" aria-hidden="true" focusable="false"><use href="#icone-relogio" /></svg>
Pronto em 2 min

<!-- Link cujo texto visível é curto demais fora de contexto -->
<a href="cardapio.html" class="btn btn-cafe">
  Ver detalhes<span class="oculto-visualmente"> do Espresso do Cerrado</span>
</a>
```

Quatro regras:

- **`alt` descreve a função da imagem naquele contexto**, não o arquivo. `alt="espresso.jpg"` e `alt="imagem"` são erros; `alt=""` em imagem decorativa é a resposta **certa**, não uma omissão.
- **Imagem dentro de link sem texto**: o `alt` vira o nome do link. Nesse caso ele descreve o **destino** ("Cardápio completo"), não a figura.
- **Ícone decorativo** recebe `aria-hidden="true"` — você já fez isso na Aula 05; confirme que não escapou nenhum.
- **Texto de link significativo fora de contexto.** Quem usa leitor de tela pode pedir a lista de todos os links da página; seis itens chamados "Ver detalhes" são inúteis. A classe `.oculto-visualmente` completa o nome sem mudar o visual.

### Passo 9 — Formulário de contato

Substitua o formulário de `contato.html` pela versão da §8, incluindo `<fieldset>`/`<legend>`, `autocomplete`, `aria-describedby` e a região `aria-live` vazia no fim. Acrescente o CSS da região:

**`css/estilo.css`**

```css
.status-envio {
  margin-top: 1rem;
  min-height: 1.5rem;          /* reserva o espaço: o texto não empurra o layout ao aparecer */
  font-weight: 600;
}

.status-envio:empty {
  margin-top: 0;
}

/* Campo obrigatório: a marca não é só cor */
.form-label .obrigatorio {
  color: var(--cor-marca-escura);
  font-weight: 700;
}
```

E a classe de conteúdo só para leitor de tela, que o Passo 8 já usou:

```css
.oculto-visualmente {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
  border: 0;
}
```

### Passo 10 — Tabela do cardápio

A tabela da Aula 03 precisa de duas coisas que quase todo mundo esquece: uma legenda e o escopo dos cabeçalhos.

**`cardapio.html`**

```html
<table class="table table-striped caption-top">
  <caption>Cafés quentes: preços em reais, atualizados semanalmente.</caption>
  <thead>
    <tr>
      <th scope="col">Item</th>
      <th scope="col">Descrição</th>
      <th scope="col">Preço</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Espresso do Cerrado</th>
      <td>Dose curta, torra média, notas de chocolate</td>
      <td>R$ 6,00</td>
    </tr>
    <tr>
      <th scope="row">Coado da Casa</th>
      <td>Coador de papel, moagem média na hora, 200 ml</td>
      <td>R$ 8,50</td>
    </tr>
    <tr>
      <th scope="row">Cappuccino Sinop</th>
      <td>Espresso duplo, leite vaporizado e canela do Cerrado</td>
      <td>R$ 12,00</td>
    </tr>
    <tr>
      <th scope="row">Cold Brew da Chapada</th>
      <td>Extração a frio de 18 horas, servido com gelo</td>
      <td>R$ 15,00</td>
    </tr>
  </tbody>
</table>
```

`<caption>` dá nome à tabela na lista de tabelas do leitor de tela. `scope="col"` e `scope="row"` dizem a que cabeçalho cada célula pertence, para que a leitura seja "Coado da Casa, Preço, R$ 8,50" em vez de "R$ 8,50" solto. A classe `caption-top` do Bootstrap coloca a legenda acima da tabela; sem ela, o Bootstrap a exibe embaixo.

### Passo 11 — Passar o site inteiro pelo teclado

Sem mouse, nas três páginas, percorra este roteiro e anote cada falha:

1. <kbd>Tab</kbd> uma vez: o link de salto aparece.
2. <kbd>Enter</kbd> nele: o foco vai para o conteúdo.
3. <kbd>Tab</kbd> até o fim da página: cada parada é visível e faz sentido na ordem visual.
4. No celular emulado, <kbd>Enter</kbd> no botão do menu abre o menu e o foco seguinte entra nos links dele.
5. No formulário, <kbd>Tab</kbd> percorre os campos na ordem, as setas trocam a opção de rádio e <kbd>Enter</kbd> envia.
6. Nenhuma parada invisível, nenhum elemento inalcançável, nenhuma armadilha (lugar de onde o <kbd>Tab</kbd> não sai).

### Passo 12 — Medir depois e registrar

Rode o Lighthouse novamente nas três páginas, salve as capturas como `lighthouse-depois-*.png` em `evidencias/` e cole a URL do GitHub Pages no WAVE (`wave.webaim.org`). Depois registre o resultado:

**`README.md`** (nova seção)

```markdown
## Acessibilidade

Auditoria da Unidade 1 (Lighthouse, categoria Accessibility, modo mobile).

| Página | Nota antes | Nota depois |
|---|---|---|
| index.html | 72 | 100 |
| cardapio.html | 68 | 96 |
| contato.html | 64 | 100 |

As três principais correções:

1. Contraste do texto secundário: o cinza claro sobre creme dava 2,7:1 e foi trocado
   pelo marrom de texto suave (8,0:1), acima do mínimo de 4,5:1 da WCAG 1.4.3.
2. Botão do menu sem nome acessível: recebeu `aria-label`, porque o ícone do
   Bootstrap é imagem de fundo e não gera texto.
3. Link de salto ausente: adicionado como primeiro elemento do body das três
   páginas, com `tabindex="-1"` no `<main>` de destino.

Testes manuais: navegação completa por teclado nas três páginas e leitura da
página inicial com o NVDA.
```

Substitua os números pelos **seus** — inventar nota é plágio de dados, e o professor roda o Lighthouse na correção.

### Como testar

- **Lighthouse:** as três páginas com Acessibilidade ≥ 90 em modo mobile, janela anônima.
- **WAVE:** zero *Errors*; *Alerts* podem existir, mas você precisa saber explicar cada um.
- **Teclado:** o roteiro do Passo 11 percorrido inteiro sem uma única falha.
- **Foco:** cada parada do <kbd>Tab</kbd> mostra o anel de dois tons, inclusive sobre a navbar escura.
- **Link de salto:** aparece na primeira tabulação e leva o foco ao `<main>`.
- **Menu:** o `aria-expanded` do botão alterna ao abrir e fechar; o `aria-current="page"` está no item certo de cada página.
- **Contraste:** nenhum par reprovado no Lighthouse; o seletor de cor do DevTools confirma os valores da tabela do Passo 6.
- **Árvore de acessibilidade:** nenhum botão, link ou campo com nome vazio no painel Accessibility.
- **Leitor de tela:** com o NVDA (ou VoiceOver/TalkBack), a página inicial é compreensível de olhos fechados: você chega ao cardápio e descobre o preço de um item.
- **Movimento reduzido:** emular `prefers-reduced-motion: reduce` continua sem esconder nem quebrar nada.

**Resultado esperado:** o Café Cerrado passa a ser utilizável por quem não usa mouse, por quem não vê a tela e por quem não distingue cores — com evidência numérica disso no `README.md` e nas capturas em `evidencias/`. A Unidade 1 está fechada. Faça o commit com a mensagem `Aula 06: acessibilidade, ARIA e auditoria` e o push.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** O que significa a sigla *a11y* e por que ela é escrita assim?

**A2.** Cite os quatro princípios das WCAG e escreva uma prática de código para cada um.

**A3.** Qual a diferença entre os níveis A, AA e AAA? Qual é a meta desta disciplina e por quê?

**A4.** Um leitor de tela lê o DOM ou a árvore de acessibilidade? Quais são as quatro informações que ele obtém de cada nó?

**A5.** Liste, em ordem de precedência, as quatro fontes possíveis do nome acessível de um elemento.

**A6.** Qual a razão de contraste mínima da WCAG AA para texto normal, texto grande e indicador de foco? Cite o critério de cada uma.

**A7.** Por que `#c2703d` passa no critério 1.4.11 sobre `#fdfaf6` (3,6:1) e reprova sobre `#6f4e37` (2,0:1), se é a mesma cor?

**A8.** Qual a diferença entre `:focus` e `:focus-visible`? Em qual dos dois o link de salto deve ser estilizado, e por quê?

**A9.** Explique os três valores possíveis de `tabindex` e diga qual deles nunca deve ser usado.

**A10.** Escreva o HTML e o CSS mínimos de um link de salto funcional, incluindo o que o elemento de destino precisa ter.

**A11.** Cite as três formas de esconder conteúdo e diga o efeito de cada uma para o olho e para o leitor de tela.

**A12.** Qual é a primeira regra do ARIA? Reescreva `<div role="button" onclick="enviar()">Enviar</div>` corretamente.

**A13.** Para que servem `aria-label`, `aria-labelledby` e `aria-describedby`? Dê um caso de uso de cada.

**A14.** O que acontece quando você coloca `aria-hidden="true"` em um `<button>`? Por que isso é pior do que não colocar nada?

**A15.** Diferencie `aria-live="polite"` de `aria-live="assertive"` e diga qual `role` equivale a cada um.

**A16.** Por que uma região `aria-live` precisa existir no HTML, vazia, desde o carregamento da página?

**A17.** Por que `<section>` sem nome acessível não vira landmark? Como dar nome a ela sem repetir texto na tela?

**A18.** Por que `placeholder` não substitui `<label>`? Dê três motivos.

**A19.** Para que servem `<fieldset>` e `<legend>`? Em que tipo de campo eles são indispensáveis?

**A20.** Que porcentagem dos problemas de acessibilidade as ferramentas automáticas detectam? O que isso implica para a sua entrega da Avaliação 1?

### Nível B — Aplicação

**B1.** Audite uma página do seu projeto autoral com o Lighthouse, liste **todos** os erros apontados e corrija-os, registrando antes/depois em uma tabela.

**Resultado esperado:** nota de Acessibilidade ≥ 90 na página escolhida, com um documento (ou seção do `README.md`) listando cada erro, a causa e a correção aplicada.

<details><summary>Dica</summary>

Rode em janela anônima e modo mobile. Comece pelos erros de contraste e de rótulo: são os mais numerosos e os mais rápidos. Cada item do Lighthouse tem um link "Learn more" que leva à documentação com o trecho de código correto.
</details>

**B2.** Implemente o link de salto e o anel de foco de dois tons nas três páginas do seu projeto, e comprove com uma sequência de três capturas de tela do <kbd>Tab</kbd>.

**Resultado esperado:** primeira tabulação revela o link de salto; <kbd>Enter</kbd> move o foco para o conteúdo; o anel de foco é visível tanto sobre a área clara quanto sobre a navbar escura.

<details><summary>Dica</summary>

Se ao pressionar <kbd>Enter</kbd> o foco parecer não se mover, falta `tabindex="-1"` no `<main>`. Para capturar o estado de foco em uma imagem, use a ferramenta de captura do sistema com atraso de 3 s, ou force o estado `:focus` pelo botão `:hov` no painel Styles.
</details>

**B3.** Torne acessível o formulário do seu projeto: `<label for>` em todos os campos, `<fieldset>`/`<legend>` nos grupos, `autocomplete` correto, `aria-describedby` nas ajudas e uma região `aria-live` vazia para o resultado.

**Resultado esperado:** cada campo é anunciado com nome, tipo, obrigatoriedade e ajuda; nenhum `placeholder` faz o papel de rótulo; o Lighthouse não reporta nenhum campo sem rótulo.

<details><summary>Dica</summary>

A lista de valores válidos de `autocomplete` está na especificação HTML e na MDN — os mais usados são `name`, `email`, `tel`, `street-address`, `postal-code`. Para conferir o nome anunciado de cada campo, use o painel Accessibility com o campo selecionado.
</details>

**B4.** Encontre e corrija cinco problemas de acessibilidade em um site real que você usa. Documente cada um com captura de tela, o critério WCAG violado e o código corrigido (a correção é sua, no papel — você não vai publicar no site alheio).

**Resultado esperado:** um documento com cinco itens, cada um nomeando o critério (por número) e mostrando o "antes" real e o "depois" proposto.

<details><summary>Dica</summary>

Sites de comércio e de prefeituras costumam falhar em contraste, foco visível, `alt` e rótulo de campo de busca. Use o WAVE para localizar rápido, mas confirme cada achado à mão: nem todo alerta é erro.
</details>

**B5.** Substitua um componente do seu projeto que esteja feito com `<div>` por HTML nativo equivalente, e compare o antes e o depois na árvore de acessibilidade.

**Resultado esperado:** duas capturas do painel Accessibility, uma mostrando papel genérico e nome vazio, outra mostrando papel e nome corretos, sem nenhum atributo ARIA adicionado.

<details><summary>Dica</summary>

Os candidatos mais comuns são: `<div class="botao">` → `<button>`; `<div class="menu">` com `<div>` filhos → `<nav>` + `<ul>`/`<li>`; `<span class="titulo">` → `<h2>`; `<div class="card">` → `<article>`.
</details>

**B6.** Escreva os textos alternativos de seis imagens do seu projeto, sendo duas informativas, duas decorativas e duas dentro de links, e justifique cada escolha em uma linha.

**Resultado esperado:** uma tabela de três colunas — imagem, `alt` escolhido, justificativa — em que nenhuma das decorativas tem texto e nenhuma das que estão dentro de link descreve a figura em vez do destino.

<details><summary>Dica</summary>

O teste do telefone: se você estivesse descrevendo a página por telefone para alguém, você mencionaria essa imagem? Se não mencionaria, ela é decorativa e leva `alt=""`. Se mencionaria, o que você diria é o `alt`.
</details>

**B7.** Prepare a região `aria-live` do seu formulário e prove que ela funciona: com o leitor de tela ligado, escreva um texto dentro dela pelo Console do DevTools e confirme que a mensagem é anunciada sem que o foco se mova.

**Resultado esperado:** um vídeo curto, ou um relato escrito passo a passo, demonstrando que a alteração do conteúdo da região foi anunciada em voz alta.

<details><summary>Dica</summary>

No Console, `document.querySelector("#status-envio").textContent = "Mensagem enviada"` altera o conteúdo. Se nada for anunciado, quase sempre é porque a região foi criada junto com o texto, em vez de já existir vazia — ou porque o elemento estava com `display: none`.
</details>

### Nível C — Desafio em sala

**C1.** **Auditoria cruzada.** Em duplas, troque a URL do seu GitHub Pages com um colega. Cada um audita o site do outro em 25 minutos, produzindo um relatório com: nota do Lighthouse por página; três erros automáticos com o critério WCAG correspondente; três problemas que **só** o teste manual revelou (teclado, ordem de foco, `alt` inútil, texto de link inútil); e uma recomendação priorizada. Depois, cada um corrige o próprio site com base no relatório recebido e mede de novo. Entregue os dois relatórios e as notas antes/depois.

<details><summary>Dica</summary>

Reserve 10 minutos para as ferramentas automáticas e 15 para o teste manual — é o manual que encontra o que vale nota. Um bom relatório diz "o quê, onde, qual critério e como corrigir", nunca "o site tem problemas de acessibilidade".
</details>

**C2.** **Dez minutos de olhos fechados.** Ligue o NVDA (ou o VoiceOver/TalkBack), feche os olhos ou desligue o monitor e tente cumprir três tarefas no site de um colega: descobrir o preço de um item do cardápio; encontrar o telefone de contato; e chegar ao campo "Mensagem" do formulário. Cronometre cada tarefa e anote em que ponto você se perdeu.

<details><summary>Dica</summary>

No NVDA, <kbd>H</kbd> pula entre títulos, <kbd>D</kbd> entre landmarks, <kbd>K</kbd> entre links e <kbd>F</kbd> entre campos de formulário; <kbd>Insert</kbd>+<kbd>F7</kbd> abre a lista de elementos. Se você não conseguir navegar por títulos, o problema não é seu: é a hierarquia da página.
</details>

## 🏆 Desafios

### ⭐ Vinte minutos sem mouse

Tags: acessibilidade, investigacao, devtools

Desconecte o mouse. Fisicamente, do computador — ou desative o touchpad. Por vinte minutos você vai usar apenas o teclado: o seu site, o site da UNEMAT, o SIGAA e um site de comércio à sua escolha. A maior parte da turma desiste nos primeiros três minutos. Não desista: o que incomoda você por vinte minutos é o dia inteiro de alguém.

**Critérios de pronto**

- Um relato de uma página com quatro seções, uma por site, contando onde você travou e o que aconteceu.
- Para cada travamento, o critério WCAG correspondente identificado pelo número (2.1.1, 2.4.3, 2.4.7…).
- Uma lista dos atalhos que você descobriu ser preciso usar (<kbd>Tab</kbd>, <kbd>Shift</kbd>+<kbd>Tab</kbd>, <kbd>Espaço</kbd>, setas, <kbd>Home</kbd>/<kbd>End</kbd>) e de onde cada um foi necessário.
- Pelo menos **um** problema encontrado no seu próprio site, corrigido e commitado.
- Uma frase final respondendo: qual das quatro páginas foi a mais fácil, e o que ela fazia de diferente?

<details><summary>Pistas</summary>

1. Comece pelo seu site: você conhece a estrutura e vai perceber rápido o que falta.
2. Se o foco "sumir", pressione <kbd>Tab</kbd> mais uma vez e olhe a barra de status do navegador: ela mostra o destino do link focado mesmo quando não há indicador visual.
3. Menus suspensos que só abrem no `:hover` são armadilhas clássicas — não há hover no teclado.
4. Antes de acusar um site, confira se o problema não é uma extensão do seu navegador: repita em janela anônima.
</details>

**Para ir além:** repita cinco minutos usando apenas o teclado **e** com a tela apagada, com o leitor de tela ligado. A diferença de dificuldade entre as duas experiências é o conteúdo de um bom parágrafo no seu relato.

### ⭐⭐ ARIA que mente: conserte o componente

Tags: acessibilidade, html, refatoracao, bug

Um "desenvolvedor sênior" entregou este acordeão de perguntas frequentes para o Café Cerrado, orgulhoso do ARIA que usou. O componente é uma coleção de mentiras: os atributos afirmam coisas que o código não cumpre, e o resultado é pior para quem usa leitor de tela do que se não houvesse ARIA nenhum. Encontre **seis** problemas e reescreva o componente — de preferência com muito menos ARIA do que ele tem.

```html
<div class="faq" role="list">
  <div class="faq-item">
    <div class="faq-titulo" role="button" aria-expanded="true" aria-controls="resposta-1">
      Vocês têm opção sem lactose?
      <img src="img/seta.png" aria-hidden="true">
    </div>
    <div id="resposta-01" class="faq-resposta" style="display: none" aria-live="assertive">
      Sim: leite de aveia e de castanha, sem custo adicional.
    </div>
  </div>

  <div class="faq-item">
    <span class="faq-titulo" role="button" tabindex="3" aria-label="Clique aqui">
      Aceitam animais de estimação?
    </span>
    <div class="faq-resposta" style="display: none">
      Sim, na área externa coberta.
    </div>
  </div>
</div>
```

**Critérios de pronto**

- Os seis problemas listados por escrito, cada um com o critério WCAG ou a regra ARIA que viola.
- O componente reescrito e funcionando: abre e fecha por mouse, por <kbd>Enter</kbd> e por <kbd>Espaço</kbd>.
- Nenhum `role` que possa ser substituído por um elemento HTML nativo permanece no código.
- Nenhum `tabindex` positivo, nenhum `aria-controls` apontando para `id` inexistente, nenhum `aria-label` que apague texto visível.
- O estado aberto/fechado é anunciado corretamente pelo leitor de tela, e o conteúdo fechado não recebe foco.
- Um parágrafo explicando por que `aria-live="assertive"` estava errado ali.

<details><summary>Pistas</summary>

1. Existe um elemento HTML nativo que faz acordeão sem uma linha de JavaScript e sem nenhum ARIA — procure `details` e `summary` na MDN. Quanto do componente sobra depois dele?
2. Compare o valor de `aria-controls` com o `id` que existe de fato no documento. Leia caractere por caractere.
3. `aria-expanded="true"` combinado com `display: none` é uma contradição: o atributo diz "está aberto" e o CSS diz "está fechado".
4. Um `<img>` sem `alt` não é a mesma coisa que um `<img alt="">`; e uma seta que indica estado talvez nem devesse ser imagem.
5. O que `role="list"` exige dos filhos diretos? Consulte a WAI-ARIA APG antes de responder.
</details>

### ⭐⭐⭐ Auditoria de um serviço público brasileiro

Tags: acessibilidade, investigacao, devtools, projeto

A Lei Brasileira de Inclusão exige acessibilidade em sites de órgãos públicos desde 2015. Você vai verificar, com método, se um deles cumpre — e produzir um documento que poderia, de fato, ser protocolado. Escolha um serviço que você mesmo precisa usar: matrícula, agendamento de saúde, emissão de documento, consulta de processo, transporte público.

**Critérios de pronto**

- Uma **tarefa real** definida em uma frase ("agendar uma consulta", "emitir a segunda via"), executada do começo ao fim em três condições: com mouse, só com teclado, e com leitor de tela.
- Auditoria automática de pelo menos três páginas do fluxo (Lighthouse e WAVE), com os números registrados.
- Um mínimo de **oito** problemas documentados, cada um com: onde ocorre, o critério WCAG pelo número, a evidência (captura ou trecho de código) e o impacto real na tarefa.
- Os problemas classificados em três severidades, com o critério de classificação explicado — impedem, dificultam ou incomodam.
- Uma proposta de correção em código para os três mais graves.
- Uma seção final de meia página em linguagem não técnica, endereçada a quem decide (um gestor, não um programador), explicando o que está em jogo e citando o artigo 63 da Lei nº 13.146/2015.
- O documento publicado no repositório do seu projeto autoral, em `docs/auditoria-acessibilidade.md`.

<details><summary>Pistas</summary>

1. Defina a tarefa **antes** de abrir o site. Auditoria sem tarefa vira lista de avisos de ferramenta, que é exatamente o que ninguém lê.
2. Grave a tela nas três condições: você vai esquecer metade do que aconteceu, e o vídeo é a evidência mais convincente que existe.
3. Formulários de várias etapas concentram os piores problemas: campos sem rótulo, erro anunciado só em vermelho, tempo limite de sessão sem aviso (critério 2.2.1).
4. Severidade se mede pelo efeito na tarefa, não pelo susto: contraste ruim incomoda; `<div>` clicável que não recebe foco **impede**.
5. Para a seção final, escreva como se explicasse a um parente. Se aparecer a palavra "landmark", reescreva.
</details>

**Para ir além:** envie o documento pelo canal de ouvidoria do órgão. Não é retórica: relatórios bem escritos de estudantes já geraram correção em portais públicos, e o e-mail de resposta vale mais no seu currículo que o certificado do trabalho.

### 🔥 Boss — O seu site pronto para a Avaliação 1

Tags: html, css, acessibilidade, responsivo, projeto

Seis aulas atrás o seu projeto era uma pasta vazia e um repositório recém-criado. Hoje ele é um site de três páginas, semântico, responsivo, com framework CSS, identidade visual em SVG, movimento com propósito e utilizável por quem não vê a tela. O Boss desta unidade não traz nada novo: traz **tudo junto, funcionando ao mesmo tempo**, no seu tema — e é literalmente o roteiro da Avaliação 1.

**Critérios de pronto**

- **Aula 02 — fundamentos:** `lang="pt-BR"`, `<title>` único e descritivo por página, `meta viewport` sem restrição de zoom, pastas `css/`, `js/` e `img/` organizadas, HTML sem erros no validador do W3C.
- **Aula 03 — semântica e formulários:** landmarks `header`/`nav`/`main`/`footer` com um único `<main>` por página; hierarquia de títulos sem saltos; `alt` correto em todas as imagens; formulário completo com validação nativa; navegação entre as três páginas com `aria-current="page"`.
- **Aula 04 — framework CSS:** Bootstrap 5.3 (ou o framework escolhido) aplicado de forma consistente, com grid responsivo, navbar e cards; escolha justificada em um parágrafo do `README.md`; nenhuma rolagem horizontal em 360 px.
- **Aula 05 — animação e SVG:** microinterações em todos os elementos clicáveis, com `:focus-visible` equivalente ao `:hover`; ao menos uma animação `@keyframes` com propósito declarado; logotipo autoral em SVG inline e sprite com pelo menos três ícones; bloco `prefers-reduced-motion` como última regra do CSS; nenhuma animação de propriedade de layout.
- **Aula 06 — acessibilidade:** link de salto funcional; anel de foco visível em fundo claro e escuro; contraste AA em **todos** os textos, comprovado com números; `aria-label` nos dois `<nav>`; `aria-expanded`/`aria-controls` no botão do menu; região `aria-live` no formulário; Lighthouse ≥ 90 nas três páginas; teste de teclado completo aprovado.
- **Evidências:** pasta `evidencias/` com capturas do Lighthouse antes e depois de cada página, capturas do site em 360 px, 768 px e 1440 px, e a captura do estado de foco do link de salto.
- **README:** seções "Sobre o projeto", "Framework escolhido e por quê", "Movimento" e "Acessibilidade" (com a tabela antes/depois e as três principais correções).
- **Repositório:** público, com histórico de commits que mostre evolução aula a aula — não um único commit "projeto final" — e o site publicado e acessível pela URL do GitHub Pages.

<details><summary>Pistas</summary>

1. Use os checkpoints das Aulas 02 a 06 como lista de verificação, na ordem. A maior parte você já fez; o Boss é o que falta mais a integração.
2. Rode o Lighthouse **antes** de mexer em qualquer coisa e guarde a captura: metade da nota da seção de acessibilidade do `README.md` é essa comparação.
3. O item que mais reprova é o contraste, e o segundo é o texto de link inútil ("Saiba mais", "Clique aqui", "Ver detalhes" repetido seis vezes). Os dois são correções de minutos.
4. Peça a um colega que use o seu site **só pelo teclado** por dois minutos e anote onde ele se perdeu. Cada anotação é um ponto da rubrica que você acabou de garantir.
5. Deixe o `README.md` por último, mas não para a última hora: ele é o único lugar onde você defende as suas decisões, e decisões defendidas valem nota em três critérios diferentes.
</details>

**Para ir além:** peça a alguém de fora do curso — um parente, um colega de trabalho — para realizar uma tarefa no seu site sem nenhuma instrução sua ("descubra quanto custa um cappuccino"). Fique calado e cronometre. O que essa pessoa não achou em 30 segundos é o que o seu site esconde.

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| Lighthouse: *"Background and foreground colors do not have a sufficient contrast ratio"* | Texto claro sobre fundo claro (o clássico cinza sobre branco, ou a cor de destaque sobre o creme) | Meça no seletor de cor do DevTools e escureça o texto ou o fundo até passar de 4,5:1 |
| Lighthouse: *"Buttons do not have an accessible name"* | Botão cujo conteúdo é só ícone, imagem de fundo ou SVG com `aria-hidden` | `aria-label` descrevendo a **ação** ("Abrir o menu"), não o desenho |
| Lighthouse: *"Links do not have a discernible name"* | Link contendo só uma imagem sem `alt`, ou só um `<svg aria-hidden>` | `alt` descrevendo o **destino**, ou texto com `.oculto-visualmente` |
| Lighthouse: *"Form elements do not have associated labels"* | Campo com `placeholder` no lugar de `<label>`, ou `for` diferente do `id` | Um `<label for="x">` para cada `<input id="x">`; confira caractere por caractere |
| Lighthouse: *"Heading elements are not in a sequentially-descending order"* | `h2` seguido de `h4`, ou tag escolhida pelo tamanho da fonte | Corrija a tag e ajuste o tamanho por classe (`class="h2"` do Bootstrap) |
| Lighthouse: *"`<html>` element does not have a `[lang]` attribute"* | Modelo de HTML copiado sem o atributo | `<html lang="pt-BR">` nas três páginas |
| Lighthouse: *"`[user-scalable="no"]` is used in the `<meta name="viewport">`"* | Tutorial antigo copiado; impede o zoom | `<meta name="viewport" content="width=device-width, initial-scale=1">` |
| axe: *"aria-controls attribute must point to an element that exists"* | `aria-controls="resposta-1"` e o `id` real é `resposta-01` | Iguale os dois; `id` deve ser único na página |
| O <kbd>Tab</kbd> percorre a página em ordem maluca, pulando de um canto ao outro | `tabindex` com valores positivos criando uma fila paralela | Remova todos os positivos; a ordem correta vem da ordem do HTML |
| Não dá para ver onde o foco está em nenhum lugar do site | `*:focus { outline: none }` herdado de um reset ou de um tutorial | Apague a regra e declare `:focus-visible` com anel de dois tons |
| O <kbd>Tab</kbd> entra em links de um menu que está fechado | Menu escondido só com `opacity: 0` ou `height: 0` | Esconda com `display: none` ou `visibility: hidden` (a dupla da Aula 05) |
| O link de salto não aparece nunca, nem ao pressionar <kbd>Tab</kbd> | Escondido com `display: none` — elementos assim não são focáveis | Tire-o da vista com `transform` ou `clip-path`, e mostre no `:focus` |
| O link de salto aparece, mas <kbd>Enter</kbd> não parece levar a lugar nenhum | Falta `tabindex="-1"` no `<main id="conteudo">` | Acrescente o atributo ao alvo do salto |
| O leitor de tela anuncia "navegação" duas vezes e a pessoa não sabe qual é qual | Dois `<nav>` na página sem `aria-label` distinto | Nomeie cada um: "Navegação principal" e "Links do rodapé" |
| A mensagem de sucesso aparece na tela mas nada é anunciado | Região `aria-live` criada junto com o texto, ou dentro de um bloco com `display: none` | Deixe a região vazia no HTML desde o carregamento e só escreva o texto dentro dela |
| O leitor de tela lê o nome do link errado, diferente do texto que aparece | `aria-label` sobrescrevendo o texto visível | Se há texto visível, ele deve compor o nome — use `.oculto-visualmente` para complementar, não `aria-label` para substituir |
| O <kbd>Tab</kbd> para em um ponto onde nada é anunciado | `aria-hidden="true"` aplicado a um elemento focável ou ao contêiner de um | Nunca ponha `aria-hidden` em `<a>`, `<button>`, `<input>` nem em quem os contenha |

## 🏠 Atividade assíncrona (1 h)

**Parte 1 — Leitura (15 min).** QUEIRÓS e PORTELA, seção sobre a camada de comportamento — é a preparação para a Unidade 2, que começa na próxima aula. Leia também a página *Acessibilidade* da MDN em português e o texto do artigo 63 da Lei nº 13.146/2015 no portal do Planalto (são cinco linhas). Anote uma obrigação legal que você não sabia que existia.

**Parte 2 — Entrega (40 min).** No **seu projeto autoral**:

1. Rode o Lighthouse e o WAVE nas três páginas e registre as notas iniciais.
2. Corrija todos os erros apontados e execute o teste de teclado completo do Passo 11.
3. Adicione: link de salto, `aria-label` nos dois `<nav>`, `aria-current="page"` no item certo de cada página, `aria-hidden` em todos os SVG decorativos e a região `aria-live` no formulário.
4. Corrija o contraste de todos os pares reprovados, incluindo o indicador de foco.
5. Registre no `README.md` a seção "Acessibilidade" com a tabela de notas antes/depois e as três principais correções, no formato do Passo 12.
6. Finalize a **Avaliação 1** conforme as instruções da seção seguinte e entregue no SIGAA.

**Critério de pronto:** Lighthouse ≥ 90 nas três páginas; zero *Errors* no WAVE; teste de teclado percorrido sem falha; seção "Acessibilidade" no `README.md` com números reais; `evidencias/` com as capturas antes e depois.

**Parte 3 — Fórum (5 min).** No fórum "O que me surpreendeu sem mouse", conte em um parágrafo o momento mais difícil da sua navegação por teclado desta semana e o que você mudou no seu site por causa dele. Comente a postagem de um colega apontando um problema semelhante ou uma solução diferente.

**Entrega:** commit + push, link do repositório e link do GitHub Pages no SIGAA.

## ✅ Checkpoint do projeto

Ao fim desta aula — e da Unidade 1 — o repositório do seu projeto autoral precisa ter:

- [ ] `lang="pt-BR"`, `<title>` único e descritivo, `meta viewport` sem restrição de zoom nas três páginas.
- [ ] Link de salto como primeiro elemento do `<body>`, visível ao receber foco, com `<main id="conteudo" tabindex="-1">` de destino.
- [ ] Anel de foco de dois tons via `:focus-visible`, visível sobre fundo claro e sobre a navbar escura; nenhuma regra `outline: none` sem substituto.
- [ ] Contraste AA em todos os textos e no indicador de foco, com os valores medidos anotados no `README.md`.
- [ ] Landmarks completos, um `<main>` por página, cada `<nav>` com `aria-label` próprio, cada `<section>` nomeada por `aria-labelledby`.
- [ ] Hierarquia de títulos sem saltos, com um único `<h1>` por página.
- [ ] `alt` correto em todas as imagens (descritivo, vazio ou descrevendo o destino do link), `aria-hidden="true"` em todos os SVG decorativos.
- [ ] Botão do menu com `aria-label`, `aria-expanded` e `aria-controls` apontando para um `id` existente.
- [ ] `aria-current="page"` apenas no link da página atual, em cada página.
- [ ] Formulário com `<label for>` em todos os campos, `<fieldset>`/`<legend>` nos grupos, `autocomplete`, `aria-describedby` nas ajudas e região `aria-live` vazia.
- [ ] Tabela com `<caption>` e `scope` nos cabeçalhos.
- [ ] Classe `.oculto-visualmente` (ou `.visually-hidden` do Bootstrap) usada onde o texto precisa existir só para o leitor de tela.
- [ ] Lighthouse ≥ 90 (categoria Accessibility, modo mobile) nas três páginas, com capturas antes e depois em `evidencias/`.
- [ ] Teste manual de teclado percorrido sem falhas nas três páginas.
- [ ] `README.md` com as seções "Sobre o projeto", "Framework escolhido e por quê", "Movimento" e "Acessibilidade".
- [ ] Tudo o que os checkpoints das Aulas 02 a 05 pediam continua funcionando.

## 📝 Avaliação 1 — instruções de entrega

### Escopo

A Avaliação 1 cobre a **Unidade 1 — Web estática** inteira: *website client-side em HTML e CSS, com HTML semântico, layout responsivo, framework CSS, animação/SVG e acessibilidade*. Você entrega o **projeto autoral** que vem evoluindo desde a Aula 01 — não o Café Cerrado, que é o exemplo construído em sala.

O projeto deve:

- Ter um domínio **diferente** do Café Cerrado e diferente do de cada colega (ex.: catálogo de plantas do Pantanal, agenda de quadras esportivas, mural de estágios, brechó, controle de pescarias, oficina de bicicletas, estúdio de tatuagem — ou outro tema aprovado na Aula 01).
- Ter no mínimo **três páginas** navegáveis entre si, sendo uma delas com formulário completo.
- Estar publicado e funcionando no **GitHub Pages**.
- Ser construído **sem JavaScript autoral** — o único JavaScript permitido é o do framework CSS escolhido (o `bootstrap.bundle.min.js`, por exemplo). O comportamento próprio começa na Unidade 2.

### Requisitos obrigatórios

1. **HTML semântico:** landmarks `header`, `nav`, `main` e `footer`; um único `<main>` por página; hierarquia de títulos sem saltos, com um `<h1>` por página; listas e tabelas usadas para o que são; HTML sem erros no validador do W3C.
2. **Layout responsivo:** usável em 360 px, 768 px e 1440 px, sem rolagem horizontal; imagens fluidas; menu adaptado ao celular.
3. **Framework CSS:** aplicado de forma consistente nas três páginas (grid, componentes e utilitários), com a escolha justificada em um parágrafo do `README.md`; CDN com versão fixa na URL.
4. **Animação e SVG:** microinterações com transição em todos os elementos clicáveis, cada `:hover` com o `:focus-visible` correspondente; pelo menos uma animação `@keyframes`; logotipo autoral em SVG inline; ao menos três ícones SVG; bloco `prefers-reduced-motion` no fim do CSS.
5. **Acessibilidade:** link de salto; foco visível com contraste adequado; contraste AA em todos os textos; `alt` correto em todas as imagens; `<label>` em todos os campos; `aria-label` nos `<nav>`; `aria-expanded`/`aria-controls` no botão do menu; `aria-current="page"`; região `aria-live` no formulário; **Lighthouse ≥ 90** na categoria Accessibility, em modo mobile, nas três páginas.
6. **`README.md`** com: nome e descrição do projeto, instruções para abrir localmente, link do GitHub Pages, justificativa do framework, seção "Movimento" e seção "Acessibilidade" com a tabela de notas antes/depois.
7. **Repositório público** no GitHub, com histórico de commits mostrando evolução incremental (um commit por aula, no mínimo) e a pasta `evidencias/` com as capturas.

### Formato e prazo de entrega

Entregue, na atividade "Avaliação 1" do SIGAA, **dois links colados no campo de texto**: o do repositório público no GitHub e o do site publicado no GitHub Pages. **Não anexe arquivo `.zip`** — a entrega é por link, e um repositório sem histórico de commits perde ponto no critério 6 da rubrica.

O prazo é o publicado no cronograma da disciplina (índice do Nível 2 no WebLab e a própria atividade no SIGAA). Confira a data lá; ela não é repetida aqui de propósito, para que este material continue válido em qualquer semestre.

### Rubrica (10,0 pontos)

| Critério | Peso |
|---|---|
| HTML semântico, estrutura das páginas e HTML válido | 2,0 |
| Layout responsivo em celular, tablet e desktop | 2,0 |
| Framework CSS aplicado com consistência e escolha justificada | 2,0 |
| Animação e SVG com propósito, incluindo `prefers-reduced-motion` | 2,0 |
| Acessibilidade: Lighthouse ≥ 90, teclado, contraste, ARIA | 1,5 |
| Versionamento, `README.md` e publicação no GitHub Pages | 0,5 |

Cada critério é avaliado em três faixas: **completo** (peso total), **parcial** (metade) e **ausente** (zero). "Parcial" é, tipicamente, o requisito presente em uma página e ausente nas outras duas.

### Política de atraso

Entregas após o prazo perdem **1,0 ponto por dia corrido** de atraso, até o limite de 5 dias. Depois desse limite a atividade recebe nota zero, salvo justificativa formal protocolada junto à coordenação do curso. O horário de referência é o registrado pelo SIGAA — não o do seu último commit.

### Política de plágio e uso de IA

É permitido usar ferramentas de IA como apoio (explicar um erro, sugerir sintaxe, revisar um trecho), assim como é permitido consultar documentação, tutoriais e o próprio WebLab. **Não é permitido** entregar um projeto gerado quase integralmente por IA sem compreensão do próprio código: na correção, qualquer estudante pode ser chamado para explicar oralmente uma parte do seu projeto — por que aquele `aria-expanded` está ali, por que a `transition` está no estado base, o que aquele `viewBox` significa — e a nota é ajustada conforme a clareza da explicação.

Cópia integral do projeto de outro colega, mesmo com o tema trocado, é plágio e resulta em **nota zero para ambos os envolvidos**, com encaminhamento conforme o regimento acadêmico da UNEMAT. Reaproveitar trechos do Café Cerrado construído em sala é esperado e permitido — o que não é permitido é entregar o Café Cerrado como se fosse o seu projeto.

## 📚 Para aprofundar

- MDN — Acessibilidade: <https://developer.mozilla.org/pt-BR/docs/Web/Accessibility> — comece pelo guia "Acessibilidade HTML" e pela lista de erros comuns.
- MDN — ARIA: <https://developer.mozilla.org/pt-BR/docs/Web/Accessibility/ARIA> — leia primeiro "As cinco regras do ARIA", depois a referência de atributos.
- W3C — WCAG 2.2 Quick Reference: <https://www.w3.org/WAI/WCAG22/quickref/> — filtre por nível A e AA e use como lista de verificação da Avaliação 1.
- W3C — WAI-ARIA Authoring Practices Guide: <https://www.w3.org/WAI/ARIA/apg/> — cada componente (acordeão, menu, modal) com o HTML e o comportamento de teclado corretos.
- W3C — Perspectivas de acessibilidade (vídeos curtos, legendados em português): <https://www.w3.org/WAI/perspective-videos/> — um minuto cada; mostre para quem disser que "ninguém usa isso".
- WebAIM — Contrast Checker: <https://webaim.org/resources/contrastchecker/> — cole os dois hexadecimais e leia o veredito AA/AAA.
- WAVE — Web Accessibility Evaluation Tool: <https://wave.webaim.org/> — auditoria pela URL, com os erros desenhados sobre a página.
- Chrome — Lighthouse: <https://developer.chrome.com/docs/lighthouse/accessibility/scoring> — como a nota de acessibilidade é calculada e por que ela não é uma nota de acessibilidade.
- NVDA — leitor de tela gratuito para Windows: <https://www.nvaccess.org/download/> — instale e passe dez minutos com ele; é a aula que mais muda a cabeça de um desenvolvedor.
- BRASIL — Lei nº 13.146/2015 (Lei Brasileira de Inclusão), art. 63: <https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13146.htm> — leia o artigo inteiro, são poucas linhas.
- eMAG — Modelo de Acessibilidade em Governo Eletrônico: <https://emag.governoeletronico.gov.br/> — a referência usada em licitações públicas brasileiras.
- QUEIRÓS, Ricardo; PORTELA, Filipe. *Introdução ao Desenvolvimento Moderno para a Web*. FCA, 2018 — camada de apresentação e boas práticas de interface (Biblioteca Virtual da UNEMAT).
- ALVES, William P. *Projetos de Sistemas Web*. Érica, 2015 — usabilidade e padrões de interface.
- LOUDON, Kyle. *Desenvolvimento de Grandes Aplicações Web*. Novatec, 2019 — qualidade de front-end em escala.

Isso encerra a **Unidade 1**. Em seis aulas o seu projeto saiu de um repositório vazio para um site de três páginas, semântico, responsivo, com framework CSS, identidade visual desenhada em código, movimento com propósito e acessível a quem não usa mouse nem enxerga a tela — publicado na internet, com endereço próprio. Ele é a Avaliação 1, e o Boss desta aula é o roteiro para fechá-la.

Na próxima aula começa a **Unidade 2 — Web dinâmica client-side**, com a revisão de JavaScript: objetos, funções, eventos e manipulação do DOM. O site que você acabou de entregar deixa de ser só apresentação e passa a **reagir**: o cardápio vai ser gerado a partir de um vetor de produtos em vez de estar escrito à mão no HTML, o formulário vai validar e responder de verdade — e aquela região `aria-live` que você deixou vazia hoje vai finalmente ganhar texto.
