import os

import sys
import yaml

try:
    import xbmcaddon
except ImportError:
    from xbmcswift2 import Plugin

# DO NOT DELETE THE FOLLOWING IMPORT
import resources.lib.di.component


class FeatureBroker:
    def __init__(self, allow_replace=False):
        self.providers = {}
        self.tags = {}
        self.initialized = {}
        self.allow_replace = allow_replace
        self._parse_config()

    def _parse_config(self):
        if 'xbmcaddon' in sys.modules:
            features_path = os.path.join(xbmcaddon.Addon().getAddonInfo('path'), 'resources/lib/config/features.yml')
        else:
            features_path = 'resources/lib/config/features.yml'

        with open(features_path) as config:
            features = yaml.load_all(config)
            for feature in features:
                self._provide(feature)
                if hasattr(feature, 'tags'):
                    for tag in feature.tags:
                        self.tag(tag['name'], feature.name)

    def _provide(self, feature):
        if not self.allow_replace:
            assert feature.name not in self.providers, "Duplicate feature: %s" % feature.name
        self.providers[feature.name] = feature

    def provide(self, feature, provider, *args, **kwargs):
        if not self.allow_replace:
            assert feature not in self.providers, "Duplicate feature: %s" % feature
        if callable(provider):
            def call():
                return provider(*args, **kwargs)
        else:
            def call():
                return provider
        self.providers[feature] = call

    def tag(self, base, feature_name):
        if base not in self.tags:
            self.tags[base] = []
        self.tags[base].append(feature_name)

    def get_tagged_features(self, base):
        try:
            tagged_features = self.tags[base]
        except KeyError:
            raise KeyError("Unknown tag named: %s" % base)

        return tagged_features

    def get_initialized(self, feature):
        try:
            instance = self.initialized[feature]
        except KeyError:
            instance = None

        return instance

    def set_initialized(self, feature, instance):
        if not self.allow_replace:
            assert feature not in self.initialized, "Duplicate instance: %s" % feature
        self.initialized[feature] = instance

    def __getitem__(self, feature):
        try:
            provider = self.providers[feature]
        except KeyError:
            try:
                # This might be more than one (plus it's returned as a list anyway)
                provider = self.tags[feature]
            except KeyError:
                print self.tags
                raise KeyError("Unknown feature named %s" % feature)

        return provider


features = FeatureBroker()


def no_assertion(obj): return True


def is_instance_of(*classes):
    def test(obj): return isinstance(obj, classes)

    return test


def has_attributes(*attributes):
    def test(obj):
        for attr in attributes:
            if not hasattr(obj, attr):
                return False
        return True

    return test


def has_methods(*methods):
    def test(obj):
        for method in methods:
            try:
                attr = getattr(obj, method)
            except AttributeError:
                return False
            if not callable(attr):
                return False
        return True

    return test
