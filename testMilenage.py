from milenage import a2b, b2a, milenage

# Inputs
K	 =	a2b("	465b5ce8 b199b49f aa5f0a2e e238a6bc	")
RAND	 =	a2b("	23553cbe 9637a89d 218ae64d ae47bf35	")
SQN	 =	a2b("	ff9bb4d0 b607	")
AMF	 =	a2b("	b9b9	")
OP	 =	a2b("	cdc202d5 123e20f6 2b6d676a c72cb318	")
OPc	 =	a2b("	cd63cb71 954a9f4e 48a5994e 37a02baf	")
				
test_f1	 =	a2b("	4a9ffac3 54dfafb3	")
test_f1_alt	 =	a2b("	01cfaf9e c4e871e9	")
test_f2	 =	a2b("	a54211d5 e3ba50bf	")
test_f5	 =	a2b("	aa689c64 8370	")
test_f3	 =	a2b("	b40ba9a3 c58b2a05 bbf0d987 b21bf8cb	")
test_f4	 =	a2b("	f769bcd7 51044604 12767271 1c6d3441	")
test_f5_alt	 =	a2b("	451e8bec a43b	")
# Test outputs. This comment is below for easy copy paste with the test sets.
# Im copy pasting from this sheet i made for easy copy paste here: https://docs.google.com/spreadsheets/d/1qT5Uw7SLgi1RLOlfV0cF4XtgFoX7P0e9mOb2vXoejek/edit?usp=sharing
# I know i could write some file reading stuff but i didnt want to deal with allat. 
# Its only 20 tests and i can do bulk operations with sheets anyways.  

# Run the script
result = milenage(K, RAND, SQN, AMF,  OP)

# Prints for easy copy paste.
print("f1:  ", b2a(result["f1"]))
print("f1*: ", b2a(result["f1*"]))
print("f2:  ", b2a(result["f2"]))
print("f5:  ", b2a(result["f5"]))
print("f3:  ", b2a(result["f3"]))
print("f4:  ", b2a(result["f4"]))
print("f5*: ", b2a(result["f5*"]))

print("\n","-"*75,"\n")

# Verification checks for if the output matches the test set.
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