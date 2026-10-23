#!/usr/bin/env python3
"""
Monitor + autoescalador del laboratorio (equivalente didáctico a un
Managed Instance Group de GCP / Auto Scaling Group de AWS / VMSS de Azure /
Horizontal Pod Autoscaler de Kubernetes).

Autor: Thiago Paolo Icochea Rodriguez (U22330428) — Servicios Cloud, UTP

Modos (--mode):
  observe    Capacidad fija: solo mide (escenarios fijo, vertical, horizontal).
  elastic    Política reactiva por objetivo de CPU (target tracking).
  scheduled  Escalado planificado: cambia réplicas en instantes definidos.

Cada --interval segundos registra en CSV: réplicas totales y listas,
utilización media de CPU respecto al límite, núcleos usados, vCPU asignadas
(base del costo) y la acción tomada.
"""
import argparse
import csv
import glob
import math
import os
import subprocess
import sys
import time

PROJECT = os.getenv("COMPOSE_PROJECT_NAME", "shoplab")


def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()


def web_containers():
    out = sh(f"docker ps -q --filter label=lab.role=web --filter label=com.docker.compose.project={PROJECT} --no-trunc")
    return [c for c in out.splitlines() if c]


def health(cid):
    return sh(f"docker inspect -f '{{{{.State.Health.Status}}}}' {cid}")


def cgroup_usage_usec(cid):
    """Lee el contador acumulado de CPU del contenedor (cgroup v2)."""
    for pattern in (f"/sys/fs/cgroup/system.slice/docker-{cid}.scope/cpu.stat",
                    f"/sys/fs/cgroup/docker/{cid}/cpu.stat"):
        for path in glob.glob(pattern):
            with open(path) as fh:
                for line in fh:
                    if line.startswith("usage_usec"):
                        return int(line.split()[1])
    return None


def docker_stats_cores(cid):
    """Respaldo si no hay acceso al cgroup: docker stats (más lento)."""
    out = sh(f"docker stats --no-stream --format '{{{{.CPUPerc}}}}' {cid}").rstrip("%")
    try:
        return float(out) / 100.0
    except ValueError:
        return 0.0


def scale(n):
    subprocess.run(f"docker compose -p {PROJECT} up -d --no-recreate --no-build --scale web={n} web",
                   shell=True, capture_output=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["observe", "elastic", "scheduled"], default="observe")
    ap.add_argument("--out", required=True)
    ap.add_argument("--duration", type=int, default=300)
    ap.add_argument("--interval", type=float, default=5.0)
    ap.add_argument("--cpus", type=float, default=float(os.getenv("CPUS", "0.5")), help="límite de CPU por réplica")
    # Política elástica
    ap.add_argument("--min", type=int, default=1)
    ap.add_argument("--max", type=int, default=6)
    ap.add_argument("--target", type=float, default=0.60, help="utilización objetivo")
    ap.add_argument("--scale-out-at", type=float, default=0.70)
    ap.add_argument("--scale-in-at", type=float, default=0.35)
    ap.add_argument("--scale-out-cooldown", type=float, default=15)
    ap.add_argument("--scale-in-window", type=float, default=30, help="ventana de estabilización para reducir")
    # Política planificada: "80:4,190:1" => en t=80 s pasar a 4 réplicas, en t=190 s a 1
    ap.add_argument("--schedule", default="")
    a = ap.parse_args()

    schedule = []
    if a.schedule:
        for item in a.schedule.split(","):
            t, n = item.split(":")
            schedule.append((float(t), int(n)))
    schedule.sort()

    prev = {}
    t0 = time.time()
    last_out = -1e9
    low_since = None
    desired = len(web_containers())

    with open(a.out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["epoch", "t_s", "replicas_total", "replicas_ready", "cpu_util", "cpu_cores_used",
                    "vcpu_allocated", "desired", "action"])
        while True:
            now = time.time()
            t = now - t0
            if t > a.duration:
                break
            cids = web_containers()
            ready = [c for c in cids if health(c) == "healthy"]
            cores = {}
            for c in cids:
                u = cgroup_usage_usec(c)
                if u is None:
                    cores[c] = docker_stats_cores(c)
                else:
                    if c in prev:
                        pu, pt = prev[c]
                        cores[c] = max(0.0, (u - pu) / 1e6 / (now - pt))
                    prev[c] = (u, now)
            measured = [cores[c] for c in ready if c in cores]
            util = (sum(measured) / len(measured) / a.cpus) if measured else 0.0
            used = sum(cores.values())
            n = len(cids)
            action = ""

            if a.mode == "elastic":
                if util > a.scale_out_at and n < a.max and (now - last_out) >= a.scale_out_cooldown:
                    base = max(len(ready), 1)
                    want = min(a.max, max(n + 1, math.ceil(base * util / a.target)))
                    desired = want
                    scale(want)
                    last_out = now
                    low_since = None
                    action = f"scale_out {n}->{want}"
                elif util < a.scale_in_at and n > a.min and len(ready) == n:
                    low_since = low_since or now
                    if now - low_since >= a.scale_in_window:
                        want = max(a.min, min(n - 1, math.ceil(n * max(util, 0.01) / a.target)))
                        desired = want
                        scale(want)
                        low_since = None
                        action = f"scale_in {n}->{want}"
                else:
                    low_since = None
            elif a.mode == "scheduled":
                while schedule and t >= schedule[0][0]:
                    _, want = schedule.pop(0)
                    desired = want
                    scale(want)
                    action = f"scheduled {n}->{want}"

            w.writerow([f"{now:.3f}", f"{t:.1f}", n, len(ready), f"{util:.3f}", f"{used:.3f}",
                        f"{n * a.cpus:.2f}", desired, action])
            fh.flush()
            if action:
                print(f"t={t:6.1f}s util={util:5.2f} {action}", flush=True)
            time.sleep(max(0.0, a.interval - (time.time() - now)))


if __name__ == "__main__":
    sys.exit(main())
