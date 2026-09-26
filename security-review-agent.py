#!/usr/bin/env python3
"""
Security & Vulnerability Review Agent for Elation Health RAG Integration
Analyzes security, HIPAA compliance, and data protection
"""
import json
import os
import re
from pathlib import Path
from datetime import datetime

def review_security():
    """Comprehensive security and vulnerability review"""

    report = {
        "timestamp": datetime.now().isoformat(),
        "agent": "Security & Vulnerability Review Agent",
        "component": "Security & Compliance",
        "findings": [],
        "vulnerabilities": [],
        "recommendations": []
    }

    backend_dir = Path("/home/labuser/Day5/Elation-Health-Chart-Review/backend")
    frontend_dir = Path("/home/labuser/Day5/Elation-Health-Chart-Review/frontend")

    # =====================================================================
    # CHECK 1: CORS Configuration
    # =====================================================================
    cors_issues = []
    if (backend_dir / "app.py").exists():
        content = (backend_dir / "app.py").read_text()

        if 'allow_origins=["*"]' in content:
            cors_issues.append({
                "severity": "HIGH",
                "issue": "CORS allows all origins (*)",
                "risk": "Potential for unauthorized cross-origin requests",
                "fix": 'Restrict to specific frontend domain'
            })

    report["findings"].append({
        "check": "CORS Security",
        "status": "FAIL" if cors_issues else "PASS",
        "details": "Cross-Origin Resource Sharing configuration",
        "issues": cors_issues
    })

    # =====================================================================
    # CHECK 2: Authentication & Authorization
    # =====================================================================
    auth_checks = {
        "api_key_validation": False,
        "jwt_tokens": False,
        "role_based_access": False,
        "mrn_access_control": False
    }

    for file_path in [backend_dir / "app.py", backend_dir / "tools_api.py"]:
        if file_path.exists():
            content = file_path.read_text()
            auth_checks["api_key_validation"] = "api_key" in content.lower() or "authorization" in content.lower()
            auth_checks["jwt_tokens"] = "jwt" in content.lower() or "token" in content.lower()
            auth_checks["role_based_access"] = "role" in content.lower() or "permission" in content.lower()
            auth_checks["mrn_access_control"] = "mrn not in" in content or "access" in content.lower()

    if not any(auth_checks.values()):
        report["vulnerabilities"].append({
            "cve": "AUTH-001",
            "severity": "CRITICAL",
            "issue": "No authentication/authorization implementation detected",
            "risk": "Unauthorized access to protected health information (PHI)",
            "affected": ["Backend API endpoints"],
            "mitigation": "Implement OAuth 2.0 or JWT authentication immediately"
        })

    report["findings"].append({
        "check": "Authentication & Authorization",
        "status": "WARN" if not any(auth_checks.values()) else "PASS",
        "details": "User identification and access control",
        "checks": auth_checks
    })

    # =====================================================================
    # CHECK 3: PII/PHI Data Protection
    # =====================================================================
    pii_risks = []

    # Check for hardcoded data
    sample_data_path = Path("/home/labuser/Day5/Elation-Health-Chart-Review/data/sample_patients.json")
    if sample_data_path.exists():
        pii_risks.append({
            "severity": "MEDIUM",
            "issue": "Sample patient data stored in repository",
            "risk": "Even de-identified data could pose privacy risk",
            "fix": "Use synthetic data generator or environment variables"
        })

    # Check for encryption
    encryption_found = False
    for file_path in [backend_dir / "app.py", backend_dir / "tools_api.py", backend_dir / "rag_engine.py"]:
        if file_path.exists():
            content = file_path.read_text()
            if "encrypt" in content.lower() or "hash" in content.lower() or "ssl" in content.lower():
                encryption_found = True

    if not encryption_found:
        pii_risks.append({
            "severity": "HIGH",
            "issue": "No encryption implementation detected",
            "risk": "PHI transmitted and stored in plaintext",
            "fix": "Implement end-to-end encryption (TLS 1.3+) and data at-rest encryption"
        })

    report["findings"].append({
        "check": "PII/PHI Protection",
        "status": "FAIL" if len(pii_risks) > 1 else "WARN",
        "details": "Protected health information handling",
        "risks": pii_risks
    })

    # =====================================================================
    # CHECK 4: Logging & Audit Trail
    # =====================================================================
    audit_checks = {
        "access_logging": 0,
        "error_logging": 0,
        "audit_events": 0,
        "log_levels": 0
    }

    for file_path in [backend_dir / "app.py", backend_dir / "tools_api.py", backend_dir / "observability.py"]:
        if file_path.exists():
            content = file_path.read_text()
            audit_checks["access_logging"] += len(re.findall(r'log.*access|log.*request', content, re.IGNORECASE))
            audit_checks["error_logging"] += len(re.findall(r'log.*error|log.*exception', content, re.IGNORECASE))
            audit_checks["audit_events"] += len(re.findall(r'audit|log.*event', content, re.IGNORECASE))
            audit_checks["log_levels"] += len(re.findall(r'debug|info|warning|error', content, re.IGNORECASE))

    report["findings"].append({
        "check": "Audit Logging",
        "status": "PASS" if audit_checks["access_logging"] > 0 else "WARN",
        "details": "Audit trail and compliance logging",
        "metrics": audit_checks
    })

    # =====================================================================
    # CHECK 5: Input Validation & Injection Attacks
    # =====================================================================
    injection_risks = []

    for file_path in [backend_dir / "tools_api.py", backend_dir / "app.py"]:
        if file_path.exists():
            content = file_path.read_text()

            # Check for SQL injection patterns
            if re.search(r'query\s*=.*\+|format\(.*mrn|f".*{.*}".*query', content):
                injection_risks.append({
                    "severity": "HIGH",
                    "type": "SQL Injection",
                    "issue": "Dynamic query construction detected",
                    "fix": "Use parameterized queries"
                })

            # Check for NoSQL injection
            if re.search(r'{".*"\s*:\s*.*mrn|\.find\(.*mrn', content):
                injection_risks.append({
                    "severity": "HIGH",
                    "type": "NoSQL Injection",
                    "issue": "Dynamic object construction in queries",
                    "fix": "Validate and sanitize all inputs"
                })

    report["findings"].append({
        "check": "Input Validation & Injection Prevention",
        "status": "FAIL" if injection_risks else "PASS",
        "details": "Protection against injection attacks",
        "issues": injection_risks
    })

    # =====================================================================
    # CHECK 6: Secrets & Configuration
    # =====================================================================
    secrets_issues = []

    for file_path in [backend_dir / "app.py", backend_dir / "tools_api.py", backend_dir / "rag_engine.py"]:
        if file_path.exists():
            content = file_path.read_text()

            # Check for hardcoded secrets
            if re.search(r'password\s*=\s*["\']', content, re.IGNORECASE):
                secrets_issues.append({
                    "severity": "CRITICAL",
                    "issue": "Hardcoded password detected",
                    "fix": "Use environment variables"
                })

            if re.search(r'api[_-]?key\s*=\s*["\']', content, re.IGNORECASE):
                secrets_issues.append({
                    "severity": "CRITICAL",
                    "issue": "Hardcoded API key detected",
                    "fix": "Use environment variables or secrets manager"
                })

    report["findings"].append({
        "check": "Secrets Management",
        "status": "FAIL" if secrets_issues else "PASS",
        "details": "Secure handling of credentials and API keys",
        "issues": secrets_issues
    })

    # =====================================================================
    # VULNERABILITIES SUMMARY
    # =====================================================================
    if cors_issues or pii_risks or injection_risks or secrets_issues:
        report["overall_security_status"] = "NEEDS_REMEDIATION"
    else:
        report["overall_security_status"] = "ACCEPTABLE"

    # =====================================================================
    # RECOMMENDATIONS
    # =====================================================================
    report["recommendations"] = [
        "CRITICAL: Implement OAuth 2.0 or OIDC authentication",
        "CRITICAL: Restrict CORS to specific frontend domain",
        "CRITICAL: Implement TLS 1.3+ encryption for all data in transit",
        "HIGH: Add encryption for sensitive data at rest",
        "HIGH: Implement input validation and sanitization middleware",
        "HIGH: Add comprehensive audit logging for all PHI access",
        "MEDIUM: Implement rate limiting and DDoS protection",
        "MEDIUM: Add security headers (CSP, X-Frame-Options, etc.)",
        "MEDIUM: Implement secrets rotation policy",
        "LOW: Add security testing to CI/CD pipeline",
        "Conduct HIPAA security audit before production deployment"
    ]

    return report


if __name__ == "__main__":
    report = review_security()
    print(json.dumps(report, indent=2))
