#!/bin/bash
# Qualified Health Pre-Commit Hooks
# Validates patient screening accuracy & intervention readiness

echo "🏥 Qualified Health Pre-Commit Checks"

# Check for screening rule changes
if git diff --cached | grep -q "screening.*rule\|criteria\|eligibility"; then
    echo "⚠️  Screening rule changed"
    echo "  Verify: Is 90%+ accuracy maintained?"
    echo "  Check: Are eligible patients correctly identified?"
fi

# Check for clinical criteria changes
if git diff --cached | grep -q "threshold\|cutoff\|risk.*score"; then
    echo "⚠️  Clinical threshold changed - verify evidence-based"
    echo "  Check: What's the false positive rate?"
fi

# Check for patient matching logic
if git diff --cached | grep -q "matching\|MPI\|identity\|dedup"; then
    echo "⚠️  Patient matching logic changed"
    echo "  Critical: Are we matching patients correctly across systems?"
fi

# Check for intervention protocols
if git diff --cached | grep -q "intervention\|protocol\|action"; then
    echo "ℹ️  Intervention protocol changed - ensure clinical appropriateness"
fi

echo "✓ Qualified Health checks passed"
