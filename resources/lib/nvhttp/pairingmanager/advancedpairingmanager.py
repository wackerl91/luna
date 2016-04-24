import binascii
import hashlib
import random

from Crypto.Cipher import AES
from Crypto.Util import asn1
from M2Crypto import X509

from resources.lib.nvhttp.pairingmanager.abstractpairingmanager import AbstractPairingManager
from resources.lib.nvhttp.sha1pairinghash import Sha1PairingHash
from resources.lib.nvhttp.sha256pairinghash import Sha256PairingHash


class AdvancedPairingManager(AbstractPairingManager):
    def __init__(self, crypto_provider):
        self.crypto_provider = crypto_provider
        self.cert = crypto_provider.get_client_cert()
        self.private_key = crypto_provider.get_client_private_key()
        self.pem_cert_bytes = crypto_provider.get_pem_encoded_client_cert()

    @staticmethod
    def _extract_plain_cert(nvhttp, text):
        cert_text = nvhttp.get_xml_string(text, "plaincert")

        cert = X509.load_cert_string(cert_text.decode('hex'))

        der_cert = cert.as_der()
        der = asn1.DerSequence()
        der.decode(der_cert)

        # der_cert = der[0]
        # der_algo = der[1]
        der_sig_raw = der[2]

        der_sig_dec = asn1.DerObject()
        der_sig_dec.decode(der_sig_raw)

        sig0 = der_sig_dec.payload

        sig = sig0[1:]

        return cert, sig.encode('hex')

    @staticmethod
    def _get_random_bytes(count):
        return bytearray(random.getrandbits(8) for i in range(count))

    @staticmethod
    def _salt_pin(salt, pin):
        pin_to_byte = bytearray(pin)
        salted_pin = bytearray()
        salted_pin[:] = salt
        salted_pin[len(salt):len(salt) + len(pin_to_byte)] = pin_to_byte

        return salted_pin

    @staticmethod
    def _generate_aes_key(hash_algo, data):
        return hash_algo.hash_data(data)[:16]

    @staticmethod
    def bytes_to_hex(byte_array):
        return binascii.hexlify(byte_array).upper()

    @staticmethod
    def _hex_to_bytes(hex_string):
        return bytearray(hex_string.decode('hex'))

    @staticmethod
    def _pad(data):
        return data + ((((len(data) + 15) / 16) * 16) - len(data)) * chr(0)

    @staticmethod
    def _encrypt_aes(data, key):
        data = AdvancedPairingManager._pad(data)
        cipher = AES.new(buffer(key))
        return cipher.encrypt(buffer(data))

    @staticmethod
    def _decrypt_aes(data, key):
        data = AdvancedPairingManager._pad(data)
        cipher = AES.new(buffer(key))
        return cipher.decrypt(buffer(data))

    @staticmethod
    def _concat_bytes(a, b):
        c = bytearray(len(a) + len(b))
        c[:] = a
        c[len(a):len(a) + len(b)] = b
        return c

    @staticmethod
    def _verify_signature(data, signature, cert):
        """
        rsakey = RSA.importKey(cert.get_pubkey())
        signer = PKCS1_v1_5.new(rsakey)
        digest = SHA256.new()
        digest.update(data)
        return signer.verify(digest, signature)
        """
        # rawsig = signature.decode('base64')
        pubkey = cert.get_pubkey()
        pubkey.reset_context(md='sha256')
        pubkey.verify_init()
        pubkey.verify_update(data)
        return pubkey.verify_final(signature)

    @staticmethod
    def _sign_data(data, key):
        """
        rsakey = RSA.importKey(key)
        signer = PKCS1_v1_5.new(rsakey)
        digest = SHA256.new()
        digest.update(data)
        return signer.sign(digest)
        """
        return key.sign(hashlib.sha256(data).digest(), 'sha256')

    def pair(self, nvhttp, server_info, pin):
        server_major_version = nvhttp.get_server_major_version(server_info)

        if int(server_major_version) >= 7:
            hash_algo = Sha256PairingHash()
        else:
            hash_algo = Sha1PairingHash()

        salt = self._get_random_bytes(16)
        salt_and_pin = self._salt_pin(salt, pin)

        aes_key = self._generate_aes_key(hash_algo, salt_and_pin)

        print 'Sending get_cert request'
        get_cert = nvhttp.open_http_connection(
            nvhttp.base_url_http + '/pair?' + nvhttp.build_uid_uuid_string() +
            '&devicename=roth&updateState=1&phrase=getservercert&salt=' +
            self.bytes_to_hex(salt) + '&clientcert=' + self.bytes_to_hex(self.pem_cert_bytes),
            False
        )
        if int(nvhttp.get_xml_string(get_cert, 'paired')) != 1:
            nvhttp.open_http_connection(
                nvhttp.base_url_http + '/unpair?' + nvhttp.build_uid_uuid_string(),
                True
            )
            return self.STATE_FAILED

        server_cert, server_sig = self._extract_plain_cert(nvhttp, get_cert)

        rnd_challenge = self._get_random_bytes(16)
        encrypted_challenge = self._encrypt_aes(rnd_challenge, aes_key)

        print 'Sending challenge request'
        challenge_response = nvhttp.open_http_connection(
            nvhttp.base_url_http + '/pair?' + nvhttp.build_uid_uuid_string() +
            '&devicename=roth&updateState=1&clientchallenge=' + self.bytes_to_hex(encrypted_challenge),
            True
        )
        if int(nvhttp.get_xml_string(challenge_response, 'paired')) != 1:
            nvhttp.open_http_connection(
                nvhttp.base_url_http + '/unpair?' + nvhttp.build_uid_uuid_string(),
                True
            )
            return self.STATE_FAILED

        enc_srv_challenge_response = self._hex_to_bytes(nvhttp.get_xml_string(challenge_response, 'challengeresponse'))
        dec_srv_challenge_response = self._decrypt_aes(enc_srv_challenge_response, aes_key)

        srv_response = dec_srv_challenge_response[:hash_algo.get_hash_length()]
        srv_challenge = dec_srv_challenge_response[hash_algo.get_hash_length():hash_algo.get_hash_length() + 16]

        client_secret = self._get_random_bytes(16)
        challenge_response_hash = hash_algo.hash_data(
            self._concat_bytes(
                self._concat_bytes(srv_challenge, self.crypto_provider.extract_cert_signature(self.cert)),
                client_secret
            )
        )
        enc_challenge_response = self._encrypt_aes(challenge_response_hash, aes_key)

        print 'Sending secret request'
        secret_response = nvhttp.open_http_connection(
            nvhttp.base_url_http + '/pair?' + nvhttp.build_uid_uuid_string() +
            '&devicename=roth&updateState=1&serverchallengeresp=' + self.bytes_to_hex(enc_challenge_response),
            True
        )
        if int(nvhttp.get_xml_string(secret_response, 'paired')) != 1:
            nvhttp.open_http_connection(
                nvhttp.base_url_http + '/unpair?' + nvhttp.build_uid_uuid_string(),
                True
            )
            return self.STATE_FAILED

        srv_secret_response = self._hex_to_bytes(nvhttp.get_xml_string(secret_response, 'pairingsecret'))
        srv_secret = srv_secret_response[:16]
        srv_signature = srv_secret_response[16:272]

        if not self._verify_signature(srv_secret, srv_signature, server_cert):
            nvhttp.open_http_connection(
                nvhttp.base_url_http + '/unpair?' + nvhttp.build_uid_uuid_string(),
                True
            )
            return self.STATE_FAILED

        srv_challenge_response_hash = hash_algo.hash_data(
            self._concat_bytes(
                self._concat_bytes(rnd_challenge, self._hex_to_bytes(server_sig)),
                srv_secret
            )
        )
        if not srv_challenge_response_hash == srv_response:
            nvhttp.open_http_connection(
                nvhttp.base_url_http + '/unpair?' + nvhttp.build_uid_uuid_string(),
                True
            )
            return self.STATE_PIN_WRONG

        client_pairing_secret = self._concat_bytes(client_secret, self._sign_data(client_secret, self.private_key))
        print 'Sending client secret request'
        client_secret_response = nvhttp.open_http_connection(
            nvhttp.base_url_http + '/pair?' + nvhttp.build_uid_uuid_string() +
            '&devicename=roth&updateState=1&clientpairingsecret=' + self.bytes_to_hex(client_pairing_secret),
            True
        )
        if int(nvhttp.get_xml_string(client_secret_response, 'paired')) != 1:
            nvhttp.open_http_connection(
                nvhttp.base_url_http + '/unpair?' + nvhttp.build_uid_uuid_string(),
                True
            )
            return self.STATE_FAILED

        pair_challenge = nvhttp.open_http_connection(
            nvhttp.base_url_https + '/pair?' + nvhttp.build_uid_uuid_string() +
            '&devicename=roth&updateState=1&phrase=pairchallenge',
            True
        )
        if int(nvhttp.get_xml_string(pair_challenge, 'paired')) != 1:
            nvhttp.open_http_connection(
                nvhttp.base_url_http + '/unpair?' + nvhttp.build_uid_uuid_string(),
                True
            )
            return self.STATE_FAILED

        return self.STATE_PAIRED
