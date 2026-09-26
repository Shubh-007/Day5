"""Audit logging for PHI access - HIPAA compliance."""

import os
import json
import logging
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler


# Set up rotating file handler for audit logs
def _setup_audit_logger():
    """Initialize the audit logger with rotating file handler."""
    log_path = os.environ.get("AUDIT_LOG_PATH", "backend/logs/audit.log")

    # Ensure log directory exists
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    logger = logging.getLogger("audit")
    logger.setLevel(logging.INFO)

    # Remove existing handlers (avoid duplicates)
    logger.handlers = []

    # Rotating file handler: 10MB per file, keep 10 files (100MB total)
    handler = RotatingFileHandler(
        log_path,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10
    )

    # Use JSON formatting for structured logging
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


_audit_logger = _setup_audit_logger()


def log_access(
    user: str,
    role: str,
    action: str,
    mrn: str,
    ip: str,
    result: str,
    detail: str = None
) -> None:
    """
    Log a PHI access event.

    Args:
        user: Username of the user
        role: Role of the user (admin, clinician)
        action: Action performed (e.g. "GET /api/patients/{mrn}", "LIST_PATIENTS")
        mrn: Patient MRN (or None for non-patient-specific actions like LIST_PATIENTS)
        ip: Client IP address
        result: Result of the access (success, denied, error)
        detail: Optional detail message (e.g. reason for denial)
    """
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user": user,
        "role": role,
        "action": action,
        "mrn": mrn,
        "ip": ip,
        "result": result,
    }

    if detail:
        event["detail"] = detail

    _audit_logger.info(json.dumps(event))
