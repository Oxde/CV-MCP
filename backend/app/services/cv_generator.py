"""Generate CV HTML from templates and user data."""
import json
from typing import Optional
from openai import AsyncOpenAI

from ..config import settings
from ..models.models import User, CV, Vacancy

client = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_BASE_URL,
)


def build_cv_data(user: User, vacancy: Optional[Vacancy] = None) -> dict:
    """Build CV data dict from user profile, optionally tailored for a vacancy."""
    data = {
        "full_name": user.full_name,
        "email": user.email,
        "phone": user.phone,
        "location": user.location,
        "linkedin": user.linkedin,
        "github": user.github,
        "portfolio": user.portfolio,
        "title": user.title,
        "summary": user.summary,
        "experience": user.work_experience or [],
        "education": user.education or [],
        "skills": user.skills or [],
        "languages": user.languages or [],
        "certifications": user.certifications or [],
        "projects": user.projects or [],
    }
    return data


async def tailor_cv_for_vacancy(cv_data: dict, vacancy: Vacancy) -> dict:
    """Use AI to tailor CV data for a specific vacancy."""
    prompt = f"""You are an expert resume writer. Tailor this CV data for the target job.

Current CV data:
```json
{json.dumps(cv_data, indent=2)}
```

Target job:
- Title: {vacancy.title}
- Company: {vacancy.company}
- Description: {vacancy.description}
- Requirements: {json.dumps(vacancy.requirements)}

Rules:
1. Rewrite the summary to target this specific role
2. Reorder and emphasize relevant skills
3. Adjust experience bullet points to highlight relevant achievements
4. Do NOT fabricate experience - only reframe existing content
5. Keep all factual info (dates, companies, degrees) unchanged

Return the COMPLETE updated cv_data as JSON only. No explanation."""

    response = await client.chat.completions.create(
        model=settings.AI_MODEL_SMART,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=3000,
    )

    import re
    content = response.choices[0].message.content
    try:
        json_match = re.search(r"\{[\s\S]*\}", content)
        if json_match:
            return json.loads(json_match.group())
    except json.JSONDecodeError:
        pass

    return cv_data  # Return original if parsing fails
