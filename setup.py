from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="discordbotdash", 
version="1.2.2",
author="Sachin Raja",
author_email="sachinraja2349@gmail.com",
license="MIT",
description="A python package for testing/managing your discord.py bot in browser.",
long_description=long_description,
long_description_content_type="text/markdown",
url="https://github.com/xCloudzx/discordbotdash",
packages=find_packages(),
include_package_data=True,
classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
]
)