# Resultados — Escalabilidad y elasticidad

_Thiago Paolo Icochea Rodriguez · U22330428 · Servicios Cloud (UTP) · GitHub Actions ubuntu-latest_

## Calibración (1 réplica × 0,5 vCPU)

| Escalón (sol/s) | Servidas (sol/s) | p50 (ms) | p95 (ms) | Errores (%) | CPU (%) |
|---|---|---|---|---|---|
| 5 | 5.0 | 20 | 26 | 0.00 | 26 |
| 10 | 10.0 | 20 | 60 | 0.00 | 44 |
| 15 | 15.1 | 20 | 74 | 0.00 | 65 |
| 20 | 20.1 | 20 | 219 | 0.00 | 84 |
| 25 | 23.8 | 735 | 978 | 0.00 | 98 |
| 30 | 23.9 | 2536 | 2891 | 14.51 | 100 |
| 35 | 24.0 | 2581 | 2954 | 31.55 | 100 |
| 40 | 24.1 | 2564 | 2889 | 39.59 | 100 |

K=20


## Promedio de repeticiones por patrón y estrategia (240 s, ventanas de 5 s)

| patron | estrategia | demanda_media_rps | demanda_pico_rps | servidas_rps | p95_ms | errores_pct | cpu_media_pct | replicas_min | replicas_max | vcpu_min | eficiencia_pct | cpu_ms_por_sol | cumplimiento_slo_pct | acciones |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | fijo | 16.0 | 16.1 | 16.0 | 28.0 | 0.0 | 52.0 | 1.0 | 1.0 | 2.0 | 53.0 | 16.2 | 100.0 | 0.0 |
| A | vertical | 16.0 | 16.0 | 16.0 | 16.0 | 0.0 | 13.0 | 1.0 | 1.0 | 7.8 | 13.0 | 16.4 | 100.0 | 0.0 |
| A | horizontal | 16.0 | 16.0 | 16.0 | 18.0 | 0.0 | 17.0 | 4.0 | 4.0 | 7.8 | 17.0 | 20.8 | 100.0 | 0.0 |
| A | elastico | 16.0 | 16.0 | 16.0 | 28.5 | 0.0 | 52.0 | 1.0 | 1.0 | 2.0 | 53.0 | 16.3 | 100.0 | 0.0 |
| B | fijo | 34.0 | 58.9 | 22.2 | 2864.5 | 34.8 | 87.5 | 1.0 | 1.0 | 2.0 | 89.5 | 19.8 | 33.0 | 0.0 |
| B | vertical | 34.0 | 58.9 | 34.0 | 23.0 | 0.0 | 33.5 | 1.0 | 1.0 | 7.8 | 34.0 | 19.6 | 100.0 | 0.0 |
| B | horizontal | 34.0 | 59.0 | 34.0 | 174.0 | 0.0 | 40.0 | 4.0 | 4.0 | 7.8 | 41.0 | 23.5 | 100.0 | 0.0 |
| B | elastico | 34.0 | 60.1 | 34.0 | 443.0 | 0.0 | 58.5 | 1.0 | 5.5 | 5.4 | 58.0 | 23.0 | 89.0 | 4.5 |
| C | fijo | 36.2 | 70.6 | 18.2 | 2981.5 | 49.7 | 77.0 | 1.0 | 1.0 | 2.0 | 79.0 | 21.2 | 46.0 | 0.0 |
| C | vertical | 36.2 | 70.7 | 35.0 | 1163.5 | 3.4 | 47.5 | 1.0 | 1.0 | 7.8 | 48.5 | 27.2 | 69.0 | 0.0 |
| C | horizontal | 36.2 | 72.3 | 36.2 | 3820.0 | 0.0 | 49.5 | 4.0 | 4.0 | 7.8 | 50.5 | 27.5 | 61.0 | 0.0 |
| C | programado | 36.2 | 72.2 | 36.0 | 2348.0 | 0.6 | 65.5 | 1.0 | 4.0 | 5.2 | 71.5 | 26.0 | 58.5 | 2.0 |
| C | elastico | 36.2 | 83.7 | 35.4 | 3133.0 | 1.9 | 56.0 | 1.0 | 6.0 | 7.3 | 53.0 | 27.3 | 74.0 | 4.0 |
| D | fijo | 31.2 | 90.8 | 14.8 | 2626.0 | 52.5 | 56.5 | 1.0 | 1.0 | 2.0 | 57.5 | 19.1 | 69.0 | 0.0 |
| D | vertical | 31.2 | 90.4 | 28.2 | 590.5 | 9.6 | 31.0 | 1.0 | 1.0 | 7.8 | 31.5 | 22.6 | 86.5 | 0.0 |
| D | horizontal | 31.2 | 91.1 | 31.0 | 1744.0 | 0.5 | 36.0 | 4.0 | 4.0 | 7.8 | 36.5 | 23.2 | 77.0 | 0.0 |
| D | elastico | 31.2 | 104.0 | 26.1 | 2970.5 | 16.4 | 45.5 | 1.0 | 6.0 | 5.4 | 44.0 | 23.1 | 72.0 | 4.5 |

## Detalle por repetición

| rep | patron | estrategia | demanda_media_rps | demanda_pico_rps | servidas_rps | p95_ms | errores_pct | cpu_media_pct | replicas_min | replicas_max | vcpu_min | eficiencia_pct | cpu_ms_por_sol | cumplimiento_slo_pct | acciones | reaccion_s | cpu_runner |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | A | elastico | 16.0 | 16.0 | 16.0 | 30 | 0.0 | 52 | 1 | 1 | 2.0 | 53 | 16.3 | 100 | 0 |  | AMD EPYC 9V74 80-Core Processor |
| 1 | A | fijo | 16.0 | 16.0 | 16.0 | 25 | 0.0 | 52 | 1 | 1 | 2.0 | 53 | 16.2 | 100 | 0 |  | AMD EPYC 9V74 80-Core Processor |
| 1 | A | horizontal | 16.0 | 16.0 | 16.0 | 18 | 0.0 | 17 | 4 | 4 | 7.8 | 17 | 20.8 | 100 | 0 |  | AMD EPYC 9V74 80-Core Processor |
| 1 | A | vertical | 16.0 | 16.0 | 16.0 | 16 | 0.0 | 13 | 1 | 1 | 7.8 | 13 | 16.5 | 100 | 0 |  | AMD EPYC 9V74 80-Core Processor |
| 1 | B | elastico | 34.0 | 58.6 | 34.0 | 411 | 0.0 | 57 | 1 | 6 | 5.5 | 55 | 22.0 | 90 | 4 | 45.0 | INTEL(R) XEON(R) PLATINUM 8573C |
| 1 | B | fijo | 34.0 | 59.2 | 22.7 | 2769 | 33.2 | 87 | 1 | 1 | 2.0 | 89 | 19.3 | 35 | 0 |  | INTEL(R) XEON(R) PLATINUM 8573C |
| 1 | B | horizontal | 34.0 | 58.0 | 34.0 | 139 | 0.0 | 38 | 4 | 4 | 7.8 | 39 | 22.3 | 100 | 0 |  | INTEL(R) XEON(R) PLATINUM 8573C |
| 1 | B | vertical | 34.0 | 59.2 | 34.0 | 21 | 0.0 | 32 | 1 | 1 | 7.8 | 33 | 18.9 | 100 | 0 |  | INTEL(R) XEON(R) PLATINUM 8573C |
| 1 | C | elastico | 36.2 | 84.6 | 35.6 | 2965 | 1.54 | 55 | 1 | 6 | 7.3 | 52 | 26.8 | 75 | 4 | 5.0 | AMD EPYC 7763 64-Core Processor |
| 1 | C | fijo | 36.2 | 71.0 | 18.3 | 2969 | 49.43 | 77 | 1 | 1 | 2.0 | 79 | 21.1 | 46 | 0 |  | AMD EPYC 7763 64-Core Processor |
| 1 | C | horizontal | 36.2 | 72.4 | 36.2 | 3554 | 0.0 | 49 | 4 | 4 | 7.8 | 50 | 27.3 | 62 | 0 |  | AMD EPYC 7763 64-Core Processor |
| 1 | C | programado | 36.2 | 73.2 | 35.9 | 678 | 0.66 | 64 | 1 | 4 | 5.2 | 69 | 25.2 | 65 | 2 |  | AMD EPYC 7763 64-Core Processor |
| 1 | C | vertical | 36.2 | 70.6 | 35.0 | 1168 | 3.35 | 47 | 1 | 1 | 7.8 | 48 | 27.1 | 69 | 0 |  | AMD EPYC 7763 64-Core Processor |
| 1 | D | elastico | 31.2 | 107.0 | 27.0 | 2321 | 13.64 | 42 | 1 | 6 | 5.2 | 41 | 19.5 | 75 | 4 | 5.0 | AMD EPYC 9V74 80-Core Processor |
| 1 | D | fijo | 31.2 | 90.8 | 16.0 | 2267 | 48.82 | 53 | 1 | 1 | 2.0 | 54 | 16.4 | 69 | 0 |  | AMD EPYC 9V74 80-Core Processor |
| 1 | D | horizontal | 31.2 | 93.4 | 31.2 | 517 | 0.0 | 33 | 4 | 4 | 7.8 | 33 | 20.9 | 83 | 0 |  | AMD EPYC 9V74 80-Core Processor |
| 1 | D | vertical | 31.2 | 90.2 | 31.2 | 23 | 0.0 | 27 | 1 | 1 | 7.8 | 27 | 17.1 | 100 | 0 |  | AMD EPYC 9V74 80-Core Processor |
| 2 | A | elastico | 16.0 | 16.0 | 16.0 | 27 | 0.0 | 52 | 1 | 1 | 2.0 | 53 | 16.3 | 100 | 0 |  | AMD EPYC 9V74 80-Core Processor |
| 2 | A | fijo | 16.0 | 16.2 | 16.0 | 31 | 0.0 | 52 | 1 | 1 | 2.0 | 53 | 16.3 | 100 | 0 |  | AMD EPYC 9V74 80-Core Processor |
| 2 | A | horizontal | 16.0 | 16.0 | 16.0 | 18 | 0.0 | 17 | 4 | 4 | 7.8 | 17 | 20.9 | 100 | 0 |  | AMD EPYC 9V74 80-Core Processor |
| 2 | A | vertical | 16.0 | 16.0 | 16.0 | 16 | 0.0 | 13 | 1 | 1 | 7.8 | 13 | 16.4 | 100 | 0 |  | AMD EPYC 9V74 80-Core Processor |
| 2 | B | elastico | 34.0 | 61.6 | 34.0 | 475 | 0.0 | 60 | 1 | 5 | 5.4 | 61 | 24.0 | 88 | 5 | 45.0 | AMD EPYC 7763 64-Core Processor |
| 2 | B | fijo | 34.0 | 58.6 | 21.6 | 2960 | 36.38 | 88 | 1 | 1 | 2.0 | 90 | 20.4 | 31 | 0 |  | AMD EPYC 7763 64-Core Processor |
| 2 | B | horizontal | 34.0 | 60.0 | 34.0 | 209 | 0.0 | 42 | 4 | 4 | 7.8 | 43 | 24.7 | 100 | 0 |  | AMD EPYC 7763 64-Core Processor |
| 2 | B | vertical | 34.0 | 58.6 | 34.0 | 25 | 0.0 | 35 | 1 | 1 | 7.8 | 35 | 20.3 | 100 | 0 |  | AMD EPYC 7763 64-Core Processor |
| 2 | C | elastico | 36.2 | 82.8 | 35.3 | 3301 | 2.29 | 57 | 1 | 6 | 7.3 | 54 | 27.8 | 73 | 4 | 5.0 | AMD EPYC 7763 64-Core Processor |
| 2 | C | fijo | 36.2 | 70.2 | 18.1 | 2994 | 49.95 | 77 | 1 | 1 | 2.0 | 79 | 21.4 | 46 | 0 |  | AMD EPYC 7763 64-Core Processor |
| 2 | C | horizontal | 36.2 | 72.2 | 36.2 | 4086 | 0.02 | 50 | 4 | 4 | 7.8 | 51 | 27.7 | 60 | 0 |  | AMD EPYC 7763 64-Core Processor |
| 2 | C | programado | 36.2 | 71.2 | 36.0 | 4018 | 0.58 | 67 | 1 | 4 | 5.2 | 74 | 26.7 | 52 | 2 |  | AMD EPYC 7763 64-Core Processor |
| 2 | C | vertical | 36.2 | 70.8 | 34.9 | 1159 | 3.4 | 48 | 1 | 1 | 7.8 | 49 | 27.3 | 69 | 0 |  | AMD EPYC 7763 64-Core Processor |
| 2 | D | elastico | 31.2 | 101.0 | 25.2 | 3620 | 19.23 | 49 | 1 | 6 | 5.7 | 47 | 26.7 | 69 | 5 | 5.0 | AMD EPYC 7763 64-Core Processor |
| 2 | D | fijo | 31.2 | 90.8 | 13.7 | 2985 | 56.18 | 60 | 1 | 1 | 2.0 | 61 | 21.8 | 69 | 0 |  | AMD EPYC 7763 64-Core Processor |
| 2 | D | horizontal | 31.2 | 88.8 | 30.9 | 2971 | 0.99 | 39 | 4 | 4 | 7.8 | 40 | 25.4 | 71 | 0 |  | AMD EPYC 7763 64-Core Processor |
| 2 | D | vertical | 31.2 | 90.6 | 25.3 | 1158 | 19.16 | 35 | 1 | 1 | 7.8 | 36 | 28.1 | 73 | 0 |  | AMD EPYC 7763 64-Core Processor |

SLO: p95 < 500 ms y errores < 1 % por ventana de 5 s. Costo = vCPU·min asignadas.
