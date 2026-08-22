"""
Merkle-Damgård padding scheme.
See page 123 in "Serious Cryptography (2ed)".

We assume a 96 bit block size here.
That is NOT a realistic block size!
However, it looks better in the printout :-)
"""
BLOCKSIZE =  12


def hexdig(hex_digit: int) -> str:
    HEXDIG = "0123456789ABCDEF"
    if hex_digit>=0 and hex_digit<=15:
        return HEXDIG[hex_digit]
    else:
        return("#")
    
def hexout(b: bytes) -> str:
    hexstr = ""
    for i in range(len(b)):
        out = b[i]
        hi = out // 16
        lo = out % 16     
        hexstr = hexstr + " " + hexdig(hi) + hexdig(lo) 
    return hexstr.strip() 


def PaddingExample(s: str = ""):
    print("\nM-D padding example. Blocks are just 12 bytes in our example.\n")
    
    if s == "":
        data = input("Input data: ").encode("utf-8")
    else:
        data = s.encode("utf-8")
    
    
    remainder= len(data) % BLOCKSIZE
    block_cnt = len(data) // BLOCKSIZE
    
    print()
    print("The original input   :",data)
    print("\nNumber of full blocks:",block_cnt)
    print("                 --->>",data[:BLOCKSIZE*block_cnt])    


    padding_block = data[BLOCKSIZE*block_cnt:]  
    print("\nBytes in last block  :",remainder, "(bits: "+str(remainder*8)+")") 
    print("                 --->>",padding_block)
          
    appendix = bytearray(BLOCKSIZE - remainder)
    appendix[0] = 0b10000000
    
    print()
    padding_block = padding_block + appendix
    print("Padding block, w/'1' :",hexout(padding_block))
    
    if (len(padding_block) != BLOCKSIZE): print("Error")
    number = remainder * 8
    byte_num = number.to_bytes()   
    padding_block = padding_block[:-1]
    padding_block += byte_num
    print("Padding block, final :",hexout(padding_block))


if  __name__ == "__main__":
    PaddingExample("Dette er en block")