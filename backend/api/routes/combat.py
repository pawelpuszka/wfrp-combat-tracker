from fastapi import APIRouter, Response, HTTPException
from uuid import UUID

from backend.services.combat_service import CombatService, CombatantState
from backend.schemas.combatant_state import CombatSession


router = APIRouter()

@router.get("/")
def list_sessions() -> dict:
    service = CombatService()
    return {"sessions": service.list_sessions()}


@router.post("/")
def create_new_session(session_name: str, combatants: list[CombatantState]):
    service = CombatService()
    session_id = service.create_session()
    return Response(status_code=201, content=str(session_id))


@router.get("/{session_id}")
def load_session_from_file(session_id: UUID) -> CombatSession:
    service = CombatService()
    
    try:
        combat_session = service.load_session(session_id=session_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Sesja nie istnieje.")
    
    return combat_session


@router.put("/{session_id}")
def update_session(session_id: UUID, combat_session: CombatSession):
    service = CombatService()

    if str(session_id) != str(combat_session.session_id):
        raise HTTPException(status_code=400, detail="Bad request")

    service.update_session(combat_session=combat_session)


@router.delete("/{id}")
def remove_session(session_id: UUID) -> Response:
    service = CombatService()

    try: 
        service.remove_session(session_id=session_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Sesja nie istnieje")

    return Response(status_code=204)

