# Aula 01 — Apresentação, arquitetura web, ambiente de desenvolvimento e Git

> **Nível 2 — Desenvolvimento Web** · Unidade 1: Web estática
> WebLab · UNEMAT — Campus Sinop
> **Tempo estimado:** 3 blocos de 50 min + 1 h de prática

Esta é a primeira aula do Nível 2. Ao final dela você terá um repositório Git publicado na internet, o ambiente de trabalho do semestre inteiro montado e uma ideia clara de onde o Nível 2 vai chegar: uma aplicação full-stack com API própria, login do Google e CRUD persistido.

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Explicar como esta trilha funciona: três unidades, três marcos do projeto, projeto fio-condutor e projeto autoral.
- Descrever o modelo cliente-servidor e narrar, passo a passo, o que acontece entre digitar uma URL e ver a página na tela.
- Identificar os métodos e os códigos de status HTTP mais usados e decompor uma URL em suas partes.
- Distinguir front-end, back-end e banco de dados, e classificar uma aplicação como estática ou dinâmica.
- Montar e **verificar** o ambiente de desenvolvimento (VS Code, navegador com DevTools, Node.js 22 LTS e Git) pela linha de comando.
- Versionar um projeto com Git usando o ciclo `init` → `status` → `add` → `commit` → `log` e publicá-lo no GitHub.
- Colocar um site estático no ar com o GitHub Pages e explicar o que acontece a cada `git push`.

## 📋 Pré-requisitos

No Nível 1 você aprendeu a escrever HTML semântico, estilizar com CSS (layout, responsividade, animações) e programar o comportamento das páginas com JavaScript (variáveis, funções, eventos, validação de formulários). Hoje o Nível 2 pega esse repertório e o coloca dentro de um processo profissional: ambiente configurado, código versionado, projeto publicado. Nas próximas 16 aulas esse mesmo projeto vai crescer até virar uma aplicação com servidor próprio.

Checklist para começar:

- [ ] Um notebook (ou uma máquina do laboratório) com **Google Chrome** ou **Firefox** atualizado.
- [ ] Permissão para instalar programas na máquina — ou, no laboratório, saber que as instalações se perdem no reboot (a §7.5 resolve isso).
- [ ] Uma conta de e-mail que você realmente acessa (vai virar sua conta do GitHub).
- [ ] Uma ideia, mesmo vaga, de **tema para o seu projeto autoral** (§1.5). Você decide hoje ou até a próxima aula.

Você **não** precisa saber Git, terminal ou Node.js. Tudo isso começa do zero hoje.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Como esta trilha funciona; a sequência das aulas e os marcos do projeto; Café Cerrado e o projeto autoral; modelo cliente-servidor |
| 2 | 50 min | HTTP na prática (métodos, status, URL, cabeçalhos); as três camadas; quem consome a web hoje; IA no fluxo de trabalho; ambiente de desenvolvimento |
| 3 | 50 min | Git do zero: ciclo básico, GitHub e GitHub Pages — o repositório `cafe-cerrado` no ar; laboratório |

## 1. Como esta trilha funciona

### 1.1 O que esta trilha cobre

**O que esta trilha cobre** (a mesma ementa da disciplina de origem, Desenvolvimento Web — FACET-SNP-307, UNEMAT Campus Sinop): arquitetura de uma aplicação web; tecnologias de back-end; tecnologias de front-end; bancos de dados para web.

**Objetivo geral:** ao concluir esta trilha você projeta, implementa e publica uma aplicação web completa — interface acessível e responsiva, comportamento dinâmico em JavaScript, API própria em Node.js/Express, autenticação com conta Google e operações de CRUD com persistência.

A palavra que resume o Nível 2 é **profundidade**. No Nível 1 você aprendeu as três linguagens da plataforma. Aqui você aprende a *arquitetura* em que elas vivem: como um site é servido, como duas máquinas conversam por HTTP, como o código sai da sua pasta e vai parar em um endereço público, e como o servidor deixa de ser um mistério e passa a ser código seu.

### 1.2 Três unidades, três camadas

Esta trilha adota **aprendizagem baseada em projeto**: um único aplicativo, construído de forma incremental, ganhando uma camada por unidade.

| Unidade | Camada | Conteúdo |
|---|---|---|
| 1 — Web estática (aulas 01–06) | Interface | Arquitetura web, HTML semântico, frameworks CSS, animação e SVG, acessibilidade e ARIA |
| 2 — Web dinâmica client-side (aulas 07–10) | Comportamento | JavaScript, DOM e eventos, callbacks e vetores, Promises e async/await, AJAX, JSON e SPA |
| 3 — Web dinâmica server-side (aulas 11–16) | Servidor | Node.js e Express, rotas e controladores, autenticação Google, CRUD com front-end assíncrono |

Repare que as unidades são cumulativas: o HTML da Unidade 1 continua lá na Unidade 3, servido pelo seu próprio servidor. Nada é jogado fora.

### 1.3 A sequência das aulas

| Aula | Tema |
|---|---|
| 01 | Apresentação; arquitetura web; ambiente de desenvolvimento e Git |
| 02 | Introdução ao desenvolvimento web moderno |
| 03 | Revisão de HTML: layout, links e formulários |
| 04 | Frameworks CSS |
| 05 | Animação e SVG |
| 06 | Acessibilidade e ARIA |
| 07 | Revisão de JavaScript: objetos, funções, eventos e DOM |
| 08 | Funções, arrow functions, callbacks e vetores |
| 09 | Promises e async/await |
| 10 | AJAX, JSON e Single Page Application |
| 11 | Introdução ao Express |
| 12 | Express estruturado e middlewares |
| 13 | Rotas e controladores |
| 14 | Autenticação com Google (front e back) |
| 15 | CRUD com front-end assíncrono (AJAX/SPA) |
| 16 | CRUD completo com autenticação Google |

O conteúdo abaixo é o mesmo em qualquer turma ou semestre, e serve igualmente a quem estuda por conta própria, sem vínculo com nenhuma turma.

> **⚠️ Atenção**
> Se você depende da rede do laboratório para subir seu trabalho, não deixe para o último minuto: ela tende a cair justamente quando mais gente está enviando ao mesmo tempo. Rode `git push` assim que terminar cada parte, não só no fim da aula.

### 1.4 Os três marcos do projeto

| Marco | Escopo |
|---|---|
| 1 | Website client-side em HTML e CSS: HTML semântico, layout responsivo, framework CSS, animação/SVG, acessibilidade. |
| 2 | Evolução do site com JavaScript: validação de formulários, DOM e eventos, programação assíncrona, SPA com AJAX/JSON. |
| 3 | Aplicação full-stack com Node.js e Express: rotas e controladores, autenticação Google, CRUD com persistência, front-end assíncrono. |

Os três marcos são **individuais**, **práticos** e recaem sobre o **mesmo projeto autoral**. Cada um vive no mesmo repositório público do GitHub — não `.zip`, não pasta no Drive, não print de tela. O repositório *é* o produto, e o histórico de commits faz parte dele.

Esta trilha soma cerca de **60 h de estudo**: aproximadamente 45 h acompanhando as 16 aulas — a construção guiada do projeto fio-condutor — e 15 h de prática independente ligada ao projeto autoral, em atividades de cerca de 1 h por aula.

> **⚠️ Atenção**
> A prática independente não é bônus: ela prepara direto o marco da unidade. Quem pula a atividade de uma aula chega na seguinte sem o pré-requisito, porque cada aula assume que a anterior foi concluída.

### 1.5 O projeto fio-condutor e o projeto autoral

A regra pedagógica do WebLab tem duas metades:

1. **O projeto fio-condutor é o Café Cerrado, construído passo a passo ao longo das aulas.** É uma cafeteria fictícia de Sinop/MT, que torra grãos do cerrado mato-grossense. Na Unidade 1 ela é um site estático publicado no GitHub Pages; na Unidade 2 ganha cardápio dinâmico, busca, filtros e navegação SPA; na Unidade 3 ganha uma API em Express, login com conta Google e um CRUD de produtos com persistência. Digite o código você mesmo — não copie e cole.
2. **Em paralelo, você desenvolve um projeto autoral** com a **mesma arquitetura** e um **domínio diferente**. Os marcos são sobre o projeto autoral.

Exemplos de temas que funcionam: catálogo de plantas do Pantanal, agenda de quadras esportivas, mural de estágios do curso, brechó, controle de pescarias no Teles Pires, loja de peças de bicicleta, biblioteca de uma escola, feira de produtores locais.

O critério para saber se um tema serve é objetivo: **ele tem uma lista de coisas?** Produtos, plantas, quadras, vagas, peças, livros. O semestre inteiro gira em torno de uma coleção de itens que é exibida, filtrada, criada, editada e apagada. Se o seu tema não tem uma lista clara, troque agora — e não na Unidade 3.

> **💡 Dica**
> Escolha um domínio sobre o qual você **tenha conteúdo real**: nomes, preços, descrições, fotos. O erro clássico é escolher "site de uma empresa" e travar na hora de escrever a terceira frase. Tema concreto gera projeto melhor — e mais fácil de defender quando alguém perguntar como funciona.

### 1.6 As quatro camadas de prática de cada aula

Cada aula do WebLab tem, sempre nesta ordem:

1. **💻 Mão na massa** — passo a passo guiado no Café Cerrado. Todo mundo faz junto, digitando (não colando).
2. **🧪 Laboratório** — exercícios práticos em três níveis: **A** (fixação), **B** (aplicação) e **C** (desafio para quem termina antes).
3. **🏆 Desafios** — extras opcionais, com estrelas de dificuldade: ⭐ (1–2 h), ⭐⭐ (uma tarde), ⭐⭐⭐ (um fim de semana). Não são obrigatórios, mas aprofundam a aula e ficam bem no portfólio.
4. **🏠 Atividade assíncrona (1 h)** — a tarefa da semana, ligada ao projeto autoral.

Uma rotina que funciona: leia os objetivos antes da aula; digite o código durante a aula; faça o Laboratório A no mesmo dia; faça o Nível B e a atividade assíncrona ao longo da semana; encare o Nível C e os Desafios se sobrar fôlego.

### 1.7 Uma palavra sobre o formato das entregas

Toda entrega desta trilha é um **link de repositório público no GitHub**. Isso não é burocracia: é a forma como software é entregue no mercado. Um repositório bem cuidado — com `README.md` que explica o projeto, commits com mensagens legíveis e o site publicado — é a peça de portfólio mais barata que existe. Você vai terminar esta trilha com duas: o Café Cerrado e o seu projeto autoral.

## 2. Arquitetura de uma aplicação web

### 2.1 O modelo cliente-servidor

A Web inteira funciona sobre um modelo de duas partes e uma regra:

- **Cliente:** quem pede. Normalmente o navegador, mas também pode ser um aplicativo de celular, um script no terminal (`curl`), outro servidor ou — cada vez mais — um agente de IA.
- **Servidor:** quem responde. Um programa que fica permanentemente escutando em uma porta, esperando requisições.
- **A regra:** o cliente sempre inicia. Em HTTP clássico o servidor nunca manda nada de forma espontânea; ele só responde ao que foi pedido.

```text
     CLIENTE                                            SERVIDOR
   ┌───────────┐          1. requisição HTTP          ┌───────────────┐
   │ Navegador │  ──────────────────────────────────> │  Servidor web │
   │  (você)   │          GET /index.html             │  (Node, nginx,│
   │           │                                      │   Apache…)    │
   │           │  <────────────────────────────────── │               │
   └───────────┘          2. resposta HTTP            └───────────────┘
                          200 OK + HTML
```

Na Unidade 3 você vai escrever o retângulo da direita. Até lá, ele é um serviço que outra pessoa mantém — o GitHub Pages, a partir de hoje.

### 2.2 O que acontece quando você digita um endereço

Esta sequência é uma das perguntas mais frequentes em entrevista técnica. Aprenda a narrá-la.

**Passo 1 — Análise da URL.** O navegador separa o endereço em partes (§3.4) e descobre qual protocolo usar e com quem falar.

**Passo 2 — Resolução DNS.** O nome `cafecerrado.com.br` não serve para roteamento; a rede trabalha com endereços IP. O navegador consulta o **DNS** (Domain Name System) para traduzir o nome em um IP, passando antes por caches: cache do navegador → cache do sistema operacional → arquivo `hosts` → servidor DNS do provedor.

**Passo 3 — Conexão TCP.** Com o IP em mãos, o navegador abre uma conexão TCP, normalmente na porta **80** (HTTP) ou **443** (HTTPS).

**Passo 4 — Handshake TLS** (só em HTTPS). Cliente e servidor negociam a criptografia, o servidor apresenta seu certificado digital e ambos combinam uma chave de sessão. É o que produz o cadeado na barra de endereço.

**Passo 5 — Requisição HTTP.** O navegador envia um texto (§3.1).

**Passo 6 — Processamento no servidor.** Se o recurso for um arquivo estático, o servidor apenas o lê do disco. Se for dinâmico, executa código, possivelmente consulta um banco e monta a resposta na hora.

**Passo 7 — Resposta HTTP.** Uma linha de status, cabeçalhos, uma linha em branco e o conteúdo.

**Passo 8 — Renderização e sub-requisições.** O navegador interpreta o HTML e dispara **novas requisições** para cada recurso referenciado: folhas de estilo, scripts, imagens, fontes. Cada uma repete os passos 5 a 7.

> **📌 Vale gravar**
> A ordem das oito etapas e o papel de cada uma. Os pontos mais cobrados: DNS traduz **nome em IP** (não "acha o site"); TLS é o que torna o HTTP seguro (HTTPS = HTTP + TLS); e uma única página dispara **dezenas** de requisições, não uma.

### 2.3 Uma página não é um arquivo

Abrir uma página comum dispara de 30 a 200 requisições. Isso muda a forma de pensar em desempenho: não adianta otimizar o HTML se a página baixa 4 MB de imagens e cinco fontes. Você vai medir isso na §7.6 e voltar ao tema na Aula 06, quando o Lighthouse entrar em cena.

## 3. HTTP: o idioma entre cliente e servidor

HTTP (*HyperText Transfer Protocol*) é um protocolo de **texto**. Isso é uma decisão de projeto: qualquer pessoa consegue ler uma requisição sem ferramenta especial. Veja.

### 3.1 Anatomia de uma requisição e de uma resposta

Uma requisição:

```http
GET /cardapio.html HTTP/1.1
Host: cafecerrado.exemplo.br
User-Agent: Mozilla/5.0 (X11; Linux x86_64) Chrome/139.0
Accept: text/html,application/xhtml+xml
Accept-Language: pt-BR,pt;q=0.9
Connection: keep-alive
```

A primeira linha diz **o que** se quer (`GET`), **onde** (`/cardapio.html`) e em qual versão do protocolo. As demais são **cabeçalhos** (*headers*): metadados no formato `Nome: valor`.

A resposta correspondente:

```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Length: 3184
Cache-Control: max-age=600
Server: GitHub.com

<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <title>Cardápio — Café Cerrado</title>
</head>
```

Três partes: linha de status (`200 OK`), cabeçalhos, e — depois de **uma linha em branco** — o corpo. Essa linha em branco é o que separa metadados de conteúdo. Guarde: na Unidade 3, quando você escrever `res.status(201).json(produto)` no Express, é exatamente esse texto que sai pela rede.

### 3.2 Métodos

| Método | Para quê | Exemplo (API do Café Cerrado, Unidade 3) |
|---|---|---|
| `GET` | Buscar um recurso. Não altera nada no servidor. | `GET /api/produtos` |
| `POST` | Enviar dados para **criar** algo. | `POST /api/produtos` |
| `PUT` / `PATCH` | Atualizar um recurso existente (inteiro / parcialmente). | `PUT /api/produtos/3` |
| `DELETE` | Remover um recurso. | `DELETE /api/produtos/3` |

Essas quatro operações são exatamente o **CRUD** (*Create, Read, Update, Delete*) que você vai implementar nas Aulas 13, 15 e 16. Repare que o método já diz a intenção: o caminho `/api/produtos` é o mesmo, o que muda é o verbo.

> **⚠️ Atenção**
> `GET` deve ser **seguro**: não pode alterar estado no servidor. Uma rota `GET /apagar-produto/3` funciona tecnicamente e é um erro de projeto grave — buscadores, pré-carregadores do navegador e agentes de IA seguem links `GET` sozinhos, e apagariam seus produtos sem que ninguém clicasse em nada.

### 3.3 Códigos de status

| Faixa | Significado | Exemplos |
|---|---|---|
| `1xx` | Informativo | `100 Continue`, `101 Switching Protocols` |
| `2xx` | Sucesso | `200 OK`, `201 Created`, `204 No Content` |
| `3xx` | Redirecionamento | `301 Moved Permanently`, `302 Found`, `304 Not Modified` |
| `4xx` | Erro do cliente | `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found` |
| `5xx` | Erro do servidor | `500 Internal Server Error`, `502 Bad Gateway`, `503 Service Unavailable` |

Os que você mais vai usar (e devolver) ao longo desta trilha:

| Código | Quando aparece | O que fazer |
|---|---|---|
| `200 OK` | Leitura bem-sucedida | Nada; é o caminho feliz |
| `201 Created` | Recurso criado por um `POST` | Devolver o recurso criado no corpo |
| `400 Bad Request` | Dados inválidos enviados pelo cliente | Explicar no corpo **qual** campo está errado |
| `401 Unauthorized` | Falta autenticação (Aula 14) | Cliente precisa fazer login |
| `403 Forbidden` | Autenticado, mas sem permissão (Aula 16) | Cliente está logado, mas o item é de outra pessoa |
| `404 Not Found` | Recurso inexistente | Verificar o caminho ou o `id` |
| `500 Internal Server Error` | Exceção não tratada no servidor | Ler o log do servidor: o erro é **seu** |

> **💡 Dica**
> Mnemônico que resolve 90% das dúvidas: **`4xx` é culpa de quem pediu; `5xx` é culpa de quem respondeu.** Um `404` diz "você pediu algo que não existe". Um `500` diz "eu quebrei ao tentar responder".

### 3.4 Anatomia de uma URL

```text
https://cafecerrado.exemplo.br:443/cardapio/cafes?categoria=espresso&ordem=preco#promocoes
└─┬─┘   └──────────┬───────────┘└┬┘└───────┬────┘└──────────────┬───────────────┘└───┬───┘
  1                2              3        4                    5                    6
```

| # | Elemento | Nome | Função |
|---|---|---|---|
| 1 | `https` | Esquema | Como falar com o servidor |
| 2 | `cafecerrado.exemplo.br` | Host / domínio | Com quem falar |
| 3 | `443` | Porta | Qual serviço na máquina (80 = HTTP, 443 = HTTPS; omitida quando é a padrão) |
| 4 | `/cardapio/cafes` | Caminho | Qual recurso dentro do servidor |
| 5 | `?categoria=espresso&ordem=preco` | Query string | Parâmetros `chave=valor` separados por `&` |
| 6 | `#promocoes` | Fragmento | Posição dentro da página. **Nunca é enviado ao servidor** |

Dois desses elementos viram protagonistas mais adiante: a **query string** é como a busca do cardápio vai conversar com a API (`GET /api/produtos?q=cafe`, Aula 13), e o **fragmento** é o que faz a navegação SPA funcionar sem recarregar a página (`#/cardapio`, Aula 10). Guarde os dois.

### 3.5 HTTP não tem memória

HTTP é ***stateless***: cada requisição é independente e o servidor, por si só, não lembra o que aconteceu na anterior. Isso parece uma limitação e é, na verdade, o que permitiu a Web escalar — qualquer servidor de um conjunto pode atender qualquer requisição.

Login, carrinho e sessão são construídos **por cima** disso: o cliente reenvia, a cada requisição, uma credencial (um cookie ou um token no cabeçalho `Authorization`). É exatamente o que você vai implementar na Aula 14, quando o Café Cerrado passar a exigir login do Google para escrever dados.

> **🔬 Investigue**
> Abra <https://www.unemat.br>, pressione <kbd>F12</kbd>, vá à aba **Network**, marque *Disable cache* e recarregue com <kbd>Ctrl</kbd>+<kbd>F5</kbd>. Observe quatro coisas: (1) quantas linhas apareceram — cada uma é uma requisição completa dos passos 5 a 7 da §2.2; (2) a coluna *Type* (`document`, `stylesheet`, `script`, `png`, `font`); (3) clique na primeira linha, abra *Headers* e localize `Content-Type`, `Server` e o status; (4) na barra inferior, leia o total de requisições e o peso transferido. Anote os números: você vai comparar com os do seu próprio site no fim da aula.

## 4. Front-end, back-end e banco de dados

Uma aplicação web moderna se organiza em três camadas — que são, não por acaso, as três unidades desta trilha.

| Camada | Onde executa | Responsabilidade | Unidade |
|---|---|---|---|
| Front-end | No navegador do usuário | Estrutura (HTML), apresentação (CSS) e comportamento (JavaScript) | 1 e 2 |
| Back-end | No servidor | Regras de negócio, autenticação, montagem das respostas | 3 |
| Banco de dados | No servidor (ou na nuvem) | Persistir as informações | 3 |

```text
┌──────────────────┐  HTTP  ┌────────────────────┐  SQL/arquivo  ┌───────────────┐
│  APRESENTAÇÃO    │ <────> │     APLICAÇÃO      │ <───────────> │     DADOS     │
│  navegador       │        │  Node.js + Express │               │  JSON, MySQL  │
│  HTML/CSS/JS     │        │  regras de negócio │               │               │
└──────────────────┘        └────────────────────┘               └───────────────┘
     Unidades 1 e 2                 Unidade 3                       Unidade 3
```

Uma regra que vale para sempre: **o navegador nunca fala com o banco de dados**. Se ele falasse, qualquer usuário poderia ler e apagar tudo, porque todo código front-end é público — o usuário pode abrir o DevTools, ler seu JavaScript e alterar valores. Validação no cliente existe para conforto; validação no servidor existe para segurança. Você vai ver essa diferença doer na Aula 13.

### 4.1 Site estático × aplicação dinâmica

| | Site estático | Aplicação dinâmica |
|---|---|---|
| Como o HTML é obtido | Arquivo pronto, lido do disco | Gerado a cada requisição por código |
| Conteúdo | Igual para todos | Varia por usuário, hora, dados |
| Custo de hospedagem | Baixíssimo ou grátis | Servidor de aplicação (+ banco) |
| Exemplo | Portfólio, cardápio, documentação | SIGAA, e-commerce, rede social |

> **⚠️ Atenção**
> "Dinâmico", em arquitetura, significa **HTML montado no servidor**. Uma página estática cheia de JavaScript, animações e busca continua sendo estática do ponto de vista arquitetural — é o caso do Café Cerrado até a Aula 10. É por isso que ele pode ficar hospedado de graça no GitHub Pages durante duas unidades inteiras.

## 5. Quem está do outro lado hoje

Durante trinta anos a resposta era óbvia: do outro lado da requisição havia uma pessoa olhando uma tela. Isso mudou.

Relatórios de tráfego da web (Imperva/Thales, Cloudflare Radar) mostram que **mais da metade do tráfego web já é gerada por máquinas** — a primeira vez em uma década em que os bots ultrapassaram os humanos. O crescimento vem principalmente de agentes de IA: em 2025 o tráfego de bots de IA cresceu quase 190%, enquanto o tráfego humano cresceu cerca de 3%. O volume de rastreamento para treinar modelos chegou a várias vezes o volume de rastreamento dos buscadores tradicionais.

E essas máquinas já são clientes que pagam:

- **x402** (proposto pela Coinbase) ressuscitou o código de status HTTP `402 Payment Required`, reservado desde os anos 90 e nunca usado de verdade. O agente faz uma requisição, recebe `402` com o preço, paga e refaz a requisição — sem checkout, sem cadastro, sem humano.
- **Redes de pagamento para agentes** (Mastercard Agent Pay, Visa Trusted Agent Protocol, AP2 do Google) dão identidade e meio de pagamento a programas.
- **MCP** (*Model Context Protocol*), aberto em 2024 e doado à Linux Foundation, padronizou a forma de conectar assistentes de IA a dados e ferramentas. Milhares de serviços já expõem "portas para agentes" em vez de telas para humanos.

> **🧠 Você sabia?**
> O código `402 Payment Required` está na especificação do HTTP desde 1997 marcado como "reservado para uso futuro". Ficou quase três décadas sem uso prático — um número guardado à espera de um caso que só apareceu quando as máquinas viraram compradoras. Vale como lembrete de que o HTTP que você está aprendendo é um protocolo vivo: os mesmos verbos e os mesmos códigos de 1997 continuam sustentando o que se inventa hoje.

**Por que isso importa para o que você vai construir aqui?** Porque muda o que é "a fachada" de um sistema. O agente não quer o botão azul: ele quer o dado, em JSON, por uma API previsível e documentada. A interface humana continua importando — mas ela passa a ser *uma* das saídas, não a única.

A boa notícia é que tudo que você vai aprender aqui serve aos dois públicos. HTML semântico (Aula 03) é o que permite a uma máquina entender a estrutura da página. HTTP bem usado (§3) é o que torna a API previsível. JSON (Aula 10) é o formato que os dois lados falam. Express e rotas REST (Unidade 3) são a porta de entrada. Ninguém precisa mudar de assunto: precisa aprender o assunto direito.

## 6. IA no desenvolvimento: ferramenta, não atalho

A pergunta não é "pode usar IA?". Pode. A pergunta é "como usar bem?".

**A favor de usar.** Assistentes de código escrevem o repetitivo — estrutura inicial, testes, documentação, refatorações mecânicas — e liberam você para o que decide o resultado: arquitetura, modelagem de dados, experiência do usuário. Pesquisas de mercado apontam que a grande maioria dos desenvolvedores já usa algum assistente ao menos uma vez por mês, e que quem usa diariamente entrega bem mais mudanças por semana. Ficar de fora não é pureza técnica; é desvantagem competitiva.

**Contra usar sem critério.** Um estudo controlado da METR (2025) mediu desenvolvedores experientes trabalhando em bases de código que dominavam: quando usaram IA, ficaram em média **19% mais lentos** — e ainda assim acharam que tinham ficado mais rápidos. Ferramenta sem domínio do problema atrapalha e dá a sensação contrária.

**Então por que estudar HTTP, DOM e Express a fundo, se a IA escreve isso?** Pelo mesmo motivo pelo qual você estuda Arquitetura de Computadores sem programar em Assembly no dia a dia: para entender o que acontece por baixo quando quebra. A IA escreve o código; quem julga se ele está correto, seguro e bem arquitetado é você. E só revisa bem quem entende a base.

**Use IA como apoio, não como atalho:** peça para ela explicar, não para resolver o que você ainda não entende. O teste real é simples — se você não consegue explicar uma linha do seu código, ela ainda não é sua.

> **💡 Dica**
> Um uso honesto e produtivo desde já: peça ao assistente para **explicar** um erro do terminal, não para "consertar o projeto". Cole a mensagem literal, pergunte o que ela significa e o que a causa. Você aprende a ler a mensagem — que é a habilidade que vai sobrar quando a ferramenta mudar de nome.

## 7. Ambiente de desenvolvimento

### 7.1 O que instalar nesta semana

| Ferramenta | Para quê | Onde obter |
|---|---|---|
| Visual Studio Code | Editor de código | <https://code.visualstudio.com/> |
| Google Chrome ou Firefox | Navegador com DevTools | Site do fabricante |
| Node.js 22 LTS | Executar JavaScript fora do navegador (ferramentas agora; servidor na Unidade 3) | <https://nodejs.org/> |
| Git | Controle de versão | <https://git-scm.com/> |

Sobre o Node.js: baixe sempre a versão marcada como **LTS** (*Long Term Support*). LTS significa suporte prolongado e estabilidade — é a versão que se usa em produção. Nesta trilha usamos o **Node.js 22 LTS**.

### 7.2 Verificando as instalações pelo terminal

Instalar não basta: é preciso confirmar que o sistema encontra os programas. Abra um terminal (no VS Code, <kbd>Ctrl</kbd>+<kbd>'</kbd>) e execute:

```bash
node -v
npm -v
git --version
code --version
```

Saída esperada (os números podem variar um pouco):

```text
v22.13.0
10.9.2
git version 2.43.0
1.96.2
```

Se algum comando responder `command not found` (Linux/macOS) ou `não é reconhecido como um comando interno ou externo` (Windows), o programa foi instalado mas não está no `PATH` — normalmente basta **fechar e abrir o terminal** de novo, porque o `PATH` só é lido na abertura. Se persistir, reinstale marcando a opção "adicionar ao PATH".

> **🔎 Por baixo do capô**
> `PATH` é uma variável de ambiente com uma lista de pastas. Quando você digita `node`, o sistema não procura no computador inteiro: ele percorre essa lista, na ordem, procurando um executável com esse nome. É por isso que a instalação precisa "adicionar ao PATH" e por que o terminal aberto antes da instalação não enxerga o programa novo — ele guardou a lista antiga.

### 7.3 Extensões do VS Code

| Extensão | Para quê |
|---|---|
| Live Server (Ritwick Dey) | Servidor local com recarga automática ao salvar |
| Prettier – Code formatter | Formatação automática do código |
| Portuguese (Brazil) Language Pack | Interface do editor em português (opcional) |

Instale-as com <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>X</kbd>. Depois, em *File → Preferences → Settings*, procure `format on save` e marque a opção: seu código passa a ser formatado a cada <kbd>Ctrl</kbd>+<kbd>S</kbd>. Isso elimina uma categoria inteira de discussão inútil sobre indentação — inclusive com você mesmo daqui a três semanas.

### 7.4 Abra a **pasta**, não o arquivo

Regra permanente: no VS Code, use *File → Open Folder* e abra a **pasta raiz** do projeto. Nunca abra um `.html` solto. Live Server, caminhos relativos, terminal integrado e Git dependem de haver uma pasta raiz — e metade dos problemas de aula 1 vem de ignorar isso.

### 7.5 Trabalhando no laboratório

Nas máquinas do laboratório as instalações podem se perder entre uma aula e outra. Duas defesas:

1. **Seu código vive no GitHub, não na máquina.** Esse é o ponto principal da §8: qualquer computador com Git baixa seu projeto inteiro em um comando.
2. **Configure o Git no início de cada aula**, se necessário. São dois comandos (§8.3) e levam dez segundos.

### 7.6 DevTools: o raio-X do navegador

Pressione <kbd>F12</kbd> (ou botão direito → *Inspecionar*). Você vai usar isto todos os dias do semestre.

| Aba | Para que serve |
|---|---|
| **Elements** | Ver e editar o DOM e o CSS aplicado, ao vivo |
| **Console** | Mensagens de erro e execução de JavaScript |
| **Network** | Todas as requisições: método, status, tipo, tamanho, tempo |
| **Sources** | Ver os arquivos e depurar JavaScript com pontos de parada |
| **Application** | Cookies, `localStorage` e armazenamento do site |
| **Lighthouse** | Auditoria de desempenho, acessibilidade e SEO (protagonista na Aula 06) |

## 8. Git: controle de versão desde o dia 1

### 8.1 O problema que o Git resolve

Você já viu (ou já criou) uma pasta assim:

```text
projeto/
├── site.html
├── site_v2.html
├── site_v2_corrigido.html
├── site_final.html
├── site_final_MESMO.html
└── site_final_agora_vai.html
```

Isso é controle de versão manual — e ele falha em tudo o que importa: você não sabe **o que** mudou entre duas versões, nem **por quê**, nem **quando**, nem como voltar a um estado intermediário sem quebrar o resto.

O **Git** resolve isso registrando *fotografias* do projeto inteiro ao longo do tempo. Cada fotografia é um **commit**: o estado completo dos arquivos, mais autor, data e uma mensagem explicando a intenção. Com isso você consegue voltar no tempo, comparar duas versões linha a linha, descobrir quando um bug entrou e trabalhar com segurança porque nada se perde.

### 8.2 Os três estados de um arquivo

```text
   working directory          staging area              repositório
   ┌────────────────┐  add   ┌───────────────┐  commit  ┌──────────────┐
   │  MODIFICADO    │ ─────> │   PREPARADO   │ ───────> │  VERSIONADO  │
   │ você editou    │        │ vai entrar no │          │  histórico   │
   │ o arquivo      │        │ próximo commit│          │  permanente  │
   └────────────────┘        └───────────────┘          └──────────────┘
```

A **staging area** (área de preparação) é o que confunde no começo e o que dá poder ao Git: ela deixa você escolher *quais* mudanças entram no próximo commit. Editou cinco arquivos mas só três formam uma mudança coerente? Prepare esses três, faça o commit, depois cuide do resto. Commits coerentes são o que torna o histórico legível.

### 8.3 Configuração inicial (uma única vez por máquina)

```bash
git config --global user.name "Seu Nome Completo"
git config --global user.email "seu-email@exemplo.com"
git config --global init.defaultBranch main
git config --global core.editor "code --wait"
```

Confira o que ficou gravado e de onde veio cada configuração:

```bash
git config --list --show-origin
```

> **⚠️ Atenção**
> Use o **mesmo e-mail** da sua conta do GitHub. É por ele que o GitHub associa os commits ao seu perfil. Com um e-mail diferente, seus commits aparecem como se fossem de um desconhecido — e, em uma entrega avaliada, isso vira dúvida sobre autoria.

### 8.4 O ciclo básico

```bash
# 1. transformar a pasta atual em um repositório Git
git init

# 2. ver o que mudou e em que estado está
git status

# 3. preparar arquivos para o commit
git add index.html      # um arquivo específico
git add .               # tudo que mudou na pasta atual e subpastas

# 4. registrar a fotografia com uma mensagem descritiva
git commit -m "Cria a página inicial do Café Cerrado"

# 5. ver o histórico
git log --oneline
```

Dois comandos que não estavam no roteiro clássico e que você vai usar muito:

```bash
# ver exatamente o que mudou, linha a linha, antes de preparar
git diff

# descartar as alterações não preparadas de um arquivo
git restore index.html
```

`git status` é o comando mais importante da lista. Ele não só mostra o estado como **sugere o comando seguinte**. Quando estiver perdido, rode `git status` e leia com calma — a resposta costuma estar ali.

### 8.5 Mensagens de commit que servem para alguma coisa

Uma mensagem de commit responde à pergunta "o que este commit faz?". Escreva no **imperativo**, como se completasse a frase "Este commit…".

| Ruim | Boa |
|---|---|
| `alterações` | `Cria a estrutura inicial do site` |
| `aula 3` | `Adiciona formulário de contato com validação nativa` |
| `arrumei` | `Corrige quebra do menu em telas menores que 480px` |
| `.` | `Remove imagens não utilizadas da pasta img` |

Commits pequenos e frequentes valem mais do que um commit gigante no fim da semana. Regra prática: **um commit por ideia concluída**. Terminou o cabeçalho? Commit. Terminou o rodapé? Commit.

> **🔎 Por baixo do capô**
> Um commit não é "a diferença desde o anterior": é um instantâneo completo da árvore de arquivos, identificado por um hash (aquela sequência tipo `a3f9c21`) calculado a partir do conteúdo, do autor, da data, da mensagem e do commit anterior. Como o hash depende do commit anterior, alterar qualquer coisa no passado muda todos os hashes seguintes — é por isso que o histórico do Git é praticamente à prova de adulteração, e é por isso que `git log` conta uma história confiável.

### 8.6 O `.gitignore`

Nem tudo deve entrar no repositório: arquivos gerados, dependências baixadas, configurações da sua máquina e — nunca esqueça — **segredos**. O arquivo `.gitignore`, na raiz do projeto, lista o que o Git deve ignorar:

```text
# Sistema operacional
.DS_Store
Thumbs.db

# Editor
.vscode/

# Node.js (a partir da Unidade 3)
node_modules/

# Segredos: chaves e senhas nunca entram no repositório
.env
```

Duas dessas linhas evitam desastres reais. `node_modules/` costuma ter dezenas de milhares de arquivos e é reconstruído com um `npm install` — versionar isso é entupir o repositório à toa. E `.env` é onde, na Aula 14, ficará o seu Client ID do Google: um arquivo desses vazado em repositório público é o tipo de erro que rende notícia.

### 8.7 Repositório remoto: GitHub

O Git é a ferramenta; o **GitHub** é um serviço que hospeda repositórios Git na internet. Ele dá três coisas ao mesmo tempo: backup, portfólio público e o canal de entrega desta trilha.

```bash
# conectar o repositório local ao remoto criado no GitHub
git remote add origin https://github.com/SEU-USUARIO/cafe-cerrado.git
git branch -M main
git push -u origin main

# nos próximos envios, basta:
git push
```

O que cada linha faz:

- `git remote add origin URL` cadastra um apelido (`origin`) para o endereço do repositório remoto.
- `git branch -M main` renomeia a branch atual para `main`, que é o nome padrão no GitHub.
- `git push -u origin main` envia os commits e memoriza a associação; o `-u` é o que permite escrever só `git push` depois.

E, para trazer para a máquina um repositório que já existe (o caso de trocar de computador ou usar o laboratório):

```bash
git clone https://github.com/SEU-USUARIO/cafe-cerrado.git
```

> **💡 Dica**
> O GitHub não aceita mais senha da conta na linha de comando. Ao pedir autenticação, use um **Personal Access Token** (em *Settings → Developer settings → Personal access tokens*) no lugar da senha, ou configure uma chave SSH. No Windows, o Git Credential Manager instalado junto com o Git abre uma janela de login do navegador e resolve isso sozinho.

### 8.8 GitHub Pages: seu primeiro deploy

Todo repositório **público** do GitHub pode virar um site estático publicado, de graça:

1. No repositório, acesse *Settings → Pages*.
2. Em *Source*, escolha *Deploy from a branch*, a branch `main` e a pasta raiz (`/ (root)`).
3. Salve. Em alguns minutos o site estará em `https://SEU-USUARIO.github.io/cafe-cerrado/`.

A partir daí, **cada `git push` republica o site automaticamente**. Esse é o seu primeiro fluxo de deploy: você edita, commita, envia, e o mundo vê. Guarde a sensação — na Unidade 3 o mesmo raciocínio vale para uma API, com algumas camadas a mais.

## 💻 Mão na massa — o repositório `cafe-cerrado` no ar

Objetivo do bloco: sair da aula com o Café Cerrado publicado em um endereço público, versionado, com dois commits e um `README.md` decente.

### Passo 1 — Criar a pasta e abrir no VS Code

Crie, em um lugar que você encontre depois (por exemplo `Documentos/dev-web/`), a pasta `cafe-cerrado`. Abra o VS Code e use *File → Open Folder* apontando para ela.

```text
dev-web/
├── cafe-cerrado/        ← projeto fio-condutor (construído ao longo das aulas)
└── meu-projeto/         ← projeto autoral (tema seu, mesma arquitetura)
```

> **⚠️ Atenção**
> Nomes de arquivos e pastas em **minúsculas, sem espaços, sem acentos**, com hífen separando palavras: `cafe-cerrado`, nunca `Café Cerrado`. Servidores Linux — inclusive o do GitHub Pages — diferenciam maiúsculas de minúsculas, e o que funciona no seu Windows quebra ao publicar.

### Passo 2 — A página inicial mínima

Crie o arquivo `index.html` na raiz da pasta. Digite (não cole):

`cafe-cerrado/index.html`

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Café Cerrado — cafeteria em Sinop/MT</title>
</head>
<body>
  <h1>Café Cerrado</h1>
  <p>Cafeteria de grãos torrados do cerrado mato-grossense, em Sinop/MT.</p>
  <p>Site em construção no Nível 2 do WebLab (Desenvolvimento Web — UNEMAT Campus Sinop).</p>
</body>
</html>
```

O nome `index.html` não é decorativo: é a **convenção** que todo servidor web segue para decidir o que entregar quando alguém pede a pasta em vez de um arquivo. Pedir `https://exemplo.br/` entrega `https://exemplo.br/index.html`.

Abra a página com o Live Server (botão *Go Live*, canto inferior direito) e confirme que os acentos aparecem corretos. Leia a URL que abriu — algo como `http://127.0.0.1:5500/index.html` — com a §3.4 na cabeça: esquema `http`, host `127.0.0.1`, porta `5500`, caminho `/index.html`. Você acabou de subir um servidor web na sua própria máquina.

### Passo 3 — O `README.md`

O `README.md` é a primeira coisa que o GitHub mostra a quem abre o repositório — e a primeira coisa que qualquer pessoa lê para decidir se vale a pena continuar explorando o projeto. Crie-o na raiz:

`cafe-cerrado/README.md`

```markdown
# Café Cerrado

Site da cafeteria fictícia **Café Cerrado** (Sinop/MT), construído aula a aula
no Nível 2 do WebLab (Desenvolvimento Web — FACET-SNP-307, UNEMAT Campus Sinop).

## O projeto

Uma cafeteria que torra grãos do cerrado mato-grossense. O site apresenta a
casa, o cardápio e um canal de contato. Ao longo do semestre ele evolui de
página estática para aplicação com API própria.

## Site publicado

https://SEU-USUARIO.github.io/cafe-cerrado/

## Tecnologias

HTML5 e CSS3. JavaScript entra na Unidade 2; Node.js e Express, na Unidade 3.

## Como executar localmente

1. Clone o repositório.
2. Abra a pasta no VS Code.
3. Clique em "Go Live" (extensão Live Server).

## Autoria

Seu Nome — Desenvolvimento Web, UNEMAT Sinop.
```

Troque `SEU-USUARIO` e `Seu Nome` pelos seus. O `.md` é **Markdown**, a mesma linguagem em que estas aulas são escritas: `#` faz título, `**texto**` deixa em negrito, `-` faz lista.

### Passo 4 — O `.gitignore`

`cafe-cerrado/.gitignore`

```text
# Sistema operacional
.DS_Store
Thumbs.db

# Editor
.vscode/

# Node.js (a partir da Unidade 3)
node_modules/

# Segredos
.env
```

O arquivo começa com ponto, então alguns gerenciadores de arquivos o escondem. No VS Code ele aparece normalmente.

### Passo 5 — Primeiro commit

No terminal integrado do VS Code (<kbd>Ctrl</kbd>+<kbd>'</kbd>), confirme que você está na pasta certa e execute:

```bash
git init
git status
git add .
git status
git commit -m "Cria a estrutura inicial do site do Cafe Cerrado"
git log --oneline
```

Rode `git status` **duas vezes**, como está acima, e compare as saídas. Na primeira, os arquivos aparecem em vermelho sob *Untracked files*; na segunda, em verde sob *Changes to be committed*. Você acabou de ver a staging area da §8.2 funcionando.

A saída de `git log --oneline` deve ser parecida com:

```text
7c1f4ab (HEAD -> main) Cria a estrutura inicial do site do Cafe Cerrado
```

Esse `7c1f4ab` é o início do hash do commit. É o endereço permanente desta fotografia.

### Passo 6 — Criar o repositório no GitHub e enviar

1. Acesse <https://github.com>, faça login e clique em *New repository*.
2. Nome: `cafe-cerrado`. Visibilidade: **Public**.
3. **Não** marque "Add a README file", "Add .gitignore" nem "Choose a license" — você já criou o que precisa localmente, e marcar essas opções cria commits no remoto que vão conflitar com os seus.
4. Clique em *Create repository* e copie a URL exibida.

De volta ao terminal:

```bash
git remote add origin https://github.com/SEU-USUARIO/cafe-cerrado.git
git branch -M main
git push -u origin main
```

Atualize a página do GitHub: seus três arquivos estão lá, e o `README.md` aparece renderizado embaixo da lista.

### Passo 7 — Ligar o GitHub Pages

1. No repositório, vá em *Settings → Pages*.
2. Em *Source*, selecione *Deploy from a branch*; em *Branch*, escolha `main` e a pasta `/ (root)`. Clique em *Save*.
3. Aguarde de um a três minutos e recarregue a página de *Settings → Pages*: aparece o endereço `https://SEU-USUARIO.github.io/cafe-cerrado/`.

Abra esse endereço no celular também. É a mesma página que estava na sua máquina, agora servida da internet para o mundo.

### Passo 8 — O segundo commit: fechando o ciclo

Edite o `README.md`, colando a URL real do site publicado no lugar de `SEU-USUARIO`. Depois:

```bash
git status
git diff
git add README.md
git commit -m "Registra o endereco do site publicado no README"
git push
```

Espere um minuto e recarregue o site publicado. Ele mudou sozinho: você acabou de fazer um deploy sem clicar em nada além de `git push`.

### Passo 9 — O projeto autoral começa hoje

Repita os passos 1 a 7 na pasta `meu-projeto`, com o **seu** tema: nome do projeto no `<title>` e no `<h1>`, um parágrafo dizendo o que é e para quem é, um `README.md` com o tema e as páginas que você pretende ter. Repositório público, GitHub Pages ligado.

A partir de hoje a regra é: **o que o Café Cerrado ganha em aula, o seu projeto ganha em paralelo.**

### Como testar

- `git log --oneline` mostra **dois** commits, com mensagens legíveis no imperativo.
- `git status` responde `nothing to commit, working tree clean`.
- O repositório `cafe-cerrado` aparece público no seu perfil do GitHub, com `index.html`, `README.md` e `.gitignore`.
- `https://SEU-USUARIO.github.io/cafe-cerrado/` abre a página com os acentos corretos, inclusive no celular.
- No DevTools do site publicado, aba **Network**, o `index.html` aparece com status `200` e o cabeçalho de resposta `Server: GitHub.com`.
- O mesmo checklist vale para o repositório do seu projeto autoral.

**Resultado esperado:** dois sites estáticos publicados na internet, versionados com Git, com histórico limpo e `README.md` que explica o projeto.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Explique, em no máximo quatro linhas, a diferença entre **cliente** e **servidor** no modelo da §2.1, e diga quem inicia a conversa.

**A2.** Coloque em ordem as oito etapas da §2.2: (a) resposta HTTP; (b) resolução DNS; (c) renderização e sub-requisições; (d) conexão TCP; (e) requisição HTTP; (f) análise da URL; (g) handshake TLS; (h) processamento no servidor.

**A3.** Decomponha a URL abaixo, nomeando as seis partes da §3.4:

```text
https://loja.cafecerrado.com.br:8443/produtos/moidos?origem=chapada&ordem=preco#avaliacoes
```

**A4.** Diga qual método HTTP e qual código de status você usaria em cada situação: (a) listar os produtos do cardápio; (b) cadastrar um produto novo com sucesso; (c) pedir um produto que não existe; (d) enviar um formulário com o campo preço em branco; (e) o servidor lançou uma exceção não tratada.

**A5.** O que significa dizer que o HTTP é *stateless*? Cite uma consequência prática disso para uma tela de login.

**A6.** Explique os três estados de um arquivo no Git e diga qual comando move o arquivo de um estado para o outro.

**A7.** Reescreva estas mensagens de commit no padrão da §8.5: `alterações`, `aula 1`, `arrumei o css`, `commit final agora vai`.

**A8.** Cite três tipos de arquivo que **não** devem entrar em um repositório e explique o porquê de cada um.

**A9.** Um site estático e uma aplicação dinâmica devolvem HTML para o navegador. Qual é, então, a diferença entre os dois? Classifique: SIGAA, cardápio do Café Cerrado na Unidade 1, portfólio pessoal, loja virtual.

**A10.** O que o comando `git push -u origin main` faz? Explique cada uma das quatro partes (`push`, `-u`, `origin`, `main`).

### Nível B — Aplicação

**B1.** Use a aba **Network** do DevTools para comparar três sites: um portal de notícias, um e-commerce e o seu `https://SEU-USUARIO.github.io/cafe-cerrado/`. Para cada um, registre: número de requisições, peso total transferido, tempo até o *Load* e qual foi o maior recurso. Escreva um parágrafo levantando hipóteses para as diferenças.

**Resultado esperado:** uma tabela com três linhas e quatro medidas, mais um parágrafo de análise (por exemplo, "o portal fez 4× mais requisições por causa de anúncios e rastreadores").

<details markdown="1">
<summary>Dica</summary>

Marque *Disable cache* antes de medir, senão a segunda visita vem do cache e distorce tudo. A barra inferior da aba Network resume "N requests | X MB transferred | Finish: Y s". Para achar o maior recurso, clique no cabeçalho da coluna *Size* para ordenar.
</details>

**B2.** Plante e resolva um erro: no seu `index.html` publicado, apague a linha `<meta charset="UTF-8">`, faça commit e push. Espere o Pages republicar e abra o site. Descreva o que aconteceu com os acentos e explique por quê. Depois, desfaça — e faça o commit da correção com uma mensagem que descreva o conserto.

**Resultado esperado:** dois novos commits no histórico — o que quebra e o que conserta, ambos com mensagens claras — mais uma explicação de 3 a 5 linhas sobre o papel do `charset` na interpretação dos bytes.

<details markdown="1">
<summary>Dica</summary>

Sem a declaração de charset, o navegador precisa adivinhar a codificação e frequentemente escolhe uma tabela de um byte por caractere, exibindo `Ã§` no lugar de `ç`. Para desfazer antes do commit, `git restore index.html` devolve o arquivo ao último estado versionado.
</details>

**B3.** Escreva o histórico de commits de uma tarefa real. Adicione ao `index.html` do Café Cerrado, em quatro etapas independentes, cada uma com **seu próprio commit**: (1) um parágrafo com o endereço da cafeteria; (2) um parágrafo com o horário de funcionamento; (3) um link `mailto:` para contato; (4) o ano de fundação. Ao final, rode `git log --oneline` e confira se o histórico conta a história sozinho.

**Resultado esperado:** quatro commits, um por mudança, com mensagens no imperativo; `git log --oneline` legível por alguém que não viu o código.

<details markdown="1">
<summary>Dica</summary>

Use `git add index.html` e `git commit` depois de **cada** alteração, não no fim. Se você fizer as quatro e commitar uma vez só, refaça o exercício — o objetivo é justamente sentir a diferença de granularidade.
</details>

**B4.** Investigue o certificado HTTPS do seu site publicado. Clique no cadeado do navegador e registre: quem emitiu o certificado, para qual domínio ele é válido, até quando vale. Explique em três linhas o que o Passo 4 da §2.2 tem a ver com esses dados.

**Resultado esperado:** três dados anotados e uma explicação ligando certificado, autoridade certificadora e a chave de sessão negociada no handshake TLS.

<details markdown="1">
<summary>Dica</summary>

No Chrome: cadeado → *A conexão é segura* → *O certificado é válido*. O emissor é a autoridade certificadora; é ela que garante ao navegador que o servidor é mesmo quem diz ser. Compare com o certificado de <https://www.unemat.br>.
</details>

**B5.** Escreva um `README.md` decente para o seu **projeto autoral**, com: título, um parágrafo explicando o tema e o público, a lista de páginas previstas, as tecnologias, como executar localmente e o link do site publicado. Commit e push.

**Resultado esperado:** o `README.md` renderizado na página inicial do repositório, com pelo menos quatro seções e nenhum trecho copiado do modelo do Café Cerrado sem adaptação.

<details markdown="1">
<summary>Dica</summary>

O GitHub renderiza Markdown: `#` e `##` para títulos, `-` para listas, `**negrito**`, e links no formato `[texto](url)`. Prévia no VS Code: <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>V</kbd>.
</details>

### Nível C — Desafio

**C1.** Recuperação de desastre. Simule a perda da máquina: apague (de verdade, ou renomeie) a pasta local `cafe-cerrado`, clone o repositório do GitHub em outro diretório, confirme que os dois commits estão lá, faça uma alteração no `README.md`, commite e envie. Depois, responda por escrito: o que exatamente foi recuperado no `git clone` — só os arquivos atuais, ou o histórico inteiro? Comprove sua resposta com a saída de um comando.

<details markdown="1">
<summary>Dica</summary>

`git clone` traz a pasta `.git` inteira, e é ela que guarda o histórico. Comprove com `git log --oneline` dentro do clone: se os dois commits originais aparecem com os mesmos hashes, você recuperou o histórico, não apenas os arquivos.
</details>

**C2.** Meça o custo do HTTPS. No terminal, use `curl` para medir os tempos de uma requisição ao seu site publicado e a um site qualquer em HTTP simples, comparando o tempo de resolução DNS, de conexão TCP e de handshake TLS. Monte uma tabela com os três tempos para cada site e escreva um parágrafo sobre onde o tempo é gasto.

<details markdown="1">
<summary>Dica</summary>

`curl` aceita um formato de saída com variáveis de tempo: experimente `curl -o /dev/null -s -w "dns=%{time_namelookup} tcp=%{time_connect} tls=%{time_appconnect} total=%{time_total}\n" https://SEU-USUARIO.github.io/cafe-cerrado/`. Rode duas vezes seguidas e observe o efeito do cache de DNS na segunda.
</details>

## 🏆 Desafios

### ⭐ Um repositório que se explica sozinho
Tags: git, github, projeto

Um recrutador abre o seu GitHub e olha um repositório por, em média, alguns segundos. Nesse tempo ele decide se você sabe trabalhar ou se apenas entregou uma tarefa. A diferença raramente está no código: está no `README.md`, no histórico de commits e em haver (ou não) um link funcionando. Pegue o repositório do seu projeto autoral e transforme-o em uma peça de portfólio.

**Critérios de pronto**

- `README.md` com: título, descrição do tema em um parágrafo, público-alvo, lista de páginas previstas, tecnologias, instruções para executar localmente e o link do site publicado, funcionando.
- Pelo menos **seis** commits, todos com mensagens no imperativo, nenhuma com menos de três palavras, nenhuma genérica (`alterações`, `update`, `aula`).
- `.gitignore` presente e adequado ao projeto.
- A descrição curta do repositório (campo *About*, no topo da página do GitHub) preenchida, com o link do site publicado no campo *Website*.
- Um parágrafo, entregue junto, explicando por que você organizou os commits daquela forma.

<details markdown="1">
<summary>Pistas</summary>

1. Leia três `README.md` de projetos populares no GitHub e anote o que os três têm em comum.
2. O campo *About* fica no canto superior direito da página do repositório, na engrenagem ao lado do nome.
3. Se o seu histórico já estiver ruim, não apague nada: faça os próximos commits bem feitos e explique a virada no parágrafo final. Histórico é biografia, não maquiagem.
4. `git log --oneline` é o teste final: leia a saída em voz alta. Se ela conta a história do projeto, está pronto.
</details>

### ⭐⭐ A viagem de um GET
Tags: http, terminal, devtools, investigacao

O navegador esconde tudo o que a §2.2 descreve. Hoje você faz o trabalho dele na mão: dispara requisições HTTP sem navegador, lê a resposta crua e mede onde o tempo é gasto. A ferramenta é o `curl`, que já vem no Windows 10+, no macOS e na maioria das distribuições Linux. Ao final você deve conseguir explicar cada uma das oito etapas com evidência na tela.

**Critérios de pronto**

- A saída de `curl -v https://SEU-USUARIO.github.io/cafe-cerrado/` salva em arquivo, com anotações marcando: resolução do nome, conexão TCP, handshake TLS (protocolo negociado e emissor do certificado), requisição enviada (linhas com `>`) e resposta recebida (linhas com `<`).
- A saída de `curl -I` no mesmo endereço, com a explicação, em uma linha cada, de pelo menos cinco cabeçalhos de resposta.
- Uma requisição a um caminho inexistente do seu site e a interpretação do status recebido, comparada com o que o navegador mostra na mesma situação.
- Uma comparação entre `curl --http1.1 -I` e `curl --http2 -I` no mesmo endereço: qual versão o servidor aceitou e como você sabe.
- Um texto de dez linhas ligando cada evidência ao passo correspondente da §2.2, escrito como se você fosse explicar o processo para outra pessoa que não acompanhou este trecho.

<details markdown="1">
<summary>Pistas</summary>

1. `curl --version` confirma a instalação e lista os protocolos suportados (procure `HTTP2` na linha *Features*).
2. Em `-v`, linhas com `*` são informações da conexão; `>` é o que foi enviado; `<` é o que voltou.
3. Se houver redirecionamento (`301`/`302`), acrescente `-L` para seguir e observe as duas respostas em sequência.
4. A primeira linha da resposta (`HTTP/2 200` ou `HTTP/1.1 200 OK`) já denuncia a versão negociada.
</details>

### ⭐⭐ Quem responde por este site?
Tags: http, devtools, dns, investigacao

Toda resposta HTTP carrega pistas sobre a infraestrutura que a produziu: qual software serviu, se passou por uma CDN, quanto tempo o arquivo pode ficar em cache. Vire detetive: escolha quatro sites (o da UNEMAT, um jornal, um e-commerce e o seu site publicado) e descubra, só pelos cabeçalhos e por consultas de DNS, como cada um é entregue.

**Critérios de pronto**

- Para cada site, uma tabela com `Server`, `Content-Type`, `Cache-Control` e pelo menos um cabeçalho que revele CDN (`cf-ray`, `x-served-by`, `via`, `x-cache`).
- A classificação de cada site em "servido direto" ou "servido via CDN", com a evidência que sustenta a conclusão.
- O resultado de `nslookup` (ou `dig`) para cada domínio, com o IP resolvido, e uma observação sobre quantos IPs cada nome devolve.
- Uma linha por site explicando o que o valor de `Cache-Control` significa na prática para quem visita a página duas vezes.
- Uma conclusão de cinco linhas sobre por que sites grandes usam CDN.

<details markdown="1">
<summary>Pistas</summary>

1. Aba Network → clique na primeira linha (o documento) → *Headers* → role até *Response Headers*.
2. Cloudflare deixa `cf-ray` e `server: cloudflare`; Fastly deixa `x-served-by`; Akamai costuma deixar `server: AkamaiGHost`.
3. `Server` ausente também é resposta: alguns sites escondem o software de propósito, por segurança.
4. Um nome que devolve vários IPs geralmente está atrás de balanceamento ou de uma CDN — compare os IPs consultando de redes diferentes (celular e Wi-Fi).
</details>

### ⭐⭐⭐ Volte no tempo
Tags: git, github, investigacao, refatoracao

O valor real do Git não aparece quando tudo dá certo — aparece às 23h30 do dia da entrega, quando você apaga o arquivo errado. Este desafio é um treino de emergência: você vai quebrar o próprio projeto de quatro formas diferentes e recuperá-lo de quatro formas diferentes, documentando cada uma.

**Critérios de pronto**

- Cenário 1: você editou um arquivo e quer descartar a edição **antes** de preparar. Recupere e documente o comando.
- Cenário 2: você já rodou `git add` e quer tirar o arquivo da staging area sem perder a edição. Recupere e documente.
- Cenário 3: você commitou uma mudança ruim que já foi enviada com `push`. Desfaça criando um commit que reverte, sem reescrever o histórico público, e explique por que reescrever seria pior.
- Cenário 4: você apagou um arquivo há três commits e só percebeu agora. Encontre o commit em que ele existia e traga o arquivo de volta.
- Um documento `docs/git-socorro.md` no seu repositório, com os quatro cenários, o comando de cada um, a saída obtida e uma frase explicando o que o comando faz.
- Bônus: um quinto cenário com `git switch -c` — você começou a trabalhar em uma ideia arriscada e quer isolá-la em uma branch, sem sujar a `main`.

<details markdown="1">
<summary>Pistas</summary>

1. Comece por `git status`: em quase todos os cenários ele sugere o comando certo na própria saída.
2. Para o cenário 3, procure na documentação a diferença entre `git revert` e `git reset`. Só um dos dois é seguro para histórico já publicado.
3. Para o cenário 4, `git log --oneline -- caminho/do/arquivo` lista só os commits que tocaram naquele arquivo; `git checkout <hash> -- caminho/do/arquivo` traz uma versão antiga de volta para a working directory.
4. O livro *Pro Git* tem um capítulo inteiro chamado "Desfazendo Coisas", em português, gratuito em <https://git-scm.com/book/pt-br>.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `fatal: not a git repository (or any of the parent directories): .git` | O terminal está em uma pasta que não é repositório, ou você esqueceu o `git init` | Confirme a pasta com `pwd` (ou `cd`, no Windows) e rode `git init` na raiz do projeto |
| `Author identity unknown` seguido de `Please tell me who you are.` | `user.name` e `user.email` não foram configurados nesta máquina | Rode os dois `git config --global` da §8.3 e refaça o commit |
| `error: src refspec main does not match any` | Você tentou dar `push` sem ter nenhum commit, ou a branch tem outro nome | Faça o primeiro commit; confirme o nome com `git branch` e ajuste com `git branch -M main` |
| `Updates were rejected because the remote contains work that you do not have locally` | O repositório foi criado no GitHub já com README/licença, gerando commits que você não tem | `git pull --rebase origin main` e depois `git push`; ou recrie o repositório vazio |
| `remote: Invalid username or password.` / `fatal: Authentication failed` | O GitHub não aceita mais a senha da conta na linha de comando | Use um Personal Access Token no lugar da senha, ou configure chave SSH |
| O GitHub Pages responde `404 File not found` | Não há `index.html` na raiz da branch publicada, ou o nome do arquivo tem maiúscula (`Index.html`) | Coloque `index.html` minúsculo na raiz, faça push e espere a republicação |
| O site publicado não reflete a última alteração | O `commit` foi feito mas o `push` não; ou o Pages ainda está republicando | `git status` e `git log --oneline origin/main..main` para ver o que falta enviar; aguarde 1–3 min |
| Acentos aparecem como `Ã§`, `Ã£`, `Ã©` | Falta `<meta charset="UTF-8">` ou o arquivo foi salvo em outra codificação | Inclua a meta no `<head>`; confira "UTF-8" na barra inferior do VS Code |
| `node: command not found` (ou `'node' não é reconhecido…`) | O Node.js não está no `PATH`, ou o terminal foi aberto antes da instalação | Feche e reabra o terminal; se persistir, reinstale marcando a opção de adicionar ao `PATH` |
| Live Server abre uma lista de pastas ou `Cannot GET /` | O VS Code foi aberto em um arquivo solto ou em uma pasta sem `index.html` | *File → Open Folder* na raiz do projeto e clique em *Go Live* de novo |

## 🏠 Para praticar depois da aula (1 h)

**Parte 1 — Ambiente (20 min).** Instale, na sua máquina pessoal, VS Code, Node.js 22 LTS e Git. Rode os quatro comandos de verificação da §7.2 e tire **uma captura de tela** do terminal com as quatro saídas visíveis.

**Parte 2 — Projeto autoral (30 min).** Crie o repositório público do seu projeto autoral no GitHub, seguindo os passos 1 a 7 do Mão na massa com o **seu** tema:

1. `index.html` com a estrutura mínima, `<title>`, `<h1>` e dois parágrafos apresentando o tema.
2. `README.md` no formato do exercício **B5**.
3. `.gitignore`.
4. Pelo menos dois commits com mensagens no imperativo.
5. GitHub Pages ligado e o site abrindo.

**Parte 3 — Leitura dirigida (10 min).** Na Biblioteca Virtual da UNEMAT: QUEIRÓS & PORTELA, capítulo introdutório sobre a evolução e a arquitetura da Web; PUREWAL, capítulo 1, sobre o fluxo de trabalho do desenvolvedor (editor, terminal e Git). Anote duas ideias de cada texto que não apareceram nesta aula — elas voltam na discussão da próxima.

**Critério de pronto:** os dois links abrem (repositório público e site no ar); o `git log` mostra pelo menos dois commits com mensagens descritivas; a captura de tela mostra Node, npm, Git e VS Code respondendo com suas versões.

**Guarde no seu repositório:** o **link do repositório** do projeto autoral, o **link do site publicado** e a captura de tela do terminal. Sem `.zip`.

## ✅ Checkpoint do projeto

Ao fim desta aula você deve ter:

- [ ] VS Code, navegador, Node.js 22 LTS e Git instalados e **verificados** pelo terminal.
- [ ] Extensões Live Server e Prettier instaladas, com *format on save* ativado.
- [ ] `git config --global user.name` e `user.email` configurados com o e-mail da sua conta do GitHub.
- [ ] Pasta `cafe-cerrado/` com `index.html`, `README.md` e `.gitignore`.
- [ ] Repositório `cafe-cerrado` público no GitHub, com pelo menos dois commits de mensagens legíveis.
- [ ] GitHub Pages ligado e `https://SEU-USUARIO.github.io/cafe-cerrado/` abrindo no computador e no celular.
- [ ] Repositório do **projeto autoral** criado, publicado e com `README.md` explicando o tema.
- [ ] Tema do projeto autoral definido, com a "lista de coisas" identificada (§1.5).
- [ ] DevTools explorado: você já viu um `200` na aba Network e leu os cabeçalhos de uma resposta.

## 📚 Para aprofundar

- MDN — Visão geral do HTTP: <https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Overview> — leia a parte de requisições e respostas; é a §3 desta aula com mais detalhe.
- MDN — Métodos de requisição HTTP: <https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Methods> — foque em `GET`, `POST`, `PUT` e `DELETE`.
- MDN — Códigos de status HTTP: <https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Status> — referência para consultar, não para decorar.
- MDN — O que é uma URL: <https://developer.mozilla.org/pt-BR/docs/Learn_web_development/Howto/Web_mechanics/What_is_a_URL> — complementa a §3.4.
- MDN — Como a Web funciona: <https://developer.mozilla.org/pt-BR/docs/Learn_web_development/Getting_started/Web_standards/How_the_web_works> — a versão ilustrada da §2.2.
- CHACON, S.; STRAUB, B. *Pro Git*, 2ª ed., gratuito em português: <https://git-scm.com/book/pt-br> — capítulos 1 e 2 cobrem tudo da §8; o capítulo "Desfazendo Coisas" salva entregas.
- GitHub Docs — GitHub Pages: <https://docs.github.com/pt/pages> — configuração, domínio próprio e limites do plano gratuito.
- Node.js — Downloads e releases: <https://nodejs.org/pt-br/download> — confira o que significa a marca LTS.
- QUEIRÓS, Ricardo; PORTELA, Filipe. *Introdução ao Desenvolvimento Moderno para a Web: do front-end ao back-end, uma visão global*. FCA, 2018 — capítulo introdutório: evolução e arquitetura da Web.
- ALVES, William P. *Projetos de Sistemas Web*. Érica, 2015 — conceitos de cliente-servidor e planejamento de projetos web.
- PUREWAL, Semmy. *Aprendendo a Desenvolver Aplicações Web*. Novatec, 2014 — capítulo 1: o fluxo de trabalho do desenvolvedor.
- LOUDON, Kyle. *Desenvolvimento de Grandes Aplicações Web*. Novatec, 2019 — leitura de fôlego para quem quer ver onde a arquitetura desta aula escala.

Na próxima aula você entra no lado do cliente: o que o navegador faz com o código depois que a resposta HTTP chega, quem define os padrões da Web, como um site é servido de verdade e como organizar as pastas de um projeto. O `index.html` mínimo de hoje vira uma página com cabeçalho, navegação, conteúdo principal e rodapé, com uma folha de estilo própria — e cada `git push` continua publicando tudo sozinho.
