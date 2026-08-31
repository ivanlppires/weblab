# Laboratório — Nível A (fixação): respostas comentadas

> Use como chave de correção **depois** de a turma tentar. As respostas erradas mais comuns
> estão anotadas em cada item — elas costumam ser mais úteis em aula do que a resposta certa.

## A1 — `<div class="col-12 col-sm-6 col-xl-3">`

| Largura | Breakpoint ativo | Classe que vale | Colunas de 12 | Na tela |
|---|---|---|---|---|
| 400 px | xs (< 576) | `col-12` | 12 | linha inteira |
| 800 px | md (≥ 768, mas não há `md`) | `col-sm-6` | 6 | metade |
| 1300 px | xl (≥ 1200) | `col-xl-3` | 3 | um quarto |

O ponto da questão é o **800 px**: não existe `col-md-*` na classe, então continua valendo
o `col-sm-6` declarado para telas menores. Mobile-first é isso: cada prefixo vale
*a partir de* sua largura **até** o próximo prefixo declarado.

**Erro comum:** responder "nenhuma classe se aplica em 800 px". Todas se aplicam de baixo
para cima; vence a maior faixa já atingida.

## A2 — `mt-3`, `my-3`, `me-3`, `ms-3`

Tamanho `3` = `1rem` na escala do Bootstrap (0 = 0; 1 = .25rem; 2 = .5rem; 3 = 1rem; 4 = 1.5rem; 5 = 3rem).

| Classe | CSS equivalente |
|---|---|
| `mt-3` | `margin-top: 1rem;` |
| `my-3` | `margin-top: 1rem; margin-bottom: 1rem;` |
| `me-3` | `margin-inline-end: 1rem;` (na prática, `margin-right` em português) |
| `ms-3` | `margin-inline-start: 1rem;` (na prática, `margin-left` em português) |

**Erro comum:** dizer que `me` é *margin-end = margin-bottom*. `e` é o fim do **eixo em linha**
(horizontal), não do vertical. O vertical é `t`/`b`.

## A3 — Por que os blocos não ficam lado a lado

```html
<div class="container">
  <div class="col-md-6">Esquerda</div>   <!-- col direto dentro de container -->
  <div class="col-md-6">Direita</div>
</div>
```

Falta a `row`. Sem ela: (a) não existe o `display: flex` que põe os filhos lado a lado —
as `div` continuam sendo blocos, um embaixo do outro; e (b) o `padding` que a regra
`.row > *` dá às colunas nunca é aplicado, porque o seletor exige uma `.row` como pai.

```html
<div class="container">
  <div class="row">
    <div class="col-md-6">Esquerda</div>
    <div class="col-md-6">Direita</div>
  </div>
</div>
```

A hierarquia `container → row → col` não é estilo de escrita: é o que os seletores do
framework exigem.

## A4 — `--bs-primary` não recolore botões

Porque **botões não leem `--bs-primary`**. Cada componente tem o seu conjunto de variáveis,
com o seu prefixo: o botão lê `--bs-btn-bg`, `--bs-btn-border-color`, `--bs-btn-color` e os
estados. O `--bs-primary` (e o `--bs-primary-rgb`) alimenta os **utilitários** de cor:
`.text-primary`, `.bg-primary`, `.border-primary`.

O colega deveria ter criado uma variante:

```css
.btn-cafe { --bs-btn-bg: #6f4e37; --bs-btn-border-color: #6f4e37; --bs-btn-color: #fff; /* + estados */ }
```

Veja ao vivo em `demos/07-variaveis-bootstrap.html`, seção 2.

## A5 — `<h3 class="h5">` × `<h5>`

- `<h5>` é um título de **quinto nível** na hierarquia do documento. Se ele aparece dentro de
  uma seção cujo título é `<h2>`, existe um salto de nível (h2 → h5): leitores de tela e o
  validador acusam, e o sumário do documento fica errado.
- `<h3 class="h5">` é um título de **terceiro** nível — a posição correta dentro de uma seção
  com `<h2>` — com o **tamanho visual** do quinto.

A forma correta é a primeira sempre que a hierarquia pedir `h3` mas o design pedir um texto
menor — exatamente o caso do título do card no Café Cerrado.

**Regra:** a tag define a estrutura; a classe define a aparência. Nunca escolha a tag pelo
tamanho da fonte.

## A6 — Classificação

| Trecho | Filosofia | Por quê |
|---|---|---|
| (a) `alert alert-danger` | Componentes prontos | Descreve **o que a coisa é**: um alerta, na variante de perigo |
| (b) `flex items-center gap-2` | Utility-first | Descreve **como a coisa parece**: display, alinhamento, espaço |
| (c) `card h-100` | Componentes prontos | `card` é o componente; `h-100` é um utilitário do próprio Bootstrap |
| (d) `mt-3 d-flex` | Utility-first (dentro do Bootstrap) | São utilitários — a prova de que as duas filosofias convergiram (§2.4) |

O item (d) é o mais instrutivo: classes utilitárias **no Bootstrap**. A guerra santa entre as
duas filosofias acabou; o que muda é de onde você parte.

## A7 — Por que o `estilo.css` vem depois

Porque a cascata do CSS resolve **empate de especificidade pela ordem**: entre duas regras de
mesmo peso, vence a que aparece por último. Com o seu arquivo depois, os seus ajustes ganham.

Essa ordem **não** resolve quando o seletor do framework é mais específico. Se o Bootstrap usa
`.navbar .nav-link` (duas classes = 0,2,0) e você escreve `.nav-link` (0,1,0), o dele vence
venha na ordem que vier. Aí a saída é subir a especificidade honestamente
(`.navbar .nav-link[aria-current]`) ou — melhor — usar as variáveis `--bs-*`.
Nunca `!important`.

Comparação ao vivo: `demos/03-ordem-no-head.html`.
