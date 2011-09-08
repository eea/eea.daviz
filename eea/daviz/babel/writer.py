""" Babel Writter
"""
import json
from zope.interface import implements
from eea.daviz.babel.interfaces import IBabelWriter

class JSONP(object):
    """ exhibit-jsonp babel writer
    """
    implements(IBabelWriter)

    def strip(self, text):
        """ Strip url from text
        """
        if not text.startswith('http'):
            return text

        output = text.split("/")[-1]
        output = output.split("#")[-1]
        return output

    def fix_types(self, items):
        """ Exhibit JSON item should have only one type
        """
        for item in items:
            typo = item.get('type', u'')
            if isinstance(typo, (str, unicode)):
                continue

            typo.sort()
            new = [t for t in typo if not t.startswith('http')]
            if new:
                item['type'] = new[0]
                continue

            new = typo[0]
            item['type'] = self.strip(new)

        return items

    def __call__(self, items, **kwargs):
        kwargs['items'] = self.fix_types(items)
        return json.dumps(kwargs, indent=2)
