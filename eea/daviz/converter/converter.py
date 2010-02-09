# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'

import csv
import logging
from itertools import izip
from StringIO import StringIO

from zope.component import adapts
from zope.interface import implements, alsoProvides
from zope.app.annotation.interfaces import IAnnotations

from interfaces import IExhibitJsonConverter
from eea.daviz.interfaces import IExhibitJson
from eea.daviz.config import ANNO_JSON

logger = logging.getLogger('eea.daviz.converter')
info = logger.info

class ExhibitJsonConverter(object):
    """ Converts context data to JSON and save the output under annotations.
    """

    implements(IExhibitJsonConverter)
    adapts(IExhibitJson)

    def __init__(self, context):
        """ Initialize adapter. """
        self.context = context
        annotations = IAnnotations(context)

        # Exhibit JSON
        annotations[ANNO_JSON] = self.getJsonData()

    def getExhibitJson(self):
        """ Get Exhibit JSON. """
        annotations = IAnnotations(self.context)
        return annotations.get(ANNO_JSON)

    def setExhibitJson(self, value):
        """ Set Exhibit JSON. """
        annotations = IAnnotations(self.context)
        annotations[ANNO_JSON] = value

    exhibitjson = property(getExhibitJson, setExhibitJson)

    def getJsonData(self):
        """ Returns JSON output after converting source data. """
        #TODO: in the first sprint will convert only CSV (comma separated) files
        #      to JSON, in a future sprint a converter from more formats to
        #      JSON will be implemented (e.g. Babel)

        columns = []
        out = []

        try:
            data = StringIO(self.context.getFile().data)
            reader = csv.reader(data, delimiter=',')
            for row in reader:
                # Ignore empty rows
                if row == []:
                    continue

                # Get column headers
                if columns == []:
                    columns = row
                    continue

                # Create JSON
                row = iter(row)
                data = {}
                for index, col in enumerate(columns):
                    # Required by exhibit
                    text = row.next()
                    if index == 0:
                        data['label'] = text
                        continue
                    # Multiple values
                    if ';' in text:
                        text = text.split(';')
                    data[col.replace(' ', '+')] = text
                out.append(data)

        except Exception, err:
            # Convertion failed
            logger.exception('Failed to convert %s: %s', self.context.absolute_url(1), err)

        return out

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
