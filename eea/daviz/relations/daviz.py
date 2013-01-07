"""Integration with eea.daviz
"""

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from eea.app.visualization.interfaces import IDataProvenance
from persistent.mapping import PersistentMapping
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter
import urlparse
import logging

logger = logging.getLogger("eea.indicators")


class SetDavizChart(BrowserView):
    """Edit the chart for a daviz presentation that's set as related
    """

    def __call__(self):
        """info is a dict of uid:[list of chart ids] values
        """
        uid = self.request.form.get("daviz_uid")
        chart = self.request.form.get("chart")
        if chart:
            selected_charts = urlparse.parse_qs(chart)['chart']
        else:
            selected_charts = []

        # selected_charts is a list in form [(chartId, type_of_view),...]
        # where type_of_view is either "live" or "preview"

        obj = self.context
        annot = IAnnotations(obj)
        
        if not 'DAVIZ_CHARTS' in annot:
            annot['DAVIZ_CHARTS'] = PersistentMapping()
        
        annot['DAVIZ_CHARTS'][uid.strip()] = selected_charts

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
        """return daviz charts as a dict of uid:[list of chart ids]
        """
        annot = IAnnotations(self.context).get('DAVIZ_CHARTS', {})
        return annot.get(uid, [])

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
            charts = []
            for chart, type_of_view in annot[uid]:
                for tab in tabs:
                    if tab['name'] == chart:
                        code = None #to be filled in, waiting for api in daviz
                        charts.append((chart, tab['title'], code,
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
            'title':adapter.title,
            'link':adapter.link,
            'owner':adapter.owner
        }
