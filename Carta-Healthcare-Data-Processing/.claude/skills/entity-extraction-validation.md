# Entity Extraction Validation Skill
## Carta Healthcare - Clinical Data Extraction Quality

**Trigger**: `/entity-validate` or `entity extraction` in Carta context  
**Type**: Data extraction quality assurance  

---

## What This Skill Does

Validates extracted clinical entities from patient records:
- **Accuracy**: Extracted entities match source documents
- **Completeness**: No critical findings missed
- **Normalization**: Proper ICD-10, RxNorm, LOINC codes
- **Relationships**: Clinical logic between entities
- **Confidence**: Confidence scores appropriate

---

## Carta Healthcare Focus

- **Problem**: 10M+ clinical records unstructured, hard to use
- **Solution**: NLP extraction + structured output
- **Metric**: 66% faster processing (4 hours → 90 minutes per 10K records)
- **Quality Gate**: 99% extraction accuracy

---

## How to Use

```bash
/entity-validate source_document.txt --entity-types condition,medication,lab
```

---

## Validates Against

- ICD-10 diagnosis codes
- RxNorm medication codes
- LOINC lab codes
- CPT procedures
- FHIR data model
