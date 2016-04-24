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

    def request(self):
        if featurebroker.features.get_initialized(self.feature) is not None:
            instance = featurebroker.features.get_initialized(self.feature)
        else:
            feature = featurebroker.features[self.feature]

            module = None

            if isinstance(feature, list):
                for possible_match in feature:
                    try:
                        loaded_component = featurebroker.features[possible_match]
                        module = importlib.import_module(loaded_component.module)
                        feature = loaded_component
                        break
                    except ImportError, e:
                        last_import_error = e
                        pass

            else:
                module = importlib.import_module(feature.module)

            if module is None:
                print 'Could not load features by name or tag %s, reason: %r' % (feature, last_import_error)
                return

            class_ = getattr(module, feature.class_name)
            if hasattr(feature, 'arguments'):
                for index, arg in enumerate(feature.arguments):
                    if arg[:1] == '@':
                        feature.arguments[index] = RequiredFeature(arg[1:]).request()
                args = inspect.getargspec(class_.__init__)[0]
                if args[0] == 'self':
                    args.pop(0)
                argument_dict = dict(zip(args, feature.arguments))
                instance = class_(**argument_dict)
            else:
                instance = class_()

            assert self.assertion(instance), \
                        "The value %s of %r does not match the specified criteria" \
                        % (instance, self.feature)

            try:
                tagged_features = featurebroker.features.get_tagged_features(self.feature)
                if featurebroker.has_methods('append')(instance):
                    instance.append(tagged_features)
            except KeyError:
                pass

            featurebroker.features.set_initialized(self.feature, instance)

        return instance
