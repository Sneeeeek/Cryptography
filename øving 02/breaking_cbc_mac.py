"""
Breaking CMC-MAC

The example uses AES-128 as the cipher.

tag - the hash output/icv
msg - message
key - the secret key

----

At step n in CBC-MAC, your xor the tag from the previous stage with the current block.
Then you encrypt the result with the secret key.

For the first step, one xors with all zeros. This is no-op step for the first block.
Then there is the encryption.

----

Assume that you have two single block messages, m1 and m2.

Then:

    tag1 := E(key,msg1)
    tag2 := E(key,msg2)
    
Now you have two pairs:

    (msg1,tag1) & (msg2,tag2)
    
Then you can deduce that:

    tag2 is the tag for the two-block message msg1 || (msg2 xor tag1)
    
Thus, without knowing the key, you can generate a properly signed two-block message.
This is fundamentally at odds with the property a MAC algorithm should have!

"""

import secrets
from bitstring import Bits
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

BLOCK_SIZE = 16
KEY_SIZE   = 128

msg1 = bytes("CMC-MAC = broken","utf-8")
msg2 = bytes(" Trust & verify!","utf-8")

key = secrets.token_bytes(KEY_SIZE//8)  # the key could be anything -- we don't need to know it!
allzero = bytes(BLOCK_SIZE)


def pad(b: bytes, length: int =  BLOCK_SIZE) -> bytes:
    assert length>0, "length must be greater than zero"
    while (len(b) % length) != 0:
        b = b + bytes([0xFF])
    return b
    

def xorblock(b1, b2: bytes) -> bytes:
    assert len(b1) == len(b2), "xorblock: b1 and b2 must have same length"
    bxor = bytearray(len(b1))
    for i in range(len(b1)): bxor[i] = b1[i] ^ b2[i]    
    return bytes(bxor)


def E(k,m: bytes) -> bytes:
    """AES-128 in ECB mode"""
    assert len(m) == 16, "E(k,m): Input block m must be 16 bytes long."
    assert len(k) == 16, "E(k,m): key must be 16 bytes long."
    
    encryptor = Cipher(algorithms.AES128(k),modes.ECB()).encryptor()
    return(encryptor.update(m) + encryptor.finalize())



def CBC_MAC_block(key, tag, msg: bytes) -> bytes:
    """1-block CBC-MAC"""
    # extract first 16 bytes from msg to cmb (the current message block)
    
    if (len(msg) >= BLOCK_SIZE):
        cmb = msg[0:BLOCK_SIZE]
        msg = msg[BLOCK_SIZE:]
    else:
        cmb = pad(msg)
        msg = b''
        
    # returns the current tag and the remaining message
    return E(key,xorblock(tag,cmb)), msg
    
    
def CBC_MAC(key, msg : bytes) -> bytes:
    tag = allzero
    while len(msg)>0:
        tag, msg = CBC_MAC_block(key, tag, msg)
    return tag

#
#  Takes a bytes object of lenght 16 (128 bit) as input
#  The output conform to the format provided in TS 35.207 for test data.
#
def b2a(b: bytes) -> str:
    """Bytes to ascii. For 16 bytes objects only. """
    assert len(b) == BLOCK_SIZE, "Lenght must be 16 bytes -- was {:d} for {:s}".format(len(b),str(b))
    hexstr = Bits(b).hex
    hexstr = hexstr[0:8] + " " + hexstr[8:16] + " " + hexstr[16:24] + " " + hexstr[24:]
    return(hexstr)


if __name__ == "__main__":

    print("\n*** Is (t2 == m1 || (m2 ^ t1)) ?  \n")
 
    msg1 = pad(msg1)
    msg2 = pad(msg2)
    
    print("Key  : ",b2a(key))
    print("msg1 : ",len(msg1), b2a(msg1))
    print("msg2 : ",len(msg2), b2a(msg2))    
    
    tag1 = CBC_MAC(key,msg1)
    tag2 = CBC_MAC(key,msg2)
    
    print("tag1 : ",len(tag1),b2a(tag1))
    print("tag2 : ",len(tag2),b2a(tag2))
    
    print("\nNow we construct msg3 to be: m1 || (m2 ^ t1)\n")
    msg3 = msg1 + xorblock(msg2,tag1)

    print("msg3 : ",len(msg3), b2a(msg3[0:BLOCK_SIZE]), b2a(msg3[BLOCK_SIZE:]))
    tag3 = CBC_MAC(key,msg3)
    print("tag3 : ",len(tag3),b2a(tag3))
    
    
    print("\nThen we have: (tag2 == tag3) is",tag3 == tag2)
    


    


    
    