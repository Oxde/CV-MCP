#!/usr/bin/env python3
"""
AI Editor - Cursor-Friendly HTML Editing Helper
==============================================
Helps prepare HTML editing instructions for manual conversation with Claude.
No external API calls - leverages existing conversation flow.
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, Optional, Any, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIEditor:
    """
    🎯 Cursor-Friendly HTML Editing Helper
    
    Prepares editing instructions and processes Claude's responses.
    No API calls needed - uses natural conversation flow.
    """
    
    def __init__(self, output_dir: str = "output/html"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"🎯 AIEditor initialized: Cursor-friendly mode → {self.output_dir}")
    
    def prepare_editing_instructions(self, html_content: str, instructions: str, output_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Prepare HTML editing instructions for manual conversation with Claude
        
        Args:
            html_content: Original HTML content or file path
            instructions: Natural language editing instructions
            output_name: Optional output filename
            
        Returns:
            Instructions and context for manual editing
        """
        # Load HTML content if path provided
        if html_content.endswith('.html') and Path(html_content).exists():
            html_path = Path(html_content)
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
        else:
            html_path = None
        
        # Analyze current HTML
        analysis = self.analyze_html_structure(html_content)
        
        # Generate output filename
        if not output_name:
            output_name = f"edited_resume_{self._generate_timestamp()}"
        
        output_path = self.output_dir / f"{output_name}.html"
        
        # Create editing prompt
        editing_prompt = self._create_editing_prompt(html_content, instructions)
        
        logger.info(f"🔄 Editing instructions prepared: {instructions[:50]}...")
        
        return {
            "original_html_path": str(html_path) if html_path else "provided_content",
            "output_path": str(output_path),
            "instructions": instructions,
            "editing_prompt": editing_prompt,
            "html_analysis": analysis,
            "ready_for_editing": True,
            "html_preview": html_content[:500] + "..." if len(html_content) > 500 else html_content
        }
    
    def process_edited_html(self, edited_html: str, output_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Process HTML that was edited by Claude in conversation
        
        Args:
            edited_html: Edited HTML content from Claude
            output_name: Optional output filename
            
        Returns:
            Results and validation of edited HTML
        """
        # Clean HTML content
        edited_html = self._clean_html_content(edited_html)
        
        # Generate output filename
        if not output_name:
            output_name = f"claude_edited_{self._generate_timestamp()}"
        
        output_path = self.output_dir / f"{output_name}.html"
        
        # Save edited HTML
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(edited_html)
        
        # Validate and analyze
        validation = self.validate_edited_html(edited_html)
        analysis = self.analyze_html_structure(edited_html)
        
        logger.info(f"✅ Edited HTML processed and saved: {output_path}")
        
        return {
            "edited_html_path": str(output_path),
            "validation": validation,
            "analysis": analysis,
            "ready_for_next_step": True
        }
    
    def prepare_job_optimization(self, html_content: str, job_description: str, output_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Prepare job optimization instructions for manual conversation
        
        Args:
            html_content: Original HTML content or file path
            job_description: Target job description
            output_name: Optional output filename
            
        Returns:
            Job optimization instructions for Claude
        """
        optimization_instructions = f"""
Optimize this resume for the following job posting:

{job_description}

OPTIMIZATION TASKS:
1. Add relevant keywords naturally throughout the content
2. Highlight matching skills and experience prominently
3. Rewrite job descriptions to better align with requirements
4. Adjust section order to emphasize relevant experience first
5. Enhance achievements with quantifiable results where possible
6. Ensure all job requirements are addressed if candidate has the experience
7. Improve action verbs and professional language
8. Make matching skills more prominent

Keep the original formatting and styling intact while improving content relevance and impact.
"""
        
        return self.prepare_editing_instructions(html_content, optimization_instructions, output_name)
    
    def prepare_layout_redesign(self, html_content: str, new_style: str, output_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Prepare layout redesign instructions for manual conversation
        
        Args:
            html_content: Original HTML content or file path  
            new_style: Target design style
            output_name: Optional output filename
            
        Returns:
            Layout redesign instructions for Claude
        """
        style_descriptions = {
            "modern": "Clean, contemporary design with plenty of whitespace, sans-serif fonts, and subtle color accents",
            "classic": "Traditional, conservative layout with serif fonts, formal styling, and professional appearance",
            "creative": "Bold, artistic design with creative use of colors, typography, and visual elements",
            "minimal": "Ultra-clean design with maximum whitespace, minimal colors, and focus on typography",
            "professional": "Business-appropriate design with balanced layout, professional colors, and clear hierarchy",
            "tech": "Modern tech-focused design with monospace accents, clean lines, and developer-friendly styling"
        }
        
        style_desc = style_descriptions.get(new_style, "professional and modern")
        
        redesign_instructions = f"""
Completely redesign this resume with a {new_style} layout style:

DESIGN REQUIREMENTS:
1. Preserve ALL original content text exactly
2. Apply {new_style} design principles: {style_desc}
3. Update colors, fonts, and spacing to match {new_style} aesthetic
4. Reorganize sections for better visual flow and hierarchy
5. Add appropriate styling elements for {new_style} theme
6. Ensure mobile responsiveness is maintained
7. Keep professional appearance suitable for job applications
8. Use inline CSS for all styling

STYLE GUIDELINES FOR {new_style.upper()}:
{self._get_style_guidelines(new_style)}

Create a fresh, {new_style} design while keeping all content intact and maintaining professional standards.
"""
        
        return self.prepare_editing_instructions(html_content, redesign_instructions, output_name)
    
    def _get_style_guidelines(self, style: str) -> str:
        """Get specific style guidelines for different design themes"""
        guidelines = {
            "modern": """
- Use sans-serif fonts (Arial, Helvetica, or similar)
- Implement clean color scheme (whites, grays, one accent color)
- Add plenty of whitespace between sections
- Use subtle shadows or borders for visual separation
- Implement modern typography hierarchy
            """,
            "classic": """
- Use serif fonts (Times New Roman, Georgia, or similar)
- Stick to traditional colors (black, navy, dark gray)
- Use formal section headers and layout
- Implement traditional spacing and margins
- Keep conservative, business-appropriate styling
            """,
            "creative": """
- Use interesting font combinations (but maintain readability)
- Implement creative color palette (2-3 complementary colors)
- Add visual elements like colored sections or creative headers
- Use asymmetrical layouts where appropriate
- Balance creativity with professionalism
            """,
            "minimal": """
- Use simple, clean fonts (minimal font variety)
- Stick to monochromatic or very limited color palette
- Maximize whitespace throughout
- Remove all unnecessary visual elements
- Focus on typography and content hierarchy
            """,
            "professional": """
- Use professional font combinations
- Implement business-appropriate color scheme
- Balance visual interest with conservative styling
- Use clear section divisions and hierarchy
- Maintain ATS-friendly structure
            """,
            "tech": """
- Use modern fonts with monospace accents for technical terms
- Implement tech-friendly color scheme (blues, grays, black)
- Add subtle tech-inspired visual elements
- Use clean, code-like structure and spacing
- Highlight technical skills prominently
            """
        }
        
        return guidelines.get(style, guidelines["professional"])
    
    def _create_editing_prompt(self, html_content: str, instructions: str) -> str:
        """Create comprehensive editing prompt for Claude"""
        return f"""
You are an expert HTML resume editor. Please edit this HTML resume according to the provided instructions.

EDITING INSTRUCTIONS:
{instructions}

EDITING GUIDELINES:
1. Preserve HTML structure and validity
2. Maintain responsive design principles  
3. Keep styling consistent and professional
4. Ensure all changes improve the resume quality
5. Return complete, valid HTML document
6. Use inline CSS for all styling
7. Do not add explanations or comments in the response

CURRENT HTML RESUME:
{html_content}

Please return the complete edited HTML document with all requested changes applied.
"""
    
    def _clean_html_content(self, html_content: str) -> str:
        """Clean HTML content from Claude response"""
        # Remove markdown code blocks if present
        if "```html" in html_content:
            start = html_content.find("```html") + 7
            end = html_content.find("```", start)
            if end != -1:
                html_content = html_content[start:end].strip()
        elif "```" in html_content and "<html" in html_content:
            start = html_content.find("```") + 3
            end = html_content.rfind("```")
            if end != -1:
                html_content = html_content[start:end].strip()
        
        # Ensure HTML starts properly
        html_content = html_content.strip()
        if not html_content.startswith(("<!DOCTYPE", "<html")):
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
    
    def analyze_html_structure(self, html_content: str) -> Dict[str, Any]:
        """Analyze HTML structure for editing insights"""
        try:
            # Basic HTML analysis
            analysis = {
                "length": len(html_content),
                "lines": html_content.count('\n'),
                "has_styling": "<style>" in html_content or "style=" in html_content,
                "sections": self._extract_sections(html_content),
                "word_count": len(self._extract_text(html_content).split()),
                "images": html_content.count('<img'),
                "links": html_content.count('<a'),
                "tables": html_content.count('<table'),
                "lists": html_content.count('<ul') + html_content.count('<ol')
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"HTML analysis failed: {e}")
            return {"error": str(e)}
    
    def _extract_sections(self, html_content: str) -> List[str]:
        """Extract section headings from HTML"""
        import re
        headings = re.findall(r'<h[1-6][^>]*>([^<]+)</h[1-6]>', html_content, re.IGNORECASE)
        return [h.strip() for h in headings]
    
    def _extract_text(self, html_content: str) -> str:
        """Extract plain text from HTML"""
        import re
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', html_content)
        # Clean whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def validate_edited_html(self, html_content: str) -> Dict[str, Any]:
        """Validate edited HTML for quality"""
        validation = {
            "valid": True,
            "issues": [],
            "quality_score": 0,
            "warnings": []
        }
        
        # Check HTML structure
        required_tags = ["<!DOCTYPE", "<html", "<head", "<body"]
        for tag in required_tags:
            if tag.lower() not in html_content.lower():
                validation["valid"] = False
                validation["issues"].append(f"Missing {tag}")
        
        # Check for common issues
        if len(html_content) < 1000:
            validation["warnings"].append("HTML content seems short")
        
        if not ("<style>" in html_content or "style=" in html_content):
            validation["warnings"].append("No CSS styling detected")
        
        if html_content.count('<h') < 2:
            validation["warnings"].append("Few section headings found")
        
        # Calculate quality score (0-100)
        score = 100
        score -= len(validation["issues"]) * 15
        score -= len(validation["warnings"]) * 5
        
        if len(html_content) < 1000:
            score -= 10
        if not ("<style>" in html_content or "style=" in html_content):
            score -= 10
        if html_content.count('<h') < 2:
            score -= 10
        
        validation["quality_score"] = max(0, score)
        
        return validation
    
    def get_editing_tips(self) -> List[str]:
        """Get general tips for HTML resume editing"""
        return [
            "Always preserve original content when redesigning",
            "Use inline CSS for maximum compatibility",
            "Ensure mobile responsiveness with proper viewport settings",
            "Keep professional appearance for job applications",
            "Use semantic HTML elements for better structure",
            "Optimize for both screen viewing and printing",
            "Test accessibility with proper heading hierarchy",
            "Include relevant keywords naturally in content",
            "Quantify achievements with numbers when possible",
            "Use action verbs to describe experiences"
        ] 