from fastapi import FastAPI, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time


app = FastAPI(title="Data Platform API", version="0.1.0")

REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"]
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds", "HTTP request latency", ["endpoint"]
)


@app.get("/healthz")
def health() -> dict:
    return {"status": "ok"}


@app.get("/readyz")
def ready() -> dict:
    return {"status": "ready"}


@app.get("/metrics")
def metrics() -> Response:
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)


@app.get("/")
def root() -> dict:
    start = time.time()
    payload = {"service": "data-platform-api", "message": "hello"}
    duration = time.time() - start
    REQUEST_LATENCY.labels(endpoint="/").observe(duration)
    REQUEST_COUNT.labels(method="GET", endpoint="/", status="200").inc()
    return payload


