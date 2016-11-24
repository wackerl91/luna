import xbmcaddon
import xbmcgui


class HostContextMenu(xbmcgui.WindowXMLDialog):
    def __new__(cls, *args, **kwargs):
        return super(HostContextMenu, cls).__new__(cls, 'lunacontextmenu.xml', xbmcaddon.Addon().getAddonInfo('path'))

    def __init__(self, host, controller):
        super(HostContextMenu, self).__init__('lunacontextmenu.xml', xbmcaddon.Addon().getAddonInfo('path'))
        self.host = host
        self.controller = controller
        self.list = None

    def onInit(self):
        self.list = self.getControl(70)
        self.build_list()
        self.setFocus(self.list)

    def build_list(self):
        items = ['Wake Host', 'Remove Host']
        self.list.addItems(items)

    def onAction(self, action):
        if action == xbmcgui.ACTION_NAV_BACK:
            self.close()
        if self.getFocus() == self.list and action == xbmcgui.ACTION_SELECT_ITEM:
            selected_position = self.list.getSelectedPosition()
            if selected_position == 0:
                self.controller.render('host_wake', {'host': self.host})
                self.close()
            if selected_position == 1:
                self.controller.render('main_host_remove', {'host': self.host})
                self.close()
