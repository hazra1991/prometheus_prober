import os

from pypi_upload_prober import __version__
from setuptools import find_packages, setup


current = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(current, "README.md"), 'r') as fd:
    LONG_DESCRIPTION = fd.read()

with open(os.path.join(current, "requirements.txt"), 'r') as fd:
    DEPENDENCIES = fd.read().strip().split('\n')

setup(
    name="pypi-upload-prober",
    version=__version__,
    description='pypi upload prober for calculating matrices',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://gitlab.aws.site.gs.com/dx/py-eng/pypi-upload-prober',
    install_requires=DEPENDENCIES,
    packages=find_packages(
        exclude=["tests*", "LOGS"]
    ),
    package_data={
        '': ["*.md", "requirements.txt"],
        'pypi_upload_prober': ["prober/conf/PROJECT_SETTINGS.json"]
    },
    # include_package_data=True

)