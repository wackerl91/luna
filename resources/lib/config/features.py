from resources.lib.controller.configcontroller import ConfigController
from resources.lib.controller.gamecontroller import GameController
from resources.lib.core.corefunctions import Core
from resources.lib.core.coremonitor import CoreMonitor
from resources.lib.core.logger import Logger
from resources.lib.di.featurebroker import features
from resources.lib.scraper.omdbscraper import OmdbScraper
from resources.lib.scraper.scraperchain import ScraperChain
from resources.lib.scraper.tgdbscraper import TgdbScraper
from resources.lib.util.confighelper import ConfigHelper
from resources.lib.util.moonlighthelper import MoonlightHelper


def init_di():
    features.provide('logger', Logger())
    features.provide('core', Core())
    features.provide('config-helper', ConfigHelper())
    features.provide('core-monitor', CoreMonitor())
    features.provide('moonlight-helper', MoonlightHelper())
    features.provide('scraper-chain', ScraperChain())
    features.provide('config-controller', ConfigController())
    features.provide('game-controller', GameController())

    features.provide('omdb-scraper', OmdbScraper())
    features.tag('scraper-chain', 'omdb-scraper')
    features.provide('tgdb-scraper', TgdbScraper())
    features.tag('scraper-chain', 'tgdb-scraper')
