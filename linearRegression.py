import numpy as np
import matplotlib.pyplot as plt

my_data = np.genfromtxt('advanced.csv', delimiter=',', dtype=None)

# print(my_data)
teamWP = np.array([0.5, 0.62, 0.69, 0.55, 0.8])
teamPER = np.array([20.2, 23.4, 24.1, 21.9, 30.5])

# teamWP.append(0.50)
# teamWP.append(0.62)
# teamWP.append(0.69)
# teamWP.append(0.55)
# teamWP.append(0.80)

# teampPER.append(20.2)
# teampPER.append(23)
# teampPER.append(24)
# teampPER.append(21)
# teampPER.append(30)


def estimate_coef(x, y):
    # number of observations/points
    n = np.size(x)

    # mean of x and y vector
    m_x, m_y = np.mean(x), np.mean(y)

    # calculating cross-deviation and deviation about x
    SS_xy = np.sum(y*x) - n*m_y*m_x
    SS_xx = np.sum(x*x) - n*m_x*m_x

    # calculating regression coefficients
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1*m_x

    return(b_0, b_1)


def plot_regression_line(x, y, b):
    # plotting the actual points as scatter plot
    plt.scatter(x, y, color="m",
                marker="o", s=30)

    # predicted response vector
    y_pred = b[0] + b[1]*x

    # plotting the regression line
    plt.plot(x, y_pred, color="g")

    # putting labels
    plt.xlabel('x')
    plt.ylabel('y')

    # function to show plot
    plt.show()

b = estimate_coef(teamWP, teamPER) 
print("Estimated coefficients:\nb_0 = {}  \nb_1 = {}".format(b[0], b[1])) 

# plotting regression line 
plot_regression_line(teamWP, teamPER, b)