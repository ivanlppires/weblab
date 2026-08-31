#!/usr/bin/env bash
# Plano B para quando a internet da sala cair.
#
#   ./ferramentas/preparar-offline.sh            baixa os arquivos para vendor/
#   ./ferramentas/preparar-offline.sh --aplicar  troca as URLs da CDN por vendor/ local
#   ./ferramentas/preparar-offline.sh --reverter volta tudo para a CDN
#
# Os caminhos aplicados são absolutos (/vendor/…), então só funcionam com o
# servidor de ./servir.sh, cuja raiz é a pasta desta aula.
#
# O que NÃO fica offline: o Material Web (esm.run importa outros módulos em
# cadeia) e o Google Fonts. As demos 10 e a bancada Material vão perder o estilo —
# o que, em si, é a demonstração da §6.3: sem JavaScript da rede, não sobra nada.
set -euo pipefail
cd "$(dirname "$0")/.."

BS_CSS="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
BS_JS="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
TW="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"

baixar() {
  mkdir -p vendor
  echo "Baixando para vendor/ …"
  curl -sL -o vendor/bootstrap.min.css        "$BS_CSS"
  curl -sL -o vendor/bootstrap.bundle.min.js  "$BS_JS"
  curl -sL -o vendor/tailwind-browser.js      "$TW"
  ls -lh vendor/
  echo
  echo "A hash integrity continua válida: o arquivo local é byte a byte o mesmo."
}

arquivos() { find . -name '*.html' -not -path './vendor/*'; }

aplicar() {
  [ -f vendor/bootstrap.min.css ] || baixar
  arquivos | xargs sed -i \
    -e "s#$BS_CSS#/vendor/bootstrap.min.css#g" \
    -e "s#$BS_JS#/vendor/bootstrap.bundle.min.js#g" \
    -e "s#$TW#/vendor/tailwind-browser.js#g"
  echo "✅ URLs trocadas por vendor/ local em $(arquivos | wc -l) arquivos."
  echo "   Rode ./servir.sh e teste com o Wi-Fi desligado."
}

reverter() {
  arquivos | xargs sed -i \
    -e "s#/vendor/bootstrap.min.css#$BS_CSS#g" \
    -e "s#/vendor/bootstrap.bundle.min.js#$BS_JS#g" \
    -e "s#/vendor/tailwind-browser.js#$TW#g"
  echo "✅ URLs da CDN restauradas em $(arquivos | wc -l) arquivos."
}

case "${1:-baixar}" in
  --aplicar)  aplicar ;;
  --reverter) reverter ;;
  *)          baixar ;;
esac
