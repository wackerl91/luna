"""
Holds all cross-controller routes, read from routing.yml
"""
import os
import sys
import yaml
import xbmc
import xbmcaddon

from resources.lib.routing.route import Route
from resources.lib.di.requiredfeature import RequiredFeature


class Router(object):
    def __init__(self):
        self.routes = {}
        self._routes_cache = {}
        self.routing = {}
        self.main_route = None

    def _parse_config(self):
        if 'xbmcaddon' in sys.modules:
            routing_path = os.path.join(xbmcaddon.Addon().getAddonInfo('path'), 'resources/lib/config/routing.yml')
        else:
            routing_path = 'resources/lib/config/routing.yml'

        with open(routing_path) as config:
            routing_objects = []
            routing = yaml.safe_load(config)
            for _route_definition in routing['routing']:
                route_object = Route.from_dict(_route_definition, **routing['routing'][_route_definition])
                routing_objects.append(route_object)
            config.close()
            for _route in routing_objects:
                self._provide_route(_route)

    def _provide_route(self, route):
        xbmc.log("[script.luna.router]: Registering route for class: %s" % route.class_name)
        self.routes[route.class_name] = {}
        self.routing[route.class_name] = route
        if route.is_main_route:
            self.main_route = route

    def register(self, cls):
        route = self.routing[cls.__name__]
        routes_cache = {}
        for key, value in self._routes_cache.iteritems():
            xbmc.log('[script.luna.router]: Added Route: %s_%s -> %s' % (route.prefix, key, value))
            routes_cache["%s_%s" % (route.prefix, key)] = value
        self.routes.update(routes_cache)
        self._routes_cache = {}
        return cls

    """
    def route(self, name):
        def decorator(func):
            xbmc.log("[script.luna.router]: Adding route with name %s" % name)
            self._routes_cache[name] = func
            return func
        return decorator
    """

    def render(self, name, instance=None, args=None):
        try:
            route = None
            prefix = name.split('_')[0]
            for key, _route in self.routing.iteritems():
                if _route.prefix == prefix:
                    route = _route
            # TODO: if we need to refactor this, call Dennis
            if route is not None:
                instance = RequiredFeature(route.service[1:]).request()
                if args:
                    return self.routes[name](instance, **args)
                else:
                    return self.routes[name](instance)
            else:
                raise ValueError("Failed determining prefix")
        except KeyError:
            if instance:
                try:
                    class_name = instance.__class__.__name__
                    route = self.routing[class_name]
                    return self.routes["%s_%s" % (route.prefix, name)]
                except KeyError:
                    pass

    def route_exists(self, name):
        return name in self.routes.keys()
