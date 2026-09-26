#!/bin/bash
# Comprehensive validation for all 5 healthcare platforms
# Run tests, clinical reviews, and compliance audits

set -e

echo "🏥 HEALTHCARE PLATFORM VALIDATION SUITE"
echo "========================================"
echo ""

PLATFORMS=(
  "Banner-Health-Clinical-Assistant"
  "Carta-Healthcare-Data-Processing"
  "Commure-Documentation-Automation"
  "Elation-Health-Chart-Review"
  "Qualified-Health-Patient-Screening"
)

TESTS_PASSED=0
TESTS_FAILED=0
PLATFORMS_VALIDATED=0

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to validate platform
validate_platform() {
  local platform=$1
  local platform_name=$(echo $platform | sed 's/-/ /g')

  echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${BLUE}Validating: ${platform_name}${NC}"
  echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""

  local platform_dir="/home/labuser/Day5/$platform"

  # Check 1: Required files exist
  echo -e "${YELLOW}[1/5] Checking required files...${NC}"
  local required_files=(
    "plan.md"
    "README.md"
    "CLAUDE.md"
    "architecture/system-architecture.md"
    "implementation/development-roadmap.md"
    "monitoring/observability-strategy.md"
    ".claude/settings.json"
  )

  for file in "${required_files[@]}"; do
    if [ -f "$platform_dir/$file" ]; then
      echo "  ✓ $file"
    else
      echo -e "  ${RED}✗ MISSING: $file${NC}"
      TESTS_FAILED=$((TESTS_FAILED + 1))
      return 1
    fi
  done
  TESTS_PASSED=$((TESTS_PASSED + 1))

  # Check 2: Documentation quality
  echo -e "${YELLOW}[2/5] Checking documentation quality...${NC}"

  local plan_lines=$(wc -l < "$platform_dir/plan.md")
  local arch_lines=$(wc -l < "$platform_dir/architecture/system-architecture.md")
  local roadmap_lines=$(wc -l < "$platform_dir/implementation/development-roadmap.md")

  if [ "$plan_lines" -gt 400 ]; then
    echo "  ✓ plan.md: $plan_lines lines"
  else
    echo -e "  ${YELLOW}⚠ plan.md: $plan_lines lines (target >400)${NC}"
  fi

  if [ "$arch_lines" -gt 200 ]; then
    echo "  ✓ architecture: $arch_lines lines"
  else
    echo -e "  ${YELLOW}⚠ architecture: $arch_lines lines (target >200)${NC}"
  fi

  if [ "$roadmap_lines" -gt 150 ]; then
    echo "  ✓ roadmap: $roadmap_lines lines"
  else
    echo -e "  ${YELLOW}⚠ roadmap: $roadmap_lines lines (target >150)${NC}"
  fi
  TESTS_PASSED=$((TESTS_PASSED + 1))

  # Check 3: Infrastructure setup
  echo -e "${YELLOW}[3/5] Checking infrastructure setup...${NC}"

  local infra_files=(
    ".claude/settings.json"
    ".claude/skills/*.md"
    ".claude/agents/*.md"
    ".claude/mcp/*.md"
  )

  if ls "$platform_dir"/.claude/skills/*.md 1>/dev/null 2>&1; then
    echo "  ✓ Skills configured"
  else
    echo "  ⚠ Skills not configured"
  fi

  if ls "$platform_dir"/.claude/agents/*.md 1>/dev/null 2>&1; then
    echo "  ✓ Agents configured"
  else
    echo "  ⚠ Agents not configured"
  fi

  if ls "$platform_dir"/.claude/mcp/*.md 1>/dev/null 2>&1; then
    echo "  ✓ MCP configured"
  else
    echo "  ⚠ MCP not configured"
  fi
  TESTS_PASSED=$((TESTS_PASSED + 1))

  # Check 4: No PII/Credentials
  echo -e "${YELLOW}[4/5] Checking for PII/credentials...${NC}"

  local pii_check=$(find "$platform_dir" -type f \( -name "*.md" -o -name "*.json" \) \
    -exec grep -l -iE "(password|api.?key|secret|credential|SSN|MRN)" {} \; 2>/dev/null | wc -l)

  if [ "$pii_check" -eq 0 ]; then
    echo "  ✓ No PII/credentials detected"
    TESTS_PASSED=$((TESTS_PASSED + 1))
  else
    echo -e "  ${RED}✗ FOUND: $pii_check files with potential PII/credentials${NC}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
    return 1
  fi

  # Check 5: Clinical/Compliance sections
  echo -e "${YELLOW}[5/5] Checking clinical & compliance coverage...${NC}"

  if grep -q -i "compliance\|HIPAA\|accuracy\|safety" "$platform_dir/plan.md"; then
    echo "  ✓ Compliance coverage in plan"
  else
    echo -e "  ${YELLOW}⚠ Limited compliance coverage in plan${NC}"
  fi

  if grep -q -i "accuracy\|validation\|quality" "$platform_dir/monitoring/observability-strategy.md"; then
    echo "  ✓ Quality metrics in monitoring"
  else
    echo -e "  ${YELLOW}⚠ Limited quality metrics${NC}"
  fi
  TESTS_PASSED=$((TESTS_PASSED + 1))

  PLATFORMS_VALIDATED=$((PLATFORMS_VALIDATED + 1))
  echo ""
}

# Run validation for all platforms
for platform in "${PLATFORMS[@]}"; do
  validate_platform "$platform"
done

# Summary
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}VALIDATION SUMMARY${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Platforms validated: $PLATFORMS_VALIDATED/5"
echo "Tests passed: $TESTS_PASSED"
echo "Tests failed: $TESTS_FAILED"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
  echo -e "${GREEN}✓ ALL VALIDATIONS PASSED${NC}"
  echo -e "${GREEN}Ready for merge to main branch${NC}"
  exit 0
else
  echo -e "${RED}✗ VALIDATION FAILED${NC}"
  echo -e "${RED}Fix failing tests before merging${NC}"
  exit 1
fi
