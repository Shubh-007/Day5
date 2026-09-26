#!/bin/bash
# Healthcare Project Pre-Commit Hooks
# Runs compliance checks before code commit

set -e

echo "🏥 Healthcare Platform Pre-Commit Checks"
echo "========================================"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

FAILED=0

# 1. Check for accidental PII commits
echo -e "\n${YELLOW}Checking for PII patterns...${NC}"
if git diff --cached | grep -iE '(SSN|social.*security|credit.*card|MRN|patient.*ID|PHI)' > /dev/null 2>&1; then
    echo -e "${RED}✗ FAILED: Potential PII detected in staged changes${NC}"
    echo "  Do not commit real patient data, SSNs, medical record numbers, etc."
    FAILED=1
else
    echo -e "${GREEN}✓ PASS: No obvious PII patterns detected${NC}"
fi

# 2. Check for HIPAA-sensitive comments
echo -e "\n${YELLOW}Checking for HIPAA-sensitive comments...${NC}"
if git diff --cached | grep -iE '(TODO.*HIPAA|FIXME.*encrypt|TODO.*audit)' > /dev/null 2>&1; then
    echo -e "${RED}✗ WARNING: HIPAA-sensitive TODOs in code${NC}"
    echo "  These should be tracked in issues, not code comments"
    # Don't fail, just warn
else
    echo -e "${GREEN}✓ PASS: No concerning TODOs${NC}"
fi

# 3. Check for required files in healthcare projects
echo -e "\n${YELLOW}Checking for required healthcare documentation...${NC}"
for file in "plan.md" "architecture/system-architecture.md" "implementation/development-roadmap.md" "monitoring/observability-strategy.md"; do
    if [ -f "$file" ]; then
        echo -e "  ${GREEN}✓ Found: $file${NC}"
    else
        # Only warn for modified projects
        if git diff --cached --name-only | grep -q "\.md$"; then
            echo -e "  ${YELLOW}⚠ Missing: $file${NC}"
        fi
    fi
done

# 4. Check Python code for security issues (if any Python files changed)
echo -e "\n${YELLOW}Checking Python code security...${NC}"
if git diff --cached --name-only | grep -q "\.py$"; then
    PY_FILES=$(git diff --cached --name-only | grep "\.py$")

    # Check for hardcoded credentials
    if echo "$PY_FILES" | xargs grep -l "password\|api_key\|secret" 2>/dev/null | grep -v "test" > /dev/null; then
        echo -e "${RED}✗ FAILED: Potential hardcoded credentials in Python${NC}"
        FAILED=1
    else
        echo -e "${GREEN}✓ PASS: No obvious hardcoded credentials${NC}"
    fi
fi

# 5. Check for required security headers in code
echo -e "\n${YELLOW}Checking for security best practices...${NC}"
if git diff --cached --name-only | grep -q "\.py$\|\.ts$\|\.js$"; then
    echo -e "${GREEN}✓ Code changes detected - security review recommended in CI${NC}"
fi

# 6. Check commit message format
echo -e "\n${YELLOW}Checking commit message format...${NC}"
COMMIT_MSG=$(cat "$1" 2>/dev/null || echo "")
if [ -z "$COMMIT_MSG" ]; then
    echo -e "${RED}✗ WARNING: Empty commit message${NC}"
fi

if ! echo "$COMMIT_MSG" | grep -q "^[A-Z]"; then
    echo -e "${YELLOW}⚠ Commit message should start with capital letter${NC}"
fi

# 7. Check for clinical/compliance keywords
echo -e "\n${YELLOW}Checking for compliance tracking...${NC}"
if echo "$COMMIT_MSG" | grep -iE "(HIPAA|compliance|security|encrypt)" > /dev/null; then
    echo -e "${GREEN}✓ Compliance-tracked change${NC}"
fi

# Summary
echo ""
echo "========================================"
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All pre-commit checks PASSED${NC}"
    echo "Ready to commit"
    exit 0
else
    echo -e "${RED}✗ Pre-commit checks FAILED${NC}"
    echo "Please address the issues above before committing"
    exit 1
fi
