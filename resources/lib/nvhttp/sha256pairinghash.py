import hashlib

from resources.lib.nvhttp.abstractpairinghash import AbstractPairingHash


class Sha256PairingHash(AbstractPairingHash):
    def get_hash_length(self):
        return 32

    def hash_data(self, data):
        m = hashlib.sha256()
        m.update(data)
        return bytearray(m.digest())
