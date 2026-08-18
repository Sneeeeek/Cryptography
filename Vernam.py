#
#  Vernam cipher -- with Norwegian letters, decimal digits, space, etc. to boot.
#

#
#  Note: we assume that all input and the key is in binary
#

import sys

def E(key: bytes, msg: bytes) -> bytes:
    """Encrypt (or decrypt) a message with XOR."""
    assert (len(key) >= len(msg)), "The key cannot be shorted than the message"
    
    # bytearray is mutable, while bytes is not.
    ba = bytearray(len(msg))        
    
    for i in range(len(msg)):
        ba[i] = key[i] ^ msg[i]
        
    return(bytes(ba))

      
if  __name__ == "__main__":
    print("\n** Vernam cipher, extended version.")
    print("** Input is read as utf-8, and converted to bytes.\n")
   

    k = bytes(input("=> Enter the cipher key (string) : "),"utf-8")
    m = bytes(input("=> Enter the plaintext message   : "),"utf-8")
    
    if len(k)<len(m):
        print("The key must be at least as long as the message!",file=sys.stderr)
        c = bytes("**  ERROR  ***","utf-8")
    else:
        c = E(k,m)
    

        
    print()
    print("== k: ",k)
    print("== m: ",m)
    print("== c: ",c)
    
