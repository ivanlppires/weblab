# Registro de programa de computador — dossiê para a AGINOV/UNEMAT

Documento de apoio ao pedido de **Registro de Programa de Computador (RPC)** do WebLab junto ao INPI, com a UNEMAT como depositante, via **AGINOV — Agência de Inovação da UNEMAT**, que é o Núcleo de Inovação Tecnológica da universidade (Resolução 043/2019 do CONSUNI, vinculada à PRPPG) e mantém formulário próprio para registro de software: <https://unemat.br/site/aginov>.

Os campos marcados com **[preencher]** dependem de dados pessoais ou de decisões do NIT e não podem ser inferidos do repositório. Os demais foram extraídos do próprio código e são reproduzíveis pelos comandos indicados.

## 1. Identificação do programa

| Campo | Conteúdo |
|---|---|
| Título | WebLab — sistema de curso online aberto de desenvolvimento web |
| Descrição resumida | Sistema que gera e publica um curso online gratuito de desenvolvimento web a partir de fontes em Markdown, com validação editorial automática, busca, banco de desafios, progresso local e publicação estática |
| Data de criação | 29/08/2026 (primeiro commit do repositório) |
| Situação | Publicado e em operação em https://weblab.aprendabit.com |
| Repositório | https://github.com/ivanlppires/weblab |
| DOI | 10.5281/zenodo.22220024 (conceitual); 10.5281/zenodo.22220025 (v1.0.0) |

## 2. Autoria e titularidade

**Autor:** Ivan Luiz Pedroso Pires — professor da FACET/UNEMAT, Campus Sinop. **[preencher: CPF, endereço, nacionalidade, RG — exigidos pelo formulário]**

**Coautores:** conforme a página de créditos do sistema (`/autores/`, gerada de `build/config.py → AUTORES`). Cada pessoa tem papel e escopo registrados. **[preencher quando houver coautores de código]** — note que o registro no INPI cobre o *programa*; quem contribui apenas com revisão de conteúdo didático é coautor da obra literária, não do software.

**Titular:** **[decisão da AGINOV]**. Pela Lei 9.609/98, art. 4º, programa desenvolvido no âmbito de vínculo funcional tem, em regra, titularidade do empregador — no caso, a UNEMAT, com o autor mantendo os direitos morais. O depósito pela instituição é o caminho usual e permite que a produção seja contabilizada institucionalmente.

## 3. Dados técnicos

| Campo | Conteúdo |
|---|---|
| Linguagens | Python 3.12 (gerador e validação), CSS3 e JavaScript ES2015+ (interface publicada), Bash (publicação) |
| Bibliotecas | `markdown` 3.5.2 e `pygments` 2.17.2 (conversão e realce de código); `pytest` (testes). Nenhuma dependência em tempo de execução no site publicado |
| Tipo de programa | Aplicativo — gerador de sítio estático com validação de conteúdo **[confirmar o código da tabela do INPI com o NIT]** |
| Campo de aplicação | Educação / ensino a distância **[confirmar o código da tabela do INPI com o NIT]** |
| Plataforma | Linux (geração); qualquer navegador moderno (uso do sistema publicado) |
| Versão depositada | `v1.0.0` — commit `06ff0f1`, o mesmo estado que recebeu o DOI |
| Linhas de código depositadas | 3.434, em 17 arquivos (ver `registro/weblab-listagem.txt`) |

## 4. O que é depositado — e o que fica de fora

Deposita-se o **código do sistema**: o gerador em Python (`build/*.py`), o design system (`build/theme.css`), o comportamento da interface (`build/app.js`), os testes automatizados (`build/tests/`) e o script de publicação (`deploy.sh`).

**Fica de fora, deliberadamente**, o conteúdo didático em Markdown (`fontes/`, mais de 71 mil linhas). Ele não é programa de computador: é obra literária, com proteção autoral automática pela Lei 9.610/98 desde a criação, independente de registro. Se houver interesse em registro formal do *texto*, o caminho é o Escritório de Direitos Autorais da Fundação Biblioteca Nacional — procedimento e taxa distintos, que podem correr em paralelo.

## 5. Descrição funcional (para o formulário)

O WebLab é um sistema de publicação de curso online que transforma material didático escrito em Markdown em um sítio estático autocontido. O sistema opera em cinco etapas encadeadas:

1. **Configuração** (`build/config.py`): estrutura do curso — trilhas, unidades, sequência de aulas, marcos de projeto, bibliografia e autoria.
2. **Validação editorial** (`build/lint.py`): verifica cada arquivo-fonte contra uma especificação editorial — presença e ordem das seções obrigatórias, quantidade mínima de exercícios por nível de dificuldade, formato dos desafios, declaração de linguagem em todo bloco de código, ausência de trechos incompletos, tamanho mínimo e largura máxima de tabelas. A geração é recusada se houver erro.
3. **Conversão e enriquecimento** (`build/render.py`): converte Markdown em HTML, transforma blocos de citação marcados por emoji em caixas de destaque tipadas, envolve blocos de código com rótulo de linguagem e botão de cópia, e extrai automaticamente os desafios de todas as aulas para um banco consolidado e filtrável.
4. **Montagem** (`build/paginas.py`, `build/build.py`): gera páginas por aula, índice por trilha, apostila em arquivo único, banco de desafios, página de links, página de autoria, busca em JSON, mapa do sítio e página de erro; ao final, verifica todos os enlaces internos e âncoras.
5. **Publicação** (`deploy.sh`): sincroniza o resultado com o servidor por `rsync`.

A interface publicada oferece tema claro/escuro persistente, busca instantânea sobre todo o material, sumário de navegação, registro local de progresso do estudante (aulas concluídas e desafios feitos), filtros no banco de desafios, atalhos de teclado e impressão limpa — tudo sem servidor de aplicação e sem requisições externas em tempo de execução.

## 6. Resumo digital (hash)

O e-Software do INPI exige o resumo digital do arquivo depositado. Gere-o com:

```bash
.venv/bin/python build/empacotar_registro.py v1.0.0
```

Sem argumento, o script empacota a árvore de trabalho; com uma tag, lê os arquivos direto do repositório naquele ponto — que é o que amarra o hash a um estado verificável.

O script produz, na pasta `registro/`:

- `weblab-codigo-fonte.zip` — o pacote a ser enviado;
- `weblab-codigo-fonte.hash.txt` — os resumos SHA-512 e SHA-256;
- `weblab-listagem.txt` — inventário com linhas e bytes por arquivo.

O `.zip` é **determinístico** (ordem e datas fixas): rodar o script de novo produz exatamente o mesmo arquivo e o mesmo hash — o que permite à AGINOV conferir de forma independente, a partir do repositório público, sem depender do arquivo que recebeu. Confira com `sha512sum registro/weblab-codigo-fonte.zip`.

Estado atual do pacote da `v1.0.0` (commit `06ff0f1`), 17 arquivos e 3.434 linhas:

```
SHA-256  2c2d4c3e35d96ddb61b9ff4d743331480ff4affaf7d13a172e9c2380cea1036f
```

## 7. Procedimento e custos (confirmar antes de protocolar)

| Item | Valor |
|---|---|
| Guia (GRU) | Código **730** — pedido de registro de programa de computador pelo e-Software |
| Taxa | R$ 210,00, **sem desconto** para universidades, ICTs ou pessoa física |
| Assinatura | Certificado digital qualificado **ICP-Brasil**; a assinatura gov.br **não** é aceita |
| Documentos | Formulário eletrônico, `.zip` do código, hash, declaração de veracidade assinada |
| Prazo | Cerca de 8 a 10 dias úteis para emissão do certificado |
| Vigência | 50 anos, contados de 1º de janeiro do ano seguinte à publicação ou criação |

Fontes: [gov.br — Solicitar o registro de programa de computador](https://www.gov.br/pt-br/servicos/solicitar-o-registro-de-programa-de-computador) e [Guia do e-RPC/INPI](https://www.gov.br/inpi/pt-br/servicos/programas-de-computador/arquivos/guia-basico/apresentaoesoftware.pdf). Valores e exigências mudam — confirme na página do INPI na data do protocolo.

## 8. Relação com o DOI e com a produção acadêmica

Registro no INPI e DOI no Zenodo respondem a perguntas diferentes e **não se substituem**:

- O **registro no INPI** dá prova de anterioridade e titularidade do *software*, com valor jurídico e institucional.
- O **DOI** dá identidade persistente e citabilidade ao *material publicado*, com valor acadêmico: entra no ORCID, permite citação formal e contagem de citações, e versiona cada revisão.

O caminho mais completo usa os dois, e cada um rende um registro distinto no Currículo Lattes — *Software* (com registro) e *Material didático ou instrucional*. A classificação como produto técnico-tecnológico segue a ficha de avaliação vigente da área; confirme os critérios atuais antes de declarar.

## 9. Pendências antes de protocolar

- [x] Congelar a versão a registrar — tag `v1.0.0` publicada, pacote gerado a partir dela, hash amarrado ao commit `06ff0f1`. É o mesmo estado que recebeu o DOI.
- [ ] Dados pessoais do autor (e de coautores de código, se houver) — item 2.
- [ ] Decisão da AGINOV sobre titularidade e sobre quem assina com certificado ICP-Brasil.
- [ ] Códigos de "tipo de programa" e "campo de aplicação" conforme a tabela vigente do INPI.

## 10. O que levar para a AGINOV

Tudo o que depende do repositório já está pronto. Ao abrir o processo, leve:

| Item | Onde está |
|---|---|
| Descrição funcional do programa | item 5 deste documento |
| Dados técnicos (linguagens, bibliotecas, plataforma) | item 3 |
| Pacote do código-fonte | `registro/weblab-codigo-fonte.zip` |
| Resumo digital SHA-512/SHA-256 | `registro/weblab-codigo-fonte.hash.txt` |
| Inventário de arquivos e linhas | `registro/weblab-listagem.txt` |
| Prova de publicação e anterioridade | DOI 10.5281/zenodo.22220024, de 31/08/2026 |
| Repositório público com a tag | https://github.com/ivanlppires/weblab/tree/v1.0.0 |

O DOI ajuda na conversa com a AGINOV por um motivo prático: ele data e fixa publicamente o material antes do protocolo, e o registro no INPI não substitui isso — as duas proteções cobrem coisas diferentes, como explica o item 8.
