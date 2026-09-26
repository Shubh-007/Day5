# Cohort Screening Validation Skill
## Qualified Health - Patient Identification Accuracy

**Trigger**: `/screen-validate` or `patient screening` in Qualified context  
**Type**: Patient cohort validation  

---

## What This Skill Does

Validates Qualified Health's patient screening engine:
- **Rule Accuracy**: Screening rules correctly identify patients
- **Clinical Appropriateness**: Identified cohorts match clinical criteria
- **Completeness**: No eligible patients missed
- **False Positive Rate**: Minimizes unnecessary alerts
- **Precision**: High positive predictive value

---

## Qualified Health Focus

- **Problem**: Identifying patients for life-saving interventions from fragmented records
- **Solution**: Rules engine + patient matching + screening
- **Metric**: 90%+ rule accuracy, <500ms patient lookup
- **Quality Gate**: >90% precision, <5% false positive rate

---

## How to Use

```bash
/screen-validate screening_cohort.json --indication heart-failure --target-accuracy 90
```

---

## Validates

- Rule logic correctness
- Patient matching accuracy
- Clinical appropriateness
- Precision metrics
- Recall (missing patients)
- Intervention readiness
