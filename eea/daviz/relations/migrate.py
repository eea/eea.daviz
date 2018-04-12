"""Migration for daviz/eea.relations integration
"""
import logging
from StringIO import StringIO
import transaction
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from zope.annotation.interfaces import IAnnotations
from persistent.mapping import PersistentMapping
from zc.dict import OrderedDict

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
                                                list(obj.__annotations__[
                                                     'DAVIZ_CHARTS'].items())))

                self.log("Migrated daviz relations for %s" % obj.absolute_url())

            self.log("Done migrating all objects of type: %s" % _type)

        transaction.commit()

        self.log("Finished migration of daviz relations")

        self.out.seek(0)
        return self.out.read()


def fix_broken_relationships(obj):
    """ fix assessmentParts broken relations
    """
    portal = getToolByName(obj, 'portal_url').getPortalObject()
    catalog = getToolByName(obj, 'portal_catalog')
    cpath = obj.absolute_url(1)
    res = catalog.searchResults(path=cpath, portal_type='AssessmentPart')
    uids_cat = getToolByName(portal, 'uid_catalog')
    logger.info("Starting cleanup of assessmentpart-daviz bad relations")
    i = 0
    results = False
    for b in res:
        obj = b.getObject()
        annot = obj.__annotations__.get('DAVIZ_CHARTS', {})
        for uid in annot.keys():
            brains = uids_cat.searchResults(UID=uid)
            if not brains:
                msg = "Couldn't find object for brain with UID %s, " \
                      "deleting assessmentpart %s" % (uid,
                                                      obj.absolute_url())
                logger.info(msg)
                del annot[uid]
                annot._p_changed = True
                obj._p_changed = True
                i += 1
                continue
            brain = brains[0]
            daviz = brain.getObject()
            if daviz is None:  # brain does not lead to object?
                path = brain.getPath()
                msg = "Couldn't find object for brain with UID %s, " \
                      "uncatalog object %s" % (uid, path)
                logger.info(msg)
                uids_cat.uncatalog_object(path)
                brains = uids_cat.searchResults(UID=uid)
                if brains and brains[0].getObject():
                    path = brains[0].getPath()
                    msg = "Brain with UID %s now found at %s" % (uid, path)
                    logger.info(msg)
                results = True
                i += 1
    logger.info("End fix of assessmentpart-daviz bad relations")
    return "FIX DONE" if results else "NO FIX NEEDED"


class FixAssessmentPartsBrokenRelations(BrowserView):
    """ Fix AssessmentPart relations that contains wrong uids_catalog uids
    """

    def __call__(self):
        """ Call
        """
        return fix_broken_relationships(self.context)
