# -*- coding: utf-8 -*-
"""
Setup script for MIDI MCP Server.

Defines package metadata, dependencies, and installation configuration
for the MIDI MCP Server Python package.
"""
#
#   __author__ = "Chris Fogelklou"
#   __email__ = "chris.fogelklou@gmail.com"
#   __copyright__ = "Copyright 2025"
#   __license__ = "MIT"
#
#   (with lots of help from AI agents)
#

from setuptools import setup, find_packages
import os
import sys
from pathlib import Path

# Get the directory containing this file
here = Path(__file__).parent.absolute()

# Read the README file
readme_path = here / "README.md"
if readme_path.exists():
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = "MIDI MCP Server - MCP Server for MIDI operations and musical content creation"

# Read requirements from requirements.txt
requirements_path = here / "requirements.txt"
requirements = []
if requirements_path.exists():
    with open(requirements_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if line and not line.startswith("#"):
                # Remove inline comments
                if "#" in line:
                    line = line.split("#")[0].strip()
                # Skip conditional dependencies for now (can be enhanced later)
                if ";" not in line:
                    requirements.append(line)

# Development requirements (optional)
dev_requirements = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-mock>=3.11.0",
    "pytest-timeout>=2.1.0",
    "pytest-xdist>=3.3.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
    "mypy>=1.5.0",
    "pre-commit>=3.4.0",
]

# Documentation requirements (for future phases)
docs_requirements = ["sphinx>=7.0.0", "sphinx-rtd-theme>=1.3.0", "myst-parser>=2.0.0"]

# Import version from package
sys.path.insert(0, str(here / "src"))
try:
    from midi_mcp.core.version import (
        __version__,
        PACKAGE_NAME,
        PACKAGE_DESCRIPTION,
        PACKAGE_AUTHOR,
        PACKAGE_EMAIL,
        PACKAGE_URL,
    )
except ImportError:
    # Fallback if package is not yet installed
    __version__ = "0.1.0"
    PACKAGE_NAME = "midi-mcp"
    PACKAGE_DESCRIPTION = "MCP Server for MIDI operations and musical content creation"
    PACKAGE_AUTHOR = "Chris Fogelklou"
    PACKAGE_EMAIL = "chris.fogelklou@gmail.com"
    PACKAGE_URL = "https://github.com/chrisfogelklou/midi-mcp"

setup(
    name=PACKAGE_NAME,
    version=__version__,
    author=PACKAGE_AUTHOR,
    author_email=PACKAGE_EMAIL,
    description=PACKAGE_DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=PACKAGE_URL,
    # Package configuration
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    # Python version requirement
    python_requires=">=3.8",
    # Dependencies
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
        "docs": docs_requirements,
        "all": dev_requirements + docs_requirements,
    },
    # Entry points
    entry_points={
        "console_scripts": [
            "midi-mcp-server=midi_mcp.core.server:main",
            "midi-mcp=midi_mcp.core.server:main",
        ],
    },
    # Package metadata
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Sound/Audio :: MIDI",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",
        "Framework :: AsyncIO",
    ],
    keywords=[
        "midi",
        "mcp",
        "server",
        "music",
        "audio",
        "protocol",
        "ai",
        "assistant",
        "claude",
        "musical",
        "composition",
        "realtime",
    ],
    project_urls={
        "Bug Reports": f"{PACKAGE_URL}/issues",
        "Source": PACKAGE_URL,
        "Documentation": f"{PACKAGE_URL}/docs",
        "Changelog": f"{PACKAGE_URL}/blob/main/CHANGELOG.md",
    },
    # Additional metadata
    zip_safe=False,
    platforms=["any"],
)
