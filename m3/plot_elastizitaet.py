import matplotlib.pyplot as plot
import numpy as np


files = ["Stab_3"]
# files = ["Stab_1", "Stab_2", "Stab_3"]

file_name = ""

for name in files:
    if files.index(name) == 0:
        file_name += name
    else:
        file_name += "-" + name

file_name = file_name.lower()

figure = plot.figure(num=file_name)

axis = plot.axes()

for name in files:
    x = []
    y = []
    with open(name, "r", encoding="utf-8") as file:
        for line in file.readlines():
            temp = line.split(";")
            x.append(float(temp[0].strip("N")))
            y.append(float(temp[1].strip("\n").strip("mm")))

    print(x, y)

    axis.scatter(x, y, label=name.replace("_", " "))

    axis.set_xlim(0, 35)
    axis.set_ylim(0, 4)

    axis.set_xlabel('F in N')
    axis.set_ylabel('s(F) in mm')

    linear_model = np.polyfit(x, y, 1)
    print(linear_model)
    linear_model_fn = np.poly1d(linear_model)
    print(linear_model_fn)
    x_s = np.arange(x[0]-1, x[-1]+1)
    # Plot linear fit
    if len(files) == 1:
        plot.plot(x_s, linear_model_fn(x_s), label=f"Steigung: {str(round(float(linear_model[0]), 4))} mm/N")

    # plot.errorbar(x, y, xerr=0.5, yerr=0.05, label='test')

plot.grid(visible=True)

plot.legend()

plot.savefig(file_name)

plot.show()
