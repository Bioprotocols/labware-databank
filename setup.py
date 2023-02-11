import os
import re

from setuptools import setup, find_packages


REGEX_COMMENT = re.compile(r"[\s^]#(.*)")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

dir_path = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(dir_path, "VERSION"), "r") as version_file:
    version = str(version_file.readline()).strip()


def parse_requirements(filename):
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(filename, "rt") as filehandle:
        requirements = filehandle.readlines()[2:]
        return tuple(filter(None, (REGEX_COMMENT.sub("", line).strip() for line in requirements)))


setup(
    name="labop_labware_ontology",
    version=version,
    packages=find_packages(),
    include_package_data=True,
    author="mark doerr",
    author_email="mark.doerr@uni-greifswald.de",
    description="LabOP open ontology for scientific labware.",
    url="opensourcelab/labop-labware-ontology",
    install_requires=parse_requirements("requirements.txt"),
    extras_require={"tests": parse_requirements("requirements_dev.txt")},
)
