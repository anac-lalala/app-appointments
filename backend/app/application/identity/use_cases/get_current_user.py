from app.infrastructure.persistence.otp_repository import OtpRepository


class GetCurrentUserUseCase:
    def __init__(self, repository: OtpRepository):
        self.repository = repository

    async def execute(self, subject: str, role: str) -> dict:
        identity = await self.repository.get_identity_by_subject(subject=subject, role=role)
        if not identity:
            raise ValueError("user_not_found")

        user_id, email, resolved_role = identity
        return {
            "id": user_id,
            "email": email,
            "role": resolved_role,
        }
