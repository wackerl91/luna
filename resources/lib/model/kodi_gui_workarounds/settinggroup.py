import inspect

import xbmcgui


class SettingGroup(object):
    def __init__(self, window, label, control):
        self.window = window
        self.label = label
        self.control = control
        self.enabled = True
        self.visible = True
        self.enable_target_values = {}
        self.enable_target_controls = {}
        self.visible_target_values = {}
        self.visible_target_controls = {}

    def getId(self):
        return self.control.getId()

    def controlDown(self, control):
        self.control.controlDown(control)

    def controlLeft(self, control):
        self.control.controlLeft(control)

    def controlRight(self, control):
        self.control.controlRight(control)

    def controlUp(self, control):
        self.control.controlUp(control)

    def getPosition(self):
        return self.label.getPosition()

    def getX(self):
        return self.label.getX()

    def getY(self):
        return self.label.getY()

    def setEnabled(self, enabled):
        if enabled:
            enable_override = self.check_enable_condition()
        else:
            enable_override = enabled
        self.enabled = enable_override
        self.label.setEnabled(enable_override)
        self.control.setEnabled(enable_override)

    def setVisible(self, visible):
        if visible:
            visible_override = self.check_visible_condition()
        else:
            visible_override = visible
        self.visible = visible_override
        self.label.setVisible(visible_override)
        self.control.setVisible(visible_override)

    def getLabel(self):
        return self.label.getLabel()

    def setLabel(self, label='', font=None, textColor=None, disabledColor=None, shadowColor=None,
                 focusedColor=None, label2=''):
        args = inspect.getargspec(self.setLabel)
        _locals = locals()
        params = {}

        for arg in args.args:
            if _locals[arg] is not None and arg != 'self':
                params[arg] = _locals[arg]

        self.label.setLabel(**params)

    def check_enable_condition(self):
        all_conditions_met = True
        if len(self.enable_target_values) > 0:
            for condition_control_id, condition_value in self.enable_target_values.iteritems():
                condition_control = self.enable_target_controls[condition_control_id]
                if str(condition_control.get_value()).lower() != condition_value.lower():
                    all_conditions_met = False
                    break

        return all_conditions_met

    def check_visible_condition(self):
        all_conditions_met = True
        if len(self.visible_target_values) > 0:
            for condition_control_id, condition_value in self.visible_target_values.iteritems():
                condition_control = self.visible_target_controls[condition_control_id]
                if str(condition_control.get_value()).lower() != condition_value.lower():
                    all_conditions_met = False
                    break

        return all_conditions_met

    def append_enable_condition(self, condition_control, condition_value):
        self.enable_target_controls[condition_control.getId()] = condition_control
        self.enable_target_values[condition_control.getId()] = condition_value

    def append_visible_condition(self, condition_control, condition_value):
        self.visible_target_controls[condition_control.getId()] = condition_control
        self.visible_target_values[condition_control.getId()] = condition_value

    def get_value(self):
        from resources.lib.model.kodi_gui_workarounds.rotaryselect import RotarySelect
        if isinstance(self.control, RotarySelect):
            return self.control.get_selected_option()
        from resources.lib.model.kodi_gui_workarounds.slider import Slider
        if isinstance(self.control, Slider):
            return self.control.get_selected_option()
        if isinstance(self.control, xbmcgui.ControlRadioButton):
            if self.control.isSelected() == 1:
                return True
            else:
                return False

    def get_main_control(self):
        try:
            ctrl = getattr(self.control, 'get_main_control')()
        except AttributeError:
            ctrl = self.control

        return ctrl

    def is_visible(self):
        return self.visible

    def is_enabled(self):
        return self.enabled

    def update_state(self):
        self.setVisible(True)
        self.setEnabled(True)

    def get_all_controls(self):
        from resources.lib.model.kodi_gui_workarounds.rotaryselect import RotarySelect
        if isinstance(self.control, RotarySelect):
            return self.control.get_all_controls()
        from resources.lib.model.kodi_gui_workarounds.slider import Slider
        if isinstance(self.control, Slider):
            return self.control.get_all_controls()
        else:
            return [self.control]
