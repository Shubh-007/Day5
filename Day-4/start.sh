#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="/home/labuser/Day-3/rd-evidence-retrieval-agent"

echo "Starting observability stack (otel-collector, prometheus, tempo, grafana)..."
(cd "$ROOT" && docker compose up -d)

echo "Installing OTel SDK dependencies for the app..."
pip install -r "$APP_DIR/requirements-otel.txt"

export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317"
export OTEL_SERVICE_NAME="rd-evidence-retrieval-agent"

echo
echo "================================================================================"
echo " App:        http://127.0.0.1:8080"
echo " Prometheus: http://127.0.0.1:9090"
echo " Grafana:    http://127.0.0.1:3000  (default admin/admin)"
echo "================================================================================"
echo

cd "$APP_DIR"
exec python3 -m web_server
