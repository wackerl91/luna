class ApiResponse:
    def __init__(self, name=None, year=None, genre=None, plot=None, posters=None, fanarts=None):
        if genre is None:
            genre = []
        if posters is None:
            posters = []
        if fanarts is None:
            fanarts = {}

        self.name = name
        self.year = year
        self.genre = genre
        self.plot = plot
        self.posters = posters
        self.fanarts = fanarts

    @classmethod
    def from_dict(cls, name=None, year=None, genre=None, plot=None, posters=None, fanarts=None, **kwargs):
        return cls(name, year, genre, plot, posters, fanarts)
