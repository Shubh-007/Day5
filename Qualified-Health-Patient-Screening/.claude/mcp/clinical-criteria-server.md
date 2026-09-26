# Clinical Criteria Server MCP
## Qualified Health - Evidence-Based Screening

**Type**: MCP Server  
**Purpose**: Provide evidence-based screening criteria for patient identification  

---

## Resources

### 1. Condition-Specific Criteria
```
Resource: /screening/heart-failure
Output: Inclusion criteria, exclusion criteria, risk scores
```

### 2. Lab Thresholds
```
Resource: /thresholds/{test_code}
Input: test name
Output: Normal ranges, intervention thresholds per condition
```

### 3. Risk Stratification Models
```
Resource: /risk/models/{condition}
Output: Validated risk calculators (CHADS2, ASCVD, etc.)
```

### 4. Clinical Guideline Rules
```
Resource: /guidelines/{indication}
Output: Evidence-based identification & intervention rules
```

### 5. Intervention Protocols
```
Resource: /interventions/{indication}
Output: What intervention for identified patients
```

---

## Impact

Helps Qualified identify:
- Patients meeting clinical criteria for intervention
- Risk stratification for prioritization
- Evidence-based eligibility rules
- Real-time patient lookup capabilities
