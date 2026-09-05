# Import the algo from milenage.py
from milenage import a2b, b2a, milenage

# Inputs. Turned into bytes. a2b = ascii to bytes.
# OPc is never actually used anywhere since it can just be calculated using other fields, but the test suite included it so i just left it in there. 
K	 =	a2b("90dca4ed a45b53cf 0f12d7c9 ff00ff00")
RAND =	a2b("9fddc720 92c6ad03 6b6e4647 89315b78")
SQN	 =	a2b("20f813bd 4141")
AMF	 =	a2b("61df")
OP	 =	a2b("3ffcfe5b 7b111158 9920d352 8e84e655")
OPc	 =	a2b("a8bf85ac 76fd86e4 425239a6 17b856ae")
                
test_f1	    =   a2b("e19dba10 8a939e67")
test_f1_alt	=   a2b("2f5f6630 d19a267f")
test_f2	    =   a2b("f4fe7be8 a616cfa2")
test_f5	    =   a2b("7377d186 47f5")
test_f3	    =   a2b("763e40ff 2edfc4d4 94db50c4 c4e03861")
test_f4	    =   a2b("e0dcd466 6d9ada04 934c0409 25100bcc")
test_f5_alt	=   a2b("ad27eb05 f61a")
# Test outputs. Turned into bytes. This comment is below for easy copy paste with the test sets.
# Im copy pasting from this sheet i made for easy copy paste here: https://docs.google.com/spreadsheets/d/1qT5Uw7SLgi1RLOlfV0cF4XtgFoX7P0e9mOb2vXoejek/edit?usp=sharing
# I know i could write some file reading stuff but it would take longer than just doing it myself. 
# Its only 20 tests and i can do bulk operations with sheets anyways.  

# Run the algorithm
result = milenage(K, RAND, SQN, AMF, OP)

# Prints for easy copy paste. Here they are converted into ascii since its more readable.
# b2a = bytes to ascii.
print("OPc  ", b2a(result["OPc"]), "\n")
print("f1:  ", b2a(result["f1"]))
print("f1*: ", b2a(result["f1*"]))
print("f2:  ", b2a(result["f2"]))
print("f5:  ", b2a(result["f5"]))
print("f3:  ", b2a(result["f3"]))
print("f4:  ", b2a(result["f4"]))
print("f5*: ", b2a(result["f5*"]))

print("\n","-"*75,"\n")

# Verification checks for if the output matches the test set.
# Tabs are there for pretty print.
# if test_f1 in globals() is a check to see if the test_f1 variable exists or not. Its here so you can easily "enable/disable" this section by just commenting the test variables at the top. 
if 'test_f1' in globals():
    if result["f1"] == test_f1:
        print("F1       Correct -      ", result["f1"])
    else:
        print("F1       Incorrect -    ", result["f1"])

    if result["f1*"] == test_f1_alt:
        print("F1*      Correct -      ", result["f1*"])
    else:
        print("F1*      Incorrect -    ", result["f1*"])

    if result["f2"] == test_f2:
        print("F2       Correct -      ", result["f2"])
    else:
        print("F2       Incorrect -    ", result["f2"])

    if result["f5"] == test_f5:
        print("F5       Correct -      ", result["f5"])
    else:
        print("F5       Incorrect -    ", result["f5"])

    if result["f3"] == test_f3:
        print("F3       Correct -      ", result["f3"])
    else:
        print("F3       Incorrect -    ", result["f3"])

    if result["f4"] == test_f4:
        print("F4       Correct -      ", result["f4"])
    else:
        print("F4       Incorrect -    ", result["f4"])

    if result["f5*"] == test_f5_alt:
        print("F5*      Correct -      ", result["f5*"])
    else:
        print("F5*      Incorrect -    ", result["f5*"])