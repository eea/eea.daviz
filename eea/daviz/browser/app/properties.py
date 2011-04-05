""" Exhibit properties
"""
import logging
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
    json = schema.Text(
        title=u"JSON",
        description=u"Edit generated JSON",
        required=False
    )

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
        }

    def setUpWidgets(self, ignore_request=False):
        """ Setup widgets
        """
        self.adapters = {}
        self.widgets = setUpWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            form=self, data=self._data, adapters=self.adapters,
            ignore_request=ignore_request)

    @formaction(_('Save'), condition=haveInputWidgets)
    def save(self, action, data):
        """ Handle save action
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
        next = self.context.absolute_url() + '/daviz-edit.html'
        self.request.response.redirect(next)
