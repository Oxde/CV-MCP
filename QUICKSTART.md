# 🚀 Quick Start Guide

Get Resume Vision MCP up and running in 5 minutes!

## One-Command Setup (macOS)

```bash
git clone <repository-url>
cd JobKiller
chmod +x setup.sh
./setup.sh
```

This will:
- ✅ Install all dependencies (LibreOffice, Python packages)
- ✅ Create virtual environment
- ✅ Generate MCP configuration
- ✅ Test the installation

## Manual Setup

### 1. Prerequisites
```bash
# Install LibreOffice
brew install --cask libreoffice

# Install PDF dependencies  
brew install cairo pango gdk-pixbuf libffi gobject-introspection
```

### 2. Python Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Cursor MCP
Add to `~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "resume-vision": {
      "command": "/path/to/JobKiller/.venv/bin/python",
      "args": ["/path/to/JobKiller/src/resume_vision_final.py"],
      "cwd": "/path/to/JobKiller"
    }
  }
}
```

### 4. Restart Cursor
Check MCP settings - "resume-vision" should be green ✅

## First Use

### Upload & Convert
```
@upload_and_screenshot file_path="/path/to/resume.docx"
```

### Complete Workflow
```
@start_resume_workflow file_path="/path/to/resume.docx" workflow_name="job_application"
```

### Check Status
```
@get_workflow_status
```

## Common Commands

| Action | Command |
|--------|---------|
| Convert document | `@upload_and_screenshot file_path="resume.pdf"` |
| Get vision instructions | `@prepare_for_vision_analysis screenshot_path="path"` |
| Process Claude HTML | `@process_claude_html html_content="<html>..."` |
| Check status | `@get_workflow_status` |
| Full workflow | `@start_resume_workflow file_path="resume.docx"` |

## Troubleshooting

**Server appears red/yellow?**
- Check Python path in MCP config
- Restart Cursor after config changes

**LibreOffice errors?**
- Verify: `libreoffice --version`
- Reinstall: `brew reinstall --cask libreoffice`

**Permission errors?**
- Check workspace directory is writable
- Ensure project directory permissions

## Need Help?

- 📖 See [README.md](README.md) for detailed documentation
- 🔧 See [MCP_TROUBLESHOOTING_GUIDE.md](MCP_TROUBLESHOOTING_GUIDE.md) for common issues
- 🎯 Test with: `@get_workflow_status`

---

**Ready in 5 minutes! 🎯** 