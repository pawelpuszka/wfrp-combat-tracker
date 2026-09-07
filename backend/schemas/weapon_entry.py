from pydantic import BaseModel, Field

class WeaponEntry(BaseModel):
    name: str
    damage: int = Field(ge=0)