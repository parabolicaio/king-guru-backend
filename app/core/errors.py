from fastapi import HTTPException


class AppError(HTTPException):
    """HTTPException that always uses the KG error envelope.

    Raise this instead of HTTPException anywhere in the app so responses
    always match { "error": { "code": "...", "message": "...", "details": {} } }.
    The exception handler in main.py unwraps detail into the correct shape.
    """

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        details: dict | None = None,
    ) -> None:
        super().__init__(
            status_code=status_code,
            detail={"code": code, "message": message, "details": details or {}},
        )


# ── Auth ─────────────────────────────────────────────────────────────────────
JWT_INVALID  = ("JWT_INVALID",  "Token is invalid.",              401)
JWT_EXPIRED  = ("JWT_EXPIRED",  "Token has expired.",             401)
UNAUTHORIZED = ("UNAUTHORIZED", "Authentication required.",       401)
FORBIDDEN    = ("FORBIDDEN",    "Insufficient permissions.",      403)
USER_DELETED = ("USER_DELETED", "This account has been deleted.", 401)

# ── Guest ────────────────────────────────────────────────────────────────────
GUEST_TOKEN_INVALID = ("GUEST_TOKEN_INVALID", "guest_token is not a valid UUID.", 400)
GUEST_TOKEN_EXPIRED = ("GUEST_TOKEN_EXPIRED", "Guest session has expired.",       401)
GUEST_ACCESS_DENIED = ("GUEST_ACCESS_DENIED", "This content requires sign-in.",   403)

# ── Validation ───────────────────────────────────────────────────────────────
VALIDATION_ERROR = ("VALIDATION_ERROR", "Request validation failed.", 422)

# ── User / onboarding ────────────────────────────────────────────────────────
ALREADY_ONBOARDED = ("ALREADY_ONBOARDED", "Onboarding already complete.", 409)
USER_NOT_FOUND    = ("USER_NOT_FOUND",    "User not found.",               404)
CANNOT_DEMOTE_SELF = ("CANNOT_DEMOTE_SELF", "Admins cannot change their own role.",         403)
CANNOT_DELETE_SELF = ("CANNOT_DELETE_SELF", "Admins cannot delete their own account here.", 403)

# ── Levels / Placement ───────────────────────────────────────────────────────
LEVEL_NOT_FOUND  = ("LEVEL_NOT_FOUND",  "Level not found.",                                       404)
LEVEL_NOT_ACTIVE = ("LEVEL_NOT_ACTIVE", "Level is not currently active.",                         400)
LEVEL_NOT_SET    = ("LEVEL_NOT_SET",    "No level assigned. Complete placement to continue.",     400)
ALREADY_PLACED   = ("ALREADY_PLACED",   "Placement already completed.",                           409)

# ── Lessons ───────────────────────────────────────────────────────────────────
LESSON_NOT_FOUND    = ("LESSON_NOT_FOUND",    "Lesson not found.",         404)
LESSON_LOCKED       = ("LESSON_LOCKED",       "Lesson is locked.",         403)
LESSON_NOT_APPROVED = ("LESSON_NOT_APPROVED", "Lesson is not published.",  403)
LESSON_NOT_OWNED    = ("LESSON_NOT_OWNED",    "You do not have permission to modify this lesson.", 403)

# ── Questions / Attempts ──────────────────────────────────────────────────────
QUESTION_NOT_FOUND = ("QUESTION_NOT_FOUND", "Question not found.", 404)

# ── Notifications ─────────────────────────────────────────────────────────────
NOTIFICATION_NOT_FOUND  = ("NOTIFICATION_NOT_FOUND",  "Notification not found.",                  404)
NOTIFICATION_NOT_OWNED  = ("NOTIFICATION_NOT_OWNED",  "Notification not found or access denied.", 403)

# ── Admin content authoring ───────────────────────────────────────────────────
SECTION_NOT_FOUND          = ("SECTION_NOT_FOUND",          "Lesson section not found.",                   404)
BLOCK_NOT_FOUND            = ("BLOCK_NOT_FOUND",            "Content block not found.",                    404)
VOCABULARY_WORD_NOT_FOUND  = ("VOCABULARY_WORD_NOT_FOUND",  "Vocabulary word not found.",                  404)
DISPLAY_ORDER_CONFLICT     = ("DISPLAY_ORDER_CONFLICT",     "This display_order is already in use.",       409)
QUESTION_HAS_ATTEMPTS      = ("QUESTION_HAS_ATTEMPTS",      "Cannot delete a question that has attempts.", 409)
SECTION_HAS_ATTEMPTS       = ("SECTION_HAS_ATTEMPTS",       "Cannot delete a section that has questions with attempts.", 409)
VOCABULARY_WORD_HAS_MASTERY = ("VOCABULARY_WORD_HAS_MASTERY", "Cannot delete a word with mastery records.", 409)

# ── Content review ────────────────────────────────────────────────────────────
CONTENT_ALREADY_PENDING  = ("CONTENT_ALREADY_PENDING",  "A review is already pending for this content.", 409)
REASON_REQUIRED          = ("REASON_REQUIRED",           "A reason is required for this decision.",      422)
CONTENT_REVIEW_NOT_FOUND = ("CONTENT_REVIEW_NOT_FOUND",  "Content review not found.",                    404)
