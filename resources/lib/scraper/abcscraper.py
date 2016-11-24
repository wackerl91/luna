import os
import subprocess

from abc import ABCMeta, abstractmethod, abstractproperty


class AbstractScraper:
    __metaclass__ = ABCMeta

    def __init__(self, plugin, core):
        self.plugin = plugin
        self.core = core
        self.base_path = self.plugin.storage_path

    @abstractproperty
    def name(self):
        """
        Returns human readable name of scraper
        :rtype: str
        :return: name
        """
        pass

    @abstractmethod
    def get_game_information(self, nvapp):
        """
        Queries game information from API and returns it as a dict
        :type nvapp: NvApp
        :rtype: dict
        """
        pass

    @abstractmethod
    def return_paths(self):
        """
        Returns a list of used cache paths by this scraper
        :rtype: list
        """
        pass

    @abstractmethod
    def is_enabled(self):
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
                if not os.path.exists(os.path.dirname(file_path)):
                    os.makedirs(os.path.dirname(file_path))
                with open(file_path, 'wb') as img:
                    curl = subprocess.Popen(['curl', '-XGET', url], stdout=subprocess.PIPE)
                    img.write(curl.stdout.read())
                    img.close()

            return file_path
        else:

            return None
