"""Integration with eea.daviz
"""

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from eea.app.visualization.interfaces import IDataProvenance
from persistent.mapping import PersistentMapping
from urlparse import parse_qs
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter
import logging

logger = logging.getLogger("eea.indicators")


class SetDavizChart(BrowserView):
    """Edit the chart for a daviz presentation that's set as related
    """

    def __call__(self):
        """info is a dict of uid:[list of chart ids] values
        """
        form = self.request.form
        uid = self.request.form.get("daviz_uid")

        live_charts = form.get("lives", [])
        preview_charts = form.get("previews", [])

        if live_charts:
            live_charts = parse_qs(live_charts)['live']

        if preview_charts:
            preview_charts = parse_qs(preview_charts)['preview']

        obj = self.context
        annot = IAnnotations(obj)

        if not 'DAVIZ_CHARTS' in annot:
            annot['DAVIZ_CHARTS'] = PersistentMapping()

        annot['DAVIZ_CHARTS'][uid.strip()] = {
            'live': live_charts or [],
            'preview': preview_charts or []
        }

        print obj, annot['DAVIZ_CHARTS'].items()

        return "done"


class GetDavizChart(BrowserView):
    """Get the chart for a daviz presentation that's set as related
    """

    def __call__(self):
        """
        """
        return self

    def get_charts(self, uid):
        """return daviz charts as a dict of {live:[], preview:[]}
        """
        annot = IAnnotations(self.context).get('DAVIZ_CHARTS', {})
        q = {'live': [], 'preview': []}
        res = annot.get(uid, q)
        if isinstance(res, list):   #during the development format has changed
            res = q
        return res

    def get_daviz(self):
        """Given an object, it will return the daviz+charts assigned
        """
        annot = IAnnotations(self.context).get('DAVIZ_CHARTS', {})

        uids_cat = getToolByName(self.context, 'uid_catalog')
        info = {}
        for uid in annot.keys():
            brains = uids_cat.searchResults(UID=uid)
            if not brains:
                logger.warning("Couldn't find visualization with UID %s" % uid)
            obj = brains[0].getObject()
            tabs = getMultiAdapter((obj, self.request),
                                   name="daviz-view.html").tabs
            charts = {'live': [], 'preview': []}

            #compensate for format change during development
            annot_info = annot[uid]
            if not isinstance(annot_info, dict):
                annot_info = {'live': [], 'preview': []}

            for chart in annot_info['live']:
                for tab in tabs:
                    if tab['name'] == chart:
                        code = None #to be filled in, waiting for api in daviz
                        charts['live'].append((chart, tab['title'], code,
                                               tab['fallback-image']))
            for chart in annot_info['preview']:
                for tab in tabs:
                    if tab['name'] == chart:
                        code = None #to be filled in, waiting for api in daviz
                        charts['preview'].append((chart, tab['title'], code,
                                                  tab['fallback-image']))
            info[uid] = (obj, charts)

        #print info
        return info


class DavizDataSource(BrowserView):
    """Info about data source for daviz
    """

    def __call__(self):
        adapter = IDataProvenance(self.context)
        return {
            'title': adapter.title,
            'link': adapter.link,
            'owner': adapter.owner
        }
