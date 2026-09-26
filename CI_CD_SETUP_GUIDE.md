# CI/CD Setup & Configuration Guide

## Quick Start

```bash
# 1. Clone repository
git clone <repo-url> Day5
cd Day5

# 2. Set up local hooks (ONE TIME)
bash .claude/hooks/setup-hooks.sh

# 3. Try committing (hooks will validate automatically)
git checkout dev
echo "test" >> test.txt
git add test.txt
git commit -m "test: verify hooks working"
```

---

## Local Setup (Developer Machine)

### Step 1: Install Hooks

```bash
# Make scripts executable
chmod +x .claude/hooks/pre-*.sh
chmod +x tests/*.sh

# Create git hooks in .git/hooks
cp .claude/hooks/pre-commit-healthcare.sh .git/hooks/pre-commit
cp .claude/hooks/pre-push-validation.sh .git/hooks/pre-push

chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/pre-push
```

### Step 2: Test Hooks

```bash
# Test pre-commit hook
cd Day5
touch test-file.txt
git add test-file.txt
git commit -m "test: hooks working"
# Should run validation and succeed

# Clean up
git reset --soft HEAD~1
rm test-file.txt
```

### Step 3: Verify Validation Scripts

```bash
# Run platform validation manually
bash tests/validate-all-platforms.sh

# Run clinical validation manually
bash tests/clinical-validation.sh
```

---

## GitHub Setup (Repository)

### Step 1: Enable Actions

1. Go to Repository → Settings → Actions
2. Enable "Allow all actions and reusable workflows"
3. Save

### Step 2: Configure Branch Protection

#### For main branch:

1. Go to Settings → Branches
2. Click "Add rule"
3. Fill in:
   - Pattern: `main`
   - Require pull request reviews before merging: ✓ (1)
   - Dismiss stale pull request approvals: ✓
   - Require status checks to pass: ✓
     - Select: `validate-platforms`
     - Select: `clinical-validation`
     - Select: `security-scan`
     - Select: `test-git-hooks`
   - Require branches to be up to date before merging: ✓
   - Include administrators: ✓
   - Restrict who can push: ✓ (select only admins)

#### For dev branch:

1. Click "Add rule"
2. Fill in:
   - Pattern: `dev`
   - Require pull request reviews before merging: ✓ (1)
   - Require status checks to pass: ✓
     - Select all 4 checks
   - Require branches to be up to date: ✓

### Step 3: Add Required Reviewers

1. Settings → Branches → main
2. Under "Require pull request reviews":
   - Require code review: ✓
   - Require review from Code Owners: (optional)
3. Save

---

## Development Workflow

### Create a Feature Branch

```bash
git checkout dev
git pull origin dev
git checkout -b feature/my-feature
```

### Make Changes

```bash
# Edit files
# ...

# Stage changes
git add .

# Commit (pre-commit hook runs automatically)
git commit -m "[PLATFORM] Feature: description"
# → Validates no PII, required files, structure
```

### Push to Remote

```bash
git push origin feature/my-feature

# Pre-push hook runs automatically
# → Validates all platforms
# → Checks clinical requirements
# → Scans for credentials
# → Either blocks push (fix needed) or allows it
```

### Create Pull Request

```bash
gh pr create --base dev --head feature/my-feature
```

### GitHub Actions Runs

1. CI workflow triggers
2. Tests run in parallel:
   - Platform validation
   - Clinical validation
   - Security scanning
   - Hook verification
3. Results shown in PR status

### Get Approval

- Wait for CI to pass (green checkmark)
- Wait for code review approval
- Clinical lead approves (if clinical changes)
- Compliance officer approves (if compliance changes)

### Merge to Dev

```bash
# When all checks pass and PR approved
git checkout dev
git pull origin dev
git merge --no-ff feature/my-feature
git push origin dev
```

### Merge to Main (When Ready)

```bash
# Create PR from dev to main
gh pr create --base main --head dev

# Wait for all checks and approvals
# Merge when ready
git checkout main
git pull origin main
git merge --no-ff dev
git push origin main
```

---

## Validation Scripts Usage

### Platform Validation

```bash
bash tests/validate-all-platforms.sh
```

**Checks:**
- All 5 platforms have required files
- Documentation quality (line counts)
- Infrastructure setup (skills, agents, MCP)
- No PII/credentials
- Clinical/compliance sections present

**Output:** ✓ PASSED or ✗ FAILED with details

### Clinical Validation

```bash
bash tests/clinical-validation.sh
```

**Checks:**
- Accuracy targets documented
- HIPAA compliance documented
- Clinical safety measures documented

**Output:** ✓ PASSED or ✗ FAILED per platform

### Pre-Push Validation

```bash
bash .claude/hooks/pre-push-validation.sh
```

**Automatically runs before push:**
- All platform validations
- Clinical validations
- PII/credential scan
- For main: Complete documentation check

---

## CI/CD Jobs (GitHub Actions)

### Job: validate-platforms
- Runs all 5 platform validations
- Checks documentation structure
- Status: Required for merge

### Job: clinical-validation
- Tests accuracy targets
- Verifies compliance
- Tests safety measures
- Status: Required for merge

### Job: test-git-hooks
- Verifies hooks exist
- Checks hook syntax
- Status: Required for merge

### Job: security-scan
- Scans for dangerous patterns
- Verifies encryption mentions
- Status: Required for merge

### Job: merge-to-main (on success)
- Reports "Ready for merge to main"
- Only runs if dev → main push
- Informational only

---

## Troubleshooting

### Hooks not running?

```bash
# Check hooks are executable
ls -la .git/hooks/pre-*
# Should show: -rwxr-xr-x

# Make executable if not
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/pre-push

# Test hook directly
bash .git/hooks/pre-commit
```

### CI failing?

```bash
# Check what's failing
gh run list --status failure --limit 1
gh run view <run-id> --log

# Run validation locally to debug
bash tests/validate-all-platforms.sh
bash tests/clinical-validation.sh

# Fix issues, commit, and push again
```

### Want to bypass hooks (emergency only)?

```bash
# For pre-commit
git commit --no-verify -m "Emergency fix"

# For pre-push
git push --no-verify origin branch-name

# DOCUMENT WHY YOU BYPASSED
# CREATE FOLLOW-UP ISSUE
```

---

## Monitoring

### Check Recent CI Results

```bash
# List recent runs
gh run list

# View specific run details
gh run view <run-id>

# Get failed runs
gh run list --status failure
```

### Monitor Branch

```bash
# Check branch protection status
gh api repos/owner/repo/branches/main

# List required status checks
gh api repos/owner/repo/branches/main | grep 'required_status_checks'
```

---

## Success Checklist

- [ ] Cloned repository
- [ ] Set up git hooks locally
- [ ] Can commit to dev without errors
- [ ] Can push to dev without errors
- [ ] GitHub Actions workflow runs successfully
- [ ] Branch protection rules configured
- [ ] Team members trained
- [ ] First PR merged to main successfully

---

## Next Steps

1. **Setup local development environment**
   - Install hooks
   - Test validation scripts
   - Create test branch

2. **Configure GitHub**
   - Enable Actions
   - Set up branch protection
   - Configure required reviewers

3. **First feature branch**
   - Create feature/test-ci branch
   - Make small change
   - Push and watch CI run
   - Verify all checks pass
   - Merge to verify workflow

4. **Team training**
   - Walk through workflow with team
   - Explain validation requirements
   - Show how to handle CI failures

---

## Questions?

- See BRANCH_PROTECTION_POLICY.md for detailed policy
- See CONTRIBUTING.md for development guidelines  
- See CLAUDE.md for platform-specific details
