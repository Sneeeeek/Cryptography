#
#  Using module secrets and SystemRandom
#
"""This is a toy stub program that simply demonstrates use of module secrets"""

import secrets
import string

#
# You may want to look up the "secrets" and "random" modules.
#

alphabet = string.ascii_letters + string.digits + string.punctuation + " øæåØÆÅ"

print("\nThis is your suggested new password: '"+"".join(secrets.choice(alphabet) for i in range(16))+"'\n")


Finished = False
while not Finished:
    print("\nGuessing game: guess a number [0..10>, end with a non-digit (or invalid choice).")
    i = secrets.randbelow(10)
    cnt = 0
    while True:
        if cnt==3: 
            print("\nYou had 3 unsuccessful guesses.\nThe number was {:1d}\n".format(i))
            break
        
        guess = input("Your guess: ")
        if guess in string.digits:
            if int(guess) == i:
                print("\nLucky guess!!\n")
                break
            else:
                if int(guess) > i:
                    print("No, it's smaller.")
                else:
                    print("No, it's bigger.")
                cnt += 1
        else:
            print("\nOk,that wasn't a valid choice (unless you wanted to quit). Take care.\n")
            Finished = True
            break



TEST_SIZE = 10000000
print("\nTesting the frequncy for integers in [0..10>.   Iterations: {:d}\n".format(TEST_SIZE), flush=True)
numberof = list(0 for item in range(10))

print("Num: {:>9}".format("Percent:"),flush=True)
print("---- "+"-"*9,flush=True)

for i in range(TEST_SIZE):
    i = secrets.randbelow(10)
    numberof[i] += 1
    
for i in range(len(numberof)):
    pecent = 0
    print("{:3d}: {:9.4f}".format(i, numberof[i]*100/TEST_SIZE))