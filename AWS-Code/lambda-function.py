import json

import algorithm


def lambda_handler(event, context):
    # return event['queryStringParameters']
    my_team = event['queryStringParameters']['Team']
    n = (int)(event['queryStringParameters']['Limit'])

    # get average stats
    avg_dict, eachteam_stats, categories = algorithm.openCSV()

    # get team id's
    team_id_dict = algorithm.getTeamIDs(eachteam_stats)

    # get percent differences
    percent_diff_dict = algorithm.getIdealPlayer(
        avg_dict, eachteam_stats, categories, my_team)

    # get target stats for ideal player
    target_stats = algorithm.getTargetStats(
        percent_diff_dict, avg_dict, categories)

    # get the team_id of the team that wants recommendations
    my_team_name = algorithm.formatName(my_team)
    team_id = 0
    for team in team_id_dict.keys():
        if team_id_dict[team] == my_team_name:
            team_id = int(team)
            break

    ideal_player_dict = target_stats
    (dict_of_players, ideal_player_array) = algorithm.read_data_file(
        "advanced_players.csv", ideal_player_dict)
    recommended_players = algorithm.n_nearest_neighbor(
        dict_of_players, ideal_player_array, team_id, n)
    # print ("The " + str(n) + " players recommended for " + str(my_team) + " are: " + str(recommended_players))

    message = {}
    message['Team'] = my_team
    message['Players'] = recommended_players
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(message)
    }
