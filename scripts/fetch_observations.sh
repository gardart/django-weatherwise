#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Activate venv if present
if [ -f ".venv/bin/activate" ]; then
  source ".venv/bin/activate"
fi

python weatherwise/manage.py get_weather_observations --verbosity 2
