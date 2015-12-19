class Game:
    def __init__(self, name, json):
        self.name = name
        if json is not None:
            self.year = json['Year']
            self.genre = json['Genre']
            self.plot = json['Plot']
            if json['Poster'] != 'N/A':
                self.thumb = json['Poster']
            else:
                self.thumb = ''
        else:
            self.year = ''
            self.genre = ''
            self.plot = ''
            self.thumb = ''
