# Branch Protection & CI/CD Validation Policy

## Overview

Healthcare Platform Portfolio uses automated validation to ensure code quality, clinical safety, and compliance before merging.

---

## Branch Strategy

### main (Production)
- **Status**: Protected branch
- **Requires**: All CI checks passing
- **Requires**: Code review (1+ approval)
- **Requires**: Clinical validation
- **Dismisses stale reviews**: Yes
- **Restricts who can push**: Admins only

### dev (Development)
- **Status**: Protected branch
- **Requires**: All CI checks passing
- **Requires**: No PII/credentials
- **Allow force push**: No (maintains history)
- **Dismiss stale reviews**: Yes

### feature/* (Feature branches)
- **Status**: Unprotected
- **Uses**: Pre-commit/pre-push hooks locally
- **Purpose**: Feature development

### platform/* (Platform-specific)
- **Status**: Unprotected
- **Uses**: Pre-commit hooks locally
- **Purpose**: Platform-specific work

---

## Automated Validation Checklist

### 1. Pre-Commit Hook (Local)
Runs automatically before `git commit`:

```
✓ Check for PII/credentials
✓ Check for HIPAA-sensitive comments
✓ Verify required files exist
✓ Check Python security patterns
✓ Verify commit message format
```

**Result**: Prevents committing dangerous data locally

### 2. Pre-Push Hook (Local)
Runs automatically before `git push`:

```
✓ Platform validation (all 5 platforms)
✓ Clinical validation (accuracy, compliance, safety)
✓ PII/credential scan
✓ For main: Complete documentation check
```

**Result**: Prevents pushing invalid code to remote

### 3. GitHub Actions CI (Remote)
Runs on push/PR to main or dev:

```
✓ Platform validation
✓ Clinical validation
✓ Git hook verification
✓ Security scanning
  - No dangerous patterns
  - Encryption/HIPAA coverage
✓ YAML configuration validation
✓ Compliance checks
```

**Result**: Automated gate before merge

---

## Validation Requirements by Branch

### → main (from dev)

**All CI Checks Must Pass**:
- ✅ Platform validation (65 files, proper structure)
- ✅ Clinical validation (accuracy, compliance, safety)
- ✅ No PII/credentials detected
- ✅ No dangerous patterns (rm -rf, eval, etc.)
- ✅ All git hooks working
- ✅ YAML/JSON configs valid
- ✅ Security scanning passed

**Merge Requirements**:
- ✅ All automated checks passed
- ✅ At least 1 code review approval
- ✅ Stale reviews dismissed
- ✅ Clinical lead approval
- ✅ Compliance officer sign-off

### → dev (from feature/*)

**All CI Checks Must Pass**:
- ✅ Platform validation
- ✅ Clinical validation
- ✅ No PII/credentials
- ✅ Git hooks working

**Merge Requirements**:
- ✅ All automated checks passed
- ✅ At least 1 code review
- ✅ No merge conflicts

### → feature/* (commits)

**Local Pre-Commit Hook Checks**:
- ✅ No PII/credentials
- ✅ Required files structure
- ✅ Commit message format

---

## Setting Up Branch Protection (GitHub)

### 1. Configure main branch

```bash
# In GitHub repository Settings → Branches

# Set main as default branch
Settings > Branches > Default branch: main

# Add branch protection rules:
Settings > Branches > Add rule

# Rule for main:
- Pattern: main
- Require pull request reviews before merging: ✓ (1 required)
- Dismiss stale pull request approvals: ✓
- Require status checks to pass: ✓
  - validate-platforms
  - clinical-validation
  - security-scan
  - test-git-hooks
- Require branches to be up to date: ✓
- Include administrators: ✓
- Restrict who can push: ✓ (Admins only)
```

### 2. Configure dev branch

```bash
# Rule for dev:
- Pattern: dev
- Require pull request reviews before merging: ✓ (1 required)
- Require status checks to pass: ✓
- Require branches to be up to date: ✓
- Allow force pushes: ✗
```

### 3. Required status checks

Require these GitHub Actions to pass:
- `validate-platforms`
- `clinical-validation`
- `security-scan`
- `test-git-hooks`

---

## Setting Up Local Hooks

### 1. Install pre-commit hook

```bash
# Copy hook to git hooks directory
cp .claude/hooks/pre-commit-healthcare.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# For each platform:
cp <platform>/.claude/hooks/pre-commit-<platform>.sh \
   .git/hooks/pre-commit-<platform>
chmod +x .git/hooks/pre-commit-<platform>
```

### 2. Install pre-push hook

```bash
cp .claude/hooks/pre-push-validation.sh .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

### 3. Verify hooks are working

```bash
# Test pre-commit hook
cd Day5
echo "test" >> test-file.txt
git add test-file.txt
git commit -m "test"  # Should trigger pre-commit hook
```

---

## CI/CD Validation Flow

```
Developer commits
  ↓
Pre-commit hook runs (local)
  - Check for PII
  - Verify structure
  ↓ (if FAIL → abort commit)
Developer pushes
  ↓
Pre-push hook runs (local)
  - Platform validation
  - Clinical validation
  - PII/credential scan
  ↓ (if FAIL → abort push)
GitHub receives push
  ↓
GitHub Actions workflow runs
  - Platform validation
  - Clinical validation
  - Security scanning
  - Git hooks verification
  ↓ (if FAIL → CI check fails, blocks merge)
CI checks passed
  ↓
PR approved
  ↓
Clinical lead reviews
  ↓
Merge to main approved
  ↓
Code merged to main ✅
```

---

## Approval Workflow for Main Branch

### Required Approvals

1. **Code Review** (≥1 approval)
   - Engineer reviews code/documentation
   - Checks for clarity, completeness
   - Verifies no regressions

2. **Clinical Validation** (Platform Lead)
   - Verifies clinical accuracy
   - Checks compliance coverage
   - Approves safety measures

3. **Compliance Officer** (for compliance-sensitive changes)
   - Reviews HIPAA/security sections
   - Verifies audit logging
   - Checks encryption implementation

### Approval Comments

When approving, include:
```
✅ Code review complete - no issues
✅ Clinical validation - accuracy targets met
✅ Compliance check - HIPAA requirements satisfied
```

---

## Bypassing Protections (Emergency Only)

### When NOT to bypass:
- Routine commits/merges
- Regular development work
- Testing changes

### When to bypass (with caution):
- Security vulnerabilities requiring immediate fix
- Production incidents requiring emergency patch
- Critical compliance issues

### Emergency bypass process:
1. Notify all team leads
2. Document reason in commit message
3. Create follow-up issue for proper review
4. Schedule post-incident review

---

## Monitoring & Reporting

### Weekly Checks

```bash
# Check merge statistics
git log --merges --oneline main | wc -l

# Check failed CI
gh run list --status failure

# Review clinical validation gaps
grep -r "⚠" test-results/ 2>/dev/null
```

### Monthly Review

- Review failed CI/CD checks
- Identify common validation failures
- Update validation criteria if needed
- Team standup on compliance posture

---

## Troubleshooting

### Hooks not running?
```bash
# Verify hooks are executable
ls -la .git/hooks/

# Re-install hooks
chmod +x .git/hooks/pre-*
```

### Getting past CI failure?
```bash
# Check what failed
gh run view <run-id> --log

# Fix the issue locally
# Run validation manually
bash tests/validate-all-platforms.sh

# Commit fix and push again
```

### Accidentally bypassed protection?
```bash
# Revert merge
git revert -m 1 <merge-commit>
git push origin main

# Create proper PR with validations
```

---

## Success Metrics

Track these metrics monthly:

| Metric | Target | Current |
|--------|--------|---------|
| CI pass rate | 95%+ | TBD |
| Failed validations | <1/week | TBD |
| Security issues caught | 100% | TBD |
| Clinical accuracy verified | 100% | TBD |
| Compliance gaps identified | 100% | TBD |

---

## Questions?

See CONTRIBUTING.md for development guidelines.
See CLAUDE.md for platform-specific instructions.
