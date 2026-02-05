---
description: Ralph Loop - Autonomous feature development (orchestrator, single feature, or status)
argument-hint: orchestrator|feature FEAT-XXX|status|stop
allowed-tools: Bash(./ralph-*:*), Bash(git:*), Bash(gh:*), Bash(python3:*), Read, Write
---

# Ralph Loop Command

Autonomous feature development using the 9-phase Feature Development Cycle.

## Usage

```bash
# Start multi-feature orchestrator (processes all Pending features)
/ralph orchestrator [max_parallel]
/ralph orchestrator 3              # Default: 3 parallel

# Run single feature loop
/ralph feature FEAT-XXX [max_iterations]
/ralph feature FEAT-001-auth 15    # Default: 15 iterations

# Check status of running loops
/ralph status

# Stop all running loops
/ralph stop
```

## How It Works

### Orchestrator Mode

1. Reads `docs/features/_index.md` for features with Pending status
2. Creates isolated git worktrees for each feature
3. Launches `ralph-feature.sh` in each worktree
4. Monitors for merge completion
5. Cleans up worktrees after merge

### Feature Loop Mode

Executes the complete 9-phase cycle:

```
Interview -> Think Critically -> Plan -> Branch -> Implement -> Verify -> PR -> Merge -> Wrap-Up
```

Each iteration:
1. Detects current phase from status.md
2. Executes phase-specific actions
3. Emits completion signal
4. Moves to next phase or continues current

### Pause Conditions

The loop pauses (not terminates) for:
- **Human input needed**: spec.md has TBD values
- **Analysis red flags**: Think Critically found issues
- **Waiting for merge**: PR created, awaiting approval
- **3 consecutive failures**: Something needs investigation

## Instructions

### For Orchestrator

```bash
# Make scripts executable
chmod +x ralph-orchestrator.sh ralph-feature.sh

# Run orchestrator
./ralph-orchestrator.sh $ARGUMENTS
```

### For Single Feature

```bash
# Extract feature ID from arguments
FEATURE_ID=$(echo "$ARGUMENTS" | grep -oE 'FEAT-[0-9]+-[a-zA-Z0-9_-]+')
MAX_ITER=$(echo "$ARGUMENTS" | grep -oE '[0-9]+$' || echo "15")

# Run feature loop
./ralph-feature.sh "$FEATURE_ID" "$MAX_ITER"
```

### For Status

```bash
./ralph-orchestrator.sh --status
```

### For Stop

```bash
./ralph-orchestrator.sh --stop
```

## Output Files

| File | Purpose |
|------|---------|
| `feature-loop-state.json` | Current state of all loops |
| `activity.md` | Chronological log of all actions |
| `ralph-FEAT-XXX.log` | Log for specific feature (in worktree) |

## Integration with Existing Commands

Ralph Loop uses the same documentation structure:
- Updates `spec.md`, `design.md`, `tasks.md`, `status.md`
- Writes to `context/session_log.md`
- Creates `context/wrap_up.md` at the end

You can still use manual commands alongside Ralph:
- `/interview FEAT-XXX` - If you want to do interview manually
- `/resume FEAT-XXX` - To continue a paused feature
- `/wrap-up FEAT-XXX` - To manually close a feature

## Argument
$ARGUMENTS
