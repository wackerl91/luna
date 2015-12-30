import os

import pyxbmct.addonwindow as pyxbmct

from xbmcswift2 import xbmc, xbmcaddon, xbmcgui

_addon_path = xbmcaddon.Addon().getAddonInfo('path')


class GameInfo(pyxbmct.AddonDialogWindow):
    def __init__(self, container, game, title=''):
        super(GameInfo, self).__init__(title)
        self.container = container
        self.game = game
        background = None
        if container.get_core().get_active_skin() == 'skin.osmc':
            media_path = '/usr/share/kodi/addons/skin.osmc/media'
            if os.path.exists(media_path):
                background = os.path.join(media_path, 'dialogs/DialogBackground_old.png')

        if background is not None:
            self.background.setImage(background)
            self.removeControl(self.title_background)
            self.removeControl(self.window_close_button)
            self.removeControl(self.title_bar)

        self.setGeometry(1280, 720, 12, 6, padding=50)
        self.set_info_controls(game)
        self.set_active_controls(game)
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

    def set_info_controls(self, game):
        title_label = pyxbmct.Label(game.name, alignment=pyxbmct.ALIGN_LEFT, font='font14')
        self.placeControl(title_label, 0, 0, 2, 3)

        self.image = pyxbmct.Image(game.poster)
        self.placeControl(self.image, 2, 0, 6, 1)

        genre_label = pyxbmct.Label('Genre', alignment=pyxbmct.ALIGN_LEFT)
        self.placeControl(genre_label, 2, 2)
        self.genre = pyxbmct.Label(game.get_genre_as_string(), alignment=pyxbmct.ALIGN_LEFT)
        self.placeControl(self.genre, 2, 3, columnspan=3)

        year_label = pyxbmct.Label('Year', alignment=pyxbmct.ALIGN_LEFT)
        self.placeControl(year_label, 3, 2)
        self.year = pyxbmct.Label(game.year, alignment=pyxbmct.ALIGN_LEFT)
        self.placeControl(self.year, 3, 3)

        self.plot = pyxbmct.TextBox()
        self.placeControl(self.plot, 4, 2, 6, 3)
        self.plot.setText(game.plot)

    def set_active_controls(self, game):
        self.button_play = pyxbmct.Button('Play', focusTexture='', noFocusTexture='', focusedColor='0xFFE50000')
        self.placeControl(self.button_play, 11, 0)
        self.connect(self.button_play, self.launch_game)

        self.button_fanart = pyxbmct.Button('Choose Fanart', focusTexture='', noFocusTexture='',
                                            focusedColor='0xFFE50000')
        self.placeControl(self.button_fanart, 11, 1)
        self.connect(self.button_fanart, self.select_fanart)

    def set_navigation(self):
        self.button_play.controlRight(self.button_fanart)
        self.button_play.controlLeft(self.button_fanart)
        self.button_fanart.controlRight(self.button_play)
        self.button_fanart.controlLeft(self.button_play)

        self.setFocus(self.button_play)

    def launch_game(self):
        xbmc.executebuiltin('XBMC.RunPlugin(%s)' % self.container.get_plugin().url_for(
                endpoint='launch_game',
                game_id=self.game.name))

    def select_fanart(self):
        browser = xbmcgui.Dialog().browse(2, 'Select Fanart', 'files', '.jpg|.png', False, False,
                                          self.game.fanart[0])
        self.game.selected_fanart = browser
        self.container.get_core().get_storage().update(self.game)
        self.container.get_core().get_storage().sync()

    def setAnimation(self, control):
        control.setAnimations(
                [
                    ('WindowOpen', 'effect=fade start=0 end=100 time=500',),
                    ('WindowClose', 'effect=fade start=100 end=0 time=500',)
                ]
        )
