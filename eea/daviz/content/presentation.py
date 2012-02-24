""" Daviz Presentation
"""
from zope.event import notify
from zope.interface import implements
from plone.app.folder.folder import ATFolder
from Products.Archetypes.atapi import Schema
from eea.daviz.content.interfaces import IDavizPresentation
from eea.daviz.config import EEAMessageFactory as _
from eea.daviz.events import DavizRelationsChanged, DavizSpreadSheetChanged
from Products.Archetypes.public import StringField, TextAreaWidget, LabelWidget
from eea.forms.widgets.QuickUploadWidget import QuickUploadWidget


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

class DavizStringField(StringField):
    """ Notify on set
    """
    def set(self, instance, value, **kwargs):
        """ Custom set
        """
        super(DavizStringField, self).set(instance, value, **kwargs)
        notify(DavizSpreadSheetChanged(instance, spreadsheet=value))

SCHEMA = Schema((
    StringField(
        'dataSources',
        schemata="default",
        widget=LabelWidget(
            label=_('daviz_label_data_sources',
                    default='Data sources'),
            description=_('daviz_help_data_sources',
                    default=".tsv, .csv files, SPARQL methods, etc"),
            i18n_domain="eea",
            visible={'edit' : 'visible', 'view' : 'invisible' }
        )
    ),
    DavizReferenceField(
        'relatedItems',
        schemata="default",
        relationship='relatesTo',
        multiValued=True,
        widget=ReferenceBrowserWidget(
            label=_("daviz_label_related_items",
                    default="Choose from existing data sources"),
            description=_("daviz_help_related_items", default=(
                "specify items to be visualized within this Daviz Visualization"
                " (e.g. .tsv, .csv files, SPARQL methods, etc)")),
            i18n_domain="eea",
            visible={'edit' : 'visible', 'view' : 'invisible' }
        )),
    StringField(
        'quickUpload',
        schemata='default',
        widget=QuickUploadWidget(
            label=_('daviz_label_quick_upload',
                    default='or upload new data sources from your computer'),
            description=_('daviz_help_quick_upload', default=(
                "drag and drop '.tsv, .csv files' in the area bellow"
            )),
            i18n_domain="eea",
            visible={'edit' : 'visible', 'view' : 'invisible' }
        )
    ),
    DavizStringField(
        'spreadsheet',
        schemata='default',
        validators=('csvfile',),
        widget=TextAreaWidget(
            label=_('daviz_label_spreadsheet',
                    default='or copy and paste text from a file'),
            description=_('daviz_help_spreadsheet', default=(
                "copy and paste 'TAB separated or Comma separated text' "
                "in the area bellow"
            )),
        i18n_domain="eea",
        helper_js=('++resource++eea.daviz.spreadsheet.js',),
        helper_css=('++resource++eea.daviz.spreadsheet.css',),
        visible={'edit' : 'visible', 'view' : 'invisible' }
        )
    ),
))

DAVIZ_SCHEMA = ATFolder.schema.copy() + SCHEMA.copy()
DAVIZ_SCHEMA.moveField('relatedItems', after="dataSources")
DAVIZ_SCHEMA.moveField('quickUpload', after="relatedItems")
DAVIZ_SCHEMA.moveField('spreadsheet', after="quickUpload")

class DavizPresentation(ATFolder):
    """ Daviz Presentation
    """
    implements(IDavizPresentation)

    meta_type = 'DavizPresentation'
    portal_type = 'DavizPresentation'
    archetype_name = 'DavizPresentation'

    schema = DAVIZ_SCHEMA
