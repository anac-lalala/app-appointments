---
name: security-review
description: "Use when reviewing authentication, authorization, token handling, endpoint abuse protections, logging hygiene, and sensitive data exposure risks."
---

# Security Review

Goal
- Block insecure changes and enforce MVP security baseline before approval.

Use when
- Auth, OTP, JWT, or access control code changes.
- Admin endpoints or sensitive data handling changes.
- Release readiness checks for a phase.

Required inputs
- Changed behavior and endpoint list.
- Expected controls from docs/security.md.
- Related contracts from docs/api.md.

Blocking checks
- OTP TTL is 5 minutes.
- OTP max attempts per challenge is 5.
- OTP cooldown per email is 60 seconds.
- OTP rate limits are enforced for IP and email.
- OTP data is hashed, not stored in plaintext.
- JWT access token lifetime is 30 minutes.
- Frontend token storage is HttpOnly Secure SameSite=Lax cookie.
- Admin routes enforce role checks in backend.
- Logs do not leak OTP, full JWT, auth headers, or raw cookies.
- CORS is restricted to known frontend origins.

Review output format
- status: approved or changes requested
- blocking findings: list with severity and exact remediation
- non-blocking recommendations: list
- verification checklist: pass or fail items

Do not
- Approve changes that weaken auth guarantees.
- Approve localStorage token storage.
- Approve missing backend authorization checks.
