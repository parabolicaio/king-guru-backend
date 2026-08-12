import os
import re
from logging.config import fileConfig
from pathlib import Path

from dotenv import load_dotenv
from alembic import context

# Load backend/.env so DATABASE_URL is available when running alembic directly.
load_dotenv(Path(__file__).parent.parent / ".env")

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---------------------------------------------------------------------------
# DB URL
# ---------------------------------------------------------------------------
# Read DATABASE_URL from the environment. We do NOT import app.core.config
# here to keep the migration runner dependency-free from the application.
#
# asyncpg  (runtime)  uses: postgresql://...
# psycopg2 (Alembic)  needs: postgresql+psycopg2://...
#
# We pass the URL directly to SQLAlchemy (not via config.set_main_option) to
# avoid configparser interpolation errors on passwords containing $ or %.
_raw_url = os.environ.get("DATABASE_URL", "")
if not _raw_url:
    raise RuntimeError(
        "DATABASE_URL environment variable is not set.\n"
        "Copy backend/.env.example to backend/.env and fill in your "
        "Supabase connection string, then re-run alembic."
    )
_migration_url = re.sub(
    r"^postgresql(\+asyncpg)?://",
    "postgresql+psycopg2://",
    _raw_url,
)

# ---------------------------------------------------------------------------
# Autogenerate is DISABLED.
# All migrations are hand-written plain SQL via op.execute("...").
# ---------------------------------------------------------------------------
target_metadata = None


def run_migrations_offline() -> None:
    """Emit SQL to stdout without a live DB connection (for code review)."""
    context.configure(
        url=_migration_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Execute migrations against a live DB connection."""
    from sqlalchemy import create_engine, pool

    # create_engine receives the URL directly — bypasses configparser so
    # passwords containing $ or % are never misinterpreted as interpolation.
    connectable = create_engine(_migration_url, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
