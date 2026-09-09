from fastapi import APIRouter
from backend.services.character_service import CharacterService

router = APIRouter()

@router.get("/")
def list_characters():
    service = CharacterService()
    return {"characters": service.list_characters("players")}