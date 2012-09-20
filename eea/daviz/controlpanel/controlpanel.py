""" Daviz Settings Section
"""
from zope.interface import implements
from eea.app.visualization.controlpanel.interfaces import IDavizSection
from zope.formlib.form import FormFields
from zope import schema
from zope.app.component.hooks import getSite

class InvalidDavizFolder(schema.ValidationError, Exception):
    """Daviz DefaultFolder Error
    """
    __doc__ = """Folder does not exist or
              doesn't allow visualizations to be added"""

class DavizSection(object):
    """ Daviz  Settings Section
    """
    implements(IDavizSection)
    prefix = 'daviz'
    title = 'Daviz Settings'

    def __init__(self):
        def validateDefaultFolder(value):
            """ DefaultFolder Validation"""
            if value == "":
                return True
            portal = getSite()
            try:
                folder = portal.restrictedTraverse(value.encode('utf8'))
                allowedContentTypes = folder.allowedContentTypes()
                for allowedContentType in allowedContentTypes:
                    if allowedContentType.id == "DavizVisualization":
                        return True

            except (KeyError, AttributeError):
                raise InvalidDavizFolder(value)
            raise InvalidDavizFolder(value)

        self.form_fields = FormFields(
            schema.TextLine(
                __name__='daviz.defaultfolder',
                title=u'Default Folder for Visualizations',
                constraint=validateDefaultFolder,
                required=False)
            )

DavizSectionFactory = DavizSection()