import os
from pathlib import Path
from app.database.database import Base, engine


def init_db():

    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    os.makedirs(data_dir, exist_ok=True)
    db_file = data_dir / "note_app.db"
    db_exists = db_file.exists()

    if not db_exists:
        print("Creating database and tables...")
        Base.metadata.create_all(bind=engine)
        print(f"Database created at {db_file}")
    else:
        print(f"Database already exists at {db_file}")

    return db_file


def check_db_connection():
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception as e:
        print(f"Database connection error: {e}")
        return False


if __name__ == "__main__":
    init_db()
    if check_db_connection():
        print("Database connection successful!")
    else:
        print("Database connection failed!")
