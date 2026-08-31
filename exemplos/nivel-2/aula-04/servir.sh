#!/usr/bin/env bash
# Sobe um servidor estático na pasta desta aula.
# Abrir os arquivos com file:// funciona para quase tudo, mas quebra os
# <iframe> de algumas demos e o importmap do Material Web. Use isto.
set -euo pipefail

PORTA="${1:-8004}"
cd "$(dirname "$0")"

echo "WebLab · Nível 2 · Aula 04 — exemplos"
echo
echo "  Painel de demos:  http://localhost:${PORTA}/demos/"
echo "  Café Cerrado:     http://localhost:${PORTA}/cafe-cerrado/"
echo "  Gabaritos:        http://localhost:${PORTA}/gabaritos/"
echo
echo "Ctrl+C para parar."
echo

python3 -m http.server "${PORTA}"
