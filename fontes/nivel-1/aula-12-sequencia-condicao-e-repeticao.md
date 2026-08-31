# Aula 12 — Estruturas sequenciais, condicionais e de repetição

> **Nível 1 — Introdução ao Desenvolvimento Web** · Unidade 3: JavaScript e interatividade
> WebLab · UNEMAT — Campus Sinop
> **Tempo estimado:** 3 blocos de 50 min + 1 h de prática

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Distinguir as três estruturas fundamentais de um algoritmo — sequência, decisão e repetição — e reconhecê-las em qualquer programa.
- Escolher entre `for`, `while`, `do…while`, `for…of` e `for…in` conforme o problema, e justificar a escolha.
- Controlar a execução de um laço com `break` e `continue`, e reconhecer (e evitar) um laço infinito.
- Criar, ler e modificar arrays, distinguindo os métodos que **alteram** o array original dos que **devolvem um novo**.
- Criar e navegar objetos, inclusive aninhados, com notação de ponto, colchetes, desestruturação e `Object.keys`/`values`/`entries`.
- Resolver problemas com `forEach`, `map`, `filter`, `find`, `reduce`, `some`, `every` e `sort`, encadeando-os quando fizer sentido.
- Modelar o domínio do seu projeto como um **array de objetos** — a estrutura de dados mais comum da web.
- Depurar um laço com breakpoints, breakpoints condicionais e o painel Scope do DevTools.

## 📋 Pré-requisitos

- [ ] Site do evento com `js/app.js` (contagem regressiva) e `js/inscricao.js` (vagas e aviso automático) funcionando, sem erros no Console.
- [ ] Console do navegador aberto e a aba **Sources** localizada — hoje ela sai do papel de coadjuvante.
- [ ] Revisar da Aula 11: `const`/`let` e escopo de bloco, operadores aritméticos e lógicos, `if`/`else if`/`else`, ternário e `switch`.
- [ ] Revisar da Aula 10: template literals, `typeof`, valores falsy e `console.table`.

> Na aula passada o seu script aprendeu a decidir: a página de inscrição escolhe sozinha entre quatro mensagens e a página inicial calcula quantos dias faltam para o evento. Mas ele ainda trata **um** dado de cada vez — um número de inscritos, uma data, uma taxa. Um site de evento real tem doze atividades, seis palestrantes, três dias e quatro trilhas. Hoje você aprende a guardar coleções de informação em **arrays** e **objetos** e a percorrê-las com estruturas de **repetição**, produzindo relatórios completos no Console. Tudo ainda acontece no console — na próxima aula esses mesmos dados viram cartões na tela.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | As três estruturas de um algoritmo; `for`, `while`, `do…while`, `for…of`; `break`, `continue` e laços aninhados |
| 2 | 50 min | Arrays: criação, índices, métodos que alteram e métodos que devolvem novo; objetos e desestruturação |
| 3 | 50 min | Métodos de ordem superior; depuração de laços; Mão na massa: `js/dados.js` e os relatórios do evento |

## 1. As três estruturas de um algoritmo

Em 1966, dois pesquisadores italianos, Corrado Böhm e Giuseppe Jacopini, provaram um resultado que organizou a programação para sempre: **qualquer** algoritmo computável pode ser escrito combinando apenas três estruturas.

| Estrutura | O que faz | Em JavaScript |
|---|---|---|
| Sequência | executa instruções, uma após a outra, na ordem escrita | linhas soltas, uma embaixo da outra |
| Decisão | escolhe entre caminhos conforme uma condição | `if`, `else if`, `else`, ternário, `switch` |
| Repetição | repete um trecho enquanto uma condição for verdadeira | `for`, `while`, `do…while`, `for…of`, `for…in` |

Você já domina as duas primeiras. A terceira é a que falta — e é a que muda a escala do que você consegue fazer: com repetição, o mesmo código que trata uma palestra trata mil.

### 1.1 Sequência: a ordem importa mais do que parece

```js
// js/exemplos-sequencia.js
let inscritos = 87;
const novos = 5;

inscritos = inscritos + novos;      // 92
const percentual = inscritos / 120; // usa o valor JÁ atualizado
console.log(percentual.toFixed(2)); // "0.77"
```

Se as duas últimas linhas trocassem de lugar, o percentual seria calculado sobre 87 e ficaria errado — sem nenhum erro no Console. Esse é o tipo de bug que a estrutura sequencial esconde: o programa roda, o número aparece, e está errado.

O exemplo clássico de dependência de ordem é a troca de valores entre duas variáveis:

```js
let primeiro = "Ana";
let segundo = "Bruno";

// ERRADO: o valor de primeiro se perde na primeira linha
// primeiro = segundo;
// segundo = primeiro;   // "Bruno" — os dois ficam iguais

// CERTO: uma variável temporária guarda o valor que seria perdido
let temporario = primeiro;
primeiro = segundo;
segundo = temporario;

console.log(primeiro, segundo); // "Bruno" "Ana"
```

Em JavaScript moderno existe um atalho — a desestruturação de array, que você vê na seção 5.6: `[primeiro, segundo] = [segundo, primeiro]`. Mas entender por que a variável temporária é necessária vale mais do que decorar o atalho.

## 2. Estruturas de repetição

### 2.1 `for`: quando você sabe quantas vezes

```js
for (let i = 0; i < 5; i++) {
  console.log("Repetição número", i);
}
// 0, 1, 2, 3, 4
```

O cabeçalho tem três partes separadas por ponto e vírgula, e cada uma roda em um momento diferente:

| Parte | Quando executa | Papel |
|---|---|---|
| `let i = 0` | uma única vez, antes de tudo | inicialização do contador |
| `i < 5` | antes de **cada** repetição | condição de continuação |
| `i++` | depois de **cada** repetição | atualização do contador |

Traduzindo para português: "comece com `i` valendo 0; enquanto `i` for menor que 5, execute o corpo; depois de cada execução, some 1 a `i`".

Duas convenções: o contador quase sempre se chama `i` (de *índice*), e ele quase sempre começa em **zero** — porque os índices de arrays começam em zero, como você verá na seção 3.

```js
// Contagem regressiva: o contador pode decrescer
for (let i = 3; i > 0; i--) {
  console.log(i);
}
console.log("Começou!");
// 3, 2, 1, Começou!

// O passo não precisa ser 1
for (let i = 0; i <= 20; i += 5) {
  console.log(i); // 0, 5, 10, 15, 20
}
```

> **⚠️ Atenção**
> Declare o contador com `let`, nunca com `const`: o `i++` reatribui a variável, e com `const` você recebe `Uncaught TypeError: Assignment to constant variable.`. E declare **dentro** do `for` (`for (let i = 0; …)`), não antes: assim o `i` existe só dentro do laço e não polui o resto do arquivo.

### 2.2 `while`: quando você não sabe quantas vezes

```js
let saldoVagas = 8;
let fila = 0;

while (saldoVagas > 0) {
  fila++;
  saldoVagas -= 2;   // cada grupo da fila ocupa 2 vagas
}

console.log("Grupos atendidos:", fila); // 4
```

O `while` testa **antes** de executar. Se a condição já começar falsa, o corpo não roda nenhuma vez. Use-o quando a quantidade de repetições depende de algo que muda dentro do laço.

### 2.3 `do…while`: pelo menos uma vez

```js
let tentativas = 0;

do {
  tentativas++;
  console.log("Tentativa", tentativas);
} while (tentativas < 3);
// Tentativa 1, Tentativa 2, Tentativa 3
```

Aqui o teste vem **depois**, então o corpo executa pelo menos uma vez, mesmo com a condição falsa desde o início:

```js
let contador = 100;

do {
  console.log("Executei mesmo assim");
} while (contador < 5);
```

É a escolha certa quando a ação precisa acontecer antes de haver o que testar: pedir um dado, sortear um valor, tentar uma conexão. Fora desses casos, o `while` comum é mais previsível.

### 2.4 `for…of`: percorrer valores

Quando você só quer os **valores** de uma coleção e não se importa com o índice, o `for…of` é mais curto e mais seguro:

```js
const trilhas = ["Desenvolvimento Web", "Ciência de Dados", "Segurança", "Inteligência Artificial"];

for (const trilha of trilhas) {
  console.log(trilha);
}
```

Repare no `const`: cada repetição cria uma variável nova, então não há reatribuição — e o `const` funciona. Não há contador, não há `length`, não há como errar o limite.

`for…of` funciona com tudo que é **iterável**: arrays, strings, `Map`, `Set` e a lista de elementos que você vai obter do DOM na Aula 13.

```js
for (const letra of "WebLab") {
  console.log(letra); // W, e, b, L, a, b
}
```

Se você precisar do índice **e** do valor ao mesmo tempo, use `entries()` com desestruturação:

```js
const trilhas = ["Web", "Dados", "Segurança"];

for (const [indice, trilha] of trilhas.entries()) {
  console.log(`${indice + 1}. ${trilha}`);
}
// 1. Web
// 2. Dados
// 3. Segurança
```

### 2.5 `for…in`: percorrer chaves

O `for…in` percorre as **chaves** (nomes de propriedades) de um objeto:

```js
const palestrante = { nome: "Ana Lúcia", instituicao: "UNEMAT", area: "ia" };

for (const chave in palestrante) {
  console.log(`${chave}: ${palestrante[chave]}`);
}
// nome: Ana Lúcia
// instituicao: UNEMAT
// area: ia
```

Repare que o valor é lido com `palestrante[chave]`, notação de colchetes — porque o nome da propriedade está em uma variável. Escrever `palestrante.chave` procuraria uma propriedade literalmente chamada "chave", que não existe.

> **⚠️ Atenção**
> Não use `for…in` em arrays. Ele percorre os **índices como texto** (`"0"`, `"1"`, `"2"`) e também qualquer propriedade extra que alguém tenha adicionado ao array, em ordem não garantida. Para arrays use `for…of` (valores), `for` clássico (índices) ou `forEach`. A regra é fácil de guardar: **`in` para objetos, `of` para arrays**.

### 2.6 `break` e `continue`

```js
const notas = [8, 6, 9, 4, 7, 10];

for (const nota of notas) {
  if (nota < 5) {
    continue;   // pula esta repetição e vai para a próxima
  }
  if (nota === 10) {
    break;      // encerra o laço inteiro
  }
  console.log("Nota válida:", nota);
}
// 8, 6, 9, 7 — o 4 foi pulado e o laço parou antes de imprimir o 10
```

`continue` pula o **restante do corpo** e segue para a próxima repetição. `break` abandona o laço imediatamente. Os dois deixam o código mais direto quando substituem um `if` gigante que envolve todo o corpo — mas dois ou três `break` espalhados no mesmo laço são sinal de que a lógica pede outra estrutura.

### 2.7 Laços infinitos

```js
// NÃO EXECUTE: o navegador congela
// let i = 0;
// while (i < 10) {
//   console.log(i);   // faltou o i++: a condição nunca fica falsa
// }
```

Um laço infinito trava a aba inteira, porque o JavaScript do navegador roda em uma única linha de execução: enquanto o laço não termina, nada é desenhado e nenhum clique é atendido. As três causas mais comuns:

1. Esquecer de atualizar a variável da condição (o caso acima).
2. Atualizar na direção errada (`i--` em um laço que testa `i < 10`).
3. Comparar decimais com `===` — `for (let x = 0; x !== 1; x += 0.1)` nunca para, porque a soma nunca dá exatamente 1, como você viu na Aula 11.

Se travar: feche a aba (<kbd>Ctrl</kbd>+<kbd>W</kbd>) ou use o gerenciador de tarefas do navegador (<kbd>Shift</kbd>+<kbd>Esc</kbd> no Chrome). Depois, antes de rodar de novo, coloque um freio de segurança:

```js
let i = 0;
let voltas = 0;
const LIMITE_DE_SEGURANCA = 1000;

while (i < 10) {
  voltas++;
  if (voltas > LIMITE_DE_SEGURANCA) {
    console.error("Laço passou do limite — provável laço infinito");
    break;
  }
  i++;
}
```

> **🧠 Você sabia?**
> A pergunta "este programa vai parar algum dia?" tem nome próprio: **problema da parada**. Alan Turing provou, em 1936, que é **impossível** escrever um programa capaz de responder a essa pergunta para qualquer outro programa — não por falta de esforço ou de computador rápido, mas por impossibilidade lógica. É por isso que nem o navegador nem o VS Code conseguem avisar "você escreveu um laço infinito": eles só percebem que a página parou de responder e oferecem encerrá-la. A responsabilidade de garantir que o laço termina é, e sempre será, sua.

### 2.8 Laços aninhados

Um laço dentro de outro percorre duas dimensões. O de fora anda uma vez para cada volta **completa** do de dentro:

```js
// Tabuada de 1 a 5
for (let tabuada = 1; tabuada <= 5; tabuada++) {
  console.group(`Tabuada do ${tabuada}`);
  for (let multiplicador = 1; multiplicador <= 10; multiplicador++) {
    console.log(`${tabuada} x ${multiplicador} = ${tabuada * multiplicador}`);
  }
  console.groupEnd();
}
```

São 5 × 10 = 50 execuções do corpo interno. Esse produto é o que torna laços aninhados perigosos: dois laços sobre uma lista de 1.000 itens dão 1.000.000 de execuções. Com três, um bilhão. Antes de aninhar, pergunte se não existe uma estrutura de dados que evite o segundo laço — no seu projeto, quase sempre existe.

Um uso legítimo e comum: agrupar por categoria, como a programação por dia que você vai montar na Mão na massa.

## 3. Arrays

Um **array** é uma lista ordenada de valores, guardada em uma única variável. É a estrutura mais usada em programação para a web.

### 3.1 Criando e lendo

```js
const notas = [8.5, 6.0, 9.0, 4.5, 7.0];
const vazio = [];
const misturado = ["texto", 42, true, null];  // permitido, mas evite

console.log(notas[0]);              // 8.5  — o primeiro item tem índice 0
console.log(notas[4]);              // 7    — o último de cinco itens
console.log(notas[5]);              // undefined — não existe, e não dá erro
console.log(notas.length);          // 5    — quantidade de itens
console.log(notas[notas.length - 1]); // 7  — forma clássica de pegar o último
console.log(notas.at(-1));          // 7    — forma moderna: índice negativo conta do fim
console.log(notas.at(-2));          // 4.5
```

O detalhe que mais gera bug: o índice do **último** item é `length - 1`, não `length`. Um laço escrito com `i <= notas.length` lê uma posição a mais e devolve `undefined` — o famoso erro "por um" (*off-by-one*).

```js
// Errado: lê o índice 5, que não existe
for (let i = 0; i <= notas.length; i++) {
  console.log(notas[i]);  // a última linha imprime undefined
}

// Certo
for (let i = 0; i < notas.length; i++) {
  console.log(notas[i]);
}
```

### 3.2 Métodos que **alteram** o array original

```js
const fila = ["Ana", "Bruno", "Carla"];

fila.push("Diego");        // adiciona no fim   → ["Ana","Bruno","Carla","Diego"]
fila.pop();                // remove do fim e devolve "Diego"
fila.unshift("Zuleide");   // adiciona no início → ["Zuleide","Ana","Bruno","Carla"]
fila.shift();              // remove do início e devolve "Zuleide"

fila.splice(1, 1);         // remove 1 item a partir do índice 1 → ["Ana","Carla"]
fila.splice(1, 0, "Beto"); // insere "Beto" no índice 1 sem remover nada
console.log(fila);         // ["Ana", "Beto", "Carla"]

const numeros = [10, 9, 1, 25];
numeros.sort((a, b) => a - b);  // ordena numericamente → [1, 9, 10, 25]
numeros.reverse();               // inverte → [25, 10, 9, 1]
console.log(numeros);
```

`push` e `pop` funcionam no fim do array e são rápidos; `shift` e `unshift` funcionam no início e obrigam o motor a reposicionar todos os itens — em listas grandes, prefira o fim.

> **⚠️ Atenção**
> `sort()` **sem função comparadora** converte tudo em texto antes de comparar: `[10, 9, 1].sort()` devolve `[1, 10, 9]`, porque `"10"` vem antes de `"9"` na ordem de texto (você viu isso na Aula 11). Para números, passe sempre `(a, b) => a - b` (crescente) ou `(a, b) => b - a` (decrescente). Para textos em português, `(a, b) => a.localeCompare(b, "pt-BR")`.

### 3.3 Métodos que **devolvem** um valor novo

Estes não tocam no array original — devolvem outra coisa:

```js
const notas = [8.5, 6.0, 9.0, 4.5, 7.0];

console.log(notas.slice(1, 3));    // [6, 9] — do índice 1 até ANTES do 3
console.log(notas.slice(-2));      // [4.5, 7] — os dois últimos
console.log(notas.concat([10]));   // [8.5, 6, 9, 4.5, 7, 10]
console.log([...notas, 10]);       // idem, com o operador spread
console.log(notas.indexOf(9.0));   // 2 — o índice, ou -1 se não existir
console.log(notas.includes(9.0));  // true — só quer saber se existe
console.log(notas.join(" · "));    // "8.5 · 6 · 9 · 4.5 · 7" — vira string
console.log(notas);                // o original continua intacto
```

O operador **spread** (`...`) "espalha" os itens de um array. Ele é a forma moderna de copiar e juntar listas:

```js
const dia1 = ["Abertura", "Git do zero"];
const dia2 = ["Acessibilidade", "Segurança"];

const tudo = [...dia1, ...dia2];       // junta as duas
const copia = [...dia1];               // cópia independente
const comExtra = [...dia1, "Extra"];   // cópia com um item a mais

copia.push("Só na cópia");
console.log(dia1);   // ["Abertura", "Git do zero"] — o original não mudou
console.log(tudo.length, comExtra.length); // 4 3
```

Isso importa por causa de uma característica da linguagem: arrays e objetos são guardados por **referência**. `const copia = dia1` não cria uma cópia, cria um segundo nome para a mesma lista — mexer em um muda o outro. O spread resolve.

```js
const original = [1, 2, 3];
const apelido = original;      // MESMA lista, dois nomes
const copiaDeVerdade = [...original];

apelido.push(4);
console.log(original);        // [1, 2, 3, 4] — mudou!
console.log(copiaDeVerdade);  // [1, 2, 3] — independente
```

> **🔬 Investigue**
> Cole no Console: `const a = [1, 2, 3]; const b = a; const c = [...a]; b.push(99);`. Agora inspecione `a`, `b` e `c`. O array `a` tem o 99, mesmo você tendo alterado `b`. Faça o mesmo teste com um número: `let x = 1; let y = x; y = 99;` — aí `x` continua 1. Você acabou de ver a diferença entre **valor** (primitivos, copiados) e **referência** (arrays e objetos, compartilhados). Essa é a causa da maioria dos bugs "eu não mexi nessa lista!" que você vai encontrar no semestre.

## 4. Métodos de ordem superior

Os métodos a seguir recebem **uma função** como argumento e a aplicam a cada item. Eles substituem a maior parte dos `for` que você escreveria — com menos código e menos chance de erro de índice.

A sintaxe `(item) => item.preco` é uma **arrow function**, formalizada na Aula 13. Por enquanto, leia assim: "recebe `item`, devolve `item.preco`".

### 4.1 `forEach` — apenas percorrer

```js
const trilhas = ["Web", "Dados", "Segurança"];

trilhas.forEach((trilha, indice) => {
  console.log(`${indice + 1}. ${trilha}`);
});
```

`forEach` **não devolve nada** (`undefined`). Use-o quando o objetivo é o efeito colateral: imprimir, somar em uma variável externa, desenhar na tela.

### 4.2 `map` — transformar

```js
const precos = [25, 50, 12.5];

const comAumento = precos.map((preco) => preco * 1.1);
console.log(comAumento); // [27.500000000000004, 55.00000000000001, 13.750000000000002]
console.log(precos);     // [25, 50, 12.5] — intacto

const formatados = precos.map((preco) => `R$ ${preco.toFixed(2)}`);
console.log(formatados); // ["R$ 25.00", "R$ 50.00", "R$ 12.50"]
```

`map` devolve um array **novo, do mesmo tamanho**, com cada item transformado. É a ferramenta que, na Aula 13, transforma dados em cartões de HTML.

E olhe de novo para o primeiro resultado: `27.500000000000004`, e não `27.5`. É o ponto flutuante da Aula 11 aparecendo de novo — `1.1` não tem representação exata em binário, e o erro se propaga item a item. Por isso a segunda linha existe: `toFixed(2)` (ou o `Intl.NumberFormat` da Aula 11) é o que você mostra na tela; o número cru fica para as contas.

### 4.3 `filter` — selecionar

```js
const notas = [8.5, 6.0, 9.0, 4.5, 7.0];

const aprovadas = notas.filter((nota) => nota >= 6);
console.log(aprovadas);        // [8.5, 6, 9, 7]
console.log(aprovadas.length); // 4
```

`filter` devolve um array novo com **os itens que passaram no teste** — de tamanho menor ou igual ao original. Se ninguém passar, devolve `[]` (array vazio, que é *truthy*: teste com `length === 0`, não com `if (!lista)`).

### 4.4 `find` e `findIndex` — achar o primeiro

```js
const alunos = [
  { nome: "Ana", nota: 8.5 },
  { nome: "Bruno", nota: 5.0 },
  { nome: "Carla", nota: 9.0 },
];

const ana = alunos.find((aluno) => aluno.nome === "Ana");
console.log(ana);        // { nome: "Ana", nota: 8.5 }

const posicao = alunos.findIndex((aluno) => aluno.nota < 6);
console.log(posicao);    // 1

const ninguem = alunos.find((aluno) => aluno.nota === 10);
console.log(ninguem);    // undefined — sempre teste antes de usar!
```

`find` devolve **o item** (ou `undefined`); `findIndex` devolve **o índice** (ou `-1`). Confundir os dois é erro comum: `if (alunos.findIndex(…))` é sempre verdadeiro quando o índice é diferente de 0, e falso quando o item achado está na primeira posição.

### 4.5 `reduce` — condensar em um valor

```js
const notas = [8.5, 6.0, 9.0, 4.5, 7.0];

const soma = notas.reduce((acumulado, nota) => acumulado + nota, 0);
console.log(soma);               // 35
console.log(soma / notas.length); // 7 — a média
```

`reduce` é o mais poderoso e o mais confuso à primeira vista. Ele recebe dois argumentos: a função e o **valor inicial** do acumulador (o `0` no fim). A cada volta, a função recebe o acumulado até agora e o item atual, e devolve o novo acumulado.

Acompanhe passo a passo:

```text
início:  acumulado = 0
item 8.5: acumulado = 0 + 8.5   = 8.5
item 6.0: acumulado = 8.5 + 6   = 14.5
item 9.0: acumulado = 14.5 + 9  = 23.5
item 4.5: acumulado = 23.5 + 4.5 = 28
item 7.0: acumulado = 28 + 7    = 35
resultado: 35
```

O acumulador não precisa ser número — pode ser texto, array ou objeto. Contar ocorrências, por exemplo:

```js
const areas = ["web", "dados", "web", "ia", "web"];

const contagem = areas.reduce((conta, area) => {
  conta[area] = (conta[area] ?? 0) + 1;
  return conta;
}, {});

console.log(contagem); // { web: 3, dados: 1, ia: 1 }
```

Repare no `?? 0` da Aula 11: na primeira vez que uma área aparece, `conta[area]` é `undefined`, e o `??` o substitui por zero.

> **⚠️ Atenção**
> **Sempre passe o valor inicial** do `reduce`. Sem ele, o primeiro item vira o acumulador — o que quebra quando o array está vazio (`Uncaught TypeError: Reduce of empty array with no initial value`) e produz resultados errados quando o acumulador tem tipo diferente dos itens.

### 4.6 `some` e `every` — perguntas de sim ou não

```js
const notas = [8.5, 6.0, 9.0, 4.5];

console.log(notas.some((n) => n === 10));  // false — algum é 10?
console.log(notas.some((n) => n < 5));      // true  — algum está abaixo de 5?
console.log(notas.every((n) => n >= 4));    // true  — todos são >= 4?
console.log(notas.every((n) => n >= 6));    // false
```

### 4.7 Encadeamento

Como `map` e `filter` devolvem arrays, você pode ligá-los em sequência. Leia sempre da esquerda para a direita, como uma frase:

```js
const alunos = [
  { nome: "Ana", nota: 8.5 },
  { nome: "Bruno", nota: 5.0 },
  { nome: "Carla", nota: 9.0 },
  { nome: "Diego", nota: 3.5 },
];

const aprovadosEmOrdem = alunos
  .filter((aluno) => aluno.nota >= 6)          // fica só quem passou
  .map((aluno) => aluno.nome)                   // vira lista de nomes
  .sort((a, b) => a.localeCompare(b, "pt-BR")) // ordena em português
  .join(", ");                                  // vira uma string

console.log(aprovadosEmOrdem); // "Ana, Carla"
```

Uma armadilha escondida nesse encadeamento: `sort` **altera** o array em que atua. Aqui isso é seguro, porque o array veio de `map` e é descartável. Mas `alunos.sort(…)` bagunçaria a ordem original dos seus dados para sempre. Quando quiser ordenar sem estragar o original, ordene uma cópia: `[...alunos].sort(…)`.

### 4.8 Laço ou método?

| Situação | Ferramenta |
|---|---|
| Transformar cada item em outra coisa | `map` |
| Selecionar alguns itens | `filter` |
| Achar um item específico | `find` |
| Somar, contar ou agrupar | `reduce` |
| Só executar algo para cada item | `forEach` ou `for…of` |
| Precisa parar no meio (`break`) | `for` ou `for…of` — `forEach` não pode parar |
| Precisa do índice e da lógica é complexa | `for` clássico |

> **📌 Vale gravar**
> `map` transforma e devolve um array do **mesmo tamanho**; `filter` seleciona e devolve um array **de tamanho menor ou igual**; `forEach` percorre e devolve `undefined`. Usar `map` só para imprimir no console é erro de intenção — o array criado é jogado fora. Saiba dizer o que cada um devolve.

## 5. Objetos

Um array guarda uma lista de coisas parecidas. Um **objeto** guarda as **características** de uma coisa só, cada uma com um nome.

### 5.1 Criando e lendo

```js
const palestrante = {
  nome: "Ana Lúcia Ferreira",
  instituicao: "UNEMAT — Sinop",
  area: "ia",
  confirmado: true,
  temas: ["redes neurais", "agricultura de precisão"],
  contato: {
    email: "ana.ferreira@exemplo.edu.br",
    cidade: "Sinop",
  },
};

console.log(palestrante.nome);            // "Ana Lúcia Ferreira" — notação de ponto
console.log(palestrante["instituicao"]);  // notação de colchetes
console.log(palestrante.contato.cidade);  // "Sinop" — objeto aninhado
console.log(palestrante.temas[0]);        // "redes neurais" — array dentro de objeto
console.log(palestrante.telefone);        // undefined — propriedade inexistente
```

Cada par é uma **propriedade**: um nome (a chave) e um valor. O valor pode ser qualquer coisa — número, texto, booleano, array, outro objeto.

Quando usar colchetes em vez de ponto? Em dois casos: quando o nome da propriedade está em uma variável (como no `for…in`) e quando o nome tem espaços ou caracteres especiais.

```js
const campo = "area";
console.log(palestrante[campo]);   // "ia" — lê a propriedade cujo nome está na variável
console.log(palestrante.campo);    // undefined — procura uma propriedade chamada "campo"
```

### 5.2 Alterando

```js
palestrante.confirmado = false;                  // altera
palestrante.telefone = "(66) 99999-0000";        // adiciona
delete palestrante.telefone;                     // remove

console.log("nome" in palestrante);              // true  — a propriedade existe?
console.log("telefone" in palestrante);          // false
```

Repare que tudo isso funciona mesmo com `palestrante` declarado como `const`: como você viu na Aula 10, `const` congela a **ligação** entre o nome e o objeto, não o conteúdo do objeto.

### 5.3 Percorrendo um objeto

```js
const palestrante = { nome: "Ana Lúcia", instituicao: "UNEMAT", area: "ia" };

// Com for...in
for (const chave in palestrante) {
  console.log(chave, "→", palestrante[chave]);
}

// Com os utilitários de Object
console.log(Object.keys(palestrante));    // ["nome", "instituicao", "area"]
console.log(Object.values(palestrante));  // ["Ana Lúcia", "UNEMAT", "ia"]
console.log(Object.entries(palestrante)); // [["nome","Ana Lúcia"], ["instituicao","UNEMAT"], ["area","ia"]]

// Object.entries + for...of + desestruturação: o padrão mais legível
for (const [chave, valor] of Object.entries(palestrante)) {
  console.log(`${chave}: ${valor}`);
}
```

`Object.keys`, `values` e `entries` devolvem **arrays** — o que significa que todos os métodos da seção 4 funcionam com eles. É assim que se filtra ou ordena as propriedades de um objeto.

### 5.4 Copiando e mesclando

```js
const base = { nome: "Ana", area: "ia", confirmado: false };

const copia = { ...base };                       // cópia independente
const atualizado = { ...base, confirmado: true };  // cópia com uma alteração
const comExtra = { ...base, sala: "Lab 3" };       // cópia com propriedade nova

console.log(atualizado); // { nome: "Ana", area: "ia", confirmado: true }
console.log(base.confirmado); // false — o original não mudou
```

A ordem importa: propriedades escritas **depois** do spread sobrescrevem as que vieram dele. Esse padrão — copiar e alterar em vez de modificar no lugar — é a base do funcionamento de Vue e React, que você verá no Nível 3.

> **🔎 Por baixo do capô**
> O spread faz uma cópia **rasa** (*shallow*): as propriedades de primeiro nível são copiadas, mas objetos aninhados continuam sendo a mesma referência. Em `const copia = { ...palestrante }`, alterar `copia.nome` não afeta o original, mas alterar `copia.contato.cidade` **afeta**, porque `contato` é o mesmo objeto nos dois. Para uma cópia profunda de dados simples, existe `structuredClone(objeto)`, disponível em todos os navegadores modernos.

### 5.5 Objetos com funções dentro

Uma propriedade cujo valor é uma função chama-se **método**. Dentro dele, `this` aponta para o próprio objeto:

```js
const turma = {
  nome: "FACET-SNP-319",
  notas: [8.5, 7.0, 9.0],
  calcularMedia() {
    return this.notas.reduce((soma, n) => soma + n, 0) / this.notas.length;
  },
};

console.log(turma.calcularMedia().toFixed(2)); // "8.17"
```

`this` é um assunto grande, com armadilhas próprias — a Aula 13 volta a ele ao falar de arrow functions. Por ora, guarde a forma: dentro de um método, `this.propriedade` acessa o próprio objeto.

### 5.6 Desestruturação

Desestruturar é extrair propriedades para variáveis soltas, em uma linha:

```js
const palestrante = {
  nome: "Ana Lúcia Ferreira",
  area: "ia",
  contato: { email: "ana@exemplo.edu.br", cidade: "Sinop" },
};

// Sem desestruturação
const nomeAntigo = palestrante.nome;
const areaAntiga = palestrante.area;

// Com desestruturação
const { nome, area } = palestrante;
console.log(nome, area);

// Renomeando e com valor padrão
const { nome: nomeCompleto, telefone = "não informado" } = palestrante;
console.log(nomeCompleto, telefone); // "Ana Lúcia Ferreira" "não informado"

// Aninhada
const { contato: { cidade } } = palestrante;
console.log(cidade); // "Sinop"

// Em arrays, a posição é que manda
const [primeiraNota, segundaNota] = [8.5, 7.0, 9.0];
console.log(primeiraNota, segundaNota); // 8.5 7

// A troca de valores da seção 1.1, agora em uma linha
let a = "Ana";
let b = "Bruno";
[a, b] = [b, a];
console.log(a, b); // "Bruno" "Ana"
```

Você vai reencontrar a desestruturação em toda parte a partir da Aula 13 — é a forma padrão de receber parâmetros de função e de ler dados de uma API.

## 6. Array de objetos: a estrutura da web

Junte as duas ideias e você tem a estrutura de dados mais comum do desenvolvimento web: uma **lista** de **registros**, cada um com as mesmas propriedades. É o formato de uma tabela de banco de dados, de uma resposta de API em JSON e da lista de produtos de qualquer loja.

```js
const produtos = [
  { id: 1, nome: "Notebook", preco: 3500, categoria: "informatica", estoque: 12 },
  { id: 2, nome: "Mouse", preco: 80, categoria: "informatica", estoque: 0 },
  { id: 3, nome: "Caderno", preco: 25, categoria: "papelaria", estoque: 40 },
];

// Quais estão disponíveis?
const disponiveis = produtos.filter((p) => p.estoque > 0);
console.log(disponiveis.length); // 2

// Quanto vale o estoque inteiro?
const valorTotal = produtos.reduce((total, p) => total + p.preco * p.estoque, 0);
console.log(valorTotal); // 43000

// Do mais barato ao mais caro (sem estragar o original)
const porPreco = [...produtos].sort((a, b) => a.preco - b.preco);
console.log(porPreco.map((p) => p.nome)); // ["Caderno", "Mouse", "Notebook"]

// Achar pelo identificador
const item = produtos.find((p) => p.id === 3);
console.log(item.nome); // "Caderno"

// Busca por nome parcial, ignorando maiúsculas
const termo = "note";
const achados = produtos.filter((p) => p.nome.toLowerCase().includes(termo.toLowerCase()));
console.log(achados.map((p) => p.nome)); // ["Notebook"]
```

Três convenções que você deve adotar desde já:

1. **Todo registro tem um `id`** único e estável. É por ele que você acha, atualiza e remove — nunca pela posição no array, que muda a cada ordenação.
2. **Todos os registros têm as mesmas propriedades.** Se um item não tem valor para uma delas, use `null` ou `""`, não omita a propriedade — assim `map` e `filter` nunca encontram `undefined` inesperado.
3. **Valores de categoria são códigos curtos e sem acento** (`"ia"`, `"web"`), com o texto bonito ("Inteligência Artificial") ficando na exibição. Isso evita comparar strings com acento e maiúscula, e é exatamente o que os filtros da Aula 13 vão precisar.

## 7. Depurando laços no DevTools

`console.log` dentro de um laço que roda 200 vezes produz 200 linhas — e você perde a linha que importa. A aba **Sources** resolve isso.

### 7.1 Breakpoint simples

1. Abra o DevTools (<kbd>F12</kbd>) e vá à aba **Sources**.
2. Na árvore de arquivos à esquerda, abra o seu `.js`.
3. Clique no **número da linha** dentro do laço: aparece um marcador azul.
4. Recarregue a página. A execução **para** ali, com a linha destacada.
5. No painel **Scope**, à direita, veja o valor de cada variável naquele instante — inclusive o contador do laço.
6. Use os botões do topo: <kbd>F10</kbd> executa a próxima linha, <kbd>F11</kbd> entra em uma função, <kbd>F8</kbd> continua até o próximo breakpoint.

### 7.2 Breakpoint condicional — o truque que economiza a aula

Parar 200 vezes é inútil. Clique com o **botão direito** no número da linha e escolha **Add conditional breakpoint**. Digite uma condição, por exemplo `i === 47` ou `palestra.inscritos > palestra.vagas`. A execução só para quando a condição for verdadeira — e você chega direto no caso problemático.

Há ainda o **logpoint** (botão direito → *Add logpoint*): ele imprime uma mensagem sem parar a execução e **sem sujar o seu código** com `console.log` que você depois esquece de remover.

### 7.3 Watch

No painel **Watch**, clique em `+` e digite uma expressão — `palestras.length`, `total / contador`, `palestra.vagas - palestra.inscritos`. O DevTools recalcula e mostra o valor a cada passo. É a forma mais rápida de descobrir em qual volta a conta começou a errar.

> **🔬 Investigue**
> Crie um arquivo com o laço `for (let i = 0; i < 100; i++) { const quadrado = i * i; }` e ponha um breakpoint condicional em `i === 42`. Recarregue: a execução para na quadragésima terceira volta e o painel Scope mostra `i: 42`. Pressione <kbd>F10</kbd> uma vez e veja `quadrado` aparecer valendo 1764. Agora adicione `i * 2` ao painel Watch e pressione <kbd>F8</kbd> — o breakpoint não dispara de novo, porque a condição só é verdadeira uma vez. Compare o esforço disso com o de encontrar a mesma informação em cem linhas de `console.log`.

## 💻 Mão na massa — Os dados do evento e os relatórios no Console

Até agora, cada informação do site da **Semana Acadêmica de Sistemas de Informação** estava digitada no HTML, uma por uma. Hoje você cria a **fonte única de dados** do projeto — um arquivo com dois arrays de objetos — e escreve os primeiros relatórios sobre eles. Na Aula 13 esses mesmos dados deixam o console e viram cartões na tela.

### Passo 1 — criar `js/dados.js` e carregá-lo antes dos outros

Crie o arquivo `js/dados.js` e inclua-o no `<head>` das **cinco** páginas, **antes** de `js/app.js`. A ordem importa: com `defer`, os scripts executam na ordem em que aparecem no HTML, e o `app.js` precisa que os dados já existam.

**`site-evento/index.html`** — trecho do `<head>` (repita nas cinco páginas)

```html
<link rel="stylesheet" href="css/estilo.css">
<script src="js/dados.js" defer></script>
<script src="js/app.js" defer></script>
```

Na página de inscrição, o `js/inscricao.js` continua sendo o último da lista:

**`site-evento/inscricao.html`** — trecho do `<head>`

```html
<link rel="stylesheet" href="css/estilo.css">
<script src="js/dados.js" defer></script>
<script src="js/app.js" defer></script>
<script src="js/inscricao.js" defer></script>
```

Estrutura de pastas resultante:

```text
site-evento/
├── index.html
├── programacao.html
├── inscricao.html
├── palestrantes.html
├── contato.html
├── css/
│   └── estilo.css
├── img/
└── js/
    ├── dados.js
    ├── app.js
    ├── inscricao.js
    └── relatorios.js
```

### Passo 2 — os palestrantes

**`site-evento/js/dados.js`**

```js
// dados.js — fonte única de dados do site do evento.
// Carregado antes de todos os outros scripts, em todas as páginas.
// A partir da Aula 13, estas listas alimentam as páginas de verdade.

const palestrantes = [
  {
    id: 1,
    nome: "Ana Lúcia Ferreira",
    instituicao: "UNEMAT — Sinop",
    area: "ia",
    tema: "Redes neurais para prever a safra de soja",
    foto: "img/palestrante-01.jpg",
  },
  {
    id: 2,
    nome: "Bruno Takahashi",
    instituicao: "Startup AgroData",
    area: "dados",
    tema: "Dashboards que os produtores realmente usam",
    foto: "img/palestrante-02.jpg",
  },
  {
    id: 3,
    nome: "Carla Mendes",
    instituicao: "UFMT",
    area: "seguranca",
    tema: "O que um ataque de phishing ensina sobre UX",
    foto: "img/palestrante-03.jpg",
  },
  {
    id: 4,
    nome: "Diego Nascimento",
    instituicao: "Prefeitura de Sinop",
    area: "web",
    tema: "Acessibilidade em portais públicos: erros que vimos",
    foto: "img/palestrante-04.jpg",
  },
  {
    id: 5,
    nome: "Eduarda Ribeiro",
    instituicao: "UNEMAT — Sinop",
    area: "web",
    tema: "Do HTML ao deploy: o caminho do estudante",
    foto: "img/palestrante-05.jpg",
  },
  {
    id: 6,
    nome: "Felipe Arruda",
    instituicao: "Cooperativa Coopercana",
    area: "ia",
    tema: "Visão computacional no controle de pragas",
    foto: "img/palestrante-06.jpg",
  },
];
```

Repare que `area` guarda um código curto e sem acento. O nome bonito de cada área vive em um objeto separado, que funciona como um dicionário de tradução:

**`site-evento/js/dados.js`** — continuação

```js
// Dicionário de áreas: código → nome de exibição
const nomesDasAreas = {
  web: "Desenvolvimento Web",
  dados: "Ciência de Dados",
  seguranca: "Segurança",
  ia: "Inteligência Artificial",
};
```

### Passo 3 — a programação

**`site-evento/js/dados.js`** — continuação

```js
const palestras = [
  {
    id: 1,
    titulo: "Abertura e palestra magna: o futuro do desenvolvimento web",
    tipo: "palestra",
    area: "web",
    dia: 1,
    hora: "19:00",
    local: "Auditório Central",
    vagas: 300,
    inscritos: 212,
    palestranteId: 5,
  },
  {
    id: 2,
    titulo: "Minicurso: Git e GitHub do zero",
    tipo: "minicurso",
    area: "web",
    dia: 1,
    hora: "20:00",
    local: "Laboratório 2",
    vagas: 30,
    inscritos: 30,
    palestranteId: 4,
  },
  {
    id: 3,
    titulo: "Mesa-redonda: mercado de trabalho em Sinop",
    tipo: "mesa",
    area: "web",
    dia: 1,
    hora: "20:00",
    local: "Sala 105",
    vagas: 80,
    inscritos: 47,
    palestranteId: 5,
  },
  {
    id: 4,
    titulo: "Dashboards que os produtores realmente usam",
    tipo: "palestra",
    area: "dados",
    dia: 1,
    hora: "21:00",
    local: "Auditório Central",
    vagas: 300,
    inscritos: 96,
    palestranteId: 2,
  },
  {
    id: 5,
    titulo: "Minicurso: acessibilidade na prática",
    tipo: "minicurso",
    area: "web",
    dia: 2,
    hora: "19:00",
    local: "Laboratório 1",
    vagas: 30,
    inscritos: 28,
    palestranteId: 4,
  },
  {
    id: 6,
    titulo: "Minicurso: primeiros passos com redes neurais",
    tipo: "minicurso",
    area: "ia",
    dia: 2,
    hora: "19:00",
    local: "Laboratório 3",
    vagas: 25,
    inscritos: 25,
    palestranteId: 1,
  },
  {
    id: 7,
    titulo: "Segurança em aplicações web: dez erros comuns",
    tipo: "palestra",
    area: "seguranca",
    dia: 2,
    hora: "20:30",
    local: "Auditório Central",
    vagas: 300,
    inscritos: 154,
    palestranteId: 3,
  },
  {
    id: 8,
    titulo: "Visão computacional no controle de pragas",
    tipo: "palestra",
    area: "ia",
    dia: 2,
    hora: "21:00",
    local: "Sala 105",
    vagas: 80,
    inscritos: 61,
    palestranteId: 6,
  },
  {
    id: 9,
    titulo: "Maratona de programação",
    tipo: "maratona",
    area: "web",
    dia: 3,
    hora: "18:30",
    local: "Laboratórios 1 e 2",
    vagas: 60,
    inscritos: 45,
    palestranteId: 5,
  },
  {
    id: 10,
    titulo: "Minicurso: phishing e engenharia social",
    tipo: "minicurso",
    area: "seguranca",
    dia: 3,
    hora: "19:00",
    local: "Laboratório 3",
    vagas: 25,
    inscritos: 19,
    palestranteId: 3,
  },
  {
    id: 11,
    titulo: "Dados abertos e cidades inteligentes",
    tipo: "palestra",
    area: "dados",
    dia: 3,
    hora: "20:00",
    local: "Auditório Central",
    vagas: 300,
    inscritos: 88,
    palestranteId: 2,
  },
  {
    id: 12,
    titulo: "Encerramento e premiação",
    tipo: "palestra",
    area: "web",
    dia: 3,
    hora: "22:00",
    local: "Auditório Central",
    vagas: 300,
    inscritos: 130,
    palestranteId: 5,
  },
];

console.log(`dados.js carregado: ${palestras.length} atividades, ${palestrantes.length} palestrantes.`);
```

O campo `palestranteId` é uma **referência**: em vez de repetir nome, instituição e foto em cada palestra, guardamos só o identificador e buscamos o resto quando precisar. É exatamente o que uma chave estrangeira faz em um banco de dados, assunto do Nível 2.

### Passo 4 — os relatórios

Crie `js/relatorios.js` e inclua-o **só em `programacao.html`**, depois dos outros scripts. Ele não altera a página: escreve tudo no Console.

**`site-evento/programacao.html`** — trecho do `<head>`

```html
<link rel="stylesheet" href="css/estilo.css">
<script src="js/dados.js" defer></script>
<script src="js/app.js" defer></script>
<script src="js/relatorios.js" defer></script>
```

**`site-evento/js/relatorios.js`**

```js
// relatorios.js — relatórios do evento no Console.
// Depende de js/dados.js, que precisa ser carregado antes.

const DIAS_DO_EVENTO = 3;

const formatarPercentual = new Intl.NumberFormat("pt-BR", {
  style: "percent",
  maximumFractionDigits: 1,
});

// ===== 1. A programação completa em tabela =====
console.group("Programação completa");
console.table(palestras, ["dia", "hora", "titulo", "local"]);
console.groupEnd();

// ===== 2. Totais gerais (reduce) =====
const totalVagas = palestras.reduce((soma, p) => soma + p.vagas, 0);
const totalInscritos = palestras.reduce((soma, p) => soma + p.inscritos, 0);

console.group("Totais gerais");
console.log("Atividades:", palestras.length);
console.log("Vagas oferecidas:", totalVagas);
console.log("Inscrições feitas:", totalInscritos);
console.log("Ocupação geral:", formatarPercentual.format(totalInscritos / totalVagas));
console.groupEnd();

// ===== 3. Resumo por dia (laço aninhado: dias × atividades) =====
console.group("Resumo por dia");
for (let dia = 1; dia <= DIAS_DO_EVENTO; dia++) {
  const doDia = palestras.filter((p) => p.dia === dia);
  const inscritosDoDia = doDia.reduce((soma, p) => soma + p.inscritos, 0);

  console.group(`Dia ${dia} — ${doDia.length} atividades, ${inscritosDoDia} inscrições`);
  for (const palestra of doDia) {
    console.log(`${palestra.hora} · ${palestra.titulo} (${palestra.local})`);
  }
  console.groupEnd();
}
console.groupEnd();

// ===== 4. Contagem por área (reduce com objeto acumulador) =====
const porArea = palestras.reduce((conta, p) => {
  conta[p.area] = (conta[p.area] ?? 0) + 1;
  return conta;
}, {});

console.group("Atividades por área");
for (const [codigo, quantidade] of Object.entries(porArea)) {
  console.log(`${nomesDasAreas[codigo]}: ${quantidade}`);
}
console.groupEnd();

// ===== 5. Atividades esgotadas e as mais concorridas =====
const esgotadas = palestras.filter((p) => p.inscritos >= p.vagas);
const maisConcorrida = palestras.reduce((maior, p) =>
  p.inscritos / p.vagas > maior.inscritos / maior.vagas ? p : maior
);

console.group("Alertas");
console.log("Esgotadas:", esgotadas.map((p) => p.titulo));
console.log("Mais concorrida:", maisConcorrida.titulo,
  formatarPercentual.format(maisConcorrida.inscritos / maisConcorrida.vagas));
console.log("Alguma atividade sem inscritos?", palestras.some((p) => p.inscritos === 0));
console.log("Todas têm local definido?", palestras.every((p) => p.local !== ""));
console.groupEnd();

// ===== 6. Busca por trilha (filter + includes) =====
const trilhaProcurada = "seguranca";
const daTrilha = palestras.filter((p) => p.area === trilhaProcurada);

console.group(`Trilha: ${nomesDasAreas[trilhaProcurada]}`);
if (daTrilha.length === 0) {
  console.log("Nenhuma atividade nesta trilha.");
} else {
  daTrilha.forEach((p) => console.log(`Dia ${p.dia}, ${p.hora} — ${p.titulo}`));
}
console.groupEnd();

// ===== 7. Juntando as duas listas (find) =====
console.group("Quem apresenta o quê");
for (const palestra of palestras) {
  const responsavel = palestrantes.find((pessoa) => pessoa.id === palestra.palestranteId);
  const nome = responsavel?.nome ?? "A definir";
  console.log(`${palestra.titulo} → ${nome}`);
}
console.groupEnd();

// ===== 8. Palestras ordenadas por ocupação (cópia + sort) =====
const porOcupacao = [...palestras]
  .sort((a, b) => b.inscritos / b.vagas - a.inscritos / a.vagas)
  .map((p) => ({
    titulo: p.titulo,
    ocupacao: formatarPercentual.format(p.inscritos / p.vagas),
  }));

console.group("Ranking de ocupação");
console.table(porOcupacao);
console.groupEnd();
```

Três detalhes valem atenção:

- **`console.table(palestras, ["dia", "hora", "titulo", "local"])`** — o segundo argumento escolhe quais colunas mostrar. Sem ele, a tabela sai com as dez propriedades e fica ilegível na projeção.
- **`responsavel?.nome ?? "A definir"`** — se algum `palestranteId` apontar para um identificador inexistente, `find` devolve `undefined`; o `?.` evita o `TypeError` e o `??` fornece o texto padrão. É a dupla da Aula 11 trabalhando junto com o `find` de hoje.
- **`[...palestras].sort(…)`** — a cópia protege a ordem original. Sem os três pontinhos, o array `palestras` ficaria reordenado para todos os scripts que rodarem depois.

### Como testar

1. Abra `programacao.html` no Live Server e o Console (<kbd>F12</kbd>). Devem aparecer oito grupos, todos recolhíveis, e **nenhuma** linha vermelha.
2. A primeira linha do Console deve ser `dados.js carregado: 12 atividades, 6 palestrantes.`, provando que a ordem dos scripts está certa.
3. Em "Totais gerais": 1.830 vagas, 935 inscrições e ocupação de 51,1%.
4. Em "Resumo por dia": 4 atividades em cada um dos três dias.
5. Em "Alertas": duas atividades esgotadas (o minicurso de Git e o de redes neurais) e a resposta `false` para "Alguma atividade sem inscritos?".
6. Em "Quem apresenta o quê": nenhum "A definir". Troque o `palestranteId` de uma palestra para `99`, recarregue e confira que aparece "A definir" — sem erro. Desfaça.
7. Troque `trilhaProcurada` para `"ia"` e recarregue: o grupo passa a listar duas atividades. Troque para `"robotica"`: aparece "Nenhuma atividade nesta trilha." Volte para `"seguranca"`.
8. Ponha um breakpoint condicional na linha do `for (const palestra of palestras)` com a condição `palestra.dia === 3` e recarregue: a execução para na primeira atividade do terceiro dia. Confira no painel Scope.

Resultado esperado: toda a informação do evento vive em um único arquivo de dados, e qualquer relatório novo é uma linha de `filter`, `map` ou `reduce` — nenhuma informação repetida no HTML.

## 🧪 Laboratório

Os exercícios do Nível B pedem **funções**. A sintaxe completa é assunto da Aula 13; por ora, use o mesmo esqueleto das Aulas 10 e 11:

```js
function nomeDaFuncao(lista) {
  const resultado = lista.length;
  return resultado;
}

console.log(nomeDaFuncao([1, 2, 3])); // 3
```

### Nível A — Fixação

**A1.** Qual a diferença entre `for…of` e `for…in`? Quando usar cada um? O que acontece se você usar `for…in` em um array?

**A2.** Qual a diferença entre `map`, `filter` e `forEach`? O que **cada um devolve**? Dê um exemplo em que usar `map` é erro de intenção.

**A3.** Dado `const n = [4, 8, 15, 16, 23, 42]`, escreva expressões que devolvam: (a) só os pares; (b) cada valor dobrado; (c) a soma total; (d) o primeiro maior que 20; (e) `true` se todos forem positivos; (f) os três maiores, em ordem decrescente.

**A4.** Dado `const p = { nome: "Ana", end: { cidade: "Sinop", uf: "MT" } }`, escreva: (a) o acesso à cidade; (b) a desestruturação de `nome`; (c) uma cópia com a propriedade `fase` valendo 3; (d) um array com todas as chaves de `p`; (e) o acesso à cidade usando notação de colchetes com o nome da propriedade em uma variável.

**A5.** O que é uma estrutura sequencial? Reescreva o trecho abaixo na ordem correta e explique por que a ordem original produz um resultado errado sem gerar nenhum erro.

```js
const media = (soma / 3).toFixed(1);
const soma = 8 + 7 + 9;
console.log(media);
```

**A6.** Escreva o mesmo laço, que imprime os números de 1 a 10, nas quatro formas: `for`, `while`, `do…while` e `for…of` (neste último, sobre um array criado com `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`).

**A7.** Qual a diferença entre `break` e `continue`? Escreva um laço que percorra `[3, 7, 0, 5, 9]` e imprima os valores, pulando os zeros e parando ao encontrar um número maior que 8.

**A8.** Escreva um laço infinito acidental (sem executá-lo), explique por que ele nunca termina e mostre as duas maneiras de corrigi-lo.

**A9.** Quando `do…while` é a escolha correta? Dê um exemplo do site do evento em que ele seria mais adequado que `while`.

**A10.** Escreva um laço aninhado que gere a tabuada de 1 a 5, agrupada com `console.group`. Quantas vezes o corpo interno executa? Mostre a conta.

**A11.** Anote sua previsão para cada linha e só depois teste no Console:

```js
const a = [10, 9, 1];
console.log(a.sort());
console.log([1, 2, 3].map((n) => n * 2));
console.log([1, 2, 3].forEach((n) => n * 2));
console.log([1, 2, 3].filter((n) => n > 5));
console.log([].reduce((s, n) => s + n, 0));
console.log([1, 2, 3].includes("2"));
console.log(Object.keys({ b: 1, a: 2 }));
```

**A12.** O trecho abaixo deveria imprimir os cinco nomes, mas imprime seis linhas e a última é `undefined`. Encontre o erro, corrija e explique o que é um erro "por um".

```js
const nomes = ["Ana", "Bruno", "Carla", "Diego", "Eduarda"];

for (let i = 0; i <= nomes.length; i++) {
  console.log(nomes[i]);
}
```

### Nível B — Aplicação

**B1.** Usando o array `palestras` da Mão na massa, escreva funções que devolvam: (a) o total de vagas ainda livres no evento; (b) as atividades sem nenhuma vaga livre; (c) a atividade com mais inscritos; (d) um objeto com a média de ocupação por área; (e) a lista ordenada por horário dentro de cada dia; (f) uma busca por título parcial, ignorando maiúsculas e acentos.

Resultado esperado: seis funções testadas no Console, cada uma com pelo menos duas chamadas de exemplo; a busca por `"git"` encontra "Minicurso: Git e GitHub do zero"; a busca por `"programacao"` (sem cedilha nem til) encontra "Maratona de programação".

<details><summary>Dica</summary>

Para (d), use `reduce` com um objeto acumulador guardando soma e contagem por área, e só depois divida. Para (f), normalize os dois lados da comparação com `texto.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase()` — a expressão regular será formalizada na Aula 14, mas você pode usá-la como receita e explicar em um comentário o que ela faz.
</details>

**B2.** Escreva `contarPalavras(texto)` que devolva um objeto com cada palavra e sua frequência, ignorando maiúsculas e pontuação. Depois escreva `topPalavras(texto, n)` que devolva as `n` mais frequentes, em ordem decrescente, como um array de objetos `{ palavra, vezes }`.

Resultado esperado: `contarPalavras("O evento é bom. O evento é gratuito!")` devolve `{ o: 2, evento: 2, é: 2, bom: 1, gratuito: 1 }`; `topPalavras(texto, 2)` devolve os dois primeiros em ordem decrescente de frequência.

<details><summary>Dica</summary>

`texto.toLowerCase().split(/[^a-zà-ú]+/)` quebra o texto em palavras descartando pontuação; filtre as strings vazias que sobram nas pontas. Para ordenar o resultado, `Object.entries(contagem)` transforma o objeto em array de pares — e aí `sort` e `map` funcionam normalmente.
</details>

**B3.** Escreva `gerarTabuada(n)` que devolva uma **string** formatada com a tabuada de 1 a 10 de `n` (uma linha por multiplicação), e `gerarTodasTabuadas()` que devolva as tabuadas de 1 a 10 concatenadas, separadas por uma linha em branco. Use apenas laços e template literals.

Resultado esperado: `gerarTabuada(7)` devolve uma string de dez linhas começando por `"7 x 1 = 7"`; `console.log(gerarTodasTabuadas())` imprime 10 blocos legíveis no Console.

<details><summary>Dica</summary>

Acumule com ``texto += `${n} x ${i} = ${n * i}\n` ``. O `\n` é a quebra de linha da Aula 10 — e o `console.log` de uma string com `\n` já imprime em várias linhas. Uma alternativa mais elegante: monte um array de linhas e use `join("\n")` no fim.
</details>

**B4.** Usando o array `palestrantes`, escreva **um único encadeamento** (`filter` + `map` + `sort` + `join`) que produza uma string com os nomes dos palestrantes das áreas de web e de IA, em ordem alfabética portuguesa, separados por vírgula.

Resultado esperado: uma linha de código (quebrada em várias por legibilidade) que devolve exatamente `"Ana Lúcia Ferreira, Diego Nascimento, Eduarda Ribeiro, Felipe Arruda"`.

<details><summary>Dica</summary>

O filtro precisa aceitar duas áreas: `["web", "ia"].includes(pessoa.area)` é mais limpo que duas comparações com `||`. Na ordenação, `localeCompare(b, "pt-BR")` é obrigatório para que "Ana Lúcia" apareça antes de "Diego" mesmo com acentos.
</details>

**B5.** Escreva `analisarTurma(alunos)` que receba um array de objetos `{ nome, notas: [] }` e devolva um objeto com: a média de cada aluno, a média geral da turma, o melhor e o pior desempenho e a quantidade de aprovados (média maior ou igual a 6). Use **apenas** métodos de ordem superior, sem nenhum `for`.

Resultado esperado: para uma turma de cinco alunos, um objeto com `medias` (array de `{ nome, media }`), `mediaGeral`, `melhor`, `pior` e `aprovados`; todas as médias arredondadas em uma casa decimal.

<details><summary>Dica</summary>

Comece com `map` para calcular a média de cada aluno (um `reduce` dentro do `map`). Com esse array pronto, `mediaGeral` é outro `reduce`, `melhor` e `pior` saem de um `reduce` comparativo (ou de um `sort` sobre uma cópia) e `aprovados` é `filter(...).length`. Arredonde só no fim, nunca no meio — arredondar antes de somar distorce o resultado.
</details>

**B6.** Escreva `agruparPorDia(palestras)` que devolva um objeto no formato `{ 1: [...], 2: [...], 3: [...] }`, com as atividades de cada dia já ordenadas por horário. Depois imprima o resultado com `for…in` e `console.group`, uma seção por dia.

Resultado esperado: um objeto com três chaves; `agruparPorDia(palestras)[2].length` devolve 4; dentro de cada dia, a primeira atividade é a de horário mais cedo.

<details><summary>Dica</summary>

Um `reduce` com objeto acumulador resolve o agrupamento: se a chave do dia ainda não existe, crie um array vazio antes de dar `push`. Como `hora` é uma string no formato `"HH:MM"`, a comparação de texto já ordena corretamente — `"09:00" < "19:00"` é `true`. Isso só funciona porque o formato tem dois dígitos sempre; explique isso em um comentário.
</details>

### Nível C — Desafio

**C1.** Modele o **seu projeto autoral** como dados. Crie `js/dados.js` com pelo menos **doze** registros em um array de objetos, cada um com no mínimo seis propriedades (incluindo `id` único, um campo de categoria em código curto, um campo numérico e um campo de texto longo). Crie também o objeto-dicionário que traduz os códigos de categoria em nomes de exibição. Depois escreva `js/relatorios.js` com pelo menos seis relatórios diferentes no Console: um `console.table` filtrado, um total com `reduce`, uma contagem por categoria, um ranking ordenado, uma busca por texto parcial e um relatório que combine duas listas com `find`.

<details><summary>Dica</summary>

Escolha as propriedades pensando no que a página vai mostrar na Aula 13 — se um cartão precisa de foto, o registro precisa do caminho da imagem. Doze registros parecem muitos, mas são o mínimo para que filtros e ordenações mostrem alguma coisa interessante; com três, todo relatório fica igual. Copie a estrutura do `dados.js` do evento e troque o domínio, não a arquitetura.
</details>

**C2.** Escreva `primos(n)` que devolva todos os números primos até `n` usando o **crivo de Eratóstenes**: crie um array de `n + 1` posições marcadas como `true`, percorra a partir do 2 e marque como `false` todos os múltiplos de cada número que ainda estiver marcado. Meça o tempo com `console.time` para `n = 100`, `n = 10.000` e `n = 1.000.000` e compare com a abordagem ingênua (testar a divisibilidade de cada número por todos os anteriores).

<details><summary>Dica</summary>

`new Array(n + 1).fill(true)` cria o array inicial. O laço externo só precisa ir até `Math.sqrt(n)` — todo múltiplo maior já terá sido marcado por um fator menor. O laço interno pode começar em `i * i`, não em `i * 2`, pelo mesmo motivo. A diferença de tempo entre as duas abordagens em um milhão de números é da ordem de mil vezes; anote os números medidos.
</details>

## 🏆 Desafios

### ⭐ O relatório que ninguém pediu
Tags: javascript, investigacao, projeto

Todo conjunto de dados esconde uma informação que ninguém tinha pensado em perguntar. Com os arrays `palestras` e `palestrantes` da Mão na massa, quantas perguntas interessantes você consegue responder em uma linha cada? Qual instituição tem mais representantes? Qual horário concentra mais inscrições? Existe alguma sala ociosa? Descubra três fatos sobre o evento que não aparecem em nenhum relatório do Passo 4 — e prove cada um com código, não com opinião.

**Critérios de pronto**

- Um arquivo `curiosidades.js` com **três** relatórios novos, cada um resolvido com uma única expressão encadeada (`filter`, `map`, `reduce`, `sort`), acompanhada de um comentário de uma linha explicando a pergunta que ele responde.
- Cada relatório imprime o resultado com `console.group` e um título em português.
- Pelo menos um dos três usa `Object.entries` para percorrer o resultado de um agrupamento.
- Um comentário no fim do arquivo com a descoberta mais surpreendente e o que a organização do evento deveria fazer a respeito.

<details><summary>Pistas</summary>

1. Agrupar é sempre `reduce` com um objeto acumulador: `conta[chave] = (conta[chave] ?? 0) + 1`.
2. Para "qual é o maior", `reduce` comparativo evita ordenar a lista inteira — e é mais rápido em listas grandes.
3. Duas listas se cruzam com `find` (um item) ou `filter` (vários): "quantas atividades cada palestrante tem" é um `map` sobre `palestrantes` com um `filter` sobre `palestras` dentro.
</details>

### ⭐⭐ Caça ao bug: o laço que conta errado
Tags: javascript, bug, devtools, refatoracao

O script abaixo deveria montar o resumo da programação. Ele roda, imprime números — e todos estão errados. São **seis** defeitos: um erro "por um", um `for…in` usado onde deveria ser `for…of`, um `sort` que ordena como texto, um `reduce` sem valor inicial que quebra com lista vazia, um array modificado durante a iteração e um `find` cujo resultado é usado sem verificação. Encontre os seis usando breakpoints condicionais — não `console.log` espalhado.

**`js/resumo-com-bug.js`**

```js
const atividades = [
  { id: 1, titulo: "Abertura", dia: 1, inscritos: 212 },
  { id: 2, titulo: "Git do zero", dia: 1, inscritos: 30 },
  { id: 3, titulo: "Acessibilidade", dia: 2, inscritos: 28 },
  { id: 4, titulo: "Segurança", dia: 2, inscritos: 154 },
  { id: 5, titulo: "Maratona", dia: 3, inscritos: 45 },
];

let total = 0;
for (let i = 0; i <= atividades.length; i++) {
  total += atividades[i].inscritos;
}
console.log("Total de inscritos:", total);

for (const atividade in atividades) {
  console.log("Atividade:", atividade.titulo);
}

const porInscritos = atividades.sort((a, b) => a.inscritos > b.inscritos);
console.log("Mais concorrida:", porInscritos[0].titulo);

const vazias = [];
const media = vazias.reduce((soma, a) => soma + a.inscritos);
console.log("Média das vazias:", media);

atividades.forEach((a) => {
  if (a.inscritos < 50) {
    atividades.splice(atividades.indexOf(a), 1);
  }
});
console.log("Sobraram:", atividades.length);

const procurada = atividades.find((a) => a.id === 99);
console.log("Procurada:", procurada.titulo);
```

**Critérios de pronto**

- Um arquivo `resumo-corrigido.js` que imprime: total de 469 inscritos, os cinco títulos, "Segurança" como mais concorrida, `0` como média da lista vazia, a contagem correta das atividades com menos de 50 inscritos e uma mensagem amigável quando o `find` não acha nada.
- O array original `atividades` continua com cinco itens ao fim do script (nenhum método destrutivo agiu sobre ele).
- Um arquivo `bugs.md` com uma tabela de seis linhas: sintoma, causa e correção.
- Pelo menos um breakpoint condicional usado durante a investigação, documentado com a condição que você digitou.

<details><summary>Pistas</summary>

1. O primeiro erro produz `Uncaught TypeError: Cannot read properties of undefined (reading 'inscritos')` — e a linha do erro diz exatamente qual índice foi longe demais.
2. `for…in` sobre um array entrega as chaves como **texto**; imprima `typeof atividade` dentro do laço para se convencer.
3. Uma função comparadora de `sort` precisa devolver um **número** (negativo, zero ou positivo), não um booleano. `true` vira 1 e `false` vira 0 — a ordenação fica indefinida.
4. Remover itens de um array enquanto o percorre faz o índice interno pular posições. Prefira `filter`, que constrói uma lista nova.
5. Todo `find` pode devolver `undefined`. A dupla `?.` e `??` da Aula 11 resolve em uma linha.
</details>

### ⭐⭐⭐ O agrupador genérico
Tags: javascript, refatoracao, investigacao, projeto

Você já agrupou atividades por dia e contou por área. Agora repare: os dois códigos são quase idênticos — muda apenas a propriedade usada como chave. Programadores experientes sentem coceira ao ver isso e escrevem **uma** função que resolve os dois casos. Construa `agruparPor(lista, chave)`, que funcione com qualquer array de objetos e qualquer propriedade, e depois estenda-a para aceitar também uma função que calcula a chave — o que permite agrupar por faixas ("lotado", "meio cheio", "vazio") e não só por valores existentes. Ao terminar, compare a sua versão com o método nativo `Object.groupBy` e descubra por que ele ainda não pode ser usado em qualquer projeto.

**Critérios de pronto**

- `agruparPor(palestras, "dia")` devolve `{ 1: [...], 2: [...], 3: [...] }`, e `agruparPor(palestrantes, "area")` devolve as quatro áreas — com a mesma função, sem nenhum `if` sobre o nome da propriedade.
- `agruparPor(palestras, (p) => p.inscritos >= p.vagas ? "esgotada" : "com vagas")` devolve dois grupos, provando que a função aceita tanto um nome de propriedade quanto uma função de classificação.
- Uma função `contarPor(lista, chave)` construída **sobre** `agruparPor`, sem repetir a lógica de agrupamento.
- Um bloco de testes com pelo menos seis casos, incluindo lista vazia e uma chave inexistente (que deve gerar um único grupo `"undefined"`, e não um erro).
- Um comentário de até dez linhas comparando a sua implementação com `Object.groupBy` da documentação da MDN: o que muda na assinatura, o que muda no tipo devolvido e qual é a situação de suporte nos navegadores.

<details><summary>Pistas</summary>

1. `typeof chave === "function"` distingue os dois modos de uso — a mesma técnica que bibliotecas famosas usam para aceitar parâmetros flexíveis.
2. O corpo é um `reduce` de cinco linhas: calcule a chave, crie o array se ele não existir (`acumulado[valor] ??= []`), dê `push`, devolva o acumulado.
3. `contarPor` pode ser `Object.entries(agruparPor(lista, chave)).map(([k, itens]) => [k, itens.length])` — e depois `Object.fromEntries` monta o objeto de volta.
4. `Object.groupBy` devolve um objeto sem protótipo e aceita **apenas** função (nunca o nome da propriedade). Procure a tabela de compatibilidade na MDN e veja a partir de qual versão de cada navegador ele existe.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `Uncaught TypeError: Cannot read properties of undefined (reading 'nome')` dentro de um laço | erro "por um": a condição usa `i <= lista.length` e lê uma posição inexistente | use `i < lista.length`, ou troque por `for…of`, que não erra o limite |
| `Uncaught ReferenceError: palestras is not defined` | `js/dados.js` não foi incluído na página, ou foi incluído **depois** do script que o usa | inclua `dados.js` antes dos demais no `<head>`, todos com `defer` |
| `Uncaught TypeError: Assignment to constant variable.` no cabeçalho do `for` | contador declarado com `const` | use `let` no contador; `const` só em `for…of` |
| `[10, 9, 1].sort()` devolve `[1, 10, 9]` | sem função comparadora, `sort` converte tudo em texto | passe `(a, b) => a - b` para números e `(a, b) => a.localeCompare(b, "pt-BR")` para textos |
| `Uncaught TypeError: Reduce of empty array with no initial value` | `reduce` sem o segundo argumento em um array vazio | passe sempre o valor inicial: `reduce((s, x) => s + x, 0)` |
| A ordem original dos dados mudou sozinha | `sort` e `reverse` **alteram** o array em que atuam | ordene uma cópia: `[...lista].sort(…)` |
| O laço não termina e a aba congela | a variável da condição nunca muda, muda na direção errada, ou compara decimais com `===` | atualize o contador; use `<`/`>` em vez de `===`; feche a aba com <kbd>Shift</kbd>+<kbd>Esc</kbd> |
| `forEach` percorre a lista errada depois de remover itens | o array foi modificado durante a própria iteração | construa uma lista nova com `filter` em vez de remover no lugar |
| `for…in` sobre um array imprime `0`, `1`, `2` como texto | `for…in` percorre chaves, não valores | use `for…of` para valores ou `for` clássico para índices |
| Um `map` foi usado só para imprimir e o retorno virou lixo | erro de intenção: `map` é para transformar | use `forEach` ou `for…of` quando não houver transformação |
| `if (lista.find(…))` entra no ramo errado | `find` devolve o item ou `undefined`; se o item for `0` ou `""`, ele é falsy | compare explicitamente: `if (lista.find(…) !== undefined)` |
| `if (lista.findIndex(…))` erra quando o item é o primeiro | `findIndex` devolve `0` para a primeira posição, e `0` é falsy | compare com `-1`: `if (indice !== -1)` |
| Alterar uma cópia alterou o original | `const copia = original` cria outro nome, não uma cópia | copie com spread: `[...lista]` ou `{ ...objeto }` |
| `console.table` sai ilegível, com dez colunas | a tabela mostra todas as propriedades por padrão | passe o array de colunas: `console.table(lista, ["dia", "hora", "titulo"])` |

## 🏠 Para praticar depois da aula (1 h)

**Parte 1 — Leitura (20 min).** FLANAGAN, D. *JavaScript: o guia definitivo*, capítulos de estruturas de controle e de arrays. STEFANOV, S. *Padrões JavaScript*, capítulo sobre arrays e objetos. Na MDN, leia "Laços e iterações" e a página de `Array` (links em Para aprofundar). Anote dois métodos de array que existem na MDN e não apareceram nesta aula.

**Parte 2 — Produção (30 min).** Produza os exercícios **B2** (`contarPalavras` e `topPalavras`) e **B5** (`analisarTurma`) em arquivos `.js` comentados, com pelo menos cinco casos de teste cada, demonstrados no Console. Produza também o exercício **C1**: o `js/dados.js` do seu projeto autoral, com doze registros, e o `js/relatorios.js` com seis relatórios.

**Critério de pronto:** o `dados.js` do projeto autoral carrega em todas as páginas sem erro e imprime, na primeira linha do Console, a contagem de registros; os seis relatórios rodam sem nenhuma linha vermelha; nenhum relatório altera a ordem original do array de dados; nenhum dado do domínio continua digitado à mão no HTML das páginas que serão renderizadas na próxima aula.

**Parte 3 — Discussão (10 min).** Em texto próprio (ou no fórum da turma, se você cursa a disciplina): discuta quando o `for` clássico ainda é preferível a `map`/`filter`/`reduce`, com um exemplo concreto de cada situação (um em que o laço vence, um em que o método vence).

**Guarde no seu repositório:** commit + push (ou a pasta do projeto).

## ✅ Checkpoint do projeto

Ao fim desta aula, o repositório do seu projeto autoral deve ter:

- [ ] `js/dados.js` com pelo menos doze registros em um array de objetos, cada um com `id` único e no mínimo seis propriedades.
- [ ] Um objeto-dicionário que traduz códigos de categoria em nomes de exibição.
- [ ] `js/dados.js` incluído com `defer` **antes** dos demais scripts em todas as páginas, e a contagem de registros impressa no Console ao carregar.
- [ ] `js/relatorios.js` com pelo menos seis relatórios: `console.table` com colunas escolhidas, total com `reduce`, contagem por categoria, ranking ordenado, busca por texto parcial e junção de duas listas com `find`.
- [ ] Pelo menos um laço aninhado usado para agrupar (por dia, por categoria ou por faixa).
- [ ] Nenhuma ordenação feita diretamente sobre o array de dados (sempre `[...lista].sort(…)`).
- [ ] Nenhum `for…in` sobre arrays e nenhum `sort` de números sem função comparadora.
- [ ] Zero ocorrências de `var` e de `==` em todos os arquivos `.js`.
- [ ] Nenhum erro vermelho no Console em nenhuma das páginas.

## 📚 Para aprofundar

- MDN — **Laços e iterações** (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Guide/Loops_and_iteration> — todos os laços da linguagem, com exemplos executáveis.
- MDN — **`Array`** (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Global_Objects/Array> — a lista completa de métodos; marque a página nos favoritos.
- MDN — **`Array.prototype.reduce`** (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Global_Objects/Array/reduce> — os exemplos de acumulador com objeto são os mais úteis.
- MDN — **`Array.prototype.sort`** (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Global_Objects/Array/sort> — a explicação de por que a função comparadora precisa devolver um número.
- MDN — **Trabalhando com objetos** (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Guide/Working_with_objects> — criação, acesso, aninhamento e iteração.
- MDN — **Desestruturação** (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Operators/Destructuring> — arrays, objetos, valores padrão e renomeação.
- Chrome DevTools — **Depurando JavaScript**: <https://developer.chrome.com/docs/devtools/javascript?hl=pt-br> — breakpoints condicionais, logpoints e o painel Watch.
- javascript.info: <https://javascript.info/> — capítulos "Loops", "Arrays", "Array methods" e "Objects"; cada um traz exercícios com solução comentada.
- web.dev — **Learn JavaScript**: <https://web.dev/learn/javascript> — módulos de arrays e de laços, com exercícios interativos.
- FLANAGAN, David. *JavaScript: o guia definitivo*. Bookman, 2014 — capítulos de instruções, arrays e objetos.
- STEFANOV, Stoyan. *Padrões JavaScript*. Novatec, 2010 — capítulo 3 (literais e construtores), sobre a forma correta de criar arrays e objetos.
- MILETTO, Evandro M.; BERTAGNOLLI, Silvia C. *Desenvolvimento de software II*. Bookman, 2014 — capítulo de estruturas de dados aplicadas à web.

Na próxima aula, o JavaScript sai do console e entra na página: você vai escrever as suas próprias funções, conhecer o DOM — a árvore de objetos que o navegador monta a partir do HTML — e reagir a cliques, teclas e envios de formulário. A lista de palestrantes que hoje só existe no `dados.js` vai virar cartões de verdade na tela, com filtro por área.
