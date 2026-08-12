from datetime import datetime

from pydantic import BaseModel, field_validator


class SessionRequest(BaseModel):
    guest_token: str | None = None


class GuestSessionRequest(BaseModel):
    guest_token: str

    @field_validator("guest_token")
    @classmethod
    def validate_uuid_format(cls, v: str) -> str:
        import re
        uuid_re = re.compile(
            r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            re.IGNORECASE,
        )
        if not uuid_re.match(v):
            raise ValueError("guest_token must be a valid UUID")
        return v.lower()


class GuestSessionResponse(BaseModel):
    user_id: str
    guest_token: str
    created_at: datetime


class CheckPhoneResponse(BaseModel):
    exists: bool
