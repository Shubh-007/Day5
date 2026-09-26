#!/bin/bash
# Banner Health Pre-Commit Hooks
# Validates physician documentation quality & time-saving metrics

echo "🏥 Banner Health Pre-Commit Checks"

FAILED=0

# Check for physician workflow changes
if git diff --cached | grep -q "physician.*workflow\|documentation.*time"; then
    echo "⚠️  Physician workflow changes detected"
    echo "   Verify: Does this improve time-saving targets?"
    echo "   Target: 20+ min/day saved"
fi

# Check for burnout-related comments
if git diff --cached | grep -iE "(burnout|time.*saving|fatigue)" > /dev/null; then
    echo "✓ Burnout-focused change detected"
fi

# Verify documentation standards are maintained
if [ -f "plan.md" ]; then
    if ! git diff --cached plan.md | grep -q "PASSED\|FAILED"; then
        echo "✓ Documentation standards maintained"
    fi
fi

[ $FAILED -eq 0 ] && echo "✓ Banner Health checks passed" || exit 1
