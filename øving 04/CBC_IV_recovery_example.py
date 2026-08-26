"""
We shall carry out a little CBC-based experiment.
What will happen if the decryption is done with a wrong IV?
That is to say, what is the error-recovery properties of CBC?

And, what if there is a bit error somewhere?


Note that we use PKCS#7 padding.
"""
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

from bitstring import Bits
import secrets
import string
import os

# We are using os.urandom to get n pseudo-random bytes 
key = os.urandom(16)
IV  = bytes('"Not even wrong"',"utf-8")     # see https://en.wikipedia.org/wiki/Not_even_wrong

msg = bytes("""Anyone, from the most clueless amateur to the best cryptographer, can create an algorithm that he himself can’t break. 
It’s not even hard. What is hard is creating an algorithm that no one else can break, even after years of analysis. 
And the only way to prove that is to subject the algorithm to years of analysis by the best cryptographers around.
""", "utf-8")
# from https://www.schneier.com/blog/archives/2011/04/schneiers_law.html
    

#
# A primitive one-trick-pony formatter
# Assuming block of 16 bytes
#
def blockbfmt(b: bytes) -> str:
    s = ""
    for byte in b:
        h = hex(byte)[2:]
        if len(h)==1: h = "0"+h
        s = s + h + " "
    return(s[:-1])


class EncrMngr:
    def __init__(self, key, iv):        
        aesContext = Cipher(algorithms.AES(key), modes.CBC(iv))
        self.encryptor = aesContext.encryptor()
        self.padder = padding.PKCS7(128).padder()

    def update_encryptor(self, plaintext):
        return self.encryptor.update(self.padder.update(plaintext))

    def finalize_encryptor(self):
        return self.encryptor.update(self.padder.finalize()) + self.encryptor.finalize()


class DecrMngr:
    def __init__(self, key, iv):        
        aesContext = Cipher(algorithms.AES(key), modes.CBC(iv))
        self.decryptor = aesContext.decryptor()
        self.unpadder = padding.PKCS7(128).unpadder()

    def update_decryptor(self, ciphertext):
        return self.unpadder.update(self.decryptor.update(ciphertext))

    def finalize_decryptor(self):
        return self.unpadder.update(self.decryptor.finalize()) + self.unpadder.finalize()


# remove unprintable characters
def rmup(b: bytes): 
    res = bytearray(b)
    for i in range(len(b)):
        if chr(b[i]) not in string.printable: 
            res[i] = ord(b"_")
    return res

                                   
if __name__ == "__main__":
   
    # 
    #  Normal case
    #
    
    encr = EncrMngr(key,IV)
    decr = DecrMngr(key,IV)    
    
    print("\n***  Testing out CBC -- first checking a normal case.\n")
    print("The key: ",Bits(key).hex)
    print("The key: ",blockbfmt(key))
    print("The IV:  ",blockbfmt(IV))

    print("\n")
    print("Encrypting the plaintext message: len={:d}\n".format(len(msg)))
    print(str(msg,"utf-8"),"\n")
    
    ctxt = bytearray()
    
    ctxt += encr.update_encryptor(msg) + encr.finalize_encryptor()
   
    print("The ciphertext: len={:d}\n".format(len(ctxt)))
    print(ctxt,"\n")
    
    recovered = bytearray()
    recovered += decr.update_decryptor(ctxt) + decr.finalize_decryptor()    
    print("The recovered plaintext: len={:d}\n\n".format(len(recovered))+str(recovered,"utf-8"),"\n")
    
    #
    #  Wrong IV
    #
    
    IVencr = IV
    IVdecr = bytes(16)
    encr = EncrMngr(key,IVencr)
    decr = DecrMngr(key,IVdecr)    
    
    print("\n***  Testing out CBC -- Corrupted/wrong IV.\n")
    print("The key: ",Bits(key).hex)
    print("The key: ",blockbfmt(key))
    print("IVencr : ",blockbfmt(IVencr))
    print("IVdecr : ",blockbfmt(IVdecr))
    
    print("\n")
    print("Encrypting the plaintext message: len={:d}\n".format(len(msg)))
    print(str(msg,"utf-8"),"\n")
    
    ctxt = bytearray()
    
    ctxt += encr.update_encryptor(msg) + encr.finalize_encryptor()
   
    print("The ciphertext: len={:d}\n".format(len(ctxt)))
    print(ctxt,"\n")
    
    recovered = bytearray()
    recovered += decr.update_decryptor(ctxt) + decr.finalize_decryptor()    
    print("The recovered plaintext: len={:d}\n\n".format(len(recovered))+str(recovered,"utf-8"),"\n")
    
    # 
    #  Corrupted the first byte in the first block
    #
    
    encr = EncrMngr(key,IV)
    decr = DecrMngr(key,IV)      
    print("\n***  Testing out CBC -- Corrupted bit in first ciphertext block.\n")
    print("The key: ",Bits(key).hex)
    print("The key: ",blockbfmt(key))
    print("The IV:  ",blockbfmt(IV))

    print("\n")
    print("Encrypting the plaintext message: len={:d}\n".format(len(msg)))
    print(str(msg,"utf-8"),"\n")
    
    ctxt = bytearray()
    
    ctxt += encr.update_encryptor(msg) + encr.finalize_encryptor()
    
    print("Corrupting the first byte in the first block")
    ctxt = bytearray(ctxt)   # ctxt was a bytes object (immutable)
    origbyte = ctxt[0]
    ctxt[0] = origbyte ^ 0b00010000 # our bitflipping trick
    ctxt = bytes(ctxt)
    print("Original ciphertext (first byte):",bin(origbyte))
    print("The corrupted first byte is now: ",bin(origbyte ^ 0b00010000))

    
    print("The ciphertext: len={:d}\n".format(len(ctxt)))
    print(ctxt,"\n")
    
    recovered = bytearray()
    recovered += decr.update_decryptor(ctxt) + decr.finalize_decryptor()    
    print("The recovered plaintext: len={:d}\n\n".format(len(recovered)))
    
    recovered = rmup(recovered)
    print(str(recovered,"utf-8"),"\n")