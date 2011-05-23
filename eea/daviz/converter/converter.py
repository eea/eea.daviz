# -*- coding: utf-8 -*-
""" Converter module responsible for converting from cvs to json
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alec Ghica"""

import csv
from zope.interface import implements
from eea.daviz.converter.interfaces import IExhibitJsonConverter

class EEADialectTab(csv.Dialect):
    """ CSV dialect having tab as delimiter 
    """
    delimiter = '\t'
    quotechar = '"'
    # Should be set to quotechar = csv.QUOTE_NONE when we will use Python 2.5
    # as setting quotechar to nothing does not work in Python 2.4. 
    # For more details see
    # http://stackoverflow.com/questions/494054/
    # how-can-i-disable-quoting-in-the-python-2-4-csv-reader/494126
    escapechar = '\\'
    doublequote = False
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = csv.QUOTE_NONE

csv.register_dialect("eea-tab", EEADialectTab)

class ExhibitJsonConverter(object):
    """ Utility to convert csv to json
    """
    implements(IExhibitJsonConverter)

    def __call__(self, datafile):
        """ Returns JSON output after converting source data. """
        #TODO: in the first sprint will convert only CSV (tab separated) files
        #      to JSON, in a future sprint a converter from more formats to
        #      JSON will be implemented (e.g. Babel)

        columns = []
        hasLabel = False
        out = []

        reader = csv.reader(datafile, dialect='eea-tab')
        for index, row in enumerate(reader):
            # Ignore empty rows
            if row == []:
                continue

            # Get column headers
            if columns == []:
                columns = [name.replace(' ', '+') for name in row]

                # Required by Exhibit
                hasLabel = bool([x for x in columns if x == 'label'])
                continue

            # Create JSON
            row = iter(row)
            data = {}

            # Required by Exhibit
            if not hasLabel:
                data['label'] = index

            for col in columns:
                text = row.next()

                detected_semicolon = ';' in text
                detected_comma = ',' in text
                detected_delimiter = None

                # Multiple values
                if ':list' in col:
                    if detected_comma:
                        detected_delimiter = ','
                    elif detected_semicolon:
                        detected_delimiter = ';'
                elif detected_semicolon:
                    detected_delimiter = ';'

                if detected_delimiter:
                    text = text.split(detected_delimiter)

                data[col] = text
            out.append(data)

        return columns, {'items': out}
