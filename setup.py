#!/usr/bin/env python3
"""
Setup script for Personal AI Agent System
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read version from VERSION file
version_file = Path(__file__).parent / "VERSION"
if version_file.exists():
    version = version_file.read_text().strip()
else:
    version = "0.1.0"

# Read long description from README
readme_file = Path(__file__).parent / "README.md"
if readme_file.exists():
    long_description = readme_file.read_text()
else:
    long_description = "Personal AI Agent System"

# Core dependencies
install_requires = [
    "anthropic>=0.40.0",
    "click>=8.1.0",
    "pydantic>=2.0.0",
    "python-dotenv>=1.0.0",
    "requests>=2.31.0",
]

# Development dependencies
dev_requires = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.7.0",
    "ruff>=0.0.280",
    "mypy>=1.4.0",
    "pre-commit>=3.3.0",
    "ipython>=8.14.0",
]

# Optional dependencies for different phases
extras_require = {
    "dev": dev_requires,
    "local": [
        "litellm>=1.50.0",
        "ollama>=0.4.0",
    ],
    "api": [
        "fastapi>=0.115.0",
        "uvicorn>=0.32.0",
    ],
    "memory": [
        "chromadb>=0.5.0",
        "sentence-transformers>=2.2.0",
    ],
    "scheduler": [
        "apscheduler>=3.10.0",
    ],
    "monitoring": [
        "prometheus-client>=0.18.0",
        "structlog>=23.1.0",
    ],
}

# Combine all extras
extras_require["all"] = sum(extras_require.values(), [])

setup(
    name="personal-ai-agent",
    version=version,
    description="A self-improving, privacy-focused AI agent orchestrator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/personal-ai-agent",
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    python_requires=">=3.11",
    install_requires=install_requires,
    extras_require=extras_require,
    entry_points={
        "console_scripts": [
            "agent=agent.cli.commands:cli",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="ai agent llm automation orchestration",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/personal-ai-agent/issues",
        "Source": "https://github.com/yourusername/personal-ai-agent",
        "Documentation": "https://github.com/yourusername/personal-ai-agent/docs",
    },
)
