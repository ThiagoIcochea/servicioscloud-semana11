#!/bin/sh
# Simula el tiempo que tarda una instancia nueva en estar lista (boot + warm-up).
echo "[$(hostname)] arrancando, warm-up de ${WARMUP_SECONDS}s"
sleep "${WARMUP_SECONDS}"
exec gunicorn --bind 0.0.0.0:8000 --workers "${WORKERS}" --threads 1 \
     --backlog 64 --timeout 30 --log-level warning app:app
