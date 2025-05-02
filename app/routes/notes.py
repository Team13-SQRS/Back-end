from fastapi import APIRouter, HTTPException, Depends
from app.database import crud
from app.services.translate import TranslationService
from app.auth.dependencies import get_current_user  #JWT tokens
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.database import get_db

router = APIRouter()


class TranslateNoteResponse(BaseModel):
    translated_text: str


@router.post("/notes/{note_id}/translate", response_model=TranslateNoteResponse)
def translate_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    note = crud.get_note_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to translate this note")

    translated_text = TranslationService.translate_text(note.content, source_lang="ru", target_lang="en")
    if not translated_text:
        raise HTTPException(status_code=502, detail="Translation failed")

    return TranslateNoteResponse(translated_text=translated_text)
