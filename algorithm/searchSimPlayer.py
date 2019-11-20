import csv
import numpy
import math
import heapq
import operator

# get the categories
def openCSV():
    filename = '../general_stats.csv'

    # Getting all of the resident rankings
    with open(filename) as file:
        linereader = csv.reader(file)

        # get categories
        cats = next(linereader)
        categories = []
        for i in cats:
            new = i.replace(' ', '')
            categories.append(new)

        # stats we are looking for
        # looking_for_stats = ['AST_PCT', 'AST_TO', 'OREB_PCT',
        #                      'DREB_PCT', 'TM_TOV_PCT', 'EFG_PCT', 'TS_PCT', 'PACE']
        looking_for_stats = ['AGE', 'FG_PCT', 'FG3_PCT','FT_PCT','REB', 'AST','TOV','STL','BLK']

        # get category indeces that we want
        want_categories = []
        # for i in range(len(categories)):
        #     if categories[i] in looking_for_stats:
        #         want_categories.append(i)

        for i in looking_for_stats:
            if i in categories:
                want_categories.append(categories.index(i))


        # Create dict to hold total score for each category, then can find averages
        # create dict to hold output of average stats
        total_stats = dict()
        avg_stats = dict()

        for i in want_categories:
            total_stats[i] = 0.0
            avg_stats[i] = 0.0

        # number of teams
        num_teams = 0

        # stats for each team
        eachteam_stats = dict()

        # add up all scores from each team
        for line in linereader:
            num_teams += 1
            for i in want_categories:
                total_stats[i] += float(line[i])
            eachteam_stats[line[1]] = line

        eachteam_stats_out = dict()
        for i in eachteam_stats:
            eachteam_stats_out[formatName(i)] = eachteam_stats[i]

        # convert all sums to averages
        for stat in total_stats:
            avg_stats[stat] = total_stats[stat] / num_teams

        return avg_stats, eachteam_stats_out, categories

# get the IDs of all the teams
def getTeamIDs(eachteam_stats):
    # maps team ID to name of team
    team_id_dict = dict()

    for i in eachteam_stats:
        team_id_dict[eachteam_stats[i][0]] = i

    return team_id_dict

# get the stats of the player you are searching for
def getTargetStats(player, categories, avg_dict):

    # Get target stats for ideal player
    target_stats = dict()

    # get dictionary of players
    playerDict = getPlayerDict()

    # find stats for the query player
    queryPlayer = playerDict[player]

    # find corresponding stats for the query player
    for cat in avg_dict:
        target_stats[categories[cat]] = float(queryPlayer[cat])

    # print(target_stats)

    # look through
    return target_stats, playerDict

# get a dictionary with all the players and their stats
def getPlayerDict():

    playerDict = dict()

    filename = '../advanced_players.csv'

    # Getting all of the players
    with open(filename) as file:
        linereader = csv.reader(file)

        # get categories
        cats = next(linereader)
        categories = []
        for i in cats:
            new = i.replace(' ', '')
            categories.append(new)

        # get each player
        for line in linereader:
            playerDict[line[1]] = line

        return playerDict

# format the team, so case and spaces don't matter
def formatName(team):
    formatted_team = team.replace(' ', '')
    return formatted_team.lower()

# find the most similar players to one specific player
def closestPlayers(target_stats, playerDict, avg_dict, team_id, categories, n, my_player):
    # the closest players to the specified person
    closest_players = []

    # get similarities of everyone
    simDict = dict()

    # stats we want to compare
    statCategories = avg_dict.keys()

    # turn target_stats into array so can dot product it
    targetStats = []
    for stat in statCategories:
        targetStats.append(target_stats[categories[stat]])

    # look through all players
    for player in playerDict:
        # only check players not on the team of person searching
        if int(playerDict[player][2]) != team_id:
            # look through stats we want to compare
            compStats = []
            for stat in statCategories:
                # print(playerDict[player][stat])
                compStats.append(float(playerDict[player][stat]))

            simDict[player] = float(
                compute_cos_similarity(compStats, targetStats))

    # simDict = sorted(simDict, key=lambda x: x[1])
    sorted_simDict = sorted(simDict.items(), key=operator.itemgetter(1))

    # closest players
    closest_players = []

    # exclude query player
    topPlayer = list(reversed(list(sorted_simDict)))[0][0]
    skip = 0
    if my_player == topPlayer:
        skip = 1

    for x in list(reversed(list(sorted_simDict)))[0+skip:n+skip]:
        closest_players.append(x)

    return closest_players

# find cosine similarity between two vectors
def compute_cos_similarity(point1, point2):
    numerator = numpy.dot(point1, point2)
    denominator = float(math.sqrt(numpy.dot(point1, point1))) * \
        float(math.sqrt(numpy.dot(point2, point2)))
    if denominator == 0:
        return 0
    return float(numerator)/float(denominator)

# get ID of the team you are on, so you don't get players on your team in the search
def getTeamID(my_team, team_id_dict):
    my_team_name = formatName(my_team)
    team_id = 0
    for team in team_id_dict.keys():
        if team_id_dict[team] == my_team_name:
            team_id = int(team)
            break

    return team_id


# Run Code below
if __name__ == '__main__':

    ######### Query #########
    my_team = "torontoraptors"
    n = 8
    player = "Stephen Curry"
    ######### Query #########

    # get average stats
    avg_dict, eachteam_stats, categories = openCSV()

    # get team id's
    team_id_dict = getTeamIDs(eachteam_stats)

    # get target stats for ideal player
    target_stats, playerDict = getTargetStats(player, categories, avg_dict)

    # get the team_id of the team that wants recommendations
    team_id = getTeamID(my_team, team_id_dict)

    closestPlayers = closestPlayers(target_stats, playerDict, avg_dict, team_id, categories, n, player)

    print("Most similar players to %s:" % player)
    count = 1
    for player in closestPlayers:
        print("%d: %s" %(count,player[0]))
        count += 1
    print('')
