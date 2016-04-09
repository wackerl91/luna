import ConfigParser


class InputMap:
    STATUS_DONE = 'done'
    STATUS_PENDING = 'pending'
    STATUS_ERROR = 'error'

    def __init__(self, file_name):
        self.file_name = file_name
        self.abs_x = -1
        self.abs_y = -1
        self.abs_z = -1
        self.reverse_x = 'false'
        self.reverse_y = 'false'
        self.abs_rx = -1
        self.abs_ry = -1
        self.abs_rz = -1
        self.reverse_rx = 'false'
        self.reverse_ry = 'false'
        # TODO: How to calculate deadzone properly? moonlight's default config uses 0 all the time ...
        self.abs_deadzone = 0
        self.abs_dpad_x = -1
        self.abs_dpad_y = -1
        self.reverse_dpad_x = 'false'
        self.reverse_dpad_y = 'false'
        self.btn_north = -1
        self.btn_east = -1
        self.btn_south = -1
        self.btn_west = -1
        self.btn_select = -1
        self.btn_start = -1
        self.btn_mode = -1
        self.btn_thumbl = -1
        self.btn_thumbr = -1
        self.btn_tl = -1
        self.btn_tr = -1
        self.btn_tl2 = -1
        self.btn_tr2 = -1
        self.btn_dpad_up = -1
        self.btn_dpad_down = -1
        self.btn_dpad_left = -1
        self.btn_dpad_right = -1
        self.status = self.STATUS_PENDING

    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            if attr not in ['status', 'file_name']:
                yield attr, value

    def set_btn(self, attr, btn_no):
        setattr(self, attr, btn_no)

    def write(self):
        mapping = ConfigParser.ConfigParser()
        print dict(self)
        for attr, value in dict(self).iteritems():
            mapping.set('', attr, value)

        if self.status == self.STATUS_DONE:
            with open(self.file_name, 'wb') as mapping_file:
                mapping.write(mapping_file)
            mapping_file.close()
