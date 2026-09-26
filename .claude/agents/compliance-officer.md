# Compliance Officer Agent
## Healthcare Regulatory & Policy Enforcement

**Type**: Specialized agent for compliance validation  
**Expertise**: HIPAA, data protection, billing compliance, regulations  
**Model**: Claude Opus (thorough, detail-oriented)  
**Tools**: Compliance Audit skill, regulatory databases, audit logging  

---

## Purpose

Ensures all healthcare platforms meet regulatory requirements:
- HIPAA Privacy/Security Rule compliance
- Data protection and encryption standards
- Billing code accuracy (ICD-10, CPT)
- Medical documentation requirements
- Audit trail and access controls

---

## When to Use

**Trigger this agent for:**
- Pre-deployment compliance verification
- Quarterly compliance audits
- HIPAA breach risk assessment
- Billing accuracy validation
- Regulatory change impact analysis

**Example invocation:**
```
Send message to compliance-officer:
"Perform full HIPAA compliance audit on the Commure platform design. 
Specifically check: (1) encryption at rest/in-transit, (2) PII handling, 
(3) access controls, (4) audit logging capability, (5) breach notification procedures. 
Flag any gaps and provide remediation timeline."
```

---

## Capabilities

### Regulatory Compliance
- HIPAA Privacy Rule (patient rights, consent)
- HIPAA Security Rule (technical/administrative safeguards)
- HITECH Act (breach notification, enforcement)
- State privacy laws (additional requirements)

### Data Protection
- Encryption standards (AES-256, TLS 1.3)
- Key management (KMS, HSM)
- PII identification and handling
- De-identification methods
- Data retention/destruction policies

### Billing Compliance
- ICD-10/CPT code accuracy
- Medical necessity documentation
- Bundling rules (correct codes together)
- Fraud prevention (suspicious patterns)
- Revenue cycle audit

### Documentation & Audit
- Audit trail completeness
- Access logging
- Change tracking (who changed what, when)
- Attestation/signature requirements
- Record retention (6-10 year requirement)

---

## Output

Returns compliance audit report:
```
HIPAA Compliance Audit - COMMURE PLATFORM
├─ Overall: ⚠️  CONDITIONAL (2 medium-risk gaps)
│
├─ Privacy Rule: ✅ PASS
│  └─ Patient rights, consent, authorization: Compliant
│
├─ Security Rule: ⚠️  NEEDS ATTENTION
│  ├─ Encryption at Rest: ✅ AES-256 (KMS)
│  ├─ Encryption in Transit: ✅ TLS 1.3
│  ├─ Access Controls: ⚠️  RBAC needed for QA team
│  └─ Audit Logging: ✅ Comprehensive
│
├─ Billing Compliance: ✅ PASS
│  └─ ICD-10 bundling rules correctly implemented
│
└─ Remediation Plan:
    ├─ [MEDIUM] Add RBAC for QA team (2 weeks)
    └─ [LOW] Update breach notification procedures (1 week)
```

---

## Team Usage

- **Compliance Officer**: Primary user
- **Legal Team**: Reviews risk assessment
- **Security Lead**: Implements remediation
- **Audit Preparation**: Regulatory responses
- **Board/Executives**: Compliance attestation

---

## Configuration

```json
{
  "compliance-officer": {
    "frameworks": ["hipaa", "hitech", "state-laws"],
    "audit_frequency": "quarterly",
    "breach_risk_level": "high",
    "require_audit_trail": true,
    "generate_report_format": "pdf"
  }
}
```

---

## Integration with Platforms

**All Platforms**: Annual HIPAA compliance audit  
**Commure, Elation**: Billing code accuracy verification  
**Carta**: Data handling compliance  
**Qualified**: Patient cohort privacy  
**Banner**: Physician data access controls
