#!/usr/bin/env bash
# Publica o WebLab em https://weblab.aprendabit.com
# Uso: ./deploy.sh            (lint + build completo + rsync)
#      ./deploy.sh --parcial  (só as aulas existentes)
#      ./deploy.sh --forcar   (ignora erros de lint — só para pré-visualizar)
set -euo pipefail
cd "$(dirname "$0")"

PY=".venv/bin/python"
[ -x "$PY" ] || PY="python3"

"$PY" build/build.py "$@"

DESTINO="webmaster@ivanpires.dev:/home/webmaster/apps/weblab/site/"
rsync -az --delete --chmod=D755,F644 site/ "$DESTINO"

echo
echo "Publicado: https://weblab.aprendabit.com/"
