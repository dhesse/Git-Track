from setuptools import setup, find_packages
import os

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "Git-Track",
    version = "0.1",
    packages = find_packages(exclude = "dist"),
    scripts = ['track.py', 'convert.py'],
    author = "Dirk Hesse",
    author_email = "herr.dirk.hesse@gmail.com",
    description = ("Minimal Bug Tracking For Git."),
    url = "http://github.com/dhesse/Git-Track",
    install_requires = ['gitpython>=0.3'],
    long_description = read('README'),
    license = "MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Software Development :: Bug Tracking",
        "Topic :: Software Development :: Version Control",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        ]
    )
