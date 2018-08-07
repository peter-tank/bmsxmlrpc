import os
import re
import sys

from setuptools import setup, find_packages
# from server.version import softwareVersion as serverVersion

py_version = sys.version_info[:2]
if py_version < (2, 7):
    raise RuntimeError('Unsupported Python version. Python 2.7.4+ required')

# if serverVersion < (0, 6):
#     raise RuntimeError('Unsupported PyBitmessage version. PyBitmessage 0.6+ required')

here = os.path.abspath(os.path.dirname(__file__))
NAME = 'bmsxmlrpc'
with open(os.path.join(here, 'README.rst')) as readme:
    README = readme.read()
with open(os.path.join(here, 'CHANGES.rst')) as changes:
    CHANGES = changes.read()

with open(os.path.join(here, NAME, '__init__.py')) as version:
    VERSION = re.compile(r".*__version__ = '(.*?)'",
                         re.S).match(version.read()).group(1)


requires = []
# requires = ['serverVersion >= 0.6.0']
#if py_version < (3, 4):
#    requires.append('server')


setup(name=NAME,
      version=VERSION,
      description='XML-RPC API client for PyBitmessage',
      long_description=README + '\n\n' +  CHANGES,
      license='MIT',
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Environment :: Web Environment',
          "Topic :: Internet",
          "Topic :: Security :: Cryptography",
          "Topic :: Software Development :: Libraries :: Python Modules",
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License'
          "Operating System :: OS Independent",
          ],
      author='peter-tank',
      author_email='gfwtank@gmail.com',
      url='https://github.com/peter-tank/bmsxmlrpc',
      keywords='PyBitmessage xml-rpc rpc api',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      scripts=['bmsxmlrpc/client.py', 'bmsxmlrpc/socks.py'],
      test_suite='{}.tests'.format(NAME),
      install_requires=requires
      )
