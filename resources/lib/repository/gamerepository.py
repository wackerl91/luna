class GameRepository(object):
    def __init__(self, core, logger):
        self.storage = core.get_storage('game_storage')
        self.logger = logger

    def get_games(self, host):
        if host.uuid in self.storage.keys():
            return self.storage[host.uuid]
        else:
            # Host isn't present yet, possibly new one
            return {}

    def add_game(self, host, game, flush=True):
        if game.host_uuid == '' or game.host_uuid is None:
            game.host_uuid = host.uuid

        if host.uuid not in self.storage.keys():
            self.storage[host.uuid] = {}

        self.storage[host.uuid][game.id] = game

        if flush:
            self.storage.sync()

    def remove_game(self, host, game, flush=True):
        self.remove_game_by_id(host, game.id, flush)

    def remove_games(self, host, flush=True):
        if host.uuid in self.storage.keys():
            del self.storage[host.uuid]

        if flush:
            self.storage.sync()

    def remove_game_by_id(self, host, id, flush=True):
        if host.uuid in self.storage.keys():
            if id in self.storage[host.uuid].keys():
                del self.storage[host.uuid][id]
                if flush:
                    self.storage.sync()

    def get_game_by_id(self, host, id):
        self.logger.info('Trying to load game by id ...')

        if host.uuid in self.storage.keys():
            if id in self.storage[host.uuid].keys():
                self.logger.info('Found game by Host / ID combination: %s -> %s' % (host.uuid, id))
                return self.storage[host.uuid][id]
            else:
                self.logger.info('Game ID is not known for host: %s -> %s' % (id, host.uuid))
        else:
            self.logger.info('Host ID is not known: %s' % host.uuid)

        return None

    def clear(self):
        self.logger.info('Clearing game_storage')
        self.storage.clear()
        self.storage.sync()
