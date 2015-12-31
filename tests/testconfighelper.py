import os
import shutil
import unittest

from xbmcswift2 import Plugin

from resources.lib.util.confighelper import ConfigHelper


class TestConfigHelper(unittest.TestCase):

    def setUp(self):
        path = os.path.join(os.path.expanduser('~'), 'LunaTestTemp/')
        if not os.path.exists(path):
            os.makedirs(path)
        self.addon_path = path
        self.bin_path = os.path.join(path, 'binary/bin')
        self.fake_settings = {
            'addon_path':                   self.addon_path,
            'binary_path':                  self.bin_path,
            'host_ip':                      '192.168.1.1',
            'enable_custom_res':            False,
            'resolution_width':             '',
            'resolution_height':            '',
            'resolution':                   '1920x1080',
            'framerate':                    '60',
            'graphics_optimizations':       False,
            'remote_optimizations':         False,
            'local_audio':                  False,
            'enable_custom_bitrate':        False,
            'bitrate':                      '',
            'packetsize':                   1024,
            'enable_custom_input':          True,
            'input_map':                    os.path.join(self.addon_path, 'input.map'),
            'input_device':                 os.path.join(self.addon_path, 'input.device'),
            'override_default_resolution':  False
        }

    def testConfigurationDump(self):
        plugin = Plugin()
        config = ConfigHelper(plugin)
        config._configure(**self.fake_settings)
        config._dump_conf()

        self.assertEqual(os.path.isfile(config.full_path), True)

    def testConfigurationCorrectness(self):
        plugin = Plugin()
        config = ConfigHelper(plugin)
        config._configure(**self.fake_settings)
        config._dump_conf()

        self.assertEqual(self.bin_path, config.get_section_setting('General', 'binpath'))
        self.assertEqual('192.168.1.1', config.get_section_setting('General', 'address'))
        self.assertEqual('60', config.get_section_setting('General', 'fps'))
        self.assertEqual('-1', config.get_section_setting('General', 'bitrate'))
        self.assertEqual('1024', config.get_section_setting('General', 'packetsize'))
        self.assertEqual(os.path.join(self.addon_path, 'input.map'), config.get_section_setting('General', 'mapping'))
        self.assertEqual(os.path.join(self.addon_path, 'input.device'), config.get_section_setting('General', 'input'))
        self.assertEqual('False', config.get_section_setting('General', 'sops'))
        self.assertEqual('False', config.get_section_setting('General', 'localaudio'))
        self.assertEqual('False', config.get_section_setting('General', 'remote'))

    def tearDown(self):
        path = os.path.join(os.path.expanduser('~'), 'LunaTestTemp/')
        shutil.rmtree(path, ignore_errors=True)
