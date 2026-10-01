"""

This is a very basic example of using RSA.
It is not "production" quality!

Generating keys, encrypting and decrypting.

You are encouraged to play around with it.
- change the key size (it takes way longer with long keys)
- change the padding
- change the message
- serialize the keys (in order to write them to a file)

"""

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

#
# Generate a private key, 2048 bit.
# We use the recommended exponent.
# Note that the private key is an object.

priv_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

# Some fields & methods that the private key class has
pub_key = priv_key.public_key()
internals = priv_key.private_numbers()

print("\n*** We have now generated a private key (RSA):\n")

print("Key size:", priv_key.key_size)

print("The internal parameter were (crt coefficients not included): ")
print("  p:",internals.p)
print("  q:",internals.q)
print("  d:",internals.d)


m = bytes("Det hemmelig møtet er ved Adalstjern kl.1400","utf-8")

#
# We encrypt with the public key.
# Everybody can do this! (we assume the public key is truly public)
#
asympad = padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
c = pub_key.encrypt(m,asympad)

print("\n*** E & D on our secret message:\n")
print("m :",str(m,"utf-8"))
print("m':",m)
print("\nc :",c)

#
# You can only decrypt if you have the private key.
# Of course, even so, you cannot know who sent the message (no integrity or message origin authentication)
#
d = priv_key.decrypt(c,asympad)
print("\nd':",d)
print("d :",str(d,"utf-8"))
