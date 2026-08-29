# Aula 15 — Deploy, apresentação e finalização

> **Nível 3 — Frameworks Modernos** · Unidade 3: Integração front-end/back-end
> WebLab · UNEMAT Sinop · Prof. Ivan Luiz Pedroso Pires

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Gerar o build de produção de uma aplicação Vue com Vite e explicar o que existe dentro de `dist/`.
- Publicar o front-end em um serviço de hospedagem estática (Vercel, Firebase Hosting ou GitHub Pages), configurando variáveis de ambiente e rewrite de SPA.
- Publicar o back-end Express em um serviço de nuvem, com `PORT` dinâmico, health check e variáveis de ambiente seguras.
- Escrever um `Dockerfile` simples para a API e um `docker-compose.yml` com API + MySQL.
- Diagnosticar e corrigir os erros mais comuns pós-deploy (CORS, mixed content, 404 em rota interna, banco inacessível).
- Configurar um pipeline básico de CI/CD no GitHub Actions que roda lint e testes a cada push.
- Relacionar cada padrão de projeto estudado no semestre ao trecho de código onde ele apareceu no UniEventos.
- Apresentar o projeto autoral em formato de seminário técnico, dentro do tempo e critérios definidos.
- Entregar a Avaliação 3 seguindo integralmente os requisitos e o prazo estabelecidos.

## 📋 Pré-requisitos desta aula

- `unieventos-api` (ou projeto autoral) com arquitetura em camadas (Aula 13) e documentação Swagger (Aula 14) completas.
- Front-end (`unieventos-web` ou equivalente) com build funcionando localmente (`npm run build` sem erro).
- Conta gratuita em pelo menos um serviço de hospedagem de front (Vercel, Netlify, Firebase Hosting ou GitHub Pages) e um de back (Render, Railway ou Fly.io).
- Repositórios do projeto autoral publicados e atualizados no GitHub.

Checklist antes de começar:

- [ ] `npm run build` do front gera a pasta `dist/` sem erro.
- [ ] `npm test` do back passa localmente.
- [ ] Você tem acesso de administrador aos dois repositórios (front e back) no GitHub.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Build de produção, deploy do front e do back, Docker, CORS em produção |
| 2 | 50 min | CI/CD com GitHub Actions, retrospectiva de padrões de projeto, guia de estudo do exame final |
| 3 | 50 min | Instruções da Avaliação 3, formato do seminário, encerramento da disciplina |

## Retomando a Aula 14

Na Aula 14 documentamos a API inteira com OpenAPI e Swagger UI — qualquer pessoa consegue entender e testar o UniEventos sem ler uma linha de código. Falta uma última etapa: tirar o projeto do `localhost` e colocá-lo no ar, com URL pública, para qualquer pessoa acessar. Hoje fechamos esse ciclo — e fechamos o semestre.

## 1. Build de produção do front-end

### 1.1 O que `npm run build` faz

```bash
cd unieventos-web
npm run build
```

O Vite lê `src/`, resolve todos os imports, faz **tree-shaking** (remove código não utilizado), minifica JavaScript e CSS, gera hashes nos nomes de arquivo (para cache eficiente no navegador) e escreve tudo em `dist/`:

```text
dist/
├─ assets/
│  ├─ index-BvPPrto3.css     ← todo o CSS do projeto, minificado
│  ├─ index-EL0WAqE7.js      ← todo o JavaScript, empacotado e minificado
│  └─ materialdesignicons-*.woff2  ← fontes de ícone do @mdi/font
├─ favicon.ico
└─ index.html                ← HTML final, já referenciando os assets com hash
```

> **🔎 Por baixo do capô**
> O hash no nome do arquivo (`index-BvPPrto3.js`) muda sempre que o conteúdo muda. Isso permite configurar cache agressivo e "para sempre" nesses arquivos no servidor: o navegador só baixa de novo se o hash (e portanto o conteúdo) mudou. O `index.html`, em contrapartida, nunca deve ser cacheado agressivamente — ele é o que aponta para os hashes corretos a cada novo deploy.

`dist/` é **tudo** que o servidor de hospedagem precisa: arquivos estáticos, sem Node.js rodando por trás. É por isso que hospedar um front-end Vue construído é barato (ou gratuito) — não é um processo de servidor, é só arquivos.

### 1.2 Variáveis de ambiente do Vite

O Vite só expõe ao código do navegador variáveis de ambiente prefixadas com `VITE_` — qualquer outra fica de fora do bundle final, por segurança (evita vazar segredos de build no JavaScript público).

```bash
# .env.production — lido automaticamente quando NODE_ENV=production (no build)
VITE_API_URL=https://unieventos-api.onrender.com
VITE_FIREBASE_API_KEY=AIzaSy...
VITE_FIREBASE_AUTH_DOMAIN=unieventos.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=unieventos
```

```bash
# .env.development — lido em npm run dev
VITE_API_URL=http://localhost:3000
VITE_FIREBASE_API_KEY=AIzaSy...
VITE_FIREBASE_AUTH_DOMAIN=unieventos.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=unieventos
```

```js
// src/services/apiClient.js — uso da variável, como já fazemos desde a Aula 06
import axios from 'axios'

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL, // troca sozinho entre dev e produção
})
```

> **⚠️ Atenção**
> `import.meta.env.VITE_*` só existe em tempo de **build** — o Vite substitui essas referências por valores literais no JavaScript final. Trocar a variável depois do build (por exemplo, direto no painel do serviço de hospedagem, sem rebuildar) **não tem efeito nenhum**: você precisa gerar um novo build para que um novo valor de `VITE_API_URL` entre no bundle. Serviços como Vercel fazem isso automaticamente a cada push, rodando `npm run build` de novo.

### 1.3 `base` no `vite.config.js`

Se o site for publicado em um subcaminho (comum no GitHub Pages, ex.: `usuario.github.io/unieventos-web/`), configure `base`:

```js
// vite.config.js — trecho relevante para deploy em subcaminho
export default defineConfig({
  base: '/unieventos-web/', // necessário só se NÃO estiver na raiz do domínio
  plugins: [
    vue({ template: { transformAssetUrls } }),
    vuetify({ autoImport: true }),
  ],
})
```

Em Vercel, Netlify e Firebase Hosting, o projeto normalmente fica na raiz do domínio (`base: '/'`, o padrão) — só ajuste isso para GitHub Pages em repositório de projeto (não em `usuario.github.io`).

### 1.4 Por que SPA precisa de rewrite para `index.html`

Uma SPA como o UniEventos tem **uma única página real** (`index.html`); rotas como `/eventos/3` ou `/minhas-inscricoes` só existem no navegador, resolvidas pelo Vue Router (Aula 04) via History API — o servidor nunca teve, e nunca terá, um arquivo físico chamado `eventos/3`.

O problema: se o usuário aperta **F5** (recarrega a página) estando em `/eventos/3`, o navegador faz uma requisição HTTP real, ao servidor, pedindo o caminho `/eventos/3`. Um servidor de arquivos estáticos comum não encontra esse arquivo e responde `404`.

A solução é configurar o servidor para, em qualquer caminho que não seja um arquivo estático real, devolver `index.html` — o Vue Router então assume o controle no navegador e resolve a rota `/eventos/3` normalmente.

```json
// vercel.json — rewrite de SPA na Vercel
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

```text
# _redirects — Netlify (arquivo dentro de public/, copiado para dist/ no build)
/*  /index.html  200
```

```json
// firebase.json — trecho relevante do Firebase Hosting
{
  "hosting": {
    "public": "dist",
    "rewrites": [
      { "source": "**", "destination": "/index.html" }
    ]
  }
}
```

> **📌 Na prova**
> "F5 em rota interna dá 404" é o sintoma mais clássico de rewrite de SPA mal configurado. Sempre que alguém relatar esse erro pós-deploy, a primeira pergunta é: "o servidor está configurado para devolver `index.html` em qualquer caminho desconhecido?"

## 2. Deploy do front-end

### 2.1 Vercel (recomendado — passo a passo testado)

1. Crie conta em [vercel.com](https://vercel.com) usando login do GitHub.
2. No painel, clique **"Add New... → Project"** e selecione o repositório `unieventos-web`.
3. A Vercel detecta automaticamente que é um projeto Vite. Confirme:
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
4. Antes de clicar em "Deploy", adicione as variáveis de ambiente na seção **Environment Variables**: `VITE_API_URL`, `VITE_FIREBASE_API_KEY`, `VITE_FIREBASE_AUTH_DOMAIN`, `VITE_FIREBASE_PROJECT_ID` — os mesmos valores do seu `.env.production` local.
5. Clique **Deploy**. Em cerca de 1 minuto, a Vercel devolve uma URL pública (`https://unieventos-web.vercel.app`).
6. A cada `git push` na branch `main`, a Vercel refaz o deploy automaticamente.

> **💡 Dica**
> A Vercel também cria um **preview deploy** automático para cada Pull Request, com URL própria — ótimo para revisar uma feature antes de mesclar em `main`, mas não obrigatório nesta disciplina.

### 2.2 Alternativa: Firebase Hosting

```bash
npm install -g firebase-tools
firebase login
firebase init hosting
# Public directory: dist
# Configure as a single-page app (rewrite all urls to /index.html)? Yes
# Set up automatic builds and deploys with GitHub? (opcional, responda conforme preferir)

npm run build
firebase deploy --only hosting
```

Como o UniEventos já usa Firebase Auth (Aula 10), hospedar no Firebase Hosting mantém tudo no mesmo painel — vantagem organizacional, sem necessidade técnica adicional.

### 2.3 Alternativa: GitHub Pages

```bash
npm install -D gh-pages
```

```json
// package.json — trecho de "scripts"
{
  "scripts": {
    "deploy": "npm run build && gh-pages -d dist"
  }
}
```

Lembre de configurar `base: '/unieventos-web/'` no `vite.config.js` (Seção 1.3) antes de publicar, já que o GitHub Pages de repositório de projeto serve em um subcaminho. Depois:

```bash
npm run deploy
```

A URL pública fica em `https://<seu-usuario>.github.io/unieventos-web/`. Habilite em **Settings → Pages** do repositório, escolhendo a branch `gh-pages` (criada automaticamente pelo pacote `gh-pages`) como fonte.

## 3. Deploy do back-end

### 3.1 O essencial, independente do serviço escolhido

```js
// src/server.js — PORT precisa vir do ambiente, nunca fixo
import { app } from './app.js'
import { config } from './config/index.js'

// A maioria dos serviços de nuvem injeta a variável PORT automaticamente —
// escutar em uma porta fixa (3000) quebra o deploy nesses ambientes.
const servidor = app.listen(config.PORT, () => {
  console.log(`API rodando na porta ${config.PORT}`)
})
```

```json
// package.json — script "start" é o que o serviço de deploy roda em produção
{
  "scripts": {
    "start": "node src/server.js",
    "dev": "node --watch src/server.js"
  }
}
```

```js
// trecho de src/app.js — health check simples, usado pelo serviço de deploy
// para saber se o processo está de pé (e reiniciar automaticamente se não estiver)
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok', ambiente: config.NODE_ENV })
})
```

Checklist mínimo antes de publicar o back:

- [ ] `PORT` vem de `process.env.PORT` (via `config`, Aula 13), nunca hardcoded.
- [ ] Script `start` existe em `package.json` e sobe a API com `node` puro (sem `--watch`, que é só para desenvolvimento).
- [ ] `GET /health` responde `200` sem exigir autenticação nem banco de dados obrigatoriamente disponível.
- [ ] Banco de dados gerenciado (não `localhost`) — MySQL na nuvem (ex.: Railway, PlanetScale-compatível, ou o banco oferecido pelo próprio Render).
- [ ] Todas as variáveis de `.env` configuradas como *secrets* no painel do serviço, nunca commitadas no Git.

### 3.2 Opções gratuitas/baratas e o que considerar

| Serviço | Ponto forte | Atenção |
|---|---|---|
| Render | Free tier simples, banco MySQL/Postgres gerenciado disponível | Cold start no plano gratuito — primeira requisição após inatividade demora alguns segundos |
| Railway | Deploy rápido a partir do GitHub, bom suporte a MySQL | Free tier limitado por uso mensal, não por tempo |
| Fly.io | Roda containers Docker diretamente, bom controle de infraestrutura | Curva de aprendizado maior, exige `fly.toml` e CLI própria |

> **⚠️ Atenção — cold start**
> Planos gratuitos costumam "dormir" o processo após um período sem tráfego. A primeira requisição depois disso demora vários segundos (o serviço precisa religar o container). Isso é normal e esperado no plano gratuito — não é bug do seu código. Avise sobre isso na apresentação se seu projeto usar plano gratuito.

### 3.3 Deploy na Render (passo a passo)

1. Crie conta em [render.com](https://render.com) com login do GitHub.
2. **New → Web Service**, selecione o repositório `unieventos-api`.
3. Configure:
   - **Runtime:** Node
   - **Build Command:** `npm install`
   - **Start Command:** `npm start`
4. Na aba **Environment**, adicione todas as variáveis do seu `.env` (exceto as que só existem localmente).
5. Se precisar de MySQL gerenciado, crie um **New → MySQL** (ou Postgres, se preferir migrar) separado na Render e copie a string de conexão para as variáveis `DB_*` do Web Service.
6. Clique **Create Web Service**. A Render builda, sobe o processo, e devolve uma URL pública (`https://unieventos-api.onrender.com`).
7. Rode as migrations manualmente uma vez, via o **Shell** da Render (aba disponível no painel do serviço) ou como *Build Command* combinado: `npm install && npm run migrar`.

### 3.4 Dockerfile simples para a API

Mesmo usando um serviço que builda direto do GitHub, ter um `Dockerfile` documenta exatamente o ambiente de execução e permite rodar a API localmente de forma idêntica à produção.

```dockerfile
# Dockerfile
FROM node:22-alpine

WORKDIR /app

# Copiar só os arquivos de manifesto primeiro aproveita o cache de camadas do
# Docker: se package.json não mudou, o npm install não roda de novo no rebuild.
COPY package.json package-lock.json ./
RUN npm install --omit=dev

COPY src ./src
COPY migrations ./migrations
COPY scripts ./scripts

EXPOSE 3000

CMD ["npm", "start"]
```

```bash
# .dockerignore
node_modules
.env
.git
test
```

```bash
docker build -t unieventos-api .
docker run -p 3000:3000 --env-file .env unieventos-api
```

### 3.5 `docker-compose.yml` com API + MySQL

```yaml
# docker-compose.yml
services:
  api:
    build: .
    ports:
      - '3000:3000'
    environment:
      NODE_ENV: development
      PORT: 3000
      DB_HOST: mysql
      DB_PORT: 3306
      DB_USER: root
      DB_PASSWORD: senha_local
      DB_NAME: uni_eventos
      FIREBASE_PROJECT_ID: unieventos
      CORS_ORIGEM_PERMITIDA: http://localhost:5173
    depends_on:
      mysql:
        condition: service_healthy

  mysql:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: senha_local
      MYSQL_DATABASE: uni_eventos
    ports:
      - '3306:3306'
    volumes:
      - dados_mysql:/var/lib/mysql
    healthcheck:
      test: ['CMD', 'mysqladmin', 'ping', '-h', 'localhost']
      interval: 5s
      timeout: 5s
      retries: 10

volumes:
  dados_mysql:
```

```bash
docker compose up --build
# API e MySQL sobem juntos, na mesma rede virtual — a API conversa
# com o banco pelo nome do serviço ("mysql"), não por "localhost"
```

> **🔎 Por baixo do capô**
> Dentro da rede criada pelo `docker compose`, cada serviço enxerga os outros pelo **nome do serviço** no YAML (`mysql`), não por `localhost` — por isso `DB_HOST: mysql` e não `DB_HOST: localhost`. O valor de "isso funcionar de primeira" é enorme: qualquer pessoa que clonar o repositório sobe o ambiente completo (API + banco, com schema aplicável via `npm run migrar`) com um único comando, sem instalar MySQL na própria máquina.

## 4. CORS em produção e diagnóstico de erros pós-deploy

Em produção, restrinja CORS **apenas** ao domínio real do front publicado — nunca deixe `origin: '*'` ou o domínio de `localhost` esquecido em produção:

```bash
# .env de produção da API
CORS_ORIGEM_PERMITIDA=https://unieventos-web.vercel.app
```

### 4.1 Erros clássicos pós-deploy e como diagnosticar

| Sintoma | Causa provável | Como diagnosticar |
|---|---|---|
| Tela em branco após publicar, console mostra "Mixed Content" | Front em HTTPS chamando API em HTTP puro | Confira `VITE_API_URL` — precisa começar com `https://`, todo serviço de deploy moderno já expõe HTTPS por padrão |
| Requisições falham com erro de CORS no console | Domínio do front não está em `CORS_ORIGEM_PERMITIDA` da API, ou variável não foi atualizada em produção | Abra a aba Network do DevTools, confira o cabeçalho `Access-Control-Allow-Origin` na resposta; ajuste a variável de ambiente e reinicie o serviço |
| Tela em branco, sem erro óbvio | Uma `VITE_*` esquecida no painel de deploy — o build usa `undefined` silenciosamente | Confira todas as variáveis `VITE_*` no painel do serviço de hospedagem, comparando com o `.env.production` local |
| F5 numa rota interna (`/eventos/3`) dá 404 | Servidor não configurado para rewrite de SPA (Seção 1.4) | Adicione `vercel.json`/`_redirects`/`firebase.json` com o rewrite para `index.html` |
| API responde, mas toda rota de banco dá erro 500 | Banco inacessível: credenciais erradas, banco não migrado, ou IP não liberado no firewall do provedor | Acesse `/health` primeiro (não depende de banco); depois confira logs do serviço e rode `npm run migrar` no ambiente de produção |
| Login funciona local, falha em produção | Domínio de produção não foi adicionado à lista de domínios autorizados do Firebase Auth | No Console do Firebase, **Authentication → Settings → Authorized domains**, adicione o domínio publicado |

> **💡 Dica**
> Sempre teste `/health` primeiro depois de um deploy. Se ele responde `200`, o processo subiu — o problema está em uma camada específica (banco, CORS, variável de ambiente), não na infraestrutura toda.

## 5. CI/CD introdutório com GitHub Actions

CI (Integração Contínua) roda verificações automáticas a cada mudança no código — lint e testes, neste caso. CD (Entrega Contínua) automatiza a publicação quando essas verificações passam. Juntos, eliminam o "funciona na minha máquina" e o deploy manual esquecido.

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: ['**']
  pull_request:
    branches: [main]

jobs:
  lint-e-testes:
    runs-on: ubuntu-latest

    steps:
      - name: Baixar o código do repositório
        uses: actions/checkout@v4

      - name: Configurar Node.js 22
        uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'

      - name: Instalar dependências
        run: npm ci

      - name: Rodar lint
        run: npm run lint --if-present

      - name: Rodar testes
        run: npm test

  deploy:
    needs: lint-e-testes
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest

    steps:
      - name: Baixar o código do repositório
        uses: actions/checkout@v4

      - name: Disparar deploy na Render via deploy hook
        run: curl -X POST "${{ secrets.RENDER_DEPLOY_HOOK_URL }}"
```

Explicando as partes:

- `on.push.branches: ['**']` — roda lint/teste em **qualquer** push, em qualquer branch, dando feedback rápido antes mesmo de abrir Pull Request.
- `needs: lint-e-testes` — o job `deploy` só roda depois que `lint-e-testes` termina com sucesso; se um teste falhar, o deploy nunca acontece.
- `if: github.ref == 'refs/heads/main' && github.event_name == 'push'` — restringe o deploy a pushes diretos (ou merges) na branch `main`, nunca em branches de feature.
- `secrets.RENDER_DEPLOY_HOOK_URL` — configurado em **Settings → Secrets and variables → Actions** do repositório GitHub; nunca aparece em texto puro no workflow nem no log de execução.

> **⚠️ Atenção**
> `npm ci` (não `npm install`) dentro de workflows de CI: ele instala exatamente as versões travadas em `package-lock.json`, de forma determinística, e falha se o lockfile estiver dessincronizado do `package.json` — evita o "passou no CI, mas com uma versão diferente da que alguém tem local".

Para a Vercel (front-end), normalmente **não é preciso** workflow de deploy próprio — a integração da Vercel com o GitHub já dispara build e deploy automaticamente a cada push em `main`, de forma nativa, sem depender do GitHub Actions.

> **🔎 Por baixo do capô**
> O nome "CI/CD" às vezes confunde por juntar duas ideias distintas. **Integração Contínua** é sobre confiança: cada push prova, automaticamente, que o código continua íntegro (lint limpo, testes passando) antes de qualquer humano revisar. **Entrega/Implantação Contínua** é sobre velocidade: reduzir a distância entre "código pronto" e "código no ar" para minutos, não para um ritual manual de deploy que alguém precisa lembrar de fazer. O workflow desta seção faz as duas coisas: garante qualidade antes, entrega depois — e só entrega se a qualidade passou.

> **💡 Dica**
> Um erro comum de quem está aprendendo CI/CD é tratar o pipeline como "burocracia extra". Na prática, ele é o que permite a um time (ou a você sozinho, meses depois) fazer mudanças com confiança: se o CI ficou verde, você sabe que não quebrou nada que já estava coberto por teste — sem isso, cada mudança pequena vira um momento de ansiedade.

## 6. Retrospectiva da disciplina

### 6.1 Mapa mental textual do que foi construído

```text
UniEventos
│
├─ Front-end (unieventos-web)
│  ├─ Vue 3 (Composition API, <script setup>)          — Aulas 01–03
│  ├─ Vuetify 4 (UI, layout, formulários)               — Aulas 04–05
│  ├─ Vue Router 5 (SPA navegável, guards)              — Aulas 04, 10
│  ├─ Pinia 4 (estado global: usuário, eventos)          — Aula 06
│  ├─ Axios (consumo da API, interceptors)               — Aula 06
│  ├─ Firebase Auth (login, cadastro)                    — Aula 10
│  └─ Deploy (Vercel/Firebase Hosting/GitHub Pages)      — Aula 15
│
├─ Back-end (unieventos-api)
│  ├─ Node.js + Express 5 (rotas, middlewares)           — Aula 07–08
│  ├─ MySQL (mysql2/promise, pool, transações)           — Aula 09
│  ├─ Firebase Admin (verificação de token)               — Aula 10
│  ├─ CRUD completo (front + back integrados)             — Aula 11
│  ├─ Supabase (alternativa: RLS, Storage, Realtime)      — Aula 12
│  ├─ Arquitetura em camadas + testes + segurança         — Aula 13
│  ├─ Documentação OpenAPI/Swagger                        — Aula 14
│  └─ Deploy + CI/CD                                      — Aula 15
│
└─ Padrões de projeto (GoF) — ver tabela consolidada abaixo
```

### 🧩 Todos os padrões de projeto usados no semestre

A ementa exige explicitamente padrões **criacionais, estruturais e comportamentais**. Aqui está a lista completa, com onde cada um apareceu de verdade no UniEventos.

**Criacionais**

| Padrão | Onde apareceu | Aula |
|---|---|---|
| Singleton | Store Pinia como instância única do estado global; pool de conexões do MySQL (`obterPool()` em `db/pool.js`) | 06, 09, 13 |
| Factory | `createPool` do `mysql2`; funções `criarServicoDeEventos`/`criarRepositorioDeEventosMySQL` que fabricam objetos configurados | 09, 13 |
| Builder | `QueryBuilderDeListagem`, que monta a query SQL de listagem incrementando condições opcionais (`.comCategoria().comBuscaDeTexto().construir()`) | 13 |
| Object Pool | O próprio pool de conexões do `mysql2` reutiliza um conjunto fixo de conexões abertas em vez de abrir/fechar uma a cada requisição | 09 |

**Estruturais**

| Padrão | Onde apareceu | Aula |
|---|---|---|
| Composite | Árvore de componentes Vue (componentes dentro de componentes); rotas aninhadas do Vue Router | 04, 05 |
| Facade | Camada `services/` no front (Aula 11) e no back (Aula 13) escondendo a complexidade de várias chamadas atrás de uma interface simples | 11, 13 |
| Adapter | Troca de MySQL por Supabase sem alterar o front — a interface do repositório permanece igual, a implementação muda por baixo | 12 |
| Proxy | `reactive()`/`ref()` do Vue usando `Proxy` do ES6 por baixo dos panos; middleware de autenticação como "proxy de proteção" antes da rota real | 03, 10 |
| Decorator | Interceptors do Axios "decorando" toda requisição (token, log) sem alterar o código de quem chama; anotações `@openapi` decorando rotas com metadados sem mudar o comportamento | 06, 14 |

**Comportamentais**

| Padrão | Onde apareceu | Aula |
|---|---|---|
| Observer | Sistema de reatividade do Vue — um `ref`/`reactive` muda, tudo que depende dele é notificado e re-renderiza automaticamente | 02 |
| Chain of Responsibility | Pipeline de middlewares do Express — cada `app.use` decide processar e passar adiante (`next()`) ou interromper a cadeia | 07, 08 |
| Strategy | Middlewares/validadores intercambiáveis; escolha de qual repositório usar por ambiente (`obterRepositorioDeEventos`, MySQL vs. memória) | 08, 13 |
| Template Method | Componentes de layout com slots definindo um "esqueleto" fixo e pontos variáveis preenchidos por quem usa o componente | 05 |

> **📌 Na prova**
> O exame final cobra a definição de cada padrão **e** um exemplo concreto de onde ele apareceu no semestre — não basta decorar o nome, é preciso saber reconhecer o padrão dentro de um trecho de código real.

## 7. Guia de estudo para o exame final

O exame final é **teórico, presencial e individual**, cobrindo as três unidades da disciplina. Ele avalia conceitos, não "rodar código" — estude o porquê de cada decisão técnica, não só a sintaxe.

### 7.1 Lista de 25 a 30 questões de estudo

**Unidade 1 — Fundamentos de Vue.js**

1. O que é programação declarativa e como ela difere de manipulação manual do DOM? (Aula 01)
2. O que é reatividade no Vue e qual padrão de projeto (GoF) explica seu funcionamento? (Aula 02)
3. Qual a diferença entre Options API e Composition API? Quando usar `<script setup>`? (Aula 02)
4. Como `reactive()` e `ref()` diferem na forma como armazenam e expõem o valor? (Aula 03)
5. Por que `v-for` sempre precisa de `:key`, e o que acontece se ela faltar? (Aula 02–03)
6. O que é uma `computed` e por que ela é preferível a um método equivalente, em termos de performance? (Aula 03)
7. Qual é a diferença entre `onMounted` e o restante do ciclo de vida de um componente? (Aula 03)

**Unidade 2 — Vue avançado (Vuetify, Vue Router, Axios, Pinia)**

8. Como o Vue Router resolve navegação sem recarregar a página inteira (SPA)? (Aula 04)
9. O que é um *navigation guard* e para que serve `beforeEach`? (Aula 10)
10. Por que instanciar `axios.create({ baseURL })` com interceptors é melhor do que usar `axios` global? (Aula 06)
11. Que padrão de projeto os interceptors do Axios exemplificam? (Aula 06)
12. Qual é o papel do Pinia como *single source of truth* do estado da aplicação? (Aula 06)
13. Por que a store Pinia é um exemplo de Singleton? (Aula 06)
14. Como slots permitem que um componente de layout seja reutilizável em vários contextos? (Aula 05)
15. O que muda estruturalmente do Vuetify 3 para o Vuetify 4 (tema padrão, tipografia, breakpoints)? (Aula 04–05)

**Unidade 3 — Back-end, autenticação, banco de dados, deploy**

16. Qual a diferença entre autenticação e autorização, e onde cada uma aparece no UniEventos? (Aula 10)
17. Como o Express 5 muda o tratamento de erros assíncronos em relação ao Express 4? (Aula 07–08, 13)
18. O que é *middleware* no Express e que padrão de projeto (GoF) o pipeline de middlewares representa? (Aula 07–08)
19. Por que usar `mysql2/promise` com queries parametrizadas (`?`) em vez de concatenar strings? (Aula 09)
20. O que é uma transação de banco de dados e quando ela é necessária? (Aula 09)
21. Como o back-end verifica um token do Firebase, e por que essa verificação precisa acontecer no servidor (nunca só no front)? (Aula 10)
22. O que é RLS (Row Level Security) no Supabase, e por que uma tabela com RLS habilitado e sem policies retorna lista vazia sem erro? (Aula 12)
23. Que padrão de projeto permite trocar MySQL por Supabase sem alterar o front-end? (Aula 12)
24. O que é injeção de dependência, e por que um service que recebe o repositório por parâmetro é mais testável? (Aula 13)
25. Qual a diferença entre um erro operacional (esperado) e um erro inesperado, e por que essa diferença importa no log? (Aula 13)
26. Por que nunca se deve vazar stack trace em uma resposta de erro em produção? (Aula 13)
27. Qual a diferença entre OpenAPI e Swagger? (Aula 14)
28. Por que a chave correta no `swagger-jsdoc` 6.x é `definition`, e o que acontece se usar `swaggerDefinition`? (Aula 14)
29. O que é uma migration de banco de dados e por que ela substitui um `schema.sql` aplicado manualmente? (Aula 13)
30. Por que uma SPA precisa de configuração de *rewrite* no servidor de hospedagem para funcionar corretamente com F5 em rotas internas? (Aula 15)

### 7.2 Questões objetivas de exemplo, com gabarito comentado

**1.** No Vue 3, o sistema de reatividade (`reactive`, `ref`) é implementado, por baixo dos panos, principalmente com:

(A) `Object.defineProperty` apenas
(B) `Proxy` do ES6
(C) `WeakMap` apenas
(D) Getters e setters manuais escritos pelo desenvolvedor

<details markdown="1">
<summary>Gabarito comentado</summary>

**Resposta: B.** O Vue 3 usa `Proxy` do ES6 para interceptar leitura e escrita de propriedades e disparar a reatividade — diferente do Vue 2, que usava `Object.defineProperty` (com limitações conhecidas, como não detectar adição de novas propriedades). Ver Aula 03.
</details>

**2.** Em Express 5, qual das alternativas abaixo é a forma correta de responder com status `201` e um corpo JSON?

(A) `res.json(objeto, 201)`
(B) `res.status(201).json(objeto)`
(C) `res.send(201, objeto)`
(D) `res.json(201, objeto)`

<details markdown="1">
<summary>Gabarito comentado</summary>

**Resposta: B.** `res.json(obj, status)` é sintaxe do Express 4, removida no Express 5. A forma correta e atual é encadear `res.status(201).json(objeto)`. Ver Aula 07/13.
</details>

**3.** Uma tabela no Supabase tem RLS (Row Level Security) habilitado, mas nenhuma policy foi criada. Uma consulta `SELECT` feita por um cliente autenticado retorna:

(A) Um erro `403 Forbidden`
(B) Todos os registros da tabela, normalmente
(C) `data: []`, sem nenhum erro
(D) Um erro `500 Internal Server Error`

<details markdown="1">
<summary>Gabarito comentado</summary>

**Resposta: C.** É a "causa nº1 de meu código não funciona" no Supabase (Aula 12): RLS sem policy não gera erro, apenas nega acesso silenciosamente, retornando lista vazia. É essencial sempre criar a policy correspondente à operação (SELECT, INSERT etc.).
</details>

**4.** Qual padrão de projeto GoF melhor descreve o pipeline de `middlewares` do Express, em que cada função decide processar a requisição e passá-la adiante com `next()`, ou interrompê-la?

(A) Observer
(B) Chain of Responsibility
(C) Singleton
(D) Facade

<details markdown="1">
<summary>Gabarito comentado</summary>

**Resposta: B.** Chain of Responsibility: uma cadeia de handlers, cada um com a chance de tratar a requisição ou repassá-la ao próximo. É exatamente o comportamento de `app.use(middleware1, middleware2, ...)`. Ver Aula 07–08.
</details>

**5.** Sobre `swagger-jsdoc` na versão 6.x usada nesta disciplina, a chave correta dentro das opções para declarar `openapi`, `info` e `components` é:

(A) `swaggerDefinition`
(B) `spec`
(C) `definition`
(D) `openApiDefinition`

<details markdown="1">
<summary>Gabarito comentado</summary>

**Resposta: C.** `swaggerDefinition` era usado em versões antigas (2.x/3.x). A versão 6.x exige `definition`. Usar a chave errada não gera erro — só produz uma spec com `paths` vazio. Ver Aula 14.
</details>

**6.** Por que uma SPA hospedada em produção pode retornar `404` ao usuário apertar F5 em uma rota interna como `/eventos/3`?

(A) Porque o Vue Router não suporta navegação direta por URL
(B) Porque o servidor de hospedagem, sem configuração de rewrite, procura um arquivo físico `eventos/3` que não existe
(C) Porque o Vite não gera `index.html` no build de produção
(D) Porque `import.meta.env` não funciona em produção

<details markdown="1">
<summary>Gabarito comentado</summary>

**Resposta: B.** O F5 dispara uma requisição HTTP real ao servidor para aquele caminho. Sem rewrite configurado, o servidor de arquivos estáticos não encontra um arquivo físico correspondente e responde `404`. A solução é configurar o rewrite para `index.html` em qualquer caminho desconhecido. Ver Aula 15, Seção 1.4.
</details>

**7.** No padrão de injeção de dependência aplicado na Aula 13, qual é a principal vantagem de um `service` receber o `repository` como parâmetro em vez de importá-lo diretamente?

(A) O código fica mais curto
(B) É possível testar o service com um repositório falso, sem depender de um banco de dados real
(C) É a única forma de usar `async/await` no Node.js
(D) Reduz o número de arquivos do projeto

<details markdown="1">
<summary>Gabarito comentado</summary>

**Resposta: B.** A motivação central de DI aqui é testabilidade: o service passa a depender apenas da interface do repositório, não da implementação concreta — em teste, injeta-se uma implementação em memória; em produção, a implementação real. Ver Aula 13, Seção 3.
</details>

**8.** No Vuetify 4, o comportamento padrão da propriedade `theme.defaultTheme`, se não for explicitamente definida, é:

(A) `'light'`, igual ao Vuetify 3
(B) `'dark'`
(C) `'system'` — segue a preferência do sistema operacional do usuário
(D) Não existe tema padrão; é obrigatório declarar

<details markdown="1">
<summary>Gabarito comentado</summary>

**Resposta: C.** No Vuetify 4 o padrão mudou de `'light'` (v3) para `'system'`. Por isso a disciplina sempre declara explicitamente `defaultTheme: 'light'` na criação da instância, para manter consistência visual em sala. Ver especificação da Aula 04/05.
</details>

## 8. Apresentação dos resultados

### 8.1 Formato do seminário final

Cada estudante apresenta seu projeto autoral individualmente, em **8 minutos**, cobrindo obrigatoriamente:

1. **O problema** (1 min) — que problema real o projeto resolve, para quem.
2. **Demonstração ao vivo** (3 min) — navegar pela aplicação publicada (URL real, não localhost): listagem com filtro, detalhe, fluxo autenticado, CRUD funcionando.
3. **Arquitetura** (2 min) — diagrama rápido das camadas (front → API → banco), tecnologias escolhidas, e onde a documentação Swagger vive.
4. **Decisão técnica mais difícil** (1 min) — um problema real enfrentado e como foi resolvido (ex.: "por que troquei X por Y", "como resolvi o CORS em produção").
5. **O que faria diferente** (1 min) — autoavaliação honesta: o que ficaria melhor com mais tempo ou outra escolha técnica.

### 8.2 Critérios de avaliação da apresentação

| Critério | O que é observado |
|---|---|
| Clareza da comunicação | Explica o projeto para alguém que nunca viu, sem depender de jargão não explicado |
| Demonstração funcional | A aplicação publicada realmente funciona ao vivo, sem "deixa eu tentar de novo" |
| Profundidade técnica | Consegue justificar decisões (por que essa arquitetura, por que esse banco) |
| Gestão do tempo | Respeita os 8 minutos, sem cortar abruptamente nem sobrar tempo vazio |

> **⚠️ Atenção**
> A apresentação é sobre o **projeto autoral publicado**, com URL pública real — não é permitido apresentar rodando em `localhost`. Se o deploy falhar no dia, tenha um vídeo curto de backup gravado com antecedência mostrando o fluxo funcionando.

### 8.3 Ordem e cronograma

A ordem de apresentação é definida por sorteio, feito em sala na aula anterior (Aula 14) ou no início desta aula, conforme a quantidade de estudantes matriculados. Com 3 blocos de 50 minutos e 8 minutos por estudante, o tempo permite aproximadamente 15 a 16 apresentações — se a turma for maior, o professor comunica com antecedência um ajuste (ex.: reduzir para 6 minutos ou dividir em dois dias, dentro do que o calendário acadêmico permitir).

## 💻 Mão na massa — publicando o UniEventos

**Passo 1 — configure as variáveis de ambiente de produção do front:**

```bash
# no repositório unieventos-web
touch .env.production
# preencha VITE_API_URL com a URL da API já publicada (Passo 4 abaixo)
```

**Passo 2 — confirme que o build local funciona:**

```bash
npm run build
npm run preview
# abra http://localhost:4173 e navegue pelas rotas internas — confirme que
# recarregar a página (F5) numa rota interna NÃO quebra localmente
# (o "vite preview" já simula o comportamento de servidor de produção)
```

**Passo 3 — publique o front na Vercel** seguindo o passo a passo da Seção 2.1.

**Passo 4 — publique o back na Render** seguindo o passo a passo da Seção 3.3. Anote a URL pública gerada.

**Passo 5 — volte ao front e atualize `VITE_API_URL`** com a URL real da API publicada, faça commit e push — a Vercel refaz o build automaticamente.

**Passo 6 — atualize `CORS_ORIGEM_PERMITIDA`** na API publicada com a URL real do front publicado (Seção 4), reinicie o serviço.

**Passo 7 — teste o fluxo completo em produção:** abra a URL do front publicado, faça login, liste eventos, crie uma inscrição, atualize a página em uma rota interna (F5) e confirme que não dá 404.

**Passo 8 — crie o workflow de CI:**

```bash
mkdir -p .github/workflows
# cole o conteúdo de .github/workflows/ci.yml da Seção 5
git add .github/workflows/ci.yml
git commit -m "adiciona pipeline de CI com lint e testes"
git push
```

Confira na aba **Actions** do GitHub que o workflow rodou e passou.

## 🧪 Laboratório

**1. Gere o build de produção do seu projeto autoral e rode `npm run preview`** — confirme que todas as rotas funcionam, incluindo F5 em rota interna.

Resultado esperado: nenhum erro no console, navegação idêntica ao ambiente de desenvolvimento.

<details markdown="1">
<summary>Dica</summary>

Se uma rota der 404 até no `preview` local, o problema é de configuração de rota no Vue Router, não de hospedagem — resolva isso antes de publicar.
</details>

**2. Publique o front-end** em um dos serviços da Seção 2, com as variáveis `VITE_*` corretas.

Resultado esperado: URL pública funcionando, aplicação carrega sem tela em branco.

<details markdown="1">
<summary>Dica</summary>

Se a tela ficar em branco sem erro óbvio, abra o Console do DevTools primeiro — normalmente aponta uma variável de ambiente `undefined`.
</details>

**3. Publique o back-end** em um dos serviços da Seção 3, com `/health` respondendo publicamente.

Resultado esperado: `curl https://sua-api.onrender.com/health` retorna `{"status":"ok",...}`.

<details markdown="1">
<summary>Dica</summary>

Rode as migrations manualmente pelo shell do serviço antes de testar qualquer rota que dependa de tabela do banco.
</details>

**4. Configure CORS restritivo em produção**, apontando exatamente para a URL do front publicado.

Resultado esperado: requisições do front publicado funcionam; uma requisição feita a partir de uma origem diferente é bloqueada.

<details markdown="1">
<summary>Dica</summary>

Teste abrindo o Console do navegador em uma aba com origem diferente (ex.: `http://localhost:5500`) e tentando um `fetch` contra sua API publicada — deve falhar por CORS.
</details>

**5. Crie o workflow de CI** no seu repositório de back-end, rodando lint e testes a cada push.

Resultado esperado: aba Actions do GitHub mostra o workflow executando e passando em verde.

<details markdown="1">
<summary>Dica</summary>

Se você não tiver `npm run lint` configurado, o `--if-present` do comando na Seção 5 evita que o workflow falhe por esse motivo — mas vale configurar ESLint se ainda não tiver.
</details>

## 🐛 Erros comuns e como resolver

| Sintoma | Causa | Solução |
|---|---|---|
| Build local funciona, produção mostra tela em branco | Variável `VITE_*` não configurada no painel do serviço de hospedagem | Confira todas as `VITE_*` no painel, compare com `.env.production` local, force um novo build |
| `Mixed Content` no console em produção | API ainda respondendo em `http://` enquanto o front está em `https://` | Troque `VITE_API_URL` para `https://`; a maioria dos serviços de deploy de back já expõe HTTPS por padrão |
| CI falha em "npm ci" com erro de lockfile | `package-lock.json` desatualizado em relação ao `package.json` | Rode `npm install` localmente, comite o `package-lock.json` atualizado |
| Deploy da API funciona, mas toda rota autenticada falha | Domínio de produção do front não está na lista de domínios autorizados do Firebase Auth | Adicione o domínio em Firebase Console → Authentication → Settings → Authorized domains |
| `docker compose up` falha ao conectar no banco | API tentando conectar em `localhost` em vez do nome do serviço `mysql` | Ajuste `DB_HOST` para `mysql` (o nome do serviço no `docker-compose.yml`), não `localhost` |
| Workflow de CI nunca dispara o job de deploy | Condição `if` do job `deploy` não bateu (branch errada ou evento errado) | Confira se o push foi feito diretamente em `main` ou via merge de PR para `main` |

## 🏠 Atividade assíncrona (1 h)

1. Finalize o deploy completo (front + back) do projeto autoral, se ainda não tiver feito no laboratório.
2. Grave um vídeo curto (3 a 5 minutos, pode ser não listado no YouTube ou enviado por link de drive) demonstrando o fluxo publicado, como backup para a apresentação.
3. Prepare os slides ou roteiro da apresentação de 8 minutos, seguindo a estrutura da Seção 8.1.
4. Revise, uma última vez, o README, garantindo que o link da aplicação publicada e do `/api-docs` estejam visíveis.

**Critério de pronto:** aplicação publicada e acessível publicamente; vídeo de backup gravado; roteiro da apresentação pronto.

## ✅ Checkpoint do projeto autoral

Ao final desta aula, seu projeto deve ter:

- [ ] Front-end publicado com URL pública, variáveis `VITE_*` corretas, rewrite de SPA configurado.
- [ ] Back-end publicado com URL pública, `/health` respondendo, banco gerenciado acessível, migrations aplicadas.
- [ ] CORS restrito ao domínio real do front publicado.
- [ ] Workflow de CI (`.github/workflows/ci.yml`) rodando lint e testes a cada push.
- [ ] README com links da aplicação publicada, da API publicada e de `/api-docs`.
- [ ] Roteiro de apresentação pronto, dentro de 8 minutos.

## 📝 Avaliação 3 — instruções de entrega

**Escopo:** aplicação full stack completa, construída sobre o projeto autoral definido na Aula 01 e evoluído ao longo de todo o semestre.

**Requisitos obrigatórios:**

1. Back-end próprio, em **Express** ou usando **Supabase** como back-end gerenciado (ou uma combinação dos dois, desde que a arquitetura em camadas da Aula 13 esteja presente onde houver código Express).
2. Banco de dados persistente (MySQL ou Supabase/Postgres), com **schema versionado** (migrations ou scripts SQL organizados).
3. Autenticação funcional (Firebase Auth ou autenticação nativa do Supabase), protegendo pelo menos as rotas de escrita (criação/edição/remoção).
4. **CRUD completo de pelo menos 2 entidades relacionadas** (ex.: "Evento" e "Inscrição"), com relacionamento real no banco (chave estrangeira ou equivalente).
5. Documentação **Swagger** (OpenAPI 3) cobrindo todos os endpoints, ou documentação equivalente de todas as políticas/endpoints se o back for majoritariamente Supabase.
6. **Deploy funcionando com URL pública** — tanto do front quanto do back (ou só do front, se usando Supabase como back completo).
7. **README completo**, seguindo a estrutura da Aula 14 (badges, requisitos, instalação, variáveis de ambiente, scripts, endpoints, licença), com os links de aplicação publicada e repositório.

**Rubrica (pesos somam 10 pontos):**

| Critério | Peso | O que precisa estar funcionando |
|---|---|---|
| CRUD completo de 2+ entidades relacionadas | 2,5 | Criar, listar, editar e remover funcionando de ponta a ponta, com relacionamento real entre as entidades |
| Banco de dados persistente e corretamente modelado | 1,5 | Schema versionado (migrations/scripts), queries corretas, sem duplicação nem inconsistência de dados |
| Autenticação protegendo rotas sensíveis | 1,5 | Rotas de escrita exigem usuário autenticado; identidade do usuário usada corretamente (ex.: só o dono edita/remove seu próprio recurso) |
| Documentação Swagger/OpenAPI completa | 1,5 | Todos os endpoints documentados, schemas reutilizáveis, segurança declarada, `/api-docs` acessível |
| Deploy funcionando com URL pública | 2,0 | Front e back publicados, acessíveis externamente, sem depender de `localhost` |
| README e qualidade geral do código | 1,0 | README completo conforme estrutura da Aula 14; arquitetura em camadas aplicada; ao menos alguns testes automatizados presentes |

**Formato de entrega:** via **SIGAA**, até **16/12/2026, 23h59**, contendo:

- Link do repositório do front-end.
- Link do repositório do back-end (ou anotação de que o back é 100% Supabase, com link do projeto Supabase se aplicável).
- Link da aplicação publicada (URL pública funcionando).
- Link de `/api-docs` (se aplicável) ou da documentação equivalente.

> **⚠️ Atenção**
> A entrega é considerada incompleta se qualquer um dos quatro links acima estiver ausente ou não funcionar no momento da correção. Teste os links em uma aba anônima do navegador antes de enviar, simulando o que o avaliador vai ver.

**Política de atraso:** entregas após 16/12/2026, 23h59 têm desconto de 1,0 ponto (sobre a nota final da Avaliação 3) por dia corrido de atraso, até o limite de 3 dias — após esse prazo, a avaliação recebe nota zero, exceto em casos de justificativa formal e documentada junto à coordenação do curso, conforme o regimento da UNEMAT.

**Política de plágio e uso de IA:** é permitido e esperado o uso de ferramentas de IA (como assistentes de código) como apoio ao desenvolvimento — é exatamente essa prática que a indústria de software usa hoje. O que não é aceito: (1) entregar código que você não é capaz de explicar linha a linha na apresentação; (2) copiar o projeto de outro colega, com ou sem alterações cosméticas; (3) apresentar como próprio um projeto gerado quase integralmente por IA sem compreensão do que foi produzido. A apresentação de 8 minutos (Seção 8) é, entre outras coisas, o mecanismo de verificação de autoria: perguntas técnicas sobre decisões do próprio código fazem parte da avaliação.

## 9. Encerramento: caminhos depois da disciplina

O que foi construído neste semestre é uma base real de desenvolvimento full stack moderno — mas é só o começo. Caminhos naturais de continuidade:

- **Nuxt** — framework full stack sobre o Vue, com SSR (Server-Side Rendering) e SSG (Static Site Generation) nativos, útil quando SEO ou performance de primeira carga importam mais do que em uma SPA pura.
- **TypeScript** — adicionar tipagem estática ao que hoje é JavaScript puro; o Vue 3 e o Vuetify 4 têm suporte de primeira classe a TS, e o ganho em projetos maiores (detecção de erro em tempo de escrita, autocomplete mais forte) é significativo.
- **Testes E2E** — Cypress ou Playwright, testando a aplicação inteira pela interface, como um usuário real faria — o topo da pirâmide de testes que só citamos na Aula 13.
- **Vue 3.6** — acompanhar o roadmap oficial do Vue (Vapor Mode e otimizações de compilador são a fronteira de pesquisa ativa do framework no momento).
- **Mobile com Capacitor/Ionic** — reaproveitar o conhecimento de Vue para publicar o mesmo código (ou uma variação) como app nativo Android/iOS.
- **Back-end com NestJS** — um framework Node.js opinativo, construído sobre Express (ou Fastify), que formaliza com decorators e módulos exatamente a arquitetura em camadas que construímos manualmente na Aula 13.

### 9.1 Como montar um portfólio a partir deste semestre

- Deixe o projeto autoral **publicado e funcionando** — um link ao vivo vale mais, para quem recruta, do que um repositório que só roda localmente.
- Escreva um README que conte a história do projeto: problema, decisões técnicas, dificuldades reais (os ADRs da Aula 14 são ótimo material bruto para isso).
- Grave um vídeo curto de demonstração e fixe no topo do repositório (ou no README, como GIF).
- Continue commitando — um projeto "morto" no GitHub (sem commit há meses) comunica menos do que um projeto pequeno e ativo.

### 9.2 Convite para iniciação científica e extensão

Muitos dos temas tocados de leve neste semestre — arquitetura de software, segurança de aplicações web, engenharia de dados, IA aplicada a desenvolvimento — são linhas de pesquisa ativas na FACET. Se algum tópico desta disciplina despertou curiosidade além do prazo de uma avaliação, procure o professor para conversar sobre projetos de iniciação científica ou extensão relacionados — é o próximo passo natural para quem quer ir além do conteúdo obrigatório da ementa.

## 📚 Para aprofundar

- [Documentação oficial da Vercel](https://vercel.com/docs)
- [Documentação oficial do Firebase Hosting](https://firebase.google.com/docs/hosting)
- [GitHub Pages — documentação oficial](https://docs.github.com/pages)
- [Documentação oficial da Render](https://render.com/docs)
- [Docker — documentação oficial](https://docs.docker.com)
- [GitHub Actions — documentação oficial](https://docs.github.com/actions)
- [Vite — variáveis de ambiente e modos](https://vite.dev/guide/env-and-mode)
- [Vue Router — histórico HTML5 e configuração de servidor](https://router.vuejs.org/guide/essentials/history-mode.html)
- [Nuxt — site oficial](https://nuxt.com)
- [NestJS — site oficial](https://nestjs.com)

---

**Fim do semestre.** Obrigado pelo empenho nas 15 aulas — do primeiro `console.log` da Aula 01 até uma aplicação full stack publicada, com autenticação, banco de dados e documentação. O exame final cobre teoria das três unidades; revise o guia de estudo da Seção 7 com antecedência, não na véspera. Bom exame, e bom portfólio.
