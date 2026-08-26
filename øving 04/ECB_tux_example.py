"""
The ECB Tux demonstration.
See also:
- https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation
- https://words.filippo.io/the-ecb-penguin/
- https://commons.wikimedia.org/wiki/File:Linux_mascot_tux.png  (the Tux we use)

Procedure:

1. We start with Tux.png
2. Tux.png is converted to Tux_result.ppm  (default naming by the XnConvert tool.)
3. $head -n 3 Tux_result.ppm Tux.ppm.header
4. $tail -n +4 Tux_result.ppm Tux.ppm.body
5. The body file contains the data that we encrypt with this tool.
6. $cat Tux.ppm.header Tux_body.ecb > Tux_ecb.ppm
7. Tux_ECB.ppm is converted back to png
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

import secrets

key = secrets.token_bytes(16)

#
# This is ECB mode using AES.
# AES is a solid cipher, but ECB is an unsafe mode.
#
def E(k,m: bytes) -> bytes:
    """AES-128 in ECB mode"""
    assert len(m) == 16, "E(k,m): Input block m must be 16 bytes long (was {:d}).".format(len(m))
    assert len(k) == 16, "E(k,m): key must be 16 bytes long."
    
    encryptor = Cipher(algorithms.AES128(k),modes.ECB()).encryptor()
    return(encryptor.update(m) + encryptor.finalize())


#
# The padding is to ensure that we have a full block.
# btw: this is not a recommended padding function, but it gets the job done (here).
#
def pad(b: bytes) -> bytes:
    while len(b)<16: b = b + bytes([0xff])
    return b
                                   
fcnt = 0
finame = "Tux.ppm.body" 
foname = "Tux_body.ecb"
target = open(foname, 'wb')
with open(finame, 'rb') as source:
    while True:
        buffer = source.read(16)
        fcnt = fcnt + len(buffer)
        if len(buffer)<16:
            buffer = pad(buffer)
            ctxt = E(key,buffer)    
            target.write(ctxt)
            break
        else:
            ctxt = E(key,buffer)
            target.write(ctxt)            
target.close()
print(fcnt)
