from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

from auth import get_current_user, can_access_patient, CurrentUser, authenticate_user, create_access_token
from crypto_store import load_encrypted_json
from audit_log import log_access
from tools_api import router as tools_router

app = FastAPI(
    title="Elation Health Chart Review API",
    description="AI-powered clinical summarization with RAG engine and sub-agent tools"
)

# Enable CORS for frontend with restricted origins
CORS_ALLOWED_ORIGIN = os.environ.get("CORS_ALLOWED_ORIGIN", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[CORS_ALLOWED_ORIGIN],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

# Include tools API router
app.include_router(tools_router)

# Load encrypted patient data
ENC_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sample_patients.json.enc")
PATIENT_DATA = load_encrypted_json(ENC_DATA_PATH)

# Index patients by MRN for quick lookup
PATIENTS_BY_MRN = {p["mrn"]: p for p in PATIENT_DATA["patients"]}


def generate_summary(patient):
    """Generate clinical summary for pre-visit preparation"""

    # Problem list summary
    active_problems = [p for p in patient["problems"] if p["status"] == "active"]
    problem_summary = ", ".join([f"{p['diagnosis']}" for p in active_problems])

    # Recent labs with abnormalities
    abnormal_labs = [l for l in patient["recentLabs"] if l.get("abnormal")]
    lab_summary = []
    for lab in abnormal_labs:
        lab_summary.append(f"{lab['testName']}: {lab['value']} {lab['unit']} (abnormal)")

    # Medications with potential issues
    med_summary = [f"{m['drugName']} {m['dose']}{m['unit']}" for m in patient["medications"]]

    # Recent changes since last visit
    recent_changes = []
    if patient["recentNotes"]:
        latest_note = patient["recentNotes"][0]
        recent_changes.append(latest_note["summary"][:150] + "...")

    # Alerts
    high_priority_alerts = [a for a in patient["alerts"] if a["severity"] in ["high", "medium"]]

    return {
        "patientMRN": patient["mrn"],
        "patientName": patient["name"],
        "age": patient["age"],
        "gender": patient["gender"],
        "lastVisit": patient["lastVisit"],
        "nextVisit": patient["nextVisit"],
        "primaryCareProvider": patient["primaryCareProvider"],
        "problemList": problem_summary,
        "activeConditions": [p["diagnosis"] for p in active_problems],
        "currentMedications": med_summary,
        "medicationCount": len(patient["medications"]),
        "abnormalLabs": lab_summary,
        "recentChanges": recent_changes,
        "alerts": high_priority_alerts,
        "vitals": patient["vitals"][-1] if patient["vitals"] else None,
        "nextVisitIn": calculate_days_until(patient["nextVisit"]),
        "timeSinceLastVisit": calculate_days_since(patient["lastVisit"]),
    }


def calculate_days_until(date_str):
    """Calculate days until a date"""
    target = datetime.strptime(date_str, "%Y-%m-%d")
    today = datetime.now()
    delta = target - today
    if delta.days < 0:
        return f"{abs(delta.days)} days overdue"
    elif delta.days == 0:
        return "Today"
    elif delta.days == 1:
        return "Tomorrow"
    else:
        return f"In {delta.days} days"


def calculate_days_since(date_str):
    """Calculate days since a date"""
    past = datetime.strptime(date_str, "%Y-%m-%d")
    today = datetime.now()
    delta = today - past
    if delta.days == 0:
        return "Today"
    elif delta.days == 1:
        return "1 day ago"
    else:
        return f"{delta.days} days ago"


@app.get("/")
def root():
    return {
        "service": "Elation Health Chart Review API",
        "version": "0.2.0",
        "status": "running",
        "features": [
            "Clinical summarization",
            "Pre-visit preparation",
            "RAG-powered clinical knowledge retrieval",
            "Sub-agent tools for AI automation",
            "Alert management & safety validation",
            "Secure authentication & authorization",
            "PHI encryption at rest",
            "Comprehensive audit logging"
        ],
        "endpoints": {
            "login": "/api/auth/login",
            "dashboard": "/api/dashboard",
            "patient_summary": "/api/patients/{mrn}/summary",
            "patient_details": "/api/patients/{mrn}",
            "sub_agent_tools": "/api/tools",
            "rag_retrieval": "/api/tools/retrieve/context",
            "available_tools": "/api/tools/available",
            "tool_definitions": "/api/tools/definitions"
        }
    }


@app.post("/api/auth/login")
def login(username: str, password: str):
    """Authenticate a user and return a JWT access token."""
    user = authenticate_user(username, password)
    if not user:
        log_access(
            user=username,
            role="unknown",
            action="LOGIN_FAILED",
            mrn=None,
            ip="unknown",
            result="denied",
            detail="Invalid credentials"
        )
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        username=user.username,
        role=user.role,
        display_name=user.display_name
    )

    log_access(
        user=user.username,
        role=user.role,
        action="LOGIN",
        mrn=None,
        ip="unknown",
        result="success"
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
        "display_name": user.display_name
    }


@app.get("/api/patients")
def list_patients(current_user: CurrentUser = Depends(get_current_user)):
    """List patients accessible to the current user"""
    # Filter patients based on user role/RBAC
    accessible_patients = [p for p in PATIENT_DATA["patients"] if can_access_patient(current_user, p)]

    log_access(
        user=current_user.username,
        role=current_user.role,
        action="LIST_PATIENTS",
        mrn=None,
        ip="unknown",
        result="success",
        detail=f"{len(accessible_patients)} patients"
    )

    return {
        "count": len(accessible_patients),
        "patients": [
            {
                "mrn": p["mrn"],
                "name": p["name"],
                "age": p["age"],
                "gender": p["gender"],
                "lastVisit": p["lastVisit"],
                "nextVisit": p["nextVisit"],
                "provider": p["primaryCareProvider"],
            }
            for p in accessible_patients
        ]
    }


@app.get("/api/patients/{mrn}/summary")
def get_patient_summary(mrn: str, current_user: CurrentUser = Depends(get_current_user)):
    """Get AI-generated pre-visit summary for a patient"""
    if mrn not in PATIENTS_BY_MRN:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient = PATIENTS_BY_MRN[mrn]

    # RBAC check: 404 for both "not found" and "not yours" to avoid MRN leakage
    if not can_access_patient(current_user, patient):
        log_access(
            user=current_user.username,
            role=current_user.role,
            action="GET /api/patients/{mrn}/summary",
            mrn=mrn,
            ip="unknown",
            result="denied",
            detail="Patient not in scope"
        )
        raise HTTPException(status_code=404, detail="Patient not found")

    log_access(
        user=current_user.username,
        role=current_user.role,
        action="GET /api/patients/{mrn}/summary",
        mrn=mrn,
        ip="unknown",
        result="success"
    )

    return generate_summary(patient)


@app.get("/api/patients/{mrn}")
def get_patient_details(mrn: str, current_user: CurrentUser = Depends(get_current_user)):
    """Get complete patient chart"""
    if mrn not in PATIENTS_BY_MRN:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient = PATIENTS_BY_MRN[mrn]

    # RBAC check: 404 for both "not found" and "not yours" to avoid MRN leakage
    if not can_access_patient(current_user, patient):
        log_access(
            user=current_user.username,
            role=current_user.role,
            action="GET /api/patients/{mrn}",
            mrn=mrn,
            ip="unknown",
            result="denied",
            detail="Patient not in scope"
        )
        raise HTTPException(status_code=404, detail="Patient not found")

    log_access(
        user=current_user.username,
        role=current_user.role,
        action="GET /api/patients/{mrn}",
        mrn=mrn,
        ip="unknown",
        result="success"
    )

    return patient


@app.get("/api/dashboard")
def get_dashboard(current_user: CurrentUser = Depends(get_current_user)):
    """Get dashboard with patient summaries accessible to current user"""
    # Filter patients based on user role/RBAC
    accessible_patients = [p for p in PATIENT_DATA["patients"] if can_access_patient(current_user, p)]

    summaries = []
    for patient in accessible_patients:
        summary = generate_summary(patient)
        summaries.append(summary)

    # Sort by next visit time
    summaries.sort(key=lambda s: s["nextVisitIn"])

    log_access(
        user=current_user.username,
        role=current_user.role,
        action="GET /api/dashboard",
        mrn=None,
        ip="unknown",
        result="success",
        detail=f"{len(summaries)} patients"
    )

    return {
        "totalPatients": len(summaries),
        "patients": summaries,
        "generatedAt": datetime.now().isoformat(),
    }


@app.get("/api/alerts")
def get_all_alerts(current_user: CurrentUser = Depends(get_current_user)):
    """Get critical alerts for patients accessible to current user"""
    # Filter patients based on user role/RBAC
    accessible_patients = [p for p in PATIENT_DATA["patients"] if can_access_patient(current_user, p)]

    all_alerts = []
    for patient in accessible_patients:
        for alert in patient["alerts"]:
            all_alerts.append({
                "patientMRN": patient["mrn"],
                "patientName": patient["name"],
                **alert
            })

    # Sort by severity
    severity_order = {"high": 0, "medium": 1, "low": 2}
    all_alerts.sort(key=lambda a: severity_order.get(a["severity"], 3))

    log_access(
        user=current_user.username,
        role=current_user.role,
        action="GET /api/alerts",
        mrn=None,
        ip="unknown",
        result="success",
        detail=f"{len(all_alerts)} alerts"
    )

    return {
        "totalAlerts": len(all_alerts),
        "alerts": all_alerts
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
