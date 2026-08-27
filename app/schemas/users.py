from datetime import datetime

from pydantic import BaseModel, field_validator

_AGE_GROUPS = ("under_15", "15_18", "19_25", "26_40", "40_plus")
_ROLE_TAGS = ("school_student", "university_student", "working_adult", "other")
_LANGUAGES = ("en", "si")
_ENGLISH_LEVELS = ("none", "little", "conversational", "good")


class UserProfile(BaseModel):
    """Full user profile — returned by GET /users/me and POST /auth/session."""

    id: str
    email: str | None
    phone: str | None
    full_name: str
    display_name: str | None
    avatar_url: str | None
    age_group: str | None
    role_tag: str | None
    english_level: str | None
    language_preference: str
    admin_role: str | None
    subscription_tier: str
    xp_total: int
    streak_current: int
    streak_longest: int
    onboarding_completed: bool
    placement_completed: bool
    current_level_id: str | None
    current_level_name: str | None
    deleted_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class UpdateProfileRequest(BaseModel):
    display_name: str | None = None
    avatar_url: str | None = None
    age_group: str | None = None
    role_tag: str | None = None
    english_level: str | None = None
    language_preference: str | None = None

    @field_validator("age_group")
    @classmethod
    def validate_age_group(cls, v: str | None) -> str | None:
        if v is not None and v not in _AGE_GROUPS:
            raise ValueError(f"age_group must be one of: {', '.join(_AGE_GROUPS)}")
        return v

    @field_validator("role_tag")
    @classmethod
    def validate_role_tag(cls, v: str | None) -> str | None:
        if v is not None and v not in _ROLE_TAGS:
            raise ValueError(f"role_tag must be one of: {', '.join(_ROLE_TAGS)}")
        return v

    @field_validator("english_level")
    @classmethod
    def validate_english_level(cls, v: str | None) -> str | None:
        if v is not None and v not in _ENGLISH_LEVELS:
            raise ValueError(f"english_level must be one of: {', '.join(_ENGLISH_LEVELS)}")
        return v

    @field_validator("language_preference")
    @classmethod
    def validate_language(cls, v: str | None) -> str | None:
        if v is not None and v not in _LANGUAGES:
            raise ValueError(f"language_preference must be one of: {', '.join(_LANGUAGES)}")
        return v


class OnboardingRequest(BaseModel):
    full_name: str
    age_group: str
    role_tag: str
    english_level: str
    language_preference: str

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("full_name must not be blank")
        return v.strip()

    @field_validator("age_group")
    @classmethod
    def validate_age_group(cls, v: str) -> str:
        if v not in _AGE_GROUPS:
            raise ValueError(f"age_group must be one of: {', '.join(_AGE_GROUPS)}")
        return v

    @field_validator("role_tag")
    @classmethod
    def validate_role_tag(cls, v: str) -> str:
        if v not in _ROLE_TAGS:
            raise ValueError(f"role_tag must be one of: {', '.join(_ROLE_TAGS)}")
        return v

    @field_validator("english_level")
    @classmethod
    def validate_english_level(cls, v: str) -> str:
        if v not in _ENGLISH_LEVELS:
            raise ValueError(f"english_level must be one of: {', '.join(_ENGLISH_LEVELS)}")
        return v

    @field_validator("language_preference")
    @classmethod
    def validate_language(cls, v: str) -> str:
        if v not in _LANGUAGES:
            raise ValueError(f"language_preference must be one of: {', '.join(_LANGUAGES)}")
        return v


class OnboardingResponse(BaseModel):
    onboarding_completed_at: datetime


class SignupRequest(BaseModel):
    """Body for POST /auth/signup — first-time account creation."""

    guest_token: str | None = None
    full_name: str
    age_group: str
    role_tag: str
    english_level: str
    language_preference: str
    placement_level_id: str | None = None

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("full_name must not be blank")
        return v.strip()

    @field_validator("age_group")
    @classmethod
    def validate_age_group(cls, v: str) -> str:
        if v not in _AGE_GROUPS:
            raise ValueError(f"age_group must be one of: {', '.join(_AGE_GROUPS)}")
        return v

    @field_validator("role_tag")
    @classmethod
    def validate_role_tag(cls, v: str) -> str:
        if v not in _ROLE_TAGS:
            raise ValueError(f"role_tag must be one of: {', '.join(_ROLE_TAGS)}")
        return v

    @field_validator("english_level")
    @classmethod
    def validate_english_level(cls, v: str) -> str:
        if v not in _ENGLISH_LEVELS:
            raise ValueError(f"english_level must be one of: {', '.join(_ENGLISH_LEVELS)}")
        return v

    @field_validator("language_preference")
    @classmethod
    def validate_language(cls, v: str) -> str:
        if v not in _LANGUAGES:
            raise ValueError(f"language_preference must be one of: {', '.join(_LANGUAGES)}")
        return v
