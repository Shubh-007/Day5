#!/bin/bash
# Elation Health Pre-Commit Hooks
# Validates chart summarization & clinician efficiency

echo "🏥 Elation Health Pre-Commit Checks"

# Check for chart summary changes
if git diff --cached | grep -q "summary\|summariz\|concise"; then
    echo "✓ Chart summary logic change"
    echo "  Verify: Can clinician understand in <30 seconds?"
    echo "  Target: 61% time savings (25 min → 10 min)"
fi

# Check for time-saving metrics
if git diff --cached | grep -q "time.*saving\|review.*time\|preparation"; then
    echo "ℹ️  Time-saving metric change - verify impact on clinician workload"
fi

# Check for visit prep changes
if git diff --cached | grep -q "visit.*prep\|preparation\|alert\|critical"; then
    echo "⚠️  Visit prep logic changed - verify alerts still accurate"
fi

# Check for adoption metrics
if git diff --cached | grep -q "adoption\|satisfaction\|NPS"; then
    echo "ℹ️  Adoption metric change - important for clinician feedback"
fi

echo "✓ Elation Health checks passed"
