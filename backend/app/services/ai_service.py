"""AI service with smart context management for cheap model usage."""
from typing import Optional
from anthropic import AsyncAnthropic
from sqlalchemy.orm import Session

from ..config import settings
from ..models.models import User, ChatMessage, CV, Vacancy

client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """You are CV Craft AI, an expert career coach and resume writer.
You help users create outstanding, ATS-friendly resumes tailored to specific job descriptions.

Your personality: Professional but friendly. Direct and actionable. You celebrate wins.

Key rules:
- Keep responses concise (2-4 sentences unless asked for more)
- When editing CVs, make specific suggestions with exact wording
- Focus on quantifiable achievements and action verbs
- Always consider the target role when making suggestions
- If user info is missing, ask for it naturally in conversation"""

ONBOARDING_PROMPT = """You are guiding a new user through CV Craft onboarding.
Be warm, conversational, and collect their info step by step.

Flow:
1. Greet them, ask their name
2. Ask about their current role/title and experience level
3. Ask about their education (briefly)
4. Ask about their key skills
5. Ask about their work experience (most recent first)
6. Ask about any notable projects
7. Ask what kind of roles they're targeting

Keep each message short. Ask ONE thing at a time. Be encouraging.
When you have enough info, say "ONBOARDING_COMPLETE" at the end of your message.

Extract structured data from their responses. When you detect user info, include a JSON block
at the end of your message in this format:
```json
{"extract": {"field": "value"}}
```

Valid fields: full_name, email, phone, location, title, summary, years_experience,
skills (array), education (array of {degree, school, year}),
work_experience (array of {company, title, start, end, bullets}),
projects (array of {name, description, tech}), target_roles (array),
linkedin, github, portfolio"""

CV_EDIT_PROMPT = """You are helping the user edit their CV. You have access to the current CV content.
When the user asks for changes:
1. Understand what they want changed
2. Make the edit and return the FULL updated CV data as JSON

When you make changes, include the updated data in this format:
```json
{"cv_update": {... full cv_data object ...}}
```

Be specific about what you changed and why."""


def _build_user_context(user: User) -> str:
    """Build a compact context string about the user (saves tokens)."""
    parts = []
    if user.full_name:
        parts.append(f"Name: {user.full_name}")
    if user.title:
        parts.append(f"Title: {user.title}")
    if user.years_experience:
        parts.append(f"Experience: {user.years_experience}y")
    if user.skills:
        parts.append(f"Skills: {', '.join(user.skills[:15])}")
    if user.target_roles:
        parts.append(f"Targeting: {', '.join(user.target_roles)}")
    if user.location:
        parts.append(f"Location: {user.location}")
    return " | ".join(parts) if parts else "New user (no info yet)"


def _build_cv_context(cv: CV) -> str:
    """Build compact CV context."""
    if not cv or not cv.cv_data:
        return ""
    data = cv.cv_data
    parts = [f"CV: {cv.name} (template: {cv.template_id})"]
    if data.get("summary"):
        parts.append(f"Summary: {data['summary'][:200]}")
    if data.get("experience"):
        exp_list = [f"{e.get('title', '')} @ {e.get('company', '')}" for e in data["experience"][:3]]
        parts.append(f"Experience: {'; '.join(exp_list)}")
    return " | ".join(parts)


def _build_vacancy_context(vacancy: Vacancy) -> str:
    """Build compact vacancy context."""
    if not vacancy:
        return ""
    parts = [f"Target: {vacancy.title} at {vacancy.company}"]
    if vacancy.requirements:
        parts.append(f"Requires: {', '.join(vacancy.requirements[:10])}")
    if vacancy.description:
        parts.append(f"Desc: {vacancy.description[:300]}")
    return " | ".join(parts)


async def chat(
    db: Session,
    user: User,
    message: str,
    context_type: str = "general",
    cv_id: Optional[int] = None,
    vacancy_id: Optional[int] = None,
) -> str:
    """Process a chat message with smart context management."""

    # Build system prompt based on context
    if context_type == "onboarding":
        system = ONBOARDING_PROMPT
    elif context_type == "cv_edit":
        system = CV_EDIT_PROMPT
    else:
        system = SYSTEM_PROMPT

    # Add user context (compact, saves tokens)
    user_ctx = _build_user_context(user)
    system += f"\n\nUser context: {user_ctx}"

    # Add CV context if editing
    if cv_id:
        cv = db.query(CV).filter(CV.id == cv_id, CV.user_id == user.id).first()
        if cv:
            cv_ctx = _build_cv_context(cv)
            if cv_ctx:
                system += f"\n\nCurrent CV: {cv_ctx}"
            if cv.cv_data:
                system += f"\n\nFull CV data:\n```json\n{_compact_json(cv.cv_data)}\n```"

    # Add vacancy context if provided
    if vacancy_id:
        vacancy = db.query(Vacancy).filter(
            Vacancy.id == vacancy_id, Vacancy.user_id == user.id
        ).first()
        if vacancy:
            system += f"\n\n{_build_vacancy_context(vacancy)}"

    # Get recent chat history (limited for cost)
    recent_messages = (
        db.query(ChatMessage)
        .filter(
            ChatMessage.user_id == user.id,
            ChatMessage.context_type == context_type,
        )
        .order_by(ChatMessage.id.desc())
        .limit(settings.MAX_CONTEXT_MESSAGES)
        .all()
    )
    recent_messages.reverse()

    # Build messages array (Anthropic format: no system in messages)
    messages = []
    for msg in recent_messages:
        messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": message})

    # Call AI
    response = await client.messages.create(
        model=settings.AI_MODEL,
        system=system,
        messages=messages,
        temperature=0.7,
        max_tokens=2000,
    )

    assistant_message = response.content[0].text

    # Save messages to DB
    db.add(ChatMessage(
        user_id=user.id, role="user", content=message,
        context_type=context_type, cv_id=cv_id,
    ))
    db.add(ChatMessage(
        user_id=user.id, role="assistant", content=assistant_message,
        context_type=context_type, cv_id=cv_id,
    ))
    db.commit()

    return assistant_message


def _compact_json(data: dict) -> str:
    """Minimal JSON representation to save tokens."""
    import json
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False)
