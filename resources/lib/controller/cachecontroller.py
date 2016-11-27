import os
import shutil

from resources.lib.controller.basecontroller import BaseController, route


class CacheController(BaseController):
    def __init__(self, core, plugin, game_manager, logger):
        self.core = core
        self.base_path = plugin.storage_path
        self.game_manager = game_manager
        self.logger = logger

        # TODO: This is a workaround until I can find a way to pull this information from the scraper chain properly
        self.art_cache = os.path.join(self.base_path, 'art/')
        self.api_cache = os.path.join(self.base_path, 'api_cache/')

    @route("reset")
    def reset_cache(self):
        import xbmcgui
        confirmed = xbmcgui.Dialog().yesno(
            self.core.string('name'),
            self.core.string('reset_cache_warning')
        )

        if confirmed:
            self.logger.info("Reset cache requested ...")
            self.game_manager.clear()

            for path in [self.art_cache, self.api_cache]:
                self.logger.info("Attempting to clear path: %s" % path)
                if os.path.exists(path):
                    self.logger.info("Clearing path: %s" % path)
                    shutil.rmtree(path, ignore_errors=True)
