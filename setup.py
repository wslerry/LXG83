import setuptools
from distutils.core import setup, Extension
from distutils.command.build_py import build_py

fh = open('README.md', 'r')
long_description = fh.read()

setuptools.setup(
    name='LXG83',
    version='2.0.0',
    author='Lerry William Seling',
    description='Data migration application for ArcMap',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    packages=setuptools.find_packages(),
    package_data={'LXG83': ['README.md', 'assets/projection/*', 'assets/workspace/*']},
    classifiers=(
        'Programming Language :: Python :: 2.5',
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
    ),
    install_requires=[]
)
