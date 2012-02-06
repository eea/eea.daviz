""" Exhibit properties
"""
import logging
try:
    import json as simplejson
    simplejson = simplejson # pylint
except ImportError:
    import simplejson
from zope import schema
from zope.interface import Interface
from zope.formlib.form import Fields
from zope.component import queryAdapter
from zope.formlib.form import SubPageForm
from Products.statusmessages.interfaces import IStatusMessage
from zope.formlib.form import action as formaction
from zope.formlib.form import setUpWidgets, haveInputWidgets
from eea.daviz.interfaces import IDavizConfig

from zope.i18nmessageid import MessageFactory

_ = MessageFactory("eea.daviz")
logger = logging.getLogger('eea.daviz')

class IExhibitPropertiesEdit(Interface):
    """ Edit Exhibit global properties
    """
    views = schema.List(
        title=u'Views',
        description=u'Enable exhibit views',
        unique=True,
        value_type=schema.Choice(
            vocabulary="eea.daviz.vocabularies.ViewsVocabulary")
    )
    views.order = 10

    json = schema.Text(
        title=u"JSON",
        description=u"Edit generated JSON",
        required=False
    )
    json.order = 20

    sources = schema.List(
        title=u'Additional sources',
        required=False,
        description=(
            u"Add additional external exhibit sources to be merged. "
            "Supported formats: "
            "'Exhibit JSON', 'Google Spreadsheet' and 'RDF/XML'. "
            "See more details "
            "http://www.simile-widgets.org/wiki/Exhibit/Creating"
            "%2C_Importing%2C_and_Managing_Data#Conversion_at_Load_Time"),
        value_type=schema.TextLine(title=u'URL')
    )
    sources.order = 30

class IDavizPresentationPropertiesEdit(IExhibitPropertiesEdit):
    """ Custom schema for Daviz Presentation
    """
    json = schema.Text(
        title=u"JSON",
        description=u"Edit JSON column types",
        required=False
    )
    json.order = 20

class EditForm(SubPageForm):
    """ Layer to edit daviz properties.
    """
    label = u"Global settings"
    form_fields = Fields(IExhibitPropertiesEdit)

    def __init__(self, context, request):
        super(EditForm, self).__init__(context, request)
        name = self.__name__
        if isinstance(name, unicode):
            name = name.encode('utf-8')
        self.prefix = name.replace('.edit', '', 1)
        self.message = 'Changes saved'

    @property
    def _data(self):
        """ Form data
        """
        accessor = queryAdapter(self.context, IDavizConfig)
        return {
            'name': self.prefix,
            'json': simplejson.dumps(dict(accessor.json), indent=2),
            'views': [view.get('name') for view in accessor.views],
            'sources':
                [source.get('name') for source in accessor.sources],
        }

    def setUpWidgets(self, ignore_request=False):
        """ Setup widgets
        """
        self.adapters = {}
        self.widgets = setUpWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            form=self, data=self._data, adapters=self.adapters,
            ignore_request=ignore_request)

    def handle_json(self, data):
        """ Handle json property
        """
        mutator = queryAdapter(self.context, IDavizConfig)
        json = data.get('json', '{}')
        try:
            json = dict(simplejson.loads(json))
        except Exception, err:
            logger.exception(err)
            self.message = "ERROR: %s" % err
        else:
            mutator.json = json

    def handle_views(self, data):
        """ Handle views property
        """
        mutator = queryAdapter(self.context, IDavizConfig)
        old = mutator.views
        old = dict((view.get('name', ''), dict(view))
                   for view in old)
        mutator.delete_views()

        for key in data.get('views', []):
            properties = old.get(key, {})
            properties.pop('name', None)
            mutator.add_view(name=key, **properties)

    def handle_sources(self, data):
        """ Handle sources property
        """
        mutator = queryAdapter(self.context, IDavizConfig)
        sources = data.get('sources', [])
        sources = set(sources)
        mutator.delete_sources()
        for source in sources:
            source = source.strip()
            if not source:
                continue

            properties = {
                "name": source,
                "converter": "",
                "type": "json"
            }

            if 'google' in source.lower():
                properties['type'] = 'jsonp'
                properties['converter'] = 'googleSpreadsheets'
            elif 'rdfa' in source.lower():
                properties['type'] = 'RDFa'
            elif ('rdf' in source.lower()) or ('xml' in source.lower()):
                properties['type'] = 'rdf+xml'

            mutator.add_source(**properties)

    @formaction(_('Save'), condition=haveInputWidgets)
    def save(self, action, data):
        """ Handle save action
        """
        self.handle_json(data)
        self.handle_views(data)
        self.handle_sources(data)

        # Return
        name = action.__name__.encode('utf-8')
        value = self.request.form.get(name, '')
        if value == 'ajax':
            return self.message
        return self.nextUrl

    @property
    def nextUrl(self):
        """ Next
        """
        IStatusMessage(self.request).addStatusMessage(self.message, type='info')
        next_url = self.context.absolute_url() + '/daviz-edit.html'
        self.request.response.redirect(next_url)

class DavizPresentationEditForm(EditForm):
    """ Custom edit form for DavizPresentation
    """
    form_fields = Fields(IDavizPresentationPropertiesEdit)
