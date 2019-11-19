import numpy as np
import matplotlib.pyplot as plt
import types
from scipy import stats

wp = np.genfromtxt('modifiedAdvanced.csv', delimiter=',', encoding='utf-8', dtype=None)
per = np.genfromtxt('nicePER.csv', delimiter=',', encoding='utf-8', dtype=None)


teamPER = {}

for line in per:
    teams = line[1].split("/")
    for team in teams:
        if team in teamPER:
            teamPER[team].append(line[2])
        else:
            teamPER[team] = []
            teamPER[team].append(line[2])
sortedByName = sorted(teamPER)

teamWp = []
teamPerAverage = []
for i in range(30):
    teamWp.append(wp[i][1])
    teamPerAverage.append(np.average(teamPER[sortedByName[i]]))

def plot_regression_line(x, y, slope, intercept):
    plt.scatter(x, y, color="m",
                marker="o", s=30)

    y_pred = intercept + slope*x

    plt.plot(x, y_pred, color="g")

    plt.xlabel('Team PER Average')
    plt.ylabel('Winning Percentage')

    plt.show()

teamWp = np.array(teamWp)
teamPerAverage = np.array(teamPerAverage)
slope, intercept, r_value, p_value, std_err = stats.linregress(teamPerAverage, teamWp)

print("Slope: %f, intercept: %f, r_value: %f" % (slope, intercept, r_value) )
plot_regression_line(teamPerAverage, teamWp, slope, intercept)
