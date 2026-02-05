---
description: Define technical architecture and create ADRs (Architecture Decision Records)
argument-hint:
allowed-tools: Read, Write, Bash(ls:*), Bash(cat:*), Bash(mkdir:*)
---

# Architecture Designer

## Triggers

This command activates on:
- `/architecture`
- "Help me define the architecture"
- "Define architecture"
- "Let's design the architecture"
- "Help me with technical architecture"

## Prerequisites

- `docs/project.md` should exist
- If not: suggest running project interview first

## Purpose

Create:
1. Architecture overview in `docs/architecture/_index.md`
2. ADRs in `docs/decisions/ADR-NNN-*.md`
3. Technical foundation for features

## Instructions

1. **Read the skill file:**
   ```
   Read .claude/skills/architecture-designer/SKILL.md
   ```

2. **Read project context:**
   ```bash
   cat docs/project.md
   ```

3. **Identify key decisions needed:**
   - Language/Runtime
   - Framework
   - Database
   - Authentication
   - Hosting
   - API style
   - etc.

4. **For each decision:**
   - Present 2-3 options with pros/cons
   - Make a recommendation based on project context
   - Ask for user preference
   - Create ADR immediately after decision

5. **Create architecture overview** with:
   - System diagram
   - Tech stack table linking to ADRs
   - Project structure
   - Key patterns

6. **When complete:**
   - Verify all major decisions have ADRs
   - Suggest next step: "Define MVP features"

## Output

- `docs/architecture/_index.md` - Overview
- `docs/decisions/ADR-001-*.md` through `ADR-00N-*.md` - Decision records
