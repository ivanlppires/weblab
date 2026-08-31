# Aula 04 — Frameworks CSS · código de aula

Exemplos **executáveis** que materializam a
[Aula 04 do Nível 2](https://weblab.ivanpires.dev/nivel-2/aula-04.html) inteira:
cada seção teórica tem uma demo rodando, o "Mão na massa" tem o resultado final
pronto, os erros comuns são reproduzidos de propósito e o laboratório tem gabarito.

## Como rodar

```bash
./servir.sh            # http://localhost:8004/demos/
./servir.sh 9000       # outra porta, se a 8004 estiver ocupada
```

Abrir os arquivos direto com `file://` funciona para quase tudo, mas quebra os
`<iframe>` de algumas demos e o `importmap` do Material Web. Use o servidor.

**Precisa de internet:** os três frameworks vêm por CDN — é o tema da aula.
Wi-Fi duvidoso? Rode antes:

```bash
./ferramentas/preparar-offline.sh --aplicar    # baixa e troca as URLs por vendor/ local
./ferramentas/preparar-offline.sh --reverter   # depois da aula, volta para a CDN
```

## Roteiro sugerido (os três blocos de 50 min da aula)

### Bloco 1 — por que frameworks existem, CDN e grid

| Momento | Abra | Seção |
|---|---|---|
| Abertura | `cafe-cerrado/index.html` (o resultado de hoje) e o mesmo site da Aula 03, para o "antes e depois" | — |
| As duas filosofias | `demos/01-duas-filosofias.html` — conte as classes com a turma: **9 contra 31** | §1, §2 |
| CDN, versão fixa e SRI | `demos/02-cdn-e-sri.html` + rode `./ferramentas/verificar-sri.sh` no terminal projetado | §3.1–3.3 |
| A ordem no `<head>` | `demos/03-ordem-no-head.html` — abra o painel Styles e mostre a declaração <s>riscada</s> | §3.4 |
| O grid | `demos/04-grid-e-breakpoints.html` — arraste a janela devagar, a régua do rodapé mostra o breakpoint | §4.2–4.3 |

### Bloco 2 — utilitários, componentes, personalização e os outros dois frameworks

| Momento | Abra | Seção |
|---|---|---|
| Utilitários | `demos/05-utilitarios.html` | §4.4 |
| Componentes | `demos/06-componentes.html` — o hambúrguer funcionando e o `h-100` | §4.5 |
| Variáveis `--bs-*` | `demos/07-variaveis-bootstrap.html` — **a demo mais importante da aula** | §4.6 |
| Tailwind | `demos/08-tailwind.html` e `demos/09-tailwind-responsivo-e-tema.html` | §5 |
| Material Web | `demos/10-material-web.html` — desligue o JavaScript e mostre a interface sumir | §6 |
| Comparativo | `demos/11-comparativo-medido.html` — meçam juntos na aba Network | §7 |

### Bloco 3 — mão na massa e laboratório

| Momento | Abra | Seção |
|---|---|---|
| O alvo | `cafe-cerrado/` — as três páginas prontas; os alunos reproduzem o caminho | 💻 Mão na massa |
| Quando alguém travar | `demos/12-erros-comuns.html` — o sintoma dele provavelmente está aí | 🐛 Erros comuns |
| Correção do laboratório | `gabaritos/` | 🧪 Laboratório |

## O que tem aqui

```
aula-04/
├── servir.sh                    servidor local (python3 -m http.server)
├── cafe-cerrado/                💻 Mão na massa — os 9 passos, prontos
│   ├── index.html · cardapio.html · contato.html
│   ├── css/estilo.css           128 linhas, zero !important
│   ├── docs/peso.md             auditoria de peso (exercício B4)
│   ├── img/                     imagens geradas por script (não são fotos)
│   └── README.md                a justificativa do Passo 8
├── demos/                       uma demo por seção teórica
│   ├── index.html               ← o painel, comece por aqui
│   ├── 01…12                    §1 a §7 e os erros comuns
│   ├── banca/                   o mesmo grid de 6 cards nos 3 frameworks
│   └── erros/                   páginas que quebram de propósito
├── gabaritos/
│   ├── nivel-a-respostas.md     A1–A7 comentadas, com os erros mais comuns
│   ├── b1-grid.html · b2-botao-cerrado-verde.html · b3-tailwind-card.html
│   └── micro-framework/         bônus ⭐⭐⭐: mini.css em 146 linhas + mini.md
└── ferramentas/
    ├── gerar-imagens.py         recria as imagens do Café Cerrado
    ├── verificar-sri.sh         🔬 Investigue da §3.3, no terminal
    └── preparar-offline.sh      plano B para a internet da sala
```

## Três avisos honestos

1. **As imagens não são fotos.** São placeholders gerados por
   `ferramentas/gerar-imagens.py`, com a paleta da marca e o nome do produto escrito.
   É de propósito: a aula não pode depender de baixar imagem de terceiros, e o aluno
   precisa ver o exemplo dizendo "fotografe você mesmo".

2. **As demos 01, 11 e `erros/dois-frameworks.html` carregam mais de um framework** —
   exatamente o que a §7.3 proíbe em um projeto. São bancadas de comparação, e é por isso
   que os frameworks aparecem isolados em `<iframe>` (menos no caso do erro, onde a
   colisão é o ponto). Diga isso à turma antes que alguém copie o padrão.

3. **Os números de KB são medições, não constantes.** Refaça na aula, com *Disable cache*
   ligado, lendo a coluna **Transferred**. O número da turma é o que vale.

## Versões usadas

| Framework | Versão | Como entra |
|---|---|---|
| Bootstrap | 5.3.3 | CDN jsDelivr, com `integrity` e `crossorigin` |
| Tailwind CSS | 4 (`@tailwindcss/browser@4`) | Play CDN, sem hash — só para estudo |
| Material Web | 2.5.0 | `importmap` + `esm.run`, sem hash |

Ao atualizar a versão do Bootstrap, **troque a URL e a hash juntas**, copiadas da mesma
linha da documentação oficial. Misturar versão e hash é o primeiro item da tabela de erros.
