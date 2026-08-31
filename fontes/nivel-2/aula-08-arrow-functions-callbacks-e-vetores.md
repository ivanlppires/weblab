# Aula 08 — Arrow functions, callbacks e operações em vetores

> **Nível 2 — Desenvolvimento Web** · Unidade 2: Web dinâmica client-side
> WebLab · curso aberto de desenvolvimento web
> **Tempo estimado:** 3 blocos de 50 min + 1 h de prática

Na Aula 07 você plantou uma ideia quase de passagem: em JavaScript, função é um valor. Ela apareceu no `addEventListener`, quando você entregou uma função ao navegador para que ele a chamasse depois. Hoje essa ideia deixa de ser detalhe e vira a ferramenta principal. Arrow functions, callbacks e os métodos de array que os recebem são o vocabulário com que se escreve JavaScript profissional — e são exatamente o que as Promises da próxima aula pressupõem que você já domina.

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Escolher entre declaração, expressão e arrow function, justificando a escolha pelo comportamento de `this` e de hoisting.
- Escrever arrow functions em todos os seus níveis de concisão, incluindo retorno implícito de objeto.
- Explicar o que é um callback e escrever suas próprias funções de ordem superior.
- Processar dados com `forEach`, `map`, `filter`, `find`, `some`, `every`, `reduce` e `sort`, sabendo o que cada um devolve.
- Encadear operações de array em uma linha de produção legível, sem alterar o array original.
- Aplicar o padrão estado → derivação → renderização para combinar busca, filtro e ordenação na mesma tela.
- Reduzir trabalho desnecessário com um `debounce` escrito por você, e medir o efeito no DevTools.

## 📋 Pré-requisitos

Na aula passada o Café Cerrado ganhou `js/app.js`: o cardápio virou o array `produtos` e passou a ser desenhado por `renderizarProdutos`, o formulário de contato passou a validar com mensagens acessíveis, e um ouvinte por delegação já escuta os cliques nos cards. Hoje o cardápio ganha inteligência — busca, filtro por categoria, ordenação por preço e um carrinho que soma sozinho —, tudo construído com callbacks e métodos de array.

Checklist antes de começar:

- [ ] `js/app.js` da Aula 07 funcionando: dez cards renderizados a partir do array `produtos`.
- [ ] O elemento `<template id="template-produto">` e o contêiner `#lista-produtos` no `cardapio.html`.
- [ ] As funções `criarCardProduto`, `renderizarProdutos` e `formatarPreco` no seu `app.js`.
- [ ] O dicionário `ROTULOS_CATEGORIA` mapeando as chaves de categoria para o texto exibido.
- [ ] Console do DevTools aberto — hoje metade dos exercícios acontece nele.

Do Nível 1 você já traz laços `for` e `for…of` (Aula 12) e funções (Aula 13). Hoje a maioria desses laços vai desaparecer do seu código, substituída por métodos que dizem **o que** você quer, em vez de **como** percorrer.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Três formas de função; arrow functions em detalhe; `this`; callbacks |
| 2 | 50 min | `forEach`, `map`, `filter`, `find`, `reduce`, `sort`; encadeamento e imutabilidade |
| 3 | 50 min | Mão na massa (busca, filtros, ordenação, carrinho) e laboratório |

## 1. Três formas de escrever uma função

```js
// 1. Declaração (function declaration)
function dobrar(numero) {
  return numero * 2;
}

// 2. Expressão de função — a função é um valor guardado numa variável
const triplicar = function (numero) {
  return numero * 3;
};

// 3. Arrow function (ES2015) — a forma que vai dominar seu código daqui em diante
const quadruplicar = (numero) => {
  return numero * 4;
};

dobrar(5);        // 10
triplicar(5);     // 15
quadruplicar(5);  // 20
```

As três são chamadas exatamente do mesmo jeito. As diferenças são três, e todas importam:

**Hoisting.** Declarações são içadas para o topo do escopo: você pode chamar `dobrar(5)` numa linha acima da definição. Expressões e arrows, não — a variável existe, mas ainda não recebeu valor, e você recebe `ReferenceError: Cannot access 'triplicar' before initialization`.

```js
console.log(dobrar(5));      // 10 — funciona, a declaração foi içada
console.log(triplicar(5));   // ReferenceError: Cannot access 'triplicar' before initialization

function dobrar(n) { return n * 2; }
const triplicar = function (n) { return n * 3; };
```

**Nome nas pilhas de erro.** Uma função nomeada aparece com nome no rastro de erro do Console; uma anônima aparece como `<anonymous>`. Atribuir a arrow a uma `const` já resolve: o motor usa o nome da variável.

**`this`.** A diferença mais profunda, tratada na seção 2.4.

Na prática, a convenção que este curso adota é a mesma da maioria dos times: **declaração** para funções nomeadas de topo (`function renderizarProdutos(lista)`), **arrow** para tudo que é passado como argumento (callbacks de evento, de `map`, de `filter`). É o que você já viu no `app.js` da Aula 07.

## 2. Arrow functions em detalhe

### 2.1 Os níveis de encolhimento

Todas as linhas abaixo definem a mesma função:

```js
const dobrar = (numero) => { return numero * 2; };  // forma completa
const dobrar = (numero) => numero * 2;              // sem chaves: retorno IMPLÍCITO
const dobrar = numero => numero * 2;                // 1 parâmetro: parênteses opcionais

const somar = (a, b) => a + b;                      // 2+ parâmetros: parênteses obrigatórios
const agora = () => new Date();                     // sem parâmetros: () obrigatório
const naoFazNada = () => {};                        // corpo vazio: útil como callback padrão
```

Este curso mantém os parênteses mesmo com um parâmetro só (`(numero) => …`). É a convenção do Prettier e do Vue, e evita reescrever a linha quando aparecer um segundo parâmetro. Consistência vale mais que dois caracteres.

### 2.2 A armadilha das chaves

```js
const dobrarErrado = (numero) => { numero * 2 };
dobrarErrado(5);  // undefined

const dobrarCerto = (numero) => { return numero * 2 };
const dobrarMelhor = (numero) => numero * 2;
```

As chaves abrem um **corpo de função comum**, que só devolve algo com `return` explícito. Ou tudo em uma expressão sem chaves, ou chaves com `return`. Não existe meio-termo — e este é o erro número um de quem está aprendendo a sintaxe.

### 2.3 Retornar um objeto exige parênteses

```js
const criarItem = (nome, preco) => { nome, preco };      // undefined — as chaves viram corpo
const criarItemCerto = (nome, preco) => ({ nome, preco }); // objeto, graças aos parênteses
```

Os parênteses avisam o interpretador: "o que vem aqui é uma expressão, não um bloco". Você vai usar isso o tempo todo em `map`, para transformar cada item em um objeto novo.

### 2.4 A diferença que importa: `this`

Arrow functions **não têm `this` próprio**. Elas herdam o `this` do lugar onde foram escritas. Em métodos de objeto, isso quebra tudo:

```js
const carrinho = {
  itens: [
    { nome: "Espresso do Cerrado", preco: 6, quantidade: 2 },
    { nome: "Torta de Frango", preco: 13, quantidade: 1 },
  ],

  // Certo: sintaxe de método — this é o objeto carrinho
  total() {
    return this.itens.reduce((soma, item) => soma + item.preco * item.quantidade, 0);
  },

  // Errado: arrow como método — this NÃO é o carrinho
  quantidadeTotal: () => {
    return this.itens.length;
  },
};

carrinho.total();           // 31.5
carrinho.quantidadeTotal(); // TypeError: Cannot read properties of undefined (reading 'itens')
```

Repare que **dentro** de `total()` a arrow do `reduce` funciona perfeitamente — ela herda o `this` do método, que é o carrinho. Essa herança é justamente a vantagem: antes do ES2015, programadores escreviam `const self = this;` para conseguir o mesmo efeito.

A mesma pegadinha aparece em ouvintes de evento:

```js
botao.addEventListener("click", function () {
  this.disabled = true;              // this é o botão
});

botao.addEventListener("click", () => {
  this.disabled = true;              // this NÃO é o botão
});

botao.addEventListener("click", (evento) => {
  evento.currentTarget.disabled = true;  // funciona sempre, com qualquer sintaxe
});
```

A regra prática que evita o assunto inteiro: **use `evento.currentTarget`, nunca `this`, dentro de ouvintes**. E use sintaxe de método (`total() { }`) quando o objeto precisa se referir a si mesmo.

> **⚠️ Atenção**
> Arrow functions também não têm `arguments`, não podem ser usadas com `new` e não podem ser geradoras. Nada disso atrapalha o que você escreve nesta unidade — mas explica por que uma arrow nunca substitui um construtor ou um método de classe que dependa de `this`.

## 3. Callbacks: funções que viajam

**Callback** é uma função passada como argumento para outra função, que decide **quando** e **quantas vezes** chamá-la. Você já usa desde a Aula 07, sem o nome:

```js
// O navegador chama a sua função quando o clique acontecer — talvez nunca:
botao.addEventListener("click", () => console.log("clicou"));

// setTimeout chama UMA vez, depois do tempo dado (em milissegundos):
setTimeout(() => console.log("2 segundos depois"), 2000);

// setInterval chama REPETIDAMENTE, até você cancelar:
const relogio = setInterval(() => console.log("tique"), 1000);
clearInterval(relogio);
```

Uma função que recebe (ou devolve) outra função é chamada de **função de ordem superior**. Você também escreve as suas:

```js
function processarPedido(pedido, aoConcluir) {
  console.log(`Processando ${pedido}…`);
  aoConcluir(pedido);
}

processarPedido("Pedido #42", (numero) => console.log(`${numero} concluído!`));
```

Callbacks com valor padrão evitam um `if` a cada chamada:

```js
function salvar(dados, aoSucesso = () => {}, aoErro = () => {}) {
  if (!dados.nome) {
    aoErro("Nome é obrigatório.");
    return;
  }
  aoSucesso(dados);
}

salvar({ nome: "Ana" }, (d) => console.log("salvo:", d.nome));
salvar({}, undefined, (mensagem) => console.warn(mensagem));
```

### 3.1 O primeiro contato com o assíncrono

Volte ao `setTimeout` e observe a ordem de execução:

```js
console.log("1 — início");
setTimeout(() => console.log("3 — o callback, depois"), 0);
console.log("2 — fim do script");

// Saída: 1, 2, 3 — mesmo com 0 milissegundos de espera
```

O programa **não para** para esperar. Ele agenda o callback e segue. Essa é a sua primeira visão da execução assíncrona, tema central da próxima aula.

### 3.2 Por que os callbacks não bastaram

Callbacks resolvem bem uma operação. Encadeie três e o código começa a andar de lado:

```js
buscarProdutos((produtos) => {
  buscarCategorias((categorias) => {
    buscarPromocoes((promocoes) => {
      renderizarTudo(produtos, categorias, promocoes);
    });
  });
});
```

Isso ficou conhecido como *callback hell* — ou "pirâmide da perdição". Três problemas: a indentação cresce sem limite, a ordem de leitura não é a ordem de execução, e tratar erro exige repetir verificação em cada nível. Foi exatamente para resolver isso que as **Promises** foram criadas. Você as conhece na próxima aula; hoje basta entender o problema.

> **🧠 Você sabia?**
> A ideia de passar funções como valores não nasceu no JavaScript — vem do Lisp, de 1958, e da programação funcional. `map`, `filter` e `reduce` são desse mesmo tronco: já existiam em Lisp antes de existir mouse. O que mudou foi a escala: em 2004, dois engenheiros do Google publicaram o artigo *MapReduce*, mostrando como aplicar essas duas operações em milhares de máquinas para processar a web inteira. O `map` que você vai escrever agora, em dez produtos, é a mesma ideia — em outra ordem de grandeza.

## 4. Operações em vetores: processar dados sem `for`

Os métodos de array recebem um callback e o aplicam a cada elemento. Eles substituem a maioria dos laços `for` por código mais curto e, principalmente, **declarativo**: você diz o que quer, não como percorrer.

A base de exemplos é o cardápio da Aula 07:

```js
const produtos = [
  { id: 1, nome: "Espresso do Cerrado", categoria: "cafes", preco: 6 },
  { id: 2, nome: "Coado da Casa", categoria: "cafes", preco: 8.5 },
  { id: 3, nome: "Cappuccino Sinop", categoria: "cafes", preco: 12 },
  { id: 4, nome: "Latte de Baunilha", categoria: "cafes", preco: 14 },
  { id: 5, nome: "Cold Brew da Chapada", categoria: "geladas", preco: 15 },
  { id: 6, nome: "Frappê de Café", categoria: "geladas", preco: 16 },
  { id: 7, nome: "Pão de Queijo Mineiro", categoria: "salgados", preco: 7 },
  { id: 8, nome: "Torta de Frango", categoria: "salgados", preco: 13 },
  { id: 9, nome: "Bolo de Milho Verde", categoria: "doces", preco: 9.5 },
  { id: 10, nome: "Brownie de Castanha", categoria: "doces", preco: 11 },
];
```

Cada callback recebe até três argumentos: o **item**, o **índice** e o **array inteiro**. Quase sempre você usa só o primeiro.

### 4.1 `forEach` — faça algo com cada item

```js
produtos.forEach((produto) => console.log(`${produto.nome}: ${produto.preco}`));

produtos.forEach((produto, indice) => {
  console.log(`${indice + 1}. ${produto.nome}`);
});
```

`forEach` devolve `undefined`. Ele existe para o **efeito colateral** (imprimir, inserir no DOM), não para produzir um valor. E não dá para interromper no meio: `break` é erro de sintaxe e `return` só pula um item. Se você precisa parar antes do fim, use `for…of`, `find` ou `some`.

### 4.2 `map` — transforme cada item

```js
const nomes = produtos.map((produto) => produto.nome);
// ["Espresso do Cerrado", "Coado da Casa", "Cappuccino Sinop", …] — 10 nomes

const comDesconto = produtos.map((produto) => ({ ...produto, preco: produto.preco * 0.9 }));
// novo array, 10% mais barato; o array original continua intacto

const opcoes = produtos.map((produto) => `<option value="${produto.id}">${produto.nome}</option>`);
```

`map` sempre devolve um array do **mesmo tamanho** do original. Se o seu `map` não usa o valor devolvido, você queria `forEach`.

### 4.3 `filter` — selecione itens

```js
const cafes = produtos.filter((produto) => produto.categoria === "cafes");      // 4 itens
const baratos = produtos.filter((produto) => produto.preco < 10);               // 4 itens
const nenhum = produtos.filter((produto) => produto.preco > 100);               // [] — array vazio
```

O callback do `filter` é um **teste**: devolva `true` para manter o item, `false` para descartar. O resultado tem de 0 a N itens — e nunca é `null`, o que dispensa verificação antes de percorrer.

### 4.4 `find`, `findIndex`, `some`, `every` e `includes`

```js
produtos.find((p) => p.preco > 12);        // { id: 4, nome: "Latte de Baunilha", … } — o PRIMEIRO
produtos.find((p) => p.preco > 100);       // undefined — cuidado ao acessar .nome depois
produtos.findIndex((p) => p.id === 5);     // 4 — a posição, ou -1 se não achar

produtos.some((p) => p.preco > 13);        // true  — ALGUM passa no teste?
produtos.every((p) => p.preco < 20);       // true  — TODOS passam?

nomes.includes("Espresso do Cerrado");     // true — comparação direta, sem callback
```

`find` é o irmão eficiente do `filter`: para na primeira ocorrência e devolve **o item**, não um array. Depois de um `find`, sempre lembre que o resultado pode ser `undefined`:

```js
const escolhido = produtos.find((p) => p.id === Number(idClicado));
if (!escolhido) return;               // guarda de segurança
console.log(escolhido.nome);
```

### 4.5 `reduce` — resuma tudo em um valor

`reduce` é o mais poderoso e o mais temido. Ele recebe dois argumentos: um callback `(acumulador, item) => novoAcumulador` e o **valor inicial** do acumulador.

```js
const total = produtos.reduce((soma, produto) => soma + produto.preco, 0);
// 112 — soma começa em 0 e vai acumulando
```

Passo a passo, o acumulador vale: `0` → `6` → `14.5` → `26.5` → `40.5` → `55.5` → `71.5` → `78.5` → `91.5` → `101` → `112`.

O acumulador não precisa ser um número. Pode ser um objeto — e aí `reduce` vira uma ferramenta de agrupamento:

```js
const porCategoria = produtos.reduce((acumulador, produto) => {
  acumulador[produto.categoria] = acumulador[produto.categoria] ?? [];
  acumulador[produto.categoria].push(produto);
  return acumulador;
}, {});

// { cafes: [4 produtos], geladas: [2], salgados: [2], doces: [2] }
Object.keys(porCategoria);   // ["cafes", "geladas", "salgados", "doces"]
```

Ou o próprio item, para achar extremos:

```js
const maisCaro = produtos.reduce((maior, produto) => (produto.preco > maior.preco ? produto : maior));
// { id: 6, nome: "Frappê de Café", preco: 16, … }
```

> **⚠️ Atenção**
> Sempre passe o valor inicial. Sem ele, `reduce` usa o primeiro item como acumulador — e em um array vazio estoura `TypeError: Reduce of empty array with no initial value`. A única exceção legítima é o caso "achar o extremo" acima, em que o acumulador é do mesmo tipo dos itens e o array comprovadamente não está vazio.

> **🧠 Você sabia?**
> Agrupar com `reduce` é tão comum que a linguagem ganhou um atalho: `Object.groupBy(produtos, (p) => p.categoria)` faz o mesmo que o bloco acima, em uma linha. Ele entrou no ES2024 e já está disponível nos navegadores atuais e no Node 21 ou superior. Vale conhecer — e vale continuar sabendo escrever o `reduce` na mão, porque é ele que aparece nas bases de código com alguns anos de vida.

### 4.6 `sort` — ordenar exige cuidado

```js
const numeros = [10, 9, 100, 25];
numeros.sort();               // [10, 100, 25, 9] — ordem alfabética de texto!
numeros.sort((a, b) => a - b); // [9, 10, 25, 100] — ordem numérica
```

Sem comparador, `sort` converte tudo em string e compara caractere a caractere: `"100"` vem antes de `"9"`. O comparador precisa devolver um **número**:

- negativo → `a` vem antes de `b`
- zero → mantém a ordem relativa
- positivo → `b` vem antes de `a`

```js
const porPrecoCrescente = [...produtos].sort((a, b) => a.preco - b.preco);
const porPrecoDecrescente = [...produtos].sort((a, b) => b.preco - a.preco);
```

Para texto em português, subtrair não funciona — use `Intl.Collator`, que sabe onde entram os acentos:

```js
const comparadorPtBr = new Intl.Collator("pt-BR", { sensitivity: "base" });
const porNome = [...produtos].sort((a, b) => comparadorPtBr.compare(a.nome, b.nome));
```

> **⚠️ Atenção**
> `sort` **altera o array original** e devolve o mesmo array (não uma cópia). É o único método desta seção que faz isso, junto de `reverse`, `push`, `splice` e `pop`. Ordenar `produtos` direto significa perder a ordem original para sempre — e o próximo filtro passa a trabalhar sobre uma lista embaralhada. Sempre copie antes: `[...produtos].sort(…)`.

### 4.7 O mapa mental

| Método | Pergunta que responde | Devolve |
|---|---|---|
| `forEach` | "Faça isso com cada um" | `undefined` |
| `map` | "Transforme cada um em…" | novo array do mesmo tamanho |
| `filter` | "Quais passam no teste?" | novo array de 0 a N itens |
| `find` | "Qual é o primeiro que…?" | o item ou `undefined` |
| `findIndex` | "Em que posição está?" | número ou `-1` |
| `some` / `every` | "Algum / todos passam?" | booleano |
| `reduce` | "Resuma tudo em um valor" | qualquer coisa |
| `sort` | "Em que ordem?" | o **mesmo** array, reordenado |

### 4.8 Encadeamento: a linha de produção

Como `map` e `filter` devolvem arrays, as operações se encaixam umas nas outras:

```js
// "Nomes dos cafés e doces abaixo de R$ 12, do mais barato ao mais caro"
const resultado = produtos
  .filter((p) => p.categoria === "cafes" || p.categoria === "doces")
  .filter((p) => p.preco < 12)
  .sort((a, b) => a.preco - b.preco)
  .map((p) => p.nome);

// ["Espresso do Cerrado", "Coado da Casa", "Bolo de Milho Verde", "Brownie de Castanha"]
```

Repare que o `.sort()` aqui é seguro **sem copiar**: o `filter` anterior já produziu um array novo, e é esse array intermediário que é ordenado. `produtos` continua intacto. A regra fica assim: copie antes de ordenar apenas quando o `sort` for a **primeira** operação da cadeia.

Uma cadeia percorre a lista uma vez por operação — quatro passagens no exemplo acima. Para dez produtos isso é irrelevante; para cem mil, um único `reduce` seria mais rápido. Legibilidade primeiro; otimize quando medir e comprovar que precisa.

> **🔬 Investigue**
> Cole no Console: `[10, 9, 100, 25].sort()` e depois `[10, 9, 100, 25].sort((a, b) => a - b)`. Agora o teste que revela a mutação: `const n = [3, 1, 2]; const m = n.sort(); m.push(99); console.log(n);`. O `99` aparece em `n` também — porque `m` e `n` são **o mesmo array**. Repita trocando `n.sort()` por `[...n].sort()` e veja a diferença.

### 4.9 Quando o `for` ainda é a melhor escolha

Os métodos de array não aposentaram o laço. Prefira `for…of` quando precisar **interromper** no meio (`break`), quando o corpo for assíncrono e precisar de `await` em sequência (Aula 09), ou quando estiver processando centenas de milhares de itens e tiver medido a diferença. Fora esses casos, o método declarativo comunica melhor a intenção.

## 5. Imutabilidade: por que não alterar o original

Todo bug de "o filtro parou de funcionar depois que ordenei" tem a mesma raiz: alguém alterou o array de dados. O array `produtos` é a sua **fonte da verdade**. Filtros, ordenações e transformações produzem **visões** dele — nunca o substituem.

```js
// Errado: destrói a ordem original e o dado
produtos.sort((a, b) => a.preco - b.preco);
produtos.forEach((p) => { p.preco = p.preco * 0.9; });

// Certo: derive uma lista nova a cada necessidade
const ordenados = [...produtos].sort((a, b) => a.preco - b.preco);
const promocionais = produtos.map((p) => ({ ...p, preco: p.preco * 0.9 }));
```

A linguagem ganhou versões que não alteram nada. Elas fazem parte do padrão desde 2023 e já funcionam nos navegadores atuais:

```js
const ordenados = produtos.toSorted((a, b) => a.preco - b.preco); // cópia ordenada
const invertidos = produtos.toReversed();                          // cópia invertida
const trocado = produtos.with(0, { ...produtos[0], preco: 7 });     // cópia com um item trocado
```

`[...array].sort(…)` continua sendo o jeito mais compatível, e é o que este curso usa. Conheça `toSorted` para ler código moderno.

## 6. Estado → derivação → renderização

Na Aula 07 o fluxo era: estado → renderização → eventos. Com filtros entra uma etapa no meio:

```js
const estado = {
  termo: "",
  categoria: "",
  ordenacao: "nome",
};

// DERIVAÇÃO: uma função pura que calcula o que deve aparecer,
// a partir do estado e da fonte da verdade. Não toca no DOM.
function produtosVisiveis() {
  return produtos
    .filter((produto) => produto.nome.toLowerCase().includes(estado.termo))
    .filter((produto) => estado.categoria === "" || produto.categoria === estado.categoria)
    .sort(ORDENADORES[estado.ordenacao]);
}

// RENDERIZAÇÃO: desenha o resultado da derivação
function render() {
  const visiveis = produtosVisiveis();
  renderizarProdutos(visiveis);
  atualizarResumo(visiveis);
}
```

Três propriedades tornam esse desenho robusto:

- **A lista visível nunca é guardada.** Ela é recalculada a cada `render()`. Não existe a possibilidade de o estado e a tela discordarem.
- **`produtosVisiveis` é uma função pura.** Recebe (pelo estado) e devolve, sem tocar no DOM nem alterar `produtos`. Dá para testá-la no Console isoladamente.
- **Cada evento faz duas coisas e só:** muda um campo do estado e chama `render()`. Nenhum ouvinte manipula o DOM diretamente.

Quando quiser um filtro novo, o roteiro é sempre o mesmo: um campo a mais no `estado`, um `.filter` a mais na derivação, um ouvinte a mais. Nada mais precisa mudar.

## 7. `debounce`: não trabalhar à toa

O evento `input` dispara a cada tecla. Digitar "cappuccino" são dez renderizações completas do cardápio. Com dez produtos ninguém percebe; com uma busca que consulta um servidor (Aula 10), são dez requisições para uma pesquisa só.

A técnica é **adiar** a execução até que a pessoa pare de digitar por um instante. E o mais bonito: ela se escreve como uma função que **devolve outra função** — o auge de "função é valor".

```js
function comAtraso(funcao, milissegundos = 300) {
  let temporizador;

  return (...argumentos) => {
    clearTimeout(temporizador);
    temporizador = setTimeout(() => funcao(...argumentos), milissegundos);
  };
}
```

Como funciona: cada chamada cancela o agendamento anterior e cria um novo. Só sobrevive o último — o que acontece quando a pessoa para de digitar por 300 ms. A variável `temporizador` continua viva entre as chamadas porque a função devolvida a "lembra": isso é um **closure**, e é o mesmo mecanismo que faz um contador manter sua contagem.

```js
const buscar = comAtraso((termo) => console.log("buscando por:", termo), 300);

buscar("c");
buscar("ca");
buscar("caf");   // só esta chega ao console, 300 ms depois
```

> **🔎 Por baixo do capô**
> `setTimeout` devolve um identificador numérico, não a função agendada. `clearTimeout(id)` diz ao navegador para descartar aquele agendamento antes que a fila de tarefas o alcance. Nenhuma das chamadas canceladas chega a executar — não é que elas rodem e o resultado seja ignorado: elas simplesmente somem da fila. Você vai olhar essa fila de frente na próxima aula, quando falarmos de event loop.

## 🧩 Padrão de projeto em uso: Strategy

Você vai precisar de três ordenações no cardápio. A solução ingênua é uma escada de `if`:

```js
function ordenar(lista, criterio) {
  if (criterio === "nome") return [...lista].sort((a, b) => a.nome.localeCompare(b.nome));
  if (criterio === "preco-asc") return [...lista].sort((a, b) => a.preco - b.preco);
  if (criterio === "preco-desc") return [...lista].sort((a, b) => b.preco - a.preco);
  return lista;
}
```

Cada critério novo exige editar a função. A alternativa guarda as estratégias em um objeto e escolhe uma pela chave:

```js
const ORDENADORES = {
  nome: (a, b) => comparadorPtBr.compare(a.nome, b.nome),
  "preco-asc": (a, b) => a.preco - b.preco,
  "preco-desc": (a, b) => b.preco - a.preco,
};

function ordenar(lista, criterio) {
  const comparador = ORDENADORES[criterio] ?? ORDENADORES.nome;
  return [...lista].sort(comparador);
}
```

Isso é o padrão **Strategy** (Estratégia): um conjunto de algoritmos intercambiáveis, encapsulados atrás de uma mesma interface, escolhidos em tempo de execução. Acrescentar "ordenar por categoria" agora é acrescentar uma linha ao objeto — a função `ordenar` não muda. Em JavaScript o padrão fica quase invisível, porque funções são valores e um objeto já serve de registro de estratégias; em linguagens sem essa facilidade, ele exige uma interface e uma classe por algoritmo. Você vai reencontrar Strategy no Nível 3, e a essa altura ele já vai parecer óbvio.

## 💻 Mão na massa — busca, filtros, ordenação e carrinho

Cinco passos, todos no `cardapio.html` e no `js/app.js` da Aula 07.

### Passo 1 — os controles no HTML

Logo acima da grade de cards, em `cardapio.html`:

`cardapio.html` (trecho do `<main>`)

```html
<form class="row g-3 align-items-end mb-4" id="controles-cardapio" role="search">
  <div class="col-12 col-md-5">
    <label class="form-label" for="busca">Buscar no cardápio</label>
    <input class="form-control" type="search" id="busca" name="busca"
           placeholder="café, pão de queijo, brownie" autocomplete="off">
  </div>

  <div class="col-6 col-md-3">
    <label class="form-label" for="filtro-categoria">Categoria</label>
    <select class="form-select" id="filtro-categoria" name="categoria">
      <option value="">Todas</option>
    </select>
  </div>

  <div class="col-6 col-md-4">
    <label class="form-label" for="ordenacao">Ordenar por</label>
    <select class="form-select" id="ordenacao" name="ordenacao">
      <option value="nome">Nome (A a Z)</option>
      <option value="preco-asc">Preço (menor primeiro)</option>
      <option value="preco-desc">Preço (maior primeiro)</option>
    </select>
  </div>
</form>

<p class="text-secondary" id="resumo-cardapio" role="status" aria-live="polite"></p>
```

O `<select>` de categoria tem só a opção "Todas": as demais são geradas do array, para que acrescentar um produto de categoria nova apareça no filtro sem editar HTML.

Acrescente também o botão ao template do card, dentro do `card-body`, depois do preço:

`cardapio.html` (dentro do `<template id="template-produto">`)

```html
<button class="btn btn-sm btn-cafe-vazado mt-3 align-self-start" type="button" data-acao="adicionar">
  Adicionar ao pedido
</button>
```

E, ao final da seção do cardápio, o painel do pedido:

`cardapio.html` (trecho do `<main>`)

```html
<aside class="card mt-5" aria-labelledby="titulo-pedido">
  <div class="card-body">
    <h2 class="h5 card-title" id="titulo-pedido">
      Seu pedido <span class="badge text-bg-secondary" id="contador-carrinho">0</span>
    </h2>
    <ul class="list-group list-group-flush" id="lista-carrinho"></ul>
    <p class="mt-3 mb-0 fw-bold" id="total-carrinho" role="status" aria-live="polite">Total: R$ 0,00</p>
  </div>
</aside>
```

### Passo 2 — estado, derivação e ordenadores

No `js/app.js`, logo abaixo do array `produtos` e das constantes da Aula 07:

`js/app.js`

```js
// ===== Estado da tela do cardápio =====
const estado = {
  termo: "",
  categoria: "",
  ordenacao: "nome",
  carrinho: [],
};

const comparadorPtBr = new Intl.Collator("pt-BR", { sensitivity: "base" });

// Estratégias de ordenação (padrão Strategy): a chave vem do <select>
const ORDENADORES = {
  nome: (a, b) => comparadorPtBr.compare(a.nome, b.nome),
  "preco-asc": (a, b) => a.preco - b.preco,
  "preco-desc": (a, b) => b.preco - a.preco,
};

// Derivação pura: do estado para a lista que deve aparecer
function produtosVisiveis() {
  const comparador = ORDENADORES[estado.ordenacao] ?? ORDENADORES.nome;

  return produtos
    .filter((produto) => produto.nome.toLowerCase().includes(estado.termo))
    .filter((produto) => estado.categoria === "" || produto.categoria === estado.categoria)
    .sort(comparador);
}
```

O `.sort()` no fim da cadeia é seguro: ele opera sobre o array produzido pelo `filter`, não sobre `produtos`.

### Passo 3 — o resumo calculado com `reduce`

`js/app.js`

```js
function atualizarResumo(lista) {
  const resumo = document.querySelector("#resumo-cardapio");

  if (lista.length === 0) {
    resumo.textContent = "Nenhum item corresponde à sua busca.";
    return;
  }

  const soma = lista.reduce((total, produto) => total + produto.preco, 0);
  const media = soma / lista.length;
  const maisBarato = lista.reduce((menor, produto) => (produto.preco < menor.preco ? produto : menor));

  resumo.textContent =
    `${lista.length} de ${produtos.length} itens · ` +
    `preço médio ${formatarPreco(media)} · ` +
    `mais barato: ${maisBarato.nome} (${formatarPreco(maisBarato.preco)})`;
}
```

Como `atualizarResumo` só é chamado com listas não vazias depois do `if`, o `reduce` sem valor inicial de `maisBarato` é seguro.

### Passo 4 — o carrinho

`js/app.js`

```js
function adicionarAoCarrinho(id) {
  const jaNoCarrinho = estado.carrinho.find((item) => item.id === id);

  if (jaNoCarrinho) {
    jaNoCarrinho.quantidade += 1;
  } else {
    const produto = produtos.find((p) => p.id === id);
    if (!produto) return;
    estado.carrinho.push({
      id: produto.id,
      nome: produto.nome,
      preco: produto.preco,
      quantidade: 1,
    });
  }

  renderizarCarrinho();
}

function removerDoCarrinho(id) {
  estado.carrinho = estado.carrinho.filter((item) => item.id !== id);
  renderizarCarrinho();
}

function totalDoCarrinho() {
  return estado.carrinho.reduce((total, item) => total + item.preco * item.quantidade, 0);
}

function renderizarCarrinho() {
  const lista = document.querySelector("#lista-carrinho");
  const contador = document.querySelector("#contador-carrinho");
  const total = document.querySelector("#total-carrinho");

  lista.replaceChildren();

  if (estado.carrinho.length === 0) {
    const vazio = document.createElement("li");
    vazio.className = "list-group-item text-secondary";
    vazio.textContent = "Nenhum item no pedido ainda.";
    lista.appendChild(vazio);
  } else {
    const fragmento = document.createDocumentFragment();

    estado.carrinho.forEach((item) => {
      const li = document.createElement("li");
      li.className = "list-group-item d-flex justify-content-between align-items-center";

      const texto = document.createElement("span");
      texto.textContent = `${item.quantidade}x ${item.nome} — ${formatarPreco(item.preco * item.quantidade)}`;

      const botao = document.createElement("button");
      botao.className = "btn btn-sm btn-cafe-vazado";
      botao.type = "button";
      botao.dataset.acao = "remover";
      botao.dataset.id = item.id;
      botao.textContent = "Remover";
      botao.setAttribute("aria-label", `Remover ${item.nome} do pedido`);

      li.append(texto, botao);
      fragmento.appendChild(li);
    });

    lista.appendChild(fragmento);
  }

  const quantidadeTotal = estado.carrinho.reduce((soma, item) => soma + item.quantidade, 0);
  contador.textContent = quantidadeTotal;
  total.textContent = `Total: ${formatarPreco(totalDoCarrinho())}`;
}
```

Repare em `removerDoCarrinho`: em vez de procurar o índice e usar `splice`, ele **substitui** o array por um novo, filtrado. Menos código e nenhum risco de errar o índice.

### Passo 5 — ligar tudo: eventos, opções geradas e `debounce`

`js/app.js`

```js
function comAtraso(funcao, milissegundos = 300) {
  let temporizador;

  return (...argumentos) => {
    clearTimeout(temporizador);
    temporizador = setTimeout(() => funcao(...argumentos), milissegundos);
  };
}

function preencherFiltroDeCategorias() {
  const select = document.querySelector("#filtro-categoria");
  const categorias = [...new Set(produtos.map((produto) => produto.categoria))];

  const opcoes = categorias.map((categoria) => {
    const opcao = document.createElement("option");
    opcao.value = categoria;
    opcao.textContent = ROTULOS_CATEGORIA[categoria] ?? categoria;
    return opcao;
  });

  select.append(...opcoes);
}

function render() {
  const visiveis = produtosVisiveis();
  renderizarProdutos(visiveis);
  atualizarResumo(visiveis);
}

function iniciarCardapio() {
  const container = document.querySelector("#lista-produtos");
  if (!container) return; // não estamos no cardapio.html

  preencherFiltroDeCategorias();
  render();
  renderizarCarrinho();

  const busca = document.querySelector("#busca");
  busca.addEventListener(
    "input",
    comAtraso((evento) => {
      estado.termo = evento.target.value.trim().toLowerCase();
      render();
    }, 300),
  );

  document.querySelector("#filtro-categoria").addEventListener("change", (evento) => {
    estado.categoria = evento.target.value;
    render();
  });

  document.querySelector("#ordenacao").addEventListener("change", (evento) => {
    estado.ordenacao = evento.target.value;
    render();
  });

  document.querySelector("#controles-cardapio").addEventListener("submit", (evento) => {
    evento.preventDefault(); // <Enter> na busca não deve recarregar a página
  });

  // Delegação: um ouvinte para os cards, outro para o pedido
  container.addEventListener("click", (evento) => {
    const botao = evento.target.closest('[data-acao="adicionar"]');
    if (!botao) return;
    const card = botao.closest(".card-produto");
    adicionarAoCarrinho(Number(card.dataset.id));
  });

  document.querySelector("#lista-carrinho").addEventListener("click", (evento) => {
    const botao = evento.target.closest('[data-acao="remover"]');
    if (!botao) return;
    removerDoCarrinho(Number(botao.dataset.id));
  });
}
```

Esta `iniciarCardapio` substitui a da Aula 07. As funções `criarCardProduto`, `renderizarProdutos`, `formatarPreco`, `iniciarTema` e `iniciarContato` continuam iguais.

### Como testar

1. Abra `cardapio.html`. O `<select>` de categoria deve ter cinco opções: "Todas" mais as quatro geradas do array.
2. Digite `caf` na busca. Sobra **um** card ("Frappê de Café" — é o único nome que contém `caf`) e o resumo começa com "1 de 10 itens". Troque para `co` e sobram dois ("Coado da Casa" e "Cold Brew da Chapada").
3. Digite `zzz`. Nenhum card, a mensagem de lista vazia aparece e o resumo diz "Nenhum item corresponde à sua busca."
4. Limpe a busca, escolha "Doces" e ordene por "Preço (maior primeiro)": Brownie de Castanha (R$ 11,00) antes de Bolo de Milho Verde (R$ 9,50).
5. Ordene por "Nome (A a Z)" com "Todas" selecionado. O primeiro card deve ser "Bolo de Milho Verde" e o último "Torta de Frango", com "Frappê de Café" entre "Espresso do Cerrado" e "Latte de Baunilha" — acento no lugar certo, graças ao `Intl.Collator`.
6. Clique duas vezes em "Adicionar ao pedido" no Coado da Casa e uma vez na Torta de Frango. O pedido mostra "2x Coado da Casa — R$ 17,00", "1x Torta de Frango — R$ 13,00", contador `3` e "Total: R$ 30,00".
7. Clique em "Remover" no Coado da Casa. O total cai para R$ 13,00 e o contador para `1`.
8. No Console, rode `produtos.map((p) => p.nome)` depois de ordenar por preço na tela. A ordem original tem que estar intacta — se mudou, algum `sort` está mordendo o array de origem.
9. Prova do `debounce`: coloque `console.count("render")` como primeira linha de `render()` e digite "cappuccino" na busca. Devem aparecer uma ou duas contagens, não dez.

```bash
git add .
git commit -m "feat: busca, filtro por categoria, ordenacao e carrinho no cardapio"
git push
```

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Preveja a saída de cada `console.log` **sem rodar**, depois confira:

```js
const precos = [10, 9, 100, 25];

console.log(precos.map((p) => p * 2));
console.log(precos.filter((p) => p > 20).length);
console.log(precos.reduce((a, b) => a + b, 0));
console.log(precos.sort());
console.log(precos.find((p) => p > 1000));
```

**A2.** As três definições abaixo deveriam ser equivalentes, mas duas estão erradas. Aponte quais, diga o que cada uma devolve ao ser chamada com `5` e corrija.

```js
const a = (n) => { n * 3 };
const b = (n) => n * 3;
const c = (n) => { return n * 3 };
```

**A3.** Escreva, em uma linha cada, usando o array `produtos` da aula: (a) os nomes de todos os produtos da categoria `"geladas"`; (b) quantos produtos custam R$ 10 ou mais; (c) `true` ou `false` para "existe algum produto abaixo de R$ 7"; (d) a soma dos preços dos salgados.

**A4.** A função abaixo devolve `undefined` e o Console acusa `TypeError: Cannot read properties of undefined (reading 'itens')`. Explique em duas linhas por quê e corrija sem mudar a lógica.

```js
const pedido = {
  itens: ["Espresso do Cerrado", "Torta de Frango"],
  quantos: () => this.itens.length,
};
```

**A5.** Verdadeiro ou falso, com justificativa de uma linha: (a) `map` pode devolver um array menor que o original; (b) `forEach` pode ser interrompido com `break`; (c) `sort` sem comparador ordena números corretamente; (d) `filter` nunca devolve `undefined`; (e) `[...produtos].sort()` deixa `produtos` intacto.

**A6.** Reescreva o laço abaixo usando um único encadeamento de métodos de array, sem `for` e sem variável auxiliar.

```js
const nomesCaros = [];
for (const produto of produtos) {
  if (produto.preco > 10) {
    nomesCaros.push(produto.nome.toUpperCase());
  }
}
```

### Nível B — Aplicação

**B1.** Faixa de preço. Acrescente ao cardápio um filtro de preço máximo (um `<input type="range">` de 5 a 15) encadeado aos filtros existentes, com o valor atual exibido ao lado.

Resultado esperado: arrastar o controle reduz a lista em tempo real e o resumo acompanha; combinar com busca e categoria funciona nos três ao mesmo tempo.

<details markdown="1">
<summary>Dica</summary>

Um campo a mais no `estado`, um `.filter` a mais em `produtosVisiveis`, um ouvinte de `input` a mais. Nada além disso precisa mudar — é o teste de que a arquitetura da seção 6 está correta.
</details>

**B2.** Quantidades no pedido. Acrescente botões "+" e "−" em cada item do carrinho. Ao chegar a zero, o item sai da lista.

Resultado esperado: o total e o contador acompanham cada clique; remover o último item volta a mostrar "Nenhum item no pedido ainda."

<details markdown="1">
<summary>Dica</summary>

Use `data-acao="aumentar"` e `data-acao="diminuir"` no mesmo ouvinte delegado que já trata `"remover"`. Depois de diminuir, `estado.carrinho = estado.carrinho.filter((i) => i.quantidade > 0)` limpa os zerados de uma vez.
</details>

**B3.** Resumo por categoria. Abaixo da grade, mostre quantos itens e qual o preço médio de cada categoria presente na lista visível, gerado com `reduce`.

Resultado esperado: uma linha por categoria ("Cafés: 4 itens · média R$ 10,13"), recalculada a cada filtro; categorias sem itens visíveis não aparecem.

<details markdown="1">
<summary>Dica</summary>

Agrupe primeiro com o `reduce` de acumulador-objeto da seção 4.5, depois `Object.entries` do resultado com `map` para montar as linhas.
</details>

**B4.** Ordenação estável e reversível. Acrescente ao `ORDENADORES` duas estratégias novas — "Categoria (A a Z)" e "Nome (Z a A)" — sem tocar na função `ordenar` nem em `produtosVisiveis`.

Resultado esperado: duas opções novas no `<select>` funcionando; o `diff` do commit mostra alteração apenas no objeto `ORDENADORES` e no HTML.

<details markdown="1">
<summary>Dica</summary>

Para inverter uma ordenação existente, envolva o comparador: `(a, b) => ORDENADORES.nome(b, a)`. Para ordenar por categoria e, dentro dela, por nome, some os comparadores: `comparadorPtBr.compare(a.categoria, b.categoria) || comparadorPtBr.compare(a.nome, b.nome)`.
</details>

**B5.** Busca em mais de um campo. Faça a busca considerar também a `descricao`, e mostre no resumo quantos resultados vieram só pela descrição.

Resultado esperado: buscar "polvilho" encontra o Pão de Queijo Mineiro, cujo nome não contém a palavra; o resumo informa "1 resultado encontrado na descrição".

<details markdown="1">
<summary>Dica</summary>

Um `filter` cujo teste é `nome.includes(termo) || descricao.includes(termo)`. Para a contagem, um segundo `filter` sobre a lista visível, testando só a descrição — e cuidado com o termo vazio, que casa com tudo.
</details>

### Nível C — Desafio

**C1.** Uma passada só. Hoje o `render()` percorre a lista cinco vezes: dois `filter`, um `sort`, o `forEach` do render e dois `reduce` do resumo. Reescreva a derivação e o resumo para que a lista seja percorrida **uma vez** para filtrar e calcular todas as estatísticas ao mesmo tempo (contagem, soma, média, mais barato, mais caro), mantendo o `sort` como única passagem adicional. Depois prove, com medição, se valeu a pena.

Resultado esperado: um único `reduce` devolve `{ visiveis, total, media, maisBarato, maisCaro }`; a tela continua idêntica; e uma tabela no README compara o tempo das duas versões com 10 e com 50.000 produtos gerados.

<details markdown="1">
<summary>Dica</summary>

O acumulador do `reduce` é um objeto com todos os campos, inicializado com `{ visiveis: [], soma: 0, maisBarato: null, maisCaro: null }`. Dentro do callback, teste o produto: se não passar nos filtros, devolva o acumulador sem mudança. Meça com `performance.now()` em volta de `render()` e rode cada versão 5 vezes, comparando a mediana. Prepare-se para a possibilidade de a diferença ser irrelevante em 10 itens — esse também é um resultado válido, e a conclusão honesta é o que vale nota.
</details>

## 🏆 Desafios

### ⭐ O comparador mentiroso
Tags: javascript, bug, investigacao

Um colega escreveu a ordenação por preço assim e jurou que testou: `produtos.sort((a, b) => a.preco > b.preco)`. Com três produtos, funcionou. Com os nove do Café Cerrado, a lista sai quase ordenada — mas não totalmente, e em outro navegador sai diferente. Descubra por que, e por que "quase certo" é pior que errado.

**Critérios de pronto**

- Um arquivo `INVESTIGACAO.md` mostra a saída errada com os dez produtos e explica, com base na documentação, qual valor o comparador deveria devolver e o que acontece quando ele devolve um booleano.
- O texto responde: por que o resultado pode variar entre navegadores, se todos seguem o mesmo padrão?
- Uma segunda parte demonstra o efeito colateral: rodar a versão errada **duas vezes seguidas** e mostrar que `produtos` já não está na ordem original.
- A correção usa subtração para números e `Intl.Collator` para texto, e o array de origem permanece intacto.

<details markdown="1">
<summary>Pistas</summary>

1. Leia na MDN a assinatura de `Array.prototype.sort` e a seção sobre a função de comparação: ela precisa devolver um número negativo, zero ou positivo.
2. `true` e `false` viram `1` e `0` quando o motor os trata como número. Repare no que nunca é produzido: um valor negativo.
3. Procure "sort stability" e "implementation-defined": desde o ES2019 a ordenação é estável, mas o algoritmo continua livre — e algoritmos diferentes reagem diferente a um comparador inconsistente.
4. Para provar a mutação, guarde `const antes = produtos.map((p) => p.id)` antes do `sort` e compare com o depois.
</details>

### ⭐⭐ Cinco laços viram uma passada
Tags: javascript, refatoracao, performance

Este relatório do Café Cerrado funciona, mas percorre o array cinco vezes e repete a mesma estrutura em todas. Refatore-o com métodos de array, meça as duas versões e decida com dados — não com gosto — qual entra no projeto.

```js
function relatorio(lista) {
  let total = 0;
  for (const p of lista) total += p.preco;

  let caros = 0;
  for (const p of lista) if (p.preco > 10) caros++;

  let maisCaro = lista[0];
  for (const p of lista) if (p.preco > maisCaro.preco) maisCaro = p;

  const categorias = [];
  for (const p of lista) if (!categorias.includes(p.categoria)) categorias.push(p.categoria);

  const nomes = [];
  for (const p of lista) nomes.push(p.nome);

  return { total, caros, maisCaro, categorias, nomes };
}
```

**Critérios de pronto**

- Versão A: cada bloco vira o método de array adequado (`reduce`, `filter`, `map`, `Set`), com no máximo uma linha por estatística.
- Versão B: um único `reduce` produz o objeto inteiro em uma passagem.
- As três versões (original, A e B) devolvem exatamente o mesmo objeto para o array de dez produtos e para um array vazio — este último documentado, porque a original quebra com lista vazia.
- Uma tabela no README compara o tempo das três com 100.000 itens gerados, com pelo menos 5 execuções e a mediana registrada.
- Um parágrafo final escolhe uma versão para o projeto e justifica considerando legibilidade **e** número.

<details markdown="1">
<summary>Pistas</summary>

1. `[...new Set(lista.map((p) => p.categoria))]` resolve a lista de categorias sem `includes` dentro de laço — que é quadrático.
2. Para a versão B, o acumulador começa como `{ total: 0, caros: 0, maisCaro: null, categorias: new Set(), nomes: [] }` e você converte o `Set` no fim.
3. Repare no que a função original faz com `lista[0]` quando `lista` é `[]`. É esse tipo de detalhe que só aparece em produção.
4. Ao medir, gere o array grande **uma vez**, fora da medição, e alterne a ordem das execuções — o primeiro a rodar costuma pagar o custo de aquecimento do motor.
</details>

### ⭐⭐ O filtro que respeita quem não vê a tela
Tags: acessibilidade, eventos, javascript

Sua busca funciona lindamente com o mouse. Agora feche os olhos: como alguém que usa leitor de tela sabe que a lista mudou? Que 2 de 10 itens sobraram? Que a busca não achou nada? Faça o cardápio filtrado ser tão utilizável de ouvido quanto de olho — e prove com um leitor de tela de verdade.

**Critérios de pronto**

- O resumo de resultados é anunciado a cada filtragem por uma região `aria-live="polite"`, sem interromper o que a pessoa está digitando.
- O anúncio só acontece depois que a digitação para (o `debounce` também protege o leitor de tela de ser bombardeado a cada tecla) e informa quantidade e critério ("2 de 10 itens, categoria Cafés").
- O estado vazio é anunciado com um texto útil, que sugere o que fazer ("Nenhum item corresponde a 'zzz'. Limpe a busca ou escolha outra categoria.").
- Navegar com <kbd>Tab</kbd> do campo de busca até o primeiro card funciona, e o foco nunca é jogado para o topo por causa de uma re-renderização.
- Um vídeo ou roteiro escrito documenta o teste com NVDA, VoiceOver ou o leitor do Android, listando o que foi anunciado em cada passo.

<details markdown="1">
<summary>Pistas</summary>

1. Uma região `aria-live` só é anunciada quando o texto **dentro** dela muda; se ela é criada junto com o texto, o anúncio se perde. Deixe o elemento na página desde o começo.
2. `role="status"` já implica `aria-live="polite"` — não precisa dos dois, mas ter os dois não atrapalha.
3. Sobre o foco: `replaceChildren()` destrói os elementos, e o foco que estava em um deles vai para o `<body>`. Se a pessoa estava no campo de busca (fora do contêiner), nada acontece — verifique se é o seu caso.
4. Leia o padrão de "results message" no ARIA Authoring Practices Guide antes de inventar o seu.
</details>

### ⭐⭐⭐ Filtros que cabem em um link
Tags: javascript, refatoracao, spa, performance

Alguém filtra o cardápio por "Doces, ordenados por preço", acha o combo perfeito e quer mandar no grupo da família. Copia a URL, cola, e a outra pessoa abre o cardápio inteiro sem filtro nenhum — porque o estado só existe na memória do navegador. Faça o estado morar na URL: filtros compartilháveis, botão Voltar funcionando e recarregar sem perder nada. É o primeiro passo do que vira roteamento na Aula 10.

**Critérios de pronto**

- Cada mudança de busca, categoria ou ordenação atualiza a URL para algo como `cardapio.html?busca=cafe&categoria=doce&ordem=preco-asc`, sem recarregar a página.
- Abrir a URL diretamente (ou apertar <kbd>F5</kbd>) reconstrói o estado exatamente: campos preenchidos, lista filtrada, resumo correto.
- O botão Voltar do navegador desfaz uma mudança de filtro por vez, e o Avançar refaz.
- A gravação na URL é adiada como a busca: digitar "cappuccino" não deixa dez entradas no histórico.
- Parâmetros ausentes, vazios ou inválidos (`?ordem=xyz`) caem em um padrão seguro, sem erro no Console.
- O `INVESTIGACAO.md` explica em um parágrafo a diferença entre `history.pushState` e `history.replaceState`, e justifica onde você usou cada um.

<details markdown="1">
<summary>Pistas</summary>

1. `new URLSearchParams(location.search)` lê os parâmetros; `parametros.get("categoria") ?? ""` já traz o padrão junto.
2. Para escrever sem recarregar: `history.pushState(null, "", `?${parametros}`)`. O `URLSearchParams` vira string sozinho na interpolação.
3. O botão Voltar dispara o evento `popstate` em `window` — é lá que você relê a URL e chama `render()`.
4. Digitar deve usar `replaceState` (substitui a entrada atual) e mudar de categoria deve usar `pushState` (cria entrada nova). Pense em quantas vezes a pessoa quer apertar Voltar em cada caso.
5. Ao reconstruir o estado, não esqueça de preencher os controles do formulário — senão a lista aparece filtrada e o `<select>` diz "Todas", e ninguém entende o que está vendo.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| A arrow devolve `undefined` sempre | Corpo entre chaves sem `return` | Remover as chaves ou acrescentar `return` |
| `Uncaught SyntaxError: Unexpected token ','` ao devolver objeto | `(a) => { nome: a, preco: 1 }` — as chaves viram bloco | Envolver o objeto em parênteses: `(a) => ({ nome: a, preco: 1 })` |
| `TypeError: Cannot read properties of undefined (reading 'itens')` em método | Arrow usada como método de objeto: não tem `this` próprio | Usar sintaxe de método (`itens() { }`) ou `function` |
| `[10, 9, 100].sort()` devolve `[10, 100, 9]` | Sem comparador, `sort` compara como texto | Passar `(a, b) => a - b` |
| O filtro para de funcionar depois de ordenar uma vez | `sort` alterou o array de origem | Copiar antes: `[...produtos].sort(…)` ou `toSorted` |
| `TypeError: Reduce of empty array with no initial value` | `reduce` sem valor inicial em array vazio | Passar sempre o segundo argumento (`0`, `[]`, `{}`) |
| A lista some ao ordenar, mas volta ao recarregar | Comparador devolvendo booleano em vez de número | Devolver negativo, zero ou positivo |
| `TypeError: Cannot read properties of undefined (reading 'nome')` depois de `find` | `find` não achou nada e devolveu `undefined` | Testar o resultado antes de usar (`if (!item) return;`) |
| `map` usado e o resultado ignorado | Confusão entre `map` (transformar) e `forEach` (efeito) | Trocar por `forEach` quando não há valor a produzir |
| A busca dispara uma renderização por tecla | Ouvinte de `input` sem `debounce` | Envolver o callback com `comAtraso(…)` |
| `TypeError: produtos.filter is not a function` | A variável não é array (é `NodeList`, objeto ou `undefined`) | Converter com `[...valor]` ou conferir de onde ela vem |

## 🏠 Para praticar depois da aula (1 h)

No repositório do **seu projeto autoral**:

1. Refatore o `js/app.js`: converta os callbacks de evento para arrow functions e substitua os laços `for` que só percorrem listas por `map`, `filter` ou `forEach`.
2. Implemente a busca por texto nos seus itens, com evento `input` e `debounce` de 300 ms.
3. Acrescente um segundo filtro encadeado ao primeiro — categoria por `<select>` ou ordenação por um campo numérico — usando o padrão estado → derivação → renderização.
4. Exiba um resumo calculado com `reduce` ou `length`, atualizado a cada filtragem (por exemplo, "8 itens encontrados · total R$ 320,00").
5. Trate a lista vazia com uma mensagem útil, que diga o que a pessoa pode fazer em seguida.

**Critério de pronto:** os filtros funcionam combinados; o array de origem permanece na ordem original depois de qualquer ordenação (comprove no Console); nenhum laço `for` sobrou onde um método de array serviria; o Console fica sem erros.

**Guarde no seu repositório:** commit + push.

**Leitura dirigida (se você tem acesso a uma biblioteca virtual pela sua instituição):** Queirós e Portela, seções de JavaScript avançado; Loudon, padrões de código JavaScript escalável; MDN, "Array" (métodos) e "Introducing asynchronous JavaScript" — preparação direta para a próxima aula.

## ✅ Checkpoint do projeto

- [ ] Nenhuma função anônima com `function` sobrou onde uma arrow serviria melhor.
- [ ] O estado da tela vive em um objeto `estado`, e não espalhado em variáveis soltas.
- [ ] Existe uma função pura de derivação que calcula a lista visível a partir do estado.
- [ ] Busca, filtro e ordenação funcionam **combinados**, em qualquer ordem de uso.
- [ ] Nenhum `sort` altera o array de origem.
- [ ] Todo `reduce` recebe valor inicial.
- [ ] O resumo com contagem e total é recalculado a cada filtragem.
- [ ] A lista vazia tem tratamento próprio, com texto que orienta a pessoa.
- [ ] A busca usa `debounce`, comprovado com `console.count`.
- [ ] Os cliques nos itens continuam funcionando por delegação depois de qualquer re-renderização.

## 📚 Para aprofundar

- [MDN — Arrow function expressions](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Functions/Arrow_functions): leia especialmente a seção sobre `this`.
- [MDN — `Array`](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Global_Objects/Array): a lista completa dos métodos, com exemplos rodáveis.
- [MDN — `Array.prototype.reduce()`](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Global_Objects/Array/reduce): os exemplos de agrupamento valem a leitura inteira.
- [MDN — `Array.prototype.sort()`](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Global_Objects/Array/sort): o contrato da função de comparação, ponto por ponto.
- [MDN — Função de callback](https://developer.mozilla.org/pt-BR/docs/Glossary/Callback_function): a definição curta, para fixar o vocabulário.
- [MDN — `Intl.Collator`](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Global_Objects/Intl/Collator): ordenação alfabética correta em português.
- [MDN — Introdução ao JavaScript assíncrono](https://developer.mozilla.org/pt-BR/docs/Learn/JavaScript/Asynchronous/Introducing): leia antes da próxima aula.
- QUEIRÓS, Ricardo; PORTELA, Filipe. *Introdução ao Desenvolvimento Moderno para a Web*. FCA, 2018 — JavaScript: funções e coleções.
- LOUDON, Kyle. *Desenvolvimento de Grandes Aplicações Web*. Novatec, 2019 — padrões de código JavaScript escalável.
- PUREWAL, Semmy. *Aprendendo a Desenvolver Aplicações Web*. Novatec, 2014 — funções e manipulação de dados.

Na próxima aula o `setTimeout` de hoje deixa de ser curiosidade e vira o assunto principal: por que o JavaScript não pode parar para esperar, o que é o event loop e como o callback evolui para a Promise. O cardápio do Café Cerrado vai passar a "buscar" seus dados com atraso simulado, ganhando estados de carregando e de erro — o ensaio final antes do `fetch` de verdade.
