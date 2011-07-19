# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alec Ghica"""

import logging
import csv
from zope.interface import implements
from interfaces import IExhibitJsonConverter

logger = logging.getLogger("eea.daviz.converter")

class EEADialectTab(csv.Dialect):
    """ CSV dialect having tab as delimiter """
    delimiter = '\t'
    quotechar = '"'
    # Should be set to quotechar = csv.QUOTE_NONE when we will use Python 2.5
    # as setting quotechar to nothing does not work in Python 2.4. For more details see
    # http://stackoverflow.com/questions/494054/how-can-i-disable-quoting-in-the-python-2-4-csv-reader/494126
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

    def text2list(self, key, value):
        """ Detect lists
        """
        if ":list" not in key:
            return value

        if "," in value:
            value = value.split(",")
        elif ";" in value:
            value = value.split(";")
        else:
            value = [value,]
        return value

    def text2number(self, key, value):
        """ Detect numbers
        """
        if ":number" not in key:
            return value

        try:
            value = int(value)
        except Exception:
            try:
                value = float(value)
            except Exception, err:
                logger.debug(err)
        return value

    def text2boolean(self, key, value):
        """ Detect boolean
        """
        if ":boolean" not in key:
            return value

        try:
            value = bool(value)
        except Exception, err:
            logger.debug(err)
        return value

    def column_type(self, column):
        """ Get column and type from column

            >>> ExhibitJsonConverter().column_type("start:date")
            ("start", "date")

            >>> ExhibitJsonConverter().column_type("Website:url")
            ("Website", "url")

            >>> ExhibitJsonConverter().column_type("Items: one, two:list")
            ("Items: one, two", "list")

            >>> ExhibitJsonConverter().column_type("Title")
            ("Title", "text")

        """

        if ":" not in column:
            return column, "text"

        typo = column.split(":")[-1]
        column = ":".join(column.split(":")[:-1])
        return column, typo

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
                for name in row:
                    name = name.replace(' ', '+')
                    if name.lower().endswith('label'):
                        name = "label"
                        hasLabel = True
                    columns.append(name)
                continue

            # Create JSON
            row = iter(row)
            data = {}

            # Required by Exhibit
            if not hasLabel:
                data['label'] = index

            for col in columns:
                text = row.next()

                text = self.text2list(col, text)
                text = self.text2number(col, text)
                text = self.text2boolean(col, text)

                col, _type = self.column_type(col)
                data[col] = text

            out.append(data)

        columns = (self.column_type(col) for col in columns)
        return columns, {'items': out}
