"""Chat routes for AI interaction."""
import json
import re
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from ..database import get_db
from ..models.models import User, ChatMessage
from ..services.ai_service import chat

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatRequest(BaseModel):
    user_id: int
    message: str
    context_type: Optional[str] = "general"  # general, onboarding, cv_edit
    cv_id: Optional[int] = None
    vacancy_id: Optional[int] = None


class ChatResponse(BaseModel):
    reply: str
    extracted_data: Optional[dict] = None
    cv_update: Optional[dict] = None
    onboarding_complete: bool = False


class ChatHistory(BaseModel):
    id: int
    role: str
    content: str
    context_type: str
    cv_id: Optional[int]

    class Config:
        from_attributes = True


@router.post("", response_model=ChatResponse)
async def send_message(data: ChatRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    reply = await chat(
        db=db,
        user=user,
        message=data.message,
        context_type=data.context_type,
        cv_id=data.cv_id,
        vacancy_id=data.vacancy_id,
    )

    # Parse any extracted data from AI response
    extracted_data = None
    cv_update = None
    onboarding_complete = False

    # Check for extracted user data (onboarding)
    json_match = re.search(r"```json\s*(\{[\s\S]*?\})\s*```", reply)
    if json_match:
        try:
            parsed = json.loads(json_match.group(1))
            if "extract" in parsed:
                extracted_data = parsed["extract"]
                # Auto-apply extracted data to user profile
                _apply_extracted_data(user, extracted_data, db)
            if "cv_update" in parsed:
                cv_update = parsed["cv_update"]
        except json.JSONDecodeError:
            pass

    if "ONBOARDING_COMPLETE" in reply:
        onboarding_complete = True
        user.onboarding_complete = True
        db.commit()
        reply = reply.replace("ONBOARDING_COMPLETE", "").strip()

    # Clean the reply (remove JSON blocks from display)
    clean_reply = re.sub(r"```json\s*\{[\s\S]*?\}\s*```", "", reply).strip()

    return ChatResponse(
        reply=clean_reply,
        extracted_data=extracted_data,
        cv_update=cv_update,
        onboarding_complete=onboarding_complete,
    )


@router.get("/history/{user_id}", response_model=list[ChatHistory])
def get_history(
    user_id: int,
    context_type: str = "general",
    limit: int = 50,
    db: Session = Depends(get_db),
):
    messages = (
        db.query(ChatMessage)
        .filter(
            ChatMessage.user_id == user_id,
            ChatMessage.context_type == context_type,
        )
        .order_by(ChatMessage.id.desc())
        .limit(limit)
        .all()
    )
    messages.reverse()
    return messages


@router.delete("/history/{user_id}")
def clear_history(
    user_id: int,
    context_type: str = "general",
    db: Session = Depends(get_db),
):
    db.query(ChatMessage).filter(
        ChatMessage.user_id == user_id,
        ChatMessage.context_type == context_type,
    ).delete()
    db.commit()
    return {"ok": True}


def _apply_extracted_data(user: User, data: dict, db: Session):
    """Apply extracted data from AI to user profile."""
    field_map = {
        "full_name": "full_name",
        "email": "email",
        "phone": "phone",
        "location": "location",
        "title": "title",
        "summary": "summary",
        "years_experience": "years_experience",
        "skills": "skills",
        "education": "education",
        "work_experience": "work_experience",
        "projects": "projects",
        "target_roles": "target_roles",
        "linkedin": "linkedin",
        "github": "github",
        "portfolio": "portfolio",
    }

    for key, field in field_map.items():
        if key in data and data[key]:
            current = getattr(user, field)
            new_val = data[key]

            # For lists, merge rather than replace
            if isinstance(current, list) and isinstance(new_val, list):
                # Add new items that aren't already there
                existing_strs = {json.dumps(x) if isinstance(x, dict) else str(x) for x in current}
                for item in new_val:
                    item_str = json.dumps(item) if isinstance(item, dict) else str(item)
                    if item_str not in existing_strs:
                        current.append(item)
                setattr(user, field, current)
            else:
                setattr(user, field, new_val)

    db.commit()
