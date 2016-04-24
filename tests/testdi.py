import unittest

import xbmcswift2

import resources.lib.core.logger
from resources.lib.di.requiredfeature import RequiredFeature
from resources.lib.nvhttp.simplecryptoprovider import SimpleCryptoProvider
from resources.lib.nvhttp.simplepairingmanager import SimplePairingManager


class TestScraperChain(unittest.TestCase):
    def testAttributesExist(self):
        core = RequiredFeature('core').request()
        self.assertEqual(hasattr(core, 'plugin'), True)
        self.assertEqual(hasattr(core, 'logger'), True)

    def testAttributeType(self):
        core = RequiredFeature('core').request()
        self.assertEqual(isinstance(core.plugin, xbmcswift2.Plugin), True)
        self.assertEqual(isinstance(core.logger, resources.lib.core.logger.Logger), True)

    def testAttributeAttributesExist(self):
        core = RequiredFeature('core').request()
        self.assertEqual(hasattr(core.logger, 'plugin'), True)

    def testAttributeAttributesType(self):
        core = RequiredFeature('core').request()
        self.assertEqual(isinstance(core.logger.plugin, xbmcswift2.Plugin), True)

    def testGetFeatureByTag(self):
        crypto_provider = RequiredFeature('crypto-provider').request()
        self.assertIsInstance(crypto_provider, SimpleCryptoProvider)
        self.assertEqual(hasattr(crypto_provider, 'config_helper'), True)
        self.assertIsNotNone(crypto_provider.config_helper)

        pairing_manager = RequiredFeature('pairing-manager').request()
        self.assertIsInstance(pairing_manager, SimplePairingManager)
