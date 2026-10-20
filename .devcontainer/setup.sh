#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python -m venv .codespaces-venv
.codespaces-venv/bin/python -m pip install -r .devcontainer/requirements.txt
mkdir -p .codespaces-logs
if [ -d .git ]; then
  for pattern in '.codespaces-venv/' '.codespaces-logs/'; do
    grep -qxF "$pattern" .git/info/exclude || echo "$pattern" >> .git/info/exclude
  done
fi
