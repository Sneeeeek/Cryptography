"""

This is part 2 of an exercise using RSA.
It is not "production" quality!

Alice loads Bob's public-key PEM file,
extracts the key and encrypts a message m.
This message is then saved to "ciphertext.bin".

"""

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key

print("\n*** Alice needs to load Bob's public key:\n")

pub_file = open("Bob_public_key.pem","rb")
pub_pem = pub_file.read()
pub_file.close()

print(">> Bob's PEM files read.")


pub_key = load_pem_public_key(pub_pem)
if isinstance(pub_key, rsa.RSAPublicKey):
    print(">> Bob's public key was successfully loaded.\n>> It is",pub_key.key_size,"bits long.\n")
    
text_input = input("Enter the plaintext: ")
byte_input = bytes(text_input,"utf-8")

print("\n>> The plaintext is",len(byte_input),"bytes long.")

#
# We encrypt with Bob's public key.
#
asympad = padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
c = pub_key.encrypt(byte_input,asympad)

print(">> The ciphertext is",len(c),"bytes long (it is padded).\n")

ctext_name = "ciphertext.bin"
cipher_file = open(ctext_name,"wb")
cipher_file.write(c)
cipher_file.close()


print(">> The ciphertext is witten to the '"+ctext_name+"' file.\n")