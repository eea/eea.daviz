""" Doc tests
"""
import doctest
import unittest
from eea.daviz.tests.base import FUNCTIONAL_TESTING
from plone.testing import layered

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

def test_suite():
    """ Suite
    """
    suite = unittest.TestSuite()
    suite.addTests([
        layered(
            doctest.DocFileSuite(
                'data/source.py',
                optionflags=OPTIONFLAGS,
                package='eea.daviz'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'README.txt',
                optionflags=OPTIONFLAGS,
                package='eea.daviz'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'docs/converter.txt',
                optionflags=OPTIONFLAGS,
                package='eea.daviz'),
            layer=FUNCTIONAL_TESTING),
        layered(
            doctest.DocFileSuite(
                'docs/app.txt',
                optionflags=OPTIONFLAGS,
                package='eea.daviz'),
            layer=FUNCTIONAL_TESTING),
    ])
    return suite
