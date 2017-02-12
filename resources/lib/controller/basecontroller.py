import xbmc
from resources.lib.di.requiredfeature import RequiredFeature

router = RequiredFeature('router').request()


def route(name):
    def decorator(func):
        xbmc.log("[script.luna.router]: Adding route with name %s to cache" % name)
        assert name not in router._routes_cache, "Route with name %s already exists on the same class" % name
        router._routes_cache[name] = func
        return func

    return decorator


class BaseController(object):
    def render(self, name, args=None):
        if args:
            return router.render(name, args=args)
        else:
            return router.render(name)

    def route_exists(self, name):
        return router.route_exists(name)

    def cleanup(self):
        raise NotImplementedError("Cleanup needs to be implemented.")
