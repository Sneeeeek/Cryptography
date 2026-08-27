"""
This example uses ChaCha20.

There is no integrity protection included in ChaCha20.
Also: The IV must NEVER by reused with the same key!
"""
import struct, os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

P1 = b"** This is a known plaintext **"
P2 = b"This is NOT a known plaintext!!"

key = os.urandom(32)
nonce = os.urandom(8)
counter = 0
iv= struct.pack("<Q", counter) + nonce

def encrypt(key, iv,plaintext):
    cipher = Cipher(algorithms.ChaCha20(key, iv), mode=None)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return ciphertext

    
def XOR(b1,b2: bytes) -> bytes:
    assert len(b1) == len(b2), "\nXOR requires two bytes structures of same length"
    result = bytearray(len(b1))
    for i in range(len(b1)):
        result[i] = b1[i] ^ b2[i]
    return bytes(result)


def NormalTest():
    ciphertext = encrypt(key, iv, P1)
    twice_encr = encrypt(key, iv, ciphertext)
    plaintext = encrypt(key,iv,ciphertext)

    print("\nChaCha20 test:\n")
    print("  Message   :", len(P1), P1)
    print("  Ciphertext:", len(ciphertext), ciphertext)
    print("  Twice encr:", len(twice_encr), twice_encr)
    print("  Plaintext :", len(plaintext), plaintext)
    

def Same_Key_IV_for_two_messages(msg1,msg2):
    C1 = encrypt(key, iv, msg1)
    C2 = encrypt(key, iv, msg2)

    print("\nChaCha20: Same Key+IV for two messages.\n")
    print("  Message 1   :", len(msg1), msg1)
    print("  Ciphertext 1:", len(C1), C1)
    print("  Message 2   :", len(msg2), msg2)
    print("  Ciphertext 2:", len(C2), C2)   
    
    print("\nIntruder knowledge:\n")
    print("  Message 1   :",msg1)
    print("  Ciphertext 1:",C1)
    print("  Ciphertext 2:",C2)
    
    print("\nNote: The intruder does not know the Key or the IV!\n")
    
    print("\nExtract the keystream w/XOR and decrypt second message:\n")
    KS = XOR(msg1,C1)
    print("  P1 ^ C1     :",KS)
    plaintext2 = XOR(C2,KS)
    print("  Decrypted P2:",plaintext2)
    
 
 
if  __name__ == "__main__":
     #NormalTest()
     Same_Key_IV_for_two_messages(P1,P2)
     