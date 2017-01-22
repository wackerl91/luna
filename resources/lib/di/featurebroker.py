import importlib
import os
import sys
import yaml

import xbmcaddon

from resources.lib.di.component import Component
from resources.lib.di.tag import Tag


class FeatureBroker:
    def __init__(self, allow_replace=False):
        self.providers = {}
        self.tagged_features = {}
        self.tags = {}
        self.initialized = {}
        self.allow_replace = allow_replace

    def _parse_config(self):
        if 'xbmcaddon' in sys.modules:
            features_path = os.path.join(xbmcaddon.Addon().getAddonInfo('path'), 'resources/lib/config/features.yml')
        else:
            features_path = 'resources/lib/config/features.yml'

        with open(features_path) as config:
            feature_objects = []
            service_definitions = yaml.safe_load(config)

            for _service in service_definitions['services']:
                feature = Component.from_dict(_service, **service_definitions['services'][_service])
                feature_objects.append(feature)

            for feature in feature_objects:
                self._provide(feature)
                tags = getattr(feature, 'tags', None)
                if tags is not None:
                    for key, tag in enumerate(feature.tags):
                        tag = Tag.from_dict(**tag)
                        feature.tags[key] = tag
                        self.tag(tag, feature)

            config.close()

        self._provide_loggers()
        self._replace_logger_args()

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

    def tag(self, tag, feature):
        if tag.name not in self.tagged_features:
            self.tagged_features[tag.name] = []

        # Building tags as list is useful for services like @logger
        if tag.name not in self.tags:
            self.tags[tag.name] = []

        # Don't add tags multiple times
        if tag not in self.tags[tag.name]:
            self.tags[tag.name].append(tag)

        if feature not in self.tagged_features[tag.name]:
            self.tagged_features[tag.name].append(feature)

    def get_tagged_features(self, tag_name):
        try:
            tagged_features = self.tagged_features[tag_name]
        except KeyError:
            raise KeyError("Unknown tag named: %s" % tag_name)

        return tagged_features

    def _provide_loggers(self):
        module = importlib.import_module('resources.lib.core.logger.loggerchain')
        class_name = 'LoggerChain'
        class_ = getattr(module, class_name)

        addon_id = xbmcaddon.Addon().getAddonInfo('id')

        for logger_definition in self.tags['logger']:
            logger_prefix = '%s.%s' % (addon_id, logger_definition.channel)
            _logger = class_(logger_prefix)

            logger_services = list(self.tagged_features['logger-chain'])

            del_keys = []

            for key, logger_service in enumerate(logger_services):
                from resources.lib.di.requiredfeature import RequiredFeature
                for tag in logger_service.tags:
                    if tag.name == 'logger-chain':
                        if hasattr(tag, 'ignore_channel') and tag.ignore_channel == logger_definition.channel:
                            del_keys.append(key)
                        else:
                            logger_services[key] = RequiredFeature(logger_service.name).request()

            for key in del_keys:
                del logger_services[key]

            _logger.append(logger_services)

            _logger_service_name = 'logger.%s' % logger_definition.channel

            self.set_initialized(_logger_service_name, _logger)

    def _replace_logger_args(self):
        for feature_definition in self.get_tagged_features('logger'):
            logger_channel = None

            for tag in feature_definition.tags:
                if tag.name == 'logger':
                    logger_channel = tag.channel
                    break

            if logger_channel is not None:
                logger_service = '@logger.%s' % logger_channel

                for key, value in enumerate(feature_definition.arguments):
                    if value[1:] == 'logger':
                        feature_definition.arguments[key] = logger_service

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

    def execute_calls(self):
        for feature_name, feature in self.providers.iteritems():
            if not isinstance(feature, Component):
                continue
            instance = self.get_initialized(feature.name)
            if instance and hasattr(feature, 'calls') and feature.calls is not None:
                import xbmc
                xbmc.log("Trying to execute calls for %s" % feature.name)
                for call in feature.calls:
                    method = call[0]
                    args = call[1]

                    for key, arg in enumerate(args):
                        if arg[:1] == '@':
                            if self.get_initialized(arg[1:]) is not None:
                                args[key] = self.get_initialized(arg[1:])
                            else:
                                from resources.lib.di.requiredfeature import RequiredFeature
                                args[key] = RequiredFeature(arg[1:]).request()

                    resolved_all_services = True
                    for key, arg in enumerate(args):
                        if isinstance(arg, str) and arg[:1] == '@':
                            resolved_all_services = False

                    if resolved_all_services:
                        if hasattr(instance, method):
                            method_ = getattr(instance, method)
                            xbmc.log(str(*args))
                            method_(*args)

    def __getitem__(self, feature):
        try:
            provider = self.providers[feature]
        except KeyError:
            raise KeyError("Unknown feature named %s" % feature)

        return provider


features = None


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
