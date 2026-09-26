# Physician Knowledge Server MCP
## Banner Health - Clinical Reference Data

**Type**: MCP Server  
**Purpose**: Provide LLM with physician-relevant clinical knowledge  

---

## Resources

### 1. Clinical Guidelines by Specialty
```
Resource: /guidelines/family-medicine
Output: Evidence-based practice recommendations
```

### 2. Documentation Standards
```
Resource: /documentation/required-elements
Output: What must be documented per visit type
```

### 3. Medication References
```
Resource: /medications/{drug_name}
Output: Dosing, interactions, contraindications
```

### 4. Clinical Decision Rules
```
Resource: /clinical-rules/{condition}
Output: Evidence-based diagnosis/treatment pathways
```

### 5. Burnout Metrics
```
Resource: /burnout/time-saving-targets
Output: Physician time-savings tracking
```

---

## Configuration

Enable in `.claude/settings.json`:
```json
{
  "mcp": {
    "physician-knowledge-server": {
      "enabled": true,
      "specialty": "family-medicine",
      "focus": "documentation-standards"
    }
  }
}
```
