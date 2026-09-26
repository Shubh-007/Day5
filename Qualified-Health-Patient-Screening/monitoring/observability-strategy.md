# Qualified Health - Observability & Monitoring Strategy

## Logging Strategy

**ELK Stack** (Elasticsearch, Logstash, Kibana)

### Retention Policies
- **Hot Storage**: 30 days (real-time search)
- **Warm Storage**: 30 days (slower, cost-optimized)
- **Cold Storage**: 7 years (compliance archive)

### Structured Logging
All logs emit JSON with required fields:
```json
{
  "timestamp": "2026-09-26T14:30:45.123Z",
  "level": "INFO",
  "service": "screening-engine",
  "trace_id": "trace-xyz",
  "correlation_id": "request-123",
  "message": "Patient screening completed",
  "context": {
    "patient_id": "pat-456",
    "intervention_id": "int-789",
    "confidence_score": 0.92
  },
  "metrics": {
    "latency_ms": 234,
    "rule_count": 15,
    "rules_passed": 12
  }
}
```

### Log Retention by Type
| Type | Hot | Cold |
|------|-----|------|
| Application | 30d | 1y |
| Audit | 30d | 7y |
| Ingestion | 30d | 90d |
| Error | 30d | 1y |

---

## Metrics & Monitoring

**Prometheus** metrics collection at 15-second intervals

### Key Metrics by Service

**Data Ingestion Layer**:
- `ingestion_events_total{source_system, status}` - Event count
- `ingestion_latency_seconds{source_system}` - P50, P95, P99
- `parsing_errors_total{error_type}` - Parse failures
- `dead_letter_events_total` - DLQ entries

**Normalization Engine**:
- `normalization_rate` - % of events normalized
- `deduplication_ratio` - % duplicates found
- `quality_score{metric}` - Null rate, anomalies detected
- `concept_mapping_success_rate` - SNOMED/LOINC mapping rate

**Patient Record Unification**:
- `patient_matching_confidence{quantile}` - Confidence score distribution
- `pmI_records_total` - Patient count in master index
- `merge_conflicts_total` - Manual review queue depth
- `patient_graph_edges_total` - Relationship count

**Clinical Rules Engine**:
- `rule_evaluation_total{rule_id, status}` - Evaluations
- `rule_latency_seconds{rule_id}` - P50, P95, P99
- `rule_timeout_errors_total` - 5s timeout breaches
- `rules_passed_rate` - % of patients passing rules

**Screening Engine**:
- `screening_candidates_total{intervention_id}` - Candidate count
- `screening_confidence_score{quantile}` - Score distribution
- `screening_latency_seconds{quantile}` - P95, P99 latency
- `batch_screening_duration_seconds` - Time for 500K patients

**Data Lake & Warehouse**:
- `warehouse_query_latency_seconds{query_type}` - Analytics queries
- `cache_hit_ratio` - Redis hit rate (target: >80%)
- `data_partition_size_bytes` - Partition growth
- `backup_duration_seconds` - Backup timing

---

## Distributed Tracing

**OpenTelemetry/Jaeger** instrumentation

### Trace Sampling
- **Development**: 100% sampling
- **Staging**: 50% sampling
- **Production**: 10% base + 100% for errors

### Trace Retention
- Full fidelity: 30 days
- Summary metrics: 1 year

### Example Trace
```
Request: Screen patient against intervention
├── span: api_gateway_auth (45ms)
├── span: retrieve_patient_record (120ms)
│   ├── span: database_query (100ms)
│   └── span: cache_lookup (20ms)
├── span: evaluate_rules (180ms)
│   ├── span: rule_1 (50ms)
│   ├── span: rule_2 (60ms)
│   └── span: rule_3 (70ms)
├── span: ml_prediction (95ms)
│   └── span: feature_extraction (45ms)
├── span: build_evidence (40ms)
└── span: format_response (20ms)
Total: 500ms
```

---

## Alerting Strategy

### Critical Alerts (Page On-Call)

| Alert | Threshold | Duration | Severity |
|-------|-----------|----------|----------|
| API Error Rate High | >5% of requests | 5 min | P1 |
| Latency High (P95) | >500ms | 10 min | P1 |
| Database Down | 0 connections | 1 min | P1 |
| Data Quality Low | <90% validation | 5 min | P1 |
| Audit Trail Down | Cannot write events | 1 min | P1 |
| Cache Hit Rate Low | <60% | 15 min | P2 |
| Queue Depth High | >10K pending | 10 min | P2 |
| Rule Evaluation Timeout | >5s | 10 min | P2 |

### Alert Routing
- **P1**: PagerDuty → On-call + Slack #incidents
- **P2**: Slack #alerts → Engineering team
- **Deduplication**: 5-minute window, repeat counter escalation

---

## Dashboarding

**Real-time Dashboards** (Grafana)

### System Health Dashboard
- Uptime percentage (target: 99.5%)
- Service status (green/red for all 10 services)
- Error rate (last 1 hour, line graph)
- P95 latency (last 1 hour, area chart)
- Active health systems count
- Total patients screened (rolling counter)

### Data Quality Dashboard
- Validation rate (target: >95%)
- Parse failure rate (target: <1%)
- Duplicate detection rate
- Temporal anomalies detected
- Concept mapping success rate
- Null field percentage by table

### Screening Performance Dashboard
- Candidates identified (daily count)
- Average screening latency (p50, p95, p99)
- Batch processing throughput (patients/hour)
- Rule evaluation success rate
- ML prediction accuracy (on validation set)
- Evidence snapshot quality score

### Clinician Adoption Dashboard
- Active clinicians (by health system)
- Total candidates reviewed
- Candidate approval rate
- Average review time
- Outcome tracking rate
- Feature adoption metrics

### Infrastructure Dashboard
- Database query latency distribution
- Cache hit ratio (target: >80%)
- Connection pool utilization
- Disk usage by table (partition growth)
- Backup status (last successful, next scheduled)
- Multi-region replication lag

### Compliance Dashboard
- Audit trail completion rate (100%)
- Access controls enforced
- Encryption verification status
- Key rotation schedule (90-day cycle)
- Data retention compliance
- HIPAA audit readiness

---

## Synthetic Monitoring

**Daily Health Checks**

1. Inject realistic test patient records (every 24h)
2. Run through full pipeline:
   - Ingestion → Normalization → Patient matching
   - Rule evaluation → Screening → Evidence building
   - Dashboard display → Report generation
3. Verify expected outcomes
4. Alert if synthetic patients not properly processed

**Expected Results**:
- Test patients screened within 5 minutes
- Evidence snapshots complete and accurate
- Dashboard shows test candidates
- Outcome tracking working

---

## Performance Baselines

### Target SLAs
- **Single Patient Lookup**: <500ms p95
- **API Response**: <200ms p95
- **Batch Screening**: 500K patients in <4 hours
- **Report Generation**: <5 minutes for 10K-patient cohort
- **System Uptime**: 99.5% availability
- **Data Quality**: >95% validation rate

### Capacity Planning
- Database: 10-100GB per health system + 50-200% annual growth
- Message Queue: Burst capacity for 100K events/sec
- Cache: 1-2GB for frequently accessed data
- Storage: 1-2PB for 7-year cold archive

---

## Observability Best Practices

### Instrumentation Standards
1. Every service emits: request count, duration histogram, error count
2. Every database operation: query duration, result size, cache hit/miss
3. Every external call: size, status, latency, retry count

### Alerting Best Practices
- Alert on **symptoms** (high latency), not **causes** (CPU >80%)
- Alerts must be **actionable** (clear remediation steps)
- Review weekly for false positives (disable >50% false positive rate)
- Adjust thresholds based on SLA targets

### Troubleshooting Workflows

**High Error Rate**:
1. Check service logs (grep by correlation_id)
2. Check distributed traces (full request path)
3. Check database query performance
4. Check external service availability
5. Check resource utilization

**High Latency**:
1. Check P95/P99 latency by service
2. Check database query latency
3. Check cache hit rate
4. Check network latency (inter-region)
5. Check queue depth

**Data Quality Issues**:
1. Check validation rate by source system
2. Check parse error distribution
3. Check temporal anomalies
4. Check reconciliation between ingestion and storage
5. Check deduplication effectiveness

---

## Cost Optimization Through Observability

### LLM/AI Cost Management
- Track screening volume and cost trends
- Identify expensive intervention types
- Optimize batch sizes vs latency tradeoffs
- Monitor model inference costs

### Infrastructure Cost Optimization
- Right-size instances based on actual usage
- Use reserved instances for baseline capacity
- Schedule scale-down during off-peak hours
- Archive old data to cold storage (S3 Glacier)

### Query Optimization
- Track slow query patterns
- Identify missing indexes
- Optimize partition pruning
- Use materialized views for complex queries

---

## Compliance Monitoring

### HIPAA Compliance Verification
- Audit trail immutability (daily checksums)
- Encryption verification (key rotation schedule)
- Access control enforcement (quarterly reviews)
- Data retention policies (automated archival)

### Clinical Quality Compliance
- Accuracy metrics against gold-standard references
- Compliance with clinical guidelines
- Risk flag appropriateness scoring
- Physician validation rate tracking

### Monthly Compliance Report
- Audit events generated (count, breakdown by action)
- Access patterns (privileged users review)
- Encryption status (key IDs in rotation)
- Backup and recovery test results
- Data retention compliance audit

---

## Observability Roadmap

**v0 (MVP)**:
- Basic application logging (ELK)
- Prometheus metrics (core services)
- Basic Grafana dashboards
- Manual alerting

**v1 (Enhanced)**:
- Distributed tracing (Jaeger)
- Advanced alerting (PagerDuty)
- Synthetic monitoring
- Comprehensive dashboards

**v2 (Predictive)**:
- Anomaly detection (ML-based)
- Predictive scaling
- Capacity forecasting
- Cost prediction

---

## Incident Response

### Runbook: High Error Rate
1. **Detection**: Error rate >5% for 5 minutes
2. **Alert**: Page on-call via PagerDuty
3. **Investigation**:
   - Check logs for error patterns
   - Check traces for failing service
   - Check recent deployments
4. **Resolution**:
   - Rollback if recent deployment
   - Scale service if capacity issue
   - Failover if service down
5. **Follow-up**: Post-incident review, runbook update

### Runbook: Data Quality Degradation
1. **Detection**: Validation rate <90%
2. **Alert**: Notify data engineering team
3. **Investigation**:
   - Check ingestion error rate
   - Check source system connectivity
   - Check schema changes
4. **Resolution**:
   - Resume ingestion if paused
   - Fix data source issue
   - Quarantine bad records
5. **Follow-up**: Root cause analysis, prevention measures

### Runbook: Multi-Region Failover
1. **Detection**: Primary region unavailable
2. **Alert**: Page primary on-call + infrastructure team
3. **Action**: DNS failover to secondary region
4. **Verification**: Check data consistency, replication lag
5. **Recovery**: Restore primary region, failback after 1 hour stability
