import numpy as np
import matplotlib.pyplot as plt
import types
from scipy import stats

team_1819 = np.genfromtxt('1819team.csv', delimiter=',',
                   encoding='utf-8', dtype=None)
player_1819 = np.genfromtxt('1819player.csv', delimiter=',', encoding='utf-8', dtype=None)

teamPER = {}
for line in player_1819:
    teams = line[1].split("/")
    for team in teams:
        if team in teamPER:
            teamPER[team].append(line[2])
        else:
            teamPER[team] = []
            teamPER[team].append(line[2])

# for all teams
for team in teamPER:
    # withoutStarting = teamPER[team]
    withoutStarting = teamPER[team][5:]
    print("%s without 5 starting: " % (team))
    print(withoutStarting)
    print("Average: %f" % (np.average(withoutStarting)))
    print()

# for specific team
teamOfInterest = "POR"
without5 = teamPER[teamOfInterest][5:]

# print("%s without 5 starting: " % (teamOfInterest))
# print(without5)
# print("Average: %f" % (np.average(without5)))
# print()
