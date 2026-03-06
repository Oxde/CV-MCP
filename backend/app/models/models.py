from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    onboarding_complete = Column(Boolean, default=False)

    # Core identity
    full_name = Column(String(200), default="")
    email = Column(String(200), default="")
    phone = Column(String(50), default="")
    location = Column(String(200), default="")
    linkedin = Column(String(300), default="")
    github = Column(String(300), default="")
    portfolio = Column(String(300), default="")

    # Professional info
    title = Column(String(200), default="")
    summary = Column(Text, default="")
    years_experience = Column(Integer, default=0)
    education = Column(JSON, default=list)  # [{degree, school, year, gpa}]
    work_experience = Column(JSON, default=list)  # [{company, title, start, end, bullets}]
    skills = Column(JSON, default=list)  # [str]
    languages = Column(JSON, default=list)  # [{language, level}]
    certifications = Column(JSON, default=list)  # [{name, issuer, year}]
    projects = Column(JSON, default=list)  # [{name, description, tech, url}]

    # Preferences
    preferred_template = Column(String(100), default="modern")
    target_roles = Column(JSON, default=list)  # [str]
    preferred_industries = Column(JSON, default=list)  # [str]

    # Relationships
    vacancies = relationship("Vacancy", back_populates="user", cascade="all, delete-orphan")
    cvs = relationship("CV", back_populates="user", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="user", cascade="all, delete-orphan")


class Vacancy(Base):
    __tablename__ = "vacancies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Job info
    title = Column(String(300), default="")
    company = Column(String(200), default="")
    location = Column(String(200), default="")
    description = Column(Text, default="")
    requirements = Column(JSON, default=list)  # [str]
    salary_range = Column(String(100), default="")
    url = Column(String(500), default="")
    source = Column(String(100), default="manual")  # manual, linkedin, link

    # Status
    status = Column(String(50), default="saved")  # saved, applied, interview, rejected, offer
    notes = Column(Text, default="")

    # Generated CV for this vacancy
    cv_id = Column(Integer, ForeignKey("cvs.id"), nullable=True)

    user = relationship("User", back_populates="vacancies")
    cv = relationship("CV", foreign_keys=[cv_id])


class CV(Base):
    __tablename__ = "cvs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    name = Column(String(200), default="My CV")
    template_id = Column(String(100), default="modern")
    html_content = Column(Text, default="")
    cv_data = Column(JSON, default=dict)  # Structured CV data used to generate HTML
    vacancy_id = Column(Integer, nullable=True)  # If tailored for a specific vacancy
    pdf_path = Column(String(500), default="")
    is_base = Column(Boolean, default=False)  # Base CV vs tailored

    user = relationship("User", back_populates="cvs")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    role = Column(String(20))  # user, assistant, system
    content = Column(Text)
    context_type = Column(String(50), default="general")  # general, cv_edit, vacancy, onboarding
    cv_id = Column(Integer, nullable=True)  # If related to a specific CV
    extra_data = Column(JSON, default=dict)

    user = relationship("User", back_populates="chat_messages")
