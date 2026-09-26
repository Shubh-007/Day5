# Healthcare Platform Portfolio - Project Instructions

**Project**: 5 Comprehensive Healthcare AI Platforms  
**Date**: 2026-09-26  
**Status**: Complete - Ready for Implementation  
**Platforms**: Banner Health, Carta Healthcare, Commure, Elation Health, Qualified Health  

---

## Project Overview

This project contains complete documentation and infrastructure for 5 healthcare AI platforms totaling 9,000+ lines of strategic planning, technical design, implementation roadmaps, and operational frameworks.

### Platforms in Portfolio

1. **Banner Health** - Physician Documentation Automation (20+ min/day saved)
2. **Carta Healthcare** - Clinical Data Extraction & Structuring (66% faster processing)
3. **Commure** - Clinical Documentation Automation at Scale (90%+ automated)
4. **Elation Health** - Chart Review & Documentation Assistant (61% faster reviews)
5. **Qualified Health** - Patient Screening for Interventions (90%+ accuracy)

---

## Working with This Project

### Skills Available

Use these custom skills for healthcare-specific tasks:

```bash
# Clinical documentation review
/clinical-review <file> --specialty primary-care

# Compliance audit (HIPAA, billing, etc.)
/compliance-audit <platform> --framework hipaa

# EHR integration testing
/ehr-test epic --endpoint https://...
```

### Agents Available

Specialized agents for healthcare work:

**Clinical Validator Agent**:
- Reviews clinical documentation for accuracy
- Validates medical terminology and coding
- Checks for safety issues
- Use when: Reviewing generated clinical content

**Compliance Officer Agent**:
- Ensures HIPAA/regulatory compliance
- Reviews data protection practices
- Audits billing code accuracy
- Use when: Preparing for regulatory review

### MCP Servers (When Configured)

The `ehr-data-server` MCP provides access to:
- Clinical terminology (ICD-10, CPT, RxNorm)
- Drug interaction database
- Clinical guidelines and protocols
- De-identified test data

---

## Development Workflow

### Before Starting Work

1. **Review Platform Documentation**
   ```bash
   cd Day5/<Platform-Name>
   less plan.md  # Executive overview
   less architecture/system-architecture.md  # Technical design
   ```

2. **Check Phase & Status**
   - Each platform has 3 phases (MVP, Scaling, Optimization)
   - Current phase: All completed planning → Ready for Phase 0 dev

3. **Review Success Criteria**
   - Phase gates define what "done" means
   - Check observability-strategy.md for metrics

### During Development

1. **Use Pre-Commit Hooks**
   - Automatically checks for PII, HIPAA issues
   - Validates required documentation exists
   - Prevents accidental credential commits

2. **Track Clinical Quality**
   - Use `/clinical-review` before code changes
   - Validate with clinical validator agent
   - Get compliance officer approval

3. **Maintain Audit Trail**
   - All changes logged automatically
   - Commit messages should reference platform/phase
   - Example: "Banner-Health Phase0: Implement ASR engine"

### Code Quality Standards

**All changes must:**
- ✅ Pass clinical accuracy review (if clinical code)
- ✅ Pass compliance audit (if handling PII/billing)
- ✅ Include appropriate documentation updates
- ✅ Have clear commit message (no PII, no credentials)
- ✅ Include team attribution in commit

---

## Key Project Files

### Documentation Structure
```
Day5/
├── Banner-Health-Clinical-Assistant/
│   ├── plan.md                                  (strategy)
│   ├── architecture/system-architecture.md      (technical)
│   ├── implementation/development-roadmap.md    (timeline)
│   ├── monitoring/observability-strategy.md     (operations)
│   └── README.md                                (quick ref)
├── Carta-Healthcare-Data-Processing/           (same structure)
├── Commure-Documentation-Automation/           (same structure)
├── Elation-Health-Chart-Review/                (same structure)
├── Qualified-Health-Patient-Screening/         (same structure)
└── .claude/
    ├── skills/                                  (custom skills)
    ├── agents/                                  (specialized agents)
    ├── mcp/                                     (data servers)
    ├── hooks/                                   (git automation)
    └── settings.json                            (configuration)
```

### Key Metrics to Know

| Platform | Focus | Team | Budget | Timeline |
|----------|-------|------|--------|----------|
| **Banner** | Physician time-saving | 8 FTE | $3-4.7M | 26 weeks |
| **Carta** | Data extraction | 6 FTE | $2-3M | 20 weeks |
| **Commure** | Note automation | 12 FTE | $4-6M | 20 weeks |
| **Elation** | Chart review | 6 FTE | $1.5-2.5M | 20 weeks |
| **Qualified** | Patient screening | 10 FTE | $3-5M | 21 weeks |

---

## Important Policies

### PII & Data Protection

**DO:**
- Use de-identified test data from MCP server
- Encrypt all sensitive data in code
- Log all access to clinical data
- Use HIPAA-compliant tools

**DON'T:**
- Commit real patient data
- Hardcode credentials or API keys
- Store unencrypted PII anywhere
- Bypass pre-commit security checks

### Clinical Safety

**DO:**
- Get clinical validator review before deployment
- Include safety rationale in code comments
- Test with qualified clinicians (8-10 person board per platform)
- Document all clinical decisions

**DON'T:**
- Make clinical recommendations without validation
- Override clinician judgment in code
- Skip safety testing for "quick" changes
- Modify clinical logic without approval

### Compliance

**DO:**
- Run compliance audit before major releases
- Maintain audit trail of all changes
- Update CLAUDE.md if adding new compliance requirements
- Schedule quarterly HIPAA audits

**DON'T:**
- Merge code that fails compliance audit
- Disable pre-commit security checks
- Work on clinical code without compliance officer notification
- Skip documentation updates

---

## Useful Commands

### Run a Clinical Review
```bash
# Review a platform's documentation
/clinical-review Day5/Commure-Documentation-Automation/plan.md --specialty primary-care

# Review specific clinical section
/clinical-review Day5/Banner-Health-Clinical-Assistant/architecture/system-architecture.md --strictness high
```

### Run Compliance Audit
```bash
# Full HIPAA audit
/compliance-audit commure --framework hipaa --generate-report

# Quarterly comprehensive audit
/compliance-audit all --framework hipaa,state-laws
```

### Test EHR Integration
```bash
# Test Epic connectivity
/ehr-test epic --endpoint https://epic.hospital.com/fhir --load-test

# Test all configured EHRs
/ehr-test all --endpoint-config .claude/ehr-endpoints.json
```

### Get Help
```bash
# Show available skills
/help skills

# Show available agents
/help agents

# Project-specific guidance
less Day5/CLAUDE.md  # (this file)
```

---

## Team Responsibilities

### Clinical Lead
- Reviews clinical accuracy of all documentation
- Approves clinical design decisions
- Leads clinician validation board
- Sign-off on clinical safety

### Compliance Officer
- Reviews all compliance-sensitive changes
- Runs quarterly HIPAA audits
- Maintains regulatory documentation
- Prepares for external audits

### DevOps / Infrastructure
- Deploys platforms following roadmap
- Manages EHR integrations
- Monitors SLAs and performance
- Maintains observability stack

### Engineers / Data Scientists
- Implement features per roadmap
- Follow pre-commit hooks (automatic)
- Request reviews from clinical lead before merging
- Document technical decisions

### Project Manager
- Tracks phase progress
- Manages team allocation
- Reports metrics to stakeholders
- Escalates blockers

---

## Before Implementation (Phase 0 Kickoff)

**Checklist:**
- [ ] All 5 platform plans reviewed and approved
- [ ] Clinician advisory boards formed (8-10 per platform)
- [ ] Budget allocated ($12.2-17.7M Year 1)
- [ ] Teams hired/allocated per roadmap
- [ ] EHR vendor relationships established (Epic, Cerner, etc.)
- [ ] Development environments provisioned
- [ ] HIPAA compliance framework in place
- [ ] Insurance/liability coverage confirmed
- [ ] Legal review of platform designs
- [ ] Baseline metrics established

---

## Where to Find Information

| Question | Location |
|----------|----------|
| **Strategic goals & ROI?** | `*/plan.md` (first 2 sections) |
| **Technical architecture?** | `*/architecture/system-architecture.md` |
| **Implementation timeline?** | `*/implementation/development-roadmap.md` |
| **Success metrics & SLAs?** | `*/monitoring/observability-strategy.md` |
| **Quick reference?** | `*/README.md` |
| **Setup instructions?** | `CLAUDE.md` (this file) |

---

## Communication

### During Development

- **Slack**: #healthcare-platforms (team updates)
- **GitHub Issues**: Platform-specific tickets
- **Standups**: Daily 15-min check-ins per platform
- **Weekly**: Cross-platform sync (architecture/blockers)
- **Monthly**: Compliance review with officer

### Before Merging

- [ ] Code passes pre-commit hooks (automatic)
- [ ] Clinical review completed (if clinical code)
- [ ] Compliance audit passed (if compliance-sensitive)
- [ ] At least 1 other engineer reviewed
- [ ] Tests pass (CI/CD)
- [ ] Commit message is clear and attribution included

---

## Success = Following This Plan

This project succeeds when:
1. ✅ All 5 platforms deployed to production
2. ✅ 1,000+ clinicians actively using platforms
3. ✅ Zero HIPAA violations or breaches
4. ✅ 95%+ uptime across all systems
5. ✅ Documented ROI >= $75M annually
6. ✅ Full regulatory compliance certified

---

## Questions?

- **Clinical questions?** → Ask clinical-validator agent or compliance-officer agent
- **Technical questions?** → See architecture docs or ask in Slack
- **Project process?** → Review this CLAUDE.md file
- **Compliance?** → Review compliance-audit results or ask compliance officer

---

**Last Updated**: 2026-09-26  
**Status**: ✅ Complete - Ready for Phase 0 Development  
**Attribution**: Claude Haiku 4.5
