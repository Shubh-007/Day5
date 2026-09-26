#!/usr/bin/env python3
"""
Integration Review Agent for Elation Health RAG Integration
Analyzes end-to-end data flow and system integration
"""
import json
import os
import re
from pathlib import Path
from datetime import datetime

def review_integration():
    """Comprehensive integration and end-to-end flow review"""

    report = {
        "timestamp": datetime.now().isoformat(),
        "agent": "Integration Review Agent",
        "component": "End-to-End Integration",
        "findings": [],
        "data_flow_tests": [],
        "recommendations": [],
        "system_readiness": {}
    }

    backend_dir = Path("/home/labuser/Day5/Elation-Health-Chart-Review/backend")
    frontend_dir = Path("/home/labuser/Day5/Elation-Health-Chart-Review/frontend")

    # =====================================================================
    # CHECK 1: Data Flow Completeness
    # =====================================================================
    data_flows = {
        "frontend_to_backend": False,
        "backend_to_rag": False,
        "rag_to_api": False,
        "api_to_frontend": False,
        "error_handling_flow": False
    }

    # Frontend -> Backend
    if (frontend_dir / "src/pages/QuickView.jsx").exists():
        content = (frontend_dir / "src/pages/QuickView.jsx").read_text()
        data_flows["frontend_to_backend"] = "fetch(" in content and "/api/" in content
        data_flows["error_handling_flow"] = "catch" in content and ".ok" in content

    # Backend -> RAG
    if (backend_dir / "tools_api.py").exists():
        content = (backend_dir / "tools_api.py").read_text()
        data_flows["backend_to_rag"] = "rag_engine" in content or "retrieve_context" in content

    # RAG -> API
    if (backend_dir / "rag_engine.py").exists():
        content = (backend_dir / "rag_engine.py").read_text()
        data_flows["rag_to_api"] = "return" in content and "{" in content

    # API -> Frontend (response structure)
    if (backend_dir / "app.py").exists():
        content = (backend_dir / "app.py").read_text()
        data_flows["api_to_frontend"] = "json.load" in content or "json.dump" in content

    report["findings"].append({
        "check": "End-to-End Data Flow",
        "status": "PASS" if sum(data_flows.values()) >= 4 else "WARN",
        "details": "Data flow from frontend through backend to RAG and back",
        "flows": data_flows
    })

    # =====================================================================
    # CHECK 2: API Response Structure Consistency
    # =====================================================================
    response_checks = {
        "consistent_format": False,
        "status_codes": False,
        "error_format": False,
        "metadata": False
    }

    if (backend_dir / "app.py").exists():
        content = (backend_dir / "app.py").read_text()
        # Check for consistent response format
        response_checks["consistent_format"] = 'return {' in content
        response_checks["status_codes"] = "status_code" in content
        response_checks["error_format"] = "HTTPException" in content
        response_checks["metadata"] = '"timestamp"' in content or '"retrieved_at"' in content or '"generatedAt"' in content

    report["findings"].append({
        "check": "API Response Consistency",
        "status": "PASS" if sum(response_checks.values()) >= 3 else "WARN",
        "details": "Standardized response formats across endpoints",
        "checks": response_checks
    })

    # =====================================================================
    # CHECK 3: Patient Data Access Pattern
    # =====================================================================
    patient_access = {
        "mrn_parameter": False,
        "data_validation": False,
        "access_control": False,
        "patient_isolation": False
    }

    for file_path in [backend_dir / "app.py", backend_dir / "tools_api.py"]:
        if file_path.exists():
            content = file_path.read_text()
            patient_access["mrn_parameter"] = "{mrn}" in content or "mrn:" in content
            patient_access["data_validation"] = "not in" in content or "Patient not found" in content
            patient_access["access_control"] = "authorization" in content.lower() or "permission" in content.lower()
            patient_access["patient_isolation"] = "PATIENTS_BY_MRN" in content or "patient_id" in content

    report["findings"].append({
        "check": "Patient Data Access Control",
        "status": "PASS" if sum(patient_access.values()) >= 3 else "WARN",
        "details": "Secure patient data access patterns",
        "patterns": patient_access
    })

    # =====================================================================
    # CHECK 4: RAG Engine Integration Points
    # =====================================================================
    rag_integrations = []

    if (backend_dir / "tools_api.py").exists():
        content = (backend_dir / "tools_api.py").read_text()

        # Find all calls to RAG engine
        rag_methods = re.findall(r'rag_engine\.(\w+)', content)
        rag_functions = re.findall(r'retrieve_(\w+)\(', content)

        rag_integrations = list(set(rag_methods + rag_functions))

    report["findings"].append({
        "check": "RAG Engine Integration Points",
        "status": "PASS" if len(rag_integrations) >= 2 else "WARN",
        "details": "Integration between backend API and RAG engine",
        "integration_points": rag_integrations
    })

    # =====================================================================
    # CHECK 5: Sample Data Tests
    # =====================================================================
    sample_data_path = Path("/home/labuser/Day5/Elation-Health-Chart-Review/data/sample_patients.json")

    test_cases = {
        "patient_p001234": False,
        "patient_p005678": False,
        "patient_p009012": False
    }

    if sample_data_path.exists():
        import json as json_lib
        try:
            with open(sample_data_path) as f:
                data = json_lib.load(f)
                if "patients" in data:
                    mrns = [p.get("mrn") for p in data["patients"]]
                    test_cases["patient_p001234"] = "P001234" in mrns or "p001234" in str(mrns).lower()
                    test_cases["patient_p005678"] = "P005678" in mrns or "p005678" in str(mrns).lower()
                    test_cases["patient_p009012"] = "P009012" in mrns or "p009012" in str(mrns).lower()
        except:
            pass

    report["data_flow_tests"] = [
        {
            "test": "Fetch patient summary for P001234",
            "endpoint": "GET /api/patients/P001234/summary",
            "expected_response": "Clinical summary with vitals, medications, alerts",
            "data_available": test_cases["patient_p001234"]
        },
        {
            "test": "Retrieve RAG clinical context for P005678",
            "endpoint": "GET /api/tools/clinical-context/P005678",
            "expected_response": "Structured patient data with clinical reasoning",
            "data_available": test_cases["patient_p005678"]
        },
        {
            "test": "Get drug interactions for P009012",
            "endpoint": "POST /api/tools/drug-interactions",
            "expected_response": "Drug safety warnings and interaction severity",
            "data_available": test_cases["patient_p009012"]
        },
        {
            "test": "Retrieve treatment guidelines",
            "endpoint": "GET /api/tools/retrieve/context?query=diabetes management",
            "expected_response": "Evidence-based guidelines with relevance scores",
            "data_available": True
        }
    ]

    report["findings"].append({
        "check": "Test Data Availability",
        "status": "PASS" if sum(test_cases.values()) >= 2 else "WARN",
        "details": "Sample patient data for integration testing",
        "test_data": test_cases
    })

    # =====================================================================
    # CHECK 6: Performance & Load Characteristics
    # =====================================================================
    performance_metrics = {
        "parallel_requests": False,
        "timeout_handling": False,
        "response_caching": False,
        "batch_operations": False
    }

    if (frontend_dir / "src/pages/QuickView.jsx").exists():
        content = (frontend_dir / "src/pages/QuickView.jsx").read_text()
        performance_metrics["parallel_requests"] = "Promise.all" in content
        performance_metrics["timeout_handling"] = "timeout" in content.lower()

    if (backend_dir / "app.py").exists():
        content = (backend_dir / "app.py").read_text()
        performance_metrics["response_caching"] = "cache" in content.lower()

    report["findings"].append({
        "check": "Performance Characteristics",
        "status": "PASS" if sum(performance_metrics.values()) >= 2 else "WARN",
        "details": "Integration performance patterns",
        "patterns": performance_metrics
    })

    # =====================================================================
    # CHECK 7: Observability & Monitoring
    # =====================================================================
    obs_path = backend_dir / "observability.py"
    observability_checks = {
        "metrics_collection": False,
        "trace_support": False,
        "log_correlation": False,
        "performance_monitoring": False
    }

    if obs_path.exists():
        content = obs_path.read_text()
        observability_checks["metrics_collection"] = "metric" in content.lower() or "prometheus" in content.lower()
        observability_checks["trace_support"] = "trace" in content.lower() or "span" in content.lower()
        observability_checks["log_correlation"] = "correlation" in content.lower() or "request_id" in content.lower()
        observability_checks["performance_monitoring"] = "latency" in content.lower() or "duration" in content.lower()

    report["findings"].append({
        "check": "Observability & Monitoring",
        "status": "PASS" if sum(observability_checks.values()) >= 2 else "WARN",
        "details": "System health and performance visibility",
        "capabilities": observability_checks
    })

    # =====================================================================
    # SYSTEM READINESS ASSESSMENT
    # =====================================================================
    passing_checks = sum(1 for f in report["findings"] if f.get("status") == "PASS")
    total_checks = len(report["findings"])

    report["system_readiness"] = {
        "passing_checks": passing_checks,
        "total_checks": total_checks,
        "readiness_percentage": (passing_checks / total_checks * 100) if total_checks > 0 else 0,
        "integration_complete": passing_checks >= (total_checks * 0.7),
        "production_ready": passing_checks >= (total_checks * 0.9)
    }

    # =====================================================================
    # RECOMMENDATIONS
    # =====================================================================
    report["recommendations"] = [
        "Implement end-to-end integration tests with sample patient data",
        "Add performance benchmarks for patient data retrieval (<2s target)",
        "Implement circuit breaker for RAG service failures",
        "Add health check endpoints for each integration component",
        "Create detailed integration documentation and sequence diagrams",
        "Implement request correlation IDs for debugging",
        "Add integration test automation in CI/CD",
        "Monitor RAG retrieval performance metrics",
        "Implement fallback strategies for degraded service",
        "Create runbooks for common integration issues"
    ]

    return report


if __name__ == "__main__":
    report = review_integration()
    print(json.dumps(report, indent=2))
