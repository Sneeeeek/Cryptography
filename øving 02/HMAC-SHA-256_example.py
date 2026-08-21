"""
A little HMAC-SHA256 example: the Kausf key.

This is similar to, but *not quite* like how the Kausf is derived.

We are cheating a bit :-)
"""
import hmac
import secrets

from bitstring import Bits

FC = bytes([0x6A])
P0 = bytes("www.TeleTull.no","utf-8")   # not correct!
L0 = bytes([len(P0)])

P1 = bytes(b'SQN^AK')
L1 = bytes([len(P1)])

S = FC + P0 + L0 + P1 + L1

CK = secrets.token_bytes(16)
IK = secrets.token_bytes(16)

Kausf = hmac.digest(CK+IK, S,'sha256')

print("\nThe Kausf anchor key, inputs:\n")
print("    CK:", Bits(CK).hex)
print("    IK:", Bits(IK).hex)
print("    FC:", Bits(FC).hex)
print("    P0:", Bits(P0).hex, ":",str(P0))
print("    L0:", Bits(L0).hex, ":",L0[0])
print("    P1:", Bits(P1).hex, ":",str(P1))
print("    L1:", Bits(L0).hex, ":",L1[0])

print("\nKausf : ", Bits(Kausf).hex, ":", len(Kausf),"bytes")
