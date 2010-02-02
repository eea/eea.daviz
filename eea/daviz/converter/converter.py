# -*- coding: utf-8 -*-

__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'

from zope.component import adapts
from zope.interface import implements, alsoProvides
from zope.app.annotation.interfaces import IAnnotations

from interfaces import IExhibitJson, IExhibitJsonConverter


EXHIBITJSON = ['exhibit_json']

class ExhibitJsonConverter(object):
    """ Converts context data to Json and save the output under annotations.
    """

    implements(IExhibitJsonConverter)
    adapts(IExhibitJson)

    def __init__(self, context):
        """ Initialize adapter. """
        self.context = context
        annotations = IAnnotations(context)

        # Exhibit Json
        annotations[EXHIBITJSON] = self.getJsonData()

    def getExhibitJson(self):
        """ Get Exhibit Json. """
        annotations = IAnnotations(self.context)
        return annotations.get(EXHIBITJSON)

    def setExhibitJson(self, value):
        """ Set Exhibit Json. """
        annotations = IAnnotations(self.context)
        annotations[EXHIBITJSON] = value

    exhibitjson = property(getExhibitJson, setExhibitJson)

    def getJsonData(self):
        """ Returns Json output after converting source data. """
        #TODO: in the first sprint will convert only CSV files to Json,
        #      in a future sprint a converter from any suported format to
        #      Json will be implemented (e.g. Babel)

        #TODO: returns just some data for test, replace this with CSV to Json convertion
        output = """
{
	"items" :      [
		{
			"AxisUnits" :                 "Meters",
			"Projection" :                "Lambert Azimutal",
			"Name" :                      "Lambert Azimutal",
			"LatituteProjectionCenter" :  [
				"48&#176",
				"00\'00\'\'"
			],
			"LongituteProjectionCenter" : [
				"09&#176",
				"00\'00\'\'"
			],
			"FalseEasting" :              0,
			"type" :                      "Item",
			"FalseNorthing" :             0,
			"projectionGID" :             "2F971D88-35D9-440D-961B-B5B656C5436D",
			"Ellipsoid" :                 "Sphere: radius 6378388",
			"label" :                     "3",
			"SemiMajorAxis" :             6378388
		}
	],
	"properties" : {
		"SemiMajorAxis" : {
			"valueType" : "number"
		},
		"FalseNorthing" : {
			"valueType" : "number"
		},
		"FalseEasting" :  {
			"valueType" : "number"
		}
	}
}
        """
        return output

class JsonOutput(object):
    """ Generate and set Json export.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        # Set marker interface
        if not IExhibitJson.providedBy(self.context):
            alsoProvides(self.context, IExhibitJson)

        # Adapt to Exhibit Json
        exhibitadaptor = IExhibitJsonConverter(self.context)

        #TODO: implement fucntionality to make public or not the json output
        return 'Json convertion uploaded.'
