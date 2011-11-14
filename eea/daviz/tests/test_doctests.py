# -*- coding: utf-8 -*-
""" Test doctests module
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alec Ghica, Alin Voinea"""

import doctest
import unittest
from eea.daviz.tests.base import DavizFunctionalTestCase
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
                  test_class=DavizFunctionalTestCase),
            Suite('docs/app.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.daviz',
                  test_class=DavizFunctionalTestCase),
            Suite('converter/converter.py',
                  optionflags=OPTIONFLAGS,
                  package='eea.daviz',
                  test_class=DavizFunctionalTestCase),
    ))
