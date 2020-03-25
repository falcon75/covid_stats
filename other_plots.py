import matplotlib.pyplot as plt
import numpy as np
import data_processing as dp


# Plot the cases for some countries roughly aligned to the hundredth case.

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


# Plots countries model and actual data with a projection

def plot_data_model(data, countries, project):

    for country in countries:

        consts, _ = dp.fit_logistic_curve(data, country)
        x = np.linspace(0, len(data[country]) + project - 1, len(data[country]) + project)
        y = dp.f(x, *consts)
        plt.plot(x, data[country])
        plt.plot(x, y, label=country)
    plt.legend()
    plt.show()
