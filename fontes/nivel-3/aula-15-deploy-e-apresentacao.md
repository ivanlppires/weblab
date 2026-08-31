# Aula 15 — Deploy, apresentação e finalização

> **Nível 3 — Frameworks Modernos** · Unidade 3: Integração front-end/back-end
> WebLab · UNEMAT — Campus Sinop
> **Tempo estimado:** 3 blocos de 50 min + 1 h de prática

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Gerar o build de produção de uma aplicação Vue com Vite e explicar o que existe dentro de `dist/`.
- Publicar o front-end em um serviço de hospedagem estática (Vercel, Firebase Hosting ou GitHub Pages), configurando variáveis de ambiente e rewrite de SPA.
- Publicar o back-end Express em um serviço de nuvem, com `PORT` dinâmico, health check e variáveis de ambiente seguras.
- Escrever um `Dockerfile` simples para a API e um `docker-compose.yml` com API + MySQL.
- Diagnosticar e corrigir os erros mais comuns pós-deploy (CORS, mixed content, 404 em rota interna, banco inacessível).
- Configurar um pipeline básico de CI/CD no GitHub Actions que roda lint e testes a cada push.
- Relacionar cada padrão de projeto estudado no semestre ao trecho de código onde ele apareceu no UniEventos.
- Apresentar o projeto autoral em formato de seminário técnico, dentro de um tempo definido, explicando as próprias decisões técnicas.
- Alcançar o Marco 3 do projeto autoral, conferindo cada requisito da unidade de ponta a ponta.

## 📋 Pré-requisitos desta aula

Na Aula 14 documentamos a API inteira com OpenAPI e Swagger UI — qualquer pessoa consegue entender e testar o UniEventos sem ler uma linha de código. Falta uma última etapa: tirar o projeto do `localhost` e colocá-lo no ar, com URL pública, para qualquer pessoa acessar. Hoje fechamos esse ciclo — e fechamos o semestre.

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
| 2 | 50 min | CI/CD com GitHub Actions, retrospectiva de padrões de projeto, teste seu domínio dos padrões |
| 3 | 50 min | Marco 3 do projeto, formato da apresentação final, encerramento da trilha |

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

> **🔬 Investigue**
> Abra a aba Network do DevTools em qualquer site grande que você usa no dia a dia (não precisa ser o UniEventos) e clique num arquivo `.js` ou `.css` com um hash estranho no nome. Olhe o cabeçalho de resposta `Cache-Control` — em serviços bem configurados, ele costuma trazer algo como `max-age=31536000, immutable` (um ano). Agora clique no documento principal da página (o HTML) e compare: o `Cache-Control` dele é bem mais curto, ou `no-cache`. Por que faz sentido cachear "para sempre" um arquivo, mas nunca o HTML que aponta para ele?

`dist/` é **tudo** que o servidor de hospedagem precisa: arquivos estáticos, sem Node.js rodando por trás. É por isso que hospedar um front-end Vue construído é barato (ou gratuito) — não é um processo de servidor, é só arquivos.

### 1.2 Variáveis de ambiente do Vite

O Vite só expõe ao código do navegador variáveis de ambiente prefixadas com `VITE_` — qualquer outra fica de fora do bundle final, por segurança (evita vazar segredos de build no JavaScript público).

```bash
# .env.production — lido automaticamente quando NODE_ENV=production (no build)
VITE_API_URL=https://unieventos-api.onrender.com/api
VITE_FIREBASE_API_KEY=AIzaSy...
VITE_FIREBASE_AUTH_DOMAIN=unieventos.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=unieventos
```

```bash
# .env.development — lido em npm run dev
VITE_API_URL=http://localhost:3000/api
VITE_FIREBASE_API_KEY=AIzaSy...
VITE_FIREBASE_AUTH_DOMAIN=unieventos.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=unieventos
```

```js
// src/services/http.js — o cliente da Aula 06, agora lendo a variável de ambiente
import axios from 'axios'

const http = axios.create({
  baseURL: import.meta.env.VITE_API_URL, // troca sozinho entre dev e produção
})

export default http
```

> **⚠️ Atenção**
> `VITE_API_URL` inclui o sufixo `/api` — é o prefixo em que a `unieventos-api` monta suas rotas desde a Aula 07. Os services chamam `http.get('/eventos')`, e a URL final vira `.../api/eventos`. Esquecer o `/api` aqui é o erro pós-deploy mais comum: tudo compila, tudo publica, e toda requisição volta `404` porque foi para `.../eventos`.

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

> **📌 Vale gravar**
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
> A Vercel também cria um **preview deploy** automático para cada Pull Request, com URL própria — ótimo para revisar uma feature antes de mesclar em `main`, mas não obrigatório nesta trilha.

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

> **🧠 Você sabia?**
> Contêineres não são uma invenção da Docker. As primitivas do kernel Linux que tornam a isolação possível — `cgroups` (limitar quanto de CPU e memória um processo pode usar) e `namespaces` (isolar o que um processo enxerga do sistema) — existem desde 2007/2008, quase seis anos antes do lançamento da Docker em 2013. O que a Docker inventou não foi a isolação em si: foi a experiência — empacotar essas primitivas complexas atrás de um `Dockerfile` legível e de dois comandos (`docker build`, `docker run`) que qualquer pessoa consegue usar sem entender kernel Linux por dentro.

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
      DB_NAME: unieventos
      FIREBASE_PROJECT_ID: unieventos
      CORS_ORIGEM_PERMITIDA: http://localhost:5173
    depends_on:
      mysql:
        condition: service_healthy

  mysql:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: senha_local
      MYSQL_DATABASE: unieventos
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

## 6. Retrospectiva da trilha

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

### 🧩 Todos os padrões de projeto usados nesta trilha

Esta trilha cobre explicitamente padrões **criacionais, estruturais e comportamentais**. Aqui está a lista completa, com onde cada um apareceu de verdade no UniEventos.

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

> **📌 Vale gravar**
> Dominar de verdade os padrões de projeto desta trilha exige duas coisas: saber a definição de cada padrão **e** conseguir apontar um exemplo concreto de onde ele apareceu — não basta decorar o nome, é preciso reconhecer o padrão dentro de um trecho de código real.

## 7. Teste seu domínio: padrões de projeto e arquitetura de toda a trilha

Esta seção é uma autoavaliação, cobrindo as três unidades desta trilha. O objetivo não é "rodar código" — é entender o porquê de cada decisão técnica, não só a sintaxe. Use as perguntas para descobrir sozinho o que você já domina e o que vale revisar antes de fechar o projeto (ou de explicar seu código na apresentação).

### 7.1 Lista de 25 a 30 perguntas para se testar

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

**5.** Sobre `swagger-jsdoc` na versão 6.x usada nesta trilha, a chave correta dentro das opções para declarar `openapi`, `info` e `components` é:

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

**Resposta: B.** A motivação central de DI aqui é testabilidade: o service passa a depender apenas da interface do repositório, não da implementação concreta — em teste, injeta-se uma implementação em memória; em produção, a implementação real. Ver Aula 13, Seção 2.
</details>

**8.** No Vuetify 4, o comportamento padrão da propriedade `theme.defaultTheme`, se não for explicitamente definida, é:

(A) `'light'`, igual ao Vuetify 3
(B) `'dark'`
(C) `'system'` — segue a preferência do sistema operacional do usuário
(D) Não existe tema padrão; é obrigatório declarar

<details markdown="1">
<summary>Gabarito comentado</summary>

**Resposta: C.** No Vuetify 4 o padrão mudou de `'light'` (v3) para `'system'`. Por isso este material sempre declara explicitamente `defaultTheme: 'light'` na criação da instância, para manter a interface consistente com as capturas de tela e exemplos do material. Ver especificação da Aula 04/05.
</details>

## 8. Apresentação dos resultados

### 8.1 Estrutura da apresentação final

Apresente seu projeto autoral individualmente, em **8 minutos**, cobrindo estes pontos:

1. **O problema** (1 min) — que problema real o projeto resolve, para quem.
2. **Demonstração ao vivo** (3 min) — navegar pela aplicação publicada (URL real, não localhost): listagem com filtro, detalhe, fluxo autenticado, CRUD funcionando.
3. **Arquitetura** (2 min) — diagrama rápido das camadas (front → API → banco), tecnologias escolhidas, e onde a documentação Swagger vive.
4. **Decisão técnica mais difícil** (1 min) — um problema real enfrentado e como foi resolvido (ex.: "por que troquei X por Y", "como resolvi o CORS em produção").
5. **O que faria diferente** (1 min) — autoavaliação honesta: o que ficaria melhor com mais tempo ou outra escolha técnica.

### 8.2 O que uma boa apresentação tem

Use esta tabela para se autoavaliar — ou peça a um colega que assista e aponte o que falta:

| Critério | O que observar |
|---|---|
| Clareza da comunicação | Explica o projeto para alguém que nunca viu, sem depender de jargão não explicado |
| Demonstração funcional | A aplicação publicada realmente funciona ao vivo, sem "deixa eu tentar de novo" |
| Profundidade técnica | Consegue justificar decisões (por que essa arquitetura, por que esse banco) |
| Gestão do tempo | Respeita os 8 minutos, sem cortar abruptamente nem sobrar tempo vazio |

> **⚠️ Atenção**
> A apresentação é sobre o **projeto autoral publicado**, com URL pública real — apresentar rodando em `localhost` não mostra o que você realmente construiu. Se o deploy falhar na hora, tenha um vídeo curto de backup gravado com antecedência mostrando o fluxo funcionando.

### 8.3 Quando apresentar

Se você está seguindo esta trilha em uma turma com professor, apresente na ordem e no dia combinados por ele, dentro do tempo do encontro. Se está estudando por conta própria, grave a apresentação e revise-a no dia seguinte, ou apresente-a para outra pessoa — um colega de estudo, alguém da família, ou uma chamada rápida com alguém da comunidade. O que importa é o exercício em si: explicar o próprio projeto em voz alta, dentro de um tempo limitado.

## 9. Encerramento: caminhos depois desta trilha

O que foi construído nesta trilha é uma base real de desenvolvimento full stack moderno — mas é só o começo. Caminhos naturais de continuidade:

- **Nuxt** — framework full stack sobre o Vue, com SSR (Server-Side Rendering) e SSG (Static Site Generation) nativos, útil quando SEO ou performance de primeira carga importam mais do que em uma SPA pura.
- **TypeScript** — adicionar tipagem estática ao que hoje é JavaScript puro; o Vue 3 e o Vuetify 4 têm suporte de primeira classe a TS, e o ganho em projetos maiores (detecção de erro em tempo de escrita, autocomplete mais forte) é significativo.
- **Testes E2E** — Cypress ou Playwright, testando a aplicação inteira pela interface, como um usuário real faria — o topo da pirâmide de testes que só citamos na Aula 13.
- **Vue 3.6** — acompanhar o roadmap oficial do Vue (Vapor Mode e otimizações de compilador são a fronteira de pesquisa ativa do framework no momento).
- **Mobile com Capacitor/Ionic** — reaproveitar o conhecimento de Vue para publicar o mesmo código (ou uma variação) como app nativo Android/iOS.
- **Back-end com NestJS** — um framework Node.js opinativo, construído sobre Express (ou Fastify), que formaliza com decorators e módulos exatamente a arquitetura em camadas que construímos manualmente na Aula 13.

### 9.1 Como montar um portfólio a partir desta trilha

- Deixe o projeto autoral **publicado e funcionando** — um link ao vivo vale mais, para quem recruta, do que um repositório que só roda localmente.
- Escreva um README que conte a história do projeto: problema, decisões técnicas, dificuldades reais (os ADRs da Aula 14 são ótimo material bruto para isso).
- Grave um vídeo curto de demonstração e fixe no topo do repositório (ou no README, como GIF).
- Continue commitando — um projeto "morto" no GitHub (sem commit há meses) comunica menos do que um projeto pequeno e ativo.

### 9.2 Convite para iniciação científica e extensão

Muitos dos temas tocados de leve nesta trilha — arquitetura de software, segurança de aplicações web, engenharia de dados, IA aplicada a desenvolvimento — são linhas de pesquisa ativas na FACET, a instituição de origem deste material. Se você está cursando esta trilha por lá e algum tópico despertou curiosidade além do conteúdo de uma aula, procure o professor para conversar sobre projetos de iniciação científica ou extensão relacionados. Se você chegou até aqui por conta própria, esses mesmos temas são bons pontos de partida para aprofundar — grupos de pesquisa, comunidades on-line e cursos avançados costumam orbitar exatamente esses assuntos.

## 🧩 Padrão de projeto em uso — Configuração externa (Twelve-Factor) e Adapter

Duas decisões de arquitetura tomadas ao longo desta trilha ficam evidentes só agora, no momento de publicar de verdade.

**Configuração externa por variáveis de ambiente.** Desde a Aula 13, o `unieventos-api` lê `PORT`, `DB_HOST`, `CORS_ORIGEM_PERMITIDA` etc. de `process.env`, nunca de um valor fixo no código (Seção 3.1). Isso não é só "boa prática" abstrata: é o que permite o **mesmo código-fonte**, sem alterar uma linha, rodar em três ambientes diferentes — seu notebook (`.env` local), o CI (variáveis do GitHub Actions) e a nuvem (secrets da Render) — só trocando o que fica fora do código. O manifesto *The Twelve-Factor App* formalizou esse princípio (fator III, "Config") como um dos doze fatores de aplicações que escalam bem em nuvem; é o mesmo raciocínio por trás de `VITE_API_URL` no front (Seção 1.2).

```js
// PORT vem de fora — o mesmo código roda em dev, CI e produção sem mudar
const servidor = app.listen(config.PORT, () => {
  console.log(`API rodando na porta ${config.PORT}`)
})
```

**Adapter — trocar o banco sem tocar no service.** Na Aula 12, MySQL virou Supabase mantendo a mesma interface de repositório (`listar`, `buscarPorId`, `criar`, `atualizar`, `remover`) — o service nunca soube qual banco estava por trás. Hoje, ao decidir onde hospedar o banco de produção (MySQL gerenciado na Render/Railway, ou Supabase), essa escolha de infraestrutura continua isolada na camada de repositório: o `Adapter` já construído é exatamente o que torna essa decisão, tomada agora no deploy, indiferente para o resto da aplicação.

> **📌 Vale gravar**
> Configuração externa e Adapter resolvem problemas diferentes, mas se reforçam: uma isola **onde a aplicação roda**, a outra isola **em que banco ela persiste** — juntas, permitem que o mesmo código passe de `localhost` para produção sem reescrever uma linha de lógica de negócio.

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

### Como testar

O teste do deploy é feito **de fora**, numa aba anônima — exatamente como qualquer pessoa acessando de fora vai ver. Nada de "funciona na minha máquina".

```bash
# 1) a API publicada responde
curl -i https://<sua-api>.onrender.com/health
curl -s https://<sua-api>.onrender.com/api/eventos | jq '.paginacao'
```

Resultado esperado: `200 {"status":"ok"}` no health check e o objeto `paginacao` do envelope de listagem. Se a segunda chamada devolver `404`, o `/api` foi esquecido em algum lugar.

2. **Front publicado** — abra a URL da Vercel numa **janela anônima**. A lista de eventos carrega (dado real, vindo da API publicada). Resultado esperado: nenhum erro de CORS no console, e nenhuma requisição para `localhost`.
3. **Rota interna com F5** — navegue até `/eventos/1` e recarregue a página. Resultado esperado: a página carrega normalmente; um `404` aqui significa que falta o rewrite de SPA (Seção 1.4).
4. **Login e escrita** — faça login pelo Firebase e crie um evento. Resultado esperado: `201`, o evento aparece na lista, e outra pessoa abrindo a URL num outro computador vê o mesmo evento.
5. **Variáveis** — confira no painel da Vercel que `VITE_API_URL` termina em `/api`, e no painel da Render que `CORS_ORIGEM_PERMITIDA` é exatamente a URL do front (sem barra no fim).
6. **CI** — faça um commit qualquer e confirme na aba **Actions** que lint e testes rodaram no push.

Só depois que os seis passam é que o Marco 3 está de fato completo.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Verdadeiro ou falso, com justificativa de uma linha: "trocar `VITE_API_URL` no painel do serviço de hospedagem, depois que o front já está publicado, atualiza a URL usada pelo bundle sem precisar gerar um novo build."

Resultado esperado: falso. `import.meta.env.VITE_*` é substituído por um valor literal **em tempo de build** — trocar a variável depois, sem rebuildar, não tem efeito nenhum no JavaScript já gerado.

**A2.** Complete a linha que falta para que o rewrite de SPA funcione na Vercel (F5 numa rota interna não pode dar 404):

```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "______________" }
  ]
}
```

Resultado esperado: `"/index.html"`.

**A3.** Em uma frase: por que `app.listen(config.PORT, ...)` precisa ler `PORT` de `process.env` em vez de usar `3000` fixo no código?

Resultado esperado: porque a maioria dos serviços de nuvem injeta a própria porta via variável de ambiente — escutar numa porta fixa quebra o deploy nesses ambientes.

**A4.** Ache o erro nas linhas abaixo (a API sobe normalmente no `docker compose up`, mas todo endpoint que usa banco falha com erro de conexão):

```yaml
environment:
  DB_HOST: localhost
  DB_PORT: 3306
```

Resultado esperado: `DB_HOST` deveria ser o nome do serviço no `docker-compose.yml` (`mysql`), não `localhost` — dentro da rede criada pelo Compose, cada serviço enxerga os outros pelo nome do serviço, não por `localhost`.

**A5.** Preveja a saída: o workflow de CI tem `on.push.branches: ['**']` e o job `deploy` com `if: github.ref == 'refs/heads/main' && github.event_name == 'push'`. Você faz `git push` numa branch `feature/relatorio`. O job `deploy` roda?

Resultado esperado: não. `lint-e-testes` roda (o push bateu em alguma branch, e o padrão `'**'` cobre qualquer uma), mas `deploy` não roda, porque a condição `if` exige que a branch seja `main`.

### Nível B — Aplicação

**B1.** Gere o build de produção do seu projeto autoral e rode `npm run preview` — confirme que todas as rotas funcionam, incluindo F5 em rota interna.

Resultado esperado: nenhum erro no console, navegação idêntica ao ambiente de desenvolvimento.

<details markdown="1">
<summary>Dica</summary>

Se uma rota der 404 até no `preview` local, o problema é de configuração de rota no Vue Router, não de hospedagem — resolva isso antes de publicar.
</details>

**B2.** Publique o front-end em um dos serviços da Seção 2, com as variáveis `VITE_*` corretas.

Resultado esperado: URL pública funcionando, aplicação carrega sem tela em branco.

<details markdown="1">
<summary>Dica</summary>

Se a tela ficar em branco sem erro óbvio, abra o Console do DevTools primeiro — normalmente aponta uma variável de ambiente `undefined`.
</details>

**B3.** Publique o back-end em um dos serviços da Seção 3, com `/health` respondendo publicamente.

Resultado esperado: `curl https://sua-api.onrender.com/health` retorna `{"status":"ok",...}`.

<details markdown="1">
<summary>Dica</summary>

Rode as migrations manualmente pelo shell do serviço antes de testar qualquer rota que dependa de tabela do banco.
</details>

**B4.** Configure CORS restritivo em produção, apontando exatamente para a URL do front publicado.

Resultado esperado: requisições do front publicado funcionam; uma requisição feita a partir de uma origem diferente é bloqueada.

<details markdown="1">
<summary>Dica</summary>

Teste abrindo o Console do navegador em uma aba com origem diferente (ex.: `http://localhost:5500`) e tentando um `fetch` contra sua API publicada — deve falhar por CORS.
</details>

### Nível C — Desafio

**C1.** Crie o workflow de CI/CD completo no seu repositório de back-end: um job `lint-e-testes` que roda em qualquer push, e um job `deploy` que só roda depois do primeiro passar, restrito à branch `main`, disparando o deploy de verdade (deploy hook do seu serviço de hospedagem).

Resultado esperado: um push numa branch de feature só dispara `lint-e-testes`; um push (ou merge) em `main` dispara os dois jobs, e a aba **Actions** do GitHub mostra ambos passando em verde, nessa ordem.

<details markdown="1">
<summary>Dica</summary>

Se você não tiver `npm run lint` configurado, o `--if-present` do comando na Seção 5 evita que o workflow falhe por esse motivo — mas vale configurar ESLint se ainda não tiver. Para o `deploy hook`, gere a URL no painel do seu serviço de hospedagem e guarde como *secret* do repositório — nunca em texto puro no workflow.
</details>

## 🏆 Desafios

### ⭐ Quanto custa acordar o servidor
Tags: deploy, devtools, investigacao, performance

Planos gratuitos de hospedagem "dormem" o processo depois de um tempo sem tráfego (Seção 3.2) — mas quanto tempo, exatamente, uma requisição demora para acordar um serviço adormecido, comparado com uma requisição normal? Meça e documente, em vez de só repetir o que a Seção 3.2 avisa.

**Critérios de pronto**

- Duas medições com `curl -w '%{time_total}\n' -o /dev/null -s https://sua-api.onrender.com/health`: uma logo depois de um período sem tráfego (cold start) e outra imediatamente em seguida (processo já acordado).
- Uma tabela de duas linhas no README compara os dois tempos.
- Uma frase explica por que `/health` é a rota certa para esse teste (não depende de banco nem de autenticação — Seção 3.1).
- Uma sugestão registrada (não precisa implementar) de como reduzir esse impacto para quem for apresentar o projeto ao vivo (ex.: "acordar" o serviço minutos antes da apresentação).

<details markdown="1">
<summary>Pistas</summary>

1. `-w '%{time_total}\n'` imprime só o tempo total da requisição, em segundos; `-o /dev/null` descarta o corpo da resposta, que não importa aqui.
2. Espere alguns minutos sem fazer nenhuma requisição ao serviço antes da primeira medição, para garantir que ele realmente "dormiu".
3. Compare também o que aparece na aba Network do DevTools ao abrir o front publicado logo depois do cold start — a primeira chamada à API "trava" visivelmente mais que as seguintes.
</details>

### ⭐⭐ O F5 que só quebra em produção
Tags: deploy, spa, bug, investigacao

Um colega jura que testou tudo: `npm run preview` local funciona perfeitamente, F5 em qualquer rota interna funciona. Mas depois de publicado, o mesmo F5 em `/eventos/3` devolve uma página de erro genérica do provedor de hospedagem, `404 Not Found`. "Funciona na minha máquina" de novo. Investigue a diferença entre o ambiente local (`vite preview`) e o provedor de hospedagem escolhido.

**Critérios de pronto**

- Um comentário identifica exatamente qual arquivo de configuração está ausente ou mal escrito no repositório publicado (`vercel.json`, `_redirects` ou `firebase.json`, conforme o serviço).
- Depois de corrigido, um F5 em pelo menos duas rotas internas diferentes, na aplicação publicada, devolve a página certa, sem 404.
- Uma frase explica por que `vite preview` **nunca** reproduz esse bug sozinho — ele já simula o rewrite de SPA por padrão, então o problema só aparece quando o arquivo de configuração do provedor real está ausente.
- Um teste com `curl -I` na URL publicada de uma rota interna confirma o status `200` (não `404`) depois da correção.

<details markdown="1">
<summary>Pistas</summary>

1. Confira se o arquivo de rewrite (`vercel.json`, `_redirects` ou o trecho de `firebase.json`) está **versionado no Git** e não só criado localmente e esquecido no `.gitignore`.
2. Para o Netlify/`_redirects`, lembre que o arquivo precisa estar dentro de `public/` para o Vite copiá-lo para `dist/` no build — fora dali, ele nunca chega à hospedagem.
3. `curl -I https://seu-front.vercel.app/eventos/3` mostra só os cabeçalhos e o status — mais rápido que abrir o navegador para conferir o resultado repetidas vezes.
</details>

### ⭐⭐⭐ Um deploy que se testa sozinho
Tags: ci-cd, deploy, testes, terminal

Hoje, se um deploy quebrar (uma variável de ambiente errada, uma migration esquecida), você só descobre quando alguém tenta usar a aplicação e encontra um erro. Implemente um **smoke test pós-deploy**: um passo automático no workflow de CI/CD que, depois de publicar, confirma que a aplicação está realmente funcionando — e falha o workflow (avisando você) se não estiver.

**Critérios de pronto**

- Um script `scripts/smoke-test.sh` (ou `.js`) que roda depois do job `deploy`: chama `/health` da API publicada e confirma `200`; chama um endpoint de leitura pública (ex.: `GET /api/eventos`) e confirma que a resposta é uma lista válida; tenta uma escrita sem token e confirma que a resposta é `401` (nunca `500`).
- Se qualquer uma dessas três checagens falhar, o script termina com código de saída diferente de zero, e o job do GitHub Actions aparece em vermelho.
- O script está incluído como o último passo do job `deploy` no `.github/workflows/ci.yml`.
- Um teste proposital: aponte o script para uma URL errada (ou pare o serviço) e confirme que o workflow realmente falha — não é suficiente que o script "pareça correto" sem nunca ter sido visto falhando.

<details markdown="1">
<summary>Pistas</summary>

1. Um script simples com `curl -f` (a flag `-f` faz o `curl` retornar código de erro se o status HTTP não for de sucesso) já cobre boa parte da checagem, sem precisar de biblioteca extra.
2. Para o teste de escrita sem token, `curl -s -o /dev/null -w '%{http_code}'` imprime só o código de status, fácil de comparar num `if` do shell.
3. Espere alguns segundos depois do deploy hook antes de rodar o smoke test — o serviço pode levar um instante para religar o processo com o novo código.
4. Rode o script manualmente contra sua API já publicada antes de colocá-lo no workflow — mais fácil depurar localmente do que lendo logs do GitHub Actions.
</details>

### 🔥 Boss — Seu projeto autoral, no ar e à prova de F5
Tags: deploy, ci-cd, projeto, testes

Chegamos ao fim das três unidades. Este é o desafio que fecha a trilha: seu projeto autoral publicado, de ponta a ponta, com todas as camadas construídas ao longo das aulas funcionando juntas em produção — e não só "funcionando", mas resistindo aos testes que costumam derrubar um projeto assim que alguém de fora tenta usá-lo.

**Critérios de pronto**

- Front-end e back-end publicados com URL pública, sem depender de `localhost` em lugar nenhum — nem em texto do README, nem em variável de ambiente esquecida.
- CRUD completo de pelo menos 2 entidades relacionadas, autenticação protegendo as rotas de escrita, e um papel diferenciado (ex.: admin) funcionando de verdade em produção — não só localmente.
- `/api-docs` acessível publicamente, com todos os endpoints documentados e o botão "Authorize" funcionando com um token real, obtido do seu Firebase de produção.
- Um script `scripts/smoke-test.sh` (do desafio ⭐⭐⭐, ou um novo) que roda depois do deploy, incluído como último passo do workflow de CI/CD.
- F5 em pelo menos três rotas internas diferentes, na aplicação publicada, não produz `404` em nenhuma delas.
- Um parágrafo no README relaciona, para cada uma das três unidades desta trilha, um padrão de projeto (da tabela consolidada da Seção 6) que sobrevive intacto na versão publicada — com o nome do arquivo e a linha onde ele aparece.

<details markdown="1">
<summary>Pistas</summary>

1. Comece pelo smoke test — ele é o que prova, de fora para dentro, que "está no ar" significa mais do que a página inicial carregar.
2. Para testar F5 em produção sem abrir o navegador manualmente três vezes, um script com `curl -I` em cada rota (a resposta, graças ao rewrite de SPA, deve vir com `200`, nunca `404`) automatiza a checagem.
3. O parágrafo de padrões não precisa ser longo — uma linha por unidade já cumpre o critério, desde que aponte um trecho de código real, não só o nome do padrão.
4. Se o smoke test falhar depois de um deploy automático, registre no README como um ADR curto (Aula 14): o que quebrou e por quê — é exatamente esse tipo de decisão que outra pessoa (ou você mesmo, em três meses) vai querer entender.
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

## 🏠 Para praticar depois da aula (1 h)

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

## 🎓 Marco do projeto — Unidade 3

O Marco 3 fecha esta trilha: uma aplicação full stack completa, construída sobre o projeto autoral definido na Aula 01 e evoluído ao longo de todas as aulas.

### Requisitos

1. Back-end próprio, em **Express** ou usando **Supabase** como back-end gerenciado (ou uma combinação dos dois, desde que a arquitetura em camadas da Aula 13 esteja presente onde houver código Express) — **Aulas 07/13**.
2. Banco de dados persistente (MySQL ou Supabase/Postgres), com **schema versionado** (migrations ou scripts SQL organizados) — **Aulas 09/12**.
3. Autenticação funcional (Firebase Auth ou autenticação nativa do Supabase), protegendo pelo menos as rotas de escrita (criação/edição/remoção) — **Aula 10**.
4. **CRUD completo de pelo menos 2 entidades relacionadas** (ex.: "Evento" e "Inscrição"), com relacionamento real no banco (chave estrangeira ou equivalente) — **Aula 11**.
5. Documentação **Swagger** (OpenAPI 3) cobrindo todos os endpoints, ou documentação equivalente de todas as políticas/endpoints se o back for majoritariamente Supabase — **Aula 14**.
6. **Deploy funcionando com URL pública** — tanto do front quanto do back (ou só do front, se usando Supabase como back completo) — **Aula 15**.
7. **README completo**, seguindo a estrutura da Aula 14 (badges, requisitos, instalação, variáveis de ambiente, scripts, endpoints, licença), com os links de aplicação publicada e repositório.

### Checklist de qualidade

O que separa um projeto pronto de um feito às pressas na véspera:

- [ ] CRUD completo de 2+ entidades relacionadas funcionando de ponta a ponta (criar, listar, editar, remover), com relacionamento real entre elas.
- [ ] Banco de dados corretamente modelado: schema versionado, queries corretas, sem duplicação nem inconsistência de dados.
- [ ] Rotas de escrita exigindo usuário autenticado, com a identidade usada corretamente (ex.: só o dono edita/remove seu próprio recurso).
- [ ] Documentação Swagger/OpenAPI completa: todos os endpoints documentados, schemas reutilizáveis, segurança declarada, `/api-docs` acessível.
- [ ] Front e back publicados e acessíveis externamente, sem depender de `localhost` em nenhum lugar (nem no README, nem em variável de ambiente esquecida).
- [ ] README completo conforme a estrutura da Aula 14; arquitetura em camadas aplicada; ao menos alguns testes automatizados presentes.

### Como saber que está pronto

- Abra a aplicação publicada em uma aba anônima do navegador (sem cache, sem sessão salva) e percorra o fluxo completo: listar, ver detalhe, autenticar, criar, editar, remover.
- Teste com `curl` (ou uma aba anônima) que uma rota de escrita sem token retorna `401`/`403`, não `200`.
- Abra `/api-docs` publicamente e use o botão "Authorize" com um token real — todos os endpoints devem responder como documentado.
- Aperte F5 em pelo menos três rotas internas da aplicação publicada: nenhuma deve retornar `404`.
- Rode `npm install && npm run dev` (ou `docker compose up`) em uma cópia limpa dos dois repositórios e confirme que tudo sobe sem passo não documentado no README.
- Explique em voz alta, para um colega ou para você mesmo, uma decisão técnica do próprio código — se travar, é sinal de que vale revisar aquele trecho antes da apresentação.

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
- Bibliografia do plano de curso FACET-SNP-310 — capítulos sobre implantação, integração contínua e ciclo de vida de aplicações web.

---

**Fim da trilha.** Obrigado pelo empenho nas 15 aulas — do primeiro `console.log` da Aula 01 até uma aplicação full stack publicada, com autenticação, banco de dados e documentação. Se você quer testar o quanto absorveu, revise as questões da Seção 7 com calma, não na véspera da apresentação. Bom estudo, e bom portfólio.
