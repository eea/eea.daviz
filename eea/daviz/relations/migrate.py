"""Migration for daviz/eea.relations integration
"""
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from zope.annotation.interfaces import IAnnotations
from StringIO import StringIO
import logging

logger = logging.getLogger("eea.daviz.relations")
    

class MigrateRelations(BrowserView):
    """A page that will migrate unsorted relations to sorted
    """
    out = None

    def log(self, msg):
        """Logging
        """

        print >> self.out, msg
        logger.info(msg)

    def __call__(self):
        """ Call
        """
        self.out = StringIO()
        catalog = getToolByName(self.context, 'portal_catalog')

        types = ['AssessmentPart']

        self.log("Started migration of daviz relations")
        self.log("Will migrate the following types: %s" % 
                        ", ".join(types))

        for _type in types:
            brains = catalog.searchResults(portal_type=_type)
            self.log("Starting to migrate %s objects of type: %s" % \
                        (len(brains), _type))
            for brain in brains:
                obj = brain.getObject()
                annot = IAnnotations(obj)
                if "DAVIZ_CHARTS" not in annot:
                    continue

                container = annot['DAVIZ_CHARTS']

                if container.has_key('live'):
                    for chart_id in container.pop('live'):
                        container[chart_id] = 'live'

                if container.has_key('preview'):
                    for chart_id in container.pop('preview'):
                        container[chart_id] = 'preview'

                self.log("Migrated daviz relations for %s" % obj.absolute_url())

            self.log("Done migrating all objects of type: %s" % _type)
            
        self.log("Finished migration of daviz relations")

        self.out.seek(0)
        return self.out.read()
