# Aula 07 — Revisão de JavaScript: objetos, funções, eventos e DOM

> **Nível 2 — Desenvolvimento Web** · Unidade 2: Web dinâmica client-side
> WebLab · curso aberto de desenvolvimento web
> **Tempo estimado:** 3 blocos de 50 min + 1 h de prática

Na Aula 06 você fechou a Unidade 1: o Café Cerrado tem HTML semântico, layout responsivo com Bootstrap, animação, SVG e uma auditoria de acessibilidade aprovada. É um site bonito e **imóvel** — tudo o que ele mostra está escrito à mão no HTML. Hoje começa a Unidade 2: o site ganha um cérebro. Você cria `js/app.js`, transforma o cardápio em **dados** e passa a desenhar a tela a partir desses dados, com eventos reagindo ao que a pessoa faz.

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Explicar como e quando o navegador executa um script e escolher entre `defer`, `async` e `type="module"`.
- Modelar dados de uma aplicação real como um array de objetos, justificando cada campo escolhido.
- Usar as sintaxes modernas de objeto — atalho de propriedade, desestruturação, espalhamento, `?.` e `??` — para escrever menos código e com menos erro.
- Selecionar, alterar, criar e remover elementos do DOM com segurança, sabendo quando `textContent` protege e `innerHTML` expõe.
- Renderizar uma lista a partir de um array usando o elemento `<template>` e `DocumentFragment`.
- Registrar ouvintes de eventos com `addEventListener`, ler o objeto `event` e aplicar delegação em listas geradas dinamicamente.
- Validar um formulário com a Constraint Validation API, mostrando erros acessíveis com `aria-live` e `aria-invalid`.

## 📋 Pré-requisitos

Na aula passada você auditou a acessibilidade do Café Cerrado e fechou o Marco 1 — o site estático completo. Hoje o mesmo repositório ganha um arquivo novo, `js/app.js`, e o cardápio deixa de ser HTML fixo para virar um array de objetos renderizado por JavaScript. Nada do que você fez na Unidade 1 é descartado: o JS vai **ligar e desligar** classes e atributos que o seu CSS já sabe estilizar.

Checklist antes de começar:

- [ ] Repositório `cafe-cerrado` clonado, com `index.html`, `cardapio.html`, `contato.html`, `css/estilo.css` e `img/`.
- [ ] Bootstrap 5.3 carregado pelo CDN em todas as páginas (Aula 04), com a navbar responsiva funcionando.
- [ ] Formulário de contato de `contato.html` com `label` para todo campo e a região `aria-live` da Aula 06.
- [ ] VS Code com a extensão Live Server (ou `npx serve`) — abrir com `file://` funciona hoje, mas a Aula 10 vai exigir um servidor local.
- [ ] Navegador com o DevTools aberto na aba Console. Programe com ele aberto o tempo todo.

Do Nível 1 você já traz: variáveis, tipos, condicionais, laços, funções, DOM e eventos (Aulas 10 a 14). Esta aula **não** reensina isso do zero — ela revisa em ritmo rápido, corrige os vícios mais comuns e avança para o que a Unidade 2 exige.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | O script na página; revisão de valores e tipos; objetos modernos; o array `produtos` |
| 2 | 50 min | DOM em profundidade: seleção, `<template>`, criação de nós; eventos, `event`, delegação |
| 3 | 50 min | Mão na massa (cardápio renderizado, tema, validação do formulário) e laboratório |

## 1. A camada de comportamento volta ao Café Cerrado

Desde a Aula 02 você trabalha com as três camadas do front-end: HTML (conteúdo e significado), CSS (apresentação) e JavaScript (comportamento). A Unidade 1 inteira foi feita nas duas primeiras. A regra que vale daqui em diante: **o JavaScript não deveria escrever estilo**. Ele altera dados, classes e atributos; quem decide a cor e o tamanho continua sendo o CSS.

Isso tem uma consequência prática imediata. Quando você quiser destacar um card, não escreva `card.style.border = "2px solid orange"`. Escreva `card.classList.add("destaque")` e deixe `.destaque` no `css/estilo.css`. O visual continua versionado em um lugar só, e o modo escuro, o `prefers-reduced-motion` e a impressão continuam funcionando.

### 1.1 Como o script entra na página

O `js/app.js` é vinculado no `<head>` com `defer`:

`cardapio.html` (trecho do `<head>`)

```html
<script src="js/app.js" defer></script>
```

Três formas de carregar um script, e o que muda em cada uma:

| Forma | Quando executa | Quando usar |
|---|---|---|
| `<script src="…">` | Na hora, bloqueando a montagem do HTML | Praticamente nunca |
| `<script src="…" defer>` | Depois que o HTML todo virou DOM, na ordem das tags | Padrão para o código da sua página |
| `<script src="…" async>` | Assim que o download terminar, fora de ordem | Scripts independentes (métricas, chat) |
| `<script src="…" type="module">` | Como `defer`, e com `import`/`export` disponíveis | Quando o código se divide em vários arquivos |

Com `defer`, quando a primeira linha de `app.js` roda, o `document` já está completo. É por isso que você não precisa mais envolver tudo em `DOMContentLoaded` como fazia no Nível 1 — o `defer` já garante essa ordem. Se o script estivesse no `<head>` **sem** `defer`, `document.querySelector("#lista-produtos")` devolveria `null`, porque o elemento ainda não teria sido criado.

> **🔎 Por baixo do capô**
> `defer` não é "esperar um pouco". O navegador continua baixando o arquivo em paralelo com o HTML — o que ele adia é apenas a **execução**, para o momento imediatamente anterior ao evento `DOMContentLoaded`. Vários scripts com `defer` executam na ordem em que aparecem no HTML; com `async`, na ordem em que chegam da rede, o que é imprevisível. Por isso `async` é péssimo para código que depende de outro código.

Um script `type="module"` já é adiado por padrão (o `defer` seria redundante) e traz duas mudanças de comportamento: o código roda em modo estrito automaticamente e as variáveis de topo **não** viram globais. Nesta unidade o Café Cerrado cabe em um arquivo só, então ficamos com `defer`. Quando o `app.js` crescer e se dividir, migramos para módulos — o Nível 3 vive inteiramente neles.

### 1.2 O Console é a sua bancada

O Console não serve só para `console.log`. Vale conhecer o resto do estojo:

```js
const produto = { id: 1, nome: "Espresso do Cerrado", preco: 6 };

console.log("valor simples:", produto.preco);
console.table([produto, { id: 2, nome: "Coado da Casa", preco: 8.5 }]);
console.group("Renderização do cardápio");
console.log("itens recebidos:", 10);
console.groupEnd();
console.warn("Imagem sem alt encontrada.");
console.error("Falha ao montar o card do produto 4.");
console.count("render");
```

`console.table` é o mais subestimado: passe um array de objetos e o DevTools desenha uma planilha com uma coluna por propriedade, ordenável por clique. Para depurar o `produtos` de hoje, é imbatível.

No painel de elementos, clique em qualquer nó e digite `$0` no Console: você recebe uma referência ao elemento selecionado e pode inspecioná-lo (`$0.className`, `$0.dataset`). E `debugger;` no meio do código pausa a execução ali, exatamente como um ponto de parada colocado na aba Sources.

> **🔬 Investigue**
> Abra o `cardapio.html`, cole no Console `console.table(document.querySelectorAll("img"))` e observe: você recebe uma tabela dos elementos, não dos arquivos. Agora rode `[...document.querySelectorAll("img")].map((i) => i.alt)`. Quantos `alt` estão vazios? Se algum aparecer como string vazia sem ser decorativo, você acabou de achar um bug de acessibilidade que o Lighthouse da Aula 06 pode ter deixado passar.

## 2. Revisão relâmpago: valores, tipos e comparações

### 2.1 `const` por padrão, `let` quando precisar mudar

```js
const nomeDaCafeteria = "Café Cerrado"; // nunca será reatribuído
let itensNoCarrinho = 0;                 // vai mudar ao longo do programa

itensNoCarrinho = itensNoCarrinho + 1;   // válido
// nomeDaCafeteria = "Outro nome";       // TypeError: Assignment to constant variable.
```

`var` não aparece em código novo — o escopo dela vaza de blocos e produz bugs difíceis. A regra prática: comece tudo com `const` e só troque para `let` quando precisar mesmo reatribuir. O Console avisa quando você errou, com `TypeError: Assignment to constant variable.`

Atenção a um detalhe que confunde: `const` congela a **ligação**, não o conteúdo. Um objeto declarado com `const` continua tendo suas propriedades alteráveis:

```js
const produto = { nome: "Espresso do Cerrado", preco: 6 };
produto.preco = 6.5;      // permitido: o objeto é o mesmo, só mudou dentro
// produto = { nome: "Outro" };  // TypeError: Assignment to constant variable.
```

### 2.2 Tipos e a comparação que você deve usar

```js
typeof "cappuccino";   // "string"
typeof 12.5;           // "number" — inteiro e decimal são o mesmo tipo
typeof true;           // "boolean"
typeof undefined;      // "undefined" — declarado, sem valor atribuído
typeof null;           // "object" — um bug histórico da linguagem, mantido por compatibilidade
typeof { id: 1 };      // "object"
typeof [1, 2, 3];      // "object" — para arrays use Array.isArray([1, 2, 3])
typeof console.log;    // "function"
```

```js
5 == "5";    // true  — converte tipos antes de comparar
5 === "5";   // false — compara valor E tipo
0 == "";     // true  — mais uma coerção surpreendente
0 === "";    // false

null == undefined;   // true
null === undefined;  // false
```

Use `===` e `!==` sempre. A única exceção defensável é `valor == null`, que testa `null` **ou** `undefined` de uma vez — e mesmo essa é melhor escrita como `valor === null || valor === undefined` enquanto você ainda está construindo o hábito.

### 2.3 Template literals

```js
const nome = "Ana";
const total = 27.5;

const recibo = `Obrigado, ${nome}!
Seu pedido soma R$ ${total.toFixed(2)}.
Status: ${total > 25 ? "frete grátis" : "frete a calcular"}`;
```

A crase permite interpolar `${qualquer expressão}` e quebrar linha dentro do texto. Concatenação com `+` só sobrevive em código antigo.

### 2.4 Verdadeiro, falso e os dois operadores que salvam linhas

Os valores **falsy** que aparecem no dia a dia são seis: `false`, `0`, `""`, `null`, `undefined` e `NaN`. Todo o resto é truthy — inclusive `"0"`, `[]` e `{}`.

```js
const lista = [];
if (lista) console.log("um array vazio é truthy!"); // imprime

if (lista.length === 0) console.log("verificação correta de lista vazia");
```

Dois operadores modernos resolvem os casos que antes exigiam `if` aninhado:

```js
const config = { titulo: "Cardápio", itensPorPagina: 0 };

// ?? (coalescência nula): usa o lado direito só se o esquerdo for null ou undefined
config.itensPorPagina ?? 12;   // 0  — respeita o zero
config.itensPorPagina || 12;   // 12 — o || trata 0 como "vazio" e atropela o valor

// ?. (encadeamento opcional): interrompe o acesso em vez de estourar erro
const produto = { nome: "Torta de Frango" };
produto.avaliacao?.media;      // undefined, sem erro
// produto.avaliacao.media;    // TypeError: Cannot read properties of undefined (reading 'media')
```

> **🧠 Você sabia?**
> `??` e `?.` só chegaram ao JavaScript em 2020 (ES2020) — vinte e cinco anos depois da primeira versão da linguagem. Brendan Eich escreveu o protótipo do JavaScript em dez dias, em maio de 1995, para a Netscape. O nome "Java" foi decisão de marketing: as duas linguagens não têm parentesco. O comitê que hoje decide o futuro da linguagem, o TC39, publica uma versão nova por ano — e cada proposta passa por cinco estágios públicos antes de virar padrão.

## 3. Objetos: o formato universal de dados da Web

Objetos merecem uma seção inteira porque tudo na Unidade 2 e na Unidade 3 é objeto: o DOM é uma árvore de objetos, o `event` que chega no clique é um objeto, a resposta de uma API chega em JSON — que é literalmente a notação de objeto do JavaScript. Investir aqui rende juros até a última aula do curso.

### 3.1 Criando e acessando

```js
const produto = {
  id: 2,
  nome: "Coado da Casa",
  categoria: "cafes",
  preco: 8.5,
  descricao: "Duzentos mililitros em coador de papel, moagem média feita na hora do pedido.",
  imagem: "img/coado.jpg",
};

produto.nome;              // "Coado da Casa" — notação de ponto
produto["preco"];          // 8.5 — notação de colchetes

const campo = "categoria";
produto[campo];            // "cafes" — colchetes aceitam variável; o ponto não
```

Use ponto sempre que souber o nome da propriedade ao escrever o código; use colchetes quando o nome vier de uma variável (é o caso do filtro por categoria da próxima aula).

### 3.2 Métodos e `this`

Uma função dentro de um objeto é um **método**. Dentro dele, `this` aponta para o próprio objeto:

```js
const cafeteria = {
  nome: "Café Cerrado",
  cidade: "Sinop",
  endereco() {
    return `${this.nome} — ${this.cidade}/MT`;
  },
};

cafeteria.endereco(); // "Café Cerrado — Sinop/MT"
```

Guarde isto para a Aula 08: `this` depende de **como** a função é chamada, e as arrow functions se comportam de outro jeito. Por enquanto, a regra é simples: método que usa `this` se escreve com a sintaxe acima.

### 3.3 Atalho de propriedade e chave calculada

```js
const nome = "Cappuccino Sinop";
const preco = 12;

const novoProduto = { nome, preco }; // atalho: { nome: nome, preco: preco }

const chave = "categoria";
const comCategoria = { ...novoProduto, [chave]: "cafes" }; // chave calculada
```

### 3.4 Desestruturação: extrair campos em uma linha

```js
const { nome: nomeDoProduto, preco: precoDoProduto } = produto;
const { descricao, imagem } = produto;
const { avaliacao = "sem avaliações" } = produto; // valor padrão se não existir
```

A desestruturação também funciona em parâmetros de função — e é aí que ela brilha, porque documenta o que a função usa:

```js
function resumirProduto({ nome, preco, categoria }) {
  return `${nome} (${categoria}): R$ ${preco.toFixed(2)}`;
}

resumirProduto(produto); // "Coado da Casa (cafes): R$ 8.50"
```

### 3.5 Espalhamento: copiar sem estragar o original

```js
const original = { nome: "Bolo de Milho Verde", preco: 9.5 };

const comDesconto = { ...original, preco: 8.5 }; // cópia com um campo trocado
original.preco;    // 9.5 — intacto
comDesconto.preco; // 8.5
```

O espalhamento (`...`) copia **um nível**. Se o objeto tiver outro objeto dentro, a cópia compartilha o interno:

```js
const pedido = { cliente: { nome: "Ana" }, itens: 2 };
const copia = { ...pedido };
copia.cliente.nome = "Bruno";
pedido.cliente.nome; // "Bruno" — o objeto interno é o mesmo!

const copiaProfunda = structuredClone(pedido); // cópia independente de verdade
```

> **⚠️ Atenção**
> Objetos e arrays são passados por **referência**. Duas variáveis podem apontar para o mesmo objeto na memória, e alterar por uma altera por outra. Metade dos bugs de "mudei uma coisa e a outra mudou junto" nasce aqui. Antes de modificar um objeto que veio de fora da sua função, copie.

### 3.6 Percorrendo um objeto

```js
const rotulos = { cafes: "Cafés", geladas: "Bebidas geladas", salgados: "Salgados", doces: "Doces" };

Object.keys(rotulos);    // ["cafes", "geladas", "salgados", "doces"]
Object.values(rotulos);  // ["Cafés", "Bebidas geladas", "Salgados", "Doces"]
Object.entries(rotulos); // [["cafes", "Cafés"], ["geladas", "Bebidas geladas"], …]

for (const [chave, valor] of Object.entries(rotulos)) {
  console.log(`${chave} → ${valor}`);
}
```

Um objeto assim, usado como dicionário de tradução, é o jeito idiomático de mapear o código interno (`"cafes"`) para o texto que a pessoa lê (`"Cafés"`). O Café Cerrado vai usar exatamente isso hoje.

### 3.7 A ponte para a Unidade 3: JSON

```js
const texto = JSON.stringify(produto);       // objeto → string
const deVolta = JSON.parse(texto);           // string → objeto

JSON.stringify(produto, null, 2);            // formatado, com 2 espaços de indentação
```

JSON é um **subconjunto** da notação de objeto: só aceita string, número, booleano, `null`, array e objeto. Funções, `undefined` e `Date` não sobrevivem à viagem (uma `Date` vira string). Na Aula 10 você vai buscar um arquivo `data/produtos.json`; na Unidade 3, o Express vai devolver JSON. É a mesma coisa que você está escrevendo agora, só que em texto.

## 4. Arrays de objetos: modelando o cardápio

O array continua o que você já conhece do Nível 1: lista ordenada, índice a partir de zero, `length`, `push`, `for…of`. O que muda no Nível 2 é o **conteúdo**: quase todo array de uma aplicação real é um array de objetos.

```js
const notas = [8, 7.5, 9, 6];
notas.length;   // 4
notas[0];       // 8
notas.push(10); // 5 — push devolve o novo tamanho

for (const nota of notas) {
  console.log(nota);
}

for (const [indice, nota] of notas.entries()) {
  console.log(`posição ${indice}: ${nota}`);
}
```

### 4.1 Decidindo os campos antes de escrever o array

Antes de digitar o cardápio em JavaScript, decida o **formato** de um item. Essa decisão vai atravessar toda esta trilha: a mesma estrutura vira JSON na Aula 10, corpo de requisição na Aula 13 e linha de banco no Nível 3. Para o Café Cerrado:

| Campo | Tipo | Por que existe |
|---|---|---|
| `id` | número | Identidade estável; sobrevive a mudanças de nome |
| `nome` | string | O que a pessoa lê no card |
| `categoria` | string curta | Chave de filtro; nunca o texto exibido |
| `preco` | número | Precisa ser somado e comparado |
| `descricao` | string | Uma frase de venda |
| `imagem` | string | Caminho relativo do arquivo |

Duas decisões merecem explicação:

**Por que `preco: 8.5` e não `preco: "R$ 8,50"`?** Porque texto não soma, não compara e não ordena. A formatação é responsabilidade da camada de apresentação, na hora de desenhar. Guarde número; formate na saída.

**Por que `categoria: "cafes"` e não `categoria: "Cafés"`?** Porque o valor guardado é uma chave técnica: sem acento, minúsculo, estável. O texto visível pode mudar (para "Nossos cafés", para outro idioma) sem quebrar nenhum filtro. É o mesmo raciocínio do `value` de um `<option>` contra o texto que aparece nele.

> **💡 Dica**
> `id` como número inteiro sequencial resolve por enquanto. Na Unidade 3, quem gera o `id` passa a ser o servidor — e ele nunca reaproveita um número já usado, mesmo depois de uma exclusão. Se você acostumar o código a tratar `id` como um valor opaco (comparar, nunca calcular), a migração não vai doer.

## 5. Funções são valores

Você usa funções desde o Nível 1. O que precisa ficar explícito agora, porque é a base da Aula 08 e de toda a programação assíncrona da unidade: **em JavaScript, função é um valor**. Pode ser guardada em variável, colocada dentro de um array ou objeto, passada como argumento e devolvida por outra função.

```js
// 1. Declaração — sofre hoisting: pode ser chamada antes da linha em que aparece
function calcularSubtotal(preco, quantidade) {
  return preco * quantidade;
}

// 2. Expressão — a função é um valor guardado numa variável
const calcularFrete = function (subtotal) {
  return subtotal >= 50 ? 0 : 8;
};

// 3. Arrow function — a forma dominante no JS moderno (aprofundada na Aula 08)
const aplicarDesconto = (valor, percentual) => valor * (1 - percentual / 100);

calcularSubtotal(6.5, 3);      // 19.5
calcularFrete(19.5);           // 8
aplicarDesconto(19.5, 10);     // 17.55
```

Parâmetros podem ter valor padrão, e a função pode receber outra função como argumento:

```js
function saudar(nome = "visitante") {
  return `Bem-vindo(a) ao Café Cerrado, ${nome}!`;
}

saudar();        // "Bem-vindo(a) ao Café Cerrado, visitante!"
saudar("Ana");   // "Bem-vindo(a) ao Café Cerrado, Ana!"

// Função que recebe função: o coração do addEventListener
function repetir(vezes, acao) {
  for (let i = 1; i <= vezes; i++) {
    acao(i);
  }
}

repetir(3, (n) => console.log(`tentativa ${n}`));
```

Quando você escreve `botao.addEventListener("click", minhaFuncao)`, você está entregando uma função ao navegador para que **ele** a chame depois. Repare no detalhe que derruba muita gente: passa-se `minhaFuncao`, sem os parênteses. Com parênteses você chamaria a função na hora e entregaria o **resultado** dela — quase sempre `undefined`.

Duas boas práticas que valem para o resto do curso:

- **Uma função, uma responsabilidade.** `renderizarProdutos` desenha; `filtrarProdutos` filtra. Se o nome precisa de um "e" no meio, provavelmente são duas funções.
- **Prefira funções puras.** Uma função pura recebe tudo pelos parâmetros, devolve um valor e não altera nada fora dela. É trivial de testar e não produz efeitos a distância. Nem tudo pode ser puro (mexer no DOM é efeito colateral por definição), mas quanto mais cálculo puro e menos DOM espalhado, melhor.

## 6. O DOM em revisão — e um pouco além

O navegador lê o HTML e constrói o **DOM**: uma árvore de objetos que representa a página viva na memória. O HTML é a receita; o DOM é o bolo. Alterar o DOM muda a tela na hora; recarregar a página joga o DOM fora e reconstrói tudo a partir do arquivo.

### 6.1 Selecionando

```js
const titulo = document.querySelector("h1");                  // o primeiro que casa
const lista = document.querySelector("#lista-produtos");       // por id
const cards = document.querySelectorAll(".card-produto");      // todos → NodeList
const primeiroCafe = document.querySelector('[data-categoria="cafes"]');
```

`querySelector` aceita qualquer seletor CSS — todo o conhecimento da Unidade 1 vale aqui. Duas armadilhas:

```js
cards.length;             // NodeList tem length e forEach
// cards.map(…);          // TypeError: cards.map is not a function
[...cards].map((c) => c.dataset.id);  // vire array antes de usar map/filter/reduce
```

E `querySelectorAll` devolve um retrato **estático**: elementos criados depois não entram nessa lista. Já `document.getElementsByClassName` devolve uma coleção viva, que se atualiza sozinha — comportamento surpreendente dentro de um laço. Prefira `querySelectorAll`.

### 6.2 Conteúdo: `textContent` × `innerHTML`

```js
titulo.textContent = "Cardápio";                      // texto puro
titulo.innerHTML = "Cardápio <span>do dia</span>";     // interpreta como HTML
```

> **⚠️ Atenção**
> Nunca coloque em `innerHTML` um valor que veio de fora — campo de formulário, parâmetro de URL, resposta de API. Uma string como `<img src=x onerror="alert(1)">` seria **executada**: é a porta do ataque XSS (Cross-Site Scripting). Para escrever texto, `textContent` sempre. Ele trata tudo como texto, inclusive `<` e `>`, e ainda por cima é mais rápido, porque não invoca o analisador de HTML.

### 6.3 Atributos, propriedades e `data-*`

Atributo é o que está escrito no HTML; propriedade é o campo do objeto no DOM. Na maioria dos casos os dois andam juntos, mas não sempre:

```js
const campo = document.querySelector("#nome");

campo.setAttribute("aria-describedby", "erro-nome"); // atributo
campo.getAttribute("type");                          // "text"
campo.hasAttribute("required");                      // true
campo.removeAttribute("disabled");

campo.value = "Ana";        // propriedade: o valor atual digitado
campo.disabled = true;      // propriedade booleana
```

Para guardar dados seus em um elemento, use `data-*`, que chega ao JavaScript pelo `dataset`:

```html
<article class="card-produto" data-id="3" data-categoria="cafes">Cappuccino Sinop</article>
```

```js
const card = document.querySelector(".card-produto");
card.dataset.id;         // "3" — sempre string!
Number(card.dataset.id); // 3
card.dataset.categoria;  // "cafes"
card.dataset.emEstoque = "sim"; // vira data-em-estoque="sim" no HTML
```

Repare: `data-em-estoque` no HTML vira `dataset.emEstoque` no JS (traço vira maiúscula). E todo valor de `dataset` é **string** — comparar com `===` contra um número sempre dá `false`.

### 6.4 Classes e estado visual

```js
card.classList.add("destaque");
card.classList.remove("oculto");
card.classList.toggle("aberto");              // liga se está desligado e vice-versa
card.classList.toggle("concluido", true);     // força para ligado
card.classList.contains("destaque");          // true/false
card.classList.replace("antigo", "novo");
```

`toggle` com segundo argumento é a forma mais limpa de sincronizar classe com um booleano do seu estado — sem `if`.

### 6.5 Criando elementos

```js
const item = document.createElement("li");
item.className = "item-cardapio";
item.textContent = "Pão de Queijo Mineiro";

const outroItem = document.createElement("li");
outroItem.textContent = "Torta de Frango";

const lista = document.querySelector("#lista-produtos");
lista.appendChild(item);       // insere no fim
lista.prepend(outroItem);      // insere no início
lista.append(item, outroItem); // aceita vários de uma vez, e também texto puro
item.remove();                 // remove a si mesmo
lista.replaceChildren();       // limpa o contêiner (melhor que innerHTML = "")
```

### 6.6 `<template>`: a marcação do card mora no HTML

Montar um card inteiro com dez `createElement` funciona, mas espalha marcação dentro do JavaScript — e quem for mexer no visual vai ter que ler código. O elemento `<template>` resolve: ele guarda um pedaço de HTML **inerte** (não é exibido, imagens não são baixadas, scripts não rodam) que o JS clona quantas vezes precisar.

`cardapio.html` (trecho)

```html
<template id="template-produto">
  <div class="col">
    <article class="card h-100 card-produto">
      <img class="card-img-top" src="" alt="">
      <div class="card-body d-flex flex-column">
        <span class="badge text-bg-secondary align-self-start mb-2" data-campo="categoria"></span>
        <h3 class="card-title h5" data-campo="nome"></h3>
        <p class="card-text flex-grow-1" data-campo="descricao"></p>
        <p class="preco fw-bold mb-0" data-campo="preco"></p>
      </div>
    </article>
  </div>
</template>
```

```js
const molde = document.querySelector("#template-produto");
const copia = molde.content.cloneNode(true); // true = clona com os filhos
copia.querySelector('[data-campo="nome"]').textContent = "Espresso do Cerrado";
document.querySelector("#lista-produtos").appendChild(copia);
```

`molde.content` é um `DocumentFragment` — um contêiner leve que não faz parte da página. Ao dar `appendChild` nele, o navegador move os filhos para o destino e descarta a casca. Duas vantagens: o HTML fica no HTML, e a inserção acontece de uma vez só.

### 6.7 Inserir muitos nós sem castigar o navegador

```js
const fragmento = document.createDocumentFragment();

for (const produto of produtos) {
  const item = document.createElement("li");
  item.textContent = produto.nome;
  fragmento.appendChild(item); // ainda fora do documento
}

lista.appendChild(fragmento);  // uma única alteração no DOM
```

Para dez produtos, a diferença é imperceptível. Para quinhentos, aparece — principalmente no celular. Adotar o hábito agora não custa nada.

### 6.8 Formatando valores para a tela

Nunca escreva `"R$ " + preco` — o Brasil usa vírgula decimal e ponto de milhar. A plataforma já resolve isso:

```js
const formatadorMoeda = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

formatadorMoeda.format(6.5);     // "R$ 6,50"
formatadorMoeda.format(1234.5);  // "R$ 1.234,50"
```

Crie o formatador **uma vez** e reutilize: construir um `Intl.NumberFormat` é caro comparado a chamar `.format()`.

> **🧠 Você sabia?**
> O objeto `Intl` carrega, dentro do navegador, as regras de formatação de mais de 400 idiomas e regiões — vindas do CLDR, o repositório de dados de localização mantido pelo consórcio Unicode. Além de moeda, ele formata datas (`Intl.DateTimeFormat`), listas ("café, pão e bolo" com `Intl.ListFormat`), tempo relativo ("há 3 dias") e faz ordenação alfabética que entende acentos (`Intl.Collator`). Tudo isso sem uma linha de biblioteca externa.

## 7. Eventos: reagindo a quem usa o site

Evento é qualquer acontecimento na página: clique, tecla, envio de formulário, rolagem, mudança de campo. O navegador é uma máquina orientada a eventos — entre um e outro, seu código simplesmente não roda.

### 7.1 `addEventListener` e suas opções

```js
const botao = document.querySelector("#btn-tema");

botao.addEventListener("click", (evento) => {
  console.log("clicou em:", evento.target);
});

// Opções úteis do terceiro argumento:
botao.addEventListener("click", aoClicarUmaVez, { once: true });   // remove sozinho após disparar
window.addEventListener("scroll", aoRolar, { passive: true });     // promete não chamar preventDefault
```

Para remover um ouvinte, você precisa da **mesma referência** de função — por isso funções anônimas não podem ser removidas:

```js
function aoClicarUmaVez() {
  console.log("primeira e única vez");
}

botao.removeEventListener("click", aoClicarUmaVez);
```

Há uma forma mais moderna, que remove vários ouvintes de uma vez:

```js
const controlador = new AbortController();

document.addEventListener("keydown", aoTeclar, { signal: controlador.signal });
window.addEventListener("resize", aoRedimensionar, { signal: controlador.signal });

controlador.abort(); // remove os dois de uma vez
```

Isso será muito útil na SPA da Aula 10, quando trocar de tela exigir desligar os ouvintes da tela anterior.

### 7.2 Os eventos que você vai usar nesta unidade

| Evento | Dispara quando | Onde registrar |
|---|---|---|
| `click` | Clique ou toque | No elemento clicável (ou no contêiner, por delegação) |
| `submit` | Formulário é enviado | No `<form>`, nunca no botão |
| `input` | Valor muda a cada tecla | No campo |
| `change` | Valor é confirmado (sai do campo, escolhe opção) | No campo ou `<select>` |
| `keydown` | Tecla é pressionada | No elemento ou no `document` |
| `focus` / `blur` | Elemento ganha/perde o foco | No campo (não borbulham; use `focusin`/`focusout`) |

### 7.3 O objeto `event`

Toda função ouvinte recebe um objeto com o que aconteceu:

```js
document.querySelector("#lista-produtos").addEventListener("click", (evento) => {
  evento.target;         // o elemento MAIS PROFUNDO onde o clique aconteceu
  evento.currentTarget;  // o elemento onde o ouvinte foi registrado (#lista-produtos)
  evento.type;           // "click"
  evento.preventDefault();   // cancela o comportamento padrão do navegador
  evento.stopPropagation();  // impede que o evento suba na árvore
});
```

A confusão entre `target` e `currentTarget` é a fonte número um de bugs em delegação. Se você clica no `<h3>` dentro do card, `target` é o `<h3>`; `currentTarget` continua sendo o contêiner que ouve.

`preventDefault()` cancela a ação natural do elemento: recarregar a página no `submit`, navegar no `click` de um link, digitar a tecla no campo. Cancele com critério — cancelar o padrão de um link sem oferecer navegação alternativa quebra a acessibilidade.

### 7.4 Propagação e delegação

Um clique não acontece em um elemento só. Ele desce da raiz até o alvo (fase de captura) e depois sobe de volta (fase de borbulhamento). Ouvintes registrados sem opção especial escutam na subida — o que permite um truque fundamental:

```js
const lista = document.querySelector("#lista-produtos");

lista.addEventListener("click", (evento) => {
  const botao = evento.target.closest("[data-acao]");
  if (!botao) return;                     // clique fora de qualquer botão: ignora

  const card = botao.closest(".card-produto");
  const id = Number(card.dataset.id);

  if (botao.dataset.acao === "detalhes") mostrarDetalhes(id);
  if (botao.dataset.acao === "favoritar") alternarFavorito(id);
});
```

Isso é **delegação de eventos**: um único ouvinte no contêiner atende todos os filhos, inclusive os que ainda não existem. Como o cardápio é renderizado do array — e re-renderizado a cada filtro na próxima aula —, registrar ouvinte card por card significaria registrar tudo de novo a cada `render`. Com delegação, você registra uma vez e esquece.

`closest(seletor)` sobe a árvore a partir do elemento e devolve o primeiro ancestral (ou ele mesmo) que casa com o seletor — ou `null`. É o companheiro inseparável da delegação.

### 7.5 Teclado e o padrão de divulgação acessível

O menu do Café Cerrado é a navbar do Bootstrap, que já cuida do `aria-expanded` sozinha. Mas o padrão vale para qualquer botão que abre e fecha alguma coisa — um "ver mais" no card, um acordeão de perguntas frequentes — e você vai precisar dele no projeto autoral:

```js
const gatilho = document.querySelector("#btn-detalhes");
const painel = document.querySelector("#painel-detalhes");

gatilho.addEventListener("click", () => {
  const aberto = painel.classList.toggle("aberto");
  gatilho.setAttribute("aria-expanded", String(aberto));
});

document.addEventListener("keydown", (evento) => {
  if (evento.key !== "Escape") return;
  if (!painel.classList.contains("aberto")) return;

  painel.classList.remove("aberto");
  gatilho.setAttribute("aria-expanded", "false");
  gatilho.focus(); // devolve o foco a quem abriu — regra de ouro
});
```

Três detalhes que separam um componente acessível de um componente quebrado: o `aria-expanded` acompanha o estado real; `Escape` fecha; e o foco volta para o botão que abriu, senão quem navega por teclado é despejado no início da página.

> **🔬 Investigue**
> Com o `cardapio.html` aberto, cole no Console: `document.body.addEventListener("click", (e) => console.log(e.target.tagName, "→", e.currentTarget.tagName))`. Agora clique no título de um card, na imagem e no espaço vazio ao lado. O segundo valor nunca muda (`BODY`), o primeiro muda sempre. Você acabou de ver o borbulhamento em ação — e por que a delegação funciona.

## 8. Estado → renderização → eventos

Antes de ir ao projeto, o esqueleto que organiza tudo o que vem pela frente:

```js
// 1. ESTADO — a fonte única da verdade
const produtos = [];      // os dados
let categoriaAtiva = "";  // o que o usuário escolheu

// 2. REFERÊNCIAS — selecionadas uma vez só
const els = {
  lista: document.querySelector("#lista-produtos"),
  filtro: document.querySelector("#filtro-categoria"),
};

// 3. RENDERIZAÇÃO — desenha a tela a partir do estado
function renderizar() {
  const visiveis = categoriaAtiva
    ? produtos.filter((produto) => produto.categoria === categoriaAtiva)
    : produtos;

  els.lista.replaceChildren();
  for (const produto of visiveis) {
    els.lista.appendChild(criarCard(produto));
  }
}

// 4. EVENTOS — capturam a intenção e mudam o estado
function registrarEventos() {
  els.filtro.addEventListener("change", (evento) => {
    categoriaAtiva = evento.target.value;
    renderizar();
  });
}

// 5. INICIALIZAÇÃO
function iniciar() {
  registrarEventos();
  renderizar();
}
```

O fluxo é sempre: **usuário age → evento → o estado muda → `renderizar()` redesenha**. Nunca corrija o DOM na mão para refletir um dado. Se o preço mudou, mude o array e renderize; não saia procurando o `<p class="preco">` certo. Quando DOM e dados divergem, os bugs viram caça ao fantasma.

Esse é o mesmo princípio que Vue e React automatizam no Nível 3. Aprender a fazer na mão agora é o que vai fazer o framework parecer óbvio depois.

## 9. Validação de formulário sem reinventar a roda

O `contato.html` já tem `required`, `type="email"` e `minlength` desde a Aula 03 — validação nativa do HTML. O navegador barra o envio e mostra um balão. O problema: esse balão não é estilizável, some sozinho, aparece só um por vez e alguns leitores de tela o anunciam mal.

A saída profissional não é jogar a validação nativa fora e reescrever tudo com `if`. É usar a **Constraint Validation API**: você desliga só a exibição do balão com `novalidate` no `<form>` e continua consultando o veredito do navegador pelo objeto `validity` de cada campo.

```js
const form = document.querySelector("#form-contato");
const campo = form.elements.email;

campo.validity.valid;          // false se qualquer regra falhou
campo.validity.valueMissing;   // true se required e vazio
campo.validity.typeMismatch;   // true se type="email" e formato inválido
campo.validity.tooShort;       // true se abaixo do minlength
campo.validity.patternMismatch;// true se não casa com o pattern
campo.checkValidity();         // o resumo: true/false
```

Isso dá o melhor dos dois mundos: as regras continuam declaradas no HTML (onde qualquer pessoa as lê) e as mensagens são suas, em português, no lugar que você escolher.

```js
function mensagemDeErro(campo) {
  const v = campo.validity;
  if (v.valueMissing) return "Este campo é obrigatório.";
  if (v.typeMismatch) return "Digite um e-mail no formato nome@dominio.com.";
  if (v.tooShort) return `Escreva pelo menos ${campo.minLength} caracteres.`;
  if (v.patternMismatch) return "O formato digitado não é aceito.";
  return "Valor inválido.";
}
```

Para o erro ser **percebido** por quem usa leitor de tela, três atributos trabalham juntos: `aria-invalid` marca o campo como inválido, `aria-describedby` liga o campo ao parágrafo da mensagem, e a região com `aria-live="polite"` anuncia o resumo sem interromper. Você já preparou esse terreno na Aula 06 — hoje ele entra em uso.

> **📌 Vale gravar**
> Validação no cliente é **conveniência**, não segurança. Qualquer pessoa desliga o JavaScript, edita o HTML pelo DevTools ou manda a requisição direto pelo terminal. A validação que protege os dados é a do servidor, que você vai escrever na Aula 13. Toda regra precisa existir nos dois lados: no cliente para dar resposta rápida, no servidor para valer.

## 💻 Mão na massa — o Café Cerrado ganha comportamento

Cinco passos. Ao final, o cardápio é desenhado a partir de um array, o site tem alternância de tema com memória, e o formulário de contato valida com mensagens acessíveis.

### Passo 1 — criar o `js/app.js` e ligá-lo em todas as páginas

Crie a pasta `js/` e o arquivo `js/app.js`. Em `index.html`, `cardapio.html` e `contato.html`, adicione ao final do `<head>`, **depois** das tags do Bootstrap que você colocou na Aula 04:

`cardapio.html` (trecho do `<head>`)

```html
<script src="js/app.js" defer></script>
```

Como o mesmo arquivo roda nas três páginas, ele vai tentar selecionar elementos que só existem em uma delas. A defesa é iniciar cada funcionalidade separadamente e sair cedo quando o elemento não existe:

`js/app.js`

```js
// ===== Café Cerrado — camada de comportamento =====
// Este arquivo roda em todas as páginas. Cada bloco "iniciar…" confere
// se os elementos de que precisa existem antes de fazer qualquer coisa.

function iniciar() {
  iniciarTema();
  iniciarCardapio();
  iniciarContato();
}

iniciar();
```

Ainda não existem as três funções — o Console vai reclamar com `Uncaught ReferenceError: iniciarTema is not defined`. Os próximos passos preenchem cada uma. Escreva as funções **acima** da chamada `iniciar()` para manter a leitura de cima para baixo.

### Passo 2 — os dados: o array `produtos`

No topo do `js/app.js`, antes de tudo:

`js/app.js` (topo do arquivo)

```js
const produtos = [
  {
    id: 1,
    nome: "Espresso do Cerrado",
    categoria: "cafes",
    preco: 6,
    descricao: "Grãos de Alto Paraíso, torra média, corpo encorpado e final achocolatado.",
    imagem: "img/espresso.jpg",
  },
  {
    id: 2,
    nome: "Coado da Casa",
    categoria: "cafes",
    preco: 8.5,
    descricao: "Duzentos mililitros em coador de papel, moagem média feita na hora do pedido.",
    imagem: "img/coado.jpg",
  },
  {
    id: 3,
    nome: "Cappuccino Sinop",
    categoria: "cafes",
    preco: 12,
    descricao: "Espresso duplo, leite vaporizado e canela do Cerrado por cima.",
    imagem: "img/cappuccino.jpg",
  },
  {
    id: 4,
    nome: "Latte de Baunilha",
    categoria: "cafes",
    preco: 14,
    descricao: "Espresso, leite vaporizado e calda de baunilha feita na casa.",
    imagem: "img/latte.jpg",
  },
  {
    id: 5,
    nome: "Cold Brew da Chapada",
    categoria: "geladas",
    preco: 15,
    descricao: "Extração a frio por dezoito horas, servida com gelo e rodela de laranja.",
    imagem: "img/cold-brew.jpg",
  },
  {
    id: 6,
    nome: "Frappê de Café",
    categoria: "geladas",
    preco: 16,
    descricao: "Espresso batido com gelo, leite e chantili. Também sai sem lactose.",
    imagem: "img/frappe.jpg",
  },
  {
    id: 7,
    nome: "Pão de Queijo Mineiro",
    categoria: "salgados",
    preco: 7,
    descricao: "Porção com quatro unidades de polvilho azedo com queijo canastra.",
    imagem: "img/pao-de-queijo.jpg",
  },
  {
    id: 8,
    nome: "Torta de Frango",
    categoria: "salgados",
    preco: 13,
    descricao: "Fatia generosa com massa amanteigada e recheio de frango desfiado.",
    imagem: "img/torta-de-frango.jpg",
  },
  {
    id: 9,
    nome: "Bolo de Milho Verde",
    categoria: "doces",
    preco: 9.5,
    descricao: "Fatia de bolo cremoso feito com milho da feira do produtor.",
    imagem: "img/bolo-de-milho.jpg",
  },
  {
    id: 10,
    nome: "Brownie de Castanha",
    categoria: "doces",
    preco: 11,
    descricao: "Chocolate meio amargo com castanha-do-pará. Sem glúten.",
    imagem: "img/brownie.jpg",
  },
];

const ROTULOS_CATEGORIA = {
  cafes: "Cafés",
  geladas: "Bebidas geladas",
  salgados: "Salgados",
  doces: "Doces",
};

const formatadorMoeda = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

function formatarPreco(valor) {
  return formatadorMoeda.format(valor);
}
```

São **exatamente** os dez produtos que você escreveu à mão nas Aulas 03 e 04, com os mesmos nomes, os mesmos preços e as mesmas quatro categorias — agora como dados, não como marcação. Este array é o contrato do projeto: ele vira `js/dados.js` na Aula 09, `data/produtos.json` na Aula 10 e as linhas da sua API na Unidade 3. Não invente produto novo aqui.

Coloque as dez imagens em `img/`. Se ainda não tem as fotos, use qualquer arquivo `.jpg` com o nome certo — o importante hoje é a estrutura. Nomes de arquivo sempre em minúsculas, sem acento e sem espaço: servidores Linux (como o do GitHub Pages) diferenciam maiúsculas de minúsculas, e `Café.JPG` funciona no seu Windows e quebra no ar.

### Passo 3 — o cardápio renderizado a partir dos dados

Em `cardapio.html`, substitua os quatro grids escritos à mão por **um** contêiner vazio e o molde. As quatro `<section>` por categoria deixam de existir como marcação — mas as âncoras `#cafes`, `#geladas`, `#salgados` e `#doces` **não podem sumir**: os botões "Ver" dos destaques de `index.html` (Aula 04) e a `<nav>` de atalhos apontam para elas. A solução é preservá-las como alvos de rolagem dentro da própria `<nav>` de atalhos, que agora vira o filtro visual do cardápio:

`cardapio.html` (trecho do `<main>`)

```html
<section class="container py-5" aria-labelledby="titulo-cardapio">
  <h2 id="titulo-cardapio" class="mb-4">Nosso cardápio</h2>

  <nav aria-label="Seções do cardápio" class="mb-4">
    <ul class="nav gap-2">
      <li class="nav-item"><a class="btn btn-sm btn-cafe-vazado" id="cafes" href="#cafes">Cafés</a></li>
      <li class="nav-item"><a class="btn btn-sm btn-cafe-vazado" id="geladas" href="#geladas">Bebidas geladas</a></li>
      <li class="nav-item"><a class="btn btn-sm btn-cafe-vazado" id="salgados" href="#salgados">Salgados</a></li>
      <li class="nav-item"><a class="btn btn-sm btn-cafe-vazado" id="doces" href="#doces">Doces</a></li>
    </ul>
  </nav>

  <div class="row row-cols-1 row-cols-sm-2 row-cols-lg-3 g-4" id="lista-produtos"></div>

  <p class="text-center text-secondary d-none" id="cardapio-vazio" role="status">
    Nenhum item do cardápio para mostrar.
  </p>
</section>

<template id="template-produto">
  <div class="col">
    <article class="card h-100 card-produto">
      <img class="card-img-top" src="" alt="">
      <div class="card-body d-flex flex-column">
        <span class="badge text-bg-secondary align-self-start mb-2" data-campo="categoria"></span>
        <h3 class="card-title h5" data-campo="nome"></h3>
        <p class="card-text flex-grow-1" data-campo="descricao"></p>
        <p class="preco fw-bold mb-0" data-campo="preco"></p>
      </div>
    </article>
  </div>
</template>
```

Agora a função que transforma um objeto em um card, e a que desenha a lista inteira:

`js/app.js`

```js
function criarCardProduto(produto) {
  const molde = document.querySelector("#template-produto");
  const copia = molde.content.cloneNode(true);

  const artigo = copia.querySelector(".card-produto");
  artigo.dataset.id = produto.id;
  artigo.dataset.categoria = produto.categoria;

  const imagem = copia.querySelector(".card-img-top");
  imagem.src = produto.imagem;
  imagem.alt = `Foto de ${produto.nome}`;
  imagem.loading = "lazy";

  copia.querySelector('[data-campo="categoria"]').textContent =
    ROTULOS_CATEGORIA[produto.categoria];
  copia.querySelector('[data-campo="nome"]').textContent = produto.nome;
  copia.querySelector('[data-campo="descricao"]').textContent = produto.descricao;
  copia.querySelector('[data-campo="preco"]').textContent = formatarPreco(produto.preco);

  return copia;
}

function renderizarProdutos(lista) {
  const container = document.querySelector("#lista-produtos");
  const aviso = document.querySelector("#cardapio-vazio");

  container.replaceChildren();
  aviso.classList.toggle("d-none", lista.length > 0);

  const fragmento = document.createDocumentFragment();
  for (const produto of lista) {
    fragmento.appendChild(criarCardProduto(produto));
  }
  container.appendChild(fragmento);
}

function iniciarCardapio() {
  const container = document.querySelector("#lista-produtos");
  if (!container) return; // não estamos no cardapio.html

  renderizarProdutos(produtos);

  container.addEventListener("click", (evento) => {
    const card = evento.target.closest(".card-produto");
    if (!card) return;
    const id = Number(card.dataset.id);
    const produto = produtos.find((p) => p.id === id);
    console.log("card clicado:", produto.nome, formatarPreco(produto.preco));
  });
}
```

O ouvinte de clique já usa delegação: um só, no contêiner, atendendo os dez cards e os que vierem. Por enquanto ele só imprime no Console — na Aula 08 esse mesmo ouvinte vai jogar o produto no carrinho.

> **⚠️ Cuidado**
> Os quatro `id` que sobraram na `<nav>` (`cafes`, `geladas`, `salgados`, `doces`) existem para que os links antigos continuem funcionando: `cardapio.html#geladas` ainda leva alguém à página certa, agora rolando até a barra de atalhos em vez de até uma seção. Na Aula 08, quando o filtro por categoria entrar, esses mesmos links passam a acionar o filtro — e aí eles voltam a fazer o que prometem. Não apague nem renomeie esses `id`: eles são referenciados por `index.html` e pela `<nav>` do cabeçalho.

### Passo 4 — botão de tema claro/escuro com memória

O Bootstrap 5.3 troca de tema pelo atributo `data-bs-theme` na tag `<html>`. Um botão na navbar, presente em todas as páginas:

`index.html`, `cardapio.html` e `contato.html` (trecho da navbar)

```html
<button class="btn btn-cafe-vazado btn-sm ms-lg-3" type="button" id="btn-tema" aria-pressed="false">
  Tema escuro
</button>
```

`js/app.js`

```js
const CHAVE_TEMA = "cafe-cerrado:tema";

function aplicarTema(tema, botao) {
  document.documentElement.setAttribute("data-bs-theme", tema);
  botao.setAttribute("aria-pressed", String(tema === "dark"));
  botao.textContent = tema === "dark" ? "Tema claro" : "Tema escuro";
}

function temaInicial() {
  const salvo = localStorage.getItem(CHAVE_TEMA);
  if (salvo === "dark" || salvo === "light") return salvo;

  const prefereEscuro = window.matchMedia("(prefers-color-scheme: dark)").matches;
  return prefereEscuro ? "dark" : "light";
}

function iniciarTema() {
  const botao = document.querySelector("#btn-tema");
  if (!botao) return;

  aplicarTema(temaInicial(), botao);

  botao.addEventListener("click", () => {
    const atual = document.documentElement.getAttribute("data-bs-theme");
    const novo = atual === "dark" ? "light" : "dark";
    aplicarTema(novo, botao);
    localStorage.setItem(CHAVE_TEMA, novo);
  });
}
```

Três decisões que valem comentário. O estado inicial respeita a preferência do sistema operacional (`prefers-color-scheme`) quando não há escolha salva — é a mesma consulta de mídia que você usou no CSS na Aula 05. `aria-pressed` transforma o botão em um interruptor que leitores de tela anunciam como "pressionado" ou "não pressionado". E `localStorage` guarda a escolha no navegador da pessoa, sobrevivendo ao fechamento da aba — é a primeira vez que o Café Cerrado tem memória.

### Passo 5 — validação acessível do formulário de contato

O formulário de `contato.html` **não muda de estrutura**: continuam ali os dois `<fieldset>` com `<legend>`, o `<select>` de assunto com `<optgroup>`, telefone, CEP, pessoas, data, horário, os rádios de canal, o checkbox de novidades e o de consentimento — treze campos, os mesmos das Aulas 03, 04 e 06, que o Marco 1 cobre. Três acréscimos, e só:

1. `id="form-contato"` e `novalidate` no `<form>`;
2. um `<p class="invalid-feedback d-block m-0" id="erro-…">` logo abaixo de cada campo que você vai validar, com o `id` do campo no nome (`erro-nome`, `erro-email`, `erro-mensagem`) e um `aria-describedby` no campo apontando para ele;
3. nada na região viva: o `<p id="status-envio">` da Aula 06 continua exatamente como está, e é ele que o JavaScript vai usar.

`contato.html` (os três campos que ganham parágrafo de erro; o restante do formulário fica intacto)

```html
<div class="mb-3">
  <label class="form-label" for="nome">Nome completo <span class="obrigatorio">*</span></label>
  <input class="form-control" type="text" id="nome" name="nome"
         required minlength="3" maxlength="80" autocomplete="name"
         aria-describedby="erro-nome">
  <p class="invalid-feedback d-block m-0" id="erro-nome"></p>
</div>

<div class="mb-3">
  <label class="form-label" for="email">E-mail <span class="obrigatorio">*</span></label>
  <input class="form-control" type="email" id="email" name="email"
         required autocomplete="email" aria-describedby="erro-email">
  <p class="invalid-feedback d-block m-0" id="erro-email"></p>
</div>

<div class="mb-3">
  <label class="form-label" for="mensagem">Mensagem <span class="obrigatorio">*</span></label>
  <textarea class="form-control" id="mensagem" name="mensagem" rows="5"
            required minlength="10" maxlength="500"
            aria-describedby="erro-mensagem"></textarea>
  <p class="invalid-feedback d-block m-0" id="erro-mensagem"></p>
</div>
```

E, no fim do `<form>`, o botão e a região viva que já existiam desde a Aula 06 — só confira que continuam lá:

```html
<button class="btn btn-cafe btn-enviar" type="submit" data-estado="pronto">Enviar mensagem</button>
<button class="btn btn-cafe-vazado" type="reset">Limpar formulário</button>

<p class="status-envio" id="status-envio" aria-live="polite" aria-atomic="true"></p>
```

`js/app.js`

```js
function mensagemDeErro(campo) {
  const v = campo.validity;
  if (v.valueMissing) return "Este campo é obrigatório.";
  if (v.typeMismatch) return "Digite um e-mail no formato nome@dominio.com.";
  if (v.tooShort) return `Escreva pelo menos ${campo.minLength} caracteres.`;
  return "Valor inválido.";
}

function validarCampo(campo) {
  const alvoDoErro = document.querySelector(`#erro-${campo.id}`);
  const valido = campo.checkValidity();

  campo.setAttribute("aria-invalid", String(!valido));
  campo.classList.toggle("is-invalid", !valido);
  alvoDoErro.textContent = valido ? "" : mensagemDeErro(campo);

  return valido;
}

function iniciarContato() {
  const form = document.querySelector("#form-contato");
  if (!form) return;

  const campos = [form.elements.nome, form.elements.email, form.elements.mensagem];
  const status = document.querySelector("#status-envio");

  for (const campo of campos) {
    // valida ao sair do campo e, depois do primeiro erro, a cada tecla
    campo.addEventListener("blur", () => validarCampo(campo));
    campo.addEventListener("input", () => {
      if (campo.getAttribute("aria-invalid") === "true") validarCampo(campo);
    });
  }

  form.addEventListener("submit", (evento) => {
    evento.preventDefault();

    const invalidos = campos.filter((campo) => !validarCampo(campo));

    if (invalidos.length > 0) {
      status.textContent = `Corrija ${invalidos.length} campo(s) antes de enviar.`;
      status.className = "status-envio text-danger";
      invalidos[0].focus(); // leva a pessoa direto ao primeiro problema
      return;
    }

    status.textContent = `Obrigado, ${form.elements.nome.value.trim()}! Sua mensagem foi registrada.`;
    status.className = "status-envio text-success";
    form.reset();
    for (const campo of campos) {
      campo.removeAttribute("aria-invalid");
      campo.classList.remove("is-invalid");
      document.querySelector(`#erro-${campo.id}`).textContent = "";
    }
  });
}
```

Repare no ritmo da validação: o erro aparece quando a pessoa **sai** do campo (`blur`), não a cada tecla — ninguém merece ver "e-mail inválido" ao digitar a primeira letra. Depois que o erro apareceu, aí sim o `input` revalida a cada tecla, para o erro sumir assim que for corrigido. Esse é o comportamento que formulários bem-feitos têm.

Ainda não enviamos nada para lugar nenhum — a mensagem só é registrada na tela. O envio real vai depender do `fetch` da Aula 10 e da API da Unidade 3.

### Como testar

1. Abra `cardapio.html` com o Live Server. Devem aparecer dez cards em três colunas no desktop, uma no celular.
2. No DevTools, aba Elements, expanda `#lista-produtos`: os `<div class="col">` estão lá, mas não estão no arquivo `.html`. Foi o JavaScript que os criou.
3. Cole `document.querySelectorAll(".card-produto").length` no Console. Deve devolver `10`.
4. Clique em um card e confira a linha impressa no Console, com nome e preço formatado em reais.
5. Clique no botão de tema. A página inteira troca de cor; recarregue (<kbd>F5</kbd>) e a escolha permanece. No DevTools, Application → Local Storage, veja a chave `cafe-cerrado:tema`.
6. Em `contato.html`, clique em "Enviar mensagem" com tudo vazio: três mensagens aparecem, o foco vai para o campo Nome e a região de status anuncia "Corrija 3 campo(s) antes de enviar".
7. Digite `ana@` no e-mail e saia do campo: aparece a mensagem de formato. Complete para `ana@exemplo.br` e a mensagem some sozinha.
8. Rode o Lighthouse de novo. A nota de acessibilidade não pode ter caído — se caiu, o culpado costuma ser uma imagem gerada sem `alt`.

Commit com mensagem descritiva:

```bash
git add .
git commit -m "feat: cardapio renderizado por JS, alternancia de tema e validacao do formulario"
git push
```

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Preveja a saída de cada linha **sem rodar**, depois confira no Console:

```js
const p = { nome: "Espresso do Cerrado", preco: 6, extras: { canela: false } };
const copia = { ...p, preco: 7 };
copia.extras.canela = true;

console.log(p.preco);
console.log(p.extras.canela);
console.log(Object.keys(copia).length);
console.log(p.avaliacao?.media ?? "sem nota");
```

**A2.** O código abaixo está no `<head>` sem `defer` e falha com `Uncaught TypeError: Cannot read properties of null (reading 'addEventListener')`. Explique em duas linhas por que `document.querySelector("#btn-tema")` devolveu `null` e cite **duas** formas diferentes de corrigir.

```js
const botao = document.querySelector("#btn-tema");
botao.addEventListener("click", () => console.log("clique"));
```

**A3.** Qual é a diferença entre `evento.target` e `evento.currentTarget` no ouvinte de `#lista-produtos` do Passo 3? Clique no `<h3>` de um card e escreva o valor de cada um.

**A4.** Complete a função para que ela devolva o rótulo legível de uma categoria e a string `"Outros"` quando a categoria não existir no dicionário:

```js
function rotuloDaCategoria(chave) {
  return ROTULOS_CATEGORIA[chave];
}

rotuloDaCategoria("doces");    // deve devolver "Doces"
rotuloDaCategoria("bebidas");  // deve devolver "Outros"
```

**A5.** Verdadeiro ou falso, com justificativa de uma linha cada: (a) `card.dataset.id === 3` é `true` quando o HTML tem `data-id="3"`; (b) `textContent` é mais seguro que `innerHTML` para exibir um nome digitado por alguém; (c) `querySelectorAll` devolve um array; (d) com `novalidate` no `<form>`, `campo.validity.valueMissing` para de funcionar.

**A6.** Em três linhas, explique por que o array `produtos` guarda `preco: 8.5` e `categoria: "cafes"` em vez de `preco: "R$ 8,50"` e `categoria: "Cafés"`.

### Nível B — Aplicação

**B1.** Contador de itens no cardápio. Acima da grade de cards, mostre em um `<p id="contador-cardapio">` a frase "10 itens no cardápio", calculada a partir do array e atualizada dentro de `renderizarProdutos`.

Resultado esperado: apagar dois objetos do array e recarregar faz o texto virar "8 itens no cardápio", sem editar o HTML.

<details markdown="1">
<summary>Dica</summary>

O número vem de `lista.length`, não de contar elementos no DOM. Atualize o texto no mesmo lugar onde você já decide se o aviso de lista vazia aparece.
</details>

**B2.** Destaque por faixa de preço. Faça os cards de produtos com preço abaixo de R$ 10 receberem a classe `.economico`, e defina no `css/estilo.css` uma borda ou selo para essa classe. O JavaScript não pode conter nenhuma cor.

Resultado esperado: três cards destacados (`id` 1, 2 e 6); mudar o preço de um produto no array muda o destaque ao recarregar, sem tocar no CSS.

<details markdown="1">
<summary>Dica</summary>

`artigo.classList.toggle("economico", produto.preco < 10)` resolve em uma linha, dentro de `criarCardProduto`.
</details>

**B3.** Detalhes sob demanda. Adicione ao template um botão "Ver detalhes" e um parágrafo escondido com uma informação extra (por exemplo, `Categoria: Cafés · Código 3`). Use delegação no contêiner e mantenha `aria-expanded` sincronizado no botão.

Resultado esperado: cada card abre e fecha o próprio parágrafo; o `aria-expanded` do botão alterna entre `"true"` e `"false"` na aba Elements.

<details markdown="1">
<summary>Dica</summary>

No ouvinte do contêiner, use `evento.target.closest("[data-acao='detalhes']")` para saber se o clique foi no botão, e `botao.closest(".card-produto")` para achar o card correspondente.
</details>

**B4.** Contador de caracteres da mensagem. No `contato.html`, mostre abaixo do `<textarea>` quantos caracteres faltam para atingir o `minlength`, atualizado a cada tecla, com `aria-live="polite"`.

Resultado esperado: com o campo vazio, "faltam 10 caracteres"; ao passar do mínimo, "mensagem com tamanho suficiente".

<details markdown="1">
<summary>Dica</summary>

O evento é `input`. O número que falta é `campo.minLength - campo.value.length`, nunca menor que zero — `Math.max(0, …)` resolve.
</details>

**B5.** Ordem alfabética por acento correto. Renderize o cardápio em ordem alfabética de nome usando `Intl.Collator("pt-BR")` em vez de comparar strings direto, e escreva no README uma frase explicando a diferença.

Resultado esperado: nenhum nome acentuado fica fora de lugar; a lista começa por "Bolo de Milho Verde" e termina em "Torta de Frango".

<details markdown="1">
<summary>Dica</summary>

`const comparador = new Intl.Collator("pt-BR");` e depois `[...produtos].sort((a, b) => comparador.compare(a.nome, b.nome))`. Copie o array antes de ordenar — a próxima aula explica por quê.
</details>

### Nível C — Desafio

**C1.** Renderização à prova de dados sujos. Alguém vai alimentar o array `produtos` a partir de uma planilha, e a planilha é bagunçada: pode faltar `descricao`, o `preco` pode vir como a string `"12,50"`, a `imagem` pode apontar para um arquivo inexistente e o `nome` pode conter `<script>alert(1)</script>`. Torne `criarCardProduto` resistente aos quatro casos, sem esconder problemas: campo ausente vira texto padrão, preço em string é convertido, imagem quebrada cai numa imagem genérica e o nome com HTML aparece **como texto**, sem executar nada.

Resultado esperado: com um array proposital de cinco itens defeituosos, a página renderiza os cinco cards sem nenhum erro no Console, e o card do nome malicioso mostra literalmente `<script>alert(1)</script>` na tela.

<details markdown="1">
<summary>Dica</summary>

Para o preço, `Number(String(valor).replace(",", "."))` seguido de `Number.isFinite`. Para a imagem, o evento `error` do próprio `<img>` (`imagem.addEventListener("error", () => { imagem.src = "img/sem-foto.jpg"; })`). Para o nome, você já está protegido se usar `textContent` — comprove trocando por `innerHTML` e vendo a diferença. E `?? "Descrição em breve."` cobre o campo ausente.
</details>

## 🏆 Desafios

### ⭐ O caçador de `null`
Tags: javascript, dom, bug, devtools

Um colega mexeu no `app.js` do Café Cerrado antes de sair de férias e agora o cardápio não aparece. O Console mostra `Uncaught TypeError: Cannot read properties of null (reading 'content')` e mais nada. Ele plantou três defeitos diferentes neste trecho — um de seletor, um de argumento esquecido e um de formatação, e só o primeiro produz mensagem de erro. Encontre os três **usando o DevTools**, não lendo o código linha a linha até adivinhar.

```js
// js/app.js — versão com defeitos
const molde = document.querySelector("#template_produto");

function criarCardProduto(produto) {
  const copia = molde.content.cloneNode();
  copia.querySelector('[data-campo="nome"]').textContent = produto.nome;
  copia.querySelector('[data-campo="preco"]').textContent = "R$ " + produto.preco;
  return copia;
}

function renderizarProdutos(lista) {
  const container = document.querySelector("#lista-produtos");
  for (const produto of lista) {
    container.appendChild(criarCardProduto(produto));
  }
}

renderizarProdutos(produtos);
```

**Critérios de pronto**

- Um arquivo `DEPURACAO.md` no repositório lista os três defeitos, cada um com: a mensagem de erro exata que ele produz, o recurso do DevTools que o revelou e a correção aplicada.
- Pelo menos um dos defeitos foi localizado com um ponto de parada (aba Sources ou `debugger;`), com print da tela pausada mostrando o valor da variável no painel Scope.
- Depois das três correções, os dez cards aparecem e o Console fica limpo.
- Uma frase final explica por que `cloneNode()` sem argumento devolve um nó vazio.

<details markdown="1">
<summary>Pistas</summary>

1. A primeira mensagem já entrega o primeiro defeito: se `molde` é `null`, o `querySelector` não achou nada. Compare caractere por caractere o seletor com o `id` no HTML — traço e sublinhado não são a mesma coisa.
2. `cloneNode()` aceita um argumento booleano. Leia na MDN o que muda entre `cloneNode()` e `cloneNode(true)`.
3. Coloque `debugger;` na primeira linha de `criarCardProduto` e inspecione `copia` no painel Scope: quantos filhos ele tem?
4. O terceiro defeito não gera erro — gera texto errado na tela. Compare o preço exibido do "Coado da Casa" com o do "Espresso do Cerrado" e pense no que `"R$ " + 6` produz.
</details>

### ⭐⭐ O cardápio que virou porta de entrada
Tags: javascript, dom, seguranca, refatoracao

Troque `textContent` por `innerHTML` em `criarCardProduto` e adicione ao array um produto chamado `<img src=x onerror="document.body.style.filter='invert(1)'">`. Recarregue a página. O que acontece é uma versão inofensiva de um ataque XSS armazenado — o mesmo mecanismo que, com outro código dentro, rouba a sessão de quem visita o site. Sua tarefa é entender o mecanismo, medir o estrago possível e blindar o render.

**Critérios de pronto**

- Um print (ou GIF) mostra a página sendo alterada pelo "produto" malicioso, e o `DEPURACAO.md` explica em três linhas por que o `onerror` roda mesmo sem ninguém clicar em nada.
- A versão corrigida usa `textContent` para todo dado variável e continua funcionando com o produto malicioso no array — que agora aparece como texto na tela.
- Existe uma função `escaparHtml(texto)` no projeto, com teste manual documentado, para o caso em que você **precisa** montar HTML (por exemplo, destacar o termo buscado em negrito na Aula 08).
- O README ganha um parágrafo curto respondendo: se os produtos viessem de um banco de dados alimentado por outros usuários, em que camadas essa proteção precisaria existir?

<details markdown="1">
<summary>Pistas</summary>

1. Procure "Cross-site scripting" na MDN e leia a diferença entre XSS refletido e armazenado.
2. O `onerror` dispara porque `src=x` é um caminho inválido — o navegador tenta carregar, falha, e executa o manipulador. Nenhum clique é necessário.
3. Uma implementação curta de `escaparHtml` usa um elemento descartável: crie um `div`, atribua o texto com `textContent` e leia de volta o `innerHTML`.
4. A resposta do README tem mais de uma camada: entrada (validação), armazenamento e saída (escape na renderização). Pense em qual delas é obrigatória mesmo que as outras existam.
</details>

### ⭐⭐ Um ouvinte para duzentos cards
Tags: dom, eventos, performance, devtools

Delegação parece um detalhe de estilo até você medir. Gere 200 produtos falsos, renderize duas versões do cardápio — uma registrando `addEventListener` em cada card, outra com um único ouvinte no contêiner — e compare tempo de renderização e memória. Depois responda com dados: a delegação vale a pena por performance, por manutenção, ou pelos dois?

**Critérios de pronto**

- Um script gera os 200 produtos a partir do array real (variando nome, preço e categoria), sem 200 objetos escritos à mão.
- O tempo das duas versões é medido com `performance.now()` em volta da renderização, com pelo menos 5 execuções de cada e a mediana registrada.
- Uma tabela no `DEPURACAO.md` compara: número de ouvintes (visível em Elements → Event Listeners), tempo mediano de render e o que acontece com cada versão quando a lista é re-renderizada 10 vezes seguidas.
- Um parágrafo final defende uma das duas abordagens para o Café Cerrado, citando os números obtidos.

<details markdown="1">
<summary>Pistas</summary>

1. `Array.from({ length: 200 }, (_, i) => ({ ...produtos[i % produtos.length], id: i + 1 }))` gera a base sem repetir código.
2. `performance.now()` devolve milissegundos com casas decimais; guarde o valor antes e depois e subtraia.
3. No DevTools, o painel Memory tira um "heap snapshot"; compare o número de objetos `EventListener` entre as duas versões.
4. Re-renderizar 10 vezes é onde a versão sem delegação escorrega: descubra o que acontece com os ouvintes dos elementos removidos e por que isso pode virar vazamento de memória.
</details>

### ⭐⭐⭐ O cardápio que lembra de você
Tags: javascript, dom, eventos, acessibilidade

Quem entra no Café Cerrado toda semana sempre pede as mesmas duas coisas. Dê a essa pessoa um jeito de marcar favoritos que sobreviva ao fechamento do navegador, funcione só com teclado, seja anunciado corretamente por leitores de tela e não dependa de nenhuma biblioteca. É um exercício completo de estado, persistência, renderização e acessibilidade — as quatro coisas de hoje juntas.

**Critérios de pronto**

- Cada card tem um botão de favoritar com `aria-pressed` refletindo o estado, rótulo acessível que inclui o nome do produto (por exemplo, "Favoritar Espresso do Cerrado") e foco visível.
- Os favoritos são guardados em `localStorage` sob uma única chave, como array de `id`, e sobrevivem a recarregar a página e fechar o navegador.
- Existe um botão "Mostrar só favoritos" que alterna a lista renderizada, com contagem ("3 favoritos") atualizada, e um estado vazio próprio ("Você ainda não marcou favoritos").
- Toda a interação funciona sem mouse: <kbd>Tab</kbd> até o botão, <kbd>Enter</kbd> ou <kbd>Espaço</kbd> para marcar, e a mudança é anunciada em uma região `aria-live`.
- O estado dos favoritos vive em **uma** variável de estado; a tela é sempre redesenhada a partir dela, nunca corrigida na mão.
- O `localStorage` é lido dentro de `try/catch`: em janela anônima com armazenamento bloqueado, o site continua funcionando sem favoritos, em vez de quebrar.

<details markdown="1">
<summary>Pistas</summary>

1. `localStorage` só guarda strings: `JSON.stringify(favoritos)` para gravar, `JSON.parse(localStorage.getItem(chave) ?? "[]")` para ler.
2. Um `Set` é mais confortável que um array para "contém / adiciona / remove"; converta com `[...conjunto]` na hora de salvar.
3. Um `<button>` de verdade já responde a <kbd>Enter</kbd> e <kbd>Espaço</kbd> sem nenhum código. Se você usar `<div>` ou `<span>`, vai ter que reimplementar teclado, foco e papel — não faça isso.
4. Para o anúncio, uma única região `aria-live="polite"` na página, com texto trocado a cada ação ("Espresso do Cerrado adicionado aos favoritos"), é melhor do que uma região por card.
5. Ao re-renderizar depois de favoritar, o foco se perde. Guarde o `id` do card afetado e devolva o foco ao botão correspondente depois do `render` — esse detalhe é o que separa um protótipo de um componente utilizável.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `Uncaught TypeError: Cannot read properties of null (reading 'addEventListener')` | O `querySelector` não achou o elemento: `id` errado, ou script sem `defer` rodando antes do HTML | Conferir o seletor no Elements e garantir `defer` na tag `<script>` |
| `Uncaught ReferenceError: produtos is not defined` | O array está declarado depois do uso, ou em outro arquivo não carregado | Declarar dados no topo do `app.js`; conferir a ordem das tags `<script>` |
| `Uncaught TypeError: cards.map is not a function` | `querySelectorAll` devolve `NodeList`, não array | Converter com `[...cards]` ou `Array.from(cards)` antes de `map`/`filter` |
| A página recarrega e o formulário "some" ao enviar | Falta `evento.preventDefault()` no ouvinte de `submit` | Chamar `preventDefault()` na primeira linha do ouvinte |
| Os cards aparecem, mas o clique neles não faz nada | Ouvintes registrados antes do `render`, em elementos que foram substituídos | Usar delegação: um ouvinte no contêiner com `evento.target.closest(…)` |
| `Uncaught TypeError: Assignment to constant variable.` | Reatribuição de uma variável `const` | Trocar para `let` — ou, se for objeto, alterar a propriedade em vez da variável |
| O preço aparece como `R$ 6.5` em vez de `R$ 6,50` | Concatenação manual em vez de formatação por localidade | Usar `Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" })` |
| `card.dataset.id === 3` é sempre `false` | Todo valor de `dataset` é string | Comparar com `Number(card.dataset.id) === 3` |
| O card do produto aparece vazio, sem erro no Console | `cloneNode()` sem `true` clonou o nó sem os filhos | Usar `molde.content.cloneNode(true)` |
| As imagens não carregam no GitHub Pages, mas funcionam localmente | Diferença de maiúsculas/minúsculas no nome do arquivo | Padronizar nomes minúsculos, sem acento e sem espaço |

## 🏠 Para praticar depois da aula (1 h)

No repositório do **seu projeto autoral**:

1. Crie `js/app.js` e vincule com `defer` em todas as páginas.
2. Modele os itens do seu domínio (produtos, serviços, plantas, quadras, vagas) como um array de objetos com, no mínimo, os campos `id`, `nome`, `categoria`, `preco` (ou outro valor numérico) e `descricao`.
3. Substitua os cards escritos à mão de uma das páginas pela renderização a partir desse array, usando `<template>` e `textContent`.
4. Implemente **uma** interação com evento: alternância de tema, abrir/fechar detalhes de um item ou menu próprio — com o atributo ARIA correspondente sincronizado.
5. Adicione ao seu formulário a validação de pelo menos dois campos com mensagens em português e foco no primeiro campo inválido.

**Critério de pronto:** o Console fica sem erros nas três páginas; os cards existem no DOM mas não no arquivo `.html`; o formulário mostra mensagem própria e não recarrega a página ao ser enviado vazio.

**Guarde no seu repositório:** commit + push.

**Leitura dirigida (se você tem acesso a uma biblioteca virtual pela sua instituição):** Queirós e Portela, capítulo da camada de comportamento (JavaScript); Purewal, capítulo de JavaScript e interatividade.

## ✅ Checkpoint do projeto

- [ ] `js/app.js` existe e é carregado com `defer` em todas as páginas do projeto.
- [ ] O Console está limpo em todas as páginas — inclusive naquelas onde o script não tem o que fazer.
- [ ] Os itens do projeto vivem em um array de objetos com campos bem escolhidos, e não em HTML repetido.
- [ ] Pelo menos uma lista é renderizada a partir dos dados, com `<template>` e `DocumentFragment`.
- [ ] Nenhum dado variável é inserido com `innerHTML`.
- [ ] Existe um estado vazio tratado ("nenhum item para mostrar").
- [ ] Há pelo menos um ouvinte por delegação, em vez de um ouvinte por item.
- [ ] O formulário valida com mensagens próprias, `aria-invalid`, `aria-describedby` e região `aria-live`.
- [ ] Nenhuma cor, tamanho ou espaçamento foi escrito dentro do JavaScript.
- [ ] Commit e push feitos, com mensagem descritiva.

## 📚 Para aprofundar

- [MDN — Introdução ao DOM](https://developer.mozilla.org/pt-BR/docs/Web/API/Document_Object_Model/Introduction): a visão geral da árvore de nós, em português.
- [MDN — Introdução aos eventos](https://developer.mozilla.org/pt-BR/docs/Learn/JavaScript/Building_blocks/Events): leia com atenção a parte de propagação e delegação.
- [MDN — `Element.closest()`](https://developer.mozilla.org/pt-BR/docs/Web/API/Element/closest): curto e essencial para delegação.
- [MDN — `<template>`](https://developer.mozilla.org/pt-BR/docs/Web/HTML/Element/template): por que o conteúdo é inerte e como cloná-lo.
- [MDN — Constraint Validation API](https://developer.mozilla.org/en-US/docs/Web/HTML/Constraint_validation): a lista completa das propriedades de `validity`.
- [MDN — `Intl.NumberFormat`](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat): formatação de moeda e de números por localidade.
- [web.dev — Cross-site scripting](https://web.dev/articles/xss): por que `innerHTML` com dado de usuário é perigoso.
- QUEIRÓS, Ricardo; PORTELA, Filipe. *Introdução ao Desenvolvimento Moderno para a Web*. FCA, 2018 — camada de comportamento: JavaScript.
- PUREWAL, Semmy. *Aprendendo a Desenvolver Aplicações Web*. Novatec, 2014 — JavaScript e interatividade.
- LOUDON, Kyle. *Desenvolvimento de Grandes Aplicações Web*. Novatec, 2019 — organização de código JavaScript.

Na próxima aula as funções deixam de ser coadjuvantes: arrow functions, callbacks e as operações de vetores (`map`, `filter`, `find`, `sort`, `reduce`) entram em cena, e o cardápio ganha busca por nome, filtro por categoria, ordenação por preço e um carrinho que soma sozinho.
