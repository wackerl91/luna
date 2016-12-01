class Tag(object):
    def __init__(self, name, **kwargs):
        self.name = name

        for key, value in kwargs.iteritems():
            self.__setattr__(key, value)

    @classmethod
    def from_dict(cls, name, **kwargs):
        return cls(name, **kwargs)

    def __str__(self):
        if hasattr(self, 'channel'):
            return '%s->%s' % (self.name, self.channel)
        else:
            return self.name
