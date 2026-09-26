# Qualified Health - Patient Screening Platform Comprehensive Plan

**Project**: Identifying Patients for Life-Saving Treatments  
**Use Case**: Screens large patient populations against fragmented medical records to surface candidates for evidence-based interventions  
**Status**: GO with phased execution and gating  
**Generated**: 2026-09-26

---

## Executive Summary

Qualified Health is a distributed healthcare analytics platform that screens large patient populations across fragmented medical records to identify candidates for evidence-based life-saving treatments. The system integrates data from multiple clinical sources (EHRs, labs, imaging, claims), normalizes heterogeneous formats, and applies clinical rules engines to surface high-value intervention candidates while prioritizing privacy, HIPAA compliance, and real-time clinical decision support.

**Recommendation**: **GO with phased execution**. This architecture is well-designed for multi-system healthcare integration with proven patterns. Key success factors: clinical advisory board governance, data quality monitoring, single health system validation in v0, FDA pathway planning by month 12.

---

## Part 1: High-Level Design (HLD)

### Core Components (10 Services)

1. **Multi-Source Data Ingestion Layer** - Connects to fragmented clinical data sources (EHRs, labs, imaging, claims, wearables), handles protocol diversity (HL7 v2, FHIR, proprietary APIs), implements real-time streams and batch imports

2. **Data Normalization & Integration Engine** - Standardizes disparate formats to clinical ontologies (SNOMED-CT, LOINC, ICD-10, RxNorm), performs validation, deduplication, temporal consistency checks

3. **Patient Record Unification & Graph** - Resolves patient identity across systems using probabilistic matching, maintains patient graph and encounter history

4. **Clinical Rules Engine** - Applies evidence-based criteria logic with declarative JSON/DSL format, versioned rules, temporal pattern matching, auditability

5. **Candidate Screening & Prioritization Engine** - Filters qualified candidates, applies risk-stratification models, ranks by intervention impact and urgency

6. **Security & Compliance Module** - HIPAA/HITRUST compliance (AES-256, TLS 1.3, RBAC, audit logging, key rotation, 7-year retention)

7. **Clinical API Gateway** - RESTful FHIR-aligned APIs for EHR integration, rate limiting, OAuth2/SMART on FHIR auth, webhooks for outcomes

8. **Analytics, Reporting & Dashboard Layer** - Real-time dashboards, cohort analysis, clinician-facing prioritized candidate lists, CSV/PDF exports

9. **ML Models Service** - Predictive models for ranking, outcome estimation, feature engineering, model versioning, A/B testing

10. **Data Lake & Warehouse** - Centralized immutable repository (columnar format), partitioned by patient/time/source, separate OLTP cache

### Scale Targets

| Dimension | Target |
|-----------|--------|
| **Health Systems** | 2-5 initial, 50+ long-term |
| **Patient Populations** | 10-50M total, 500K-5M per system |
| **Active Clinicians** | 10-100 per system, 10K+ at scale |
| **Historical Data** | 10-100GB per system (compressed) |
| **Real-time Throughput** | 10K-100K events/sec at scale |
| **Single Patient Lookup** | 100-500ms end-to-end |
| **Batch Screening** | 500K patients in 2-4 hours |
| **API Uptime** | 99.5% SLA |
| **API Latency** | <200ms p95 |

### Redundancy Strategy

- **Multi-region active-active** deployment (2+ regions)
- **Database replication** with <5 second RPO
- **Geo-routing** load balancing
- **Daily snapshots** + weekly full backups (7-year cold storage)
- **Circuit breakers** for EHR dependencies
- **Graceful degradation** with fallback to cached state

### Version Strategy

**v0 (MVP, 3 months)**: Single health system, HL7 v2 source, basic patient matching, hard-coded rules (1-2 intervention types), manual workflows

**v1 (Multi-source, 6 months)**: 2-3 health systems, FHIR APIs, patient graph unification, declarative rules engine, automated prioritization, dashboards, cloud deployment

**v2 (ML-Enhanced, 8 months)**: 5-10 health systems, ML outcome prediction, model A/B testing, real-time feature engineering, advanced analytics

**v3+ (Enterprise, ongoing)**: 50+ health systems, federated learning, FDA premarket readiness, HITRUST certification, longitudinal outcomes

---

## Part 2: Low-Level Design (LLD)

### 10 Modules with Detailed Interfaces

#### Module 1: Multi-Source Data Ingestion Layer
- **Interfaces**: HL7v2Parser, FHIRClient, BatchFileProcessor, RealtimeStreamListener, IngestionController
- **Error Handling**: Circuit breaker, dead-letter queues, exponential backoff (1s→8s), graceful degradation
- **Key Feature**: Protocol diversity support (HL7v2, FHIR, proprietary APIs, flat files)

#### Module 2: Data Normalization & Integration Engine
- **Interfaces**: Normalizer, QualityValidator, DeduplicationService, OntologyMapper, TemporalConsistency
- **Error Handling**: Quarantine table for failures, fuzzy matching for dedup, rollback on >10% concept drift
- **Key Feature**: Standard ontology mapping (SNOMED-CT, LOINC, ICD-10, RxNorm)

#### Module 3: Patient Record Unification & Graph
- **Interfaces**: PatientResolver, PatientGraphBuilder, RecordMerger, TimelineService, PatientStore
- **Error Handling**: Probabilistic matching confidence threshold (>0.8), conflict queues for manual review
- **Key Feature**: Identity resolution across fragmented systems

#### Module 4: Clinical Rules Engine
- **Interfaces**: RulesEvaluator, RuleBuilder, RulesVersioning, ComorbidityCalculator, TemporalMatcher
- **Error Handling**: Rule syntax validation, circular dependency detection, 5s evaluation timeout
- **Key Feature**: Declarative JSON/DSL format with version control

#### Module 5: Candidate Screening & Prioritization Engine
- **Interfaces**: ScreeningEngine, PrioritizationService, CohortFilter, EvidenceBuilder, ConfidenceCalculator
- **Error Handling**: ML model unavailability fallback to rule-only scoring, 4-hour batch timeout
- **Key Feature**: Risk-stratification and urgency-based ranking

#### Module 6: ML Models Service
- **Interfaces**: ModelRegistry, ModelPredictor, FeatureEngineer, ModelTrainer, ABTest
- **Error Handling**: Fallback to previous model version, prediction caching (1h TTL), model drift detection
- **Key Feature**: Feature engineering pipeline, model versioning, A/B testing

#### Module 7: Security & Compliance Module
- **Interfaces**: EncryptionService, TLSManager, AccessControl, AuditLogger, KeyRotationService, DeIdentifier
- **Error Handling**: Encryption failure circuit breaker, permission denied + admin notify, audit log queue fallback
- **Key Feature**: AES-256 at-rest, TLS 1.3, RBAC, 7-year audit retention

#### Module 8: Clinical API Gateway
- **Interfaces**: RESTController (candidates, evaluate, export, webhooks), WebhookManager, RateLimiter
- **Error Handling**: 401 on invalid API key, 429 on rate limit, 400 on validation errors, 503 on timeout with fallback
- **Key Feature**: FHIR-aligned, SMART on FHIR auth, webhook callbacks

#### Module 9: Analytics, Reporting & Dashboard Layer
- **Interfaces**: ReportGenerator, DashboardService, CohortAnalysis, OutcomeTracker, ExportService
- **Error Handling**: Large cohort async processing (>10K patients), export size limits, data anomaly alerts
- **Key Feature**: Real-time dashboards, PDF/CSV exports, BI integration

#### Module 10: Data Lake & Warehouse
- **Interfaces**: DataLakeWriter, DataLakeReader, PartitionManager, OLTPCache, BackupService
- **Error Handling**: Write retry to backup partition, read circuit breaker + cache fallback, corruption detection + restore
- **Key Feature**: Columnar storage (Parquet/Iceberg), partitioned by date + patient_id_range

### Database Schema (Key Tables)

**Patient Master Index**: patient_id, mrn, npi_hash, demographics, status
**MRN Mapping**: System-to-system linking with confidence scores
**Encounters**: admission/discharge, facility, provider, diagnoses, procedures
**Clinical Events**: labs, meds, vitals, diagnoses with SNOMED/LOINC codes
**Clinical Rules**: Versioned rules with JSON DSL definitions
**Screening Results**: Patient-intervention-rule evaluation results with confidence scores
**Audit Log**: 7-year immutable retention for HIPAA compliance
**ML Predictions**: Outcome probabilities with model version tracking

**Indexing Strategy**: Patient_id, encounter_date, normalized_codes, facility_id (all with proper indexes)
**Partitioning**: Daily + patient_id_range for scalability
**Caching**: Redis OLTP layer (1-hour TTL for frequently accessed data)

---

## Part 3: Implementation Plan (21+ Weeks)

### Phase 0: Infrastructure & Pilot Setup (Weeks 1-4)

**Week 1-2**: Cloud environment provision, KMS/encryption setup, VPC/networking
**Week 3-4**: HL7v2 parser, FHIR client, S3 batch processor, Kafka listeners, dead-letter queues

**Deliverables**: Cloud infrastructure, data ingestion framework, compliance baseline

### Phase 1: Data Integration & Rules Engine (Weeks 5-12)

**Week 5-6**: Patient matching algorithm (PMI), probabilistic matching, deduplication
**Week 7-8**: Encounter/clinical event storage, patient graph, timeline service
**Week 9-12**: Rules engine DSL parser, temporal pattern matching, rule versioning

**Deliverables**: Unified patient records, versioned rules engine, clinical validation

### Phase 2: Screening & Workflow Automation (Weeks 13-20)

**Week 13-14**: Screening engine, candidate filtering, confidence scoring
**Week 15-16**: Clinical API Gateway, authentication, rate limiting, error handling
**Week 17-20**: Clinician dashboard, outcome tracking, advanced reporting

**Deliverables**: End-to-end screening pipeline, clinician interface, outcome tracking

### Phase 3: Analytics & Multi-System Scale (Weeks 21-28)

**Week 21-24**: Data warehouse (Parquet), columnar storage, OLTP cache layer
**Week 25-28**: Multi-region active-active, geo-routing failover, disaster recovery

**Deliverables**: Scalable analytics, multi-region deployment, 2-3 additional health systems

### Phase 4: ML & Production Hardening (Weeks 29-40)

**Week 29-32**: Feature engineering, model trainer, A/B testing framework
**Week 33-36**: Security audit, penetration testing, HIPAA/HITRUST controls
**Week 37-40**: SLA monitoring, performance tuning, production readiness

**Deliverables**: ML models in production, security audit pass, enterprise-ready infrastructure

### Phase 5+: Operations & Continuous Improvement (Ongoing)

- Production support, SLA monitoring
- Rule and model iteration based on outcomes
- v2+ feature development

---

## Part 4: Risk Analysis

### High-Risks

1. **Data Quality** (10-100GB+ fragmented data) → Mitigation: Comprehensive validation layer, anomaly detection, quarantine tables, manual review queues

2. **HIPAA Compliance** (audit failures, breaches, regulatory fines) → Mitigation: Dedicated compliance module, quarterly audits, 7-year immutable retention

3. **Patient Identity Errors** (wrong records merged) → Mitigation: Probabilistic confidence thresholds (>0.8), conflict detection, manual review, versioning

4. **Scale Performance** (<2-4h batch screening) → Mitigation: OLTP caching, indexing, async processing with checkpoints, auto-scaling

5. **EHR Dependency** (cascading failures if sources down) → Mitigation: Circuit breakers, fallback to cache, graceful degradation

6. **Clinical Rule Accuracy** (missed interventions or wrong treatment) → Mitigation: Rules versioning, clinical advisory board, evidence auditing, feedback loops

7. **ML Model Drift** (predictions become inaccurate) → Mitigation: Performance monitoring, drift detection, A/B testing, frequent retraining

---

## Part 5: Success Metrics

### v0 MVP Criteria (Month 3)
- Single health system pilot operational
- 90%+ rule accuracy (independently validated)
- <500ms patient lookup latency
- 99% system availability
- HIPAA encryption verified

### v1 Success (Month 9)
- 2-3 health systems live
- 1M+ patient records processed
- 90%+ clinician adoption
- Multi-EHR integration working
- <200ms API p95 latency

### v2 Success (Month 18)
- 5-10 health systems at scale
- ML models improving candidate ranking
- Real-world outcomes tracking
- 99.5% availability sustained

---

## Part 6: Recommendations & Decision Gates

### Critical Success Factors

1. **Clinical Advisory Board**: Form with 3-5 domain experts before v0 to validate rules and outcomes
2. **Data Quality Monitoring**: Dashboard from week 3 tracking validation rates, anomalies, reconciliation
3. **Offline Mode**: Candidate screening and API responses function with cached data if data lake unavailable
4. **Event Sourcing**: Immutable event log for audit trail and state reconstruction
5. **Explainability Layer**: SHAP values for ML predictions to ensure clinician transparency
6. **Synthetic Monitoring**: Daily test patient injection through full pipeline to validate end-to-end
7. **Canary Deployments**: New rules/models to 5% of traffic for 24h before full rollout
8. **FDA Engagement**: Pre-Sub meeting by month 12 to clarify regulatory pathway (510(k) vs De Novo)

### Phase Gate Criteria

**v0 → v1 Gate**: 90%+ rule accuracy, <10% data reconciliation failures, HIPAA audit pass
**v1 → v2 Gate**: 99.5% uptime, multi-EHR integration success, <200ms API latency
**v2 → v3 Gate**: Real-world outcomes evidence, FDA pathway clarity, HITRUST certification

### Go/No-Go Decision

**PROCEED with conditions**:
- ✓ Clinical advisory board formed before month 1
- ✓ Data quality monitoring implemented by week 3
- ✓ v0 single health system validation by month 3 with 90%+ accuracy
- ✓ Explicit v0→v1 gate before scaling to multiple systems
- ✓ FDA engagement by month 12

**Resource**: 15-20 FTE immediately (backend, infra, compliance, clinical), growing to 40-50 FTE by month 12

**Budget**: $3-5M/year infrastructure (multi-region, managed services), $2-3M/year personnel, $500K-1M regulatory/legal starting month 12

---

## Conclusion

This platform addresses a critical healthcare need: identifying patients for life-saving interventions across fragmented systems. The architecture demonstrates enterprise-grade patterns with security-first design, realistic scaling strategy, and clinical governance mechanisms. Success depends on clinical validation, data quality rigor, and FDA pathway planning starting early.

**Status**: GO with phased execution and gating. Ready for Phase 0 infrastructure kickoff.

---

**Plan Version**: v0.1  
**Generated**: Multi-Agent Orchestration Workflow  
**Confidence**: High (healthcare integration, compliance, scale patterns proven)
