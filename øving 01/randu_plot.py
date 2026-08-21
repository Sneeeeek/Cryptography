"""
The infamous RANDU linear congruential generator: https://en.wikipedia.org/wiki/RANDU

Visualized by using matplotlib.
This code was very much inspired by the following code: 
-- https://github.com/jacksonrakena/lcg-toolkit/blob/master/lcg.py

"...its very name RANDU is enough to bring dismay into the eyes and stomachs of many computer scientists!"

-- Donald E. Knuth, The Art of Computer Programming

"""
import matplotlib.pyplot as plt

# SEED VALUE
X0 = 1      #  RANDU: Sequence A096555 in the OEIS: https://oeis.org/A096555

SIZE = 10000
A = 65539   # MULTIPLICATIVE FACTOR
C = 0       # ADDITIVE FACTOR
M = 2**31   # MODULUS FACTOR


class RANDU():
    "Pseudorandom number generator RANDU, a (flawed) linear congruential PRNG."
    
    def __init__(self):
        self._state = X0

    def random(self):
        self._state = (A * self._state) % M
        return self._state / M



prng = RANDU()

x = []
y = []
z = []

for i in range(SIZE):
    x.append(prng.random())
    y.append(prng.random())
    z.append(prng.random())

fig = plt.figure(f'RANDU, points: {SIZE}') 
ax = fig.add_axes([0,0,1,1], projection='3d') # use 3d plotting


#----------------------------layout-------------------------------------
plt.style.use('ggplot')
fig.set_facecolor('w')
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
#-----------------------------------------------------------------------

#
# You might need to configure the timings, etc.
# The timing of the ploting behaved very differently on different machinesmemoryview
#

ax.plot(x,y,z,'.', color='#006F00')
ax.view_init(90, -90) # set initial view
plt.suptitle(f'X: {90}')
plt.draw()
plt.pause(2) # wait 2 secs, then start rotating


for angle in range(0, 361): # rotate the view
    plt.suptitle(f'X: {angle}')
    ax.view_init(angle,-45 + (angle // 5))
    plt.draw()
    plt.pause(0.01)

plt.pause(2)

for i in range(20):
    ax.view_init(85+i,-45) 
    plt.suptitle(f'The Planes: X: {85+i}')
    plt.draw()
    plt.pause(0.01)

plt.pause(2)
ax.view_init(97,00) 
plt.suptitle(f'The Planes: X: {97}')
plt.show()