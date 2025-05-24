#!/usr/bin/env python3
"""
Optimal PDF Exporter Component
==============================
High-quality PDF generation using Playwright with optimal settings discovered through testing.
Uses the best configuration for single-page, professional resumes.
"""

import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

class OptimalPDFExporter:
    """
    PDF exporter using optimal Playwright configuration discovered through testing.
    Generates high-quality, single-page PDFs with proper fonts and spacing.
    """
    
    def __init__(self, output_dir: str):
        """
        Initialize the PDF exporter.
        
        Args:
            output_dir: Directory where PDFs will be saved
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"📄 OptimalPDFExporter initialized - Output: {self.output_dir}")
    
    def convert_html_to_pdf(self, html_file_path: str, output_name: Optional[str] = None) -> str:
        """
        Convert HTML to PDF using optimal Playwright configuration.
        
        Args:
            html_file_path: Path to the HTML file to convert
            output_name: Optional custom name for output PDF
            
        Returns:
            str: Path to the generated PDF file
            
        Raises:
            Exception: If PDF generation fails
        """
        try:
            # Import Playwright (lazy import to handle missing dependency gracefully)
            from playwright.sync_api import sync_playwright
        except ImportError:
            raise Exception(
                "Playwright not installed. Install with: pip install playwright && playwright install chromium"
            )
        
        html_file = Path(html_file_path)
        if not html_file.exists():
            raise Exception(f"HTML file not found: {html_file}")
        
        # Generate output filename
        if output_name:
            if not output_name.endswith('.pdf'):
                output_name += '.pdf'
            output_file = self.output_dir / output_name
        else:
            output_file = self.output_dir / f"{html_file.stem}.pdf"
        
        logger.info(f"🔄 Generating PDF: {html_file} → {output_file}")
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                
                # Read HTML content
                with open(html_file, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # Set content and wait for complete rendering
                page.set_content(html_content, wait_until='networkidle')
                
                # Optimal PDF configuration (discovered through extensive testing)
                pdf_options = {
                    'width': '8.5in',       # US Letter width for optimal layout
                    'height': '11in',       # US Letter height
                    'margin': {
                        'top': '0.6in',     # Tight but professional margins
                        'right': '0.6in',
                        'bottom': '0.6in',
                        'left': '0.6in'
                    },
                    'print_background': True,  # Include background colors and styling
                    'scale': 0.85,            # Scale down slightly for better content fit
                    'prefer_css_page_size': False,  # Use our dimensions
                    'display_header_footer': False   # No headers/footers
                }
                
                # Generate PDF
                page.pdf(path=str(output_file), **pdf_options)
                browser.close()
            
            if output_file.exists():
                file_size = output_file.stat().st_size
                logger.info(f"✅ PDF generated successfully!")
                logger.info(f"   File: {output_file.name}")
                logger.info(f"   Size: {file_size:,} bytes")
                
                return str(output_file)
            else:
                raise Exception("PDF file was not created")
                
        except Exception as e:
            logger.error(f"❌ PDF generation failed: {e}")
            raise Exception(f"PDF generation failed: {str(e)}")
    
    def get_template_path(self) -> str:
        """
        Get the path to the optimized resume template.
        
        Returns:
            str: Path to the optimized template
        """
        # Look for the optimized template in the workspace
        workspace_dir = self.output_dir.parent
        template_path = workspace_dir / "templates" / "saved_templates" / "Optimized_Resume_Template.html"
        
        if template_path.exists():
            return str(template_path)
        
        # Fallback to any template in saved_templates
        saved_templates_dir = workspace_dir / "templates" / "saved_templates"
        if saved_templates_dir.exists():
            html_files = list(saved_templates_dir.glob("*.html"))
            if html_files:
                return str(html_files[0])
        
        raise Exception("No optimized template found. Please save a template first.")
    
    def test_configuration(self) -> dict:
        """
        Test the PDF generation configuration.
        
        Returns:
            dict: Test results and configuration info
        """
        try:
            from playwright.sync_api import sync_playwright
            
            # Test basic functionality
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                
                # Simple test HTML
                test_html = """
                <!DOCTYPE html>
                <html>
                <head><title>Test</title></head>
                <body><h1>PDF Generation Test</h1><p>This is a test.</p></body>
                </html>
                """
                
                page.set_content(test_html)
                
                # Test our configuration
                test_file = self.output_dir / "test_config.pdf"
                page.pdf(
                    path=str(test_file),
                    width='8.5in',
                    height='11in',
                    margin={
                        'top': '0.6in',
                        'right': '0.6in',
                        'bottom': '0.6in',
                        'left': '0.6in'
                    },
                    print_background=True,
                    scale=0.85
                )
                
                browser.close()
                
                # Check result
                if test_file.exists():
                    file_size = test_file.stat().st_size
                    test_file.unlink()  # Clean up
                    
                    return {
                        "success": True,
                        "playwright_available": True,
                        "test_file_size": file_size,
                        "configuration": {
                            "page_size": "8.5in x 11in (US Letter)",
                            "margins": "0.6in all sides",
                            "scale": "0.85 (15% reduction for better fit)",
                            "background": "Enabled",
                            "headers_footers": "Disabled"
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": "Test PDF was not created"
                    }
                    
        except ImportError:
            return {
                "success": False,
                "playwright_available": False,
                "error": "Playwright not installed"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

if __name__ == "__main__":
    # Test the exporter
    import tempfile
    
    with tempfile.TemporaryDirectory() as temp_dir:
        exporter = OptimalPDFExporter(temp_dir)
        test_result = exporter.test_configuration()
        
        print("🧪 PDF Exporter Test Results:")
        if test_result["success"]:
            print("✅ Configuration test passed!")
            print(f"   Test file size: {test_result['test_file_size']:,} bytes")
            print("📋 Configuration:")
            for key, value in test_result["configuration"].items():
                print(f"   • {key}: {value}")
        else:
            print(f"❌ Configuration test failed: {test_result['error']}") 