from zope.component import queryUtility
from plone.app.registry.browser import controlpanel
from plone.registry.interfaces import IRegistry
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from z3c.form import button

from eea.daviz.interfaces import IDavizSettings

class DavizSettingsEditForm(controlpanel.RegistryEditForm):
    schema = IDavizSettings
    id = "DavizSettingsEditForm"
    label = "Daviz settings"
    description = "Daviz settings"

class DavizSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = DavizSettingsEditForm
    index = ViewPageTemplateFile('../zpt/controlpanel.pt')

    def settings(self):
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IDavizSettings, check=False)

        return settings.defaultFolder