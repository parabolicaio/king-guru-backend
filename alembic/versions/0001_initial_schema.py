"""Initial Phase 1 schema — all 32 tables.

Revision ID: e1a2b3c4d5f6
Revises: None
Create Date: 2026-05-28

Tables are created in FK-safe dependency order.
NOTE: vocabulary_word is created BEFORE question because question holds a
nullable FK to vocabulary_word (vocabulary_word_id). The build-plan doc lists
them in the wrong order; this migration uses the correct FK-safe sequence.
"""
from typing import Sequence, Union
from alembic import op

revision: str = "e1a2b3c4d5f6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # -----------------------------------------------------------------------
    # Group 0 — Lookup / seed tables
    # -----------------------------------------------------------------------

    op.execute("""
        CREATE TABLE streak_milestone (
            days     INTEGER PRIMARY KEY,
            bonus_xp INTEGER NOT NULL
        )
    """)

    op.execute("""
        CREATE TABLE xp_rule (
            id             UUID        NOT NULL PRIMARY KEY,
            action_type    TEXT        NOT NULL
                               CHECK (action_type IN (
                                   'lesson_complete',
                                   'word_learned',
                                   'essay_submitted',
                                   'streak_day',
                                   'streak_milestone',
                                   'achievement_unlocked',
                                   'daily_goal_complete'
                               )),
            context_key    TEXT,
            xp_value       INTEGER     NOT NULL DEFAULT 0,
            is_active      BOOLEAN     NOT NULL DEFAULT TRUE,
            effective_from TIMESTAMPTZ NOT NULL DEFAULT now(),
            effective_to   TIMESTAMPTZ,
            notes          TEXT,
            created_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at     TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)
    op.execute("""
        CREATE UNIQUE INDEX xp_rule_unique_no_context
            ON xp_rule (action_type)
            WHERE context_key IS NULL
    """)
    op.execute("""
        CREATE UNIQUE INDEX xp_rule_unique_with_context
            ON xp_rule (action_type, context_key)
            WHERE context_key IS NOT NULL
    """)

    # -----------------------------------------------------------------------
    # Group 1 — Level
    # -----------------------------------------------------------------------

    op.execute("""
        CREATE TABLE level (
            id                  UUID    NOT NULL PRIMARY KEY,
            name                TEXT    NOT NULL,
            code                TEXT    NOT NULL,
            display_order       INTEGER NOT NULL,
            description         TEXT,
            is_active           BOOLEAN NOT NULL DEFAULT TRUE,
            daily_essay_enabled BOOLEAN NOT NULL DEFAULT FALSE,
            created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
            CONSTRAINT level_name_unique          UNIQUE (name),
            CONSTRAINT level_code_unique          UNIQUE (code),
            CONSTRAINT level_display_order_unique UNIQUE (display_order)
        )
    """)

    # -----------------------------------------------------------------------
    # Group 2 — User
    # "user" is a PostgreSQL reserved word — quoted in every SQL statement.
    # -----------------------------------------------------------------------

    op.execute("""
        CREATE TABLE "user" (
            id                        UUID    NOT NULL PRIMARY KEY,
            supabase_uid              UUID    UNIQUE,
            email                     TEXT,
            phone                     TEXT,
            full_name                 TEXT    NOT NULL DEFAULT '',
            display_name              TEXT,
            avatar_url                TEXT,
            age_group                 TEXT    CHECK (age_group IN ('child', 'teen', 'adult')),
            role_tag                  TEXT    NOT NULL DEFAULT '',
            auth_provider             TEXT    CHECK (auth_provider IN ('email', 'google', 'phone')),
            language_preference       TEXT    NOT NULL DEFAULT 'en'
                                          CHECK (language_preference IN ('en', 'si', 'singlish')),
            is_guest                  BOOLEAN NOT NULL DEFAULT FALSE,
            guest_token               TEXT,
            admin_role                TEXT    CHECK (admin_role IN ('content_manager', 'admin')),
            xp_total                  INTEGER NOT NULL DEFAULT 0,
            streak_current            INTEGER NOT NULL DEFAULT 0,
            streak_longest            INTEGER NOT NULL DEFAULT 0,
            streak_last_activity_date DATE,
            onboarding_completed_at   TIMESTAMPTZ,
            placement_completed_at    TIMESTAMPTZ,
            current_level_id          UUID    REFERENCES level(id) ON DELETE SET NULL,
            subscription_tier         TEXT    NOT NULL DEFAULT 'free'
                                          CHECK (subscription_tier IN ('free', 'basic', 'premium')),
            deleted_at                TIMESTAMPTZ,
            created_at                TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at                TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)
    op.execute("""
        CREATE INDEX user_current_level_idx ON "user" (current_level_id)
    """)
    op.execute("""
        CREATE INDEX user_guest_token_idx ON "user" (guest_token)
            WHERE guest_token IS NOT NULL
    """)
    op.execute("""
        CREATE INDEX user_admin_role_idx ON "user" (admin_role)
            WHERE admin_role IS NOT NULL
    """)
    op.execute("""
        CREATE INDEX user_active_idx ON "user" (created_at)
            WHERE deleted_at IS NULL
    """)

    # -----------------------------------------------------------------------
    # Group 3 — Lesson chain
    # Creation order: lesson → lesson_section → content_block
    #                 → question_group → vocabulary_word → question
    # -----------------------------------------------------------------------

    op.execute("""
        CREATE TABLE lesson (
            id                  UUID    NOT NULL PRIMARY KEY,
            level_id            UUID    NOT NULL REFERENCES level(id) ON DELETE RESTRICT,
            title               TEXT    NOT NULL,
            description         TEXT,
            lesson_order        INTEGER NOT NULL,
            status              TEXT    NOT NULL DEFAULT 'draft'
                                    CHECK (status IN (
                                        'draft', 'pending_review', 'approved', 'rejected'
                                    )),
            is_guest_accessible BOOLEAN NOT NULL DEFAULT FALSE,
            thumbnail_url       TEXT,
            translations        JSONB   NOT NULL DEFAULT '{}',
            archived_at         TIMESTAMPTZ,
            deleted_at          TIMESTAMPTZ,
            created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
            CONSTRAINT lesson_order_unique_per_level UNIQUE (level_id, lesson_order)
        )
    """)
    op.execute("""
        CREATE INDEX lesson_level_order_idx ON lesson (level_id, lesson_order)
    """)
    op.execute("""
        CREATE INDEX lesson_active_chain_idx ON lesson (level_id, lesson_order)
            WHERE status = 'approved' AND archived_at IS NULL AND deleted_at IS NULL
    """)

    op.execute("""
        CREATE TABLE lesson_section (
            id            UUID    NOT NULL PRIMARY KEY,
            lesson_id     UUID    NOT NULL REFERENCES lesson(id) ON DELETE CASCADE,
            category      TEXT    NOT NULL
                              CHECK (category IN (
                                  'vocabulary', 'grammar', 'pronunciation',
                                  'reading', 'listening', 'writing', 'speaking'
                              )),
            display_order INTEGER NOT NULL,
            title         TEXT,
            translations  JSONB   NOT NULL DEFAULT '{}',
            created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
            CONSTRAINT section_order_unique_per_lesson UNIQUE (lesson_id, display_order)
        )
    """)
    op.execute("""
        CREATE INDEX lesson_section_lesson_idx ON lesson_section (lesson_id)
    """)

    op.execute("""
        CREATE TABLE content_block (
            id                UUID    NOT NULL PRIMARY KEY,
            lesson_section_id UUID    NOT NULL REFERENCES lesson_section(id) ON DELETE CASCADE,
            block_type        TEXT    NOT NULL
                                  CHECK (block_type IN (
                                      'text', 'image', 'audio', 'dialogue',
                                      'word_card', 'rich_html', 'self_check'
                                  )),
            display_order     INTEGER NOT NULL,
            payload           JSONB   NOT NULL DEFAULT '{}',
            translations      JSONB   NOT NULL DEFAULT '{}',
            created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
            CONSTRAINT block_order_unique_per_section UNIQUE (lesson_section_id, display_order)
        )
    """)
    op.execute("""
        CREATE INDEX content_block_section_idx ON content_block (lesson_section_id)
    """)

    # Phase 2 table — created now because question.question_group_id FKs to it.
    op.execute("""
        CREATE TABLE question_group (
            id                UUID    NOT NULL PRIMARY KEY,
            lesson_section_id UUID    NOT NULL REFERENCES lesson_section(id) ON DELETE CASCADE,
            group_type        TEXT    NOT NULL
                                  CHECK (group_type IN ('reading_passage', 'audio_passage')),
            display_order     INTEGER NOT NULL,
            passage_text      TEXT,
            audio_url         TEXT,
            image_url         TEXT,
            translations      JSONB   NOT NULL DEFAULT '{}',
            created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at        TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)
    op.execute("""
        CREATE INDEX question_group_section_idx ON question_group (lesson_section_id)
    """)

    # vocabulary_word before question — question.vocabulary_word_id FKs to this.
    op.execute("""
        CREATE TABLE vocabulary_word (
            id                     UUID    NOT NULL PRIMARY KEY,
            lesson_section_id      UUID    NOT NULL REFERENCES lesson_section(id) ON DELETE RESTRICT,
            word                   TEXT    NOT NULL,
            definition             TEXT    NOT NULL,
            example_sentence       TEXT,
            pronunciation_guide_si TEXT,
            difficulty             TEXT    NOT NULL
                                       CHECK (difficulty IN ('easy', 'medium', 'hard')),
            image_url              TEXT,
            audio_url              TEXT,
            translations           JSONB   NOT NULL DEFAULT '{}',
            created_at             TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at             TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)
    op.execute("""
        CREATE INDEX vocabulary_word_section_idx ON vocabulary_word (lesson_section_id)
    """)

    op.execute("""
        CREATE TABLE question (
            id                 UUID    NOT NULL PRIMARY KEY,
            lesson_section_id  UUID    NOT NULL REFERENCES lesson_section(id) ON DELETE CASCADE,
            question_group_id  UUID    REFERENCES question_group(id) ON DELETE SET NULL,
            type               TEXT    NOT NULL
                                   CHECK (type IN (
                                       'mcq_single', 'mcq_long_short_form',
                                       'fill_blank_typed', 'fill_blank_options',
                                       'match_pairs', 'true_false',
                                       'order_events', 'sentence_builder',
                                       'correct_mistake',
                                       'audio_mcq', 'audio_image_select',
                                       'audio_fill_blank', 'reading_passage_mcq',
                                       'reading_passage_short_answer',
                                       'pronunciation_practice', 'picture_speak_target',
                                       'free_speak', 'picture_describe'
                                   )),
            purpose            TEXT    NOT NULL
                                   CHECK (purpose IN ('practice', 'assessment')),
            display_order      INTEGER NOT NULL,
            prompt_text        TEXT,
            prompt_audio_url   TEXT,
            prompt_image_url   TEXT,
            payload            JSONB   NOT NULL DEFAULT '{}',
            xp_value           INTEGER NOT NULL DEFAULT 0,
            hint_text          TEXT,
            vocabulary_word_id UUID    REFERENCES vocabulary_word(id) ON DELETE SET NULL,
            translations       JSONB   NOT NULL DEFAULT '{}',
            created_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at         TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)
    op.execute("""
        CREATE INDEX question_section_idx         ON question (lesson_section_id)
    """)
    op.execute("""
        CREATE INDEX question_group_fk_idx        ON question (question_group_id)
            WHERE question_group_id IS NOT NULL
    """)
    op.execute("""
        CREATE INDEX question_section_purpose_idx ON question (lesson_section_id, purpose)
    """)
    op.execute("""
        CREATE INDEX question_vocab_word_idx      ON question (vocabulary_word_id)
            WHERE vocabulary_word_id IS NOT NULL
    """)

    # -----------------------------------------------------------------------
    # Group 4 — Learner activity
    # -----------------------------------------------------------------------

    op.execute("""
        CREATE TABLE attempt (
            id                UUID         NOT NULL PRIMARY KEY,
            user_id           UUID         REFERENCES "user"(id) ON DELETE RESTRICT,
            guest_token       TEXT,
            question_id       UUID         NOT NULL REFERENCES question(id) ON DELETE RESTRICT,
            lesson_section_id UUID         NOT NULL REFERENCES lesson_section(id) ON DELETE RESTRICT,
            lesson_id         UUID         NOT NULL REFERENCES lesson(id) ON DELETE RESTRICT,
            response          JSONB        NOT NULL DEFAULT '{}',
            question_version  INTEGER      NOT NULL DEFAULT 1,
            score_fraction    NUMERIC(3,2) CHECK (score_fraction BETWEEN 0.00 AND 1.00),
            score_numerator   INTEGER,
            score_denominator INTEGER,
            ai_feedback       JSONB,
            xp_awarded        INTEGER      NOT NULL DEFAULT 0,
            duration_ms       INTEGER,
            created_at        TIMESTAMPTZ  NOT NULL DEFAULT now(),

            CONSTRAINT attempt_user_or_guest CHECK (
                (user_id IS NOT NULL AND guest_token IS NULL)
                OR (user_id IS NULL AND guest_token IS NOT NULL)
            )
        )
    """)
    op.execute("""
        CREATE INDEX attempt_user_question_idx ON attempt (user_id, question_id, created_at DESC)
            WHERE user_id IS NOT NULL
    """)
    op.execute("""
        CREATE INDEX attempt_guest_question_idx ON attempt (guest_token, question_id, created_at DESC)
            WHERE guest_token IS NOT NULL
    """)
    op.execute("""
        CREATE INDEX attempt_lesson_section_idx ON attempt (lesson_section_id)
    """)
    op.execute("""
        CREATE INDEX attempt_lesson_idx ON attempt (lesson_id)
    """)
    op.execute("""
        CREATE INDEX attempt_guest_token_idx ON attempt (guest_token)
            WHERE guest_token IS NOT NULL
    """)

    op.execute("""
        CREATE TABLE lesson_progress (
            id             UUID         NOT NULL PRIMARY KEY,
            user_id        UUID         NOT NULL REFERENCES "user"(id) ON DELETE RESTRICT,
            lesson_id      UUID         NOT NULL REFERENCES lesson(id) ON DELETE RESTRICT,
            status         TEXT         NOT NULL DEFAULT 'not_started'
                               CHECK (status IN ('not_started', 'in_progress', 'completed')),
            completion_pct NUMERIC(5,2) NOT NULL DEFAULT 0.00
                               CHECK (completion_pct BETWEEN 0.00 AND 100.00),
            started_at     TIMESTAMPTZ,
            completed_at   TIMESTAMPTZ,
            created_at     TIMESTAMPTZ  NOT NULL DEFAULT now(),
            updated_at     TIMESTAMPTZ  NOT NULL DEFAULT now(),
            CONSTRAINT lesson_progress_unique UNIQUE (user_id, lesson_id)
        )
    """)
    op.execute("""
        CREATE INDEX lesson_progress_user_idx   ON lesson_progress (user_id)
    """)
    op.execute("""
        CREATE INDEX lesson_progress_lesson_idx ON lesson_progress (lesson_id)
    """)

    op.execute("""
        CREATE TABLE vocabulary_mastery (
            id                    UUID    NOT NULL PRIMARY KEY,
            user_id               UUID    NOT NULL REFERENCES "user"(id) ON DELETE RESTRICT,
            vocabulary_word_id    UUID    NOT NULL REFERENCES vocabulary_word(id) ON DELETE RESTRICT,
            attempt_count         INTEGER NOT NULL DEFAULT 0,
            correct_attempt_count INTEGER NOT NULL DEFAULT 0,
            is_mastered           BOOLEAN NOT NULL DEFAULT FALSE,
            last_seen_at          TIMESTAMPTZ,
            created_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
            CONSTRAINT vocab_mastery_unique UNIQUE (user_id, vocabulary_word_id)
        )
    """)
    op.execute("""
        CREATE INDEX vocab_mastery_user_idx ON vocabulary_mastery (user_id)
    """)
    op.execute("""
        CREATE INDEX vocab_mastery_word_idx ON vocabulary_mastery (vocabulary_word_id)
    """)

    op.execute("""
        CREATE TABLE xp_ledger (
            id             UUID    NOT NULL PRIMARY KEY,
            user_id        UUID    NOT NULL REFERENCES "user"(id) ON DELETE RESTRICT,
            action_type    TEXT    NOT NULL
                               CHECK (action_type IN (
                                   'lesson_complete', 'word_learned', 'essay_submitted',
                                   'streak_day', 'streak_milestone', 'achievement_unlocked',
                                   'daily_goal_complete', 'question_attempt'
                               )),
            xp_delta       INTEGER NOT NULL,
            reference_id   UUID,
            reference_type TEXT    CHECK (reference_type IN (
                               'attempt', 'essay', 'achievement', 'daily_goal',
                               'lesson', 'vocabulary_word'
                           )),
            awarded_at     TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)
    op.execute("""
        CREATE INDEX xp_ledger_user_idx      ON xp_ledger (user_id)
    """)
    op.execute("""
        CREATE INDEX xp_ledger_user_time_idx ON xp_ledger (user_id, awarded_at DESC)
    """)

    # -----------------------------------------------------------------------
    # Group 5 — Placement
    # -----------------------------------------------------------------------

    op.execute("""
        CREATE TABLE placement_question (
            id            UUID    NOT NULL PRIMARY KEY,
            type          TEXT    NOT NULL
                              CHECK (type IN (
                                  'mcq_single', 'mcq_long_short_form',
                                  'fill_blank_typed', 'fill_blank_options',
                                  'match_pairs', 'true_false',
                                  'order_events', 'sentence_builder', 'correct_mistake'
                              )),
            payload       JSONB   NOT NULL DEFAULT '{}',
            difficulty    TEXT    NOT NULL
                              CHECK (difficulty IN (
                                  'beginner_a', 'beginner_b', 'elementary',
                                  'intermediate', 'upper_intermediate', 'advanced'
                              )),
            display_order INTEGER NOT NULL UNIQUE,
            translations  JSONB   NOT NULL DEFAULT '{}',
            created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)

    op.execute("""
        CREATE TABLE placement_scoring_rule (
            id                   UUID         NOT NULL PRIMARY KEY,
            min_percent          NUMERIC(5,2) NOT NULL,
            max_percent          NUMERIC(5,2) NOT NULL,
            recommended_level_id UUID         NOT NULL REFERENCES level(id) ON DELETE RESTRICT,
            created_at           TIMESTAMPTZ  NOT NULL DEFAULT now(),
            updated_at           TIMESTAMPTZ  NOT NULL DEFAULT now(),
            CONSTRAINT placement_rule_range_valid  CHECK (min_percent <= max_percent),
            CONSTRAINT placement_rule_level_unique UNIQUE (recommended_level_id)
        )
    """)
    op.execute("""
        CREATE INDEX placement_rule_range_idx ON placement_scoring_rule (min_percent, max_percent)
    """)

    # -----------------------------------------------------------------------
    # Group 6 — Content management
    # -----------------------------------------------------------------------

    op.execute("""
        CREATE TABLE content_review (
            id            UUID    NOT NULL PRIMARY KEY,
            content_type  TEXT    NOT NULL
                              CHECK (content_type IN ('lesson', 'question_group', 'question')),
            content_id    UUID    NOT NULL,
            submitted_by  UUID    NOT NULL REFERENCES "user"(id) ON DELETE RESTRICT,
            submitted_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
            reviewer_id   UUID    REFERENCES "user"(id) ON DELETE RESTRICT,
            decision      TEXT    NOT NULL DEFAULT 'pending'
                              CHECK (decision IN ('pending', 'approved', 'rejected', 'needs_revision')),
            reason        TEXT,
            reviewed_at   TIMESTAMPTZ,
            created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
            CONSTRAINT content_review_reason_required CHECK (
                decision NOT IN ('rejected', 'needs_revision') OR reason IS NOT NULL
            )
        )
    """)
    op.execute("""
        CREATE INDEX content_review_content_idx   ON content_review (content_type, content_id)
    """)
    op.execute("""
        CREATE INDEX content_review_submitter_idx ON content_review (submitted_by)
    """)
    op.execute("""
        CREATE INDEX content_review_reviewer_idx  ON content_review (reviewer_id)
            WHERE reviewer_id IS NOT NULL
    """)
    op.execute("""
        CREATE INDEX content_review_pending_idx   ON content_review (submitted_at DESC)
            WHERE decision = 'pending'
    """)

    op.execute("""
        CREATE TABLE feature_flag (
            id                UUID        NOT NULL PRIMARY KEY,
            flag_key          TEXT        NOT NULL UNIQUE,
            description       TEXT        NOT NULL,
            default_value     BOOLEAN     NOT NULL DEFAULT FALSE,
            enabled_for_tiers TEXT[]      NOT NULL DEFAULT '{}',
            created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at        TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)

    op.execute("""
        CREATE TABLE user_feature_flag_override (
            id         UUID    NOT NULL PRIMARY KEY,
            user_id    UUID    NOT NULL REFERENCES "user"(id) ON DELETE RESTRICT,
            flag_key   TEXT    NOT NULL REFERENCES feature_flag(flag_key) ON DELETE CASCADE,
            value      BOOLEAN NOT NULL,
            reason     TEXT,
            set_by     UUID    NOT NULL REFERENCES "user"(id) ON DELETE RESTRICT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            CONSTRAINT flag_override_unique UNIQUE (user_id, flag_key)
        )
    """)
    op.execute("""
        CREATE INDEX flag_override_user_idx ON user_feature_flag_override (user_id)
    """)

    # -----------------------------------------------------------------------
    # Group 7 — Notifications and audit
    # -----------------------------------------------------------------------

    op.execute("""
        CREATE TABLE notification (
            id             UUID    NOT NULL PRIMARY KEY,
            user_id        UUID    NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
            type           TEXT    NOT NULL
                               CHECK (type IN (
                                   'achievement_unlocked', 'streak_at_risk',
                                   'lesson_unlocked', 'lesson_complete',
                                   'announcement', 'content_review_decision'
                               )),
            title          TEXT    NOT NULL,
            body           TEXT    NOT NULL,
            is_read        BOOLEAN NOT NULL DEFAULT FALSE,
            read_at        TIMESTAMPTZ,
            reference_id   UUID,
            reference_type TEXT,
            translations   JSONB   NOT NULL DEFAULT '{}',
            created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)
    op.execute("""
        CREATE INDEX notification_user_idx   ON notification (user_id, created_at DESC)
    """)
    op.execute("""
        CREATE INDEX notification_unread_idx ON notification (user_id)
            WHERE is_read = FALSE
    """)

    op.execute("""
        CREATE TABLE audit_log (
            id           UUID    NOT NULL PRIMARY KEY,
            actor_id     UUID    REFERENCES "user"(id) ON DELETE RESTRICT,
            action       TEXT    NOT NULL,
            target_type  TEXT    NOT NULL,
            target_id    UUID    NOT NULL,
            before_state JSONB,
            after_state  JSONB,
            ip_address   TEXT,
            created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)
    op.execute("""
        CREATE INDEX audit_log_actor_idx  ON audit_log (actor_id)
            WHERE actor_id IS NOT NULL
    """)
    op.execute("""
        CREATE INDEX audit_log_target_idx ON audit_log (target_type, target_id)
    """)
    op.execute("""
        CREATE INDEX audit_log_time_idx   ON audit_log (created_at DESC)
    """)

    # -----------------------------------------------------------------------
    # Phase 2 stubs — full column definitions now to avoid schema churn later
    # -----------------------------------------------------------------------

    op.execute("""
        CREATE TABLE essay_prompt (
            id            UUID    NOT NULL PRIMARY KEY,
            prompt_text   TEXT    NOT NULL,
            level_id      UUID    REFERENCES level(id) ON DELETE RESTRICT,
            is_active     BOOLEAN NOT NULL DEFAULT TRUE,
            date_assigned DATE,
            translations  JSONB   NOT NULL DEFAULT '{}',
            created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)
    op.execute("""
        CREATE INDEX essay_prompt_level_idx  ON essay_prompt (level_id)
            WHERE level_id IS NOT NULL
    """)
    op.execute("""
        CREATE INDEX essay_prompt_active_idx ON essay_prompt (date_assigned)
            WHERE is_active = TRUE
    """)

    op.execute("""
        CREATE TABLE daily_essay_submission (
            id                UUID         NOT NULL PRIMARY KEY,
            user_id           UUID         NOT NULL REFERENCES "user"(id) ON DELETE RESTRICT,
            essay_prompt_id   UUID         NOT NULL REFERENCES essay_prompt(id) ON DELETE RESTRICT,
            prompt_text       TEXT         NOT NULL,
            essay_text        TEXT         NOT NULL,
            submitted_at      TIMESTAMPTZ  NOT NULL DEFAULT now(),
            submission_date   DATE         NOT NULL,
            grade             TEXT         CHECK (grade IN ('A+', 'A', 'B+', 'B', 'C+', 'C', 'D', 'F')),
            score_grammar     NUMERIC(5,2),
            score_vocabulary  NUMERIC(5,2),
            score_content     NUMERIC(5,2),
            score_suggestions NUMERIC(5,2),
            ai_feedback       JSONB,
            ai_model          TEXT,
            xp_awarded        INTEGER      NOT NULL DEFAULT 0,
            created_at        TIMESTAMPTZ  NOT NULL DEFAULT now(),
            updated_at        TIMESTAMPTZ  NOT NULL DEFAULT now()
        )
    """)
    op.execute("""
        CREATE INDEX essay_submission_user_date_idx
            ON daily_essay_submission (user_id, submission_date DESC)
    """)

    op.execute("""
        CREATE TABLE achievement (
            id                UUID    NOT NULL PRIMARY KEY,
            name              TEXT    NOT NULL UNIQUE,
            description       TEXT    NOT NULL,
            icon_url          TEXT,
            condition_type    TEXT    NOT NULL
                                  CHECK (condition_type IN (
                                      'lesson_count', 'streak_days', 'xp_total',
                                      'words_mastered', 'essay_count', 'custom'
                                  )),
            condition_value   INTEGER NOT NULL,
            condition_payload JSONB,
            xp_reward         INTEGER NOT NULL DEFAULT 0,
            is_active         BOOLEAN NOT NULL DEFAULT TRUE,
            translations      JSONB   NOT NULL DEFAULT '{}',
            created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at        TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)

    op.execute("""
        CREATE TABLE user_achievement (
            id             UUID    NOT NULL PRIMARY KEY,
            user_id        UUID    NOT NULL REFERENCES "user"(id) ON DELETE RESTRICT,
            achievement_id UUID    NOT NULL REFERENCES achievement(id) ON DELETE RESTRICT,
            unlocked_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
            CONSTRAINT user_achievement_unique UNIQUE (user_id, achievement_id)
        )
    """)
    op.execute("""
        CREATE INDEX user_achievement_user_idx ON user_achievement (user_id)
    """)

    op.execute("""
        CREATE TABLE daily_goal (
            id           UUID    NOT NULL PRIMARY KEY,
            title        TEXT    NOT NULL,
            description  TEXT,
            goal_type    TEXT    NOT NULL
                             CHECK (goal_type IN (
                                 'questions_answered', 'lessons_completed', 'xp_earned',
                                 'words_learned', 'essay_submitted'
                             )),
            target_value INTEGER NOT NULL,
            xp_reward    INTEGER NOT NULL DEFAULT 0,
            is_active    BOOLEAN NOT NULL DEFAULT TRUE,
            translations JSONB   NOT NULL DEFAULT '{}',
            created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at   TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)

    op.execute("""
        CREATE TABLE daily_goal_progress (
            id            UUID    NOT NULL PRIMARY KEY,
            user_id       UUID    NOT NULL REFERENCES "user"(id) ON DELETE RESTRICT,
            daily_goal_id UUID    NOT NULL REFERENCES daily_goal(id) ON DELETE RESTRICT,
            goal_date     DATE    NOT NULL,
            current_value INTEGER NOT NULL DEFAULT 0,
            is_completed  BOOLEAN NOT NULL DEFAULT FALSE,
            completed_at  TIMESTAMPTZ,
            xp_awarded    INTEGER NOT NULL DEFAULT 0,
            created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
            CONSTRAINT daily_goal_progress_unique UNIQUE (user_id, daily_goal_id, goal_date)
        )
    """)
    op.execute("""
        CREATE INDEX daily_goal_progress_user_idx
            ON daily_goal_progress (user_id, goal_date DESC)
    """)

    op.execute("""
        CREATE TABLE ai_tutor_conversation (
            id            UUID    NOT NULL PRIMARY KEY,
            user_id       UUID    NOT NULL REFERENCES "user"(id) ON DELETE RESTRICT,
            started_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
            ended_at      TIMESTAMPTZ,
            message_count INTEGER NOT NULL DEFAULT 0,
            created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)
    op.execute("""
        CREATE INDEX ai_tutor_conv_user_idx ON ai_tutor_conversation (user_id)
    """)

    op.execute("""
        CREATE TABLE ai_tutor_message (
            id                UUID    NOT NULL PRIMARY KEY,
            conversation_id   UUID    NOT NULL
                                  REFERENCES ai_tutor_conversation(id) ON DELETE CASCADE,
            role              TEXT    NOT NULL CHECK (role IN ('user', 'assistant')),
            content_text      TEXT    NOT NULL,
            content_audio_url TEXT,
            ai_model          TEXT,
            token_count       INTEGER,
            created_at        TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)
    op.execute("""
        CREATE INDEX ai_tutor_msg_conv_idx
            ON ai_tutor_message (conversation_id, created_at ASC)
    """)

    op.execute("""
        CREATE TABLE ai_usage_log (
            id            UUID         NOT NULL PRIMARY KEY,
            user_id       UUID         NOT NULL REFERENCES "user"(id) ON DELETE RESTRICT,
            feature       TEXT         NOT NULL
                              CHECK (feature IN (
                                  'essay_grading', 'tutor_chat', 'pronunciation_assessment'
                              )),
            ai_model      TEXT         NOT NULL,
            input_tokens  INTEGER,
            output_tokens INTEGER,
            cost_usd      NUMERIC(10,6),
            created_at    TIMESTAMPTZ  NOT NULL DEFAULT now()
        )
    """)
    op.execute("""
        CREATE INDEX ai_usage_user_idx ON ai_usage_log (user_id, created_at DESC)
    """)

    # -----------------------------------------------------------------------
    # Phase 3 stubs
    # -----------------------------------------------------------------------

    op.execute("""
        CREATE TABLE subscription (
            id                      UUID    NOT NULL PRIMARY KEY,
            user_id                 UUID    NOT NULL REFERENCES "user"(id) ON DELETE RESTRICT,
            tier                    TEXT    NOT NULL CHECK (tier IN ('free', 'basic', 'premium')),
            status                  TEXT    NOT NULL
                                        CHECK (status IN (
                                            'active', 'cancelled', 'expired', 'past_due'
                                        )),
            payhere_order_id        TEXT,
            payhere_subscription_id TEXT,
            current_period_start    TIMESTAMPTZ NOT NULL,
            current_period_end      TIMESTAMPTZ NOT NULL,
            cancelled_at            TIMESTAMPTZ,
            created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at              TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)
    op.execute("""
        CREATE INDEX subscription_user_idx ON subscription (user_id)
    """)

    op.execute("""
        CREATE TABLE certificate (
            id             UUID    NOT NULL PRIMARY KEY,
            user_id        UUID    NOT NULL REFERENCES "user"(id) ON DELETE RESTRICT,
            level_id       UUID    NOT NULL REFERENCES level(id) ON DELETE RESTRICT,
            serial_number  TEXT    NOT NULL UNIQUE,
            grade          TEXT    NOT NULL
                               CHECK (grade IN ('A+', 'A', 'B+', 'B', 'C+', 'C', 'D', 'F')),
            issued_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
            revoked_at     TIMESTAMPTZ,
            hmac_signature TEXT    NOT NULL,
            pdf_url        TEXT,
            created_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at     TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)
    op.execute("""
        CREATE INDEX certificate_user_idx ON certificate (user_id)
    """)


def downgrade() -> None:
    # Drop in reverse FK-dependency order so no RESTRICT constraint fires.
    # Tables referencing "user" via RESTRICT must be dropped before "user".
    # CASCADE row-level behaviour does not affect DROP TABLE ordering —
    # PostgreSQL still requires FK-referencing tables to be dropped first.
    op.execute('DROP TABLE IF EXISTS certificate')
    op.execute('DROP TABLE IF EXISTS subscription')
    op.execute('DROP TABLE IF EXISTS ai_usage_log')
    op.execute('DROP TABLE IF EXISTS ai_tutor_message')
    op.execute('DROP TABLE IF EXISTS ai_tutor_conversation')
    op.execute('DROP TABLE IF EXISTS daily_goal_progress')
    op.execute('DROP TABLE IF EXISTS daily_goal')
    op.execute('DROP TABLE IF EXISTS user_achievement')
    op.execute('DROP TABLE IF EXISTS achievement')
    op.execute('DROP TABLE IF EXISTS daily_essay_submission')
    op.execute('DROP TABLE IF EXISTS essay_prompt')
    op.execute('DROP TABLE IF EXISTS audit_log')
    op.execute('DROP TABLE IF EXISTS notification')
    op.execute('DROP TABLE IF EXISTS user_feature_flag_override')
    op.execute('DROP TABLE IF EXISTS feature_flag')
    op.execute('DROP TABLE IF EXISTS content_review')
    op.execute('DROP TABLE IF EXISTS placement_scoring_rule')
    op.execute('DROP TABLE IF EXISTS placement_question')
    op.execute('DROP TABLE IF EXISTS xp_ledger')
    op.execute('DROP TABLE IF EXISTS vocabulary_mastery')
    op.execute('DROP TABLE IF EXISTS lesson_progress')
    op.execute('DROP TABLE IF EXISTS attempt')
    op.execute('DROP TABLE IF EXISTS question')
    op.execute('DROP TABLE IF EXISTS vocabulary_word')
    op.execute('DROP TABLE IF EXISTS question_group')
    op.execute('DROP TABLE IF EXISTS content_block')
    op.execute('DROP TABLE IF EXISTS lesson_section')
    op.execute('DROP TABLE IF EXISTS lesson')
    op.execute('DROP TABLE IF EXISTS "user"')
    op.execute('DROP TABLE IF EXISTS level')
    op.execute('DROP TABLE IF EXISTS xp_rule')
    op.execute('DROP TABLE IF EXISTS streak_milestone')
