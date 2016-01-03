import os

import subprocess

from resources.lib.model.fanart import Fanart


class Game:
    def __init__(self, name, year=None, genre=None, plot=None, posters=None, fanarts=None):
        self.name = name
        self.year = year
        self.genre = genre
        self.plot = plot
        self.posters = posters
        self.fanarts = fanarts
        self.selected_fanart = self.get_fanart('')
        self.selected_poster = self.get_poster(0, '')

    @classmethod
    def from_dict(cls, name=None, year=None, genre=None, plot=None, posters=None, fanarts=None, **kwargs):
        game = cls(name, year, genre, plot, posters, fanarts)

        return game

    def merge(self, other):
        """
        :type other: Game
        """
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
            self.fanarts = list(set(self.fanarts) | set(other.fanarts))

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
        if not os.path.isfile(art.get_original()):
            art.set_original(self._replace_thumb(art.get_thumb(), art.get_original()))

    def get_genre_as_string(self):
        if self.genre is not None:
            return ', '.join(self.genre)
        else:
            return ''

    def get_poster(self, index, alt):
        if self.posters is None:
            return alt
        else:
            try:
                response = self.posters[0]
            except KeyError:
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
