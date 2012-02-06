""" Daviz Presentation
"""
from zope.event import notify
from zope.interface import implements
from plone.app.folder.folder import ATFolder
from Products.Archetypes.atapi import Schema
from eea.daviz.content.interfaces import IDavizPresentation
from eea.daviz.config import EEAMessageFactory as _
from eea.daviz.events import DavizRelationsChanged

try:
    from eea.relations.field.referencefield import EEAReferenceField
    ReferenceField = EEAReferenceField
    from eea.relations.widget.referencewidget import EEAReferenceBrowserWidget
    ReferenceBrowserWidget = EEAReferenceBrowserWidget
except ImportError:
    from Products.Archetypes.Field import ReferenceField
    from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

class DavizReferenceField(ReferenceField):
    """ Notify on set
    """
    def set(self, instance, value, **kwargs):
        """ Notify custom event on set
        """
        old = self.getRaw(instance, aslist=True)
        super(DavizReferenceField, self).set(instance, value, **kwargs)

        if set(old) != set(value):
            relatedItems = self.get(instance, aslist=True)
            notify(DavizRelationsChanged(instance, relatedItems=relatedItems))


SCHEMA = Schema((
    DavizReferenceField(
        'relatedItems',
        schemata="default",
        relationship='relatesTo',
        multiValued=True,
        widget=ReferenceBrowserWidget(
            label=_("daviz_label_related_items",
                    default="Sources (exhibit sources)"),
            description=_("daviz_help_related_items", default=(
                "Specify items to be visualized within this DaViz Presentation"
                " (e.g. TAB separated files, SPARQL methods, etc)")),
            i18n_domain="eea",
            visible={'edit' : 'visible', 'view' : 'invisible' }
        )),
))

class DavizPresentation(ATFolder):
    """ Daviz Presentation
    """
    implements(IDavizPresentation)

    meta_type = 'DavizPresentation'
    portal_type = 'DavizPresentation'
    archetype_name = 'DavizPresentation'

    schema = ATFolder.schema.copy() + SCHEMA.copy()
