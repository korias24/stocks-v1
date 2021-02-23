# -*- coding: utf-8 -*-

import datetime
import functools

from stocks.predicate import *

def filter_tickers(p, tickers):
    return {symbol: ticker for symbol, ticker in tickers.items() if p(ticker)}

def andf(*fs):
    def _f(tickers):
        return functools.reduce(lambda _tickers, f: f(_tickers), fs, tickers)

    return _f

# _dictp => dictionary predicate
def _dictp(d, k, p):
    if k in d:
        return p(d[k])
    return False

# NOTE: be careful when doing e.g. gte(0) here, because EODHD will set companies
# with "null" close price to 0 so you may end up including stocks that are actually
# quite expensive
def close(td, np):
    def f(tickers):
        return filter_tickers(lambda t: _dictp(t.eod_data(td), 'close', np), tickers)

    return f

def market_cap(td, np):
    def f(tickers):
        return filter_tickers(lambda t: _dictp(t.eod_data(td), 'MarketCapitalization', np), tickers)

    return f

def exchange(sp):
    def f(tickers):
        return filter_tickers(lambda t: sp(t.exchange), tickers)

    return f

def ignore_exchanges(*exchanges):
    sp = [neql(exchange) for exchange in exchanges]
    sp = andp(*sp)
    return exchange(sp)

def min_volume(v, from_date, to_date, min_satisfying):
    def f(tickers):
        np = gte(v)
        def p(ticker):
            num_satisfying = 0
            delta = to_date - from_date
            for num_days in range(0, delta.days + 1):
                date = from_date + datetime.timedelta(days = num_days)
                if _dictp(ticker.eod_data(date), 'volume', np):
                    num_satisfying = num_satisfying + 1
            return num_satisfying >= min_satisfying

        return filter_tickers(p, tickers)

    return f

def symbol(sp):
    def f(tickers):
        return filter_tickers(lambda t: sp(t.symbol), tickers)

    return f

def ignore_symbols(*symbols):
    sp = [neql(symbol) for symbol in symbols]
    sp = andp(*sp)
    return symbol(sp)

