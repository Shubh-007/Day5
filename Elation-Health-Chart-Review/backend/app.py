from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from datetime import datetime
from typing import Optional

app = FastAPI(title="Elation Health Chart Review API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load sample patient data
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sample_patients.json")
with open(DATA_PATH, "r") as f:
    PATIENT_DATA = json.load(f)

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
        "version": "0.1.0",
        "status": "running",
        "endpoints": {
            "patients": "/api/patients",
            "patient_summary": "/api/patients/{mrn}/summary",
            "patient_details": "/api/patients/{mrn}",
            "dashboard": "/api/dashboard",
        }
    }


@app.get("/api/patients")
def list_patients():
    """List all patients with basic info"""
    return {
        "count": len(PATIENT_DATA["patients"]),
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
            for p in PATIENT_DATA["patients"]
        ]
    }


@app.get("/api/patients/{mrn}/summary")
def get_patient_summary(mrn: str):
    """Get AI-generated pre-visit summary for a patient"""
    if mrn not in PATIENTS_BY_MRN:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient = PATIENTS_BY_MRN[mrn]
    return generate_summary(patient)


@app.get("/api/patients/{mrn}")
def get_patient_details(mrn: str):
    """Get complete patient chart"""
    if mrn not in PATIENTS_BY_MRN:
        raise HTTPException(status_code=404, detail="Patient not found")

    return PATIENTS_BY_MRN[mrn]


@app.get("/api/dashboard")
def get_dashboard():
    """Get dashboard with all patient summaries (like a clinician's daily schedule)"""
    summaries = []
    for patient in PATIENT_DATA["patients"]:
        summary = generate_summary(patient)
        summaries.append(summary)

    # Sort by next visit time
    summaries.sort(key=lambda s: s["nextVisitIn"])

    return {
        "totalPatients": len(summaries),
        "patients": summaries,
        "generatedAt": datetime.now().isoformat(),
    }


@app.get("/api/alerts")
def get_all_alerts():
    """Get all critical alerts across all patients"""
    all_alerts = []
    for patient in PATIENT_DATA["patients"]:
        for alert in patient["alerts"]:
            all_alerts.append({
                "patientMRN": patient["mrn"],
                "patientName": patient["name"],
                **alert
            })

    # Sort by severity
    severity_order = {"high": 0, "medium": 1, "low": 2}
    all_alerts.sort(key=lambda a: severity_order.get(a["severity"], 3))

    return {
        "totalAlerts": len(all_alerts),
        "alerts": all_alerts
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
