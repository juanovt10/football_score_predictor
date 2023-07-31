import gspread
from google.oauth2.service_account import Credentials

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
        print("Please enter the home team")
        print("Note that this program only assesses the Premier League 2023/24 teams")
        print("Example: Manchester United")

        home_team = input("Enter team A here:\n")

        if validate_team_entry(home_team, ""):
            print(f'{home_team} is in the Premier League\n')
            break

    return home_team

def validate_team_entry(team_entry, home_team):
    """
    Inside here, it will transpose the columns to rows to have a list will all the 
    Premier League teams. Then it will compare the value imputted by the user to see 
    if the team inputted is part of the premier league. 
    """

    premier_league_worksheet = SHEET.worksheet("PremierLeague")
    original_data = premier_league_worksheet.get_all_values()
    transpose_data = [list(row) for row in zip(*original_data)]

    teams = (transpose_data[0])[1:]

    for team in teams:
        if team_entry == team and team_entry != home_team:
            return True

    print(f"Sorry but {team_entry} is not in the Premier League\n")
    return False


def input_away_team(home_team):
    """
    Requests the away team to retrive the previous season statistics
    """
    while True:
        print("Please enter the away team")
        print("Note that this program only assesses the Premier League 2023/24 teams")
        print("Example: Manchester City")

        away_team = input("Enter team B here:\n")

        if validate_team_entry(away_team, home_team):
            print(f'{away_team} is in the Premier League\n')
            break

    return away_team

def get_team_data(team):
    premier_league_worksheet = SHEET.worksheet("PremierLeague")
    original_data = premier_league_worksheet.get_all_values()
    
    str_data = []
    for team_data in original_data:
        if team_data[0] == team:
            str_data = team_data[1:]
            break

    data = [float(i) for i in str_data]

    print(data)

    xg_weighted_average = 0

    for i in range(0, len(data), 5):
        xg_weighted_average += ((data[i]) * (5-(i/5)))
    
    xg_weighted_average /= 15

    print(xg_weighted_average)



def main():
    home_team = input_home_team()
    away_team = input_away_team(home_team)
    get_team_data(home_team)
    get_team_data(away_team)

main()