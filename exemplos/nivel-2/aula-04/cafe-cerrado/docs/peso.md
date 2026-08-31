# Auditoria de peso — página inicial

Medido na aba **Network** do DevTools, com *Disable cache* ligado, recarregando
com <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>R</kbd>. A coluna lida é **Transferred**
(o que veio pela rede, comprimido), não **Size**.

| Recurso | Origem | Transferido | % do total |
|---|---|---|---|
| `bootstrap.min.css` | jsDelivr | ~32 KB | 21 % |
| `bootstrap.bundle.min.js` | jsDelivr | ~25 KB | 16 % |
| `fachada.jpg` | própria | ~90 KB | 59 % |
| `index.html` | própria | ~5 KB | 3 % |
| `css/estilo.css` | própria | ~1 KB | 1 % |
| **Total** | | **~153 KB** | 100 % |

> Os números acima são os desta cópia de exemplo, com imagens geradas por script.
> **Refaça a medição no seu projeto** — o exercício B4 pede os seus números, não estes.

## Quem é o vilão

O framework inteiro (CSS + JS = ~57 KB) pesa **menos que uma única foto**.
A conclusão prática é a de sempre: antes de discutir o peso do Bootstrap,
exporte as imagens no tamanho em que elas aparecem na tela e em formato moderno
(WebP ou AVIF). Uma foto de 3 MB tirada do celular e jogada direto no repositório
custa mais do que todos os frameworks desta aula somados — cinquenta vezes mais.

Segundo passo, quando o projeto ganhar build (Nível 3): instalar o Bootstrap por
npm e deixar o empacotador remover o CSS não utilizado. Hoje, sem build, os 32 KB
comprimidos são o preço honesto de não escrever 250 linhas de CSS na mão.
