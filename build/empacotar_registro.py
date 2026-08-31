"""Empacota o código-fonte do WebLab para o registro de programa de computador (INPI).

Gera, em `registro/`:

- `weblab-codigo-fonte.zip` — o código do sistema (gerador, tema, comportamento,
  publicação e testes), sem o conteúdo didático em Markdown, que é obra
  literária e tem proteção autoral própria.
- `weblab-codigo-fonte.hash.txt` — os resumos SHA-512 e SHA-256 do .zip, o
  formato que o e-Software do INPI pede para garantir a integridade do depósito.
- `weblab-listagem.txt` — inventário dos arquivos com tamanho e nº de linhas,
  útil para o formulário e para a conferência do NIT.

Uso: .venv/bin/python build/empacotar_registro.py

O .zip é determinístico (ordem fixa e data fixa nas entradas), então o hash só
muda quando o código muda de verdade — o que permite repetir o cálculo e chegar
ao mesmo resultado durante a conferência.
"""
import hashlib
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "registro"
DATA_FIXA = (2026, 1, 1, 0, 0, 0)  # entradas com data fixa → zip reprodutível

# Código do sistema. O conteúdo em fontes/*.md fica de fora de propósito.
PADROES = [
    "build/*.py",
    "build/*.css",
    "build/*.js",
    "build/tests/*.py",
    "deploy.sh",
]


def arquivos():
    achados = []
    for padrao in PADROES:
        achados += sorted(RAIZ.glob(padrao))
    return [a for a in achados if a.is_file() and "__pycache__" not in a.parts]


def main():
    itens = arquivos()
    if not itens:
        print("nenhum arquivo encontrado — rode a partir da raiz do repositório", file=sys.stderr)
        return 1
    SAIDA.mkdir(exist_ok=True)
    zip_path = SAIDA / "weblab-codigo-fonte.zip"

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for a in itens:
            rel = a.relative_to(RAIZ).as_posix()
            info = zipfile.ZipInfo(rel, date_time=DATA_FIXA)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, a.read_bytes())

    dados = zip_path.read_bytes()
    sha512 = hashlib.sha512(dados).hexdigest()
    sha256 = hashlib.sha256(dados).hexdigest()

    linhas_totais = 0
    listagem = ["Arquivo,linhas,bytes"]
    for a in itens:
        n = len(a.read_text(encoding="utf-8", errors="replace").splitlines())
        linhas_totais += n
        listagem.append(f"{a.relative_to(RAIZ).as_posix()},{n},{a.stat().st_size}")
    listagem.append(f"TOTAL,{linhas_totais},{len(dados)}")
    (SAIDA / "weblab-listagem.txt").write_text("\n".join(listagem) + "\n", encoding="utf-8")

    (SAIDA / "weblab-codigo-fonte.hash.txt").write_text(
        "Resumo digital (hash) do arquivo weblab-codigo-fonte.zip\n"
        "Programa: WebLab — sistema de curso online aberto de desenvolvimento web\n\n"
        f"Arquivo ..... weblab-codigo-fonte.zip\n"
        f"Tamanho ..... {len(dados)} bytes\n"
        f"Arquivos .... {len(itens)}\n"
        f"Linhas ...... {linhas_totais}\n\n"
        f"SHA-512 ..... {sha512}\n"
        f"SHA-256 ..... {sha256}\n\n"
        "Confira com:\n"
        "  sha512sum weblab-codigo-fonte.zip\n"
        "  sha256sum weblab-codigo-fonte.zip\n",
        encoding="utf-8")

    print(f"{zip_path.relative_to(RAIZ)} — {len(itens)} arquivos, {linhas_totais} linhas, {len(dados)} bytes")
    print(f"SHA-512: {sha512}")
    print(f"SHA-256: {sha256}")
    print(f"Listagem e hash em {SAIDA.relative_to(RAIZ)}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
