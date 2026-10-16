# otworzyć plik json
# załadować wsadowo plik json do bazy danych

from pathlib import Path
import json
from sqlalchemy import text
from ..connection import engine


def seed_skills():
  path_to_file: Path = Path(__file__).parent / "skills.json"

  with open(path_to_file, 'r', encoding="utf-8") as file:
    skills: list = json.load(file)

  with engine.begin() as conn:
    conn.execute(
      text(
        """
        INSERT INTO skills (name, governing_stat, is_basic, is_grouped, for_combat, source, description)
        VALUES (:name, :governing_stat, :is_basic, :is_grouped, :for_combat, :source, :description)
        ON CONFLICT (name) DO NOTHING
        """
      ), skills
    )



def seed_talents():
  path_to_file: Path = Path(__file__).parent / "talents.json"

  with open(path_to_file, 'r', encoding="utf-8") as file:
    talents: list = json.load(file)

  with engine.begin() as conn:
    conn.execute(
      text(
        """
        INSERT INTO talents (name, description, max_rank, tests, source)
        VALUES (:name, :description, :max_rank, :tests, :source)
        ON CONFLICT (name) DO NOTHING
        """
      ), talents
    )



def seed_item_traits():
  path_to_file: Path = Path(__file__).parent / "item_traits.json"

  with open(path_to_file, 'r', encoding="utf-8") as file:
    item_traits: list = json.load(file)

  with engine.begin() as conn:
    conn.execute(
      text(
        """
        INSERT INTO item_traits (name, description, category_id, is_advantage, has_rating, trait_rating, source)
        VALUES (:name, :description, :category_id, :is_advantage, :has_rating, :trait_rating, :source)
        ON CONFLICT (name) DO NOTHING
        """
      ), item_traits
    )


def seed_items():
  pass


def seed_weapons():
  path_to_file: Path = Path(__file__).parent / "weapons.json"

  with open(path_to_file, 'r', encoding="utf-8") as file:
    weapons: list = json.load(file)

  with engine.begin() as conn:
    conn.execute(
      text(
        """
        INSERT INTO weapons (name, category_id, damage, uses_strength_bonus, reach, range_yards, availability, price_gc, price_ss, price_bp, encumbrance, source)
        VALUES (:name, :category_id, :damage, :uses_strength_bonus, :reach, :range_yards, :availability, :price_gc, :price_ss, :price_bp, :encumbrance, :source)
        ON CONFLICT (name) DO NOTHING
        """
      ), weapons
    )



def seed_weapon_item_traits():
  path_to_file: Path = Path(__file__).parent / "weapon_item_traits.json"

  with open(path_to_file, 'r', encoding="utf-8") as file:
    weapon_item_traits: list = json.load(file)

  with engine.begin() as conn:
    conn.execute(
      text(
        """
        INSERT INTO weapon_item_traits (weapon_id, trait_id)
        VALUES (:weapon_id, :trait_id)
        ON CONFLICT (weapon_id, trait_id) DO NOTHING
        """
      ), weapon_item_traits
    )



def seed_armors():
  path_to_file: Path = Path(__file__).parent / "armors.json"

  with open(path_to_file, 'r', encoding="utf-8") as file:
    armors: list = json.load(file)

  with engine.begin() as conn:
    conn.execute(
      text(
        """
        INSERT INTO armors (name, category_id, penalty, penalty_stat, protected_location, armor_points, availability, price_gc, price_ss, price_bp, encumbrance, source)
        VALUES (:name, :category_id, :penalty, :penalty_stat, :protected_location, :armor_points, :availability, :price_gc, :price_ss, :price_bp, :encumbrance, :source)
        ON CONFLICT (name) DO NOTHING
        """
      ), armors
    )



def seed_armor_item_traits():
  pass


if __name__ == "__main__":
  seed_item_traits()