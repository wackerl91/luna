from xbmcgui import Action, Control


class _BaseWindow(object):
    ALIGN_LEFT = 0
    ALIGN_RIGHT = 1
    ALIGN_CENTER_X = 2
    ALIGN_CENTER_Y = 4
    ALIGN_CENTER = 6
    ALIGN_TRUNCATED = 8
    ALIGN_JUSTIFY = 10

    def __init__(self):
        self._connected_actions = {}
        self._connected_controls = {}

    def connect(self, element, _callable):
        if not callable(_callable):
            raise ValueError("Not a callable: %s" % str(_callable))

        if isinstance(element, int):
            if element not in self._connected_actions.keys():
                self._connected_actions[element] = _callable
        elif isinstance(element, Action):
            if element.getId() not in self._connected_actions.keys():
                self._connected_actions[element.getId()] = _callable
        elif isinstance(element, Control):
            if element.getId() not in self._connected_controls.keys():
                self._connected_controls[element.getId()] = _callable
        else:
            raise ValueError("Passed element is neither event nor control: %s" % str(element))

    def onAction(self, action):
        if isinstance(action, Action):
            action_id = action.getId()
        else:
            action_id = action

        if action_id in self._connected_actions.keys():
            self._connected_actions[action_id]()

    def onClick(self, controlId):
        if controlId in self._connected_controls.keys():
            self._connected_controls[controlId]()
