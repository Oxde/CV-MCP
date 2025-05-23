#!/bin/bash

# Resume Vision MCP Server Setup Script
# =====================================

set -e  # Exit on any error

echo "🎯 Resume Vision MCP Server Setup"
echo "=================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${RED}❌ This setup script is designed for macOS. Please install dependencies manually.${NC}"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python version
echo -e "${YELLOW}🔍 Checking Python version...${NC}"
if command_exists python3; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    echo "✅ Python $PYTHON_VERSION found"
    
    # Check if version is 3.8+
    if python3 -c 'import sys; exit(0 if sys.version_info >= (3, 8) else 1)'; then
        echo "✅ Python version is compatible"
    else
        echo -e "${RED}❌ Python 3.8+ required. Current: $PYTHON_VERSION${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.8+ first.${NC}"
    exit 1
fi

# Check/Install Homebrew
echo -e "${YELLOW}🔍 Checking Homebrew...${NC}"
if command_exists brew; then
    echo "✅ Homebrew found"
else
    echo "📦 Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install LibreOffice
echo -e "${YELLOW}📦 Installing LibreOffice...${NC}"
if brew list --cask libreoffice &>/dev/null; then
    echo "✅ LibreOffice already installed"
else
    echo "📦 Installing LibreOffice via Homebrew..."
    brew install --cask libreoffice
fi

# Install system dependencies for PDF generation
echo -e "${YELLOW}📦 Installing PDF generation dependencies...${NC}"
DEPS=("cairo" "pango" "gdk-pixbuf" "libffi" "gobject-introspection")
for dep in "${DEPS[@]}"; do
    if brew list "$dep" &>/dev/null; then
        echo "✅ $dep already installed"
    else
        echo "📦 Installing $dep..."
        brew install "$dep"
    fi
done

# Create virtual environment
echo -e "${YELLOW}🐍 Setting up Python virtual environment...${NC}"
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Install Python dependencies
echo -e "${YELLOW}📦 Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Create workspace directory
echo -e "${YELLOW}📁 Creating workspace directory...${NC}"
mkdir -p resume_workspace/{screenshots,html,templates,pdf,temp}
echo "✅ Workspace directories created"

# Get current directory for MCP config
CURRENT_DIR=$(pwd)
PYTHON_PATH="$CURRENT_DIR/.venv/bin/python"
SCRIPT_PATH="$CURRENT_DIR/src/resume_vision_final.py"

# Generate MCP configuration
echo -e "${YELLOW}⚙️  Generating MCP configuration...${NC}"
cat > mcp_config_example.json << EOF
{
  "mcpServers": {
    "resume-vision": {
      "command": "$PYTHON_PATH",
      "args": ["$SCRIPT_PATH"],
      "cwd": "$CURRENT_DIR"
    }
  }
}
EOF

echo "✅ MCP configuration generated: mcp_config_example.json"

# Test installation
echo -e "${YELLOW}🧪 Testing installation...${NC}"
if python src/resume_vision_final.py --help &>/dev/null; then
    echo "✅ MCP server can start successfully"
else
    echo -e "${RED}❌ MCP server test failed${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 Setup Complete!${NC}"
echo ""
echo "📋 Next Steps:"
echo "1. Copy the contents of mcp_config_example.json"
echo "2. Add to your ~/.cursor/mcp.json file:"
echo "   - If file doesn't exist, create it with the generated content"
echo "   - If file exists, add the 'resume-vision' server to the 'mcpServers' object"
echo "3. Restart Cursor IDE"
echo "4. Check MCP settings - 'resume-vision' should appear green"
echo ""
echo "🚀 Usage:"
echo "   @start_resume_workflow file_path=\"/path/to/resume.docx\""
echo ""
echo -e "${GREEN}Ready to transform your resume workflow! 🎯${NC}" 