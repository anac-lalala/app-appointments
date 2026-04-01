from typing import Protocol


class OtpServicePort(Protocol):
    def generate_code(self) -> str:
        ...

    def hash_code(self, otp_code: str) -> str:
        ...

    def verify_code(self, otp_code: str, otp_hash: str) -> bool:
        ...


class JwtServicePort(Protocol):
    def create_access_token(self, subject: str, role: str) -> str:
        ...

    def decode_access_token(self, token: str) -> dict:
        ...
