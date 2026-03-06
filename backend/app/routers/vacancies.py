"""Vacancy management routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from ..database import get_db
from ..models.models import Vacancy
from ..services.vacancy_parser import parse_vacancy_from_url, parse_vacancy_from_text

router = APIRouter(prefix="/api/vacancies", tags=["vacancies"])


class VacancyCreate(BaseModel):
    user_id: int
    title: Optional[str] = ""
    company: Optional[str] = ""
    location: Optional[str] = ""
    description: Optional[str] = ""
    requirements: Optional[list] = []
    salary_range: Optional[str] = ""
    url: Optional[str] = ""
    source: Optional[str] = "manual"


class VacancyFromURL(BaseModel):
    user_id: int
    url: str


class VacancyFromText(BaseModel):
    user_id: int
    text: str


class VacancyUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[list] = None
    salary_range: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    cv_id: Optional[int] = None


class VacancyResponse(BaseModel):
    id: int
    user_id: int
    title: str
    company: str
    location: str
    description: str
    requirements: list
    salary_range: str
    url: str
    source: str
    status: str
    notes: str
    cv_id: Optional[int]

    class Config:
        from_attributes = True


@router.get("/{user_id}", response_model=list[VacancyResponse])
def list_vacancies(user_id: int, db: Session = Depends(get_db)):
    return db.query(Vacancy).filter(Vacancy.user_id == user_id).order_by(Vacancy.created_at.desc()).all()


@router.post("", response_model=VacancyResponse)
def create_vacancy(data: VacancyCreate, db: Session = Depends(get_db)):
    vacancy = Vacancy(**data.model_dump())
    db.add(vacancy)
    db.commit()
    db.refresh(vacancy)
    return vacancy


@router.post("/from-url", response_model=VacancyResponse)
async def create_from_url(data: VacancyFromURL, db: Session = Depends(get_db)):
    """Parse a vacancy from a URL (LinkedIn, Indeed, etc.)."""
    parsed = await parse_vacancy_from_url(data.url)
    if "error" in parsed:
        # Still create with partial data
        pass

    vacancy = Vacancy(
        user_id=data.user_id,
        title=parsed.get("title", ""),
        company=parsed.get("company", ""),
        location=parsed.get("location", ""),
        description=parsed.get("description", ""),
        requirements=parsed.get("requirements", []) + parsed.get("tech_stack", []),
        salary_range=parsed.get("salary_range", ""),
        url=data.url,
        source="link",
    )
    db.add(vacancy)
    db.commit()
    db.refresh(vacancy)
    return vacancy


@router.post("/from-text", response_model=VacancyResponse)
async def create_from_text(data: VacancyFromText, db: Session = Depends(get_db)):
    """Parse a vacancy from pasted text."""
    parsed = await parse_vacancy_from_text(data.text)

    vacancy = Vacancy(
        user_id=data.user_id,
        title=parsed.get("title", ""),
        company=parsed.get("company", ""),
        location=parsed.get("location", ""),
        description=parsed.get("description", ""),
        requirements=parsed.get("requirements", []) + parsed.get("tech_stack", []),
        salary_range=parsed.get("salary_range", ""),
        source="text",
    )
    db.add(vacancy)
    db.commit()
    db.refresh(vacancy)
    return vacancy


@router.patch("/{vacancy_id}", response_model=VacancyResponse)
def update_vacancy(vacancy_id: int, update: VacancyUpdate, db: Session = Depends(get_db)):
    vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")

    for field, value in update.model_dump(exclude_unset=True).items():
        setattr(vacancy, field, value)

    db.commit()
    db.refresh(vacancy)
    return vacancy


@router.delete("/{vacancy_id}")
def delete_vacancy(vacancy_id: int, db: Session = Depends(get_db)):
    vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    db.delete(vacancy)
    db.commit()
    return {"ok": True}
