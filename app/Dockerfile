FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir flask==3.0.3 gunicorn==22.0.0
COPY app.py entrypoint.sh ./
RUN chmod +x entrypoint.sh
# WARMUP_SECONDS simula el tiempo de aprovisionamiento/arranque de una instancia nueva
ENV WARMUP_SECONDS=10 WORKERS=2 WORK_ITERATIONS=12000
EXPOSE 8000
HEALTHCHECK --interval=3s --timeout=2s CMD python -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:8000/health')"
ENTRYPOINT ["./entrypoint.sh"]
