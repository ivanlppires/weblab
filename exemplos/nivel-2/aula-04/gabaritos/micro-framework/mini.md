# mini.css — a documentação honesta de um framework de 146 linhas

Desafio ⭐⭐⭐ da Aula 04. Abra `mini.html`: é a página inicial do Café Cerrado
com **zero** dependências externas — sem CDN, sem `integrity`, sem JavaScript.

## Comparativo de tamanho

| Arquivo | Bruto | Comprimido (gzip) | Linhas |
|---|---|---|---|
| `bootstrap.min.css` | 227 KB | ~32 KB | (minificado) |
| `bootstrap.bundle.min.js` | 79 KB | ~25 KB | (minificado) |
| **`mini.css`** | **~6 KB** | **~2,5 KB** | **146** |

Ou seja: ~2 % do peso. Antes de comemorar, leia a próxima seção.

## A sintaxe do grid, e por que CSS Grid

```html
<div class="grade">
  <div class="c-12 c-md-6 c-lg-4">…</div>
</div>
```

- `.grade` = `display: grid; grid-template-columns: repeat(12, 1fr); gap: var(--e-4)`.
- `.grade > *` já ocupa `span 12` — mobile-first, sem escrever nada.
- `.c-N`, `.c-sm-N`, `.c-md-N`, `.c-lg-N` = `grid-column: span N`.

**Escolhi CSS Grid, e não Flexbox, por dois motivos:** o "12 colunas" já existe na
propriedade `grid-template-columns` (não preciso calcular porcentagens), e o `gap`
resolve a calha sem a dupla margem-negativa-no-pai + padding-no-filho que o Bootstrap
precisa usar por ser feito em Flexbox. Foram 6 linhas onde o Bootstrap gasta dezenas.
O preço é não ter os utilitários de ordenação e alinhamento que o Flexbox dá de graça.

## O que este framework NÃO faz (a parte mais importante)

- **Sem spans intermediários nos breakpoints.** Base tem 1–12; `sm`, `md` e `lg` só têm
  2, 3, 4, 6 e 12 — os que o projeto usa de verdade. Precisar de `c-md-7` significa
  acrescentar uma linha.
- **Sem offsets, sem `order`, sem colunas automáticas.** `offset-md-2` não existe.
- **Sem modal, dropdown, carrossel, tooltip, accordion, paginação, badge, alerta, tabs,
  toast, spinner ou breadcrumb.** São quatro componentes, e só.
- **Sem modo escuro.** Nem `prefers-color-scheme`, nem atributo de tema.
- **Sem RTL.** As margens usam propriedades lógicas onde deu, mas nada foi testado em árabe.
- **Sem sistema de validação de formulário** além do `:user-invalid` nativo.
- **Sem tabela responsiva** (o `overflow-x: auto` teria que ser escrito à mão).
- **Sem suporte a navegador antigo.** `:is()`, `:user-invalid`, `aspect-ratio` e `gap` em
  grid exigem navegador recente. O Bootstrap carrega anos de compatibilidade que você
  não vê — e é boa parte dos 227 KB.

## O que eu subestimei

1. **A navbar colapsável.** Parecia trivial e foi o componente mais caro. O truque do
   `checkbox` + `:checked` funciona sem JavaScript, mas custa acessibilidade: um
   `<label>` não anuncia estado, então o leitor de tela não sabe se o menu está aberto ou
   fechado. O Bootstrap usa `aria-expanded` atualizado por JavaScript justamente por isso.
   Meu menu é mais leve **e** pior — e essa é uma frase honesta, não uma desculpa.

2. **Os estados dos componentes.** O `.botao` normal saiu em duas linhas. Depois vieram
   `:hover`, `:focus-visible`, `[disabled]` e a variante vazada com os mesmos quatro
   estados — e o componente triplicou. É exatamente o que a Demo 07 mostra sobre o
   `!important`: o estado normal é a parte fácil.

3. **A escala de espaçamento.** Definir `--e-1` a `--e-5` levou um minuto; fazer **todos**
   os componentes lerem dela, e resistir à tentação de escrever `padding: 14px` em um
   lugar só, foi o que deu coerência visual ao conjunto. Mais do que qualquer cor.

4. **O reset.** Achei que `box-sizing` e `margin: 0` bastariam. Faltaram `img { display:
   block; max-width: 100% }` (a linha que impede o estouro no celular), o
   `border-collapse` da tabela e a herança de fonte nos controles de formulário — que os
   navegadores **não** herdam por padrão, e é por isso que todo framework tem essa linha.

## Depois de terminar

Compare com `new.css`, `Pico.css` e `Water.css` — projetos reais de CSS mínimo.
Compare **depois**, nunca antes: o valor do exercício está em ter tomado as decisões
sozinho e ter descoberto na mão por que cada linha existe.
