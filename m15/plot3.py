import matplotlib.pyplot as plot
import numpy as np
import math

x_data_unit = ""
y_data_unit = ""

x_graph_unit = "m²"
y_graph_unit = ""

messwerte = False

files = ["kappa1", "kappa2", "kappa3"]

names = ["κ 1,2 ", "κ Theorie", "κ +,-"]

file_name = ""
for name in files:
    if files.index(name) == 0:
        file_name += name
    else:
        file_name += "-" + name

file_name = file_name.lower()

figure = plot.figure(num=file_name)

axis = plot.axes()

axis.set_xlabel('z² in m²')
axis.set_ylabel('K')

for name in files:
    x = []
    y = []

    x_error = []
    y_error = []

    with open(name, "r", encoding="utf-8") as file:
        for line in file.readlines():
            temp = line.split(";")
            x.append(float(temp[0].strip(x_data_unit))**2)
            y.append(float(temp[2].strip(y_data_unit)))
            if temp[1] != '':
                x_error.append(float(temp[1].strip(x_data_unit))**2)
            if temp[3] != '':
                y_error.append(float(temp[3].strip(y_data_unit)))

    print("X-Werte:\n", x)
    print("Y-Werte:\n", y)
    print("X-Fehler-Werte:\n", x_error)
    print("Y-Fehler-Werte:\n", y_error)

    if messwerte:
        name = name + "_messwerte"

    axis.scatter(x, y, label=names[files.index(name)])

    if not messwerte:
        linear_model = np.polyfit(x, y, 1)

        linear_model_fn = np.poly1d(linear_model)
        print("Gerade:", linear_model_fn)

        x_s_step = (x[-1] - x[0]) / 100
        x_s = np.arange(x[0] - x_s_step * 10, x[-1] + x_s_step * 20, x_s_step)

        # label = ""
        # if x_graph_unit == '' and y_graph_unit == '':
        #     label = f"Steigung: {str(round(float(linear_model[0]), 4))}\nY-Abschnitt: {str(round(float(linear_model[1]), 4))}"
        # elif x_graph_unit != '' and y_graph_unit != '':
        #     label = f"Steigung: {str(round(float(linear_model[0]), 4))}{y_graph_unit}/{x_graph_unit}\nY-Abschnitt: {str(round(float(linear_model[1]), 4))}{y_graph_unit}"
        # elif y_graph_unit == '':
        #     label = f"Steigung: {str(round(float(linear_model[0]), 4))} 1/{x_graph_unit}\nY-Abschnitt: {str(round(float(linear_model[1]), 4))}"
        # elif x_graph_unit == '':
        label = f"Steigung: {str(round(float(linear_model[0]), 4))}\nY-Abschnitt: {str(round(float(linear_model[1]), 4))}"

        plot.plot(x_s, linear_model_fn(x_s), label=label)

    if x_error or y_error:
        plot.errorbar(x, y, xerr=x_error, yerr=y_error, fmt='o', elinewidth=2)

plot.grid(visible=True)

plot.legend()

plot.savefig(file_name)

plot.show()
