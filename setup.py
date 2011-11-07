""" Installer
"""
import os
from os.path import join
from setuptools import setup, find_packages

NAME = 'eea.daviz'
PATH = NAME.split('.') + ['version.txt']
VERSION = open(join(*PATH)).read().strip()

setup(name=NAME,
      version=VERSION,
      description="EEA DaViz",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='eea daviz data visualization',
      author='European Environment Agency',
      author_email="webadmin@eea europa eu",
      url='http://svn.eionet.europa.eu/projects/Zope/wiki/DaViz',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['eea'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'eea.exhibit',
          'p4a.z2utils',
          'collective.js.jqueryui',
          'rdflib',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
