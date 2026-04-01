from uuid import uuid4

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.identity.use_cases.get_current_user import GetCurrentUserUseCase
from app.application.identity.use_cases.request_otp_login import RequestOtpLoginUseCase
from app.application.identity.use_cases.verify_otp_login import VerifyOtpLoginUseCase
from app.core.config import settings
from app.infrastructure.db import get_db_session
from app.infrastructure.persistence.otp_repository import OtpRepository
from app.infrastructure.security.dependencies import require_current_claims
from app.infrastructure.security.jwt_service import JwtService
from app.infrastructure.security.otp_service import OtpService
from app.presentation.api.schemas.auth import MeResponse
from app.presentation.api.schemas.auth import OtpRequestPayload
from app.presentation.api.schemas.auth import OtpRequestResponse
from app.presentation.api.schemas.auth import OtpVerifyPayload
from app.presentation.api.schemas.auth import OtpVerifyResponse


router = APIRouter(prefix="/auth", tags=["auth"])


def _request_id() -> str:
    return f"req_{uuid4().hex[:12]}"


@router.post("/otp/request", response_model=OtpRequestResponse, status_code=status.HTTP_202_ACCEPTED)
async def request_otp(
    payload: OtpRequestPayload,
    request: Request,
    session: AsyncSession = Depends(get_db_session),
) -> OtpRequestResponse:
    repository = OtpRepository(session)
    use_case = RequestOtpLoginUseCase(repository=repository, otp_service=OtpService())

    try:
        await use_case.execute(email=str(payload.email), requested_ip=request.client.host if request.client else None)
        await session.commit()
    except ValueError as exc:
        await session.rollback()
        if str(exc) in {"rate_limited_email", "rate_limited_ip", "cooldown_active"}:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="rate limit exceeded")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid payload")

    return OtpRequestResponse(
        data={"message": "If the account exists, an OTP was sent"},
        meta={"request_id": _request_id()},
    )


@router.post("/otp/verify", response_model=OtpVerifyResponse)
async def verify_otp(
    payload: OtpVerifyPayload,
    response: Response,
    session: AsyncSession = Depends(get_db_session),
) -> OtpVerifyResponse:
    repository = OtpRepository(session)
    use_case = VerifyOtpLoginUseCase(
        repository=repository,
        otp_service=OtpService(),
        jwt_service=JwtService(),
    )

    try:
        result = await use_case.execute(email=str(payload.email), otp_code=payload.otp_code)
        await session.commit()
    except ValueError:
        await session.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="otp invalid or expired")

    response.set_cookie(
        key="access_token",
        value=result["access_token"],
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.JWT_ACCESS_TOKEN_EXPIRES_MINUTES * 60,
    )

    return OtpVerifyResponse(data=result, meta={"request_id": _request_id()})


@router.get("/me", response_model=MeResponse)
async def me(
    claims: dict = Depends(require_current_claims),
    session: AsyncSession = Depends(get_db_session),
) -> MeResponse:
    repository = OtpRepository(session)
    use_case = GetCurrentUserUseCase(repository=repository)

    try:
        user = await use_case.execute(subject=claims["sub"], role=claims["role"])
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not found")

    return MeResponse(data=user, meta={"request_id": _request_id()})
