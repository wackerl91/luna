class Game:
    def __init__(self, name, json):
        self.name = name
        if json is not None:
            self.year = json['Year']
            self.genre = json['Genre']
            self.plot = json['Plot']
            self.thumb = json['Poster']
            if len(json['Fanarts']) > 0:
                self.fanarts = json['Fanarts']
            else:
                self.fanarts = ['N/A']
        else:
            self.year = ''
            self.genre = ''
            self.plot = ''
            self.thumb = 'N/A'
            self.fanarts = ['N/A']
