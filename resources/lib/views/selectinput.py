import hashlib
import os
import time

import pyxbmct.addonwindow as pyxbmct

import xbmcaddon
import xbmcgui

from resources.lib.model.ctrlselectionwrapper import CtrlSelectionWrapper
from resources.lib.model.inputdevice import InputDevice

_addon_path = xbmcaddon.Addon().getAddonInfo('path')

COLOR_FO = '0xFFE0B074'
COLOR_NF = '0xFF808080'
COLOR_HEADING = '0xFFD6D6D6'
COLOR_DETAILS = '0xFF707070'
COLOR_SELECTED = '0xFFF1F1F1'


def create_button():
    return pyxbmct.Button(
        '',
        focusTexture='',
        noFocusTexture='',
        focusedColor=COLOR_FO,
        textColor=COLOR_NF,
        font='Med',
        alignment=pyxbmct.ALIGN_LEFT
    )


def create_label():
    return pyxbmct.Label(
        '',
        alignment=pyxbmct.ALIGN_LEFT,
        font='Med',
        textColor=COLOR_DETAILS
    )


class SelectInput(pyxbmct.AddonDialogWindow):
    def __init__(self, controller, available_devices, input_devices, title=''):
        super(SelectInput, self).__init__(title)
        self.controller = controller
        self.available_devices = available_devices
        self.md5 = hashlib.md5()
        self.input_devices = input_devices

        background = None
        if self.controller.get_active_skin() == 'skin.osmc':
            media_path = '/usr/share/kodi/addons/skin.osmc/media'
            if os.path.exists(media_path):
                background = os.path.join(media_path, 'dialogs/DialogBackground_old.png')

        if background is not None:
            self.background.setImage(background)
            self.removeControl(self.title_background)
            self.removeControl(self.window_close_button)
            self.removeControl(self.title_bar)

        self.controls = {}
        self.add_ctrl_btn = None

        self.setGeometry(1280, 720, 12, 6, padding=60)
        self.place_add_ctrl_btn()
        self.setFocus(self.add_ctrl_btn)
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close())
        self.init_existing_controls()  # initalise controls / mappings read from .storage

    def place_add_ctrl_btn(self):
        self.add_ctrl_btn = create_button()
        self.add_ctrl_btn.setLabel('Add Controller')
        self.placeControl(self.add_ctrl_btn, row=12, column=1, rowspan=1, columnspan=2)
        self.connect(self.add_ctrl_btn, self.add_ctrl)

    def add_ctrl(self, device=None):
        idx = len(self.controls)

        control = CtrlSelectionWrapper()
        self.md5.update(str(time.time()))
        ctrl_id = self.md5.hexdigest()
        control.id = ctrl_id
        control.idx = idx

        if not device:
            device = InputDevice()
            device.name = 'None (Disabled)'

        control.device = device

        label = create_label()
        label.setLabel('Controller ' + str(idx))
        control.label = label

        input_select_btn = create_button()
        input_select_btn.setLabel(
            control.device.name,
        )
        control.input_select_btn = input_select_btn

        trigger_adv_mapping_btn = create_button()
        trigger_adv_mapping_btn.setLabel('Add Mapping')
        control.trigger_adv_mapping_btn = trigger_adv_mapping_btn

        remove_btn = create_button()
        remove_btn.setLabel('Remove')
        control.remove_btn = remove_btn

        if idx == 0:
            row = 0
            adv_row = 1
        else:
            row = idx * 2
            adv_row = row + 1

        control.adv_row = adv_row

        self.placeControl(control.label, row=row, column=0, rowspan=1, columnspan=1)
        self.placeControl(control.input_select_btn, row=row, column=1, rowspan=1, columnspan=3)
        self.placeControl(control.trigger_adv_mapping_btn, row=row, column=4, rowspan=1, columnspan=1)
        self.placeControl(control.remove_btn, row=row, column=5, rowspan=1, columnspan=1)

        self.connect_controls(control)

        if control.device.is_kbd() or control.device.is_mouse() or control.device.is_none_device():
            trigger_adv_mapping_btn.setEnabled(False)
            # Still visible for now, but disabled
            # trigger_adv_mapping_btn.setVisible(False)

        control.set_internal_navigation()

        self.controls[control.id] = control

        # TODO: Should be a dedicated method (set_navigation)
        self.add_ctrl_btn.controlUp(control.input_select_btn)
        if control.adv_on_flag:
            control.adv_select_mapping.controlDown(self.add_ctrl_btn)
        else:
            control.input_select_btn.controlDown(self.add_ctrl_btn)
        previous_control = None
        for _ctrl_id, _control in self.controls.iteritems():
            if _control.idx == control.idx-1:
                previous_control = _control
        if previous_control:
            if previous_control.adv_on_flag:
                control.input_select_btn.controlUp(previous_control.adv_select_mapping)
                previous_control.adv_select_mapping.controlDown(control.input_select_btn)
            else:
                control.input_select_btn.controlUp(previous_control.input_select_btn)
                previous_control.input_select_btn.controlDown(control.input_select_btn)

        if control.device.mapping:
            self.trigger_advanced(control)

    def connect_controls(self, control):
        self.connect(control.input_select_btn, lambda: self.select_input(control))
        self.connect(control.remove_btn, lambda: self.remove_input(control))
        self.connect(control.trigger_adv_mapping_btn, lambda: self.trigger_advanced(control))

    def select_input(self, control):
        available_devices = self.filter_input_devices()
        device_names = [_dev.name for _dev in available_devices]
        controller = xbmcgui.Dialog().select('Select Input Device', device_names)
        if controller == -1:
            return
        else:
            device = self.controller.find_device_by_name(device_names[controller])
            control.device = device
            control.input_select_btn.setLabel(device.name)
            if device.is_kbd() or device.is_mouse() or device.is_none_device():
                control.trigger_adv_mapping_btn.setEnabled(False)
            else:
                control.trigger_adv_mapping_btn.setEnabled(True)
            self.add_input_device(control.idx, device)

    def remove_input(self, control, dry=False):
        self.removeControls(control.controls_as_list())
        del_key = None
        for key, value in self.input_devices.iteritems():
            if value.name == control.device.name:
                del_key = key
        if not dry:
            try:
                self.remove_input_device(del_key)
            except KeyError:
                pass
            del self.controls[control.id]
            del control
            self.init_existing_controls()
            self.setFocus(self.add_ctrl_btn)

    def trigger_advanced(self, control):
        control.adv_on(self)
        control.set_internal_navigation()
        next_control = None
        for _ctrl_id, _control in self.controls.iteritems():
            if _control.idx == control.idx+1:
                next_control = _control
        if next_control:
            control.adv_select_mapping.controlDown(next_control.input_select_btn)
            next_control.input_select_btn.controlUp(control.adv_select_mapping)
        else:
            control.adv_select_mapping.controlDown(self.add_ctrl_btn)
            self.add_ctrl_btn.controlUp(control.adv_select_mapping)
        self.setFocus(control.input_select_btn)

    def unset_advanced(self, control):
        control.adv_off(self)
        control.set_internal_navigation()
        control.unset_mapping_file()
        for key, device in self.input_devices.iteritems():
                if device.name == control.device.name:
                    device.mapping = None
                    self.update_input_device(control.idx, device)
                    break
        next_control = None
        for _ctrl_id, _control in self.controls.iteritems():
            if _control.idx == control.idx+1:
                next_control = _control
        if next_control:
            control.input_select_btn.controlDown(next_control.input_select_btn)
            next_control.input_select_btn.controlUp(control.input_select_btn)
        else:
            control.input_select_btn.controlDown(self.add_ctrl_btn)
            self.add_ctrl_btn.controlUp(control.input_select_btn)
        self.setFocus(control.input_select_btn)

    def select_mapping(self, control):
        browser = xbmcgui.Dialog().browse(1, 'Select Mapping File', 'files', '.map|.conf', False, False,
                                          os.path.expanduser('~'))
        if browser:
            control.set_mapping_file(browser)
            for key, device in self.input_devices.iteritems():
                if device.name == control.device.name:
                    device.mapping = browser
                    self.update_input_device(control.idx, device)
                    break

    def create_mapping(self, control):
        map_name = xbmcgui.Dialog().input(self.controller.get_string('enter_filename'))

        progress_dialog = xbmcgui.DialogProgress()
        progress_dialog.create(
            self.controller.get_string('name'),
            self.controller.get_string('starting_mapping')
        )

        map_file = '%s/%s.map' % (os.path.expanduser('~'), map_name)

        success = self.controller.create_ctrl_map_new(progress_dialog, map_file, control.device)

        if success:
            confirmed = xbmcgui.Dialog().yesno(
                    self.controller.get_string('name'),
                    self.controller.get_string('mapping_success'),
                    self.controller.get_string('set_mapping_active')
            )

            if confirmed:
                control.set_mapping_file(map_file)
                for key, device in self.input_devices.iteritems():
                    if device.name == control.device.name:
                        device.mapping = map_file
                        self.update_input_device(control.idx, device)
                        break

        else:
            xbmcgui.Dialog().ok(
                    self.controller.get_string('name'),
                    self.controller.get_string('mapping_failure')
            )

    def init_existing_controls(self):
        if self.controls is not None:
            for key, value in self.controls.iteritems():
                self.remove_input(value, True)
            self.controls = {}

        del_keys = []
        for key, device in self.input_devices.iteritems():
            if not self.controller.find_device_by_name(device.name):
                del_keys.append(key)

        for key in del_keys:
            self.remove_input(key)

        for key, device in self.input_devices.iteritems():
            self.add_ctrl(device)

    def filter_input_devices(self):
        device_list = []
        current_ctrl_labels = [ctrl.input_select_btn.getLabel() for key, ctrl in self.controls.iteritems()]
        for device in self.available_devices:
            if device.name not in current_ctrl_labels:
                device_list.append(device)
        return device_list

    def add_input_device(self, ctrl_id, device):
        self.controller.add_input_device(ctrl_id, device)
        self.input_devices[ctrl_id] = device

    def remove_input_device(self, ctrl_id):
        self.controller.remove_input_device(ctrl_id)
        del self.input_devices[ctrl_id]

    def update_input_device(self, ctrl_id, device):
        self.controller.update_input_device(ctrl_id, device)

    def setAnimation(self, control):
        control.setAnimations(
            [
                ('WindowOpen', 'effect=fade start=0 end=100 time=300',),
                ('WindowClose', 'effect=fade start=100 end=0 time=300',)
            ]
        )
