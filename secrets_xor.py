#
#  XOR'ing two 128-bit fields.
# 
#  Random numbers: 
#      - use the secrets module or os.urandom
#      - DO NOT use the random module.
#      - More info: https://cryptography.io/en/latest/random-numbers/
#
"""This is a toy stub program that demonstrates use of XOR on 128-bit fields."""

import os


key = os.urandom(16)
print()
print("Key: ",len(key),key)


def xor128(a,b: bytes) -> bytes:
    assert len(a) == len(b), "Input of different lengths not permitted."
    assert len(a) == 16, "Input must be 16 (bytes)."
    c = bytearray(16)
    
    for i in range(len(a)):
        c[i] = a[i] ^ b[i]
        
    return(bytes(c))
    

plaintext = b"( Cryptography )"
print("Ptxt:",len(plaintext),plaintext)

ciphertext = xor128(key,plaintext)
print("Ctxt:",len(ciphertext),ciphertext)

print("\nXORing the ciphertext with the key once more.")

decrypted = xor128(key,ciphertext)
print("Data:",len(decrypted),decrypted)

print("\nConverting to an ordinary string.")
text = decrypted.decode("utf-8")
print("Text:",len(text),text)