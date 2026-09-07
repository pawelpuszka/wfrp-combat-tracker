from pydantic import BaseModel, Field

class SkillEntry(BaseModel):
    name: str
    advances: int = Field(ge=0, default=0)