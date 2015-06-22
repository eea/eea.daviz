""" Create visualizations with datasources
"""
from zope.component.hooks import getSite
from zope.component import queryUtility
from eea.app.visualization.controlpanel.interfaces import IDavizSettings
from zope.container.interfaces import INameChooser

class Daviz(object):
    """ Daviz
    """
    def createNewDaviz(self):
        """ Create new visualization
        """
        davizsettings = queryUtility(IDavizSettings)
        strFolder = davizsettings.settings.get("daviz.defaultfolder", "")
        if strFolder != "":
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
        chooser = INameChooser(folder)
        newId = chooser.chooseName(self.context.title, folder)
        if newId in folder.objectIds():
            raise NameError, 'Object id %s already exists' % newId
        else:
            folder.invokeFactory("DavizVisualization", newId)
        newObj = folder[newId]
        newObj.title = self.context.title
        newObj.setRelatedItems([self.context])
        self.request.response.redirect(newObj.absolute_url()+"/daviz-edit.html")

