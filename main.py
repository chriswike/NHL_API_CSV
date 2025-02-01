import requests
import csv
import json

game_or_season = input("Get Single Game or Entire Season?\n1 for Single Game\n2 for Entire Regular Season\n")

while game_or_season not in ['1', '2']:
    print("Invalid input. Please enter 1 for Game or 2 for Season")
    print("1 for Single Game")
    print("2 for Entire Regular Season")
    print()  # A blank line for better user input
    game_or_season = input()

if game_or_season == "1":
    # Get game ID from user
    game_id = input("Enter the game ID: ")
    game = f"https://api-web.nhle.com/v1/gamecenter/{game_id}/boxscore"
    response = requests.get(game)
    data = response.json()
elif game_or_season == "2":
    print("\nWARNING: The NHL API has rate limits. Making too many requests too quickly may result in temporary blocks.")
    print("This script will attempt to get data for all regular season games (~1300 games).")
    print("Press Enter to continue or Ctrl+C to cancel...")
    input()
    # Get Season Year from user
    season_year = input("Enter The Year\n")
    # Create base game ID using season year
    base_game_id = f"{season_year}02"
    # Make a way to monitor progress
    total_games = 13
    successful_games = 0
    failed_games = 0
    #Tell user its starting
    print("\nFetching games data...")
    # Loop through game numbers 1-999, padding with leading zeros
    for game_num in range(0, total_games):
        game_id = f"{base_game_id}{str(game_num).zfill(4)}"
        # Print status
        print(f"\rProgress: {game_num}/{total_games-1} games | Success: {successful_games} | Failed: {failed_games}", end="")
        # Construct API URL
        game = f"https://api-web.nhle.com/v1/gamecenter/{game_id}/boxscore"
        # Make API request
        response = requests.get(game)
        # Skip if game doesn't exist (non-200 status code)
        if response.status_code != 200:
            print(f"\nGame not found: {game_id}")
            failed_games += 1
            continue
        successful_games += 1
        data = response.json()
        
        # Extract plays data
        games = data['playerByGameStats']
        
        # Open CSV files for writing - one for skaters and one for goalies
        with open(f'{game_id}_skaters.csv', 'a', newline='') as skaters_file, \
             open(f'{game_id}_goalies.csv', 'a', newline='') as goalies_file:
            
            # Define headers for skaters and goalies (only write headers for first game)
            if game_num == 1:
                skater_headers = ['playerId', 'sweaterNumber', 'name', 'position', 'goals', 
                                'assists', 'points', 'plusMinus', 'pim', 'hits', 
                                'powerPlayGoals', 'sog', 'faceoffWinningPctg', 'toi', 
                                'blockedShots', 'shifts', 'giveaways', 'takeaways']
                
                goalie_headers = ['playerId', 'sweaterNumber', 'name', 'position',
                                'decision', 'powerPlayGoalsAgainst', 'savePctg', 'starter',
                                'shotsAgainst', 'saveShotsAgainst', 'shorthandedGoalsAgainst',
                                'evenStrengthGoalsAgainst', 'goalsAgainst', 'powerPlayShotsAgainst',
                                'saves', 'shorthandedShotsAgainst', 'evenStrengthShotsAgainst', 'toi',
                                'pim']
                
                skater_writer = csv.DictWriter(skaters_file, fieldnames=skater_headers)
                goalie_writer = csv.DictWriter(goalies_file, fieldnames=goalie_headers)
                skater_writer.writeheader()
                goalie_writer.writeheader()
            
            skater_writer = csv.DictWriter(skaters_file, fieldnames=skater_headers)
            goalie_writer = csv.DictWriter(goalies_file, fieldnames=goalie_headers)
            
            # Iterate through each team (away and home)
            for team in games.values():
                # Handle skaters (forwards and defense)
                for position_group in ['forwards', 'defense']:
                    if position_group in team:
                        for player_data in team[position_group]:
                            row = {}
                            for key, value in player_data.items():
                                if isinstance(value, dict):
                                    row[key] = value.get('default', '')
                                else:
                                    row[key] = value
                            skater_writer.writerow(row)
                
                # Handle goalies
                if 'goalies' in team:
                    for goalie_data in team['goalies']:
                        row = {}
                        for key, value in goalie_data.items():
                            if isinstance(value, dict):
                                row[key] = value.get('default', '')
                            else:
                                row[key] = value
                        goalie_writer.writerow(row)

# Print the keys to see the structure
# print("Available keys in response:", data.keys()) 

# Extract plays data
games = data['playerByGameStats']

# Print the structure to understand the data
# print("playerByGameStats structure:", type(games))
# print("Sample data:", json.dumps(games, indent=2)[:200])  # Print first 200 chars to see structure

# Open CSV files for writing - one for skaters and one for goalies
with open(f'{game_id}_skaters.csv', 'w', newline='') as skaters_file, \
     open(f'{game_id}_goalies.csv', 'w', newline='') as goalies_file:
    # Define headers for skaters
    skater_headers = ['playerId', 'sweaterNumber', 'name', 'position', 'goals', 
                     'assists', 'points', 'plusMinus', 'pim', 'hits', 
                     'powerPlayGoals', 'sog', 'faceoffWinningPctg', 'toi', 
                     'blockedShots', 'shifts', 'giveaways', 'takeaways']
    
    # Define headers for goalies
    goalie_headers = ['playerId', 'sweaterNumber', 'name', 'position',
                     'decision', 'powerPlayGoalsAgainst', 'savePctg', 'starter',
                     'shotsAgainst', 'saveShotsAgainst', 'shorthandedGoalsAgainst',
                     'evenStrengthGoalsAgainst', 'goalsAgainst', 'powerPlayShotsAgainst',
                     'saves', 'shorthandedShotsAgainst', 'evenStrengthShotsAgainst', 'toi',
                     'pim']
    
    skater_writer = csv.DictWriter(skaters_file, fieldnames=skater_headers)
    goalie_writer = csv.DictWriter(goalies_file, fieldnames=goalie_headers)
    
    skater_writer.writeheader()
    goalie_writer.writeheader()
    
    # Iterate through each team (away and home)
    for team in games.values():
        # Handle skaters (forwards and defense)
        for position_group in ['forwards', 'defense']:
            if position_group in team:
                for player_data in team[position_group]:
                    row = {}
                    for key, value in player_data.items():
                        if isinstance(value, dict):
                            row[key] = value.get('default', '')
                        else:
                            row[key] = value
                    skater_writer.writerow(row)
        
        # Handle goalies
        if 'goalies' in team:
            for goalie_data in team['goalies']:
                row = {}
                for key, value in goalie_data.items():
                    if isinstance(value, dict):
                        row[key] = value.get('default', '')
                    else:
                        row[key] = value
                goalie_writer.writerow(row)
