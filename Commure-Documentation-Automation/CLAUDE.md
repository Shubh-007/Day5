# Commure: Clinical Documentation Automation
## Project Instructions

**Platform**: Commure - Fully Automated Clinical Documentation  
**Focus**: Transform voice encounters → compliant clinical notes (90%+ automated)  
**Metric**: $5-8 saved per encounter, 90%+ one-click approval  
**Timeline**: 20+ weeks to production  

---

## Skills & Agents for This Project

### Skills
```bash
/asr-review note.txt --specialty primary-care --check-billing
/compliance-audit . --framework hipaa
```

### Agents
- **documentation-automation-specialist**: Validates end-to-end note generation
- **compliance-officer**: HIPAA & billing compliance

### MCP Server
- **billing-optimization-server**: Revenue cycle, compliance, medical necessity

---

## Platform-Specific Checks

### Pre-Commit Hooks
- ASR accuracy changes
- Billing code modifications
- Note template logic
- Automation rate metrics

**Auto-checks for:**
- Medical necessity documentation
- ICD-10/CPT code compliance
- Fraud prevention
- Encryption of encounter data

---

## Key Success Metrics

- **Automation Rate**: 90%+ notes one-click approved
- **Accuracy**: 95%+ clinically accurate
- **Compliance**: 99.5% medical necessity documented
- **Latency**: <15 sec per note generation
- **Financial**: $5-8 saved per encounter

---

## Development Priorities

### Phase 0 (Weeks 1-6)
- ASR engine + medical dictionary
- Primary care note generation
- Physician review interface
- Manual QA with 50 physicians

### Phase 1 (Weeks 7-14)
- 10+ specialty templates
- Epic/Cerner integration
- Compliance layer (billing optimization)
- 100K encounters/day scale

### Phase 2 (Weeks 15-20)
- Model fine-tuning (100K real notes)
- Full compliance certification
- 1M+ encounters/day capability

---

## Compliance Checklist

Before each phase gate:
- [ ] /compliance-audit passed
- [ ] Billing codes verified
- [ ] Medical necessity documented
- [ ] Encryption enabled
- [ ] Audit logging active
- [ ] Clinical validator approved

---

## Team Permissions

- **Clinical Lead**: Approves generated notes, validates accuracy
- **Compliance Officer**: Reviews billing, medical necessity
- **DevOps**: Manages ASR engine, scaling
- **Engineers**: Implement per roadmap

---

## Quick Reference

| Metric | Target | Status |
|--------|--------|--------|
| Automation | 90%+ | Phase 0 testing |
| Accuracy | 95%+ | BioBERT baseline |
| Compliance | 99.5%+ | Building layer |
| Latency | <15s | <20s current |

---

**Attribution**: Claude Haiku 4.5  
**Last Updated**: 2026-09-26
