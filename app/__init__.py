from app.database.database import Base, engine, get_db
from app.database.crud import create_user, authenticate_user, get_user_by_username
from sqlalchemy.orm import Session
import sqlite3
from tabulate import tabulate

Base.metadata.create_all(bind=engine)


def print_db_contents():
    print("\nDatabase content:")
    conn = sqlite3.connect('data/note_app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        table_name = table[0]
        print(f"\nTable: {table_name}")
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [column[1] for column in cursor.fetchall()]
        print(tabulate(rows, headers=columns, tablefmt="grid"))
    conn.close()


def main():
    db: Session = next(get_db())

    # Create user
    username = "alex"
    password = "mysecretpassword"
    print(f"User: {username}\tPassword: {password}")
    user = create_user(db, username, password)
    print(f"User created: ID={user.id}, username={user.username}")
    print(f"Hash password: {user.password_hash}")

    print("\nVerify login:")
    print("mysecretpassword:", authenticate_user(db, username, password) is not None)
    print("wrongpassword:", authenticate_user(db, username, "wrong") is not None)

    print_db_contents()


if __name__ == "__main__":
    main()