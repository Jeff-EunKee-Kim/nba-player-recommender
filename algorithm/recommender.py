import numpy
import math
import heapq

# input = (team_name, n)
# team_name = name of team that we want to recommend players for
# n = number of players to be recommended 

# data will be in dictionary form
# key = player name; value = numpy array of data

def read_data_file(filename):
    file = open(filename)
    first_line = ("".join(file.readline().strip("\n"))).split(",")
    player_name = first_line.index("PLAYER_NAME")
    team_id = first_line.index("TEAM_ID")
    stats = ["AST_PCT", "AST_TO", "OREB_PCT", "DREB_PCT", "TM_TOV_PCT", "EFG_PCT", "TS_PCT", "PACE"]
    indices_of_stats = []
    for stat in stats:
        indices_of_stats.append(first_line.index(stat))
    dict_of_players = {}
    for line in file:
        newline = ("".join(line.strip("\n"))).split(",")
        stats_list = []
        for id in indices_of_stats:
            stats_list.append(float(newline[id]))
        dict_of_players[(newline[player_name], int(newline[team_id]))] = numpy.asarray(stats_list)
    return dict_of_players


def n_nearest_neighbor(dict_of_players, ideal_player, team_id, n):
    list = []
    for (person, person_team_id) in dict_of_players.keys():
        if team_id != person_team_id:
            (player, val) = (person, compute_cos_similarity(ideal_player, dict_of_players[(person, person_team_id)]))
            list.append((player,val))    
    list = sorted(list, key = lambda x: x[1])
    list.reverse()
    recommended_players = []
    for i in range(n):
        recommended_players.append(list[i][0])
    return recommended_players

def compute_cos_similarity(point1, point2):
    numerator = numpy.dot(point1, point2)
    denominator = math.sqrt(numpy.dot(point1, point1)) * math.sqrt(numpy.dot(point2, point2))
    return float(numerator)/float(denominator)

### Run Stuff Below
dict_of_players = read_data_file("advanced_players.csv")
n = 6
players = n_nearest_neighbor(dict_of_players, dict_of_players[("Alfonzo McKinnie", 1610612744)], 1610612744, n)
# Get the team name from the team id in the advanced.csv file
print ("The top " + str(n) + " recommended players for " + "INSERT TEAM NAME HERE" + " are: " + str(players))





