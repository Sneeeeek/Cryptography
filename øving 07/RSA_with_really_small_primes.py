# A silly little RSA example implementation
#
#
# We will need a few primes, and have decided to just look them up.
# -- https://t5k.org/lists/
# -- for us this will do: https://t5k.org/lists/small/10000.txt
#
# More info at: https://en.wikipedia.org/wiki/RSA_(cryptosystem)
#

import math
import random # this is the standard library !! not security minded

list_of_primes = []

default = True

def getPrimes():
    with open("øving 07/t5k.org_lists_small_10000.txt") as f:
        lines = f.readlines()
        
    # the 4 first lines is just text & the last is an "end." statement
    lines = lines[4:]
    del lines[-1]
    
    primes = list()
    
    for i in range(len(lines)):
        primes += list(map(int,lines[i].split()))  
    return primes



def choosePQ() -> tuple:
    """choose two similar size primes, p and q"""
    if default: return 61,53
    
    # p and q should not fairly similar in size
    
    p = random.choice(list_of_primes[50:100])
    q = p
    while (p == q):
        q = random.choice(list_of_primes[50:100])
    return p,q
    
    

def genN(p,q: int) -> int:
    return q*p

def choosePrime(upperlim: int) -> int:
    """choose a prime smaller than upperlim"""
    if default: return 17
    prime = upperlim
    while prime >= upperlim:
        prime = random.choice(list_of_primes)
    return prime

def cm_tot(p,q: int) -> int:
    """Carmichael's totient function of the product."""
    return math.lcm(p-1,q-1)
    
def chooseE(upperlim: int) -> int:
    """e must be coprime to the upper limit. 1 < e < upperlim."""
    # easiest to choose a prime, and the verify it.
    # that is, gcd(e,upperlim) should be 1
    
    while True:
        e_cand = choosePrime(upperlim)
        if math.gcd(e_cand,upperlim):
            break
    return e_cand
    
    
def findD(e,cmtot: int) -> int:
    """find the modular multiplicative inverse of e (mod cmtot)"""
    # we will cheat and just bf it
    start = (cmtot // e) + 1
    while (e*start)%cmtot != 1:
        start += 1
    return start
    
public_key = ()
private_key = ()


def encr(m: int) -> int:
    return m**public_key[1] % public_key[0]

def decr(c: int) -> int:
    return c**private_key[1] % private_key[0]


def testRSA(default: bool=True):
    global public_key, private_key
    
    p,q = choosePQ()
        
    n = genN(p,q)
    print("Our modulus is: "+str(n)+", which is the product of ",p," and ",q)

    cmtot = cm_tot(p,q)
    e = chooseE(cmtot)
    print("Our e (public key) is:",e)
    public_key = n,e

    d = findD(e,cmtot)
    print("Our d (private key) is:",d)
    private_key = n,d

    print("\nEncrypting a message m (0 <= m < {:d})".format(n))
    print("We are lazy -- let m be an integer")
    m = -1
    while not ((m>=0) and (m<n)):
        m = int(input("m: "))
    
    print("\nEncryption:")
    c = encr(m)
    print("m:",m)
    print("c:",c)

    print("\nDecryption:")
    m1 = decr(c)
    print("m1:",m1)
    print("c :",c)    


if __name__ == "__main__":
    print("\nRSA example with really small primes!!\n")

    # the first run is for the example from Wikipedia 
    default = True
    testRSA()
    print("\n"+"-"*80,"\n"*2)
    default = False
    
    # now we will pick primes from this list
    list_of_primes = getPrimes()
    while True:
        testRSA()
        c = input("\nContinue (Y/N)? ")
        if c.upper() != "Y": break
        
