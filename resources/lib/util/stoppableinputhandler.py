import Queue

from resources.lib.model.inputmap import InputMap
from resources.lib.util.stoppablethread import StoppableThread

input_prompt = {
    'abs_x':            'left stick left',
    'reverse_x':        'left stick right',
    'abs_y':            'left stick up',
    'reverse_y':        'left stick down',
    'abs_rx':           'right stick left',
    'reverse_rx':       'right stick right',
    'abs_ry':           'right stick up',
    'reverse_ry':       'right stick down',
    'abs_dpad_x':       'dpad left',
    'reverse_dpad_x':   'dpad right',
    'abs_dpad_y':       'dpad up',
    'reverse_dpad_y':   'dpad down',
    'btn_thumbl':       'press left stick',
    'btn_thumbr':       'press right stick',
    'btn_select':       'select',
    'btn_start':        'start',
    'btn_mode':         'special',
    'btn_south':        'a',
    'btn_east':         'b',
    'btn_west':         'x',
    'btn_north':        'y',
    'btn_tl':           'bumper left',
    'btn_tr':           'bumper right',
    'btn_tl2':          'trigger left',
    'btn_tr2':          'trigger right'
}

input_no = [
    'abs_x',
    'reverse_x',
    'abs_y',
    'reverse_y',
    'abs_rx',
    'reverse_rx',
    'abs_ry',
    'reverse_ry',
    'abs_dpad_x',
    'reverse_dpad_x',
    'abs_dpad_y',
    'reverse_dpad_y',
    'btn_thumbl',
    'btn_thumbr',
    'btn_select',
    'btn_start',
    'btn_mode',
    'btn_south',
    'btn_east',
    'btn_west',
    'btn_north',
    'btn_tl',
    'btn_tr',
    'btn_tl2',
    'btn_tr2'
]


class StoppableInputHandler(StoppableThread):
    def __init__(self, input_queue, input_map, dialog, input_number):
        self.input_queue = input_queue
        self.input_map = input_map
        self.dialog = dialog
        self.input_number = input_number
        self._trigger_as_button = True
        StoppableThread.__init__(self)

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        self.input_queue.queue.clear()
        i = 0
        while self.input_map.status is not InputMap.STATUS_DONE:
            if self.stopped():
                self.cleanup()
                break
            try:
                btn_waiting_for_input = input_no[i]
                self.dialog.update(0, input_prompt.get(btn_waiting_for_input))
                in_number, name, fvalue, in_type = self.input_queue.get()

                if name == 'brake' and fvalue == -1.0:
                    self._trigger_as_button = False
                    continue
                if name == 'gas' and fvalue == -1.0:
                    self._trigger_as_button = False
                    continue

                if in_type == 'ax':
                    if btn_waiting_for_input.split('_')[0] == 'reverse':
                        if fvalue == -1.0:
                            self.input_map.set_btn(btn_waiting_for_input, 'true')
                        else:
                            self.input_map.set_btn(btn_waiting_for_input, 'false')
                    else:
                        if btn_waiting_for_input in ['btn_tl2', 'btn_tr2']:
                            if btn_waiting_for_input == 'btn_tl2':
                                self.input_map.set_btn('abs_z', in_number)
                            if btn_waiting_for_input == 'btn_tr2':
                                self.input_map.set_btn('abs_rz', in_number)
                        else:
                            self.input_map.set_btn(btn_waiting_for_input, in_number)

                if in_type == 'btn':
                    self.input_map.set_btn(btn_waiting_for_input, in_number)

                if self._trigger_as_button and i == self.input_number-1:
                    self.input_map.status = InputMap.STATUS_DONE
                    break
                if not self._trigger_as_button and i == self.input_number-3:
                    self.input_map.status = InputMap.STATUS_DONE
                    break
                else:
                    i += 1
            except Queue.Empty:
                pass
            except IndexError:
                self.input_map.status = InputMap.STATUS_ERROR
                break
        self.stop()

    def cleanup(self):
        return
