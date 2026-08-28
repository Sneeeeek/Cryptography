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

def milenage(K, RAND, SQN, AMF, OP):
    OPc = xor(OP, E(K, OP))
    TEMP = E(K, xor(RAND,OPc))
    IN1 = SQN+AMF+SQN+AMF

    OUT1 = xor(OPc, E(K, xor(c1, xor(TEMP, rotate(r1,xor(IN1, OPc))))))
    OUT2 = xor(OPc, E(K, xor(c2, rotate(r2, xor(TEMP, OPc)))))
    OUT3 = xor(OPc, E(K, xor(c3, rotate(r3, xor(TEMP, OPc)))))
    OUT4 = xor(OPc, E(K, xor(c4, rotate(r4, xor(TEMP, OPc)))))
    OUT5 = xor(OPc, E(K, xor(c5, rotate(r5, xor(TEMP, OPc)))))

    return {
            "f1":  OUT1[:8],
            "f1*": OUT1[8:],
            "f2":  OUT2[8:],
            "f5":  OUT2[:6],
            "f3":  OUT3,
            "f4":  OUT4,
            "f5*": OUT5[:6],
        }