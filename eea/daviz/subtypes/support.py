""" Module to enable or disable visualization
"""
from zope.component import queryMultiAdapter
from eea.app.visualization.subtypes.support import DavizPublicSupport

class DavizVisualizationSupport(DavizPublicSupport):
    """ Enable/Disable visualization
    """
    @property
    def can_edit(self):
        """ Can edit visualization
        """
        # Is locked
        locked = queryMultiAdapter((self.context, self.request),
                                      name=u'plone_lock_info')
        locked = getattr(locked, 'is_locked_for_current_user', lambda: False)

        if locked():
            return False

        return True

    @property
    def is_visualization(self):
        """ Is visualization enabled?
        """
        return True
