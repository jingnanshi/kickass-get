
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='kickass-get',
    version='0.2.4',
    description='A command-line interface for kat.cr (Kickass Torrents)',
    long_description=long_description,
    url='https://github.com/jingnanshi/kickass-get',
    author='Jingnan Shi',
    author_email='jshi@g.hmc.edu',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'Topic :: Terminals',
        'Topic :: System :: Networking',
        'Programming Language :: Python :: 2 :: Only',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License',
    ],
    keywords=['torrent', 'magnet', 'download', 'kickass', 'kat', 'client'],
    packages=find_packages(exclude=['tests']),
    install_requires=['colorama', 'termcolor', 'multiprocessing', 'beautifulsoup4', 'requests', 'argparse', 'tabulate', 'requests_cache'],

    entry_points={
        'console_scripts': [
            'kickass-get=kickass.kickass_parse:main',
        ],
    }
    # test_suite='tests'
)
