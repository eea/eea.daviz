"""Integration with eea.daviz
"""

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from persistent.mapping import PersistentMapping
from zc.dict import OrderedDict
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter
import logging

logger = logging.getLogger("eea.indicators")

KEY = 'DAVIZ_CHARTS'

class SetDavizChart(BrowserView):
    """Edit the chart for a daviz presentation that's set as related

    We store the charts in an annotation on the context object;
    This annotation is an OrderedDict, where the keys are the UIDs
    of the daviz objects; As values we have OrderedDicts of
    chart_id:type_of_embed, where type_of_embed is either "live" or "preview"
    """

    def __call__(self):
        """info is a dict of uid:[list of chart ids] values
        """
        form = self.request.form
        uid = form.get("daviz_uid", "").strip()

        obj = self.context
        annot = IAnnotations(obj)

        if not KEY in annot:
            annot[KEY] = PersistentMapping()

        info = annot[KEY].get(uid)
        if not info:
            info = annot[KEY][uid] = OrderedDict()

        previous_info = dict(info)
        info.clear()


        #this is a string like: 'chart_1=preview&chart_2=live'
        #from urlparse import parse_qs
        #cannot use parse_qs because it doesn't guarantee order
        req_charts = form.get("charts", "").strip()
        charts = []

        for pair in req_charts.split("&"):
            if pair:
                chart_id, embed = pair.split("=")
                chart_settings = PersistentMapping()
                chart_settings['type'] = embed
                for prev_key, prev_val in previous_info.get(chart_id, {}).\
                    items():
                    if prev_key != 'type':
                        chart_settings[prev_key] = prev_val
                charts.append((chart_id, chart_settings))


        info.update(charts)

        self.context._p_changed = True

        return "OK"

    def set_daviz_size(self):
        """Set the custom size of the chart
        """
        form = self.request.form
        uid = form.get("daviz_uid", "").strip()
        chart_id = form.get("chart_id", "").strip()

        annot = IAnnotations(self.context).get("DAVIZ_CHARTS", {})

        form = self.request.form
        uid = form.get("daviz_uid", "").strip()
        chart_id = form.get("chart_id", "").strip()

        chart_settings = annot[uid][chart_id]
        chart_settings['width'] = form.get("width", "").strip()
        chart_settings['height'] = form.get("height", "").strip()
        chart_settings['chartAreaWidth'] = form.get("chartAreaWidth", "").\
            strip()
        chart_settings['chartAreaHeight'] = form.get("chartAreaHeight", "").\
            strip()
        chart_settings['chartAreaTop'] = form.get("chartAreaTop", "").strip()
        chart_settings['chartAreaLeft'] = form.get("chartAreaLeft", "").strip()

class GetDavizChart(BrowserView):
    """Get the chart for a daviz presentation that's set as related
    """

    def __call__(self):
        """Not usable standalone so we return self
        """
        return self

    def get_charts(self, uid):
        """return daviz charts as a dict of {chart_id:"preview|live"}
        """
        info = self.get_daviz().get(uid)
        if info:
            return info[1]  #only the charts
        return []

    def get_daviz(self):
        """Given an object, it will return the daviz+charts assigned

        It returns a mapping of
        <daviz uid A>:
            [daviz, (chart_id, chart title, embed_type, fallback_image)],
        <daviz uid B>:
            [daviz, (chart_id, chart title, embed_type, fallback_image)],
        """
        annot = IAnnotations(self.context).get('DAVIZ_CHARTS', {})

        uids_cat = getToolByName(self.context, 'uid_catalog')
        info = {}
        for uid in annot.keys():
            brains = uids_cat.searchResults(UID=uid)
            if not brains:
                msg = "Couldn't find visualization with UID %s" % uid
                logger.warning(msg)
                continue
            daviz = brains[0].getObject()
            if daviz is None:   #brain does not lead to object?
                msg = "Couldn't find object for brain with UID %s" % uid
                logger.warning(msg)
                continue
            tabs = getMultiAdapter((daviz, self.request),
                                       name="daviz-view.html").tabs

            annot_info = annot.get(uid, {})
            charts = []

            for chart_id in annot_info.keys():
                for tab in tabs:
                    if tab['name'] == chart_id:
                        #code = None #for the future, needs api in daviz
                        embed_type = annot_info[chart_id]
                        charts.append((chart_id, tab['title'], embed_type,
                                       tab['fallback-image']))
            info[uid] = (daviz, charts)

        return info


def handle_daviz_delete(context, event):
    """ Remove annotations from assessmentparts when a daviz has been deleted
    """
    context_uid = context.UID()
    refs = context.getBRefs()

    for o in refs:
        annot = IAnnotations(o).get(KEY, {})
        if context_uid in annot.keys():
            del annot[context_uid]
            annot._p_changed = True
            o._p_changed = True
