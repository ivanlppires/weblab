# Café Cerrado

Estudo de caso da disciplina **Desenvolvimento Web (FACET-SNP-307)** — UNEMAT/Sinop.
Site estático de três páginas, sem etapa de build, publicado no GitHub Pages.

Esta cópia é o **estado do projeto ao fim da Aula 04**: a mesma estrutura semântica
da Aula 03, agora estilizada com Bootstrap 5.3.

## Páginas

| Arquivo | Conteúdo |
|---|---|
| `index.html` | Hero, história, três destaques em grid e tabela de horários |
| `cardapio.html` | Dez produtos em quatro categorias, guia de torras e tabela de grãos |
| `contato.html` | Formulário com treze campos e validação nativa do navegador |

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

## Imagens

As imagens de `img/` são **placeholders gerados por script**, não fotografias.
Recrie-as a qualquer momento com:

```bash
python3 ../ferramentas/gerar-imagens.py
```

No seu projeto real, fotografe você mesmo ou remova a tag `<img>` do card.
Não use imagem qualquer da internet: direito autoral e 3 MB por card.

## Como rodar

```bash
python3 -m http.server 8004     # e abra http://localhost:8004
```

Precisa de internet: o CSS e o JavaScript do Bootstrap vêm da CDN.
Para rodar sem rede, veja `../ferramentas/preparar-offline.sh`.
