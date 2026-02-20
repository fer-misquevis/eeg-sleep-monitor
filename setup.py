"""
Setup script for EEG Sleep Monitor
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="eeg-sleep-monitor",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Sistema de monitoramento em tempo real de sinais EEG para análise de sono",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seu-usuario/eeg-sleep-monitor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.109.0",
        "uvicorn[standard]>=0.27.0",
        "numpy>=1.26.3",
        "scipy>=1.12.0",
        "pylsl>=1.16.2",
        "python-multipart>=0.0.6",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
        "muse": [
            "muselsl>=2.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "eeg-monitor=src.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["static/*.html", "static/*.css", "static/*.js"],
    },
)
