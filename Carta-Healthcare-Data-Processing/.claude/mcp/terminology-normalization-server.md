# Terminology Normalization Server MCP
## Carta Healthcare - Clinical Code Standardization

**Type**: MCP Server  
**Purpose**: Normalize clinical terminology to standard codes  

---

## Resources

### 1. ICD-10 Lookup & Validation
```
Resource: /icd10/lookup
Input: "diabetes type 2"
Output: ICD-10 code + validation
```

### 2. RxNorm Drug Codes
```
Resource: /rxnorm/lookup
Input: "metformin 500mg"
Output: RxNorm code + dosing
```

### 3. LOINC Lab Tests
```
Resource: /loinc/lookup
Input: "hemoglobin"
Output: LOINC code + normal ranges
```

### 4. CPT Procedures
```
Resource: /cpt/lookup
Input: "cardiac catheterization"
Output: CPT code + bundling rules
```

### 5. SNOMED-CT Relations
```
Resource: /snomed/relations
Input: ["diabetes", "kidney_disease"]
Output: Clinical relationships
```

---

## Use Case

When Carta extracts "patient has Type 2 diabetes", MCP:
1. Looks up ICD-10: E11.9
2. Validates code correctness
3. Checks for bundling conflicts
4. Returns normalized clinical code
