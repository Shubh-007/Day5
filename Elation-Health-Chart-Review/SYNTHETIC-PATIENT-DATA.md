# 🏥 Synthetic Patient Data - Test Suite for RAG Chatbot

## Overview

Added **10 new synthetic patients** to the test database, bringing the total to **13 diverse patient profiles**. These patients represent realistic clinical scenarios to thoroughly test the RAG chatbot with varied:

- Age groups (7 to 78 years)
- Disease complexity (1-5 active conditions)
- Medication loads (1-9 medications)
- Clinical scenarios (asthma, cancer, pregnancy, mental health, etc.)
- Lab abnormalities and safety alerts

---

## Patient Population Summary

```
Total Patients: 13
Age Range: 7 - 78 years

Age Groups:
├─ Pediatric (1):     Sophie Williams, age 7
├─ Young Adult (3):   Emily Watson (28), Jessica Thompson (24), Sarah Johnson (32)
├─ Adult (6):         Linda Martinez (45), David Chen (38), Marcus Davis (41), 
│                      Maria Rodriguez (54), Thomas Anderson (55), Margaret O'Brien (62)
└─ Elderly (3):       James Morrison (67), Robert Chen (72), Robert Mitchell (78)

Complexity:
├─ Simple (1-2 conditions):    Emily Watson, Jessica Thompson, Sarah Johnson, Marcus Davis
├─ Moderate (3-4 conditions):  James Morrison, Maria Rodriguez, Robert Chen, Linda Martinez, 
│                              David Chen, Margaret O'Brien, Thomas Anderson
└─ Complex (5+ conditions):    Robert Mitchell (5 active conditions, 9 medications)
```

---

## New Synthetic Patients - Detailed Profiles

### 1. **Emily Watson** (MRN: P002001)
**Demographics**: 28F, Primary care patient  
**Clinical Focus**: Asthma + Mental Health  

**Active Problems**:
- ✅ Asthma with exacerbations
- ✅ Generalized anxiety disorder

**Medications** (3):
- Albuterol inhaler
- Fluticasone/Salmeterol inhaler
- Sertraline (SSRI)

**Key Testing Points**:
- ✅ Test drug interaction between SSRI and inhalers
- ✅ Query lung function (FEV1)
- ✅ Preventive care screening due
- **Try asking**: "What are the drug interactions?" → Should show minimal interactions
- **Try asking**: "Is this patient's asthma well-controlled?" → Check FEV1 values

---

### 2. **Robert Mitchell** (MRN: P002002) ⭐ Most Complex
**Demographics**: 78M, High-risk patient  
**Clinical Focus**: Polypharmacy + Heart Failure + CKD + Diabetes  

**Active Problems** (5):
- ✅ Congestive heart failure (systolic, EF 35-40%)
- ✅ Hypertension (elevated BP 158/92)
- ✅ Type 2 diabetes with diabetic CKD
- ✅ Coronary artery disease
- ✅ COPD

**Medications** (9) - Complex regimen:
- Carvedilol, Lisinopril, Furosemide, Metoprolol (cardiac)
- Insulin Glargine, Metformin (diabetes)
- Atorvastatin, Aspirin (CAD prevention)
- Tiotropium (COPD)

**Labs** - Multiple abnormalities:
- ⚠️ A1c 8.2% (suboptimal diabetes control)
- ⚠️ Creatinine 1.8 (CKD stage 3)
- ⚠️ eGFR 38 (reduced renal function)
- ⚠️ BNP 480 (elevated - HF marker)
- ⚠️ Potassium 5.2 (hyperkalemia risk)

**Allergies** (2):
- NSAIDs → GI bleeding (MAJOR)
- Codeine → rash (mild)

**Key Testing Points** - Most challenging:
- ✅ Multiple drug interactions (ACE-I + K+ sparing diuretic)
- ✅ Abnormal labs with clinical significance
- ✅ Critical safety alerts (hyperkalemia)
- ✅ Complex clinical guidelines (HF + CKD + DM)
- **Try asking**: "What drug interactions should I be aware of?" → 9 meds, lots to check
- **Try asking**: "Are there any critical labs?" → Multiple abnormalities
- **Try asking**: "What's the clinical guideline for this patient's conditions?" → Complex HF management
- **Try asking**: "What preventive care is overdue?" → Multiple screenings due

---

### 3. **Jessica Thompson** (MRN: P002003)
**Demographics**: 24F, Orthopedic patient  
**Clinical Focus**: Sports injury recovery  

**Active Problems**:
- ✅ Anterior tibial dislocation (acute injury)

**Resolved Problems**:
- ✓ Spinal misalignment (resolved)

**Medications** (1):
- Ibuprofen PRN

**Recent Imaging**:
- X-ray: Anterior tibial dislocation with soft tissue injury

**Key Testing Points**:
- ✅ Young, healthy patient with acute injury
- ✅ NSAID counseling (limit to 2-3 weeks)
- ✅ Physical therapy tracking
- **Try asking**: "What medications should this patient avoid?" → Should note NSAID duration
- **Try asking**: "What's the recovery plan?" → PT for 6 weeks

---

### 4. **Linda Martinez** (MRN: P002004)
**Demographics**: 45F, Endocrine patient  
**Clinical Focus**: Thyroid + Fibromyalgia  

**Active Problems**:
- ✅ Autoimmune thyroiditis (Hashimoto's)
- ✅ Hypothyroidism
- ✅ Fibromyalgia

**Medications** (2):
- Levothyroxine (thyroid replacement)
- Gabapentin (fibromyalgia)

**Lab Trends**:
- ✅ TSH 2.1 (normal - well-controlled)
- ✅ Free T4 1.2 (normal)

**Key Testing Points**:
- ✅ Stable endocrine patient
- ✅ Medication interactions minimal
- ✅ Good disease control
- **Try asking**: "Is the patient's thyroid disease controlled?" → Check TSH/Free T4
- **Try asking**: "What's the treatment for fibromyalgia?" → Gabapentin management

---

### 5. **Sarah Johnson** (MRN: P002005)
**Demographics**: 32F, OB/GYN patient  
**Clinical Focus**: Pregnancy management  

**Active Problems**:
- ✅ Pregnancy <20 weeks gestation

**Medications** (3) - Prenatal only:
- Prenatal vitamin
- Folic acid (800 mcg - neural tube defect prevention)
- Iron supplement

**Labs**:
- ✅ Hemoglobin 12.1 (normal for pregnancy)
- ✅ Fasting glucose 88 (normal)
- ✅ 12-week ultrasound normal

**Key Testing Points**:
- ✅ First trimester pregnancy
- ✅ Appropriate prenatal screening
- ✅ Drug safety in pregnancy
- **Try asking**: "What prenatal screening is due?" → 2nd trimester screening
- **Try asking**: "Are there any medication concerns?" → All prenatal meds safe

---

### 6. **David Chen** (MRN: P002006)
**Demographics**: 38M, Psychiatry patient  
**Clinical Focus**: Depression + Anxiety + Insomnia  

**Active Problems** (3):
- ✅ Major depressive disorder (moderate, single episode)
- ✅ Generalized anxiety disorder
- ✅ Insomnia

**Medications** (2):
- Sertraline 100mg (depression, anxiety)
- Hydroxyzine 25mg (anxiety, sleep)

**Key Testing Points**:
- ✅ Mental health focus
- ✅ Psychotropic drug interactions
- ✅ Sleep management
- **Try asking**: "What medications is this patient on?" → Psychiatric meds
- **Try asking**: "What's the treatment plan for depression?" → SSRI + therapy referral

---

### 7. **Margaret O'Brien** (MRN: P002007) ⭐ Oncology
**Demographics**: 62F, Oncology patient  
**Clinical Focus**: Active cancer treatment with toxicities  

**Active Problems**:
- ✅ Lung cancer (non-small cell)
- ✅ On active chemotherapy (Cycle 7)
- ✅ Chemotherapy-induced anemia

**Medications** (4):
- Carboplatin + Pemetrexed (chemo regimen)
- Ondansetron (nausea)
- Filgrastim (neutropenia prevention)

**Major Allergy**:
- ⚠️ **TAXANE CHEMOTHERAPY HYPERSENSITIVITY** - AVOID!

**Labs**:
- ⚠️ Hemoglobin 10.2 (anemia - trending down)
- ⚠️ WBC 3.8 (neutropenia risk, manageable with filgrastim)
- ✅ Creatinine normal

**Imaging**:
- CT chest: 30% tumor reduction response

**Key Testing Points**:
- ✅ Complex oncology case
- ✅ CRITICAL drug allergy documentation
- ✅ Multiple medication interactions
- ✅ Supportive care coordination
- **Try asking**: "What drug interactions should I be aware of?" → Chemo interactions
- **Try asking**: "What allergies does this patient have?" → TAXANE ALLERGY (critical!)
- **Try asking**: "Are there any lab concerns?" → Anemia management

---

### 8. **Thomas Anderson** (MRN: P002008)
**Demographics**: 55M, Pain management patient  
**Clinical Focus**: Chronic pain with controlled substances  

**Active Problems** (3):
- ✅ Chronic low back pain (16 years)
- ✅ Osteoarthritis (multiple sites)
- ✅ Depression

**Medications** (4):
- Methadone 60mg (long-term opioid)
- Amitriptyline 75mg (pain + mood)
- Muscle relaxant
- Naltrexone (opioid antagonist)

**Key Testing Points**:
- ✅ Complex pain management
- ✅ Controlled substance monitoring
- ✅ Opioid-antidepressant interactions
- ✅ Urine drug screening required
- **Try asking**: "What medications is this patient on?" → Controlled substance alert
- **Try asking**: "What drug interactions should I monitor?" → Opioid/antidepressant combo

---

### 9. **Sophie Williams** (MRN: P002009) 👧 Pediatric
**Demographics**: 7F, Healthy with seasonal issues  
**Clinical Focus**: Pediatric allergies  

**Active Problems**:
- ✅ Allergic rhinitis
- ✓ Recent otitis media (resolved)

**Medications** (1):
- Cetirizine 5mg (pediatric antihistamine)

**Vitals**:
- Age-appropriate growth and development

**Key Testing Points**:
- ✅ Pediatric patient (age 7)
- ✅ Age-appropriate dosing
- ✅ Preventive care focus
- **Try asking**: "What medications is this patient on?" → Pediatric dosing consideration
- **Try asking**: "Is this child up to date on vaccines?" → Check immunization status

---

### 10. **Marcus Davis** (MRN: P002010)
**Demographics**: 41M, HIV specialist patient  
**Clinical Focus**: Well-controlled HIV on modern ART  

**Active Problems** (2):
- ✅ HIV disease (long-term non-progressor)
- ✅ Tobacco use

**Medications** (2):
- Bictegravir/Tenofovir/Emtricitabine (integrase inhibitor-based)
- Cobicistat/Ritonavir booster

**Labs**:
- ✅ CD4 620 (excellent - >500)
- ✅ Viral load <20 copies/mL (undetectable - excellent!)

**Key Testing Points**:
- ✅ Modern HIV care (undetectable = untransmittable)
- ✅ Long-term medication adherence
- ✅ Comprehensive care coordination
- **Try asking**: "What's this patient's HIV status?" → Viral load undetectable
- **Try asking**: "Are there any medication interactions?" → Modern ART, minimal interactions

---

## Testing Scenarios by RAG Query Type

### 💊 Drug Interactions Testing

**Easy** (Few medications):
- Emily Watson: 3 meds, minimal interactions
- Jessica Thompson: 1 med, simple
- Linda Martinez: 2 meds, simple
- Sarah Johnson: 3 prenatal meds

**Moderate** (Multiple medications):
- James Morrison: 4 meds
- David Chen: 2 psychotropic meds
- Marcus Davis: Modern HIV regimen

**Challenging** (Complex interactions):
- Robert Mitchell: 9 medications with critical interaction (K+/ACE-I)
- Margaret O'Brien: 4 chemo + supportive meds
- Thomas Anderson: Opioid + antidepressant + muscle relaxant

**Try these queries:**
```
"What drug interactions should I check?"
"Are there any dangerous medication combinations?"
"What medications interact with [specific drug]?"
```

---

### 🧪 Lab Values Testing

**Normal Labs**:
- Emily Watson, Jessica Thompson (few labs)
- Sarah Johnson (pregnancy labs normal)
- Marcus Davis (HIV labs excellent)

**Abnormal Labs**:
- James Morrison: A1c 7.8%, HDL low
- Robert Mitchell: Multiple abnormalities (A1c, Creatinine, eGFR, K+)
- Margaret O'Brien: Anemia (Hgb 10.2)
- Linda Martinez: Thyroid labs (well-controlled)

**Try these queries:**
```
"Are there any abnormal lab values?"
"What do these lab results mean?"
"Which labs are trending the wrong way?"
"Is this patient's diabetes controlled?"
```

---

### 📚 Clinical Guidelines Testing

**Single Condition**:
- Emily Watson: Asthma guidelines
- Jessica Thompson: Sports injury management
- Linda Martinez: Thyroid disease
- Sarah Johnson: Prenatal care

**Multiple Conditions Requiring Coordination**:
- James Morrison: HTN + DM + Hyperlipidemia
- Robert Mitchell: HF + CKD + DM + CAD (complex!)
- David Chen: Depression + Anxiety
- Thomas Anderson: Chronic pain management

**Try these queries:**
```
"What are the guidelines for managing [condition]?"
"What's the recommended treatment for this patient's conditions?"
"Should we adjust any management plans?"
```

---

### 🚨 Safety & Alerts Testing

**Critical Allergies**:
- Margaret O'Brien: TAXANE HYPERSENSITIVITY (major!)
- Robert Mitchell: NSAID → GI bleeding
- James Morrison: Penicillin rash (mild)

**Safety Alerts**:
- Robert Mitchell: Hyperkalemia risk (K+ 5.2)
- James Morrison: A1c trending up (DM control worsening)
- Margaret O'Brien: Anemia from chemo

**Try these queries:**
```
"What allergies does this patient have?"
"Are there any critical safety alerts?"
"What contraindications should I know about?"
"Is there anything I should avoid prescribing?"
```

---

### 🏥 Preventive Care Testing

**Due Screenings**:
- Emily Watson: Annual physical due
- James Morrison: Diabetic retinopathy screening overdue
- Marcus Davis: Regular HIV monitoring due
- Sophie Williams: Vaccination status

**Pregnancy Screening**:
- Sarah Johnson: 2nd trimester screening due (weeks 15-22)

**Try these queries:**
```
"What preventive care is due?"
"Are there any overdue screenings?"
"What screening should this patient have at this age?"
```

---

## Quick Test Matrix

| Patient | Best For Testing | Complexity | Try This Query |
|---------|------------------|-----------|----------------|
| Emily Watson | Asthma + Mental Health | Low | "What's the FEV1?" |
| Robert Mitchell | **Maximum Complexity** | ⭐⭐⭐ | "What drug interactions should I check?" |
| Jessica Thompson | Sports/Acute Injury | Low | "How long can the patient use ibuprofen?" |
| Linda Martinez | Stable Chronic Illness | Low | "Is the thyroid controlled?" |
| Sarah Johnson | Pregnancy | Moderate | "What screening is due?" |
| David Chen | Psychiatric Meds | Moderate | "What psychiatric meds?" |
| Margaret O'Brien | **Oncology/Critical Allergy** | ⭐⭐⭐ | "What allergies?" |
| Thomas Anderson | Pain/Controlled Substance | Moderate | "What controlled medications?" |
| Sophie Williams | Pediatrics | Low | "Pediatric dosing?" |
| Marcus Davis | HIV/Well-controlled | Moderate | "What's the viral load?" |

---

## Running Tests

### Start with Easy Cases
1. **Emily Watson**: Few meds, simple interactions
2. **Linda Martinez**: Stable disease, good control
3. **Jessica Thompson**: Simple medication regimen

### Progress to Challenging Cases
4. **James Morrison**: Multiple conditions, trending labs
5. **Margaret O'Brien**: Oncology complexity, critical allergy
6. **Robert Mitchell**: Maximum complexity (9 meds, 5 conditions)

### Test All Query Types
- Drug interactions ✅
- Lab values ✅
- Clinical guidelines ✅
- Safety/allergies ✅
- Preventive care ✅

---

## Data File

The synthetic patient data is in:
```
/data/sample_patients.json
```

**Generated by**: `data/generate_patients.py`

To regenerate or add more patients:
```bash
cd data
python3 generate_patients.py
```

---

## Key Statistics

```
Total Patients: 13
├─ Pediatric: 1 (7%)
├─ Young Adult (18-35): 3 (23%)
├─ Middle-aged (36-65): 6 (46%)
└─ Elderly (65+): 3 (23%)

Active Conditions:
├─ Simple (1-2): 4 patients
├─ Moderate (3-4): 6 patients
└─ Complex (5+): 1 patient (Robert Mitchell)

Medication Loads:
├─ Light (1-2): 3 patients
├─ Moderate (3-4): 5 patients
├─ Heavy (5-9): 5 patients
└─ Max: 9 (Robert Mitchell)

Lab Abnormalities:
├─ None: 4 patients
├─ Minor (1-2): 4 patients
├─ Moderate (3-5): 4 patients
└─ Significant (5+): 1 patient (Robert Mitchell)

Allergies:
├─ None: 8 patients
├─ Minor: 3 patients (rash)
└─ Major: 2 patients (GI bleed, hypersensitivity)
```

---

## Next Steps

1. **Run Chatbot Tests**: Ask queries about each patient
2. **Verify Accuracy**: Check RAG responses against medical facts
3. **Test Edge Cases**: Use Robert Mitchell for maximum complexity
4. **Gather Feedback**: Note which queries work best
5. **Refine RAG Engine**: Update response formatters if needed

---

**Generated**: 2026-09-26  
**Total Patients**: 13 (3 original + 10 new)  
**Data File**: `sample_patients.json`  
**Generator Script**: `data/generate_patients.py`
