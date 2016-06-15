import os

import subprocess

from resources.lib.model.fanart import Fanart


class Game:
    version = 20160424

    def __init__(self, name, host_uuid, id=None, year=None, genre=None, plot=None, posters=None, fanarts=None):
        if genre is None:
            genre = []
        if posters is None:
            posters = []
        if fanarts is None:
            fanarts = {}

        self.name = name
        self.host_uuid = host_uuid
        self.id = id
        self.year = year
        self.genre = genre
        self.plot = plot
        self.posters = posters
        self.fanarts = fanarts
        self.selected_fanart = self.get_fanart('')
        self.selected_poster = self.get_poster(0, '')

    @classmethod
    def from_api_response(cls, api_response):
        """
        :param ApiResponse api_response:
        :rtype: Game
        """
        game = cls(
            api_response.name,
            api_response.year,
            api_response.genre,
            api_response.plot,
            api_response.posters,
            api_response.fanarts
        )

        return game

    def merge(self, other):
        """
        :type other: Game
        """
        if self.host_uuid is None:
            self.host_uuid = other.host_uuid

        if self.id is None:
            self.id = other.id

        if self.year is None:
            self.year = other.year

        if self.genre is None:
            self.genre = sorted(other.genre, key=str.lower)
        elif other.genre is not None:
            self.genre = sorted(list(set(self.genre) | set(other.genre)), key=str.lower)

        if self.plot is None:
            self.plot = other.plot
        elif other.plot is not None and len(other.plot) > len(self.plot):
            self.plot = other.plot

        if self.posters is None:
            self.posters = other.posters
        elif other.posters is not None:
            self.posters = list(set(self.posters) | set(other.posters))

        if self.fanarts is None:
            self.fanarts = other.fanarts
        elif other.fanarts is not None:
            new_dict = self.fanarts.copy()
            new_dict.update(other.fanarts)
            self.fanarts = new_dict

        if self.selected_fanart is None or self.selected_fanart == '':
            self.selected_fanart = other.selected_fanart

    def get_fanart(self, alt):
        if self.fanarts is None:
            return Fanart(alt, alt)
        else:
            try:
                response = self.fanarts.itervalues().next()
                if not os.path.isfile(response.get_original()):
                    response.set_original(self._replace_thumb(response.get_thumb(), response.get_original()))
            except:
                response = Fanart(alt, alt)

            return response

    def get_selected_fanart(self):
        if hasattr(self, 'selected_fanart'):
            if self.selected_fanart.get_thumb() == '':
                self.selected_fanart = self.get_fanart('')

            return self.selected_fanart
        else:
            self.selected_fanart = self.get_fanart('')
            return self.selected_fanart

    def set_selected_fanart(self, uri):
        art = self.fanarts.get(os.path.basename(uri))
        if isinstance(art, Fanart):
            if not os.path.isfile(art.get_original()):
                art.set_original(self._replace_thumb(art.get_thumb(), art.get_original()))
            self.selected_fanart = art
        else:
            if os.path.isfile(uri):
                self.selected_fanart = Fanart(uri, uri)

    def get_genre_as_string(self):
        if self.genre is not None:
            return ', '.join(self.genre)
        else:
            return ''

    # TODO: Index param is not used anywhere
    def get_poster(self, index, alt):
        if self.posters is None:
            return alt
        else:
            try:
                response = self.posters[0]
            except IndexError:
                response = alt

            return response

    def get_selected_poster(self):
        if hasattr(self, 'selected_poster'):
            if self.selected_poster == '':
                self.selected_poster = self.get_poster(0, '')

            return self.selected_poster
        else:
            self.selected_poster = self.get_poster(0, '')
            return self.selected_poster

    def _replace_thumb(self, thumbfile, original):
        file_path = thumbfile
        with open(file_path, 'wb') as img:
            curl = subprocess.Popen(['curl', '-XGET', original], stdout=subprocess.PIPE)
            img.write(curl.stdout.read())
            img.close()

        return file_path
