# Contributing to Healthcare Platform Portfolio

## Overview

This repository contains 5 comprehensive healthcare AI platform designs:
- Banner Health (Physician Documentation)
- Carta Healthcare (Data Extraction)
- Commure (Documentation Automation)
- Elation Health (Chart Review)
- Qualified Health (Patient Screening)

## Branch Strategy

- **main**: Production-ready documentation and infrastructure
- **dev**: Development branch for feature work
- **platform/***: Platform-specific branches (e.g., `platform/commure-phase0`)
- **feature/***: Feature branches (e.g., `feature/asr-engine`)

## Before Contributing

1. Review the platform's CLAUDE.md guide
2. Check pre-commit hooks are set up: `chmod +x .claude/hooks/pre-commit-*.sh`
3. Understand the success criteria in the platform's README

## Commit Guidelines

- Keep commits focused and atomic
- Use platform abbreviations in commits: `[BANNER]`, `[CARTA]`, `[COMMURE]`, `[ELATION]`, `[QUALIFIED]`
- Example: `[COMMURE] Phase 0: Implement ASR engine`
- Always include attribution line: `Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>`

## Clinical/Compliance Reviews

Before merging clinical or compliance-sensitive changes:
1. Run `/clinical-review` if modifying clinical logic
2. Run `/compliance-audit` if modifying compliance-sensitive code
3. Get platform clinical lead approval

## Pull Requests

Include:
- What platform(s) affected
- Which phase/module touched
- Success criteria being addressed
- Testing plan (if applicable)

## Questions?

Review the CLAUDE.md guide in the repository root or platform-specific guides.
