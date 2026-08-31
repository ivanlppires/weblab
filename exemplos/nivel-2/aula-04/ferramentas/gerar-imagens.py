#!/usr/bin/env python3
"""Gera as imagens de exemplo (placeholders) do Café Cerrado.

Os arquivos de imagem NÃO ficam versionados no repositório: este script os
recria a partir de nada, com a paleta da marca e o nome do produto escrito
em cima. Servem para a aula rodar offline, sem baixar foto de lugar nenhum
e sem problema de direito autoral.

Uso:  python3 ferramentas/gerar-imagens.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

DESTINO = Path(__file__).resolve().parent.parent / "cafe-cerrado" / "img"

# Paleta da marca (a mesma do css/estilo.css).
MARCA = (111, 78, 55)
MARCA_ESCURA = (74, 51, 37)
DESTAQUE = (194, 112, 61)
CREME = (253, 250, 246)

FONTES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]

IMAGENS = [
    ("fachada.jpg", "Fachada", 1200, 800, MARCA_ESCURA),
    ("grao-cerrado.jpg", "Grãos verdes", 1000, 667, MARCA),
    ("espresso.jpg", "Espresso", 1200, 900, MARCA_ESCURA),
    ("coado.jpg", "Coado da Casa", 1200, 900, MARCA),
    ("cappuccino.jpg", "Cappuccino", 1200, 900, DESTAQUE),
    ("latte.jpg", "Latte de Baunilha", 1200, 900, MARCA),
    ("cold-brew.jpg", "Cold Brew", 1200, 900, MARCA_ESCURA),
    ("frappe.jpg", "Frappê de Café", 1200, 900, DESTAQUE),
    ("pao-de-queijo.jpg", "Pão de Queijo", 1200, 900, MARCA),
    ("torta-de-frango.jpg", "Torta de Frango", 1200, 900, DESTAQUE),
    ("bolo-de-milho.jpg", "Bolo de Milho", 1200, 900, MARCA),
    ("brownie.jpg", "Brownie", 1200, 900, MARCA_ESCURA),
]


def carregar_fonte(tamanho):
    for caminho in FONTES:
        if Path(caminho).exists():
            return ImageFont.truetype(caminho, tamanho)
    return ImageFont.load_default()


def gerar(nome, titulo, largura, altura, cor):
    imagem = Image.new("RGB", (largura, altura), cor)
    pincel = ImageDraw.Draw(imagem)

    # Faixas diagonais claras, só para a imagem não ser um retângulo chapado.
    for x in range(-altura, largura, 90):
        pincel.polygon(
            [(x, altura), (x + 45, altura), (x + 45 + altura, 0), (x + altura, 0)],
            fill=tuple(min(255, c + 14) for c in cor),
        )

    fonte_titulo = carregar_fonte(int(largura * 0.055))
    fonte_aviso = carregar_fonte(int(largura * 0.028))

    pincel.text((largura / 2, altura / 2 - largura * 0.03), titulo,
                font=fonte_titulo, fill=CREME, anchor="mm")
    pincel.text((largura / 2, altura / 2 + largura * 0.045), "imagem de exemplo · Café Cerrado",
                font=fonte_aviso, fill=(255, 255, 255, 200), anchor="mm")

    imagem.save(DESTINO / nome, "JPEG", quality=78, optimize=True)
    return (DESTINO / nome).stat().st_size


def main():
    DESTINO.mkdir(parents=True, exist_ok=True)
    total = 0
    for args in IMAGENS:
        total += gerar(*args)
        print(f"  {args[0]:<22} {args[2]}x{args[3]}")
    print(f"\n{len(IMAGENS)} imagens em {DESTINO} ({total / 1024:.0f} KB no total)")


if __name__ == "__main__":
    main()
