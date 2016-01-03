class FeatureBroker:
    def __init__(self, allow_replace=False):
        self.providers = {}
        self.tags = {}
        self.allow_replace = allow_replace

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

    def tag(self, base, feature):
        if base not in self.tags:
            self.tags[base] = []
        self.tags[base].append(feature)

    def get_tagged_features(self, base):
        try:
            tagged_features = self.tags[base]
        except KeyError:
            raise KeyError("Unknown tag named: %s" % base)

        return tagged_features

    def __getitem__(self, feature):
        try:
            provider = self.providers[feature]
        except KeyError:
            raise KeyError("Unknown feature named %s" % feature)

        return provider()


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
