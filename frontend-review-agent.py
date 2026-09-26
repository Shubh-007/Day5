#!/usr/bin/env python3
"""
Frontend Review Agent for Elation Health RAG Integration
Analyzes React/JSX integration with RAG endpoints
"""
import json
import os
import re
from pathlib import Path
from datetime import datetime

def review_frontend():
    """Comprehensive frontend RAG integration review"""

    report = {
        "timestamp": datetime.now().isoformat(),
        "agent": "Frontend Review Agent",
        "component": "React Frontend Integration",
        "findings": [],
        "metrics": {},
        "recommendations": []
    }

    frontend_dir = Path("/home/labuser/Day5/Elation-Health-Chart-Review/frontend")
    quickview_path = frontend_dir / "src/pages/QuickView.jsx"

    # =====================================================================
    # CHECK 1: RAG Endpoint Integration
    # =====================================================================
    rag_endpoints_found = set()
    if quickview_path.exists():
        content = quickview_path.read_text()

        # Find all fetch calls to RAG endpoints
        rag_patterns = [
            r'/api/tools/clinical-context/',
            r'/api/tools/drug-interactions',
            r'/api/tools/retrieve/context',
            r'/api/tools/condition-profile/',
            r'/api/tools/lab-trends/'
        ]

        for pattern in rag_patterns:
            if re.search(pattern, content):
                rag_endpoints_found.add(pattern)

        report["findings"].append({
            "check": "RAG Endpoint Integration",
            "status": "PASS" if len(rag_endpoints_found) >= 3 else "WARN",
            "details": f"Found {len(rag_endpoints_found)} RAG endpoints called from frontend",
            "endpoints": list(rag_endpoints_found)
        })

        # =====================================================================
        # CHECK 2: Error Handling
        # =====================================================================
        error_handling_checks = {
            "try_catch_blocks": len(re.findall(r'try\s*\{', content)),
            "error_state": "error" in content and "setError" in content,
            "loading_state": "loading" in content and "setLoading" in content,
            "null_checks": len(re.findall(r'&&\s*\w+\.|if\s*\(\s*\w+\s*\)', content))
        }

        report["findings"].append({
            "check": "Error Handling",
            "status": "PASS" if error_handling_checks["try_catch_blocks"] >= 1 else "WARN",
            "details": "Error handling implementation",
            "metrics": error_handling_checks
        })

        # =====================================================================
        # CHECK 3: UI Components for RAG
        # =====================================================================
        rag_components = {
            "drug_safety_card": "Drug Safety Check (RAG)" in content,
            "clinical_guidelines_card": "Clinical Guidelines (RAG)" in content,
            "clinical_context_card": "Clinical Context (RAG)" in content,
            "rag_badges": len(re.findall(r'rag-card', content))
        }

        report["findings"].append({
            "check": "RAG UI Components",
            "status": "PASS" if sum(rag_components.values()) >= 3 else "WARN",
            "details": "RAG-specific UI components rendering",
            "components": rag_components
        })

        # =====================================================================
        # CHECK 4: Performance Optimization
        # =====================================================================
        performance_checks = {
            "promise_all": "Promise.all" in content,
            "parallel_fetches": len(re.findall(r'Promise\.all', content)) > 0,
            "slice_for_pagination": ".slice(" in content,
            "lazy_loading": "useEffect" in content
        }

        report["findings"].append({
            "check": "Performance Optimization",
            "status": "PASS" if sum(performance_checks.values()) >= 3 else "WARN",
            "details": "Frontend performance patterns",
            "optimizations": performance_checks
        })

        # =====================================================================
        # CHECK 5: Data Flow & State Management
        # =====================================================================
        state_variables = re.findall(r'setState\((\w+)\)', content)
        state_setters = set(re.findall(r'set(\w+)', content))

        report["findings"].append({
            "check": "State Management",
            "status": "PASS" if len(state_setters) >= 5 else "WARN",
            "details": f"State management with {len(state_setters)} state variables",
            "state_vars": sorted(state_setters)
        })

        # =====================================================================
        # CHECK 6: Clinical Data Display
        # =====================================================================
        clinical_elements = {
            "vitals_display": "vitals" in content and "vital-value" in content,
            "medications_list": "medications" in content,
            "problems_display": "problems" in content or "conditions" in content,
            "alerts_display": "alerts" in content,
            "lab_values": "abnormal" in content or "labs" in content
        }

        report["findings"].append({
            "check": "Clinical Data Display",
            "status": "PASS" if sum(clinical_elements.values()) >= 4 else "WARN",
            "details": "Clinical data elements rendered to UI",
            "elements": clinical_elements
        })

    else:
        report["findings"].append({
            "check": "File Check",
            "status": "FAIL",
            "details": f"QuickView.jsx not found at {quickview_path}"
        })

    # =====================================================================
    # RECOMMENDATIONS
    # =====================================================================
    report["recommendations"] = [
        "Add loading indicators for each RAG endpoint fetch",
        "Implement retry logic for failed RAG requests",
        "Add caching for frequently requested RAG data",
        "Implement request deduplication to prevent duplicate API calls",
        "Add unit tests for RAG endpoint integration",
        "Implement accessibility features (ARIA labels) for RAG sections",
        "Add telemetry/analytics to track RAG feature usage"
    ]

    return report


if __name__ == "__main__":
    report = review_frontend()
    print(json.dumps(report, indent=2))
