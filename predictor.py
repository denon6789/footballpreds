import os
import numpy as np
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('FOOTBALL_API_KEY')
API_BASE = 'https://api.football-data.org/v4'

class ScorePredictor:
    def __init__(self):
        self.session = requests.Session()
        if API_KEY:
            self.session.headers.update({'X-Auth-Token': API_KEY})

    def get_team_id(self, team_name):
        # Search for team by name
        resp = self.session.get(f'{API_BASE}/teams')
        teams = resp.json().get('teams', [])
        for team in teams:
            if team_name.lower() in team['name'].lower():
                return team['id']
        return None

    def get_team_stats(self, team_name):
        team_id = self.get_team_id(team_name)
        if not team_id:
            # Fallback: random stats
            return {'avg_for': 1.3 + np.random.rand()/2, 'avg_against': 1.0 + np.random.rand()/2}
        # Get last 5 matches
        url = f'{API_BASE}/teams/{team_id}/matches?limit=5&status=FINISHED'
        resp = self.session.get(url)
        matches = resp.json().get('matches', [])
        goals_for, goals_against = 0, 0
        count = 0
        for match in matches:
            if match['homeTeam']['id'] == team_id:
                goals_for += match['score']['fullTime']['home']
                goals_against += match['score']['fullTime']['away']
            else:
                goals_for += match['score']['fullTime']['away']
                goals_against += match['score']['fullTime']['home']
            count += 1
        avg_for = goals_for / count if count else 1.2
        avg_against = goals_against / count if count else 1.1
        return {'avg_for': avg_for, 'avg_against': avg_against}

    def predict_score(self, home_team, away_team):
        # Get stats
        home = self.get_team_stats(home_team)
        away = self.get_team_stats(away_team)
        # Poisson-based prediction
        home_goals = np.random.poisson(lam=(home['avg_for'] + away['avg_against'])/2)
        away_goals = np.random.poisson(lam=(away['avg_for'] + home['avg_against'])/2)
        return int(home_goals), int(away_goals)
