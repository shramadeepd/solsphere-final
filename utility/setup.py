#!/usr/bin/env python3
"""
Setup script for the System Utility
A cross-platform system health monitoring utility
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "System Utility - Cross-platform system health monitoring"

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="system-utility",
    version="1.0.0",
    description="Cross-platform system health monitoring utility",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="System Utility Team",
    author_email="admin@example.com",
    url="https://github.com/your-org/system-utility",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    entry_points={
        "console_scripts": [
            "system-utility=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="system monitoring health security compliance",
    project_urls={
        "Bug Reports": "https://github.com/your-org/system-utility/issues",
        "Source": "https://github.com/your-org/system-utility",
        "Documentation": "https://github.com/your-org/system-utility#readme",
    },
)
