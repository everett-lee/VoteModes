from datetime import timedelta

import dateutil.parser


class Division:
    def __init__(self, division: dict, saved_dates: set):
        self.date = self.increment_date(division['Date'].strip(), saved_dates)
        self.division_id = division['DivisionId']
        self.title = division['Title'].strip()
        self.aye_count = division['AyeCount']
        self.no_count = division['NoCount']

    def increment_date(self, old_date: str, saved_dates: set) -> str:
        """
        Division datetime is used as a range key in the database. The time portion
        sometimes gets defaulted to midnight in the source data, resulting in duplicate keys.
        This workaround ensures all datetimes are unique.
        """

        if old_date not in saved_dates:
            return old_date

        old_date_str = dateutil.parser.parse(old_date)
        incremented_date = old_date_str + timedelta(seconds=1)
        return self.increment_date(incremented_date.strftime("%Y-%m-%dT%H:%M:%S%z"), saved_dates)
