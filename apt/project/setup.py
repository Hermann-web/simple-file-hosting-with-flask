import os
from pathlib import Path
from typing import List
from setuptools import setup, find_packages

SRC_FOLDER = "../../src"

def find_data_files(folders:List[os.PathLike], src:os.PathLike):
    
    src_folder = Path(src).resolve()
    
    # Check if the source directory exists
    if not src_folder.exists() or not src_folder.is_dir():
        raise FileNotFoundError(f"Source directory '{src}' does not exist.")
    
    data_files = []
    
    for folder in folders:
        folder_path = src_folder / folder
        
        # Check if the specified folder exists
        if not folder_path.exists() or not folder_path.is_dir():
            raise FileNotFoundError(f"Folder '{folder}' within source directory '{src_folder}' does not exist.")
        
        print(f"listing data files from {folder_path} ...")

        for file_path in folder_path.glob("**/*"):
            if not file_path.is_file(): continue
            relative_path = file_path.relative_to(src_folder)
            data_files.append((str(relative_path.parent), [str(file_path)]))
                
    return data_files

setup(
    name="flask-file-share",
    version="0.1.1",
    description="Flask-based file sharing with web interface, API, and CLI app",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="hermann-web",
    author_email="hermannagossou6@gmail.com",
    url="https://flask-file-share.readthedocs.io",
    license="MIT",
    packages=find_packages(SRC_FOLDER),
    package_dir={"": SRC_FOLDER},
    include_package_data=True,
    data_files = find_data_files(folders=["flask_file_share/static", "flask_file_share/templates"], src=SRC_FOLDER),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Framework :: Flask",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=["flask", "file sharing", "web interface", "API", "CLI"],
    python_requires=">=3.8.1",
    install_requires=[
        "Flask>=2.0.1",#3.0.3
        "python-dotenv>=1.0.1",
        "python-slugify>=8.0.4",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "yapf>=0.40.2",
            "flake8>=7.0.0",
            "isort>=5.13.2",
            "mypy>=1.9.0",
            "pylint>=3.1.0",
            "pydeps>=1.12.20",
        ],
        "buildthedocs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=2.0.0",
            "m2r2>=0.3.3.post2",
        ],
    },
    entry_points={
        "console_scripts": [
            "ffs-app=flask_file_share.app:main",
            "ffs-cli=flask_file_share.cli:main",
            "ffs=flask_file_share.main:main",
        ]
    },
)
