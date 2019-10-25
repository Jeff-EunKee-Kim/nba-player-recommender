import numpy
import math
import heapq

# input = (team_name, n)
# team_name = name of team that we want to recommend players for
# n = number of players to be recommended

def compute_cos_similarity(point1, point2):
    numerator = numpy.dot(point1, point2)
    denominator = math.sqrt(numpy.dot(point1, point1)) * math.sqrt(numpy.dot(point2, point2))
    return float(numerator)/float(denominator)

