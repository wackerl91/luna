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
        obj = featurebroker.features[self.feature]
        assert self.assertion(obj), \
            "The value %s of %r does not match the specified criteria" \
            % (obj, self.feature)

        try:
            tagged_features = featurebroker.features.get_tagged_features(self.feature)
            if featurebroker.has_methods('append')(obj):
                obj.append(tagged_features)
        except KeyError:
            pass

        return obj
