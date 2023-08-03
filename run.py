import gspread
from google.oauth2.service_account import Credentials
from fuzzywuzzy import fuzz

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCROPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCROPED_CREDS)
SHEET = GSPREAD_CLIENT.open('europe_football_leagues')


def input_home_team():
    """
    Requests the home team to retrive the previous season statistics
    """
    while True:
        home_team = input("Enter home team:\n").title()

        entry_check = validate_team_entry(home_team, "")

        if entry_check[0]:
            print(f'\nHome team: {entry_check[2]}, league: {entry_check[1]}\n')
            break

    return entry_check[2], entry_check[1]


def input_away_team(home_team):
    """
    Requests the away team to retrive the previous season statistics
    """
    while True:
        away_team = input("Enter away team:\n").title()

        entry_check = validate_team_entry(away_team, home_team)

        if entry_check[0]:
            print(f'\nAway team: {entry_check[2]}, league: {entry_check[1]}\n')
            break

    return entry_check[2], entry_check[1]


def suggest_team(input_team, teams_list):
    best_match = None
    highest_ratio = 0

    for team in teams_list:
        ratio = fuzz.ratio(input_team.lower(), team.lower())
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = team

    return best_match, highest_ratio


def validate_team_entry(team_entry, home_team):
    premier_league_worksheet = SHEET.worksheet("Premier League")
    la_liga_worksheet = SHEET.worksheet("La Liga")
    serie_a_worksheet = SHEET.worksheet("Serie A")
    bundesliga_worksheet = SHEET.worksheet("Bundesliga")
    ligue_1_worksheet = SHEET.worksheet("Ligue 1")

    premier_league_data = premier_league_worksheet.get_all_values()
    la_liga_data = la_liga_worksheet.get_all_values()
    serie_a_data = serie_a_worksheet.get_all_values()
    bundesliga_data = bundesliga_worksheet.get_all_values()
    ligue_1_data = ligue_1_worksheet.get_all_values()

    europe_leagues_data = {
        "Premier League": premier_league_data,
        "La Liga": la_liga_data,
        "Serie A": serie_a_data,
        "Bundesliga": bundesliga_data,
        "Ligue 1": ligue_1_data
    }

    league_teams = {}

    for league_name, league_teams_data in europe_leagues_data.items():
        transpose_data = [list(row) for row in zip(*league_teams_data)]
        teams = (transpose_data[0])[1:]
        league_teams[league_name] = teams

    for league_name, team_list in league_teams.items():
        if team_entry in team_list and team_entry != home_team:
            return True, league_name, team_entry

    europe_teams_list = []

    for value_list in league_teams.values():
        europe_teams_list.extend(value_list)

    suggested_team_info = suggest_team(team_entry, europe_teams_list)

    if suggested_team_info[1] > 70:
        print(f"\nDid you mean '{suggested_team_info[0]}'?")
        confirm_input = input("Enter 'Y' for Yes or 'N' for No:\n").strip().lower()
        if confirm_input == "y":
            for league_name, team_list in league_teams.items():
                if suggested_team_info[0] in team_list and suggested_team_info[0] != home_team:
                    return True, league_name, suggested_team_info[0]

    if team_entry == home_team:
        print(f"\nSorry but {team_entry} cannot be both the home and away team\n")
    else:
        print(f"\nSorry but {team_entry} is not in Europe's top 5 leagues\n")

    return False, league_name, suggested_team_info[0]


def get_team_data(team, league_name):
    """
    This function scans the spreadsheet and collects the row (list) of the stats of
    the inputted teams. It then, calculate a weighted average of each stat by giving
    more weight to latest season stats.
    """
    league_worksheet = SHEET.worksheet(league_name)
    league_data = league_worksheet.get_all_values()

    str_data = []
    for team_data in league_data:
        if team_data[0] == team:
            str_data = team_data[1:]
            break

    data = [float(i) for i in str_data]

    stat_indexes = [0, 1, 2, 3, 4, 5]

    stats_weighted_averages = []

    for index in stat_indexes:
        stat_weighted_average = 0
        for i in range(index, len(data), 6):
            stat_weighted_average += ((data[i]) * (6-(i/6)))

        stats_weighted_averages.append(stat_weighted_average / 15)

    return stats_weighted_averages


def result_calculator(stats, location):
    """
    This function multyply each stat for a factor and then adds them all up to
    provide a match
    """
    score = 0
    score += int(stats[0] * 0.5)
    score += int(stats[1] * 0.25)
    score += int(stats[2] * 0.75)
    score += int(stats[3] * 1)
    score += int(stats[4] * (-0.5))
    score += int(stats[5] * (-1))

    if location == "home":
        score += 1
    else:
        score -= 1

    if score > 5:
        score = 5
    elif score < 0:
        score = 0

    return score


def main():
    print("Welcome to the 2023/24 season foorball predictor. Enter the teams and based in the last 5 seasons performance, find out the score!\n")
    print("Note that this program only assesses Europe's top 5 leagues' teams:")
    print("Premier League (ENG), La Liga (ESP), Serie A (ITA), Bundesliga (GER) and Ligue 1 (FRA)\n")
    print("Example: Manchester United, Real Madrid, Inter, PSG, Bayern Munich\n")
    home_team_info = input_home_team()
    away_team_info = input_away_team(home_team_info[0])
    home_team_data = get_team_data(home_team_info[0], home_team_info[1])
    away_team_data = get_team_data(away_team_info[0], away_team_info[1])
    home_result = result_calculator(home_team_data, "home")
    away_result = result_calculator(away_team_data, "away")

    print(f"The result is: {home_team_info[0]} {home_result} - {away_result} {away_team_info[0]}")


main()
