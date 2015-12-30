import os
import subprocess

from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element

from abcscraper import AbstractScraper


class TgdbScraper(AbstractScraper):
    def __init__(self, addon_path):
        AbstractScraper.__init__(self, addon_path)
        self.api_url = 'http://thegamesdb.net/api/GetGame.php?name=%s'
        self.cover_cache = self._set_up_path(os.path.join(self.base_path, 'art/poster/'))
        self.fanart_cache = self._set_up_path(os.path.join(self.base_path, 'art/fanart/'))
        self.api_cache = os.path.join(self.base_path, 'api_cache/')

    def get_game_information(self, game_name):
        request_name = game_name.replace(" ", "+").replace(":", "")
        response = self._gather_information(request_name)
        if response is None:
            response = {}
        response['name'] = game_name
        # TODO: This should return an instance of a specific response object
        return response

    def return_paths(self):
        return [self.cover_cache, self.fanart_cache, self.api_cache]

    def _gather_information(self, game):
        game_cover_path = self._set_up_path(os.path.join(self.cover_cache, game))
        game_fanart_path = self._set_up_path(os.path.join(self.fanart_cache, game))

        xml_response_file = self._get_xml_data(game)
        xml_root = ElementTree(file=xml_response_file).getroot()

        dict_response = self._parse_xml_to_dict(xml_root)

        if dict_response:
            dict_response['poster'] = self._dump_image(game_cover_path, dict_response.get('poster'))

            local_arts = []
            for art in dict_response.get('fanarts'):
                local_arts.append(self._dump_image(game_fanart_path, art))
            dict_response['fanarts'] = local_arts

            return dict_response

    def _get_xml_data(self, game):
        file_path = os.path.join(self.api_cache, game, game+'.xml')

        if not os.path.isfile(file_path):
            curl = subprocess.Popen(['curl', '-XGET', self.api_url % game], stdout=subprocess.PIPE)
            with open(file_path, 'w') as response_file:
                response_file.write(curl.stdout.read())

        return file_path

    @staticmethod
    def _parse_xml_to_dict(root):
        """

        :rtype: dict
        :type root: Element
        """
        data = {'year': 'N/A', 'plot': 'N/A', 'poster': 'N/A', 'genre': [], 'fanarts': []}
        base_img_url = root.find('baseImgUrl').text
        for game in root.findall('Game'):
            if game.find('Platform').text == 'PC':
                if game.find('ReleaseDate') is not None:
                    data['year'] = os.path.basename(game.find('ReleaseDate').text)
                if game.find('Overview') is not None:
                    data['plot'] = game.find('Overview').text
                for img in game.find('Images'):
                    if img.get('side') == 'front':
                        data['poster'] = os.path.join(base_img_url, img.text)
                    if img.tag == 'fanart':
                        data['fanarts'].append(os.path.join(base_img_url, img.find('original').text))
                if game.find('Genres') is not None:
                    for genre in game.find('Genres'):
                        data['genre'].append(str(genre.text))
                return data

        return None
