# Commure: System Architecture
## Detailed Technical Design

**Version**: 1.0  
**Date**: 2026-09-26  
**Scope**: Clinical documentation automation platform architecture

---

## 1. Multi-Modal Input Processing

### Speech Recognition (ASR) Pipeline

```
Audio Input (patient + clinician)
  ↓
[Audio Streaming] (UDP chunks)
  ↓
[Pre-processing] (normalize, filter background noise)
  ↓
[ASR Model] (real-time speech-to-text)
  ├─ Medical Dictionary (50K terms)
  ├─ Speaker Separation (distinguish speakers)
  └─ Confidence Scoring
  ↓
[Post-processing] (punctuation, normalization)
  ↓
Transcribed Text
```

**ASR Engine Options**:
- **Nuance Dragon Medical**: Specialized for clinical documentation, ~98% accuracy
- **Google Cloud Speech-to-Text**: General purpose, medical model available, ~95% accuracy
- **Azure Speech Services**: Enterprise-grade, ~96% accuracy
- **Custom In-house**: Fine-tuned on 100K+ clinical audio samples

**Performance**:
- Real-time latency: <2 seconds
- Throughput: 1,000+ concurrent audio streams
- Medical accuracy: 96%+ with medical dictionary
- Fallback: Manual correction interface for misheard sections

### Structured Input Processing

```python
# Web/Mobile form submission
encounter_data = {
    "visit_type": "follow_up",  # Dropdown
    "chief_complaint": "HTN check",  # Structured
    "vital_signs": {
        "bp": "128/78",  # Auto-validated ranges
        "hr": "72",
        "temp": "98.6"
    },
    "problems": ["I10", "E11"],  # ICD-10 codes (EHR context)
    "exam_findings": {
        "heart": "Regular rate and rhythm",  # Text field
        "lungs": "Clear to auscultation"
    }
}

# Validation & normalization
validated = validate_and_normalize(encounter_data)
```

---

## 2. Clinical Language Engine

### NLP Pipeline (PubMedBERT)

```
Unified Input Text
  ↓
[Tokenization] (medical-aware splitting)
  ↓
[PubMedBERT Embeddings]
  ↓
[Entity Recognition]
  ├─ Diagnoses (ICD-10)
  ├─ Procedures (CPT)
  ├─ Medications (RxNorm)
  ├─ Findings
  └─ Temporal Info
  ↓
[Relation Extraction]
  ├─ Med→Diagnosis (treats, for)
  ├─ Finding→Diagnosis (indicates)
  ├─ Lab→Diagnosis (abnormal for)
  └─ Procedure→Indication
  ↓
[Temporal Analysis]
  ├─ Onset dates
  ├─ Duration
  └─ Trends
  ↓
Structured Clinical Understanding
```

**Entity Recognition Examples**:
```
Input: "Patient with hypertension on lisinopril, complaining of chest pain"

Extracted Entities:
- Diagnosis: "hypertension" → ICD-10: I10
- Medication: "lisinopril" → RxNorm: 11091 (lisinopril 10mg)
- Finding: "chest pain" → ICD-10: R07.9
- Relation: lisinopril --treats--> hypertension
- Relation: chest pain --new_finding_for--> hypertension patient
```

**Model Configuration**:
- Base: PubMedBERT (pre-trained on 14M PubMed abstracts)
- Fine-tuning: 100K+ annotated clinical notes per specialty
- Entity types: 20+ types (diagnoses, medications, procedures, lab values, findings)
- Relation types: 15+ types (treats, contraindicated, indicates, abnormal for, etc.)

---

## 3. Documentation Generation

### Template-Based Generation

```python
class DocumentationGenerator:
    def generate_note(self, clinical_data: ClinicalModel, template: Template):
        """Generate complete clinical note"""
        
        note = Note()
        
        # 1. HPI (History of Present Illness)
        note.hpi = self.generate_hpi(clinical_data)
        
        # 2. ROS (Review of Systems)
        note.ros = template.populate_ros(clinical_data.findings)
        
        # 3. PMH/PSH (from EHR)
        note.pmh = self.fetch_pmh(clinical_data.patient_id)
        note.psh = self.fetch_psh(clinical_data.patient_id)
        
        # 4. Medications
        note.medications = self.generate_med_section(clinical_data)
        
        # 5. Allergies
        note.allergies = self.fetch_allergies(clinical_data.patient_id)
        
        # 6. Exam
        note.physical_exam = self.generate_exam(clinical_data)
        
        # 7. Assessment
        note.assessment = self.generate_assessment(clinical_data)
        
        # 8. Plan
        note.plan = self.generate_plan(clinical_data, note.assessment)
        
        return note
```

### HPI Generation (Example)

```python
def generate_hpi(self, data: ClinicalModel) -> str:
    """Generate History of Present Illness section"""
    
    hpi = f"The {data.patient.age}-year-old {data.patient.gender} "
    hpi += f"with {', '.join(data.active_problems)} "
    hpi += f"presents with {data.chief_complaint}."
    
    # Add temporal info
    if data.symptom_duration:
        hpi += f" The {data.chief_complaint} started {data.symptom_duration} ago."
    
    # Add descriptive findings
    if data.exam_findings:
        hpi += f" On exam, the {data.chief_finding}."
    
    # Add recent labs/tests
    if data.recent_labs:
        hpi += f" Recent {data.recent_labs[0].test_name}: {data.recent_labs[0].value}."
    
    return hpi
```

### Assessment Generation (Example)

```python
def generate_assessment(self, data: ClinicalModel) -> str:
    """Generate Assessment section"""
    
    assessment = []
    
    # Primary diagnosis
    primary_dx = self.select_primary_diagnosis(data)
    assessment.append(f"1. {primary_dx.description}")
    
    # Associated diagnoses
    for dx in data.supporting_diagnoses:
        assessment.append(f"• {dx.description}")
    
    # Clinical reasoning
    assessment.append(f"\nClinical reasoning: {self.generate_clinical_reasoning(data)}")
    
    return "\n".join(assessment)
```

---

## 4. Compliance & Validation Layer

### Medical Necessity Checking

```python
def check_medical_necessity(note: Note, patient: Patient) -> ComplianceResult:
    """Verify note demonstrates medical necessity for billed level"""
    
    # Count Documentation Elements
    elements = count_documentation_elements(note)
    # E.g., HPI, ROS, Exam, Assessment, Plan
    
    # Check Diagnosis Support
    for diagnosis in note.diagnoses:
        if not has_supporting_findings(note, diagnosis):
            return ComplianceResult(
                valid=False,
                reason=f"Diagnosis {diagnosis} not supported by documented findings"
            )
    
    # Check Medication Appropriateness
    for medication in note.medications:
        if not is_appropriate_for_diagnosis(medication, note.diagnoses):
            return ComplianceResult(
                valid=False,
                reason=f"Medication {medication} not appropriate for documented diagnoses"
            )
    
    return ComplianceResult(valid=True)
```

### ICD-10 Bundling & Optimization

```python
def optimize_icd10_codes(diagnoses: List[str]) -> List[Tuple[str, str]]:
    """Suggest optimal ICD-10 codes for billing"""
    
    optimized = []
    
    for diagnosis in diagnoses:
        # Look up specific codes
        codes = icd10_lookup(diagnosis)
        
        # Filter out non-billable combinations
        codes = filter_unbundleable_codes(codes, diagnoses)
        
        # Select highest-severity appropriate code
        best_code = select_highest_severity(codes)
        
        optimized.append((diagnosis, best_code))
    
    return optimized
```

---

## 5. Physician Review Interface

### Quick Review UI

```python
# Note display with approval interface
class PhysicianReviewUI:
    def render(self, note: Note, encounter_data: Dict):
        """Render quick-review interface"""
        
        return {
            "left_pane": {
                "encounter_data": encounter_data,  # Input data
                "vital_signs": encounter_data.vitals,
                "chief_complaint": encounter_data.chief_complaint
            },
            "center_pane": {
                "generated_note": note.formatted(),
                "highlighted_differences": highlight_auto_generated(note, encounter_data)
            },
            "right_pane": {
                "actions": [
                    {"label": "Approve", "action": "submit"},
                    {"label": "Approve & Next", "action": "submit_next"},
                    {"label": "Edit", "action": "enter_edit_mode"},
                    {"label": "Regenerate", "action": "regenerate"},
                    {"label": "Reject", "action": "reject"}
                ],
                "compliance_status": compliance_check_result(note)
            }
        }
```

**Target**: 90%+ one-click approvals (zero edits)

---

## 6. EHR Integration

### HL7 CDA Submission

```python
def submit_to_ehr(note: Note, ehr_system: str) -> SubmissionResult:
    """Submit approved note to EHR"""
    
    # Convert to EHR-specific format
    if ehr_system == "epic":
        hl7_doc = convert_to_epic_cda(note)
    elif ehr_system == "cerner":
        hl7_doc = convert_to_cerner_cda(note)
    else:
        hl7_doc = convert_to_fhir_bundle(note)
    
    # Submit via API
    result = ehr_api.submit_document(hl7_doc)
    
    # Audit log
    audit_log.record({
        "event": "note_submitted_to_ehr",
        "note_id": note.id,
        "ehr_system": ehr_system,
        "timestamp": datetime.now(),
        "physician_id": note.approved_by,
        "status": result.status
    })
    
    return result
```

---

## 7. Database Schema

```sql
CREATE TABLE encounters (
    id UUID PRIMARY KEY,
    patient_id VARCHAR(255),
    clinician_id VARCHAR(255),
    encounter_datetime TIMESTAMP,
    visit_type VARCHAR(50),
    specialty VARCHAR(50),
    chief_complaint TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE clinical_notes (
    id UUID PRIMARY KEY,
    encounter_id UUID REFERENCES encounters(id),
    generated_note TEXT,  -- Full note content
    note_status VARCHAR(20),  -- generated, reviewed, approved, submitted
    accuracy_score DECIMAL(3,2),  -- 0.0-1.0
    compliance_score DECIMAL(3,2),
    physician_edits INT,
    submission_status VARCHAR(20),  -- pending, submitted, confirmed, failed
    submitted_to_ehr_timestamp TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    INDEX idx_encounter_status (encounter_id, note_status)
);

CREATE TABLE audit_log (
    id UUID PRIMARY KEY,
    event_type VARCHAR(50),  -- note_generated, note_approved, note_submitted
    actor_id VARCHAR(255),
    actor_type VARCHAR(20),  -- system, physician
    encounter_id UUID,
    changes JSONB,  -- What changed
    timestamp TIMESTAMP DEFAULT NOW(),
    INDEX idx_encounter_time (encounter_id, timestamp DESC)
);
```

---

## 8. Monitoring & Observability

### Key Metrics

```python
# Quality metrics
note_accuracy = Gauge('commure_note_accuracy_percent')
physician_edit_rate = Gauge('commure_physician_edit_rate')
one_click_approval_rate = Gauge('commure_one_click_approval_rate')

# Throughput
encounters_per_minute = Gauge('commure_encounters_per_minute')
notes_generated_total = Counter('commure_notes_generated_total')
notes_approved_total = Counter('commure_notes_approved_total')

# Latency
note_generation_latency = Histogram(
    'commure_note_generation_seconds',
    buckets=[0.5, 1, 2, 5, 10, 30]
)

# Infrastructure
asr_latency = Histogram('commure_asr_latency_seconds')
nlp_latency = Histogram('commure_nlp_latency_seconds')
generation_latency = Histogram('commure_generation_latency_seconds')
```

---

## 9. Security & Compliance

```python
# Encryption at rest
class DocumentEncryption:
    def encrypt_note(self, note: Note, kms_key_id: str) -> bytes:
        """Encrypt with KMS"""
        return kms_encrypt(note.serialize(), kms_key_id)
    
    def decrypt_note(self, encrypted: bytes) -> Note:
        """Decrypt from KMS"""
        plaintext = kms_decrypt(encrypted)
        return Note.deserialize(plaintext)

# Audit trail
def log_audit_event(event_type: str, actor_id: str, 
                   encounter_id: str, details: Dict):
    """Log all access & actions for HIPAA compliance"""
    audit_log.insert({
        "event_type": event_type,
        "actor_id": actor_id,
        "encounter_id": encounter_id,
        "timestamp": datetime.now(),
        "details": details,
        "ip_address": get_request_ip()
    })
```

---

## 10. Deployment Architecture

### Kubernetes Configuration

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: commure-api
spec:
  replicas: 20  # Auto-scale
  template:
    spec:
      containers:
      - name: api
        image: commure/api:v1.0
        resources:
          requests:
            cpu: 2000m
            memory: 4Gi
          limits:
            cpu: 4000m
            memory: 8Gi
      - name: asr-worker
        image: commure/asr-worker:v1.0
        resources:
          requests:
            gpu: 1  # GPU for ASR
            memory: 8Gi
```

---

## Conclusion

This architecture delivers:
1. **Real-time Processing**: Sub-500ms latency end-to-end
2. **Clinical Intelligence**: PubMedBERT understands medical context
3. **Enterprise Compliance**: Audit-ready, encryption, HIPAA
4. **High Accuracy**: 90%+ automation rate (minimal physician edits)
5. **Scalability**: 1M+ encounters/day on Kubernetes
