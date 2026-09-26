# Compliance Audit Skill
## HIPAA & Healthcare Regulatory Verification

**Trigger**: `/compliance-audit` or `compliance audit` in prompt  
**Type**: Specialized audit agent  
**Use Case**: Verify healthcare platform compliance with regulations  

---

## What This Skill Does

Audits platforms/code for:
- **HIPAA Compliance**: Encryption, access controls, breach notification, audit logging
- **Data Protection**: PII handling, de-identification, data retention policies
- **Billing Compliance**: ICD-10/CPT accuracy, medical necessity documentation, fraud prevention
- **Security**: Authentication, authorization, encryption standards
- **Documentation**: Adequate for regulatory review, signed attestations
- **EHR Standards**: HL7/FHIR compliance, data exchange safety

---

## How to Use

```
/compliance-audit <platform_name> [--framework <framework>] [--generate-report]
```

**Examples**:
```
/compliance-audit commure --framework hipaa --generate-report

/compliance-audit elation-health --framework hitech

/compliance-audit all --framework hipaa,state-laws
```

---

## Frameworks

- **HIPAA**: Federal privacy/security rule
- **HITECH**: Breach notification, enforcement
- **State Laws**: Additional state privacy requirements
- **HIPAA-Omnibus**: Updated HIPAA rules (2013+)
- **21 CFR Part 11**: FDA regulatory compliance

---

## Output

1. **Compliance Score**: 0-100% across frameworks
2. **Gap Analysis**: Which controls are missing/weak
3. **Risk Assessment**: High/medium/low per finding
4. **Remediation Plan**: Priority fixes with timelines
5. **Audit Report**: Exportable for regulators

---

## Integration

Used by:
- **All Platforms**: Pre-deployment verification
- **Banner, Commure, Elation**: Documentation generation compliance
- **Carta, Qualified**: Data handling compliance
- **Security Team**: Annual audits
- **Regulators**: Compliance certification

---

## Configuration

```json
{
  "compliance-audit": {
    "frameworks": ["hipaa", "state-laws"],
    "strictness": "high",
    "generate-remediation-plan": true,
    "export-format": "pdf"
  }
}
```

---

## Team Permissions

- **Compliance Officer**: Full access, can approve fixes
- **Security Lead**: Full access
- **Project Manager**: Read-only
- **Developers**: Can trigger on code changes
