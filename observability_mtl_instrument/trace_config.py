from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

class ConfigTrace:
    def __init__(self, service_name: str, tempo_url: str) -> None:
        self.config_data_trace(service_name, tempo_url)
        self.trace = trace
        self.tracer = trace.get_tracer(__name__)

    def get_tracer(self):
        return self.tracer

    def get_trace(self):
        return self.trace
    
    def config_data_trace(self, service_name: str, tempo_url: str) -> None:
        resource = Resource.create({SERVICE_NAME: service_name})
        trace.set_tracer_provider(TracerProvider(resource=resource))
        trace.get_tracer_provider().add_span_processor(
            BatchSpanProcessor(OTLPSpanExporter(endpoint=tempo_url))
        )