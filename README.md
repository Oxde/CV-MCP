# JobKiller - Resume Vision MCP Server 🚀

## Overview

**JobKiller** is a Model Context Protocol (MCP) server that provides an AI-powered resume editing workflow. Upload any document format, get AI vision analysis, and export professional PDFs with optimized settings.

## 🎯 Key Features

### ✅ Complete Resume Workflow
- **Document Upload**: Support for DOCX, PDF, and image formats
- **AI Vision Analysis**: Claude analyzes document structure and content
- **HTML Generation**: Creates editable HTML replicas
- **Template Management**: Save and reuse optimized templates
- **PDF Export**: Professional single-page PDFs with optimal settings

### 🔧 Optimized PDF Generation (V2)
Based on extensive testing of 6+ PDF generation methods, V2 uses the best configuration:
- **Single-page output**: Ensures resume fits on one page like the original
- **No headers/footers**: Clean output without unwanted timestamps or file paths
- **Perfect fonts**: Preserves original typography and spacing (~183KB files)
- **Playwright-powered**: Most reliable PDF generation method

## 🏗️ Architecture

### Current Versions
- **`resume_vision_v2.py`** - ✅ **CURRENT**: Optimized with FastMCP + enhanced PDF generation
- **`resume_vision_v1.py`** - Legacy: Original working version (backup)

### Core Components
- **`optimal_pdf_exporter.py`** - Optimized PDF generation with Playwright
- **`document_converter.py`** - Document to screenshot conversion
- **`vision_replicator.py`** - AI vision analysis coordination
- **`template_manager.py`** - Template storage and management
- **`ai_editor.py`** - Content editing capabilities
- **`pdf_exporter.py`** - Original PDF generation (fallback)

## 📦 Installation

1. **Clone and setup:**
   ```bash
   git clone https://github.com/yourusername/JobKiller.git
   cd JobKiller
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install mcp playwright
   playwright install chromium
   ```

3. **Configure MCP in Cursor:**
   Add to your `~/.cursor/mcp.json`:
   ```json
   {
     "mcpServers": {
       "resume-vision": {
         "command": "/path/to/JobKiller/.venv/bin/python",
         "args": ["/path/to/JobKiller/src/resume_vision_v2.py"],
         "cwd": "/path/to/JobKiller"
       }
     }
   }
   ```

4. **Restart Cursor** to load the MCP server

## 🛠️ Available Tools

### Primary Workflow
- **`upload_and_screenshot`** - Convert documents to high-quality screenshots
- **`prepare_for_vision_analysis`** - Get Claude analysis instructions
- **`process_claude_html`** - Process HTML from Claude's vision analysis
- **`export_to_pdf`** - Generate optimized PDFs

### Management Tools
- **`save_as_template`** - Save HTML as reusable template
- **`get_workflow_status`** - Check system status and component health
- **`start_resume_workflow`** - Begin complete editing workflow
- **`clear_component_cache`** - Development tool for reloading components

## 🧪 PDF Generation Journey

Our V2 includes extensively tested PDF optimization:

### Testing Results
| Method | File Size | Pages | Quality | Status |
|--------|-----------|-------|---------|---------|
| Chrome Headless | 208KB | ✅ | Good | ✅ Works |
| **Playwright (V2)** | **~183KB** | **✅** | **Excellent** | **✅ Optimal** |
| WeasyPrint | N/A | ❌ | Poor | ❌ Dependencies |
| wkhtmltopdf | N/A | ❌ | Layout issues | ❌ Failed |

### Optimal Configuration (V2)
```python
{
    'width': '8.5in',           # US Letter
    'height': '11in',
    'margin': {'top': '0.6in', 'right': '0.6in', 'bottom': '0.6in', 'left': '0.6in'},
    'print_background': True,    # Include styling
    'scale': 0.85,              # 15% reduction for better fit
    'display_header_footer': False  # No unwanted headers
}
```

## 🎯 Usage Example

```bash
# In Cursor with MCP enabled:
@upload_and_screenshot /path/to/resume.pdf
@prepare_for_vision_analysis /path/to/screenshot.png
# [Follow Claude vision analysis steps]
@process_claude_html "<html>...</html>"
@export_to_pdf /path/to/resume.html
```

## 📁 Project Structure

```
JobKiller/
├── src/
│   ├── resume_vision_v2.py         # 🚀 Current optimized version
│   ├── resume_vision_v1.py         # Legacy version (backup)
│   ├── optimal_pdf_exporter.py     # Optimized PDF generation
│   ├── document_converter.py       # Document processing
│   ├── vision_replicator.py        # AI vision coordination
│   ├── template_manager.py         # Template management
│   ├── ai_editor.py               # Content editing
│   └── pdf_exporter.py            # Original PDF export (fallback)
├── resume_workspace/
│   ├── templates/saved_templates/  # Optimized templates
│   ├── screenshots/               # Document screenshots
│   ├── html/                     # Generated HTML files
│   └── pdf/                      # Exported PDFs
├── README_OPTIMIZED_SOLUTION.md   # Detailed technical documentation
└── README.md                     # This file
```

## ✅ Success Metrics (V2)

- ✅ **Single-page output** (vs original 2-page problem)
- ✅ **No unwanted headers** (vs timestamp/path problem)
- ✅ **Optimal file size** (~183KB vs 208KB+ alternatives)
- ✅ **Professional quality** (fonts, spacing, layout preserved)
- ✅ **Reliable generation** (consistent results across documents)
- ✅ **FastMCP stability** (no more yellow MCP status)

## 🔬 Technical Details

### Why V2 is Better
1. **FastMCP Framework**: More stable than manual Server setup
2. **Lazy Loading**: Components load only when needed
3. **Graceful Fallback**: Falls back to original PDF exporter if optimized fails
4. **Comprehensive Testing**: Based on extensive multi-method testing

### PDF Quality Evolution
1. **Original Problem**: 2 pages, unwanted headers, poor layout
2. **V1**: Working but basic PDF generation
3. **V2**: Optimized single-page, professional quality, ~183KB files

## 🚀 Development

The project uses:
- **Python 3.8+** with async/await
- **MCP (Model Context Protocol)** for Cursor integration
- **FastMCP** for stable server framework
- **Playwright** for optimal PDF generation
- **Lazy loading** for component management

## 📄 License

MIT License - Feel free to use and modify for your resume editing needs!

---

**Result**: A production-ready MCP server that transforms resume editing with AI vision analysis and generates professional, single-page PDFs! 🎉 