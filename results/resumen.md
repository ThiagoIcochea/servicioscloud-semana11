# Resultados — Escalabilidad y elasticidad

_Thiago Paolo Icochea Rodriguez · U22330428 · Servicios Cloud (UTP) · GitHub Actions ubuntu-latest_

## Calibración (1 réplica × 0,5 vCPU)

| Escalón (sol/s) | Servidas (sol/s) | p50 (ms) | p95 (ms) | Errores (%) | CPU (%) |
|---|---|---|---|---|---|
| 5 | 5.0 | 16 | 20 | 0.00 | 21 |
| 10 | 10.0 | 16 | 34 | 0.00 | 36 |
| 15 | 15.0 | 16 | 20 | 0.00 | 51 |
| 20 | 20.0 | 16 | 52 | 0.00 | 68 |
| 25 | 25.0 | 16 | 177 | 0.00 | 85 |
| 30 | 29.6 | 341 | 493 | 0.00 | 99 |
| 35 | 30.1 | 2028 | 2298 | 8.03 | 100 |
| 40 | 30.1 | 2087 | 2346 | 24.69 | 100 |

K=25


## Promedio de repeticiones por patrón y estrategia (240 s, ventanas de 5 s)

| patron | estrategia | demanda_media_rps | demanda_pico_rps | servidas_rps | p95_ms | errores_pct | cpu_media_pct | replicas_min | replicas_max | vcpu_min | eficiencia_pct | cpu_ms_por_sol | cumplimiento_slo_pct | acciones |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | fijo | 16.0 | 16.2 | 16.0 | 83.0 | 0.0 | 60.0 | 1.0 | 1.0 | 2.0 | 61.0 | 18.8 | 100.0 | 0.0 |
| A | vertical | 16.0 | 16.0 | 16.0 | 18.0 | 0.0 | 15.0 | 1.0 | 1.0 | 7.8 | 15.0 | 18.8 | 100.0 | 0.0 |
| A | horizontal | 16.0 | 16.1 | 16.0 | 25.5 | 0.0 | 19.0 | 4.0 | 4.0 | 7.8 | 19.5 | 24.0 | 100.0 | 0.0 |
| A | elastico | 16.0 | 16.3 | 16.0 | 48.5 | 0.0 | 46.0 | 1.0 | 1.5 | 2.9 | 46.0 | 19.8 | 100.0 | 0.5 |
| A | elastico_mejorado | 16.0 | 16.3 | 16.0 | 29.0 | 0.0 | 32.5 | 2.0 | 2.0 | 3.9 | 33.0 | 20.4 | 100.0 | 0.0 |
| B | fijo | 34.0 | 58.7 | 21.8 | 2927.5 | 36.1 | 88.5 | 1.0 | 1.0 | 2.0 | 90.0 | 20.4 | 32.0 | 0.0 |
| B | vertical | 34.0 | 58.6 | 34.0 | 23.5 | 0.0 | 34.0 | 1.0 | 1.0 | 7.8 | 35.0 | 20.0 | 100.0 | 0.0 |
| B | horizontal | 34.0 | 59.8 | 34.0 | 180.5 | 0.0 | 40.5 | 4.0 | 4.0 | 7.8 | 41.5 | 24.0 | 99.0 | 0.0 |
| B | elastico | 34.0 | 60.3 | 34.0 | 336.0 | 0.0 | 60.0 | 1.0 | 5.0 | 5.4 | 60.0 | 23.4 | 88.5 | 4.5 |
| B | elastico_mejorado | 34.0 | 58.8 | 34.0 | 237.5 | 0.0 | 47.0 | 2.0 | 6.0 | 6.8 | 48.0 | 23.8 | 95.0 | 3.5 |
| C | fijo | 36.2 | 70.4 | 21.2 | 2467.5 | 41.3 | 72.5 | 1.0 | 1.0 | 2.0 | 73.5 | 17.5 | 50.0 | 0.0 |
| C | vertical | 36.2 | 70.3 | 35.6 | 585.0 | 1.5 | 36.5 | 1.0 | 1.0 | 7.8 | 37.5 | 20.5 | 84.5 | 0.0 |
| C | horizontal | 36.2 | 70.0 | 36.1 | 1975.0 | 0.3 | 41.0 | 4.0 | 4.0 | 7.8 | 41.5 | 22.6 | 80.0 | 0.0 |
| C | programado | 36.2 | 70.8 | 36.2 | 1197.5 | 0.0 | 53.0 | 1.0 | 4.0 | 5.2 | 56.5 | 20.4 | 78.0 | 2.0 |
| C | elastico | 36.2 | 88.6 | 35.2 | 3230.5 | 2.7 | 49.0 | 1.0 | 6.0 | 7.0 | 46.0 | 22.8 | 77.0 | 4.0 |
| C | elastico_mejorado | 36.2 | 83.0 | 36.1 | 1897.5 | 0.2 | 37.5 | 2.0 | 6.0 | 8.2 | 38.0 | 21.8 | 86.5 | 3.5 |
| D | fijo | 31.2 | 90.4 | 15.6 | 2485.5 | 50.3 | 55.0 | 1.0 | 1.0 | 2.0 | 56.5 | 18.2 | 69.0 | 0.0 |
| D | vertical | 31.2 | 90.2 | 28.1 | 613.0 | 9.9 | 29.0 | 1.0 | 1.0 | 7.8 | 30.0 | 21.4 | 86.5 | 0.0 |
| D | horizontal | 31.2 | 90.3 | 30.8 | 1841.5 | 1.3 | 33.0 | 4.0 | 4.0 | 7.8 | 34.0 | 21.5 | 85.5 | 0.0 |
| D | elastico | 31.2 | 104.3 | 25.9 | 3194.0 | 17.1 | 44.5 | 1.0 | 6.0 | 5.4 | 42.5 | 22.4 | 73.0 | 4.5 |
| D | elastico_mejorado | 31.2 | 105.1 | 29.5 | 3182.5 | 5.5 | 33.0 | 2.0 | 6.0 | 8.8 | 32.5 | 24.4 | 78.0 | 4.5 |

## Detalle por repetición

| rep | patron | estrategia | demanda_media_rps | demanda_pico_rps | servidas_rps | p95_ms | errores_pct | cpu_media_pct | replicas_min | replicas_max | vcpu_min | eficiencia_pct | cpu_ms_por_sol | cumplimiento_slo_pct | acciones | reaccion_s | cpu_runner |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | A | elastico | 16.0 | 16.4 | 16.0 | 67 | 0.0 | 40 | 1 | 2 | 3.8 | 39 | 23.4 | 100 | 1 | 10.0 | AMD EPYC 7763 64-Core Processor |
| 1 | A | elastico_mejorado | 16.0 | 16.4 | 16.0 | 39 | 0.0 | 36 | 2 | 2 | 3.9 | 37 | 22.8 | 100 | 0 |  | AMD EPYC 7763 64-Core Processor |
| 1 | A | fijo | 16.0 | 16.4 | 16.0 | 133 | 0.0 | 68 | 1 | 1 | 2.0 | 69 | 21.3 | 100 | 0 |  | AMD EPYC 7763 64-Core Processor |
| 1 | A | horizontal | 16.0 | 16.2 | 16.0 | 33 | 0.0 | 21 | 4 | 4 | 7.8 | 22 | 26.9 | 100 | 0 |  | AMD EPYC 7763 64-Core Processor |
| 1 | A | vertical | 16.0 | 16.0 | 16.0 | 20 | 0.0 | 17 | 1 | 1 | 7.8 | 17 | 21.1 | 100 | 0 |  | AMD EPYC 7763 64-Core Processor |
| 1 | B | elastico | 34.0 | 61.2 | 34.0 | 371 | 0.0 | 61 | 1 | 5 | 5.2 | 62 | 23.4 | 85 | 5 | 45.0 | AMD EPYC 7763 64-Core Processor |
| 1 | B | elastico_mejorado | 34.0 | 58.2 | 34.0 | 199 | 0.0 | 48 | 2 | 6 | 6.5 | 50 | 23.8 | 100 | 4 | 80.0 | AMD EPYC 7763 64-Core Processor |
| 1 | B | fijo | 34.0 | 58.6 | 21.6 | 2966 | 36.54 | 89 | 1 | 1 | 2.0 | 90 | 20.5 | 31 | 0 |  | AMD EPYC 7763 64-Core Processor |
| 1 | B | horizontal | 34.0 | 61.0 | 34.0 | 206 | 0.0 | 41 | 4 | 4 | 7.8 | 42 | 24.3 | 98 | 0 |  | AMD EPYC 7763 64-Core Processor |
| 1 | B | vertical | 34.0 | 58.6 | 34.0 | 23 | 0.0 | 34 | 1 | 1 | 7.8 | 35 | 20.0 | 100 | 0 |  | AMD EPYC 7763 64-Core Processor |
| 1 | C | elastico | 36.2 | 92.2 | 35.7 | 2356 | 1.3 | 41 | 1 | 6 | 6.6 | 37 | 16.9 | 83 | 4 | 10.0 | AMD EPYC 9V45 96-Core Processor |
| 1 | C | elastico_mejorado | 36.2 | 76.6 | 36.2 | 340 | 0.0 | 29 | 2 | 6 | 8.0 | 28 | 15.6 | 92 | 4 | 20.0 | AMD EPYC 9V45 96-Core Processor |
| 1 | C | fijo | 36.2 | 70.6 | 24.3 | 1950 | 32.77 | 67 | 1 | 1 | 2.0 | 68 | 13.7 | 54 | 0 |  | AMD EPYC 9V45 96-Core Processor |
| 1 | C | horizontal | 36.2 | 70.6 | 36.2 | 44 | 0.0 | 30 | 4 | 4 | 7.8 | 30 | 16.3 | 100 | 0 |  | AMD EPYC 9V45 96-Core Processor |
| 1 | C | programado | 36.2 | 70.4 | 36.2 | 36 | 0.0 | 38 | 1 | 4 | 5.2 | 39 | 14.1 | 98 | 2 |  | AMD EPYC 9V45 96-Core Processor |
| 1 | C | vertical | 36.2 | 70.0 | 36.2 | 14 | 0.0 | 25 | 1 | 1 | 7.8 | 26 | 13.9 | 100 | 0 |  | AMD EPYC 9V45 96-Core Processor |
| 1 | D | elastico | 31.2 | 101.8 | 25.1 | 3811 | 19.71 | 50 | 1 | 6 | 5.7 | 48 | 27.0 | 69 | 5 | 5.0 | AMD EPYC 7763 64-Core Processor |
| 1 | D | elastico_mejorado | 31.2 | 97.0 | 28.2 | 4204 | 9.67 | 39 | 2 | 6 | 8.8 | 40 | 31.2 | 71 | 4 | 5.0 | AMD EPYC 7763 64-Core Processor |
| 1 | D | fijo | 31.2 | 90.4 | 13.5 | 3081 | 56.78 | 60 | 1 | 1 | 2.0 | 62 | 22.4 | 69 | 0 |  | AMD EPYC 7763 64-Core Processor |
| 1 | D | horizontal | 31.2 | 89.0 | 30.5 | 3558 | 2.51 | 40 | 4 | 4 | 7.8 | 41 | 26.1 | 71 | 0 |  | AMD EPYC 7763 64-Core Processor |
| 1 | D | vertical | 31.2 | 90.4 | 25.0 | 1210 | 19.88 | 36 | 1 | 1 | 7.8 | 37 | 28.6 | 73 | 0 |  | AMD EPYC 7763 64-Core Processor |
| 2 | A | elastico | 16.0 | 16.2 | 16.0 | 30 | 0.0 | 52 | 1 | 1 | 2.0 | 53 | 16.3 | 100 | 0 |  | AMD EPYC 9V74 80-Core Processor |
| 2 | A | elastico_mejorado | 16.0 | 16.2 | 16.0 | 19 | 0.0 | 29 | 2 | 2 | 3.9 | 29 | 17.9 | 100 | 0 |  | AMD EPYC 9V74 80-Core Processor |
| 2 | A | fijo | 16.0 | 16.0 | 16.0 | 33 | 0.0 | 52 | 1 | 1 | 2.0 | 53 | 16.4 | 100 | 0 |  | AMD EPYC 9V74 80-Core Processor |
| 2 | A | horizontal | 16.0 | 16.0 | 16.0 | 18 | 0.0 | 17 | 4 | 4 | 7.8 | 17 | 21.1 | 100 | 0 |  | AMD EPYC 9V74 80-Core Processor |
| 2 | A | vertical | 16.0 | 16.0 | 16.0 | 16 | 0.0 | 13 | 1 | 1 | 7.8 | 13 | 16.5 | 100 | 0 |  | AMD EPYC 9V74 80-Core Processor |
| 2 | B | elastico | 34.0 | 59.4 | 34.0 | 301 | 0.0 | 59 | 1 | 5 | 5.5 | 58 | 23.4 | 92 | 4 | 45.0 | AMD EPYC 7763 64-Core Processor |
| 2 | B | elastico_mejorado | 34.0 | 59.4 | 34.0 | 276 | 0.0 | 46 | 2 | 6 | 7.0 | 46 | 23.8 | 90 | 3 | 90.0 | AMD EPYC 7763 64-Core Processor |
| 2 | B | fijo | 34.0 | 58.8 | 21.9 | 2889 | 35.69 | 88 | 1 | 1 | 2.0 | 90 | 20.2 | 33 | 0 |  | AMD EPYC 7763 64-Core Processor |
| 2 | B | horizontal | 34.0 | 58.6 | 34.0 | 155 | 0.0 | 40 | 4 | 4 | 7.8 | 41 | 23.7 | 100 | 0 |  | AMD EPYC 7763 64-Core Processor |
| 2 | B | vertical | 34.0 | 58.6 | 34.0 | 24 | 0.0 | 34 | 1 | 1 | 7.8 | 35 | 20.1 | 100 | 0 |  | AMD EPYC 7763 64-Core Processor |
| 2 | C | elastico | 36.2 | 85.0 | 34.7 | 4105 | 4.14 | 57 | 1 | 6 | 7.3 | 55 | 28.8 | 71 | 4 | 5.0 | AMD EPYC 7763 64-Core Processor |
| 2 | C | elastico_mejorado | 36.2 | 89.4 | 36.0 | 3455 | 0.47 | 46 | 2 | 6 | 8.3 | 48 | 27.9 | 81 | 3 | 10.0 | AMD EPYC 7763 64-Core Processor |
| 2 | C | fijo | 36.2 | 70.2 | 18.2 | 2985 | 49.75 | 78 | 1 | 1 | 2.0 | 79 | 21.3 | 46 | 0 |  | AMD EPYC 7763 64-Core Processor |
| 2 | C | horizontal | 36.2 | 69.4 | 36.0 | 3906 | 0.53 | 52 | 4 | 4 | 7.8 | 53 | 28.8 | 60 | 0 |  | AMD EPYC 7763 64-Core Processor |
| 2 | C | programado | 36.2 | 71.2 | 36.2 | 2359 | 0.0 | 68 | 1 | 4 | 5.2 | 74 | 26.7 | 58 | 2 |  | AMD EPYC 7763 64-Core Processor |
| 2 | C | vertical | 36.2 | 70.6 | 35.0 | 1156 | 3.08 | 48 | 1 | 1 | 7.8 | 49 | 27.1 | 69 | 0 |  | AMD EPYC 7763 64-Core Processor |
| 2 | D | elastico | 31.2 | 106.8 | 26.7 | 2577 | 14.46 | 39 | 1 | 6 | 5.2 | 37 | 17.8 | 77 | 4 | 5.0 | AMD EPYC 9V45 96-Core Processor |
| 2 | D | elastico_mejorado | 31.2 | 113.2 | 30.8 | 2161 | 1.41 | 27 | 2 | 6 | 8.7 | 25 | 17.7 | 85 | 5 | 5.0 | AMD EPYC 9V45 96-Core Processor |
| 2 | D | fijo | 31.2 | 90.4 | 17.6 | 1890 | 43.78 | 50 | 1 | 1 | 2.0 | 51 | 14.1 | 69 | 0 |  | AMD EPYC 9V45 96-Core Processor |
| 2 | D | horizontal | 31.2 | 91.6 | 31.2 | 125 | 0.0 | 26 | 4 | 4 | 7.8 | 27 | 16.8 | 100 | 0 |  | AMD EPYC 9V45 96-Core Processor |
| 2 | D | vertical | 31.2 | 90.0 | 31.2 | 16 | 0.0 | 22 | 1 | 1 | 7.8 | 23 | 14.2 | 100 | 0 |  | AMD EPYC 9V45 96-Core Processor |

SLO: p95 < 500 ms y errores < 1 % por ventana de 5 s. Costo = vCPU·min asignadas.
