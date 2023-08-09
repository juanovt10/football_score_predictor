import gspread
import random
import numpy as np
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
        home_team = input("Enter home team:\n").strip().title()

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
        away_team = input("Enter away team:\n").strip().title()

        entry_check = validate_team_entry(away_team, home_team)

        if entry_check[0]:
            print(f'\nAway team: {entry_check[2]}, league: {entry_check[1]}\n')
            break

    return entry_check[2], entry_check[1]


def suggest_team(input_team, teams_list):
    """
    In case the user's input is not a direct match with the strings from the
    spreadsheet. This function, scans the list of teams and use the fuzz method
    to check the similarity ratio, then the functions returns the best match
    from the scan, and the ratio so it can be checked in the
    validate_team_entry() function
    """
    best_match = None
    highest_ratio = 0

    for team in teams_list:
        ratio = fuzz.ratio(input_team.lower(), team.lower())
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = team

    return best_match, highest_ratio


def validate_team_entry(team_entry, home_team):
    """
    It retrives the data from all 5 worksheets.

    It then places the data in a dictionary where the keys are the league names
    and the values are the data from each worksheet.

    Then it extracts the list of teams, and added to a new dictionary where
    the keys are the league names and the values are a list of teams of each
    league.

    It then scans the lists of the dictionary to find a match, if it finds it,
    it returns a boolean, the league and the team entry.

    In the case that it doesn't find a match it calls the suggest_team()
    function. This function recives the user team entry and the list of all
    the teams of the 5 leagues, it then returns the best match and the match
    ratio.

    Then the function just assess if the ratio is high enough, provides a
    suggestion to the user, and then the user needs to confirm. If it does,
    then the function will return the league, team_suggestion and the boolean.
    If the user does not confirm, it returns the same but with a False boolean.
    """
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

    # Dictionary for all de leagues data:

    europe_leagues_data = {
        "Premier League": premier_league_data,
        "La Liga": la_liga_data,
        "Serie A": serie_a_data,
        "Bundesliga": bundesliga_data,
        "Ligue 1": ligue_1_data
    }

    league_teams = {}

    # Transpose data, get lists of league teams and fill them as the values of 
    # the league team dictionary
    for league_name, league_teams_data in europe_leagues_data.items():
        transpose_data = [list(row) for row in zip(*league_teams_data)]
        teams = (transpose_data[0])[1:]
        league_teams[league_name] = teams

    # Check values of the list in dicitonary
    for league_name, team_list in league_teams.items():
        if team_entry in team_list and team_entry != home_team:
            return True, league_name, team_entry

    # Check if the user input the same team as away
    if team_entry == home_team:
        print(f"""\nSorry but {team_entry} cannot be both the home and away team\n""")
        return False, league_name, team_entry

    # Create list with all the 5 league teams to use the suggest_team()
    europe_teams_list = []

    for value_list in league_teams.values():
        europe_teams_list.extend(value_list)

    suggested_team_info = suggest_team(team_entry, europe_teams_list)

    # With the values of the suggest_team() check if there is a match
    # higher than 70% and check with the user if they to confirm their input
    if suggested_team_info[1] > 70:
        while True:
            print(f"\nDid you mean '{suggested_team_info[0]}'?")
            confirm_input = input("Enter 'Y' for Yes or 'N' for No:\n").strip().lower()
            if confirm_input == "y":
                for league_name, team_list in league_teams.items():
                    if suggested_team_info[0] in team_list and suggested_team_info[0] != home_team:
                        return True, league_name, suggested_team_info[0] 
                break
            elif confirm_input == "n":
                break
            else: 
                print(f"\nInvalid answer: {confirm_input}")

    print(f"""\nSorry but we couldn't find a match for {team_entry}. If you are sure that {team_entry} plays in Europe's top 5 leagues, try to check for typos or an alternative name for the team\n""")
    return False, league_name, suggested_team_info[0]


def retrive_random_teams():
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

    # Dictionary for all de leagues data:

    europe_leagues_data = {
        "Premier League": premier_league_data,
        "La Liga": la_liga_data,
        "Serie A": serie_a_data,
        "Bundesliga": bundesliga_data,
        "Ligue 1": ligue_1_data
    }

    league_teams = {}

    # Transpose data, get lists of league teams and fill them as the values of 
    # the league team dictionary
    for league_name, league_teams_data in europe_leagues_data.items():
        transpose_data = [list(row) for row in zip(*league_teams_data)]
        teams = (transpose_data[0])[1:]
        league_teams[league_name] = teams

    europe_teams_list = []

    for value_list in league_teams.values():
        europe_teams_list.extend(value_list)
    
    random_teams = random.sample(europe_teams_list, 2)

    return random_teams


def input_match_score():
    while True:
        try:
            score_input = input("Please enter the score (e.g 2-1, 1-2, 3-0):\n").strip()
            home_score, away_score = map(int, score_input.split('-'))

            if home_score < 0 or away_score < 0: 
                print("\nInvalid score. Scores must be positive integers")
            else:
                return home_score, away_score
        except ValueError:
            print("\nInvalid input. Please enter the score in the format 'X-Y', where X and Y are positive integers")


def score_comparisson(input_scores, calculated_scores):
    input_home, input_away = input_scores
    calc_home, calc_away = calculated_scores

    if input_scores == calculated_scores:
        return "\nYou guessed it!"
    else: 
        return "\nSorry wrong answer"


def get_team_data(team, league_name):
    """
    This function scans the spreadsheet and collects the row (list) of the
    stats of the inputted teams. It then, calculate a weighted average of
    each stat by giving more weight to latest season stats.
    """
    league_worksheet = SHEET.worksheet(league_name)
    league_data = league_worksheet.get_all_values()

    str_data = []
    for team_data in league_data:
        if team_data[0] == team:
            str_data = team_data[1:]
            break
    
    
    data = [float(i) for i in str_data]

    stat_indexes = [0, 1, 2, 3, 4, 5, 6]

    stats_weighted_averages = []

    for index in stat_indexes:
        stat_weighted_average = 0
        counter = 0

        for i in range(index, len(data), 7):
            stat_weighted_average += ((data[i]) * (5 - counter))
            counter += 1
            

        stats_weighted_averages.append(stat_weighted_average / 15)
        

    return stats_weighted_averages


def result_calculator(home_stats, away_stats):
    """
    This function multyply each stat for a factor and then adds them all up to
    provide a match
    """

    score_factors = [0.5, 0.25, 0.5, 0.75, 0.5, 0.75, -0.75]

    home_score_factors = [x * y for x, y in zip(home_stats, score_factors)]
    away_score_factors = [x * y for x, y in zip(away_stats, score_factors)]

    home_offensive_factors = home_score_factors[:4]
    away_offensive_factors = away_score_factors[:4]

    home_defensive_factors = home_score_factors[-3:]
    away_defensive_factors = away_score_factors[-3:]

    home_ratio = sum(home_offensive_factors) / (1/sum(away_defensive_factors))
    away_ratio = sum(away_offensive_factors) / (1/sum(home_defensive_factors))

    home_ratio = np.exp(home_ratio) / (np.exp(home_ratio) + np.exp(away_ratio))
    away_ratio = np.exp(away_ratio) / (np.exp(home_ratio) + np.exp(away_ratio))

    home_score = int(home_ratio * sum(home_offensive_factors))
    away_score = int(away_ratio * sum(away_offensive_factors))

    home_score += 1

    home_score = max(0, min(5, home_score))
    away_score = max(0, min(5, away_score))

    return home_score, away_score


def find_mode():
    print("\nPlease enter the teams you want to find out the score")
    print("Example: Manchester United, Real Madrid, Juventus, Montpellier, Bayern Munich\n")
    home_team_info = input_home_team()
    away_team_info = input_away_team(home_team_info[0])
    home_team_data = get_team_data(home_team_info[0], home_team_info[1])
    away_team_data = get_team_data(away_team_info[0], away_team_info[1])
    result = result_calculator(home_team_data, away_team_data)

    print(f"The result is: {home_team_info[0]} {result[0]} - {result[1]} {away_team_info[0]}")


def guess_mode():
    random_teams = retrive_random_teams()
    print("\nWhat do you think will be the score between these two teams?")
    print(f"Home team: {random_teams[0]}")
    print(f"Away team: {random_teams[1]}")
    score_input = input_match_score()

    home_team_info = validate_team_entry(random_teams[0], "")
    away_team_info = validate_team_entry(random_teams[1], "")

    home_team_data = get_team_data(home_team_info[2], home_team_info[1])
    away_team_data = get_team_data(away_team_info[2], away_team_info[1])
    result = result_calculator(home_team_data, away_team_data)

    guess_feedback = score_comparisson(score_input, result)

    print(guess_feedback + " " + f"The result is: {home_team_info[2]} {result[0]} - {result[1]} {away_team_info[2]}")


def restart_program():
    while True: 
        print("\nDo you want to use the program again?")
        use_again = input("Enter 'Y' for yes or 'N' for no:\n").strip().lower()
        if use_again == 'y':
            break
        elif use_again == 'n':
            print("\nThank you for using the 2023/24 footbal predictor!")
            exit()
        else:
            print(f"\nInvalid input: {use_again}. Please enter 'Y' for yes or 'N' for no")


def main():
    print("Welcome to the 2023/24 season foorball predictor. This program allows you to choose between find out a score or guessing one from two random teams\n")
    print("Note that this program only assesses Europe's top 5 leagues' teams:")
    print("Premier League (ENG), La Liga (ESP), Serie A (ITA), Bundesliga (GER) and Ligue 1 (FRA)")
    
    while True:
        print("\nChoose program mode")
        user_decision = input("Enter 'find' or 'guess':\n").strip().lower()
        if user_decision == 'find':
            find_mode()

            restart_program()

        elif user_decision == 'guess':
            guess_mode()

            restart_program()
        else:
            print(f"\nInvalid answer: {user_decision}")


main()
