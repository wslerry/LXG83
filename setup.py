try:
    import os
    import sys
    if os.path.isdir(r"C:\Program Files (x86)\ArcGIS\Bin"):
        sys.path.append(r"C:\Program Files (x86)\ArcGIS\Bin")
    else:
        sys.exit("LXG83 requires ArcMAP 9.3 to be installed")
except IOError:
    sys.exit()
from setuptools import setup, find_packages
import LXG83


package_data = {
    '': ['*.prj', '*.XML']
}

setup(
    name='LXG83',
    version=str(LXG83.__version__),
    author='Lerry William',
    author_email="lerryws@sains.com.my",
    description='Data migration application for ArcMap 8.3/9.3',
    long_description="""
    LXG83 make it easier to migrate SDE/MDB/GDB to a new FileGeodatabase (GDB).
    """,
    packages=find_packages(),
    package_data=package_data,
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Python Software Foundation License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.5",
        "Topic :: Scientific/Engineering :: GIS"
        "Topic :: Software Development :: Arcgis 9.3",
        "Topic :: Software Development :: Libraries :: Python Modules"
    )
)
