# 🧪 Patient Testing Guide - RAG Chatbot

## Quick Reference: 13 Synthetic Patients

### Dashboard View - All Patients

```
MRN        Name               Age  Gender  Provider             Complexity
--------   ---------------    ---  ------  -------------------  -----------
P001234    James Morrison     67   M       Dr. Sarah Chen       ⭐⭐
P005678    Maria Rodriguez    54   F       Dr. Michael Torres   ⭐
P009012    Robert Chen        72   M       Dr. Angela Jackson   ⭐⭐
P002001    Emily Watson       28   F       Dr. Kevin Patel      ⭐
P002002    Robert Mitchell    78   M       Dr. Michael Torres   ⭐⭐⭐ COMPLEX
P002003    Jessica Thompson   24   F       Dr. Angela Jackson   ⭐
P002004    Linda Martinez     45   F       Dr. Kevin Patel      ⭐
P002005    Sarah Johnson      32   F       Dr. Rebecca Wilson   ⭐⭐
P002006    David Chen         38   M       Dr. James Lee        ⭐⭐
P002007    Margaret O'Brien   62   F       Dr. Angela Jackson   ⭐⭐⭐ ONCOLOGY
P002008    Thomas Anderson    55   M       Dr. Kevin Patel      ⭐⭐
P002009    Sophie Williams    7    F       Dr. Rebecca Wilson   ⭐ PEDIATRIC
P002010    Marcus Davis       41   M       Dr. Sarah Chen       ⭐⭐
```

---

## Test Scenarios by Specialty

### 🫀 CARDIOLOGY - Heart Failure Complex
**Patient**: Robert Mitchell (P002002) ⭐⭐⭐  
**Age**: 78M | **Provider**: Dr. Michael Torres  
**Primary Condition**: Systolic heart failure (EF 35-40%)

**Test Queries**:
```
1. "What drug interactions should I check?"
   Expected: ACE-I + K-sparing diuretic warning ✓

2. "Are there any critical labs?"
   Expected: K+ 5.2 (hyperkalemia), BNP 480 (elevated) ✓

3. "What's the clinical guideline for heart failure management?"
   Expected: Beta-blocker, ACE-I, diuretic, monitoring ✓

4. "What preventive care is overdue?"
   Expected: Diabetic retinopathy, COPD management ✓

5. "What are the patient's vital signs?"
   Expected: BP 158/92 (elevated), HR 68 ✓
```

**Medications**: 9 (Maximum load)  
**Active Conditions**: 5 (HF, HTN, DM+CKD, CAD, COPD)  
**Critical Alerts**: ⚠️ Hyperkalemia risk  

---

### 🫁 PULMONOLOGY - Asthma & COPD
**Easy**: Emily Watson (P002001) - Young asthma  
**Complex**: Robert Mitchell (P002002) - COPD with CHF  

#### Emily Watson (P002001)
**Age**: 28F | **Provider**: Dr. Sarah Chen  
**Conditions**: Asthma + Anxiety

**Test Queries**:
```
1. "Is this patient's asthma well-controlled?"
   Expected: FEV1 88% (good), using inhaler 1-2x/week ✓

2. "What about medication interactions?"
   Expected: Minimal - SSRI + inhalers safe together ✓

3. "What screenings are recommended?"
   Expected: Annual physical, anxiety monitoring ✓
```

---

### 🧠 PSYCHIATRY - Mental Health
**Patient**: David Chen (P002006)  
**Age**: 38M | **Provider**: Dr. James Lee  
**Conditions**: Depression + Anxiety + Insomnia

**Test Queries**:
```
1. "What psychiatric medications is this patient on?"
   Expected: Sertraline 100mg, Hydroxyzine 25mg ✓

2. "Are there any drug interactions with psychiatric meds?"
   Expected: Minimal interactions, monitor for serotonin syndrome ✓

3. "What's the treatment plan?"
   Expected: SSRI + sleep aid + CBT referral pending ✓
```

**Medications**: 2 (SSRI + anxiolytic)  
**Active Conditions**: 3 (depression, anxiety, insomnia)  

---

### 👶 PEDIATRICS - Child Health
**Patient**: Sophie Williams (P002009)  
**Age**: 7F | **Provider**: Dr. Rebecca Wilson  
**Conditions**: Allergic rhinitis, recent otitis media (resolved)

**Test Queries**:
```
1. "What medications is this child on?"
   Expected: Cetirizine 5mg (pediatric dose) ✓

2. "Is the child up to date on vaccines?"
   Expected: Yes, vaccines current ✓

3. "What's the recommended preventive care?"
   Expected: Annual physical, routine screenings ✓
```

**Special**: Pediatric dosing, age-appropriate care  

---

### 🤰 OB/GYN - Pregnancy
**Patient**: Sarah Johnson (P002005)  
**Age**: 32F | **Provider**: Dr. Rebecca Wilson  
**Condition**: Pregnancy <20 weeks

**Test Queries**:
```
1. "What's the pregnancy status?"
   Expected: 12 weeks, normal development ✓

2. "What prenatal screening is due?"
   Expected: 2nd trimester screening (weeks 15-22) ✓

3. "Are all medications safe in pregnancy?"
   Expected: Yes - prenatal vitamins, folic acid, iron safe ✓

4. "What's the ultrasound status?"
   Expected: 12-week anatomy normal ✓
```

**Medications**: 3 (All prenatal/safe)  
**Labs**: Normal pregnancy labs  
**Alerts**: Screening reminders  

---

### 🏥 ENDOCRINOLOGY - Thyroid & Diabetes
**Easy Thyroid**: Linda Martinez (P002004) - Well-controlled  
**Complex Diabetes**: Robert Mitchell (P002002) - Poorly controlled with CKD  

#### Linda Martinez (P002004)
**Age**: 45F | **Provider**: Dr. Kevin Patel  
**Conditions**: Hashimoto's + Hypothyroidism + Fibromyalgia

**Test Queries**:
```
1. "Is this patient's thyroid disease controlled?"
   Expected: TSH 2.1, Free T4 1.2 - well controlled ✓

2. "What's the fibromyalgia treatment?"
   Expected: Gabapentin 300mg three times daily ✓
```

---

### 🔬 ONCOLOGY - Cancer Treatment
**Patient**: Margaret O'Brien (P002007) ⭐⭐⭐  
**Age**: 62F | **Provider**: Dr. Angela Jackson  
**Condition**: Lung cancer on active chemo (Cycle 7)

**Test Queries**:
```
1. "What allergies does this patient have?"
   Expected: ⚠️ TAXANE HYPERSENSITIVITY - CRITICAL! ✓

2. "What chemotherapy drugs is the patient on?"
   Expected: Carboplatin + Pemetrexed (non-taxane) ✓

3. "Are there any lab concerns?"
   Expected: Hemoglobin 10.2 (anemia), WBC 3.8 (manageable) ✓

4. "What's the tumor response?"
   Expected: CT shows 30% reduction (good response) ✓
```

**Medications**: 4 chemo + supportive care  
**Critical Allergy**: TAXANE (must avoid!)  
**Labs**: Anemia, neutropenia risk  

---

### 💊 PAIN MANAGEMENT - Chronic Pain
**Patient**: Thomas Anderson (P002008)  
**Age**: 55M | **Provider**: Dr. Kevin Patel  
**Condition**: Chronic low back pain (16 years)

**Test Queries**:
```
1. "What controlled medications is this patient on?"
   Expected: Methadone 60mg (opioid), monitoring required ✓

2. "Are there medication interactions?"
   Expected: Opioid + antidepressant + muscle relaxant - monitor ✓

3. "Is urine drug screening required?"
   Expected: Yes, required for opioid therapy ✓
```

**Medications**: 4 (Including methadone)  
**Controlled Substance**: Methadone monitoring  
**Labs**: UDS positive for methadone (expected) ✓  

---

### 🦠 INFECTIOUS DISEASE - HIV
**Patient**: Marcus Davis (P002010)  
**Age**: 41M | **Provider**: Dr. Sarah Chen  
**Condition**: HIV (well-controlled, undetectable)

**Test Queries**:
```
1. "What's this patient's HIV viral load?"
   Expected: <20 copies/mL (undetectable!) ✓

2. "Is the CD4 count adequate?"
   Expected: 620 (excellent, >500 is safe) ✓

3. "What ART medications?"
   Expected: Modern integrase inhibitor-based regimen ✓
```

**Medications**: 2 (Modern ART)  
**Viral Load**: Undetectable ✓  
**CD4**: 620 (excellent) ✓  

---

## Testing Difficulty Levels

### 🟢 EASY - Start Here
**Best for learning RAG chatbot behavior**

1. **Emily Watson** (P002001)
   - Simple case, stable asthma
   - Few medications, minimal interactions
   - Normal or near-normal labs
   
2. **Linda Martinez** (P002004)
   - Stable thyroid disease
   - Well-controlled on monotherapy essentially
   - Normal TSH/Free T4
   
3. **Jessica Thompson** (P002003)
   - Young, healthy athlete with acute injury
   - Single medication (ibuprofen)
   - Clear clinical picture

### 🟡 MEDIUM - Middle Ground
**For intermediate testing**

1. **James Morrison** (P001234)
   - Multiple conditions (HTN, DM, Hyperlipidemia)
   - 4 medications, some interactions
   - Some abnormal labs (A1c trending up)

2. **Sarah Johnson** (P002005)
   - Pregnancy-specific care
   - Prenatal screening management
   - Multiple medication categories (safe in pregnancy)

3. **David Chen** (P002006)
   - Psychiatric focus
   - Psychotropic drug interactions
   - Mental health management

### 🔴 HARD - Advanced Testing
**For comprehensive RAG validation**

1. **Margaret O'Brien** (P002007)
   - ⭐ Oncology focus
   - Critical allergy (TAXANE)
   - Chemotherapy toxicities
   - Complex supportive care

2. **Thomas Anderson** (P002008)
   - Controlled substance management
   - Opioid monitoring requirements
   - Complex drug interactions

3. **Robert Mitchell** (P002002)
   - ⭐⭐⭐ MAXIMUM COMPLEXITY
   - 9 medications (polypharmacy)
   - 5 active conditions
   - Multiple abnormal labs
   - Critical safety alert (hyperkalemia)
   - Heart failure + CKD + diabetes coordination

---

## Test Plan by Query Type

### Test 1: Drug Interactions
```
Start:     Emily Watson (P002001)     3 meds, minimal interactions
Progress:  James Morrison (P001234)   4 meds, some interactions
Challenge: Robert Mitchell (P002002)  9 meds, critical interaction
Oncology:  Margaret O'Brien (P002007) Chemo + supportive care
```

### Test 2: Lab Values
```
Start:     Linda Martinez (P002004)    All normal (TSH, Free T4)
Progress:  James Morrison (P001234)    Some abnormalities (A1c, lipids)
Challenge: Robert Mitchell (P002002)   Multiple abnormalities
Oncology:  Margaret O'Brien (P002007)  Chemotherapy toxicities
```

### Test 3: Clinical Guidelines
```
Start:     Emily Watson (P002001)      Single condition (asthma)
Progress:  James Morrison (P001234)    Multiple conditions
Challenge: Robert Mitchell (P002002)   Complex multi-condition management
OB/GYN:    Sarah Johnson (P002005)     Pregnancy-specific guidelines
```

### Test 4: Safety & Allergies
```
Start:     Emily Watson (P002001)      Mild allergy (Sulfonamide)
Progress:  James Morrison (P001234)    Single allergy (Penicillin)
Challenge: Margaret O'Brien (P002007)  CRITICAL allergy (Taxane!)
Warning:   Robert Mitchell (P002002)   NSAID contraindication
```

### Test 5: Preventive Care
```
Start:     Emily Watson (P002001)      Annual physical due
Progress:  James Morrison (P001234)    Diabetic screening overdue
OB/GYN:    Sarah Johnson (P002005)     Prenatal screening due
Pediatric: Sophie Williams (P002009)   Immunization status
```

---

## Success Criteria Checklist

For each patient, verify:

- ✅ **Can find patient in dashboard**
- ✅ **Can view patient's QuickView**
- ✅ **RAG chatbot appears at bottom**
- ✅ **Can expand/collapse chatbot**
- ✅ **Suggested questions appear**
- ✅ **Can type custom question**
- ✅ **Response appears with confidence score**
- ✅ **Sources are cited**
- ✅ **Response is clinically accurate**

---

## Quick Test Checklist

### For Each Patient, Try:
```
□ "What medications is this patient on?"
□ "Are there any drug interactions?"
□ "Are there any abnormal lab values?"
□ "What's the clinical guideline?"
□ "What preventive care is due?"
□ "What allergies does this patient have?"
□ "Are there any safety concerns?"
```

### Expected Results:
- ✅ All queries return within 300ms
- ✅ All responses show confidence 75-95%
- ✅ Sources are cited (1-3 per response)
- ✅ No JavaScript errors in browser console
- ✅ Responses match clinical data

---

## Performance Baseline

```
Empty Query Response:    < 50ms
Simple Query (1 data):   100-150ms
Moderate Query (2-3):    150-250ms
Complex Query (5+ items):<300ms
```

---

## Troubleshooting

**Chatbot not appearing?**
→ Make sure you're on QuickView (not Dashboard)
→ Scroll down past vital signs and alerts

**Getting errors?**
→ Check browser console (F12)
→ Verify backend is running on port 8000
→ Check network tab for API errors

**Response seems wrong?**
→ Verify patient data in sample_patients.json
→ Check RAG engine responses in backend logs
→ Compare to clinical guidelines

---

**Last Updated**: 2026-09-26  
**Total Patients**: 13  
**Difficulty Levels**: Easy (3) | Medium (3) | Hard (3) | Plus originals (4)  
**Total Test Queries**: 50+
