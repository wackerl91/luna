import os
import pyxbmct.addonwindow as pyxbmct

import xbmcaddon
import xbmcgui

from resources.lib.di.requiredfeature import RequiredFeature
from resources.lib.util.inputwrapper import InputWrapper

_addon_path = xbmcaddon.Addon().getAddonInfo('path')

COLOR_FO = '0xFFE0B074'
COLOR_NF = '0xFF808080'
COLOR_HEADING = '0xFFD6D6D6'
COLOR_DETAILS = '0xFF707070'
COLOR_SELECTED = '0xFFF1F1F1'


class SelectInput(pyxbmct.AddonDialogWindow):
    def __init__(self, title=''):
        print 'Init Called'
        super(SelectInput, self).__init__(title)
        self.plugin = RequiredFeature('plugin').request()
        self.core = RequiredFeature('core').request()
        self.available_devices = InputWrapper.list_all_devices()

        background = None
        if self.core.get_active_skin() == 'skin.osmc':
            media_path = '/usr/share/kodi/addons/skin.osmc/media'
            if os.path.exists(media_path):
                background = os.path.join(media_path, 'dialogs/DialogBackground_old.png')

        if background is not None:
            self.background.setImage(background)
            self.removeControl(self.title_background)
            self.removeControl(self.window_close_button)
            self.removeControl(self.title_bar)

        # init controls
        self.ctl_1_select = None
        self.ctl_2_select = None
        self.ctl_3_select = None
        self.ctl_4_select = None

        self.setGeometry(1280, 720, 12, 6, padding=60)
        self.set_labels()
        self.set_buttons()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

    def set_labels(self):
        ctl_1_label = pyxbmct.Label('Controller 1', alignment=pyxbmct.ALIGN_LEFT, font='Med', textColor=COLOR_DETAILS)
        self.placeControl(ctl_1_label, 0, 0, 1, 1)
        ctl_2_label = pyxbmct.Label('Controller 2', alignment=pyxbmct.ALIGN_LEFT, font='Med', textColor=COLOR_DETAILS)
        self.placeControl(ctl_2_label, 1, 0, 1, 1)
        ctl_3_label = pyxbmct.Label('Controller 3', alignment=pyxbmct.ALIGN_LEFT, font='Med', textColor=COLOR_DETAILS)
        self.placeControl(ctl_3_label, 2, 0, 1, 1)
        ctl_4_label = pyxbmct.Label('Controller 4', alignment=pyxbmct.ALIGN_LEFT, font='Med', textColor=COLOR_DETAILS)
        self.placeControl(ctl_4_label, 3, 0, 1, 1)

    def set_buttons(self):
        self.ctl_1_select = pyxbmct.Button(
            self.reverse_device(self.plugin.get_setting('input_device_1', unicode)),
            focusTexture='',
            noFocusTexture='',
            focusedColor=COLOR_FO,
            textColor=COLOR_NF,
            font='Med',
            alignment=pyxbmct.ALIGN_LEFT
        )
        self.placeControl(self.ctl_1_select, 0, 1, 1, 4)
        self.ctl_2_select = pyxbmct.Button(
            self.reverse_device(self.plugin.get_setting('input_device_2', unicode)),
            focusTexture='',
            noFocusTexture='',
            focusedColor=COLOR_FO,
            textColor=COLOR_NF,
            font='Med',
            alignment=pyxbmct.ALIGN_LEFT
        )
        self.placeControl(self.ctl_2_select, 1, 1, 1, 4)
        self.ctl_3_select = pyxbmct.Button(
            self.reverse_device(self.plugin.get_setting('input_device_3', unicode)),
            focusTexture='',
            noFocusTexture='',
            focusedColor=COLOR_FO,
            textColor=COLOR_NF,
            font='Med',
            alignment=pyxbmct.ALIGN_LEFT
        )
        self.placeControl(self.ctl_3_select, 2, 1, 1, 4)
        self.ctl_4_select = pyxbmct.Button(
            self.reverse_device(self.plugin.get_setting('input_device_4', unicode)),
            focusTexture='',
            noFocusTexture='',
            focusedColor=COLOR_FO,
            textColor=COLOR_NF,
            font='Med',
            alignment=pyxbmct.ALIGN_LEFT
        )
        self.placeControl(self.ctl_4_select, 3, 1, 1, 4)

        self.connect(self.ctl_1_select, self.select_ctl_1)
        self.connect(self.ctl_2_select, self.select_ctl_2)
        self.connect(self.ctl_3_select, self.select_ctl_3)
        self.connect(self.ctl_4_select, self.select_ctl_4)

    def set_navigation(self):
        self.ctl_1_select.controlDown(self.ctl_2_select)

        self.ctl_2_select.controlUp(self.ctl_1_select)
        self.ctl_2_select.controlDown(self.ctl_3_select)

        self.ctl_3_select.controlUp(self.ctl_2_select)
        self.ctl_3_select.controlDown(self.ctl_4_select)

        self.ctl_4_select.controlUp(self.ctl_3_select)

        self.setFocus(self.ctl_1_select)

    def select_ctl_1(self):
        setting = 'input_device_1'
        ctl = self.ctl_1_select
        self.call_selection(setting, ctl)

    def select_ctl_2(self):
        setting = 'input_device_2'
        ctl = self.ctl_2_select
        self.call_selection(setting, ctl)

    def select_ctl_3(self):
        setting = 'input_device_3'
        ctl = self.ctl_3_select
        self.call_selection(setting, ctl)

    def select_ctl_4(self):
        setting = 'input_device_4'
        ctl = self.ctl_4_select
        self.call_selection(setting, ctl)

    def call_selection(self, setting, ctl):
        available_devices = self.filter_devices()
        device_values = available_devices.values()
        controller = xbmcgui.Dialog().select('Select Input Device', device_values)
        if controller == -1:
            return
        else:
            print device_values[controller]
            controller_key = ''
            for dev, name in available_devices.iteritems():
                if name == device_values[controller]:
                    controller_key = dev
            if self.set_input_device(setting, controller_key):
                ctl.setLabel(device_values[controller])

    def set_input_device(self, setting, controller):
        print setting
        if controller is not '':
            controller = os.path.join('/dev/input/', controller)

        self.plugin.set_setting(setting, str(controller))
        return True

    def filter_devices(self):
        filtered_devices = self.available_devices.copy()
        del_keys = []
        for key, value in filtered_devices.iteritems():
            if value in [
                self.ctl_1_select.getLabel(),
                self.ctl_2_select.getLabel(),
                self.ctl_3_select.getLabel(),
                self.ctl_4_select.getLabel()
            ]:
                del_keys.append(key)
        for key in del_keys:
            del filtered_devices[key]
        filtered_devices[''] = 'None (Disabled)'
        return filtered_devices

    def reverse_device(self, key):
        return self.available_devices.get(os.path.basename(key), 'None (Disabled)')
