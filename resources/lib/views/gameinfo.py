import addonwindow as pyxbmct

from xbmcswift2 import xbmc, xbmcaddon

_addon_path = xbmcaddon.Addon().getAddonInfo('path')


class GameInfo(pyxbmct.AddonDialogWindow):
    def __init__(self, title=''):
        super(GameInfo, self).__init__(title)
        self.setGeometry(700, 450, 9, 4)
        self.set_info_controls()
        self.set_active_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

    def set_info_controls(self):
        no_int_label = pyxbmct.Label('Information output', alignment=pyxbmct.ALIGN_CENTER)
        self.placeControl(no_int_label, 0, 0, 1, 2)

        label_label = pyxbmct.Label('Label')
        self.placeControl(label_label, 1, 0)

        self.label = pyxbmct.Label('Simple Label')
        self.placeControl(self.label, 1, 1)

        fadelabel_label = pyxbmct.Label('FadeLabel')
        self.placeControl(fadelabel_label, 2, 0)

        self.fade_label = pyxbmct.FadeLabel()
        self.placeControl(self.fade_label, 2, 1)
        self.fade_label.addLabel('This should support very long strings')

        textbox_label = pyxbmct.Label('Textbox')
        self.placeControl(textbox_label, 3, 0)

        self.textbox = pyxbmct.TextBox()
        self.placeControl(self.textbox, 3, 1, 2, 1)
        self.textbox.setText('Text box. \n It should support multiple lines')

        image_label = pyxbmct.Label('Image')
        self.placeControl(image_label, 5, 0)

        self.image = pyxbmct.Image(os.path.join(_addon_path, 'resources/icons/controller.png'))
        self.placeControl(self.image, 5, 1, 2, 1)

    def set_active_controls(self):
        int_label = pyxbmct.Label('Interactive Controls', alignment=pyxbmct.ALIGN_CENTER)
        self.placeControl(int_label, 0, 2, 1, 2)

        radiobutton_label = pyxbmct.Label('Radiobutton')
        self.placeControl(radiobutton_label, 1, 2)

        self.radiobutton = pyxbmct.RadioButton('Off')
        self.placeControl(self.radiobutton, 1, 3)
        self.connect(self.radiobutton, self.radio_update)

        edit_label = pyxbmct.Label('Edit')
        self.placeControl(edit_label, 2, 2)

        self.edit = pyxbmct.Edit('Edit')
        self.placeControl(self.edit, 2, 3)
        self.edit.setText('Enter text here')

        list_label = pyxbmct.Label('List')
        self.placeControl(list_label, 3, 2)

        self.list_item_label = pyxbmct.Label('', textColor='0xFF808080')
        self.placeControl(self.list_item_label, 4, 2)

        self.list = pyxbmct.List()
        self.placeControl(self.list, 3, 3, 3, 1)
        items = ['Item {0}'.format(i) for i in range(1, 8)]
        self.list.addItems(items)

        self.connect(self.list, lambda: xbmc.executebuiltin('Notification(Note!, {0} selected.)'.format(
            self.list.getListItem(self.list.getSelectedPosition()).getLabel()
        )))

        self.connectEventList(
            [pyxbmct.ACTION_MOVE_UP,
             pyxbmct.ACTION_MOVE_DOWN],
            self.list_update
        )

        SLIDER_INIT = 25.0
        self.slider_value = pyxbmct.Label(str(SLIDER_INIT), alignment=pyxbmct.ALIGN_CENTER)
        self.placeControl(self.slider_value, 6, 3)

        slider_caption = pyxbmct.Label('Slider')
        self.placeControl(slider_caption, 7, 2)

        self.slider = pyxbmct.Slider()
        self.placeControl(self.slider, 7, 3, pad_y=10)
        self.slider.setPercent(SLIDER_INIT)
        self.connectEventList(
            [
                pyxbmct.ACTION_MOVE_LEFT,
                pyxbmct.ACTION_MOVE_RIGHT
            ],
            self.slider_update
        )

        button_label = pyxbmct.Label('Button')
        self.placeControl(button_label, 8, 2)

        self.button = pyxbmct.Button('Close')
        self.placeControl(self.button, 8, 3)
        self.connect(self.button, self.close)

    def set_navigation(self):
        self.button.controlUp(self.slider)
        self.button.controlDown(self.radiobutton)
        self.radiobutton.controlUp(self.button)
        self.radiobutton.controlDown(self.edit)
        self.edit.controlUp(self.radiobutton)
        self.edit.controlDown(self.list)
        self.list.controlUp(self.edit)
        self.list.controlDown(self.slider)
        self.slider.controlUp(self.list)
        self.slider.controlDown(self.button)

        self.setFocus(self.radiobutton)

    def slider_update(self):
        try:
            if self.getFocus() == self.slider:
                self.slider_value.setLabel('{:.1F}'.format(
                    self.slider.getPercent()
                ))
        except (RuntimeError, SystemError):
            pass

    def radio_update(self):
        if self.radiobutton.isSelected():
            self.radiobutton.setLabel('On')
        else:
            self.radiobutton.setLabel('Off')

    def list_update(self):
        try:
            if self.getFocus() == self.list:
                self.list_item_label.setLabel(self.list.getListItem(self.list.getSelectedPosition()).getLabel())
            else:
                self.list_item_label.setLabel('')
        except (RuntimeError, SystemError):
            pass

    def setAnimation(self, control):
        control.setAnimations(
            [
                ('WindowOpen', 'effect=fade start=0 end=100 time=500',),
                ('WindowClose', 'effect=fade start=100 end=0 time=500',)
            ]
        )
