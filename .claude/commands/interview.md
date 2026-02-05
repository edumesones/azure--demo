---
description: Deep interview process to define feature specification (spec-architect integration)
argument-hint: FEAT-XXX
allowed-tools: Read, Write, AskUserQuestionTool
---

# Interview Feature (Spec Architect Mode)

## Purpose

Transform a rough feature idea into a **professional technical specification** through exhaustive interviewing. This is NOT a superficial Q&A - it's a deep dive into requirements.

Based on the Spec Architect methodology.

## Usage

```
"Interview me about FEAT-001-auth"
/interview FEAT-001-auth
```

## Instructions

### 1. Read Context

```bash
# Read the feature spec (may be empty template or rough notes)
cat docs/features/$ARGUMENTS/spec.md
```

Also read related context if exists:
- `docs/project.md` - Project overview
- `docs/architecture/_index.md` - Technical constraints
- Related features that this depends on

### 2. The Interview Loop

**YOU MUST ASK QUESTIONS. DO NOT ASSUME.**

Interview in extreme detail about:

#### Technical Implementation
- Data models and relationships
- API design (endpoints, payloads, responses)
- State management
- Error handling strategies
- Performance requirements
- Security considerations

#### UI & UX Flows
- User journey step by step
- What does the user see at each state?
- Loading states, empty states, error states
- Mobile vs desktop considerations
- Accessibility requirements

#### Edge Cases and Concerns
- What happens when X fails?
- What if user does Y unexpectedly?
- Concurrent users/requests handling
- Data validation rules
- Rate limiting needs

#### Trade-offs
- Speed vs reliability
- Simplicity vs flexibility
- Build vs buy decisions
- Database choices
- Caching strategies

### Interview Constraints

```
CRITICAL INTERVIEW RULES

1. Questions must NOT be obvious
   BAD: "What should the login button say?"
   GOOD: "If OAuth fails mid-flow, should we retry silently or show error?"

2. Do NOT stop after one question
   Continue interviewing until YOU have a complete mental model

3. Maximum 3-4 questions per turn
   Give user time to think and respond

4. Provide options when possible
   "Do you want A) retry 3x silently, B) show error immediately, C) other?"

5. If user says "I don't know" or "you decide"
   Propose the most sensible default with reasoning
   Document it as "Claude recommended: X because Y"

6. Document EVERY decision immediately
   Update spec.md after each answer, not at the end
```

### 3. Update spec.md in Real Time

After EACH user response, update the spec.md file:

```markdown
## Technical Decisions

| # | Area | Question | Decision | Notes |
|---|------|----------|----------|-------|
| 1 | Auth | OAuth failure handling | Retry 3x then show error | Claude recommended |
| 2 | Session | Token duration | 24h with refresh | User specified |
| 3 | Security | Failed login limit | 5 attempts then 15min lockout | User specified |
```

### 4. Interview Completion Check

Before ending, verify you have answers for:

- [ ] All user stories defined
- [ ] All acceptance criteria clear
- [ ] Technical approach decided
- [ ] Edge cases documented
- [ ] Error handling defined
- [ ] Security considerations addressed
- [ ] Dependencies identified
- [ ] Out of scope clearly listed

Ask user: "I believe I have enough information to write the complete spec. Should I finalize it, or are there areas you want to discuss further?"

### 5. Final Output

When interview is complete:

1. Rewrite `docs/features/$ARGUMENTS/spec.md` with full professional specification
2. Update `docs/features/$ARGUMENTS/status.md`:
   - Phase: Interview completed
   - Interview completed: [date]
3. Update `docs/features/_index.md` if status changed

### 6. Transition to Plan

After finalizing spec, tell user:

```
Interview complete. spec.md has been updated with all decisions.

Next step: Run "/plan implement $ARGUMENTS" to create the technical design.
```

## Argument
$ARGUMENTS
