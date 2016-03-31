import yaml


class Component(yaml.YAMLObject):
    """Symbolic base class for components"""
    yaml_tag = u'!component'

    def __init__(self, name, module, class_name, arguments, tags):
        self.name = name
        self.module = module
        self.class_name = class_name,
        self.arguments = arguments,
        self.tags = tags
