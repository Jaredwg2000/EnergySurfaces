# EnergySurfaces
Finds a potential energy minimum for a set of n particles

The user specifies a number of particles n; the type of potential (either Leonard-Jones or Morse - designing the input
for a truly arbitrary potential seems difficult); and the value of r_e/sigma for the Morse potential.

The program runs until the changes being made are small enough that it could be considered converged.

The program then produces a plot of the final positions of the particles, and the user can save the output to a .xyz file.

It takes a while to run as it is not particularly well optimized as far as I know (particularly for Morse potentials), but it does run and come to reasonable solutions.
As such, I coded a file to read the outputs from the program (XYZReader.py). The xyz files in the repository are the outputs for the different potentials
(LJ, Morse with r_e/sigma = 1 and 2) for n = 7. Running the main program for smaller values of n is less painfully slow.
