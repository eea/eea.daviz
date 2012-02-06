""" Caching
"""
def cacheJsonKey(method, self, *args, **kwargs):
    """ Generate unique cache id
    """
    kwargs = kwargs.copy()
    kwargs.update(self.request.form)
    name = getattr(self, '__name__', '')
    return (self.context.absolute_url(1), name, kwargs)
