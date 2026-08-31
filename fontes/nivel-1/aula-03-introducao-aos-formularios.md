# Aula 03 — Introdução aos formulários

> **Nível 1 — Introdução ao Desenvolvimento Web** · Unidade 1: Arquitetura da Web e HTML
> WebLab · UNEMAT — Campus Sinop
> **Tempo estimado:** 3 blocos de 50 min + 1 h de prática

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Explicar o que acontece entre o clique em "Enviar" e a chegada dos dados ao servidor, identificando cada par `nome=valor` na aba **Network** do DevTools.
- Decidir entre `GET` e `POST` justificando a escolha pelo tipo de operação, pelo tamanho dos dados e pelos riscos de cada método.
- Montar um `<form>` completo com `action`, `method` e os campos adequados a cada dado coletado.
- Escolher o `type` de `<input>` certo para cada informação e explicar o ganho prático de cada escolha, principalmente no celular.
- Associar rótulos a campos com `<label>` (por `for`/`id` e na forma envolvente) e agrupar campos relacionados com `<fieldset>`/`<legend>`.
- Usar `<select>`, `<optgroup>`, `<datalist>` e `<textarea>`, sabendo quando cada um é a escolha certa.
- Aplicar a validação nativa do HTML (`required`, `minlength`, `pattern`, `min`, `max`, `step`) e explicar por que ela **nunca** substitui a validação no servidor.

## 📋 Pré-requisitos

- [ ] Pasta `introducao-web/site-evento/` com as cinco páginas da Aula 02 (`index.html`, `programacao.html`, `inscricao.html`, `palestrantes.html`, `contato.html`), todas validadas no W3C.
- [ ] VS Code com Live Server e Prettier, e o navegador com DevTools (<kbd>F12</kbd>). Hoje você vai passar boa parte da aula na aba **Network**.
- [ ] Revisar da Aula 02: caminhos relativos, hierarquia de títulos, `<nav>` como lista e o hábito de validar cada página no W3C.
- [ ] Pasta `meu-projeto/` com o tema autoral definido e as páginas equivalentes já criadas.

Na aula passada você aprendeu a marcar conteúdo: textos, listas, links e tabelas, e construiu três das cinco páginas do site do evento com HTML semântico e validado. As páginas `inscricao.html` e `contato.html` ficaram só com o esqueleto, esperando esta aula. Hoje elas ganham o elemento que transforma um site em **sistema**: o formulário — a porta por onde os dados das pessoas entram no seu programa.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Por que formulários importam; o elemento `<form>`; GET × POST; os dados na aba Network |
| 2 | 50 min | `<input>` e seus tipos; atributos essenciais; `<label>`; `<select>`, `<datalist>`, `<textarea>`, radio e checkbox; `<fieldset>` |
| 3 | 50 min | Botões; validação nativa; checklist de acessibilidade; Mão na massa: a página de inscrição completa |

## 1. Por que formulários importam

### 1.1 A porta de entrada de todo sistema

Pense em qualquer sistema web que você usa: SIGAA, internet banking, loja on-line, rede social, portal da prefeitura. Todos têm uma coisa em comum — em algum momento **alguém digitou alguma coisa**. Login, matrícula, transferência, pedido, comentário, denúncia: tudo entra por um formulário.

Isso faz do formulário o elemento com maior consequência de todo o HTML. Uma tabela mal marcada deixa o site feio para um leitor de tela. Um formulário mal construído:

- **Gera dado sujo.** Um campo de telefone sem restrição recebe `(66) 9 9999-9999`, `66999999999`, `9999-9999` e `me liga no zap`. Quem sofre é o banco de dados, o relatório e a pessoa que vai tentar ligar.
- **Afasta usuários.** Cada campo desnecessário, cada teclado errado no celular, cada erro sem explicação é um motivo para desistir. Formulário longo demais é a principal causa de carrinho abandonado no comércio eletrônico.
- **Exclui pessoas.** Um campo sem `<label>` é, para quem usa leitor de tela, apenas "campo de edição, em branco". Sem rótulo, não há como saber o que digitar.
- **Cria retrabalho.** Todo dado que não foi validado na entrada vira, depois, uma planilha de correção manual.

Nesta aula você constrói a **estrutura**. Na Aula 04 fecha o ciclo com campos avançados e upload de arquivos. Na Aula 06 estiliza o formulário com CSS. Na Aula 14 acrescenta validação em JavaScript, com expressões regulares e mensagens acessíveis. O formulário de inscrição do evento vai atravessar a disciplina inteira.

### 1.2 O que acontece quando você clica em "Enviar"

Você já viu na Aula 01 o caminho de uma requisição HTTP. O formulário usa exatamente esse caminho, com um detalhe novo: ele **monta a requisição para você**.

```text
1. Você preenche os campos e clica no botão de envio.
2. O navegador percorre o formulário e monta uma lista de pares nome=valor,
   usando o atributo name de cada campo preenchido.
3. Se method="get": a lista vira a query string da URL (depois do ?).
   Se method="post": a lista vira o corpo (body) da requisição.
4. O navegador envia a requisição para o endereço do atributo action.
5. O servidor lê os pares, faz o que tem de fazer e devolve uma resposta.
6. O navegador exibe a resposta — normalmente uma página de confirmação.
```

Repare no passo 2: **é o `name` que vira a chave**. Não é o `id`, não é o texto do `<label>`, não é o `placeholder`. Um campo sem `name` simplesmente não existe do ponto de vista do servidor. Guarde isso; é o erro número um da lista de Erros comuns desta aula.

> **🧠 Você sabia?**
> Formulários existem na Web desde 1993 — são mais antigos que o CSS, que o JavaScript e que a maioria das pessoas que os usam. Eles apareceram no HTML 2.0 e praticamente não mudaram de sintaxe desde então: um `<form>` escrito em 1995 ainda funciona hoje, em qualquer navegador. Essa estabilidade tem um nome na Web: **compatibilidade retroativa**. É por isso que uma página antiga não "para de funcionar" — a plataforma quase nunca remove nada, ela só acrescenta. O preço dessa escolha é conviver com atributos estranhos como `enctype`, cujo nome só faz sentido quando você conhece a história. O benefício é que o que você aprende hoje continua valendo daqui a dez anos.

## 2. O elemento `<form>`

Todo formulário começa e termina no elemento `<form>`. Ele não desenha nada na tela: é o **envelope** que agrupa os campos, define para onde os dados vão e como viajam.

**`exemplos/form-minimo.html` (trecho)**

```html
<form action="/processa-cadastro" method="post">
  <label for="nome">Nome completo</label>
  <input type="text" id="nome" name="nome" required>

  <button type="submit">Enviar</button>
</form>
```

Três linhas de conteúdo, e já temos um sistema: um rótulo, um campo e um botão que dispara a requisição.

### 2.1 Atributos do `<form>`

| Atributo | Função |
|---|---|
| `action` | URL que vai receber os dados. Ausente ou vazio: a própria página |
| `method` | `get` (padrão) ou `post` |
| `enctype` | Como os dados são codificados; use `multipart/form-data` para upload (Aula 04) |
| `novalidate` | Desliga a validação nativa do navegador (útil ao testar validação em JS) |
| `autocomplete` | `on` (padrão) ou `off` — permite ou bloqueia o preenchimento automático |
| `target` | Onde exibir a resposta: `_self` (padrão) ou `_blank` (nova aba) |
| `name` | Nome do formulário; usado por JavaScript e por scripts antigos |

Nesta disciplina você ainda não tem um servidor para receber os dados — isso é assunto do Nível 2. Por enquanto, o `action` aponta para um endereço fictício (`/inscrever`), e o que interessa é **observar a requisição sendo montada** no DevTools. O servidor do Live Server vai responder `404 Not Found`, e está tudo bem: os dados foram enviados, e é isso que vamos inspecionar.

### 2.2 GET × POST

Essa é a decisão mais importante do `<form>` — e a que mais confunde quem está começando.

| Aspecto | GET | POST |
|---|---|---|
| Onde vão os dados | Na URL, como *query string* | No corpo da requisição |
| Visível na barra de endereço | Sim | Não |
| Limite prático de tamanho | Sim (cerca de 2.000 caracteres) | Praticamente ilimitado |
| Fica no histórico e nos favoritos | Sim | Não |
| Pode ser recarregado sem efeito colateral | Sim | Não (o navegador pergunta antes) |
| Uso típico | Busca, filtros, paginação | Cadastro, login, envio de dados |

A regra prática: **`GET` para ler, `POST` para alterar.**

Se a operação apenas consulta informação e poderia ser repetida cem vezes sem consequência, use `GET`. É por isso que a URL de uma busca é compartilhável: `programacao.html?dia=2&trilha=web` descreve exatamente o que você está vendo, e mandar esse link para um colega mostra a ele a mesma tela. Essa propriedade — repetir sem mudar nada — chama-se **idempotência**.

Se a operação **cria, altera ou apaga** alguma coisa, use `POST`. Uma inscrição feita duas vezes por engano vira duas inscrições. Por isso o navegador avisa antes de reenviar um `POST` quando você aperta <kbd>F5</kbd>.

**Como fica a URL de um `GET`.** Um formulário com `method="get"`, `action="busca.html"` e um campo `name="q"` preenchido com `html` leva o navegador para:

```text
busca.html?q=html
```

Com mais campos, os pares são separados por `&`:

```text
programacao.html?dia=2&trilha=web&ordem=horario
```

Caracteres especiais são codificados: um espaço vira `+` ou `%20`, o `@` vira `%40`, o acento de `programação` vira `programa%C3%A7%C3%A3o`. Esse processo é a **codificação de URL** (*percent-encoding*), e o navegador faz tudo sozinho.

> **⚠️ Atenção**
> **Nunca envie senha por `GET`.** Ela ficaria visível na barra de endereço, no histórico do navegador, no cache, nos registros (*logs*) do servidor e no cabeçalho `Referer` enviado a sites de terceiros. Já houve vazamento de milhões de senhas exatamente assim. Formulário de login é sempre `method="post"`.

> **🔎 Por baixo do capô**
> `POST` não é "seguro" no sentido de escondido: os dados vão no corpo da requisição, em texto puro, e qualquer pessoa com acesso à rede pode lê-los se a conexão for `http://`. O que protege de verdade é o **HTTPS**, que cifra a requisição inteira — URL, cabeçalhos e corpo. `POST` protege dos olhos de quem está do seu lado vendo a tela e do histórico do navegador; o HTTPS protege do resto do mundo. Você vai ver os detalhes do certificado e do cadeado na trilha Deploy; por ora, guarde a distinção entre **não aparecer na URL** e **estar cifrado**.

### 2.3 Vendo os dados viajarem

Este é o experimento central da aula. Faça com o professor, e depois refaça sozinho.

> **🔬 Investigue**
> Crie um arquivo `exemplos/get-vs-post.html` com dois formulários idênticos — um com `method="get"` e outro com `method="post"`, ambos com `action="recebe.html"` e dois campos (`name="usuario"` e `name="mensagem"`). Abra com o Live Server, abra o DevTools na aba **Network** e marque "Preserve log". Preencha e envie o primeiro: na lista de requisições aparece `recebe.html?usuario=maria&mensagem=oi` — os dados estão na própria URL, e você os vê também na barra de endereço. Agora envie o segundo: a URL fica limpa; clique na requisição, vá em **Payload** (ou **Requisição**, no Firefox) e veja `usuario: maria` e `mensagem: oi`. Repita o `POST` e aperte <kbd>F5</kbd>: o navegador pergunta se você quer reenviar os dados. Agora **apague o atributo `name`** de um dos campos e envie de novo: o campo some da requisição, mesmo estando preenchido na tela. Esse é o bug mais silencioso dos formulários.

### 2.4 Um formulário sem servidor ainda ensina

Enquanto não existe um back-end, três truques deixam o experimento útil:

1. **`action` vazio** (`action=""`): o formulário envia para a própria página. Com `method="get"`, os dados aparecem na URL e a página recarrega — ótimo para ver a *query string* sem erro 404.
2. **`action="recebe.html"`**: crie uma página simples de "recebido com sucesso". Com `GET`, ela abre com os dados na URL.
3. **Aba Network**: funciona sempre, mesmo com resposta `404`. A requisição saiu; é ela que interessa.

## 3. Campos de entrada: `<input>` e seus tipos

O `<input>` é o campo mais versátil do HTML. Ele não tem tag de fechamento (é um elemento **vazio**) e muda completamente de comportamento conforme o atributo `type`.

### 3.1 O catálogo de tipos

**`exemplos/tipos-de-input.html` (trecho do `<form>`)**

```html
<input type="text"           name="nome"        id="nome">
<input type="email"          name="email"       id="email">
<input type="password"       name="senha"       id="senha">
<input type="number"         name="idade"       id="idade" min="16" max="120" step="1">
<input type="tel"            name="telefone"    id="telefone">
<input type="url"            name="site"        id="site">
<input type="date"           name="nascimento"  id="nascimento">
<input type="time"           name="horario"     id="horario">
<input type="datetime-local" name="agendamento" id="agendamento">
<input type="month"          name="competencia" id="competencia">
<input type="week"           name="semana"      id="semana">
<input type="search"         name="busca"       id="busca">
<input type="color"          name="cor"         id="cor" value="#0b3d5c">
<input type="range"          name="nota"        id="nota" min="0" max="10" step="0.5">
<input type="file"           name="anexo"       id="anexo" accept=".pdf,.docx">
<input type="checkbox"       name="termos"      id="termos">
<input type="radio"          name="turno"       id="manha" value="manha">
<input type="hidden"         name="origem"      value="site">
```

Nenhum desses tipos exige uma linha de JavaScript. O navegador entrega calendário, seletor de cor, controle deslizante e validação de formato de graça.

| `type` | Ganho prático imediato |
|---|---|
| `email` | Teclado com `@` no celular e validação de formato |
| `tel` | Teclado numérico no celular (sem validar formato) |
| `number` | Setas de incremento e validação numérica com `min`, `max` e `step` |
| `date` | Seletor de calendário nativo, no idioma do sistema |
| `url` | Validação de endereço (exige o esquema, como `https://`) |
| `search` | Botão de limpar (×) e integração com o histórico de buscas |
| `color` | Seletor de cores do sistema operacional |
| `range` | Controle deslizante — bom para valores aproximados |
| `file` | Botão de escolher arquivo, filtrado por `accept` |
| `hidden` | Dado enviado sem aparecer na tela (origem, identificador, etapa) |

> **💡 Dica**
> Escolher o `type` certo não é detalhe estético: no celular, é ele que decide **qual teclado aparece**. Um campo de telefone com `type="text"` obriga a pessoa a trocar de teclado antes de digitar — uma fricção pequena que, multiplicada por milhares de usuários, vira abandono. Teste o seu formulário no celular pelo IP do Live Server na mesma rede Wi-Fi: é o teste mais barato de usabilidade que existe.

> **⚠️ Atenção**
> `type="number"` serve para **quantidades**, não para "sequências de dígitos". CPF, CEP, telefone, matrícula e número de cartão **não** são números: eles têm zeros à esquerda que importam, podem ter pontuação e nunca são somados. Em `type="number"`, o navegador remove zeros à esquerda, mostra setas de incremento sem sentido e permite notação como `1e5`. Para esses campos, use `type="text"` com `pattern` — e, a partir da Aula 04, com `inputmode="numeric"` para o teclado certo.

### 3.2 Atributos essenciais dos campos

```html
<label for="nome">Nome completo (obrigatório)</label>
<input type="text" id="nome" name="nome" value="Maria"
       placeholder="Ex.: Maria da Silva"
       required minlength="3" maxlength="80"
       autocomplete="name" autofocus>
```

| Atributo | O que faz |
|---|---|
| `id` | Liga o campo ao `<label for="…">`; precisa ser único na página |
| `name` | Chave enviada ao servidor; sem ele o campo não é enviado |
| `value` | Valor inicial, já preenchido e já enviável |
| `placeholder` | Dica dentro do campo; some ao digitar e **não** é enviada |
| `required` | Bloqueia o envio enquanto o campo estiver vazio |
| `minlength` / `maxlength` | Mínimo e máximo de caracteres |
| `autocomplete` | Diz ao navegador que dado é este, para preenchimento automático |
| `autofocus` | Coloca o foco neste campo ao abrir a página; use no máximo um por página |
| `readonly` | Não editável, **mas** é enviado |
| `disabled` | Não editável, **não** é enviado e sai da ordem do <kbd>Tab</kbd> |

Quatro pares que costumam ser confundidos:

- **`id` × `name`.** O `id` é para a página (ligar o `<label>`, servir de âncora, ser encontrado pelo JavaScript na Aula 13) e precisa ser **único** no documento. O `name` é para o servidor e **pode se repetir** — é assim que um grupo de caixas de seleção manda vários valores com a mesma chave.
- **`placeholder` × `value`.** O `placeholder` é um texto cinza que some quando você digita; ele **não é enviado**. O `value` é conteúdo de verdade: aparece preenchido e é enviado se não for alterado.
- **`readonly` × `disabled`.** Os dois impedem edição. `readonly` **envia** o valor; `disabled` **não envia** e também tira o campo da navegação por <kbd>Tab</kbd>. Se você precisa que um valor calculado chegue ao servidor, use `readonly` (ou um `hidden`), nunca `disabled`.
- **`minlength` × `min`.** `minlength` conta **caracteres** (texto); `min` compara **valores** (números e datas). Trocar um pelo outro é um erro clássico: `minlength="16"` em um campo de idade exige um número de dezesseis dígitos.

> **🔎 Por baixo do capô**
> O atributo `autocomplete` não é um simples liga/desliga. Ele tem um **vocabulário padronizado** de mais de cinquenta valores — `name`, `given-name`, `family-name`, `email`, `tel`, `street-address`, `postal-code`, `cc-number`, `one-time-code` — e é isso que permite ao navegador (e ao gerenciador de senhas do celular) preencher um cadastro inteiro em um toque. Preencher `autocomplete` corretamente é acessibilidade: consta na WCAG 2.1 como critério 1.3.5 ("identificar a finalidade da entrada"), justamente porque reduz a carga de digitação para pessoas com deficiência motora ou cognitiva. Um formulário com `autocomplete="off"` em tudo, "por segurança", só torna a vida mais difícil — e leva as pessoas a escolherem senhas piores.

## 4. `<label>` — obrigatório, não opcional

Todo campo precisa de um rótulo associado. Não é recomendação de estilo: é requisito de acessibilidade e de usabilidade — e o checklist de qualidade do Marco do projeto cobra isso.

### 4.1 As duas formas de associar

```html
<!-- Forma 1: atributo for apontando para o id do campo (preferida) -->
<label for="email">E-mail institucional</label>
<input type="email" id="email" name="email">

<!-- Forma 2: o <label> envolve o campo -->
<label>
  E-mail institucional
  <input type="email" name="email">
</label>
```

A **forma 1** é a preferida porque separa rótulo e campo no HTML — o que dá liberdade total ao CSS para colocá-los lado a lado, um acima do outro ou em colunas, sem lutar contra a estrutura. Ela também é a única que funciona quando o rótulo está em outra célula de uma tabela ou em outro contêiner.

A **forma 2** dispensa `id` e é útil em casos pequenos, especialmente caixas de seleção dentro de uma lista. Cuidado: se você usar as duas ao mesmo tempo (`<label for="x">` envolvendo o campo de `id="x"`), o `for` precisa apontar para esse mesmo campo, senão o validador acusa erro.

### 4.2 Por que o rótulo é obrigatório

1. **Acessibilidade.** Ao focar um campo, o leitor de tela anuncia o rótulo: "E-mail institucional, campo de edição". Sem `<label>`, a pessoa ouve apenas "campo de edição" e não tem como saber o que digitar.
2. **Usabilidade para todo mundo.** Clicar no rótulo foca o campo. Em uma caixa de seleção de 16 × 16 pixels, o rótulo multiplica por dez a área clicável — a diferença entre acertar e errar o toque no celular.
3. **Clareza permanente.** O rótulo continua visível depois que a pessoa digitou. O `placeholder`, não.

> **⚠️ Atenção**
> **`placeholder` não é `<label>`.** Ele desaparece assim que a pessoa começa a digitar (e quem se distraiu no meio do preenchimento não sabe mais o que aquele campo pedia), costuma ter contraste baixo demais para a WCAG, não é lido de forma confiável por todas as tecnologias assistivas e, em campos preenchidos automaticamente, some sem nunca ter sido lido. Use `placeholder` só para **exemplo de formato** ("Ex.: 78550-000") — e sempre além do rótulo, nunca no lugar dele.

### 4.3 Marcando campos obrigatórios

Marcar obrigatoriedade só com um asterisco vermelho falha duas vezes: quem não enxerga a cor não percebe, e quem usa leitor de tela ouve "asterisco". Faça assim:

```html
<label for="nome">Nome completo (obrigatório)</label>
<input type="text" id="nome" name="nome" required minlength="5" maxlength="100"
       autocomplete="name">
```

O texto "(obrigatório)" no rótulo é lido por todos. O atributo `required` faz o navegador barrar o envio e, de quebra, é anunciado pelos leitores de tela como "obrigatório". E, no rodapé do formulário, uma frase explicando a convenção resolve o resto: "Os campos marcados como obrigatórios precisam ser preenchidos".

## 5. Os outros campos

### 5.1 `<textarea>` — texto longo

```html
<label for="mensagem">Mensagem</label>
<textarea id="mensagem" name="mensagem" rows="6" cols="40"
          maxlength="500" placeholder="Escreva sua mensagem"></textarea>
```

- `rows` e `cols` definem o tamanho **inicial** em linhas e colunas de caractere; o CSS pode sobrescrever (Aula 06).
- `maxlength` limita os caracteres, exatamente como no `<input>`.

> **⚠️ Atenção**
> `<textarea>` **não usa o atributo `value`**: o conteúdo inicial vai entre as tags. E tudo que estiver ali dentro — inclusive espaços e quebras de linha de indentação — vira conteúdo do campo. Escreva sempre `<textarea></textarea>` colado quando o campo deve começar vazio. Um `<textarea>` "indentado bonitinho" nasce com espaços em branco dentro, e um `required` passa a aceitar um campo que parece vazio.

### 5.2 `<select>` — escolha em lista fechada

```html
<label for="curso">Curso</label>
<select id="curso" name="curso" required>
  <option value="">Selecione o seu curso</option>
  <optgroup label="Computação">
    <option value="si">Sistemas de Informação</option>
    <option value="ads">Análise e Desenvolvimento de Sistemas</option>
  </optgroup>
  <optgroup label="Engenharias">
    <option value="civil" selected>Engenharia Civil</option>
    <option value="agro">Engenharia Agronômica</option>
  </optgroup>
  <optgroup label="Outros">
    <option value="outro">Outro curso</option>
  </optgroup>
</select>
```

Pontos que fazem diferença:

- O `value` é o que vai para o servidor; o texto entre as tags é o que a pessoa lê. Quando o `value` é omitido, o próprio texto é enviado.
- A **primeira `<option>` com `value=""`** é o truque que faz `required` funcionar em um `<select>`: enquanto ela estiver escolhida, o campo é considerado vazio. Sem ela, o primeiro item já conta como resposta válida — e você recebe "Sistemas de Informação" de quem nunca olhou a lista.
- `<optgroup label="…">` agrupa opções. O `label` é obrigatório e é anunciado pelo leitor de tela.
- `selected` define a opção inicial. Use com parcimônia: uma resposta pré-marcada é uma resposta que muita gente vai deixar como está.

**Seleção múltipla:**

```html
<label for="linguagens">Linguagens que você já usou</label>
<select id="linguagens" name="linguagens" multiple size="4">
  <option value="html">HTML</option>
  <option value="css">CSS</option>
  <option value="js">JavaScript</option>
  <option value="python">Python</option>
  <option value="java">Java</option>
</select>
```

`multiple` permite escolher vários (com <kbd>Ctrl</kbd> ou <kbd>Shift</kbd>) e `size` define quantas opções ficam visíveis. Na prática, um `<select multiple>` é pouco descoberto pelos usuários: em telas de toque, quase ninguém adivinha como selecionar mais de um. Prefira caixas de seleção quando as opções forem poucas.

### 5.3 Radio e checkbox

```html
<fieldset>
  <legend>Turno de preferência</legend>

  <input type="radio" id="matutino" name="turno" value="matutino" checked>
  <label for="matutino">Matutino</label>

  <input type="radio" id="vespertino" name="turno" value="vespertino">
  <label for="vespertino">Vespertino</label>

  <input type="radio" id="noturno" name="turno" value="noturno">
  <label for="noturno">Noturno</label>
</fieldset>

<fieldset>
  <legend>Oficinas de interesse</legend>

  <input type="checkbox" id="of-git" name="oficinas" value="git">
  <label for="of-git">Git e GitHub do zero</label>

  <input type="checkbox" id="of-api" name="oficinas" value="api">
  <label for="of-api">Introdução a APIs REST</label>

  <input type="checkbox" id="of-acess" name="oficinas" value="acessibilidade">
  <label for="of-acess">Acessibilidade na prática</label>
</fieldset>
```

**A regra decisiva:** botões de rádio do mesmo grupo compartilham o **mesmo `name`** e têm `value` diferentes. É o `name` igual que faz um desmarcar o outro. Dar um `name` diferente para cada rádio é o erro mais comum da aula — e o sintoma é fácil de reconhecer: todos ficam marcáveis ao mesmo tempo.

Nas caixas de seleção, o `name` repetido tem outro efeito: o servidor recebe **uma lista** de valores sob a mesma chave (`oficinas=git&oficinas=api`).

| Aspecto | Radio | Checkbox |
|---|---|---|
| Escolha | Uma entre várias | Várias independentes, ou nenhuma |
| Atributo `name` | Igual em todo o grupo | Igual (lista) ou diferente (sim/não) |
| Dá para desmarcar clicando | Não | Sim |
| Valor enviado quando não marcado | Nada | Nada |

> **💡 Dica**
> Uma caixa de seleção **não marcada não é enviada** — o servidor não recebe `termos=false`, ele simplesmente não recebe `termos`. Se você precisa distinguir "respondeu não" de "não respondeu", use dois botões de rádio ("Sim" e "Não") em vez de uma caixa de seleção.

### 5.4 `<datalist>` — sugestão com digitação livre

```html
<label for="instituicao">Instituição de ensino</label>
<input type="text" id="instituicao" name="instituicao" list="instituicoes"
       autocomplete="organization">
<datalist id="instituicoes">
  <option value="UNEMAT — Campus Sinop"></option>
  <option value="UFMT — Campus Sinop"></option>
  <option value="IFMT — Campus Sorriso"></option>
  <option value="UNIC"></option>
  <option value="Outra instituição"></option>
</datalist>
```

O `<input>` aponta para o `<datalist>` pelo atributo `list`, que recebe o `id` da lista. À medida que a pessoa digita, o navegador filtra as sugestões — mas **qualquer valor fora da lista continua sendo aceito**. É a diferença essencial em relação ao `<select>`.

| Situação | Use |
|---|---|
| O conjunto de respostas válidas é fechado e conhecido | `<select>` |
| A lista é longa e a digitação acelera a busca, mas há exceções | `<input list>` + `<datalist>` |
| Você precisa garantir que o valor esteja na lista | `<select>` (e revalide no servidor) |
| Poucas opções (até cinco) e todas devem ficar visíveis | Botões de rádio |

### 5.5 `<fieldset>` e `<legend>` — agrupar é semântica

```html
<fieldset>
  <legend>Dados pessoais</legend>
  <!-- campos do grupo -->
</fieldset>
```

`<fieldset>` agrupa campos relacionados; `<legend>` (que precisa ser o **primeiro filho**) dá título ao grupo. Por padrão o navegador desenha uma borda em volta — na Aula 06 você troca isso por algo mais bonito.

O valor real está na acessibilidade: para um leitor de tela, a legenda é anunciada **junto com cada campo do grupo**. Sem `<fieldset>`, três botões de rádio rotulados "Matutino", "Vespertino" e "Noturno" são apenas três opções soltas; com ele, viram "Turno de preferência, Matutino, botão de opção, 1 de 3". É o que torna um grupo de rádios compreensível sem visão.

Use `<fieldset>` sempre em grupos de rádio e de caixas de seleção, e em blocos temáticos de formulários longos (dados pessoais, endereço, pagamento). Não use para envolver um campo só.

## 6. Botões

```html
<button type="submit">Enviar inscrição</button>
<button type="reset">Limpar formulário</button>
<button type="button">Calcular total</button>
```

| `type` | O que faz |
|---|---|
| `submit` | Valida e envia o formulário. É o padrão dentro de um `<form>` |
| `reset` | Devolve todos os campos aos valores iniciais |
| `button` | Não faz nada sozinho; existe para receber uma ação em JavaScript (Aula 13) |

> **⚠️ Atenção**
> Dentro de um `<form>`, um `<button>` **sem `type` age como `submit`**. Isso causa envios acidentais em botões criados para outra finalidade ("mostrar mais", "adicionar linha", "calcular"). Declare sempre o `type` — é uma linha que evita um bug difícil de perceber, porque a página parece só "recarregar sozinha".

**`<button>` ou `<input type="submit">`?** Os dois enviam. Prefira `<button>`: ele aceita conteúdo HTML dentro (um ícone SVG ao lado do texto, por exemplo), enquanto o `<input>` só aceita o texto do atributo `value`. E nunca use uma imagem com um manipulador de clique no lugar de um botão: `<img onclick="enviar()">` não é focável pelo teclado, não é anunciado como botão e não funciona com <kbd>Enter</kbd>.

**Evite `type="reset"`.** Ele fica ao lado do botão de envio, tem o mesmo tamanho e apaga meia hora de preenchimento com um clique errado. Praticamente nenhum formulário profissional oferece "Limpar" hoje. Se você incluir um, coloque-o longe do botão principal e com aparência secundária.

## 7. Validação nativa do HTML

O navegador valida os campos **antes** de enviar, sem uma linha de JavaScript. Você só precisa declarar as regras.

**`exemplos/validacao-nativa.html` (trecho)**

```html
<form action="/cadastrar" method="post">
  <label for="v-nome">Nome completo (obrigatório)</label>
  <input type="text" id="v-nome" name="nome" required minlength="5" maxlength="100"
         autocomplete="name">

  <label for="v-email">E-mail (obrigatório)</label>
  <input type="email" id="v-email" name="email" required autocomplete="email">

  <label for="v-idade">Idade</label>
  <input type="number" id="v-idade" name="idade" min="16" max="120" step="1">

  <label for="v-cep">CEP</label>
  <input type="text" id="v-cep" name="cep"
         pattern="[0-9]{5}-[0-9]{3}"
         placeholder="Ex.: 78550-000"
         title="Use o formato 00000-000, com o hífen"
         autocomplete="postal-code">

  <label for="v-senha">Senha (obrigatório)</label>
  <input type="password" id="v-senha" name="senha" required
         minlength="8"
         autocomplete="new-password">

  <button type="submit">Cadastrar</button>
</form>
```

### 7.1 Os atributos de validação

| Atributo | O que valida |
|---|---|
| `required` | O campo não pode ficar vazio |
| `minlength` / `maxlength` | Quantidade mínima e máxima de caracteres |
| `min` / `max` | Valor mínimo e máximo (números, datas e horas) |
| `step` | Incremento permitido (`step="0.5"`, `step="any"`) |
| `type` | O formato inerente do tipo (`email`, `url`, `number`, `date`) |
| `pattern` | Uma expressão regular que o valor precisa satisfazer |
| `title` | Texto exibido junto da mensagem quando o `pattern` falha |

### 7.2 `pattern` e `title` andam juntos

`pattern` recebe uma **expressão regular** — um assunto que a Aula 14 aprofunda. Por enquanto, três padrões resolvem quase tudo:

```html
<!-- CEP: cinco dígitos, hífen, três dígitos -->
<input type="text" name="cep" pattern="[0-9]{5}-[0-9]{3}"
       title="Use o formato 00000-000, com o hífen">

<!-- CPF: 000.000.000-00 -->
<input type="text" name="cpf" pattern="[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}"
       title="Use o formato 000.000.000-00, com pontos e hífen">

<!-- Matrícula: exatamente oito dígitos -->
<input type="text" name="matricula" pattern="[0-9]{8}"
       title="A matrícula tem 8 dígitos, sem pontos ou traços">
```

Como ler `[0-9]{5}-[0-9]{3}`: "um dígito de 0 a 9, repetido cinco vezes; depois um hífen; depois um dígito repetido três vezes". O ponto precisa de barra invertida (`\.`) porque, sozinho, `.` significa "qualquer caractere".

Sem `title`, o navegador mostra uma mensagem inútil como **"Corresponda ao formato solicitado."** — a pessoa fica sabendo que errou, mas não o que fazer. Com `title`, a mensagem inclui o seu texto. **`pattern` sem `title` é considerado formulário incompleto neste material.**

### 7.3 As mensagens são do navegador

Quando a validação falha, quem escreve a mensagem é o navegador, no idioma do sistema operacional:

```text
Preencha este campo.
Inclua um "@" no endereço de e-mail.
O valor precisa ser maior ou igual a 16.
Aumente o texto para 5 caracteres ou mais.
Selecione um item na lista.
```

Você **não controla** esse texto no HTML puro (na Aula 14 vai controlar, com a Constraint Validation API do JavaScript). O que você controla é o `title` do `pattern` e, principalmente, o rótulo: um campo bem rotulado gera menos erro do que qualquer mensagem bem escrita.

> **📌 Vale gravar**
> Três perguntas voltam sempre: (1) o que acontece com um campo sem `name` ao enviar — ele não é enviado; (2) por que os rádios de um grupo precisam do mesmo `name` — é o que os torna mutuamente exclusivos; (3) a validação nativa garante que o dado chega correto ao servidor? **Não.** Ela é conveniência para o usuário, não segurança.

### 7.4 Validação no cliente não é segurança

> **⚠️ Atenção**
> Toda a validação desta seção pode ser desligada em cinco segundos: basta abrir o DevTools e apagar o atributo `required`, ou acrescentar `novalidate` ao `<form>`, ou enviar a requisição por fora do navegador com uma ferramenta de linha de comando. **Validação no cliente é usabilidade; validação no servidor é segurança.** O servidor precisa revalidar absolutamente tudo — e isso vale para o resto da sua carreira, não só para esta disciplina. Você vai implementar essa segunda camada no Nível 2, com Express.

O atributo `novalidate` no `<form>` desliga a validação nativa da página inteira. Ele parece um tiro no pé, mas tem uso legítimo: quando o formulário passa a ter validação em JavaScript, com mensagens próprias e acessíveis, você desliga a nativa para não ter duas mensagens competindo. É exatamente o que a Aula 14 faz.

## 8. Acessibilidade em formulários — checklist

Passe esta lista em todo formulário que você entregar nesta disciplina. Ela também é a base do desafio ⭐⭐ de hoje.

- [ ] Todo campo tem `<label>` associado por `for`/`id` (ou envolvente). Nenhum rótulo é só `placeholder`.
- [ ] Grupos de rádio e de caixas de seleção estão dentro de `<fieldset>` com `<legend>`.
- [ ] A obrigatoriedade está no **texto** do rótulo, não apenas em uma cor ou em um asterisco.
- [ ] A ordem de tabulação é a ordem visual: siga a ordem do HTML e não use `tabindex` positivo.
- [ ] O foco é visível em todos os campos e botões (não remova o contorno sem colocar outro indicador).
- [ ] `autocomplete` está preenchido com o valor semântico correto (`name`, `email`, `tel`, `postal-code`, `organization`, `bday`).
- [ ] Cada `<input type="file">` diz, no rótulo, os formatos e o tamanho aceitos.
- [ ] O formulário inteiro é utilizável **só com o teclado**: <kbd>Tab</kbd> para avançar, <kbd>Espaço</kbd> para marcar, <kbd>Enter</kbd> para enviar.
- [ ] Não há campo pedindo informação que você não vai usar. O campo mais acessível é o que não existe.

> **🔬 Investigue**
> Abra qualquer formulário que você já tenha escrito e **guarde o mouse**. Navegue só com <kbd>Tab</kbd>, <kbd>Shift</kbd>+<kbd>Tab</kbd>, setas (nos rádios) e <kbd>Espaço</kbd>. Anote: você sempre sabe onde está o foco? A ordem faz sentido? Consegue marcar todas as opções? Consegue enviar com <kbd>Enter</kbd>? Depois repita clicando **no texto de cada rótulo**: se o campo correspondente não recebe o foco, aquele `<label>` não está associado — e o problema é `for` sem `id` correspondente, ou `id` duplicado na página.

## 💻 Mão na massa — a página de inscrição da Semana Acadêmica

A `inscricao.html` que você criou na Aula 02 tem apenas a frase "O formulário de inscrição será construído na próxima aula". Chegou a hora. Ao final destes passos, a página terá um formulário de inscrição completo, acessível e validado, com quatro grupos de campos.

Trabalhe em `introducao-web/site-evento/inscricao.html`.

### Passo 1 — Cabeçalho, `<head>` e o esqueleto do `<main>`

Abra `inscricao.html` e substitua o conteúdo inteiro por este esqueleto. O `<head>`, o `<header>` e o `<footer>` são os mesmos das outras páginas — só mudam `<title>` e `description`.

**`site-evento/inscricao.html`**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Formulário de inscrição na Semana Acadêmica de Sistemas de Informação da UNEMAT Sinop: dados pessoais, acadêmicos e escolha de oficinas.">
  <meta name="author" content="Curso de Sistemas de Informação — UNEMAT Sinop">
  <title>Inscrição — Semana Acadêmica de Sistemas de Informação</title>
</head>
<body>
  <header id="topo">
    <h1>Semana Acadêmica de Sistemas de Informação</h1>
    <p>UNEMAT Sinop · três noites de outubro · Auditório Central</p>
    <nav>
      <ul>
        <li><a href="index.html">Início</a></li>
        <li><a href="programacao.html">Programação</a></li>
        <li><a href="inscricao.html">Inscrição</a></li>
        <li><a href="palestrantes.html">Palestrantes</a></li>
        <li><a href="contato.html">Contato</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <h2>Inscrição</h2>
    <p>
      A inscrição é gratuita e dá direito a certificado de 20 horas para quem
      participar de pelo menos 75% das atividades. As oficinas têm vagas
      limitadas e são preenchidas por ordem de inscrição.
    </p>
    <p>Os campos marcados como <strong>obrigatório</strong> precisam ser preenchidos.</p>
  </main>

  <footer>
    <p>Realização: Curso de Sistemas de Informação — UNEMAT, Campus Sinop.</p>
    <p>
      <a href="mailto:semana.si@unemat.br">semana.si@unemat.br</a> ·
      <a href="tel:+556635111000">(66) 3511-1000</a>
    </p>
    <p>&copy; Curso de Sistemas de Informação &mdash; UNEMAT Sinop. Todos os direitos reservados.</p>
  </footer>
</body>
</html>
```

Salve e confira no Live Server: a página abre com o mesmo cabeçalho das outras e o menu continua funcionando.

### Passo 2 — Abrir o `<form>`

Dentro do `<main>`, logo depois do parágrafo sobre os campos obrigatórios, abra o formulário:

**`site-evento/inscricao.html` (trecho: início do `<form>`)**

```html
    <form action="/inscrever" method="post" id="form-inscricao">
      <input type="hidden" name="origem" value="site-evento">
```

Três decisões, cada uma com um motivo:

- **`method="post"`**: a inscrição **cria** um registro. Não é uma consulta, não deve ficar no histórico e não pode ser repetida por engano com <kbd>F5</kbd>.
- **`action="/inscrever"`**: o endereço que vai receber os dados. Ele ainda não existe — o Live Server vai responder `404`, e nós vamos observar a requisição na aba Network mesmo assim.
- **`<input type="hidden" name="origem">`**: um dado que a pessoa não digita, mas que o servidor precisa. Aqui, de onde veio a inscrição — útil quando o mesmo endereço também recebe inscrições feitas no balcão do credenciamento.

### Passo 3 — Grupo 1: dados pessoais

**`site-evento/inscricao.html` (trecho: primeiro `<fieldset>`)**

```html
      <fieldset>
        <legend>Dados pessoais</legend>

        <p>
          <label for="nome">Nome completo (obrigatório)</label>
          <input type="text" id="nome" name="nome" required
                 minlength="5" maxlength="100"
                 placeholder="Ex.: Maria Aparecida da Silva"
                 autocomplete="name">
        </p>

        <p>
          <label for="cpf">CPF (obrigatório)</label>
          <input type="text" id="cpf" name="cpf" required
                 pattern="[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}"
                 placeholder="Ex.: 000.000.000-00"
                 title="Use o formato 000.000.000-00, com pontos e hífen">
        </p>

        <p>
          <label for="nascimento">Data de nascimento</label>
          <input type="date" id="nascimento" name="nascimento"
                 min="1930-01-01" autocomplete="bday">
        </p>

        <p>
          <label for="email">E-mail (obrigatório)</label>
          <input type="email" id="email" name="email" required
                 placeholder="Ex.: maria@exemplo.br"
                 autocomplete="email">
        </p>

        <p>
          <label for="telefone">Telefone com DDD</label>
          <input type="tel" id="telefone" name="telefone"
                 placeholder="Ex.: (66) 99999-0000"
                 autocomplete="tel">
        </p>
      </fieldset>
```

Cada par rótulo + campo está dentro de um `<p>`. Isso não é decoração: sem CSS, elementos de formulário são todos `inline` e ficariam todos na mesma linha, um grudado no outro. O `<p>` dá a quebra e o espaçamento mínimos até a Aula 06 assumir o controle.

Repare no `type="date"` com `min="1930-01-01"`: o formato do atributo é sempre `AAAA-MM-DD`, independentemente de como o navegador **mostra** a data para o usuário (no Brasil, `DD/MM/AAAA`). Essa separação entre formato de máquina e formato humano é a mesma do atributo `datetime` que você usou nas tabelas da Aula 02.

### Passo 4 — Grupo 2: dados acadêmicos

**`site-evento/inscricao.html` (trecho: segundo `<fieldset>`)**

```html
      <fieldset>
        <legend>Dados acadêmicos</legend>

        <p>
          <label for="instituicao">Instituição de ensino</label>
          <input type="text" id="instituicao" name="instituicao"
                 list="instituicoes"
                 placeholder="Comece a digitar para ver sugestões"
                 autocomplete="organization">
          <datalist id="instituicoes">
            <option value="UNEMAT — Campus Sinop"></option>
            <option value="UFMT — Campus Sinop"></option>
            <option value="IFMT — Campus Sorriso"></option>
            <option value="UNIC — Sinop"></option>
            <option value="Escola de ensino médio"></option>
          </datalist>
        </p>

        <p>
          <label for="curso">Curso (obrigatório)</label>
          <select id="curso" name="curso" required>
            <option value="">Selecione o seu curso</option>
            <optgroup label="Computação">
              <option value="si">Sistemas de Informação</option>
              <option value="ads">Análise e Desenvolvimento de Sistemas</option>
              <option value="cc">Ciência da Computação</option>
            </optgroup>
            <optgroup label="Engenharias">
              <option value="civil">Engenharia Civil</option>
              <option value="agro">Engenharia Agronômica</option>
            </optgroup>
            <optgroup label="Outros">
              <option value="outro">Outro curso</option>
              <option value="nenhum">Ainda não estou na graduação</option>
            </optgroup>
          </select>
        </p>

        <p>
          <label for="fase">Fase ou semestre</label>
          <input type="number" id="fase" name="fase" min="1" max="8" step="1"
                 placeholder="Ex.: 3">
        </p>

        <p>
          <label for="matricula">Matrícula</label>
          <input type="text" id="matricula" name="matricula"
                 pattern="[0-9]{8}"
                 placeholder="Ex.: 20240001"
                 title="A matrícula tem 8 dígitos, sem pontos ou traços">
        </p>
      </fieldset>
```

Compare de propósito os dois campos de escolha deste grupo:

- **Instituição** é um `<input list>` com `<datalist>`: as cinco instituições da região cobrem quase todos os casos, mas alguém de fora precisa poder digitar a sua.
- **Curso** é um `<select>` com `<optgroup>`: o conjunto é fechado, existe a opção "Outro curso" e a primeira `<option>` tem `value=""` para que o `required` funcione de verdade.

### Passo 5 — Grupo 3: participação

**`site-evento/inscricao.html` (trecho: terceiro `<fieldset>`)**

```html
      <fieldset>
        <legend>Participação</legend>

        <fieldset>
          <legend>Turno de preferência (obrigatório)</legend>

          <input type="radio" id="turno-matutino" name="turno" value="matutino" required>
          <label for="turno-matutino">Matutino</label>

          <input type="radio" id="turno-vespertino" name="turno" value="vespertino">
          <label for="turno-vespertino">Vespertino</label>

          <input type="radio" id="turno-noturno" name="turno" value="noturno">
          <label for="turno-noturno">Noturno</label>
        </fieldset>

        <fieldset>
          <legend>Oficinas de interesse</legend>

          <input type="checkbox" id="of-git" name="oficinas" value="git">
          <label for="of-git">Git e GitHub do zero (dia 1, 40 vagas)</label>
          <br>

          <input type="checkbox" id="of-html" name="oficinas" value="html-css">
          <label for="of-html">Do zero ao primeiro site com HTML e CSS (dia 2, 30 vagas)</label>
          <br>

          <input type="checkbox" id="of-api" name="oficinas" value="api-rest">
          <label for="of-api">Introdução a APIs REST (dia 2, 30 vagas)</label>
          <br>

          <input type="checkbox" id="of-acessibilidade" name="oficinas" value="acessibilidade">
          <label for="of-acessibilidade">Acessibilidade na prática (dia 3, 25 vagas)</label>
        </fieldset>

        <p>
          <label for="camiseta">Tamanho da camiseta</label>
          <select id="camiseta" name="camiseta">
            <option value="">Não quero camiseta</option>
            <option value="p">P</option>
            <option value="m">M</option>
            <option value="g">G</option>
            <option value="gg">GG</option>
          </select>
        </p>
      </fieldset>
```

Dois detalhes que valem nota:

- **`required` em um grupo de rádios** só precisa aparecer **uma vez**, em qualquer um dos botões do grupo. O navegador entende que o grupo inteiro é obrigatório, porque todos compartilham o mesmo `name`.
- **`<fieldset>` dentro de `<fieldset>`** é válido e é a marcação correta aqui: "Participação" é o bloco temático, e dentro dele há dois grupos de escolha que precisam, cada um, da sua própria legenda.

Os `<br>` entre as caixas de seleção são um paliativo até a Aula 06: sem CSS, todas ficariam na mesma linha. Não use `<br>` para espaçamento em conteúdo normal — aqui ele marca uma quebra real entre opções de uma escolha.

### Passo 6 — Grupo 4: informações complementares

**`site-evento/inscricao.html` (trecho: quarto `<fieldset>`)**

```html
      <fieldset>
        <legend>Informações complementares</legend>

        <p>
          <label for="acessibilidade">Você precisa de algum recurso de acessibilidade?</label>
          <textarea id="acessibilidade" name="acessibilidade" rows="4" cols="50"
                    maxlength="500"
                    placeholder="Ex.: intérprete de Libras, lugar reservado, material ampliado"></textarea>
        </p>

        <p>
          <label for="restricao">Restrição alimentar (para o coffee break)</label>
          <input type="text" id="restricao" name="restricao" maxlength="120"
                 placeholder="Ex.: sem lactose">
        </p>

        <p>
          <label for="como-soube">Como você ficou sabendo do evento?</label>
          <select id="como-soube" name="como_soube">
            <option value="">Prefiro não responder</option>
            <option value="professor">Um professor divulgou em aula</option>
            <option value="redes">Redes sociais do curso</option>
            <option value="colega">Um colega me contou</option>
            <option value="cartaz">Cartaz no campus</option>
          </select>
        </p>

        <p>
          <input type="checkbox" id="termos" name="termos" value="aceito" required>
          <label for="termos">
            Li e aceito o regulamento do evento e autorizo o uso da minha imagem
            nas fotos de divulgação (obrigatório).
          </label>
        </p>

        <p>
          <button type="submit">Enviar inscrição</button>
        </p>
      </fieldset>
    </form>
```

O aceite dos termos é uma caixa de seleção com `required`: o formulário não é enviado enquanto ela não for marcada. Repare que o rótulo vem **depois** do campo — a convenção para caixas de seleção e rádios é rótulo à direita, ao contrário dos campos de texto.

O campo `name="como_soube"` usa sublinhado em vez de hífen. Não é obrigatório, mas é hábito: chaves com hífen dão trabalho em algumas linguagens do lado do servidor, onde `dados.como-soube` seria interpretado como uma subtração.

### Passo 7 — Fechar a página

Depois do `</form>`, antes de fechar o `<main>`, acrescente o link de volta ao topo, como nas outras páginas:

**`site-evento/inscricao.html` (trecho: fim do `<main>`)**

```html
      <p><a href="#topo">Voltar ao topo</a></p>
    </main>
```

### Passo 8 — Testar a validação nativa

1. Abra `inscricao.html` no Live Server.
2. Clique direto em **Enviar inscrição**, com tudo vazio. O navegador rola até o primeiro campo inválido, coloca o foco nele e mostra **"Preencha este campo."**.
3. Preencha o nome com três letras: **"Aumente o texto para 5 caracteres ou mais."**
4. Digite `maria.exemplo.br` no e-mail: **"Inclua um '@' no endereço de e-mail."**
5. Digite `12345678900` no CPF: a mensagem traz o seu `title` — "Use o formato 000.000.000-00, com pontos e hífen".
6. Coloque `12` na fase: **"O valor precisa ser menor ou igual a 8."**
7. Deixe o curso em "Selecione o seu curso": **"Selecione um item na lista."**
8. Não marque nenhum turno: **"Selecione uma dessas opções."**

Cada mensagem veio de um atributo diferente. Volte ao HTML e identifique qual.

### Passo 9 — Ver os dados na aba Network

1. Abra o DevTools (<kbd>F12</kbd>), vá à aba **Network** e marque **Preserve log**.
2. Preencha o formulário inteiro, marcando **duas** oficinas.
3. Envie. Vai aparecer uma requisição `inscrever` com status `404` — esperado, porque não existe servidor nesse endereço.
4. Clique nela e abra **Payload** (Chrome) ou **Requisição** (Firefox). Confira: cada campo aparece com o seu `name`; `oficinas` aparece **duas vezes**, uma para cada caixa marcada; `origem` aparece com `site-evento`, mesmo você nunca tendo digitado nada; a camiseta, se você deixou "Não quero camiseta", aparece com valor vazio.
5. Agora troque `method="post"` por `method="get"`, recarregue e envie de novo. Os mesmos dados aparecem na **URL**, separados por `&`. Repare na codificação: o espaço do nome virou `+`, o `@` do e-mail virou `%40` e os parênteses do telefone viraram `%28` e `%29`.
6. Volte para `method="post"`. Inscrição não é consulta.

### Passo 10 — Validar no W3C

Abra <https://validator.w3.org/#validate_by_input>, cole a página inteira e corrija até ver **"No errors or warnings to show"**. Os erros mais prováveis aqui são:

- `Duplicate ID` — dois campos com o mesmo `id` (fácil de acontecer copiando e colando um `<p>`).
- `The for attribute of the label element must refer to a non-hidden form control` — um `for` apontando para um `id` que você renomeou depois.
- `Element optgroup is missing required attribute label` — um `<optgroup>` sem `label`.

### Como testar

- A página abre no Live Server com o mesmo cabeçalho e rodapé das outras quatro.
- Enviar o formulário vazio mostra a mensagem do navegador no primeiro campo obrigatório, sem sair da página.
- Clicar no **texto** de cada rótulo coloca o foco (ou marca a opção) no campo correspondente — teste em todos, inclusive nos rádios e nas caixas de seleção.
- Marcar um turno desmarca automaticamente o anterior; marcar duas oficinas mantém as duas marcadas.
- Só com o teclado, você consegue percorrer o formulário inteiro na ordem visual e enviar com <kbd>Enter</kbd>.
- Na aba Network, a requisição `POST` traz um par `nome=valor` para cada campo preenchido — inclusive o `hidden`.
- O validador do W3C não acusa nenhum erro.

**Resultado esperado:** uma página de inscrição feia e completamente funcional, com quatro blocos de campos, mais de vinte controles, validação nativa em mais de dez deles e zero erros no W3C. A aparência é assunto da Unidade 2; hoje o que importa é que o dado sai certo.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Qual `type` de `<input>` é o mais adequado para cada dado, e por quê: (a) CPF; (b) data de nascimento; (c) senha; (d) avaliação de 0 a 10 com controle deslizante; (e) upload de currículo; (f) cor favorita; (g) e-mail; (h) site pessoal?

**A2.** Cite três diferenças entre `GET` e `POST` e dê um exemplo de formulário real para cada método.

**A3.** Por que `placeholder` não substitui `<label>`? Dê três motivos diferentes.

**A4.** Qual é a diferença prática entre `readonly` e `disabled`? Em qual situação a escolha errada faz um dado desaparecer do servidor?

**A5.** O que acontece com um campo preenchido que **não** tem o atributo `name` quando o formulário é enviado? Como você comprovaria isso em 30 segundos?

**A6.** Escreva um grupo de três botões de rádio para escolha de turno, com `<fieldset>`, `<legend>` e `<label>` corretos, e com o grupo marcado como obrigatório.

**A7.** Por que os botões de rádio de um grupo precisam ter o mesmo `name`? O que acontece na tela se cada um tiver um `name` diferente?

**A8.** O que faz o atributo `required`? Ele garante que o dado chegará preenchido ao servidor? Justifique em duas frases.

**A9.** Escreva um `<select>` de estados do Centro-Oeste com um `<optgroup>` chamado "Centro-Oeste" contendo MT, MS, GO e DF, e uma primeira opção que faça o `required` funcionar.

**A10.** Qual é a diferença entre `<select>` e `<datalist>`? Dê um exemplo de dado do site do evento em que cada um seria a escolha certa.

**A11.** Explique o que este `pattern` aceita, caractere por caractere: `[0-9]{2}/[0-9]{2}/[0-9]{4}`. Escreva um `title` adequado para ele.

**A12.** Um `<button>` sem atributo `type` dentro de um `<form>`: o que ele faz ao ser clicado? Que bug isso costuma causar?

### Nível B — Aplicação

**B1.** Construa `exercicios/aula03/login.html`: um formulário de login com e-mail, senha (mínimo 8 caracteres), caixa de seleção "manter conectado", botão "Entrar" e um link "Esqueci minha senha". Todos os campos com `<label>`, `autocomplete` correto (`email` e `current-password`) e validação nativa. O método precisa ser `post`.

Resultado esperado: enviar com os campos vazios mostra a mensagem do navegador no e-mail; digitar uma senha de 5 caracteres mostra a mensagem de tamanho mínimo; clicar no texto "Manter conectado" marca a caixa; a aba Network mostra a senha no corpo da requisição, e nunca na URL.

<details markdown="1"><summary>Dica</summary>

O `autocomplete` de senha tem dois valores diferentes: `current-password` em telas de login e `new-password` em cadastro e troca de senha. Usar o valor certo é o que faz o gerenciador de senhas do celular oferecer a senha salva em vez de sugerir uma nova.
</details>

**B2.** Construa `exercicios/aula03/matricula.html`: um formulário de matrícula em disciplinas com dados do aluno (nome, matrícula, curso), seleção múltipla de disciplinas (caixas de seleção, no mínimo seis opções, com a carga horária no texto do rótulo), turno preferencial (rádios), observações (`<textarea>` de 500 caracteres) e aceite do regulamento (obrigatório). Use um `<fieldset>` por grupo.

Resultado esperado: quatro `<fieldset>` com `<legend>`; marcar três disciplinas gera três pares `disciplinas=…` na aba Network; o envio é bloqueado enquanto o aceite não estiver marcado; zero erros no validador do W3C.

<details markdown="1"><summary>Dica</summary>

Todas as caixas de seleção de disciplinas usam o **mesmo** `name` (`disciplinas`) e `value` diferentes — é assim que o servidor recebe uma lista. Cada uma precisa, ainda assim, de um `id` único para o seu `<label>`.
</details>

**B3.** Construa `exercicios/aula03/busca.html`: um formulário de busca com `method="get"`, um campo `name="q"`, um `<select>` de categoria (palestras, minicursos, oficinas) e um `<select>` de ordenação (por horário, por título). Envie e **transcreva a URL gerada**, explicando em uma frase cada parte da *query string* e por que este formulário usa `GET` e não `POST`.

Resultado esperado: a URL final tem a forma `busca.html?q=acessibilidade&categoria=oficinas&ordem=titulo`; o texto explica os três pares, o papel do `?` e do `&`, e argumenta que a busca é idempotente e compartilhável.

<details markdown="1"><summary>Dica</summary>

Use `action="busca.html"` (a própria página) para não cair em 404. Depois de enviar, copie a URL da barra de endereço e cole em uma aba nova: se a mesma busca aparece, você acabou de demonstrar por que buscas usam `GET`.
</details>

**B4.** Caça aos problemas. O formulário abaixo tem **pelo menos oito** problemas de acessibilidade, semântica e funcionamento. Encontre todos, reescreva o formulário corrigido e entregue um documento listando cada problema, a correção e o motivo.

**`exercicios/aula03/formulario-quebrado.html` (trecho)**

```html
<form>
  <div>Nome: <input type="text"></div>
  <div>Email: <input type="text" placeholder="Email"></div>
  <div>Senha: <input type="text" name="senha"></div>
  <div>
    <input type="radio" name="a" value="m">Masculino
    <input type="radio" name="b" value="f">Feminino
  </div>
  <div>Curso: <input type="text" name="curso"></div>
  <div>CEP: <input type="number" name="cep"></div>
  <div><img src="enviar.png" onclick="enviar()"></div>
</form>
```

Resultado esperado: uma versão corrigida com `method` declarado, `<label>` associado a cada campo, `name` em todos, `type` adequado a cada dado, um único `name` para o grupo de rádios (dentro de `<fieldset>` com `<legend>`), um `<button type="submit">` no lugar da imagem clicável e validação nativa nos campos aplicáveis; e uma lista com pelo menos oito itens justificados.

<details markdown="1"><summary>Dica</summary>

Comece pelos problemas que impedem o formulário de **funcionar** (campos sem `name`, rádios com `name` diferente, botão que não é botão) e depois passe aos de acessibilidade (rótulos, agrupamento, foco). O campo de senha com `type="text"` e o CEP com `type="number"` são dois erros de tipo, cada um com uma consequência diferente.
</details>

**B5.** Estenda a página de contato. Em `site-evento/contato.html`, construa um formulário de mensagem com: nome, e-mail, assunto (`<select>` com quatro opções), mensagem (`<textarea>` com `maxlength="600"`) e uma escolha entre "quero receber resposta por e-mail" e "por telefone" (rádios), com o telefone aparecendo como campo opcional. Método `post`, `action="/contato"`.

Resultado esperado: o formulário completo dentro do `<main>` da `contato.html`, com `<fieldset>` no grupo de rádios, `autocomplete` correto em nome, e-mail e telefone, e zero erros no W3C.

<details markdown="1"><summary>Dica</summary>

Um `<select>` de assunto com `value=""` na primeira opção mais `required` garante uma escolha consciente. Para o telefone opcional, não use `required`: em HTML puro você ainda não consegue tornar um campo obrigatório **em função de outro** — isso é JavaScript, e você fará na Aula 14.
</details>

### Nível C — Desafio

**C1.** Formulário de matrícula institucional. Reproduza, em HTML puro, um formulário de matrícula acadêmica com pelo menos **25 campos** organizados em **cinco** `<fieldset>`: identificação, documentos, endereço, dados acadêmicos e informações complementares. Requisitos: todo campo com `<label>` associado e `autocomplete` semântico; validação nativa em todos os campos aplicáveis (`required`, `pattern`, `min`/`max`, `minlength`); ordem de tabulação lógica sem `tabindex` positivo; zero erros no validador do W3C. Ao final, escreva meia página justificando a escolha do `type` de cada campo não trivial (CPF, CEP, data, matrícula, renda, telefone).

<details markdown="1"><summary>Dica</summary>

Comece pela lista de dados em papel, agrupando-os antes de escrever uma linha de HTML: os cinco `<fieldset>` saem naturalmente do agrupamento. Para o endereço, use os valores de `autocomplete` específicos (`postal-code`, `address-line1`, `address-level2`, `address-level1`) — é o que faz o navegador preencher tudo depois do CEP. Teste com o teclado antes de validar no W3C.
</details>

**C2.** Formulário de inscrição do projeto autoral. No seu `meu-projeto/`, construa a página de formulário equivalente à `inscricao.html` — pedido, reserva, cadastro, matrícula, agendamento: o que fizer sentido no seu tema — com no mínimo 12 campos, 3 `<fieldset>`, um `<select>` com `<optgroup>`, um `<datalist>`, um grupo de rádios, um grupo de caixas de seleção, um `<textarea>` e validação nativa em pelo menos 5 campos. Este formulário é um dos requisitos do Marco 1 do projeto (Aula 06).

<details markdown="1"><summary>Dica</summary>

Não copie os campos do site do evento trocando os textos: pergunte-se que dados o **seu** domínio realmente precisa coletar. Um brechó precisa de tamanho e forma de pagamento; uma agenda de quadras precisa de data, horário e número de jogadores. Cada campo que você não usar depois é um campo que não deveria existir.
</details>

## 🏆 Desafios

### ⭐ O formulário de três campos
Tags: html, formularios, acessibilidade

Todo mundo já desistiu de preencher um cadastro. Qual é o menor formulário capaz de inscrever alguém em um evento? Pegue a `inscricao.html` que você acabou de construir e faça o caminho inverso: corte tudo que não é indispensável e chegue a uma versão de **três campos**. Depois defenda cada corte. A pergunta que guia o exercício é sempre a mesma: "o que a organização do evento faria de diferente se soubesse este dado?" — se a resposta for "nada", o campo sai.

**Critérios de pronto**

- Um arquivo `inscricao-minima.html` com exatamente três campos visíveis, todos com `<label>`, `autocomplete` e validação nativa.
- Um arquivo `cortes.md` listando cada campo removido da versão completa e a justificativa em uma linha.
- Pelo menos dois campos removidos com a justificativa "pode ser perguntado depois" e a explicação de quando seria o momento certo de perguntar.
- Uma medição honesta: cronometre o preenchimento das duas versões (a completa e a mínima) por um colega e registre os dois tempos.

<details markdown="1"><summary>Pistas</summary>

1. Comece pelos campos que a organização consegue **deduzir** de outro campo (a matrícula diz o curso; o CPF diz a data de nascimento em outro sistema).
2. Procure "progressive disclosure" e pense em quais dados podem ser pedidos só no credenciamento, presencialmente.
3. Um campo obrigatório custa mais que um opcional: o opcional que quase ninguém preenche talvez devesse simplesmente não existir.
4. Nome, e-mail e mais um. Qual é o terceiro, e por quê?
</details>

### ⭐⭐ Auditoria de um formulário real
Tags: formularios, acessibilidade, investigacao, html

Escolha um formulário público de verdade: matrícula de uma universidade, agendamento de uma prefeitura, cadastro de uma loja, abertura de conta de um banco. Abra o DevTools e leia o HTML dele. Quantos campos têm `<label>` de verdade? Quantos usam `placeholder` como rótulo? O grupo de rádios está em `<fieldset>`? Dá para preencher tudo só com o teclado? Você vai descobrir que sites enormes, com equipes enormes, erram exatamente as coisas desta aula — e vai aprender mais lendo o erro dos outros do que acertando sozinho.

**Critérios de pronto**

- Um relatório de duas páginas com o endereço do formulário auditado e a data da auditoria.
- Cada problema encontrado classificado por severidade (impede o uso / atrapalha / incomoda), com o trecho de HTML original copiado do DevTools e o trecho corrigido ao lado.
- O resultado de uma passagem completa **só com o teclado**, descrevendo onde você travou (ou registrando que não travou).
- Uma reescrita completa do formulário em HTML acessível, com todos os problemas corrigidos, que valide sem erros no W3C.
- Pelo menos um problema encontrado com o checklist da seção 8 que uma ferramenta automática **não** apontaria.

<details markdown="1"><summary>Pistas</summary>

1. No DevTools, com o campo selecionado, procure o painel **Accessibility**: ele mostra o "nome acessível" calculado do elemento. Nome vazio significa rótulo ausente.
2. Rode também o **Lighthouse** (aba do DevTools) na categoria Accessibility, ou a extensão axe DevTools — mas lembre-se: as ferramentas pegam cerca de um terço dos problemas.
3. O teste do teclado é o mais revelador e não precisa de ferramenta nenhuma: <kbd>Tab</kbd>, <kbd>Shift</kbd>+<kbd>Tab</kbd>, setas, <kbd>Espaço</kbd>, <kbd>Enter</kbd>.
4. Compare a ordem do <kbd>Tab</kbd> com a ordem visual: quando o CSS move um campo de lugar, elas divergem — e o formulário fica confuso para quem não usa mouse.
</details>

### ⭐⭐ Dado sujo: o formulário que estraga o banco
Tags: formularios, html, investigacao, bug

Um mesmo campo "telefone", sem restrição nenhuma, recebeu na vida real: `66999990000`, `(66) 99999-0000`, `66 9 9999 0000`, `+55 66 99999-0000`, `9999-0000 (falar com a Maria)` e `não tenho`. Nenhum está errado do ponto de vista de quem digitou — todos estão errados do ponto de vista de quem vai usar o dado. Sua missão: descobrir quanto de sujeira um formulário mal projetado gera e provar que dá para reduzir isso só com HTML.

**Critérios de pronto**

- Uma página `coleta-suja.html` com cinco campos sem nenhuma restrição (telefone, CEP, data, valor em reais e nome) e uma página `coleta-limpa.html` com os mesmos cinco dados, agora com `type`, `pattern`, `min`/`max`, `maxlength` e `title` adequados.
- Dez pessoas (colegas, familiares) preenchendo as duas versões, com as respostas registradas em uma tabela.
- Uma contagem de quantos valores de cada versão poderiam entrar direto em um banco de dados sem tratamento manual.
- Uma conclusão de dez linhas explicando qual restrição trouxe o maior ganho por linha de HTML escrita.
- Um campo em que você **não** conseguiu impedir a sujeira só com HTML, com a explicação do porquê e do que faltaria (adiante o que a Aula 14 vai resolver).

<details markdown="1"><summary>Pistas</summary>

1. Para registrar as respostas sem servidor, use `method="get"` e copie a URL gerada a cada envio — a *query string* já é a sua tabela de coleta.
2. `pattern` resolve formato, mas não resolve **conteúdo**: `000.000.000-00` passa no padrão de CPF e não é um CPF válido. Guarde esse caso para a conclusão.
3. Compare `type="date"` com um campo de texto pedindo "DD/MM/AAAA": a diferença na sujeira costuma ser a maior de todas.
4. Para valores em reais, teste `type="number"` com `step="0.01"` e observe o que acontece quando alguém digita vírgula.
</details>

### ⭐⭐⭐ Formulário multietapas sem JavaScript
Tags: html, formularios, acessibilidade, projeto

Formulários longos assustam. A solução clássica é dividir em etapas ("Etapa 2 de 4") — e quase todo mundo faz isso com JavaScript. Mas dá para construir um formulário de várias etapas usando **apenas HTML**, com uma página por etapa e os dados sendo carregados de uma para a próxima em campos ocultos. O resultado funciona sem JavaScript, funciona com o botão Voltar do navegador e é totalmente acessível. Descubra como e construa.

**Critérios de pronto**

- Quatro páginas (`etapa-1.html` a `etapa-4.html`), cada uma com o seu `<form method="get">` apontando para a etapa seguinte e um `<progress>` ou um texto "Etapa N de 4".
- Os dados das etapas anteriores viajam até a última página e aparecem lá em campos ocultos, prontos para o envio final.
- Uma página `revisao.html` que mostra, em texto, tudo o que foi preenchido antes do envio definitivo.
- O botão **Voltar** do navegador funciona em todas as etapas e mantém as respostas já dadas.
- Validação nativa em cada etapa: não é possível avançar com um campo obrigatório vazio.
- Um texto de meia página comparando essa abordagem com a de "abas em JavaScript", listando duas vantagens e duas desvantagens concretas de cada uma.

<details markdown="1"><summary>Pistas</summary>

1. Com `method="get"`, tudo que foi preenchido está na URL da próxima etapa — e uma URL pode ser lida, copiada e retomada depois.
2. `<input type="hidden">` é o elemento que carrega um dado de uma página para a outra sem exibi-lo. Você precisará de um por campo herdado.
3. Sem servidor, os campos ocultos da etapa seguinte não se preenchem sozinhos: para o exercício, preencha os `value` à mão a partir da URL e explique no texto o que um servidor faria automaticamente.
4. Cuidado com dados sensíveis: uma senha nunca poderia atravessar etapas assim. Diga isso no seu texto final — vale ponto.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| O campo está preenchido, mas não aparece na aba Network nem na URL | Falta o atributo `name` (ou o campo está `disabled`) | Todo campo que deve ser enviado precisa de `name`; troque `disabled` por `readonly` se o valor precisa chegar ao servidor |
| Todos os botões de rádio ficam marcados ao mesmo tempo | Cada rádio recebeu um `name` diferente | Mesmo `name` no grupo inteiro, `value` diferente em cada um |
| Clicar no rótulo não foca o campo | `for` sem `id` correspondente, ou `id` duplicado na página | Confira o par `for`/`id`; o validador acusa `Duplicate ID` quando há repetição |
| O `<select>` com `required` nunca acusa erro | A primeira `<option>` tem um valor real em vez de `value=""` | Inclua uma primeira opção `<option value="">Selecione…</option>` |
| O `<textarea>` com `required` é aceito parecendo vazio | Espaços e quebras de linha de indentação viraram conteúdo do campo | Escreva `<textarea></textarea>` colado, sem nada entre as tags |
| A página "recarrega sozinha" ao clicar num botão qualquer | `<button>` sem `type` dentro do `<form>` age como `submit` | Declare `type="button"` em todos os botões que não enviam |
| A mensagem de erro do `pattern` é "Corresponda ao formato solicitado." | Falta o atributo `title` no campo | Sempre acompanhe `pattern` de um `title` explicando o formato esperado |
| O CPF perde os zeros à esquerda e mostra setinhas de incremento | Uso de `type="number"` em uma sequência de dígitos | Use `type="text"` com `pattern` (e `inputmode="numeric"`, a partir da Aula 04) |
| A senha aparece na barra de endereço depois do envio | O formulário está com `method="get"` | Troque para `method="post"`; nenhum dado sensível vai por `GET` |
| O validador acusa `The for attribute of the label element must refer to a non-hidden form control` | O `for` aponta para um `id` que não existe, foi renomeado ou pertence a um campo `hidden` | Corrija o `for` para o `id` do campo visível correspondente |
| O validador acusa `Element optgroup is missing required attribute label` | `<optgroup>` sem o atributo `label` | Todo `<optgroup>` precisa de `label`; ele é anunciado pelo leitor de tela |
| Só o último valor do grupo de caixas de seleção chega ao servidor | Cada caixa recebeu um `name` diferente, e o servidor foi programado para uma chave só | Use o mesmo `name` em todas as caixas do grupo e `value` distintos |

## 🏠 Para praticar depois da aula (1 h)

**Parte 1 — Leitura (20 min).** SILVA, Maurício Samy. *Criando sites com HTML*, capítulo de formulários. TERUEL, Evandro C. *HTML 5 — Guia Prático*, capítulo de formulários HTML5. Na MDN em pt-BR, o guia "Seu primeiro formulário" e a referência de `<input>`. Anote dois atributos que aparecem nas leituras e não apareceram nesta aula.

**Parte 2 — Produção (30 min).** Exercícios **B2** (matrícula em disciplinas) e **B4** (caça aos problemas), em arquivos `.html` comentados dentro de `exercicios/aula03/`. Para o B4, produza também o documento listando cada problema identificado, a correção aplicada e a justificativa.

**Parte 3 — Discussão (10 min).** Em texto próprio (ou no fórum da turma, se você cursa a disciplina): em 10 a 15 linhas, explique como a escolha do tipo de campo e das restrições de validação influencia a qualidade do que chega ao banco de dados. Traga um exemplo concreto de dado sujo que você já viu (um telefone impossível, um nome em caixa alta, uma data no futuro) e diga qual atributo desta aula teria evitado.

**Critério de pronto:** os dois arquivos abrem no navegador, validam sem erros no W3C, permitem envio apenas com os campos obrigatórios preenchidos e podem ser percorridos inteiramente pelo teclado, com o rótulo de cada campo funcionando ao clique.

**Guarde:** a pasta do projeto (ou, se você já usa Git — assunto do capítulo 02 da trilha Deploy e da Aula 15 —, faça commit e push).

## ✅ Checkpoint do projeto

Ao fim desta aula, em `site-evento/` e em `meu-projeto/`:

- [ ] `inscricao.html` com um `<form method="post" action="/inscrever">` e um `<input type="hidden">` de origem.
- [ ] Quatro `<fieldset>` de primeiro nível com `<legend>` (dados pessoais, dados acadêmicos, participação e informações complementares), com os grupos de escolha em `<fieldset>` aninhados.
- [ ] Pelo menos oito tipos diferentes de `<input>` em uso (`text`, `email`, `tel`, `date`, `number`, `radio`, `checkbox`, `hidden`).
- [ ] Um `<select>` com `<optgroup>` e primeira opção `value=""`, um `<datalist>` e um `<textarea>` com `maxlength`.
- [ ] `<label>` associado a **todos** os campos, com a obrigatoriedade indicada no texto do rótulo.
- [ ] Validação nativa em pelo menos seis campos: `required`, `minlength`, `min`/`max` e dois `pattern` acompanhados de `title`.
- [ ] Um grupo de rádios com o mesmo `name` e um grupo de caixas de seleção com o mesmo `name`.
- [ ] `autocomplete` semântico em nome, e-mail, telefone, instituição e data de nascimento.
- [ ] O formulário inteiro percorrível e enviável apenas com o teclado.
- [ ] `contato.html` com o formulário de mensagem do exercício B5.
- [ ] Zero erros no validador do W3C nas cinco páginas.
- [ ] Em `meu-projeto/`: o formulário equivalente do seu tema (exercício C2), com no mínimo 12 campos.

## 📚 Para aprofundar

- MDN — Formulários web, guia completo (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Learn_web_development/Extensions/Forms> — comece por "Seu primeiro formulário" e "Como estruturar um formulário web".
- MDN — O elemento `<input>`: <https://developer.mozilla.org/pt-BR/docs/Web/HTML/Element/input> — a referência de todos os tipos, com exemplo interativo de cada um.
- MDN — O elemento `<form>`: <https://developer.mozilla.org/pt-BR/docs/Web/HTML/Element/form> — todos os atributos, incluindo `enctype` e `novalidate`.
- MDN — Validação de dados de formulário: <https://developer.mozilla.org/pt-BR/docs/Learn_web_development/Extensions/Forms/Form_validation> — a validação nativa em detalhe; a segunda metade usa JavaScript e é a Aula 14.
- MDN — O elemento `<label>`: <https://developer.mozilla.org/pt-BR/docs/Web/HTML/Element/label> — as duas formas de associação e os erros mais comuns.
- MDN — Atributo `autocomplete`: <https://developer.mozilla.org/pt-BR/docs/Web/HTML/Attributes/autocomplete> — a lista completa dos valores semânticos.
- web.dev — Learn Forms: <https://web.dev/learn/forms> — curso gratuito só sobre formulários, com um capítulo por elemento.
- W3C — WCAG 2.1 em português, critérios 1.3.1, 1.3.5 e 3.3.2: <https://www.w3.org/Translations/WCAG21-ptbr/> — os critérios que esta aula atende.
- Validador do W3C: <https://validator.w3.org/> — use em todas as páginas, sempre.
- SILVA, Maurício Samy. *Criando sites com HTML: sites de alta qualidade com HTML e CSS*. Novatec, 2008 — capítulo de formulários.
- TERUEL, Evandro C. *HTML 5 — Guia Prático*. Saraiva, 2014 — capítulo de formulários HTML5 (Minha Biblioteca).
- MILETTO, Evandro M.; BERTAGNOLLI, Silvia C. *Desenvolvimento de software II*. Bookman, 2014 — capítulo sobre entrada de dados em aplicações web.

Na próxima aula você fecha o capítulo de formulários com os campos que faltaram — upload de arquivos com `enctype`, `<output>`, `<progress>`, `<meter>`, `inputmode` e campos ligados a um formulário à distância — e passa para o que dá vida às páginas: listas bem estruturadas, imagens responsivas com `srcset` e `<picture>`, vídeo com legendas e conteúdo externo em `<iframe>`.
