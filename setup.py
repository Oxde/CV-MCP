#!/usr/bin/env python3
"""
Setup script for Resume Vision MCP - Cursor-Friendly Edition
===========================================================
Simple installation and dependency management.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Read requirements
requirements = []
with open('requirements.txt') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            requirements.append(line)

setup(
    name="resume-vision-mcp",
    version="1.0.0",
    author="Resume Vision Team",
    author_email="team@resumevision.ai",
    description="Fast & Simple CV/Resume Editing with AI Vision - Cursor-Friendly Edition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/JobKiller",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "resume-vision=mcp_server:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="resume cv editing pdf mcp cursor ai vision",
    project_urls={
        "Bug Reports": "https://github.com/your-username/JobKiller/issues",
        "Source": "https://github.com/your-username/JobKiller",
        "Documentation": "https://github.com/your-username/JobKiller/blob/main/README.md",
    },
) 