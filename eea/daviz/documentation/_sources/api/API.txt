=============
EEA Daviz API
=============
EEA Daviz python package `eea.daviz`_ is more a bundle package (a collection of
visualization packages) than the real visualization package. Thus, the scope of
this package is to put together the visualization core application
`eea.app.visualization`_ and the visualization add-ons (`eea.googlecharts`_,
`eea.exhibit`_, etc). It also brings in `eea.sparql`_ package whitch allows
fetching data from Linked open data servers (sparql endpoints) and use it as
input for our visualizations.


.. contents::


A Layered Architecture
======================
EEA Daviz consists of three independent layers. Bottom layers do not require the
other top layers, so an application builder can choose the one or more
layers required for a particular solution:

- **Visualization API** - eea.app.visualization
- ** Visualization Libraries** - eea.googlecharts, eea.exhibit, etc
- ** Visualization Bundle** - eea.daviz

.. image:: images/eea.daviz.layers.svg


Dependencies graph
==================
This diagram shows how the visualization packages depends each other
and also which packages are Plone dependent and which requires only
Zope or Python (see the background colors).

.. image:: images/eea.daviz.dependencies.svg


.. include:: ../../stub.rst


.. _`eea.daviz`: ../../../docs/eea.daviz/index.html
.. _`eea.app.visualization`: ../../../docs/eea.app.visualization/index.html
.. _`eea.googlecharts`: ../../../docs/eea.googlecharts/index.html
.. _`eea.exhibit`: ../../../docs/eea.exhibit/index.html
.. _`eea.sparql`: ../../../docs/eea.sparql/index.html
