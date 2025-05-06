from fastapi import APIRouter, HTTPException, Depends, status
from app.database import crud
from app.services.translate import TranslationService
from app.auth.dependencies import (
    get_current_user,
)  # JWT tokens
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.database import get_db
from typing import List, Optional
from datetime import datetime

router = APIRouter()


# --------------- Helper Functions ---------------
def verify_note_ownership(note_id: int,
                          user_id: int,
                          db: Session
                          ) -> crud.Note:
    """Verify note exists and user has ownership.

    Args:
        note_id: Target note ID
        user_id: Authenticated user ID
        db: Database session

    Returns:
        Note: Verified note object

    Raises:
        HTTPException: 404 if not found, 403 if unauthorized
    """
    note = crud.get_note_by_id(db, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note resource not found"
        )
    if note.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized note access"
        )
    return note


# --------------- Pydantic Models ---------------
class NoteBase(BaseModel):
    title: str
    content: str


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class NoteResponse(NoteBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TranslateNoteResponse(BaseModel):
    translated_text: str


# --------------- Route Handlers ---------------
@router.post("/", response_model=NoteResponse)
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Create a new note for the authenticated user."""
    return crud.create_note(db, note.title, note.content, current_user.id)


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Retrieve a specific note with authorization check."""
    return verify_note_ownership(note_id, current_user.id, db)


@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    note_update: NoteUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Update note details with partial data."""
    verify_note_ownership(note_id, current_user.id, db)
    return crud.update_note(
        db, note_id,
        title=note_update.title,
        content=note_update.content
    )


@router.delete("/{note_id}")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Permanently delete a note."""
    verify_note_ownership(note_id, current_user.id, db)
    crud.delete_note(db, note_id)
    return {"message": "Note deleted successfully"}


@router.get("/", response_model=List[NoteResponse])
def list_notes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """List all notes for the authenticated user."""
    return crud.get_user_notes(db, current_user.id, skip=skip, limit=limit)


@router.post("/{note_id}/translate", response_model=TranslateNoteResponse)
def translate_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Translate note content using external service."""
    note = verify_note_ownership(note_id, current_user.id, db)
    translated_text = TranslationService.translate_text(
        note.content,
        source_lang="ru",
        target_lang="en",
    )
    if not translated_text:
        raise HTTPException(status_code=502, detail="Translation failed")

    # Fix: If the translation returns a list, join it into a string
    if isinstance(translated_text, list):
        translated_text = " ".join(translated_text)

    return TranslateNoteResponse(translated_text=translated_text)
