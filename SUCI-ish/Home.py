from SUCI_util import *
from cryptography import exceptions
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


PRIVPW   = bytes("BTS4410 Høsten 2025","utf-8")

cmd = cmd_arg([CMD_KEYGEN,CMD_DECONCEAL])

if cmd==None:
    err_print("\nNo valid command given.")
    sys.exit(1)


if cmd==CMD_KEYGEN:
    print("\nHome: Generating long-term ECDH key-pair.")
    private_key, public_key = gen_ECDH_key_pair(ec.SECP256R1())
    
    print("    Key-pair generated.")
    
    len_priv_pem = len(store_private_key(private_key,PRIV_PEM,PRIVPW))
    print("    Private key stored in pem-file. Filesize:",len_priv_pem)
    
    len_pub_pem = len(store_public_key(public_key,PUB_PEM))
    print("    Public key stored in pem-file.  Filesize:",len_pub_pem)    
    
    print("Home: Command completed.")
    sys.exit(0)
    

if cmd==CMD_DECONCEAL:
    print("\nHome: Deconceal command given.")
    
    priv_key = load_private_key(PRIV_PEM, PRIVPW)
    print("    Loaded own private key. Size:",priv_key.key_size)
    
    f = open(SUCI_FILE_NAME,"rb")
    raw_suci_data = f.read()
    f.close()
    print("    Loaded: "+SUCI_FILE_NAME+", Length:",len(raw_suci_data))

    IV = raw_suci_data[0:16]
    home_ID = raw_suci_data[16:80]
    user_pub = raw_suci_data[80:260]
    ct = raw_suci_data[260:340]

    aad = IV + home_ID + user_pub

    home_ID_length = int.from_bytes(home_ID[0:2])

    home_ID = home_ID[2:(home_ID_length+2)] # Må legge på to etter prefixen for å kompensere for lengdeprefiksen

    home_ID = home_ID.decode("utf-8")

    print("Home_ID: ", home_ID)


    user_pub_length = int.from_bytes(user_pub[0:2])

    user_pub = user_pub[2:(user_pub_length+2)]

    user_pub = serialization.load_pem_public_key(user_pub) #Gjør om fra bytes til et EC key objekt

    dhs = priv_key.exchange(ec.ECDH(), user_pub)

    session_key = key_derivation(dhs) # For å få AES nøkkelen

    aesgcm = AESGCM(session_key)

    user_ID = aesgcm.decrypt(IV, ct, aad) # Dekrypterer user_ID, på motsatt måte som ble gjort i User.py

    user_ID_length = int.from_bytes(user_ID[0:2])

    user_ID = user_ID[2:(user_ID_length+2)]

    user_ID = user_ID.decode("utf-8")

    print("The decoded user ID is: ", user_ID)
    
    print("Home: Command completed.")    
    sys.exit(0)


err_print("\nSomething went wrong:",cmd)
sys.exit(1)