""" Data controllers
"""
from urllib2 import urlparse
from Products.Five.browser import BrowserView
import re

try:
    from eea.daviz.content.schema import tmpOrganisationsVocabulary
    hasVocab = True
except ImportError:
    hasVocab = False

class Info(BrowserView):
    """ Data source info
    """
    def __init__(self, context, request):
        super(Info, self).__init__(context, request)
        self._info = {}

    @property
    def info(self):
        """ Info
        """
        if not self._info:
            self._info = {
                'provenances': []
            }
        return self._info

    def __call__(self, **kwargs):
        field = self.context.getField('provenances')
        provenances = field.getAccessor(self.context)()
        formatted_provenances = []
        for provenance in provenances:
            title = provenance.get('title', '')
            link = provenance.get('link', '')
            owner = provenance.get('owner', '')
            if title != '' or owner != '' or link != '':
                formatted_provenance = {'source':{}, 'owner':{}}
                formatted_provenance['source']['title'] = title
                formatted_provenance['source']['url'] = link

                if owner != '':
                    if hasVocab:
                        owner_title = tmpOrganisationsVocabulary.\
                            getDisplayList(self.context).getValue(owner)
                        if not owner_title:
                            owner_title = owner
                    else:
                        owner_title = owner
                    formatted_provenance['owner']['title'] = owner_title
                    formatted_provenance['owner']['acronym'] = ""
                    # 21467 extract acronym from owner_title if present
                    # which is found within parenthesis ()
                    acronym = re.search(r'\((.*?)\)', owner_title)
                    if acronym:
                        formatted_provenance['owner']['acronym'] = \
                            acronym.group(1)
                    parser = urlparse.urlparse(owner)
                    if all((parser.scheme, parser.netloc)):
                        formatted_provenance['owner']['url'] = owner
                    else:
                        formatted_provenance['owner']['url'] = link
                formatted_provenances.append(formatted_provenance)

        self.info['provenances'] = formatted_provenances
        return self.info
