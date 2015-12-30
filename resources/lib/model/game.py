class Game:
    def __init__(self, name, year=None, genre=None, plot=None, poster=None, fanarts=None):
        self.name = name
        self.year = year
        self.genre = genre
        self.plot = plot
        self.poster = poster
        self.fanarts = fanarts
        self.selected_fanart = self.get_fanart(0, '')

    @classmethod
    def from_dict(cls, name=None, year=None, genre=None, plot=None, poster=None, fanarts=None, **kwargs):
        game = cls(name, year, genre, plot, poster, fanarts)

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
        elif len(other.plot) > len(self.plot):
            self.plot = other.plot

        if self.poster is None:
            self.poster = other.poster

        if self.fanarts is None:
            self.fanarts = other.fanarts
        elif other.fanarts is not None:
            self.fanarts = list(set(self.fanarts) | set(other.fanarts))

        if self.selected_fanart is None or self.selected_fanart == '':
            self.selected_fanart = other.selected_fanart

    def get_fanart(self, index, alt):
        if self.fanarts is None:
            return alt
        else:
            try:
                response = self.fanarts[index]
            except:
                response = alt

            return response

    def get_selected_fanart(self):
        if hasattr(self, 'selected_fanart'):
            if self.selected_fanart == '':
                self.selected_fanart = self.get_fanart(0, '')

            return self.selected_fanart
        else:
            self.selected_fanart = self.get_fanart(0, '')
            return self.selected_fanart

    def get_genre_as_string(self):
        if self.genre is not None:
            return ', '.join(self.genre)
        else:
            return ''
