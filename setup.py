from setuptools import setup, find_packages

setup(
    name="tk-export",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "tk-export=tk_export.interactive:main",
        ],
    },
    author="vagueGM",
    author_email="",
    description="A tool to export data from Tavern Keeper",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vagueGM/tk-export",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 