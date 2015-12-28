from resources.lib.confighelper import ConfigHelper
from resources.lib.moonlighthelper import MoonlightHelper
from resources.lib.scraperchain import ScraperChain


class PluginContainer:
    def __init__(self, plugin):
        self.plugin = plugin
        self.config_helper = ConfigHelper()
        self.moonlight_helper = MoonlightHelper()
        self.scraper_chain = ScraperChain()

    def get_plugin(self):
        return self.plugin

    def get_config_helper(self):
        return self.config_helper

    def get_moonlight_helper(self):
        return self.moonlight_helper

    def get_scraper_chain(self):
        return self.scraper_chain
