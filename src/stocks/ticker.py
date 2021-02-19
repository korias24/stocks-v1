# -*- coding: utf-8 -*-

class Ticker:
    def __init__(self, symbol, exchange_code, metadata, data_provider):
        self.symbol = symbol
        self._exchange_code = exchange_code
        self.company = metadata.get('Name', "")
        self.exchange = metadata.get('Exchange', "")
        # dp => data_provider
        self._dp = data_provider

    """
    fd_data => fundamental_data

    TODO: Use this only if needed. Right now, we don't really need it. But we will
    if we need to filter on sector in the future.
    """
    @property
    def fd_data(self):
        return self._dp.fundamental_data(self.symbol, self._exchange_code)

    def eod_data(self, date):
        return self._dp.eod_data(self.symbol, self._exchange_code, date)

    def __str__(self):
        return "(%s, %s, %s)" % (self.symbol, self.company, self.exchange)

    def __repr__(self):
        return self.__str__()

    """
    If I want to take any averages of the data, I'll have to use the ticker-specific EOD
    endpoint. E.g. eod/ticker/from_date_to_date ...

    The files are about 384K for 10 years, ~30K for 1 year. Reading 50k of these files
    doesn't take too long -- about 21 seconds. Can probably do some clever filtering to
    only get the data we need.

    ^ For v1, it is probably good enough to use the bulk data, at least up to the max
    limit (21 in this case?). We can store ~80 MB in memory, so it should be a lot simpler.

    We can add things like charting later. No need for now.

    So, order of filters will matter for performance. Should probably investigate some
    caching strategies in the future.
    """
