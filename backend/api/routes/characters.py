from fastapi import APIRouter, Response
from pathlib import Path
from  fastapi import HTTPException
from backend.services.character_service import CharacterService
from backend.schemas.character_card import CharacterCard 

router = APIRouter()

@router.get("/")
def list_characters() -> dict:
    service = CharacterService()
    return {"characters": service.list_characters("players")}


@router.get("/{id}")
def get_full_character_card(id: str, card_type="players") -> CharacterCard:
    file_name: str = str(id) + ".json"
    path_to_file: Path = Path("data/characters") / card_type/ file_name
    service = CharacterService()
    try:
        return service.read_character_from_json(path_to_file=path_to_file)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Postać nie istnieje")


@router.post("/")
def create_character(character_card: CharacterCard, card_type: str="players"):
    service = CharacterService()
    service.upload_character_to_json(data=character_card, card_type=card_type)
    return Response(status_code=201)

    