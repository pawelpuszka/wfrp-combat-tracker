from pydantic import BaseModel, Field
from uuid import uuid4, UUID
from datetime import datetime, timezone

from backend.schemas.character_stats import CharacterStats
from backend.schemas.weapon_entry import WeaponEntry
from backend.schemas.armor_entry import ArmorEntry
from backend.schemas.skill_entry import SkillEntry
from backend.schemas.talent_entry import TalentEntry
from backend.schemas.condition_entry import ConditionEntry

class CombatantState(BaseModel):
    character_id: UUID
    name: str
    type: str = Field(pattern="^(player|enemy|template)$")
    stats: CharacterStats
    weapons: list[WeaponEntry]
    armors: list[ArmorEntry]
    skills: list[SkillEntry]
    talents: list[TalentEntry]
    current_wounds: int
    momentum: bool
    initiative: int
    conditions: list[ConditionEntry]
    is_active: bool


class GroupAdvantage(BaseModel):
    players_advantage: int = Field(ge=0, default=0)
    enemies_advantage: int = Field(ge=0, default=0)


class CombatSession(BaseModel):
    session_id: UUID = Field(default_factory=uuid4)
    name: str
    round: int = Field(ge=1, default=1)
    group_advantage: GroupAdvantage = Field(default_factory=GroupAdvantage)
    combatants: list[CombatantState]
    initiative_order: list[UUID]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
