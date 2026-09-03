from sqlalchemy import create_engine
from backend.config import settings
from sqlalchemy.orm import Session, sessionmaker


engine = create_engine(
    url=settings.database_url,
    pool_pre_ping=True,
    echo=(settings.environment == "development"),
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()