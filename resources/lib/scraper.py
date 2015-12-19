import json
import os
import subprocess
import urllib2
import xml.etree.ElementTree as ET

from game import Game


class ScraperCollection:
    def __init__(self, addon_path):
        _configure(addon_path)
        self.omdb = OmdbScraper()
        self.tgdb = TgdbScraper(addon_path)
        self.img_path = addon_path + '/boxarts/'

    def query_game_information(self, game_name):
        request_name = game_name.replace(" ", "+").replace(":", "")
        game = _get_information(self, request_name)
        game.name = game_name
        return game


class OmdbScraper:
    def __init__(self):
        self.api_url = 'http://www.omdbapi.com/?t=%s&plot=short&r=json&type=game'


class TgdbScraper:
    def __init__(self, addon_path):
        self.api_url = 'http://thegamesdb.net/api/GetGame.php?name=%s'
        self.api_cache = addon_path + '/api_cache/'


def _configure(addon_path):
    if not os.path.exists(addon_path + '/boxarts'):
        os.makedirs(addon_path + '/boxarts')
    if not os.path.exists(addon_path + '/api_cache'):
        os.makedirs(addon_path + '/api_cache')


def _get_information(self, game_name):
    """

    :type self: ScraperCollection
    :rtype Game
    """
    if game_name == 'Steam':
        return Game(game_name, None)

    omdb_response = json.load(urllib2.urlopen(self.omdb.api_url % game_name))

    if omdb_response['Response'] == 'False':
        file_path = self.tgdb.api_cache + game_name + '.xml'
        _cache_tgdb_response_data(self, file_path, game_name)

        root = ET.ElementTree(file=file_path).getroot()

        omdb_response = _parse_xml(root)

        full_img_url = omdb_response['Poster']
        full_img_path = self.img_path + os.path.basename(full_img_url)

    else:
        if omdb_response['Poster'] == 'N/A':
            file_path = self.tgdb.api_cache + game_name + '.xml'
            _cache_tgdb_response_data(self, file_path, game_name)

            root = ET.ElementTree(file=file_path).getroot()

            full_img_url = _build_image_path(_get_img_base_url(root), _get_image(root))
            full_img_path = self.img_path + os.path.basename(full_img_url)
        else:
            full_img_url = omdb_response['Poster']
            full_img_path = self.img_path + os.path.basename(full_img_url)

    _dump_image(full_img_path, full_img_url)
    omdb_response['Poster'] = full_img_path

    return Game(game_name, omdb_response)


def _cache_tgdb_response_data(self, file_path, name):
    """

    :type self: ScraperCollection
    """
    if not os.path.isfile(file_path):
        curl = subprocess.Popen(['curl', '-XGET', self.tgdb.api_url % name], stdout=subprocess.PIPE)
        with open(file_path, 'w') as response_file:
            response_file.write(curl.stdout.read())


def _get_img_base_url(r):
    return r.find('baseImgUrl').text


def _get_image(r):
    for i in r.findall('Game'):
        if i.find('Platform').text == 'PC':
            for b in i.find('Images'):
                if b.get('side') == 'front':
                    return b.text
    return None


def _parse_xml(r):
    data = {}
    img_base_url = _get_img_base_url(r)
    for i in r.findall('Game'):
        if i.find('Platform').text == 'PC':
            if i.find('ReleaseDate'):
                data['Year'] = os.path.basename(i.find('ReleaseDate').text)
            else:
                data['Year'] = 'N/A'
            if i.find('Overview'):
                data['Plot'] = i.find('Overview').text
            else:
                data['Plot'] = 'N/A'
            data['Poster'] = 'N/A'
            for b in i.find('Images'):
                if b.get('side') == 'front':
                    data['Poster'] = img_base_url + b.text
            if not i.find('Genres'):
                data['Genre'] = 'N/A'
            else:
                for g in i.find('Genres'):
                    data['Genre'] = ', '.join([data['Genre'], g.text])
            break
    return data


def _build_image_path(base_url, img_url=None):
    if base_url is not None and img_url is not None:
        return base_url + img_url
    if base_url is not None:
        return base_url
    else:
        return None


def _dump_image(path, url):
    if not os.path.exists(path):
        with open(path, 'wb') as img:
            img_curl = subprocess.Popen(['curl', '-XGET', url], stdout=subprocess.PIPE)
            img.write(img_curl.stdout.read())
            img.close()
