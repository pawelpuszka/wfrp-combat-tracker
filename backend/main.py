from fastapi import FastAPI
from backend.api.routes import characters

app = FastAPI()

app.include_router(characters.router,  prefix="/api/characters", tags=["characters"])