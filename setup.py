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
    description='Data migration application for ArcMap',
    long_description="""
    LXG83 make it easier to migrate SDE to file geodatabase.
    """,
    packages=find_packages(),
    package_data=package_data,
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
