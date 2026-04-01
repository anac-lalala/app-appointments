from datetime import datetime
from datetime import timedelta
from datetime import timezone
import hashlib
import uuid

from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import or_
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.infrastructure.persistence.models import AdminUser
from app.infrastructure.persistence.models import Client
from app.infrastructure.persistence.models import OtpChallenge


class OtpRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def is_rate_limited_by_email(self, email: str) -> bool:
        now = datetime.now(timezone.utc)
        window_start = now - timedelta(hours=1)

        query = select(func.count()).select_from(OtpChallenge).where(
            and_(OtpChallenge.email == email, OtpChallenge.created_at >= window_start)
        )
        count = (await self.session.execute(query)).scalar_one()
        return count >= 5

    async def is_rate_limited_by_ip(self, ip: str | None) -> bool:
        if not ip:
            return False

        now = datetime.now(timezone.utc)
        window_start = now - timedelta(minutes=15)
        ip_hash = hashlib.sha256(ip.encode("utf-8")).hexdigest()

        query = select(func.count()).select_from(OtpChallenge).where(
            and_(OtpChallenge.requested_ip_hash == ip_hash, OtpChallenge.created_at >= window_start)
        )
        count = (await self.session.execute(query)).scalar_one()
        return count >= 10

    async def is_cooldown_active(self, email: str) -> bool:
        latest_query = (
            select(OtpChallenge.created_at)
            .where(OtpChallenge.email == email)
            .order_by(OtpChallenge.created_at.desc())
            .limit(1)
        )
        latest_created_at = (await self.session.execute(latest_query)).scalar_one_or_none()

        if latest_created_at is None:
            return False

        now = datetime.now(timezone.utc)
        return (now - latest_created_at).total_seconds() < settings.OTP_COOLDOWN_SECONDS

    async def invalidate_active_challenges(self, email: str) -> None:
        now = datetime.now(timezone.utc)
        stmt = (
            update(OtpChallenge)
            .where(
                and_(
                    OtpChallenge.email == email,
                    OtpChallenge.used_at.is_(None),
                    OtpChallenge.expires_at > now,
                )
            )
            .values(used_at=now)
        )
        await self.session.execute(stmt)

    async def create_challenge(self, email: str, otp_hash: str, requested_ip: str | None) -> OtpChallenge:
        now = datetime.now(timezone.utc)
        requested_ip_hash = hashlib.sha256(requested_ip.encode("utf-8")).hexdigest() if requested_ip else None
        challenge = OtpChallenge(
            id=uuid.uuid4(),
            email=email,
            otp_hash=otp_hash,
            expires_at=now + timedelta(seconds=settings.OTP_TTL_SECONDS),
            attempt_count=0,
            max_attempts=settings.OTP_MAX_ATTEMPTS,
            requested_ip_hash=requested_ip_hash,
        )
        self.session.add(challenge)
        await self.session.flush()
        return challenge

    async def get_latest_active_challenge(self, email: str) -> OtpChallenge | None:
        now = datetime.now(timezone.utc)
        query = (
            select(OtpChallenge)
            .where(
                and_(
                    OtpChallenge.email == email,
                    OtpChallenge.used_at.is_(None),
                    OtpChallenge.expires_at > now,
                    OtpChallenge.attempt_count < OtpChallenge.max_attempts,
                )
            )
            .order_by(OtpChallenge.created_at.desc())
            .limit(1)
        )
        return (await self.session.execute(query)).scalar_one_or_none()

    async def increment_attempt(self, challenge: OtpChallenge) -> None:
        challenge.attempt_count += 1
        await self.session.flush()

    async def mark_used(self, challenge: OtpChallenge) -> None:
        challenge.used_at = datetime.now(timezone.utc)
        await self.session.flush()

    async def resolve_identity(self, email: str) -> tuple[str, str, str]:
        admin_query = select(AdminUser).where(and_(AdminUser.email == email, AdminUser.is_active.is_(True))).limit(1)
        admin = (await self.session.execute(admin_query)).scalar_one_or_none()
        if admin:
            return str(admin.id), admin.email, "admin"

        client_query = select(Client).where(and_(Client.email == email, Client.is_active.is_(True))).limit(1)
        client = (await self.session.execute(client_query)).scalar_one_or_none()
        if client:
            return str(client.id), client.email, "client"

        client = Client(
            id=uuid.uuid4(),
            email=email,
            full_name=None,
            phone=None,
            is_active=True,
        )
        self.session.add(client)
        await self.session.flush()
        return str(client.id), client.email, "client"

    async def get_identity_by_subject(self, subject: str, role: str) -> tuple[str, str, str] | None:
        try:
            subject_uuid = uuid.UUID(subject)
        except ValueError:
            return None

        if role == "admin":
            query = select(AdminUser).where(and_(AdminUser.id == subject_uuid, AdminUser.is_active.is_(True))).limit(1)
            admin = (await self.session.execute(query)).scalar_one_or_none()
            if admin:
                return str(admin.id), admin.email, "admin"
            return None

        query = select(Client).where(and_(Client.id == subject_uuid, Client.is_active.is_(True))).limit(1)
        client = (await self.session.execute(query)).scalar_one_or_none()
        if client:
            return str(client.id), client.email, "client"
        return None
