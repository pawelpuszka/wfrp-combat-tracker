from pydantic import BaseModel, Field

class ConditionEntry(BaseModel):
    name: str
    rank: int = Field(ge=1, default=1)