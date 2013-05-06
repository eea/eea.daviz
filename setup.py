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
          "Framework :: Zope2",
          "Framework :: Zope3",
          "Framework :: Plone",
          "Framework :: Plone :: 4.0",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Programming Language :: Zope",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "License :: OSI Approved :: Mozilla Public License 1.0 (MPL)",
        ],
      keywords=('eea daviz data visualization exhibit googlecharts '
                'sparql rdf zope plone'),
      author='European Environment Agency',
      author_email="webadmin@eea.europa.eu",
      url='http://eea.github.com/docs/eea.daviz',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['eea'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'eea.app.visualization > 6.9',
          'eea.forms >= 5.2',
          'eea.sparql >= 2.4',
          'eea.exhibit > 6.9',
          'eea.googlecharts > 6.9',
          'zc.dict',
          'Products.DataGridField',
      ],
      extras_require={
          'full': [
              'eea.relations >= 5.0',
              'eea.cache >= 4.0',
              'eea.depiction >= 5.0',
              ],
          'test': [
              'plone.app.testing',
          ]
      },

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
