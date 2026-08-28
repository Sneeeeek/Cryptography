from cryptography. hazmat. primitives. ciphers import Cipher, algorithms, modes

def E(k,m: bytes) -> bytes:
    """AES-128 in ECB mode"""
    assert len(m) == 16, "E(k,m): Input block m must be 16 bytes long (was {:d}).".format(len(m))
    assert len(k) == 16, "E(k,m): key must be 16 bytes long."

    encryptor = Cipher(algorithms.AES128(k),modes.ECB()).encryptor()
    return(encryptor.update(m) + encryptor.finalize())

def a2b(s: str) -> bytes:
    """Ascii to bytes. Require even length on string. """
    s = s.replace(" ","").strip()
    assert(len(s) % 2 == 0)
    bytelist = list()
    for i in range(0,len(s),2):
        bytelist.append(int("0x"+s[i]+s[i+1],16))

    return bytes (bytelist)

hexdig = "0123456789abcdef"
def b2a(b: bytes | bytearray    ) -> str:
    """Bytes to ascii a la TS 35.207/208 test data."""
    assert(len(b) > 0)
    #hexstr = Bits(b).hex
    hexstr = ""
    for byte in b:
        lo = hexdig[byte & 0x0F]
        hi = hexdig[byte >> 4]
        hexstr += hi+lo

    # our "default"
    if len(hexstr) == 32:
        hexstr = hexstr[0:8] + " "+ hexstr[8:16] + " " + hexstr[16:24] + " " + hexstr[24:]
    else:
        hs = ""
        while len(hexstr)>=8:
            hs = hs + hexstr[0:8] +" "
            hexstr = hexstr[8:]
            hexstr = hs + hexstr

    return(hexstr)

def xor(a,b: bytes) -> bytes:
    """xor bytes objects, must be the same length"""
    assert len(a) == len(b), "xor -- input a and must be same size."
    assert len(a) > 0, "xor -- input cannot be zero length."

    result = bytearray(len(a))

    for i in range(len(result)):
        result[i] = a[i] ^ b[i]
    return bytes(result)

def rotate(rotNum: int, input: bytes) -> bytes:
    # Divide by 8 since the rotate numbers are byte size. If they are not that you need to remove this.
    rotNum = rotNum//8 
    rotated = input[rotNum:]+input[0:rotNum]
    return bytes(rotated)

# $ 	TEST SET 1 INPUTS
# K:	465b5ce8 b199b49f aa5f0a2e e238a6bc
# RAND:	23553cbe 9637a89d 218ae64d ae47bf35
# SQN:	ff9bb4d0 b607
# AMF:	b9b9
# OP:	cdc202d5 123e20f6 2b6d676a c72cb318
# OPc:	cd63cb71 954a9f4e 48a5994e 37a02baf

# Inputs
K =     a2b("465b5ce8 b199b49f aa5f0a2e e238a6bc")
RAND =  a2b("23553cbe 9637a89d 218ae64d ae47bf35")
SQN =   a2b("ff9bb4d0 b607")
AMF =   a2b("b9b9")
OP =    a2b("cdc202d5 123e20f6 2b6d676a c72cb318")
OPc =   a2b("cd63cb71 954a9f4e 48a5994e 37a02baf")

# Constants
c1 = bytearray(16)

c2 = bytearray(16)
c2[-1] = 0b00000001

c3 = bytearray(16)
c3[-1] = 0b00000010

c4 = bytearray(16)
c4[-1] = 0b00000100

c5 = bytearray(16)
c5[-1] = 0b00001000

# Rotations
r1 = 64
r2 = 0
r3 = 32
r4 = 64
r5 = 96

TEMP = E(K, xor(RAND,OPc))
IN1 = SQN+AMF+SQN+AMF

OUT1 = xor(OPc,E(K,xor(c1,xor(TEMP,rotate(r1,xor(OPc,IN1))))))
OUT2 = xor(OPc,E(K,xor(c2,rotate(r2,xor(OPc,TEMP)))))
OUT3 = xor(OPc,E(K,xor(c3,rotate(r3,xor(TEMP,OPc)))))
OUT4 = xor(OPc,E(K,xor(c4,rotate(r4,xor(TEMP,OPc)))))
OUT5 = xor(OPc,E(K,xor(c5,rotate(r5,xor(TEMP,OPc)))))

# OUT1  4a9ffac3 54dfafb3 01cfaf9e c4e871e9
# OUT2  aa689c64 8370ac1e a54211d5 e3ba50bf
# OUT3  b40ba9a3 c58b2a05 bbf0d987 b21bf8cb
# OUT4  f769bcd7 51044604 12767271 1c6d3441
# OUT5  451e8bec a43b78e0 f940c8db 54fd21c1

# $ 	TEST SET 1 OUTPUTS
# f1:	4a9ffac3 54dfafb3
# f1*:	01cfaf9e c4e871e9
# f2:	a54211d5 e3ba50bf
# f5:	aa689c64 8370
# f3:	b40ba9a3 c58b2a05 bbf0d987 b21bf8cb
# f4:	f769bcd7 51044604 12767271 1c6d3441
# f5*:	451e8bec a43b

test_f1 = a2b("4a9ffac3 54dfafb3")
test_f1_alt = a2b("01cfaf9e c4e871e9")
test_f2 = a2b("a54211d5 e3ba50bf")
test_f5 = a2b("aa689c64 8370")
test_f3 = a2b("b40ba9a3 c58b2a05 bbf0d987 b21bf8cb")
test_f4 = a2b("f769bcd7 51044604 12767271 1c6d3441")
test_f5_alt = a2b("451e8bec a43b")

# The number is +1 what youd expect because there is a space, which is +1 letter
if OUT1[:8] == test_f1:
    print("F1       Correct -      ", OUT1[:8])
else:
    print("F1       Incorrect -    ", OUT1[:8])

if OUT1[8:] == test_f1_alt:
    print("F1*      Correct -      ", OUT1[8:])
else:
    print("F1*      Incorrect -    ", OUT1[8:])

if OUT2[8:] == test_f2:
    print("F2       Correct -      ", OUT2[8:])
else:
    print("F2       Incorrect -    ", OUT2[8:])

if OUT2[:6] == test_f5:
    print("F5       Correct -      ", OUT2[:6])
else:
    print("F5       Incorrect -    ", OUT2[:6])

if OUT3 == test_f3:
    print("F3       Correct -      ", OUT3)
else:
    print("F3       Incorrect -    ", OUT3)

if OUT4 == test_f4:
    print("F4       Correct -      ", OUT4)
else:
    print("F4       Incorrect -    ", OUT4)

if OUT5[:6] == test_f5_alt:
    print("F5_alt   Correct -      ", OUT5[:6])
else:
    print("F5_alt   Incorrect -    ", OUT5[:6])
