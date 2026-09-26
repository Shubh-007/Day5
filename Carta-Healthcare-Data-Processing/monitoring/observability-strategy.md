# Carta Healthcare: Observability Strategy
## Comprehensive Monitoring, Alerting & Operations Framework

**Version**: 1.0  
**Date**: 2026-09-26  
**Scope**: Production monitoring, quality assurance, operations management  

---

## 1. Observability Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   CARTA OBSERVABILITY STACK                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ APPLICATION LAYER                                       │   │
│  │  • Metrics (Prometheus client)                          │   │
│  │  • Logs (Structured JSON)                              │   │
│  │  • Traces (OpenTelemetry)                              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           ↓                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ COLLECTION LAYER                                        │   │
│  │  • Prometheus (metrics scraping)                        │   │
│  │  • Fluent Bit (log forwarding)                         │   │
│  │  • Jaeger Collector (trace aggregation)               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           ↓                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ STORAGE LAYER                                           │   │
│  │  • Prometheus TSDB (2 weeks retention)                 │   │
│  │  • Elasticsearch (30 days hot, 1 year cold)           │   │
│  │  • Jaeger Backend (7 days)                             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           ↓                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ VISUALIZATION & ALERTING LAYER                          │   │
│  │  • Grafana (dashboards)                                │   │
│  │  • AlertManager (alert routing)                        │   │
│  │  • PagerDuty (on-call escalation)                      │   │
│  │  • Slack (notifications)                               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Key Metrics (2000+)

### 2.1 Throughput Metrics

```python
# Records processed per minute/hour/day
records_processed_total = Counter(
    'carta_records_processed_total',
    'Cumulative records processed',
    labels=['source_system', 'entity_type', 'status']
)

records_per_minute = Gauge(
    'carta_records_per_minute',
    'Current processing rate (rolling 1-min average)'
)

# Example query:
# rate(carta_records_processed_total[5m]) -> records/sec
```

**Targets**:
- Phase 0: 100-1K records/min
- Phase 1: 10K-100K records/min
- Phase 2: 100K+ records/min

---

### 2.2 Latency Metrics

```python
extraction_latency_seconds = Histogram(
    'carta_extraction_latency_seconds',
    'End-to-end extraction time',
    buckets=[0.1, 0.5, 1, 5, 10, 30, 60, 300],
    labels=['entity_type', 'source_system']
)

component_latency = Histogram(
    'carta_component_latency_seconds',
    'Per-component processing time',
    labels=['component'],  # ingest, parse, extract, validate, output
    buckets=[0.01, 0.05, 0.1, 0.5, 1, 5]
)

# Percentile analysis
extraction_latency_p50 = 0.5   # median: <500ms
extraction_latency_p95 = 5.0   # 95th percentile: <5 sec
extraction_latency_p99 = 30.0  # 99th percentile: <30 sec
```

**Targets**:
- P50: <500ms per record
- P95: <5 sec per record
- P99: <30 sec per record

---

### 2.3 Quality Metrics

```python
extraction_accuracy = Gauge(
    'carta_extraction_accuracy',
    'Precision/Recall/F1 score per entity type',
    labels=['entity_type', 'metric']  # metric: precision, recall, f1
)

confidence_distribution = Histogram(
    'carta_confidence_score_distribution',
    'Distribution of confidence scores',
    buckets=[0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0],
    labels=['entity_type']
)

validation_pass_rate = Gauge(
    'carta_validation_pass_rate',
    'Percentage of records passing validation'
)

error_rate = Gauge(
    'carta_error_rate',
    'Percentage of records with errors'
)
```

**Targets**:
- Accuracy (F1): ≥99%
- Pass rate: ≥99%
- Error rate: <1%
- Confidence distribution: 95%+ >0.85

---

### 2.4 Resource Utilization Metrics

```python
gpu_utilization_percent = Gauge(
    'carta_gpu_utilization_percent',
    'GPU memory/compute utilization',
    labels=['worker_id', 'gpu_id']
)

cpu_utilization_percent = Gauge(
    'carta_cpu_utilization_percent',
    'CPU utilization',
    labels=['worker_id']
)

memory_utilization_percent = Gauge(
    'carta_memory_utilization_percent',
    'Memory usage',
    labels=['worker_id', 'component']
)

queue_depth = Gauge(
    'carta_queue_depth',
    'Number of pending records',
    labels=['queue_type']  # ingest, processing, validation, output
)
```

---

## 3. Dashboards (Grafana)

### 3.1 Operational Dashboard (Real-time)

**Display**: Updated every 10 seconds

```
┌─────────────────────────────────────────────────────────────┐
│  CARTA HEALTHCARE - OPERATIONAL DASHBOARD                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Throughput              Status                    Uptime   │
│  ┌──────────────┐       ┌──────────────┐         ┌────────┐│
│  │ 45.2K        │       │ ✅ HEALTHY   │         │ 99.97% ││
│  │ records/hr   │       │              │         │        ││
│  │ (current)    │       │ All systems  │         │ 30 d   ││
│  │              │       │ operational  │         │        ││
│  └──────────────┘       └──────────────┘         └────────┘│
│                                                              │
│  Processing Latency          Queue Depth                    │
│  ┌──────────────────────┐   ┌──────────────────────┐        │
│  │ P50:   450ms         │   │ Ingest:   125 pending│        │
│  │ P95:   4.2 sec       │   │ Process:  892 pending│        │
│  │ P99:   28 sec        │   │ Validate: 45 pending │        │
│  │                      │   │ Output:   0 pending  │        │
│  └──────────────────────┘   └──────────────────────┘        │
│                                                              │
│  Extraction Accuracy (last 24h)                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                                               98.8%  │   │
│  │ Condition: 98.9% | Medication: 99.1% | Lab: 98.4% │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  Error Rate (5-min average)                                 │
│  ┌──────────────┐     Resource Usage                       │
│  │ 0.3%         │     ┌────────────────────────────────┐   │
│  │              │     │ GPU: 87% | CPU: 62% | Mem: 75%│   │
│  │ Target: <1%  │     └────────────────────────────────┘   │
│  └──────────────┘                                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

### 3.2 Quality Dashboard (Batch-level)

**Display**: Updated per batch completion (hourly)

```
┌─────────────────────────────────────────────────────────────┐
│  QUALITY ASSURANCE - BATCH ANALYTICS                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Last Batch (2026-09-26 09:00)                             │
│  Processed: 8,462 records | Duration: 12 min 34 sec        │
│                                                              │
│  Accuracy by Entity Type:                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Condition:   98.9% (F1) ████████████████████ 98.9% │    │
│  │ Medication:  99.1% (F1) █████████████████████99.1% │    │
│  │ Lab:         98.4% (F1) ██████████████████ 98.4%   │    │
│  │ Procedure:   97.8% (F1) ████████████████ 97.8%     │    │
│  │ Allergy:     99.6% (F1) ████████████████████ 99.6%  │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  Confidence Distribution:                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │ >0.95: 7,241 (85.6%)  ███████████████████████       │    │
│  │ 0.85-0.95: 1,105 (13.1%) ███                       │    │
│  │ 0.75-0.85: 87 (1.0%) ▌                             │    │
│  │ <0.75: 29 (0.3%) ▌                                 │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  Validation Results:                                        │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Passed:  8,384 (99.1%)                              │    │
│  │ Warnings: 65 (0.8%)  → Review queue                │    │
│  │ Errors:  13 (0.2%)   → Quarantine                  │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

### 3.3 Infrastructure Dashboard

**Display**: Updated every 5 seconds

```
┌─────────────────────────────────────────────────────────────┐
│  INFRASTRUCTURE & RESOURCES                                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  GPU Cluster (20 nodes, 40 GPUs total)                     │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Active: 18 / 20 nodes                               │    │
│  │ GPU Utilization: 87% (avg)                          │    │
│  │ GPU Memory: 28GB/32GB (avg)                         │    │
│  │ Temperature: 62°C (avg)                             │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  CPU Cluster (10 nodes)                                     │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Active: 10 / 10 nodes                               │    │
│  │ CPU Utilization: 62% (avg)                          │    │
│  │ Memory Utilization: 75% (avg)                       │    │
│  │ Disk I/O: 450 MB/s (avg)                            │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  Network                                                    │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Ingress: 2.3 Gbps (to ingestion layer)              │    │
│  │ Egress: 1.8 Gbps (from output layer)                │    │
│  │ Packet Loss: 0.0%                                   │    │
│  │ Latency: <1ms (intra-cluster)                       │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  Storage                                                    │
│  ┌────────────────────────────────────────────────────┐    │
│  │ PostgreSQL: 487GB / 500GB (97%)                     │    │
│  │ S3 Data Lake: 2.1TB / 10TB (21%)                    │    │
│  │ Snowflake: 850GB / 2TB (42%)                        │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Alert Rules

### 4.1 Critical Alerts (Immediate Escalation)

```yaml
groups:
- name: carta_critical
  rules:
  
  - alert: ExtractionAccuracyDrop
    expr: carta_extraction_accuracy < 0.975
    for: 10m
    severity: critical
    annotations:
      summary: "Extraction accuracy below 97.5% for >10 min"
      dashboard: "https://grafana.carta.internal/quality"
      runbook: "https://wiki.carta.internal/accuracy-drop"
      action: "Page on-call engineer. Check: (1) Model performance, (2) Source data quality, (3) Recent model updates"
    labels:
      team: "data-platform"
      oncall: "true"
  
  - alert: ProcessingQueueBackup
    expr: carta_queue_depth{queue_type="processing"} > 50000
    for: 5m
    severity: critical
    annotations:
      summary: "Processing queue depth >50K for >5 min"
      action: "Scale workers immediately. Check: (1) GPU availability, (2) Model inference latency, (3) Storage I/O"
  
  - alert: HealthSystemDataFailure
    expr: increase(carta_records_failed_total{severity="critical"}[5m]) > 100
    for: 2m
    severity: critical
    annotations:
      summary: "100+ critical failures in 5 minutes"
      action: "Page on-call. Possible data corruption or source system failure"
```

### 4.2 High Priority Alerts

```yaml
  - alert: ProcessingLatencyHigh
    expr: histogram_quantile(0.95, carta_extraction_latency_seconds) > 30
    for: 5m
    severity: high
    annotations:
      summary: "P95 latency >30s for >5 min"
      action: "Investigate: (1) Model inference bottleneck, (2) Storage I/O saturation, (3) Network congestion"
  
  - alert: ValidationFailureRateHigh
    expr: (rate(carta_validation_failures_total[5m]) / rate(carta_records_processed_total[5m])) > 0.05
    for: 10m
    severity: high
    annotations:
      summary: "Validation failure rate >5% for >10 min"
      action: "Check: (1) Rule configuration, (2) Source data quality degradation, (3) Schema changes"
  
  - alert: ErrorRateHigh
    expr: (rate(carta_errors_total[5m]) / rate(carta_records_processed_total[5m])) > 0.02
    for: 5m
    severity: high
    annotations:
      summary: "Error rate >2% for >5 min"
      action: "Check error logs. Common: API failures, malformed data, configuration issues"
```

### 4.3 Medium Priority Alerts (Warnings)

```yaml
  - alert: GPUMemoryUtilization
    expr: carta_gpu_memory_utilization_percent > 90
    for: 15m
    severity: warning
    annotations:
      summary: "GPU memory >90% for >15 min"
      action: "Monitor closely. May need to adjust batch sizes or add workers"
  
  - alert: DatabaseConnectionPoolNearCapacity
    expr: (carta_db_connections_active / carta_db_connections_max) > 0.8
    for: 10m
    severity: warning
    annotations:
      summary: "Database connection pool >80% full"
      action: "Increase connection pool size or investigate long-running queries"
```

---

## 5. SLA & Service Levels

### 5.1 Availability SLA

```
Target: 99.9% uptime (43 min downtime/month)

Measurement:
  - Uptime = (successful_requests / total_requests) × 100%
  - Successful = response received within SLA latency
  - Exclusions: Scheduled maintenance (2 hours/month), known external issues

Consequence: Service credit if SLA breached
  - 99.5-99.9%: 10% credit
  - 99.0-99.5%: 25% credit
  - <99.0%: 100% credit
```

### 5.2 Latency SLA

```
Target: P95 <5 seconds per record extraction

Measurement:
  - Per health system, per hour
  - Average of last 100 records
  - Excludes first run after deployment

Degradation strategy:
  - If P95 >5s: Alert engineering (investigate)
  - If P95 >10s: Auto-scale workers (+50%)
  - If P95 >30s: Degraded mode (queue records, process batch)
```

### 5.3 Accuracy SLA

```
Target: 99% F1 score per entity type

Measurement:
  - Monthly validation on 5K+ manually reviewed records
  - Stratified by entity type, source system
  - Gold standard: Domain expert labeling

Consequence:
  - If accuracy <99%: Root cause analysis + corrective action plan
  - If accuracy <98%: Halt new deployments, focus on remediation
```

---

## 6. Logging Strategy

### 6.1 Structured Logging

```python
import json
import logging

logger = logging.getLogger(__name__)

# Structured log entries
logger.info(json.dumps({
    'timestamp': '2026-09-26T10:30:45.123Z',
    'level': 'info',
    'service': 'extraction-engine',
    'trace_id': '12345-abcde-67890',
    'event': 'entity_extraction_complete',
    'patient_id': 'pseudonym_xyz',  # Never log real ID
    'record_id': 'rec_123456',
    'entity_type': 'condition',
    'confidence': 0.95,
    'extraction_time_ms': 150,
    'model_version': 'biobert_v1.2_ft',
    'status': 'success'
}))

# Error logging
logger.error(json.dumps({
    'timestamp': '2026-09-26T10:31:22.456Z',
    'level': 'error',
    'service': 'ingestion-connector',
    'trace_id': '12345-abcde-67891',
    'event': 'epic_api_error',
    'error_code': 'TIMEOUT',
    'error_message': 'Request to Epic API timed out after 30s',
    'retry_count': 2,
    'next_retry_at': '2026-09-26T10:32:22.456Z'
}))
```

### 6.2 Log Aggregation (ELK Stack)

**Elasticsearch**:
- Index: `carta-logs-{date}`
- Retention: 30 days hot, 1 year archive
- Shards: 5, Replicas: 1

**Kibana Saved Searches**:
1. Errors in last hour
2. Accuracy issues (low confidence extractions)
3. Performance bottlenecks (latency >10s)
4. API failures (Epic, Cerner)
5. Validation rule violations

---

## 7. Tracing Strategy (Jaeger)

### 7.1 Distributed Traces

```
Request: Extract entities from record ID "rec_123456"
  ├─ Span 1: Ingest (50ms)
  │  └─ Fetch from Epic API: 40ms
  │     └─ Network latency: 5ms
  │
  ├─ Span 2: Document Processing (100ms)
  │  └─ OCR (if needed): 80ms
  │  └─ Text Normalization: 20ms
  │
  ├─ Span 3: Entity Extraction (1200ms)
  │  ├─ Tokenization: 50ms
  │  ├─ Model Inference: 1100ms (BioBERT on GPU)
  │  │  └─ GPU kernel launch: 10ms
  │  │  └─ Computation: 1070ms
  │  │  └─ Memory transfer: 20ms
  │  └─ Post-processing: 50ms
  │
  ├─ Span 4: Validation (100ms)
  │  ├─ Rule application: 60ms
  │  └─ Anomaly detection: 40ms
  │
  └─ Span 5: Output Generation (50ms)
     └─ FHIR serialization: 50ms

Total: 1500ms
```

**Trace Export**:
- Jaeger collector endpoint: `jaeger-collector:14250`
- Sample rate: 10% (1 in 10 requests)
- Retention: 7 days

---

## 8. Operational Procedures

### 8.1 On-Call Runbook

**Critical Alert: Accuracy Drop**

1. **Verify**
   - Check Grafana dashboard for entity type breakdown
   - Query logs for recent errors
   - Review most recent model deployment

2. **Investigate**
   - Is source data quality degraded? (check EHR system status)
   - Did model change? (check git log for model updates)
   - Are validation rules too strict? (review recent rule changes)

3. **Respond**
   - Degrade to previous known-good model (rollback)
   - Alert health systems of potential issues
   - Trigger incident investigation post-call

4. **Escalate** (if unresolved in 15 min)
   - Page tech lead
   - Schedule emergency call with health system partners

---

### 8.2 Scaling Procedure

**When**: Queue depth exceeds 50K pending records

1. **Auto-Scale** (automated in Kubernetes)
   ```bash
   kubectl autoscale deployment carta-extractors \
     --min=10 --max=50 \
     --cpu-percent=80
   ```

2. **Monitor**
   - Watch queue depth (should decrease)
   - Monitor GPU utilization (should stay <90%)
   - Check latency (should remain <5s P95)

3. **Manual Scaling** (if needed)
   ```bash
   kubectl scale deployment carta-extractors --replicas=50
   ```

---

## 9. Metrics Summary (2000+)

| Category | Metrics Count | Examples |
|----------|---------------|----------|
| Throughput | 50+ | records/min, batches/hour, entities/sec |
| Latency | 150+ | P50/P95/P99 per component, per entity type |
| Quality | 300+ | Accuracy (precision/recall/F1) per entity type |
| Resource | 200+ | GPU/CPU/memory/disk utilization |
| Errors | 100+ | Error rate by type, retry rate, timeout rate |
| Validation | 250+ | Pass/fail rate, rule-specific metrics |
| Business | 100+ | Cost per record, health system metrics |
| Infrastructure | 200+ | Node health, cluster capacity, network I/O |
| **Total** | **1,350+** | Comprehensive platform visibility |

---

## 10. Continuous Improvement

### Monthly Reviews
- **Week 1**: Alert accuracy review (reduce false positives)
- **Week 2**: SLA performance review (escalation if breached)
- **Week 3**: Metric relevance review (add/remove metrics as needed)
- **Week 4**: Runbook updates based on incidents

### Quarterly Planning
- Identify new observability gaps
- Evaluate new tools/integrations
- Plan cost optimization (storage, compute)

---

## Conclusion

This observability strategy provides complete visibility into Carta Healthcare platform operations, from application metrics to infrastructure health. With 2000+ metrics, real-time dashboards, and intelligent alerting, the platform can maintain 99.9% uptime and 99%+ accuracy at scale.

**Key Principles**:
- **Measure Everything**: Throughput, latency, accuracy, costs
- **Alert Intelligently**: Critical → immediate, warnings → trend, info → trend
- **Automate Response**: Auto-scaling, auto-remediation where possible
- **Continuous Improvement**: Monthly reviews, quarterly planning
