import os
import pandas as pd
from datetime import datetime
from predictor import ScorePredictor
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv('FOOTBALL_API_KEY')


def get_first_scheduled_date_and_fixtures():
    url = 'https://api.football-data.org/v4/matches?status=SCHEDULED&limit=100'
    headers = {'X-Auth-Token': API_KEY} if API_KEY else {}
    resp = requests.get(url, headers=headers)
    data = resp.json()
    matches = data.get('matches', [])
    if not matches:
        return None, []
    # Find the earliest date
    matches.sort(key=lambda m: m['utcDate'])
    first_date = matches[0]['utcDate'][:10]
    # Get all fixtures for that date
    fixtures = []
    for match in matches:
        if match['utcDate'][:10] == first_date:
            fixtures.append({
                'home_team': match['homeTeam']['name'],
                'away_team': match['awayTeam']['name'],
                'competition': match['competition']['name'],
                'utc_date': match['utcDate']
            })
    return first_date, fixtures

def main():
    first_date, fixtures = get_first_scheduled_date_and_fixtures()
    if not fixtures:
        print('No scheduled fixtures found.')
        return
    print(f'Predicting for first scheduled date: {first_date}')
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
    df.to_csv(f'predictions_{first_date}.csv', index=False)
    df.to_html(f'predictions_{first_date}.html', index=False)
    print(f'Predictions saved to predictions_{first_date}.csv and .html')

if __name__ == '__main__':
    main()
