// Patrones de tráfico empresarial — Laboratorio Servicios Cloud (Semana 11)
// Autor: Thiago Paolo Icochea Rodriguez (U22330428)
//
// Uso:  k6 run -e PATTERN=D -e K=30 load/patterns.js
//   PATTERN: A (estable) | B (creciente) | C (pico previsible) | D (pico súbito) | CALIB
//   K: capacidad de referencia de UNA réplica de 0,5 vCPU en solicitudes/s (medida en la calibración)
//
// Un "día" de comercio electrónico se comprime en 240 s para que cada prueba
// sea corta y de bajo costo. El ejecutor ramping-arrival-rate fija la tasa de
// llegada (modelo abierto), así la demanda no baja cuando el sistema se satura.
import http from 'k6/http';
import { check } from 'k6';

const K = Number(__ENV.K || 30);
const BASE = __ENV.TARGET || 'http://localhost:8080';
const P = (__ENV.PATTERN || 'A').toUpperCase();
const r = (x) => Math.max(1, Math.round(x * K));

const PATTERNS = {
  // A) Carga estable: demanda constante cercana a la capacidad base
  A: { start: r(0.8), stages: [{ target: r(0.8), duration: '240s' }] },
  // B) Crecimiento gradual sostenido (p. ej., una campaña que gana tráfico)
  B: { start: r(0.4), stages: [{ target: r(3.0), duration: '240s' }] },
  // C) Pico previsible (campaña programada, p. ej. CyberWow a las 20:00)
  C: {
    start: r(0.6), stages: [
      { target: r(0.6), duration: '80s' },
      { target: r(3.5), duration: '30s' },
      { target: r(3.5), duration: '70s' },
      { target: r(0.6), duration: '30s' },
      { target: r(0.6), duration: '30s' },
    ],
  },
  // D) Pico súbito y descenso (contenido viral, mención de un influencer)
  D: {
    start: r(0.6), stages: [
      { target: r(0.6), duration: '60s' },
      { target: r(4.5), duration: '5s' },
      { target: r(4.5), duration: '60s' },
      { target: r(0.4), duration: '5s' },
      { target: r(0.4), duration: '110s' },
    ],
  },
  // Calibración: escalones de 10 en 10 sol/s para hallar la saturación de 1 réplica
  CALIB: {
    start: 10, stages: [10, 20, 30, 40, 50, 60, 70, 80].flatMap((x) => [
      { target: x, duration: '2s' }, { target: x, duration: '18s' }]),
  },
};

const cfg = PATTERNS[P];
export const options = {
  discardResponseBodies: true,
  scenarios: {
    trafico: {
      executor: 'ramping-arrival-rate',
      startRate: cfg.start,
      timeUnit: '1s',
      preAllocatedVUs: 150,
      maxVUs: 600,
      stages: cfg.stages,
    },
  },
  thresholds: { http_req_duration: ['p(95)>=0'] },
};

export default function () {
  const res = http.get(`${BASE}/api/checkout`, { timeout: '10s', tags: { name: 'checkout' } });
  check(res, { 'status 200': (x) => x.status === 200 });
}
