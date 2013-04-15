"""Migration for daviz/eea.relations integration
"""
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from zope.annotation.interfaces import IAnnotations
from StringIO import StringIO
from persistent.mapping import PersistentMapping
from zc.dict import OrderedDict
import logging
import transaction

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
                d = {}

                for UID in container.keys():
                    d[UID] = OrderedDict()
                    daviz = container[UID]

                    if daviz.has_key('live'):
                        for chart_id in daviz.pop('live'):
                            daviz[chart_id] = 'live'
                            d[UID][chart_id] = 'live'

                    if daviz.has_key('preview'):
                        for chart_id in daviz.pop('preview'):
                            daviz[chart_id] = 'preview'
                            d[UID][chart_id] = 'preview'

                    d[UID].update(daviz)

                obj.__annotations__['DAVIZ_CHARTS'] = PersistentMapping()
                obj.__annotations__['DAVIZ_CHARTS'].update(d)

                obj._p_changed = True
                self.log("Content of %s: %s" % (obj,
                             list(obj.__annotations__['DAVIZ_CHARTS'].items())))

                self.log("Migrated daviz relations for %s" % obj.absolute_url())

            self.log("Done migrating all objects of type: %s" % _type)

        transaction.commit()

        self.log("Finished migration of daviz relations")

        self.out.seek(0)
        return self.out.read()
