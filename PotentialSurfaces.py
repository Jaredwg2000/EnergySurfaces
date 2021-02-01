"""Calculates potenital surfaces.

Takes an input n, a number of particles, and an input to choose as
type of potential, then finds a minimum of an energy surface
to find the equilibrium geometry of the particles.
"""

# import numpy as np
import math
from random import random
import matplotlib.pyplot as plt


class vec3d:
    """A 3D cartesian vector.

    This is taken for the most part from the handout.
    """

    def __init__(self, lst=(0, 0, 0)):
        """Initialize vector.

        lst is a tuple or list with three elements (default (0, 0, 0)).
        """
        self.r = list(lst)

    def length(self):
        """Return the length of the vector."""
        return math.sqrt(self.r[0]*self.r[0] + self.r[1]*self.r[1] +
                         self.r[2]*self.r[2])

    def __sub__(self, other):
        """Subtract self to other and return the result."""
        ret = vec3d()
        for i in range(3):
            ret.r[i] = self.r[i] - other.r[i]
        return ret


def potentialLJ(positions):
    """Calculate the potential of the particles using the LJ potential.

    Takes the particle positions in a list as input, and outputs the potential
    energy by summing each pairwise term.
    """
    U = 0.0

    # Loop through each pair of particles
    for i, posi in enumerate(positions):
        for j, posj in enumerate(positions):
            if(j > i):
                rVec = posi - posj

                # Calculate the LJ potential for that pair
                U += 4*(pow(rVec.length(), -12) - pow(rVec.length(), -6))
    return U


def potentialMorse(positions):
    """Calculate the potential of the particles using the LJ potential.

    Takes the particle positions in a list as input, and outputs the potential
    energy by summing each pairwise term. Also uses the value of r_e/σ
    but does not need this as an input.
    """
    U = 0.0

    # Loop through each pair of particles
    for i, posi in enumerate(positions):
        for j, posj in enumerate(positions):
            if(j > i):
                rVec = posi - posj
                # Calculate the Morse potenital for the pair
                U += pow(1 - pow(math.e, rVec.length() - morseRe), 2)
    return U


def nudgePositions(positions, factor, potential):
    """Calculate the new positions of the particles.

    Takes the positions, a factor and a potential as input, calculates
    the gradient using finite differences, and nudges the position of
    each particle, in terms of each of its coordinates, based on that
    gradient.
    """
    # Initialize some lists. nudgePos and nudgeNeg are used to find the
    # gradient using finite differences.
    output = []
    nudgePos = []
    nudgeNeg = []
    for i in positions:

        # Copying the contents of the positions list to nudgePos and nudgeNeg
        nudgePos.append(vec3d([i.r[0], i.r[1], i.r[2]]))
        nudgeNeg.append(vec3d([i.r[0], i.r[1], i.r[2]]))

    # Loop through each particle, and sequentially nudge the x, y and z coords
    for i, posi in enumerate(positions):
        temp = [0, 0, 0]
        for j in range(3):
            # Change the positions of nudgePos and nudgeNeg
            nudgePos[i].r[j] += factor
            nudgeNeg[i].r[j] -= factor

            # Use nudgePos annd nudgeNeg to find dE/dr
            delta = (potential(nudgePos) - potential(nudgeNeg))/(2*factor)

            # Could have some issues with delta being very large by chance.
            # This prevents that from having too big an impact.
            limit = 1e3
            if(delta > limit):
                delta = limit
            elif(delta < -limit):
                delta = -limit

            # Nudge the coordinate of the particle to be output according to
            # dE/dr in the coordinate being worked on.
            temp[j] = posi.r[j] - (1e-4 * delta)
            nudgePos[i].r[j] -= factor
            nudgeNeg[i].r[j] += factor

        # After calculating the new position on the particle, add it to output.
        output.append(vec3d(list(temp)))
    return output


# Ask the user what they want to do.
# This is not strictly an "arbitrary potetnial", but it does the two types
# of potential specified in the handout. Could change these to be
# asking questions like "polynomial or exponential?", then find number of
# terms, powers and coefficients etc., but even then that is not strictly
# "arbitrary". Not really sure how to make it truly general.
print("How many particles?")
numberOfParticles = int(input())
print("Which potential? (LJ / Morse)")
potentialType = input()
if(potentialType == "Morse"):
    print("Value of r_e/σ? (1 or 2, but can be anything)")
    morseRe = float(input())

# Initialize variable(s)
particlePositions = []

# Generate the particles inital positions. Vaguely puts them randomly on
# a sphere of radius 1.
for i in range(numberOfParticles):
    coordX = (random() - 1)/2
    other = math.sqrt((1 - pow(coordX, 2))/2)
    quadrant = math.floor(random()*4)
    if(quadrant == 0):
        particlePositions.append(vec3d([coordX, other, other]))
    elif(quadrant == 1):
        particlePositions.append(vec3d([coordX, -other, other]))
    elif(quadrant == 2):
        particlePositions.append(vec3d([coordX, other, -other]))
    else:
        particlePositions.append(vec3d([coordX, -other, -other]))

    print(particlePositions[i].r)

print("\n")

# More variables
converged = False
x = []
y = []
z = []
printI = 10000
i = 0

# Nudge the positions of the particles until they are moving by a
# sufficiently small amount each iteration.
while not converged:
    # Nudge according to the correct potential.
    if(potentialType == "LJ"):
        nudgedPos = nudgePositions(particlePositions, 1e-5, potentialLJ)
    elif(potentialType == "Morse"):
        nudgedPos = nudgePositions(particlePositions, 1e-5, potentialMorse)

    # Output something to the user every so often so they know what's going on.
    if(i % (printI/100) == 0):
        difference = 0.0

        # Check if we have converged to a minimum yet
        for j in range(numberOfParticles):
            difference += (particlePositions[j] - nudgedPos[j]).length()
            if(difference < 5e-13):
                converged = True
        print("Progress: " + str(i) + " iterations. Difference: " +
              str(difference/numberOfParticles))

    particlePositions = nudgedPos
    i += 1

# Plot the positions, partly as a sanity check, partly because it looks cool
for i in particlePositions:
    x.append(i.r[0])
    y.append(i.r[1])
    z.append(i.r[2])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z)

plt.show()

# After seeing the plot, user can check if it looks right and save the output
print("Output to XYZ file? (yes/no)")
if(input() == "yes"):
    with open(str(numberOfParticles) + potentialType + ".xyz", "w") as f:
        f.write(str(numberOfParticles) + "\n")
        f.write("Geometry of " + str(numberOfParticles) + " calculated using" +
                " the " + potentialType + " potential. \n")
        for i in particlePositions:
            f.write("X \t" + str(i.r[0]) + "\t" + str(i.r[1]) + "\t" +
                    str(i.r[2]) + "\n")
