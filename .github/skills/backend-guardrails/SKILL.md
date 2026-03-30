---
name: backend-guardrails
description: "Use when implementing or reviewing FastAPI backend code, domain modules, use cases, repositories, transactions, and API contract compliance."
---

# Backend Guardrails

Goal
- Keep backend implementation consistent with modular monolith boundaries and stable contracts.

Use when
- You add or modify endpoints.
- You write use cases, repositories, or domain logic.
- You implement reservation concurrency or state transitions.

Required inputs
- Phase context from docs/implementacion.md.
- API contract from docs/api.md.
- Security constraints from docs/security.md.

Architecture rules
- Keep clear boundaries: presentation, application, domain, infrastructure.
- Routers map transport only.
- Use cases orchestrate business behavior.
- Domain holds core rules and valid state transitions.
- Infrastructure handles persistence and integrations.

Contract and data rules
- Use UUID identifiers and UTC timestamps.
- Respect API envelope and status codes.
- Validate inputs strictly.
- Keep role checks enforced in backend for admin operations.

Critical backend checks
- OTP challenge storage uses hash only.
- OTP verify enforces expiration, max attempts, and single use.
- Booking endpoint is atomic and concurrency-safe.
- Appointment status transitions are explicit and validated.

Minimum test obligations
- Auth success and failure cases.
- OTP expiration and reuse denial.
- Reservation concurrency test for same time block.
- Admin authorization and transition validation.

Do not
- Put business rules directly in routers.
- Bypass transactions in booking operations.
- Change contract shape without docs synchronization.
