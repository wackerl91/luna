class Fanart:
    def __init__(self, original=None, thumb=None):
        self.original = original
        self.thumb = thumb

    def get_original(self):
        return self.original

    def set_original(self, original):
        self.original = original

    def get_thumb(self):
        return self.thumb

    def set_thumb(self, thumb):
        self.thumb = thumb
