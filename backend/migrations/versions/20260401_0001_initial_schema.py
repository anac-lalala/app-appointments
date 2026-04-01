"""initial schema

Revision ID: 20260401_0001
Revises: 
Create Date: 2026-04-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "20260401_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "admin_users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email", sa.Text(), nullable=False),
        sa.Column("full_name", sa.Text(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email", name="uq_admin_users_email"),
    )

    op.create_table(
        "clients",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email", sa.Text(), nullable=False),
        sa.Column("full_name", sa.Text(), nullable=True),
        sa.Column("phone", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email", name="uq_clients_email"),
    )

    op.create_table(
        "otp_challenges",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email", sa.Text(), nullable=False),
        sa.Column("otp_hash", sa.Text(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("attempt_count", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("max_attempts", sa.Integer(), nullable=False, server_default=sa.text("5")),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("requested_ip_hash", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("attempt_count >= 0", name="ck_otp_attempt_count_non_negative"),
        sa.CheckConstraint("max_attempts > 0", name="ck_otp_max_attempts_positive"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_otp_email_created", "otp_challenges", ["email", "created_at"], unique=False)

    op.create_table(
        "services",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("duration_minutes", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_by_admin_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("duration_minutes > 0", name="ck_services_duration_positive"),
        sa.ForeignKeyConstraint(
            ["created_by_admin_id"],
            ["admin_users.id"],
            ondelete="RESTRICT",
            onupdate="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_services_is_active", "services", ["is_active"], unique=False)

    op.create_table(
        "service_availability_rules",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("service_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("weekday", sa.SmallInteger(), nullable=False),
        sa.Column("start_time", sa.Time(), nullable=False),
        sa.Column("end_time", sa.Time(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("weekday BETWEEN 0 AND 6", name="ck_rules_weekday_range"),
        sa.CheckConstraint("start_time < end_time", name="ck_rules_start_before_end"),
        sa.ForeignKeyConstraint(["service_id"], ["services.id"], ondelete="RESTRICT", onupdate="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_rules_service_weekday", "service_availability_rules", ["service_id", "weekday"], unique=False)

    op.create_table(
        "service_time_blocks",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("service_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("start_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default=sa.text("'available'")),
        sa.Column("generated_from_rule_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("start_at < end_at", name="ck_blocks_start_before_end"),
        sa.CheckConstraint("status IN ('available','blocked','cancelled')", name="ck_blocks_status"),
        sa.ForeignKeyConstraint(["generated_from_rule_id"], ["service_availability_rules.id"], ondelete="RESTRICT", onupdate="RESTRICT"),
        sa.ForeignKeyConstraint(["service_id"], ["services.id"], ondelete="RESTRICT", onupdate="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("service_id", "start_at", "end_at", name="uq_blocks_service_range"),
    )
    op.create_index("idx_blocks_service_start", "service_time_blocks", ["service_id", "start_at"], unique=False)
    op.create_index("idx_blocks_status_start", "service_time_blocks", ["status", "start_at"], unique=False)

    op.create_table(
        "appointments",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("client_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("service_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("service_time_block_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default=sa.text("'pending_review'")),
        sa.Column("client_name_snapshot", sa.Text(), nullable=False),
        sa.Column("client_email_snapshot", sa.Text(), nullable=False),
        sa.Column("client_phone_snapshot", sa.Text(), nullable=True),
        sa.Column("confirmed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cancelled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cancel_reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("status IN ('pending_review','confirmed','cancelled')", name="ck_appointments_status"),
        sa.CheckConstraint("confirmed_at IS NULL OR status = 'confirmed'", name="ck_appointments_confirmed_state"),
        sa.CheckConstraint("cancelled_at IS NULL OR status = 'cancelled'", name="ck_appointments_cancelled_state"),
        sa.ForeignKeyConstraint(["client_id"], ["clients.id"], ondelete="RESTRICT", onupdate="RESTRICT"),
        sa.ForeignKeyConstraint(["service_id"], ["services.id"], ondelete="RESTRICT", onupdate="RESTRICT"),
        sa.ForeignKeyConstraint(["service_time_block_id"], ["service_time_blocks.id"], ondelete="RESTRICT", onupdate="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_appointments_client_created", "appointments", ["client_id", "created_at"], unique=False)
    op.create_index("idx_appointments_status_created", "appointments", ["status", "created_at"], unique=False)
    op.create_index(
        "uq_active_appointment_per_block",
        "appointments",
        ["service_time_block_id"],
        unique=True,
        postgresql_where=sa.text("status IN ('pending_review','confirmed')"),
    )


def downgrade() -> None:
    op.drop_index("uq_active_appointment_per_block", table_name="appointments")
    op.drop_index("idx_appointments_status_created", table_name="appointments")
    op.drop_index("idx_appointments_client_created", table_name="appointments")
    op.drop_table("appointments")

    op.drop_index("idx_blocks_status_start", table_name="service_time_blocks")
    op.drop_index("idx_blocks_service_start", table_name="service_time_blocks")
    op.drop_table("service_time_blocks")

    op.drop_index("idx_rules_service_weekday", table_name="service_availability_rules")
    op.drop_table("service_availability_rules")

    op.drop_index("idx_services_is_active", table_name="services")
    op.drop_table("services")

    op.drop_index("idx_otp_email_created", table_name="otp_challenges")
    op.drop_table("otp_challenges")

    op.drop_table("clients")
    op.drop_table("admin_users")
