"""
The SuperEncrypt program -- the ultimate extra-super-duper ultra-secret program!!!!
"""

import hashlib
from blake3 import blake3
import hmac
from datetime import datetime

#
# We made this ourselves -- uses Sha3, md5 and Blake3 in a very clever way
# Roll Your Own is ALWAYS BEST
# 
# We don't need a 'normal' cipher -- we make it ourselves from hashes and MACs
# We also use a secret sauce to avoid this mess with keys.
# And, we use a super-clever counter to bind the sequence together.
# It wasn't even hard!
#
counter = 42    # Where to start? The ANSWER is 42.


def EK(m: bytes) -> bytes:
    global counter
    key_stream = hmac.new(hashlib.sha3_256(secret_sauce2).digest()[0:16], bytes(str(counter),"utf-8"),"md5").digest()
    counter += 1
    ciphertext = bytearray(16)
    for i in range(len(m)):
        ciphertext[i] = m[i] ^ key_stream[i]
    return ciphertext
        
#
# The padding is to ensure that we have a full block.
# btw: this is not a recommended padding function, but it gets the job done (here).
#
def pad(b: bytes) -> bytes:
    while len(b)<16: b = b + b" "
    return b

#
# Taking a byte-like block (16 bytes) and make a hex string
# We intentionally include a "\n" to make the output line-oriented
#
def hexstr(c: bytes) -> str:
    assert len(c) == 16, "hexstr: Input block m must be 16 bytes long (was {:d}).".format(len(c))
    tmp = list()
    for i in range(len(c)):
        tmp.append(f"{c[i]:02x}")
    return "".join(tmp)+"\n"



finame = "Ultra_secret_message.txt"
foname = "Ultra_encrypted_message.txt"
target = open(foname, 'wb')


secret_sauce1 = bytes(datetime.today().isoformat(),"utf-8") 
target.write(secret_sauce1+b"\n")
secret_sauce2 = blake3(secret_sauce1).digest()
secret_sauce2 += bytes("\tBTS4410","utf-8")
               
               
with open(finame, 'rb') as source:
    while True:
        buffer = source.read(16)
        if len(buffer)<16:
            buffer = pad(buffer)
            ctxt = EK(buffer)    
            target.write(bytes(hexstr(ctxt),"utf-8"))
            break
        else:
            ctxt = EK(buffer)
            target.write(bytes(hexstr(ctxt),"utf-8"))
target.close()

