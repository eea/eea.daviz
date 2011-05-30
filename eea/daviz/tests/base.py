# -*- coding: utf-8 -*-
""" Base tests module
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alec Ghica, Alin Voinea"""

import os
from StringIO import StringIO
from App.Common import package_home
from cgi import FieldStorage
from ZPublisher.HTTPRequest import FileUpload
from Products.Five import zcml
from Products.Five import fiveconfigure
product_globals = globals()

# Import PloneTestCase - this registers more products with Zope as a side effect
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup


@onsetup
def setup_eea_daviz():
    """Set up the additional products.

    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer.
    """
    fiveconfigure.debug_mode = True
    import Products.Five
    zcml.load_config('meta.zcml', Products.Five)

    import eea.daviz
    zcml.load_config('configure.zcml', eea.daviz)
    fiveconfigure.debug_mode = False

    ptc.installProduct('Five')

setup_eea_daviz()
ptc.setupPloneSite()

class DavizTestCase(ptc.PloneTestCase):
    """ Base class for integration tests for the 'DaViz' product.
    """

class DavizFunctionalTestCase(ptc.FunctionalTestCase, DavizTestCase):
    """ Base class for functional integration tests for the 'DaViz' product.
    """
    def loadfile(self, rel_filename, ctype='text/xml', zope=False):
        """ Loads a file
        """
        home = package_home(product_globals)
        filename = os.path.sep.join([home, rel_filename])
        data = open(filename, 'r').read()

        fp = StringIO(data)
        fp.seek(0)

        if not zope:
            return fp

        header_filename = rel_filename.split('/')[-1]
        env = {'REQUEST_METHOD':'PUT'}
        headers = {'content-type' : ctype,
                   'content-length': len(data),
                   'content-disposition':'attachment; filename=%s'
                                                % header_filename}

        fs = FieldStorage(fp=fp, environ=env, headers=headers)
        return FileUpload(fs)
