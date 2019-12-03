""" Create visualizations with datasources
"""
from zope.component.hooks import getSite
from zope.component import queryUtility
from zope.container.interfaces import INameChooser
from zope.interface import implementer
from eea.app.visualization.controlpanel.interfaces import IDavizSettings
from eea.depiction.interfaces import IRecreateScales
from plone.scale.storage import AnnotationStorage
from plone.scale.scale import scaleImage
from uuid import uuid4
from time import time


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


@implementer(IRecreateScales)
class RecreateScales(object):
    """ Recreate image scales daviz custom adapter
    """
    def __init__(self, context):
        self.context = context

    def __call__(self, fieldname='image'):
        image_view = self.context.restrictedTraverse('@@imgview')
        image = getattr(image_view, 'img', None)
        if not image:
            raise AttributeError(fieldname)
        if getattr(image, 'portal_type', '') == 'Image':
            field = image.getField(fieldname)
            if not field:
                raise AttributeError(fieldname)
            field.removeScales(image)
            field.createScales(image)
        else:
            # use plone.scale annotation storage
            image_data = image()
            scale_result = scaleImage(image_data, width=image.width(), height=image.height())
            storage = AnnotationStorage(self.context, time)

            if scale_result is not None:
                # storage will be modified:
                # good time to also cleanup
                parameters = {
                    'image_hash': image.__hash__(),
                    'modified': time()
                }

                key = storage.hash(**parameters)
                storage._cleanup()
                data, format_, dimensions = scale_result
                width, height = dimensions
                uid = str(uuid4())
                info = dict(
                    uid=uid,
                    data=data,
                    width=width,
                    height=height,
                    mimetype='image/{0}'.format(format_.lower()),
                    key=key,
                    modified=storage.modified_time,
                )
                try:
                    storage.storage[uid] = info
                except:
                    import pdb; pdb.set_trace()
        return info or None