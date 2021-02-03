"""Take a .xyz file, comprehend it and plot it."""
import matplotlib.pyplot as plt

print("Path:")

path = input()

x = []
y = []
z = []

with open(path, "r") as f:
    for line in f:
        linesplit = line.split()
        if(linesplit[0] == "X"):
            x.append(float(linesplit[1]))
            y.append(float(linesplit[2]))
            z.append(float(linesplit[3]))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z)

plt.show()
