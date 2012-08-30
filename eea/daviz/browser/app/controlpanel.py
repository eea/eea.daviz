""" Daviz controlpanel
"""
from zope.component import queryUtility
from plone.app.registry.browser import controlpanel
from plone.registry.interfaces import IRegistry
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from eea.daviz.interfaces import IDavizSettings

class DavizSettingsEditForm(controlpanel.RegistryEditForm):
    """Daviz settings form
    """
    schema = IDavizSettings
    id = "DavizSettingsEditForm"
    label = "Daviz settings"
    description = "Daviz settings"

class DavizSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    """Daviz settings control panel
    """
    form = DavizSettingsEditForm
    index = ViewPageTemplateFile('../zpt/controlpanel.pt')

    def settings(self):
        """settings
        """
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IDavizSettings, check=False)

        return settings.defaultFolder