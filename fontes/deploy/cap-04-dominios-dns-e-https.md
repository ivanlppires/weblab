# Capítulo 04 — Domínios, DNS e HTTPS

> **Deploy & Ferramentas** · Unidade 2: Publicação: estático, back-end, domínio e servidor
> WebLab · UNEMAT — Campus Sinop
> **Tempo estimado:** 2 a 3 h · estudo autônomo, em paralelo à sua trilha

## 🎯 Objetivos de aprendizagem

Ao final deste capítulo você será capaz de:

- Explicar, etapa por etapa, como o navegador transforma `evento.seudominio.dev` em um endereço IP, e o que TTL e "propagação" significam de verdade.
- Registrar um domínio (`.br` no Registro.br ou genérico em outro registrador), ler um WHOIS e separar os três papéis: registrador, provedor de DNS e hospedagem.
- Criar registros `A`, `AAAA`, `CNAME`, `TXT` e `MX`, escolhendo o tipo certo para cada situação.
- Apontar um domínio ou subdomínio para GitHub Pages, Netlify, Vercel ou um VPS, e diagnosticar o resultado com `dig`, `nslookup`, `host` e dnschecker.org.
- Descrever o que um certificado TLS prova, como a cadeia de confiança funciona e como a Let's Encrypt emite e renova certificados pelo protocolo ACME.
- Forçar HTTPS, ativar HSTS e usar a Cloudflare como DNS e proxy escolhendo o modo SSL correto.
- Reconhecer e corrigir os erros clássicos: `DNS_PROBE_FINISHED_NXDOMAIN`, certificado de outro domínio e conteúdo misto.

## 📋 Pré-requisitos

- [ ] Site do evento acadêmico (Nível 1) publicado no GitHub Pages ou Netlify (Capítulo 03), acessível em `https://<usuario>.github.io/<repositorio>/`.
- [ ] Terminal com `dig` (Ubuntu/Debian: `sudo apt install dnsutils`; macOS: já vem instalado; Windows: use o WSL ou o `nslookup`, que já vem no sistema).
- [ ] `curl` instalado (`curl --version`).
- [ ] Um domínio próprio — opcional, mas recomendado. A §2 mostra opções baratas e gratuitas para quem ainda não tem.

> No Capítulo 03 você publicou o site do evento em um endereço que a plataforma escolheu por você, algo como `usuario.github.io/site-evento`. Funciona, mas ninguém coloca isso num cartão de visita. Hoje o site ganha um nome próprio, com cadeado — e você entende tudo o que acontece entre a barra de endereço e o servidor.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 45 min | Como um nome vira IP; registrar um domínio; tipos de registro (§1 a §3) |
| 2 | 45 min | Apontar para cada hospedagem; diagnosticar com `dig`; HTTPS, Let's Encrypt, HSTS e Cloudflare (§4 a §8) |
| 3 | 60 min | Passo a passo: `evento.seudominio.dev` com HTTPS no GitHub Pages + Laboratório |

## 1. Como um nome vira um endereço IP

### 1.1 Anatomia de um nome

Leia um nome de domínio **da direita para a esquerda**. O nome completo de `evento.seudominio.dev` é, tecnicamente, `evento.seudominio.dev.` — com um ponto final que representa a **raiz** do DNS:

| Parte | Nome técnico | Quem controla |
|---|---|---|
| `.` (ponto final, invisível) | raiz | 13 grupos de servidores-raiz, coordenados pela IANA |
| `dev` | TLD (domínio de topo) | o operador do TLD (`.br` é do NIC.br; `.dev` é do Google) |
| `seudominio` | domínio registrado ("apex" ou "raiz do domínio") | você, enquanto pagar a anuidade |
| `evento` | subdomínio | você, sem pagar nada a mais |

Um domínio registrado dá direito a **quantos subdomínios você quiser**: `evento.seudominio.dev`, `cafe.seudominio.dev`, `api.cafe.seudominio.dev`. É por isso que um único domínio serve para publicar todos os projetos das trilhas.

### 1.2 Resolução recursiva, passo a passo

Quando você digita `evento.seudominio.dev` no navegador, ninguém tem a resposta pronta. O nome é resolvido por uma cadeia de perguntas:

```text
navegador ──► cache do navegador ──► cache do sistema (/etc/hosts, resolvedor local)
                                              │
                                              ▼
                                   resolvedor recursivo
                              (do provedor, 8.8.8.8, 1.1.1.1)
                                              │
        1. "quem cuida de .dev?"              ▼
        ◄────────────────────────── servidores-raiz (.)
        2. "quem cuida de seudominio.dev?"    ▼
        ◄────────────────────────── servidores do TLD .dev
        3. "qual o IP de evento.seudominio.dev?"
        ◄────────────────────────── servidores autoritativos do seu domínio
                                    (Registro.br, Cloudflare, Netlify DNS)
                                              │
                                              ▼
                              resposta: 185.199.108.153 (TTL 300)
```

Os papéis:

- **Resolvedor recursivo** (*recursive resolver*): o "assistente" que faz todas as perguntas em seu nome. Normalmente é o do seu provedor de internet, mas você pode configurar outro (`1.1.1.1` da Cloudflare, `8.8.8.8` do Google). Ele guarda as respostas em cache.
- **Servidores-raiz**: sabem apenas quem cuida de cada TLD. Nunca sabem o IP do seu site.
- **Servidores do TLD**: sabem quais são os **servidores autoritativos** (registros `NS`) de cada domínio registrado sob eles.
- **Servidores autoritativos**: os únicos que têm a resposta definitiva. É neles que você edita registros. Quem hospeda esses servidores é o seu **provedor de DNS** — pode ser o registrador (Registro.br oferece de graça), a Cloudflare ou a própria hospedagem.

A analogia clássica: você quer o endereço de uma pessoa. Pergunta à recepção do prédio (resolvedor). A recepção liga para a lista nacional (raiz), que indica a lista do estado (TLD), que indica a prefeitura da cidade (autoritativo), que finalmente sabe a rua e o número. Da próxima vez, a recepção já lembra — por um tempo.

### 1.3 TTL, cache e a tal "propagação"

Cada registro DNS carrega um **TTL** (*time to live*), em segundos: por quanto tempo um resolvedor pode guardar a resposta antes de perguntar de novo. TTL 3600 significa "confie nesta resposta por uma hora".

É daí que vem a "propagação". **DNS não propaga nada** — não existe um sinal que sai do seu servidor e se espalha pelo mundo. O que acontece é o oposto: milhares de resolvedores guardam a resposta antiga até o TTL dela expirar. Se o TTL era 86400 (um dia), alguém que acessou o site ontem à noite pode continuar vendo o IP antigo por até um dia inteiro.

Regra prática:

1. **Antes** de mudar um registro importante, reduza o TTL para 300 (5 minutos) e espere o TTL antigo expirar.
2. Faça a mudança.
3. Confirmado que funcionou, suba o TTL de volta para 3600 ou mais — TTL alto alivia os servidores autoritativos e acelera o acesso.

Existe também o **cache negativo**: se você consulta um nome que **ainda não existe** e só depois cria o registro, o resolvedor pode lembrar do "não existe" por alguns minutos. Por isso, crie o registro **antes** de testar no navegador.

> **🧠 Você sabia?**
> Os "13 servidores-raiz" (nomeados de `a.root-servers.net` a `m.root-servers.net`) não são 13 máquinas: cada letra é replicada em centenas de locais pelo mundo com uma técnica chamada *anycast* — o mesmo IP é anunciado de vários pontos e sua consulta vai para o mais próximo. O Brasil hospeda dezenas dessas cópias, várias mantidas pelo NIC.br. E o TLD `.dev` tem uma peculiaridade: ele inteiro está na lista de *HSTS preload* dos navegadores, então **todo** site `.dev` só abre por HTTPS. Não existe `http://alguma-coisa.dev`.

> **🔬 Investigue**
> Rode `dig +trace weblab.ivanpires.dev` e conte quantos "saltos" aparecem: raiz, `.dev`, autoritativo. Em seguida rode `dig weblab.ivanpires.dev` duas vezes seguidas e compare o número na coluna do TTL (a segunda coluna da seção `ANSWER SECTION`). Ele diminui entre uma consulta e outra? Isso é o cache do resolvedor contando o tempo restante.

## 2. Registrando um domínio

### 2.1 Registro.br: domínios `.br`

O **Registro.br** (<https://registro.br>) é o registrador oficial de tudo que termina em `.br`, operado pelo NIC.br, sem fins lucrativos. Para desenvolvedores, as categorias mais usadas são `.com.br`, `.dev.br`, `.app.br`, `.tec.br` e `.eng.br`.

O que você precisa saber:

- É preciso um **CPF ou CNPJ** válido. Pessoa física pode registrar.
- O preço fica na faixa de **algumas dezenas de reais por ano** (confira o valor atual no site — ele é o mesmo para quase todas as categorias). Pagamento por Pix ou boleto.
- O Registro.br **hospeda o DNS de graça**: depois de registrar, você edita registros `A`, `CNAME`, `TXT` e `MX` direto no painel, sem contratar nada.
- O domínio é seu enquanto você renovar. Deixou vencer, ele passa por um período de carência e depois **volta a ficar disponível para qualquer pessoa**. Ative a renovação automática.

### 2.2 Domínios genéricos: `.dev`, `.com`, `.app`

Para TLDs genéricos, qualquer **registrador credenciado** serve. Três com boa reputação entre desenvolvedores: **Cloudflare Registrar** (vende a preço de custo, mas exige que o DNS fique na Cloudflare), **Porkbun** e **Namecheap**. Um `.dev` custa por volta de uma dezena de dólares por ano.

Cuidado com dois truques comuns: o preço promocional do **primeiro ano** (a renovação pode custar o dobro) e a "proteção WHOIS" vendida à parte — na maioria dos registradores modernos ela já vem inclusa.

### 2.3 Sem dinheiro para um domínio? Opções para estudar

Duas alternativas mantidas pela comunidade, boas para laboratório e ruins para entregar a um cliente:

- **is-a.dev** (<https://is-a.dev>): subdomínios gratuitos `seunome.is-a.dev`, obtidos abrindo um *pull request* com um arquivo JSON no repositório do projeto — um ótimo exercício depois do Capítulo 02. Aceita `CNAME` para GitHub Pages e registros `A`.
- **DuckDNS** (<https://www.duckdns.org>): subdomínios `seunome.duckdns.org` apontando para um IP que você pode atualizar por uma URL — útil para um VPS ou até para a sua máquina em casa.

Se você usar uma delas, troque `seudominio.dev` por `seunome.is-a.dev` em todos os exemplos deste capítulo.

### 2.4 WHOIS: a certidão do domínio

Todo domínio tem uma ficha pública, o **WHOIS**, com registrador, datas de criação e expiração e servidores de nome. Dados de contato hoje costumam vir ocultos (LGPD e GDPR), mas o essencial continua visível:

```bash
sudo apt install whois        # Ubuntu/Debian; no macOS já vem
whois registro.br
whois ivanpires.dev
```

Procure na saída as linhas `expires`/`Registry Expiry Date` (quando vence) e `nserver`/`Name Server` (quem responde pelo domínio). É a forma mais rápida de descobrir **onde** o DNS de um domínio está hospedado antes de sair procurando painel.

### 2.5 Três papéis que não se confundem

| Papel | O que faz | Exemplos |
|---|---|---|
| **Registrador** | vende o nome e diz ao TLD quais são os servidores `NS` | Registro.br, Cloudflare Registrar, Porkbun |
| **Provedor de DNS** | hospeda a zona: os registros `A`, `CNAME`, `TXT` | DNS do Registro.br, Cloudflare, Netlify DNS |
| **Hospedagem** | guarda e serve os arquivos ou roda o processo | GitHub Pages, Netlify, Render, um VPS |

Os três podem ser a mesma empresa ou três diferentes. O erro mais comum de iniciante é editar registros no painel do registrador quando os `NS` apontam para outro provedor — a edição simplesmente não tem efeito. Antes de mexer em qualquer registro, rode `dig +short seudominio.dev NS` e confirme quem está respondendo.

## 3. Os tipos de registro que você vai usar

Uma **zona** DNS é o conjunto de registros de um domínio. Cada registro tem nome, tipo, valor e TTL. Estes cinco tipos resolvem 95% do dia a dia:

| Tipo | Guarda | Exemplo de valor | Use para |
|---|---|---|---|
| `A` | endereço IPv4 | `203.0.113.10` | apontar para um VPS ou para os IPs fixos de uma plataforma |
| `AAAA` | endereço IPv6 | `2606:50c0:8000::153` | o mesmo que `A`, em IPv6 |
| `CNAME` | outro **nome** (apelido) | `usuario.github.io.` | apontar um subdomínio para um serviço cujo IP pode mudar |
| `TXT` | texto livre | `google-site-verification=abc123` | provar posse do domínio, SPF de e-mail, desafio ACME |
| `MX` | servidor de e-mail + prioridade | `10 mail.provedor.com.` | receber e-mail no domínio |

Dois tipos que você vai **ver**, mas raramente editar: `NS` (quais servidores são autoritativos — definido no registrador) e `CAA` (quais autoridades certificadoras podem emitir certificado para o domínio — uma camada extra de segurança).

Uma zona típica de estudante, no formato de arquivo de zona (é assim que o `dig` mostra as respostas):

```text
; zona seudominio.dev
seudominio.dev.            3600  IN  A      185.199.108.153
seudominio.dev.            3600  IN  A      185.199.109.153
seudominio.dev.            3600  IN  A      185.199.110.153
seudominio.dev.            3600  IN  A      185.199.111.153
www.seudominio.dev.        3600  IN  CNAME  usuario.github.io.
evento.seudominio.dev.      300  IN  CNAME  usuario.github.io.
cafe.seudominio.dev.        300  IN  CNAME  cafe-cerrado.netlify.app.
api.seudominio.dev.         300  IN  A      203.0.113.10
seudominio.dev.            3600  IN  MX     10 mail.provedor.com.
seudominio.dev.            3600  IN  TXT    "v=spf1 include:_spf.provedor.com ~all"
_acme-challenge.seudominio.dev. 60 IN TXT   "gfj9Xq_Lr3V0w2cZ4pAyT8mHq"
```

Repare no **ponto final** depois de `usuario.github.io.` — em arquivos de zona ele indica nome absoluto. Nos painéis web, normalmente você digita sem o ponto e o painel cuida disso.

Um `CNAME` diz "para saber o IP deste nome, consulte aquele outro nome". Quando o GitHub troca os IPs do Pages, `usuario.github.io` passa a resolver para os novos endereços e o seu `CNAME` continua válido sem que você faça nada. É por isso que as plataformas pedem `CNAME` para subdomínios.

> **⚠️ Atenção**
> **`CNAME` não pode ficar no apex** (`seudominio.dev` sem nada na frente) nem coexistir com outros registros no mesmo nome — é uma regra do protocolo, porque o apex sempre tem `NS` e `SOA`. Para o apex, use registros `A`/`AAAA` com os IPs fixos que a plataforma publica, ou um provedor de DNS que ofereça `ALIAS`/"CNAME flattening" — o Cloudflare (que faz o *flattening*) e o Netlify DNS oferecem; o DNS do Registro.br, não. Painéis que "aceitam" um `CNAME` no apex costumam quebrar o e-mail do domínio.

## 4. Apontando o domínio para cada hospedagem

### 4.1 GitHub Pages

Para um **subdomínio** (`evento.seudominio.dev`): um único registro `CNAME` apontando para `<usuario>.github.io` — **sem** o nome do repositório. O GitHub descobre qual repositório servir pelo arquivo `CNAME` que fica na raiz do site publicado.

Para o **apex** (`seudominio.dev`): quatro registros `A` (e, opcionalmente, quatro `AAAA`) com os IPs fixos do GitHub Pages:

```text
A     185.199.108.153
A     185.199.109.153
A     185.199.110.153
A     185.199.111.153
AAAA  2606:50c0:8000::153
AAAA  2606:50c0:8001::153
AAAA  2606:50c0:8002::153
AAAA  2606:50c0:8003::153
```

Depois do DNS, no repositório: **Settings → Pages → Custom domain**, digite o nome e salve. O GitHub cria um commit com o arquivo `CNAME` na raiz do site, verifica o DNS ("DNS check successful"), emite um certificado Let's Encrypt e, minutos depois, libera a caixa **Enforce HTTPS**. Marque-a.

Duas armadilhas:

- Se o site é gerado por GitHub Actions (um projeto Vite, por exemplo), o arquivo `CNAME` precisa estar **na saída do build**. No Vite, coloque-o em `public/CNAME` — tudo em `public/` é copiado para `dist/`.
- Com domínio próprio, o site sai de `usuario.github.io/site-evento/` e passa a viver na **raiz** `evento.seudominio.dev/`. Links absolutos como `/site-evento/css/estilo.css` quebram; links relativos (`css/estilo.css`) continuam funcionando. Se o projeto é Vite, volte `base` para `'/'`.

### 4.2 Netlify

No painel do site: **Domain management → Add a domain**. Para subdomínio, a Netlify pede um `CNAME` para `<nome-do-site>.netlify.app`. Para o apex, ou você delega o DNS inteiro para a Netlify (ela vira seu provedor de DNS) ou cria um `A` para o balanceador `75.2.60.5` — o painel mostra o valor atual. O certificado é emitido automaticamente pela Let's Encrypt; em **HTTPS**, ative **Force HTTPS**.

### 4.3 Vercel

No projeto: **Settings → Domains → Add**. Subdomínio: `CNAME` para `cname.vercel-dns.com`. Apex: registro `A` para `76.76.21.21`. A Vercel valida o DNS na própria tela (fica verde quando resolve), emite o certificado sozinha e já redireciona HTTP para HTTPS.

### 4.4 Um VPS (servidor próprio)

Aqui não existe mágica: um registro `A` com o IP público do servidor (e um `AAAA` se ele tiver IPv6). O certificado passa a ser **responsabilidade sua** — é o que o `certbot` faz no Capítulo 06.

A vantagem do VPS aparece agora: **vários subdomínios podem apontar para o mesmo IP** (`cafe.seudominio.dev`, `eventos.seudominio.dev`, `api.seudominio.dev`, todos `A → 203.0.113.10`) e o nginx decide qual site servir pelo cabeçalho `Host` da requisição. Um servidor, N projetos.

> **💡 Dica**
> Adote a convenção **um subdomínio por projeto**: `evento.seudominio.dev` para o site do Nível 1, `cafe.seudominio.dev` para o Café Cerrado, `eventos.seudominio.dev` para o UniEventos. Subdomínios são grátis, isolam cookies e certificados por projeto e ficam apresentáveis no portfólio. Enquanto configura, use TTL 300 em tudo; quando estabilizar, suba para 3600.

## 5. Ferramentas de diagnóstico

### 5.1 `dig`: a ferramenta principal

```bash
dig evento.seudominio.dev                  # consulta A (padrão), saída completa
dig +short evento.seudominio.dev           # só a resposta
dig +short evento.seudominio.dev CNAME     # um tipo específico
dig +short seudominio.dev NS               # quem é autoritativo
dig +short seudominio.dev MX
dig +short seudominio.dev TXT
dig @1.1.1.1 +short evento.seudominio.dev  # pergunta a um resolvedor específico
dig +trace evento.seudominio.dev           # o caminho completo desde a raiz
dig +noall +answer evento.seudominio.dev   # só a seção ANSWER, com TTL
dig -x 185.199.108.153                     # reverso: de IP para nome
```

Anatomia de uma resposta completa:

```text
;; QUESTION SECTION:
;evento.seudominio.dev.         IN      A

;; ANSWER SECTION:
evento.seudominio.dev.  300     IN      CNAME   usuario.github.io.
usuario.github.io.      3600    IN      A       185.199.108.153
usuario.github.io.      3600    IN      A       185.199.109.153
usuario.github.io.      3600    IN      A       185.199.110.153
usuario.github.io.      3600    IN      A       185.199.111.153

;; Query time: 24 msec
;; SERVER: 127.0.0.53#53(127.0.0.53)
```

Leia: o nome é um `CNAME` para `usuario.github.io`, que por sua vez tem quatro `A`. A segunda coluna é o TTL restante. A linha `SERVER` diz **quem respondeu** — `127.0.0.53` é o cache local do Ubuntu, não a internet. Para ignorar caches locais, pergunte direto a um resolvedor público com `@1.1.1.1`.

A comparação decisiva quando "no meu computador funciona e no do colega não":

```bash
dig +short evento.seudominio.dev @1.1.1.1
dig +short evento.seudominio.dev @8.8.8.8
dig +short evento.seudominio.dev @ns1.registro.br    # direto no autoritativo (troque pelo seu NS)
```

Se o autoritativo já responde certo e os públicos ainda não, é TTL — espere. Se o autoritativo responde errado, o registro está errado ou você editou a zona no provedor errado (§2.5).

### 5.2 `nslookup` e `host`

`nslookup` existe em todo Windows; `host` é um atalho curto no Linux/macOS:

```bash
nslookup evento.seudominio.dev
nslookup -type=CNAME evento.seudominio.dev 8.8.8.8
host evento.seudominio.dev
host -t MX seudominio.dev
host -a seudominio.dev          # tudo o que conseguir
```

### 5.3 Caches locais e dnschecker.org

Quando o `dig @1.1.1.1` já responde certo e o navegador insiste no erro, o problema está nos caches da sua máquina:

```bash
resolvectl flush-caches         # Ubuntu (systemd-resolved)
sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder   # macOS
ipconfig /flushdns              # Windows (PowerShell/cmd)
```

O Chrome tem cache próprio: `chrome://net-internals/#dns` → **Clear host cache**.

Para ver o mundo de uma vez, use <https://dnschecker.org>: digite o nome, escolha o tipo e veja o que resolvedores de dezenas de países estão respondendo. É a ferramenta certa para responder "já propagou?" com dados em vez de achismo.

## 6. HTTPS: o que o cadeado prova

### 6.1 Certificado, chaves e o que ele garante

HTTPS é HTTP dentro de um túnel **TLS**. O túnel garante três coisas: **confidencialidade** (ninguém no meio lê), **integridade** (ninguém no meio altera) e **autenticidade** (você está falando com o dono do nome, não com um impostor). O certificado serve à terceira.

Um certificado é um documento assinado contendo:

- o **nome** (ou nomes) que ele cobre — no campo *Subject Alternative Name*, como `evento.seudominio.dev`; um certificado **curinga** `*.seudominio.dev` cobre um nível de subdomínio, e só um;
- a **chave pública** do servidor (a privada fica só no servidor e nunca sai de lá);
- quem **emitiu** (a autoridade certificadora, CA) e o período de validade;
- a **assinatura** da CA sobre tudo isso.

O que o cadeado prova, então: **que o servidor com quem você fala tem a chave privada correspondente a um certificado que uma CA confiável emitiu para exatamente este nome**. Só isso. Ele não prova que o site é honesto, que a loja entrega, que a API não tem bugs. Um site de golpe pode ter cadeado — e hoje quase todos têm.

### 6.2 Cadeia de confiança

O navegador não conhece a Let's Encrypt diretamente. Ele conhece um conjunto pequeno de **raízes** instaladas no sistema operacional. A confiança é uma corrente:

```text
ISRG Root X1  (raiz; está no seu sistema; chave guardada off-line)
     └── assina ► intermediária da Let's Encrypt  (renovada periodicamente)
                       └── assina ► evento.seudominio.dev  (o seu, o "folha")
```

Ao conectar, o servidor envia **o certificado folha e a intermediária** (por isso o `certbot` gera um `fullchain.pem`). O navegador verifica cada assinatura até chegar em uma raiz que ele já tem. Faltou a intermediária? Alguns navegadores buscam sozinhos e funcionam; `curl`, Android antigo e clientes Node falham com `unable to get local issuer certificate`. É um bug clássico de "funciona no Chrome, quebra no app".

### 6.3 Let's Encrypt e o protocolo ACME

A **Let's Encrypt** é uma CA gratuita e automatizada, mantida pela ISRG. Antes dela, certificado custava dinheiro e envolvia formulários; hoje é um comando. Seus certificados valem **90 dias** — de propósito, para forçar automação.

A emissão segue o protocolo **ACME**: um cliente (o `certbot`, por exemplo) pede um certificado e a CA responde com um **desafio** para provar que você controla o nome:

| Desafio | Como você prova | Precisa de |
|---|---|---|
| `HTTP-01` | servir um arquivo em `http://seudominio/.well-known/acme-challenge/<token>` | porta 80 aberta e DNS já apontando |
| `DNS-01` | criar um `TXT` em `_acme-challenge.seudominio` com o valor pedido | acesso ao DNS (manual ou por API) |
| `TLS-ALPN-01` | responder na porta 443 com um certificado temporário especial | porta 443, sem porta 80 |

`HTTP-01` é o padrão e o que o GitHub Pages, a Netlify e o `certbot --nginx` usam. `DNS-01` é o único que emite **curingas** (`*.seudominio.dev`), porque não dá para servir um arquivo em "todos os subdomínios".

A Let's Encrypt tem limites: cerca de 50 certificados por domínio registrado por semana e 5 certificados **idênticos** por semana. Enquanto testa, use `--dry-run` (ambiente de homologação) para não gastar cota.

### 6.4 `certbot` e renovação automática

O `certbot` é o cliente ACME recomendado pela própria Let's Encrypt. Em um VPS com nginx, o fluxo inteiro é:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d evento.seudominio.dev
sudo certbot renew --dry-run     # simula a renovação: se passar, a automática vai passar
sudo certbot certificates        # lista o que está instalado e quando vence
```

O pacote instala um **timer do systemd** (`certbot.timer`) que roda duas vezes por dia e renova qualquer certificado com menos de 30 dias de validade. Os arquivos ficam em `/etc/letsencrypt/live/<dominio>/fullchain.pem` e `privkey.pem`. Você vai fazer isso de verdade no Capítulo 06; nas plataformas gerenciadas (Pages, Netlify, Vercel, Render) tudo isso acontece por você.

### 6.5 HSTS: proibindo o HTTP de vez

Mesmo com redirecionamento de `http://` para `https://`, a **primeira** requisição de um visitante ainda pode sair sem criptografia — e é nela que um ataque de *downgrade* age. O cabeçalho **HSTS** fecha essa brecha:

```text
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

Ele diz ao navegador: "por um ano, nem tente HTTP neste domínio (e nos subdomínios)". A partir da segunda visita, o navegador reescreve `http://` para `https://` antes de qualquer conexão. A diretiva `preload` permite inscrever o domínio em <https://hstspreload.org> — uma lista embutida nos navegadores, que cobre até a primeira visita. É o que o TLD `.dev` inteiro tem.

Ative HSTS só quando **todos** os subdomínios já responderem em HTTPS: com `includeSubDomains`, um `blog.seudominio.dev` sem certificado fica inacessível por um ano nos navegadores que já viram o cabeçalho. E `preload` é, na prática, irreversível.

> **🔬 Investigue**
> Veja o certificado do WebLab pelo terminal e responda: para qual nome ele foi emitido, quem assinou e até quando vale?
>
> ```bash
> openssl s_client -connect weblab.ivanpires.dev:443 -servername weblab.ivanpires.dev </dev/null 2>/dev/null | openssl x509 -noout -subject -issuer -dates
> curl -sI https://weblab.ivanpires.dev | grep -i strict-transport
> ```
>
> Depois repita o `openssl` com `-servername` de um nome errado (por exemplo `-servername exemplo.com`) e observe que o servidor pode devolver **outro** certificado — é exatamente o que gera o erro `ERR_CERT_COMMON_NAME_INVALID` da §8.

## 7. Cloudflare: DNS e proxy na frente do site

A **Cloudflare** oferece, no plano gratuito, um provedor de DNS rápido e um **proxy reverso global**: quando o registro está com a "nuvem laranja" ligada, o `dig` devolve IPs da Cloudflare, não os do seu servidor. O visitante fala com a Cloudflare; a Cloudflare fala com a sua origem. Ganhos: cache de estáticos perto do usuário, proteção contra DDoS, ocultação do IP real do VPS, HTTPS "de graça" na borda.

Para usar: crie a conta, adicione o domínio, ela importa os registros existentes e pede que você troque os `NS` no registrador para os dois nomes que ela indicar (`algo.ns.cloudflare.com`). A partir daí, todo registro tem duas opções: **Proxied** (laranja) ou **DNS only** (cinza).

### 7.1 Os modos SSL/TLS

Aqui mora a decisão mais importante — e o erro mais comum. Em **SSL/TLS → Overview**:

| Modo | Visitante ↔ Cloudflare | Cloudflare ↔ seu servidor | Quando usar |
|---|---|---|---|
| Off | HTTP | HTTP | nunca |
| Flexible | HTTPS | **HTTP, sem criptografia** | nunca em produção |
| Full | HTTPS | HTTPS, aceita certificado autoassinado | servidor com certificado de origem da Cloudflare |
| Full (strict) | HTTPS | HTTPS, exige certificado válido | **o padrão a adotar** com Let's Encrypt ou certificado de origem |

Ative também **Always Use HTTPS** (redireciona na borda) e, em **Edge Certificates**, o **HSTS** — com a mesma cautela da §6.5.

> **⚠️ Atenção**
> O modo **Flexible** mostra cadeado ao visitante enquanto o tráfego entre a Cloudflare e o seu servidor viaja **em texto puro** pela internet. É segurança de fachada. Ele também gera o famoso `ERR_TOO_MANY_REDIRECTS`: seu nginx redireciona HTTP para HTTPS, a Cloudflare chega sempre por HTTP, o nginx redireciona de novo, para sempre. Use **Full (strict)**; se o servidor ainda não tem certificado, gere um com o `certbot` (Capítulo 06) ou instale o certificado de origem gratuito da Cloudflare.

Detalhes práticos com o proxy ligado:

- O seu servidor passa a ver o **IP da Cloudflare** como cliente. O IP real vem no cabeçalho `CF-Connecting-IP` (e em `X-Forwarded-For`). Isso importa para logs e limites de taxa no Capítulo 06.
- Para GitHub Pages, deixe o registro em **DNS only** até o GitHub emitir o certificado e liberar *Enforce HTTPS*; só então ligue o proxy, em Full (strict).
- Com o proxy, um subdomínio de API também passa pela Cloudflare — o cache não interfere em respostas JSON por padrão, mas o *timeout* de 100 segundos por requisição existe.

## 8. Erros clássicos, explicados

**`DNS_PROBE_FINISHED_NXDOMAIN`** — "este nome não existe" para o resolvedor que o seu navegador usa. Causas, da mais comum para a mais rara: erro de digitação no registro (`evento` vs `eventos`), registro criado no provedor de DNS errado (§2.5), TTL ainda não venceu, cache negativo por ter testado antes de criar. Diagnóstico: `dig +short nome @1.1.1.1` e `dig +short nome @<seu NS autoritativo>`.

**`NET::ERR_CERT_COMMON_NAME_INVALID`** — o servidor respondeu com um certificado que **não cobre** o nome digitado. Acontece quando você aponta `cafe.seudominio.dev` para um VPS cujo nginx só tem certificado para `evento.seudominio.dev` (ele entrega o certificado do site padrão), quando o GitHub Pages ainda não emitiu o certificado do domínio novo, ou quando `www.` foi esquecido no certificado. Diagnóstico: o comando `openssl` da §6.5 com `-servername` do nome problemático.

**`NET::ERR_CERT_AUTHORITY_INVALID`** — o certificado existe, mas foi assinado por alguém que o navegador não conhece: autoassinado (o "snakeoil" do Ubuntu), certificado de origem da Cloudflare exposto sem o proxy, ou cadeia incompleta.

**Mixed content** (conteúdo misto) — a página veio por HTTPS, mas pede um recurso por `http://`. O navegador **bloqueia** conteúdo ativo (scripts, `fetch`, iframes, CSS) e apenas **avisa** em conteúdo passivo (imagens, vídeos). Sintoma típico: site publicado com a API em `http://` e o console dizendo `Mixed Content: The page at 'https://…' was loaded over HTTPS, but requested an insecure resource 'http://…'. This request has been blocked`. Correção: use `https://` em tudo; enquanto migra, a meta-tag abaixo faz o navegador tentar HTTPS em todo recurso `http://` da página:

```html
<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
```

**`ERR_TOO_MANY_REDIRECTS`** — loop de redirecionamento, quase sempre Cloudflare em modo Flexible com um servidor que força HTTPS (§7.1).

**`ERR_SSL_PROTOCOL_ERROR`** ou `SSL_ERROR_RX_RECORD_TOO_LONG` — a porta 443 está respondendo **HTTP puro**: um `listen 443;` sem `ssl` no nginx, ou o certificado ainda não instalado.

## 🚀 Passo a passo — `evento.seudominio.dev` com HTTPS

O que vai ao ar: o site do evento acadêmico (Nível 1), já publicado no GitHub Pages no Capítulo 03, agora em um subdomínio seu, com certificado e HTTPS obrigatório. Troque `seudominio.dev` pelo seu domínio (ou por `seunome.is-a.dev`) e `usuario` pelo seu usuário do GitHub.

### Passo 1 — confirme o ponto de partida

```bash
curl -I https://usuario.github.io/site-evento/
```

Resultado esperado: `HTTP/2 200` e um cabeçalho `server: GitHub.com`. Se não, volte ao Capítulo 03.

### Passo 2 — descubra quem responde pelo seu domínio

```bash
dig +short seudominio.dev NS
```

Anote os servidores. É **nesse** provedor (Registro.br, Cloudflare, o painel do registrador) que você vai criar o registro. Se estiver na Cloudflare, mantenha o registro em **DNS only** por enquanto.

### Passo 3 — crie o registro `CNAME`

No painel de DNS, adicione:

```text
Tipo:   CNAME
Nome:   evento            (alguns painéis pedem o nome completo: evento.seudominio.dev)
Valor:  usuario.github.io
TTL:    300
```

Sem o nome do repositório no valor. Sem `https://`. Sem barra no final.

### Passo 4 — confira o DNS antes de mexer no GitHub

```bash
dig +short evento.seudominio.dev CNAME @1.1.1.1
dig +short evento.seudominio.dev A @1.1.1.1
```

Resultado esperado: a primeira consulta devolve `usuario.github.io.`; a segunda mostra a cadeia inteira — `usuario.github.io.` na primeira linha e, abaixo dele, os quatro IPs `185.199.108.153` a `185.199.111.153`. Se voltar vazio, espere alguns minutos e repita — e confira o Passo 2. Não abra o navegador ainda (cache negativo, §1.3).

### Passo 5 — informe o domínio ao GitHub

No repositório `site-evento`: **Settings → Pages → Custom domain** → digite `evento.seudominio.dev` → **Save**. O GitHub:

1. cria um commit adicionando o arquivo `CNAME` (com uma linha: `evento.seudominio.dev`) na raiz da branch publicada — faça `git pull` para trazê-lo;
2. mostra **"DNS check in progress"** e, em seguida, **"DNS check successful"**;
3. pede um certificado à Let's Encrypt. Isso leva de alguns minutos a, raramente, algumas horas.

Se o site é gerado por Actions, adicione você mesmo o arquivo `public/CNAME` ao projeto, com o nome do domínio, e faça commit.

### Passo 6 — corrija os caminhos

O site saiu de `/site-evento/` e agora vive na raiz. Abra os HTMLs e verifique links e `src`: `css/estilo.css` e `imagens/logo.png` (relativos) funcionam; `/site-evento/css/estilo.css` (absoluto com o nome do repositório) quebra. Ajuste, commit, push.

### Passo 7 — force HTTPS

Volte em **Settings → Pages**. Quando a caixa **Enforce HTTPS** ficar clicável, marque. Se ela aparecer desabilitada com a mensagem "Unavailable for your site because your domain is not properly configured", o certificado ainda não foi emitido — espere e recarregue.

### Passo 8 — se você usa Cloudflare

Só agora ligue o proxy (nuvem laranja) no registro `evento`, e confirme que **SSL/TLS** está em **Full (strict)** e **Always Use HTTPS** está ativo.

### Como conferir

```bash
curl -I https://evento.seudominio.dev
curl -I http://evento.seudominio.dev
openssl s_client -connect evento.seudominio.dev:443 -servername evento.seudominio.dev </dev/null 2>/dev/null | openssl x509 -noout -subject -issuer -dates
```

Resultado esperado:

- o primeiro `curl` devolve `HTTP/2 200` com `server: GitHub.com` (ou `server: cloudflare`, se o proxy estiver ligado);
- o segundo devolve `HTTP/1.1 301 Moved Permanently` com `location: https://evento.seudominio.dev/` (em um `.dev`, o navegador nem chega a fazer essa requisição, mas o `curl` faz);
- o `openssl` mostra `subject=CN = evento.seudominio.dev` e um `issuer` da Let's Encrypt, com `notAfter` cerca de 90 dias à frente;
- no navegador, o cadeado abre e mostra o certificado para o seu nome; a página não tem avisos de conteúdo misto no console;
- em <https://dnschecker.org>, o tipo `CNAME` de `evento.seudominio.dev` mostra `usuario.github.io` em todos os locais.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Para o nome `blog.cafe.seudominio.dev`, liste da direita para a esquerda: raiz, TLD, domínio registrado e subdomínios. Qual é o apex?

**A2.** Preveja antes de rodar: `dig +short www.github.com` devolve uma linha `CNAME` seguida de `A`, ou só `A`? Rode e explique a diferença para `dig +short github.com`.

**A3.** Um registro `A` tem TTL 86400 e você acabou de trocar o IP. No pior caso, quanto tempo um visitante que acessou o site ontem à noite pode continuar vendo o IP antigo? E se o TTL fosse 300? Por que a recomendação é baixar o TTL **antes** da mudança, e não durante?

**A4.** Verdadeiro ou falso: "um `CNAME` pode coexistir com um `MX` no mesmo nome". Justifique com a regra da §3 e diga o que acontece com o e-mail de quem coloca `CNAME` no apex.

**A5.** Complete: para apontar `api.seudominio.dev` para um VPS de IP `203.0.113.10`, o registro é do tipo `____`, nome `____`, valor `____`. E para apontar `docs.seudominio.dev` para um site na Vercel?

**A6.** Um site está atrás da Cloudflare em modo Flexible e mostra cadeado. Em qual trecho do caminho o tráfego viaja sem criptografia? Que erro aparece se o nginx da origem redireciona HTTP para HTTPS?

### Nível B — Aplicação

**B1.** Mapa DNS do WebLab. Usando só o terminal, descubra: os servidores `NS` de `ivanpires.dev`; para onde `weblab.ivanpires.dev` aponta (`CNAME` ou `A`, e os IPs); quem emitiu o certificado e até quando vale; se o site envia HSTS.

Resultado esperado: uma tabela de quatro linhas (NS · apontamento · certificado · HSTS) com o comando usado em cada uma.

<details><summary>Dica</summary>

`dig +short … NS`, `dig +noall +answer …`, o `openssl s_client` da §6.5 e `curl -sI … | grep -i strict`.
</details>

**B2.** Segundo subdomínio, segunda plataforma. Aponte `cafe.seudominio.dev` para o Café Cerrado estático publicado na Netlify (ou Vercel) no Capítulo 03 e force HTTPS.

Resultado esperado: `curl -I https://cafe.seudominio.dev` devolve `200` com `server: Netlify` (ou `server: Vercel`), e `curl -I http://cafe.seudominio.dev` devolve um redirecionamento `301`/`308` para `https://`.

<details><summary>Dica</summary>

Subdomínio é sempre `CNAME` — o valor está no painel da plataforma (`<site>.netlify.app` ou `cname.vercel-dns.com`). Adicione o domínio no painel **depois** que o `dig` já responder.
</details>

**B3.** Medindo a "propagação". Crie um registro `TXT` em `teste.seudominio.dev` com o valor `weblab-<seu-nome>` e TTL 60. Cronometre quanto tempo leva até cada um destes responder com o valor: `dig @1.1.1.1`, `dig @8.8.8.8`, `dig` sem `@` (o resolvedor do seu provedor) e o dnschecker.org. Depois **altere** o valor e meça de novo.

Resultado esperado: quatro tempos anotados para a criação e quatro para a alteração; uma frase explicando por que a alteração pode demorar mais que a criação, mesmo com TTL 60.

<details><summary>Dica</summary>

Use `watch -n 5 'dig +short teste.seudominio.dev TXT @8.8.8.8'` para não ficar repetindo o comando. Na alteração, quem já tinha a resposta em cache só pergunta de novo quando o TTL antigo expirar.
</details>

**B4.** Conteúdo misto plantado. No site do evento (publicado em HTTPS), adicione uma imagem carregada por `http://` e um `<script src="http://…">` de qualquer arquivo JS público. Abra o site, leia o console e anote qual dos dois foi bloqueado e qual só gerou aviso. Corrija com a meta-tag `upgrade-insecure-requests` e depois da forma definitiva.

Resultado esperado: as duas mensagens do console copiadas, a explicação "ativo × passivo" e o site sem nenhum aviso ao final.

<details><summary>Dica</summary>

Scripts são conteúdo ativo: bloqueados. Imagens são passivas: carregam com aviso. A meta-tag muda o comportamento; trocar o `http://` por `https://` remove o problema.
</details>

### Nível C — Desafio

**C1.** Cloudflare na frente do GitHub Pages. Migre os `NS` do seu domínio para a Cloudflare, mantenha `evento` em DNS only até o certificado do GitHub existir, depois ligue o proxy, escolha **Full (strict)**, ative **Always Use HTTPS** e **HSTS** (sem `preload`). Prove com `curl -I` que a resposta agora vem com `server: cloudflare` e com o cabeçalho `strict-transport-security`, e mostre com `dig` que os IPs retornados mudaram. Explique, em três linhas, por que o GitHub continua sabendo qual repositório servir mesmo com a Cloudflare no meio.

<details><summary>Dica</summary>

A Cloudflare repassa o cabeçalho `Host` original para a origem; é por ele (e pelo arquivo `CNAME`) que o GitHub Pages escolhe o site. O `dig` passa a devolver IPs `104.x` ou `172.x` da Cloudflare em vez dos `185.199.x` do GitHub.
</details>

## 🏆 Desafios

### ⭐ O caminho completo de um nome
Tags: dns, terminal, investigacao

Quantos servidores diferentes precisam ser consultados para que o seu navegador descubra o IP de `weblab.ivanpires.dev`? E de `www.unemat.br`? A resposta muda de um nome para outro — e o `dig +trace` mostra cada parada, com o nome do servidor que respondeu. Descubra o caminho dos dois nomes e explique as diferenças.

**Critérios de pronto**

- Saída do `dig +trace` dos dois nomes salva em um arquivo de texto, com as linhas de cada "salto" (raiz, TLD, autoritativo) marcadas por você.
- Uma lista com o nome de **um** servidor de cada nível consultado, para cada domínio.
- Resposta para: qual dos dois nomes envolve mais níveis de delegação, e por quê (pense em `.br` versus `.com.br`).
- Resposta para: por que o `+trace` demora mais que um `dig` comum, e por que o TTL não aparece diminuindo nele.

<details><summary>Pistas</summary>

1. Leia a seção *+trace* em `man dig`: ele ignora o resolvedor recursivo e faz as perguntas ele mesmo, começando pela raiz.
2. Cada bloco da saída termina com `;; Received … from <IP>#53(<nome>)` — esse é o servidor que respondeu naquele nível.
3. Compare o número de blocos: `unemat.br` passa pela raiz, pelo `.br` e pelo autoritativo da UNEMAT; veja se aparece um nível extra em algum dos casos.
4. Sem cache, o TTL mostrado é sempre o valor original configurado na zona.
</details>

### ⭐⭐ Um domínio, três hospedagens
Tags: dns, deploy, github, https

Um único domínio é suficiente para o portfólio inteiro do semestre: o apex para a sua página pessoal, um subdomínio para cada projeto, cada um em uma plataforma diferente. Monte essa estrutura de verdade: apex (`seudominio.dev`) no GitHub Pages com `A`/`AAAA`, `cafe.seudominio.dev` na Netlify ou Vercel com `CNAME`, e `api.seudominio.dev` com um registro `A` para um IP (o do VPS do Capítulo 06, ou um IP qualquer de teste, ou um DuckDNS).

**Critérios de pronto**

- `dig +noall +answer` dos três nomes salvos, mostrando os tipos corretos de registro em cada um (`A`/`AAAA` no apex, `CNAME` no subdomínio de plataforma, `A` no subdomínio de VPS).
- `curl -I https://seudominio.dev` e `curl -I https://cafe.seudominio.dev` devolvendo `200` com HTTPS forçado (o `http://` redireciona).
- `www.seudominio.dev` redireciona para o apex (ou o contrário) — sem erro de certificado em nenhum dos dois.
- Um `README.md` no repositório do site pessoal com a tabela de registros e a explicação de por que o apex **não** pôde usar `CNAME`.

<details><summary>Pistas</summary>

1. Os IPs do GitHub Pages para o apex estão na §4.1; o `www` é um `CNAME` para `usuario.github.io` e o GitHub cuida do redirecionamento se você cadastrar o apex como domínio principal.
2. Em cada plataforma, cadastre o domínio **só depois** de o `dig @1.1.1.1` responder certo — assim a verificação passa de primeira.
3. Se a caixa *Enforce HTTPS* não liberar, `dig` o nome de novo: certificado só é emitido quando o DNS resolve para a plataforma.
4. Para o registro `A` de `api`, qualquer IP funciona para o `dig`; o HTTPS dele fica para o Capítulo 06.
</details>

### ⭐⭐⭐ Certificado curinga com desafio DNS
Tags: https, dns, terminal, seguranca

Você tem dez subdomínios de projetos e não quer emitir dez certificados. Um certificado **curinga** `*.seudominio.dev` cobre todos — mas a Let's Encrypt só o emite pelo desafio `DNS-01`, porque não existe como "servir um arquivo em todos os subdomínios". Emita um curinga no seu próprio computador (não precisa de servidor), inspecione-o e explique o que ele cobre e o que não cobre.

**Critérios de pronto**

- Certificado emitido com `certbot certonly --manual --preferred-challenges dns` para `*.seudominio.dev` **e** `seudominio.dev` no mesmo pedido.
- Saída de `openssl x509 -noout -text -in fullchain.pem | grep -A1 "Subject Alternative Name"` mostrando os dois nomes.
- Resposta, testada com o `dig`, para: o registro `_acme-challenge` ainda precisa existir depois da emissão?
- Resposta para: o curinga cobre `api.cafe.seudominio.dev`? E `seudominio.dev` sozinho, se você não o tivesse incluído?
- Uma explicação de por que a renovação automática **não** vai funcionar com `--manual`, e o nome do plugin do `certbot` que resolveria isso para o seu provedor de DNS.

<details><summary>Pistas</summary>

1. Leia "Wildcard certificates" na documentação da Let's Encrypt e a página do `certbot` sobre o modo `--manual`.
2. O `certbot` vai imprimir um valor e pedir que você crie um `TXT` em `_acme-challenge.seudominio.dev`; confirme com `dig +short … TXT @1.1.1.1` **antes** de apertar Enter — se apertar antes, o desafio falha e você gasta cota. Comece com `--dry-run`.
3. Um curinga cobre exatamente um nível: `*.seudominio.dev` inclui `cafe.seudominio.dev`, mas não `api.cafe.seudominio.dev` nem o apex.
4. Existem plugins `python3-certbot-dns-cloudflare`, `dns-route53` e outros que criam o `TXT` via API; com eles a renovação vira automática.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `DNS_PROBE_FINISHED_NXDOMAIN` no navegador, mas o registro "está lá" no painel | Registro criado no provedor errado: os `NS` do domínio apontam para outro lugar (Cloudflare, Netlify DNS) | `dig +short seudominio.dev NS`; edite a zona **nesse** provedor |
| `dig @1.1.1.1` responde certo, o navegador insiste no erro | Cache do sistema ou do Chrome, ou cache negativo de um teste feito antes de criar o registro | `resolvectl flush-caches` (Ubuntu) e `chrome://net-internals/#dns` → Clear host cache |
| `NET::ERR_CERT_COMMON_NAME_INVALID` ao abrir o subdomínio novo | O servidor respondeu com o certificado de outro site: GitHub ainda não emitiu o certificado, ou o nginx do VPS não tem `server` para esse nome | No Pages, espere o *DNS check* e o *Enforce HTTPS*; no VPS, rode `certbot --nginx -d nome` |
| `NET::ERR_CERT_AUTHORITY_INVALID` | Certificado autoassinado, certificado de origem da Cloudflare acessado sem o proxy, ou intermediária faltando | Emita pela Let's Encrypt; no nginx use `fullchain.pem`, não `cert.pem` |
| `ERR_TOO_MANY_REDIRECTS` | Cloudflare em modo Flexible com origem que redireciona para HTTPS | SSL/TLS → **Full (strict)**; certifique a origem |
| Console: `Mixed Content: … requested an insecure resource 'http://…'. This request has been blocked` | Página HTTPS pedindo script, CSS ou `fetch` por `http://` | Troque para `https://`; provisoriamente, `<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">` |
| Painel diz "Enforce HTTPS: Unavailable for your site because your domain is not properly configured" | O `CNAME`/`A` ainda não resolve para o GitHub, ou o proxy da Cloudflare está ligado antes da emissão | Confira o `dig @1.1.1.1`; na Cloudflare, deixe DNS only até o certificado sair |
| Site abre em `evento.seudominio.dev`, mas sem CSS e imagens | Links absolutos com o nome do repositório (`/site-evento/css/…`) — o site agora está na raiz | Use caminhos relativos; em projetos Vite, `base: '/'` |
| `curl: (60) SSL certificate problem: unable to get local issuer certificate` | Servidor envia só o certificado folha, sem a intermediária | Configure `ssl_certificate` com `fullchain.pem` |
| `ERR_SSL_PROTOCOL_ERROR` | Porta 443 respondendo HTTP puro (`listen 443` sem `ssl`) | Rode o `certbot --nginx` ou adicione `ssl` e os caminhos do certificado |

## 🏠 Para praticar depois da aula (1 h)

No seu **projeto autoral** do Nível 1 (ou do nível que você está cursando), já publicado no Capítulo 03:

1. Escolha um subdomínio com o nome do projeto (`plantas.seudominio.dev`, `quadras.seudominio.dev`). Sem domínio próprio, use `seunome.is-a.dev`.
2. Crie o registro DNS correto para a plataforma onde o site está e cadastre o domínio nela.
3. Force HTTPS e elimine qualquer conteúdo misto.
4. Salve em um arquivo `dns.md` na raiz do repositório: a saída de `dig +noall +answer <nome>`, a saída de `curl -I https://<nome>` e a de `openssl x509 -noout -subject -issuer -dates` do certificado.

**Critério de pronto:** o site abre em `https://<subdominio>` com cadeado, `http://` redireciona, e o console do navegador não mostra avisos de conteúdo misto. O `dns.md` está commitado.

**Guarde no seu repositório:** commit + push, com a URL do site na descrição.

## ✅ Está no ar quando…

- [ ] `dig +short evento.seudominio.dev @1.1.1.1` devolve o alvo certo (`CNAME` da plataforma ou `A` do VPS) — e `@8.8.8.8` concorda.
- [ ] `curl -I https://evento.seudominio.dev` devolve `HTTP/2 200` (ou `HTTP/1.1 200`) sem erro de certificado.
- [ ] `curl -I http://evento.seudominio.dev` devolve `301`/`308` com `location: https://…`.
- [ ] `openssl s_client … | openssl x509 -noout -subject -dates` mostra o **seu** nome no `subject` e validade futura.
- [ ] O console do navegador não tem mensagens `Mixed Content`.
- [ ] Você sabe dizer, sem olhar, quem é o registrador, quem é o provedor de DNS e quem é a hospedagem do seu domínio.
- [ ] O TTL dos registros voltou para 3600 depois que tudo estabilizou.

## 📚 Para aprofundar

- Registro.br — <https://registro.br> — registro de domínios `.br`, painel de DNS e a seção de ajuda sobre tipos de registro.
- Cloudflare Learning Center, "What is DNS?" — <https://www.cloudflare.com/learning/dns/what-is-dns/> — a explicação mais didática da resolução recursiva, com animações.
- Documentação de DNS da Cloudflare — <https://developers.cloudflare.com/dns/> — registros, proxy, modos SSL/TLS e CNAME flattening.
- GitHub Docs, "Managing a custom domain for your GitHub Pages site" — <https://docs.github.com/pt/pages/configuring-a-custom-domain-for-your-github-pages-site> — os IPs oficiais e o passo a passo do `CNAME`.
- Netlify Docs, "Custom domains" — <https://docs.netlify.com/domains/> — e Vercel Docs, "Domains" — <https://vercel.com/docs/domains> — os valores exatos de cada plataforma.
- Let's Encrypt, "Como funciona" — <https://letsencrypt.org/pt-br/how-it-works/> — ACME, desafios e cadeia de confiança, em português.
- certbot — <https://certbot.eff.org> — instruções por sistema operacional e servidor web.
- MDN, "Strict-Transport-Security" — <https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Headers/Strict-Transport-Security> — e "Conteúdo misto" — <https://developer.mozilla.org/pt-BR/docs/Web/Security/Mixed_content>.
- dnschecker.org — <https://dnschecker.org> — e SSL Labs — <https://www.ssllabs.com/ssltest/> — para ver o seu domínio como o mundo o vê.

No próximo capítulo, o back-end sai da sua máquina: a API do Café Cerrado vai para o Render, com variáveis de ambiente, CORS restrito ao front publicado e um `/health` para provar que está viva.
