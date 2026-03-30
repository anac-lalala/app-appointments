---
name: implementation-flow
description: "Use when planning or implementing any MVP phase, vertical slice sequencing, dependency mapping, or delivery checkpoints for phases 0 to 6."
---

# Implementation Flow

Goal
- Produce executable phase plans and slice sequencing for the MVP.

Use when
- You need a realistic implementation plan.
- You need to split work by phases 0 to 6.
- You need to coordinate frontend and backend without blocking.

Required inputs
- Target phase and objective.
- Current constraints and dependencies.
- Relevant contracts from docs/api.md and guardrails from docs/security.md.

Process
1. Confirm target phase and direct dependencies.
2. Define one visible deliverable for the phase.
3. Split into backend tasks, frontend tasks, and integration checks.
4. Add minimum tests and risk mitigations.
5. Define acceptance criteria and closure evidence.

Phase template
- objective
- scope
- dependencies
- backend tasks
- frontend tasks
- integration tasks
- risks and mitigations
- minimum tests
- acceptance criteria
- closure evidence

Output contract
- Return a concise phase plan using the template.
- Include explicit do and do not statements.
- Keep all values aligned with AGENTS.md invariants.

Do not
- Propose microservices.
- Add enterprise-level features outside MVP scope.
- Skip dependency order or mix unrelated phases.
