#!/usr/bin/env bash
# 🔬 Investigue (§3.3) — prova, no terminal e na frente da turma, que a hash
# do integrity não é mágica: é o SHA-384 do arquivo, em base64.
set -euo pipefail

URL="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
ESPERADA="QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
cd "$TMP"

echo "1) Baixando o arquivo da CDN…"
echo "   $URL"
curl -sO "$URL"
printf '   %s bytes\n\n' "$(wc -c < bootstrap.min.css)"

echo "2) Calculando o SHA-384 e codificando em base64:"
echo "   openssl dgst -sha384 -binary bootstrap.min.css | openssl base64 -A"
CALCULADA="$(openssl dgst -sha384 -binary bootstrap.min.css | openssl base64 -A)"
printf '\n   calculada: %s\n' "$CALCULADA"
printf '   no HTML:   %s\n\n' "$ESPERADA"

if [ "$CALCULADA" = "$ESPERADA" ]; then
  echo "   ✅ IDÊNTICAS. É esta conta que o navegador refaz a cada carregamento."
else
  echo "   ❌ DIFERENTES. Ou a CDN mudou o arquivo, ou a hash do exemplo está desatualizada."
fi

echo
echo "3) Agora um único byte a mais — um espaço no fim do arquivo:"
printf ' ' >> bootstrap.min.css
QUEBRADA="$(openssl dgst -sha384 -binary bootstrap.min.css | openssl base64 -A)"
printf '   nova hash: %s\n\n' "$QUEBRADA"
echo "   A hash inteira mudou por causa de um caractere. É isso que o SRI detecta:"
echo "   se um byte for diferente, o navegador BLOQUEIA o recurso e a página fica sem estilo."
echo
echo "   Veja o bloqueio acontecendo em: demos/erros/sri-quebrada.html"
