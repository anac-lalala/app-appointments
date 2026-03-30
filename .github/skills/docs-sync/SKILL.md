---
name: docs-sync
description: "Use when code changes affect architecture, API contracts, security controls, implementation phases, or scope boundaries and documentation must be updated immediately."
---

# Docs Sync

Goal
- Keep documentation as an accurate source of truth after each relevant change.

Use when
- API request or response format changes.
- Security policy or auth behavior changes.
- Phase plan, dependencies, or acceptance criteria change.
- Scope in or scope out decisions change.

Required inputs
- What changed in behavior.
- Why it changed.
- Which phase and module are affected.

Sync targets
- docs/api.md for endpoint contract changes.
- docs/security.md for auth and control changes.
- docs/implementacion.md for phase and delivery changes.
- docs/architecture.md for boundary-level structural changes.
- docs/backend.md or docs/frontend.md for implementation conventions.

Update rules
- Preserve one source of truth per topic.
- Do not duplicate detailed content across multiple docs.
- Keep terms and values consistent with AGENTS.md invariants.
- Use clear changelog-style notes in updated sections when helpful.

Output contract
- list of updated documents
- summary of what changed and why
- consistency checks performed
- open questions or follow-up items

Do not
- Delay documentation updates until later phases.
- Introduce contradictory values across docs.
