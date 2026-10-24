# Resultados — Escalabilidad y elasticidad

_Thiago Paolo Icochea Rodriguez · U22330428 · Servicios Cloud (UTP) · GitHub Actions ubuntu-latest_

## Calibración (1 réplica × 0,5 vCPU)

| Escalón (sol/s) | Servidas (sol/s) | p50 (ms) | p95 (ms) | Errores (%) | CPU (%) |
|---|---|---|---|---|---|
| 5 | 5.0 | 16 | 24 | 0.00 | 21 |
| 10 | 10.0 | 16 | 20 | 0.00 | 37 |
| 15 | 15.0 | 16 | 20 | 0.00 | 51 |
| 20 | 20.0 | 16 | 41 | 0.00 | 68 |
| 25 | 25.0 | 16 | 185 | 0.00 | 85 |
| 30 | 29.0 | 414 | 672 | 0.00 | 99 |
| 35 | 29.6 | 2065 | 2383 | 10.59 | 100 |
| 40 | 29.4 | 2147 | 2396 | 26.29 | 100 |

K=25


## Resumen por patrón y estrategia (ventana de 240 s, bins de 5 s)

| patron | estrategia | demanda_media_rps | demanda_pico_rps | servidas_rps | p95_ms | errores_pct | cpu_media_pct | replicas_min | replicas_max | vcpu_min | eficiencia_pct | cumplimiento_slo_pct | acciones |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | elastico | 16.0 | 16.2 | 16.0 | 61 | 0.0 | 39 | 1 | 2 | 3.8 | 39 | 100 | 1 |
| A | fijo | 16.0 | 16.4 | 16.0 | 146 | 0.0 | 70 | 1 | 1 | 2.0 | 71 | 100 | 0 |
| A | horizontal | 16.0 | 16.2 | 16.0 | 20 | 0.0 | 17 | 4 | 4 | 7.8 | 17 | 100 | 0 |
| A | vertical | 16.0 | 16.0 | 16.0 | 15 | 0.0 | 11 | 1 | 1 | 7.8 | 12 | 100 | 0 |
| B | elastico | 34.0 | 57.6 | 34.0 | 550 | 0.0 | 60 | 1 | 5 | 5.5 | 60 | 83 | 4 |
| B | fijo | 34.0 | 59.6 | 21.7 | 2942 | 36.19 | 89 | 1 | 1 | 2.0 | 91 | 31 | 0 |
| B | horizontal | 34.0 | 58.2 | 34.0 | 113 | 0.0 | 37 | 4 | 4 | 7.8 | 38 | 100 | 0 |
| B | vertical | 34.0 | 59.4 | 34.0 | 13 | 0.0 | 22 | 1 | 1 | 7.8 | 22 | 100 | 0 |
| C | elastico | 36.2 | 81.0 | 35.6 | 3141 | 1.59 | 57 | 1 | 6 | 7.3 | 53 | 75 | 4 |
| C | fijo | 36.2 | 70.8 | 21.8 | 2274 | 39.6 | 71 | 1 | 1 | 2.0 | 72 | 50 | 0 |
| C | horizontal | 36.2 | 71.6 | 36.2 | 3241 | 0.0 | 49 | 4 | 4 | 7.8 | 50 | 62 | 0 |
| C | programado | 36.2 | 73.4 | 36.0 | 3782 | 0.4 | 68 | 1 | 4 | 5.2 | 74 | 52 | 2 |
| C | vertical | 36.2 | 70.0 | 36.2 | 23 | 0.0 | 34 | 1 | 1 | 7.8 | 34 | 100 | 0 |
| D | elastico | 31.2 | 108.0 | 26.5 | 3289 | 15.12 | 45 | 1 | 6 | 5.2 | 45 | 71 | 4 |
| D | fijo | 31.2 | 90.4 | 13.7 | 2987 | 56.17 | 60 | 1 | 1 | 2.0 | 61 | 69 | 0 |
| D | horizontal | 31.2 | 91.0 | 27.8 | 5317 | 10.87 | 40 | 4 | 4 | 7.8 | 41 | 69 | 0 |
| D | vertical | 31.2 | 90.8 | 25.3 | 1179 | 19.15 | 36 | 1 | 1 | 7.8 | 36 | 73 | 0 |

SLO: p95 < 500 ms y errores < 1 % por ventana de 5 s. Costo = vCPU·min asignadas.
