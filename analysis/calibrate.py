"""Calibración: capacidad sostenible de 1 réplica (0,5 vCPU).
K = mayor tasa del escalón con p95 <= 250 ms, errores < 1 % y servida >= 95 % de lo ofrecido.
Autor: Thiago Paolo Icochea Rodriguez (U22330428)"""
import sys

from common import load_run

d = sys.argv[1]
meta, k, cap = load_run(d)
dur = k[k.metric_name == "http_req_duration"]
fail = k[k.metric_name == "http_req_failed"]
drop = k[k.metric_name == "dropped_iterations"]
best = 10
print("| Escalón (sol/s) | Servidas (sol/s) | p50 (ms) | p95 (ms) | Errores (%) | CPU (%) |")
print("|---|---|---|---|---|---|")
for i, rate in enumerate([10, 20, 30, 40, 50, 60, 70, 80]):
    a, b = i * 20 + 4, i * 20 + 20  # se descartan los 4 s de transición
    d = dur[(dur.t >= a) & (dur.t < b)].metric_value
    f = fail[(fail.t >= a) & (fail.t < b)].metric_value.sum()
    dr = drop[(drop.t >= a) & (drop.t < b)].metric_value.sum()
    c = cap[(cap.t >= a) & (cap.t < b)]
    served = (len(d) - f) / (b - a)
    err = 100 * (f + dr) / max(1, len(d) + dr)
    p95 = d.quantile(0.95)
    print(f"| {rate} | {served:.1f} | {d.quantile(0.5):.0f} | {p95:.0f} | {err:.2f} | {100*c.cpu_util.mean():.0f} |")
    if p95 <= 250 and err < 1 and served >= 0.95 * rate:
        best = rate
print(f"\nK={best}")
