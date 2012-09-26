""" Testing
"""
from plone.testing import z2
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import FunctionalTesting

class EEAFixture(PloneSandboxLayer):
    """ EEA Testing Policy
    """
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """ Setup Zope
        """
        import eea.daviz
        self.loadZCML(package=eea.daviz)
        z2.installProduct(app, 'eea.daviz')
        z2.installProduct(app, 'eea.sparql')

    def tearDownZope(self, app):
        """ Uninstall Zope
        """
        z2.uninstallProduct(app, 'eea.daviz')
        z2.uninstallProduct(app, 'eea.sparql')

    def setUpPloneSite(self, portal):
        """ Setup Plone
        """
        applyProfile(portal, 'eea.daviz:default')

        # Login as manager
        setRoles(portal, TEST_USER_ID, ['Manager'])

EEAFIXTURE = EEAFixture()
FUNCTIONAL_TESTING = FunctionalTesting(bases=(EEAFIXTURE,),
                                       name='EEADaviz:Functional')
