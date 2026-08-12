"""Pydantic schemas for app-meta endpoints (feature flags, version gate)."""

from pydantic import BaseModel


class AppMetaResponse(BaseModel):
    min_mobile_version: str
    latest_mobile_version: str
