from typing import Literal

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class MetaResponse(BaseModel):
    request_id: str


class ErrorResponse(BaseModel):
    error: dict
    meta: MetaResponse


class OtpRequestPayload(BaseModel):
    email: EmailStr


class OtpRequestData(BaseModel):
    message: str


class OtpRequestResponse(BaseModel):
    data: OtpRequestData
    meta: MetaResponse


class OtpVerifyPayload(BaseModel):
    email: EmailStr
    otp_code: str = Field(min_length=6, max_length=6, pattern=r"^\d{6}$")


class UserPayload(BaseModel):
    id: str
    email: EmailStr
    role: Literal["client", "admin"]


class OtpVerifyData(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    user: UserPayload


class OtpVerifyResponse(BaseModel):
    data: OtpVerifyData
    meta: MetaResponse


class MeResponse(BaseModel):
    data: UserPayload
    meta: MetaResponse
