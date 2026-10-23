"""
Tienda de prueba "ShopLab" — Laboratorio Servicios Cloud (Semana 11)
Autor: Thiago Paolo Icochea Rodriguez (U22330428)

Aplicación web mínima que simula el endpoint de checkout de un comercio
electrónico. Cada solicitud consume CPU de forma determinista (derivación
PBKDF2), de modo que la utilización de CPU crece con la demanda y el efecto
de escalar (vertical / horizontal / elástico) es medible.
"""
import hashlib
import os
import socket
import time

from flask import Flask, jsonify

WORK_ITERATIONS = int(os.getenv("WORK_ITERATIONS", "100000"))
INSTANCE = socket.gethostname()
STARTED = time.time()

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify(status="ok", instance=INSTANCE, uptime_s=round(time.time() - STARTED, 1))


@app.get("/api/checkout")
def checkout():
    t0 = time.perf_counter()
    # Trabajo de CPU equivalente a validar y firmar una orden de compra
    digest = hashlib.pbkdf2_hmac("sha256", b"orden-ecommerce", INSTANCE.encode(), WORK_ITERATIONS)
    cpu_ms = (time.perf_counter() - t0) * 1000
    return jsonify(order=digest.hex()[:16], instance=INSTANCE, cpu_ms=round(cpu_ms, 2))


@app.get("/")
def index():
    return jsonify(app="ShopLab", lab="Escalabilidad y elasticidad",
                   autor="Thiago Paolo Icochea Rodriguez", codigo="U22330428")
