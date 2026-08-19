#
#  Vigenere's cipher -- with Norwegian letters, decimal digits, space, etc. to boot.
#

#
#  All characters in the input string must belong to the alphabet defined below.
#  That is, the encoding will proceed, but the code for an unknown character is -1.
#  This is due to the use of the "".find() method. 
#  As such, this 'error' has been permitted to exist.
#
#  The 'key' should be in the alphabeth.
#  Lowercase letters are accepted as input, but is converted to uppercase before coding.
#

import string

alphabet = string.ascii_letters + 'æøåÆØÅ' + string.digits + ' ' + '-:/,!?.'
alen = len(alphabet)


def E(key: str, msg: str) -> str:
    while len(msg)>len(key): key += key
    message = list(msg)
    for i in range(len(message)):
        n = alphabet.find(message[i])
        nkey = alphabet.find(key[i])
        message[i] = alphabet[(n + nkey) % alen]      
    return "".join(message)


def D(key: str, msg: str) -> str:
    while len(msg)>len(key): key += key
    message = list(msg)
    for i in range(len(message)):
        n = alphabet.find(message[i]) 
        nkey = alphabet.find(key[i])
        message[i] = alphabet[(n - nkey) % alen]      
    return "".join(message)

      
if  __name__ == "__main__":
    print("\n** Vigenere's cipher, extended version.\n")
    print("   Alphabet: '"+alphabet+"'")
    print("   Length  : ",alen,"\n")    
    

    ciphertext = "1fR-EssfN-SqEoNfNeE-SfToIoG"

    for a in alphabet:
        for b in alphabet:
            key = a + b
            with open("demofile.txt", "a") as f:
                f.write(key + ": " + D(key, ciphertext) + "\n")
            # print(key, D(key, ciphertext))

    # while True:
    #     k = input("=> Enter the cipher key (string) : ")
    #     m = input("=> Enter the plaintext message   : ")
        
    #     if (set(k) | set(m) | set(alphabet)) == set(alphabet):
    #         break
    #     print("\n*** The key and the message must belong to the alphabet!\n")

        
        
    # c = E(k,m)    
    # print()
    # print("== k: ",k)
    # print("== m: ",m)
    # print("== c: ",c)
    
    # print()
    # print("The key 'k' and the message 'm' can be modified.")
    # print("E(k,m)  and  D(k,c)  can be used.") 