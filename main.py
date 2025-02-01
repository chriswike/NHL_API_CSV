import requests
import csv
import json

def get_user_choice():
    """Get and validate user input for game/season choice."""
    prompt = ("Get Single Game or Entire Season?\n"
              "1 for Single Game\n"
              "2 for Entire Regular Season\n")
    choice = input(prompt)
    
    while choice not in ['1', '2']:
        print("Invalid input. Please enter 1 for Game or 2 for Season")
        print("1 for Single Game")
        print("2 for Entire Regular Season")
        print()
        choice = input()
    return choice

def write_player_data(writer, player_data):
    """Write player data to CSV, handling nested dictionaries."""
    row = {}
    for key, value in player_data.items():
        if isinstance(value, dict):
            row[key] = value.get('default', '')
        else:
            row[key] = value
    writer.writerow(row)

def process_game_data(game_id, data, is_first_game=False):
    """Process and write game data to CSV files."""
    games = data['playerByGameStats']
    
    # Define headers
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
    
    # Open files in write mode
    with open(f'{game_id}_skaters.csv', 'w', newline='') as skaters_file, \
         open(f'{game_id}_goalies.csv', 'w', newline='') as goalies_file:
        
        skater_writer = csv.DictWriter(skaters_file, fieldnames=skater_headers)
        goalie_writer = csv.DictWriter(goalies_file, fieldnames=goalie_headers)
        
        # Write headers for each game file
        skater_writer.writeheader()
        goalie_writer.writeheader()
        
        # Process each team's data
        for team in games.values():
            # Process skaters
            for position_group in ['forwards', 'defense']:
                if position_group in team:
                    for player_data in team[position_group]:
                        write_player_data(skater_writer, player_data)
            
            # Process goalies
            if 'goalies' in team:
                for goalie_data in team['goalies']:
                    write_player_data(goalie_writer, goalie_data)

def fetch_single_game():
    """Handle single game data fetching."""
    game_id = input("Enter the game ID: ")
    url = f"https://api-web.nhle.com/v1/gamecenter/{game_id}/boxscore"
    response = requests.get(url)
    if response.status_code == 200:
        process_game_data(game_id, response.json(), True)
        print(f"\nData written to {game_id}_skaters.csv and {game_id}_goalies.csv")
    else:
        print(f"Error: Could not fetch game {game_id}")

def fetch_season():
    """Handle entire season data fetching."""
    print("\nWARNING: The NHL API has rate limits. Making too many requests too quickly may result in temporary blocks.")
    print("This script will attempt to get data for all regular season games (~1312 games).")
    print("Press Enter to continue or Ctrl+C to cancel...")
    input()
    
    season_year = input("Enter The Year\n")
    base_game_id = f"{season_year}02"
    
    total_games = 1313
    successful_games = 0
    failed_games = 0
    
    print("\nFetching games data...")
    for game_num in range(1, total_games):
        game_id = f"{base_game_id}{str(game_num).zfill(4)}"
        print(f"\rProgress: {game_num}/{total_games-1} games | Success: {successful_games} | Failed: {failed_games}", end="")
        
        url = f"https://api-web.nhle.com/v1/gamecenter/{game_id}/boxscore"
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"\nGame not found: {game_id}")
            failed_games += 1
            continue
        
        successful_games += 1
        process_game_data(game_id, response.json(), game_num == 1)

def main():
    """Main program execution."""
    choice = get_user_choice()
    if choice == "1":
        fetch_single_game()
    else:
        fetch_season()

if __name__ == "__main__":
    main()
