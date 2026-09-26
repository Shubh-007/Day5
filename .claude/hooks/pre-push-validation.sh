#!/bin/bash
# Pre-push validation hook
# Runs comprehensive tests before pushing to remote

echo "🔍 Pre-push validation running..."
echo ""

# Check if pushing to main or dev
remote="$1"
url="$2"

# Get list of commits being pushed
local_branch=$(git rev-parse --abbrev-ref HEAD)
remote_branch="$local_branch"

echo "Branch being pushed: $local_branch → $remote/$remote_branch"
echo ""

# Run validations
FAILED=0

# 1. Run all platform validations
echo "📋 Running platform validations..."
if bash tests/validate-all-platforms.sh > /tmp/platform-test.log 2>&1; then
  echo "✓ Platform validation passed"
else
  echo "✗ Platform validation FAILED"
  cat /tmp/platform-test.log
  FAILED=1
fi

# 2. Run clinical validation
echo "🏥 Running clinical validation..."
if bash tests/clinical-validation.sh > /tmp/clinical-test.log 2>&1; then
  echo "✓ Clinical validation passed"
else
  echo "✗ Clinical validation FAILED"
  cat /tmp/clinical-test.log
  FAILED=1
fi

# 3. Check for PII in commits
echo "🔒 Scanning for PII/credentials..."
if git diff --cached --name-only | while read file; do
  if grep -l -iE "(password|api.?key|secret|credential|SSN|MRN)" "$file" 2>/dev/null; then
    echo "✗ Found potential PII in: $file"
    exit 1
  fi
done; then
  echo "✓ No PII detected"
else
  echo "✗ PII/credentials found - cannot push"
  FAILED=1
fi

# 4. For main branch - stricter checks
if [ "$local_branch" = "main" ]; then
  echo ""
  echo "⚠️  Pushing to MAIN branch - running strict checks..."

  # Verify all platforms have complete documentation
  for platform in Banner-Health-Clinical-Assistant Carta-Healthcare-Data-Processing \
                 Commure-Documentation-Automation Elation-Health-Chart-Review \
                 Qualified-Health-Patient-Screening; do
    for file in plan.md CLAUDE.md README.md architecture/system-architecture.md \
               implementation/development-roadmap.md monitoring/observability-strategy.md; do
      if [ ! -f "$platform/$file" ]; then
        echo "✗ Missing required file: $platform/$file"
        FAILED=1
      fi
    done
  done

  if [ $FAILED -eq 0 ]; then
    echo "✓ All platforms have complete documentation"
  fi
fi

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $FAILED -eq 0 ]; then
  echo "✅ All pre-push validations PASSED"
  echo "Safe to push to $remote/$remote_branch"
  exit 0
else
  echo "❌ Pre-push validations FAILED"
  echo "Fix errors before pushing"
  exit 1
fi
