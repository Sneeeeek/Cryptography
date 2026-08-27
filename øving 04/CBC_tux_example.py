"""
The CBC Tux demonstration.
See also:
- https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation

This example serves to illustrate that CBC is much better than ECB :-)

"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

import secrets
import hashlib # hashlib includes the hash functions (they are also in the cryptography module)

key = secrets.token_bytes(16)
IV  = hashlib.sha256(b"Nobody inspects the spammish repetition").digest()[16:]

class EncryptionManager:
    def __init__(self, key, iv):
        
        aesContext = Cipher(algorithms.AES(key),
                            modes.CBC(iv),
                            backend=default_backend())
        self.encryptor = aesContext.encryptor()
        self.decryptor = aesContext.decryptor()
        self.padder = padding.PKCS7(128).padder()
        self.unpadder = padding.PKCS7(128).unpadder()

    def update_encryptor(self, plaintext):
        return self.encryptor.update(self.padder.update(plaintext))

    def finalize_encryptor(self):
        return self.encryptor.update(self.padder.finalize()) + self.encryptor.finalize()

    def update_decryptor(self, ciphertext):
        return self.unpadder.update(self.decryptor.update(ciphertext))

    def finalize_decryptor(self):
        return self.unpadder.update(self.decryptor.finalize()) + self.unpadder.finalize()

manager = EncryptionManager(key,IV)

plaintext = bytearray()
ciphertext = bytearray()

fcnt = 0
finame = "Tux.ppm.body" 
foname = "Tux_body.cbc"
target = open(foname, 'wb')



with open(finame, 'rb') as source:
    while True:
        buffer = source.read(1024)
        fcnt = fcnt + len(buffer)
        ciphertext += manager.update_encryptor(buffer)       
        
        if len(buffer) == 0: break

ciphertext += manager.finalize_encryptor()
target.write(ciphertext)            
target.close()
print(fcnt)
