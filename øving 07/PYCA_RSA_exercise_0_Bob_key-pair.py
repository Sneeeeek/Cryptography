"""

This is part 1 of an exercise using RSA.
It is not "production" quality!

Bob is generating keys, and then serializes the keys.
Note that you would normally have a strict system for handling the keys!

"""

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

#
# Generete a private key.
# The exponent is *strongly* recommended.
# Note the the private key is an object.

priv_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

# Some fields & methods that the private key class has
pub_key = priv_key.public_key()
internals = priv_key.private_numbers()


print("\n*** Bob have now generated a private key (RSA):\n")

print("Key size:", priv_key.key_size)

pub_pem = pub_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo)

pub_file = open("Bob_public_key.pem","wb")
pub_file.write(pub_pem)
pub_file.close()

priv_pem = priv_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption())

priv_file = open("Bob_private_key.pem","wb")
priv_file.write(priv_pem)
priv_file.close()

print("Bob's PEM files written.")