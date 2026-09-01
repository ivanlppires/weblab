# DOI no Zenodo — roteiro de depósito

Como o WebLab ganha um **DOI** (identificador persistente e citável) no Zenodo, a partir de uma tag do repositório. Complementa `docs/registro-inpi.md`: o INPI protege o *software*, o DOI dá citabilidade acadêmica ao *material publicado*. Os dois convivem.

## Como funciona

O depósito é feito pela **API do Zenodo**, por `build/publicar_zenodo.py`: o script empacota a tag, envia os metadados do `.zenodo.json` e publica, recebendo o DOI de volta. É o mesmo que a integração GitHub↔Zenodo faria sozinha — ela existe, mas está quebrada para esta conta (ver passo 1).

São dois DOIs, e vale entender a diferença:

| DOI | Valor | O que identifica | Onde usar |
|---|---|---|---|
| **Concept DOI** | `10.5281/zenodo.22220024` | a obra como um todo — resolve sempre para a versão mais recente | citação geral, Lattes, ORCID, rodapé do site |
| **Version DOI** | `10.5281/zenodo.22220025` (v1.0.0) | uma versão específica | quando o texto precisa apontar para o estado exato consultado |

Ambos vivem em `build/config.py` (`DOI`, `DOI_VERSAO`, `VERSAO`, `DATA_VERSAO`) e de lá alimentam o `CITATION.cff` e o rodapé do site. A cada novo depósito, atualize `DOI_VERSAO`, `VERSAO` e `DATA_VERSAO` — o conceitual não muda nunca.

O *concept DOI* só nasce a partir da primeira versão publicada, e é ele que vai para o Lattes, o ORCID e o rodapé do site.

## Fontes dos metadados

Nada é digitado à mão no Zenodo. Tudo sai de `build/config.py → AUTORES`:

```bash
.venv/bin/python build/citacao.py    # regera CITATION.cff e .zenodo.json
```

- `.zenodo.json` — título, resumo em HTML, os 8 autores com ORCID e afiliação, `upload_type: software`, licença CC BY 4.0, idioma `por`, palavras-chave e o enlace para <https://weblab.aprendabit.com>.
- `CITATION.cff` — o botão *Cite this repository* do GitHub.

Se a autoria mudar, edite `config.AUTORES`, rode `citacao.py` de novo e deposite uma versão nova: o `.zenodo.json` é lido a cada depósito.

## Passo a passo

### 1. Obter o token — *feito no navegador, uma única vez*

A integração automática do GitHub **não funcionou** para esta conta: o `Sync now` de <https://zenodo.org/account/settings/github/> falha com 504 e a lista de repositórios continua congelada em um cache antigo, sem o `weblab`. É bug conhecido do InvenioRDM, não da conta. O depósito é feito, então, pela API — o que sai no mesmo lugar e ainda fica reprodutível.

1. Criar um token em <https://zenodo.org/account/settings/applications/tokens/new> com os escopos **`deposit:write`** e **`deposit:actions`**.
2. Guardar em `~/.config/zenodo/token` (ou exportar como `ZENODO_TOKEN`). O arquivo está fora do repositório de propósito.
3. Preencher o perfil do Zenodo com o **ORCID** (`0000-0002-1380-082X`) — assim o depósito entra automaticamente no ORCID.

### 2. Congelar a versão

O que entra no depósito é o repositório inteiro na tag — exceto o que o `.gitignore` corta (`site/`, `registro/`, `.venv/`). Antes de marcar:

```bash
.venv/bin/python -m pytest build/tests -q     # 36 testes
.venv/bin/python build/lint.py                # 0 erros
git status --short                            # nada solto que devesse entrar
```

### 3. Marcar a versão e depositar

```bash
git tag -a v1.0.0 -m "WebLab v1.0.0 — 57 aulas em quatro trilhas"
git push origin v1.0.0
gh release create v1.0.0 --title "WebLab v1.0.0" --notes-file <notas>   # opcional

.venv/bin/python build/publicar_zenodo.py v1.0.0 --rascunho   # confere antes
.venv/bin/python build/publicar_zenodo.py v1.0.0              # publica e emite o DOI
```

O `build/publicar_zenodo.py` monta o pacote com `git archive` na tag — só arquivos versionados, sem `site/`, `registro/` nem `.venv/` —, envia os metadados do `.zenodo.json` acrescidos da versão, da data da tag e do enlace para a tag no GitHub, e publica. Aceita `--sandbox` para ensaiar em <https://sandbox.zenodo.org> com DOI de teste, e `--nova-versao=ID` para publicar uma versão nova preservando o *concept DOI*.

A mesma tag serve de ponto identificável para o pacote do INPI (`build/empacotar_registro.py`), fechando a pendência do item 9 de `docs/registro-inpi.md`.

### 4. Colher o DOI

O script imprime os dois DOIs ao publicar, e o depósito fica em <https://zenodo.org/me/uploads>. Conferir antes de divulgar:

- [ ] os 8 autores, na ordem certa, cada um com ORCID;
- [ ] licença CC BY 4.0 e acesso aberto;
- [ ] idioma português;
- [ ] o resumo em HTML formatado (parágrafos e negritos preservados).

O Zenodo permite **editar os metadados depois** sem gerar novo DOI — o que não dá para trocar são os arquivos.

### 5. Espalhar o DOI

Feito na v1.0.0:

- [x] crachá no `README.md`;
- [x] `doi:` e `identifiers:` no `CITATION.cff`, gerados de `config.DOI` por `build/citacao.py`;
- [x] "Como citar" no rodapé de toda página e na seção *Como citar* de `fontes/autores.md`.

Ainda a fazer, fora do repositório:

- [ ] **ORCID** — entra sozinho se o perfil do Zenodo estiver vinculado ao ORCID; conferir em <https://orcid.org/0000-0002-1380-082X>;
- [ ] **Currículo Lattes**, em *Material didático ou instrucional* (o registro no INPI, quando sair, vira uma entrada separada em *Software*);
- [ ] avisar os sete coautores de que o depósito saiu, com o DOI para o Lattes de cada um.

## Decisões tomadas

**`upload_type: software`.** O depósito vem do repositório, e o repositório é o gerador mais as fontes. Se em algum momento interessar depositar a *apostila* como obra à parte — o `apostila.html` ou um PDF —, o caminho é um segundo depósito manual com `upload_type: lesson`, com DOI próprio e relacionado a este por `isPartOf`. Não é necessário para citar o material.

**Sem afiliação institucional no corpo do material.** A instituição aparece na página de autores e nos metadados de cada pessoa, não como titular da obra (ver commit `6227834`).

**Licença dupla.** Conteúdo em CC BY 4.0, gerador em MIT. O Zenodo aceita uma licença só no campo estruturado: fica CC BY 4.0, e a MIT do código está no campo `notes` e no `LICENSE`.
