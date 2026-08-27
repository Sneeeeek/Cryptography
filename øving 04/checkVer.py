import sys
import cryptography
from cryptography.hazmat.backends.openssl.backend import backend
print()
print("Python",sys.version,"\n")
print(" Cryptography", cryptography.__version__)
print(" "+backend.openssl_version_text())