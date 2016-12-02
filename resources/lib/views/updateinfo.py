import os

import pyxbmct.addonwindow as pyxbmct

import xbmcaddon

from resources.lib.di.requiredfeature import RequiredFeature

_addon_path = xbmcaddon.Addon().getAddonInfo('path')

COLOR_FO = '0xFFE0B074'
COLOR_NF = '0xFF808080'
COLOR_HEADING = '0xFFD6D6D6'
COLOR_DETAILS = '0xFF707070'
COLOR_SELECTED = '0xFFF1F1F1'


class UpdateInfo(pyxbmct.AddonDialogWindow):
    core = RequiredFeature('core')

    def __init__(self, update, title=''):
        super(UpdateInfo, self).__init__(title)
        self.update = update
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
        self.version = None
        self.changelog = None
        self.button_update = None
        self.button_cancel = None

        self.setGeometry(1280, 720, 12, 6, padding=60)
        self.set_info_controls(update)
        self.set_active_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

    def set_info_controls(self, update):
        update_headline = 'Luna %s available' % update.update_version
        title_label = pyxbmct.Label(update_headline, alignment=pyxbmct.ALIGN_LEFT, font='XLarge', textColor=COLOR_HEADING)
        self.placeControl(title_label, 0, 0, 2, 3)

        changelog_label = pyxbmct.Label('Changelog', alignment=pyxbmct.ALIGN_LEFT, font='Med', textColor=COLOR_DETAILS)
        self.placeControl(changelog_label, 2, 0)

        self.changelog = pyxbmct.TextBox(font='Med')
        self.placeControl(self.changelog, 4, 0, 6, 6)
        self.changelog.setText(update.changelog)
        self.changelog.autoScroll(delay=5000, time=2000, repeat=10000)

    def set_active_controls(self):
        self.button_update = pyxbmct.Button('Update', focusTexture='', noFocusTexture='', focusedColor=COLOR_FO,
                                            textColor=COLOR_NF, font='Med', alignment=pyxbmct.ALIGN_LEFT)
        self.placeControl(self.button_update, 11, 0)
        self.connect(self.button_update, self.do_update)

        self.button_cancel = pyxbmct.Button('Cancel', focusTexture='', noFocusTexture='',
                                            focusedColor=COLOR_FO, textColor=COLOR_NF, font='Med',
                                            alignment=pyxbmct.ALIGN_LEFT)
        self.placeControl(self.button_cancel, 11, 1, columnspan=2)
        self.connect(self.button_cancel, self.cancel)

    def set_navigation(self):
        self.button_update.controlRight(self.button_cancel)
        self.button_update.controlLeft(self.button_cancel)
        self.button_cancel.controlRight(self.button_update)
        self.button_cancel.controlLeft(self.button_update)

        self.setFocus(self.button_update)

    def do_update(self):
        self.update.do_update()
        self.close()

    def cancel(self):
        self.close()

    def setAnimation(self, control):
        control.setAnimations(
            [
                ('WindowOpen', 'effect=fade start=0 end=100 time=500',),
                ('WindowClose', 'effect=fade start=100 end=0 time=500',)
            ]
        )
