""" EEA Daviz javascripts
"""
from App.Common import rfc1123_date
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.ResourceRegistries.tools.packer import JavascriptPacker

class Javascript(object):
    """ Handle criteria
    """
    def __init__(self, context, request, resources=()):
        self.context = context
        self.request = request
        self._resources = resources
        self.duration = 3600*24*365

        self.jstool = getToolByName(context, 'portal_javascripts', None)
        if self.jstool:
            self.debug = self.jstool.getDebugMode()

    @property
    def resources(self):
        """ Return resources
        """
        return self._resources

    def get_resource(self, resource):
        """ Get resource content
        """
        obj = self.context.restrictedTraverse(resource, None)
        if not obj:
            return '/* ERROR */'
        try:
            content = obj.GET()
        except AttributeError, err:
            return str(obj)
        except Exception, err:
            return '/* ERROR: %s */' % err
        else:
            return content

    def get_content(self, **kwargs):
        """ Get content
        """
        output = []
        for resource in self.resources:
            content = self.get_resource(resource)
            header = '\n/* - %s - */\n' % resource
            if not self.debug:
                content = JavascriptPacker('safe').pack(content)
            output.append(header + content)
        return '\n'.join(output)

    @property
    def helper_js(self):
        """ Helper js
        """
        return []

class ViewJavascript(Javascript):
    """ Javascript libs used in view mode
    """
    @property
    def js_libs(self):
        """ JS libs
        """
        return (
            '++resource++eea.daviz.view.js',
        )

    @property
    def resources(self):
        """ Return view resources
        """
        res = self.helper_js
        res.extend(self.js_libs)
        return res

    def __call__(self, *args, **kwargs):
        """ view.js
        """
        self.request.RESPONSE.setHeader('content-type', 'text/javascript')
        expires = rfc1123_date((DateTime() + 365).timeTime())
        self.request.RESPONSE.setHeader('Expires', expires)
        self.request.RESPONSE.setHeader('Cache-Control',
                                        'max-age=%d' % self.duration)
        return self.get_content()

class EditJavascript(Javascript):
    """ Javascript libs used in edit form
    """
    @property
    def js_libs(self):
        """ JS libs
        """
        return (
            '++resource++eea.daviz.edit.js',
        )

    @property
    def resources(self):
        """ Return edit resources
        """
        res = self.helper_js
        res.extend(self.js_libs)
        return res

    def __call__(self, *args, **kwargs):
        """ edit.js
        """
        self.request.RESPONSE.setHeader('content-type', 'text/javascript')
        expires = rfc1123_date((DateTime() + 365).timeTime())
        self.request.RESPONSE.setHeader('Expires', expires)
        self.request.RESPONSE.setHeader('Cache-Control',
                                        'max-age=%d' % self.duration)
        return self.get_content()
