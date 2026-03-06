"""CV management and generation routes."""
import os
import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from ..database import get_db
from ..models.models import User, CV, Vacancy
from ..services.cv_generator import build_cv_data, tailor_cv_for_vacancy
from ..services.pdf_service import generate_pdf
from ..services.template_renderer import render_cv_html, get_available_templates

router = APIRouter(prefix="/api/cvs", tags=["cvs"])


class CVCreate(BaseModel):
    user_id: int
    name: Optional[str] = "My CV"
    template_id: Optional[str] = "modern"
    vacancy_id: Optional[int] = None


class CVUpdate(BaseModel):
    name: Optional[str] = None
    template_id: Optional[str] = None
    cv_data: Optional[dict] = None


class CVResponse(BaseModel):
    id: int
    user_id: int
    name: str
    template_id: str
    html_content: str
    cv_data: dict
    vacancy_id: Optional[int]
    is_base: bool
    pdf_path: str

    class Config:
        from_attributes = True


@router.get("/templates")
def list_templates():
    """Get all available CV templates."""
    return get_available_templates()


@router.get("/{user_id}", response_model=list[CVResponse])
def list_cvs(user_id: int, db: Session = Depends(get_db)):
    return db.query(CV).filter(CV.user_id == user_id).order_by(CV.updated_at.desc()).all()


@router.post("", response_model=CVResponse)
async def create_cv(data: CVCreate, db: Session = Depends(get_db)):
    """Generate a new CV from user profile."""
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    cv_data = build_cv_data(user)

    # If targeting a vacancy, tailor the CV
    if data.vacancy_id:
        vacancy = db.query(Vacancy).filter(Vacancy.id == data.vacancy_id).first()
        if vacancy:
            cv_data = await tailor_cv_for_vacancy(cv_data, vacancy)

    html_content = render_cv_html(data.template_id, cv_data)

    cv = CV(
        user_id=data.user_id,
        name=data.name,
        template_id=data.template_id,
        html_content=html_content,
        cv_data=cv_data,
        vacancy_id=data.vacancy_id,
        is_base=data.vacancy_id is None,
    )
    db.add(cv)
    db.commit()
    db.refresh(cv)
    return cv


@router.get("/detail/{cv_id}", response_model=CVResponse)
def get_cv(cv_id: int, db: Session = Depends(get_db)):
    cv = db.query(CV).filter(CV.id == cv_id).first()
    if not cv:
        raise HTTPException(status_code=404, detail="CV not found")
    return cv


@router.patch("/{cv_id}", response_model=CVResponse)
def update_cv(cv_id: int, update: CVUpdate, db: Session = Depends(get_db)):
    cv = db.query(CV).filter(CV.id == cv_id).first()
    if not cv:
        raise HTTPException(status_code=404, detail="CV not found")

    if update.name is not None:
        cv.name = update.name
    if update.template_id is not None:
        cv.template_id = update.template_id
    if update.cv_data is not None:
        cv.cv_data = update.cv_data

    # Re-render HTML if data or template changed
    if update.cv_data is not None or update.template_id is not None:
        from ..services.template_renderer import render_cv_html
        cv.html_content = render_cv_html(cv.template_id, cv.cv_data)

    db.commit()
    db.refresh(cv)
    return cv


@router.post("/{cv_id}/pdf")
async def export_pdf(cv_id: int, db: Session = Depends(get_db)):
    """Generate PDF from CV."""
    cv = db.query(CV).filter(CV.id == cv_id).first()
    if not cv:
        raise HTTPException(status_code=404, detail="CV not found")

    pdf_path = await generate_pdf(cv.html_content, f"cv_{cv_id}")
    cv.pdf_path = pdf_path
    db.commit()

    return FileResponse(
        pdf_path,
        media_type="application/pdf" if pdf_path.endswith(".pdf") else "text/html",
        filename=f"{cv.name}.pdf",
    )


@router.post("/{cv_id}/change-template", response_model=CVResponse)
def change_template(cv_id: int, template_id: str, db: Session = Depends(get_db)):
    """Re-render CV with a different template."""
    cv = db.query(CV).filter(CV.id == cv_id).first()
    if not cv:
        raise HTTPException(status_code=404, detail="CV not found")

    cv.template_id = template_id
    cv.html_content = render_cv_html(template_id, cv.cv_data)
    db.commit()
    db.refresh(cv)
    return cv


@router.delete("/{cv_id}")
def delete_cv(cv_id: int, db: Session = Depends(get_db)):
    cv = db.query(CV).filter(CV.id == cv_id).first()
    if not cv:
        raise HTTPException(status_code=404, detail="CV not found")
    db.delete(cv)
    db.commit()
    return {"ok": True}
