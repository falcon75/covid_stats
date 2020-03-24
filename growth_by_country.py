import matplotlib.pyplot as plt
import json
import scipy.optimize as opt
import numpy as np
import math


def f(x, a, b, c, d):
    return a / (1. + np.exp(-c * (x - d))) + b


def f_inv(y, a, b, c, d):
    return d - ((np.log(a / (y - b) - 1)) / c)


def confirmed_cases():

    with open('data.json', 'r') as f:
        m = f.read()
        m = json.loads(m)

        data = {}

        for country in m:

            time_series = []

            for data_point in m[country]:

                '''
                # This code subtracts recovered cases.
                
                if data_point["recovered"] is not None:
                    time_series.append(data_point['confirmed'] - data_point['recovered'])
                else:
                    time_series.append(data_point['confirmed'])
                '''

                time_series.append(data_point['confirmed'])

            data[country] = time_series

        return data


def log_plot_cases_adjusted(data, countries):

    data_100 = {}

    for country in countries:

        n_time_series = []
        for dp in data[country]:
            if dp > 100:
                n_time_series.append(dp)

        data_100[country] = n_time_series

    for country in countries:
        plt.semilogy(data_100[country], label=country)

    plt.xlabel('Days since hundredth case')
    plt.ylabel('Number of cases')
    plt.legend()
    plt.show()


def fit_logistic_curve(data, country):

    x = np.linspace(0, len(data[country]) - 1, len(data[country]))
    y = np.array(data[country])

    # Key issue fixed, an inital estimate for the curve allows much more reliable finding
    # I used a one instance of fitting spain, this may have to be changed

    consts, a = opt.curve_fit(f, x, y, p0=(-72223,  72151, -0.260743, 62.356))

    return consts


def plot_data_model(data, countries, project):

    for country in countries:

        consts = fit_logistic_curve(data, country)
        x = np.linspace(0, len(data[country]) + project - 1, len(data[country]) + project)
        y = f(x, *consts)
        plt.plot(x, data[country])
        plt.plot(x, y, label=country)
    plt.legend()
    plt.show()


def plot_data_model_100(data, countries, project):

    colours = ['g', 'b', 'c', 'm', 'y', 'k']

    for country in countries:

        # Fit logistic curve, return consts in logistic function
        consts = fit_logistic_curve(data, country)

        # Calculate and offset to align graphs at the 100th case (make variable)
        off = f_inv(100, *consts)
        c = colours.pop()
        print(country, consts, off)

        # Create time series over which to plot, including a projection into the future
        x_r = np.linspace(0, len(data[country]) - 1, len(data[country]))
        x = np.linspace(0, len(data[country]) + project, len(data[country]) + project + 1)

        # Plot, inc the offset
        y = f(x + off, *consts)
        plt.plot(x, y, (c + '--'))
        plt.plot(x_r - off, data[country], (c + '-'), label=country)

    # Plot China
    data_set = data["China"]
    plt.plot(np.linspace(0, len(data_set) - 1, len(data_set)) + 5, data_set, 'r-',label='China')

    # Plot Formatting
    plt.ylim(90, 200000)
    plt.xlim(-1, 60)
    plt.xlabel('Days since hundredth case')
    plt.ylabel('Number of cases')
    plt.legend()
    plt.show()


countries_to_plot = ['Spain', 'Italy', 'Germany', 'Japan', 'United Kingdom', 'US']

data = confirmed_cases()

plot_data_model_100(data, countries_to_plot, 30)
