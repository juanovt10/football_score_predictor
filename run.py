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

def get_home_team_data():
    """
    Requests the home team to retrive the previous season statistics
    """
    while True:
        print("Please enter the home team")
        print("Note that this program only assesses the Premier League 2023/24 teams")
        print("Example: Manchester United")

        home_team = input("Enter team A here:\n")

        if validate_team_entry(home_team):
            print(f'{home_team} is in the Premier League\n')
            break

    return home_team

def validate_team_entry(team_entry):
    """
    Inside here, it will transpose the columns to rows to have a list will all the 
    Premier League teams. Then it will compare the value imputted by the user to see 
    if the team inputted is part of the premier league. 
    """

    all_data = SHEET.worksheet("PremierLeague")
    original_data = all_data.get_all_values()
    transpose_data = [list(row) for row in zip(*original_data)]

    teams = (transpose_data[0])[1:]

    for team in teams:
        if team_entry == team:
            return True

    print(f"Sorry but {team_entry} is not in the Premier League\n")
    return False


def get_away_team_data():
    """
    Requests the away team to retrive the previous season statistics
    """
    while True:
        print("Please enter the away team")
        print("Note that this program only assesses the Premier League 2023/24 teams")
        print("Example: Manchester City")

        away_team = input("Enter team B here:\n")

        if validate_team_entry(away_team):
            print(f'{away_team} is in the Premier League\n')
            break

    return away_team

def main():
    home_team = get_home_team_data()
    away_team = get_away_team_data()


main()