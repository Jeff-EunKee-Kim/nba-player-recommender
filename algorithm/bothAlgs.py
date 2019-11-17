import csv 
import numpy
import math 
import heapq 

# Ideal Player Algorithm below
def openCSV():
    filename = '../general_team.csv'

    # Getting all of the resident rankings
    with open(filename) as file:
        linereader = csv.reader(file)
        
        # get categories
        cats = next(linereader)
        categories = []
        for i in cats:
            new = i.replace(' ','')
            categories.append(new)

        # stats we are looking for
        looking_for_stats = ['AGE', 'FG_PCT', 'FG3_PCT','FT_PCT','REB', 'AST','TOV','STL','BLK']

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

        print(avg_stats)

        return avg_stats, eachteam_stats_out, categories

def getIdealPlayer(avg_dict, eachteam_stats, categories, my_team):

    # final output dict
    comparisons_dict = dict()

    # query team
    team = formatName(my_team)

    # stats for query team
    team_stats = eachteam_stats[team]

    for i in avg_dict:
        comparisons_dict[categories[i]] = percentDiff(team_stats[i], avg_dict[i])

    print(comparisons_dict)

    return comparisons_dict

def getTeamIDs(eachteam_stats):
    # maps team ID to name of team
    team_id_dict = dict()

    for i in eachteam_stats:
        team_id_dict[eachteam_stats[i][0]] = i

    return team_id_dict

def getTargetStats(percent_diff_dict, avg_dict, categories):

    # Get target stats for ideal player
    target_stats = dict()
    for i in avg_dict:
        percent_diff = percent_diff_dict[categories[i]]

        # if percent diff is negative, that means team is worse than average, so include this stat
        if percent_diff < 0:
            target_stats[categories[i]] = avg_dict[i] * (1 - percent_diff)

    print(target_stats)

    return target_stats
    
def formatName(team):
    formatted_team = team.replace(' ','')
    return formatted_team.lower()

def percentDiff(thisteam, average):
    return ((float(thisteam) - average) / average)

# Recommender Algorithm below
def read_data_file(filename, ideal_player_dict):
    # key = title of statistic
    # value = numerical value of statistic
    file = open(filename)
    first_line = ("".join(file.readline().strip("\n"))).split(",")
    player_name = first_line.index("PLAYER_NAME")
    team_id = first_line.index("TEAM_ID")
    mpg_index = first_line.index("MIN")
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
        mpg_val = float(newline[mpg_index])
        if mpg_val < 12:
            continue
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
    denominator = float(math.sqrt(numpy.dot(point1, point1))) * float(math.sqrt(numpy.dot(point2, point2)))
    if denominator == 0:
        return 0
    return float(numerator)/float(denominator)

## Run Code below
if __name__ == '__main__':

    ######### Query #########
    my_team = "bostonceltics"
    n = 5
    ######### Query #########

    # get average stats
    avg_dict, eachteam_stats, categories = openCSV()

    # get team id's
    team_id_dict = getTeamIDs(eachteam_stats)

    # get percent differences
    percent_diff_dict = getIdealPlayer(avg_dict, eachteam_stats, categories, my_team)

    # get target stats for ideal player
    target_stats = getTargetStats(percent_diff_dict, avg_dict, categories)

    # get the team_id of the team that wants recommendations
    my_team_name = formatName(my_team)
    team_id = 0
    for team in team_id_dict.keys():
        if team_id_dict[team] == my_team_name:
            team_id = int(team)
            break

    ideal_player_dict = target_stats
    (dict_of_players, ideal_player_array) = read_data_file("../general_stats.csv", ideal_player_dict)
    recommended_players = n_nearest_neighbor(dict_of_players, ideal_player_array, team_id, n)
    print ("The " + str(n) + " players recommended for " + str(my_team) + " are: " + str(recommended_players))
