"""Pydantic schemas for admin user management (B8)."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AdminUserListItem(BaseModel):
    id: UUID
    full_name: str
    email: str | None
    phone: str | None
    auth_provider: str | None
    admin_role: str | None
    subscription_tier: str
    xp_total: int
    streak_current: int
    onboarding_completed: bool
    placement_completed: bool
    current_level_id: UUID | None
    created_at: datetime
    deleted_at: datetime | None


class AdminUserListResponse(BaseModel):
    data: list[AdminUserListItem]
    total: int
    page: int
    page_size: int


class XPLedgerEntryAdmin(BaseModel):
    action_type: str
    xp_delta: int
    reference_type: str | None
    reference_id: UUID | None
    awarded_at: datetime


class AdminUserDetail(AdminUserListItem):
    completed_lesson_count: int
    recent_xp_ledger: list[XPLedgerEntryAdmin]


class UpdateRoleRequest(BaseModel):
    admin_role: str | None  # null | 'content_manager' | 'admin'


class UpdateRoleResponse(BaseModel):
    id: UUID
    admin_role: str | None
    updated_at: datetime
