#!/usr/bin/env python3
"""
Template Manager - Save and Reuse AI-Generated HTML Templates
============================================================
Manages AI-generated HTML templates for reuse across different resumes.
Templates are user-saved HTML replicas that can be applied to new content.
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TemplateManager:
    """
    🎯 Manage AI-Generated HTML Templates
    
    Save successful AI-generated HTML replicas as reusable templates.
    Users can save, load, compare, and apply templates to new content.
    """
    
    def __init__(self, templates_dir: str = "templates"):
        self.templates_dir = Path(templates_dir)
        self.saved_templates_dir = self.templates_dir / "saved_templates"
        self.generated_dir = self.templates_dir / "generated"
        
        # Create directories
        self.saved_templates_dir.mkdir(parents=True, exist_ok=True)
        self.generated_dir.mkdir(parents=True, exist_ok=True)
        
        # Metadata file for template information
        self.metadata_file = self.saved_templates_dir / "templates_metadata.json"
        self.metadata = self._load_metadata()
        
        logger.info(f"🎯 TemplateManager initialized: {self.saved_templates_dir}")
    
    def save_as_template(self, html_file: str, template_name: str, description: str = "") -> str:
        """
        Save AI-generated HTML as reusable template
        
        Args:
            html_file: Path to HTML file to save as template
            template_name: Unique name for the template
            description: Optional description of the template
            
        Returns:
            Path to saved template
        """
        html_path = Path(html_file)
        
        if not html_path.exists():
            raise FileNotFoundError(f"HTML file not found: {html_file}")
        
        # Clean template name for filename
        clean_name = self._clean_template_name(template_name)
        template_path = self.saved_templates_dir / f"{clean_name}.html"
        
        # Check if template already exists
        if template_path.exists():
            raise FileExistsError(f"Template '{template_name}' already exists")
        
        # Copy HTML file to templates directory
        shutil.copy2(html_path, template_path)
        
        # Update metadata
        template_info = {
            "name": template_name,
            "filename": f"{clean_name}.html",
            "description": description,
            "created_date": datetime.now().isoformat(),
            "original_file": str(html_path),
            "file_size": template_path.stat().st_size,
            "preview": self._generate_preview(template_path)
        }
        
        self.metadata[clean_name] = template_info
        self._save_metadata()
        
        logger.info(f"✅ Template saved: '{template_name}' → {template_path}")
        return str(template_path)
    
    def load_template(self, template_name: str) -> str:
        """
        Load saved template HTML content
        
        Args:
            template_name: Name of template to load
            
        Returns:
            HTML content as string
        """
        clean_name = self._clean_template_name(template_name)
        template_path = self.saved_templates_dir / f"{clean_name}.html"
        
        if not template_path.exists():
            available = self.list_templates()
            raise FileNotFoundError(f"Template '{template_name}' not found. Available: {available}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        logger.info(f"✅ Template loaded: '{template_name}'")
        return content
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """Get list of all saved templates with metadata"""
        templates = []
        
        for template_id, info in self.metadata.items():
            template_path = self.saved_templates_dir / info["filename"]
            
            # Check if file still exists
            if template_path.exists():
                templates.append({
                    "id": template_id,
                    "name": info["name"],
                    "description": info["description"],
                    "created_date": info["created_date"],
                    "file_size_kb": round(info["file_size"] / 1024, 1),
                    "preview": info["preview"]
                })
        
        # Sort by creation date (newest first)
        templates.sort(key=lambda x: x["created_date"], reverse=True)
        
        return templates
    
    def delete_template(self, template_name: str) -> bool:
        """
        Delete saved template
        
        Args:
            template_name: Name of template to delete
            
        Returns:
            True if deleted successfully
        """
        clean_name = self._clean_template_name(template_name)
        template_path = self.saved_templates_dir / f"{clean_name}.html"
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template '{template_name}' not found")
        
        # Remove file and metadata
        template_path.unlink()
        if clean_name in self.metadata:
            del self.metadata[clean_name]
            self._save_metadata()
        
        logger.info(f"✅ Template deleted: '{template_name}'")
        return True
    
    def duplicate_template(self, source_name: str, new_name: str, description: str = "") -> str:
        """Create a copy of existing template with new name"""
        source_content = self.load_template(source_name)
        
        # Create temporary file and save as new template
        temp_path = self.generated_dir / f"temp_{new_name}.html"
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(source_content)
        
        try:
            new_template_path = self.save_as_template(str(temp_path), new_name, description)
            return new_template_path
        finally:
            # Clean up temp file
            if temp_path.exists():
                temp_path.unlink()
    
    def get_template_info(self, template_name: str) -> Dict[str, Any]:
        """Get detailed information about a template"""
        clean_name = self._clean_template_name(template_name)
        
        if clean_name not in self.metadata:
            raise KeyError(f"Template '{template_name}' not found")
        
        info = self.metadata[clean_name].copy()
        template_path = self.saved_templates_dir / info["filename"]
        
        # Add current file stats
        if template_path.exists():
            info["current_size"] = template_path.stat().st_size
            info["last_modified"] = datetime.fromtimestamp(
                template_path.stat().st_mtime
            ).isoformat()
        
        return info
    
    def export_template(self, template_name: str, export_path: str) -> str:
        """Export template to external location"""
        content = self.load_template(template_name)
        export_path = Path(export_path)
        
        with open(export_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"✅ Template exported: '{template_name}' → {export_path}")
        return str(export_path)
    
    def import_template(self, html_file: str, template_name: str, description: str = "") -> str:
        """Import external HTML file as template"""
        return self.save_as_template(html_file, template_name, description)
    
    def _clean_template_name(self, name: str) -> str:
        """Clean template name for use as filename"""
        # Remove invalid characters and spaces
        import re
        clean = re.sub(r'[^\w\-_]', '_', name.lower())
        clean = re.sub(r'_+', '_', clean)  # Multiple underscores → single
        return clean.strip('_')
    
    def _generate_preview(self, template_path: Path) -> Dict[str, Any]:
        """Generate preview information for template"""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract basic info for preview
            preview = {
                "title": self._extract_title(content),
                "word_count": len(content.split()),
                "has_styling": "<style>" in content or "style=" in content,
                "sections": self._count_sections(content),
                "snippet": self._extract_text_snippet(content)
            }
            
            return preview
            
        except Exception as e:
            logger.warning(f"Preview generation failed: {e}")
            return {"error": "Preview unavailable"}
    
    def _extract_title(self, html_content: str) -> str:
        """Extract title from HTML content"""
        # Try to find title tag
        import re
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
        if title_match:
            return title_match.group(1).strip()
        
        # Try to find first heading
        h1_match = re.search(r'<h1[^>]*>([^<]+)</h1>', html_content, re.IGNORECASE)
        if h1_match:
            return h1_match.group(1).strip()
        
        return "Resume Template"
    
    def _count_sections(self, html_content: str) -> int:
        """Count approximate number of sections"""
        import re
        headings = re.findall(r'<h[1-6][^>]*>', html_content, re.IGNORECASE)
        return len(headings)
    
    def _extract_text_snippet(self, html_content: str) -> str:
        """Extract text snippet for preview"""
        try:
            # Simple text extraction (could use BeautifulSoup for better results)
            import re
            # Remove HTML tags
            text = re.sub(r'<[^>]+>', ' ', html_content)
            # Clean whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            # Return first 200 characters
            return text[:200] + "..." if len(text) > 200 else text
        except:
            return "Preview unavailable"
    
    def _load_metadata(self) -> Dict[str, Any]:
        """Load templates metadata from file"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load metadata: {e}")
        
        return {}
    
    def _save_metadata(self) -> None:
        """Save templates metadata to file"""
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save metadata: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get template library statistics"""
        templates = self.list_templates()
        
        if not templates:
            return {"total_templates": 0}
        
        total_size = sum(t["file_size_kb"] for t in templates)
        
        return {
            "total_templates": len(templates),
            "total_size_kb": round(total_size, 1),
            "newest_template": templates[0]["name"] if templates else None,
            "oldest_template": templates[-1]["name"] if templates else None
        } 