""" Daviz Visualization
"""
from zope.event import notify
from zope.interface import implements
from plone.app.folder.folder import ATFolder
from Products.Archetypes.atapi import Schema
from eea.daviz.content.interfaces import IDavizVisualization
from eea.daviz.config import EEAMessageFactory as _
from eea.daviz.events import DavizRelationsChanged, DavizSpreadSheetChanged
from Products.Archetypes.public import StringField, TextAreaWidget
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
    DavizReferenceField(
        'relatedItems',
        schemata="data input",
        relationship='relatesTo',
        multiValued=True,
        widget=ReferenceBrowserWidget(
            label=_("daviz_label_related_items",
                    default="Find and reuse existing data"),
            description=_("daviz_help_related_items",
              default=(
                "Look for compatible datasets in catalogue"
                " (e.g. visualization data, .tsv, .csv, SPARQL, etc)"
              )
            ),
            i18n_domain="eea",
            visible={'edit' : 'visible', 'view' : 'invisible' }
        )),
    StringField(
        'quickUpload',
        schemata='data input',
        widget=QuickUploadWidget(
            label=_('daviz_label_quick_upload',
                    default='Upload CSV/TSV data files from your computer'),
            description=_('daviz_help_quick_upload',
              default=(
                "Drag and drop '.tsv, .csv files' in the area below, see "
                '<a target="_blank" href="http://www.eea.europa.eu/'
                'data-and-maps/daviz/learn-more/examples">data examples</a> '
                'or read '
                '<a target="_blank" href="http://www.eea.europa.eu/'
                'data-and-maps/daviz/learn-more/prepare-data">'
                'how to prepare data</a>'
              )
            ),
            i18n_domain="eea",
            visible={'edit' : 'visible', 'view' : 'invisible' }
        )
    ),
    DavizStringField(
        'spreadsheet',
        schemata='data input',
        validators=('csvfile',),
        widget=TextAreaWidget(
            label=_('daviz_label_spreadsheet',
                    default='Copy and paste a data table from a file/webpage'),
            description=_('daviz_help_spreadsheet',
              default=(
                "Check these "
                '<a target="_blank" href="http://www.eea.europa.eu/'
                'data-and-maps/daviz/learn-more/examples">data examples</a> '
                'or read '
                '<a target="_blank" href="http://www.eea.europa.eu/'
                'data-and-maps/daviz/learn-more/prepare-data">'
                'how to prepare data</a>'
              )
            ),
        i18n_domain="eea",
        helper_js=('++resource++eea.daviz.spreadsheet.js',),
        helper_css=('++resource++eea.daviz.spreadsheet.css',),
        visible={'edit' : 'visible', 'view' : 'invisible' }
        )
    ),
))

DAVIZ_SCHEMA = ATFolder.schema.copy() + SCHEMA.copy()

def finalizeSchema(schema=DAVIZ_SCHEMA):
    """ Reorder and update schemata
    """
    # Move all fields to Metadata schemata
    for field in schema.fields():
        # Leave this fields in their original schemata
        if field.getName() in ('spreadsheet', 'quickUpload', 'relatedItems'):
            continue

        # We use schema extender for this fields, so leave them in
        # categorization tab
        if field.getName() in ('subject', 'location', 'themes'):
            field.schemata = 'categorization'
            continue

        # Group all the other fields in a new schemata. Don't try to use
        # 'metadata' as it seems to be a reserved keyword in Plone (or EEA)
        field.schemata = 'other metadata'

    # Add a default value for title
    schema['title'].default = u'Data Visualization'

    # Reorder data input fields
    # schema.moveField('dataSources', pos=0)
    schema.moveField('spreadsheet', pos=0)
    schema.moveField('quickUpload', after="spreadsheet")
    schema.moveField('relatedItems', after="quickUpload")

finalizeSchema(DAVIZ_SCHEMA)

class DavizVisualization(ATFolder):
    """ Daviz Visualization
    """
    implements(IDavizVisualization)

    meta_type = 'DavizVisualization'
    portal_type = 'DavizVisualization'
    archetype_name = 'DavizVisualization'

    schema = DAVIZ_SCHEMA

#BBB
DavizPresentation = DavizVisualization
