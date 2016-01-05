import os
import shutil
import unittest
import resources.lib.config.bootstrap as bootstrapper

from resources.lib.di.requiredfeature import RequiredFeature


class TestUpdateService(unittest.TestCase):
    bootstrapper.bootstrap()

    def setUp(self):
        self.update_service = RequiredFeature('update-service').request()

    def testVersionCheck(self):
        self.update_service.check_for_update()
