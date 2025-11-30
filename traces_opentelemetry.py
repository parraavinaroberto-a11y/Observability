import time
import random

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter


def setup_tracer(service_name: str = "demo-python-service"):
    resource = Resource.create({"service.name": service_name})

    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    # Exportador OTLP (cámbialo a tu collector)
    otlp_exporter = OTLPSpanExporter(
        endpoint="http://localhost:4318/v1/traces",
        insecure=True,
    )
    provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

    # Exportar también a consola para debug
    console_exporter = ConsoleSpanExporter()
    provider.add_span_processor(BatchSpanProcessor(console_exporter))

    return trace.get_tracer(__name__)


tracer = setup_tracer()


def do_work(x: int) -> int:
    with tracer.start_as_current_span("do_work") as span:
        span.set_attribute("work.input", x)
        time.sleep(random.uniform(0.1, 0.3))
        result = x * 2
        span.set_attribute("work.output", result)
        return result


if __name__ == "__main__":
    for i in range(5):
        with tracer.start_as_current_span("request") as span:
            span.set_attribute("request.id", i)
            res = do_work(i)
            print(f"Resultado = {res}")
        time.sleep(1)
