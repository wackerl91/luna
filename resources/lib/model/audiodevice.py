class AudioDevice:
    def __init__(self):
        self.original_name = None
        self.card = None
        self.device = None
        self.subdevice = None
        self.stream = None
        self.id = None
        self.name = None
        self.subname = None
        self.cls = None
        self.subcls = None
        self.subdevices_count = None
        self.subdevices_avail = None
        self.handler = ''

    def get_name(self):
        if self.original_name == self.id:
            return '%s - %s' % (self.id, self.name)
        else:
            return '%s - %s' % (self.id, self.original_name)
