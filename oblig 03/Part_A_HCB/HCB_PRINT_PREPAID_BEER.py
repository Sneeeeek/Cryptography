"""
The Homegrown Crypto Bar.

Print the voucher.

"""
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os


VOUCHER_NAME = "oblig 03/Part_A_HCB/HCB_PREPAID_BEER.BIN"
KEYFILE_NAME = "oblig 03/Part_A_HCB/HCB_PREPAID_BEER.KEY"

# AES block size: 128-bit (16-byte) 


def decrypt(key, iv, ciphertext):
    decryptor = Cipher(algorithms.AES(key), modes.CTR(iv)).decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()


def get_key(fname: str) -> bytes:
    f = open(fname,"rb")
    key = f.read()
    f.close()
    return key


def get_iv_and_ct(fname: str):
    f = open(fname,"rb")
    contents = f.read()
    f.close()
    iv = contents[0:16]
    ciphertext = contents[16:]
    return iv, ciphertext


# xor 128 er kopiert (og modifisert) fra Malleable_OTP.py fra øving 00
def xor128(a,b: bytes) -> bytes:
    c = bytearray(66)    
    for i in range(len(a)): c[i] = a[i] ^ b[i]
    return(bytes(c))

if  __name__ == "__main__":
    key = get_key(KEYFILE_NAME)
    iv, ciphertext = get_iv_and_ct(VOUCHER_NAME)
    plaintext = decrypt(key, iv, ciphertext)
    
    print("\nThe Homegrown Crypto Bar;\n")
    print("  Voucher  :", plaintext)

    # Lag XOR mask av 1 og 2 
    mask1to2 = ord("1") ^ ord("2")
    # Lag blockmask (like lang som meldingen)
    blockmask = bytearray(66)
    # Byte nr 55 er hvor tallet 1 hører til
    blockmask[54] = mask1to2

    # XOR de to, her gjør vi 1 om til 2 
    c2 = xor128(ciphertext,blockmask)

    # Skriver til ny _EDIT fil istedenfor så slipper jeg å fikse orginalfila hele tiden.
    with open("oblig 03/Part_A_HCB/HCB_PREPAID_BEER_EDIT.BIN", "wb") as file:
        file.write(c2)

    # Dekrypter og print for å sjekke om det gikk
    p2 = decrypt(key, iv, c2)
    print("  Voucher  :", p2)

    #   Voucher  : b'*** The Homegrown Crypto Bar --- Beer voucher. Value: 1 beers. ***'
    #   Voucher  : b'*** The Homegrown Crypto Bar --- Beer voucher. Value: 2 beers. ***'