# Capítulo 11 — IA como ferramenta de desenvolvimento

> **Deploy & Ferramentas** · Unidade 3: Infraestrutura, automação e qualidade
> WebLab · curso aberto de desenvolvimento web
> **Tempo estimado:** 2 a 3 h · estudo autônomo, em paralelo à sua trilha

## 🎯 Objetivos de aprendizagem

Ao final deste capítulo você será capaz de:

- Explicar, em termos práticos, o que um modelo de linguagem faz ao gerar código e por que "responder com confiança" não é o mesmo que "responder certo".
- Escolher entre os três formatos de assistente — chat, autocompletar no editor e agente que edita arquivos — de acordo com a tarefa, sabendo o que cada um enxerga do seu projeto.
- Escrever um prompt com os seis elementos que mudam a qualidade da resposta: objetivo, código real, versões, erro literal, o que você já tentou e o formato esperado.
- Usar o assistente com proveito em cinco tarefas concretas: explicar um erro, revisar código, gerar testes, escrever mensagem de commit e `README`, e aprender uma API nova.
- Reconhecer os modos típicos de falha — API alucinada, versão desatualizada, pacote inexistente, código plausível e inseguro — e checar cada um na documentação oficial em menos de dois minutos.
- Aplicar as regras de segurança e privacidade sobre o que nunca entra em um prompt (segredos, `.env`, dados pessoais reais) e o que fazer se algo escapar.
- Adotar uma política pessoal de uso de IA como estudante: apoio bem-vindo, mas autoria e capacidade de explicar são o que provam — para você mesmo, antes de qualquer outra pessoa — que o aprendizado aconteceu.

## 📋 Pré-requisitos

- [ ] Seu **projeto autoral** versionado no GitHub, com front e API, rodando localmente (`npm run dev` e `npm start`).
- [ ] O projeto publicado, ainda que parcialmente (Capítulos 03, 05, 06 ou 07).
- [ ] `npm test` e `npm run lint` configurados como no Capítulo 10 — este capítulo usa os dois para conferir o que a IA propõe.
- [ ] Uma conta em pelo menos um assistente de chat com plano gratuito, e o navegador com a documentação oficial da sua stack aberta em outra aba.
- [ ] Git limpo (`git status` sem alterações pendentes) antes de começar o Passo a passo.

> No Capítulo 10 você instrumentou o projeto e transformou "acho que está bom" em número: linter, testes, Lighthouse e monitoramento de erros. Hoje a trilha fecha com a ferramenta mais nova da caixa e, de longe, a mais mal usada — o assistente de inteligência artificial. Ele acelera muito quem já sabe o que está fazendo e atrapalha silenciosamente quem não sabe, porque escreve com a mesma confiança um trecho correto e um trecho inventado; a diferença entre os dois casos não está na ferramenta, e sim no que você faz **depois** que a resposta aparece na tela. É esse "depois" que você vai aprender aqui, usando exatamente aquelas ferramentas como **rede de verificação** para tudo o que o assistente sugerir — porque a única maneira honesta de aceitar código de IA é ter como provar que ele funciona. Ao fim deste capítulo, o ciclo completo (escrever, versionar, publicar, medir, revisar) fecha.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | O que o assistente é; os três formatos; anatomia de um prompt com contexto; os cinco usos que valem a pena |
| 2 | 50 min | Modos de falha: alucinação de API e de versão, pacote inexistente, código inseguro; segredos no prompt; protocolo de verificação |
| 3 | 50 min | Dependência e aprendizado; política pessoal de uso de IA; Passo a passo de revisão assistida do projeto autoral; Laboratório |

## 1. O que a ferramenta faz, de verdade

Um assistente de código é um **modelo de linguagem**: dado um texto, ele calcula qual pedaço de texto tem maior chance de vir a seguir, e repete isso até formar a resposta. Ele foi treinado em uma quantidade enorme de código público, documentação, fóruns e livros. O efeito prático é impressionante — ele "sabe" a forma de uma rota Express, a cara de um componente Vue, o jeito de uma consulta SQL — porque essas formas se repetem milhões de vezes no material de treino.

O que não existe nesse processo é uma etapa de conferência. O modelo não executa o código que escreve, não consulta a documentação da versão que você usa e não tem um banco de dados de verdades para checar. Ele produz o texto **mais plausível**. Quando o plausível coincide com o correto — o caso comum em tarefas rotineiras — você ganha tempo. Quando não coincide, você recebe um erro escrito com a mesma segurança de uma resposta certa. Esse é o ponto central deste capítulo, e vale escrever em letras grandes:

> **⚠️ Atenção**
> A confiança do texto não carrega nenhuma informação sobre a correção do texto. Um assistente não diz "acho que" com menos frequência quando está errado. Trate toda resposta como um **palpite muito bem informado de um colega que nunca rodou o seu projeto**.

Três consequências práticas disso, que explicam quase todos os problemas do capítulo:

1. **Ele responde pela média do que existe na internet.** Se 90 % do código público de Express ainda é da versão 4, a resposta média será da versão 4 — mesmo você usando a 5.
2. **Ele não sabe o que não está no prompt.** O nome das suas tabelas, a estrutura das suas pastas, o que você já tentou: nada disso existe para ele se você não colar.
3. **Ele erra mais no específico do que no geral.** "Explique o que é um middleware" tem chance altíssima de sair correto. "Qual o nome exato da opção do Vuetify 4 para o tema padrão" tem chance bem menor.

> **🧠 Você sabia?**
> O termo técnico para uma resposta inventada com aparência de verdade é **alucinação**. Ele já saiu do jargão acadêmico e virou vetor de ataque: pesquisadores mostraram que modelos inventam nomes de pacotes npm/PyPI de forma **repetível** — o mesmo nome falso aparece várias vezes para prompts parecidos. Atacantes registram esses nomes inventados e esperam alguém rodar `npm install`. O apelido do golpe é *slopsquatting*, primo do *typosquatting*. É por isso que a regra "todo pacote novo é conferido no `npmjs.com` antes de instalar" deixou de ser preciosismo.

### 1.1 Onde ele é excelente e onde é fraco

| Tarefa | Desempenho típico | Por quê |
|---|---|---|
| Explicar um erro conhecido | Muito bom | A mensagem literal é um ótimo indexador do material de treino |
| Escrever código repetitivo (CRUD, formulário, teste) | Muito bom | Padrão altamente repetido, verificável em segundos |
| Traduzir entre linguagens ou estilos | Muito bom | Tarefa de forma, não de verdade |
| Escrever `README`, commit, comentário | Bom, com revisão | Ele só sabe o que você contou do projeto |
| Lembrar detalhes de uma versão recente | Fraco | A média do treino puxa para a versão antiga |
| Decidir arquitetura do seu projeto | Fraco | Ele não conhece seus requisitos nem o seu prazo |
| Afirmar que algo "não existe" | Muito fraco | Ele tende a inventar em vez de admitir lacuna |
| Contar, medir, garantir desempenho | Muito fraco | Não executa nada; números costumam ser inventados |

A leitura correta dessa tabela não é "use só nas linhas boas". É: **quanto mais para baixo na tabela, mais cara fica a verificação — e a verificação é sua**.

## 2. Os três formatos de assistente

Os produtos mudam de nome o tempo todo; os três formatos, não. Saber em qual você está muda o que você precisa colar no prompt.

### 2.1 Chat (ChatGPT, Claude, Gemini)

Você conversa em uma janela separada do editor. O assistente enxerga **apenas o que você cola**. É o formato mais fácil de controlar e o melhor para aprender, justamente porque obriga você a decidir o que é relevante — o ato de recortar o contexto já é metade do diagnóstico.

Bom para: entender um erro, comparar duas abordagens, revisar um arquivo, transformar um rascunho em `README`, pedir explicação de um conceito com exemplos.

Cuidado: a conversa não conhece o resto do projeto. Se você pedir "adicione paginação" sem colar a rota, ele vai inventar uma rota plausível e você vai colar código que não casa com o seu.

### 2.2 Autocompletar no editor (GitHub Copilot)

Uma extensão do VS Code sugere a continuação enquanto você digita, em cinza; <kbd>Tab</kbd> aceita, <kbd>Esc</kbd> descarta. Ele lê os arquivos abertos e o arquivo atual, então acerta muito o **estilo** do seu projeto: seus nomes em português, sua indentação, seu jeito de tratar erro.

Bom para: a segunda, terceira e quarta rota depois que você escreveu a primeira; testes parecidos entre si; blocos `catch`; preencher um objeto grande.

Cuidado: é o formato que mais induz a aceitar sem ler, porque a sugestão aparece exatamente onde o seu olho já está. E ele continua o padrão do arquivo, inclusive quando o padrão está errado — se a sua primeira rota concatena SQL, ele vai concatenar nas próximas cinco.

### 2.3 Agente no editor ou no terminal (Claude Code, Cursor)

Aqui o assistente **lê e escreve arquivos** do projeto, roda comandos e mostra um diff para você aprovar. É o formato mais poderoso e o mais perigoso: ele pode alterar dez arquivos com uma frase sua.

Bom para: refatorações mecânicas em muitos arquivos, criar a estrutura inicial de testes, migrar um padrão repetido, investigar "onde está a função que faz X" em um projeto grande.

Cuidado: só use com o Git limpo e em uma branch (`git switch -c ia/refatora-inscricoes`). O diff é o seu contrato — se você não consegue ler o diff, não aceite. E jamais deixe um agente rodar comandos destrutivos ou de deploy sem olhar.

| Formato | O que ele enxerga | Risco principal |
|---|---|---|
| Chat | Só o que você colar | Resposta genérica que não casa com o projeto |
| Autocompletar | Arquivos abertos no editor | Aceitar por reflexo, sem ler |
| Agente | O repositório inteiro, se autorizado | Mudança ampla difícil de auditar |

> **💡 Dica**
> Com agente, adote a regra do commit-âncora: `git add -A && git commit -m "checkpoint antes da IA"` antes de começar. Se a refatoração sair errada, `git reset --hard HEAD` devolve tudo. Sem esse commit você fica refém do "desfazer" do editor.

## 3. Contexto é tudo: a anatomia de um prompt

A diferença entre uma resposta inútil e uma resposta cirúrgica quase nunca está no modelo. Está em seis elementos. Um prompt profissional tem todos.

1. **Objetivo em uma frase** — o que você quer que aconteça, não como fazer.
2. **Código real** — o trecho mínimo que reproduz o problema, com o caminho do arquivo.
3. **Versões** — Node, framework, biblioteca. É o elemento mais esquecido e o que mais evita alucinação.
4. **Erro literal** — copiado e colado do terminal ou do console, inteiro, com a pilha.
5. **O que você já tentou** — evita que ele repita o caminho que você já eliminou.
6. **Formato esperado** — "responda com a causa em duas frases e depois o arquivo corrigido inteiro".

Compare. O prompt ruim, que todo mundo escreve na primeira semana:

```text
minha api não ta funcionando, da erro quando eu mando o post. me ajuda
```

E o prompt bom, sobre o mesmo problema:

```text
Objetivo: descobrir por que meu POST /api/inscricoes responde 500.

Stack: Node 22 LTS, Express 5.1, mysql2 3 (mysql2/promise, createPool), ESM.

Arquivo unieventos-api/src/rotas/inscricoes.js:

import { Router } from 'express';
import { pool } from '../db/pool.js';

export const rotasInscricoes = Router();

rotasInscricoes.post('/', async (req, res) => {
  const { eventoId, nome, email } = req.body;
  const [resultado] = await pool.query(
    'INSERT INTO inscricoes (evento_id, nome, email) VALUES (?, ?, ?)',
    [eventoId, nome, email]
  );
  res.json({ id: resultado.insertId });
});

Erro literal no terminal:

TypeError: Cannot destructure property 'eventoId' of 'req.body' as it is undefined.
    at /home/ana/unieventos-api/src/rotas/inscricoes.js:7:11

Requisição feita com: curl -X POST http://localhost:3000/api/inscricoes
  -H "Content-Type: application/json" -d '{"eventoId":1,"nome":"Ana","email":"ana@exemplo.com"}'

Já tentei: reiniciar o servidor e conferir que a tabela existe.

Formato da resposta: causa em duas frases, depois a linha exata que falta e onde ela entra.
```

O segundo prompt tem uma resposta praticamente inevitável e correta: falta `app.use(express.json())` antes das rotas, e no Express 5 `req.body` é `undefined` (não `{}`) quando nada foi analisado. O primeiro prompt tem mil respostas possíveis, e você vai testar seis delas antes de chegar à certa.

> **🔬 Investigue**
> Faça o teste dos dois prompts acima com o seu próprio bug, agora. Abra duas conversas novas. Na primeira, escreva a versão preguiçosa. Na segunda, os seis elementos. Cronometre quanto tempo passa até você ter uma correção **que funciona** em cada caso. Anote os dois tempos — eles vão para o `IA.md` do Passo a passo. É comum a diferença ser de uma ordem de grandeza.

### 3.1 Três frases que melhoram qualquer prompt

- **"Se faltar informação para responder, pergunte antes de supor."** Reduz drasticamente a invenção de nomes de tabela e de rota.
- **"Cite a página da documentação oficial que sustenta cada afirmação."** Ele pode errar o link, mas passa a ancorar a resposta em algo verificável — e um link inventado é fácil de flagrar: você clica.
- **"Aponte problemas; não elogie o código."** Sem isso, muitos assistentes começam por "ótimo código!" e amaciam a crítica. Você não quer um elogio; quer a lista de defeitos.

> **💡 Dica**
> Peça sempre o **arquivo inteiro** corrigido, não "as linhas que mudam". Resposta em pedaços solta reticências e comentários do tipo "restante igual", e é aí que você cola um arquivo quebrado. Arquivo inteiro você compara com `git diff` e enxerga tudo.

## 4. Cinco usos que valem o tempo

### 4.1 Explicar um erro

É o melhor uso, disparado. A mensagem literal do erro é um índice quase perfeito: se aquele erro é comum, o assistente já viu centenas de discussões sobre ele. Cole a mensagem **inteira**, com a pilha, e diga a versão.

O ganho não é só a correção — é a **explicação**. Peça sempre: "explique por que esse erro acontece, em três frases, antes de corrigir". Em um semestre isso constrói um repertório de diagnóstico que nenhuma correção copiada constrói.

### 4.2 Revisar código

Aqui a IA rende porque a tarefa é procurar padrões ruins, e padrões ruins são exatamente o que se repete no material de treino. Um exemplo real, tirado do que aparece em quase todo projeto autoral na primeira versão:

```js
// unieventos-api/src/rotas/inscricoes.js — versão antes da revisão
import { Router } from 'express';
import { pool } from '../db/pool.js';

export const rotasInscricoes = Router();

rotasInscricoes.post('/', async (req, res) => {
  const { eventoId, nome, email } = req.body;
  const [resultado] = await pool.query(
    "INSERT INTO inscricoes (evento_id, nome, email) VALUES (" +
      eventoId + ", '" + nome + "', '" + email + "')"
  );
  res.json({ id: resultado.insertId, nome, email });
});
```

O prompt de revisão que funciona:

```text
Revise esta rota Express 5 procurando problemas de segurança, validação e
tratamento de erro. Não elogie. Para cada problema, dê: (1) o trecho exato,
(2) por que é problema, (3) como reproduzir o problema com um curl,
(4) a correção. Ordene do mais grave para o menos grave.

Stack: Node 22, Express 5.1, mysql2 3 com createPool, MySQL 8.
[cole aqui o código acima]
```

Uma resposta típica traz cinco achados. Você **não** aceita nenhum antes de checar — a coluna "confirmei como?" é a parte que importa:

| Achado apontado pela IA | Gravidade | Confirmei como? |
|---|---|---|
| SQL montado por concatenação: injeção | Alta | `curl` com `nome` contendo apóstrofo derruba a consulta |
| Nenhuma validação: aceita `nome` vazio ou ausente | Alta | `curl` sem `nome` grava a string `undefined` no banco |
| Responde 200 na criação, deveria ser 201 | Média | `curl -i` mostra `HTTP/1.1 200 OK` |
| Devolve o e-mail na resposta (dado pessoal) | Média | Leitura do corpo da resposta |
| Não confere se o evento existe | Média | `curl` com `eventoId` 9999 grava inscrição órfã |

A versão corrigida, que você escreve **entendendo cada linha**:

```js
// unieventos-api/src/rotas/inscricoes.js — versão revisada
import { Router } from 'express';
import { pool } from '../db/pool.js';

export const rotasInscricoes = Router();

rotasInscricoes.post('/', async (req, res) => {
  const { eventoId, nome, email } = req.body ?? {};

  if (!Number.isInteger(eventoId) || eventoId <= 0) {
    return res.status(400).json({ erro: 'Informe eventoId como número inteiro positivo.' });
  }
  if (typeof nome !== 'string' || nome.trim().length < 3) {
    return res.status(400).json({ erro: 'Informe nome com ao menos 3 caracteres.' });
  }
  if (typeof email !== 'string' || !email.includes('@')) {
    return res.status(400).json({ erro: 'Informe um e-mail válido.' });
  }

  const [eventos] = await pool.query('SELECT id FROM eventos WHERE id = ?', [eventoId]);
  if (eventos.length === 0) {
    return res.status(404).json({ erro: 'Evento não encontrado.' });
  }

  const [resultado] = await pool.query(
    'INSERT INTO inscricoes (evento_id, nome, email) VALUES (?, ?, ?)',
    [eventoId, nome.trim(), email.trim().toLowerCase()]
  );

  res.status(201).json({ id: resultado.insertId, eventoId, nome: nome.trim() });
});
```

Repare que os `?` do `mysql2` não são "escapar aspas": o driver envia valor e comando separados, então nenhum conteúdo digitado pelo usuário vira instrução SQL. Essa é a frase que você precisa saber dizer se alguém perguntar — numa revisão de código, numa entrevista técnica ou para si mesmo.

### 4.3 Gerar testes

Escrever o **primeiro** teste é chato; escrever o décimo é mecânico. A IA é ótima nos dois casos, desde que você faça três coisas depois:

1. **Rodar.** Teste gerado que nunca rodou é decoração.
2. **Quebrar de propósito.** Mude a regra no código (`length < 3` para `length < 0`) e confirme que o teste **falha**. Teste que passa com o código quebrado não testa nada — é o erro número um de suíte gerada por IA, porque o modelo tende a escrever asserções frouxas.
3. **Acrescentar o caso que ele não pensou.** Ele cobre o caminho feliz e o campo faltando; raramente cobre o seu caso de negócio (evento lotado, inscrição duplicada, e-mail já cadastrado).

Prompt que produz teste utilizável, no formato do runner embutido apresentado no Capítulo 10 §3.1 — a alternativa sem dependências, apropriada aqui porque o pedido é justamente não instalar nada:

```text
Gere testes com node:test (Node 22, ESM) para a rota POST /api/inscricoes abaixo.
O app é exportado nomeado em src/app.js (export const app) e não chama listen:
suba-o no teste com app.listen(0) e faça as requisições com fetch. Cubra: criação
válida (201), nome ausente (400), nome com 2 caracteres (400) e evento inexistente
(404). Feche o servidor e o pool no after. Não use nenhuma biblioteca externa.
[cole a rota revisada]
```

E o resultado, depois de você conferir e completar:

```js
// unieventos-api/tests/inscricoes.test.js
import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { app } from '../src/app.js';
import { pool } from '../src/db/pool.js';

let servidor;
let base;

before(async () => {
  servidor = app.listen(0);
  await new Promise((pronto) => servidor.once('listening', pronto));
  base = `http://127.0.0.1:${servidor.address().port}`;
  await pool.query('DELETE FROM inscricoes');
  await pool.query('INSERT INTO eventos (id, titulo, vagas) VALUES (1, ?, 40) ' +
    'ON DUPLICATE KEY UPDATE titulo = VALUES(titulo)', ['Semana Acadêmica']);
});

after(async () => {
  servidor.close();
  await pool.end();
});

async function inscrever(corpo) {
  return fetch(`${base}/api/inscricoes`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(corpo)
  });
}

test('cria a inscrição e responde 201', async () => {
  const resposta = await inscrever({ eventoId: 1, nome: 'Ana Souza', email: 'ana@exemplo.com' });
  assert.equal(resposta.status, 201);
  const corpo = await resposta.json();
  assert.ok(Number.isInteger(corpo.id));
  assert.equal(corpo.nome, 'Ana Souza');
});

test('recusa inscrição sem nome', async () => {
  const resposta = await inscrever({ eventoId: 1, email: 'ana@exemplo.com' });
  assert.equal(resposta.status, 400);
  const corpo = await resposta.json();
  assert.match(corpo.erro, /nome/i);
});

test('recusa nome com menos de 3 caracteres', async () => {
  const resposta = await inscrever({ eventoId: 1, nome: 'An', email: 'ana@exemplo.com' });
  assert.equal(resposta.status, 400);
});

test('recusa evento inexistente', async () => {
  const resposta = await inscrever({ eventoId: 9999, nome: 'Ana Souza', email: 'ana@exemplo.com' });
  assert.equal(resposta.status, 404);
});
```

### 4.4 Escrever commit e `README`

Mensagem de commit é o uso mais subestimado. Dê a ele o diff em texto e peça o padrão que você usa:

```bash
git add -p
git diff --staged > /tmp/mudanca.diff
wc -l /tmp/mudanca.diff
```

```text
Escreva uma mensagem de commit no padrão Conventional Commits, em português,
com título de no máximo 72 caracteres e um corpo de até 4 linhas explicando o
porquê (não o quê). Baseie-se apenas neste diff:
[cole o conteúdo de /tmp/mudanca.diff]
```

Resultado típico, muito melhor do que o "ajustes" que você escreveria com pressa:

```text
fix(inscricoes): usa parâmetros na consulta e valida a entrada

A rota montava o INSERT por concatenação, permitindo injeção de SQL com
qualquer apóstrofo no nome. Passa a usar placeholders do mysql2 e a
recusar com 400 corpo sem eventoId, nome curto ou e-mail sem arroba.
Inscrição em evento inexistente agora responde 404.
```

Para o `README`, o segredo é o mesmo: alimente com **fatos do repositório**, não com adjetivos.

```bash
cat package.json
ls -R src | head -40
cat .env.example
grep -rn "router\.\(get\|post\|put\|delete\)" src/rotas | head -20
```

```text
Escreva o README.md do meu projeto a partir dos fatos abaixo, em português,
com estas seções: o que é, tecnologias, como rodar localmente, variáveis de
ambiente, rotas da API, como rodar os testes, como publicar. Não invente
funcionalidade que não esteja nos fatos. Onde faltar informação, escreva a
seção com uma pergunta objetiva para mim entre colchetes.
[cole a saída dos comandos acima]
```

A instrução final é a mais importante: sem ela, o assistente preenche as lacunas com invenção simpática ("suporta autenticação JWT", que você nunca implementou). Com ela, você recebe uma lista de perguntas — que é exatamente o que um bom `README` precisa que você responda.

### 4.5 Aprender uma API nova

Use o assistente como um professor particular impaciente, não como um manual. Três pedidos que funcionam:

- "Explique `createPool` do mysql2 comparando com abrir e fechar uma conexão a cada requisição, com uma analogia."
- "Me faça cinco perguntas de múltipla escolha sobre middlewares do Express 5 e só depois mostre as respostas."
- "Escreva o menor exemplo executável possível de um `store` Pinia com uma ação assíncrona, e diga qual linha eu deveria mudar primeiro se a lista vier vazia."

Depois de entender, **confirme na documentação oficial**. Esse par — explicação rápida da IA, confirmação lenta na doc — é mais eficiente do que só ler a doc e infinitamente mais confiável do que só perguntar.

> **🧠 Você sabia?**
> Um estudo controlado da Universidade Stanford comparou pessoas resolvendo tarefas de programação com e sem assistente de IA. O grupo com assistente escreveu, em média, código **menos seguro** — e, ao mesmo tempo, declarou **mais confiança** de que o código estava seguro. Não é que a ferramenta seja ruim: é que ela desliga a desconfiança de quem a usa. O antídoto é procedimento, não força de vontade: é por isso que a §7 deste capítulo é um checklist e não um conselho.

## 5. Como a IA erra

### 5.1 Alucinação de API e de versão

O modo de falha mais frequente na nossa stack, porque quase toda biblioteca desta trilha teve uma virada de versão recente e o material de treino é dominado pela versão antiga. Os quatro casos que você vai encontrar com mais frequência:

| Você usa | A IA costuma responder | Como flagrar |
|---|---|---|
| Express 5 | `body-parser`, `app.del()`, `res.json(obj, 201)` | `express.json()` é nativo; `app.del is not a function` |
| Firebase 12 modular | `firebase.auth().signInWith…` | `firebase.auth is not a function`; só existe `import { getAuth }` |
| Vuetify 4 | Props `align`/`justify` em `v-row`; supõe tema claro por padrão | Na 4 o alinhamento é classe utilitária e o tema padrão é `system` |
| swagger-jsdoc 6 | Chave `swaggerDefinition` | A 6.x usa `definition`; a doc gerada sai vazia |

Vale para o Supabase também: código gerado costuma esquecer que uma tabela com RLS habilitado e **sem policy** devolve `data: []` sem nenhum erro. O assistente entrega uma consulta correta, o front mostra "nenhum evento" e você passa duas horas caçando um bug que não está no JavaScript.

O antídoto é barato e cabe no prompt: **diga a versão**. "Express 5", "Vuetify 4", "firebase 12 modular". Melhora a resposta na hora — e, quando não melhora, você tem a linha exata para conferir.

> **🔬 Investigue**
> Peça agora ao seu assistente: "Como faço para o Vuetify 4 abrir sempre no tema claro?" e, em outra conversa, "Como faço para o Vuetify abrir sempre no tema claro?". Compare. Depois abra a documentação oficial do Vuetify e confira qual das duas respostas casa com a opção `defaultTheme` de `createVuetify`. Guarde as duas respostas: elas são o material do desafio ⭐⭐.

### 5.2 Pacote que não existe

Peça uma funcionalidade específica e é comum vir um `npm install nome-plausivel-qualquer`. Antes de instalar qualquer pacote sugerido:

```bash
npm view express-validator version
npm view pacote-que-a-ia-sugeriu version
```

Se o pacote não existe, o npm responde com clareza:

```text
npm error code E404
npm error 404 Not Found - GET https://registry.npmjs.org/pacote-que-a-ia-sugeriu
npm error 404  'pacote-que-a-ia-sugeriu@*' is not in this registry.
```

Se existe, olhe três números antes de instalar: downloads por semana, data da última publicação (no site do npm) e número de dependências. Um pacote com 12 downloads semanais para uma tarefa comum é bandeira vermelha — pode ser o nome que o modelo inventou e alguém registrou. E rode `npm audit` depois de qualquer instalação nova.

### 5.3 Código plausível e inseguro

Este é o mais perigoso porque **funciona**. O código roda, o teste manual passa, e o problema só aparece quando alguém mal-intencionado chega. Os cinco que mais aparecem em projetos autorais gerados com ajuda de IA:

- `cors()` sem opção nenhuma, liberando qualquer origem, em uma API com sessão.
- Consulta SQL montada por concatenação, como na §4.2.
- Chave `service_role` do Supabase no front-end "porque assim funciona sem configurar policy".
- Senha ou token aparecendo no `console.log` de depuração que ficou no código.
- Verificação de autorização feita **no front** (esconder o botão) e não na rota da API.

Nenhum desses é pegado por um teste de caminho feliz. Todos são pegados por uma pergunta explícita no prompt de revisão — "procure problemas de segurança e diga como reproduzir cada um" — seguida da reprodução com `curl`.

## 6. O que nunca entra em um prompt

Tudo que você cola em um assistente sai do seu computador. Dependendo do serviço e do plano, o conteúdo pode ser guardado, revisado por pessoas ou usado para treinar modelos futuros. Trate a caixa de texto como um **post público**.

| Nunca cole | Por quê | O que fazer no lugar |
|---|---|---|
| `.env`, senhas, `DATABASE_URL` | Vaza credencial de produção | Cole só os **nomes** das variáveis |
| Chave de API, token, `service_role` | Uso indevido imediato da sua conta | Substitua por `CHAVE_AQUI` |
| Dados pessoais reais (CPF, telefone, e-mail de gente de verdade) | LGPD: você é o controlador desses dados | Gere dados fictícios |
| Código sob contrato do estágio | Pode violar o contrato do seu trabalho | Reescreva um exemplo mínimo equivalente |
| Prova, processo seletivo ou material sob sigilo (seu ou de outra pessoa) | Confidencialidade não é sua para compartilhar | Nada substitui; simplesmente não cole |

Como redigir um trecho antes de colar, sem perder o contexto:

```js
// unieventos-api/src/db/pool.js — versão segura para colar em um prompt
import mysql from 'mysql2/promise';

export const pool = mysql.createPool({
  host: process.env.DB_HOST,          // valor real: um hostname da nuvem
  user: process.env.DB_USER,          // valor real: um usuário da aplicação
  password: process.env.DB_PASSWORD,  // valor real: senha forte, não colada aqui
  database: process.env.DB_NAME,
  waitForConnections: true,
  connectionLimit: 10
});
```

Repare: o código continua completo e o assistente entende tudo o que precisa. O que ele não recebe é o valor.

> **⚠️ Atenção**
> Se um segredo escapar — para o chat, para um commit ou para um print compartilhado com outras pessoas — a única correção é **rotacionar**: gere uma chave nova no painel do serviço, invalide a antiga, atualize o `.env` local, os secrets do GitHub Actions e o servidor. Apagar a mensagem não resolve, e reverter o commit não resolve: o valor continua no histórico do Git. O GitHub ajuda com a proteção de push, que recusa o envio com uma mensagem parecida com esta:
>
> ```text
> remote: - GITHUB PUSH PROTECTION
> remote:   Push cannot contain secrets
> remote:   —— Supabase Service Key ————————————————————
> remote:    locations:
> remote:      commit: 8a1f3c2
> ```

## 7. Verificar é o trabalho: o protocolo dos cinco passos

Aceitar uma sugestão de IA sem esse ciclo é o equivalente a fazer deploy sem testar. São cinco passos, sempre na mesma ordem, e o quinto é o mais importante.

1. **Reproduza o problema antes.** Se você não sabe demonstrar o defeito, não vai saber demonstrar a correção. Um `curl`, um teste que falha, uma linha no log.
2. **Leia linha a linha.** Toda linha que você não entende é uma pergunta para o assistente ("por que essa linha existe?"), não uma linha para aceitar.
3. **Confira o que é específico na fonte oficial.** Nome de opção, assinatura de função, comportamento de versão: cinco minutos na documentação valem cinco horas de depuração. Assuma que o específico está errado até provar o contrário.
4. **Rode.** `npm run lint`, `npm test`, `curl` na rota, clique na tela. Depois **quebre de propósito** e confirme que o teste falha.
5. **Explique em voz alta, sem olhar.** Feche o editor e conte para um colega — ou para a parede — o que a mudança faz e por quê. Se travar, você não entendeu; volte ao passo 2.

> **📌 Vale gravar**
> O passo 5 não é uma metáfora. A qualquer momento — um colega perguntando, uma entrevista técnica, ou você mesmo relendo o código em seis meses — alguém pode apontar uma linha e pedir a explicação. Você pode ter usado IA para escrevê-la, mas precisa saber dizer o que ela faz, por que está ali e o que aconteceria se fosse removida. Saber explicar o próprio código é o que separa quem aprendeu de quem colou.

## 8. Dependência: o custo que só aparece depois

Existe um efeito bem documentado no aprendizado: o esforço de recuperar uma informação da memória, e o de errar antes de acertar, são exatamente o que fixa o conhecimento. Ler uma explicação clara dá a **sensação** de aprendizado sem o aprendizado — a chamada fluência ilusória. Um assistente é uma máquina industrial de produzir fluência ilusória: tudo fica claro, tudo parece óbvio, e três dias depois você não consegue escrever a mesma rota sozinho.

Isso não é argumento para não usar. É argumento para usar **em uma ordem específica**:

- **Regra dos 15 minutos.** Tente sozinho por 15 minutos antes de perguntar. Se resolver, você ganhou a habilidade. Se não, você chega ao prompt com um diagnóstico — e o prompt fica muito melhor.
- **Regra do rascunho.** Escreva a sua versão primeiro, ainda que feia, e só depois peça revisão. Comparar a sua solução com a dele ensina; receber a dele pronta, não.
- **Regra do fechamento.** Ao fim de cada tarefa em que você usou IA, refaça de memória a parte central, com o editor fechado. Leva dois minutos e converte a leitura em prática.
- **Zona sem IA.** Escolha uma área para aprender na mão neste semestre — para muita gente, é CSS de layout ou a lógica assíncrona. Sem autocompletar, sem chat.

> **🧠 Você sabia?**
> Quando o ChatGPT surgiu, o Stack Overflow proibiu respostas geradas por IA no site. O motivo declarado não foi a qualidade média — era razoável — e sim a **taxa de acerto combinada com a facilidade de produção**: respostas erradas passaram a chegar mais rápido do que voluntários conseguiam revisar. É o mesmo problema em escala pessoal: a IA gera código mais rápido do que você revisa. Quem não impõe um limite de revisão acumula dívida técnica em velocidade recorde.

## 9. Como usar IA sem enganar a si mesmo

Não existe fiscal aqui, e este material não tem nota. O motivo para ter uma política pessoal de uso de IA não é evitar punição — é que só você paga o preço de aprender de mentirinha. Um projeto que "funciona" mas que você não sabe explicar não te prepara para a próxima vaga, para a próxima entrevista técnica, ou para o próximo bug que a IA não vai resolver sozinha.

A regra que resume tudo isto: **use IA para explicar, não para entregar o que você não sabe explicar.** Pedir para o assistente destrinchar um erro, revisar um trecho, sugerir testes, ensinar uma API nova — isso é estudo, e é o uso incentivado ao longo deste capítulo. Colar uma resposta pronta num projeto e seguir em frente sem entender por que ela funciona não é estudo: é adiar o problema para o momento em que você mais precisar da habilidade que pulou.

| Situação | Ajuda a aprender? | Por quê |
|---|---|---|
| Pedir explicação de um erro e corrigir entendendo | Sim | O melhor uso; recomendado |
| Gerar testes, revisar e completar com casos seus | Sim | Verifique quebrando de propósito |
| Gerar o `README` a partir de fatos do repositório | Sim | Revise; ele inventa funcionalidade |
| Colar código do assistente sem entender | Não | Na próxima vez que precisar mexer ali, você vai travar |
| Pedir para alguém (ou uma IA) terminar o seu projeto autoral por você | Não | O projeto para de ser seu; a habilidade que ele deveria treinar não aparece |
| Colar `.env` ou dado pessoal real no chat | Não | Incidente de segurança; rotacione a chave |

Duas práticas que fazem essa política funcionar de verdade, sem precisar de ninguém cobrando:

1. **Registre o uso.** Um arquivo `IA.md` na raiz do projeto (modelo no Passo a passo) dizendo em que partes você usou assistente, o que aceitou e o que recusou — guarde-o no seu próprio repositório. Não é para prestar contas a ninguém: é um espelho. Escrever obriga você a notar o que realmente aconteceu, e reler daqui a um mês mostra se você está aprendendo ou só acelerando a entrega.
2. **Teste-se de vez em quando.** Feche o editor e explique em voz alta — para um colega, ou para a parede — o que uma parte do seu código faz e por que está ali. Se travar, você ainda não entendeu; volte ao passo 2 do protocolo da §7. Ninguém vai te arguir por isso, mas o dia em que alguém perguntar — numa entrevista, numa vaga, numa dúvida sua mesmo — é o dia em que essa prática se paga.

> **💡 Dica**
> Ajudar um colega a entender um problema é ótimo — é assim que se aprende em grupo. Entregar o arquivo pronto para ele é outra coisa: você tira dele exatamente o exercício que o projeto deveria proporcionar. Se dois projetos autorais chegam com a mesma estrutura de pastas, os mesmos nomes de variável e os mesmos comentários, vale perguntar a si mesmo quem realmente escreveu aquilo — e se alguém aprendeu o que deveria.

## 🚀 Passo a passo — Revisão assistida do projeto autoral, com tudo verificado

Ao final destes passos o seu projeto autoral terá **três problemas reais corrigidos** (cada um com o commit que prova a correção), **uma suíte de testes** que falha quando o código quebra, um **`README.md`** que descreve o que existe de verdade e um **`IA.md`** registrando como a IA foi usada.

Está no **Nível 2**? Aplique o mesmo passo na `cafe-cerrado-api`: o projeto autoral pode ser o Café Cerrado estendido, e todo o roteiro — contexto, revisão, teste, commit — vale sem alteração.

### Passo 1 — Preparar o terreno

```bash
cd seu-projeto-autoral
git status
git switch -c revisao-assistida
npm run lint
npm test
```

O `git status` precisa estar limpo: a partir daqui, tudo que aparecer em `git diff` é mudança sua ou proposta da IA, e você quer conseguir distinguir. Se `npm run lint` ou `npm test` já falham, corrija antes — você não vai conseguir avaliar sugestão nenhuma com a base quebrada.

Escolha o recorte: **uma rota da API que grava dados** e **um componente do front que consome essa rota**. Não peça revisão do projeto inteiro; resposta genérica é o que se ganha com prompt genérico.

### Passo 2 — Pedir a revisão, com contexto completo

Monte o prompt com os seis elementos da §3. Modelo, adapte aos seus arquivos:

```text
Você é um revisor de código experiente em Node e Vue. Não elogie o código.
Objetivo: encontrar problemas reais nesta rota e neste componente.

Stack: Node 22 LTS, Express 5.1, mysql2 3 (mysql2/promise, createPool),
Vue 3.5 com <script setup>, Vuetify 4, Pinia 4, axios 1.19 com axios.create.

Para cada problema encontrado, responda nesta ordem:
1. arquivo e trecho exato
2. por que é problema (uma frase)
3. como eu reproduzo o problema (comando curl ou passo na tela)
4. a correção, com o arquivo inteiro corrigido
5. o link da documentação oficial que sustenta a correção

Ordene do mais grave para o menos grave. Se faltar informação, pergunte
antes de supor.

Arquivo 1 — src/rotas/<sua-rota>.js:
[cole o arquivo inteiro]

Arquivo 2 — src/components/<SeuComponente>.vue:
[cole o arquivo inteiro]
```

### Passo 3 — Triagem: transformar a resposta em lista verificável

Crie `ACHADOS.md` na raiz e transcreva **cada** achado, um por linha, antes de mexer em qualquer código. Escrever a lista força você a separar o que é problema do que é opinião de estilo.

```markdown
# Achados da revisão assistida

| # | Achado (em uma linha) | Situação |
|---|---|---|
| 1 | INSERT montado por concatenação: injeção de SQL | a verificar |
| 2 | Nenhuma validação do corpo: grava "undefined" | a verificar |
| 3 | Componente não trata erro do axios: tela em branco | a verificar |
| 4 | Sugere instalar express-async-errors | a verificar |
| 5 | Sugere usar align="center" em v-row | a verificar |
```

### Passo 4 — Verificar cada achado, um por um

Esta é a etapa que separa este capítulo de "pedir código para a IA". Para cada linha da tabela, aplique o protocolo da §7 e mude a coluna **Situação** para `confirmado`, `falso` ou `estilo`:

```bash
# achado 1: reproduzir a injeção antes de corrigir
curl -i -X POST http://localhost:3000/api/inscricoes \
  -H "Content-Type: application/json" \
  -d '{"eventoId":1,"nome":"O'\''Brien","email":"teste@exemplo.com"}'

# achado 2: reproduzir a falta de validação
curl -i -X POST http://localhost:3000/api/inscricoes \
  -H "Content-Type: application/json" -d '{"eventoId":1}'

# achado 4: conferir se o pacote é mesmo necessário nesta versão
npm view express-async-errors version
node -e "console.log(require('express/package.json').version)"
```

No exemplo acima, o achado 4 é **falso**: o Express 5 já captura erros de handlers `async` sozinho, então o pacote é dispensável. O achado 5 também é **falso** para nós: no Vuetify 4 o alinhamento de `v-row` é feito por classes utilitárias. Marcar os dois como falsos e escrever o motivo no `ACHADOS.md` vale tanto quanto corrigir os verdadeiros — é a prova de que você revisou o revisor.

### Passo 5 — Corrigir os três problemas confirmados

Um commit por problema, cada um com a mensagem escrita a partir do diff (§4.4):

```bash
git add src/rotas/inscricoes.js
git commit -m "fix(inscricoes): usa placeholders do mysql2 na consulta"
npm test

git add src/rotas/inscricoes.js
git commit -m "fix(inscricoes): valida corpo e responde 400 com mensagem clara"
npm test

git add src/components/FormularioInscricao.vue
git commit -m "fix(inscricao): mostra mensagem de erro quando a API falha"
npm run lint
```

Depois de cada correção, **repita o `curl` do Passo 4**. A mesma requisição que reproduzia o problema agora precisa responder 400, 404 ou 201 — nunca 500.

### Passo 6 — Gerar os testes e endurecê-los

Peça a suíte com o prompt da §4.3, rode e então faça o teste de mutação, que é o passo que quase ninguém faz:

```bash
npm test
```

Agora quebre o código de propósito, em três lugares diferentes, e rode de novo:

```bash
# 1. afrouxe a validação: troque length < 3 por length < 0 e rode
npm test
# 2. troque res.status(201) por res.status(200) e rode
npm test
# 3. remova a checagem de evento inexistente e rode
npm test
```

Cada mutação precisa fazer **pelo menos um teste falhar**. Se alguma passar, o teste correspondente é decorativo: aperte a asserção (compare o corpo, não só o status) e repita. Desfaça as três mutações no fim (`git checkout -- .` se você não commitou nada) e confirme que `npm test` volta a passar inteiro.

### Passo 7 — `README.md` a partir de fatos

Colete os fatos e use o prompt da §4.4:

```bash
cat package.json
cat .env.example
grep -rn "rotasApp.use\|router\." src/rotas | head -20
ls src/components
```

Responda às perguntas entre colchetes que vierem na resposta, apague as que não se aplicam e confira uma a uma as instruções de execução: **rode o seu próprio `README` do zero**, em um clone novo, seguindo apenas o que está escrito.

```bash
cd /tmp
git clone https://github.com/seu-usuario/seu-projeto.git teste-readme
cd teste-readme
```

Se travar em algum passo, o `README` está errado — não a sua memória. Corrija o `README`.

### Passo 8 — Registrar o uso em `IA.md`

```markdown
# Uso de IA neste projeto

Assistentes usados: [nome do chat] para revisão e testes; [nome] no editor
para autocompletar rotas repetidas.

## Onde usei

- Revisão da rota POST /api/inscricoes e do FormularioInscricao.vue.
- Geração da primeira versão de tests/inscricoes.test.js.
- Primeira versão deste README.

## O que aceitei (e verifiquei)

- Uso de placeholders no mysql2: reproduzi a injeção com curl antes e depois.
- Validação do corpo com 400: coberta por dois testes.
- Tratamento de erro do axios no componente: testado com a API desligada.

## O que recusei

- Instalar express-async-errors: o Express 5 já captura erro em handler async.
- Usar align="center" em v-row: no Vuetify 4 isso é classe utilitária.
- Sugestão de guardar a chave do Supabase no front: seria vazamento.

## O que escrevi sem IA

- Toda a modelagem do banco e as regras de negócio do projeto.
- O componente de listagem e o filtro de busca.
```

Comite tudo e abra o pull request:

```bash
git add ACHADOS.md IA.md README.md
git commit -m "docs: registra revisão assistida, achados e uso de IA"
git push -u origin revisao-assistida
gh pr create --title "Revisão assistida do projeto autoral" \
  --body "Três problemas confirmados e corrigidos; testes endurecidos; README e IA.md."
```

### Como conferir

1. `gh pr view --web` mostra o pull request com pelo menos quatro commits, um por correção mais o de documentação.
2. `ACHADOS.md` tem toda linha com situação `confirmado`, `falso` ou `estilo` — nenhuma como `a verificar` — e os falsos têm o motivo escrito.
3. `npm test` passa; e, com qualquer uma das três mutações do Passo 6, falha.
4. Os `curl` que reproduziam os problemas agora respondem 201, 400 e 404, conforme o caso.
5. Você consegue explicar, sem olhar o editor, o que cada uma das três correções faz.

**Resultado esperado:** um pull request em que dá para ver a IA sendo usada como revisora e você sendo o autor — problemas reproduzidos, correções testadas e duas sugestões erradas recusadas com justificativa.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Explique em duas frases por que um assistente pode descrever com total segurança uma função que não existe. Depois diga qual dos seis elementos do prompt (§3) mais reduz esse risco e por quê.

**A2.** Classifique cada prompt como bom ou ruim e diga qual elemento falta em cada ruim: (a) "corrige meu css"; (b) "No Vue 3.5 com script setup e Vuetify 4, meu v-data-table não mostra os itens; segue o componente inteiro e o JSON que a API devolve"; (c) "melhor jeito de fazer login"; (d) "Node 22, Express 5: `TypeError: app.del is not a function` na linha 14 de src/rotas/eventos.js, arquivo colado abaixo; o que mudou?".

**A3.** Um assistente respondeu com `firebase.auth().signInWithEmailAndPassword(email, senha)`. Diga o que está errado, qual seria a forma correta na versão que usamos e em que página da documentação oficial você confirmaria isso.

**A4.** Destes itens, quais podem ir para um prompt e quais não podem — justifique cada um: o trecho de uma rota; o conteúdo do `.env`; a mensagem de erro do terminal; a `DATABASE_URL` de produção; o `.env.example`; a lista de nomes reais dos inscritos no seu evento de teste.

**A5.** A IA sugeriu `npm install express-async-errors` para o seu projeto Express 5 e `npm install body-parser` para ler JSON. Diga se cada uma é necessária, por quê, e escreva o comando que confirma a sua resposta sem instalar nada.

### Nível B — Aplicação

**B1.** Pegue um bug real do seu projeto e escreva dois prompts sobre ele: um preguiçoso (uma linha) e um completo (os seis elementos da §3). Use conversas separadas e registre quanto tempo passou até você ter uma correção que funciona em cada caso.

Resultado esperado: um trecho no seu `IA.md` com os dois prompts, os dois tempos e uma frase dizendo qual elemento fez mais diferença.

<details><summary>Dica</summary>

Cronometre de verdade, com o relógio do celular. O tempo do prompt completo inclui o tempo de escrevê-lo — é justamente esse o custo que você quer medir, e ele costuma se pagar já na primeira rodada.
</details>

**B2.** Caça à alucinação. Faça cinco perguntas específicas de versão ao assistente (uma de Express 5, uma de Vuetify 4, uma de Firebase modular, uma de Supabase com RLS, uma de swagger-jsdoc) e confira cada resposta na documentação oficial.

Resultado esperado: uma tabela de cinco linhas com pergunta, resposta da IA e veredito (`confere` ou `errado`, com o link da doc). É normal aparecerem duas ou três erradas.

<details><summary>Dica</summary>

Perguntas que rendem: "como capturo erro de handler async no Express 5?", "qual a opção do createVuetify para o tema padrão?", "como faço login por e-mail no firebase 12?", "por que meu select do Supabase devolve array vazio sem erro?", "qual a chave de configuração do swagger-jsdoc 6?".
</details>

**B3.** Peça ao assistente testes para uma função de regra de negócio sua (cálculo de vagas restantes, validação de inscrição, formatação). Rode, depois quebre a função de propósito em dois lugares e rode de novo.

Resultado esperado: cada mutação derruba pelo menos um teste. Se alguma mutação passa, você aperta a asserção e mostra o antes e o depois do arquivo de teste.

<details><summary>Dica</summary>

Asserção frouxa típica: `assert.ok(resultado)` — verdadeira para qualquer número diferente de zero. Troque por `assert.equal(resultado, 12)`. Outra: verificar só o status HTTP e ignorar o corpo da resposta.
</details>

**B4.** Peça uma revisão **só de segurança** de uma rota sua que grava dados, no formato da §4.2, e reproduza cada achado com `curl` antes de corrigir.

Resultado esperado: para cada achado confirmado, dois comandos `curl` no seu `ACHADOS.md` — o que demonstrava o problema e o mesmo comando depois da correção, com o novo status.

<details><summary>Dica</summary>

Use `curl -i` para ver o status e os cabeçalhos. Para testar injeção, um apóstrofo dentro de um campo de texto já basta: se a resposta for 500 com erro de sintaxe SQL, o problema está confirmado.
</details>

### Nível C — Desafio

**C1.** O trecho abaixo foi gerado por um assistente e "funciona". Encontre **quatro** problemas **sem usar IA**, em no máximo dez minutos. Depois peça a revisão ao assistente e compare: quantos ele achou, quantos você achou, e se ele inventou algum que não existe.

```js
// api/src/app.js — versão gerada por assistente, com problemas
import express from 'express';
import cors from 'cors';
import { createClient } from '@supabase/supabase-js';

const app = express();
app.use(cors({ origin: '*', credentials: true }));
app.use(express.json());

const supabase = createClient(
  'https://abcdefgh.supabase.co',
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.chave-de-servico-colada-aqui'
);

app.post('/api/login', async (req, res) => {
  const { email, senha } = req.body;
  console.log('tentativa de login', email, senha);
  const { data, error } = await supabase
    .from('usuarios')
    .select('id, nome, papel')
    .eq('email', email)
    .eq('senha', senha);
  if (error) return res.status(500).json({ erro: error.message });
  res.json({ usuario: data[0], admin: data[0]?.papel === 'admin' });
});

app.listen(3000);
```

<details><summary>Dica</summary>

Olhe nesta ordem: (1) o que `origin: '*'` combinado com `credentials: true` significa e por que os navegadores recusam essa combinação; (2) o que está sendo impresso no log e onde esse log vai parar em produção; (3) que tipo de chave do Supabase está no código e o que alguém faz com ela se ler o repositório; (4) como as senhas estão sendo comparadas e o que deveria estar guardado na coluna; (5) de bônus, o que acontece quando `data` vem vazio e por que a resposta ainda assim é 200.
</details>

## 🏆 Desafios

### ⭐ Caderno de bordo da IA
Tags: ia, projeto, investigacao

Você provavelmente não faz ideia de quanto do seu código vem de sugestão aceita sem leitura. Ninguém faz — e é justamente por isso que a conta assusta quando aparece. Durante uma semana de trabalho no projeto autoral, registre **toda** interação com assistente e transforme isso em número.

**Critérios de pronto**

- Um arquivo `IA.md` com no mínimo 10 interações registradas, cada uma com: o que você pediu, se aceitou, e o que fez para verificar.
- Uma coluna dizendo se a sugestão foi aceita sem mudança, aceita com mudança ou recusada — e o total de cada categoria.
- Pelo menos duas recusas com o motivo técnico escrito (não "não gostei").
- Um parágrafo final respondendo: em qual tipo de tarefa a taxa de aceitação foi maior, e por que você acha que foi.
- O arquivo está commitado no repositório do projeto autoral.

<details><summary>Pistas</summary>

1. Registre na hora, em três linhas. Reconstituir de memória no fim da semana produz um relato bonito e falso.
2. Separe por tipo de tarefa: explicar erro, gerar código novo, revisar, documentar. As taxas são bem diferentes entre elas.
3. "Verifiquei" precisa ser um ato: rodei o teste, abri a doc, reproduzi com `curl`. Se a verificação foi "pareceu certo", registre exatamente isso — é um dado honesto.
4. Este é o tipo de registro que fecha bem o Marco final da sua trilha.
</details>

### ⭐⭐ Placar do caça-alucinação
Tags: ia, investigacao, testes

Quem consegue medir uma ferramenta para de discutir sobre ela. Monte uma bateria de perguntas cuja resposta certa está na documentação oficial das versões que usamos, aplique em **dois** assistentes diferentes e publique o placar.

**Critérios de pronto**

- 10 perguntas específicas de versão, cobrindo pelo menos quatro tecnologias diferentes desta trilha (Express 5, Vuetify 4, Firebase modular, Supabase com RLS, mysql2, swagger-jsdoc, Vite, Pinia).
- Um gabarito escrito **antes** de perguntar, cada resposta com o link da documentação oficial que a sustenta.
- As respostas dos dois assistentes, classificadas em correta, parcialmente correta ou errada, com o critério de classificação declarado.
- Um `PLACAR.md` com a tabela, o total de cada assistente e três frases sobre em que tipo de pergunta os dois erram junto.
- A mesma bateria repetida com a versão explícita no prompt (por exemplo, "Express 5" em vez de "Express"), comparando os dois placares.

<details><summary>Pistas</summary>

1. Perguntas boas têm resposta objetiva e curta: nome de opção, assinatura, valor padrão. "Qual a melhor arquitetura" não dá para pontuar.
2. Escreva o gabarito primeiro. Ler a resposta da IA antes do gabarito contamina o seu julgamento — o efeito é forte e você não percebe acontecendo.
3. Repare no padrão: erros costumam se concentrar no que mudou de versão recentemente. Isso é uma previsão testável do seu relatório.
4. Para a comparação final, mude **só** a menção de versão no prompt. Qualquer outra mudança invalida a comparação.
</details>

### ⭐⭐⭐ Revisor de segurança do seu projeto
Tags: ia, seguranca, testes, projeto

Toda API construída nesta trilha tem pelo menos uma falha de segurança real. A sua também. Use o assistente como um revisor incansável, mas prove cada coisa: aqui, um problema só conta depois que você escreveu o teste que **falha** por causa dele.

**Critérios de pronto**

- Uma revisão de segurança de todas as rotas que gravam ou apagam dados, guiada por prompts com o formato da §4.2.
- Para cada achado confirmado, um teste automatizado que **falha** no código atual e **passa** depois da correção — commitados nessa ordem (teste primeiro, correção depois).
- No mínimo três falhas reais corrigidas, entre: injeção de SQL, falta de autorização na rota, CORS permissivo demais, segredo no repositório, dado pessoal exposto na resposta, ausência de validação de entrada.
- Um achado **refutado** com justificativa técnica e o link da documentação: você discordou do revisor e provou por quê.
- Um `SEGURANCA.md` de no máximo uma página com o que foi corrigido, o que ficou de fora e por quê.
- `npm test` e `npm run lint` passando no CI do Capítulo 09, com a branch protegida.

<details><summary>Pistas</summary>

1. Comece pelas rotas de escrita e pelas que retornam dados de outra pessoa — é onde mora quase toda falha de autorização.
2. Um teste de autorização precisa de dois usuários: um dono do recurso e um intruso. O intruso precisa receber 403, não 200 com o dado.
3. Para segredo no histórico do Git, o `git log -p -S "eyJ"` acha a linha que introduziu uma chave em formato JWT. Achou, rotacione a chave.
4. Não peça "torne meu código seguro". Peça "liste como um atacante exploraria cada rota, em ordem de facilidade" — a resposta fica muito mais concreta e testável.
</details>

### 🔥 Boss — Tudo no ar, medido e defensável
Tags: deploy, ci-cd, ia, seguranca, projeto

Este é o encerramento da trilha, e ele é simples de enunciar: o seu projeto autoral, inteiro, funcionando na internet, com tudo o que os onze capítulos ensinaram — e você capaz de defender cada decisão em dez minutos, sem consultar nada. Não é um exercício novo; é a prova de que os anteriores viraram sistema.

**Critérios de pronto**

- Front publicado em HTTPS com domínio ou subdomínio próprio, e API publicada (Render, VPS com nginx ou contêiner), conversando entre si com CORS restrito à origem do front.
- Banco em serviço gerenciado, com backup gerado por você e uma restauração testada de verdade em uma base vazia.
- CI no GitHub Actions rodando lint e testes a cada pull request, com a branch `main` protegida, e deploy automatizado a cada merge.
- Lighthouse do site publicado com Performance e Accessibility em 90 ou mais no modo Mobile, e os dois relatórios (antes e depois) no repositório.
- Monitoramento ativo: erros no Sentry, `/health` vigiado por um serviço de uptime e pelo menos um alerta recebido.
- `README.md` que um estranho consegue seguir do clone ao servidor rodando, `IA.md` declarando o uso de assistentes e `SEGURANCA.md` com as falhas corrigidas.
- Nenhum segredo no repositório: `git log -p -S "SUPABASE" | head -50` e a proteção de push do GitHub limpas.
- Uma apresentação de 10 minutos, sem slides prontos, navegando pelo repositório e pelo sistema no ar, respondendo a três perguntas sobre linhas escolhidas por outra pessoa — quem te orienta, um colega ou alguém do seu grupo de estudos. Estudando sozinho? Peça para alguém sortear três números de linha do seu `git diff` (ou use um gerador aleatório) e explique exatamente essas linhas, sem ensaio prévio.

<details><summary>Pistas</summary>

1. Faça na ordem inversa da entrega: comece pelo que quebra em produção (variáveis de ambiente, CORS, banco) e deixe a maquiagem por último.
2. Teste a restauração do backup em uma base nova e vazia. Backup nunca restaurado não é backup — é um arquivo.
3. Ensaie a apresentação com outra pessoa escolhendo as linhas por você, não você mesmo. Escolher as próprias linhas esconde exatamente os trechos que você não entende.
4. Se alguma linha do seu código só existe porque a IA escreveu e você não sabe explicar, apague e reescreva. Uma linha a menos que você entende vale mais do que dez que você defende mal.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `TypeError: Cannot destructure property 'nome' of 'req.body' as it is undefined` | Código gerado sem `express.json()`; no Express 5 `req.body` é `undefined`, não `{}` | `app.use(express.json())` antes das rotas; ou `const { nome } = req.body ?? {}` |
| `TypeError: app.del is not a function` | Sugestão em sintaxe do Express 4 | Use `app.delete()`; sempre informe "Express 5" no prompt |
| `Error: Cannot find module 'body-parser'` | A IA mandou instalar um pacote que virou nativo | `express.json()` e `express.urlencoded()` já vêm no Express; remova a dependência |
| `TypeError: firebase.auth is not a function` | Resposta com a API de namespace, anterior à modular | `import { getAuth, signInWithEmailAndPassword } from 'firebase/auth'` |
| `npm error code E404` … `is not in this registry` | Nome de pacote alucinado | Confira com `npm view <pacote> version` antes de instalar; procure alternativa real |
| `Error: ER_PARSE_ERROR: You have an error in your SQL syntax` ao gravar um nome com apóstrofo | SQL montado por concatenação (o mesmo defeito que permite injeção) | Placeholders `?` do `mysql2` e valores no array de parâmetros |
| A consulta do Supabase devolve `data: []` e `error: null`, mas há linhas na tabela | RLS habilitado sem policy; o código gerado esqueceu a policy | Crie a policy de `select` no painel; nunca use a chave de serviço no front |
| `Access to fetch … has been blocked by CORS policy` depois de publicar | `cors()` local aberto, produção com origem diferente | Configure `origin` com a URL do front publicado; nada de `origin: '*'` com credenciais |
| `SyntaxError: Cannot use import statement outside a module` | Resposta em ESM colada em projeto CommonJS (ou o contrário) | Declare `"type": "module"` no `package.json` ou peça a resposta em CommonJS |
| A documentação do Swagger sobe vazia, sem erro | Resposta usando `swaggerDefinition`, chave da versão antiga | `swagger-jsdoc` 6.x usa `definition` |
| `remote: - GITHUB PUSH PROTECTION` … `Push cannot contain secrets` | Chave colada no código pela IA ou por você, e commitada | Rotacione a chave no painel do serviço, tire do código, use `.env` e secrets |
| Todos os testes gerados passam, mesmo com o código quebrado de propósito | Asserções frouxas (`assert.ok`) e nenhum caso de erro | Compare valores exatos e corpo da resposta; teste de mutação como no Passo 6 |
| `npm error code ERESOLVE` ao instalar o que a IA sugeriu | Versões incompatíveis inventadas no `package.json` | Instale sem fixar versão (`npm install pacote`) e deixe o npm resolver; não force `--legacy-peer-deps` sem entender |
| O componente Vue some da tela depois de uma refatoração do agente | Mudança ampla aceita sem ler o diff | `git diff` antes de aceitar; `git reset --hard` para o commit-âncora e refaça em pedaços |

## 🏠 Para praticar depois da aula (1 h)

No repositório do seu **projeto autoral**:

1. Rode o Passo a passo completo em **uma** rota de escrita e **um** componente que a consome. Entregue o `ACHADOS.md` com todos os itens resolvidos (`confirmado`, `falso` ou `estilo`) e nenhum como `a verificar`.
2. Corrija os três problemas confirmados, um commit por problema, com mensagem no padrão Conventional Commits gerada a partir do diff e revisada por você.
3. Gere a suíte de testes da rota, rode o teste de mutação em dois pontos do código e ajuste as asserções frouxas que aparecerem.
4. Escreva o `README.md` a partir de fatos do repositório e valide clonando em outra pasta e seguindo apenas o que está escrito.
5. Escreva o `IA.md` no formato do Passo 8, incluindo pelo menos duas sugestões **recusadas** com o motivo técnico.

**Critério de pronto:** existe um pull request com quatro ou mais commits; `npm test` passa e falha quando você quebra o código de propósito; `ACHADOS.md` tem pelo menos um achado marcado como `falso` com justificativa; o `README` funciona em um clone limpo; o `IA.md` está na raiz.

**Guarde no seu repositório:** commit + push, com o link do pull request na descrição.

## ✅ Está no ar quando…

- [ ] O repositório do projeto autoral tem `IA.md` na raiz, declarando onde você usou assistente, o que aceitou e o que recusou.
- [ ] `ACHADOS.md` registra a revisão assistida com cada item classificado e nenhum pendente.
- [ ] Pelo menos três problemas reais foram corrigidos, cada um com o seu commit e com o `curl` (ou passo na tela) que reproduzia o problema antes.
- [ ] Pelo menos uma sugestão da IA foi **recusada** com justificativa técnica e link da documentação oficial.
- [ ] `npm test` passa, e falha quando você quebra a regra de negócio de propósito em qualquer um de três pontos.
- [ ] `npm run lint` passa sem avisos nos dois projetos.
- [ ] O `README.md` foi validado em um clone novo: quem nunca viu o projeto consegue rodá-lo seguindo só o texto.
- [ ] Nenhum segredo entrou no repositório nem em prompt: `git log -p -S "eyJ"` não retorna chaves e o `.env` continua ignorado.
- [ ] Você consegue explicar, sem abrir o editor, o que cada uma das três correções faz e o que aconteceria se fosse removida.

## 📚 Para aprofundar

- [GitHub Docs — Copilot](https://docs.github.com/pt/copilot) — o que a extensão enxerga do seu projeto, como aceitar e recusar sugestões e as configurações de privacidade.
- [OpenAI — Prompt engineering](https://platform.openai.com/docs/guides/prompt-engineering) — o guia oficial de como estruturar instruções; leia a parte sobre dar contexto e delimitar o formato da resposta.
- [Anthropic — Prompt engineering overview](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview) — as mesmas ideias por outro ângulo, com ênfase em exemplos e em pedir raciocínio antes da resposta.
- [Claude Code — documentação](https://docs.claude.com/en/docs/claude-code/overview) — como funciona um assistente que lê e escreve arquivos, e onde ficam os controles de permissão.
- [Cursor — documentação](https://docs.cursor.com/) — o mesmo formato dentro de um editor; leia a parte de contexto e de revisão de diff.
- [GitHub Docs — Sobre a proteção de push](https://docs.github.com/pt/code-security/secret-scanning/introduction/about-push-protection) — o que o GitHub bloqueia, quais provedores ele reconhece e o que fazer quando um segredo vaza.
- [npm Docs — `npm audit`](https://docs.npmjs.com/cli/v10/commands/npm-audit) — como ler o relatório de vulnerabilidades antes de aceitar uma dependência sugerida.
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) — a lista canônica de falhas de aplicação web; use como roteiro do desafio ⭐⭐⭐.
- [Conventional Commits (pt-BR)](https://www.conventionalcommits.org/pt-br/v1.0.0/) — a especificação completa dos tipos `feat`, `fix`, `docs`, `chore` e do corpo da mensagem.
- [Node.js — Test runner](https://nodejs.org/api/test.html) — a referência de `node:test` para endurecer os testes que a IA gerar.
- [Express 5 — Migrating to v5](https://expressjs.com/en/guide/migrating-5.html) — a lista oficial do que mudou; é a página que refuta metade das sugestões desatualizadas.
- [Lei Geral de Proteção de Dados (Lei 13.709)](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm) — o texto oficial; leia os artigos 5º e 6º para entender o que é tratamento de dado pessoal, que é o que você faz ao colar um cadastro real em um chat.

---

Aqui termina a trilha **Deploy & Ferramentas**. Você começou montando a bancada — terminal, editor, Node — e passou por versionamento, publicação de sites estáticos, domínio e HTTPS, back-end em PaaS, servidor próprio com nginx, contêineres, banco na nuvem, integração contínua, qualidade e observabilidade. Cada capítulo colocou algo real no ar, e o conjunto é o ciclo completo do ofício: escrever, versionar, publicar, medir e revisar.

Este último capítulo fecha o ciclo com a única coisa que nenhuma ferramenta faz por você — responder pelo que está no ar. Um assistente escreve rápido; quem entende do sistema é você. Continue: mantenha os projetos publicados vivos, volte ao Banco de Desafios quando faltar o que fazer, e trate cada linha que você não sabe explicar como uma linha que ainda não é sua.
