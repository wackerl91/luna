import sys
import threading
import xbmc

from resources.lib.di import featurebroker
from resources.lib.di.featurebroker import FeatureBroker
from resources.lib.di.requiredfeature import RequiredFeature
from resources.lib.routing.router import Router


class XBMCApplicationKernel(object):
    def __init__(self):
        self.featurebroker = None
        self.router = None

    def bootstrap(self, callback=None):
        xbmc.executebuiltin("Dialog.Close(busydialog)")
        try:
            self._bootstrap(callback)
        except Exception as e:
            xbmc.executebuiltin("Dialog.Close(busydialog)")
            xbmc.log("[script.luna.kernel]: Failed to start Luna: %s" % e.message, xbmc.LOGERROR)
            exc_type, exc_value, exc_tb = sys.exc_info()
            sys.excepthook(exc_type, exc_value, exc_tb)

    def _bootstrap(self, callback=None):
        xbmc.executebuiltin("ActivateWindow(busydialog)")

        xbmc.log("[script.luna.kernel]: Bootstrapping DI ...")
        xbmc.log("[script.luna.kernel]: Bootstrapping Router ...")

        self.featurebroker = FeatureBroker()
        featurebroker.features = self.featurebroker
        di_thread = threading.Thread(target=self.featurebroker._parse_config())

        self.router = Router()
        self.featurebroker.provide('router', Router)
        self.featurebroker.set_initialized('router', self.router)

        router_thread = threading.Thread(target=self.router._parse_config())

        di_thread.start()
        router_thread.start()

        di_thread.join()

        warmup_thread = None
        preload_thread = None

        if not di_thread.isAlive():
            self.featurebroker.execute_calls()
            xbmc.log("[script.luna.kernel]: Bootstrapping DI ... done")
            xbmc.log('[script.luna.kernel]: Warming up managers ...')
            warmup_thread = threading.Thread(target=self._warmup_repositories())
            warmup_thread.start()

        router_thread.join()
        if not router_thread.isAlive():
            xbmc.log("[script.luna.kernel]: Bootstrapping Router ... done")
            xbmc.log("[script.luna.kernel]: Pre-Loading Controllers ...")
            preload_thread = threading.Thread(target=self._preload_controllers)
            preload_thread.start()

        if not di_thread.isAlive() and not router_thread.isAlive():
            warmup_thread.join()
            preload_thread.join()

            if not warmup_thread.isAlive() and not preload_thread.isAlive():
                xbmc.executebuiltin("Dialog.Close(busydialog)")
                if callback:
                    try:
                        return callback()
                    except Exception, e:
                        exc_type, exc_value, exc_tb = sys.exc_info()
                        sys.excepthook(exc_type, exc_value, exc_tb)

    def _warmup_repositories(self):
        managers = featurebroker.features.get_tagged_features('manager')
        for manager in managers:
            xbmc.log("[script.luna.kernel]: Currently warming up: %s" % manager.name)
            RequiredFeature(manager.name).request()
        xbmc.log('[script.luna.kernel]: Warming up managers ... done')

    def _preload_controllers(self):
        from resources.lib.di.requiredfeature import RequiredFeature
        main_route = self.router.main_route
        controller = RequiredFeature(main_route.service[1:]).request()
        self.router.register(controller.__class__)

        for key, route in self.router.routing.iteritems():
            if not route.is_main_route:
                controller = RequiredFeature(route.service[1:]).request()
                self.router.register(controller.__class__)
        xbmc.log("[script.luna.kernel]: Pre-Loading Controllers ... done")
