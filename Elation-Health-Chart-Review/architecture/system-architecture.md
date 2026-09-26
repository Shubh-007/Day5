# Elation Health: System Architecture
## Detailed Technical Design

**Version**: 1.0  
**Date**: 2026-09-26  
**Scope**: Chart review & documentation platform architecture

---

## 1. EHR Integration Architecture

### SMART-on-FHIR Gateway

```python
class EHRConnector(ABC):
    @abstractmethod
    def authenticate(self, credentials: EHRCredentials) -> Token:
        """OAuth2 authentication flow"""
        pass
    
    @abstractmethod
    def fetch_patient(self, patient_id: str) -> PatientBundle:
        """Fetch complete patient record (demographics + resources)"""
        pass
    
    @abstractmethod
    def subscribe_updates(self, patient_id: str) -> Stream:
        """Subscribe to real-time updates (HL7 ADT or webhooks)"""
        pass
```

### Supported EHRs

| EHR | Protocol | Real-time? | API Rate Limit | Latency Target |
|-----|----------|-----------|-----------------|-----------------|
| **Epic** | SMART-on-FHIR + HL7v2 | Yes (ADT feed) | 500 req/min | <5 sec |
| **Cerner** | FHIR R4 + proprietary | Yes (webhook) | 1000 req/min | <5 sec |
| **Meditech** | HL7v2 + REST | Polling only | Limited | <30 sec |
| **Athena** | REST API | Polling | 300 req/min | <1 min |

### Data Caching Strategy

```python
# Redis-backed cache with TTL
patient_cache = {
    f"patient:{patient_id}": {
        "demographics": {...},
        "problems": [...],
        "medications": [...],
        "labs": [...],
        "notes": [...],
        "last_updated": timestamp,
        "ttl": 3600  # 1 hour
    }
}

# Invalidation strategy:
# - HL7 ADT (real-time): Update immediately
# - Webhook events: Update immediately
# - Polling fallback: Refresh every 5 minutes
```

---

## 2. Clinical NLP Pipeline

### BioClinicalBERT Integration

```
Raw Clinical Text
  ↓
[Tokenizer (BioSentenceTokenizer)]
  ↓
[BioClinicalBERT Embeddings]
  ↓
[Entity Recognition Head]
  ├─ Diagnoses (ICD-10 codes)
  ├─ Medications (RxNorm codes)
  ├─ Labs (LOINC codes)
  └─ Procedures (CPT codes)
  ↓
[Relation Extraction Head]
  ├─ medication --treats--> diagnosis
  ├─ lab --abnormal_for--> diagnosis
  └─ procedure --indication--> diagnosis
  ↓
[Temporal Analysis]
  ├─ Onset dates
  ├─ Resolution dates
  └─ Relationships between events
  ↓
Structured Clinical Model
```

### Model Configuration

```json
{
  "base_model": "emilyalsentzer/biomedical_bert_base_uncased",
  "fine_tune_data": "10K labeled EHR notes",
  "entity_types": {
    "B-PROBLEM": "Problem (diagnosis)",
    "B-MEDICATION": "Medication",
    "B-LAB": "Laboratory result",
    "B-PROCEDURE": "Procedure",
    "B-ALLERGY": "Allergy reaction"
  },
  "relation_types": {
    "treats": "medication treats condition",
    "contraindicated": "medication contraindicated in condition",
    "abnormal_for": "lab abnormal relative to condition",
    "precedes": "event A precedes event B temporally"
  }
}
```

### Performance Optimization

- **Batch Processing**: Inference on 32 notes simultaneously
- **Model Quantization**: INT8 quantization (-30% latency, -5% accuracy)
- **GPU Caching**: Keep model in GPU memory across requests
- **Attention Pattern Caching**: Cache attention outputs for repeated text patterns

**Latency Targets**:
- Single note: <500ms (with GPU)
- Batch of 32: <15 sec (real-time acceptable)

---

## 3. Summarization Engine

### Algorithm: Extractive + Abstractive Summarization

```python
def generate_clinical_summary(patient_chart: Chart) -> Summary:
    """Generate concise clinical summary"""
    
    # Step 1: Extract clinical entities
    entities = extract_entities(patient_chart.notes)
    
    # Step 2: Link to structured data (from EHR)
    problems = merge_with_problem_list(entities)
    medications = merge_with_med_list(entities)
    labs = fetch_recent_labs(patient_chart)
    
    # Step 3: Identify recent changes
    changes = detect_changes_since(
        patient_chart, 
        time_window=timedelta(days=30)
    )
    
    # Step 4: Generate summaries (per section)
    summary = Summary()
    summary.problems = summarize_problems(problems, limit=150_words)
    summary.medications = summarize_medications(medications, limit=100_words)
    summary.labs = summarize_labs(labs, recent_only=True, limit=100_words)
    summary.changes = format_changes(changes)
    summary.alerts = extract_clinical_alerts(patient_chart)
    
    return summary
```

### Abstractive Summarization (T5 Model)

For sections where conciseness is critical:

```
Input: Full medication list (20 items, 500 words)
T5 Model: "Summarize in <100 words"
Output: "On 3 antihypertensives (lisinopril, amlodipine, HCTZ - BP well-controlled), 
         metformin for diabetes (A1c 7.2), atorvastatin for cholesterol. 
         No interactions. Refill due: HCTZ, metformin this month."
```

---

## 4. Documentation Assistant

### Smart Template Selection

```python
def select_template(chief_complaint: str, 
                    visit_type: str,
                    patient_history: PatientChart) -> Template:
    """Select most appropriate note template"""
    
    # Classify visit type using intent detection
    visit_type = classify_visit(chief_complaint)
    # Returns: "acute_illness", "follow_up_chronic", "preventive", "post_op"
    
    # Load template matching visit type
    if visit_type == "acute_illness":
        template = get_template("acute_visit")
    elif visit_type == "follow_up_chronic":
        template = get_template("chronic_disease_followup")
        template = customize_for_conditions(template, patient_history.problems)
    else:
        template = get_template(visit_type)
    
    return template
```

### Auto-Complete Engine

```python
class AutoCompleteEngine:
    def predict_next_text(self, partial_text: str, context: Dict) -> str:
        """Predict next text segment based on context"""
        
        # Gather context
        current_note = partial_text
        patient_problems = context["problems"]
        visit_type = context["visit_type"]
        recent_labs = context["recent_labs"]
        
        # Generate candidates using fine-tuned GPT-2 (healthcare)
        candidates = model.generate(
            input_ids=tokenize(partial_text),
            context_tokens=encode_context(context),
            max_length=30,
            num_beams=3,
            top_p=0.9
        )
        
        # Rank by clinical plausibility
        ranked = rank_by_plausibility(candidates, context)
        
        # Return top suggestion (or top 3 for user selection)
        return ranked[0]
```

### Clinical Decision Support

```python
def provide_cds(note_section: str, section_type: str) -> List[Suggestion]:
    """Provide clinical decision support suggestions"""
    
    suggestions = []
    
    if section_type == "assessment":
        # ICD-10 suggestions based on assessment text
        conditions = extract_conditions(note_section)
        for cond in conditions:
            icd10_codes = lookup_icd10(cond)
            for code in icd10_codes[:3]:  # Top 3
                suggestions.append({
                    "type": "icd10",
                    "text": f"{code}: {code.description}",
                    "action": "click to add"
                })
    
    elif section_type == "plan":
        # Medication + dosing suggestions
        medications = extract_medications(note_section)
        for med in medications:
            suggestions.extend(generate_med_suggestions(med))
        
        # Interaction checking
        for med_pair in combinations(medications, 2):
            interaction = check_interaction(med_pair)
            if interaction.severity in ["moderate", "severe"]:
                suggestions.append({
                    "type": "interaction_alert",
                    "text": f"⚠️  {interaction.description}",
                    "severity": interaction.severity
                })
    
    return suggestions
```

---

## 5. Database Schema

### Core Tables

```sql
CREATE TABLE patients (
    id UUID PRIMARY KEY,
    ehr_patient_id VARCHAR(255),  -- External EHR ID
    ehr_system VARCHAR(50),  -- Epic, Cerner, etc.
    demographics JSONB,  -- Name, DOB, MRN, etc.
    last_sync TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(ehr_system, ehr_patient_id)
);

CREATE TABLE patient_summaries (
    id UUID PRIMARY KEY,
    patient_id UUID REFERENCES patients(id),
    summary_type VARCHAR(50),  -- 'visit_prep', 'complete'
    problems_summary TEXT,  -- ~150 words
    medications_summary TEXT,  -- ~100 words
    labs_summary TEXT,  -- ~100 words
    alerts JSONB,  -- Array of alert objects
    generated_at TIMESTAMP,
    generated_by VARCHAR(255),  -- AI model version
    cache_ttl INTERVAL DEFAULT '1 hour',
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_patient_generated (patient_id, generated_at DESC)
);

CREATE TABLE clinical_notes (
    id UUID PRIMARY KEY,
    patient_id UUID REFERENCES patients(id),
    note_type VARCHAR(50),  -- 'visit', 'progress', 'procedure'
    content TEXT,
    author_id VARCHAR(255),  -- Clinician ID
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    finalized_at TIMESTAMP,  -- When signed
    ai_suggestions JSONB,  -- What was suggested
    ai_accepted BOOLEAN,  -- Clinician accepted AI suggestions?
    audit_log JSONB,  -- Track edits
    INDEX idx_patient_finalized (patient_id, finalized_at DESC)
);

CREATE TABLE clinical_entities (
    id UUID PRIMARY KEY,
    note_id UUID REFERENCES clinical_notes(id),
    entity_type VARCHAR(50),  -- diagnosis, medication, lab, procedure
    entity_value VARCHAR(500),
    normalized_code VARCHAR(50),  -- ICD-10, RxNorm, LOINC
    confidence DECIMAL(3,2),
    extracted_by VARCHAR(255),  -- Model version
    created_at TIMESTAMP,
    INDEX idx_note_type (note_id, entity_type)
);
```

---

## 6. API Specification

### Core Endpoints

```
GET /api/v1/patients/{patient_id}/summary
  Response: {
    "problems": "HTN (well-controlled), DM2, HLD",
    "medications": "Lisinopril 10mg daily, metformin 1000mg BID...",
    "recent_changes": ["A1c up to 7.2", "New cardiology note"],
    "alerts": [{"severity": "warning", "text": "Overdue eye exam"}],
    "generated_at": "2026-09-26T10:30:00Z",
    "cache_age_seconds": 15
  }

POST /api/v1/notes/{note_id}/ai_suggestions
  Request: {
    "partial_text": "Patient presents with chest pain...",
    "section_type": "hpi",
    "context": {"patient_id": "...", "visit_type": "acute"}
  }
  Response: {
    "suggestion": "...x 2 days, worse with exertion, improved with rest",
    "alternatives": ["...sharp, pleuritic", "...dull, constant"],
    "confidence": 0.87
  }

GET /api/v1/cds/icd10
  Params: {"condition": "hypertension", "limit": 5}
  Response: {
    "codes": [
      {"code": "I10", "description": "Essential HTN", "prevalence": "35%"},
      {"code": "I11", "description": "HTN with CKD", "prevalence": "8%"}
    ]
  }

POST /api/v1/interactions/check
  Request: {"medications": ["lisinopril", "ibuprofen"]}
  Response: {
    "interaction": "ACE inhibitor + NSAID may reduce renal function",
    "severity": "moderate",
    "recommendation": "Monitor kidney function, consider gastroprotection"
  }
```

---

## 7. Caching Strategy

### Multi-Layer Cache

```
Request for Patient Summary
  ↓
[L1: Redis - Patient cache (1 hour TTL)]
  ↓ (miss)
[L2: Database - Patient summary table]
  ↓ (miss)
[L3: EHR API - Fetch fresh data]
  ↓
Generate summary (NLP pipeline)
  ↓
Store in Redis + DB
  ↓
Return to client
```

**Cache Invalidation**:
- HL7 ADT message received → invalidate immediately
- EHR webhook → invalidate immediately
- Polling (5-min interval) → lazy invalidation
- Manual cache clear → admin function

---

## 8. Security & Compliance

### Data Protection

```python
# Encryption at rest (AES-256)
patient_data_encrypted = encrypt_with_kms(
    patient_data,
    kms_key_id="arn:aws:kms:us-east-1:account:key/12345"
)

# Encryption in transit (TLS 1.3)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["chart.elation.health"])

# PII masking in logs
def mask_pii(text: str) -> str:
    """Remove identifiable information before logging"""
    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]', text)  # SSN
    text = re.sub(r'\b\d{5}(?:-\d{4})?\b', '[ZIP]', text)  # Zip code
    return text
```

### Audit Logging

```json
{
  "timestamp": "2026-09-26T10:30:45.123Z",
  "event": "patient_summary_viewed",
  "actor": "clinician_12345",
  "patient_id": "pseudonym_xyz",
  "action": "view",
  "data_accessed": ["problems", "medications", "recent_labs"],
  "ip_address": "203.0.113.5",
  "outcome": "success"
}
```

---

## 9. Monitoring & Observability

### Key Metrics

```python
# Latency
summary_generation_latency = Histogram(
    'elation_summary_generation_seconds',
    buckets=[0.1, 0.5, 1, 2, 5, 10]
)

# Cache hit rate
cache_hit_rate = Gauge(
    'elation_cache_hit_rate_percent',
    labels=['cache_layer']  # redis, db, api
)

# Clinical accuracy
ai_suggestion_acceptance_rate = Gauge(
    'elation_ai_suggestion_acceptance_rate'
)

# Infrastructure
concurrent_active_users = Gauge(
    'elation_concurrent_active_users'
)
```

---

## 10. Deployment Architecture

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: elation-api
spec:
  replicas: 10  # Auto-scale based on load
  template:
    spec:
      containers:
      - name: api
        image: elation/api:v1.0
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: 2000m
            memory: 2Gi
        env:
        - name: CACHE_REDIS_URL
          value: redis://elation-cache:6379
        - name: DB_CONNECTION_STRING
          valueFrom:
            secretKeyRef:
              name: elation-secrets
              key: db-connection
```

---

## Conclusion

This architecture prioritizes:
1. **Performance**: Sub-second summaries via multi-layer caching
2. **Clinical Safety**: Conservative AI suggestions, clinician always in control
3. **Compliance**: Encryption, audit logging, HIPAA-ready
4. **Scalability**: Kubernetes auto-scaling, stateless API design
5. **Reliability**: Multiple data sources (EHR API + webhooks + polling)
