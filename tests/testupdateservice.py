import unittest
from resources.lib.di.requiredfeature import RequiredFeature


class TestUpdateService(unittest.TestCase):
    def setUp(self):
        self.update_service = RequiredFeature('update-service').request()

    def testVersionCheck(self):
        self.update_service.check_for_update()
