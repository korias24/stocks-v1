# -*- coding: utf-8 -*-

class Ticker:
    def __init__(self, symbol, exchange_code, data_provider):
        self.symbol = symbol
        self._exchange_code = exchange_code
        # dp => data_provider
        self._dp = data_provider

    """
    fd_data => fundamental_data
    """
    @property
    def fd_data(self):
        return self._dp.fundamental_data(self.symbol, self._exchange_code)

    def eod_data(self, date):
        return self._dp.eod_data(self.symbol, self._exchange_code, date)

    """
    If I want to take any averages of the data, I'll have to use the ticker-specific EOD
    endpoint. E.g. eod/ticker/from_date_to_date ...

    The files are about 384K for 10 years, ~30K for 1 year. Reading 50k of these files
    doesn't take too long -- about 21 seconds. Can probably do some clever filtering to
    only get the data we need.

    So, order of filters will matter for performance. Should probably investigate some
    caching strategies in the future.
    """
