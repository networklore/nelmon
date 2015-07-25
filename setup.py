import re

from codecs import open
from setuptools import setup

version = ''
with open('nelmon/__init__.py', 'r') as fd:
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
    'packages': ['nelmon'],
    'version': version,
    'description': 'Monitoring Plugins for Nagios and compatible products',
    'long_description': long_description,
    'author': 'Patrick Ogenstad',
    'author_email': 'patrick@ogenstad.com',
    'license': 'Apache',
    'url': 'http://networklore.com/nelmon/',
    'install_requires': ['nelsnmp >= 0.1.7'],
    'classifiers': ['Development Status :: 4 - Beta',
                    'Intended Audience :: Developers',
                    'Intended Audience :: System Administrators']
}

setup(**config)
