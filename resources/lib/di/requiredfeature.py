import importlib
import inspect

from resources.lib.di import featurebroker


class RequiredFeature(object):
    def __init__(self, feature, assertion=featurebroker.no_assertion):
        self.feature = feature
        self.assertion = assertion

    def __get__(self, instance, owner):
        return self.result

    def __getattr__(self, name):
        assert name == 'result', "Unexpected attribute request other than 'result': %s" % name
        self.result = self.request()
        return self.result

    def _build_attributes_dict(self, class_, feature):
        args = getattr(feature, 'arguments', None)
        if args is not None:
            for index, arg in enumerate(feature.arguments):
                if arg[:1] == '@':
                    feature.arguments[index] = RequiredFeature(arg[1:]).request()
            args = inspect.getargspec(class_.__init__)[0]
            if args[0] == 'self':
                args.pop(0)
            argument_dict = dict(zip(args, feature.arguments))

            return argument_dict
        else:
            return None

    def request(self):
        if featurebroker.features.get_initialized(self.feature) is not None:
            instance = featurebroker.features.get_initialized(self.feature)
        else:
            feature = featurebroker.features[self.feature]

            lazy = getattr(feature, 'lazy', None)
            if lazy is not None:
                lazy_module = importlib.import_module('resources.lib.di.lazyproxy')
                lazy_class = getattr(lazy_module, 'LazyProxy')

                lazy_instance = lazy_class(
                    original_module=feature.module,
                    original_class=feature.class_name,
                    init_args=feature.arguments
                )

                featurebroker.features.set_initialized(self.feature, lazy_instance)

                return lazy_instance

            module = importlib.import_module(feature.module)
            class_ = getattr(module, feature.class_name)

            factory = getattr(feature, 'factory_class', None)
            if factory is not None:
                factory_class = RequiredFeature(feature.factory_class[1:]).request()
                factory_method = feature.factory_method

                if featurebroker.has_methods(factory_method)(factory_class):
                    arguments = self._build_attributes_dict(class_, feature)
                    if arguments is not None:
                        instance = getattr(factory_class, factory_method)(**arguments)
                    else:
                        instance = getattr(factory_class, factory_method)()

            else:
                arguments = self._build_attributes_dict(class_, feature)
                if arguments is not None:
                    instance = class_(**arguments)
                else:
                    instance = class_()
                assert self.assertion(instance), \
                    "The value %s of %r does not match the specified criteria" \
                    % (instance, self.feature)

            try:
                tagged_features = featurebroker.features.get_tagged_features(self.feature)
                if featurebroker.has_methods('append')(instance):
                    for key, tagged_feature in enumerate(tagged_features):
                        tagged_features[key] = RequiredFeature(tagged_feature.name).request()

                    instance.append(tagged_features)
            except KeyError:
                pass

            featurebroker.features.set_initialized(self.feature, instance)

        return instance
