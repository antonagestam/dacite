import sys

from setuptools import setup

if sys.version_info < (3, 7):
    requirements = ["dataclasses"]
else:
    requirements = []

setup(
    name="dacite",
    version="1.0.2",
    description="Simple creation of data classes from dictionaries.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Konrad Hałas",
    author_email="halas.konrad@gmail.com",
    url="https://github.com/konradhalas/dacite",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    keywords="dataclasses",
    packages=["dacite"],
    install_requires=requirements,
    extras_require={"dev": ["pytest>=4", "pytest-cov", "coveralls", "black", "mypy", "pylint"]},
)
