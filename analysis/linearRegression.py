import numpy as np
import matplotlib.pyplot as plt
import types
from scipy import stats

team_1415 = np.genfromtxt('1415team.csv', delimiter=',',
                          encoding='utf-8', dtype=None)
player_1415 = np.genfromtxt(
    '1415player.csv', delimiter=',', encoding='utf-8', dtype=None)
team_1516 = np.genfromtxt('1516team.csv', delimiter=',',
                          encoding='utf-8', dtype=None)
player_1516 = np.genfromtxt(
    '1516player.csv', delimiter=',', encoding='utf-8', dtype=None)
team_1617 = np.genfromtxt('1617team.csv', delimiter=',',
                          encoding='utf-8', dtype=None)
player_1617 = np.genfromtxt(
    '1617player.csv', delimiter=',', encoding='utf-8', dtype=None)
team_1718 = np.genfromtxt('1718team.csv', delimiter=',',
                          encoding='utf-8', dtype=None)
player_1718 = np.genfromtxt(
    '1718player.csv', delimiter=',', encoding='utf-8', dtype=None)
team_1819 = np.genfromtxt('1819team.csv', delimiter=',',
                          encoding='utf-8', dtype=None)
player_1819 = np.genfromtxt(
    '1819player.csv', delimiter=',', encoding='utf-8', dtype=None)


def makeVar(wp, per):
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

    return teamWp, teamPerAverage


def plot_regression_line(x, y, slope, intercept):
    plt.scatter(x, y, color="m",
                marker="o", s=30)

    y_pred = intercept + slope*x

    plt.plot(x, y_pred, color="g")

    plt.xlabel('Team PER Average')
    plt.ylabel('Winning Percentage')

    plt.show()


teamWp1, teamPerAverage1 = makeVar(team_1415, player_1415)
teamWp2, teamPerAverage2 = makeVar(team_1516, player_1516)
teamWp3, teamPerAverage3 = makeVar(team_1617, player_1617)
teamWp4, teamPerAverage4 = makeVar(team_1718, player_1718)
teamWp5, teamPerAverage5 = makeVar(team_1819, player_1819)

teamWp = []

for i in teamWp1:
    teamWp.append(i)
for i in teamWp2:
    teamWp.append(i)
for i in teamWp3:
    teamWp.append(i)
for i in teamWp4:
    teamWp.append(i)
for i in teamWp5:
    teamWp.append(i)

teamPerAverage = []

for i in teamPerAverage1:
    teamPerAverage.append(i)
for i in teamPerAverage2:
    teamPerAverage.append(i)
for i in teamPerAverage3:
    teamPerAverage.append(i)
for i in teamPerAverage4:
    teamPerAverage.append(i)
for i in teamPerAverage5:
    teamPerAverage.append(i)

print(len(teamWp))
print(len(teamPerAverage))
teamWp = np.array(teamWp)
teamPerAverage = np.array(teamPerAverage)
slope, intercept, r_value, p_value, std_err = stats.linregress(
    teamPerAverage, teamWp)

print("Slope: %f, intercept: %f, r_value: %f" % (slope, intercept, r_value))
plot_regression_line(teamPerAverage, teamWp, slope, intercept)
