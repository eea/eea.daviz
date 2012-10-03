""" Various setup
"""
import logging
logger = logging.getLogger('eea.daviz')
from Products.CMFCore.utils import getToolByName

def importVarious(self):
    """ Various setup
    """
    if self.readDataFile('eea.daviz.txt') is None:
        return

    site = self.getSite()
    st = getToolByName(site, "portal_setup")
    st.runAllImportStepsFromProfile("profile-eea.relations:default")
    st.runAllImportStepsFromProfile("profile-eea.depiction:default")
