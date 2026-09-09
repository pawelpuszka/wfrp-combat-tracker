import json
from pathlib import Path
from backend.schemas.character_card import CharacterCard


class CharacterService():

    def read_character_from_json(self, path_to_file: str):
        if not path_to_file.exists():
            raise FileNotFoundError(f"Plik {path_to_file} nie istnieje.")
        with open(path_to_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return CharacterCard.model_validate(data)


    def upload_character_to_json(self, data: CharacterCard, card_type: str="players"):
        file_name: str = str(data.id) + ".json"
        path_to_file = Path("data/characters/") / card_type / file_name
        with open(path_to_file, 'w', encoding="utf-8") as file:
            file.write(data.model_dump_json(indent=4))


    def list_characters(self, card_type: str):
        path: Path = Path("data/characters") / card_type 
        path_to_files = list(path.glob("*.json"))
        characters = []
        for path_to_file in path_to_files:
            with open(path_to_file, 'r', encoding="utf-8") as file: 
                data = json.load(file)
            characters.append({"name": data["name"], "type": data["type"], "id": data["id"]})
        return characters




if __name__ == "__main__":
    service = CharacterService()
    character = service.read_character_from_json("data/characters/players/brunon_witz_test.json")
    # print(character.model_dump_json(indent=4))

    service.upload_character_to_json(character)
    characters = service.list_characters("players")
    print(characters)