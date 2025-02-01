# NHL API CSV Extractor

## How to Find a Game ID

1. Go to [NHL.com/scores](https://www.nhl.com/scores)
2. Find the game you want
3. Click on the game to open its page
4. Look at the URL, for example:
   ```
   https://www.nhl.com/gamecenter/bos-vs-wpg/2025/01/30/2024020812
   ```
5. The Game ID is the last number in the URL (in this example: `2024020812`)

## Usage

1. Run the script
2. Choose between:
   - Single Game (Option 1)
   - Entire Regular Season (Option 2)
3. Follow the prompts to enter the required information

## Output

The script will generate CSV files containing:
- Skater statistics
- Goalie statistics

## Note

The NHL API has rate limits. When fetching an entire season (~1300 games), the process may take some time and could be interrupted if too many requests are made too quickly.