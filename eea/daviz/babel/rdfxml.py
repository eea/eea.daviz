""" Babel readers
"""
from urlparse import urldefrag
from rdflib import ConjunctiveGraph
from zope.interface import implements
from eea.daviz.babel.interfaces import IBabelReader

class RDFXMLReader(object):
    """ Read from rdf-xml source
    """
    implements(IBabelReader)

    def strip(self, text):
        """ Strip url from text
        """
        if not text.startswith('http'):
            return text

        output = text.split("/")[-1]
        output = output.split("#")[-1]
        return output

    def defrag(self, uri):
        """ Try to guess value from rdflib.URIRef
        """
        url, frag = urldefrag(uri)
        if not frag:
            return url
        return frag

    def __call__(self, url, **kwargs):

        if not url:
            return []

        graph = ConjunctiveGraph()
        graph.parse(url)
        output = {}

        for subject, predicate, context in graph:
            key = self.strip(subject)
            prop = self.strip(predicate)
            value = self.defrag(context)

            output.setdefault(key, {
                'label': key,
                'uri': unicode(subject)
            })

            if prop in output[key]:
                old = output[key][prop]
                if not isinstance(old, list):
                    output[key][prop] = [old]
                output[key][prop].append(value)
            else:
                output[key][prop] = value

        return output.values()
