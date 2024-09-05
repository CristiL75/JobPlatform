# setup.py
from setuptools import setup, find_packages

setup(
    name='JobPlatform',
    version='0.1',
    packages=find_packages(where='backend'),
    package_dir={'': 'backend'},
    install_requires=[
        # List your project dependencies here
    ],
    include_package_data=True,
    zip_safe=False,
)
