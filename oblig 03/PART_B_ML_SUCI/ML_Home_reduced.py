from ML_SUCI_util import *
from cryptography import exceptions
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


PRIVPW   = bytes("BTS4410 Høsten 2026","utf-8")

cmd = cmd_arg([CMD_KEYGEN,CMD_DECONCEAL])

if cmd==None:
    err_print("\nNo valid command given.")
    sys.exit(1)


if cmd==CMD_KEYGEN:
    print("\nHome: Generating an ML-KEM 768 key-pair.\n")
    private_key, public_key = gen_MLKEM768_key_pair()
    
    print("    Key-pair generated.")
    
    len_priv_pem = len(store_private_key(private_key,PRIV_PEM,PRIVPW))
    print("    Private key stored in pem-file. Filesize:",len_priv_pem)
    
    len_pub_pem = len(store_public_key(public_key,PUB_PEM))
    print("    Public key stored in pem-file.  Filesize:",len_pub_pem)    
    
    print("\nHome: Command completed.")
    sys.exit(0)
    

if cmd==CMD_DECONCEAL:
    print("\nHome: Deconceal command given.\n")
    
    decapsulation_key = load_private_key(PRIV_PEM, PRIVPW)
    print("    Loaded own private decapsulation key.")
    
    f = open(ML_SUCI_FILE_NAME,"rb")
    raw_suci_data = f.read()
    f.close()
    print("    Loaded: "+ML_SUCI_FILE_NAME+", Length:",len(raw_suci_data))
    
    print("""
    
    -------------------------------------------------------------
    You must do the rest yourself.
    
    Good luck!
    -------------------------------------------------------------
    
    """)
    
    print("\nHome: Command completed.")    
    sys.exit(0)


err_print("\nSomething went wrong:",cmd)
sys.exit(1)