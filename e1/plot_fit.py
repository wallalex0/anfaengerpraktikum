import matplotlib.pyplot as plot
import numpy as np
from lmfit import Model


def linear_fit(x, m, c):
    return m * x + c


def non_linear_fit():
    return


files = ["kennline_teilversuch_5", "kennlinie5"]
# files = ["kennline_teilversuch_6_1", "kennlinie6_1"]
# files = ["kennline_teilversuch_6_2", "kennlinie6_2"]

x_data_unit = "mA"
y_data_unit = "V"

x_graph_unit = "mA"
y_graph_unit = "V"

figure = plot.figure(num=files[0])

axis = plot.axes()

axis.set_xlabel(f'I in {x_graph_unit}')
axis.set_ylabel(f'U in {y_graph_unit}')


x = []
y = []

x_error = []
y_error = []

with open(files[1], "r", encoding="utf-8") as file:
    for line in file.readlines():
        temp = line.split(" ")
        x.append(float(temp[0].strip(x_data_unit)))
        y.append(float(temp[2].strip(y_data_unit)))
        if temp[1] != '':
            x_error.append(float(temp[1].strip(x_data_unit)))
        if temp[3] != '':
            y_error.append(float(temp[3].strip(y_data_unit)))

print("X-Werte:\n", x)
print("Y-Werte:\n", y)

print("X-Fehler-Werte:\n", x_error)
print("Y-Fehler-Werte:\n", y_error)

plot.errorbar(x, y, xerr=x_error, yerr=y_error, fmt='o', label='Messpunkte', ms=0.5, zorder=100, capsize=2, capthick=0.75, elinewidth=0.75, color="blue")

model = Model(linear_fit)

params = model.make_params(m=0.2421, c=0.0017)

out = model.fit(y, params, x=x)

linear_model = np.poly1d([out.params['m'].value, out.params['c'].value])

print('-------------------------------')
print('Parameter    Value       Stderr')
for name, param in out.params.items():
    if param.stderr is not None:
        print(f'{name:7s} {param.value:11.5f} {param.stderr:11.5f}')
    else:
        print(f'{name:7s} {param.value:11.5f} {0.0:11.5f}')
print('-------------------------------')

x_s_step = (x[-1] - x[0]) / 100
x_s = np.arange(x[0] - x_s_step * 20, x[-1] + x_s_step * 20, x_s_step)

plot.plot(x_s, linear_model(x_s))


plot.grid(visible=True)

plot.legend()

plot.savefig(files[0])

plot.show()
