import secrets

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class OtpService:
    def generate_code(self) -> str:
        return "".join(str(secrets.randbelow(10)) for _ in range(6))

    def hash_code(self, otp_code: str) -> str:
        return pwd_context.hash(otp_code)

    def verify_code(self, otp_code: str, otp_hash: str) -> bool:
        return pwd_context.verify(otp_code, otp_hash)
