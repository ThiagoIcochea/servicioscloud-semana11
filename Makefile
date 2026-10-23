# Atajos para ejecutar el laboratorio en Codespaces o en local (requiere Docker y k6)
PATRON ?= D
ESTRATEGIA ?= elastico
K ?= 30

.PHONY: calibrar experimento todo analizar limpiar

calibrar:
	bash scripts/run_experiment.sh CALIB fijo $(K) results/raw/CALIB_fijo
	python3 analysis/calibrate.py results/raw/CALIB_fijo | tee results/raw/CALIB_fijo/calibration.txt

experimento:
	bash scripts/run_experiment.sh $(PATRON) $(ESTRATEGIA) $(K)

todo:
	for p in A B C D; do for e in fijo vertical horizontal elastico; do \
	  bash scripts/run_experiment.sh $$p $$e $(K); done; done
	bash scripts/run_experiment.sh C programado $(K)

analizar:
	python3 analysis/analyze.py results/raw results

limpiar:
	COMPOSE_PROJECT_NAME=shoplab docker compose down -v --remove-orphans
	docker image rm shoplab-web:latest || true
