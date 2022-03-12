import matplotlib.pyplot as plt
from numpy import exp, loadtxt, pi, sqrt
from lmfit.models import LinearModel, StepModel, Model
import numpy as np

names = ['testtemp1_1', 'testtemp1_2']

for name in names:
    data = loadtxt(name)
    x = data[:, 0]
    x_error = data[:, 1]
    y = data[:, 2]
    y_error = data[:, 3]


    def linear_fit(x, m, c):
        return m * x + c


    model = Model(linear_fit)

    params = model.make_params(m=0.2421, c=0.0017)

    out = model.fit(y, params, x=x)

    print(out.fit_report())

    # dely = result.eval_uncertainty()
    # plt.fill_between(x, result.best_fit-dely, result.best_fit+dely, color="#ABABAB")

    plt.plot(x, y)
    plt.plot(x, out.best_fit, '-', label='best fit')
plt.legend()
plt.show()
