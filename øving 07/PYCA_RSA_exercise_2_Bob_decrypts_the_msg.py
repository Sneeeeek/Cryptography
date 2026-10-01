"""

This is part 3 of an exercise using RSA.
It is not "production" quality!

Bob loads Alices's ciphertext from a file.
Bob also loads he's public private key from a file.
Then he decrypts the message.

"""


from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

print("\n*** Bob needs to load Alice's encrypted message:\n")

ctext_name = "ciphertext.bin"
cipher_file = open(ctext_name,"rb")
c = cipher_file.read()
cipher_file.close()

print(">> Bob's read the ciphertext.")


priv_file = open("Bob_private_key.pem","rb")
priv_pem = priv_file.read()
priv_file.close()

priv_key = serialization.load_pem_private_key(priv_pem,password=None)

if isinstance(priv_key, rsa.RSAPrivateKey):
    print(">> Bob successfully loaded his own private key.\n>> It is",priv_key.key_size,"bits long.")
    
asympad = padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)

recovered_text = priv_key.decrypt(c,asympad)

print("\n>> The message was:'"+str(recovered_text,"utf-8")+"'")
