# Aula 07 — Introdução ao Firebase, Node.js e Express

> **Nível 3 — Frameworks Modernos** · Unidade 3: Integração front-end/back-end
> WebLab · UNEMAT Sinop · Prof. Ivan Luiz Pedroso Pires

Na Aula 06 você conectou o UniEventos a uma API falsa com `json-server`, encapsulou as chamadas numa instância dedicada do Axios e organizou o estado global com Pinia. O front-end ficou pronto para conversar com um back-end de verdade. A partir de hoje ele existe — e você é quem vai escrevê-lo.

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- explicar por que uma aplicação séria não pode viver só no navegador, e o que precisa acontecer do lado do servidor;
- descrever o que é o Node.js, como funciona seu event loop e por que ele é adequado para servidores web;
- diferenciar módulos CommonJS de ES Modules e configurar um projeto Node com `"type": "module"`;
- criar um projeto no Firebase, obter as credenciais do app web e ler/escrever documentos no Firestore com o SDK modular;
- explicar o que é um BaaS (*Backend as a Service*) e quando ele resolve — e quando não resolve — o problema de back-end;
- subir um servidor Express 5 mínimo, com CORS e rotas JSON, evitando as armadilhas de sintaxe do Express 4;
- apontar o front-end UniEventos para uma API Express real, no lugar do `json-server`.

## 📋 Pré-requisitos desta aula

- [ ] Front-end `unieventos-web` da Aula 06 rodando localmente com `npm run dev`, consumindo `json-server` via instância Axios dedicada.
- [ ] Store Pinia de eventos funcionando (estado, `carregando`, `erro`).
- [ ] Node.js 22.x instalado (`node -v`). Se você tem outra versão, use `nvm install 22 && nvm use 22`.
- [ ] Conta Google para criar o projeto no console do Firebase.
- [ ] VS Code com a extensão **REST Client** ou **Thunder Client** instalada (vamos usar hoje).
- [ ] Terminal com `curl` disponível (já vem no Linux/macOS; no Windows use o `curl` do PowerShell ou WSL).
- [ ] Editor com abas suficientes para acompanhar dois projetos abertos ao mesmo tempo (`unieventos-web` e, a partir de hoje, `unieventos-api`).
- [ ] Duas janelas de terminal livres — uma para cada projeto rodando simultaneamente.

> **⚠️ Atenção**
> Muito tutorial de Express na internet — inclusive vídeos recentes — ainda usa a sintaxe do Express 4. A partir de hoje você trabalha com o Express **5.2.1**, que já é o padrão de instalação (`npm install express` traz a v5). Este material tem uma seção inteira (§5) só sobre isso. Leia com atenção antes de copiar código de fora.

Retomando rapidamente onde a Aula 06 parou: você tem hoje um front-end Vue com Vuetify, Router e Pinia, consumindo dados de um `json-server` através de uma instância Axios dedicada, com interceptors e uma camada `src/services/`. Essa arquitetura de consumo não muda — o que muda, a partir de agora, é o que está do outro lado da rede.

Duas frentes novas se abrem hoje, e vamos alternar entre elas: primeiro o Node.js e o Firebase (uma introdução rápida a um back-end pronto), depois o Express (o back-end que você mesmo escreve, e que vai crescer pelo resto do semestre).
## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Por que back-end existe; arquitetura cliente-servidor; Node.js e seu modelo de execução |
| 2 | 50 min | BaaS vs API própria; criação do projeto Firebase; primeira leitura/escrita no Firestore |
| 3 | 50 min | Express 5 na prática: servidor mínimo, rotas, CORS, armadilhas de sintaxe; conectar o front real |

## 1. Por que o front sozinho não basta

Até a Aula 06, o UniEventos rodava inteiro no navegador de quem acessa. O `json-server` simulava uma API, mas ele não impõe nenhuma regra: qualquer pessoa com o DevTools aberto pode alterar o corpo de uma requisição e gravar o que quiser. Isso é aceitável para prototipar, mas não para um sistema real. Três problemas aparecem assim que você tenta ir além do protótipo.

**Segredos não podem ficar no navegador.** Toda variável, toda constante, todo arquivo `.js` que você entrega ao navegador é público — qualquer pessoa pode abrir o DevTools, ver o código-fonte baixado e ler o que está ali. Uma chave de API paga, uma credencial de banco de dados ou uma regra de negócio sigilosa não podem estar no front-end. Elas precisam morar em um ambiente que o usuário não acessa diretamente: o servidor.

**Regras de negócio precisam de um lugar confiável para rodar.** Pense no UniEventos: um evento tem um número de vagas. Se a lógica "não deixar inscrever além do limite de vagas" estiver só no front-end (por exemplo, desabilitando um botão quando `vagas === 0`), basta alguém chamar a API diretamente — pelo `curl`, pelo Postman, por um script — ignorando a interface, para furar a regra. A regra de negócio real precisa ser verificada no servidor, porque é o único lugar que o usuário não controla.

**Integridade e autorização dependem de um árbitro imparcial.** "Este usuário pode editar este evento?" "Este evento realmente existe e tem vaga disponível neste exato momento?" Essas perguntas não podem ser respondidas com confiança por código que roda na máquina do próprio usuário — ele poderia simplesmente alterar a resposta. É preciso um terceiro, fora do alcance do cliente, que centralize a decisão. Esse terceiro é o back-end.

Um jeito direto de sentir isso na prática: abra o DevTools do navegador (F12) numa aplicação Vue rodando com `npm run dev`, vá na aba **Sources** e procure pelos arquivos `.js` da sua própria aplicação. Estão todos ali, legíveis, com nomes de variáveis e comentários incluídos (a não ser que você tenha ativado minificação/ofuscação — que dificulta a leitura, mas não impede). Qualquer verificação de senha, qualquer "if usuário é admin" escrito só em JavaScript de front-end, está exposto a quem quiser ler.

> **🔎 Por baixo do capô**
> "Confiável" aqui não é sobre honestidade — é sobre controle de execução. O servidor é confiável não porque é "mais correto", mas porque só você (o dono da infraestrutura) pode alterar o código que roda nele. O código do navegador, qualquer usuário pode alterar antes de ele rodar (interceptando a requisição, editando o JS carregado, etc.).

### Arquitetura cliente-servidor: o que trafega, onde cada coisa roda

O modelo cliente-servidor divide responsabilidades em duas metades que se comunicam por rede:

- **Cliente** — o front-end UniEventos rodando no navegador do usuário. Responsável por interface, navegação (Vue Router), estado local de tela (Pinia) e por *pedir* dados e ações ao servidor via HTTP (Axios).
- **Servidor** — um processo rodando em uma máquina que você controla (seu notebook agora, um provedor de nuvem depois). Responsável por validar entradas, aplicar regras de negócio, autenticar e autorizar, e ler/gravar dados persistentes.

O que trafega entre os dois é **HTTP**: requisições com método, URL, cabeçalhos e corpo (geralmente JSON), e respostas com status code, cabeçalhos e corpo. Você já usa isso desde a Aula 06 com o Axios — a diferença é que, a partir de hoje, do outro lado da requisição não tem mais o `json-server` genérico, tem um programa que você escreve, controla e pode fazer aplicar qualquer regra que quiser.

```text
┌─────────────────────┐        HTTP (JSON)        ┌──────────────────────┐
│  unieventos-web      │  ────────────────────▶    │  unieventos-api       │
│  (Vue + Vuetify)      │                            │  (Node + Express)     │
│  roda no navegador    │  ◀────────────────────    │  roda no servidor     │
│  do usuário            │                            │  que você controla    │
└─────────────────────┘                             └──────────────────────┘
                                                                │
                                                                ▼
                                                      banco de dados / Firestore
```

> **📌 Na prova**
> Se a pergunta for "por que não validar tudo no front-end?", a resposta certa cita que o código do cliente é executado em uma máquina que o usuário controla, portanto não é confiável para decisões de segurança ou integridade — só o servidor pode ser esse árbitro.

### Relembrando HTTP, porque hoje você escreve os dois lados

Desde a Aula 06 você usa o Axios para fazer requisições. Hoje você passa a escrever o código que **recebe** essas requisições, então vale relembrar o vocabulário do protocolo — ele é o mesmo dos dois lados.

Toda requisição HTTP tem um **método**, que expressa a intenção da ação:

| Método | Intenção |
|---|---|
| `GET` | ler um recurso, sem alterar nada |
| `POST` | criar um recurso novo |
| `PUT`/`PATCH` | atualizar um recurso existente (inteiro ou parcial) |
| `DELETE` | remover um recurso |

E toda resposta HTTP tem um **status code**, um número de três dígitos que resume o resultado sem precisar ler o corpo:

| Faixa | Significado |
|---|---|
| `2xx` | sucesso (`200 OK`, `201 Created`, `204 No Content`) |
| `4xx` | erro do cliente — pedido malformado, recurso inexistente (`400`, `404`, `422`) |
| `5xx` | erro do servidor — algo quebrou ao processar (`500`) |

Você já viu o Axios lançar exceção quando o status vem `4xx` ou `5xx` (Aula 06, nos interceptors). Hoje o ponto de vista muda: você é quem decide qual status devolver em cada rota. Vamos aprofundar status codes por operação na Aula 08 — por ora, guarde que `res.status(código)` é como o Express define esse número antes do corpo da resposta.

Por trás do que o Axios monta e o Express interpreta, uma requisição HTTP crua se parece com isto (é texto puro, trafegando pela rede):

```http
GET /api/eventos/1 HTTP/1.1
Host: localhost:3000
Accept: application/json

```

E a resposta, também texto puro, com cabeçalhos seguidos de uma linha em branco e depois o corpo:

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: 132

{"id":1,"titulo":"Semana Acadêmica de Computação","categoria":"palestra","vagas":80}
```

O Axios, no front, monta essa requisição a partir do que você escreve em `api.get(...)`. O Express, no servidor, faz o caminho inverso: recebe esse texto cru, faz o parse do método, da URL, dos cabeçalhos e do corpo, e entrega tudo isso organizado em `req.method`, `req.path`, `req.headers` e `req.body` para o seu código usar. É exatamente esse trabalho de parsing que `express.json()` completa para o corpo, quando o `Content-Type` é `application/json`.

## 2. Node.js: o runtime por trás do servidor

JavaScript nasceu para rodar dentro de navegadores. O Node.js é um **runtime** — um ambiente de execução — que tira o motor V8 (o mesmo que roda JS no Chrome) de dentro do navegador e o coloca para rodar direto no sistema operacional, com acesso a coisas que o navegador não dá: sistema de arquivos, rede em nível baixo, processos. É isso que permite escrever um servidor HTTP em JavaScript.

### Event loop e I/O não bloqueante, sem mistério

A pergunta que costuma travar quem vem de outras linguagens: como um programa de **uma única thread** atende centenas de requisições ao mesmo tempo sem travar?

A resposta é que o Node.js é bom em uma coisa específica: esperar. A maior parte do trabalho de um servidor web não é "calcular muito" — é "esperar coisas lentas": esperar o banco de dados responder, esperar um arquivo ser lido do disco, esperar outra API responder. Essas operações são de **I/O** (entrada/saída) e, no Node, elas não bloqueiam a thread principal.

Pense assim: quando seu código pede "leia este arquivo" ou "consulte este banco de dados", o Node não fica parado esperando. Ele delega essa espera para o sistema operacional (ou para uma thread interna de apoio) e imediatamente volta a executar a próxima linha de código disponível — atendendo outra requisição, por exemplo. Quando a operação de I/O termina, o resultado entra em uma fila. O **event loop** é o mecanismo que fica continuamente perguntando "tem algo pronto na fila para eu processar agora?" e, quando tem, executa o callback (ou resolve a `Promise`, ou retoma o `await`) correspondente.

```text
 chegou requisição A (buscar eventos no Firestore)
     │
     ▼
 Node dispara a consulta e NÃO espera parado
     │
     ▼
 thread livre → atende requisição B (buscar 1 evento por id)
     │
     ▼
 Node dispara a consulta B e NÃO espera parado
     │
     ▼
 resultado de A fica pronto → event loop retoma o código de A
     │
     ▼
 resultado de B fica pronto → event loop retoma o código de B
```

Isso é diferente de um modelo **bloqueante**, onde a thread ficaria parada, sem fazer nada, do início ao fim de cada consulta — atendendo uma requisição de cada vez, em fila, mesmo que 99% do tempo seja espera. Um servidor Node consegue lidar com milhares de conexões simultâneas com uma única thread principal porque quase todo esse tempo é espera de I/O, não cálculo.

> **⚠️ Atenção**
> Isso não significa que o Node é mágico para tudo. Se seu código fizer um cálculo pesado e síncrono (por exemplo, um laço `for` gigantesco processando dados em memória), ele **bloqueia** a thread principal e trava todas as requisições até terminar. O modelo não bloqueante vale para I/O — rede, disco, banco de dados —, não para processamento pesado de CPU. Para isso existem *worker threads*, fora do escopo desta disciplina.

Na prática, isso aparece no seu código como `async`/`await` e `Promise`, que você já usa desde a Aula 01. `await pool.query(...)` (aula 09) ou `await getDocs(...)` (Firestore, ainda hoje) são exatamente isso: "dispare esta operação de I/O e me devolva o controle quando o resultado chegar, sem travar o resto do programa".

> **🔎 Por baixo do capô**
> Internamente, o Node usa uma biblioteca em C chamada **libuv** para implementar o event loop e delegar operações de I/O ao sistema operacional (ou a uma pequena pool de threads auxiliares, para coisas como leitura de arquivo que o SO não oferece de forma assíncrona nativa). Sua thread JavaScript principal continua única — é a libuv que faz o trabalho de bastidores para nunca bloqueá-la. Você não precisa mexer nisso diretamente; só precisa saber que existe, para entender por que `async`/`await` "simplesmente funciona" sem travar o servidor.

> **💡 Dica**
> Uma analogia útil: pense num garçom (a thread do Node) atendendo várias mesas (requisições) num restaurante. Um garçom **bloqueante** ficaria parado do lado de uma mesa esperando a cozinha terminar um prato antes de atender a próxima mesa. Um garçom **não bloqueante** anota o pedido, leva para a cozinha, e imediatamente vai atender a próxima mesa — voltando a cada mesa só quando o prato dela está pronto. É o mesmo garçom (uma thread), mas ele nunca fica parado esperando.

### Módulos: CommonJS vs ES Modules

Node.js existe desde 2009, muito antes de o JavaScript ter um sistema de módulos padronizado na própria linguagem. Por isso o Node criou o seu: **CommonJS**, baseado em `require()` e `module.exports`.

```js
// estilo CommonJS (antigo, ainda muito comum em tutoriais e pacotes legados)
const express = require('express')
module.exports = { minhaFuncao }
```

Anos depois, o JavaScript ganhou um sistema de módulos oficial da linguagem: **ES Modules** (ESM), baseado em `import`/`export` — o mesmo que você já usa em todo componente Vue desde a Aula 01.

```js
// estilo ES Modules (o que esta disciplina usa no back-end)
import express from 'express'
export function minhaFuncao() { /* ... */ }
```

**Nesta disciplina, o back-end usa ESM.** É consistente com o que você já escreve no front-end, é o padrão recomendado para projetos novos e evita misturar dois estilos de `import`/`require` no mesmo projeto. Para o Node tratar seus arquivos `.js` como ESM (e não CommonJS, que é o padrão histórico), é preciso declarar isso no `package.json`:

```json
{
  "name": "unieventos-api",
  "type": "module"
}
```

Com `"type": "module"` presente, todo arquivo `.js` do projeto passa a ser interpretado como ESM. `require` deixa de funcionar; use sempre `import`.

> **⚠️ Atenção**
> Se você copiar um trecho de tutorial que usa `require('express')` e colar em um projeto com `"type": "module"` no `package.json`, o Node lança `ReferenceError: require is not defined in ES module scope`. A correção é reescrever para `import express from 'express'`. Isso vai acontecer — memorize a mensagem de erro.

### Preparando o ambiente: `npm init`, scripts, `node --watch`

Todo projeto Node começa com um `package.json`, que descreve o projeto, suas dependências e seus scripts.

```bash
mkdir unieventos-api && cd unieventos-api
npm init -y
```

O `npm init -y` gera um `package.json` com valores padrão. Ajuste-o para o que a disciplina usa:

```json
{
  "name": "unieventos-api",
  "version": "1.0.0",
  "description": "API do projeto UniEventos — FACET-SNP-310",
  "type": "module",
  "main": "src/servidor.js",
  "scripts": {
    "dev": "node --watch --env-file=.env src/servidor.js",
    "start": "node --env-file=.env src/servidor.js"
  }
}
```

Dois pontos merecem atenção:

**`node --watch` no lugar do `nodemon`.** Historicamente, quem desenvolvia com Node instalava o pacote `nodemon` para reiniciar o servidor automaticamente a cada alteração de arquivo. Desde a versão 18.11, o próprio Node tem essa funcionalidade embutida: a flag `--watch`. Não é preciso instalar mais nada.

```bash
node --watch src/servidor.js
```

**Variáveis de ambiente com `process.env` e `--env-file`.** Toda configuração que muda entre ambientes (porta do servidor, credenciais de banco, chaves de API) deve vir de variáveis de ambiente, nunca de valores fixos no código. O Node expõe essas variáveis no objeto global `process.env`. Desde a versão 20.6 (estável desde a 22), o Node lê arquivos `.env` nativamente, sem precisar do pacote `dotenv`:

```bash
node --env-file=.env src/servidor.js
```

```bash
# .env (nunca commitar este arquivo)
PORTA=3000
```

```js
// uso de process.env em qualquer arquivo do projeto
const porta = process.env.PORTA || 3000
```

> **💡 Dica**
> Crie sempre um `.env.example` versionado, com as chaves (sem os valores sigilosos), para quem clonar o repositório saber o que configurar. E adicione `.env` ao `.gitignore` imediatamente — antes do primeiro commit, não depois.

### `dependencies` vs `devDependencies`, e o que é o `package-lock.json`

Quando você roda `npm install express cors`, dois efeitos acontecem: os pacotes são baixados para `node_modules/`, e o `package.json` ganha uma entrada em `"dependencies"`. Pacotes que só existem para ajudar durante o desenvolvimento — nunca rodam em produção — vão em `"devDependencies"`, instalados com a flag `-D`:

```bash
npm install express cors          # vai para "dependencies" — necessário em produção
npm install -D algum-pacote-de-teste   # vai para "devDependencies" — só em desenvolvimento
```

O `package-lock.json`, gerado automaticamente, trava a versão exata (inclusive das dependências transitivas — as dependências das suas dependências) que foi instalada. Ele **deve** ser commitado: garante que qualquer pessoa que clone o repositório e rode `npm install` receba exatamente as mesmas versões que você testou, evitando o clássico "na minha máquina funciona".

> **⚠️ Atenção**
> `node_modules/` nunca é commitado — é sempre reconstruído com `npm install` a partir do `package.json` e do `package-lock.json`. Ele já está no `.gitignore` do projeto.

## 🧩 Padrão de projeto em uso

> ### 🧩 Padrão de projeto em uso — Chain of Responsibility
>
> Um servidor Express processa toda requisição através de uma sequência de funções chamadas **middlewares**: `express.json()`, `cors()`, sua rota, e (aula 08) validadores e tratadores de erro. Cada função na cadeia decide se trata a requisição, a repassa adiante com `next()`, ou interrompe o fluxo respondendo diretamente. Isso é o padrão comportamental **Chain of Responsibility**: uma corrente de handlers, cada um com a chance de agir e passar adiante. Você já viu a ideia em ação nos interceptors do Axios (Aula 06) — lá era uma cadeia de duas etapas (requisição/resposta); aqui é uma cadeia configurável de N etapas. Vamos aprofundar isso na Aula 08, quando você escrever seus próprios middlewares.

## 3. BaaS vs API própria: o que é o Firebase

Nem todo back-end precisa ser escrito do zero. Um **BaaS** (*Backend as a Service*) é um serviço de terceiros que já entrega pedaços prontos de back-end — banco de dados, autenticação, upload de arquivos, hospedagem — através de um SDK que você chama direto do seu front-end, sem escrever seu próprio servidor para essas partes.

O **Firebase**, do Google, é o BaaS mais usado no mercado. Os serviços relevantes para esta disciplina:

| Serviço | Para que serve |
|---|---|
| **Authentication** | login/cadastro (e-mail+senha, Google, etc.) — usado na Aula 10 |
| **Firestore** | banco de dados NoSQL orientado a documentos, em tempo real |
| **Storage** | upload e hospedagem de arquivos (ex.: imagem do evento) |
| **Hosting** | hospedagem estática do front-end compilado |
| **Cloud Functions** | código de back-end sob demanda, sem gerenciar servidor |

**Quando um BaaS resolve:** protótipos, MVPs, projetos pequenos ou médios onde autenticação e um banco de dados de propósito geral já cobrem a necessidade. Você escreve praticamente zero código de servidor — o SDK do Firebase fala direto com a nuvem do Google a partir do seu Vue.

**Quando um BaaS não resolve:** quando a regra de negócio é complexa demais para expressar só em regras de segurança do Firestore; quando você precisa de consultas relacionais complexas (JOINs, agregações — ponto forte de um SGBD relacional, Aula 09); quando você precisa de controle total sobre a lógica do servidor; ou, como nesta disciplina, quando o objetivo é justamente **aprender a construir um back-end**. Por isso o UniEventos vai usar o Firestore hoje para uma leitura/escrita simples, mas a partir da Aula 08 a lógica de negócio migra para uma API Express própria, e na Aula 09 os dados migram para MySQL.

> **⚠️ Atenção**
> Nunca use a API antiga do Firebase, com namespace (`firebase.initializeApp(...)`, `firebase.firestore()`). Ela ainda aparece em vídeos e artigos antigos. Esta disciplina usa **exclusivamente a API modular**, versão 12, com `import` nomeado de funções: `import { initializeApp } from 'firebase/app'`.

### Criando o projeto no console do Firebase

1. Acesse [console.firebase.google.com](https://console.firebase.google.com) com sua conta Google.
2. Clique em **Adicionar projeto**, dê o nome `unieventos` (ou `unieventos-seu-nome`, já que o nome do projeto precisa ser único globalmente) e siga o assistente (pode desativar o Google Analytics, não é necessário para a disciplina).
3. Dentro do projeto, clique no ícone **`</>`** (Web) para registrar um app web. Dê o apelido `unieventos-web`.
4. O console mostra um objeto `firebaseConfig` — **copie-o**, ele contém as chaves de configuração do seu projeto (não são segredos no sentido de senha, mas identificam seu projeto):

```js
// exemplo de firebaseConfig — o seu terá valores diferentes
const firebaseConfig = {
  apiKey: 'AIzaSyExemploDeChaveNaoUseEsta',
  authDomain: 'unieventos-xxxxx.firebaseapp.com',
  projectId: 'unieventos-xxxxx',
  storageBucket: 'unieventos-xxxxx.firebasestorage.app',
  messagingSenderId: '123456789012',
  appId: '1:123456789012:web:abcdef1234567890',
}
```

5. No menu lateral, vá em **Build → Firestore Database** e clique em **Criar banco de dados**. Escolha a localização (qualquer região das Américas serve) e, quando perguntado sobre regras de segurança, escolha **modo de teste**.

> **⚠️ Atenção**
> O modo de teste libera leitura e escrita para qualquer um por **30 dias**, sem autenticação nenhuma. Isso é intencional para você aprender sem se preocupar com regras agora — mas **nunca** vá para produção assim. Na Aula 10, quando integrarmos o Firebase Auth, vamos escrever regras de segurança de verdade, amarradas ao usuário autenticado.

### Instalando o SDK e inicializando o app

Isso aqui roda no **front-end** (`unieventos-web`), não na API que vamos criar depois — o SDK do Firebase fala direto com a nuvem do Google a partir do navegador.

```bash
npm install firebase@12
```

```js
// src/firebase.js — em unieventos-web
import { initializeApp } from 'firebase/app'
import { getFirestore } from 'firebase/firestore'

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
}

// inicializa a conexão com o projeto Firebase
export const appFirebase = initializeApp(firebaseConfig)

// instância do Firestore usada em todo o projeto
export const db = getFirestore(appFirebase)
```

```bash
# .env (em unieventos-web, prefixo VITE_ obrigatório para o Vite expor a variável ao front)
VITE_FIREBASE_API_KEY=AIzaSyExemploDeChaveNaoUseEsta
VITE_FIREBASE_AUTH_DOMAIN=unieventos-xxxxx.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=unieventos-xxxxx
VITE_FIREBASE_STORAGE_BUCKET=unieventos-xxxxx.firebasestorage.app
VITE_FIREBASE_MESSAGING_SENDER_ID=123456789012
VITE_FIREBASE_APP_ID=1:123456789012:web:abcdef1234567890
```

> **💡 Dica**
> No Vite, variáveis de ambiente expostas ao código do navegador precisam começar com `VITE_`. É uma proteção: assim você não expõe acidentalmente uma variável sensível do servidor de build para o navegador.

### Primeira leitura e escrita no Firestore

O Firestore organiza dados em **coleções** (como uma tabela, mas sem schema fixo) de **documentos** (como uma linha, mas um objeto JSON aninhável). Vamos escrever e ler eventos de teste.

```js
// src/testeFirestore.js — script de exploração, não faz parte da app final
import {
  collection,
  addDoc,
  getDocs,
  doc,
  updateDoc,
  deleteDoc,
  query,
  where,
  orderBy,
} from 'firebase/firestore'
import { db } from './firebase.js'

// referência para a coleção "eventos"
const colecaoEventos = collection(db, 'eventos')

async function criarEventoDeTeste() {
  // addDoc gera um id automático e grava o documento
  const referencia = await addDoc(colecaoEventos, {
    titulo: 'Semana Acadêmica de Computação',
    categoria: 'palestra',
    vagas: 80,
    dataHora: '2026-10-15T19:00:00',
  })
  console.log('documento criado com id:', referencia.id)
}

async function listarTodosOsEventos() {
  const snapshot = await getDocs(colecaoEventos)
  const eventos = snapshot.docs.map((d) => ({ id: d.id, ...d.data() }))
  console.log('eventos encontrados:', eventos)
}

async function listarPalestrasOrdenadasPorData() {
  // query + where + orderBy formam uma consulta filtrada e ordenada
  const consulta = query(
    colecaoEventos,
    where('categoria', '==', 'palestra'),
    orderBy('dataHora', 'asc'),
  )
  const snapshot = await getDocs(consulta)
  return snapshot.docs.map((d) => ({ id: d.id, ...d.data() }))
}

async function atualizarVagas(idDoEvento, novasVagas) {
  // doc() aponta para um documento específico dentro da coleção
  const referenciaDoDocumento = doc(db, 'eventos', idDoEvento)
  await updateDoc(referenciaDoDocumento, { vagas: novasVagas })
}

async function removerEvento(idDoEvento) {
  const referenciaDoDocumento = doc(db, 'eventos', idDoEvento)
  await deleteDoc(referenciaDoDocumento)
}

await criarEventoDeTeste()
await listarTodosOsEventos()
```

> **🔎 Por baixo do capô**
> `getDocs` devolve um `QuerySnapshot`, não um array direto. Cada item é um `QueryDocumentSnapshot`, com `.id` (o id do documento) separado de `.data()` (o conteúdo). Por isso o padrão `{ id: d.id, ...d.data() }` aparece toda vez que você lê uma coleção — é assim que você recompõe um objeto "normal" com id incluso.

### As regras de segurança por trás do modo de teste

Quando você escolheu "modo de teste" ao criar o banco, o Firebase gravou uma regra de segurança liberando tudo por 30 dias. Vale abrir **Firestore Database → Regras** no console e olhar o que foi gerado:

```text
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if request.time < timestamp.date(2026, 10, 12);
    }
  }
}
```

Note a condição: `allow read, write` só vale **até uma data**. Depois disso, toda leitura e escrita passa a ser negada por padrão — é assim que o Firestore evita bancos de teste esquecidos abertos para o mundo. Não precisa mexer nessas regras hoje; na Aula 10, quando o Firebase Authentication entrar, vamos trocar essa condição por algo como `allow read: if true; allow write: if request.auth != null;` — leitura pública, escrita só para quem está autenticado.

> **⚠️ Atenção**
> Um erro comum é confundir "regra de segurança do Firestore" com "regra de negócio da aplicação". A regra de segurança só decide **quem pode ler/escrever**; ela não valida, por exemplo, se o número de vagas de um evento é positivo. Esse tipo de validação continua sendo responsabilidade do código — do front-end como primeira camada de UX, e do back-end como camada de verdade (Aula 08).

Esta exploração no Firestore serve para você conhecer o SDK modular — ele volta com força na Aula 10, quando o Firebase Authentication entrar em cena. **A partir de agora**, porém, o motor de dados principal do UniEventos passa a ser a API Express que vamos construir, primeiro em memória (hoje e na Aula 08) e depois em MySQL (Aula 09).

## 4. Express 5.2.1: o servidor mínimo

Express é um **framework web minimalista** para Node.js: ele não decide como você organiza pastas nem qual banco usar, só oferece o essencial para receber requisições HTTP, rotear por método e caminho, e responder. É a ferramenta padrão de mercado para APIs Node.

```bash
mkdir -p src
npm install express cors
```

```js
// src/servidor.js
import express from 'express'
import cors from 'cors'

const app = express()

// middlewares de aplicação: rodam em toda requisição, nesta ordem
app.use(cors())           // libera requisições de outras origens (o front em outra porta)
app.use(express.json())   // faz o parse do corpo JSON e popula req.body

// primeira rota: responde a GET /
app.get('/', (req, res) => {
  res.json({ mensagem: 'API do UniEventos no ar' })
})

const porta = process.env.PORTA || 3000

app.listen(porta, () => {
  console.log(`unieventos-api rodando em http://localhost:${porta}`)
})
```

Suba o servidor:

```bash
node --watch src/servidor.js
```

Teste no navegador acessando `http://localhost:3000/`, ou no terminal:

```bash
curl http://localhost:3000/
# {"mensagem":"API do UniEventos no ar"}
```

`express.json()` e `cors()` são exemplos de **middlewares de aplicação**: funções que rodam para toda requisição, registradas com `app.use()`, antes de qualquer rota. `express.json()` lê o corpo da requisição, faz o parse como JSON, e disponibiliza o resultado em `req.body`. `cors()` adiciona os cabeçalhos que autorizam o navegador a aceitar a resposta quando a requisição vem de uma origem diferente (por exemplo, o front-end rodando em `localhost:5173` chamando a API em `localhost:3000`) — sem isso, o navegador bloqueia a resposta por política de mesma origem.

### Estrutura inicial de pastas

```text
unieventos-api/
├─ src/
│  └─ servidor.js
├─ .env
├─ .env.example
├─ .gitignore
├─ package.json
└─ requests.http
```

Vamos crescer essa estrutura nas próximas duas aulas (`routes/`, `middlewares/`, `repositories/`, `services/`, `controllers/`). Por enquanto, um único arquivo é suficiente.

## ⚠️ Express 5 não é Express 4

Quando você instala Express hoje (`npm install express`), recebe a versão 5.2.1 — mas a maioria dos tutoriais, cursos gravados e respostas de fórum na internet ainda ensina Express 4, que tem sintaxe diferente em pontos que quebram silenciosamente ou lançam erro. A tabela a seguir foi **testada no ambiente real** desta disciplina — não é teoria, é o que de fato acontece rodando o código.

| Express 4 (não use) | Express 5.2.1 (use) |
|---|---|
| erro em handler `async` precisa de `.catch(next)` manual | erro em handler `async` é capturado automaticamente pelo Express |
| `req.query` podia ser reatribuído | `req.query` é **somente leitura** |
| `app.del('/rota', ...)` | `app.delete('/rota', ...)` — `app.del` foi removido |
| `res.redirect('/rota', 302)` | `res.redirect(302, '/rota')` — ordem invertida |
| `res.json(objeto, 201)` | `res.status(201).json(objeto)` — a assinatura de dois argumentos não existe mais |
| `req.param('id')` | `req.params.id` — `req.param()` foi removido |
| `res.sendfile()` | `res.sendFile()` |
| `app.get('/arquivos/*')` | `app.get('/arquivos/*splat')` — curinga nomeado, `req.params.splat` vira **array** |
| `app.get('/relatorio/:ano?')` | `app.get('/relatorio{/:ano}')` — segmento opcional é chave, não `?` |
| exigia `body-parser` instalado à parte | `express.json()`/`express.urlencoded()` já são nativos |
| `req.body` virava `{}` sem parser | `req.body` é `undefined` se nada foi parseado |

Os pontos que mais pegam quem está aprendendo:

**Erros assíncronos, agora automáticos.** No Express 4, se um handler `async` lançasse uma exceção, ela **não** era capturada pelo tratador de erros — a requisição ficava pendurada ou o processo caía, a menos que você embrulhasse manualmente com `.catch(next)` ou usasse o pacote `express-async-handler`. É por isso que tanto código por aí ainda importa esse pacote. No Express 5, isso já funciona sem nada extra:

```js
// Express 5: pode dar throw dentro de um handler async — cai direto no error handler
app.get('/api/eventos/:id', async (req, res) => {
  const evento = await buscarEventoPorId(req.params.id)
  if (!evento) {
    throw new Error('Evento não encontrado')  // capturado automaticamente
  }
  res.json(evento)
})
```

Vamos explorar isso a fundo na Aula 08, com uma classe de erro própria (`ErroHttp`) e um tratador central.

**`req.query` é somente leitura.** No Express 4 era comum, embora não recomendado, fazer `req.query.pagina = Number(req.query.pagina)` para normalizar um valor. No Express 5, isso lança erro em runtime — `req.query` não pode ser reatribuído. Se precisar de um valor tratado, crie uma variável nova:

```js
// ERRADO no Express 5: lança TypeError
// req.query.pagina = Number(req.query.pagina)

// CORRETO: crie uma variável nova a partir do valor lido
const pagina = Number(req.query.pagina) || 1
```

**Curingas e segmentos opcionais mudaram de sintaxe.** O Express 5 trocou o motor de rotas para `path-to-regexp` v8, que não aceita mais `*` solto nem `?` para tornar um segmento opcional. É preciso nomear o curinga e envolver o opcional em chaves:

```js
// Express 4 (não use): curinga solto
// app.get('/arquivos/*', (req, res) => { ... })

// Express 5: curinga nomeado — req.params.splat vem como ARRAY de segmentos
app.get('/arquivos/*splat', (req, res) => {
  console.log(req.params.splat) // ex.: ['pdf', 'edital-2026.pdf']
})

// Express 4 (não use): segmento opcional com "?"
// app.get('/relatorio/:ano?', (req, res) => { ... })

// Express 5: segmento opcional entre chaves
app.get('/relatorio{/:ano}', (req, res) => {
  // GET /relatorio      -> req.params.ano é undefined
  // GET /relatorio/2026 -> req.params.ano é '2026'
  const ano = req.params.ano || 'atual'
  res.json({ relatorioDoAno: ano })
})
```

Não vamos precisar de curingas nem de segmentos opcionais na API do UniEventos por enquanto, mas é comum encontrar essa sintaxe em documentação de upload de arquivos ou rotas de relatório — reconhecer a diferença evita copiar sintaxe do Express 4 sem perceber.

**`app.del` e `res.sendfile`, os "quase iguais" que quebram silenciosamente.** Esses dois têm um detalhe traiçoeiro: o Express 5 não lança erro amigável — `app.del` simplesmente não existe mais como método (`TypeError: app.del is not a function`), e `res.sendfile` (tudo minúsculo) também não existe (`res.sendfile is not a function`). A diferença de capitalização em `sendFile` é sutil o bastante para passar despercebida numa leitura rápida.

```js
// ERRADO — Express 4
// app.del('/api/eventos/:id', removerEvento)
// res.sendfile(caminhoDoArquivo)

// CORRETO — Express 5
app.delete('/api/eventos/:id', removerEvento)
res.sendFile(caminhoDoArquivo)
```

> **📌 Na prova**
> Se aparecer um trecho de código com `app.del(...)`, `res.json(obj, 201)` ou `req.param('id')`, é Express 4 — identifique a sintaxe errada e corrija para a equivalente do Express 5.

## 💻 Mão na massa — criando a `unieventos-api` e conectando o front

### Passo 1 — criar o repositório e o projeto Node

```bash
mkdir unieventos-api && cd unieventos-api
git init
npm init -y
npm install express cors
```

Edite o `package.json` gerado:

```json
{
  "name": "unieventos-api",
  "version": "1.0.0",
  "description": "API do projeto UniEventos — FACET-SNP-310",
  "type": "module",
  "main": "src/servidor.js",
  "scripts": {
    "dev": "node --watch --env-file=.env src/servidor.js",
    "start": "node --env-file=.env src/servidor.js"
  },
  "dependencies": {
    "cors": "^2.8.5",
    "express": "^5.2.1"
  }
}
```

```text
# .gitignore
node_modules/
.env
```

```bash
# .env.example
PORTA=3000
```

```bash
# .env
PORTA=3000
```

### Passo 2 — dados de eventos em memória

```js
// src/dados/eventos.js
// dados em memória — nesta aula ainda não temos banco de dados (chega na Aula 09)
export const eventos = [
  {
    id: 1,
    titulo: 'Semana Acadêmica de Computação',
    descricao: 'Palestras e minicursos sobre o mercado de tecnologia.',
    categoria: 'palestra',
    dataHora: '2026-10-15T19:00:00',
    local: 'Auditório FACET',
    vagas: 80,
    imagemUrl: 'https://picsum.photos/seed/semana-computacao/400/240',
  },
  {
    id: 2,
    titulo: 'Minicurso de Vue 3',
    descricao: 'Introdução prática ao framework Vue com Composition API.',
    categoria: 'minicurso',
    dataHora: '2026-10-20T14:00:00',
    local: 'Laboratório 3',
    vagas: 30,
    imagemUrl: 'https://picsum.photos/seed/minicurso-vue/400/240',
  },
  {
    id: 3,
    titulo: 'Workshop de Firebase e Express',
    descricao: 'Construindo uma API real do zero.',
    categoria: 'workshop',
    dataHora: '2026-10-28T19:30:00',
    local: 'Laboratório 1',
    vagas: 25,
    imagemUrl: 'https://picsum.photos/seed/workshop-firebase/400/240',
  },
]
```

### Passo 3 — servidor com as duas primeiras rotas

```js
// src/servidor.js
import express from 'express'
import cors from 'cors'
import { eventos } from './dados/eventos.js'

const app = express()

app.use(cors())
app.use(express.json())

// GET /api/eventos — lista todos os eventos
app.get('/api/eventos', (req, res) => {
  res.json(eventos)
})

// GET /api/eventos/:id — busca um evento específico
app.get('/api/eventos/:id', (req, res) => {
  // req.params.id sempre chega como string — convertemos para comparar com o id numérico
  const id = Number(req.params.id)
  const evento = eventos.find((e) => e.id === id)

  if (!evento) {
    return res.status(404).json({ erro: 'Evento não encontrado' })
  }

  res.json(evento)
})

const porta = process.env.PORTA || 3000

app.listen(porta, () => {
  console.log(`unieventos-api rodando em http://localhost:${porta}`)
})
```

Suba com `npm run dev` e teste:

```bash
curl http://localhost:3000/api/eventos
curl http://localhost:3000/api/eventos/1
curl http://localhost:3000/api/eventos/999
# {"erro":"Evento não encontrado"}
```

### Três formas de testar, e quando usar cada uma

Você vai testar a mesma API de três jeitos diferentes ao longo do curso. Cada um serve para um momento:

**Navegador.** Rápido para conferir uma rota `GET` simples visualmente — cole a URL na barra de endereços. Limitação: o navegador só faz `GET` ao digitar uma URL; não dá para testar `POST`, `PUT`, `DELETE` nem enviar cabeçalhos customizados dessa forma.

**`curl`.** Funciona para qualquer método, direto do terminal, sem depender do VS Code estar aberto. Ótimo para scripts, para depuração rápida e para copiar/colar em relatos de bug. A sintaxe fica mais verbosa conforme a requisição cresce:

```bash
curl -X POST http://localhost:3000/api/eventos \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Palestra de teste","categoria":"palestra","vagas":10}'
```

**REST Client / Thunder Client (VS Code).** O melhor equilíbrio para desenvolvimento do dia a dia: a requisição fica escrita em um arquivo versionado (`requests.http`), legível, reaproveitável pelo time todo, e você clica para executar sem digitar nada no terminal. É o que vamos usar como principal ferramenta de teste manual a partir de agora — inclusive na Aula 08, onde o arquivo `requests.http` cresce para cobrir todo o CRUD.

> **💡 Dica**
> Nenhuma das três ferramentas substitui testes automatizados (fora do escopo desta disciplina). Elas servem para verificação manual durante o desenvolvimento — e o arquivo `requests.http` tem a vantagem extra de documentar a API para quem vai usá-la depois, inclusive você mesmo daqui a um mês.

### Passo 4 — testando com REST Client (VS Code)

Crie um arquivo de requisições versionado, que serve de documentação viva da API:

```http
### requests.http — abra este arquivo no VS Code com a extensão REST Client instalada
### clique em "Send Request" acima de cada bloco para testar

### listar todos os eventos
GET http://localhost:3000/api/eventos

### buscar um evento específico
GET http://localhost:3000/api/eventos/1

### buscar um evento que não existe (deve responder 404)
GET http://localhost:3000/api/eventos/999
```

> **💡 Dica**
> Se você usa a extensão **Thunder Client** em vez de REST Client, a ideia é a mesma, mas a interface é uma aba própria no VS Code, com histórico de requisições e coleções salvas. Escolha a que preferir — o importante é testar toda rota antes de conectar o front.

### Passo 5 — apontar o front-end da Aula 06 para a API real

No `unieventos-web`, você já tem uma instância dedicada do Axios (Aula 06). Troque só a `baseURL`:

```js
// src/services/api.js — em unieventos-web
import axios from 'axios'

const api = axios.create({
  // antes: baseURL: 'http://localhost:3001' (json-server)
  baseURL: 'http://localhost:3000/api',
})

export default api
```

Nada mais no front-end precisa mudar — nem a store Pinia, nem os componentes. O service continua chamando `api.get('/eventos')` e `api.get(`/eventos/${id}`)`; quem muda é só o destino das requisições. Esse desacoplamento é exatamente o motivo pelo qual a Aula 06 insistiu em centralizar o `baseURL` numa instância única, em vez de espalhar URLs pelo código.

```bash
# em dois terminais separados:

# terminal 1 — dentro de unieventos-api
npm run dev

# terminal 2 — dentro de unieventos-web
npm run dev
```

Abra o front no navegador. A lista de eventos deve carregar exatamente como antes — só que agora vem de um servidor Express que você escreveu, não de um `json-server`.

## 🧪 Laboratório

**1. Rota de saudação personalizada.** Crie `GET /api/saudacao/:nome` que responde `{ "mensagem": "Olá, <nome>!" }`, capitalizando a primeira letra do nome recebido.

<details markdown="1">
<summary>Dica</summary>

Use `req.params.nome` e uma função para capitalizar: `nome.charAt(0).toUpperCase() + nome.slice(1)`.
</details>

**2. Filtro por categoria via query string.** Modifique `GET /api/eventos` para aceitar `?categoria=palestra` e retornar só os eventos daquela categoria. Sem o parâmetro, retorna todos.

<details markdown="1">
<summary>Dica</summary>

Leia `req.query.categoria` (lembre-se: é somente leitura, não reatribua). Se estiver presente, filtre o array com `.filter()` antes de responder.
</details>

**3. Contagem total no cabeçalho.** Adicione um cabeçalho de resposta `X-Total-Count` com a quantidade de eventos retornados em `GET /api/eventos`, usando `res.set('X-Total-Count', String(eventos.length))`.

<details markdown="1">
<summary>Dica</summary>

`res.set(nome, valor)` precisa vir antes de `res.json(...)`, porque depois que o corpo é enviado os cabeçalhos não podem mais ser alterados.
</details>

**4. Teste de erro proposital.** Escreva uma rota `GET /api/quebra` que dá `throw new Error('falha proposital')` dentro de um handler `async`. Suba o servidor, acesse a rota e observe no terminal o que acontece — sem nenhum tratamento de erro escrito por você ainda.

<details markdown="1">
<summary>Dica</summary>

No Express 5 isso não derruba o servidor: a resposta padrão é um HTML de erro 500. Guarde essa observação — na Aula 08 você substitui isso por um tratador de erros customizado.
</details>

**5. Front consumindo a nova rota de filtro.** No `unieventos-web`, adicione um `<v-select>` de categoria na Home e faça a requisição incluir `params: { categoria }` quando um filtro estiver selecionado (lembre do terceiro parâmetro do `axios.get`, visto na Aula 06).

<details markdown="1">
<summary>Dica</summary>

`api.get('/eventos', { params: { categoria: valorSelecionado } })` — se `valorSelecionado` for `undefined` ou string vazia, o Axios omite o parâmetro da URL automaticamente.
</details>

**6. Explorando o Firestore com uma segunda coleção.** Crie, pelo console do Firebase ou por script, uma coleção `organizadores` com pelo menos 2 documentos (`nome`, `email`). Escreva uma função `listarOrganizadores()` que usa `getDocs` para trazer todos e imprime no console. Depois, escreva `buscarOrganizadorPorEmail(email)` usando `query` + `where('email', '==', email)`.

<details markdown="1">
<summary>Dica</summary>

`where` sempre entra como argumento de `query(colecao, where(...), ...)` — não é um método encadeado como em outras bibliotecas. Lembre de importar `where` de `'firebase/firestore'`.
</details>

## 🐛 Erros comuns e como resolver

| Sintoma | Causa | Solução |
|---|---|---|
| `ReferenceError: require is not defined in ES module scope` | copiou código CommonJS num projeto com `"type": "module"` | troque `require`/`module.exports` por `import`/`export` |
| `EADDRINUSE: address already in use :::3000` | outro processo já ocupa a porta 3000 | finalize o processo anterior ou mude `PORTA` no `.env` |
| Front recebe erro de CORS no console do navegador | esqueceu `app.use(cors())` ou ele vem depois das rotas | registre `app.use(cors())` antes de declarar as rotas |
| `req.body` chega `undefined` | `express.json()` não foi registrado, ou o `Content-Type` da requisição não é `application/json` | adicione `app.use(express.json())` antes das rotas; confira o cabeçalho enviado |
| `TypeError: Cannot set property query of #<IncomingMessage>` | tentou reatribuir `req.query` diretamente (hábito do Express 4) | crie uma variável nova a partir do valor lido, não reatribua `req.query` |
| Página em branco ao testar rota no navegador, sem erro no terminal | esqueceu do `return` antes de um segundo `res.status().json()` na mesma função | sempre `return res...` quando houver mais de uma resposta possível no handler |
| Firestore: `getDocs` retorna vazio mesmo com dados no console | está lendo de uma coleção com nome diferente do usado ao gravar (ex.: `Eventos` vs `eventos`) | nomes de coleção são case-sensitive; confira a grafia exata |
| `FirebaseError: Missing or insufficient permissions` | as regras de segurança de teste do Firestore expiraram (30 dias) | reabra o modo de teste no console ou escreva regras explícitas (Aula 10) |
| `Cannot find module 'firebase/app'` | instalou uma versão muito antiga do pacote, ou digitou `firebase-admin` por engano no front | confirme `npm install firebase@12` no `unieventos-web`; `firebase-admin` é só para back-end (Aula 10) |
| Rota `GET /api/eventos/:id` sempre cai no "não encontrado" | comparou `req.params.id` (string) com `id` (number) sem converter | use `Number(req.params.id)` antes de comparar com `===` |
| `npm run dev` não reinicia ao salvar o arquivo | versão do Node anterior à 18.11, sem suporte a `--watch` | rode `node -v` e atualize para a 22.x indicada na disciplina |

## 🏠 Atividade assíncrona (1 h)

No seu **projeto autoral**, replique o que foi feito hoje:

1. Crie o repositório `<seu-projeto>-api`, com `package.json` configurado em ESM, scripts `dev`/`start`, `.env`/`.env.example`/`.gitignore`.
2. Monte um arquivo `src/dados/<entidade-principal>.js` com pelo menos 4 itens de exemplo do domínio do seu projeto autoral (ex.: se seu tema é "cardápio de restaurante", 4 pratos).
3. Escreva `src/servidor.js` com Express 5, `cors()`, `express.json()`, e as duas rotas equivalentes: listar tudo e buscar por id.
4. Teste as duas rotas com `curl` **e** com REST Client/Thunder Client — cole as evidências (prints ou saída do terminal) num arquivo `EVIDENCIAS.md` no repositório.
5. Aponte o front-end do seu projeto autoral (já existente desde a Aula 06) para esta nova API, trocando só o `baseURL`.

**Critério de pronto:** os dois repositórios (`-web` e `-api`) rodando simultaneamente em portas diferentes, com a listagem do seu projeto autoral carregando dados vindos da sua própria API Express — nada de `json-server` a partir de agora.

## ✅ Checkpoint do projeto autoral

- [ ] Repositório `<seu-projeto>-api` criado, com `"type": "module"` no `package.json`.
- [ ] Servidor Express 5 rodando com `npm run dev` (usando `node --watch`).
- [ ] `.env` e `.env.example` configurados; `.env` no `.gitignore` (nunca commitado).
- [ ] `cors()` e `express.json()` registrados antes das rotas.
- [ ] `GET /api/<entidade>` e `GET /api/<entidade>/:id` respondendo corretamente, inclusive o caso de id inexistente (404).
- [ ] Front-end do projeto autoral consumindo essa API real via a instância Axios dedicada.
- [ ] Nenhuma sintaxe de Express 4 (`app.del`, `res.json(obj, 201)`, `req.param()`) presente no código.

## 📚 Para aprofundar

- Documentação oficial do Node.js — [nodejs.org/docs](https://nodejs.org/en/docs) (seções *Modules: ECMAScript modules* e *Command-line API* para `--watch` e `--env-file`).
- Documentação oficial do Express — [expressjs.com](https://expressjs.com/) e o guia de migração *Express 5 changes* — [expressjs.com/en/guide/migrating-5.html](https://expressjs.com/en/guide/migrating-5.html).
- Documentação oficial do Firebase — [firebase.google.com/docs/web/setup](https://firebase.google.com/docs/web/setup) e [firebase.google.com/docs/firestore](https://firebase.google.com/docs/firestore) (API modular).
- Referência de `path-to-regexp` v8, usado internamente pelo Express 5 para casar rotas — útil para entender a sintaxe de curingas e segmentos opcionais em profundidade.
- Plano de curso FACET-SNP-310 — bibliografia básica, capítulos sobre arquitetura cliente-servidor e Node.js.

Na Aula 08 você transforma o servidor de hoje num CRUD completo, modulariza rotas com `express.Router()`, escreve middlewares próprios e recebe as instruções da **Avaliação 2**. Deixe a `unieventos-api` rodando — ela cresce a partir daqui, aula após aula, até virar a API do seu projeto autoral final.
