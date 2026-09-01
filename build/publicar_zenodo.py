"""Deposita uma versão do WebLab no Zenodo e emite o DOI.

Faz pela API o que a integração GitHub↔Zenodo faria sozinha — que hoje falha ao
sincronizar a lista de repositórios (bug conhecido do InvenioRDM). O resultado é
o mesmo, com a vantagem de ser reprodutível e de viver no repositório.

O pacote enviado sai de `git archive` na tag: só arquivos versionados, sem
`site/`, `registro/` nem `.venv/`, e sempre igual para a mesma tag. Os metadados
saem de `.zenodo.json` — gerado por `build/citacao.py` a partir de
`config.AUTORES` —, acrescidos da versão, da data da tag e do enlace para a tag
no GitHub.

Uso:

    export ZENODO_TOKEN=...                      # ou ~/.config/zenodo/token
    .venv/bin/python build/publicar_zenodo.py v1.0.0

    --sandbox           deposita em sandbox.zenodo.org (DOI de teste, 10.5072)
    --rascunho          envia tudo mas não publica; a revisão final fica no site
    --nova-versao ID    nova versão do depósito ID, preservando o concept DOI

O token precisa dos escopos `deposit:write` e `deposit:actions`, criado em
https://zenodo.org/account/settings/applications/tokens/new

Publicar é irreversível: o DOI é registrado e os arquivos não podem mais ser
trocados (os metadados, sim). Para conferir antes, use --rascunho ou --sandbox.
"""
import json
import mimetypes
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
REPO = "https://github.com/ivanlppires/weblab"
TOKEN_ARQUIVO = Path.home() / ".config" / "zenodo" / "token"


def token():
    """Lê o token do ambiente ou de ~/.config/zenodo/token."""
    t = os.environ.get("ZENODO_TOKEN", "").strip()
    if not t and TOKEN_ARQUIVO.exists():
        t = TOKEN_ARQUIVO.read_text(encoding="utf-8").strip()
    if not t:
        raise SystemExit(
            "token ausente — defina ZENODO_TOKEN ou crie ~/.config/zenodo/token.\n"
            "Gere em https://zenodo.org/account/settings/applications/tokens/new "
            "com os escopos deposit:write e deposit:actions.")
    return t


def git(*args):
    r = subprocess.run(["git", "-C", str(RAIZ), *args],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout.strip()


def pedir(url, tk, metodo="GET", corpo=None, binario=None, tipo=None):
    """Chamada à API. `corpo` vai como JSON; `binario`, como bytes crus."""
    dados = binario if binario is not None else (
        json.dumps(corpo).encode() if corpo is not None else None)
    req = urllib.request.Request(url, data=dados, method=metodo)
    req.add_header("Authorization", f"Bearer {tk}")
    if binario is not None:
        req.add_header("Content-Type", tipo or "application/octet-stream")
    elif corpo is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            texto = r.read().decode()
            return json.loads(texto) if texto.strip() else {}
    except urllib.error.HTTPError as e:
        detalhe = e.read().decode(errors="replace")
        try:  # o Zenodo devolve os erros de validação campo a campo
            j = json.loads(detalhe)
            detalhe = json.dumps(j, ensure_ascii=False, indent=2)
        except json.JSONDecodeError:
            pass
        raise SystemExit(f"Zenodo respondeu {e.code} em {metodo} {url}:\n{detalhe}")


def empacotar(tag, destino):
    """Gera o .zip da tag — só arquivos versionados, sempre o mesmo conteúdo."""
    subprocess.run(
        ["git", "-C", str(RAIZ), "archive", "--format=zip",
         f"--prefix=weblab-{tag}/", "-o", str(destino), tag],
        check=True)
    return destino


def metadados(tag):
    """Metadados do .zenodo.json mais o que depende da tag."""
    m = json.loads((RAIZ / ".zenodo.json").read_text(encoding="utf-8"))
    m["version"] = tag.lstrip("v")
    m["publication_date"] = git("log", "-1", "--format=%cs", tag)
    m.setdefault("related_identifiers", []).append(
        {"identifier": f"{REPO}/tree/{tag}", "relation": "isSupplementTo",
         "resource_type": "software", "scheme": "url"})
    return m


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    op = [a for a in argv if a.startswith("--")]
    if len(args) != 1:
        print(__doc__.split("Uso:")[1].split("O token")[0].strip(), file=sys.stderr)
        return 2
    tag = args[0]
    sandbox = "--sandbox" in op
    rascunho = "--rascunho" in op
    anterior = next((a.split("=", 1)[1] for a in op if a.startswith("--nova-versao=")), None)

    base = "https://sandbox.zenodo.org/api" if sandbox else "https://zenodo.org/api"
    tk = token()

    if tag not in git("tag").splitlines():
        raise SystemExit(f"tag {tag} não existe — crie-a antes de depositar")

    meta = metadados(tag)
    zip_path = RAIZ / f"registro/weblab-{tag}.zip"
    zip_path.parent.mkdir(exist_ok=True)
    empacotar(tag, zip_path)
    print(f"pacote: {zip_path.relative_to(RAIZ)} ({zip_path.stat().st_size} bytes)")

    if anterior:  # nova versão herda o concept DOI do depósito anterior
        r = pedir(f"{base}/deposit/depositions/{anterior}/actions/newversion", tk, "POST")
        dep = pedir(r["links"]["latest_draft"], tk)
        for f in dep.get("files", []):  # o rascunho vem com os arquivos da versão anterior
            pedir(f"{base}/deposit/depositions/{dep['id']}/files/{f['id']}", tk, "DELETE")
    else:
        dep = pedir(f"{base}/deposit/depositions", tk, "POST", {"metadata": meta})

    dep_id = dep["id"]
    print(f"depósito {dep_id} criado em {base.removesuffix('/api')}")

    tipo = mimetypes.guess_type(zip_path.name)[0] or "application/zip"
    pedir(f"{dep['links']['bucket']}/{zip_path.name}", tk, "PUT",
          binario=zip_path.read_bytes(), tipo=tipo)
    print(f"arquivo enviado: {zip_path.name}")

    dep = pedir(f"{base}/deposit/depositions/{dep_id}", tk, "PUT", {"metadata": meta})
    print(f"metadados gravados: {len(meta['creators'])} autores, versão {meta['version']}")

    if rascunho:
        print(f"\nrascunho pronto, NÃO publicado — revise e publique em:\n"
              f"  {dep['links']['html']}")
        return 0

    pub = pedir(f"{base}/deposit/depositions/{dep_id}/actions/publish", tk, "POST")
    doi = pub.get("doi", "")
    conceito = pub.get("conceptdoi", "")
    print(f"\npublicado: {pub['links']['record_html']}")
    print(f"DOI desta versão ... {doi}")
    if conceito:
        print(f"DOI conceitual ..... {conceito}   ← use este para citar o WebLab")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
