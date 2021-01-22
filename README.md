# EnergySurfaces
Finds a potential energy minimum for a set of n particles

The user specifies a number of particles n; the type of potential (either Leonard-Jones or Morse - designing the input
for a truly arbitrary potential seems difficult); and the value of r_e/sigma for the Morse potential.

The program runs until the changes being made are small enough that it could be considered converged.

The program then produces a plot of the final positions of the particles, and the user can save the output to a .xyz file.

It takes a while to run as it is not particularly well optimized as far as I know, but it does run and come to reasonable solutions.
