import xbmc
from resources.lib.di.requiredfeature import RequiredFeature

router = RequiredFeature('router').request()


def route(name):
    def decorator(func):
        xbmc.log("[script.luna.router]: Adding route with name %s" % name)
        router._routes_cache[name] = func
        return func

    return decorator


def register(cls):
    route_object = router.routing[cls.__name__]
    routes_cache = {}
    for key, value in router._routes_cache.iteritems():
        routes_cache["%s_%s" % (route_object.prefix, key)] = value
    router.routes.update(routes_cache)
    router._routes_cache = {}
    return cls


class BaseController(object):
    def render(self, name, args=None):
        if args:
            return router.render(name, args=args)
        else:
            return router.render(name)
