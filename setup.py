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
      description=("EEA DaViz is a plone product which uses Exhibit and Google "
                   "Charts API to easily create data visualizations based "
                   "on data from csv/tsv, JSON, SPARQL endpoints and more."
                   ),
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='eea daviz data visualization exhibit googlecharts' \
               'sparql rdf zope plone',
      author='European Environment Agency',
      author_email="webadmin@eea.europa.eu",
      url='http://svn.eionet.europa.eu/projects/Zope/wiki/DaViz',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['eea'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'eea.app.visualization',
          'eea.forms',
          'eea.sparql',
          'eea.exhibit',
          'eea.googlecharts',

          ## Optional
          #eea.relations,
          #eea.cache,

      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
