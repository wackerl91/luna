import os

import pyxbmct
import xbmcaddon
import xbmcgui
from resources.lib.di.requiredfeature import RequiredFeature
from resources.lib.model.hostcontrolwrapper import HostControlWrapper

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
        alignment=pyxbmct.ALIGN_CENTER_X
    )


def create_label():
    return pyxbmct.Label(
        '',
        alignment=pyxbmct.ALIGN_LEFT,
        font='Med',
        textColor=COLOR_DETAILS
    )


class Main(pyxbmct.BlankFullWindow):
    def __init__(self, controller, title='', hosts=None):
        _ADDON_NAME = 'script.module.pyxbmct'
        _addon = xbmcaddon.Addon(id=_ADDON_NAME)
        _addon_path = _addon.getAddonInfo('path')
        _images = os.path.join(_addon_path, 'lib', 'pyxbmct', 'textures', 'default')
        del _ADDON_NAME
        del _addon
        del _addon_path

        super(Main, self).__init__()
        self.window_close_button = None

        self.addon = RequiredFeature('addon').request()
        self.core = RequiredFeature('core').request()
        self.host_manager = RequiredFeature('host-manager').request()
        self.logger = RequiredFeature('logger').request()

        self.controller = controller

        if hosts is None:
            hosts = {}
        self.hosts = hosts
        self.controls = {}

        self.tile_bg = None
        if self.core.get_active_skin() == 'skin.osmc':
            media_path = '/usr/share/kodi/addons/skin.osmc/media'
            if os.path.exists(media_path):
                self.tile_bg = os.path.join(media_path, 'dialogs/DialogBackground_old.png')

        background = '/home/osmc/.kodi/addons/script.luna/fanart.jpg'

        if background is not None:
            self.main_bg = xbmcgui.ControlImage(1, 1, 1280, 720, background)
            self.addControl(self.main_bg)

            self.main_bg_img = os.path.join(_images, 'AddonWindow', 'ContentPanel.png')
            # Fullscreen background image control.
            self.main_bg_overlay = xbmcgui.ControlImage(-20, -20, 1920, 1080, self.main_bg_img)
            self.addControl(self.main_bg_overlay)

        self.setGeometry(1280, 720, 13, 13)

        self.add_host_btn = None
        self.settings_btn = None

        # TODO: Add Luna Logo to top left corner
        self.place_settings_btn()
        self.init_existing_hosts()
        self.place_add_host_btn()

        self.setFocus(self.settings_btn)
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
        # xbmcgui.ACTION_CONTEXT_MENU

        self.init_controls()

    def place_add_host_btn(self):
        idx = len(self.controls)
        column = idx * 4 + 1

        self.add_host_btn = create_button()
        self.add_host_btn.setLabel('Add Host')
        tile_bg = pyxbmct.Image(self.tile_bg)
        self.placeControl(tile_bg, row=3, column=column, rowspan=3, columnspan=3)
        self.placeControl(self.add_host_btn, row=5, column=column, columnspan=3)
        self.connect(self.add_host_btn, self.controller.add_host)

    def place_settings_btn(self):
        print 'Placed Settings Btn'
        # setAnimations([('focus', 'effect=zoom end=90,247,220,56 time=0',)])
        self.settings_btn = create_button()
        self.settings_btn.setLabel('Settings')
        # Not selectable, animation not working
        # self.settings_btn = xbmcgui.ControlImage(200, 400, 200, 200, os.path.join(self.addon.getAddonInfo('path'), 'resources/icons/cog.png'))
        # self.settings_btn.setAnimations([('focus', 'effect=zoom end=90,247,220,56 time=0',)])
        tile_bg = pyxbmct.Image(self.tile_bg)
        self.placeControl(tile_bg, row=7, column=1, rowspan=3, columnspan=3)
        self.placeControl(self.settings_btn, row=9, column=1, columnspan=3)
        self.connect(self.settings_btn, self.controller.open_settings)

    def place_host_btn(self, host):
        idx = len(self.controls)
        self.logger.info('Adding Host with Index: ' + str(idx))
        host_ctrl = HostControlWrapper()
        host_ctrl.host = host
        host_ctrl.idx = idx

        tile_bg = self.create_tile_bg()
        host_ctrl.tile_bg = tile_bg

        host_ctrl_btn = create_button()
        host_ctrl_btn.setLabel(
            host.name,
        )
        host_ctrl.btn = host_ctrl_btn

        if idx == 0:
            column = 1
        else:
            column = idx * 4 + 1

        self.placeControl(host_ctrl.tile_bg, row=3, column=column, rowspan=3, columnspan=3)
        self.placeControl(host_ctrl.btn, row=5, column=column, rowspan=3, columnspan=3)

        self.connect_controls(host_ctrl)

        self.controls[idx] = host_ctrl

        host_ctrl.btn.controlDown(self.settings_btn)

        previous_host = None

        for _host_id, _host in self.controls.iteritems():
            if _host_id == host_ctrl.idx-1:
                previous_host = _host

        if previous_host:
            self.logger.info('Found previous host')
            host_ctrl.btn.controlLeft(previous_host.btn)
            previous_host.btn.controlRight(host_ctrl.btn)

        if self.add_host_btn:
            self.logger.info('Found add_host_btn')
            host_ctrl.btn.controlRight(self.add_host_btn)
            self.add_host_btn.controlLeft(host_ctrl.btn)

    def init_controls(self):
        self.add_host_btn.controlDown(self.settings_btn)
        self.settings_btn.controlUp(self.add_host_btn)

        if len(self.controls) > 0:
            self.logger.info('Found hosts, attaching controls')
            last_host = self.controls[len(self.controls) - 1]
            self.add_host_btn.controlLeft(last_host.btn)
            last_host.btn.controlRight(self.add_host_btn)
            self.logger.info('Found hosts, attaching controls.... done')

    def init_existing_hosts(self):
        for key, host in self.host_manager.get_hosts().iteritems():
            self.logger.info(host)
            self.place_host_btn(host)

    def connect_controls(self, host_ctrl):
        self.connect(host_ctrl.btn, lambda: self.controller.select_host(host_ctrl.host))

    def create_tile_bg(self):
        return pyxbmct.Image(self.tile_bg)

    def update(self):
        self.removeControl(self.add_host_btn)
        self.add_host_btn = None

        for _host_ctrl in self.controls:
            self.removeControl(_host_ctrl)
        self.controls = {}

        self.init_existing_hosts()
        self.place_add_host_btn()
        self.init_controls()

        self.setFocus(self.settings_btn)
