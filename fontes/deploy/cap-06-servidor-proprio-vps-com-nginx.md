# Capítulo 06 — Servidor próprio (VPS) com nginx

> **Deploy & Ferramentas** · Unidade 2: Publicação: estático, back-end, domínio e servidor
> WebLab · UNEMAT — Campus Sinop
> **Tempo estimado:** 2 a 3 h · estudo autônomo, em paralelo à sua trilha

## 🎯 Objetivos de aprendizagem

Ao final deste capítulo você será capaz de:

- Justificar quando um VPS compensa e quando uma PaaS resolve melhor, comparando custo, latência, controle e trabalho de manutenção.
- Acessar um servidor Ubuntu por SSH com par de chaves, criar o usuário `deploy`, desligar o login por senha e ligar o firewall `ufw` sem se trancar do lado de fora.
- Instalar e configurar Node 22, MySQL 8 e nginx em um Ubuntu 24.04, criando banco e usuário com privilégios mínimos.
- Escrever um `server` do nginx que sirva arquivos estáticos e outro que funcione como **proxy reverso** para `127.0.0.1:3000`, entendendo cada `proxy_set_header`.
- Manter um processo Node vivo com pm2 (`pm2 start`, `pm2 save`, `pm2 startup`) e escrever a unidade `systemd` equivalente.
- Emitir e renovar certificados com `sudo certbot --nginx`, conferindo o timer de renovação automática.
- Publicar arquivos no servidor com `rsync` e explicar o que a barra final e o `--delete` fazem.
- Operar o laboratório real da disciplina em `https://ivanpires.dev/dsw/gN/`: publicar o front em `~/frontend`, atualizar o back em `~/backend`, reiniciar o serviço e ler os logs.
- Diagnosticar `502 Bad Gateway`, `403 Forbidden`, `Permission denied (publickey)` e falha de emissão de certificado usando os logs certos.

## 📋 Pré-requisitos

- [ ] Capítulos 02 e 04 concluídos: repositórios no GitHub e um domínio (ou subdomínio gratuito) sob seu controle, com acesso ao painel de DNS.
- [ ] Terminal com `ssh`, `rsync` e `dig` (Windows: use o WSL — todos os comandos deste capítulo assumem um shell Linux/macOS).
- [ ] Um VPS próprio — a §2 lista opções a partir de poucos reais por mês. Se você é aluno da turma de Deploy & Ferramentas na UNEMAT Sinop, vale também o acesso ao laboratório da disciplina (`gN@ivanpires.dev`) fornecido pelo professor, descrito na §11.
- [ ] `unieventos-api` (Nível 3) e `unieventos-web` funcionando na sua máquina, com `npm run build` gerando `dist/`. Não está no Nível 3? Use a `cafe-cerrado-api` e o Café Cerrado estático — os passos são idênticos.
- [ ] Paciência para errar: você **vai** se trancar fora do servidor pelo menos uma vez. A §4 mostra como não perder o acesso de vez.

> No Capítulo 05 a `cafe-cerrado-api` subiu numa PaaS: você entregou um repositório e a plataforma cuidou de porta, processo, HTTPS e reinício. O preço foi o *cold start*, o disco efêmero e um servidor do outro lado do continente. Hoje você troca de lado: aluga uma máquina Linux vazia e monta tudo com as próprias mãos — usuário, firewall, Node, MySQL, nginx, supervisor e certificado. É mais trabalho e é o que revela o que a PaaS fazia por você.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Por que um VPS; criar a máquina; SSH com chave; usuário `deploy`, `ufw` e atualizações (§1 a §4) |
| 2 | 50 min | Node 22, MySQL 8, nginx (estático + proxy reverso), pm2 e systemd (§5 a §8) |
| 3 | 60 min | `certbot`, `rsync`, o laboratório `ivanpires.dev/dsw/gN/` e o Passo a passo completo (§9 a §11) |

## 1. Por que um servidor próprio — e quando não vale a pena

Um **VPS** (*virtual private server*) é uma fatia de um servidor físico com o seu próprio sistema operacional, IP público e acesso de administrador. Você recebe uma máquina Ubuntu vazia e um endereço IP. Tudo o mais é com você.

### 1.1 O que você ganha

- **Controle total.** Qualquer versão de qualquer coisa, qualquer porta, qualquer serviço. Nada de "a plataforma não suporta".
- **Vários projetos no mesmo lugar.** Um VPS de 10 reais por mês hospeda os três projetos do semestre, cada um em um subdomínio, com um banco compartilhado — algo que na PaaS seria um serviço (e uma cota) por projeto.
- **Nada dorme.** Sem *cold start*: o processo fica de pé o tempo todo.
- **Região.** Existem provedores com data center em São Paulo. A diferença de latência para Sinop é visível.
- **Custo previsível.** Preço fixo por mês, sem surpresa por consumo.
- **Aprendizado.** Você entende o que a PaaS escondia. Isso vale para o resto da carreira — e é o que a maioria das vagas de back-end espera que você saiba.

### 1.2 O que você assume

- **Segurança é sua.** Um IP público recebe tentativas de invasão automatizadas em minutos (§4.4). Atualizar o sistema, fechar portas e proteger o SSH passa a ser tarefa sua.
- **Backup é seu.** Apagou o banco? Não há botão de restaurar. O Capítulo 08 trata disso a sério.
- **Disponibilidade é sua.** O processo morreu às 3h da manhã? Ninguém reinicia por você — a não ser que você tenha configurado o supervisor (§8).
- **Certificado é seu.** Renovação vencida = site fora do ar com aviso vermelho. O `certbot` automatiza, mas você precisa conferir que ele está rodando (§9).

### 1.3 Como escolher

| Escolha | Quando |
|---|---|
| **PaaS** (Capítulo 05) | protótipo, trabalho pequeno, sem tempo de manutenção |
| **VPS** (este capítulo) | vários projetos, precisa de baixa latência ou de controle |
| **Contêiner** (Capítulo 07) | quer o VPS, mas com ambiente reproduzível |

Não existe resposta certa universal. Existe a resposta certa para um contexto — e agora você conhece os dois lados para argumentar.

> **🧠 Você sabia?**
> O nginx nasceu para resolver um problema com nome próprio: o **problema C10K** — como atender dez mil conexões simultâneas em uma máquina. Os servidores da época criavam um processo (ou uma thread) por conexão, e a memória acabava muito antes das dez mil. Igor Sysoev escreveu o nginx em 2004 com arquitetura **orientada a eventos**: poucos processos, cada um cuidando de milhares de conexões em um laço não bloqueante. É exatamente a mesma ideia por trás do *event loop* do Node.js — dois projetos diferentes, a mesma resposta para a mesma pergunta.

## 2. Escolhendo e criando o VPS

### 2.1 Provedores

| Provedor | Observação |
|---|---|
| Hetzner, Contabo | melhor relação recurso/preço; data centers na Europa e nos EUA |
| DigitalOcean, Vultr, Linode | documentação excelente; região em São Paulo em alguns planos |
| Oracle Cloud (Always Free) | camada gratuita permanente com máquinas ARM; cadastro exige cartão |
| Provedores brasileiros | latência baixa e suporte em português; preços em real |

Para os projetos deste semestre, o menor plano serve: **1 vCPU, 1 a 2 GB de RAM, 20 GB de disco**. O gargalo aparecerá muito antes na sua consulta SQL do que no hardware.

### 2.2 Na criação da máquina

Escolha **Ubuntu Server 24.04 LTS**. LTS significa suporte longo — atualizações de segurança por anos, sem precisar migrar de versão no meio do semestre. É a distribuição com mais tutoriais e a que todo provedor oferece.

Se o painel do provedor oferecer **adicionar uma chave SSH na criação**, faça isso (§3.1): a máquina já nasce sem senha de acesso, o que elimina a janela de risco entre criar e proteger.

Anote: o **IP público** (algo como `203.0.113.10`) e a senha de `root`, se o provedor mandar uma por e-mail.

## 3. SSH: entrar com chave, nunca com senha

### 3.1 Gerar o par de chaves

Uma chave SSH é um par de arquivos: a **privada** (`~/.ssh/id_ed25519`), que nunca sai da sua máquina, e a **pública** (`~/.ssh/id_ed25519.pub`), que você copia para todo servidor onde quiser entrar. O servidor lança um desafio que só quem tem a privada consegue responder. Nenhuma senha viaja pela rede.

```bash
ls ~/.ssh                                  # já existe id_ed25519? então pule
ssh-keygen -t ed25519 -C "seu-email@exemplo.com"
cat ~/.ssh/id_ed25519.pub
```

O `ssh-keygen` pergunta onde salvar (aceite o padrão com <kbd>Enter</kbd>) e uma **frase secreta**. Use uma: ela criptografa a chave privada em disco, de modo que um notebook roubado não vira acesso ao servidor. Para não digitá-la a cada comando, o `ssh-agent` guarda a chave destravada durante a sessão:

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
ssh-add -l
```

`ed25519` é o algoritmo recomendado hoje: chaves curtas, rápidas e fortes. Se um serviço antigo não aceitar, o alternativo é `ssh-keygen -t rsa -b 4096`.

### 3.2 Primeiro acesso e cópia da chave

```bash
ssh root@203.0.113.10
```

Na primeira vez aparece a pergunta sobre a impressão digital do servidor. Responder `yes` grava a chave pública do **servidor** em `~/.ssh/known_hosts`; a partir daí, o seu cliente avisa se ela mudar (o que pode significar um servidor recriado — ou um ataque).

Para instalar a sua chave pública no servidor sem editar arquivo nenhum:

```bash
ssh-copy-id root@203.0.113.10
```

Ele acrescenta a linha ao `~/.ssh/authorized_keys` do servidor, com as permissões certas (`700` na pasta `.ssh`, `600` no arquivo) — permissão errada é a causa nº 1 de "copiei a chave e continua pedindo senha".

### 3.3 Um apelido para o servidor

Digitar `ssh deploy@203.0.113.10` vinte vezes por dia é desperdício. O arquivo de configuração do cliente resolve:

`~/.ssh/config`

```text
Host meuvps
    HostName 203.0.113.10
    User deploy
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60

Host dsw
    HostName ivanpires.dev
    User g3
    IdentityFile ~/.ssh/id_ed25519
```

A partir daí, `ssh meuvps` e `ssh dsw` bastam — e o `rsync` e o `scp` também entendem o apelido. `ServerAliveInterval 60` manda um pacote de vida por minuto e evita que a sessão caia sozinha quando você fica lendo documentação.

> **💡 Dica**
> Comandos úteis no dia a dia: `ssh meuvps 'uptime'` roda um comando e volta sem abrir sessão interativa; `scp arquivo.sql meuvps:~/` copia um arquivo; `ssh -v meuvps` mostra o passo a passo da autenticação e é a melhor ferramenta para entender um `Permission denied (publickey)`.

## 4. Os primeiros 20 minutos no servidor

Esta é a sequência que você repete em **todo** servidor novo. Faça na ordem.

### 4.1 Atualizar o sistema

```bash
sudo apt update
sudo apt upgrade -y
sudo reboot
```

`apt update` atualiza a lista de pacotes disponíveis; `apt upgrade` instala as versões novas. São coisas diferentes, e confundi-las gera aquele "atualizei e nada mudou".

### 4.2 Criar o usuário `deploy`

Trabalhar como `root` é como programar com o dedo no botão de formatar: um comando errado apaga tudo, sem confirmação. Crie um usuário comum com poder de `sudo`:

```bash
adduser deploy
usermod -aG sudo deploy
rsync --archive --chown=deploy:deploy ~/.ssh /home/deploy
```

A terceira linha copia o `authorized_keys` do `root` para o novo usuário, já com o dono correto — é assim que a sua chave passa a funcionar para o `deploy`.

**Abra um segundo terminal** e teste, sem fechar o primeiro:

```bash
ssh deploy@203.0.113.10
sudo whoami
```

O `sudo whoami` deve responder `root`. Só depois de esse teste passar você pode mexer na configuração do SSH.

### 4.3 Fechar o SSH

Com a chave funcionando, desligue a senha e o login direto de `root`. No Ubuntu 24.04, o `/etc/ssh/sshd_config` começa com `Include /etc/ssh/sshd_config.d/*.conf`, então o jeito limpo é criar um arquivo próprio:

```bash
sudo nano /etc/ssh/sshd_config.d/00-weblab.conf
```

`/etc/ssh/sshd_config.d/00-weblab.conf`

```text
PasswordAuthentication no
KbdInteractiveAuthentication no
PermitRootLogin no
```

```bash
sudo sshd -t                    # testa a sintaxe; sem saída = tudo certo
sudo systemctl restart ssh
```

> **⚠️ Atenção**
> O número no nome do arquivo **importa**: no SSH, para cada opção vale o **primeiro** valor encontrado, e os arquivos são lidos em ordem alfabética. Imagens de nuvem costumam trazer um `/etc/ssh/sshd_config.d/50-cloud-init.conf` com `PasswordAuthentication yes` — por isso o nosso arquivo se chama `00-weblab.conf`, e não `99-`. Confira o resultado real com `sudo sshd -T | grep -i passwordauthentication`: tem que responder `passwordauthentication no`. E **nunca feche a sessão atual** antes de abrir uma nova em outro terminal para validar; enquanto a antiga estiver viva, você ainda consegue desfazer.

### 4.4 Firewall com `ufw`

O `ufw` é a interface amigável do firewall do Linux. A ordem dos comandos é vital:

```bash
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status numbered
```

Se você rodar `ufw enable` **antes** de liberar o OpenSSH, a sua sessão cai e você fica sem acesso — recuperável só pelo console de emergência do painel do provedor. Falta abrir as portas 80 e 443, e para isso existe o perfil `Nginx Full`; ele só passa a existir **depois** que o nginx é instalado — rodá-lo agora responde `ERROR: Could not find a profile matching 'Nginx Full'`. Por isso o `sudo ufw allow 'Nginx Full'` fica na §7.1, junto da instalação do nginx.

Para ver quem está batendo na porta:

```bash
sudo journalctl -u ssh --since "1 hour ago" | grep -c "Invalid user"
```

Em um servidor com poucas horas de vida esse número já costuma passar de mil. Não é pessoal: são robôs varrendo faixas inteiras de IP tentando `admin`, `test`, `ubuntu` e senhas óbvias. Com senha desligada, todos falham.

### 4.5 Duas proteções que custam dois comandos

```bash
sudo apt install -y unattended-upgrades fail2ban
sudo dpkg-reconfigure --priority=low unattended-upgrades
sudo systemctl enable --now fail2ban
sudo fail2ban-client status sshd
```

O `unattended-upgrades` instala sozinho as atualizações de segurança. O `fail2ban` lê os logs e bloqueia temporariamente o IP que erra a autenticação várias vezes seguidas. O `status sshd` mostra quantos IPs já foram banidos — costuma ser uma boa surpresa.

> **🔬 Investigue**
> Descubra em quantos segundos o seu servidor novo recebe a primeira tentativa de invasão. Logo depois de criar a máquina, rode:
>
> ```bash
> sudo journalctl -u ssh --since "10 minutes ago" | grep -E "Invalid user|Failed password" | head -20
> sudo journalctl -u ssh --since "1 hour ago" | grep "Invalid user" | awk '{print $NF}' | sort | uniq -c | sort -rn | head
> ```
>
> A segunda linha ranqueia os IPs mais insistentes. Escolha um e procure de que país ele é (`whois <ip> | grep -i country`). Depois responda: com `PasswordAuthentication no`, o que exatamente acontece com essas tentativas? Elas param de aparecer no log?

## 5. Node 22 no servidor

Duas formas, e a escolha muda a vida do §8.

### 5.1 NodeSource (recomendado em servidor)

```bash
curl -fsSL https://deb.nodesource.com/setup_22.x -o nodesource_setup.sh
sudo -E bash nodesource_setup.sh
sudo apt install -y nodejs
node -v
npm -v
which node
```

O `which node` deve responder `/usr/bin/node`. Guarde esse caminho: é ele que a unidade `systemd` do §8.3 vai usar.

### 5.2 nvm (e por que ele atrapalha aqui)

O `nvm` é ótimo na sua máquina — troca de versão em um comando. Mas ele instala o Node dentro de `~/.nvm/versions/node/v22.x/bin/node` e ativa a versão através de um trecho no `~/.bashrc`, que só roda em **shell interativo**. O `systemd` não abre shell interativo. O resultado é o erro clássico `status=203/EXEC` ao iniciar o serviço: "o arquivo não existe" — porque o caminho `node` só existe dentro do seu shell.

Se insistir no nvm, use o caminho absoluto no `ExecStart` e aceite que ele muda a cada atualização. Em servidor, prefira o pacote do sistema.

### 5.3 O `npm` global e o `sudo`

Instalar pacotes globais (`sudo npm install -g pm2`) escreve em `/usr/lib/node_modules`. Funciona, é o caminho mais direto, e é o que vamos usar para o pm2. Só tome cuidado com um detalhe: comandos instalados assim ficam em `/usr/bin` e são visíveis a todos — mas o `sudo` de algumas distribuições reseta o `PATH` e "esconde" binários instalados em outros lugares. Se `sudo pm2` disser `command not found` e `pm2` sozinho funcionar, é isso.

## 6. MySQL 8

### 6.1 Instalar e endurecer

```bash
sudo apt install -y mysql-server
sudo systemctl status mysql
sudo mysql_secure_installation
```

O `mysql_secure_installation` faz quatro perguntas que importam: ativar o validador de senhas (aceite), definir a senha do `root` (defina uma longa), remover usuários anônimos e o banco `test` (sim), e desativar login remoto de `root` (sim).

### 6.2 Banco e usuário do projeto

Nunca conecte a aplicação como `root`. Um usuário por projeto, com acesso só ao banco daquele projeto:

```bash
sudo mysql
```

```sql
CREATE DATABASE unieventos
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;

CREATE USER 'unieventos'@'localhost'
  IDENTIFIED BY 'troque-por-uma-senha-longa-e-aleatoria';

GRANT ALL PRIVILEGES ON unieventos.* TO 'unieventos'@'localhost';
FLUSH PRIVILEGES;

SHOW GRANTS FOR 'unieventos'@'localhost';
SELECT user, host, plugin FROM mysql.user;
```

`utf8mb4` é o conjunto de caracteres que guarda **todo** o Unicode, emoji incluído; o antigo `utf8` do MySQL guarda no máximo três bytes por caractere e corrompe emoji. `'unieventos'@'localhost'` restringe o usuário a conexões vindas da própria máquina.

Teste com o usuário novo e saia:

```bash
mysql -u unieventos -p unieventos -e "SELECT DATABASE(), USER();"
```

### 6.3 O banco não pode estar na internet

Por padrão, no Ubuntu, o MySQL escuta só em `127.0.0.1` — e é assim que deve ficar. Confirme:

```bash
sudo ss -tlnp | grep 3306
grep -n "^bind-address" /etc/mysql/mysql.conf.d/mysqld.cnf
```

A saída do `ss` precisa mostrar `127.0.0.1:3306`, nunca `0.0.0.0:3306`. Um MySQL exposto na internet com senha fraca é comprometido em horas — existem varreduras dedicadas a isso. Se algum dia você precisar acessar o banco do servidor pela sua máquina, **não** abra a porta: use um túnel SSH, que passa por dentro da conexão que você já tem.

```bash
ssh -L 3307:127.0.0.1:3306 meuvps
mysql -h 127.0.0.1 -P 3307 -u unieventos -p unieventos
```

O primeiro comando abre a porta `3307` na **sua** máquina e a liga, por dentro do SSH, à porta `3306` do servidor. Nenhum byte de MySQL trafega desprotegido, e o firewall continua fechado.

## 7. nginx: servir arquivos e ser proxy reverso

### 7.1 Instalar

```bash
sudo apt install -y nginx
sudo ufw allow 'Nginx Full'
sudo systemctl status nginx
curl -I http://localhost
```

O `curl` deve responder `HTTP/1.1 200 OK` com `Server: nginx`. Abrindo o IP no navegador, aparece a página de boas-vindas.

A estrutura de arquivos do Ubuntu:

| Caminho | Para que serve |
|---|---|
| `/etc/nginx/nginx.conf` | configuração global; inclui as duas pastas abaixo |
| `/etc/nginx/sites-available/` | um arquivo por site (habilitado ou não) |
| `/etc/nginx/sites-enabled/` | links simbólicos para os sites que estão no ar |
| `/var/log/nginx/access.log` e `error.log` | onde você descobre o que aconteceu |

### 7.2 Um site estático

Crie a pasta que vai receber os arquivos, com dono `deploy` — assim o `rsync` do §10 funciona sem `sudo`:

```bash
sudo mkdir -p /var/www/unieventos-web
sudo chown -R deploy:deploy /var/www/unieventos-web
```

`/etc/nginx/sites-available/eventos.seudominio.dev`

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name eventos.seudominio.dev;

    root /var/www/unieventos-web;
    index index.html;

    # SPA: qualquer rota desconhecida devolve o index.html,
    # e o vue-router decide o que mostrar no lado do navegador.
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Arquivos com hash no nome (gerados pelo Vite) podem ser cacheados para sempre:
    # se o conteúdo mudar, o nome do arquivo muda junto.
    location ~* \.(css|js|woff2|png|jpg|jpeg|svg|webp|ico)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    gzip on;
    gzip_types text/css application/javascript application/json image/svg+xml;
    gzip_min_length 1024;
}
```

```bash
sudo ln -s /etc/nginx/sites-available/eventos.seudominio.dev /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

`nginx -t` testa a configuração **sem** aplicar. Nunca faça `reload` sem ele: uma vírgula errada derruba todos os sites da máquina. E prefira `reload` a `restart`: o `reload` troca a configuração sem derrubar as conexões em andamento.

### 7.3 Proxy reverso para a API

Um **proxy reverso** é um servidor que recebe a requisição do visitante e a repassa para outro processo, devolvendo a resposta. Quem fala com a internet é o nginx; o Node fica escondido em `127.0.0.1:3000`, inalcançável de fora.

Por que não deixar o Node atender a porta 443 direto? Porque o nginx faz melhor cinco coisas que o Node faria pior: termina o TLS, serve arquivos estáticos, comprime, limita taxa e — o principal — permite **vários sites na mesma máquina**, escolhidos pelo cabeçalho `Host`.

`/etc/nginx/sites-available/api.seudominio.dev`

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name api.seudominio.dev;

    # Corpo máximo aceito (upload de imagem de evento, por exemplo).
    client_max_body_size 5m;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;

        # Sem estas quatro linhas, a API só enxerga o nginx.
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_connect_timeout 5s;
        proxy_read_timeout    60s;
    }
}
```

Os quatro `proxy_set_header` são o contrato com o `app.set('trust proxy', 1)` que você escreveu no Capítulo 05:

| Cabeçalho | O que carrega |
|---|---|
| `Host` | o domínio que o visitante digitou |
| `X-Real-IP` | o IP do visitante |
| `X-Forwarded-For` | a cadeia de proxies por onde a requisição passou |
| `X-Forwarded-Proto` | `http` ou `https` — o protocolo original |

Sem eles, `req.ip` na API devolve `127.0.0.1` para todo mundo e `req.protocol` devolve `http` mesmo em páginas com cadeado.

> **🔎 Por baixo do capô**
> Como o nginx decide qual `server` usa, se todos escutam na mesma porta 80? Ele lê o cabeçalho `Host` da requisição HTTP e procura um `server_name` que case. Se nenhum casar, usa o **primeiro** bloco declarado (ou o marcado com `default_server`) — foi por isso que, no Capítulo 04, apontar um domínio novo para um VPS devolvia o certificado de outro site. Teste você mesmo, sem mexer no DNS:
>
> ```bash
> curl -H "Host: api.seudominio.dev" http://203.0.113.10/api/saude
> curl -H "Host: nome-inexistente.exemplo" -I http://203.0.113.10/
> ```
>
> O primeiro chega à API; o segundo cai no site padrão. É o mesmo mecanismo que permite hospedar dez projetos em um IP só.

### 7.4 O bloco padrão

Enquanto existir o arquivo `/etc/nginx/sites-enabled/default`, qualquer nome desconhecido apontado para o seu IP mostra a página "Welcome to nginx" — inclusive nomes de terceiros. Duas opções: remover o link (`sudo rm /etc/nginx/sites-enabled/default`) ou substituí-lo por um bloco que simplesmente fecha a conexão:

`/etc/nginx/sites-available/000-catch-all`

```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;
    return 444;
}
```

O código `444` é uma extensão do nginx: fecha a conexão sem responder nada. É a resposta certa para requisição sem `Host` válido.

## 8. Manter o processo vivo

Rodar `node src/server.js` numa sessão SSH funciona até você fechar o terminal. Precisa de um **supervisor**: alguém que suba o processo no boot, reinicie quando ele morrer e guarde os logs.

### 8.1 pm2: primeiros comandos

```bash
sudo npm install -g pm2
pm2 --version

cd ~/apps/unieventos-api
pm2 start src/server.js --name unieventos-api
pm2 ls
pm2 logs unieventos-api --lines 50
pm2 restart unieventos-api
pm2 monit
```

### 8.2 Sobreviver ao reboot

Esta é a parte que quase todo mundo esquece — e descobre no primeiro reinício, com o site fora do ar:

```bash
pm2 startup
```

O comando **não** faz nada sozinho: ele imprime uma linha começando com `sudo env PATH=...` que você deve copiar e colar. Essa linha cria uma unidade `systemd` que chama o pm2 no boot. Depois:

```bash
pm2 save
```

O `pm2 save` grava a lista atual de processos em `~/.pm2/dump.pm2`. É essa lista que o pm2 restaura no boot. Mudou a lista (adicionou ou removeu um app)? Rode `pm2 save` de novo, ou a mudança se perde no próximo reinício.

### 8.3 Arquivo de configuração do pm2

Passar tudo por linha de comando não é reproduzível. Descreva o serviço em um arquivo versionado no repositório. Como o `package.json` da API tem `"type": "module"` (Capítulo 05 §4.3) e o pm2 lê o arquivo como CommonJS, a extensão precisa ser `.cjs`:

`ecosystem.config.cjs`

```js
// ecosystem.config.cjs — descrição do processo para o pm2.
// Rode com: pm2 start ecosystem.config.cjs
module.exports = {
  apps: [
    {
      name: 'unieventos-api',
      script: 'src/server.js',
      cwd: '/home/deploy/apps/unieventos-api',
      // Carrega o .env que está ao lado do código: é ele que traz
      // DB_USER, DB_PASSWORD, DB_NAME e as demais chaves.
      node_args: '--env-file=.env',
      instances: 1,
      exec_mode: 'fork',
      env: {
        NODE_ENV: 'production',
        // Só o nginx conversa com a API: escutar em loopback é mais seguro
        // do que em 0.0.0.0, que era o obrigatório na PaaS do Capítulo 05.
        HOST: '127.0.0.1',
        PORT: 3000,
      },
      max_memory_restart: '300M',
      autorestart: true,
      time: true,
      out_file: '/home/deploy/logs/unieventos-api.out.log',
      error_file: '/home/deploy/logs/unieventos-api.err.log',
    },
  ],
};
```

```bash
mkdir -p ~/logs
pm2 start ecosystem.config.cjs
pm2 save
```

Os segredos (senha do banco, chaves) **não** entram aqui: este arquivo vai para o Git. Eles ficam no `.env` do servidor, com permissão `chmod 600`, e quem os carrega é o `node_args: '--env-file=.env'` acima — sem essa linha o pm2 sobe o processo só com `NODE_ENV`, `HOST` e `PORT`, e a API morre na validação da configuração por falta de `DB_USER`/`DB_PASSWORD`/`DB_NAME`.

### 8.4 A alternativa nativa: `systemd`

O pm2 é conveniente, mas o Ubuntu já tem um supervisor: o `systemd`, o mesmo que cuida do nginx e do MySQL. É o que o laboratório da disciplina usa (§11), e vale conhecer.

`/etc/systemd/system/unieventos-api.service`

```ini
[Unit]
Description=API do UniEventos
After=network.target mysql.service

[Service]
Type=simple
User=deploy
Group=deploy
WorkingDirectory=/home/deploy/apps/unieventos-api
EnvironmentFile=/home/deploy/apps/unieventos-api/.env
ExecStart=/usr/bin/node src/server.js
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now unieventos-api
sudo systemctl status unieventos-api
sudo journalctl -u unieventos-api -f
```

Três detalhes que derrubam a primeira tentativa:

- **`ExecStart` exige caminho absoluto.** `node src/server.js` falha com `status=203/EXEC`; use `/usr/bin/node` (§5.1).
- **`EnvironmentFile` não é shell.** Ele lê linhas `CHAVE=valor` literais: nada de `export`, e as aspas viram parte do valor.
- **`daemon-reload` depois de editar.** Sem ele, o systemd continua usando a versão antiga do arquivo e você jura que a edição não fez efeito.

| Critério | pm2 | systemd |
|---|---|---|
| Instalação | pacote npm global | já vem no sistema |
| Configuração | `ecosystem.config.cjs` no repositório | arquivo `.service` como root |
| Logs | `pm2 logs` (arquivos em `~/.pm2/logs`) | `journalctl -u <nome>` |
| Recarga sem queda | `pm2 reload` (com várias instâncias) | `systemctl restart` derruba por instantes |

## 9. HTTPS de verdade: `certbot --nginx`

No Capítulo 04 você viu a teoria do ACME e viu plataformas emitindo certificado por você. Agora é você.

Antes de rodar qualquer coisa, três pré-condições — todas verificáveis:

1. O DNS já resolve os nomes para o IP do servidor: `dig +short api.seudominio.dev @1.1.1.1`.
2. A porta 80 está aberta e chegando ao nginx: `curl -I http://api.seudominio.dev`.
3. Existe um `server` com `server_name` **exatamente** igual ao nome que você vai pedir.

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d eventos.seudominio.dev -d api.seudominio.dev
```

O `certbot` pede um e-mail (para avisos de expiração), pede aceite dos termos, resolve o desafio `HTTP-01` servindo um arquivo em `/.well-known/acme-challenge/` pelo próprio nginx, e então **edita os seus arquivos de configuração**: acrescenta `listen 443 ssl;`, as diretivas `ssl_certificate` e `ssl_certificate_key`, e cria um bloco que redireciona `http://` para `https://` com `301`.

Confira o resultado:

```bash
sudo certbot certificates
sudo nginx -t
curl -I http://api.seudominio.dev     # 301 para https
curl -I https://api.seudominio.dev    # 200
```

### 9.1 Renovação automática

Certificados da Let's Encrypt valem 90 dias. O pacote instala um timer do systemd que roda duas vezes por dia e renova o que estiver a menos de 30 dias do vencimento:

```bash
systemctl list-timers | grep certbot
sudo certbot renew --dry-run
```

O `--dry-run` faz o ensaio completo contra o ambiente de homologação da Let's Encrypt, sem gastar cota nem trocar o certificado real. **Se ele passa, a renovação automática vai passar.** Rode-o hoje; assim você não descobre o problema daqui a três meses, com o site fora do ar.

> **⚠️ Atenção**
> Depois que o `certbot` mexeu nos arquivos, edite-os com cuidado: se você apagar o `server_name` ou trocar o nome do arquivo, a renovação seguinte falha com `Could not automatically find a matching server block`. E, se um dia precisar refazer tudo, use `--dry-run` primeiro — a Let's Encrypt limita a poucos certificados idênticos por semana, e estourar o limite deixa você esperando dias.

## 10. Publicando com `rsync`

O `rsync` copia só o que mudou, comparando tamanho e data de modificação. Para um site estático, é a ferramenta certa: rápido, incremental e por cima do SSH.

```bash
npm run build
rsync -avz --delete --dry-run dist/ meuvps:/var/www/unieventos-web/
rsync -avz --delete           dist/ meuvps:/var/www/unieventos-web/
```

As opções, uma a uma:

| Opção | O que faz |
|---|---|
| `-a` (*archive*) | copia recursivamente preservando permissões e datas |
| `-v` | mostra os arquivos transferidos |
| `-z` | comprime durante a transferência |
| `--delete` | apaga no destino o que não existe mais na origem |
| `--dry-run` | simula e lista o que faria, sem copiar nada |

E o detalhe que mais causa confusão: **a barra final na origem**. `dist/` copia *o conteúdo* de `dist` para dentro do destino; `dist` (sem barra) copia *a pasta* `dist` para dentro do destino, criando `/var/www/unieventos-web/dist/`. Sempre rode com `--dry-run` na primeira vez — ainda mais com `--delete`, que apaga de verdade.

Outras variações úteis:

```bash
rsync -avz --exclude '.git' --exclude 'node_modules' ./ meuvps:~/apps/unieventos-api/
rsync -avz -e "ssh -p 2222" dist/ meuvps:/var/www/unieventos-web/
rsync -avz meuvps:~/backups/unieventos.sql ./
```

Guarde a linha de publicação em um script do `package.json` para não errar a digitação nunca mais:

```json
{
  "scripts": {
    "publicar": "npm run build && rsync -avz --delete dist/ meuvps:/var/www/unieventos-web/"
  }
}
```

## 11. Estudo de caso: o laboratório da turma da UNEMAT em `ivanpires.dev/dsw/gN/`

Esta seção descreve o servidor real da turma de Deploy & Ferramentas na UNEMAT Sinop — é o mesmo VPS que hospeda este WebLab, com uma conta por grupo. Se você é aluno dessa turma, é o ambiente que você vai usar, e o acesso é fornecido pelo professor. Se está estudando por conta própria, leia esta seção como um **estudo de caso completo** de tudo o que as §§1–10 ensinaram, aplicado a um servidor de verdade — e repita o mesmo desenho no seu próprio VPS. Substitua `N` pelo número do seu grupo em tudo o que segue — os exemplos usam o grupo 3.

### 11.1 O que cada grupo recebe

| Recurso | Valor (grupo `N`) | Exemplo (grupo 3) |
|---|---|---|
| Endereço público | `https://ivanpires.dev/dsw/gN/` | `https://ivanpires.dev/dsw/g3/` |
| Acesso | `ssh gN@ivanpires.dev` | `ssh g3@ivanpires.dev` |
| Pastas | `~/frontend` e `~/backend` | as mesmas |
| Porta da API e serviço | `350N` · `dsw-gN` | `3503` · `dsw-g3` |
| Banco MySQL | `db_gN` | `db_g3` |

O front fica em `~/frontend` e é servido pelo nginx em `/dsw/gN/`. O back roda em `~/backend`, escuta em `127.0.0.1:350N` e recebe as requisições de `/dsw/gN/api/` por proxy reverso. O banco `db_gN` é acessível só de `localhost`.

Na primeira vez, envie a sua chave pública para o professor (`cat ~/.ssh/id_ed25519.pub`) — a conta não aceita senha, exatamente como você configurou o seu VPS na §4.3.

### 11.2 Como o professor montou isso (e você repetirá no seu VPS)

O lado do servidor é o que você acabou de estudar. Um trecho do `server` de `ivanpires.dev`:

```nginx
# Front do grupo 3: arquivos estáticos em /home/g3/frontend
location /dsw/g3/ {
    alias /home/g3/frontend/;
    try_files $uri $uri/ /dsw/g3/index.html;
}

# API do grupo 3: proxy para a porta 3503, só em loopback
location /dsw/g3/api/ {
    proxy_pass http://127.0.0.1:3503/api/;
    proxy_http_version 1.1;
    proxy_set_header Host              $host;
    proxy_set_header X-Real-IP         $remote_addr;
    proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

E a unidade do serviço, no molde da §8.4:

`/etc/systemd/system/dsw-g3.service`

```ini
[Unit]
Description=API do grupo 3 (DSW)
After=network.target mysql.service

[Service]
Type=simple
User=g3
Group=g3
WorkingDirectory=/home/g3/backend
EnvironmentFile=/home/g3/backend/.env
ExecStart=/usr/bin/node src/server.js
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Repare no `location /dsw/g3/api/` com `proxy_pass http://127.0.0.1:3503/api/`: os dois terminam em barra. Isso faz o nginx **substituir** o prefixo `/dsw/g3/api/` por `/api/` antes de repassar — então a sua API continua respondendo em `/api/eventos` como na sua máquina, sem saber que existe um prefixo. Tire a barra final do `proxy_pass` e o caminho inteiro é repassado; a API recebe `/dsw/g3/api/eventos` e devolve `404`.

### 11.3 O ciclo de trabalho do grupo

Do lado da sua máquina, para publicar o front:

```bash
npm run build
rsync -avz --delete dist/ g3@ivanpires.dev:~/frontend/
```

Do lado do servidor, para atualizar a API:

```bash
ssh g3@ivanpires.dev
cd ~/backend
git pull
npm ci --omit=dev
sudo systemctl restart dsw-g3
systemctl status dsw-g3 --no-pager
journalctl -u dsw-g3 -n 50 --no-pager
```

O `sudo systemctl restart dsw-g3` é o **único** comando privilegiado liberado para a sua conta: o professor autorizou exatamente essa linha na configuração do `sudo`. Qualquer outro `sudo` responde que você não está no arquivo de permissões — e isso é proposital: um grupo não consegue derrubar o serviço de outro nem tocar na configuração do nginx.

### 11.4 O detalhe que quebra todo semestre: o subcaminho

O seu site vive em `/dsw/g3/`, não na raiz. Tudo o que for caminho absoluto quebra:

- `<link href="/css/estilo.css">` procura `https://ivanpires.dev/css/estilo.css` — que não existe. Use caminhos relativos ou o prefixo completo.
- Em um projeto Vite, ajuste a base antes de gerar o build.

`vite.config.js`

```js
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  // O site é servido em https://ivanpires.dev/dsw/g3/, não na raiz.
  base: '/dsw/g3/',
});
```

E o `vue-router` precisa saber do mesmo prefixo:

`src/router/index.js`

```js
import { createRouter, createWebHistory } from 'vue-router';
import rotas from './rotas.js';

export default createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: rotas,
});
```

`import.meta.env.BASE_URL` recebe automaticamente o valor de `base` do `vite.config.js` — assim o prefixo fica escrito em um só lugar. E a URL da API no front vira `/dsw/g3/api`, um caminho relativo à mesma origem: sem CORS, porque front e back compartilham `https://ivanpires.dev`.

## 🚀 Passo a passo — o UniEventos no seu VPS

O que vai ao ar: `https://eventos.seudominio.dev` servindo o `unieventos-web` e `https://api.seudominio.dev` servindo a `unieventos-api` por proxy reverso, com MySQL local, pm2 e certificado válido. Troque `seudominio.dev` pelo seu domínio (Capítulo 04) e `203.0.113.10` pelo IP do seu VPS. Está no Nível 2? Troque UniEventos por Café Cerrado; os comandos são os mesmos.

### Passo 1 — crie a máquina e entre

Ubuntu Server 24.04 LTS, plano mínimo, chave SSH adicionada na criação se o painel permitir.

```bash
ssh root@203.0.113.10
apt update && apt upgrade -y
```

### Passo 2 — usuário `deploy` e chave

```bash
adduser deploy
usermod -aG sudo deploy
rsync --archive --chown=deploy:deploy ~/.ssh /home/deploy
```

Em **outro terminal**, valide antes de continuar:

```bash
ssh deploy@203.0.113.10 'sudo whoami'
```

Resultado esperado: `root`. Acrescente o apelido `meuvps` ao seu `~/.ssh/config` (§3.3).

### Passo 3 — feche o SSH e ligue o firewall

```bash
ssh meuvps
sudo tee /etc/ssh/sshd_config.d/00-weblab.conf > /dev/null <<'FIM'
PasswordAuthentication no
KbdInteractiveAuthentication no
PermitRootLogin no
FIM
sudo sshd -t && sudo systemctl restart ssh
sudo sshd -T | grep -i passwordauthentication

sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status
```

### Passo 4 — aponte o DNS

No painel de DNS do seu domínio, dois registros `A` com TTL 300:

```text
Tipo: A    Nome: eventos    Valor: 203.0.113.10
Tipo: A    Nome: api        Valor: 203.0.113.10
```

Confirme antes de seguir — o `certbot` do Passo 11 depende disso:

```bash
dig +short eventos.seudominio.dev @1.1.1.1
dig +short api.seudominio.dev @1.1.1.1
```

### Passo 5 — Node, MySQL e nginx

```bash
curl -fsSL https://deb.nodesource.com/setup_22.x -o nodesource_setup.sh
sudo -E bash nodesource_setup.sh
sudo apt install -y nodejs mysql-server nginx
sudo ufw allow 'Nginx Full'
node -v && mysql --version && nginx -v
sudo mysql_secure_installation
```

### Passo 6 — banco e usuário

```bash
sudo mysql
```

```sql
CREATE DATABASE unieventos CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
CREATE USER 'unieventos'@'localhost' IDENTIFIED BY 'coloque-uma-senha-longa-aqui';
GRANT ALL PRIVILEGES ON unieventos.* TO 'unieventos'@'localhost';
FLUSH PRIVILEGES;
```

### Passo 7 — código e `.env` da API

```bash
mkdir -p ~/apps ~/logs
cd ~/apps
git clone https://github.com/seu-usuario/unieventos-api.git
cd unieventos-api
npm ci --omit=dev
nano .env
chmod 600 .env
npm run migrar
```

`~/apps/unieventos-api/.env`

```text
NODE_ENV=production
HOST=127.0.0.1
PORT=3000
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=unieventos
DB_PASSWORD=coloque-uma-senha-longa-aqui
DB_NAME=unieventos
CORS_ORIGENS=https://eventos.seudominio.dev
```

Teste antes de envolver o supervisor:

```bash
node --env-file=.env src/server.js
```

Em outro terminal do servidor: `curl -s http://127.0.0.1:3000/api/saude` deve responder `{"status":"ok"}` (a mesma rota do Capítulo 05 §6.1, que também atende em `/health`). Encerre com <kbd>Ctrl</kbd>+<kbd>C</kbd>.

Ainda no Passo 7, **crie o `ecosystem.config.cjs`** da §8.3 na raiz do projeto — na sua máquina, com `git add ecosystem.config.cjs`, commit e push, e depois `git pull` no servidor; ou direto no servidor com `nano ecosystem.config.cjs`, lembrando de levá-lo para o repositório em seguida. Ele não guarda segredo nenhum (é o `node_args: '--env-file=.env'` que lê o `.env` do servidor), então **deve** ficar versionado: é a descrição do processo, e sem ele o Passo 8 não tem o que iniciar.

### Passo 8 — pm2

```bash
sudo npm install -g pm2
cd ~/apps/unieventos-api
pm2 start ecosystem.config.cjs
pm2 ls
pm2 logs unieventos-api --lines 20
pm2 startup           # copie e cole a linha 'sudo env PATH=...' que ele imprimir
pm2 save
```

### Passo 9 — nginx

Crie os dois arquivos da §7.2 e da §7.3, com os seus nomes de domínio, e habilite:

```bash
sudo mkdir -p /var/www/unieventos-web
sudo chown -R deploy:deploy /var/www/unieventos-web
sudo ln -s /etc/nginx/sites-available/eventos.seudominio.dev /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/api.seudominio.dev /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
curl -s http://api.seudominio.dev/api/saude
```

### Passo 10 — publique o front

Na **sua máquina**, com `VITE_API_URL=https://api.seudominio.dev` no `.env.production` do projeto:

```bash
npm run build
rsync -avz --delete --dry-run dist/ meuvps:/var/www/unieventos-web/
rsync -avz --delete           dist/ meuvps:/var/www/unieventos-web/
curl -I http://eventos.seudominio.dev
```

### Passo 11 — HTTPS

```bash
ssh meuvps
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d eventos.seudominio.dev -d api.seudominio.dev
sudo certbot renew --dry-run
systemctl list-timers | grep certbot
```

### Passo 12 — prove que sobrevive ao reboot

```bash
sudo reboot
```

Espere um minuto e, da sua máquina:

```bash
curl -s https://api.seudominio.dev/api/saude
curl -I https://eventos.seudominio.dev
```

Se a API não responder, o `pm2 save` ou o `pm2 startup` não foram feitos (§8.2). Volte, refaça, reinicie de novo.

### Como conferir

```bash
curl -I https://eventos.seudominio.dev
curl -s https://api.seudominio.dev/api/saude
curl -I http://api.seudominio.dev
ssh meuvps 'pm2 ls; sudo ss -tlnp | grep -E ":80|:443|:3000|:3306"'
```

Resultado esperado:

- o primeiro devolve `HTTP/2 200` com `server: nginx`;
- o segundo devolve `{"status":"ok"}` com `ambiente` igual a `production`;
- o terceiro devolve `301` com `location: https://api.seudominio.dev/`;
- o `pm2 ls` mostra `unieventos-api` com status `online` e `restarts` igual a 0 ou 1;
- o `ss` mostra o nginx em `0.0.0.0:80` e `0.0.0.0:443`, o Node em `127.0.0.1:3000` e o MySQL em `127.0.0.1:3306` — **nenhum** dos dois últimos em `0.0.0.0`;
- no navegador, o site lista eventos vindos da API, com cadeado e sem erro no console.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Explique, em duas frases, a diferença entre chave pública e chave privada, e diga qual das duas vai para o servidor e em qual arquivo.

**A2.** Preveja a saída. Você roda, nesta ordem: `sudo ufw enable` e depois `sudo ufw allow OpenSSH`. O que acontece com a sua sessão SSH atual? E com a próxima tentativa de conexão? Como você recuperaria o acesso?

**A3.** O que muda entre `rsync -avz dist/ meuvps:/var/www/site/` e `rsync -avz dist meuvps:/var/www/site/`? Desenhe a árvore de diretórios resultante nos dois casos.

**A4.** A API responde em `http://127.0.0.1:3000/api/saude` dentro do servidor, mas `https://api.seudominio.dev/api/saude` devolve `502 Bad Gateway`. Liste três causas possíveis, em ordem do mais provável ao menos provável, e o comando que confirma cada uma.

**A5.** Complete: no Capítulo 05 a API precisava escutar em `______` porque `______`; neste capítulo ela escuta em `______` porque `______`.

**A6.** Um colega diz: "coloquei `pm2 start` e testei o reboot; não voltou". Quais dois comandos faltaram, e o que cada um deles guarda?

### Nível B — Aplicação

**B1.** Hospede um segundo site no **mesmo** VPS: publique o `site-evento` (Nível 1) em `evento.seudominio.dev`, com registro DNS, `server` próprio no nginx, `rsync` e certificado.

Resultado esperado: os dois sites respondem `200` em HTTPS pelo mesmo IP; `curl -H "Host: evento.seudominio.dev" http://203.0.113.10` traz o site do evento e `curl -H "Host: eventos.seudominio.dev" http://203.0.113.10` traz o UniEventos.

<details><summary>Dica</summary>

Copie o arquivo da §7.2, troque `server_name` e `root`, crie a pasta com `chown deploy`, `ln -s`, `nginx -t`, `reload`. O `certbot` aceita vários `-d` em um só comando e reaproveita o certificado existente se você usar `--expand`.
</details>

**B2.** Provoque e diagnostique um `502 Bad Gateway`. Pare a API (`pm2 stop unieventos-api`), acesse a URL pública, leia o erro no navegador e depois encontre a linha correspondente no log do nginx. Suba a API de novo e confirme que o erro sumiu.

Resultado esperado: a linha do `/var/log/nginx/error.log` copiada, contendo `connect() failed (111: Connection refused) while connecting to upstream`, e uma explicação de qual processo recusou a conexão e por quê.

<details><summary>Dica</summary>

`sudo tail -f /var/log/nginx/error.log` em um terminal enquanto você acessa a URL em outro. O nginx registra o `upstream` que tentou alcançar — compare-o com o `proxy_pass` do seu arquivo.
</details>

**B3.** Faça o túnel SSH da §6.3 e conecte-se ao MySQL do servidor a partir de um cliente gráfico (DBeaver, MySQL Workbench, ou a extensão do VS Code) rodando na sua máquina, **sem** abrir a porta 3306 no firewall.

Resultado esperado: o cliente gráfico lista as tabelas do banco `unieventos`; `sudo ufw status` continua sem nenhuma regra para 3306; e você consegue explicar por onde os dados trafegaram.

<details><summary>Dica</summary>

`ssh -L 3307:127.0.0.1:3306 meuvps` e, no cliente, host `127.0.0.1`, porta `3307`. Deixe o terminal do túnel aberto: fechando-o, a conexão do cliente cai. `ssh -fNL 3307:127.0.0.1:3306 meuvps` roda o túnel em segundo plano.
</details>

**B4.** Compare pm2 e systemd na prática: pare o pm2, escreva a unidade da §8.4 para a mesma API, suba por systemd, mate o processo à força (`kill -9 <pid>`) e cronometre em quanto tempo ele volta. Repita com o pm2.

Resultado esperado: uma tabela de quatro linhas (supervisor · comando de status · onde ficam os logs · tempo até voltar depois do `kill -9`) e uma recomendação justificada para o seu projeto.

<details><summary>Dica</summary>

Descubra o PID com `pm2 ls` ou `systemctl show -p MainPID unieventos-api`. O `RestartSec=5` da unidade define a espera do systemd; o pm2 reinicia quase instantaneamente, mas tem proteção contra laço de reinício se o processo morrer rápido demais várias vezes seguidas.
</details>

### Nível C — Desafio

**C1.** Publique o seu projeto no laboratório da disciplina, do zero, em 20 minutos: build do front com `base` correta, `rsync` para `~/frontend`, `git pull` e `npm ci --omit=dev` no `~/backend`, `.env` apontando para `db_gN`, `sudo systemctl restart dsw-gN` e verificação em `https://ivanpires.dev/dsw/gN/`. Documente cada comando em um arquivo `PUBLICAR.md` no repositório, de modo que qualquer integrante do grupo consiga repetir sem perguntar nada.

<details><summary>Dica</summary>

Comece pelo `base: '/dsw/gN/'` do `vite.config.js` — sem isso, o site abre em branco e o console mostra `404` em todos os `.js` e `.css`. A URL da API no front deve ser relativa (`/dsw/gN/api`), nunca `http://localhost:350N`. Se o serviço não subir, `journalctl -u dsw-gN -n 50 --no-pager` mostra a exceção do Node.
</details>

## 🏆 Desafios

### ⭐ O diário do servidor
Tags: seguranca, terminal, investigacao, deploy

O seu VPS tem poucas horas de vida e já é alvo de milhares de tentativas de acesso. Elas vêm de robôs que varrem faixas inteiras de IP procurando senhas fracas — e ficam todas registradas. Faça a auditoria: descubra quantas tentativas houve, de onde vieram, quais usuários foram testados e o que aconteceria se você tivesse deixado a autenticação por senha ligada.

**Critérios de pronto**

- Um `auditoria.md` no repositório com: total de tentativas de login inválidas nas últimas 24 h, os 10 IPs mais insistentes com país de origem, e os 10 nomes de usuário mais tentados.
- O comando usado em cada número, copiado exatamente como você rodou.
- A saída de `sudo fail2ban-client status sshd` mostrando pelo menos um IP banido, com a explicação de qual regra o baniu.
- A saída de `sudo sshd -T | grep -i -E "passwordauthentication|permitrootlogin"` provando que nenhuma dessas tentativas poderia ter sucesso.
- Um parágrafo respondendo: por que as tentativas **continuam** aparecendo no log mesmo com a senha desligada?

<details><summary>Pistas</summary>

1. `sudo journalctl -u ssh --since "24 hours ago"` é a fonte; `grep`, `awk '{print $NF}'`, `sort | uniq -c | sort -rn | head` fazem a contagem.
2. Para os usuários tentados, procure as linhas `Invalid user <nome> from <ip>` — o nome é o penúltimo campo antes de `from`.
3. `whois <ip> | grep -i -E "country|netname"` identifica a origem; muitos IPs pertencem a provedores de nuvem, não a "hackers em porões".
4. O SSH registra a tentativa **antes** de decidir se o método é aceito; o que muda com a senha desligada é o desfecho, não o registro.
</details>

### ⭐⭐ Nota A no SSL Labs
Tags: https, nginx, seguranca, performance

O `certbot` deixa o seu site funcionando, mas com a configuração TLS padrão. Submeta `https://eventos.seudominio.dev` ao teste do SSL Labs (<https://www.ssllabs.com/ssltest/>) e veja a nota. Depois melhore a configuração até chegar a **A** — e entenda cada mudança, em vez de colar um bloco de configuração pronto da internet.

**Critérios de pronto**

- Captura (ou texto) do relatório do SSL Labs antes e depois, com as notas.
- Nota final **A** ou superior, com os quatro grupos de pontuação do relatório anotados.
- Cabeçalhos de segurança presentes na resposta, provados com `curl -sI https://eventos.seudominio.dev`: `Strict-Transport-Security`, `X-Content-Type-Options` e `Referrer-Policy`.
- Um arquivo de configuração comentado, com **uma linha explicando cada diretiva** que você acrescentou — sem diretiva copiada que você não saiba justificar.
- `sudo nginx -t` passa e `sudo certbot renew --dry-run` continua passando depois das mudanças.

<details><summary>Pistas</summary>

1. O `certbot` cria `/etc/letsencrypt/options-ssl-nginx.conf` com um conjunto razoável de protocolos e cifras; leia-o antes de mudar qualquer coisa.
2. Os pontos que costumam faltar: TLS 1.0/1.1 ainda habilitados, ausência de HSTS e chave Diffie-Hellman fraca (`ssl_dhparam`, gerado com `openssl dhparam -out /etc/nginx/dhparam.pem 2048`).
3. `add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;` — releia a §6.5 do Capítulo 04 antes de ligar `includeSubDomains`, e não use `preload` ainda.
4. `ssl_stapling on;` e `ssl_session_cache shared:SSL:10m;` melhoram desempenho; confirme o efeito no próprio relatório do SSL Labs.
</details>

### ⭐⭐⭐ Publicação sem derrubar o site
Tags: deploy, nginx, node, terminal

Hoje o seu deploy é uma sequência de comandos digitados à mão que deixa o site fora do ar por alguns segundos — e, se algo falhar no meio, deixa o servidor num estado híbrido, com o front novo e a API antiga. Escreva um script de publicação que seja **repetível**, **verificável** e **reversível**: se qualquer etapa falhar, ele volta o servidor exatamente ao estado anterior.

**Critérios de pronto**

- Um `publicar.sh` no repositório, com `set -euo pipefail`, que publica front e back em um comando e imprime o que está fazendo.
- Publicação do front por **troca de link simbólico**: os arquivos vão para `/var/www/unieventos-web/releases/<data-hora>/`, e só depois de o `rsync` terminar o link `current` passa a apontar para a versão nova. O `root` do nginx aponta para `current`.
- Verificação automática depois de reiniciar a API: o script consulta a rota de saúde por até 30 segundos e, se ela não responder `200`, refaz o link para a versão anterior, reinicia a API na versão anterior e sai com código diferente de zero.
- Um teste real de rollback: quebre a API de propósito (uma variável de ambiente errada), rode o script e mostre que o site continuou no ar com a versão antiga.
- `README.md` com o número de segundos em que o site ficou indisponível durante uma publicação bem-sucedida, medido por você.

<details><summary>Pistas</summary>

1. `ln -sfn /var/www/unieventos-web/releases/<data-hora> /var/www/unieventos-web/current` troca o alvo de um link de forma atômica; o `-n` evita criar um link dentro do diretório apontado.
2. O nginx segue o link a cada requisição, então não precisa de `reload` para ver a versão nova — mas confira se `root` aponta para `current` e não para o caminho real.
3. Para a verificação, um laço `for` com `curl -fsS URL/api/saude` e `sleep 2`; a opção `-f` faz o `curl` sair com erro em status HTTP de falha, o que combina com o `set -e`.
4. `pm2 reload` (em vez de `restart`) e um `trap` no shell para executar o rollback quando o script sair com erro são as duas peças que fecham o desafio.
5. Guarde as três últimas versões e apague as mais antigas — senão o disco de 20 GB acaba no meio do semestre.
</details>

### 🔥 Boss — Os três projetos no ar, com HTTPS, em subdomínios
Tags: deploy, nginx, https, dns, projeto

Um servidor. Um domínio. Três projetos do semestre, cada um em um subdomínio, todos com cadeado — e um `README.md` que qualquer pessoa consegue seguir para reconstruir tudo do zero em uma máquina nova. É o fechamento da Unidade 2: DNS (Capítulo 04), publicação estática (Capítulo 03), back-end (Capítulo 05) e servidor próprio (este capítulo) funcionando juntos, na sua infraestrutura.

Os três: o **site do evento** (Nível 1, estático), o **Café Cerrado** (Nível 2: front estático + `cafe-cerrado-api`) e o **UniEventos** (Nível 3: `unieventos-web` + `unieventos-api` com MySQL). Cinco endereços no total, dois processos Node em portas diferentes, um único IP.

**Critérios de pronto**

- Cinco subdomínios respondendo `200` em HTTPS, com certificado válido para o nome exato: `evento`, `cafe`, `api-cafe`, `eventos` e `api` — e `http://` redirecionando com `301` em todos.
- `sudo ss -tlnp` mostra os dois processos Node em `127.0.0.1` (portas `3000` e `3001`) e o MySQL em `127.0.0.1`; `sudo ufw status` lista apenas OpenSSH e Nginx Full.
- `pm2 ls` mostra os dois processos `online`, e um `sudo reboot` traz os cinco endereços de volta sem nenhuma intervenção.
- Cada API só aceita a origem do seu próprio front no CORS: provado com seis `curl -H "Origin: …"` (dois por API, um permitido e um negado).
- `sudo certbot certificates` lista os certificados cobrindo os cinco nomes, e `sudo certbot renew --dry-run` passa.
- Um `INFRAESTRUTURA.md` no repositório com: tabela de subdomínio → projeto → pasta ou porta, os arquivos do nginx comentados, os comandos de publicação de cada projeto e o procedimento de recuperação ("o servidor pegou fogo; como refazer tudo em uma máquina nova").
- Um teste de carga simples em um dos endereços estáticos, com o resultado anotado — e uma frase dizendo o que quebraria primeiro se o tráfego decuplicasse.

<details><summary>Pistas</summary>

1. Cinco registros `A` para o mesmo IP (Capítulo 04 §4.4). Confirme todos com `dig +short … @1.1.1.1` **antes** de rodar o `certbot`, e emita tudo num comando só: `sudo certbot --nginx -d evento.seudominio.dev -d cafe.seudominio.dev -d api-cafe.seudominio.dev -d eventos.seudominio.dev -d api.seudominio.dev`.
2. Duas APIs na mesma máquina precisam de portas diferentes. Defina `PORT` no `env` de cada app do `ecosystem.config.cjs` e confira com `sudo ss -tlnp` antes de configurar o nginx.
3. Um arquivo de `server` por subdomínio em `sites-available` deixa o diagnóstico muito mais fácil do que um arquivo gigante. Repita a §7.2 para os três estáticos e a §7.3 para as duas APIs, mudando `server_name`, `root` e a porta do `proxy_pass`.
4. Para o teste de carga, `ab -n 500 -c 20 https://evento.seudominio.dev/` (pacote `apache2-utils`) ou `curl` em laço. Olhe `htop` durante o teste: o que satura primeiro, CPU, memória ou rede?
5. O procedimento de recuperação fica muito mais curto se você anotar os comandos enquanto executa, em vez de tentar lembrar depois. É exatamente esse arquivo que o Capítulo 07 vai transformar em `Dockerfile` e o Capítulo 09, em automação.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `Permission denied (publickey)` ao conectar | chave não instalada no usuário certo, ou permissões erradas em `~/.ssh` | `ssh-copy-id`; no servidor, `chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys`; diagnostique com `ssh -v` |
| `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!` | o servidor foi recriado e tem outra chave de host | confirme que foi você quem recriou e rode `ssh-keygen -R 203.0.113.10` |
| Perdeu o acesso logo depois de `sudo ufw enable` | firewall ligado sem liberar o OpenSSH antes | console de emergência no painel do provedor; `sudo ufw allow OpenSSH` |
| `PasswordAuthentication no` não faz efeito | um `50-cloud-init.conf` em `sshd_config.d` vem antes e vence | renomeie o seu arquivo para `00-…`; confira com `sudo sshd -T \| grep -i password` |
| `nginx: [emerg] bind() to 0.0.0.0:80 failed (98: Address already in use)` | outro processo (Apache, outro nginx) já ocupa a porta 80 | `sudo ss -tlnp \| grep :80`; remova o Apache ou pare o processo |
| `nginx: [emerg] conflicting server name "api.seudominio.dev"` | dois arquivos habilitados com o mesmo `server_name` | apague o link duplicado em `sites-enabled` e recarregue |
| `502 Bad Gateway` e, no `error.log`, `connect() failed (111: Connection refused) while connecting to upstream` | o processo Node não está rodando, ou está em outra porta | `pm2 ls`; `sudo ss -tlnp \| grep 3000`; compare com o `proxy_pass` |
| `403 Forbidden` em site estático e, no `error.log`, `Permission denied` | o usuário `www-data` não consegue atravessar as pastas até o arquivo | publique em `/var/www/...`, não em `/home/deploy/...`; `chmod 755` nas pastas |
| `ERROR 1045 (28000): Access denied for user 'unieventos'@'localhost' (using password: YES)` | senha errada no `.env`, ou usuário criado com outro `host` | `SELECT user, host FROM mysql.user;`; recrie com `ALTER USER … IDENTIFIED BY …` |
| API: `Error: connect ECONNREFUSED 127.0.0.1:3306` | MySQL parado, ou `DB_HOST` apontando para o lugar errado | `sudo systemctl status mysql`; `DB_HOST=127.0.0.1` |
| Serviço systemd não sobe: `status=203/EXEC` | `ExecStart` sem caminho absoluto, ou Node instalado via nvm | `which node` e use o caminho completo (`/usr/bin/node`) |
| Editou o `.service` e nada mudou | o systemd usa a cópia carregada em memória | `sudo systemctl daemon-reload` e depois `restart` |
| Depois do reboot, o site voltou mas a API não | faltou `pm2 startup` (a linha `sudo env PATH=…`) ou `pm2 save` | refaça os dois e teste com `sudo reboot` |
| `certbot`: `Challenge failed for domain … Invalid response … 404` | o DNS ainda não resolve para este servidor, ou a porta 80 está fechada | `dig +short nome @1.1.1.1`; `sudo ufw status`; `curl -I http://nome` |
| `413 Request Entity Too Large` ao enviar imagem | limite padrão de corpo do nginx (1 MB) | `client_max_body_size 5m;` no `server` e `reload` |
| `rsync` apagou arquivos que você queria manter | `--delete` sincroniza destruindo o que não está na origem | use `--dry-run` antes; e nunca `--delete` numa pasta que recebe uploads |

## 🏠 Para praticar depois da aula (1 h)

No seu **projeto autoral** (ou no projeto do grupo, no laboratório da disciplina):

1. Publique o front e a API no servidor, seguindo o Passo a passo (ou a §11, se estiver usando `gN@ivanpires.dev`).
2. Garanta que a API escuta apenas em `127.0.0.1` e que o nginx é a única porta de entrada. Comprove com `sudo ss -tlnp`.
3. Escreva um `PUBLICAR.md` na raiz do repositório com o procedimento completo de publicação: os comandos exatos, na ordem, com o que se espera ver depois de cada um.
4. Registre no mesmo arquivo uma seção **"Se der errado"** com três problemas que você enfrentou e como diagnosticou cada um (o comando que revelou a causa, não só a solução).

**Critério de pronto:** o endereço público responde em HTTPS, sem erro no console do navegador; `sudo ss -tlnp` mostra o Node em loopback; e um colega consegue publicar uma alteração seguindo apenas o seu `PUBLICAR.md`, sem fazer perguntas.

**Guarde no seu repositório:** commit + push, com a URL pública na descrição.

## ✅ Está no ar quando…

- [ ] `ssh meuvps` entra sem pedir senha, e `ssh -o PubkeyAuthentication=no meuvps` é recusado.
- [ ] `sudo ufw status` lista apenas OpenSSH e Nginx Full; `sudo sshd -T | grep -i permitrootlogin` responde `no`.
- [ ] `sudo ss -tlnp` mostra o nginx em `0.0.0.0:80` e `0.0.0.0:443`, o Node em `127.0.0.1:3000` e o MySQL em `127.0.0.1:3306`.
- [ ] `curl -I https://eventos.seudominio.dev` devolve `200`, e `curl -I http://eventos.seudominio.dev` devolve `301` para HTTPS.
- [ ] `curl -s https://api.seudominio.dev/api/saude` responde `{"status":"ok"}` com `ambiente` igual a `production`.
- [ ] `pm2 ls` mostra a API `online`; depois de `sudo reboot`, tudo volta sem intervenção.
- [ ] `sudo certbot certificates` lista os certificados com validade futura e `sudo certbot renew --dry-run` passa sem erro.
- [ ] `rsync -avz --delete dist/ meuvps:/var/www/...` publica uma alteração do front e você a vê no navegador depois de um `Ctrl+F5`.
- [ ] No laboratório da disciplina, `https://ivanpires.dev/dsw/gN/` abre o seu projeto, com o front carregando de `~/frontend` e a API respondendo em `/dsw/gN/api/`.
- [ ] Você tem um `PUBLICAR.md` que permite repetir tudo sem consultar este capítulo.

## 📚 Para aprofundar

- Ubuntu Server — documentação oficial: <https://documentation.ubuntu.com/server/> — instalação, OpenSSH, `ufw` e serviços, direto da fonte.
- DigitalOcean — "Initial Server Setup with Ubuntu": <https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-22-04> — o roteiro clássico da §4, passo a passo e em detalhe.
- OpenSSH — manual do `sshd_config`: <https://man.openbsd.org/sshd_config> — a referência de cada diretiva, incluindo a regra do "primeiro valor vence".
- nginx — "Beginner's Guide": <https://nginx.org/en/docs/beginners_guide.html> — e o guia de proxy reverso: <https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/>.
- nginx — referência do `ngx_http_proxy_module`: <https://nginx.org/en/docs/http/ngx_http_proxy_module.html> — `proxy_pass`, a regra da barra final e todos os `proxy_set_header`.
- MySQL 8 — "Securing the Initial MySQL Account" e `GRANT`: <https://dev.mysql.com/doc/refman/8.0/en/> — privilégios e usuários por host.
- pm2 — documentação: <https://pm2.keymetrics.io/docs/usage/quick-start/> — e "Startup Script": <https://pm2.keymetrics.io/docs/usage/startup/>.
- systemd — `systemd.service` e `systemd.exec`: <https://www.freedesktop.org/software/systemd/man/systemd.service.html> — o que cada diretiva da unidade faz.
- certbot — instruções para nginx no Ubuntu: <https://certbot.eff.org/instructions> — e Let's Encrypt, limites de emissão: <https://letsencrypt.org/docs/rate-limits/>.
- `rsync` — manual: <https://download.samba.org/pub/rsync/rsync.1> — a seção sobre a barra final na origem vale a leitura.
- SSL Labs — teste de servidor: <https://www.ssllabs.com/ssltest/> — para o desafio ⭐⭐, e para conferir qualquer site em produção.

No próximo capítulo, tudo o que você instalou na mão vira receita: o Docker empacota a `unieventos-api`, o MySQL e o site em contêineres que rodam idênticos no seu notebook e neste mesmo VPS — e você descobre por que "funciona na minha máquina" deixa de ser desculpa.
