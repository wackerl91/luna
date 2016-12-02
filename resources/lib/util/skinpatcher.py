import os
import shutil
import copy
import xml.etree.ElementTree as ElementTree


# This is taken from http://effbot.org/zone/element-lib.htm#prettyprint
def indent(elem, level=0):
    i = "\n" + level * "  "
    j = "\n" + (level - 1) * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem


class SkinPatcher:
    def __init__(self, core, addon):
        self.core = core
        self.addon = addon
        self.base_path = '/usr/share/kodi/addons/skin.osmc/16x9/'
        self.shortcut_path = '/usr/share/kodi/addons/skin.osmc/shortcuts/'
        self.widget = 'Includes_Widgets.xml'
        self.var = 'Variables.xml'
        self.home = 'Home.xml'
        self.override = 'overrides.xml'
        self.widget_backup = 'Includes_Widgets.backup'
        self.var_backup = 'Variables.backup'
        self.home_backup = 'Home.backup'
        self.override_backup = 'overrides.backup'
        self.id = None

        self.supported = self.core.get_active_skin() == 'skin.osmc' \
            and os.path.isfile(os.path.join(self.base_path, self.widget)) \
            and os.path.isfile(os.path.join(self.base_path, self.var)) \
            and os.path.isfile(os.path.join(self.base_path, self.home)) \
            and os.path.isfile(os.path.join(self.shortcut_path, self.override))

        self.rollback_supported = os.path.isfile(os.path.join(self.base_path, self.widget_backup)) \
            and os.path.isfile(os.path.join(self.base_path, self.var_backup)) \
            and os.path.isfile(os.path.join(self.base_path, self.home_backup)) \
            and os.path.isfile(os.path.join(self.shortcut_path, self.override_backup))

    def backup(self):
        shutil.copy(os.path.join(self.base_path, self.widget), os.path.join(self.base_path, self.widget_backup))
        shutil.copy(os.path.join(self.base_path, self.var), os.path.join(self.base_path, self.var_backup))
        shutil.copy(os.path.join(self.base_path, self.home), os.path.join(self.base_path, self.home_backup))
        shutil.copy(os.path.join(self.shortcut_path, self.override),
                    os.path.join(self.shortcut_path, self.override_backup))

    def patch(self):
        if self.supported:
            self.backup()
            self.patch_widget()
            self.patch_home()
            self.patch_var()
            self.patch_override()
            self.addon.set_setting('luna_widget_patched', 'true')
        else:
            print 'Not Supported'

    def patch_widget(self):
        xml_root = ElementTree.ElementTree(file=os.path.join(self.base_path, self.widget)).getroot()

        include = ElementTree.SubElement(xml_root, 'include', name="Luna")
        content = ElementTree.SubElement(include, 'content')

        for i in range(0, 20):
            item = ElementTree.SubElement(content, 'item')

            ElementTree.SubElement(item, 'icon').text = "$INFO[Window.Property(Luna.%s.icon)]" % i
            ElementTree.SubElement(item, 'thumb').text = "$INFO[Window.Property(Luna.%s.thumb)]" % i
            ElementTree.SubElement(item, 'label').text = "$INFO[Window.Property(Luna.%s.name)]" % i
            ElementTree.SubElement(item, 'property', name="fanart").text = "$INFO[Window.Property(Luna.%s.fanart)]" % i
            ElementTree.SubElement(item, 'onclick')\
                .text = "RunPlugin(plugin://script.luna/games/launch-from-widget/%s)" % i
            ElementTree.SubElement(item, 'visible').text = "!IsEmpty(Window.Property(Luna.%s.name))" % i

        indent(include)
        tree = ElementTree.ElementTree(xml_root)
        tree.write(os.path.join(self.base_path, self.widget))

    def patch_home(self):
        xml_root = ElementTree.ElementTree(file=os.path.join(self.base_path, self.home)).getroot()
        print self.addon.get_setting('luna_force_fanart')

        controls = xml_root.find('controls')
        control_group = None
        for control in controls:
            print control.get('type')
            if control.get('type') == 'image':
                print "Found Image Control"
                if self.addon.get_setting('luna_force_fanart', bool):
                    control.find('visible').text = "True"
                    print 'Visible Text is %s' % control.find('visible').text
            if control.get('type') == 'group':
                control_group = control
                break

        inner_control_group = None
        for control in control_group:
            if control.get('type') == 'group':
                inner_control_group = control_group
                break

        widget_control = None
        for control in inner_control_group:
            if control.get('type') == 'group':
                widget_control = control
                break

        inner_widget_control = None
        for control in widget_control:
            if control.get('id') is not None:
                inner_widget_control = control
                break

        current_max_id = ""
        myosmc_control = None
        for control in inner_widget_control:
            if control.get('id') is not None:
                current_max_id = control.get('id')
                myosmc_control = control

        current_max_id = int(current_max_id) + 1
        self.id = current_max_id

        luna_control = copy.deepcopy(myosmc_control)

        luna_control.set('id', str(current_max_id))
        luna_control.find('include').text = "Luna"
        luna_control.find('visible').text = "StringCompare(Container(9000).ListItem.Property(Widget),Luna)"

        luna_item_layout = luna_control.find('itemlayout')
        luna_item_layout.set('width', "270")
        luna_focus_layout = luna_control.find('focusedlayout')
        luna_focus_layout.set('width', "270")

        for control in luna_item_layout:
            if control.get('type') == 'image':
                control.find('width').text = "250"
            if control.find('texture') is not None and control.find('texture').text == 'common/black.png':
                control.find('texture').text = ""

        for control in luna_focus_layout:
            if control.get('type') == 'image':
                control.find('width').text = "250"
            if control.find('texture') is not None and control.find('texture').text == 'common/black.png':
                control.find('texture').text = ""

        inner_widget_control.append(luna_control)

        tree = ElementTree.ElementTree(xml_root)
        tree.write(os.path.join(self.base_path, self.home))

    def patch_var(self):
        xml_root = ElementTree.ElementTree(file=os.path.join(self.base_path, self.var)).getroot()

        label_group = None
        heading_group = None
        fanart_group = None

        for var in xml_root.findall('variable'):
            if var.get('name') == 'WidgetLabel':
                label_group = var
            if var.get('name') == 'WidgetHeading':
                heading_group = var
            if var.get('name') == 'WidgetFanart':
                fanart_group = var
            if label_group is not None and heading_group is not None and fanart_group is not None:
                break

        ElementTree.SubElement(label_group, "value",
                               condition="StringCompare(Container(9000).ListItem.Property(Widget),Luna)")\
            .text = "$INFO[Container(%s).ListItem.Label]" % self.id

        ElementTree.SubElement(heading_group, "value",
                               condition="StringCompare(Container(9000).ListItem.Property(Widget),Luna)")\
            .text = "Games"

        ElementTree.SubElement(fanart_group, "value",
                               condition="StringCompare(Container(9000).ListItem.Property(Widget),Luna)")\
            .text = "$INFO[Container(%s).ListItem.Property(fanart)]" % self.id

        tree = ElementTree.ElementTree(xml_root)
        tree.write(os.path.join(self.base_path, self.var))

    def patch_override(self):
        xml_root = ElementTree.ElementTree(file=os.path.join(self.shortcut_path, self.override)).getroot()

        ElementTree.SubElement(xml_root, "widget", label="Luna").text = "Luna"
        ElementTree.SubElement(xml_root, "widgetdefault", labelID="script.luna").text = "Luna"

        tree = ElementTree.ElementTree(xml_root)
        tree.write(os.path.join(self.shortcut_path, self.override))

    def rollback(self):
        if self.rollback_supported:
            shutil.move(os.path.join(self.base_path, self.widget_backup), os.path.join(self.base_path, self.widget))
            shutil.move(os.path.join(self.base_path, self.var_backup), os.path.join(self.base_path, self.var))
            shutil.move(os.path.join(self.base_path, self.home_backup), os.path.join(self.base_path, self.home))
            shutil.move(os.path.join(self.shortcut_path, self.override_backup), os.path.join(self.shortcut_path, self.override))
            self.addon.set_setting('luna_widget_patched', 'false')
