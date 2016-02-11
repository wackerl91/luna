def init_di():
    # Import when init is called instead of when this module is imported
    from resources.lib.controller.configcontroller import ConfigController
    from resources.lib.controller.gamecontroller import GameController
    from resources.lib.core.corefunctions import Core
    from resources.lib.core.coremonitor import CoreMonitor
    from resources.lib.core.logger import Logger
    from resources.lib.core.updateservice import UpdateService
    from resources.lib.di.featurebroker import features
    from resources.lib.scraper.omdbscraper import OmdbScraper
    from resources.lib.scraper.scraperchain import ScraperChain
    from resources.lib.scraper.tgdbscraper import TgdbScraper
    from resources.lib.scraper.igdbscraper import IgdbScraper
    from resources.lib.util.confighelper import ConfigHelper
    from resources.lib.util.moonlighthelper import MoonlightHelper

    features.provide('logger', Logger)
    features.provide('core', Core)
    features.provide('config-helper', ConfigHelper)
    features.provide('core-monitor', CoreMonitor)
    features.provide('moonlight-helper', MoonlightHelper)
    features.provide('config-controller', ConfigController)
    features.provide('game-controller', GameController)
    features.provide('update-service', UpdateService)

    # Singleton initialization
    features.provide('scraper-chain', ScraperChain())

    features.provide('omdb-scraper', OmdbScraper())
    features.tag('scraper-chain', 'omdb-scraper')
    features.provide('tgdb-scraper', TgdbScraper())
    features.tag('scraper-chain', 'tgdb-scraper')
    features.provide('igdb-scraper', IgdbScraper())
    features.tag('scraper-chain', 'igdb-scraper')
