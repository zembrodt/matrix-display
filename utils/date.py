from datetime import datetime
from zoneinfo import ZoneInfo


def parse_mlb_date(date: str) -> datetime:
    if date is not None:
        try:
            _date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=ZoneInfo('UTC'))
            return _date.astimezone(datetime.now().astimezone().tzinfo)
        except ValueError:
            print(f'Unable to parse date "{date}"')
    return None
