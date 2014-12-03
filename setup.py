import os
import re

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
NAME = 'pyramid_aiorm'
with open(os.path.join(here, 'README.rst')) as readme:
    README = readme.read()
with open(os.path.join(here, 'CHANGES.rst')) as changes:
    CHANGES = changes.read()

with open(os.path.join(here, NAME, '__init__.py')) as version:
    VERSION = re.compile(r".*__version__ = '(.*?)'",
                         re.S).match(version.read()).group(1)


requires = ['pyramid', 'aiorm']


setup(name=NAME,
      version=VERSION,
      description='pyramid binding for aiorm',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        ],
      author='Guillaume Gauvrit',
      author_email='guillaume@gauvr.it',
      url='',
      keywords='pyramid aiorm orm',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      # test_suite=NAME,
      install_requires=requires,
      entry_points="""\
      [console_scripts]
      {pkg} = {pkg}.__main__:main
      """.format(pkg=NAME),
      )
