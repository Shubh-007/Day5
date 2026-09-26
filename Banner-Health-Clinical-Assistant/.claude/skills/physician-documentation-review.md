# Physician Documentation Review Skill
## Banner Health - Clinical Note Quality & Accuracy

**Trigger**: `/doc-review` or `documentation review` in Banner context  
**Type**: Specialized clinical review  
**Use Case**: Validate AI-generated physician documentation  

---

## What This Skill Does

Reviews physician documentation (clinical notes) for:
- **Clinical Accuracy**: Medical facts, diagnosis appropriateness, treatment logic
- **Physician Workflow**: Time savings, efficiency, physician satisfaction
- **Documentation Quality**: Completeness, required elements, clinical reasoning
- **Compliance**: Medical necessity, ICD-10 codes, EHR integration
- **Burnout Relief**: How well AI reduces physician administrative burden

---

## Banner Health Focus Areas

- **Problem**: Physicians spend 40% of time on documentation (huge burnout driver)
- **Solution**: AI drafts notes, physician reviews/approves
- **Metric**: 20+ minutes saved per physician per day
- **Quality Gate**: 95%+ clinical accuracy, 85%+ one-click approval

---

## How to Use

```bash
/doc-review <note> --physician-specialty family-medicine --review-type draft-quality
```

---

## Integration

Used by Banner Health to validate:
- AI-drafted clinical notes before physician review
- Physician satisfaction with AI suggestions
- Time savings impact
