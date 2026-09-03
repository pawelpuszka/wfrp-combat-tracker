from backend.db.connection import engine
from sqlalchemy import text

def test_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Połączenie działa!", result.fetchone())

test_connection()