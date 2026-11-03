import blake3
import hashlib
from time import perf_counter

dbRuns = 100000
db3Runs = 10000

with open("oblig 03/Part_C_Blake3/datablob1.bytes", "rb") as dbFile:
    data = dbFile.read()
    start_time = perf_counter()
    for i in range(dbRuns): 
        blake3.blake3(data).hexdigest()
    end_time = perf_counter()

elapsed_time = end_time - start_time
print(f"BLAKE3 on DB1:     {elapsed_time:.6f}", "seconds")

with open("oblig 03/Part_C_Blake3/datablob1.bytes", "rb") as dbFile:
    data = dbFile.read()
    start_time = perf_counter()
    for i in range(dbRuns): 
        hashlib.sha3_256(data).hexdigest()
    end_time = perf_counter()

elapsed_time = end_time - start_time
print(f"SHA3 on DB1:       {elapsed_time:.6f}", "seconds")

with open("oblig 03/Part_C_Blake3/datablob2.bytes", "rb") as dbFile:
    data = dbFile.read()
    start_time = perf_counter()
    for i in range(dbRuns): 
        blake3.blake3(data).hexdigest()
    end_time = perf_counter()

elapsed_time = end_time - start_time
print(f"BLAKE3 on DB2:     {elapsed_time:.6f}", "seconds")

with open("oblig 03/Part_C_Blake3/datablob2.bytes", "rb") as dbFile:
    data = dbFile.read()
    start_time = perf_counter()
    for i in range(dbRuns): 
        hashlib.sha3_256(data).hexdigest()
    end_time = perf_counter()

elapsed_time = end_time - start_time
print(f"SHA3 on DB2:       {elapsed_time:.6f}", "seconds")

with open("oblig 03/Part_C_Blake3/datablob3.bytes", "rb") as dbFile:
    data = dbFile.read()
    start_time = perf_counter()
    for i in range(db3Runs): 
        blake3.blake3(data).hexdigest()
    end_time = perf_counter()

elapsed_time = end_time - start_time
print(f"BLAKE3 on DB3:     {elapsed_time:.6f}", "seconds")

with open("oblig 03/Part_C_Blake3/datablob3.bytes", "rb") as dbFile:
    data = dbFile.read()
    start_time = perf_counter()
    for i in range(db3Runs): 
        hashlib.sha3_256(data).hexdigest()
    end_time = perf_counter()

elapsed_time = end_time - start_time
print(f"SHA3 on DB3:       {elapsed_time:.6f}", "seconds")

# Algorithm	    Blob	        Time
# BLAKE3	    datablob1	    0.094804
# SHA3	        datablob1	    0.115236
# BLAKE3	    datablob2	    0.495742
# SHA3	        datablob2	    3.107946
# BLAKE3	    datablob3	    18.794108
# SHA3	        datablob3	    307.316511

# Blake3 er mye raskere enn SHA3.