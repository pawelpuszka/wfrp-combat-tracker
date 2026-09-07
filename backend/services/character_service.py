import json
from pathlib import Path
from backend.schemas.character_card import CharacterCard


class CharacterService():

    def load_character(self, path_to_file: str):
        with open(path_to_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return CharacterCard.model_validate(data)


    def upload_character(self, data: CharacterCard, card_type: str="players"):
        file_name: str = data.name + ".json"
        path_to_file = Path("data/characters/") / card_type / file_name
        with open(path_to_file, 'w', encoding="utf-8") as file:
            file.write(data.model_dump_json(indent=4))


if __name__ == "__main__":
    service = CharacterService()
    character = service.load_character("data/characters/players/brunon_witz_test.json")
    # print(character.model_dump_json(indent=4))

    service.upload_character(character)