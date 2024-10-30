from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in zfpl/__init__.py
from zfpl import __version__ as version

setup(
	name="zfpl",
	version=version,
	description="An app for manufacturing process including token etc",
	author="Atom Global",
	author_email="info@atom-global.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
