# coding=utf-8
import xbmcaddon
import xbmcgui
from resources.lib.views.windowxmldialog import WindowXMLDialog


class GameInfo(WindowXMLDialog):
    def __new__(cls, *args, **kwargs):
        return super(GameInfo, cls).__new__(cls, 'gameinfo.xml', xbmcaddon.Addon().getAddonInfo('path'))

    def __init__(self, controller, host, game):
        super(GameInfo, self).__init__('gameinfo.xml', xbmcaddon.Addon().getAddonInfo('path'))
        self.controller = controller
        self.host = host
        self.game = game
        self.list = None
        self.play_btn = None
        self.select_poster_btn = None
        self.select_fanart_btn = None

    def onInit(self):
        self.list = self.getControl(51)
        self.play_btn = self.getControl(52)
        self.select_poster_btn = self.getControl(53)
        self.select_fanart_btn = self.getControl(54)
        self.setFocus(self.play_btn)

        item = xbmcgui.ListItem()
        item.setLabel(self.game.name)
        item.setIconImage(self.game.get_selected_poster())
        item.setThumbnailImage(self.game.get_selected_poster())
        item.setInfo('video', {
            'year': self.game.year,
            'plot': self.game.plot,
            'genre': self.game.genre,
            'originaltitle': self.game.name
        })
        item.setProperty('icon', self.game.get_selected_poster())
        item.setProperty('fanart', self.game.get_selected_fanart().get_original())
        item.setProperty('year_genre', '%s • %s' % (self.game.year, ', '.join(self.game.genre)))
        item.setProperty('description', self.game.plot)
        item.setProperty('id', self.game.id)

        self.list.addItems([item])

        self.connect(xbmcgui.ACTION_NAV_BACK, self.close)
        self.connect(self.play_btn, lambda: self.controller.render("game_launch", {'game': self.game}))
        self.connect(self.select_poster_btn, lambda: self.controller.select_cover_art(self.game, item))
        self.connect(self.select_fanart_btn, lambda: self.controller.select_fanart(self.game, item))
