from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in contact_grouping/__init__.py
from contact_grouping import __version__ as version

setup(
	name="contact_grouping",
	version=version,
	description="App for creating contact groups",
	author="Devershi",
	author_email="devershi.v@smartedgesolutions.co.uk",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
