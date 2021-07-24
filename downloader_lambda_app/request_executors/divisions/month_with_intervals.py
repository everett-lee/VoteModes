class DateInterval:
    def __init__(self, open: str, close: str):
        self.open = open
        self.close = close

    def __str__(self):
        return "Open: {open}, Close: {close}".format(open=self.open, close=self.close)


class MonthWithIntervals:
    def __init__(self, month: int, year: int):
        self.month = month
        self.month_str = self.month_to_str(month)
        self.year = year
        self.first_interval = self.get_first_interval()
        self.second_interval = self.get_second_interval()
        self.third_interval = self.get_third_interval()
        self.get_interval_list = [self.first_interval, self.second_interval, self.third_interval]

    @staticmethod
    def month_to_str(int_month: int) -> str:
        if int_month < 10:
            return "0{month}".format(month=int_month)
        else:
            return "{month}".format(month=int_month)

    def get_first_interval(self) -> DateInterval:
        first_open = '{year}-{month}-01'.format(year=self.year, month=self.month_str) if self.month == 1 \
            else '{year}-{month}-02'.format(year=self.year, month=self.month_str)
        first_close = '{year}-{month}-10'.format(year=self.year, month=self.month_str)

        return DateInterval(first_open, first_close)

    def get_second_interval(self) -> DateInterval:
        second_open = '{year}-{month}-11'.format(year=self.year, month=self.month_str)
        second_close = '{year}-{month}-20'.format(year=self.year, month=self.month_str)

        return DateInterval(second_open, second_close)

    def get_third_interval(self) -> DateInterval:
        third_open = '{year}-{month}-21'.format(year=self.year, month=self.month_str)
        third_close = '{year}-{month}-01'.format(year=self.year, month=self.month_to_str(self.month + 1)) if \
            self.month < 12 else '{year}-12-31'.format(year=self.year)

        return DateInterval(third_open, third_close)
