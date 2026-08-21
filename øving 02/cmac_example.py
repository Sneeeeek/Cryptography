"""
A small CMAC example: handle with care :-)
"""

import secrets
from bitstring import BitArray
from cryptography.hazmat.primitives import cmac
from cryptography.hazmat.primitives.ciphers import algorithms

print("\nCMAC example\n")

key = secrets.token_bytes(16)
mac = cmac.CMAC(algorithms.AES(key))

msg = input("Provide a message: ")
m = bytes(msg,'utf-8')

mac.update(m)
icv = mac.finalize()

print("\nThe key:",BitArray(key).hex)
print("The icv:", BitArray(icv).hex)

