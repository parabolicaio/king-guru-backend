# KingGuru Backend — Changelog

All API changes are documented here per CLAUDE.md workflow rules.
Additive changes (new optional fields) ship freely.
Removals or type changes require Flutter team sign-off before merge.

---

## Unreleased — Slice 0 (Foundation)

### Added
- Repository scaffold: FastAPI app skeleton, asyncpg pool, pydantic-settings config
- `GET /health` smoke-test endpoint
- Full Phase 1 DDL migration (`0001_initial_schema`) — all 32 tables
- Seed data migration (`0002_seed_data`) — levels, XP rules, placement rules, Beginner A Lessons 1–2
