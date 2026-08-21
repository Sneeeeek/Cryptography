m1 = """
A little demonstration of the malleability of the one-time-pad (OTP). 
Here we use an XOR "trick" to modify the intercepted ciphertext.
This will translate to a modified plaintext."""

import os


def byte2binstr(b): return("{:08b}".format(b))
def bytes2hexstr(b): 
    # we assume b to be bytes or bytearray (or a list of byte-values)
    s = ""
    for i in range(len(b)):
        s = s+"{:02X}".format(b[i])+" "
    return(s.strip())
    

def xor128(a,b: bytes) -> bytes:
    assert len(a) == len(b), "Input of different lengths not permitted."
    assert len(a) == 16, "Input must be 16 (bytes)."
    c = bytearray(16)    
    for i in range(len(a)): c[i] = a[i] ^ b[i]
    return(bytes(c))


# note -- to simplify, we insist that everything is 128-bit (16-bytes) long. 
def E(K,P): return(xor128(K,P))
def D(K,C): return(xor128(K,C))


if __name__ == "__main__":
    print("\n"*2 + "-"*72, end="")
    print(m1)
    print("-"*72,"\n"*2)
    
    
    print("(1) " + "-"*68)    
    print("Generate the OTP and define the plaintext (p1).")
    print("Then, we encrypt p1 with the OTP (this is (P1 XOR OTP)):\n")

    otp = os.urandom(16)    
    p1  = b"Send $10000 to C"
    c1 = E(otp,p1)
    
    print("  Plaintext, p1 : '"+str(p1,"utf-8")+"'")
    print("  Hexfied p1    :",bytes2hexstr(p1))    
    print("  The OTP       :",bytes2hexstr(otp))
    print("  Ciphertext, c1:",bytes2hexstr(c1))  


    print("\n\n"+"(2) " + "-"*68)   
    print("Adversary goal:",p1,"\n")
    print("\t - change the sum of money from '1' into '2'")
    print("\t - change destination from 'C' to 'M'")
    
    
    print("\n\n"+"(3) " + "-"*68)   
    print("Determine the position of '1' in the sum of money (plaintext, p1).")
    print("Then, create a (byte) mask that we call 'mask2'.")
    print("We do all this on plaintext.\n")
    pos1 =  p1.find(b"1")
    the1 = p1[pos1]   
    print("  The '1' character (ascii,chr,binary):",the1,"'"+chr(the1)+"'",byte2binstr(the1))
    
    # mask2 is our byte mask.
    # by XORing it with the byte that holds "1", we can transform the ciphertext
    mask2 = 0b00000011       
    the2 = the1 ^ mask2 
    print("  The '2' character (ascii,chr,binary):",the2,"'"+chr(the2)+"'",byte2binstr(the2))
    
    
    # Rinse and repeat for the the receiver (C -> M)
    print("\n\n"+"(4) " + "-"*68)   
    print("Determine the position of 'C', and make a mask to get 'M'.")
    print("We call this mask for 'maskM' (also done on plaintext).\n")
    posC =  p1.find(b"C")
    theC = p1[posC]   
    theM = ord("M")
    print("  The 'C' character (ascii,chr,binary):",theC,"'"+chr(theC)+"'",byte2binstr(theC))
    print("  The 'M' character (ascii,chr,binary):",theM,"'"+chr(theM)+"'",byte2binstr(theM))    
    
    # This is how to make the mask (better way than for mask2)
    maskM = theC ^ theM  
    
        
    print("\n\n"+"(5) " + "-"*68)   
    print("Create a 'blockmask' mask for use with the ciphertext.")
    print("Done by inserting the masks into an all-zero block.")
    print("The masks are inserted into the plaintext positions.")
        
    blockmask = bytearray(16)
    blockmask[pos1] = mask2
    blockmask[posC] = maskM
    
    
    print("\n\n"+"(6) " + "-"*68)   
    print("Execute the XOR 'trick' :-)\n")    
    print("\t - c2 := c1 XOR blockmask")
    c2 = xor128(c1,blockmask)   
    
    
    print("\n\n"+"(7) " + "-"*68)      
    print("Recipient receives 'c2' and decrypt it with the OTP.")
    print("The decryption result is not p1 but p2.\n")
    print("  Ciphertext, c2:",bytes2hexstr(c2))  
    print("  The mask      :",bytes2hexstr(blockmask))    

    p2 = D(otp,c2) 

    print("\nDecryption: D(otp,c2) -> p2\n")
    print("  Hexfied p2    :",bytes2hexstr(p2))       
    print("  Plaintext, p2 : '"+str(p2,"utf-8")+"'")
