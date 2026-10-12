import json
from pathlib import Path
from uuid import uuid4, UUID
from pydantic import Field

from backend.schemas.combatant_state import CombatSession, CombatantState

def generate_file_name_by(session_id: UUID):
    file_name: str = str(session_id) + ".json"
    path_to_file: Path = Path("data/sessions/") / file_name
    return path_to_file

class CombatService():

    def create_session(self, session_name: str, combatants: list[CombatantState]) -> UUID:
        combat_session = CombatSession(
            combatants = combatants,
            name = session_name
        )

        session_id: UUID = combat_session.session_id
        path_to_file: Path = generate_file_name_by(session_id=session_id)

        with open(path_to_file, 'w', encoding="utf-8") as file:
            file.write(combat_session.model_dump_json(indent=4))

        return session_id


    def load_session(self, session_id: UUID) -> CombatSession:
        path_to_file: Path = generate_file_name_by(session_id=session_id)
        
        if not path_to_file.exists():
            raise FileNotFoundError(f"Plik {path_to_file} nie istnieje.")
        
        with open(path_to_file, 'r', encoding="utf-8") as file:
            combat_session: CombatSession = json.load(file)

        return CombatSession.model_validate(combat_session)


    def update_session(self, combat_session: CombatSession):
        session_id: UUID = combat_session.session_id
        path_to_file: Path = generate_file_name_by(session_id=session_id)
        
        if not path_to_file.exists():
            raise FileNotFoundError(f"Nie można aktualizować {path_to_file} ponieważ nie istnieje")

        with open(path_to_file, 'w', encoding="utf-8") as file:
            file.write(combat_session.model_dump_json(indent=4))
       

    def list_sessions(self):
        path_to_sessions: Path = Path("data/sessions/")
        list_of_files = list(path_to_sessions.glob("*.json"))
        sessions = []

        for file in list_of_files:
            with open(file, 'r', encoding="utf-8") as file_session:
                session = json.load(file_session)
            sessions.append({"session_id": session["session_id"], "session_name": session["name"]})

        return sessions


    def remove_session(self, session_id: UUID):
        path_to_file: Path = generate_file_name_by(session_id=session_id)

        if not path_to_file.exists():
            raise FileNotFoundError(f"Nie można usunąć {path_to_file} ponieważ nie istnieje")

        path_to_file.unlink()