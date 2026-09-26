"""
Elation Health - OpenTelemetry Observability Setup
Traces, Logs, Metrics for production monitoring
"""

from opentelemetry import trace, metrics
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import Counter, Histogram, Gauge
from datetime import datetime
import time
import json
import logging

# Configure Prometheus metrics
TRACES_COUNTER = Counter(
    'elation_traces_total',
    'Total traces',
    ['service', 'endpoint', 'status']
)

LATENCY_HISTOGRAM = Histogram(
    'elation_latency_seconds',
    'Request latency in seconds',
    ['endpoint', 'method'],
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0)
)

TOOL_CALLS = Counter(
    'elation_tool_calls_total',
    'Total tool calls',
    ['tool_name', 'status']
)

RAG_QUERIES = Counter(
    'elation_rag_queries_total',
    'Total RAG queries',
    ['query_type', 'status']
)

ACTIVE_PATIENTS = Gauge(
    'elation_active_patients',
    'Number of patients currently being reviewed'
)

API_ERRORS = Counter(
    'elation_api_errors_total',
    'Total API errors',
    ['endpoint', 'error_type', 'status_code']
)

CLINICAL_ALERTS = Counter(
    'elation_clinical_alerts_total',
    'Total clinical alerts generated',
    ['alert_type', 'severity']
)


class ObservabilitySetup:
    """OpenTelemetry configuration for Elation Health"""

    def __init__(self, service_name="elation-health"):
        self.service_name = service_name
        self.setup_tracing()
        self.setup_metrics()

    def setup_tracing(self):
        """Configure OpenTelemetry tracing"""
        # Create resource
        resource = Resource.create({
            "service.name": self.service_name,
            "service.version": "0.2.0",
            "environment": "production"
        })

        # Set up tracer provider
        tracer_provider = TracerProvider(resource=resource)

        # Export to OTLP (SigNoz/Jaeger)
        otlp_exporter = OTLPSpanExporter(
            endpoint="localhost:4317",  # Default OTLP endpoint
            insecure=True
        )
        tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

        # Set as global
        trace.set_tracer_provider(tracer_provider)
        self.tracer = trace.get_tracer(__name__)

    def setup_metrics(self):
        """Configure OpenTelemetry metrics"""
        # Use Prometheus exporter
        prometheus_reader = PrometheusMetricReader()

        # Create meter provider
        meter_provider = MeterProvider(metric_readers=[prometheus_reader])
        metrics.set_meter_provider(meter_provider)

        self.meter = metrics.get_meter(__name__)

    @staticmethod
    def instrument_app(app):
        """Instrument FastAPI app with OpenTelemetry"""
        FastAPIInstrumentor.instrument_app(app)
        RequestsInstrumentor().instrument()


class PerformanceTracer:
    """Track performance metrics for tools and operations"""

    @staticmethod
    def trace_tool_call(tool_name, status, duration):
        """Record tool call metrics"""
        TOOL_CALLS.labels(tool_name=tool_name, status=status).inc()
        LATENCY_HISTOGRAM.labels(endpoint=f"tool_{tool_name}", method="POST").observe(duration)

    @staticmethod
    def trace_rag_query(query_type, status, duration):
        """Record RAG query metrics"""
        RAG_QUERIES.labels(query_type=query_type, status=status).inc()
        LATENCY_HISTOGRAM.labels(endpoint="rag_retrieve", method="GET").observe(duration)

    @staticmethod
    def trace_patient_review(patient_mrn):
        """Track patient review activity"""
        ACTIVE_PATIENTS.inc()
        LATENCY_HISTOGRAM.labels(endpoint="patient_view", method="GET").observe(0.1)

    @staticmethod
    def trace_api_error(endpoint, error_type, status_code):
        """Record API errors"""
        API_ERRORS.labels(endpoint=endpoint, error_type=error_type, status_code=status_code).inc()

    @staticmethod
    def trace_clinical_alert(alert_type, severity):
        """Record clinical alert generation"""
        CLINICAL_ALERTS.labels(alert_type=alert_type, severity=severity).inc()


# Configure logging
def setup_logging():
    """Setup structured logging for observability"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    logger = logging.getLogger("elation_health")

    # Structured logging
    class StructuredLogger:
        def __init__(self, base_logger):
            self.logger = base_logger

        def log_event(self, event_name, **kwargs):
            """Log structured event"""
            log_data = {
                "timestamp": datetime.now().isoformat(),
                "event": event_name,
                **kwargs
            }
            self.logger.info(json.dumps(log_data))

        def log_tool_call(self, tool_name, mrn, duration, status):
            self.log_event(
                "tool_call",
                tool_name=tool_name,
                mrn=mrn,
                duration_ms=round(duration * 1000, 2),
                status=status
            )

        def log_rag_retrieval(self, query, results_count, duration):
            self.log_event(
                "rag_retrieval",
                query=query,
                results_count=results_count,
                duration_ms=round(duration * 1000, 2)
            )

        def log_api_request(self, endpoint, method, status_code, duration):
            self.log_event(
                "api_request",
                endpoint=endpoint,
                method=method,
                status_code=status_code,
                duration_ms=round(duration * 1000, 2)
            )

        def log_error(self, error_type, endpoint, details):
            self.log_event(
                "error",
                error_type=error_type,
                endpoint=endpoint,
                details=details
            )

    return StructuredLogger(logger)


# Initialize
observability = None
structured_logger = None


def init_observability():
    """Initialize observability system"""
    global observability, structured_logger
    observability = ObservabilitySetup("elation-health")
    structured_logger = setup_logging()
    return observability, structured_logger
