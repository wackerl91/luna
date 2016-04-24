import hashlib

from resources.lib.nvhttp.abstractpairinghash import AbstractPairingHash


class Sha1PairingHash(AbstractPairingHash):
    def get_hash_length(self):
        return 20

    def hash_data(self, data):
        m = hashlib.sha1()
        m.update(data)
        return bytearray(m.digest())
