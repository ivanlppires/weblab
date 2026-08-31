# Aula 01 — Apresentação, tecnologias e arquitetura da Web

> **Nível 1 — Introdução ao Desenvolvimento Web** · Unidade 1: Arquitetura da Web e HTML
> WebLab · UNEMAT — Campus Sinop
> **Tempo estimado:** 3 blocos de 50 min + 1 h de prática

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Descrever como esta trilha funciona: unidades, marcos do projeto, projeto fio-condutor e projeto autoral.
- Distinguir Internet de World Wide Web e situar os principais marcos da história da Web.
- Explicar o modelo cliente-servidor e o papel do front-end e do back-end.
- Descrever, passo a passo, o que acontece entre digitar uma URL e ver a página renderizada.
- Decompor uma URL em suas seis partes e escrever caminhos relativos e absolutos corretos.
- Classificar arquiteturas web (camadas, estático × dinâmico, MPA × SPA) e apontar onde o front-end se encaixa.
- Configurar o ambiente de trabalho (VS Code, Live Server e DevTools) e criar o primeiro documento HTML.

## 📋 Pré-requisitos

Esta é a primeira aula: não há conteúdo anterior para retomar. Mas há o que trazer:

- [ ] Um notebook ou computador com **Google Chrome** ou **Firefox** atualizado.
- [ ] **Visual Studio Code** instalado (<https://code.visualstudio.com/>). Se ainda não instalou, faremos juntos no Bloco 3.
- [ ] Extensões do VS Code **Live Server** e **Prettier** (instalação na §1.6 desta aula).
- [ ] Uma pasta dedicada no computador para guardar os arquivos do curso (o Git chega na Aula 15).
- [ ] Uma ideia, mesmo vaga, de **tema para o seu projeto autoral** (ver §1.4). Você decide hoje.

Nenhuma experiência prévia com programação é exigida. Se você nunca escreveu uma linha de código, está no lugar certo — a trilha começa do zero.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Como esta trilha funciona (marcos do projeto, projeto fio-condutor e projeto autoral); Internet × Web; linha do tempo |
| 2 | 50 min | Cliente-servidor; o que acontece ao digitar uma URL; anatomia da URL; renderização; camadas, estático × dinâmico, MPA × SPA, APIs e REST |
| 3 | 50 min | Mão na massa: ambiente de trabalho, pasta do projeto, primeiro HTML e exploração do DevTools |

## 1. Como funciona esta trilha

### 1.1 O que esta trilha cobre

**Esta trilha cobre:** arquiteturas computacionais para Web; criação de páginas web com HTML, CSS e JavaScript.

**Objetivo geral:** ao final desta trilha, você projeta e desenvolve o **front-end** de aplicações web funcionais, acessíveis e responsivas, dominando as três tecnologias fundamentais da plataforma (HTML, CSS e JavaScript) e entendendo a arquitetura em que elas operam.

A palavra-chave é *front-end*: tudo que roda no navegador do usuário. Você vai entender o sistema completo (servidor, banco de dados, API), mas vai **construir** a parte que o usuário vê e toca. O back-end é assunto do Nível 2.

### 1.2 Três unidades, três marcos do projeto

| Unidade | Foco | Aulas | Marco do projeto |
|---|---|---|---|
| 1 | Arquitetura da Web e HTML | 01 a 05 | Marco 1 |
| 2 | CSS: estilo, layout e responsividade | 06 a 09 | Marco 2 |
| 3 | JavaScript e interatividade | 10 a 15 | Marco 3 |

Os três marcos incidem sobre **o mesmo site**: o Marco 1 constrói a estrutura em HTML, o Marco 2 aplica o design com CSS, o Marco 3 acrescenta o comportamento com JavaScript. Por isso é importante escolher hoje um tema que você aguente desenvolver até o fim da trilha.

### 1.3 A sequência das aulas

| Aula | Tema |
|---|---|
| 01 | Apresentação da trilha; tecnologias e arquitetura da Web |
| 02 | Introdução ao HTML: estrutura, textos, links, tabelas |
| 03 | Introdução ao formulário |
| 04 | Formulário, mídias e listas |
| 05 | Elementos HTML para layout e introdução ao CSS |
| 06 | CSS: sintaxe, seletores, classes, atributos e valores — Marco 1 do projeto |
| 07 | Formatando o layout de um website e o menu |
| 08 | Criando telas responsivas |
| 09 | Animações e efeitos em CSS |
| 10 | Introdução ao JavaScript — Marco 2 do projeto |
| 11 | Variáveis, operações aritméticas e estruturas de controle |
| 12 | Estruturas sequenciais, condicionais e de repetição |
| 13 | Funções e eventos |
| 14 | JavaScript para validação de formulários e consultas dinâmicas |
| 15 | Publicando seu website na internet — Marco 3 do projeto |

O conteúdo abaixo é o mesmo em qualquer oferta: serve igualmente a quem estuda por conta própria, sem data alguma, e a quem cursa esta trilha em uma turma com professor e calendário próprios — nesse caso, é o professor quem define as datas.

| Marco | Escopo |
|---|---|
| 1 | Site em HTML com os elementos da Unidade 1 (estrutura, textos, links, tabelas, formulários, mídias, listas). |
| 2 | O mesmo site estilizado com CSS: layout, menu, responsividade e animações. |
| 3 | O site dinâmico e interativo com JavaScript: eventos, validação de formulários e consultas dinâmicas. |

Os blocos `📌 Vale gravar` espalhados pelas aulas destacam os pontos que mais reaparecem mais adiante — vale mesmo memorizar.

Esta trilha soma aproximadamente **60 h de estudo**: cerca de 45 h acompanhando as 15 aulas (teoria e prática guiada, em três blocos de 50 min cada) e 15 h nas atividades assíncronas — uma por aula, feita por conta própria depois do conteúdo principal.

> **⚠️ Atenção**
> As atividades assíncronas não são extras opcionais. Elas compõem a prática real da trilha e alimentam o Marco do projeto da unidade correspondente. Pule uma e você sente falta dela mais adiante.

### 1.4 Projeto fio-condutor e projeto autoral

A regra pedagógica central do WebLab é simples:

1. **O projeto fio-condutor** é construído ao longo da trilha — o **site de um evento acadêmico**, a "Semana Acadêmica de Sistemas de Informação" da UNEMAT Sinop. São cinco páginas: **início**, **programação**, **inscrição**, **palestrantes** e **contato**. Na Unidade 1 elas nascem em HTML puro; na Unidade 2 ganham CSS; na Unidade 3 ganham JavaScript. Se você está em aula com um professor, é o projeto que ele constrói com a turma, passo a passo, e todo mundo digita junto; se está estudando sozinho, é o que você constrói acompanhando cada Mão na massa.
2. **Cada pessoa desenvolve também um projeto autoral** com a **mesma arquitetura** (cinco páginas, mesma sequência de tecnologias) e um **domínio diferente**. Os marcos do projeto acompanham o projeto autoral, não o site do evento.

Exemplos de temas que funcionam bem: catálogo de plantas do Pantanal, agenda de quadras esportivas, mural de estágios do curso, brechó de roupas, controle de pescarias no Teles Pires, cardápio de um restaurante, portfólio de um fotógrafo, site de uma ONG de proteção animal. O critério é: você consegue pensar em **cinco páginas com conteúdo real** para esse tema? Se sim, serve.

> **💡 Dica**
> Escolha um tema que você **goste** e sobre o qual **tenha conteúdo** (textos, dados para tabelas, fotos). O erro mais comum é escolher algo genérico demais ("site de uma empresa") e ficar sem o que escrever na página. Tema concreto gera site melhor.

### 1.5 Como estudar com este material

Cada aula do WebLab tem quatro camadas de prática, sempre nesta ordem: **💻 Mão na massa** (o passo a passo guiado, que você acompanha digitando junto — em aula ou sozinho), **🧪 Laboratório** (exercícios em três níveis), **🏆 Desafios** (extras, opcionais, com estrelas de dificuldade) e **🏠 Para praticar depois da aula** (a tarefa de 1 h ligada ao seu projeto autoral).

Uma rotina que funciona:

1. **Antes de estudar cada aula**, leia os objetivos e passe os olhos no conteúdo. Você aproveita muito mais sabendo aonde ela vai chegar.
2. **Ao acompanhar o conteúdo**, digite o código junto. Copiar e colar não fixa nada; digitar e errar, sim.
3. **Logo em seguida**, faça o Laboratório Nível A. São perguntas curtas que consolidam o vocabulário.
4. **Nos dias seguintes**, faça o Nível B e a Atividade assíncrona. São eles que constroem habilidade de verdade.
5. **Se sobrar tempo e vontade**, encare o Nível C e os Desafios. São do tamanho de um item de portfólio — o tipo de coisa que impressiona em uma entrevista de emprego.

Programação não se aprende lendo. Se você fechar esta página achando que entendeu tudo e não tiver escrito código, não aprendeu. Abra o editor.

### 1.6 Ambiente de trabalho

| Ferramenta | Para quê |
|---|---|
| Google Chrome ou Firefox | Executar as páginas e depurar com o DevTools |
| Visual Studio Code | Editar código |
| Live Server (extensão do VS Code) | Servidor local com recarregamento automático |
| Prettier (extensão do VS Code) | Formatação automática do código |
| Validador do W3C (<https://validator.w3.org/>) | Verificar se a marcação HTML está correta |
| Git e GitHub | Versionamento e publicação (a partir da Aula 15 e da trilha Deploy) |

Instalação, em ordem:

1. Baixe e instale o **VS Code** em <https://code.visualstudio.com/>. Aceite as opções padrão.
2. Abra o VS Code e pressione <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>X</kbd> para abrir a aba de extensões.
3. Procure **Live Server** (autor: Ritwick Dey) e clique em *Install*.
4. Procure **Prettier – Code formatter** e clique em *Install*.
5. Em *File → Preferences → Settings*, procure `format on save` e marque a opção. A partir de agora o código é formatado toda vez que você salva.
6. Instale o **Chrome** ou o **Firefox**, se ainda não tiver. Os dois têm DevTools equivalentes; os exemplos das aulas usam o Chrome.

Git e GitHub ficam para mais tarde: o capítulo 02 da trilha **Deploy & Ferramentas** ensina do zero, e a Aula 15 publica o site.

## 2. Internet não é a Web

São coisas diferentes, e confundi-las é o primeiro erro conceitual da área.

A **Internet** é a infraestrutura física e lógica: cabos, fibras, roteadores, satélites e um conjunto de protocolos (principalmente **TCP/IP**) que permitem que máquinas em qualquer lugar do planeta troquem pacotes de dados. A Internet existe desde os anos 1970 (ARPANET) e transporta muito mais do que páginas: e-mail (SMTP), transferência de arquivos (FTP), streaming, chamadas de voz (VoIP), jogos online, o próprio DNS.

A **World Wide Web** é *uma aplicação* que roda sobre a Internet. Foi proposta por Tim Berners-Lee no CERN em 1989 e é composta por três invenções combinadas:

| Invenção | Função |
|---|---|
| **URL** (Uniform Resource Locator) | Um endereço universal para identificar qualquer recurso |
| **HTTP** (HyperText Transfer Protocol) | Um protocolo para pedir e receber esses recursos |
| **HTML** (HyperText Markup Language) | Uma linguagem para descrever documentos com links entre si |

> **💡 Dica**
> Analogia: a Internet é o sistema rodoviário (asfalto, placas, regras de trânsito). A Web é o serviço de entregas que usa essas estradas. WhatsApp, e-mail e jogos online são outros serviços que usam as mesmas estradas sem serem a Web.

Repare que as três invenções são exatamente o que você vai estudar: URLs (hoje), HTTP (hoje e no Nível 2) e HTML (a partir da próxima aula). A Web é, no fundo, uma ideia simples: documentos com endereço, que apontam uns para os outros.

### Linha do tempo essencial

| Ano | Marco |
|---|---|
| 1969 | ARPANET — primeira rede de comutação de pacotes |
| 1983 | TCP/IP se torna o protocolo padrão da ARPANET |
| 1989–1991 | Berners-Lee propõe e implementa a Web no CERN; o primeiro site vai ao ar |
| 1993 | O navegador Mosaic populariza a Web com imagens |
| 1994 | Fundação do W3C (World Wide Web Consortium) |
| 1995 | Nasce o JavaScript (Brendan Eich, Netscape, em cerca de 10 dias) |
| 1996 | Primeira recomendação do CSS |
| 1999–2005 | Ajax e o conceito de "Web 2.0": páginas que atualizam sem recarregar |
| 2014–2015 | HTML5 vira recomendação do W3C; ES2015 moderniza o JavaScript |
| Hoje | Padrões vivos (*living standards*) mantidos por WHATWG, W3C e TC39 |

> **🧠 Você sabia?**
> O primeiro site do mundo continua no ar, no endereço original: <http://info.cern.ch/hypertext/WWW/TheProject.html>. É só HTML, sem uma linha de CSS ou JavaScript — e abre em qualquer navegador moderno em milissegundos. Essa compatibilidade com o passado é uma decisão de projeto da Web: um navegador de hoje precisa continuar exibindo uma página de 1991. Poucas plataformas de software conseguem dizer o mesmo.

## 3. O modelo cliente-servidor

Praticamente toda a Web funciona sobre um modelo de **requisição e resposta** entre dois papéis:

- **Cliente:** quem pede. Na Web, tipicamente o navegador (Chrome, Firefox, Safari, Edge). Também pode ser um aplicativo de celular, um script, outro servidor.
- **Servidor:** quem responde. Um computador executando um software servidor web (Apache, Nginx, Node.js) que fica permanentemente à espera de requisições.

```text
     CLIENTE                                          SERVIDOR
   ┌───────────┐          1. Requisição HTTP        ┌───────────┐
   │ Navegador │    ────────────────────────────>   │ Servidor  │
   │           │          GET /index.html           │    Web    │
   │           │                                    │           │
   │           │    <────────────────────────────   │           │
   └───────────┘          2. Resposta HTTP          └───────────┘
                          200 OK + HTML
```

Três características definem esse modelo:

1. **O cliente sempre inicia.** O servidor nunca "manda" nada espontaneamente numa conexão HTTP tradicional — ele só responde ao que foi pedido.
2. **HTTP é *stateless* (sem estado).** Cada requisição é independente: o servidor não lembra, por si só, o que aconteceu na requisição anterior. Sessões, logins e carrinhos de compra são construídos *por cima* disso, com cookies e tokens.
3. **Uma página não é um arquivo, são dezenas.** Abrir uma página comum dispara de 30 a 200 requisições: o HTML, cada folha de estilo, cada script, cada imagem, cada fonte.

### Front-end e back-end

| | Front-end | Back-end |
|---|---|---|
| **Onde executa** | No navegador do usuário | No servidor |
| **Tecnologias** | HTML, CSS, JavaScript | Node.js, PHP, Java, Python, C#, Go |
| **Responsabilidade** | Interface, interação, apresentação | Regras de negócio, banco de dados, autenticação |
| **Quem controla** | O usuário (pode ver e alterar tudo) | O dono do sistema |

> **⚠️ Atenção**
> Consequência de segurança, importante desde já: **todo código front-end é público**. O usuário pode ler seu JavaScript, alterar valores e burlar validações. Validação no cliente é para conforto do usuário; validação no servidor é para segurança. Nunca confie apenas na validação client-side — você vai ver isso na prática na Aula 03 e voltaremos ao tema na Unidade 3.

Nesta trilha trabalhamos exclusivamente com front-end, mas com consciência do sistema completo.

## 4. O que acontece quando você digita uma URL

Este é um dos assuntos mais cobrados em entrevistas técnicas. Aprenda a sequência.

**Passo 1 — Análise da URL.** O navegador separa o endereço em partes (§5) e descobre qual protocolo usar e qual servidor contatar.

**Passo 2 — Resolução DNS.** O nome `www.unemat.br` não serve para roteamento; a rede trabalha com endereços IP. O navegador consulta o **DNS** (Domain Name System), um serviço distribuído de diretórios, para traduzir o nome em um IP. Antes de sair para a rede, ele consulta caches, nesta ordem: cache do navegador → cache do sistema operacional → arquivo `hosts` → servidor DNS do provedor.

**Passo 3 — Conexão TCP.** Com o IP em mãos, o navegador abre uma conexão TCP com o servidor, normalmente na porta **80** (HTTP) ou **443** (HTTPS), usando o *three-way handshake* (SYN → SYN-ACK → ACK).

**Passo 4 — Handshake TLS (apenas em HTTPS).** Cliente e servidor negociam algoritmos de criptografia, o servidor apresenta seu certificado digital e ambos combinam uma chave de sessão. É isso que produz o cadeado na barra de endereço.

**Passo 5 — Requisição HTTP.** O navegador envia um texto parecido com este:

```http
GET /cursos/sistemas HTTP/1.1
Host: www.unemat.br
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/139.0
Accept: text/html,application/xhtml+xml
Accept-Language: pt-BR,pt;q=0.9
Connection: keep-alive
```

A primeira linha diz **o que** se quer (`GET`) e **onde** (`/cursos/sistemas`). As demais são **cabeçalhos** (*headers*): metadados no formato `Nome: valor`. Repare que é texto puro, legível — HTTP foi projetado para ser simples.

**Passo 6 — Processamento no servidor.** O servidor identifica o recurso pedido. Se for um arquivo estático, apenas o lê do disco. Se for dinâmico, executa código (PHP, Node, Java), possivelmente consulta um banco de dados e gera o HTML na hora.

**Passo 7 — Resposta HTTP.** O servidor devolve outro texto, com uma linha de status, cabeçalhos e, depois de uma linha em branco, o conteúdo:

```http
HTTP/1.1 200 OK
Date: Wed, 12 Aug 2030 22:14:05 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 8420
Cache-Control: max-age=3600

<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <title>Sistemas de Informação — UNEMAT</title>
</head>
```

**Passo 8 — Renderização.** O navegador processa a resposta (detalhado na §6) e dispara **novas requisições** para cada recurso referenciado no HTML: folhas de estilo, scripts, imagens, fontes. Cada uma repete os passos 5 a 7.

> **🔎 Por baixo do capô**
> Por que tanto cache de DNS? Porque cada consulta que sai para a rede custa dezenas de milissegundos — e uma página faz dezenas de requisições, muitas para domínios diferentes. Sem cache, só a tradução de nomes já deixaria a Web visivelmente lenta. O mesmo raciocínio (guardar o que já foi obtido para não pedir de novo) aparece no cabeçalho `Cache-Control` da resposta acima, e é o tema do desafio C1 de hoje.

> **📌 Vale gravar**
> A ordem das etapas (URL → DNS → TCP → TLS → requisição → processamento → resposta → renderização) e o que cada uma faz. Saber que o DNS traduz **nome em IP** e que HTTP é **stateless** são perguntas frequentes.

## 5. Anatomia de uma URL

```text
https://www.unemat.br:443/cursos/sistemas?campus=sinop&turno=noite#ementa
└─┬─┘   └──────┬─────┘└┬┘└──────┬───────┘└────────┬─────────────┘└──┬──┘
  1            2       3        4                 5                 6
```

| # | Elemento | Nome | Função |
|---|---|---|---|
| 1 | `https` | Esquema / protocolo | Como falar com o servidor |
| 2 | `www.unemat.br` | Host / domínio | Com quem falar |
| 3 | `443` | Porta | Qual serviço na máquina (80 = HTTP, 443 = HTTPS; omitida quando é a padrão) |
| 4 | `/cursos/sistemas` | Caminho (*path*) | Qual recurso dentro do servidor |
| 5 | `?campus=sinop&turno=noite` | Query string | Parâmetros no formato `chave=valor`, separados por `&` |
| 6 | `#ementa` | Fragmento / âncora | Posição dentro da página. **Nunca é enviado ao servidor** — é processado só pelo navegador |

O fragmento (`#`) vai ser seu aliado a partir da Aula 02: é ele que faz um link "pular" para uma seção da mesma página. A query string (`?`) vai aparecer na Aula 03, quando um formulário enviado com `GET` grava os campos digitados na própria URL.

### Caminhos absolutos e relativos

Você vai usar isto em toda aula a partir de agora, em links, imagens, folhas de estilo e scripts:

| Notação | Significado | Exemplo |
|---|---|---|
| `pagina.html` | Mesma pasta do arquivo atual | `contato.html` |
| `./pagina.html` | Idem, de forma explícita | `./contato.html` |
| `imagens/foto.jpg` | Subpasta | `img/logo.png` |
| `../pagina.html` | Uma pasta acima | `../index.html` |
| `/pagina.html` | A partir da raiz do site | `/sobre.html` |
| `https://site.com/x` | Absoluto, outro servidor | link externo |

O ponto de partida de um caminho relativo é sempre **a pasta do arquivo onde o caminho está escrito**, não a pasta do projeto. Se `paginas/contato.html` precisa da imagem `img/logo.png` que está na raiz, o caminho correto é `../img/logo.png`: sobe um nível, entra em `img`.

> **⚠️ Atenção**
> Erro clássico: usar `C:\Users\Ivan\Documents\site\logo.png` no `src` de uma imagem. Funciona na sua máquina e quebra em todas as outras. Caminhos de sistema de arquivos não existem na Web — o servidor só conhece a pasta do site.

## 6. Como o navegador renderiza uma página

O navegador não "mostra o HTML". Ele executa um *pipeline*:

```text
HTML   ──parsing──>   DOM ┐
                          ├──> Render Tree ──> Layout ──> Paint ──> Composite
CSS   ──parsing──> CSSOM ┘
                            ▲
JavaScript ─────────────────┘ (pode alterar DOM e CSSOM a qualquer momento)
```

1. **Parsing do HTML → DOM.** O navegador lê o HTML caractere a caractere e monta uma árvore de objetos chamada **DOM** (Document Object Model). Cada tag vira um nó da árvore.
2. **Parsing do CSS → CSSOM.** As regras de estilo viram outra árvore, o CSSOM.
3. **Render Tree.** DOM + CSSOM são combinados, descartando o que não é visível (por exemplo, o que tem `display: none`).
4. **Layout (*reflow*).** Cálculo da posição e do tamanho exatos de cada caixa na tela.
5. **Paint.** Preenchimento de pixels: cores, textos, bordas, sombras.
6. **Composite.** Montagem das camadas na tela.

Cada navegador tem um **motor de renderização**: Blink (Chrome, Edge, Opera), Gecko (Firefox), WebKit (Safari). Diferenças entre motores são a razão de existirem os padrões — e a razão de os sites às vezes ficarem diferentes em cada navegador.

> **🔎 Por baixo do capô**
> Por que JavaScript bloqueia o parsing: quando o parser encontra um `<script>` sem atributos, ele **para** de montar o DOM, baixa e executa o script, e só então continua. Por isso a boa prática de colocar `<script>` antes de `</body>` ou usar o atributo `defer`. Você vai ver isso de perto na Aula 10, quando o JavaScript entrar em cena.

O DOM é uma das ideias mais importantes do semestre. Guarde desde já: o arquivo `.html` no disco é **texto**; o DOM é a **árvore em memória** que o navegador constrói a partir dele. O DevTools mostra o DOM, não o arquivo — e o JavaScript, na Unidade 3, vai manipular o DOM, não o arquivo.

## 7. Os três pilares do front-end

| Pilar | Papel | Analogia |
|---|---|---|
| **HTML** | Estrutura e significado do conteúdo | O esqueleto e os órgãos |
| **CSS** | Apresentação visual | A pele, as roupas, a aparência |
| **JavaScript** | Comportamento e interatividade | Os músculos e o sistema nervoso |

A separação entre eles é chamada de **separação de responsabilidades** (*separation of concerns*) e é um princípio de engenharia, não capricho: permite trocar o visual sem tocar no conteúdo, reaproveitar estilos entre páginas e manter o código legível por equipes diferentes.

Um mesmo HTML com três CSS distintos vira três sites visualmente diferentes. Esse é o ponto — e é exatamente o que vai acontecer com o site do evento: o HTML que você escreve na Unidade 1 não muda quando o CSS chega na Unidade 2.

### Padrões e quem os define

| Organização | Cuida de |
|---|---|
| **W3C** | Especificações da Web, com destaque para CSS e acessibilidade |
| **WHATWG** | HTML e DOM como *living standard* |
| **TC39 / Ecma International** | ECMAScript, a especificação da linguagem JavaScript |
| **IETF** | Protocolos de rede (HTTP, TCP/IP), publicados como RFCs |

Nenhuma empresa é dona da Web. Os navegadores implementam especificações públicas, escritas em processo aberto. É por isso que a documentação oficial (MDN, especificações do W3C e da WHATWG) vale mais do que qualquer tutorial — e é para ela que os links de "Para aprofundar" apontam.

## 8. Arquitetura em camadas

"Camada" (*tier* ou *layer*) é uma divisão lógica de responsabilidades. Quanto mais camadas, maior a separação — e maior a complexidade.

### Uma camada (monolítica local)

Tudo em um único programa, em uma única máquina. Não é Web — é o modelo de um aplicativo desktop antigo, com interface, regras e dados no mesmo executável.

### Duas camadas (cliente-servidor clássico)

```text
[ Cliente com lógica ]   <──────>   [ Servidor de Banco de Dados ]
```

O cliente é "gordo" (*fat client*): contém a interface **e** as regras de negócio, e conversa diretamente com o banco. Problema: qualquer mudança de regra exige reinstalar o programa em todas as máquinas, e o banco fica exposto na rede.

### Três camadas — o padrão da Web

```text
┌──────────────────┐   HTTP   ┌──────────────────┐   SQL   ┌──────────────┐
│ APRESENTAÇÃO     │ <──────> │    APLICAÇÃO     │ <─────> │    DADOS     │
│ (navegador)      │          │ (servidor web +  │         │   (SGBD)     │
│ HTML/CSS/JS      │          │ regras negócio)  │         │ MySQL,       │
│                  │          │ Node, PHP, Java  │         │ PostgreSQL   │
└──────────────────┘          └──────────────────┘         └──────────────┘
     CLIENTE                        SERVIDOR                  SERVIDOR
```

| Camada | Responsabilidade | Onde executa |
|---|---|---|
| Apresentação | Interface, captura de entrada, exibição | Navegador (cliente) |
| Aplicação / Lógica | Regras de negócio, validação, autenticação, orquestração | Servidor |
| Dados | Armazenamento, integridade, consultas | Servidor de banco |

Vantagens: cada camada pode ser escalada, atualizada e substituída de forma independente; o banco nunca fica exposto ao cliente; as regras existem em um único lugar.

**Esta trilha inteira vive na camada de apresentação.** O Nível 2 constrói a camada de aplicação (Node.js + Express) e o Nível 3 integra as três.

### N camadas e microsserviços

Sistemas grandes fragmentam ainda mais: camada de cache (Redis), fila de mensagens (RabbitMQ, Kafka), balanceador de carga (Nginx), serviços independentes por domínio de negócio. Ganha-se escalabilidade e autonomia de equipes; paga-se com complexidade operacional e latência de rede. Nada disso é assunto deste nível, mas você vai reconhecer os nomes quando ler uma vaga de emprego.

## 9. Sites estáticos e dinâmicos

| | Estático | Dinâmico |
|---|---|---|
| **Como o HTML é obtido** | Arquivo pronto, lido do disco | Gerado a cada requisição por código |
| **Conteúdo** | Igual para todos | Varia por usuário, hora, banco |
| **Velocidade** | Muito alta | Depende do processamento |
| **Custo de hospedagem** | Baixíssimo (ou grátis) | Servidor de aplicação + banco |
| **Segurança** | Superfície de ataque mínima | Exige cuidado (SQL injection, XSS) |
| **Exemplos** | Portfólio, landing page, documentação | Rede social, e-commerce, sistema acadêmico |

> **⚠️ Atenção**
> Confusão frequente: "dinâmico", no sentido de arquitetura, significa **HTML gerado no servidor**. Uma página estática com muito JavaScript e animações continua sendo estática do ponto de vista arquitetural. O SIGAA é dinâmico. Um portfólio com carrossel animado é estático. O site do evento que vamos construir é estático — e vai ser publicado de graça, por isso mesmo.

## 10. MPA e SPA

**MPA — Multi Page Application.** Cada navegação carrega um novo documento HTML completo do servidor. É o modelo tradicional. Vantagens: simples, ótimo para buscadores (SEO), funciona sem JavaScript. Desvantagem: a tela "pisca" a cada clique.

**SPA — Single Page Application.** O servidor entrega um HTML e um pacote JavaScript. A partir daí, o JavaScript intercepta a navegação, busca apenas os **dados** (via API, em JSON) e reescreve o DOM. Vantagens: sensação de aplicativo, menos tráfego após a carga inicial. Desvantagens: carga inicial pesada, complexidade, SEO exige trabalho extra, quebra sem JavaScript. Frameworks típicos: React, Vue, Angular, Svelte.

```text
MPA:   clique ──> servidor ──> HTML completo ──> recarrega a página
SPA:   clique ──> JS intercepta ──> API ──> JSON ──> JS reescreve o DOM
```

O site do evento é uma MPA: cinco arquivos `.html`, um por página. É o ponto de partida certo — SPAs são o assunto do Nível 2 (Unidade 2) e do Nível 3 inteiro.

## 11. APIs, JSON e REST

Uma **API** (Application Programming Interface) é um contrato pelo qual dois sistemas conversam. Na Web, o estilo dominante é o **REST**, que usa os próprios verbos do HTTP:

| Verbo HTTP | Ação | Exemplo |
|---|---|---|
| `GET` | Ler | `GET /api/alunos` — lista alunos |
| `POST` | Criar | `POST /api/alunos` — cadastra aluno |
| `PUT` / `PATCH` | Atualizar | `PUT /api/alunos/42` |
| `DELETE` | Remover | `DELETE /api/alunos/42` |

Perceba que essas quatro operações são exatamente o **CRUD** (Create, Read, Update, Delete). Neste nível você vai reconhecer o CRUD nas requisições que o navegador faz; a leitura de dados aparece nas consultas dinâmicas da Aula 14, e a escrita no servidor é assunto do Nível 2.

O formato de troca padrão é o **JSON** (JavaScript Object Notation) — texto, legível, com pares `chave: valor`:

```json
{
  "id": 42,
  "nome": "Maria Silva",
  "curso": "Sistemas de Informação",
  "fase": 2,
  "ativo": true,
  "disciplinas": ["Desenvolvimento Web", "Banco de Dados"]
}
```

### Principais códigos de status HTTP

| Faixa | Significado | Exemplos |
|---|---|---|
| `1xx` | Informativo | `100 Continue` |
| `2xx` | Sucesso | `200 OK`, `201 Created`, `204 No Content` |
| `3xx` | Redirecionamento | `301 Moved Permanently`, `304 Not Modified` |
| `4xx` | Erro do cliente | `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found` |
| `5xx` | Erro do servidor | `500 Internal Server Error`, `502 Bad Gateway`, `503 Service Unavailable` |

> **💡 Dica**
> Mnemônico: **4xx é culpa de quem pediu; 5xx é culpa de quem respondeu.** Um `404` diz "você pediu algo que não existe"; um `500` diz "eu quebrei ao tentar responder".

> **🔬 Investigue**
> Abra <https://www.unemat.br>, pressione <kbd>F12</kbd>, vá à aba **Network** e recarregue com <kbd>Ctrl</kbd>+<kbd>F5</kbd>. Observe: (1) quantas linhas apareceram — cada uma é uma requisição; (2) a coluna *Type*: `document`, `stylesheet`, `script`, `png`, `font`; (3) clique na primeira linha, abra *Headers* e procure `Content-Type` e `Server` na resposta; (4) na barra inferior, leia o total de requisições e o peso transferido. Você acabou de ver o "uma página são dezenas de arquivos" acontecendo — e o cabeçalho `Server` conta qual software respondeu.

## 12. Infraestrutura de entrega

- **Servidor web:** Apache, Nginx, IIS, Node.js. Recebe requisições e devolve recursos.
- **CDN (Content Delivery Network):** rede de servidores espalhados geograficamente que guardam cópias dos arquivos. Um usuário em Sinop recebe o arquivo de um nó em São Paulo, não da Califórnia. Reduz a latência drasticamente. Exemplos: Cloudflare, Akamai.
- **Hospedagem estática:** GitHub Pages, Netlify, Vercel, Cloudflare Pages — gratuitas e suficientes para tudo que faremos nesta trilha. O projeto do Marco 3 (Aula 15) é publicado em uma delas.
- **DNS e domínio:** registro de domínios `.br` via Registro.br. Um domínio próprio custa por volta de R$ 40 por ano; a trilha Deploy (capítulo 04) mostra como apontar um para o seu site.

## 💻 Mão na massa — Pasta do projeto, primeiro HTML e DevTools

Hoje nasce a pasta que você vai usar até o fim da trilha e o primeiro arquivo do site do evento.

### Passo 1 — Estrutura de pastas

Crie, no seu computador (em *Documentos*, por exemplo), a seguinte estrutura. Por enquanto só as pastas e um arquivo:

```text
introducao-web/
├── site-evento/          ← projeto fio-condutor (construído aula a aula)
│   ├── index.html
│   ├── css/
│   ├── img/
│   └── js/
├── meu-projeto/          ← projeto autoral (tema seu, mesma estrutura)
└── exercicios/
    ├── aula01/
    ├── aula02/
    └── aula03/
```

> **⚠️ Atenção**
> Regra permanente: nomes de arquivos e pastas em **minúsculas, sem espaços, sem acentos**. Use hífen para separar palavras (`sobre-nos.html`, nunca `Sobre Nós.html`). Servidores Linux diferenciam maiúsculas de minúsculas — `Index.html` e `index.html` são arquivos distintos para eles, e o que funciona no Windows pode quebrar quando você publicar.

Abra o VS Code, vá em *File → Open Folder* e abra a pasta `introducao-web`. Sempre abra a **pasta raiz**, não um arquivo solto: o Live Server e os caminhos relativos dependem disso.

### Passo 2 — O primeiro HTML

No painel esquerdo, clique com o botão direito em `site-evento` → *New File* → `index.html`. Digite (não cole):

`site-evento/index.html`

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Semana Acadêmica de Sistemas de Informação</title>
</head>
<body>
  <h1>Semana Acadêmica de Sistemas de Informação</h1>
  <p>Três dias de palestras, minicursos e oficinas na UNEMAT Sinop.</p>
  <p>Este site está sendo construído com o WebLab, na trilha <strong>Introdução ao Desenvolvimento Web</strong>.</p>
</body>
</html>
```

Cada linha será explicada na Aula 02. Por hoje, o essencial: `<!DOCTYPE html>` diz que é HTML5; `<head>` guarda informações *sobre* a página; `<body>` guarda o que aparece na tela; e `<meta charset="UTF-8">` diz ao navegador como ler os acentos.

### Passo 3 — Subir o servidor local

Clique com o botão direito no arquivo `index.html` → **Open with Live Server** (ou clique em *Go Live* no canto inferior direito). O navegador abre em um endereço parecido com:

```text
http://127.0.0.1:5500/site-evento/index.html
```

Leia essa URL com a §5 na cabeça: esquema `http`, host `127.0.0.1`, porta `5500`, caminho `/site-evento/index.html`. Você acabou de subir um **servidor web** na sua máquina — `127.0.0.1` é o endereço que todo computador usa para se referir a si mesmo (também chamado de `localhost`). A partir de agora o navegador é o **cliente** e o Live Server é o **servidor**, exatamente como no diagrama da §3.

Altere o texto do `<p>`, salve com <kbd>Ctrl</kbd>+<kbd>S</kbd> e olhe o navegador: ele recarrega sozinho. É isso que o Live Server faz.

### Passo 4 — Experimento obrigatório: o charset

Remova a linha `<meta charset="UTF-8">`, salve e olhe o navegador. Os acentos viram símbolos estranhos (`Ã§`, `Ã£`, `Ã©`). Isso acontece porque o navegador passa a interpretar os bytes com outra tabela de caracteres. **Recoloque a linha.** Esse é o erro mais comum de iniciante e agora você sabe reconhecê-lo em dois segundos.

### Passo 5 — Ferramentas do desenvolvedor (DevTools)

Pressione <kbd>F12</kbd> (ou <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>I</kbd>). Você vai usar isto todos os dias do semestre.

| Aba | Para que serve |
|---|---|
| **Elements** | Ver e editar o DOM e o CSS aplicado, ao vivo |
| **Console** | Mensagens de erro e execução de JavaScript |
| **Network** | Todas as requisições: método, status, tamanho, tempo |
| **Sources** | Ver arquivos e depurar JavaScript com *breakpoints* |
| **Application** | Cookies e `localStorage` (usaremos na Unidade 3) |
| **Lighthouse** | Auditoria de desempenho, acessibilidade e SEO |

Roteiro de exploração — faça agora, na sua página:

1. **Elements:** dê duplo clique no texto do `<h1>` e altere. Note que muda na tela mas **não no arquivo** — você está editando o DOM em memória, não o HTML. Recarregue e a alteração some.
2. **Console:** digite `document.title` e pressione <kbd>Enter</kbd>. Aparece o texto do seu `<title>`. Digite `document.body.children.length` — quantos filhos diretos o `<body>` tem?
3. **Network:** marque *Disable cache*, recarregue com <kbd>Ctrl</kbd>+<kbd>F5</kbd> e observe o status `200` ao lado de `index.html`. Agora renomeie o arquivo para `inicio.html` e recarregue: status `404`. Renomeie de volta.
4. Abra <https://www.unemat.br> em outra aba e, na aba Network, conte quantas requisições a página faz e qual é o maior arquivo (clique no cabeçalho da coluna *Size* para ordenar).

### Passo 6 — O projeto autoral começa hoje

Copie `site-evento/index.html` para `meu-projeto/index.html` e troque o `<title>`, o `<h1>` e os parágrafos pelo tema do **seu** projeto. Abra também com o Live Server. Está feito o primeiro commit mental: a partir de agora, tudo que o site do evento ganha nesta trilha, o seu projeto ganha também.

### Como testar

- O Live Server abre `http://127.0.0.1:5500/site-evento/index.html` e a página mostra o título e os parágrafos com acentos corretos.
- Alterar e salvar o arquivo recarrega o navegador sozinho.
- Na aba Network, `index.html` aparece com status `200`.
- No Console, `document.title` devolve `"Semana Acadêmica de Sistemas de Informação"`.
- `meu-projeto/index.html` abre com o seu tema.

**Resultado esperado:** duas páginas simples no ar, servidas pelo Live Server; o DevTools aberto e explorado; a estrutura de pastas pronta para o semestre.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Explique, com suas palavras e em no máximo 4 linhas, a diferença entre Internet e World Wide Web.

**A2.** Classifique cada item como *Internet* ou *Web*: (a) protocolo TCP/IP; (b) HTML; (c) e-mail via SMTP; (d) HTTP; (e) cabos de fibra óptica submarinos; (f) URL.

**A3.** Decomponha a URL abaixo, nomeando cada uma das seis partes:

```text
https://loja.exemplo.com.br:8443/produtos/notebooks?marca=dell&ordem=preco#avaliacoes
```

**A4.** O que significa dizer que o HTTP é *stateless*? Cite uma consequência prática disso.

**A5.** Qual a porta padrão do HTTP? E do HTTPS? Por que elas normalmente não aparecem na URL?

**A6.** Coloque em ordem correta as etapas: (1) handshake TCP; (2) renderização; (3) resolução DNS; (4) resposta HTTP; (5) requisição HTTP; (6) análise da URL.

**A7.** Associe cada tecnologia ao seu papel: HTML / CSS / JavaScript ↔ comportamento / apresentação / estrutura.

**A8.** Um arquivo está em `site/paginas/contato.html` e precisa referenciar `site/img/logo.png`. Qual o caminho relativo correto?

**A9.** O que é o DOM? Ele existe no arquivo `.html` salvo em disco ou apenas em memória?

**A10.** Cite três organizações que mantêm padrões da Web e diga do que cada uma cuida.

**A11.** Por que `#secao2` na URL não gera requisição ao servidor?

**A12.** Qual a diferença entre os status HTTP `200` e `404`? Cite mais dois códigos e seus significados.

### Nível B — Aplicação

**B1.** Usando a aba Network do DevTools, acesse três sites diferentes (um portal de notícias, um e-commerce e o site da UNEMAT) e registre, para cada um: número de requisições, peso total transferido (KB ou MB), tempo de carregamento (*Load*, na barra inferior) e qual foi o maior recurso. Escreva um parágrafo comparando os resultados e levantando hipóteses sobre as diferenças.

**Resultado esperado:** uma tabela com três linhas e quatro medidas cada, mais um parágrafo de análise (por exemplo: "o portal de notícias fez 3× mais requisições por causa de anúncios e rastreadores").

<details><summary>Dica</summary>

Marque *Disable cache* antes de medir, senão a segunda visita vem do cache e distorce a comparação. A barra de resumo na parte inferior da aba Network mostra "N requests | X MB transferred | Load: Y s".
</details>

**B2.** Crie `exercicios/aula01/sobre-mim.html` contendo: título da página no `<title>`, um `<h1>` com seu nome, um parágrafo de apresentação, um parágrafo com seus objetivos nesta trilha e um link para o site da UNEMAT que abra em nova aba (pesquise o atributo `target`).

**Resultado esperado:** a página abre no Live Server com acentos corretos; o link abre `https://www.unemat.br` em outra aba.

<details><summary>Dica</summary>

Parta do `index.html` que você criou no Mão na massa. O link é `<a href="https://www.unemat.br" target="_blank">UNEMAT</a>`. Na Aula 02 você vai descobrir por que esse link precisa de um atributo extra de segurança.
</details>

**B3.** Desenhe (no papel, no Draw.io ou no Excalidraw) um diagrama do ciclo requisição-resposta incluindo: usuário, navegador, DNS, Internet, servidor web e banco de dados. Indique com setas numeradas a ordem dos eventos.

**Resultado esperado:** um diagrama com pelo menos 8 setas numeradas, do "usuário digita a URL" ao "navegador renderiza".

<details><summary>Dica</summary>

Siga os oito passos da §4. O banco de dados só entra no Passo 6, e só se o site for dinâmico — represente isso.
</details>

**B4.** No Console do DevTools, execute os comandos abaixo em uma página qualquer e registre o resultado de cada um, explicando o que retornaram:

```js
window.location.href
window.location.protocol
window.location.hostname
document.title
navigator.userAgent
```

**Resultado esperado:** cinco linhas de saída com a sua explicação; você deve conseguir relacionar `protocol` e `hostname` com as partes 1 e 2 da URL da §5.

<details><summary>Dica</summary>

`window.location` é um objeto que representa a URL atual, já decomposta. Experimente também `window.location.port` e `window.location.hash` na sua página do Live Server.
</details>

**B5.** Pesquise e escreva um resumo de meia página sobre a diferença entre HTTP/1.1, HTTP/2 e HTTP/3, focando em: multiplexação, cabeçalhos e protocolo de transporte usado.

**Resultado esperado:** texto de 15 a 25 linhas, com pelo menos uma fonte citada (a MDN serve).

<details><summary>Dica</summary>

Comece por "HTTP/2 multiplexação" e "HTTP/3 QUIC" na MDN. Na aba Network, a coluna *Protocol* (ative-a clicando com o botão direito no cabeçalho das colunas) mostra `h2` ou `h3` para cada requisição — veja o que os sites que você visita usam.
</details>

**B6.** Abra um site com HTTPS, clique no cadeado e examine o certificado. Registre: quem emitiu, para qual domínio é válido, data de validade e qual o algoritmo de chave. Explique para que serve cada informação.

**Resultado esperado:** quatro dados anotados e uma explicação de 2 a 3 linhas para cada um.

<details><summary>Dica</summary>

No Chrome: cadeado → *A conexão é segura* → *O certificado é válido*. O "emissor" é a autoridade certificadora (Let's Encrypt, DigiCert); ela é quem garante ao navegador que o servidor é quem diz ser — é o Passo 4 da §4.
</details>

### Nível C — Desafio

**C1.** Investigação de cache. Acesse um mesmo site duas vezes na aba Network: uma com *Disable cache* marcado e outra desmarcado. Compare o número de requisições e o peso transferido. Identifique quais recursos vieram do cache (procure por `(disk cache)`, `(memory cache)` ou status `304`). Produza um relatório de 1 página explicando o que é cache HTTP, o papel do cabeçalho `Cache-Control` e por que ele é essencial para a performance da Web.

<details><summary>Dica</summary>

Na segunda visita, a coluna *Size* mostra "(disk cache)" em vez de um tamanho — esses arquivos nem saíram para a rede. O status `304 Not Modified` é diferente: a requisição saiu, mas o servidor respondeu "você já tem a versão atual". Clique em um recurso e leia `Cache-Control` e `ETag` nos cabeçalhos de resposta.
</details>

## 🏆 Desafios

### ⭐ Quem entregou esta página?
Tags: devtools, http, investigacao

Toda resposta HTTP carrega cabeçalhos que contam quem a produziu — e muitos sites deixam pistas: qual servidor web, se passou por uma CDN, há quanto tempo o arquivo está em cache. Hoje você vira detetive: escolha três sites (o da UNEMAT, um jornal e um e-commerce) e descubra, só pelos cabeçalhos, como cada um é entregue.

**Critérios de pronto**

- Para cada site, uma tabela com os valores dos cabeçalhos de resposta do documento HTML principal: `Server`, `Content-Type`, `Cache-Control` e pelo menos um cabeçalho que revele CDN (por exemplo `cf-ray`, `x-served-by`, `via`, `x-cache`).
- Uma classificação de cada site em "servido direto" ou "servido via CDN", com a evidência.
- Uma linha explicando o que o valor de `Cache-Control` de cada site significa na prática.

<details><summary>Pistas</summary>

1. Aba Network → clique na primeira linha (o documento) → *Headers* → role até *Response Headers*.
2. Cloudflare deixa `cf-ray` e `server: cloudflare`; Fastly deixa `x-served-by`; Akamai costuma deixar `x-akamai-*` ou `server: AkamaiGHost`.
3. Se `Server` estiver ausente, o site está escondendo o software de propósito — isso também é uma resposta (e uma prática de segurança).
4. Leia a página da MDN sobre `Cache-Control` para traduzir `max-age`, `no-cache` e `public`.
</details>

### ⭐⭐ Linha do tempo da Web, só com HTML
Tags: html, projeto

A tabela da §2 resume meio século em dez linhas. Ela merece mais: crie uma página HTML com uma linha do tempo de **pelo menos 10 marcos** da história da Web (1969 até hoje), cada um com ano, título e um parágrafo de 2 a 3 linhas explicando sua importância. Use apenas HTML nesta etapa — o CSS entra a partir da Aula 05 e você vai reaproveitar exatamente esta página para estilizá-la.

**Critérios de pronto**

- Arquivo `exercicios/aula01/linha-do-tempo.html` com a estrutura mínima completa (doctype, `lang`, charset, viewport, title).
- Pelo menos 10 marcos, em ordem cronológica, cada um com ano, título e parágrafo.
- Pelo menos 3 marcos que **não** estão na tabela da §2 (pesquise: o primeiro navegador gráfico, a criação do Google, o lançamento do iPhone e o efeito na Web móvel, o nascimento do Node.js).
- Uma fonte citada ao final da página, com link.

<details><summary>Pistas</summary>

1. Você ainda não conhece os elementos de lista e de título — use `<h2>` para o ano + título e `<p>` para o texto; na Aula 02 você reescreve com `<ol>` e `<time>`.
2. A Wikipédia em português tem um artigo "História da World Wide Web" com datas confiáveis.
3. Pense na página como um documento que alguém vai ler de cima a baixo sem nenhum estilo: a ordem e a hierarquia dos títulos precisam contar a história sozinhas.
</details>

### ⭐⭐ A rota até a UNEMAT
Tags: terminal, dns, investigacao

Quantos computadores um pacote atravessa entre a sua máquina e o servidor da UNEMAT? A resposta está em um comando que existe em todo sistema operacional. No terminal, execute `tracert www.unemat.br` (Windows) ou `traceroute www.unemat.br` (Linux/macOS). Registre a saída e responda: quantos saltos foram necessários? O que representa cada linha? Qual o tempo total? Relacione o resultado com o conceito de comutação de pacotes.

**Critérios de pronto**

- A saída completa do comando, copiada em um bloco de texto.
- O número de saltos e o tempo aproximado do último salto.
- Uma explicação, por escrito, do que são as três medidas de tempo em cada linha e por que algumas linhas mostram `* * *`.
- Uma comparação com `nslookup www.unemat.br` (ou `dig`): qual IP foi resolvido, e ele bate com o destino do traceroute?
- Um parágrafo relacionando o resultado com "a Internet é uma rede de comutação de pacotes".

<details><summary>Pistas</summary>

1. No Windows, abra o *Prompt de Comando* ou o *PowerShell*; no Linux/macOS, o *Terminal*. Se `traceroute` não existir no Linux, instale com `sudo apt install traceroute`.
2. Cada linha é um roteador no caminho; as três medidas são três tentativas de ida e volta (RTT). `* * *` significa que aquele roteador não respondeu ao pacote de teste — não que a rota parou.
3. Os primeiros saltos são a sua rede local e o seu provedor; os últimos, o data center do destino. Os nomes dos roteadores costumam entregar a cidade (procure siglas como `spo`, `cgb`, `gru`).
4. Rode duas vezes em horários diferentes e compare os tempos.
</details>

### ⭐⭐⭐ HTTP à mão
Tags: http, https, terminal, investigacao

O navegador esconde tudo o que a §4 descreve. Hoje você faz o trabalho dele manualmente: dispara uma requisição HTTP sem navegador, lê a resposta crua e compara protocolos. A ferramenta é o `curl`, que já vem instalado no Windows 10+, no macOS e na maioria das distribuições Linux. Ao final, você vai conseguir explicar para outra pessoa, com evidências, cada etapa do "o que acontece quando digito uma URL".

**Critérios de pronto**

- A saída de `curl -v https://www.unemat.br` salva em um arquivo, com anotações marcando: a resolução DNS, a conexão TCP, o handshake TLS (algoritmo negociado e emissor do certificado), a requisição enviada (linhas com `>`) e a resposta recebida (linhas com `<`).
- A saída de `curl -I https://www.unemat.br` (só cabeçalhos) com uma explicação, em uma linha cada, de pelo menos 5 cabeçalhos de resposta.
- Uma requisição a um caminho inexistente (`curl -I https://www.unemat.br/nao-existe`) e a interpretação do status recebido.
- Uma comparação entre `curl --http1.1 -I` e `curl --http2 -I` no mesmo site: qual versão o servidor aceitou, e como você sabe?
- Um texto de 10 linhas, escrito como se fosse explicar a outra pessoa, ligando cada evidência ao passo correspondente da §4.

<details><summary>Pistas</summary>

1. `curl --version` confirma que o comando existe e lista os protocolos suportados (procure `HTTP2` e `HTTP3` na linha *Features*).
2. Em `-v`, as linhas que começam com `*` são informações da conexão (DNS, TCP, TLS); `>` é o que foi enviado; `<` é o que voltou.
3. Se o site redirecionar (status `301` ou `302`), adicione `-L` para seguir o redirecionamento e observe as duas respostas.
4. A primeira linha da resposta (`HTTP/2 200` ou `HTTP/1.1 200 OK`) já denuncia a versão do protocolo negociada.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| Acentos aparecem como `Ã§`, `Ã£`, `Ã©` | Falta `<meta charset="UTF-8">` ou o arquivo foi salvo em outra codificação | Incluir a meta como primeira linha do `<head>`; no VS Code, conferir "UTF-8" na barra inferior |
| Link ou imagem funciona no seu computador e quebra no do colega | Nome com espaço, acento ou maiúscula, ou caminho de disco (`C:\`) | Nomes em minúsculas, sem acentos, com hífen; caminhos relativos |
| Navegador exibe o código-fonte como texto puro | Arquivo salvo como `.txt` (às vezes `index.html.txt`, com a extensão oculta) | Conferir a extensão no VS Code; no Windows, ativar "mostrar extensões de arquivo" |
| Live Server abre uma lista de pastas ou "Cannot GET /" | O VS Code foi aberto em um arquivo solto, ou em uma pasta que não contém o `index.html` | *File → Open Folder* na pasta raiz `introducao-web`; abrir o Live Server a partir do arquivo |
| A página não recarrega ao salvar | Live Server não está ativo (não aparece "Port: 5500" na barra inferior) | Clicar em *Go Live*; se a porta estiver ocupada, fechar o outro servidor |
| Edição feita no DevTools sumiu ao recarregar | O DevTools altera o DOM em memória, não o arquivo | Fazer a alteração no VS Code e salvar |
| Confundir Internet com Web | Erro conceitual: tratar as duas como sinônimos | Web é uma **aplicação** que roda **sobre** a Internet (§2) |
| Aba Network vazia ao abrir o DevTools | A aba só registra a partir do momento em que é aberta | Abrir o DevTools **antes** e recarregar a página |

## 🏠 Para praticar depois da aula (1 h)

**Parte 1 — Leitura (20 min).** SILVA, M. S. *Criando sites com HTML*, capítulo introdutório. MILETTO, E. M.; BERTAGNOLLI, S. C. *Desenvolvimento de software II*, capítulo sobre arquiteturas para a Web. Anote duas ideias de cada texto que não apareceram nesta aula.

**Parte 2 — Produção (30 min).** Produza:

1. O exercício **B2** (`sobre-mim.html`) e o exercício **B5** (resumo sobre HTTP/1.1, 2 e 3).
2. Uma captura de tela do VS Code com a pasta `introducao-web` aberta e outra do Live Server exibindo `site-evento/index.html`, com a URL `127.0.0.1:5500` visível.
3. **O tema do seu projeto autoral**, em 3 linhas: o que é, para quem é, e o nome das cinco páginas (a versão "início, programação, inscrição, palestrantes, contato" do seu domínio).

**Parte 3 — Discussão (10 min).** Em texto próprio — ou no fórum da turma, se você está cursando esta trilha em grupo —, escreva 10 a 15 linhas sobre por que a Web se tornou a plataforma dominante de aplicações — pense em distribuição (não precisa instalar nada), padrões abertos e compatibilidade entre dispositivos. Se puder, compare sua resposta com a de outra pessoa que esteja estudando o mesmo conteúdo.

**Critério de pronto:** os dois arquivos abrem sem erro de codificação; as duas capturas mostram o ambiente funcionando; o tema tem cinco páginas nomeadas.

**Guarde:** os arquivos `.html` e as capturas na pasta `exercicios/aula01/` — a partir da Aula 15 tudo isso passa a viver em um repositório Git.

## ✅ Checkpoint do projeto

Ao fim desta aula, na sua máquina:

- [ ] Pasta `introducao-web/` criada com `site-evento/`, `meu-projeto/` e `exercicios/`.
- [ ] `site-evento/index.html` com a estrutura mínima (doctype, `lang="pt-BR"`, charset, viewport, title, um `<h1>` e parágrafos).
- [ ] `meu-projeto/index.html` com o mesmo esqueleto e o **seu** tema.
- [ ] Live Server instalado e abrindo as páginas em `http://127.0.0.1:5500/`.
- [ ] Prettier instalado, com *format on save* ativado.
- [ ] DevTools explorado: você já editou o DOM na aba Elements, rodou `document.title` no Console e viu um `200` e um `404` na aba Network.
- [ ] Tema do projeto autoral escolhido e as cinco páginas nomeadas.

## 📚 Para aprofundar

- MDN — Aprenda desenvolvimento web (índice geral, em português): <https://developer.mozilla.org/pt-BR/docs/Learn_web_development> — comece por "Primeiros passos".
- MDN — Como a Web funciona: <https://developer.mozilla.org/pt-BR/docs/Learn_web_development/Getting_started/Web_standards/How_the_web_works> — a versão ilustrada da §3 e da §4 desta aula.
- MDN — Visão geral do HTTP: <https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Overview> — leia a parte sobre requisições e respostas.
- MDN — Códigos de status HTTP: <https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Status> — referência para consultar, não para decorar.
- MDN — O que é uma URL: <https://developer.mozilla.org/pt-BR/docs/Learn_web_development/Howto/Web_mechanics/What_is_a_URL> — complementa a §5.
- web.dev — Learn HTML (em inglês): <https://web.dev/learn/html> — o primeiro capítulo, "Overview of HTML", prepara a Aula 02.
- CERN — O primeiro site da Web: <http://info.cern.ch/> — abra e veja a §2 ao vivo.
- SILVA, Maurício Samy. *Criando sites com HTML: sites de alta qualidade com HTML e CSS*. Novatec, 2008 — capítulo 1.
- TERUEL, Evandro C. *HTML 5 — Guia Prático*. Saraiva, 2014 — introdução (disponível na Minha Biblioteca).
- MILETTO, Evandro M.; BERTAGNOLLI, Silvia C. *Desenvolvimento de software II*. Bookman, 2014 — capítulo sobre arquiteturas para a Web.

Na próxima aula, o HTML entra de verdade: você vai entender cada linha do `index.html` que criou hoje, aprender os elementos de texto, listas, links e tabelas, e construir a página inicial, a programação e a página de palestrantes do site do evento com HTML semântico e validado no W3C.
