import os
import unittest

import xbmcswift2


import resources.lib.core.logger
from resources.lib.di.requiredfeature import RequiredFeature
from resources.lib.nvhttp.cryptoprovider.cryptoproviderwrapper import CryptoProviderWrapper
from resources.lib.nvhttp.cryptoprovider.simplecryptoprovider import SimpleCryptoProvider
from resources.lib.nvhttp.pairingmanager.pairingmanagerwrapper import PairingManagerWrapper


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
        pairing_manager = RequiredFeature('pairing-manager').request()
        self.assertIsInstance(pairing_manager, PairingManagerWrapper)
        self.assertEqual(hasattr(pairing_manager, '_pairing_manager'), True)
        self.assertIsNone(pairing_manager._pairing_manager)

        crypto_provider = RequiredFeature('crypto-provider').request()
        self.assertIsInstance(crypto_provider, CryptoProviderWrapper)
        self.assertEqual(hasattr(crypto_provider, '_crypto_provider'), True)
        self.assertIsNone(crypto_provider._crypto_provider)
        asserted_path = os.path.join(os.path.expanduser('~'), '.cache/moonlight/')
        self.assertEqual(asserted_path, crypto_provider.get_key_dir())
        self.assertIsNotNone(crypto_provider._crypto_provider)
        self.assertIsInstance(crypto_provider._crypto_provider, SimpleCryptoProvider)

        self.assertRaises(NotImplementedError, crypto_provider.get_client_private_key)
