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

# Inputs
K =     a2b("90dca4ed a45b53cf 0f12d7c9 ff00ff00")
RAND =  a2b("9fddc720 92c6ad03 6b6e4647 89315b78")
SQN =   a2b("20f813bd 4141")
AMF =   a2b("61df")
OP =    a2b("3ffcfe5b 7b111158 9920d352 8e84e655")
OPc =   xor(OP, E(K, OP))

# Test outputs
test_f1 = a2b("e19dba10 8a939e67")
test_f1_alt = a2b("2f5f6630 d19a267f")
test_f2 = a2b("f4fe7be8 a616cfa2")
test_f5 = a2b("7377d186 47f5")
test_f3 = a2b("763e40ff 2edfc4d4 94db50c4 c4e03861")
test_f4 = a2b("e0dcd466 6d9ada04 934c0409 25100bcc")
test_f5_alt = a2b("ad27eb05 f61a")

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

OUT1 = xor(OPc, E(K, xor(c1, xor(TEMP, rotate(r1,xor(IN1, OPc))))))
OUT2 = xor(OPc, E(K, xor(c2, rotate(r2, xor(TEMP, OPc)))))
OUT3 = xor(OPc, E(K, xor(c3, rotate(r3, xor(TEMP, OPc)))))
OUT4 = xor(OPc, E(K, xor(c4, rotate(r4, xor(TEMP, OPc)))))
OUT5 = xor(OPc, E(K, xor(c5, rotate(r5, xor(TEMP, OPc)))))

# Verification checks for if the output matches the test set.
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

print("\n","-"*75,"\n")

# Prints for easy copy paste to fill in the extra tests.
print("f1:  ", b2a(OUT1[:8]))
print("f1*: ", b2a(OUT1[8:]))
print("f2:  ", b2a(OUT2[8:]))
print("f5:  ", b2a(OUT2[:6]))
print("f3:  ", b2a(OUT3))
print("f4:  ", b2a(OUT4))
print("f5*: ", b2a(OUT5[:6]))