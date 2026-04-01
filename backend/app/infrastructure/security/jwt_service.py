from datetime import datetime
from datetime import timedelta
from datetime import timezone

from jose import JWTError
from jose import jwt

from app.core.config import settings


class JwtService:
    def create_access_token(self, subject: str, role: str) -> str:
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRES_MINUTES)
        payload = {
            "sub": subject,
            "role": role,
            "iat": int(now.timestamp()),
            "exp": int(expires_at.timestamp()),
        }
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    def decode_access_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except JWTError as exc:
            raise ValueError("invalid token") from exc
