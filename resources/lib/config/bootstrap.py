import resources.lib.config.features as provider

from xbmcswift2 import Plugin

from resources.lib.di.featurebroker import features


def bootstrap():
    print 'Bootstrapper called'
    plugin = Plugin()
    features.provide('plugin', plugin)
    provider.init_di()
    return plugin
