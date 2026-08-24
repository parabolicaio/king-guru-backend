# KingGuru EdTech API

KingGuru is the backend API for a gamified English-learning app (lessons, placement testing, vocabulary, pronunciation/essay grading, daily goals, streaks, achievements, and a content-authoring/admin workflow). All routes are versioned under the `/api/v1` base path except the infrastructure health check.

Authentication is **Supabase-issued JWTs** — this backend does not issue tokens itself, it only validates them (via Supabase's JWKS endpoint for RS256/ES256, or a shared secret for legacy HS256) and resolves the token's `sub` claim to a row in this service's own `user` table.

All error responses use a single envelope shape, regardless of which endpoint failed:

```json
{
  "error": {
    "code": "LESSON_LOCKED",
    "message": "Lesson is locked.",
    "details": {}
  }
}
```

`code` is a stable SCREAMING_SNAKE_CASE identifier clients can branch on (e.g. `UNAUTHORIZED`, `VALIDATION_ERROR`, `RATE_LIMITED`), `message` is a human-readable description, and `details` is an optional object with extra context (for example `RATE_LIMITED` includes `retry_after_seconds`). Unhandled validation errors from FastAPI/Pydantic surface as HTTP 422 with `VALIDATION_ERROR`-style content.

## Authentication

Pass the token as a standard bearer header: `Authorization: Bearer <supabase-jwt>`. Each endpoint below is labeled with one of the following levels:

| Level | Meaning |
|---|---|
| **Public** | No token needed. |
| **Optional** | Token is read if present (`Authorization: Bearer …` and/or `X-Guest-Token`) but the endpoint still works without one — behavior often differs for guests vs. signed-in users. |
| **User** | Any authenticated, non-deleted user (valid JWT that resolves to a `user` row). |
| **Content Manager** | User whose JWT `app_metadata.admin_role` is `content_manager` or `admin`. |
| **Admin** | User whose JWT `app_metadata.admin_role` is exactly `admin`. |

Two auth-flow endpoints (`POST /auth/signup`, `POST /auth/session`) are a special case: they require a **valid Supabase JWT** but run before any `user` row is guaranteed to exist yet — they use a lighter dependency (`get_token_payload`) instead of the standard `get_current_user`, since their entire job is to create/return that row.

Guest flows (unauthenticated trial users) are identified by an `X-Guest-Token` header (a client-generated UUID) instead of a JWT; several endpoints (`attempts`, `placement`) accept either.

---

## Auth

Base path: `/api/v1`

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/auth/check-phone` | Public | Checks whether a phone number is already registered; rate-limited to 20 requests/60s per caller (IP/token) to slow account-enumeration probing. |
| POST | `/api/v1/auth/signup` | User (JWT only) | First-time account creation — collapses create-user + onboarding + optional placement into one call; idempotent/safe to retry if onboarding is already complete. |
| POST | `/api/v1/auth/session` | User (JWT only) | Exchanges a Supabase JWT for the app session; **creates the `user` row on first call**, returns the full profile on every call. |
| POST | `/api/v1/users/guest` | Public | Registers or fetches a guest session by `guest_token`; idempotent (returns the existing row if the token is already known). Returns `GUEST_TOKEN_EXPIRED` (401) if the token is older than 30 days. |

- `GET /auth/check-phone` — query param `phone` (E.164 string). Response: `{ exists: bool }`.
- `POST /auth/signup` — body: `guest_token?`, `full_name`, `age_group`, `role_tag`, `english_level`, `language_preference`, `placement_level_id?`. Returns the full `UserProfile`.
- `POST /auth/session` — body: `{ guest_token?: string }`. If a guest token is supplied, guest progress is intended to be reattributed to the new account.
- `POST /users/guest` — body: `{ guest_token: <uuid> }`. Response: `{ user_id, guest_token, created_at }`.

## Users

Base path: `/api/v1/users`

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/users/me` | User | Returns the caller's own profile. |
| PATCH | `/api/v1/users/me` | User | Updates editable profile fields. |
| DELETE | `/api/v1/users/me` | User | Soft-deletes the caller's own account (204 No Content). |
| POST | `/api/v1/users/me/onboarding` | User | Completes onboarding (name, age group, role, English level, language). |

- `PATCH /users/me` — body: any subset of `display_name`, `avatar_url`, `age_group`, `role_tag`, `english_level`, `language_preference` (each validated against a fixed enum where applicable).
- `POST /users/me/onboarding` — body: `full_name`, `age_group`, `role_tag`, `english_level`, `language_preference` (all required). Response: `{ onboarding_completed_at }`.

## Levels

Base path: `/api/v1/levels`

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/levels` | Public | Lists all active course levels (name, code, icon, topics, guest/payment flags). |

## Lessons

Defined with full paths (no router prefix).

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/levels/{level_id}/lessons` | Optional | Lists lessons in a level with the caller's per-lesson progress; guests only see lessons flagged `is_guest_accessible`. |
| GET | `/api/v1/lessons/{lesson_id}` | Optional | Returns full lesson detail — sections, content blocks, questions (with the caller's latest attempt if any), and vocabulary words (with mastery state). |

- `GET /lessons/{lesson_id}` — 403 `GUEST_ACCESS_DENIED` if a guest requests a non-guest-accessible lesson; 403 `LESSON_LOCKED` for a signed-in user who hasn't unlocked a lesson beyond order 1; 403 `LESSON_NOT_APPROVED` if the lesson isn't in `approved` status.

## Placement

Base path: `/api/v1/placement`

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/placement/fact` | Public | Returns one random educational fact (shown on the results screen). |
| GET | `/api/v1/placement/questions` | Public | Returns the placement-test question set. |
| POST | `/api/v1/placement/submit` | Optional | Scores placement answers and returns a full breakdown (per-question correctness, skill breakdown, recommended level, XP). Works pre-auth via `X-Guest-Token` or post-auth via Bearer JWT; can also atomically persist the chosen level if `confirm_level_id` is passed. |
| POST | `/api/v1/placement/choose-level` | Optional* | Persists the caller's chosen level. Requires at least one of a valid JWT or `X-Guest-Token` — returns 401 `UNAUTHORIZED` if neither is present. |

- `POST /placement/submit` — body: `answers: [{question_id, response}]`, `confirm_level_id?`. Response includes `score_percent`, `recommended_level`/`recommended_level_id`, `xp_awarded`, per-answer detail, and skill-category breakdown.
- `POST /placement/choose-level` — body: `{ level_id }`. Response: `{ current_level_id, placement_completed_at }`.

## Progress

Base path: `/api/v1/users/me`

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/users/me/progress` | User | Overall progress summary — XP, streak, current level, and lesson list with per-lesson status. |
| GET | `/api/v1/users/me/skills` | User | Per-skill-category accuracy/question-count breakdown for the user's current level. Returns 400 `LEVEL_NOT_SET` if no level assigned. |

## Attempts

Defined with full paths (no router prefix).

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/attempts` | Optional | Submits an answer to a question and runs the full scoring/XP/streak/progress/achievement side-effect chain; rate-limited to 60/60s per caller. Requires either a JWT or `X-Guest-Token` (401 `UNAUTHORIZED` otherwise). |
| GET | `/api/v1/users/me/xp-summary` | User | Paginated XP ledger for the caller (cursor-based). |
| GET | `/api/v1/users/me/streak` | User | Current/longest streak plus the next milestone and its bonus XP. |

- `POST /attempts` — body: `{ question_id, response: <dict, shape varies by question type> }`. Optional header `X-Guest-Token` for guest attempts (guest progress is tracked under a synthetic guest user). Pronunciation-type questions expect `response.audio_data_base64` + `response.audio_mime_type` (capped at 5 MB decoded, allow-listed MIME types) — audio is uploaded to Supabase Storage and graded via Gemini. Response includes score, XP awarded, streak result, lesson-completion info, pronunciation detail (if applicable), and any achievements newly unlocked by this attempt.
- `GET /users/me/xp-summary` — query: `limit` (default 20), `cursor`. Response: `{ xp_total, data: [...], cursor, has_more }`.

## Vocabulary

Base path: `/api/v1/vocabulary`

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/vocabulary` | User | Cursor-paginated vocabulary list for the caller, each word annotated with the user's mastery state. |

- Query params: `level_id?`, `mastered?` (bool filter), `cursor?`, `limit` (default 40).

## Notifications

Base path: `/api/v1/notifications`

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/notifications` | User | Cursor-paginated notification list with unread count; `unread_only` query flag filters to unread. |
| PATCH | `/api/v1/notifications/{notification_id}/read` | User | Marks a single notification read (scoped to the caller). |
| POST | `/api/v1/notifications/read-all` | User | Marks all of the caller's notifications read; returns the count updated. |

## Achievements

Base path: `/api/v1/achievements`

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/achievements` | User | Lists all achievements with the caller's unlock state and a total/unlocked count. |

## Leaderboard

Base path: `/api/v1/leaderboard`

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/leaderboard` | User | Top-N users ranked by total XP (all-time), plus the caller's own rank even if outside the top N. `limit` query param, capped at 100. |

## Daily Essay

Base path: `/api/v1/daily-essay`

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/daily-essay/today` | User | Returns today's prompt plus the caller's submission state for today (`null` = not started; draft vs. submitted). |
| PUT | `/api/v1/daily-essay/draft` | User | Creates or overwrites today's draft; idempotent, safe on every autosave tick. Returns 409 if today's essay is already submitted. |
| POST | `/api/v1/daily-essay/submit` | User | Submits today's essay (promotes an existing draft if present); rate-limited to 15/60s. Grading runs asynchronously via a background task calling Gemini — `grade` is `null` in the immediate response. Also fires daily-goal, streak, and achievement side effects. |
| GET | `/api/v1/daily-essay/history` | User | Cursor-paginated history of the caller's past submissions. |
| GET | `/api/v1/daily-essay/{submission_id}` | User | Fetches one submission, scoped to the caller; 404 if not found/not owned. |

- `PUT /draft` — body: `essay_prompt_id`, `draft_text`, `feedback_language` (default `en`).
- `POST /submit` — body: `essay_text`, `essay_prompt_id`, `feedback_language` (default `en`).

## Daily Goal

Base path: `/api/v1/daily-goal`

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/daily-goal/today` | User | Returns today's assigned goal and the caller's progress toward it; lazily generates the day's assignment for the user's level if none exists yet. `goal` is `null` if the user has no level assigned. |

## Content Reviews

Base path: `/api/v1/content-reviews`

Editorial workflow gating lesson/question/block edits from Content Managers before an Admin approves them.

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/content-reviews` | Content Manager | Submits a piece of content (lesson / question_group / question) for review. |
| GET | `/api/v1/content-reviews` | Content Manager | Lists reviews with filters; Content Managers see only their own submissions, Admins see all. |
| GET | `/api/v1/content-reviews/{review_id}` | Content Manager | Fetches one review; 403 if a non-admin requests someone else's review. |
| PATCH | `/api/v1/content-reviews/{review_id}/decide` | Admin | Records an approve/reject/needs-revision decision. |

- `POST /content-reviews` — body: `content_type`, `content_id`. Returns 409 `CONTENT_ALREADY_PENDING` if a review is already pending for that content.
- `GET /content-reviews` — query: `content_type?`, `decision?`, `page` (default 1), `page_size` (default 20).
- `PATCH /{review_id}/decide` — body: `decision` (`approved` | `rejected` | `needs_revision`), `reason?` (required for rejections per service logic).

## Meta

Base path: `/api/v1`

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/feature-flags` | Public | Returns all feature flags as `{ flag_name: bool }`. Public so pre-auth screens can gate on them too. |
| GET | `/api/v1/meta` | Public | Returns `min_mobile_version` / `latest_mobile_version` for the client's app-update gate; must be reachable before sign-in. |

## Admin — Lessons

Base path: `/api/v1/admin/lessons`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/admin/lessons` | Content Manager | Creates a lesson under a level; `lesson_order` is computed automatically (appended). Logs an audit entry. |
| GET | `/api/v1/admin/lessons` | Content Manager | Paginated lesson list, filterable by level/status; Content Managers see only lessons they created, Admins see all. |
| GET | `/api/v1/admin/lessons/{lesson_id}` | Content Manager | Fetches one lesson (admin view — includes unpublished/archived). |
| PATCH | `/api/v1/admin/lessons/{lesson_id}` | Content Manager | Edits a lesson. Non-minor edits to an already-`approved` lesson flip its status back to `pending_review`; `is_minor_edit=true` (admin-only) skips that and only logs an audit entry. |
| DELETE | `/api/v1/admin/lessons/{lesson_id}` | Admin | Soft-deletes a lesson. |
| PATCH | `/api/v1/admin/lessons/{lesson_id}/archive` | Admin | Archives a lesson (sets `archived_at`). |

- `POST /admin/lessons` — body: `level_id`, `title`, `description?`, `is_guest_accessible` (default false), `thumbnail_url?`, `translations?`, `objectives?`, `objectives_translations?`.
- `PATCH /admin/lessons/{id}` — any subset of the create fields, plus `is_minor_edit` (bool, default false).

## Admin — Sections

Full paths (no router prefix), nested under lessons.

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/admin/lessons/{lesson_id}/sections` | Content Manager | Creates a lesson section (category + display order); 409 `DISPLAY_ORDER_CONFLICT` if the order is already used within the lesson. |
| PATCH | `/api/v1/admin/sections/{section_id}` | Content Manager | Updates a section's category/order/title/translations. |
| DELETE | `/api/v1/admin/sections/{section_id}` | Content Manager | Deletes a section; 409 `SECTION_HAS_ATTEMPTS` if any of its questions already have learner attempts. |

- `POST` body: `category` (vocabulary/grammar/pronunciation/reading/listening/writing/speaking), `display_order`, `title?`, `translations?`.

## Admin — Blocks

Full paths (no router prefix), nested under sections.

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/admin/sections/{section_id}/blocks` | Content Manager | Creates a content block (text/image/audio/dialogue/word_card/rich_html/self_check) inside a section; `word_card` blocks queue an async TTS-generation background task. 409 on duplicate `display_order` within the section. |
| PATCH | `/api/v1/admin/blocks/{block_id}` | Content Manager | Updates block type/order/payload/translations (any subset). |
| DELETE | `/api/v1/admin/blocks/{block_id}` | Content Manager | Deletes a content block. |

- `POST` body: `block_type`, `display_order`, `payload?`, `translations?`.

## Admin — Questions

Full paths (no router prefix), nested under sections.

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/admin/sections/{section_id}/questions` | Content Manager | Creates a question in a section. |
| PATCH | `/api/v1/admin/questions/{question_id}` | Content Manager | Updates any subset of question fields. |
| DELETE | `/api/v1/admin/questions/{question_id}` | Content Manager | Deletes a question; 409 `QUESTION_HAS_ATTEMPTS` if learners have already attempted it. |

- `POST` body: `type`, `purpose` (practice/assessment), `display_order`, `prompt_text?`, `prompt_audio_url?`, `prompt_image_url?`, `payload?`, `xp_value` (default 0), `hint_text?`, `vocabulary_word_id?`, `translations?`.

## Admin — Vocabulary

Full paths (no router prefix), nested under sections.

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/admin/sections/{section_id}/vocabulary-words` | Content Manager | Creates a vocabulary word; queues an async TTS-generation task for the English word (and Sinhala translation if provided). |
| PATCH | `/api/v1/admin/vocabulary-words/{word_id}` | Content Manager | Updates any subset of word fields. |
| DELETE | `/api/v1/admin/vocabulary-words/{word_id}` | Content Manager | Deletes a word; 409 `VOCABULARY_WORD_HAS_MASTERY` if learners already have mastery records for it. |

- `POST` body: `word`, `definition`, `example_sentence?`, `pronunciation_guide_si?`, `difficulty` (easy/medium/hard), `image_url?`, `translations?`.

## Admin — Users

Base path: `/api/v1/admin/users`

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/admin/users` | Admin | Paginated, filterable user list (search, auth provider, subscription tier, admin role, level, active-only). |
| GET | `/api/v1/admin/users/{user_id}` | Admin | Full user detail including completed-lesson count and recent XP ledger. |
| PATCH | `/api/v1/admin/users/{user_id}/role` | Admin | Changes a user's `admin_role` (null / content_manager / admin); also pushes the change into the user's Supabase `app_metadata` claim. Admins cannot change their own role (403 `CANNOT_DEMOTE_SELF`). Logs an audit entry. |
| DELETE | `/api/v1/admin/users/{user_id}` | Admin | Soft-deletes another user's account. Admins cannot delete themselves via this endpoint (403 `CANNOT_DELETE_SELF`). Logs an audit entry. |

- `PATCH /{user_id}/role` — body: `{ admin_role: null | "content_manager" | "admin" }`.

## Hooks

Base path: `/api/v1/hooks`

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/hooks/send-sms` | Public (signature-verified) | Supabase's "Send SMS" auth hook — called by Supabase itself (not app clients) to deliver phone-OTP codes via the text.lk SMS provider. Not user-facing; not bearer-token protected. |

- Request is not JWT-authenticated; instead it's verified against the [Standard Webhooks](https://www.standardwebhooks.com/) spec using `webhook-id` / `webhook-timestamp` / `webhook-signature` headers and a shared secret from the Supabase dashboard, with a 5-minute timestamp tolerance. Returns 401 on a bad/missing signature, 400 on a malformed payload, 502 if the SMS provider fails.

## Infra

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/health` | Public | Plain smoke-test endpoint; returns `{"status": "ok"}`. Not under `/api/v1`. |
