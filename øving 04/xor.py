# xor.py

keystream = b'\x8bW\xbb\x02\xfb.\xf6\x15\xe3L~\x82l\x07D\x01\x95\x9e9_G56\x16\xbb\xc6AK\xbfD\x01\x8d'
ciphertxt = b'\xab}\x91(\xdbb\x93a\x97?\x15\xf0\tj0!\xe6\xf5K:,^\xf5\xae\xdc\xaa$k\x95n+\xad'

msg = b""

for i in range(len(keystream)):
    msg += bytes([keystream[i] ^ ciphertxt[i]])

print(msg)
print(str(msg, 'utf-8'))