""" Doc tests
"""
import doctest
import unittest
from base import DavizFunctionalTestCase
from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)


def test_suite():
    """ Suite
    """
    return unittest.TestSuite((
            Suite('docs/converter.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.daviz',
                  test_class=DavizFunctionalTestCase) ,
              ))
