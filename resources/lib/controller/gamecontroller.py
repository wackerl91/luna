import resources.lib.core.corefunctions as core

from resources.lib.model.game import Game
from resources.lib.scraperchain import ScraperChain


def get_games():
    """
    Fills local game storage with scraper results (if enabled) or game names (if scrapers are disabled)
    """
    game_list = core.get_moonlight().list_games()
    storage = core.get_storage()
    cache = storage.raw_dict()
    storage.clear()

    for game_name in game_list:
        if core.get_plugin().get_setting('disable_scraper', bool):
            core.Logger.info('Scraper have been disabled, just adding game names to list.')
            storage[game_name] = Game(game_name, None)
        else:
            scraper = ScraperChain()

            if game_name in cache:
                if not storage.get(game_name):
                    storage[game_name] = cache.get(game_name)
            else:
                try:
                    storage[game_name] = scraper.query_game_information(game_name)
                except KeyError:
                    core.Logger.info('Key Error thrown while getting information for game {0}: {1}'
                                     .format(game_name,
                                             KeyError.message))
                    storage[game_name] = Game(game_name, None)

    storage.sync()


def get_games_as_list():
    """
    Parses contents of local game storage into a list that can be interpreted by Kodi
    :rtype: list
    """
    context_menu = [
        (
            core.string('addon_settings'),
            'XBMC.RunPlugin(%s)' % core.get_plugin().url_for(
                    endpoint='open_settings'
            )
        ),
        (
            core.string('full_refresh'),
            'XBMC.RunPlugin(%s)' % core.get_plugin().url_for(
                    endpoint='do_full_refresh'
            )
        )
    ]

    core.get_plugin().set_content('movies')
    storage = core.get_storage()

    if len(storage.raw_dict()) == 0:
        get_games()

    items = []
    for game in storage:
        items.append({
            'label':     game.name,
            'icon':      game.thumb,
            'thumbnail': game.thumb,
            'info': {
                'year':  game.year,
                'plot':  game.plot,
                'genre': game.genre,
                'originaltitle': game.name,
            },
            'replace_context_menu': True,
            'context_menu': context_menu,
            'path': core.get_plugin().url_for(
                    endpoint='launch_game',
                    game_id=game.name
            ),
            'properties': {
                'fanart_image': game.fanarts[0]
            }
        })

    return items
