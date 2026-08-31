# Aula 13 — Funções e eventos

> **Nível 1 — Introdução ao Desenvolvimento Web** · Unidade 3: JavaScript e interatividade
> WebLab · UNEMAT Sinop · Prof. Ivan Luiz Pedroso Pires
> **Carga:** 3 aulas de 50 min (presencial) + 1 h (assíncrona)

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Escrever funções nas três formas (declaração, expressão e arrow) e escolher a adequada para cada situação.
- Usar parâmetros padrão, `rest`, `spread` e objetos como parâmetro, respeitando o escopo de bloco de `let` e `const`.
- Explicar o que é o DOM e por que ele não é o mesmo que o arquivo HTML.
- Selecionar, ler, alterar, criar e remover elementos com `querySelector`, `textContent`, `classList`, `dataset` e `createElement`.
- Renderizar uma lista na tela a partir de um array de objetos, tratando o estado vazio e evitando XSS.
- Registrar tratadores de evento com `addEventListener`, usar o objeto `event` e explicar as fases de propagação.
- Aplicar delegação de eventos em listas dinâmicas e controlar a frequência de eventos com `debounce` e `throttle`.

## 📋 Pré-requisitos

- [ ] VS Code com a extensão Live Server funcionando e o DevTools do navegador aberto na aba **Console**.
- [ ] O site do evento acadêmico com as cinco páginas estilizadas e responsivas (Unidade 2) e o `js/app.js` ligado com `defer`.
- [ ] Conforto com arrays e objetos: `forEach`, `map`, `filter`, `find` e a notação `{ chave: valor }` (Aula 12).
- [ ] Seletores CSS (Aula 06): `#id`, `.classe`, `elemento`, `[atributo]`, descendente e `:checked` — `querySelector` usa exatamente essa sintaxe.

> Na aula passada você aprendeu a controlar o fluxo do programa (condicionais e laços) e a organizar dados em arrays e objetos — mas tudo aconteceu no console. Hoje o JavaScript sai do console e entra na página: você vai escrever funções reutilizáveis, manipular a árvore do documento e reagir a cliques, teclas e envios de formulário. Na próxima aula, esse mesmo conhecimento valida o formulário de inscrição e cria a busca da programação.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Funções: declaração, expressão, arrow, parâmetros, escopo, funções de ordem superior e boas práticas |
| 2 | 50 min | DOM: seleção, conteúdo, atributos, classes, criação de elementos, navegação e renderização de listas |
| 3 | 50 min | Eventos: modelo, tipos, objeto `event`, propagação, delegação, debounce; Mão na massa no site do evento |

## 1. Funções

Uma função é um bloco de código com nome, que recebe entradas (parâmetros), faz algo e devolve uma saída (`return`). Você já usou funções prontas o semestre inteiro — `console.log`, `alert`, `Number`, `push` — hoje passa a escrever as suas. O motivo é simples: sem funções, todo comportamento repetido vira código copiado e colado, e cada correção precisa ser feita em vários lugares.

### Declaração de função

```js
// js/exemplos-funcoes.js
function calcularMedia(a1, a2, a3) {
  return (a1 + a2 + a3) / 3;
}

const media = calcularMedia(8, 7, 9); // 8
console.log(media);
```

Declarações sofrem **hoisting** (içamento): o motor JavaScript lê o arquivo inteiro antes de executar e "sobe" as declarações de função para o topo. Por isso é possível chamar `calcularMedia` em uma linha acima de onde ela foi escrita. Isso é útil para organizar o arquivo com as funções principais no fim e o "programa" no começo.

### Expressão de função

```js
const calcularMedia = function (a1, a2, a3) {
  return (a1 + a2 + a3) / 3;
};
```

Aqui a função é um **valor** guardado em uma constante. Não sofre hoisting — precisa ser definida antes do uso, como qualquer outra variável.

### Arrow function (ES6)

```js
const calcularMedia = (a1, a2, a3) => (a1 + a2 + a3) / 3;

// Um parâmetro: parênteses opcionais
const dobrar = (n) => n * 2;

// Sem parâmetros
const saudacao = () => "Olá!";

// Corpo com várias linhas exige chaves e return explícito
const classificar = (nota) => {
  if (nota >= 6) return "Aprovado";
  if (nota >= 4) return "Exame";
  return "Reprovado";
};

// Retornando um objeto: envolva em parênteses,
// senão as chaves são lidas como corpo da função
const criarAluno = (nome, nota) => ({ nome, nota });

console.log(dobrar(21));                 // 42
console.log(classificar(5.5));           // "Exame"
console.log(criarAluno("Ana", 9.2));     // { nome: "Ana", nota: 9.2 }
```

> **⚠️ Atenção**
> Arrow functions não têm `this` próprio — herdam o do escopo onde foram criadas. Isso as torna ideais como *callbacks* (funções passadas para `forEach`, `map`, `addEventListener`) e inadequadas como métodos de objeto que precisam acessar o próprio objeto por `this`.

| Forma | Hoisting | `this` próprio | Quando usar |
|---|---|---|---|
| Declaração `function nome() {}` | Sim | Sim | Funções principais do arquivo, chamadas de vários lugares |
| Expressão `const nome = function () {}` | Não | Sim | Raro em código novo; aparece em código antigo |
| Arrow `const nome = () => {}` | Não | Não (herda) | Callbacks, funções curtas, `map`/`filter`/`reduce` |

### Parâmetros

```js
// Valor padrão: usado quando o argumento não é passado (ou é undefined)
function saudar(nome = "visitante", saudacao = "Olá") {
  return `${saudacao}, ${nome}!`;
}
saudar();                   // "Olá, visitante!"
saudar("Ana", "Bom dia");   // "Bom dia, Ana!"

// Rest (...) no parâmetro: número variável de argumentos vira um array
function somar(...numeros) {
  return numeros.reduce((acumulado, n) => acumulado + n, 0);
}
somar(1, 2, 3, 4, 5);       // 15

// Spread (...) na chamada: "espalha" um array como argumentos separados
const notas = [8, 7, 9];
calcularMedia(...notas);    // o mesmo que calcularMedia(8, 7, 9)

// Objeto como parâmetro: argumentos nomeados, em qualquer ordem
function cadastrar({ nome, email, curso = "Não informado" }) {
  return `${nome} | ${email} | ${curso}`;
}
cadastrar({ email: "a@b.com", nome: "Ana" }); // "Ana | a@b.com | Não informado"
```

O último padrão — objeto como parâmetro — resolve um problema real: quando a função tem quatro ou cinco parâmetros, ninguém lembra a ordem. Com um objeto, a chamada se autodocumenta.

### Escopo

```js
const global = "visível em toda parte";

function exemplo() {
  const local = "só dentro desta função";

  if (true) {
    let bloco = "só dentro deste bloco";
    const tambemBloco = "idem";
    var vazado = "vaza para a função inteira"; // por isso não use var
  }

  console.log(bloco);   // ReferenceError: bloco is not defined
  console.log(vazado);  // funciona — comportamento confuso do var
}

console.log(local);     // ReferenceError: local is not defined
```

`let` e `const` têm escopo de **bloco** (`{}`). `var` tem escopo de **função**. Regra: cada variável deve existir no menor escopo possível. Se só é usada dentro do `if`, declare dentro do `if`.

### Funções de ordem superior

Funções que recebem ou retornam outras funções. `map`, `filter` e `reduce` (Aula 12) são exemplos: recebem uma função e a aplicam a cada item. Você também pode criar as suas:

```js
function aplicarDesconto(percentual) {
  return function (preco) {
    return preco * (1 - percentual / 100);
  };
}

const desconto10 = aplicarDesconto(10);
const desconto50 = aplicarDesconto(50);

desconto10(200); // 180
desconto50(200); // 100
```

`aplicarDesconto(10)` devolve uma **nova função** que "lembra" o percentual. Esse "lembrar" tem nome — *closure* — e é o mecanismo por trás do `debounce` que você verá na seção 16.

### Boas práticas

1. **Uma função, uma responsabilidade.** Se o nome tem "e" (`salvarEEnviar`), provavelmente são duas funções.
2. **Nomes são verbos:** `calcularMedia`, `validarEmail`, `formatarData`, `renderizarLista`.
3. **Evite mais de 3–4 parâmetros.** Acima disso, receba um objeto.
4. **Prefira retornar valores a alterar variáveis externas.** Funções puras (mesma entrada → mesma saída, sem efeitos colaterais) são fáceis de testar no console.
5. **Retorne cedo** para reduzir aninhamento:

```js
// Em vez de aninhar três ifs
function processar(dado) {
  if (!dado) return null;
  if (!dado.ativo) return null;
  return dado.valor * 2;
}
```

## 2. O que é o DOM

O **DOM** (*Document Object Model*) é a representação em memória do documento, montada pelo navegador ao interpretar o HTML. Ele expõe o documento como uma **árvore de objetos** que o JavaScript pode ler e modificar.

```html
<!-- exemplo.html -->
<html>
  <body>
    <h1 id="titulo">Olá</h1>
    <ul class="lista">
      <li>Item 1</li>
      <li>Item 2</li>
    </ul>
  </body>
</html>
```

```text
document
└── html
    └── body
        ├── h1#titulo
        │   └── "Olá"              (nó de texto)
        └── ul.lista
            ├── li → "Item 1"
            └── li → "Item 2"
```

Três verdades importantes:

1. **O DOM não é o HTML.** O HTML é o texto-fonte; o DOM é a estrutura viva em memória. Se o JavaScript adicionar elementos, eles existem no DOM sem existir no arquivo `.html`. Por isso "Exibir código-fonte" (<kbd>Ctrl</kbd>+<kbd>U</kbd>) mostra o arquivo original, enquanto a aba **Elements** do DevTools mostra o DOM atual.
2. **Alterar o DOM altera a tela imediatamente.** Não há "salvar" nem "atualizar".
3. **Recarregar a página descarta tudo.** Toda alteração feita por JavaScript some — a menos que seja persistida (você verá `localStorage` na próxima aula).

O objeto de entrada é `document`, que é filho de `window` (o objeto global do navegador — `alert`, `setTimeout` e `location` também vivem nele).

> **🧠 Você sabia?**
> O DOM nasceu de uma guerra. Em 1997, Netscape Navigator 4 e Internet Explorer 4 lançaram, cada um, seu próprio modelo de objetos para "HTML dinâmico" — `document.layers` de um lado, `document.all` do outro — e o mesmo script não rodava nos dois. Programadores escreviam tudo em dobro. O W3C publicou o **DOM Level 1** em 1998 para acabar com isso, e hoje o padrão é mantido pelo WHATWG como o *DOM Living Standard*. O `querySelector` que você vai usar só chegou em 2008, com a especificação Selectors API.

## 3. Seleção de elementos

### Métodos modernos — use estes

```js
// Retorna o PRIMEIRO elemento que casa com o seletor CSS (ou null)
const titulo = document.querySelector("#titulo");
const primeiroItem = document.querySelector(".lista li");
const botao = document.querySelector("button.primario");
const campo = document.querySelector("input[type='email']");

// Retorna TODOS os que casam, como NodeList (mesmo que vazia)
const itens = document.querySelectorAll(".lista li");
const paragrafos = document.querySelectorAll("article p");
```

`querySelector` e `querySelectorAll` aceitam **qualquer seletor CSS** — combinadores, pseudoclasses, seletores de atributo. É por isso que a Aula 06 é pré-requisito desta.

### Métodos clássicos

```js
document.getElementById("titulo");          // sem #
document.getElementsByClassName("lista");   // HTMLCollection AO VIVO
document.getElementsByTagName("li");        // HTMLCollection AO VIVO
document.getElementsByName("turno");        // NodeList
```

| Característica | `querySelectorAll` | `getElementsBy*` |
|---|---|---|
| Retorna | `NodeList` estática | `HTMLCollection` ao vivo |
| Reflete mudanças posteriores no DOM | Não | Sim |
| Tem `forEach` | Sim | Não (precisa converter) |
| Aceita seletor CSS | Sim | Não |

> **⚠️ Atenção**
> A coleção "ao vivo" é uma fonte clássica de bugs: se você remove elementos dentro de um laço que percorre uma `HTMLCollection`, a coleção encolhe durante a iteração e você pula elementos. Prefira `querySelectorAll`.

### Percorrendo o resultado

```js
const itens = document.querySelectorAll("li");

itens.forEach((item) => console.log(item.textContent));

// Se precisar de métodos de array (map, filter, find), converta:
const textos = Array.from(itens).map((i) => i.textContent);
const textos2 = [...itens].map((i) => i.textContent);
```

> **⚠️ Atenção**
> `querySelector` retorna `null` quando não encontra. Chamar algo em `null` gera `TypeError: Cannot read properties of null (reading 'addEventListener')`. Este é o erro mais frequente de quem está aprendendo DOM. Suas duas causas quase sempre são: **(a)** seletor errado (`#menu` quando o id é `menu-principal`); **(b)** script rodando antes de o HTML existir — resolvido com `defer` na tag `<script>`.

> **🔬 Investigue**
> Abra qualquer página, vá à aba **Elements** do DevTools e clique em um elemento. Volte ao **Console** e digite `$0` — o navegador devolve o elemento selecionado. Agora experimente `$0.textContent`, `$0.classList`, `$0.parentElement` e `$0.style.outline = "3px solid red"`. `$0` é o último elemento clicado, `$1` o anterior, e assim por diante. É a forma mais rápida de testar seletores: `$$(".card")` equivale a `document.querySelectorAll(".card")`.

## 4. Lendo e alterando conteúdo

```js
const titulo = document.querySelector("#titulo");

// LEITURA
titulo.textContent; // texto puro, incluindo o de elementos ocultos
titulo.innerText;   // texto como renderizado (respeita CSS, mais lento)
titulo.innerHTML;   // conteúdo HTML como string

// ESCRITA
titulo.textContent = "Novo título";
titulo.innerHTML = "Novo <strong>título</strong>";
```

| Propriedade | Interpreta HTML? | Uso |
|---|---|---|
| `textContent` | Não — tags viram texto literal | Padrão. Use sempre que possível |
| `innerText` | Não | Quando importa o texto visível (respeita `display: none`) |
| `innerHTML` | Sim | Só quando você realmente precisa inserir marcação |

> **⚠️ Atenção — XSS**
> Nunca faça `elemento.innerHTML = dadoDoUsuario`. Se o usuário digitar `<img src=x onerror="alert(document.cookie)">` em um campo e você inserir isso com `innerHTML`, o código dele executa na sua página — para todo mundo que abrir. Isso se chama **Cross-Site Scripting (XSS)** e é uma das vulnerabilidades mais exploradas da Web.
> Regra: dado vindo de usuário → `textContent`. Marcação que você mesmo escreveu → `innerHTML` é aceitável.

## 5. Atributos

```js
const link = document.querySelector("a");

link.getAttribute("href");
link.setAttribute("href", "https://unemat.br");
link.setAttribute("target", "_blank");
link.hasAttribute("download"); // true/false
link.removeAttribute("target");

// Propriedades diretas para atributos comuns
link.href;
link.id;
img.src;
img.alt;
input.value;           // valor atual do campo
input.checked;         // true/false para checkbox/radio
input.disabled = true;
select.value;
```

> **💡 Dica**
> `input.value` é diferente de `input.getAttribute("value")`. O primeiro é o valor **atual** (o que o usuário digitou); o segundo é o valor **inicial** escrito no HTML. Ao trabalhar com formulários, use sempre `.value`.

### `data-*` — atributos personalizados

```html
<button data-id="42" data-acao="excluir" data-nome-produto="Notebook">
  Excluir
</button>
```

```js
const btn = document.querySelector("button");

btn.dataset.id;          // "42" (sempre string!)
btn.dataset.acao;        // "excluir"
btn.dataset.nomeProduto; // "Notebook" — data-nome-produto vira nomeProduto (camelCase)

btn.dataset.status = "ativo"; // cria data-status="ativo" no HTML
```

Atributos `data-*` são a forma padrão de guardar informação de aplicação no HTML. Serão essenciais na delegação de eventos (seção 14) e no CRUD do Boss da Unidade: cada botão de editar/excluir carrega o `data-id` do registro.

## 6. Classes e estilos

### `classList` — a forma correta

```js
const card = document.querySelector(".card");

card.classList.add("ativo");
card.classList.add("destaque", "novo");   // várias de uma vez
card.classList.remove("ativo");
card.classList.toggle("aberto");          // adiciona se não tem, remove se tem
card.classList.toggle("aberto", condicao); // força adicionar (true) ou remover (false)
card.classList.contains("ativo");         // true/false
card.classList.replace("antigo", "novo");
```

> **⚠️ Atenção**
> Evite `card.className = "novo"` — isso substitui **todas** as classes existentes de uma vez.

### Estilos inline

```js
card.style.backgroundColor = "#0b3d5c"; // camelCase, não background-color
card.style.fontSize = "18px";           // sempre com unidade
card.style.display = "none";
card.style.setProperty("--cor-tema", "#e74c3c"); // variáveis CSS

// Leitura do estilo COMPUTADO (o que realmente está aplicado, vindo de qualquer folha)
const estilo = getComputedStyle(card);
estilo.backgroundColor;
estilo.width;
```

> **💡 Dica**
> Prefira trocar classes a manipular `style` diretamente. O CSS fica no CSS, o comportamento fica no JS, e você mantém a separação de responsabilidades que construiu na Unidade 2.

```js
// Espalha estilo pelo JavaScript
el.style.display = "none";
el.style.opacity = "0";

// O CSS define o que é "oculto"; o JS só decide quando
el.classList.add("oculto");
```

```css
/* css/estilo.css */
.oculto {
  display: none;
}
```

## 7. Criando e inserindo elementos

```js
// 1. Criar
const li = document.createElement("li");

// 2. Configurar
li.textContent = "Novo item";
li.classList.add("item");
li.dataset.id = "7";

// 3. Inserir
const lista = document.querySelector("ul");
lista.appendChild(li);               // no fim
lista.append(li, outroLi);           // no fim, aceita vários nós e texto
lista.prepend(li);                   // no início
lista.insertBefore(li, referencia);  // antes de um filho específico

// Inserção posicional em relação a um elemento
elemento.insertAdjacentElement("beforebegin", novo); // antes do elemento
elemento.insertAdjacentElement("afterbegin", novo);  // primeiro filho
elemento.insertAdjacentElement("beforeend", novo);   // último filho
elemento.insertAdjacentElement("afterend", novo);    // depois do elemento

elemento.insertAdjacentHTML("beforeend", "<li>Item</li>"); // com string HTML
```

### Removendo e substituindo

```js
elemento.remove();              // remove a si mesmo
pai.removeChild(filho);         // forma antiga
pai.replaceChild(novo, antigo);
elemento.replaceWith(novo);

lista.innerHTML = "";           // esvazia (rápido e comum)
```

### Clonando

```js
const copia = elemento.cloneNode(true); // true = com descendentes
```

## 8. Navegação entre nós

```js
const item = document.querySelector(".item");

// Para cima
item.parentElement;
item.closest(".card"); // ancestral mais próximo que casa com o seletor (inclui o próprio)

// Para baixo
item.children;           // HTMLCollection de elementos filhos
item.firstElementChild;
item.lastElementChild;
item.querySelector(".titulo"); // busca DENTRO do item

// Para os lados
item.nextElementSibling;
item.previousElementSibling;
```

> **⚠️ Atenção**
> Existem versões sem `Element` no nome (`parentNode`, `firstChild`, `nextSibling`) que consideram **nós de texto** — inclusive espaços e quebras de linha do seu HTML. Isso surpreende: `ul.firstChild` costuma ser um nó de texto vazio, não o primeiro `<li>`. Use sempre as versões com `Element`.

`closest()` é indispensável: em uma lista, ao clicar num botão dentro de um card, `btn.closest(".card")` devolve o card inteiro — mesmo que o clique tenha sido em um ícone dentro do botão.

## 9. Renderizando listas a partir de dados

Este é o padrão central do desenvolvimento front-end e será usado em todas as aulas seguintes: os dados vivem em um **array**; uma função **desenha** a tela a partir dele. Quando os dados mudam, chama-se a função de novo.

```js
// js/produtos.js
const produtos = [
  { id: 1, nome: "Notebook", preco: 3500, categoria: "Informática" },
  { id: 2, nome: "Mouse", preco: 80, categoria: "Periféricos" },
  { id: 3, nome: "Teclado", preco: 150, categoria: "Periféricos" },
];

const container = document.querySelector("#lista-produtos");

function renderizar(lista) {
  container.innerHTML = ""; // 1. limpa

  if (lista.length === 0) {  // 2. estado vazio
    const aviso = document.createElement("p");
    aviso.classList.add("vazio");
    aviso.textContent = "Nenhum produto encontrado.";
    container.appendChild(aviso);
    return;
  }

  lista.forEach((produto) => { // 3. cria um nó por item
    const card = document.createElement("article");
    card.classList.add("card-produto");
    card.dataset.id = produto.id;

    const titulo = document.createElement("h3");
    titulo.textContent = produto.nome; // textContent: seguro contra XSS

    const preco = document.createElement("p");
    preco.classList.add("preco");
    preco.textContent = produto.preco.toLocaleString("pt-BR", {
      style: "currency",
      currency: "BRL",
    });

    const btn = document.createElement("button");
    btn.type = "button";
    btn.textContent = "Excluir";
    btn.dataset.id = produto.id;
    btn.classList.add("btn-excluir");

    card.append(titulo, preco, btn);
    container.appendChild(card);
  });
}

renderizar(produtos);
```

### Versão com template literal

Mais concisa, porém exige cuidado com XSS se os dados vierem do usuário:

```js
function renderizar(lista) {
  container.innerHTML = lista
    .map(
      (p) => `
      <article class="card-produto" data-id="${p.id}">
        <h3>${p.nome}</h3>
        <p class="preco">R$ ${p.preco.toFixed(2)}</p>
        <button type="button" class="btn-excluir" data-id="${p.id}">Excluir</button>
      </article>
    `
    )
    .join("");
}
```

Se `p.nome` veio de um campo digitado por alguém, essa versão é vulnerável. Uma saída intermediária: montar a marcação fixa com template literal e preencher os textos variáveis com `textContent` depois.

### Performance: `DocumentFragment`

Cada `appendChild` direto no documento pode disparar um *reflow* (recálculo de layout). Para inserir muitos elementos, monte fora do documento e insira uma vez só:

```js
const fragmento = document.createDocumentFragment();
lista.forEach((item) => {
  const li = document.createElement("li");
  li.textContent = item.nome;
  fragmento.appendChild(li); // ainda fora do documento
});
container.appendChild(fragmento); // uma única operação no DOM
```

> **🔎 Por baixo do capô**
> O navegador não redesenha a tela a cada linha de JavaScript — ele acumula mudanças e recalcula o layout quando precisa (ou quando você lê uma medida, como `offsetHeight`, forçando o cálculo). Mesmo assim, inserir 500 nós um a um é mais caro que inserir um fragmento com 500 nós. Para listas de até algumas dezenas de itens, a diferença é imperceptível; para centenas, ela aparece no celular.

## 10. O modelo de eventos

Um **evento** é um sinal de que algo aconteceu: um clique, uma tecla, o envio de um formulário, o fim do carregamento. O JavaScript no navegador é **orientado a eventos**: você registra funções (*ouvintes* ou *listeners*) que serão chamadas quando o evento ocorrer. Entre um evento e outro, seu código não faz nada — o navegador fica esperando.

### O mínimo para começar

```js
const botao = document.querySelector("#meu-botao");

botao.addEventListener("click", function (evento) {
  console.log("Clicado!", evento.target);
});

// Com arrow function
botao.addEventListener("click", () => {
  document.querySelector("#saida").textContent = "Você clicou!";
});

// Garantir que o DOM está pronto (desnecessário se o script usa defer)
document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM montado");
});
```

### As três formas (e a única correta)

```html
<!-- 1. Atributo HTML — evite: mistura comportamento com estrutura -->
<button onclick="alert('Oi')">Clique</button>
```

```js
// 2. Propriedade do elemento — permite apenas UM ouvinte por evento
botao.onclick = function () { console.log("A"); };
botao.onclick = function () { console.log("B"); }; // sobrescreve o anterior!

// 3. addEventListener — a forma correta
botao.addEventListener("click", function () { console.log("A"); });
botao.addEventListener("click", function () { console.log("B"); });
// Ambos executam, na ordem de registro
```

> **🧠 Você sabia?**
> `addEventListener` só passou a funcionar em todos os navegadores em 2009, com o Internet Explorer 9. Até lá, o IE usava um método próprio, `attachEvent`, com outra assinatura e outro comportamento de `this`. Uma das razões de a biblioteca jQuery ter dominado a Web por uma década foi justamente esconder essa diferença atrás de um `.on("click", fn)` único. Hoje o padrão venceu e o jQuery é desnecessário — mas você ainda encontrará `onclick` e `attachEvent` em código legado.

### Sintaxe completa

```js
elemento.addEventListener(tipo, funcao, opcoes);

// Exemplos
botao.addEventListener("click", tratarClique);
botao.addEventListener("click", () => console.log("Oi"));

botao.addEventListener("click", tratarClique, {
  once: true,     // executa apenas uma vez e se remove
  capture: false, // fase de captura em vez de borbulhamento (seção 13)
  passive: true,  // promete não chamar preventDefault (melhora a rolagem no celular)
});

// Remoção — exige a MESMA referência de função
function tratarClique() { console.log("Oi"); }
botao.addEventListener("click", tratarClique);
botao.removeEventListener("click", tratarClique); // funciona

botao.addEventListener("click", () => {});
botao.removeEventListener("click", () => {});     // não remove nada
```

> **⚠️ Atenção**
> Funções anônimas não podem ser removidas, porque cada arrow function escrita é um objeto novo — a segunda `() => {}` não é a mesma que a primeira. Se precisar remover depois, nomeie a função.

> **⚠️ Atenção — o erro mais comum de todos**
> `botao.addEventListener("click", tratarClique())` — com parênteses — **chama** a função imediatamente, no momento do registro, e passa o *retorno* dela (geralmente `undefined`) como ouvinte. O clique depois não faz nada. Passe a **referência**: `tratarClique`, sem parênteses. Se precisar passar argumentos, envolva em uma arrow: `() => tratarClique(42)`.

## 11. Principais tipos de evento

### Mouse

| Evento | Quando ocorre |
|---|---|
| `click` | Clique (pressionar e soltar sobre o elemento); também disparado por Enter/Espaço em botões e por toque |
| `dblclick` | Duplo clique |
| `mousedown` / `mouseup` | Botão pressionado / solto |
| `mouseenter` / `mouseleave` | Entra / sai do elemento. Não borbulham |
| `mouseover` / `mouseout` | Idem, mas borbulham dos filhos |
| `mousemove` | Movimento do ponteiro (dispara dezenas de vezes por segundo) |
| `contextmenu` | Botão direito |

### Teclado

| Evento | Quando ocorre |
|---|---|
| `keydown` | Tecla pressionada (repete se segurar) |
| `keyup` | Tecla solta |
| `keypress` | Obsoleto — não use |

```js
campo.addEventListener("keydown", (e) => {
  console.log(e.key);  // "a", "Enter", "Escape", "ArrowUp", " "
  console.log(e.code); // "KeyA", "Enter", "Space" — posição física da tecla
  console.log(e.ctrlKey, e.shiftKey, e.altKey);

  if (e.key === "Enter") enviar();
  if (e.key === "Escape") fecharModal();
  if (e.ctrlKey && e.key === "s") {
    e.preventDefault(); // impede o "Salvar página" do navegador
    salvar();
  }
});
```

> **💡 Dica**
> Use `e.key` para saber **qual caractere**; use `e.code` para saber **qual tecla física** (importante em jogos e em teclados de layouts diferentes — no teclado ABNT2, `e.key` da tecla ao lado do Enter é `"ç"`, mas `e.code` é `"Semicolon"`).

### Formulário

| Evento | Quando ocorre |
|---|---|
| `submit` | Formulário enviado — registre no `<form>`, não no botão |
| `input` | A cada alteração do valor. O mais útil para validação ao vivo |
| `change` | Ao perder o foco após alterar (ou imediatamente em `select`/checkbox/radio) |
| `focus` / `blur` | Ganha / perde foco. Não borbulham |
| `focusin` / `focusout` | Idem, mas borbulham |
| `reset` | Formulário limpo |

### Janela e documento

| Evento | Quando ocorre |
|---|---|
| `DOMContentLoaded` | HTML lido e DOM montado (não espera imagens) |
| `load` | Tudo carregado, inclusive imagens e estilos |
| `resize` | Janela redimensionada |
| `scroll` | Rolagem |
| `beforeunload` | Antes de sair da página |

### Toque

`touchstart`, `touchmove`, `touchend`. Em geral, `click` já funciona em telas de toque — só use eventos de toque para gestos específicos (arrastar, pinçar).

> **🔬 Investigue**
> No Console, digite `monitorEvents(document.body, "click")` e clique em qualquer lugar da página: cada clique é impresso com o objeto do evento. Troque para `monitorEvents(document.body, ["keydown", "keyup"])` e digite algo. Quando cansar, `unmonitorEvents(document.body)`. Depois selecione um botão na aba **Elements** e abra a sub-aba **Event Listeners** no painel lateral: ela lista todos os ouvintes registrados naquele elemento e nos ancestrais — com o arquivo e a linha onde cada um foi escrito. É assim que você descobre "quem está reagindo a esse clique" em um site que não escreveu.

## 12. O objeto `event`

Toda função ouvinte recebe automaticamente um objeto com informações sobre o que ocorreu.

```js
elemento.addEventListener("click", function (event) {
  event.type;          // "click"
  event.target;        // elemento que ORIGINOU o evento
  event.currentTarget; // elemento onde o OUVINTE está registrado
  event.timeStamp;     // milissegundos desde o carregamento da página

  event.clientX, event.clientY; // coordenadas na janela
  event.pageX, event.pageY;     // coordenadas na página (com rolagem)

  event.preventDefault();  // cancela o comportamento padrão
  event.stopPropagation(); // interrompe a propagação
});
```

> **⚠️ Atenção — `target` × `currentTarget`**
> Se você clica em um `<span>` dentro de um `<button>` que tem o ouvinte, `target` é o `<span>` e `currentTarget` é o `<button>`. Confundir os dois é a causa mais comum de bugs em delegação de eventos.

### `preventDefault()`

```js
// Impede o envio e o recarregamento da página
formulario.addEventListener("submit", (e) => {
  e.preventDefault();
  processarDados();
});

// Impede a navegação de um link
link.addEventListener("click", (e) => {
  e.preventDefault();
  abrirModal();
});

// Bloqueia caracteres não numéricos (teclas de um só caractere)
campo.addEventListener("keydown", (e) => {
  if (!/[0-9]/.test(e.key) && e.key.length === 1) e.preventDefault();
});
```

Sem `e.preventDefault()` no `submit`, a página recarrega e todo o seu JavaScript é reiniciado — os dados somem e parece que "o código não funcionou". É o erro nº 1 da próxima aula.

## 13. Propagação de eventos

Quando você clica em um elemento aninhado, o evento percorre a árvore em três fases:

```text
                ┌── document ──┐
   CAPTURA      │              │     BORBULHAMENTO
   (descendo)   ▼              ▲     (subindo)
              <div>          <div>
                ▼              ▲
               <ul>          <ul>
                ▼              ▲
               <li>          <li>
                ▼              ▲
            <button> ── ALVO ──┘
```

1. **Captura:** de `document` até o alvo.
2. **Alvo:** no elemento clicado.
3. **Borbulhamento** (*bubbling*): do alvo de volta até `document`. É a fase padrão — onde os ouvintes ficam, a menos que você peça o contrário.

```js
document.querySelector("ul").addEventListener("click", () => console.log("UL"));
document.querySelector("li").addEventListener("click", () => console.log("LI"));
// Clicar no LI imprime: "LI", depois "UL"

// Para ouvir na captura:
ul.addEventListener("click", tratar, true);
// ou { capture: true } — agora imprime "UL", depois "LI"
```

```js
event.stopPropagation();          // impede que continue subindo
event.stopImmediatePropagation(); // também impede outros ouvintes no MESMO elemento
```

> **⚠️ Atenção**
> Use `stopPropagation` com parcimônia. Ele quebra a delegação e cria comportamentos difíceis de rastrear meses depois ("por que o menu não fecha quando clico aqui?"). Antes de usá-lo, pergunte se não é melhor verificar `event.target`.

## 14. Delegação de eventos

**O problema:** você adiciona ouvintes a 50 botões de "excluir". Depois, o JavaScript cria mais 10 botões dinamicamente. Os novos não têm ouvinte — porque `addEventListener` só afeta elementos que existiam no momento do registro.

**A solução:** registre um único ouvinte no contêiner pai e descubra, pelo `event.target`, quem foi realmente clicado. Isso funciona porque os eventos borbulham.

```js
const lista = document.querySelector("#lista-produtos");

lista.addEventListener("click", (event) => {
  // Encontra o botão, mesmo se o clique foi num ícone dentro dele
  const botaoExcluir = event.target.closest(".btn-excluir");
  if (!botaoExcluir) return; // clique fora dos botões: ignora

  const id = Number(botaoExcluir.dataset.id);
  excluirProduto(id);
});
```

Vantagens:

1. Funciona para elementos criados depois — sem re-registrar nada.
2. Um ouvinte em vez de N — menos memória, melhor desempenho.
3. Código mais simples — a lógica fica concentrada em um lugar.

### Padrão para múltiplas ações no mesmo contêiner

```html
<button type="button" data-acao="editar" data-id="7">Editar</button>
<button type="button" data-acao="excluir" data-id="7">Excluir</button>
```

```js
lista.addEventListener("click", (e) => {
  const botao = e.target.closest("button[data-acao]");
  if (!botao) return;

  const { acao, id } = botao.dataset;

  switch (acao) {
    case "editar":
      editar(Number(id));
      break;
    case "excluir":
      excluir(Number(id));
      break;
    case "concluir":
      concluir(Number(id));
      break;
  }
});
```

Este padrão é a espinha dorsal de qualquer CRUD em JavaScript puro — e será exigido no projeto da Avaliação 3. Vale a pena entendê-lo agora.

## 15. Eventos personalizados

Você também pode criar os seus próprios eventos, com dados anexados em `detail`:

```js
const evento = new CustomEvent("produtoAdicionado", {
  detail: { id: 5, nome: "Mouse" },
  bubbles: true,
});

document.dispatchEvent(evento);

document.addEventListener("produtoAdicionado", (e) => {
  console.log(e.detail.nome); // "Mouse"
});
```

Útil para desacoplar partes da aplicação: um módulo avisa que algo aconteceu sem conhecer quem vai reagir. No site do evento, por exemplo, o formulário de inscrição pode disparar `inscricaoConfirmada` e o contador de vagas, em outro arquivo, apenas escuta.

## 16. Controle de frequência: debounce e throttle

Eventos como `input`, `scroll`, `mousemove` e `resize` disparam dezenas de vezes por segundo. Executar uma operação pesada (filtrar 500 itens, redesenhar uma lista) em cada disparo trava a interface.

```js
// DEBOUNCE — só executa depois que os disparos PARAM por X ms
function debounce(fn, atraso = 300) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), atraso);
  };
}

const buscar = debounce((texto) => {
  console.log("Buscando por:", texto);
}, 400);

campoBusca.addEventListener("input", (e) => buscar(e.target.value));
```

```js
// THROTTLE — executa no máximo uma vez a cada X ms
function throttle(fn, intervalo = 200) {
  let podeExecutar = true;
  return function (...args) {
    if (!podeExecutar) return;
    podeExecutar = false;
    fn.apply(this, args);
    setTimeout(() => {
      podeExecutar = true;
    }, intervalo);
  };
}

window.addEventListener(
  "scroll",
  throttle(() => {
    console.log("Rolando");
  }, 200)
);
```

| Aspecto | Debounce | Throttle |
|---|---|---|
| Quando executa | Após a pausa nos disparos | Em intervalos regulares |
| Uso típico | Busca ao digitar, validação, redimensionamento | Rolagem, movimento do mouse, animações |

> **🔎 Por baixo do capô**
> `debounce` só funciona por causa das *closures* da seção 1: a variável `timer` fica "presa" dentro da função retornada e sobrevive entre uma chamada e outra. Cada tecla cancela o `setTimeout` anterior e agenda outro; só o último sobrevive 300 ms e executa `fn`.

## 17. Acessibilidade em eventos

```js
// Só funciona com mouse
div.addEventListener("click", acao);

// Use um <button> de verdade: já é focável, acionável por Enter/Espaço
// e anunciado como botão pelo leitor de tela
botao.addEventListener("click", acao);
```

Se por algum motivo precisar tornar um elemento genérico interativo:

```html
<div role="button" tabindex="0" aria-pressed="false">Alternar</div>
```

```js
div.addEventListener("keydown", (e) => {
  if (e.key === "Enter" || e.key === " ") {
    e.preventDefault();
    acao();
  }
});
```

Regra: se algo é **clicável**, use `<button>`. Se **navega** para outro lugar, use `<a href>`. Reinventar controles com `<div>` é a origem da maioria dos problemas de acessibilidade em sites modernos — e o Lighthouse (Aula 15) penaliza isso.

> **📌 Na prova**
> Costuma cair: (1) a diferença entre `target` e `currentTarget`; (2) por que `addEventListener("click", fn())` não funciona; (3) o que acontece sem `preventDefault` no `submit`; (4) por que delegação resolve elementos criados depois; (5) a ordem de impressão em um exemplo de borbulhamento.

## 18. A arquitetura: estado → dados → renderização → eventos

Antes de ir para o projeto, um esqueleto que vale para qualquer aplicação front-end — do menu de hoje ao CRUD do fim da unidade:

```js
// js/app.js — esqueleto de organização
// ===== ESTADO: a fonte única da verdade =====
let tarefas = [];
let filtroAtual = "todas";

// ===== SELEÇÃO DE ELEMENTOS (uma vez só) =====
const els = {
  form: document.querySelector("#form-tarefa"),
  input: document.querySelector("#input-tarefa"),
  lista: document.querySelector("#lista-tarefas"),
};

// ===== FUNÇÕES DE DADOS (puras: alteram só o estado) =====
function adicionarTarefa(texto) {
  tarefas.push({ id: Date.now(), texto, concluida: false });
}

function alternarConclusao(id) {
  const tarefa = tarefas.find((t) => t.id === id);
  if (tarefa) tarefa.concluida = !tarefa.concluida;
}

function obterTarefasVisiveis() {
  if (filtroAtual === "pendentes") return tarefas.filter((t) => !t.concluida);
  if (filtroAtual === "concluidas") return tarefas.filter((t) => t.concluida);
  return [...tarefas];
}

// ===== RENDERIZAÇÃO (desenha a tela a partir do estado) =====
function renderizar() {
  els.lista.innerHTML = "";
  obterTarefasVisiveis().forEach((t) => {
    const li = document.createElement("li");
    li.dataset.id = t.id;
    li.classList.toggle("concluida", t.concluida);
    li.textContent = t.texto;
    els.lista.appendChild(li);
  });
}

// ===== EVENTOS (capturam a intenção do usuário) =====
function registrarEventos() {
  els.form.addEventListener("submit", (e) => {
    e.preventDefault();
    const texto = els.input.value.trim();
    if (texto === "") return;
    adicionarTarefa(texto);
    els.input.value = "";
    renderizar();
  });

  els.lista.addEventListener("click", (e) => {
    const li = e.target.closest("li[data-id]");
    if (!li) return;
    alternarConclusao(Number(li.dataset.id));
    renderizar();
  });
}

// ===== INICIALIZAÇÃO =====
function iniciar() {
  registrarEventos();
  renderizar();
}

iniciar();
```

O fluxo é sempre o mesmo: **usuário age → evento → função altera o estado → `renderizar()` redesenha**. Nunca altere o DOM "na mão" para refletir uma mudança de dado: se o usuário conclui uma tarefa, não risque o `<li>` — mude o array e renderize de novo. Quando DOM e dados divergem, os bugs se tornam impossíveis de rastrear. Frameworks como Vue e React (Nível 3) apenas automatizam essa mesma ideia.

## 💻 Mão na massa — Menu mobile e lista de palestrantes

O site do evento acadêmico tem um menu que, em telas estreitas, ocupa a tela inteira, e uma página de palestrantes escrita à mão, card por card. Hoje o menu ganha um botão "hambúrguer" que abre e fecha por clique, teclado e clique fora — e a página de palestrantes passa a ser **renderizada a partir de um array**, com filtro por área usando delegação.

### Passo 1 — o botão do menu no cabeçalho (todas as páginas)

O cabeçalho é o mesmo nas cinco páginas; altere-o em cada uma. O botão vem **antes** do `<nav>`, com `aria-expanded` (estado) e `aria-controls` (o que ele controla):

**`index.html`** (trecho do `<header>`; repita em `programacao.html`, `palestrantes.html`, `inscricao.html` e `contato.html`)

```html
<header class="cabecalho">
  <a class="logo" href="index.html">Semana Acadêmica de Sistemas de Informação</a>

  <button class="menu-toggle" type="button"
          aria-expanded="false" aria-controls="menu-principal"
          aria-label="Abrir menu">
    <span class="menu-toggle__barra"></span>
    <span class="menu-toggle__barra"></span>
    <span class="menu-toggle__barra"></span>
  </button>

  <nav id="menu-principal" class="menu" aria-label="Principal">
    <ul>
      <li><a href="index.html">Início</a></li>
      <li><a href="programacao.html">Programação</a></li>
      <li><a href="palestrantes.html">Palestrantes</a></li>
      <li><a href="inscricao.html">Inscrição</a></li>
      <li><a href="contato.html">Contato</a></li>
    </ul>
  </nav>
</header>
```

E, no `<head>` de todas as páginas, o script comum com `defer`:

```html
<script src="js/app.js" defer></script>
```

### Passo 2 — o CSS do menu fechado e aberto

**`css/estilo.css`** (acrescente ao fim)

```css
/* ===== Menu mobile ===== */
.menu-toggle {
  display: none; /* escondido no desktop */
}

@media (max-width: 47.99rem) {
  .cabecalho {
    position: relative;
  }

  .menu-toggle {
    display: inline-flex;
    flex-direction: column;
    gap: 5px;
    padding: 0.5rem;
    background: none;
    border: 0;
    color: inherit;
    cursor: pointer;
  }

  .menu-toggle__barra {
    width: 26px;
    height: 3px;
    border-radius: 2px;
    background: currentColor;
    transition: transform 0.2s, opacity 0.2s;
  }

  /* O botão vira um "X" quando o menu está aberto */
  .menu-toggle[aria-expanded="true"] .menu-toggle__barra:nth-child(1) {
    transform: translateY(8px) rotate(45deg);
  }
  .menu-toggle[aria-expanded="true"] .menu-toggle__barra:nth-child(2) {
    opacity: 0;
  }
  .menu-toggle[aria-expanded="true"] .menu-toggle__barra:nth-child(3) {
    transform: translateY(-8px) rotate(-45deg);
  }

  .menu {
    display: none; /* o CSS define o que é "fechado" */
    position: absolute;
    inset: 100% 0 auto 0;
    background: var(--cor-fundo-cabecalho, #0b3d5c);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  }

  .menu.aberto {
    display: block; /* o JS só decide quando */
  }

  .menu ul {
    flex-direction: column;
  }

  .menu a {
    display: block;
    padding: 0.9rem 1.25rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  .menu-toggle__barra {
    transition: none;
  }
}
```

### Passo 3 — o comportamento do menu

**`js/app.js`**

```js
// js/app.js — comportamento comum a todas as páginas do site do evento
const botaoMenu = document.querySelector(".menu-toggle");
const menu = document.querySelector("#menu-principal");
const LARGURA_DESKTOP = 768; // mesmo ponto de quebra do CSS (48rem)

function abrirMenu() {
  menu.classList.add("aberto");
  botaoMenu.setAttribute("aria-expanded", "true");
  botaoMenu.setAttribute("aria-label", "Fechar menu");
}

function fecharMenu() {
  menu.classList.remove("aberto");
  botaoMenu.setAttribute("aria-expanded", "false");
  botaoMenu.setAttribute("aria-label", "Abrir menu");
}

function menuEstaAberto() {
  return menu.classList.contains("aberto");
}

function alternarMenu() {
  if (menuEstaAberto()) {
    fecharMenu();
  } else {
    abrirMenu();
  }
}

// Marca o link da página atual (aria-current) sem editar cada HTML
function marcarPaginaAtual() {
  const arquivoAtual = location.pathname.split("/").pop() || "index.html";

  menu.querySelectorAll("a").forEach((link) => {
    const destino = link.getAttribute("href");
    if (destino === arquivoAtual) {
      link.setAttribute("aria-current", "page");
    } else {
      link.removeAttribute("aria-current");
    }
  });
}

function registrarEventosDoMenu() {
  // 1. Clique no botão: abre/fecha
  botaoMenu.addEventListener("click", alternarMenu);

  // 2. Escape fecha e devolve o foco ao botão
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && menuEstaAberto()) {
      fecharMenu();
      botaoMenu.focus();
    }
  });

  // 3. Clique fora do menu e do botão: fecha (delegação em document)
  document.addEventListener("click", (e) => {
    const clicouDentro = menu.contains(e.target) || botaoMenu.contains(e.target);
    if (!clicouDentro && menuEstaAberto()) fecharMenu();
  });

  // 4. Ao alargar a janela para desktop, garante o estado fechado
  window.addEventListener("resize", () => {
    if (window.innerWidth >= LARGURA_DESKTOP && menuEstaAberto()) fecharMenu();
  });
}

// Só liga o comportamento se os elementos existem nesta página
if (botaoMenu && menu) {
  marcarPaginaAtual();
  registrarEventosDoMenu();
}
```

Repare no `if (botaoMenu && menu)` do fim: se uma página não tiver o cabeçalho (uma página de erro, por exemplo), o script não quebra com `Cannot read properties of null`.

### Passo 4 — a página de palestrantes renderizada do array

Substitua os cards escritos à mão por um contêiner vazio, os botões de filtro e um contador:

**`palestrantes.html`** (trecho do `<main>`)

```html
<main class="conteudo">
  <h1>Palestrantes</h1>
  <p>Conheça quem vai compartilhar conhecimento nesta edição.</p>

  <div id="filtros-area" class="filtros" role="group" aria-label="Filtrar por área">
    <button type="button" class="ativo" data-area="todas" aria-pressed="true">Todas</button>
    <button type="button" data-area="ia" aria-pressed="false">Inteligência Artificial</button>
    <button type="button" data-area="web" aria-pressed="false">Desenvolvimento Web</button>
    <button type="button" data-area="seguranca" aria-pressed="false">Segurança</button>
    <button type="button" data-area="dados" aria-pressed="false">Ciência de Dados</button>
  </div>

  <p id="contador-palestrantes" class="contador" aria-live="polite"></p>

  <section id="lista-palestrantes" class="grade-palestrantes"></section>
</main>

<script src="js/palestrantes.js" defer></script>
```

**`js/palestrantes.js`**

```js
// js/palestrantes.js — lista de palestrantes renderizada a partir de dados

// ===== ESTADO =====
const palestrantes = [
  {
    id: 1,
    nome: "Ana Lúcia Ferreira",
    instituicao: "UNEMAT — Sinop",
    area: "ia",
    tema: "Redes neurais para prever a safra de soja",
    foto: "img/palestrantes/ana-lucia.webp",
  },
  {
    id: 2,
    nome: "Bruno Takahashi",
    instituicao: "Startup AgroData",
    area: "dados",
    tema: "Dashboards que os produtores realmente usam",
    foto: "img/palestrantes/bruno.webp",
  },
  {
    id: 3,
    nome: "Carla Mendes",
    instituicao: "UFMT",
    area: "seguranca",
    tema: "O que um ataque de phishing ensina sobre UX",
    foto: "img/palestrantes/carla.webp",
  },
  {
    id: 4,
    nome: "Diego Nascimento",
    instituicao: "Prefeitura de Sinop",
    area: "web",
    tema: "Acessibilidade em portais públicos: erros que vimos",
    foto: "img/palestrantes/diego.webp",
  },
  {
    id: 5,
    nome: "Eduarda Ribeiro",
    instituicao: "UNEMAT — Sinop",
    area: "web",
    tema: "Do HTML ao deploy: o caminho do estudante",
    foto: "img/palestrantes/eduarda.webp",
  },
  {
    id: 6,
    nome: "Felipe Arruda",
    instituicao: "Cooperativa Coopercana",
    area: "ia",
    tema: "Visão computacional no controle de pragas",
    foto: "img/palestrantes/felipe.webp",
  },
];

const NOMES_DAS_AREAS = {
  ia: "Inteligência Artificial",
  web: "Desenvolvimento Web",
  seguranca: "Segurança",
  dados: "Ciência de Dados",
};

let areaAtual = "todas";

// ===== SELEÇÃO DE ELEMENTOS =====
const els = {
  lista: document.querySelector("#lista-palestrantes"),
  filtros: document.querySelector("#filtros-area"),
  contador: document.querySelector("#contador-palestrantes"),
};

// ===== FUNÇÕES DE DADOS =====
function obterPalestrantesVisiveis() {
  if (areaAtual === "todas") return [...palestrantes];
  return palestrantes.filter((p) => p.area === areaAtual);
}

// ===== RENDERIZAÇÃO =====
function criarCard(p) {
  const card = document.createElement("article");
  card.classList.add("card-palestrante");
  card.dataset.id = p.id;

  const foto = document.createElement("img");
  foto.src = p.foto;
  foto.alt = `Foto de ${p.nome}`;
  foto.width = 240;
  foto.height = 240;
  foto.loading = "lazy";

  const nome = document.createElement("h2");
  nome.textContent = p.nome; // textContent: seguro

  const instituicao = document.createElement("p");
  instituicao.classList.add("instituicao");
  instituicao.textContent = p.instituicao;

  const area = document.createElement("span");
  area.classList.add("etiqueta");
  area.textContent = NOMES_DAS_AREAS[p.area];

  const tema = document.createElement("p");
  tema.classList.add("tema");
  tema.textContent = p.tema;

  card.append(foto, nome, instituicao, area, tema);
  return card;
}

function renderizar() {
  const visiveis = obterPalestrantesVisiveis();
  els.lista.innerHTML = "";

  if (visiveis.length === 0) {
    const aviso = document.createElement("p");
    aviso.classList.add("vazio");
    aviso.textContent = "Nenhum palestrante nesta área ainda. Volte em breve!";
    els.lista.appendChild(aviso);
  } else {
    const fragmento = document.createDocumentFragment();
    visiveis.forEach((p) => fragmento.appendChild(criarCard(p)));
    els.lista.appendChild(fragmento);
  }

  const total = visiveis.length;
  els.contador.textContent =
    total === 1 ? "1 palestrante" : `${total} palestrantes`;
}

function atualizarBotoesDeFiltro() {
  els.filtros.querySelectorAll("button[data-area]").forEach((botao) => {
    const ativo = botao.dataset.area === areaAtual;
    botao.classList.toggle("ativo", ativo);
    botao.setAttribute("aria-pressed", String(ativo));
  });
}

// ===== EVENTOS =====
function registrarEventos() {
  // Um único ouvinte para todos os botões de filtro (delegação)
  els.filtros.addEventListener("click", (e) => {
    const botao = e.target.closest("button[data-area]");
    if (!botao) return;

    areaAtual = botao.dataset.area;
    atualizarBotoesDeFiltro();
    renderizar();
  });
}

// ===== INICIALIZAÇÃO =====
function iniciar() {
  registrarEventos();
  renderizar();
}

iniciar();
```

### Passo 5 — o estilo dos cards e dos filtros

**`css/estilo.css`** (acrescente ao fim)

```css
/* ===== Palestrantes ===== */
.filtros {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-block: 1rem;
}

.filtros button {
  padding: 0.5rem 1rem;
  border: 2px solid var(--cor-primaria, #0b3d5c);
  border-radius: 999px;
  background: transparent;
  color: var(--cor-primaria, #0b3d5c);
  cursor: pointer;
}

.filtros button.ativo {
  background: var(--cor-primaria, #0b3d5c);
  color: #fff;
}

.filtros button:focus-visible {
  outline: 3px solid var(--cor-destaque, #e67e22);
  outline-offset: 2px;
}

.contador {
  color: var(--cor-texto-suave, #555);
}

.grade-palestrantes {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(16rem, 1fr));
  gap: 1.5rem;
}

.card-palestrante {
  display: grid;
  gap: 0.5rem;
  padding: 1rem;
  border-radius: 12px;
  background: var(--cor-superficie, #fff);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.card-palestrante img {
  width: 100%;
  height: auto;
  aspect-ratio: 1;
  object-fit: cover;
  border-radius: 8px;
}

.card-palestrante h2 {
  font-size: 1.15rem;
  margin: 0;
}

.etiqueta {
  justify-self: start;
  padding: 0.15rem 0.6rem;
  border-radius: 999px;
  background: var(--cor-fundo-suave, #eef3f7);
  font-size: 0.8rem;
}

.vazio {
  grid-column: 1 / -1;
  padding: 2rem;
  text-align: center;
  color: var(--cor-texto-suave, #555);
}
```

### Como testar

1. Abra `index.html` com o Live Server e estreite a janela para menos de 768 px (ou use o modo dispositivo do DevTools, <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>M</kbd>). O botão hambúrguer aparece; o menu, não.
2. Clique no botão: o menu abre, as barras viram um "X" e, na aba **Elements**, `aria-expanded` muda para `"true"`.
3. Pressione <kbd>Esc</kbd>: o menu fecha e o foco volta ao botão (o contorno de foco aparece nele). Abra de novo e clique fora do menu: fecha.
4. Alargue a janela: o menu fecha sozinho e o botão desaparece.
5. Vá a `palestrantes.html`: os seis cards aparecem gerados pelo JavaScript (confira em **Elements** que o `<section>` está cheio, enquanto em "Exibir código-fonte" ele está vazio). O contador mostra "6 palestrantes".
6. Clique em "Segurança": só a Carla aparece e o contador diz "1 palestrante". Clique em "Todas": tudo volta. Navegue pelos filtros com <kbd>Tab</kbd> e acione com <kbd>Enter</kbd> — funciona igual.
7. Console limpo: nenhum erro em vermelho em nenhuma das cinco páginas.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Escreva a mesma função nas três formas (declaração, expressão e arrow): recebe o raio e retorna a área do círculo (`Math.PI * raio ** 2`).

**A2.** O que faz o operador rest (`...numeros`) em um parâmetro de função? E o spread em uma chamada? Dê um exemplo de cada.

**A3.** O que é o DOM? Ele é o mesmo que o arquivo HTML? Justifique com o que você vê em "Exibir código-fonte" versus a aba Elements.

**A4.** Qual a diferença entre `querySelector` e `querySelectorAll`? O que cada um retorna quando não encontra nada?

**A5.** Qual a diferença entre `textContent`, `innerText` e `innerHTML`?

**A6.** Explique o que é XSS e como `textContent` previne esse ataque.

**A7.** Escreva o código para: (a) selecionar o elemento de id `menu`; (b) selecionar todos os `<li>` dentro de `.nav`; (c) selecionar o primeiro input do tipo email.

**A8.** Escreva o código que adiciona a classe `ativo`, remove `inativo` e alterna `aberto` em um elemento.

**A9.** Escreva os três passos para criar e inserir um novo `<li>` com texto "Item" em uma `<ul>` existente.

**A10.** O que faz `closest(".card")`? Dê um caso de uso.

**A11.** Por que é preferível trocar classes a definir `element.style` diretamente?

**A12.** Um `querySelector` retornou `null` e o código quebrou com `Cannot read properties of null`. Cite duas causas prováveis e como corrigir cada uma.

**A13.** Por que `addEventListener` é preferível a `elemento.onclick`?

**A14.** Diferencie `event.target` de `event.currentTarget` com um exemplo concreto.

**A15.** Descreva as três fases da propagação de eventos.

**A16.** O que faz `event.preventDefault()`? Dê dois casos de uso.

**A17.** Qual a diferença entre `stopPropagation()` e `preventDefault()`?

**A18.** O que é delegação de eventos e qual problema ela resolve?

**A19.** Diferencie os eventos `input` e `change`. Quando usar cada um?

**A20.** Escreva o código que executa uma função quando o usuário pressiona Enter em um campo de texto.

**A21.** Escreva o código que impede o recarregamento da página ao enviar um formulário.

**A22.** O que faz a opção `{ once: true }` em `addEventListener`?

**A23.** Por que `<div onclick="">` é pior que `<button>` do ponto de vista de acessibilidade? Cite três motivos.

### Nível B — Aplicação

**B1.** Implemente `calculadora` como um objeto com os métodos `somar`, `subtrair`, `multiplicar`, `dividir` (tratando divisão por zero) e `potencia`, todos com validação de tipo dos parâmetros (`typeof`).

**Resultado esperado:** `calculadora.dividir(10, 0)` retorna `null` (ou lança um erro com mensagem clara); `calculadora.somar("2", 3)` rejeita a string; `calculadora.potencia(2, 10)` retorna `1024`.

<details><summary>Dica</summary>

Crie uma função auxiliar `saoNumeros(...valores)` que use `valores.every((v) => typeof v === "number" && !Number.isNaN(v))` e chame-a no início de cada método. Métodos de objeto precisam de `this`? Aqui não — cada método só usa seus parâmetros, então arrow functions ou métodos curtos servem.
</details>

**B2.** Dada uma lista `<ul>` com 10 `<li>`, escreva o JavaScript que: pinta os ímpares de cinza-claro (via classe); adiciona a classe `destaque` ao primeiro e ao último; adiciona um número de ordem antes do texto de cada um; e exibe no console o texto de todos.

**Resultado esperado:** a lista alterna cores, o primeiro e o último ficam em negrito, cada item começa com "1. ", "2. " e assim por diante, e o console mostra os 10 textos.

<details><summary>Dica</summary>

`querySelectorAll("ul li").forEach((li, indice) => …)` — o segundo parâmetro do `forEach` é o índice. Para o texto, `li.textContent = \`${indice + 1}. ${li.textContent}\``. Para o primeiro e o último, compare `indice` com `0` e com `lista.length - 1`.
</details>

**B3.** Construa uma tabela dinâmica: dado um array de alunos com três notas, gere uma `<table>` completa com `<thead>`, `<tbody>`, média calculada e uma coluna "Situação" cuja célula recebe a classe `.aprovado`, `.exame` ou `.reprovado` conforme o valor (≥ 6, ≥ 4, abaixo).

**Resultado esperado:** uma tabela com uma linha por aluno, a média com duas casas (`toFixed(2)`) e a célula de situação colorida pelo CSS.

<details><summary>Dica</summary>

Crie `criarLinha(aluno)` que devolve um `<tr>` com `<td>` gerados por `createElement`. Use `reduce` para a média e a função `classificar` da seção 1 para a situação. Monte tudo em um `DocumentFragment` e insira no `<tbody>` uma vez.
</details>

**B4.** Escreva uma função `criarElemento(tag, atributos, filhos)` que crie e configure um elemento genericamente. Exemplo de uso:

```js
criarElemento("a", { href: "#", class: "btn", "data-id": 5 }, ["Clique aqui"]);
```

Use-a para reconstruir a renderização de produtos da seção 9 em menos linhas.

**Resultado esperado:** `criarElemento("li", { class: "item" }, ["Texto", criarElemento("strong", {}, ["!"])])` gera `<li class="item">Texto<strong>!</strong></li>`.

<details><summary>Dica</summary>

`Object.entries(atributos).forEach(([nome, valor]) => el.setAttribute(nome, valor))`. Para os filhos, se for string use `document.createTextNode`; se for elemento, `appendChild` direto — `el.append(...filhos)` já aceita os dois tipos.
</details>

**B5.** Implemente um modal: botão que abre, botão "×" que fecha, clique no fundo escurecido que fecha, tecla Escape que fecha. Ao abrir, o foco deve ir para dentro do modal; ao fechar, voltar ao botão que o abriu.

**Resultado esperado:** o modal funciona só com o teclado (<kbd>Tab</kbd> até o botão, <kbd>Enter</kbd> abre, <kbd>Esc</kbd> fecha) e o foco nunca "some".

<details><summary>Dica</summary>

Use o elemento nativo `<dialog>` com `dialog.showModal()` e `dialog.close()` — ele já trata Escape e o foco inicial. Para o clique no fundo, ouça `click` no próprio `dialog` e feche se `e.target === dialog`. Guarde `document.activeElement` antes de abrir para devolver o foco ao fechar.
</details>

**B6.** Crie um menu suspenso (dropdown) que abre ao clicar, fecha ao clicar fora (use delegação em `document`), fecha com Escape e navega com as setas do teclado.

**Resultado esperado:** <kbd>↓</kbd> move o foco para o próximo item, <kbd>↑</kbd> para o anterior, <kbd>Esc</kbd> fecha e devolve o foco ao botão.

<details><summary>Dica</summary>

Guarde os itens em `[...menu.querySelectorAll("a")]` e o índice do item focado. No `keydown`, calcule o novo índice com `(indice + 1) % itens.length` (e `(indice - 1 + itens.length) % itens.length` para subir) e chame `.focus()`. O padrão de "clique fora" é o mesmo do Mão na massa.
</details>

**B7.** Implemente um contador de caracteres em um `<textarea>` com limite de 280: exibe os restantes, fica amarelo abaixo de 40 e vermelho abaixo de 10, e desabilita o botão de envio ao ultrapassar.

**Resultado esperado:** "280 caracteres restantes" ao carregar; ao digitar, o número cai; com 281 caracteres o botão fica `disabled` e o texto, vermelho.

<details><summary>Dica</summary>

Ouça `input` no textarea, calcule `restantes = LIMITE - textarea.value.length` e use `classList.toggle("alerta", restantes < 40)` e `classList.toggle("perigo", restantes < 10)`. `botao.disabled = restantes < 0`.
</details>

**B8.** Crie uma lista de 20 itens gerados dinamicamente onde cada item tem botões "subir", "descer" e "excluir", todos tratados por um **único** ouvinte no contêiner (delegação).

**Resultado esperado:** clicar em "subir" troca o item de posição com o anterior; "excluir" remove; a lista continua funcionando depois de qualquer operação porque é re-renderizada a partir do array.

<details><summary>Dica</summary>

Não mova o `<li>` no DOM — troque as posições no array com `[itens[i - 1], itens[i]] = [itens[i], itens[i - 1]]` e chame `renderizar()`. Use `data-acao` e `data-id` nos botões e o `switch` da seção 14.
</details>

### Nível C — Desafio em sala

**C1.** Kanban com arrastar e soltar. Construa um quadro com três colunas (A fazer, Em andamento, Concluído). Cartões podem ser criados, editados, excluídos e arrastados entre colunas usando a API de Drag and Drop (`dragstart`, `dragover`, `drop`). Contadores por coluna. Deve funcionar também por teclado (botões "mover para →" e "← mover para").

<details><summary>Dica</summary>

Cada cartão tem `draggable="true"` e `data-id`. No `dragstart`, guarde o id em `e.dataTransfer.setData("text/plain", id)`. A coluna precisa chamar `e.preventDefault()` no `dragover` para aceitar o *drop*. No `drop`, leia o id, mude o campo `coluna` do cartão no array e renderize tudo — o mesmo fluxo estado → renderização de sempre. Os botões de teclado fazem exatamente a mesma alteração no array.
</details>

## 🏆 Desafios

### ⭐ O botão que só funciona uma vez
Tags: javascript, eventos, bug, devtools

Um colega enviou o código abaixo dizendo que "o contador funciona uma vez e depois para, e às vezes nem começa". Rode-o, reproduza os dois sintomas e encontre os **três** bugs plantados — sem reescrever do zero. Cada um é um erro clássico visto nesta aula.

```html
<!-- bug-contador.html -->
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Contador</title>
  <script src="contador.js"></script>
</head>
<body>
  <p>Cliques: <strong id="total">0</strong></p>
  <button id="btn-somar"><span>Somar</span></button>
  <button id="btn-zerar">Zerar</button>
</body>
</html>
```

```js
// contador.js
let total = 0;
const saida = document.querySelector("#total");
const btnSomar = document.querySelector("#btn-somar");
const btnZerar = document.querySelector("#btn-zerar");

function somar(e) {
  if (e.target !== btnSomar) return;
  total = total + 1;
  saida.textContent = total;
}

btnSomar.addEventListener("click", somar, { once: true });
btnZerar.addEventListener("click", zerar());

function zerar() {
  total = 0;
  saida.textContent = total;
}
```

**Critérios de pronto**

- O contador incrementa a cada clique, indefinidamente, inclusive quando o clique cai no texto "Somar".
- "Zerar" volta o contador a 0 apenas quando clicado.
- Nenhum erro no console ao carregar a página.
- Um comentário acima de cada correção diz qual era o bug e por que acontecia (uma frase cada).

<details><summary>Pistas</summary>

1. Abra o Console antes de qualquer coisa: uma das falhas aparece em vermelho no carregamento e tem a ver com a **ordem** em que o navegador lê `<head>` e `<body>`.
2. Releia a seção 12 sobre `target` × `currentTarget` e pense no `<span>` dentro do botão.
3. Uma opção passada ao `addEventListener` está fazendo exatamente o que promete.
4. Compare `zerar` com `zerar()` — o que está sendo passado como ouvinte?
</details>

### ⭐⭐ Lista de tarefas interativa
Tags: javascript, dom, eventos, projeto

Uma lista de tarefas é o "olá, mundo" das interfaces dinâmicas — e o exercício que mais revela se você entendeu o fluxo estado → renderização → eventos. Construa a sua, do zero, seguindo a arquitetura da seção 18, sem alterar o DOM "na mão" em nenhum momento: toda mudança na tela nasce de uma mudança no array seguida de `renderizar()`.

**Critérios de pronto**

- **Adicionar** pelo botão ou pela tecla Enter; texto vazio ou só com espaços é rejeitado com mensagem de erro visível.
- **Concluir**: clicar no checkbox alterna `concluida` no array e re-renderiza.
- **Excluir**: botão com `data-id`, tratado por delegação, com confirmação.
- **Editar**: duplo clique no texto o transforma em `<input>`; Enter confirma, Escape cancela, `blur` salva.
- **Filtrar**: três botões (Todas / Pendentes / Concluídas) alteram uma variável de estado e re-renderizam; o botão ativo recebe a classe `.ativo` e `aria-pressed="true"`.
- **Buscar**: campo de texto com `input` + debounce de 300 ms, filtrando pelo termo.
- **Ordenar**: `<select>` com as opções mais recentes, mais antigas e alfabética.
- **Limpar concluídas** remove todas de uma vez, com confirmação.
- **Contadores** de total, pendentes e concluídas, sempre atualizados.
- **Atalhos**: Ctrl+Enter adiciona; Escape limpa o campo.
- O arquivo `js/tarefas.js` está dividido nos blocos ESTADO, ELEMENTOS, DADOS, RENDERIZAÇÃO, EVENTOS e INICIALIZAÇÃO, nessa ordem.

<details><summary>Pistas</summary>

1. Comece pelo estado: `let tarefas = []`, `let filtroAtual = "todas"`, `let termoBusca = ""`, `let ordenacao = "recentes"`. Cada tarefa é `{ id, texto, concluida, criadaEm }` com `id: Date.now()`.
2. Escreva `obterTarefasVisiveis()` como uma cadeia: copia o array, aplica `filter` do filtro, `filter` da busca e `sort` da ordenação — e só ela é usada por `renderizar()`.
3. Para editar, guarde `idEmEdicao` no estado; `renderizar()` desenha um `<input>` em vez do texto quando o id bate. Enter/Escape/blur apenas alteram o estado e renderizam.
4. Um único `addEventListener("click")` na `<ul>` resolve checkbox, excluir e iniciar edição — use `closest("[data-acao]")` e um `switch`.
</details>

### ⭐⭐⭐ Quiz com pontuação e cronômetro
Tags: javascript, dom, eventos, acessibilidade

Sites de evento costumam ter um "quiz de conhecimentos" para engajar quem se inscreve. Construa um quiz de 10 perguntas de múltipla escolha sobre a Unidade 3 (você escreve as perguntas), com uma pergunta por tela, cronômetro de 20 segundos por questão, pontuação e um placar final. As perguntas vivem em um array de objetos; a tela é renderizada a partir do estado; não existe uma linha de HTML de pergunta escrita à mão.

**Critérios de pronto**

- Uma pergunta por vez, com quatro alternativas em `<button>`; responder ou esgotar o tempo avança automaticamente.
- Barra de tempo animada com CSS e atualizada por `setInterval`, que respeita `prefers-reduced-motion`.
- Pontuação: 10 pontos por acerto mais um bônus de 1 ponto por segundo restante; a fórmula está comentada no código.
- Navegação completa por teclado: teclas <kbd>1</kbd>–<kbd>4</kbd> selecionam a alternativa; <kbd>Enter</kbd> confirma.
- Ao terminar, um placar mostra acertos, erros, tempo médio e as questões erradas com a resposta certa.
- O quiz dispara um `CustomEvent("quizFinalizado", { detail })` com o resultado, e um script separado escuta esse evento para gravar o melhor placar em `localStorage`.
- Nenhum `innerHTML` recebe texto vindo das perguntas — tudo por `textContent`.

<details><summary>Pistas</summary>

1. Estado mínimo: `indiceAtual`, `pontuacao`, `respostas` (array), `segundosRestantes` e o id do `setInterval` — para poder cancelar com `clearInterval` ao responder.
2. Escreva `renderizarPergunta()` e `renderizarPlacar()` como funções separadas; `avancar()` decide qual chamar.
3. Para as teclas 1–4, ouça `keydown` em `document` e use `Number(e.key) - 1` como índice da alternativa — mas ignore quando o quiz não estiver em andamento.
4. `localStorage.setItem("quiz:melhor", JSON.stringify(detail))` no ouvinte do evento personalizado; leia com `JSON.parse` ao carregar. A próxima aula aprofunda o `localStorage`.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `Uncaught TypeError: Cannot read properties of null (reading 'addEventListener')` | `querySelector` não encontrou o elemento: seletor errado ou script no `<head>` sem `defer` | Confira o seletor no Console com `$$("seletor")`; coloque `defer` na tag `<script>` |
| Clicar no botão não faz nada e não há erro | `addEventListener("click", fn())` — a função foi chamada no registro e o retorno (`undefined`) virou o ouvinte | Passe a referência `fn`, sem parênteses |
| Página recarrega ao enviar o formulário e "os dados somem" | Falta `e.preventDefault()` no ouvinte de `submit` | Chame `e.preventDefault()` na primeira linha do ouvinte |
| Ouvinte registrado no botão, mas Enter no campo envia o formulário sem passar por ele | O evento certo é `submit` no `<form>`, não `click` no botão | Ouça `submit` no formulário |
| Itens criados pelo JavaScript não reagem ao clique | Ouvintes foram registrados antes de os elementos existirem | Use delegação: um ouvinte no contêiner + `closest()` |
| `e.target.dataset.id` é `undefined` em alguns cliques | O clique caiu em um filho do botão (ícone, `<span>`) — `target` é o filho | Use `e.target.closest("button[data-id]")` |
| `if (botao.dataset.id === produto.id)` nunca é verdadeiro | `dataset` sempre devolve string; `produto.id` é número | Converta com `Number(botao.dataset.id)` |
| `removeEventListener` não remove nada | Foi passada uma função anônima diferente da registrada | Nomeie a função e passe a mesma referência nos dois lugares |
| Busca ao digitar trava a página em listas grandes | Um filtro pesado roda a cada tecla | Envolva o ouvinte em `debounce(fn, 300)` |
| `<div onclick>` não funciona com Tab/Enter nem é lido pelo leitor de tela | `div` não é focável nem tem semântica de controle | Troque por `<button type="button">` |
| Menu abre e fecha no mesmo clique | O clique no botão borbulha até o ouvinte de "clique fora" em `document` | Verifique `botao.contains(e.target)` antes de fechar (ou não use `stopPropagation`) |

## 🏠 Atividade assíncrona (1 h)

**Parte 1 — Leitura (15 min).** FLANAGAN, *JavaScript: o guia definitivo*, capítulos de funções, de scripting de documentos e de eventos. MILETTO & BERTAGNOLLI, *Desenvolvimento de software II*, capítulo de interação com o usuário. Na MDN em português, o guia "Introdução a eventos" (link em Para aprofundar).

**Parte 2 — Entrega (40 min).** No seu **projeto autoral**:

1. O menu mobile funcionando com clique, <kbd>Esc</kbd> e clique fora, com `aria-expanded` sincronizado (como no Mão na massa).
2. A listagem principal do seu domínio (produtos, quadras, vagas, pratos, pescarias) **renderizada a partir de um array** de pelo menos 6 objetos, com estado vazio tratado.
3. Ao menos um filtro por botões usando delegação de eventos.
4. Os exercícios **B7** (contador de caracteres, aplicado ao seu formulário de contato) e **B8** (lista com subir/descer/excluir) em uma pasta `exercicios/aula-13/`.

**Critério de pronto:** nenhuma página do projeto mostra erro no Console; a listagem some do "Exibir código-fonte" e aparece na aba Elements; o menu abre e fecha só com o teclado.

**Parte 3 — Fórum (5 min).** No fórum "Delegação salva", explique, com um trecho do seu projeto, um problema que só a delegação de eventos resolve bem — e o que aconteceria sem ela.

**Entrega:** commit + push e link do repositório (ou `.zip`) no SIGAA.

## ✅ Checkpoint do projeto

- [ ] `js/app.js` carregado com `defer` em todas as páginas, sem erro no Console.
- [ ] Botão hambúrguer com `aria-expanded`, `aria-controls` e `aria-label`; menu abre/fecha por clique, <kbd>Esc</kbd>, clique fora e `resize`.
- [ ] Link da página atual marcado com `aria-current="page"` pelo JavaScript.
- [ ] Listagem principal renderizada a partir de um array de objetos, com `textContent` (nunca `innerHTML` para dados) e estado vazio tratado.
- [ ] Filtro por botões com um único ouvinte (delegação) e `aria-pressed` atualizado.
- [ ] Nenhum `var`, nenhum `onclick` no HTML, nenhum `<div>` clicável.
- [ ] Código organizado nos blocos ESTADO → ELEMENTOS → DADOS → RENDERIZAÇÃO → EVENTOS → INICIALIZAÇÃO.

## 📚 Para aprofundar

- MDN — Document Object Model (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Web/API/Document_Object_Model> — a visão geral da árvore e das interfaces `Document`, `Element` e `Node`.
- MDN — Introdução a eventos (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Learn_web_development/Core/Scripting/Events> — o guia introdutório com os mesmos exemplos de propagação e delegação desta aula.
- MDN — `EventTarget.addEventListener` (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Web/API/EventTarget/addEventListener> — todas as opções (`once`, `capture`, `passive`, `signal`).
- MDN — Arrow functions (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Functions/Arrow_functions> — quando **não** usar (métodos com `this`).
- MDN — `Element.closest` (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Web/API/Element/closest> — o método que torna a delegação robusta.
- WHATWG — DOM Living Standard: <https://dom.spec.whatwg.org/#events> — a especificação oficial das fases de propagação, para quem quer ver a fonte.
- FLANAGAN, David. *JavaScript: o guia definitivo*. Bookman, 2014 — capítulos sobre funções, scripting de documentos e tratamento de eventos.
- STEFANOV, Stoyan. *Padrões JavaScript*. Novatec, 2010 — padrões de callbacks e de organização de código em módulos.
- MILETTO, Evandro M.; BERTAGNOLLI, Silvia C. *Desenvolvimento de software II*. Bookman, 2014 — capítulo de interação com o usuário.

Na próxima aula, o formulário de inscrição do evento ganha validação campo a campo com mensagens acessíveis, expressões regulares para CPF, telefone e e-mail, e a programação passa a ter busca, filtro e ordenação em tempo real — tudo construído sobre as funções, o DOM e os eventos de hoje.
