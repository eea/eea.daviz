# -*- coding: utf-8 -*-
""" Basic layer for daviz edit views
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alin Voinea"""

from zope.component import queryAdapter
from zope.formlib.form import SubPageForm
from Products.statusmessages.interfaces import IStatusMessage
from zope.formlib.form import action, setUpWidgets, haveInputWidgets
from eea.daviz.interfaces import IDavizConfig

from zope.i18nmessageid import MessageFactory
_ = MessageFactory("eea.daviz")

class EditForm(SubPageForm):
    """
    Basic layer to edit daviz views. For more details on how to use this,
    see implementation in eea.daviz.views.map.edit.Edit.

    Assign these attributes in your subclass:
      - form_fields: Fields(Interface)

    """
    form_fields = None

    def __init__(self, context, request):
        """ EditForm init
        """
        super(EditForm, self).__init__(context, request)
        name = self.__name__
        if isinstance(name, unicode):
            name = name.encode('utf-8')
        self.prefix = name.replace('.edit', '', 1)

    @property
    def _data(self):
        """ Return view
        """
        accessor = queryAdapter(self.context, IDavizConfig)
        return accessor.view(self.prefix, {})

    def setUpWidgets(self, ignore_request=False):
        """ Sets up widgets
        """
        self.adapters = {}
        self.widgets = setUpWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            form=self, data=self._data, adapters=self.adapters,
            ignore_request=ignore_request)

    @action(_('Save'), condition=haveInputWidgets)
    def save(self, saction, data):
        """ Handle save action
        """
        mutator = queryAdapter(self.context, IDavizConfig)
        mutator.edit_view(self.prefix, **data)

        name = saction.__name__.encode('utf-8')
        value = self.request.form.get(name, '')
        if value == 'ajax':
            return 'Changes saved'
        return self.nextUrl

    @property
    def nextUrl(self):
        """ Redirect to daviz-edit.html as next_url
        """
        IStatusMessage(self.request).addStatusMessage('Changes saved',
                                                        type='info')
        next_url = self.context.absolute_url() + '/daviz-edit.html'
        self.request.response.redirect(next_url)
