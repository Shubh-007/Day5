# Carta Healthcare: Development Roadmap
## Phase-by-Phase Implementation Timeline

**Version**: 1.0  
**Duration**: 20+ weeks  
**Target Completion**: Q1 2027  

---

## Timeline Overview

```
Phase 0 (MVP)        Phase 1 (Scaling)       Phase 2 (Optimization)   Phase 3+ (Growth)
├─ Weeks 1-6         ├─ Weeks 7-14           ├─ Weeks 15-20           └─ Ongoing
├─ 2 eng, 1 DS       ├─ 3 eng, 2 DS          ├─ 2 eng, 3 DS, 1 sec    └─ Domain expansion
└─ Single source     └─ Multi-source         └─ 99% accuracy target
  + basic NER          + orchestration         + compliance certs
```

---

## Phase 0: MVP (Weeks 1-6)

### Objective
Proof of concept: Extract clinical entities from HL7v2 records with 90%+ accuracy using off-the-shelf BioBERT.

### Deliverables

#### Week 1: Foundation & HL7v2 Ingestion
- **Monday-Wednesday**: Development environment setup
  - [ ] Kubernetes cluster (1 GPU node, 2 CPU nodes)
  - [ ] CI/CD pipeline (GitHub Actions → ECR → ECS)
  - [ ] Logging infrastructure (CloudWatch + Loki)
  - [ ] Repository structure (src/, tests/, docs/)
  
- **Thursday-Friday**: HL7v2 Listener implementation
  - [ ] MLLP server in Python (threaded socket listener)
  - [ ] HL7 message parsing (hl7 library)
  - [ ] Schema validation (jsonschema)
  - [ ] Kafka producer (send to processing topic)
  
- **Deliverable**: 
  - HL7v2 listener accepting messages at localhost:2575
  - 1K test records processed
  - End-to-end test: Send → Parse → Publish

**Metrics**:
- Uptime: >99%
- Latency: <100ms per message
- Error rate: <0.1%

---

#### Week 2: Entity Extraction (NER)
- **Monday-Wednesday**: BioBERT model setup
  - [ ] Download pretrained BioBERT from Hugging Face
  - [ ] Convert to inference pipeline (torch.no_grad)
  - [ ] Batch processing setup (32 records at a time)
  - [ ] GPU memory optimization (quantization to INT8)
  
- **Thursday-Friday**: Extraction pipeline
  - [ ] Clinical text preprocessing (tokenization, abbreviation expansion)
  - [ ] NER inference loop
  - [ ] Entity post-processing (span extraction, type classification)
  - [ ] Confidence scoring (softmax from model)
  
- **Deliverable**:
  - BioBERT extraction on 500 HL7 records
  - Confidence scores generated
  - Precision/Recall/F1 calculated on validation set
  
**Metrics**:
- Accuracy (F1): >88%
- Throughput: 100 records/min on single GPU
- Latency: <5 sec per 100 records

---

#### Week 3: Quality Validation & Manual Review
- **Monday-Wednesday**: QA framework
  - [ ] Clinical plausibility rules (lab ranges, drug interactions)
  - [ ] Validation engine (rules DSL in JSON)
  - [ ] Low-confidence flagging (>0.75 threshold)
  - [ ] Review queue (CSV export for manual triage)
  
- **Thursday-Friday**: Manual validation
  - [ ] Domain expert review of 100 extracted records
  - [ ] Accuracy measurement (vs manual gold standard)
  - [ ] Error analysis (false positives, false negatives)
  - [ ] Feedback for model improvement
  
- **Deliverable**:
  - Validation framework
  - Manual review of 500 records
  - Accuracy report: 90.2% (F1)
  - Error log: Top 10 failure patterns

**Metrics**:
- Accuracy: 90%+
- False positive rate: <5%
- Manual review time: 2-3 min per record

---

#### Week 4: FHIR Output Generation
- **Monday-Wednesday**: FHIR bundle construction
  - [ ] fhir.resources library integration
  - [ ] Patient → Condition/Medication mapping
  - [ ] Confidence scores as FHIR extensions
  - [ ] Bundle serialization (JSON)
  
- **Thursday-Friday**: End-to-end testing
  - [ ] Process 500 records: HL7 → Extract → Validate → FHIR
  - [ ] Validate FHIR bundles (official validator)
  - [ ] Performance testing (latency per record)
  - [ ] Schema documentation
  
- **Deliverable**:
  - FHIR bundle generator
  - 500 validated FHIR bundles
  - Bundle validation pass rate: 100%
  - Sample bundle documentation

**Metrics**:
- FHIR generation time: <1 sec per bundle
- Validation pass rate: 100%
- Bundle size: 50-200KB per patient

---

#### Week 5: End-to-End Integration & Testing
- **Monday-Wednesday**: Full pipeline integration
  - [ ] Connect all modules (ingest → extract → validate → output)
  - [ ] Error handling (failed records → DLQ → alert)
  - [ ] Logging (structured JSON logs)
  - [ ] Unit tests (80%+ coverage)
  
- **Thursday-Friday**: Load & stability testing
  - [ ] Process 10K records continuously
  - [ ] Monitor resource usage (CPU, memory, GPU)
  - [ ] Identify bottlenecks
  - [ ] Performance optimization (batch sizes, caching)
  
- **Deliverable**:
  - Integrated system passing all tests
  - 10K records processed successfully
  - Stability report (uptime >99%)
  - Performance baseline

---

#### Week 6: Beta Release & Health System Pilot
- **Monday-Wednesday**: Deployment & documentation
  - [ ] Package Docker images
  - [ ] Write deployment guide
  - [ ] Create operational runbook
  - [ ] Health system onboarding kit
  
- **Thursday-Friday**: Pilot with partner health system
  - [ ] Deploy to staging environment
  - [ ] Process 1K real records from health system
  - [ ] Collect feedback
  - [ ] Validate output with clinical team
  
- **Deliverable**:
  - Beta release (v0.1.0)
  - Deployment documentation
  - 1K real records processed
  - Health system validation report
  - Go/No-go decision for Phase 1

**Success Criteria** (Phase 0→1 Gate):
- ✅ 1K HL7 records ingested
- ✅ 500 records extracted with >90% accuracy
- ✅ FHIR bundles generated and validated
- ✅ 1 health system partner validates output
- ✅ System uptime >99%
- ✅ Error rate <1%

---

## Phase 1: Production Scaling (Weeks 7-14)

### Objective
Scale to 100K records/day with multi-source ingestion, confidence-based review workflow, and production orchestration.

---

#### Week 7: Epic FHIR Connector
- **Monday-Wednesday**: Epic API integration
  - [ ] OAuth2 client setup
  - [ ] FHIR endpoint discovery
  - [ ] Pagination handling (100 records/request)
  - [ ] Error handling (rate limits, timeouts)
  
- **Thursday-Friday**: Load testing
  - [ ] Ingest 5K records/day from Epic
  - [ ] Latency testing (<500ms per request)
  - [ ] Concurrent connection tuning
  
- **Deliverable**: Epic connector production-ready, 5K records/day

---

#### Week 8: PDF Processing & OCR
- **Monday-Wednesday**: Document processing pipeline
  - [ ] PDF parser (PyPDF2, pdfplumber)
  - [ ] OCR engine (Tesseract + PaddleOCR)
  - [ ] Layout analysis (detect tables, sections)
  - [ ] Text cleanup (abbreviation expansion, de-identification)
  
- **Thursday-Friday**: Performance optimization
  - [ ] Batch OCR processing (20 pages parallel on GPU)
  - [ ] Latency target: <1 sec per page
  - [ ] Testing on real scanned clinical documents
  
- **Deliverable**: PDF processor handling 100+ pages/sec

---

#### Week 9: Confidence-Based Review Workflow
- **Monday-Wednesday**: Human review system
  - [ ] Review queue UI (simple dashboard)
  - [ ] Extract low-confidence items (<0.80)
  - [ ] Batch review (50 items per QA session)
  - [ ] Feedback storage (corrections → retraining data)
  
- **Thursday-Friday**: Integration & testing
  - [ ] Connect to extraction pipeline
  - [ ] Run pilot with 3 QA analysts
  - [ ] Measure review time (target: 2-3 min per item)
  
- **Deliverable**: Review workflow, 500 reviewed items, feedback dataset

---

#### Week 10-11: Airflow Orchestration & Deployment
- **Monday (Week 10)**: Airflow DAG design
  - [ ] Design multi-stage DAG (ingest → process → extract → validate → output)
  - [ ] Parallel task configuration (20 workers each)
  - [ ] Monitoring & alerting integration
  
- **Tuesday-Wednesday (Week 10)**: Kubernetes deployment
  - [ ] StatefulSet for Airflow scheduler
  - [ ] HPA (Horizontal Pod Autoscaler) for workers
  - [ ] Persistent volumes for data/logs
  
- **Thursday-Friday (Week 10)**: Monitoring dashboards
  - [ ] Grafana dashboards (throughput, latency, accuracy)
  - [ ] Alert rules (accuracy <98%, latency >10min)
  - [ ] Alert routing (Slack, PagerDuty)
  
- **Week 11 (entire)**: Load testing
  - [ ] Ramp to 10K records/day (Monday-Tuesday)
  - [ ] Ramp to 50K records/day (Wednesday)
  - [ ] Ramp to 100K records/day (Thursday-Friday)
  - [ ] Identify scaling bottlenecks
  - [ ] Document SLA targets
  
- **Deliverable**: Production DAG, 100K records/day capability

---

#### Week 12: Monitoring & Observability
- **Monday-Wednesday**: Observability stack
  - [ ] Prometheus metrics (throughput, latency, accuracy)
  - [ ] ELK stack (logs + search)
  - [ ] Distributed tracing (Jaeger for end-to-end visibility)
  - [ ] Dashboard templates
  
- **Thursday-Friday**: Operational runbook
  - [ ] Troubleshooting guide (common errors)
  - [ ] Scaling playbook (when/how to add workers)
  - [ ] On-call procedures (alert response, escalation)
  
- **Deliverable**: Production monitoring setup, runbook

---

#### Week 13: Load Testing & Optimization
- **Monday-Wednesday**: Performance profiling
  - [ ] CPU/memory/GPU bottleneck analysis
  - [ ] Network I/O optimization (batch sizes, compression)
  - [ ] Database query optimization (indexes, caching)
  
- **Thursday-Friday**: Optimization implementation
  - [ ] Model quantization (INT8 inference)
  - [ ] Batch size tuning (32 → 64 for better GPU utilization)
  - [ ] Connection pooling optimization
  
- **Deliverable**: 30-40% latency reduction, stable at 100K records/day

---

#### Week 14: Production Deployment & Multi-Health System Pilot
- **Monday-Wednesday**: Deployment to production
  - [ ] Blue-green deployment setup
  - [ ] Production secrets management (KMS)
  - [ ] Health checks & auto-recovery
  
- **Thursday-Friday**: Multi-health system pilot
  - [ ] Deploy to 2-3 health systems
  - [ ] Onboard Epic/Cerner connectors
  - [ ] Collect feedback
  
- **Deliverable**: Production system, 2+ health systems live

**Success Criteria** (Phase 1→2 Gate):
- ✅ 100K records/day throughput
- ✅ 95% accuracy (with confidence scoring)
- ✅ <5 min end-to-end latency
- ✅ <1% error rate
- ✅ Monitoring dashboards operational
- ✅ 2+ health systems in pilot
- ✅ Operational runbook complete

---

## Phase 2: Optimization & Compliance (Weeks 15-20)

### Objective
Achieve 99% accuracy target, implement compliance features, optimize for 66% performance improvement over baseline.

---

#### Week 15: Model Fine-Tuning
- **Day 1-2**: Collect training data
  - [ ] Review 5K manually validated records from pilots
  - [ ] Generate labeled dataset (entity boundaries + types)
  - [ ] Train/val/test split (70/15/15)
  
- **Day 3-5**: Fine-tune BioBERT
  - [ ] Start from pretrained model
  - [ ] Training on custom EHR data
  - [ ] Evaluate on validation set (target: +2-3% F1 improvement)
  - [ ] Error analysis (focus on failure patterns)
  
- **Deliverable**: Fine-tuned model achieving +2% accuracy

---

#### Week 16: Anomaly Detection & Advanced Validation
- **Monday-Wednesday**: Anomaly detection implementation
  - [ ] Implement Isolation Forest for statistical outliers
  - [ ] Train on historical data distribution
  - [ ] Tune contamination threshold (target: <2% false alarms)
  
- **Thursday-Friday**: Advanced validation rules
  - [ ] Temporal consistency checks (medications before diagnoses)
  - [ ] Clinical logic rules (drug interactions, allergies)
  - [ ] Reconciliation with medical ontologies (SNOMED, RxNorm)
  
- **Deliverable**: Anomaly detection engine, 50+ clinical rules

---

#### Week 17: MPI Integration & Cross-System Reconciliation
- **Monday-Wednesday**: Master Patient Index integration
  - [ ] Connect to health system MPI
  - [ ] Probabilistic matching (name, DOB, medical record #)
  - [ ] Handle duplicates and merges
  
- **Thursday-Friday**: Cross-system reconciliation
  - [ ] Match extracted data across EHRs
  - [ ] Flag conflicts (same test, different values within 24h)
  - [ ] Confidence boost for confirmed matches
  
- **Deliverable**: MPI integration, reconciliation logic

---

#### Week 18: HL7 v3 CDA & Compliance Features
- **Monday-Wednesday**: HL7 v3 CDA generation
  - [ ] Implement CDA document template
  - [ ] Map extracted entities to CDA concepts
  - [ ] Validate CDA documents
  
- **Thursday-Friday**: Compliance features
  - [ ] Encryption at rest (KMS)
  - [ ] Encryption in transit (TLS 1.3)
  - [ ] Audit logging (every access)
  - [ ] De-identification templates (PII masking)
  
- **Deliverable**: CDA generation, compliance framework

---

#### Week 19: Security Audit & Certification
- **Monday-Wednesday**: Internal security audit
  - [ ] Vulnerability scanning (SAST/DAST)
  - [ ] Dependency scanning (known CVEs)
  - [ ] Access control review (RBAC)
  
- **Thursday-Friday**: External security audit + HIPAA compliance
  - [ ] Third-party penetration testing
  - [ ] HIPAA risk assessment
  - [ ] BAA (Business Associate Agreement) templates
  - [ ] Compliance certification (SOC2 Type II readiness)
  
- **Deliverable**: Security audit report, BAA templates

---

#### Week 20: Performance Optimization & Production Hardening
- **Monday-Wednesday**: Performance tuning
  - [ ] Measure current baseline (minutes per 10K records)
  - [ ] Target: 90 min per 10K records (66% faster than 4-hour baseline)
  - [ ] Optimize bottlenecks (identified in load testing)
  - [ ] Database query optimization, model inference caching
  
- **Thursday-Friday**: Production hardening
  - [ ] Disaster recovery testing (RTO/RPO)
  - [ ] Failover testing (graceful degradation)
  - [ ] Load balancing optimization
  - [ ] Final production certification
  
- **Deliverable**: 66% performance improvement achieved, production-hardened system

**Success Criteria** (Phase 2 Complete - Full Production):
- ✅ 99% accuracy target reached
- ✅ 66% faster than baseline (90 min per 10K records)
- ✅ 10+ health systems live
- ✅ <$2/patient processed
- ✅ Security audit passed
- ✅ HIPAA compliance certified
- ✅ DR/failover tested
- ✅ Operational excellence achieved

---

## Phase 3+: Advanced Features (Ongoing)

### Post-Phase 2 Roadmap

**Q2 2027**: Advanced capabilities
- [ ] Temporal reasoning (disease progression patterns)
- [ ] Image analysis (radiology report extraction)
- [ ] ML outcome prediction (readmission risk)
- [ ] Real-time streaming (event-based processing)

**Q3 2027**: Expansion
- [ ] Multi-language support (Spanish, Chinese)
- [ ] Advanced relationship extraction (higher-order links)
- [ ] Graph-based analytics (patient journey visualization)
- [ ] Custom model training (per-health-system fine-tuning)

**Q4 2027+**: Scaling & ecosystem
- [ ] API marketplace (third-party integrations)
- [ ] Mobile app (field clinical documentation capture)
- [ ] Partner integrations (EHR vendors, analytics platforms)

---

## Resource Allocation

### Team Structure

**Phase 0** (6 weeks):
- 2 Backend Engineers
- 1 Data Scientist/ML Engineer
- Shared QA/DevOps resources

**Phase 1** (8 weeks):
- 3 Backend Engineers (+1)
- 2 Data Scientists (+1)
- 1 DevOps Engineer (shared)

**Phase 2** (6 weeks):
- 2 Backend Engineers (-1, focus on optimization)
- 3 Data Scientists (+1, for fine-tuning)
- 1 Security Engineer
- 1 DevOps Engineer (dedicated)

**Phase 3+**: Expand as needed

### Budget Allocation

| Phase | Personnel | Infrastructure | Software | Total |
|-------|-----------|-----------------|----------|-------|
| 0 | $250K | $50K | $20K | $320K |
| 1 | $400K | $120K | $40K | $560K |
| 2 | $400K | $100K | $40K | $540K |
| **Total (Phases 0-2)** | **$1.05M** | **$270K** | **$100K** | **$1.42M** |

---

## Risk Mitigation Timeline

| Risk | Phase | Mitigation | Owner |
|------|-------|-----------|-------|
| Model accuracy plateau | 1 | Allocate data scientist for fine-tuning; start feedback loop Week 7 | ML Lead |
| Scaling bottleneck (GPU) | 1 | Load test starting Week 13; pre-purchase GPU nodes Week 10 | DevOps |
| Data quality issues | 1 | Partner with health system IT Week 7; validation rules Week 9 | Data Quality |
| Compliance delays | 2 | Engage security team Week 10; early assessment Week 15 | Security |
| Key person dependency | All | Cross-train; documentation starting Week 1; pair programming | Tech Lead |

---

## Conclusion

This 20-week roadmap balances speed (MVP by Week 6) with rigor (99% accuracy, compliance certification by Week 20). Each phase has clear gates ensuring stakeholder alignment and technical feasibility before proceeding to the next stage.

**Next Steps**:
1. Stakeholder sign-off (this roadmap)
2. Team hiring/allocation
3. Development environment setup (Week 1)
4. Begin Phase 0
