import os
from ML_SUCI_util import *
from cryptography import exceptions
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


ENTITY_NAME_USER = "A Boy Named Sue"

cmd = cmd_arg([CMD_CONCEAL])

if cmd==None:
    err_print("\nNo valid command given.")
    sys.exit(1)


if cmd==CMD_CONCEAL:
    print("\nUser: Concealing a permanent identifier.\n")
    
    # Loading the Home Pulic key.
    home_pub_key = load_public_key(PUB_PEM)
    
   
    # generate shared key
    shared_key, encr_key = home_pub_key.encapsulate()
    print("    Using ML-KEM 768; size of 'ciphertext': {:4d} bytes".format(len(encr_key)))
    
   
    # add length indicator and padding (as appropriate)
    utf8_home_ID = bytes(ENTITY_NAME_HOME, "utf-8")
    utf8_user_ID = bytes(ENTITY_NAME_USER, "utf-8")
    home_ID = add_len_prefix(utf8_home_ID)
    user_ID = add_padding(add_len_prefix(utf8_user_ID),128)
    print("    Entity name home: '"+str(utf8_home_ID,"utf-8")+"'")
    print("    Entity name user: '"+str(utf8_user_ID,"utf-8")+"',")
    
    # Add a length prefix to the ML-KEM ciphertext
    pre_encr_key = add_len_prefix(encr_key)
   
    # using AEAD to encrypt/protect the "ML-SUCI" information.   
    aesgcm = AESGCM(shared_key) 
    IV = os.urandom(12)  
    aad = IV + utf8_home_ID + encr_key
    ct = aesgcm.encrypt(IV, user_ID, aad)
    
    ML_SUCI_data = IV + home_ID + pre_encr_key + ct
    print("\n    Data to be written to 'ML-SUCI_data.bin' file:")
    print("\t IV                   : {:4d} bytes".format(len(IV)))
    print("\t home_ID              : {:4d} bytes (incl. length prefix)".format(len(home_ID)))
    print("\t ML-KEM ciphertext    : {:4d} bytes (incl. length prefix)".format(len(pre_encr_key)))
    print("\t AES-GCM ciphertext   : {:4d} bytes ({:d} byte data + tag)".format(len(ct),len(user_ID))) 
    print("\t ML_SUCI_data.bin size: {:4d} bytes".format(len(ML_SUCI_data)))    
    print()
    
    suci_file = open(ML_SUCI_FILE_NAME,"wb")
    suci_file.write(ML_SUCI_data)
    suci_file.close()

    
    print("\nUser: Command completed.")
    sys.exit(0)
    

err_print("\nSomething went wrong:",cmd)
sys.exit(1)