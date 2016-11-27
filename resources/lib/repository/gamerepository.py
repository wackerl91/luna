from resources.lib.di.requiredfeature import RequiredFeature


class GameRepository(object):
    # TODO: host aware methods
    def __init__(self, core):
        self.storage = core.get_storage('game_storage')
        self.logger = RequiredFeature('logger').request()

    def get_games(self, host):
        return {key: value for key, value in self.storage.iteritems() if value.host_uuid == host.uuid}

    def add_game(self, host, game, flush=True):
        if game.host_uuid == '' or game.host_uuid is None:
            game.host_uuid = host.uuid
        self.storage[game.id] = game
        if flush:
            self.storage.sync()

    def remove_game(self, host, game, flush=True):
        self.remove_game_by_id(host, game.id, flush)

    def remove_games(self, host, flush=True):
        games = self.get_games(host)
        for id, game in games.iteritems():
            del self.storage[id]
        if flush:
            self.storage.sync()

    def remove_game_by_id(self, host, id, flush=True):
        if id in self.storage.raw_dict():
            if self.storage[id].host_uuid == host.uuid:
                del self.storage[id]
                if flush:
                    self.storage.sync()

    def get_game_by_id(self, host, id):
        self.logger.info('Trying to load game by id ...')
        try:
            game = self.storage[id]
            if game:
                self.logger.info('Found game by id, its host is %s' % game.host_uuid)
            if game.host_uuid == host.uuid:
                self.logger.info('Host UUID matches, returning game')
                return game
        except KeyError:
            self.logger.error('Couldnt find game with ID %s for host %s' % (host.uuid, id))
            return None

    def clear(self):
        self.logger.info('Clearing game_storage')
        self.storage.clear()
        self.storage.sync()
