import ConfigParser
import json
import os
import urllib2
import dateutil.parser as date_parser

import xbmcgui
from abcscraper import AbstractScraper
from resources.lib.di.requiredfeature import RequiredFeature
from resources.lib.model.apiresponse import ApiResponse


class IgdbScraper(AbstractScraper):
    def __init__(self):
        AbstractScraper.__init__(self)
        self.plugin = RequiredFeature('plugin').request()
        self.api_url = 'https://www.igdb.com/api/v1/games/%s'
        self.api_img_url = 'https://res.cloudinary.com/igdb/image/upload/t_%s/%s.jpg'
        self.cover_cache = self._set_up_path(os.path.join(self.base_path, 'art/poster/'))
        self.api_cache = self._set_up_path(os.path.join(self.base_path, 'api_cache/'))

    def name(self):
        return 'IGDB'

    def get_game_information(self, game_name):
        if self.plugin.get_setting('api_key_file', str) == "":
            return ApiResponse()

        request_name = game_name.replace(" ", "+").replace(":", "")
        response = self._gather_information(request_name)
        response.name = game_name

        return response

    def return_paths(self):
        return [self.cover_cache, self.api_cache]

    def is_enabled(self):
        return self.plugin.get_setting('enable_igdb', bool)

    def _gather_information(self, game):
        game_cover_path = self._set_up_path(os.path.join(self.cover_cache, game))
        game_cache_path = self._set_up_path(os.path.join(self.api_cache, game))

        file_path = os.path.join(game_cache_path, game+'.json')

        try:
            cp = ConfigParser.ConfigParser()
            cp.read(self.plugin.get_setting('api_key_file', str))
            igdb_api_key = cp.get('API', 'igdb')
        except:
            xbmcgui.Dialog().notification(
                self.core().string('name'),
                self.core().string('scraper_failed') % (game, self.name())
            )
            return ApiResponse()

        url_opener = urllib2.build_opener()
        url_opener.addheaders = [
            ('Accept', 'application/json'),
            ('Authorization', 'Token token=%s' % igdb_api_key)
        ]

        if not os.path.isfile(file_path):
            query_string = 'search?q=%s' % game
            response = url_opener.open(self.api_url % query_string)
            if response.getcode() in [200, 304]:
                search_results = json.load(url_opener.open(self.api_url % query_string))
                print search_results
                if len(search_results) > 0:
                    best_match_id = search_results['games'][0]['id']
                else:
                    return None
            else:
                raise IOError("Server failed with status code %s" % response.getcode())
        else:
            best_match_id = None

        try:
            json_data = json.load(open(self._get_json_data(url_opener, game_cache_path, game, best_match_id)))
        except IOError:
            return None

        json_data = json_data['game']

        api_response = ApiResponse()
        api_response.year = date_parser.parse(json_data['release_date']).year
        api_response.plot = json_data['summary'].encode('utf-8')
        for genre in json_data['genres']:
            api_response.genre.append(genre['name'].encode('utf-8'))

        if json_data['cover'] is not None:
            img_id = json_data['cover']['id']
            cover_path = self._dump_image(game_cover_path, self.api_img_url % ('cover_big', img_id))
            if cover_path is not None:
                api_response.posters.append(cover_path)

        return api_response

    def _get_json_data(self, url_opener, path, game, best_match_id):
        file_path = os.path.join(path, game+'_igdb.json')
        if not os.path.exists(file_path) and best_match_id is not None:
            response = url_opener.open(self.api_url % best_match_id)
            if response.getcode() in [200, 304]:
                json_response = json.load(response)
                with open(file_path, 'w') as response_file:
                    json.dump(json_response, response_file)
            else:
                raise IOError("Server failed with status code %s" % response.get())

        return file_path
