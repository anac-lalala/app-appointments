from app.infrastructure.persistence.otp_repository import OtpRepository
from app.infrastructure.security.otp_service import OtpService


class RequestOtpLoginUseCase:
    def __init__(self, repository: OtpRepository, otp_service: OtpService):
        self.repository = repository
        self.otp_service = otp_service

    async def execute(self, email: str, requested_ip: str | None) -> None:
        if await self.repository.is_rate_limited_by_email(email):
            raise ValueError("rate_limited_email")

        if await self.repository.is_rate_limited_by_ip(requested_ip):
            raise ValueError("rate_limited_ip")

        if await self.repository.is_cooldown_active(email):
            raise ValueError("cooldown_active")

        await self.repository.invalidate_active_challenges(email)
        otp_code = self.otp_service.generate_code()
        otp_hash = self.otp_service.hash_code(otp_code)

        await self.repository.create_challenge(email=email, otp_hash=otp_hash, requested_ip=requested_ip)

        # TODO: send OTP via SMTP service.
