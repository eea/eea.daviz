""" Edit Form for Facetds
"""
from zope.component import queryAdapter
from zope.formlib.form import SubPageForm
from Products.statusmessages.interfaces import IStatusMessage
from zope.formlib.form import action as formAction
from zope.formlib.form import setUpWidgets, haveInputWidgets
from eea.daviz.interfaces import IDavizConfig

from zope.i18nmessageid import MessageFactory
_ = MessageFactory("eea.daviz")

class EditForm(SubPageForm):
    """
    Basic layer to edit daviz facets. For more details on how to use this,
    see implementation in eea.daviz.facets.list.edit.Edit.

    Assign these attributes in your subclass:
      - form_fields: Fields(Interface)

    """
    form_fields = None
    _prefix = ''

    def __init__(self, context, request):
        super(EditForm, self).__init__(context, request)
        for key in self.request.form:
            if key.endswith('.label'):
                self._prefix = key.split('.')[0]
                break

    def getPrefix(self):
        """ Form prefix getter
        """
        return self._prefix

    def setPrefix(self, value):
        """ Form prefix setter
        """
        self._prefix = value

    prefix = property(getPrefix, setPrefix)

    @property
    def label(self):
        """ Label
        """
        return self.prefix

    @property
    def _data(self):
        """ Form data
        """
        accessor = queryAdapter(self.context, IDavizConfig)
        return accessor.facet(self.prefix, {})

    def setUpWidgets(self, ignore_request=False):
        """ Setup form widgets
        """
        self.adapters = {}
        self.widgets = setUpWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            form=self, data=self._data, adapters=self.adapters,
            ignore_request=ignore_request)

    @formAction(_('Save'), condition=haveInputWidgets)
    def save(self, action, data):
        """ Handle save action
        """
        mutator = queryAdapter(self.context, IDavizConfig)
        mutator.edit_facet(self.prefix, **data)

        name = action.__name__.encode('utf-8')
        value = self.request.form.get(name, '')
        if value == 'ajax':
            return 'Changes saved'
        return self.nextUrl

    @property
    def nextUrl(self):
        """ Next URL
        """
        IStatusMessage(self.request).addStatusMessage(
            'Changes saved', type='info')
        to = self.context.absolute_url() + '/daviz-edit.html'
        self.request.response.redirect(to)
