#!/usr/bin/env bash
# Prepara el Codespace: k6 (generador de carga) + dependencias de análisis.
set -e
K6_VERSION=v0.54.0
curl -fsSL "https://github.com/grafana/k6/releases/download/${K6_VERSION}/k6-${K6_VERSION}-linux-amd64.tar.gz" \
  | sudo tar -xz -C /usr/local/bin --strip-components=1 "k6-${K6_VERSION}-linux-amd64/k6"
pip install --quiet pandas matplotlib
k6 version
echo "Listo. Prueba: make experimento PATRON=D ESTRATEGIA=elastico K=<valor de calibración>"
