class Game:
    def __init__(self, name, year=None, genre=None, plot=None, poster=None, fanart=None):
        self.name = name
        self.year = year
        self.genre = genre
        self.plot = plot
        self.poster = poster
        self.fanart = fanart

    @classmethod
    def from_dict(cls, name=None, year=None, genre=None, plot=None, poster=None, fanart=None, **kwargs):
        game = cls(name, year, genre, plot, poster, fanart)

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

        if self.fanart is None:
            self.fanart = other.fanart
        elif other.fanart is not None:
            self.fanart = list(set(self.fanart) | set(other.fanart))
