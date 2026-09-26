"""
Elation Health - Tools API for Sub-Agents
Provides endpoints for MCP tools used by sub-agents
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from datetime import datetime
from rag_engine import retrieve_context, retrieve_patient_context, rag_engine
from auth import get_current_user, can_access_patient, CurrentUser
from audit_log import log_access
import json


router = APIRouter(prefix="/api/tools", tags=["Sub-Agent Tools"])


# ============================================================================
# CLINICAL CONTEXT TOOLS
# ============================================================================

@router.get("/clinical-context/{mrn}")
def get_clinical_context(
    mrn: str,
    include: str = "all",  # comma-separated: problems,medications,labs,alerts,history
    time_window: str = "6m",  # 1w, 1m, 6m, 1y, all
    current_user: CurrentUser = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Tool: get_clinical_context
    Retrieve rich clinical context for a patient

    Used by: chart-intelligence-engine, safety-validator
    """
    from app import PATIENTS_BY_MRN

    if mrn not in PATIENTS_BY_MRN:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient = PATIENTS_BY_MRN[mrn]

    # RBAC check
    if not can_access_patient(current_user, patient):
        log_access(
            user=current_user.username,
            role=current_user.role,
            action="GET /api/tools/clinical-context/{mrn}",
            mrn=mrn,
            ip="unknown",
            result="denied",
            detail="Patient not in scope"
        )
        raise HTTPException(status_code=404, detail="Patient not found")

    log_access(
        user=current_user.username,
        role=current_user.role,
        action="GET /api/tools/clinical-context/{mrn}",
        mrn=mrn,
        ip="unknown",
        result="success"
    )
    include_fields = [f.strip() for f in include.split(",")] if include != "all" else [
        "problems", "medications", "labs", "alerts", "history"
    ]

    context = {
        "patient_id": mrn,
        "patient_name": patient.get("name"),
        "age": patient.get("age"),
        "gender": patient.get("gender"),
        "retrieved_at": datetime.now().isoformat(),
        "time_window": time_window
    }

    if "problems" in include_fields:
        context["active_problems"] = [
            p for p in patient.get("problems", []) if p.get("status") == "active"
        ]

    if "medications" in include_fields:
        context["medications"] = patient.get("medications", [])

    if "labs" in include_fields:
        context["recent_labs"] = patient.get("recentLabs", [])

    if "alerts" in include_fields:
        context["alerts"] = patient.get("alerts", [])

    if "history" in include_fields:
        context["recent_notes"] = patient.get("recentNotes", [])

    return context


@router.get("/condition-profile/{icd10}")
def get_condition_profile(
    icd10: str,
    include: str = "all",  # pathophysiology, complications, management, red_flags
    current_user: CurrentUser = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Tool: get_condition_profile
    Get clinical profile for a diagnosis

    Used by: chart-intelligence-engine, documentation-assistant
    """
    profile = rag_engine.kb.conditions.get(icd10)

    if not profile:
        raise HTTPException(status_code=404, detail=f"Condition {icd10} not found")

    include_fields = [f.strip() for f in include.split(",")] if include != "all" else [
        "pathophysiology", "complications", "management", "red_flags"
    ]

    response = {
        "icd10": icd10,
        "name": profile.get("name"),
        "description": profile.get("description")
    }

    for field in include_fields:
        if field in profile:
            response[field] = profile[field]

    return response


@router.post("/drug-interactions")
def check_drug_interactions(
    medications: List[str],
    patient_age: int = None,
    kidney_function: str = "normal",  # normal, mild, moderate, severe
    severity_threshold: str = "all"  # critical, major, moderate, minor, all
) -> Dict[str, Any]:
    """
    Tool: get_drug_interaction_context
    Check medication interactions with clinical context

    Used by: safety-validator, chart-intelligence-engine
    """
    interactions_result = rag_engine.kb.get_drug_interactions(medications)

    if severity_threshold != "all":
        severity_map = {
            "critical": ["major"],
            "major": ["major"],
            "moderate": ["major", "moderate"],
            "minor": ["major", "moderate", "minor"]
        }
        threshold_severities = severity_map.get(severity_threshold, [])
        interactions_result["interactions"] = [
            i for i in interactions_result.get("interactions", [])
            if i.get("severity") in threshold_severities
        ]

    # Add patient-specific risk factors
    patient_risks = []
    if kidney_function in ["mild", "moderate", "severe"]:
        patient_risks.append(f"Renal function: {kidney_function} - avoid nephrotoxic drugs")
    if patient_age and patient_age > 75:
        patient_risks.append("Age > 75 - higher risk for drug interactions and side effects")

    interactions_result["patient_specific_risks"] = patient_risks

    return interactions_result


@router.get("/preventive-care/{mrn}")
def get_preventive_care_status(
    mrn: str,
    age: int = None,
    gender: str = None,
    current_user: CurrentUser = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Tool: get_preventive_care_status
    Get overdue preventive care screening status

    Used by: compliance-officer, quality-validator
    """
    from app import PATIENTS_BY_MRN

    if mrn not in PATIENTS_BY_MRN:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient = PATIENTS_BY_MRN[mrn]

    # RBAC check
    if not can_access_patient(current_user, patient):
        log_access(
            user=current_user.username,
            role=current_user.role,
            action="GET /api/tools/preventive-care/{mrn}",
            mrn=mrn,
            ip="unknown",
            result="denied",
            detail="Patient not in scope"
        )
        raise HTTPException(status_code=404, detail="Patient not found")
    age = age or patient.get("age")
    gender = gender or patient.get("gender")
    conditions = [p.get("diagnosis") for p in patient.get("problems", [])]

    screening_recs = rag_engine.kb.get_screening_recommendations({
        "age": age,
        "gender": gender,
        "conditions": conditions
    })

    return {
        "patient_id": mrn,
        "patient_name": patient.get("name"),
        "age": age,
        "gender": gender,
        "overdue_screenings": [s for s in screening_recs if s.get("priority") == "high"],
        "upcoming_screenings": [s for s in screening_recs if s.get("priority") == "medium"],
        "all_recommendations": screening_recs,
        "checked_at": datetime.now().isoformat()
    }


# ============================================================================
# PATIENT DATA TOOLS
# ============================================================================

@router.get("/search-records")
def search_patient_records(
    query: str,
    mrn: str = None,
    search_fields: str = "notes,labs,diagnoses",
    limit: int = 10
) -> Dict[str, Any]:
    """
    Tool: search_patient_records
    Full-text search across patient records

    Used by: chart-intelligence-engine, research-agent
    """
    from app import PATIENTS_BY_MRN

    results = []

    patients_to_search = {mrn: PATIENTS_BY_MRN[mrn]} if mrn and mrn in PATIENTS_BY_MRN else PATIENTS_BY_MRN

    fields = [f.strip() for f in search_fields.split(",")]
    query_lower = query.lower()

    for patient_id, patient in patients_to_search.items():
        matches = []

        if "notes" in fields:
            for note in patient.get("recentNotes", []):
                if query_lower in note.get("summary", "").lower():
                    matches.append({
                        "field": "note",
                        "content": note.get("summary")[:200],
                        "date": note.get("date")
                    })

        if "labs" in fields:
            for lab in patient.get("recentLabs", []):
                if query_lower in lab.get("testName", "").lower():
                    matches.append({
                        "field": "lab",
                        "content": f"{lab.get('testName')}: {lab.get('value')} {lab.get('unit')}",
                        "date": lab.get("date")
                    })

        if "diagnoses" in fields:
            for problem in patient.get("problems", []):
                if query_lower in problem.get("diagnosis", "").lower():
                    matches.append({
                        "field": "diagnosis",
                        "content": problem.get("diagnosis"),
                        "status": problem.get("status")
                    })

        if matches:
            results.append({
                "patient_mrn": patient_id,
                "patient_name": patient.get("name"),
                "matches": matches[:limit]
            })

    return {
        "query": query,
        "total_results": len(results),
        "results": results,
        "searched_at": datetime.now().isoformat()
    }


@router.get("/lab-trends/{mrn}/{test_code}")
def get_lab_trend_analysis(
    mrn: str,
    test_code: str,
    time_window: str = "6m",
    include_interpretation: bool = True
) -> Dict[str, Any]:
    """
    Tool: get_lab_trend_analysis
    Analyze lab value trends over time

    Used by: analytics-engine, quality-validator
    """
    from app import PATIENTS_BY_MRN

    if mrn not in PATIENTS_BY_MRN:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient = PATIENTS_BY_MRN[mrn]
    labs = patient.get("recentLabs", [])

    # Find matching labs
    matching_labs = [l for l in labs if test_code.lower() in l.get("testName", "").lower()]

    if not matching_labs:
        raise HTTPException(status_code=404, detail=f"Lab test {test_code} not found")

    # Determine trend
    if len(matching_labs) > 1:
        recent = float(matching_labs[0].get("value", 0))
        older = float(matching_labs[-1].get("value", 0))
        if recent > older:
            trend = "worsening"
        elif recent < older:
            trend = "improving"
        else:
            trend = "stable"
    else:
        trend = "insufficient_data"

    interpretation = ""
    if include_interpretation:
        if matching_labs[0].get("abnormal"):
            interpretation = f"ABNORMAL: {test_code} is above/below normal range"
        else:
            interpretation = f"NORMAL: {test_code} is within normal range"

    return {
        "patient_mrn": mrn,
        "test_name": test_code,
        "time_window": time_window,
        "values": matching_labs,
        "trend": trend,
        "interpretation": interpretation,
        "analyzed_at": datetime.now().isoformat()
    }


# ============================================================================
# ALERT & SAFETY TOOLS
# ============================================================================

@router.get("/safety-alerts/{mrn}")
def check_safety_alerts(
    mrn: str,
    alert_types: str = "all",  # medication, allergy, lab, screening, contraindication
    severity: str = "all"  # critical, high, medium, all
) -> Dict[str, Any]:
    """
    Tool: check_safety_alerts
    Get all active safety alerts for a patient

    Used by: safety-validator, compliance-officer
    """
    from app import PATIENTS_BY_MRN

    if mrn not in PATIENTS_BY_MRN:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient = PATIENTS_BY_MRN[mrn]
    alerts = patient.get("alerts", [])

    types = [t.strip() for t in alert_types.split(",")] if alert_types != "all" else []
    all_alerts = alerts if not types else [a for a in alerts if a.get("type") in types]

    if severity != "all":
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        all_alerts = [a for a in all_alerts if severity_order.get(a.get("severity"), 4) <= severity_order.get(severity, 4)]

    return {
        "patient_mrn": mrn,
        "patient_name": patient.get("name"),
        "total_alerts": len(all_alerts),
        "critical_alerts": [a for a in all_alerts if a.get("severity") == "critical" or a.get("severity") == "high"],
        "high_alerts": [a for a in all_alerts if a.get("severity") == "high"],
        "medium_alerts": [a for a in all_alerts if a.get("severity") == "medium"],
        "all_alerts": all_alerts,
        "checked_at": datetime.now().isoformat()
    }


@router.post("/create-alert")
def create_clinical_alert(
    patient_mrn: str,
    alert_type: str,
    severity: str,
    clinical_reason: str,
    recommended_action: str,
    escalate_to: List[str] = None
) -> Dict[str, Any]:
    """
    Tool: create_clinical_alert
    Flag a clinical concern for review

    Used by: safety-validator, compliance-officer
    """
    return {
        "status": "created",
        "alert_id": f"ALR_{patient_mrn}_{hash(clinical_reason) % 10000}",
        "patient_mrn": patient_mrn,
        "alert_type": alert_type,
        "severity": severity,
        "clinical_reason": clinical_reason,
        "recommended_action": recommended_action,
        "escalate_to": escalate_to or [],
        "created_at": datetime.now().isoformat(),
        "status_message": "Alert created and queued for review"
    }


# ============================================================================
# RAG RETRIEVAL TOOLS
# ============================================================================

@router.get("/retrieve/context")
def retrieve_clinical_context_tool(
    query: str,
    context_type: str = "all"  # condition, medication, interaction, guideline, screening, all
) -> Dict[str, Any]:
    """
    Tool: retrieve_clinical_context
    Use RAG engine to retrieve relevant clinical information

    Used by: chart-intelligence-engine, documentation-assistant, any sub-agent
    """
    return retrieve_context(query, context_type)


@router.post("/chat/rag")
def rag_chatbot(
    patient_mrn: str,
    query: str,
    conversation_history: List[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Conversational RAG chatbot for clinical Q&A
    Allows clinicians to ask questions about patient data, RAG knowledge, etc.

    Used by: Frontend chatbot interface
    """
    from app import PATIENTS_BY_MRN

    if patient_mrn not in PATIENTS_BY_MRN:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient = PATIENTS_BY_MRN[patient_mrn]

    # Context for the RAG query
    patient_context = get_clinical_context(patient_mrn, include="all")

    # Retrieve relevant clinical information based on the query
    query_lower = query.lower()

    response_text = ""
    sources = []
    confidence = 0.0

    # Detect intent and retrieve relevant information
    if any(keyword in query_lower for keyword in ["drug", "medication", "interaction", "side effect"]):
        # Drug interaction query
        medications = [m["drugName"] for m in patient.get("medications", [])]
        if medications:
            interactions = rag_engine.kb.get_drug_interactions(medications)
            response_text = format_drug_interaction_response(medications, interactions)
            sources = ["Drug Interaction Database", "Clinical Knowledge Base"]
            confidence = 0.85
        else:
            response_text = "This patient doesn't have any current medications on file."
            confidence = 0.95

    elif any(keyword in query_lower for keyword in ["lab", "result", "value", "abnormal", "trend"]):
        # Lab query
        labs = patient.get("recentLabs", [])
        abnormal_labs = [l for l in labs if l.get("abnormal")]

        if abnormal_labs:
            response_text = format_lab_response(abnormal_labs)
            sources = ["Laboratory Results", "Clinical Standards"]
            confidence = 0.90
        else:
            response_text = "All recent lab values are within normal ranges for this patient."
            confidence = 0.95

    elif any(keyword in query_lower for keyword in ["condition", "diagnosis", "problem", "disease", "guideline"]):
        # Clinical guideline query
        conditions = [p.get("diagnosis") for p in patient.get("problems", [])]

        if conditions:
            guideline_text = format_guidelines_response(conditions, rag_engine.kb)
            response_text = guideline_text
            sources = ["Clinical Guidelines", "Evidence-Based Medicine", "ICD-10 Database"]
            confidence = 0.82
        else:
            response_text = "No active conditions on file for this patient."
            confidence = 0.95

    elif any(keyword in query_lower for keyword in ["allergy", "contraindication", "alert", "warning"]):
        # Safety/alert query
        alerts = patient.get("alerts", [])
        allergies = patient.get("allergies", [])

        if alerts or allergies:
            response_text = format_safety_response(alerts, allergies)
            sources = ["Patient Safety Database", "Clinical Alerts", "Allergy Records"]
            confidence = 0.90
        else:
            response_text = "No current safety alerts or known allergies for this patient."
            confidence = 0.95

    elif any(keyword in query_lower for keyword in ["preventive", "screening", "vaccine", "check-up"]):
        # Preventive care query
        age = patient.get("age")
        gender = patient.get("gender")
        conditions = [p.get("diagnosis") for p in patient.get("problems", [])]

        screening_recs = rag_engine.kb.get_screening_recommendations({
            "age": age,
            "gender": gender,
            "conditions": conditions
        })

        if screening_recs:
            overdue = [s for s in screening_recs if s.get("priority") == "high"]
            response_text = format_preventive_care_response(overdue, screening_recs)
            sources = ["Preventive Care Guidelines", "Screening Protocols"]
            confidence = 0.85
        else:
            response_text = "No preventive care recommendations at this time."
            confidence = 0.80

    elif any(keyword in query_lower for keyword in ["vital", "blood pressure", "heart rate", "weight", "bmi"]):
        # Vitals query
        vitals = patient.get("vitals", [])
        if vitals:
            latest_vitals = vitals[-1] if vitals else {}
            response_text = format_vitals_response(latest_vitals)
            sources = ["Vital Signs Record"]
            confidence = 0.95
        else:
            response_text = "No vital signs recorded for this patient."
            confidence = 0.95

    else:
        # General query - retrieve context
        retrieved = retrieve_context(query, "all")
        response_text = format_general_response(query, retrieved, patient)
        sources = ["Clinical Knowledge Base", "Patient Records"]
        confidence = 0.75

    return {
        "patient_mrn": patient_mrn,
        "query": query,
        "response": response_text,
        "sources": sources,
        "confidence": confidence,
        "timestamp": datetime.now().isoformat()
    }


@router.post("/retrieve/patient")
def retrieve_patient_context_tool(patient_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Tool: retrieve_patient_context
    Retrieve all relevant clinical context for a patient using RAG

    Used by: chart-intelligence-engine, compliance-officer
    """
    return retrieve_patient_context(patient_data)


# ============================================================================
# HELPER ENDPOINTS
# ============================================================================

@router.get("/tools/available")
def list_available_tools() -> Dict[str, Any]:
    """List all available tools for sub-agents"""
    return {
        "clinical_context_tools": [
            "get_clinical_context",
            "get_condition_profile",
            "check_drug_interactions",
            "get_preventive_care_status"
        ],
        "patient_data_tools": [
            "search_patient_records",
            "get_lab_trend_analysis"
        ],
        "alert_safety_tools": [
            "check_safety_alerts",
            "create_clinical_alert"
        ],
        "rag_retrieval_tools": [
            "retrieve_clinical_context",
            "retrieve_patient_context"
        ],
        "documentation_tools": [
            "generate_documentation_template",
            "validate_documentation"
        ],
        "analytics_tools": [
            "get_quality_metrics",
            "analyze_alert_patterns"
        ]
    }


@router.get("/tools/definitions")
def get_tool_definitions() -> Dict[str, Any]:
    """Get detailed definitions of all available tools"""
    return {
        "tools": [
            {
                "name": "get_clinical_context",
                "category": "clinical_context",
                "description": "Retrieve rich clinical context for a patient",
                "endpoint": "/api/tools/clinical-context/{mrn}",
                "method": "GET",
                "parameters": {
                    "mrn": "Patient MRN",
                    "include": "Comma-separated fields to include",
                    "time_window": "Time period for data"
                }
            },
            {
                "name": "get_condition_profile",
                "category": "clinical_context",
                "description": "Get clinical profile for a diagnosis",
                "endpoint": "/api/tools/condition-profile/{icd10}",
                "method": "GET"
            },
            {
                "name": "check_drug_interactions",
                "category": "alert_safety",
                "description": "Check medication interactions",
                "endpoint": "/api/tools/drug-interactions",
                "method": "POST"
            },
            {
                "name": "retrieve_clinical_context",
                "category": "rag_retrieval",
                "description": "Use RAG to retrieve clinical information",
                "endpoint": "/api/tools/retrieve/context",
                "method": "GET"
            }
        ]
    }


from datetime import datetime


# ============================================================================
# CHATBOT RESPONSE FORMATTERS
# ============================================================================

def format_drug_interaction_response(medications: List[str], interactions: Dict) -> str:
    """Format drug interaction data for chatbot response"""
    total = interactions.get("total_interactions", 0)

    if total == 0:
        return f"Good news! No significant drug interactions detected for {', '.join(medications)}."

    response = f"⚠️ Found {total} drug interaction(s):\n\n"

    for interaction in interactions.get("interactions", [])[:3]:
        severity = interaction.get("severity", "moderate").upper()
        drug1 = interaction.get("drug1", "")
        drug2 = interaction.get("drug2", "")
        response += f"• **{drug1}** ↔️ **{drug2}** [{severity}]\n"
        response += f"  {interaction.get('interaction_type', 'May interact')}\n"

    if total > 3:
        response += f"\n...and {total - 3} more interaction(s)."

    return response


def format_lab_response(abnormal_labs: List[Dict]) -> str:
    """Format lab results for chatbot response"""
    response = f"⚠️ {len(abnormal_labs)} abnormal lab value(s):\n\n"

    for lab in abnormal_labs[:5]:
        test_name = lab.get("testName", "Unknown test")
        value = lab.get("value", "N/A")
        unit = lab.get("unit", "")
        normal_range = lab.get("normalRange", "see reference range")

        response += f"• **{test_name}**: {value} {unit}\n"
        response += f"  Normal: {normal_range}\n"

    return response


def format_guidelines_response(conditions: List[str], kb) -> str:
    """Format clinical guidelines for chatbot response"""
    if not conditions:
        return "No active conditions to provide guidelines for."

    response = "📚 Clinical Guidelines:\n\n"

    for condition in conditions[:3]:
        # Try to find condition in KB
        condition_data = kb.conditions.get(condition)

        if condition_data:
            response += f"**{condition_data.get('name', condition)}**\n"
            response += f"Management: {', '.join(condition_data.get('management', ['See specialist']))}\n"
            response += f"Target: {condition_data.get('target_bp', condition_data.get('target', 'Follow protocol'))}\n"
            response += f"⚠️ Red flags: {', '.join(condition_data.get('red_flags', ['See documentation'])[:2])}\n\n"
        else:
            response += f"**{condition}** - Please consult clinical references for latest guidelines.\n\n"

    return response


def format_safety_response(alerts: List[Dict], allergies: List[Dict]) -> str:
    """Format safety alerts and allergies for chatbot response"""
    response = "🚨 Safety Information:\n\n"

    if alerts:
        response += "**Active Alerts:**\n"
        for alert in alerts[:3]:
            severity = alert.get("severity", "medium").upper()
            response += f"• [{severity}] {alert.get('message', 'Alert')}\n"
        response += "\n"

    if allergies:
        response += "**Known Allergies:**\n"
        for allergy in allergies[:3]:
            allergen = allergy.get("allergen", "Unknown")
            reaction = allergy.get("reactionType", "Unknown")
            severity = allergy.get("severity", "moderate")
            response += f"• **{allergen}** → {reaction} ({severity})\n"

    return response


def format_preventive_care_response(overdue: List[Dict], all_recs: List[Dict]) -> str:
    """Format preventive care recommendations for chatbot response"""
    response = "🏥 Preventive Care Status:\n\n"

    if overdue:
        response += f"⚠️ **Overdue ({len(overdue)}):**\n"
        for rec in overdue[:3]:
            response += f"• {rec.get('name', 'Screening')} (due {rec.get('due_date', 'now')})\n"
        response += "\n"

    upcoming = [r for r in all_recs if r.get("priority") == "medium"]
    if upcoming:
        response += f"📅 **Upcoming ({len(upcoming)}):**\n"
        for rec in upcoming[:3]:
            response += f"• {rec.get('name', 'Screening')} (due {rec.get('due_date', 'soon')})\n"

    return response


def format_vitals_response(vitals: Dict) -> str:
    """Format vital signs for chatbot response"""
    if not vitals:
        return "No vital signs available."

    response = "📊 Current Vitals:\n\n"
    response += f"• BP: {vitals.get('bloodPressure', 'N/A')}\n"
    response += f"• HR: {vitals.get('heartRate', 'N/A')} bpm\n"
    response += f"• Weight: {vitals.get('weight', 'N/A')} lbs\n"
    response += f"• BMI: {vitals.get('bmi', 'N/A')}\n"

    return response


def format_general_response(query: str, retrieved: Dict, patient: Dict) -> str:
    """Format general query response"""
    response = f"Based on your question about '{query}', here's what I found:\n\n"

    results = retrieved.get("results", [])

    if results:
        for item in results[:3]:
            response += f"• {item.get('content', 'Information found')[:100]}...\n"
    else:
        response += f"I searched the clinical knowledge base but didn't find specific information matching '{query}'.\n"
        response += "Please try asking about:\n"
        response += "- Medications and drug interactions\n"
        response += "- Lab values and trends\n"
        response += "- Clinical conditions and guidelines\n"
        response += "- Preventive care and screening\n"

    return response
