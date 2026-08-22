"""
A Simple Birthday Paradox test  --  https://en.wikipedia.org/wiki/Birthday_problem

On average, only 23 people need enter a room before there is a 50% chance of a collision.

Note that we use the standard random methods (based on the Mersenne Twister).
https://docs.python.org/3/library/random.html
"""
# import random

# # random.seed(42)     # Set the seed if you want repeatbility

# birthdates = dict()    

# print("\nThe Birthday Paradox: How many must enter the room?\n")
# new_entry = random.randint(1,365)
# i = 0

# while  True:
#     i += 1
#     print("{:2d}: New entry, birthday on day: {:3d}".format(i,new_entry))
#     if new_entry in birthdates: 
#         print("\nNumber of entries: ",i)
#         print("Collision for birthday on day {:d}. Entries: {:d} and {:d}".format(new_entry,birthdates[new_entry],i))
#         break
#     else:
#         birthdates[new_entry] = i
#         new_entry = random.randint(1,365)


        # VERSION LOOKING FOR N COLLISSIONS
# import random
# from collections import defaultdict
# print("\nThe Birthday Paradox: How many must enter the room?\n")
# i = 0
# birthdatesList = defaultdict(int)

# while True:
#     new_entry = random.randint(1,365)
#     birthdatesList[new_entry] += 1
#     i += 1
#     print("{:2d}: New entry, birthday on day: {:3d}".format(i,new_entry))
#     if birthdatesList[new_entry] >= 6:
#         print("\nNumber of entries: ", i)
#         print("3 point collission for birthday on day", new_entry)
#         break


#         # VERSION LOOKING FOR SPECIFIC DATE
# import random
# print("\nHow many must enter the room to match my specific birthday?\n")
# new_entry = random.randint(1,365)
# i = 0

# while  True:
#     i += 1
#     print("{:2d}: New entry, birthday on day: {:3d}".format(i,new_entry))
#     if new_entry == 67: 
#         print("\nNumber of entries: ",i)
#         print("Collision for birthday on day {:d}. Entries: {:d}".format(new_entry,i))
#         break
#     else:
#         new_entry = random.randint(1,365)