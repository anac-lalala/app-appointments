from fastapi import Cookie
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException
from fastapi import status

from app.infrastructure.security.jwt_service import JwtService


def _extract_bearer_token(authorization: str | None) -> str | None:
    if not authorization:
        return None
    prefix = "Bearer "
    if not authorization.startswith(prefix):
        return None
    return authorization[len(prefix) :]


def get_current_claims(
    authorization: str | None = Header(default=None),
    access_token: str | None = Cookie(default=None),
) -> dict:
    token = _extract_bearer_token(authorization) or access_token
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not authenticated")

    jwt_service = JwtService()
    try:
        claims = jwt_service.decode_access_token(token)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")

    if "sub" not in claims or "role" not in claims:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token payload")

    return claims


def require_current_claims(claims: dict = Depends(get_current_claims)) -> dict:
    return claims
