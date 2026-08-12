-- =============================================================================
-- cleanup_lesson_content.sql
--
-- Removes all seeded lesson content and every trace of learner progress
-- tied to those lessons. Run against the Supabase Postgres instance via
-- the SQL editor or psql.
--
-- IMPORTANT: Run the steps in order. FK RESTRICT constraints will cause
-- errors if the order is changed.
--
-- Scoped to lesson_order = 1 only. To wipe ALL lessons instead, remove the
-- WHERE lesson_order = 1 clauses below.
-- =============================================================================


-- ---------------------------------------------------------------------------
-- STEP 0: Verify current state (read-only, safe to run at any time)
-- ---------------------------------------------------------------------------

SELECT id, lesson_order, title, status
FROM lesson
WHERE lesson_order = 1
ORDER BY lesson_order;

SELECT
  (SELECT COUNT(*) FROM attempt a
     JOIN lesson l ON l.id = a.lesson_id)  AS attempts,
  (SELECT COUNT(*) FROM lesson_progress)    AS lesson_progress_rows,
  (SELECT COUNT(*) FROM vocabulary_mastery) AS vocab_mastery_rows,
  (SELECT COUNT(*) FROM xp_ledger)          AS xp_ledger_rows;


-- ---------------------------------------------------------------------------
-- STEP 1: Delete vocabulary mastery
-- vocabulary_mastery.vocabulary_word_id → vocabulary_word(id) RESTRICT
-- ---------------------------------------------------------------------------

DELETE FROM vocabulary_mastery
WHERE vocabulary_word_id IN (
    SELECT vw.id
    FROM   vocabulary_word vw
    JOIN   lesson_section ls ON ls.id = vw.lesson_section_id
    JOIN   lesson         l  ON l.id  = ls.lesson_id
    WHERE  l.lesson_order = 1
);


-- ---------------------------------------------------------------------------
-- STEP 2: Delete XP ledger entries linked to these lessons
-- Cleans up XP awarded for question attempts and lesson completions.
-- ---------------------------------------------------------------------------

-- XP from question attempts
DELETE FROM xp_ledger
WHERE reference_type = 'attempt'
  AND reference_id IN (
      SELECT a.id FROM attempt a
      WHERE  a.lesson_id IN (SELECT id FROM lesson WHERE lesson_order = 1)
  );

-- XP from lesson completion events
DELETE FROM xp_ledger
WHERE reference_type = 'lesson'
  AND reference_id IN (SELECT id FROM lesson WHERE lesson_order = 1);


-- ---------------------------------------------------------------------------
-- STEP 3: Delete attempts
-- attempt.lesson_id / lesson_section_id / question_id are all RESTRICT
-- ---------------------------------------------------------------------------

DELETE FROM attempt
WHERE lesson_id IN (SELECT id FROM lesson WHERE lesson_order = 1);


-- ---------------------------------------------------------------------------
-- STEP 4: Delete lesson progress rows
-- lesson_progress.lesson_id → lesson(id) RESTRICT
-- ---------------------------------------------------------------------------

DELETE FROM lesson_progress
WHERE lesson_id IN (SELECT id FROM lesson WHERE lesson_order = 1);


-- ---------------------------------------------------------------------------
-- STEP 5: Delete content_review entries
-- content_review references lesson/question IDs as plain UUIDs (no FK),
-- but clean them up so there are no orphaned review records.
-- ---------------------------------------------------------------------------

DELETE FROM content_review
WHERE (content_type = 'lesson'
       AND content_id IN (SELECT id FROM lesson WHERE lesson_order = 1))
   OR (content_type = 'question'
       AND content_id IN (
           SELECT q.id
           FROM   question q
           JOIN   lesson_section ls ON ls.id = q.lesson_section_id
           JOIN   lesson         l  ON l.id  = ls.lesson_id
           WHERE  l.lesson_order = 1
       ));


-- ---------------------------------------------------------------------------
-- STEP 6: Delete vocabulary words
-- vocabulary_word.lesson_section_id → lesson_section(id) RESTRICT
-- This is what prevents a direct DELETE FROM lesson from cascading cleanly.
-- ---------------------------------------------------------------------------

DELETE FROM vocabulary_word
WHERE lesson_section_id IN (
    SELECT ls.id
    FROM   lesson_section ls
    JOIN   lesson         l ON l.id = ls.lesson_id
    WHERE  l.lesson_order = 1
);


-- ---------------------------------------------------------------------------
-- STEP 7: Delete lessons
-- lesson_section → content_block, question, question_group all CASCADE,
-- so deleting the lesson row removes all child content automatically.
-- ---------------------------------------------------------------------------

DELETE FROM lesson WHERE lesson_order = 1;


-- ---------------------------------------------------------------------------
-- STEP 8: Recalculate user XP totals
-- xp_total on the user table is denormalized. Recompute from the ledger.
-- ---------------------------------------------------------------------------

UPDATE "user"
SET    xp_total   = COALESCE(
           (SELECT SUM(xp_delta) FROM xp_ledger WHERE xp_ledger.user_id = "user".id),
           0
       ),
       updated_at = now();


-- ---------------------------------------------------------------------------
-- STEP 9 (optional): Reset streak data
-- Run this if you want user streak counters wiped as well.
-- ---------------------------------------------------------------------------

-- UPDATE "user"
-- SET  streak_current           = 0,
--      streak_longest            = 0,
--      streak_last_activity_date = NULL,
--      updated_at                = now();


-- ---------------------------------------------------------------------------
-- STEP 10 (optional): Clear daily goal progress
-- Removes stale progress counts now that the underlying attempts are gone.
-- ---------------------------------------------------------------------------

-- DELETE FROM daily_goal_progress;


-- ---------------------------------------------------------------------------
-- VERIFICATION: Run after all steps to confirm clean state
-- All counts should be 0 (xp_ledger may still have streak/essay entries).
-- ---------------------------------------------------------------------------

SELECT
  (SELECT COUNT(*) FROM lesson)             AS lessons,
  (SELECT COUNT(*) FROM lesson_section)     AS sections,
  (SELECT COUNT(*) FROM content_block)      AS blocks,
  (SELECT COUNT(*) FROM question)           AS questions,
  (SELECT COUNT(*) FROM vocabulary_word)    AS vocab_words,
  (SELECT COUNT(*) FROM attempt)            AS attempts,
  (SELECT COUNT(*) FROM lesson_progress)    AS progress_rows,
  (SELECT COUNT(*) FROM vocabulary_mastery) AS mastery_rows,
  (SELECT COUNT(*) FROM xp_ledger)          AS xp_rows;
