"""Admin user management endpoints (B8)."""

from uuid import UUID

import asyncpg
from fastapi import APIRouter, Depends, Response

from app.core.errors import AppError, CANNOT_DELETE_SELF, CANNOT_DEMOTE_SELF, USER_NOT_FOUND
from app.core.security import get_admin_user
from app.db.pool import get_db
from app.db.queries.admin_users import (
    get_recent_xp_ledger,
    get_user_with_progress,
    list_users,
    update_user_role,
)
from app.schemas.admin_users import (
    AdminUserDetail,
    AdminUserListItem,
    AdminUserListResponse,
    UpdateRoleRequest,
    UpdateRoleResponse,
    XPLedgerEntryAdmin,
)
from app.services import audit_service, user_service

router = APIRouter(prefix="/api/v1/admin/users", tags=["admin-users"])


def _row_to_list_item(row: asyncpg.Record) -> AdminUserListItem:
    return AdminUserListItem(
        id=row["id"],
        full_name=row["full_name"],
        email=row["email"],
        phone=row["phone"],
        auth_provider=row["auth_provider"],
        admin_role=row["admin_role"],
        subscription_tier=row["subscription_tier"],
        xp_total=row["xp_total"],
        streak_current=row["streak_current"],
        onboarding_completed=row["onboarding_completed_at"] is not None,
        placement_completed=row["placement_completed_at"] is not None,
        current_level_id=row["current_level_id"],
        created_at=row["created_at"],
        deleted_at=row["deleted_at"],
    )


@router.get("", response_model=AdminUserListResponse)
async def list_users_endpoint(
    search: str | None = None,
    auth_provider: str | None = None,
    subscription_tier: str | None = None,
    admin_role: str | None = None,
    level_code: str | None = None,
    active_only: bool = True,
    page: int = 1,
    page_size: int = 20,
    user: asyncpg.Record = Depends(get_admin_user),
    db: asyncpg.Connection = Depends(get_db),
) -> AdminUserListResponse:
    rows, total = await list_users(
        db,
        page=page,
        page_size=page_size,
        search=search,
        auth_provider=auth_provider,
        subscription_tier=subscription_tier,
        admin_role=admin_role,
        level_code=level_code,
        active_only=active_only,
    )
    return AdminUserListResponse(
        data=[_row_to_list_item(r) for r in rows],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{user_id}", response_model=AdminUserDetail)
async def get_user_endpoint(
    user_id: UUID,
    admin: asyncpg.Record = Depends(get_admin_user),
    db: asyncpg.Connection = Depends(get_db),
) -> AdminUserDetail:
    row = await get_user_with_progress(db, str(user_id))
    if row is None:
        raise AppError(*USER_NOT_FOUND)

    ledger_rows = await get_recent_xp_ledger(db, str(user_id), limit=10)

    return AdminUserDetail(
        **_row_to_list_item(row).model_dump(),
        completed_lesson_count=row["completed_lesson_count"],
        recent_xp_ledger=[
            XPLedgerEntryAdmin(
                action_type=r["action_type"],
                xp_delta=r["xp_delta"],
                reference_type=r["reference_type"],
                reference_id=r["reference_id"],
                awarded_at=r["awarded_at"],
            )
            for r in ledger_rows
        ],
    )


@router.patch("/{user_id}/role", response_model=UpdateRoleResponse)
async def update_role_endpoint(
    user_id: UUID,
    body: UpdateRoleRequest,
    admin: asyncpg.Record = Depends(get_admin_user),
    db: asyncpg.Connection = Depends(get_db),
) -> UpdateRoleResponse:
    if str(user_id) == str(admin["id"]):
        raise AppError(*CANNOT_DEMOTE_SELF)

    target = await get_user_with_progress(db, str(user_id))
    if target is None:
        raise AppError(*USER_NOT_FOUND)

    row = await update_user_role(db, str(user_id), body.admin_role)

    # Update Supabase JWT claim
    from app.core import supabase_admin
    if target.get("supabase_uid"):
        await supabase_admin.update_admin_role_claim(str(target["supabase_uid"]), body.admin_role)

    await audit_service.log(
        db,
        action="user.role_changed",
        actor_id=str(admin["id"]),
        target_type="user",
        target_id=str(user_id),
    )

    return UpdateRoleResponse(
        id=row["id"],
        admin_role=row["admin_role"],
        updated_at=row["updated_at"],
    )


@router.delete("/{user_id}", status_code=204)
async def delete_user_endpoint(
    user_id: UUID,
    admin: asyncpg.Record = Depends(get_admin_user),
    db: asyncpg.Connection = Depends(get_db),
) -> Response:
    if str(user_id) == str(admin["id"]):
        raise AppError(*CANNOT_DELETE_SELF)

    target = await get_user_with_progress(db, str(user_id))
    if target is None:
        raise AppError(*USER_NOT_FOUND)

    await user_service.delete_account(
        db,
        user_id=str(user_id),
        supabase_uid=str(target["supabase_uid"]),
    )

    await audit_service.log(
        db,
        action="user.deleted",
        actor_id=str(admin["id"]),
        target_type="user",
        target_id=str(user_id),
    )

    return Response(status_code=204)
