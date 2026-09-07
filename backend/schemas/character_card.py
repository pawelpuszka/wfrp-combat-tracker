from pydantic import BaseModel, Field
from backend.schemas.character_stats import CharacterStats
from backend.schemas.skill_entry import SkillEntry
from backend.schemas.talent_entry import TalentEntry
from backend.schemas.weapon_entry import WeaponEntry
from backend.schemas.armor_entry import ArmorEntry

from uuid import uuid4, UUID
from typing import Optional

class CharacterCard(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    type: str = Field(pattern="^(player|enemy|template)$")
    character_stats: CharacterStats
    skills: list[SkillEntry]
    talents: list[TalentEntry]
    weapons: list[WeaponEntry]
    armor: list[ArmorEntry]
    notes: Optional[str] = None



# if __name__ == "__main__":
#     brunon_witz = CharacterCard(
#         name="Brunon Witz",
#         type="player",
#         character_stats=CharacterStats(
#             WS=32, BS=44, S=31, T=28, I=43, Ag=44, Dex=29, Int=58, WP=49, Fel=36, fate=4, fortune=4, resilience=2, determination=2
#         ),
#         skills=[],
#         talents=[],
#         weapons=[],
#         armor=[],
#         notes=None
#     )

#     print(brunon_witz.model_dump())