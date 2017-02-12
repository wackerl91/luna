from resources.lib.kernel.xbmcapplicationkernel import XBMCApplicationKernel

if __name__ == '__main__':
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

        # do some cleanup
        from resources.lib.di import featurebroker
        controller_list = featurebroker.features.get_tagged_features('controller')
        for definition in controller_list:
            instance = featurebroker.features.get_initialized(definition.name)
            if instance and hasattr(instance, 'window'):
                delattr(instance, 'window')


    XBMCApplicationKernel().bootstrap(callback)
