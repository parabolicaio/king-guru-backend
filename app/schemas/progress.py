from pydantic import BaseModel


class SkillProgress(BaseModel):
    category: str
    total_questions: int
    is_available: bool
    questions_answered: int
    accuracy: float | None


class SkillsProgressResponse(BaseModel):
    skills: list[SkillProgress]
