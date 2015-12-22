import os
import subprocess

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

    @staticmethod
    def _set_up_path(path):
        if not os.path.exists(path):
            os.makedirs(path)

        return path

    @staticmethod
    def _dump_image(base_path, url):
        if url != 'N/A':
            file_path = os.path.join(base_path, os.path.basename(url))
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as img:
                    curl = subprocess.Popen(['curl', '-XGET', url], stdout=subprocess.PIPE)
                    img.write(curl.stdout.read())
                    img.close()

            return file_path
        else:

            return None
