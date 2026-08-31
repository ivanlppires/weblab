# Aula 09 — Promises e async/await

> **Nível 2 — Desenvolvimento Web** · Unidade 2: Web dinâmica client-side
> WebLab · UNEMAT — Campus Sinop
> **Tempo estimado:** 3 blocos de 50 min + 1 h de prática

Até agora todos os dados do Café Cerrado estavam prontos no momento em que a página abria: o array `produtos` já existia dentro do `js/app.js`, e renderizar os cards era uma questão de percorrer o que já estava na memória. No mundo real isso não acontece. Os dados moram em outro computador, do outro lado de uma rede que pode estar rápida, lenta ou fora do ar — e o navegador não pode parar tudo para esperar. Hoje você aprende o mecanismo que o JavaScript inventou para lidar com valores que ainda não chegaram: a **Promise**, e a sintaxe que a tornou confortável, o **async/await**.

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Explicar por que o JavaScript do navegador roda em uma única thread e o que o **event loop** faz com as tarefas que não cabem nela.
- Prever a ordem de execução de um trecho que mistura código síncrono, `setTimeout` e Promises, distinguindo **tarefas** de **microtarefas**.
- Identificar os três estados de uma Promise (`pending`, `fulfilled`, `rejected`) e criar uma Promise própria com `new Promise(resolve, reject)`.
- Consumir Promises com `.then()`, `.catch()` e `.finally()`, e reescrever a mesma cadeia com `async/await` e `try/catch/finally`.
- Implementar o padrão de interface **carregando → sucesso → erro → vazio**, com feedback acessível para leitores de tela.
- Escolher entre `Promise.all`, `Promise.allSettled`, `Promise.race` e `Promise.any` conforme o que a tela precisa fazer, e medir o ganho do paralelismo.
- Depurar código assíncrono no DevTools: reconhecer `Promise { <pending> }`, ler um `Uncaught (in promise)` e simular rede lenta.

## 📋 Pré-requisitos

- [ ] Repositório `cafe-cerrado` clonado e funcionando, com `index.html`, `cardapio.html`, `contato.html`, `css/estilo.css` e `js/app.js`.
- [ ] O array `produtos` de objetos `{ id, nome, categoria, preco, descricao, imagem }` renderizado como cards em `cardapio.html` (Aula 07).
- [ ] Busca por nome, filtro por categoria e ordenação por preço funcionando com `filter`, `sort` e `map` (Aula 08).
- [ ] VS Code com a extensão **Live Server** — abra o projeto sempre por `http://127.0.0.1`, nunca por `file://` (na próxima aula isso deixa de ser recomendação e vira obrigação).
- [ ] Navegador com DevTools e a aba **Network** disponível (vamos simular conexão lenta nela).

> Na aula passada as funções deixaram de ser blocos de código e viraram valores: você passou arrow functions para `filter`, `sort`, `map` e `reduce`, e viu o `setTimeout` receber um callback que dispara depois. Hoje o "depois" vira o assunto principal. Você vai entender por que o JavaScript não pode simplesmente parar e esperar, conhecer o objeto que representa um valor futuro e refatorar o cardápio do Café Cerrado para que ele nasça de uma fonte de dados que demora — e que às vezes falha.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Uma thread só; event loop, tarefas e microtarefas; callbacks e seus limites; a Promise e seus três estados |
| 2 | 50 min | `.then/.catch/.finally`; `async/await`; `try/catch`; onde os erros assíncronos caem; padrão carregando/sucesso/erro/vazio |
| 3 | 50 min | `Promise.all`, `allSettled`, `race` e `any`; Mão na massa no Café Cerrado; laboratório |

## 1. Por que o JavaScript não pode esperar

### 1.1 Uma thread só, e ela também desenha a tela

O JavaScript do navegador roda em **uma única thread** — a mesma que calcula o layout, pinta os pixels, responde ao clique, rola a página e processa a digitação. Isso é uma decisão de projeto antiga, e ela tem uma consequência brutal: **enquanto o seu código roda, nada mais acontece na página**.

Não é uma metáfora. Abra qualquer site, abra o console (<kbd>F12</kbd>) e cole isto:

```js
console.log("1 — começou");

const limite = Date.now() + 3000;
while (Date.now() < limite) {
  // Laço vazio de propósito: segura a única thread por 3 segundos.
}

console.log("2 — terminou");
```

Durante esses três segundos, tente rolar a página, clicar em um link, selecionar um texto. Nada responde. O cursor pode até virar uma ampulheta. A aba está viva, mas surda.

> **🔬 Investigue**
> Rode o trecho acima em uma página com alguma animação CSS visível (o próprio WebLab serve). Observe: a animação **congela** durante os 3 segundos e depois "salta" para onde deveria estar. Agora troque `3000` por `300` e repita. Em 300 ms a maioria das pessoas não percebe travamento; a partir de ~100 ms de bloqueio, uma interação já parece "pesada". Guarde esse número: é o orçamento de tempo que você tem para qualquer trabalho síncrono.

Agora pense numa requisição de rede. Buscar dados de um servidor leva de 50 ms (rede boa, servidor perto) a vários segundos (4G ruim no meio do Mato Grosso, servidor nos Estados Unidos). Se essa espera fosse síncrona, cada carregamento de cardápio congelaria a página inteira. Inaceitável.

### 1.2 A saída: delegar e seguir em frente

A plataforma resolve isso assim: operações lentas **não** são executadas pelo seu código. Você as **entrega ao navegador** (que tem outras threads, escritas em C++) junto com uma instrução: "quando terminar, execute esta função". Seu código continua rodando na hora.

```js
console.log("1 — início");

setTimeout(() => console.log("3 — callback, mesmo com 0 ms de espera"), 0);

console.log("2 — fim do script");
```

Saída, sempre nessa ordem:

```text
1 — início
2 — fim do script
3 — callback, mesmo com 0 ms de espera
```

Repare no detalhe que incomoda todo mundo na primeira vez: mesmo pedindo `0` milissegundos, o callback só roda **depois** que todo o código síncrono terminou. O `0` não significa "agora"; significa "na primeira oportunidade depois que a thread ficar livre".

### 1.3 Por baixo do capô: pilha, filas e o event loop

O mecanismo que coordena isso tem quatro peças. Vale conhecer os nomes, porque eles aparecem em toda discussão séria sobre performance web.

| Peça | O que é | Quem coloca coisas lá |
|---|---|---|
| Pilha de chamadas | As funções em execução agora | O motor JS, ao chamar funções |
| Fila de tarefas | Callbacks aguardando a vez | `setTimeout`, eventos, rede |
| Fila de microtarefas | Callbacks com prioridade | `.then` de Promises |
| Event loop | O laço que move da fila para a pilha | O navegador, continuamente |

O event loop faz sempre a mesma coisa, para sempre: *se a pilha estiver vazia, esvazie toda a fila de microtarefas; depois pegue uma tarefa da fila de tarefas e execute; repita*.

A prioridade das microtarefas é observável:

```js
console.log("1 — síncrono");

setTimeout(() => console.log("4 — tarefa (setTimeout 0)"), 0);

Promise.resolve().then(() => console.log("3 — microtarefa (Promise)"));

console.log("2 — síncrono");
```

Saída: `1`, `2`, `3`, `4`. As duas linhas síncronas rodam primeiro (elas estão na pilha). Depois o event loop esvazia as microtarefas — a Promise. Só então pega a próxima tarefa — o `setTimeout`.

> **🔎 Por baixo do capô**
> Entre esvaziar as microtarefas e pegar a próxima tarefa, o navegador tem a chance de **renderizar**: recalcular estilos, fazer layout e pintar. É por isso que uma cadeia infinita de microtarefas trava a tela tanto quanto um `while` infinito, enquanto uma cadeia de `setTimeout` deixa a página respirar entre uma e outra. Se você algum dia precisar processar 100 mil itens sem congelar a interface, a solução é fatiar o trabalho em tarefas, não em microtarefas.

> **📌 Vale gravar**
> Saber prever a saída de um trecho que mistura `console.log` síncrono, `setTimeout(fn, 0)` e `Promise.resolve().then(fn)` é questão clássica. A regra em uma frase: **síncrono primeiro, depois microtarefas, depois tarefas** — e o número em milissegundos do `setTimeout` é um mínimo, nunca uma garantia.

## 2. Callbacks: a primeira solução, e por que ela não bastou

Antes das Promises, "avise-me quando terminar" se escrevia passando uma função. Você já faz isso desde a Aula 07 com `addEventListener`, e desde a Aula 08 com `setTimeout`.

### 2.1 O padrão erro-primeiro

Como uma operação assíncrona pode falhar, a comunidade padronizou uma convenção: o callback recebe o erro como **primeiro** parâmetro e o resultado como segundo. Se o primeiro for `null`, deu certo.

```js
// Exemplo didático: fonte de dados fake com callback erro-primeiro.
function buscarProdutosComCallback(aoTerminar) {
  setTimeout(() => {
    const deuErro = Math.random() < 0.3;
    if (deuErro) {
      aoTerminar(new Error("Servidor do cardápio fora do ar"), null);
      return;
    }
    aoTerminar(null, ["Espresso do Cerrado", "Coado da Casa"]);
  }, 800);
}

buscarProdutosComCallback((erro, nomes) => {
  if (erro) {
    console.error("Falhou:", erro.message);
    return;
  }
  console.log("Chegaram:", nomes);
});
```

Funciona. O problema aparece quando uma operação depende da anterior.

### 2.2 A pirâmide da desgraça

Imagine que, para montar a tela do cardápio, você precise: buscar as categorias, depois buscar os produtos da primeira categoria, depois buscar as avaliações do produto mais vendido. Cada passo depende do anterior. Com callbacks:

```js
// Exemplo do que NÃO queremos escrever: cada nível aninha mais um.
buscarCategorias((erro, categorias) => {
  if (erro) {
    mostrarErro(erro);
    return;
  }
  buscarProdutosDaCategoria(categorias[0], (erroProdutos, produtos) => {
    if (erroProdutos) {
      mostrarErro(erroProdutos);
      return;
    }
    buscarAvaliacoes(produtos[0], (erroAvaliacoes, avaliacoes) => {
      if (erroAvaliacoes) {
        mostrarErro(erroAvaliacoes);
        return;
      }
      renderizar(produtos, avaliacoes);
    });
  });
});
```

Três operações, e o código já anda para a direita como uma escada. Com cinco ou seis, vira o famoso **callback hell**: difícil de ler, difícil de reordenar e, sobretudo, difícil de tratar erro — repare que o tratamento de falha está repetido três vezes, com nomes de variável artificialmente diferentes.

### 2.3 O problema mais sutil: inversão de controle

Há um incômodo pior que a estética. Quando você passa um callback para uma função de terceiros, você entrega o controle: **quem garante** que ela vai chamar o seu callback exatamente uma vez? Uma biblioteca com bug pode chamar duas vezes (e o seu carrinho ganha dois itens), nunca (e a tela fica em "Carregando…" para sempre), ou de forma síncrona quando você esperava assíncrona.

A Promise resolve isso pelo design: um objeto Promise só muda de estado **uma vez**, e essa mudança é irreversível. Quem cria a Promise controla o valor; quem consome controla o que fazer com ele. Ninguém precisa confiar em ninguém.

## 3. Promise: o contrato de um valor futuro

Uma **Promise** é um objeto que representa um valor que ainda não existe, mas vai existir — ou vai falhar tentando. É um comprovante, um número de protocolo: você não tem o café ainda, mas tem a garantia de que ele será entregue ou de que alguém virá dizer que acabou.

### 3.1 Três estados, uma transição só

| Estado | Significado | O que dispara |
|---|---|---|
| `pending` | Pendente — a operação está em andamento | nada ainda |
| `fulfilled` | Resolvida — o valor chegou | o `.then()` |
| `rejected` | Rejeitada — a operação falhou | o `.catch()` |

Uma Promise nasce `pending` e vai **uma única vez** para `fulfilled` ou `rejected`. Depois disso está *settled* (assentada) e nunca mais muda. Chamar `resolve()` duas vezes não faz nada na segunda; chamar `reject()` depois de `resolve()` também não.

### 3.2 Criando uma Promise para entender o mecanismo

No dia a dia você quase sempre **consome** Promises que outra pessoa criou (`fetch`, APIs de banco de dados, bibliotecas). Mas criar uma à mão desmistifica o objeto — e é exatamente o que faremos no Café Cerrado, para simular a demora da rede antes de termos rede de verdade.

O construtor recebe uma função chamada **executor**, que roda imediatamente e recebe duas funções: `resolve` (entregar o valor) e `reject` (entregar o erro).

```js
// Exemplo: uma fonte de dados que demora 1,5 s e pode falhar.
const catalogo = [
  { id: 1, nome: "Espresso do Cerrado", preco: 6 },
  { id: 2, nome: "Coado da Casa", preco: 8.5 },
];

function buscarProduto(id) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const produto = catalogo.find((item) => item.id === id);
      if (produto) {
        resolve(produto);
      } else {
        reject(new Error(`Produto ${id} não encontrado`));
      }
    }, 1500);
  });
}

console.log(buscarProduto(1));
```

O `console.log` da última linha imprime `Promise { <pending> }` — porque o valor ainda não chegou. **Guarde essa imagem**: sempre que você vir `Promise { <pending> }` no console, é sinal de que você está olhando para o comprovante em vez de olhar para o café.

> **⚠️ Atenção**
> Sempre rejeite com um objeto `Error` (`reject(new Error("..."))`), nunca com uma string. O `Error` carrega `message`, `name` e a pilha de chamadas — sem ele, você perde a informação de **onde** a falha nasceu, que é justamente o que você vai precisar às 23h de um dia de entrega.

### 3.3 Consumindo com `.then`, `.catch` e `.finally`

```js
buscarProduto(1)
  .then((produto) => {
    console.log("Chegou:", produto.nome);
  })
  .catch((erro) => {
    console.error("Falhou:", erro.message);
  })
  .finally(() => {
    console.log("Terminou — com sucesso ou com falha");
  });
```

Três métodos, três papéis:

- `.then(aoResolver)` — roda quando a Promise resolve, recebendo o valor.
- `.catch(aoRejeitar)` — roda quando a Promise (ou qualquer `.then` anterior da cadeia) falha, recebendo o erro.
- `.finally(sempre)` — roda nos dois casos, sem receber nada. É o lugar certo para "esconder o Carregando…".

### 3.4 Encadeamento: a escada vira uma lista

O que salva a legibilidade é uma regra simples: **`.then` devolve uma nova Promise**. Se o callback do `.then` retornar um valor comum, a próxima Promise resolve com esse valor. Se retornar **outra Promise**, a cadeia espera por ela. É isso que achata a pirâmide.

```js
buscarProduto(1)
  .then((produto) => {
    console.log("Primeiro:", produto.nome);
    return buscarProduto(2);      // retornar uma Promise encadeia a próxima etapa
  })
  .then((outro) => {
    console.log("Segundo:", outro.nome);
    return outro.preco * 2;       // retornar um valor comum também funciona
  })
  .then((dobro) => console.log("Dobro do preço:", dobro))
  .catch((erro) => console.error("Algo na cadeia falhou:", erro.message))
  .finally(() => console.log("Fim da cadeia"));
```

Compare com a pirâmide da seção 2.2: o código desce em vez de andar para a direita, e **um único `.catch` cobre todos os passos**. Se qualquer etapa rejeitar, a cadeia pula direto para o `.catch`, ignorando os `.then` intermediários — igualzinho ao que um `try/catch` faz com código síncrono.

> **🧠 Você sabia?**
> Promises não nasceram no JavaScript nem em 2015. O conceito de *promise* / *future* é dos anos 1970, em linguagens de pesquisa como MultiLisp. Na web, cada biblioteca tinha a sua versão incompatível — o `$.Deferred` do jQuery, o `Q`, o `when.js`, o `bluebird`. Em 2012 a comunidade escreveu a especificação aberta **Promises/A+**, que define em detalhe como o `.then` deve se comportar; o ES2015 padronizou o objeto `Promise` seguindo essa especificação. É por isso que qualquer objeto com um método `.then` compatível — um "thenable" — funciona dentro de um `await` até hoje, mesmo vindo de uma biblioteca antiga.

### 3.5 Um detalhe que confunde: o `.catch` no lugar errado

A ordem importa. Um `.catch()` só enxerga o que aconteceu **antes** dele na cadeia:

```js
// (a) o .catch cobre os dois .then
buscarProduto(99)
  .then((p) => console.log(p.nome))
  .then(() => console.log("segundo passo"))
  .catch((erro) => console.error("pego:", erro.message));

// (b) o .catch NÃO cobre o .then que vem depois dele
buscarProduto(99)
  .catch((erro) => console.error("pego:", erro.message))
  .then(() => console.log("este .then roda mesmo depois da falha"));
```

No caso (b), o `.then` final roda normalmente, porque o `.catch` "consertou" a cadeia: ele devolveu uma Promise resolvida (com `undefined`). Isso é útil de propósito às vezes — é assim que se implementa um valor padrão em caso de falha — mas pega desprevenido quem não sabe.

## 4. async/await: assíncrono com cara de síncrono

O ES2017 acrescentou açúcar sintático sobre Promises. Não é um mecanismo novo: por baixo, tudo continua sendo Promise, microtarefa e event loop. O que muda é a leitura.

Duas palavras-chave, duas regras:

- **`async`** antes de uma função faz com que ela **sempre** retorne uma Promise, aconteça o que acontecer.
- **`await`** pausa a execução **daquela função** até a Promise resolver, e entrega o valor. Enquanto isso, a thread fica livre para o resto da página.

```js
async function exibirProduto(id) {
  const produto = await buscarProduto(id);
  console.log("Chegou:", produto.nome);
  return produto;
}

exibirProduto(1);
```

Compare a mesma lógica da seção 3.4 nas duas sintaxes:

```js
// Com .then
function mostrarDois() {
  return buscarProduto(1)
    .then((primeiro) => {
      console.log("Primeiro:", primeiro.nome);
      return buscarProduto(2);
    })
    .then((segundo) => {
      console.log("Segundo:", segundo.nome);
      return segundo.preco * 2;
    });
}

// Com async/await — mesma coisa, sem aninhamento e sem callbacks
async function mostrarDoisComAwait() {
  const primeiro = await buscarProduto(1);
  console.log("Primeiro:", primeiro.nome);

  const segundo = await buscarProduto(2);
  console.log("Segundo:", segundo.nome);

  return segundo.preco * 2;
}
```

A segunda versão lê de cima para baixo, como qualquer código que você já escreveu. É por isso que ela virou o padrão da indústria — e é a que usaremos no resto do curso.

### 4.1 `async` sempre devolve uma Promise

Isto surpreende quase todo mundo:

```js
async function numero() {
  return 42;
}

console.log(numero());                  // uma Promise já resolvida — não o número 42
numero().then((n) => console.log(n));   // 42
```

Uma função `async` **embrulha** o retorno numa Promise. Consequência prática: quem chama uma função `async` precisa lidar com uma Promise — com `await` (se estiver dentro de outra `async`) ou com `.then`.

### 4.2 `await` pausa a função, não a página

Este é o mal-entendido número um da turma. Quando o motor encontra um `await`, ele:

1. Registra o resto da função como uma continuação (uma microtarefa).
2. **Devolve o controle** para quem chamou a função.
3. Volta a executar a função só quando a Promise assentar.

Ou seja: a página continua rolando, animando e respondendo a cliques durante o `await`. Só aquela função está parada.

```js
async function demonstrar() {
  console.log("A — antes do await");
  await buscarProduto(1);
  console.log("C — depois do await");
}

demonstrar();
console.log("B — esta linha roda antes do C");
```

Saída: `A`, `B`, `C`. A linha `B` está fora da função e não espera nada.

### 4.3 `try/catch/finally`: erro assíncrono tratado como erro comum

Com `await`, uma Promise rejeitada **lança uma exceção** no ponto do `await`. Isso significa que você trata falha de rede com a mesma estrutura que trata qualquer outro erro:

```js
async function exibirProdutoSeguro(id) {
  try {
    const produto = await buscarProduto(id);
    console.log("Chegou:", produto.nome);
    return produto;
  } catch (erro) {
    console.error("Falhou:", erro.message);
    return null;
  } finally {
    console.log("Terminou — com sucesso ou com falha");
  }
}
```

O mapeamento é direto: `.then` → o corpo do `try`; `.catch` → o bloco `catch`; `.finally` → o bloco `finally`.

### 4.4 Os dois erros que a turma inteira comete

**Erro 1 — esquecer o `await`.**

```js
async function errado() {
  const produto = buscarProduto(1);   // faltou o await
  console.log(produto.nome);          // undefined
}
```

`produto` recebe a Promise, não o objeto. `produto.nome` é `undefined` porque uma Promise não tem propriedade `nome`. O sintoma no console é sempre o mesmo: `Promise { <pending> }` ou `undefined` onde você esperava um dado.

**Erro 2 — usar `await` fora de uma função `async`.**

```js
function tambemErrado() {
  const produto = await buscarProduto(1);
  console.log(produto.nome);
}
```

O navegador nem chega a rodar: `SyntaxError: await is only valid in async functions and the top level bodies of modules`. A mensagem entrega a exceção da regra — em um **módulo ES** (`<script type="module">`), `await` funciona no nível superior do arquivo, sem função nenhuma. Você vai usar isso na próxima aula.

> **💡 Dica**
> Configure o VS Code para avisar antes de o navegador reclamar: com o arquivo `.js` aberto, um `await` sem `async` já aparece sublinhado em vermelho. E crie o reflexo de escrever `async` e `await` juntos, no mesmo momento — como quem escreve o `}` logo depois do `{`.

## 5. Onde os erros assíncronos caem (e onde eles se perdem)

### 5.1 `throw` dentro de `async` vira `reject`

```js
async function validarPedido(quantidade) {
  if (quantidade <= 0) {
    throw new Error("Quantidade precisa ser maior que zero");
  }
  return quantidade;
}

validarPedido(0)
  .catch((erro) => console.error("Rejeitou:", erro.message));
```

Um `throw` dentro de uma função `async` não estoura na hora: ele **rejeita a Promise** que a função devolve. Por isso ele é capturável com `.catch()` ou com um `try/catch` de quem der `await`.

### 5.2 O erro que ninguém pegou

Se ninguém trata a rejeição, o navegador reclama sozinho no console:

```text
Uncaught (in promise) Error: Servidor do cardápio fora do ar
```

Nada quebra visivelmente — e é justamente esse o perigo. A tela fica em "Carregando…" para sempre e o usuário não faz ideia do porquê. Toda operação assíncrona que chega perto da interface precisa de um `catch`.

Para caçar esses casos em desenvolvimento, um ouvinte global ajuda:

```js
// Cole no console (ou no topo do app.js durante a depuração) para não perder rejeição nenhuma.
window.addEventListener("unhandledrejection", (evento) => {
  console.warn("Rejeição sem tratamento:", evento.reason);
});
```

### 5.3 Erro com contexto vale mais que erro genérico

"Erro ao carregar" não ajuda ninguém. Enriqueça a mensagem antes de repassá-la:

```js
async function carregarComContexto(id) {
  try {
    return await buscarProduto(id);
  } catch (causa) {
    throw new Error(`Não foi possível carregar o produto ${id}`, { cause: causa });
  }
}

carregarComContexto(99).catch((erro) => {
  console.error(erro.message);          // mensagem amigável, com o id
  console.error("Causa original:", erro.cause.message);   // o erro técnico preservado
});
```

Repare no `return await` dentro do `try`: sem o `await`, a Promise seria devolvida **antes** de falhar, e o `catch` local nunca rodaria. É uma das poucas situações em que `return await` não é redundante.

> **📌 Vale gravar**
> Duas confusões comuns: (1) "`await` bloqueia a página" é **falsa** — ele pausa apenas a função `async` onde está escrito; (2) "uma função `async` pode retornar um valor comum" é **falsa na prática** — o valor sai sempre embrulhado numa Promise.

## 6. O padrão de interface: carregando, sucesso, erro, vazio

Aqui está a parte que separa um trabalho de aluno de uma aplicação de verdade. Toda operação assíncrona que alimenta a tela tem **quatro** desfechos possíveis, e a interface precisa de uma resposta visual para cada um.

| Estado | O que o usuário vê | O que quase todo mundo esquece |
|---|---|---|
| Carregando | Mensagem ou esqueleto de conteúdo | Anunciar para leitores de tela |
| Sucesso | Os dados renderizados | Limpar a mensagem de carregando |
| Erro | Mensagem clara + ação de recuperação | Oferecer "tentar de novo" |
| Vazio | "Nenhum item encontrado" | Diferenciar de erro e de carregando |

O estado **vazio** merece atenção: uma busca que não encontra nada é um sucesso técnico (a operação funcionou) com resultado vazio. Mostrar tela em branco nesse caso faz o usuário achar que o site quebrou.

### 6.1 Feedback acessível

Uma pessoa que usa leitor de tela não vê o spinner girar. Para que a mudança seja anunciada, a região de status precisa de atributos ARIA:

```html
<p id="status-cardapio" class="status" role="status" aria-live="polite">Carregando o cardápio…</p>
```

- `role="status"` marca o elemento como área de mensagens de estado.
- `aria-live="polite"` faz o leitor anunciar a mudança **sem interromper** o que ele está lendo. Use `assertive` só para emergências.

E na região que está sendo preenchida, `aria-busy` avisa que o conteúdo está em construção:

```js
elementoDaLista.setAttribute("aria-busy", "true");
// depois de renderizar:
elementoDaLista.setAttribute("aria-busy", "false");
```

> **💡 Dica**
> O elemento com `aria-live` precisa existir no HTML **antes** de a mensagem chegar. Se você criar o `<p>` e o texto ao mesmo tempo, muitos leitores de tela não anunciam nada. Deixe o parágrafo vazio na página e troque só o `textContent`.

### 6.2 A corrida de respostas

Um problema que só aparece com rede lenta: o usuário digita "ca", a busca dispara; digita "caf", dispara de novo; digita "café", dispara a terceira. Se a primeira requisição for a mais lenta, ela chega **por último** e sobrescreve o resultado certo com o resultado velho.

A defesa mais simples é numerar as requisições e ignorar as respostas atrasadas:

```js
let requisicaoAtual = 0;

async function buscarComProtecao(termo) {
  const minhaVez = ++requisicaoAtual;
  const resultado = await buscarProdutosPorTermo(termo);

  if (minhaVez !== requisicaoAtual) {
    return;   // chegou uma resposta mais nova depois desta: descarta
  }
  renderizarProdutos(resultado);
}
```

Guarde esse padrão: ele reaparece em toda tela de busca do mundo real, e é um dos desafios de hoje.

## 7. Fazendo várias coisas ao mesmo tempo

### 7.1 Sequencial soma; paralelo não

Duas operações independentes, cada uma de 1,5 s:

```js
async function compararTempos() {
  // SEQUENCIAL — ~3 s: a segunda só começa quando a primeira termina
  const inicioSequencial = performance.now();
  const produtosSeq = await buscarProdutos();
  const categoriasSeq = await buscarCategorias();
  console.log("sequencial:", Math.round(performance.now() - inicioSequencial), "ms",
    produtosSeq.length, "produtos e", categoriasSeq.length, "categorias");

  // PARALELO — ~1,5 s: as duas começam juntas
  const inicioParalelo = performance.now();
  const [produtosPar, categoriasPar] = await Promise.all([buscarProdutos(), buscarCategorias()]);
  console.log("paralelo:", Math.round(performance.now() - inicioParalelo), "ms",
    produtosPar.length, "produtos e", categoriasPar.length, "categorias");
}

compararTempos();
```

A diferença é gritante e **gratuita**: as duas buscas não dependem uma da outra, então não há motivo para enfileirá-las. A regra prática: **use `await` em sequência apenas quando o passo seguinte precisa do resultado do anterior.**

O detalhe técnico é que `Promise.all` não "dispara" nada: quem dispara é a chamada da função. Quando você escreve `buscarProdutos()` dentro do array, a operação **já começou**. O `Promise.all` só junta os comprovantes e espera todos.

### 7.2 Os quatro combinadores

| Combinador | Resolve quando | Rejeita quando |
|---|---|---|
| `Promise.all` | todas resolvem (array de valores) | a primeira que rejeitar |
| `Promise.allSettled` | todas assentam (array de status) | nunca |
| `Promise.race` | a primeira assenta (resolvendo ou rejeitando) | se a primeira a assentar rejeitou |
| `Promise.any` | a primeira que resolver | todas rejeitarem (`AggregateError`) |

**`Promise.all` — tudo ou nada.** Ideal quando a tela não faz sentido sem todas as partes:

```js
const [produtos, categorias] = await Promise.all([buscarProdutos(), buscarCategorias()]);
```

**`Promise.allSettled` — falhas parciais são aceitáveis.** Ideal para um painel em que cada bloco é independente:

```js
async function carregarPainel() {
  const resultados = await Promise.allSettled([buscarProdutos(), buscarCategorias()]);

  resultados.forEach((resultado, indice) => {
    if (resultado.status === "fulfilled") {
      console.log(indice, "ok:", resultado.value.length, "itens");
    } else {
      console.warn(indice, "falhou:", resultado.reason.message);
    }
  });
}
```

**`Promise.race` — o primeiro que chegar.** O uso clássico é impor um limite de tempo:

```js
function comLimiteDeTempo(promessa, milissegundos) {
  const estouro = new Promise((resolve, reject) => {
    setTimeout(() => reject(new Error(`Tempo esgotado (${milissegundos} ms)`)), milissegundos);
  });
  return Promise.race([promessa, estouro]);
}

async function carregarComLimite() {
  try {
    const produtos = await comLimiteDeTempo(buscarProdutos(), 3000);
    renderizarProdutos(produtos);
  } catch (erro) {
    console.error(erro.message);
  }
}
```

**`Promise.any` — o primeiro que der certo.** Útil quando há fontes alternativas: tente o servidor principal e o espelho, fique com quem responder primeiro **com sucesso**.

> **⚠️ Atenção**
> `Promise.race` com um timeout **não cancela** a operação original — ela continua rodando em segundo plano até terminar; você só parou de esperar por ela. Cancelamento de verdade exige `AbortController`, que aparece na próxima aula, junto com o `fetch`.

## 💻 Mão na massa — o cardápio do Café Cerrado que chega depois

Objetivo do dia: o array `produtos` sai de dentro do `js/app.js` e passa a vir de uma "fonte de dados" que demora, que pode falhar e que o resto do código só acessa por Promises. Quando trocarmos essa fonte por um `fetch` de verdade na próxima aula, **nenhuma linha do `app.js` precisará mudar** — é esse o ponto.

### Passo 1 — Criar `js/dados.js`, a fonte que finge ser um servidor

Crie o arquivo `js/dados.js` no repositório `cafe-cerrado`. O conteúdo é **exatamente** o array `produtos` que você escreveu na Aula 07 — os mesmos dez itens, os mesmos ids, os mesmos preços, as mesmas quatro categorias. Ele só muda de casa: sai do `js/app.js` e passa a ser entregue por funções que devolvem Promises.

```js
// cafe-cerrado/js/dados.js
// Fonte de dados simulada do Café Cerrado.
// Ela existe para treinar código assíncrono antes de termos um servidor de verdade:
// devolve Promises, demora de propósito e falha de vez em quando.

const CATALOGO = [
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

// As mesmas quatro categorias das Aulas 03 a 08, agora com id e rótulo separados:
// o id é a chave técnica (o que está em produto.categoria), o nome é o texto da tela.
const CATEGORIAS = [
  { id: "cafes", nome: "Cafés" },
  { id: "geladas", nome: "Bebidas geladas" },
  { id: "salgados", nome: "Salgados" },
  { id: "doces", nome: "Doces" },
];

// Probabilidade de falha simulada (0 = nunca falha, 1 = sempre falha).
// Deixe em 0.25 para ver os dois caminhos; zere quando for gravar um vídeo de demonstração.
const CHANCE_DE_FALHA = 0.25;

/**
 * Devolve uma Promise que resolve com uma cópia de `valor` depois de `atraso` ms,
 * ou rejeita com um Error se a "rede" simulada falhar.
 */
function responderComAtraso(valor, atraso, descricao) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (Math.random() < CHANCE_DE_FALHA) {
        reject(new Error(`Falha simulada de rede ao buscar ${descricao}`));
        return;
      }
      // Cópia rasa para ninguém alterar o catálogo original por acidente.
      resolve(valor.map((item) => ({ ...item })));
    }, atraso);
  });
}

function buscarProdutos() {
  return responderComAtraso(CATALOGO, 1200, "os produtos");
}

function buscarCategorias() {
  return responderComAtraso(CATEGORIAS, 800, "as categorias");
}

function buscarProdutoPorId(id) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const produto = CATALOGO.find((item) => item.id === Number(id));
      if (!produto) {
        reject(new Error(`Produto ${id} não encontrado`));
        return;
      }
      resolve({ ...produto });
    }, 600);
  });
}
```

> **💡 Dica**
> `CATALOGO` e `CATEGORIAS` em maiúsculas é uma convenção para constantes de configuração — não é regra da linguagem, mas ajuda a bater o olho e saber que aquilo não muda em tempo de execução.

> **⚠️ Atenção**
> Não invente produto novo aqui, não renomeie nenhum e não mexa nas chaves de categoria. Esses dez objetos são o **contrato do projeto**: eles viram `data/produtos.json` na Aula 10 e as linhas da sua API na Unidade 3. Qualquer diferença aqui vira um bug três aulas adiante, quando o filtro do front-end deixar de casar com o que o servidor devolve.

### Passo 2 — Carregar os dois arquivos, na ordem certa

Em `cardapio.html`, substitua o `<script>` único pelos dois arquivos. O atributo `defer` faz o navegador baixar os scripts em paralelo e executá-los **na ordem em que aparecem**, depois que o HTML terminou de ser lido:

```html
<!-- cafe-cerrado/cardapio.html — antes do </body> -->
<script src="js/dados.js" defer></script>
<script src="js/app.js" defer></script>
```

Faça o mesmo em `index.html` e `contato.html`. O `app.js` é o **mesmo arquivo** nas três páginas — ele continua ligando o botão de tema (Aula 07) e a validação do formulário de contato (Aula 07), e só monta o cardápio quando encontra a grade `#lista-produtos`. Manter o par de tags igual nas três páginas evita o erro clássico de esquecer uma linha em um arquivo e passar a tarde procurando por que "no contato não funciona".

> **⚠️ Atenção**
> A ordem importa: `app.js` usa funções declaradas em `dados.js`. Se você inverter as linhas, o console mostra `Uncaught ReferenceError: buscarProdutos is not defined`. E não troque `defer` por `async` aqui — `async` executa assim que cada arquivo terminar de baixar, **sem garantir ordem**.

### Passo 3 — Reservar o espaço do status e do botão de recuperação

O `cardapio.html` que você fechou na Aula 08 já tem quase tudo: o formulário `#controles-cardapio` com busca, filtro e ordenação, o parágrafo `#resumo-cardapio`, a grade `#lista-produtos`, o aviso `#cardapio-vazio`, o `<template id="template-produto">` e o painel do pedido. **Nada disso muda.** Faltam duas coisas: a região que anuncia o carregamento e o botão que oferece uma saída quando a busca falha.

Acrescente as duas linhas entre o resumo e a grade:

```html
<!-- cafe-cerrado/cardapio.html — entre o #resumo-cardapio e a grade de cards -->
<p class="status" id="status-cardapio" role="status" aria-live="polite"></p>

<button class="btn btn-cafe-vazado mb-3" type="button" id="tentar-de-novo" hidden>
  Tentar de novo
</button>
```

A região do cardápio fica assim (só as duas linhas marcadas com `<!-- novo -->` são de hoje):

```html
<!-- cafe-cerrado/cardapio.html — região do cardápio, versão da Aula 09 -->
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

  <p class="status" id="status-cardapio" role="status" aria-live="polite"></p>          <!-- novo -->

  <button class="btn btn-cafe-vazado mb-3" type="button" id="tentar-de-novo" hidden>    <!-- novo -->
    Tentar de novo
  </button>

  <div class="row row-cols-1 row-cols-sm-2 row-cols-lg-3 g-4" id="lista-produtos" aria-busy="false"></div>

  <p class="text-center text-secondary d-none" id="cardapio-vazio" role="status">
    Nenhum item do cardápio para mostrar.
  </p>
</section>
```

Repare que a grade ganhou `aria-busy="false"`: é o atributo que o JavaScript vai virar para `"true"` durante a espera. E note que existem agora **duas** regiões vivas com papéis diferentes — `#resumo-cardapio` fala sobre o resultado dos filtros ("3 de 10 itens…"), `#status-cardapio` fala sobre a operação ("Carregando o cardápio…", "Não foi possível carregar…"). Estado vazio e estado de erro deixam de se confundir porque cada um tem o seu lugar na tela.

### Passo 4 — O estilo do carregando

Acrescente ao final de `css/estilo.css`:

```css
/* cafe-cerrado/css/estilo.css — estados assíncronos (Aula 09) */
.status {
  min-height: 1.5rem;
  margin: 0.75rem 0;
  font-weight: 600;
}

.status--erro {
  color: #a4161a;
}

.status--vazio {
  color: var(--cor-texto-suave);
  font-weight: 500;
}

.esqueleto {
  height: 11rem;
  border-radius: var(--raio);
  background: linear-gradient(90deg, #e9e4dd 25%, #f5f1ec 50%, #e9e4dd 75%);
  background-size: 200% 100%;
  animation: brilho 1.2s linear infinite;
}

@keyframes brilho {
  from { background-position: 200% 0; }
  to   { background-position: -200% 0; }
}

@media (prefers-reduced-motion: reduce) {
  .esqueleto {
    animation: none;
    background: #e9e4dd;
  }
}
```

O bloco `prefers-reduced-motion` não é enfeite: é a mesma regra de acessibilidade da Aula 05, e vale para qualquer animação nova que você criar.

### Passo 5 — Refatorar `js/app.js`: os dados passam a chegar

Aqui está a diferença entre um profissional e um copiador de tutorial: **nada do que você escreveu nas Aulas 07 e 08 é apagado hoje.** O `<template>`, `criarCardProduto`, `renderizarProdutos`, `produtosVisiveis`, o objeto `ORDENADORES`, `atualizarResumo`, `render`, o carrinho inteiro (`adicionarAoCarrinho`, `removerDoCarrinho`, `totalDoCarrinho`, `renderizarCarrinho`), o `comAtraso`, a delegação de cliques, `iniciarTema` e `iniciarContato` continuam **byte por byte iguais**. Muda só a origem dos dados — quatro edições cirúrgicas.

**Edição 1 — o array deixa de ser literal.** No topo do `js/app.js`, apague as oitenta linhas do `const produtos = [ … ]` e o objeto `ROTULOS_CATEGORIA` escrito à mão. Eles agora moram no `js/dados.js`. No lugar deles:

```js
// cafe-cerrado/js/app.js — topo do arquivo (Aula 09)
// Os dados não estão mais aqui: eles chegam de js/dados.js, por Promise.

let produtos = [];                  // preenchido quando buscarProdutos() resolve
const ROTULOS_CATEGORIA = {};       // preenchido quando buscarCategorias() resolve
```

`let` no lugar de `const` porque `produtos` passa a ser **reatribuído** quando os dados chegam. `ROTULOS_CATEGORIA` continua `const`: o objeto é sempre o mesmo, ele só ganha chaves. E é por isso que `produtosVisiveis()`, `atualizarResumo()` e `adicionarAoCarrinho()` não precisam de uma vírgula sequer: elas leem `produtos` como sempre leram — só que agora o array começa vazio e enche depois.

O `formatadorMoeda` e a `formatarPreco` da Aula 07 ficam onde estão: formatação é assunto de tela, não de dados.

**Edição 2 — o filtro de categorias vem da fonte, não do array.** Na Aula 08, `preencherFiltroDeCategorias` deduzia as categorias com um `Set` sobre os produtos. Agora elas chegam prontas, com id e rótulo, e a mesma função aproveita para preencher o `ROTULOS_CATEGORIA` que os cards usam:

```js
function preencherFiltroDeCategorias(categorias) {
  const select = document.querySelector("#filtro-categoria");

  const opcoes = categorias.map((categoria) => {
    ROTULOS_CATEGORIA[categoria.id] = categoria.nome;   // rótulo do badge do card

    const opcao = document.createElement("option");
    opcao.value = categoria.id;
    opcao.textContent = categoria.nome;
    return opcao;
  });

  select.append(...opcoes);
}
```

Duas responsabilidades em uma função pequena, e nenhuma delas repetida em outro lugar: o nome legível de cada categoria passa a existir em **um** ponto do sistema, o `js/dados.js`. Quando a Unidade 3 trocar o `dados.js` por uma API, o rótulo vem do servidor e nada mais muda aqui.

**Edição 3 — três funções novas: status, esqueleto e carregamento.** Acrescente-as acima de `iniciarCardapio`:

```js
function mostrarStatus(mensagem, modificador = "") {
  const status = document.querySelector("#status-cardapio");
  status.textContent = mensagem;
  status.className = modificador ? `status ${modificador}` : "status";
}

function renderizarEsqueleto(quantidade) {
  const container = document.querySelector("#lista-produtos");
  container.replaceChildren();
  container.setAttribute("aria-busy", "true");

  const fragmento = document.createDocumentFragment();

  for (let i = 0; i < quantidade; i += 1) {
    const coluna = document.createElement("div");
    coluna.className = "col";

    const caixa = document.createElement("div");
    caixa.className = "esqueleto";
    caixa.setAttribute("aria-hidden", "true");   // decoração: o leitor de tela ignora

    coluna.appendChild(caixa);
    fragmento.appendChild(coluna);
  }

  container.appendChild(fragmento);
}

async function carregarCardapio() {
  const container = document.querySelector("#lista-produtos");
  const botaoTentarDeNovo = document.querySelector("#tentar-de-novo");

  botaoTentarDeNovo.hidden = true;
  document.querySelector("#cardapio-vazio").classList.add("d-none");
  mostrarStatus("Carregando o cardápio…");
  renderizarEsqueleto(6);

  const inicio = performance.now();

  try {
    const [produtosRecebidos, categorias] = await Promise.all([
      buscarProdutos(),
      buscarCategorias(),
    ]);

    produtos = produtosRecebidos;            // a variável declarada no topo do arquivo
    preencherFiltroDeCategorias(categorias);

    container.setAttribute("aria-busy", "false");
    mostrarStatus("");
    render();                                 // a mesma render() da Aula 08, sem alteração

    console.log(`Cardápio carregado em ${Math.round(performance.now() - inicio)} ms`);
  } catch (erro) {
    console.error(erro);
    container.replaceChildren();
    container.setAttribute("aria-busy", "false");
    document.querySelector("#resumo-cardapio").textContent = "";
    mostrarStatus("Não foi possível carregar o cardápio. Verifique sua conexão.", "status--erro");
    botaoTentarDeNovo.hidden = false;
    botaoTentarDeNovo.focus();                // quem navega por teclado não precisa procurar
  }
}
```

O `catch` faz cinco coisas, e nenhuma delas é decorativa: registra o erro técnico no console (para você), tira os esqueletos da tela (senão eles pulsam para sempre), desliga o `aria-busy`, mostra uma mensagem em português para a pessoa e oferece o caminho de volta. Um `catch` que só faz `console.error` é um `catch` que mente: a tela continua dizendo "Carregando…".

**Edição 4 — `iniciarCardapio` chama o carregamento.** É a única função da Aula 08 que muda, e muda em três linhas. Substitua-a inteira por esta versão:

```js
function iniciarCardapio() {
  const container = document.querySelector("#lista-produtos");
  if (!container) return; // não estamos no cardapio.html

  renderizarCarrinho();   // o pedido começa vazio e não depende da rede
  carregarCardapio();     // no lugar de preencherFiltroDeCategorias() + render()

  document.querySelector("#tentar-de-novo").addEventListener("click", () => {
    const select = document.querySelector("#filtro-categoria");
    select.length = 1;        // descarta as opções da tentativa anterior, mantém "Todas"
    select.value = "";
    estado.categoria = "";
    carregarCardapio();
  });

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

Compare com a versão da Aula 08: os oito ouvintes são idênticos, `estado.termo`, `estado.categoria` e `estado.ordenacao` continuam com os mesmos nomes, e a delegação segue apontando para os mesmos seletores. As três linhas novas são `carregarCardapio()` no lugar do par `preencherFiltroDeCategorias() + render()` e o ouvinte do botão "Tentar de novo".

E a chamada final do arquivo, escrita na Aula 07, continua exatamente como estava:

```js
function iniciar() {
  iniciarTema();
  iniciarCardapio();
  iniciarContato();
}

iniciar();
```

Note o que **não** aconteceu: a delegação de cliques foi registrada uma vez, em `iniciarCardapio`, e vale para cards que ainda nem existiam quando o ouvinte nasceu. É por isso que trocar todos os cards por Promises não quebrou o carrinho — o ouvinte está no contêiner, não nos cards. Essa decisão da Aula 07 é o que torna a refatoração de hoje tão pequena.

### Passo 6 — Como testar

1. Clique com o botão direito em `cardapio.html` no VS Code e escolha **Open with Live Server**. A URL precisa começar com `http://127.0.0.1`, não com `file://`.
2. Recarregue a página algumas vezes. Em cerca de três de cada quatro vezes você deve ver: os seis retângulos cinza pulsando por ~1,2 s, depois os **dez** cards reais, o `<select>` de categoria com cinco opções ("Todas" mais as quatro) e a mensagem de status sumindo.
3. Nas outras vezes, aparece **"Não foi possível carregar o cardápio"** em vermelho, os esqueletos somem e o botão **Tentar de novo** recebe o foco. Clique nele: o ciclo recomeça e o `<select>` não fica com categorias duplicadas.
4. Digite `caf` na busca: sobra um card, o Frappê de Café. Agora `zzz`: nenhum card, o aviso `#cardapio-vazio` aparece e o resumo diz "Nenhum item corresponde à sua busca." Esse é o estado **vazio** — texto neutro, sem botão de recuperação —, visivelmente diferente do estado de **erro** do passo anterior.
5. Clique duas vezes em "Adicionar ao pedido" no Coado da Casa e uma vez na Torta de Frango: o pedido mostra "Total: R$ 30,00" e o contador `3`. O carrinho da Aula 08 continua inteiro — se ele quebrou, alguma função foi apagada em vez de refatorada.
6. Abra `contato.html` e envie o formulário vazio: as mensagens de erro da Aula 07 continuam aparecendo e o foco vai para o primeiro campo inválido. A validação também sobreviveu.
7. No console, confira a linha `Cardápio carregado em N ms`. Ela deve ficar perto de **1200 ms**, não de 2000 ms: as duas buscas rodaram em paralelo. Para provar, troque temporariamente o `Promise.all` por dois `await` em sequência e recarregue — o número pula para cerca de 2000 ms.
8. Na aba **Network** do DevTools, mude a velocidade de "No throttling" para **Slow 4G** e recarregue. Os arquivos demoram mais para chegar, mas a página continua rolável durante toda a espera — a prova de que o `await` não bloqueia nada.

**Resultado esperado:** o cardápio nunca aparece "do nada"; ele sempre passa por um estado visível de carregamento, e qualquer falha resulta em mensagem clara com caminho de recuperação — sem tela branca e sem console silencioso. Busca, filtro, ordenação, carrinho e validação continuam funcionando como na Aula 08.

```bash
git add .
git commit -m "refactor: cardapio carregado por Promises com estados de carregando, erro e vazio"
git push
```

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Preveja a saída **sem rodar**, depois confira no console:

```js
console.log("A");
setTimeout(() => console.log("B"), 0);
Promise.resolve().then(() => console.log("C"));
console.log("D");
```

Escreva a ordem e justifique cada posição usando as palavras *pilha*, *microtarefa* e *tarefa*.

**A2.** O que cada `console.log` imprime? Explique a diferença em uma linha.

```js
async function valor() {
  return "café";
}

console.log(valor());
valor().then((v) => console.log(v));
```

**A3.** Este trecho tem um erro que o navegador recusa antes de rodar. Qual é a mensagem exata do console e como se conserta sem transformar a função em `async`?

```js
function mostrar() {
  const produto = await buscarProdutoPorId(1);
  console.log(produto.nome);
}
```

**A4.** Complete o código para que a mensagem "Carregando…" suma tanto no sucesso quanto na falha, usando **um único** método da cadeia de Promise:

```js
mostrarStatus("Carregando…");
buscarProdutos()
  .then((produtos) => renderizarProdutos(produtos))
  .catch((erro) => mostrarStatus(erro.message, "status--erro"));
```

**A5.** Em `carregarCardapio()`, o `Promise.all` recebe `[buscarProdutos(), buscarCategorias()]` — com os parênteses. Se alguém trocar por `[buscarProdutos, buscarCategorias]` (sem parênteses), o que acontece com o valor de `produtos` e `categorias`? A tela quebra ou apenas fica errada? Justifique.

**A6.** `buscarProdutos()` demora 1200 ms e `buscarCategorias()` demora 800 ms. Quanto tempo, aproximadamente, leva cada uma das três funções abaixo?

```js
async function bloco1() {
  await buscarProdutos();
  await buscarCategorias();
}

async function bloco2() {
  await Promise.all([buscarProdutos(), buscarCategorias()]);
}

async function bloco3() {
  await Promise.race([buscarProdutos(), buscarCategorias()]);
}
```

### Nível B — Aplicação

**B1.** Escreva `esperar(ms)`, uma função que devolve uma Promise que resolve (sem valor) depois de `ms` milissegundos, e use-a para imprimir três mensagens espaçadas de 1 segundo dentro de uma função `async`, sem nenhum `setTimeout` aninhado.

Resultado esperado: no console, "um", "dois" e "três" aparecem com um segundo de intervalo, e o código tem uma linha `await esperar(1000);` entre eles.

<details markdown="1">
<summary>Dica</summary>

O executor da Promise pode ignorar o `reject`: `new Promise((resolve) => setTimeout(resolve, ms))`. Como não há valor, você não precisa de variável para receber o `await`.
</details>

**B2.** No `js/dados.js`, acrescente `buscarAvaliacoes(idProduto)`, que resolve depois de 500 ms com um array de objetos `{ autor, nota, comentario }` (mínimo três avaliações para o produto 1) e rejeita com `Error` para qualquer outro id. Em `app.js`, crie `mostrarAvaliacoes(id)` que trate os dois casos.

Resultado esperado: `mostrarAvaliacoes(1)` imprime as avaliações; `mostrarAvaliacoes(4)` imprime uma mensagem amigável de erro no console — e **nenhuma** linha `Uncaught (in promise)` aparece.

<details markdown="1">
<summary>Dica</summary>

Copie a estrutura de `buscarProdutoPorId`. O `try/catch` de `mostrarAvaliacoes` é o que impede o `Uncaught (in promise)`.
</details>

**B3.** Converta a cadeia abaixo para `async/await` com `try/catch/finally`, preservando exatamente o mesmo comportamento (inclusive a ordem das mensagens):

```js
function carregar() {
  mostrarStatus("Carregando…");
  return buscarProdutos()
    .then((produtos) => {
      renderizarProdutos(produtos);
      return produtos.length;
    })
    .then((quantidade) => console.log("itens:", quantidade))
    .catch((erro) => mostrarStatus(erro.message, "status--erro"))
    .finally(() => console.log("fim"));
}
```

Resultado esperado: a versão nova roda com a mesma sequência de mensagens no caminho de sucesso e no de falha; force os dois cenários subindo `CHANCE_DE_FALHA` para `1` e baixando para `0`.

<details markdown="1">
<summary>Dica</summary>

Cada `.then` vira uma linha depois do `await`; o `.catch` vira o bloco `catch (erro)`; o `.finally` vira o bloco `finally`. Não esqueça o `async` na declaração.
</details>

**B4.** Implemente o estado **vazio** de verdade no seu projeto autoral: quando a busca não encontrar nada, além da mensagem, mostre um botão "Limpar filtros" que zera `estado.termo`, `estado.categoria` e os campos do formulário, e re-renderiza a lista completa.

Resultado esperado: buscar por `zzz` mostra a mensagem e o botão; clicar no botão devolve todos os itens e esconde o botão de novo.

<details markdown="1">
<summary>Dica</summary>

O botão pode ficar no HTML com `hidden`, como o "Tentar de novo". Ao limpar, lembre-se de atualizar também `document.querySelector("#busca").value` e o `value` do `#filtro-categoria` — o estado do objeto e o estado dos campos precisam andar juntos.
</details>

**B5.** Meça e documente. Crie no `app.js` uma função `medirCarregamento()` que rode a versão sequencial e a versão paralela do carregamento (cinco vezes cada) e imprima a média de cada uma com `performance.now()`.

Resultado esperado: duas linhas no console, algo como `sequencial: 2013 ms (média de 5)` e `paralelo: 1207 ms (média de 5)`, com a diferença aproximada de 800 ms — o tempo de `buscarCategorias`.

<details markdown="1">
<summary>Dica</summary>

Zere `CHANCE_DE_FALHA` antes de medir, senão uma rejeição derruba a rodada. Um laço `for` com `await` dentro acumula os tempos; divida pelo número de repetições no final.
</details>

### Nível C — Desafio

**C1.** Nem toda falha é permanente: uma rede instável costuma funcionar na segunda tentativa. Implemente em `js/dados.js` a função `comTentativas(criarPromessa, tentativas, esperaInicial)` que executa `criarPromessa()`, e em caso de rejeição tenta de novo, dobrando a espera a cada falha (500 ms, 1000 ms, 2000 ms) — o padrão conhecido como *exponential backoff*. Depois, envolva a chamada com um limite de tempo total usando `Promise.race`, de modo que a tela nunca fique presa em "Carregando…" por mais de 8 segundos.

Resultado esperado: com `CHANCE_DE_FALHA = 0.6`, o cardápio carrega na maioria das recargas (o console mostra as tentativas com `console.warn`); com `CHANCE_DE_FALHA = 1`, depois de três tentativas a tela mostra a mensagem de erro e o botão "Tentar de novo" em no máximo 8 segundos.

<details markdown="1">
<summary>Dica</summary>

O parâmetro precisa ser uma **função** que cria a Promise (`() => buscarProdutos()`), não a Promise pronta — uma Promise já rejeitada não pode ser "executada de novo". Um laço `for` com `try/catch` dentro de uma função `async` resolve: no `catch`, se ainda houver tentativas, `await esperar(espera)` e `espera *= 2`; se acabaram, `throw`. O limite total é o `comLimiteDeTempo` da seção 7.2 aplicado sobre o resultado de `comTentativas`.
</details>

## 🏆 Desafios

### ⭐ O cronômetro do cardápio
Tags: async, performance, devtools

Você trocou dois `await` em sequência por um `Promise.all` e o professor disse que ficou mais rápido. Mas "mais rápido" é opinião até virar número. Meça: quanto tempo, exatamente, o seu cardápio leva para aparecer nas duas versões? E o que acontece com esses números quando a conexão é ruim de verdade?

**Critérios de pronto**

- Uma função `medir(rotulo, tarefa)` no `app.js` imprime `rotulo` e o tempo em milissegundos usando `performance.now()`, arredondado para inteiro.
- O `README.md` do seu projeto autoral ganha uma tabela com três linhas — sequencial, paralelo e a diferença — para dois cenários da aba Network: "No throttling" e "Slow 4G".
- A tabela registra a **média de cinco medições** por cenário, não uma medição única, e o texto explica em duas linhas por que uma medição só não serve.
- Uma frase responde: quando a conexão piora, a vantagem do paralelo aumenta, diminui ou fica igual? Por quê?

<details markdown="1">
<summary>Pistas</summary>

1. `performance.now()` devolve milissegundos com casas decimais desde o carregamento da página — muito mais preciso que `Date.now()` para medir trechos curtos.
2. A aba Network tem um seletor de velocidade ("No throttling", "Slow 4G", "Fast 4G"). Ele também afeta o download dos seus próprios arquivos `.js`, então recarregue a página inteira entre as medições.
3. `console.table()` recebe um array de objetos e imprime uma tabela formatada no console — copiar de lá para o README é mais rápido que anotar à mão.
4. Para a última pergunta, pense no que é somado no caso sequencial: dois tempos de espera, cada um com a latência da rede embutida.
</details>

### ⭐⭐ A resposta que chega atrasada
Tags: async, javascript, bug, investigacao

Ative "Slow 4G" na aba Network, digite `a`, depois `ca`, depois `café` na busca do cardápio — rápido, como qualquer pessoa digita. De vez em quando a tela mostra o resultado de `a` embora o campo diga `café`. O bug não está na sua lógica de filtro: está no fato de que respostas de rede não chegam na ordem em que foram pedidas. Reproduza a falha de forma confiável, entenda por que ela acontece e conserte.

Para reproduzir, troque a busca local por uma busca "no servidor": acrescente ao `dados.js` uma função `buscarProdutosPorTermo(termo)` que espera um tempo **aleatório** entre 200 ms e 2000 ms antes de resolver com os produtos filtrados.

**Critérios de pronto**

- Um comentário no topo da função registra a sequência de teclas que reproduz o bug e o que aparece na tela quando ele ocorre.
- Depois da correção, digitar qualquer sequência rápida sempre termina exibindo o resultado do **último** termo digitado, mesmo com atrasos aleatórios.
- A correção descarta respostas obsoletas explicitamente (nada de "resolver" escondendo o problema com um `setTimeout` maior).
- Há também um *debounce*: enquanto a pessoa digita, a busca só dispara depois de 300 ms de pausa — e o README explica em três linhas a diferença entre o que o debounce resolve e o que o descarte de resposta obsoleta resolve.

<details markdown="1">
<summary>Pistas</summary>

1. `Math.random() * 1800 + 200` dá o atraso aleatório da faixa pedida.
2. A seção 6.2 mostra o padrão do contador de requisições. A variável do contador precisa viver **fora** da função, senão ela reinicia a cada chamada.
3. Debounce é `clearTimeout` seguido de `setTimeout`: cada tecla cancela o temporizador anterior. Ele reduz o número de requisições, mas **não** garante a ordem das que sobraram.
4. Para provar que o conserto funciona, imprima no console o termo de cada resposta que chega e marque com um prefixo as que foram descartadas.
</details>

### ⭐⭐ Carregando para quem não vê
Tags: acessibilidade, async, dom

Feche os olhos e navegue no seu cardápio usando só o teclado e o leitor de tela do sistema (NVDA no Windows, Orca no Linux, VoiceOver no macOS). Enquanto os dados carregam, você provavelmente ouve silêncio — e quando eles chegam, também. Uma pessoa cega não sabe se a página travou, se está carregando ou se não há nada. Conserte isso no seu projeto autoral.

**Critérios de pronto**

- A região de status tem `role="status"` e `aria-live="polite"`, existe no HTML desde o carregamento inicial (não é criada por JavaScript) e anuncia as quatro situações: carregando, quantidade de itens carregados, erro e resultado vazio.
- O contêiner da lista alterna `aria-busy` entre `"true"` e `"false"` nos momentos corretos, inclusive no caminho de erro.
- Os retângulos de esqueleto não são anunciados pelo leitor de tela (eles são decoração, não conteúdo).
- O botão "Tentar de novo" recebe o foco quando aparece, para que quem navega por teclado não precise procurar por ele.
- Um roteiro de teste de 6 passos no `README.md` descreve o que foi ouvido em cada etapa, com o nome do leitor de tela usado.

<details markdown="1">
<summary>Pistas</summary>

1. Um elemento decorativo se esconde do leitor de tela com `aria-hidden="true"`.
2. `elemento.focus()` move o foco; para que faça sentido, o elemento precisa estar visível — mude o `hidden` antes de chamar o foco.
3. Anunciar "10 itens carregados" é mais útil que "carregado": diga **o que mudou**, não que algo mudou.
4. Se o mesmo texto for atribuído duas vezes seguidas ao elemento com `aria-live`, o leitor não repete o anúncio. Se você precisar reanunciar, limpe o texto antes.
</details>

### ⭐⭐⭐ Trinta pedidos, quatro de cada vez
Tags: async, performance, refatoracao, javascript

`Promise.all` com 30 operações dispara as 30 ao mesmo tempo. Em um navegador real isso esbarra no limite de conexões simultâneas por domínio (historicamente 6 no HTTP/1.1) e, em um servidor de verdade, é um jeito rápido de derrubar a própria API. Empresas resolvem isso com uma **fila com limite de concorrência**: no máximo N tarefas rodando, e assim que uma termina, a próxima entra. Implemente a sua.

**Critérios de pronto**

- Uma função `executarComLimite(tarefas, limite)` recebe um array de funções que devolvem Promise e um número máximo de execuções simultâneas, e devolve uma Promise que resolve com o array de resultados **na ordem original das tarefas**, não na ordem de conclusão.
- Uma falha isolada não derruba o lote: o resultado de cada posição é `{ status, valor }` ou `{ status, erro }`, no espírito do `Promise.allSettled`.
- Um teste no console cria 30 tarefas com atrasos aleatórios entre 100 ms e 900 ms, roda com `limite = 4`, e imprime uma linha por tarefa registrando quando começou e quando terminou.
- Um contador global prova que **nunca** houve mais de 4 tarefas rodando ao mesmo tempo: o pico registrado é exatamente 4.
- O `README.md` compara o tempo total com `limite = 1`, `limite = 4` e `limite = 30`, e explica em três linhas por que o ganho para de crescer a partir de certo ponto.

<details markdown="1">
<summary>Pistas</summary>

1. O array de entrada precisa ser de **funções** (`() => buscarProduto(3)`), não de Promises já criadas — uma Promise criada já começou a rodar, e aí não há o que limitar.
2. Um padrão que funciona: mantenha um índice compartilhado e crie exatamente `limite` "trabalhadores", cada um um laço `while` `async` que pega o próximo índice disponível, executa e guarda o resultado na posição certa do array de saída. `Promise.all` dos trabalhadores resolve quando todos esvaziarem a fila.
3. Para o contador de pico: incremente antes do `await` da tarefa, decremente no `finally`, e guarde o máximo já visto.
4. Cuidado com o índice: `const meuIndice = proximo++` dentro do trabalhador garante que dois trabalhadores nunca peguem a mesma tarefa, porque o incremento é síncrono.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| Console mostra `Promise { <pending> }` | Faltou `await` (ou `.then`) antes da chamada | Acrescentar `await` e garantir que a função envolvente seja `async` |
| `SyntaxError: await is only valid in async functions and the top level bodies of modules` | `await` usado em função comum | Marcar a função com `async` ou mover o código para dentro de uma `async` |
| `Uncaught (in promise) Error: Falha simulada de rede ao buscar os produtos` | Promise rejeitada sem `catch` em nenhum ponto da cadeia | Envolver o `await` em `try/catch` ou acrescentar `.catch()` no fim da cadeia |
| `TypeError: Cannot read properties of undefined (reading 'nome')` | O objeto ainda não chegou (faltou `await`) ou a busca não encontrou nada | Conferir o `await` e testar o resultado antes de acessar propriedades |
| A tela fica presa em "Carregando…" para sempre | O caminho de erro não esconde a mensagem; falta `finally` ou `catch` | Mover a limpeza do status para `finally`, que roda nos dois desfechos |
| `Uncaught ReferenceError: buscarProdutos is not defined` | `js/app.js` foi carregado antes de `js/dados.js` | Corrigir a ordem das tags `<script defer>` no HTML |
| `Uncaught TypeError: produtos.map is not a function` | A variável guarda a Promise, não o array (faltou `await` ou `resolve` sem valor) | Conferir o que o `resolve()` recebe e o `await` na chamada |
| `Promise.all` falha inteiro por causa de uma operação só | `Promise.all` rejeita na primeira falha, por definição | Trocar por `Promise.allSettled` quando falhas parciais forem aceitáveis |
| A página congela por segundos ao clicar em um botão | Trabalho síncrono pesado (laço grande) na thread principal | Fatiar o processamento em tarefas ou movê-lo para fora do caminho do clique |
| Leitor de tela não anuncia o carregamento | Elemento com `aria-live` criado junto com a mensagem | Deixar o elemento vazio no HTML e alterar apenas o `textContent` |

## 🏠 Para praticar depois da aula (1 h)

No **seu projeto autoral** (não no Café Cerrado), aplique tudo o que fizemos hoje:

1. Crie `js/dados.js` com uma fonte simulada do seu domínio: `buscarItens()` e `buscarCategorias()`, ambas devolvendo Promises com atraso entre 1 e 2 segundos via `setTimeout`.
2. Faça as duas falharem aleatoriamente em cerca de 30% das chamadas, rejeitando com um objeto `Error` cuja mensagem diga **o que** falhou.
3. Refatore a inicialização da sua lista para uma função `async` com o padrão completo: mensagem de carregando (com `role="status"` e `aria-live="polite"`), `try/catch/finally`, mensagem de erro amigável e botão "Tentar de novo".
4. Carregue as duas fontes em paralelo com `Promise.all` e registre no console o tempo total com `performance.now()`.
5. Garanta os quatro estados visuais: carregando, sucesso, erro e **vazio** (busca sem resultados). Cada um com um texto diferente.
6. Recarregue a página dez vezes e confirme que a interface se comporta bem nos dois cenários — nenhuma tela branca, nenhum `Uncaught (in promise)` no console.

**Critério de pronto:** a lista do seu projeto autoral nunca aparece instantaneamente; ela sempre passa por "Carregando…", e uma falha simulada produz mensagem visível na tela com caminho de recuperação. O console fica limpo de erros não tratados.

**Guarde no seu repositório:** commit + push.

**Leitura dirigida (Biblioteca Virtual da UNEMAT):** QUEIRÓS & PORTELA, capítulo de JavaScript assíncrono; MDN, *Usando Promises* e a página da *Fetch API* — o `fetch` é o protagonista da próxima aula.

## ✅ Checkpoint do projeto

- [ ] `js/dados.js` existe, é carregado antes de `js/app.js` com `defer`, e não contém nenhuma referência ao DOM.
- [ ] `buscarProdutos()` e `buscarCategorias()` devolvem Promises e rejeitam com objetos `Error`.
- [ ] O carregamento inicial usa `Promise.all` e uma função `async` com `try/catch`.
- [ ] Os quatro estados (carregando, sucesso, erro, vazio) têm tratamento visual distinto na tela.
- [ ] A região de status tem `role="status"` e `aria-live="polite"` e existe no HTML desde o início.
- [ ] O botão "Tentar de novo" aparece só no estado de erro e recarrega os dados sem recarregar a página.
- [ ] O esqueleto de carregamento respeita `prefers-reduced-motion`.
- [ ] O console fica sem nenhum `Uncaught (in promise)` em dez recargas seguidas.
- [ ] Tudo commitado e enviado para o GitHub, com o GitHub Pages ainda funcionando.

## 📚 Para aprofundar

- [MDN — Usando Promises](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Guide/Using_promises) — o guia oficial; leia especialmente a parte sobre encadeamento e composição.
- [MDN — `Promise`](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Global_Objects/Promise) — referência dos métodos estáticos: `all`, `allSettled`, `race`, `any`.
- [MDN — `async function`](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Statements/async_function) e [MDN — `await`](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Operators/await) — as duas páginas curtas que valem reler antes da prova.
- [MDN — Guia de microtarefas](https://developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_API/Microtask_guide) — a diferença entre fila de tarefas e fila de microtarefas, com exemplos.
- [Loupe — visualizador do event loop](https://latentflip.com/loupe/) — cole um trecho com `setTimeout` e veja a pilha, a fila e o loop se movendo.
- [MDN — Regiões `aria-live`](https://developer.mozilla.org/pt-BR/docs/Web/Accessibility/ARIA/ARIA_Live_Regions) — quando usar `polite`, `assertive` e `aria-busy`.
- QUEIRÓS, R.; PORTELA, F. *Introdução ao Desenvolvimento Moderno para a Web*. FCA, 2018 — seção de JavaScript assíncrono.
- LOUDON, K. *Desenvolvimento de Grandes Aplicações Web*. Novatec, 2019 — fluxos assíncronos em aplicações grandes.
- PUREWAL, S. *Aprendendo a Desenvolver Aplicações Web*. Novatec, 2014 — capítulo sobre interação com o servidor.

Na próxima aula a simulação sai de cena. O `setTimeout` do `js/dados.js` dá lugar ao **`fetch`**: você vai buscar JSON de um arquivo do próprio projeto e de uma API pública na internet, enviar dados com `POST` e transformar o Café Cerrado em uma **SPA** — uma única página em que a navegação acontece sem recarregar nada. É também a aula que fecha a Unidade 2 e traz o Marco 2.
