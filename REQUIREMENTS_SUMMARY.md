# 📋 Requirements Summary

## What You Need to Run Resume Vision MCP

### System Requirements
- **macOS** (tested and optimized for)
- **Python 3.8+**
- **Cursor IDE** with MCP support

### Dependencies (Auto-installed by setup.sh)

**System Dependencies:**
```bash
brew install --cask libreoffice          # Document conversion
brew install cairo pango gdk-pixbuf      # PDF generation
brew install libffi gobject-introspection
```

**Python Dependencies:**
```bash
pip install mcp>=1.0.0                   # MCP framework
pip install PyMuPDF>=1.23.0              # PDF processing
pip install python-docx>=1.1.0           # DOCX handling
pip install Pillow>=10.0.0               # Image processing
pip install weasyprint>=60.0             # HTML to PDF
pip install beautifulsoup4>=4.12.0       # HTML parsing
pip install lxml>=4.9.0                  # XML/HTML parser
```

### Quick Setup Commands

**Option 1: Automated (Recommended)**
```bash
git clone <repository-url>
cd resume-vision-mcp
./setup.sh
```

**Option 2: Manual**
```bash
# Install system deps
brew install --cask libreoffice
brew install cairo pango gdk-pixbuf libffi gobject-introspection

# Setup Python
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure Cursor MCP (add to ~/.cursor/mcp.json)
{
  "mcpServers": {
    "resume-vision": {
      "command": "/path/to/resume-vision-mcp/.venv/bin/python",
      "args": ["/path/to/resume-vision-mcp/src/resume_vision_final.py"],
      "cwd": "/path/to/resume-vision-mcp"
    }
  }
}
```

### Usage Requirements

**Input Files Supported:**
- `.docx` - Microsoft Word documents
- `.pdf` - PDF files  
- `.png`, `.jpg`, `.jpeg` - Image files
- Any format LibreOffice can handle

**Workspace:**
- Automatically creates `resume_workspace/` directory
- Needs write permissions in project directory

**MCP Integration:**
- Cursor IDE with MCP support
- Restart Cursor after config changes
- Server should appear green in MCP settings

### No External APIs Required ✅
- No OpenAI/Anthropic API keys needed
- Uses Claude through Cursor conversation
- Fully self-contained workflow

---

**That's it! Everything else is handled automatically.** 🚀 