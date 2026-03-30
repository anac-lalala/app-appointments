# Citas App Agent System

Purpose
- Keep MVP implementation coherent across architecture, API, security, and phase roadmap.
- Maximize delivery speed without redesign loops.
- Enforce scope boundaries and non-negotiable technical constraints.

Project Canonical Context
- Frontend: Next.js App Router, TypeScript, Tailwind.
- Backend: FastAPI async, SQLAlchemy async, Alembic.
- Database: PostgreSQL.
- Auth: OTP by email plus JWT.
- Infra: Docker Compose for development and simple container deployment.
- Architecture: modular monolith with clear module boundaries.

MVP Scope Guardrails
- In scope: OTP login, service management, availability blocks, booking, admin appointment operations, hardening.
- Out of scope: multi-business, advanced RBAC, payments, complex external integrations, mobile native app, enterprise auth features.

Non-Negotiable Security and API Invariants
- OTP TTL: 5 minutes.
- OTP max attempts per challenge: 5.
- OTP cooldown per email: 60 seconds.
- OTP rate limit per IP: 10 requests per 15 minutes.
- OTP rate limit per email: 5 requests per hour.
- JWT access token TTL: 30 minutes.
- Frontend auth storage: HttpOnly Secure SameSite=Lax cookie.
- API response envelope: data and meta.request_id for success, error and meta.request_id for failures.
- Never log OTP values, full JWT tokens, auth headers, or raw cookies.

Phase-First Execution Policy
- Always execute by phases 0 to 6.
- Do not skip dependencies between phases.
- Freeze API contract per slice before parallel frontend and backend implementation.
- Close each phase with evidence: tests, demo path, and acceptance checks.

Agent Routing Matrix
- Use Implementation Flow skill when planning or executing phase work.
- Use Backend Guardrails skill when touching backend modules, use cases, repositories, or contracts.
- Use Security Review skill before approving auth, role checks, or sensitive data handling.
- Use Docs Sync skill whenever architecture, API behavior, security policy, or phase plans change.

Coordination Rules
- One critical slice at a time unless contracts are frozen and validated.
- No architectural redesign without explicit architecture decision.
- Keep responsibilities separated: routers for transport, use cases for orchestration, domain for business rules, infrastructure for integration.
- Frontend must not duplicate backend business logic.

Definition of Done for Any Feature
- Contract is explicit and respected.
- Access control and validation are implemented in backend.
- Critical tests exist for success and failure paths.
- Security invariants remain unchanged.
- Documentation is synchronized.

Preferred Output Style for AI
- Write clear, direct, imperative instructions.
- Include exact inputs, outputs, and acceptance criteria.
- Avoid vague guidance and avoid introducing optional architecture not required by MVP.
