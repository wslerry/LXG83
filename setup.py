from setuptools import setup
from LXG83 import app_version

setup(
    name='LXG83',
    version=app_version,
    author='Lerry William',
    description='Data migration application for ArcMap',
    # long_description="""
    # LXG83 make it easier to migrate SDE to file geodatabase.
    # """,
    packages=['LXG83',
              'LXG83.migrate',
              'LXG83.replicate',
              'LXG83.utils'
              ],
    package_data={'LXG83': ['README.md', 'assets/projection/BRSO_4.prj', 'assets/workspace/*.XML']},
    package_dir={'LXG83': ''},
    classifiers=(
        "Development Status :: 1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Python Software Foundation License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: GIS",
        "Topic :: Software Development :: Arcgis 9.3",
        "Topic :: Software Development :: Libraries :: Python Modules"
    )
)
