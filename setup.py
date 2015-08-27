import re

from codecs import open
from glob import glob
from setuptools import setup, find_packages

version = ''
with open('lib/nelmon/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

with open('HISTORY.rst', 'r', 'utf-8') as f:
    history = f.read()

long_description = readme + '\n\n' + history

config = {
    'name': 'nelmon',
    'package_dir': {'': 'lib'},
    'packages': find_packages('lib'),
    'version': version,
    'description': 'Monitoring Plugins for Nagios and compatible products',
    'long_description': long_description,
    'author': 'Patrick Ogenstad',
    'author_email': 'patrick@ogenstad.com',
    'license': 'Apache',
    'url': 'http://networklore.com/nelmon/',
    'install_requires': ['argparse', 'nelsnmp >= 0.2.1'],
    'scripts': glob('plugins/*'),
    'classifiers': ['Development Status :: 4 - Beta',
                    'Intended Audience :: Developers',
                    'Intended Audience :: System Administrators']
}

setup(**config)
