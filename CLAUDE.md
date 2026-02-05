# Ralph Loop Methodology - Project Guide

This is a **methodology-only repository**. It contains the Ralph Loop autonomous feature development system, not project-specific code.

## What is Ralph Loop?

Ralph Loop is an autonomous 9-phase feature development system (8 core phases + Phase 5.5 VERIFY) that executes the complete lifecycle from specification to production merge with minimal human intervention.

## The 9-Phase Cycle

```
1. INTERVIEW        → Capture technical decisions (spec.md)
2. THINK CRITICALLY → 11-step pre-implementation analysis (analysis.md)
3. PLAN             → Design architecture + tasks (design.md, tasks.md)
4. BRANCH           → Create isolated git worktree
5. IMPLEMENT        → Execute tasks with atomic commits
5.5 VERIFY          → Browser automation tests (agent-browser E2E) [NEW]
6. PR               → Auto-sync, auto-resolve conflicts, create PR with test results
7. MERGE            → Human approval → Production
8. WRAP-UP          → Capture learnings (wrap_up.md)
```

**Phase 5.5 (VERIFY)** automatically runs when:
- Frontend files changed (tsx/jsx/css/scss)
- Test scripts exist in `docs/features/FEAT-XXX/tests/`
- Uses Anthropic's agent-browser CLI for E2E testing
- Blocks PR creation if tests fail
- Security filters prevent secret leakage

## Documentation

- [8-Phase Feature Cycle](./docs/feature_cycle.md)
- [Ralph Loop Guide](./docs/ralph-feature-loop.md)
- [Methodology Article](./docs/RALPH_METHODOLOGY_ARTICLE.md)

## This is NOT a Code Repository

This repository contains methodology documentation, not project code.
Use this as a reference implementation for your own projects.
