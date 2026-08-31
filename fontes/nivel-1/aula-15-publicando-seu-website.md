# Aula 15 — Publicando seu website na internet

> **Nível 1 — Introdução ao Desenvolvimento Web** · Unidade 3: JavaScript e interatividade
> WebLab · UNEMAT — Campus Sinop
> **Tempo estimado:** 3 blocos de 50 min + 1 h de prática

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Explicar o que são hospedagem, domínio e certificado HTTPS, e como os três se combinam para que um endereço digitado por um estranho chegue ao seu `index.html`.
- Identificar as diferenças entre o ambiente local e um servidor real — sensibilidade a maiúsculas, caminhos e subdiretório na URL — e corrigir o projeto antes de publicar.
- Preparar um projeto front-end para produção: limpeza de código, otimização de imagens, metadados de SEO e Open Graph, favicon e página 404.
- Versionar o projeto com os comandos essenciais do Git e publicá-lo em um repositório público no GitHub, com `.gitignore` e `README.md` adequados.
- Publicar o site no **GitHub Pages** e reconhecer quando a Netlify ou a Vercel são alternativas melhores.
- Auditar o site publicado com o **validador do W3C** e o **Lighthouse**, interpretar as quatro pontuações e aplicar as correções de maior impacto.
- Fechar o Marco 3 com o projeto autoral no ar, acessível por uma URL pública que qualquer pessoa consegue abrir.

## 📋 Pré-requisitos

- [ ] O site do evento acadêmico completo: cinco páginas responsivas, animações, menu hambúrguer acessível, listagens renderizadas por JavaScript, formulário validado e programação com busca, filtro e ordenação (Aulas 01 a 14).
- [ ] Console limpo nas cinco páginas, conforme o Checkpoint da Aula 14.
- [ ] Git instalado e configurado com o seu nome e e-mail (`git --version` responde no terminal). Se ainda não estiver, o [Capítulo 01 — Caixa de ferramentas do dev web](../deploy/cap-01.html) tem o passo a passo por sistema operacional.
- [ ] Uma conta gratuita no GitHub, com o e-mail confirmado.
- [ ] Navegador Chrome ou Edge atualizado (a aba **Lighthouse** do DevTools existe neles; no Firefox, use o PageSpeed Insights).
- [ ] Uma pasta de projeto chamada `site-evento/`, com `index.html` na raiz.

> Na aula passada você fechou o ciclo do JavaScript no navegador: o formulário de inscrição ganhou validação campo a campo com mensagens acessíveis, e a programação ganhou busca, filtro e ordenação em tempo real. O site está pronto — e existe para exatamente uma pessoa, porque só roda no `http://127.0.0.1:5500` da sua máquina. Hoje ele sai daí: você vai prepará-lo para produção, versioná-lo com Git, publicá-lo no GitHub Pages, auditar o resultado com o Lighthouse e terminar a aula com um endereço que qualquer pessoa do mundo consegue abrir.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Hospedagem, domínio e HTTPS; o que muda entre "funciona aqui" e "está no ar"; preparação para produção |
| 2 | 50 min | Git essencial, repositório no GitHub, GitHub Pages passo a passo e alternativas |
| 3 | 50 min | Auditoria com validador do W3C e Lighthouse, correções, README e Marco 3 do projeto |

## 1. O caminho de um site até o navegador de outra pessoa

Na Aula 01 você viu o ciclo requisição–resposta: o navegador pede, o servidor responde, o navegador desenha. Naquele momento o servidor era o Live Server, rodando na sua própria máquina. Publicar um site significa trocar esse servidor doméstico por um que fica ligado o tempo todo, com um endereço que existe para o mundo inteiro.

Três peças fazem isso acontecer. Elas são independentes — dá para ter uma sem a outra — e é justamente por isso que confundi-las causa tanta dor de cabeça.

### 1.1 Hospedagem: onde os arquivos ficam

**Hospedagem** é o computador (ou o conjunto de computadores) que guarda os seus arquivos e os entrega quando alguém pede. Para um site estático como o seu — só HTML, CSS, JavaScript e imagens, sem banco de dados nem código rodando no servidor —, hospedar é barato ao ponto de ser gratuito: o servidor não precisa *pensar*, só devolver arquivos.

Existem três modelos que você vai encontrar por aí:

| Modelo | Como funciona | Quando usar |
|---|---|---|
| Hospedagem de sites estáticos | Você envia os arquivos; a plataforma serve e distribui | Sites como o seu, portfólios, documentação |
| Hospedagem compartilhada | Um servidor com PHP e banco, dividido entre muitos clientes | Sites em WordPress e similares |
| Servidor próprio (VPS) | Você aluga uma máquina Linux e configura tudo | Aplicações com back-end e requisitos próprios |

O primeiro modelo é o desta aula, e o serviço que você vai usar — o GitHub Pages — pertence a ele. O terceiro é assunto do [Capítulo 06 — Servidor próprio (VPS) com nginx](../deploy/cap-06.html) da trilha Deploy, e vale a leitura quando você quiser entender o que as plataformas escondem de você.

> **🧠 Você sabia?**
> Sites estáticos praticamente não custam nada para servir porque a resposta é sempre a mesma para todo mundo — o arquivo pode ser copiado para servidores espalhados pelo planeta (uma **CDN**) e entregue a partir do mais próximo de quem pediu. É por isso que o GitHub Pages, a Netlify e a Vercel oferecem o serviço de graça: o custo marginal de mais um site pequeno é ínfimo. Um site que gera cada página na hora, consultando um banco, custa ordens de grandeza mais — e essa diferença é o principal motivo do renascimento dos sites estáticos na última década.

### 1.2 Domínio: o nome que as pessoas digitam

Servidores são encontrados por **endereço IP** (`185.199.108.153`, por exemplo). Ninguém decora isso. O **domínio** é um apelido legível — `unemat.br`, `github.io`, `weblab.ivanpires.dev` — e o **DNS** é a agenda telefônica mundial que traduz o apelido no número.

Quando alguém digita o endereço do seu site, acontece o seguinte, nesta ordem:

1. O navegador pergunta ao DNS qual é o IP daquele domínio.
2. O DNS responde (ou diz que não conhece, e você vê `DNS_PROBE_FINISHED_NXDOMAIN`).
3. O navegador abre uma conexão com aquele IP e pede o caminho da URL.
4. O servidor responde com o arquivo — ou com um status de erro, como o `404` que você já viu na aba Network.

Registrar um domínio `.com.br` custa por volta de quarenta reais por ano no [Registro.br](https://registro.br). Para esta disciplina **você não precisa comprar nada**: o GitHub oferece um subdomínio gratuito no formato `https://<seu-usuario>.github.io/<nome-do-repositorio>/`, e ele é um endereço público de verdade — funciona no celular do seu colega, na casa da sua avó e em qualquer lugar com internet.

Se, depois da disciplina, você quiser um domínio seu, o [Capítulo 04 — Domínios, DNS e HTTPS](../deploy/cap-04.html) da trilha Deploy cobre registro, registros `A` e `CNAME`, propagação e a configuração no lado da plataforma.

### 1.3 HTTPS: o cadeado

O `s` de HTTPS significa que a conversa entre o navegador e o servidor é **cifrada**. Sem ele, qualquer pessoa no mesmo Wi-Fi consegue ler — e alterar — o que trafega. Com ele, o conteúdo é embaralhado por chaves negociadas no início da conexão, e um **certificado** emitido por uma autoridade confiável garante que o servidor do outro lado é mesmo quem diz ser.

Três consequências práticas para você hoje:

- **O HTTPS é gratuito.** A autoridade certificadora Let's Encrypt emite certificados sem custo, e as plataformas de hospedagem cuidam da emissão e da renovação sozinhas. No GitHub Pages, basta marcar uma caixa.
- **Recursos misturados não carregam.** Uma página servida por HTTPS que tenta buscar uma imagem por `http://` recebe do navegador um bloqueio de *conteúdo misto*, com a mensagem `Mixed Content: The page at 'https://…' was loaded over HTTPS, but requested an insecure element`. Solução: nunca escreva `http://` nas URLs do seu site.
- **Algumas APIs só existem em HTTPS.** Geolocalização, câmera, microfone e notificações são bloqueadas em conexões inseguras. Isso não afeta o site do evento, mas afeta o seu próximo projeto.

> **⚠️ Atenção**
> `localhost` é tratado pelo navegador como origem segura mesmo em `http://`. Ou seja: coisas que funcionam na sua máquina podem falhar assim que o site vai ao ar em outro domínio. Depois de publicar, **refaça o teste no endereço público**, não no Live Server.

### 1.4 Onde a trilha Deploy aprofunda

Esta aula é uma travessia rápida e completa: no fim dela o seu site está no ar. Ela não é, porém, o assunto inteiro. O WebLab tem uma trilha transversal só para isso, e dois capítulos dela conversam diretamente com o que você vai fazer hoje:

- [Capítulo 02 — Git e GitHub do zero ao pull request](../deploy/cap-02.html): branches, merge, resolução de conflitos, `git stash`, tags, revisão de código em pull request e o `gh` (o GitHub pela linha de comando). Hoje você usa seis comandos; lá estão os outros trinta.
- [Capítulo 03 — Publicando sites estáticos](../deploy/cap-03.html): GitHub Pages, Netlify e Vercel em profundidade, domínio próprio, cabeçalhos de cache, redirecionamentos, prévia por branch e publicação automática.

Leia os dois quando quiser ir além do "está no ar" e chegar ao "está no ar com processo".

## 2. O que muda entre "funciona aqui" e "está no ar"

Um site que funciona perfeitamente no Live Server pode chegar ao servidor completamente quebrado — sem estilo, sem imagens, com o JavaScript morto. Não é azar: são três diferenças concretas de ambiente.

| Diferença | Consequência no ar |
|---|---|
| O servidor distingue maiúsculas de minúsculas | `Estilo.css` ≠ `estilo.css`: a página aparece "crua", sem CSS |
| Caminhos absolutos da sua máquina | `C:/Users/ana/site/img/logo.png` não existe em servidor nenhum |
| O site fica em um subdiretório da URL | Em `usuario.github.io/site-evento/`, o caminho `/img/logo.png` aponta para a raiz errada |

A primeira diferença é a mais cruel. O Windows e o macOS, por padrão, tratam `Foto.JPG` e `foto.jpg` como o mesmo arquivo. O Linux — que roda em praticamente todo servidor do mundo — não. O seu site funciona na sua máquina e morre no servidor, com um `404` para cada arquivo cujo nome você escreveu com uma letra diferente da real.

**As três regras que evitam quase todos os problemas:**

1. **Tudo em minúsculas, sem espaços e sem acentos**, em arquivos e em pastas. `foto-do-palestrante.webp`, nunca `Foto do Palestrante.WEBP`.
2. **Sempre caminhos relativos**: `css/estilo.css`, `img/logo-sasi.svg`, `../index.html`. Nunca comece um caminho com `/` em um site que vai para subdiretório, e nunca use caminho de disco.
3. **O arquivo de entrada se chama `index.html` e fica na raiz** do repositório. É o nome que todo servidor procura quando a URL termina em `/`.

> **🔎 Por baixo do capô**
> Quando você pede `https://usuario.github.io/site-evento/`, o servidor recebe o caminho `/site-evento/` e precisa decidir o que devolver. A convenção, herdada dos primeiros servidores web dos anos 1990, é procurar um **arquivo de índice** dentro do diretório: `index.html`. Se não achar, ele responde `404` ou, em servidores configurados para isso, devolve a listagem do diretório — aquela página cinza feia com os nomes dos arquivos. Renomear `index.html` para `home.html` é o jeito mais rápido de ver essa tela.

> **🔬 Investigue**
> Abra o `index.html` do site do evento e troque a linha do CSS para `<link rel="stylesheet" href="CSS/Estilo.css">`. Salve e recarregue no Live Server: no Windows e no macOS, provavelmente nada muda — o site continua estilizado. Agora abra o DevTools na aba **Network**, marque a caixa **Disable cache** e recarregue: a linha do CSS aparece com status `200` mesmo com o nome errado. Esse é exatamente o cenário que quebra no servidor Linux, onde o mesmo pedido volta `404`. Desfaça a alteração e adote a regra: nomes de arquivo sempre em minúsculas, escritos uma vez e copiados, nunca redigitados.

## 3. Preparando o projeto para produção

"Produção" é o nome que se dá ao ambiente onde os usuários de verdade usam o sistema. Preparar para produção é fazer, de uma vez, o que você foi adiando durante o semestre.

### 3.1 A estrutura final de pastas

Antes de qualquer coisa, o projeto precisa ter uma estrutura que outra pessoa entenda em dez segundos:

```text
site-evento/
├── index.html
├── programacao.html
├── inscricao.html
├── palestrantes.html
├── contato.html
├── 404.html
├── css/
│   └── estilo.css
├── js/
│   ├── menu.js
│   ├── efeitos.js
│   ├── dados.js
│   ├── app.js
│   ├── relatorios.js
│   ├── palestrantes.js
│   ├── inscricao.js
│   └── programacao.js
├── img/
│   ├── favicon.svg
│   ├── logo-sasi.svg
│   ├── preview.jpg
│   ├── banner.jpg
│   └── palestrante-01.webp  (até palestrante-06.webp)
├── .gitignore
├── .nojekyll
└── README.md
```

Regras dessa estrutura:

- **HTML na raiz.** Colocar as páginas dentro de uma pasta `paginas/` quebra todos os caminhos relativos e não traz benefício algum em um site de cinco páginas.
- **Uma pasta por tipo de recurso**: `css/`, `js/`, `img/`. Se as imagens forem muitas, subpastas por seção (`img/palestrantes/`) — no site do evento elas são poucas e ficam direto em `img/`, com os nomes numerados que o `js/dados.js` referencia desde a Aula 12.
- **Nada de arquivos órfãos.** `teste.html`, `estilo-antigo.css`, `Nova pasta/`, `index - Cópia.html`: apague. Se der medo, é para isso que serve o Git — depois do primeiro commit, nada se perde de verdade.

### 3.2 A limpeza obrigatória

Percorra esta lista antes de publicar. Ela leva vinte minutos e evita metade dos problemas do Marco 3:

- **Remova os `console.log` de depuração.** Console limpo é critério de qualidade, e um console cheio de mensagens suas denuncia código não revisado. O truque profissional está na próxima subseção.
- **Remova blocos de código comentado.** Aquele CSS antigo que você "deixou comentado por via das dúvidas" não serve para nada: a versão anterior está no histórico do Git.
- **Remova arquivos não referenciados.** Se nenhum HTML aponta para ele, ele só está ocupando espaço e confundindo quem lê.
- **Confira todos os links.** Nenhum `href="#"` esquecido, nenhum link para uma página que você renomeou.
- **Confira todas as imagens.** Cada `<img>` tem `alt` adequado, e o arquivo existe com exatamente aquele nome.
- **Confira os textos.** Nada de texto de preenchimento sobrando: o conteúdo tem que ser real, ainda que curto.

### 3.3 Depuração que não suja o console

Apagar todos os `console.log` na véspera da entrega é péssimo: você perde as ferramentas justo quando mais precisa delas. A solução é uma chave única e uma função que a consulta.

Ela precisa ficar **no topo do `js/dados.js`**, não do `app.js`. Desde a Aula 12, `dados.js` é o primeiro script do projeto que declara coisas usadas pelos outros — e ele mesmo tem um `console.log` no fim, que você vai querer trocar por `depurar`. Se a função morasse no `app.js`, que é carregado **depois**, essa troca daria `Uncaught ReferenceError: depurar is not defined` na primeira linha do site.

**`site-evento/js/dados.js`** (acrescente no início do arquivo, antes dos arrays)

```js
// ---------- DEPURAÇÃO ----------
// Chave de depuração: deixe true enquanto desenvolve, false antes de publicar.
const DEPURAR = false;

/**
 * Escreve no console apenas quando a depuração está ligada.
 * Use no lugar de console.log em qualquer mensagem de desenvolvimento.
 * @param {...*} mensagens - o que você quer inspecionar
 */
function depurar(...mensagens) {
  if (DEPURAR) {
    console.log("[site-evento]", ...mensagens);
  }
}
```

A partir daí, troque todo `console.log` de desenvolvimento por `depurar` — a começar pela última linha do próprio `dados.js`, que passa a ser `depurar(\`dados.js carregado: ${palestras.length} atividades, ${palestrantes.length} palestrantes.\`)`. Ligar e desligar a depuração inteira vira uma edição de uma linha.

Duas ressalvas importantes:

- `console.error` **fica**. Erros de verdade — uma imagem que não carregou, um dado inválido — devem aparecer sempre, inclusive em produção.
- `depurar` precisa estar declarado antes de ser usado pelos outros scripts. Com ele no topo do `js/dados.js`, isso vale para `app.js`, `relatorios.js`, `palestrantes.js`, `inscricao.js` e `programacao.js` — todos carregados depois, e `defer` garante a ordem das tags. O único que vem antes é o `js/menu.js`, que não escreve nada no console; se um dia precisar, mova a função para um `js/util.js` carregado em primeiro lugar.

### 3.4 Imagens: o maior peso do seu site

Em quase todo projeto de estudante, as imagens respondem por 80% dos bytes da página. Uma foto de celular tem cerca de 4000 pixels de largura e pesa 4 MB; exibida em um cartão de 400 pixels, ela entrega cem vezes mais dados do que o necessário — e quem paga a conta é quem abre o seu site em dados móveis.

| Ação | Ganho típico |
|---|---|
| Redimensionar para o tamanho real de exibição | 50% a 90% |
| Converter de JPEG para WebP | 25% a 35% a mais |
| Usar SVG para logos e ícones | Enorme, e escala sem perder qualidade |
| `loading="lazy"` no que está abaixo da dobra | Carregamento inicial mais rápido |
| Declarar `width` e `height` | Elimina o "pulo" do layout ao carregar |

O caminho prático, sem instalar nada: abra [squoosh.app](https://squoosh.app), arraste a imagem, escolha **WebP** com qualidade em torno de 75, ajuste a largura para o dobro do tamanho de exibição (para telas de alta densidade) e baixe. Uma foto de 4 MB costuma sair com 80 KB e nenhuma diferença visível.

A marcação final de uma imagem otimizada:

```html
<img
  src="img/palestrante-03.webp"
  alt="Carla Mendes, palestrante da área de segurança, sorrindo em frente a um quadro branco"
  width="400"
  height="400"
  loading="lazy"
>
```

Os atributos `width` e `height` não fixam o tamanho na tela — o CSS continua mandando. Eles informam ao navegador a **proporção** da imagem, para que ele reserve o espaço correto antes do arquivo chegar. Sem eles, o texto abaixo da imagem "pula" quando ela carrega, e o Lighthouse penaliza isso na métrica de estabilidade visual.

> **⚠️ Atenção**
> Não coloque `loading="lazy"` na imagem principal do topo da página (o herói, o logo do cabeçalho). Ela é justamente a que precisa aparecer primeiro; adiar o seu carregamento piora a experiência e a pontuação. `lazy` é para o que está **abaixo da dobra** — fora da primeira tela.

### 3.5 Metadados: o que o Google e o WhatsApp leem

O `<head>` de cada página carrega informações que não aparecem na tela, mas definem como o seu site é visto pelo mundo: o título na aba, o resumo no resultado de busca, o cartão que aparece quando alguém cola o link em um grupo de WhatsApp.

**`site-evento/index.html`** (o `<head>` completo)

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>Semana Acadêmica de Sistemas de Informação — UNEMAT Sinop</title>
  <meta name="description" content="Três dias de palestras, minicursos e maratona de programação no campus de Sinop. Programação completa, inscrição gratuita e certificado.">
  <meta name="author" content="Semana Acadêmica de Sistemas de Informação">
  <meta name="theme-color" content="#0b3d5c">

  <link rel="icon" href="img/favicon.svg" type="image/svg+xml">
  <link rel="canonical" href="https://usuario.github.io/site-evento/">

  <meta property="og:type" content="website">
  <meta property="og:title" content="Semana Acadêmica de Sistemas de Informação">
  <meta property="og:description" content="Palestras, minicursos e maratona de programação. Inscrição gratuita.">
  <meta property="og:image" content="https://usuario.github.io/site-evento/img/preview.jpg">
  <meta property="og:url" content="https://usuario.github.io/site-evento/">
  <meta property="og:locale" content="pt_BR">

  <link rel="stylesheet" href="css/estilo.css">
  <script src="js/menu.js" defer></script>
  <script src="js/dados.js" defer></script>
  <script src="js/app.js" defer></script>
  <script src="js/efeitos.js" defer></script>
</head>
```

A ordem dos `<script>` é a mesma fixada nas Aulas 13 e 14 — `menu.js`, `dados.js`, `app.js` e, por último, o script específico da página (aqui o `efeitos.js` da Aula 09; em `programacao.html` seriam `relatorios.js` e `programacao.js`, e em `inscricao.html` o `inscricao.js`). É por isso que o `depurar()` da seção 3.3 mora no topo do `dados.js`: assim ele já existe quando o `app.js` e os scripts de página rodam.

O que cada bloco faz:

- **`<title>`** — o texto da aba e o link azul do resultado de busca. Escreva no padrão `Assunto da página — Nome do site`, com no máximo 60 caracteres. Cada página tem o seu, diferente das outras.
- **`<meta name="description">`** — o parágrafo cinza abaixo do link no Google. Até 160 caracteres, escritos para uma pessoa, não para um robô. Cada página tem a sua.
- **`theme-color`** — colore a barra do navegador no Android. Detalhe pequeno, efeito grande.
- **`<link rel="icon">`** — o favicon, o ícone da aba. Um SVG resolve todos os tamanhos.
- **`canonical`** — declara qual é o endereço oficial da página, evitando que ela seja tratada como conteúdo duplicado quando acessível por mais de uma URL.
- **`og:*`** — o protocolo **Open Graph**, criado pelo Facebook e adotado por praticamente todo mundo (WhatsApp, Telegram, LinkedIn, Discord, Slack). É o que gera o cartão com imagem, título e descrição quando alguém compartilha o link. A `og:image` precisa ser uma **URL absoluta** — endereço completo, com `https://` — porque quem lê essa marcação é um servidor de outra empresa, que não tem como resolver caminho relativo.

A imagem de prévia deve ter 1200 × 630 pixels. Menos que isso e as plataformas mostram um cartão pequeno, sem destaque.

> **🧠 Você sabia?**
> Quando você cola um link no WhatsApp, não é o seu celular que gera a prévia: um servidor da plataforma abre a sua página, lê apenas o `<head>` e monta o cartão. Isso tem duas consequências curiosas. A primeira: se o seu site estiver fora do ar naquele instante, a prévia nunca mais é gerada para aquele link, porque o resultado fica em cache por muito tempo. A segunda: conteúdo inserido por JavaScript **não** entra na prévia — esses leitores não executam scripts. É por isso que as metatags precisam estar escritas no HTML, e não geradas pelo seu `app.js`.

### 3.6 A página 404

Cedo ou tarde alguém vai digitar errado o endereço de uma das suas páginas, ou clicar num link antigo. A resposta padrão do GitHub Pages é uma página em inglês, com o mascote do GitHub — nada a ver com o seu site.

Uma página `404.html` na raiz do repositório resolve: o Pages a serve automaticamente sempre que um caminho não existir.

**`site-evento/404.html`**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Página não encontrada — Semana Acadêmica de SI</title>
  <meta name="description" content="A página que você procurou não existe neste site.">
  <meta name="robots" content="noindex">
  <link rel="icon" href="/site-evento/img/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/site-evento/css/estilo.css">
</head>
<body>
  <a class="pular-para-conteudo" href="#conteudo">Pular para o conteúdo</a>

  <main id="conteudo" class="erro-404">
    <p class="erro-404__codigo">404</p>
    <h1>Esta página não existe</h1>
    <p>
      O endereço que você abriu não corresponde a nenhuma página do site da
      Semana Acadêmica. Pode ser um link antigo, um erro de digitação — ou uma
      página que ainda vamos criar.
    </p>
    <p>Talvez você esteja procurando por:</p>
    <ul class="erro-404__links">
      <li><a href="/site-evento/">Página inicial</a></li>
      <li><a href="/site-evento/programacao.html">Programação completa</a></li>
      <li><a href="/site-evento/inscricao.html">Inscrição</a></li>
      <li><a href="/site-evento/palestrantes.html">Palestrantes</a></li>
      <li><a href="/site-evento/contato.html">Contato</a></li>
    </ul>
  </main>
</body>
</html>
```

Repare que esta é a **única** página do projeto com caminhos começando por `/site-evento/`. O motivo: a `404.html` é servida em resposta a qualquer caminho inexistente, inclusive `/site-evento/uma/pasta/funda/pagina.html`. Um caminho relativo seria resolvido a partir dessa pasta imaginária e apontaria para o nada. Como o prefixo é o nome do repositório, você o ajusta se um dia renomeá-lo.

O CSS correspondente, no fim de `css/estilo.css`:

**`site-evento/css/estilo.css`**

```css
/* ---------- Página 404 ---------- */
.erro-404 {
  max-width: 60ch;
  margin-inline: auto;
  padding: var(--espaco-xl) var(--espaco-md);
  text-align: center;
}

.erro-404__codigo {
  font-size: clamp(4rem, 18vw, 9rem);
  font-weight: 800;
  line-height: 1;
  margin: 0;
  color: var(--cor-primaria);
  opacity: 0.25;
}

.erro-404__links {
  list-style: none;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  gap: var(--espaco-sm);
  justify-content: center;
}

.erro-404__links a {
  display: inline-block;
  padding: 0.5rem 1rem;
  border: 2px solid var(--cor-primaria);
  border-radius: var(--raio-md);
  text-decoration: none;
}

.erro-404__links a:hover,
.erro-404__links a:focus-visible {
  background-color: var(--cor-primaria);
  color: var(--cor-clara);
}
```

O `<meta name="robots" content="noindex">` pede aos buscadores que não indexem a página de erro — ela não deveria aparecer em resultado de busca nenhum.

## 4. Auditoria: provar que está bom

Publicar sem auditar é entregar prova sem reler. Três ferramentas dão, em minutos, um diagnóstico honesto do seu site.

### 4.1 O validador do W3C

O [validator.w3.org](https://validator.w3.org) lê o seu HTML e aponta tudo o que está fora da especificação: tag não fechada, atributo inventado, `id` repetido, hierarquia de títulos quebrada, texto solto onde só cabe elemento.

Três modos de uso, todos gratuitos:

| Modo | Quando usar |
|---|---|
| **Address** | O site já está publicado: cole a URL e valide a página no ar |
| **File Upload** | Ainda local: envie o arquivo `.html` |
| **Direct Input** | Um trecho suspeito: cole o HTML direto na caixa |

Valide **todas** as páginas, não só a inicial. A meta é zero erros. Avisos (*warnings*) merecem leitura, mas nem todos exigem ação — o aviso sobre `<section>` sem cabeçalho, por exemplo, costuma ser legítimo em alguns layouts.

> **📌 Vale gravar**
> Saiba dizer a diferença entre **erro** e **aviso** no validador, e por que HTML inválido pode funcionar no navegador mesmo assim: o algoritmo de análise do HTML é deliberadamente tolerante, e "conserta" a árvore do documento por conta própria. O problema é que cada navegador conserta de um jeito, e o resultado deixa de ser previsível — sem falar que leitores de tela e buscadores dependem da estrutura correta.

### 4.2 Links quebrados e o console

Duas conferências rápidas, feitas no próprio DevTools:

1. **Aba Console**, nas cinco páginas: zero mensagens em vermelho. Cada `Uncaught` é um recurso do seu site que não funciona.
2. **Aba Network**, com o filtro de status: qualquer linha `404` é um arquivo que o HTML pede e o servidor não tem. Nome errado, arquivo esquecido fora do commit ou caminho equivocado.

Para os links internos, o teste é manual e leva cinco minutos: clique em todos, em todas as páginas, incluindo os do rodapé e os do menu. Depois de publicado, um serviço como o [W3C Link Checker](https://validator.w3.org/checklink) faz a varredura sozinho.

### 4.3 Lighthouse: a nota do seu site

O **Lighthouse** vem embutido no Chrome e no Edge. Ele carrega a sua página simulando um celular modesto em rede 4G, mede dezenas de indicadores e devolve quatro notas de 0 a 100.

| Categoria | Meta na disciplina | O que costuma derrubar |
|---|---|---|
| Desempenho | ≥ 80 | Imagens grandes, fontes pesadas, layout instável |
| Acessibilidade | ≥ 90 | Contraste, `alt` ausente, `label` ausente, ordem de títulos |
| Práticas recomendadas | ≥ 90 | Erros no console, imagens sem proporção, recursos por HTTP |
| SEO | ≥ 90 | Sem `description`, sem `title`, link sem texto, sem `viewport` |

Como rodar, do jeito certo:

1. Abra o site **publicado** (não o `localhost`) em uma **janela anônima** — extensões do navegador poluem o resultado e derrubam a nota de práticas recomendadas.
2. `F12` → aba **Lighthouse**.
3. Modo **Navigation**, dispositivo **Mobile**, as quatro categorias marcadas.
4. **Analyze page load**. Aguarde de vinte segundos a um minuto.

Rode duas ou três vezes: a nota de desempenho oscila alguns pontos entre execuções, porque depende da rede e da carga da sua máquina naquele instante. Considere a mediana.

**As correções de maior impacto, em ordem de retorno pelo esforço:**

1. Comprimir e converter as imagens para WebP.
2. Declarar `width` e `height` em todas as imagens.
3. Aplicar `loading="lazy"` no que está abaixo da dobra.
4. Reduzir a dois os pesos de fonte importados (por exemplo, 400 e 700 apenas).
5. Corrigir os contrastes reprovados.
6. Zerar os erros do console.
7. Preencher `title` e `description` de cada página.

> **🔬 Investigue**
> Rode o Lighthouse no site do evento **antes** de otimizar as imagens e anote as quatro notas. Depois abra a aba **Network**, marque **Disable cache**, recarregue e leia a barra de status no rodapé: ela mostra o total transferido. Anote também esse número. Faça a otimização das imagens e repita as duas medições. Em turmas anteriores, o peso da página inicial costuma cair de 6 MB para menos de 500 KB, e o desempenho salta trinta pontos — com **uma tarde** de trabalho e nenhuma linha de código. É a melhor relação entre esforço e resultado de toda a disciplina.

### 4.4 O teste que nenhuma ferramenta faz

Automação não cobre tudo. Antes de considerar o site pronto:

- **Teclado apenas.** Percorra o site inteiro com <kbd>Tab</kbd>, <kbd>Shift</kbd>+<kbd>Tab</kbd>, <kbd>Enter</kbd> e <kbd>Esc</kbd>. Todo elemento focado precisa ser visível, e a ordem precisa fazer sentido.
- **Celular real, com dados móveis.** O emulador do DevTools mente sobre desempenho e sobre o tamanho do seu dedo.
- **Dois navegadores.** Chrome e Firefox, no mínimo.
- **Janela anônima.** Elimina cache, cookies e extensões — é o que um visitante novo vê.
- **Zoom em 200%.** Requisito de acessibilidade: o conteúdo tem que continuar utilizável, sem rolagem horizontal.

## 5. Git: o mínimo para publicar

O Git é um sistema de controle de versão: ele guarda fotografias sucessivas do seu projeto, permite voltar a qualquer uma delas e junta o trabalho de várias pessoas. Ele é também o mecanismo pelo qual o seu código chega ao GitHub e, de lá, ao ar.

Esta seção é o **suficiente para publicar**. A versão completa — branches, merges, conflitos, pull requests, `stash`, tags — está no [Capítulo 02 — Git e GitHub do zero ao pull request](../deploy/cap-02.html).

### 5.1 Configuração, uma vez na vida

```bash
git config --global user.name "Seu Nome Completo"
git config --global user.email "seu-email@exemplo.com"
git config --global init.defaultBranch main
```

O e-mail precisa ser **o mesmo cadastrado no GitHub**. É por ele que a plataforma associa cada commit à sua conta — e é assim que o professor confere quem escreveu o quê. Confira o que ficou gravado:

```bash
git config --global --list
```

### 5.2 Os seis comandos do dia a dia

```bash
git init                    # cria o repositório na pasta atual (uma vez por projeto)
git status                  # o que mudou desde o último commit
git add .                   # prepara todas as mudanças para o próximo commit
git commit -m "mensagem"    # grava a fotografia com uma descrição
git log --oneline           # o histórico, uma linha por commit
git push                    # envia os commits para o GitHub
```

O ciclo normal de trabalho tem três passos, repetidos indefinidamente: **editar → `git add .` → `git commit -m "…"`**. Ao fim da sessão, `git push`.

### 5.3 Mensagens de commit que servem para alguma coisa

Uma mensagem de commit é um bilhete para o seu eu de daqui a três meses. Escreva no imperativo, dizendo o que o commit **faz** ao projeto:

```bash
git commit -m "Adiciona validação de CPF no formulário de inscrição"
git commit -m "Corrige menu que não fechava com Esc no celular"
git commit -m "Otimiza imagens dos palestrantes para WebP"
```

O que não escrever: `alteracoes`, `att`, `final`, `final2`, `agora vai`, `.`. Um histórico assim é indistinguível de nenhum histórico.

Uma boa regra: **um commit por ideia**. Terminou o menu? Commit. Corrigiu o contraste dos botões? Outro commit. Commits pequenos e frequentes são fáceis de entender e de desfazer.

### 5.4 `.gitignore`: o que nunca entra no repositório

Alguns arquivos não pertencem ao repositório: lixo do sistema operacional, configuração pessoal do editor, dependências que qualquer um consegue reinstalar e — principalmente — segredos.

**`site-evento/.gitignore`**

```text
# Sistema operacional
.DS_Store
Thumbs.db
desktop.ini

# Editor
.vscode/
.idea/

# Dependências e logs
node_modules/
*.log

# Arquivos temporários e originais pesados
*.tmp
img-originais/
```

A pasta `img-originais/` é uma sugestão prática: guarde nela as fotos em tamanho original, fora do Git, e versione apenas as versões otimizadas que o site usa.

> **⚠️ Atenção**
> O `.gitignore` só funciona para arquivos que **ainda não** foram commitados. Se você já enviou um arquivo por engano, adicioná-lo ao `.gitignore` não o remove do repositório nem do histórico. E, uma vez publicado, considere que o conteúdo vazou: um repositório público é lido por robôs em minutos. Nunca coloque senhas, tokens ou chaves de API em um repositório — no seu site do evento não há nenhum, mas no Nível 2 haverá.

### 5.5 O `.nojekyll`

O GitHub Pages nasceu como uma plataforma para o gerador de sites Jekyll, e por herança ele ainda processa os arquivos antes de publicá-los. Um efeito colateral: **pastas e arquivos que começam com `_` são ignorados**. Se um dia você criar `_imagens/` ou `_parciais/`, elas simplesmente não vão ao ar.

A solução é um arquivo vazio na raiz, chamado `.nojekyll`:

```bash
touch .nojekyll
```

No Windows, sem o Git Bash, o mesmo efeito com o PowerShell:

```bash
New-Item -Path .nojekyll -ItemType File
```

## 6. GitHub Pages passo a passo

O GitHub Pages transforma um repositório em um site. A cada `git push`, ele pega os arquivos da branch escolhida e os serve em um endereço público, com HTTPS incluído. É gratuito para repositórios públicos e não exige cartão de crédito.

### 6.1 Criar o repositório no GitHub

1. Entre em [github.com](https://github.com) e clique no **+** no canto superior direito → **New repository**.
2. **Repository name:** `site-evento` (minúsculas, com hífen, sem acento e sem espaço — esse nome vai aparecer na URL).
3. **Description:** uma frase sobre o projeto.
4. **Public.** Obrigatório aqui: em repositório privado, o GitHub Pages só está disponível nos planos pagos.
5. **Não marque nada** em "Initialize this repository": nem README, nem `.gitignore`, nem licença. Você já tem esses arquivos localmente, e um repositório remoto com commits próprios complica o primeiro `push`.
6. **Create repository.**

A página seguinte mostra os comandos para conectar um repositório local existente. São estes:

```bash
git remote add origin https://github.com/usuario/site-evento.git
git branch -M main
git push -u origin main
```

Traduzindo:

- `git remote add origin <url>` — apelida a URL do repositório remoto como `origin`.
- `git branch -M main` — garante que a branch local se chama `main` (o nome que o GitHub espera).
- `git push -u origin main` — envia os commits e memoriza o destino; a partir daí, `git push` sozinho basta.

Na primeira vez, o Git pedirá autenticação. O navegador abre e você autoriza — é o fluxo padrão do Git Credential Manager. Se preferir chave SSH ou o GitHub CLI, o [Capítulo 02](../deploy/cap-02.html) cobre os dois.

### 6.2 Ativar o Pages

1. No repositório, abra **Settings** (a engrenagem, na barra superior do repositório — não a do seu perfil).
2. No menu lateral esquerdo, clique em **Pages**.
3. Em **Source**, escolha **Deploy from a branch**.
4. Em **Branch**, escolha `main` e a pasta `/ (root)`. Clique em **Save**.
5. Aguarde de um a três minutos. Recarregue a página: aparece uma faixa verde com **Your site is live at** e o endereço.

O endereço segue o padrão:

```text
https://<seu-usuario>.github.io/<nome-do-repositorio>/
```

Para o repositório `site-evento` da usuária `ana-souza`, por exemplo: `https://ana-souza.github.io/site-evento/`.

Existe um caso especial: se você nomear o repositório exatamente como `<seu-usuario>.github.io`, o site é publicado na **raiz** do subdomínio, sem subpasta. É a escolha certa para um portfólio pessoal — e cada conta só pode ter um.

> **🧠 Você sabia?**
> O `github.io` é um domínio separado do `github.com` por um motivo de segurança, não de estética. Se as páginas dos usuários fossem servidas em `github.com/paginas/…`, qualquer JavaScript publicado por qualquer pessoa rodaria na **mesma origem** do GitHub — e poderia, pela política de mesma origem, ler os cookies de sessão de quem estivesse logado. Isolando os sites em outro domínio, o navegador impede a leitura. A mesma preocupação explica por que o Google usa `googleusercontent.com` e a Microsoft usa `sharepointonline.com` para conteúdo enviado por usuários.

### 6.3 A armadilha do subdiretório

Este é o erro que mais aparece na primeira publicação. O site funciona no Live Server, sobe para o Pages e chega **sem estilo nenhum**.

A causa: caminhos que começam com barra.

```html
<!-- Funciona no Live Server, quebra no GitHub Pages -->
<link rel="stylesheet" href="/css/estilo.css">
```

No Live Server, a raiz é a pasta do projeto, e `/css/estilo.css` resolve certo. No Pages, a raiz é `https://usuario.github.io/`, e a barra manda o navegador buscar `https://usuario.github.io/css/estilo.css` — um lugar onde o seu CSS não está.

```html
<!-- Funciona nos dois -->
<link rel="stylesheet" href="css/estilo.css">
```

Regra prática para o seu site: **nenhum `href` ou `src` interno começa com `/`**, exceto os da `404.html`, pelo motivo já explicado na seção 3.6. Localize os culpados de uma vez com a busca do VS Code (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>F</kbd>) procurando por `href="/` e `src="/`.

### 6.4 Republicar e o cache

Publicar de novo é só isto:

```bash
git add .
git commit -m "Corrige caminhos das imagens para publicação"
git push
```

De trinta segundos a dois minutos depois, o site no ar reflete a mudança. A aba **Actions** do repositório mostra a publicação em andamento; um visto verde significa concluída.

Se a alteração não aparecer, o culpado quase sempre é o **cache do navegador**: recarregue com <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>R</kbd> (ou <kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>R</kbd> no macOS), ou abra em janela anônima. Antes de concluir que "o Pages está com problema", confirme no próprio GitHub que o commit chegou: se o arquivo mudou lá, o problema está do seu lado da conexão.

## 7. Netlify e Vercel: quando valem mais

O GitHub Pages resolve o caso desta disciplina. Duas alternativas gratuitas resolvem casos que ele não cobre.

**Netlify.** Em [netlify.com](https://www.netlify.com), há dois caminhos. O primeiro é literalmente arrastar a pasta do projeto para a área indicada no painel: em vinte segundos o site está no ar, sem Git nenhum. O segundo, recomendado, é **Import from Git** → autorizar o GitHub → escolher o repositório → deixar o *build command* vazio e o *publish directory* como `.` → **Deploy**. O endereço sai como `nome-aleatorio.netlify.app` e pode ser renomeado nas configurações do site.

**Vercel.** Em [vercel.com](https://vercel.com), o fluxo é praticamente idêntico ao da Netlify. Para um site estático, o resultado é o mesmo; a Vercel brilha quando há um framework moderno envolvido.

| Recurso | GitHub Pages | Netlify | Vercel |
|---|---|---|---|
| Custo e HTTPS automático | Gratuito, sim | Gratuito, sim | Gratuito, sim |
| Prévia automática por branch | Não | Sim | Sim |
| Formulários sem back-end | Não | Sim | Não |
| Redirecionamentos e cabeçalhos | Limitado | Sim | Sim |

A **prévia por branch** é o recurso mais transformador dos três da tabela: cada branch enviada ganha uma URL própria, o que permite mostrar uma versão em teste sem tocar no site oficial. Os **formulários** da Netlify recebem envios de um `<form>` HTML puro e mostram as respostas no painel — resolvendo, sem back-end, o formulário de contato que hoje só existe visualmente no seu site.

Para o Marco 3, qualquer uma das três serve. Publique em uma; se sobrar tempo, publique nas três e compare (é o exercício B4).

## 8. Domínio próprio, em quatro passos

Você não precisa de domínio próprio para o marco. Mas se quiser um — para o portfólio, por exemplo —, o caminho é curto:

1. **Registre.** No [Registro.br](https://registro.br) para `.com.br` (exige CPF e custa por volta de quarenta reais por ano); em registradores internacionais para `.com`, `.dev`, `.me`.
2. **Aponte o DNS.** No painel do registrador, crie os registros que a plataforma de hospedagem indicar: quatro registros `A` para o GitHub Pages (com os IPs listados na documentação oficial) ou um `CNAME` apontando para `<seu-usuario>.github.io`.
3. **Declare o domínio na plataforma.** No GitHub: **Settings → Pages → Custom domain**. Isso cria um arquivo `CNAME` na raiz do repositório — não o apague.
4. **Ative o HTTPS.** Marque **Enforce HTTPS**. O certificado é emitido automaticamente, em minutos ou algumas horas.

A propagação do DNS leva de minutos a algumas horas; enquanto isso, é normal ver o site ora pelo endereço antigo, ora pelo novo. O [Capítulo 04 — Domínios, DNS e HTTPS](../deploy/cap-04.html) explica cada tipo de registro, o TTL e como diagnosticar problemas com `dig` e `nslookup`.

## 9. O `README.md`: a capa do projeto

O `README.md` é a primeira coisa que o GitHub mostra ao abrir o repositório — e, muitas vezes, a única que um avaliador apressado lê. Ele é escrito em **Markdown**, a mesma linguagem desta apostila.

**`site-evento/README.md`**

```markdown
# Semana Acadêmica de Sistemas de Informação

Site do evento acadêmico do curso de Sistemas de Informação da UNEMAT — Campus
Sinop, desenvolvido na disciplina Introdução ao Desenvolvimento Web
(FACET-SNP-319).

**Site publicado:** https://usuario.github.io/site-evento/

## Sobre

Site de cinco páginas que divulga a programação do evento, apresenta os
palestrantes e recebe inscrições. O objetivo é concentrar em um só lugar as
informações que hoje se perdem em grupos de mensagens: o que acontece, quando,
onde e como participar.

O visitante encontra a programação completa com busca e filtro por trilha, a
lista de palestrantes e um formulário de inscrição validado no navegador.

## Funcionalidades

- Menu de navegação responsivo, acessível por teclado, com indicação da página atual
- Programação renderizada a partir de dados em JavaScript, com busca, filtro por
  trilha e ordenação
- Formulário de inscrição com validação campo a campo, incluindo CPF, telefone e
  e-mail, com mensagens acessíveis
- Rascunho da inscrição salvo no navegador com localStorage
- Layout responsivo em três larguras, com animações que respeitam
  prefers-reduced-motion

## Tecnologias

HTML5 semântico, CSS3 (variáveis, Flexbox, Grid, media queries) e JavaScript
(ES2015+), sem frameworks nem bibliotecas externas.

## Estrutura

- `index.html`, `programacao.html`, `inscricao.html`, `palestrantes.html`,
  `contato.html` — as cinco páginas
- `404.html` — página de erro
- `css/estilo.css` — folha de estilo única, organizada por seções comentadas
- `js/menu.js` — abre e fecha o menu hambúrguer (Aulas 08, 09 e 13)
- `js/efeitos.js` — revelação ao rolar com IntersectionObserver (Aula 09)
- `js/dados.js` — fonte única de dados: palestras, palestrantes e áreas
- `js/app.js` — comportamento comum a todas as páginas (contagem regressiva,
  `aria-current` e `debounce`)
- `js/relatorios.js` — relatórios do evento no console (Aula 12)
- `js/palestrantes.js` — lista de palestrantes com filtro por área (Aula 13)
- `js/inscricao.js` — vagas restantes e validação do formulário
- `js/programacao.js` — busca, filtro e ordenação da programação
- `img/` — imagens otimizadas em WebP e SVG

## Como executar localmente

1. Clone o repositório: `git clone https://github.com/usuario/site-evento.git`
2. Abra a pasta no VS Code
3. Clique com o botão direito em `index.html` e escolha "Open with Live Server"

## Auditoria

Lighthouse (mobile, janela anônima, no site publicado):
desempenho 92, acessibilidade 100, práticas recomendadas 100, SEO 100.
HTML validado sem erros no validator.w3.org em todas as páginas.

## Autoria

Desenvolvido por Nome Sobrenome, estudante de Sistemas de Informação da UNEMAT
Sinop.
```

Sete seções, nenhuma opcional na prática: o que é, onde está no ar, o que faz, com o que foi feito, como está organizado, como rodar e quem fez. Um README com o link do site no topo economiza o tempo de quem avalia — e isso conta.

> **💡 Dica**
> No Markdown do GitHub, três coisas melhoram muito o README com pouco esforço: uma **captura de tela** do site logo abaixo do título (`![Página inicial do site](img/captura-inicial.png)`), listas de tarefas com `- [x]` para mostrar o que já está pronto, e blocos de código com a linguagem declarada. Evite badges decorativos: eles enchem o topo e não dizem nada sobre um trabalho acadêmico.

## 💻 Mão na massa — O site do evento no ar

Ao fim deste roteiro, o site do evento acadêmico estará acessível em `https://<seu-usuario>.github.io/site-evento/`, auditado e documentado. Reserve os cinquenta minutos do segundo bloco e os primeiros vinte do terceiro.

### Passo 1 — Limpeza e conferência local

Com o projeto aberto no VS Code:

1. <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>F</kbd> e procure por `console.log`. Substitua cada ocorrência de depuração por `depurar(`, depois de acrescentar o bloco da seção 3.3 ao **topo** do `js/dados.js`. Mantenha os `console.error`.
2. Procure por `href="/` e por `src="/`. Cada resultado é um caminho absoluto que vai quebrar no Pages: remova a barra inicial.
3. Procure por `href="#"`. Todo link de menu ou de rodapé precisa apontar para uma página real.
4. Apague arquivos órfãos: testes, cópias, folhas antigas, pastas de rascunho.
5. Renomeie para minúsculas, sem espaço e sem acento, qualquer arquivo que ainda esteja fora do padrão — e corrija as referências no HTML e no CSS.
6. Abra as cinco páginas no Live Server e confirme: console limpo, nenhuma linha vermelha na aba Network.

### Passo 2 — O favicon

Crie um favicon vetorial simples com as iniciais do evento. Um SVG resolve todos os tamanhos e pesa menos de 1 KB.

**`site-evento/img/favicon.svg`**

```html
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="SASI">
  <rect width="64" height="64" rx="14" fill="#0b3d5c"></rect>
  <text x="32" y="42" text-anchor="middle"
        font-family="Segoe UI, Roboto, sans-serif"
        font-size="26" font-weight="700" fill="#ffffff">SA</text>
</svg>
```

Referencie-o no `<head>` de todas as páginas:

```html
<link rel="icon" href="img/favicon.svg" type="image/svg+xml">
```

### Passo 3 — Metadados nas cinco páginas

Cada página recebe `title` e `description` próprios. Copie o `<head>` completo da seção 3.5 para o `index.html` e ajuste as demais:

**`site-evento/programacao.html`**

```html
<title>Programação — Semana Acadêmica de Sistemas de Informação</title>
<meta name="description" content="Palestras, minicursos e mesas-redondas dos três dias do evento, com busca por título e filtro por trilha.">
```

**`site-evento/inscricao.html`**

```html
<title>Inscrição — Semana Acadêmica de Sistemas de Informação</title>
<meta name="description" content="Inscreva-se gratuitamente na Semana Acadêmica de Sistemas de Informação e garanta o seu certificado de participação.">
```

**`site-evento/palestrantes.html`**

```html
<title>Palestrantes — Semana Acadêmica de Sistemas de Informação</title>
<meta name="description" content="Conheça quem vai palestrar no evento: professores, profissionais do mercado e egressos do curso.">
```

**`site-evento/contato.html`**

```html
<title>Contato — Semana Acadêmica de Sistemas de Informação</title>
<meta name="description" content="Fale com a organização da Semana Acadêmica: e-mail, telefone e endereço do campus de Sinop.">
```

As metatags `og:` ficam iguais em todas as páginas, exceto `og:title` e `og:url`, que acompanham a página. Se ainda não tiver a imagem de prévia, gere uma de 1200 × 630 com o logo e o nome do evento e salve como `img/preview.jpg`.

### Passo 4 — A página 404

Crie `404.html` na raiz com o conteúdo da seção 3.6 e acrescente ao fim de `css/estilo.css` o bloco `.erro-404`. Teste depois de publicar: abrir `https://<seu-usuario>.github.io/site-evento/pagina-que-nao-existe` deve mostrar a **sua** página de erro.

### Passo 5 — Otimizar as imagens

1. Crie a pasta `img-originais/` e mova para lá as fotos em tamanho original.
2. Para cada imagem, abra o [squoosh.app](https://squoosh.app), arraste o arquivo, escolha **WebP** com qualidade 75 e ajuste a largura para o dobro da exibição (uma foto exibida em 400 px sai com 800 px de largura).
3. Salve o resultado em `img/`, com nome em minúsculas e hífens.
4. Atualize os `src` no HTML e acrescente `width`, `height` e `loading="lazy"` no que estiver abaixo da dobra:

As fotos dos palestrantes não estão mais no HTML desde a Aula 13 — quem as escreve é o `js/palestrantes.js`, a partir do campo `foto` do `js/dados.js`. Então o ajuste acontece **em um lugar só**: no array de dados, trocando a extensão dos seis caminhos de `.jpg` para `.webp`. Nada mais do arquivo muda — os nomes, as áreas, os `id` e os `palestranteId` são os mesmos desde a Aula 12, e o `relatorios.js` e o `programacao.js` continuam lendo os mesmos campos.

**`site-evento/js/dados.js`** (trecho: só o campo `foto` de cada pessoa)

```js
const palestrantes = [
  { id: 1, nome: "Ana Lúcia Ferreira", instituicao: "UNEMAT — Sinop", area: "ia",
    tema: "Redes neurais para prever a safra de soja",
    foto: "img/palestrante-01.webp" },
  { id: 2, nome: "Bruno Takahashi", instituicao: "Startup AgroData", area: "dados",
    tema: "Dashboards que os produtores realmente usam",
    foto: "img/palestrante-02.webp" },
  { id: 3, nome: "Carla Mendes", instituicao: "UFMT", area: "seguranca",
    tema: "O que um ataque de phishing ensina sobre UX",
    foto: "img/palestrante-03.webp" },
  { id: 4, nome: "Diego Nascimento", instituicao: "Prefeitura de Sinop", area: "web",
    tema: "Acessibilidade em portais públicos: erros que vimos",
    foto: "img/palestrante-04.webp" },
  { id: 5, nome: "Eduarda Ribeiro", instituicao: "UNEMAT — Sinop", area: "web",
    tema: "Do HTML ao deploy: o caminho do estudante",
    foto: "img/palestrante-05.webp" },
  { id: 6, nome: "Felipe Arruda", instituicao: "Cooperativa Coopercana", area: "ia",
    tema: "Visão computacional no controle de pragas",
    foto: "img/palestrante-06.webp" },
];
```

Recarregue `palestrantes.html`: os seis cartões continuam lá, agora com as fotos em WebP. Se algum ficar com o ícone de imagem quebrada, o nome do arquivo em `img/` não bate com o do array — o Linux do GitHub Pages diferencia maiúsculas de minúsculas, e o seu Windows não.

6. Compare o peso da página na aba **Network** antes e depois. Anote os dois números: eles entram na atividade assíncrona.

### Passo 6 — `.gitignore`, `.nojekyll` e `README.md`

Crie os três arquivos na raiz do projeto: o `.gitignore` da seção 5.4, o `.nojekyll` vazio e o `README.md` da seção 9, com os seus dados. Deixe o campo do Lighthouse em branco por enquanto — você o preenche no Passo 10.

### Passo 7 — O repositório local

No terminal integrado do VS Code (<kbd>Ctrl</kbd>+<kbd>'</kbd>), dentro da pasta `site-evento/`:

```bash
git init
git status
```

O `git status` lista todos os arquivos como não rastreados. Confirme que **`img-originais/` não aparece** — se aparecer, o `.gitignore` está com o nome errado ou fora da raiz.

Agora o primeiro commit:

```bash
git add .
git commit -m "Site do evento academico completo, pronto para publicacao"
```

E confira:

```bash
git log --oneline
```

Uma linha com um código de sete caracteres e a sua mensagem. Esse código é o identificador do commit.

### Passo 8 — O repositório no GitHub

1. Crie no GitHub o repositório público `site-evento`, sem inicializar com nenhum arquivo (seção 6.1).
2. Conecte e envie:

```bash
git remote add origin https://github.com/SEU-USUARIO/site-evento.git
git branch -M main
git push -u origin main
```

Troque `SEU-USUARIO` pelo seu nome de usuário do GitHub. Autentique no navegador quando pedido.

3. Recarregue a página do repositório: os arquivos estão lá, e o `README.md` aparece renderizado abaixo da lista.

### Passo 9 — Ativar o GitHub Pages

1. **Settings → Pages**.
2. **Source:** Deploy from a branch. **Branch:** `main`, pasta `/ (root)`. **Save.**
3. Espere de um a três minutos e recarregue. Copie o endereço da faixa verde.
4. Abra o endereço em uma **janela anônima**.

### Passo 10 — Corrigir o que quebrou e auditar

É normal que algo quebre agora. Com o site aberto no endereço público:

1. `F12` → **Console**: nenhum erro. Se houver `Failed to load resource`, veja qual arquivo faltou.
2. `F12` → **Network**, com **Disable cache** marcado: nenhuma linha com status `404`. Cada `404` é caminho errado ou arquivo que ficou de fora do commit.
3. Clique em todos os links, nas cinco páginas.
4. Abra `https://<seu-usuario>.github.io/site-evento/pagina-que-nao-existe` e confirme que a sua `404.html` aparece.
5. Valide as cinco páginas em [validator.w3.org](https://validator.w3.org), no modo **Address**, colando a URL de cada uma. Corrija os erros.
6. Rode o **Lighthouse** (Mobile, janela anônima) na página inicial e anote as quatro notas.
7. Aplique as correções da lista da seção 4.3, da primeira para a última, até bater as metas.
8. Preencha a seção **Auditoria** do `README.md` com as notas finais.

A cada rodada de correções, republique:

```bash
git add .
git commit -m "Corrige caminhos e otimiza imagens apontadas pelo Lighthouse"
git push
```

### Passo 11 — A prova dos nove

Pegue o celular, **desligue o Wi-Fi** e abra o endereço público usando dados móveis. Navegue pelas cinco páginas, abra o menu, use a busca da programação e preencha o formulário de inscrição.

Se tudo funcionar aí, o seu site está no ar de verdade. Mande o link para alguém que não é da turma e peça para abrir.

### Como testar

1. O endereço `https://<seu-usuario>.github.io/site-evento/` abre a página inicial em janela anônima, com todo o estilo aplicado.
2. As cinco páginas carregam, com CSS e JavaScript, e o menu funciona em todas.
3. A aba da página mostra o seu favicon.
4. O console está limpo e a aba Network não tem nenhum `404` nas cinco páginas.
5. `https://<seu-usuario>.github.io/site-evento/qualquer-coisa` mostra a sua página 404 personalizada, com os links funcionando.
6. Colar o link em uma conversa de WhatsApp gera um cartão com título, descrição e imagem.
7. O validador do W3C não aponta erros em nenhuma das cinco páginas.
8. O Lighthouse (Mobile, anônima) devolve desempenho ≥ 80 e acessibilidade, práticas recomendadas e SEO ≥ 90.
9. `git log --oneline` mostra ao menos cinco commits com mensagens descritivas.
10. O `README.md` aparece renderizado no GitHub, com o link do site publicado logo no início.
11. O site funciona no celular, com dados móveis, sem depender do Wi-Fi do campus.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Cite as três diferenças entre o ambiente local e o servidor que mais quebram sites recém-publicados, e a regra que evita cada uma.

**A2.** Por que o arquivo de entrada precisa se chamar `index.html` e ficar na raiz do repositório? O que o servidor faz quando não encontra esse arquivo?

**A3.** Explique, para um colega que faltou, a diferença entre hospedagem, domínio e certificado HTTPS. Dê um exemplo de cada um no endereço `https://ana.github.io/site-evento/`.

**A4.** Qual a diferença entre `href="/css/estilo.css"` e `href="css/estilo.css"` em um site publicado em `usuario.github.io/site-evento/`? Qual dos dois funciona, e por quê?

**A5.** Para que serve o `.gitignore`? Cite três entradas típicas e explique o que aconteceria sem elas.

**A6.** Escreva, na ordem correta, a sequência completa de comandos para transformar uma pasta com o site em um repositório publicado no GitHub — do `git init` ao `git push -u origin main`.

**A7.** Quais são as quatro categorias avaliadas pelo Lighthouse e qual é a meta de cada uma na disciplina? Cite duas causas comuns de nota baixa em cada uma.

**A8.** Por que a auditoria do Lighthouse deve ser feita no site publicado, em janela anônima e no modo Mobile? O que cada uma dessas três escolhas evita?

**A9.** O que fazem os atributos `width`, `height` e `loading="lazy"` em uma tag `<img>`? Em qual imagem da sua página inicial você **não** deve usar `loading="lazy"`, e por quê?

**A10.** Para que servem as metatags `og:`? Por que a `og:image` precisa de URL absoluta, enquanto o `src` de uma `<img>` pode ser relativo?

### Nível B — Aplicação

**B1.** Publique o site do evento no GitHub Pages e produza um registro do processo: uma captura de tela de cada etapa (repositório criado, primeiro `push`, tela do Pages, site no ar) e um parágrafo descrevendo **um** problema que você encontrou e como o resolveu.

Resultado esperado: um arquivo `publicacao.md` no repositório, com as quatro capturas e o relato; o site acessível pela URL pública em janela anônima.

<details><summary>Dica</summary>

No GitHub, arraste a imagem para dentro do editor de arquivos: ele faz o upload e insere o Markdown sozinho. Se preferir versionar as capturas, crie `img/capturas/` e referencie com caminho relativo.
</details>

**B2.** Otimize todas as imagens do projeto: redimensione, converta para WebP, aplique `loading="lazy"` onde couber e declare `width` e `height` em todas. Registre o peso total da página inicial antes e depois, com as capturas da aba Network.

Resultado esperado: redução de pelo menos 60% no peso total transferido da página inicial, sem perda visível de qualidade; nenhuma imagem sem `alt`, `width` e `height`.

<details><summary>Dica</summary>

Na aba Network, o rodapé mostra `transferred` (o que veio pela rede) e `resources` (o tamanho descompactado). Compare o primeiro. Marque **Disable cache** antes de medir, senão a segunda medição vem do cache e não significa nada.
</details>

**B3.** Rode o Lighthouse no site publicado, registre as quatro pontuações iniciais, aplique todas as correções sugeridas pelo relatório e registre as pontuações finais. Escreva um parágrafo sobre qual correção teve o maior impacto e por quê.

Resultado esperado: uma tabela antes/depois com as quatro notas no `README.md` e as metas da disciplina atingidas.

<details><summary>Dica</summary>

Abra cada item reprovado no relatório: o Lighthouse mostra exatamente quais elementos causaram o problema e estima quantos milissegundos você ganha ao corrigir. Comece pelos de maior estimativa.
</details>

**B4.** Publique o mesmo projeto nas três plataformas (GitHub Pages, Netlify e Vercel) e compare: passos necessários, tempo até ficar no ar, o que cada painel oferece e o que faltou em cada um.

Resultado esperado: três URLs funcionais e uma tabela comparativa de no máximo quatro colunas, com sua conclusão sobre qual usar em cada situação.

<details><summary>Dica</summary>

Na Netlify e na Vercel, importe o **mesmo repositório** do GitHub — não recrie o projeto. Como o site é estático, o campo de comando de build fica vazio e o diretório de publicação é a raiz.
</details>

**B5.** Escreva o `README.md` completo do projeto seguindo o modelo da seção 9, acrescentando uma captura de tela da página inicial logo abaixo do título e uma lista de tarefas com `- [x]` mostrando o que já está pronto e o que ficou para depois.

Resultado esperado: o README renderizado no GitHub, sem link quebrado e sem imagem faltando, legível por alguém que nunca viu o projeto.

<details><summary>Dica</summary>

Teste o resultado renderizado, não o texto-fonte: uma imagem referenciada com caminho errado aparece como um ícone quebrado. Caminhos no README são relativos à raiz do repositório.
</details>

### Nível C — Desafio

**C1.** Faça uma **auditoria cruzada**: forme dupla com um colega, troquem as URLs publicadas e cada um audita o site do outro. Produza um relatório de uma página com as quatro notas do Lighthouse (mobile e desktop), o resultado da validação W3C de todas as páginas, a navegação completa por teclado (o que quebrou), o teste com zoom em 200% e uma lista priorizada de cinco problemas com a correção sugerida para cada um.

<details><summary>Dica</summary>

Auditar site alheio é mais fácil que auditar o próprio: você não tem os atalhos mentais de quem construiu. Comece pelo teclado — desconecte o mouse de verdade — e depois rode as ferramentas. Escreva os problemas de forma acionável: "o botão de filtro não recebe foco visível" vale mais do que "acessibilidade ruim".
</details>

**C2.** Configure o repositório com um fluxo de trabalho por branch: crie uma branch com uma melhoria (por exemplo, um modo escuro no CSS), publique-a, abra um **pull request** descrevendo a mudança, peça a revisão de um colega e só então faça o merge na `main`. Documente o processo com as URLs do PR e das revisões.

<details><summary>Dica</summary>

Os comandos são `git switch -c melhoria/modo-escuro`, os commits normais e `git push -u origin melhoria/modo-escuro`. O GitHub oferece o botão "Compare & pull request" sozinho quando detecta a branch nova. O [Capítulo 02 da trilha Deploy](../deploy/cap-02.html) tem o fluxo completo com revisão.
</details>

## 🏆 Desafios

### ⭐ O site que quebrou ao subir
Tags: deploy, bug, devtools, investigacao

O repositório abaixo quase funciona no Live Server do Windows e chega ao GitHub Pages sem estilo, sem imagens e com o JavaScript morto. São **cinco linhas com defeito**, e nenhum defeito é erro de sintaxe: todos são consequência das diferenças entre a sua máquina e um servidor Linux servindo o site em um subdiretório. Encontre as cinco lendo apenas as abas Console e Network do DevTools, sem baixar o repositório.

**`index.html`** (trecho do `<head>` e do corpo)

```html
<head>
  <meta charset="UTF-8">
  <title>Meu site</title>
  <link rel="stylesheet" href="/CSS/Estilo.css">
  <script src="js/App.js" defer></script>
</head>
<body>
  <img src="C:/Users/ana/projeto/img/logo.png" alt="Logotipo">
  <a href="/programacao.html">Programação</a>
  <img src="img/Foto Palestrante.JPG" alt="Palestrante">
</body>
```

**Critérios de pronto**

- Os cinco defeitos estão listados, cada um com o sintoma exato que aparece no DevTools (mensagem literal do console ou status da aba Network).
- Cada defeito tem a correção escrita, com o antes e o depois da linha.
- Um parágrafo explica por que **quatro** dos cinco passam despercebidos no Live Server do Windows — e identifica qual é o quinto, que falha em qualquer ambiente.
- A regra geral que evitaria os cinco de uma vez está enunciada em uma frase.

<details><summary>Pistas</summary>

1. Duas abas bastam: no Console aparecem os erros de script; na Network, o status de cada arquivo pedido.
2. Compare, letra a letra, o nome do arquivo no HTML e o nome real no repositório. Sistemas de arquivos do Linux não perdoam.
3. Qual é a raiz de `usuario.github.io/site-evento/`? Onde uma barra inicial faz o navegador procurar?
4. Um dos cinco defeitos nem chega a virar requisição HTTP: o navegador se recusa a buscar aquele endereço a partir de uma página web.
</details>

### ⭐⭐ Cem pontos em acessibilidade
Tags: acessibilidade, performance, devtools, deploy

O Lighthouse dá nota 100 em acessibilidade para páginas que um usuário de leitor de tela não consegue usar — ele testa o que é automatizável, e isso é menos da metade do problema. Neste desafio você faz as duas coisas: tira 100 na ferramenta **e** prova que o site funciona sem mouse e sem enxergar a tela.

**Critérios de pronto**

- As cinco páginas do site publicado marcam 100 em acessibilidade no Lighthouse, em Mobile e em Desktop.
- Um vídeo de até três minutos mostra a navegação completa de uma tarefa (abrir a programação, buscar uma palestra, ir à inscrição e preencher o formulário) **usando apenas o teclado**, com o foco visível em cada parada.
- O mesmo percurso é feito com um leitor de tela (NVDA no Windows, VoiceOver no macOS ou Orca no Linux) e relatado em texto: o que foi anunciado, o que ficou mudo, o que confundiu.
- Um relatório lista pelo menos três problemas que o Lighthouse **não** detectou e as correções aplicadas.
- Todas as correções estão publicadas no site no ar, não apenas no repositório local.

<details><summary>Pistas</summary>

1. Comece pelo relatório do Lighthouse: a seção "Additional items to manually check" lista justamente o que a ferramenta não consegue testar sozinha.
2. Ordem de tabulação, foco preso dentro de um menu aberto, mensagens que aparecem sem serem anunciadas e imagens decorativas com `alt` descritivo são os quatro problemas invisíveis mais comuns.
3. No NVDA, <kbd>Insert</kbd>+<kbd>F7</kbd> abre a lista de elementos da página: se os seus títulos e links não fizerem sentido fora do contexto visual, o problema aparece ali imediatamente.
4. Uma região `aria-live` só anuncia mudanças se já existir no HTML quando a página carrega. Criar o elemento junto com a mensagem faz o leitor de tela ignorá-la.
</details>

### ⭐⭐⭐ Meio megabyte, no máximo
Tags: performance, deploy, devtools, refatoracao

A página inicial de um site de evento não deveria pesar mais que um aplicativo de celular. Neste desafio, a meta é objetiva e medida por ferramenta: **a página inicial do seu site, carregada pela primeira vez em um navegador sem cache, transfere no máximo 500 KB no total** — HTML, CSS, JavaScript, fontes e imagens somados — mantendo o mesmo visual e as mesmas funcionalidades.

**Critérios de pronto**

- A aba Network, com **Disable cache** marcado e o perfil de rede em *Fast 4G*, mostra total transferido ≤ 500 KB na primeira carga da página inicial publicada.
- Uma tabela de no máximo quatro colunas mostra o peso por tipo de recurso (documento, estilo, script, imagem, fonte), antes e depois.
- O desempenho no Lighthouse mobile é ≥ 90, e a métrica de estabilidade visual (CLS) fica abaixo de 0,1.
- Nenhuma funcionalidade foi removida para atingir a meta, e nenhuma imagem ficou visivelmente pior. As decisões de compressão estão justificadas em um parágrafo.
- Um parágrafo final explica qual foi a otimização de maior impacto e quantos KB ela economizou.

<details><summary>Pistas</summary>

1. Ordene a aba Network pela coluna de tamanho, em ordem decrescente. Os três primeiros itens costumam responder por 80% do peso; comece por eles.
2. Fontes do Google Fonts entram com vários pesos por padrão. Cada peso é um arquivo. Dois pesos bastam para quase todo projeto — e uma fonte do sistema custa zero byte.
3. `<img>` aceita várias fontes com `srcset` e `sizes`: o navegador escolhe o arquivo certo para o tamanho da tela, e o celular deixa de baixar a imagem do desktop.
4. Ícones em SVG inline no HTML economizam uma requisição inteira cada. Se você usa uma biblioteca de ícones inteira por causa de cinco ícones, esse é o corte mais fácil da lista.
</details>

### 🔥 Boss — Do zero ao ar, em três horas
Tags: projeto, deploy, github, acessibilidade

Este é o desafio que fecha a Unidade 3 e a disciplina. A regra é simples e desconfortável: **um tema novo, do zero, publicado e auditado em três horas**. Sem reaproveitar o código do site do evento nem o do seu projeto autoral — só o que está na sua cabeça e a documentação aberta.

Escolha um tema que você nunca usou (catálogo de plantas do Pantanal, agenda de quadras do bairro, mural de estágios, brechó, controle de pescarias, cardápio de restaurante) e construa um site de três páginas que exercite tudo o que a disciplina cobriu: HTML semântico, CSS com sistema de design e responsividade, JavaScript com listagem renderizada a partir de dados, busca e formulário validado. Marque o tempo do início ao fim.

Esta é a simulação mais honesta do que se pede em um teste técnico de estágio — e a prova, para você mesmo, de que o semestre entrou.

**Critérios de pronto**

- Três páginas interligadas, HTML5 semântico, zero erros no validador do W3C nas três.
- CSS externo com variáveis, layout em Grid ou Flexbox, responsivo em pelo menos duas larguras e estados `:hover`, `:focus-visible` e `:active` nos elementos interativos.
- Uma listagem renderizada por JavaScript a partir de um array de objetos, com busca funcionando e estado vazio tratado.
- Um formulário com validação em JavaScript, incluindo pelo menos uma regra por expressão regular e mensagens de erro acessíveis por campo.
- Publicado no GitHub Pages, em repositório público próprio, com `README.md`, `.gitignore` e página `404.html`.
- Lighthouse no site publicado: acessibilidade ≥ 90 e SEO ≥ 90.
- Um `RELATO.md` no repositório com o tempo total gasto, o que você conseguiu de memória, o que precisou consultar e o que faria diferente com mais uma hora.

<details><summary>Pistas</summary>

1. Planeje quinze minutos antes de escrever a primeira linha: as três páginas, os campos do formulário e os cinco atributos dos objetos da listagem. Quem começa pelo CSS não termina.
2. Comece pelo HTML das três páginas inteiro, depois o CSS, depois o JavaScript. Trocar de camada o tempo todo custa mais do que parece.
3. Publique **antes** de terminar — no primeiro commit que renderiza alguma coisa. Um site incompleto no ar vale mais que um site completo que quebrou na publicação e não deu tempo de investigar.
4. Guarde os últimos trinta minutos para auditar: validador, Lighthouse, teclado e o teste no celular. É onde os pontos aparecem.
</details>

**Para ir além:** publique o repositório com um tópico (*topic*) `weblab` no GitHub e compare o seu resultado com o dos colegas da turma.

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| O site publicado aparece "cru", sem nenhum estilo | O `href` do CSS começa com `/` e aponta para a raiz do `github.io`, não do repositório | Use caminho relativo: `href="css/estilo.css"` |
| `Failed to load resource: the server responded with a status of 404 ()` para o CSS | Nome do arquivo com maiúscula diferente da referência no HTML | Padronize tudo em minúsculas e corrija a referência |
| `net::ERR_FILE_NOT_FOUND` em uma imagem | `src` com caminho de disco (`C:/Users/...`) em vez de relativo | Mova a imagem para `img/` e use `src="img/arquivo.webp"` |
| A URL do Pages devolve a página do mascote do GitHub | Não existe `index.html` na raiz do repositório, ou o Pages foi apontado para a pasta errada | Renomeie o arquivo de entrada para `index.html` e escolha `/ (root)` em Settings → Pages |
| `Your site is live` não aparece e o repositório não tem a aba Pages ativa | Repositório privado no plano gratuito | Settings → General → Change visibility → Public |
| A alteração não aparece no site depois do `git push` | Cache do navegador ou publicação ainda em andamento | Recarregue com <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>R</kbd> e confira a aba Actions do repositório |
| `fatal: not a git repository (or any of the parent directories): .git` | O terminal está numa pasta acima ou abaixo da pasta do projeto | `cd` até a pasta que contém o `index.html` e rode `git init` ali |
| `error: remote origin already exists.` | O `git remote add origin` foi executado duas vezes | `git remote set-url origin <url-correta>` |
| `Updates were rejected because the remote contains work that you do not have locally` | O repositório do GitHub foi criado com README, gerando um commit que você não tem | `git pull --rebase origin main` e depois `git push` |
| `Support for password authentication was removed` ao dar `push` | O GitHub não aceita mais senha de conta pela linha de comando | Autentique pelo navegador quando o Git pedir, ou configure chave SSH |
| Os seus commits aparecem no GitHub sem foto e sem link para o seu perfil | O `user.email` do Git é diferente do e-mail cadastrado na conta do GitHub | `git config --global user.email` com o e-mail da conta; os commits novos já saem vinculados |
| `Mixed Content: The page at 'https://…' was loaded over HTTPS, but requested an insecure element` | Alguma URL do site está escrita com `http://` | Troque por `https://` ou por caminho relativo |
| Lighthouse com nota de desempenho abaixo de 40 | Imagens em tamanho original, de vários megabytes cada | Redimensione, converta para WebP e declare `width`/`height` |
| A nota de práticas recomendadas cai sem motivo aparente | Auditoria rodada com extensões do navegador ativas | Rode em janela anônima, com as extensões desabilitadas |
| A prévia do link no WhatsApp mostra só a URL, sem cartão | Falta `og:title`, `og:description` ou `og:image`, ou a `og:image` está com caminho relativo | Preencha as três com URL absoluta na imagem e teste em uma conversa consigo mesmo |
| Uma pasta com nome começando por `_` não aparece no site | O Jekyll do GitHub Pages ignora arquivos e pastas iniciados por sublinhado | Crie um arquivo vazio `.nojekyll` na raiz do repositório |

## 🏠 Para praticar depois da aula (1 h)

**Parte 1 — Leitura (15 min).** MILETTO & BERTAGNOLLI, *Desenvolvimento de software II*, capítulo sobre implantação. TERUEL, *HTML 5 — Guia Prático*, capítulo de publicação. Na documentação oficial do GitHub Pages, a página "Configuring a publishing source for your GitHub Pages site". Anote uma diferença entre o processo descrito no livro e o que você fez hoje.

**Parte 2 — Produção (40 min).** No seu **projeto autoral**:

1. Publique o projeto autoral no GitHub Pages, com repositório público e `README.md` completo conforme o modelo da seção 9.
2. Otimize todas as imagens e registre no README o peso total da página inicial **antes** e **depois**, com as duas capturas da aba Network.
3. Rode o Lighthouse no site publicado (Mobile, janela anônima), registre as quatro notas no README e aplique as correções necessárias até atingir as metas deste material (veja o Marco 3, logo abaixo).
4. Valide as páginas no validador do W3C até zero erros e crie a página `404.html` personalizada.

**Critério de pronto:** o link público abre o site em qualquer máquina, em janela anônima; o console está limpo; o validador não aponta erros; o README traz o link do site, as quatro notas do Lighthouse e a comparação de peso.

**Parte 3 — Discussão (5 min).** Em texto próprio (ou no fórum da turma, se você cursa a disciplina): poste o link do seu projeto autoral publicado, com uma frase sobre o problema mais difícil da publicação. Se puder, peça a um colega para abrir o link, rodar o Lighthouse e devolver um elogio específico e uma sugestão acionável.

**Guarde no seu repositório:** o link do site publicado, registrado no README.

## ✅ Checkpoint do projeto

- [ ] Repositório público no GitHub, com `.gitignore`, `.nojekyll` e `README.md` completo na raiz.
- [ ] Histórico com pelo menos cinco commits de mensagens descritivas, no imperativo.
- [ ] Site publicado e acessível por URL pública, com HTTPS ativo, aberto em janela anônima.
- [ ] `index.html` na raiz; nomes de arquivos e pastas em minúsculas, sem espaços e sem acentos.
- [ ] Nenhum caminho interno absoluto, exceto os da `404.html`.
- [ ] Página `404.html` personalizada, servida em qualquer caminho inexistente.
- [ ] `title` e `description` próprios em cada página; metatags `og:` com `og:image` em URL absoluta; favicon aparecendo na aba.
- [ ] Todas as imagens otimizadas (WebP ou SVG), com `alt`, `width`, `height` e `loading="lazy"` onde couber.
- [ ] Zero erros no validador do W3C nas cinco páginas.
- [ ] Console limpo e nenhum `404` na aba Network, nas cinco páginas do site publicado.
- [ ] Lighthouse no site publicado: desempenho ≥ 80; acessibilidade, práticas recomendadas e SEO ≥ 90.
- [ ] Site testado em celular real com dados móveis e navegável inteiramente por teclado.

## 🎓 Marco do projeto — Unidade 3

**Escopo.** Ao fim da Unidade 3, o seu **projeto autoral** — o mesmo dos Marcos 1 e 2, com as correções apontadas já aplicadas — precisa estar dinâmico e interativo com **JavaScript** (eventos, validação de formulários e consultas dinâmicas) e **publicado na internet**.

**Requisitos.**

| # | Requisito | Onde foi estudado |
|---|---|---|
| 1 | JavaScript externo, carregado com `defer`, organizado em funções nomeadas | Aula 10 |
| 2 | Código estruturado nos blocos ESTADO → ELEMENTOS → DADOS → RENDERIZAÇÃO → EVENTOS → INICIALIZAÇÃO | Aula 13 |
| 3 | Dados do domínio em um array de objetos, em arquivo próprio | Aula 12 |
| 4 | Listagem renderizada a partir desse array, com `textContent`, e estado vazio tratado | Aulas 12 e 13 |
| 5 | Menu responsivo funcional em JavaScript, acessível por teclado, com `aria-expanded` | Aula 13 |
| 6 | Delegação de eventos em pelo menos uma lista dinâmica | Aula 13 |
| 7 | Busca com normalização de acentos e `debounce`, mais um filtro e uma ordenação | Aula 14 |
| 8 | Formulário validado em JavaScript, com pelo menos uma regra por expressão regular | Aula 14 |
| 9 | Mensagens de erro específicas por campo, com `role="alert"`, `aria-invalid` e `aria-describedby` | Aula 14 |
| 10 | Uso de condicionais, laços e operadores com valores calculados na página | Aulas 11 e 12 |
| 11 | Zero erros no console durante o uso normal, nas páginas todas | Aulas 13 a 15 |
| 12 | Repositório público no GitHub, com `.gitignore`, `README.md` e ao menos cinco commits descritivos | Aula 15 |
| 13 | Site publicado, acessível por URL pública com HTTPS, e `404.html` personalizada | Aula 15 |
| 14 | Imagens otimizadas, metatags de SEO e Open Graph em todas as páginas | Aula 15 |
| 15 | Zero erros no validador do W3C e Lighthouse com acessibilidade ≥ 90 no site publicado | Aula 15 |

Frameworks e bibliotecas de JavaScript (jQuery, React, Vue e similares) não entram aqui — o objetivo deste marco é demonstrar domínio da linguagem pura. O site publicado é o que fecha o marco: um projeto que só existe na sua máquina ainda não chegou lá.

**Checklist de qualidade.**

- Interatividade construída com eventos, delegação e manipulação do DOM, não com gambiarras.
- Formulário validado com regras claras, regex corretas e mensagens acessíveis (não só cor).
- Consultas dinâmicas (busca, filtro, ordenação) com estados vazios tratados com uma mensagem de verdade, não uma tela em branco.
- Código JavaScript organizado e legível — você deveria conseguir reabri-lo em seis meses e entender na hora.
- Publicação completa: repositório com histórico de commits que conta uma história, README que orienta um estranho e site no ar com HTTPS.
- Qualidade auditada: validador W3C e Lighthouse sem alertas ignorados.
- Coerência do projeto como um todo — o visitante não percebe onde uma aula terminou e a outra começou.

**Como saber que está pronto.**

- Abra o site publicado em uma janela anônima, em outro computador se possível: se abrir e funcionar sem nada da sua máquina, está no ar de verdade.
- Rode o Lighthouse (Mobile) no site publicado: desempenho ≥ 80; acessibilidade, boas práticas e SEO ≥ 90.
- No Console, use o site inteiro (busca, filtro, formulário) e confirme zero linhas vermelhas.
- Peça para alguém preencher o formulário tentando errar de propósito: as mensagens de erro precisam fazer sentido para quem não escreveu o código.
- Use IA para tirar dúvida ou revisar uma abordagem — não para gerar a lógica inteira. Se você não souber explicar por que os blocos do seu `app.js` estão naquela ordem, ainda não é seu.

## 📚 Para aprofundar

- GitHub Docs — **Criando um site do GitHub Pages** (pt-BR): <https://docs.github.com/pt/pages/getting-started-with-github-pages/creating-a-github-pages-site> — a referência oficial do que você fez na Mão na massa.
- GitHub Docs — **Configurando um domínio personalizado**: <https://docs.github.com/pt/pages/configuring-a-custom-domain-for-your-github-pages-site> — registros DNS e o arquivo `CNAME`, passo a passo.
- GitHub Docs — **Sobre READMEs**: <https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes> — o que a plataforma espera desse arquivo.
- Git — **Livro Pro Git em português**: <https://git-scm.com/book/pt-br/v2> — leia os capítulos 1 e 2; são as duas horas mais bem investidas da sua vida de programador.
- MDN — **HTTPS**: <https://developer.mozilla.org/pt-BR/docs/Glossary/HTTPS> — o glossário explica o essencial em cinco minutos.
- MDN — **`<img>` e imagens responsivas**: <https://developer.mozilla.org/pt-BR/docs/Learn_web_development/Core/Structuring_content/Responsive_images> — `srcset` e `sizes` para o desafio ⭐⭐⭐.
- MDN — **Adicionando metadados com `<meta>`**: <https://developer.mozilla.org/pt-BR/docs/Learn_web_development/Core/Structuring_content/Webpage_metadata> — inclui Open Graph e favicon.
- web.dev — **Lighthouse**: <https://web.dev/explore/lighthouse> — o que cada auditoria mede e como interpretar cada nota.
- web.dev — **Core Web Vitals**: <https://web.dev/articles/vitals> — as três métricas que o Google usa para classificar a experiência de uma página.
- Squoosh: <https://squoosh.app> — compressão e conversão de imagens no próprio navegador, com comparação lado a lado.
- Validador do W3C: <https://validator.w3.org> — valide todas as páginas pelo modo Address, no site publicado.
- Netlify Docs — **Deploy overview**: <https://docs.netlify.com/deploy/deploy-overview/> — a alternativa com formulários e prévia por branch.
- Open Graph protocol: <https://ogp.me> — a especificação das metatags `og:`, curta e legível.
- MILETTO, Evandro M.; BERTAGNOLLI, Silvia C. *Desenvolvimento de software II*. Bookman, 2014 — capítulo de implantação e manutenção.
- TERUEL, Evandro C. *HTML 5 — Guia Prático*. Saraiva, 2014 — capítulo de publicação de sites.
- SILVA, Maurício Samy. *Criando sites com HTML*. Novatec, 2008 — releia o capítulo de boas práticas agora que você tem um site inteiro para comparar.

---

## 🎓 Fim da disciplina — para onde ir agora

Quinze aulas atrás você abriu um arquivo vazio e escreveu `<!DOCTYPE html>` sem saber direito por quê. Hoje você tem, no ar, um site de cinco páginas com estrutura semântica, um sistema de design em CSS, layout responsivo, animações que respeitam quem prefere menos movimento, listagens geradas por JavaScript, busca, filtro, ordenação e um formulário que valida CPF de verdade. E, o mais importante: **você entende cada linha**, porque escreveu cada uma.

Guarde o repositório. Ele já é peça de portfólio — o tipo de link que se coloca em um currículo de estágio e que sobrevive a qualquer pergunta de entrevista, porque você sabe explicar o que fez.

### O Nível 2, a continuação direta

O [Nível 2 — Desenvolvimento Web](../nivel-2/) (FACET-SNP-307) tem esta disciplina como pré-requisito e continua exatamente de onde você parou. Lá, o CSS escrito à mão ganha a companhia de frameworks (Bootstrap e Tailwind) e de SVG; o `js/dados.js` com o array fixo vira um `fetch` que busca dados de uma API real, com `async/await`, estados de carregamento e tratamento de erro; as cinco páginas HTML viram uma **SPA**, uma aplicação de página única com navegação sem recarregamento. E, na terceira unidade, o JavaScript sai do navegador: com **Node.js e Express** você escreve o servidor que responde às requisições, adiciona login com conta Google e constrói um CRUD completo, com dados que sobrevivem ao fechar do navegador.

O projeto fio-condutor de lá é o **Café Cerrado**, uma cafeteria fictícia que percorre o mesmo caminho: site estático, depois dinâmico, depois full-stack.

### A trilha Deploy, para quando publicar virar rotina

Hoje você publicou clicando em botões. A trilha [Deploy & Ferramentas](../deploy/) é transversal e transforma isso em processo: o [Capítulo 02](../deploy/cap-02.html) leva o seu Git de seis comandos a branches, conflitos e pull requests revisados; o [Capítulo 03](../deploy/cap-03.html) aprofunda a publicação de sites estáticos com prévia por branch, cache e redirecionamentos; o [Capítulo 09](../deploy/cap-09.html) automatiza tudo com GitHub Actions, para que cada `git push` valide, audite e publique sozinho.

### Por conta própria, até lá

- **Refaça o site do evento com outro tema, do zero.** É o Boss desta aula, e é o exercício que mais consolida.
- **Contribua com um projeto de código aberto.** Comece por uma correção de documentação em português: é uma contribuição real, e o fluxo de pull request é o mesmo dos projetos grandes.
- **Leia o código dos sites que você usa.** <kbd>Ctrl</kbd>+<kbd>U</kbd> mostra o HTML de qualquer página. Você já entende boa parte dele — e a parte que não entende é a sua próxima lista de estudo.
- **Publique tudo o que fizer.** Um projeto no ar vale mais que dez pastas na sua máquina. O hábito de terminar e publicar é, sozinho, uma vantagem competitiva.

Na próxima aula da sua trajetória — a Aula 01 do [Nível 2 — Desenvolvimento Web](../nivel-2/) — o Café Cerrado começa com um `index.html` vazio, exatamente como este começou. A diferença é que, desta vez, você já sabe o que fazer com ele. Bons deploys a todos.
