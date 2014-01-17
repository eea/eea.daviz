""" Daviz content schema
"""

from Products.ATContentTypes.content.folder import ATFolder
from Products.Archetypes.atapi import Schema, DisplayList
from Products.Archetypes.public import StringField, ReferenceField, \
                                        BooleanWidget, BooleanField
from Products.Archetypes.public import TextAreaWidget, StringWidget, LabelWidget
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from eea.app.visualization.interfaces import IDataProvenance
from eea.app.visualization.interfaces import IMultiDataProvenance
from eea.daviz.config import EEAMessageFactory as _
from eea.daviz.events import DavizExternalChanged
from eea.daviz.events import DavizRelationsChanged
from eea.daviz.events import DavizSpreadSheetChanged
from eea.forms.widgets.QuickUploadWidget import QuickUploadWidget
from zope.component import queryAdapter, queryUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.event import notify
import logging
from Products.Archetypes.interfaces import IVocabulary
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.field import ExtensionField
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.interfaces import IBaseObject


logger = logging.getLogger('eea.daviz')
#
# eea.relations
#
EEAReferenceField = ReferenceField
EEAReferenceBrowserWidget = ReferenceBrowserWidget
try:
    from eea.relations.field.referencefield import EEAReferenceField
    from eea.relations.widget.referencewidget import EEAReferenceBrowserWidget
except ImportError:
    logger.warn('eea.relations is not installed')
#
# eea.dataservice
#
OrganisationsWidget = StringWidget
OrganisationsVocabulary = None
OwnerColumn = Column("Owner")
widget_helper_js = ('++resource++eea.daviz.datasource.js',
                   'datagridwidget.js',)
try:
    from eea.dataservice.widgets import OrganisationsWidget
    OrganisationsVocabulary = u'Organisations'
    class ArchetypesOrganisationsVocabulary:
        """Wrapper for OrganisationsVocabulary to Archetypes Vocabulary
        """
        implements(IVocabulary)

        def getDisplayList(self, instance):
            """getDisplayList
            """
            voc_fact = queryUtility(IVocabularyFactory, OrganisationsVocabulary)
            items = [(t.value, t.title or t.token) for t in voc_fact(instance)]
            items.insert(0, ('',''))
            vocabulary = DisplayList(items)
            return vocabulary

    tmpOrganisationsVocabulary = ArchetypesOrganisationsVocabulary()
    OwnerColumn = SelectColumn("Owner",
                                vocabulary=tmpOrganisationsVocabulary,
                                default='')
    widget_helper_js = ('++resource++eea.daviz.datasource.js',
                        'datagridwidget.js',
                        'selectautocomplete_widget.js',)
except ImportError:
    logger.warn('eea.dataservice is not installed')


class DavizReferenceField(EEAReferenceField):
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
        try:
            old = self.getStorage(instance).get(
                self.getName(), instance, **kwargs)
        except Exception, err:
            logger.debug(err)
            old = u''

        super(DavizStringField, self).set(instance, value, **kwargs)
        if old != value:
            notify(DavizSpreadSheetChanged(instance, spreadsheet=value))
class DavizUrlField(StringField):
    """ Notify on set
    """
    def set(self, instance, value, **kwargs):
        """ Custom set
        """
        super(DavizUrlField, self).set(instance, value, **kwargs)
        notify(DavizExternalChanged(instance, external=value))

class DavizDataField(StringField):
    """ Custom data field
    """
    _properties = StringField._properties.copy()
    _properties.update({
        'alias': '',
    })

    def get(self, instance, **kwargs):
        """ Get data source from annotations
        """
        config = queryAdapter(instance, IDataProvenance)
        return getattr(config, self.alias, u'')

    def set(self, instance, value, **kwargs):
        """ Updates data source
        """
        config = queryAdapter(instance, IDataProvenance)
        setattr(config, self.alias, value)

class DavizDataGridField(ExtensionField, DataGridField):
    """ Custom data grid field
    """
    def get(self, instance, **kwargs):
        """ get provenances
        """
        config = queryAdapter(instance, IMultiDataProvenance)
        return getattr(config, 'provenances', ({},))

    def set(self, instance, value, **kwargs):
        """ update provenances
        """
        config = queryAdapter(instance, IMultiDataProvenance)
        original_values = getattr(config, 'provenances', ({'link': ''},))
        setattr(config, 'provenances', value)

        # Add relation when adding internal link for data provenance
        new_links = []
        portal_url = getToolByName(instance, 'portal_url')()
        if value == ({},):
            value = ({'link': ''},)
        for val in value:
            if val.get('link').startswith(portal_url):
                source_obj = self.getRelation(instance, val['link'])
                if source_obj:
                    relatedItems = source_obj.getRelatedItems()
                    relatedItems.append(instance)
                    source_obj.setRelatedItems(relatedItems)
                new_links.append(val['link'])

        # Delete the relation if the internal link was removed
        for val in original_values:
            if (not val.get('link') in new_links) and \
                                   val['link'].startswith(portal_url):
                source_obj = self.getRelation(instance, val['link'])
                if source_obj:
                    relatedItems = source_obj.getRelatedItems()
                    if instance in relatedItems:
                        relatedItems.remove(instance)
                    source_obj.setRelatedItems(relatedItems)

    def getRelation(self, instance, path=None):
        """ Extract the relation object
        """
        portal_url = getToolByName(instance, 'portal_url')
        path = path.replace(portal_url(), '', 1)
        site = portal_url.getPortalObject().absolute_url(1)
        if site and (not path.startswith(site)):
            path = site + path
        path = path[1:]

        try:
            referer = instance.restrictedTraverse(path)
        except Exception:
            logger.info('Relation object not found: %s', path)
            return None

        if IBaseObject.providedBy(referer):
            return referer

        path = '/'.join(path.split('/')[:-1])

        return self.getRelation(instance, path)

class DavizBooleanField(ExtensionField, BooleanField):
    """ BooleanField for schema extender
    """
    def get(self, instance, **kwargs):
        """ check if provenance info is inherited or not
        """
        config = queryAdapter(instance, IMultiDataProvenance)
        return getattr(config, 'isInheritedProvenance', False)

SCHEMA = Schema((
    DavizReferenceField('relatedItems',
        schemata="data input",
        relationship='relatesTo',
        multiValued=True,
        widget=EEAReferenceBrowserWidget(
            label=_("Find and reuse existing data"),
            description=_(u"Look for compatible datasets in catalogue"
                " (e.g. visualization data, .tsv, .csv, SPARQL, etc)"
            ),
            i18n_domain="eea",
            visible={'edit': 'visible', 'view': 'invisible' }
        )),
    StringField('quickUpload',
        schemata='data input',
        widget=QuickUploadWidget(
            label=_('Upload CSV/TSV data files from your computer'),
            description=_(u"upload-csv-description", default=(
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
            visible={'edit': 'visible', 'view': 'invisible' }
        )
    ),
    DavizStringField('spreadsheet',
        schemata='data input',
        validators=('csvfile',),
        widget=TextAreaWidget(
            label=_('Copy and paste a data table from a file/webpage'),
            description=_(u"copy-paste-description", default=(
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
        helper_js=(
            '++resource++eea.daviz.common.js',
            '++resource++eea.daviz.spreadsheet.js',),
        helper_css=(
            '++resource++eea.daviz.common.css',
            '++resource++eea.daviz.spreadsheet.css',),
        visible={'edit': 'visible', 'view': 'invisible'}
        )
    ),
    DavizUrlField('external',
        schemata="data input",
        validators=('externalURL',),
        widget=StringWidget(
            label=_(u"Add data from URL"),
            description=_(u"Add a data URL which returns CSV/TSV, "
                          "standard JSON, Exhibit JSON or Google Spreadsheet")
        ),
        i18n_domain="eea",
        visible={'edit': 'visible', 'view': 'invisible'}
    ),
    StringField('dataWarning',
        schemata='data input',
        widget=LabelWidget(
            label=_('Warning'),
            description=_(u"Changing data sources may break existing "
                    "visualizations for this context. You should consider "
                    "creating a new Visualization rather than changing this "
                    "one if the new data is different than the existing one. "
                    "Are you sure you want to continue?"
            ),
            i18n_domain="eea",
            visible={'edit': 'visible', 'view': 'invisible'}
        )
    ),
    DavizDataField('dataTitle', alias="title",
        schemata='default',
        widget=StringWidget(
            label=_("Data source title"),
            description=_("Specify data source"),
            i18n_domain="eea",
            visible={'edit': 'invisible', 'view': 'invisible'}
        ),
    ),
    DavizDataField('dataLink', alias="link",
        schemata='default',
        widget=StringWidget(
            label=_("Data source link"),
            description=_("Specify data source link"),
            i18n_domain="eea",
            visible={'edit': 'invisible', 'view': 'invisible'}
        )
    ),
    DavizDataField('dataOwner', alias="owner",
        schemata='default',
        vocabulary_factory=OrganisationsVocabulary,
        widget=OrganisationsWidget(
            label=_("Data source Organisation"),
            description=_("Specify data source Organisation"),
            i18n_domain="eea",
            visible={'edit': 'invisible', 'view': 'invisible'}
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
        if field.schemata == 'data input':
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
    schema.moveField('spreadsheet', pos=0)
    schema.moveField('quickUpload', after="spreadsheet")
    schema.moveField('external', after="quickUpload")
    schema.moveField('relatedItems', after="external")

finalizeSchema(DAVIZ_SCHEMA)


class MultiDataProvenanceSchemaExtender(object):
    """ Schema extender for content types with data provenance
    """
    implements(ISchemaExtender)
    fields = (
        DavizDataGridField(
            name='provenances',
            schemata='Data Provenance',
            searchable=False,
            widget=DataGridWidget(
                label="Data Provenance",
                description="""List of Data Provenance""",
                columns={'title':Column("Title"),
                         'link':Column("Link"),
                         'owner':OwnerColumn,
                         },
                auto_insert=False,
                i18n_domain='eea',
                helper_js=widget_helper_js,
                helper_css=('++resource++eea.daviz.datasource.css',
                            'datagridwidget.css')
                ),
            columns=("title", "link", "owner"),
        ),
        DavizBooleanField(
            name='inheritedprovenance',
            schemata='Data Provenance',
            searchable=False,
            widget=BooleanWidget(
                label='Inherited Provenance',
                description= 'Inherited Provenance',
            )
        ),

    )


    def __init__(self, context):
        self.context = context

    def getFields(self):
        """ Returns provenance list field
        """
        return self.fields

