from aenum import Enum
from zoneinfo import ZoneInfo


class GameState(Enum):
    _init_ = 'value string'

    SCHEDULED = 1, 'Scheduled'
    PREGAME = 2, 'Pre-game'
    IN_PROGRESS = 3, 'In Progress'
    SUSPENDED = 4, 'Suspended'
    FINAL = 5, 'Final'
    FORFEIT = 6, 'Forfeit'
    UNKNOWN = 7, 'Unknown'
    ERR = 8, 'Error'

    def __str__(self):
        return self.string


_STATUS_CODE_MAPPING = {
    'S': GameState.SCHEDULED,
    'P': GameState.PREGAME,
    'I': GameState.IN_PROGRESS,
    'T': GameState.SUSPENDED,
    'U': GameState.SUSPENDED,
    'F': GameState.FINAL,
    'O': GameState.FINAL,
    'Q': GameState.FORFEIT,
    'R': GameState.FORFEIT,
    'X': GameState.UNKNOWN,
    'W': GameState.UNKNOWN
}


def get_game_state(status_code: str) -> GameState:
    if status_code is not None:
        if status_code.upper() in _STATUS_CODE_MAPPING:
            return _STATUS_CODE_MAPPING.get(status_code)
        else:
            print(f'Unsupported status code: "{status_code}"')
    return GameState.ERR


class InningState(Enum):
    _init_ = 'value string'

    BOTTOM = 1, 'Bot'
    MIDDLE = 2, 'Mid'
    TOP = 3, 'Top'
    END = 4, 'End'
    NONE = 5, 'N/A'

    def __str__(self):
        return self.string


_INNING_STATE_MAPPING = {
    'bottom': InningState.BOTTOM,
    'middle': InningState.MIDDLE,
    'top': InningState.TOP,
    'end': InningState.END
}


def get_inning_state(inning_state: str) -> InningState:
    if inning_state is not None:
        if inning_state.lower() in _INNING_STATE_MAPPING:
            return _INNING_STATE_MAPPING.get(inning_state.lower())
        else:
            print(f'Unsupported inning state: "{inning_state}"')
    return InningState.NONE


class VenueData:
    def __init__(self, data):
        if data is not None:
            self._venue_id: int = data['id']
            self._name: str = data['name']
            if data['location']:
                self._city: str = data['location']['city']
                self._state: str = data['location']['stateAbbrev']
                if data['location']['defaultCoordinates']:
                    self._lat: float = data['location']['defaultCoordinates']['latitude']
                    self._lon: float = data['location']['defaultCoordinates']['longitude']
            if data['timeZone']:
                self._timezone: ZoneInfo = ZoneInfo(data['timeZone']['id'])

    @property
    def venue_id(self) -> int:
        return self._venue_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def city(self) -> str:
        return self._city

    @property
    def state(self) -> str:
        return self._state

    @property
    def latitude(self) -> float:
        return self._lat

    @property
    def longitude(self) -> float:
        return self._lon

    @property
    def timezone(self) -> ZoneInfo:
        return self._timezone


class TeamBoxscoreBattingData:
    def __init__(self, data):
        if data is not None:
            self._runs: int = data['runs']
            self._rbi: int = data['rbi']
            self._hits: int = data['hits']
            self._home_runs: int = data['homeRuns']
            self._avg: str = data['avg']

    @property
    def runs(self) -> int:
        return self._runs

    @property
    def rbi(self) -> int:
        return self._rbi

    @property
    def hits(self) -> int:
        return self._hits

    @property
    def home_runs(self) -> int:
        return self._home_runs

    @property
    def avg(self) -> str:
        return self._avg


class TeamBoxscorePitchingData:
    def __init__(self, data):
        if data is not None:
            self._runs_given: int = data['runs']
            self._obp: str = data['obp']
            self._era: str = data['era']
            self._strike_outs: int = data['strikeOuts']
            self._pitch_count: int = data['pitchesThrown'] if 'pitchesThrown' in data else 0
            self._balls: int = data['balls']
            self._strikes: int = data['strikes']

    @property
    def runs_given(self) -> int:
        return self._runs_given

    @property
    def obp(self) -> str:
        return self._obp

    @property
    def era(self) -> str:
        return self._era

    @property
    def strike_outs(self) -> int:
        return self._strike_outs

    @property
    def pitch_count(self) -> int:
        return self._pitch_count

    @property
    def balls(self) -> int:
        return self._balls

    @property
    def strikes(self) -> int:
        return self._strikes


class TeamBoxscoreData:
    def __init__(self, data):
        if data is not None and data['teamStats'] is not None:
            self._batting: TeamBoxscoreBattingData = TeamBoxscoreBattingData(data['teamStats']['batting'])
            self._pitching: TeamBoxscorePitchingData = TeamBoxscorePitchingData(data['teamStats']['pitching'])

    @property
    def batting(self) -> TeamBoxscoreBattingData:
        return self._batting

    @property
    def pitching(self) -> TeamBoxscorePitchingData:
        return self._pitching


class TeamData:
    def __init__(self, data, boxscore: TeamBoxscoreData):
        if data is not None:
            self._team_id: int = data['id']
            self._name: str = data['name']
            self._team_name: str = data['teamName']
            self._location_name: str = data['locationName']
            if data['record'] and data['record']:
                self._wins: int = data['record']['wins']
                self._losses: int = data['record']['losses']
            self._boxscore: TeamBoxscoreData = boxscore

    @property
    def team_id(self) -> int:
        return self._team_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def team_name(self) -> str:
        return self._team_name

    @property
    def location_name(self) -> str:
        return self._location_name

    @property
    def wins(self) -> int:
        return self._wins

    @property
    def losses(self) -> int:
        return self._losses

    @property
    def runs(self) -> int:
        return self._boxscore.batting.runs

    @property
    def boxscore(self) -> TeamBoxscoreData:
        return self._boxscore


class LinescoreData:
    def __init__(self, data):
        if data is not None:
            self._inning: int = data['currentInning'] if 'currentInning' in data else 0
            self._inning_text: str = data['currentInningOrdinal'] if 'currentInningOrdinal' in data else 'n/a'
            _inning_state_str: str = data['inningState'] if 'inningState' in data else None
            self._inning_state: InningState = get_inning_state(_inning_state_str)
            self._scheduled_innings: int = data['scheduledInnings']
            self._is_top_inning: bool = data['isTopInning'] if 'isTopInning' in data else True
            self._is_runner_on_first: bool = 'first' in data['offense'] if 'offense' in data else False
            self._is_runner_on_second: bool = 'second' in data['offense'] if 'offense' in data else False
            self._is_runner_on_third: bool = 'third' in data['offense'] if 'offense' in data else False

    @property
    def inning(self) -> int:
        if self._inning:
            return self._inning
        return 0

    @property
    def inning_text(self) -> str:
        if self._inning_text != 'n/a':
            return self._inning_text
        elif self._inning:
            print(f'Did not retrieve inning ordinal text, but did receive inning value: {self._inning}')
            return f'{self._inning}'
        return None

    @property
    def inning_state(self) -> str:
        return self._inning_state

    @property
    def scheduled_innings(self) -> int:
        return self._scheduled_innings

    @property
    def is_top_inning(self) -> bool:
        return self._is_top_inning

    @property
    def is_runner_on_first(self) -> bool:
        return self._is_runner_on_first

    @property
    def is_runner_on_second(self) -> bool:
        return self._is_runner_on_second

    @property
    def is_runner_on_third(self) -> bool:
        return self._is_runner_on_third


class CurrentPlayData:
    def __init__(self, data):
        if data is not None and data['count'] is not None:
            self._balls: int = data['count']['balls']
            self._strikes: int = data['count']['strikes']
            self._outs: int = data['count']['outs']

    @property
    def balls(self) -> int:
        return self._balls

    @property
    def strikes(self) -> int:
        return self._strikes

    @property
    def outs(self) -> int:
        return self._outs
