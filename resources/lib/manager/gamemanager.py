class GameManager(object):
    # TODO: host aware methods
    def __init__(self, repository):
        self.repository = repository

    def get_games(self, host):
        return self.repository.get_games(host)

    def add_game(self, host, game, flush=True):
        self.repository.add_game(host, game, flush)

    def remove_game(self, host, game, flush=True):
        self.repository.remove_game(host, game, flush)

    def remove_games(self, host, flush=True):
        self.repository.remove_games(host, flush)

    def remove_game_by_id(self, host, id, flush=True):
        self.repository.remove_game_by_id(host, id, flush)

    def get_game_by_id(self, host, id):
        self.repository.get_game_by_id(host, id)

    def add_games(self, host, games):
        # TODO!!!!
        pass
