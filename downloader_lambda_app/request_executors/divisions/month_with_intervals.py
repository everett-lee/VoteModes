class DateInterval:
    def __init__(self, open: str, close: str):
        self.open = open
        self.close = close

    def __str__(self):
        return "Open: {open}, Close: {close}".format(open=self.open, close=self.close)


class MonthWithIntervals:
    def __init__(self, month: int, year: int):
        self.first_interval = self.get_first_interval(month, year)
        self.second_interval = self.get_second_interval(month, year)
        self.third_interval = self.get_third_interval(month, year)
        self.get_interval_list = [
            self.first_interval,
            self.second_interval,
            self.third_interval,
        ]

    @staticmethod
    def month_to_str(int_month: int) -> str:
        if int_month < 10:
            return "0{month}".format(month=int_month)
        else:
            return "{month}".format(month=int_month)

    def get_first_interval(self, month, year) -> DateInterval:
        month_str = self.month_to_str(month)
        first_open = (
            "{year}-{month}-01".format(year=year, month=month_str)
            if month == 1
            else "{year}-{month}-02".format(year=year, month=month_str)
        )
        first_close = "{year}-{month}-10".format(year=year, month=month_str)

        return DateInterval(first_open, first_close)

    def get_second_interval(self, month, year) -> DateInterval:
        month_str = self.month_to_str(month)
        second_open = "{year}-{month}-11".format(year=year, month=month_str)
        second_close = "{year}-{month}-20".format(year=year, month=month_str)

        return DateInterval(second_open, second_close)

    def get_third_interval(self, month, year) -> DateInterval:
        month_str = self.month_to_str(month)
        next_month_str = self.month_to_str(month + 1)

        third_open = "{year}-{month}-21".format(year=year, month=month_str)
        third_close = (
            "{year}-{month}-01".format(year=year, month=next_month_str)
            if month < 12
            else "{year}-12-31".format(year=year)
        )

        return DateInterval(third_open, third_close)
