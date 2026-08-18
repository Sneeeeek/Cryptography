#
#  Caesar's cipher -- with Norwegian letters, decimal digits, space, etc. to boot.
#

#
#  All characters in the input string must belong to the alphabet defined below.
#  Only uppercase letters are supported (using upper() to modify lowercase to uppercase).
#  Note that unrecognized input charcters as seen as belonging to position -1.
#  (-1 is the last character of the alphabet)
#  Thus, the input will be processed. 
#
#  The 'key' should be in the same range as the length of the alphabeth (starting at 0).
#  Lowercase letters are accepted as input, but is converted to uppercase before coding.
#

import string

alphabet = string.ascii_uppercase + 'ÆØÅ' + string.digits + ' ' + ',!?.'
alen = len(alphabet)


#
# The string is converted to a list (strings are immutable).
# Then the rotation by "key" positions (modulo alphabet size)
#
def Transmute(key: int, msg: str) -> str:
    message = list(msg.upper())
    for i in range(len(message)):
        n = alphabet.find(message[i])
        message[i] = alphabet[(n + key) % alen]      
    return "".join(message)


def E(key: int, msg: str) -> str:
    return(Transmute(key,msg))

def D(key: int, msg: str) -> str:
    return(Transmute(-key,msg))
    
    
def bf(c: str) -> None:
    print("Brute-force on '"+c+"'")
    for i in range(alen):
        print("Key={:02d}: '".format(i)+D(i,c)+"'")


def kpt(c: str, known: str) -> tuple:
    """Brute-force and check for a known plaintext string."""
    known = known.upper()
    for i in range(alen):
        if known in D(i,c):
            return(i, D(i,c))
    
    return(-1,"No known plaintext match!")
        
        
if  __name__ == "__main__":
    print("\n** Caesar cipher, extended version.\n")
    print("   Alphabet: '"+alphabet+"'")
    print("   Length  : ",alen,"\n")
    
    ckey = "?"
    key = -1

    bf("XÆA5MA9Z1XV1VOMUV7MV5M9ZØ7ZXQ")
    
    # while True:
    #     ckey = input("=> Enter the cipher key (int > 0): ")
    #     if ckey.isdigit():
    #         key = int(ckey)
            
    #         if key>=0 and key<=alen:
    #             break
    #         else:
    #             print("\n *** Outside of range.\n")            
    #     else:
    #         print("\n *** Not a valid number.\n")
            

    # while True:
    #     m = input("=> Enter the plaintext message   : ").upper()
    #     if (set(m) | set(alphabet)) == set(alphabet):
    #         break
    #     else:
    #         print("\n *** Message characters must belong to the alphabet.\n")

            
    # c = E(key,m)
    
    # print()
    # print("== Key: ",key)
    # print("== Plaintext:  ",m)
    # print("== Ciphertext: ",c)
    
    # print("\nYou may now play around with E() and D().")
    # print("E(key,m)  and  D(key,c)  can be used. c, m and k (key) is available.\n") 