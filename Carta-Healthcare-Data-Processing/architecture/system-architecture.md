# Carta Healthcare: System Architecture
## Detailed Technical Design

**Version**: 1.0  
**Date**: 2026-09-26  
**Scope**: Core extraction platform architecture

---

## 1. Ingestion Architecture

### Connector Framework

```python
# Abstract base for all connectors
class SourceConnector(ABC):
    @abstractmethod
    def connect(self, config: ConnectorConfig) -> Connection:
        """Establish connection to source system"""
        pass
    
    @abstractmethod
    def fetch(self, query: SourceQuery) -> List[SourceRecord]:
        """Fetch records from source"""
        pass
    
    @abstractmethod
    def validate_schema(self, record: SourceRecord) -> ValidationResult:
        """Validate record against expected schema"""
        pass
```

### Connector Implementations

#### Epic FHIR Connector
- **Protocol**: REST HTTPS + OAuth2
- **Auth**: Client credentials flow
- **Endpoints**: `/Patient/$everything`, `/Observation`, `/Condition`
- **Batch size**: 100 records per request
- **Retry**: 3 attempts, exponential backoff

#### HL7v2 Listener
- **Protocol**: MLLP (Minimal Lower Layer Protocol)
- **Port**: 2575 (configurable)
- **Message types**: ADT, ORU, OBX
- **Queue**: Kafka topic per health system
- **Format**: HL7 v2.5 UTF-8

#### S3/SFTP File Processor
- **Trigger**: SNS event (S3) or polling (SFTP)
- **Formats**: PDF, TIFF, HL7 text, CSV
- **Processing**: Batch → queue → document processor

---

## 2. Document Processing Architecture

### NLP Pipeline

```
Input Text
  ↓
[Tokenizer] → [Segmenter] → [POS Tagger]
  ↓
[Clinical Normalizer] → [Abbreviation Expander]
  ↓
[Entity Recognizer (BioBERT)] → [Confidence Scorer]
  ↓
[Relation Extractor] → [Entity Linker]
  ↓
Structured Entities + Relations
```

### Model Configuration

**Primary Models**:
- BioBERT-base-cased-v1.2: 12 layers, 768 hidden
- Fine-tuned on 10K labeled EHR examples
- Retraining: Monthly (incremental learning)

**Entity Recognition**:
```json
{
  "model": "biobert_cased_v1.2",
  "task": "token_classification",
  "entity_types": [
    "B-CONDITION", "I-CONDITION",
    "B-MEDICATION", "I-MEDICATION",
    "B-LAB", "I-LAB",
    "B-PROCEDURE", "I-PROCEDURE",
    "B-ALLERGY", "I-ALLERGY",
    "B-VITAL", "I-VITAL",
    "B-IMAGING", "I-IMAGING",
    "O"  // not an entity
  ]
}
```

**Relation Extraction**:
```json
{
  "model": "relation_extraction_v1",
  "task": "classification",
  "relations": [
    "treats",
    "contraindicated_in",
    "worsens",
    "improves",
    "indicates_for",
    "no_relation"
  ]
}
```

---

## 3. Extraction Quality Assurance

### Confidence Scoring Formula

```
confidence = α₁ × model_confidence 
           + α₂ × context_score 
           + α₃ × temporal_consistency 
           + α₄ × spelling_confidence

where:
  α₁ = 0.5 (NER model primary signal)
  α₂ = 0.25 (contextual evidence)
  α₃ = 0.15 (temporal alignment)
  α₄ = 0.10 (spelling/typographical)
```

**Example Calculation**:
```
Entity: "metformin 500mg"
- model_confidence: 0.92
- context_score: 0.88 (appears in medication list section)
- temporal_consistency: 0.90 (consistent with historical records)
- spelling_confidence: 0.98 (exact match in drug database)

final_confidence = 0.5×0.92 + 0.25×0.88 + 0.15×0.90 + 0.10×0.98
                 = 0.46 + 0.22 + 0.135 + 0.098
                 = 0.913  ≈ 91.3%
```

### Validation Rules Engine

```python
class ValidationRule:
    def __init__(self, rule_id: str, entity_type: str):
        self.rule_id = rule_id
        self.entity_type = entity_type
    
    def validate(self, entity: Entity) -> ValidationResult:
        """Check entity against rule"""
        pass
    
    def explain(self) -> str:
        """Human-readable explanation of rule"""
        pass

# Registry of clinical rules
VALIDATION_RULES = {
    "lab_range_hemoglobin": LabRangeRule(
        min_value=7.0,
        max_value=18.0,
        unit="g/dL"
    ),
    "drug_interaction_warfarin": DrugInteractionRule(
        drug1="warfarin",
        drug2="ibuprofen",
        severity="error"
    ),
    "temporal_pregnancy_vasectomy": TemporalRule(
        condition1="pregnancy",
        condition2="vasectomy",
        min_years=0.5
    )
}
```

---

## 4. Data Persistence Layer

### Schema: Extracted Entities

```sql
CREATE TABLE extracted_entities (
    id UUID PRIMARY KEY,
    source_id VARCHAR(255) NOT NULL,  -- reference to original record
    patient_id VARCHAR(255) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,  -- diagnosis, medication, etc.
    entity_value VARCHAR(4096) NOT NULL,
    confidence DECIMAL(3,2),  -- 0.0-1.0
    extracted_at TIMESTAMP,
    source_system VARCHAR(50),  -- Epic, Cerner, HL7v2
    validation_status VARCHAR(20),  -- passed, failed, warning
    error_details JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_patient_entity_type (patient_id, entity_type),
    INDEX idx_confidence (confidence),
    INDEX idx_extracted_at (extracted_at)
);

CREATE TABLE extracted_relations (
    id UUID PRIMARY KEY,
    source_entity_id UUID REFERENCES extracted_entities(id),
    target_entity_id UUID REFERENCES extracted_entities(id),
    relation_type VARCHAR(50),  -- treats, contraindicated_in, etc.
    confidence DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Storage Strategy

**Hot Storage** (recent: <30 days):
- PostgreSQL (transactional queries)
- Redis cache (high-confidence entities)
- Performance: <100ms p95 latency

**Warm Storage** (recent: 30 days - 1 year):
- Snowflake (analytics-optimized)
- Compressed Parquet (columnar)
- Searchable: Full patient timelines

**Cold Storage** (archive: >1 year):
- S3/Glacier
- Immutable, encrypted
- Audit trail preserved

---

## 5. Output Generation

### FHIR Bundle Generation

```python
def generate_fhir_bundle(patient: Patient, entities: List[Entity]) -> Bundle:
    """Generate FHIR R4 Bundle from extracted entities"""
    
    bundle = Bundle()
    bundle.type = "transaction"
    
    # 1. Patient resource
    patient_resource = Patient()
    patient_resource.id = patient.id
    patient_resource.name = [HumanName(text=patient.name)]
    bundle.add_entry(BundleEntry(resource=patient_resource))
    
    # 2. Condition resources
    for entity in entities:
        if entity.type == "diagnosis":
            condition = Condition()
            condition.subject = Reference(f"Patient/{patient.id}")
            condition.code = CodeableConcept(
                coding=[Coding(
                    system="http://snomed.info/sct",
                    code=snomed_lookup(entity.value)
                )]
            )
            # Add confidence as extension
            condition.extension = [
                Extension(
                    url="extraction-confidence",
                    valueDecimal=entity.confidence
                )
            ]
            bundle.add_entry(BundleEntry(resource=condition))
    
    # 3. Medication resources
    for entity in entities:
        if entity.type == "medication":
            medication_statement = MedicationStatement()
            medication_statement.subject = Reference(f"Patient/{patient.id}")
            medication_statement.medicationCodeableConcept = CodeableConcept(
                coding=[Coding(
                    system="http://www.nlm.nih.gov/research/umls/rxnorm",
                    code=rxnorm_lookup(entity.value)
                )]
            )
            bundle.add_entry(BundleEntry(resource=medication_statement))
    
    return bundle
```

### HL7 v3 CDA Document

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <realmCode code="US"/>
    <typeId root="2.16.840.1.113883.1.3" extension="POCD_HD000040"/>
    
    <id root="1.2.3.4.5" extension="extracted_doc_12345"/>
    <code code="34133-9" codeSystem="2.16.840.1.113883.6.1" displayName="Summary of care document"/>
    
    <title>Extracted Clinical Summary</title>
    <effectiveTime value="20260926"/>
    
    <recordTarget>
        <patientRole>
            <id root="1.2.3.4.5" extension="patient_12345"/>
            <patient>
                <name>John Doe</name>
            </patient>
        </patientRole>
    </recordTarget>
    
    <component>
        <structuredBody>
            <component>
                <section>
                    <title>Problems</title>
                    <entry>
                        <act classCode="ACT" moodCode="EVN">
                            <code code="44054006" codeSystem="2.16.840.1.113883.6.96" displayName="type 2 diabetes"/>
                            <statusCode code="active"/>
                            <effectiveTime value="20260926"/>
                        </act>
                    </entry>
                </section>
            </component>
        </structuredBody>
    </component>
</ClinicalDocument>
```

---

## 6. Orchestration & Scaling

### Airflow DAG Structure

```python
from airflow import DAG
from airflow.operators.kubernetes_pod_operator import KubernetesPodOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'carta-healthcare',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(hours=2)
}

dag = DAG(
    'carta_extraction_daily',
    default_args=default_args,
    schedule_interval='0 2 * * *',  # 2 AM UTC daily
    start_date=datetime(2026, 1, 1)
)

# Task 1: Ingest from all sources (parallel)
ingest_epic = KubernetesPodOperator(
    task_id='ingest_epic',
    image='carta/connector:latest',
    cmds=['python', 'ingestion/epic_connector.py'],
    env_vars={'CONNECTOR_TYPE': 'epic', 'BATCH_SIZE': '100'},
    pool_slots=5  # 5 concurrent instances
)

ingest_hl7 = KubernetesPodOperator(
    task_id='ingest_hl7',
    image='carta/connector:latest',
    cmds=['python', 'ingestion/hl7_connector.py'],
    env_vars={'CONNECTOR_TYPE': 'hl7v2'},
    pool_slots=1  # Always running listener
)

# Task 2: Document processing (parallel, GPU)
process_docs = KubernetesPodOperator(
    task_id='process_documents',
    image='carta/processor:latest',
    cmds=['python', 'processing/document_processor.py'],
    resources={
        'limit_memory': '16Gi',
        'limit_cpu': '4',
        'limit_gpu': '1'  # 1 GPU per pod
    },
    pool_slots=20,  # 20 GPU workers
    parallelism=20
)

# Task 3: Entity extraction (parallel, GPU)
extract_entities = KubernetesPodOperator(
    task_id='extract_entities',
    image='carta/extractor:latest',
    cmds=['python', 'extraction/entity_extractor.py'],
    resources={
        'limit_memory': '32Gi',
        'limit_cpu': '8',
        'limit_gpu': '2'  # 2 GPUs per pod
    },
    pool_slots=20,
    parallelism=20
)

# Task 4: Validation (parallel, CPU)
validate_data = KubernetesPodOperator(
    task_id='validate_data',
    image='carta/validator:latest',
    cmds=['python', 'validation/validator.py'],
    resources={
        'limit_memory': '8Gi',
        'limit_cpu': '4'
    },
    pool_slots=10,
    parallelism=10
)

# Task 5: Generate FHIR output (parallel)
generate_fhir = KubernetesPodOperator(
    task_id='generate_fhir',
    image='carta/output-generator:latest',
    cmds=['python', 'output/fhir_generator.py'],
    pool_slots=5,
    parallelism=5
)

# Task 6: Upload to data lake (serial)
upload_to_datalake = KubernetesPodOperator(
    task_id='upload_to_datalake',
    image='carta/uploader:latest',
    cmds=['python', 'output/datalake_uploader.py'],
    pool_slots=1
)

# Define dependencies
[ingest_epic, ingest_hl7] >> process_docs >> extract_entities >> validate_data >> generate_fhir >> upload_to_datalake
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: carta-extraction-workers
  namespace: carta-healthcare
spec:
  replicas: 20  # GPU worker nodes
  selector:
    matchLabels:
      app: extraction-worker
  template:
    metadata:
      labels:
        app: extraction-worker
    spec:
      nodeSelector:
        accelerator: gpu
      containers:
      - name: extractor
        image: carta/extractor:v1.0
        resources:
          requests:
            nvidia.com/gpu: 2
            memory: "32Gi"
            cpu: "8"
          limits:
            nvidia.com/gpu: 2
            memory: "32Gi"
            cpu: "8"
        env:
        - name: BATCH_SIZE
          value: "32"
        - name: MODEL_CACHE
          value: "/mnt/models"
        volumeMounts:
        - name: model-cache
          mountPath: /mnt/models
      volumes:
      - name: model-cache
        persistentVolumeClaim:
          claimName: model-cache-pvc
```

---

## 7. Monitoring & Observability

### Key Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

# Throughput
records_processed = Counter(
    'carta_records_processed_total',
    'Total records processed',
    ['source_system', 'entity_type']
)

extraction_latency = Histogram(
    'carta_extraction_latency_seconds',
    'Time to extract entities',
    buckets=[1, 5, 10, 30, 60, 300]
)

# Quality
extraction_accuracy = Gauge(
    'carta_extraction_accuracy',
    'Current extraction accuracy',
    ['entity_type']
)

confidence_distribution = Histogram(
    'carta_confidence_distribution',
    'Distribution of confidence scores',
    buckets=[0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0],
    ['entity_type']
)

validation_failures = Counter(
    'carta_validation_failures_total',
    'Records failing validation',
    ['rule_id', 'severity']
)

# Infrastructure
gpu_utilization = Gauge(
    'carta_gpu_utilization_percent',
    'GPU utilization',
    ['worker_id']
)

queue_depth = Gauge(
    'carta_processing_queue_depth',
    'Number of pending records',
    ['queue_type']
)
```

### Alert Rules

```yaml
groups:
- name: carta_healthcare
  rules:
  - alert: ExtractionAccuracyLow
    expr: carta_extraction_accuracy < 0.985
    for: 10m
    annotations:
      summary: "Extraction accuracy below 98.5%"
      action: "Review model performance, check data quality"
  
  - alert: ProcessingLatencyHigh
    expr: histogram_quantile(0.95, carta_extraction_latency_seconds) > 300
    for: 5m
    annotations:
      summary: "P95 latency above 5 minutes"
      action: "Scale workers, investigate bottleneck"
  
  - alert: ValidationFailureRateHigh
    expr: rate(carta_validation_failures_total[5m]) > 0.02
    for: 5m
    annotations:
      summary: "Validation failure rate >2%"
      action: "Check rule configurations, source data quality"
  
  - alert: GPUMemoryLeak
    expr: increase(carta_gpu_utilization_percent[1h]) > 5
    annotations:
      summary: "GPU memory utilization increasing"
      action: "Investigate GPU worker processes"
```

---

## 8. Security & Compliance

### Data Protection

```python
from cryptography.fernet import Fernet

class PatientDataProtector:
    def __init__(self, kms_key_id: str):
        self.kms_client = boto3.client('kms')
        self.kms_key_id = kms_key_id
    
    def encrypt_pii(self, data: str) -> str:
        """Encrypt PII using KMS"""
        response = self.kms_client.encrypt(
            KeyId=self.kms_key_id,
            Plaintext=data.encode()
        )
        return base64.b64encode(response['CiphertextBlob']).decode()
    
    def decrypt_pii(self, encrypted_data: str) -> str:
        """Decrypt PII from KMS"""
        ciphertext_blob = base64.b64decode(encrypted_data)
        response = self.kms_client.decrypt(CiphertextBlob=ciphertext_blob)
        return response['Plaintext'].decode()
    
    def pseudonymize_patient(self, patient_id: str) -> str:
        """Generate pseudonym for reporting"""
        import hashlib
        salt = self.kms_key_id[:16]
        return hashlib.sha256(f"{patient_id}{salt}".encode()).hexdigest()[:16]
```

### Audit Trail

```sql
CREATE TABLE audit_log (
    id UUID PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT NOW(),
    actor_id VARCHAR(255),  -- service/user who performed action
    action VARCHAR(50),  -- ingestion, extraction, validation, output
    resource_type VARCHAR(50),  -- entity_type
    resource_id UUID,
    details JSONB,
    source_ip INET,
    status VARCHAR(20),  -- success, failure
    error_message TEXT,
    UNIQUE(timestamp, actor_id, resource_id)
);

-- Example: Track every extraction with confidence score
INSERT INTO audit_log (actor_id, action, resource_type, resource_id, details)
VALUES (
    'extraction-service',
    'entity_extraction',
    'condition',
    entity_id,
    jsonb_build_object(
        'confidence', 0.95,
        'model_version', 'biobert_v1.2',
        'extraction_time_ms', 150
    )
);
```

---

## Conclusion

This architecture prioritizes:
1. **Scalability**: Horizontal scaling via Kubernetes, parallel processing
2. **Accuracy**: Confidence scoring, validation rules, human review loop
3. **Compliance**: Encryption at rest/in-transit, audit trails, de-identification
4. **Observability**: Comprehensive metrics, alerting, logging

The modular design enables independent scaling of each layer (ingestion, processing, validation, output) based on bottleneck analysis.
