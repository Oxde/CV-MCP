# MCP Server Troubleshooting Guide
**Complete Guide to Debugging and Fixing Common MCP Issues**

## 🎯 Overview

This guide covers the most common issues when developing MCP (Model Context Protocol) servers with FastMCP and Cursor, based on real troubleshooting experience.

## 🚨 Common Issues & Solutions

### 1. **Server Shows Yellow/Red in Cursor (Connection Closed)**

**Symptom:** 
- MCP server appears yellow or red in Cursor settings
- Logs show: `MCP error -32000: Connection closed`
- Server starts but immediately disconnects

**Root Causes & Solutions:**

#### A. Python Path Manipulation at Startup
```python
# ❌ PROBLEMATIC CODE - Breaks MCP communication
import sys
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))
```

**Why it breaks:** Modifying `sys.path` during server initialization interferes with Cursor's stdio pipe communication.

**✅ Solution:** Use relative imports or dynamic imports instead:
```python
# Option 1: Relative imports (if modules are in same directory)
from document_converter import DocumentConverter

# Option 2: Dynamic imports with importlib
import importlib
module = importlib.import_module("document_converter")
component = module.DocumentConverter()
```

#### B. Heavy Imports at Startup
```python
# ❌ PROBLEMATIC - All imports happen at startup
from document_converter import DocumentConverter
from vision_replicator import VisionReplicator
from template_manager import TemplateManager
from ai_editor import AIEditor
from pdf_exporter import PDFExporter

# All components initialized immediately
document_converter = DocumentConverter()
# ... etc
```

**Why it breaks:** Heavy imports and initializations at startup can cause the server to crash before it responds to Cursor.

**✅ Solution:** Use lazy loading:
```python
# Component cache
_component_cache = {}

def get_component(component_name: str):
    """Lazy load components only when needed"""
    if component_name in _component_cache:
        return _component_cache[component_name]
    
    try:
        if component_name == "document_converter":
            module = importlib.import_module("document_converter")
            component = module.DocumentConverter(output_dir="./workspace")
            _component_cache[component_name] = component
            return component
    except Exception as e:
        logger.error(f"Failed to load {component_name}: {e}")
        _component_cache[component_name] = None
        return None
```

### 2. **Read-Only File System Errors**

**Symptom:**
- `[Errno 30] Read-only file system: '/workspace_name'`
- Components fail to initialize

**Root Cause:** Path resolution issues causing directories to be created in root filesystem instead of project directory.

**❌ Problematic code:**
```python
# This resolves to root filesystem: /workspace_name
base_dir = Path("workspace_name").resolve()
```

**✅ Solution:** Use explicit project paths:
```python
# Option 1: Use current working directory
base_dir = Path.cwd() / "workspace_name"

# Option 2: Use explicit project path
PROJECT_DIR = Path("/Users/username/ProjectName")
WORKSPACE_DIR = PROJECT_DIR / "workspace_name"

def ensure_workspace():
    """Ensure workspace directories exist"""
    try:
        WORKSPACE_DIR.mkdir(exist_ok=True)
        (WORKSPACE_DIR / "subdirectory").mkdir(exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Failed to create workspace: {e}")
        return False
```

### 3. **FastMCP vs Standard MCP Issues**

**FastMCP Compatibility Issues:**
- Some FastMCP versions may have stdio communication issues
- Error: `anyio.BrokenResourceError` in stdio communication

**✅ Solution:** Test with minimal FastMCP server first:
```python
#!/usr/bin/env python3
import logging
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("test-server", description="Simple test server")

@mcp.tool()
def hello() -> str:
    """Simple hello test"""
    return "Hello from MCP! 🎯"

if __name__ == "__main__":
    try:
        logger.info("🚀 Starting test server...")
        mcp.run()
    except Exception as e:
        logger.error(f"💥 Server crashed: {e}")
        raise
```

### 4. **MCP Configuration Issues**

**Common config problems in `.cursor/mcp.json`:**

**❌ Problematic:**
```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["src/server.py"],
      "cwd": "/relative/path"
    }
  }
}
```

**✅ Best practices:**
```json
{
  "mcpServers": {
    "my-server": {
      "command": "/absolute/path/to/.venv/bin/python",
      "args": ["/absolute/path/to/project/src/server.py"],
      "cwd": "/absolute/path/to/project"
    }
  }
}
```

## 🔧 Debugging Process

### Step 1: Test Basic FastMCP
1. Create minimal server with just basic tools
2. Test if it appears green in Cursor
3. If it works, the issue is in your complex server

### Step 2: Isolate Import Issues
```python
@mcp.tool()
def test_imports() -> Dict[str, Any]:
    """Test importing modules individually"""
    results = {}
    modules = ["module1", "module2", "module3"]
    
    for module_name in modules:
        try:
            __import__(module_name)
            results[module_name] = "✅ OK"
        except Exception as e:
            results[module_name] = f"❌ Error: {e}"
    
    return {"import_results": results}
```

### Step 3: Test Component Creation
```python
@mcp.tool()
def test_component_creation(component_name: str) -> Dict[str, Any]:
    """Test creating specific components"""
    try:
        module = importlib.import_module(component_name)
        component = getattr(module, "ComponentClass")(params)
        return {"success": True, "message": f"✅ {component_name} created"}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

### Step 4: Check Logs
Monitor MCP logs in Cursor for specific error messages:
- Connection closed errors → Startup issues
- Import errors → Module/dependency problems  
- Permission errors → File system issues

## 🏗️ Best Practices Architecture

### Recommended Server Structure:
```python
#!/usr/bin/env python3
import logging
import importlib
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create server
mcp = FastMCP("server-name", description="Server description")

# Set explicit paths
PROJECT_DIR = Path("/absolute/path/to/project")
WORKSPACE_DIR = PROJECT_DIR / "workspace"

# Component cache for lazy loading
_component_cache = {}

def get_component(name: str):
    """Lazy load components"""
    if name not in _component_cache:
        try:
            module = importlib.import_module(name)
            component = module.ComponentClass(config)
            _component_cache[name] = component
        except Exception as e:
            logger.error(f"Failed to load {name}: {e}")
            _component_cache[name] = None
    return _component_cache[name]

@mcp.tool()
def tool_function() -> dict:
    """Tool that uses lazy-loaded components"""
    component = get_component("component_name")
    if not component:
        return {"success": False, "error": "Component failed to load"}
    
    # Use component...
    return {"success": True, "result": "..."}

if __name__ == "__main__":
    try:
        logger.info("🚀 Starting server...")
        mcp.run()
    except Exception as e:
        logger.error(f"💥 Server crashed: {e}")
        raise
```

## ✅ Pre-flight Checklist

Before deploying an MCP server:

- [ ] **No `sys.path` modifications** at startup
- [ ] **Use lazy loading** for heavy components  
- [ ] **Explicit absolute paths** for workspace
- [ ] **Test minimal version** first
- [ ] **Check file permissions** in target directories
- [ ] **Use proper error handling** to prevent crashes
- [ ] **Test each component** individually
- [ ] **Monitor MCP logs** during development

## 🎯 Success Indicators

Your MCP server is working correctly when:
- ✅ Shows **green** in Cursor MCP settings
- ✅ **Tools are visible** and callable
- ✅ **Components load on-demand** without crashing server
- ✅ **Proper error handling** keeps server running even if components fail
- ✅ **Workspace creates** in correct project directory

## 📚 Additional Resources

- [FastMCP Documentation](https://gofastmcp.com)
- [MCP Specification](https://modelcontextprotocol.io)
- [Cursor MCP Guide](https://docs.cursor.com/advanced/model-context-protocol)

---

**Created:** Based on real troubleshooting experience with FastMCP and Cursor integration.  
**Status:** Battle-tested solutions for common MCP development issues. 