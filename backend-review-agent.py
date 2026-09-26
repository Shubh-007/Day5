#!/usr/bin/env python3
"""
Backend Review Agent for Elation Health RAG Integration
Analyzes Python FastAPI backend and RAG engine implementation
"""
import json
import os
import re
from pathlib import Path
from datetime import datetime

def review_backend():
    """Comprehensive backend RAG integration review"""

    report = {
        "timestamp": datetime.now().isoformat(),
        "agent": "Backend Review Agent",
        "component": "FastAPI Backend & RAG Engine",
        "findings": [],
        "metrics": {},
        "recommendations": []
    }

    backend_dir = Path("/home/labuser/Day5/Elation-Health-Chart-Review/backend")

    # =====================================================================
    # CHECK 1: API Endpoints Availability
    # =====================================================================
    tools_api_path = backend_dir / "tools_api.py"
    app_path = backend_dir / "app.py"

    endpoints_found = {}

    if tools_api_path.exists():
        content = tools_api_path.read_text()

        endpoints = re.findall(r'@router\.(\w+)\("([^"]+)"', content)
        for method, path in endpoints:
            endpoints_found[f"{method.upper()} {path}"] = True

    if app_path.exists():
        content = app_path.read_text()
        endpoints = re.findall(r'@app\.(\w+)\("([^"]+)"', content)
        for method, path in endpoints:
            endpoints_found[f"{method.upper()} {path}"] = True

    report["findings"].append({
        "check": "API Endpoints",
        "status": "PASS" if len(endpoints_found) >= 8 else "WARN",
        "details": f"Found {len(endpoints_found)} API endpoints",
        "endpoints": list(endpoints_found.keys())
    })

    # =====================================================================
    # CHECK 2: RAG Engine Integration
    # =====================================================================
    rag_path = backend_dir / "rag_engine.py"
    rag_checks = {
        "kb_system": False,
        "retrieve_context": False,
        "retrieve_patient_context": False,
        "clinical_reasoning": False,
        "safety_validation": False
    }

    if rag_path.exists():
        content = rag_path.read_text()
        rag_checks["kb_system"] = "class KnowledgeBase" in content or "kb" in content
        rag_checks["retrieve_context"] = "def retrieve_context" in content
        rag_checks["retrieve_patient_context"] = "def retrieve_patient_context" in content
        rag_checks["clinical_reasoning"] = "reasoning" in content.lower() or "clinical" in content.lower()
        rag_checks["safety_validation"] = "safety" in content.lower() or "validate" in content.lower()

    report["findings"].append({
        "check": "RAG Engine Components",
        "status": "PASS" if sum(rag_checks.values()) >= 4 else "WARN",
        "details": "RAG engine implementation completeness",
        "components": rag_checks
    })

    # =====================================================================
    # CHECK 3: Error Handling & Validation
    # =====================================================================
    error_handling = {
        "http_exceptions": 0,
        "try_except_blocks": 0,
        "input_validation": 0,
        "logging_calls": 0
    }

    for file_path in [app_path, tools_api_path, rag_path]:
        if file_path.exists():
            content = file_path.read_text()
            error_handling["http_exceptions"] += len(re.findall(r'HTTPException', content))
            error_handling["try_except_blocks"] += len(re.findall(r'try:|except', content))
            error_handling["input_validation"] += len(re.findall(r'if.*not.*:', content))

    report["findings"].append({
        "check": "Error Handling & Validation",
        "status": "PASS" if error_handling["try_except_blocks"] >= 2 else "WARN",
        "details": "Backend error handling patterns",
        "metrics": error_handling
    })

    # =====================================================================
    # CHECK 4: Data Flow & Type Safety
    # =====================================================================
    type_hints = 0
    dict_operations = 0

    if tools_api_path.exists():
        content = tools_api_path.read_text()
        type_hints = len(re.findall(r'->\s*Dict|:\s*str|:\s*List|:\s*Dict', content))
        dict_operations = len(re.findall(r'Dict\[|\.get\(|\.keys\(|\.items\(', content))

    report["findings"].append({
        "check": "Type Safety & Data Structures",
        "status": "PASS" if type_hints >= 5 else "WARN",
        "details": "Type hints and data validation",
        "metrics": {
            "type_hints": type_hints,
            "dict_operations": dict_operations
        }
    })

    # =====================================================================
    # CHECK 5: Clinical Tool Availability
    # =====================================================================
    clinical_tools = {
        "clinical_context": False,
        "drug_interactions": False,
        "condition_profile": False,
        "lab_trends": False,
        "treatment_guidelines": False
    }

    if tools_api_path.exists():
        content = tools_api_path.read_text()
        clinical_tools["clinical_context"] = "clinical-context" in content
        clinical_tools["drug_interactions"] = "drug-interactions" in content
        clinical_tools["condition_profile"] = "condition-profile" in content
        clinical_tools["lab_trends"] = "lab-trends" in content
        clinical_tools["treatment_guidelines"] = "guideline" in content.lower() or "management" in content.lower()

    report["findings"].append({
        "check": "Clinical Tools Implementation",
        "status": "PASS" if sum(clinical_tools.values()) >= 4 else "WARN",
        "details": "Clinical-specific RAG tools",
        "tools": clinical_tools
    })

    # =====================================================================
    # CHECK 6: Performance & Scalability
    # =====================================================================
    performance_checks = {
        "async_support": False,
        "caching_strategy": False,
        "batch_operations": False,
        "pagination": False
    }

    if app_path.exists():
        content = app_path.read_text()
        performance_checks["async_support"] = "async def" in content or "await" in content
        performance_checks["caching_strategy"] = "cache" in content.lower()

    if tools_api_path.exists():
        content = tools_api_path.read_text()
        performance_checks["pagination"] = "skip" in content or "limit" in content

    report["findings"].append({
        "check": "Performance & Scalability",
        "status": "PASS" if sum(performance_checks.values()) >= 2 else "WARN",
        "details": "Backend performance optimizations",
        "patterns": performance_checks
    })

    # =====================================================================
    # RECOMMENDATIONS
    # =====================================================================
    report["recommendations"] = [
        "Implement async/await for RAG retrieval calls",
        "Add caching layer (Redis) for frequently accessed clinical data",
        "Implement request rate limiting to prevent API abuse",
        "Add comprehensive logging/audit trail for clinical data access",
        "Implement data validation middleware for all inputs",
        "Add circuit breaker pattern for external service calls",
        "Create comprehensive API documentation (Swagger/OpenAPI)",
        "Implement health check endpoints for monitoring"
    ]

    return report


if __name__ == "__main__":
    report = review_backend()
    print(json.dumps(report, indent=2))
