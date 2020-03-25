import json
import scipy.optimize as opt
import numpy as np


# Logistic curve and inverse functions for fitting

def f(x, a, b, c, d):
    return a / (1. + np.exp(-c * (x - d))) + b


def f_inv(y, a, b, c, d):
    return d - ((np.log(a / (y - b) - 1)) / c)


# Read the local data file to obtain number of confirmed cases by country

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


def fit_logistic_curve(data, country):
    x = np.linspace(0, len(data[country]) - 1, len(data[country]))
    y = np.array(data[country])

    # Key issue fixed, an inital estimate for the curve allows much more reliable finding
    # I used a one instance of fitting spain, this may have to be changed

    consts, cov = opt.curve_fit(f, x, y, p0=(-72223, 72151, -0.260743, 62.356))

    return consts, cov
