from datetime import datetime
from utils.date import parse_mlb_date
from .attributes import GameState, TeamData, VenueData, LinescoreData, TeamBoxscoreData, CurrentPlayData, get_game_state


class MlbLiveFeedData:
    def __init__(self, game_id: int, data):
        self._game_id: int = game_id
        print(f'Creating game with id {game_id}')

        away_boxscore: TeamBoxscoreData = None
        home_boxscore: TeamBoxscoreData = None
        live_data = data['liveData']
        if live_data:
            if live_data['linescore']:
                self._linescore: LinescoreData = LinescoreData(live_data['linescore'])
            if live_data['boxscore'] and live_data['boxscore']['teams']:
                away_boxscore = TeamBoxscoreData(live_data['boxscore']['teams']['away'])
                home_boxscore = TeamBoxscoreData(live_data['boxscore']['teams']['home'])
            if live_data['plays'] and 'currentPlay' in live_data['plays']:
                self._current_play = CurrentPlayData(live_data['plays']['currentPlay'])

        game_data = data['gameData']
        if game_data:
            if game_data['datetime'] and game_data['datetime']['dateTime']:
                self._game_time: datetime = parse_mlb_date(game_data['datetime']['dateTime'])
            if game_data['status']:
                self._game_state: GameState = get_game_state(game_data['status']['codedGameState'])
                if self._game_state == GameState.ERR:
                    print(f'Unhandled game status found for object: {game_data["status"]}')
            if game_data['teams']:
                if game_data['teams']['away']:
                    self._away_team: TeamData = TeamData(game_data['teams']['away'], away_boxscore)
                if game_data['teams']['home']:
                    self._home_team: TeamData = TeamData(game_data['teams']['home'], home_boxscore)
            if game_data['venue']:
                self._venue: VenueData = VenueData(game_data['venue'])

    @property
    def game_id(self) -> int:
        return self._game_id

    @property
    def game_time(self) -> datetime:
        return self._game_time

    @property
    def status(self) -> GameState:
        return self._game_state

    @property
    def away(self) -> TeamData:
        return self._away_team

    @property
    def home(self) -> TeamData:
        return self._home_team

    @property
    def linescore(self) -> LinescoreData:
        return self._linescore

    @property
    def current_play(self) -> CurrentPlayData:
        return self._current_play

    @property
    def balls(self) -> int:
        if self._current_play:
            return self._current_play.balls
        return 0

    @property
    def strikes(self) -> int:
        if self._current_play:
            return self._current_play.strikes
        return 0

    @property
    def outs(self) -> int:
        if self._current_play:
            return self._current_play.outs
        return 0

    @property
    def venue(self) -> VenueData:
        return self._venue
