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
    

    otp = bytes("En dårlig OTP!!",'utf-8')    
    p1 = B"BTS4420 er BEST!"
    c1 = E(otp,p1)
    
    print("  Plaintext, p1 : '"+str(p1,"utf-8")+"'")
    print("  Hexfied p1    :",bytes2hexstr(p1))    
    print("  The OTP       :",bytes2hexstr(otp))
    print("  Ciphertext, c1:",bytes2hexstr(c1) + "\n")  

    pos1 =  p1.find(b"2")
    the1 = p1[pos1]   
    print("  The '2' character (ascii,chr,binary):",the1,"'"+chr(the1)+"'",byte2binstr(the1))
    
    # mask2 is our byte mask.
    # by XORing it with the byte that holds "1", we can transform the ciphertext

        #LÆRERN HADDE XORet DET PÅ FORHÅND, HER GJØR DEN DET FOR MEG. DET ER I HEX -> 3
    mask2 = 0b11    #ord("2") ^ ord("1")
        #Equivlent til hexene til 2 og 1 (32 og 31) XORet sammen til 03

    the2 = the1 ^ mask2 
    print("  The '1' character (ascii,chr,binary):",the2,"'"+chr(the2)+"'",byte2binstr(the2))

        
    blockmask = bytearray(16)
    blockmask[pos1] = mask2
    
    c2 = xor128(c1,blockmask)   
    
    
    print("\n\n"+ "-"*68)      
    print("Recipient receives 'c2' and decrypt it with the OTP.")
    print("The decryption result is not p1 but p2.\n")
    print("  Ciphertext, c2:",bytes2hexstr(c2))  
    print("  The mask      :",bytes2hexstr(blockmask))    

    p2 = D(otp,c2) 

    print("\nDecryption: D(otp,c2) -> p2\n")
    print("  Hexfied p2    :",bytes2hexstr(p2))       
    print("  Plaintext, p2 : '"+str(p2,"utf-8")+"'")

    print("\n\n c1:", bytes2hexstr(c1))
    print("\n c2:", bytes2hexstr(c2))