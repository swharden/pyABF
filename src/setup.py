from setuptools import setup

# load the module to determine the version
#exec(open("pyabf/__init__.py").read())

__version__=open('pyabf/__init__.py').read().split("__version__")[1].split("'")[1]

setup(
    name='pyabf',
    version=__version__,
    author='Scott W Harden',
    author_email='SWHarden@gmail.com',
    packages=['pyabf'],
    url='http://github.com/swharden/pyABF',
    license='MIT License',
    platforms='any',
    description='Python library for reading files in Axon Binary Format (ABF)',
    long_description=open('README.rst').read(),
    install_requires=[	
       'matplotlib>=2.1.0',
       'numpy>=1.13.3',
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
    ]
)