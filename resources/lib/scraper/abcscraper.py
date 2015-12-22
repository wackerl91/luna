from abc import ABCMeta, abstractmethod


class AbstractScraper(metaclass=ABCMeta):
    def __init__(self, addon_path):
        self.base_path = addon_path

    @abstractmethod
    def get_game_information(self, game_name):
        """
        Queries game information from API and returns it as a dict
        :type game_name: str
        :rtype: object
        """
        pass
