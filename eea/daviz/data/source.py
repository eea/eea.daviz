""" Daviz Data Provenance

    >>> portal = layer['portal']
    >>> from eea.app.visualization.interfaces import IDataProvenance

"""
from zope.interface import implements
from zope.component import queryAdapter
from eea.app.visualization.interfaces import IDataProvenance
from eea.app.visualization.data.source import DataProvenance

from eea.app.visualization.interfaces import IMultiDataProvenance
from eea.app.visualization.data.source import MultiDataProvenance

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
    implements(IMultiDataProvenance)

    def defaultProvenances(self):
        """ default provenances
        """
        relatedProvenances = ()
        relatedItems = self.context.getRelatedItems()
        orderindex = 0
        for item in relatedItems:
            source = queryAdapter(item, IMultiDataProvenance)

            #fix for #20869 if related item has provenance info with a link
            #to this visualization, skip it
            is_provenance_info = False
            for provenance in source.provenances:
                if provenance['link'] == self.context.absolute_url():
                    is_provenance_info = True
            if is_provenance_info:
                continue
            #end of fix for #20869

            item_provenances = getattr(source, 'provenances')
            for item_provenance in item_provenances:
                dict_item_provenance = dict(item_provenance)
                if dict_item_provenance.get('title', '') != '' and \
                    dict_item_provenance.get('link', '') != '' and \
                    dict_item_provenance.get('owner', '') != '':
                    dict_item_provenance['orderindex_'] = orderindex
                    orderindex = orderindex + 1
                    relatedProvenances = relatedProvenances + \
                                        (dict_item_provenance,)
        return relatedProvenances
