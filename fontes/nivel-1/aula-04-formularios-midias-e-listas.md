# Aula 04 — Formulários, mídias e listas

> **Nível 1 — Introdução ao Desenvolvimento Web** · Unidade 1: Arquitetura da Web e HTML
> WebLab · UNEMAT Sinop · Prof. Ivan Luiz Pedroso Pires
> **Carga:** 3 aulas de 50 min (presencial) + 1 h (assíncrona)

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Completar um formulário com campos avançados (`<output>`, `<progress>`, `<meter>`, upload múltiplo, `inputmode`, atributos `form` e `formaction`) e justificar a escolha de cada um.
- Aplicar listas ordenadas, não ordenadas e de definição para organizar conteúdo — e explicar por que um menu de navegação é uma lista.
- Inserir imagens com `alt` adequado a cada situação (informativa, decorativa, dentro de link, logotipo) e escolher o formato de arquivo certo.
- Usar `<figure>`, `<figcaption>`, `srcset`, `sizes` e `<picture>` para imagens responsivas e com formatos modernos.
- Incorporar áudio, vídeo (com legendas em WebVTT) e conteúdo externo em `<iframe>` de forma acessível e segura.
- Medir o peso de uma página na aba Network do DevTools e reduzi-lo otimizando as mídias.

## 📋 Pré-requisitos

- [ ] VS Code com a extensão Live Server e o navegador com DevTools (<kbd>F12</kbd>) funcionando.
- [ ] A pasta do projeto do evento com as **cinco** páginas validadas no W3C: `index.html`, `programacao.html`, `palestrantes.html` (Aula 02), `inscricao.html` com o formulário (Aula 03) e `contato.html` (esqueleto da Aula 02).
- [ ] Três fotos suas (ou livres de direitos) e um vídeo curto em `.mp4` — usaremos para medir peso de página. Se não tiver, baixe amostras do Unsplash ou do Pexels.

> Na Aula 03 você construiu a página de inscrição da Semana Acadêmica de Sistemas de Informação: `<form>`, tipos de `<input>`, `<label>`, `<select>`, `<datalist>`, `<fieldset>` e validação nativa. Hoje você fecha o capítulo de formulários com os campos que faltavam e passa para o que dá vida a uma página: listas bem estruturadas, imagens que carregam rápido, vídeo com legenda e conteúdo externo incorporado. Ao final, as cinco páginas do site do evento — todas já existentes — ganham logo, banner responsivo, listas de dois níveis, vídeo legendado, áudio, mapa e os campos de formulário que faltavam.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Formulários: campos avançados, `<output>`, `<meter>`, upload; listas `ul`, `ol`, `dl`, aninhamento e menus |
| 2 | 50 min | Imagens: `alt` por situação, formatos, `figure`, `srcset`/`sizes`, `<picture>`, `loading="lazy"` |
| 3 | 50 min | Áudio, vídeo, `<track>`, `<iframe>`; Mão na massa: ampliando as cinco páginas do evento; medição de peso no DevTools |

## 1. Formulários: fechando o ciclo

Na Aula 03 você viu os tipos de `<input>`, `<textarea>`, `<select>`, `<datalist>`, `<fieldset>` e a validação nativa. Faltam alguns elementos e atributos que aparecem em formulários reais — inscrição em evento, cadastro com anexo, pesquisa de satisfação — e que resolvem problemas específicos.

### 1.1 Upload de arquivos de verdade

Um campo `type="file"` só funciona de fato quando o formulário sabe empacotar bytes, não apenas texto. Isso é responsabilidade do atributo `enctype`:

**`inscricao.html` (trecho)**

```html
<form action="/inscrever" method="post" enctype="multipart/form-data">
  <fieldset>
    <legend>Comprovante de matrícula</legend>

    <label for="comprovante">Arquivo (PDF ou imagem, até 2 MB)</label>
    <input type="file" id="comprovante" name="comprovante"
           accept=".pdf,image/png,image/jpeg" required>

    <label for="certificados">Certificados anteriores (opcional, vários)</label>
    <input type="file" id="certificados" name="certificados"
           accept="application/pdf" multiple>
  </fieldset>

  <button type="submit">Enviar inscrição</button>
</form>
```

| Atributo | Efeito |
|---|---|
| `enctype="multipart/form-data"` | Sem ele, o navegador envia **só o nome** do arquivo, não o conteúdo |
| `accept` | Filtra o seletor de arquivos por extensão ou tipo MIME (`image/*` aceita qualquer imagem) |
| `multiple` | Permite selecionar vários arquivos; o `name` vira uma lista no servidor |
| `capture="environment"` | No celular, abre a câmera traseira direto em vez da galeria |

> **⚠️ Atenção**
> `accept` é conveniência, não segurança. O usuário pode trocar o filtro para "Todos os arquivos" e enviar o que quiser. Como toda validação no navegador, o servidor precisa checar tipo e tamanho de novo — esse lembrete vai se repetir até a última aula.

### 1.2 Mais de um valor em um campo só

`multiple` também vale para `type="email"`: o campo aceita vários endereços separados por vírgula e valida cada um.

```html
<label for="coautores">E-mails dos coautores (separe por vírgula)</label>
<input type="email" id="coautores" name="coautores" multiple
       placeholder="ana@exemplo.br, joao@exemplo.br">
```

### 1.3 `<output>`, `<progress>` e `<meter>` — mostrar, não coletar

Nem tudo dentro de um formulário é um campo de entrada. Três elementos existem para **exibir** valores com significado:

```html
<!-- <output>: resultado de um cálculo. O atributo for aponta os campos envolvidos -->
<label for="lote">Lote</label>
<select id="lote" name="lote">
  <option value="30">1º lote — R$ 30</option>
  <option value="45">2º lote — R$ 45</option>
</select>

<label for="qtd">Quantidade de ingressos</label>
<input type="number" id="qtd" name="qtd" min="1" max="5" value="1">

<p>Total: <output id="total" for="lote qtd">R$ 30</output></p>

<!-- <progress>: andamento de uma tarefa (etapa 2 de 4 da inscrição) -->
<label for="etapa">Andamento da inscrição</label>
<progress id="etapa" value="2" max="4">2 de 4</progress>

<!-- <meter>: medida dentro de uma faixa conhecida (vagas ocupadas) -->
<label for="vagas">Vagas ocupadas no minicurso de Git</label>
<meter id="vagas" value="38" min="0" max="40" low="20" high="35" optimum="0">38 de 40</meter>
```

| Elemento | Serve para | Não serve para |
|---|---|---|
| `<output>` | Resultado calculado a partir de outros campos (total, IMC, prazo) | Texto estático |
| `<progress>` | Quanto de uma tarefa já foi feito (upload, passo a passo) | Medida que pode subir e descer |
| `<meter>` | Valor escalar em uma faixa: espaço em disco, vagas, força da senha | Andamento de tarefa |

O texto entre as tags de `<progress>` e `<meter>` é o **fallback**: aparece em navegadores muito antigos e é o que um leitor de tela lê quando não consegue interpretar a barra. Sem JavaScript o `<output>` fica parado no valor inicial — na Aula 13 você o atualizará em tempo real.

### 1.4 Campos fora do `<form>` e botões que mudam o destino

Dois atributos pouco conhecidos resolvem layouts que parecem impossíveis:

```html
<form id="form-inscricao" action="/inscrever" method="post">
  <label for="nome">Nome completo</label>
  <input type="text" id="nome" name="nome" required>
</form>

<!-- Este campo está FORA do form no HTML, mas pertence a ele pelo atributo form -->
<label for="newsletter">Quero receber novidades do evento</label>
<input type="checkbox" id="newsletter" name="newsletter" form="form-inscricao">

<!-- Botões podem sobrescrever action, method e a validação do form -->
<button type="submit" form="form-inscricao">Enviar inscrição</button>
<button type="submit" form="form-inscricao"
        formaction="/rascunho" formnovalidate>Salvar rascunho</button>
```

- `form="id"` liga um campo ou botão a um formulário, mesmo estando em outra região da página (um botão fixo no rodapé, por exemplo).
- `formaction` e `formmethod` mudam o destino só daquele botão.
- `formnovalidate` envia sem passar pela validação nativa — útil para "salvar rascunho", em que campos obrigatórios ainda podem estar vazios.

### 1.5 `inputmode` — o teclado certo sem mudar o tipo

Na Aula 03 você viu que `type="tel"` abre o teclado numérico no celular. Mas e um campo de CPF, que precisa de `pattern` e é do tipo `text`? Use `inputmode`:

```html
<label for="cpf">CPF</label>
<input type="text" id="cpf" name="cpf" inputmode="numeric"
       pattern="[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}"
       placeholder="000.000.000-00" title="Formato: 000.000.000-00"
       autocomplete="off">
```

Valores úteis: `numeric` (só dígitos), `decimal` (dígitos e vírgula/ponto), `tel`, `email`, `url`, `search`. O `type` continua controlando a **validação**; o `inputmode` controla o **teclado**.

> **🔬 Investigue**
> Abra o DevTools, ative o modo dispositivo (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>M</kbd>) e escolha um celular. Crie três campos: `type="text"`, `type="text" inputmode="numeric"` e `type="number"`. Foque cada um. O emulador não mostra o teclado virtual, mas na aba Elements você verá que a validação de `type="number"` rejeita "12abc" e a de `type="text" inputmode="numeric"` aceita — a diferença entre **validar** e **sugerir teclado** fica visível. Se tiver um celular na mão, abra a página pelo IP do Live Server na mesma rede Wi-Fi e veja o teclado de verdade.

## 2. Listas

Uma lista é uma sequência de itens relacionados. Parece óbvio, mas o HTML oferece três tipos com semânticas diferentes, e escolher o certo muda como o leitor de tela anuncia o conteúdo ("lista com 5 itens") e como você o estilizará na Unidade 2.

### 2.1 Os três tipos

```html
<!-- Lista não ordenada: a ordem NÃO importa -->
<ul>
  <li>HTML</li>
  <li>CSS</li>
  <li>JavaScript</li>
</ul>

<!-- Lista ordenada: a ordem IMPORTA (passos, ranking, cronograma) -->
<ol>
  <li>Analisar a URL</li>
  <li>Resolver o DNS</li>
  <li>Abrir a conexão TCP</li>
  <li>Enviar a requisição HTTP</li>
</ol>

<!-- Lista de definições: pares termo → descrição (glossário, ficha técnica) -->
<dl>
  <dt>HTML</dt>
  <dd>Linguagem de marcação que estrutura o conteúdo.</dd>
  <dt>CSS</dt>
  <dd>Linguagem de estilo que define a apresentação.</dd>
  <dt>JavaScript</dt>
  <dd>Linguagem de programação que adiciona comportamento.</dd>
</dl>
```

| Elemento | Quando usar | Exemplo real |
|---|---|---|
| `<ul>` | Itens sem ordem significativa | Menu de navegação, lista de requisitos, tags |
| `<ol>` | A sequência carrega informação | Passo a passo, programação do dia, ranking |
| `<dl>` | Pares nome/valor | Glossário, ficha técnica de produto, perguntas e respostas |

Um `<dt>` pode ter vários `<dd>` (um termo com duas definições) e vários `<dt>` podem compartilhar um `<dd>` (sinônimos). Isso torna a `<dl>` a escolha certa para FAQ e para a ficha de um palestrante (Nome → valor, Instituição → valor, Tema → valor).

### 2.2 Atributos da lista ordenada

```html
<!-- Numeração romana, começando em 3, decrescente -->
<ol type="I" start="3" reversed>
  <li>Terceiro colocado</li>
  <li>Segundo colocado</li>
  <li>Campeão</li>
</ol>

<!-- Pular a numeração em um item -->
<ol>
  <li>Abertura</li>
  <li value="5">Encerramento (os itens 2 a 4 estão em outra página)</li>
</ol>
```

| Atributo | Valores | Uso |
|---|---|---|
| `type` | `1`, `a`, `A`, `i`, `I` | Tipo do marcador (numérico, alfabético, romano) |
| `start` | inteiro | Primeiro número da sequência |
| `reversed` | booleano | Conta para baixo (top 10, contagem regressiva) |
| `value` (no `<li>`) | inteiro | Força o número de um item específico |

Na Unidade 2 você verá que a **aparência** do marcador (bolinha, traço, ícone) é assunto de CSS (`list-style`). Os atributos acima mudam o **significado** — por isso ficam no HTML.

### 2.3 Listas aninhadas: o erro que o validador sempre pega

O `<ul>` filho vai **dentro** do `<li>` pai, nunca solto entre dois `<li>`:

```html
<!-- CERTO: o <ul> das sessões fica dentro do <li> da trilha -->
<ul>
  <li>Trilha Front-end
    <ul>
      <li>HTML semântico na prática</li>
      <li>CSS moderno sem framework</li>
    </ul>
  </li>
  <li>Trilha Back-end
    <ul>
      <li>APIs REST com Node</li>
      <li>Bancos de dados na nuvem</li>
    </ul>
  </li>
</ul>
```

```html
<!-- ERRADO: <ul> diretamente dentro de <ul>. O W3C acusa "Element ul not allowed as child of element ul" -->
<ul>
  <li>Trilha Front-end</li>
  <ul>
    <li>HTML semântico na prática</li>
  </ul>
</ul>
```

Os únicos filhos permitidos de `<ul>` e `<ol>` são `<li>` (e `<script>`/`<template>`, que não renderizam). Qualquer outra coisa — um `<p>`, um `<div>`, outro `<ul>` — precisa estar dentro de um `<li>`.

### 2.4 Por que um menu é uma lista

Um menu de navegação é um conjunto de links relacionados. Marcá-lo como `<ul>` dentro de `<nav>` entrega três coisas de graça:

1. O leitor de tela anuncia "navegação, lista com 5 itens" — o usuário sabe o tamanho do menu antes de percorrê-lo.
2. A estrutura se mantém mesmo sem CSS: os itens ficam um embaixo do outro, legíveis.
3. Na Aula 07 você transformará essa mesma lista em um menu horizontal só com CSS, sem tocar no HTML.

**`programacao.html` (trecho do cabeçalho)**

```html
<header id="topo">
  <img src="img/logo-sasi.svg" alt="" width="160" height="48">
  <h1>Semana Acadêmica de Sistemas de Informação</h1>
  <p>UNEMAT Sinop · três noites de outubro · Auditório Central</p>
  <nav aria-label="Principal">
    <ul>
      <li><a href="index.html">Início</a></li>
      <li><a href="programacao.html" aria-current="page">Programação</a></li>
      <li><a href="inscricao.html">Inscrição</a></li>
      <li><a href="palestrantes.html">Palestrantes</a></li>
      <li><a href="contato.html">Contato</a></li>
    </ul>
  </nav>
</header>
```

`aria-current="page"` marca o link da página atual — o leitor de tela anuncia "página atual" e, na Unidade 2, você o usará como gancho para destacar o item ativo.

> **🧠 Você sabia?**
> O Safari (e, com ele, o VoiceOver do iPhone) **remove a semântica de lista** quando o CSS aplica `list-style: none` a uma `<ul>` fora de `<nav>`. O leitor de tela deixa de anunciar "lista com 5 itens" e lê os links soltos. Foi uma decisão deliberada da Apple, porque muitos desenvolvedores usavam listas para tudo. A solução é justamente a que você aprendeu hoje: manter o menu dentro de `<nav>`, onde a semântica é preservada, ou acrescentar `role="list"` na `<ul>` quando a lista precisa ser anunciada e vive fora da navegação.

## 3. Imagens

Imagem é, disparado, o maior peso da maioria dos sites — e também a maior fonte de barreiras de acessibilidade. Uma `<img>` bem escrita resolve os dois problemas.

### 3.1 A `<img>` completa

```html
<img src="img/campus-sinop.jpg"
     alt="Vista aérea do campus da UNEMAT em Sinop ao entardecer"
     width="800" height="600"
     loading="lazy">
```

| Atributo | Função |
|---|---|
| `src` | Caminho da imagem (relativo à página, como nos links da Aula 02) |
| `alt` | Texto alternativo — **obrigatório** em toda `<img>` |
| `width` / `height` | Dimensões intrínsecas. O navegador reserva o espaço antes de baixar o arquivo e evita o "pulo" do layout |
| `loading="lazy"` | Só baixa quando a imagem estiver perto de entrar na tela. Ganho grande em páginas longas |
| `title` | Tooltip ao passar o mouse. **Não substitui** o `alt` |

Sobre `width` e `height`: declare sempre os valores reais do arquivo. Eles não impedem o CSS de redimensionar depois (você fará `max-width: 100%` na Aula 08); servem para o navegador calcular a **proporção** e reservar a área. Sem eles, o texto abaixo da imagem "pula" quando ela chega — o que o Google mede como *Cumulative Layout Shift* e penaliza no ranqueamento.

### 3.2 Escrevendo bons `alt`

O `alt` é o que uma pessoa cega ouve, o que aparece quando a imagem não carrega e o que o buscador indexa. A regra não é "descreva a imagem"; é "**entregue a mesma informação** que a imagem entrega para quem vê".

| Situação | Regra | Exemplo |
|---|---|---|
| Imagem informativa | Descreva a informação, não a aparência | `alt="Gráfico de barras: inscrições subiram de 120 na primeira edição para 180 na terceira"` |
| Imagem decorativa | `alt=""` (vazio, mas **presente**) — o leitor de tela pula | Linha divisória, textura de fundo |
| Imagem dentro de link | Descreva o **destino**, não a imagem | `alt="Página inicial da UNEMAT"` |
| Logotipo | O nome, sem a palavra "logo" | `alt="UNEMAT"` |

Nunca escreva `alt="imagem"`, `alt="foto.jpg"`, `alt="clique aqui"` ou omita o atributo. Sem `alt`, o leitor de tela lê o **nome do arquivo** — "DSC underline zero zero quatro dois ponto jpg".

Um teste simples: feche os olhos e peça para alguém ler só o `alt`. Se você entende o que a imagem comunica, está bom. Se ouve "foto bonita do campus", não está.

### 3.3 `<figure>` e `<figcaption>`

Quando a imagem tem uma **legenda visível** — figura numerada, crédito, explicação — envolva-a em `<figure>`:

```html
<figure>
  <img src="img/modelo-cliente-servidor.png"
       alt="Diagrama: o navegador envia uma requisição HTTP e o servidor devolve uma resposta"
       width="640" height="360">
  <figcaption>
    Figura 1 — Modelo cliente-servidor. Fonte: organização do evento.
  </figcaption>
</figure>
```

`alt` e `figcaption` não são redundantes: o `alt` é para quem **não vê** a imagem; a `figcaption` é a legenda **para todos**. Um leitor de tela lê os dois — por isso a legenda não deve repetir o `alt` palavra por palavra. `<figure>` também serve para trechos de código, tabelas, citações e vídeos com legenda — qualquer conteúdo autocontido ao qual o texto se refere.

### 3.4 Formatos de imagem

| Formato | Melhor para | Transparência | Observação |
|---|---|---|---|
| JPG | Fotografias | Não | Compressão com perdas; ajuste a qualidade (75–85 costuma bastar) |
| PNG | Logos, ícones, capturas de tela | Sim | Sem perdas; arquivos maiores em fotos |
| WebP | Substituto moderno de JPG e PNG | Sim | Cerca de 30% menor; suporte universal nos navegadores atuais |
| AVIF | Compressão máxima | Sim | Ainda menor que WebP; suporte amplo, com exceções em navegadores antigos |
| SVG | Logos, ícones, diagramas | Sim | Vetorial: escala sem perder qualidade; arquivo minúsculo; é texto (XML) |
| GIF | Animações simples | Sim (binária) | Obsoleto; prefira vídeo em MP4/WebM (10× menor) |

> **💡 Dica**
> Regra de otimização: nunca coloque na web uma foto de 4000×3000 px e 6 MB para exibi-la em um espaço de 400 px. Redimensione e comprima **antes** de subir — Squoosh (no navegador), TinyPNG ou GIMP. Um site de evento com dez fotos de celular sem tratamento pesa 40 MB; o mesmo site, tratado, pesa 1 MB. No 4G da zona rural de Sinop, isso é a diferença entre carregar em 2 segundos e em 1 minuto.

### 3.5 Imagens responsivas: `srcset` e `sizes`

Um celular de 360 px de largura não precisa baixar a mesma foto de 1600 px que o monitor do laboratório. Com `srcset` você oferece **a mesma imagem em vários tamanhos** e o navegador escolhe:

```html
<img src="img/banner-800.jpg"
     srcset="img/banner-400.jpg 400w,
             img/banner-800.jpg 800w,
             img/banner-1600.jpg 1600w"
     sizes="(max-width: 600px) 100vw, 50vw"
     alt="Banner da Semana Acadêmica de Sistemas de Informação"
     width="800" height="450">
```

Como o navegador decide:

1. Lê `sizes`: "se a janela tem até 600 px, a imagem ocupará 100% da largura (`100vw`); senão, 50%".
2. Calcula a largura em pixels que a imagem terá na tela, multiplicada pela densidade da tela (um celular com tela 2× precisa do dobro).
3. Escolhe em `srcset` o **menor arquivo** que ainda cobre essa largura. Os números com `w` são as larguras reais de cada arquivo.
4. O `src` continua sendo o fallback para navegadores que não entendem `srcset`.

> **⚠️ Atenção**
> `srcset` sem `sizes` faz o navegador supor que a imagem ocupa 100% da janela — e ele baixará o arquivo grande mesmo para uma miniatura. Os dois atributos andam juntos.

### 3.6 Formatos alternativos com `<picture>`

`srcset` resolve **tamanho**; `<picture>` resolve **formato** (e também troca de enquadramento entre telas, a chamada "direção de arte"):

```html
<picture>
  <source srcset="img/banner.avif" type="image/avif">
  <source srcset="img/banner.webp" type="image/webp">
  <img src="img/banner.jpg"
       alt="Banner da Semana Acadêmica de Sistemas de Informação"
       width="1600" height="900" loading="lazy">
</picture>
```

O navegador lê os `<source>` de cima para baixo e usa o **primeiro cujo `type` ele suporta**. O `<img>` final é obrigatório: é ele que carrega `alt`, `width`, `height`, `loading` — e serve de garantia para navegadores antigos. Os `<source>` também aceitam `srcset` com vários tamanhos e `sizes`, combinando as duas técnicas.

> **🔬 Investigue**
> Coloque o `<picture>` acima em uma página, abra o DevTools na aba **Network**, filtre por **Img** e recarregue. Qual arquivo foi baixado — `.avif`, `.webp` ou `.jpg`? Agora, na coluna **Type**, confira o tipo real. Depois teste uma `<img>` com `srcset` de três larguras: redimensione a janela de 400 px até 1400 px recarregando a cada vez e anote qual arquivo veio em cada largura. Marque a opção **Disable cache** antes, senão o navegador reaproveita o arquivo anterior e o experimento mente.

### 3.7 Prioridade de carregamento

Nem toda imagem deve ser `lazy`. A imagem principal do topo da página (o banner, o "herói") precisa chegar **primeiro**: ela é o que o usuário vê antes de qualquer rolagem e o que as ferramentas de performance medem como *Largest Contentful Paint*.

```html
<!-- Banner do topo: prioridade alta, sem lazy -->
<img src="img/banner-800.jpg" alt="Banner do evento" width="800" height="450"
     fetchpriority="high" decoding="async">

<!-- Fotos da galeria, abaixo da dobra: lazy -->
<img src="img/palestrante-01.jpg" alt="Ana Lúcia Ferreira" width="400" height="400"
     loading="lazy" decoding="async">
```

`decoding="async"` permite que o navegador decodifique a imagem sem travar o desenho do texto. Regra prática: **as duas ou três primeiras imagens visíveis sem rolar não levam `lazy`**; todas as outras levam.

## 4. Áudio e vídeo

Antes do HTML5, vídeo na web exigia o plugin Flash. Hoje `<audio>` e `<video>` são nativos, controláveis por teclado e legendáveis — desde que você use os atributos certos.

### 4.1 `<audio>`

```html
<audio controls preload="metadata">
  <source src="midia/depoimento.mp3" type="audio/mpeg">
  <source src="midia/depoimento.ogg" type="audio/ogg">
  Seu navegador não suporta áudio HTML5.
  <a href="midia/depoimento.mp3">Baixe o arquivo</a>.
</audio>
```

Assim como em `<picture>`, o navegador usa o primeiro `<source>` que consegue tocar. O texto e o link no final são o fallback — aparecem só onde o elemento não é suportado. MP3 é aceito em todo lugar; OGG é opcional.

### 4.2 `<video>`

```html
<video controls width="640" height="360"
       poster="img/capa-abertura.jpg" preload="metadata">
  <source src="midia/abertura.mp4" type="video/mp4">
  <source src="midia/abertura.webm" type="video/webm">
  <track src="legendas/abertura-pt.vtt" kind="captions"
         srclang="pt" label="Português" default>
  Seu navegador não suporta vídeo HTML5.
  <a href="midia/abertura.mp4">Baixe o vídeo</a>.
</video>
```

| Atributo | Efeito |
|---|---|
| `controls` | Exibe os controles nativos (play, volume, tempo, tela cheia, legendas) |
| `autoplay` | Inicia sozinho — os navegadores **bloqueiam** se houver som |
| `muted` | Sem som. Necessário para `autoplay` funcionar |
| `loop` | Repete indefinidamente |
| `poster` | Imagem exibida antes do play (a "capa") |
| `preload` | `none` (nada), `metadata` (só duração e dimensões), `auto` (o navegador decide) |
| `playsinline` | No iPhone, toca dentro da página em vez de abrir em tela cheia |

Sobre `preload`: o padrão de cada navegador varia, e `auto` pode baixar o vídeo inteiro mesmo que o usuário nunca aperte play. Para vídeos que não são o foco da página, `metadata` é a escolha segura. MP4 (H.264) toca em todos os navegadores; WebM é menor, mas opcional.

### 4.3 Legendas com `<track>` e WebVTT

Vídeo sem legenda é conteúdo inacessível para pessoas surdas — e, na prática, para qualquer pessoa no ônibus sem fone. Legenda não é extra: é requisito do critério 1.2.2 da WCAG e item da rubrica desta disciplina.

O `<track>` aponta para um arquivo **WebVTT**, um texto simples com marcações de tempo:

**`legendas/abertura-pt.vtt`**

```text
WEBVTT

00:00:00.000 --> 00:00:03.500
Bem-vindos à Semana Acadêmica de Sistemas de Informação.

00:00:04.000 --> 00:00:08.000
Nesta edição, teremos três dias de palestras, minicursos e maratona de programação.

00:00:08.500 --> 00:00:12.000
As inscrições estão abertas no site do evento.

00:00:12.500 --> 00:00:15.000
[música de abertura]
```

Regras do formato: a primeira linha é `WEBVTT`; cada bloco tem um intervalo `início --> fim` no formato `hh:mm:ss.mmm` (as horas podem ser omitidas) seguido do texto; blocos separados por uma linha em branco. Sons relevantes vão entre colchetes — é isso que diferencia *captions* (para quem não ouve) de *subtitles* (tradução).

| `kind` | Para que serve |
|---|---|
| `captions` | Legenda completa com falas **e** sons relevantes (acessibilidade) |
| `subtitles` | Tradução das falas (o usuário ouve, mas não entende o idioma) |
| `descriptions` | Descrição textual do que aparece na tela, para pessoas cegas |
| `chapters` | Marcadores de capítulo para navegar no vídeo |

Um `<video>` pode ter vários `<track>` — um por idioma ou por tipo. `default` marca o que liga sozinho. O Live Server serve arquivos `.vtt` sem configuração; em servidores próprios, o tipo MIME `text/vtt` precisa estar registrado (você verá isso na trilha Deploy).

> **🔎 Por baixo do capô**
> Por que os navegadores bloqueiam `autoplay` com som? Há alguns anos, Chrome e Safari adotaram políticas que só permitem reprodução automática **sem som** ou depois de uma interação do usuário com a página (clique, toque, tecla). O motivo foi o abuso de anúncios em vídeo que começavam a gritar assim que a página abria. Hoje, `autoplay` sem `muted` simplesmente não toca — e o console avisa: `play() failed because the user didn't interact with the document first`. Se a interface depende de vídeo de fundo, ele será silencioso.

## 5. `<iframe>` — conteúdo externo

Um `<iframe>` abre uma **outra página** dentro da sua: um vídeo do YouTube, um mapa, um formulário do Google, um widget de clima.

```html
<iframe src="https://www.youtube.com/embed/ID_DO_VIDEO"
        title="Vídeo: abertura da edição anterior da Semana Acadêmica"
        width="560" height="315"
        loading="lazy"
        allow="fullscreen; picture-in-picture"
        referrerpolicy="strict-origin-when-cross-origin">
</iframe>
```

| Atributo | Função |
|---|---|
| `src` | Endereço da página incorporada (use a URL de *embed* que o serviço fornece, não a do site) |
| `title` | **Obrigatório** para acessibilidade: é o que o leitor de tela anuncia ao entrar no quadro |
| `loading="lazy"` | Só carrega quando estiver perto da tela — iframes pesam mais que imagens |
| `allow` | Lista de permissões concedidas ao conteúdo (tela cheia, câmera, geolocalização) |
| `sandbox` | Restringe o que o conteúdo pode fazer (scripts, formulários, pop-ups); vazio = bloqueia tudo |

Mapa incorporado do Google Maps (o serviço gera este código em "Compartilhar → Incorporar um mapa"):

```html
<iframe src="https://www.google.com/maps/embed?pb=CODIGO_GERADO_PELO_MAPS"
        title="Mapa: localização do campus da UNEMAT em Sinop"
        width="600" height="450"
        loading="lazy"
        referrerpolicy="no-referrer-when-downgrade">
</iframe>
```

> **⚠️ Atenção**
> Um `<iframe>` executa **código de terceiros** dentro da sua página: ele pode rastrear o visitante, mostrar anúncios e, se o serviço for comprometido, servir conteúdo malicioso. Só incorpore fontes confiáveis. Para conteúdo que você não controla (um widget de fórum, por exemplo), use `sandbox="allow-scripts allow-same-origin"` e libere apenas o necessário. E nunca coloque um `<iframe>` de um site que você não tem permissão para incorporar: muitos enviam o cabeçalho `X-Frame-Options: DENY` e o quadro fica em branco — esse é um dos erros mais comuns da aula.

Também existem `<embed>` e `<object>`, dos tempos dos plugins. Hoje só têm um uso corrente: exibir um PDF dentro da página (`<object data="edital.pdf" type="application/pdf">`). Para todo o resto, `<iframe>`.

## 6. Medindo o peso da página

Tudo o que você aprendeu hoje tem um custo em bytes. A aba **Network** do DevTools mostra esse custo com precisão:

1. Abra o DevTools (<kbd>F12</kbd>) e vá à aba **Network**.
2. Marque **Disable cache** — senão a segunda visita esconde o peso real.
3. Recarregue a página (<kbd>Ctrl</kbd>+<kbd>R</kbd>).
4. Leia a barra de status no rodapé: **N requests · X MB transferred · Y MB resources · Z s**.
5. Clique no cabeçalho da coluna **Size** para ordenar: os maiores arquivos ficam no topo. Quase sempre são imagens ou vídeo.
6. No menu **Throttling** (ao lado de "Disable cache"), escolha **Slow 4G** e recarregue: é assim que metade dos seus usuários vê o site.

| Faixa de peso total | Avaliação |
|---|---|
| até 1 MB | Bom para uma página com fotos |
| 1 a 3 MB | Aceitável; procure a imagem mais pesada e otimize |
| acima de 3 MB | Problema. Alguém subiu foto de celular sem tratar |

A coluna **Size** mostra dois números: o de cima é o **transferido** (comprimido pela rede); o de baixo, o **tamanho real** do recurso. Para imagens e vídeo eles são quase iguais — esses formatos já são comprimidos e a rede não ganha nada extra. Para HTML e CSS, o transferido costuma ser 3 a 5× menor (compressão gzip/brotli do servidor).

Fluxo de otimização de uma imagem no **Squoosh** (squoosh.app, roda no navegador, sem instalar nada):

1. Arraste a foto original.
2. Em **Resize**, reduza para o dobro da largura em que ela será exibida (uma foto mostrada em 400 px sai com 800 px, para telas de alta densidade).
3. Em **Compress**, escolha **WebP** com qualidade 75 e compare visualmente com o original arrastando a linha divisória.
4. Repita em **AVIF** e **MozJPEG** para gerar os três formatos do `<picture>`.
5. Anote o peso antes e depois — você fará isso na Mão na massa.

## 💻 Mão na massa — Mídias, listas e campos avançados nas páginas do evento

As cinco páginas do site da **Semana Acadêmica de Sistemas de Informação** já existem: `index.html`, `programacao.html` e `palestrantes.html` nasceram na Aula 02, e `inscricao.html` recebeu o formulário completo na Aula 03. Hoje **nenhuma página é criada do zero** — você amplia o que já está lá.

> **⚠️ Atenção**
> Nada do que as Aulas 02 e 03 entregaram é jogado fora. O `<header id="topo">` com o `<h1>` do site, o `<h2>` que titula cada página, o rodapé de três parágrafos e a **tabela** da programação continuam exatamente onde estão. Todo o trabalho de hoje é *acrescentar* — se em algum passo você se pegar apagando conteúdo antigo, pare e releia o passo.

Ao final, a pasta do projeto ficará assim:

```text
site-evento/
├── index.html              ← ganha o banner responsivo
├── programacao.html        ← ganha trilhas, vídeo, áudio e mapa
├── inscricao.html          ← ganha os campos avançados da seção 1
├── palestrantes.html       ← ganha as fotos e o elenco completo
├── contato.html
├── img/
│   ├── logo-sasi.svg
│   ├── banner.avif
│   ├── banner.webp
│   ├── banner.jpg
│   ├── banner-400.jpg
│   ├── banner-800.jpg
│   ├── banner-1600.jpg
│   ├── capa-abertura.jpg
│   └── palestrante-01.jpg  (até palestrante-06.jpg)
├── midia/
│   ├── abertura.mp4
│   └── depoimento.mp3
└── legendas/
    └── abertura-pt.vtt
```

### Passo 1 — Logo e navegação marcada nas cinco páginas

O `<head>` de cada página **não muda** hoje: `charset`, `viewport`, `description`, `meta name="author"` e `title` continuam como você os escreveu na Aula 02. O que muda é o cabeçalho: entram o logo e dois atributos de acessibilidade do `<nav>`.

**`programacao.html` (trecho: `<header>`, depois da mudança)**

```html
  <header id="topo">
    <img src="img/logo-sasi.svg" alt="" width="160" height="48">
    <h1>Semana Acadêmica de Sistemas de Informação</h1>
    <p>UNEMAT Sinop · três noites de outubro · Auditório Central</p>
    <nav aria-label="Principal">
      <ul>
        <li><a href="index.html">Início</a></li>
        <li><a href="programacao.html" aria-current="page">Programação</a></li>
        <li><a href="inscricao.html">Inscrição</a></li>
        <li><a href="palestrantes.html">Palestrantes</a></li>
        <li><a href="contato.html">Contato</a></li>
      </ul>
    </nav>
  </header>
```

Três decisões deste passo:

- **`alt=""` no logo.** Pela tabela da seção 3.2, um logotipo leva o nome da organização no `alt` — mas aqui o `<h1>` logo abaixo já diz exatamente esse nome. Repetir faria o leitor de tela anunciar o mesmo texto duas vezes seguidas; então a imagem é **decorativa** e recebe `alt` vazio (presente, e vazio). Na Aula 07, quando o logo virar um link para a página inicial, o `alt` passa a descrever o destino.
- **`aria-label="Principal"`** distingue este `<nav>` de qualquer outro que a página venha a ter.
- **`aria-current="page"`** muda em cada página: em `index.html` ele vai no link "Início", em `palestrantes.html` no link "Palestrantes", e assim por diante. Repita o cabeçalho nas **cinco** páginas, trocando só onde o atributo está.

### Passo 2 — Banner responsivo na página inicial

Em `index.html`, o banner entra como **primeiro** elemento do `<main>`, antes da lista "Nesta página". Ele combina as duas técnicas da seção 3: `<picture>` escolhe o **formato**, `srcset`/`sizes` escolhem o **tamanho**. Como é a primeira imagem visível, ela não leva `lazy`.

**`index.html` (trecho: início do `<main>`)**

```html
  <main>
    <picture>
      <source srcset="img/banner.avif" type="image/avif">
      <source srcset="img/banner.webp" type="image/webp">
      <img src="img/banner-800.jpg"
           srcset="img/banner-400.jpg 400w,
                   img/banner-800.jpg 800w,
                   img/banner-1600.jpg 1600w"
           sizes="(max-width: 700px) 100vw, 1100px"
           alt="Auditório lotado na abertura da edição anterior da Semana Acadêmica"
           width="1600" height="900"
           fetchpriority="high" decoding="async">
    </picture>

    <p>Nesta página:</p>
```

Gere os seis arquivos no Squoosh a partir da mesma foto: três larguras em JPG e a versão de 1600 px também em WebP e AVIF. Anote o peso de cada um em um comentário HTML acima do `<picture>` — você vai comparar no Passo 10.

### Passo 3 — Trilhas em lista aninhada

A tabela da programação continua sendo a fonte de horários. O que falta é uma visão **por assunto**, e ela é uma lista de dois níveis. Em `programacao.html`, logo **depois** do `</table>` e **antes** do parágrafo "Voltar ao topo", acrescente:

**`programacao.html` (trecho: novo `<section>` dentro do `<main>`)**

```html
    <section id="trilhas">
      <h3>Trilhas do evento</h3>
      <p>As mesmas atividades da tabela acima, agrupadas por assunto.</p>
      <ul>
        <li>Desenvolvimento Web
          <ul>
            <li>Abertura e palestra magna: o futuro do desenvolvimento web</li>
            <li>Minicurso: Git e GitHub do zero</li>
            <li>Minicurso: acessibilidade na prática</li>
            <li>Maratona de programação</li>
          </ul>
        </li>
        <li>Ciência de Dados
          <ul>
            <li>Dashboards que os produtores realmente usam</li>
            <li>Dados abertos e cidades inteligentes</li>
          </ul>
        </li>
        <li>Inteligência Artificial
          <ul>
            <li>Minicurso: primeiros passos com redes neurais</li>
            <li>Visão computacional no controle de pragas</li>
          </ul>
        </li>
        <li>Segurança
          <ul>
            <li>Segurança em aplicações web: dez erros comuns</li>
            <li>Minicurso: phishing e engenharia social</li>
          </ul>
        </li>
      </ul>
    </section>
```

Repare que cada `<ul>` filho está **dentro** do `<li>` pai — é o erro da seção 2.3 que o validador sempre pega. O título é `<h3>` porque o `<h2>Programação</h2>` no topo do `<main>` é o título da página; as seções que vêm depois ficam um nível abaixo.

### Passo 4 — As cinco mais procuradas, com `<ol reversed>`

Ainda em `programacao.html`, depois da seção de trilhas, um ranking. Aqui os atributos da lista ordenada (seção 2.2) fazem trabalho semântico de verdade: a contagem é **decrescente**, e a marcação diz isso.

**`programacao.html` (trecho: novo `<section>` dentro do `<main>`)**

```html
    <section id="mais-procuradas">
      <h3>As cinco atividades mais procuradas</h3>
      <p>Posição pela procura na edição anterior, da quinta para a primeira.</p>
      <ol reversed>
        <li>Dados abertos e cidades inteligentes</li>
        <li>Segurança em aplicações web: dez erros comuns</li>
        <li>Maratona de programação</li>
        <li>Minicurso: primeiros passos com redes neurais</li>
        <li>Minicurso: Git e GitHub do zero</li>
      </ol>
    </section>
```

Com `reversed`, o navegador numera 5, 4, 3, 2, 1 — sem uma linha de CSS e sem digitar número nenhum. Se depois você inserir um item no meio, a contagem se reajusta sozinha.

### Passo 5 — Vídeo de abertura com legenda

**`programacao.html` (trecho: novo `<section>` dentro do `<main>`)**

```html
    <section id="abertura">
      <h3>Abertura da edição anterior</h3>
      <video controls width="640" height="360"
             poster="img/capa-abertura.jpg" preload="metadata" playsinline>
        <source src="midia/abertura.mp4" type="video/mp4">
        <track src="legendas/abertura-pt.vtt" kind="captions"
               srclang="pt" label="Português" default>
        Seu navegador não suporta vídeo HTML5.
        <a href="midia/abertura.mp4">Baixe o vídeo</a>.
      </video>
    </section>
```

Crie o arquivo de legendas com pelo menos quatro blocos, seguindo o exemplo da seção 4.3. Se o vídeo for seu, transcreva as falas reais; se for um vídeo de amostra sem fala, descreva o que aparece e os sons.

**`legendas/abertura-pt.vtt`**

```text
WEBVTT

00:00:00.000 --> 00:00:03.000
[música de abertura]

00:00:03.500 --> 00:00:07.000
Boa noite e sejam bem-vindos à Semana Acadêmica de Sistemas de Informação.

00:00:07.500 --> 00:00:11.000
Serão três noites de palestras, minicursos e maratona de programação.

00:00:11.500 --> 00:00:14.000
[aplausos]
```

### Passo 6 — Depoimento em áudio dentro de `<figure>`

**`programacao.html` (trecho: novo `<section>` dentro do `<main>`)**

```html
    <section id="depoimento">
      <h3>Depoimento de uma participante</h3>
      <figure>
        <audio controls preload="metadata">
          <source src="midia/depoimento.mp3" type="audio/mpeg">
          Seu navegador não suporta áudio HTML5.
          <a href="midia/depoimento.mp3">Baixe o áudio</a>.
        </audio>
        <figcaption>Maria Eduarda, estudante do 4º semestre, sobre o minicurso de Git.</figcaption>
      </figure>
    </section>
```

Este é o caso clássico de `<figure>`: um conteúdo autocontido (o áudio) com uma legenda visível que o identifica.

### Passo 7 — Mapa do local em `<iframe>`

**`programacao.html` (trecho: último `<section>` do `<main>`, antes do "Voltar ao topo")**

```html
    <section id="onde">
      <h3>Onde acontece</h3>
      <p>Auditório central do campus da UNEMAT em Sinop.</p>
      <iframe src="https://www.google.com/maps/embed?pb=CODIGO_GERADO_PELO_MAPS"
              title="Mapa: campus da UNEMAT em Sinop"
              width="600" height="450"
              loading="lazy"
              referrerpolicy="no-referrer-when-downgrade">
      </iframe>
    </section>
```

Para obter o código: abra o Google Maps, pesquise "UNEMAT Sinop", clique em **Compartilhar → Incorporar um mapa → Copiar HTML** e substitua o `src` acima pelo que veio no código copiado. Mantenha o `title` — o código do Maps não o inclui.

### Passo 8 — Fotos e elenco completo em `palestrantes.html`

A Aula 02 deixou três `<article>` nesta página, cada um com `<h3>`, dois parágrafos e um `<dl>` de atividades e contato. Hoje você faz duas coisas: acrescenta a **foto** dentro de cada `<article>` existente e **completa o elenco** com os três convidados que faltavam.

Em cada um dos três artigos que já existem, a `<img>` entra logo depois do `<h3>`:

**`palestrantes.html` (trecho: o artigo de Ana Lúcia Ferreira, depois da mudança)**

```html
    <article id="ana-lucia-ferreira">
      <h3>Ana Lúcia Ferreira</h3>
      <img src="img/palestrante-01.jpg"
           alt="Ana Lúcia Ferreira em frente a um quadro com um diagrama de rede neural"
           width="400" height="400" decoding="async">
      <p><strong>Professora e pesquisadora</strong> da UNEMAT — Sinop, na área de inteligência artificial.</p>
```

Faça o mesmo em Bruno Takahashi (`img/palestrante-02.jpg`) e Carla Mendes (`img/palestrante-03.jpg`), com `alt` que descreva **aquela** pessoa naquela foto. Esses três ficam visíveis sem rolar a página, então **não** levam `loading="lazy"`.

Depois do artigo de Carla Mendes, e antes do parágrafo "Voltar ao topo", acrescente os três novos — agora com `loading="lazy"`, porque estão abaixo da dobra:

**`palestrantes.html` (trecho: os três novos `<article>`)**

```html
    <article id="diego-nascimento">
      <h3>Diego Nascimento</h3>
      <img src="img/palestrante-04.jpg"
           alt="Diego Nascimento sentado em frente a dois monitores com um portal do governo aberto"
           width="400" height="400" loading="lazy" decoding="async">
      <p><strong>Desenvolvedor web</strong> na Prefeitura de Sinop, responsável pelos portais de serviços ao cidadão.</p>
      <p>Trabalha com acessibilidade em portais públicos e conduz auditorias de conformidade com a WCAG.</p>
      <dl>
        <dt>Atividades</dt>
        <dd><a href="programacao.html#dia-1">Minicurso: Git e GitHub do zero</a> (dia 1)</dd>
        <dd><a href="programacao.html#dia-2">Minicurso: acessibilidade na prática</a> (dia 2)</dd>
        <dt>Contato</dt>
        <dd><a href="https://www.linkedin.com/" target="_blank" rel="noopener noreferrer">Perfil no LinkedIn</a></dd>
      </dl>
    </article>

    <article id="eduarda-ribeiro">
      <h3>Eduarda Ribeiro</h3>
      <img src="img/palestrante-05.jpg"
           alt="Eduarda Ribeiro apresentando slides em um auditório"
           width="400" height="400" loading="lazy" decoding="async">
      <p><strong>Professora</strong> do curso de Sistemas de Informação da UNEMAT — Sinop.</p>
      <p>Coordena a Semana Acadêmica e orienta projetos de extensão que levam estudantes do HTML ao deploy.</p>
      <dl>
        <dt>Atividades</dt>
        <dd><a href="programacao.html#dia-1">Abertura e palestra magna: o futuro do desenvolvimento web</a> (dia 1)</dd>
        <dd><a href="programacao.html#dia-3">Maratona de programação</a> (dia 3)</dd>
        <dt>Contato</dt>
        <dd><a href="mailto:eduarda@exemplo.com">eduarda@exemplo.com</a></dd>
      </dl>
    </article>

    <article id="felipe-arruda">
      <h3>Felipe Arruda</h3>
      <img src="img/palestrante-06.jpg"
           alt="Felipe Arruda em um canavial, segurando um tablet com imagens de drone"
           width="400" height="400" loading="lazy" decoding="async">
      <p><strong>Engenheiro de visão computacional</strong> na cooperativa Coopercana.</p>
      <p>Usa imagens de drone e modelos de aprendizado profundo para detectar pragas antes que elas se espalhem.</p>
      <dl>
        <dt>Atividades</dt>
        <dd><a href="programacao.html#dia-2">Visão computacional no controle de pragas</a> (dia 2)</dd>
        <dt>Contato</dt>
        <dd><a href="https://github.com/" target="_blank" rel="noopener noreferrer">Perfil no GitHub</a></dd>
      </dl>
    </article>
```

Cada `alt` descreve a pessoa — o que a foto mostra. O parágrafo abaixo traz o minicurrículo — a informação que o texto acrescenta. Nada se repete.

> **💡 Dica**
> Os seis nomes desta página são os mesmos que vão alimentar o `js/dados.js` na Aula 12 e a página gerada por JavaScript na Aula 13. Manter o elenco estável agora poupa retrabalho depois — e é exatamente o que acontece em um projeto real.

### Passo 9 — Campos avançados em `inscricao.html`

O formulário da Aula 03 tem quatro `<fieldset>` e nenhum arquivo para enviar. Hoje ele ganha o quinto grupo e o atributo que faz upload funcionar.

Primeiro, no `<form>`, acrescente o `enctype`:

**`inscricao.html` (trecho: abertura do `<form>`)**

```html
    <form action="/inscrever" method="post" id="form-inscricao"
          enctype="multipart/form-data">
```

Depois, antes do `</form>`, o novo grupo:

**`inscricao.html` (trecho: novo `<fieldset>`)**

```html
      <fieldset>
        <legend>Comprovante e pagamento</legend>

        <p>
          <label for="comprovante">Comprovante de matrícula (PDF ou imagem, até 5 MB) — obrigatório</label>
          <input type="file" id="comprovante" name="comprovante"
                 accept=".pdf,image/*" required>
        </p>

        <p>
          <label for="certificados">Certificados de edições anteriores (opcional, vários arquivos)</label>
          <input type="file" id="certificados" name="certificados" accept=".pdf" multiple>
        </p>

        <p>
          <label for="cpf">CPF — obrigatório</label>
          <input type="text" id="cpf" name="cpf" inputmode="numeric" required
                 pattern="[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}"
                 placeholder="000.000.000-00" title="Formato: 000.000.000-00"
                 autocomplete="off">
        </p>

        <p>
          <label for="lote">Lote</label>
          <select id="lote" name="lote">
            <option value="30">1º lote — R$ 30</option>
            <option value="45">2º lote — R$ 45</option>
          </select>
        </p>

        <p>
          <label for="qtd">Quantidade de ingressos</label>
          <input type="number" id="qtd" name="qtd" min="1" max="5" value="1">
        </p>

        <p>Total: <output id="total" for="lote qtd">R$ 30</output></p>

        <p>
          <label for="vagas">Vagas ocupadas no minicurso de Git</label>
          <meter id="vagas" value="38" min="0" max="40" low="20" high="35" optimum="0">38 de 40</meter>
        </p>
      </fieldset>
```

E, junto ao botão de envio que já existe, um segundo botão que salva sem validar:

**`inscricao.html` (trecho: os dois botões)**

```html
      <button type="submit">Enviar inscrição</button>
      <button type="submit" formaction="/rascunho" formnovalidate>Salvar rascunho</button>
```

O `<output>` fica parado em "R$ 30" por enquanto: sem JavaScript ele não calcula nada. Na Aula 13, com eventos, ele passa a mudar sozinho quando o lote ou a quantidade mudam.

### Passo 10 — Validação e medição

1. Valide as **cinco** páginas em validator.w3.org (aba **Validate by File Upload**). Meta: **zero erros**.
2. Abra `index.html` no Live Server, DevTools → **Network**, marque **Disable cache**, recarregue e anote o peso total no rodapé da aba (**transferred**). Repita em `programacao.html`.
3. Ordene por **Size**. Otimize no Squoosh os três maiores arquivos que forem imagens; substitua-os na pasta `img/`.
4. Recarregue e anote o novo peso. Registre os dois valores em um comentário HTML no topo do `<body>` de cada uma das duas páginas:

```html
<!-- Peso da página antes da otimização: 7,8 MB · depois: 1,1 MB (redução de 86%) -->
```

### Como testar

- Menu: os cinco links levam às cinco páginas, **todas existentes** — nenhum 404. Em cada página, o item correspondente tem `aria-current="page"`.
- `index.html`: na aba Network, filtrando por **Img**, o banner baixado é `.avif` (ou `.webp`, conforme o navegador). Estreitando a janela para 400 px e recarregando com **Disable cache**, o arquivo escolhido pelo `srcset` muda.
- `programacao.html`: a tabela dos três dias continua lá, com `<caption>`, três `<tbody>` e `<tfoot>`; a lista de trilhas mostra as atividades recuadas sob cada assunto; o ranking numera de 5 para 1.
- Vídeo: o `poster` aparece antes do play; ao dar play, o botão **CC** dos controles liga a legenda e o texto aparece nos tempos definidos.
- Áudio: o player aparece com play, tempo e volume, e a legenda da `<figure>` fica abaixo dele.
- Mapa: o quadro mostra o campus; se estiver em branco, confira se o `src` é a URL de **embed** (contém `/maps/embed?`), não a URL normal do Maps.
- `palestrantes.html`: seis artigos, cada um com foto e `<dl>`; na aba Network, as três últimas fotos só são baixadas quando você rola até elas.
- `inscricao.html`: o seletor de arquivos filtra PDF e imagens; o botão "Enviar inscrição" bloqueia se o CPF estiver vazio ou fora do formato, e o "Salvar rascunho" envia mesmo assim.
- Validador: zero erros nas cinco páginas.
- Network: o peso de cada página ficou abaixo de 2 MB (com o vídeo em `preload="metadata"`, ele não conta até o play).

**Resultado esperado:** o mesmo site de cinco páginas da Aula 02, agora com identidade visual (logo), navegação marcada, banner responsivo, listas de dois níveis, mídia acessível e o formulário completo — sem uma linha de CSS e sem ter descartado nada do que já estava pronto.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Escreva o `alt` adequado para: (a) o logotipo da UNEMAT; (b) uma linha decorativa entre duas seções; (c) um gráfico de pizza mostrando 60% de aprovados e 40% de reprovados; (d) uma foto do campus dentro de um link para a página de contato.

**A2.** Diferencie `alt` de `figcaption`: para quem cada um existe, e por que não devem ter o mesmo texto.

**A3.** Qual formato de imagem você usaria para: (a) foto de paisagem; (b) logotipo vetorial; (c) captura de tela com texto pequeno; (d) ícone que precisa escalar de 16 px a 512 px sem perder qualidade?

**A4.** O que faz `loading="lazy"` em uma `<img>`? Por que ele melhora a performance — e por que a imagem do topo da página **não** deve tê-lo?

**A5.** Por que um `<button>` sem `type` dentro de um formulário pode causar problemas? Cite os três valores possíveis de `type` e quando usar cada um.

**A6.** Para que serve o elemento `<track>` dentro de `<video>`? Qual a diferença entre `kind="captions"` e `kind="subtitles"`?

**A7.** Quando usar `<ul>`, `<ol>` e `<dl>`? Dê um exemplo real de cada, retirado do site do evento.

**A8.** Escreva uma lista de definição com três termos técnicos desta disciplina (por exemplo: `alt`, `srcset`, WebVTT) e suas definições.

**A9.** Como se representa uma lista aninhada corretamente? Escreva o HTML de dois níveis e explique qual erro o validador do W3C acusa quando o aninhamento está errado.

**A10.** Por que um menu de navegação deve ser marcado como lista dentro de `<nav>`? Cite dois ganhos concretos.

**A11.** Um campo `<input type="file">` está em um `<form method="post">` sem `enctype`. O que chega ao servidor quando o usuário envia uma foto? Qual atributo corrige isso?

**A12.** Dado `<meter value="38" min="0" max="40" low="20" high="35" optimum="0">`, o que os atributos `low`, `high` e `optimum` comunicam ao navegador? Quando `<progress>` seria a escolha errada para esse mesmo dado?

### Nível B — Aplicação

**B1.** Crie uma galeria de seis imagens usando `<figure>` e `<figcaption>`, com `alt` descritivo em todas, `loading="lazy"` nas três últimas e `width`/`height` declarados. Otimize as imagens no Squoosh e documente, em comentários HTML acima de cada `<figure>`, o peso original e o peso após a otimização.

**Resultado esperado:** seis figuras com legenda visível; o validador não acusa erros; na aba Network, ordenando por Size, nenhuma imagem passa de 150 KB; os comentários mostram redução em todas as seis.

<details><summary>Dica</summary>

Redimensione antes de comprimir: uma foto exibida em 400 px de largura sai do Squoosh com 800 px (para telas 2×), não com 4000. Só depois escolha WebP a 75 de qualidade. Para saber o peso original, veja a coluna Size no Network antes de trocar o arquivo, ou clique com o botão direito no arquivo e escolha Propriedades.
</details>

**B2.** Monte uma página de contato (para o seu projeto autoral) com: formulário (nome, e-mail, assunto via `<select>`, mensagem em `<textarea>`), telefone e e-mail clicáveis (`tel:` e `mailto:`), mapa incorporado por `<iframe>` com `title`, e horário de atendimento em uma tabela com `caption`, `thead` e `th scope`.

**Resultado esperado:** ao clicar no telefone em um celular, o discador abre; ao clicar no e-mail, o cliente de e-mail abre com o destinatário preenchido; o mapa mostra o local; a tabela tem cabeçalho de coluna; zero erros no validador.

<details><summary>Dica</summary>

`<a href="tel:+5566999990000">(66) 99999-0000</a>` — o número no `href` vai sem espaços, parênteses ou traços, com o código do país. Para `mailto:`, você pode pré-preencher o assunto: `mailto:contato@evento.br?subject=Inscrição`. Se o mapa ficar em branco, confira se copiou o `src` da opção "Incorporar um mapa", e não a URL da barra de endereço.
</details>

**B3.** Implemente uma página com um `<picture>` servindo AVIF, WebP e JPG, e uma `<img>` com `srcset`/`sizes` em três larguras (400, 800 e 1600 px). Na aba Network do DevTools, com **Disable cache** ligado, teste em três larguras de janela (400, 900 e 1400 px) e registre em uma tabela qual arquivo foi baixado em cada caso e por quê.

**Resultado esperado:** o `<picture>` baixa o `.avif` (ou `.webp`, dependendo do navegador); a `<img>` com `srcset` baixa arquivos diferentes conforme a largura; a tabela explica cada escolha com base em `sizes` e na densidade da tela.

<details><summary>Dica</summary>

Use o modo dispositivo do DevTools para fixar larguras exatas. Se em todas as larguras o navegador baixar sempre o mesmo arquivo, confira se o `sizes` está presente — sem ele, o navegador assume `100vw`. Se ele baixar sempre o maior, você provavelmente está em uma tela com densidade 2× (o DevTools mostra o DPR no modo dispositivo).
</details>

**B4.** Monte uma página de cardápio usando `<dl>` para os pratos (termo = nome; definição = descrição e preço), `<ul>` para os acompanhamentos e `<ol>` para o modo de preparo de um dos pratos. Inclua uma foto por prato em `<figure>` com `<figcaption>`.

**Resultado esperado:** cada prato aparece como termo com descrição recuada; o modo de preparo está numerado; os acompanhamentos, com marcadores; cada foto tem `alt` que descreve o prato e legenda com o nome; zero erros no validador.

<details><summary>Dica</summary>

Um prato pode ter dois `<dd>`: um para a descrição, outro para o preço. Para colocar a `<figure>` junto ao prato, ela pode ficar dentro do `<dd>` — `<dd>` aceita conteúdo de fluxo, inclusive figuras.
</details>

**B5.** Amplie o formulário de inscrição da Aula 03 com um `<fieldset>` "Comprovante e pagamento" contendo: upload do comprovante de matrícula (`accept` para PDF e imagens), upload opcional de vários certificados (`multiple`), CPF com `inputmode="numeric"` e `pattern`, `<select>` de lote, `<input type="number">` de quantidade e um `<output>` com o total. Acrescente um botão "Salvar rascunho" com `formaction` diferente e `formnovalidate`.

**Resultado esperado:** o `<form>` tem `enctype="multipart/form-data"`; o seletor de arquivos filtra os tipos permitidos; o botão "Enviar" exige os campos obrigatórios e o "Salvar rascunho" envia sem validar; zero erros no validador.

<details><summary>Dica</summary>

Teste o `formnovalidate` deixando um campo `required` vazio e clicando nos dois botões: só o "Enviar" deve bloquear. Para o `<output>`, o valor fica fixo por enquanto — ele só passará a calcular sozinho quando você aprender eventos, na Aula 13.
</details>

### Nível C — Desafio em sala

**C1.** Landing page multimídia. Crie a landing page de um produto ou evento contendo: vídeo de fundo (`muted`, `loop`, `autoplay`, com `poster`), galeria responsiva com `<picture>` em três formatos, player de áudio com depoimento, formulário de captação de contatos (nome, e-mail, telefone, interesse em `<select>`) e mapa em `<iframe>`. Sem CSS ainda. Otimize todas as mídias e apresente uma tabela comparando o peso de cada arquivo antes e depois, com o percentual de redução total da página.

<details><summary>Dica</summary>

O vídeo de fundo só toca sozinho se tiver `muted` — sem isso, o navegador bloqueia o `autoplay`. Para o percentual de redução, some os pesos de todos os arquivos antes e depois: `(antes − depois) ÷ antes × 100`. A aba Network dá os dois totais se você trocar os arquivos e recarregar com Disable cache.
</details>

## 🏆 Desafios

### ⭐ Caça aos bugs na galeria
Tags: html, acessibilidade, bug

Um colega entregou a galeria abaixo dizendo que "abre normal no navegador". Abre — mas o validador do W3C acusa erros, o leitor de tela lê nomes de arquivo e o vídeo nunca mostra legenda. Há **oito** problemas no trecho. Encontre todos sem rodar o validador primeiro; depois use o validador para conferir quantos você achou sozinho.

```html
<section>
  <h2>Galeria</h2>
  <ul>
    <li><img src="img/foto1.jpg" alt="imagem"></li>
    <ul>
      <li><img src="img/foto2.jpg"></li>
    </ul>
    <li>
      <figure>
        <img src="img/foto3.jpg" alt="foto3.jpg" loading="lazy">
      </figure>
    </li>
  </ul>
  <video controls>
    <source src="midia/abertura.mp4">
    <track src="legendas/abertura.vtt" kind="captions">
  </video>
  <iframe src="https://www.youtube.com/watch?v=abc123" width="560" height="315"></iframe>
  <img src="img/logo.png" alt="logo da empresa" title="logo">
</section>
```

**Critérios de pronto**

- Uma lista numerada com os oito problemas, cada um com: a linha, o que está errado, por que importa (validação, acessibilidade ou funcionamento) e a correção.
- O trecho reescrito, validando com zero erros no W3C.
- Pelo menos três dos problemas são de acessibilidade (não apenas de validação).
- Um parágrafo explicando por que "abre normal no navegador" não é critério de qualidade.

<details><summary>Pistas</summary>

1. Releia a seção 2.3 sobre o que pode ser filho direto de `<ul>`.
2. Releia a tabela de `alt` da seção 3.2: dois `alt` estão presentes mas errados, e um está ausente.
3. Um `<source>` sem `type` obriga o navegador a baixar o arquivo para descobrir se consegue tocá-lo; um `<track>` sem `srclang` e `label` não aparece no menu de legendas.
4. A URL do YouTube que funciona em `<iframe>` contém `/embed/`, e todo `<iframe>` precisa de um atributo que o leitor de tela anuncia.
</details>

### ⭐⭐ Galeria dez vezes mais leve
Tags: html, performance, devtools, investigacao

Uma página de galeria com doze fotos de celular pesa em média 40 MB. Quanto tempo ela leva para abrir no 4G lento? Você vai medir. Monte uma página com doze fotos originais (sem tratamento), meça o peso e o tempo de carregamento com throttling **Slow 4G** e, depois, construa a mesma galeria com um pipeline completo de imagens responsivas — tamanhos, formatos e prioridade de carregamento — até reduzir o peso em pelo menos 90% sem que a qualidade visível caia.

**Critérios de pronto**

- Duas versões da página (`galeria-antes.html` e `galeria-depois.html`) com as mesmas doze fotos.
- Cada `<img>` da versão final usa `srcset` com três larguras, `sizes` coerente com o layout, e está dentro de `<picture>` com AVIF, WebP e JPG.
- As duas ou três primeiras fotos têm `fetchpriority="high"`; as demais, `loading="lazy"`.
- Uma tabela em Markdown ou HTML com, para cada versão: peso total transferido, número de requisições e tempo até o evento **Load** (visível no rodapé do Network), medidos com **Slow 4G** e cache desabilitado.
- Redução de peso igual ou superior a 90%.

<details><summary>Pistas</summary>

1. No Squoosh, a aba **Resize** reduz dimensões; a aba **Compress** troca o formato. Faça as duas coisas: a maior economia vem de reduzir a dimensão.
2. Em vez de tratar doze fotos uma a uma, procure o modo de linha de comando do Squoosh (`@squoosh/cli`) ou a ferramenta ImageMagick (`magick foto.jpg -resize 800x foto-800.jpg`) — vale a pena aprender agora.
3. `sizes` deve refletir o espaço real: se as fotos ficarão em três colunas em telas largas, cada uma ocupa cerca de `33vw`.
4. Meça com **Disable cache** marcado e sempre na mesma largura de janela; senão os números não são comparáveis.
</details>

**Para ir além:** rode o Lighthouse (aba do DevTools) nas duas versões e compare a nota de Performance e a métrica *Largest Contentful Paint*.

### ⭐⭐⭐ Mídia acessível de ponta a ponta
Tags: html, acessibilidade, investigacao, projeto

A WCAG exige, para vídeo pré-gravado: legendas (critério 1.2.2), audiodescrição ou alternativa em texto (1.2.3) e, para áudio, transcrição (1.2.1). Quase nenhum site de evento cumpre isso — o seu vai cumprir. Pegue um vídeo de dois a três minutos com fala (pode ser uma palestra curta gravada por você ou um vídeo livre) e um áudio de um minuto, e construa uma página em que **toda** a informação da mídia esteja disponível para alguém que não ouve e para alguém que não vê.

**Critérios de pronto**

- O `<video>` tem três `<track>`: `captions` em português com sons relevantes entre colchetes, `chapters` com pelo menos quatro capítulos, e `descriptions` descrevendo o que aparece na tela nos momentos em que a fala não explica.
- Uma transcrição completa do vídeo em texto na própria página, dentro de `<details>` para não ocupar espaço, sincronizada com os capítulos por `<h3>`.
- O `<audio>` tem, logo abaixo, a transcrição completa em texto.
- Ao ligar as legendas nos controles do navegador, os três tipos de trilha aparecem no menu, com os rótulos corretos.
- Um relatório de uma página: quanto tempo levou transcrever cada minuto de mídia, que ferramentas ajudaram (transcrição automática do YouTube, Whisper, transcrição do Google Docs) e o que precisou ser corrigido à mão.

<details><summary>Pistas</summary>

1. Leia a especificação de WebVTT na MDN ("WebVTT API") — capítulos e descrições usam o mesmo formato de tempo das legendas, mudando só o `kind` do `<track>`.
2. O YouTube gera legendas automáticas para vídeos enviados; é possível baixá-las em formato `.vtt` e corrigir os erros — muito mais rápido que transcrever do zero.
3. Descrições (`kind="descriptions"`) são lidas em voz alta pelo leitor de tela nos intervalos sem fala; escreva-as curtas o bastante para caber no silêncio disponível.
4. Para ver a transcrição sincronizada por capítulos, cada `<h3>` da transcrição deve corresponder a um bloco do arquivo de capítulos — mesmo texto, mesma ordem.
</details>

**Para ir além:** publique a página e teste com o leitor de tela NVDA (Windows, gratuito) ou o VoiceOver (macOS): navegue só pelo teclado até o vídeo, dê play e ouça as descrições.

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| A imagem aparece no VS Code mas não no Live Server (ícone quebrado) | Caminho errado ou diferença de maiúsculas: `Foto.JPG` no disco e `foto.jpg` no `src`. Windows ignora a diferença; o servidor de deploy (Linux) não | Use caminhos relativos à página, nomes em minúsculas, sem espaços nem acentos |
| Leitor de tela lê "DSC zero zero quatro dois ponto jpg" | `<img>` sem `alt` | Todo `<img>` tem `alt`; `alt=""` só em imagens decorativas |
| `Element ul not allowed as child of element ul` no validador | Lista aninhada colocada entre dois `<li>` em vez de dentro de um | O `<ul>` filho vai dentro do `<li>` pai |
| O vídeo de fundo não inicia e o console mostra `play() failed because the user didn't interact with the document first` | `autoplay` sem `muted` | Adicione `muted` (e `playsinline` para iPhone) |
| O botão CC não aparece nos controles do vídeo | `<track>` com caminho errado, sem `kind`, ou arquivo `.vtt` sem a primeira linha `WEBVTT` | Confira o caminho na aba Network (deve retornar 200) e a primeira linha do arquivo |
| O `<iframe>` fica em branco | URL normal do site em vez da URL de embed, ou o site proíbe incorporação (`X-Frame-Options: DENY`) | Use a URL de embed fornecida pelo serviço (YouTube: `/embed/ID`; Maps: "Incorporar um mapa") |
| A página "pula" quando as imagens carregam | `<img>` sem `width` e `height` | Declare as dimensões reais do arquivo; o CSS redimensiona depois |
| O `srcset` está lá, mas o navegador baixa sempre o maior arquivo | Falta o `sizes`, então o navegador assume `100vw`; ou a tela tem densidade 2× | Escreva `sizes` coerente com o layout; teste com o DPR do modo dispositivo em 1 |
| O servidor recebe só o nome do arquivo, não o conteúdo | `<form>` com `type="file"` sem `enctype="multipart/form-data"` | Adicione o `enctype` ao `<form>` |
| Peso da página não muda depois de otimizar as imagens | Cache do navegador servindo os arquivos antigos | Marque **Disable cache** na aba Network antes de recarregar |

## 🏠 Atividade assíncrona (1 h)

**Parte 1 — Leitura (20 min).** SILVA, M. S. *Criando sites com HTML*, capítulos sobre listas e imagens. TERUEL, E. C. *HTML5 — Guia Prático*, capítulo sobre APIs de mídia. Na MDN em pt-BR, leia "Imagens responsivas" e "Conteúdo de vídeo e áudio" (links em Para aprofundar).

**Parte 2 — Entrega (30 min).** No seu **projeto autoral**, entregue os exercícios **B1** (galeria com a tabela de peso antes/depois) e **B5** (formulário ampliado com upload, `inputmode`, `<output>` e botão de rascunho). Entregue também as páginas de programação e de galeria do seu projeto, com todas as mídias e os três tipos de lista aplicados, validadas no W3C.

**Critério de pronto:** as páginas validam com zero erros; toda `<img>` tem `alt`, `width` e `height`; o vídeo tem `<track>` com arquivo `.vtt` funcionando; a página de galeria pesa menos de 2 MB na aba Network com cache desabilitado; o comentário HTML com o peso antes/depois está no topo do `<body>`.

**Entrega:** commit + push e link do repositório no SIGAA (ou o `.zip` da pasta do projeto, se você ainda não estiver usando Git).

**Parte 3 — Fórum (10 min).** No fórum "Descrever imagens", escreva o `alt` de três imagens do seu próprio projeto — uma informativa, uma decorativa e uma dentro de link — e justifique cada escolha em duas linhas. Comente o `alt` de dois colegas: ele entrega a mesma informação que a imagem entrega para quem vê?

## ✅ Checkpoint do projeto

Ao fim desta aula, o repositório do seu projeto autoral deve ter:

- [ ] Página de programação (ou equivalente do seu domínio) com os horários em `<time>`, uma `<ul>` aninhada de dois níveis e uma `<ol>` usando pelo menos um dos atributos `start`, `reversed` ou `type`.
- [ ] Menu de navegação como `<ul>` dentro de `<nav aria-label>`, com `aria-current="page"` na página atual.
- [ ] Uma `<dl>` em uso (glossário, ficha de pessoa, cardápio — o que fizer sentido no seu domínio).
- [ ] Página de galeria com seis `<figure>`/`<figcaption>`, `alt` descritivo, `width`/`height` e `loading="lazy"` nas imagens abaixo da dobra.
- [ ] Banner em `<picture>` com AVIF, WebP e JPG, sem `lazy`.
- [ ] Um `<video>` com `controls`, `poster`, `preload="metadata"` e `<track kind="captions">` apontando para um `.vtt` válido.
- [ ] Um `<audio>` com `controls` e fallback.
- [ ] Um `<iframe>` com `title` e `loading="lazy"`.
- [ ] Formulário de inscrição com `enctype`, campo de upload com `accept`, `inputmode` no CPF e um `<output>`.
- [ ] Zero erros no validador W3C em todas as páginas.
- [ ] Comentário no topo do `<body>` com o peso da página antes e depois da otimização.

## 📚 Para aprofundar

- MDN — Imagens responsivas: <https://developer.mozilla.org/pt-BR/docs/Learn_web_development/Core/Structuring_content/Responsive_images> — o guia completo de `srcset`, `sizes` e `<picture>`, com exemplos para testar.
- MDN — Conteúdo de vídeo e áudio: <https://developer.mozilla.org/pt-BR/docs/Learn_web_development/Core/Structuring_content/HTML_video_and_audio> — atributos, fallback e `<track>`.
- MDN — Elemento `<img>`: <https://developer.mozilla.org/pt-BR/docs/Web/HTML/Element/img> — referência de todos os atributos, incluindo `loading`, `decoding` e `fetchpriority`.
- MDN — Elemento `<iframe>`: <https://developer.mozilla.org/pt-BR/docs/Web/HTML/Element/iframe> — `sandbox`, `allow` e `referrerpolicy` explicados.
- MDN — Elemento `<dl>`: <https://developer.mozilla.org/pt-BR/docs/Web/HTML/Element/dl> — casos de uso e aninhamento de `<dt>`/`<dd>`.
- MDN — API WebVTT: <https://developer.mozilla.org/pt-BR/docs/Web/API/WebVTT_API> — o formato de legendas em detalhe.
- web.dev — Learn Images: <https://web.dev/learn/images> — curso gratuito sobre formatos, compressão e imagens responsivas.
- Squoosh: <https://squoosh.app> — otimizador de imagens no navegador, usado nesta aula.
- W3C — WCAG 2.1, critérios 1.1.1 (conteúdo não textual), 1.2.2 (legendas) e 1.3.1 (informação e relações): <https://www.w3.org/Translations/WCAG21-ptbr/> — tradução oficial em português.
- SILVA, Maurício Samy. *Criando sites com HTML: sites de alta qualidade com HTML e CSS*. Novatec, 2008 — capítulos sobre listas e imagens.
- TERUEL, Evandro C. *HTML 5 — Guia Prático*. Saraiva, 2014 — capítulo sobre APIs de mídia.

Na próxima aula você dá ao site o esqueleto de layout com `<header>`, `<main>`, `<section>`, `<article>` e `<aside>` — e escreve as primeiras linhas de CSS.
