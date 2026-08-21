"""
A naive little test of the avalanche property of hash functions.
We are using MD5 here, but any hash should have avalanche effects.

NOTE: MD5 is BROKEN!  --> https://en.wikipedia.org/wiki/MD5#Security
"""
import bitstring # get it with pip
import secrets
from hashlib import sha256


def bitdistance(a,b: str) -> int:
    if len(a) != len(b): return(-1)
    
    dist = 0
    for i in range(len(a)):
        if a[i] != b[i]: dist += 1
    return(dist)
    
    
if __name__ == "__main__":
    print("\n*** A naive 'bit avalanche' test of sha256: the 'distance' should be 64 on average.")
    
    START = secrets.randbelow(2**32)
    print("\n*** Start value: ",START,"\n")
    
    previous = bitstring.BitArray(bytes(16))
    ba = bitstring.BitArray(sha256(START.to_bytes(16)).digest())
    bitdist_acc = bitdistance(previous,ba)
    print(START,ba.bin+", Bitdistance all zero: ",bitdist_acc)  
    previous = ba
    
    ITER=32
    for i in range(START+1,START+ITER):
        ba = bitstring.BitArray(sha256(i.to_bytes(16)).digest())
        print(i,ba.bin,end="")    
        bitdist = bitdistance(ba,previous)
        bitdist_acc += bitdist
        print(", Bitdistance previous: ",bitdist)
        previous = ba
        
    print("\n*** Average bitdistance was: ",bitdist_acc/ITER)