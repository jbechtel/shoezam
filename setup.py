from setuptools import find_packages, setup

VERSION = "0.0.0"

REQUIRED_PACKAGES = []
with open("requirements.txt", "r") as reqs_txt_file:
    REQUIRED_PACKAGES = [line.strip() for line in reqs_txt_file]

REQUIRED_DEV_PACKAGES = []
with open("requirements-dev.txt", "r") as reqs_dev_txt_file:
    REQUIRED_DEV_PACKAGES = [line.strip() for line in reqs_dev_txt_file]

setup(
    name="shoezam", 
    version=VERSION,
    author="Jonathon Bechtel",
    description="Computer vision shoe comparison app",
    url="https://github.com/jbechtel/shoezam",
    packages=find_packages(),
    python_requires='==3.8.1',
)
