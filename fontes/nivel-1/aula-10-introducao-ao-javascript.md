# Aula 10 — Introdução ao JavaScript

> **Nível 1 — Introdução ao Desenvolvimento Web** · Unidade 3: JavaScript e interatividade
> WebLab · UNEMAT — Campus Sinop
> **Tempo estimado:** 3 blocos de 50 min + 1 h de prática

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Situar o JavaScript entre as três tecnologias do front-end e explicar o que cada uma faz.
- Incluir scripts corretamente com `defer` e explicar por que a posição da tag `<script>` importa.
- Usar o Console e a aba Sources do DevTools para executar, inspecionar e depurar código.
- Declarar variáveis com `const` e `let`, escolhendo a forma certa em cada caso.
- Reconhecer os tipos primitivos, prever o resultado de `typeof` e listar os valores falsy.
- Montar textos com template literals e usar os métodos essenciais de string.
- Converter tipos explicitamente e prever o resultado das conversões implícitas.
- Fechar o Marco 2 do projeto autoral.

## 📋 Pré-requisitos

- [ ] Site do evento com as cinco páginas (início, programação, inscrição, palestrantes, contato) estilizadas, responsivas e com animações, abrindo no Live Server.
- [ ] VS Code com a extensão Live Server; Chrome ou Firefox com o DevTools acessível pelo <kbd>F12</kbd>.
- [ ] Marco 2 pronto para fechar — as instruções completas estão no fim desta aula.

> Na aula passada você fechou a Unidade 2 com transições, `@keyframes` e `prefers-reduced-motion`: o site do evento está bonito e responsivo, mas continua parado — cada número de vagas foi digitado à mão no HTML e nada reage ao visitante. Hoje começa a Unidade 3: o JavaScript entra em cena, o site ganha o seu primeiro script e o Console do navegador vira a sua principal ferramenta de trabalho.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | O que é JavaScript; as três formas de incluir um script; `defer` × `async`; o Console e o DevTools |
| 2 | 50 min | Variáveis com `const`/`let`; tipos primitivos e `typeof`; strings e template literals; conversões e valores falsy |
| 3 | 50 min | Mão na massa: o site do evento ganha um script externo; Marco 2 do projeto |

## 1. O que é JavaScript

### As três camadas do front-end

Uma página web é feita de três linguagens que dividem responsabilidades. Você já domina duas delas; hoje entra a terceira.

| Tecnologia | Responsabilidade | Pergunta que responde | No site do evento |
|---|---|---|---|
| HTML | estrutura e conteúdo | *o que* está na página? | títulos, tabela da programação, formulário de inscrição |
| CSS | apresentação | *como* a página aparece? | cores, grid do layout, menu responsivo, animações |
| JavaScript | comportamento | *o que acontece* quando o usuário interage? | calcular vagas, validar o formulário, filtrar a programação |

A analogia clássica é a de um corpo: o HTML é o esqueleto, o CSS é a pele e a roupa, e o JavaScript são os músculos e o sistema nervoso — sem ele, nada se move nem reage.

### Uma linguagem, quatro adjetivos

JavaScript é uma linguagem **interpretada**, de **tipagem dinâmica**, **multiparadigma** e **padronizada**. Cada adjetivo diz algo prático:

- **Interpretada** — você não compila nada antes de rodar. O navegador lê o arquivo `.js` e executa na hora. (Por baixo do capô, os motores modernos compilam trechos "quentes" para código de máquina em tempo real, a chamada compilação JIT; para você, o efeito é que salvar o arquivo e recarregar a página já basta.)
- **Tipagem dinâmica** — uma variável não tem tipo fixo; o *valor* tem tipo. A mesma variável pode guardar um número agora e um texto depois. Isso dá agilidade e também é a origem de boa parte dos bugs que você vai caçar nesta unidade.
- **Multiparadigma** — dá para programar de forma imperativa (sequência de comandos), funcional (funções que recebem e devolvem funções, Aula 13) e orientada a objetos (classes, que você verá no Nível 2).
- **Padronizada** — a especificação da linguagem chama-se **ECMAScript** e é mantida pelo comitê **TC39** da Ecma International. "JavaScript" é o nome popular; "ECMAScript" é o nome do padrão. Na prática, são sinônimos.

É a única linguagem executada nativamente por todos os navegadores: Chrome, Firefox, Safari e Edge entendem JavaScript sem instalar nada.

### JavaScript não é Java

A confusão é antiga e o nome foi a causa. Em 1995, a Netscape lançou a linguagem como "LiveScript" e, semanas depois, renomeou para "JavaScript" em um acordo de marketing com a Sun Microsystems, dona do Java — que estava na moda. As linguagens são diferentes em sintaxe, tipagem, forma de execução e propósito. Dizer que JavaScript é parecido com Java é como dizer que "hamster" é parecido com "ham" — compartilham letras, não natureza.

### ECMAScript e as versões

| Versão | Ano | O que trouxe |
|---|---|---|
| ES1 | 1997 | primeira padronização |
| ES5 | 2009 | modo estrito, JSON nativo, `forEach`, `map`, `filter` |
| ES6 / ES2015 | 2015 | `let`, `const`, arrow functions, classes, template literals, módulos, Promises |
| ES2016 em diante | anual | pequenas adições por ano: `**`, `includes`, `async/await`, `?.`, `??`, `at()` |

Desde 2015 sai uma versão por ano, com o nome do ano. Nesta trilha você escreve **JavaScript moderno (ES2015+)**: `const` e `let` em vez de `var`, template literals em vez de concatenação, e os métodos de array que você vai conhecer na Aula 12.

> **🧠 Você sabia?**
> A primeira versão do JavaScript foi escrita por Brendan Eich em **dez dias**, em maio de 1995, sob pressão para que o Netscape Navigator 2 saísse com uma linguagem de script. O nome interno era "Mocha". Várias decisões tomadas às pressas naquelas semanas — como o comportamento estranho de `==` e o resultado de `typeof null` — continuam na linguagem até hoje, porque corrigi-las quebraria milhões de sites.

### Onde o JavaScript roda

O código JavaScript é executado por um **motor** (engine). Cada navegador tem o seu: o Chrome e o Edge usam o V8, o Firefox usa o SpiderMonkey, o Safari usa o JavaScriptCore. Em 2009, o V8 foi retirado do navegador e embrulhado em um programa de linha de comando chamado **Node.js** — desde então, JavaScript também roda em servidores, e é isso que você vai usar no Nível 2 para construir APIs. Nesta trilha, porém, o único lugar onde o seu JavaScript roda é o navegador.

## 2. Como incluir JavaScript em uma página

Existem três maneiras de colocar um script em uma página HTML. Só uma delas é a forma correta para o dia a dia.

**Arquivo:** `exemplo-inclusao.html`

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Três formas de incluir JavaScript</title>

  <!-- 3. Externo, com defer — a forma correta -->
  <script src="js/script.js" defer></script>
</head>
<body>
  <!-- 1. Inline, dentro de um atributo — evite -->
  <button onclick="alert('Oi')">Clique</button>

  <!-- 2. Interno, dentro da própria página — só para testes rápidos -->
  <script>
    console.log("Executando o script interno");
  </script>
</body>
</html>
```

1. **Inline** (`onclick="…"`): mistura comportamento com estrutura, não pode ser reaproveitado entre páginas e dificulta a leitura. É o equivalente ao `style="…"` que você aprendeu a evitar na Aula 06.
2. **Interno** (`<script>` com código dentro): útil para um experimento de dois minutos, mas o código fica preso a uma única página.
3. **Externo** (`<script src="…">`): um arquivo `.js` separado, incluído por todas as páginas que precisam dele, com cache do navegador e leitura limpa. É o que você vai usar no site do evento.

### `defer`, `async` e a posição da tag

O navegador lê o HTML de cima para baixo e vai construindo a árvore de elementos (o **DOM**, que você conhecerá a fundo na Aula 13). Quando encontra um `<script>` sem atributos, ele **para** de ler o HTML, baixa o script, executa e só então continua. Isso tem duas consequências: a página demora mais para aparecer e, pior, o script roda antes de o restante do HTML existir — qualquer tentativa de acessar um elemento que ainda não foi lido falha.

| Forma | Quando baixa | Quando executa | Use quando |
|---|---|---|---|
| `<script>` no `<head>` sem atributo | interrompe a leitura do HTML | imediatamente — o DOM ainda não existe | nunca, para scripts que tocam a página |
| `<script>` antes de `</body>` | quando o HTML já foi lido | imediatamente — o DOM já existe | solução clássica; funciona, mas atrasa o download |
| `defer` | em paralelo com a leitura do HTML | depois que todo o HTML foi lido, **na ordem em que foram declarados** | sempre — é a melhor opção |
| `async` | em paralelo com a leitura do HTML | assim que terminar de baixar, **fora de ordem** | só para scripts independentes, como analytics |

A regra desta trilha: `<script src="…" defer>` no `<head>`. Você ganha o download em paralelo, a garantia de que o HTML inteiro já foi lido e a ordem previsível entre vários scripts — o que vai importar na Aula 12, quando um arquivo de dados precisar ser carregado antes do arquivo que o usa.

> **🔎 Por baixo do capô**
> O `defer` só faz sentido com `src`. Em um script interno (sem `src`), o atributo é ignorado e o código roda na hora. Se você precisa de um script interno que espere o HTML, coloque-o antes de `</body>` — ou, melhor, mova o código para um arquivo externo.

### O primeiro script completo

**Arquivo:** `primeiro.html`

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Primeiro script</title>
  <script src="js/primeiro.js" defer></script>
</head>
<body>
  <h1>Semana Acadêmica de Sistemas de Informação</h1>
  <p>Vagas restantes: <strong id="vagas">?</strong></p>
</body>
</html>
```

**Arquivo:** `js/primeiro.js`

```js
// Tudo depois de // até o fim da linha é comentário: o navegador ignora.
console.log("O script carregou!");

const vagasTotais = 120;
const inscritos = 87;
const vagasRestantes = vagasTotais - inscritos;

console.log("Vagas restantes:", vagasRestantes);

// Localiza o elemento com id="vagas" e troca o texto dele.
// A manipulação da página será aprofundada na Aula 13; por ora,
// leia esta linha como "escreva o valor dentro do <strong>".
document.querySelector("#vagas").textContent = vagasRestantes;
```

Abra `primeiro.html` no Live Server, pressione <kbd>F12</kbd> e olhe a aba **Console**: a mensagem "O script carregou!" e o número 33 devem aparecer, e o `?` da página deve ter virado `33`.

> **🔬 Investigue**
> Remova o `defer` da tag `<script>` em `primeiro.html`, salve e recarregue. A página mostra `?` e o Console exibe `Uncaught TypeError: Cannot read properties of null (reading 'textContent')` (no Firefox: `document.querySelector(...) is null`). Leia a mensagem com calma: `querySelector` devolveu `null` porque o `<strong>` ainda não existia quando o script rodou. Agora mova a tag `<script>` (ainda sem `defer`) para antes de `</body>` e recarregue: funciona de novo. Você acabou de ver, na prática, por que a posição importa. Devolva o `defer` ao `<head>` antes de continuar.

## 3. O Console e o DevTools

### Abrindo o DevTools

<kbd>F12</kbd> abre o painel; <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>J</kbd> (no macOS, <kbd>Cmd</kbd>+<kbd>Option</kbd>+<kbd>J</kbd>) abre direto na aba Console. Você já usou as abas Elements e Styles na Unidade 2; agora as abas que interessam são **Console** e **Sources**.

### Os métodos de `console`

`console.log` é a sua principal ferramenta de depuração enquanto aprende. Mas o objeto `console` tem mais do que `log`:

**Arquivo:** `js/console-demo.js`

```js
console.log("Mensagem comum");
console.info("Informação — igual ao log, com ícone em alguns navegadores");
console.warn("Aviso — fundo amarelo");
console.error("Erro — fundo vermelho e pilha de chamadas");

// Vários valores separados por vírgula: o console mostra cada um com o tipo certo
const nome = "Ana";
const nota = 8.5;
console.log("Aluna:", nome, "Nota:", nota);

// typeof mostra o tipo do valor
console.log("Valor:", nota, typeof nota);

// console.table monta uma tabela a partir de um array de objetos
console.table([
  { nome: "Ana", nota: 8 },
  { nome: "Bruno", nota: 7 },
]);

// console.group agrupa mensagens com recuo (útil para separar etapas)
console.group("Cálculo de vagas");
console.log("Total: 120");
console.log("Inscritos: 87");
console.groupEnd();

// console.time mede quanto tempo passou entre time e timeEnd
console.time("cálculo");
const resultado = 120 - 87;
console.timeEnd("cálculo"); // cálculo: 0.01ms (o número varia)

// console.assert só imprime se a condição for falsa
console.assert(resultado === 33, "O cálculo de vagas está errado!");

// console.count conta quantas vezes foi chamado com aquele rótulo
console.count("carregamento");

// console.clear limpa o console
```

> **💡 Dica**
> Use vírgula, não `+`, para mostrar vários valores: `console.log("Nota:", nota)` preserva o tipo e a cor de cada valor; `console.log("Nota: " + nota)` transforma tudo em texto. Isso importa quando o valor é um objeto — com `+` você vê apenas `[object Object]`.

### Escrevendo direto no Console

O Console é um **REPL** (leia, avalie, imprima, repita): digite uma expressão, pressione <kbd>Enter</kbd> e veja o resultado na hora. É o melhor lugar para testar uma dúvida em cinco segundos.

```js
2 + 2
// 4

"Web".toUpperCase()
// "WEB"

typeof 42
// "number"

document.title
// "Primeiro script"
```

Para escrever mais de uma linha, use <kbd>Shift</kbd>+<kbd>Enter</kbd>. Para reaproveitar o último resultado, use `$_`. Para pegar o elemento selecionado na aba Elements, use `$0`. As setas para cima e para baixo percorrem o histórico.

### A aba Sources e os breakpoints

`console.log` funciona, mas exige que você adivinhe onde colocar a mensagem, salve, recarregue e leia. A aba **Sources** oferece algo melhor: o **breakpoint**, um ponto de parada. Abra `js/primeiro.js` na árvore de arquivos, clique no número de uma linha e recarregue a página. O navegador **pausa** exatamente ali e mostra, no painel **Scope**, o valor de cada variável naquele instante. Os botões no topo permitem avançar linha a linha (<kbd>F10</kbd>), entrar em uma função (<kbd>F11</kbd>) ou continuar a execução (<kbd>F8</kbd>).

Você também pode pausar por código: a instrução `debugger;` no meio do script tem o mesmo efeito de um breakpoint quando o DevTools está aberto.

```js
const vagasTotais = 120;
const inscritos = 87;
debugger; // a execução pausa aqui, com o DevTools aberto
const vagasRestantes = vagasTotais - inscritos;
```

Nas primeiras semanas, `console.log` basta. Quando os scripts crescerem (Aula 13 em diante), os breakpoints vão economizar horas.

### `alert`, `prompt` e `confirm`

Os três abrem caixas de diálogo do próprio navegador: `alert("texto")` mostra uma mensagem; `prompt("pergunta")` pede um texto e devolve o que o usuário digitou (ou `null` se cancelar); `confirm("pergunta")` devolve `true` ou `false`. Você vai vê-los em tutoriais antigos, e eles servem para um experimento rápido. Em aplicações reais são inadequados: **bloqueiam** a página inteira até serem fechados, não podem ser estilizados, ignoram o CSS do site, atrapalham leitores de tela e alguns navegadores os suprimem depois do segundo uso. Na Aula 14 você vai construir mensagens de validação de verdade, dentro da própria página.

## 4. Variáveis: `const`, `let` e por que não `var`

Uma variável é um nome que aponta para um valor guardado na memória. Em JavaScript moderno há duas palavras-chave para declarar variáveis — e uma terceira, herdada, que você precisa reconhecer para nunca usar.

```js
let contador = 0;        // pode receber outro valor depois
const PI = 3.14159;      // NÃO pode receber outro valor
var antigo = "evite";    // legado: escopo de função e comportamento confuso
```

**Regra prática:** declare tudo com `const`. Só troque por `let` quando o valor precisar mudar ao longo do programa (um contador, um acumulador, um estado que alterna). Nunca use `var` em código novo — a Aula 11 mostra em detalhe o que ele faz de estranho.

### `const` congela a ligação, não o conteúdo

```js
const lista = [1, 2, 3];
lista.push(4);      // permitido: o conteúdo mudou, a referência continua a mesma
console.log(lista); // [1, 2, 3, 4]

lista = [5, 6];     // Uncaught TypeError: Assignment to constant variable.
```

`const` impede que o **nome** seja religado a outro valor. Se o valor é um array ou um objeto, o seu interior continua editável. Isso confunde no começo, mas é coerente: `const` protege a ligação entre nome e valor, não o valor em si.

### Nomes de variáveis

- Podem conter letras, dígitos, `_` e `$`; não podem começar com dígito. Acentos são permitidos, mas evite-os — o teclado do colega pode não ter.
- São **case-sensitive**: `nome`, `Nome` e `NOME` são três variáveis diferentes.
- Convenção: `camelCase` para variáveis e funções (`totalInscritos`), `PascalCase` para classes (`EventoCard`), `MAIUSCULO_COM_UNDERSCORE` para constantes globais que nunca mudam (`VAGAS_TOTAIS`).
- Nomes devem descrever o conteúdo: `totalAlunosAprovados`, não `x` ou `tmp2`. O código é lido muito mais vezes do que escrito.
- Palavras reservadas não podem ser nomes: `let`, `class`, `for`, `if`, `return`, `new` e cerca de quarenta outras. O Console avisa com `Uncaught SyntaxError: Unexpected token` se você tentar.

```js
// Bons nomes
const nomeDoEvento = "Semana Acadêmica de Sistemas de Informação";
const VAGAS_TOTAIS = 120;
let inscritosConfirmados = 87;

// Nomes ruins (funcionam, mas ninguém entende)
const n = "Semana Acadêmica de Sistemas de Informação";
const v = 120;
let x = 87;
```

## 5. Tipos de dados

### Os sete tipos primitivos

Um valor **primitivo** é um valor simples, sem partes internas, copiado por valor.

```js
const texto = "Olá";                 // string — texto entre aspas
const numero = 42;                   // number — inteiro
const decimal = 3.14;                // number — decimal (não existe tipo separado)
const verdadeiro = true;             // boolean — true ou false
const nada = null;                   // null — ausência intencional de valor
let indefinido;                      // undefined — declarada, mas sem valor
const grande = 9007199254740993n;    // bigint — inteiros gigantes, com n no fim
const simbolo = Symbol("id");        // symbol — identificador único (raro no Nível 1)
```

Tudo que não é primitivo é **objeto**: arrays, funções, datas, o próprio `document`. Você vai trabalhar com arrays e objetos na Aula 12.

### `typeof`

O operador `typeof` devolve, como string, o tipo de um valor:

```js
typeof "texto";       // "string"
typeof 42;            // "number"
typeof 3.14;          // "number"
typeof true;          // "boolean"
typeof undefined;     // "undefined"
typeof 10n;           // "bigint"
typeof Symbol("id");  // "symbol"
typeof null;          // "object"   ← bug histórico, mantido por compatibilidade
typeof [1, 2];        // "object"   ← arrays são objetos
typeof {};            // "object"
typeof function () {}; // "function" ← funções são objetos, mas typeof as distingue
typeof NaN;           // "number"   ← sim, "não é um número" é do tipo number
```

> **🧠 Você sabia?**
> `typeof null === "object"` é um bug da primeira implementação de 1995. Os valores eram guardados com uma etiqueta de tipo nos bits mais baixos; a etiqueta `0` significava "objeto", e `null` era representado pelo ponteiro nulo — que também é `0`. Quando o TC39 discutiu corrigir isso (uma proposta chegou a sugerir `typeof null === "null"`), a resposta foi não: sites demais dependem do comportamento antigo. Para testar se um valor é `null`, compare diretamente: `valor === null`.

### `number`: um tipo só para inteiros e decimais

JavaScript não separa `int` de `float`: todo número é um `number`, armazenado como ponto flutuante de 64 bits (padrão IEEE 754). Alguns valores especiais moram nesse tipo:

```js
1 / 0;                    // Infinity
-1 / 0;                   // -Infinity
0 / 0;                    // NaN — "Not a Number", resultado de contas impossíveis
Number("abc");            // NaN
Number.MAX_SAFE_INTEGER;  // 9007199254740991 — maior inteiro representado com exatidão
9007199254740992 + 1;     // 9007199254740992 — acima do limite, a conta erra em silêncio
9007199254740992n + 1n;   // 9007199254740993n — bigint resolve
0.1 + 0.2;                // 0.30000000000000004 — a Aula 11 explica esse resultado
```

`NaN` tem uma propriedade única: é o único valor de JavaScript que **não é igual a si mesmo**. `NaN === NaN` é `false`. Para verificar se algo é `NaN`, use `Number.isNaN(valor)`.

### `null` e `undefined`: dois jeitos de dizer "nada"

| | `undefined` | `null` |
|---|---|---|
| Quem atribui | a própria linguagem | você, o programador |
| Significado | "ainda não recebeu valor" | "intencionalmente vazio" |
| Quando aparece | variável declarada sem valor; propriedade inexistente; função sem `return` | quando você escreve `= null`; `querySelector` sem resultado |
| `typeof` | `"undefined"` | `"object"` |

Uma variável declarada sem valor vale `undefined`. Se quiser dizer explicitamente "este campo está vazio de propósito", use `null`.

## 6. Strings e template literals

### Três formas de escrever texto

```js
const aspasDuplas = "Semana Acadêmica";
const aspasSimples = 'Semana Acadêmica';
const crase = `Semana Acadêmica`;
```

As duas primeiras são equivalentes; escolha uma e seja consistente (esta apostila usa aspas duplas). A terceira, com **crase** (acento grave), é o **template literal** — e faz coisas que as outras não fazem.

### Concatenação × template literal

```js
const nome = "Maria";
const idade = 20;

// Concatenação clássica com + : funciona, mas é fácil esquecer um espaço ou uma aspa
const frase1 = "Olá, " + nome + "! Você tem " + idade + " anos.";

// Template literal: a expressão entre ${ } é avaliada e inserida no texto
const frase2 = `Olá, ${nome}! Você tem ${idade} anos.`;

console.log(frase1 === frase2); // true — o resultado é idêntico
```

Dentro de `${ }` cabe qualquer expressão, não só uma variável:

```js
const vagasTotais = 120;
const inscritos = 87;

console.log(`Restam ${vagasTotais - inscritos} vagas.`);
console.log(`Ocupação: ${((inscritos / vagasTotais) * 100).toFixed(1)}%`);
console.log(`Situação: ${inscritos >= vagasTotais ? "lotado" : "aberto"}`);
```

### Multilinha

Um template literal pode ocupar várias linhas, preservando as quebras — perfeito para montar trechos de HTML, como você fará na Aula 13:

```js
const nome = "Maria";
const idade = 20;

const html = `
  <div class="cartao">
    <h3>${nome}</h3>
    <p>Idade: ${idade}</p>
  </div>
`;

console.log(html);
```

Com aspas comuns, o mesmo texto exigiria `\n` para cada quebra e `+` para cada linha.

### Métodos essenciais de string

Uma string sabe fazer várias coisas consigo mesma. Os métodos abaixo cobrem 90% do uso diário. Repare que **nenhum deles altera a string original** — strings são imutáveis; cada método devolve uma string nova.

```js
const s = "  Desenvolvimento Web  "; // dois espaços em cada ponta

s.length;                     // 23 — quantidade de caracteres (é propriedade, sem parênteses)
s.trim();                     // "Desenvolvimento Web" — remove espaços das pontas
s.trimStart();                // "Desenvolvimento Web  "
s.toUpperCase();              // "  DESENVOLVIMENTO WEB  "
s.toLowerCase();              // "  desenvolvimento web  "
s.includes("Web");            // true — contém?
s.startsWith("  Des");        // true — começa com?
s.trim().endsWith("Web");     // true — termina com?
s.indexOf("Web");             // 18 — posição da primeira ocorrência (ou -1)
s.slice(2, 17);               // "Desenvolvimento" — do índice 2 até antes do 17
s.replace("Web", "Mobile");   // "  Desenvolvimento Mobile  " — só a primeira ocorrência
s.replaceAll("e", "3");       // "  D3s3nvolvim3nto W3b  " — todas
s.trim().split(" ");          // ["Desenvolvimento", "Web"] — quebra em array
"7".padStart(3, "0");         // "007" — completa à esquerda até 3 caracteres
"ab".repeat(3);               // "ababab"
s.trim().charAt(0);           // "D" — caractere na posição 0
s.trim()[0];                  // "D" — mesma coisa, com colchetes
s.trim().at(-1);              // "b" — índice negativo conta do fim
```

O índice começa em zero: o primeiro caractere é o `[0]`. Isso vale para strings hoje e para arrays na Aula 12.

### Caracteres especiais

```js
const comAspas = "Ela disse \"oi\" e saiu";   // \" escapa a aspa dentro da string
const comAspas2 = 'Ela disse "oi" e saiu';    // ou troque o tipo de aspa
const quebra = "Linha 1\nLinha 2";            // \n é quebra de linha
const tab = "Nome:\tAna";                      // \t é tabulação
const barra = "C:\\pasta\\arquivo";            // \\ é uma barra literal
```

> **🔬 Investigue**
> No Console, digite `"ação".length` e depois `"😀".length`. A primeira dá `4`, como esperado. A segunda dá `2`, embora seja um único emoji. JavaScript conta strings em unidades de 16 bits (UTF-16), e emojis modernos ocupam duas. Agora teste `[..."😀"].length` — o resultado é `1`. Guarde esse detalhe: ele explica bugs de "limite de caracteres" em formulários com emoji.

## 7. Conversão de tipos: explícita e implícita

### Conversão explícita

Você pede a conversão chamando a função do tipo de destino:

```js
Number("42");          // 42
Number("42.5");        // 42.5
Number("  42  ");      // 42 — espaços nas pontas são ignorados
Number("");            // 0 — string vazia vira zero (armadilha!)
Number("abc");         // NaN
Number("42px");        // NaN — qualquer letra sobrando invalida tudo
Number(null);          // 0
Number(undefined);     // NaN
Number(true);          // 1

parseInt("42px");      // 42 — lê dígitos até encontrar algo que não é dígito
parseInt("3.99");      // 3 — descarta a parte decimal
parseInt("abc");       // NaN
parseFloat("3.14m");   // 3.14

String(42);            // "42"
String(null);          // "null"
(42).toFixed(2);       // "42.00" — atenção: devolve STRING, com 2 casas decimais
(3.14159).toFixed(2);  // "3.14"

Boolean("");           // false
Boolean("0");          // true — string com conteúdo é verdadeira
Boolean(0);            // false
Boolean([]);           // true — array vazio é verdadeiro
```

Quando o valor vem de um formulário — e todo valor de formulário chega como **string** —, converter com `Number()` é o primeiro passo antes de qualquer conta. Isso será o centro da Aula 14.

### Conversão implícita (coerção)

JavaScript converte tipos sozinho quando um operador recebe tipos diferentes. As regras são previsíveis, mas nem sempre intuitivas:

```js
"5" + 3;        // "53"  — + com string vira concatenação
"5" - 3;        // 2     — os outros operadores aritméticos convertem para número
"5" * "2";      // 10
"10" / "4";     // 2.5
true + 1;       // 2     — true vira 1
null + 1;       // 1     — null vira 0
undefined + 1;  // NaN   — undefined vira NaN
"3" + 4 + 5;    // "345" — da esquerda para a direita: "3" + 4 = "34", "34" + 5 = "345"
3 + 4 + "5";    // "75"  — 3 + 4 = 7 (número), 7 + "5" = "75"
```

A regra de ouro: **o `+` prefere texto; os outros preferem número.** Se um dos lados do `+` é string, o resultado é string.

### `==` e `===`

Existem dois operadores de igualdade. O `==` (igualdade **frouxa**) converte os tipos antes de comparar; o `===` (igualdade **estrita**) compara valor **e** tipo, sem converter nada.

```js
5 == "5";             // true  — "5" vira 5
5 === "5";            // false — tipos diferentes
null == undefined;    // true
null === undefined;   // false
NaN === NaN;          // false — NaN não é igual a nada, nem a si mesmo
0 == "";              // true  — "" vira 0
0 == "0";             // true
"" == "0";            // false — o == nem é transitivo!
[] == false;          // true
null == 0;            // false
```

Use **sempre** `===` e `!==`. A coerção do `==` produz resultados bizarros e elimina uma classe inteira de bugs quando abandonada. Se você precisa comparar um número que chegou como texto, converta primeiro (`Number(entrada) === 5`), não relaxe a comparação.

### Falsy e truthy

Quando JavaScript precisa de um booleano — em um `if`, em um `!`, em um `Boolean()` —, ele converte o valor. Apenas **oito** valores viram `false`; todos os outros viram `true`.

Valores **falsy**: `false`, `0`, `-0`, `0n`, `""` (string vazia), `null`, `undefined`, `NaN`.

Todo o resto é **truthy** — inclusive `"0"`, `"false"`, `" "` (espaço), `[]` e `{}`.

```js
Boolean("false");   // true — é uma string com conteúdo
Boolean("0");       // true
Boolean(" ");       // true — o espaço é conteúdo
Boolean([]);        // true
Boolean({});        // true
Boolean(0);         // false
Boolean("");        // false
Boolean(NaN);       // false
```

> **📌 Vale gravar**
> A lista dos oito valores falsy e a diferença entre `==` e `===` aparecem em toda entrevista técnica de front-end. Decore a lista e saiba explicar por que `"0"` é truthy (é uma string não vazia) enquanto `0` é falsy.

## 8. Lendo erros no Console

Todo erro de JavaScript aparece em vermelho no Console, com três partes: o **tipo** do erro, a **mensagem** e o **local** (arquivo e linha). Aprender a ler as três é metade da depuração.

```text
Uncaught ReferenceError: inscrito is not defined
    at app.js:12:13
```

- **`ReferenceError`** — você usou um nome que não existe. Quase sempre é um erro de digitação (`inscrito` em vez de `inscritos`) ou uma variável usada antes de ser declarada.
- **`TypeError`** — o valor existe, mas não é do tipo que a operação exige: reatribuir uma `const`, chamar algo que não é função, ler uma propriedade de `null`.
- **`SyntaxError`** — o navegador nem começou a executar; o arquivo tem um erro de escrita. Aspa não fechada, parêntese sobrando, vírgula faltando.
- **`RangeError`** — um número fora da faixa permitida (por exemplo, `(1).toFixed(200)`).

O `app.js:12:13` diz: arquivo `app.js`, linha 12, coluna 13. Clique nesse link: o DevTools abre a aba Sources exatamente naquela linha.

```js
// SyntaxError — a aspa nunca fecha
const nome = "Ana;
// Uncaught SyntaxError: Invalid or unexpected token

// ReferenceError — a variável se chama nome, não nomes
console.log(nomes);
// Uncaught ReferenceError: nomes is not defined

// TypeError — reatribuição de const
const total = 10;
total = 20;
// Uncaught TypeError: Assignment to constant variable.

// TypeError — chamar algo que não é função
const idade = 20;
idade();
// Uncaught TypeError: idade is not a function
```

Um `SyntaxError` impede **todo** o arquivo de rodar, mesmo as linhas corretas. Se nada acontece e o Console mostra um erro de sintaxe, corrija-o primeiro — o resto do script só será avaliado depois.

## 💻 Mão na massa — O site do evento ganha um script

O site da Semana Acadêmica de Sistemas de Informação tem cinco páginas prontas em HTML e CSS. Hoje ele recebe dois arquivos JavaScript: um compartilhado por todas as páginas e um só para a página de inscrição, que passa a calcular sozinha as vagas restantes.

### Passo 1 — criar `js/app.js` e incluí-lo em todas as páginas

A pasta `js/` já existe desde a Aula 08, quando você colou ali o `menu.js` do hambúrguer, e na Aula 09 ela ganhou o `efeitos.js` do `IntersectionObserver`. Hoje entra o terceiro arquivo: `js/app.js`, o script compartilhado por todas as páginas.

Inclua-o no `<head>` das **cinco** páginas, sempre com `defer`, logo após a folha de estilo — e **sem apagar** os dois `<script>` que já estavam lá:

**Arquivo:** `index.html` (repita o mesmo `<head>` em `programacao.html`, `inscricao.html`, `palestrantes.html` e `contato.html`, trocando só o `<title>`)

```html
<!DOCTYPE html>
<html lang="pt-BR">
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
  <script src="js/efeitos.js" defer></script>
  <script src="js/app.js" defer></script>
</head>
```

O `efeitos.js` (Aula 09) foi incluído só em `index.html`; nas outras quatro páginas ficam apenas `menu.js` e `app.js`. A ordem entre eles não importa hoje — nenhum depende do outro —, mas a partir da Aula 12 vai importar muito, e é por isso que os três estão declarados com `defer` no `<head>`, e não espalhados pelo `<body>`.

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
    ├── menu.js       (Aula 08)
    ├── efeitos.js    (Aula 09)
    └── app.js        (hoje)
```

### Passo 2 — a mensagem de boas-vindas e os dados do evento

**Arquivo:** `js/app.js`

```js
// app.js — carregado por todas as páginas do site do evento

// Dados gerais do evento. Por enquanto vivem aqui; na Aula 12 viram
// arrays e objetos, e no Nível 2 virão de uma API.
const NOME_EVENTO = "Semana Acadêmica de Sistemas de Informação";
const EDICAO = 12;
const LOCAL_EVENTO = "UNEMAT — Campus Sinop";
const TRILHAS = "Desenvolvimento Web, Dados, Segurança";

console.log(`Bem-vindo à ${EDICAO}ª ${NOME_EVENTO}!`);
console.info("Página atual:", document.title);

console.group("Dados do evento");
console.log("Local:", LOCAL_EVENTO);
console.log("Trilhas:", TRILHAS);
console.log("Tipo de EDICAO:", typeof EDICAO);
console.log("Tipo de NOME_EVENTO:", typeof NOME_EVENTO);
console.groupEnd();

console.table([
  { pagina: "Início", arquivo: "index.html" },
  { pagina: "Programação", arquivo: "programacao.html" },
  { pagina: "Inscrição", arquivo: "inscricao.html" },
  { pagina: "Palestrantes", arquivo: "palestrantes.html" },
  { pagina: "Contato", arquivo: "contato.html" },
]);
```

Salve, abra qualquer página no Live Server e confira o Console: a saudação, o grupo com os dados e a tabela devem aparecer. Navegue para outra página — o script roda de novo, com o `document.title` correto.

### Passo 3 — o cálculo de vagas na página de inscrição

A página de inscrição tem, em algum lugar, uma frase como "Restam 33 vagas". Esse número foi digitado à mão. Agora ele será calculado. Localize (ou crie) o parágrafo e dê `id` aos números:

**Arquivo:** `inscricao.html` (trecho dentro do `<main>`, antes do formulário)

```html
<section class="vagas" aria-live="polite">
  <h2>Vagas</h2>
  <p>
    Restam <strong id="vagas-restantes">—</strong> de
    <span id="vagas-totais">—</span> vagas
    (<span id="percentual-ocupacao">—</span>% ocupadas).
  </p>
</section>
```

Os travessões são o conteúdo "enquanto o script não roda" — se o JavaScript falhar, o visitante vê um traço, não um número errado.

Inclua um segundo script **só nesta página**, depois do `app.js`:

**Arquivo:** `inscricao.html` (trecho do `<head>`)

```html
<link rel="stylesheet" href="css/estilo.css">
<script src="js/app.js" defer></script>
<script src="js/inscricao.js" defer></script>
```

**Arquivo:** `js/inscricao.js`

```js
// inscricao.js — carregado apenas por inscricao.html

const VAGAS_TOTAIS = 120;
let inscritos = 87; // let: este número vai mudar quando o formulário funcionar (Aula 14)

const vagasRestantes = VAGAS_TOTAIS - inscritos;
const percentualOcupacao = (inscritos / VAGAS_TOTAIS) * 100;

console.group("Vagas");
console.log("Totais:", VAGAS_TOTAIS);
console.log("Inscritos:", inscritos);
console.log("Restantes:", vagasRestantes);
console.log("Ocupação bruta:", percentualOcupacao);              // 72.5
console.log("Ocupação formatada:", percentualOcupacao.toFixed(1)); // "72.5" (string)
console.groupEnd();

// Sanidade: se alguém digitar mais inscritos do que vagas, o console avisa
console.assert(vagasRestantes >= 0, "Há mais inscritos do que vagas!");

// Escreve os valores na página (detalhes na Aula 13)
document.querySelector("#vagas-restantes").textContent = vagasRestantes;
document.querySelector("#vagas-totais").textContent = VAGAS_TOTAIS;
document.querySelector("#percentual-ocupacao").textContent = percentualOcupacao.toFixed(1);

console.log(`Resumo: ${inscritos} inscritos, ${vagasRestantes} vagas livres.`);
```

### Passo 4 — um toque de estilo para o número

**Arquivo:** `css/estilo.css` (acrescente ao fim, antes do bloco `prefers-reduced-motion`)

```css
/* ===== Vagas (Aula 10) ===== */
.vagas {
  background: var(--cor-fundo-destaque);
  border-left: 4px solid var(--cor-primaria);
  padding: var(--espaco-medio);
  border-radius: var(--raio-borda);
}

.vagas strong {
  font-size: 1.5em;
  color: var(--cor-primaria);
}
```

Os nomes das variáveis são os do sistema de design que você montou na Aula 06 (`--espaco-medio`, `--raio-borda`, `--cor-primaria`). A única nova é `--cor-fundo-destaque` — declare-a no `:root`, junto das outras, em vez de escrever a cor solta aqui.

### Como testar

1. Abra `inscricao.html` no Live Server. A frase deve mostrar **33** de **120** vagas (**72.5**% ocupadas), sem travessões.
2. No Console, confira a saudação do `app.js`, o grupo "Vagas" e o resumo. Nenhuma linha vermelha.
3. Mude `inscritos` para `130`, salve e recarregue: o Console mostra `Assertion failed: Há mais inscritos do que vagas!` e a página exibe `-10`. Volte para `87`.
4. Abra `index.html`: só a saudação e a tabela aparecem — o `inscricao.js` não é carregado aqui, então não há erro de elemento inexistente.
5. Tire o `defer` de `inscricao.js`, recarregue e observe o `TypeError`. Devolva o `defer`.

Resultado esperado: a página de inscrição calcula as vagas sozinha; trocar um único número no `.js` atualiza os três valores na tela.

## 🧪 Laboratório

Os exercícios do Nível B pedem **funções** — a sintaxe completa é assunto da Aula 13. Por ora, copie este esqueleto e preencha o corpo:

```js
function nomeDaFuncao(parametro) {
  // cálculos aqui
  return resultado; // o valor devolvido a quem chamou
}

console.log(nomeDaFuncao(10)); // chamada: o argumento 10 entra em parametro
```

### Nível A — Fixação

**A1.** Qual o resultado e por quê: `5 == "5"`, `5 === "5"`, `null == undefined`, `null === undefined`, `NaN === NaN`? Confirme cada resposta no Console antes de escrever a justificativa.

**A2.** Liste todos os valores falsy do JavaScript. Depois, explique por que `"0"` e `[]` não estão na lista.

**A3.** Reescreva com template literal: `"Aluno: " + nome + " - Média: " + media`.

**A4.** Explique a diferença entre `defer` e `async` em uma tag `<script>`. Em qual situação `async` seria aceitável?

**A5.** O que retorna `typeof null`? Por quê? Como testar corretamente se uma variável vale `null`?

**A6.** Onde a tag `<script>` deve ficar e por quê? Cite as duas alternativas que funcionam e diga qual é a preferida.

**A7.** Qual a diferença entre `console.log`, `console.table` e `console.error`? Dê um exemplo de dado que fica melhor em `console.table`.

**A8.** Por que `alert` e `prompt` não são adequados em aplicações reais? Cite três motivos.

**A9.** O que a aba Sources do DevTools permite fazer que o `console.log` não permite?

**A10.** Qual a saída de cada linha? Anote sua previsão e só depois teste no Console.

```js
console.log("2" + 2);
console.log("2" - 2);
console.log(2 + 2 + "2");
console.log("2" + 2 + 2);
console.log(typeof (1 + "1"));
console.log(Number("") + 1);
console.log("10" < "9");
```

**A11.** O trecho abaixo tem três erros, um de cada tipo (`SyntaxError`, `ReferenceError`, `TypeError`). Encontre-os sem rodar; depois rode e compare com as mensagens do Console.

```js
const evento = "Semana Acadêmica;
const vagas = 120;
vagas = 100;
console.log(nomeEvento, vagas);
```

### Nível B — Aplicação

**B1.** Escreva `formatarMoeda(valor)` que converta `1234.5` em `"R$ 1.234,50"` usando só `toFixed`, `split`, `replace` e `padStart`. Depois refaça com `Intl.NumberFormat` e compare o resultado dos dois com `===`.

Resultado esperado: `formatarMoeda(1234.5)` devolve `"R$ 1.234,50"`; `formatarMoeda(7)` devolve `"R$ 7,00"`; `formatarMoeda(1000000)` devolve `"R$ 1.000.000,00"`.

<details><summary>Dica</summary>

`valor.toFixed(2)` dá `"1234.50"`; `split(".")` separa inteiro e centavos. Para os pontos de milhar sem laço, comece resolvendo até 999.999 (um ponto só) e observe o que falta. Para a versão com `Intl`: `new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(valor)`. A comparação com `===` pode dar `false` mesmo com textos "iguais" — o `Intl` usa um espaço especial (não separável, código U+00A0) entre `R$` e o número. Inspecione com `.charCodeAt(2)`.
</details>

**B2.** Escreva um script que, ao carregar a página, exiba no Console: a data e a hora formatadas em pt-BR, o tamanho da janela (largura × altura), o navegador em uso e uma tabela com cinco produtos (nome, preço, estoque).

Resultado esperado: quatro blocos no Console; a data no formato "dia/mês/ano", o tamanho como `1366 x 768` (varia por máquina), o texto de `navigator.userAgent` e uma `console.table` com cinco linhas.

<details><summary>Dica</summary>

`new Date().toLocaleDateString("pt-BR")` e `new Date().toLocaleTimeString("pt-BR")` formatam data e hora; `window.innerWidth` e `window.innerHeight` dão o tamanho; `navigator.userAgent` identifica o navegador. Redimensione a janela e recarregue para ver os números mudarem.
</details>

**B3.** Crie um arquivo `tipos.js` que demonstre, com `console.table`, o resultado de `typeof` para dez valores diferentes, e escreva um comentário explicando cada resultado inesperado.

Resultado esperado: uma tabela com colunas `valor`, `tipo` e dez linhas, incluindo `null`, `NaN`, `[]`, `function () {}` e `10n`; pelo menos três comentários explicando resultados surpreendentes.

<details><summary>Dica</summary>

Monte um array de objetos no formato `{ valor: String(x), tipo: typeof x }` — o `String(x)` evita que o `console.table` tente expandir arrays e funções. Os resultados inesperados a comentar: `typeof null`, `typeof NaN`, `typeof []` e `typeof function () {}`.
</details>

**B4.** Escreva `descreverConversao(entrada)` que receba uma string e devolva, em uma única frase montada com template literal, o resultado de `Number(entrada)`, `parseInt(entrada)` e `parseFloat(entrada)`, dizendo qual dos três é `NaN`.

Resultado esperado: `descreverConversao("42px")` devolve `"Number: NaN | parseInt: 42 | parseFloat: 42 | NaN em: Number"`; `descreverConversao("3.9kg")` devolve `"Number: NaN | parseInt: 3 | parseFloat: 3.9 | NaN em: Number"`; `descreverConversao("abc")` indica NaN nos três.

<details><summary>Dica</summary>

`Number.isNaN(x)` diz se `x` é `NaN`. Monte a lista de quem deu `NaN` concatenando strings condicionalmente com o ternário `condicao ? "Number " : ""` — a Aula 11 formaliza esse operador.
</details>

### Nível C — Desafio

**C1.** Crie `js/diagnostico.js` e inclua-o (com `defer`) em todas as páginas do site do evento. Ao carregar, o script deve imprimir um único `console.group` chamado "Diagnóstico" com: o caminho da página (`location.pathname`), o título, o idioma do navegador (`navigator.language`), se está online (`navigator.onLine`), a largura da janela classificada como texto (`"estreita"` abaixo de 600 px, `"média"` até 1024 px, `"larga"` acima — use ternários encadeados) e o tempo, em milissegundos, que o próprio script levou para montar tudo isso (`console.time`/`console.timeEnd`). Ao fim, remova o arquivo das páginas — ele foi só um exercício.

<details><summary>Dica</summary>

Chame `console.time("diagnostico")` na primeira linha e `console.timeEnd("diagnostico")` na última. Para a classificação: `const largura = window.innerWidth; const faixa = largura < 600 ? "estreita" : largura <= 1024 ? "média" : "larga";`.
</details>

## 🏆 Desafios

### ⭐ Adivinhe a saída: a coerção posta à prova
Tags: javascript, investigacao

Você acabou de ver que `"5" + 3` é `"53"` e `"5" - 3` é `2`. Alguém afirma que "com prática dá para prever qualquer coerção sem testar". Vamos ver. Abaixo estão doze expressões; escreva a sua previsão para cada uma **antes** de digitar no Console, depois confira e conte os acertos. Cada erro é uma regra que você ainda não internalizou — anote-a.

```js
[] + [];
[] + {};
[1, 2] + [3];
"b" + "a" + +"a" + "a";
true + true;
"3" * "4";
"3" + "4";
1 + null;
1 + undefined;
"" == 0;
"0" == false;
null == false;
```

**Critérios de pronto**

- Um arquivo `coercao.js` com as doze expressões, cada uma precedida por um comentário com a sua previsão e seguida por um `console.log` que mostra o resultado real.
- Ao lado de cada expressão errada, um comentário de uma linha explicando a regra que você não conhecia.
- Uma linha final no arquivo com a contagem: `// Acertos: N de 12`.
- Nenhum `==` sobreviveu em **nenhum** dos seus arquivos `.js` após este exercício — busque no VS Code com <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>F</kbd> e troque todos por `===`.

<details><summary>Pistas</summary>

1. Procure "Equality comparisons and sameness" na MDN e leia a tabela de `==`.
2. Um array vira string com `join(",")` antes de qualquer `+`; um objeto comum vira `"[object Object]"`.
3. O `+` unário (o `+"a"`) força conversão para número — e `"a"` não é um número.
4. `null == false` é `false` porque `null` só é `==` a `undefined` e a ele mesmo; a regra dos falsy não vale para o `==`.
</details>

### ⭐⭐ Caça ao bug: cinco erros em um script de 20 linhas
Tags: javascript, bug, devtools

O script abaixo deveria mostrar, na página de inscrição, o nome do evento e as vagas restantes. Ele tem **cinco** defeitos: um impede o arquivo inteiro de rodar, um faz a página quebrar antes de o HTML existir, um produz `NaN`, um produz um `TypeError` e um é silencioso — o resultado aparece, mas está errado. Encontre os cinco usando só as mensagens do Console e a aba Sources, e explique cada um.

**Arquivo:** `bug.html`

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Caça ao bug</title>
  <script src="js/bug.js"></script>
</head>
<body>
  <h1 id="titulo">—</h1>
  <p>Restam <strong id="vagas">—</strong> vagas.</p>
</body>
</html>
```

**Arquivo:** `js/bug.js`

```js
const NOME_EVENTO = "Semana Acadêmica;
const VAGAS_TOTAIS = "120";
const inscritos = 87;

const vagasRestantes = VAGAS_TOTAIS - inscritos;
const percentual = inscritos / VAGAS_TOTAIS * 100;

console.log("Percentual: " + percentual.toFixed(1) + "%");

const resumo = "Restam " + vagasRestantes + " vagas de " + VAGAS_TOTAIS;
document.querySelector("#titulo").textContent = NOME_EVENTO;
document.querySelector("#vagas").textContent = vagasRestantes;

const totalComExtras = VAGAS_TOTAIS + 10;
console.log("Total com vagas extras:", totalComExtras);

NOME_EVENTO = NOME_EVENTO.toUpperCase();
console.log(resumo);
```

**Critérios de pronto**

- A página mostra o nome do evento no `<h1>` e `33` no `<strong>`, sem nenhuma linha vermelha no Console.
- O `console.log` de "Total com vagas extras" mostra `130`, não `"12010"`.
- Um arquivo `bugs.md` com uma tabela de cinco linhas: sintoma observado (mensagem literal do Console ou valor errado), causa e correção.
- O script continua com `const` em tudo que não muda — corrigir não é trocar tudo por `let`.

<details><summary>Pistas</summary>

1. Corrija primeiro o erro que o Console mostra como `SyntaxError` — enquanto ele existir, nenhuma outra linha roda e você não verá os demais.
2. O segundo erro não está no `.js`: releia a tabela de `defer` da §2.
3. Passe o mouse sobre `VAGAS_TOTAIS` na aba Sources com a execução pausada e olhe o tipo do valor. Onde o `-` funciona e o `+` não?
4. O erro silencioso é o mesmo de `"5" + 3`; o `TypeError` aparece na última linha por causa de uma palavra-chave da §4.
</details>

### ⭐⭐⭐ Dinheiro não cabe em ponto flutuante
Tags: javascript, investigacao, bug

Um sistema de inscrição cobra R$ 0,10 de taxa por SMS e envia três. No Console, `0.1 * 3` dá `0.30000000000000004`; o cliente vê "R$ 0,30000000000000004" no boleto e liga furioso. Bancos, lojas e sistemas de ingressos não guardam dinheiro em ponto flutuante — guardam **centavos inteiros**. Investigue por que `0.1 + 0.2 !== 0.3`, descubra pelo menos três operações do dia a dia que quebram com decimais, e escreva `js/dinheiro.js`, um script que representa valores em centavos e formata com `Intl.NumberFormat`.

**Critérios de pronto**

- Um comentário de até dez linhas no topo do arquivo explicando, com suas palavras, por que `0.1` não tem representação exata em binário (cite a quantidade de bits da mantissa no IEEE 754).
- Três pares de `console.log` mostrando uma conta que **erra** em ponto flutuante e a mesma conta **correta** em centavos (por exemplo: `0.1 + 0.2`, `1.005.toFixed(2)`, `19.99 * 3`).
- Uma demonstração de que `Math.abs(a - b) < Number.EPSILON` compara decimais com segurança quando centavos não são opção.
- A formatação final usa `Intl.NumberFormat("pt-BR", …)` a partir de um inteiro em centavos, e o resultado de `formatar(1999 * 3)` é `"R$ 59,97"`.

<details><summary>Pistas</summary>

1. Leia a página `https://0.30000000000000004.com/` — ela mostra o mesmo problema em dezenas de linguagens; não é um defeito do JavaScript.
2. No Console, `(0.1).toString(2)` mostra a representação binária: repare que é uma dízima periódica, como 1/3 em decimal.
3. `(1.005).toFixed(2)` dá `"1.00"`, não `"1.01"`, porque `1.005` é, na verdade, `1.00499999999999989…` — teste `(1.005).toPrecision(20)`.
4. Para formatar centavos: divida por 100 só na hora de exibir (`centavos / 100`) e entregue esse número ao `format` do `Intl.NumberFormat`.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `Uncaught TypeError: Cannot read properties of null (reading 'textContent')` | script no `<head>` sem `defer`: o elemento ainda não existe quando o código roda | adicione `defer` à tag `<script>` (ou confira se o `id` no HTML é exatamente o mesmo do seletor) |
| `GET http://127.0.0.1:5500/js/app.js net::ERR_ABORTED 404 (Not Found)` | caminho do `src` errado, pasta com outro nome ou arquivo salvo em outro lugar | confira o caminho relativo à página HTML; abra a aba Network e veja qual URL foi pedida |
| `Uncaught ReferenceError: inscrito is not defined` | nome digitado errado, variável nunca declarada ou declarada em outro arquivo que não foi incluído | corrija a grafia; declare com `const`/`let`; confira a ordem dos `<script>` |
| `Uncaught TypeError: Assignment to constant variable.` | tentativa de dar novo valor a uma `const` | se o valor precisa mudar, declare com `let`; se não, remova a reatribuição |
| `Uncaught SyntaxError: Invalid or unexpected token` | aspa não fechada, caractere estranho colado do Word, crase no lugar de aspa | leia a linha indicada; o VS Code sublinha o ponto exato |
| `Uncaught SyntaxError: missing ) after argument list` | parêntese ou vírgula faltando em uma chamada como `console.log("a" "b")` | feche o parêntese ou coloque a vírgula entre os argumentos |
| `Uncaught ReferenceError: Cannot access 'total' before initialization` | a variável foi usada em uma linha acima da linha em que foi declarada com `let`/`const` | declare antes de usar; a Aula 11 explica a "zona morta temporal" |
| A página mostra `NaN` no lugar de um número | uma conta usou um valor que não é número: string com letras, `undefined`, campo vazio | converta com `Number()` antes de calcular e verifique com `Number.isNaN()` |
| O console mostra `[object Object]` | um objeto foi concatenado com string usando `+` | use vírgula no `console.log` ou `JSON.stringify(objeto)` |
| Nada acontece e nenhum erro aparece | o script nem foi carregado (cache do navegador, Live Server parado) ou um `SyntaxError` em outro arquivo silenciou tudo | coloque um `console.log("carregou")` na primeira linha; recarregue com <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>R</kbd> |

## 🏠 Para praticar depois da aula (1 h)

**Parte 1 — Leitura (20 min).** FLANAGAN, D. *JavaScript: o guia definitivo*, capítulos introdutórios sobre tipos, valores e variáveis. STEFANOV, S. *Padrões JavaScript*, capítulo de fundamentos (o trecho sobre variáveis globais e `var`). Na MDN, leia "Tipos e estruturas de dados do JavaScript" (link em Para aprofundar).

**Parte 2 — Produção (30 min).** Hoje fecha o **Marco 2** (instruções completas logo abaixo). Além dele, produza o exercício **B4** em um arquivo `conversao.js` com pelo menos cinco casos de teste no Console. No seu **projeto autoral**: crie a pasta `js`, inclua `js/app.js` com `defer` em todas as páginas e imprima no Console, com `console.table`, pelo menos cinco dados do seu domínio (por exemplo, cinco plantas do catálogo, cinco quadras da agenda). Em uma das páginas, calcule e exiba um número derivado de constantes — o equivalente às "vagas restantes" do site do evento.

**Critério de pronto:** todas as páginas do projeto autoral carregam `js/app.js` sem erro no Console; uma página exibe um valor calculado por JavaScript no lugar de um número digitado no HTML; o `conversao.js` roda sem erros e mostra os cinco casos.

**Parte 3 — Discussão (10 min).** Em texto próprio — ou no fórum da turma, se você está cursando esta trilha em grupo —: traga um resultado surpreendente de comparação ou de operação em JavaScript (diferente dos que apareceram nesta aula), explique tecnicamente por que ele ocorre e como evitá-lo.

**Guarde no seu repositório:** commit + push (ou a pasta do projeto).

## ✅ Checkpoint do projeto

Ao fim desta aula, o repositório do seu projeto autoral deve ter:

- [ ] Pasta `js/` com `app.js`, incluído por `<script src="js/app.js" defer>` no `<head>` de **todas** as páginas.
- [ ] Nenhum erro vermelho no Console em nenhuma página.
- [ ] Um `console.table` com dados do seu domínio ao carregar qualquer página.
- [ ] Pelo menos uma página com um valor calculado em JavaScript (não digitado no HTML), com o HTML mostrando um travessão quando o script não roda.
- [ ] Zero ocorrências de `var` e de `==` nos seus arquivos `.js`.
- [ ] Marco 2 fechado.

## 🎓 Marco do projeto — Unidade 2

**Escopo.** Ao fim da Unidade 2, o **mesmo site do Marco 1** (com as correções apontadas já aplicadas) precisa estar completamente estilizado: layout, menu, responsividade em três larguras e animações.

**Requisitos.**

| # | Requisito | Onde foi estudado |
|---|---|---|
| 1 | CSS externo, em arquivo único, organizado por seções comentadas | Aula 05 |
| 2 | Reset ou normalização no topo da folha, com `box-sizing: border-box` global | Aulas 05 e 06 |
| 3 | Sistema de design em variáveis CSS: cores, espaçamentos, tipografia e raios | Aula 06 |
| 4 | Uso demonstrado de seletores de classe, atributo, combinadores, pseudoclasses e pseudoelementos | Aula 06 |
| 5 | Layout principal com CSS Grid e componentes internos com Flexbox | Aula 07 |
| 6 | Menu de navegação estilizado, com item ativo destacado e link de salto para o conteúdo | Aula 07 |
| 7 | Responsividade *mobile first*, com no mínimo três breakpoints | Aula 08 |
| 8 | Menu responsivo funcional em telas estreitas | Aula 08 |
| 9 | Imagens e tipografia fluidas | Aula 08 |
| 10 | Estados visuais em todos os elementos interativos: `:hover`, `:focus-visible`, `:active`, `:disabled` | Aulas 06 e 09 |
| 11 | Transições nos elementos interativos e ao menos uma animação com `@keyframes` que cumpra uma função | Aula 09 |
| 12 | Bloco `prefers-reduced-motion` ao final da folha | Aula 09 |
| 13 | Contraste WCAG AA em todos os textos, verificado e documentado em `contraste.md` | Aula 06 |
| 14 | Formulário estilizado com indicação visual de campo inválido que não dependa só de cor | Aulas 06 e 09 |
| 15 | Sem `float` para estrutura e sem `!important` (exceto dentro do bloco `prefers-reduced-motion`) | Aulas 07 e 09 |

Frameworks CSS (Bootstrap, Tailwind e similares) não entram aqui — o objetivo deste marco é demonstrar domínio do CSS puro.

**Checklist de qualidade.**

- Folha de estilo organizada e sistema de design coerente (variáveis, não valores soltos).
- Domínio de seletores e especificidade — nenhum `!important` usado como atalho.
- Layout com Grid e Flexbox aplicados onde cada um faz sentido, não ao acaso.
- Responsividade real nas três larguras, testada em dispositivo de verdade, não só no simulador.
- Estados visuais completos e contraste acessível em todo texto.
- Transições e animações com propósito, nunca só para "parecer moderno".
- Coerência visual entre as cinco páginas e capricho geral no acabamento.

**Como saber que está pronto.**

- Rode o Lighthouse (modo mobile) em cada página: Acessibilidade e Boas práticas ≥ 90.
- No DevTools, alterne `prefers-reduced-motion: reduce` e `prefers-color-scheme: dark` e confira que nada quebra.
- Redimensione a janela (ou use o modo *Responsive*) em 360 px, 768 px e 1440 px: nenhuma rolagem horizontal, nenhum texto cortado.
- Verifique `contraste.md` contra o WebAIM: todo par texto × fundo em AA.
- Use IA para tirar dúvida ou revisar sintaxe — não para gerar a folha de estilo inteira. Se você não souber explicar por que escolheu Grid em vez de Flexbox num trecho, ainda não é seu.

## 📚 Para aprofundar

- MDN — Guia JavaScript: <https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Guide> — leia "Introdução" e "Gramática e tipos".
- MDN — Aprendendo desenvolvimento web, módulo de scripting: <https://developer.mozilla.org/pt-BR/docs/Learn_web_development/Core/Scripting> — os dois primeiros artigos cobrem exatamente esta aula.
- MDN — Tipos e estruturas de dados: <https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Data_structures> — referência dos primitivos.
- MDN — O elemento `<script>`: <https://developer.mozilla.org/pt-BR/docs/Web/HTML/Element/script> — os atributos `defer` e `async` em detalhe.
- MDN — `console`: <https://developer.mozilla.org/pt-BR/docs/Web/API/console> — todos os métodos, com exemplos.
- MDN — `Intl.NumberFormat`: <https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat> — para o exercício B1.
- javascript.info: <https://javascript.info/> — capítulos "Hello, world!", "Variables", "Data types" e "Type Conversions"; é o melhor tutorial gratuito da linguagem.
- freeCodeCamp em português — Algoritmos e estruturas de dados em JavaScript: <https://www.freecodecamp.org/portuguese/learn/javascript-algorithms-and-data-structures> — exercícios interativos; faça a primeira seção.
- Chrome DevTools — depurando JavaScript: <https://developer.chrome.com/docs/devtools/javascript?hl=pt-br> — o tutorial oficial de breakpoints.
- Especificação ECMAScript: <https://tc39.es/ecma262/> — só para curiosidade; é onde a linguagem é definida.
- FLANAGAN, David. *JavaScript: o guia definitivo*. Bookman, 2014 — capítulos 1 a 3.
- STEFANOV, Stoyan. *Padrões JavaScript*. Novatec, 2010 — capítulo 2 (fundamentos).
- OLIVEIRA, C.; ZANETTI, H. *JavaScript Descomplicado*. Saraiva, 2020 — capítulos iniciais.

Na próxima aula, o JavaScript começa a decidir: você vai aprofundar escopo e `const`/`let`, dominar os operadores aritméticos, de comparação e lógicos (incluindo `??` e `?.`) e escrever as primeiras estruturas condicionais — e a página de inscrição do evento passará a mostrar "Últimas vagas!" sozinha.
