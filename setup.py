from setuptools import setup, find_packages

setup(
    name="system",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0,<0.69.0",
        "uvicorn>=0.15.0,<0.16.0",
        "python-multipart>=0.0.5,<0.1.0",
        "pydantic>=1.8.0,<2.0.0",
        "pydantic-settings>=2.0.0",
        "sqlalchemy>=1.4.0",
    ],
)