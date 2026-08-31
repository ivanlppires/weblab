# Aula 11 — Variáveis, operações aritméticas e estruturas de controle

> **Nível 1 — Introdução ao Desenvolvimento Web** · Unidade 3: JavaScript e interatividade
> WebLab · UNEMAT Sinop · Prof. Ivan Luiz Pedroso Pires
> **Carga:** 3 aulas de 50 min (presencial) + 1 h (assíncrona)

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Explicar escopo global, de função e de bloco, e justificar por que `const` e `let` substituíram `var`.
- Reconhecer a zona morta temporal e ler a mensagem `Cannot access 'x' before initialization`.
- Aplicar todos os operadores aritméticos, incluindo `%` e `**`, e prever o resultado de uma expressão com base na tabela de precedência.
- Usar o objeto `Math` para arredondar, limitar e sortear valores, e explicar por que `0.1 + 0.2` não é `0.3`.
- Escolher entre `||`, `??` e `?.` sabendo exatamente o que cada um testa, e explicar o curto-circuito.
- Escrever condicionais com `if`/`else if`/`else`, com o operador ternário e com `switch`, decidindo qual forma cabe em cada problema.
- Formatar números, moedas e datas para o público brasileiro com `Intl.NumberFormat` e `toLocaleDateString`.
- Fazer a página de inscrição do site do evento decidir sozinha quando avisar "Últimas vagas!".

## 📋 Pré-requisitos

- [ ] Site do evento com as cinco páginas funcionando no Live Server e `js/app.js` incluído com `defer` no `<head>` de todas elas.
- [ ] `js/inscricao.js` criado na Aula 10, calculando vagas restantes e percentual de ocupação e escrevendo os valores em `inscricao.html`.
- [ ] Console do navegador aberto (<kbd>F12</kbd>) e sem nenhuma linha vermelha em nenhuma das cinco páginas.
- [ ] Revisar da Aula 10: `const`/`let`, os sete tipos primitivos, `typeof`, os oito valores falsy, `===` versus `==` e template literals.

> Na aula passada o JavaScript entrou no site do evento: você criou `js/app.js`, aprendeu a declarar variáveis, conheceu os tipos primitivos e fez a página de inscrição calcular as vagas restantes em vez de exibir um número digitado à mão. O script, porém, faz sempre a mesma coisa — ele não **decide** nada. Hoje você aprende a calcular de verdade (com todos os operadores e com o objeto `Math`), a combinar condições com `&&`, `||`, `??` e `?.` e a escrever as primeiras estruturas de decisão. Ao fim da aula, a página de inscrição avisa "Últimas vagas!" sozinha e a página inicial mostra quantos dias faltam para o evento.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Escopo, hoisting e zona morta temporal; operadores aritméticos, precedência e o objeto `Math` |
| 2 | 50 min | Comparação, operadores lógicos, curto-circuito, `??` e `?.`; formatação com `Intl` e datas |
| 3 | 50 min | `if`/`else if`/`else`, ternário e `switch`; Mão na massa: a inscrição decide sozinha |

## 1. Variáveis e escopo

### 1.1 O que você já sabe (e o que falta)

Na Aula 10 você aprendeu a regra prática: **declare tudo com `const`; troque para `let` só quando o valor precisar mudar; nunca use `var`**. O que ficou faltando é o motivo técnico. Ele tem um nome: **escopo** — a região do código em que um nome existe.

Existem três escopos em JavaScript:

| Escopo | Onde o nome existe | Criado por |
|---|---|---|
| Global | o arquivo inteiro (e todos os outros scripts da página) | declaração fora de qualquer bloco ou função |
| De função | dentro da função onde foi declarado | `var`, parâmetros, `const`/`let` dentro da função |
| De bloco | dentro do par de chaves `{ }` mais próximo | `const` e `let` |

Um **bloco** é qualquer par de chaves: o corpo de um `if`, de um `for`, de uma função — ou um par de chaves solto, escrito só para agrupar código.

```js
// js/exemplos-escopo.js
const nomeEvento = "Semana Acadêmica"; // escopo global: vale no arquivo todo

{
  const local = "Auditório Central";   // escopo de bloco: só existe aqui dentro
  console.log(nomeEvento);             // "Semana Acadêmica" — enxerga o de fora
  console.log(local);                  // "Auditório Central"
}

console.log(local);
// Uncaught ReferenceError: local is not defined
```

A regra é assimétrica e vale a pena guardar: **de dentro você enxerga o de fora; de fora você não enxerga o de dentro.** Um bloco é uma sala com janela: quem está dentro vê a rua, quem está na rua não vê a sala.

### 1.2 Por que `var` é um problema

`var` não respeita blocos. Ele só respeita funções. Compare:

```js
// js/exemplos-var.js
if (true) {
  var comVar = "vazou";
  let comLet = "presa";
  const comConst = "presa";
}

console.log(comVar);   // "vazou" — var ignorou as chaves do if
console.log(comLet);   // Uncaught ReferenceError: comLet is not defined
console.log(comConst); // Uncaught ReferenceError: comConst is not defined
```

A variável declarada com `var` dentro do `if` continua viva **fora** dele. Em um script de dez linhas isso parece inofensivo; em um arquivo de trezentas, é a receita para dois trechos distantes usarem o mesmo nome sem perceber e sobrescreverem os valores um do outro.

Há um segundo problema, ainda pior. `var` permite **redeclarar** o mesmo nome em silêncio:

```js
var inscritos = 87;
var inscritos = 120;  // nenhum aviso: o valor anterior simplesmente sumiu
console.log(inscritos); // 120

let vagas = 87;
let vagas = 120;
// Uncaught SyntaxError: Identifier 'vagas' has already been declared
```

Com `let`, o mesmo erro de digitação vira um erro de sintaxe que o navegador aponta antes de rodar qualquer coisa. É exatamente o que você quer: falhar cedo, com uma mensagem clara.

> **🧠 Você sabia?**
> Antes de 2015, `var` era a única forma de declarar variáveis — e o vazamento de escopo era tão incômodo que a comunidade inventou uma gambiarra famosa, a **IIFE** (*Immediately Invoked Function Expression*): embrulhar o código inteiro dentro de uma função anônima executada na hora, escrita como `(function () { })();` com o programa todo dentro das chaves, só para criar um escopo. Bibliotecas inteiras (jQuery entre elas) começam assim. Quando `let` e `const` chegaram com escopo de bloco, a IIFE perdeu o motivo de existir. Se você abrir um arquivo `.js` de dez anos atrás e encontrar esse embrulho, agora sabe o que ele está fazendo.

### 1.3 Hoisting e a zona morta temporal

Antes de executar qualquer linha, o motor JavaScript lê o arquivo inteiro e **registra** todas as declarações. Esse registro antecipado se chama **hoisting** (içamento). O que muda entre `var` e `let`/`const` é o que acontece com o nome nesse intervalo:

```js
console.log(comVar);   // undefined — o nome já existe, o valor ainda não
var comVar = 10;

console.log(comLet);
// Uncaught ReferenceError: Cannot access 'comLet' before initialization
let comLet = 10;
```

`var` é içado **e inicializado com `undefined`** — por isso a leitura não falha, ela devolve lixo. `let` e `const` são içados, mas ficam em um estado inacessível desde o começo do bloco até a linha da declaração. Esse intervalo tem nome: **zona morta temporal** (*temporal dead zone*). Tocar na variável ali dentro é um `ReferenceError` — e isso é uma boa notícia, porque um erro visível é infinitamente melhor que um `undefined` silencioso que só vai causar problema três funções adiante.

> **⚠️ Atenção**
> As duas mensagens são parecidas e significam coisas diferentes. `x is not defined` quer dizer "esse nome não existe em lugar nenhum" — geralmente um erro de digitação. `Cannot access 'x' before initialization` quer dizer "o nome existe, mas você o usou antes da linha que o declara" — mova a declaração para cima.

### 1.4 Sombreamento

Declarar, dentro de um bloco, um nome que já existe fora dele é **sombreamento** (*shadowing*). É permitido, e às vezes útil, mas confunde quem lê:

```js
const trilha = "Desenvolvimento Web";

{
  const trilha = "Segurança";   // sombreia a de fora, só dentro deste bloco
  console.log(trilha);          // "Segurança"
}

console.log(trilha);            // "Desenvolvimento Web" — intacta
```

Evite sombrear nomes importantes. Se dois valores são coisas diferentes, dê nomes diferentes: `trilhaPadrao` e `trilhaEscolhida` dizem mais do que duas variáveis chamadas `trilha`.

### 1.5 Constantes de verdade

Uma convenção que vale ouro em projetos pequenos: valores fixos do domínio ficam no topo do arquivo, em `MAIUSCULO_COM_UNDERSCORE`, e nunca aparecem "soltos" no meio do código.

```js
// js/inscricao.js — topo do arquivo
const VAGAS_TOTAIS = 120;
const LIMITE_ULTIMAS_VAGAS = 20;
const TAXA_INSCRICAO = 25;
const DESCONTO_ESTUDANTE = 0.5;
```

Um número solto no meio de uma conta (`if (restantes < 20)`) é o que se chama de **número mágico**: seis meses depois ninguém lembra de onde veio o 20, e quando o valor mudar você vai ter que caçá-lo em cinco lugares. Com a constante, você troca **uma** linha e o programa inteiro obedece — e o nome documenta a intenção.

## 2. Operadores aritméticos

### 2.1 Os sete operadores

```js
// js/exemplos-aritmetica.js
console.log(5 + 3);    // 8   — soma
console.log(5 - 3);    // 2   — subtração
console.log(5 * 3);    // 15  — multiplicação
console.log(5 / 3);    // 1.6666666666666667 — divisão (sempre com decimais)
console.log(5 % 3);    // 2   — resto da divisão inteira
console.log(5 ** 3);   // 125 — potência (5 elevado a 3)
console.log(-5);       // -5  — negação (o único operador unário da lista)
```

Duas surpresas para quem vem de outra linguagem: a divisão **nunca** trunca (`5 / 2` é `2.5`, não `2`) e não existe operador de divisão inteira. Para obter a parte inteira use `Math.trunc(5 / 2)` ou `Math.floor(5 / 2)`, da seção 3.

### 2.2 O resto (`%`) é mais útil do que parece

O operador `%` devolve o que sobra de uma divisão inteira. Ele resolve quatro problemas que aparecem o tempo todo:

```js
// 1. Par ou ímpar
console.log(10 % 2);       // 0 → par
console.log(7 % 2);        // 1 → ímpar

// 2. Múltiplo de alguma coisa (a cada 5 inscritos, um brinde)
const inscritos = 85;
console.log(inscritos % 5); // 0 → é múltiplo de 5

// 3. Ciclos: dar a volta em uma lista de 3 cores
console.log(0 % 3, 1 % 3, 2 % 3, 3 % 3, 4 % 3); // 0 1 2 0 1

// 4. Quebrar um total em unidades (segundos → minutos e segundos)
const totalSegundos = 4000;
const horas = Math.trunc(totalSegundos / 3600);          // 1
const minutos = Math.trunc((totalSegundos % 3600) / 60); // 6
const segundos = totalSegundos % 60;                      // 40
console.log(`${horas}h ${minutos}min ${segundos}s`);      // "1h 6min 40s"
```

> **💡 Dica**
> Com números negativos, `%` em JavaScript devolve o sinal do **dividendo**: `-7 % 3` é `-1`, não `2`. Se você precisa de um resto sempre positivo (para ciclos, por exemplo), use `((n % m) + m) % m`.

### 2.3 Incremento, decremento e atribuição composta

```js
let contador = 5;

contador++;          // pós-incremento: usa o valor e DEPOIS soma 1
++contador;          // pré-incremento: soma 1 e DEPOIS usa o valor
contador--;          // pós-decremento
--contador;          // pré-decremento

console.log(contador); // 5 — subiu duas vezes e desceu duas
```

A diferença entre `n++` e `++n` só aparece quando você usa o resultado da expressão no mesmo lugar:

```js
let a = 5;
console.log(a++);   // 5 — imprime, depois vira 6
console.log(a);     // 6

let b = 5;
console.log(++b);   // 6 — vira 6, depois imprime
console.log(b);     // 6
```

Na prática, use `++` sozinho em uma linha (é o caso dos laços da Aula 12) e evite combiná-lo com outra operação — código como `x = a++ + ++a` é um enigma, não um programa.

Os operadores de **atribuição composta** encurtam a forma "pegue o valor, faça uma conta, guarde de volta":

```js
let inscritos = 87;

inscritos += 3;   // igual a: inscritos = inscritos + 3   → 90
inscritos -= 5;   // 85
inscritos *= 2;   // 170
inscritos /= 4;   // 42.5
inscritos %= 10;  // 2.5
inscritos **= 2;  // 6.25

let titulo = "Semana";
titulo += " Acadêmica";   // funciona com strings: "Semana Acadêmica"
```

### 2.4 Precedência: quem faz a conta primeiro

Toda expressão com mais de um operador segue uma ordem, do mais "forte" para o mais "fraco". Esta é a parte da tabela que importa no Nível 1:

| Nível | Operadores | Sentido de avaliação |
|---|---|---|
| 1 (mais forte) | `( )`, `.`, `[ ]`, chamada de função | da esquerda para a direita |
| 2 | `!`, `-` unário, `++`, `--`, `typeof` | da direita para a esquerda |
| 3 | `**` | da direita para a esquerda |
| 4 | `*`, `/`, `%` | da esquerda para a direita |
| 5 | `+`, `-` | da esquerda para a direita |
| 6 | `<`, `<=`, `>`, `>=` | da esquerda para a direita |
| 7 | `===`, `!==`, `==`, `!=` | da esquerda para a direita |
| 8 | `&&` | da esquerda para a direita |
| 9 | `\|\|`, `??` | da esquerda para a direita |
| 10 (mais fraco) | `? :`, `=`, `+=`, `-=` | da direita para a esquerda |

```js
console.log(2 + 3 * 4);        // 14 — a multiplicação vem antes
console.log((2 + 3) * 4);      // 20 — o parêntese muda tudo
console.log(2 ** 3 ** 2);      // 512 — ** é da direita para a esquerda: 2 ** (3 ** 2)
console.log((-2) ** 2);        // 4 — o parêntese é obrigatório aqui (veja abaixo)
console.log(10 - 4 - 3);       // 3 — da esquerda para a direita: (10 - 4) - 3
console.log(1 + 2 + "3");      // "33" — soma numérica primeiro, depois concatena
```

Escrever `-2 ** 2` sem parênteses é `Uncaught SyntaxError: Unary operator used immediately before exponentiation expression`. A linguagem se recusa a adivinhar se você quis `(-2) ** 2` (que dá 4) ou `-(2 ** 2)` (que dá −4) — e faz bem.

> **💡 Dica**
> Não decore a tabela: **use parênteses**. Ninguém nunca perdeu tempo lendo uma expressão com parênteses demais; muita gente já perdeu uma tarde caçando um bug em uma expressão com parênteses de menos. Escreva `(a + b) / 2`, não `a + b / 2`.

### 2.5 Onde a aritmética quebra

Você viu na Aula 10 que `0.1 + 0.2` dá `0.30000000000000004`. A causa é a representação binária: números decimais como `0,1` viram dízimas periódicas em base 2, exatamente como `1/3` vira `0,333…` em base 10. Como o padrão IEEE 754 guarda 53 bits de precisão, a dízima é cortada — e o erro aparece na décima sétima casa.

```js
console.log(0.1 + 0.2);                    // 0.30000000000000004
console.log(0.1 + 0.2 === 0.3);            // false
console.log(1.005 * 100);                   // 100.49999999999999
console.log((1.005).toFixed(2));             // "1.00" — e não "1.01"

// Comparando decimais com segurança: a diferença é desprezível?
console.log(Math.abs(0.1 + 0.2 - 0.3) < Number.EPSILON); // true
```

`Number.EPSILON` é a menor diferença representável entre 1 e o próximo número — aproximadamente `2,22 × 10⁻¹⁶`. A regra prática: **nunca compare decimais com `===`**; compare a diferença absoluta com uma tolerância. E, para dinheiro, faça o que os bancos fazem: guarde **centavos inteiros** e divida por 100 só na hora de exibir.

Outro ponto de atenção é o que acontece quando um valor não numérico entra na conta:

```js
console.log("120" - 87);        // 33 — o - converte a string
console.log("120" + 87);        // "12087" — o + concatena
console.log(Number("120") + 87); // 207 — a forma correta
console.log(undefined + 1);      // NaN
console.log(0 / 0);              // NaN
console.log(Number.isNaN(0 / 0)); // true
```

Todo valor vindo de um formulário chega como **string**. Converta com `Number()` antes de qualquer conta — é o erro número um dos primeiros scripts, e você vai reencontrá-lo na Aula 14.

> **🔬 Investigue**
> Abra o Console e digite `0.1 + 0.2` — o resultado com o erro na ponta aparece. Agora digite `(0.1).toString(2)`: você vê a representação binária de 0,1, uma dízima periódica com `0011` se repetindo. Compare com `(0.5).toString(2)`, que dá `0.1` exato — porque 0,5 é uma potência de 2. Por fim, teste `0.1 + 0.2 === 0.3` e `Math.abs(0.1 + 0.2 - 0.3) < Number.EPSILON`. Você acabou de ver, em três linhas, por que sistemas financeiros não usam ponto flutuante.

## 3. O objeto `Math`

`Math` é um objeto embutido com constantes e operações matemáticas. Você não cria um `Math`; ele já existe e você usa direto.

### 3.1 Arredondamento

```js
console.log(Math.round(4.5));    // 5  — meio para cima
console.log(Math.round(4.4));    // 4
console.log(Math.round(-4.5));   // -4 — atenção: "para cima" é em direção ao +infinito
console.log(Math.floor(4.9));    // 4  — sempre para baixo
console.log(Math.ceil(4.1));     // 5  — sempre para cima
console.log(Math.trunc(4.9));    // 4  — corta a parte decimal, sem arredondar
console.log(Math.trunc(-4.9));   // -4 — floor daria -5
```

Escolha pelo significado: para **quantas páginas** cabem 47 itens de 10 em 10, `Math.ceil` (5, porque a quinta página existe mesmo com 7 itens). Para **quantos brindes completos** dá para montar, `Math.floor`. Para exibir uma média, `toFixed(1)` — lembrando que ele devolve **string**.

### 3.2 O resto do arsenal

```js
console.log(Math.abs(-15));          // 15  — valor absoluto
console.log(Math.max(3, 9, 1));      // 9
console.log(Math.min(3, 9, 1));      // 1
console.log(Math.pow(2, 10));        // 1024 — o mesmo que 2 ** 10
console.log(Math.sqrt(144));         // 12
console.log(Math.cbrt(27));          // 3
console.log(Math.sign(-8));          // -1  — -1, 0 ou 1
console.log(Math.hypot(3, 4));       // 5   — raiz de (3² + 4²)
console.log(Math.PI);                // 3.141592653589793
console.log(Math.random());          // número entre 0 (incluso) e 1 (excluso)
```

`Math.max` e `Math.min` recebem números soltos, não um array — para o array você vai usar `Math.max(...numeros)` com o operador spread da Aula 12.

### 3.3 Sorteio: a receita que você vai usar sempre

```js
// Um inteiro entre 0 e 9
const sorteioSimples = Math.floor(Math.random() * 10);

// Um inteiro entre minimo e maximo, ambos inclusos
const minimo = 1;
const maximo = 6;
const dado = Math.floor(Math.random() * (maximo - minimo + 1)) + minimo;

console.log("Dado:", dado);
```

Leia a fórmula de dentro para fora: `Math.random()` dá algo como `0,7314`; multiplicar por `(maximo - minimo + 1)` espalha o valor pela faixa; `Math.floor` corta para o inteiro de baixo; somar `minimo` desloca a faixa para o início certo. O `+ 1` é o que inclui o `maximo` no sorteio — sem ele, o 6 nunca sai.

Limitar um valor a uma faixa (*clamp*) é outro padrão comum, e sai de graça combinando `min` e `max`:

```js
const percentual = 137;
const percentualValido = Math.min(100, Math.max(0, percentual)); // 100
```

## 4. Comparação

### 4.1 Relacionais e igualdade

```js
console.log(10 > 9);       // true
console.log(10 >= 10);     // true
console.log(10 < 9);       // false
console.log(10 <= 9);      // false

console.log(10 === 10);    // true  — mesmo valor E mesmo tipo
console.log(10 !== "10");  // true  — tipos diferentes
```

Você já sabe da Aula 10 que `==` converte os tipos antes de comparar e produz resultados absurdos (`0 == ""` é `true`, `"" == "0"` é `false`). A regra desta disciplina é definitiva: **`===` e `!==`, sempre**. Se um dos lados chegou como texto, converta explicitamente (`Number(entrada) === 5`) em vez de relaxar a comparação.

### 4.2 Comparar strings compara letra por letra

```js
console.log("a" < "b");        // true  — ordem dos códigos Unicode
console.log("Z" < "a");        // true  — maiúsculas vêm antes das minúsculas
console.log("10" < "9");       // true  — comparação de TEXTO: "1" vem antes de "9"
console.log(10 < 9);           // false — comparação de NÚMEROS
console.log("Ana" < "Álvaro"); // true  — "A" (código 65) vem antes de "Á" (código 193)
```

As três últimas linhas são armadilhas clássicas. Comparar strings com `<` compara **códigos Unicode**, não ordem alfabética do português: todas as letras acentuadas ficam depois de todas as não acentuadas, então uma lista ordenada assim joga "Álvaro" para o fim, depois de "Zuleide". Para ordenar nomes em português, use `localeCompare`, que conhece as regras do idioma:

```js
console.log("Ana".localeCompare("Álvaro", "pt-BR")); // 1  → "Ana" vem DEPOIS de "Álvaro"
console.log("ana".localeCompare("Ana", "pt-BR"));    // -1 → minúscula antes, sem virar outra letra
```

Repare no resultado oposto: para o operador `<`, "Ana" vem antes; para o português, "Álvaro" vem antes, porque o acento não muda a letra.

`localeCompare` devolve um número negativo, zero ou positivo — exatamente o que a função de ordenação de arrays espera, como você verá na Aula 12.

> **📌 Na prova**
> Três resultados costumam cair: `"10" < "9"` é `true` (comparação textual), `NaN === NaN` é `false` (o único valor diferente de si mesmo) e `0.1 + 0.2 === 0.3` é `false` (ponto flutuante). Saiba explicar cada um em uma frase.

## 5. Operadores lógicos

### 5.1 `&&`, `||` e `!`

```js
const temVaga = true;
const inscricoesAbertas = false;

console.log(temVaga && inscricoesAbertas); // false — E: só é true se AMBOS forem true
console.log(temVaga || inscricoesAbertas); // true  — OU: é true se ALGUM for true
console.log(!temVaga);                     // false — NÃO: inverte
```

| Expressão | `&&` (E) | `\|\|` (OU) |
|---|---|---|
| `true` com `true` | `true` | `true` |
| `true` com `false` | `false` | `true` |
| `false` com `true` | `false` | `true` |
| `false` com `false` | `false` | `false` |

### 5.2 Curto-circuito: o que eles realmente devolvem

Aqui está a parte que quase ninguém aprende no primeiro contato. `&&` e `||` **não devolvem `true` ou `false`** — eles devolvem **um dos operandos**, e param de avaliar assim que o resultado está decidido. Isso se chama **curto-circuito**.

```js
console.log(true && "texto");     // "texto" — o E precisa checar o segundo; devolve ele
console.log(false && "texto");    // false   — decidido no primeiro; o segundo nem é lido
console.log("primeiro" || "segundo"); // "primeiro" — o OU para no primeiro truthy
console.log("" || "padrão");      // "padrão"  — "" é falsy, então segue adiante
console.log(0 || 100);            // 100
console.log(null && "nunca lido"); // null
```

Regra em uma frase: `&&` devolve o **primeiro valor falsy** que encontrar (ou o último, se todos forem truthy); `||` devolve o **primeiro valor truthy** (ou o último, se todos forem falsy).

Isso permite dois padrões que você vai ver em todo código JavaScript moderno:

```js
// Valor padrão quando a variável está vazia
const corEscolhida = "";
const cor = corEscolhida || "azul";   // "azul"

// Executar algo apenas se a condição for verdadeira
const modoDebug = true;
modoDebug && console.log("Modo de depuração ligado");
```

O segundo padrão é engenhoso, mas prefira um `if` de verdade: ele diz a intenção sem exigir que quem lê conheça o truque.

### 5.3 `??` — o padrão que respeita o zero

O `||` tem um defeito grave: ele considera `0` e `""` valores "vazios", porque são falsy. Em um formulário, isso corrompe dados legítimos.

```js
const inscritos = 0;

console.log(inscritos || 87);  // 87 — ERRADO: zero inscritos é um dado válido!
console.log(inscritos ?? 87);  // 0  — CERTO
```

O operador `??` (*nullish coalescing*, coalescência nula) só usa o valor da direita quando o da esquerda é `null` ou `undefined`. Todo o resto — inclusive `0`, `""` e `false` — passa direto.

| Valor da esquerda | `\|\| "padrão"` | `?? "padrão"` |
|---|---|---|
| `undefined` | `"padrão"` | `"padrão"` |
| `null` | `"padrão"` | `"padrão"` |
| `0` | `"padrão"` | `0` |
| `""` | `"padrão"` | `""` |
| `false` | `"padrão"` | `false` |

Existe também a atribuição `??=`, que só escreve se o valor atual for nulo:

```js
let comentario = null;
comentario ??= "Sem observações";
console.log(comentario); // "Sem observações"
```

> **⚠️ Atenção**
> Misturar `??` com `&&` ou `||` na mesma expressão, sem parênteses, é um `SyntaxError` proposital da linguagem: `a || b ?? c` não compila. Os projetistas preferiram obrigar você a escrever `(a || b) ?? c` a deixar a ambiguidade passar. É uma das poucas vezes em que JavaScript é rígido — aproveite.

### 5.4 `?.` — encadeamento opcional

Quando você lê uma propriedade de algo que pode não existir, o erro é fatal:

```js
const inscricao = { nome: "Maria", contato: { email: "maria@exemplo.br" } };
const vazia = {};

console.log(inscricao.contato.email);  // "maria@exemplo.br"
console.log(vazia.contato.email);
// Uncaught TypeError: Cannot read properties of undefined (reading 'email')
```

O operador `?.` interrompe a leitura e devolve `undefined` em vez de quebrar:

```js
console.log(vazia.contato?.email);        // undefined — nenhum erro
console.log(vazia.contato?.email ?? "não informado"); // "não informado"
```

Ele funciona em três formas: `objeto?.propriedade`, `objeto?.[chave]` e `funcao?.()`. A combinação `?.` com `??` é o par mais útil do JavaScript moderno: "leia com segurança e, se não houver nada, use este padrão".

> **💡 Dica**
> Não espalhe `?.` por todo lado. Use onde o valor **pode legitimamente não existir** (um campo opcional, um elemento que só existe em uma página). Se o valor deveria existir e não existe, você quer o erro — ele está te avisando de um bug de verdade, e o `?.` só o esconderia.

## 6. Formatando números e datas para o Brasil

O JavaScript nasceu nos Estados Unidos, e por isso `(1234.5).toString()` devolve `"1234.5"` — ponto decimal, sem separador de milhar. Mostrar isso para um usuário brasileiro é um erro de produto. A solução padrão é a família `Intl`.

### 6.1 `Intl.NumberFormat`

```js
// js/exemplos-formatacao.js
const formatarReal = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

console.log(formatarReal.format(25));       // "R$ 25,00"
console.log(formatarReal.format(1234.5));   // "R$ 1.234,50"
console.log(formatarReal.format(0));        // "R$ 0,00"

const formatarPercentual = new Intl.NumberFormat("pt-BR", {
  style: "percent",
  maximumFractionDigits: 1,
});

console.log(formatarPercentual.format(0.725)); // "72,5%" — recebe a FRAÇÃO, não 72.5

const formatarInteiro = new Intl.NumberFormat("pt-BR");
console.log(formatarInteiro.format(1200000));  // "1.200.000"
```

Repare que `style: "percent"` espera a fração (`0.725`), não o número já multiplicado. É um erro comum mostrar "72500%" na tela por causa disso.

Existe também o atalho `toLocaleString`, que faz o mesmo sem guardar o formatador:

```js
console.log((1234.5).toLocaleString("pt-BR", { style: "currency", currency: "BRL" }));
// "R$ 1.234,50"
```

Quando o mesmo formato é usado muitas vezes, criar o `Intl.NumberFormat` uma vez e reaproveitar é mais rápido.

### 6.2 Datas com `Date`

Um objeto `Date` guarda um instante como a quantidade de milissegundos desde 1º de janeiro de 1970, UTC — a chamada *época Unix*.

```js
const agora = new Date();

console.log(agora.getFullYear());   // o ano, com quatro dígitos
console.log(agora.getMonth());      // 0 a 11 — janeiro é 0! (armadilha clássica)
console.log(agora.getDate());       // o dia do mês, 1 a 31
console.log(agora.getDay());        // o dia da semana, 0 (domingo) a 6 (sábado)
console.log(agora.getHours());      // a hora, 0 a 23
console.log(agora.getTime());       // milissegundos desde a época Unix
```

Para exibir, use os métodos `toLocale*`, que respeitam o idioma:

```js
const agora = new Date();

console.log(agora.toLocaleDateString("pt-BR"));  // dia/mês/ano
console.log(agora.toLocaleTimeString("pt-BR"));  // hora:minuto:segundo

console.log(agora.toLocaleDateString("pt-BR", {
  weekday: "long",
  day: "2-digit",
  month: "long",
}));
// algo como "segunda-feira, 05 de maio"
```

Subtrair duas datas devolve a diferença em **milissegundos** — porque o operador `-` converte cada objeto em número, exatamente a coerção que você estudou na Aula 10:

```js
const MS_POR_DIA = 1000 * 60 * 60 * 24;

const agora = new Date();
const daquiUmaSemana = new Date();
daquiUmaSemana.setDate(agora.getDate() + 7);

const diferenca = daquiUmaSemana - agora;             // número, em milissegundos
console.log(Math.round(diferenca / MS_POR_DIA));      // 7
```

`setDate` aceita valores fora da faixa e ajusta o mês sozinho: se hoje é dia 28 e você soma 7, o objeto vira dia 4 do mês seguinte, sem que você precise saber quantos dias tem o mês. É a forma segura de fazer contas com calendário.

> **🧠 Você sabia?**
> O `getMonth()` devolver 0 para janeiro não é um capricho: a API de datas do JavaScript foi copiada, em 1995 e às pressas, da classe `java.util.Date` do Java, que já tinha essa numeração. O erro se espalhou para milhões de linhas de código e nunca pôde ser corrigido. O comitê da linguagem trabalha desde então em uma substituta completa, a API `Temporal`, com meses de 1 a 12 e objetos imutáveis. Enquanto ela não chega a todos os navegadores, some 1 ao `getMonth()` — e prefira `toLocaleDateString` para exibir.

## 7. Estruturas condicionais

Até agora todo script que você escreveu executava de cima para baixo, sem desvios. A **estrutura condicional** é o que permite ao programa escolher um caminho.

### 7.1 `if`, `else if`, `else`

```js
// js/exemplos-condicionais.js
const nota = 7.5;

if (nota >= 6) {
  console.log("Aprovado");
} else if (nota >= 4) {
  console.log("Exame final");
} else {
  console.log("Reprovado");
}
```

Três regras que evitam a maior parte dos erros:

1. **A condição é convertida para booleano.** Qualquer valor serve; os oito falsy da Aula 10 (`false`, `0`, `-0`, `0n`, `""`, `null`, `undefined`, `NaN`) levam ao `else`, todo o resto entra no `if`.
2. **A ordem importa.** Os testes são avaliados de cima para baixo e o primeiro verdadeiro vence — os demais nem são lidos. Se você escrever `if (nota >= 4)` antes de `if (nota >= 6)`, ninguém nunca será aprovado.
3. **Use sempre as chaves.** JavaScript permite omiti-las quando há uma instrução só, e essa permissão já causou falhas de segurança famosas:

```js
const temVaga = false;

if (temVaga)
  console.log("Inscrição liberada");
  console.log("Enviando e-mail de confirmação"); // SEMPRE executa: não está no if!
```

O recuo engana o olho; o interpretador só enxerga a primeira linha como corpo do `if`. Com chaves, o problema não existe.

### 7.2 Condições compostas

```js
const vagasRestantes = 12;
const inscricoesAbertas = true;
const idade = 17;

if (inscricoesAbertas && vagasRestantes > 0) {
  console.log("Pode se inscrever");
}

if (idade < 18 || idade >= 65) {
  console.log("Precisa de autorização ou tem gratuidade");
}

// Erro clássico: JavaScript não entende "entre"
// if (0 < vagasRestantes < 20) — não faça isso
if (vagasRestantes > 0 && vagasRestantes < 20) {
  console.log("Últimas vagas");
}
```

Por que `0 < vagasRestantes < 20` não funciona? Porque a avaliação é da esquerda para a direita: `0 < 12` dá `true`, e então `true < 20` compara `1 < 20`, que também dá `true` — mesmo se `vagasRestantes` fosse 500. A condição parece certa e está sempre certa, que é o pior tipo de bug.

### 7.3 O operador ternário

Para escolher **um valor** entre dois, o ternário é mais direto que um `if`:

```js
const nota = 7.5;

const situacao = nota >= 6 ? "Aprovado" : "Reprovado";
console.log(situacao);

// Muito usado dentro de template literals
const vagas = 3;
console.log(`Restam ${vagas} ${vagas === 1 ? "vaga" : "vagas"}.`);
```

Leia `condicao ? valorSeVerdadeiro : valorSeFalso` como uma pergunta: "a condição é verdadeira? então isto; senão, aquilo".

Ternários podem ser encadeados, e aí a legibilidade depende da formatação:

```js
const ocupacao = 82;

const status =
  ocupacao >= 100 ? "esgotado"
  : ocupacao >= 80 ? "últimas vagas"
  : ocupacao >= 50 ? "enchendo"
  : "vagas à vontade";

console.log(status); // "últimas vagas"
```

Escrito assim, em uma coluna, o encadeamento vira quase uma tabela e continua legível. Escrito em uma linha só, vira um enigma. **Regra:** ternário para escolher um valor; `if` para executar blocos de instruções. Se você precisa fazer três coisas dentro de um ramo, o ternário é a ferramenta errada.

### 7.4 `switch`

Quando a decisão é sobre **um único valor comparado com várias possibilidades exatas**, o `switch` é mais claro que uma escada de `else if`:

```js
const trilha = "web";

switch (trilha) {
  case "web":
    console.log("Laboratório 1 — Desenvolvimento Web");
    break;
  case "dados":
    console.log("Laboratório 2 — Ciência de Dados");
    break;
  case "seguranca":
    console.log("Sala 105 — Segurança");
    break;
  default:
    console.log("Local a definir");
}
```

Quatro pontos essenciais:

- A comparação de cada `case` é **estrita** (`===`). `case "3"` não casa com o número `3`.
- **`break` encerra o `switch`.** Sem ele, a execução "vaza" para os casos seguintes e executa tudo até encontrar um `break` ou o fim do bloco.
- `default` é o "senão" — pode ficar em qualquer posição, mas por convenção vai no fim.
- O vazamento pode ser **intencional**: casos empilhados sem corpo compartilham o mesmo bloco.

```js
const diaDaSemana = 6;

switch (diaDaSemana) {
  case 0:
  case 6:
    console.log("Fim de semana — campus fechado");
    break;
  case 1:
  case 2:
  case 3:
  case 4:
  case 5:
    console.log("Dia útil — evento das 19h às 22h");
    break;
  default:
    console.log("Dia inválido");
}
```

Um detalhe de escopo: as chaves do `switch` formam **um único bloco**, então declarar `const` dentro de um `case` afeta todos os outros. Se precisar de variáveis locais em um caso, embrulhe o corpo dele em chaves próprias:

```js
const tipo = "minicurso";

switch (tipo) {
  case "minicurso": {
    const duracao = 4;
    console.log(`Minicurso de ${duracao} horas`);
    break;
  }
  case "palestra": {
    const duracao = 1;
    console.log(`Palestra de ${duracao} hora`);
    break;
  }
  default:
    console.log("Tipo desconhecido");
}
```

### 7.5 Qual usar?

| Situação | Ferramenta |
|---|---|
| Escolher **um valor** entre duas opções | ternário |
| Executar **blocos diferentes** conforme faixas ou condições compostas | `if` / `else if` / `else` |
| Comparar **um valor** com várias possibilidades exatas | `switch` |
| Interromper cedo quando algo não faz sentido | `if` no topo, com aviso no console |

> **🔬 Investigue**
> Cole no Console o `switch` do dia da semana acima, mas **apague todos os `break`**. Rode com `diaDaSemana = 0` e observe: as três mensagens aparecem, uma atrás da outra, porque a execução vazou por todos os casos. Agora coloque o `break` só no primeiro caso e rode de novo com `diaDaSemana = 1`. Você acabou de reproduzir, de propósito, o bug mais difícil de enxergar em `switch` — e vai reconhecê-lo em um segundo quando ele acontecer sem querer.

## 💻 Mão na massa — A página de inscrição decide sozinha

Hoje o site da **Semana Acadêmica de Sistemas de Informação** ganha três comportamentos novos: o aviso automático de "Últimas vagas!", a taxa de inscrição formatada em reais e uma contagem regressiva na página inicial. Tudo com o que você acabou de aprender — nenhuma linha nova de manipulação da página além do `textContent` que você já usa desde a Aula 10.

### Passo 1 — o parágrafo de aviso na página de inscrição

Abra `inscricao.html` e acrescente, logo abaixo da seção de vagas criada na Aula 10, um parágrafo vazio para o aviso e a linha da taxa.

**`site-evento/inscricao.html`** — trecho dentro do `<main>`, antes do formulário

```html
<section class="vagas" aria-live="polite">
  <h2>Vagas</h2>
  <p>
    Restam <strong id="vagas-restantes">—</strong> de
    <span id="vagas-totais">—</span> vagas
    (<span id="percentual-ocupacao">—</span>% ocupadas).
  </p>

  <p id="aviso-vagas" class="aviso" role="status"></p>

  <p class="taxa">
    Taxa de inscrição: <strong id="valor-taxa">—</strong>
    <span id="observacao-taxa"></span>
  </p>
</section>
```

O parágrafo `#aviso-vagas` nasce **vazio**. Quando o script não tiver nada a dizer, ele continua vazio — e o CSS do Passo 6 esconde parágrafos vazios, então nada aparece na tela. O `role="status"` faz leitores de tela anunciarem a mensagem quando ela surgir, sem interromper o que o usuário está fazendo.

### Passo 2 — as constantes e o cálculo

Substitua o conteúdo de `js/inscricao.js` pelo arquivo abaixo. As cinco declarações do topo são a única parte que a organização do evento precisa editar durante a semana — todo o resto se ajusta sozinho.

**`site-evento/js/inscricao.js`**

```js
// inscricao.js — carregado apenas por inscricao.html

// ===== CONSTANTES DO EVENTO =====
const VAGAS_TOTAIS = 120;
const LIMITE_ULTIMAS_VAGAS = 20;   // a partir daqui, o aviso aparece
const TAXA_INSCRICAO = 25;         // em reais
const DESCONTO_ESTUDANTE = 0.5;    // 50%

let inscritos = 87;                // let: muda quando o formulário funcionar (Aula 14)

// ===== CÁLCULOS =====
// Math.max evita número negativo se alguém digitar mais inscritos que vagas
const vagasRestantes = Math.max(0, VAGAS_TOTAIS - inscritos);
const fracaoOcupada = inscritos / VAGAS_TOTAIS;
const percentualOcupacao = Math.min(100, fracaoOcupada * 100);
const taxaComDesconto = TAXA_INSCRICAO * (1 - DESCONTO_ESTUDANTE);

console.group("Vagas");
console.log("Totais:", VAGAS_TOTAIS);
console.log("Inscritos:", inscritos);
console.log("Restantes:", vagasRestantes);
console.log("Ocupação:", percentualOcupacao.toFixed(1), "%");
console.groupEnd();
```

`Math.max(0, …)` e `Math.min(100, …)` são a defesa contra dados inconsistentes: mesmo que alguém digite 130 inscritos, a página mostra 0 vagas e 100% de ocupação, em vez de "-10 vagas (108,3% ocupadas)".

### Passo 3 — a decisão: qual aviso mostrar

Continue o mesmo arquivo. Esta é a parte que **decide**.

**`site-evento/js/inscricao.js`** — continuação

```js
// ===== DECISÃO: qual mensagem o visitante deve ver =====
let mensagem = "";
let situacao = "";

if (vagasRestantes === 0) {
  situacao = "esgotado";
  mensagem = "Inscrições encerradas — todas as vagas foram preenchidas.";
} else if (vagasRestantes <= 5) {
  situacao = "critico";
  mensagem = `Corra! Restam apenas ${vagasRestantes} ${vagasRestantes === 1 ? "vaga" : "vagas"}.`;
} else if (vagasRestantes <= LIMITE_ULTIMAS_VAGAS) {
  situacao = "alerta";
  mensagem = `Últimas vagas! Menos de ${LIMITE_ULTIMAS_VAGAS} lugares disponíveis.`;
} else {
  situacao = "tranquilo";
  mensagem = "";
}

console.log("Situação:", situacao);

// ===== ESCRITA NA PÁGINA =====
document.querySelector("#vagas-restantes").textContent = vagasRestantes;
document.querySelector("#vagas-totais").textContent = VAGAS_TOTAIS;
document.querySelector("#percentual-ocupacao").textContent = percentualOcupacao.toFixed(1);
document.querySelector("#aviso-vagas").textContent = mensagem;
```

Repare na ordem dos testes: do caso mais restrito (`=== 0`) para o mais amplo (`<= LIMITE_ULTIMAS_VAGAS`). Se você invertesse as duas últimas condições, a mensagem "Corra!" nunca apareceria — porque `vagasRestantes <= 20` também é verdadeira quando restam 3 vagas, e o primeiro teste verdadeiro vence.

O ternário dentro do template literal resolve o singular e o plural. Essa concordância é o tipo de detalhe que separa uma página feita com capricho de uma que mostra "Restam 1 vagas".

### Passo 4 — a taxa formatada em reais

**`site-evento/js/inscricao.js`** — continuação

```js
// ===== FORMATAÇÃO EM REAIS =====
const formatarReal = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

// Estudantes da UNEMAT pagam metade; o aviso só aparece se houver desconto
const temDesconto = DESCONTO_ESTUDANTE > 0;

document.querySelector("#valor-taxa").textContent = formatarReal.format(TAXA_INSCRICAO);
document.querySelector("#observacao-taxa").textContent = temDesconto
  ? `(estudantes da UNEMAT: ${formatarReal.format(taxaComDesconto)})`
  : "";

console.log("Taxa cheia:", formatarReal.format(TAXA_INSCRICAO));
console.log("Taxa com desconto:", formatarReal.format(taxaComDesconto));
```

### Passo 5 — a contagem regressiva na página inicial

A contagem vive em `js/app.js`, que é carregado pelas **cinco** páginas. Só que o elemento da contagem existe apenas em `index.html` — nas outras páginas `querySelector` devolverá `null`, e tentar escrever em `null` derruba o script inteiro com `Cannot read properties of null`. A solução é um `if`: só escreve se o elemento existir.

**`site-evento/index.html`** — trecho dentro do herói do `<main>`

```html
<p class="contagem" id="contagem-regressiva" role="status">Calculando…</p>
```

**`site-evento/js/app.js`** — acrescente ao fim do arquivo criado na Aula 10

```js
// ===== CONTAGEM REGRESSIVA PARA A ABERTURA =====
// A data do evento é calculada a partir de hoje, para que o exemplo nunca
// fique no passado. No seu projeto autoral, troque o cálculo abaixo pela
// data real do seu evento: new Date(ano, mes - 1, dia) — lembre do mes - 1.
const DIAS_ATE_A_ABERTURA = 45;
const HORA_DE_ABERTURA = 19;
const MS_POR_DIA = 1000 * 60 * 60 * 24;

// Meia-noite de hoje: queremos contar dias de CALENDÁRIO, não horas corridas
const inicioDeHoje = new Date();
inicioDeHoje.setHours(0, 0, 0, 0);

// new Date(outraData) cria uma cópia; sem isso, alterar uma alteraria a outra
const dataDoEvento = new Date(inicioDeHoje);
dataDoEvento.setDate(inicioDeHoje.getDate() + DIAS_ATE_A_ABERTURA);

// Math.round, não Math.ceil: no dia em que o horário de verão muda, um "dia"
// tem 23 ou 25 horas, e a divisão dá 44,96 ou 45,04 — o round acerta os dois
const diasRestantes = Math.round((dataDoEvento - inicioDeHoje) / MS_POR_DIA);

const dataFormatada = dataDoEvento.toLocaleDateString("pt-BR", {
  weekday: "long",
  day: "2-digit",
  month: "long",
});

let textoContagem = "";

if (diasRestantes > 1) {
  textoContagem = `Faltam ${diasRestantes} dias — abertura ${dataFormatada}, às ${HORA_DE_ABERTURA}h.`;
} else if (diasRestantes === 1) {
  textoContagem = `É amanhã! Abertura ${dataFormatada}, às ${HORA_DE_ABERTURA}h.`;
} else if (diasRestantes === 0) {
  textoContagem = `É hoje! Abertura às ${HORA_DE_ABERTURA}h.`;
} else {
  textoContagem = "Esta edição já aconteceu. Obrigado a quem participou!";
}

// O elemento só existe em index.html — nas outras páginas, querySelector devolve null
const elementoContagem = document.querySelector("#contagem-regressiva");

if (elementoContagem !== null) {
  elementoContagem.textContent = textoContagem;
}

console.log("Dias restantes:", diasRestantes);
```

Esse `if` no fim é a lição prática da aula: um script compartilhado por várias páginas **precisa** verificar se o elemento existe antes de tocá-lo. Você poderia escrever a mesma verificação com curto-circuito (`elementoContagem && (elementoContagem.textContent = textoContagem)`), mas o `if` explícito é mais fácil de ler — e legibilidade vale mais que economia de caracteres.

### Passo 6 — o estilo do aviso

**`site-evento/css/estilo.css`** — acrescente na seção de componentes

```css
/* ===== Aviso de vagas (Aula 11) ===== */
.aviso {
  margin-top: var(--espaco-pequeno);
  padding: var(--espaco-pequeno) var(--espaco-medio);
  border-left: 4px solid #b42318;
  border-radius: var(--raio-borda);
  background: #fdf2f2;
  color: #8a1b12;
  font-weight: 600;
}

/* Se o script não escreveu nada, o parágrafo some da tela */
.aviso:empty {
  display: none;
}

.taxa {
  margin-top: var(--espaco-medio);
}

.contagem {
  display: inline-block;
  padding: var(--espaco-pequeno) var(--espaco-medio);
  border-radius: 999px;
  background: var(--cor-primaria);
  color: #fff;
  font-weight: 600;
}
```

A pseudoclasse `:empty` casa com elementos que não têm **nenhum** filho, nem texto. É a forma mais limpa de esconder um aviso que ainda não tem conteúdo, sem precisar de JavaScript para mexer em classes — isso fica para a Aula 13.

Use os nomes de variáveis do **seu** sistema de design da Aula 06; os acima seguem os da Mão na massa da Aula 07.

### Como testar

1. Abra `inscricao.html` no Live Server com `inscritos = 87`. A página mostra **33** de **120** vagas, **72.5**% de ocupação, taxa **R$ 25,00** com observação de **R$ 12,50** — e **nenhum** aviso (33 é maior que o limite de 20).
2. Troque para `inscritos = 105`, salve e recarregue: aparece a faixa vermelha com "Últimas vagas! Menos de 20 lugares disponíveis."
3. Troque para `inscritos = 119`: a mensagem vira "Corra! Restam apenas 1 vaga." — no singular.
4. Troque para `inscritos = 130`: a página mostra 0 vagas, 100.0% e "Inscrições encerradas". Nenhum número negativo aparece. Volte para `87`.
5. Abra `index.html`: o balão azul mostra "Faltam 45 dias — abertura …, às 19h.", com o dia da semana e o mês por extenso em português.
6. Abra `contato.html` e olhe o Console: a linha "Dias restantes: 45" aparece e **nenhum** erro vermelho — porque o `if` protegeu o script na página que não tem o elemento da contagem.
7. Comente o `if` (deixando só a atribuição) e recarregue `contato.html`: aparece `Uncaught TypeError: Cannot read properties of null (reading 'textContent')`. Desfaça.

Resultado esperado: a página de inscrição muda de comportamento sozinha ao trocar um único número, e a página inicial mostra a contagem sem que ninguém precise editar o HTML.

## 🧪 Laboratório

Alguns exercícios do Nível B pedem **funções**. A sintaxe completa é assunto da Aula 13; por ora, use o mesmo esqueleto da Aula 10:

```js
function nomeDaFuncao(parametro) {
  const resultado = parametro * 2;
  return resultado;
}

console.log(nomeDaFuncao(10)); // 20
```

### Nível A — Fixação

**A1.** Diferencie `let`, `const` e `var` quanto a três critérios: escopo, reatribuição e redeclaração. Escreva um exemplo curto de cada diferença.

**A2.** Por que `const lista = [1, 2]; lista.push(3);` funciona, mas `lista = [3]` produz `Uncaught TypeError: Assignment to constant variable.`? Explique com suas palavras o que exatamente `const` congela.

**A3.** Explique escopo de bloco com um exemplo que produza `Uncaught ReferenceError: x is not defined`. Depois altere o exemplo para produzir `Uncaught ReferenceError: Cannot access 'x' before initialization` e explique a diferença entre as duas mensagens.

**A4.** Escreva um ternário que atribua `"Par"` ou `"Ímpar"` a uma variável `paridade`, conforme o valor de `n`. Teste com `n = 0`, `n = 7` e `n = -4`.

**A5.** Qual a diferença entre `||` e `??`? Dê um caso concreto do site do evento em que os dois produzem resultados diferentes, e diga qual é o correto.

**A6.** Qual o resultado de `0.1 + 0.2 === 0.3`? Explique a causa e escreva a forma correta de comparar esses dois valores.

**A7.** Qual a diferença entre `%` e `/`? Escreva a expressão que verifica se um número é par e a que descobre quantas horas completas há em 7300 segundos.

**A8.** Diferencie `++i` de `i++` com um exemplo em que os dois produzem saídas diferentes no `console.log`.

**A9.** Escreva a condicional encadeada que converte uma média em conceito: `>= 9` vira A, `>= 7` vira B, `>= 6` vira C, o resto vira D. Depois reescreva com ternário encadeado e diga qual das duas versões você prefere e por quê.

**A10.** Quando `switch` é preferível a uma escada de `else if`? Por que o `break` é praticamente obrigatório, e em que situação omiti-lo é intencional?

**A11.** Anote sua previsão para cada linha e só depois teste no Console:

```js
console.log(2 + 3 * 4);
console.log("10" < "9");
console.log(10 < 9);
console.log(0 || "padrão");
console.log(0 ?? "padrão");
console.log(null && "nunca");
console.log(Math.round(-4.5));
console.log(Math.trunc(-4.9));
console.log(5 % 3, -5 % 3);
```

**A12.** O trecho abaixo deveria mostrar "Últimas vagas", mas mostra sempre a mesma coisa, para qualquer valor. Encontre o erro sem rodar e explique por que a condição é sempre verdadeira.

```js
const vagas = 500;

if (0 < vagas < 20) {
  console.log("Últimas vagas");
} else {
  console.log("Vagas à vontade");
}
```

### Nível B — Aplicação

**B1.** Escreva `validarSenha(senha)`, que devolva um objeto `{ valida: true, erros: [] }` verificando quatro regras: mínimo de 8 caracteres, ao menos uma letra maiúscula, ao menos um dígito e ao menos um caractere que não seja letra nem dígito. Sem expressões regulares (elas são da Aula 14) — use os métodos de string da Aula 10 e comparações de caractere.

Resultado esperado: `validarSenha("abc")` devolve `valida: false` com três erros descritivos; `validarSenha("Semana@Web7")` devolve `valida: true` e lista vazia; cada erro é uma frase que o usuário entenderia, não um código.

<details><summary>Dica</summary>

Percorrer a string caractere a caractere é assunto da Aula 12, mas você não precisa disso: `senha.toUpperCase() !== senha` já indica que existe pelo menos uma minúscula, e `senha.toLowerCase() !== senha` indica uma maiúscula. Para o dígito, teste se `"0123456789".includes(caractere)` para os caracteres que você extrair com `senha[0]`, `senha.at(-1)` e comparações. Monte a lista de erros com um array e `push` — a Aula 12 formaliza, mas `const erros = []; erros.push("texto");` já funciona.
</details>

**B2.** Escreva `converterTemperatura(valor, de, para)` que aceite `"C"`, `"F"` e `"K"` em qualquer combinação. Use `switch` para identificar a unidade de origem, converta tudo para Celsius internamente e depois para a unidade de destino. Se a unidade for inválida, devolva `null` e escreva um `console.error` explicando.

Resultado esperado: `converterTemperatura(100, "C", "F")` devolve `212`; `converterTemperatura(32, "F", "C")` devolve `0`; `converterTemperatura(0, "C", "K")` devolve `273.15`; `converterTemperatura(10, "X", "C")` devolve `null` e registra um erro.

<details><summary>Dica</summary>

Converter tudo para uma unidade intermediária evita escrever nove fórmulas — bastam seis. As fórmulas: `C = (F - 32) * 5 / 9`, `C = K - 273.15`, `F = C * 9 / 5 + 32`, `K = C + 273.15`. Use `de.toUpperCase()` antes do `switch` para aceitar `"c"` e `"C"`.
</details>

**B3.** Escreva `classificarIMC(peso, altura)` que calcule o índice de massa corporal (`peso / altura ** 2`) e devolva um objeto com o valor arredondado para uma casa e a faixa correspondente (abaixo do peso, adequado, sobrepeso, obesidade). Trate entradas inválidas: valores não numéricos, zero ou negativos devem devolver `null` com um aviso no console.

Resultado esperado: `classificarIMC(70, 1.75)` devolve algo como `{ imc: 22.9, faixa: "Peso adequado" }`; `classificarIMC(70, 0)` devolve `null`; `classificarIMC("setenta", 1.75)` devolve `null`.

<details><summary>Dica</summary>

Comece pelas validações, com um `if` que devolve `null` logo no início — isso evita aninhar todo o resto do código dentro de um `else`. `Number.isFinite(peso)` é melhor que `typeof peso === "number"`, porque `NaN` e `Infinity` também são do tipo `number`. Para arredondar em uma casa e continuar com um número (não uma string), use `Math.round(imc * 10) / 10`.
</details>

**B4.** Implemente `calcularFrete(uf, peso, valorCompra)` com regras encadeadas: frete grátis acima de R$ 200; base de R$ 15,00; acréscimo de R$ 10,00 para as UFs do Norte e Centro-Oeste; acréscimo de R$ 2,00 por quilo acima de 10 kg. Devolva o valor já formatado em reais com `Intl.NumberFormat`.

Resultado esperado: `calcularFrete("SP", 5, 100)` devolve `"R$ 15,00"`; `calcularFrete("MT", 5, 100)` devolve `"R$ 25,00"`; `calcularFrete("MT", 14, 100)` devolve `"R$ 33,00"`; `calcularFrete("MT", 14, 250)` devolve `"R$ 0,00"`.

<details><summary>Dica</summary>

Teste a regra do frete grátis **primeiro** e devolva imediatamente — as outras regras não precisam ser avaliadas. Para as UFs, `"AC AM AP PA RO RR TO DF GO MS MT".includes(uf.toUpperCase())` resolve sem array. O peso excedente é `Math.max(0, peso - 10)`, o que dispensa um `if`.
</details>

**B5.** Escreva `analisarInscricao(nome, idade, tipoIngresso)` que valide os três campos e devolva um objeto com `{ valida, mensagem, valorDevido }`. Regras: nome com pelo menos 3 caracteres depois do `trim()`; idade entre 14 e 120; `tipoIngresso` só pode ser `"estudante"`, `"profissional"` ou `"apoiador"`, com valores de R$ 12,50, R$ 25,00 e R$ 50,00. Menores de 18 anos recebem, além do resultado, um aviso de que precisam de autorização.

Resultado esperado: `analisarInscricao("Ana", 17, "estudante")` devolve `valida: true`, `valorDevido: 12.5` e uma mensagem que menciona a autorização; `analisarInscricao(" ", 30, "estudante")` devolve `valida: false` com mensagem sobre o nome; `analisarInscricao("Ana", 30, "vip")` devolve `valida: false` com mensagem sobre o tipo de ingresso.

<details><summary>Dica</summary>

Use `switch` para o preço e `if` para as validações. O aviso de menor de idade é um bom uso do operador `&&` dentro de um template literal: `${idade < 18 ? " Menores precisam de autorização." : ""}`. Devolva sempre o mesmo formato de objeto, mesmo quando inválido — quem chama a função não deveria precisar checar se a propriedade existe.
</details>

**B6.** Reescreva o bloco de decisão do Passo 3 da Mão na massa usando **apenas** ternários encadeados, sem nenhum `if`. Depois escreva um parágrafo comparando as duas versões: qual é mais fácil de ler? Qual é mais fácil de alterar quando surgir uma quinta faixa?

Resultado esperado: dois arquivos (`decisao-if.js` e `decisao-ternario.js`) que produzem exatamente a mesma saída para os valores 0, 3, 15, 33 e 130 de `inscritos`, e um texto de comparação com pelo menos três argumentos.

<details><summary>Dica</summary>

Para que a versão com ternário produza duas variáveis (`situacao` e `mensagem`), você precisará de dois encadeamentos — ou de um objeto. Formate o encadeamento em coluna, uma condição por linha, como no exemplo da seção 7.3. Ao comparar, considere também o caso de um ramo precisar executar **duas** instruções: o que acontece com o ternário nessa hora?
</details>

### Nível C — Desafio em sala

**C1.** No seu **projeto autoral**, crie o equivalente ao painel de vagas do site do evento: um bloco de estado que muda sozinho conforme um único número que você edita no topo do script. Requisitos: pelo menos quatro faixas de decisão (com `if`/`else if`), um valor formatado com `Intl.NumberFormat` (preço, distância, peso — o que fizer sentido no seu domínio), uma data formatada com `toLocaleDateString("pt-BR")`, concordância correta de singular e plural com ternário, e nenhum número mágico no meio do código (todos os limites devem ser constantes nomeadas no topo).

<details><summary>Dica</summary>

Comece escrevendo, em comentários, as quatro faixas em português: "se não há nenhum, então…; se há menos de 5, então…". Só depois traduza para `if`. Teste cada faixa trocando o número e recarregando — se alguma nunca aparece, a ordem dos testes está errada. Lembre-se de usar `Math.max(0, …)` para nunca exibir um número negativo.
</details>

**C2.** Escreva `js/relogio-evento.js` que, ao carregar qualquer página, imprima no Console um único `console.group` chamado "Relógio do evento" com: a data e a hora atuais formatadas em pt-BR; quantos dias faltam para a abertura (usando a constante `DIAS_ATE_A_ABERTURA`); a fase do evento como texto (`"pré-inscrições"` acima de 30 dias, `"inscrições abertas"` entre 30 e 8, `"reta final"` entre 7 e 1, `"acontecendo"` em 0, `"encerrado"` abaixo de 0), decidida com `switch (true)`; e o tempo restante quebrado em dias, horas e minutos com `%`.

<details><summary>Dica</summary>

`switch (true)` é uma forma pouco conhecida e perfeitamente válida: cada `case` recebe uma expressão booleana, e o primeiro `case` cujo valor for `true` é executado — `case diasRestantes > 30:`. Para a quebra em dias/horas/minutos, calcule a diferença total em milissegundos uma vez e vá dividindo: dias com `Math.trunc(ms / MS_POR_DIA)`, horas com `Math.trunc((ms % MS_POR_DIA) / MS_POR_HORA)`, e assim por diante.
</details>

## 🏆 Desafios

### ⭐ O sorteio honesto
Tags: javascript, investigacao, projeto

Quantas vezes você precisa sortear um número de 1 a 6 até que os seis valores tenham saído pelo menos uma vez? A intuição diz "umas dez"; a matemática diz 14,7 em média; e o seu computador pode dizer a verdade em três segundos. Antes de aprender laços (isso é a Aula 12), você consegue investigar isso **na mão**: um script que sorteia uma vez por recarregamento, guarda o resultado e mostra a contagem. Use o sorteio da seção 3.3 e as condicionais de hoje para construir um mini-experimento honesto — e descubra, de quebra, se `Math.random()` é tão uniforme quanto promete.

**Critérios de pronto**

- Um arquivo `sorteio.js` que, a cada recarregamento, sorteia um inteiro de 1 a 6 e imprime no Console o valor e um comentário decidido por `switch` (por exemplo, "número da sorte", "de novo esse não").
- Uma versão com faixa configurável por duas constantes (`MINIMO` e `MAXIMO`) no topo, funcionando corretamente para `1..6`, `0..9` e `10..20`.
- Uma verificação, com `console.assert`, de que o valor sorteado nunca sai da faixa — inclusive quando `MINIMO === MAXIMO`.
- Um comentário de três linhas explicando, com suas palavras, por que a fórmula usa `Math.floor` e por que existe o `+ 1`.

<details><summary>Pistas</summary>

1. Troque `Math.floor` por `Math.round` na fórmula e recarregue trinta vezes anotando os resultados: os extremos saem com metade da frequência dos outros. Descubra por quê.
2. `Math.random()` nunca devolve exatamente 1 — a documentação da MDN diz "de 0 (inclusivo) até 1 (exclusivo)". É essa exclusão que faz o `Math.floor` funcionar.
3. Para guardar a contagem entre recarregamentos, uma linha basta: `localStorage`. Procure `localStorage.getItem` na MDN — a Aula 14 aprofunda o assunto.
</details>

### ⭐⭐ Caça ao bug: o script que decide errado
Tags: javascript, bug, devtools, refatoracao

O script abaixo deveria classificar as inscrições do evento e mostrar o preço final. Ele roda sem nenhuma linha vermelha no Console — e mesmo assim está errado em **cinco** pontos: uma faixa nunca é alcançada, um desconto legítimo é ignorado, um preço aparece com quinze casas decimais, uma comparação é sempre verdadeira e um `switch` executa dois casos de uma vez. Nenhum erro é de sintaxe; todos são de lógica. Encontre os cinco usando o depurador da aba Sources, não `console.log` espalhado.

**`js/decisao-com-bug.js`**

```js
const inscritos = 118;
const VAGAS_TOTAIS = 120;
const vagasRestantes = VAGAS_TOTAIS - inscritos;

const tipo = "estudante";
const cupomDigitado = 0;
const desconto = cupomDigitado || 0.1;

let situacao;

if (vagasRestantes <= 20) {
  situacao = "últimas vagas";
} else if (vagasRestantes <= 5) {
  situacao = "crítico";
} else if (vagasRestantes === 0) {
  situacao = "esgotado";
} else {
  situacao = "tranquilo";
}

let preco;

switch (tipo) {
  case "estudante":
    preco = 25 * 0.5;
  case "profissional":
    preco = 25;
    break;
  default:
    preco = 50;
}

const precoFinal = preco - preco * desconto;

if (0 < vagasRestantes < 10) {
  console.log("Poucas vagas!");
}

console.log(`Situação: ${situacao} | Preço final: R$ ${precoFinal}`);
```

**Critérios de pronto**

- Um arquivo `decisao-corrigida.js` em que as quatro faixas funcionam: teste com `inscritos` valendo 0, 100, 115, 119 e 120 e mostre a saída de cada um.
- O preço final aparece formatado com `Intl.NumberFormat`, sem casas decimais sobrando.
- Um cupom de `0` (zero por cento de desconto) é respeitado como zero, e não substituído por 10%.
- Um arquivo `bugs.md` com uma tabela de cinco linhas: sintoma observado, causa técnica e correção aplicada.
- Pelo menos uma captura de tela da aba **Sources** com um breakpoint parado dentro da cadeia de `if`, mostrando o painel **Scope**.

<details><summary>Pistas</summary>

1. Em uma escada de `else if`, o primeiro teste verdadeiro vence e os demais nem são lidos. Qual ordem faz cada faixa ser alcançável?
2. Releia a tabela da seção 5.3: qual operador respeita o zero como valor legítimo?
3. Um `case` sem `break` não termina o `switch` — ele continua executando o próximo. Qual valor sobra em `preco` no fim?
4. `0 < x < 10` é avaliado em dois passos, e o resultado do primeiro é um booleano. Escreva a comparação do jeito certo.
5. Preço em ponto flutuante multiplicado por porcentagem quase sempre gera dízima. A solução da seção 2.5 se aplica aqui.
</details>

### ⭐⭐⭐ A calculadora de cronograma do evento
Tags: javascript, investigacao, projeto, acessibilidade

A organização da Semana Acadêmica precisa saber, a qualquer momento, em que fase está: falta mais de um mês, está na reta final, é hoje, ou já acabou? E precisa que a página inicial diga isso em português correto — "falta 1 dia", "faltam 2 dias", "é hoje", "começa em 3 horas". Datas são a área do JavaScript onde mais gente escorrega: fuso horário, mês que começa em zero, mudança de mês, horário de verão. Construa um módulo de cronograma que acerte todos esses casos e prove que acerta.

**Critérios de pronto**

- Um arquivo `cronograma.js` com as constantes do evento no topo (dias até a abertura, hora de início, duração em dias) e nenhum número mágico no restante do código.
- Uma variável de texto que descreve a situação com concordância correta em **seis** casos: mais de um dia, exatamente um dia, hoje antes da abertura (mostrando horas e minutos), durante o evento, no último dia e depois do fim.
- A quebra do tempo restante em dias, horas e minutos usando `%` e `Math.trunc`, sem nenhuma biblioteca externa.
- A data de abertura exibida por extenso em português com `toLocaleDateString("pt-BR", …)`, incluindo o dia da semana.
- Uma seção de testes no fim do arquivo que força os seis casos alterando a constante de dias (inclusive valores negativos) e imprime o resultado de cada um com `console.group`.
- O texto é escrito em um elemento com `role="status"`, para que leitores de tela anunciem a mudança.

<details><summary>Pistas</summary>

1. Comece pelo caso mais difícil: o dia da abertura. Nesse dia, `diasRestantes` é 0, mas ainda podem faltar horas — e a mensagem "faltam 0 dias" seria absurda.
2. Para forçar os seis casos sem esperar o calendário, transforme a constante de dias em uma variável e escreva um bloco de testes que a altera e recalcula. É exatamente assim que se testa código dependente de tempo.
3. `Math.ceil` e `Math.trunc` dão respostas diferentes para 0,3 dia restante. Decida qual você quer **antes** de escrever a condição, e escreva um comentário justificando.
4. Consulte a página de `Intl.DateTimeFormat` na MDN e compare com `toLocaleDateString`: os dois aceitam as mesmas opções, e um deles é mais eficiente quando o formato se repete.
5. Cuidado com o fuso: uma string ISO só com a data (no formato `AAAA-MM-DD`) é interpretada como UTC e pode "voltar um dia" no Brasil. Passar os números separados, `new Date(ano, mes - 1, dia)`, evita a armadilha.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `Uncaught ReferenceError: Cannot access 'total' before initialization` | a variável `let`/`const` foi usada acima da linha que a declara — zona morta temporal | mova a declaração para antes do primeiro uso; declare tudo no topo do bloco |
| `Uncaught SyntaxError: Identifier 'vagas' has already been declared` | o mesmo nome foi declarado duas vezes com `let`/`const` no mesmo escopo | apague a segunda declaração (provavelmente você queria apenas atribuir) |
| `Uncaught TypeError: Assignment to constant variable.` | tentativa de reatribuir uma `const` | se o valor muda ao longo do programa, declare com `let` |
| `Uncaught TypeError: Cannot read properties of null (reading 'textContent')` | `querySelector` não achou o elemento: o `id` está diferente, ou a página atual não tem esse elemento | proteja com `if (elemento !== null)`; confira o `id` no HTML |
| `Uncaught TypeError: Cannot read properties of undefined (reading 'email')` | leitura de uma propriedade dentro de um objeto que não existe | use `objeto.parte?.email` quando a ausência for legítima |
| `Uncaught SyntaxError: Unexpected token '??'` | `??` misturado com `\|\|` ou `&&` sem parênteses | escreva `(a \|\| b) ?? c` — a linguagem exige o parêntese |
| A página mostra `NaN` no lugar de um número | uma conta usou uma string com letras, `undefined` ou um campo vazio | converta com `Number()` antes de calcular e verifique com `Number.isNaN()` |
| O preço aparece como `22.500000000000004` | multiplicação de decimais em ponto flutuante | arredonde na exibição com `Intl.NumberFormat`, ou trabalhe com centavos inteiros |
| Uma faixa do `else if` nunca é alcançada | as condições estão em ordem errada: uma condição mais ampla vem antes de uma mais restrita | ordene do caso mais restrito para o mais amplo e teste todas as faixas |
| A condição é sempre verdadeira | escreveu `0 < x < 20`, que JavaScript avalia em dois passos, ou usou `=` no lugar de `===` | escreva `x > 0 && x < 20`; use sempre `===` na comparação |
| O `switch` executa dois casos seguidos | falta `break` no fim de um `case` — a execução "vaza" | acrescente `break` em todos os casos, exceto onde o vazamento for intencional e comentado |
| Um zero legítimo foi substituído pelo valor padrão | uso de `\|\|`, que trata `0` e `""` como vazios | troque por `??`, que só reage a `null` e `undefined` |
| O texto sai "Restam 1 vagas" | falta concordância de singular e plural | use um ternário: `${n === 1 ? "vaga" : "vagas"}` |
| `Uncaught RangeError: toFixed() digits argument must be between 0 and 100` | passou um número inválido para `toFixed` | use de 0 a 100; para dinheiro, `toFixed(2)` ou `Intl.NumberFormat` |
| O mês exibido está um a menos do esperado | `getMonth()` devolve 0 para janeiro | some 1 ao exibir, ou use `toLocaleDateString` com a opção `month` |

## 🏠 Atividade assíncrona (1 h)

**Parte 1 — Leitura (20 min).** FLANAGAN, D. *JavaScript: o guia definitivo*, capítulos sobre expressões, operadores e instruções. Na MDN, leia "Expressões e operadores" e a página do operador de coalescência nula (links em Para aprofundar). Anote dois operadores que existem na MDN e não apareceram nesta aula.

**Parte 2 — Entrega (30 min).** Entregue os exercícios **B1** (`validarSenha`) e **B4** (`calcularFrete`) em arquivos `.js` comentados, cada um com pelo menos cinco casos de teste demonstrados no Console. No seu **projeto autoral**, entregue o exercício **C1**: o bloco de estado que decide sozinho, com as constantes no topo, quatro faixas e formatação em pt-BR.

**Critério de pronto:** ao trocar um único número no topo do script do projeto autoral e recarregar, a mensagem e o destaque visual mudam de faixa; nenhuma página do projeto mostra erro vermelho no Console; nenhum número mágico aparece no meio do código; nenhum `var` e nenhum `==` sobreviveram nos arquivos `.js`.

**Parte 3 — Fórum (10 min).** No fórum "`let` ou `const`" do SIGAA: defenda, com argumentos técnicos, a prática de declarar tudo como `const` por padrão e usar `let` só quando a reatribuição for necessária. Traga um trecho do seu próprio projeto em que a escolha importou, e comente o argumento de um colega.

**Entrega:** commit + push e link do repositório (ou `.zip`) no SIGAA, no prazo do cronograma da trilha.

## ✅ Checkpoint do projeto

Ao fim desta aula, o repositório do seu projeto autoral deve ter:

- [ ] Todas as constantes do domínio declaradas em `MAIUSCULO_COM_UNDERSCORE` no topo do script, sem números mágicos espalhados pelo código.
- [ ] Pelo menos uma cadeia `if`/`else if`/`else` com quatro faixas, todas alcançáveis (testadas uma a uma).
- [ ] Pelo menos um ternário usado para concordância de singular e plural em um texto exibido na tela.
- [ ] Pelo menos um `switch` com `break` em todos os casos e um `default`.
- [ ] Um valor monetário (ou numérico) formatado com `Intl.NumberFormat("pt-BR", …)` e uma data formatada com `toLocaleDateString("pt-BR", …)`.
- [ ] Um elemento de aviso que aparece e desaparece conforme o estado, sem que o HTML precise ser editado (`textContent` vazio + `:empty` no CSS).
- [ ] Um `if (elemento !== null)` protegendo qualquer script compartilhado por várias páginas.
- [ ] Zero ocorrências de `var` e de `==` em todos os arquivos `.js`.
- [ ] Nenhum erro vermelho no Console em nenhuma das páginas.

## 📚 Para aprofundar

- MDN — **Expressões e operadores** (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Operators> — a referência completa, com a tabela de precedência oficial.
- MDN — **`let`** (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Statements/let> — a seção sobre a zona morta temporal, com exemplos.
- MDN — **Operador de coalescência nula `??`** (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Operators/Nullish_coalescing> — a comparação com `||`, caso a caso.
- MDN — **Encadeamento opcional `?.`** (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Operators/Optional_chaining> — as três formas do operador.
- MDN — **`Math`** (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Global_Objects/Math> — todos os métodos, com exemplos executáveis.
- MDN — **`Intl.NumberFormat`** (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat> — as opções de moeda, percentual e unidades.
- MDN — **`Date`** (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Global_Objects/Date> — os métodos de leitura, escrita e formatação.
- MDN — **`switch`** (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Statements/switch> — inclui o caso do vazamento intencional.
- javascript.info: <https://javascript.info/> — capítulos "Operators", "Comparisons", "Conditional branching" e "Logical operators"; cada um tem exercícios com solução comentada.
- web.dev — **Learn JavaScript**: <https://web.dev/learn/javascript> — os módulos de operadores e de fluxo de controle, com exemplos interativos.
- FLANAGAN, David. *JavaScript: o guia definitivo*. Bookman, 2014 — capítulos de expressões, operadores e instruções.
- STEFANOV, Stoyan. *Padrões JavaScript*. Novatec, 2010 — capítulo 2, na parte sobre escopo e declaração de variáveis.
- MILETTO, Evandro M.; BERTAGNOLLI, Silvia C. *Desenvolvimento de software II*. Bookman, 2014 — capítulo sobre lógica de programação aplicada à web.

Na próxima aula, o programa deixa de fazer uma coisa de cada vez: você vai aprender as estruturas de repetição (`for`, `while`, `do…while`, `for…of`), organizar informação em arrays e objetos e produzir os primeiros relatórios do evento no Console — totais por dia, busca por trilha e a lista de palestras que vai alimentar as páginas nas aulas seguintes.
