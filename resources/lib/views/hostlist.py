import xbmcaddon
import xbmcgui


# TODO: Needs styling
class HostList(xbmcgui.WindowXMLDialog):
    def __new__(cls, *args, **kwargs):
        return super(HostList, cls).__new__(cls, 'hostlist.xml', xbmcaddon.Addon().getAddonInfo('path'))

    def __init__(self, hosts):
        super(HostList, self).__init__('hostlist.xml', xbmcaddon.Addon().getAddonInfo('path'))
        self.hosts = hosts
        self.selected_host = None
        self.list = None

    def onInit(self):
        self.list = self.getControl(202)
        self.list.reset()
        self.build_list()
        self.setFocus(self.list)

    def build_list(self):
        items = []
        for key, host in self.hosts.iteritems():
            item = xbmcgui.ListItem()
            item.setLabel(host.name)
            item.setLabel2(host.local_ip)
            item.setProperty('gpu_type', host.gpu_type)
            item.setProperty('uuid', host.uuid)

            items.append(item)

        self.list.addItems(items)

    def onAction(self, action):
        if action == xbmcgui.ACTION_NAV_BACK:
            self.close()

        focus_item_id = self.getFocusId()

        if focus_item_id:
            focus_item = self.getControl(focus_item_id)

            if focus_item == self.list:
                if action == xbmcgui.ACTION_SELECT_ITEM:
                    selected_item = self.list.getSelectedItem()
                    try:
                        selected_host = self.hosts[selected_item.getProperty('uuid')]
                        self.selected_host = selected_host
                        self.close()
                    except KeyError:
                        pass
