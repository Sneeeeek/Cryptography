"""
This example uses AES-CTR.

There is no integrity protection included in AES-CTR.
Also: The IV must NEVER by reused with the same key!

cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/#cryptography.hazmat.primitives.ciphers.modes.CTR
"""
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os


def encrypt(key, iv, plaintext):
    encryptor = Cipher(algorithms.AES(key), modes.CTR(iv)).encryptor()
    return encryptor.update(plaintext) + encryptor.finalize()


def decrypt(key, iv, ciphertext):
    decryptor = Cipher(algorithms.AES(key), modes.CTR(iv)).decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()


key = os.urandom(16)
iv = os.urandom(16)
message = b"AES-CTR er en stream-cipher metode. Derfor trenger vi ikke padding."

ciphertext = encrypt(key, iv, message)
plaintext = decrypt(key,iv,ciphertext)

print("\nAES-CTR eksempel:\n")
print("  Message   :", len(message), message)
print("  Ciphertext:", len(ciphertext), ciphertext)
print("  Plaintext :", len(plaintext), plaintext)