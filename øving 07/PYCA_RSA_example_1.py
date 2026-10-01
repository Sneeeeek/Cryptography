"""
This is a very basic example of using RSA.
It is not "production" quality!

Generating keys, signing and verifying.
Note that the whole of the signed message is encrypted (and not a hashed version).

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

priv_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
pub_key = priv_key.public_key()


print("\n*** We have now generated a key-pair (RSA):\n")
print("Key size:", priv_key.key_size)


m = bytes("Denne meldinger er signert!","utf-8")

asympad = padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH)
s = priv_key.sign(m,asympad,hashes.SHA256())


print("\n*** S & V on our protected message:\n")
print("m :",str(m,"utf-8"))
print("m':",m)
print("s :",s)

#
# The signing was done with the private key!
# Everybody can verify the signature (requires the public key)
#
result = pub_key.verify(s,m,asympad,hashes.SHA256())
#
# Curiously, the results should be "None" is the verification succeeded.
#
print("v :",result==None)

#
# In principles, we may also "recover" the the message (which may be the message or a hash).
# But, this functionality is only partially supported by the current version of PYCA.
# That is, with padding=PKCS1v1 (which has its weaknesses).
#