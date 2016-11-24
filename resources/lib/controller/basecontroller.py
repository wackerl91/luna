import xbmc
from resources.lib.di.requiredfeature import RequiredFeature

router = RequiredFeature('router').request()


def route(name):
    def decorator(func):
        xbmc.log("[script.luna.router]: Adding route with name %s" % name)
        router._routes_cache[name] = func
        return func

    return decorator


class BaseController(object):
    def render(self, name, args=None):
        xbmc.log("Trying to render: %s" % name)
        if args:
            return router.render(name, args=args)
        else:
            return router.render(name)
