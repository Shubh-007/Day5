"""
Elation Health - RAG Engine
Retrieval-Augmented Generation for Clinical Knowledge

Enables sub-agents to retrieve relevant clinical information,
guidelines, drug interactions, and diagnostic criteria.
"""

import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class KnowledgeEntry:
    """Represents a clinical knowledge entry"""
    id: str
    type: str  # "condition", "medication", "drug_interaction", "guideline", "screening"
    title: str
    content: str
    relevance_score: float = 0.0
    source: str = "clinical_database"
    last_updated: str = None


class ClinicalKnowledgeBase:
    """Clinical knowledge base for RAG retrieval"""

    def __init__(self):
        self.conditions = self._load_conditions()
        self.medications = self._load_medications()
        self.drug_interactions = self._load_drug_interactions()
        self.guidelines = self._load_guidelines()
        self.screening_protocols = self._load_screening_protocols()

    def _load_conditions(self) -> Dict[str, Dict]:
        """Load condition profiles (ICD-10 based)"""
        return {
            "I10": {
                "name": "Essential (primary) hypertension",
                "icd10": "I10",
                "description": "Hypertension without secondary cause",
                "pathophysiology": "Increased vascular resistance and/or increased cardiac output",
                "complications": ["Coronary artery disease", "Stroke", "Heart failure", "Chronic kidney disease"],
                "management": ["ACE inhibitor or ARB", "Beta-blocker", "Calcium channel blocker", "Diuretic", "Lifestyle modifications"],
                "target_bp": "< 130/80 mmHg",
                "red_flags": ["BP > 180/120 (hypertensive urgency)", "Chest pain", "Shortness of breath", "Neurological symptoms"],
                "monitoring": "Monthly until controlled, then quarterly"
            },
            "E11.9": {
                "name": "Type 2 diabetes mellitus without complications",
                "icd10": "E11.9",
                "description": "Type 2 diabetes, the most common form",
                "pathophysiology": "Insulin resistance and beta-cell dysfunction",
                "complications": ["Neuropathy", "Nephropathy", "Retinopathy", "Cardiovascular disease"],
                "management": ["Metformin (first-line)", "GLP-1 agonist", "SGLT2 inhibitor", "Sulfonylurea", "Insulin"],
                "target_a1c": "< 7%",
                "red_flags": ["A1c > 10%", "Blood glucose > 500 mg/dL", "DKA symptoms", "Severe hypoglycemia"],
                "monitoring": "A1c every 3 months until stable"
            },
            "E78.5": {
                "name": "Hyperlipidemia, unspecified",
                "icd10": "E78.5",
                "description": "Elevated cholesterol and/or triglycerides",
                "pathophysiology": "Abnormal lipid metabolism",
                "complications": ["Atherosclerosis", "Acute coronary syndrome", "Stroke"],
                "management": ["Statin (first-line)", "Ezetimibe", "Bile acid sequestrant", "PCSK9 inhibitor"],
                "target_ldl": "< 100 mg/dL (or < 70 for high-risk)",
                "red_flags": ["LDL > 200 mg/dL", "Triglycerides > 500 mg/dL"],
                "monitoring": "Lipid panel 4-12 weeks after start/change"
            },
            "I50.9": {
                "name": "Heart failure, unspecified",
                "icd10": "I50.9",
                "description": "Impaired cardiac output leading to hemodynamic dysfunction",
                "pathophysiology": "Systolic or diastolic dysfunction",
                "complications": ["Arrhythmias", "Acute pulmonary edema", "Cardiorenal syndrome", "Sudden cardiac death"],
                "management": ["ACE inhibitor/ARB", "Beta-blocker", "Aldosterone antagonist", "SGLT2 inhibitor", "Diuretic"],
                "target_ef": "> 40%",
                "red_flags": ["Orthopnea", "Paroxysmal nocturnal dyspnea", "Rapid weight gain", "Syncope"],
                "monitoring": "BNP/NT-proBNP, echocardiogram annually"
            },
            "F41.1": {
                "name": "Generalized anxiety disorder",
                "icd10": "F41.1",
                "description": "Persistent worry and anxiety lasting > 6 months",
                "pathophysiology": "Dysregulation of GABAergic and serotonergic systems",
                "complications": ["Depression", "Substance abuse", "Panic disorder", "Social dysfunction"],
                "management": ["SSRI (first-line)", "Buspirone", "Cognitive behavioral therapy", "Mindfulness"],
                "assessment_tools": ["GAD-7 questionnaire", "PSYCH-5 screening"],
                "red_flags": ["Suicidal ideation", "Acute panic", "Substance use escalation"],
                "monitoring": "GAD-7 at each visit; titrate meds over 4-6 weeks"
            }
        }

    def _load_medications(self) -> Dict[str, Dict]:
        """Load medication profiles"""
        return {
            "Metformin": {
                "generic_name": "Metformin",
                "drug_class": "Biguanide (antidiabetic)",
                "indications": ["Type 2 diabetes"],
                "starting_dose": "500 mg daily",
                "target_dose": "1000-2000 mg daily (divided)",
                "max_dose": "2550 mg daily",
                "side_effects": ["GI upset", "Lactic acidosis (rare)", "Vitamin B12 deficiency"],
                "monitoring": "Renal function, B12 level annually",
                "contraindications": ["eGFR < 30", "Acute illness", "Radiographic contrast"],
                "interactions": []
            },
            "Lisinopril": {
                "generic_name": "Lisinopril",
                "drug_class": "ACE inhibitor (antihypertensive)",
                "indications": ["Hypertension", "Heart failure"],
                "starting_dose": "10 mg daily",
                "target_dose": "20-40 mg daily",
                "max_dose": "40 mg daily",
                "side_effects": ["Dry cough", "Hyperkalemia", "Angioedema (rare but serious)"],
                "monitoring": "Potassium, creatinine at baseline and 2-4 weeks",
                "contraindications": ["Pregnancy", "Angioedema history", "Bilateral renal artery stenosis"],
                "interactions": ["NSAIDs", "Potassium supplements", "ARBs"]
            },
            "Atorvastatin": {
                "generic_name": "Atorvastatin",
                "drug_class": "Statin (lipid-lowering)",
                "indications": ["Hyperlipidemia", "Cardiovascular disease prevention"],
                "starting_dose": "20 mg daily",
                "target_dose": "40-80 mg daily",
                "max_dose": "80 mg daily",
                "side_effects": ["Muscle pain/myopathy", "Elevated liver enzymes", "Memory issues (rare)"],
                "monitoring": "Lipid panel 4-12 weeks; liver enzymes baseline and if symptoms",
                "contraindications": ["Active liver disease", "Pregnancy"],
                "interactions": ["CYP3A4 inhibitors", "Fibrates", "Grapefruit juice"]
            },
            "Sertraline": {
                "generic_name": "Sertraline",
                "drug_class": "SSRI (antidepressant/anxiolytic)",
                "indications": ["Depression", "Anxiety disorders", "OCD", "PTSD"],
                "starting_dose": "50 mg daily",
                "target_dose": "100-200 mg daily",
                "max_dose": "200 mg daily",
                "side_effects": ["Sexual dysfunction", "Sleep disturbance", "GI upset", "Serotonin syndrome"],
                "monitoring": "Clinical response at 4-6 weeks; suicide risk in young adults",
                "contraindications": ["MAOI use", "Linezolid, methylene blue"],
                "interactions": ["NSAIDs", "Warfarin", "Other serotonergic agents"]
            },
            "Metoprolol": {
                "generic_name": "Metoprolol",
                "drug_class": "Beta-blocker (antihypertensive, cardioprotective)",
                "indications": ["Hypertension", "Heart failure", "Coronary artery disease"],
                "starting_dose": "25-50 mg daily",
                "target_dose": "100-200 mg daily (divided)",
                "max_dose": "200 mg daily",
                "side_effects": ["Fatigue", "Bradycardia", "Dyspnea", "Sexual dysfunction"],
                "monitoring": "Heart rate, blood pressure; adjust for symptoms",
                "contraindications": ["Cardiogenic shock", "Severe bradycardia", "Decompensated heart failure"],
                "interactions": ["Verapamil", "Diltiazem", "Clonidine"]
            }
        }

    def _load_drug_interactions(self) -> Dict[str, List[Dict]]:
        """Load known drug interactions"""
        return {
            "Lisinopril": [
                {
                    "interacting_drug": "NSAIDs (ibuprofen, naproxen)",
                    "severity": "major",
                    "mechanism": "Reduced antihypertensive effect, increased renal toxicity",
                    "management": "Use alternative analgesic or monitor renal function"
                },
                {
                    "interacting_drug": "Potassium supplements",
                    "severity": "major",
                    "mechanism": "Hyperkalemia risk",
                    "management": "Monitor potassium levels; usually avoid potassium supplements"
                },
                {
                    "interacting_drug": "Atorvastatin",
                    "severity": "moderate",
                    "mechanism": "Increased myopathy risk",
                    "management": "Monitor for muscle pain"
                }
            ],
            "Metformin": [
                {
                    "interacting_drug": "Iodinated contrast",
                    "severity": "major",
                    "mechanism": "Risk of lactic acidosis",
                    "management": "Hold metformin before and 48 hours after contrast"
                },
                {
                    "interacting_drug": "Alcohol (chronic)",
                    "severity": "moderate",
                    "mechanism": "Increased lactic acidosis risk",
                    "management": "Limit alcohol intake"
                }
            ],
            "Atorvastatin": [
                {
                    "interacting_drug": "CYP3A4 inhibitors (erythromycin, diltiazem)",
                    "severity": "major",
                    "mechanism": "Increased statin levels, myopathy risk",
                    "management": "Use lower statin dose or alternative agent"
                },
                {
                    "interacting_drug": "Grapefruit juice",
                    "severity": "moderate",
                    "mechanism": "Increased statin levels",
                    "management": "Avoid grapefruit juice"
                }
            ]
        }

    def _load_guidelines(self) -> Dict[str, Dict]:
        """Load clinical guidelines"""
        return {
            "hypertension_2024": {
                "title": "2024 ACC/AHA Hypertension Guidelines",
                "source": "American College of Cardiology / American Heart Association",
                "target_bp_general": "< 130/80 mmHg",
                "target_bp_elderly": "< 130/80 mmHg (if tolerated)",
                "first_line_agents": ["ACE inhibitor", "ARB", "Calcium channel blocker", "Thiazide diuretic"],
                "key_points": [
                    "Start with single agent in most patients",
                    "Add second agent if BP not at goal after 1 month",
                    "Lifestyle modifications essential",
                    "Regular monitoring required"
                ]
            },
            "diabetes_management_2024": {
                "title": "2024 ADA Standards of Medical Care in Diabetes",
                "source": "American Diabetes Association",
                "target_a1c_general": "7%",
                "target_a1c_elderly": "7.5-8.5%",
                "target_a1c_new_diagnosis": "Start with 7.5%, reassess",
                "screening_frequency": "A1c every 3-6 months",
                "first_line_medication": "Metformin",
                "add_on_agents": ["GLP-1 receptor agonist", "SGLT2 inhibitor", "DPP-4 inhibitor"],
                "key_points": [
                    "Individualize glycemic targets",
                    "Consider cardiovascular and renal benefits",
                    "SGLT2 inhibitors for CKD/HF",
                    "GLP-1 agonists for weight loss/CVD benefit"
                ]
            }
        }

    def _load_screening_protocols(self) -> Dict[str, List[Dict]]:
        """Load preventive care screening protocols"""
        return {
            "diabetes": [
                {"screening": "Retinopathy exam", "frequency": "Annual", "method": "Dilated eye exam or imaging"},
                {"screening": "Urine microalbumin", "frequency": "Annual", "method": "Urine ACR"},
                {"screening": "Foot exam", "frequency": "Annual", "method": "Monofilament, vibration, reflexes"},
                {"screening": "Lipid panel", "frequency": "Annual", "method": "Lab test"},
            ],
            "cancer": [
                {"screening": "Colorectal cancer", "frequency": "Every 10 years (age 45+)", "method": "Colonoscopy"},
                {"screening": "Mammography", "frequency": "Annual (age 40+) or every 2 years (age 50+)", "method": "Screening mammography"},
                {"screening": "Prostate cancer", "frequency": "Shared decision-making (age 50+)", "method": "PSA + DRE"},
            ],
            "cardiovascular": [
                {"screening": "Blood pressure", "frequency": "Every visit", "method": "BP measurement"},
                {"screening": "Lipid panel", "frequency": "Every 5 years (adults)", "method": "Lipid panel"},
                {"screening": "AAA screening", "frequency": "One-time (men 65-75 who smoke)", "method": "Abdominal ultrasound"},
            ]
        }

    def search_conditions(self, query: str) -> List[KnowledgeEntry]:
        """Search for condition information"""
        results = []
        query_lower = query.lower()

        for icd_code, condition in self.conditions.items():
            score = 0
            if query_lower in condition["name"].lower():
                score += 2.0
            if query_lower in condition.get("description", "").lower():
                score += 1.0

            if score > 0:
                results.append(KnowledgeEntry(
                    id=icd_code,
                    type="condition",
                    title=condition["name"],
                    content=json.dumps(condition),
                    relevance_score=score,
                    source="clinical_database"
                ))

        return sorted(results, key=lambda x: x.relevance_score, reverse=True)

    def search_medications(self, query: str) -> List[KnowledgeEntry]:
        """Search for medication information"""
        results = []
        query_lower = query.lower()

        for med_name, med_info in self.medications.items():
            score = 0
            if query_lower in med_name.lower():
                score += 2.0
            if query_lower in med_info.get("indications", []):
                score += 1.5

            if score > 0:
                results.append(KnowledgeEntry(
                    id=med_name,
                    type="medication",
                    title=med_name,
                    content=json.dumps(med_info),
                    relevance_score=score,
                    source="drug_database"
                ))

        return sorted(results, key=lambda x: x.relevance_score, reverse=True)

    def get_drug_interactions(self, medications: List[str]) -> Dict[str, Any]:
        """Get interactions between multiple medications"""
        interactions = []
        medications_lower = [m.lower() for m in medications]

        for med1 in medications:
            if med1 in self.drug_interactions:
                for interaction in self.drug_interactions[med1]:
                    interacting_drug_lower = interaction["interacting_drug"].lower()
                    # Check if any other medication matches
                    for med2 in medications:
                        if med1 != med2 and med2.lower() in interacting_drug_lower:
                            interactions.append({
                                "drug1": med1,
                                "drug2": med2,
                                **interaction
                            })

        return {
            "medications_checked": medications,
            "total_interactions": len(interactions),
            "interactions": interactions,
            "critical_interactions": [i for i in interactions if i["severity"] == "major"],
            "timestamp": datetime.now().isoformat()
        }

    def get_guidelines(self, condition: str) -> Optional[Dict]:
        """Get clinical guidelines for a condition"""
        condition_lower = condition.lower()

        for guideline_id, guideline in self.guidelines.items():
            if condition_lower in guideline.get("title", "").lower():
                return {
                    "guideline_id": guideline_id,
                    **guideline
                }

        return None

    def get_screening_recommendations(self, patient_profile: Dict) -> List[Dict]:
        """Get screening recommendations based on patient profile"""
        recommendations = []
        age = patient_profile.get("age", 0)
        gender = patient_profile.get("gender", "")
        conditions = patient_profile.get("conditions", [])

        # Diabetes screenings
        if any("diabetes" in cond.lower() or "E11" in cond for cond in conditions):
            recommendations.extend([
                {
                    "screening": "Retinopathy exam",
                    "priority": "high",
                    "reason": "Patient has diabetes",
                    "frequency": "Annual"
                },
                {
                    "screening": "Urine microalbumin",
                    "priority": "high",
                    "reason": "Diabetes complication screening",
                    "frequency": "Annual"
                }
            ])

        # Age-based cancer screenings
        if age >= 45:
            recommendations.append({
                "screening": "Colorectal cancer",
                "priority": "medium",
                "reason": f"Age {age}, standard screening age",
                "frequency": "Every 10 years"
            })

        if gender.upper() == "F" and age >= 40:
            recommendations.append({
                "screening": "Mammography",
                "priority": "medium",
                "reason": f"Age {age}, standard screening",
                "frequency": "Annual (age 40-49) or every 2 years (50+)"
            })

        return recommendations


class RAGEngine:
    """Retrieval-Augmented Generation Engine"""

    def __init__(self):
        self.kb = ClinicalKnowledgeBase()
        self.retrieval_cache = {}

    def retrieve_clinical_context(self, query: str, context_type: str = "all") -> Dict[str, Any]:
        """
        Retrieve clinical context for a query

        Args:
            query: Search query
            context_type: "condition", "medication", "interaction", "guideline", "screening", "all"

        Returns:
            Retrieved context with relevance scores
        """
        results = {
            "query": query,
            "context_type": context_type,
            "retrieved_at": datetime.now().isoformat(),
            "results": []
        }

        if context_type in ["condition", "all"]:
            conditions = self.kb.search_conditions(query)
            results["results"].extend([asdict(c) for c in conditions[:3]])

        if context_type in ["medication", "all"]:
            medications = self.kb.search_medications(query)
            results["results"].extend([asdict(m) for m in medications[:3]])

        return results

    def retrieve_for_patient(self, patient_data: Dict) -> Dict[str, Any]:
        """
        Retrieve all relevant clinical context for a patient
        """
        context = {
            "patient_mrn": patient_data.get("mrn"),
            "retrieved_at": datetime.now().isoformat(),
            "condition_profiles": [],
            "medication_profiles": [],
            "interactions": [],
            "guidelines": [],
            "screening_recommendations": []
        }

        # Get condition profiles
        for problem in patient_data.get("problems", []):
            condition_results = self.kb.search_conditions(problem.get("diagnosis", ""))
            if condition_results:
                context["condition_profiles"].append({
                    "diagnosis": problem.get("diagnosis"),
                    "profile": json.loads(condition_results[0].content)
                })

        # Get medication profiles
        medications = [m.get("drugName") for m in patient_data.get("medications", [])]
        for med in medications:
            med_results = self.kb.search_medications(med)
            if med_results:
                context["medication_profiles"].append(json.loads(med_results[0].content))

        # Get interactions
        interactions = self.kb.get_drug_interactions(medications)
        context["interactions"] = interactions

        # Get guidelines
        for problem in patient_data.get("problems", []):
            guideline = self.kb.get_guidelines(problem.get("diagnosis", ""))
            if guideline:
                context["guidelines"].append(guideline)

        # Get screening recommendations
        screening_recs = self.kb.get_screening_recommendations({
            "age": patient_data.get("age"),
            "gender": patient_data.get("gender"),
            "conditions": [p.get("diagnosis") for p in patient_data.get("problems", [])]
        })
        context["screening_recommendations"] = screening_recs

        return context


# Initialize global RAG engine
rag_engine = RAGEngine()


def retrieve_context(query: str, context_type: str = "all") -> Dict[str, Any]:
    """Helper function to retrieve context"""
    return rag_engine.retrieve_clinical_context(query, context_type)


def retrieve_patient_context(patient_data: Dict) -> Dict[str, Any]:
    """Helper function to retrieve patient-specific context"""
    return rag_engine.retrieve_for_patient(patient_data)
