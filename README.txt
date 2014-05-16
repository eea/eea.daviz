=========
EEA Daviz
=========
|DaViz logo|

.. image:: http://ci.eionet.europa.eu/job/eea.daviz-www/badge/icon
  :target: http://ci.eionet.europa.eu/job/eea.daviz-www/lastBuild
.. image:: http://ci.eionet.europa.eu/job/eea.daviz-plone4/badge/icon
  :target: http://ci.eionet.europa.eu/job/eea.daviz-plone4/lastBuild
.. image:: http://ci.eionet.europa.eu/job/eea.daviz-zope/badge/icon
  :target: http://ci.eionet.europa.eu/job/eea.daviz-zope/lastBuild



Introduction
============

`EEA Daviz`_ is a web tool developed by the European Environment Agency which
helps creating interactive data visualizations easily through the web
browser, no extra tools are necessary. It is free and open source.

You can generate attractive and interactive charts and combine them in a
dashboard with facets/filters which updates the charts simultaneously.
Data can be uploaded as CSV/TSV or you can specify SPARQL to query
online Linked open data servers (aka sparql endpoints).

  **Daviz is the first Semantic web data visualisation tool for Plone CMS,
  entirely web-based!**

At the moment `Simile Exhibit`_ and `Google Charts`_ visualizations are
supported. The architecture allows to extend Daviz with more
visualisation libraries (visualisations plugins).

.. image:: http://eea.github.io/_images/eea.daviz.cover.png
   :target: http://www.youtube.com/watch?list=PLVPSQz7ahsByeq8nVKC7TT9apArEXBrV0&v=CYEAAAdyWII


.. contents::

Main features
=============

|Daviz features diagram|

1. No desktop tools needed to make visualizations. all web based.
2. Data input: easy copy and paste of data table from any webpage or
   excel sheet
3. Data input from URL (CSV/TSV/JSON)
4. Data input: drag-and-drop your data from CSV/TSV files, and we do the rest
5. Data input advanced: retrieve data from any SPARQL endpoint on the fly
6. Intuitive visualization editor to create interactive charts.
7. Large amount of visualizations available: Area, Bar,
   Bubble, Candlestick, Column, Combo Chart, Gauge, Geo Intensity Maps,
   Line, Pie, Radar, Scatter, Stepped Area, Table, Tree Map, Motion Charts,
   Faceted search table, Faceted tiles, Faceted timeline,
   Faceted map and more...
8. Dashboard. Group charts into one or more dashboards.
9. Share any chart. Embeddable visualization in any webpage.
10. Customizable chart options and colors
11. Data table manipulation via drag and drop, preparing table for chart
12. Pivot table (Transpose), transform row values into columns
13. Modular framework for extending it with more visualizations
14. Branding: add your own logo to each chart + QR code
15. And much more...


It is simple to use, needs no desktop application, everything is done
through the web by uploading an "excel file", CSV, TSV. You can also query
the "web of data" via public available sparql endpoints.

You can easily make visualizations like:

1. `Simile Exhibit <http://www.simile-widgets.org/exhibit3>`_
2. `Google Charts <http://code.google.com/apis/chart>`_

See also initial project `wiki page <http://taskman.eionet.europa.eu/projects/zope/wiki/DaViz>`_
for the reasoning behind this project.


Video Tutorials
===============
Most of DaViz features are presented throughout a series of video tutorials available under the `EEA Web Systems Training`_ YouTube channel.
The screencasts are divided in two playlists: Basic_ and Advanced_.


Live demos
==========

* `Basic tutorials <http://www.youtube.com/playlist?list=PLVPSQz7ahsByeq8nVKC7TT9apArEXBrV0>`_
* `Advanced tutorials <http://www.youtube.com/playlist?list=PLVPSQz7ahsBxbe8pwzFWLQuvDSP9JFn8I>`_
* `Daviz showroom <http://daviz.eionet.europa.eu>`_
* `Google charts demos <http://code.google.com/apis/chart>`_
* `MIT Simile Exhibit demos <http://www.simile-widgets.org/exhibit3>`_


Architecture overview
=====================

At the moment `Simile Exhibit`_ and `Google Charts`_ visualizations are
supported. The architecture allows to extend Daviz with more
visualisation libraries (visualisations plugins).

.. image:: http://eea.github.com/_images/eea.daviz.layers.svg


Installation
============

zc.buildout
-----------
If you are using `zc.buildout`_ and the `plone.recipe.zope2instance`_
recipe to manage your project, you can do this:

* Update your buildout.cfg file:

  * Add ``eea.daviz`` to the list of eggs to install

  ::

    [instance]
    ...
    eggs =
      ...
      eea.daviz

* Re-run buildout, e.g. with::

  $ ./bin/buildout


Google Maps API Key
~~~~~~~~~~~~~~~~~~~

Plone
+++++
Within ZMI -> Plone Site -> portal_properties add a plone property sheet called
geographical_properties and inside it add a new string property
called google_key.

Zope
++++
Within ZMI -> Top Folder -> manage_propertiesForm add a string property called
google_key

In this property you have to paste the Google maps API KEY, follow instruction
https://developers.google.com/maps/documentation/javascript/tutorial#api_key

The Google account you use to generate the key has to be owner of the site,
this is done by verification via Google webmaster tools.


Dependencies
============

`EEA Daviz`_ has the following dependencies:
  - `Plone 4.x`_
  - `eea.app.visualization`_
  - `eea.sparql`_
  - `eea.forms`_
  - `eea.googlecharts`_
  - `eea.exhibit`_
  - `collective.js.jqueryui < 1.9`_ (Plone 4.0, 4.1, 4.2)
  - `collective.js.jqueryui > 1.9`_ (Plone 4.3+)

The following package are optional. Still they can improve the user experience with this tool:
  - `eea.relations`_
  - `eea.cache`_ (Check `eea.cache`_ documentation for more about
    memcache configuration)
  - `eea.depiction`_

  ::

    [instance]
    ...
    eggs =
      ...
      eea.daviz [full]

    zcml =
      ...
      eea.daviz-overrides
      eea.daviz-full


.. image:: http://eea.github.com/_images/eea.daviz.dependencies.svg


Source code
===========

Latest source code (Plone 4 compatible):
  - `Plone Collective on Github <https://github.com/collective/eea.daviz>`_
  - `EEA on Github <https://github.com/eea/eea.daviz>`_

Plone 2 and 3 compatible (Simile Exhibit visualisations only):
  https://github.com/collective/eea.daviz/tree/plone25


Copyright and license
=====================

The Initial Owner of the Original Code is European Environment Agency (EEA).
All Rights Reserved.

The EEA Daviz (the Original Code) is free software;
you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation;
either version 2 of the License, or (at your option) any later
version.

More details under eea.daviz/docs/License.txt


More documentation
==================

-  `Daviz technical documentation on
   github <http://eea.github.com/docs/eea.daviz>`_
-  `Daviz plone product summary <http://plone.org/products/eea.daviz>`_
-  `Data input
   examples <http://www.eea.europa.eu/data-and-maps/daviz/learn-more/examples>`_
-  `How to prepare your
   data <http://www.eea.europa.eu/data-and-maps/daviz/learn-more/prepare-data>`_


Links
=====

1. Simile Wiki - Exhibit 2.0: http://simile.mit.edu/wiki/Exhibit
2. Simile widgets: http://www.simile-widgets.org/exhibit
3. EEA Daviz how-to: http://taskman.eionet.europa.eu/projects/zope/wiki/HowToDaViz
4. EEA Daviz backlog wiki: http://taskman.eionet.europa.eu/projects/zope/wiki/DaViz
5. Google charts: http://code.google.com/apis/chart/


Funding and project management
==============================

EEA_ - European Environment Agency (EU)

.. _EEA: http://www.eea.europa.eu/
.. _`EEA Daviz`: http://eea.github.com/docs/eea.daviz
.. _`EEA Google Charts`: http://eea.github.com/docs/eea.googlecharts
.. _`EEA Exhibit`: http://eea.github.com/docs/eea.exhibit
.. _`eea.daviz`: http://eea.github.com/docs/eea.daviz
.. _`eea.depiction`: http://eea.github.com/docs/eea.depiction
.. _`eea.googlecharts`: http://eea.github.com/docs/eea.googlecharts
.. _`eea.exhibit`: http://eea.github.com/docs/eea.exhibit
.. _`eea.app.visualization`: http://eea.github.com/docs/eea.app.visualization
.. _`eea.sparql`: http://eea.github.com/docs/eea.sparql
.. _`eea.cache`: http://eea.github.com/docs/eea.cache
.. _`eea.forms`: http://eea.github.com/docs/eea.forms
.. _`eea.relations`: http://eea.github.com/docs/eea.relations
.. _`plone.recipe.zope2instance`: http://pypi.python.org/pypi/plone.recipe.zope2instance
.. _`EEA App Visualization`: http://eea.github.com/docs/eea.app.visualization
.. _`Simile Exhibit`: http://www.simile-widgets.org/exhibit3
.. _`Google Charts`: http://code.google.com/apis/chart
.. _`plone.recipe.zope2instance`: http://pypi.python.org/pypi/plone.recipe.zope2instance
.. _`zc.buildout`: http://pypi.python.org/pypi/zc.buildout
.. |Daviz features diagram| image:: http://daviz.eionet.europa.eu/learn-more/davizdiagram.png/image_large
.. |DaViz logo| image:: http://daviz.eionet.europa.eu/logo.png
.. _`Plone 4.x`: http://plone.org
.. _`collective.js.jqueryui < 1.9`: https://pypi.python.org/pypi/collective.js.jqueryui
.. _`collective.js.jqueryui > 1.9`: https://pypi.python.org/pypi/collective.js.jqueryui
.. _Basic: http://www.youtube.com/playlist?list=PLVPSQz7ahsByeq8nVKC7TT9apArEXBrV0
.. _Advanced: http://www.youtube.com/playlist?list=PLVPSQz7ahsBxbe8pwzFWLQuvDSP9JFn8I
.. _`EEA Web Systems Training`: https://www.youtube.com/channel/UCAjXKVcpfF05urEk9uYFveA
