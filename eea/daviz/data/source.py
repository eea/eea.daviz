""" Daviz Data Provenance

    >>> portal = layer['portal']
    >>> from eea.app.visualization.interfaces import IDataProvenance

"""
from zope.component import queryAdapter
from eea.app.visualization.interfaces import IDataProvenance
from eea.app.visualization.data.source import DataProvenance

from eea.app.visualization.interfaces import IMultiDataProvenance
from eea.app.visualization.data.source import MultiDataProvenance

from zope.annotation.interfaces import IAnnotations

from eea.app.visualization.config import ANNO_MULTIDATA

class DavizDataProvenance(DataProvenance):
    """
    Daviz Visualization data provenance metadata accessor/mutator

        >>> doc = portal.invokeFactory('DavizVisualization', 'daviz')
        >>> doc = portal._getOb(doc)
        >>> source = IDataProvenance(doc)
        >>> source
        <eea.daviz.data.source.DavizDataProvenance object...>

    """
    #
    # Internal
    #
    def getProperty(self, name):
        """ Get property by name
        """
        relatedItems = self.context.getRelatedItems()
        if not relatedItems:
            return getattr(DataProvenance(self.context), name, u'')

        for item in relatedItems:
            source = queryAdapter(item, IDataProvenance)
            if not source:
                continue
            if not getattr(source, name):
                continue
            return getattr(source, name)
        return u''

    def setProperty(self, name, value):
        """ Set property by name with given value
        """
        if not value:
            return

        relatedItems = self.context.getRelatedItems()
        if not relatedItems:
            return setattr(DataProvenance(self.context), name, value)

        for item in relatedItems:
            source = queryAdapter(item, IDataProvenance)
            if not source:
                continue
            setattr(source, name, value)
    #
    # Title
    #
    @property
    def title(self):
        """Data source title

            >>> source.title
            u''

        """
        return self.getProperty('title')


    @title.setter
    def title(self, value):
        """
        Data source title setter

            >>> source.title = 'GDP vs. GHG'
            >>> source.title
            u'GDP vs. GHG'

        """
        return self.setProperty('title', value)
    #
    # Link
    #
    @property
    def link(self):
        """
        Data source link

            >>> source.link
            u''

        """
        return self.getProperty('link')

    @link.setter
    def link(self, value):
        """
        Data source link setter

            >>> source.link = 'http://daviz.eionet.europa.eu'
            >>> source.link
            u'http://daviz.eionet.europa.eu'

        """
        return self.setProperty('link', value)
    #
    # Owner
    #
    @property
    def owner(self):
        """
        Data source owner

            >>> source.owner
            u''

        """
        return self.getProperty('owner')

    @owner.setter
    def owner(self, value):
        """
        Data source owner setter

            >>> source.owner = 'EEA'
            >>> source.owner
            u'EEA'

        """
        return self.setProperty('owner', value)

class DavizMultiDataProvenance(MultiDataProvenance):
    """ daviz multi data provenance
    """

    @property
    def provenances(self):
        anno = IAnnotations(self.context)
        anno_provenances = anno.get(ANNO_MULTIDATA, ({},))

        orderindex = 0
        if anno_provenances == ({},):
            anno_provenances = ()
            relatedItems = self.context.getRelatedItems()
            for item in relatedItems:
                source = queryAdapter(item, IMultiDataProvenance)
                item_provenances = getattr(source, 'provenances')
                for item_provenance in item_provenances:
                    item_provenance['orderindex_'] = orderindex
                    orderindex = orderindex + 1
                    anno_provenances = anno_provenances + (item_provenance,)

        return anno_provenances


    @provenances.setter
    def provenances(self, value):
        anno = IAnnotations(self.context)
        anno[ANNO_MULTIDATA] = value
