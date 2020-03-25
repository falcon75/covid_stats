import matplotlib.pyplot as plt
import data_processing as dp
import numpy as np


# Main plot, logarithmic with projected growth curves based on fitting logistic regression

def plot_data_model_100(data, countries, project):

    colours = ['g', 'b', 'c', 'm', 'y', 'k']

    for country in countries:

        # Fit logistic curve, return consts in logistic function
        consts, cov = dp.fit_logistic_curve(data, country)

        # Calculate and offset to align graphs at the 100th case (make variable)
        off = dp.f_inv(100, *consts)
        c = colours.pop()
        print(country, consts, off)

        m = len(data[country])

        # Create time series over which to plot, including a projection into the future
        x_r = np.linspace(0, m - 1, m)
        x = np.linspace(0, m + project, m + project + 1)

        y = dp.f(x, *consts)

        # Plot, inc the offset
        plt.plot((x - off)[(m-2):], y[(m-2):], (c + '--'))
        plt.plot(x_r - off, data[country], (c + '-'), label=country) # + str(np.sqrt(np.diag(cov)))))
        plt.plot((x_r - off)[-1], data[country][-1], (c + 'o'))

    # Plot China
    off_c = 5
    data_set = data["China"]
    plt.plot(np.linspace(0, len(data_set) - 1, len(data_set)) + off_c, data_set, 'r-',label='China')
    plt.plot(len(data_set) + off_c - 1, data_set[-1], 'ro')

    # Plot Formatting
    plt.ylim(90, 200000)
    plt.xlim(-1, 70)
    plt.xlabel('Days since hundredth case')
    plt.ylabel('Number of cases')
    plt.yscale('log')
    plt.title("Cases over time for COVID19, dashed line - logistic regression fit")
    plt.legend()
    plt.show()


countries_to_plot = ['Spain', 'Italy', 'Germany', 'Japan', 'United Kingdom', 'US']

data = dp.confirmed_cases()

plot_data_model_100(data, countries_to_plot, 30)
