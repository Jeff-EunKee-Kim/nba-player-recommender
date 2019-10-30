import numpy
import math
import heapq

# input = (team_name, n)
# team_name = name of team that we want to recommend players for
# n = number of players to be recommended 

# data will be in dictionary form
# key = player name; value = numpy array of data

def n_nearest_neighbor(dict_of_players, ideal_player, n):
    #dict_of_players = key = player name; value = numpy array of data
    #ideal_player = numpy array representing ideal player's data
    #n = total number of players to recommend
    list = []
    for player in dict_of_players.keys():
        (player, val) = (player, compute_cos_similarity(ideal_player, dict_of_players[player]))
        list.append((player,val))
    sorted(list, key = lambda x: x[1])
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



