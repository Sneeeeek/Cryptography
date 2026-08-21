#
# randu -- https://en.wikipedia.org/wiki/RANDU
#
# "IBM's RANDU is widely considered to be one of the most ill-conceived random number generators ever designed."
#


state = 1 # the seed needs to be an odd number

def RANDU() -> int:
    global state
    state = (state * 65539) % 2**31
    return state

if __name__ == "__main__":
    print("\nA minimal test of RANDU. But, don't be fooled. It's BAD.\n")
    for i in range(20):
        print(RANDU())