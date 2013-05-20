""" Daviz Visualization
"""
from Products.ATContentTypes.content.folder import ATFolder
from eea.daviz.content import schema as daviz_schema
from eea.daviz.content.events import DavizWillBeRemovedEvent
from eea.daviz.content.interfaces import IDavizVisualization
from zope.event import notify
from zope.interface import implements


class DavizVisualization(ATFolder):
    """ Daviz Visualization
    """
    implements(IDavizVisualization)

    meta_type = 'DavizVisualization'
    portal_type = 'DavizVisualization'
    archetype_name = 'DavizVisualization'

    schema = daviz_schema.DAVIZ_SCHEMA

    def manage_beforeDelete(self, item, container):
        """Override manage_beforeDelete to be able to catch the
        proper backreferences. We could not use ObjectWillBeRemovedEvent
        because there's an override in Archetypes.Referenceble
        that will remove all relations and we need them
        """

        #only trigger event once, at the end, when dealing
        #with plone.app.linkintegrity
        if self.REQUEST.getURL().endswith('delete_confirmation'):
            #delete has been confirmed
            if self.REQUEST.form.get('_authenticator') and \
                not self.REQUEST.form.get('form.submitted'):
                notify(DavizWillBeRemovedEvent(self))
        else:
            notify(DavizWillBeRemovedEvent(self))

        super(DavizVisualization, self).manage_beforeDelete(item, container)
