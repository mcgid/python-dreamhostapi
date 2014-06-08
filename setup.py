from setuptools import setup
from codecs import open # Following PyPUG advice; not neccessary in Python 3.x
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dreamhostapi',

    version='0.1.0',

    description='A Python wrapper around DreamHost\'s API',
    long_description=long_description,

    url='https://github.com/mcgid/python-dreamhostapi',

    author='mcgid',
    author_email='dan@mcgid.ca',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',

        # Untested on any other Python version
        'Programming Language :: Python :: 2.7',

        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    keywords='DreamHost API interaction wrapper',

    packages=['dreamhostapi'],

    install_requires=['requests'],
) 
