"""Lectura de datos crudos del laboratorio (k6 + monitor de capacidad).
Autor: Thiago Paolo Icochea Rodriguez (U22330428)"""
import gzip
import json
import os

import pandas as pd

BIN_S = 5  # resolución temporal de las métricas (s)


def load_run(d):
    meta = json.load(open(os.path.join(d, "meta.json")))
    k6_start = float(open(os.path.join(d, "k6_start_epoch.txt")).read().strip())
    with gzip.open(os.path.join(d, "k6.csv.gz"), "rt") as fh:
        k = pd.read_csv(fh, usecols=["metric_name", "timestamp", "metric_value"])
    k = k[k.metric_name.isin(["http_req_duration", "http_req_failed", "dropped_iterations"])]
    k["t"] = k.timestamp - k6_start
    cap = pd.read_csv(os.path.join(d, "capacity.csv"))
    cap["t"] = cap.epoch - k6_start
    return meta, k, cap


def bins(k, cap, end=None):
    """Agrega por ventanas de BIN_S segundos."""
    end = end or int(k.t.max()) + 1
    edges = list(range(0, end + BIN_S, BIN_S))
    rows = []
    dur = k[k.metric_name == "http_req_duration"]
    fail = k[k.metric_name == "http_req_failed"]
    drop = k[k.metric_name == "dropped_iterations"]
    for a, b in zip(edges[:-1], edges[1:]):
        d = dur[(dur.t >= a) & (dur.t < b)].metric_value
        f = fail[(fail.t >= a) & (fail.t < b)].metric_value
        dr = drop[(drop.t >= a) & (drop.t < b)].metric_value.sum()
        c = cap[(cap.t >= a - 2.5) & (cap.t < b + 2.5)]
        n = len(d)
        failed = float(f.sum())
        rows.append(dict(
            t=a + BIN_S / 2,
            offered_rps=(n + dr) / BIN_S,
            served_rps=(n - failed) / BIN_S,
            p50_ms=d.quantile(0.50) if n else float("nan"),
            p95_ms=d.quantile(0.95) if n else float("nan"),
            err_pct=100 * (failed + dr) / (n + dr) if (n + dr) else 0.0,
            replicas=c.replicas_total.mean() if len(c) else float("nan"),
            ready=c.replicas_ready.mean() if len(c) else float("nan"),
            cpu_util=100 * c.cpu_util.mean() if len(c) else float("nan"),
            vcpu=c.vcpu_allocated.mean() if len(c) else float("nan"),
            cores_used=c.cpu_cores_used.mean() if len(c) else float("nan"),
        ))
    return pd.DataFrame(rows)
