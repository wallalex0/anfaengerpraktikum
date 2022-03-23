import math
import matplotlib.pyplot as plot
import numpy as np
from scipy.optimize import curve_fit
from lmfit import models


files = ["teilversuch-2-c-tiefpass", "teilversuch-2-c-tiefpass"]
# files = ["teilversuch-2-c-hochpass", "teilversuch-2-c-hochpass"]
# files = ["teilversuch-2-c-bandpass", "teilversuch-2-c-bandpass-1", "teilversuch-2-c-bandpass-2"]

x_data_unit = "Hz"
y_data_unit = "V"

x_graph_unit = "Hz"
y_graph_unit = ""

figure = plot.figure(num=files[0])

axis = plot.axes()

axis.set_xlabel(f'f in {x_graph_unit}')
axis.set_ylabel(f'Ua/Ue in {y_graph_unit}')


x = []
y = []
x_error = []
y_error = []

with open(files[1], "r", encoding="utf-8") as file:
    for line in file.readlines():
        temp = line.split(" ")
        x.append(float(temp[0].strip(x_data_unit)))
        y.append(float(temp[4].strip(y_data_unit)) / float(temp[2].strip(y_data_unit)))
        if temp[1] != '':
            x_error.append(float(temp[1].strip(x_data_unit)))
        if temp[3] != '':
            y_error.append(math.sqrt((1 / float(temp[2].strip(y_data_unit)) * float(temp[5].strip(y_data_unit))) ** 2 + ((-float(temp[4].strip(y_data_unit)) / (float(temp[2].strip(y_data_unit)) ** 2)) * float(temp[3].strip(y_data_unit))) ** 2))

if len(files) == 3:
    with open(files[2], "r", encoding="utf-8") as file:
        for line in file.readlines():
            temp = line.split(" ")
            x.append(float(temp[0].strip(x_data_unit)))
            y.append(float(temp[4].strip(y_data_unit)) / float(temp[2].strip(y_data_unit)))
            if temp[1] != '':
                x_error.append(float(temp[1].strip(x_data_unit)))
            if temp[3] != '':
                y_error.append(math.sqrt((1 / float(temp[2].strip(y_data_unit)) * float(temp[5].strip(y_data_unit))) ** 2 + ((-float(temp[4].strip(y_data_unit)) / (float(temp[2].strip(y_data_unit)) ** 2)) * float(temp[3].strip(y_data_unit))) ** 2))


x, y = zip(*sorted(zip(x, y)))
x = np.array(x)
y = np.array(y)
x_error = np.array(x_error)
y_error = np.array(y_error)


axis.semilogx(x, np.exp(-x / 5.0), visible=False)

print("X-Werte:\n", x)
print("Y-Werte:\n", y)

print("X-Fehler-Werte:\n", x_error)
print("Y-Fehler-Werte:\n", y_error)

plot.errorbar(x, y, xerr=x_error, yerr=y_error, fmt='o', label='Messpunkte', ms=0.5, zorder=100, capsize=2, capthick=0.75, elinewidth=0.75, color="blue")

model = models.LognormalModel()

params = model.guess(y, x=x)
# params = model.make_params(amplitude=1, center=0.0, sigma=0.25, height=1.65, fwhm=0.56)

out = model.fit(y, params, x=x, weights=y_error)

print('-------------------------------')
print('Guess Values')
print('Parameter      Value       Stderr')
for name, param in params.items():
    if param.stderr is not None:
        print(f'{name:9s} {param.value:11.5f} {param.stderr:11.5f}')
    else:
        print(f'{name:9s} {param.value:11.5f} {0.0:11.5f}')
print('-------------------------------')
print('Functions Values')
print('Parameter      Value       Stderr')
for name, param in out.params.items():
    if param.stderr is not None:
        print(f'{name:9s} {param.value:11.5f} {param.stderr:11.5f}')
    else:
        print(f'{name:9s} {param.value:11.5f} {0.0:11.5f}')
print('-------------------------------')

filter_pass = [154.9, 158.7, 178.2, 1516]

if files[0].endswith("tiefpass"):
    plot.hlines(1/math.sqrt(2), 0, filter_pass[0], linestyle="--", color='orange', label="1/sqrt(2)")
    plot.vlines(filter_pass[0], 0, 1/math.sqrt(2), linestyle='--', color='red', label="fg")
elif files[0].endswith("hochpass"):
    plot.hlines(1/math.sqrt(2), 0, filter_pass[1], linestyle="--", color='orange', label="1/sqrt(2)")
    plot.vlines(filter_pass[1], 0, 1/math.sqrt(2), linestyle='--', color='red', label="fg")
elif files[0].endswith("bandpass"):
    plot.hlines(1/math.sqrt(2), 0, filter_pass[2], linestyle="--", color='orange', label="1/sqrt(2)")
    plot.vlines(filter_pass[2], 0, 1/math.sqrt(2), linestyle='--', color='red', label="fg1")

    plot.hlines(1/math.sqrt(2), filter_pass[3], x[-1], linestyle="--", color='orange')
    plot.vlines(filter_pass[3], 0, 1/math.sqrt(2), linestyle='--', color='darkred', label="fg2")

x_s = np.arange(x[0], x[-1], (x[-1] - x[0]) / 100)

# plot.plot(x, out.best_fit)
# plot.plot(x, out.init_fit)

plot.grid(visible=True)

plot.legend()

plot.savefig(files[0])

plot.show()
