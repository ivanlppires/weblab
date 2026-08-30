# WebLab — Laboratório de Desenvolvimento Web

Apostila online, gratuita e autocontida das disciplinas de desenvolvimento web da **UNEMAT — Campus Sinop (FACET)**, ministradas pelo Prof. Ivan Luiz Pedroso Pires.

**No ar em <https://weblab.ivanpires.dev>**

| Trilha | Disciplina | Aulas | Projeto fio-condutor |
|---|---|---|---|
| Nível 1 — Introdução ao Desenvolvimento Web | FACET-SNP-319 | 15 | Site de um evento acadêmico (HTML → CSS → JS) |
| Nível 2 — Desenvolvimento Web | FACET-SNP-307 | 16 | Café Cerrado (estático → SPA → Express + OAuth Google + CRUD) |
| Nível 3 — Frameworks Modernos | FACET-SNP-310 | 15 | UniEventos (Vue 3 + Vuetify + Pinia + Express + MySQL/Supabase + Firebase) |
| Deploy & Ferramentas | transversal | 11 | Publicar os três projetos acima |

Mais o **Banco de Desafios** (todos os desafios das aulas + projetos integradores, filtráveis) e **Links úteis**.

## Como está organizado

```
fontes/            ★ conteúdo canônico em Markdown
  ESPECIFICACAO.md   regras editoriais (estrutura das aulas, formato dos desafios, stack, armadilhas)
  nivel-1/ nivel-2/ nivel-3/ deploy/   uma aula por arquivo
  desafios/projetos-integradores.md · links.md · home.md
build/             gerador do site (Python 3.12, python-markdown + pygments)
  config.py          trilhas, aulas, cronograma 2026.2, avaliações — ÚNICO lugar com datas
  render.py          Markdown → HTML, callouts, blocos de código, extração de desafios
  lint.py            valida as fontes (seções obrigatórias, mínimos, fences, placeholders)
  paginas.py         templates · theme.css / app.js design system e comportamento
  build.py           gera site/ (aulas, índices, apostilas únicas, banco, links, busca, sitemap)
  tests/             pytest
site/              saída gerada (não versionada)
deploy.sh          build + rsync para o servidor
docs/              planos de curso (PDF), fontes brutas, spec e plano de implementação
```

## Editar e publicar

```bash
python3 -m venv --system-site-packages .venv && .venv/bin/pip install pytest markdown pygments
.venv/bin/python -m pytest build/tests -q      # testes do gerador
.venv/bin/python build/lint.py                 # valida todas as fontes
.venv/bin/python build/build.py                # gera site/ (falha se o lint acusar erro)
.venv/bin/python build/build.py --parcial      # gera só o que existe (durante a escrita)
./deploy.sh                                    # build + rsync → https://weblab.ivanpires.dev
```

Para escrever ou alterar uma aula, siga `fontes/ESPECIFICACAO.md`. O lint rejeita aulas sem a estrutura completa (Objetivos → Pré-requisitos → Roteiro → teoria → Mão na massa → Laboratório A/B/C → 🏆 Desafios → Erros comuns → Atividade assíncrona → Checkpoint → Para aprofundar).

Para adicionar uma aula ou trilha: inclua-a em `build/config.py`, crie o arquivo em `fontes/<trilha>/` e rode o build. Para reutilizar em outro semestre: troque `CRONOGRAMA` e `AVALIACOES` em `build/config.py`.

## Recursos do site

Tema claro/escuro · busca global · botão *Copiar* em todo código · sumário lateral · apostila em arquivo único por trilha · progresso local (aulas concluídas e desafios feitos, salvos no navegador) · Banco de Desafios com filtros · impressão limpa (Ctrl+P) · atalhos `j`/`k`/`/`.

## Licença

Material didático de uso educacional. Livre para consulta, estudo e reuso com atribuição.
