"""
Authenticated encryption using Cobblestone
"""
from cryptography.cobblestone import (Cobblestone128Decryptor, Cobblestone128Encryptor)

key = Cobblestone128Encryptor.generate_key()
context = b"BTS4410 Sikkerhet og Anvendt Kryptografi"

message = """
“Anyone who tries to create his or her own cryptographic primitive is either a genius or a fool. 
Givent the genius/fool ratio of our species, the odds aren't very good.” 
― Bruce Schneier, Secrets and Lies: Digital Security in a Networked World"""
message = bytes(message,"utf-8")

encryptor = Cobblestone128Encryptor(key, context)
ciphertext = encryptor.update(message)
ciphertext += encryptor.finalize()

decryptor = Cobblestone128Decryptor(key, context)

message = decryptor.update(ciphertext) + decryptor.finalize()
print(str(message,"utf-8"))