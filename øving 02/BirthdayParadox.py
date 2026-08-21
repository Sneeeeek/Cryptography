"""
A Simple Birthday Paradox test  --  https://en.wikipedia.org/wiki/Birthday_problem

On average, only 23 people need enter a room before there is a 50% chance of a collision.

Note that we use the standard random methods (based on the Mersenne Twister).
https://docs.python.org/3/library/random.html
"""
import random

#random.seed(42)     # Set the seed if you want repeatbility

birthdates = dict()    

print("\nThe Birthday Paradox: How many must enter the room?\n")
new_entry = random.randint(1,365)
i = 0

while  True:
    i += 1
    print("{:2d}: New entry, birthday on day: {:3d}".format(i,new_entry))
    if new_entry in birthdates: 
        print("\nNumber of entries: ",i)
        print("Collision for birthday on day {:d}. Entries: {:d} and {:d}".format(new_entry,birthdates[new_entry],i))
        break
    else:
        birthdates[new_entry] = i
        new_entry = random.randint(1,365)