---
description: Fork a terminal with git worktree isolation for parallel feature development
argument-hint: FEAT-XXX-name <role>
allowed-tools: Bash(python:*), Bash(git:*), Read, Write
---

# Fork Feature (with Git Worktree Isolation)

## Purpose

Launch a new terminal with Claude Code in an **isolated git worktree**. This ensures:
- Zero conflicts between parallel work
- Each fork has its own physical directory
- Safe parallel development on multiple features
- Clean PR workflow after completion

## How It Works

```
proyecto/                              <- Main repo (you stay here)
proyecto-FEAT-001-auth-full/           <- Worktree for FEAT-001 (isolated)
proyecto-FEAT-002-dashboard-full/      <- Worktree for FEAT-002 (isolated)
```

Each worktree:
- Is a **separate directory** with full repo copy
- Shares the same `.git` (commits are shared)
- Works on its **feature branch**
- No risk of overwriting other work

## Available Roles

| Role | Focus | Tasks Section |
|------|-------|---------------|
| `full` | All tasks (recommended for single dev) | ALL |
| `backend` | FastAPI, models, services | Backend |
| `frontend` | React, Gradio, UI | Frontend |
| `data` | Pipelines, ML, preprocessing | Data |
| `tests` | Unit, integration, e2e tests | Tests |
| `docs` | README, docstrings, API docs | Documentation |

## Usage

```bash
# Fork full feature (most common)
/fork-feature FEAT-001-auth full

# Fork specific roles (for splitting work)
/fork-feature FEAT-001-auth backend
/fork-feature FEAT-001-auth frontend

# List active worktrees
python .claude/skills/fork-feature/tools/fork_feature.py --list-worktrees

# Cleanup after merge
python .claude/skills/fork-feature/tools/fork_feature.py --cleanup FEAT-001-auth
```

## What Happens When You Fork

1. **Creates branch** `feature/001-auth` (if not exists)
2. **Creates worktree** at `../proyecto-FEAT-001-auth-full/`
3. **Generates context file** with spec, design, tasks
4. **Opens new terminal** in the worktree directory
5. **Starts Claude Code** ready to work

## Instructions

1. Parse arguments: `$ARGUMENTS` -> feature_id, role

2. Execute fork script:
   ```bash
   python .claude/skills/fork-feature/tools/fork_feature.py $ARGUMENTS
   ```

3. Script will:
   - Create branch if needed
   - Create worktree
   - Launch terminal
   - Save context file

4. Tell user to paste startup command in new terminal

## After Fork Completes Work

```bash
# In the forked terminal, when all tasks done:
git push -u origin feature/001-auth
gh pr create --title "FEAT-001: Auth" --base main

# After PR is merged, cleanup from main terminal:
python .claude/skills/fork-feature/tools/fork_feature.py --cleanup FEAT-001-auth
```

## Argument
$ARGUMENTS
