"""

pyca Recipes Layer: X.509 - reating a Certificate Signing Request (CSR)


The code follows the outline provided in https://cryptography.io/en/latest/x509/tutorial/

"""

print("\nCreating a Certificate Signing Request (CSR).")

#
# Part 1: Generate and store RSA private key
#

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

priv_key_pw = bytes("BTS4410: Høstsemester.","utf-8")
priv_key_fname = "RSA_private_key.pem"

# generate a RSA private key
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Write our key to disk for safe keeping
with open(priv_key_fname, "wb") as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.BestAvailableEncryption(priv_key_pw),
    ))
    

#
# Part 2: Generate and store the CSR
#
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes

# Generate a CSR
csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
    # Provide various details about who we are.
    x509.NameAttribute(NameOID.COUNTRY_NAME, "NO"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Vestfold"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Campus Vestfold"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "BTS4410"),
    x509.NameAttribute(NameOID.COMMON_NAME, "bts4410.edu"),
])).add_extension(
    x509.SubjectAlternativeName([
        # Describe what sites we want this certificate for.
        x509.DNSName("bts4410.edu"),
        x509.DNSName("www.bts4410.edu"),
        x509.DNSName("cryptography.bts4410.edu"),
    ]),
    critical=False,
# Sign the CSR with our private key.
).sign(key, hashes.SHA256())
# Write our CSR out to disk.
with open("csr.pem", "wb") as f:
    f.write(csr.public_bytes(serialization.Encoding.PEM))
    
print("Check out the new private-key and CSR PEM-files.")
