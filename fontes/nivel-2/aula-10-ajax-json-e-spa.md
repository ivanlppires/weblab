# Aula 10 — AJAX, JSON e Single Page Application

> **Nível 2 — Desenvolvimento Web** · Unidade 2: Web dinâmica client-side
> WebLab · UNEMAT — Campus Sinop
> **Tempo estimado:** 3 blocos de 50 min + 1 h de prática

Na aula passada você aprendeu a esperar por um valor que ainda não chegou. Só que o valor não chegava de lugar nenhum: era o seu próprio `setTimeout` fingindo ser um servidor. Hoje a simulação acaba. O `fetch` entra em cena, os produtos do Café Cerrado passam a nascer de um arquivo JSON, o formulário de contato ganha destino de verdade e a navegação entre as páginas deixa de recarregar o navegador. No fim da aula você não terá mais um site: terá uma **aplicação**. E esta é a aula que fecha a Unidade 2.

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Explicar o que é AJAX, o que ele mudou na Web e por que o "X" de XML acabou substituído por JSON.
- Escrever e ler JSON válido, converter entre texto e objeto com `JSON.stringify` e `JSON.parse`, e identificar os erros de sintaxe mais comuns.
- Buscar dados com `fetch` + `async/await`, testando `response.ok` e tratando status HTTP e falhas de rede separadamente.
- Enviar dados com `POST`, montando `method`, `headers` e `body` corretamente e lidando com a resposta do servidor.
- Consumir um arquivo JSON do próprio projeto e duas APIs públicas (JSONPlaceholder e ViaCEP), entendendo o que CORS permite e o que ele bloqueia.
- Organizar o código em **módulos ES** (`import` / `export`) e explicar por que módulos exigem servidor HTTP.
- Implementar uma **SPA** com roteamento por hash: várias telas em um único HTML, com histórico do navegador, link direto e foco acessível funcionando.
- Reunir tudo isso no Marco 2 do projeto.

## 📋 Pré-requisitos

- [ ] Repositório `cafe-cerrado` com `js/dados.js` e `js/app.js` da Aula 09 funcionando, incluindo os estados carregando/sucesso/erro/vazio.
- [ ] Bootstrap 5.3 por CDN e `css/estilo.css` como na Unidade 1, com skip link e foco visível (Aula 06).
- [ ] Formulário de contato com validação nativa e mensagens em JavaScript (Aulas 03 e 07).
- [ ] Live Server instalado — hoje o `http://` deixa de ser recomendação e passa a ser **obrigatório**.
- [ ] Internet funcionando na máquina: vamos chamar duas APIs públicas na internet.

> Na aula passada o cardápio passou a chegar "depois": `buscarProdutos()` devolvia uma Promise, o `Promise.all` disparava duas buscas em paralelo e a interface aprendeu a mostrar carregando, sucesso, erro e vazio. Hoje trocamos o `setTimeout` por rede de verdade — e tudo que você escreveu continua valendo, porque o `fetch` também devolve Promises. Depois disso, juntamos as três páginas do site em uma só e implementamos a navegação sem recarga que define uma SPA.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | AJAX e o que ele mudou; JSON a fundo; `fetch` com `async/await`; `response.ok`; status HTTP |
| 2 | 50 min | Módulos ES; `data/produtos.json`; APIs públicas (JSONPlaceholder, ViaCEP); CORS; `POST` no formulário |
| 3 | 50 min | Padrão SPA; roteador por hash; acessibilidade na troca de tela; Mão na massa; laboratório e Marco 2 |

## 1. AJAX: a Web que parou de recarregar

### 1.1 Como era antes

Até o começo dos anos 2000, **toda** interação com um site significava uma volta completa ao servidor: você clicava, o navegador pedia uma página HTML inteira, o servidor a montava e devolvia, e a tela piscava em branco antes de redesenhar tudo. Marcar um e-mail como lido? Página nova. Ir para a página 2 de resultados? Página nova. Corrigir um campo do formulário? Página nova — e adeus aos outros campos que você já tinha preenchido.

Isso limitava o que dava para construir na Web. Aplicações "de verdade" eram programas instalados; o navegador servia para ler documentos.

### 1.2 O que mudou

AJAX é a sigla de **Asynchronous JavaScript And XML**. A ideia: o JavaScript faz requisições HTTP **por conta própria**, em segundo plano, recebe só os dados de que precisa e atualiza apenas o pedaço do DOM que mudou. A página não recarrega.

É o que acontece quando um e-mail novo aparece na sua caixa sem você fazer nada, quando o feed carrega mais posts ao chegar no fim da rolagem, quando a busca sugere resultados a cada tecla, quando o "curtir" muda de cor antes de qualquer navegação. Todos esses são pedaços de tela sendo atualizados com dados que chegaram por AJAX.

A ferramenta original era o objeto `XMLHttpRequest`. Ele funciona até hoje, mas é verboso e baseado em callbacks e eventos:

```js
// Como era com XMLHttpRequest — mostrado só para você reconhecer em código antigo.
const requisicao = new XMLHttpRequest();
requisicao.open("GET", "data/produtos.json");
requisicao.onload = function () {
  if (requisicao.status >= 200 && requisicao.status < 300) {
    const produtos = JSON.parse(requisicao.responseText);
    console.log(produtos.length, "produtos");
  } else {
    console.error("Erro HTTP", requisicao.status);
  }
};
requisicao.onerror = function () {
  console.error("Falha de rede");
};
requisicao.send();
```

O padrão moderno é a **Fetch API**, baseada em Promises — exatamente o que você dominou na Aula 09. É o que usaremos daqui em diante.

> **🧠 Você sabia?**
> A tecnologia veio antes do nome. A Microsoft criou o componente `XMLHTTP` por volta de 1999 para o Outlook Web Access — queriam que o webmail parecesse o Outlook instalado. O Mozilla copiou a ideia como `XMLHttpRequest`, e o Google a levou ao limite no Gmail (2004) e no Google Maps (2005), que arrastava o mapa sem recarregar nada. O nome "AJAX" só apareceu em fevereiro de 2005, num artigo do designer Jesse James Garrett. E a ironia ficou: o "X" era de XML, mas quem venceu como formato de dados foi o **JSON** — a sigla, porém, já estava na boca do mundo e ninguém mais trocou.

## 2. JSON: o idioma dos dados na Web

**JSON** (JavaScript Object Notation) é texto puro com a aparência de um objeto JavaScript. Foi criado por Douglas Crockford no início dos anos 2000 como alternativa enxuta ao XML, e hoje é o formato do tráfego navegador ↔ servidor em praticamente toda API do mundo. Python, Java, PHP, C#, Go: todas as linguagens leem e escrevem JSON.

### 2.1 A sintaxe, sem exceções

```json
{
  "id": 1,
  "nome": "Espresso do Cerrado",
  "preco": 6,
  "disponivel": true,
  "observacao": null,
  "tamanhos": ["pequeno", "médio", "grande"],
  "fornecedor": { "cidade": "Sinop", "uf": "MT" }
}
```

Os tipos permitidos são apenas seis: **string** (sempre com aspas duplas), **número**, **booleano**, **null**, **array** e **objeto**. Nada mais.

### 2.2 JSON não é JavaScript

Parece, mas não é. As diferenças pegam todo mundo pelo menos uma vez:

| Em JavaScript é válido | Em JSON é proibido | Consequência |
|---|---|---|
| `{ nome: "Café" }` | chave sem aspas | erro de parse |
| `{ 'nome': 'Café' }` | aspas simples | erro de parse |
| `{ "a": 1, }` | vírgula sobrando no fim | erro de parse |
| `// comentário` | qualquer comentário | erro de parse |
| `{ "f": function () {} }` | funções | erro de parse |
| `{ "x": undefined }` | `undefined` | erro de parse |

Não existe tipo data em JSON: datas viajam como string (normalmente no formato ISO, `"2030-03-15T19:00:00.000Z"`) e são convertidas para `Date` no destino, se precisar.

### 2.3 As duas conversões

```js
const produto = { id: 1, nome: "Espresso do Cerrado", preco: 6 };

const texto = JSON.stringify(produto);
console.log(texto);
console.log(typeof texto);        // "string" — pronto para ENVIAR pela rede

const objeto = JSON.parse(texto);
console.log(objeto.nome);         // "Espresso do Cerrado"
console.log(typeof objeto);       // "object" — pronto para USAR no código
```

Duas regras para não confundir nunca mais:

- **`stringify` = enviar.** Vai no `body` de um `POST`, ou no `localStorage`.
- **`parse` = receber.** Transforma texto em objeto quando os dados chegam como texto.

O `stringify` aceita um terceiro parâmetro de indentação, muito útil para depurar:

```js
console.log(JSON.stringify(produto, null, 2));
```

### 2.4 O que o `stringify` descarta em silêncio

```js
const bagunca = {
  nome: "Café",
  quando: new Date("2030-03-15T19:00:00Z"),
  calcular: function () { return 1; },
  nada: undefined,
};

console.log(JSON.stringify(bagunca));
```

A saída é `{"nome":"Café","quando":"2030-03-15T19:00:00.000Z"}`. A função e o `undefined` **somem sem aviso**, e a data virou string. Não é bug: é a especificação. Mas é motivo frequente de "meus dados chegaram incompletos no servidor".

> **🔬 Investigue**
> Abra o console e rode `JSON.parse('{ "a": 1, }')`. Leia a mensagem de erro inteira, com atenção ao número da posição. Agora rode `JSON.parse("{ 'a': 1 }")` e depois `JSON.parse('{ a: 1 }')`. Anote as três mensagens: elas são exatamente as que você vai ver quando escrever um `.json` à mão e esquecer uma vírgula ou uma aspa. Saber traduzir "position 10" para "a décima primeira letra do arquivo" economiza muito tempo.

## 3. `fetch`: HTTP com JavaScript

### 3.1 O básico

`fetch(url)` devolve uma Promise. Ela resolve com um objeto `Response` — que representa a **resposta**, não os dados. Extrair os dados é uma segunda operação assíncrona:

```js
async function buscarProdutos() {
  const resposta = await fetch("data/produtos.json");   // 1º await: chegaram os cabeçalhos
  const produtos = await resposta.json();               // 2º await: chegou e foi lido o corpo
  return produtos;
}
```

Por que dois `await`? Porque uma resposta HTTP chega em duas etapas: primeiro a linha de status e os cabeçalhos (o servidor já pode dizer "200 OK, tipo JSON"), depois o corpo, que pode ser grande e demorar. O `fetch` te devolve o controle assim que os cabeçalhos chegam, para que você possa decidir se vale a pena ler o corpo.

O objeto `Response` tem, entre outras, estas propriedades e métodos:

| Membro | O que é | Uso típico |
|---|---|---|
| `resposta.ok` | `true` se o status está entre 200 e 299 | o teste obrigatório |
| `resposta.status` | o número do status (200, 404, 500) | mensagem de erro |
| `resposta.json()` | Promise com o corpo já convertido | APIs JSON |
| `resposta.text()` | Promise com o corpo como texto | HTML, CSV, depuração |

### 3.2 A pegadinha número um do `fetch`

Leia com atenção, porque isso derruba metade da turma:

> **⚠️ Atenção**
> A Promise do `fetch` **só rejeita quando a requisição não acontece**: sem internet, DNS que não resolve, CORS bloqueado, URL malformada. Um `404 Not Found` ou um `500 Internal Server Error` são respostas **bem-sucedidas** do ponto de vista do `fetch` — ele conseguiu falar com o servidor, e o servidor respondeu. A Promise resolve normalmente. Se você não testar `resposta.ok`, seu código vai tentar processar uma página de erro como se fossem dados.

O sintoma clássico dessa falta é uma mensagem que parece não ter nada a ver:

```text
SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON
```

Traduzindo: o servidor devolveu uma página HTML de erro 404, e o `.json()` tentou interpretar `<!DOCTYPE html>` como JSON. A causa real está três linhas acima, no `fetch` sem verificação.

A forma correta:

```js
async function buscarProdutos() {
  const resposta = await fetch("data/produtos.json");

  if (!resposta.ok) {
    throw new Error(`Erro HTTP ${resposta.status} ao buscar os produtos`);
  }

  return resposta.json();
}
```

### 3.3 Os status que você precisa reconhecer

| Faixa | Significado | Exemplos do dia a dia |
|---|---|---|
| 2xx | Deu certo | `200 OK`, `201 Created`, `204 No Content` |
| 3xx | Redirecionamento | `301 Moved Permanently`, `304 Not Modified` |
| 4xx | Erro de quem pediu | `400 Bad Request`, `401`, `403`, `404 Not Found` |
| 5xx | Erro de quem respondeu | `500 Internal Server Error`, `503` |

A distinção 4xx × 5xx é prática: **4xx é culpa sua** (URL errada, dados inválidos, sem permissão) e você conserta no código; **5xx é culpa do servidor** e a única saída do cliente é avisar o usuário e oferecer nova tentativa.

> **🔎 Por baixo do capô**
> Abra a aba **Network** do DevTools, recarregue qualquer página e clique em uma requisição. Em "Headers" você vê exatamente o que foi trocado: o método (`GET`), a URL, os cabeçalhos de requisição (`Accept`, `User-Agent`) e os de resposta (`Content-Type`, `Cache-Control`). É o mesmo protocolo HTTP da Aula 01 (§3), só que agora **você** é quem escreve as requisições. Tudo o que o `fetch` faz aparece ali — inclusive as que falharam.

### 3.4 Uma função reutilizável

Escrever `if (!resposta.ok) throw` em cada chamada é repetitivo e fácil de esquecer. Concentre em um lugar só:

```js
async function pegarJson(url, opcoes = {}) {
  const resposta = await fetch(url, opcoes);

  if (!resposta.ok) {
    throw new Error(`Erro HTTP ${resposta.status} (${resposta.statusText}) em ${url}`);
  }

  return resposta.json();
}
```

Toda chamada do projeto passa por aqui. Se amanhã você precisar acrescentar um cabeçalho de autenticação em todas as requisições — e vai precisar, na Aula 14 —, muda-se uma função só.

### 3.5 Desistindo da espera: `AbortController`

Na Aula 09 você viu que `Promise.race` com um temporizador **para de esperar**, mas não cancela nada. Com `fetch` dá para cancelar de verdade:

```js
async function pegarJsonComPrazo(url, milissegundos = 8000) {
  const controlador = new AbortController();
  const temporizador = setTimeout(() => controlador.abort(), milissegundos);

  try {
    const resposta = await fetch(url, { signal: controlador.signal });
    if (!resposta.ok) {
      throw new Error(`Erro HTTP ${resposta.status} em ${url}`);
    }
    return await resposta.json();
  } catch (erro) {
    if (erro.name === "AbortError") {
      throw new Error(`A resposta demorou mais de ${milissegundos} ms e a requisição foi cancelada`);
    }
    throw erro;
  } finally {
    clearTimeout(temporizador);
  }
}
```

O `signal` é a ponte: quando `abort()` é chamado, o navegador interrompe a conexão e a Promise do `fetch` rejeita com um erro cujo `name` é `"AbortError"`.

## 4. De onde vêm os dados

### 4.1 Um arquivo JSON no próprio projeto

O passo mais natural depois da simulação da Aula 09: tirar o array de dentro do JavaScript e colocá-lo em `data/produtos.json`. Vantagens imediatas: quem edita o cardápio não precisa mexer em código, e o formato é exatamente o que uma API devolveria — quando você construir a sua, na Unidade 3, o front-end nem vai notar a troca.

### 4.2 Por que `file://` para de funcionar

Abra `index.html` com dois cliques, direto do gerenciador de arquivos, e o console mostra:

```text
Access to fetch at 'file:///home/aluno/cafe-cerrado/data/produtos.json' from origin 'null'
has been blocked by CORS policy: Cross origin requests are only supported for
protocol schemes: http, https, ...
```

A **origem** de uma página é a combinação de protocolo + domínio + porta (`http://127.0.0.1:5500`). Páginas abertas como arquivo têm origem `null`, e o navegador recusa requisições a partir dela por segurança — senão qualquer HTML baixado poderia ler os seus arquivos locais.

A solução é servir o projeto por HTTP: **Live Server** no VS Code (`http://127.0.0.1:5500`). Isso vale também para os módulos ES da seção 5.

### 4.3 CORS em uma frase

**CORS** (Cross-Origin Resource Sharing) é a regra que decide se uma página de uma origem pode ler a resposta de outra origem. Quem decide é o **servidor de destino**: se ele mandar o cabeçalho `Access-Control-Allow-Origin`, o navegador libera; se não mandar, o navegador bloqueia a leitura mesmo que a requisição tenha chegado ao destino.

Duas consequências que você vai encontrar hoje:

- JSONPlaceholder e ViaCEP mandam esse cabeçalho de propósito, para permitir uso em qualquer página. Por isso funcionam.
- Muitos sites **não** mandam. Tentar `fetch("https://www.unemat.br")` do seu projeto resulta em bloqueio — e não há nada que você possa fazer do lado do cliente. A solução, quando você tiver um servidor próprio, é pedir do back-end.

> **⚠️ Atenção**
> Erro de CORS **não** é um `404` nem um erro do seu código: é o navegador recusando entregar a resposta ao JavaScript. Na aba Network a requisição costuma aparecer como enviada, e mesmo assim o `fetch` rejeita com `TypeError: Failed to fetch`. Sempre leia o console inteiro: a mensagem de CORS é longa e explica exatamente qual cabeçalho faltou.

### 4.4 Duas APIs públicas para treinar

**JSONPlaceholder** (`https://jsonplaceholder.typicode.com`) é uma API falsa de treino: devolve posts, comentários, usuários e fotos, e aceita `POST`, `PUT` e `DELETE` fingindo que salvou. Nada é gravado de verdade, o que é perfeito para aprender sem estragar nada.

```js
const comentarios = await pegarJson("https://jsonplaceholder.typicode.com/comments?postId=1&_limit=4");
console.log(comentarios[0].name, comentarios[0].body);
```

**ViaCEP** (`https://viacep.com.br`) é um serviço brasileiro real: você passa um CEP e ele devolve o endereço. Vamos usá-lo no formulário de contato.

```js
const endereco = await pegarJson("https://viacep.com.br/ws/78550000/json/");
console.log(endereco.localidade, endereco.uf);
```

Detalhe importante do ViaCEP: quando o CEP não existe, ele responde **200 OK** com `{ "erro": "true" }`. Ou seja, `resposta.ok` é `true` e ainda assim não há endereço. Sempre leia a documentação de cada API — o contrato de erro não é padronizado entre elas.

## 5. Módulos ES: o código deixa de ser um arquivo só

Até a Aula 09, `js/dados.js` e `js/app.js` eram carregados com `defer` e conversavam por variáveis globais. Funciona para dois arquivos; começa a doer no terceiro. Hoje o projeto ganha três arquivos com papéis distintos, e é o momento certo de usar **módulos ES**.

```html
<script type="module" src="js/app.js"></script>
```

O que `type="module"` muda:

- Cada arquivo tem **escopo próprio**: nada vaza para `window`. Para compartilhar algo, você exporta e importa explicitamente.
- A execução é **adiada por padrão** (comporta-se como `defer`), então a posição da tag não importa.
- `import` e `export` passam a funcionar, e a ordem de carregamento é resolvida pelo navegador a partir das dependências.
- O modo estrito (`"use strict"`) é sempre ligado.
- Só funciona por HTTP — mais um motivo para o Live Server.

A sintaxe:

```js
// arquivo js/api.js — exporta
export function pegarJson(url) {
  return fetch(url).then((r) => r.json());
}

export const BASE = "https://jsonplaceholder.typicode.com";
```

```js
// arquivo js/app.js — importa (repare no './' e no '.js' obrigatórios)
import { pegarJson, BASE } from "./api.js";
```

> **💡 Dica**
> Ao contrário do Node.js, o navegador exige o caminho **completo e relativo**: `"./api.js"`, com o ponto inicial e a extensão. Escrever `import { pegarJson } from "api.js"` resulta em erro, porque sem `./` o navegador acha que é o nome de um pacote.

## 6. SPA: Single Page Application

### 6.1 O que muda

Juntando `fetch` + DOM + eventos, chega-se ao padrão que define as aplicações web modernas: carrega-se **um** HTML; a partir daí o JavaScript intercepta a navegação, busca dados por AJAX e troca o conteúdo da tela. A página nunca recarrega.

| Aspecto | Site multipágina (MPA) | SPA |
|---|---|---|
| Navegação | cada clique traz um HTML novo | o JS troca o conteúdo |
| Dados | já embutidos no HTML | buscados por AJAX (JSON) |
| Primeira carga | rápida | mais pesada (todo o JS) |
| Sensação | "site" | "aplicativo" |

Nenhum dos dois é melhor sempre. Um blog ou um portal institucional vive bem como MPA e ainda ganha em SEO e em tempo de primeira carga. Um painel, um webmail, um sistema com muita interação ganha como SPA.

### 6.2 O mecanismo, em poucas linhas

Frameworks como Vue e React automatizam a SPA (você verá isso no Nível 3), mas o núcleo cabe em uma função. Duas peças:

1. **Telas**: seções no HTML, apenas uma visível por vez.
2. **Roteador**: uma função que lê a URL, decide qual tela mostrar e dispara o carregamento de dados daquela tela.

```html
<nav>
  <a href="#/inicio">Início</a>
  <a href="#/cardapio">Cardápio</a>
  <a href="#/contato">Contato</a>
</nav>

<main>
  <section data-rota="/inicio">Conteúdo da tela inicial</section>
  <section data-rota="/cardapio" hidden>Conteúdo do cardápio</section>
  <section data-rota="/contato" hidden>Conteúdo do contato</section>
</main>
```

```js
function navegar() {
  const rota = location.hash.slice(1) || "/inicio";

  document.querySelectorAll("[data-rota]").forEach((tela) => {
    tela.hidden = tela.dataset.rota !== rota;
  });
}

window.addEventListener("hashchange", navegar);   // o usuário navegou
navegar();                                        // primeira carga: respeita a URL atual
```

O `location.hash` de `http://site.com/#/cardapio` é a string `"#/cardapio"`; o `.slice(1)` remove o `#` e sobra `"/cardapio"`.

### 6.3 Por que hash, e não a History API

Existe outra forma de fazer roteamento sem recarga, com `history.pushState()`, que produz URLs limpas (`/cardapio` em vez de `/#/cardapio`). Ela é a usada em produção pelos frameworks — mas exige uma configuração no servidor: qualquer caminho precisa devolver o mesmo `index.html`, senão recarregar a página em `/cardapio` resulta em 404.

O **GitHub Pages**, onde o Café Cerrado está publicado, não permite essa configuração. Por isso usamos o hash: ele funciona em qualquer hospedagem estática, sem servidor nenhum, porque o navegador **nunca** envia a parte depois do `#` na requisição HTTP.

E o hash preserva de graça três coisas que uma SPA malfeita quebra:

- **Voltar e avançar** no navegador funcionam, porque mudar o hash cria uma entrada no histórico.
- **Favoritar e compartilhar** um link direto para uma tela funciona.
- **Recarregar** com <kbd>F5</kbd> mantém você na mesma tela.

### 6.4 O que a SPA quebra na acessibilidade (e como consertar)

Quando o navegador carrega uma página nova, ele faz três coisas automaticamente que uma SPA precisa refazer à mão:

1. **Anuncia o título da página.** Atualize `document.title` a cada troca de tela.
2. **Move o foco para o topo do documento.** Sem isso, quem navega por teclado continua com o foco no link clicado e o leitor de tela não anuncia nada. Solução: dar `tabindex="-1"` ao título da tela e chamar `.focus()` nele.
3. **Sinaliza onde você está.** No menu, marque o link ativo com `aria-current="page"` — o mesmo atributo da Aula 03, agora atualizado por JavaScript.

> **📌 Vale gravar**
> Três perguntas recorrentes: (1) por que `fetch` não rejeita em um 404; (2) qual a diferença entre `JSON.parse` e `response.json()` — o segundo lê o corpo **e** faz o parse, devolvendo uma Promise; (3) por que a navegação por hash preserva o histórico do navegador enquanto trocar classes CSS "na mão" não preserva.

## 💻 Mão na massa — o Café Cerrado vira uma SPA

Vamos transformar o site em uma aplicação de página única, com dados vindos de arquivo JSON e de APIs reais. O repositório termina a aula com esta estrutura:

```text
cafe-cerrado/
├── index.html
├── css/
│   └── estilo.css
├── data/
│   ├── categorias.json
│   └── produtos.json
├── img/
└── js/
    ├── api.js
    ├── app.js
    └── roteador.js
```

Os arquivos `cardapio.html`, `contato.html` e `js/dados.js` deixam de existir: o conteúdo deles migra para o `index.html` e para o `data/`. Apague-os ao final — o histórico do Git guarda tudo, nada se perde.

### Passo 1 — Os dados saem do código

Crie a pasta `data/` e, dentro dela, `produtos.json`:

```json
[
  {
    "id": 1,
    "nome": "Espresso do Cerrado",
    "categoria": "cafes",
    "preco": 6,
    "descricao": "Grãos de Alto Paraíso, torra média, corpo encorpado e final achocolatado.",
    "imagem": "img/espresso.jpg"
  },
  {
    "id": 2,
    "nome": "Coado da Casa",
    "categoria": "cafes",
    "preco": 8.5,
    "descricao": "Duzentos mililitros em coador de papel, moagem média feita na hora do pedido.",
    "imagem": "img/coado.jpg"
  },
  {
    "id": 3,
    "nome": "Cappuccino Sinop",
    "categoria": "cafes",
    "preco": 12,
    "descricao": "Espresso duplo, leite vaporizado e canela do Cerrado por cima.",
    "imagem": "img/cappuccino.jpg"
  },
  {
    "id": 4,
    "nome": "Latte de Baunilha",
    "categoria": "cafes",
    "preco": 14,
    "descricao": "Espresso, leite vaporizado e calda de baunilha feita na casa.",
    "imagem": "img/latte.jpg"
  },
  {
    "id": 5,
    "nome": "Cold Brew da Chapada",
    "categoria": "geladas",
    "preco": 15,
    "descricao": "Extração a frio por dezoito horas, servida com gelo e rodela de laranja.",
    "imagem": "img/cold-brew.jpg"
  },
  {
    "id": 6,
    "nome": "Frappê de Café",
    "categoria": "geladas",
    "preco": 16,
    "descricao": "Espresso batido com gelo, leite e chantili. Também sai sem lactose.",
    "imagem": "img/frappe.jpg"
  },
  {
    "id": 7,
    "nome": "Pão de Queijo Mineiro",
    "categoria": "salgados",
    "preco": 7,
    "descricao": "Porção com quatro unidades de polvilho azedo com queijo canastra.",
    "imagem": "img/pao-de-queijo.jpg"
  },
  {
    "id": 8,
    "nome": "Torta de Frango",
    "categoria": "salgados",
    "preco": 13,
    "descricao": "Fatia generosa com massa amanteigada e recheio de frango desfiado.",
    "imagem": "img/torta-de-frango.jpg"
  },
  {
    "id": 9,
    "nome": "Bolo de Milho Verde",
    "categoria": "doces",
    "preco": 9.5,
    "descricao": "Fatia de bolo cremoso feito com milho da feira do produtor.",
    "imagem": "img/bolo-de-milho.jpg"
  },
  {
    "id": 10,
    "nome": "Brownie de Castanha",
    "categoria": "doces",
    "preco": 11,
    "descricao": "Chocolate meio amargo com castanha-do-pará. Sem glúten.",
    "imagem": "img/brownie.jpg"
  }
]
```

E `data/categorias.json`:

```json
[
  { "id": "cafes", "nome": "Cafés" },
  { "id": "geladas", "nome": "Bebidas geladas" },
  { "id": "salgados", "nome": "Salgados" },
  { "id": "doces", "nome": "Doces" }
]
```

Salve e abra `http://127.0.0.1:5500/data/produtos.json` no navegador. Se aparecer o JSON formatado, o caminho está certo; se aparecer 404, confira o nome da pasta antes de seguir.

### Passo 2 — `js/api.js`: todo acesso a dados em um lugar

```js
// cafe-cerrado/js/api.js
// Camada de acesso a dados do Café Cerrado.
// Nenhuma outra parte do projeto chama fetch diretamente.

const BASE_TESTE = "https://jsonplaceholder.typicode.com";
const BASE_CEP = "https://viacep.com.br/ws";

/**
 * Faz a requisição, verifica o status e devolve o corpo já convertido de JSON.
 * Toda chamada do projeto passa por aqui.
 */
export async function pegarJson(url, opcoes = {}) {
  const resposta = await fetch(url, opcoes);

  if (!resposta.ok) {
    throw new Error(`Erro HTTP ${resposta.status} (${resposta.statusText}) em ${url}`);
  }

  return resposta.json();
}

export function buscarProdutos() {
  return pegarJson("data/produtos.json");
}

export function buscarCategorias() {
  return pegarJson("data/categorias.json");
}

/** Depoimentos de clientes — por enquanto, comentários falsos da JSONPlaceholder. */
export function buscarDepoimentos() {
  return pegarJson(`${BASE_TESTE}/comments?postId=1&_limit=4`);
}

/** Envia a mensagem do formulário de contato. A JSONPlaceholder responde 201 com um id. */
export function enviarMensagem(mensagem) {
  return pegarJson(`${BASE_TESTE}/posts`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(mensagem),
  });
}

/** Consulta o endereço de um CEP brasileiro no ViaCEP. */
export async function buscarEnderecoPorCep(cep) {
  const digitos = cep.replace(/\D/g, "");

  if (digitos.length !== 8) {
    throw new Error("O CEP precisa ter 8 dígitos.");
  }

  const endereco = await pegarJson(`${BASE_CEP}/${digitos}/json/`);

  // O ViaCEP responde 200 OK com { "erro": "true" } quando o CEP não existe.
  if (endereco.erro) {
    throw new Error("CEP não encontrado.");
  }

  return endereco;
}
```

### Passo 3 — `index.html`: uma página, três telas

O `<head>` continua exatamente como na Aula 06 (Bootstrap 5.3 por CDN com `integrity`, `css/estilo.css`, `meta viewport`). O que muda é o menu, o `<main>` e a linha do `<script>`.

O menu passa a apontar para rotas com `#`:

```html
<!-- cafe-cerrado/index.html — navegação -->
<a class="pular-para-conteudo" href="#conteudo">Pular para o conteúdo</a>

<header>
  <nav class="navbar navbar-expand-md navbar-light" aria-label="Navegação principal">
    <div class="container">
      <a class="navbar-brand" href="#/inicio">Café Cerrado</a>
      <ul class="navbar-nav flex-row gap-3">
        <li class="nav-item"><a class="nav-link" href="#/inicio" data-link="/inicio">Início</a></li>
        <li class="nav-item"><a class="nav-link" href="#/cardapio" data-link="/cardapio">Cardápio</a></li>
        <li class="nav-item"><a class="nav-link" href="#/contato" data-link="/contato">Contato</a></li>
      </ul>
    </div>
  </nav>
</header>
```

O `<main>` guarda as três telas. Só uma fica visível por vez — o roteador cuida disso com o atributo `hidden`:

```html
<!-- cafe-cerrado/index.html — as três telas -->
<main id="conteudo" class="container my-4">

  <section class="tela" data-rota="/inicio">
    <h2 tabindex="-1">Café Cerrado</h2>
    <p>Cafeteria de Sinop/MT. Grãos do cerrado, torra da semana, sem pressa.</p>

    <h3>O que dizem nossos clientes</h3>
    <p id="status-depoimentos" class="status" role="status" aria-live="polite"></p>
    <ul id="depoimentos" class="list-unstyled" aria-busy="false"></ul>
  </section>

  <section class="tela" data-rota="/cardapio" hidden>
    <h2 tabindex="-1">Cardápio</h2>

    <div class="filtros row g-2 align-items-end mb-3">
      <div class="col-12 col-md-5">
        <label class="form-label" for="busca">Buscar</label>
        <input class="form-control" type="search" id="busca" placeholder="café, açaí, pão…">
      </div>
      <div class="col-6 col-md-4">
        <label class="form-label" for="filtro-categoria">Categoria</label>
        <select class="form-select" id="filtro-categoria">
          <option value="">Todas as categorias</option>
        </select>
      </div>
      <div class="col-6 col-md-3">
        <label class="form-label" for="ordenacao">Ordenar por</label>
        <select class="form-select" id="ordenacao">
          <option value="nome">Nome (A–Z)</option>
          <option value="preco-asc">Menor preço</option>
          <option value="preco-desc">Maior preço</option>
        </select>
      </div>
    </div>

    <p id="status-cardapio" class="status" role="status" aria-live="polite"></p>
    <button type="button" id="tentar-de-novo" class="btn btn-outline-dark mb-3" hidden>Tentar de novo</button>

    <div id="cards" class="row g-3" aria-busy="false"></div>
    <p id="resumo" class="resumo"></p>
  </section>

  <section class="tela" data-rota="/contato" hidden>
    <h2 tabindex="-1">Fale com a gente</h2>

    <form id="form-contato" class="row g-3" novalidate>
      <div class="col-12 col-md-6">
        <label class="form-label" for="nome">Nome</label>
        <input class="form-control" type="text" id="nome" name="nome" required minlength="3">
      </div>
      <div class="col-12 col-md-6">
        <label class="form-label" for="email">E-mail</label>
        <input class="form-control" type="email" id="email" name="email" required>
      </div>
      <div class="col-6 col-md-3">
        <label class="form-label" for="cep">CEP</label>
        <input class="form-control" type="text" id="cep" name="cep" inputmode="numeric" maxlength="9">
      </div>
      <div class="col-6 col-md-4">
        <label class="form-label" for="cidade">Cidade/UF</label>
        <input class="form-control" type="text" id="cidade" name="cidade" readonly>
      </div>
      <div class="col-12">
        <label class="form-label" for="mensagem">Mensagem</label>
        <textarea class="form-control" id="mensagem" name="mensagem" rows="4" required minlength="10"></textarea>
      </div>
      <div class="col-12">
        <button class="btn btn-dark" type="submit" id="enviar">Enviar mensagem</button>
      </div>
    </form>

    <p id="status-contato" class="status" role="status" aria-live="polite"></p>
  </section>

</main>
```

E, antes do `</body>`, uma única linha de script — sem `defer`, porque módulos já são adiados:

```html
<!-- cafe-cerrado/index.html — antes do </body> -->
<script type="module" src="js/app.js"></script>
```

### Passo 4 — `js/roteador.js`: o coração da SPA

```js
// cafe-cerrado/js/roteador.js
// Roteador por hash: lê a URL, mostra a tela certa e avisa quem quiser saber.

const ROTA_PADRAO = "/inicio";
const acoes = new Map();

/** Registra o que deve acontecer ao entrar em uma rota (ex.: carregar dados). */
export function registrarRota(caminho, aoEntrar) {
  acoes.set(caminho, aoEntrar);
}

function lerRota() {
  const bruta = location.hash.slice(1);
  return acoes.has(bruta) ? bruta : ROTA_PADRAO;
}

function mostrarTela(rota) {
  document.querySelectorAll("[data-rota]").forEach((tela) => {
    tela.hidden = tela.dataset.rota !== rota;
  });

  document.querySelectorAll("[data-link]").forEach((link) => {
    const ativo = link.dataset.link === rota;
    link.classList.toggle("active", ativo);
    if (ativo) {
      link.setAttribute("aria-current", "page");
    } else {
      link.removeAttribute("aria-current");
    }
  });
}

function ajustarTituloEFoco(rota, moverFoco) {
  const tela = document.querySelector(`[data-rota="${rota}"]`);
  const titulo = tela.querySelector("h2");

  document.title = `${titulo.textContent} — Café Cerrado`;

  if (moverFoco) {
    titulo.focus();
  }
}

async function navegar(moverFoco) {
  const rota = lerRota();

  mostrarTela(rota);
  ajustarTituloEFoco(rota, moverFoco);

  const aoEntrar = acoes.get(rota);
  if (aoEntrar) {
    await aoEntrar();
  }
}

export function iniciarRoteador() {
  window.addEventListener("hashchange", () => {
    navegar(true).catch((erro) => console.error("Falha ao navegar:", erro));
  });

  // Primeira carga: respeita a URL que veio no link, mas não rouba o foco de ninguém.
  navegar(false).catch((erro) => console.error("Falha ao navegar:", erro));
}
```

Repare no `.catch` das duas chamadas de `navegar`. Sem ele, uma falha dentro da função de entrada da rota viraria um `Uncaught (in promise)` silencioso — exatamente o que a Aula 09 ensinou a evitar.

### Passo 5 — `js/app.js`: o aplicativo

```js
// cafe-cerrado/js/app.js
// Café Cerrado — SPA com dados vindos de arquivo JSON e de APIs públicas.

import {
  buscarProdutos,
  buscarCategorias,
  buscarDepoimentos,
  enviarMensagem,
  buscarEnderecoPorCep,
} from "./api.js";

import { registrarRota, iniciarRoteador } from "./roteador.js";

const estado = {
  produtos: [],
  categorias: [],
  termo: "",
  categoria: "",
  ordem: "nome",
  cardapioCarregado: false,
  depoimentosCarregados: false,
};

const elementos = {
  cards: document.querySelector("#cards"),
  statusCardapio: document.querySelector("#status-cardapio"),
  resumo: document.querySelector("#resumo"),
  busca: document.querySelector("#busca"),
  filtroCategoria: document.querySelector("#filtro-categoria"),
  ordenacao: document.querySelector("#ordenacao"),
  tentarDeNovo: document.querySelector("#tentar-de-novo"),
  depoimentos: document.querySelector("#depoimentos"),
  statusDepoimentos: document.querySelector("#status-depoimentos"),
  formulario: document.querySelector("#form-contato"),
  statusContato: document.querySelector("#status-contato"),
  botaoEnviar: document.querySelector("#enviar"),
  cep: document.querySelector("#cep"),
  cidade: document.querySelector("#cidade"),
};

function formatarPreco(valor) {
  return valor.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

function mostrarStatus(elemento, mensagem, modificador) {
  elemento.textContent = mensagem;
  elemento.className = modificador ? `status ${modificador}` : "status";
}

function renderizarEsqueleto(quantidade) {
  elementos.cards.innerHTML = "";
  elementos.cards.setAttribute("aria-busy", "true");

  for (let i = 0; i < quantidade; i += 1) {
    const coluna = document.createElement("div");
    coluna.className = "col-12 col-sm-6 col-lg-4";
    const caixa = document.createElement("div");
    caixa.className = "esqueleto";
    caixa.setAttribute("aria-hidden", "true");
    coluna.appendChild(caixa);
    elementos.cards.appendChild(coluna);
  }
}

function criarCard(produto) {
  const coluna = document.createElement("div");
  coluna.className = "col-12 col-sm-6 col-lg-4";

  const card = document.createElement("article");
  card.className = "card h-100";

  const imagem = document.createElement("img");
  imagem.src = produto.imagem;
  imagem.alt = `Foto de ${produto.nome}`;
  imagem.className = "card-img-top";
  imagem.loading = "lazy";

  const corpo = document.createElement("div");
  corpo.className = "card-body";

  const titulo = document.createElement("h3");
  titulo.className = "card-title h5";
  titulo.textContent = produto.nome;

  const descricao = document.createElement("p");
  descricao.className = "card-text";
  descricao.textContent = produto.descricao;

  const preco = document.createElement("p");
  preco.className = "preco fw-bold";
  preco.textContent = formatarPreco(produto.preco);

  corpo.append(titulo, descricao, preco);
  card.append(imagem, corpo);
  coluna.appendChild(card);
  return coluna;
}

function renderizarCards(lista) {
  elementos.cards.innerHTML = "";
  lista.forEach((produto) => elementos.cards.appendChild(criarCard(produto)));
  elementos.cards.setAttribute("aria-busy", "false");
}

function atualizarResumo(lista) {
  if (lista.length === 0) {
    elementos.resumo.textContent = "";
    return;
  }
  const total = lista.reduce((acumulado, produto) => acumulado + produto.preco, 0);
  elementos.resumo.textContent =
    `${lista.length} item(ns) — soma dos preços: ${formatarPreco(total)}`;
}

function preencherFiltroCategorias(categorias) {
  elementos.filtroCategoria.length = 1;   // mantém só a opção "Todas as categorias"
  categorias.forEach((categoria) => {
    const opcao = document.createElement("option");
    opcao.value = categoria.id;
    opcao.textContent = categoria.nome;
    elementos.filtroCategoria.appendChild(opcao);
  });
}

function ordenar(lista, criterio) {
  const copia = [...lista];
  if (criterio === "preco-asc") {
    return copia.sort((a, b) => a.preco - b.preco);
  }
  if (criterio === "preco-desc") {
    return copia.sort((a, b) => b.preco - a.preco);
  }
  return copia.sort((a, b) => a.nome.localeCompare(b.nome, "pt-BR"));
}

function aplicarFiltros() {
  const termo = estado.termo.trim().toLowerCase();

  const filtrados = estado.produtos
    .filter((produto) => produto.nome.toLowerCase().includes(termo))
    .filter((produto) => estado.categoria === "" || produto.categoria === estado.categoria);

  const lista = ordenar(filtrados, estado.ordem);

  renderizarCards(lista);
  atualizarResumo(lista);

  if (lista.length === 0) {
    mostrarStatus(elementos.statusCardapio, "Nenhum item combina com esses filtros.", "status--vazio");
  } else {
    mostrarStatus(elementos.statusCardapio, "");
  }
}

async function carregarCardapio() {
  if (estado.cardapioCarregado) {
    return;                       // já buscamos uma vez: não repete a requisição
  }

  elementos.tentarDeNovo.hidden = true;
  mostrarStatus(elementos.statusCardapio, "Carregando o cardápio…");
  renderizarEsqueleto(6);

  try {
    const [produtos, categorias] = await Promise.all([buscarProdutos(), buscarCategorias()]);

    estado.produtos = produtos;
    estado.categorias = categorias;
    estado.cardapioCarregado = true;

    preencherFiltroCategorias(categorias);
    aplicarFiltros();
  } catch (erro) {
    console.error(erro);
    elementos.cards.innerHTML = "";
    elementos.cards.setAttribute("aria-busy", "false");
    elementos.resumo.textContent = "";
    mostrarStatus(elementos.statusCardapio, "Não foi possível carregar o cardápio.", "status--erro");
    elementos.tentarDeNovo.hidden = false;
    elementos.tentarDeNovo.focus();
  }
}

async function carregarDepoimentos() {
  if (estado.depoimentosCarregados) {
    return;
  }

  mostrarStatus(elementos.statusDepoimentos, "Carregando depoimentos…");
  elementos.depoimentos.setAttribute("aria-busy", "true");

  try {
    const comentarios = await buscarDepoimentos();

    elementos.depoimentos.innerHTML = "";
    comentarios.forEach((comentario) => {
      const item = document.createElement("li");
      item.className = "depoimento";

      const texto = document.createElement("p");
      texto.textContent = `“${comentario.body}”`;

      const autor = document.createElement("p");
      autor.className = "autor";
      autor.textContent = comentario.name;

      item.append(texto, autor);
      elementos.depoimentos.appendChild(item);
    });

    estado.depoimentosCarregados = true;
    mostrarStatus(elementos.statusDepoimentos, `${comentarios.length} depoimentos carregados.`);
  } catch (erro) {
    console.error(erro);
    mostrarStatus(elementos.statusDepoimentos, "Não foi possível carregar os depoimentos.", "status--erro");
  } finally {
    elementos.depoimentos.setAttribute("aria-busy", "false");
  }
}

async function preencherCidadePeloCep() {
  const valor = elementos.cep.value.trim();

  if (valor === "") {
    elementos.cidade.value = "";
    return;
  }

  try {
    const endereco = await buscarEnderecoPorCep(valor);
    elementos.cidade.value = `${endereco.localidade}/${endereco.uf}`;
    mostrarStatus(elementos.statusContato, "");
  } catch (erro) {
    elementos.cidade.value = "";
    mostrarStatus(elementos.statusContato, erro.message, "status--erro");
  }
}

async function enviarFormulario(evento) {
  evento.preventDefault();

  if (!elementos.formulario.checkValidity()) {
    elementos.formulario.reportValidity();
    mostrarStatus(elementos.statusContato, "Confira os campos destacados.", "status--erro");
    return;
  }

  const dados = new FormData(elementos.formulario);
  const mensagem = {
    title: `Contato de ${dados.get("nome")}`,
    body: dados.get("mensagem"),
    email: dados.get("email"),
    userId: 1,
  };

  elementos.botaoEnviar.disabled = true;
  mostrarStatus(elementos.statusContato, "Enviando…");

  try {
    const criado = await enviarMensagem(mensagem);
    mostrarStatus(elementos.statusContato, `Mensagem enviada! Protocolo ${criado.id}.`);
    elementos.formulario.reset();
    elementos.cidade.value = "";
  } catch (erro) {
    console.error(erro);
    mostrarStatus(elementos.statusContato, "Não foi possível enviar. Tente novamente.", "status--erro");
  } finally {
    elementos.botaoEnviar.disabled = false;
  }
}

function ligarEventos() {
  elementos.busca.addEventListener("input", (evento) => {
    estado.termo = evento.target.value;
    aplicarFiltros();
  });

  elementos.filtroCategoria.addEventListener("change", (evento) => {
    estado.categoria = evento.target.value;
    aplicarFiltros();
  });

  elementos.ordenacao.addEventListener("change", (evento) => {
    estado.ordem = evento.target.value;
    aplicarFiltros();
  });

  elementos.tentarDeNovo.addEventListener("click", () => {
    carregarCardapio().catch((erro) => console.error(erro));
  });

  elementos.cep.addEventListener("change", () => {
    preencherCidadePeloCep().catch((erro) => console.error(erro));
  });

  elementos.formulario.addEventListener("submit", (evento) => {
    enviarFormulario(evento).catch((erro) => console.error(erro));
  });
}

registrarRota("/inicio", carregarDepoimentos);
registrarRota("/cardapio", carregarCardapio);
registrarRota("/contato", async () => {});

ligarEventos();
iniciarRoteador();
```

### Passo 6 — Um retoque no CSS

Acrescente ao final de `css/estilo.css` (o `.status` e o `.esqueleto` já vieram da Aula 09):

```css
/* cafe-cerrado/css/estilo.css — SPA (Aula 10) */
.tela h2:focus {
  outline: 3px solid #0d6efd;
  outline-offset: 4px;
}

.depoimento {
  border-left: 4px solid #7a5c3e;
  padding: 0.25rem 0 0.25rem 1rem;
  margin-bottom: 1rem;
}

.depoimento .autor {
  font-weight: 600;
  margin: 0;
}

[data-link].active {
  font-weight: 700;
  text-decoration: underline;
}
```

### Passo 7 — Como testar

1. Abra `index.html` pelo **Live Server**. A URL deve virar `http://127.0.0.1:5500/index.html` e, logo em seguida, mostrar a tela de início com os depoimentos carregando.
2. Clique em **Cardápio**. A URL vira `http://127.0.0.1:5500/index.html#/cardapio` e a página **não** recarrega — confira que o indicador de carregamento da aba do navegador não pisca.
3. Aperte <kbd>F5</kbd> nessa URL. Você continua no cardápio: o link direto funciona.
4. Clique em **Contato**, depois no botão **voltar** do navegador. Você volta ao cardápio, e o menu marca o link certo.
5. Na aba **Network**, filtre por `Fetch/XHR` e navegue entre as telas. Você deve ver `produtos.json`, `categorias.json` e `comments?postId=1&_limit=4` — cada um **uma única vez**, graças aos sinalizadores `cardapioCarregado` e `depoimentosCarregados`.
6. No formulário, digite o CEP `78550000` e saia do campo. O campo Cidade/UF deve preencher com `Sinop/MT`. Agora digite `00000000`: o status mostra "CEP não encontrado."
7. Preencha nome, e-mail e mensagem e envie. Deve aparecer "Mensagem enviada! Protocolo 101." — a JSONPlaceholder sempre devolve o id 101, porque não grava nada de verdade.
8. Em Network, clique na requisição `posts` e veja a aba **Payload**: lá está o JSON que o seu `JSON.stringify` produziu. Na aba **Response**, o que o servidor devolveu.
9. Renomeie `data/produtos.json` para `data/produtos-x.json` e recarregue no cardápio. Deve aparecer a mensagem de erro e o botão "Tentar de novo" — e no console, `Erro HTTP 404 (Not Found) em data/produtos.json`. Volte o nome depois.

**Resultado esperado:** um único HTML, três telas navegáveis com histórico funcionando, dados vindos de arquivo e de duas APIs reais, formulário enviando por `POST` com feedback, e nenhum erro não tratado no console.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Este arquivo tem três erros de sintaxe JSON. Aponte cada um e escreva a versão corrigida.

```text
{
  nome: 'Espresso do Cerrado',
  "preco": 7.5,
  "tags": ["quente", "coado",],
}
```

**A2.** O servidor respondeu `404 Not Found`. Para cada linha, diga o valor:

```js
const resposta = await fetch("data/produtos-inexistente.json");
console.log(resposta.ok);
console.log(resposta.status);
```

A Promise do `fetch` rejeitou? Justifique em uma linha.

**A3.** Qual a diferença entre `JSON.parse(texto)` e `resposta.json()`? As duas devolvem a mesma coisa? Responda citando o tipo de retorno de cada uma.

**A4.** Complete o objeto de opções para que o `fetch` abaixo envie um novo produto como JSON:

```js
const novo = { nome: "Chá de hibisco", preco: 6.5 };

const resposta = await fetch("https://jsonplaceholder.typicode.com/posts", {
  method: "POST",
});
```

**A5.** A URL do navegador é `http://127.0.0.1:5500/index.html#/contato`. Qual o valor de `location.hash`? E o de `location.hash.slice(1)`? Se o usuário apagar o `#/contato` da barra de endereços e apertar Enter, qual rota o roteador escolhe e por quê?

**A6.** Em `carregarCardapio()` existe a guarda `if (estado.cardapioCarregado) return;`. Descreva o que passa a acontecer na aba Network se alguém apagar essa linha e o usuário alternar cinco vezes entre Início e Cardápio.

### Nível B — Aplicação

**B1.** Acrescente ao `js/api.js` a função `buscarProdutoPorId(id)`, que busca `data/produtos.json` e devolve apenas o produto com aquele id, lançando `Error` com mensagem clara se não existir. Teste no console do navegador com um id válido e um inválido.

Resultado esperado: `buscarProdutoPorId(3)` devolve o objeto do Cappuccino Sinop; `buscarProdutoPorId(99)` cai no `catch` com a mensagem "Produto 99 não encontrado", e o console não mostra `Uncaught (in promise)`.

<details markdown="1">
<summary>Dica</summary>

Reaproveite `buscarProdutos()` em vez de repetir o `fetch`. Depois é só um `find` — e um `throw` quando o resultado for `undefined`.
</details>

**B2.** Adicione uma quarta tela ao Café Cerrado: `#/sobre`, com a história da cafeteria e um mapa em texto do endereço. Registre a rota, acrescente o link no menu e confirme que voltar/avançar continuam funcionando.

Resultado esperado: quatro links no menu, quatro seções com `data-rota`, `document.title` mudando em cada uma e `aria-current="page"` sempre no link correto.

<details markdown="1">
<summary>Dica</summary>

A rota só aparece se você registrá-la: `registrarRota("/sobre", async () => {})`. Sem isso, `lerRota()` não a reconhece e cai na rota padrão.
</details>

**B3.** Troque a fonte dos depoimentos: em vez de `comments`, use `https://jsonplaceholder.typicode.com/users` e monte uma lista de "parceiros" com nome, cidade (`address.city`) e site (`website`) de cada usuário.

Resultado esperado: dez itens na lista, cada um com nome, cidade e site; o site é um link clicável que abre em nova aba com `rel="noopener"`.

<details markdown="1">
<summary>Dica</summary>

Inspecione um objeto de `users` no console antes de escrever o código: `console.log(usuarios[0])`. A cidade está aninhada em `address`, então o acesso é `usuario.address.city`.
</details>

**B4.** Trate a falta de internet. Antes de qualquer `fetch`, verifique `navigator.onLine`; se estiver `false`, mostre "Você está sem conexão" em vez de deixar o `fetch` falhar. Escute também os eventos `online` e `offline` do `window` para atualizar a mensagem sozinho.

Resultado esperado: com o modo avião ligado (ou o *throttling* "Offline" da aba Network), a mensagem aparece imediatamente; ao voltar a conexão, a mensagem some e o cardápio carrega sem recarregar a página.

<details markdown="1">
<summary>Dica</summary>

`navigator.onLine` é confiável para dizer "não há rede nenhuma", mas não garante que a internet funcione — por isso ele complementa o `try/catch`, não o substitui.
</details>

**B5.** Persista os filtros na URL: ao digitar na busca ou trocar a categoria, atualize o hash para `#/cardapio?busca=cafe&categoria=doces`; ao carregar a página com esse hash, aplique os filtros automaticamente.

Resultado esperado: copiar a URL e abrir em outra aba reproduz exatamente a mesma tela filtrada.

<details markdown="1">
<summary>Dica</summary>

Separe o hash em duas partes com `split("?")`: a primeira é a rota, a segunda alimenta `new URLSearchParams(...)`. Para escrever sem criar entrada nova no histórico a cada tecla, use `history.replaceState(null, "", novoHash)`.
</details>

### Nível C — Desafio

**C1.** Implemente a rota de detalhe do produto: `#/produto/3` mostra uma tela com a foto grande, o nome, a descrição, o preço e um botão "Voltar ao cardápio". Cada card do cardápio vira um link para a rota do seu produto. Se o id não existir, a tela mostra "Produto não encontrado" com link para o cardápio — sem quebrar a aplicação.

Resultado esperado: clicar em um card leva ao detalhe sem recarga; o botão voltar do navegador retorna ao cardápio com os filtros como estavam; abrir `#/produto/99` direto na barra de endereços mostra a mensagem de não encontrado; abrir `#/produto/3` direto funciona.

<details markdown="1">
<summary>Dica</summary>

O roteador atual compara a rota inteira com as chaves do `Map`. Para rotas com parâmetro, quebre o caminho: `const [, secao, parametro] = rota.split("/")` transforma `"/produto/3"` em `secao = "produto"` e `parametro = "3"`. Registre a ação pela seção e passe o parâmetro para a função de entrada. Lembre-se de que o parâmetro chega sempre como **string**: compare com `Number(parametro)` ou converta o id antes.
</details>

## 🏆 Desafios

### ⭐ O 404 que o fetch não viu
Tags: fetch, bug, devtools, investigacao

Um colega "simplificou" o `pegarJson` do projeto e agora a tela do cardápio mostra "Carregando…" para sempre quando o arquivo não existe — em vez da mensagem de erro. Pior: o console mostra um `SyntaxError` falando de `<!DOCTYPE`, que não parece ter nada a ver com o problema. Este é o trecho alterado:

```js
// cafe-cerrado/js/api.js — versão com o bug plantado
export async function pegarJson(url, opcoes = {}) {
  const resposta = await fetch(url, opcoes);
  return resposta.json();
}
```

Reproduza o erro renomeando `data/produtos.json`, leia a mensagem inteira, explique a ligação entre o `<!DOCTYPE` e o arquivo que sumiu — e conserte.

**Critérios de pronto**

- Um comentário de três linhas no `api.js` explica por que o `fetch` **não** rejeitou diante de um 404 e de onde veio o `<!DOCTYPE` da mensagem.
- Com o arquivo renomeado, a tela mostra a mensagem de erro amigável e o botão "Tentar de novo" em vez de ficar carregando.
- A mensagem lançada inclui o status numérico e a URL que falhou, para facilitar a depuração.
- Um print da aba Network mostrando a linha vermelha do 404 está no `README.md`, ao lado de uma frase explicando o que a coluna "Status" informa.

<details markdown="1">
<summary>Pistas</summary>

1. Releia a seção 3.2: a Promise do `fetch` só rejeita quando a requisição **não acontece**.
2. Peça `resposta.text()` em vez de `resposta.json()` e imprima o resultado: você vai ver a página de erro do servidor, com `<!DOCTYPE html>` na primeira linha.
3. O `statusText` (`"Not Found"`) deixa a mensagem mais legível do que só o número.
4. Depois de consertar, teste também o caminho feliz — é fácil deixar um `throw` disparando quando não deveria.
</details>

### ⭐⭐ O cardápio que não pergunta duas vezes
Tags: fetch, performance, json, devtools

Cada vez que alguém entra na tela do cardápio, você busca `produtos.json` de novo. Hoje isso é rápido porque o arquivo é seu e pequeno. Amanhã será uma API na internet, e a mesma resposta viajará dezenas de vezes por sessão. Construa um **cache com validade**: a primeira chamada busca na rede, as seguintes respondem da memória — até o dado envelhecer.

**Critérios de pronto**

- Uma função `comCache(chave, buscar, validadeEmSegundos)` guarda o resultado e o instante da busca, e só chama `buscar()` de novo depois que a validade expirar.
- O cardápio e as categorias passam a usá-la com validade de 60 segundos; os depoimentos, de 5 minutos.
- Uma medição no `README.md` compara, com `performance.now()`, o tempo da primeira chamada e o da segunda (dentro da validade), com a diferença em milissegundos.
- Um teste documentado prova que, passada a validade, a requisição volta a aparecer na aba Network.
- O cache sobrevive a um <kbd>F5</kbd> — e o README explica em duas linhas qual armazenamento você escolheu para isso e por quê.

<details markdown="1">
<summary>Pistas</summary>

1. Um `Map` na memória basta para a primeira versão: a chave é a URL, o valor é `{ dados, salvoEm }`.
2. Validade expirada é `Date.now() - salvoEm > validadeEmSegundos * 1000`.
3. Para sobreviver ao F5, `sessionStorage` guarda strings — o que significa `JSON.stringify` ao salvar e `JSON.parse` ao ler, exatamente como na seção 2.3.
4. Cuidado com duas chamadas simultâneas antes de a primeira responder: guardar a **Promise** no cache, e não só o resultado, resolve isso de graça.
</details>

### ⭐⭐⭐ Um roteador de verdade
Tags: spa, rotas, javascript, refatoracao

O roteador da aula é um `Map` de caminhos fixos. Frameworks reais aceitam parâmetros (`/produto/:id`), rota coringa para 404, e proteção de rota (entrar em `/admin` só se estiver logado). Escreva o seu, genérico o suficiente para ser copiado para qualquer projeto — e prove que ele funciona.

**Critérios de pronto**

- `registrarRota("/produto/:id", aoEntrar)` funciona: o `aoEntrar` recebe um objeto de parâmetros (`{ id: "3" }`) extraído da URL.
- Existe uma rota coringa `"*"` que responde por qualquer caminho não registrado, exibindo uma tela 404 própria — e a URL **não** é alterada, para o usuário poder corrigi-la.
- Um `antesDeEntrar(rota, parametros)` opcional pode bloquear a navegação devolvendo `false` ou redirecionar devolvendo outra rota; demonstre com uma tela fictícia de administração.
- O roteador continua atualizando `document.title`, `aria-current` e o foco no título — e nada disso vive dentro do `app.js`.
- Um arquivo `docs/roteador.md` documenta a API pública em uma tabela e traz um exemplo mínimo de uso em 15 linhas.

<details markdown="1">
<summary>Pistas</summary>

1. Guarde cada rota registrada como um padrão em partes: `"/produto/:id".split("/")` dá `["", "produto", ":id"]`. Comparar parte a parte com a URL atual, tratando as que começam com `:` como curinga, resolve a extração de parâmetros.
2. Ordem importa: teste as rotas exatas antes das paramétricas, e a coringa por último.
3. Para o `antesDeEntrar` assíncrono, `await` o resultado antes de decidir; retornar uma string significa redirecionar (`location.hash = novaRota`).
4. Cuidado com o laço infinito: se `antesDeEntrar` redirecionar para uma rota que também é bloqueada, a navegação nunca termina. Um contador de redirecionamentos por navegação evita o problema.
</details>

### 🔥 Boss — Pedido do Café Cerrado, do cardápio à confirmação
Tags: spa, fetch, json, projeto

Este é o Boss da Unidade 2: um fluxo completo de pedido, em quatro telas, usando **tudo** o que você aprendeu desde a Aula 07 — DOM e eventos, `map`/`filter`/`reduce`, assíncrono com estados, `fetch` de arquivo e de API, `POST`, formulário validado e roteamento SPA. É também o melhor treino possível para o Marco 2: quem faz o Boss no projeto autoral já tem o marco praticamente pronto.

O fluxo: a pessoa navega o cardápio, adiciona itens ao carrinho, revisa o pedido, preenche a entrega com busca de CEP e confirma. O pedido é enviado por `POST` e a tela final mostra o número do protocolo.

**Critérios de pronto**

- Quatro rotas funcionando com histórico e link direto: `#/cardapio`, `#/carrinho`, `#/entrega` e `#/confirmacao`.
- O carrinho é um array no estado, com quantidade por item; adicionar o mesmo produto duas vezes soma a quantidade em vez de duplicar a linha.
- O total é calculado com `reduce` e reexibido a cada mudança; o contador de itens aparece no menu, em todas as telas.
- O carrinho sobrevive a um <kbd>F5</kbd> (persistido com `JSON.stringify` / `JSON.parse`), e um botão "Esvaziar carrinho" pede confirmação antes de apagar.
- Entrar em `#/entrega` com o carrinho vazio redireciona para `#/cardapio` com uma mensagem explicando o motivo.
- A tela de entrega valida nome, telefone e endereço, e preenche cidade e rua pelo CEP (ViaCEP), tratando CEP inexistente.
- Confirmar envia o pedido inteiro por `POST` para a JSONPlaceholder, com o botão desabilitado durante o envio, e mostra o protocolo devolvido na tela de confirmação.
- Todas as quatro telas tratam carregando, erro e vazio, com `role="status"`, `aria-live` e foco movido para o título a cada troca de tela.
- O `README.md` traz um roteiro de teste numerado de 10 passos que qualquer pessoa consegue seguir para verificar o fluxo inteiro.

<details markdown="1">
<summary>Pistas</summary>

1. Um único objeto `estado` com `produtos`, `carrinho` e `entrega` é mais fácil de depurar do que três variáveis soltas — e é exatamente a ideia que o Pinia formaliza no Nível 3.
2. Para somar quantidades, procure o item antes de inserir: `const existente = carrinho.find((i) => i.id === produto.id)`.
3. Salve o carrinho a cada alteração em uma função só (`salvarCarrinho()`), chamada no fim de toda operação — assim você nunca esquece de persistir.
4. O redirecionamento com carrinho vazio cabe na função de entrada da rota: se `carrinho.length === 0`, `location.hash = "#/cardapio"` e mostre a mensagem.
5. Para o protocolo, a JSONPlaceholder devolve sempre `id: 101` no `POST`. Guarde-o no estado antes de navegar para a confirmação, senão a tela abre sem dado nenhum.
6. Deixe o `POST` por último. Faça as telas e o carrinho funcionarem primeiro; envio é a parte mais curta do desafio.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `Access to fetch at 'file:///…/data/produtos.json' from origin 'null' has been blocked by CORS policy` | Página aberta com duplo clique, não por HTTP | Abrir pelo Live Server (`http://127.0.0.1:5500`) |
| `Uncaught SyntaxError: Cannot use import statement outside a module` | Faltou `type="module"` na tag `<script>` | Trocar `<script src="js/app.js" defer>` por `<script type="module" src="js/app.js">` |
| `GET http://127.0.0.1:5500/js/api.js net::ERR_ABORTED 404` | `import` sem `./` ou sem a extensão `.js` | Usar sempre o caminho relativo completo: `from "./api.js"` |
| `SyntaxError: Unexpected token '<', "<!DOCTYPE "… is not valid JSON` | `.json()` chamado sobre uma página de erro HTML | Testar `resposta.ok` antes de ler o corpo |
| `SyntaxError: Expected double-quoted property name in JSON at position 42` | Vírgula sobrando ou aspas simples no `.json` | Corrigir a sintaxe; validar o arquivo abrindo-o no navegador |
| `TypeError: Failed to fetch` | Sem internet, URL inválida ou CORS bloqueado pelo servidor de destino | Ler o console inteiro: a mensagem de CORS aparece logo abaixo |
| `Access to fetch at 'https://exemplo.com/api' from origin 'http://127.0.0.1:5500' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present` | O servidor de destino não libera outras origens | Usar uma API que permita CORS; a definitiva é pedir pelo back-end (Unidade 3) |
| A página recarrega inteira ao enviar o formulário | Faltou `evento.preventDefault()` no `submit` | Chamar `preventDefault()` na primeira linha do handler |
| O menu troca a tela, mas voltar no navegador não funciona | A troca foi feita só por classe CSS, sem mexer no hash | Navegar sempre por `href="#/rota"`; deixar o `hashchange` decidir |
| `Uncaught (in promise) TypeError: Cannot read properties of null (reading 'addEventListener')` | O elemento não existe na tela atual (`querySelector` devolveu `null`) | Conferir o `id` no HTML; em SPA, o elemento precisa existir no `index.html` |
| O `POST` chega ao servidor sem corpo | Faltou `JSON.stringify` no `body` ou o cabeçalho `Content-Type` | Enviar `body: JSON.stringify(objeto)` com `headers: { "Content-Type": "application/json" }` |

## 🏠 Para praticar depois da aula (1 h)

No **seu projeto autoral**, feche a Unidade 2:

1. Mova os dados do seu domínio para `data/<recurso>.json` e substitua a fonte simulada da Aula 09 por um `fetch` real, mantendo o padrão carregando/sucesso/erro/vazio.
2. Reorganize o JavaScript em módulos ES: `js/api.js` (todo o acesso a dados), `js/roteador.js` (a navegação) e `js/app.js` (a aplicação), com `<script type="module">`.
3. Implemente a navegação SPA por hash com no mínimo **três telas**, com histórico funcionando, `document.title` atualizado, `aria-current="page"` no menu e foco movido para o título a cada troca.
4. Consuma ao menos **uma API pública** de verdade (JSONPlaceholder, ViaCEP ou outra à sua escolha que permita CORS) em alguma tela.
5. Faça o formulário enviar por `POST` sem recarregar a página, com o botão desabilitado durante o envio e mensagem de sucesso ou de erro.
6. Confira o console: zero erros não tratados, zero `Uncaught (in promise)`.
7. Atualize o `README.md` com o que o projeto faz, como rodar (Live Server) e quais APIs ele consome.

**Critério de pronto:** o projeto autoral roda inteiro a partir de um único `index.html`, os dados vêm de arquivos JSON e de pelo menos uma API, e a navegação entre as telas não recarrega o navegador em momento nenhum.

**Guarde no seu repositório:** commit + push. Esta atividade é também a base do Marco 2 — veja as instruções abaixo.

**Leitura dirigida (Biblioteca Virtual da UNEMAT):** QUEIRÓS & PORTELA, capítulos sobre AJAX, JSON e comunicação com o servidor, e a introdução ao back-end com Node.js — a Unidade 3 começa na próxima aula.

## ✅ Checkpoint do projeto

- [ ] `data/produtos.json` e `data/categorias.json` existem, são JSON válido e abrem direto no navegador.
- [ ] `js/api.js` concentra todo o acesso a dados; nenhum `fetch` solto em outro arquivo.
- [ ] `pegarJson` verifica `resposta.ok` e lança `Error` com status e URL.
- [ ] O `index.html` carrega um único `<script type="module">` e nada mais de JavaScript.
- [ ] As três telas funcionam por hash, com voltar/avançar, link direto e <kbd>F5</kbd>.
- [ ] `document.title`, `aria-current="page"` e o foco no título mudam a cada navegação.
- [ ] A consulta de CEP preenche o campo de cidade e trata CEP inexistente.
- [ ] O formulário envia por `POST` com `Content-Type: application/json`, desabilita o botão durante o envio e mostra o protocolo.
- [ ] Nenhuma requisição repetida sem necessidade na aba Network ao alternar entre telas.
- [ ] `cardapio.html`, `contato.html` e `js/dados.js` removidos, e o site publicado no GitHub Pages continua funcionando.

## 🎓 Marco do projeto — Unidade 2

**Escopo.** A evolução do **seu projeto autoral** (não o Café Cerrado, que é o exemplo construído em sala) para uma aplicação client-side dinâmica: validação de formulários, DOM e eventos, programação assíncrona e SPA com AJAX/JSON. É o resultado das Aulas 07 a 10 sobre a base do Marco 1.

**Requisitos:**

1. **Validação de formulário** com pelo menos quatro campos: validação nativa do HTML (`required`, `type`, `minlength`, `pattern`) somada a mensagens em JavaScript por campo, anunciadas em região com `aria-live`.
2. **DOM e eventos**: uma lista de itens do seu domínio renderizada dinamicamente a partir de dados (nada de cards escritos à mão no HTML), com busca por texto, um filtro e uma ordenação funcionando juntos.
3. **Operações em vetores**: `map`, `filter` e `reduce` usados de verdade — inclusive um resumo calculado (total, média, contagem) que se atualiza a cada filtragem.
4. **Programação assíncrona**: carregamento de dados com `async/await` e tratamento explícito dos quatro estados — carregando, sucesso, erro e vazio — com caminho de recuperação no erro.
5. **AJAX e JSON**: dados vindos de pelo menos um arquivo `.json` do próprio repositório **e** de uma API pública real, sempre com verificação de `resposta.ok`.
6. **Envio por `POST`** de um formulário, com `Content-Type: application/json`, botão desabilitado durante o envio e feedback de sucesso e de falha, sem recarregar a página.
7. **SPA** com no mínimo três telas em um único HTML, roteamento por hash, histórico do navegador funcionando, link direto para cada tela e `aria-current="page"` no menu.
8. **Acessibilidade mantida** da Unidade 1: skip link, foco visível, contraste, `alt` nas imagens, foco movido para o título a cada troca de tela.
9. **Repositório organizado**: `data/`, `js/` em módulos ES, `css/`, `README.md` explicando o projeto, como rodar e quais APIs consome; commits com mensagens descritivas ao longo do desenvolvimento.

**Checklist de qualidade**

- **Validação de formulário** completa: nativa + JS, com mensagens acessíveis por campo.
- **DOM e eventos**: render dinâmico, busca, filtro e ordenação funcionando juntos, não isolados.
- **Programação assíncrona**: os quatro estados (carregando, sucesso, erro, vazio) tratados de verdade, com caminho de recuperação no erro — não só o caminho feliz.
- **AJAX e JSON**: `fetch` de arquivo e de API, sempre checando `resposta.ok`, com `POST` funcionando de ponta a ponta.
- **SPA**: roteamento por hash, histórico do navegador, link direto para cada tela e acessibilidade mantida na troca de tela.
- **Organização do repositório**: `README.md` completo e histórico de commits que mostra o projeto evoluindo, não um único commit final.

Um projeto "pela metade" costuma ter um dos itens acima funcionando só no caminho feliz (sem tratar erro, sem lidar com lista vazia) — teste sempre os casos de borda antes de considerar algo pronto.

**Sobre IA:** use como apoio — explicar um erro, sugerir uma correção pontual, revisar um trecho —, não como atalho para gerar o projeto sem entender o que ele faz. O teste real: se alguém apontar para um `await` ou um `filter` do seu código e perguntar por que está ali, você precisa saber responder.

### Como saber que está pronto

- Abra a aba **Network** do DevTools ao alternar entre telas: nenhuma requisição repetida sem necessidade.
- Force os quatro estados manualmente (desligue a rede, aponte para uma URL inexistente, filtre até a lista ficar vazia) e confirme que cada um tem uma tela própria, não uma tela em branco.
- Navegue pelo histórico do navegador (voltar/avançar) dentro da SPA e confirme que cada tela tem link direto funcional.
- Rode o teste de teclado e confira que o foco muda para o título a cada troca de tela.
- Abra o repositório: `README.md` explica o projeto e como rodar, e o histórico de commits mostra evolução real ao longo das quatro aulas.

## 📚 Para aprofundar

- [MDN — Usando a Fetch API](https://developer.mozilla.org/pt-BR/docs/Web/API/Fetch_API/Using_Fetch) — leia com atenção a parte sobre verificar o sucesso da requisição.
- [MDN — `Response`](https://developer.mozilla.org/pt-BR/docs/Web/API/Response) — todos os métodos de leitura do corpo, além de `.json()`.
- [MDN — Trabalhando com JSON](https://developer.mozilla.org/pt-BR/docs/Learn/JavaScript/Objects/JSON) — tutorial curto com exercícios.
- [MDN — CORS](https://developer.mozilla.org/pt-BR/docs/Web/HTTP/CORS) — a explicação completa do que o navegador bloqueia e por quê.
- [MDN — Módulos JavaScript](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Guide/Modules) — `import`, `export`, exportação padrão e os cuidados com caminhos.
- [MDN — `AbortController`](https://developer.mozilla.org/pt-BR/docs/Web/API/AbortController) — cancelamento de requisições.
- [JSONPlaceholder — documentação](https://jsonplaceholder.typicode.com/) e [ViaCEP — documentação](https://viacep.com.br/) — os contratos das duas APIs usadas hoje.
- [json.org](https://www.json.org/json-pt.html) — a especificação do JSON em português, em uma página com os diagramas de sintaxe.
- QUEIRÓS, R.; PORTELA, F. *Introdução ao Desenvolvimento Moderno para a Web*. FCA, 2018 — AJAX, JSON e comunicação com o servidor.
- LOUDON, K. *Desenvolvimento de Grandes Aplicações Web*. Novatec, 2019 — arquitetura de aplicações ricas no cliente.
- ALVES, W. P. *Projetos de Sistemas Web*. Érica, 2015 — integração entre camadas de uma aplicação web.
- PUREWAL, S. *Aprendendo a Desenvolver Aplicações Web*. Novatec, 2014 — AJAX e consumo de APIs.

Na próxima aula começa a **Unidade 3**, e o JavaScript atravessa a rede: com **Node.js e Express** você deixa de consumir a API dos outros e passa a construir a sua — num repositório novo, o `cafe-cerrado-api`, que a Aula 11 cria no primeiro passo. Aquele `data/produtos.json` que hoje é servido por acaso pelo Live Server vira o banco de dados de um servidor que você mesmo escreveu — e o `fetch` do front-end continuará exatamente igual, apontando para `/api/produtos` em vez de um arquivo.
