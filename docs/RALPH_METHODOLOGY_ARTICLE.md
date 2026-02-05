# Ralph Loop: Autonomous Feature Development for Claude

Hey team,

A few months ago I started exploring how to use Claude for real production features without context rot, decision amnesia, or constant hand-holding.

Today I'm not here to sell a tool, instead I want to share the methodology and logic flow behind **Ralph Loop**, because I think it solves problems we've all hit.

## The Core Problem

When using Claude (or any LLM) for multi-step features, we run into:
- **Context window fills up** → quality degrades
- **Coordination chaos** → hard to track what's done, AI forgets earlier decisions
- **Incomplete execution** → gets stuck mid-implementation
- **No clear path** from spec to merged PR

## The Pattern That Solves It

**Ralph Loop** executes the complete 9-phase feature development cycle autonomously (8 core + Phase 5.5 VERIFY), with intelligent pause conditions.

The diagram below shows how this addresses it:

```
┌────────────────────────────────────────────────────────────────┐
│  RALPH: 9-PHASE AUTONOMOUS FEATURE DEVELOPMENT                 │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  1. INTERVIEW      2. THINK CRITICALLY    3. PLAN              │
│  └─ spec.md        └─ analysis.md         └─ design.md         │
│                       ⚠️ Pauses if:          + tasks.md        │
│                       • Red flags                              │
│                       • Low confidence                         │
│                                                                │
│  4. BRANCH         5. IMPLEMENT           5.5 VERIFY ← NEW!    │
│  └─ worktree       └─ Atomic commits      └─ Browser E2E      │
│                       Real-time docs         agent-browser    │
│                                              Auto-skip if      │
│                                              no frontend       │
│                                                                │
│  6. PR             7. MERGE               8. WRAP-UP           │
│  └─ Auto-sync main └─ ⏸️ Human review     └─ Learnings        │
│     Auto-resolve      + test results                          │
│     conflicts                                                  │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

**Phase 5.5 (VERIFY)** uses Anthropic's agent-browser CLI for frontend E2E testing. Runs automatically when tsx/jsx/css files changed. Includes security filters to prevent secret leakage in screenshots/logs.

## Why This Matters

The insight isn't the specific tool — it's the pattern:

**1. File-Based State Handoff**
- Each phase writes to files: spec.md → analysis.md → design.md → tasks.md
- Next phase reads previous outputs
- No accumulated conversation history → zero context rot

**2. Think Critically Before Code**
- 11-step adversarial analysis before implementation
- Catches architectural issues early
- AI pauses automatically if red flags or low confidence

**3. Git Worktree Isolation**
- Each feature runs in its own worktree
- True parallel development (3+ features simultaneously)
- Zero merge conflicts between features

**4. Smart Pauses**
Ralph pauses autonomously only when human judgment needed:
- Interview: TBD values in spec
- Analysis: Red flags or low confidence
- PR: Source code conflicts (auto-resolves docs/lockfiles)
- Merge: Approval required
- 80% of execution is autonomous

**5. Living Documentation**
- Updates tasks.md, status.md in real-time (not at the end)
- Context resumable at any iteration
- Captures learnings in wrap_up.md post-merge

## State as the Source of Truth

Everything flows through persistent markdown files:

```
docs/features/FEAT-XXX/
├── spec.md         ← Interview decisions
├── analysis.md     ← Pre-implementation analysis
├── design.md       ← Architecture
├── tasks.md        ← Real-time checklist
├── status.md       ← Progress tracking
└── context/
    ├── session_log.md
    ├── decisions.md
    └── wrap_up.md
```

This is memory across sessions. You can stop at iteration 7, resume tomorrow at iteration 8.

## Ralph vs GSD

| Dimension | GSD | Ralph |
|-----------|-----|-------|
| **Scope** | Implementation | Full lifecycle (spec → merge) |
| **Autonomy** | Manual commands per phase | Fully autonomous loop |
| **Pre-analysis** | Optional | Mandatory (Think Critically) |
| **Parallel work** | Subagents | Git worktrees |
| **Pausing** | Manual checkpoints | Auto (4 conditions) |
| **Git integration** | Manual | Auto (branch, commit, PR, conflicts) |

**Both solve context rot. Ralph adds end-to-end automation.**

## Real Example

```bash
# Add feature to pipeline
echo "| FEAT-001-auth | User Auth | ⚪ Pending |" >> _index.md

# Start loop
./ralph-feature.ps1 FEAT-001-auth 15

# Ralph executes:
Iter 1:  Interview → spec.md
Iter 2:  Think Critically → analysis.md (confidence: High)
Iter 3:  Plan → design.md + tasks.md (19 tasks)
Iter 4:  Branch → feature/001-auth
Iter 5-12: Implement → 19 commits
Iter 13: PR → Auto-resolved conflicts, created PR #15
Iter 14: Merge → ⏸️ Waiting for approval
Iter 15: Wrap-Up → Learnings captured
✅ COMPLETE
```

**Result:** Feature shipped in 15 iterations with 3 human touchpoints (Interview answers, PR approval, done).

## The Insight

> **Decompose feature development into 8 autonomous phases with file-based state handoff and intelligent pause conditions.**

This is how you ship production features with AI, not just prototype them.

The complexity is in the system, not in your workflow.

What you see: Features going from idea to production.

What's happening: 8-phase execution, smart pausing, worktree orchestration, conflict resolution, living docs.

---

*Written January 2026*

**Resources:**
- [Ralph Loop Documentation](./ralph-feature-loop.md)
- [8-Phase Feature Cycle](./feature_cycle.md)
