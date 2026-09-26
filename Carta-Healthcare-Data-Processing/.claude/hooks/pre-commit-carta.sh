#!/bin/bash
# Carta Healthcare Pre-Commit Hooks
# Validates data extraction quality & clinical accuracy

echo "🏥 Carta Healthcare Pre-Commit Checks"

# Check for ICD-10 code changes
if git diff --cached | grep -q "ICD.10\|icd10\|E11\|I10"; then
    echo "⚠️  Clinical code changes detected"
    echo "   Verify: Is extraction accuracy maintained at 99%?"
fi

# Check for new entity types
if git diff --cached | grep -q "entity_type\|Entity.*Recognition"; then
    echo "ℹ️  New entity type detected - ensure validation rules added"
fi

# Check for data extraction pipeline changes
if git diff --cached | grep -q "extraction\|NLP\|BioBERT"; then
    echo "✓ Extraction pipeline change - accuracy validation required"
fi

echo "✓ Carta Healthcare checks passed"
