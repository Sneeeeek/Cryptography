#
# sha256filecheck.py  -- USN, BTS4410, 2025
#

"""
This program reads a file and checks that the "sha256" digest matches.
It is a "toy" program, so don't use it for any real task!

The RPI image and sha256 files are found at:
https://downloads.raspberrypi.com/raspios_lite_armhf/images/raspios_lite_armhf-2024-07-04/
"""
import os
import sys
from hashlib import sha256

# the default target name
RPIOL = "2024-07-04-raspios-bookworm-armhf-lite.img.xz"
# the signature (checksum) is assumed to be in "RPIOL.sha256"


#----------------------------------------------------------------------------------------------------
# A little challenge: rewrite the program to scan for sha256 files.
# Then read the files, and check the checksum and target (based on the name in the sha256 file).
#----------------------------------------------------------------------------------------------------

#
# Read the file (fname) and compute the sha256 checksum.
#
def get_checksum(fname: str):
    "Read the file, and apply update the checksum"
    BUFSIZE = 102400
    buffer = bytes()
    flen = 0
    
    md = sha256()
    
    with open(fname, 'rb') as source:
        while True:
            buffer = source.read(BUFSIZE)
            flen += len(buffer)
            md.update(buffer)
            if len(buffer)==0: break
    return md
    
    
if  __name__ == "__main__":
    fname = input("Filename? (ENTER to use default name) ")
    if fname == "": fname = RPIOL   # when no name is given, use the default name
    if not os.path.isfile(fname): 
        print('ERROR: "'+fname+'" -- Not a file, or it does not exist!')
        sys.exit(1)
   
        
    csum = get_checksum(fname)
    byte_digest = csum.digest()
    hex_digest = csum.hexdigest()
    print('\nTarget file : "'+fname+'" successfully read.')
    print(  'Computed checksum: '+hex_digest)
    
    # find, open, read and close "sha256" file
    fnamechk = fname+".sha256"
    if not os.path.isfile(fnamechk): 
        print('\nERROR: Expected to find "'+fnamechk+'"')
        sys.exit(1)    
        
    fchk = open(fnamechk,'r')
    line = fchk.readline().strip()
    print("\nThe checksum in the "+fnamechk+" file was:\n"+'--> "'+line+'"')
    fchk.close()
    
    assumedchksum,assumedname = line.split()
    
    # do the checking
    print()
    if bytes.fromhex(assumedchksum) == byte_digest:      
        print("The checksum matched!")
    else:
        print("The checksum DID NOT match!")
        print("  -- Computed: ",byte_digest)
        print("  -- Provided: ",bytes.fromhex(assumedchksum))
    
    # the "sha256" file also contains the filename file to be checked
    if assumedname == fname:
        print("The filename matched!")
    else:
        print("The filename did not match:")
        print("  -- Provided by user: ",fname)
        print("  -- Provided in file: ",assumedname)
