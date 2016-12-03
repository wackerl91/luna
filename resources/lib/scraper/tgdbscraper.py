import os
import subprocess

from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element

try:
    import xbmcgui
except ImportError:
    from xbmcswift2 import xbmcgui

from abcscraper import AbstractScraper
from resources.lib.model.apiresponse import ApiResponse
from resources.lib.model.fanart import Fanart


class TgdbScraper(AbstractScraper):
    def __init__(self, core):
        AbstractScraper.__init__(self, core)
        self.api_url = 'http://thegamesdb.net/api/GetGame.php?name=%s'
        self.cover_cache = self._set_up_path(os.path.join(self.base_path, 'art/poster/'))
        self.fanart_cache = self._set_up_path(os.path.join(self.base_path, 'art/fanart/'))
        self.api_cache = os.path.join(self.base_path, 'api_cache/')

    def name(self):
        return 'TGDB'

    def get_game_information(self, nvapp):
        request_name = nvapp.title.replace(" ", "+").replace(":", "")
        response = self._gather_information(nvapp, request_name)
        response.name = nvapp.title
        return response

    def return_paths(self):
        return [self.cover_cache, self.fanart_cache, self.api_cache]

    def is_enabled(self):
        return self.core.get_setting('enable_tgdb', bool)

    def _gather_information(self, nvapp, game):
        game_cover_path = self._set_up_path(os.path.join(self.cover_cache, nvapp.id))
        game_fanart_path = self._set_up_path(os.path.join(self.fanart_cache, nvapp.id))

        xml_response_file = self._get_xml_data(nvapp.id, game)

        try:
            xml_root = ElementTree(file=xml_response_file).getroot()
        except:
            xbmcgui.Dialog().notification(
                self.core.string('name'),
                self.core.string('scraper_failed') % (game, self.name())
            )

            if xml_response_file is not None and os.path.isfile(xml_response_file):
                os.remove(xml_response_file)

            return ApiResponse()

        dict_response = self._parse_xml_to_dict(xml_root)

        if dict_response:
            posters = dict_response['posters']
            dict_response['posters'] = []
            for poster in posters:
                dict_response['posters'].append(self._dump_image(game_cover_path, poster))

            local_arts = {}
            for art in dict_response.get('fanarts'):
                art.set_thumb(self._dump_image(game_fanart_path, art.get_thumb()))
                local_arts[os.path.basename(art.get_thumb())] = art
            dict_response['fanarts'] = local_arts

            return ApiResponse.from_dict(**dict_response)

    def _get_xml_data(self, id, game):
        file_path = os.path.join(self.api_cache, id, game+'_tgdb.xml')

        if not os.path.isfile(file_path):
            if not os.path.exists(os.path.dirname(file_path)):
                os.makedirs(os.path.dirname(file_path))
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
        data = {'year': 'N/A', 'plot': 'N/A', 'posters': [], 'genre': [], 'fanarts': []}
        similar_id = []
        base_img_url = root.find('baseImgUrl').text

        for game in root.findall('Game'):
            if game.find('Platform').text == 'PC':
                if game.find('ReleaseDate') is not None:
                    data['year'] = os.path.basename(game.find('ReleaseDate').text)
                if game.find('Overview') is not None:
                    data['plot'] = game.find('Overview').text
                for img in game.find('Images'):
                    if img.get('side') == 'front':
                        data['posters'].append(os.path.join(base_img_url, img.text))
                    if img.tag == 'fanart':
                        image = Fanart()
                        image.set_original(os.path.join(base_img_url, img.find('original').text))
                        image.set_thumb(os.path.join(base_img_url, img.find('thumb').text))
                        data['fanarts'].append(image)
                        del image
                if game.find('Genres') is not None:
                    for genre in game.find('Genres'):
                        data['genre'].append(str(genre.text))
                if game.find('Similar') is not None:
                    for similar in game.find('Similar'):
                        if similar.tag == 'Game':
                            similar_id.append(similar.find('id').text)
                break

        for game in root.findall('Game'):
            if game.find('id').text in similar_id:
                for img in game.find('Images'):
                    if img.tag == 'fanart':
                        image = Fanart()
                        image.set_original(os.path.join(base_img_url, img.find('original').text))
                        image.set_thumb(os.path.join(base_img_url, img.find('thumb').text))
                        data['fanarts'].append(image)
                        del image

        return data
