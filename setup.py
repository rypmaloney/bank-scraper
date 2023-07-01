from setuptools import setup

setup(
    name="bank_scraper",
    version="1.0",
    packages=["bank_scraper"],
    install_requires=[
        "selenium",
        "beautifulsoup4",
    ],
)
