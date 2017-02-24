import xbmcgui


class Action(object):
    def __init__(self, window, label, route):
        self.window = window
        self.label = label
        self._route = route

        self.window.addControl(label)

    def set_label_color(self):
        if self.label.getLabel()[1:6] != 'COLOR':
            self.label.setLabel(
                label='[COLOR FFE0B074]' + self.label.getLabel() + '[/COLOR]',
                font='Small'
            )

    def unset_label_color(self):
        if self.label.getLabel()[1:6] == 'COLOR':
            self.label.setLabel(
                label=self.label.getLabel()[16:-8],
                font='Small'
            )

    def get_main_control(self):
        return self.label

    def get_all_controls(self):
        return [self.label]

    def getId(self):
        return self.label.getId()

    def setVisible(self, value):
        self.label.setVisible(value)

    def setEnabled(self, value):
        self.label.setEnabled(value)

    def getPosition(self):
        return self.label.getPosition()

    def getY(self):
        return self.label.getY()

    def getX(self):
        return self.label.getX()

    def controlUp(self, control):
        self.label.controlUp(control)

    def controlDown(self, control):
        self.label.controlDown(control)

    def controlLeft(self, control):
        self.label.controlLeft(control)

    def controlRight(self, control):
        self.label.controlRight(control)

    def forward_input(self, actionId):
        focus_id = self.window.getFocusId()

        if focus_id:
            focused_item = self.window.getControl(focus_id)

            if focused_item == self.label:
                if actionId == xbmcgui.ACTION_SELECT_ITEM:
                    return self._route
