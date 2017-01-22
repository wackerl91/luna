import yaml


class Component(yaml.YAMLObject):
    """Symbolic base class for components"""
    yaml_tag = u'!component'

    def __init__(self, name, module, class_name, arguments, tags, factory_class, factory_method, lazy, calls):
        self.name = name
        self.module = module
        self.class_name = class_name
        self.arguments = arguments
        self.tags = tags
        self.factory_class = factory_class
        self.factory_method = factory_method
        self.lazy = lazy
        self.calls = calls

    @classmethod
    def from_dict(cls, name, module=None, class_name=None, arguments=None, tags=None, factory_class=None,
                  factory_method=None, lazy=None, calls=None, **kwargs):
        return cls(name, module, class_name, arguments, tags, factory_class, factory_method, lazy, calls)
