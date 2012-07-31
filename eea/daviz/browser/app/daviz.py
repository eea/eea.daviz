""" Create visualizations with datasources
"""
class Daviz(object):
    """ Daviz
    """
    def createNewDavizReuse(self):
        """ create new visualization using 
        the datasources of current visualization
        """
        objId = self.context.aq_parent.generateUniqueId("DavizVisualization")
        relatedItems = self.context.getRelatedItems()
        url = self.context.aq_parent.absolute_url() + \
                "/portal_factory/DavizVisualization/" + \
                objId + \
                "/edit" + \
                "?title=" + relatedItems[0].title
        for item in relatedItems:
            url = url + "&relatedItems:list=" + item.UID()
        self.request.response.redirect(url)

    def createNewDavizReuseObj(self):
        """ create new visualization using 
        as datasource the object of current visualization
        """
        objId = self.context.aq_parent.generateUniqueId("DavizVisualization")
        url = self.context.aq_parent.absolute_url() + \
                "/portal_factory/DavizVisualization/" + \
                objId + \
                "/edit" + \
                "?title=" + self.context.title
        url = url + "&relatedItems:list=" + self.context.UID()
        self.request.response.redirect(url)

    def createNewDavizSparql(self):
        """ create new visualization using 
        the current Sparql
        """
        # Find parent folder where Daviz can be created
        folder = self.context.aq_parent
        found = False
        while True:
            try:
                allowedContentTypes = folder.allowedContentTypes()
            except AttributeError:
                break
            for allowedContentType in allowedContentTypes:
                if allowedContentType.id == "DavizVisualization":
                    found = True
            if found:
                break
            folder = folder.aq_parent
        if not found:
            return

        objId = folder.generateUniqueId("DavizVisualization")
        url = folder.absolute_url() + \
                "/portal_factory/DavizVisualization/" + \
                objId + \
                "/edit" + \
                "?title=" + self.context.title
        url = url + "&relatedItems:list=" + self.context.UID()
        self.request.response.redirect(url)
