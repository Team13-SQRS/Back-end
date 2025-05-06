from sqlalchemy.orm import Session
from .models import User, Note
from app.security.hashing import get_password_hash, verify_password


def create_user(db: Session, username: str, password: str) -> User:
    """Create a new user in the database.
    Args:
        db: Database session
        username: Unique username
        password: Plain-text password (will be hashed)
    Returns:
        User: Created user object
    """
    hashed_password = get_password_hash(password)
    db_user = User(username=username, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user


def get_note_by_id(db: Session, note_id: int):
    return db.query(Note).filter(Note.id == note_id).first()


def create_note(db: Session, title: str, content: str, user_id: int):
    db_note = Note(title=title, content=content, user_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def update_note(
        db: Session,
        note_id: int,
        title: str = None,
        content: str = None
):
    note = get_note_by_id(db, note_id)
    if title is not None:
        note.title = title
    if content is not None:
        note.content = content
    db.commit()
    db.refresh(note)
    return note


def delete_note(db: Session, note_id: int):
    note = get_note_by_id(db, note_id)
    if note:
        db.delete(note)
        db.commit()
    return note


def get_user_notes(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(Note)
        .filter(Note.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
