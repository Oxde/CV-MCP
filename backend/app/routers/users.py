"""User profile and onboarding routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from ..database import get_db
from ..models.models import User

router = APIRouter(prefix="/api/users", tags=["users"])


class UserCreate(BaseModel):
    pass  # No info needed to create


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None
    title: Optional[str] = None
    summary: Optional[str] = None
    years_experience: Optional[int] = None
    education: Optional[list] = None
    work_experience: Optional[list] = None
    skills: Optional[list] = None
    languages: Optional[list] = None
    certifications: Optional[list] = None
    projects: Optional[list] = None
    preferred_template: Optional[str] = None
    target_roles: Optional[list] = None
    preferred_industries: Optional[list] = None
    onboarding_complete: Optional[bool] = None


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str
    location: str
    linkedin: str
    github: str
    portfolio: str
    title: str
    summary: str
    years_experience: int
    education: list
    work_experience: list
    skills: list
    languages: list
    certifications: list
    projects: list
    preferred_template: str
    target_roles: list
    preferred_industries: list
    onboarding_complete: bool

    class Config:
        from_attributes = True


@router.post("", response_model=UserResponse)
def create_user(db: Session = Depends(get_db)):
    """Create a new user (start onboarding)."""
    user = User()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in update.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user
