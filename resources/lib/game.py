class Game:
    def __init__(self, name, json):
        self.name = name
        self.year = json['Year']
        self.genre = json['Genre']
        self.plot = json['Plot']
        self.thumb = json['Poster']
