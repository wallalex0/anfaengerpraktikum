import matplotlib.pyplot as plot
import numpy as np


x = []
y = []

name = "torsion2"

messwerte = False

with open(name, "r", encoding="utf-8") as file:
    for line in file.readlines():
        temp = line.split(";")
        x.append(float(temp[0].strip("mm"))**2)
        y.append(float(temp[1].strip("\n").strip("s"))**2)

print(x, y)

if messwerte:
    name = name + "_messwerte"

figure = plot.figure(num=name)

axis = plot.axes()

axis.scatter(x, y, label="Schwingungsdauer gegen Abstand")

axis.set_xlabel('d² in mm')
axis.set_ylabel('T²(d) in s')

# axis.set_xlim(0, 15000)
# axis.set_ylim(0, 120)

linear_model = np.polyfit(x, y, 1)
print(linear_model)
linear_model_fn = np.poly1d(linear_model)
print(linear_model_fn)
x_s = np.arange(0, x[-1]+1)
if not messwerte:
    plot.plot(x_s, linear_model_fn(x_s), color="green", label=f"Steigung: {str(round(float(linear_model[0]), 4))} s/mm")

plot.grid(visible=True)

plot.legend()

plot.savefig(name)

plot.show()
