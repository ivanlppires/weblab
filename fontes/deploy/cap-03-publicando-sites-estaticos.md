# Capítulo 03 — Publicando sites estáticos

> **Deploy & Ferramentas** · Unidade 2: Publicação: estático, back-end, domínio e servidor
> WebLab · UNEMAT — Campus Sinop
> **Tempo estimado:** 2 a 3 h · estudo autônomo, em paralelo à sua trilha

## 🎯 Objetivos de aprendizagem

Ao final deste capítulo você será capaz de:

- Explicar o que uma hospedagem estática faz (e o que ela **não** faz), por que ela é rápida e por que é gratuita para projetos como os seus.
- Publicar um repositório no **GitHub Pages** pelas configurações do site e pelo terminal (`gh api`), e ler o estado da publicação sem sair do terminal.
- Distinguir caminho **relativo ao documento**, **relativo à raiz** e **absoluto**, prever para onde cada um resolve e consertar um site que perde o CSS ao ser publicado em um subcaminho como `usuario.github.io/site-evento/`.
- Colocar favicon, ícone de tela inicial e `site.webmanifest` em um site publicado em subcaminho, sem depender do pedido automático que o navegador faz à raiz do domínio.
- Criar uma página `404.html` que funciona em qualquer profundidade de URL, no GitHub Pages e na Netlify.
- Publicar na **Netlify** por arrastar-e-soltar e a partir do Git, com um `netlify.toml` que define diretório publicado, redirecionamentos e cabeçalhos.
- Comparar GitHub Pages, Netlify, Vercel e Cloudflare Pages e justificar a escolha para um projeto específico.
- Ler `cache-control`, `etag` e `age` com `curl -I`, explicar por que a versão antiga insiste em aparecer e resolver com recarga forçada e nomes versionados.
- Rodar o Lighthouse contra a URL pública e transformar o relatório em uma lista de correções concretas.

## 📋 Pré-requisitos

- [ ] Repositório `site-evento` no GitHub, público, com `README.md` e histórico limpo (Capítulo 02) — ou o repositório do seu projeto autoral.
- [ ] `git` e `gh` funcionando: `gh auth status` responde `Logged in to github.com`.
- [ ] `curl` instalado (`curl --version`) e o navegador com DevTools (Capítulo 01).
- [ ] Uma conta na Netlify (pode entrar com a conta do GitHub) — <https://app.netlify.com>.
- [ ] Node.js 22 LTS instalado, para rodar o Lighthouse com `npx` no fim do capítulo.

> No Capítulo 02 o `site-evento` virou um repositório com histórico legível, um pull request mesclado e uma tag `v1.0.0` — mas ele ainda só existe na sua máquina e em um repositório que só desenvolvedores sabem ler. Hoje ele ganha um endereço que você pode mandar para qualquer pessoa. E, no caminho, você resolve os dois problemas que o Capítulo 01 prometeu resolver aqui: o `favicon.ico` com 404 no console e a diferença entre caminho absoluto e relativo, que é a causa número um de "publiquei e o site ficou sem CSS".

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 45 min | O que é hospedagem estática; GitHub Pages pelo painel e pelo `gh`; caminhos absolutos e relativos (§1 a §3) |
| 2 | 45 min | Favicon, `404.html`, Netlify (arrastar-e-soltar, Git e `netlify.toml`), Vercel e Cloudflare Pages; cache e Lighthouse (§4 a §9) |
| 3 | 60 min | Passo a passo: `site-evento` no GitHub Pages e `cafe-cerrado` na Netlify + Laboratório |

## 1. O que é uma hospedagem estática

### 1.1 Arquivos, não programas

Um **site estático** é uma pasta de arquivos: HTML, CSS, JavaScript, imagens, fontes. Quando alguém pede `https://ana-souza.github.io/site-evento/programacao.html`, o servidor procura o arquivo `programacao.html` dentro da pasta publicada e devolve os bytes. Ele não executa nada seu, não consulta banco, não decide nada. O JavaScript existe, mas roda **no navegador de quem visita**, não no servidor.

Isso é uma limitação enorme e, ao mesmo tempo, a razão de tudo o que vem a seguir ser fácil:

| Consequência | Por quê |
|---|---|
| É rápido | Devolver um arquivo já pronto custa quase nada; não há código para rodar antes |
| É barato (grátis, nos seus projetos) | Copiar arquivos para servidores é a operação mais barata que existe na internet |
| Escala sozinho | Dez ou dez mil visitantes pedem o mesmo arquivo; o servidor só repete a resposta |
| Não quebra sozinho | Não há processo para cair, memória para vazar, conexão de banco para expirar |
| É difícil de invadir | Não há código seu no servidor para explorar |

E o que ele **não** faz: guardar uma inscrição enviada por formulário, verificar uma senha, listar produtos de um banco, esconder uma chave de API. Tudo isso exige um processo rodando do lado do servidor — é o assunto do Capítulo 05. Por enquanto, se o seu formulário de inscrição precisa de fato receber respostas, a saída honesta é apontar o `action` para um serviço de formulários (a Netlify tem um embutido) ou usar `mailto:`.

### 1.2 CDN: por que o site fica perto de quem acessa

As quatro plataformas deste capítulo não guardam o seu site em um servidor só. Elas copiam os arquivos para uma **CDN** (*Content Delivery Network*): uma rede de servidores espalhados pelo mundo, com pontos de presença em várias cidades. Quem acessa de Sinop é atendido por um servidor perto de Sinop; quem acessa de Lisboa, por um perto de Lisboa.

```text
   você faz                     a plataforma copia para
   git push  ──►  build  ──►  dezenas de servidores (CDN)
                                │        │        │
                             São Paulo  Miami   Frankfurt
                                │        │        │
                             visitante visitante visitante
```

O ganho é de **latência**, não de banda: cada ida e volta até um servidor a 8.000 km custa uns 200 ms, e uma página faz várias idas e voltas. É por isso que um site estático bem publicado costuma abrir em menos de um segundo, mesmo em 4G.

> **🧠 Você sabia?**
> O GitHub Pages nasceu em 2008 e, até hoje, roda por padrão um gerador de sites chamado **Jekyll**, escrito por Tom Preston-Werner — um dos fundadores do próprio GitHub — para publicar o blog dele. É por isso que o GitHub Pages tem manias estranhas de gerador de blog: pastas cujo nome começa com `_` recebem tratamento especial e podem sumir do site publicado. A §2.4 mostra o arquivo de uma linha que desliga isso.

### 1.3 O que muda em relação ao Live Server

No Capítulo 01 você abriu o site com o Live Server, em `http://127.0.0.1:5500/site-evento/index.html`. Na publicação, quatro coisas mudam — e todas viram bug se você não souber:

1. **A raiz do site muda.** No Live Server a raiz é a pasta que você abriu no VS Code. No GitHub Pages de projeto, o site vive dentro de `/site-evento/`, e a raiz do domínio pertence a outro site. É a §3 inteira.
2. **O sistema de arquivos diferencia maiúsculas.** Windows e macOS, por padrão, tratam `Logo.png` e `logo.png` como o mesmo arquivo. O servidor Linux da CDN não. Um `<img src="img/Logo.png">` que funciona na sua máquina devolve 404 no ar.
3. **Existe cache.** O Live Server manda o navegador nunca guardar nada. A CDN faz o contrário: guarda tudo o que puder, por minutos ou meses. É a §8.
4. **Só vai para o ar o que está no Git.** Se `img/logo.png` está no `.gitignore`, ou se você esqueceu de commitar, ele simplesmente não existe do lado de lá.

> **🔬 Investigue**
> Rode `curl -I https://weblab.ivanpires.dev` e `curl -I https://github.com` e compare os cabeçalhos das duas respostas. Procure `server`, `cache-control`, `content-type` e `etag`. Depois rode `curl -I https://weblab.ivanpires.dev/pagina-que-nao-existe` e anote o código de status. O `-I` pede só os cabeçalhos (método `HEAD`) — é a forma mais rápida de saber quem está servindo um site e como ele manda o navegador guardar as respostas.

## 2. GitHub Pages

### 2.1 Os dois tipos de site

O GitHub Pages publica o conteúdo de um repositório em um endereço `*.github.io`. Existem dois formatos, e a diferença entre eles é a origem da maior parte dos problemas deste capítulo:

| Tipo | Nome do repositório | URL publicada |
|---|---|---|
| Site de usuário | exatamente `<usuario>.github.io` | `https://<usuario>.github.io/` |
| Site de projeto | qualquer outro nome | `https://<usuario>.github.io/<repositorio>/` |

Você tem **um** site de usuário por conta e **quantos sites de projeto quiser**. O `site-evento` é um site de projeto: ele vai morar em `https://ana-souza.github.io/site-evento/` — dentro de um subcaminho, e não na raiz do domínio.

Guarde isso: **o seu site não está na raiz**. A §3 existe por causa desta frase.

### 2.2 Publicando pelo painel

O caminho oficial tem cinco cliques:

1. Abra o repositório no GitHub (`gh repo view --web` faz isso do terminal).
2. **Settings** (aba do topo, à direita) → **Pages** (menu da esquerda, seção *Code and automation*).
3. Em **Build and deployment → Source**, escolha **Deploy from a branch**.
4. Em **Branch**, escolha `main` e a pasta `/ (root)`. Clique em **Save**.
5. Espere. Volte para a aba **Actions** do repositório: existe uma execução chamada **pages build and deployment**. Quando ela ficar verde, o site está no ar.

A caixa de **Branch** oferece duas pastas: `/ (root)` e `/docs`. Use `/ (root)` quando o `index.html` está na raiz do repositório — é o caso do `site-evento`. Use `/docs` quando o site é só uma parte de um repositório maior (documentação de uma API, por exemplo).

A opção **GitHub Actions**, no mesmo menu **Source**, serve para sites que precisam ser **construídos** antes de publicar — um projeto Vite do Nível 3, por exemplo, em que o que vai ao ar é a pasta `dist/`, e não os fontes. Esse é o assunto do Capítulo 09; aqui, o site já está pronto no repositório.

> **⚠️ Atenção**
> O GitHub Pages é gratuito para **repositórios públicos**. Em repositório privado, ele exige uma conta paga. Neste projeto o repositório é público de qualquer jeito, então isso não te afeta — mas não coloque no `site-evento` nada que você não mostraria a qualquer pessoa. Publicar é publicar.

### 2.3 Publicando pelo terminal, com o `gh`

Tudo o que o painel faz, a API do GitHub também faz — e o `gh api` fala com ela. Dentro da pasta do repositório, os marcadores `{owner}` e `{repo}` são preenchidos sozinhos com o repositório atual:

```bash
# Liga o Pages, servindo a raiz da branch main
gh api --method POST repos/{owner}/{repo}/pages \
  -f "source[branch]=main" \
  -f "source[path]=/"
```

A resposta é um JSON com a configuração criada. Para acompanhar o estado sem abrir o navegador:

```bash
# Estado atual, URL pública e origem da publicação
gh api repos/{owner}/{repo}/pages --jq '{status: .status, url: .html_url, branch: .source.branch}'

# Última construção: status e mensagem de erro, se houver
gh api repos/{owner}/{repo}/pages/builds/latest --jq '{status: .status, erro: .error.message}'
```

O campo `status` passa por `building` e termina em `built`. Se der `errored`, a mensagem em `.error.message` diz o motivo (quase sempre uma sintaxe que o Jekyll não engoliu — veja a §2.4).

Se você mudar a configuração depois, o verbo é `PUT`, não `POST`:

```bash
# Trocar a pasta publicada de / para /docs
gh api --method PUT repos/{owner}/{repo}/pages \
  -f "source[branch]=main" \
  -f "source[path]=/docs"

# Pedir uma reconstrução manual (útil quando a publicação travou)
gh api --method POST repos/{owner}/{repo}/pages/builds
```

Saber fazer isso pelo terminal não é frescura: é o que permite automatizar a criação de um projeto inteiro em um script, como no Boss do Capítulo 02, e é a mesma API que o GitHub Actions usa no Capítulo 09.

### 2.4 As três manias do GitHub Pages

**Jekyll come pastas com `_`.** Por padrão, o Pages processa o site com o Jekyll antes de publicar, e o Jekyll trata pastas iniciadas por sublinhado como pastas de trabalho dele — elas não vão para o site. Um projeto Vite gera `_assets/` ou nomes parecidos, e o resultado é um site sem CSS e sem JS. A solução é um arquivo vazio na raiz do site:

```bash
touch .nojekyll
git add .nojekyll
git commit -m "Desliga o processamento Jekyll no GitHub Pages"
git push
```

Crie esse arquivo **sempre**. Ele não atrapalha nada e evita uma tarde de depuração.

**O `index.html` manda.** Se não existe `index.html` na pasta publicada, o Pages mostra o `README.md` renderizado — e o estudante jura que "publicou errado". Não publicou: publicou uma pasta sem página inicial.

**Existem limites, e eles são suaves.** O site publicado deve ficar abaixo de 1 GB, a banda mensal recomendada é de 100 GB e há um limite de dez construções por hora. Nenhum projeto de disciplina chega perto disso, mas vale saber que existe — e que a documentação oficial é a fonte a conferir, porque os números mudam.

> **📌 Vale gravar**
> "Um site estático pode ter formulário de login?" Não com validação de verdade: qualquer verificação feita em JavaScript no navegador é lida e burlada por quem abre o DevTools. Autenticação exige servidor. Um site estático pode ter o **formulário**; a verificação precisa acontecer do outro lado.

## 3. Caminhos absolutos e relativos: o bug que aparece só depois de publicar

Este é o problema anunciado no Capítulo 01, e ele merece a seção mais longa deste capítulo. O sintoma é sempre o mesmo: **na sua máquina o site está perfeito; publicado, ele aparece sem estilo, sem imagens e sem JavaScript, como um documento de texto dos anos 90.**

### 3.1 Os três tipos de caminho

Todo `href`, `src` e `url()` do seu código é resolvido pelo navegador contra a URL da página atual. Há três formas de escrever:

| Forma | Exemplo | Como resolve |
|---|---|---|
| Relativo ao documento | `css/estilo.css`, `./css/estilo.css`, `../img/logo.png` | A partir da **pasta da página atual** |
| Relativo à raiz | `/css/estilo.css` | A partir da **raiz do domínio**, ignorando a pasta atual |
| Absoluto | `https://ana-souza.github.io/site-evento/css/estilo.css` | Endereço completo, ignora tudo |

A confusão de nome atrapalha: muita gente chama `/css/estilo.css` de "caminho absoluto". Ele é absoluto **dentro do domínio** — e é exatamente por isso que ele quebra quando o domínio não é seu inteiro.

### 3.2 Onde cada um vai parar

Suponha a página `https://ana-souza.github.io/site-evento/programacao.html`. Veja para onde o navegador manda cada requisição:

| Escrito no HTML | O navegador pede |
|---|---|
| `css/estilo.css` | `https://ana-souza.github.io/site-evento/css/estilo.css` ✔ |
| `./css/estilo.css` | `https://ana-souza.github.io/site-evento/css/estilo.css` ✔ |
| `/css/estilo.css` | `https://ana-souza.github.io/css/estilo.css` ✘ 404 |
| `../css/estilo.css` | `https://ana-souza.github.io/css/estilo.css` ✘ 404 |
| `img/logo.png` | `https://ana-souza.github.io/site-evento/img/logo.png` ✔ |
| `/img/logo.png` | `https://ana-souza.github.io/img/logo.png` ✘ 404 |

Na sua máquina, com o Live Server servindo a pasta `site-evento` como raiz, `/css/estilo.css` resolve para `http://127.0.0.1:5500/css/estilo.css` e **funciona**. É a mesma linha, com dois destinos diferentes. Por isso o bug só aparece depois do `git push`.

A regra prática para sites publicados em subcaminho é curta: **nada de barra no começo**. Use caminhos relativos ao documento em todo o HTML, no CSS e no JavaScript.

> **🔬 Investigue**
> Abra o `site-evento` no Live Server. No `index.html`, troque `href="css/estilo.css"` por `href="/css/estilo.css"` e recarregue: continua funcionando. Agora abra o DevTools → **Network**, recarregue e clique na linha do `estilo.css`: leia a **Request URL** completa. Some `/site-evento` mentalmente à frente do host e você acaba de simular o que vai acontecer no ar. Desfaça a mudança.

### 3.3 O detalhe da barra final

Existe uma armadilha extra, e ela pega gente experiente. Compare:

```text
https://ana-souza.github.io/site-evento/     →  a pasta é /site-evento/
https://ana-souza.github.io/site-evento      →  a "pasta" é /
```

Sem a barra final, o navegador considera que `site-evento` é um **arquivo** e resolve `css/estilo.css` como `/css/estilo.css`. O GitHub Pages e a Netlify normalmente redirecionam a URL sem barra para a URL com barra (`301`), e o problema desaparece — mas um servidor mal configurado não redireciona, e aí você tem um site quebrado só quando o link vem sem a barra.

Duas consequências práticas: ao divulgar o endereço, **inclua a barra final**; e, ao linkar uma pasta dentro do seu site, escreva `<a href="blog/">`, não `<a href="blog">`.

### 3.4 Páginas em subpastas mudam a conta

Caminho relativo ao documento depende da **profundidade** da página. Se você criar `blog/post-1.html`, o `css/estilo.css` escrito lá dentro resolve para `/site-evento/blog/css/estilo.css` — que não existe. De dentro de uma subpasta, o caminho correto é `../css/estilo.css`.

Enquanto o site é plano (todas as páginas na raiz, como o `site-evento`), isso não aparece. Quando o site cresce, há três saídas:

1. **Contar os `../` em cada página.** Funciona, é chato e quebra quando você move um arquivo.
2. **Usar `<base>`.** Uma única tag no `<head>` redefine a base de todos os caminhos relativos daquele documento:

`blog/post-1.html`

```html
<head>
  <meta charset="UTF-8">
  <base href="/site-evento/">
  <link rel="stylesheet" href="css/estilo.css">
</head>
```

Com essa `<base>`, `css/estilo.css` resolve para `/site-evento/css/estilo.css` de qualquer profundidade. O preço: a `<base>` afeta **tudo**, inclusive links de âncora (`href="#programacao"` passa a apontar para `/site-evento/#programacao`, o que muda a página) e requisições de JavaScript. Use com consciência, e sempre com a barra final.

3. **Deixar o construtor resolver.** É o que Vite e companhia fazem: você declara a base uma vez e a ferramenta reescreve todos os caminhos no build.

`vite.config.js`

```js
import { defineConfig } from 'vite'

export default defineConfig({
  // O site será servido em https://<usuario>.github.io/unieventos-web/
  // Sem esta linha, o Vite gera caminhos começando com / e o site publica quebrado.
  base: '/unieventos-web/'
})
```

Também dá para passar a base na linha de comando, sem tocar no arquivo — é o que o workflow do Capítulo 09 faz:

```bash
npm run build -- --base=/unieventos-web/
```

E, no código Vue/JS do projeto, o valor fica disponível em `import.meta.env.BASE_URL`, para montar caminhos de imagens dinâmicas sem chutar prefixo.

> **💡 Dica**
> Antes de publicar, cace os caminhos com barra inicial em todo o projeto de uma vez:
>
> ```bash
> grep -rn 'href="/\|src="/\|url(/' --include='*.html' --include='*.css' --include='*.js' .
> ```
>
> Cada linha que aparecer é um candidato a 404 no ar. As exceções legítimas são URLs completas (`https://…`), uma `<base href>` deliberada e os caminhos dentro do `404.html`, explicados na §5.

### 3.5 Maiúsculas contam

O servidor da CDN roda Linux e diferencia maiúsculas de minúsculas. `img/Logo.png` e `img/logo.png` são dois arquivos distintos para ele — mas o mesmo arquivo para o Windows e para o macOS com formatação padrão. Resultado: imagem que aparece na sua máquina e some no ar, sem erro nenhum além de um 404 no console.

Padronize tudo em minúsculas, sem acento e sem espaço: `img/logo-semana-academica.png`. Para corrigir um arquivo já versionado em um sistema que ignora maiúsculas, o Git precisa de dois passos, senão ele não percebe a mudança:

```bash
git mv img/Logo.png img/temporario.png
git mv img/temporario.png img/logo.png
git commit -m "Padroniza o nome do logo em minusculas"
```

## 4. Favicon: o 404 que o Capítulo 01 deixou pendente

### 4.1 Por que ele dá 404 sozinho

Todo navegador, ao abrir qualquer página, pede automaticamente `/favicon.ico` **na raiz do domínio** — mesmo que você nunca tenha escrito uma linha sobre isso. No Live Server, isso vira um 404 inofensivo no console. No GitHub Pages de projeto, é pior: o pedido vai para `https://ana-souza.github.io/favicon.ico` — a raiz do domínio, que pertence ao **site de usuário**, e não ao seu repositório de projeto. Colocar o `favicon.ico` na raiz do repositório não faz o navegador encontrá-lo sozinho nesse caso.

A solução é declarar o ícone explicitamente com `<link rel="icon">`, usando caminho relativo. Aí o navegador para de adivinhar.

### 4.2 O conjunto que resolve na prática

Três arquivos cobrem tudo o que importa hoje: um `.ico` de 32×32 para navegadores antigos e para a aba, um SVG que escala em qualquer tamanho, e um PNG de 180×180 para o ícone de tela inicial do iOS.

`index.html` (dentro do `<head>`, nas cinco páginas)

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Semana Acadêmica de Sistemas de Informação — UNEMAT Sinop</title>

  <!-- Ícone clássico, para a aba e para navegadores antigos -->
  <link rel="icon" href="favicon.ico" sizes="32x32">
  <!-- Ícone vetorial: escala perfeito em qualquer densidade de tela -->
  <link rel="icon" href="img/favicon.svg" type="image/svg+xml">
  <!-- Ícone do atalho na tela inicial do iOS (180x180) -->
  <link rel="apple-touch-icon" href="img/apple-touch-icon.png">
  <!-- Metadados de aplicativo: nome curto, cores e ícones grandes -->
  <link rel="manifest" href="site.webmanifest">
  <meta name="theme-color" content="#0b3d2e">

  <link rel="stylesheet" href="css/estilo.css">
</head>
```

Repare que **nenhum caminho começa com barra**. É a regra da §3 aplicada aos ícones.

`site.webmanifest`

```json
{
  "name": "Semana Acadêmica de Sistemas de Informação — UNEMAT Sinop",
  "short_name": "Semana Acadêmica",
  "start_url": "./",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#0b3d2e",
  "icons": [
    { "src": "img/icone-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "img/icone-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
```

Os caminhos dentro do manifesto são resolvidos **em relação ao próprio manifesto**, e não à página. Como o `site.webmanifest` está na raiz do site, `img/icone-192.png` funciona; `start_url: "./"` mantém o atalho apontando para o subcaminho certo.

### 4.3 Fazendo os arquivos

Comece por um SVG quadrado simples — ícone bom é ícone que se reconhece a 16 pixels. Um monograma resolve:

`img/favicon.svg`

```html
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="Semana Academica">
  <rect width="64" height="64" rx="12" fill="#0b3d2e"/>
  <text x="32" y="43" font-family="system-ui, sans-serif" font-size="34"
        font-weight="700" fill="#ffffff" text-anchor="middle">SA</text>
</svg>
```

Para gerar os PNG e o `.ico` a partir de uma imagem quadrada de pelo menos 512 pixels, o ImageMagick resolve em três linhas (Ubuntu: `sudo apt install imagemagick`):

```bash
magick img/logo-512.png -resize 192x192 img/icone-192.png
magick img/logo-512.png -resize 180x180 img/apple-touch-icon.png
magick img/logo-512.png -resize 32x32 favicon.ico
```

Sem ImageMagick, o <https://realfavicongenerator.net> faz o mesmo pelo navegador e entrega um `.zip` com todos os tamanhos e o trecho de HTML pronto.

> **🧠 Você sabia?**
> O `favicon.ico` é uma herança direta do Internet Explorer 5, de 1999. A Microsoft inventou o recurso para mostrar um ícone quando o usuário adicionava a página aos *favoritos* — daí o nome, *favorite icon*. O formato `.ico` é da própria Microsoft e guarda **várias resoluções dentro do mesmo arquivo**. A convenção de pedir `/favicon.ico` automaticamente pegou tão bem que, um quarto de século depois, todo navegador do planeta ainda faz esse pedido em toda página que abre — inclusive na sua.

## 5. A página 404

Quando alguém digita errado ou clica em um link velho, o servidor devolve o código `404 Not Found` e uma página feia e genérica. Você pode substituí-la por uma sua: basta um arquivo `404.html` na raiz do site publicado. GitHub Pages, Netlify, Vercel e Cloudflare Pages usam esse arquivo automaticamente, sem configuração.

`404.html`

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Página não encontrada — Semana Acadêmica</title>
  <link rel="icon" href="/site-evento/favicon.ico" sizes="32x32">
  <link rel="stylesheet" href="/site-evento/css/estilo.css">
</head>
<body>
  <main class="erro">
    <h1>404 — esta página não existe</h1>
    <p>
      O endereço que você abriu não corresponde a nenhuma página do site da
      Semana Acadêmica. Talvez o link esteja desatualizado.
    </p>
    <ul>
      <li><a href="/site-evento/">Ir para a página inicial</a></li>
      <li><a href="/site-evento/programacao.html">Ver a programação</a></li>
      <li><a href="/site-evento/contato.html">Falar com a organização</a></li>
    </ul>
  </main>
</body>
</html>
```

**Aqui a regra da §3 se inverte, e por um bom motivo.** O `404.html` é servido em resposta a *qualquer* endereço inexistente: `/site-evento/programacao/dia-1/`, `/site-evento/a/b/c/d`. A profundidade é imprevisível, então caminho relativo ao documento resolveria para lugares diferentes a cada erro — e a página de erro apareceria sem CSS, o que é uma ironia difícil de justificar. Por isso, e **só** no `404.html`, use caminho relativo à raiz **incluindo o nome do repositório**: `/site-evento/css/estilo.css`.

Se um dia o site ganhar domínio próprio (Capítulo 04), ele passa a viver na raiz e esses caminhos viram `/css/estilo.css`. Deixe um comentário no arquivo lembrando disso.

> **💡 Dica**
> Aplicações de página única (o UniEventos do Nível 3, com `vue-router`) precisam que **toda** URL devolva o `index.html`, para o roteador do navegador decidir o que mostrar. Na Netlify, na Vercel e na Cloudflare Pages isso se declara em uma regra de reescrita (§6.3). O GitHub Pages não tem reescrita — o truque conhecido é publicar uma cópia do `index.html` com o nome `404.html`: o servidor devolve a cópia (com status 404, que os buscadores não gostam, mas o navegador ignora) e o roteador assume dali. Funciona; não é elegante.

## 6. Netlify

A Netlify resolve as mesmas necessidades do GitHub Pages com mais recursos: pré-visualização de cada pull request, redirecionamentos, cabeçalhos personalizados, formulários e funções. Para o Café Cerrado estático do Nível 2, ela é a escolha natural.

### 6.1 Arrastar e soltar: publicando em quarenta segundos

O caminho mais rápido do mundo para colocar um site no ar:

1. Abra <https://app.netlify.com/drop> (logado).
2. Arraste a **pasta** do site (não um `.zip`, não os arquivos soltos) para a área indicada.
3. Pronto. Em segundos você recebe uma URL como `https://elegant-pasteur-1a2b3c.netlify.app`.
4. Em **Site configuration → Site details → Change site name**, troque para `cafe-cerrado`. A URL vira `https://cafe-cerrado.netlify.app`.

Use isso para mostrar um trabalho para alguém em cinco minutos, e só. O problema é óbvio: publicar de novo exige arrastar de novo, não há histórico, e o que está no ar não tem relação com o que está no Git. É publicação descartável.

### 6.2 A partir do Git: o jeito que se usa de verdade

1. No painel, **Add new site → Import an existing project → Deploy with GitHub**. Autorize o acesso ao repositório `cafe-cerrado`.
2. A Netlify pergunta três coisas:
   - **Branch to deploy**: `main`.
   - **Build command**: vazio, para um site sem construção (HTML/CSS/JS puro). Para um projeto Vite, `npm run build`.
   - **Publish directory**: `.` para um site puro (a raiz do repositório); `dist` para um projeto Vite.
3. **Deploy site**. A Netlify clona o repositório, roda o build (se houver) e publica a pasta indicada.

A partir daí, **todo `git push` na `main` publica automaticamente**. E cada pull request aberto ganha um *Deploy Preview*: uma URL temporária com aquela versão do site, que a Netlify comenta no próprio PR. É a peça que faltava na revisão de código do Capítulo 02 — o revisor deixa de imaginar como ficou e clica para ver.

> **🧠 Você sabia?**
> Quem popularizou o nome **Jamstack** foi a Netlify, por volta de 2015: *JavaScript, APIs e Markup*. A ideia era dar nome a uma arquitetura em que o HTML é gerado antes (não a cada requisição), servido por CDN, e tudo que é dinâmico chega por chamadas a APIs feitas no navegador. É exatamente a arquitetura dos seus três projetos das trilhas quando ficam prontos: front estático publicado em CDN, conversando com uma API própria.

### 6.3 `netlify.toml`: a configuração versionada

Configuração feita por cliques no painel não vai para o Git, não é revisada em pull request e some quando o site é recriado. A alternativa é um arquivo na raiz do repositório:

`netlify.toml`

```toml
# Configuração do site Café Cerrado na Netlify.
# Este arquivo tem prioridade sobre o que estiver configurado no painel.

[build]
  # Pasta que vai ao ar. "." = a raiz do repositório (site sem etapa de build).
  publish = "."
  # Sem comando de build: o site é HTML/CSS/JS puro.
  command = ""

[build.environment]
  NODE_VERSION = "22"

# Endereço antigo, divulgado no primeiro cardápio impresso: redireciona de vez.
[[redirects]]
  from = "/menu.html"
  to = "/cardapio.html"
  status = 301
  force = true

# Cabeçalhos de segurança em todas as respostas.
[[headers]]
  for = "/*"
  [headers.values]
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"

# Imagens e fontes mudam pouco: cache longo (uma semana).
[[headers]]
  for = "/img/*"
  [headers.values]
    Cache-Control = "public, max-age=604800"
```

Três blocos que você vai reusar em quase todo projeto:

- **`[build]`** define o que é construído e o que é publicado. É o bloco que resolve o erro "Page Not Found" logo depois do primeiro deploy: quase sempre o `publish` aponta para a pasta errada.
- **`[[redirects]]`** cria redirecionamentos. Com `status = 200` em vez de `301`, o redirecionamento vira **reescrita**: a URL na barra continua a mesma e o conteúdo vem de outro arquivo. É assim que se serve uma SPA:

```toml
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

- **`[[headers]]`** adiciona cabeçalhos de resposta — segurança, cache, o que você precisar. Cada bloco casa com um padrão de caminho.

A Netlify também aceita os arquivos de texto `_redirects` e `_headers` na pasta publicada, com a mesma função e sintaxe mais enxuta (a Cloudflare Pages entende os mesmos dois arquivos). Prefira o `netlify.toml`: um arquivo só, comentado, e com o build junto.

### 6.4 A CLI da Netlify

Para quem prefere o terminal, ou para automatizar depois:

```bash
# Autentica pelo navegador (uma vez por máquina)
npx --yes netlify-cli login

# Liga a pasta atual a um site já existente na sua conta
npx --yes netlify-cli link

# Publicação de rascunho: gera uma URL temporária para conferir
npx --yes netlify-cli deploy --dir=.

# Publicação definitiva, no endereço oficial do site
npx --yes netlify-cli deploy --prod --dir=. --message "Cardapio com fotos novas"

# Estado do site ligado a esta pasta
npx --yes netlify-cli status
```

O `deploy` sem `--prod` é um recurso subestimado: ele publica uma **URL de rascunho** que você abre, confere e só então promove. É a versão em produção do "olha antes de mandar".

## 7. Vercel e Cloudflare Pages, em resumo

As quatro plataformas fazem a mesma coisa básica. As diferenças aparecem no que vem junto:

| Plataforma | Ponto forte | Quando escolher |
|---|---|---|
| GitHub Pages | Já está onde o código está; zero configuração | Sites simples e trabalhos da disciplina |
| Netlify | Redirecionamentos, cabeçalhos, previews de PR, formulários | Projeto de equipe, SPA, site com regras |
| Vercel | Melhor integração com Next.js; build muito rápido | Projeto React/Next |
| Cloudflare Pages | Rede enorme, banda sem limite declarado | Site com muito acesso ou muita imagem |

**Vercel.** Pelo painel: <https://vercel.com/new> → importar o repositório do GitHub → ela detecta o framework, sugere o comando de build e a pasta de saída → **Deploy**. Pelo terminal, na pasta do projeto:

```bash
npx --yes vercel login
npx --yes vercel          # publica uma URL de pré-visualização
npx --yes vercel --prod   # publica no endereço de produção
```

A configuração versionada é o `vercel.json`:

`vercel.json`

```json
{
  "cleanUrls": true,
  "redirects": [
    { "source": "/menu.html", "destination": "/cardapio.html", "permanent": true }
  ],
  "headers": [
    {
      "source": "/img/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=604800" }
      ]
    }
  ]
}
```

O `cleanUrls: true` faz `/cardapio` servir `cardapio.html`, sem a extensão na barra de endereço.

**Cloudflare Pages.** Pelo painel: **Workers & Pages → Create → Pages → Connect to Git**, escolher o repositório, informar comando de build e diretório de saída. Pelo terminal, com o `wrangler`:

```bash
npx --yes wrangler login
npx --yes wrangler pages deploy . --project-name=site-evento
```

Ela lê os mesmos arquivos `_redirects` e `_headers` da Netlify, o que torna a migração entre as duas quase indolor.

Para os trabalhos da disciplina, a recomendação é simples: **GitHub Pages para o `site-evento`** (é onde o código já está) e **Netlify para o `cafe-cerrado`** (você vai precisar de redirecionamento e de cabeçalhos). Publicar o mesmo site em mais de uma plataforma, para comparar de verdade, é um ótimo exercício — e é o desafio ⭐⭐.

## 8. Cache: por que o site velho insiste em aparecer

### 8.1 Quem guarda o quê

Você corrigiu o CSS, fez `git push`, a publicação ficou verde — e o site continua igual. Antes de duvidar da plataforma, saiba que há **quatro** camadas de cache entre o seu arquivo e o olho de quem visita:

```text
seu arquivo ─► CDN da plataforma ─► proxy do provedor ─► cache do navegador ─► tela
```

Cada camada guarda uma cópia pelo tempo que o cabeçalho `cache-control` autorizar. Leia esse cabeçalho com `curl`:

```bash
curl -I https://ana-souza.github.io/site-evento/
curl -I https://ana-souza.github.io/site-evento/css/estilo.css
```

Interessam quatro cabeçalhos da resposta:

| Cabeçalho | O que significa |
|---|---|
| `cache-control: max-age=600` | Pode guardar por 600 segundos sem perguntar de novo |
| `etag: "a1b2c3"` | Impressão digital do conteúdo; muda quando o arquivo muda |
| `age: 240` | A cópia que você recebeu está há 240 s no cache intermediário |
| `last-modified` | Data da última modificação do arquivo |

Com `etag`, o navegador faz uma requisição condicional na próxima visita: manda `If-None-Match` e recebe `304 Not Modified` (resposta vazia, rápida) se nada mudou. Com `max-age` ainda válido, ele nem pergunta.

### 8.2 Como forçar a versão nova

Na sua máquina, para conferir se a correção subiu:

| Ação | Como |
|---|---|
| Recarga forçada | <kbd>Ctrl</kbd>+<kbd>F5</kbd> (Windows/Linux) ou <kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>R</kbd> (macOS) |
| Limpar e recarregar | DevTools aberto → clique direito no botão de recarregar → *Empty cache and hard reload* |
| Desligar o cache durante o trabalho | DevTools → **Network** → marcar **Disable cache** (vale só com o DevTools aberto) |
| Testar como um visitante novo | Janela anônima |

Para os **visitantes**, nada disso serve: você não pode pedir a cada pessoa que aperte <kbd>Ctrl</kbd>+<kbd>F5</kbd>. A solução é mudar o **nome do arquivo** sempre que o conteúdo muda, para que o navegador seja obrigado a pedir de novo:

```html
<link rel="stylesheet" href="css/estilo.css?v=3">
```

Cada mudança relevante no CSS vira `?v=4`, `?v=5`. É rústico, mas funciona e é suficiente para um site escrito à mão. Ferramentas de build fazem isso melhor, colocando um resumo do conteúdo no nome (`estilo-8f3a91c2.css`): mudou um byte, muda o nome, o cache antigo fica órfão e ninguém precisa lembrar de nada.

A partir daí vale a regra de ouro do cache:

- **HTML**: cache curto ou nenhum, porque é ele que aponta para os outros arquivos.
- **CSS, JS e imagens com nome versionado**: cache longo (`max-age=31536000, immutable`), porque o nome garante que o conteúdo nunca muda.

> **🔎 Por baixo do capô**
> `304 Not Modified` é a resposta mais barata do HTTP: o servidor manda só cabeçalhos, sem corpo. O navegador guardou o `etag` da visita anterior, reenvia em `If-None-Match`, e o servidor compara. Se bate, `304` e o navegador reaproveita a cópia local. Isso significa que existem **duas** economias distintas: com `max-age` válido não há requisição nenhuma (economia de tempo e de banda); com `max-age` vencido mas `etag` igual há requisição, mas sem download (economia só de banda). Na aba **Network**, a coluna **Size** mostra `(disk cache)` no primeiro caso e `304` no segundo.

## 9. Medindo o site publicado com o Lighthouse

Site no ar não é site pronto. O Lighthouse abre a sua página em condições controladas (rede e processador simulados de celular médio) e devolve nota de 0 a 100 em quatro categorias: **Performance**, **Acessibilidade**, **Práticas recomendadas** e **SEO**.

Pelo navegador: DevTools → aba **Lighthouse** → modo **Navigation**, dispositivo **Mobile**, marcar as quatro categorias → **Analyze page load**. Faça isso em uma **janela anônima**: extensões do navegador injetam scripts e derrubam a nota sem culpa do seu site.

Pelo terminal, o que é útil quando você quer guardar o relatório no repositório:

```bash
npx --yes lighthouse https://ana-souza.github.io/site-evento/ \
  --output html --output-path ./relatorio-antes.html --view
```

O `--view` abre o relatório no navegador ao terminar. Para simular desktop em vez de celular, acrescente `--preset=desktop`. Uma terceira via, sem instalar nada, é o <https://pagespeed.web.dev>: ele roda o mesmo Lighthouse nos servidores do Google.

As correções que mais rendem em um site estático de disciplina, em ordem de retorno:

| Problema apontado | Correção |
|---|---|
| `Image elements do not have explicit width and height` | Declare `width` e `height` no `<img>` (evita o layout pular) |
| `Serve images in next-gen formats` / imagens enormes | Redimensione para o tamanho real de exibição e exporte em WebP |
| `Background and foreground colors do not have a sufficient contrast ratio` | Ajuste as cores para contraste mínimo de 4,5:1 |
| `Image elements do not have [alt] attributes` | Escreva `alt` descritivo; `alt=""` só em imagem decorativa |
| `Document does not have a meta description` | Adicione `<meta name="description" content="…">` em cada página |
| `<html> element does not have a [lang] attribute` | `<html lang="pt-BR">` |
| `Links do not have a discernible name` | Link com só um ícone precisa de `aria-label` |

Anote as quatro notas **antes** de mexer em qualquer coisa. Sem o número inicial, "melhorou" é opinião.

## 🚀 Passo a passo — o site do evento no GitHub Pages e o Café Cerrado na Netlify

O que vai ao ar: o `site-evento` (Nível 1) em `https://<usuario>.github.io/site-evento/`, com favicon e página 404, e o `cafe-cerrado` (Nível 2) em `https://cafe-cerrado.netlify.app`, publicado a partir do Git com `netlify.toml`. Troque `ana-souza` pelo seu usuário do GitHub. Faça na ordem.

### Passo 1 — Confirme o ponto de partida

```bash
cd ~/weblab/site-evento
git status
gh repo view --json name,visibility,url
```

Resultado esperado: `nothing to commit, working tree clean`, visibilidade `PUBLIC` e a URL do repositório. Se `git status` listar arquivos pendentes, commite e dê push antes de continuar — o Pages publica o que está no GitHub, não o que está no seu disco.

### Passo 2 — Cace os caminhos que vão quebrar

```bash
grep -rn 'href="/\|src="/\|url(/' --include='*.html' --include='*.css' --include='*.js' .
```

Cada resultado é um caminho relativo à raiz do domínio. Troque todos por relativos ao documento: `/css/estilo.css` vira `css/estilo.css`, `/img/logo.png` vira `img/logo.png`. Confira também os nomes dos arquivos de imagem: tudo minúsculo, sem acento e sem espaço (§3.5).

```bash
ls -1 img/
git add -A
git commit -m "Troca caminhos absolutos por relativos para publicar em subcaminho"
```

### Passo 3 — Favicon, manifesto e 404

Crie `img/favicon.svg`, `favicon.ico`, `img/apple-touch-icon.png`, `img/icone-192.png` e `img/icone-512.png` com os comandos da §4.3 (ou pelo gerador online). Depois:

1. Cole o bloco de `<link rel="icon">` da §4.2 no `<head>` das **cinco** páginas.
2. Crie o `site.webmanifest` da §4.2 na raiz.
3. Crie o `404.html` da §5, com os caminhos começando em `/site-evento/`.
4. Crie o arquivo que desliga o Jekyll:

```bash
touch .nojekyll
git add -A
git commit -m "Adiciona favicon, manifesto, pagina 404 e .nojekyll"
git push
```

### Passo 4 — Ligue o GitHub Pages

Pelo painel: **Settings → Pages → Source: Deploy from a branch → Branch: `main` / `(root)` → Save**.

Ou, sem sair do terminal:

```bash
gh api --method POST repos/{owner}/{repo}/pages \
  -f "source[branch]=main" \
  -f "source[path]=/"
```

Acompanhe a publicação:

```bash
gh api repos/{owner}/{repo}/pages --jq '{status: .status, url: .html_url}'
```

Repita até `status` virar `built`. Costuma levar menos de um minuto na primeira vez.

### Passo 5 — Confira o que foi publicado

```bash
curl -I https://ana-souza.github.io/site-evento/
curl -I https://ana-souza.github.io/site-evento/css/estilo.css
curl -I https://ana-souza.github.io/site-evento/pagina-inexistente
```

Resultado esperado: `HTTP/2 200` com `server: GitHub.com` nas duas primeiras e `HTTP/2 404` na terceira, com `content-type: text/html`. Depois abra a URL no navegador **em janela anônima**, com o DevTools na aba **Network**: nenhuma linha em vermelho, e a linha do `favicon.ico` com status 200 apontando para `/site-evento/favicon.ico`.

### Passo 6 — Conserte o que ainda estiver 404

Se aparecer linha vermelha, clique nela e leia a **Request URL** completa. Praticamente sempre é uma destas três causas: caminho com barra inicial que escapou do `grep` (§3.2), nome de arquivo com maiúscula (§3.5) ou arquivo que não foi commitado. Corrija, `git push` e recarregue com <kbd>Ctrl</kbd>+<kbd>F5</kbd>.

### Passo 7 — Café Cerrado na Netlify, versão descartável

Abra <https://app.netlify.com/drop> e arraste a pasta `cafe-cerrado` inteira. Anote a URL sorteada e abra o site. Isso leva menos de um minuto e serve para você **ver a diferença** para o passo seguinte — não é a forma que você vai usar no semestre.

### Passo 8 — Café Cerrado na Netlify, a partir do Git

Primeiro, o arquivo de configuração no repositório:

`cafe-cerrado/netlify.toml`

```toml
[build]
  publish = "."
  command = ""

[build.environment]
  NODE_VERSION = "22"

[[headers]]
  for = "/*"
  [headers.values]
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"

[[headers]]
  for = "/img/*"
  [headers.values]
    Cache-Control = "public, max-age=604800"
```

```bash
cd ~/weblab/cafe-cerrado
git add netlify.toml
git commit -m "Configura publicacao e cabecalhos na Netlify"
git push
```

No painel da Netlify: **Add new site → Import an existing project → Deploy with GitHub → `cafe-cerrado` → Deploy**. Como o `netlify.toml` já define `publish` e `command`, aceite o que o formulário sugerir. Quando terminar, vá em **Site configuration → Site details → Change site name** e troque para `cafe-cerrado`.

Agora prove que o deploy contínuo funciona: mude uma linha visível do site (o título do cardápio, por exemplo), commite, dê push e acompanhe em **Deploys** no painel. A nova versão sobe sozinha.

### Passo 9 — Meça os dois

```bash
npx --yes lighthouse https://ana-souza.github.io/site-evento/ \
  --output html --output-path ./relatorio-site-evento.html --view

npx --yes lighthouse https://cafe-cerrado.netlify.app/ \
  --output html --output-path ./relatorio-cafe-cerrado.html --view
```

Anote as quatro notas de cada um em um arquivo `medicoes.md` e escolha **três** correções da tabela da §9 para aplicar hoje.

### Como conferir

```bash
curl -I https://ana-souza.github.io/site-evento/
curl -s https://ana-souza.github.io/site-evento/ | grep -c 'rel="icon"'
curl -I https://cafe-cerrado.netlify.app/img/xicara.png | grep -i cache-control
curl -I https://cafe-cerrado.netlify.app/pagina-inexistente
```

Resultado esperado:

- o primeiro `curl` devolve `HTTP/2 200` com `server: GitHub.com`;
- o `grep -c` conta **2** (o `.ico` e o SVG) — se contar 0, o `<link rel="icon">` não subiu;
- o terceiro mostra `cache-control: public, max-age=604800`, provando que o `netlify.toml` está valendo;
- o quarto devolve `404`, servindo a sua página de erro;
- nos dois sites, o DevTools em janela anônima não mostra nenhuma requisição em vermelho, e o ícone aparece na aba do navegador.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** A página `https://ana-souza.github.io/site-evento/palestrantes.html` contém `<img src="../img/foto.png">`. Escreva a URL exata que o navegador vai pedir. Ela existe? Qual seria a forma correta?

**A2.** Um repositório se chama `portfolio` e pertence ao usuário `joao-silva`. Qual é a URL do site de projeto? E se ele renomear o repositório para `joao-silva.github.io`, qual passa a ser a URL?

**A3.** Preveja antes de rodar: em `curl -I` de um CSS recém-publicado no GitHub Pages, quais destes cabeçalhos você espera encontrar — `cache-control`, `etag`, `content-type`, `set-cookie`? Rode e confirme. Por que um deles não faz sentido em hospedagem estática?

**A4.** Explique em duas linhas por que colocar `favicon.ico` na raiz do repositório **não** basta em um site de projeto do GitHub Pages, mas basta em um site de usuário.

**A5.** Complete o `netlify.toml` para um projeto Vite cujo `index.html` gerado vai para `dist/`: qual é o `publish`, qual é o `command` e qual bloco você acrescenta para que uma SPA responda em qualquer rota?

**A6.** Verdadeiro ou falso, justificando: "trocar `estilo.css` por `estilo.css?v=2` no HTML faz o servidor mandar um arquivo diferente". O que exatamente muda?

### Nível B — Aplicação

**B1.** Quebre e conserte. No `site-evento` já publicado, crie a branch `teste-caminhos`, troque **todos** os `href`/`src` do `index.html` para a forma com barra inicial, commite e publique essa branch no Pages (mude o *Branch* em Settings → Pages). Documente o estrago e desfaça.

Resultado esperado: um arquivo `caminhos.md` com uma captura da aba Network mostrando os 404, a **Request URL** de dois recursos quebrados, a explicação de por que na sua máquina funcionava, e o `git revert` do commit que quebrou.

<details><summary>Dica</summary>

Publique a branch de teste, confira, e devolva o *Branch* para `main` antes de sair. `git revert <hash>` desfaz criando um commit novo — mais honesto que apagar a branch e fingir que nada aconteceu.
</details>

**B2.** Página 404 que se defende. Escreva um `404.html` para o seu projeto autoral que funcione em qualquer profundidade de URL e que ofereça ajuda de verdade: os três destinos mais prováveis e um campo de busca que leve para a página inicial com o termo na query string.

Resultado esperado: abrir `https://<seu-site>/a/b/c/d` mostra a sua página com CSS aplicado, e `curl -I` na mesma URL devolve `404`. A página passa no Lighthouse em Acessibilidade com nota igual ou maior que a da home.

<details><summary>Dica</summary>

Os caminhos do `404.html` precisam começar com `/` mais o nome do repositório (§5). O campo de busca pode ser um `<form action="/<repo>/index.html" method="get">` com um `<input name="q">` e um `<label>` associado.
</details>

**B3.** O mesmo site, duas plataformas. Publique o `site-evento` também na Netlify a partir do Git, sem desligar o GitHub Pages, e compare as duas hospedagens.

Resultado esperado: uma tabela em `comparacao.md` com quatro linhas (URL, `server`, `cache-control` do HTML, nota de Performance no Lighthouse) e as duas colunas de plataforma, mais um parágrafo dizendo qual você escolheria para o seu projeto autoral e por quê.

<details><summary>Dica</summary>

`curl -sI <url> | grep -iE 'server|cache-control'` dá as duas primeiras linhas de uma vez. Rode o Lighthouse nas duas URLs na mesma sessão, em janela anônima, para a comparação valer.
</details>

### Nível C — Desafio

**C1.** Publicação sem cliques. Escreva um script `publicar.sh` que, rodado dentro de qualquer pasta de site estático não versionada, deixe o site no ar em uma URL do GitHub Pages: cria `.nojekyll` e `.gitignore` se não existirem, roda `git init` e o primeiro commit, cria o repositório remoto com `gh repo create`, faz push, liga o Pages via `gh api`, espera o `status` virar `built` consultando a API em laço, e imprime a URL final. Rodar o script duas vezes na mesma pasta não pode dar erro nem duplicar nada.

<details><summary>Dica</summary>

`gh repo view >/dev/null 2>&1` diz se já existe repositório remoto. Para o laço de espera, `until [ "$(gh api repos/{owner}/{repo}/pages --jq .status)" = "built" ]; do sleep 5; done`, com um contador para desistir depois de vinte tentativas. A URL final sai de `gh api repos/{owner}/{repo}/pages --jq .html_url`.
</details>

## 🏆 Desafios

### ⭐ A autópsia do site quebrado
Tags: deploy, github, investigacao

Todo semestre alguém publica o site e recebe de volta uma página de texto sem estilo, sem imagem e sem menu — e conclui que "o GitHub Pages não funciona". Ele funciona. O que não funciona é um caminho que começa com barra. Hoje você faz a autópsia desse caso e escreve o laudo que vai economizar horas dos seus colegas.

**Critérios de pronto**

- Um repositório público `autopsia-caminhos` com duas páginas idênticas no visual: `com-barra.html` (todos os `href`/`src` relativos à raiz) e `sem-barra.html` (todos relativos ao documento), compartilhando o mesmo `css/estilo.css` e a mesma imagem.
- O site publicado no GitHub Pages, em subcaminho, com as duas páginas acessíveis.
- Um `laudo.md` com: a URL de cada página; a **Request URL** completa de três recursos, para cada versão, copiada da aba Network; a explicação de por que as duas se comportam igual no Live Server e diferente no ar.
- Uma tabela de três colunas relacionando o que está escrito no HTML, para onde resolve no Live Server e para onde resolve no Pages.
- Um parágrafo final respondendo: em que situação um caminho relativo à raiz é a escolha **certa**?

<details><summary>Pistas</summary>

1. Reveja a §3.2 e a §5 antes de responder à última pergunta — o `404.html` é a exceção, e entender por quê vale mais que a tabela inteira.
2. No DevTools → Network, clique em uma linha e leia **Headers → Request URL**; é ela que você precisa colar, não o que está escrito no HTML.
3. Para as duas páginas ficarem realmente idênticas, escreva uma e copie, trocando só os caminhos com um `sed 's|="|="/repo/|g'` conferido à mão.
4. Um site de usuário (`usuario.github.io`) vive na raiz do domínio: lá, as duas versões funcionam. Explique isso no laudo — é a razão de tanta gente jurar que "sempre funcionou".
</details>

**Para ir além:** publique o mesmo repositório na Netlify e mostre que o comportamento muda, porque lá o site fica na raiz do subdomínio.

### ⭐⭐ Quatro hospedagens, um site, um veredicto
Tags: deploy, performance, http

As quatro plataformas deste capítulo prometem a mesma coisa: seu site no ar, de graça, em uma CDN. Elas entregam a mesma coisa? Descubra medindo, e não lendo página de marketing. O mesmo site, publicado quatro vezes, medido do mesmo jeito, no mesmo dia.

**Critérios de pronto**

- O seu projeto autoral (ou o `site-evento`) publicado nas quatro: GitHub Pages, Netlify, Vercel e Cloudflare Pages, a partir do mesmo repositório e do mesmo commit.
- Um `benchmark.md` com uma tabela de quatro colunas comparando, para cada plataforma: tempo total de resposta do HTML, cabeçalho `cache-control` do HTML e cabeçalho `cache-control` de uma imagem.
- Uma segunda tabela com as quatro notas do Lighthouse em cada plataforma, todas medidas em janela anônima, com o mesmo dispositivo simulado.
- Três medições de cada tempo, com a mediana registrada — uma medição só não é medição.
- Um veredicto de dez linhas: qual você escolheria para um site de portfólio, qual para um site com muitas imagens, qual para um trabalho de disciplina, e o que te faria mudar de ideia.
- Uma seção "o que eu não consegui medir" listando pelo menos duas diferenças relevantes que os seus testes não capturam.

<details><summary>Pistas</summary>

1. `curl -o /dev/null -s -w 'total: %{time_total}s conexao: %{time_connect}s\n' <url>` mede tempo sem baixar nada para a tela.
2. Publique nas quatro a partir do mesmo commit; se uma delas construir o site e outra não, a comparação já nasce torta.
3. Rode as medições em sequência, no mesmo minuto: a sua conexão varia mais ao longo do dia do que as plataformas entre si.
4. Entre as coisas que você não mede daí: latência a partir de outros países, comportamento sob pico de acesso, e o que acontece quando a plataforma cobra. Cite as fontes que você consultou para essas.
</details>

### ⭐⭐⭐ De 60 a 95 no Lighthouse, com prova
Tags: performance, deploy, devtools

Nota de Lighthouse é fácil de melhorar quando você sabe o que ela mede — e impossível quando você chuta. O trabalho aqui é científico: medir, mudar **uma** coisa, medir de novo, registrar o efeito. No fim, você vai saber quanto cada técnica vale, em pontos, no seu próprio site.

**Critérios de pronto**

- Ponto de partida documentado: as quatro notas do Lighthouse do seu site publicado, relatório HTML salvo como `relatorio-00-inicial.html` no repositório.
- No mínimo **seis** otimizações aplicadas, cada uma em **um commit separado**, com mensagem descrevendo a técnica, e um relatório salvo após cada uma (`relatorio-01-…html` até `relatorio-06-…html`).
- Cobertura obrigatória de quatro frentes: imagens (dimensão real e formato), fontes (`font-display` e quantidade de pesos), cabeçalhos de cache (via `netlify.toml` ou equivalente) e acessibilidade (contraste, `alt`, `lang`, rótulos de formulário).
- Um `otimizacoes.md` com uma tabela de quatro colunas: técnica, nota de Performance antes, nota depois, ganho em pontos — ordenada do maior ganho para o menor.
- Performance e Acessibilidade em **90 ou mais** no modo Mobile, medidos em janela anônima, com os relatórios finais no repositório.
- Um parágrafo honesto sobre pelo menos uma otimização que você tentou e que **não** mudou nada, com a hipótese do porquê.
- O peso total da página inicial (soma da coluna **Size** na aba Network, com o cache desligado) antes e depois, em KB.

<details><summary>Pistas</summary>

1. Comece pelas imagens: em quase todo site de disciplina elas são mais de 80% do peso. `magick foto.jpg -resize 1200x -quality 82 foto.webp` costuma cortar 90%.
2. `width` e `height` no `<img>` não mudam o peso, mas eliminam o deslocamento de layout — é a métrica CLS, e ela vale pontos.
3. Fonte do Google Fonts: cada peso extra é um arquivo. Dois pesos bastam. `font-display: swap` evita texto invisível enquanto a fonte carrega.
4. Cabeçalho de cache não muda a nota da primeira visita (o Lighthouse simula visitante novo) — esse é um bom candidato à "otimização que não mudou nada", e a explicação é o que vale.
5. Acessibilidade é a categoria com melhor retorno por minuto: contraste, `alt`, `lang="pt-BR"` e `<label>` costumam somar 20 pontos em meia hora.
6. Rode cada medição três vezes e use a mediana; a variação entre execuções chega a 5 pontos e pode inventar um ganho que não existe.
</details>

**Para ir além:** isso compõe bem o Marco de qualidade da sua trilha, se os relatórios estiverem no repositório e o histórico mostrar um commit por otimização.

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `404 There isn't a GitHub Pages site here.` na URL do projeto | A publicação ainda não terminou, ou o *Source* aponta para a branch errada | Aba **Actions** → veja *pages build and deployment*; confira `gh api repos/{owner}/{repo}/pages --jq .status` |
| Site abre, mas sem CSS, sem imagem e sem JS | Caminhos começando com `/` em um site de projeto (subcaminho) | Troque por relativos ao documento; rode o `grep` da §3.4 |
| Console: `Failed to load resource: the server responded with a status of 404 ()` em `/css/estilo.css` | O navegador pediu na raiz do domínio, não na pasta do repositório | Remova a barra inicial: `css/estilo.css` |
| A imagem aparece na sua máquina e some no ar | Nome com maiúscula ou acento: `img/Logo.PNG` × `img/logo.png` | Renomeie tudo em minúsculas com o `git mv` de dois passos da §3.5 |
| O Pages mostra o `README.md` renderizado em vez do site | Não existe `index.html` na pasta publicada | Confira o nome do arquivo e a pasta escolhida em *Source*; `index.html`, tudo minúsculo |
| Site Vite publicado sem estilo, com 404 em `/_assets/…` | O Jekyll ignorou a pasta iniciada por sublinhado | Crie o arquivo `.nojekyll` na raiz do site e publique de novo |
| Alterei, dei push, a publicação ficou verde e o site continua igual | Cache do navegador ou da CDN | <kbd>Ctrl</kbd>+<kbd>F5</kbd>, janela anônima, `curl -I` para ler `age` e `cache-control` |
| O favicon novo não aparece de jeito nenhum | Favicon é o recurso com cache mais teimoso do navegador | Abra a URL do ícone direto e recarregue forçado; ou publique com nome novo (`favicon-2.ico`) |
| Netlify: `Page Not Found` logo depois do primeiro deploy | `publish` apontando para pasta errada (raiz em vez de `dist`, ou o contrário) | Ajuste `[build] publish` no `netlify.toml` e refaça o deploy |
| Netlify: `Build script returned non-zero exit code: 2` | O comando de build falhou (dependência faltando, versão de Node diferente) | Leia o log completo em **Deploys**; fixe `NODE_VERSION` em `[build.environment]` |
| Links funcionam na home e quebram nas páginas de subpasta | Caminho relativo ao documento em profundidade diferente | `../` a mais, ou uma `<base href>` no `<head>` (§3.4) |
| Tudo certo, mas a URL sem barra final quebra o CSS | `…/site-evento` resolve os relativos como se estivesse na raiz | Divulgue sempre a URL com a barra final: `…/site-evento/` |

## 🏠 Para praticar depois da aula (1 h)

Publique o **seu projeto autoral** e deixe-o apresentável:

1. Garanta que o repositório está público e limpo (`git status` sem pendências) e que não há nenhum caminho com barra inicial fora do `404.html` — prove com a saída do `grep` da §3.4 colada no relatório.
2. Publique no GitHub Pages (ou na Netlify, se o projeto precisar de redirecionamentos) e anote a URL completa, com barra final.
3. Adicione favicon (`.ico` + SVG), `apple-touch-icon`, `site.webmanifest` e `404.html`, todos funcionando na URL publicada.
4. Rode o Lighthouse na URL pública e salve o relatório como `relatorio-lighthouse.html` no repositório.
5. Escreva no `README.md` uma seção **Site publicado** com: a URL clicável, a plataforma escolhida com uma linha de justificativa, e as quatro notas do Lighthouse.

**Critério de pronto:** a URL abre em janela anônima com todos os recursos carregando (nenhuma linha vermelha no DevTools), o ícone aparece na aba, um endereço inexistente devolve a sua página 404 com CSS aplicado, e o `README.md` do repositório mostra a URL e as notas.

**Guarde no seu repositório:** o link do repositório e a URL do site publicado. Nada de `.zip`.

## ✅ Está no ar quando…

- [ ] `https://<seu-usuario>.github.io/site-evento/` abre em janela anônima, com estilo, imagens e o menu funcionando.
- [ ] `curl -I https://<seu-usuario>.github.io/site-evento/` devolve `HTTP/2 200` com `server: GitHub.com`.
- [ ] O DevTools → **Network**, com o cache desligado, não mostra nenhuma requisição em vermelho — inclusive a do favicon.
- [ ] O ícone aparece na aba do navegador e no atalho de tela inicial do celular.
- [ ] `https://<seu-usuario>.github.io/site-evento/nao-existe` mostra a **sua** página 404, com CSS, e `curl -I` confirma o status `404`.
- [ ] O arquivo `.nojekyll` está no repositório.
- [ ] `https://cafe-cerrado.netlify.app` abre, e `curl -I` em uma imagem mostra o `cache-control` definido no `netlify.toml`.
- [ ] Um `git push` na `main` do `cafe-cerrado` publica a mudança sozinho, sem nenhum clique.
- [ ] Você tem, salvos no repositório, os relatórios do Lighthouse dos dois sites, e sabe dizer as quatro notas de cada um.
- [ ] Você explica, sem consultar, para onde `/css/estilo.css` resolve em `https://usuario.github.io/site-evento/programacao.html`, e por que na sua máquina isso funcionava.

## 📚 Para aprofundar

- GitHub Docs, "GitHub Pages" — <https://docs.github.com/pt/pages> — comece por "Criando um site do GitHub Pages" e "Configurando uma fonte de publicação"; é a referência oficial de tudo na §2.
- GitHub REST API, "Pages" — <https://docs.github.com/pt/rest/pages> — os endpoints usados com `gh api` na §2.3, com todos os campos da resposta.
- Netlify Docs — <https://docs.netlify.com> — leia "Get started", "File-based configuration" (o `netlify.toml` da §6.3) e "Redirects and rewrites".
- Netlify CLI — <https://cli.netlify.com> — todos os comandos, incluindo o `deploy` de rascunho da §6.4.
- Vercel Docs, "Projects" e "Configuring projects with vercel.json" — <https://vercel.com/docs> — o equivalente da Vercel ao `netlify.toml`.
- Cloudflare Pages — <https://developers.cloudflare.com/pages/> — a seção "Get started" e a de `_headers`/`_redirects`.
- MDN, "Escolhendo entre URLs absolutas e relativas" — <https://developer.mozilla.org/pt-BR/docs/Learn/Common_questions/Web_mechanics/What_is_a_URL> — a anatomia de uma URL, base de toda a §3.
- MDN, "`<base>`" — <https://developer.mozilla.org/pt-BR/docs/Web/HTML/Element/base> — e "`<link rel="icon">`" — <https://developer.mozilla.org/pt-BR/docs/Web/HTML/Attributes/rel> — as duas tags da §3.4 e da §4.2.
- MDN, "Cache-Control" — <https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Headers/Cache-Control> — e "HTTP caching" — a base da §8.
- web.dev, "Lighthouse" — <https://developer.chrome.com/docs/lighthouse/> — o que cada categoria mede e como interpretar cada auditoria da §9.
- PageSpeed Insights — <https://pagespeed.web.dev> — o Lighthouse rodando nos servidores do Google, com dados de campo quando o site tem visitantes.
- MILETTO, Evandro M.; BERTAGNOLLI, Silvia C. *Desenvolvimento de software II*. Bookman — capítulo sobre publicação e implantação de aplicações web.

No próximo capítulo, o endereço deixa de ser sorteado pela plataforma: você registra um domínio, entende como um nome vira um IP, aponta `evento.seudominio.dev` para este mesmo site e coloca o cadeado do HTTPS na barra de endereço.
