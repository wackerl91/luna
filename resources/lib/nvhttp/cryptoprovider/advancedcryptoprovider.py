import os
import time

from Crypto.Util import asn1
from M2Crypto import RSA as M2RSA
from M2Crypto import X509, EVP, ASN1

from resources.lib.nvhttp.cryptoprovider.abstractcryptoprovider import AbstractCryptoProvider


class AdvancedCryptoProvider(AbstractCryptoProvider):
    def __init__(self, config_helper):
        self.config_helper = config_helper
        self.cert_file = self.get_cert_path()
        self.key_file = self.get_key_path()
        self.cert = None
        self.private_key = None
        self.pem_cert_bytes = None

    def load_file_to_bytes(self, cert_file):
        self.pem_cert_bytes = buffer(open(cert_file).read())
        return self.pem_cert_bytes

    def load_cert_key_pair(self):
        if not os.path.isfile(self.cert_file) or not os.path.isfile(self.key_file):
            return False

        self.cert = X509.load_cert(self.cert_file)
        self.private_key = M2RSA.load_key(self.key_file)
        self.load_file_to_bytes(self.cert_file)

        return True

    def validate_cert(self, cert, days=365):
        t = long(time.time())
        now = ASN1.ASN1_UTCTIME()
        now.set_time(t)
        expire = ASN1.ASN1_UTCTIME()
        expire.set_time(t + days * 24 * 60 * 60)
        cert.set_not_before(now)
        cert.set_not_after(expire)

    def generate_cert_key_pair(self):
        private_key = EVP.PKey()
        rsa = M2RSA.gen_key(2048, 65537, lambda: None)
        private_key.assign_rsa(rsa)

        req = X509.Request()
        req.set_pubkey(private_key)
        name = req.get_subject()
        name.CN = 'NVIDIA GameStream Client'
        req.sign(private_key, 'sha1')

        public_key = req.get_pubkey()
        cert = X509.X509()
        cert.set_serial_number(1)
        cert.set_version(2)
        self.validate_cert(cert)
        cert.set_issuer(name)
        cert.set_subject(cert.get_issuer())
        cert.set_pubkey(public_key)
        cert.add_ext(X509.new_extension('basicConstraints', 'CA:TRUE', 1))
        cert.add_ext(X509.new_extension('keyUsage', 'keyCertSign, cRLSign', 1))
        cert.add_ext(X509.new_extension('subjectKeyIdentifier', cert.get_fingerprint()))
        cert.sign(private_key, 'sha1')

        cert.save(self.cert_file, 1)

        with open(self.key_file, 'wb') as key_file:
            key_file.write(private_key.as_pem(None))
            key_file.close()

        self.load_cert_key_pair()

    def extract_cert_signature(self, cert):
        # TODO: Can this be done from M2Crypto's certificate object?
        der_cert = cert.as_der()
        der = asn1.DerSequence()
        der.decode(der_cert)

        der_sig_raw = der[2]

        der_sig_dec = asn1.DerObject()
        der_sig_dec.decode(der_sig_raw)

        sig0 = der_sig_dec.payload

        sig = sig0[1:]

        return sig

    def extract_cert_signature_as_hex(self, cert):
        return self.extract_cert_signature(cert).encode('hex')

    def get_client_cert(self):
        if not self.cert:
            if not self.load_cert_key_pair():
                self.generate_cert_key_pair()
            else:
                return self.cert
        return self.cert

    def get_client_private_key(self):
        if not self.private_key:
            if not self.load_cert_key_pair():
                self.generate_cert_key_pair()
            else:
                return self.private_key
        return self.private_key

    def get_pem_encoded_client_cert(self):
        if not self.pem_cert_bytes:
            if not self.load_cert_key_pair():
                self.generate_cert_key_pair()
            else:
                return self.pem_cert_bytes
        return self.pem_cert_bytes

    def get_cert_path(self):
        return os.path.join(os.path.expanduser('~'), '.cache/moonlight/client.pem')

    def get_key_path(self):
        return os.path.join(os.path.expanduser('~'), '.cache/moonlight/key.pem')

    def get_key_dir(self):
        return os.path.join(os.path.expanduser('~'), '.cache/moonlight')
