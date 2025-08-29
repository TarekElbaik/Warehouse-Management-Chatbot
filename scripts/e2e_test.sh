#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "[1/7] Create venvs"
python -m venv "$ROOT/.venv-classifier"
python -m venv "$ROOT/.venv-llm"
python -m venv "$ROOT/.venv-rasa"

echo "[2/7] Install deps & train classifier"
source "$ROOT/.venv-classifier/bin/activate"
pip install -r "$ROOT/services/classifier/requirements.txt" -q
python "$ROOT/services/classifier/train_classifier.py" > /dev/null
deactivate

echo "[3/7] Install LLM deps"
source "$ROOT/.venv-llm/bin/activate"
pip install -r "$ROOT/services/llm/requirements.txt" -q
deactivate

echo "[4/7] Install Rasa deps & train model"
source "$ROOT/.venv-rasa/bin/activate"
pip install -r "$ROOT/rasa/requirements.txt" -q
rasa train --domain "$ROOT/rasa/domain.yml" --data "$ROOT/rasa/data" --config "$ROOT/rasa/config.yml" > /dev/null
deactivate

echo "[5/7] Start services"
source "$ROOT/.venv-classifier/bin/activate"; python "$ROOT/services/classifier/app.py" & CLF_PID=$!; deactivate
source "$ROOT/.venv-llm/bin/activate"; python "$ROOT/services/llm/app.py" & LLM_PID=$!; deactivate
source "$ROOT/.venv-rasa/bin/activate"; rasa run --enable-api -p 5005 --endpoints "$ROOT/rasa/endpoints.yml" --credentials "$ROOT/rasa/credentials.yml" & RASA_PID=$!
rasa run actions --actions actions --port 5055 & ACTIONS_PID=$!
deactivate

sleep 8

cleanup() {
  echo "[CLEANUP]"
  kill $CLF_PID $LLM_PID $RASA_PID $ACTIONS_PID 2>/dev/null || true
}
trap cleanup EXIT

echo "[6/7] Send test messages"
check() {
  local msg="$1"; local expect="$2"
  out="$(curl -s -X POST http://localhost:5005/webhooks/rest/webhook -H 'Content-Type: application/json' -d "{\"sender\":\"test\",\"message\":\"$msg\"}")"
  echo "User: $msg"
  echo "Bot: $out"
  echo "$out" | grep -i "$expect" >/dev/null
}

check "hi" "assist"
check "where is order 1002" "1002"
check "reschedule order 1002 to 2025-09-02" "Rescheduled order 1002"
check "bye" "Goodbye"

echo "[7/7] E2E OK ✅"

