import csv
import numpy
import math
import heapq

# Ideal Player Algorithm below


def openCSV():
    filename = '../advanced.csv'

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
        looking_for_stats = ['AST_PCT', 'AST_TO', 'OREB_PCT',
                             'DREB_PCT', 'TM_TOV_PCT', 'EFG_PCT', 'TS_PCT', 'PACE']

        # get category indeces that we want
        want_categories = []
        for i in range(len(categories)):
            if categories[i] in looking_for_stats:
                want_categories.append(i)

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

        # output dict with string keys, not index keys
        # out = dict()
        # for stat in avg_stats:
        #     str_name = categories[stat]
        #     out[str_name] = avg_stats[stat]

        return avg_stats, eachteam_stats_out, categories


def getTeamIDs(eachteam_stats):
    # maps team ID to name of team
    team_id_dict = dict()

    for i in eachteam_stats:
        team_id_dict[eachteam_stats[i][0]] = i

    return team_id_dict


def getTargetStats(player, categories, avg_dict):

    # Get target stats for ideal player
    target_stats = dict()

    # get dictionary of players
    playerDict = getPlayerDict()

    # find stats for the query player
    queryPlayer = playerDict[player]

    # find corresponding stats for the query player
    for cat in avg_dict:
        # print(categories[cat])
        target_stats[categories[cat]] = float(queryPlayer[cat])

    # print(target_stats)

    # look through 
    return target_stats


def getPlayerDict():

    playerDict = dict()

    filename = '../advanced_players.csv'

    # Getting all of the resident rankings
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


def formatName(team):
    formatted_team = team.replace(' ', '')
    return formatted_team.lower()


# Recommender Algorithm below
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
        dict_of_players[(newline[player_name], int(
            newline[team_id]))] = numpy.asarray(stats_list)
    return (dict_of_players, ideal_player_array)


def n_nearest_neighbor(dict_of_players, ideal_player, team_id, n):
    list = []
    for (person, person_team_id) in dict_of_players.keys():
        if team_id != person_team_id:
            (player, val) = (person, compute_cos_similarity(
                ideal_player, dict_of_players[(person, person_team_id)]))
            list.append((player, val))
    list = sorted(list, key=lambda x: x[1])
    list.reverse()
    recommended_players = []
    for i in range(n):
        recommended_players.append(list[i][0])
    return recommended_players


def compute_cos_similarity(point1, point2):
    numerator = numpy.dot(point1, point2)
    denominator = float(math.sqrt(numpy.dot(point1, point1))) * \
        float(math.sqrt(numpy.dot(point2, point2)))
    if denominator == 0:
        return 0
    return float(numerator)/float(denominator)


# Run Code below
if __name__ == '__main__':

    ######### Query #########
    my_team = "chicagobulls"
    n = 5
    # player = "Grayson Allen"
    player = "Paul George"
    ######### Query #########

    # get average stats
    avg_dict, eachteam_stats, categories = openCSV()

    # get team id's
    team_id_dict = getTeamIDs(eachteam_stats)

    # get target stats for ideal player
    target_stats = getTargetStats(player, categories, avg_dict)

    # get the team_id of the team that wants recommendations
    my_team_name = formatName(my_team)
    team_id = 0
    for team in team_id_dict.keys():
        if team_id_dict[team] == my_team_name:
            team_id = int(team)
            break

    ideal_player_dict = target_stats
    print(ideal_player_dict)
    (dict_of_players, ideal_player_array) = read_data_file("advanced_players.csv", ideal_player_dict)
    # recommended_players = n_nearest_neighbor(dict_of_players, ideal_player_array, team_id, n)
    # print ("The " + str(n) + " players recommended for " + str(my_team) + " are: " + str(recommended_players))
