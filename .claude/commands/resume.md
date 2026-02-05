---
description: Resume an interrupted feature - Recover context and continue from where you left off
argument-hint: FEAT-XXX
allowed-tools: Read, Bash(git:*), Bash(cat:*), Bash(ls:*)
---

# Resume Feature

## Purpose

Recover context from an interrupted feature session and continue work seamlessly.

## When to Use

- Session interrupted unexpectedly
- Returning to feature after days/weeks
- Switching machines or environments
- Starting new Claude session on existing feature

## Instructions

### 1. Read Feature Status (FIRST)

```bash
cat docs/features/$ARGUMENTS/status.md
```

Identify:
- Current phase (Interview, Plan, Branch, Implement, PR, Merge)
- Progress (X/Y tasks if in Implement)
- Any blockers
- Last activity date

### 2. Read Session Log (SECOND)

```bash
cat docs/features/$ARGUMENTS/context/session_log.md
```

Find:
- Last entry timestamp
- What was being worked on
- Next step that was planned

### 3. Read Current Tasks (THIRD)

```bash
cat docs/features/$ARGUMENTS/tasks.md
```

Identify:
- Tasks marked [x] (complete)
- Tasks marked [in progress] (was interrupted)
- Tasks marked [blocked]
- Next pending task [ ]

### 4. Check for Active Blockers

```bash
cat docs/features/$ARGUMENTS/context/blockers.md
```

Look for any Active blockers that need resolution.

### 5. Verify Git State

```bash
# Current branch
git branch --show-current

# Expected: feature/XXX-nombre
# If on main: need to checkout feature branch

# Uncommitted changes?
git status

# Recent commits
git log -n 5 --oneline
```

If not on correct branch:
```bash
git checkout feature/XXX-nombre
git pull origin feature/XXX-nombre
```

### 6. Create Resume Entry

Add to `docs/features/$ARGUMENTS/context/session_log.md`:

```markdown
### [YYYY-MM-DD HH:MM] - Session Resumed

**Last activity:** [date from last log]
**Days without activity:** X
**State found:**
- Phase: [current phase]
- Progress: X/Y tasks
- Branch: [name]
- Uncommitted changes: yes/no

**Continuing from:** [pending task or action]

**Active blockers:** [none / list]
```

### 7. Present Summary to User

```
Resuming FEAT-XXX

**Last Activity:** [date] ([X days ago])

**Current State:**
- Phase: [Implement]
- Progress: [5/12 tasks (42%)]
- Branch: feature/XXX-nombre

**Last Completed:** [Task B3 - Create UserService]

**Next Task:** [Task B4 - Create API endpoints]

**Blockers:** [None] or [List active blockers]

**Ready to continue?**
```

### 8. Continue Work

Once context is recovered:
- Resume from the identified task/phase
- Follow normal feature_cycle.md flow
- Update context/session_log.md as you progress

## Argument
$ARGUMENTS
