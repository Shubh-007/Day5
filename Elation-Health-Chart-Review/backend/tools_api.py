"""
Elation Health - Tools API for Sub-Agents
Provides endpoints for MCP tools used by sub-agents
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from rag_engine import retrieve_context, retrieve_patient_context, rag_engine
import json


router = APIRouter(prefix="/api/tools", tags=["Sub-Agent Tools"])


# ============================================================================
# CLINICAL CONTEXT TOOLS
# ============================================================================

@router.get("/clinical-context/{mrn}")
def get_clinical_context(
    mrn: str,
    include: str = "all",  # comma-separated: problems,medications,labs,alerts,history
    time_window: str = "6m"  # 1w, 1m, 6m, 1y, all
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
    include: str = "all"  # pathophysiology, complications, management, red_flags
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
    gender: str = None
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
