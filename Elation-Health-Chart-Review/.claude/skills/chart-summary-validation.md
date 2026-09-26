# Chart Summary Validation Skill
## Elation Health - Clinical Summarization Quality

**Trigger**: `/summary-validate` or `chart summary` in Elation context  
**Type**: Summarization quality assurance  

---

## What This Skill Does

Validates Elation Health's AI-generated chart summaries:
- **Conciseness**: Summary captures key info in 100-200 words
- **Completeness**: No critical findings missed
- **Relevance**: Highlights what matters for today's visit
- **Accuracy**: Information matches source chart
- **Usefulness**: Clinician can prepare for visit in <30 seconds

---

## Elation Health Focus

- **Problem**: Clinicians spend 25-30 min per patient on chart review
- **Solution**: AI summarization + visit prep assistant
- **Metric**: 61% time savings (25 min → 10 min)
- **Quality Gate**: 98%+ accuracy, 85%+ adoption

---

## How to Use

```bash
/summary-validate chart_summary.txt --patient-specialty family-medicine --time-target 30-seconds
```

---

## Validates

- Problem list accuracy
- Recent changes identified
- Critical alerts included
- Visit preparation topics
- Clinician can understand in <30 seconds
