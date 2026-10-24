#!/usr/bin/env bash
# Ejecuta UN experimento: patrón de tráfico × estrategia de capacidad.
# Autor: Thiago Paolo Icochea Rodriguez (U22330428)
#
#   scripts/run_experiment.sh <PATRON A|B|C|D|CALIB> <ESTRATEGIA> [K] [DIR_SALIDA]
#
# Estrategias (misma imagen, misma app; solo cambia la capacidad):
#   fijo        1 réplica × 0,5 vCPU                    (capacidad base)
#   vertical    1 réplica × 2,0 vCPU                    (scale up)
#   horizontal  4 réplicas × 0,5 vCPU = 2,0 vCPU        (scale out manual)
#   elastico    1..6 réplicas × 0,5 vCPU, objetivo CPU 60 % (scale out/in automático)
#   programado  1 réplica, pasa a 4 antes del pico previsto y vuelve a 1 (scheduled scaling)
#   elastico_mejorado  2..6 réplicas, objetivo 50 %, sube >60 %, baja de a 1 réplica (propuesta del informe)
set -euo pipefail

PATTERN="${1:?patrón}"; STRATEGY="${2:?estrategia}"; K="${3:-30}"
OUT="${4:-results/raw/${PATTERN}_${STRATEGY}}"
export COMPOSE_PROJECT_NAME=shoplab
mkdir -p "$OUT"

REPLICAS=1; export CPUS=0.5 WORKERS=2; MODE=observe; EXTRA=""
case "$STRATEGY" in
  fijo)       ;;
  vertical)   export CPUS=2.0 WORKERS=8 ;;
  horizontal) REPLICAS=4 ;;
  elastico)   MODE=elastic; EXTRA="--min 1 --max 6 --target 0.60 --scale-out-at 0.70 --scale-in-at 0.35" ;;
  programado) MODE=scheduled; EXTRA="--schedule 66:4,200:1" ;;
  elastico_mejorado) REPLICAS=2; MODE=elastic
              EXTRA="--min 2 --max 6 --target 0.50 --scale-out-at 0.60 --scale-in-at 0.30 --scale-out-cooldown 10 --scale-in-window 45 --scale-in-step 1" ;;
  *) echo "estrategia desconocida: $STRATEGY"; exit 1 ;;
esac

DURATION=250; [ "$PATTERN" = "CALIB" ] && DURATION=170

echo "== Patrón $PATTERN | Estrategia $STRATEGY | réplicas=$REPLICAS cpus=$CPUS workers=$WORKERS K=$K"
docker compose down -v --remove-orphans >/dev/null 2>&1 || true
docker compose build --quiet web
docker compose up -d --scale web="$REPLICAS"

# Esperar a que todas las réplicas estén sanas (capacidad inicial lista)
for i in $(seq 1 60); do
  ok=$(docker ps --filter label=lab.role=web --filter health=healthy -q | wc -l)
  [ "$ok" -ge "$REPLICAS" ] && break; sleep 1
done
curl -fsS localhost:8080/api/checkout >/dev/null
echo "réplicas sanas: $ok"

python3 autoscaler/autoscaler.py --mode "$MODE" --cpus "$CPUS" --duration "$DURATION" \
  --out "$OUT/capacity.csv" $EXTRA > "$OUT/autoscaler.log" 2>&1 &
MON=$!

date +%s.%N > "$OUT/k6_start_epoch.txt"
k6 run --quiet -e PATTERN="$PATTERN" -e K="$K" \
  --out csv="$OUT/k6.csv" --summary-export "$OUT/k6_summary.json" load/patterns.js \
  > "$OUT/k6.log" 2>&1 || true

wait $MON || true
docker compose logs --no-color > "$OUT/compose.log" 2>&1 || true
cat > "$OUT/meta.json" <<EOF
{"pattern":"$PATTERN","strategy":"$STRATEGY","K":$K,"replicas_initial":$REPLICAS,"cpus_per_replica":$CPUS,
 "workers":$WORKERS,"mode":"$MODE","extra":"$EXTRA","runner_cpus":$(nproc),
 "runner_cpu_model":"$(lscpu | sed -n 's/^Model name: *//p' | head -1)","rep":"${REP:-1}",
 "autor":"Thiago Paolo Icochea Rodriguez","codigo":"U22330428"}
EOF
gzip -f "$OUT/k6.csv"
# Buenas prácticas: eliminar los recursos creados para la práctica
docker compose down -v --remove-orphans
echo "== listo: $OUT"
