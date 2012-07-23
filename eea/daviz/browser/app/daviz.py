""" Create visualizations with datasources
"""
class Daviz(object):
    """ Daviz
    """
    def createNewDaviz(self):
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
