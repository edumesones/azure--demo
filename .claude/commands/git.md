---
description: Git sync, commit, and push with smart conflict handling (git-automator)
argument-hint: [commit message] or "pr" or "sync"
allowed-tools: Bash(git:*), Bash(gh:*), Read, Write
---

# Git Automator Commands

## Usage

```bash
# Sync current branch with main
/git sync

# Commit with message
/git "Add user authentication"

# Create PR
/git pr

# Full flow: sync -> commit -> push
/git "Message" --push
```

## Operations

### Sync (`/git sync`)

```bash
# 1. Fetch latest
git fetch origin

# 2. Rebase on main
git pull --rebase origin main

# 3. If conflicts -> follow conflict protocol
```

### Commit (`/git "message"`)

```bash
# 1. Check status
git status

# 2. Show diff for review
git diff --no-pager

# 3. Stage all changes
git add .

# 4. Commit with feature prefix
# Detect feature from branch name
BRANCH=$(git branch --show-current)
# Extract FEAT-XXX from feature/XXX-name format

git commit -m "[FEAT-ID]: $ARGUMENTS"
```

### Push (`/git push`)

```bash
git push -u origin HEAD
```

### PR (`/git pr`)

```bash
# Detect gh command
gh --version 2>/dev/null || GH_CMD="/c/Program Files/GitHub CLI/gh"

# Check if PR exists
$GH_CMD pr view 2>/dev/null

# If no PR, create one
$GH_CMD pr create --fill --base main --web
```

## Conflict Resolution

When conflicts occur:

1. **Show conflicts:**
   ```bash
   git status
   ```

2. **List conflicting files to user**

3. **For each file, ask:**
   "Do you want to keep LOCAL (your changes) or REMOTE (incoming changes)?"

4. **After user decides:**
   ```bash
   # If keep local
   git checkout --ours [file]

   # If keep remote
   git checkout --theirs [file]

   # If manual merge needed, read file and help user
   git add [file]
   ```

5. **Continue rebase:**
   ```bash
   git rebase --continue
   ```

## Smart Commit Message

If no message provided, analyze changes:

```bash
# Get changed files
git diff --cached --name-only

# Categorize:
# - New files -> "Add [component]"
# - Modified files -> "Update [component]"
# - Deleted files -> "Remove [component]"
# - Test files -> "Add tests for [component]"
```

Suggest message to user, let them confirm or edit.

## Feature Branch Detection

```bash
# Get current branch
BRANCH=$(git branch --show-current)

# Extract feature ID
# feature/001-auth -> FEAT-001
# feature/002-dashboard -> FEAT-002

# Prefix commits automatically
```

## Argument
$ARGUMENTS
