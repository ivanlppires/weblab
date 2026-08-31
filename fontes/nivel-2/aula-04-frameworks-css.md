# Aula 04 — Frameworks CSS: Bootstrap, Tailwind e Material

> **Nível 2 — Desenvolvimento Web** · Unidade 1: Web estática
> WebLab · UNEMAT — Campus Sinop
> **Tempo estimado:** 3 blocos de 50 min + 1 h de prática

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Explicar quais problemas concretos um framework CSS resolve — reset, grid, breakpoints, componentes e escala visual — e quais problemas ele **cria**.
- Distinguir as duas filosofias dominantes do mercado (componentes prontos × classes utilitárias) e reconhecer qual delas um projeto qualquer está usando só olhando o HTML.
- Carregar um framework por CDN com versão fixa, `integrity` e `crossorigin`, e explicar o que a hash SRI protege e o que ela **não** protege.
- Montar layouts responsivos com o grid de 12 colunas do Bootstrap 5.3 (`container` → `row` → `col-*`) e prever, sem abrir o navegador, o que acontece em cada breakpoint.
- Personalizar o Bootstrap pelo caminho certo — sobrescrevendo as variáveis CSS `--bs-*` — em vez de brigar com o framework a golpes de `!important`.
- Escrever o mesmo componente nos três frameworks (Bootstrap, Tailwind 4 e Material Web) e comparar peso, verbosidade e liberdade visual com números medidos na aba Network.
- Justificar por escrito, no `README.md`, a escolha de framework do seu projeto — requisito do Marco 1.

## 📋 Pré-requisitos

- [ ] Repositório `cafe-cerrado` com `index.html`, `cardapio.html` e `contato.html` publicados no GitHub Pages (Aula 03).
- [ ] As três páginas com landmarks completos (`header`, `nav`, `main`, `footer`), menu idêntico com `aria-current="page"` e zero erros no validador do W3C.
- [ ] `css/estilo.css` ligado às três páginas e com o bloco `:root` de variáveis criado na Aula 02.
- [ ] Formulário de `contato.html` com `fieldset`, `label` em todos os campos e validação nativa funcionando.
- [ ] VS Code com Live Server; Chrome ou Firefox com DevTools — hoje você vai viver nas abas **Elements**, **Network** e no **modo dispositivo**.
- [ ] Git configurado e o hábito de `commit` + `push` a cada passo concluído.

> Na aula passada o Café Cerrado virou um site de verdade: três páginas ligadas entre si, cardápio com listas e tabela, formulário de contato que o navegador valida sozinho e um CSS mínimo, escrito à mão, só para enxergar a estrutura. O problema é que esse CSS mínimo continua mínimo: em 380 px de largura o menu se amontoa, os cartões não viram uma coluna e o formulário tem cara de 1998. Hoje você não vai escrever quinhentas linhas de CSS para resolver isso — vai comparar os três frameworks que dominam o mercado, entender a filosofia de cada um e adotar um deles no projeto. A estrutura semântica de ontem não muda uma tag: o framework entra nas **classes**.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Por que frameworks existem; as duas filosofias; CDN, SRI e a ordem no `<head>`; Bootstrap: grid de 12 colunas e breakpoints |
| 2 | 50 min | Bootstrap: utilitários, componentes e personalização por variáveis `--bs-*`; Tailwind 4 no Play CDN; Material Web via importmap; comparativo medido |
| 3 | 50 min | Mão na massa: o Café Cerrado adota o Bootstrap 5.3 nas três páginas; justificativa no `README.md`; Laboratório |

## 1. Por que um framework CSS existe

### 1.1 A lista de coisas que ninguém quer reescrever

Abra o `css/estilo.css` que você escreveu nas Aulas 02 e 03 e conte: são cerca de 250 linhas para três páginas simples. Agora imagine o site inteiro de uma prefeitura, com quarenta páginas. Toda equipe que começa um projeto do zero precisa resolver, na mão, exatamente os mesmos seis problemas:

1. **Normalizar o navegador.** Chrome, Firefox e Safari têm margens, tamanhos de fonte e estilos de botão diferentes por padrão. Sem um reset, a mesma página fica com espaçamentos distintos em cada um.
2. **Um sistema de grid.** Colocar três blocos lado a lado no desktop e um embaixo do outro no celular é o problema de layout mais repetido da Web.
3. **Breakpoints coerentes.** Em que largura o layout muda? 600 px? 768 px? Se cada componente escolher o seu, o site quebra em pedaços diferentes conforme a tela.
4. **Componentes repetitivos.** Menu que colapsa em hambúrguer, card, modal, alerta, badge, paginação. Todo site tem os mesmos.
5. **Uma escala visual.** Espaçamentos, tamanhos de fonte, raios de borda e sombras precisam vir de um conjunto pequeno de valores. Sem escala, um botão tem `padding: 11px`, o outro `12px`, e a página parece torta sem que ninguém saiba dizer por quê.
6. **Estados dos formulários.** Campo focado, campo inválido, campo desabilitado, texto de ajuda.

Um framework CSS é uma resposta pronta e testada para os seis. Você troca "escrever" por "aprender o vocabulário": em vez de `padding: 1rem`, escreve `class="p-3"`; em vez de uma media query, escreve `class="col-12 col-md-6"`.

### 1.2 O que você paga por isso

Não existe almoço grátis. O preço vem em quatro parcelas:

- **Peso.** O CSS completo do Bootstrap 5.3 tem cerca de 230 KB (uns 32 KB comprimidos na rede). Seu site vai usar talvez 15 % disso. Em produção séria, o framework é instalado via npm e passa por uma etapa de build que remove o não utilizado.
- **Cara de framework.** Sites que usam os componentes sem customizar nada ficam idênticos entre si. É o famoso "isso aí é Bootstrap" que qualquer desenvolvedor identifica em dois segundos.
- **Vocabulário para decorar.** `ms-auto`, `d-flex`, `col-md-6`, `text-bg-primary`. Nada disso é CSS: é o dialeto de um framework específico, que você esquece se ficar seis meses sem usar.
- **Dependência.** Quando o Bootstrap 4 virou 5, `ml-3` virou `ms-3` e o jQuery sumiu. Projetos inteiros pararam para migrar.

> **⚠️ Atenção**
> Framework é aceleração, não substituto do fundamento. É por isso que este curso ensinou HTML semântico e CSS na mão **antes**: quando o `col-md-6` não fizer o que você espera, quem resolve é quem sabe que aquilo é `flex: 0 0 auto; width: 50%` por baixo. Quem só decorou classes trava.

### 1.3 Framework, biblioteca e design system

Três palavras que a internet mistura e que caem em prova:

| Termo | O que é | Exemplo |
|---|---|---|
| Framework CSS | Conjunto pronto de classes, grid e componentes que você usa como base do layout | Bootstrap, Bulma, Tailwind |
| Biblioteca de componentes | Componentes prontos para um framework de **JavaScript** específico | Vuetify (Vue), MUI (React) |
| Design system | Especificação de princípios visuais, independente de tecnologia | Material Design, GOV.BR DS |

Um design system pode ter várias implementações. O Material Design do Google tem implementação oficial em Web Components (Material Web), em Flutter, em Android e em React (via MUI, que é de terceiros). Guarde essa distinção: no Nível 3 você usa o **Vuetify**, que é uma biblioteca de componentes Vue que implementa o Material Design. É o mesmo design system desta aula, embrulhado de outro jeito.

> **🧠 Você sabia?**
> O Bootstrap nasceu como um problema interno do Twitter. Em 2010, cada equipe da empresa fazia sua própria interface, e o painel administrativo era uma colcha de retalhos. Dois funcionários, Mark Otto e Jacob Thornton, criaram uma biblioteca interna chamada **Twitter Blueprint** para padronizar aquilo. Em agosto de 2011 ela foi liberada como software livre com o nome Bootstrap e, por cerca de uma década, foi o repositório com mais estrelas do GitHub — antes de ser ultrapassado por listas de estudo e por projetos de IA. A escolha de abrir o código foi feita por dois desenvolvedores, sem plano de negócio: hoje é a base visual de uma fatia enorme dos sites administrativos do mundo, inclusive de muitos sistemas de universidades brasileiras.

## 2. As duas filosofias

### 2.1 Componentes prontos

A ideia é dar a você classes de **alto nível**, cada uma com um significado de interface inteira:

```html
<button class="btn btn-primary">Enviar</button>
<span class="badge text-bg-success">Novo</span>
<div class="alert alert-warning">Estoque baixo.</div>
```

Você lê `btn btn-primary` e sabe o que é: um botão de ação principal. Não sabe (nem precisa saber, no primeiro momento) qual é o `padding`, o `border-radius` ou a cor. Seguem essa filosofia: **Bootstrap**, **Bulma**, **Materialize**, **Foundation**.

**A favor:** protótipo rápido, HTML curto e legível, decisão de design já tomada por alguém.
**Contra:** para fugir do visual padrão você precisa lutar com a especificidade do framework — e é aí que aparece o `!important` desesperado.

### 2.2 Classes utilitárias (utility-first)

A ideia oposta: classes **minúsculas**, cada uma equivalente a uma ou duas declarações CSS. O componente nasce da composição:

```html
<button class="px-4 py-2 rounded-lg bg-sky-700 text-white font-semibold hover:bg-sky-800">
  Enviar
</button>
```

Nenhuma dessas classes sabe o que é um botão. `px-4` é `padding-left` e `padding-right`; `bg-sky-700` é uma cor da paleta; `hover:bg-sky-800` é a mesma coisa dentro de `:hover`. O framework dominante aqui é o **Tailwind CSS**.

**A favor:** liberdade visual total, nenhum "visual padrão", CSS final minúsculo (só as classes usadas entram no arquivo gerado), e você nunca mais inventa nome de classe.
**Contra:** HTML verboso, curva de memorização, e a repetição só desaparece quando você extrai componentes em algum outro lugar (um `include`, um componente Vue, um `@apply`).

### 2.3 As duas filosofias em uma tabela

| Critério | Componentes prontos | Utility-first |
|---|---|---|
| Unidade de trabalho | O componente (`card`, `navbar`) | A declaração (`p-4`, `flex`) |
| Onde mora a decisão visual | No framework | No seu HTML |
| Primeiro dia de projeto | Muito rápido | Lento |
| Sexto mês de projeto | Rápido, se o design couber no padrão | Rápido e sem surpresas |
| Tamanho do HTML | Curto | Longo |
| Tamanho do CSS final | Fixo e grande | Proporcional ao que você usou |

### 2.4 Na prática, as duas convergiram

Não caia na guerra santa. O Bootstrap 5 tem **centenas** de classes utilitárias (`d-flex`, `mt-3`, `text-center`, `gap-2`) — a filosofia utility entrou nele. E o Tailwind tem `@apply` e plugins que empacotam conjuntos de utilitários em uma classe só — a filosofia de componente entrou nele. A diferença real, hoje, é **de onde você parte**: de um componente que você customiza, ou de peças soltas que você monta.

> **📌 Vale gravar**
> Saber diferenciar as duas filosofias olhando um trecho de HTML é pergunta clássica. Regra prática: se as classes descrevem **o que a coisa é** (`card`, `navbar`, `btn`), é componente pronto; se descrevem **como a coisa parece** (`flex`, `p-4`, `text-xl`), é utility-first.

## 3. Como um framework chega até a página

### 3.1 CDN ou npm?

Há dois caminhos para colocar o CSS de um framework no seu projeto:

| Caminho | Como é | Quando usar |
|---|---|---|
| **CDN** | Uma tag `<link>` apontando para um servidor público | Aprendizado, protótipos, sites estáticos pequenos |
| **npm + build** | `npm install`, `import` no código, empacotador gera o CSS | Produção; permite remover o CSS não utilizado |

Nesta unidade o site é estático, sem Node e sem build — CDN é a resposta certa. A partir do Nível 3, com Vite, você instala tudo por npm.

Uma CDN (*Content Delivery Network*) é uma rede de servidores espalhados pelo mundo que devolve o arquivo a partir do ponto mais próximo de quem pediu. As duas mais usadas para pacotes JavaScript e CSS são a **jsDelivr** (`cdn.jsdelivr.net`) e a **cdnjs** (`cdnjs.cloudflare.com`); ambas servem qualquer pacote publicado no npm.

### 3.2 Fixe a versão. Sempre.

Compare estas duas URLs:

```text
https://cdn.jsdelivr.net/npm/bootstrap/dist/css/bootstrap.min.css
https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css
```

A primeira significa "me dê a versão mais recente". Parece prático e é uma armadilha: no dia em que o Bootstrap 6 sair, o seu site — que você não tocou há um ano — muda de layout sozinho, sem aviso e sem você ter feito nenhum `commit`. A segunda trava a versão. O seu site continua exatamente igual até você decidir mudar.

### 3.3 `integrity`: o que a hash protege

Ao usar CDN você está executando, no navegador dos seus usuários, um arquivo hospedado por **outra pessoa**. Se a CDN for invadida e o arquivo trocado, o site inteiro é comprometido. A defesa se chama **SRI** (*Subresource Integrity*):

```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
      rel="stylesheet"
      integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"
      crossorigin="anonymous">
```

O que acontece: o navegador baixa o arquivo, calcula o resumo criptográfico SHA-384 do conteúdo recebido e compara com o valor de `integrity`. Se um único byte for diferente, o recurso é **bloqueado** — não é aplicado, e um erro aparece no console. O `crossorigin="anonymous"` é obrigatório junto: sem ele, o navegador não consegue ler o corpo da resposta de outra origem para conferir a hash.

O que a hash **não** protege: ela não impede a CDN de saber quem visitou o seu site (cada usuário faz uma requisição para lá), nem funciona para conteúdo que muda a cada requisição. Ela garante uma coisa só, e garante bem: *o arquivo que chegou é byte a byte o que eu esperava*.

> **🔬 Investigue**
> Gere você mesmo a hash de um arquivo e prove que o número não é mágica. No terminal:
>
> ```bash
> curl -sO https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css
> openssl dgst -sha384 -binary bootstrap.min.css | openssl base64 -A
> ```
>
> A saída tem que ser exatamente `QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH`. Agora abra o arquivo baixado, acrescente um espaço no final, salve e rode o comando de novo: a hash inteira muda. Depois, no `index.html`, troque um caractere do `integrity` e recarregue: a página fica sem estilo nenhum e o console mostra *"Failed to find a valid digest in the 'integrity' attribute for resource"*. É o navegador se recusando a executar algo que não é o que você pediu.

### 3.4 A ordem no `<head>` decide quem vence

Esta é a linha que mais gera bug nesta aula:

```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"
      integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"
      crossorigin="anonymous">
<link rel="stylesheet" href="css/estilo.css">
```

O seu `estilo.css` vem **depois**. Motivo: quando dois seletores têm a mesma especificidade, a cascata do CSS dá a vitória ao que aparece por último. Se você inverter a ordem, o Bootstrap sobrescreve o seu ajuste e você vai passar meia hora achando que "o CSS não está pegando".

Isso vale só para o empate de especificidade. Se o Bootstrap usa `.navbar .nav-link` (dois seletores de classe) e você escreve `.nav-link` (um), a ordem não salva: o dele é mais específico e ganha de qualquer jeito. A saída correta nesse caso **não** é `!important` — é subir na especificidade do jeito certo ou, melhor ainda, mexer nas variáveis do framework (§4.6).

> **💡 Dica**
> No DevTools, aba **Elements** → painel **Styles**, as regras aparecem em ordem de vitória, de cima para baixo, e as declarações perdedoras aparecem **riscadas**. Quando um estilo seu não funcionar, a resposta está sempre nesse painel — não no seu editor.

## 4. Bootstrap 5.3 na prática

### 4.1 O que vem na caixa

Duas peças, e a segunda é opcional:

- `bootstrap.min.css` — o framework inteiro: reset, grid, componentes, utilitários.
- `bootstrap.bundle.min.js` — apenas o **comportamento**: menu que abre e fecha, modal, dropdown, carrossel, tooltip. O "bundle" inclui o Popper, biblioteca de posicionamento usada pelos dropdowns.

Desde a versão 5 não há dependência de jQuery — o JavaScript é nativo. Se o seu site não usa nenhum componente interativo, você pode carregar só o CSS. O Café Cerrado precisa do JS por um motivo só: a navbar que colapsa em hambúrguer.

### 4.2 O grid de 12 colunas

O coração do Bootstrap são três níveis encaixados:

```html
<div class="container">
  <div class="row">
    <div class="col-12 col-md-6 col-lg-4">Bloco 1</div>
    <div class="col-12 col-md-6 col-lg-4">Bloco 2</div>
    <div class="col-12 col-md-12 col-lg-4">Bloco 3</div>
  </div>
</div>
```

- `container` limita a largura e centraliza (existe também `container-fluid`, que ocupa 100 %).
- `row` é a linha. Ela é um `display: flex; flex-wrap: wrap`.
- `col-*` são as colunas. Doze é o total; `col-md-6` significa "metade da linha a partir de 768 px".

Leia o exemplo acima como três frases: no celular, cada bloco ocupa a linha inteira (12/12); no tablet, os dois primeiros dividem a linha e o terceiro ocupa uma linha só; no desktop, os três ficam lado a lado (4 + 4 + 4 = 12).

> **🔎 Por baixo do capô**
> Nada disso é mágico. Abra o `bootstrap.min.css`, formate o arquivo no VS Code e procure as três classes principais: é CSS comum, do tipo que você escreve desde a Aula 02.
>
> ```css
> .row {
>   --bs-gutter-x: 1.5rem;
>   display: flex;
>   flex-wrap: wrap;
>   margin-right: calc(-0.5 * var(--bs-gutter-x));
>   margin-left: calc(-0.5 * var(--bs-gutter-x));
> }
>
> .row > * {
>   flex-shrink: 0;
>   width: 100%;
>   padding-right: calc(var(--bs-gutter-x) * 0.5);
>   padding-left: calc(var(--bs-gutter-x) * 0.5);
> }
>
> .col-md-4 { flex: 0 0 auto; width: 33.33333333%; }
> ```
>
> Três coisas ficam claras: o "12 colunas" é só uma tabela de porcentagens; a calha (`gutter`) é `padding` nas colunas compensado por `margin` negativa na linha — por isso uma `col-*` fora de uma `row` fica com um espaço estranho na borda; e a largura padrão de qualquer filho direto de `.row` é 100 %, o que explica por que uma coluna sem `col-md-*` ocupa a linha toda no celular sem você escrever nada.

### 4.3 Os breakpoints

| Faixa | Prefixo | Largura mínima |
|---|---|---|
| Extra small (celular) | nenhum | 0 |
| Small (celular deitado) | `sm` | 576 px |
| Medium (tablet) | `md` | 768 px |
| Large (notebook) | `lg` | 992 px |
| Extra large (monitor) | `xl` / `xxl` | 1200 px / 1400 px |

O Bootstrap é **mobile-first**: `col-md-6` quer dizer "6 colunas **a partir de** 768 px", e não "apenas em 768 px". Abaixo disso vale o que você declarou para telas menores, ou o padrão (largura total). É por isso que se escreve `col-12 col-md-6` e nunca o contrário.

Existe um atalho para grades regulares:

```html
<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
  <div class="col">Card 1</div>
  <div class="col">Card 2</div>
  <div class="col">Card 3</div>
</div>
```

`row-cols-lg-3` diz "três colunas por linha a partir de 992 px", e cada filho é só `col`. Menos repetição, e para acrescentar um quarto card você não precisa recalcular nada. O `g-4` é o espaçamento entre as células (a calha).

### 4.4 Os utilitários que você vai usar todo dia

O sistema de espaçamento é o mais importante e segue um padrão: `{propriedade}{lado}-{tamanho}`.

| Peça | Valores | Exemplo |
|---|---|---|
| Propriedade | `m` (margin), `p` (padding) | `m`, `p` |
| Lado | `t` `b` `s` `e` `x` `y`, ou nada | `mt`, `px`, `me` |
| Tamanho | `0`=0, `1`=.25rem, `2`=.5rem, `3`=1rem, `4`=1.5rem, `5`=3rem | `mt-3`, `py-5` |

O `s` é *start* e o `e` é *end* — não *left* e *right*. Isso existe para que o mesmo CSS funcione em idiomas escritos da direita para a esquerda, como o árabe. `ms-auto` significa "margem automática do lado inicial", o truque clássico para empurrar um bloco para a direita dentro de um flex.

Outros que aparecem no projeto de hoje:

```html
<div class="d-flex align-items-center justify-content-between gap-3">Flexbox pronto</div>
<p class="text-center text-body-secondary">Texto centralizado e apagado</p>
<img src="img/fachada.jpg" alt="Fachada da cafeteria" class="img-fluid rounded-3">
<span class="badge text-bg-success">Sem glúten</span>
<span class="visually-hidden">Texto só para leitor de tela</span>
```

`img-fluid` é `max-width: 100%; height: auto` — a linha que impede toda imagem de estourar a tela do celular.

### 4.5 Os componentes que o Café Cerrado precisa

**Navbar** — o único componente com JavaScript no projeto:

```html
<nav class="navbar navbar-expand-lg" aria-label="Navegação principal">
  <div class="container">
    <a class="navbar-brand" href="index.html">Café Cerrado</a>
    <button class="navbar-toggler" type="button"
            data-bs-toggle="collapse" data-bs-target="#menu-principal"
            aria-controls="menu-principal" aria-expanded="false"
            aria-label="Abrir e fechar o menu de navegação">
      <span class="navbar-toggler-icon" aria-hidden="true"></span>
    </button>
    <div class="collapse navbar-collapse" id="menu-principal">
      <ul class="navbar-nav ms-auto">
        <li class="nav-item"><a class="nav-link" href="index.html" aria-current="page">Início</a></li>
        <li class="nav-item"><a class="nav-link" href="cardapio.html">Cardápio</a></li>
      </ul>
    </div>
  </div>
</nav>
```

`navbar-expand-lg` diz: menu horizontal a partir de 992 px, hambúrguer abaixo disso. O par `data-bs-toggle`/`data-bs-target` liga o botão ao bloco `#menu-principal` — é o JavaScript do Bootstrap lendo esses atributos. Os atributos ARIA (`aria-controls`, `aria-expanded`, `aria-label`) você já escreve hoje; **por que** cada um é obrigatório, você disseca na Aula 06.

**Card** — a caixa que vai substituir os `.produto` da Aula 03:

```html
<article class="card h-100">
  <img src="img/espresso.jpg" class="card-img-top" alt="Xícara de espresso sobre a mesa de madeira">
  <div class="card-body">
    <h3 class="h5 card-title">Espresso do Cerrado</h3>
    <p class="card-text">Grãos de Alto Paraíso, torra média, corpo encorpado e final achocolatado.</p>
  </div>
  <div class="card-footer">R$ 6,00</div>
</article>
```

Repare no `h5` junto do `h3`: a **tag** define a hierarquia do documento (e é `h3` porque está dentro de uma seção com `h2`); a **classe** define só o tamanho visual. Nunca escolha a tag pelo tamanho da fonte. E `h-100` faz o card ocupar toda a altura da célula do grid, para que uma fileira de cards fique alinhada mesmo com textos de tamanhos diferentes.

**Formulário** — três classes resolvem quase tudo:

```html
<div class="mb-3">
  <label for="nome" class="form-label">Nome completo *</label>
  <input type="text" id="nome" name="nome" class="form-control" required minlength="3">
  <div class="form-text">Como você quer ser chamado no atendimento.</div>
</div>

<div class="form-check">
  <input type="checkbox" id="novidades" name="novidades" value="sim" class="form-check-input">
  <label for="novidades" class="form-check-label">Quero receber avisos de novos lotes</label>
</div>
```

`form-control` para `input`, `textarea` e afins; `form-select` para `select`; `form-check` + `form-check-input` + `form-check-label` para caixas e rádios.

> **⚠️ Atenção**
> O Bootstrap tem um sistema próprio de validação visual (`needs-validation`, `was-validated`, `is-invalid`) que **depende de JavaScript autoral** para funcionar. Nesta unidade o único JavaScript permitido é o do framework, então continuamos com a validação nativa da Aula 03 e marcamos o campo errado com `:user-invalid`, que é CSS puro. Na Unidade 2, quando o `js/app.js` existir, você troca por `is-invalid` e mensagens próprias.

### 4.6 Personalizar sem brigar: as variáveis `--bs-*`

Esta é a parte que separa quem usa Bootstrap de quem apanha do Bootstrap. Na versão 5.3 quase tudo é controlado por variáveis CSS, em dois níveis.

**Nível global**, no `:root` — cores e tipografia do documento inteiro:

```css
:root {
  --bs-body-bg: #fdfaf6;
  --bs-body-color: #2b2118;
  --bs-link-color-rgb: 111, 78, 55;
}
```

Repare que a cor do link é declarada como **três números**, não como `#6f4e37`. O Bootstrap guarda as cores nesse formato para poder montar `rgba(var(--bs-link-color-rgb), var(--bs-link-opacity, 1))` e oferecer utilitários de opacidade como `link-opacity-50`. Se você escrever `--bs-link-color-rgb: #6f4e37`, o `rgba()` recebe lixo e o link fica preto.

**Nível de componente**, na classe — cada componente lê o próprio conjunto de variáveis:

```css
.btn-cafe {
  --bs-btn-bg: #6f4e37;
  --bs-btn-border-color: #6f4e37;
  --bs-btn-color: #ffffff;
  --bs-btn-hover-bg: #4a3325;
  --bs-btn-hover-border-color: #4a3325;
  --bs-btn-hover-color: #ffffff;
}
```

Isso cria uma variante de botão nova, do mesmo jeito que o `btn-primary` é criado internamente — sem sobrescrever nada, sem `!important` e sem risco de quebrar outro botão da página. É o caminho oficial e é o que o Café Cerrado vai usar.

Um erro comum: achar que `--bs-primary: #6f4e37` no `:root` recolore os botões. Não recolore. `--bs-primary` alimenta utilitários como `.text-primary` e `.bg-primary`; os botões leem `--bs-btn-*`. Cada componente tem o seu prefixo (`--bs-card-*`, `--bs-navbar-*`, `--bs-nav-*`), e a lista completa está na documentação de cada um.

A versão 5.3 também trouxe o atributo `data-bs-theme`, que troca o conjunto inteiro de cores de qualquer subárvore:

```html
<body data-bs-theme="dark">
  <p>A página inteira em modo escuro, sem uma linha de CSS.</p>
</body>
```

Funciona em qualquer elemento, não só no `<body>` — dá para ter um card claro dentro de uma página escura.

## 5. Tailwind CSS 4 — utility-first em vinte minutos

### 5.1 Experimentando no navegador

O Tailwind de verdade é uma ferramenta de build: ela varre o seu HTML, descobre quais classes você usou e gera um CSS só com elas. Para **estudar**, existe uma versão que faz isso no próprio navegador:

**`experimentos/tailwind.html`**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Experimento com Tailwind 4</title>
  <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
<body class="bg-stone-100 p-8">

  <div class="max-w-sm overflow-hidden rounded-xl bg-white shadow-lg">
    <img class="h-48 w-full object-cover" src="../img/espresso.jpg"
         alt="Xícara de espresso sobre a mesa de madeira">
    <div class="p-6">
      <h2 class="mb-2 text-xl font-bold text-stone-800">Espresso do Cerrado</h2>
      <p class="mb-4 text-stone-600">Grãos de Alto Paraíso, torra média, final achocolatado.</p>
      <a href="#"
         class="inline-block rounded-lg bg-amber-800 px-4 py-2 font-semibold text-white hover:bg-amber-900">
        Ver detalhes
      </a>
    </div>
  </div>

</body>
</html>
```

Compare com o card do Bootstrap da §4.5: mesmo resultado visual, filosofias opostas. O card Bootstrap tem oito classes, todas com nome de coisa (`card`, `card-body`, `card-title`), e carrega um CSS de 230 KB; o card Tailwind tem mais de vinte classes, todas com nome de propriedade, e depois do build gera um CSS de poucos KB.

> **⚠️ Atenção**
> Este script é o **Play CDN**: ele carrega o compilador do Tailwind no navegador e monta o CSS na hora. Serve para aprender e prototipar, e é o que usamos aqui. Em produção ele é lento e pesado — o Tailwind de verdade se instala com `npm install tailwindcss` e roda no build. O endereço `cdn.tailwindcss.com`, que você vai achar em tutoriais antigos, é do Tailwind 3: para a versão 4 o pacote é `@tailwindcss/browser@4`, servido pela jsDelivr.

### 5.2 Responsividade e estados por prefixo

No Tailwind não existe media query no seu código: existe prefixo.

```html
<div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
  <div class="rounded-lg bg-white p-4">Card 1</div>
  <div class="rounded-lg bg-white p-4">Card 2</div>
  <div class="rounded-lg bg-white p-4">Card 3</div>
</div>
```

`md:grid-cols-2` é "duas colunas a partir de 768 px" — mesma lógica mobile-first do Bootstrap, sintaxe diferente. O mesmo mecanismo vale para estados e para preferências do usuário:

```html
<button class="bg-amber-800 hover:bg-amber-900 focus-visible:outline-2 dark:bg-amber-600">
  Composição de estados
</button>
```

`hover:`, `focus:`, `focus-visible:`, `disabled:`, `dark:`, `motion-reduce:` — e eles se combinam (`md:hover:bg-amber-900`). É essa composição que torna o Tailwind poderoso e o HTML comprido ao mesmo tempo.

### 5.3 O que mudou na versão 4

A versão 4 (2025) reescreveu o motor e mudou a configuração de lugar: o antigo arquivo `tailwind.config.js` deu lugar a **configuração dentro do próprio CSS**.

```css
@import "tailwindcss";

@theme {
  --color-cafe: #6f4e37;
  --color-cafe-escuro: #4a3325;
}
```

Declarar `--color-cafe` no bloco `@theme` cria automaticamente as classes `bg-cafe`, `text-cafe`, `border-cafe` e todas as variantes. No Play CDN você faz o mesmo dentro de uma tag de estilo especial:

```html
<style type="text/tailwindcss">
  @theme {
    --color-cafe: #6f4e37;
  }
</style>
```

E aí `class="bg-cafe"` funciona. É a mesma ideia das variáveis `--bs-*` do Bootstrap, vista pelo outro lado: em vez de sobrescrever os tokens de um design pronto, você **declara** os tokens do seu design e o framework gera as classes.

## 6. Material Design e o Material Web

### 6.1 Um design system, várias implementações

O Material Design é a linguagem visual que o Google publicou em 2014 e usa no Android, no Gmail e no Drive. Ele não é um arquivo CSS: é uma especificação — superfícies em camadas com elevação, cores derivadas de uma cor-semente, movimento com significado, um botão flutuante de ação. A versão atual é a **Material 3**, documentada em `m3.material.io`.

Para usar Material Design em HTML puro existem dois caminhos, e é importante não confundir:

| Caminho | O que é | Situação |
|---|---|---|
| Materialize | Framework de componentes de terceiros, estilo Bootstrap | Última versão estável de 2018, implementa o Material 1 |
| Material Web | Implementação **oficial** do Google em Web Components | Material 3; em modo de manutenção desde 2024 |

Muito material de aula ainda ensina o Materialize porque ele se parece com o Bootstrap. Nesta trilha usamos o **Material Web**, porque ele mostra uma terceira ideia que os outros dois frameworks não mostram: componentes como **elementos HTML próprios**.

### 6.2 Web Components: tags que não existem no HTML

Um Web Component é um elemento customizado, registrado por JavaScript, que o navegador passa a tratar como uma tag nativa — com estilo encapsulado dentro de um *shadow DOM*, isolado do CSS da página. Você não escreve `<button class="md-button">`: você escreve `<md-filled-button>`.

**`experimentos/material.html`**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Experimento com Material Web</title>

  <link rel="stylesheet"
        href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap">

  <script type="importmap">
    {
      "imports": {
        "@material/web/": "https://esm.run/@material/web@2.5.0/"
      }
    }
  </script>

  <script type="module">
    import '@material/web/all.js';
    import { styles as typescaleStyles } from '@material/web/typography/md-typescale-styles.js';
    document.adoptedStyleSheets.push(typescaleStyles.styleSheet);
  </script>

  <style>
    :root { --md-sys-color-primary: #6f4e37; --md-sys-color-on-primary: #ffffff; }
    body { font-family: Roboto, system-ui, sans-serif; margin: 0; padding: 2rem;
           display: flex; flex-direction: column; gap: 1.5rem; max-width: 24rem; }
  </style>
</head>
<body>

  <h1 class="md-typescale-headline-medium">Reserve sua mesa</h1>

  <md-outlined-text-field label="Nome completo" required></md-outlined-text-field>
  <md-outlined-text-field label="E-mail" type="email" required></md-outlined-text-field>

  <label>
    <md-checkbox touch-target="wrapper"></md-checkbox>
    Quero receber avisos de novos lotes
  </label>

  <div>
    <md-filled-button>Enviar</md-filled-button>
    <md-text-button>Cancelar</md-text-button>
  </div>

</body>
</html>
```

Três mecanismos novos aparecem aqui, e vale entender cada um:

- **`<script type="importmap">`** é um recurso nativo do navegador que traduz nomes de pacote em URLs. Sem ele, o `import '@material/web/all.js'` não teria como saber onde procurar o arquivo. O `esm.run` é o serviço da jsDelivr que entrega pacotes npm já no formato de módulo ES.
- **`type="module"`** é obrigatório: `import` só existe em módulos ES. É a mesma sintaxe que você vai usar na Unidade 2 e no Nível 3.
- **`--md-sys-color-primary`** é um *design token* do Material 3. Todos os componentes leem a mesma paleta de tokens, então trocar duas variáveis recolore a interface inteira — exatamente a ideia das variáveis `--bs-*`, com outro nome.

### 6.3 Por que este não é o caminho do Café Cerrado

Material Web é elegante e é o futuro anunciado dos componentes web, mas tem três características que pesam contra ele na Unidade 1:

1. **Depende de JavaScript para tudo.** Se o script não carregar, `<md-filled-button>` fica sendo uma tag desconhecida e some da tela. Um site Bootstrap sem JavaScript perde o menu hambúrguer; um site Material Web sem JavaScript perde tudo.
2. **Não tem sistema de grid.** Ele entrega componentes, não layout. Você teria que escrever o grid à mão com CSS Grid — que é ótimo, mas não é o que o Marco 1 pede ("sistema de grid do framework").
3. **Identidade visual muito forte.** Um site com Material Web parece um app do Google. Para uma cafeteria de Sinop, isso é uma escolha, não um padrão.

> **🧠 Você sabia?**
> Em 2024 o Google anunciou que a equipe do Material Web foi realocada e que o projeto entrou em **modo de manutenção**: correções de segurança continuam, mas novos componentes não vêm. O card, por exemplo, nunca saiu da pasta `labs`. Isso é um lembrete útil para toda escolha de dependência: você não está escolhendo só uma sintaxe, está escolhendo quem vai manter aquele código nos próximos cinco anos. A pergunta "quando foi o último commit?" e "quantas pessoas mantêm isso?" vale tanto quanto "que bonito ficou o botão".

## 7. Escolhendo com critério

### 7.1 A matriz de decisão

| Critério | Bootstrap 5.3 | Tailwind 4 | Material Web 2 |
|---|---|---|---|
| Filosofia | Componentes prontos | Classes utilitárias | Web Components |
| Curva inicial | Baixa | Média | Média |
| Grid | 12 colunas, pronto | Utilitários de grid/flex | Não tem |
| Liberdade visual | Média (`--bs-*`) | Total | Baixa (estética Google) |
| Funciona sem build | Sim, por CDN | Só para estudo | Sim, por importmap |
| Funciona sem JavaScript | Quase tudo | Sim | Não |
| Oferece hash SRI | Sim | Não | Não |

A última linha merece atenção: o Bootstrap publica o `integrity` de cada arquivo na própria documentação. O Play CDN do Tailwind e o `esm.run` do Material Web **não** publicam hash — o primeiro porque o conteúdo é gerado, o segundo porque um módulo ES importa outros arquivos que a hash da primeira requisição não cobre. Isso reforça o que a §5.1 e a §6.3 já diziam: os dois entram no projeto como experimento, não como dependência de produção.

### 7.2 Meça, não ache

"O Bootstrap é pesado" é uma frase que se repete sem número. Números você tira da aba **Network** do DevTools em trinta segundos: abra a página, recarregue com <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>R</kbd>, ordene por **Size** e leia a coluna **Transferred** (o que veio pela rede, comprimido) ao lado da coluna de tamanho real. O CSS do Bootstrap 5.3 completo transfere cerca de 32 KB comprimidos; o `bundle` de JavaScript, cerca de 25 KB. Uma única foto de café mal exportada pesa mais que os dois juntos — e é aí que quase sempre está o problema real de desempenho do site de um aluno.

### 7.3 A regra de ouro

> **⚠️ Atenção**
> **Um framework por projeto.** Misturar Bootstrap e Materialize, ou Bootstrap e Tailwind, gera três problemas de uma vez: classes com o mesmo nome e comportamentos diferentes (`.card`, `.btn`, `.container` existem em quase todos), CSS duplicado baixado à toa, e um visual sem identidade. Se você quiser trocar de framework no meio do projeto, troque — mas remova o anterior por inteiro.

### 7.4 A escolha do Café Cerrado

O Café Cerrado adota o **Bootstrap 5.3**. A justificativa, que vai literalmente para o `README.md`, tem quatro pontos:

1. O projeto é um site estático, sem etapa de build — e o Bootstrap é o único dos três que entrega grid **e** componentes por CDN, sem npm.
2. O critério "framework CSS" do Marco 1 pede um sistema de grid responsivo; o de 12 colunas é o mais direto e o mais documentado em português.
3. Uma cafeteria de bairro precisa de menu, cards e formulário bem-resolvidos, não de um design autoral disputando prêmio — a curva baixa vale mais que a liberdade total.
4. As variáveis `--bs-*` da versão 5.3 permitem aplicar a paleta da marca sem lutar contra o framework, o que responde à principal crítica ao Bootstrap ("todo site fica igual").

Seu projeto autoral **pode escolher outro**. O que o marco exige não é a escolha, é a **justificativa** e a aplicação consistente.

## 💻 Mão na massa — O Café Cerrado adota o Bootstrap 5.3

Nove passos. Ao final, as três páginas da Aula 03 continuam com exatamente a mesma estrutura semântica, mas responsivas, com menu que colapsa, cardápio em grid de cards e formulário consistente — e com um `css/estilo.css` três vezes menor do que ontem.

### Passo 1 — Carregar o framework nas três páginas

Em `index.html`, `cardapio.html` e `contato.html`, o `<head>` fica assim (só o `<title>` e a `description` mudam entre elas):

**`cafe-cerrado/index.html`**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Café Cerrado: torrefação artesanal de grãos do Cerrado mato-grossense em Sinop, MT.">
  <title>Café Cerrado — Torrefação artesanal em Sinop, MT</title>

  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
        rel="stylesheet"
        integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"
        crossorigin="anonymous">

  <link rel="stylesheet" href="css/estilo.css">
</head>
```

E, nas três páginas, a última linha antes de `</body>`:

**`cafe-cerrado/index.html`** (fim do arquivo)

```html
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
          integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz"
          crossorigin="anonymous"></script>
</body>
</html>
```

O script vai no **fim** do `<body>` por dois motivos: um `<script>` no `<head>` sem `defer` bloqueia a renderização enquanto baixa e executa, e os componentes que leem o DOM ao inicializar já encontram a página inteira montada. Salve e recarregue: a página muda de fonte e de espaçamento na hora. Ela ainda está feia — é o reset do Bootstrap desmanchando o seu CSS antigo. Os próximos passos arrumam isso.

### Passo 2 — A navbar responsiva

Substitua o `<header>` inteiro das três páginas por este bloco. Ele é idêntico nas três; só muda em qual link fica o `aria-current="page"`.

**`cafe-cerrado/index.html`** (o `<header>` completo)

```html
<header>
  <nav class="navbar navbar-expand-lg" aria-label="Navegação principal">
    <div class="container">
      <a class="navbar-brand" href="index.html">
        Café Cerrado
        <span class="d-block small fw-normal opacity-75">Torrefação artesanal · Sinop, MT</span>
      </a>

      <button class="navbar-toggler" type="button"
              data-bs-toggle="collapse" data-bs-target="#menu-principal"
              aria-controls="menu-principal" aria-expanded="false"
              aria-label="Abrir e fechar o menu de navegação">
        <span class="navbar-toggler-icon" aria-hidden="true"></span>
      </button>

      <div class="collapse navbar-collapse" id="menu-principal">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <a class="nav-link" href="index.html" aria-current="page">Início</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="cardapio.html">Cardápio</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="contato.html">Contato</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</header>
```

Em `cardapio.html`, o `aria-current="page"` vai para o link do Cardápio; em `contato.html`, para o de Contato. O `<nav>` continua dentro do `<header>`: a semântica da Aula 03 não muda.

### Passo 3 — `index.html`: hero, história, destaques e horários

Substitua o `<main>` da página inicial:

**`cafe-cerrado/index.html`** (conteúdo do `<main>`)

```html
<main>
  <section class="hero text-center py-5">
    <div class="container">
      <h1 class="hero__titulo display-4">Café do Cerrado, torrado em Sinop</h1>
      <p class="hero__texto lead">
        Grãos de produtores de Mato Grosso, torra artesanal e um lugar para ficar.
      </p>
      <div class="hero__acoes">
        <a class="btn btn-cafe btn-lg" href="cardapio.html">Ver o cardápio</a>
      </div>
    </div>
  </section>

  <section id="sobre" class="container py-5">
    <div class="row align-items-center g-4">
      <div class="col-12 col-md-6">
        <h2>Nossa história</h2>
        <p>
          O Café Cerrado nasceu em uma garagem no Setor Comercial de Sinop, com um
          torrador de dois quilos e a teimosia de provar que o café produzido no
          Mato Grosso pode brigar com os grãos mais famosos do país.
        </p>
        <p>
          Hoje trabalhamos com quatro sítios parceiros e torramos, em média,
          sessenta quilos por semana — tudo consumido aqui mesmo, no balcão ou nas
          mesas da calçada.
        </p>
        <ul class="list-unstyled">
          <li>Wi-Fi liberado e tomada em todas as mesas</li>
          <li>Moagem na hora, com escolha da torra</li>
          <li>Opções sem lactose e sem glúten identificadas no cardápio</li>
        </ul>
      </div>

      <div class="col-12 col-md-6">
        <img src="img/fachada.jpg" class="img-fluid rounded-3 shadow-sm"
             alt="Fachada do Café Cerrado com toldo verde e mesas na calçada"
             width="1200" height="800">
      </div>
    </div>
  </section>

  <section id="destaques" class="container py-5">
    <h2 class="mb-4">Destaques da semana</h2>

    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
      <div class="col">
        <article class="card card-produto h-100">
          <div class="card-body">
            <h3 class="h5 card-title">Cold Brew da Chapada</h3>
            <p class="card-text">Extração a frio por dezoito horas, servido com gelo e rodela de laranja.</p>
          </div>
          <div class="card-footer d-flex justify-content-between align-items-center">
            <span class="fw-bold">R$ 15,00</span>
            <a class="btn btn-sm btn-cafe-vazado" href="cardapio.html#geladas">Ver</a>
          </div>
        </article>
      </div>

      <div class="col">
        <article class="card card-produto h-100">
          <div class="card-body">
            <h3 class="h5 card-title">Pão de Queijo Mineiro</h3>
            <p class="card-text">Massa de polvilho azedo com queijo canastra, assado de hora em hora.</p>
          </div>
          <div class="card-footer d-flex justify-content-between align-items-center">
            <span class="fw-bold">R$ 7,00</span>
            <a class="btn btn-sm btn-cafe-vazado" href="cardapio.html#salgados">Ver</a>
          </div>
        </article>
      </div>

      <div class="col">
        <article class="card card-produto h-100">
          <div class="card-body">
            <h3 class="h5 card-title">Bolo de Milho Verde</h3>
            <p class="card-text">Fatia de bolo cremoso feito com milho da feira do produtor.</p>
          </div>
          <div class="card-footer d-flex justify-content-between align-items-center">
            <span class="fw-bold">R$ 9,50</span>
            <a class="btn btn-sm btn-cafe-vazado" href="cardapio.html#doces">Ver</a>
          </div>
        </article>
      </div>
    </div>
  </section>

  <section id="horarios" class="container py-5">
    <h2 class="mb-4">Horário de atendimento</h2>

    <div class="table-responsive">
      <table class="table table-striped align-middle caption-top">
        <caption>Horário de atendimento do Café Cerrado</caption>
        <thead>
          <tr>
            <th scope="col">Dia</th>
            <th scope="col">Abertura</th>
            <th scope="col">Fechamento</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <th scope="row">Segunda a sexta</th>
            <td>07h00</td>
            <td>20h00</td>
          </tr>
          <tr>
            <th scope="row">Sábado</th>
            <td>08h00</td>
            <td>18h00</td>
          </tr>
          <tr>
            <th scope="row">Domingo</th>
            <td colspan="2">Fechado</td>
          </tr>
        </tbody>
      </table>
    </div>

    <p>
      Precisa de um horário fora do expediente para um evento?
      <a href="contato.html">Fale com a gente pelo formulário de contato</a>.
    </p>
  </section>
</main>
```

Três decisões para reparar:

- O `container` saiu do `<main>` e entrou em **cada seção**. Isso permite que uma seção futura ocupe a largura toda da tela (uma faixa colorida, por exemplo) sem quebrar o alinhamento das outras.
- `row-cols-1 row-cols-md-2 row-cols-lg-3` faz o trabalho de três media queries. Acrescente um quarto destaque e nada precisa ser recalculado.
- `table-responsive` substitui o `.tabela-rolavel` que você escreveu à mão na Aula 03: é a mesma ideia (`overflow-x: auto`), já pronta. Pode apagar a sua.

### Passo 4 — `cardapio.html`: dez produtos em grid

Cada categoria vira uma `<section>` com um grid próprio, e as quatro âncoras da Aula 03 (`#cafes`, `#geladas`, `#salgados`, `#doces`) continuam sendo os `id` das seções — é para elas que apontam os botões "Ver" dos destaques e a `<nav>` de atalhos. São os mesmos dez produtos da Aula 03, com os mesmos preços.

**`cafe-cerrado/cardapio.html`** (o `<main>` inteiro)

```html
<main>
  <section class="container pt-5">
    <h1>Cardápio</h1>
    <p class="lead">
      Preços válidos para consumo no local. Todos os cafés podem ser preparados
      com leite vegetal por R$ 2,00 adicionais.
    </p>

    <nav aria-label="Seções do cardápio">
      <ul class="nav gap-2">
        <li class="nav-item"><a class="btn btn-sm btn-cafe-vazado" href="#cafes">Cafés</a></li>
        <li class="nav-item"><a class="btn btn-sm btn-cafe-vazado" href="#geladas">Bebidas geladas</a></li>
        <li class="nav-item"><a class="btn btn-sm btn-cafe-vazado" href="#salgados">Salgados</a></li>
        <li class="nav-item"><a class="btn btn-sm btn-cafe-vazado" href="#doces">Doces</a></li>
        <li class="nav-item"><a class="btn btn-sm btn-cafe-vazado" href="#torras">Guia de torras</a></li>
      </ul>
    </nav>
  </section>

  <section id="cafes" class="container py-5">
    <h2 class="mb-4">Cafés</h2>

    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
    <div class="col">
      <article class="card card-produto h-100">
        <img src="img/espresso.jpg" class="card-img-top"
             alt="Xícara de espresso sobre a mesa de madeira">
        <div class="card-body">
          <h3 class="h5 card-title">Espresso do Cerrado</h3>
          <p class="card-text">
            Grãos de Alto Paraíso, torra média, corpo encorpado e final achocolatado.
          </p>
        </div>
        <div class="card-footer d-flex justify-content-between align-items-center">
          <span class="fw-bold">R$ 6,00</span>
          <span class="badge text-bg-secondary">Torra média</span>
        </div>
      </article>
    </div>

    <div class="col">
      <article class="card card-produto h-100">
        <img src="img/coado.jpg" class="card-img-top"
             alt="Café sendo coado em filtro de papel sobre uma jarra de vidro">
        <div class="card-body">
          <h3 class="h5 card-title">Coado da Casa</h3>
          <p class="card-text">
            Duzentos mililitros em coador de papel, moagem média feita na hora do pedido.
          </p>
        </div>
        <div class="card-footer d-flex justify-content-between align-items-center">
          <span class="fw-bold">R$ 8,50</span>
          <span class="badge text-bg-secondary">Torra clara</span>
        </div>
      </article>
    </div>

    <div class="col">
      <article class="card card-produto h-100">
        <img src="img/cappuccino.jpg" class="card-img-top"
             alt="Cappuccino com canela polvilhada sobre a espuma">
        <div class="card-body">
          <h3 class="h5 card-title">Cappuccino Sinop</h3>
          <p class="card-text">
            Espresso duplo, leite vaporizado e canela do Cerrado por cima.
          </p>
        </div>
        <div class="card-footer d-flex justify-content-between align-items-center">
          <span class="fw-bold">R$ 12,00</span>
          <span class="badge text-bg-secondary">Com leite</span>
        </div>
      </article>
    </div>

    <div class="col">
      <article class="card card-produto h-100">
        <img src="img/latte.jpg" class="card-img-top"
             alt="Copo de latte com camadas de leite e café visíveis">
        <div class="card-body">
          <h3 class="h5 card-title">Latte de Baunilha</h3>
          <p class="card-text">
            Espresso, leite vaporizado e calda de baunilha feita na casa.
          </p>
        </div>
        <div class="card-footer d-flex justify-content-between align-items-center">
          <span class="fw-bold">R$ 14,00</span>
          <span class="badge text-bg-secondary">Com leite</span>
        </div>
      </article>
    </div>
    </div>
  </section>

  <section id="geladas" class="container py-5">
    <h2 class="mb-4">Bebidas geladas</h2>

    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
    <div class="col">
      <article class="card card-produto h-100">
        <img src="img/cold-brew.jpg" class="card-img-top"
             alt="Copo alto de cold brew com gelo e rodela de laranja">
        <div class="card-body">
          <h3 class="h5 card-title">Cold Brew da Chapada</h3>
          <p class="card-text">
            Extração a frio por dezoito horas, servida com gelo e rodela de laranja.
          </p>
        </div>
        <div class="card-footer d-flex justify-content-between align-items-center">
          <span class="fw-bold">R$ 15,00</span>
          <span class="badge text-bg-secondary">Gelado</span>
        </div>
      </article>
    </div>

    <div class="col">
      <article class="card card-produto h-100">
        <img src="img/frappe.jpg" class="card-img-top"
             alt="Frappê de café coberto com chantili em copo de vidro">
        <div class="card-body">
          <h3 class="h5 card-title">Frappê de Café</h3>
          <p class="card-text">
            Espresso batido com gelo, leite e chantili. Também sai sem lactose.
          </p>
        </div>
        <div class="card-footer d-flex justify-content-between align-items-center">
          <span class="fw-bold">R$ 16,00</span>
          <span class="badge text-bg-secondary">Gelado</span>
        </div>
      </article>
    </div>
    </div>
  </section>

  <section id="salgados" class="container py-5">
    <h2 class="mb-4">Salgados</h2>

    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
    <div class="col">
      <article class="card card-produto h-100">
        <img src="img/pao-de-queijo.jpg" class="card-img-top"
             alt="Porção de pães de queijo dourados em um prato branco">
        <div class="card-body">
          <h3 class="h5 card-title">Pão de Queijo Mineiro</h3>
          <p class="card-text">
            Porção com quatro unidades de polvilho azedo com queijo canastra.
          </p>
        </div>
        <div class="card-footer d-flex justify-content-between align-items-center">
          <span class="fw-bold">R$ 7,00</span>
          <span class="badge text-bg-secondary">Sem glúten</span>
        </div>
      </article>
    </div>

    <div class="col">
      <article class="card card-produto h-100">
        <img src="img/torta-de-frango.jpg" class="card-img-top"
             alt="Fatia de torta de frango em um prato de cerâmica">
        <div class="card-body">
          <h3 class="h5 card-title">Torta de Frango</h3>
          <p class="card-text">
            Fatia generosa com massa amanteigada e recheio de frango desfiado.
          </p>
        </div>
        <div class="card-footer d-flex justify-content-between align-items-center">
          <span class="fw-bold">R$ 13,00</span>
          <span class="badge text-bg-secondary">Assado do dia</span>
        </div>
      </article>
    </div>
    </div>
  </section>

  <section id="doces" class="container py-5">
    <h2 class="mb-4">Doces</h2>

    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
    <div class="col">
      <article class="card card-produto h-100">
        <img src="img/bolo-de-milho.jpg" class="card-img-top"
             alt="Fatia de bolo de milho verde sobre papel manteiga">
        <div class="card-body">
          <h3 class="h5 card-title">Bolo de Milho Verde</h3>
          <p class="card-text">
            Fatia de bolo cremoso feito com milho da feira do produtor.
          </p>
        </div>
        <div class="card-footer d-flex justify-content-between align-items-center">
          <span class="fw-bold">R$ 9,50</span>
          <span class="badge text-bg-secondary">Feito na casa</span>
        </div>
      </article>
    </div>

    <div class="col">
      <article class="card card-produto h-100">
        <img src="img/brownie.jpg" class="card-img-top"
             alt="Brownie de chocolate com castanhas por cima">
        <div class="card-body">
          <h3 class="h5 card-title">Brownie de Castanha</h3>
          <p class="card-text">
            Chocolate meio amargo com castanha-do-pará. Sem glúten.
          </p>
        </div>
        <div class="card-footer d-flex justify-content-between align-items-center">
          <span class="fw-bold">R$ 11,00</span>
          <span class="badge text-bg-secondary">Sem glúten</span>
        </div>
      </article>
    </div>
    </div>
  </section>
</main>
```

Guarde esta lista: são **os** dez produtos do Café Cerrado, com estes nomes, estes preços, estas quatro categorias e estes arquivos de imagem. Eles voltam na Aula 07 como um array de objetos, na Aula 09 como `js/dados.js`, na Aula 10 como `data/produtos.json` e na Unidade 3 como as linhas da sua API. Mudar um preço aqui obriga a mudar em todos os outros lugares — por isso não mude.

Não tem foto de cada produto? Duas saídas honestas: fotografe com o celular (uma xícara, uma mesa, luz de janela — leva dez minutos) ou remova a tag `<img>` do card, como nos destaques da página inicial. **Não** use uma imagem qualquer da internet: além do problema de direito autoral, você vai carregar 3 MB por card.

Mantenha, logo abaixo dos grids, a `<figure>` do guia de torras e a tabela de grãos da Aula 03 dentro de uma `<section id="torras" class="container py-5">` — só acrescente `class="table table-striped caption-top"` na tabela e envolva-a em `<div class="table-responsive">`, como você fez na página inicial.

### Passo 5 — `contato.html`: o formulário com classes do Bootstrap

A estrutura do formulário não muda: **os mesmos treze campos** da Aula 03, com os mesmos `name`, os mesmos `<optgroup>` e a mesma validação nativa. O que muda são as classes e a troca dos `<p class="campo">` por `<div class="mb-3">`. Nenhum campo pode desaparecer — o requisito 5 do Marco 1 cobra o formulário completo.

**`cafe-cerrado/contato.html`** (trecho do `<main>`)

```html
<main class="container py-5">
  <h1>Fale com a gente</h1>
  <p class="lead">
    Reservas para grupos, encomendas, eventos e parcerias. Respondemos em até um
    dia útil. Campos marcados com asterisco são obrigatórios.
  </p>

  <form class="row g-4" action="contato.html" method="post">
    <fieldset class="col-12 col-lg-6">
      <legend class="h5">Seus dados</legend>

      <div class="mb-3">
        <label for="nome" class="form-label">Nome completo *</label>
        <input type="text" id="nome" name="nome" class="form-control"
               required minlength="3" maxlength="80"
               autocomplete="name" placeholder="Ana Beatriz Souza">
      </div>

      <div class="mb-3">
        <label for="email" class="form-label">E-mail *</label>
        <input type="email" id="email" name="email" class="form-control"
               required autocomplete="email" placeholder="voce@exemplo.com">
      </div>

      <div class="mb-3">
        <label for="telefone" class="form-label">Telefone com DDD</label>
        <input type="tel" id="telefone" name="telefone" class="form-control"
               pattern="\(?[0-9]{2}\)?\s?9?[0-9]{4}-?[0-9]{4}"
               title="Digite o telefone com DDD, no formato (66) 99999-0000"
               inputmode="tel" autocomplete="tel" placeholder="(66) 99999-0000">
        <div class="form-text">Só usamos para confirmar reservas.</div>
      </div>

      <div class="mb-3">
        <label for="cep" class="form-label">CEP</label>
        <input type="text" id="cep" name="cep" class="form-control"
               pattern="[0-9]{5}-?[0-9]{3}"
               title="Digite um CEP no formato 78550-000"
               inputmode="numeric" autocomplete="postal-code" placeholder="78550-000">
      </div>
    </fieldset>

    <fieldset class="col-12 col-lg-6">
      <legend class="h5">Sobre o seu pedido</legend>

      <div class="mb-3">
        <label for="assunto" class="form-label">Assunto *</label>
        <select id="assunto" name="assunto" class="form-select" required>
          <option value="">Selecione um assunto</option>
          <optgroup label="Atendimento">
            <option value="reserva">Reserva de mesa</option>
            <option value="encomenda">Encomenda de bolos e tortas</option>
            <option value="graos">Compra de grãos em pacote</option>
          </optgroup>
          <optgroup label="Institucional">
            <option value="evento">Evento ou parceria</option>
            <option value="trabalhe">Trabalhe conosco</option>
          </optgroup>
        </select>
      </div>

      <div class="row g-3 mb-3">
        <div class="col-12 col-sm-4">
          <label for="pessoas" class="form-label">Pessoas</label>
          <input type="number" id="pessoas" name="pessoas" class="form-control"
                 min="1" max="40" step="1" value="2">
        </div>
        <div class="col-12 col-sm-4">
          <label for="data" class="form-label">Data desejada</label>
          <input type="date" id="data" name="data" class="form-control">
        </div>
        <div class="col-12 col-sm-4">
          <label for="horario" class="form-label">Horário</label>
          <input type="time" id="horario" name="horario" class="form-control"
                 min="07:00" max="20:00" step="900">
        </div>
      </div>

      <div class="mb-3">
        <label for="mensagem" class="form-label">Mensagem *</label>
        <textarea id="mensagem" name="mensagem" class="form-control"
                  rows="5" maxlength="500" required minlength="10"
                  placeholder="Conte o que você precisa"></textarea>
      </div>
    </fieldset>

    <fieldset class="col-12">
      <legend class="h5">Como prefere ser respondido?</legend>

      <div class="form-check form-check-inline">
        <input type="radio" id="canal-email" name="canal" value="email"
               class="form-check-input" checked>
        <label for="canal-email" class="form-check-label">E-mail</label>
      </div>

      <div class="form-check form-check-inline">
        <input type="radio" id="canal-telefone" name="canal" value="telefone"
               class="form-check-input">
        <label for="canal-telefone" class="form-check-label">Telefone</label>
      </div>

      <div class="form-check form-check-inline">
        <input type="radio" id="canal-whatsapp" name="canal" value="whatsapp"
               class="form-check-input">
        <label for="canal-whatsapp" class="form-check-label">WhatsApp</label>
      </div>
    </fieldset>

    <div class="col-12">
      <div class="form-check">
        <input type="checkbox" id="novidades" name="novidades" value="sim"
               class="form-check-input">
        <label for="novidades" class="form-check-label">
          Quero receber avisos de novos lotes de café por e-mail
        </label>
      </div>

      <div class="form-check">
        <input type="checkbox" id="consentimento" name="consentimento" value="sim"
               class="form-check-input" required>
        <label for="consentimento" class="form-check-label">
          Autorizo o Café Cerrado a usar meus dados para responder a este contato *
        </label>
      </div>
    </div>

    <input type="hidden" name="origem" value="site-contato">

    <div class="col-12 d-flex gap-2">
      <button type="submit" class="btn btn-cafe btn-enviar">Enviar mensagem</button>
      <button type="reset" class="btn btn-cafe-vazado">Limpar formulário</button>
    </div>
  </form>
</main>
```

Repare que os `<fieldset>` viraram **colunas do grid**: `col-12 col-lg-6` põe os dois primeiros blocos lado a lado em telas grandes e um sobre o outro no celular. Um `fieldset` é um elemento como outro qualquer — pode receber classes de coluna sem perder o significado de agrupamento para o leitor de tela.

Os rádios ganharam `id` e `label for`. Na Aula 03 eles estavam envolvidos pelo próprio `<label>`, o que também é válido; o Bootstrap, porém, estiliza `form-check-input` e `form-check-label` como irmãos, e o par `for`/`id` é a forma que funciona com esse layout.

### Passo 6 — O rodapé

**`cafe-cerrado/index.html`** (o `<footer>` completo, igual nas três páginas)

```html
<footer class="rodape mt-5 py-5">
  <div class="container">
    <div class="row g-4">
      <section class="col-12 col-md-4">
        <h2 class="h5">Café Cerrado</h2>
        <p class="mb-0">
          Torrefação artesanal de grãos do Cerrado mato-grossense. Projeto fictício
          usado como estudo de caso do Nível 2 do WebLab (Desenvolvimento Web).
        </p>
      </section>

      <section class="col-12 col-md-4">
        <h2 class="h5">Onde estamos</h2>
        <address class="mb-0">
          Avenida dos Jacarandás, 1200 — Setor Comercial<br>
          Sinop — MT<br>
          <a href="tel:+556699999000">(66) 9 9999-9000</a><br>
          <a href="mailto:contato@cafecerrado.exemplo.br">contato@cafecerrado.exemplo.br</a>
        </address>
      </section>

      <nav class="col-12 col-md-4" aria-label="Rodapé">
        <h2 class="h5">Navegação</h2>
        <ul class="list-unstyled mb-0">
          <li><a href="index.html">Início</a></li>
          <li><a href="cardapio.html">Cardápio</a></li>
          <li><a href="contato.html">Contato</a></li>
          <li><a href="index.html#horarios">Horários</a></li>
        </ul>
      </nav>
    </div>

    <p class="text-center small mt-4 mb-0">Café Cerrado · UNEMAT Sinop · Projeto acadêmico</p>
  </div>
</footer>
```

### Passo 7 — O novo `css/estilo.css`

Agora a melhor parte: apagar código. Substitua **todo** o conteúdo de `css/estilo.css` pelo arquivo abaixo. Ele tem menos de um terço do tamanho do anterior, porque tudo o que era layout, tabela, formulário e espaçamento agora vem do framework. O que sobra é só o que o Bootstrap não sabe: a identidade da sua marca.

**`cafe-cerrado/css/estilo.css`** (arquivo completo)

```css
/* Café Cerrado — tempero sobre o Bootstrap 5.3.
   Só o que o framework não entrega: paleta da marca, variantes de botão,
   card de produto, navbar colorida e o realce de campo inválido. */

/* ---------- 1. Variáveis do projeto (Aula 02) ---------- */
:root {
  --cor-marca: #6f4e37;
  --cor-marca-escura: #4a3325;
  --cor-destaque: #c2703d;
  --cor-fundo: #fdfaf6;
  --cor-superficie: #ffffff;
  --cor-texto: #2b2118;
  --cor-texto-suave: #5c4b3c;
  --cor-menu-inativo: rgba(255, 255, 255, 0.82);
  --cor-menu-borda: rgba(255, 255, 255, 0.35);
  --borda-suave: rgba(111, 78, 55, 0.15);
  --realce-invalido: rgba(220, 53, 69, 0.2);

  --fonte-base: system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
  --raio: 0.75rem;
}

/* ---------- 2. Tokens globais do Bootstrap ---------- */
/* Cores em três números são exigência do Bootstrap: ele monta rgba() com elas
   para oferecer os utilitários de opacidade. 111,78,55 = #6f4e37. */
:root {
  --bs-body-bg: var(--cor-fundo);
  --bs-body-color: var(--cor-texto);
  --bs-body-font-family: var(--fonte-base);
  --bs-link-color-rgb: 111, 78, 55;
  --bs-link-hover-color-rgb: 74, 51, 37;
  --bs-border-radius: var(--raio);
  --bs-secondary-color: var(--cor-texto-suave);
}

/* ---------- 3. Navbar com a cor da marca ---------- */
/* Só variáveis do componente: o HTML fica limpo, sem classe de cor. A única cor literal fora do :root está dentro da data URI do ícone — ali ela é texto de uma imagem SVG, não uma declaração CSS. */
.navbar {
  background-color: var(--cor-marca);
  --bs-navbar-color: var(--cor-menu-inativo);
  --bs-navbar-hover-color: var(--cor-superficie);
  --bs-navbar-active-color: var(--cor-superficie);
  --bs-navbar-brand-color: var(--cor-superficie);
  --bs-navbar-brand-hover-color: var(--cor-superficie);
  --bs-navbar-toggler-border-color: var(--cor-menu-borda);
  --bs-navbar-toggler-icon-bg: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3e%3cpath stroke='rgba%28255, 255, 255, 0.85%29' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3e%3c/svg%3e");
}

.navbar .nav-link[aria-current="page"] {
  font-weight: 600;
}

/* ---------- 4. Variantes de botão da marca ---------- */
.btn-cafe {
  --bs-btn-bg: var(--cor-marca);
  --bs-btn-border-color: var(--cor-marca);
  --bs-btn-color: var(--cor-superficie);
  --bs-btn-hover-bg: var(--cor-marca-escura);
  --bs-btn-hover-border-color: var(--cor-marca-escura);
  --bs-btn-hover-color: var(--cor-superficie);
  --bs-btn-active-bg: var(--cor-marca-escura);
  --bs-btn-active-border-color: var(--cor-marca-escura);
  --bs-btn-active-color: var(--cor-superficie);
  --bs-btn-disabled-bg: var(--cor-marca);
  --bs-btn-disabled-border-color: var(--cor-marca);
  --bs-btn-disabled-color: var(--cor-superficie);
  --bs-btn-focus-shadow-rgb: 111, 78, 55;
}

.btn-cafe-vazado {
  --bs-btn-bg: transparent;
  --bs-btn-border-color: var(--cor-marca);
  --bs-btn-color: var(--cor-marca);
  --bs-btn-hover-bg: var(--cor-marca);
  --bs-btn-hover-border-color: var(--cor-marca);
  --bs-btn-hover-color: var(--cor-superficie);
  --bs-btn-active-bg: var(--cor-marca-escura);
  --bs-btn-active-border-color: var(--cor-marca-escura);
  --bs-btn-active-color: var(--cor-superficie);
  --bs-btn-focus-shadow-rgb: 111, 78, 55;
}

/* ---------- 5. Hero e cards ---------- */
.hero {
  background-color: var(--cor-superficie);
  border-bottom: 1px solid var(--borda-suave);
}

.hero__titulo {
  color: var(--cor-marca-escura);
}

.hero__texto {
  color: var(--cor-texto-suave);
  max-width: 40rem;
  margin-inline: auto;
}

.card-produto {
  --bs-card-bg: var(--cor-superficie);
  --bs-card-border-color: var(--borda-suave);
  --bs-card-border-radius: var(--raio);
  --bs-card-cap-bg: transparent;
}

.card-produto .card-img-top {
  aspect-ratio: 4 / 3;
  object-fit: cover;
}

/* ---------- 6. Formulário: o que o Bootstrap não faz sem JavaScript ---------- */
/* :user-invalid só marca o campo DEPOIS da interação (Aula 03, §4.5). */
.form-control:user-invalid,
.form-select:user-invalid {
  border-color: var(--bs-form-invalid-border-color);
  box-shadow: 0 0 0 0.25rem var(--realce-invalido);
}

/* ---------- 7. Rodapé ---------- */
.rodape {
  background-color: var(--cor-marca-escura);
  color: var(--cor-menu-inativo);
}

.rodape h2,
.rodape a {
  color: var(--cor-superficie);
}
```

Guarde o arquivo antigo? Não precisa: o Git guarda. Se der saudade, `git show HEAD~1:css/estilo.css` mostra a versão anterior sem restaurar nada.

### Passo 8 — A justificativa no `README.md`

Este passo vale nota. Acrescente a seção abaixo ao `README.md` do repositório:

**`cafe-cerrado/README.md`** (acrescente ao final)

```markdown
## Framework CSS

Este projeto usa **Bootstrap 5.3.3**, carregado por CDN (jsDelivr) com versão
fixa, `integrity` e `crossorigin`.

Por que Bootstrap e não Tailwind ou Material Web:

- O site é estático e não tem etapa de build. O Bootstrap é o único dos três que
  entrega grid **e** componentes prontos por CDN; o Tailwind por CDN é só para
  estudo e o Material Web não tem sistema de grid.
- O projeto precisa de menu responsivo, cards e formulário bem resolvidos, não de
  um design autoral. A curva de aprendizado baixa vale mais aqui do que a
  liberdade visual total do Tailwind.
- A identidade da marca é aplicada pelas variáveis CSS `--bs-*` da versão 5.3
  (`--bs-btn-*`, `--bs-navbar-*`), sem `!important` e sem lutar com a
  especificidade do framework.

O que é nosso e o que é do framework: todo o layout, os componentes e os
utilitários vêm do Bootstrap; o arquivo `css/estilo.css` tem apenas a paleta da
marca, duas variantes de botão (`.btn-cafe`, `.btn-cafe-vazado`), o card de
produto e o realce de campo inválido com `:user-invalid`.
```

### Passo 9 — Publicar

**Terminal, na pasta do repositório**

```bash
git add index.html cardapio.html contato.html css/estilo.css README.md
git commit -m "Aula 04: adocao do Bootstrap 5.3 nas tres paginas"
git push
```

### Como testar

1. Abra `index.html` com o Live Server e reduza a janela até abaixo de 992 px. O menu vira um botão hambúrguer; clique nele: o menu abre e fecha. É o único JavaScript do projeto funcionando.
2. Ainda no modo estreito, confira que **não existe rolagem horizontal**. Se existir, algum bloco está fora de um `container` ou uma imagem está sem `img-fluid`.
3. Abra o modo dispositivo (<kbd>F12</kbd> → ícone de celular) e teste em 360 px, 768 px e 1200 px. Os cards de destaque devem ficar em 1, 2 e 3 colunas, nessa ordem.
4. No `cardapio.html`, confira que todos os cards de uma mesma fileira têm a **mesma altura**, mesmo com descrições de tamanhos diferentes. Se não tiverem, faltou `h-100`.
5. Passe o mouse nos botões: `btn-cafe` escurece; `btn-cafe-vazado` preenche. Navegue por <kbd>Tab</kbd>: o anel de foco aparece na cor da marca (é o `--bs-btn-focus-shadow-rgb`).
6. Em `contato.html`, com a janela larga, os dois primeiros `fieldset` ficam lado a lado; estreite a janela e eles empilham.
7. Envie o formulário vazio: o navegador continua bloqueando com "Preencha este campo". Digite duas letras no nome, saia do campo: a borda fica vermelha (é o `:user-invalid`).
8. Na aba **Network**, recarregue com cache desativado e anote o valor transferido de `bootstrap.min.css` e de `bootstrap.bundle.min.js`. Some: o total deve ficar perto de 57 KB.
9. Quebre um caractere do `integrity` do CSS e recarregue: a página perde todo o estilo e o console acusa o bloqueio. Desfaça.
10. Valide as três páginas no W3C outra vez. Zero erros — as classes não mudam a validade do HTML, mas um `<div>` esquecido aberto muda.

**Resultado esperado:** as três páginas do Café Cerrado responsivas, com menu que colapsa, cardápio em grid de cards de altura igual, formulário em duas colunas no desktop e uma no celular, tudo na paleta marrom da marca — e um `css/estilo.css` que cabe em uma tela e meia.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Traduza para português o que este HTML faz em cada uma das três faixas de tela: `<div class="col-12 col-sm-6 col-xl-3">`. Quantas colunas de 12 ele ocupa em 400 px, em 800 px e em 1300 px?

**A2.** Qual a diferença entre `mt-3`, `my-3`, `me-3` e `ms-3`? Escreva o CSS equivalente de cada um, com o valor em `rem`.

**A3.** O trecho abaixo não coloca os dois blocos lado a lado em nenhuma largura. Aponte o erro e corrija:

```html
<div class="container">
  <div class="col-md-6">Esquerda</div>
  <div class="col-md-6">Direita</div>
</div>
```

**A4.** Um colega escreveu `:root { --bs-primary: #6f4e37; }` e reclama que os botões `btn-primary` continuam azuis. Explique por que, e diga qual variável ele deveria ter usado.

**A5.** Qual é a diferença entre `<h3 class="h5">` e `<h5>`? Em que situação a primeira forma é a correta?

**A6.** Classifique cada trecho como "componentes prontos" ou "utility-first" e justifique em uma linha: (a) `class="alert alert-danger"`; (b) `class="flex items-center gap-2"`; (c) `class="card h-100"`; (d) `class="mt-3 d-flex"`.

**A7.** Por que o `<link>` do `css/estilo.css` precisa vir **depois** do `<link>` do Bootstrap? Em que caso essa ordem, sozinha, não resolve?

### Nível B — Aplicação

**B1.** Monte, em um arquivo novo `experimentos/grid.html` com o Bootstrap por CDN, uma página com uma linha de seis blocos coloridos numerados. Eles devem ficar em 1 coluna abaixo de 576 px, 2 colunas a partir de 576 px, 3 a partir de 768 px e 6 a partir de 1200 px — usando `row-cols-*`, sem escrever nenhuma media query.

**Resultado esperado:** ao arrastar a borda da janela, o layout assume exatamente quatro arranjos, mudando nas três larguras previstas.

<details markdown="1"><summary>Dica</summary>

`row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-xl-6` na `row`, e `class="col"` em cada filho. Para enxergar os blocos, use os utilitários `p-3`, `border` e `text-bg-secondary`. Confirme os pontos de quebra com a régua do modo dispositivo do DevTools, não no olho.

</details>

**B2.** Crie uma variante de botão nova, `.btn-cerrado-verde`, usando **apenas** variáveis `--bs-btn-*` — nenhuma propriedade CSS comum, nenhum `!important`. Ela precisa ter cor de fundo, cor de borda, cor de texto, estados `:hover`, `:active` e `:disabled` coerentes, e um anel de foco na mesma família de cor.

**Resultado esperado:** o botão se comporta como qualquer `btn-*` nativo do Bootstrap, inclusive combinado com `btn-lg` e `btn-sm`.

<details markdown="1"><summary>Dica</summary>

A lista completa está na documentação do componente Button, seção "CSS variables". Você precisa de pelo menos `--bs-btn-bg`, `--bs-btn-border-color`, `--bs-btn-color`, os três `--bs-btn-hover-*`, os três `--bs-btn-active-*`, os três `--bs-btn-disabled-*` e `--bs-btn-focus-shadow-rgb`. Confira no DevTools: selecione o botão e procure as variáveis no painel Computed.

</details>

**B3.** Reescreva o card de produto do Café Cerrado em Tailwind 4, em `experimentos/tailwind-card.html`, chegando o mais perto possível do resultado do Bootstrap: imagem no topo com proporção fixa, corpo com título e texto, rodapé com preço à esquerda e etiqueta à direita, e altura total igual à do vizinho quando em grid.

**Resultado esperado:** dois cards lado a lado em telas médias, com a mesma altura, e nenhuma linha de CSS escrita fora das classes utilitárias.

<details markdown="1"><summary>Dica</summary>

Altura igual em grid sai de `h-full` no card e `items-stretch` (ou o padrão) no contêiner do grid. Para empurrar o rodapé para baixo, o card precisa ser `flex flex-col` e o corpo `grow`. A proporção da imagem sai de `aspect-[4/3] object-cover`.

</details>

**B4.** Faça a auditoria de peso da sua página inicial: na aba Network, com o cache desativado, monte uma tabela em `docs/peso.md` com três colunas — recurso, tamanho transferido e percentual do total. Inclua CSS, JavaScript, fontes e **todas** as imagens.

**Resultado esperado:** a tabela mostra, com números, quem realmente pesa na sua página; um parágrafo final aponta o maior vilão e o que fazer com ele.

<details markdown="1"><summary>Dica</summary>

A coluna **Transferred** é o que veio pela rede (comprimido); a coluna **Size** é o tamanho descompactado. Use a primeira. Clique em "Disable cache" antes de recarregar, senão você mede zero. O rodapé do painel mostra o total agregado.

</details>

### Nível C — Desafio

**C1.** Aplique o framework escolhido ao **seu projeto autoral** inteiro, nas três páginas, com os mesmos requisitos do Café Cerrado: menu responsivo que colapsa, grid com no mínimo três cards que viram uma coluna no celular, formulário estilizado, paleta própria aplicada por variáveis do framework (não por `!important`), estrutura semântica da Aula 03 intacta e a justificativa no `README.md`. Publique no GitHub Pages e abra o endereço no celular de outra pessoa (ou em outro aparelho seu).

<details markdown="1"><summary>Dica</summary>

Trabalhe em uma página por vez e faça `commit` a cada uma. Antes de mexer no CSS, apague todo o layout escrito à mão da Aula 03: manter os dois brigando é a causa número um de "o Bootstrap não está funcionando". Se aparecer rolagem horizontal, o culpado quase sempre é uma `row` sem `container` em volta, ou um `col-*` que é filho de algo que não é `row`.

</details>

**C2.** Pegue a página inicial pronta e crie uma segunda versão dela em `experimentos/tailwind-home.html`, com o mesmo conteúdo, feita inteiramente em Tailwind 4 pelo Play CDN. Depois escreva, em `docs/comparacao.md`, o que ficou melhor e o que ficou pior — com números de linhas e um trecho de cada versão lado a lado.

<details markdown="1"><summary>Dica</summary>

Não tente reproduzir o visual do Bootstrap pixel a pixel: o objetivo é comparar o **processo**, não o resultado. Cronometre quanto tempo você levou em cada versão e registre também isso; é o dado mais honesto da comparação.

</details>

## 🏆 Desafios

### ⭐ O framework por baixo do capô
Tags: css, layout, devtools, investigacao

Você usou `col-md-6` a tarde inteira sem nunca ter visto o CSS que faz aquilo acontecer. Isso é confortável e é perigoso: no dia em que a coluna não obedecer, você não vai ter para onde olhar. Abra a caixa preta. O `bootstrap.min.css` é um arquivo de texto comum — e tudo que ele faz é CSS que você já sabe ler.

**Critérios de pronto**

- Um arquivo `docs/bootstrap-por-dentro.md` com o CSS real (copiado do arquivo, não de tutorial) de cinco classes: `.container`, `.row`, `.col-md-6`, `.d-flex` e `.h-100`.
- Para cada uma, duas linhas explicando o que aquele CSS faz — em português, sem repetir o nome da propriedade.
- A resposta, com evidência, para: por que uma `col-*` colocada fora de uma `row` fica com um espaço estranho nas laterais?
- A resposta, com evidência, para: quantas media queries diferentes o `.container` usa e quais são as larguras máximas em cada uma?

<details markdown="1"><summary>Pistas</summary>

1. Baixe o arquivo com `curl -sO` e formate-o antes de ler: o VS Code faz isso com <kbd>Shift</kbd>+<kbd>Alt</kbd>+<kbd>F</kbd> em um arquivo `.css`.
2. Existe uma versão não minificada oficial, `bootstrap.css`, no mesmo caminho da CDN, com comentários — muito mais fácil de ler.
3. Para a pergunta do espaço lateral, procure `margin-left` na regra `.row` e `padding-left` na regra `.row > *`. Um cancela o outro; sozinho, o segundo aparece.
4. No DevTools, o painel **Computed** mostra o valor final de cada propriedade e, clicando na setinha, de qual regra ele veio.

</details>

### ⭐⭐ O mesmo componente, três vezes
Tags: css, layout, responsivo, performance

Discussões sobre framework na internet duram anos e quase nunca têm números. Você vai encerrar a sua em uma tarde: construa **o mesmo** componente — um card de produto com imagem, título, texto, preço e botão — nos três frameworks desta aula, meça tudo, e só então opine.

**Critérios de pronto**

- Três arquivos em `experimentos/`, um por framework, cada um com um grid de seis cards responsivo (1 / 2 / 3 colunas).
- Uma tabela em `docs/tres-frameworks.md` com quatro colunas: framework, KB transferidos, linhas de HTML do card, tempo que você levou.
- Um parágrafo sobre **manutenção**: em qual das três versões é mais fácil mudar a cor da marca em todos os cards de uma vez? Prove fazendo a mudança e contando quantas linhas foram tocadas.
- Uma conclusão de cinco linhas que não use as palavras "melhor" nem "pior" sem número ao lado.

<details markdown="1"><summary>Pistas</summary>

1. Meça sempre com "Disable cache" ligado e leia a coluna **Transferred**, não a **Size**.
2. Para o Material Web, lembre que ele não tem grid: use CSS Grid nativo e registre isso como um custo na sua tabela.
3. Para a pergunta da manutenção, a resposta não é óbvia: no Tailwind sem build, trocar a cor significa editar todas as ocorrências da classe; com `@theme`, significa editar uma linha. Compare os dois cenários.
4. Um cronômetro honesto vale mais que uma opinião elegante. Anote o tempo antes de começar cada versão.

</details>

### ⭐⭐ Fuja da cara de Bootstrap
Tags: css, layout, refatoracao, projeto

Existe um jogo cruel entre desenvolvedores: abrir um site e adivinhar o framework em dois segundos. Sites feitos com Bootstrap sem customização são os mais fáceis — azul `#0d6efd`, cantos de 6 px, a mesma sombra, a mesma fonte. Seu desafio é fazer o Café Cerrado passar despercebido nesse jogo, **sem** abandonar o framework e **sem** escrever um único `!important`.

**Critérios de pronto**

- Nenhuma cor padrão do Bootstrap visível na página: primária, secundária, links, foco, badges e alertas todos na paleta da marca.
- Tipografia própria: uma fonte de título diferente da fonte de corpo, carregada de forma que não bloqueie a renderização.
- Raios de borda, sombras e escala de espaçamento ajustados por variáveis, não por regras novas.
- Um arquivo `docs/tema.md` listando cada variável `--bs-*` que você sobrescreveu e o que ela controla.
- Prova final: mostre a página para três pessoas quaisquer — colegas de estudo, amigos, familiares — e registre quantos acertaram o framework. Se alguém acertar, pergunte pelo quê — e conserte.

<details markdown="1"><summary>Pistas</summary>

1. Comece pelo `:root`: `--bs-primary-rgb`, `--bs-body-bg`, `--bs-body-color`, `--bs-border-radius`, `--bs-box-shadow`, `--bs-font-sans-serif`.
2. As cores do Bootstrap 5.3 vivem em duas formas, `--bs-primary` e `--bs-primary-rgb`. Utilitários de fundo e texto usam a segunda; se você trocar só a primeira, metade da página não muda.
3. Fonte sem bloquear renderização significa `<link rel="preconnect">` mais `display=swap` na URL do Google Fonts — ou, melhor ainda, a fonte hospedada no seu próprio repositório.
4. O detalhe que mais entrega o Bootstrap não é a cor: é o `border-radius` de 6 px e o espaçamento vertical dos componentes. Mexa neles.

</details>

### ⭐⭐⭐ Seu micro-framework de 200 linhas
Tags: css, layout, grid, refatoracao

A melhor forma de entender um framework é escrever um. Não um clone do Bootstrap — um **micro-framework** honesto, de no máximo 200 linhas de CSS, com o mínimo necessário para montar o site do Café Cerrado sem nenhuma dependência externa. Quando terminar, você vai saber exatamente o que está comprando quando importa 230 KB de CSS.

**Critérios de pronto**

- Um arquivo `experimentos/mini.css` com, no máximo, 200 linhas: reset, escala de espaçamento por variáveis, grid responsivo de 12 colunas com três breakpoints, e quatro componentes (botão, card, campo de formulário, barra de navegação).
- O grid precisa funcionar com a mesma sintaxe de nome que você escolher, documentada em `experimentos/mini.md`, e ser implementado com CSS Grid ou Flexbox — a escolha justificada por escrito.
- Uma cópia da página inicial do Café Cerrado usando **apenas** o seu `mini.css`, visualmente coerente (não precisa ser idêntica) e sem rolagem horizontal em 360 px.
- Comparativo de tamanho: quantos KB o seu arquivo tem contra os do Bootstrap, e a lista honesta do que o seu **não** faz.
- Uma seção "o que eu subestimei" com pelo menos três itens que pareciam simples e não eram.

<details markdown="1"><summary>Pistas</summary>

1. Comece pelo grid; é a parte que dá mais retorno. Com CSS Grid, `grid-template-columns: repeat(12, 1fr)` e classes de `grid-column: span N` resolvem em menos de 20 linhas.
2. Use uma única escala de espaçamento em variáveis (`--e-1` a `--e-5`) e faça todos os componentes lerem dela. É isso que dá coerência visual, mais do que qualquer cor.
3. Não tente cobrir todos os casos. Um framework de 200 linhas é uma **decisão sobre o que não fazer** — e essa lista de recusas é a parte mais valiosa da entrega.
4. Compare o seu resultado com projetos reais de CSS mínimo, como o `new.css` ou o `Pico.css`, depois de terminar o seu — nunca antes.

</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| A página perde todo o estilo e o console mostra `Failed to find a valid digest in the 'integrity' attribute for resource` | Hash SRI errada, ou versão da URL diferente da versão da hash | Copie o par URL + `integrity` da mesma linha da documentação oficial; nunca misture versões |
| O menu hambúrguer aparece mas não abre ao clicar | O `bootstrap.bundle.min.js` não foi carregado, ou o `data-bs-target` não bate com o `id` do bloco | Confira o script antes de `</body>` e o par `data-bs-target="#menu-principal"` / `id="menu-principal"` |
| `Uncaught ReferenceError: bootstrap is not defined` | Uso da API JavaScript do framework (`new bootstrap.Modal(…)`) sem o `bundle` na página, ou antes dele | Carregue o `bundle` como último elemento antes de `</body>`, e o seu código depois dele |
| O seu CSS "não pega" e no DevTools a declaração aparece riscada | O `estilo.css` foi carregado antes do Bootstrap, ou o seletor dele é menos específico | Ponha o seu `<link>` depois do dele; se o seletor perder, use as variáveis `--bs-*` em vez de subir a especificidade |
| Trocar `--bs-primary` no `:root` não muda a cor dos botões | Botões leem `--bs-btn-*`; `--bs-primary` alimenta os utilitários de cor | Crie uma variante própria (`.btn-cafe`) definindo as variáveis `--bs-btn-*` |
| Links ficam pretos depois de você definir `--bs-link-color-rgb: #6f4e37` | A variável espera três números separados por vírgula, não um hexadecimal | Use `--bs-link-color-rgb: 111, 78, 55` |
| Aparece rolagem horizontal no celular | Uma `col-*` fora de uma `row`, ou uma `row` fora de um `container` | Respeite `container` → `row` → `col`; a margem negativa da `row` precisa do padding do `container` |
| Os cards de uma fileira têm alturas diferentes | Falta `h-100` no card dentro da `col` | `class="card h-100"` no card; a coluna já estica por padrão |
| Imagens estouram a largura da tela | Imagem sem `img-fluid` (ou sem `max-width: 100%`) | Acrescente `class="img-fluid"` em toda `<img>` de conteúdo |
| `col-md-6` deixa tudo em uma coluna só no notebook | Confusão de mobile-first: `md` vale **a partir de** 768 px, não "no tablet apenas" | Declare do menor para o maior: `col-12 col-md-6 col-lg-4` |
| Os campos do formulário continuam com a aparência antiga | Falta `form-control` (ou `form-select` no `<select>`) | Cada tipo de controle tem a sua classe; caixas e rádios usam `form-check-input` |
| As classes do Tailwind não fazem nada no arquivo de experimento | Uso do endereço do Tailwind 3 (`cdn.tailwindcss.com`) esperando comportamento da v4 | Use `https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4` |
| `<md-filled-button>` não aparece na tela | O `importmap` veio depois do módulo que importa, ou o script não é `type="module"` | O `<script type="importmap">` precisa vir antes de qualquer `import`; o segundo script precisa de `type="module"` |
| Dois frameworks juntos e componentes com aparência quebrada | Colisão de nomes: `.card`, `.btn` e `.container` existem em quase todos | Um framework por projeto; remova o anterior por inteiro antes de trocar |

## 🏠 Para praticar depois da aula (1 h)

**Parte 1 — Leitura (20 min).** QUEIRÓS e PORTELA, *Introdução ao Desenvolvimento Moderno para a Web*, seções sobre a camada de apresentação e frameworks de CSS (Biblioteca Virtual da UNEMAT). Em seguida, leia a página *Layout → Breakpoints* da documentação oficial do Bootstrap 5.3 e a página *Styling with utility classes* do Tailwind. Anote **duas** ideias que os dois textos defendem de formas opostas.

**Parte 2 — Entrega (30 min).** No repositório do seu **projeto autoral**:

1. O framework escolhido aplicado às três páginas, com menu responsivo, grid de no mínimo três cards e formulário estilizado (exercício **C1**).
2. `README.md` com a seção "Framework CSS": qual, por quê (dois a quatro argumentos), como foi carregado e o que é seu contra o que é do framework.
3. `docs/peso.md` com a auditoria do exercício **B4**.
4. Nenhum `!important` no seu CSS — fora do bloco `prefers-reduced-motion` da Aula 05, onde ele é a forma correta. Se houver algum, troque por variável do framework ou por um seletor honesto, e registre a troca no `README.md`.

**Parte 3 — Argumento contrário (10 min).** Em `docs/framework.md`, anote o framework escolhido e **um** argumento contra a sua própria escolha (todo framework tem um). Se puder, compare com outra pessoa que tenha feito uma escolha diferente e anote uma situação concreta em que a escolha dela seria melhor que a sua.

**Critério de pronto:** o site do projeto autoral abre pelo endereço do GitHub Pages; em 360 px de largura não há rolagem horizontal e o menu colapsa; em 1200 px os cards ficam lado a lado; a paleta é a da sua marca, não a padrão do framework; e o `README.md` justifica a escolha em texto próprio.

**Guarde no seu repositório:** commit + push.

## ✅ Checkpoint do projeto

Ao fim desta aula, o repositório do seu projeto autoral deve ter:

- [ ] Framework CSS carregado por CDN nas três páginas, com **versão fixa** na URL e, quando o provedor fornecer, `integrity` e `crossorigin="anonymous"`.
- [ ] O seu arquivo de estilos carregado **depois** do framework, em todas as páginas.
- [ ] Menu responsivo que colapsa em telas estreitas e volta ao normal nas largas, com `aria-current="page"` preservado da Aula 03.
- [ ] Grid do framework em uso com pelo menos três cards que passam de 3 para 1 coluna conforme a largura.
- [ ] Formulário de contato inteiro estilizado pelas classes do framework, com a validação nativa ainda funcionando.
- [ ] Estrutura semântica da Aula 03 intacta: `header`, `nav`, `main`, `footer`, `fieldset`, `legend`, `caption`, `th scope`, `alt` em todas as imagens.
- [ ] Paleta da marca aplicada por variáveis do framework; **zero** `!important` no seu CSS. A única exceção aceita no curso inteiro é o bloco `@media (prefers-reduced-motion: reduce)` que você vai escrever na Aula 05: ali o `!important` é o mecanismo previsto para desligar animações que qualquer outra regra tenha ligado.
- [ ] Nenhuma rolagem horizontal em 360 px de largura, em nenhuma das três páginas.
- [ ] Um único framework CSS no projeto.
- [ ] `README.md` com a seção "Framework CSS" justificando a escolha em texto próprio.
- [ ] `docs/peso.md` com a auditoria de tamanho da página inicial.
- [ ] Zero erros no validador do W3C nas três páginas; `commit` e `push` feitos e site atualizado no GitHub Pages.

## 📚 Para aprofundar

- **Bootstrap 5.3 — Introdução**: <https://getbootstrap.com/docs/5.3/getting-started/introduction/> — a página com as tags de CDN oficiais, sempre com o `integrity` atualizado. É de lá que você copia, nunca de tutorial de terceiros.
- **Bootstrap 5.3 — Grid**: <https://getbootstrap.com/docs/5.3/layout/grid/> — leia até "Row columns"; é o que resolve 90 % dos layouts do curso.
- **Bootstrap 5.3 — CSS variables**: <https://getbootstrap.com/docs/5.3/customize/css-variables/> — a lista das variáveis globais e a explicação do formato RGB das cores.
- **Bootstrap 5.3 — Navbar**: <https://getbootstrap.com/docs/5.3/components/navbar/> — a seção "How it works" explica exatamente o que `navbar-expand-*` faz.
- **Bootstrap 5.3 — Forms**: <https://getbootstrap.com/docs/5.3/forms/overview/> — a tabela de classes por tipo de controle; deixe aberta enquanto estiliza o formulário.
- **Tailwind CSS — Styling with utility classes**: <https://tailwindcss.com/docs/styling-with-utility-classes> — o texto em que a equipe defende a filosofia; leia mesmo que você tenha escolhido Bootstrap.
- **Tailwind CSS — Play CDN**: <https://tailwindcss.com/docs/installation/play-cdn> — os avisos oficiais sobre por que não usar isso em produção.
- **Material Design 3**: <https://m3.material.io/> — a especificação do design system; a seção *Styles → Color* explica o esquema de cores derivado de uma cor-semente.
- **Material Web — Quick start**: <https://material-web.dev/about/quick-start/> — o `importmap` e a lista de componentes disponíveis.
- MDN — **Layout responsivo** (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Learn/CSS/CSS_layout/Responsive_Design> — a base que todo framework implementa por baixo.
- MDN — **Especificidade** (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Web/CSS/CSS_cascade/Specificity> — leia antes de escrever o seu próximo `!important`.
- MDN — **Usando propriedades customizadas** (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Web/CSS/Using_CSS_custom_properties> — as variáveis que fazem o `--bs-*` funcionar.
- MDN — **Subresource Integrity**: <https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity> — como a hash é calculada e verificada, e como gerar a sua.
- MDN — **Web Components** (pt-BR): <https://developer.mozilla.org/pt-BR/docs/Web/API/Web_components> — o mecanismo por trás do `<md-filled-button>`.
- **Bootstrap Icons**: <https://icons.getbootstrap.com/> — biblioteca MIT de ícones SVG; você vai usar na próxima aula.
- QUEIRÓS, Ricardo; PORTELA, Filipe. *Introdução ao Desenvolvimento Moderno para a Web*. FCA, 2018 — camada de apresentação e frameworks CSS.
- LOUDON, Kyle. *Desenvolvimento de Grandes Aplicações Web*. Novatec, 2019 — organização e manutenibilidade de CSS em projetos grandes; o capítulo que explica por que a escala de espaçamento importa.
- ALVES, William P. *Projetos de Sistemas Web*. Érica, 2015 — layout e interface de sistemas web.

O site do Café Cerrado agora é responsivo e tem a cor da marca — mas ele é estático como uma foto: o botão troca de estado num estalo, o card não reage ao mouse, o logotipo ainda é texto puro e os ícones não existem. Na próxima aula você acrescenta a camada de movimento e desenho: `transition` e `@keyframes` com propósito, `transform` medido no painel Performance, o logotipo desenhado em SVG inline, um sprite de ícones vetoriais e o bloco `prefers-reduced-motion` que respeita quem prefere a tela quieta. As classes `.btn-cafe`, `.card-produto` e `.hero__titulo` que você criou hoje são exatamente os ganchos onde essas animações vão se pendurar.
