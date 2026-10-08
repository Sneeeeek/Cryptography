"""
Authenticated encryption using Cobblestone - with password

In this take, we include having a password as an input to generate the secret key.
"""
from cryptography.cobblestone import (Cobblestone128Decryptor, Cobblestone128Encryptor)
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


MIN_PW_LENGTH = 10


def pw2key(pw: bytes) -> bytes:
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=16, salt=salt, iterations=1_200_000,)
    return kdf.derive(pw)

    
if __name__ == "__main__":
    context = b"BTS4410: Password-based Cobblestone encryption"

    message = """
    “Anyone who tries to create his or her own cryptographic primitive is either a genius or a fool. 
    Givent the genius/fool ratio of our species, the odds aren't very good.” 
    ― Bruce Schneier, Secrets and Lies: Digital Security in a Networked World"""
    message = bytes(message,"utf-8")


    pw = ""
    print("\nThe password must have a minimum lenghth of",MIN_PW_LENGTH,"\n")
    while len(pw) < MIN_PW_LENGTH: pw = bytes(input("Password:"),"utf-8")
    key = pw2key(pw)
    
    print("\nThe key:",key)

    # There can be many "update" calls. 
    # Typically, one process one block at at time.
    # Only the current message/ciphertext need be in memory.
    # This allows for file- or stream encryption of really big amounts of data.
    # See https://cryptography.io/en/latest/cobblestone/ for more.
    encryptor = Cobblestone128Encryptor(key, context)
    ciphertext = encryptor.update(message)
    ciphertext += encryptor.finalize()
    
    print("The ciphertext:\n",ciphertext)

    decryptor = Cobblestone128Decryptor(key, context)
    message = decryptor.update(ciphertext) + decryptor.finalize()
    print("\nThe decrypted text:\n",str(message,"utf-8"),"\n")