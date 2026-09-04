from backend.db.connection import engine
from sqlalchemy import text
import sqlparse
import sys

def migrate_db_test(file):
    print("Migracja z pliku: ", file)

def migrate_db(file):
    print("START")
    print("Migracja z pliku: ", file)
    with open(file, 'r', encoding="UTF-8") as f:
        file_content = f.read()
    statements = sqlparse.split(file_content) 
    with engine.connect() as conn:
        for statement in statements:
            conn.execute(text(statement))
            print(f"Wykonano: {statement}")
        conn.commit()


if  __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Zapomniałeś podać ścieżki do pliku")
    else:
        migrate_db(sys.argv[1])
