import xbmc
from resources.lib.kernel.xbmcapplicationkernel import XBMCApplicationKernel

if __name__ == '__main__':
    import sys
    xbmc.log(str(sys.argv))

    # TODO: This is sometimes called before main controller is known to router
    def callback():
        from resources.lib.di.requiredfeature import RequiredFeature
        import threading
        RequiredFeature('core').request().check_script_permissions()
        updater = RequiredFeature('update-service').request()
        update_thread = threading.Thread(target=updater.check_for_update)
        update_thread.start()
        router = RequiredFeature('router').request()
        router.render('main_index')

    XBMCApplicationKernel().bootstrap(callback)
