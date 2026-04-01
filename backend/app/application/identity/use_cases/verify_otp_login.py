from app.core.config import settings
from app.infrastructure.persistence.otp_repository import OtpRepository
from app.infrastructure.security.jwt_service import JwtService
from app.infrastructure.security.otp_service import OtpService


class VerifyOtpLoginUseCase:
    def __init__(self, repository: OtpRepository, otp_service: OtpService, jwt_service: JwtService):
        self.repository = repository
        self.otp_service = otp_service
        self.jwt_service = jwt_service

    async def execute(self, email: str, otp_code: str) -> dict:
        challenge = await self.repository.get_latest_active_challenge(email)
        if not challenge:
            raise ValueError("invalid_or_expired_otp")

        if not self.otp_service.verify_code(otp_code, challenge.otp_hash):
            await self.repository.increment_attempt(challenge)
            raise ValueError("invalid_or_expired_otp")

        await self.repository.mark_used(challenge)

        user_id, user_email, role = await self.repository.resolve_identity(email)
        token = self.jwt_service.create_access_token(subject=user_id, role=role)

        return {
            "access_token": token,
            "token_type": "Bearer",
            "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRES_MINUTES * 60,
            "user": {
                "id": user_id,
                "email": user_email,
                "role": role,
            },
        }
