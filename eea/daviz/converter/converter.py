# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Alec Ghica"""

import csv
import logging
from zope.event import notify
from itertools import izip
from StringIO import StringIO

from zope.component import adapts
from zope.interface import implements, alsoProvides
try:
    from zope.annotation.interfaces import IAnnotations
except ImportError:
    #BBB Plone 2.5
    from zope.app.annotation.interfaces import IAnnotations

from interfaces import IExhibitJsonConverter
from eea.daviz.interfaces import IExhibitJson
from eea.daviz.config import ANNO_JSON
from eea.daviz.events import DavizEnabledEvent

logger = logging.getLogger('eea.daviz.converter')
info = logger.info

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
    """ Converts context data to JSON and save the output under annotations.
    """

    implements(IExhibitJsonConverter)
    adapts(IExhibitJson)

    def __init__(self, context):
        """ Initialize adapter. """
        self.context = context
        self.updateJsonData()

    def getExhibitJson(self):
        """ Get Exhibit JSON. """
        annotations = IAnnotations(self.context)
        return annotations.get(ANNO_JSON)

    def setExhibitJson(self, value):
        """ Set Exhibit JSON. """
        annotations = IAnnotations(self.context)
        annotations[ANNO_JSON] = value

    exhibitjson = property(getExhibitJson, setExhibitJson)

    def updateJsonData(self):
        """ Returns JSON output after converting source data. """
        #TODO: in the first sprint will convert only CSV (comma separated) files
        #      to JSON, in a future sprint a converter from more formats to
        #      JSON will be implemented (e.g. Babel)

        columns = []
        hasLabel = False
        out = []

        try:
            data = StringIO(self.context.getFile().data)
            reader = csv.reader(data, dialect='eea-tab')
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
                    # Multiple values
                    if ';' in text:
                        text = text.split(';')
                    data[col] = text
                out.append(data)

        except Exception, err:
            # Convertion failed
            logger.exception('Failed to convert %s: %s', self.context.absolute_url(1), err)
            return

        # Update annotations
        annotations = IAnnotations(self.context)
        annotations[ANNO_JSON] = out
        notify(DavizEnabledEvent(self.context, columns=columns))

class JsonOutput(object):
    """ Generate and set JSON export.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        # Set marker interface
        if not IExhibitJson.providedBy(self.context):
            alsoProvides(self.context, IExhibitJson)

        # Adapt to Exhibit JSON
        exhibitadaptor = IExhibitJsonConverter(self.context)
        json_output = exhibitadaptor.getExhibitJson()

        msg = """<h3>JSON convertion done.</h3>
                  <strong>JSON output:</strong><br />
                  %s
              """ % json_output
        if not json_output:
            msg = """<h3>JSON convertion failed, empty output.</h3>"""
        return msg
