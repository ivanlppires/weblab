# DOI no Zenodo — roteiro de depósito

Como o WebLab ganha um **DOI** (identificador persistente e citável) pelo Zenodo, a partir de uma *release* do GitHub. Complementa `docs/registro-inpi.md`: o INPI protege o *software*, o DOI dá citabilidade acadêmica ao *material publicado*. Os dois convivem.

## Como funciona

O Zenodo mantém uma integração com o GitHub: ao ligar a chave para um repositório público, ele instala um *webhook*. A cada **release publicada**, o Zenodo baixa o `.zip` da tag, lê o `.zenodo.json` da raiz para preencher os metadados e emite um DOI.

São dois DOIs, e vale entender a diferença:

| DOI | O que identifica | Onde usar |
|---|---|---|
| **Concept DOI** | a obra como um todo — resolve sempre para a versão mais recente | citação geral, Lattes, ORCID, rodapé do site |
| **Version DOI** | uma versão específica (v1.0.0, v1.1.0…) | quando o texto precisa apontar para o estado exato consultado |

O Zenodo só recebe releases **publicadas depois** de a chave ser ligada. Ligar a chave é, portanto, o primeiro passo — não o último.

## Fontes dos metadados

Nada é digitado à mão no Zenodo. Tudo sai de `build/config.py → AUTORES`:

```bash
.venv/bin/python build/citacao.py    # regera CITATION.cff e .zenodo.json
```

- `.zenodo.json` — título, resumo em HTML, os 8 autores com ORCID e afiliação, `upload_type: software`, licença CC BY 4.0, idioma `por`, palavras-chave e o enlace para <https://weblab.aprendabit.com>.
- `CITATION.cff` — o botão *Cite this repository* do GitHub.

Se a autoria mudar, edite `config.AUTORES`, rode `citacao.py` de novo e faça uma nova release: o Zenodo relê o `.zenodo.json` a cada versão.

## Passo a passo

### 1. Ligar a chave no Zenodo — *feito no navegador, uma única vez*

1. <https://zenodo.org/signup/> — entrar **com a conta do GitHub** (o vínculo é o que autoriza o webhook). Se já houver conta Zenodo criada por e-mail, ligar o GitHub em *Settings → Linked accounts*.
2. Ir em <https://zenodo.org/account/settings/github/> e autorizar o acesso aos repositórios.
3. Achar `ivanlppires/weblab` na lista e **virar a chave para ON**. Se não aparecer, usar *Sync now* — o Zenodo só lista repositórios públicos em que a conta tem permissão de administração.
4. Aproveitar e preencher o perfil do Zenodo com o **ORCID** (`0000-0002-1380-082X`) — assim o depósito entra automaticamente no ORCID.

### 2. Congelar a versão

O que entra na release é o repositório inteiro na tag — exceto o que o `.gitignore` corta (`site/`, `registro/`, `.venv/`). Antes de marcar:

```bash
.venv/bin/python -m pytest build/tests -q     # 36 testes
.venv/bin/python build/lint.py                # 0 erros
git status --short                            # nada solto que devesse entrar
```

### 3. Criar a release

```bash
git tag -a v1.0.0 -m "WebLab v1.0.0 — 57 aulas em quatro trilhas"
git push origin v1.0.0
gh release create v1.0.0 --title "WebLab v1.0.0" --notes-file <notas>
```

A mesma tag serve de ponto identificável para o pacote do INPI (`build/empacotar_registro.py`), fechando a pendência do item 9 de `docs/registro-inpi.md`.

### 4. Colher o DOI

Em um a dois minutos o depósito aparece em <https://zenodo.org/me/uploads>. Conferir antes de divulgar:

- [ ] os 8 autores, na ordem certa, cada um com ORCID;
- [ ] licença CC BY 4.0 e acesso aberto;
- [ ] idioma português;
- [ ] o resumo em HTML formatado (parágrafos e negritos preservados).

O Zenodo permite **editar os metadados depois** sem gerar novo DOI — o que não dá para trocar são os arquivos.

### 5. Espalhar o DOI

Depois de emitido, com o *concept DOI* em mãos:

- [ ] crachá no `README.md`: `[![DOI](https://zenodo.org/badge/DOI/<doi>.svg)](https://doi.org/<doi>)`;
- [ ] `doi:` e `identifiers:` no `CITATION.cff` — pela geração, em `build/citacao.py`, não no arquivo;
- [ ] "Como citar" no rodapé do site (`build/config.py` + `build/paginas.py`);
- [ ] ORCID — entra sozinho se o perfil do Zenodo estiver vinculado; conferir;
- [ ] Currículo Lattes, em *Material didático ou instrucional* (o registro no INPI, quando sair, vira uma entrada separada em *Software*).

## Decisões tomadas

**`upload_type: software`.** O depósito vem do repositório, e o repositório é o gerador mais as fontes. Se em algum momento interessar depositar a *apostila* como obra à parte — o `apostila.html` ou um PDF —, o caminho é um segundo depósito manual com `upload_type: lesson`, com DOI próprio e relacionado a este por `isPartOf`. Não é necessário para citar o material.

**Sem afiliação institucional no corpo do material.** A instituição aparece na página de autores e nos metadados de cada pessoa, não como titular da obra (ver commit `6227834`).

**Licença dupla.** Conteúdo em CC BY 4.0, gerador em MIT. O Zenodo aceita uma licença só no campo estruturado: fica CC BY 4.0, e a MIT do código está no campo `notes` e no `LICENSE`.
