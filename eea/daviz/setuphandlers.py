""" Various setup
"""
import logging
from Products.CMFCore.utils import getToolByName

logger = logging.getLogger('eea.daviz')

def importVarious(self):
    """ Various setup
    """
    if self.readDataFile('eea.daviz.txt') is None:
        return

    site = self.getSite()
    st = getToolByName(site, "portal_setup")
    st.runAllImportStepsFromProfile("profile-eea.relations:default")
    st.runAllImportStepsFromProfile("profile-eea.depiction:default")
