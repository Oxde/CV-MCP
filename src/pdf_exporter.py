#!/usr/bin/env python3
"""
PDF Exporter - Simple HTML to Professional PDF
==============================================
Converts HTML resumes to high-quality, print-ready PDF files.
Simple and portable - works with optional WeasyPrint or browser fallback.
"""

import os
import tempfile
import asyncio
from pathlib import Path
from typing import Dict, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFExporter:
    """
    🎯 Simple & Portable PDF Export
    
    HTML → Professional PDF with multiple backend options:
    - pyppeteer (headless Chrome) - automated
    - WeasyPrint - optional high quality
    - browser - manual fallback
    """
    
    def __init__(self, output_dir: str = "output/pdf"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Try backends in order of preference
        self.backend = "browser"
        self.pyppeteer = None
        self.weasyprint = None
        
        # Try pyppeteer first (best automation)
        try:
            import pyppeteer
            self.pyppeteer = pyppeteer
            self.backend = "pyppeteer"
            logger.info("✅ Pyppeteer available - Automated PDF generation enabled")
        except ImportError:
            logger.info("📝 Pyppeteer not available")
        
        # Try WeasyPrint as secondary option
        if not self.pyppeteer:
            try:
                import weasyprint
                self.weasyprint = weasyprint
                self.backend = "weasyprint"
                logger.info("✅ WeasyPrint available - PDF generation enabled")
            except (ImportError, OSError):
                logger.info("📝 WeasyPrint not available")
        
        logger.info(f"🎯 PDFExporter initialized: {self.backend} → {self.output_dir}")
    
    def convert_html_to_pdf(self, html_path: str, output_name: Optional[str] = None, 
                          style: str = "professional") -> str:
        """
        Convert HTML to PDF - Simple & Reliable
        
        Args:
            html_path: Path to HTML file or HTML content string
            output_name: Optional output filename
            style: PDF style (professional, compact, detailed)
            
        Returns:
            Path to generated PDF or instructions for browser method
        """
        
        # Load HTML content
        if html_path.endswith('.html') and Path(html_path).exists():
            html_path = Path(html_path)
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            base_name = html_path.stem
        else:
            html_content = html_path  # Assume it's HTML string
            base_name = "resume"
        
        # Generate output filename
        if not output_name:
            output_name = f"{base_name}_{style}"
        
        output_path = self.output_dir / f"{output_name}.pdf"
        
        if self.backend == "pyppeteer":
            return self._generate_with_pyppeteer(html_content, output_path, style, html_path)
        elif self.backend == "weasyprint":
            return self._generate_with_weasyprint(html_content, output_path, style)
        else:
            return self._generate_with_browser(html_content, output_path, style, html_path)
    
    def _generate_with_weasyprint(self, html_content: str, output_path: Path, style: str) -> str:
        """Generate PDF using WeasyPrint"""
        try:
            logger.info(f"📄 Converting HTML → PDF: {output_path.name}")
            
            # Optimize HTML for PDF
            optimized_html = self._optimize_for_pdf(html_content, style)
            
            # Generate PDF with WeasyPrint
            html_doc = self.weasyprint.HTML(string=optimized_html)
            html_doc.write_pdf(str(output_path))
            
            # Validate result
            if not output_path.exists() or output_path.stat().st_size < 1000:
                raise RuntimeError("PDF generation failed - file too small or missing")
            
            size_kb = round(output_path.stat().st_size / 1024, 1)
            logger.info(f"✅ PDF ready: {output_path.name} ({size_kb} KB)")
            
            return str(output_path)
            
        except Exception as e:
            logger.error(f"❌ WeasyPrint failed: {e}")
            # Fallback to browser method
            return self._generate_with_browser(html_content, output_path, style)
    
    def _generate_with_browser(self, html_content: str, output_path: Path, style: str, original_html_path=None) -> str:
        """Generate PDF using browser method"""
        
        # Create print-optimized HTML file
        optimized_html = self._optimize_for_pdf(html_content, style)
        temp_html = self.output_dir / f"{output_path.stem}_print.html"
        temp_html.write_text(optimized_html, encoding='utf-8')
        
        instructions = f"""
✅ HTML ready for PDF conversion!

📁 Print-optimized HTML saved: {temp_html}

🖨️ BROWSER METHOD (Simple & Reliable):
1. Open file in browser: {temp_html}
2. Press Cmd+P (Mac) or Ctrl+P (Windows)
3. Choose "Save as PDF"
4. Select "More settings" → "Margins: None"
5. Save as: {output_path}

💡 This method gives you perfect control over the final PDF appearance!

🎯 File ready: {temp_html}
"""
        
        logger.info(f"📄 Browser PDF method ready: {temp_html.name}")
        return instructions
    
    def _generate_with_pyppeteer(self, html_content: str, output_path: Path, style: str, html_path=None) -> str:
        """Generate PDF using pyppeteer (headless Chrome)"""
        try:
            logger.info(f"📄 Converting HTML → PDF with pyppeteer: {output_path.name}")
            
            # Optimize HTML for PDF
            optimized_html = self._optimize_for_pdf(html_content, style)
            
            # Create temporary HTML file for pyppeteer
            temp_html = self.output_dir / f"{output_path.stem}_temp.html"
            temp_html.write_text(optimized_html, encoding='utf-8')
            
            # Run async PDF generation with absolute path
            absolute_temp_html = temp_html.resolve()
            asyncio.run(self._async_generate_pdf(str(absolute_temp_html), str(output_path)))
            
            # Clean up temp file
            temp_html.unlink()
            
            # Validate result
            if not output_path.exists() or output_path.stat().st_size < 1000:
                raise RuntimeError("PDF generation failed - file too small or missing")
            
            size_kb = round(output_path.stat().st_size / 1024, 1)
            logger.info(f"✅ PDF ready: {output_path.name} ({size_kb} KB)")
            
            return str(output_path)
            
        except Exception as e:
            logger.error(f"❌ Pyppeteer failed: {e}")
            # Fallback to next available method
            if self.weasyprint:
                return self._generate_with_weasyprint(html_content, output_path, style)
            else:
                return self._generate_with_browser(html_content, output_path, style, html_path)
    
    async def _async_generate_pdf(self, html_file_path: str, pdf_path: str):
        """Async function to generate PDF with pyppeteer"""
        browser = None
        try:
            # Launch browser with proper options
            browser = await self.pyppeteer.launch({
                'headless': True,
                'args': ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
            })
            page = await browser.newPage()
            
            # Load the HTML file
            file_url = f"file://{html_file_path}"
            await page.goto(file_url, {'waitUntil': 'networkidle0'})
            
            # Generate PDF with proper settings
            await page.pdf({
                'path': pdf_path,
                'format': 'A4',
                'printBackground': True,
                'margin': {
                    'top': '0.75in',
                    'right': '0.75in', 
                    'bottom': '0.75in',
                    'left': '0.75in'
                }
            })
            
        finally:
            if browser:
                await browser.close()
    
    def _optimize_for_pdf(self, html_content: str, style: str) -> str:
        """Add PDF-optimized CSS"""
        
        # Style-specific configurations
        style_configs = {
            "professional": {
                "margin": "0.75in",
                "font_size": "11pt",
                "line_height": "1.4"
            },
            "compact": {
                "margin": "0.5in", 
                "font_size": "10pt",
                "line_height": "1.3"
            },
            "detailed": {
                "margin": "1in",
                "font_size": "12pt", 
                "line_height": "1.5"
            }
        }
        
        config = style_configs.get(style, style_configs["professional"])
        
        # PDF optimization CSS
        pdf_css = f"""
<style>
/* PDF Print Optimization */
@page {{
    size: A4;
    margin: {config['margin']};
}}

* {{
    -webkit-print-color-adjust: exact !important;
    color-adjust: exact !important;
    print-color-adjust: exact !important;
}}

body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
    font-size: {config['font_size']};
    line-height: {config['line_height']};
    color: #333;
    background: white;
    margin: 0;
    padding: 0;
}}

/* Remove web-specific elements for print */
@media print {{
    nav, .no-print {{
    display: none !important;
}}

    body {{
        font-size: {config['font_size']} !important;
    }}
    
    h1, h2, h3 {{
        page-break-after: avoid;
    }}
    
    .page-break {{
        page-break-before: always;
    }}
}}

/* Ensure text is selectable and crisp */
* {{
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}}
</style>
"""
        
        # Insert CSS before closing head tag or at the beginning
        if '</head>' in html_content:
            html_content = html_content.replace('</head>', f'{pdf_css}</head>')
        elif '<body>' in html_content:
            html_content = html_content.replace('<body>', f'{pdf_css}<body>')
        else:
            html_content = pdf_css + html_content
        
        return html_content
    
    def export_to_pdf(self, html_content: str, output_name: str, format_options: Optional[Dict[str, Any]] = None) -> str:
        """Legacy method for compatibility"""
        style = "professional"
        if format_options:
            if format_options.get("margin") == "0.5in":
                style = "compact"
            elif format_options.get("margin") == "1in":
                style = "detailed"
        
        return self.convert_html_to_pdf(html_content, output_name, style)
    
    def get_pdf_info(self, pdf_path: str) -> Dict[str, Any]:
        """Get PDF file information"""
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        
        size_bytes = pdf_path.stat().st_size
        
        return {
            "filename": pdf_path.name,
            "size_kb": round(size_bytes / 1024, 1),
            "size_mb": round(size_bytes / (1024 * 1024), 2),
            "backend": self.backend,
            "optimized": True
        }
    
    def test_pdf_generation(self) -> bool:
        """Test if PDF generation is working"""
        if self.backend == "none":
            return False
        
        try:
            test_html = """
            <html>
            <head><title>Test</title></head>
            <body>
                <h1>Test Resume</h1>
                <p>This is a test PDF generation.</p>
                <h2>Skills</h2>
                <ul>
                    <li>HTML to PDF conversion</li>
                    <li>Professional formatting</li>
                </ul>
            </body>
            </html>
            """
            
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=True) as f:
                html_doc = self.weasyprint.HTML(string=test_html)
                html_doc.write_pdf(f.name)
                
                # Check if file was created and has content
                return f.tell() > 1000 or Path(f.name).stat().st_size > 1000
                
        except Exception as e:
            logger.warning(f"PDF test failed: {e}")
            return False 