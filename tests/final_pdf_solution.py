#!/usr/bin/env python3
"""
Final PDF generation solution using the best settings we discovered.
This can be integrated into the MCP server.
"""

import time
from pathlib import Path
from playwright.sync_api import sync_playwright

def generate_optimal_pdf(html_file_path: str, output_pdf_path: str) -> bool:
    """
    Generate PDF using the optimal Playwright configuration discovered through testing.
    
    Args:
        html_file_path: Path to the HTML file to convert
        output_pdf_path: Path where the PDF should be saved
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        html_file = Path(html_file_path)
        output_file = Path(output_pdf_path)
        
        if not html_file.exists():
            print(f"❌ HTML file not found: {html_file}")
            return False
        
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"🔄 Generating PDF...")
        print(f"📄 Input:  {html_file}")
        print(f"📁 Output: {output_file}")
        
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            
            # Read HTML content
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Set content and wait for rendering
            page.set_content(html_content, wait_until='networkidle')
            
            # Optimal PDF configuration (discovered through testing)
            pdf_options = {
                'width': '8.5in',       # US Letter width
                'height': '11in',       # US Letter height  
                'margin': {
                    'top': '0.6in',     # Tight but professional margins
                    'right': '0.6in',
                    'bottom': '0.6in',
                    'left': '0.6in'
                },
                'print_background': True,  # Include background colors/images
                'scale': 0.85              # Scale down slightly to fit more content
            }
            
            # Generate PDF
            page.pdf(path=str(output_file), **pdf_options)
            browser.close()
        
        if output_file.exists():
            file_size = output_file.stat().st_size
            print(f"✅ PDF generated successfully!")
            print(f"   File size: {file_size:,} bytes")
            print(f"   Location: {output_file}")
            return True
        else:
            print(f"❌ Failed to generate PDF")
            return False
            
    except Exception as e:
        print(f"❌ Error generating PDF: {str(e)}")
        return False

def test_final_solution():
    """Test the final solution with both original and compact HTML."""
    test_files = [
        ("Template1.html", "Template1_final.pdf"),
        ("Template1_compact.html", "Template1_compact_final.pdf")
    ]
    
    print("🧪 Testing final PDF generation solution")
    print("=" * 60)
    
    results = []
    
    for html_filename, pdf_filename in test_files:
        html_path = Path(__file__).parent / html_filename
        pdf_path = Path(__file__).parent / pdf_filename
        
        print(f"\n📄 Testing: {html_filename}")
        start_time = time.time()
        
        success = generate_optimal_pdf(str(html_path), str(pdf_path))
        
        end_time = time.time()
        
        if success:
            results.append((html_filename, pdf_filename, True, end_time - start_time))
        else:
            results.append((html_filename, pdf_filename, False, 0))
    
    # Summary
    print("\n" + "=" * 60)
    print("🏁 FINAL RESULTS")
    print("=" * 60)
    
    for html_file, pdf_file, success, duration in results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        if success:
            pdf_path = Path(__file__).parent / pdf_file
            file_size = pdf_path.stat().st_size if pdf_path.exists() else 0
            print(f"{status} - {html_file}")
            print(f"   Output: {pdf_file}")
            print(f"   Time: {duration:.2f}s")
            print(f"   Size: {file_size:,} bytes")
        else:
            print(f"{status} - {html_file}")
    
    print(f"\n📂 Check the '{Path(__file__).parent}' directory for final PDF files")
    print("🎯 Use the compact version for best space utilization!")

if __name__ == "__main__":
    test_final_solution() 