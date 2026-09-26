# ASR Note Generation Review Skill
## Commure - Automated Documentation Quality

**Trigger**: `/asr-review` or `note generation` in Commure context  
**Type**: Automated documentation validation  

---

## What This Skill Does

Reviews Commure's automatically generated clinical notes:
- **ASR Accuracy**: Speech-to-text quality
- **Note Completeness**: All required sections present
- **Billing Appropriateness**: ICD-10/CPT codes correct
- **Physician Usability**: Will physician approve without edits?
- **Compliance**: Medical necessity documented

---

## Commure Focus

- **Problem**: 75M clinician hours/year on documentation ($11.25B)
- **Solution**: Fully automated note generation from encounters
- **Metric**: 90%+ automation (minimal physician edits)
- **Quality Gate**: 95%+ accuracy, 99%+ compliance

---

## How to Use

```bash
/asr-review generated_note.txt --specialty primary-care --check-billing
```

---

## Special Checks

- Speech recognition quality
- Template appropriateness
- Billing code accuracy
- Medical necessity documentation
- One-click approval likelihood
