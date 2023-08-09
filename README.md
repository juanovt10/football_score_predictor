# Europe's football top 5 leagues 2023/24 predictor

This european football predictor is a python tool is designed to help users forecast match scores between two teams from the top European leagues. By analyzing their performance over the past five seasons, the tool generates accurate score predictions, offering valuable insights for football enthusiasts.

This project runs in the Code Institue mock terminal on Heroku.

This football predictor is live, to access it [click here.](https://football-score-predictor-a1ed8268ea3d.herokuapp.com/)

![responsive test](assets/readme_images/responsive_test.png)

# Table of contents 
+ [How to use it](#how-to-use-it)
+ [Project Planning](#project-planning)
+ [Features](#features)
+ [Data Model](#data-model)
+ [Testing](#testing)
+ [Technologies used](#technologies-used)
+ [Deployment](#deployment)
+ [Credits](#credits)

# How to use it

This football predictor utilizes data from the top 5 European leagues spanning from the 2018/19 season to the 2022/23 season.

Upon launching the program, users are welcomed and provided with a concise explanation of its functionalities, as well as the leagues it can evaluate. 

The user has two choices, find out a score by inputing two teams or guess a score between two teams randomly displayed.

## Find out score mode

The program prompts the user to input the home and away teams. Leveraging their past season data and considering the home advantage, it calculates the likely match outcome. Home teams enjoy the "home" advantage, which is factored into the result prediction.

In scenarios where the user inputs a team name that does not precisely match the data spreadsheet, the program incorporates a percentage match feature. It then suggests a team based on this matching percentage and asks for user confirmation before proceeding further. This ensures accurate team selection and enhances the overall user experience.

If the user fails to provide an input with a match larger than 70%, the program will promptly provide feedback indicating that the input team is not part of Europe's top five leagues. Following that, it will request the user to re-enter the team name, ensuring compatibility with the supported leagues for accurate predictions.

## Guess score mode

In this mode, the program scans teams from the five European leagues and randomly selects two for users to guess the score of a match between them. Users must adhere to a specific format when entering scores (two numbers separated by a hyphen). If scores are not input in the correct format, an error message is displayed, prompting users to re-enter the input.

Upon correct input of the score, the program assesses the result based on calculations performed in the "find out score" mode. It then compares this result with the user's input and delivers feedback indicating the accuracy of the guess.

# Project planning

The purpose of the project is to process the data of the past 5 seasons of the european leagues and find out scores. The project features were defined by the following flow chart:

![flow chart p1](assets/readme_images/flow_chart_p1.png)
![flow chart p2](assets/readme_images/flow_chart_p2.png)

However, the process was break down into 4 stages: 

1. Begin by integrating data for a single league into the datasheet, ensuring the functionality of the "find out score" mode.
2. Once the initial mode is verified, extend the implementation to encompass the remaining four European leagues, while maintaining the effectiveness of the "find out score" mode.
3. Enhance the program by incorporating a team suggestion function, recognizing that football teams often have multiple recognized names.
4. Elevate the program's capabilities by introducing the "guess score" mode. This mode will present users with two randomly selected teams, prompt for precise user input, and subsequently compare the user's input against the calculated outcome.e 

The presented flowchart showcases a notable omission—the inclusion of the head-to-head results for incorporation into the score result calculation. To address this, an API connection is recommended for retrieving this dynamic statistic. This approach is favored due to the substantial volume of data involved. While each team competes in 38 league matches annually, additional engagements like regional and international cups further compound the dataset. Leveraging an API streamlines the retrieval process by accessing specialized databases, expediting requests that would otherwise be time-intensive when dealing with static data.

# Features

## Existing features
- Welcome the user to the program
    * Clear display of the capacities and limitations of the program

    ![Welcome message](assets/readme_images/welcome_message.png)

- Ability to choose between two program modes

    ![Program modes](assets/readme_images/program_modes.png)

- Find out score
    * When choosing the find out score, the console asks the user which teams they want to check for the score, with some examples:

    ![Find mode welcome](assets/readme_images/find_mode_intro.png)

    * After the user inputs an accurate team, the program will provide feedback of which team the user selected and the league this team plays. Then it proceeds to ask the user the away team:

    ![Find mode away team](assets/readme_images/find_mode_second_input.png)

    * If the user inputs a valid team, the program will also display the away team and the league where the team plays. Then it will retrieve the data of both teams using the API connection, perform statistical calculations and provide a result: 

    ![Find mode result](assets/readme_images/find_mode_result.png)

- Guess mode
    * When the guess mode is selected, the program will randomly select two teams from the 5 leagues, and will ask the user to input the score in a specific format:

    ![Guess mode intro](assets/readme_images/guess_mode_intro.png)

    * If the user inputs a score in the correct format, the program will calculate which will be the score of those two teams using the statistical analysis and will then compare it with the user input. If the user is correct, it will display positive feedback and if the user is incorrect, it will display negative feedback:

    ![Guess mode result](assets/readme_images/guess_mode_result.png)

- Restart program
    * After using the find or guess mode, the program will ask the user if they want to use the project again:

    ![Restart program](assets/readme_images/restart_program.png)



- Team suggestion
    * In football, teams can be known by various names, including nicknames, acronyms, or simplified versions of their official names. For instance: 
        * Machester Untied, Man Untied
        * Bayern Munchen, Bayern Munich
        * FC Barcelona, Barcelona, Barca
    * To address the variation in team names, I utilized the fuzzywuzzy fuzz method. This approach calculates the similarity between two strings, allowing for a more robust and flexible matching process.
    * By combining the fuzzywuzzy method with data_entry_validation(), the program offers the best matching suggestion for the user's input. It then seeks user confirmation to ensure the intended team is accurately identified and considered for further processing.

    ![Team suggestion](assets/readme_images/team_suggestion.png)

- Input control 
    * The program asks the user multiple inputs in various formats:
        * Select program mode
        * Input teams in find mode
        * Approve team suggestion
        * Input teams score
        * Restart program
    
    For the approval of team suggestion, restart program and selecting program mode, the user is asked to enter specific inputs depending on the action the want to take. It can be 'y' or 'n' for yes or no, or 'find' or 'guess' for find or guess modes. If the user enters something different than specified, the program will display and invalid input and ask the user again:

    ![Program mode error](assets/readme_images/program_mode_incorrect_input.png)

    ![Team suggestion error](assets/readme_images/team_suggestion_incorrect_input.png)

    ![Restart program error](assets/readme_images/restart_program_incorrect_input.png)

    When entering the input teams, the program will first try to suggest a team if the user input has a 70% similarity with any of the teams in the database. However, if there is no match, it will provide feedback to the user stating that the team is either not in the leagues that the program uses or to check for typos or alternative names:

    ![Team input error](assets/readme_images/invalid_team_input.png)

    For the guess mode, the program specifies which type of format the score sholuld be enter to run the program. If the user does not comply, it will display an invalid message and ask for the input again:

    ![Score input error](assets/readme_images/invalid_score_input.png)

- Data retrival and processing
    * The program scans all 5 worksheets to identify or suggest a match based on user input
    * The program then uses the matches to retrive the specfiic statistics for the teams
    * It the process this data by calculating a weighted average of each team's statistics, which is then multiplied by a factor to determine the result
    * To account for the home advantage, it adds 1 goal for the home team and subtracts 1 goal from the away team.
    * To provide a realistic result, the program sets a maximum goal output of 5 goals.

## Future features

- Use API connection to retrive data from a specific database instead if using static data 
- When using an API connetion, a regression model can be used in conjuction of multiple statistics to arrive to a more accurate result

# Data model
For this project, I employed static data retrieved from [FootyStats](https://footystats.org/). The following statistics were utilized to process and calculate the match result:

- xG (expected goals/match)
- Possession percentage/match
- Shots per match/covertion ratio
- Goals scored/match
- xG against (expected goals conceded/match)
- Goals conceded/match
- Clean sheet percentage

## Data collection and manipulation

The data collection process involved organizing the statistics for each team into specific worksheets. The spreadsheet comprises 5 worksheets, each representing one of Europe's top 5 leagues.

It is important to note that European football leagues operate on a relegation/promotion basis. This means that teams ending a season in the bottom part of the table (typically the last three positions) get relegated to a lower division, while the winners of the lower division get promoted to the first division.

Due to this system, teams are constantly moving between divisions, resulting in discrepancies in statistics due to the different football level. To address this, the data was amended and corrected accordingly. For teams that played in lower divisions in the past five seasons, offensive statistics (such as xG, possession, shots, and goals) were reduced by 20%, while defensive statistics (like xG against and goals conceded) were increased by 20%. This adjustment ensures a fair comparison between teams playing at different levels of football.

## Data processing

The program scans the spreadsheet to retrieve statistics for the user-inputted teams, calculating a weighted average by assigning higher importance to more recent seasons. This approach accounts for the dynamic nature of football teams, which can experience exponential growth or decline based on their performance.

To compute the weighted average, each statistic is multiplied by a corresponding factor. Specifically, the statistics from the 2022/23 season are multiplied by 5, those from 2021/22 by 4, and so on, until the 2018/19 season, which is multiplied by 1. The resulting values are then summed and divided by 15 (the sum of the weights) to derive the weighted average, offering a nuanced evaluation of the teams' overall performance.

After processing the weighted averages, these are multuply by a factor to provide a result. The factors used where: 

- xG * 0.5 
- Possession * 0.25
- Shots/conversion rate * 0.5
- Goals * 0.75
- xG against * 0.5 
- Goals conceded * 0.75
- Clean sheet percentage * -0.75

After multiplying the weighted averages with the "score" factors, the offensive and defensive values are compared by calculating a ratio between the sum of all offensive factors of the home team and the inverse of the defensive factors the away team and viceversa. The purpose of using the inverse, is that the largerst the sum of the defensive factors the worst they are defensively. After calculating the ratios, I used numpy to apply a softmax-like transformation of this ratios to keep them between 0 and 1, then I just multiply these ratios by the sum offensive values to arrive to a score. 

Additionally, home teams typically enjoy an advantage, benefiting from the majority of supporters and familiar conditions. Consequently, one goal was added to home teams.

To ensure more realistic predictions, a maximum limit of 5 goals was set, preventing results that exceeded this threshold. Similarly, to maintain realism, a minimum limit of 0 goals was applied to teams with extremely negative statistics, preventing them from obtaining negative scores. 

# Testing*

I have tested the project by performing the following tests: 

- Passed the code throigh a PEP8 linter and confirm there are no problems
- Provide invalid inputs, such as numbers or strings that do not match or provide a realistic match for the teams in these leagues
- Tested in my local terminal and the Code Institute Heroku terminal

Most of the coding challenges centered around refining the validate_team_entry() function. At the project's outset, the focus was on ensuring exact matches, data retrieval, and precise result provision. To accomplish this, a single worksheet was scanned, data transposed, and exact matches retrieved for processing.

Once the core functionality was robust, expansion to cover the other four leagues was necessary. This entailed not only checking team presence but also determining the league for scanning in the get_team_data() function. A get_team_league() function was introduced, utilizing a dictionary structure to categorize teams by league. This enabled accurate league detection for proper spreadsheet access in get_team_data().

Recognizing similarities between get_team_data() and validate_team_entry(), a refactoring effort emerged. The latter function, apart from allowing program continuation via boolean return, now also supplied the team's league for get_team_data() reference.

The ensuing challenge lay in suggesting teams when an exact match eluded user input. Incorporating a team suggestion mechanism within validate_team_entry() was logical, encompassing match assessment, user confirmation, and entry validation.

To achieve this, the suggest_team() function was formulated, employing the Levenshtein distance method to gauge string similarity. By comparing user input with league-specific teams, the function determined the best match, presenting it for user confirmation.

Integration of suggest_team() within validate_team_entry() proved slightly intricate due to technicalities involving the lower() method in the suggest_team() function and the league_teams dictionary in the validate_team_entry() function. To mitigate this, a consolidated list of all teams was generated within validate_team_entry() and fed into suggest_team().

This meticulous process significantly enhanced the program's functionality, ranging from exact match validation to team suggestions, and culminated in a more streamlined and efficient codebase.

## Unfixed bugs

- The program operates within a specific constraint concerning the number of requests it can process per minute. Consequently, should a user opt for multiple program iterations, an error message will eventually be displayed, indicating the program's surpassing of the API request limit: 

![API request limit](assets/readme_images/API_request_limit.png)

## Validator testing

- The python file passes through the [PP8 validator](link) with no issues

# Technologies used

## Programming languages used

- Python 3

## Frameworks, Libraries & programs

- GitHub - to store my repository for submission.
- CodeAnywere - to creat my py file before pushing the project to Github.
- Heroku - by using the Code Institute template, I could deploy a web mock terminal where the program can run 
- gspread - to have a direct access to google sheets 
- google-auth - Google authentication credential to access Google APIs
- fuzzywuzzy - Python library used for string matching and string similarity
- NumPy - Python library used for scientific computing
- Am I responsive - to ensure the project looked good across all devices.

# Deployment

The program was deployed using Code Institue's mock termina for Heroku.

- Create a new Heroku app 
- Define the configuration vars: creds.json and PORT 
- Define the python and Node.js buildpacks
- Link the Heroku app with the GitHub repository
- Deploy the app

# Credits

## Data

- Data was collected from [FootyStats](https://footystats.org/)

## Code

- Love-sandwiches walkthorugh project provided by [Code Institute](https://codeinstitute.net/global/)
- Fuzzywuzzy library [Offical Python documentation](https://pypi.org/project/fuzzywuzzy/), and [use explanation](https://www.geeksforgeeks.org/fuzzywuzzy-python-library/)
- NumPy Library [Official NumPy](https://numpy.org/), and [stackoverflow](https://stackoverflow.com/questions/34968722/how-to-implement-the-softmax-function-in-python) to get the explanations of how to use the Softmax-like transformation.
- The .title() method [explanation](https://www.w3schools.com/python/ref_string_title.asp#:~:text=The%20title()%20method%20returns,be%20converted%20to%20upper%20case.)
- Function retruning more than 1 value [explanation](https://www.geeksforgeeks.org/g-fact-41-multiple-return-values-in-python/)
- List() method [explanation](https://www.programiz.com/python-programming/methods/built-in/list)