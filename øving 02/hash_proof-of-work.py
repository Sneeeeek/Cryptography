"""
A naive little proof-of-work test with md5.

We are using MD5 here: in reality you'd use sha-256, scrypt, or similar

NOTE: MD5 is BROKEN!  --> https://en.wikipedia.org/wiki/MD5#Security

If you want to measure the execution time, then just run the timing() function.
Perhaps: timing(1000)
"""

import secrets
import timeit

from hashlib import md5


BLOCK = bytes("""
From Wikipedia, the free encyclopedia: https://en.wikipedia.org/wiki/Proof_of_work

Proof of work (PoW) is a form of cryptographic proof in which one party (the prover) proves to others (the verifiers) that a certain amount of a specific computational effort has been expended.[1] Verifiers can subsequently confirm this expenditure with minimal effort on their part. The concept was invented by Moni Naor and Cynthia Dwork in 1993 as a way to deter denial-of-service attacks and other service abuses such as spam on a network by requiring some work from a service requester, usually meaning processing time by a computer. The term "proof of work" was first coined and formalized in a 1999 paper by Markus Jakobsson and Ari Juels.[2][3]

Proof of work was later popularized by Bitcoin as a foundation for consensus in a permissionless decentralized network, in which miners compete to append blocks and mine new currency, each miner experiencing a success probability proportional to the computational effort expended. PoW and PoS (proof of stake) remain the two best known Sybil deterrence mechanisms. In the context of cryptocurrencies they are the most common mechanisms.[4]

A key feature of proof-of-work schemes is their asymmetry: the work – the computation – must be moderately hard (yet feasible) on the prover or requester side but easy to check for the verifier or service provider. This idea is also known as a CPU cost function, client puzzle, computational puzzle, or CPU pricing function. Another common feature is built-in incentive-structures that reward allocating computational capacity to the network with value in the form of cryptocurrency.[5][6]

The purpose of proof-of-work algorithms is not proving that certain work was carried out or that a computational puzzle was "solved", but deterring manipulation of data by establishing large energy and hardware-control requirements to be able to do so.[5] Proof-of-work systems have been criticized by environmentalists for their energy consumption.
""", 'utf-8')




def get_nonce() -> bytes:
    """Return a nonce 16 bytes long"""
    return(secrets.token_bytes(16))


def main(silent: bool = False):
    """ Our 'main' function"""
    cnt = 0
    LEADING_ZEROS = 5
    md_block = md5(BLOCK)

    if not silent:
        print("\n*** A naive 'proof-of-work' test with md5: the target has {:d} leading '0' (hexdigest).".format(LEADING_ZEROS))
        print("*** You can modify the number of zero's to see how it impacts the performance.")
        print("*** You may even modify the code to run sha256 (it's in the hashlib).\n")
    
    while True:
        md = md_block.copy()
        nonce = get_nonce()
        cnt += 1
        md.update(nonce)
        md_hexstr = md.hexdigest()
        if md_hexstr[0:LEADING_ZEROS] == '0'*LEADING_ZEROS: 
            if not silent:
                print("No.of tries: {:5d} --  the 'solution': ".format(cnt)+md_hexstr)
            break


def timing(ITER: int = 100):
    print("\nAve.execution time: ",
          "{:7.5f}".format(timeit.timeit("main(True)","from __main__ import main",number=ITER)/ITER), 
          "("+str(ITER),"iterations)")
    
if  __name__ == "__main__":
    main()
    
    response = input("\nRun the timing test (Y/N)? ").upper()
    if response == "Y":
        timing()