from setuptools import setup, find_packages

setup(
    name="bank_scraper",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "selenium",
        "beautifulsoup4",
    ],
)
