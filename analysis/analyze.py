"""Análisis de los experimentos: tablas por patrón/estrategia y gráficos rotulados.
Autor: Thiago Paolo Icochea Rodriguez (U22330428) — Servicios Cloud, UTP

Uso: python3 analysis/analyze.py results/raw results
"""
import json
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from common import BIN_S, bins, load_run  # noqa: E402

RAW, OUT = sys.argv[1], sys.argv[2]
FIG = os.path.join(OUT, "figuras")
os.makedirs(FIG, exist_ok=True)

SLO_P95_MS = 500      # objetivo de nivel de servicio: p95 < 500 ms
SLO_ERR_PCT = 1.0     # y errores < 1 %
PATTERNS = {"A": "Estable", "B": "Creciente", "C": "Pico previsible", "D": "Pico súbito"}
STRATS = ["fijo", "vertical", "horizontal", "programado", "elastico"]
LABEL = {"fijo": "Fija (1×0,5 vCPU)", "vertical": "Vertical (1×2,0 vCPU)",
         "horizontal": "Horizontal (4×0,5 vCPU)", "programado": "Programada (1→4→1)",
         "elastico": "Elástica (1–6 réplicas, CPU 60 %)"}
COLOR = {"fijo": "#7a7a7a", "vertical": "#c2410c", "horizontal": "#2563eb",
         "programado": "#9333ea", "elastico": "#059669"}
FOOT = "Thiago Paolo Icochea Rodriguez · U22330428 · Servicios Cloud (UTP) · GitHub Actions ubuntu-latest"

runs = {}
for name in sorted(os.listdir(RAW)):
    d = os.path.join(RAW, name)
    if not os.path.exists(os.path.join(d, "meta.json")) or name.startswith("CALIB"):
        continue
    meta, k, cap = load_run(d)
    b = bins(k, cap, end=240)
    b.to_csv(os.path.join(d, "series_5s.csv"), index=False)
    runs[(meta["pattern"], meta["strategy"])] = (meta, k, cap, b)

cal = os.path.join(RAW, "CALIB_fijo", "calibration.txt")
if not runs:
    txt = open(cal).read() if os.path.exists(cal) else "sin datos"
    open(os.path.join(OUT, "resumen.md"), "w").write("# Calibración\n\n" + txt + "\n")
    print(txt)
    sys.exit(0)

summary = []
for (p, s), (meta, k, cap, b) in sorted(runs.items()):
    dur = k[k.metric_name == "http_req_duration"].metric_value
    failed = k[k.metric_name == "http_req_failed"].metric_value.sum()
    dropped = k[k.metric_name == "dropped_iterations"].metric_value.sum()
    total = len(dur) + dropped
    c = cap[(cap.t >= 0) & (cap.t <= 240)]
    dt = c.t.diff().fillna(0).clip(upper=10)
    vcpu_min = float((c.vcpu_allocated * dt).sum() / 60)
    used_min = float((c.cpu_cores_used * dt).sum() / 60)
    ok_bins = ((b.p95_ms < SLO_P95_MS) & (b.err_pct < SLO_ERR_PCT)).mean() * 100
    actions = [a for a in c.action.fillna("") if a]
    react = ""
    if p == "D" and s == "elastico":
        outs = c[c.action.fillna("").str.startswith("scale_out") & (c.t >= 60)]
        if len(outs):
            react = f"{outs.t.iloc[0] - 60:.0f}"
    summary.append(dict(
        patron=p, estrategia=s,
        demanda_media_rps=round(total / 240, 1),
        demanda_pico_rps=round(b.offered_rps.max(), 1),
        servidas_rps=round((len(dur) - failed) / 240, 1),
        p50_ms=round(dur.quantile(0.50)), p95_ms=round(dur.quantile(0.95)), p99_ms=round(dur.quantile(0.99)),
        errores_pct=round(100 * (failed + dropped) / total, 2) if total else 0,
        cpu_media_pct=round(100 * c.cpu_util.mean()), cpu_max_pct=round(100 * c.cpu_util.max()),
        replicas_min=int(c.replicas_total.min()), replicas_max=int(c.replicas_total.max()),
        replicas_media=round(c.replicas_total.mean(), 2),
        vcpu_min=round(vcpu_min, 1), vcpu_usado_min=round(used_min, 1),
        eficiencia_pct=round(100 * used_min / vcpu_min) if vcpu_min else 0,
        cumplimiento_slo_pct=round(ok_bins), acciones=len(actions), reaccion_s=react,
    ))
S = pd.DataFrame(summary)
S.to_csv(os.path.join(OUT, "resumen.csv"), index=False)


def fig_pattern(p):
    strats = [s for s in STRATS if (p, s) in runs]
    fig, ax = plt.subplots(4, 1, figsize=(10, 11), sharex=True)
    first = runs[(p, strats[0])][3]
    ax[0].fill_between(first.t, first.offered_rps, color="#e5e7eb", label="Demanda ofrecida", step="mid")
    for s in strats:
        b = runs[(p, s)][3]
        ax[0].plot(b.t, b.served_rps, color=COLOR[s], lw=1.6, label=LABEL[s])
        ax[1].plot(b.t, b.p95_ms, color=COLOR[s], lw=1.6)
        ax[2].step(b.t, b.vcpu, where="mid", color=COLOR[s], lw=1.8)
        ax[3].plot(b.t, b.cpu_util, color=COLOR[s], lw=1.4)
    ax[0].set_ylabel("Solicitudes/s")
    ax[0].set_title("Demanda ofrecida vs. solicitudes servidas con éxito", loc="left", fontsize=10)
    ax[0].legend(fontsize=8, ncol=2, loc="upper left")
    ax[1].set_yscale("log")
    ax[1].axhline(SLO_P95_MS, color="#dc2626", ls="--", lw=1)
    ax[1].text(2, SLO_P95_MS * 1.1, "SLO p95 = 500 ms", color="#dc2626", fontsize=8)
    ax[1].set_ylabel("Latencia p95 (ms, log)")
    ax[1].set_title("Latencia percentil 95 por ventana de 5 s", loc="left", fontsize=10)
    ax[2].set_ylabel("vCPU asignadas")
    ax[2].set_title("Capacidad asignada (réplicas × vCPU por réplica)", loc="left", fontsize=10)
    ax[3].axhline(70, color="#059669", ls=":", lw=1)
    ax[3].axhline(35, color="#059669", ls=":", lw=1)
    ax[3].text(2, 72, "umbral scale-out 70 %", fontsize=7, color="#059669")
    ax[3].text(2, 37, "umbral scale-in 35 %", fontsize=7, color="#059669")
    ax[3].set_ylabel("CPU media (% del límite)")
    ax[3].set_title("Utilización media de CPU de las réplicas listas", loc="left", fontsize=10)
    ax[3].set_xlabel("Tiempo de prueba (s) — 240 s representan un día de operación comprimido")
    for a in ax:
        a.grid(alpha=0.3)
    fig.suptitle(f"Patrón {p} · {PATTERNS[p]} — comparación de estrategias de capacidad", fontsize=13, x=0.01, ha="left")
    fig.text(0.01, 0.005, FOOT, fontsize=7, color="#555")
    fig.tight_layout(rect=(0, 0.015, 1, 0.98))
    fig.savefig(os.path.join(FIG, f"patron_{p}.png"), dpi=150)
    plt.close(fig)


for p in PATTERNS:
    if any(k[0] == p for k in runs):
        fig_pattern(p)

# Gráfico resumen: costo (vCPU·min) vs. latencia p95 por patrón
fig, axes = plt.subplots(1, 4, figsize=(14, 4.2), sharey=False)
for a, p in zip(axes, PATTERNS):
    sub = S[S.patron == p]
    for _, r in sub.iterrows():
        a.scatter(r.vcpu_min, r.p95_ms, s=90, color=COLOR[r.estrategia], edgecolor="k", zorder=3)
        a.annotate(r.estrategia, (r.vcpu_min, r.p95_ms), textcoords="offset points", xytext=(5, 4), fontsize=8)
    a.set_yscale("log")
    a.axhline(SLO_P95_MS, color="#dc2626", ls="--", lw=1)
    a.set_title(f"{p} · {PATTERNS[p]}", fontsize=10)
    a.set_xlabel("Costo: vCPU·min asignadas")
    a.grid(alpha=0.3)
axes[0].set_ylabel("Latencia p95 total (ms, log)")
fig.suptitle("Compromiso costo–rendimiento por patrón y estrategia (abajo-izquierda = mejor)", x=0.01, ha="left")
fig.text(0.01, 0.005, FOOT, fontsize=7, color="#555")
fig.tight_layout(rect=(0, 0.03, 1, 0.95))
fig.savefig(os.path.join(FIG, "costo_vs_latencia.png"), dpi=150)
plt.close(fig)

# Calibración
cal = os.path.join(RAW, "CALIB_fijo", "calibration.txt")
cal_txt = open(cal).read() if os.path.exists(cal) else ""

cols = ["patron", "estrategia", "demanda_media_rps", "demanda_pico_rps", "servidas_rps", "p95_ms",
        "errores_pct", "cpu_media_pct", "replicas_min", "replicas_max", "vcpu_min", "eficiencia_pct",
        "cumplimiento_slo_pct", "acciones"]
with open(os.path.join(OUT, "resumen.md"), "w") as fh:
    fh.write("# Resultados — Escalabilidad y elasticidad\n\n")
    fh.write(f"_{FOOT}_\n\n")
    if cal_txt:
        fh.write("## Calibración (1 réplica × 0,5 vCPU)\n\n" + cal_txt + "\n\n")
    fh.write(f"## Resumen por patrón y estrategia (ventana de 240 s, bins de {BIN_S} s)\n\n")
    fh.write("| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n")
    for _, r in S[cols].iterrows():
        fh.write("| " + " | ".join(str(v) for v in r.values) + " |\n")
    fh.write("\nSLO: p95 < 500 ms y errores < 1 % por ventana de 5 s. Costo = vCPU·min asignadas.\n")
print(open(os.path.join(OUT, "resumen.md")).read())
json.dump({"n_runs": len(runs)}, open(os.path.join(OUT, "meta.json"), "w"))
