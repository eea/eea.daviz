""" Create visualizations with datasources
"""
from zope.app.component.hooks import getSite
from zope.component import queryUtility
from eea.app.visualization.controlpanel.interfaces import IDavizSettings

class Daviz(object):
    """ Daviz
    """
    def createNewDaviz(self):
        """ Create new visualization
        """
        davizsettings = queryUtility(IDavizSettings)
        strFolder = davizsettings.settings.get("daviz.defaultfolder", "")
        if (strFolder != ""):
            portal = getSite()
            folder = portal.restrictedTraverse(strFolder)
        else:
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
                "?title=" + self.context.title + \
                "&relatedItems:list=" + self.context.UID()
        self.request.response.redirect(url)

