import os
from setuptools import setup
from setuptools import find_packages
import sys

if sys.version_info[:2] < (3, 6):
    raise RuntimeError("Python version >= 3.6 required.")

# load the description
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.abspath(PATH_HERE+"/README.rst")) as f:
    long_description = f.read()

# standard pypi stuff
setup(
    name='pyabf',
    version='2.3.6',
    author='Scott W Harden',
    author_email='SWHarden@gmail.com',
    python_requires='>=3.6',
    packages=find_packages(),
    include_package_data=True,
    url='http://swharden.com/pyabf',
    license='MIT License',
    platforms='any',
    description='Python library for reading files in Axon Binary Format (ABF)',
    long_description=long_description,
    install_requires=[
        'matplotlib>=2.1.0',
        'numpy>=1.13.3',
        'pytest>=3.0.7',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    project_urls={
        'Bug Reports': 'https://github.com/swharden/pyABF/issues',
        'Source': 'https://github.com/swharden/pyABF',
        'Documentation': 'https://swharden.com/pyabf/tutorial',
    },
)
