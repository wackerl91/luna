class Setting(object):
    def __init__(self, setting_id, setting_label, priority, *args, **kwargs):
        self.setting_id = setting_id
        self.setting_label = setting_label
        self.priority = priority

        if 'type' in kwargs.keys():
            self.type = kwargs['type']
        else:
            self.type = None  # TODO: This should never happen

        if 'default' in kwargs.keys():
            self.default = kwargs['default']
        else:
            self.default = None

        if 'visible' in kwargs.keys():
            self.visible = kwargs['visible']
        else:
            self.visible = None

        if 'enable' in kwargs.keys():
            self.enable = kwargs['enable']
        else:
            self.enable = None

        if 'values' in kwargs.keys():
            self.values = kwargs['values']  # TODO: Parse into list
        else:
            self.values = None

        if 'range' in kwargs.keys():
            self.range = kwargs['range']  # TODO: Parse into list
        else:
            self.range = None

        if 'option' in kwargs.keys():
            self.option = kwargs['option']
        else:
            self.option = None

        if 'subsetting' in kwargs.keys():
            self.subsetting = kwargs['subsetting']
        else:
            self.subsetting = None

        if 'current_value' in kwargs.keys():
            self.current_value = kwargs['current_value']
        else:
            self.current_value = self.default
