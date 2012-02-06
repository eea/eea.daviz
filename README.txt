EEA Daviz product
=================
EEA DaViz is a plone product which uses Exhibit to lets you easily create web pages
with advanced text search and filtering functionalities (facets), with interactive maps,
timelines, and other visualizations like these examples can be seen
at  http://www.simile-widgets.org/exhibit.


Contents
========

.. contents::


Introduction
============

It is simply to use, needs no desktop application, everything is done
through the web by uploading an "excel file" and configure its visualisations.

See also initial project wiki page https://svn.eionet.europa.eu/projects/Zope/wiki/DaViz
for the reasoning behind this project.


Main features
=============

EEA Daviz generates different views and a customisable faceted search on CSV/TSV data
uploaded in a Plone site. Just upload a CSV file under a normal Plone file and
go to actions menu and click convert to exhibit view, the page will automatically
refresh to edit the Exhibit view

More details about how to use this package can be found at the following link:

  1. http://svn.eionet.europa.eu/projects/Zope/wiki/HowToDaviz


Installation
============

To install eea.daviz into the global Python environment (or a workingenv),
using a traditional Zope 2 instance, you can do this:

 * When you're reading this you have probably already run
   ``easy_install eea.daviz``. Find out how to install setuptools
   (and EasyInstall) here:
   http://peak.telecommunity.com/DevCenter/EasyInstall

 * If you are using Zope 2.9 (not 2.10), get `pythonproducts`_ and install it
   via::

       python setup.py install --home /path/to/instance

   into your Zope instance.

 * Create a file called ``eea.daviz-configure.zcml`` in the
   ``/path/to/instance/etc/package-includes`` directory.  The file
   should only contain this::

       <include package="eea.daviz" />

.. _pythonproducts: http://plone.org/products/pythonproducts


Alternatively, if you are using zc.buildout and the plone.recipe.zope2instance
recipe to manage your project, you can do this:

  * Add ``eea.daviz`` to the list of eggs to install, e.g.::

      [buildout]
      eggs = eea.daviz

  * Tell the plone.recipe.zope2instance recipe to install a ZCML slug::

      [instance]
      recipe = plone.recipe.zope2instance
      zcml = eea.daviz

  * Re-run buildout, e.g. with::

      $ ./bin/buildout

You can skip the ZCML slug if you are going to explicitly include the package
from another package's configure.zcml file.


Dependecies
===========

  1. Plone 4.x
  2. eea.exhibit
  3. p4a.z2utils
  4. collective.js.jqueryui
  5. rdflib


Live demo
=========

  1. http://www.simile-widgets.org/exhibit
  2. http://www.eea.europa.eu/data-and-maps/data/national-emissions-reported-to-the-unfccc-and-to-the-eu-greenhouse-gas-monitoring-mechanism-3/national-total-excluding-lulucf/ghg_v10_extract.csv


Source code
===========

Latest source code (Plone 4 compatible):
   https://svn.eionet.europa.eu/repositories/Zope/trunk/eea.daviz/trunk

Plone 2 and 3 compatible:
   https://svn.eionet.europa.eu/repositories/Zope/trunk/eea.daviz/branches/plone25


Copyright and license
=====================

The Initial Owner of the Original Code is European Environment Agency (EEA).
All Rights Reserved.

The EEA Daviz (the Original Code) is free software;
you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation;
either version 2 of the License, or (at your option) any later
version.

More details under docs/License.txt


Links
=====

  1. Simile Wiki - Exhibit 2.0: http://simile.mit.edu/wiki/Exhibit
  2. Simile widgets: http://www.simile-widgets.org/exhibit
  3. EEA Daviz howto: https://svn.eionet.europa.eu/projects/Zope/wiki/HowToDaviz
  4. EEA Daviz backlog wiki: https://svn.eionet.europa.eu/projects/Zope/wiki/DaViz

Funding
=======

  EEA_ - European Enviroment Agency (EU)

.. _EEA: http://www.eea.europa.eu/
