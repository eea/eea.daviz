EEA Daviz product
=================
EEA Daviz is a plone product for data visualizations. You can generate attractive 
and interactive charts and combine them in a dashboard with facets/filters 
which updates the charts simultaneously. Data can be uploade as CSV,TSV or you can 
specify SPARQL to query Linked open data servers (sparql endpoints). 

At the moment Simile Exhibit and Google Charts visualizations are supported. 

The first Semantic web data visualisation tool for Plone.


Contents
========

.. contents::


Introduction
============

It is simple to use, needs no desktop application, everything is done
through the web by uploading an "excel file", CSV, TSV. You can also query 
the "web of data" via public available sparql endpoints. 

You can easily make visualizations like: 
   1. http://www.simile-widgets.org/exhibit
   2. http://code.google.com/apis/chart/

See also initial project wiki page https://svn.eionet.europa.eu/projects/Zope/wiki/DaViz
for the reasoning behind this project.


Main features
=============


The main features are:

  1. no desktop tools needed to make visualizations. all web based.
  2. data input: easy copy and paste of data table from any webpage or excel sheet
  3. data input: drag-and-drop your data from CSV/TSV files, and we do the rest
  4. data input advanced: retrieve data from any SPARQL endpoint on the fly
  5. Intuitive visualization editor to create interactive charts.
  6. Large amount of visualizations available: Area, Bar, \
     Bubble, Candlestick, Column, Combo Chart, Gauge, Geo Intensity Maps, Line, Pie, Radar, Scatter, Stepped Area, Table, Tree Map, Motion Charts, Faceted search table, Faceted tiles, Faceted timeline, Faceted map and more...
  7. Dashboard. Group charts into one dashboard.
  8. Share any chart. Embeddabe visualization in any webpage.
  9. Customizable chart options and colors
  10. Data table manipulation via drag and drop, preparing table for chart
  11. Pivot table (Transpose), tranform row values into columns
  12. Modular framework for extending it with more visualizations
  13. And much more...

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
  6. eea.sparql
  7. eea.googlecharts


Live demos
==========

Eurostat data employment rates 2000-2010 (demo using Linked Data): 
   http://www.eea.europa.eu/data-and-maps/daviz/data-visualization-employement-trends-eu-1

GHG vs GDP in Europe 1990 - 2009 (demo using Linked Data)
   http://www.eea.europa.eu/data-and-maps/daviz/ghg-vs-gdp-in-europe
   
GHG national emissions reporting to UNFCC (Simile Exhibit demo with TSV)
   http://www.eea.europa.eu/data-and-maps/data/national-emissions-reported-to-the-unfccc-and-to-the-eu-greenhouse-gas-monitoring-mechanism-3/national-total-excluding-lulucf/ghg_v10_extract.csv

Google charts demos:
   http://code.google.com/apis/chart/

MIT Simile Exhibit demos:
   http://www.simile-widgets.org/exhibit

   
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
  5. Google charts: http://code.google.com/apis/chart/

Funding
=======

  EEA_ - European Enviroment Agency (EU)

.. _EEA: http://www.eea.europa.eu/
