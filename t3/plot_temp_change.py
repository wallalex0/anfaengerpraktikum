import matplotlib.pyplot as plot
import numpy as np
from lmfit import Model


def linear_fit(x, m, c):
    return m * x + c


# files = ["temp_teilversuch_1", "temp1_1", "temp1_2"]
# files = ["temp_teilversuch_2_blei", "temp2_blei_1", "temp2_blei_2"]
# files = ["temp_teilversuch_2_glas", "temp2_glas_1", "temp2_glas_2"]
# files = ["temp_teilversuch_2_kupfer", "temp2_kupfer_1", "temp2_kupfer_2"]
files = ["temp_teilversuch_4", "temp4_1", "temp4_3", "temp4_2"]

names = ["Vorkurve", "Nachkurve", "Mischvorgang"]

x_data_unit = "s"
y_data_unit = "°C"

x_graph_unit = "s"
y_graph_unit = "°C"

figure = plot.figure(num=files[0])

axis = plot.axes()

axis.set_xlabel('t in s')
axis.set_ylabel('T in °C')


x_1 = []
y_1 = []

x_1_error = []
y_1_error = []

last_point = []

with open(files[1], "r", encoding="utf-8") as file:
    for line in file.readlines():
        temp = line.split(" ")
        x_1.append(float(temp[0].strip(x_data_unit)))
        y_1.append(float(temp[2].strip(y_data_unit)))
        if temp[1] != '':
            x_1_error.append(float(temp[1].strip(x_data_unit)))
        if temp[3] != '':
            y_1_error.append(float(temp[3].strip(y_data_unit)))
        last_point = [float(temp[0]), float(temp[2])]

print("X-Werte:\n", x_1)
print("Y-Werte:\n", y_1)

print("X-Fehler-Werte:\n", x_1_error)
print("Y-Fehler-Werte:\n", y_1_error)

plot.errorbar(x_1, y_1, xerr=x_1_error, yerr=y_1_error, fmt='o', label=names[0], ms=0.5, zorder=100, capsize=2, capthick=0.75, elinewidth=0.75, color="blue")

model = Model(linear_fit)

params = model.make_params(m=0.2421, c=0.0017)

out = model.fit(y_1, params, x=x_1)

linear_model_1 = np.poly1d([out.params['m'].value, out.params['c'].value])

print('-------------------------------')
print('Parameter     Wert       Fehler')
for name, param in out.params.items():
    if param.stderr is not None:
        print(f'{name:7s} {param.value:11.5f} {param.stderr:11.5f}')
    else:
        print(f'{name:7s} {param.value:11.5f} {0.0:11.5f}')
print('-------------------------------')


x_2 = []
y_2 = []

x_2_error = []
y_2_error = []

first_point = []

with open(files[2], "r", encoding="utf-8") as file:
    for line in file.readlines():
        temp = line.split(" ")
        x_2.append(float(temp[0].strip(x_data_unit)))
        y_2.append(float(temp[2].strip(y_data_unit)))
        if temp[1] != '':
            x_2_error.append(float(temp[1].strip(x_data_unit)))
        if temp[3] != '':
            y_2_error.append(float(temp[3].strip(y_data_unit)))
        if not first_point:
            first_point = [float(temp[0]), float(temp[2])]

print("X-Werte:\n", x_2)
print("Y-Werte:\n", y_2)

print("X-Fehler-Werte:\n", x_2_error)
print("Y-Fehler-Werte:\n", y_2_error)

plot.errorbar(x_2, y_2, xerr=x_2_error, yerr=y_2_error, fmt='o', label=names[1], ms=0.5, zorder=100, capsize=2, capthick=0.75, elinewidth=0.75, color="green")

model = Model(linear_fit)

params = model.make_params(m=0.2421, c=0.0017)

out = model.fit(y_2, params, x=x_2)

linear_model_2 = np.poly1d([out.params['m'].value, out.params['c'].value])

print('-------------------------------')
print('Parameter     Wert       Fehler')
for name, param in out.params.items():
    if param.stderr is not None:
        print(f'{name:7s} {param.value:11.5f} {param.stderr:11.5f}')
    else:
        print(f'{name:7s} {param.value:11.5f} {0.0:11.5f}')
print('-------------------------------')

if len(files) == 4:
    x_3 = []
    y_3 = []

    x_3_error = []
    y_3_error = []
    with open(files[3], "r", encoding="utf-8") as file:
        for line in file.readlines():
            temp = line.split(" ")
            x_3.append(float(temp[0].strip(x_data_unit)))
            y_3.append(float(temp[2].strip(y_data_unit)))
            if temp[1] != '':
                x_3_error.append(float(temp[1].strip(x_data_unit)))
            if temp[3] != '':
                y_3_error.append(float(temp[3].strip(y_data_unit)))

    print("X-Werte:\n", x_3)
    print("Y-Werte:\n", y_3)

    print("X-Fehler-Werte:\n", x_3_error)
    print("Y-Fehler-Werte:\n", y_3_error)

    plot.errorbar(x_3, y_3, xerr=x_3_error, yerr=y_3_error, fmt='o', label=names[2], ms=0.5, zorder=100, capsize=2, capthick=0.75, elinewidth=0.75, color="purple")


extra_point = last_point[0] + (first_point[0] - last_point[0]) / 2


x_s_step = (x_1[-1] - x_1[0]) / 100
x_s_1 = np.arange(x_1[0] - x_s_step * 20, extra_point, x_s_step)
plot.plot(x_s_1, linear_model_1(x_s_1), color="blue")

x_s_step = (x_2[-1] - x_2[0]) / 100
x_s_2 = np.arange(extra_point, x_2[-1] + x_s_step * 20, x_s_step)
plot.plot(x_s_2, linear_model_2(x_s_2), color="green")


t_1 = linear_model_1(extra_point)
print(f"T1: {t_1:11.5f}")
t_n = linear_model_2(extra_point)
print(f"Tn: {t_n:11.5f}")


plot.hlines(t_1, last_point[0], x_s_2[-1], label=f"T1", linestyle="--", color='red', zorder=-1)
plot.hlines(t_n, 0, first_point[0], label=f"Tn", linestyle="--", color='orange', zorder=-1)
plot.vlines(extra_point, t_n, t_1, color='black', linestyle='--')
plot.plot([last_point[0], first_point[0]], [last_point[1], first_point[1]], 'black', marker='', label=f"Extrapolation")

plot.grid(visible=True)

plot.legend()

plot.savefig(files[0])

plot.show()
