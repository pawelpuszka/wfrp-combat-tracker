from pydantic import BaseModel, Field

class TalentEntry(BaseModel):
    name: str
    rank: int = Field(ge=1, default=0)