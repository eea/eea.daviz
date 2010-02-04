# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'

import csv
import logging
from itertools import izip

from zope.component import adapts
from zope.interface import implements, alsoProvides
from zope.app.annotation.interfaces import IAnnotations

from interfaces import IExhibitJsonConverter
from eea.daviz.interfaces import IExhibitJson

logger = logging.getLogger('eea.daviz.converter')
info = logger.info

EXHIBITJSON = ['exhibit_json']

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
        annotations[EXHIBITJSON] = self.getJsonData()

    def getExhibitJson(self):
        """ Get Exhibit JSON. """
        annotations = IAnnotations(self.context)
        return annotations.get(EXHIBITJSON)

    def setExhibitJson(self, value):
        """ Set Exhibit JSON. """
        annotations = IAnnotations(self.context)
        annotations[EXHIBITJSON] = value

    exhibitjson = property(getExhibitJson, setExhibitJson)

    def getJsonData(self):
        """ Returns JSON output after converting source data. """
        #TODO: in the first sprint will convert only CSV (comma separated) files
        #      to JSON, in a future sprint a converter from more formats to
        #      JSON will be implemented (e.g. Babel)

        columns = []
        out = []

        try:
            reader = csv.reader(self.context.getFile().data, delimiter=',')
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
                for col in columns:
                        data[col] = row.next()
                out += [data]
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
