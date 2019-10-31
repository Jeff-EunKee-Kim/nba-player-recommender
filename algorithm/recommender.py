import numpy
import math
import heapq

# ideal player will be a dictionary
# key = name of statistic
# value = numerical value of statistic

def read_data_file(filename, ideal_player_dict):
    # key = title of statistic
    # value = numerical value of statistic
    file = open(filename)
    first_line = ("".join(file.readline().strip("\n"))).split(",")
    player_name = first_line.index("PLAYER_NAME")
    team_id = first_line.index("TEAM_ID")
    # create the ideal player using dict
    ideal_player = []
    stats = ideal_player_dict.keys()
    #stats = ["AST_PCT", "AST_TO", "OREB_PCT", "DREB_PCT", "TM_TOV_PCT", "EFG_PCT", "TS_PCT", "PACE"]
    for stat in stats:
        ideal_player.append(ideal_player_dict[stat])
    ideal_player_array = numpy.asarray(ideal_player)
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
    return (dict_of_players, ideal_player_array)


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
(dict_of_players, ideal_player_array) = read_data_file("advanced_players.csv")
n = 6
players = n_nearest_neighbor(dict_of_players, ideal_player_array, 1610612744, n)
# Get the team name from the team id in the advanced.csv file
print ("The top " + str(n) + " recommended players for " + "INSERT TEAM NAME HERE" + " are: " + str(players))
