""" Create visualizations with datasources
"""
from Acquisition import aq_base
from ZODB.blob import Blob
from eea.app.visualization.controlpanel.interfaces import IDavizSettings
from eea.depiction.interfaces import IRecreateScales
from plone.app.blob.config import blobScalesAttr
from plone.scale.scale import scaleImage
from zope.component.hooks import getSite
from zope.component import queryUtility
from zope.container.interfaces import INameChooser
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
from Products.Five.browser import BrowserView
import logging
logger = logging.getLogger('eea.daviz')


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
        import requests
        url_base = 'https://www.eea.europa.eu/'
        requests.get(url_base + self.context.absolute_url() + '/@@recreate.scale')


@implementer(IPublishTraverse)
class RecreateScaleView(BrowserView):
    """ Recreate daviz scales view
    """
    def __call__(self, fieldname='image'):
        image_view = self.context.unrestrictedTraverse('@@imgview')
        image = getattr(image_view, 'img', None)
        url = self.context.absolute_url()
        if not image:
            logger.error("Error while recreating scale for %s" % url)
            raise AttributeError(fieldname)

        info = None
        if getattr(image, 'portal_type', '') == 'Image':
            field = image.getField(fieldname)
            if not field:
                raise AttributeError(fieldname)
            try:
                field.removeScales(image)
                field.createScales(image)
                logger.info("Succesfully scaled %s" % url)
            except Exception:
                logger.error("Error while recreating scale for %s" % url)
        else:
            # use plone.app.blob store scale
            for name, size in image.sizes.items():
                image_data = image_view(name)
                if not image_data:
                    continue

                width, height = size
                scale_result = scaleImage(image_data, width=width, height=height)
                if scale_result is not None:
                    id = fieldname + "_" + name
                    data, format_, dimensions = scale_result
                    info = dict(
                        data=data,
                        id = id,
                        content_type='image/{0}'.format(format_.lower()),
                        filename='',
                    )
                    fields = getattr(aq_base(self.context), blobScalesAttr, {})
                    scales = fields.setdefault(fieldname, {})
                    info['blob'] = Blob()
                    blob = info['blob'].open('w')
                    blob.write(info['data'])
                    blob.close()
                    del info['data']
                    scales[name] = info
                    setattr(self.context, blobScalesAttr, fields)
                    self.context._p_changed = True
            logger.info("Succesfully scaled %s " % url)
        return "Done"