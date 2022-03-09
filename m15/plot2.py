import matplotlib.pyplot as plot
import numpy as np
import math

x = []
y = []

x_error = []
y_error = []

x_data_unit = "m"
y_data_unit = "kg"

x_graph_unit = "m"
y_graph_unit = "N"

name = "gewicht-auslenkung"

messwerte = False

with open(name, "r", encoding="utf-8") as file:
    for line in file.readlines():
        temp = line.split(";")
        x.append(float(temp[0].strip("\n").strip(x_data_unit)) - 0.15)
        y.append(float(temp[2].strip("\n").strip(y_data_unit)) * 9.81)
        x_error.append(float(temp[1].strip("\n").strip(x_data_unit)))
        y_error.append(float(temp[3].strip("\n").strip(y_data_unit)) * 9.81)

print(x, y)
print(x_error, y_error)

if messwerte:
    name = name + "_messwerte"

figure = plot.figure(num=name)

axis = plot.axes()

axis.scatter(x, y, label="Datenpunkte")

axis.set_xlabel('d in m')
axis.set_ylabel('F(d) in N')

# axis.set_xlim(0, 15000)
# axis.set_ylim(0, 120)

linear_model = np.polyfit(x, y, 1)
print(str(linear_model))
linear_model_fn = np.poly1d(linear_model)
print(linear_model_fn)
x_s_step = (x[-1] - x[0]) / 100
x_s = np.arange(x[0] - x_s_step * 10, x[-1] + x_s_step * 20, x_s_step)

if not messwerte:
    plot.plot(x_s, linear_model_fn(x_s), color="green", label=f"Steigung: {str(round(float(linear_model[0]), 4))} kg/s²\nY-Abschnitt: {str(round(float(linear_model[1]), 4))} N")

plot.errorbar(x, y, xerr=x_error, yerr=y_error, fmt='o', elinewidth=2)

plot.grid(visible=True)

plot.legend()

plot.savefig(name)

plot.show()
