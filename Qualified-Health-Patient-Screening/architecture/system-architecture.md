# Qualified Health - System Architecture

## LLD Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         QUALIFIED HEALTH - LLD ARCHITECTURE                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                   CLINICAL API GATEWAY (Port 443)                   │    │
│  │  - OAuth2/SMART on FHIR Auth │ Rate Limiting │ Request Validation  │    │
│  │  - Route to: Rules, Screening, Dashboards, Webhooks               │    │
│  └──────────────────┬──────────────────────────────────────────────────┘    │
│                     │                                                         │
│    ┌────────────────┼──────────────┬────────────────┬────────────────┐      │
│    │                │              │                │                │      │
│    ▼                ▼              ▼                ▼                ▼      │
│ ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│ │ INGESTION│  │NORMALIZE │  │ PATIENT  │  │ RULES    │  │SCREENING │      │
│ │ LAYER    │  │& VALIDATE│  │ GRAPH    │  │ ENGINE   │  │ ENGINE   │      │
│ │          │  │          │  │ UNIFY    │  │          │  │          │      │
│ └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘      │
│      │             │             │             │             │             │
│      └─────────────┼─────────────┼─────────────┼─────────────┘             │
│                    │             │             │                            │
│                    ▼             ▼             ▼                            │
│          ┌──────────────────────────────────────────┐                       │
│          │    DATA LAKE & WAREHOUSE (Columnar)      │                       │
│          │  - Partitioned: patient, time, source    │                       │
│          │  - OLTP cache layer for real-time ops    │                       │
│          │  - Immutable audit trail + lineage       │                       │
│          └──────┬───────────────┬───────────────────┘                       │
│                 │               │                                            │
│          ┌──────▼──────┐  ┌─────▼──────────┐                                │
│          │  ANALYTICS  │  │  ML MODELS     │                                │
│          │  & REPORTING│  │  SERVICE       │                                │
│          └──────┬──────┘  └─────┬──────────┘                                │
│                 │               │                                            │
│                 └───────┬───────┘                                            │
│                         ▼                                                    │
│              ┌──────────────────────┐                                        │
│              │  DASHBOARD & EXPORT  │                                        │
│              │  - Real-time UI      │                                        │
│              │  - PDF/CSV Export    │                                        │
│              │  - EHR BI Integration│                                        │
│              └──────────────────────┘                                        │
│                                                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │           SECURITY & COMPLIANCE (Cross-cutting)                      │   │
│  │  - AES-256 encryption (at-rest, in-transit TLS)  - RBAC            │   │
│  │  - Audit logging + retention  - Key rotation  - De-identification   │   │
│  │  - HIPAA/HITRUST controls     - Data retention policies             │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │        EXTERNAL DATA SOURCES (Real-time & Batch)                    │   │
│  │  - EHR Systems (HL7v2, FHIR)  │ Labs │ Imaging │ Claims │ Wearables│   │
│  │  - Message Queues (Kafka/RabbitMQ) │ Dead-letter handling           │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘

Data Flows:
1. Ingestion: EHR/Labs/Claims → Message Queue → Data Lake
2. Normalization: Raw events → Standardized concepts (SNOMED/LOINC/ICD-10)
3. Patient Matching: Multi-source MRN mapping → Unified patient graph
4. Screening: Patient record + rules → Candidate ranking + confidence
5. Analytics: Screening results → Dashboard + Reports + Outcomes tracking
```

## Module Interfaces & Data Structures

### 1. Multi-Source Data Ingestion Layer
**Supported Protocols**: HL7 v2, FHIR REST, S3 batch files, Kafka/RabbitMQ streams
**Error Handling**: Circuit breaker on 3 failed retries, dead-letter queue, exponential backoff (1s → 8s)
**Throughput**: 10K-100K events/sec at scale

### 2. Data Normalization & Integration Engine
**Ontologies**: SNOMED-CT, LOINC, ICD-10, RxNorm
**Quality Validation**: Schema checks, null handling, temporal consistency, deduplication
**Alert Threshold**: >5% parse failure rate triggers notification

### 3. Patient Record Unification & Graph
**Matching Confidence**: Probability-based (name similarity: 0.85, DOB match: true, MRN: false, SSN: true)
**Graph Operations**: Encounter timeline, relationship traversal, merge conflict detection
**Key Index**: patient_id, mrn, npi_hash (SHA-256)

### 4. Clinical Rules Engine
**Rule Format**: JSON/DSL with versioning and effective dates
**Evaluation**: Boolean logic, temporal patterns (min/max gap days), comorbidity algorithms
**Timeout**: 5s per rule evaluation

### 5. Candidate Screening & Prioritization Engine
**Ranking Factors**: Rule pass/fail, confidence score, ML prediction, urgency signals
**Output**: CandidateList with rank, confidence, ready_for_contact flag, evidence snapshot
**Batch Capability**: 500K patients in 2-4 hours with checkpointing

### 6. ML Models Service
**Feature Engineering**: Automated extraction from patient records
**Model Versioning**: Track all versions, performance metrics, hyperparameters
**A/B Testing**: Compare models on test cohort, significance testing
**Prediction Caching**: 1-hour TTL for real-time operations

### 7. Security & Compliance Module
**Encryption**: AES-256 at-rest, TLS 1.3 in-transit
**Key Management**: AWS KMS, annual rotation (90-day cycle)
**Audit Trail**: Immutable append-only, 7-year HIPAA retention
**Access Control**: RBAC with role-based screening, RBAC/ABAC for resources

### 8. Clinical API Gateway
**Authentication**: OAuth2/SMART on FHIR, JWT validation
**Rate Limiting**: 100 req/min per API key, burst allowance 20%
**Response Codes**: 401 (auth failure), 429 (rate limit), 400 (validation), 503 (timeout)
**Webhooks**: Event-based callbacks for treatment outcomes

### 9. Analytics, Reporting & Dashboard Layer
**Report Types**: Cohort analysis, PDF/CSV exports, BI integration
**Dashboards**: Real-time candidate lists, conversion metrics, intervention distribution
**Export Limits**: Enforced size limits, de-identification verification on export

### 10. Data Lake & Warehouse
**Storage Format**: Columnar (Parquet/Iceberg) for analytics efficiency
**Partitioning**: Date (daily) + patient_id_range for scalability
**OLTP Cache**: Redis with 1-hour TTL for real-time candidate checks
**Backup**: Daily incremental, weekly full, 7-year cold storage (Glacier)

## Database Design

**Core Tables**:
- `patient_master_index` (PMI): Central patient registry with demographics
- `mrn_mapping`: System-to-system MRN linking with confidence scores
- `encounters`: Admission/discharge records with diagnoses, procedures
- `clinical_events`: Labs, medications, vitals with normalized codes
- `medications`: Prescriptions with RxNorm codes
- `lab_results`: Test results with LOINC codes
- `clinical_rules`: Versioned rules with JSON DSL
- `screening_results`: Patient-intervention evaluations with confidence scores
- `audit_log`: Immutable 7-year HIPAA compliance trail

**Indexing Strategy**: patient_id, encounter_date, normalized_code, facility_id (all tables)
**Partitioning**: Date (monthly for old data) + patient_id_range
**Replication**: Multi-region streaming (PostgreSQL), <5s RPO, automatic failover

## Technology Stack

**Compute**: Kubernetes (AWS EKS / GCP GKE)
**Database**: PostgreSQL 15+ (primary + replicas), Redis 7+ (OLTP cache)
**Message Queue**: Kafka or RabbitMQ (3-node cluster, mirrored queues)
**Storage**: S3/GCS (data lake, backups), Glacier (7-year cold storage)
**Observability**: ELK stack (logs), Prometheus (metrics), Jaeger (tracing), Grafana (dashboards)
**API Gateway**: Kong or AWS API Gateway
**ML**: Feature store (Feast), model registry (MLflow), training (Spark)

## Scaling Patterns

**Horizontal Scaling**: Stateless ingestion, normalization, screening services scale to 10+ instances
**Load Balancing**: Sticky sessions for clinician WebSocket connections, round-robin for batch jobs
**Caching Strategy**: L1 (in-memory), L2 (Redis), invalidation via event-based pub/sub
**Async Processing**: Large cohorts processed asynchronously with progress checkpointing
**Auto-scaling**: HPA based on CPU/memory, custom metrics (queue depth, latency)

## Disaster Recovery

**RTO/RPO**: RTO <4 hours, RPO <1 hour
**Multi-region**: Active-active in 2+ regions, <5s replication lag
**Backup Verification**: Monthly restore testing with checksum validation
**Failover**: Automatic DNS failover, geo-routing load balancer
