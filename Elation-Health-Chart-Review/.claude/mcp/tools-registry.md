# Elation Health - MCP Tools Registry
## Sub-Agent Tools & External Plugin Integration

**Version**: 1.0  
**Purpose**: Define all tools available to sub-agents and external plugins  
**Last Updated**: 2026-09-26

---

## 📋 Table of Contents
1. Clinical Context Tools
2. Patient Data Tools
3. Alert & Safety Tools
4. Documentation Tools
5. Analytics Tools
6. External Plugin Integration

---

## 1. Clinical Context Tools

### Tool: `get_clinical_context`
**Type**: Read-only  
**Purpose**: Retrieve rich clinical context for a patient  
**Sub-agents**: chart-intelligence-engine, compliance-officer  

```
Parameters:
  - patient_id: string (MRN)
  - include: array ["problems", "medications", "labs", "alerts", "history"]
  - time_window: string ("1w", "1m", "6m", "1y", "all")

Returns:
  {
    patient_id: string
    demographics: object
    active_problems: array[Diagnosis]
    medications: array[Medication]
    recent_labs: array[Lab]
    alerts: array[Alert]
    timeline: array[Event]
  }

Example:
  get_clinical_context("P001234", include=["problems", "medications", "labs"], time_window="6m")
```

### Tool: `get_condition_profile`
**Type**: Reference  
**Purpose**: Get clinical profile for a diagnosis  
**Sub-agents**: chart-intelligence-engine, clinical-validator  

```
Parameters:
  - icd10_code: string (e.g., "I10")
  - include: array ["pathophysiology", "complications", "management", "red_flags"]

Returns:
  {
    icd10: string
    condition_name: string
    description: string
    typical_progression: string
    common_complications: array[string]
    management_approaches: array[string]
    red_flags: array[string]
    evidence_base: string
  }

Example:
  get_condition_profile("E11.9", include=["complications", "red_flags"])
```

### Tool: `get_drug_interaction_context`
**Type**: Safety  
**Purpose**: Check medication interactions with clinical context  
**Sub-agents**: safety-validator, chart-intelligence-engine  

```
Parameters:
  - medications: array[string] (drug names)
  - patient_factors: object {age, kidney_function, liver_function, allergies}
  - severity_threshold: string ("critical", "major", "moderate", "minor")

Returns:
  {
    total_interactions: int
    critical_interactions: array[Interaction]
    major_interactions: array[Interaction]
    minor_interactions: array[Interaction]
    patient_specific_risks: array[string]
    recommendations: array[string]
  }

Example:
  get_drug_interaction_context(
    medications=["Lisinopril", "Atorvastatin"],
    patient_factors={age: 72, kidney_function: "mild decline"},
    severity_threshold="major"
  )
```

### Tool: `get_preventive_care_status`
**Type**: Screening  
**Purpose**: Get overdue preventive care screening status  
**Sub-agents**: compliance-officer, quality-validator  

```
Parameters:
  - patient_id: string
  - age: int
  - gender: string ("M" | "F")
  - conditions: array[string] (ICD-10 codes)
  - last_screening: object {test_name: date}

Returns:
  {
    patient_id: string
    overdue_screenings: array[Screening]
    upcoming_screenings: array[Screening]
    recommendations: array[string]
    evidence_based_guidelines: array[string]
  }

Example:
  get_preventive_care_status(
    patient_id="P001234",
    age=67,
    gender="M",
    conditions=["I10", "E11.9"],
    last_screening={mammography: null, colonoscopy: "2024-02-15"}
  )
```

---

## 2. Patient Data Tools

### Tool: `search_patient_records`
**Type**: Query  
**Purpose**: Full-text search across patient records  
**Sub-agents**: chart-intelligence-engine, research-agent  

```
Parameters:
  - query: string (e.g., "chest pain", "medication side effect")
  - patient_id: string (optional, if searching one patient)
  - search_fields: array (["notes", "labs", "diagnoses", "medications"])
  - date_range: object {start: date, end: date}

Returns:
  {
    matches: int
    results: array[Match]
    relevance_scores: array[float]
    clinical_context: string
  }

Example:
  search_patient_records(
    query="A1c trending up",
    patient_id="P001234",
    search_fields=["labs", "notes"],
    date_range={start: "2026-03-01", end: "2026-09-26"}
  )
```

### Tool: `get_patient_summary`
**Type**: Summarization  
**Purpose**: Get AI-generated patient summary (30-second view)  
**Sub-agents**: chart-intelligence-engine, documentation-assistant  

```
Parameters:
  - patient_id: string
  - summary_type: string ("quick_view", "detailed", "visit_prep", "handoff")
  - clinical_focus: array (["problems", "medications", "alerts", "recent_changes"])

Returns:
  {
    summary_text: string
    key_points: array[string]
    alerts: array[Alert]
    action_items: array[string]
    generated_at: datetime
  }

Example:
  get_patient_summary(
    patient_id="P001234",
    summary_type="quick_view",
    clinical_focus=["problems", "alerts", "recent_changes"]
  )
```

### Tool: `get_lab_trend_analysis`
**Type**: Analytics  
**Purpose**: Analyze lab value trends over time  
**Sub-agents**: analytics-engine, quality-validator  

```
Parameters:
  - patient_id: string
  - test_code: string (e.g., "A1c", "creatinine")
  - time_window: string ("1m", "3m", "6m", "1y")
  - include_interpretation: bool

Returns:
  {
    test_name: string
    values: array[{date: date, value: float, reference_range: string}]
    trend: string ("improving", "worsening", "stable")
    trajectory: string (linear description)
    interpretation: string (clinical meaning)
    recommendations: array[string]
  }

Example:
  get_lab_trend_analysis(
    patient_id="P001234",
    test_code="A1c",
    time_window="6m",
    include_interpretation=true
  )
```

---

## 3. Alert & Safety Tools

### Tool: `check_safety_alerts`
**Type**: Safety  
**Purpose**: Get all active safety alerts for a patient  
**Sub-agents**: safety-validator, compliance-officer  

```
Parameters:
  - patient_id: string
  - alert_types: array (["medication", "allergy", "lab", "screening", "contraindication"])
  - severity: string ("critical", "high", "medium", "all")

Returns:
  {
    total_alerts: int
    critical_alerts: array[Alert]
    high_alerts: array[Alert]
    medium_alerts: array[Alert]
    requires_immediate_action: bool
  }

Example:
  check_safety_alerts(
    patient_id="P009012",
    alert_types=["medication", "allergy", "contraindication"],
    severity="critical"
  )
```

### Tool: `create_clinical_alert`
**Type**: Write  
**Purpose**: Flag a clinical concern for review  
**Sub-agents**: safety-validator, compliance-officer  

```
Parameters:
  - patient_id: string
  - alert_type: string (enum)
  - severity: string ("critical", "high", "medium", "low")
  - clinical_reason: string
  - recommended_action: string
  - escalate_to: array[string] (roles: ["prescriber", "pharmacist", "compliance"])

Returns:
  {
    alert_id: string
    created_at: datetime
    status: "created"
  }

Example:
  create_clinical_alert(
    patient_id="P009012",
    alert_type="medication_contraindication",
    severity="critical",
    clinical_reason="Patient on Lisinopril (ACE inhibitor) but has documented angioedema allergy",
    recommended_action="Review immediately, consider alternative antihypertensive",
    escalate_to=["prescriber", "pharmacist"]
  )
```

---

## 4. Documentation Tools

### Tool: `generate_documentation_template`
**Type**: Assistance  
**Purpose**: Generate smart template for clinical documentation  
**Sub-agents**: documentation-assistant  

```
Parameters:
  - visit_type: string ("follow-up", "acute", "preventive", "chronic_disease")
  - patient_id: string
  - chief_complaint: string (optional)
  - include_sections: array (["HPI", "ROS", "PMH", "Assessment", "Plan"])

Returns:
  {
    template: string (pre-filled with patient context)
    suggested_sections: array[string]
    clinical_context: object
    documentation_tips: array[string]
  }

Example:
  generate_documentation_template(
    visit_type="chronic_disease",
    patient_id="P001234",
    include_sections=["HPI", "Assessment", "Plan"]
  )
```

### Tool: `validate_documentation`
**Type**: Quality  
**Purpose**: Validate clinical documentation completeness and accuracy  
**Sub-agents**: quality-validator, compliance-officer  

```
Parameters:
  - documentation: string (full note text)
  - required_fields: array (["diagnoses", "medications", "assessment", "plan"])
  - clinical_context: object

Returns:
  {
    is_complete: bool
    missing_fields: array[string]
    issues_found: array[Issue]
    compliance_score: float
    recommendations: array[string]
  }

Example:
  validate_documentation(
    documentation="Patient presents with...",
    required_fields=["diagnoses", "assessment", "plan"],
    clinical_context={patient_id: "P001234"}
  )
```

---

## 5. Analytics Tools

### Tool: `get_quality_metrics`
**Type**: Analytics  
**Purpose**: Get performance metrics on summaries and documentation  
**Sub-agents**: analytics-engine, quality-validator  

```
Parameters:
  - metric_type: string ("accuracy", "completeness", "timeliness", "adoption")
  - time_window: string ("1w", "1m", "3m")
  - filter_by: object (optional)

Returns:
  {
    metric_name: string
    value: float
    target: float
    trend: string
    benchmark: float
  }

Example:
  get_quality_metrics(
    metric_type="accuracy",
    time_window="1m"
  )
```

### Tool: `analyze_alert_patterns`
**Type**: Analytics  
**Purpose**: Analyze patterns in clinical alerts  
**Sub-agents**: analytics-engine, research-agent  

```
Parameters:
  - time_window: string ("1w", "1m", "3m")
  - alert_types: array
  - group_by: string ("alert_type", "severity", "condition")

Returns:
  {
    total_alerts: int
    pattern_analysis: object
    trending_issues: array[Issue]
    recommendations: array[string]
  }

Example:
  analyze_alert_patterns(
    time_window="1m",
    alert_types=["medication", "lab"],
    group_by="alert_type"
  )
```

---

## 6. External Plugin Integration

### Available Official Claude Plugins

#### Plugin: `@claude/web-search`
**Purpose**: Search web for clinical guidelines, drug info, latest research  
**Use Cases**:
- Look up latest clinical guidelines
- Check FDA drug approvals
- Search for clinical trial information
- Verify dosing recommendations

```
Usage: search_web("latest hypertension guidelines 2026")
Returns: Web search results with sources
```

#### Plugin: `@claude/knowledge-base`
**Purpose**: Access to medical knowledge bases  
**Use Cases**:
- ICD-10 code validation
- Drug interaction checking
- Clinical guideline references
- Diagnosis reference material

```
Usage: lookup_knowledge("ICD-10", "E11.9")
Returns: Structured knowledge base entry
```

#### Plugin: `@claude/calendar`
**Purpose**: Manage appointment scheduling and reminders  
**Use Cases**:
- Schedule follow-up visits
- Track appointment adherence
- Set preventive care reminders
- Coordinate care team meetings

```
Usage: schedule_appointment(patient_id, visit_type, provider)
Returns: Appointment confirmation
```

#### Plugin: `@claude/email`
**Purpose**: Send clinical alerts and notifications  
**Use Cases**:
- Alert prescriber of drug interactions
- Notify patients of overdue screenings
- Send clinical summaries for handoff
- Escalate critical alerts

```
Usage: send_alert(recipient, alert_content, priority)
Returns: Delivery confirmation
```

---

## Sub-Agent Specializations

### 1. `chart-intelligence-engine` Agent
**Capabilities**:
- Summarization & context extraction
- Alert detection & prioritization
- Clinical insight generation

**Tools Access**:
- `get_clinical_context`
- `get_condition_profile`
- `search_patient_records`
- `get_patient_summary`
- `get_lab_trend_analysis`

### 2. `compliance-officer` Agent
**Capabilities**:
- Documentation validation
- Safety alert management
- Quality metrics tracking

**Tools Access**:
- `check_safety_alerts`
- `create_clinical_alert`
- `validate_documentation`
- `get_quality_metrics`
- `get_preventive_care_status`

### 3. `safety-validator` Agent
**Capabilities**:
- Drug interaction analysis
- Allergy cross-checking
- Contraindication detection

**Tools Access**:
- `get_drug_interaction_context`
- `check_safety_alerts`
- `create_clinical_alert`

### 4. `documentation-assistant` Agent
**Capabilities**:
- Template generation
- Auto-complete suggestions
- Quality validation

**Tools Access**:
- `generate_documentation_template`
- `validate_documentation`
- `get_patient_summary`

### 5. `analytics-engine` Agent
**Capabilities**:
- Performance metrics
- Pattern analysis
- Trend identification

**Tools Access**:
- `get_quality_metrics`
- `analyze_alert_patterns`
- `get_lab_trend_analysis`

---

## Tool Security & Permissions

### Read-Only Tools (Safe for any sub-agent)
- `get_clinical_context`
- `get_condition_profile`
- `search_patient_records`
- `get_patient_summary`
- `get_lab_trend_analysis`
- `check_safety_alerts`
- `get_quality_metrics`

### Write Tools (Require explicit permission)
- `create_clinical_alert` - Requires compliance approval
- `validate_documentation` - Audit logging required
- `generate_documentation_template` - Context-aware only

### External Plugin Tools (Require user approval)
- `@claude/email` - Manual review required for clinical alerts
- `@claude/calendar` - Appointment coordination approval
- `@claude/web-search` - Search results review required

---

## Implementation Status

| Tool | Status | Sub-agents | Plugins |
|------|--------|-----------|---------|
| get_clinical_context | ✅ Implemented | chart-intel, safety-val | - |
| get_condition_profile | ✅ Implemented | chart-intel, documentation | - |
| get_drug_interaction_context | 🔄 Building | safety-val | knowledge-base |
| search_patient_records | 🔄 Building | chart-intel, research | web-search |
| check_safety_alerts | ✅ Implemented | compliance, safety-val | - |
| generate_documentation_template | 🔄 Building | documentation | - |
| get_lab_trend_analysis | ✅ Implemented | analytics, quality | - |
| validate_documentation | 🔄 Building | compliance, quality | knowledge-base |
| analyze_alert_patterns | 🔄 Building | analytics, research | - |

---

## Next Steps

1. ✅ Define tool interfaces (this document)
2. 🔄 Implement tools in backend
3. 🔄 Integrate external plugins
4. ✅ Configure sub-agents
5. 🔄 Build RAG engine for knowledge retrieval
6. 🔄 Set up audit logging
7. 🔄 Deploy to production
