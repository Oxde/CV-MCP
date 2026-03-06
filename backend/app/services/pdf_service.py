"""PDF generation service using Playwright."""
import os
import asyncio
from pathlib import Path
from ..config import settings


async def generate_pdf(html_content: str, output_name: str = "cv") -> str:
    """Generate a PDF from HTML content using Playwright."""
    output_dir = Path(settings.CV_OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = str(output_dir / f"{output_name}.pdf")

    try:
        from playwright.async_api import async_playwright

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.set_content(html_content, wait_until="networkidle")
            await page.pdf(
                path=pdf_path,
                format="Letter",
                margin={"top": "0.5in", "right": "0.5in", "bottom": "0.5in", "left": "0.5in"},
                print_background=True,
                scale=0.85,
            )
            await browser.close()

        return pdf_path
    except Exception as e:
        # Fallback: save HTML for manual printing
        html_path = str(output_dir / f"{output_name}.html")
        with open(html_path, "w") as f:
            f.write(html_content)
        return html_path
