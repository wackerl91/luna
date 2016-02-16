import json
import os
import urllib2

import xbmcgui

from abcscraper import AbstractScraper
from resources.lib.di.requiredfeature import RequiredFeature
from resources.lib.model.apiresponse import ApiResponse


class OmdbScraper(AbstractScraper):
    def __init__(self):
        AbstractScraper.__init__(self)
        self.plugin = RequiredFeature('plugin').request()
        self.api_url = 'http://www.omdbapi.com/?t=%s&plot=short&r=json&type=game'
        self.cover_cache = self._set_up_path(os.path.join(self.base_path, 'art/poster/'))
        self.api_cache = self._set_up_path(os.path.join(self.base_path, 'api_cache/'))

    def name(self):
        return 'OMDB'

    def get_game_information(self, game_name):
        request_name = game_name.replace(" ", "+").replace(":", "")
        response = self._gather_information(request_name)
        response.name = game_name
        return response

    def return_paths(self):
        return [self.cover_cache, self.api_cache]

    def is_enabled(self):
        return self.plugin.get_setting('enable_omdb', bool)

    def _gather_information(self, game):
        game_cover_path = self._set_up_path(os.path.join(self.cover_cache, game))
        game_cache_path = self._set_up_path(os.path.join(self.api_cache, game))

        json_file = self._get_json_data(game_cache_path, game)
        try:
            json_data = json.load(open(json_file))
        except:
            xbmcgui.Dialog().notification(
                self.core().string('name'),
                self.core().string('scraper_failed') % (game, self.name())
            )

            if json_file is not None and os.path.isfile(json_file):
                os.remove(json_file)

            return ApiResponse()

        if json_data['Response'] != 'False':
            json_data['posters'] = []
            cover_path = self._dump_image(game_cover_path, json_data['Poster'])
            if cover_path is not None:
                json_data['posters'].append(cover_path)
            del json_data['Poster']
            response = dict((k.lower(), v) for k, v in json_data.iteritems())
            if 'genre' in response:
                response['genre'] = response.get('genre').split(',')
                response['genre'] = [str(v).strip() for v in response.get('genre')]

            return ApiResponse.from_dict(**response)
        else:

            return ApiResponse()

    def _get_json_data(self, path, game):
        file_path = os.path.join(path, game+'_omdb.json')
        if not os.path.exists(file_path):
            json_response = json.load(urllib2.urlopen(self.api_url % game))
            with open(file_path, 'w') as response_file:
                json.dump(json_response, response_file)

        return file_path
