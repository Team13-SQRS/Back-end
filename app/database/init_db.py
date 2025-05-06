import os
from app.database.database import Base, engine, DATA_DIR


def init_db():
    """Create database tables if they don't exist.

    Returns:
        Tuple: (success status, database file path)
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    db_file = DATA_DIR / "note_app.db"
    db_exists = db_file.exists()

    if not db_exists:
        print("Creating database and tables...")
        Base.metadata.create_all(bind=engine)
        print(f"Database created at {db_file}")
    else:
        print(f"Database already exists at {db_file}")

    return db_file


def check_db_connection():
    """Perform a basic connectivity check.

    Returns:
        bool: True if connection succeeds
    """
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
