from uuid6 import uuid7


def new_uuid() -> str:
    """Generate a UUIDv7 string for use as a database primary key.

    Call this function app-side and pass the result as a query parameter in
    every INSERT. Never use DEFAULT gen_random_uuid() or any DB-side UUID
    generator — UUIDv7 app-side generation is a hard convention per CLAUDE.md.

    UUIDv7 encodes a millisecond-precision Unix timestamp in the high bits,
    which makes primary keys monotonically increasing and index-friendly.
    """
    return str(uuid7())
