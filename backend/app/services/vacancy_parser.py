"""Parse job vacancies from URLs and text."""
import re
from typing import Optional
import httpx
from bs4 import BeautifulSoup
from anthropic import AsyncAnthropic

from ..config import settings

client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)


async def parse_vacancy_from_url(url: str) -> dict:
    """Fetch and parse a job posting from a URL."""
    try:
        async with httpx.AsyncClient(
            follow_redirects=True,
            timeout=15.0,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/120.0.0.0 Safari/537.36"
            }
        ) as http:
            response = await http.get(url)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove scripts, styles, nav, footer
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)
        # Trim to reasonable size
        text = text[:6000]

        # Use AI to extract structured data
        extracted = await _extract_with_ai(text, url)
        return extracted

    except httpx.HTTPError as e:
        return {"error": f"Could not fetch URL: {str(e)}", "url": url}
    except Exception as e:
        return {"error": f"Parse error: {str(e)}", "url": url}


async def parse_vacancy_from_text(text: str) -> dict:
    """Parse job posting from pasted text."""
    return await _extract_with_ai(text[:6000], "")


async def _extract_with_ai(text: str, url: str) -> dict:
    """Use AI to extract structured vacancy data from text."""
    prompt = f"""Extract job posting information from this text. Return JSON only.

Text:
{text}

Return this exact JSON structure (use empty string if not found):
{{
  "title": "Job Title",
  "company": "Company Name",
  "location": "City, Country or Remote",
  "description": "Brief 2-3 sentence summary of the role",
  "requirements": ["requirement 1", "requirement 2", ...],
  "salary_range": "$XX,XXX - $XX,XXX or empty",
  "nice_to_have": ["nice to have 1", ...],
  "tech_stack": ["technology 1", "technology 2", ...]
}}"""

    response = await client.messages.create(
        model=settings.AI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=1000,
    )

    content = response.content[0].text
    # Extract JSON from response
    import json
    try:
        # Try to find JSON in the response
        json_match = re.search(r"\{[\s\S]*\}", content)
        if json_match:
            data = json.loads(json_match.group())
            data["url"] = url
            data["source"] = "link" if url else "text"
            return data
    except json.JSONDecodeError:
        pass

    return {
        "title": "",
        "company": "",
        "location": "",
        "description": text[:500],
        "requirements": [],
        "url": url,
        "source": "link" if url else "text",
        "error": "Could not parse structured data",
    }
