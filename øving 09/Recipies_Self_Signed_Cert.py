"""

pyca Recipes Layer: X.509 - Creating a self-signed certificate


The code follows the outline provided in https://cryptography.io/en/latest/x509/tutorial/

"""

print("\nCreating a self-signed certificate.")

#
# Part 1: Generate and store RSA private key
#

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

priv_key_pw = bytes("BTS4410: Høstsemester.","utf-8")
priv_key_fname = "Self_sign_RSA_private_key.pem"

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
# Part 2: Generate and store the certificate
#
import datetime
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes

# Various details about who we are. For a self-signed certificate the
# subject and issuer are always the same.
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "NO"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Vestfold"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Campus Vestfold"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "BTS4410"),
    x509.NameAttribute(NameOID.COMMON_NAME, "bts4410.edu"),
])

cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.datetime.now(datetime.timezone.utc)
).not_valid_after(
    # Our certificate will be valid for 10 days
    datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30)
).add_extension(
    x509.SubjectAlternativeName([x509.DNSName("localhost")]),
    critical=False,
# Sign our certificate with our private key
).sign(key, hashes.SHA256())

# Write our certificate out to disk.
with open("OurVeryOwn_Certificate.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

    
print("Check out the new PEM-files.")
