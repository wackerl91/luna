import yaml


class Route(yaml.YAMLObject):
    """Symbolic base class for routes"""
    yaml_tag = u'!route'

    def __init__(self, service_name, class_name, service, prefix):
        self.service_name = service_name
        self.class_name = class_name
        self.service = service
        self.prefix = prefix
        self.is_main_route = (prefix == 'main')

    @classmethod
    def from_dict(cls, service_name=None, class_name=None, service=None, prefix=None, **kwargs):
        return cls(service_name, class_name, service, prefix)
