class RotarySelect(object):
    def __init__(self, window, btn_up, btn_down, label, select_options, selected_index=0):
        self.window = window
        self.btn_up = btn_up
        self.btn_down = btn_down
        self.label = label
        self.select_options = select_options
        self.selected_index = selected_index

        self.window.addControls([btn_down, btn_up, label])

        self.btn_up.controlLeft(self.btn_down)
        self.btn_down.controlRight(self.btn_up)

        self.set_selected()

    def set_selected(self):
        if self.selected_index < 0:
            self.selected_index = 0
        elif self.selected_index > len(self.select_options) - 1:
            self.selected_index = len(self.select_options) - 1

        self.label.setLabel(self.select_options[self.selected_index])
        return

    def forward_input(self, action_id):
        focus_id = self.window.getFocusId()
        focused_item = None

        if focus_id:
            focused_item = self.window.getControl(focus_id)

        if focused_item and action_id == 7:
            if focused_item == self.btn_up:
                self.selected_index -= 1
                self.set_selected()
                self.set_label_color()
            if focused_item == self.btn_down:
                self.selected_index += 1
                self.set_selected()
                self.set_label_color()
        else:
            if not focused_item or (focused_item != self.btn_up and focused_item != self.btn_down):
                self.unset_label_color()
            else:
                self.set_label_color()

    def get_selected_option(self):
        return self.select_options[self.selected_index]

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
        return self.btn_down

    def get_all_controls(self):
        return [
            self.btn_down,
            self.btn_up
        ]

    def getId(self):
        return self.btn_down.getId()

    def setVisible(self, value):
        self.btn_up.setVisible(value)
        self.btn_down.setVisible(value)
        self.label.setVisible(value)

    def setEnabled(self, value):
        self.btn_up.setEnabled(value)
        self.btn_down.setEnabled(value)
        self.label.setEnabled(value)

    def setEnableCondition(self, condition):
        self.btn_up.setEnableCondition(condition)
        self.btn_down.setEnableCondition(condition)
        self.label.setEnableCondition(condition)

    def setVisibleCondition(self, condition):
        self.btn_up.setVisibleCondition(condition)
        self.btn_down.setVisibleCondition(condition)
        self.label.setVisibleCondition(condition)

    def getPosition(self):
        return self.label.getPosition()

    def getY(self):
        return self.label.getY()

    def getX(self):
        return self.label.getX()

    def controlUp(self, control):
        self.btn_up.controlUp(control)
        self.btn_down.controlUp(control)

    def controlDown(self, control):
        self.btn_up.controlDown(control)
        self.btn_down.controlDown(control)

    def controlLeft(self, control):
        self.btn_down.controlLeft(control)
