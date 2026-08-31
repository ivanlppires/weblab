# Capítulo 07 — Docker para desenvolvedores web

> **Deploy & Ferramentas** · Unidade 3: Infraestrutura, automação e qualidade
> WebLab · UNEMAT — Campus Sinop
> **Tempo estimado:** 2 a 3 h · estudo autônomo, em paralelo à sua trilha

## 🎯 Objetivos de aprendizagem

Ao final deste capítulo você será capaz de:

- Explicar, com suas palavras, o que é um contêiner, em que ele difere de uma máquina virtual e qual problema o Docker resolve no dia a dia de um time.
- Distinguir imagem, contêiner, volume e rede, e usar os comandos básicos (`run`, `ps`, `logs`, `exec`, `stop`, `rm`) para inspecionar e controlar contêineres.
- Escrever um `Dockerfile` correto para uma API Node: imagem pequena, cache de camadas, sem `devDependencies`, sem rodar como root.
- Escrever um `Dockerfile` multi-stage que gera o build de um site Vite e o serve com nginx.
- Orquestrar API + MySQL com `docker compose`, usando volume para persistir dados, healthcheck e `depends_on` para controlar a ordem de subida, e `.env` para configuração.
- Publicar uma imagem no GitHub Container Registry e rodá-la no VPS do Capítulo 06 atrás do nginx.

## 📋 Pré-requisitos

- [ ] `unieventos-api` na forma final da trilha do Nível 3: `src/app.js` + `src/server.js`, configuração validada em `src/config/index.js`, `npm run migrar` aplicando `migrations/*.sql` e `GET /health` respondendo `{ "status": "ok" }`.
- [ ] `unieventos-web` (Vue 3 + Vite) gerando `dist/` com `npm run build`.
- [ ] VPS do Capítulo 06 acessível por SSH — o mesmo servidor, pelo mesmo alias `meuvps` (usuário `deploy`) do `~/.ssh/config` —, com nginx fazendo proxy reverso para `127.0.0.1:3000`.
- [ ] Conta no GitHub (Capítulo 02) — o registro de imagens fica lá.
- [ ] 4 GB de disco livres e permissão de administrador na sua máquina para instalar o Docker.

> No Capítulo 06 você alugou um VPS e subiu a API "na mão": `apt install`, `npm ci`, `pm2 start`. Funcionou — mas repare em quanta coisa ficou "instalada no servidor": versão do Node, versão do MySQL, pacotes do sistema, o usuário que roda o processo. Se amanhã você precisar de um segundo servidor, ou um colega precisar rodar o mesmo ambiente na máquina dele, tudo isso precisa ser refeito, na mesma ordem, sem esquecer nada. Hoje o **mesmo** VPS passa a rodar a API e o MySQL como **contêineres** — idênticos no seu notebook, no do colega e no servidor —, a partir de uma imagem construída na sua máquina e publicada no GitHub. No Capítulo 08 o banco sai do VPS e vai para um serviço gerenciado; no Capítulo 09 o GitHub Actions passa a construir e publicar essa imagem sozinho a cada push.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | O problema, os quatro conceitos (imagem, contêiner, volume, rede), instalação e primeiros comandos |
| 2 | 50 min | `Dockerfile` da API linha a linha, `.dockerignore`, multi-stage para o site Vite + nginx |
| 3 | 50 min | `docker compose` com API + MySQL, publicação no GHCR e execução no VPS |

## 1. O problema que o Docker resolve

A frase mais cara da história do software é "**na minha máquina funciona**". Ela custa caro porque é verdadeira: o código é o mesmo, mas o *ambiente* não é. Alguns exemplos que você provavelmente já viveu na disciplina:

- O colega tem Node 18, você tem Node 22 — e `--env-file` não existe no dele.
- O MySQL do laboratório está em 8.0, o seu em 8.4 — e o plugin de autenticação padrão mudou.
- No VPS o processo roda como `root`; no seu notebook, como o seu usuário — e a permissão de um arquivo é diferente.
- Você instalou um pacote global (`npm install -g`) meses atrás, esqueceu, e o projeto depende dele sem ninguém saber.

Um **contêiner** resolve isso empacotando, junto com o seu código, **tudo de que ele precisa para rodar**: a versão exata do Node, as dependências, os arquivos de configuração, o usuário, até a distribuição Linux mínima por baixo. O pacote (a **imagem**) é construído uma vez e roda igual em qualquer lugar onde exista um Docker — seu notebook, o do colega, o VPS, o servidor de CI.

### Contêiner não é máquina virtual

Uma máquina virtual emula um computador inteiro, com kernel próprio, e leva minutos para subir. Um contêiner é só um **processo comum do Linux**, isolado do resto do sistema por dois recursos do kernel: *namespaces* (o processo enxerga a própria árvore de arquivos, a própria rede, os próprios PIDs) e *cgroups* (limites de CPU e memória). Não há segundo kernel — o contêiner usa o kernel da máquina hospedeira. Por isso ele sobe em milissegundos e consome pouca memória.

```text
   Máquina virtual                       Contêiner
┌─────────────────────┐            ┌─────────────────────┐
│ app  │ app  │ app   │            │ app  │ app  │ app   │
│ libs │ libs │ libs  │            │ libs │ libs │ libs  │
│ SO   │ SO   │ SO    │  ← kernel  ├──────┴──────┴───────┤
├──────┴──────┴───────┤    por VM  │   Docker Engine     │
│     hipervisor      │            ├─────────────────────┤
├─────────────────────┤            │  kernel Linux (um)  │
│  kernel do host     │            ├─────────────────────┤
├─────────────────────┤            │      hardware       │
│      hardware       │            └─────────────────────┘
└─────────────────────┘
```

> **🧠 Você sabia?**
> As tecnologias que o Docker usa — namespaces e cgroups — já existiam no kernel Linux anos antes de o Docker aparecer. A inovação do Docker não foi o isolamento, e sim o **empacotamento**: um formato de imagem em camadas, um arquivo de receita (`Dockerfile`) e um registro público para compartilhar imagens. Ele foi apresentado ao mundo numa palestra-relâmpago de cinco minutos, como projeto interno de uma empresa de hospedagem — e em poucos anos virou o padrão da indústria.

> **🔬 Investigue**
> Depois de instalar o Docker (§3), rode `docker run --rm alpine uname -r` e, em seguida, `uname -r` na sua própria máquina (no Windows, dentro do WSL). Compare. Depois rode `docker run --rm alpine cat /etc/os-release` e `cat /etc/os-release`. O que é igual e o que é diferente? A resposta é a definição prática de contêiner: **mesmo kernel, sistema de arquivos diferente**.

## 2. Imagem, contêiner, volume e rede

Quatro palavras que você vai usar o tempo todo. Vale fixar a diferença agora:

| Conceito | O que é | Analogia |
|---|---|---|
| **Imagem** | pacote imutável, em camadas, com sistema de arquivos + comando inicial | a receita e os ingredientes lacrados |
| **Contêiner** | uma imagem em execução (um processo isolado); pode haver vários da mesma imagem | o bolo assado — cada um independente |
| **Volume** | área de disco gerenciada pelo Docker que sobrevive ao contêiner | a geladeira: o que está nela não some quando o forno desliga |
| **Rede** | rede virtual onde contêineres se enxergam pelo nome | o ramal interno da empresa |

Três consequências práticas dessas definições:

1. **Tudo o que um contêiner grava dentro de si mesmo é descartável.** Ao remover o contêiner, os arquivos somem. Dados que precisam sobreviver (o diretório de dados do MySQL, uploads) vão para um **volume**.
2. **Uma imagem nunca muda.** Para mudar, você constrói outra e dá outra *tag* (`unieventos-api:1.0.1`). Isso é o que permite voltar atrás em um deploy: basta rodar a tag anterior.
3. **Contêineres na mesma rede se resolvem pelo nome.** Dentro de um `docker compose`, a API alcança o banco em `db:3306`, não em `localhost:3306` — `localhost` dentro de um contêiner é o próprio contêiner. Esse detalhe causa o erro mais comum do capítulo (§🐛).

### Camadas e cache

Cada instrução do `Dockerfile` gera uma **camada**. O Docker guarda as camadas em cache e só reconstrói a partir da primeira que mudou. Por isso a ordem das instruções importa: o que muda pouco (instalar dependências) vem antes do que muda a cada commit (copiar o código-fonte). Você vai ver isso em ação na §5.

## 3. Instalando o Docker

Dois produtos, o mesmo motor:

- **Docker Desktop** (Windows e macOS): aplicativo com interface gráfica que traz o Docker Engine dentro de uma máquina virtual Linux leve. No Windows ele usa o **WSL 2** — instale o WSL antes (`wsl --install` em um PowerShell de administrador, reinicie) e marque a integração com a sua distribuição nas configurações do Docker Desktop.
- **Docker Engine** (Linux, inclusive o VPS): só o motor e a linha de comando, sem interface gráfica. É o que vamos usar no servidor.

### Linux (Ubuntu/Debian) e VPS

O script oficial de conveniência configura o repositório da Docker e instala o Engine, a CLI e o plugin do Compose:

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

Por padrão só o `root` fala com o daemon do Docker. Adicione o seu usuário ao grupo `docker` para não precisar de `sudo` a cada comando:

```bash
sudo usermod -aG docker $USER
newgrp docker          # aplica o grupo na sessão atual (ou saia e entre de novo)
docker --version
docker compose version
```

> **⚠️ Atenção**
> Estar no grupo `docker` equivale a ter `root` na máquina — quem pode subir um contêiner pode montar `/` dentro dele. No VPS, só adicione ao grupo o usuário que faz deploy (o `deploy` que você criou no Capítulo 06), nunca crie contas extras "só para testar".

### Confirmando a instalação

```bash
docker run hello-world
```

```text
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.
```

Leia as três primeiras linhas: o Docker não achou a imagem localmente, **baixou** do Docker Hub (o registro público padrão) e só então **rodou** um contêiner a partir dela. É o ciclo que se repete para toda imagem.

## 4. Primeiros comandos

Vamos praticar com uma imagem útil — o nginx — antes de construir a nossa:

```bash
# sobe um contêiner em segundo plano (-d), com nome, mapeando a porta 8080 do host para a 80 do contêiner
docker run -d --name teste-nginx -p 8080:80 nginx:1.28-alpine

# lista os contêineres em execução (com -a, também os parados)
docker ps

# acompanha os logs (Ctrl+C para sair — o contêiner continua rodando)
docker logs -f teste-nginx

# abre um shell DENTRO do contêiner (-i interativo, -t com terminal)
docker exec -it teste-nginx sh
```

Dentro do shell, olhe em volta e saia:

```bash
ls /usr/share/nginx/html     # os arquivos que o nginx está servindo
ps aux                       # só o nginx: um processo por contêiner
exit
```

Abra `http://localhost:8080` no navegador — a página de boas-vindas do nginx vem do contêiner. Agora pare e limpe:

```bash
docker stop teste-nginx      # envia SIGTERM; depois de 10 s, SIGKILL
docker rm teste-nginx        # remove o contêiner (parado)
docker images                # imagens baixadas/construídas, com tamanho
docker rmi nginx:1.28-alpine # remove a imagem, se não quiser mais
```

Os comandos que você vai digitar mais na vida:

| Comando | Faz |
|---|---|
| `docker ps -a` | lista todos os contêineres, inclusive parados (e por que pararam: `Exited (1)`) |
| `docker logs --tail 100 -f nome` | últimas 100 linhas do log e segue |
| `docker exec -it nome sh` | shell dentro do contêiner (imagens Alpine não têm `bash`) |
| `docker inspect nome` | tudo sobre o contêiner em JSON: IP, volumes, variáveis, estado do healthcheck |
| `docker system df` | quanto disco imagens, contêineres e volumes ocupam |
| `docker system prune` | remove contêineres parados, redes sem uso e cache de build |

> **💡 Dica**
> `docker run` **cria e inicia** um contêiner novo a cada vez. Se você rodar duas vezes o mesmo `docker run --name teste-nginx`, a segunda falha com `Conflict. The container name "/teste-nginx" is already in use`. Para voltar a rodar um contêiner parado, use `docker start teste-nginx`.

## 5. Dockerfile de uma API Node

Um `Dockerfile` é a receita da imagem: uma sequência de instruções que o `docker build` executa de cima para baixo. Este é o da `unieventos-api`, completo:

```dockerfile
# unieventos-api/Dockerfile
# 1. Imagem base: Node 22 LTS sobre Alpine Linux (pequena: ~50 MB comprimida)
FROM node:22-alpine

# 2. Metadado que liga a imagem ao repositório no GitHub (aparece no GHCR)
LABEL org.opencontainers.image.source="https://github.com/seu-usuario/unieventos-api"

# 3. Em produção o Express desliga detalhes de depuração e algumas libs ficam mais rápidas
ENV NODE_ENV=production

# 4. Diretório de trabalho dentro da imagem; todas as instruções seguintes rodam aqui
WORKDIR /app

# 5. Copia SÓ os manifestos primeiro: se eles não mudaram, a camada do npm ci vem do cache
COPY package.json package-lock.json ./

# 6. Instala exatamente o que está no lockfile, sem devDependencies (vitest, eslint, supertest)
RUN npm ci --omit=dev

# 7. Agora o código. --chown entrega os arquivos ao usuário "node", que já existe na imagem
COPY --chown=node:node . .

# 8. A partir daqui nada roda como root — se a API for invadida, o invasor não é root
USER node

# 9. Documenta a porta (não abre nada sozinho; quem abre é o -p do run ou o ports: do compose)
EXPOSE 3000

# 10. Comando inicial, na forma exec (array): o node vira o processo principal e recebe sinais
CMD ["node", "src/server.js"]
```

Cada linha tem um motivo:

- **`FROM node:22-alpine`** — a tag fixa a versão maior do Node (22) e a distribuição (Alpine). Sem tag, `node` significa `node:latest`, e "latest" hoje pode ser outra versão amanhã.
- **`COPY package.json package-lock.json` antes de `COPY . .`** — é o truque de cache da §2: mudar um arquivo em `src/` invalida só a camada 7 em diante; a camada 6 (`npm ci`, a mais lenta) continua no cache.
- **`npm ci --omit=dev`** — `ci` instala o que está travado no `package-lock.json` e falha se ele estiver dessincronizado; `--omit=dev` deixa de fora tudo o que só serve para desenvolver e testar. A imagem fica menor e com menos superfície de ataque.
- **`USER node`** — a imagem oficial já traz um usuário sem privilégios chamado `node`. Tudo o que vem depois (inclusive o `CMD`) roda como ele.
- **`CMD ["node", "src/server.js"]`** e não `CMD npm start` — na forma *shell* (string) ou passando pelo npm, o processo principal do contêiner (PID 1) é um shell ou o npm, e o `SIGTERM` que o `docker stop` envia não chega ao Node. Na forma *exec*, o Node é o PID 1.

### Encerramento limpo

Há um detalhe do Linux aqui: o processo de PID 1 **ignora** sinais para os quais não instalou um tratador. Se o Node for PID 1 sem tratar `SIGTERM`, o `docker stop` espera 10 segundos e mata o processo com `SIGKILL` — no meio de uma requisição, se houver uma. Trate o sinal no `src/server.js`:

```js
// src/server.js — trecho: adicione depois do app.listen(...)
function encerrar(sinal) {
  console.log(`${sinal} recebido — parando de aceitar conexões`)
  servidor.close(() => process.exit(0))          // termina as requisições em andamento e sai
  setTimeout(() => process.exit(1), 8000).unref() // se algo travar, sai de qualquer jeito antes do SIGKILL
}

process.on('SIGTERM', () => encerrar('SIGTERM'))
process.on('SIGINT', () => encerrar('SIGINT'))
```

(`servidor` é a constante devolvida por `app.listen`, como no `server.js` da Aula 13 do Nível 3.) Se não quiser mexer no código, `init: true` no compose coloca um mini-supervisor como PID 1 que encaminha os sinais — as duas coisas juntas são o ideal.

### `.dockerignore`

`COPY . .` copia **tudo** que está no diretório do projeto para dentro da imagem — inclusive `node_modules` da sua máquina (pesado e possivelmente compilado para outro sistema), `.git` e, pior, o `.env` com senhas. O `.dockerignore` funciona como o `.gitignore` do build:

```text
node_modules
npm-debug.log
.env
.env.*
!.env.example
serviceAccountKey.json
.git
.github
test
coverage
compose*.yaml
Dockerfile
README.md
```

> **⚠️ Atenção**
> Uma imagem é um arquivo que você vai enviar para um registro. Se o `.env` entrar nela, qualquer pessoa com acesso à imagem tem as suas senhas — mesmo que você "apague" o arquivo em uma camada posterior, a camada anterior continua lá. Configuração entra no contêiner **em tempo de execução** (variáveis de ambiente), nunca em tempo de build.

### Construindo e rodando

```bash
cd unieventos-api
docker build -t unieventos-api:dev .
docker images unieventos-api
```

Repita o `docker build` sem mudar nada: todas as camadas vêm do cache (`CACHED`) e o build termina em um segundo. Edite qualquer arquivo em `src/` e construa de novo: só as camadas 7 a 10 rodam. Esse é o cache funcionando.

Para rodar, a API precisa das variáveis de ambiente e de um MySQL para conectar. Na §7 o compose resolve os dois; por enquanto, aponte para o MySQL da sua máquina:

```bash
docker run --rm --name api-teste -p 3000:3000 \
  --env-file .env \
  -e DB_HOST=host.docker.internal \
  --add-host=host.docker.internal:host-gateway \
  unieventos-api:dev
```

`host.docker.internal` é o nome pelo qual o contêiner alcança a **sua máquina** (no Docker Desktop ele existe sozinho; no Linux, o `--add-host` cria). Em outro terminal, `curl http://localhost:3000/health` deve responder `{"status":"ok"}`.

> **🔎 Por baixo do capô**
> A imagem oficial `node` existe em três sabores: `node:22` (Debian completo, ~1 GB), `node:22-slim` (Debian mínimo, ~200 MB) e `node:22-alpine` (Alpine Linux, ~150 MB com o Node). Alpine usa a biblioteca C `musl` em vez da `glibc`; para código JavaScript puro isso é indiferente, mas módulos nativos (`sharp`, `bcrypt`) às vezes exigem compilação ou a variante `slim`. Se um `npm ci` falhar dentro do Alpine com erro de compilação, troque para `node:22-slim` antes de perder uma tarde.

## 6. Site Vite servido por nginx (multi-stage)

O site tem um problema diferente da API: para **construir** o `dist/` você precisa de Node, npm e todas as `devDependencies`; para **servir** o `dist/`, você precisa só de um servidor de arquivos estáticos. Um build **multi-stage** usa duas imagens base no mesmo `Dockerfile` — a primeira constrói, a segunda serve — e só a segunda vira a imagem final:

```dockerfile
# unieventos-web/Dockerfile
# ---- Estágio 1: construir o site (precisa de Node e de todas as dependências) ----
FROM node:22-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .

# VITE_* é embutida no JavaScript em tempo de BUILD — por isso é um ARG, não uma variável de execução
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

# ---- Estágio 2: servir o resultado (só nginx + arquivos estáticos) ----
FROM nginx:1.28-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

```nginx
# unieventos-web/nginx.conf
server {
  listen 80;
  server_name _;
  root /usr/share/nginx/html;
  index index.html;

  # SPA: qualquer rota que não seja um arquivo real devolve o index.html, e o Vue Router assume
  location / {
    try_files $uri $uri/ /index.html;
  }

  # os arquivos em /assets/ têm hash no nome; podem ficar em cache por muito tempo
  location /assets/ {
    expires 1y;
    add_header Cache-Control "public, immutable";
  }
}
```

```bash
cd unieventos-web
docker build --build-arg VITE_API_URL=https://api.seudominio.dev -t unieventos-web:dev .
docker run -d --rm --name web-teste -p 8080:80 unieventos-web:dev
docker images unieventos-web
```

A imagem final tem uns 50 MB — o Node, o npm e os 300 MB de `node_modules` ficaram no estágio `build`, que é descartado. Abra `http://localhost:8080`, navegue até uma rota interna (`/eventos/1`) e dê F5: o `try_files` garante que o nginx devolva o `index.html` em vez de 404.

> **💡 Dica**
> Mudar `VITE_API_URL` exige **reconstruir** a imagem — o valor foi substituído dentro do JavaScript pelo Vite. É a mesma regra que você viu ao publicar o front na Aula 15 do Nível 3: variável `VITE_*` é de build, não de execução.

## 7. `docker compose`: API + MySQL

Subir dois contêineres na mão, com rede, volume, variáveis e ordem certa, é chato e propenso a erro. O **Compose** descreve tudo isso em um arquivo YAML e sobe (ou derruba) o conjunto com um comando.

### `compose.yaml` completo

```yaml
# unieventos-api/compose.yaml — ambiente de desenvolvimento: API + MySQL
services:
  api:
    build: .                                   # constrói a partir do Dockerfile desta pasta
    image: ghcr.io/seu-usuario/unieventos-api:dev
    ports:
      - "3000:3000"
    env_file: .env                             # todas as variáveis do .env entram no contêiner
    environment:
      DB_HOST: db                              # sobrescreve o .env: aqui o MySQL se chama "db"
      DB_PORT: 3306
    depends_on:
      db:
        condition: service_healthy             # só sobe quando o healthcheck do banco passar
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://127.0.0.1:3000/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 15s
    init: true                                 # PID 1 minimalista que encaminha sinais ao node
    restart: unless-stopped                    # volta sozinho depois de um reboot do host

  db:
    image: mysql:8.4
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
      MYSQL_DATABASE: ${DB_NAME}
      MYSQL_USER: ${DB_USER}
      MYSQL_PASSWORD: ${DB_PASSWORD}
    ports:
      - "127.0.0.1:3306:3306"                  # só a sua máquina alcança; útil para o Workbench/DBeaver
    volumes:
      - dados-mysql:/var/lib/mysql             # os dados sobrevivem a down/up e a novas imagens
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "127.0.0.1", "--silent"]
      interval: 10s
      timeout: 5s
      retries: 10
      start_period: 30s
    restart: unless-stopped

volumes:
  dados-mysql:
```

```text
# unieventos-api/.env — nunca commitado; copie de .env.example
NODE_ENV=production
PORT=3000

DB_HOST=localhost
DB_PORT=3306
DB_USER=unieventos
DB_PASSWORD=troque-esta-senha
DB_ROOT_PASSWORD=troque-esta-tambem
DB_NAME=unieventos

FIREBASE_PROJECT_ID=unieventos-xxxxx
FIREBASE_SERVICE_ACCOUNT_BASE64=cole-aqui-o-json-em-base64

CORS_ORIGEM_PERMITIDA=http://localhost:5173
```

O que cada parte faz:

- **`${DB_NAME}` no YAML** — o Compose lê o `.env` do diretório e substitui as variáveis no próprio arquivo. Assim a senha do MySQL e a senha que a API usa são **a mesma variável**, sem duplicar.
- **`env_file` + `environment`** — `env_file` injeta todo o `.env` no contêiner da API; `environment` sobrescreve o que precisa ser diferente dentro da rede do Compose (`DB_HOST=db`).
- **`MYSQL_USER`/`MYSQL_PASSWORD`** — a imagem oficial cria esse usuário com acesso total ao `MYSQL_DATABASE`. É por isso que `DB_USER` **não pode ser `root`**: a imagem se recusa a usar essas variáveis para o root (o erro exato está na §🐛).
- **`healthcheck` + `depends_on: condition: service_healthy`** — sem isso a API sobe antes de o MySQL aceitar conexões e morre com `ECONNREFUSED`. O `mysqladmin ping` em `127.0.0.1` força uma conexão TCP, que só funciona quando o servidor definitivo está de pé (durante a inicialização o MySQL sobe um servidor temporário só por socket).
- **`volumes: dados-mysql`** — um volume nomeado. `docker compose down` mantém; `docker compose down -v` apaga.
- **`restart: unless-stopped`** — o Docker reinicia o contêiner se ele cair e depois de um reboot, a menos que você o tenha parado de propósito.

### Os comandos do dia a dia

```bash
docker compose up -d --build     # constrói a imagem da API (se mudou) e sobe tudo em segundo plano
docker compose ps                # estado de cada serviço, inclusive o healthcheck
docker compose logs -f api       # logs só da API (sem o nome: de todos)
docker compose run --rm api npm run migrar   # comando avulso em um contêiner descartável
docker compose exec db mysql -u root -p unieventos   # cliente MySQL dentro do contêiner do banco
docker compose restart api       # reinicia só a API
docker compose down              # para e remove contêineres e rede; volumes ficam
docker compose down -v           # idem, e APAGA os volumes (os dados do banco)
```

> **⚠️ Atenção**
> `docker compose down -v` apaga o banco inteiro sem perguntar. Antes de rodar em qualquer máquina que não seja de desenvolvimento, faça um `mysqldump` (Capítulo 08). No VPS, prefira nunca usar `-v`.

### Variáveis: quem vence quem

Quando a mesma variável aparece em mais de um lugar, o Compose aplica esta ordem, da menor para a maior prioridade: valor dentro do `Dockerfile` (`ENV`) → `env_file` → `environment` → `-e` na linha de comando. É por isso que `DB_HOST=localhost` no `.env` (bom para rodar a API fora do Docker) não atrapalha o `DB_HOST: db` do `environment`.

## 8. Publicando a imagem no GitHub Container Registry

Construir a imagem no VPS funciona, mas gasta CPU e memória de um servidor pequeno e exige o código-fonte lá. O fluxo profissional é: construir **uma** vez (na sua máquina ou, no Capítulo 09, no CI), enviar para um **registro**, e o servidor só **baixa**. O GitHub oferece um registro gratuito para repositórios públicos: o **GHCR** (`ghcr.io`).

### Token e login

Crie um token clássico em **Settings → Developer settings → Personal access tokens → Tokens (classic)**, com os escopos `write:packages` e `read:packages`. Guarde-o em uma variável de ambiente do terminal (nunca em arquivo do projeto) e faça login:

```bash
export GHCR_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
echo "$GHCR_TOKEN" | docker login ghcr.io -u seu-usuario --password-stdin
```

### Nome, tag e push

No GHCR o nome da imagem é `ghcr.io/<usuário>/<imagem>:<tag>`, **tudo em minúsculas**:

```bash
docker build -t ghcr.io/seu-usuario/unieventos-api:1.0.0 .
docker tag ghcr.io/seu-usuario/unieventos-api:1.0.0 ghcr.io/seu-usuario/unieventos-api:latest
docker push ghcr.io/seu-usuario/unieventos-api:1.0.0
docker push ghcr.io/seu-usuario/unieventos-api:latest
```

A imagem aparece em **Packages** no seu perfil. Por padrão ela é **privada**: para o VPS baixá-la sem login, abra a página do pacote → **Package settings → Change visibility → Public**. O `LABEL org.opencontainers.image.source` que você colocou no `Dockerfile` faz o pacote aparecer também na página do repositório.

> **⚠️ Atenção**
> Se você usa um Mac com chip Apple (ARM), a imagem construída com `docker build` é `linux/arm64` — e o VPS é `linux/amd64`. O `pull` até funciona, mas o contêiner morre com `exec format error`. Construa para a arquitetura do servidor: `docker buildx build --platform linux/amd64 -t ghcr.io/seu-usuario/unieventos-api:1.0.0 --push .`

## 9. Boas práticas

Um resumo do que separa um `Dockerfile` de tutorial de um `Dockerfile` de produção:

| Prática | Por quê | Como |
|---|---|---|
| Não rodar como root | invasão do processo não vira invasão do host | `USER node`; `COPY --chown` |
| Imagem pequena | menos download, menos vulnerabilidades, deploy mais rápido | `-alpine`, `--omit=dev`, multi-stage, `.dockerignore` |
| Tags fixas | reprodutibilidade: o mesmo build hoje e daqui a um ano | `node:22-alpine`, `mysql:8.4`, nunca `latest` em produção |
| Configuração por ambiente | a mesma imagem serve dev, teste e produção | variáveis de ambiente, nunca `.env` dentro da imagem |
| Um processo por contêiner | logs, reinício e escala independentes | API em um, banco em outro, nginx em outro |
| Logs no stdout | `docker logs` e o Capítulo 10 dependem disso | `console.log`/pino sem arquivo |
| Healthcheck | orquestrador sabe se o serviço está vivo, não só se o processo existe | `HEALTHCHECK` ou `healthcheck:` no compose |
| Dados em volume | contêiner é descartável; dados não | `volumes:` para `/var/lib/mysql`, uploads |

> **🔎 Por baixo do capô**
> Uma tag como `node:22-alpine` é um **ponteiro móvel**: aponta para a última 22.x.y publicada. Para congelar de verdade, use o *digest*: `FROM node:22-alpine@sha256:…` (o valor aparece em `docker images --digests`). Em projetos grandes é comum um bot (Dependabot, Renovate) abrir pull requests atualizando esse digest — assim a atualização é uma decisão revisada, não uma surpresa no próximo build.

## 🚀 Passo a passo — UniEventos API + MySQL com `docker compose`, local e no VPS

Ao final destes passos a `unieventos-api` estará rodando em contêiner na sua máquina **e** no VPS do Capítulo 06, a partir da mesma imagem publicada no GHCR, com o MySQL também em contêiner e os dados em volume.

### Passo 1 — `Dockerfile`, `.dockerignore` e encerramento limpo

Crie `Dockerfile` e `.dockerignore` na raiz de `unieventos-api` com o conteúdo da §5 (troque `seu-usuario` no `LABEL`) e adicione o tratamento de `SIGTERM` ao `src/server.js`. Construa uma vez para validar:

```bash
cd unieventos-api
docker build -t unieventos-api:dev .
```

Se o build falhar em `npm ci`, o `package-lock.json` está dessincronizado do `package.json`: rode `npm install` fora do Docker, commite o lockfile e tente de novo.

### Passo 2 — `compose.yaml` e `.env`

Crie `compose.yaml` com o conteúdo da §7. Atualize o `.env` com `DB_USER=unieventos`, `DB_PASSWORD`, `DB_ROOT_PASSWORD` e `DB_NAME=unieventos`; espelhe as chaves (sem valores) no `.env.example`. Confirme que `.env` está no `.gitignore` **e** no `.dockerignore`.

### Passo 3 — subir tudo local

```bash
docker compose up -d --build
docker compose ps
```

Espere a coluna `STATUS` do `db` mostrar `healthy` (até 30 s na primeira vez, porque o MySQL inicializa o diretório de dados). A API só sobe depois disso. Aplique as migrations e confira:

```bash
docker compose run --rm api npm run migrar
docker compose logs -f api
```

Em outro terminal:

```bash
curl http://localhost:3000/health
curl http://localhost:3000/api/eventos
```

### Passo 4 — provar que os dados persistem

```bash
docker compose down
docker compose up -d
curl http://localhost:3000/api/eventos
```

Os eventos continuam lá: o diretório `/var/lib/mysql` está no volume `dados-mysql`, não no contêiner. Confira com `docker volume ls`.

### Passo 5 — publicar a imagem

```bash
echo "$GHCR_TOKEN" | docker login ghcr.io -u seu-usuario --password-stdin
docker build -t ghcr.io/seu-usuario/unieventos-api:1.0.0 .
docker push ghcr.io/seu-usuario/unieventos-api:1.0.0
```

(No Mac ARM, use o `docker buildx build --platform linux/amd64 --push` da §8.) Torne o pacote público na página do pacote no GitHub.

### Passo 6 — preparar o VPS

É **o mesmo VPS do Capítulo 06** — o alias `meuvps` do seu `~/.ssh/config`, que entra como usuário `deploy`. Não crie máquina nova: o nginx, o firewall e o certificado que você configurou lá continuam valendo, e o domínio `seudominio.dev` é o mesmo do Capítulo 04. Instale o Docker (§3) e libere o usuário `deploy`:

```bash
ssh meuvps
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
```

Pare a versão em pm2 do Capítulo 06 — a API e o MySQL do sistema vão ser substituídos pelos contêineres:

```bash
pm2 stop unieventos-api
pm2 delete unieventos-api
pm2 save
sudo systemctl stop mysql
sudo systemctl disable mysql
```

(Se você tinha dados no MySQL do VPS, exporte antes com `mysqldump -u root -p unieventos > unieventos-backup.sql` — o Capítulo 08 mostra como importar.)

### Passo 7 — `compose.prod.yaml` no VPS

Crie `/srv/unieventos-api/compose.prod.yaml`. A diferença para o arquivo de desenvolvimento: usa a **imagem publicada** em vez de `build:`, expõe a API só em `127.0.0.1` (o nginx é quem fala com o mundo) e não expõe o MySQL:

```yaml
# /srv/unieventos-api/compose.prod.yaml
services:
  api:
    image: ghcr.io/seu-usuario/unieventos-api:1.0.0
    ports:
      - "127.0.0.1:3000:3000"
    env_file: .env
    environment:
      DB_HOST: db
      DB_PORT: 3306
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://127.0.0.1:3000/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 15s
    init: true
    restart: unless-stopped

  db:
    image: mysql:8.4
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
      MYSQL_DATABASE: ${DB_NAME}
      MYSQL_USER: ${DB_USER}
      MYSQL_PASSWORD: ${DB_PASSWORD}
    volumes:
      - dados-mysql:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "127.0.0.1", "--silent"]
      interval: 10s
      timeout: 5s
      retries: 10
      start_period: 30s
    restart: unless-stopped

volumes:
  dados-mysql:
```

Crie o `.env` de produção ao lado (com senhas **diferentes** das de desenvolvimento e `CORS_ORIGEM_PERMITIDA` apontando para o domínio do site), com permissão restrita:

```bash
# /srv pertence ao root: sem o sudo, o mkdir responde "Permission denied".
sudo mkdir -p /srv/unieventos-api
sudo chown deploy:deploy /srv/unieventos-api
cd /srv/unieventos-api
nano .env
chmod 600 .env
```

> **⚠️ Atenção**
> O Docker manipula o firewall do kernel diretamente e **passa por cima do `ufw`** que você configurou no Capítulo 06: um `ports: - "3000:3000"` abre a porta 3000 para a internet inteira, mesmo com `ufw deny 3000`. Por isso o `compose.prod.yaml` usa `"127.0.0.1:3000:3000"` — só processos do próprio VPS (o nginx) alcançam a API — e não publica porta nenhuma do MySQL.

### Passo 8 — subir no VPS

```bash
docker compose -f compose.prod.yaml pull
docker compose -f compose.prod.yaml up -d
docker compose -f compose.prod.yaml ps
docker compose -f compose.prod.yaml run --rm api npm run migrar
```

Se você exportou dados no Passo 6, importe agora:

```bash
# O compose lê o .env sozinho; o seu shell, não. Carregue-o antes,
# senão o -p fica sem valor, vira prompt e a senha sai da primeira linha do .sql.
set -a; . ./.env; set +a
docker compose -f compose.prod.yaml exec -T db \
  mysql -u root -p"$DB_ROOT_PASSWORD" unieventos < unieventos-backup.sql
```

O nginx do Capítulo 06 continua fazendo proxy para `127.0.0.1:3000` — não precisa mudar nada nele.

### Como conferir

1. No VPS: `docker compose -f compose.prod.yaml ps` mostra `api` e `db` com `healthy`.
2. Da sua máquina: `curl https://api.seudominio.dev/health` responde `{"status":"ok"}` e `curl https://api.seudominio.dev/api/eventos` devolve a lista.
3. `docker compose -f compose.prod.yaml logs --tail 20 api` mostra as requisições que você acabou de fazer.
4. Reinicie o VPS (`sudo reboot`), espere um minuto e repita o item 2 — `restart: unless-stopped` trouxe os dois contêineres de volta sem você fazer nada.

**Resultado esperado:** a mesma imagem `ghcr.io/seu-usuario/unieventos-api:1.0.0` rodando no seu notebook e no VPS, com o `unieventos-web` publicado apontando para `https://api.seudominio.dev` e funcionando de ponta a ponta.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Explique a diferença entre imagem e contêiner em duas frases. Depois responda: se você rodar `docker run -d nginx:1.28-alpine` três vezes, quantas imagens e quantos contêineres existem?

**A2.** Preveja a saída. Você roda `docker run -d --name a nginx:1.28-alpine`, depois `docker stop a`, depois `docker ps`. O contêiner `a` aparece? E em `docker ps -a`? O que aparece na coluna `STATUS`?

**A3.** Um colega diz: "rodei `docker compose down -v` e o banco sumiu, o Docker perdeu meus dados". Explique o que aconteceu e qual comando ele deveria ter usado.

**A4.** Reordene estas instruções de `Dockerfile` para aproveitar o cache ao máximo e justifique: `COPY . .`, `RUN npm ci --omit=dev`, `FROM node:22-alpine`, `COPY package*.json ./`, `WORKDIR /app`, `CMD ["node","src/server.js"]`.

**A5.** Dentro do contêiner da API, `DB_HOST=localhost` falha e `DB_HOST=db` funciona. Explique o que `localhost` significa dentro de um contêiner e de onde vem o nome `db`.

### Nível B — Aplicação

**B1.** Adicione ao `compose.yaml` um terceiro serviço, `adminer` (imagem oficial `adminer`, porta `8080:8080`, variável `ADMINER_DEFAULT_SERVER=db`), e use-o para navegar nas tabelas do UniEventos pelo navegador.

Resultado esperado: `http://localhost:8080` mostra a tela de login do Adminer; com servidor `db`, usuário e senha do `.env`, você vê as tabelas `eventos`, `inscricoes` e `migrations_executadas`.

<details><summary>Dica</summary>

O Adminer está na mesma rede do Compose, então o "servidor" no formulário é o nome do serviço (`db`), não `localhost`. Não é preciso `depends_on` — ele só conecta quando você preenche o formulário.
</details>

**B2.** Faça um backup do volume `dados-mysql` sem parar o banco, usando um contêiner descartável que monta o volume e compacta o conteúdo em um `.tgz` na sua pasta atual.

Resultado esperado: um arquivo `dados-mysql.tgz` de alguns MB no diretório do projeto; `tar tzf dados-mysql.tgz | head` lista arquivos do MySQL.

<details><summary>Dica</summary>

`docker volume ls` mostra o nome real do volume (o Compose prefixa com o nome da pasta: `unieventos-api_dados-mysql`). O comando tem a forma `docker run --rm -v NOME_DO_VOLUME:/dados -v "$PWD":/backup alpine tar czf /backup/dados-mysql.tgz -C /dados .`. Para um backup consistente de verdade, prefira o `mysqldump` do Capítulo 08 — este exercício é sobre volumes.
</details>

**B3.** Derrube o MySQL de propósito (`docker compose stop db`) com a API rodando, faça uma requisição a `/api/eventos` e observe o log da API. Depois suba o banco de novo e repita a requisição.

Resultado esperado: com o banco parado, a API responde `500` (ou `503`, se o seu tratador de erros distingue) e o log mostra o erro de conexão; com o banco de volta, a requisição funciona **sem reiniciar a API** — o pool do `mysql2` reconecta sozinho.

<details><summary>Dica</summary>

`docker compose logs -f api` em um terminal, `curl -i http://localhost:3000/api/eventos` em outro. Se a API morreu junto com o banco, procure um `process.exit` ou uma exceção não tratada no seu código de conexão.
</details>

**B4.** Descubra quanto a imagem da API pesa e quanto pesaria sem `--omit=dev` e sem Alpine. Construa três variantes (`node:22-alpine` com `--omit=dev`, `node:22-alpine` sem `--omit=dev`, `node:22` com `--omit=dev`) com tags diferentes e compare em `docker images`.

Resultado esperado: uma tabela com os três tamanhos, a variante Alpine + `--omit=dev` sendo a menor por larga margem.

<details><summary>Dica</summary>

Use `docker build -f` com Dockerfiles alternativos (`Dockerfile.debian`, `Dockerfile.dev`) ou passe `--build-arg`. `docker history nome:tag` mostra o tamanho de cada camada — a do `npm ci` é a que muda.
</details>

### Nível C — Desafio

**C1.** Faça a API recarregar sozinha dentro do contêiner quando você edita um arquivo em `src/`, sem reconstruir a imagem. Crie um `compose.override.yaml` (o Compose o mescla automaticamente com `compose.yaml`) que monte a pasta do projeto dentro do contêiner e troque o comando por `node --watch src/server.js`.

<details><summary>Dica</summary>

Três problemas para resolver, nesta ordem: (1) o `node_modules` da sua máquina não deve sobrescrever o do contêiner — monte um volume anônimo em `/app/node_modules`; (2) `--watch` precisa das `devDependencies`? Não, mas o `vitest` sim — se quiser rodar testes dentro do contêiner, o override precisa de uma imagem construída sem `--omit=dev` (use um `target` ou um `Dockerfile.dev`); (3) `NODE_ENV=production` desliga coisas úteis em desenvolvimento — sobrescreva no override.
</details>

## 🏆 Desafios

### ⭐ Imagem abaixo de 150 MB
Tags: docker, performance, investigacao

A imagem da API construída no Passo a passo pesa quanto? `docker images ghcr.io/seu-usuario/unieventos-api` responde. Se passou de 150 MB, algo desnecessário entrou: `devDependencies`, cache do npm, arquivos que o `.dockerignore` deveria barrar. Reduza-a até ficar abaixo de 150 MB **sem quebrar** o `/health` nem o `npm run migrar`.

**Critérios de pronto**

- `docker images` mostra a imagem final com menos de 150 MB.
- `docker compose up -d` com a imagem reduzida sobe, passa no healthcheck e `GET /api/eventos` responde.
- `docker history` da imagem não mostra nenhuma camada com `node_modules` de desenvolvimento.
- Um parágrafo no `README.md` registra o tamanho antes e depois e o que foi removido.

<details><summary>Pistas</summary>

1. `docker history --no-trunc nome:tag` mostra o tamanho de cada camada; comece pela maior.
2. O `npm ci` deixa um cache em `~/.npm` dentro da imagem; `npm cache clean --force` na mesma instrução `RUN` (encadeada com `&&`) evita que ele vire camada.
3. Confira se `test/`, `coverage/`, `.git/` e `docs/` estão no `.dockerignore` — `docker build` mostra o tamanho do contexto enviado na primeira linha.
4. Se ainda estiver acima, compare `node:22-alpine` com `node:22-slim` — e verifique quais dependências de produção são realmente necessárias.
</details>

### ⭐⭐ Café Cerrado em contêiner
Tags: docker, express, projeto

A `cafe-cerrado-api` do Nível 2 é mais simples que a do UniEventos: um Express 5 que serve a pasta `public/` e expõe `/api/produtos`, gravando em um arquivo JSON. Justamente por gravar em arquivo ela tem um problema que a `unieventos-api` não tem: se o JSON ficar dentro do contêiner, cada `docker compose up` de uma imagem nova zera o cardápio. Empacote-a de forma que os dados sobrevivam.

**Critérios de pronto**

- `Dockerfile` com `node:22-alpine`, `npm ci --omit=dev`, `USER node` e forma exec no `CMD`.
- `compose.yaml` com um volume nomeado montado exatamente na pasta onde o JSON é gravado, e nada mais.
- Criar um produto pela API, rodar `docker compose down && docker compose up -d` e o produto continuar lá.
- O usuário `node` consegue **escrever** no diretório do volume (o erro `EACCES` é o obstáculo esperado).

<details><summary>Pistas</summary>

1. Descubra o caminho absoluto em que a API grava o JSON dentro do contêiner (`WORKDIR` + caminho relativo).
2. Um volume nomeado novo é criado como `root`. Ou você cria o diretório e faz `chown node:node` no `Dockerfile` **antes** de declarar o `VOLUME`, ou monta com `user: "1000:1000"` no compose.
3. Se a API lê o arquivo de exemplo do repositório na primeira execução, ela precisa copiá-lo para o volume quando o volume estiver vazio — ou o `Dockerfile` copia o JSON inicial para o diretório antes de o volume ser montado (o Docker copia o conteúdo pré-existente do diretório para um volume nomeado vazio na primeira montagem).
4. Teste o cenário de "imagem nova": mude qualquer coisa no código, `up -d --build`, e confira que o produto criado continua.
</details>

### ⭐⭐⭐ Três contêineres, um comando, zero CORS
Tags: docker, nginx, vue, express

Hoje o site chama a API em outra origem e o CORS precisa liberar o domínio do front. Se o **mesmo** nginx que serve o site fizer proxy de `/api/` para a API, front e back passam a ter a mesma origem — e o CORS deixa de existir. Monte um `compose.yaml` com três serviços — `web` (imagem multi-stage da §6), `api` e `db` — em que `docker compose up -d --build` sobe o UniEventos completo em `http://localhost:8080`, e nenhuma requisição do navegador sai para outra porta.

**Critérios de pronto**

- `docker compose up -d --build` na raiz de um repositório que contém `unieventos-web/` e `unieventos-api/` sobe os três serviços.
- `http://localhost:8080` abre o site; a aba Rede do DevTools mostra `GET http://localhost:8080/api/eventos` (mesma origem).
- O site foi construído com `VITE_API_URL` vazio ou igual à própria origem, e o `nginx.conf` do `web` tem um `location /api/` fazendo proxy para `http://api:3000`.
- A porta 3000 **não** está publicada no host — só o `web` alcança a API.
- O `README.md` explica em até 10 linhas por que o CORS deixou de ser necessário.

<details><summary>Pistas</summary>

1. `docker compose` aceita `build: context: ./unieventos-api` para construir a partir de subpastas; o `Dockerfile` do `web` precisa de `args: VITE_API_URL: ""` na seção `build:`.
2. No nginx, `location /api/ { proxy_pass http://api:3000; }` — atenção à barra final em `proxy_pass`: com ou sem ela o caminho repassado muda. Teste as duas formas e observe o log da API.
3. O nginx resolve o nome `api` na hora de subir; se a API ainda não existir, ele falha com `host not found in upstream`. `depends_on` resolve a ordem.
4. O `helmet` da API pode enviar cabeçalhos que conflitam com os do nginx (`X-Frame-Options`, CSP). Se o site quebrar, olhe os cabeçalhos da resposta antes de mexer no código.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock` | seu usuário não está no grupo `docker` (ou a sessão não foi reaberta depois do `usermod`) | `sudo usermod -aG docker $USER` e `newgrp docker`, ou saia e entre de novo |
| `Error: connect ECONNREFUSED 127.0.0.1:3306` no log da API dentro do contêiner | `DB_HOST=localhost` — dentro do contêiner, `localhost` é o próprio contêiner, e lá não há MySQL | `DB_HOST=db` (nome do serviço no compose) via `environment:` |
| `dependency failed to start: container unieventos-api-db-1 is unhealthy` | o healthcheck do MySQL não passou no tempo previsto (primeira inicialização lenta, senha do root ausente) | `docker compose logs db`; aumente `start_period`; confira `MYSQL_ROOT_PASSWORD` no `.env` |
| `MYSQL_USER="root", MYSQL_USER and MYSQL_PASSWORD are for configuring a regular user and cannot be used for the root user` | `.env` com `DB_USER=root` | use um usuário dedicado (`DB_USER=unieventos`) e `DB_ROOT_PASSWORD` separado |
| `Bind for 0.0.0.0:3306 failed: port is already allocated` | um MySQL nativo (ou outro contêiner) já ocupa a porta na sua máquina | pare o serviço nativo (`sudo systemctl stop mysql`) ou mapeie `"127.0.0.1:3307:3306"` |
| `invalid reference format: repository name must be lowercase` | usuário do GitHub com maiúsculas no nome da imagem | `ghcr.io/seu-usuario/unieventos-api` tudo em minúsculas |
| `exec /usr/local/bin/docker-entrypoint.sh: exec format error` no VPS | imagem construída em Mac ARM (`linux/arm64`) rodando em servidor `linux/amd64` | `docker buildx build --platform linux/amd64 --push` |
| `denied: permission_denied: write_package` no `docker push` | token sem o escopo `write:packages`, ou login feito em outro usuário | gere um token clássico com `write:packages` e refaça o `docker login ghcr.io` |
| `EACCES: permission denied, open '/app/dados/produtos.json'` | processo roda como `node`, mas o diretório pertence ao `root` | `COPY --chown=node:node` e/ou `RUN mkdir -p /app/dados && chown node:node /app/dados` antes do `USER node` |
| Mudei o `.sql` de inicialização e o banco não mudou | scripts em `/docker-entrypoint-initdb.d` só rodam na **primeira** inicialização, com o volume vazio | aplique a mudança como migration (`npm run migrar`) ou, em desenvolvimento, `docker compose down -v` |
| `docker stop` demora 10 s e a API "morre" em vez de encerrar | Node como PID 1 sem tratador de `SIGTERM` ignora o sinal | `process.on('SIGTERM')` no `server.js` e `init: true` no compose |
| A porta 3000 do VPS está aberta para a internet apesar do `ufw` | o Docker escreve regras de firewall próprias, antes das do `ufw` | publique como `"127.0.0.1:3000:3000"` e deixe o nginx ser a única porta de entrada |

## 🏠 Para praticar depois da aula (1 h)

No repositório da API do seu **projeto autoral**:

1. Escreva `Dockerfile` e `.dockerignore` seguindo a §5 (imagem `node:22-alpine`, `npm ci --omit=dev`, `USER node`, forma exec no `CMD`, `LABEL` apontando para o seu repositório).
2. Escreva `compose.yaml` com a API e o banco (MySQL 8.4 ou Postgres, conforme o seu projeto), volume nomeado, healthcheck e `depends_on` com `condition: service_healthy`.
3. Atualize `.env.example` com todas as variáveis que o compose precisa e adicione ao `README.md` uma seção **"Rodando com Docker"** de no máximo 10 linhas: clonar, copiar `.env.example` para `.env`, `docker compose up -d --build`, migrar, testar `/health`.
4. Publique a imagem no GHCR com a tag `1.0.0` e torne o pacote público.

**Critério de pronto:** um colega (ou você, em outra pasta) consegue clonar o repositório, seguir só o `README.md` e ter `curl http://localhost:3000/health` respondendo `{"status":"ok"}` — sem instalar Node nem banco na máquina. O `.env` não está no repositório nem na imagem (`docker run --rm sua-imagem cat .env` deve falhar).

**Guarde no seu repositório:** commit + push, junto com o link do pacote no GHCR.

## ✅ Está no ar quando…

- [ ] `docker run hello-world` funciona sem `sudo` na sua máquina e no VPS.
- [ ] `Dockerfile` da API constrói sem erro; `docker images` mostra a imagem abaixo de 200 MB; `docker history` não mostra `.env` nem `node_modules` de desenvolvimento.
- [ ] `.dockerignore` barra `node_modules`, `.env`, `.git` e o JSON da conta de serviço do Firebase.
- [ ] `docker compose up -d --build` sobe API + MySQL; `docker compose ps` mostra os dois `healthy`.
- [ ] `docker compose down` seguido de `up -d` preserva os dados (volume nomeado).
- [ ] Imagem publicada em `ghcr.io/seu-usuario/unieventos-api:1.0.0`, pacote público.
- [ ] No VPS, `compose.prod.yaml` roda a imagem do GHCR com a API em `127.0.0.1:3000` e sem porta do MySQL publicada.
- [ ] `https://api.seudominio.dev/health` responde `{"status":"ok"}` depois de um `sudo reboot` do VPS, sem intervenção.
- [ ] `Dockerfile` multi-stage do `unieventos-web` gera uma imagem nginx de ~50 MB que serve o site com fallback para `index.html`.

## 📚 Para aprofundar

- [Docker — Get started](https://docs.docker.com/get-started/) — o guia oficial; leia "What is a container?" e "Build and push your first image".
- [Docker Compose — documentação](https://docs.docker.com/compose/) — em especial a referência do arquivo Compose (`services`, `volumes`, `healthcheck`, `depends_on`).
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/) — cada instrução, com as diferenças entre forma shell e forma exec.
- [Best practices for writing Dockerfiles](https://docs.docker.com/build/building/best-practices/) — multi-stage, cache, `.dockerignore`, usuário não-root.
- [Imagem oficial `node` no Docker Hub](https://hub.docker.com/_/node) — variantes `alpine`/`slim` e o usuário `node`.
- [Imagem oficial `mysql` no Docker Hub](https://hub.docker.com/_/mysql) — variáveis `MYSQL_*`, `docker-entrypoint-initdb.d` e healthcheck.
- [GitHub — Working with the Container registry](https://docs.github.com/pt/packages/working-with-a-github-packages-registry/working-with-the-container-registry) — login, push e visibilidade de pacotes no GHCR.
- [Docker and ufw](https://docs.docker.com/engine/network/packet-filtering-firewalls/) — por que o Docker passa por cima do firewall e como publicar portas só em `127.0.0.1`.

No Capítulo 08 o MySQL sai do VPS: você vai levar o banco para um serviço gerenciado (Supabase, Neon ou um MySQL na nuvem), com migrations versionadas, seed, backup e restauração — e descobrir por que a região do banco importa tanto quanto a região da API.
