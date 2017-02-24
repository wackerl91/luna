import xbmcgui


class Slider(object):
    def __init__(self, window, label, slider_range, initial):
        self.window = window
        self.label = label
        self.slider_range = slider_range
        self.selected_index = 0

        for key, value in enumerate(self.slider_range):
            if int(value) == int(initial):
                self.selected_index = key

        self.window.addControl(label)
        self.set_selected()

    def set_selected(self):
        if self.selected_index < 0:
            self.selected_index = 0
        elif self.selected_index > len(self.slider_range) - 1:
            self.selected_index = len(self.slider_range) - 1

        self.label.setLabel(str(self.slider_range[self.selected_index]))
        return

    def forward_input(self, action_id):
        # TODO: Pass focus ID and compare it to label ID
        focus_id = self.window.getFocusId()
        focused_item = None

        if focus_id:
            focused_item = self.window.getControl(focus_id)

        if focused_item and focused_item == self.label:
            if action_id == xbmcgui.ACTION_MOVE_LEFT:
                self.selected_index -= 1
                self.set_selected()
                self.set_label_color()
            elif action_id == xbmcgui.ACTION_MOVE_RIGHT:
                self.selected_index += 1
                self.set_selected()
                self.set_label_color()
            else:
                self.set_label_color()
        else:
            self.unset_label_color()

    def get_selected_option(self):
        return self.slider_range[self.selected_index]

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
        pass
