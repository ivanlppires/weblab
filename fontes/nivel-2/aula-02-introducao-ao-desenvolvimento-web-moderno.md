# Aula 02 — Introdução ao desenvolvimento web moderno

> **Nível 2 — Desenvolvimento Web** · Unidade 1: Web estática
> WebLab · UNEMAT Sinop · Prof. Ivan Luiz Pedroso Pires
> **Carga:** 3 aulas de 50 min (presencial) + 1 h (assíncrona)

Na Aula 01 você acompanhou a requisição saindo do navegador e a resposta voltando do servidor. Hoje a câmera vira para o outro lado: o que acontece **depois** que a resposta chega — como o navegador transforma texto em pixels, quem decide as regras dessa transformação e como organizar um projeto para que ele funcione tanto na sua máquina quanto em um servidor real.

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Situar as fases da Web (estática, social, aplicações) e explicar o que mudou tecnicamente em cada uma.
- Nomear as organizações que mantêm os padrões da Web e explicar o que significa um *living standard*.
- Explicar como um servidor estático decide o que entregar: convenção `index`, tipos MIME e caminhos relativos.
- Descrever o pipeline de renderização do navegador (DOM, CSSOM, render tree, layout, paint) e o que bloqueia cada etapa.
- Distinguir o arquivo HTML do DOM e comprovar a diferença no DevTools.
- Escrever a anatomia completa de um documento HTML5 válido, com os *landmarks* `header`, `nav`, `main` e `footer`.
- Organizar um projeto front-end em `css/`, `js/` e `img/` e escrever uma folha de estilo base com variáveis CSS.

## 📋 Pré-requisitos

Na aula passada você montou o ambiente, aprendeu o ciclo do Git e publicou o Café Cerrado no GitHub Pages com um `index.html` de oito linhas. Hoje esse arquivo mínimo vira uma página de verdade — com cabeçalho, navegação, conteúdo principal e rodapé — e ganha a primeira folha de estilo do projeto. Cada `git push` continua republicando o site sozinho.

Checklist antes de começar:

- [ ] VS Code com Live Server e Prettier funcionando; `node -v`, `git --version` respondendo no terminal.
- [ ] Repositório `cafe-cerrado` no GitHub, com pelo menos dois commits e o GitHub Pages ligado.
- [ ] O site em `https://SEU-USUARIO.github.io/cafe-cerrado/` abrindo.
- [ ] Repositório do **projeto autoral** criado, com o tema definido.
- [ ] Do Nível 1: seletores CSS, o modelo de caixa e o que faz um `<div>`. Se estiver enferrujado, revise antes da Aula 03.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Fases da Web e padrões abertos; como um site é servido (convenção `index`, tipos MIME, caminhos); `file://` × `http://` |
| 2 | 50 min | O pipeline de renderização; DOM × arquivo; o trio HTML/CSS/JS e separação de responsabilidades; anatomia do documento HTML5 |
| 3 | 50 min | Mão na massa: pastas do projeto, `index.html` com landmarks, `css/estilo.css` com variáveis, push e republicação; laboratório |

## 1. Como a Web chegou até aqui

A Web nasceu entre 1989 e 1991, no CERN, das mãos de Tim Berners-Lee, combinando três invenções que continuam sustentando tudo o que você faz hoje: o **HTML** (a linguagem dos documentos), o **HTTP** (o protocolo de transporte, que você viu na Aula 01) e a **URL** (o endereçamento universal). Três coisas simples, encaixadas — e é isso que sobreviveu a três décadas de mudança.

| Fase | O que caracteriza | Exemplo típico |
|---|---|---|
| Web 1.0 (anos 90) | Páginas estáticas, somente leitura; o usuário consome | Sites institucionais, portais de notícias |
| Web 2.0 (anos 2000) | Conteúdo gerado pelo usuário, interatividade, requisições em segundo plano | Redes sociais, wikis, blogs |
| Web moderna | Aplicações completas no navegador, APIs, mobile, tempo real | Webmail, mensageiros web, sistemas bancários |

Do ponto de vista técnico, o que muda de uma fase para a outra é **onde o HTML é montado e quem tem iniciativa**:

- Na Web 1.0, o servidor entrega um arquivo pronto e a conversa acaba.
- Na Web 2.0, o JavaScript passa a fazer requisições em segundo plano e a **alterar a página já carregada** sem recarregá-la. É o que se chamou de AJAX, e é o assunto da Aula 10.
- Na Web moderna, o servidor muitas vezes entrega só um esqueleto e **dados** (JSON), e o navegador monta a interface. É a arquitetura SPA — que você vai construir na Unidade 2 e sofisticar no Nível 3.

O Café Cerrado vai atravessar as três fases ao longo do curso, nessa mesma ordem. Hoje ele está firmemente na primeira: arquivos estáticos entregues pelo GitHub Pages.

## 2. Quem define as regras: padrões abertos

A Web é a única plataforma de software relevante que **não pertence a ninguém**. Nenhuma empresa é dona do HTML. Isso é o que faz o seu site funcionar no Chrome, no Firefox, no Safari do iPhone do seu colega, em um leitor de tela e em um navegador que ainda vai ser lançado.

| Organização | Cuida de |
|---|---|
| **WHATWG** | HTML e DOM, mantidos como *living standard* |
| **W3C** | CSS, acessibilidade (WCAG/ARIA) e diversas APIs da plataforma |
| **Ecma International (TC39)** | ECMAScript, a especificação da linguagem JavaScript, com edições anuais |
| **IETF** | Protocolos de rede, publicados como RFCs — HTTP, TCP/IP, TLS |

### 2.1 O que é um *living standard*

O HTML **deixou de ter versões**. Depois do HTML5, não veio um "HTML6": a especificação virou um documento vivo, atualizado continuamente conforme navegadores implementam e a comunidade valida. Na prática, isso significa três coisas para você:

1. Não existe "meu site é HTML 5.2". Existe HTML, e existe o que os navegadores implementam hoje.
2. A pergunta certa nunca é "isso é padrão?", e sim **"isso já funciona nos navegadores que meu público usa?"**.
3. A documentação de referência precisa ser viva também. Por isso a MDN (<https://developer.mozilla.org/pt-BR/>) é a fonte desta disciplina, e não um livro impresso.

> **🧠 Você sabia?**
> No começo dos anos 2000 o W3C decidiu abandonar o HTML e apostar no XHTML 2.0, uma linguagem mais rígida e incompatível com o que já existia. Em 2004, gente da Opera, da Mozilla e da Apple discordou publicamente e fundou um grupo paralelo, o **WHATWG**, para continuar evoluindo o HTML de forma compatível com as páginas existentes. O grupo paralelo ganhou: o trabalho deles virou o HTML5, o XHTML 2.0 foi abandonado, e em 2019 o próprio W3C encerrou sua especificação de HTML e reconheceu o *living standard* da WHATWG como o documento oficial. A Web escolheu não quebrar o passado — e essa decisão é a razão de uma página de 1995 ainda abrir hoje.

### 2.2 Consequência prática: escreva para o padrão

Escrever "para o Chrome" é uma armadilha antiga e cara. O caminho seguro tem três passos, e você vai repeti-los o semestre inteiro:

1. **Consulte a MDN** antes de usar algo que você não domina. Cada página tem uma tabela de compatibilidade no final.
2. **Valide a marcação** no validador do W3C (<https://validator.w3.org/>). Ele aponta tags não fechadas, atributos inválidos e aninhamentos ilegais que o navegador silenciosamente "conserta" — de formas diferentes em cada navegador.
3. **Teste em dois navegadores diferentes**, sempre. Chrome e Firefox usam motores distintos (Blink e Gecko).

> **🔬 Investigue**
> Abra a página da MDN sobre um recurso qualquer de CSS — por exemplo `gap` (<https://developer.mozilla.org/pt-BR/docs/Web/CSS/gap>) — e role até o fim. Você vai encontrar uma tabela de **compatibilidade com navegadores**, com versões e datas de suporte. Agora repita com um recurso recente que você nunca usou (procure `:has()` na MDN). Compare as duas tabelas e responda: qual dos dois você usaria hoje em um site que precisa funcionar no celular antigo de um cliente? Essa consulta de 30 segundos é o que separa uma decisão técnica de um chute.

## 3. Como um site é servido

Você publicou um site na Aula 01 sem entender exatamente o que o GitHub Pages faz. Vamos abrir essa caixa, porque na Unidade 3 quem vai fazer esse trabalho é o seu próprio código Express.

### 3.1 A convenção `index`

Um **servidor estático** faz uma coisa só: mapeia o caminho da URL para um arquivo dentro de uma pasta e devolve o conteúdo. Pedir `/cardapio.html` entrega o arquivo `cardapio.html`.

Quando a URL termina em uma pasta (`/` ou `/promocoes/`), não há arquivo nomeado. Aí entra a convenção mais antiga da Web: o servidor procura um arquivo chamado **`index.html`** dentro dessa pasta e entrega esse. É por isso que o seu site abre em `https://SEU-USUARIO.github.io/cafe-cerrado/` sem você escrever o nome do arquivo.

Se não houver `index.html`, o servidor faz uma de duas coisas, dependendo da configuração: lista o conteúdo da pasta (*directory listing*) ou responde `404`. O GitHub Pages responde `404`.

### 3.2 Tipos MIME: como o navegador sabe o que recebeu

O navegador **não decide pela extensão do arquivo**. Ele obedece ao cabeçalho `Content-Type` da resposta, que carrega um **tipo MIME**:

| Arquivo | `Content-Type` | O que o navegador faz |
|---|---|---|
| `index.html` | `text/html; charset=UTF-8` | Interpreta como documento e renderiza |
| `css/estilo.css` | `text/css` | Aplica como folha de estilo |
| `js/app.js` | `text/javascript` | Executa como script |
| `img/logo.png` | `image/png` | Decodifica e exibe como imagem |

Isso explica um erro que você vai encontrar mais cedo ou mais tarde. Se o caminho da folha de estilo estiver errado, o servidor responde a página de erro `404` — que é **HTML** — e o navegador reclama:

```text
Refused to apply style from 'http://127.0.0.1:5500/css/estilo.css' because its MIME
type ('text/html') is not a supported stylesheet MIME type, and strict MIME checking
is enabled.
```

Traduzindo: "você me mandou HTML e disse que era CSS; não vou aplicar". A causa quase nunca é o MIME em si — é o caminho errado. Verifique na aba **Network** se o `estilo.css` voltou com status `200` ou `404`.

### 3.3 Caminhos relativos e absolutos

Caminho é a causa da maioria dos "funciona na minha máquina".

| Notação | Significado | Exemplo |
|---|---|---|
| `arquivo.html` | Mesma pasta do arquivo atual | `cardapio.html` |
| `pasta/arquivo.css` | Subpasta a partir do arquivo atual | `css/estilo.css` |
| `../arquivo.html` | Uma pasta acima | `../index.html` |
| `/arquivo.html` | A partir da **raiz do site**, não da pasta | `/cardapio.html` |

O ponto de partida de um caminho relativo é sempre **a pasta do arquivo onde o caminho está escrito**. E há uma armadilha específica do GitHub Pages: o seu site não fica na raiz do domínio, e sim em `https://SEU-USUARIO.github.io/cafe-cerrado/`. Um caminho absoluto como `/css/estilo.css` aponta para `https://SEU-USUARIO.github.io/css/estilo.css` — fora do seu projeto. Resultado: funciona no Live Server e quebra no site publicado.

> **⚠️ Atenção**
> Regra desta disciplina: **use sempre caminhos relativos** (`css/estilo.css`, `img/logo.png`) enquanto o projeto for publicado em subpasta. E jamais use caminho de disco (`C:\Users\...`): isso não existe na Web — o servidor só conhece a pasta do site.

### 3.4 `file://` não é a mesma coisa que `http://`

Dar duplo clique em um `.html` abre a página com o esquema `file://`, direto do disco, sem servidor nenhum. Parece funcionar — até parar de funcionar:

- Requisições `fetch` para arquivos locais são bloqueadas por política de segurança (você sentiria isso na Aula 10).
- Módulos ES (`<script type="module">`) não carregam.
- Caminhos que começam com `/` apontam para a raiz do **disco**.
- Nada do que você vê corresponde ao que o servidor real vai entregar.

Por isso a regra: **sempre pelo Live Server**, mesmo para uma página de uma linha. O botão *Go Live* sobe um servidor em `http://127.0.0.1:5500` e você passa a testar no mesmo esquema em que o site vai viver.

> **🔎 Por baixo do capô**
> `127.0.0.1` é o endereço de *loopback*: todo computador o usa para se referir a si mesmo (o apelido é `localhost`). Quando o Live Server escuta na porta 5500 e o navegador pede `http://127.0.0.1:5500/index.html`, os pacotes nem chegam à placa de rede — o sistema operacional os devolve internamente. É por isso que funciona sem internet e é instantâneo. E é exatamente o que vai acontecer na Aula 11, quando o servidor na porta 3000 for código seu.

## 4. O que o navegador faz com o código

Recebida a resposta, o navegador executa um pipeline. Entender essas etapas é o que permite explicar por que uma página "pisca", por que ela demora a aparecer e por que um script na posição errada trava tudo.

```text
HTML  ──parsing──>  DOM   ┐
                          ├──> Render Tree ──> Layout ──> Paint ──> Composite
CSS   ──parsing──>  CSSOM ┘
                            ▲
JavaScript ─────────────────┘  (pode alterar DOM e CSSOM a qualquer momento)
```

1. **Parsing do HTML → DOM.** O navegador lê o HTML caractere a caractere e monta uma árvore de objetos: o **DOM** (*Document Object Model*). Cada tag vira um nó.
2. **Parsing do CSS → CSSOM.** As regras de estilo viram outra árvore, o CSSOM, com a cascata e a especificidade já resolvidas.
3. **Render tree.** DOM e CSSOM são combinados, descartando o que não é visível (por exemplo, o que tem `display: none`).
4. **Layout** (ou *reflow*). Cálculo da posição e do tamanho exatos de cada caixa, em pixels.
5. **Paint.** Preenchimento: cores, textos, bordas, sombras.
6. **Composite.** Montagem das camadas na tela.

### 4.1 O que bloqueia o quê

Duas regras de ouro, que explicam metade das dúvidas de desempenho:

- **CSS bloqueia a renderização.** O navegador não pinta nada enquanto não tiver o CSSOM, porque pintar antes causaria um "flash" de página sem estilo. É por isso que a folha de estilo vai no `<head>` e precisa ser pequena.
- **JavaScript bloqueia o parsing.** Quando o parser encontra um `<script>` sem atributos, ele **para** de montar o DOM, baixa e executa o script, e só então continua. Por isso a boa prática de usar o atributo `defer` (o script é baixado em paralelo e executado só depois que o DOM estiver pronto) ou de colocar o `<script>` antes de `</body>`.

A partir da Unidade 2 todo script do Café Cerrado será carregado com `defer`. Guarde o motivo agora; você vai medir o efeito no desafio ⭐⭐ desta aula.

### 4.2 O DOM não é o arquivo

Esta é a ideia mais importante da aula, e ela vai reaparecer em todas as aulas da Unidade 2:

- O arquivo `.html` no disco é **texto**. Ele nunca muda sozinho.
- O **DOM** é a árvore em memória que o navegador construiu a partir desse texto. Ele muda o tempo todo.

A aba **Elements** do DevTools mostra o **DOM atual**, não o arquivo. É por isso que você pode editar um texto ali, ver a página mudar e, ao recarregar, tudo voltar ao que era: você alterou a memória, não o disco.

> **🔬 Investigue**
> Abra o seu site publicado e faça três coisas em sequência. (1) Digite `view-source:https://SEU-USUARIO.github.io/cafe-cerrado/` na barra de endereço: isso mostra o **arquivo**, exatamente como veio do servidor. (2) Pressione <kbd>F12</kbd> e vá em **Elements**: isso é o **DOM**. Compare — por enquanto são idênticos. (3) No **Console**, execute `document.body.append("Isto não está no arquivo")` e pressione <kbd>Enter</kbd>. Olhe de novo o Elements (mudou) e o `view-source` (não mudou). Você acabou de ver, com evidência, a diferença entre o arquivo e o DOM. Recarregue a página e o texto some.

## 5. O trio fundamental e a separação de responsabilidades

| Tecnologia | Responsabilidade | Analogia |
|---|---|---|
| **HTML** | Estrutura e significado do conteúdo | Esqueleto |
| **CSS** | Apresentação: cor, tipografia, espaçamento, layout | Aparência |
| **JavaScript** | Comportamento: reagir, validar, buscar, atualizar | Músculos e reflexos |

O princípio que organiza os três é a **separação de responsabilidades**: estrutura no `.html`, estilo no `.css`, comportamento no `.js`. Não é preciosismo — é o que permite trocar o visual inteiro sem tocar no conteúdo, reaproveitar uma folha de estilo em vinte páginas e ter duas pessoas trabalhando no mesmo projeto sem se atropelar.

Um exemplo mínimo, completo, com os três arquivos integrados:

`exemplo/index.html`

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Separação de responsabilidades</title>
  <link rel="stylesheet" href="css/estilo.css">
  <script src="js/app.js" defer></script>
</head>
<body>
  <h1>Bem-vindo ao Café Cerrado</h1>
  <button id="botao-saudacao" type="button">Diga olá</button>
  <p id="saida"></p>
</body>
</html>
```

`exemplo/css/estilo.css`

```css
h1 {
  color: #6f4e37;
  font-family: system-ui, sans-serif;
}

#botao-saudacao {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 8px;
  background-color: #6f4e37;
  color: #ffffff;
  cursor: pointer;
}
```

`exemplo/js/app.js`

```js
const botao = document.getElementById("botao-saudacao");
const saida = document.getElementById("saida");

botao.addEventListener("click", () => {
  saida.textContent = "Olá! Este texto veio do JavaScript.";
});
```

Três arquivos, três papéis, uma página. Repare que o `<script>` está no `<head>` **com `defer`**: o navegador começa a baixar o arquivo cedo, mas só o executa depois que o HTML inteiro virou DOM. Sem o `defer`, um script no `<head>` rodaria antes de o `<button>` existir e `document.getElementById` devolveria `null` — e `null.addEventListener` estoura `TypeError`. (A outra saída é pôr o `<script>` sem atributos logo antes de `</body>`, quando o botão já existe; `defer` no `<head>` é a forma preferida porque o download acontece em paralelo com a análise do HTML.) Você vai reencontrar exatamente esse bug na Aula 07 — e agora já sabe o nome dele.

## 6. Anatomia de um documento HTML5

Todo documento desta disciplina precisa ter, no mínimo:

| Elemento | Função |
|---|---|
| `<!DOCTYPE html>` | Declara HTML5 e liga o modo padrão de renderização |
| `<html lang="pt-BR">` | Elemento raiz; `lang` informa o idioma a leitores de tela e buscadores |
| `<head>` | Metadados — nada aqui aparece na página |
| `<meta charset="UTF-8">` | Codificação de caracteres; garante a acentuação |
| `<meta name="viewport" …>` | Adapta a página à largura real da tela do celular |
| `<title>` | Título na aba do navegador e nos resultados de busca |
| `<meta name="description" …>` | Resumo usado por buscadores e ao compartilhar o link |
| `<link rel="stylesheet" …>` | Conecta a folha de estilo |
| `<body>` | Todo o conteúdo visível |

Três observações que valem nota na Avaliação 1:

- **`lang="pt-BR"` não é decoração.** É o que faz um leitor de tela pronunciar "pão" como português e não como inglês, e o que informa ao navegador qual dicionário usar na correção ortográfica de campos de formulário.
- **Sem `<meta name="viewport">` o celular mente.** O navegador móvel finge ter 980 px de largura e encolhe a página inteira, deixando o texto ilegível. Essa única linha é o pré-requisito de todo layout responsivo (Aula 04).
- **`<title>` é conteúdo, não enfeite.** É o que aparece na aba, no histórico, nos favoritos e como primeiro link no resultado de busca. Escreva algo útil: `Cardápio — Café Cerrado`, não `Documento`.

### 6.1 Os landmarks estruturais

Dentro do `<body>`, quatro elementos definem as **regiões** da página. São chamados de *landmarks* porque leitores de tela permitem saltar diretamente entre eles:

| Elemento | Papel na página |
|---|---|
| `<header>` | Cabeçalho da página ou de uma seção: marca, título, navegação principal |
| `<nav>` | Bloco de links de navegação |
| `<main>` | Conteúdo principal — **único por página**, e não repetido entre páginas |
| `<footer>` | Rodapé: contato, créditos, links institucionais |

O esqueleto típico:

```html
<body>
  <header>
    <p>Nome do site</p>
    <nav aria-label="Navegação principal">
      <ul>
        <li><a href="index.html">Início</a></li>
        <li><a href="cardapio.html">Cardápio</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <h1>Título da página</h1>
    <p>Conteúdo principal.</p>
  </main>

  <footer>
    <p>Rodapé com contato e créditos.</p>
  </footer>
</body>
```

Um `<div>` não diz nada sobre o próprio conteúdo; um `<nav>` declara "isto é a navegação do site". A Aula 03 aprofunda a semântica (`section`, `article`, `aside`, hierarquia de títulos) e a Aula 06 mostra o efeito disso em um leitor de tela. Por hoje, basta o esqueleto — mas ele já entra certo.

> **💡 Dica**
> O `aria-label` no `<nav>` dá nome à região. Uma página com dois `<nav>` (principal e rodapé) sem rótulo produz, no leitor de tela, duas entradas idênticas chamadas "navegação". Com rótulo, viram "Navegação principal" e "Navegação do rodapé". Custo: um atributo.

## 7. CSS moderno de base: variáveis, reset e unidades

A folha de estilo do projeto começa hoje, e ela começa por três decisões que valem o semestre inteiro.

### 7.1 Variáveis CSS (custom properties)

Uma **variável CSS** é uma propriedade personalizada, declarada com dois hifens e lida com `var()`:

```css
:root {
  --cor-marca: #6f4e37;
  --espaco-2: 1rem;
}

h1 {
  color: var(--cor-marca);
  margin-bottom: var(--espaco-2);
}
```

`:root` é o seletor do elemento raiz (`<html>`), então tudo declarado ali fica disponível na página inteira. Três motivos para começar assim:

1. **Um lugar só para mudar.** Trocar a paleta do site inteiro vira uma edição de cinco linhas.
2. **Elas são vivas.** Diferente das variáveis de pré-processadores (Sass, Less), que somem na compilação, as variáveis CSS existem em tempo de execução: o navegador as resolve na hora, elas respeitam a cascata e o JavaScript pode alterá-las com `document.documentElement.style.setProperty('--cor-marca', '#c2703d')`. É assim que se faz um seletor de tema claro/escuro sem recarregar a página.
3. **Elas documentam a intenção.** `var(--cor-marca)` diz mais do que `#6f4e37`.

> **⚠️ Atenção**
> Os dois hifens fazem parte do nome. `--cor-marca` declara; `var(--cor-marca)` lê. Escrever `var(cor-marca)` ou `color: --cor-marca` não dá erro visível: o navegador simplesmente ignora a declaração inválida e você fica olhando para uma cor que não mudou. Quando isso acontecer, abra o DevTools → Elements → aba *Styles*: a declaração inválida aparece riscada.

### 7.2 Um reset mínimo

Cada navegador aplica uma folha de estilo própria antes da sua. Um reset mínimo elimina as diferenças que mais incomodam:

```css
*,
*::before,
*::after {
  box-sizing: border-box;
}

body {
  margin: 0;
}

img {
  max-width: 100%;
  height: auto;
  display: block;
}
```

`box-sizing: border-box` faz com que `width` inclua padding e borda — o comportamento que todo mundo espera e que o padrão original não tem. `body { margin: 0 }` remove a margem de 8 px que os navegadores aplicam por conta própria. E as três linhas de `img` impedem que uma foto grande estoure o layout no celular.

### 7.3 Unidades relativas

| Unidade | Relativa a | Use para |
|---|---|---|
| `rem` | Tamanho de fonte da raiz | Espaçamentos, tamanhos de fonte, larguras máximas |
| `em` | Tamanho de fonte do próprio elemento | Espaçamento interno proporcional ao texto |
| `%` | Tamanho do elemento pai | Larguras fluidas |
| `px` | Pixel de referência | Bordas finas e raios de canto |

Use `rem` como padrão. O motivo é de acessibilidade: quem aumenta o tamanho de fonte nas configurações do navegador — e isso é comum — vê o layout inteiro acompanhar. Layout medido em `px` ignora essa preferência.

## 💻 Mão na massa — o Café Cerrado ganha estrutura

Hoje o `index.html` de oito linhas vira uma página com landmarks, o projeto ganha as pastas que vai usar até o fim do semestre e nasce a folha de estilo base.

### Passo 1 — As pastas do projeto

Na raiz de `cafe-cerrado`, crie as pastas `css/`, `js/` e `img/`. A estrutura fica assim:

```text
cafe-cerrado/
├── index.html          # página inicial (a convenção da §3.1)
├── README.md
├── .gitignore
├── css/
│   └── estilo.css
├── js/
│   └── .gitkeep
└── img/
    └── .gitkeep
```

O `.gitkeep` é um arquivo vazio com um propósito curioso: **o Git não versiona pastas, só arquivos**. Uma pasta vazia simplesmente não existe para ele. Colocar um arquivo vazio dentro dela é a convenção usada para que a estrutura chegue ao repositório. `js/` e `img/` ganham conteúdo real nas próximas aulas.

Regras de nomenclatura, que valem para o semestre inteiro: minúsculas, sem espaços, sem acentos, hífen separando palavras (`sobre-nos.html`, nunca `Sobre Nós.html`). O servidor do GitHub Pages roda Linux e diferencia maiúsculas de minúsculas.

### Passo 2 — A folha de estilo base

`cafe-cerrado/css/estilo.css`

```css
/* Café Cerrado — folha de estilo base
   Variáveis do projeto, reset mínimo e estilos das regiões da página. */

/* ---------- 1. Variáveis do projeto ---------- */
:root {
  --cor-marca: #6f4e37;
  --cor-marca-escura: #4a3325;
  --cor-destaque: #c2703d;
  --cor-fundo: #fdfaf6;
  --cor-superficie: #ffffff;
  --cor-texto: #2b2118;
  --cor-texto-suave: #5c4b3c;
  --borda-suave: rgba(111, 78, 55, 0.15);

  --fonte-base: system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;

  --espaco-1: 0.5rem;
  --espaco-2: 1rem;
  --espaco-3: 2rem;
  --espaco-4: 4rem;

  --largura-maxima: 60rem;
  --raio: 8px;
}

/* ---------- 2. Reset mínimo ---------- */
*,
*::before,
*::after {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: var(--fonte-base);
  font-size: 1rem;
  line-height: 1.6;
  color: var(--cor-texto);
  background-color: var(--cor-fundo);
}

img {
  max-width: 100%;
  height: auto;
  display: block;
}

a {
  color: var(--cor-marca);
}

/* ---------- 3. Cabeçalho e navegação ---------- */
.cabecalho {
  display: flex;
  flex-wrap: wrap;
  gap: var(--espaco-2);
  align-items: center;
  justify-content: space-between;
  padding: var(--espaco-2) var(--espaco-3);
  background-color: var(--cor-marca);
  color: var(--cor-superficie);
}

.marca {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: 0.02em;
}

.navegacao ul {
  display: flex;
  gap: var(--espaco-2);
  margin: 0;
  padding: 0;
  list-style: none;
}

.navegacao a {
  color: var(--cor-superficie);
  text-decoration: none;
  padding: var(--espaco-1);
}

.navegacao a:hover,
.navegacao a:focus {
  text-decoration: underline;
}

/* ---------- 4. Conteúdo principal ---------- */
main {
  max-width: var(--largura-maxima);
  margin: 0 auto;
  padding: var(--espaco-3) var(--espaco-2);
}

.destaque {
  padding: var(--espaco-4) var(--espaco-3);
  border-radius: var(--raio);
  background-color: var(--cor-superficie);
  border: 1px solid var(--borda-suave);
  text-align: center;
}

.destaque h1 {
  margin-top: 0;
  color: var(--cor-marca-escura);
  font-size: 2.25rem;
}

.destaque p {
  color: var(--cor-texto-suave);
  max-width: 40rem;
  margin-left: auto;
  margin-right: auto;
}

.botao {
  display: inline-block;
  margin-top: var(--espaco-2);
  padding: var(--espaco-1) var(--espaco-3);
  border-radius: var(--raio);
  background-color: var(--cor-destaque);
  color: var(--cor-superficie);
  text-decoration: none;
  font-weight: 600;
}

.botao:hover,
.botao:focus {
  background-color: var(--cor-marca);
}

.sobre {
  margin-top: var(--espaco-4);
}

.sobre h2 {
  color: var(--cor-marca-escura);
}

/* ---------- 5. Rodapé ---------- */
.rodape {
  margin-top: var(--espaco-4);
  padding: var(--espaco-3) var(--espaco-2);
  background-color: var(--cor-marca-escura);
  color: var(--cor-superficie);
  text-align: center;
}

.rodape p {
  margin: var(--espaco-1) 0;
  font-size: 0.9rem;
}
```

### Passo 3 — A página inicial com landmarks

Substitua o conteúdo de `index.html` por este. Digite, não cole — e repare em cada tag nova.

`cafe-cerrado/index.html`

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Café Cerrado: cafeteria de grãos torrados do cerrado mato-grossense, em Sinop/MT.">
  <title>Café Cerrado — cafeteria em Sinop/MT</title>
  <link rel="stylesheet" href="css/estilo.css">
</head>
<body>
  <header class="cabecalho">
    <p class="marca">Café Cerrado</p>

    <nav class="navegacao" aria-label="Navegação principal">
      <ul>
        <li><a href="index.html">Início</a></li>
        <li><a href="cardapio.html">Cardápio</a></li>
        <li><a href="contato.html">Contato</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <section class="destaque">
      <h1>Café que nasce no cerrado</h1>
      <p>
        Torramos em Sinop grãos colhidos na Chapada dos Parecis e no médio-norte
        de Mato Grosso. Cada lote tem origem, data de torra e ficha de sabor.
      </p>
      <a class="botao" href="cardapio.html">Ver o cardápio</a>
    </section>

    <section class="sobre">
      <h2>A casa</h2>
      <p>
        Somos uma cafeteria de bairro com torrefação própria. Servimos espresso,
        métodos filtrados e uma pequena confeitaria feita no dia.
      </p>
      <p>
        Funcionamos de terça a sábado, das 8h às 19h, na Avenida dos
        Jacarandás, 1200, no Setor Comercial de Sinop.
      </p>
    </section>
  </main>

  <footer class="rodape">
    <p>Café Cerrado — Avenida dos Jacarandás, 1200, Sinop/MT</p>
    <p>Projeto acadêmico da disciplina Desenvolvimento Web — UNEMAT Campus Sinop.</p>
  </footer>
</body>
</html>
```

Os links para `cardapio.html` e `contato.html` ainda apontam para páginas que não existem: clicar neles produz um `404`. Isso é intencional — as duas páginas nascem na Aula 03, e ver o `404` acontecer é uma boa oportunidade para reler a §3.1.

### Passo 4 — Ver funcionando e ler a rede

Abra com o Live Server (*Go Live*) e confira:

1. O cabeçalho marrom, com a navegação alinhada à direita.
2. O bloco de destaque centralizado, com o botão laranja.
3. O rodapé escuro no fim da página.

Agora abra o DevTools na aba **Network** e recarregue com <kbd>Ctrl</kbd>+<kbd>F5</kbd>. Você deve ver **duas** requisições: `index.html` e `estilo.css`. Clique em `estilo.css` e confirme, nos cabeçalhos de resposta, `Content-Type: text/css` — exatamente o que a §3.2 previu.

### Passo 5 — Provar que o CSS bloqueia a renderização

Um experimento de 30 segundos que fixa a §4.1. No DevTools, aba **Network**, mude o seletor de velocidade de *No throttling* para *Slow 4G* e recarregue. Observe a ordem: o HTML chega, mas a página só aparece pintada quando o CSS termina de baixar.

Agora troque a linha do `<link>` de lugar: mova-a do `<head>` para logo antes de `</body>`, salve e recarregue com a mesma simulação de rede lenta. Você vai ver a página aparecer **sem estilo** por um instante e depois "pular" para o visual correto. Isso se chama FOUC (*flash of unstyled content*), e é a razão de a folha de estilo ficar no `<head>`. **Desfaça a alteração** e volte o `<link>` para o `<head>`.

### Passo 6 — Validar a marcação

Acesse <https://validator.w3.org/nu/>, escolha a aba *Validate by Direct Input*, cole o conteúdo do seu `index.html` e clique em *Check*. A meta é: **zero erros**. Avisos (*warnings*) merecem leitura, mas nem todos exigem ação.

Se aparecer algo, o validador diz a linha e o motivo. Os erros mais comuns nesta etapa são tag não fechada, atributo escrito errado e `<li>` fora de `<ul>`.

### Passo 7 — Commit e republicação

```bash
git status
git add .
git commit -m "Estrutura a pagina inicial com landmarks e folha de estilo base"
git push
```

Espere um a três minutos e recarregue `https://SEU-USUARIO.github.io/cafe-cerrado/`. O site publicado agora tem o mesmo visual da sua máquina.

> **⚠️ Atenção**
> Se o site publicado aparecer **sem estilo**, o problema quase sempre é caminho: você escreveu `/css/estilo.css` (absoluto) em vez de `css/estilo.css` (relativo). Confirme na aba Network do site publicado: se `estilo.css` voltou `404`, é isso. A §3.3 explica por quê.

### Passo 8 — O projeto autoral acompanha

Repita os passos 1 a 7 no repositório do seu projeto autoral, com o **seu** tema: mesmas pastas, mesmos landmarks, sua paleta de variáveis, seu conteúdo. Não copie os textos do Café Cerrado — copie a **estrutura**.

### Como testar

- A aba Network mostra `index.html` e `estilo.css`, ambos com status `200`.
- `estilo.css` responde com `Content-Type: text/css`.
- O validador do W3C aponta zero erros.
- No DevTools → Elements → Styles, clicar em `var(--cor-marca)` mostra o valor `#6f4e37` resolvido.
- Reduzir a janela para 400 px de largura não gera barra de rolagem horizontal.
- O site publicado no GitHub Pages tem o mesmo visual da máquina local.

**Resultado esperado:** o Café Cerrado com estrutura semântica, folha de estilo baseada em variáveis, pastas organizadas e tudo isso no ar, atualizado por um `git push`.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Explique, em duas frases, a diferença entre o arquivo `index.html` e o DOM. Cite a aba do DevTools que mostra cada um.

**A2.** Um servidor recebe a requisição `GET /promocoes/`. Não existe arquivo com esse nome. O que ele procura, e o que responde se não encontrar?

**A3.** Ordene as etapas do pipeline de renderização: paint, parsing do HTML, layout, render tree, parsing do CSS, composite.

**A4.** O que acontece com a página se você remover a linha `<meta name="viewport" content="width=device-width, initial-scale=1.0">` e abrir no celular? E se remover `<meta charset="UTF-8">`?

**A5.** Qual a diferença entre `css/estilo.css` e `/css/estilo.css`? Em qual dos dois cenários o segundo quebra?

**A6.** Complete o código para que a cor de fundo do botão venha de uma variável chamada `--cor-destaque`:

```css
:root {
  --cor-destaque: #c2703d;
}

.botao {
  background-color: ;
}
```

**A7.** Diga o papel de cada landmark: `<header>`, `<nav>`, `<main>`, `<footer>`. Qual deles pode aparecer só uma vez por página?

**A8.** Por que um `<script>` sem atributos, colocado no `<head>`, atrasa a exibição da página? Cite dois jeitos de resolver.

**A9.** Cite as quatro organizações da §2 e o que cada uma padroniza.

**A10.** O navegador respondeu com este erro no Console. Diga a causa mais provável e como confirmar em dez segundos:

```text
Refused to apply style from 'http://127.0.0.1:5500/css/estilo.css' because its MIME
type ('text/html') is not a supported stylesheet MIME type.
```

**A11.** Qual a diferença entre `rem` e `em`? Por que a disciplina prefere `rem` para espaçamentos?

**A12.** O Git não versiona pastas vazias. Qual é a convenção usada no Mão na massa para contornar isso, e por que ela funciona?

### Nível B — Aplicação

**B1.** Crie a página `sobre.html` no Café Cerrado, reaproveitando o mesmo cabeçalho, a mesma navegação e o mesmo rodapé do `index.html`, com um `<main>` contendo um `<h1>` e três parágrafos sobre a história da cafeteria. Acrescente o link "Sobre" à navegação **das duas páginas**.

**Resultado esperado:** as duas páginas navegam entre si nos dois sentidos, com o mesmo visual, e o validador do W3C aponta zero erros em ambas.

<details markdown="1">
<summary>Dica</summary>

Copie o `index.html`, troque o conteúdo do `<main>` e ajuste o `<title>`. O `<link>` para o CSS é o mesmo caminho relativo, porque as duas páginas estão na mesma pasta. Na Aula 03 você vai marcar qual item do menu corresponde à página atual.
</details>

**B2.** Troque a identidade visual do Café Cerrado alterando **apenas** o bloco `:root` do `estilo.css`: transforme a paleta marrom em uma paleta verde (ou a que você preferir), mantendo contraste legível entre texto e fundo. Nenhuma outra regra do arquivo pode ser modificada.

**Resultado esperado:** o site inteiro muda de cor com a edição de um único bloco; nenhuma cor literal (`#rrggbb`) aparece fora do `:root`.

<details markdown="1">
<summary>Dica</summary>

Se alguma cor não mudar, é porque ela está escrita direto na regra em vez de vir de `var()`. Use <kbd>Ctrl</kbd>+<kbd>F</kbd> no arquivo procurando por `#` e converta cada ocorrência fora do `:root` em uma variável.
</details>

**B3.** Meça o efeito do CSS bloqueante. Na aba Network, com *Slow 4G* ativado, registre o tempo até a página aparecer pintada em três cenários: (a) `<link>` no `<head>`, como está; (b) `<link>` antes de `</body>`; (c) `<link>` no `<head>` mas com o CSS colado dentro de uma tag `<style>` no próprio HTML. Escreva um parágrafo comparando os três.

**Resultado esperado:** três medidas anotadas com o critério de medição declarado, mais uma conclusão sobre qual cenário é melhor e por quê.

<details markdown="1">
<summary>Dica</summary>

Use a coluna *Waterfall* da aba Network e o marcador de eventos na barra inferior. O cenário (c) elimina uma requisição inteira, mas cria outro problema: o CSS deixa de ser cacheado separadamente entre páginas. Mencione esse custo na conclusão.
</details>

**B4.** Escreva uma variação do `estilo.css` que respeite o tema escuro do sistema operacional, sem duplicar nenhuma regra: dentro de `@media (prefers-color-scheme: dark)`, redefina **apenas** as variáveis do `:root`.

**Resultado esperado:** alternar o tema do sistema entre claro e escuro muda o site inteiro; o bloco `@media` contém somente declarações de variáveis.

<details markdown="1">
<summary>Dica</summary>

A estrutura é `@media (prefers-color-scheme: dark) { :root { --cor-fundo: #1c1714; } }`. No Chrome dá para simular sem mexer no sistema: DevTools → menu de três pontinhos → *More tools* → *Rendering* → *Emulate CSS media feature prefers-color-scheme*.
</details>

**B5.** Investigue a diferença entre `file://` e `http://` na prática. Abra o `index.html` das duas formas (duplo clique no arquivo e pelo Live Server) e compare, em uma tabela: o que aparece na barra de endereço, o que a aba Network mostra em cada caso, e o valor de `window.location.protocol` no Console.

**Resultado esperado:** uma tabela com três linhas de comparação e um parágrafo explicando por que a disciplina exige o uso do Live Server.

<details markdown="1">
<summary>Dica</summary>

Em `file://` a aba Network normalmente não registra nada, porque não houve requisição HTTP nenhuma — o navegador leu o disco. Esse é o ponto central da resposta.
</details>

### Nível C — Desafio em sala

**C1.** Reproduza uma página real. Escolha a página inicial de uma cafeteria ou restaurante que você conheça, abra o DevTools e identifique: quais landmarks ela usa (ou deixa de usar), quantas requisições faz, qual o peso total e quantas fontes externas carrega. Depois reescreva o esqueleto dessa página — só a estrutura HTML com os landmarks corretos, sem copiar textos nem imagens — em um arquivo `exercicios/aula02/estrutura-analisada.html`, e escreva cinco linhas apontando o que você faria diferente.

<details markdown="1">
<summary>Dica</summary>

No Console, `document.querySelectorAll('header, nav, main, footer').length` conta os landmarks de uma vez. Muitos sites comerciais têm zero: são `<div>` de ponta a ponta. Isso é matéria-prima para a sua análise, não motivo para imitar.
</details>

**C2.** Sirva o seu site sem o Live Server. Usando o Node.js já instalado, suba um servidor estático na pasta do projeto (por exemplo com `npx serve` ou com o módulo `http` do Node) e acesse pelo endereço que ele indicar. Depois responda, com evidência da aba Network: qual `Content-Type` ele devolve para o HTML e para o CSS, o que acontece ao pedir um arquivo inexistente e o que acontece ao pedir a pasta raiz.

<details markdown="1">
<summary>Dica</summary>

`npx serve` baixa e executa o pacote sem instalar nada permanentemente. Compare a resposta de `/nao-existe.html` com a do GitHub Pages: os dois respondem `404`, mas o corpo da resposta é diferente. Na Aula 11 você vai escrever esse servidor com quatro linhas de Express.
</details>

## 🏆 Desafios

### ⭐ A identidade em um bloco só
Tags: css, layout, projeto

Um cliente pede: "gostei do site, mas a marca agora é verde-oliva, e queremos um modo escuro". Quanto tempo isso custa? Em um CSS bem escrito, cinco minutos; em um CSS com cores espalhadas por 300 linhas, uma tarde. Descubra em qual dos dois o **seu** projeto autoral está — e conserte.

**Critérios de pronto**

- Nenhuma cor literal (`#rrggbb`, `rgb()`, nomes como `white`) aparece fora do bloco `:root` do arquivo de estilos.
- Pelo menos oito variáveis nomeadas por **função** (`--cor-marca`, `--cor-superficie`, `--espaco-2`), nunca por aparência (`--marrom`, `--cor1`).
- Um bloco `@media (prefers-color-scheme: dark)` que redefine apenas variáveis e produz um tema escuro legível.
- Contraste entre texto e fundo verificado nos dois temas, com o resultado anotado (a aba *Elements → Styles* do Chrome mostra a razão de contraste ao inspecionar uma cor de texto).
- Uma captura de tela do site nos dois temas.

<details markdown="1">
<summary>Pistas</summary>

1. Comece procurando `#` no arquivo de estilos: cada ocorrência fora do `:root` é uma variável esperando para nascer.
2. Nomes por função sobrevivem à troca de paleta; nomes por cor viram mentira no dia em que o verde vira azul.
3. Para o tema escuro, não basta inverter: fundos escuros pedem texto levemente acinzentado e sombras mais sutis.
4. A MDN tem uma página sobre `prefers-color-scheme` com exemplos prontos para adaptar.
</details>

### ⭐⭐ O que trava a primeira pintura
Tags: performance, devtools, css, investigacao

Por que um site com pouquíssimo conteúdo demora dois segundos para aparecer? Quase sempre porque alguma coisa está bloqueando o caminho até a primeira pintura. Hoje você vira perito: mede, identifica o culpado e comprova a melhora com número.

**Critérios de pronto**

- A medição do seu site em três configurações (`<link>` no `<head>`, `<link>` antes de `</body>`, CSS embutido em `<style>`), com a rede simulada em *Slow 4G* e o critério de medição declarado.
- Uma tabela com os tempos das três configurações e a indicação de qual venceu.
- A aba **Coverage** do DevTools usada para descobrir qual porcentagem do seu CSS é efetivamente utilizada na página inicial, com o número anotado.
- Um teste com um `<script>` sem `defer` no `<head>` (pode ser um script que só imprime uma mensagem), mostrando na aba Network que ele atrasa o resto, e o mesmo teste com `defer` para comparação.
- Uma conclusão de dez linhas dizendo o que você mudaria em um site real, na ordem de prioridade.

<details markdown="1">
<summary>Pistas</summary>

1. A aba Coverage fica em DevTools → menu de três pontinhos → *More tools* → *Coverage*. Ela mostra, em vermelho, o CSS baixado e não usado.
2. Para simular latência, use o seletor de throttling da aba Network; para resultados comparáveis, marque também *Disable cache*.
3. O painel *Performance* grava a linha do tempo e marca os eventos de primeira pintura. Não precisa dominar a ferramenta: basta achar o marcador e ler o tempo.
4. Cuidado com a conclusão fácil: embutir o CSS acelera a **primeira** visita e prejudica as seguintes, porque o estilo deixa de ser cacheado à parte.
</details>

### ⭐⭐ O site sobrevive sem CSS?
Tags: html, acessibilidade, investigacao, devtools

Um teste brutal e revelador: desligue a folha de estilo do seu site e leia a página resultante. Se ela continuar fazendo sentido — títulos na ordem certa, links com texto claro, conteúdo antes do rodapé — a estrutura é boa. Se virar uma sopa ilegível, o significado estava no CSS, e não no HTML. É assim que um leitor de tela e um buscador enxergam a sua página.

**Critérios de pronto**

- Captura de tela do seu site com o CSS desabilitado (DevTools → Elements → desmarque a folha, ou remova o `<link>` temporariamente).
- Uma análise escrita de dez a quinze linhas respondendo: a ordem do conteúdo faz sentido? Os títulos formam uma hierarquia? Dá para navegar só pelos links?
- A saída de `document.querySelectorAll('h1, h2, h3')` no Console, listando a hierarquia de títulos, com um comentário sobre saltos de nível.
- Pelo menos três correções aplicadas ao HTML como resultado da análise, cada uma com o commit correspondente.
- O relatório do validador do W3C sem erros, anexado.

<details markdown="1">
<summary>Pistas</summary>

1. Só deve existir um `<h1>` por página, e os níveis não devem pular (`h1` → `h3` sem `h2` é um problema).
2. Textos de link como "clique aqui" e "saiba mais" são inúteis fora de contexto: um leitor de tela pode listar todos os links da página de uma vez.
3. Se o conteúdo principal aparecer depois do rodapé na página sem CSS, a ordem no HTML está errada — e nenhum `order` de flexbox conserta isso para quem não vê a tela.
4. Este é um ensaio geral da Aula 06, quando o Lighthouse vai pontuar exatamente esses itens.
</details>

### ⭐⭐⭐ Seu próprio servidor estático
Tags: node, http, terminal, investigacao

O GitHub Pages e o Live Server fazem a mesma coisa que você vai programar na Unidade 3: receber um caminho, achar um arquivo, devolver com o cabeçalho certo. Antecipe o assunto. Escreva, em Node.js puro (sem Express, sem instalar nada), um servidor estático de umas 40 linhas que sirva a pasta do Café Cerrado — e depois compare o comportamento dele com o do GitHub Pages.

**Critérios de pronto**

- Um arquivo `servidor.js` que sobe um servidor HTTP em uma porta local usando o módulo `http` do Node e serve os arquivos da pasta atual.
- Tipos MIME corretos para `.html`, `.css`, `.js`, `.png`, `.svg` e `.json`, comprovados na aba Network.
- A convenção `index` implementada: pedir `/` entrega `index.html`.
- Resposta `404` com uma mensagem própria para arquivos inexistentes, comprovada na aba Network.
- Um `README` curto no repositório do desafio comparando, em tabela, três comportamentos do seu servidor com os do GitHub Pages: `Content-Type` do CSS, resposta a `/`, resposta a um caminho inexistente.
- Uma reflexão de cinco linhas sobre o que o seu servidor **não** faz e um servidor de produção faz (cache, compressão, HTTPS, segurança de caminho).

<details markdown="1">
<summary>Pistas</summary>

1. Comece pela documentação do módulo `http` do Node: <https://nodejs.org/api/http.html>. O núcleo é `http.createServer((req, res) => { })` seguido de `servidor.listen(porta)`.
2. `req.url` traz o caminho pedido; o módulo `fs/promises` lê o arquivo; `res.writeHead(200, { 'Content-Type': tipo })` define o cabeçalho.
3. Um objeto simples mapeando extensão para tipo MIME resolve a tabela: `{ '.html': 'text/html', '.css': 'text/css' }`.
4. Cuidado com um caminho como `/../../etc/senha`: pense em como impedir que alguém saia da pasta do site. Esse é um problema de segurança real, com nome próprio (*path traversal*).
5. Quando chegar à Aula 11, compare o seu código com quatro linhas de `express.static`. A comparação é o prêmio do desafio.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `Refused to apply style from '…' because its MIME type ('text/html') is not a supported stylesheet MIME type` | O caminho do CSS está errado; o servidor devolveu a página de erro HTML no lugar do arquivo | Conferir o `href` do `<link>` e o status na aba Network; usar `css/estilo.css` relativo |
| O site funciona no Live Server e aparece sem estilo no GitHub Pages | Caminho absoluto (`/css/estilo.css`) apontando para a raiz do domínio, fora da subpasta do projeto | Trocar por caminho relativo (`css/estilo.css`) |
| `GET https://…/Cardapio.html 404 (Not Found)` | O arquivo é `cardapio.html`; o servidor Linux diferencia maiúsculas de minúsculas | Padronizar nomes em minúsculas e corrigir o `href` |
| A cor não muda por mais que você edite o valor | `var()` escrito sem os dois hifens, ou a variável declarada fora de `:root` | Conferir `--nome` na declaração e `var(--nome)` no uso; a declaração inválida aparece riscada em Elements → Styles |
| A página aparece minúscula e ilegível no celular | Falta `<meta name="viewport" content="width=device-width, initial-scale=1.0">` | Incluir a meta no `<head>` |
| Acentos viram `Ã§`, `Ã£`, `Ã©` | Falta `<meta charset="UTF-8">` ou o arquivo foi salvo em outra codificação | Incluir a meta; conferir "UTF-8" na barra inferior do VS Code |
| A pasta `img/` não aparece no GitHub depois do push | O Git não versiona pastas vazias | Criar um arquivo `.gitkeep` dentro dela e commitar |
| A página "pisca" sem estilo antes de aparecer formatada | O `<link>` da folha de estilo está no fim do `<body>` (FOUC) | Mover o `<link>` para o `<head>` |
| Alterações no CSS não aparecem no site publicado | Cache do navegador servindo a versão anterior | Recarregar com <kbd>Ctrl</kbd>+<kbd>F5</kbd>; confirmar na aba Network que o arquivo veio com `200`, não `304` |
| `fetch` bloqueado ou módulo não carrega ao abrir o arquivo | A página foi aberta com duplo clique, no esquema `file://` | Abrir sempre pelo Live Server, em `http://127.0.0.1:5500` |

## 🏠 Atividade assíncrona (1 h)

**Parte 1 — Estrutura do projeto autoral (35 min).** No repositório do seu projeto:

1. Crie as pastas `css/`, `js/` e `img/`, com `.gitkeep` nas duas últimas.
2. Reescreva o `index.html` com a anatomia completa (doctype, `lang`, charset, viewport, description, title) e os quatro landmarks: `header` com `nav`, `main` com um `<h1>` e pelo menos duas `<section>`, e `footer`.
3. Crie `css/estilo.css` com, no mínimo, oito variáveis no `:root`, o reset da §7.2 e estilos para cabeçalho, conteúdo e rodapé. Nenhuma cor literal fora do `:root`.
4. Crie a segunda página `sobre.html`, com a mesma estrutura e navegação funcionando nos dois sentidos.
5. Valide as duas páginas em <https://validator.w3.org/nu/> até zerar os erros.

**Parte 2 — Publicação (15 min).** Commit com mensagem descritiva, push e verificação do site publicado. Abra o site publicado no celular e confira que não há rolagem horizontal.

**Parte 3 — Leitura dirigida (10 min).** Na Biblioteca Virtual da UNEMAT: QUEIRÓS & PORTELA, capítulos sobre a evolução da Web e a camada de estrutura (HTML); PUREWAL, capítulos 1 e 2, sobre fluxo de trabalho e primeiras páginas. Anote duas diferenças entre o que os livros descrevem e o que você fez hoje.

**Critério de pronto:** as duas páginas do projeto autoral abrem no site publicado, navegam entre si, passam no validador sem erros e usam variáveis CSS para todas as cores.

**Entrega:** no SIGAA, o **link do repositório** e o **link do site publicado**. Sem `.zip`.

## ✅ Checkpoint do projeto

Ao fim desta aula, o repositório `cafe-cerrado` e o do seu projeto autoral devem ter:

- [ ] Pastas `css/`, `js/` e `img/` versionadas (as duas últimas com `.gitkeep`).
- [ ] `index.html` com doctype, `lang="pt-BR"`, charset, viewport, description, title e `<link>` para a folha de estilo.
- [ ] Os quatro landmarks no lugar: `header` (com `nav` rotulado), `main` único, `footer`.
- [ ] `css/estilo.css` com bloco `:root` de variáveis, reset mínimo e estilos das regiões.
- [ ] Nenhuma cor literal fora do `:root`.
- [ ] Zero erros no validador do W3C.
- [ ] Aba Network mostrando `index.html` e `estilo.css` com status `200` e tipos MIME corretos.
- [ ] Site publicado no GitHub Pages com o mesmo visual da máquina local, sem rolagem horizontal no celular.
- [ ] Commit com mensagem descritiva enviado com `git push`.

## 📚 Para aprofundar

- MDN — Introdução ao HTML: <https://developer.mozilla.org/pt-BR/docs/Learn_web_development/Core/Structuring_content> — leia "Começando com HTML" e "O que há na cabeça".
- MDN — Estruturando um documento: <https://developer.mozilla.org/pt-BR/docs/Learn_web_development/Core/Structuring_content/Structuring_documents> — a referência dos landmarks da §6.1.
- MDN — Usando propriedades personalizadas (variáveis CSS): <https://developer.mozilla.org/pt-BR/docs/Web/CSS/Using_CSS_custom_properties> — a fonte da §7.1.
- MDN — Tipos MIME comuns: <https://developer.mozilla.org/pt-BR/docs/Web/HTTP/MIME_types/Common_types> — a tabela completa da §3.2.
- MDN — `prefers-color-scheme`: <https://developer.mozilla.org/pt-BR/docs/Web/CSS/@media/prefers-color-scheme> — base para o desafio ⭐.
- web.dev — Critical rendering path: <https://web.dev/learn/performance/understanding-the-critical-path> — a §4 com muito mais detalhe (em inglês).
- WHATWG — HTML Living Standard: <https://html.spec.whatwg.org/> — a especificação viva citada na §2.1; abra uma vez para saber que ela existe.
- Validador do W3C: <https://validator.w3.org/nu/> — use antes de cada entrega, não depois.
- QUEIRÓS, Ricardo; PORTELA, Filipe. *Introdução ao Desenvolvimento Moderno para a Web*. FCA, 2018 — evolução da Web e camada de estrutura.
- PUREWAL, Semmy. *Aprendendo a Desenvolver Aplicações Web*. Novatec, 2014 — capítulos 1 e 2: fluxo de trabalho e primeiras páginas.
- ALVES, William P. *Projetos de Sistemas Web*. Érica, 2015 — organização de projetos e estrutura de sites.

Na próxima aula o HTML entra em profundidade: hierarquia de títulos, listas, tabelas, imagens com `figure`, links em todas as suas formas e formulários com validação nativa. O Café Cerrado ganha as duas páginas que hoje respondem `404` — `cardapio.html`, com os produtos organizados em tabelas e listas, e `contato.html`, com um formulário completo — e o menu passa a indicar em qual página você está.
