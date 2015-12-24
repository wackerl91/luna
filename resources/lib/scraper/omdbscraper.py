import json
import os
import urllib2

from abcscraper import AbstractScraper


class OmdbScraper(AbstractScraper):
    def __init__(self, addon_path):
        AbstractScraper.__init__(self, addon_path)

        self.api_url = 'http://www.omdbapi.com/?t=%s&plot=short&r=json&type=game'
        self.cover_cache = self._set_up_path(os.path.join(self.base_path, 'art/poster/'))
        self.api_cache = self._set_up_path(os.path.join(self.base_path, 'api_cache/'))

    def get_game_information(self, game_name):
        request_name = game_name.replace(" ", "+").replace(":", "")
        response = self._gather_information(request_name)
        response['name'] = game_name
        # TODO: This should return an instance of a specific response object
        return response

    def _gather_information(self, game):
        game_cover_path = self._set_up_path(os.path.join(self.cover_cache, game))
        game_cache_path = self._set_up_path(os.path.join(self.api_cache, game))

        raw_json = open(self._get_json_data(game_cache_path, game))
        json_data = json.load(raw_json)
        if json_data['Response'] != 'False':
            cover_path = self._dump_image(game_cover_path, json_data['Poster'])
            json_data['Poster'] = cover_path
            response = dict((k.lower(), v) for k, v in json_data.iteritems())
            if 'genre' in response:
                response['genre'] = response.get('genre').split(',')
                response['genre'] = [str(v).strip() for v in response.get('genre')]

            return response
        else:

            return None

    def _get_json_data(self, path, game):
        file_path = os.path.join(path, game+'.json')
        if not os.path.exists(file_path):
            json_response = json.load(urllib2.urlopen(self.api_url % game))
            with open(file_path, 'w') as response_file:
                json.dump(json_response, response_file)

        return file_path
