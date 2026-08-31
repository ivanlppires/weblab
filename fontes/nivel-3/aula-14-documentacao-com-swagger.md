# Aula 14 — Documentação com Swagger

> **Nível 3 — Frameworks Modernos** · Unidade 3: Integração front-end/back-end
> WebLab · UNEMAT Sinop · Prof. Ivan Luiz Pedroso Pires
> **Carga:** 3 aulas de 50 min (presencial) + 1 h (assíncrona)

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Explicar por que documentar uma API é parte do trabalho de engenharia, não um extra opcional.
- Diferenciar OpenAPI (a especificação) de Swagger (o conjunto de ferramentas que a implementa).
- Ler e escrever a anatomia de um documento OpenAPI 3.0: `info`, `servers`, `paths`, `components.schemas`, `components.securitySchemes`.
- Gerar a especificação a partir de anotações `@openapi` com `swagger-jsdoc`, usando corretamente a chave `definition`.
- Servir e customizar o Swagger UI com `swagger-ui-express`, incluindo o endpoint com o JSON cru.
- Documentar todos os endpoints do UniEventos com schemas reutilizáveis e segurança via `bearerAuth`.
- Testar endpoints protegidos direto pelo Swagger UI usando o botão "Authorize".
- Produzir um README de qualidade, um `CONTRIBUTING.md` mínimo e registrar decisões de arquitetura em formato ADR.

## 📋 Pré-requisitos desta aula

Na Aula 13 transformamos o `unieventos-api` em uma arquitetura em camadas testável e segura. O código ficou sólido por dentro — mas de fora, para quem nunca viu o projeto (um colega de equipe, um avaliador, você mesmo em três meses), ele ainda é uma caixa-preta: só descobre o que a API faz lendo o código-fonte inteiro. Hoje resolvemos isso com um contrato formal e navegável: **OpenAPI + Swagger UI**.

- `unieventos-api` (ou projeto autoral) já refatorado para arquitetura em camadas (Aula 13), com rotas de eventos, inscrições e autenticação funcionando.
- Node.js 22 LTS e a API rodando localmente com `npm run dev`.

Checklist antes de começar:

- [ ] `GET /health` responde `200` na sua API.
- [ ] Você consegue autenticar via Firebase e obter um token de ID (Aula 10) para testar rotas protegidas.
- [ ] Ferramenta para chamadas HTTP manuais disponível (Insomnia, Postman ou `curl`).

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Por que documentar, OpenAPI vs. Swagger, anatomia do documento |
| 2 | 50 min | `swagger-jsdoc` + `swagger-ui-express`: configuração e primeiros endpoints anotados |
| 3 | 50 min | Documentando toda a API do UniEventos, segurança com bearerAuth, README/ADR |

## 1. Por que documentar uma API

Um endpoint sem documentação obriga quem for consumi-lo a ler o código-fonte do back-end inteiro — ou pior, a adivinhar por tentativa e erro. Em qualquer cenário além do "eu programando sozinho e lembrando de tudo", isso custa tempo real:

- **Contrato entre times.** O time de front-end pode começar a construir a tela de "Minhas inscrições" **antes** do endpoint estar pronto, desde que o contrato (formato de entrada/saída) esteja documentado e estável. Documentação é o que permite front e back trabalharem em paralelo.
- **Onboarding.** Um novo integrante do time entende a API lendo uma página, não vasculhando 40 arquivos de rota.
- **Geração de clientes.** A partir de um documento OpenAPI, ferramentas geram automaticamente SDKs tipados em várias linguagens — você escreve o contrato uma vez, o cliente sai de graça.
- **Contrato como teste.** Ferramentas de teste de contrato conferem se a resposta real da API bate com o que foi documentado — a documentação vira uma fonte de verdade verificável, não um texto que fica defasado.

> **⚠️ Atenção**
> Documentação que não é gerada a partir do código (ou vinculada a ele por anotação) apodrece rápido: alguém muda um campo na rota e esquece de atualizar o Word/Notion separado. É exatamente esse problema que o `swagger-jsdoc` resolve — a documentação vive ao lado do código, no mesmo arquivo, na mesma revisão de código.

### 1.1 OpenAPI vs. Swagger — não são sinônimos

- **OpenAPI** é a **especificação**: um formato (YAML ou JSON) que descreve endpoints, parâmetros, corpos de requisição, respostas e esquemas de segurança de uma API REST, de forma independente de linguagem. A versão usada nesta disciplina é a **OpenAPI 3.0**.
- **Swagger** é o **conjunto de ferramentas** (hoje mantido pela SmartBear) construído em torno da especificação OpenAPI — o nome "Swagger" é anterior ao nome "OpenAPI" (a especificação se chamava Swagger Specification até a versão 2.0; a partir da 3.0 passou a se chamar OpenAPI, mas o ecossistema de ferramentas manteve o nome Swagger).

Duas ferramentas do ecossistema Swagger que usaremos hoje:

| Ferramenta | Papel |
|---|---|
| `swagger-jsdoc` | Lê anotações `@openapi` em comentários JSDoc no seu código e gera o documento OpenAPI (JSON) |
| `swagger-ui-express` | Recebe esse documento OpenAPI e renderiza uma interface HTML interativa (o "Swagger UI") |

O `swagger-ui` é a interface visual que você provavelmente já viu em várias APIs públicas — aquela página com os endpoints agrupados por tag, cada um expansível, com botão "Try it out" para testar direto do navegador.

> **🧠 Você sabia?**
> Até a versão 2.0, a especificação se chamava literalmente "Swagger Specification". Em 2015, a empresa por trás dela doou o formato para a Linux Foundation, que criou a **OpenAPI Initiative** — um consórcio com Google, Microsoft, IBM, PayPal e dezenas de outras empresas — para governar a especificação de forma neutra, sem depender de uma única companhia. Foi nesse momento que o nome do *formato* virou "OpenAPI" e o nome "Swagger" ficou só com o *conjunto de ferramentas* (que a mesma empresa continuou mantendo, hoje sob a SmartBear).

## 2. Anatomia de um documento OpenAPI 3.0

Um documento OpenAPI é um único objeto JSON (ou YAML) com estas chaves de topo:

```yaml
openapi: 3.0.0        # versão da especificação usada
info:                  # metadados da API
  title: UniEventos API
  version: 1.0.0
  description: API de eventos acadêmicos do UniEventos
servers:               # onde a API está hospedada (pode ter vários)
  - url: http://localhost:3000
    description: Ambiente local
tags:                  # agrupamento visual dos endpoints no Swagger UI
  - name: Eventos
  - name: Inscrições
  - name: Autenticação
paths:                 # cada endpoint documentado
  /api/eventos:
    get: { ... }
    post: { ... }
components:            # peças reutilizáveis entre paths
  schemas: { ... }        # formatos de objeto (Evento, EventoInput, Erro...)
  securitySchemes: { ... } # como a API autentica (ex.: bearerAuth)
```

Explicando cada bloco com o UniEventos:

- **`openapi`** — string fixa `3.0.0`, indica a versão da especificação. Não confunda com a versão da **sua** API (isso é `info.version`).
- **`info`** — título, versão e descrição da API. É o que aparece no topo do Swagger UI.
- **`servers`** — lista de URLs onde a API responde de verdade. Em desenvolvimento, `http://localhost:3000`; em produção, a URL pública (Aula 15). O Swagger UI usa isso para montar a URL completa quando você clica em "Try it out".
- **`tags`** — só organiza visualmente os endpoints em grupos colapsáveis (Eventos, Inscrições, Autenticação).
- **`paths`** — o coração do documento: cada rota (`/api/eventos`, `/api/eventos/{id}`...) e, dentro dela, cada método HTTP (`get`, `post`, `put`, `delete`), com `parameters`, `requestBody` e `responses`.
- **`components.schemas`** — formatos de objeto reutilizáveis (o formato de um `Evento`, de um `EventoInput`, de um `Erro` padrão), referenciados de dentro de `paths` com `$ref` em vez de repetidos em cada endpoint.
- **`components.securitySchemes`** — descreve **como** a API autentica (aqui, Bearer Token JWT do Firebase), sem misturar isso com a lógica de cada endpoint individual.
- **`parameters`** — parâmetros de path (`{id}`), query (`?categoria=palestra`) ou header, com tipo e descrição.
- **`requestBody`** — o formato esperado do corpo da requisição (POST/PUT), normalmente referenciando um schema via `$ref`.
- **`responses`** — para cada status HTTP possível (`200`, `400`, `404`...), o formato do corpo de resposta.
- **`$ref`** — mecanismo de referência: em vez de repetir a definição de `Evento` em 5 endpoints diferentes, cada um aponta para `#/components/schemas/Evento`. Mude uma vez, atualiza em todo lugar.

> **🔬 Investigue**
> Abra [https://petstore.swagger.io](https://petstore.swagger.io) — a "API de exemplo" oficial do ecossistema Swagger, publicada há anos exatamente para esse tipo de teste. Expanda um endpoint, clique em "Try it out" e "Execute"; depois abra a aba Network do DevTools e confira a URL exata que foi chamada — ela deve bater com o que está declarado em `servers`. Agora abra direto no navegador `https://petstore.swagger.io/v2/swagger.json`: é o documento OpenAPI cru, em JSON, o mesmo que alimenta a interface bonita que você acabou de usar. Ache, nesse JSON, a chave `paths` e conte quantos métodos HTTP diferentes o endpoint `/pet/{petId}` responde.

## 3. Duas abordagens para gerar o documento

### 3.1 Abordagem (a): anotações `@openapi` com `swagger-jsdoc` — a que vamos implementar

A ideia: você escreve um comentário JSDoc especial, com bloco YAML dentro, logo acima da definição da rota no próprio arquivo de rotas. O `swagger-jsdoc` varre os arquivos configurados, extrai esses comentários e monta o documento OpenAPI completo em tempo de execução. É a abordagem que implementamos, passo a passo, na seção "💻 Mão na massa" logo adiante.

### 3.2 Abordagem (b): `openapi.yaml` escrito à mão

A alternativa é escrever o documento OpenAPI inteiro em um arquivo `.yaml`, sem anotação nenhuma no código, e servir esse arquivo estático:

```yaml
# openapi.yaml (resumo — não é o que vamos usar hoje, é só para você conhecer a alternativa)
openapi: 3.0.0
info:
  title: UniEventos API
  version: 1.0.0
paths:
  /api/eventos:
    get:
      tags: [Eventos]
      summary: Lista eventos
      responses:
        '200':
          description: Lista de eventos
```

```js
// server.js — servindo o YAML escrito à mão, em vez de gerado por anotação
import { readFileSync } from 'node:fs'
import yaml from 'yaml' // npm install yaml
import swaggerUi from 'swagger-ui-express'

const documentoOpenApi = yaml.parse(readFileSync('./openapi.yaml', 'utf-8'))
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(documentoOpenApi))
```

Vantagem: controle total do texto, sem depender de comentário no meio do código. Desvantagem: fica fácil o YAML "descolar" do código real, porque nada obriga a atualizá-lo junto com a rota. Por isso, nesta disciplina, a abordagem oficial é a (a) — anotações junto ao código, sempre atualizadas na mesma revisão.

## 4. Além do Swagger: documentação completa do projeto

### 4.1 README de qualidade

````markdown
<!-- README.md -->
# UniEventos API

![Node.js](https://img.shields.io/badge/node-22.x-green)
![Express](https://img.shields.io/badge/express-5.2.1-blue)
![Licença](https://img.shields.io/badge/licença-MIT-lightgrey)

API REST da plataforma **UniEventos** — divulgação e inscrição em eventos acadêmicos.
Projeto desenvolvido na disciplina FACET-SNP-310 (UNEMAT/Sinop).

## Requisitos

- Node.js 22 LTS
- MySQL 8 (local ou gerenciado)
- Conta de serviço do Firebase (arquivo de credenciais)

## Instalação

```bash
git clone https://github.com/seu-usuario/unieventos-api.git
cd unieventos-api
npm install
cp .env.example .env   # preencha com suas credenciais
npm run migrar
npm run dev
```

## Variáveis de ambiente

| Variável | Descrição |
|---|---|
| `PORT` | Porta HTTP da API (padrão 3000) |
| `DB_HOST` / `DB_PORT` / `DB_USER` / `DB_PASSWORD` / `DB_NAME` | Credenciais do MySQL |
| `FIREBASE_PROJECT_ID` | Id do projeto Firebase usado na verificação de token |
| `CORS_ORIGEM_PERMITIDA` | Origem do front-end autorizada pelo CORS |

## Scripts disponíveis

| Comando | Efeito |
|---|---|
| `npm run dev` | Sobe a API com recarregamento automático |
| `npm start` | Sobe a API em modo produção |
| `npm test` | Executa a suíte de testes (vitest) |
| `npm run migrar` | Aplica migrations pendentes no banco |

## Endpoints

Documentação interativa completa em `/api-docs` (Swagger UI) com o projeto rodando.
Resumo:

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/eventos` | Lista eventos, com filtros |
| GET | `/api/eventos/:id` | Detalha um evento |
| POST | `/api/eventos` | Cria evento (autenticado) |
| PUT | `/api/eventos/:id` | Atualiza evento (autenticado) |
| DELETE | `/api/eventos/:id` | Remove evento (autenticado) |
| GET | `/api/inscricoes` | Lista inscrições do usuário logado |
| POST | `/api/inscricoes` | Inscreve o usuário em um evento |
| DELETE | `/api/inscricoes/:id` | Cancela inscrição |

## Licença

MIT — veja o arquivo LICENSE.
````

### 4.2 Coleção de API exportada

Além do Swagger UI, exporte uma coleção do Insomnia ou Postman e comite no repositório em `docs/insomnia-collection.json` — facilita quem prefere testar fora do navegador. No Insomnia: menu **Application → Preferences → Data → Export Data**, escolha a workspace do projeto, formato Insomnia v4, e salve o arquivo na pasta `docs/` do repositório.

### 4.3 `CONTRIBUTING.md` mínimo

```markdown
<!-- CONTRIBUTING.md -->
# Como contribuir

1. Crie uma branch a partir de `main`: `git checkout -b feature/nome-da-mudanca`.
2. Rode `npm test` antes de abrir o Pull Request — a suíte precisa passar.
3. Siga o padrão de nomes em português para identificadores de domínio (`eventos`, `criarEvento`).
4. Toda rota nova precisa ter anotação `@openapi` correspondente (Aula 14).
5. Abra o Pull Request descrevendo o que mudou e por quê.
```

### 4.4 Documentação do front: JSDoc em composables

```js
// src/composables/useEventos.js
/**
 * Composable que encapsula a busca e o estado de carregamento da lista de eventos.
 *
 * @param {Object} [opcoes] - opções de filtro inicial
 * @param {string} [opcoes.categoria] - categoria para filtrar a busca inicial
 * @returns {{
 *   eventos: import('vue').Ref<Array>,
 *   carregando: import('vue').Ref<boolean>,
 *   erro: import('vue').Ref<string|null>,
 *   buscarEventos: (filtros?: Object) => Promise<void>
 * }}
 */
export function useEventos(opcoes = {}) {
  // implementação já construída na Aula 06/11 — reaproveitada aqui
}
```

Comentários JSDoc em composables dão autocomplete e checagem de tipo básica no VS Code, mesmo em projetos JavaScript puro (sem TypeScript) — o editor lê o `@param`/`@returns` e sugere os campos corretos a quem consome o composable.

### 4.5 ADR — Architecture Decision Record

Um ADR é um documento curto (10 a 20 linhas) que registra **uma decisão técnica**, o contexto que levou a ela, e as alternativas consideradas — para que, meses depois, ninguém precise adivinhar "por que fizemos assim?".

**Formato em 10 linhas:**

```markdown
# ADR 0001: <título curto da decisão>

**Status:** aceito | proposto | substituído por ADR-000X
**Data:** AAAA-MM-DD

## Contexto
<qual problema motivou esta decisão>

## Decisão
<o que foi decidido>

## Consequências
<o que fica mais fácil, o que fica mais difícil, o que foi trocado por quê>
```

**Exemplo real do UniEventos:**

```markdown
<!-- docs/adr/0001-escolha-do-repository-pattern.md -->
# ADR 0001: Usar o padrão Repository para acesso a dados

**Status:** aceito
**Data:** AAAA-MM-DD

## Contexto
O service de eventos precisava consultar o MySQL diretamente, o que impedia
testar as regras de negócio (ex.: "vagas não pode ser negativo") sem subir
um banco de dados real, e acoplava o service à sintaxe SQL do mysql2.

## Decisão
Extrair toda a lógica de acesso a dados para `repositories/`, com uma
interface comum (`listar`, `buscarPorId`, `criar`, `atualizar`, `remover`),
injetada no service por parâmetro (Dependency Injection). O ambiente de
teste usa uma implementação em memória; produção usa a implementação MySQL.

## Consequências
Testes de service ficaram instantâneos e sem dependência externa. Trocar o
banco de dados (como fizemos ao avaliar Supabase na Aula 12) passou a exigir
apenas uma nova implementação de repositório, sem tocar em services ou
controllers. Custo: uma camada de indireção a mais para quem está lendo o
código pela primeira vez.
```

> **📌 Na prova**
> Um ADR não documenta código — documenta **decisão e motivo**. Se a resposta para "por que você fez assim?" está só na sua cabeça, ela vai se perder. Escrever ADRs curtos ao longo do desenvolvimento é mais barato do que reconstruir esse raciocínio depois.

## 🧩 Padrão de projeto em uso — Decorator (documentação como anotação)

O padrão **Decorator** adiciona comportamento ou informação a um objeto sem alterar sua estrutura original. As anotações `@openapi` fazem exatamente isso, só que no nível de **documentação de código-fonte** em vez de tempo de execução: o comentário JSDoc "decora" a rota com metadados (parâmetros, respostas, segurança) sem alterar uma linha da lógica real do `router.get(...)`. Remova o comentário e a rota continua funcionando idêntica — a documentação é uma camada adicionada por cima, não uma dependência funcional.

```js
/**
 * @openapi
 * /api/eventos:
 *   get:
 *     summary: Lista eventos                    ← "decoração": metadado
 *     tags: [Eventos]                            ← "decoração": metadado
 */
router.get('/', eventosController.listar)         // ← comportamento real, intocado
```

É a mesma lógica dos decorators de linguagens como TypeScript/Java (`@Component`, `@Test`) — mas aqui implementada via convenção de comentário, lida por uma ferramenta externa (`swagger-jsdoc`), porque JavaScript puro (sem TypeScript) não tem decorators nativos estáveis no runtime do Node.

## 💻 Mão na massa — documentando a unieventos-api com Swagger

Chega de teoria: agora você instala as duas bibliotecas, configura a spec, serve a interface, documenta os schemas e todos os endpoints do UniEventos, e liga a segurança `bearerAuth` — na ordem em que você faria isso de verdade num projeto novo.

### Passo 1 — Instalar e configurar o `swagger-jsdoc`

```bash
npm install swagger-jsdoc swagger-ui-express
```

```js
// src/docs/swaggerSpec.js
import swaggerJsdoc from 'swagger-jsdoc'

// ATENÇÃO: a chave é "definition", NÃO "swaggerDefinition" — swagger-jsdoc 6.x
// renomeou essa chave em relação a versões anteriores. Usar o nome errado faz
// a spec sair vazia, sem erro nenhum no console.
const opcoes = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'UniEventos API',
      version: '1.0.0',
      description:
        'API REST da plataforma UniEventos — divulgação e inscrição em eventos acadêmicos. ' +
        'Desenvolvida na disciplina FACET-SNP-310 (UNEMAT/Sinop).',
      contact: {
        name: 'Prof. Ivan Luiz Pedroso Pires',
        email: 'ivanpires@unemat.br',
      },
      license: {
        name: 'MIT',
      },
    },
    servers: [
      { url: 'http://localhost:3000', description: 'Ambiente local' },
      { url: 'https://unieventos-api.onrender.com', description: 'Produção' },
    ],
    tags: [
      { name: 'Eventos', description: 'Cadastro e consulta de eventos acadêmicos' },
      { name: 'Inscrições', description: 'Inscrição de usuários autenticados em eventos' },
      { name: 'Autenticação', description: 'Fluxo de login com Firebase Auth' },
    ],
    components: {
      securitySchemes: {
        bearerAuth: {
          type: 'http',
          scheme: 'bearer',
          bearerFormat: 'JWT',
          description: 'Token de ID do Firebase Auth, obtido após o login no front-end.',
        },
      },
    },
  },
  // Arquivos onde o swagger-jsdoc procura comentários @openapi.
  apis: ['./src/routes/*.js', './src/docs/schemas/*.js'],
}

export const swaggerSpec = swaggerJsdoc(opcoes)
```

> **⚠️ Atenção**
> Repare na chave `definition` dentro de `opcoes`. Em versões antigas do `swagger-jsdoc` (2.x/3.x) essa chave se chamava `swaggerDefinition`. Nesta disciplina usamos `swagger-jsdoc@6.3.0`, que exige `definition`. Se você copiar um tutorial antigo da internet com `swaggerDefinition`, a spec gerada fica com `paths: {}` vazio e nenhum erro é lançado — o bug é silencioso.

### Passo 2 — Servir a documentação com `swagger-ui-express`

```js
// src/app.js — trecho adicionado à montagem da aplicação (depois das rotas de negócio)
import swaggerUi from 'swagger-ui-express'
import { swaggerSpec } from './docs/swaggerSpec.js'

// Opções de customização visual do Swagger UI.
const opcoesDoSwaggerUi = {
  customSiteTitle: 'UniEventos API — Documentação',
  customCss: '.swagger-ui .topbar { display: none }', // esconde a barra verde padrão
}

app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec, opcoesDoSwaggerUi))

// Expõe o JSON cru da spec — útil para importar em Insomnia/Postman
// ou para ferramentas de geração de cliente consumirem diretamente.
app.get('/api-docs.json', (req, res) => {
  res.status(200).json(swaggerSpec)
})
```

```bash
npm run dev
# abra no navegador:
# http://localhost:3000/api-docs       → interface interativa
# http://localhost:3000/api-docs.json  → JSON cru da especificação
```

> **💡 Dica**
> `swaggerUi.serve` é um **array** de middlewares (serve os arquivos estáticos da interface: CSS, JS, HTML); `swaggerUi.setup(spec, opcoes)` é o middleware que injeta sua spec nessa interface. Os dois sempre andam juntos, nessa ordem, no mesmo `app.use`.

### Passo 3 — Documentar os schemas reutilizáveis

Antes de anotar cada rota, definimos os formatos de objeto que se repetem — assim cada endpoint só referencia (`$ref`) em vez de redigitar os mesmos campos.

```js
// src/docs/schemas/evento.schema.js
/**
 * @openapi
 * components:
 *   schemas:
 *     Evento:
 *       type: object
 *       properties:
 *         id:
 *           type: integer
 *           example: 3
 *         titulo:
 *           type: string
 *           example: Hackathon FACET
 *         descricao:
 *           type: string
 *           example: Maratona de programação de 24 horas aberta a todos os cursos.
 *         categoria:
 *           type: string
 *           enum: [palestra, minicurso, workshop]
 *           example: workshop
 *         dataHora:
 *           type: string
 *           format: date-time
 *           example: 2030-10-05T08:00:00
 *         local:
 *           type: string
 *           example: Bloco A, Auditório
 *         vagas:
 *           type: integer
 *           example: 60
 *         imagemUrl:
 *           type: string
 *           format: uri
 *           example: https://storage.unieventos.dev/eventos/hackathon.jpg
 *
 *     EventoInput:
 *       type: object
 *       required: [titulo, categoria, dataHora, local, vagas]
 *       properties:
 *         titulo:
 *           type: string
 *           minLength: 3
 *           maxLength: 150
 *         descricao:
 *           type: string
 *         categoria:
 *           type: string
 *           enum: [palestra, minicurso, workshop]
 *         dataHora:
 *           type: string
 *           format: date-time
 *         local:
 *           type: string
 *         vagas:
 *           type: integer
 *           minimum: 0
 *         imagemUrl:
 *           type: string
 *           format: uri
 *
 *     Erro:
 *       type: object
 *       description: Envelope único de erro da API, fixado na Aula 08.
 *       properties:
 *         erro:
 *           type: object
 *           properties:
 *             mensagem:
 *               type: string
 *               example: Evento não encontrado
 *             codigo:
 *               type: string
 *               example: NAO_ENCONTRADO
 *             detalhes:
 *               type: array
 *               description: Presente apenas em erros de validação (422).
 *               items:
 *                 type: object
 *                 properties:
 *                   campo:
 *                     type: string
 *                   mensagem:
 *                     type: string
 *
 *     Paginacao:
 *       type: object
 *       properties:
 *         pagina:
 *           type: integer
 *           example: 1
 *         porPagina:
 *           type: integer
 *           example: 20
 *         total:
 *           type: integer
 *           example: 47
 *         totalPaginas:
 *           type: integer
 *           example: 3
 *
 *     ListaDeEventos:
 *       type: object
 *       description: Envelope de listagem da API — { dados, paginacao }.
 *       properties:
 *         dados:
 *           type: array
 *           items:
 *             $ref: '#/components/schemas/Evento'
 *         paginacao:
 *           $ref: '#/components/schemas/Paginacao'
 */
export {} // arquivo só existe para hospedar o comentário — sem código de fato
```

```js
// src/docs/schemas/inscricao.schema.js
/**
 * @openapi
 * components:
 *   schemas:
 *     Inscricao:
 *       type: object
 *       properties:
 *         id:
 *           type: integer
 *           example: 12
 *         eventoId:
 *           type: integer
 *           example: 3
 *         usuarioUid:
 *           type: string
 *           example: fY3k9sLp2QaB1cD4eF5gH6iJ7kL8
 *         criadoEm:
 *           type: string
 *           format: date-time
 *
 *     InscricaoInput:
 *       type: object
 *       required: [eventoId]
 *       properties:
 *         eventoId:
 *           type: integer
 *           example: 3
 */
export {}
```

> **🔎 Por baixo do capô**
> Esses arquivos `*.schema.js` não exportam nada útil em termos de código JavaScript — servem só para o `swagger-jsdoc` encontrar o comentário (por isso estão incluídos em `apis: [...]` na configuração do Passo 1). É uma convenção comum para não poluir arquivos de rota reais com blocos de schema grandes.

### Passo 4 — Documentar os endpoints do UniEventos

#### Eventos — as 5 operações (CRUD completo)

```js
// src/routes/eventos.routes.js — versão anotada
import { Router } from 'express'
import { validar } from '../middlewares/validar.js'
import { eventoSchema, eventoAtualizacaoSchema } from '../validators/eventoSchema.js'
import { autenticar } from '../middlewares/autenticar.js'
import { autorizar } from '../middlewares/autorizar.js'

export function criarRotasDeEventos({ eventosController }) {
  const router = Router()

  /**
   * @openapi
   * /api/eventos:
   *   get:
   *     summary: Lista eventos, com filtros opcionais
   *     tags: [Eventos]
   *     parameters:
   *       - in: query
   *         name: categoria
   *         schema:
   *           type: string
   *           enum: [palestra, minicurso, workshop]
   *         description: Filtra por categoria do evento
   *       - in: query
   *         name: busca
   *         schema:
   *           type: string
   *         description: Filtra por trecho do título
   *       - in: query
   *         name: pagina
   *         schema:
   *           type: integer
   *           default: 1
   *       - in: query
   *         name: porPagina
   *         schema:
   *           type: integer
   *           default: 20
   *     responses:
   *       200:
   *         description: Lista paginada de eventos, no envelope { dados, paginacao }
   *         content:
   *           application/json:
   *             schema:
   *               $ref: '#/components/schemas/ListaDeEventos'
   */
  router.get('/', eventosController.listar)

  /**
   * @openapi
   * /api/eventos/{id}:
   *   get:
   *     summary: Busca um evento pelo id
   *     tags: [Eventos]
   *     parameters:
   *       - in: path
   *         name: id
   *         required: true
   *         schema:
   *           type: integer
   *         description: Id numérico do evento
   *     responses:
   *       200:
   *         description: Evento encontrado
   *         content:
   *           application/json:
   *             schema:
   *               $ref: '#/components/schemas/Evento'
   *       404:
   *         description: Evento não encontrado
   *         content:
   *           application/json:
   *             schema:
   *               $ref: '#/components/schemas/Erro'
   */
  router.get('/:id', eventosController.buscarPorId)

  /**
   * @openapi
   * /api/eventos:
   *   post:
   *     summary: Cria um novo evento
   *     tags: [Eventos]
   *     security:
   *       - bearerAuth: []
   *     requestBody:
   *       required: true
   *       content:
   *         application/json:
   *           schema:
   *             $ref: '#/components/schemas/EventoInput'
   *     responses:
   *       201:
   *         description: Evento criado
   *         content:
   *           application/json:
   *             schema:
   *               $ref: '#/components/schemas/Evento'
   *       400:
   *         description: Dados inválidos
   *         content:
   *           application/json:
   *             schema:
   *               $ref: '#/components/schemas/Erro'
   *       401:
   *         description: Token ausente ou inválido
   *         content:
   *           application/json:
   *             schema:
   *               $ref: '#/components/schemas/Erro'
   */
  router.post('/', autenticar, validar(eventoSchema), eventosController.criar)

  /**
   * @openapi
   * /api/eventos/{id}:
   *   put:
   *     summary: Atualiza um evento existente
   *     tags: [Eventos]
   *     security:
   *       - bearerAuth: []
   *     parameters:
   *       - in: path
   *         name: id
   *         required: true
   *         schema:
   *           type: integer
   *     requestBody:
   *       required: true
   *       content:
   *         application/json:
   *           schema:
   *             $ref: '#/components/schemas/EventoInput'
   *     responses:
   *       200:
   *         description: Evento atualizado
   *         content:
   *           application/json:
   *             schema:
   *               $ref: '#/components/schemas/Evento'
   *       404:
   *         description: Evento não encontrado
   *         content:
   *           application/json:
   *             schema:
   *               $ref: '#/components/schemas/Erro'
   */
  router.put('/:id', autenticar, validar(eventoAtualizacaoSchema), eventosController.atualizar)

  /**
   * @openapi
   * /api/eventos/{id}:
   *   delete:
   *     summary: Remove um evento
   *     tags: [Eventos]
   *     security:
   *       - bearerAuth: []
   *     parameters:
   *       - in: path
   *         name: id
   *         required: true
   *         schema:
   *           type: integer
   *     responses:
   *       204:
   *         description: Evento removido com sucesso, sem corpo de resposta
   *       404:
   *         description: Evento não encontrado
   *         content:
   *           application/json:
   *             schema:
   *               $ref: '#/components/schemas/Erro'
   */
  router.delete('/:id', autenticar, autorizar(['admin']), eventosController.remover)

  return router
}
```

#### Inscrições

```js
// src/routes/inscricoes.routes.js — versão anotada
import { Router } from 'express'
import { validar } from '../middlewares/validar.js'
import { inscricaoSchema } from '../validators/inscricaoSchema.js'
import { autenticar } from '../middlewares/autenticar.js'
import { autorizar } from '../middlewares/autorizar.js'

export function criarRotasDeInscricoes({ inscricoesController }) {
  const router = Router()

  /**
   * @openapi
   * /api/inscricoes:
   *   get:
   *     summary: Lista as inscrições do usuário autenticado
   *     tags: [Inscrições]
   *     security:
   *       - bearerAuth: []
   *     responses:
   *       200:
   *         description: Lista de inscrições do usuário logado
   *         content:
   *           application/json:
   *             schema:
   *               type: array
   *               items:
   *                 $ref: '#/components/schemas/Inscricao'
   *       401:
   *         description: Token ausente ou inválido
   */
  router.get('/', autenticar, inscricoesController.listarMinhas)

  /**
   * @openapi
   * /api/inscricoes:
   *   post:
   *     summary: Inscreve o usuário autenticado em um evento
   *     tags: [Inscrições]
   *     security:
   *       - bearerAuth: []
   *     requestBody:
   *       required: true
   *       content:
   *         application/json:
   *           schema:
   *             $ref: '#/components/schemas/InscricaoInput'
   *     responses:
   *       201:
   *         description: Inscrição criada
   *         content:
   *           application/json:
   *             schema:
   *               $ref: '#/components/schemas/Inscricao'
   *       409:
   *         description: Usuário já está inscrito neste evento
   *         content:
   *           application/json:
   *             schema:
   *               $ref: '#/components/schemas/Erro'
   */
  router.post('/', autenticar, validar(inscricaoSchema), inscricoesController.criar)

  /**
   * @openapi
   * /api/inscricoes/{id}:
   *   delete:
   *     summary: Cancela uma inscrição do próprio usuário
   *     tags: [Inscrições]
   *     security:
   *       - bearerAuth: []
   *     parameters:
   *       - in: path
   *         name: id
   *         required: true
   *         schema:
   *           type: integer
   *     responses:
   *       204:
   *         description: Inscrição cancelada
   *       403:
   *         description: A inscrição pertence a outro usuário
   *         content:
   *           application/json:
   *             schema:
   *               $ref: '#/components/schemas/Erro'
   */
  router.delete('/:id', autenticar, inscricoesController.cancelar)

  return router
}
```

#### Autenticação

O UniEventos não implementa login no back-end — o login acontece no front, direto contra o Firebase Auth (Aula 10). O back-end só **verifica** o token recebido. Ainda assim, documentamos esse fluxo, porque quem consumir a API precisa saber como obter o token:

```js
// src/routes/autenticacao.routes.js
import { Router } from 'express'
import { autenticar } from '../middlewares/autenticar.js'

export function criarRotasDeAutenticacao() {
  const router = Router()

  /**
   * @openapi
   * /api/auth/verificar:
   *   get:
   *     summary: Confirma se o token enviado é válido e devolve os dados do usuário
   *     description: >
   *       Não existe endpoint de login nesta API — o login acontece no front-end,
   *       diretamente contra o Firebase Auth (signInWithEmailAndPassword). Este
   *       endpoint serve apenas para confirmar que um token de ID do Firebase é válido.
   *     tags: [Autenticação]
   *     security:
   *       - bearerAuth: []
   *     responses:
   *       200:
   *         description: Token válido
   *         content:
   *           application/json:
   *             schema:
   *               type: object
   *               properties:
   *                 uid:
   *                   type: string
   *                 email:
   *                   type: string
   *       401:
   *         description: Token ausente, expirado ou inválido
   *         content:
   *           application/json:
   *             schema:
   *               $ref: '#/components/schemas/Erro'
   */
  // o `autenticar` NÃO é decorativo: é ele que valida o token e preenche
  // `req.usuario`. Sem ele, a anotação promete 401 e o handler estoura 500.
  router.get('/verificar', autenticar, (req, res) => {
    res.status(200).json({ uid: req.usuario.uid, email: req.usuario.email })
  })

  return router
}
```

### Passo 5 — Segurança com bearerAuth e o botão "Authorize"

O esquema `bearerAuth` já foi declarado em `components.securitySchemes` (Passo 1):

```yaml
securitySchemes:
  bearerAuth:
    type: http
    scheme: bearer
    bearerFormat: JWT
```

Cada endpoint protegido referencia esse esquema com `security: [{ bearerAuth: [] }]` (como fizemos em `POST /api/eventos`, `PUT /api/eventos/{id}`, `DELETE /api/eventos/{id}` e todas as rotas de inscrições). O efeito no Swagger UI:

1. Um cadeado aparece ao lado de cada operação protegida.
2. Um botão verde **"Authorize"** aparece no topo da página.
3. Clicar nele abre um campo para colar o token — só o token puro, sem o prefixo `Bearer` (o Swagger UI adiciona isso sozinho no cabeçalho `Authorization`).
4. Depois de autorizado, todo "Try it out" em endpoint protegido já envia o cabeçalho automaticamente.

> **💡 Dica**
> Para obter um token de teste rápido, abra o console do navegador na sua aplicação front-end já logada e rode:
> ```js
> import { getAuth } from 'firebase/auth'
> const token = await getAuth().currentUser.getIdToken()
> console.log(token)
> ```
> Copie o valor impresso e cole no botão "Authorize" do Swagger UI.

### Como testar

1. Abra `http://localhost:3000/api-docs`.
2. Expanda `GET /api/eventos`, clique em **"Try it out"**, depois em **"Execute"** — a resposta real da API aparece embaixo, com status e corpo formatado.
3. Para testar `POST /api/eventos`, clique em **"Authorize"** primeiro (Passo 5), depois expanda a operação, edite o JSON de exemplo no campo de corpo, e execute.

Resultado esperado: as chamadas respondem com o status e o corpo documentados — `GET /api/eventos` devolve o envelope `{ dados, paginacao }` exatamente como o schema `ListaDeEventos` promete; `POST /api/eventos` sem autorizar devolve `401` no envelope `{ erro: { mensagem, codigo } }`; depois do "Authorize", devolve `201` com o evento criado. Se a resposta real e o exemplo documentado divergirem em **qualquer** campo, a documentação está mentindo — conserte o schema, não o print.

> **⚠️ Atenção — CORS e `servers`**
> O Swagger UI faz a requisição **do navegador**, então as mesmas regras de CORS da Aula 13 se aplicam: se `servers` apontar para uma URL diferente da que está rodando o front (ou se a API não liberar a origem da própria página do Swagger UI), o "Try it out" falha com erro de CORS no console — mesmo a API estando no ar. Garanta que `CORS_ORIGEM_PERMITIDA` inclua a origem de onde o Swagger UI está sendo servido (geralmente a própria API, `http://localhost:3000`, o que já é liberado por padrão pelo mesmo processo).

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Verdadeiro ou falso, com justificativa de uma linha: "`swagger-jsdoc` gera a documentação automaticamente a partir dos tipos declarados nas funções JavaScript, sem precisar de comentário nenhum."

Resultado esperado: falso — o `swagger-jsdoc` só lê comentários `@openapi` com bloco YAML dentro; ele não infere nada a partir da assinatura de funções ou do corpo do código.

**A2.** Complete a linha que falta para que as opções abaixo gerem a spec corretamente na versão 6.x do `swagger-jsdoc`:

```js
const opcoes = {
  ______________: { openapi: '3.0.0', info: { title: 'UniEventos API', version: '1.0.0' } },
  apis: ['./src/routes/*.js'],
}
```

Resultado esperado: `definition` (nunca `swaggerDefinition`, que é a chave das versões antigas 2.x/3.x).

**A3.** Em uma frase: qual a diferença entre OpenAPI e Swagger?

Resultado esperado: OpenAPI é a **especificação** — o formato que descreve a API; Swagger é o **conjunto de ferramentas** (`swagger-jsdoc`, `swagger-ui-express`) construído em torno dessa especificação.

**A4.** Ache o erro nas linhas abaixo (o Swagger UI mostra "not found" ao tentar exibir o exemplo do corpo de resposta):

```yaml
responses:
  200:
    content:
      application/json:
        schema:
          $ref: '#/components/schema/Evento'
```

Resultado esperado: falta o "s" em "schemas" — o caminho correto é `#/components/schemas/Evento`.

**A5.** Preveja a saída: dois endpoints diferentes referenciam `$ref: '#/components/schemas/Erro'`. Você muda um campo desse schema. Quantos lugares no Swagger UI mostram a mudança?

Resultado esperado: todos os endpoints que referenciam esse schema por `$ref` mudam juntos, imediatamente — é justamente a vantagem de não repetir a definição em cada endpoint.

### Nível B — Aplicação

**B1.** Configure `swagger-jsdoc` e `swagger-ui-express` no seu projeto autoral, com `definition` (não `swaggerDefinition`), `info`, pelo menos uma `tag` e o `securityScheme` `bearerAuth`.

Resultado esperado: `http://localhost:3000/api-docs` abre com o título e a descrição da sua API.

<details markdown="1">
<summary>Dica</summary>

Copie `src/docs/swaggerSpec.js` do Passo 1 e troque só o `title`, `description` e as `tags` para o domínio do seu projeto.
</details>

**B2.** Documente 3 endpoints do seu projeto autoral com anotações `@openapi` completas (parâmetros, requestBody quando houver, respostas para pelo menos 2 status diferentes).

Resultado esperado: os 3 endpoints aparecem expansíveis no Swagger UI, com exemplos de corpo preenchidos.

<details markdown="1">
<summary>Dica</summary>

Comece pelo endpoint de listagem (mais simples, sem `requestBody`) e depois avance para um de criação (com `requestBody` e `security`).
</details>

**B3.** Teste um endpoint protegido pelo "Authorize" — obtenha um token do Firebase (Passo 5) e confirme que a requisição autenticada funciona pelo Swagger UI.

Resultado esperado: sem token, a rota protegida retorna `401`; com token válido, retorna `200`/`201`.

<details markdown="1">
<summary>Dica</summary>

Se a resposta continuar `401` mesmo com token colado, confira se você colou só o token puro, sem o prefixo `Bearer `.
</details>

**B4.** Escreva um ADR para uma decisão técnica real do seu projeto (ex.: por que escolheu MySQL ou Supabase, por que escolheu determinado padrão de rota).

Resultado esperado: arquivo `docs/adr/0001-<slug>.md` seguindo o formato de 10 linhas da Seção 4.5.

<details markdown="1">
<summary>Dica</summary>

Escolha uma decisão que você realmente tomou e hesitou entre alternativas — é mais fácil escrever o "Contexto" quando a dúvida foi real.
</details>

### Nível C — Desafio em sala

**C1.** Crie os schemas reutilizáveis da entidade principal do seu domínio (equivalente a `Evento`/`EventoInput`/`Erro`/`Paginacao`) e referencie com `$ref` nos 3 endpoints do exercício B2 — nenhum campo pode ser redigitado à mão dentro de uma anotação de rota.

Resultado esperado: mudar um campo no schema reflete automaticamente em todos os endpoints que o referenciam, sem editar nenhuma rota; o Swagger UI mostra o mesmo exemplo de corpo em todas elas.

<details markdown="1">
<summary>Dica</summary>

Coloque os schemas em `src/docs/schemas/*.schema.js` e inclua o caminho no array `apis` da configuração do `swagger-jsdoc` (Passo 1) — sem isso, o arquivo do schema é ignorado silenciosamente.
</details>

## 🏆 Desafios

### ⭐ As tags sumidas
Tags: swagger, api, bug, investigacao

Um colega documentou um novo endpoint `PATCH /api/eventos/{id}/destaque` (marca um evento como destaque na home) com uma anotação `@openapi` completa — mas o Swagger UI insiste em mostrar essa operação isolada, fora dos grupos "Eventos"/"Inscrições"/"Autenticação", num grupo solto chamado "default" no fim da página. Antes de olhar o código, abra `/api-docs` do seu projeto e investigue: o que diferencia visualmente uma operação agrupada de uma "solta"?

**Critérios de pronto**

- Um comentário registra qual chave do bloco `@openapi` **da operação** (não da configuração global) estava faltando.
- Depois de corrigida, a operação aparece dentro do grupo correto no Swagger UI.
- Uma frase explica a diferença entre a lista `tags` da configuração global (`definition.tags`, Passo 1) e a lista `tags: [...]` escrita dentro de cada anotação de rota — os dois têm o mesmo nome, mas papéis diferentes.
- Você documenta pelo menos um outro endpoint do seu projeto autoral usando o mesmo padrão de agrupamento, para confirmar que entendeu a diferença.

<details markdown="1">
<summary>Pistas</summary>

1. Compare a anotação da operação "solta" com uma que aparece agrupada corretamente — falta exatamente uma chave dentro do bloco `@openapi` da operação.
2. `tags` na configuração global só declara o **nome** e a **descrição** do grupo — quem coloca de fato uma operação dentro dele é o `tags: [...]` escrito na anotação de cada rota.
3. Depois de corrigir, reinicie a API (ou deixe `npm run dev` reiniciar sozinho, já que ele roda com `--watch`) e recarregue `/api-docs` — a spec só é montada de novo quando o módulo `swaggerSpec.js` é reimportado.
</details>

### ⭐⭐ O schema que não bate mais
Tags: swagger, refatoracao, api, json

Reproduza no seu repositório uma divergência que acontece o tempo todo em projeto real. Renomeie, **só no `linhaParaEvento` do repositório**, o campo `imagemUrl` para `urlDaImagem`, e ajuste a anotação Swagger de `GET /api/eventos/{id}` — e apenas ela — para o nome novo. Suba a API: agora `GET /api/eventos` (a listagem) documenta `imagemUrl`, `GET /api/eventos/{id}` documenta `urlDaImagem`, e as duas devolvem a mesma coisa. Quem está integrando o front pelo Swagger UI vai escrever código para um campo que não existe na metade das respostas. Encontre a causa estrutural dessa divergência e conserte — sem editar o mesmo nome de campo em três lugares diferentes.

**Critérios de pronto**

- Ao final, o campo volta a se chamar `imagemUrl` (o nome do contrato da trilha) e aparece igual em **todas** as operações que retornam um evento.
- A correção acontece em **um único lugar** (o schema `Evento` em `components.schemas`), referenciado por `$ref` em todos os endpoints — não copiado em cada anotação de rota.
- Um teste manual (`curl` num endpoint real) confirma que o nome do campo na resposta bate exatamente com o que a documentação promete.
- Um comentário de uma linha explica por que documentar o mesmo campo em vários lugares (em vez de usar `$ref`) foi o que permitiu essa divergência passar despercebida.

<details markdown="1">
<summary>Pistas</summary>

1. Procure todas as ocorrências do nome antigo do campo dentro de `src/docs/schemas/` e `src/routes/` — um `grep -r` no terminal encontra rápido.
2. Se um endpoint declarar o exemplo do corpo "na mão", em vez de usar `$ref: '#/components/schemas/Evento'`, ele fica exposto a esse tipo de esquecimento — troque para `$ref` sempre que possível.
3. Depois de corrigir o schema, confirme visualmente no Swagger UI que o exemplo de **todas** as operações relacionadas ao evento mudou junto.
</details>

### ⭐⭐⭐ Documentação como teste de contrato
Tags: testes, api, swagger, ci-cd

Na Seção 1 você leu que "documentação vira uma fonte de verdade verificável" quando existe uma ferramenta de teste de contrato comparando a resposta real com o que foi documentado. Hoje isso ainda é só teoria no UniEventos: nada garante que a resposta real de `GET /api/eventos` continua batendo com o schema `Evento` documentado depois de um refactor. Construa esse teste de contrato mínimo, sem depender de biblioteca externa pesada.

**Critérios de pronto**

- Um script `scripts/testar-contrato.js` busca `/api-docs.json`, extrai o schema `Evento` de `components.schemas`, faz uma chamada real a `GET /api/eventos`, e confere que cada campo obrigatório do schema existe na resposta real e bate com o `type` declarado (string, integer etc.).
- O script termina com código de saída diferente de zero e uma mensagem clara se algum campo estiver faltando ou com tipo errado.
- Um teste proposital: remova temporariamente um campo do controller que monta a resposta de `/api/eventos` e confirme que o script acusa a divergência.
- O script está incluído como um passo do workflow de CI (ou de um script `npm`), rodando antes ou depois da suíte de testes de unidade.

<details markdown="1">
<summary>Pistas</summary>

1. `fetch('http://localhost:3000/api-docs.json')` devolve o JSON completo da spec — o schema fica em `components.schemas.Evento.properties`.
2. Para cada chave de `properties`, confira `typeof valorReal` contra o `type` declarado (`"integer"`/`"number"` → `typeof === 'number'`; `"string"` → `typeof === 'string'`).
3. Registre o script como um script `npm` (ex.: `"testar:contrato": "node scripts/testar-contrato.js"`).
4. Não tente validar formatos complexos (`date-time`, `uri`) de início — comece só conferindo presença do campo e o tipo primitivo.
</details>

## 🐛 Erros comuns e como resolver

| Sintoma | Causa | Solução |
|---|---|---|
| `/api-docs` abre, mas `paths` está vazio | Usou a chave `swaggerDefinition` em vez de `definition` nas opções do `swagger-jsdoc` | Troque para `definition` — é a chave exigida na versão 6.x |
| Endpoint documentado não aparece no Swagger UI | O arquivo onde está o comentário `@openapi` não está listado em `apis: [...]` | Adicione o caminho (ou glob) do arquivo à lista `apis` da configuração |
| `$ref: '#/components/schemas/Evento'` gera erro "not found" | O schema `Evento` não foi anotado em nenhum arquivo varrido pelo `apis` | Confira se `src/docs/schemas/evento.schema.js` está no array `apis` e se o YAML do comentário está corretamente indentado |
| Botão "Authorize" não aparece | Nenhum endpoint tem `security: [{ bearerAuth: [] }]`, ou `securitySchemes` não foi declarado em `components` | Declare `securitySchemes.bearerAuth` em `definition.components` e adicione `security` nos endpoints protegidos |
| "Try it out" falha com erro de CORS | A origem da própria página do Swagger UI não está liberada pelo middleware de CORS da API | Garanta que a origem da API (onde o `/api-docs` é servido) está coberta pela configuração de CORS, ou sirva o Swagger UI na mesma origem da API |
| YAML do comentário `@openapi` quebra a spec inteira silenciosamente | Indentação incorreta no bloco YAML dentro do comentário JSDoc | YAML é sensível a espaços — nunca misture tabs, use 2 espaços por nível, consistentemente |

## 🏠 Atividade assíncrona (1 h)

1. Documente **todos** os endpoints do seu projeto autoral com anotações `@openapi` (não só os 3 do laboratório).
2. Garanta que os schemas `Erro` e de paginação (se aplicável) estão presentes e referenciados.
3. Revise o `README.md` seguindo a estrutura da Seção 4.1: badges, requisitos, instalação, variáveis de ambiente, scripts, endpoints (com link para `/api-docs`), licença.
4. Escreva pelo menos 1 ADR adicional sobre uma decisão do seu back-end.

**Critério de pronto:** `/api-docs` mostra 100% dos endpoints do projeto autoral documentados; README revisado; ao menos 2 ADRs no repositório.

## ✅ Checkpoint do projeto autoral

Ao final desta aula, seu repositório `<tema>-api` deve ter:

- [ ] `swagger-jsdoc` configurado com a chave `definition` e `swagger-ui-express` servindo em `/api-docs`.
- [ ] `/api-docs.json` expondo a spec crua.
- [ ] Schemas reutilizáveis (`$ref`) para a entidade principal, incluindo um schema de `Erro`.
- [ ] `securityScheme` `bearerAuth` configurado e usado em todos os endpoints protegidos.
- [ ] README revisado com badges, instalação, variáveis de ambiente, scripts e tabela de endpoints.
- [ ] Pasta `docs/adr/` com pelo menos 2 registros de decisão.

## 📚 Para aprofundar

- [Especificação OpenAPI 3.0 (oficial)](https://spec.openapis.org/oas/v3.0.3)
- [swagger-jsdoc — repositório no GitHub](https://github.com/Surnet/swagger-jsdoc)
- [swagger-ui-express — repositório no GitHub](https://github.com/scottie1984/swagger-ui-express)
- [Swagger.io — guia oficial de OpenAPI](https://swagger.io/docs/specification/about/)
- [ADR GitHub organization — modelos de Architecture Decision Record](https://adr.github.io)
- [Keep a README — checklist do que compõe um bom README](https://www.makeareadme.com/)
- Bibliografia do plano de curso FACET-SNP-310 — capítulos sobre documentação de APIs REST e contratos de serviço.

**Na Aula 15** fechamos o semestre com deploy real (front e back), CI/CD com GitHub Actions, retrospectiva de todos os padrões de projeto usados, guia de estudo para o exame final e as instruções completas da Avaliação 3. Traga a API documentada e pronta para publicar.
