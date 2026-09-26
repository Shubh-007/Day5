# Clinical Context Server MCP
## Elation Health - Chart Intelligence & Context

**Type**: MCP Server  
**Purpose**: Provide rich clinical context for chart summarization  

---

## Resources

### 1. Patient History Timeline
```
Resource: /patient/history/{patient_id}
Output: Key events in timeline (diagnoses, procedures, med changes)
```

### 2. Chronic Condition Profiles
```
Resource: /conditions/{icd10_code}
Output: Typical trajectory, expected complications, management
```

### 3. Recent Lab Trends
```
Resource: /labs/trends/{test_code}
Output: Historical values, trajectory (improving/worsening)
```

### 4. Drug Interaction Context
```
Resource: /medications/interactions
Input: current med list
Output: Significant interactions to flag
```

### 5. Preventive Care Status
```
Resource: /preventive/overdue
Input: patient age, sex, history
Output: Overdue screenings, immunizations
```

---

## Impact

Helps Elation create summaries that:
- Highlight what changed since last visit
- Flag critical trends
- Identify overdue preventive care
- Help clinician prep in <30 seconds
