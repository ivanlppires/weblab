# Capítulo 09 — CI/CD com GitHub Actions

> **Deploy & Ferramentas** · Unidade 3: Infraestrutura, automação e qualidade
> WebLab · curso aberto de desenvolvimento web
> **Tempo estimado:** 2 a 3 h · estudo autônomo, em paralelo à sua trilha

## 🎯 Objetivos de aprendizagem

Ao final deste capítulo você será capaz de:

- Explicar o que são integração contínua e entrega contínua, e que problema real cada uma resolve em um time (mesmo um time de duas pessoas).
- Ler e escrever um workflow do GitHub Actions em YAML, distinguindo workflow, evento, job, step, runner e action.
- Montar um workflow de CI que instala com `npm ci`, roda lint e testes a cada push e pull request, com cache de dependências e um banco de verdade em contêiner de serviço.
- Guardar credenciais em *secrets* e variáveis do repositório, e usá-las sem vazá-las nos logs.
- Publicar automaticamente um site estático no GitHub Pages (ou no Netlify) a partir do `main`.
- Construir e enviar a imagem Docker para o GHCR e atualizar o VPS por SSH, com tag rastreável e rollback em um comando.
- Proteger a branch principal exigindo que a esteira passe, e exibir o badge do resultado no `README.md`.

## 📋 Pré-requisitos

- [ ] `unieventos-api` com `npm test` funcionando localmente (Aula 13 do Nível 3: vitest + supertest) e `Dockerfile` do Capítulo 07.
- [ ] Banco na nuvem configurado por `DATABASE_URL` (Capítulo 08) — é o que torna o deploy automático seguro.
- [ ] Repositório no GitHub com a branch `main` (Capítulo 02) e a imagem já publicada uma vez no GHCR na mão (Capítulo 07).
- [ ] VPS acessível por SSH com o usuário `deploy`, `docker compose` instalado e `compose.prod.yaml` funcionando (Capítulos 06 e 07).
- [ ] `unieventos-web` (ou o `site-evento` do Nível 1) gerando `dist/` com `npm run build`.

> No Capítulo 07 você construiu a imagem na sua máquina e a subiu no GHCR digitando os comandos; no Capítulo 08 o banco saiu do servidor e a `unieventos-api` ficou **sem estado** — uma imagem Docker que pode ser destruída e recriada sem perder nada. Só que o caminho até o ar ainda é manual: você constrói a imagem no notebook, faz `docker push`, abre o SSH, roda `docker compose pull` e torce. São seis comandos em três máquinas, na ordem certa, sempre que muda uma linha — e alguém vai esquecer um deles em uma sexta-feira à noite. Hoje esse trabalho passa a ser feito por um robô a cada `git push`: instalar dependências, rodar lint e testes, publicar o site estático, construir a imagem, enviar para o GHCR e atualizar o VPS por SSH — e a branch `main` ganha um porteiro, que recusa o código que não passar pela esteira. No Capítulo 10 essa mesma esteira ganha medidas de qualidade — cobertura, Lighthouse e monitoramento de erros em produção.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | CI/CD na prática; anatomia de um workflow; o primeiro `ci.yml` com lint, testes e cache |
| 2 | 50 min | Segredos; banco em contêiner de serviço; publicação automática do site estático |
| 3 | 50 min | Imagem no GHCR, deploy por SSH com rollback, proteção de branch, badge e Laboratório |

## 1. Integração e entrega contínuas

Duas siglas, dois problemas diferentes.

**CI — integração contínua.** Cada mudança é integrada ao código principal várias vezes por dia, e **uma máquina neutra** verifica se ela continua funcionando. A palavra importante é "neutra": o teste que roda no seu computador prova que funciona *no seu computador*, com as suas variáveis de ambiente, as suas dependências instaladas há três meses e aquele arquivo que você esqueceu de commitar. O runner do GitHub começa do zero, clona o repositório e só tem o que está versionado. É por isso que a CI pega o clássico "esqueci de commitar o `package-lock.json`".

**CD — entrega/implantação contínua.** O que passou na CI vai para produção **sem intervenção manual**. O ganho não é preguiça: é que o deploy deixa de ser um evento raro e assustador (e por isso arriscado) e vira uma rotina de dois minutos que acontece dez vezes por semana. Quanto menor a mudança que vai ao ar, mais fácil descobrir qual delas quebrou.

A esteira que você vai montar:

```text
git push
   │
   ├─► CI ......... npm ci → lint → testes         (todo push e todo PR)
   │                  │
   │                  └─ falhou? o PR fica vermelho e não pode ser mesclado
   │
   └─► main ─┬─► site estático: build → GitHub Pages
             │
             └─► API: build da imagem → GHCR → ssh no VPS → compose pull/up → /health
```

Três princípios que valem mais que qualquer YAML:

1. **A esteira é a fonte da verdade.** "Na minha máquina passa" não conta. Se o teste falha na CI, o código está errado — ou o teste depende de algo que não está versionado.
2. **Rápido ou ninguém usa.** Uma CI de 15 minutos é ignorada; as pessoas mesclam sem esperar. Cache, jobs paralelos e testes que não dependem de rede mantêm o ciclo abaixo de 3 minutos.
3. **Falha barulhenta, sucesso silencioso.** O sucesso é o esperado. O que precisa gritar é a falha — no PR, no badge e, se você quiser, no e-mail.

> **🧠 Você sabia?**
> A ideia de integrar o trabalho de todo mundo continuamente é bem mais velha que a nuvem: nos anos 1990 o *daily build* da Microsoft era uma regra quase religiosa, e quem quebrasse a compilação do dia herdava um chapéu ridículo ou o dever de vigiar o próximo build. O ritual era feio, mas o objetivo é exatamente o mesmo de um workflow de CI: tornar visível, no mesmo dia, quem quebrou o quê — em vez de descobrir na integração final, quando já é impossível saber qual das duzentas mudanças foi a culpada.

> **🔬 Investigue**
> Abra um projeto popular no GitHub (por exemplo `vuejs/core` ou `expressjs/express`), entre na aba **Actions** e escolha uma execução recente. Responda: quantos jobs rodam em paralelo? Quanto tempo levou o mais lento? Em qual sistema operacional cada um roda? Depois clique em um step e veja o log linha a linha. Você está lendo exatamente o mesmo tipo de arquivo YAML que vai escrever nos próximos 40 minutos — a diferença é a quantidade de jobs, não a complexidade de cada um.

## 2. Anatomia de um workflow

Um workflow é um arquivo YAML dentro de `.github/workflows/` no seu repositório. O GitHub lê a pasta a cada push e obedece ao que estiver lá. O vocabulário:

| Termo | O que é |
|---|---|
| **workflow** | um arquivo `.yml`; tem um nome, uma lista de eventos e um ou mais jobs |
| **evento** (`on:`) | o que dispara: `push`, `pull_request`, `schedule`, `workflow_dispatch` (botão manual) |
| **job** | um conjunto de steps que roda em **uma máquina**; jobs rodam em paralelo por padrão |
| **runner** | a máquina temporária (`ubuntu-latest`) criada para o job e destruída no fim |
| **step** | um passo: ou um `run:` (comando de shell) ou um `uses:` (uma action pronta) |
| **action** | um pedaço reutilizável, referenciado por `dono/nome@versão` |
| **secret** | valor cifrado do repositório, disponível como `${{ secrets.NOME }}` |

O menor workflow útil que existe:

```yaml
# .github/workflows/exemplo.yml
name: Exemplo

on: [push]

jobs:
  dizer-oi:
    runs-on: ubuntu-latest
    steps:
      - name: Falar com o mundo
        run: echo "rodando no commit ${{ github.sha }}"
```

Cinco regras de YAML que resolvem 90% dos erros de sintaxe:

- **Indentação é com espaços, nunca com tabulação.** Dois espaços por nível é a convenção.
- **Lista é `-` no começo da linha**, no mesmo nível dos irmãos.
- **`chave: valor`** precisa do espaço depois dos dois-pontos.
- **Valor com `:` dentro precisa de aspas**: `run: "echo a: b"`.
- **Bloco de várias linhas** usa `|` (preserva as quebras) — é como se escrevem scripts inteiros dentro de um `run:`.

> **💡 Dica**
> O VS Code entende workflows do GitHub Actions se você instalar a extensão oficial **GitHub Actions**: ela valida o YAML enquanto você digita, completa nomes de actions e avisa quando uma chave não existe. Vale mais do que descobrir o erro dois minutos depois, no log da execução.

### Onde cada coisa roda

Cada job começa em uma máquina virtual **limpa**, com Ubuntu, Git, Node, Docker e mais uma centena de ferramentas pré-instaladas. Duas consequências que confundem todo mundo no começo:

1. **Jobs não compartilham disco.** O que o job A baixou não existe no job B. Para passar arquivos entre jobs, use artefatos (`actions/upload-artifact`) ou reconstrua.
2. **Cada step compartilha o disco, mas não o shell.** Um `cd pasta` em um step não vale no próximo (use `working-directory:`), e uma variável exportada com `export` some (escreva em `$GITHUB_ENV`).

## 3. Workflow 1 — CI: lint e testes

Este é o workflow que você vai usar todos os dias. Ele roda a cada push no `main` e a cada pull request:

```yaml
# unieventos-api/.github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

# Princípio do menor privilégio: este workflow só precisa LER o repositório.
permissions:
  contents: read

# Se você empurrar dois commits seguidos, cancela a execução antiga e roda só a nova.
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  verificar:
    name: Lint e testes
    runs-on: ubuntu-latest
    timeout-minutes: 10

    # O config.js valida o ambiente com zod (Aula 13): sem estas variáveis o processo
    # nem sobe. No runner não existe .env, então elas entram aqui. Os testes usam
    # repositórios falsos, então a DATABASE_URL só precisa ter forma válida.
    env:
      NODE_ENV: test
      DATABASE_URL: postgresql://postgres:teste@localhost:5432/unieventos_teste
      FIREBASE_PROJECT_ID: projeto-de-teste
      CORS_ORIGEM_PERMITIDA: http://localhost:5173

    steps:
      - name: Baixar o código
        uses: actions/checkout@v4

      - name: Preparar o Node 22 com cache do npm
        uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: npm

      - name: Instalar dependências do lockfile
        run: npm ci

      - name: Conferir o estilo do código
        run: npm run lint --if-present

      - name: Rodar os testes
        run: npm test
```

Passo a passo do que acontece:

- **`actions/checkout@v4`** clona o repositório dentro do runner. Sem ele, a máquina está vazia — é o step que todo workflow começa.
- **`actions/setup-node@v4` com `cache: npm`** instala o Node 22 e restaura o cache do npm a partir do `package-lock.json`. Na primeira execução ele guarda; nas seguintes, o `npm ci` cai de ~40 s para ~8 s.
- **`npm ci`** (e não `npm install`) instala exatamente as versões travadas no lockfile e **falha** se o `package.json` e o `package-lock.json` estiverem dessincronizados. Em CI é sempre `ci`.
- **`--if-present`** faz o npm ignorar um script que ainda não existe. Assim o workflow já funciona antes de você montar o ESLint (Capítulo 10).
- **`timeout-minutes`** evita que um teste travado consuma minutos de execução até o limite padrão de seis horas.

> **⚠️ Atenção**
> `npm ci` apaga a pasta `node_modules` e reinstala do zero. Se o seu `package-lock.json` não estiver commitado, o step falha com `npm ci can only install packages when your package.json and package-lock.json … are in sync`. Rode `npm install` localmente, commite o lockfile e empurre de novo — é o erro número um de quem monta a primeira CI.

### 3.1 Testes de integração com um banco de verdade

Os testes da Aula 13 usam repositórios falsos e não precisam de banco. Mas em algum momento você vai querer testar a consulta SQL de verdade. O GitHub sobe contêineres auxiliares para o job com a chave `services:` — é o `docker compose` do Capítulo 07, embutido na CI:

```yaml
# unieventos-api/.github/workflows/ci.yml — segundo job, no mesmo arquivo
  integracao:
    name: Testes de integração com Postgres
    runs-on: ubuntu-latest
    timeout-minutes: 15

    services:
      postgres:
        image: postgres:17-alpine
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: teste
          POSTGRES_DB: unieventos_teste
        ports:
          - 5432:5432
        # Sem healthcheck o job começa antes de o banco aceitar conexão.
        options: >-
          --health-cmd "pg_isready -U postgres"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    env:
      NODE_ENV: test
      DATABASE_URL: postgresql://postgres:teste@localhost:5432/unieventos_teste
      FIREBASE_PROJECT_ID: projeto-de-teste
      CORS_ORIGEM_PERMITIDA: http://localhost:5173

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: npm

      - run: npm ci

      - name: Criar o schema no banco do job
        run: npm run migrar

      - name: Rodar a suíte inteira
        run: npm test
```

O contêiner de serviço fica acessível em `localhost:5432` porque a porta foi mapeada. Falta um detalhe: o pool do Capítulo 08 exige TLS com certificado, e esse Postgres local não tem TLS nenhum. Torne a decisão explícita no código, em vez de manter dois arquivos:

```js
// src/db/pool.js — trecho: TLS só quando o banco é remoto
const ehBancoLocal = /@(localhost|127\.0\.0\.1)[:/]/.test(config.DATABASE_URL)

export const pool = new pg.Pool({
  connectionString: config.DATABASE_URL,
  ssl: ehBancoLocal
    ? false
    : { ca: certificadoDaAutoridade, rejectUnauthorized: true },
  max: 10,
})
```

> **🔎 Por baixo do capô**
> Contêiner de serviço não é a mesma coisa que `docker compose`: o GitHub cria uma rede própria para o job e sobe cada serviço nela **antes** do primeiro step. Se os steps rodassem dentro de um contêiner (chave `container:`), o endereço do banco seria o nome do serviço (`postgres:5432`), como no compose; como os nossos steps rodam direto no runner, o endereço é `localhost` na porta que você mapeou. Trocar um pelo outro é a causa de metade dos `ECONNREFUSED` em CI.

### 3.2 Matriz: a mesma suíte em várias versões

Se o seu projeto precisa funcionar em mais de uma versão do Node, a matriz cria um job por combinação, todos em paralelo:

```yaml
  compatibilidade:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false        # não cancela as outras quando uma falha
      matrix:
        node: ['22', '24']
    name: Testes no Node ${{ matrix.node }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
          cache: npm
      - run: npm ci
      - run: npm test
        env:
          NODE_ENV: test
          DATABASE_URL: postgresql://postgres:teste@localhost:5432/unieventos_teste
          FIREBASE_PROJECT_ID: projeto-de-teste
          CORS_ORIGEM_PERMITIDA: http://localhost:5173
```

## 4. Segredos e variáveis

A chave SSH do VPS, o token do Netlify e a senha do banco não podem entrar no repositório. O GitHub guarda esses valores cifrados em **Settings → Secrets and variables → Actions**:

- **Secrets** — cifrados, nunca exibidos de novo depois de salvos, e mascarados nos logs (aparecem como `***`). Use para senhas, tokens e chaves.
- **Variables** — texto simples, visível no painel e no log. Use para coisas não sensíveis, como a URL pública da API.

```yaml
      - name: Usar um segredo sem vazá-lo
        run: |
          # CERTO: o valor vai para a variável de ambiente do processo
          curl -fsS -H "Authorization: Bearer $TOKEN" https://api.exemplo.com/status
        env:
          TOKEN: ${{ secrets.TOKEN_DA_API }}
```

Três regras sobre segredos:

1. **Nunca imprima um segredo.** `echo "${{ secrets.X }}"` é mascarado pelo GitHub, mas qualquer transformação (base64, uma quebra em pedaços) escapa da máscara e vira log público para sempre.
2. **Um segredo por finalidade.** Uma chave SSH só para o deploy, revogável sem afetar o resto.
3. **Segredos não existem em PRs de forks.** Quem abre um pull request a partir de um fork não recebe os seus segredos — por segurança óbvia. Por isso o job de deploy roda só em `push` no `main`, nunca em `pull_request`.

Além dos seus, o GitHub injeta em todo workflow um segredo automático, o **`GITHUB_TOKEN`**: um token temporário, válido só durante a execução, cujas permissões você declara no bloco `permissions:`. É com ele que o workflow publica no GHCR (§6) sem você criar token nenhum.

> **⚠️ Atenção**
> `permissions:` sem declaração herda o padrão da organização, que pode ser de escrita em tudo. Declare sempre o mínimo: `contents: read` para CI, mais `packages: write` para publicar imagem, mais `pages: write` e `id-token: write` para o Pages. Um workflow comprometido com permissão de escrita pode reescrever o seu repositório.

## 5. Workflow 2 — publicar o site estático

No Capítulo 03 você publicou o `site-evento` no GitHub Pages arrastando arquivos e escolhendo uma branch. Agora o Pages passa a ser alimentado pelo próprio workflow — o que resolve o caso de um site que **precisa ser construído** antes (Vite, do Nível 3).

```yaml
# unieventos-web/.github/workflows/publicar-site.yml
name: Publicar site

on:
  push:
    branches: [main]
  workflow_dispatch:          # botão "Run workflow" na aba Actions

permissions:
  contents: read
  pages: write                # publicar no Pages
  id-token: write             # provar ao Pages que a publicação veio deste workflow

# Um deploy por vez, sem cancelar o que já começou a publicar.
concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  construir:
    name: Construir o site
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Preparar o Pages
        id: pages
        uses: actions/configure-pages@v5

      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: npm

      - run: npm ci

      # base_path resolve o subcaminho /nome-do-repositorio/ do Pages (Capítulo 03).
      - name: Gerar o dist/
        run: npm run build -- --base="${{ steps.pages.outputs.base_path }}"
        env:
          VITE_API_URL: ${{ vars.VITE_API_URL }}

      - name: Empacotar o dist/ como artefato do Pages
        uses: actions/upload-pages-artifact@v3
        with:
          path: dist

  publicar:
    name: Publicar no Pages
    needs: construir            # só roda se o build terminou bem
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.publicacao.outputs.page_url }}
    steps:
      - name: Publicar
        id: publicacao
        uses: actions/deploy-pages@v4
```

Antes do primeiro push, ligue a chave: **Settings → Pages → Build and deployment → Source: GitHub Actions**. Sem isso o job falha com `Get Pages site failed`.

Repare em duas coisas:

- **`vars.VITE_API_URL`** é uma *variável* (não segredo): a URL pública da API vai ser embutida no JavaScript e ficaria visível de qualquer jeito. Como você viu no Capítulo 07, tudo que começa com `VITE_` é resolvido em tempo de **build** — mudar a variável exige rodar o workflow de novo.
- **`environment:`** cria um ambiente nomeado no GitHub, com histórico de implantações e a URL clicável no fim da execução. É também onde se configura aprovação manual (§8).

### Alternativa: Netlify

Se o site está no Netlify (Capítulo 03), troque os dois jobs por um step só, usando a CLI oficial:

```yaml
      - name: Publicar no Netlify
        run: npx --yes netlify-cli deploy --prod --dir=dist --message "commit ${{ github.sha }}"
        env:
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
```

O token sai de **User settings → Applications → Personal access tokens** no Netlify, e o `NETLIFY_SITE_ID` do painel do site (`Site configuration → General`). Em produção, fixe a versão principal da CLI (`netlify-cli@<versão>`) para não ser surpreendido por uma mudança de comportamento.

## 6. Workflow 3 — imagem no GHCR e deploy no VPS

Este é o workflow que fecha a esteira: constrói a imagem do Capítulo 07, publica no GHCR e manda o VPS baixar a nova versão.

```yaml
# unieventos-api/.github/workflows/deploy.yml
name: Publicar imagem e implantar

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  packages: write             # publicar no GitHub Container Registry

concurrency:
  group: deploy-producao
  cancel-in-progress: false   # nunca cancele um deploy pela metade

jobs:
  imagem:
    name: Construir e publicar a imagem
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@v4

      - name: Preparar o Buildx
        uses: docker/setup-buildx-action@v3

      - name: Autenticar no GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Calcular nome e tags da imagem
        id: metadados
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }}
          # prefix= (vazio) remove o prefixo padrão "sha-": a tag fica sendo
          # exatamente o SHA do commit, o mesmo valor usado no deploy abaixo.
          tags: |
            type=sha,format=long,prefix=
            type=raw,value=latest

      - name: Construir e enviar
        uses: docker/build-push-action@v6
        with:
          context: .
          platforms: linux/amd64
          push: true
          tags: ${{ steps.metadados.outputs.tags }}
          labels: ${{ steps.metadados.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  implantar:
    name: Implantar no VPS
    needs: imagem
    runs-on: ubuntu-latest
    timeout-minutes: 10
    environment: producao
    steps:
      - name: Atualizar os contêineres por SSH
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_USUARIO }}
          key: ${{ secrets.VPS_CHAVE_SSH }}
          script: |
            set -e
            cd /srv/unieventos-api
            export TAG_IMAGEM="${{ github.sha }}"
            docker compose -f compose.prod.yaml pull
            docker compose -f compose.prod.yaml up -d
            docker image prune -f
            for tentativa in 1 2 3 4 5 6 7 8 9 10; do
              if curl -fsS http://127.0.0.1:3000/health > /dev/null; then
                echo "no ar na versão $TAG_IMAGEM"
                exit 0
              fi
              sleep 3
            done
            echo "a API não respondeu ao /health em 30 s"
            exit 1
```

### 6.1 A tag que permite voltar atrás

`docker/metadata-action@v5` calcula as tags da imagem a partir do evento. Com a configuração acima, cada push no `main` publica **duas** tags para a mesma imagem: `latest` e o SHA completo do commit (`ghcr.io/usuario/unieventos-api:9f2c1a…`). O `prefix=` vazio importa: sem ele, `type=sha` gera `sha-9f2c1a…`, e o script de deploy — que usa `${{ github.sha }}` puro — pediria uma tag que não existe, falhando com `manifest unknown`.

Para o `compose.prod.yaml` usar essa tag, troque a versão fixa por uma variável:

```yaml
# /srv/unieventos-api/compose.prod.yaml — trecho alterado
services:
  api:
    image: ghcr.io/seu-usuario/unieventos-api:${TAG_IMAGEM:-latest}
    ports:
      - "127.0.0.1:3000:3000"
    env_file: .env
    init: true
    restart: unless-stopped
```

`${TAG_IMAGEM:-latest}` significa "use a variável `TAG_IMAGEM`; se ela não existir, use `latest`". Como o script do deploy exporta `TAG_IMAGEM` com o SHA do commit, o servidor sobe exatamente a imagem daquele commit — e o **rollback** vira um comando só, com o SHA do commit anterior:

```bash
ssh meuvps
cd /srv/unieventos-api
TAG_IMAGEM=<sha-do-commit-anterior> docker compose -f compose.prod.yaml up -d
```

> **💡 Dica**
> Publicar só `latest` parece mais simples e é uma armadilha: `latest` não identifica nada, dois deploys diferentes têm a mesma tag e não existe para onde voltar. Tag por commit é o que transforma "deu ruim, e agora?" em trinta segundos de rollback.

### 6.2 A chave SSH do robô

Não use a sua chave pessoal. Gere um par dedicado, sem senha (o robô não tem como digitá-la), e autorize só ele:

```bash
# na SUA máquina
ssh-keygen -t ed25519 -C "github actions unieventos" -f chave-deploy -N ""

# envia a chave PÚBLICA para o VPS
ssh-copy-id -i chave-deploy.pub meuvps

# mostra a chave PRIVADA para copiar (inteira, com as linhas BEGIN e END)
cat chave-deploy
```

No GitHub, crie três secrets: `VPS_HOST` (o IP ou domínio), `VPS_USUARIO` (`deploy`) e `VPS_CHAVE_SSH` (o conteúdo **completo** de `chave-deploy`, incluindo as linhas `-----BEGIN OPENSSH PRIVATE KEY-----` e `-----END OPENSSH PRIVATE KEY-----`). Depois apague o arquivo privado da sua máquina: `shred -u chave-deploy`.

> **⚠️ Atenção**
> Quem tem essa chave entra no seu servidor. Limite o estrago antes de precisar: no `~/.ssh/authorized_keys` do VPS, prefixe a linha da chave com `from="140.82.0.0/16",no-agent-forwarding,no-port-forwarding` para restringir a origem, ou crie um usuário `robo` que só pode rodar os comandos do deploy. E, se algum dia o repositório for exposto, revogue a chave apagando a linha do `authorized_keys` — é mais rápido do que trocar tudo.

## 7. Badge e proteção de branch

Um workflow que ninguém olha não protege nada. Duas providências fazem o resultado virar consequência.

**Badge no `README.md`** — a imagem que mostra se o `main` está passando:

```markdown
[![CI](https://github.com/seu-usuario/unieventos-api/actions/workflows/ci.yml/badge.svg)](https://github.com/seu-usuario/unieventos-api/actions/workflows/ci.yml)
```

**Proteção da branch** — em **Settings → Branches → Add branch protection rule** (ou em **Rules → Rulesets**), para `main`:

- [ ] Exigir pull request antes de mesclar (com pelo menos uma aprovação, se você trabalha em dupla).
- [ ] Exigir que verificações de status passem: marque o job **Lint e testes**.
- [ ] Exigir que a branch esteja atualizada com o `main` antes de mesclar.
- [ ] Bloquear `force push` e exclusão da branch.

A partir daí, o botão "Merge pull request" fica cinza enquanto a CI estiver vermelha. É a regra do Capítulo 02 (trabalhar por pull request) ganhando um porteiro que não esquece e não faz exceção para ninguém — nem para você, se marcar "Include administrators".

> **🧠 Você sabia?**
> O GitHub Actions é gratuito e ilimitado para repositórios **públicos**. Para repositórios privados existe uma cota mensal de minutos, e o consumo depende do sistema: um minuto de runner Linux conta como um minuto; Windows conta como dois; macOS conta como dez. É por isso que praticamente toda CI de projeto JavaScript roda em `ubuntu-latest` — e mais um motivo para deixar o repositório do seu projeto autoral público, com o `.env` de fora, claro.

## 8. Boas práticas

| Prática | Por quê | Como |
|---|---|---|
| Menor privilégio | um workflow comprometido faz menos estrago | `permissions:` explícito em cada workflow |
| `concurrency` | evita dois deploys simultâneos e economiza minutos | `group:` por ref, `cancel-in-progress` só na CI |
| `timeout-minutes` | um job travado queima minutos até seis horas | 10 a 20 minutos em cada job |
| Cache de dependências | corta o tempo do `npm ci` | `cache: npm` no `setup-node`; `type=gha` no build da imagem |
| Filtros de caminho | não rodar a CI da API quando só o README mudou | `paths:` e `paths-ignore:` no `on:` |
| Fixar a versão da action | uma action é código de terceiros que roda com os seus segredos | `@v4` no mínimo; em produção, o SHA completo |
| Atualização revisada | actions e imagens envelhecem e ganham falhas | Dependabot com `package-ecosystem: github-actions` |
| Aprovação manual | um humano decide quando o deploy acontece | `environment:` com *required reviewers* |

Exemplo de filtro de caminho, útil em um repositório que guarda front e back juntos:

```yaml
on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - 'package.json'
      - 'package-lock.json'
      - 'Dockerfile'
      - '.github/workflows/deploy.yml'
```

E o Dependabot mantendo as actions atualizadas por pull request (que passa pela sua própria CI antes de ser mesclado):

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly

  - package-ecosystem: npm
    directory: /
    schedule:
      interval: weekly
```

## 🚀 Passo a passo — do `git push` ao ar, sem tocar no servidor

Ao final destes passos, empurrar um commit no `main` da `unieventos-api` vai rodar os testes, construir a imagem, publicá-la no GHCR e atualizar o VPS sozinho — e um pull request que quebra os testes não vai conseguir ser mesclado.

Está no **Nível 2**? Aplique o mesmo passo na `cafe-cerrado-api`: troque o nome do repositório e o da imagem no GHCR, e o resto dos workflows — `ci.yml`, `imagem.yml` e `deploy.yml` — vale linha por linha.

### Passo 1 — a CI antes de tudo

```bash
cd unieventos-api
mkdir -p .github/workflows
```

Crie `.github/workflows/ci.yml` com o conteúdo da §3 (só o job `verificar`, por enquanto). Commite em uma **branch**, não no `main`:

```bash
git switch -c ci-inicial
git add .github/workflows/ci.yml
git commit -m "ci: rodar lint e testes a cada push e pull request"
git push -u origin ci-inicial
gh pr create --fill
```

Abra o pull request no navegador: em segundos aparece a verificação "CI / Lint e testes" rodando. Espere ficar verde.

### Passo 2 — provar que a CI pega erro

Antes de confiar na esteira, quebre-a de propósito. Na mesma branch, edite um teste para esperar o valor errado e empurre:

```bash
git commit -am "test: quebrar um teste de propósito"
git push
```

O PR fica vermelho, com o log mostrando exatamente qual expectativa falhou. **Esse é o momento em que a CI ganha valor.** Desfaça e empurre de novo:

```bash
git revert --no-edit HEAD
git push
```

Mescle o PR quando voltar ao verde.

### Passo 3 — proteger o `main`

Com a CI verde no `main`, aplique a proteção de branch da §7 exigindo o status **Lint e testes**. Teste: crie uma branch com um teste quebrado, abra o PR e confirme que o botão de merge fica bloqueado.

### Passo 4 — segredos do deploy

Gere a chave dedicada (§6.2) e cadastre em **Settings → Secrets and variables → Actions**:

| Nome | Tipo | Conteúdo |
|---|---|---|
| `VPS_HOST` | secret | IP ou domínio do VPS |
| `VPS_USUARIO` | secret | `deploy` |
| `VPS_CHAVE_SSH` | secret | a chave privada inteira |

### Passo 5 — o VPS pronto para receber

No VPS, ajuste o `compose.prod.yaml` para usar `${TAG_IMAGEM:-latest}` (§6.1) e confirme que o deploy manual ainda funciona:

```bash
ssh meuvps
cd /srv/unieventos-api
TAG_IMAGEM=latest docker compose -f compose.prod.yaml up -d
curl -fsS http://127.0.0.1:3000/health
```

Se o pacote no GHCR for privado, faça um `docker login ghcr.io` no VPS com um token de leitura; se for público (Capítulo 07), não precisa de nada.

### Passo 6 — o workflow de deploy

Crie `.github/workflows/deploy.yml` com o conteúdo da §6, abra o PR, espere a CI e mescle. Assim que o merge entra no `main`, abra a aba **Actions**: o job `imagem` leva uns 2 minutos (na primeira vez; depois o cache derruba para menos de 1) e o `implantar` termina em segundos.

```bash
curl -s https://api.seudominio.dev/health
```

### Passo 7 — o site estático

No `unieventos-web`, crie `.github/workflows/publicar-site.yml` (§5), ligue **Settings → Pages → Source: GitHub Actions** e cadastre a variável `VITE_API_URL` com a URL pública da API. Empurre e acompanhe.

### Passo 8 — mudar algo de verdade

Altere uma mensagem visível da API (por exemplo, o texto de erro 404), commite em uma branch, abra o PR, espere o verde, mescle — e **não faça mais nada**. Em três minutos, `curl https://api.seudominio.dev/rota-que-nao-existe` mostra o texto novo.

### Como conferir

1. A aba **Actions** mostra três workflows com execuções verdes.
2. O `README.md` exibe o badge da CI, e ele está verde.
3. Um PR com teste quebrado não pode ser mesclado.
4. **Packages** no GitHub lista a imagem com uma tag `latest` e uma tag por commit.
5. `ssh meuvps 'docker ps --format "{{.Image}}"'` mostra a imagem com o SHA do último commit.
6. Um `TAG_IMAGEM=<sha anterior> docker compose up -d` volta a versão anterior em segundos.

**Resultado esperado:** você não digita mais nenhum comando de deploy. Digita código, abre PR, mescla — e o resto acontece.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Explique a diferença entre `on: push` e `on: pull_request` e diga por que o workflow de deploy usa só o primeiro. O que aconteceria se ele também rodasse em pull requests vindos de forks?

**A2.** Preveja a saída. Um workflow tem dois jobs sem `needs:` entre eles. Eles rodam em sequência ou em paralelo? O job B enxerga um arquivo que o job A criou com `touch relatorio.txt`? Justifique.

**A3.** Por que `npm ci` e não `npm install` na CI? Cite dois comportamentos diferentes entre os dois comandos.

**A4.** Este step está errado: `- run: cd unieventos-api` seguido de `- run: npm test`. Explique por que o segundo step não roda dentro da pasta e escreva a correção.

**A5.** Você precisa guardar a URL pública da API (`https://api.seudominio.dev`) e o token do Netlify. Qual dos dois vai em *secret* e qual em *variable*? Justifique com uma frase.

**A6.** O que o bloco `permissions: contents: read, packages: write` autoriza e o que ele impede? Por que declarar isso é melhor do que deixar o padrão?

### Nível B — Aplicação

**B1.** Adicione ao `ci.yml` um step que roda `npm audit --audit-level=high` e faz o job falhar se houver vulnerabilidade alta ou crítica nas dependências de produção.

Resultado esperado: um PR com uma dependência vulnerável fica vermelho; o log mostra o pacote, a severidade e a versão corrigida.

<details><summary>Dica</summary>

`npm audit --omit=dev --audit-level=high` limita a checagem ao que vai para produção. Se hoje o seu projeto já tem um aviso conhecido e sem correção, `continue-on-error: true` no step deixa o aviso visível sem bloquear a esteira — mas isso é dívida, anote no README.
</details>

**B2.** Faça a CI só rodar quando o código muda. Use `paths-ignore` para ignorar alterações em `README.md`, `docs/**` e `.gitignore`, e prove que funciona com dois commits.

Resultado esperado: um commit que muda só o `README.md` não dispara execução nenhuma na aba Actions; um commit em `src/` dispara.

<details><summary>Dica</summary>

`paths-ignore` fica dentro do `push:` e do `pull_request:`, no mesmo nível de `branches:`. Cuidado: se a proteção de branch exige o status "Lint e testes" e o PR não dispara a CI, o merge trava esperando um status que nunca virá — teste esse cenário e descreva a solução.
</details>

**B3.** Publique um relatório como artefato. Faça o job de testes gerar a saída em arquivo e anexá-la à execução com `actions/upload-artifact@v4`, com retenção de 7 dias.

Resultado esperado: na página da execução, uma seção **Artifacts** com um arquivo baixável contendo a saída dos testes.

<details><summary>Dica</summary>

`npm test -- --reporter=junit --outputFile=relatorio.xml` (Vitest) gera o arquivo. Use `if: always()` no step de upload, senão ele não roda justamente quando você mais precisa: quando o teste falhou.
</details>

**B4.** Meça o ganho do cache. Rode o workflow uma vez com `cache: npm` no `setup-node` e outra sem, e compare a duração do step `npm ci` nos logs.

Resultado esperado: uma tabela no `README.md` com os dois tempos e o percentual de redução.

<details><summary>Dica</summary>

O cache só existe a partir da segunda execução da mesma chave (que vem do `package-lock.json`). Compare a terceira execução com cache contra uma execução em que você removeu a linha `cache: npm` — e repare que o step passa a se chamar "Post Setup Node" quando o cache é salvo.
</details>

### Nível C — Desafio

**C1.** Faça o deploy acontecer **apenas** quando você criar uma tag de versão (`v1.2.0`), e não a cada push no `main`. A imagem precisa ser publicada com a tag da versão (`1.2.0`), com `1.2` e com `latest`, e o VPS precisa subir exatamente a versão criada.

<details><summary>Dica</summary>

No `on:`, troque `branches: [main]` por `tags: ['v*']`. No `docker/metadata-action@v5`, `type=semver,pattern={{version}}` e `type=semver,pattern={{major}}.{{minor}}` geram as tags a partir do nome da tag do Git. No script SSH, `${{ github.ref_name }}` traz `v1.2.0` — decida se a imagem usa o `v` ou não e mantenha a decisão nos dois lados.
</details>

## 🏆 Desafios

### ⭐ A esteira que reprova
Tags: ci-cd, github, testes

Uma CI que nunca ficou vermelha não provou nada — talvez ela não esteja rodando o que você pensa. Comprove que a sua esteira reprova de verdade, nas três formas de errar que mais acontecem, e documente o que cada uma mostra no log.

**Critérios de pronto**

- Três pull requests, cada um com uma falha diferente e proposital: um teste quebrado, um erro de lint e um `package-lock.json` dessincronizado do `package.json`.
- Os três aparecem vermelhos e com o merge bloqueado pela proteção de branch.
- Uma tabela no `README.md` com a mensagem de erro literal de cada caso e a correção.
- Os três PRs são fechados sem mesclar, e o `main` continua verde.

<details><summary>Pistas</summary>

1. Para dessincronizar o lockfile, edite a versão de uma dependência no `package.json` sem rodar `npm install`.
2. Se o erro de lint não reprova, veja se o step do lint está mesmo rodando: `npm run lint --if-present` não falha quando o script não existe.
3. A mensagem literal está no log do step que falhou; a aba **Annotations** da execução traz o resumo.
4. Ao fechar um PR sem mesclar, apague também a branch remota — `gh pr close --delete-branch`.
</details>

### ⭐⭐ Ambiente de revisão para cada pull request
Tags: ci-cd, deploy, github, projeto

Revisar um PR lendo o diff é uma coisa; **abrir o site do PR no navegador** é outra. Faça com que todo pull request do `unieventos-web` publique uma versão temporária e comente no próprio PR o endereço onde ela pode ser vista.

**Critérios de pronto**

- Um workflow disparado por `pull_request` constrói o site e publica uma pré-visualização (deploy preview do Netlify, do Cloudflare Pages ou uma pasta por PR no seu VPS).
- Um comentário automático no PR traz o link, atualizado a cada novo commit em vez de repetido dez vezes.
- A pré-visualização é apagada quando o PR é fechado ou mesclado.
- O workflow não expõe segredo nenhum em PR vindo de fork — descreva no README como você tratou esse caso.

<details><summary>Pistas</summary>

1. `netlify deploy` sem `--prod` já devolve uma URL de pré-visualização; a saída do comando traz o endereço, que você pode capturar para `$GITHUB_OUTPUT`.
2. Para comentar, `gh pr comment ${{ github.event.pull_request.number }} --body "..."` usando o `GITHUB_TOKEN` com `pull-requests: write`.
3. Para não repetir comentários, procure por um marcador oculto no corpo do comentário existente e edite-o em vez de criar outro.
4. O evento `pull_request` com `types: [closed]` é o gancho para a limpeza.
</details>

### ⭐⭐⭐ Banco de verdade em cada pull request
Tags: ci-cd, banco-de-dados, testes, investigacao

Testes com repositório falso não pegam erro de SQL. Faça a CI validar as consultas contra um Postgres real, aplicando as migrations do zero a cada execução — e, de quebra, provar que toda migration nova também **desfaz** o que fez.

**Critérios de pronto**

- Um job de integração sobe o banco (contêiner de serviço ou uma branch efêmera do Neon), roda `npm run migrar` em um banco vazio e executa a suíte contra ele.
- Pelo menos três testes exercitam SQL de verdade: listagem com filtro, inserção com restrição única violada e exclusão em cascata.
- Cada migration tem um par `.desfazer.sql`, e o job aplica todas, desfaz todas e aplica de novo — terminando com o schema idêntico.
- O job roda em menos de 3 minutos e não depende do banco de produção em nenhum momento.

<details><summary>Pistas</summary>

1. O contêiner de serviço da §3.1 já dá o banco; o `--health-cmd` é o que evita a corrida entre o job e o Postgres.
2. Para comparar schemas antes e depois, `pg_dump --schema-only` nos dois momentos e `diff` entre os arquivos.
3. Se optar pelo Neon, uma branch do banco nasce em segundos com uma cópia dos dados; crie-a no início do job e apague no fim, mesmo quando a suíte falha (`if: always()`).
4. Teste em cascata é onde aparecem os erros interessantes: apague um evento com inscrições e confira o que sobrou.
</details>

### 🔥 Boss — A esteira completa, com rollback automático
Tags: ci-cd, docker, deploy, nginx, seguranca

Você tem CI, imagem publicada e deploy por SSH. Falta o que separa um pipeline de aula de um pipeline de produção: **saber que o deploy deu errado e desfazê-lo sozinho**. Monte a esteira completa do UniEventos (front e back), em que um push no `main` entrega tudo no ar — e uma versão quebrada volta atrás sem ninguém acordar.

**Critérios de pronto**

- Um push no `main` da API dispara, em ordem: testes → build da imagem com tag por commit → publicação no GHCR → deploy no VPS → verificação de saúde.
- A verificação de saúde consulta `https://api.seudominio.dev/health` **de fora** do servidor (não só `127.0.0.1`) por até 60 segundos.
- Se a verificação falhar, o próprio workflow refaz o deploy da versão anterior e termina em vermelho, com a versão anterior no ar e funcionando.
- Um push no `main` do front publica o site e invalida o cache, e o site publicado consome a API publicada (sem erro de CORS e sem conteúdo misto, Capítulo 04).
- O `main` é protegido: PR obrigatório, CI verde obrigatória, sem `force push`.
- O `README.md` traz um diagrama em texto da esteira, a lista de secrets necessários (nomes, nunca valores) e o procedimento de rollback manual em 3 linhas.
- Nenhum segredo aparece em log algum; o workflow de deploy não roda em PR de fork.

<details><summary>Pistas</summary>

1. A versão anterior está a um comando de distância: guarde o SHA que estava no ar antes (`docker inspect` no contêiner atual, ou a saída de `git rev-parse HEAD~1`) em uma variável antes de trocar a imagem.
2. `if: failure()` em um step faz dele um step de compensação, que só roda quando algo antes falhou. É o gancho natural do rollback.
3. Para a verificação de fora, um step com `curl --fail --retry 10 --retry-delay 6 --retry-all-errors` no próprio runner testa o caminho inteiro: DNS, nginx, HTTPS e API.
4. Deploy com zero interrupção é outro nível: suba o contêiner novo em outra porta, confira a saúde dele, troque o `proxy_pass` do nginx e só então derrube o antigo. Se for tentar, faça o `nginx -t` antes de cada `reload`.
5. O front e o back estão em repositórios diferentes: `workflow_run` ou `repository_dispatch` permitem que um dispare o outro, se você quiser encadeá-los.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `Invalid workflow file … (Line: 12, Col: 5): Unexpected value 'run'` | indentação errada no YAML (tabulação ou nível trocado) | reindente com 2 espaços; valide com a extensão GitHub Actions do VS Code |
| `npm ci can only install packages when your package.json and package-lock.json … are in sync` | lockfile desatualizado ou não commitado | `npm install` local, commite o `package-lock.json` e empurre |
| `Dependencies lock file is not found in /home/runner/work/…` | `cache: npm` sem lockfile na raiz (monorepo) | aponte `cache-dependency-path:` para o lockfile certo |
| `Error: Process completed with exit code 1` sem mais nada | o comando do `run:` falhou; a causa está nas linhas acima | abra o step no log e leia de baixo para cima até a primeira linha vermelha |
| `Error: Resource not accessible by integration` | `GITHUB_TOKEN` sem a permissão que o step precisa | acrescente a permissão no bloco `permissions:` do workflow |
| `denied: permission_denied: write_package` no push da imagem | falta `packages: write` ou login feito com o usuário errado | `permissions: packages: write` e `username: ${{ github.actor }}` |
| `Error: Get Pages site failed. Please verify that the repository has Pages enabled` | Pages não configurado como origem "GitHub Actions" | Settings → Pages → Source: GitHub Actions |
| `ssh: handshake failed: ssh: unable to authenticate` | chave privada incompleta no secret, ou chave pública não autorizada no VPS | cole a chave inteira (com `BEGIN`/`END`); confira o `authorized_keys` do usuário `deploy` |
| `Error: connect ECONNREFUSED 127.0.0.1:5432` no job | o job começou antes de o contêiner de serviço estar pronto | `options:` com `--health-cmd` e `--health-retries` no serviço |
| Deploy "funciona", mas o servidor continua na versão antiga | `compose` reusou a imagem `latest` já baixada | tag por commit e `docker compose pull` antes do `up -d` |
| `exec /usr/local/bin/docker-entrypoint.sh: exec format error` | imagem construída para outra arquitetura | `platforms: linux/amd64` no `docker/build-push-action@v6` |
| O secret aparece como `***` mas o script falha na autenticação | segredo cadastrado com espaço ou quebra de linha a mais | recadastre colando sem espaços; teste com o tamanho (`echo -n "$TOKEN" \| wc -c`) |
| A CI não roda em um PR aberto de um fork | política do repositório exige aprovação para colaboradores de primeira viagem | aprove a execução no botão da própria página do PR |

## 🏠 Para praticar depois da aula (1 h)

No repositório do seu **projeto autoral**:

1. Crie `.github/workflows/ci.yml` rodando `npm ci`, lint e testes a cada push e pull request, com `cache: npm`, `permissions: contents: read`, `concurrency` e `timeout-minutes`.
2. Proteja o `main`: pull request obrigatório e a verificação da CI como status obrigatório.
3. Adicione o badge da CI na primeira linha do `README.md`.
4. Crie o segundo workflow: publicação automática do front (Pages ou Netlify) **ou** da imagem no GHCR — o que fizer sentido para o seu projeto.
5. Abra um PR com um erro proposital, mostre que ele foi bloqueado, corrija no mesmo PR e mescle.

**Critério de pronto:** a aba **Actions** tem pelo menos quatro execuções (duas vermelhas e duas verdes), o badge está verde, o `main` não aceita push direto e nenhum segredo aparece em log ou no código.

**Guarde no seu repositório:** commit + push, junto com o link de uma execução vermelha e de uma verde.

## ✅ Está no ar quando…

- [ ] `.github/workflows/ci.yml` roda em todo push e PR, com `npm ci`, lint, testes, cache e `permissions` explícito.
- [ ] Um PR com teste quebrado fica vermelho e **não pode** ser mesclado.
- [ ] O badge da CI aparece no `README.md` e reflete o estado do `main`.
- [ ] O site estático é publicado sozinho a partir do `main` (Pages ou Netlify), com a URL da API vindo de uma variável.
- [ ] Cada push no `main` da API publica no GHCR uma imagem com tag `latest` **e** tag com o SHA do commit.
- [ ] O VPS é atualizado por SSH, sem você digitar nada, e o workflow confirma o `/health` antes de terminar.
- [ ] `TAG_IMAGEM=<sha anterior> docker compose -f compose.prod.yaml up -d` devolve a versão anterior ao ar.
- [ ] Nenhum segredo está no repositório; a chave SSH do deploy é dedicada e revogável.
- [ ] Os workflows terminam em menos de 5 minutos do push até o ar.

## 📚 Para aprofundar

- [GitHub Actions — documentação](https://docs.github.com/pt/actions) — comece por "Escrever fluxos de trabalho" e "Entendendo o GitHub Actions".
- [Sintaxe de fluxo de trabalho](https://docs.github.com/pt/actions/reference/workflow-syntax-for-github-actions) — a referência completa de `on`, `jobs`, `steps`, `strategy`, `concurrency` e `permissions`.
- [Contextos e expressões](https://docs.github.com/pt/actions/learn-github-actions/contexts) — o que existe dentro de `${{ github.* }}`, `${{ secrets.* }}` e `${{ matrix.* }}`.
- [Segurança em GitHub Actions](https://docs.github.com/pt/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions) — segredos, permissões do `GITHUB_TOKEN` e riscos de PRs de forks.
- [Contêineres de serviço](https://docs.github.com/pt/actions/using-containerized-services/about-service-containers) — bancos e filas dentro do job, com healthcheck.
- [`actions/setup-node`](https://github.com/actions/setup-node) — opções de `node-version`, `cache` e `cache-dependency-path`.
- [Publicando no GitHub Pages com Actions](https://docs.github.com/pt/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) — a origem "GitHub Actions" e o fluxo de artefato.
- [`docker/build-push-action`](https://github.com/docker/build-push-action) e [`docker/metadata-action`](https://github.com/docker/metadata-action) — cache, plataformas e geração automática de tags.
- [Netlify CLI](https://docs.netlify.com/cli/get-started/) — `deploy`, `--prod` e variáveis de autenticação para uso em CI.

No próximo capítulo a esteira ganha exigência: ESLint e Prettier padronizando o código, cobertura de testes, Lighthouse medindo o site publicado antes e depois, logs estruturados, monitoramento de erros em produção e um aviso quando o site sair do ar.
