# Aula 14 — JavaScript para validação de formulários e consultas dinâmicas

> **Nível 1 — Introdução ao Desenvolvimento Web** · Unidade 3: JavaScript e interatividade
> WebLab · UNEMAT Sinop · Prof. Ivan Luiz Pedroso Pires
> **Carga:** 3 aulas de 50 min (presencial) + 1 h (assíncrona)

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Capturar os valores de um formulário pelas três vias (`querySelector`, `form.elements` e `FormData`) e converter cada tipo de campo corretamente.
- Escolher o momento certo de validar (`input`, `blur`, `submit`) e implementar a estratégia "valide no `blur`, corrija no `input`".
- Usar a **Constraint Validation API** (`validity`, `checkValidity`, `setCustomValidity`, `novalidate`) combinando os atributos do HTML com regras de negócio em JavaScript.
- Escrever funções validadoras puras, incluindo a verificação dos dígitos verificadores do CPF.
- Ler e escrever **expressões regulares** para os formatos brasileiros usuais, reconhecendo o que a regex consegue e o que ela **não** consegue validar.
- Exibir mensagens de erro específicas e acessíveis com `role="alert"`, `aria-invalid`, `aria-describedby` e `aria-live`, levando o foco ao primeiro campo inválido.
- Implementar busca, filtro e ordenação em tempo real sobre uma listagem, com normalização de acentos, `debounce` e tratamento do estado vazio.

## 📋 Pré-requisitos

- [ ] O site do evento acadêmico com as cinco páginas responsivas, `js/app.js` carregado com `defer` em todas elas e o menu hambúrguer funcionando (Aula 13).
- [ ] `js/dados.js` com os arrays `palestras` e `palestrantes` criados na Aula 12.
- [ ] Domínio de funções, `querySelector`, `classList`, `dataset`, `createElement`, `addEventListener`, `preventDefault` e delegação de eventos (Aula 13).
- [ ] Domínio de `filter`, `map`, `find`, `forEach` e `sort` sobre arrays de objetos (Aula 12).
- [ ] O formulário de `inscricao.html` com `<label>`, `<fieldset>`, `<select>` e validação nativa (Aulas 03 e 04).
- [ ] DevTools aberto na aba **Console** e o Live Server rodando.

> Na aula passada o JavaScript saiu do console e entrou na página: você escreveu funções, manipulou o DOM, registrou ouvintes e renderizou os palestrantes a partir de um array, com filtro por delegação. Hoje o mesmo conjunto de ferramentas resolve os dois problemas que todo site real tem: **impedir que dados errados entrem** e **deixar o usuário encontrar o que procura**. O formulário de inscrição ganha validação campo a campo com mensagens acessíveis, e a programação passa a ter busca, filtro e ordenação em tempo real.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Captura dos dados, momento de validar, Constraint Validation API e funções validadoras puras |
| 2 | 50 min | Expressões regulares do zero, padrões brasileiros, máscaras e mensagens acessíveis |
| 3 | 50 min | `localStorage`, consultas dinâmicas (busca, filtro, ordenação) e Mão na massa no site do evento |

## 1. Capturando os dados do formulário

### 1.1 O ponto de partida: `submit` e `preventDefault`

Todo processamento de formulário em JavaScript começa no mesmo lugar: o evento `submit` do `<form>` — nunca o `click` do botão. O motivo você já viu na Aula 13: <kbd>Enter</kbd> em qualquer campo de texto envia o formulário sem passar pelo botão, e um ouvinte de `click` simplesmente não é acionado.

**`inscricao.html` — estrutura mínima de um campo**

```html
<form id="form-inscricao" novalidate>
  <div class="campo">
    <label for="nome">Nome completo *</label>
    <input type="text" id="nome" name="nome" autocomplete="name" required>
    <span class="erro" id="erro-nome" role="alert"></span>
  </div>

  <button type="submit">Enviar inscrição</button>
</form>
```

**`js/inscricao.js` — o ouvinte**

```js
const form = document.querySelector("#form-inscricao");

form.addEventListener("submit", (evento) => {
  evento.preventDefault(); // SEMPRE: sem isso a página recarrega e tudo some
  console.log("Formulário enviado sem recarregar a página");
});
```

O atributo `novalidate` no `<form>` **desliga a validação nativa do navegador**. Fazemos isso quando queremos controlar totalmente as mensagens: as caixas amarelas do Chrome não são personalizáveis, mudam de texto entre navegadores, somem sozinhas depois de alguns segundos e não são lidas de forma confiável por leitores de tela. Mesmo desligando a exibição, **mantemos** os atributos `required`, `type`, `minlength` e `pattern` no HTML: eles continuam alimentando a Constraint Validation API (seção 3) e documentam as regras para quem lê o HTML.

> **⚠️ Atenção**
> `novalidate` desliga a **exibição** das mensagens nativas, não a validação. `campo.validity.valueMissing` continua funcionando. É por isso que a combinação "atributos no HTML + mensagens em JavaScript" é a arquitetura recomendada: você não reescreve regras que o navegador já sabe aplicar.

### 1.2 Três formas de ler os valores

```js
const form = document.querySelector("#form-inscricao");

// 1. Elemento por elemento — explícito, bom quando você precisa do elemento em si
const nome = document.querySelector("#nome").value.trim();

// 2. Pela coleção elements do formulário — usa o atributo name
const email = form.elements.email.value.trim();

// 3. FormData — a forma mais prática quando você quer o objeto inteiro
const dados = Object.fromEntries(new FormData(form).entries());
console.log(dados); // { nome: "Ana Souza", email: "ana@exemplo.br", cpf: "123.456.789-09" }
```

`new FormData(form)` monta um objeto iterável com todos os campos que têm `name` e não estão desabilitados. `Object.fromEntries` transforma esses pares chave/valor em um objeto JavaScript comum. Duas limitações que valem a pena guardar: `FormData` ignora campos sem `name`, e um grupo de checkboxes com o mesmo `name` fica só com o último valor — para esse caso, use `dados.getAll("atividades")`.

| Forma | Vantagem | Quando usar |
|---|---|---|
| `querySelector("#id").value` | Devolve o elemento, não só o valor | Quando você vai mexer em classes e atributos do campo |
| `form.elements.nome.value` | Não depende de `id`, só de `name` | Validação genérica, percorrendo campos |
| `new FormData(form)` | Pega tudo de uma vez, pronto para enviar | Montar o objeto final depois de validado |

### 1.3 Cada tipo de campo devolve uma coisa diferente

```js
// Texto: SEMPRE aplique trim() — "   " não é um nome preenchido
const nome = document.querySelector("#nome").value.trim();

// Número: value é SEMPRE string, mesmo em type="number"
const idade = Number(document.querySelector("#idade").value);

// Checkbox único: booleano
const aceitouTermos = document.querySelector("#termos").checked;

// Radio: pegue o que está marcado (pode não haver nenhum)
const vinculo = form.querySelector("input[name='vinculo']:checked")?.value ?? "";

// Grupo de checkboxes: transforme a NodeList em array e extraia os valores
const atividades = [...form.querySelectorAll("input[name='atividades']:checked")]
  .map((caixa) => caixa.value);

// Select simples e select múltiplo
const curso = document.querySelector("#curso").value;
const cursos = [...document.querySelector("#cursos").selectedOptions].map((o) => o.value);

// Arquivo: uma lista de File, mesmo sem o atributo multiple
const comprovante = document.querySelector("#comprovante").files[0];
```

> **⚠️ Atenção**
> O erro que aparece em toda turma: `input.value` de um `type="number"` retorna a **string** `"25"`, não o número `25`. Fazer `idade + 1` produz `"251"`. Converta sempre com `Number()` — e lembre-se, da Aula 11, de que `Number("")` é `0`, então teste o campo vazio **antes** de converter.

O `?.` no radio (encadeamento opcional, Aula 11) evita o clássico `Cannot read properties of null (reading 'value')` quando nenhuma opção está marcada; o `??` completa com uma string vazia.

## 2. Quando validar

Validar cedo demais irrita; validar tarde demais frustra. O momento certo depende do evento:

| Momento | Evento | Custo de escolher errado |
|---|---|---|
| Ao digitar | `input` | Acusa "e-mail inválido" na segunda letra digitada |
| Ao sair do campo | `blur` | O usuário só descobre o erro depois de sair |
| Ao enviar | `submit` | Tarde demais como **único** feedback |

A estratégia que dá a melhor experiência combina os três, em quatro regras:

1. **Não valide enquanto o usuário digita pela primeira vez.** Ele ainda está escrevendo.
2. **Valide no `blur`**, quando ele sai do campo — o momento natural de "terminei este aqui".
3. **A partir do instante em que o campo já mostrou erro, passe a validar no `input`.** Assim o usuário vê a mensagem sumir enquanto corrige, em vez de precisar sair do campo de novo.
4. **Valide tudo no `submit`** e leve o foco ao primeiro campo inválido.

```js
const campos = [...form.querySelectorAll("input, select, textarea")];

campos.forEach((campo) => {
  campo.addEventListener("blur", () => {
    validarCampo(campo);
    campo.dataset.tocado = "true"; // marca: este campo já foi visitado
  });

  campo.addEventListener("input", () => {
    if (campo.dataset.tocado === "true") validarCampo(campo);
  });
});
```

O truque está no `dataset.tocado` (Aula 13): o próprio DOM guarda o estado "este campo já foi visitado", sem precisar de um array paralelo em JavaScript. Como `dataset` sempre devolve string, a comparação é com `"true"`, não com `true`.

> **💡 Dica**
> `blur` não borbulha, então `form.addEventListener("blur", …)` não funciona — é por isso que o código acima registra o ouvinte campo a campo. Se você quiser um ouvinte só, use o evento `focusout`, que é a versão borbulhante do `blur`.

## 3. A Constraint Validation API

O navegador já validou o campo antes de você escrever qualquer linha. A Constraint Validation API é a interface que expõe esse resultado — e é ela que faz `required`, `type="email"`, `min`, `max`, `minlength` e `pattern` valerem também para o seu código.

### 3.1 O objeto `validity`

```js
const campo = document.querySelector("#email");

campo.validity.valid;           // true se o campo passa em todas as restrições
campo.validity.valueMissing;    // required não preenchido
campo.validity.typeMismatch;    // type="email" ou type="url" com formato errado
campo.validity.patternMismatch; // não casou com o atributo pattern
campo.validity.tooShort;        // abaixo do minlength (tooLong: acima do maxlength)
campo.validity.rangeUnderflow;  // abaixo do min (rangeOverflow: acima do max)
campo.validity.customError;     // há uma mensagem definida por setCustomValidity
```

### 3.2 Os três métodos

```js
campo.checkValidity();   // true/false, silencioso (não mostra nada na tela)
campo.reportValidity();  // valida E mostra a mensagem nativa do navegador
campo.setCustomValidity("As senhas não coincidem."); // define um erro seu
campo.setCustomValidity("");                          // limpa o erro personalizado
```

`setCustomValidity` merece cuidado: enquanto a mensagem estiver definida, o campo é considerado **inválido para sempre**, mesmo que o usuário corrija o valor. Você precisa limpá-la (`setCustomValidity("")`) no início de cada nova validação. Esquecer isso produz o bug "o formulário nunca envia" mais comum da aula.

### 3.3 Traduzindo `validity` em mensagem útil

Em vez de escrever de novo a regra "e-mail precisa ter arroba", leia o diagnóstico que o navegador já fez e devolva um texto em português decente:

```js
function mensagemNativa(campo) {
  const v = campo.validity;
  const rotulo = campo.labels[0]?.textContent.replace("*", "").trim() || "Este campo";

  if (v.valueMissing) return `${rotulo} é obrigatório.`;
  if (v.typeMismatch) return `${rotulo} está em um formato inválido.`;
  if (v.tooShort) return `${rotulo} deve ter ao menos ${campo.minLength} caracteres.`;
  if (v.tooLong) return `${rotulo} deve ter no máximo ${campo.maxLength} caracteres.`;
  if (v.rangeUnderflow) return `${rotulo} deve ser no mínimo ${campo.min}.`;
  if (v.rangeOverflow) return `${rotulo} deve ser no máximo ${campo.max}.`;
  if (v.patternMismatch) return campo.title || `${rotulo} está em um formato inválido.`;
  return "";
}
```

`campo.labels` é uma coleção com todos os `<label>` associados ao campo — mais uma razão para você ter caprichado no `for`/`id` da Aula 03. O `?.` protege contra campos sem rótulo, e o `campo.title` aproveita o atributo `title` do `pattern` como mensagem, que é exatamente para isso que ele existe.

A arquitetura final combina duas camadas: **os atributos HTML declaram as regras simples e servem de documentação; o JavaScript cuida das regras de negócio** (dígitos do CPF, idade mínima, senhas coincidentes, ao menos um minicurso escolhido) **e da apresentação das mensagens**.

> **🔬 Investigue**
> Abra `inscricao.html` com o Live Server e o Console. Digite `const e = document.querySelector("#email")` e depois `e.validity`. Expanda o objeto: todos os campos aparecem como `false` e `valid: true` porque o campo está vazio e ainda não é `required` para o navegador… ou aparece `valueMissing: true`, se você já colocou `required`. Agora digite `e.value = "ana@"` e chame `e.validity` de novo: `typeMismatch` virou `true`. Por fim, chame `e.reportValidity()` e veja a caixa nativa — a mesma que `novalidate` esconde.

> **🧠 Você sabia?**
> O atributo `pattern` existe desde o HTML5, mas as âncoras `^` e `$` são **implícitas** nele: o navegador sempre exige correspondência total. Escrever `pattern="^\d{5}-?\d{3}$"` funciona por acidente (as âncoras extras não atrapalham), mas escrever `pattern="/\d{5}-?\d{3}/"` **nunca** casa, porque as barras viram caracteres literais a serem procurados. É o erro nº 1 de quem aprendeu regex em JavaScript antes de usar `pattern`.

## 4. Funções validadoras puras

A melhor forma de organizar validação é escrever funções **puras**: recebem um valor, devolvem a mensagem de erro (string) ou `""` quando está tudo certo. Elas não tocam no DOM, não dependem de variáveis globais e por isso podem ser testadas no console, reaproveitadas em outro projeto e lidas sem sustos.

```js
// js/inscricao.js — validadores (funções puras: entram dados, sai mensagem)

function validarObrigatorio(valor, rotulo = "Este campo") {
  return valor.trim() === "" ? `${rotulo} é obrigatório.` : "";
}

function validarTamanho(valor, minimo, maximo, rotulo) {
  const v = valor.trim();
  if (v.length < minimo) return `${rotulo} deve ter ao menos ${minimo} caracteres.`;
  if (v.length > maximo) return `${rotulo} deve ter no máximo ${maximo} caracteres.`;
  return "";
}

function validarNomeCompleto(valor) {
  const partes = valor.trim().split(/\s+/); // divide por qualquer sequência de espaços
  if (partes.length < 2) return "Informe nome e sobrenome.";
  if (partes.some((parte) => parte.length < 2)) {
    return "Cada parte do nome deve ter ao menos 2 letras.";
  }
  return "";
}

function validarEmail(valor) {
  const v = valor.trim();
  if (v === "") return "O e-mail é obrigatório.";
  if (!v.includes("@")) return "O e-mail deve conter @.";
  const [usuario, dominio] = v.split("@");
  if (!usuario || !dominio) return "Formato de e-mail inválido.";
  if (!dominio.includes(".")) return "O domínio do e-mail está incompleto.";
  return "";
}
```

Repare no padrão: cada função devolve **uma** mensagem, a primeira que se aplica. Mensagens boas dizem **o que fazer**. "Campo inválido" não ajuda ninguém; "A senha deve conter ao menos uma letra maiúscula" resolve o problema do usuário em um segundo.

### 4.1 Datas digitadas: duas armadilhas do `Date`

Validar uma data digitada como `31/02/2000` exige mais do que formato. Duas armadilhas do objeto `Date` explicam por quê:

```js
const data = new Date(2000, 1, 31); // meses vão de 0 a 11: 1 é fevereiro
data.getDate();  // 2   ← o Date "conserta" a data sozinho, sem erro nenhum
data.getMonth(); // 2   ← virou março
```

A primeira armadilha é que **os meses vão de 0 a 11**. A segunda é que `Date` nunca reclama de uma data inexistente: ele a desloca. A defesa é sempre a mesma — reconstruir dia, mês e ano a partir do objeto criado e comparar com o que foi digitado. Se não bate, a data não existe no calendário. A função completa, com o cálculo da idade, está na Mão na massa.

### 4.2 CPF: o algoritmo de verdade

O CPF tem 11 dígitos, sendo os dois últimos **dígitos verificadores** calculados a partir dos nove primeiros. Isso significa que um CPF digitado errado é detectável sem consultar nenhum servidor — e é por isso que nenhum site sério aceita `111.111.111-11`.

```js
function validarCPF(cpf) {
  const numeros = cpf.replace(/\D/g, ""); // \D = tudo que NÃO é dígito

  if (numeros.length !== 11) return "O CPF deve ter 11 dígitos.";
  if (/^(\d)\1{10}$/.test(numeros)) return "CPF inválido."; // 000…0, 111…1, 999…9

  const calcularDigito = (base, pesoInicial) => {
    let soma = 0;
    for (let i = 0; i < base.length; i++) {
      soma = soma + Number(base[i]) * (pesoInicial - i);
    }
    const resto = (soma * 10) % 11;
    return resto === 10 ? 0 : resto;
  };

  const primeiro = calcularDigito(numeros.slice(0, 9), 10);
  const segundo = calcularDigito(numeros.slice(0, 10), 11);

  if (primeiro !== Number(numeros[9]) || segundo !== Number(numeros[10])) {
    return "CPF inválido. Confira os números digitados.";
  }
  return "";
}
```

Leia a regex `/^(\d)\1{10}$/` com calma, porque ela usa um recurso que a seção 5 vai formalizar: `(\d)` captura um dígito no grupo 1, e `\1{10}` exige que **o mesmo dígito** apareça mais dez vezes. É a forma mais curta de dizer "todos os onze dígitos são iguais".

> **🧠 Você sabia?**
> O algoritmo do CPF é uma variação do cálculo de **dígito verificador módulo 11**, o mesmo princípio usado no ISBN de livros, no código de barras dos boletos bancários e no número de matrícula de muitas universidades. A ideia é antiga e simples: some os dígitos multiplicados por pesos decrescentes, tire o resto da divisão por 11, e guarde o resultado no fim do número. Um dígito trocado ou dois dígitos invertidos mudam a soma e o erro é detectado na hora — sem internet, sem banco de dados.

## 5. Expressões regulares

### 5.1 O que é e como criar

Uma **expressão regular** (regex) é um padrão que descreve um conjunto de strings. Com ela você responde perguntas como "este texto tem formato de e-mail?", "quais números aparecem aqui?" ou "troque todo espaço duplo por um só". Regex existe em praticamente todas as linguagens e ferramentas — JavaScript, Python, Java, SQL, `grep`, a busca do VS Code — e é um dos poucos conhecimentos que você leva inteiro para qualquer tecnologia da carreira.

```js
// 1. Forma literal — preferida quando o padrão é fixo
const padrao = /abc/;

// 2. Construtor — quando o padrão é montado em tempo de execução
const termoDigitado = "café";
const busca = new RegExp(termoDigitado, "gi");
```

No construtor, a string precisa escapar as barras invertidas em dobro (`"\\d"` em vez de `\d`), porque a barra invertida também é especial dentro de strings. Use a forma literal sempre que puder.

### 5.2 Flags

| Flag | Nome | Efeito |
|---|---|---|
| `g` | global | Encontra todas as ocorrências, não só a primeira |
| `i` | insensitive | Ignora maiúsculas e minúsculas |
| `m` | multiline | `^` e `$` passam a casar em cada linha |
| `s` | dotAll | O ponto passa a casar também com quebra de linha |
| `u` | unicode | Tratamento correto de caracteres fora do ASCII |

```js
/casa/gi.test("Minha CASA e a casa dela"); // true, ignorando a caixa
```

### 5.3 Classes de caracteres

```text
.     qualquer caractere, exceto quebra de linha
\d    dígito  [0-9]              \D    NÃO dígito
\w    palavra [A-Za-z0-9_]       \W    NÃO caractere de palavra
\s    espaço, tabulação, quebra  \S    NÃO espaço em branco

[abc]   a, b OU c                [^abc]  qualquer coisa EXCETO a, b, c
[a-z]   letra minúscula          [A-Z]   letra maiúscula
[0-9]   dígito                   [À-ÿ]   letras acentuadas da faixa Latin-1
```

```js
/[A-Za-zÀ-ÿ]/.test("ção"); // true — letra com ou sem acento
/[^\d]/.test("1234");      // false — só há dígitos
```

### 5.4 Quantificadores

```text
*        0 ou mais
+        1 ou mais
?        0 ou 1 (opcional)
{n}      exatamente n
{n,}     n ou mais
{n,m}    entre n e m
```

```js
/^\d{3}$/.test("123");     // true — exatamente três dígitos
/^\d{2,4}$/.test("12345"); // false — passou de quatro
/colou?r/.test("colour");  // true — o "u" é opcional
```

**Gulosos e preguiçosos.** Por padrão, quantificadores são gulosos: pegam o máximo possível. Acrescentar `?` os torna preguiçosos.

```js
const texto = "<b>negrito</b> e <i>itálico</i>";

texto.match(/<.+>/)[0];  // "<b>negrito</b> e <i>itálico</i>"  ← guloso
texto.match(/<.+?>/)[0]; // "<b>"                              ← preguiçoso
```

### 5.5 Âncoras e limites

```text
^     início da string (ou da linha, com a flag m)
$     fim da string
\b    limite de palavra
\B    NÃO limite de palavra
```

```js
/^abc/.test("abcdef");     // true  — começa com abc
/abc$/.test("xyzabc");     // true  — termina com abc
/^abc$/.test("abc");       // true  — é exatamente abc
/\bgato\b/.test("gatorade"); // false — "gato" precisa ser palavra inteira
```

> **📌 Na prova**
> A âncora é o que separa **busca** de **validação**. `/\d{3}/.test("abc1234xyz")` é `true`: encontrou três dígitos em algum lugar. `/^\d{3}$/.test("abc1234xyz")` é `false`: a string **inteira** precisa ser exatamente três dígitos. Toda regex de validação de formato precisa de `^` no início e `$` no fim. Essa questão cai todo semestre.

### 5.6 Grupos, alternância e lookahead

```js
/(abc)+/;                    // grupo de captura: "abc" repetido
/(?:abc)+/;                  // grupo SEM captura (não guarda o trecho)
/(palestra|minicurso|mesa)/; // alternância: um dos três
```

Grupos nomeados deixam o resultado legível:

```js
const padraoData = /(?<dia>\d{2})\/(?<mes>\d{2})\/(?<ano>\d{4})/;
const resultado = "07/05/1998".match(padraoData);

resultado.groups.dia; // "07"
resultado.groups.mes; // "05"
resultado.groups.ano; // "1998"
```

**Lookahead** (`(?=…)` positivo, `(?!…)` negativo) e **lookbehind** (`(?<=…)` e `(?<!…)`) verificam o que vem depois ou antes sem consumir os caracteres:

```js
// Senha forte: ao menos 1 minúscula, 1 maiúscula, 1 dígito, 1 especial, mínimo 8
const senhaForte = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$/;

/\d+(?=\s*vagas)/.exec("Restam 12 vagas")[0];             // "12"  — seguido de "vagas"
/(?<=R\$\s?)\d+([.,]\d{2})?/.exec("Total: R$ 89,90")[0];  // "89,90" — precedido de R$
```

Cada lookahead da senha forte é uma verificação independente feita a partir do início da string: "olhando para a frente, existe em algum ponto uma minúscula?". Todas precisam ser verdadeiras, e só então `[A-Za-z\d@$!%*?&#]{8,}` consome a string de fato.

### 5.7 Escapando metacaracteres

Estes caracteres têm significado especial e precisam de barra invertida quando você quer o caractere literal:

```text
.  *  +  ?  ^  $  {  }  (  )  |  [  ]  \  /
```

```js
/\./;            // ponto literal
/R\$\s?\d+/;     // "R$ 100"
/\(\d{2}\)/;     // "(66)"
/https?:\/\//;   // "http://" ou "https://"
```

### 5.8 Os métodos que você vai usar

```js
// test — devolve booleano. O mais usado em validação.
/\d/.test("abc123"); // true

// match — sem a flag g, devolve os grupos capturados
"07/05/1998".match(/(\d{2})\/(\d{2})\/(\d{4})/);
// ["07/05/1998", "07", "05", "1998", index: 0, ...]

// match — com a flag g, devolve só as ocorrências
"a1 b2 c3".match(/\d/g); // ["1", "2", "3"]

// matchAll — precisa da flag g; devolve um iterável com os grupos de cada ocorrência
for (const m of "Ana: 8.5, Bruno: 6.0".matchAll(/(?<nome>\w+): (?<nota>[\d.]+)/g)) {
  console.log(m.groups.nome, m.groups.nota);
}

// replace — $1, $2 referenciam os grupos capturados; uma função permite calcular
"  muitos     espaços  ".replace(/\s+/g, " ").trim();          // "muitos espaços"
"07/05/1998".replace(/(\d{2})\/(\d{2})\/(\d{4})/, "$3-$2-$1"); // "1998-05-07"
"restam 100".replace(/\d+/, (n) => Number(n) * 2);             // "restam 200"

// split aceita regex como separador
"nome; idade , curso".split(/\s*[;,]\s*/); // ["nome", "idade", "curso"]
```

### 5.9 Padrões brasileiros de referência

```js
// js/inscricao.js — padrões reutilizáveis
const CPF = /^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$/;
const CEP = /^\d{5}-?\d{3}$/;
const TELEFONE = /^\(?\d{2}\)?\s?9?\d{4}-?\d{4}$/;
const DATA = /^(0[1-9]|[12]\d|3[01])\/(0[1-9]|1[0-2])\/\d{4}$/;
const HORA = /^([01]\d|2[0-3]):[0-5]\d$/;
const NOME = /^[A-Za-zÀ-ÿ]+(\s[A-Za-zÀ-ÿ]+)+$/;
const URL = /^https?:\/\/[\w.-]+\.[a-z]{2,}(\/\S*)?$/i;
const SLUG = /^[a-z0-9]+(-[a-z0-9]+)*$/;
```

O padrão `TELEFONE` merece uma leitura guiada: `\(?\d{2}\)?` aceita o DDD com ou sem parênteses; `\s?` permite um espaço; `9?` torna opcional o nono dígito dos celulares; `\d{4}-?\d{4}` aceita o traço ou a ausência dele. Assim `(66) 99999-9999`, `66999999999` e `(66) 3511-1000` passam, e `9999-9999` (sem DDD) não passa.

### 5.10 O caso do e-mail

```js
// Suficiente para 99,9% dos casos reais
const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
```

Não existe regex simples que valide e-mail perfeitamente. A especificação que define o formato permite construções tão exóticas (comentários entre parênteses, aspas, caracteres acentuados) que a expressão completa passa de seis mil caracteres e é ilegível. A recomendação profissional é usar uma regex simples de formato e **confirmar o endereço por um e-mail de verificação**. Uma regex agressiva demais rejeita endereços válidos — problema pior do que aceitar um endereço inválido, porque o usuário desiste do cadastro sem entender por quê.

> **🧠 Você sabia?**
> As expressões regulares nasceram em 1951, num artigo do matemático **Stephen Kleene** sobre linguagens regulares — décadas antes da web. O `*` que você usa em `\d*` chama-se, até hoje, **estrela de Kleene**. A notação chegou à programação nos anos 1960, com o editor `qed` de Ken Thompson, e de lá foi para o `grep` do Unix (o nome vem de `g/re/p`, "global / regular expression / print"). Ou seja: você está usando uma ideia de setenta anos para conferir um CPF.

### 5.11 O que a regex NÃO faz

Regex verifica **formato**, não **validade**:

| Regex verifica | Regex NÃO verifica |
|---|---|
| O CPF tem 11 dígitos no formato certo | Se os dígitos verificadores conferem |
| A data está em dd/mm/aaaa | Se o dia 31/02 existe no calendário |
| O e-mail tem arroba e domínio | Se a caixa postal existe |
| O cartão tem 16 dígitos | Se passa no algoritmo de Luhn |

Combine sempre regex (formato) com validação algorítmica (regra), como você fez no CPF da seção 4.2.

**ReDoS — travar o navegador com uma regex.** Padrões com quantificador dentro de quantificador podem levar tempo exponencial para concluir que algo **não** casa:

```js
// Perigosa: quantificador aninhado
const perigosa = /^(a+)+$/;
// perigosa.test("aaaaaaaaaaaaaaaaaaaaaaaaaaaaX") pode travar a aba

// Reescrita segura, com o mesmo efeito prático
const segura = /^a+$/;
```

Evite `(x+)+`, `(x*)*` e `(x|x)*`. E, quando um padrão passar de uma linha, decomponha-o em pedaços nomeados e monte com `new RegExp`: você não vai lembrar o que aquela sequência de símbolos faz daqui a duas semanas. Sempre comente uma regex não trivial.

> **🔬 Investigue**
> Abra o console e teste: `/^\d{3}$/.test("123")`, depois `/^\d{3}$/.test(" 123")` — por que o segundo é `false`? Agora rode `"Ana Paula da Silva".split(/\s+/)` e conte os elementos. Por fim, vá a <https://regex101.com>, cole `^\(?\d{2}\)?\s?9?\d{4}-?\d{4}$` no campo da expressão, escolha o sabor **ECMAScript (JavaScript)** e teste com `(66) 99988-7766`, `66999887766` e `9998-7766`. O painel da direita explica **token por token** o que cada símbolo faz — é a melhor forma de aprender regex que existe.

## 6. Máscaras e formatação

Máscara é a formatação que aparece enquanto o usuário digita: `12345678909` vira `123.456.789-09`. Ela reduz erros de digitação e deixa claro qual formato o campo espera.

```js
// js/inscricao.js — máscaras

function mascaraCPF(valor) {
  return valor
    .replace(/\D/g, "")                     // fica só com os dígitos
    .slice(0, 11)                           // no máximo 11
    .replace(/(\d{3})(\d)/, "$1.$2")        // primeiro ponto
    .replace(/(\d{3})(\d)/, "$1.$2")        // segundo ponto
    .replace(/(\d{3})(\d{1,2})$/, "$1-$2"); // traço antes dos verificadores
}

// Aplicação: reescreve o valor do campo a cada tecla
document.querySelector("#cpf").addEventListener("input", (evento) => {
  evento.target.value = mascaraCPF(evento.target.value);
});
```

A receita é sempre a mesma: limpe tudo o que não é dígito, corte no comprimento máximo e insira os separadores com `replace` e grupos capturados. As máscaras de telefone e de data seguem exatamente esse molde e estão completas na Mão na massa.

> **⚠️ Atenção**
> Máscaras atrapalham quem cola um valor já formatado e quem usa leitor de tela (o campo muda sozinho enquanto a pessoa digita). Duas regras compensam isso: **sempre remova a formatação** (`valor.replace(/\D/g, "")`) antes de validar e antes de enviar ao servidor, e **nunca use a máscara como única indicação do formato** — coloque também um texto de ajuda visível, ligado ao campo por `aria-describedby`.

## 7. Mostrando o erro de forma acessível

Uma mensagem de erro só cumpre seu papel se **todo mundo** a percebe: quem enxerga, quem não distingue vermelho de verde e quem usa leitor de tela.

```js
// js/inscricao.js — exibição do estado de um campo

function mostrarErro(campo, mensagem) {
  const alvo = document.querySelector(`#erro-${campo.id}`);

  if (mensagem) {
    campo.classList.add("invalido");
    campo.classList.remove("valido");
    campo.setAttribute("aria-invalid", "true");
    campo.setAttribute("aria-describedby", `erro-${campo.id}`);
    alvo.textContent = mensagem;
  } else {
    campo.classList.remove("invalido");
    campo.classList.add("valido");
    campo.setAttribute("aria-invalid", "false");
    campo.removeAttribute("aria-describedby");
    alvo.textContent = "";
  }
}
```

**`css/estilo.css` — estados do formulário**

```css
/* ===== Formulário validado ===== */
.campo {
  display: grid;
  gap: 0.25rem;
  margin-bottom: 1.25rem;
}

.campo input,
.campo select,
.campo textarea {
  width: 100%;
  padding: 0.625rem 0.75rem;
  border: 2px solid var(--cor-borda, #ccc);
  border-radius: 6px;
  font: inherit;
  transition: border-color 0.2s;
}

.campo input:focus-visible,
.campo select:focus-visible {
  outline: 3px solid rgba(26, 127, 181, 0.4);
  outline-offset: 1px;
  border-color: var(--cor-secundaria, #1a7fb5);
}

.campo .invalido {
  border-color: #c0392b;
}

.campo .valido {
  border-color: #27ae60;
}

.erro {
  display: block;
  min-height: 1.2em; /* reserva espaço: evita o layout "pular" ao exibir o erro */
  color: #c0392b;
  font-size: 0.875rem;
}

.erro:not(:empty)::before {
  content: "⚠ "; /* o erro não depende só da cor */
}

@media (prefers-reduced-motion: reduce) {
  .campo input,
  .campo select {
    transition: none;
  }
}
```

Os cinco requisitos de acessibilidade em mensagens de erro:

1. **`role="alert"`** no elemento da mensagem: leitores de tela anunciam o conteúdo assim que ele aparece, sem o usuário precisar navegar até lá.
2. **`aria-invalid="true"`** no campo: o leitor anuncia "inválido" ao entrar no campo.
3. **`aria-describedby`** ligando o campo à mensagem: o texto do erro é lido junto com o rótulo.
4. **Nunca sinalize erro só pela cor.** Some texto e um símbolo (o `::before` do CSS acima).
5. **Reserve espaço para a mensagem** com `min-height`. Sem isso, o layout salta quando o erro aparece e o usuário perde a referência visual — e quem usa ampliador de tela se perde de vez.

### 7.1 Validação no envio e o foco no primeiro erro

```js
form.addEventListener("submit", (evento) => {
  evento.preventDefault();
  let primeiroInvalido = null;

  [...form.querySelectorAll("input, select, textarea")].forEach((campo) => {
    const valido = validarCampo(campo);
    if (!valido && !primeiroInvalido) primeiroInvalido = campo;
  });

  if (primeiroInvalido) {
    primeiroInvalido.focus();
    primeiroInvalido.scrollIntoView({ behavior: "smooth", block: "center" });
    return;
  }
  console.log("Dados válidos:", Object.fromEntries(new FormData(form).entries()));
});
```

Note que o `forEach` valida **todos** os campos antes de parar: o usuário vê de uma vez tudo o que precisa corrigir, e não um erro por tentativa. O `focus()` no primeiro inválido é obrigatório para quem navega por teclado — sem ele, a pessoa aperta "Enviar", nada acontece e ela não faz ideia de onde está o problema.

> **⚠️ Atenção**
> Toda a validação desta aula acontece **no navegador**, e o navegador é do usuário. Qualquer pessoa abre o DevTools, apaga o `required` e envia o formulário; ou envia a requisição direto, sem passar pela sua página. Validação no cliente serve para **experiência** (avisar cedo, evitar ida e volta ao servidor); a validação que serve para **segurança** é a do servidor, e você a construirá no Nível 2. Nunca confie em dados que vieram do navegador.

## 8. Guardando a inscrição com `localStorage`

O navegador oferece um armazenamento simples, que sobrevive ao fechamento da aba: o `localStorage`. Ele guarda pares chave/valor, **sempre em texto**.

```js
// Escrever
localStorage.setItem("inscricao:rascunho", JSON.stringify({ nome: "Ana", curso: "SI" }));

// Ler (devolve null quando a chave não existe)
const bruto = localStorage.getItem("inscricao:rascunho");
const rascunho = bruto ? JSON.parse(bruto) : null;

// Remover uma chave e limpar tudo
localStorage.removeItem("inscricao:rascunho");
localStorage.clear();
```

Como só há texto, objetos e arrays precisam de `JSON.stringify` na ida e `JSON.parse` na volta. Guardar `{ nome: "Ana" }` sem `stringify` armazena a string `"[object Object]"` — outro clássico da primeira semana.

| Recurso | Vive até | Cabe |
|---|---|---|
| `localStorage` | Ser apagado pelo código ou pelo usuário | Cerca de 5 MB por origem |
| `sessionStorage` | A aba ser fechada | Cerca de 5 MB por aba |
| Variável em JavaScript | A página recarregar | A memória disponível |

> **⚠️ Atenção**
> `localStorage` é legível por qualquer script da mesma origem e fica no computador, muitas vezes compartilhado. **Nunca** guarde senha, CPF, token de acesso ou dado de cartão. No rascunho da inscrição vamos salvar apenas nome, e-mail e curso — CPF e telefone ficam de fora, de propósito.

> **🔬 Investigue**
> Abra qualquer página do site, vá ao DevTools na aba **Application** (Chrome) ou **Armazenamento** (Firefox) e clique em **Local Storage** → a URL do seu site. Rode no console `localStorage.setItem("teste", "olá")` e veja a linha aparecer na tabela em tempo real. Feche o navegador inteiro, abra de novo, volte à página e rode `localStorage.getItem("teste")`: o valor continua lá. Agora abra a mesma página em uma janela anônima e repita o `getItem`: devolve `null`, porque a janela anônima é outra área de armazenamento.

## 9. Consultas dinâmicas: busca, filtro e ordenação

A segunda metade da aula responde a outra pergunta: como deixar o usuário **encontrar** o que procura numa lista? A resposta é sempre a mesma arquitetura da Aula 13 — **estado → dados → renderização → eventos** —, com o estado agora guardando o termo buscado, o filtro escolhido e o critério de ordenação.

### 9.1 O pipeline

A função que produz a lista visível é sempre a mesma sequência: **cópia → busca → filtro → ordenação**.

```js
// Estado da consulta (os nomes dos campos vêm do js/dados.js da Aula 12)
let termoBusca = "";
let areaAtual = "todas";
let ordenacaoAtual = "hora";

function obterPalestrasVisiveis() {
  let resultado = [...palestras]; // 1. cópia: sort() modifica o array original

  if (termoBusca) {                                       // 2. busca por texto
    const termo = normalizar(termoBusca);
    resultado = resultado.filter((p) => normalizar(p.titulo).includes(termo));
  }

  if (areaAtual !== "todas") {                            // 3. filtro por categoria
    resultado = resultado.filter((p) => p.area === areaAtual);
  }

  const ordenadores = {                                   // 4. ordenação
    hora: (a, b) => a.dia - b.dia || a.hora.localeCompare(b.hora),
    titulo: (a, b) => a.titulo.localeCompare(b.titulo, "pt-BR"),
    vagas: (a, b) => b.vagas - b.inscritos - (a.vagas - a.inscritos),
  };
  resultado.sort(ordenadores[ordenacaoAtual]);

  return resultado;
}
```

Três detalhes que separam código que funciona de código que funciona **sempre**:

- **`[...palestras]`** cria uma cópia. `sort()` reordena o array **original**; sem a cópia, a ordem dos dados mudaria a cada renderização e o filtro seguinte partiria de outra base. É um bug sutil, difícil de encontrar e frequente.
- **`localeCompare(b, "pt-BR")`** ordena corretamente palavras acentuadas. O `sort()` puro compara códigos de caractere e coloca "Ávila" **depois** de "Zampieri".
- **`a.dia - b.dia || a.hora.localeCompare(b.hora)`** é ordenação em dois níveis: quando os dias são iguais, a subtração dá `0` (falso) e o `||` passa para o critério de desempate. Repare no nome do campo: `hora`, como no `dados.js` da Aula 12. Inventar um `horario` aqui daria `undefined.localeCompare` — `TypeError` na primeira ordenação.

### 9.2 Buscar ignorando acentos e caixa

```js
function normalizar(texto) {
  return texto
    .normalize("NFD")               // separa a letra do acento combinante
    .replace(/[̀-ͯ]/g, "") // remove os acentos combinantes
    .toLowerCase()
    .trim();
}

normalizar("Segurança"); // "seguranca"
normalizar("CAFÉ");      // "cafe"
```

Na forma de normalização **NFD**, o caractere "é" é decomposto em "e" mais um acento combinante separado. Esses acentos vivem no intervalo Unicode `̀`–`ͯ`, e uma única regex com a flag `g` remove todos de uma vez. Aplique `normalizar` nos **dois** lados da comparação: no termo digitado e no texto pesquisado. Sem isso, quem digita "seguranca" no celular não encontra "Segurança" — e desiste.

### 9.3 `debounce`: não filtrar a cada tecla

Digitar "acessibilidade" dispara catorze eventos `input`. Filtrar e redesenhar catorze vezes trava a interface em listas grandes. O `debounce` da Aula 13 resolve: a função só executa quando os disparos **param** por um tempo.

```js
function debounce(fn, atraso = 300) {
  let temporizador;
  return function (...args) {
    clearTimeout(temporizador);
    temporizador = setTimeout(() => fn.apply(this, args), atraso);
  };
}
```

Entre 250 ms e 400 ms é a faixa que soa instantânea sem disparar demais. Abaixo de 150 ms você perde o efeito; acima de 600 ms o usuário sente atraso.

### 9.4 Estado vazio e contador

Toda listagem filtrável precisa de duas coisas que iniciantes esquecem:

- Uma **mensagem de estado vazio** que diga o que fazer ("Nenhuma atividade encontrada para 'xyz'. Tente outro termo ou limpe os filtros."), e não uma tela em branco.
- Um **contador anunciado** (`aria-live="polite"`) informando quantos resultados apareceram. Quem usa leitor de tela não vê a lista encolher; sem o contador, digitar na busca não produz nenhum retorno perceptível.

```html
<p id="contador-programacao" class="contador" aria-live="polite" role="status"></p>
```

> **🔎 Por baixo do capô**
> `aria-live="polite"` cria uma **região viva**: o leitor de tela passa a observar aquele elemento e anuncia mudanças de conteúdo assim que terminar de ler o que estava lendo. `assertive` interrompe na hora — reserve para erros graves. A região precisa existir no HTML **antes** de ser preenchida: se você criar o elemento e já colocar o texto dentro, muitos leitores não anunciam nada, porque não havia região para observar. É por isso que o `<p>` vazio já vem no HTML.

## 💻 Mão na massa — Inscrição validada e programação com busca

Ao fim destes oito passos, o site da **Semana Acadêmica de Sistemas de Informação** terá um formulário de inscrição que valida campo a campo com mensagens acessíveis, salva rascunho e mostra confirmação; e uma página de programação com busca em tempo real, filtro por área e ordenação — tudo sobre o array `palestras` do `js/dados.js` da Aula 12, **sem mudar uma linha daquele arquivo**.

> **⚠️ Atenção**
> `js/dados.js` é a fonte única de dados do projeto desde a Aula 12, e o esquema dele é lei: `palestras` com `area`, `hora` e `palestranteId`; o array `palestrantes`; o dicionário `nomesDasAreas`. O `js/relatorios.js` (Aula 12) e o `js/palestrantes.js` (Aula 13) já dependem desses nomes. Hoje você **adapta a consulta aos dados**, não os dados à consulta.

### Passo 1 — o formulário de `inscricao.html`

Primeiro o `<head>`, com os quatro scripts na ordem que importa — `defer` executa na ordem das tags, e `inscricao.js` precisa que `debounce` (do `app.js`, Passo 4) já exista:

**`inscricao.html` — `<head>` completo**

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Inscrição gratuita na Semana Acadêmica de Sistemas de Informação da UNEMAT Sinop.">
  <meta name="author" content="Curso de Sistemas de Informação — UNEMAT Sinop">
  <title>Inscrição — Semana Acadêmica de Sistemas de Informação</title>
  <link rel="stylesheet" href="css/estilo.css">
  <script src="js/menu.js" defer></script>
  <script src="js/dados.js" defer></script>
  <script src="js/app.js" defer></script>
  <script src="js/inscricao.js" defer></script>
</head>
```

Agora o `<main>`. A estrutura repete o mesmo bloco para cada campo: `<label>`, campo, `<span class="erro" role="alert">`.

> **⚠️ Atenção**
> A `<section class="vagas">` das Aulas 10 e 11 — com `#vagas-restantes`, `#vagas-totais`, `#percentual-ocupacao`, `#aviso-vagas` e `#valor-taxa` — **fica onde está**, acima do formulário. É ela que mostra o "Últimas vagas!" exigido no Checkpoint da Aula 11, e o código que a alimenta continua no `js/inscricao.js` (você o amplia no Passo 3, não o substitui). O que muda de lugar é só o `<form>`.

**`inscricao.html` — conteúdo do `<main>`**

```html
<main id="conteudo" tabindex="-1" class="container">
  <h1>Inscrição</h1>
  <p>Preencha os dados abaixo. Os campos marcados com * são obrigatórios.</p>

  <!-- Seção de vagas das Aulas 10 e 11: continua exatamente como estava -->
  <section class="vagas">
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

  <p id="aviso-formulario" class="aviso-formulario" role="status"></p>

  <form id="form-inscricao" novalidate>
    <fieldset>
      <legend>Seus dados</legend>

      <div class="campo">
        <label for="nome">Nome completo *</label>
        <input type="text" id="nome" name="nome" autocomplete="name"
               required minlength="5" maxlength="80">
        <span class="erro" id="erro-nome" role="alert"></span>
      </div>

      <div class="campo">
        <label for="email">E-mail *</label>
        <input type="email" id="email" name="email" autocomplete="email" required>
        <span class="erro" id="erro-email" role="alert"></span>
      </div>

      <div class="campo">
        <label for="cpf">CPF *</label>
        <input type="text" id="cpf" name="cpf" inputmode="numeric"
               maxlength="14" placeholder="000.000.000-00" required>
        <span class="erro" id="erro-cpf" role="alert"></span>
      </div>

      <div class="campo">
        <label for="telefone">Telefone com DDD *</label>
        <input type="text" id="telefone" name="telefone" inputmode="tel"
               maxlength="15" placeholder="(66) 99999-9999" required>
        <span class="erro" id="erro-telefone" role="alert"></span>
      </div>

      <div class="campo">
        <label for="nascimento">Data de nascimento *</label>
        <input type="text" id="nascimento" name="nascimento" inputmode="numeric"
               maxlength="10" placeholder="dd/mm/aaaa" required>
        <span class="erro" id="erro-nascimento" role="alert"></span>
      </div>
    </fieldset>

    <fieldset>
      <legend>Participação</legend>

      <div class="campo">
        <label for="curso">Curso ou vínculo *</label>
        <select id="curso" name="curso" required>
          <option value="">Selecione…</option>
          <option value="si">Sistemas de Informação</option>
          <option value="ads">Análise e Desenvolvimento de Sistemas</option>
          <option value="eng">Engenharias</option>
          <option value="outro">Outro curso da UNEMAT</option>
          <option value="externo">Comunidade externa</option>
        </select>
        <span class="erro" id="erro-curso" role="alert"></span>
      </div>

      <div class="campo">
        <span class="rotulo-grupo" id="rotulo-atividades">Atividades de interesse *</span>
        <div class="grupo-caixas" role="group" aria-labelledby="rotulo-atividades">
          <label><input type="checkbox" name="atividades" value="git"> Minicurso de Git</label>
          <label><input type="checkbox" name="atividades" value="acessibilidade"> Minicurso de acessibilidade</label>
          <label><input type="checkbox" name="atividades" value="maratona"> Maratona de programação</label>
          <label><input type="checkbox" name="atividades" value="palestras"> Somente palestras</label>
        </div>
        <span class="erro" id="erro-atividades" role="alert"></span>
      </div>

      <div class="campo">
        <label class="linha"><input type="checkbox" id="termos" name="termos" required>
          Li e aceito o regulamento do evento *</label>
        <span class="erro" id="erro-termos" role="alert"></span>
      </div>
    </fieldset>

    <div class="acoes-formulario">
      <button type="submit" class="botao">Enviar inscrição</button>
      <button type="button" class="botao botao--contorno" id="limpar-rascunho">Limpar rascunho</button>
    </div>
  </form>
</main>
```

Quatro decisões que valem nota: `novalidate` no formulário (as mensagens são nossas), `inputmode` nos campos numéricos (o celular abre o teclado certo sem mudar o `type`, como na Aula 04), o grupo de checkboxes dentro de um `role="group"` com `aria-labelledby` — assim o leitor de tela anuncia "Atividades de interesse, grupo" antes das opções — e a classe **`.aviso-formulario`** no parágrafo de resposta do envio. Ela **não** é a `.aviso` da Aula 11: aquela é a caixa vermelha de "Últimas vagas!", com `.aviso:empty { display: none }`, e continua sendo usada pelo `#aviso-vagas` logo acima. Dois componentes diferentes, dois nomes diferentes — reaproveitar o nome faria as duas regras brigarem no mesmo `estilo.css`.

### Passo 2 — o CSS dos campos

Acrescente ao fim de `css/estilo.css` o bloco da seção 7 e mais estes complementos:

**`css/estilo.css` — complementos do formulário**

```css
.grupo-caixas {
  display: grid;
  gap: 0.4rem;
}

.grupo-caixas label,
.campo label.linha {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 400;
}

.rotulo-grupo {
  font-weight: 600;
}

.acoes-formulario {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 1rem;
}

.aviso-formulario {
  min-height: 1.5em;
}

.aviso-formulario.sucesso {
  padding: 0.75rem 1rem;
  border-left: 4px solid #27ae60;
  background: #eafaf1;
  color: #14532d;
}

.aviso-formulario.falha {
  padding: 0.75rem 1rem;
  border-left: 4px solid #c0392b;
  background: #fdecea;
  color: #7f1d1d;
}
```

### Passo 3 — `js/inscricao.js` ampliado

O `js/inscricao.js` já existe desde a Aula 10 e cresceu na Aula 11: é ele que calcula as vagas restantes, o percentual de ocupação, o aviso "Últimas vagas!" e o valor da taxa. **Esse bloco não sai** — ele continua no topo do arquivo, sob o comentário `// ===== VAGAS (Aulas 10 e 11) =====`, e tudo o que você escreve hoje vem **depois** dele.

Este arquivo usa a função `debounce` para salvar o rascunho; ela é declarada no `js/app.js` no Passo 4, que toda página já carrega antes deste script.

**`js/inscricao.js`** (topo do arquivo — o que já existe, apenas identificado com um comentário)

```js
// js/inscricao.js — vagas (Aulas 10 e 11) e validação do formulário (Aula 14)

// ===== VAGAS (Aulas 10 e 11) =====
// As constantes VAGAS_TOTAIS e INSCRITOS, o cálculo do percentual, o aviso
// de "Últimas vagas!" e o valor da taxa continuam exatamente como estavam.
// Nada abaixo depende deles, e nada deles depende do que vem abaixo.
```

**`js/inscricao.js`** (acrescente a partir daqui)

```js
// ===== ESTADO =====
const CHAVE_RASCUNHO = "inscricao:rascunho";
const CAMPOS_DO_RASCUNHO = ["nome", "email", "curso"]; // sem CPF e sem telefone, de propósito

// ===== ELEMENTOS =====
const els = {
  form: document.querySelector("#form-inscricao"),
  aviso: document.querySelector("#aviso-formulario"),
  limpar: document.querySelector("#limpar-rascunho"),
};

// ===== PADRÕES =====
const PADROES = {
  telefone: /^\(?\d{2}\)?\s?9?\d{4}-?\d{4}$/,
  email: /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/,
  data: /^(0[1-9]|[12]\d|3[01])\/(0[1-9]|1[0-2])\/\d{4}$/,
};

// ===== VALIDADORES (funções puras) =====
function validarNomeCompleto(valor) {
  const partes = valor.trim().split(/\s+/);
  if (valor.trim() === "") return "O nome completo é obrigatório.";
  if (partes.length < 2) return "Informe nome e sobrenome.";
  if (partes.some((parte) => parte.length < 2)) {
    return "Cada parte do nome deve ter ao menos 2 letras.";
  }
  return "";
}

function validarEmail(valor) {
  const v = valor.trim();
  if (v === "") return "O e-mail é obrigatório.";
  if (!PADROES.email.test(v)) return "Informe um e-mail no formato nome@dominio.br.";
  return "";
}

function validarTelefone(valor) {
  const v = valor.trim();
  if (v === "") return "O telefone é obrigatório.";
  if (!PADROES.telefone.test(v)) return "Informe o telefone com DDD, como (66) 99999-9999.";
  return "";
}

function validarCPF(cpf) {
  const numeros = cpf.replace(/\D/g, "");
  if (numeros === "") return "O CPF é obrigatório.";
  if (numeros.length !== 11) return "O CPF deve ter 11 dígitos.";
  if (/^(\d)\1{10}$/.test(numeros)) return "CPF inválido.";

  const calcularDigito = (base, pesoInicial) => {
    let soma = 0;
    for (let i = 0; i < base.length; i++) {
      soma = soma + Number(base[i]) * (pesoInicial - i);
    }
    const resto = (soma * 10) % 11;
    return resto === 10 ? 0 : resto;
  };

  const primeiro = calcularDigito(numeros.slice(0, 9), 10);
  const segundo = calcularDigito(numeros.slice(0, 10), 11);

  if (primeiro !== Number(numeros[9]) || segundo !== Number(numeros[10])) {
    return "CPF inválido. Confira os números digitados.";
  }
  return "";
}

function calcularIdade(dataTexto) {
  const partes = dataTexto.trim().split("/");
  if (partes.length !== 3) return null;

  const dia = Number(partes[0]);
  const mes = Number(partes[1]);
  const ano = Number(partes[2]);
  const data = new Date(ano, mes - 1, dia);

  const existe =
    data.getFullYear() === ano && data.getMonth() === mes - 1 && data.getDate() === dia;
  if (!existe) return null;

  const hoje = new Date();
  let anos = hoje.getFullYear() - ano;
  const jaFez =
    hoje.getMonth() > mes - 1 || (hoje.getMonth() === mes - 1 && hoje.getDate() >= dia);
  if (!jaFez) anos = anos - 1;
  return anos;
}

function validarNascimento(valor) {
  const v = valor.trim();
  if (v === "") return "A data de nascimento é obrigatória.";
  if (!PADROES.data.test(v)) return "Use o formato dd/mm/aaaa.";
  const anos = calcularIdade(v);
  if (anos === null) return "Essa data não existe no calendário.";
  if (anos < 0) return "A data de nascimento não pode estar no futuro.";
  if (anos < 16) return "É necessário ter ao menos 16 anos para se inscrever.";
  if (anos > 120) return "Confira o ano digitado.";
  return "";
}

function validarCurso(valor) {
  return valor === "" ? "Escolha o seu curso ou vínculo." : "";
}

function validarAtividades() {
  const marcadas = els.form.querySelectorAll("input[name='atividades']:checked");
  return marcadas.length === 0 ? "Escolha ao menos uma atividade." : "";
}

function validarTermos(marcado) {
  return marcado ? "" : "É preciso aceitar o regulamento para se inscrever.";
}

// ===== MÁSCARAS =====
function mascaraCPF(valor) {
  return valor
    .replace(/\D/g, "")
    .slice(0, 11)
    .replace(/(\d{3})(\d)/, "$1.$2")
    .replace(/(\d{3})(\d)/, "$1.$2")
    .replace(/(\d{3})(\d{1,2})$/, "$1-$2");
}

function mascaraTelefone(valor) {
  return valor
    .replace(/\D/g, "")
    .slice(0, 11)
    .replace(/(\d{2})(\d)/, "($1) $2")
    .replace(/(\d{5})(\d)/, "$1-$2");
}

function mascaraData(valor) {
  return valor
    .replace(/\D/g, "")
    .slice(0, 8)
    .replace(/(\d{2})(\d)/, "$1/$2")
    .replace(/(\d{2})(\d)/, "$1/$2");
}

// ===== EXIBIÇÃO =====
function mostrarErro(campo, mensagem) {
  const alvo = document.querySelector(`#erro-${campo.id}`);
  if (!alvo) return;

  if (mensagem) {
    campo.classList.add("invalido");
    campo.classList.remove("valido");
    campo.setAttribute("aria-invalid", "true");
    campo.setAttribute("aria-describedby", `erro-${campo.id}`);
    alvo.textContent = mensagem;
  } else {
    campo.classList.remove("invalido");
    campo.classList.add("valido");
    campo.setAttribute("aria-invalid", "false");
    campo.removeAttribute("aria-describedby");
    alvo.textContent = "";
  }
}

function mostrarAviso(texto, tipo) {
  els.aviso.textContent = texto;
  els.aviso.className = texto ? `aviso-formulario ${tipo}` : "aviso-formulario";
}

// ===== ORQUESTRAÇÃO =====
function validarCampo(campo) {
  let mensagem = "";

  switch (campo.id) {
    case "nome":
      mensagem = validarNomeCompleto(campo.value);
      break;
    case "email":
      mensagem = validarEmail(campo.value);
      break;
    case "cpf":
      mensagem = validarCPF(campo.value);
      break;
    case "telefone":
      mensagem = validarTelefone(campo.value);
      break;
    case "nascimento":
      mensagem = validarNascimento(campo.value);
      break;
    case "curso":
      mensagem = validarCurso(campo.value);
      break;
    case "termos":
      mensagem = validarTermos(campo.checked);
      break;
    default:
      mensagem = "";
  }

  if (campo.name === "atividades") {
    const grupo = document.querySelector("#erro-atividades");
    grupo.textContent = validarAtividades();
    return grupo.textContent === "";
  }

  mostrarErro(campo, mensagem);
  return mensagem === "";
}

function camposValidaveis() {
  return [...els.form.querySelectorAll("#nome, #email, #cpf, #telefone, #nascimento, #curso, #termos")];
}

// ===== RASCUNHO (localStorage) =====
function salvarRascunho() {
  const dados = {};
  CAMPOS_DO_RASCUNHO.forEach((nome) => {
    dados[nome] = els.form.elements[nome].value;
  });
  localStorage.setItem(CHAVE_RASCUNHO, JSON.stringify(dados));
}

function restaurarRascunho() {
  const bruto = localStorage.getItem(CHAVE_RASCUNHO);
  if (!bruto) return;

  const dados = JSON.parse(bruto);
  CAMPOS_DO_RASCUNHO.forEach((nome) => {
    if (dados[nome]) els.form.elements[nome].value = dados[nome];
  });
  mostrarAviso("Recuperamos o rascunho que você tinha começado.", "sucesso");
}

function limparRascunho() {
  localStorage.removeItem(CHAVE_RASCUNHO);
  els.form.reset();
  camposValidaveis().forEach((campo) => {
    campo.classList.remove("valido", "invalido");
    campo.removeAttribute("aria-invalid");
    mostrarErro(campo, "");
  });
  document.querySelector("#erro-atividades").textContent = "";
  mostrarAviso("Rascunho apagado.", "sucesso");
}

// ===== EVENTOS =====
function registrarEventos() {
  // Máscaras
  document.querySelector("#cpf").addEventListener("input", (e) => {
    e.target.value = mascaraCPF(e.target.value);
  });
  document.querySelector("#telefone").addEventListener("input", (e) => {
    e.target.value = mascaraTelefone(e.target.value);
  });
  document.querySelector("#nascimento").addEventListener("input", (e) => {
    e.target.value = mascaraData(e.target.value);
  });

  // Valide no blur; depois do primeiro erro, valide também no input
  camposValidaveis().forEach((campo) => {
    campo.addEventListener("blur", () => {
      validarCampo(campo);
      campo.dataset.tocado = "true";
    });
    campo.addEventListener("input", () => {
      if (campo.dataset.tocado === "true") validarCampo(campo);
    });
  });

  // Grupo de checkboxes: um ouvinte só, por delegação
  els.form.addEventListener("change", (e) => {
    if (e.target.name === "atividades") validarCampo(e.target);
  });

  // Rascunho: salva 500 ms depois de o usuário parar de digitar
  els.form.addEventListener("input", debounce(salvarRascunho, 500));
  els.limpar.addEventListener("click", limparRascunho);

  // Envio
  els.form.addEventListener("submit", (e) => {
    e.preventDefault();

    let primeiroInvalido = null;
    camposValidaveis().forEach((campo) => {
      const ok = validarCampo(campo);
      campo.dataset.tocado = "true";
      if (!ok && !primeiroInvalido) primeiroInvalido = campo;
    });

    const erroAtividades = validarAtividades();
    document.querySelector("#erro-atividades").textContent = erroAtividades;

    if (primeiroInvalido || erroAtividades) {
      mostrarAviso("Confira os campos destacados antes de enviar.", "falha");
      const alvo = primeiroInvalido || document.querySelector("input[name='atividades']");
      alvo.focus();
      alvo.scrollIntoView({ behavior: "smooth", block: "center" });
      return;
    }

    const dados = Object.fromEntries(new FormData(els.form).entries());
    dados.atividades = new FormData(els.form).getAll("atividades");
    dados.cpf = dados.cpf.replace(/\D/g, ""); // sem máscara, como o servidor espera
    dados.telefone = dados.telefone.replace(/\D/g, "");
    console.log("Inscrição válida:", dados);

    localStorage.removeItem(CHAVE_RASCUNHO);
    els.form.reset();
    camposValidaveis().forEach((campo) => campo.classList.remove("valido", "invalido"));
    mostrarAviso(
      `Inscrição de ${dados.nome} registrada! Você receberá a confirmação em ${dados.email}.`,
      "sucesso"
    );
  });
}

// ===== INICIALIZAÇÃO =====
function iniciar() {
  if (!els.form) return;
  registrarEventos();
  restaurarRascunho();
}

iniciar();
```

### Passo 4 — `debounce` disponível em todas as páginas

O `debounce` é usado pelo rascunho e, no próximo passo, pela busca. Como todas as páginas carregam `js/app.js` **antes** do script específico (os dois com `defer`, e `defer` preserva a ordem das tags), basta declarar a função lá uma vez. Confira que o `<script src="js/app.js" defer>` está mesmo no `<head>` das **cinco** páginas — inclusive em `programacao.html`, que vai usar o `debounce` no Passo 7. Sem ele, a busca morre no primeiro caractere digitado com `Uncaught ReferenceError: debounce is not defined`.

**`js/app.js` — acrescente ao fim**

```js
// Utilitário compartilhado: adia a execução até os disparos pararem por X ms.
// Como este arquivo é carregado antes dos scripts de página, a função fica
// disponível para inscricao.js e programacao.js.
function debounce(fn, atraso = 300) {
  let temporizador;
  return function (...args) {
    clearTimeout(temporizador);
    temporizador = setTimeout(() => fn.apply(this, args), atraso);
  };
}
```

### Passo 5 — conferir (e não tocar) o `js/dados.js`

Não há arquivo novo aqui: o `js/dados.js` da Aula 12 já tem tudo de que a consulta precisa. Abra-o e confirme os três nomes que os próximos passos vão usar:

| Nome | O que é | Campos usados hoje |
|---|---|---|
| `palestras` | array com as 12 atividades | `id`, `titulo`, `tipo`, `area`, `dia`, `hora`, `local`, `vagas`, `inscritos`, `palestranteId` |
| `palestrantes` | array com as 6 pessoas | `id`, `nome`, `instituicao` |
| `nomesDasAreas` | dicionário código → nome | `web`, `dados`, `seguranca`, `ia` |

Duas armadilhas que este passo evita:

- **O campo do horário chama `hora`, não `horario`.** Um `p.horario` devolve `undefined`, e `undefined.localeCompare(…)` derruba a ordenação inteira com `TypeError`.
- **A palestra não guarda o nome de quem apresenta, só o `palestranteId`.** Para buscar por nome, você precisa cruzar as duas listas — exatamente o que o relatório 7 da Aula 12 fazia com `find`. É a mesma ideia de chave estrangeira que você verá no Nível 2.

Se você sentir vontade de "só ajustar um campinho" no `dados.js` para simplificar o filtro, resista: o `js/relatorios.js` (Aula 12) e o `js/palestrantes.js` (Aula 13) leem esse mesmo arquivo e quebram junto. Adaptar o consumidor ao dado é barato; adaptar o dado a um consumidor é como se perde a fonte única.

### Passo 6 — a interface de consulta em `programacao.html`

Troque os cartões escritos à mão (Aula 07) por um contêiner vazio e os controles de consulta. Antes, o `<head>` com os cinco scripts:

**`programacao.html` — `<head>` completo**

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Programação completa da Semana Acadêmica de Sistemas de Informação da UNEMAT Sinop.">
  <meta name="author" content="Curso de Sistemas de Informação — UNEMAT Sinop">
  <title>Programação — Semana Acadêmica de Sistemas de Informação</title>
  <link rel="stylesheet" href="css/estilo.css">
  <script src="js/menu.js" defer></script>
  <script src="js/dados.js" defer></script>
  <script src="js/app.js" defer></script>
  <script src="js/relatorios.js" defer></script>
  <script src="js/programacao.js" defer></script>
</head>
```

O `relatorios.js` da Aula 12 continua aqui: ele só escreve no Console e não atrapalha nada. E repare que `js/app.js` vem **antes** de `js/programacao.js`: é dele que sai o `debounce` do Passo 4.

**`programacao.html` — conteúdo do `<main>`**

```html
<main id="conteudo" tabindex="-1" class="container">
  <h1>Programação</h1>
  <p>Três dias de palestras, minicursos e maratona. Use a busca e os filtros para achar sua atividade.</p>

  <form class="consulta" id="consulta-programacao" role="search">
    <div class="campo">
      <label for="busca">Buscar por título ou palestrante</label>
      <input type="search" id="busca" name="busca" placeholder="Ex.: acessibilidade"
             autocomplete="off">
    </div>

    <div class="campo">
      <label for="area">Área</label>
      <select id="area" name="area">
        <option value="todas">Todas as áreas</option>
        <option value="web">Desenvolvimento Web</option>
        <option value="dados">Ciência de Dados</option>
        <option value="seguranca">Segurança</option>
        <option value="ia">Inteligência Artificial</option>
      </select>
    </div>

    <div class="campo">
      <label for="ordenacao">Ordenar por</label>
      <select id="ordenacao" name="ordenacao">
        <option value="hora">Dia e horário</option>
        <option value="titulo">Título (A–Z)</option>
        <option value="vagas">Vagas restantes</option>
      </select>
    </div>

    <button type="button" class="botao botao--contorno" id="limpar-consulta">Limpar filtros</button>
  </form>

  <p id="contador-programacao" class="contador" role="status" aria-live="polite"></p>

  <ul id="lista-programacao" class="cartoes"></ul>
</main>
```

O `<form role="search">` não envia nada: ele existe para agrupar os controles semanticamente (leitores de tela anunciam "busca") e para o `reset()` do botão "Limpar filtros" funcionar de graça. Os cinco `<script>` precisam estar **na ordem do `<head>` acima**: `dados.js` declara `palestras` e `palestrantes`, `app.js` declara `debounce`, e só então `programacao.js` usa os três.

### Passo 7 — `js/programacao.js`

Ele consome `palestras`, `palestrantes` e `nomesDasAreas` do `js/dados.js` — sem redeclarar nada — e `debounce` do `js/app.js`. Os nomes das constantes e funções levam o sufixo `Programacao` pelo mesmo motivo da Aula 13: scripts sem `type="module"` dividem o escopo global, e um `els` ou um `renderizar` genérico colide com o do arquivo vizinho no dia em que as duas páginas carregarem os dois.

**`js/programacao.js`**

```js
// js/programacao.js — busca, filtro e ordenação da programação.
// Depende de js/dados.js (palestras, palestrantes, nomesDasAreas) e de
// js/app.js (debounce), ambos carregados antes deste arquivo.

// ===== ESTADO =====
let termoBusca = "";
let areaAtualProgramacao = "todas";
let ordenacaoAtual = "hora";

// ===== ELEMENTOS =====
const elementosProgramacao = {
  form: document.querySelector("#consulta-programacao"),
  busca: document.querySelector("#busca"),
  area: document.querySelector("#area"),
  ordenacao: document.querySelector("#ordenacao"),
  limpar: document.querySelector("#limpar-consulta"),
  lista: document.querySelector("#lista-programacao"),
  contador: document.querySelector("#contador-programacao"),
};

// ===== FUNÇÕES DE DADOS =====
function normalizar(texto) {
  return texto
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .toLowerCase()
    .trim();
}

/**
 * Cruza a palestra com o array de palestrantes pelo palestranteId.
 * É a mesma junção do relatório 7 da Aula 12: `find` + `?.` + `??`.
 * @param {Object} palestra - item de `palestras`
 * @returns {string} o nome de quem apresenta, ou "A definir"
 */
function nomeDoPalestrante(palestra) {
  const pessoa = palestrantes.find((p) => p.id === palestra.palestranteId);
  return pessoa?.nome ?? "A definir";
}

function vagasRestantes(palestra) {
  return palestra.vagas - palestra.inscritos;
}

function obterPalestrasVisiveis() {
  let resultado = [...palestras]; // cópia: sort() altera o array original

  if (termoBusca) {
    const termo = normalizar(termoBusca);
    resultado = resultado.filter(
      (p) =>
        normalizar(p.titulo).includes(termo) ||
        normalizar(nomeDoPalestrante(p)).includes(termo) ||
        normalizar(p.local).includes(termo)
    );
  }

  if (areaAtualProgramacao !== "todas") {
    resultado = resultado.filter((p) => p.area === areaAtualProgramacao);
  }

  const ordenadores = {
    hora: (a, b) => a.dia - b.dia || a.hora.localeCompare(b.hora),
    titulo: (a, b) => a.titulo.localeCompare(b.titulo, "pt-BR"),
    vagas: (a, b) => vagasRestantes(b) - vagasRestantes(a),
  };
  resultado.sort(ordenadores[ordenacaoAtual]);

  return resultado;
}

// ===== RENDERIZAÇÃO =====
function criarCartaoDePalestra(palestra) {
  const item = document.createElement("li");
  item.classList.add("cartao");
  item.dataset.id = palestra.id;

  const restantes = vagasRestantes(palestra);
  if (restantes === 0) {
    const selo = document.createElement("span");
    selo.classList.add("cartao__selo");
    selo.textContent = "Esgotado";
    item.appendChild(selo);
  }

  const titulo = document.createElement("h2");
  titulo.textContent = palestra.titulo;

  const meta = document.createElement("p");
  meta.classList.add("cartao__meta");
  meta.textContent = `Dia ${palestra.dia} · ${palestra.hora} · ${palestra.local}`;

  const quem = document.createElement("p");
  quem.textContent = nomeDoPalestrante(palestra);

  const etiqueta = document.createElement("span");
  etiqueta.classList.add("etiqueta");
  etiqueta.textContent = nomesDasAreas[palestra.area];

  const vagas = document.createElement("p");
  vagas.classList.add("cartao__vagas");
  vagas.textContent =
    restantes === 0 ? "Sem vagas — entre na lista de espera" : `${restantes} vagas restantes`;

  item.append(titulo, meta, quem, etiqueta, vagas);
  return item;
}

function renderizarProgramacao() {
  const visiveis = obterPalestrasVisiveis();
  elementosProgramacao.lista.innerHTML = "";

  if (visiveis.length === 0) {
    const vazio = document.createElement("li");
    vazio.classList.add("vazio");
    vazio.textContent = termoBusca
      ? `Nenhuma atividade encontrada para "${termoBusca}". Tente outro termo ou limpe os filtros.`
      : "Nenhuma atividade nesta área. Escolha outra ou limpe os filtros.";
    elementosProgramacao.lista.appendChild(vazio);
  } else {
    const fragmento = document.createDocumentFragment();
    visiveis.forEach((p) => fragmento.appendChild(criarCartaoDePalestra(p)));
    elementosProgramacao.lista.appendChild(fragmento);
  }

  elementosProgramacao.contador.textContent =
    visiveis.length === 1 ? "1 atividade encontrada" : `${visiveis.length} atividades encontradas`;
}

// ===== EVENTOS =====
function registrarEventosDaProgramacao() {
  elementosProgramacao.busca.addEventListener(
    "input",
    debounce((e) => {
      termoBusca = e.target.value;
      renderizarProgramacao();
    }, 300)
  );

  elementosProgramacao.area.addEventListener("change", (e) => {
    areaAtualProgramacao = e.target.value;
    renderizarProgramacao();
  });

  elementosProgramacao.ordenacao.addEventListener("change", (e) => {
    ordenacaoAtual = e.target.value;
    renderizarProgramacao();
  });

  elementosProgramacao.limpar.addEventListener("click", () => {
    elementosProgramacao.form.reset();
    termoBusca = "";
    areaAtualProgramacao = "todas";
    ordenacaoAtual = "hora";
    renderizarProgramacao();
    elementosProgramacao.busca.focus();
  });
}

// ===== INICIALIZAÇÃO =====
function iniciarProgramacao() {
  if (!elementosProgramacao.lista) return;
  registrarEventosDaProgramacao();
  renderizarProgramacao();
}

iniciarProgramacao();
```

### Passo 8 — o CSS da consulta

**`css/estilo.css` — acrescente ao fim**

```css
/* ===== Consulta da programação ===== */
.consulta {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  align-items: end;
  gap: 1rem;
  margin-block: 1.5rem;
  padding: 1rem;
  border-radius: 12px;
  background: var(--cor-fundo);
  border: 1px solid var(--cor-borda);
}

.consulta .campo {
  margin-bottom: 0;
}

.cartao__vagas {
  font-size: 0.875rem;
}

.contador {
  font-weight: 600;
}
```

### Como testar

1. Abra `inscricao.html` com o Live Server. Clique no campo "Nome completo", saia sem digitar: aparece "O nome completo é obrigatório." em vermelho, com o símbolo de alerta, e a borda fica vermelha. Digite "Ana": a mensagem muda para "Informe nome e sobrenome." **enquanto você digita** — porque o campo já foi tocado.
2. Digite qualquer sequência de 11 dígitos no CPF: a máscara aplica pontos e traço sozinha. Teste `111.111.111-11` (rejeitado por repetição) e `123.456.789-00` (rejeitado pelos dígitos verificadores). Um CPF válido de verdade deixa a borda verde.
3. No campo de nascimento, digite `31/02/2000`: "Essa data não existe no calendário." Digite uma data que resulte em menos de 16 anos: "É necessário ter ao menos 16 anos para se inscrever."
4. Clique em "Enviar inscrição" com o formulário vazio: todos os erros aparecem de uma vez, o foco vai para o primeiro campo inválido, a página rola até ele e o aviso do topo diz "Confira os campos destacados antes de enviar."
5. Preencha tudo corretamente e envie: o console mostra o objeto com `cpf` e `telefone` **sem máscara**, `atividades` como array, e a página exibe a mensagem verde de sucesso.
6. Preencha só o nome e o e-mail e recarregue a página (<kbd>F5</kbd>): os valores voltam e o aviso diz que o rascunho foi recuperado. Confira no DevTools → Application → Local Storage que a chave `inscricao:rascunho` **não** contém CPF nem telefone. Clique em "Limpar rascunho" e recarregue: o formulário volta vazio.
7. Abra `programacao.html`: os **doze** cartões do `dados.js` aparecem ordenados por dia e horário, e o contador diz "12 atividades encontradas". Cada cartão mostra o nome de quem apresenta — resolvido pelo `palestranteId`, não digitado.
8. Digite `seguranca` (sem cedilha e sem acento) na busca: aparece "Segurança em aplicações web: dez erros comuns". Digite `carla`: aparecem as duas atividades de Carla Mendes, provando que a busca cruza as duas listas. Digite `xyz`: a mensagem de estado vazio explica o que fazer.
9. Mude "Ordenar por" para "Vagas restantes": o minicurso de Git e o de redes neurais (ambos esgotados) vão para o fim e ganham o selo "Esgotado". Mude para "Título (A–Z)" e confira que os acentos ficam na ordem correta. No filtro de área, "Segurança" deixa duas atividades e "Inteligência Artificial", outras duas.
10. Percorra a página inteira com <kbd>Tab</kbd>: todo campo tem foco visível, o botão "Limpar filtros" devolve o foco à busca, e o console está sem nenhum erro em vermelho nas cinco páginas — em especial, nenhum `ReferenceError: debounce is not defined` e nenhum `Identifier … has already been declared`.
11. Ainda em `inscricao.html`, confira que a seção de vagas continua no topo, com o número calculado e o aviso "Últimas vagas!" das Aulas 10 e 11 — e que ele é visualmente diferente do aviso verde/vermelho do envio do formulário.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Por que `event.preventDefault()` é obrigatório no ouvinte de `submit` quando o formulário é processado em JavaScript? O que acontece exatamente sem ele?

**A2.** Cite as três formas de ler os valores de um formulário e uma vantagem de cada uma.

**A3.** O que `input.value` devolve em um campo `type="number"`? Escreva a conversão correta e diga o que acontece se o campo estiver vazio.

**A4.** Diferencie os eventos `input`, `change` e `blur` para fins de validação. Qual deles não borbulha, e qual é a alternativa borbulhante?

**A5.** Para que serve o atributo `novalidate` no `<form>`? Por que mantemos `required` e `pattern` no HTML mesmo assim?

**A6.** O que fazem `campo.checkValidity()`, `campo.reportValidity()` e `campo.setCustomValidity()`? Qual armadilha o terceiro traz?

**A7.** Por que sinalizar erro apenas pela cor da borda é um problema de acessibilidade? Cite duas formas de resolver.

**A8.** Para que servem `role="alert"`, `aria-invalid` e `aria-describedby` na exibição de erros? O que cada um muda para quem usa leitor de tela?

**A9.** Reescreva como mensagem útil: "Erro no campo 3". Invente o contexto que preferir e justifique a sua escolha em uma linha.

**A10.** Por que a validação no navegador não substitui a validação no servidor? Descreva, em duas frases, como alguém burlaria a sua validação.

**A11.** O que faz `Object.fromEntries(new FormData(form).entries())`? Cite duas limitações do `FormData`.

**A12.** Por que a máscara precisa ser removida antes de validar e de enviar o dado?

**A13.** O que fazem as flags `g`, `i` e `m` de uma expressão regular?

**A14.** Qual a diferença entre `\d`, `\w` e `\s`? E entre `\d` e `\D`?

**A15.** O que casa cada padrão: `/a+/`, `/a*/`, `/a?/`, `/a{2,4}/`? Dê um exemplo de string aceita e uma rejeitada para cada.

**A16.** Diferencie quantificador guloso de preguiçoso, com um exemplo próprio.

**A17.** Qual a diferença entre `/\d{3}/` e `/^\d{3}$/`? Por que isso é crítico em validação?

**A18.** O que faz `\b`? Dê um exemplo em que a presença dele muda o resultado.

**A19.** Diferencie `(abc)` de `(?:abc)`. Quando você usaria o segundo?

**A20.** O que faz o lookahead `(?=…)`? Escreva uma regex que aceite apenas strings que contenham ao menos um dígito, em qualquer posição.

**A21.** Escreva a regex para: (a) somente dígitos; (b) somente letras, com acento; (c) alfanumérico de 6 a 12 caracteres; (d) começa com maiúscula; (e) termina com `.pdf`.

**A22.** Diferencie `test()`, `match()` e `matchAll()`. Qual deles exige a flag `g`?

**A23.** Escreva o `replace` que converta `"07/05/1998"` em `"1998-05-07"`, usando grupos capturados.

**A24.** Por que a validação de e-mail por regex não deve ser rigorosa demais? Qual é a estratégia profissional recomendada?

**A25.** O que a regex **não** consegue validar em um CPF? E em uma data?

**A26.** O que é ReDoS e qual padrão de escrita costuma causá-lo?

**A27.** Por que `[...palestras]` aparece antes do `sort()` em `obterPalestrasVisiveis()`? Descreva o bug que surge sem essa cópia.

**A28.** O que `localeCompare(b, "pt-BR")` resolve que o `sort()` puro não resolve? Dê um exemplo com nomes acentuados.

**A29.** Explique, linha a linha, o que a função `normalizar()` faz com a string `"Segurança"`.

**A30.** Por que o `<p>` do contador de resultados precisa existir vazio no HTML em vez de ser criado pelo JavaScript?

### Nível B — Aplicação

**B1.** Implemente um formulário de login com validação de e-mail, senha de no mínimo 8 caracteres, botão "mostrar senha" que alterna o `type` do campo, bloqueio após três tentativas com contagem regressiva de 30 segundos e mensagens acessíveis por campo.

Resultado esperado: as três tentativas erradas desabilitam o botão de envio e mostram "Tente novamente em 30, 29, 28… segundos"; o botão "mostrar senha" tem `aria-pressed` sincronizado; nenhum erro é sinalizado só por cor.

<details><summary>Dica</summary>

Guarde o número de tentativas em uma variável de estado e use `setInterval` para a contagem, limpando com `clearInterval` ao chegar a zero. Para alternar o tipo do campo: `campo.type = campo.type === "password" ? "text" : "password"`.
</details>

**B2.** Crie um medidor de força de senha com cinco critérios (comprimento ≥ 8, maiúscula, minúscula, número e caractere especial), exibindo a lista de critérios que ficam verdes conforme atendidos e uma barra de progresso colorida.

Resultado esperado: cada critério é um `<li>` com um ícone que muda de estado; a barra usa `<meter>` ou uma `div` com largura proporcional; o texto do nível ("Fraca", "Razoável", "Forte") é anunciado por uma região `aria-live`.

<details><summary>Dica</summary>

Uma regex por critério: `/[A-Z]/`, `/[a-z]/`, `/\d/`, `/[^A-Za-z0-9]/`. Some um ponto por critério atendido e penalize repetições com `/(.)\1{2,}/`. Nunca guarde a senha em `localStorage`.
</details>

**B3.** Implemente a validação de data de nascimento como um componente independente: o campo calcula a idade exata em tempo real e a exibe ao lado ("Você tem 19 anos"), rejeita datas futuras, datas que não existem no calendário e idade abaixo de 16 anos.

Resultado esperado: digitar `29/02/2001` mostra "Essa data não existe no calendário" (2001 não é bissexto); digitar `29/02/2000` é aceito; a idade aparece assim que a data fica completa e válida.

<details><summary>Dica</summary>

Reaproveite `calcularIdade` da Mão na massa e teste a existência da data reconstruindo dia, mês e ano do objeto `Date`, como explica a seção 4.1. Para o ano bissexto você não precisa de regra própria: o `Date` já sabe.
</details>

**B4.** Construa um formulário de agendamento de sala com: data (não pode ser passada nem fim de semana), horário em um `<select>` gerado dinamicamente de 30 em 30 minutos entre 8h e 18h, duração em horas e observações, exibindo um resumo textual do agendamento antes da confirmação.

Resultado esperado: as opções do `<select>` são criadas por um laço, não escritas à mão; escolher um sábado mostra "A sala não é liberada aos fins de semana"; o resumo é atualizado a cada alteração e lido por uma região `aria-live`.

<details><summary>Dica</summary>

`data.getDay()` devolve 0 para domingo e 6 para sábado. Para gerar os horários, um `for` de 8 a 17 com dois `push` por hora (`:00` e `:30`) resolve. Use `String(hora).padStart(2, "0")` para formatar.
</details>

**B5.** Pegue o formulário de contato de `contato.html` (Unidade 1), que hoje só tem validação nativa, e adicione validação completa em JavaScript sem alterar o HTML além de acrescentar os `<span>` de erro. Documente cada regra implementada em um comentário no topo do arquivo.

Resultado esperado: um arquivo `js/contato.js` com validadores puros e reaproveitáveis; o HTML mantém `required` e `type`, e ganha apenas os `<span class="erro" role="alert">`; o console fica limpo.

<details><summary>Dica</summary>

Comece copiando a estrutura de `js/inscricao.js` e apagando o que não se aplica. As funções `mostrarErro`, `validarEmail` e `validarNomeCompleto` saem de lá sem alteração — esse é o ponto de escrever validadores puros.
</details>

**B6.** Escreva e teste expressões regulares para validar: matrícula da UNEMAT (quatro dígitos de ano seguidos de cinco dígitos), placa Mercosul, código de rastreio dos Correios (duas letras, nove dígitos e `BR`), IPv4 e cartão com 16 dígitos com ou sem espaços e hífens.

Resultado esperado: uma página `exercicios/aula14/regex.html` com um campo por padrão, validação em tempo real e, ao lado de cada campo, três exemplos válidos e três inválidos que você testou.

<details><summary>Dica</summary>

Ancore tudo com `^` e `$`. Para o IPv4, cada octeto vai de 0 a 255: `(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)` repetido quatro vezes, separado por `\.`. Teste cada expressão no <https://regex101.com> antes de colar no código.
</details>

**B7.** Escreva `gerarSlug(titulo)` que converta `"Minicurso: Acessibilidade na Prática — Nível 1!"` em `"minicurso-acessibilidade-na-pratica-nivel-1"`, tratando acentos, símbolos, espaços múltiplos e hífens nas pontas.

Resultado esperado: uma função pura com cinco casos de teste no console, incluindo uma string só com símbolos (que deve devolver string vazia) e uma com espaços nas pontas.

<details><summary>Dica</summary>

O caminho é: `normalizar` (seção 9.2) para tirar acentos, `replace(/[^a-z0-9]+/g, "-")` para trocar tudo que não é alfanumérico por hífen e `replace(/^-+|-+$/g, "")` para limpar as pontas.
</details>

**B8.** Implemente um destacador de busca: dado o termo digitado e o texto de cada cartão da programação, envolva todas as ocorrências em `<mark>`, ignorando maiúsculas e acentos, sem quebrar quando o termo contiver caracteres especiais de regex.

Resultado esperado: buscar `web` destaca "web" em todos os títulos; buscar `(` não gera erro no console; o destaque some ao limpar a busca.

<details><summary>Dica</summary>

Escape o termo antes de montar a regex: `termo.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")`. Como o destaque exige HTML, este é o único lugar da aula em que `innerHTML` é aceitável — e só porque o texto vem dos **seus** dados, não do usuário. Sanitize antes.
</details>

**B9.** Acrescente **paginação** à programação: quatro itens por página, botões "anterior" e "próxima", indicação "Página 2 de 3" e volta automática à página 1 sempre que a busca ou o filtro mudarem.

Resultado esperado: a paginação respeita o resultado filtrado (não o array completo); os botões ficam desabilitados nos extremos; o foco vai para o topo da lista ao trocar de página.

<details><summary>Dica</summary>

Guarde `paginaAtual` no estado e use `lista.slice(inicio, inicio + POR_PAGINA)`. O total de páginas é `Math.ceil(lista.length / POR_PAGINA)` — e nunca deixe `paginaAtual` maior que ele depois de um filtro.
</details>

### Nível C — Desafio em sala

**C1.** Biblioteca de validação configurável. Escreva um `js/validador.js` genérico, dirigido por um objeto de regras, que funcione em qualquer formulário do seu projeto:

```js
const validador = criarValidador(form, {
  nome: { obrigatorio: true, min: 5, max: 80, tipo: "nomeCompleto" },
  email: { obrigatorio: true, tipo: "email" },
  cpf: { obrigatorio: true, tipo: "cpf" },
  nascimento: { obrigatorio: true, tipo: "data", idadeMinima: 16 },
});
```

Deve suportar regras predefinidas por tipo, regras personalizadas por função, mensagens customizadas, validação em `blur`/`input`/`submit`, exibição automática das mensagens e um método `validador.estaValido()`. Demonstre a mesma biblioteca funcionando em **três** formulários diferentes do seu projeto.

<details><summary>Dica</summary>

`criarValidador` devolve um objeto com métodos — é o padrão de módulo que você reencontrará no Nível 2. Guarde as regras em uma constante e percorra `Object.entries(regras)` para registrar os ouvintes. Cada tipo é uma entrada em um objeto `VALIDADORES_POR_TIPO`, o que evita uma cadeia gigante de `if`.
</details>

**C2.** Painel de consulta completo. Sobre a listagem principal do seu projeto autoral, implemente ao mesmo tempo: busca com `debounce` e normalização de acentos, dois filtros combináveis (categoria e faixa de valor ou data), ordenação por três critérios, paginação, contagem de resultados anunciada, estado vazio com sugestão útil e persistência da consulta no `localStorage` (ao recarregar, os filtros voltam como estavam).

<details><summary>Dica</summary>

Mantenha **um** objeto de estado (`const consulta = { termo: "", categoria: "todas", ordem: "nome", pagina: 1 }`) e uma função `aplicarConsulta()` que lê esse objeto, filtra, ordena, pagina e renderiza. Salvar e restaurar vira `JSON.stringify(consulta)` e `Object.assign(consulta, JSON.parse(bruto))`.
</details>

## 🏆 Desafios

### ⭐ O formulário que aceita qualquer coisa
Tags: formularios, javascript, bug, acessibilidade

O arquivo abaixo deveria validar uma inscrição, mas aceita `nome` vazio, e-mail sem arroba e CPF com uma letra no meio — e, quando reclama, ninguém que use leitor de tela fica sabendo. São **seis** defeitos: quatro de lógica e dois de acessibilidade. Encontre todos usando só o DevTools e o console, sem reescrever o arquivo do zero.

**`caca-ao-bug.html`**

```html
<form id="form" novalidate>
  <label for="nome">Nome</label>
  <input type="text" id="nome" name="nome">
  <span id="erro-nome"></span>

  <label for="email">E-mail</label>
  <input type="text" id="email" name="email">
  <span id="erro-email"></span>

  <button type="button" id="enviar">Enviar</button>
</form>
```

**`caca-ao-bug.js`**

```js
const form = document.querySelector("#form");

function validarNome(valor) {
  if (valor === "") return "Nome obrigatório";
  return "";
}

function validarEmail(valor) {
  if (/\w+@\w+/.test(valor)) return "";
  return "Inválido";
}

document.querySelector("#enviar").addEventListener("click", () => {
  const nome = document.querySelector("#nome").value;
  const email = document.querySelector("#email").value;

  document.querySelector("#erro-nome").style.color = "red";
  document.querySelector("#erro-nome").innerHTML = validarNome(nome);
  document.querySelector("#erro-email").innerHTML = validarEmail(email);

  if (validarNome(nome) == "" && validarEmail(email) == "") {
    form.submit();
  }
});
```

**Critérios de pronto**

- Um espaço em branco (`"   "`) no campo nome passa a ser rejeitado.
- `"ana@teste"` e `"ana @teste.br"` passam a ser rejeitados, e `"ana@teste.br"` continua sendo aceito.
- O envio passa pelo evento `submit` do formulário e funciona com <kbd>Enter</kbd> em qualquer campo.
- Cada mensagem é anunciada por leitor de tela e o campo com erro fica marcado com `aria-invalid`.
- As mensagens dizem o que fazer, não apenas "Inválido".
- Um comentário de uma linha acima de cada correção explica o defeito que ela resolve.

<details><summary>Pistas</summary>

1. Compare a regex de e-mail com a da seção 5.10: o que falta nas pontas dela? E o que `\w` deixa passar?
2. `valor === ""` e `valor.trim() === ""` não são a mesma pergunta.
3. Releia a Aula 13 sobre por que ouvir `click` no botão não é o mesmo que ouvir `submit` no formulário.
4. `innerHTML` para texto puro é desnecessário e arriscado; e cor não é mensagem. Volte à seção 7 e liste os cinco requisitos.
</details>

### ⭐⭐ Busca que ignora acentos, plurais e a ordem das palavras
Tags: javascript, investigacao, performance, dom

Digite "minicurso git" na busca da programação: nada aparece, porque nenhum título contém exatamente essa sequência. Digite "seguranças": também nada. Usuários não digitam do jeito que os seus dados foram escritos — e a sua busca não pode depender disso. Torne a busca **tolerante**: ela deve encontrar o item quando todas as palavras digitadas aparecerem no texto, em qualquer ordem, ignorando acentos, maiúsculas e o "s" final.

**Critérios de pronto**

- `"minicurso git"` encontra "Minicurso: Git e GitHub do zero ao primeiro pull request".
- `"git minicurso"` encontra o mesmo item (a ordem das palavras não importa).
- `"seguranças"` encontra "segurança em aplicações web".
- A tolerância está isolada em **uma** função pura, testada no console com pelo menos seis casos.
- A busca continua respondendo instantaneamente com 500 itens no array (meça com `console.time` antes e depois).

<details><summary>Pistas</summary>

1. Divida o termo digitado em palavras com `split(/\s+/)` e exija que **todas** passem: `palavras.every(...)`.
2. `String.prototype.normalize("NFD")` mais a faixa `̀-ͯ` resolvem os acentos; a seção 9.2 tem a receita.
3. Para o plural ingênuo, remova um `s` final de cada palavra antes de comparar — e documente em um comentário que essa é uma simplificação, não uma regra do português.
4. Normalizar o texto de cada item a cada tecla é desperdício. Faça isso **uma vez**, guardando o texto já normalizado em um campo do próprio objeto ao iniciar.
</details>

### ⭐⭐ Validação sem uma linha de `if`
Tags: javascript, refatoracao, formularios

O `validarCampo` da Mão na massa tem um `switch` com sete casos. Funciona, mas cada campo novo exige mexer nessa função — e, num formulário de vinte campos, ela vira um monstro. Existe uma alternativa que os frameworks usam: descrever as regras como **dados** e deixar uma função genérica aplicá-las. Refatore a validação da inscrição para esse modelo, sem perder nenhuma mensagem nem nenhum comportamento.

**Critérios de pronto**

- Existe um objeto `REGRAS` mapeando o `id` de cada campo para uma lista de validadores.
- `validarCampo(campo)` tem no máximo dez linhas e não cita nenhum campo pelo nome.
- Acrescentar um campo novo ao formulário exige alterar **apenas** o HTML e o objeto `REGRAS`.
- Todos os comportamentos do Como testar continuam funcionando, item por item.
- Um comentário no topo explica, em três linhas, a vantagem dessa organização.

<details><summary>Pistas</summary>

1. Um validador é uma função `(valor) => mensagem`. Uma lista deles pode ser percorrida com `find` para achar a primeira mensagem não vazia.
2. Regras que precisam de parâmetro (tamanho mínimo, idade mínima) viram funções que **devolvem** funções: `minimo(5)` devolve `(valor) => ...`.
3. O campo `termos` trabalha com `checked`, não com `value`. Padronize a entrada do validador (por exemplo, sempre o elemento) para não precisar de exceções.
4. Compare o resultado com o `criarValidador` do exercício C1: você acabou de construir metade dele.
</details>

### ⭐⭐⭐ O formulário mais acessível da turma
Tags: acessibilidade, formularios, investigacao, projeto

Um formulário pode passar em todos os testes automáticos e ainda ser impossível de preencher sem o mouse. Nesta missão você vai auditar o formulário do **seu projeto autoral** como um usuário que não enxerga a tela, corrigir o que encontrar e provar o resultado. Vale como item extra na rubrica da Avaliação 3.

**Critérios de pronto**

- Um vídeo de até três minutos preenchendo e enviando o formulário **só com o teclado**, com o monitor desligado ou os olhos fechados, usando o leitor de tela do sistema (NVDA no Windows, Orca no Linux, VoiceOver no macOS).
- O formulário tem um resumo de erros no topo, ligado por link a cada campo com problema, que recebe foco ao falhar o envio.
- Todo campo tem rótulo associado, texto de ajuda ligado por `aria-describedby` e mensagem por `role="alert"`.
- A aba **Lighthouse** do DevTools marca 100 em Acessibilidade na página do formulário, e a captura está no relatório.
- Um arquivo `acessibilidade.md` lista os problemas encontrados, a correção aplicada e — o item mais importante — **dois** problemas que o Lighthouse **não** apontou e que só a navegação por teclado revelou.

<details><summary>Pistas</summary>

1. Comece navegando só com <kbd>Tab</kbd>, <kbd>Shift</kbd>+<kbd>Tab</kbd>, <kbd>Espaço</kbd> e <kbd>Enter</kbd>. Anote todo momento em que você não soube onde estava.
2. O resumo de erros é uma `<div tabindex="-1">` com uma lista de links `href="#id-do-campo"`; ao falhar o envio, chame `.focus()` nela.
3. Ferramentas automáticas não detectam rótulo errado, ordem de foco ilógica nem mensagem que não diz o que fazer. É aí que estão os seus dois achados.
4. O leitor de tela do seu sistema já está instalado. No Windows, o Narrador abre com <kbd>Ctrl</kbd>+<kbd>Win</kbd>+<kbd>Enter</kbd>; no Linux, o Orca com <kbd>Super</kbd>+<kbd>Alt</kbd>+<kbd>S</kbd>.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| A página recarrega ao enviar e "os dados somem" | Falta `e.preventDefault()` no ouvinte de `submit` | Chame `e.preventDefault()` na primeira linha do ouvinte |
| `Uncaught TypeError: Cannot read properties of null (reading 'value')` | `querySelector` não achou o campo: `id` errado, ou o script roda antes do HTML | Confira o seletor com `$$("#id")` no console e use `defer` na tag `<script>` |
| O botão "Enviar" não faz nada, e <kbd>Enter</kbd> no campo envia sem validar | O ouvinte está no `click` do botão, não no `submit` do formulário | Ouça `submit` no `<form>`; o botão deve ser `type="submit"` |
| `idade + 1` resulta em `"251"` | `input.value` é sempre string, mesmo em `type="number"` | Converta com `Number(campo.value)` antes de qualquer conta |
| `"   "` passa na validação de campo obrigatório | Comparou `valor === ""` sem `trim()` | Use `valor.trim() === ""` |
| O formulário nunca envia, mesmo com tudo preenchido | `setCustomValidity("mensagem")` nunca foi limpo | Chame `campo.setCustomValidity("")` no início de cada validação |
| `pattern="/\d{5}/"` nunca casa | As barras da forma literal viraram caracteres a serem procurados | No atributo `pattern` não use barras; as âncoras `^` e `$` já são implícitas |
| `/\d{3}/.test("abc1234")` devolve `true` e aceita lixo | Regex sem âncoras verifica se o padrão existe **em algum lugar** | Ancore o padrão de validação: `/^\d{3}$/` |
| `Uncaught SyntaxError: Identifier 'els' has already been declared` | Dois scripts da mesma página declaram a mesma `const` no escopo global | Nomes diferentes por arquivo, ou um único script por página (módulos só no Nível 2) |
| `Uncaught ReferenceError: palestras is not defined` | `js/programacao.js` carregou antes de `js/dados.js` | Coloque `dados.js` antes na ordem das tags `<script defer>` |
| A lista some ao clicar em um filtro e volta errada depois | `sort()` reordenou o array original de dados | Ordene sempre uma cópia: `[...palestras].sort(...)` |
| Buscar "cafe" não encontra "Café" | Comparação direta entre strings com e sem acento | Normalize os dois lados com `normalize("NFD")` e a remoção dos combinantes |
| "Ávila" aparece depois de "Zampieri" na ordenação | `sort()` puro compara códigos de caractere | Use `a.nome.localeCompare(b.nome, "pt-BR")` |
| A página trava ao digitar na busca de uma lista grande | Filtro pesado executado a cada tecla | Envolva o ouvinte em `debounce(fn, 300)` |
| O layout "pula" toda vez que uma mensagem de erro aparece | O elemento da mensagem tem altura zero quando vazio | `min-height` no `.erro`, reservando o espaço da linha |
| O leitor de tela não anuncia o resultado da busca | A região `aria-live` foi criada junto com o conteúdo | Deixe o elemento vazio no HTML e só altere o `textContent` depois |
| `localStorage.getItem` devolve `[object Object]` | O objeto foi salvo sem `JSON.stringify` | `setItem(chave, JSON.stringify(obj))` e `JSON.parse` na leitura |

## 🏠 Atividade assíncrona (1 h)

**Parte 1 — Leitura (15 min).** FLANAGAN, *JavaScript: o guia definitivo*, capítulo de expressões regulares. MILETTO & BERTAGNOLLI, *Desenvolvimento de software II*, seção de validação de dados de entrada. Na MDN em português, o artigo "Validação de formulário no lado do cliente" (link em Para aprofundar). Anote duas restrições de validação nativa que não apareceram nesta aula.

**Parte 2 — Entrega (40 min).** No seu **projeto autoral**:

1. O formulário principal com validação completa em JavaScript: pelo menos seis campos, mensagens específicas por campo, **ao menos uma validação por expressão regular** e uma regra de negócio que a regex não resolve (dígito verificador, idade mínima, data no calendário ou confirmação de senha).
2. Mensagens acessíveis: `role="alert"`, `aria-invalid`, `aria-describedby`, indicação que não dependa só de cor e foco no primeiro campo inválido ao enviar.
3. A listagem principal do seu domínio com **busca** (com `debounce` e normalização de acentos), **um filtro** e **uma ordenação**, com contador anunciado e estado vazio tratado.
4. Os exercícios **B2** (medidor de força de senha) e **B7** (`gerarSlug`) em `exercicios/aula14/`.

**Critério de pronto:** enviar o formulário vazio destaca todos os campos com erro, leva o foco ao primeiro e não recarrega a página; digitar um termo sem acento encontra o item acentuado; o console fica limpo em todas as páginas.

**Parte 3 — Fórum (5 min).** No fórum "Regex que quebrou": traga uma expressão regular sua que falhou em um caso que você não tinha previsto, explique por que falhou e mostre a correção. Comente a de um colega apontando outro caso que a expressão dele ainda não cobre.

**Entrega:** commit + push e link do repositório (ou `.zip`) no SIGAA.

## ✅ Checkpoint do projeto

- [ ] Formulário principal com `novalidate`, um `<span class="erro" role="alert">` por campo e `id` no padrão `erro-<id-do-campo>`.
- [ ] Validadores escritos como funções puras (recebem valor, devolvem mensagem ou `""`), separados da exibição.
- [ ] Ao menos uma validação por expressão regular ancorada com `^` e `$`, e uma regra algorítmica que a regex não resolve.
- [ ] Validação no `blur`, revalidação no `input` depois do primeiro erro e validação completa no `submit`.
- [ ] Foco levado ao primeiro campo inválido, com rolagem até ele.
- [ ] `aria-invalid`, `aria-describedby` e indicação visual que não dependa só de cor em todos os campos.
- [ ] Máscara aplicada na digitação e removida antes de usar o valor.
- [ ] Rascunho no `localStorage` sem nenhum dado sensível, com `JSON.stringify`/`JSON.parse`.
- [ ] Listagem com busca (`debounce` + normalização de acentos), filtro e ordenação sobre uma **cópia** do array.
- [ ] Contador de resultados em região `aria-live` e mensagem de estado vazio com sugestão útil.
- [ ] Nenhum erro no console em nenhuma das cinco páginas.

## 📚 Para aprofundar

- MDN — **Validação de formulário no lado do cliente** (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Learn_web_development/Extensions/Forms/Form_validation> — o guia completo, com a Constraint Validation API passo a passo.
- MDN — **Expressões regulares** (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Guide/Regular_expressions> — leia "Classes de caracteres" e "Asserções"; é a referência definitiva.
- MDN — **`ValidityState`**: <https://developer.mozilla.org/pt-BR/docs/Web/API/ValidityState> — todas as propriedades do objeto `validity`, com o atributo HTML que dispara cada uma.
- MDN — **`FormData`**: <https://developer.mozilla.org/pt-BR/docs/Web/API/FormData> — inclusive `getAll`, para grupos de checkboxes.
- MDN — **`String.prototype.normalize`**: <https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Global_Objects/String/normalize> — as formas NFC e NFD explicadas com exemplos.
- MDN — **`Array.prototype.sort`**: <https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Global_Objects/Array/sort> — por que a função comparadora devolve número negativo, zero ou positivo.
- MDN — **`Window.localStorage`**: <https://developer.mozilla.org/pt-BR/docs/Web/API/Window/localStorage> — limites, eventos e o que nunca guardar ali.
- web.dev — **Learn Forms**: <https://web.dev/learn/forms> — os módulos de validação e de acessibilidade em formulários, com exemplos interativos.
- regex101: <https://regex101.com> — testa a expressão, explica token por token e mede o desempenho. Escolha o sabor ECMAScript (JavaScript).
- Regexr: <https://regexr.com> — alternativa com uma biblioteca de padrões prontos para comparar com os seus.
- FLANAGAN, David. *JavaScript: o guia definitivo*. Bookman, 2014 — capítulo de expressões regulares e de trabalho com formulários.
- STEFANOV, Stoyan. *Padrões JavaScript*. Novatec, 2010 — o padrão de módulo, base do exercício C1.
- MILETTO, Evandro M.; BERTAGNOLLI, Silvia C. *Desenvolvimento de software II*. Bookman, 2014 — validação de dados de entrada e tratamento de erros.
- TERUEL, Evandro C. *HTML 5 — Guia Prático*. Saraiva, 2014 — capítulo de formulários, para revisar os atributos que alimentam a Constraint Validation API.

Na próxima aula, o site sai da sua máquina e vai para a internet: você vai preparar o projeto para produção, versioná-lo com Git, publicá-lo no GitHub Pages, auditar o resultado com o Lighthouse e entregar a Avaliação 3 — o site do evento, no ar, com um endereço que qualquer pessoa pode acessar.
