class Game:
    def __init__(self, name, year=None, genre=None, plot=None, cover=None, fanarts=None):
        self.name = name
        if year is not None:
            self.year = year
        if genre is not None:
            self.genre = genre
        if plot is not None:
            self.plot = plot
        if cover is not None:
            self.cover = cover
        if fanarts is not None:
            self.fanarts = fanarts

    @classmethod
    def from_dict(cls, name=None, year=None, genre=None, plot=None, cover=None, fanarts=None):
        game = cls(name, year, genre, plot, cover, fanarts)

        return game

    def merge(self, other):
        """
        :type other: Game
        """
        if self.year is None:
            self.year = other.year

        if self.genre is None:
            self.genre = other.genre
        elif other.genre is not None:
            self.genre = list(set(self.genre) | set(other.genre))

        if self.plot is None:
            self.plot = other.plot
        if len(other.plot) > len(self.plot):
            self.plot = other.plot

        if self.cover is None:
            self.cover = other.cover

        if self.fanarts is None:
            self.fanarts = other.fanarts
        elif other.fanarts is not None:
            self.fanarts = list(set(self.fanarts) | set(other.fanarts))
