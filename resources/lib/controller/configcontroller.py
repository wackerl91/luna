import os

import xbmcgui


class ConfigController:
    def __init__(self, container):
        """

        :type container: PluginContainer
        """
        self.container = container
        self.core = container.get_core()
        self.moonlight_helper = container.get_moonlight_helper()
        self.logger = container.get_core().logger

    def create_controller_mapping(self):
        self.logger.info('Starting mapping')

        controllers = ['XBOX', 'PS3', 'Wii']
        ctrl_type = xbmcgui.Dialog().select(self.core.string('choose_ctrl_type'), controllers)
        map_name = xbmcgui.Dialog().input(self.core.string('enter_filename'))

        progress_dialog = xbmcgui.DialogProgress()
        progress_dialog.create(
                self.core.string('name'),
                self.core.string('starting_mapping')
        )

        self.core.Logger.info('Trying to call subprocess')
        map_file = '%s/%s-%s.map' % (os.path.expanduser('~'), controllers[ctrl_type], map_name)

        success = self.moonlight_helper.create_ctrl_map(progress_dialog, map_file)

        if success:
            confirmed = xbmcgui.Dialog().yesno(
                    self.core.string('name'),
                    self.core.string('mapping_success'),
                    self.core.string('set_mapping_active')
            )

            self.core.Logger.info('Dialog Yes No Value: %s' % confirmed)

            if confirmed:
                self.container.get_plugin().set_setting('input_map', map_file)

        else:
            xbmcgui.Dialog().ok(
                    self.core.string('name'),
                    self.core.string('mapping_failure')
            )

    def pair_host(self):
        pair_dialog = xbmcgui.DialogProgress()
        pair_dialog.create(
                self.core.string('name'),
                'Starting Pairing'
        )

        success = self.moonlight_helper.pair_host(pair_dialog)

        if success:
            xbmcgui.Dialog().ok(
                    self.core.string('name'),
                    'Successfully paired'
            )
        else:
            confirmed = xbmcgui.Dialog().yesno(
                    self.core.string('name'),
                    'Pairing failed - do you want to try again?'
            )
            if confirmed:
                self.pair_host()
