# -*- coding: utf-8 -*-
""" Converter module responsible for converting from cvs to json
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alec Ghica"""

import re
import logging
import csv
from zope.interface import implements
from eea.daviz.converter.interfaces import IExhibitJsonConverter
from Products.CMFPlone.utils import normalizeString

logger = logging.getLogger("eea.daviz.converter")
REGEX = re.compile(r"[\W]+")

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

        >>> from zope.component import getUtility
        >>> from eea.daviz.interfaces import IExhibitJsonConverter

        >>> converter = getUtility(IExhibitJsonConverter)
        >>> converter
        <eea.daviz.converter.converter.ExhibitJsonConverter object at ...>

    """
    implements(IExhibitJsonConverter)

    def text2list(self, key, value):
        """ Detect lists in value

            Works with ","
            >>> converter.text2list("animals:list", "Pig, Goat, Cow")
            ['Pig', 'Goat', 'Cow']

            Also with ";"
            >>> converter.text2list("animals:List", "Pig; Goat; Cow")
            ['Pig', 'Goat', 'Cow']

            If it can't find any comma or semicolon it will return a list of one
            item
            >>> converter.text2list("animals:LIST", "Pig")
            ['Pig']

            It will not work if you don't specify :list type in the key
            >>> converter.text2list("animals", "Pig, Goat, Cow")
            'Pig, Goat, Cow'

        """
        if ":list" not in key.lower():
            return value

        if "," in value:
            value = value.split(",")
        elif ";" in value:
            value = value.split(";")
        else:
            value = [value, ]

        value = [item.strip() for item in value]
        return value

    def text2number(self, key, value):
        """ Detect numbers in value

            >>> converter.text2number("year:number", "2010")
            2010

            >>> converter.text2number("year:NUMBER", "2011")
            2011

            >>> converter.text2number("price:Number", "9.99")
            9.9...

            It fails silently if the provided value is not a number
            >>> converter.text2number("phone:number", "9-99")
            '9-99'

            It will not work if you don't provide :number type in the key
            >>> converter.text2number("price", "9.99")
            '9.99'

        """
        if ":number" not in key.lower():
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
        """ Detect boolean in string

            >>> converter.text2boolean("year:boolean", "2011")
            True

            >>> converter.text2boolean("year:BOOLEAN", "2011")
            True

            Be carefull, "False" is a True in python as it's not an emtry string
            >>> converter.text2boolean("year:Boolean", "False")
            True

            So use :bool only when you test if value is empty or not
            >>> converter.text2boolean("year:boolean", "")
            False

            It will not work if you don't specify :boolean type in the key
            >>> converter.text2boolean("year", "2345")
            '2345'

        """
        if ":boolean" not in key.lower():
            return value

        try:
            value = bool(value)
        except Exception, err:
            logger.debug(err)
        return value

    def column_type(self, column):
        """ Get column and type from column

            >>> converter.column_type("start:Date")
            ('start', 'date')

            >>> converter.column_type("Website:URL")
            ('website', 'url')

            >>> converter.column_type("Items: one, two:List")
            ('items_one_two', 'list')

            >>> converter.column_type("Title")
            ('title', 'text')

            >>> converter.column_type("Title is some-thing. + something @lse")
            ('title_is_some_thing_something_lse', 'text')

        """

        if ":" not in column:
            column = normalizeString(column, encoding='utf-8')
            column = REGEX.sub('_', column)
            return column, "text"

        typo = column.split(":")[-1].lower()
        column = ":".join(column.split(":")[:-1])
        column = normalizeString(column, encoding='utf-8')
        column = REGEX.sub('_', column)
        return column, typo

    def __call__(self, datafile):
        """
        Returns: columns_headers_with_type, exhibit_dict:

          ( <generator
              (('label', 'text'), ('year', 'text'), ('country', 'text'))>,

            {'items': [
                {'country': 'Romania', 'year': '2010', 'label': 'romania'},
              ],
             'properties': {
               'country': {'valueType': 'text'},
               'year': {'valueType': 'text'},
               'label': {'valueType': 'text'}
              }
            }
          )

        Let's see how it works:

          CSV

            >>> csvfile = '\n'.join((
            ...   'label, year, country',
            ...   'romania, 2010, Romania',
            ... ))

            >>> from StringIO import StringIO
            >>> csvfile = StringIO(csvfile)
            >>> columns, jsondict = converter(csvfile)

            >>> [x for x in columns]
            [('label', 'text'), ('year', 'text'), ('country', 'text')]

            >>> jsondict['properties']['year']
            {'valueType': 'text'}

          TSV

            >>> tabfile = '\n'.join((
            ...   'label \t year:number \t country',
            ...   'romania \t 2010 \t Romania',
            ... ))
            >>> tabfile = StringIO(tabfile)
            >>> columns, jsondict = converter(tabfile)
            >>> [x for x in columns]
            [('label', 'text'), ('year', 'number'), ('country', 'text')]

            >>> jsondict['properties']['year']
            {'valueType': 'number'}

        """

        columns = []
        hasLabel = False
        out = []
        properties = {}

        sniffer = csv.Sniffer()
        try:
            dialect = sniffer.sniff(datafile.read(1024))
        except Exception, err:
            logger.debug(err)
            dialect = 'eea-tab'

        datafile.seek(0)
        reader = csv.reader(datafile, dialect=dialect)
        for index, row in enumerate(reader):
            # Ignore empty rows
            if row == []:
                continue

            # Get column headers
            if columns == []:
                for name in row:
                    name = name.strip()
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
                properties[col] = {"valueType": _type}

            out.append(data)

        columns = (self.column_type(col) for col in columns)
        return columns, {'items': out, 'properties': properties}
