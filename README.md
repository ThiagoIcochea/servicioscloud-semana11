# Servicios Cloud · Semana 11 — Escalabilidad y elasticidad ante patrones de tráfico

**Thiago Paolo Icochea Rodriguez · U22330428** — Universidad Tecnológica del Perú, curso Servicios Cloud (sección 45104), docente Dr. Eleodoro Orbegoso Carrera.

Laboratorio reproducible que compara cinco estrategias de capacidad (fija, vertical, horizontal, programada y elástica) frente a cuatro patrones de tráfico de comercio electrónico (estable, creciente, pico previsible y pico súbito), usando **GitHub Actions** como nube efímera y **GitHub Codespaces** como entorno de trabajo.

## Arquitectura

```
k6 (patrones A–D) ──HTTP──> Nginx :8080 (balanceador, DNS dinámico) ──> réplicas "web" (1..6 × 0,5 vCPU)
                                                                              ▲            │
                                                    docker compose --scale ───┘            │ CPU (cgroup) y salud
                                                                    autoescalador/monitor <┘  (cada 5 s, regla tipo HPA)
```

| Componente | Archivo | Rol |
| --- | --- | --- |
| Tienda ShopLab | `app/` | Flask + gunicorn; `/api/checkout` consume ≈17 ms de CPU por compra |
| Balanceador | `lb/nginx.conf` | Round-robin entre réplicas descubiertas por DNS |
| Autoescalador | `autoscaler/autoscaler.py` | Modos `observe`, `elastic` (objetivo CPU 60 %, 1–6 réplicas) y `scheduled` |
| Patrones de carga | `load/patterns.js` | k6 `ramping-arrival-rate`, 240 s por prueba |
| Experimento | `scripts/run_experiment.sh` | Levanta, mide, guarda y elimina los recursos |
| Análisis | `analysis/` | Calibración, métricas por ventana de 5 s y gráficos |

## Estrategias

| Estrategia | Réplicas × vCPU | Política |
| --- | --- | --- |
| fijo | 1 × 0,5 | ninguna |
| vertical | 1 × 2,0 | ninguna (scale up) |
| horizontal | 4 × 0,5 | ninguna (scale out manual) |
| programado | 1 → 4 → 1 × 0,5 | 4 réplicas en t=66 s, 1 en t=200 s (solo patrón C) |
| elastico | 1..6 × 0,5 | sube si CPU > 70 %, baja si CPU < 35 % por 30 s, objetivo 60 % |

## Ejecutar

**GitHub Actions:** pestaña *Actions → Laboratorio Escalabilidad y Elasticidad → Run workflow* (deja `k` vacío para usar la calibración). Los resultados se publican en [`results/`](results/).

**Codespaces:** *Code → Codespaces → Create codespace on main*, y luego:

```bash
make calibrar                                   # capacidad K de una réplica
make experimento PATRON=D ESTRATEGIA=elastico K=20
make todo K=20 && make analizar                 # los 17 experimentos (~75 min)
make limpiar                                    # elimina contenedores e imagen
```

## Resultados

Ver [`results/resumen.md`](results/resumen.md) y las figuras en [`results/figuras/`](results/figuras/). Los datos crudos (k6 y monitor) de cada prueba están en `results/raw/r<repetición>/<PATRÓN>_<estrategia>/`.

## Limpieza

Cada prueba termina con `docker compose down -v`, y los runners de GitHub Actions son máquinas efímeras que se destruyen al finalizar. En Codespaces, ejecutar `make limpiar` y detener el Codespace.
