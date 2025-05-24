#!/usr/bin/env python3
"""
Resume Vision MCP Server - Final Working Version
================================================
Uses lazy loading and explicit workspace paths to avoid all issues
"""

import logging
import importlib
from pathlib import Path
from typing import Optional, Dict, Any, List
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastMCP server
mcp = FastMCP("resume-vision", 
              description="MCP server for CV/resume editing workflow. "
                          "Upload documents → AI vision analysis → HTML editing → PDF export. "
                          "Works with Cursor conversation flow - no external API keys needed!")

# Set explicit project directory (avoid any path resolution issues)
PROJECT_DIR = Path("/Users/nikmarf/JobKiller")
WORKSPACE_DIR = PROJECT_DIR / "resume_workspace"

logger.info("🎯 Resume Vision MCP initialized with lazy loading and explicit paths")

# Component cache and session tracking
_component_cache = {}
current_session = {
    "last_screenshot": None,
    "last_html": None,
    "last_template": None,
    "workflow_step": "start"
}

def ensure_workspace():
    """Ensure workspace directories exist"""
    try:
        WORKSPACE_DIR.mkdir(exist_ok=True)
        (WORKSPACE_DIR / "screenshots").mkdir(exist_ok=True)
        (WORKSPACE_DIR / "html").mkdir(exist_ok=True)
        (WORKSPACE_DIR / "templates").mkdir(exist_ok=True)
        (WORKSPACE_DIR / "pdf").mkdir(exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"❌ Failed to create workspace: {e}")
        return False

def get_component(component_name: str):
    """Lazy load components only when needed"""
    if component_name in _component_cache:
        return _component_cache[component_name]
    
    try:
        # Ensure workspace exists first
        if not ensure_workspace():
            raise Exception("Failed to create workspace directories")
        
        if component_name == "document_converter":
            module = importlib.import_module("document_converter")
            # Force reload to pick up any code changes
            importlib.reload(module)
            component = module.DocumentConverter(output_dir=str(WORKSPACE_DIR / "screenshots"))
            _component_cache[component_name] = component
            logger.info("✅ DocumentConverter loaded (with reload)")
            return component
            
        elif component_name == "vision_replicator":
            module = importlib.import_module("vision_replicator")
            component = module.VisionReplicator(output_dir=str(WORKSPACE_DIR / "html"))
            _component_cache[component_name] = component
            logger.info("✅ VisionReplicator loaded")
            return component
            
        elif component_name == "template_manager":
            module = importlib.import_module("template_manager")
            component = module.TemplateManager(templates_dir=str(WORKSPACE_DIR / "templates"))
            _component_cache[component_name] = component
            logger.info("✅ TemplateManager loaded")
            return component
            
        elif component_name == "ai_editor":
            module = importlib.import_module("ai_editor")
            component = module.AIEditor(output_dir=str(WORKSPACE_DIR / "html"))
            _component_cache[component_name] = component
            logger.info("✅ AIEditor loaded")
            return component
            
        elif component_name == "pdf_exporter":
            module = importlib.import_module("pdf_exporter")
            component = module.PDFExporter(output_dir=str(WORKSPACE_DIR / "pdf"))
            _component_cache[component_name] = component
            logger.info("✅ PDFExporter loaded")
            return component
            
    except Exception as e:
        logger.error(f"❌ Failed to load {component_name}: {e}")
        _component_cache[component_name] = None
        return None
    
    return None

# Resource for getting vision prompt
@mcp.resource("resume://vision-prompt")
def get_vision_prompt() -> str:
    """Get the recommended prompt for Claude vision analysis."""
    vision_replicator = get_component("vision_replicator")
    if vision_replicator:
        return vision_replicator.get_analysis_prompt()
    return "Vision replicator not available"

# Document Processing Tools
@mcp.tool()
def upload_and_screenshot(file_path: str, output_name: Optional[str] = None) -> Dict[str, Any]:
    """Convert uploaded document (DOCX, PDF, image) to high-quality screenshot for analysis."""
    document_converter = get_component("document_converter")
    if not document_converter:
        return {
            "success": False,
            "error": "DocumentConverter component failed to initialize. Check server logs."
        }
    
    try:
        logger.info(f"📄 Converting document: {file_path}")
        
        screenshot_path = document_converter.convert_to_screenshot(file_path, output_name)
        
        current_session["last_screenshot"] = screenshot_path
        current_session["workflow_step"] = "screenshot_ready"
        
        return {
            "success": True,
            "screenshot_path": screenshot_path,
            "message": f"✅ Document converted to screenshot: {Path(screenshot_path).name}",
            "next_step": "Use @prepare_for_vision_analysis to get Claude instructions"
        }
        
    except Exception as e:
        logger.error(f"❌ Document conversion failed: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def prepare_for_vision_analysis(screenshot_path: str, output_name: Optional[str] = None) -> Dict[str, Any]:
    """Prepare screenshot for manual vision analysis by Claude with instructions."""
    vision_replicator = get_component("vision_replicator")
    if not vision_replicator:
        return {
            "success": False,
            "error": "VisionReplicator component failed to initialize. Check server logs."
        }
    
    try:
        logger.info(f"🔄 Preparing vision analysis: {screenshot_path}")
        
        result = vision_replicator.prepare_for_analysis(screenshot_path, output_name)
        current_session["workflow_step"] = "ready_for_vision"
        
        return {
            "success": True,
            "instructions": result["instructions"],
            "image_info": result["image_info"],
            "output_path": result["output_path"],
            "message": "🎯 Ready for Claude vision analysis",
            "next_steps": [
                "1. Upload the screenshot to Claude conversation",
                "2. Use the vision analysis prompt (available as resource)",
                "3. Copy Claude's HTML response",
                "4. Use @process_claude_html with the HTML content"
            ]
        }
        
    except Exception as e:
        logger.error(f"❌ Vision preparation failed: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def process_claude_html(html_content: str, output_name: Optional[str] = None) -> Dict[str, Any]:
    """Process and save HTML replica created by Claude from vision analysis."""
    vision_replicator = get_component("vision_replicator")
    if not vision_replicator:
        return {
            "success": False,
            "error": "VisionReplicator component failed to initialize. Check server logs."
        }
    
    try:
        logger.info("🔄 Processing Claude's HTML response")
        
        result = vision_replicator.process_claude_response(html_content, output_name)
        
        current_session["last_html"] = result["html_path"]
        current_session["workflow_step"] = "html_ready"
        
        return {
            "success": True,
            "html_path": result["html_path"],
            "validation": result["validation"],
            "message": f"✅ HTML processed and saved: {Path(result['html_path']).name}",
            "next_options": [
                "@save_as_template - Save as reusable template",
                "@prepare_html_editing - Edit content or styling",
                "@export_to_pdf - Create final PDF"
            ]
        }
    
    except Exception as e:
        logger.error(f"❌ HTML processing failed: {e}")
        return {"success": False, "error": str(e)}

# Workflow and status tools
@mcp.tool()
def get_workflow_status() -> Dict[str, Any]:
    """Get current workflow status and next suggested steps."""
    component_status = {}
    for comp_name in ["document_converter", "vision_replicator", "template_manager", "ai_editor", "pdf_exporter"]:
        if comp_name in _component_cache:
            component_status[comp_name] = "✅ loaded" if _component_cache[comp_name] else "❌ failed"
        else:
            component_status[comp_name] = "⏳ not loaded"
    
    return {
        "success": True,
        "current_session": current_session,
        "workflow_step": current_session["workflow_step"],
        "workspace": str(WORKSPACE_DIR),
        "project_directory": str(PROJECT_DIR),
        "components_status": component_status,
        "message": "🎯 Resume Vision MCP is operational with lazy loading"
    }

@mcp.tool()
def start_resume_workflow(file_path: str, workflow_name: Optional[str] = None) -> Dict[str, Any]:
    """Start complete resume editing workflow from document upload."""
    try:
        logger.info(f"🚀 Starting resume workflow: {file_path}")
        
        # Step 1: Convert to screenshot
        screenshot_result = upload_and_screenshot(file_path)
        if not screenshot_result["success"]:
            return screenshot_result
        
        # Step 2: Prepare for vision analysis
        vision_result = prepare_for_vision_analysis(screenshot_result["screenshot_path"])
        if not vision_result["success"]:
            return vision_result
        
        current_session["workflow_step"] = "workflow_started"
        current_session["workflow_name"] = workflow_name or f"workflow_{_get_timestamp()}"
        
        return {
            "success": True,
            "screenshot_path": screenshot_result["screenshot_path"],
            "instructions": vision_result["instructions"],
            "workflow_name": current_session["workflow_name"],
            "message": "🚀 Resume workflow started successfully",
            "next_steps": vision_result["next_steps"]
        }
        
    except Exception as e:
        logger.error(f"❌ Workflow start failed: {e}")
        return {"success": False, "error": str(e)}

# Helper functions
def _get_timestamp() -> str:
    """Get timestamp for unique names."""
    from datetime import datetime
    return datetime.now().strftime("%Y%m%d_%H%M%S")

# Development/Debug tools
@mcp.tool()
def export_to_pdf(html_file_path: str, output_name: Optional[str] = None) -> Dict[str, Any]:
    """Export HTML resume to PDF using automated generation."""
    pdf_exporter = get_component("pdf_exporter")
    if not pdf_exporter:
        return {
            "success": False,
            "error": "PDFExporter component failed to initialize. Check server logs."
        }
    
    try:
        logger.info(f"📄 Exporting to PDF: {html_file_path}")
        
        result = pdf_exporter.convert_html_to_pdf(html_file_path, output_name, "professional")
        
        # Check if result is a file path (successful) or instructions (fallback)
        if result.endswith('.pdf') and Path(result).exists():
            current_session["last_pdf"] = result
            return {
                "success": True,
                "pdf_path": result,
                "message": f"✅ PDF exported successfully: {Path(result).name}",
                "file_size_kb": round(Path(result).stat().st_size / 1024, 1)
            }
        else:
            # Fallback method - return instructions
            return {
                "success": True,
                "method": "browser_fallback",
                "instructions": result,
                "message": "📄 PDF ready via browser method - follow instructions to complete"
            }
        
    except Exception as e:
        logger.error(f"❌ PDF export failed: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def save_as_template(html_file_path: str, template_name: str, description: Optional[str] = None) -> Dict[str, Any]:
    """Save the current HTML resume as a reusable template."""
    template_manager = get_component("template_manager")
    if not template_manager:
        return {
            "success": False,
            "error": "TemplateManager component failed to initialize. Check server logs."
        }
    
    try:
        logger.info(f"💾 Saving template: {template_name}")
        
        template_path = template_manager.save_as_template(html_file_path, template_name, description or "")
        current_session["last_template"] = template_path
        
        return {
            "success": True,
            "template_path": template_path,
            "template_name": template_name,
            "message": f"✅ Template saved: {template_name}",
            "description": description
        }
        
    except Exception as e:
        logger.error(f"❌ Template save failed: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def clear_component_cache() -> Dict[str, Any]:
    """Clear the component cache to force reload of all components (for development)."""
    global _component_cache
    old_cache = _component_cache.copy()
    _component_cache.clear()
    
    return {
        "success": True,
        "message": "🔄 Component cache cleared",
        "cleared_components": list(old_cache.keys()),
        "cache_size": len(old_cache)
    }

if __name__ == "__main__":
    try:
        logger.info("🚀 Starting Resume Vision MCP Server...")
        mcp.run()
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"💥 Server crashed: {e}")
        import traceback
        traceback.print_exc()
        raise 