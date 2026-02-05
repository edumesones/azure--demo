---
description: Deep interview to define project fundamentals (vision, users, tech stack, constraints)
argument-hint:
allowed-tools: Read, Write, Bash(ls:*), Bash(cat:*)
---

# Project Interview

## Triggers

This command activates on:
- `/project-interview`
- "Interview me about this project"
- "Interview me about the project"
- "Let's define the project"
- "Help me define this project"

## Purpose

Before any coding, we need answers to:
- **What** are we building?
- **Who** is it for?
- **Why** does it need to exist?
- **How** will it work?
- **What** constraints exist?

## Instructions

1. **Read the skill file:**
   ```
   Read .claude/skills/project-interview/SKILL.md
   ```

2. **Check existing context:**
   ```bash
   cat docs/project.md 2>/dev/null
   ```

3. **Follow the interview protocol** from the skill file:
   - Start with Vision & Problem
   - Move to Users & Personas
   - Then Core Functionality
   - Then Technical Constraints
   - Finally Scope & Risks

4. **Rules:**
   - Max 3-4 questions per turn
   - Update docs/project.md after EACH response
   - Propose defaults for unknowns
   - Challenge vague answers

5. **When complete:**
   - Verify all sections of project.md are filled
   - Suggest next step: "Help me define the architecture"

## Output

Updates `docs/project.md` with complete project definition.
