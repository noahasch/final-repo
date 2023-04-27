"This is a setup file."
from setuptools import setup

setup(
    name="pkg",
    version="0.0.1",
    description="final project",
    maintainer="Noah Asch",
    maintainer_email="nasch@andrew.cmu.edu",
    license="MIT",
    packages=["pkg"],
    scripts=[],
    entry_points={"console_scripts": ["papers = pkg.main:main"]},
    long_description="""OpenAlex based package""",
)
