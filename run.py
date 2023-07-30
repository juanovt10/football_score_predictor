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


# data = SHEET.worksheet("PremierLeague")
# original_data = data.get_all_values()
# transpose_data = [list(row) for row in zip(*original_data)]

# teams = (transpose_data[0])[1:]
# match_found = False

# team_entry = input("Enter team A here:\n")
# for team in teams: 
#     if team_entry == team:
#         match_found = True
#         break 

# if match_found:
#     print('good entry')
# else: 
#     print('bad entry')




def get_teamA_data():
    """
    Requests the home team to retrive the previous season statistics
    """
    while True:
        print("Please enter the home team")
        print("Note that this program only assesses the Premier League 2023/24 teams")
        print("Example: Manchester United")

        team_a = input("Enter team A here:\n")

        if validate_team_entry(team_a):
            print(f'{team_a} is in the Premier League\n')
            break

    return team_a

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

get_teamA_data()