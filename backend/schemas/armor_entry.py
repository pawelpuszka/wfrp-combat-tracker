from pydantic import BaseModel, Field

class ArmorEntry(BaseModel):
    name: str
    armor_points: int = Field(ge=1)
    penalty: int = Field(ge=0, default=0)
    penalty_stat: str = Field(default=None)