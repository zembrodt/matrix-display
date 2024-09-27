from datetime import datetime, timedelta
from api import MlbApi
from models.mlb import GameState, MlbLiveFeedData, TeamData
from models.mlb.attributes import InningState


class MlbGame:
    def __init__(self, team_name: str):
        self._team_id: int = None
        teams = MlbApi.get_team_id(team_name)
        if len(teams) > 0:
            self._team_id: int = teams[0]
        else:
            print(f'Unable to find a team with name "{team_name}"\nExiting...')
            exit()
        self._current_game_id: int = None
        self._game: MlbLiveFeedData = None

    def get_game(self, date: datetime):
        game_found = False
        retries = 0
        max_retries = 100
        while not game_found and retries < max_retries:
            schedule = MlbApi.get_schedule(date.strftime('%Y-%m-%d'), team_id=self._team_id)
            if len(schedule.dates) > 0 and len(schedule.dates[0].games) > 0:
                self._current_game_id = schedule.dates[0].games[0].gamepk
                game_found = True
            if not game_found:
                print(f'Unable to find a game on {date} for team ID {self._team_id}. Trying previous day...')
                date -= timedelta(days=1)
            retries += 1
        if not game_found:
            print(f'Could not find any games after {max_retries} retries for team ID {self._team_id} starting on date {date}')
            exit()

    def refresh_game(self):
        if self._current_game_id is not None:
            self._game = MlbApi.get_game(self._current_game_id)
            print(f'State during refresh: {self._game.status}')

    @property
    def home_team(self) -> TeamData:
        if self._game is None:
            self.refresh_game()
        return self._game.home

    @property
    def away_team(self) -> TeamData:
        if self._game is None:
            self.refresh_game()
        return self._game.away

    @property
    def game_state(self) -> GameState:
        if self._game is None:
            self.refresh_game()
        return self._game.status

    @property
    def inning(self) -> int:
        if self._game is None:
            self.refresh_game()
        return self._game.linescore.inning

    @property
    def inning_text(self) -> str:
        if self._game is None:
            self.refresh_game()
        return self._game.linescore.inning_text

    @property
    def is_top_of_inning(self) -> bool:
        if self._game is None:
            self.refresh_game()
        return self._game.linescore.is_top_inning

    @property
    def inning_state(self) -> InningState:
        if self._game is None:
            self.refresh_game()
        return self._game.linescore.inning_state

    @property
    def balls(self) -> int:
        if self._game is None:
            self.refresh_game()
        return self._game.balls

    @property
    def strikes(self) -> int:
        if self._game is None:
            self.refresh_game()
        return self._game.strikes

    @property
    def outs(self) -> int:
        if self._game is None:
            self.refresh_game()
        return self._game.outs

    @property
    def is_on_first(self) -> bool:
        if self._game is None:
            self.refresh_game()
        return self._game.linescore.is_runner_on_first

    @property
    def is_on_second(self) -> bool:
        if self._game is None:
            self.refresh_game()
        return self._game.linescore.is_runner_on_second

    @property
    def is_on_third(self) -> bool:
        if self._game is None:
            self.refresh_game()
        return self._game.linescore.is_runner_on_third

    @property
    def game_time(self) -> datetime:
        return self._game.game_time

    @property
    def start_time(self) -> str:
        if self._game is None:
            self.refresh_game()
        if self._game.game_time is not None:
            return f'{int(self._game.game_time.strftime("%I"))}:{self._game.game_time.strftime("%M")}{self._game.game_time.strftime("%p").lower()}'
        return '--:--'

    @property
    def game_data(self) -> MlbLiveFeedData:
        if self._game is None:
            self.refresh_game()
        return self._game
