import mlbstatsapi
import requests
from models.mlb import MlbLiveFeedData


class MlbApi:
    _mlb = mlbstatsapi.Mlb()

    @staticmethod
    def get_game(game_id: int) -> MlbLiveFeedData:
        response = requests.get(f'https://statsapi.mlb.com/api/v1.1/game/{game_id}/feed/live/')
        if response.status_code == 200:
            data = response.json()
            if data:
                return MlbLiveFeedData(game_id, data)
        return None

    @staticmethod
    def get_team_id(team_name: str):
        return MlbApi._mlb.get_team_id(team_name)

    @staticmethod
    def get_schedule(date: str, team_id=None):
        return MlbApi._mlb.get_schedule(date=date, team_id=team_id)
