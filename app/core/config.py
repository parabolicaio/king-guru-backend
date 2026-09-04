from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env.local",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Database ---
    # asyncpg accepts postgresql:// directly.
    # alembic/env.py converts to postgresql+psycopg2:// for migration runs.
    database_url: str

    # --- Supabase ---
    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str
    # Used server-side to verify JWTs without hitting the Supabase Auth API per-request.
    supabase_jwt_secret: str

    # --- CDN ---
    # Backend appends storage paths to this prefix when building response URLs.
    # Default points at local Supabase dev instance.
    cdn_base_url: str = "http://localhost:54321/storage/v1/object/public"

    # --- Azure Neural TTS (Phase 1 — vocabulary words/phrases) ---
    azure_tts_key: str = ""
    azure_tts_region: str = "eastus"

    # --- AI (Phase 2+) ---
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"

    # --- SMS (text.lk) ---
    # API key from text.lk dashboard. Required in production.
    text_lk_api_key: str = ""
    # Alphanumeric sender ID shown to recipients (max 11 chars).
    text_lk_sender_id: str = "KingGuru"
    # Shared secret configured in Supabase → Auth → Hooks → Send SMS.
    # Used to verify that incoming hook requests genuinely come from Supabase.
    supabase_hook_secret: str = ""

    # --- Sentry (optional; disabled when empty) ---
    sentry_dsn: str = ""

    # --- OnePay (payment gateway) ---
    # From your OnePay merchant dashboard — sandbox and live each have their
    # own App ID/Hash Salt pair. Hash Salt is a secret: server-side only,
    # never sent to the frontend or included in any client-visible response.
    onepay_app_id: str = ""
    onepay_hash_salt: str = ""
    # Not documented on OnePay's public docs site at all — discovered live:
    # requests without an Authorization header 401 with "Please provide
    # request headers". Whatever your dashboard calls "App Token" goes here.
    onepay_app_token: str = ""
    onepay_base_url: str = "https://api.onepay.lk"
    # Where the frontend sends the customer after they finish on OnePay's
    # hosted page — the frontend route that polls our own payment status.
    onepay_redirect_url: str = "http://localhost:5173/payment/return"

    # --- App ---
    app_env: str = "production"
    # Comma-separated list of allowed CORS origins, or "*" to allow all.
    cors_origins: str = "*"

    # --- Mobile version gate (Phase 5.2) ---
    # Bumped by the Release Manager per APK release — no redeploy required to
    # raise min_mobile_version and force sideloaded installs to update.
    min_mobile_version: str = "1.0.0"
    latest_mobile_version: str = "1.0.0"

    # ------------------------------------------------------------------ #
    # Derived properties                                                   #
    # ------------------------------------------------------------------ #

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def cors_origins_list(self) -> list[str]:
        if self.cors_origins.strip() == "*":
            return ["*"]
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    def build_cdn_url(self, storage_path: str | None) -> str | None:
        """Convert a Supabase Storage path to a full CDN URL.

        Returns None for null/empty paths so callers can pass audio_url
        and image_url directly without additional None-checks.
        """
        if not storage_path:
            return None
        return f"{self.cdn_base_url.rstrip('/')}/{storage_path.lstrip('/')}"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
