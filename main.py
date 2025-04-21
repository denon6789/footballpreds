import os
import pandas as pd
from datetime import datetime, timedelta
from predictor import ScorePredictor
from dotenv import load_dotenv

# Load API key from .env if present
load_dotenv()
API_KEY = os.getenv('FOOTBALL_API_KEY')

# --- Fetch tomorrow's fixtures ---
def get_tomorrow_fixtures(simulate=False):
    if simulate:
        # Return some sample fixtures for simulation
        return [
            {'home_team': 'Manchester United', 'away_team': 'Liverpool', 'competition': 'Premier League', 'utc_date': '2025-04-22T15:00:00Z'},
            {'home_team': 'Real Madrid', 'away_team': 'Barcelona', 'competition': 'La Liga', 'utc_date': '2025-04-22T19:00:00Z'},
            {'home_team': 'Bayern Munich', 'away_team': 'Borussia Dortmund', 'competition': 'Bundesliga', 'utc_date': '2025-04-22T17:30:00Z'}
        ]
    import requests
    tomorrow = (datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%d')
    url = f'https://api.football-data.org/v4/matches?dateFrom={tomorrow}&dateTo={tomorrow}'
    headers = {'X-Auth-Token': API_KEY} if API_KEY else {}
    resp = requests.get(url, headers=headers)
    data = resp.json()
    fixtures = []
    for match in data.get('matches', []):
        fixtures.append({
            'home_team': match['homeTeam']['name'],
            'away_team': match['awayTeam']['name'],
            'competition': match['competition']['name'],
            'utc_date': match['utcDate']
        })
    return fixtures

# --- Main workflow ---
def main(simulate=False):
    fixtures = get_tomorrow_fixtures(simulate=simulate)
    if not fixtures:
        print('No fixtures found for tomorrow.')
        return
    predictor = ScorePredictor()
    results = []
    for fixture in fixtures:
        pred = predictor.predict_score(fixture['home_team'], fixture['away_team'])
        results.append({
            'Competition': fixture['competition'],
            'Home': fixture['home_team'],
            'Away': fixture['away_team'],
            'Predicted Home': pred[0],
            'Predicted Away': pred[1],
            'Date': fixture['utc_date']
        })
    df = pd.DataFrame(results)
    print(df)
    df.to_csv('tomorrow_predictions.csv', index=False)
    # Output to HTML
    df.to_html('tomorrow_predictions.html', index=False)
    print('HTML results saved to tomorrow_predictions.html')

if __name__ == '__main__':
    import sys
    simulate = '--simulate' in sys.argv
    main(simulate=simulate)
