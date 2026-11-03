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

    # Splitt inn i individuelle delene
    IV = raw_suci_data[0:12]
    home_ID = raw_suci_data[12:27]
    ML_KEM_ciphertext = raw_suci_data[27:1117]
    AES_GCM_ciphertext = raw_suci_data[1117:1261]

    # Splitt igjen for å fjerne lenght prefixen. lenPrefix variablene er aldri brukt så man kan egentlig bare slette den.  
    ML_KEM_lenPrefix = ML_KEM_ciphertext[:2]
    ML_KEM_ciphertext = ML_KEM_ciphertext[2:]

    # Samme som før
    home_ID_lenPrefix = home_ID[:2]
    home_ID = home_ID[2:]

    # Decapsulate med private keyen
    decapped_data = decapsulation_key.decapsulate(ML_KEM_ciphertext)

    # Decapsulert data er nøkkelen vi bruker til å dekryptere
    aesgcm = AESGCM(decapped_data) 
    
    # Additional Authentication Data 
    aad = IV + home_ID + ML_KEM_ciphertext

    # dekrypter med IVen, ciphertext, og AADet
    AES_GCM_cleartext = aesgcm.decrypt(IV, AES_GCM_ciphertext, aad)

    # A boy named sue
    print("\n",AES_GCM_cleartext.decode())
    
    print("\nHome: Command completed.")    
    sys.exit(0)


err_print("\nSomething went wrong:",cmd)
sys.exit(1)