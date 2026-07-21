from setuptools import find_packages
from setuptools import setup

setup(
    name='soarm100_interfaces',
    version='0.1.0',
    packages=find_packages(
        include=('soarm100_interfaces', 'soarm100_interfaces.*')),
)
