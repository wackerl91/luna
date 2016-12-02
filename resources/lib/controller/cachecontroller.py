from resources.lib.controller.basecontroller import BaseController, route


class CacheController(BaseController):
    def __init__(self, core, scraper_chain):
        self.core = core
        self.base_path = core.storage_path
        self.scraper_chain = scraper_chain

    @route("reset")
    def reset_cache(self):
        import xbmcgui
        confirmed = xbmcgui.Dialog().yesno(
            self.core.string('name'),
            self.core.string('reset_cache_warning')
        )

        if confirmed:
            self.scraper_chain.reset_cache()
