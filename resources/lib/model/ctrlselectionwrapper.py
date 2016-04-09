class CtrlSelectionWrapper(object):
    def __init__(self):
        self.id = None
        self.idx = None
        self.label = None
        self.input_select_btn = None
        self.trigger_adv_mapping_btn = None
        self.remove_btn = None
        self.adv_row = None
        self.adv_select_mapping = None
        self.adv_create_mapping = None
        self.adv_remove_mapping = None
        self.adv_on_flag = False
        self.device = None

    def set_internal_navigation(self):
        if self.adv_on_flag:
            self.input_select_btn.controlRight(self.remove_btn)
            self.remove_btn.controlLeft(self.input_select_btn)
            self.input_select_btn.controlDown(self.adv_select_mapping)
            self.adv_select_mapping.controlUp(self.input_select_btn)
            self.adv_select_mapping.controlRight(self.adv_create_mapping)
            self.adv_create_mapping.controlRight(self.adv_remove_mapping)
            self.adv_remove_mapping.controlLeft(self.adv_create_mapping)
            self.adv_create_mapping.controlLeft(self.adv_select_mapping)
            self.trigger_adv_mapping_btn.setEnabled(False)
        else:
            self.input_select_btn.controlRight(self.trigger_adv_mapping_btn)
            self.trigger_adv_mapping_btn.controlRight(self.remove_btn)
            self.remove_btn.controlLeft(self.trigger_adv_mapping_btn)
            self.trigger_adv_mapping_btn.controlLeft(self.input_select_btn)
        pass

    def adv_on(self, view):
        from resources.lib.views import selectinput
        self.adv_on_flag = True
        self.adv_select_mapping = selectinput.create_button()
        if self.device.mapping:
            self.adv_select_mapping.setLabel(self.device.mapping)
        else:
            self.adv_select_mapping.setLabel('Select Mapping')
        self.adv_create_mapping = selectinput.create_button()
        self.adv_create_mapping.setLabel('Create Mapping')
        self.adv_remove_mapping = selectinput.create_button()
        self.adv_remove_mapping.setLabel('Remove')

        view.placeControl(self.adv_select_mapping, row=self.adv_row, column=1, rowspan=1, columnspan=3)
        view.placeControl(self.adv_create_mapping, row=self.adv_row, column=4, rowspan=1, columnspan=1)
        view.placeControl(self.adv_remove_mapping, row=self.adv_row, column=5, rowspan=1, columnspan=1)

        view.connect(self.adv_select_mapping, lambda: view.select_mapping(self))
        view.connect(self.adv_create_mapping, lambda: view.create_mapping(self))
        view.connect(self.adv_remove_mapping, lambda: view.unset_advanced(self))

    def adv_off(self, view):
        self.adv_on_flag = False
        view.removeControls(self.advanced_controls_as_list())
        self.trigger_adv_mapping_btn.setEnabled(True)

    def controls_as_list(self):
        control_list = [self.label, self.input_select_btn, self.trigger_adv_mapping_btn, self.remove_btn]
        if self.adv_on_flag:
            control_list.append(self.adv_select_mapping)
            control_list.append(self.adv_create_mapping)
            control_list.append(self.adv_remove_mapping)
        return control_list

    def advanced_controls_as_list(self):
        return [self.adv_select_mapping, self.adv_create_mapping, self.adv_remove_mapping]

    def set_mapping_file(self, browser):
        self.device.mapping = browser
        self.adv_select_mapping.setLabel(browser)

    def unset_mapping_file(self):
        self.device.mapping = None
        self.adv_select_mapping.setLabel('Select Mapping')
