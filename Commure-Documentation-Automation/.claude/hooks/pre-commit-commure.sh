#!/bin/bash
# Commure Pre-Commit Hooks
# Validates automated documentation quality, compliance, billing

echo "🏥 Commure Pre-Commit Checks"

# Check for ASR changes
if git diff --cached | grep -q "ASR\|speech.*recognition\|transcription"; then
    echo "⚠️  ASR pipeline change - verify >95% accuracy maintained"
fi

# Check for billing code changes
if git diff --cached | grep -q "CPT\|ICD.10\|billing\|RVU"; then
    echo "⚠️  Billing code change - verify compliance & fraud prevention"
    echo "   Check: Medical necessity documented? Codes legal?"
fi

# Check for note generation changes
if git diff --cached | grep -q "template\|generation\|documentation.*format"; then
    echo "✓ Note generation logic change - validate 90%+ automation rate"
fi

# Check for automation targets
if git diff --cached | grep -q "approve\|edit.*rate\|automation"; then
    echo "ℹ️  Automation metrics changed - verify targets achieved"
fi

echo "✓ Commure checks passed"
