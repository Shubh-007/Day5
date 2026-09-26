# Clinical Review Skill
## Healthcare Documentation Quality Assurance

**Trigger**: `/clinical-review` or `clinical-review` in prompt  
**Type**: Specialized review agent  
**Use Case**: Review clinical documentation for accuracy, compliance, and safety  

---

## What This Skill Does

Reviews clinical documentation (from any of the 5 healthcare platforms) for:
- **Clinical Accuracy**: Medical terminology, diagnosis/treatment appropriateness
- **Compliance**: HIPAA, billing codes (ICD-10, CPT), medical necessity
- **Safety**: Missing critical findings, drug interactions, temporal inconsistencies
- **Documentation Quality**: Completeness, clarity, evidence of clinical reasoning
- **EHR Integration**: Proper code mappings, required fields, format compliance

---

## How to Use

```
/clinical-review <document_path> [--specialty <specialty>] [--strictness high|medium|low]
```

**Examples**:
```
/clinical-review /home/labuser/Day5/Commure-Documentation-Automation/plan.md --specialty primary-care

/clinical-review clinical_note.txt --strictness high

/clinical-review sample_documentation.md --specialty cardiology
```

---

## Output

Returns structured review with:
1. **Overall Assessment**: ✅/⚠️/❌ + confidence score
2. **Clinical Issues**: List of accuracy/safety concerns with severity
3. **Compliance Issues**: Billing, HIPAA, documentation gaps
4. **Suggestions**: Specific improvements with examples
5. **Recommendations**: Priority fixes before deployment

---

## Specialties Supported

- Primary Care
- Cardiology
- Orthopedics
- Psychiatry
- Pediatrics
- Emergency Medicine
- Specialty-agnostic (default)

---

## Integration

Used by:
- **Commure**: Validate generated notes before physician review
- **Elation**: Review chart summaries for accuracy
- **Banner**: Validate AI-drafted documentation
- **Qualified**: Screen patient cohort documentation
- **Carta**: Validate extracted clinical data

---

## Configuration

Available in: `.claude/settings.json`
```json
{
  "clinical-review": {
    "specialty": "primary-care",
    "compliance-strictness": "high",
    "include-billing-checks": true,
    "hipaa-compliance-level": "strict"
  }
}
```

---

## Team Permissions

- **Clinical Lead**: Full access
- **Data Scientist**: Read results, suggest improvements
- **Compliance Officer**: Can trigger compliance-only review
- **Developers**: Can trigger on documentation changes
