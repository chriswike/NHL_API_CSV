import requests
import csv
import json

# Get game ID from user
game_id = input("Enter the game ID: ")
game = f"https://api-web.nhle.com/v1/gamecenter/{game_id}/boxscore"
response = requests.get(game)
data = response.json()

# Print the keys to see the structure
# print("Available keys in response:", data.keys())

# Extract plays data
games = data['playerByGameStats']

# Print the structure to understand the data
# print("playerByGameStats structure:", type(games))
# print("Sample data:", json.dumps(games, indent=2)[:200])  # Print first 200 chars to see structure

# Open CSV files for writing - one for skaters and one for goalies
with open('skaters.csv', 'w', newline='') as skaters_file, open('goalies.csv', 'w', newline='') as goalies_file:
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
