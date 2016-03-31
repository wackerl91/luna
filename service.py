import xbmcaddon

__addon__ = xbmcaddon.Addon()

if __name__ == '__main__':
    if __addon__.getSetting("luna_widget_enable") == 'true':
        from xbmcswift2 import xbmcgui
        from resources.lib.di.requiredfeature import RequiredFeature
        plugin = RequiredFeature('plugin').request()
        WINDOW = xbmcgui.Window(10000)
        core = RequiredFeature('core').request()
        storage = core.get_storage()

        sorted_list = sorted(storage.raw_dict().keys())

        sorted_storage = plugin.get_storage('sorted_game_storage')
        sorted_storage.clear()

        for i, game_name in enumerate(sorted_list):
            game = storage.get(game_name)
            WINDOW.setProperty('Luna.%s.name' % i, game.name)
            WINDOW.setProperty('Luna.%s.icon' % i, game.get_selected_poster())
            WINDOW.setProperty('Luna.%s.thumb' % i, game.get_selected_poster())
            WINDOW.setProperty('Luna.%s.fanart' % i, game.get_selected_fanart().get_original())
            sorted_storage[i] = game_name

        sorted_storage.sync()
