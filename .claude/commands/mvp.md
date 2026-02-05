---
description: Define and prioritize MVP features, create feature folders
argument-hint:
allowed-tools: Read, Write, Bash(ls:*), Bash(cat:*), Bash(mkdir:*), Bash(cp:*)
---

# MVP Planner

## Triggers

This command activates on:
- `/mvp`
- "Define MVP features"
- "Help me plan the MVP"
- "What features should we build?"
- "Let's define the features"
- "Plan the MVP"

## Prerequisites

- `docs/project.md` should exist
- `docs/architecture/_index.md` ideally exists
- If not: suggest running project interview and architecture first

## Purpose

Create:
1. Prioritized feature list in `docs/features/_index.md`
2. Feature folders for MVP features (3-5 max)
3. Clear scope of what's in/out of MVP

## Instructions

1. **Read the skill file:**
   ```
   Read .claude/skills/mvp-planner/SKILL.md
   ```

2. **Read project context:**
   ```bash
   cat docs/project.md
   cat docs/architecture/_index.md 2>/dev/null
   ```

3. **Brainstorm features** in categories:
   - CORE (Must have) - Won't work without it
   - IMPORTANT (Should have) - Valuable but not blocking
   - NICE TO HAVE (Could have) - Post-MVP
   - OUT OF SCOPE (Won't have) - Explicitly excluded

4. **Interview to prioritize:**
   - Ask user to validate/adjust categorization
   - Identify dependencies between features
   - Set realistic timeline

5. **For each MVP feature:**
   - Create folder: `docs/features/FEAT-00X-name/`
   - Copy templates from `docs/features/_template/`
   - Pre-fill spec.md with scope from discussion

6. **Update dashboard:**
   - Create/update `docs/features/_index.md`
   - Include timeline, dependencies, status

7. **Rules:**
   - Maximum 5 features for MVP
   - Ruthlessly cut scope
   - Each feature needs clear "done" criteria

8. **When complete:**
   - Suggest starting with first feature
   - "Interview me about FEAT-001-[name]"

## Output

- `docs/features/_index.md` - Dashboard with all features
- `docs/features/FEAT-001-*/` - First MVP feature folder
- `docs/features/FEAT-002-*/` - Second MVP feature folder
- `docs/features/FEAT-00N-*/` - Remaining MVP features
