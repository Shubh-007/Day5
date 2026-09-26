# Qualified Health: Patient Screening for Interventions
## Project Instructions

**Platform**: Qualified - Life-Saving Patient Identification  
**Focus**: Rules engine + patient screening (90%+ accuracy)  
**Metric**: <500ms patient lookup, >90% precision  

---

## Skills & Agents
```bash
/screen-validate cohort.json --indication heart-failure --target-accuracy 90
```

**Agents**: screening-rules-validator, compliance-officer  
**MCP**: clinical-criteria-server  

---

## Key Checks

- Rule accuracy (90%+)
- Patient identification precision
- False positive rate <5%
- Evidence-based criteria
- Intervention readiness

---

## Success Metrics

- Accuracy: 90%+
- Patient Lookup: <500ms
- Precision: >90%
- Scale: 10-50M patients

---

**Attribution**: Claude Haiku 4.5
