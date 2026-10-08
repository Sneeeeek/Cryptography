import sys
from datetime import datetime
import platform
import cryptography
from cryptography.hazmat.backends.openssl.backend import backend

print()
print("Today   :",datetime.today().strftime('%Y-%m-%d'))
print("Python  :",sys.version)
print("Platform:", platform.platform())
print()
print("You are running:\n")
print("  Cryptography", cryptography.__version__)
print("  "+backend.openssl_version_text())