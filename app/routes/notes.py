from fastapi import APIRouter, HTTPException, Depends
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


@router.post("/", response_model=NoteResponse)
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_note = crud.create_note(db, note.title, note.content, current_user.id)
    return db_note


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    note = crud.get_note_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this note"
        )
    return note


@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    note_update: NoteUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    note = crud.get_note_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this note"
        )
    updated_note = crud.update_note(
        db, note_id, title=note_update.title, content=note_update.content
    )
    return updated_note


@router.delete("/{note_id}")
def delete_note(
    note_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    note = crud.get_note_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this note"
        )
    crud.delete_note(db, note_id)
    return {"message": "Note deleted successfully"}


@router.get("/", response_model=List[NoteResponse])
def list_notes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    notes = crud.get_user_notes(db, current_user.id, skip=skip, limit=limit)
    return notes


@router.post("/{note_id}/translate", response_model=TranslateNoteResponse)
def translate_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    note = crud.get_note_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to translate this note",
        )
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
