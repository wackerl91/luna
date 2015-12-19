class Game:
    def __init__(self, name, json):
        self.name = name
        if json is not None:
            self.year = json['Year']
            self.genre = json['Genre']
            self.plot = json['Plot']
            self.thumb = json['Poster']
        else:
            self.year = ''
            self.genre = ''
            self.plot = ''
            self.thumb = 'N/A'
