# -*- coding: utf-8 -*-

# TODO: Change this interface later
class Interface:
    """
    Provides EOD data for the given ticker
    """
    def eod_data(self, ticker, exchange, date):
        pass

    def eod_data_range(self, ticker, exchange, from_date, to_date):
        pass

    def fundamental_data(self, ticker, exchange):
        pass
