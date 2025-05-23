# Resume Vision MCP Server 🎯

**AI-Powered Resume Processing Workflow for Cursor IDE**

Transform any resume document (DOCX, PDF, images) into editable HTML replicas using AI vision analysis, then export to professional PDFs. Fully integrated with Cursor's MCP (Model Context Protocol) for seamless AI-assisted editing.

## ✨ Features

- 📄 **Universal Document Support**: DOCX, PDF, images → High-quality screenshots
- 🔍 **AI Vision Analysis**: Claude vision integration for pixel-perfect HTML replication  
- ✏️ **Smart Editing**: AI-powered content and styling improvements
- 📝 **Template Management**: Save and reuse professional resume templates
- 📑 **PDF Export**: Generate print-ready PDFs from edited HTML
- 🚀 **Cursor Integration**: Native MCP tools for seamless workflow in Cursor IDE

## 🏗️ Architecture

```
Document (DOCX/PDF/Image) 
    ↓ [DocumentConverter]
Screenshot (High-quality PNG)
    ↓ [VisionReplicator + Claude]
HTML Replica (Pixel-perfect)
    ↓ [AIEditor]
Enhanced HTML (Improved content/styling)
    ↓ [PDFExporter]
Professional PDF (Print-ready)
```

## 📦 Installation

### Prerequisites

**Required:**
- Python 3.8+
- Cursor IDE
- LibreOffice (for DOCX conversion)

**macOS Setup:**
```bash
# Install LibreOffice
brew install --cask libreoffice

# Install system dependencies for PDF generation
brew install cairo pango gdk-pixbuf libffi gobject-introspection
```

### Project Setup

1. **Clone and Setup:**
```bash
git clone <repository-url>
cd resume-vision-mcp
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure MCP in Cursor:**
Add to your `~/.cursor/mcp.json`:
```json
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

3. **Verify Installation:**
Restart Cursor and check MCP settings - the "resume-vision" server should appear green.

## 🚀 Usage

### Quick Start

1. **Upload Document:**
```
@upload_and_screenshot file_path="/path/to/resume.docx"
```

2. **Prepare for Vision Analysis:**
```
@prepare_for_vision_analysis screenshot_path="generated_path"
```

3. **Upload Screenshot to Claude** and ask for HTML replica

4. **Process Claude's Response:**
```
@process_claude_html html_content="<html>...</html>"
```

### Complete Workflow

**One-command workflow:**
```
@start_resume_workflow file_path="/path/to/resume.docx" workflow_name="my_resume"
```

**Manual step-by-step workflow:**
1. `@upload_and_screenshot` - Convert document to screenshot
2. `@prepare_for_vision_analysis` - Get Claude instructions  
3. Upload screenshot to Claude and get HTML replica
4. `@process_claude_html` - Save and validate HTML
5. `@edit_with_ai` - Enhance content/styling (optional)
6. `@export_to_pdf` - Generate final PDF

### Available MCP Tools

| Tool | Purpose |
|------|---------|
| `upload_and_screenshot` | Convert any document to high-quality screenshot |
| `prepare_for_vision_analysis` | Prepare Claude vision analysis with instructions |
| `process_claude_html` | Process and validate Claude's HTML response |
| `get_workflow_status` | Check server status and progress |
| `start_resume_workflow` | Complete automated workflow |
| `clear_component_cache` | Reload components (development) |

## 📁 Project Structure

```
resume-vision-mcp/
├── src/                          # Core application code
│   ├── resume_vision_final.py    # Main MCP server
│   ├── document_converter.py     # Document → Screenshot conversion
│   ├── vision_replicator.py      # Claude vision integration
│   ├── ai_editor.py              # AI-powered editing
│   ├── template_manager.py       # Template system
│   ├── pdf_exporter.py           # HTML → PDF export
│   └── utils/                    # Utility functions
├── resume_workspace/             # Working directory (auto-created)
│   ├── screenshots/              # Generated screenshots
│   ├── html/                     # HTML replicas
│   ├── templates/                # Saved templates
│   ├── pdf/                      # Final PDFs
│   └── temp/                     # Temporary files
├── original_docs/                # Source documents
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🔧 Configuration

### Environment Variables
- `WORKSPACE_DIR`: Custom workspace directory (default: `./resume_workspace`)
- `LOG_LEVEL`: Logging level (default: `INFO`)

### MCP Configuration
The server automatically configures itself with:
- Explicit workspace paths to avoid permission issues
- Lazy component loading for optimal performance
- Comprehensive error handling and recovery

## 🛠️ Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Formatting
```bash
black src/
flake8 src/
```

### Adding New Components
1. Create module in `src/`
2. Add to lazy loading in `get_component()` function
3. Add MCP tool wrapper if needed

## ❌ Troubleshooting

### Common Issues

**"MCP server appears yellow/red in Cursor"**
- Check Python path in MCP config
- Verify virtual environment activation
- Check server logs in Cursor MCP settings

**"LibreOffice conversion failed"**
- Ensure LibreOffice is installed: `brew install --cask libreoffice`
- Check if LibreOffice is accessible from command line: `libreoffice --version`

**"PDF generation failed"**
- Install system dependencies: `brew install cairo pango gdk-pixbuf`
- Check WeasyPrint installation: `python -c "import weasyprint; print('OK')"`

**"Permission denied errors"**
- Check workspace directory permissions
- Ensure project directory is writable

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python src/resume_vision_final.py
```

## 📝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit Pull Request

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- Built for [Cursor IDE](https://cursor.sh) with MCP integration
- Uses [Claude](https://claude.ai) for AI vision analysis
- Document processing powered by PyMuPDF and LibreOffice
- PDF generation via WeasyPrint

---

**Ready to transform your resume workflow! 🚀** 