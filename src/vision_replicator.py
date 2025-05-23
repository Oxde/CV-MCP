#!/usr/bin/env python3
"""
Vision Replicator - Cursor-Friendly Image Preparation
====================================================
Prepares document screenshots for manual analysis by Claude in Cursor.
No external API calls - leverages existing conversation flow.
"""

import os
import json
from pathlib import Path
from typing import Dict, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VisionReplicator:
    """
    🎯 Cursor-Friendly Vision Helper
    
    Prepares screenshots for manual analysis by Claude in conversation.
    No API calls needed - uses natural conversation flow.
    """
    
    def __init__(self, output_dir: str = "output/html"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"🎯 VisionReplicator initialized: Cursor-friendly mode → {self.output_dir}")
    
    def prepare_for_analysis(self, image_path: str, output_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Prepare screenshot for manual analysis by Claude
        
        Args:
            image_path: Path to document screenshot
            output_name: Optional output filename for future HTML
            
        Returns:
            Instructions and info for manual process
        """
        image_path = Path(image_path)
        
        if not image_path.exists():
            raise FileNotFoundError(f"Screenshot not found: {image_path}")
        
        # Get image info
        image_info = self.get_image_info(str(image_path))
        
        # Prepare output filename
        if not output_name:
            output_name = f"{image_path.stem}_replica"
        
        output_path = self.output_dir / f"{output_name}.html"
        
        # Generate instructions for user
        instructions = self._generate_analysis_instructions(image_path, output_path)
        
        logger.info(f"🔄 Image prepared for analysis: {image_path.name}")
        
        return {
            "image_path": str(image_path),
            "image_info": image_info,
            "output_path": str(output_path),
            "instructions": instructions,
            "ready_for_analysis": True
        }
    
    def process_claude_response(self, html_content: str, output_name: Optional[str] = None) -> str:
        """
        Process HTML response from Claude conversation
        
        Args:
            html_content: HTML content from Claude's analysis
            output_name: Optional output filename
            
        Returns:
            Path to saved HTML file
        """
        # Clean HTML content (remove markdown if present)
        html_content = self._clean_html_content(html_content)
        
        # Generate output filename
        if not output_name:
            output_name = f"claude_replica_{self._generate_timestamp()}"
        
        output_path = self.output_dir / f"{output_name}.html"
        
        # Save HTML file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Validate HTML
        validation = self.validate_html(html_content)
        
        logger.info(f"✅ Claude's HTML processed and saved: {output_path}")
        
        return {
            "html_path": str(output_path),
            "validation": validation,
            "ready_for_next_step": True
        }
    
    def _generate_analysis_instructions(self, image_path: Path, output_path: Path) -> str:
        """Generate instructions for manual analysis"""
        return f"""
🎯 READY FOR CLAUDE ANALYSIS

📸 **Screenshot prepared:** {image_path.name}
📍 **Location:** {image_path}
💾 **Will save to:** {output_path}

🔄 **NEXT STEPS:**
1. Upload the screenshot to this Claude conversation
2. Ask: "Create a pixel-perfect HTML replica of this resume"
3. Copy Claude's HTML response (entire HTML document)
4. Use: @process_claude_response html_content="<html>..." output_name="{image_path.stem}"

💡 **Prompt suggestion:**
"Please analyze this resume screenshot and create an exact HTML replica that matches:
- All visual elements: fonts, sizes, spacing, colors, alignment
- Complete content preservation
- Professional responsive design
- Inline CSS for styling
- Print-optimized layout

Return only the complete HTML document."
"""
    
    def _clean_html_content(self, html_content: str) -> str:
        """Clean HTML content from Claude response"""
        # Remove markdown code blocks if present
        if "```html" in html_content:
            # Extract HTML from markdown code block
            start = html_content.find("```html") + 7
            end = html_content.find("```", start)
            if end != -1:
                html_content = html_content[start:end].strip()
        elif "```" in html_content and "<html" in html_content:
            # Extract HTML from generic code block
            start = html_content.find("```") + 3
            end = html_content.rfind("```")
            if end != -1:
                html_content = html_content[start:end].strip()
        
        # Ensure HTML starts with doctype or html tag
        html_content = html_content.strip()
        if not html_content.startswith(("<!DOCTYPE", "<html")):
            # Look for HTML content within the response
            html_start = html_content.find("<!DOCTYPE")
            if html_start == -1:
                html_start = html_content.find("<html")
            if html_start != -1:
                html_content = html_content[html_start:]
        
        return html_content
    
    def _generate_timestamp(self) -> str:
        """Generate timestamp for unique filenames"""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def validate_html(self, html_content: str) -> Dict[str, Any]:
        """Basic validation of HTML content"""
        validation = {
            "valid": True,
            "issues": [],
            "stats": {}
        }
        
        # Check for essential HTML structure
        required_tags = ["<!DOCTYPE", "<html", "<head", "<body"]
        for tag in required_tags:
            if tag.lower() not in html_content.lower():
                validation["valid"] = False
                validation["issues"].append(f"Missing {tag}")
        
        # Basic stats
        validation["stats"] = {
            "length": len(html_content),
            "lines": html_content.count('\n'),
            "has_css": "<style>" in html_content or "style=" in html_content,
            "has_content": len(html_content.strip()) > 1000,
            "word_count": len(html_content.split())
        }
        
        # Quality checks
        if validation["stats"]["length"] < 1000:
            validation["issues"].append("HTML content seems too short")
        if not validation["stats"]["has_css"]:
            validation["issues"].append("No CSS styling detected")
        
        return validation
    
    def extract_content_structure(self, html_content: str) -> Dict[str, Any]:
        """Extract structured content from HTML for analysis"""
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            structure = {
                "title": soup.title.string if soup.title else "Resume",
                "headings": [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3', 'h4'])],
                "paragraphs": len(soup.find_all('p')),
                "lists": len(soup.find_all(['ul', 'ol'])),
                "tables": len(soup.find_all('table')),
                "sections": len(soup.find_all(['section', 'div'])),
                "text_content": soup.get_text()[:300] + "..." if len(soup.get_text()) > 300 else soup.get_text()
            }
            
            return structure
            
        except ImportError:
            logger.warning("BeautifulSoup not available for content analysis")
            return {"error": "BeautifulSoup required for detailed content extraction"}
        except Exception as e:
            logger.error(f"Content extraction failed: {e}")
            return {"error": str(e)}
    
    def get_image_info(self, image_path: str) -> Dict[str, Any]:
        """Get information about the input image"""
        try:
            from PIL import Image
            
            image_path = Path(image_path)
            image = Image.open(image_path)
            
            return {
                "filename": image_path.name,
                "size": image.size,
                "width": image.size[0],
                "height": image.size[1],
                "mode": image.mode,
                "format": image.format,
                "file_size_mb": round(image_path.stat().st_size / (1024 * 1024), 2),
                "file_size_kb": round(image_path.stat().st_size / 1024, 1)
            }
        except Exception as e:
            logger.error(f"Failed to get image info: {e}")
            return {
                "filename": Path(image_path).name,
                "error": str(e)
            }
    
    def get_analysis_prompt(self) -> str:
        """Get the recommended prompt for Claude analysis"""
        return """
Please analyze this resume screenshot and create a pixel-perfect HTML replica that matches:

🎯 EXACT REQUIREMENTS:
- Match every visual element: fonts, sizes, spacing, colors, alignment
- Preserve exact layout structure and positioning  
- Include all text content word-for-word
- Replicate formatting: bold, italics, bullet points, tables
- Match margins, padding, line heights precisely
- Use modern HTML5 and inline CSS for exact styling

📝 OUTPUT FORMAT:
Generate complete, valid HTML document with:
- <!DOCTYPE html> declaration
- Full HTML structure (<html>, <head>, <body>)
- Inline CSS for exact styling (no external files)
- Responsive design principles
- Professional fonts and spacing
- Print-optimized CSS

🎨 STYLING GUIDELINES:
- Use web-safe fonts that match the original
- Precise margins and padding measurements
- Exact color values for text and backgrounds
- Professional spacing between sections
- Clean, semantic HTML structure

📱 RESPONSIVE DESIGN:
- Mobile-friendly layout
- Proper viewport meta tag
- Scalable typography
- Flexible containers

Return ONLY the complete HTML document - no explanations, no markdown, just pure HTML that perfectly replicates the original document.
""" 