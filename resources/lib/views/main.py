import os

import xbmcaddon
import xbmcgui
from resources.lib.views.hostcontextmenu import HostContextMenu


class Main(xbmcgui.WindowXML):
    def __new__(cls, *args, **kwargs):
        return super(Main, cls).__new__(cls, 'main.xml', xbmcaddon.Addon().getAddonInfo('path'))

    def __init__(self, controller, hosts):
        super(Main, self).__init__('main.xml', xbmcaddon.Addon().getAddonInfo('path'))
        self.controller = controller
        self.hosts = hosts
        self.list = None
        self.host_index_key_map = {}
        self.options_list = None
        self.settings_item = None
        self.add_host_item = None
        self.controller_config_item = None
        self.audio_config_item = None

    def onInit(self):
        self.list = self.getControl(102)
        self.options_list = self.getControl(103)
        self.list.reset()
        self.options_list.reset()
        self.build_list()
        if len(self.host_index_key_map) > 0:
            self.setFocusId(102)
        else:
            self.setFocusId(103)

    def build_list(self):
        items = []
        i = 0
        for key, host in self.hosts.iteritems():
            item = xbmcgui.ListItem()
            item.setLabel(host.name)
            item.setProperty('state', str(host.state))
            item.setProperty('uuid', host.uuid)
            item.setThumbnailImage(
                os.path.join(xbmcaddon.Addon().getAddonInfo('path'), 'resources/icons/host.png'))

            items.append(item)
            self.host_index_key_map[host.uuid] = i
            i += 1

        self.list.addItems(items)

        self.settings_item = xbmcgui.ListItem('Settings')

        self.settings_item.setThumbnailImage(
            os.path.join(xbmcaddon.Addon().getAddonInfo('path'), 'resources/icons/cog.png'))

        self.controller_config_item = xbmcgui.ListItem('Controller Configuration')
        self.controller_config_item.setThumbnailImage(
            os.path.join(xbmcaddon.Addon().getAddonInfo('path'), 'resources/icons/controller.png'))

        self.audio_config_item = xbmcgui.ListItem('Audio Configuration')
        self.audio_config_item.setThumbnailImage(
            os.path.join(xbmcaddon.Addon().getAddonInfo('path'), 'resources/icons/audio.png'))

        self.add_host_item = xbmcgui.ListItem('Add Host')
        self.add_host_item.setThumbnailImage(
            os.path.join(xbmcaddon.Addon().getAddonInfo('path'), 'resources/icons/add.png'))

        self.options_list.addItems(
            [self.settings_item, self.controller_config_item, self.audio_config_item, self.add_host_item, ])

    def update(self):
        self.hosts = self.controller.get_hosts()
        self.list.reset()
        self.options_list.reset()
        self.host_index_key_map.clear()
        self.build_list()

    def update_host_status(self, hosts):
        while len(hosts) != len(self.host_index_key_map):
            import xbmc
            xbmc.sleep(500)

        for key, host in hosts.iteritems():
            index = self.host_index_key_map[key]
            list_item = self.list.getListItem(index)
            list_item.setProperty('state', str(host[0].state))

        return

    def onAction(self, action):
        if action == xbmcgui.ACTION_NAV_BACK:
            self.close()

        focus_item = self.getFocus()
        if focus_item == self.options_list:
            if action == xbmcgui.ACTION_SELECT_ITEM:
                # TODO: Assign actions as item properties and call them
                if self.options_list.getSelectedPosition() == 0:
                    self.controller.render('settings_index')
                if self.options_list.getSelectedPosition() == 1:
                    self.controller.render('controller_select')
                if self.options_list.getSelectedPosition() == 2:
                    self.controller.render('audio_select')
                if self.options_list.getSelectedPosition() == 3:
                    self.controller.render('main_add_host')

        if focus_item == self.list:
            if action == xbmcgui.ACTION_CONTEXT_MENU:
                selected_item = self.list.getSelectedItem()
                host = self.hosts[selected_item.getProperty('uuid')]

                window = HostContextMenu(host, self.controller)
                window.doModal()
                del window
                if len(self.host_index_key_map) > 0:
                    self.setFocusId(102)
                else:
                    self.setFocusId(103)
            if action == xbmcgui.ACTION_SELECT_ITEM:
                selected_item = self.list.getSelectedItem()
                host = self.hosts[selected_item.getProperty('uuid')]
                self.controller.render('main_host_select', {'host': host})
