import random
import time
from prometheus_client import start_http_server, Counter, Histogram

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total de peticiones procesadas",
    ["endpoint", "method", "status"]
)

REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "Latencia de peticiones",
    ["endpoint"]
)

def process_request(endpoint="/api/demo"):
    with REQUEST_LATENCY.labels(endpoint=endpoint).time():
        # Simular trabajo
        time.sleep(random.uniform(0.1, 0.8))

    status = random.choice(["200", "200", "200", "500"])
    REQUEST_COUNT.labels(
        endpoint=endpoint,
        method="GET",
        status=status
    ).inc()

    return status

if __name__ == "__main__":
    # Exponer métricas en http://0.0.0.0:8000/metrics
    start_http_server(8000)
    print("Servidor de métricas Prometheus escuchando en 0.0.0.0:8000/metrics")

    while True:
        status = process_request("/api/demo")
        print(f"Request procesada con status={status}")
        time.sleep(1)
